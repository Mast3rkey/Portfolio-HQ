"""XASSET-0022 -- fail-closed validator for the Level-1 application artifact.

Enforces the exact schema, canonical serialization, closed vocabularies,
canonical ordering, deterministic trace, reopen-trigger set, non-circular
lifecycle binding, and frozen-evidence identity defined by
`level1_application_schema`.

This validator is MECHANICAL authority only. It never decides an economic
question, never chooses an endpoint, never selects a representation, and never
grants application authority. It consumes the closed states that XASSET-0020
and XASSET-0021 already fixed and rejects anything else.

Application authority is WITHHELD. `APPLICATION_AUTHORIZATION_REGISTRY` is
empty, so every artifact is rejected today regardless of its other contents.

Zero import coupling with `allocate.py` / `margin_state.py` in either
direction. Reads no holdings, targets, gates, weights, margin state, prices, or
network data.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import level1_application_schema as S

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class _NonStandardConstant(ValueError):
    """Raised when JSON input carries NaN / Infinity / -Infinity."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name

# ── Independent adversarial scans ────────────────────────────────────────
#
# These are a second, materially different mechanism from the structural
# schema checks: the structural checks walk the closed key sets, while these
# walk every string value and key name in the document tree regardless of
# where it sits. Neither delegates to the other.

# §M item 28 -- a field that purports to carry the SHA of its own containing
# commit. The closed key sets already bar these names; this is defence in
# depth against a future schema edit reintroducing one.
_SELF_REFERENTIAL_KEY_NAMES = frozenset({
    "exact_head",
    "application_exact_head",
    "self_commit",
    "self_commit_sha",
    "containing_commit",
    "containing_commit_sha",
    "artifact_commit_sha",
    "own_commit_sha",
    "this_commit",
})

# §L item 5 -- no wall-clock or author-chosen metadata in canonical bytes.
_NONDETERMINISTIC_KEY_NAMES = frozenset({
    "generated_at",
    "generated_at_utc",
    "created_at",
    "timestamp",
    "frozen_at",
    "run_at",
    "executed_at",
    "author",
    "author_name",
    "reviewer",
    "reviewed_by",
    "hostname",
    "machine",
    "tmpdir",
    "temp_path",
    "branch",
    "branch_name",
    "environment",
})

# §M item 17 -- score/optimizer machinery in any form.
_FORBIDDEN_SCORE_KEY_NAMES = frozenset({
    "score",
    "confidence",
    "confidence_pct",
    "confidence_percentage",
    "tally",
    "utility",
    "weighting",
    "weight",
    "weights",
    "rank",
    "ranking",
    "optimizer",
    "solver",
    "grid",
    "sweep",
    "target_pct",
    "sleeve_weight",
    "allocation_pct",
})

# §M items 7 and 16 -- legacy or current allocation anchors.
_LEGACY_ANCHOR_TOKENS = (
    "18.67",
    "14.67",
    "16.67",
    "33.32",
    "XASSET-0016",
    "XASSET-0018",
    "holdings.yaml",
    "targets.yaml",
    "gates.yaml",
    "current_weight",
    "current_target",
    "current_holding",
    "incumbency",
)

# §M item 10 -- unclosed materiality judgment.
_UNCLOSED_JUDGMENT_TOKENS = (
    "material",
    "significant",
    "sufficient",
    "meaningful",
    "reasonable",
)

# §M item 19 -- policy/adoption/deployment/trading language.
_POLICY_TOKENS = (
    "adopt",
    "adoption",
    "deploy",
    "deployment",
    "rebalance",
    "trade",
    "order",
    "buy",
    "sell",
    "trim",
    "purchase",
    "brokerage",
)

# §M item 18 -- Level-2 leakage.
_LEVEL2_TOKENS = ("level-2", "level 2", "level2", "instrument_sizing", "refreeze")

# Chart/technical-analysis leakage.
_CHART_TOKENS = (
    "support level",
    "resistance",
    "breakout",
    "trend line",
    "moving average",
    "rsi",
    "macd",
    "candlestick",
    "chart pattern",
    "technical analysis",
    "oversold",
    "overbought",
    "fibonacci",
)

def _iter_strings(value: object, path: str):
    """Yield (json_path, string) for every string value in the tree."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, sub in value.items():
            yield from _iter_strings(sub, f"{path}.{key}")
    elif isinstance(value, list):
        for index, sub in enumerate(value):
            yield from _iter_strings(sub, f"{path}[{index}]")


def _iter_keys(value: object, path: str):
    """Yield (json_path, key_name) for every mapping key in the tree."""
    if isinstance(value, dict):
        for key, sub in value.items():
            yield path, key
            yield from _iter_keys(sub, f"{path}.{key}")
    elif isinstance(value, list):
        for index, sub in enumerate(value):
            yield from _iter_keys(sub, f"{path}[{index}]")


def _scan_forbidden_key_names(document: object, errors: list[str]) -> None:
    for where, key in _iter_keys(document, "$"):
        lowered = key.lower()
        if lowered in _SELF_REFERENTIAL_KEY_NAMES:
            errors.append(
                f"{where}: self-referential lifecycle field '{key}' is barred "
                "(XASSET-0021 §L item 8 / §M item 28)"
            )
        if lowered in _NONDETERMINISTIC_KEY_NAMES:
            errors.append(
                f"{where}: nondeterministic metadata field '{key}' is barred "
                "from canonical bytes (XASSET-0021 §L item 5)"
            )
        if lowered in _FORBIDDEN_SCORE_KEY_NAMES:
            errors.append(
                f"{where}: score/optimizer/allocation field '{key}' is barred "
                "(XASSET-0021 §M item 17)"
            )


def _scan_free_text(document: object, errors: list[str]) -> None:
    """Scan genuinely free-text string values for forbidden tokens.

    A string that is EXACTLY a governed identifier defined by the schema is a
    closed-vocabulary value, already checked against its own vocabulary at its
    own position, so it is not free text and is skipped here. That keeps
    governed identifiers such as `diversification_cobehavior` (which contains
    the substring "rsi") and `liquidity_or_level2_boundary_changed` (which
    contains "level2") from producing false positives, without weakening any
    check on the free-text fields these scans exist to police.
    """
    for where, text in _iter_strings(document, "$"):
        if text in S.GOVERNED_IDENTIFIERS:
            continue
        lowered = text.lower()
        for token in _LEGACY_ANCHOR_TOKENS:
            if token.lower() in lowered:
                errors.append(f"{where}: legacy/current allocation anchor '{token}'")
        for token in _POLICY_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", lowered):
                errors.append(f"{where}: policy/deployment/trading token '{token}'")
        for token in _LEVEL2_TOKENS:
            if token in lowered:
                errors.append(f"{where}: Level-2 leakage token '{token}'")
        for token in _UNCLOSED_JUDGMENT_TOKENS:
            if re.search(rf"\b{re.escape(token)}\w*", lowered):
                errors.append(f"{where}: unclosed judgment token '{token}'")
        for token in _CHART_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", lowered):
                errors.append(f"{where}: chart/technical-analysis token '{token}'")


# ── Result types ─────────────────────────────────────────────────────────


@dataclass
class ValidationResult:
    source: str
    valid: bool
    errors: list[str] = field(default_factory=list)


@dataclass
class DirectoryValidationResult:
    valid: bool
    record_count: int
    results: list[ValidationResult] = field(default_factory=list)


# ── Generic helpers ──────────────────────────────────────────────────────


def _reject_unknown_keys(
    value: dict, where: str, allowed: frozenset[str], errors: list[str]
) -> None:
    extra = set(value) - allowed
    if extra:
        errors.append(f"{where}: unknown key(s) {sorted(extra)}")
    missing = allowed - set(value)
    if missing:
        errors.append(f"{where}: missing required key(s) {sorted(missing)}")


def _require_mapping(value: object, where: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{where}: must be a mapping, got {type(value).__name__}")
        return False
    return True


def _require_list(value: object, where: str, errors: list[str]) -> bool:
    if not isinstance(value, list):
        errors.append(f"{where}: must be a list, got {type(value).__name__}")
        return False
    return True


def _require_enum(
    value: object, where: str, vocabulary: frozenset[str], errors: list[str]
) -> None:
    if not isinstance(value, str):
        errors.append(f"{where}: must be a string, got {type(value).__name__}")
    elif value not in vocabulary:
        errors.append(f"{where}: '{value}' is outside the closed vocabulary")


def _require_exact(value: object, where: str, expected: object, errors: list[str]) -> None:
    """Type-strict exact comparison.

    Python equality alone is unsafe here: `False == 0` and `True == 1`, so a
    plain `!=` would accept byte-distinct encodings of a governed boolean or
    integer. Requiring identical concrete types first makes bool and int
    mutually unsatisfiable, so each governed value has exactly one lawful
    encoding.
    """
    if type(value) is not type(expected) or value != expected:
        errors.append(
            f"{where}: must be exactly {expected!r} ({type(expected).__name__}), "
            f"got {value!r} ({type(value).__name__})"
        )


def _require_str_list(value: object, where: str, errors: list[str]) -> None:
    if not _require_list(value, where, errors):
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{where}[{index}]: must be a string")


# ── Section validators ───────────────────────────────────────────────────


def _validate_schema_identity(data: object, errors: list[str]) -> None:
    if not _require_mapping(data, "$.schema_identity", errors):
        return
    _reject_unknown_keys(data, "$.schema_identity", S.SCHEMA_IDENTITY_KEYS, errors)
    for key, expected in S.SCHEMA_IDENTITY.items():
        if key in data:
            _require_exact(data[key], f"$.schema_identity.{key}", expected, errors)


def _validate_methodology_identity(data: object, errors: list[str]) -> None:
    if not _require_mapping(data, "$.methodology_identity", errors):
        return
    _reject_unknown_keys(
        data, "$.methodology_identity", S.METHODOLOGY_IDENTITY_KEYS, errors
    )
    for key, expected in S.METHODOLOGY_IDENTITY.items():
        if key in data:
            _require_exact(data[key], f"$.methodology_identity.{key}", expected, errors)


def _validate_prerequisite_identity(data: object, errors: list[str]) -> None:
    if not _require_mapping(data, "$.prerequisite_identity", errors):
        return
    _reject_unknown_keys(
        data, "$.prerequisite_identity", S.PREREQUISITE_IDENTITY_KEYS, errors
    )
    _require_exact(
        data.get("closure_decision_id"),
        "$.prerequisite_identity.closure_decision_id",
        S.CLOSURE_IDENTITY["decision_id"],
        errors,
    )
    _require_exact(
        data.get("closure_accepted_head"),
        "$.prerequisite_identity.closure_accepted_head",
        S.CLOSURE_IDENTITY["accepted_head"],
        errors,
    )
    _require_exact(
        data.get("closure_merge_commit"),
        "$.prerequisite_identity.closure_merge_commit",
        S.CLOSURE_IDENTITY["merge_commit"],
        errors,
    )
    _require_exact(
        data.get("schema_decision_id"),
        "$.prerequisite_identity.schema_decision_id",
        "XASSET-0022",
        errors,
    )
    # XASSET-0022's own accepted head is pinned by the future application
    # authorization decision, not by this module (which cannot know the SHA of
    # a commit that does not exist yet). Format is enforced here; the exact
    # value is bound at authorization time.
    head = data.get("schema_accepted_head")
    if not isinstance(head, str) or not _COMMIT_RE.match(head):
        errors.append(
            "$.prerequisite_identity.schema_accepted_head: must be a 40-hex commit SHA"
        )


def _validate_application_authorization(data: object, errors: list[str]) -> None:
    if not _require_mapping(data, "$.application_authorization", errors):
        return
    _reject_unknown_keys(
        data, "$.application_authorization", S.APPLICATION_AUTHORIZATION_KEYS, errors
    )
    _require_enum(
        data.get("authorization_status"),
        "$.application_authorization.authorization_status",
        S.AUTHORIZATION_STATUS,
        errors,
    )
    decision_id = data.get("decision_id")
    if not isinstance(decision_id, str) or not decision_id.strip():
        errors.append("$.application_authorization.decision_id: must be a non-empty string")
        return
    # THE HARD GATE. An artifact may exist only under a granted authorization,
    # and a granted authorization must be registered. The registry is empty, so
    # this rejects every artifact until a separate governance decision lands.
    if data.get("authorization_status") != "granted":
        errors.append(
            "$.application_authorization: an artifact may exist only under "
            "authorization_status 'granted'; application authority is WITHHELD"
        )
    if decision_id not in S.APPLICATION_AUTHORIZATION_REGISTRY:
        errors.append(
            f"$.application_authorization.decision_id: '{decision_id}' is not a "
            "registered application-authorization decision; application "
            "authority is WITHHELD (XASSET-0021 §O double gate)"
        )


def _validate_authorization_head_binding(data: dict, errors: list[str]) -> None:
    """Bind the registered authorization to the exact XASSET-0022 accepted head.

    Registry membership alone is insufficient: the artifact's
    `prerequisite_identity.schema_accepted_head` must equal the head the
    registry binds to that decision, so no arbitrary 40-hex value validates.
    """
    authorization = data.get("application_authorization")
    prerequisite = data.get("prerequisite_identity")
    if not isinstance(authorization, dict) or not isinstance(prerequisite, dict):
        return
    decision_id = authorization.get("decision_id")
    if not isinstance(decision_id, str):
        return
    expected_head = S.APPLICATION_AUTHORIZATION_REGISTRY.get(decision_id)
    if expected_head is None:
        return  # already reported by the registry gate above
    if prerequisite.get("schema_accepted_head") != expected_head:
        errors.append(
            "$.prerequisite_identity.schema_accepted_head: does not match the "
            f"head bound to '{decision_id}' by the application-authorization "
            "registry"
        )


def _validate_evidence_snapshot_identity(data: object, errors: list[str]) -> None:
    if not _require_mapping(data, "$.evidence_snapshot_identity", errors):
        return
    _reject_unknown_keys(
        data, "$.evidence_snapshot_identity", S.EVIDENCE_SNAPSHOT_IDENTITY_KEYS, errors
    )
    _require_exact(
        data.get("snapshot_id"),
        "$.evidence_snapshot_identity.snapshot_id",
        S.SNAPSHOT_ID,
        errors,
    )
    _require_exact(
        data.get("source_count"),
        "$.evidence_snapshot_identity.source_count",
        S.FROZEN_EVIDENCE_COUNT,
        errors,
    )
    _require_exact(
        data.get("source_tree_identity"),
        "$.evidence_snapshot_identity.source_tree_identity",
        S.SOURCE_TREE_IDENTITY,
        errors,
    )
    _require_exact(
        data.get("evidence_manifest_sha256"),
        "$.evidence_snapshot_identity.evidence_manifest_sha256",
        S.EVIDENCE_MANIFEST_SHA256,
        errors,
    )


def _validate_normalized_asset_state(data: object, errors: list[str]) -> None:
    if not _require_mapping(data, "$.normalized_asset_state", errors):
        return
    _reject_unknown_keys(
        data, "$.normalized_asset_state", S.NORMALIZED_ASSET_STATE_KEYS, errors
    )
    _require_exact(
        data.get("denominator_identity"),
        "$.normalized_asset_state.denominator_identity",
        S.DENOMINATOR_IDENTITY,
        errors,
    )
    _require_exact(
        data.get("debt_excluded"), "$.normalized_asset_state.debt_excluded", True, errors
    )
    liquidity = data.get("separately_governed_liquidity_state")
    where = "$.normalized_asset_state.separately_governed_liquidity_state"
    if not _require_mapping(liquidity, where, errors):
        return
    _reject_unknown_keys(liquidity, where, S.LIQUIDITY_STATE_KEYS, errors)
    _require_enum(liquidity.get("status"), f"{where}.status", S.LIQUIDITY_STATUS, errors)
    # Null, never zero. A numeric zero would silently size liquidity.
    if liquidity.get("numeric_value") is not None:
        errors.append(
            f"{where}.numeric_value: must be null while liquidity is unresolved; "
            "zero or any number would silently size liquidity (XASSET-0021 §I)"
        )
    if liquidity.get("status") != "unresolved_not_entered_into_application_ledger":
        errors.append(
            f"{where}.status: liquidity remains unresolved under this snapshot"
        )


def _validate_evidence_snapshot(data: object, errors: list[str]) -> None:
    if not _require_list(data, "$.evidence_snapshot", errors):
        return
    if len(data) != S.FROZEN_EVIDENCE_COUNT:
        errors.append(
            f"$.evidence_snapshot: must contain exactly {S.FROZEN_EVIDENCE_COUNT} "
            f"entries, got {len(data)}"
        )
    expected_order = [e["evidence_id"] for e in S.FROZEN_EVIDENCE_LEDGER]
    seen: list[str] = []
    for index, entry in enumerate(data):
        where = f"$.evidence_snapshot[{index}]"
        if not _require_mapping(entry, where, errors):
            continue
        _reject_unknown_keys(entry, where, S.EVIDENCE_ENTRY_KEYS, errors)
        evidence_id = entry.get("evidence_id")
        if not isinstance(evidence_id, str):
            errors.append(f"{where}.evidence_id: must be a string")
            continue
        seen.append(evidence_id)
        frozen = S.FROZEN_EVIDENCE_LEDGER_BY_ID.get(evidence_id)
        if frozen is None:
            errors.append(
                f"{where}.evidence_id: '{evidence_id}' is not in the frozen "
                "XASSET-0021 §C snapshot"
            )
            continue
        # Every field is frozen or mechanically derived, so exact equality is
        # required on all of them. Nothing here is caller discretion.
        for key in sorted(S.EVIDENCE_ENTRY_KEYS):
            _require_exact(entry.get(key), f"{where}.{key}", frozen[key], errors)
    if len(set(seen)) != len(seen):
        errors.append("$.evidence_snapshot: duplicate evidence_id")
    if seen != expected_order:
        errors.append(
            "$.evidence_snapshot: entries must appear in canonical evidence_id order"
        )


def _validate_trace(data: object, where: str, errors: list[str]) -> None:
    if not _require_list(data, where, errors):
        return
    if len(data) != len(S.CANONICAL_TRACE_STEP_ORDER):
        errors.append(
            f"{where}: must contain exactly {len(S.CANONICAL_TRACE_STEP_ORDER)} "
            f"steps, got {len(data)}"
        )
        return
    for index, step in enumerate(data):
        step_where = f"{where}[{index}]"
        if not _require_mapping(step, step_where, errors):
            continue
        _reject_unknown_keys(step, step_where, S.TRACE_STEP_KEYS, errors)
        expected_id = S.CANONICAL_TRACE_STEP_ORDER[index]
        _require_exact(step.get("step_id"), f"{step_where}.step_id", expected_id, errors)
        _require_exact(step.get("step_index"), f"{step_where}.step_index", index, errors)
        _require_exact(
            step.get("output_recorded"),
            f"{step_where}.output_recorded",
            S.TRACE_STEP_REQUIRED_OUTPUT[expected_id],
            errors,
        )
        _require_str_list(
            step.get("inputs_referenced"), f"{step_where}.inputs_referenced", errors
        )


def _validate_sleeves(data: object, errors: list[str]) -> None:
    if not _require_list(data, "$.sleeves", errors):
        return
    if len(data) != len(S.CANONICAL_SLEEVE_ORDER):
        errors.append(
            f"$.sleeves: must contain exactly {len(S.CANONICAL_SLEEVE_ORDER)} "
            f"sleeves, got {len(data)}"
        )
        return
    for index, sleeve in enumerate(data):
        where = f"$.sleeves[{index}]"
        if not _require_mapping(sleeve, where, errors):
            continue
        _reject_unknown_keys(sleeve, where, S.SLEEVE_KEYS, errors)
        _require_exact(
            sleeve.get("sleeve_id"),
            f"{where}.sleeve_id",
            S.CANONICAL_SLEEVE_ORDER[index],
            errors,
        )
        _require_enum(
            sleeve.get("representation_sensitivity"),
            f"{where}.representation_sensitivity",
            S.REPRESENTATION_STATE,
            errors,
        )
        _require_enum(
            sleeve.get("uncertainty_state"),
            f"{where}.uncertainty_state",
            S.UNCERTAINTY_STATE,
            errors,
        )
        _require_enum(
            sleeve.get("sleeve_vs_unassigned"),
            f"{where}.sleeve_vs_unassigned",
            S.SLEEVE_VS_UNASSIGNED,
            errors,
        )
        _require_enum(
            sleeve.get("conflict_missingness_state"),
            f"{where}.conflict_missingness_state",
            S.CONFLICT_STATE,
            errors,
        )
        _require_enum(
            sleeve.get("outcome_type"), f"{where}.outcome_type", S.SLEEVE_OUTCOME_TYPE, errors
        )
        _require_str_list(sleeve.get("admitted_drivers"), f"{where}.admitted_drivers", errors)
        _require_str_list(
            sleeve.get("applicable_constraints"), f"{where}.applicable_constraints", errors
        )
        _require_str_list(sleeve.get("disclosures"), f"{where}.disclosures", errors)
        _validate_trace(
            sleeve.get("deterministic_derivation_trace"),
            f"{where}.deterministic_derivation_trace",
            errors,
        )


def _validate_pairs(data: object, errors: list[str]) -> None:
    if not _require_list(data, "$.pairs", errors):
        return
    if len(data) != len(S.CANONICAL_PAIR_ORDER):
        errors.append(
            f"$.pairs: must contain exactly {len(S.CANONICAL_PAIR_ORDER)} pairs, "
            f"got {len(data)}"
        )
        return
    for index, pair in enumerate(data):
        where = f"$.pairs[{index}]"
        if not _require_mapping(pair, where, errors):
            continue
        _reject_unknown_keys(pair, where, S.PAIR_KEYS, errors)
        expected_id = S.CANONICAL_PAIR_ORDER[index]
        _require_exact(
            pair.get("canonical_pair_id"), f"{where}.canonical_pair_id", expected_id, errors
        )
        left, right = S.CANONICAL_PAIR_MEMBERS[expected_id]
        # A reversed pair is not expressible: members are pinned to canonical
        # sleeve order.
        _require_exact(pair.get("self_sleeve"), f"{where}.self_sleeve", left, errors)
        _require_exact(
            pair.get("counterpart_sleeve"), f"{where}.counterpart_sleeve", right, errors
        )
        _require_enum(pair.get("conclusion"), f"{where}.conclusion", S.PAIR_CONCLUSION, errors)
        _require_str_list(pair.get("direct_evidence"), f"{where}.direct_evidence", errors)
        _require_str_list(
            pair.get("missing_conflicting_stale_evidence"),
            f"{where}.missing_conflicting_stale_evidence",
            errors,
        )
        _validate_driver_ledger(pair.get("driver_ledger"), f"{where}.driver_ledger", errors)
        _validate_constraint_effects(
            pair.get("constraint_effects"), f"{where}.constraint_effects", errors
        )


def _validate_driver_ledger(data: object, where: str, errors: list[str]) -> None:
    if not _require_list(data, where, errors):
        return
    if len(data) != len(S.CANONICAL_DRIVER_CLASS_ORDER):
        errors.append(
            f"{where}: must contain exactly {len(S.CANONICAL_DRIVER_CLASS_ORDER)} "
            f"driver classes, got {len(data)}"
        )
        return
    for index, entry in enumerate(data):
        entry_where = f"{where}[{index}]"
        if not _require_mapping(entry, entry_where, errors):
            continue
        _reject_unknown_keys(entry, entry_where, S.DRIVER_LEDGER_ENTRY_KEYS, errors)
        _require_exact(
            entry.get("driver_class"),
            f"{entry_where}.driver_class",
            S.CANONICAL_DRIVER_CLASS_ORDER[index],
            errors,
        )
        _require_enum(
            entry.get("direction"), f"{entry_where}.direction", S.DRIVER_DIRECTION, errors
        )
        _require_enum(
            entry.get("missingness"), f"{entry_where}.missingness", S.MISSINGNESS_STATE, errors
        )
        _require_enum(
            entry.get("conflict_state"),
            f"{entry_where}.conflict_state",
            S.CONFLICT_STATE,
            errors,
        )
        _require_str_list(entry.get("evidence_refs"), f"{entry_where}.evidence_refs", errors)


def _validate_constraint_effects(data: object, where: str, errors: list[str]) -> None:
    if not _require_list(data, where, errors):
        return
    for index, entry in enumerate(data):
        entry_where = f"{where}[{index}]"
        if not _require_mapping(entry, entry_where, errors):
            continue
        _reject_unknown_keys(entry, entry_where, S.CONSTRAINT_EFFECT_KEYS, errors)
        _require_enum(entry.get("state"), f"{entry_where}.state", S.CONSTRAINT_STATE, errors)
        if not isinstance(entry.get("constraint_id"), str):
            errors.append(f"{entry_where}.constraint_id: must be a string")
        _require_str_list(entry.get("evidence_refs"), f"{entry_where}.evidence_refs", errors)


def _validate_portfolio_reconciliation(data: object, errors: list[str]) -> None:
    where = "$.portfolio_reconciliation"
    if not _require_mapping(data, where, errors):
        return
    _reject_unknown_keys(data, where, S.PORTFOLIO_RECONCILIATION_KEYS, errors)
    _require_exact(
        data.get("reconciliation_identity"),
        f"{where}.reconciliation_identity",
        S.RECONCILIATION_IDENTITY_TEXT,
        errors,
    )
    _require_enum(
        data.get("reconciliation_state"),
        f"{where}.reconciliation_state",
        S.RECONCILIATION_STATE,
        errors,
    )
    if data.get("reconciliation_state") != "exact_symbolic_identity_holds":
        errors.append(
            f"{where}.reconciliation_state: a reconciliation requiring a plug or "
            "producing a negative complement invalidates the artifact"
        )
    unassigned = data.get("unsized_unassigned_capital")
    u_where = f"{where}.unsized_unassigned_capital"
    if _require_mapping(unassigned, u_where, errors):
        _reject_unknown_keys(unassigned, u_where, S.UNSIZED_UNASSIGNED_CAPITAL_KEYS, errors)
        _require_exact(
            unassigned.get("symbol"),
            f"{u_where}.symbol",
            S.UNSIZED_UNASSIGNED_CAPITAL_SYMBOL,
            errors,
        )
        _require_enum(
            unassigned.get("deployment_status"),
            f"{u_where}.deployment_status",
            S.UNASSIGNED_DEPLOYMENT_STATUS,
            errors,
        )
    _require_str_list(
        data.get("constraint_clipping_to_unassigned"),
        f"{where}.constraint_clipping_to_unassigned",
        errors,
    )


def _validate_reopen_triggers(data: object, errors: list[str]) -> None:
    where = "$.reopen_triggers"
    if not _require_list(data, where, errors):
        return
    if list(data) != list(S.CANONICAL_REOPEN_TRIGGER_ORDER):
        errors.append(
            f"{where}: must be exactly the closed reopen-trigger identifier set "
            "in canonical order"
        )


def _validate_authority_boundary(data: object, errors: list[str]) -> None:
    where = "$.authority_boundary"
    if not _require_mapping(data, where, errors):
        return
    _reject_unknown_keys(data, where, S.AUTHORITY_BOUNDARY_KEYS, errors)
    _require_exact(
        data.get("provisional_not_adopted"),
        f"{where}.provisional_not_adopted",
        True,
        errors,
    )
    for key in ("no_policy_effect", "no_level2_effect", "no_liquidity_or_debt_effect"):
        _require_exact(data.get(key), f"{where}.{key}", True, errors)


def _validate_frozen_snapshot_abstention(data: dict, errors: list[str]) -> None:
    """Enforce XASSET-0021 §§D/E/F under the frozen snapshot.

    These are transcriptions of already-accepted closures, not new economics:
    §F fixes point and range eligibility as APPLICATION_MUST_ABSTAIN for every
    sleeve and requires `point_or_range_or_null` to remain null; §D fixes every
    pair conclusion at `unable_to_determine`. The rule is gated on the frozen
    snapshot identity so a future, separately governed snapshot is unaffected.
    """
    identity = data.get("evidence_snapshot_identity")
    if not isinstance(identity, dict) or identity.get("snapshot_id") != S.SNAPSHOT_ID:
        return
    sleeves = data.get("sleeves")
    if isinstance(sleeves, list):
        for index, sleeve in enumerate(sleeves):
            if not isinstance(sleeve, dict):
                continue
            where = f"$.sleeves[{index}]"
            if sleeve.get("outcome_type") != "abstain":
                errors.append(
                    f"{where}.outcome_type: no lawful Level-1 endpoint authority "
                    "exists under the frozen snapshot; must be 'abstain' "
                    "(XASSET-0021 §F)"
                )
            if sleeve.get("point_or_range_or_null") is not None:
                errors.append(
                    f"{where}.point_or_range_or_null: must remain null under the "
                    "frozen snapshot (XASSET-0021 §F)"
                )
            if sleeve.get("uncertainty_state") != "unable_to_determine":
                errors.append(
                    f"{where}.uncertainty_state: must remain 'unable_to_determine' "
                    "(XASSET-0021 §K)"
                )
            if sleeve.get("sleeve_vs_unassigned") != "no_positive_endpoint_authority":
                errors.append(
                    f"{where}.sleeve_vs_unassigned: no positive endpoint authority "
                    "exists under the frozen snapshot (XASSET-0021 §F)"
                )
    pairs = data.get("pairs")
    if isinstance(pairs, list):
        for index, pair in enumerate(pairs):
            if not isinstance(pair, dict):
                continue
            if pair.get("conclusion") != "unable_to_determine":
                errors.append(
                    f"$.pairs[{index}].conclusion: every pair conclusion is "
                    "'unable_to_determine' under the frozen snapshot "
                    "(XASSET-0021 §D)"
                )
            ledger = pair.get("driver_ledger")
            if isinstance(ledger, list):
                for d_index, entry in enumerate(ledger):
                    if isinstance(entry, dict) and entry.get("direction") != "unable_to_determine":
                        errors.append(
                            f"$.pairs[{index}].driver_ledger[{d_index}].direction: "
                            "no admitted direct-comparative source determines "
                            "marginal preference (XASSET-0021 §D)"
                        )


# ── Public API ───────────────────────────────────────────────────────────


def validate_application_document(data: object) -> ValidationResult:
    """Validate a parsed artifact document against the closed schema."""
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("$: artifact must be a mapping")
        return ValidationResult(source="<document>", valid=False, errors=errors)

    _reject_unknown_keys(data, "$", S.TOP_LEVEL_KEYS, errors)
    if S.contains_float(data):
        errors.append(
            "$: floats are barred from canonical bytes; an exact numeric must be "
            "an exact-precision string with NUM-0001 provenance"
        )
    _scan_forbidden_key_names(data, errors)
    _scan_free_text(data, errors)

    _validate_schema_identity(data.get("schema_identity"), errors)
    _validate_methodology_identity(data.get("methodology_identity"), errors)
    _validate_prerequisite_identity(data.get("prerequisite_identity"), errors)
    _validate_application_authorization(data.get("application_authorization"), errors)
    _validate_evidence_snapshot_identity(data.get("evidence_snapshot_identity"), errors)
    _validate_normalized_asset_state(data.get("normalized_asset_state"), errors)
    _validate_evidence_snapshot(data.get("evidence_snapshot"), errors)
    _validate_sleeves(data.get("sleeves"), errors)
    _validate_pairs(data.get("pairs"), errors)
    _validate_portfolio_reconciliation(data.get("portfolio_reconciliation"), errors)
    _validate_reopen_triggers(data.get("reopen_triggers"), errors)
    _validate_authority_boundary(data.get("authority_boundary"), errors)
    _validate_authorization_head_binding(data, errors)
    _validate_frozen_snapshot_abstention(data, errors)

    return ValidationResult(source="<document>", valid=not errors, errors=errors)


def validate_application_bytes(raw: bytes, source: str = "<bytes>") -> ValidationResult:
    """Validate raw artifact bytes, including exact canonical byte identity.

    The byte-identity check is independent of the generator: the bytes are
    parsed and re-serialized through the canonical serializer, then compared.
    Any alternate encoding, newline, whitespace, key ordering, duplicate key,
    or noncanonical null/numeric form fails here.
    """
    errors: list[str] = []
    if raw.startswith(b"\xef\xbb\xbf"):
        return ValidationResult(source=source, valid=False, errors=["$: UTF-8 BOM is barred"])
    if b"\r" in raw:
        return ValidationResult(
            source=source, valid=False, errors=["$: CR byte present; newline must be LF only"]
        )
    try:
        text = raw.decode(S.ENCODING)
    except UnicodeDecodeError as exc:
        return ValidationResult(source=source, valid=False, errors=[f"$: not valid UTF-8: {exc}"])

    duplicate_keys: list[str] = []

    def _object_pairs_hook(pairs):
        keys = [k for k, _ in pairs]
        if len(set(keys)) != len(keys):
            duplicate_keys.append(str(sorted(keys)))
        return dict(pairs)

    def _reject_constant(name: str):
        # `json.loads` accepts the non-standard NaN/Infinity/-Infinity literals
        # by default. Rejecting them at parse time keeps them a structured
        # validation failure rather than an uncaught serializer crash later.
        raise _NonStandardConstant(name)

    try:
        data = json.loads(
            text,
            object_pairs_hook=_object_pairs_hook,
            parse_constant=_reject_constant,
        )
    except _NonStandardConstant as exc:
        return ValidationResult(
            source=source,
            valid=False,
            errors=[f"$: non-standard JSON constant '{exc.name}' is barred"],
        )
    except json.JSONDecodeError as exc:
        return ValidationResult(source=source, valid=False, errors=[f"$: invalid JSON: {exc}"])
    if duplicate_keys:
        errors.append(f"$: duplicate key(s) present in {duplicate_keys[0]}")

    result = validate_application_document(data)
    errors.extend(result.errors)

    try:
        canonical = S.canonical_bytes(data)
    except ValueError as exc:
        return ValidationResult(
            source=source,
            valid=False,
            errors=errors + [f"$: content is not canonically serializable: {exc}"],
        )
    if raw != canonical:
        errors.append(
            "$: bytes are not the canonical serialization of their own content "
            "(ordering, whitespace, encoding, newline, or numeric/null form)"
        )
    return ValidationResult(source=source, valid=not errors, errors=errors)


def validate_application_file(path: Path) -> ValidationResult:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return ValidationResult(source=str(path), valid=False, errors=[f"unreadable: {exc}"])
    if path.name != Path(S.CANONICAL_ARTIFACT_PATH).name:
        return ValidationResult(
            source=str(path),
            valid=False,
            errors=[
                f"filename must be '{Path(S.CANONICAL_ARTIFACT_PATH).name}', got '{path.name}'"
            ],
        )
    return validate_application_bytes(raw, source=str(path))


def validate_level1_application_directory(directory: Path) -> DirectoryValidationResult:
    """Validate the application directory.

    A missing or empty directory is a valid zero-coverage state, matching every
    sibling Intelligence validator's filesystem-as-index doctrine. No
    application exists today and none is authorized.
    """
    if not directory.exists():
        return DirectoryValidationResult(valid=True, record_count=0, results=[])
    results = [
        validate_application_file(p) for p in sorted(directory.glob("*.json"))
    ]
    return DirectoryValidationResult(
        valid=all(r.valid for r in results), record_count=len(results), results=results
    )


if __name__ == "__main__":
    import sys

    _root = Path(__file__).resolve().parent
    _result = validate_level1_application_directory(_root / "intelligence" / "level1_application")
    if _result.valid:
        print(f"level1_application_validator: OK ({_result.record_count} artifact(s))")
        sys.exit(0)
    print("level1_application_validator: FAILED")
    for _r in _result.results:
        if not _r.valid:
            for _err in _r.errors:
                print(f"  - [{_r.source}] {_err}")
    sys.exit(1)
