"""XASSET-0022 -- deterministic generator for the Level-1 application artifact.

Given identical frozen inputs, this generator necessarily produces identical
canonical bytes. It has no wall-clock, environment, filesystem, network,
market-data, holdings, targets, gates, or randomness dependency of any kind.

It chooses NO economic value. Every economic state it writes is a transcription
of a closure already fixed by XASSET-0020/XASSET-0021 under the frozen
snapshot: every pair conclusion and driver direction is `unable_to_determine`,
every sleeve abstains, `point_or_range_or_null` is null, liquidity is
unresolved/null, and unsupported capital stays `UNSIZED_UNASSIGNED_CAPITAL`.

Application authority is WITHHELD. Generation refuses unless the named
application-authorization decision appears in
`level1_application_schema.APPLICATION_AUTHORIZATION_REGISTRY`, which is empty.
No real artifact can be produced today.

Zero import coupling with `allocate.py` / `margin_state.py` in either direction.
"""

from __future__ import annotations

import re

import level1_application_schema as S

_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

# The closed input contract. Any missing or extra top-level input key is a
# hard error -- the generator never fills a gap with a default.
GENERATOR_INPUT_KEYS = frozenset({
    "application_authorization",
    "schema_accepted_head",
    "evidence_attributes",
})

# Per-evidence attributes the caller must supply from governed sources. The
# generator validates their shape but never invents or infers them.
EVIDENCE_ATTRIBUTE_KEYS = frozenset({
    "governing_authority",
    "authority_lifecycle",
    "permitted_question",
    "classification",
    "admission",
    "freshness_state",
    "representation_scope",
    "forbidden_implications",
})


class GeneratorInputError(ValueError):
    """Raised when frozen inputs are missing, extra, or invalid."""


def _check_inputs(frozen_inputs: object) -> dict:
    if not isinstance(frozen_inputs, dict):
        raise GeneratorInputError("frozen_inputs must be a mapping")
    extra = set(frozen_inputs) - GENERATOR_INPUT_KEYS
    missing = GENERATOR_INPUT_KEYS - set(frozen_inputs)
    if extra:
        raise GeneratorInputError(f"unknown frozen input key(s): {sorted(extra)}")
    if missing:
        raise GeneratorInputError(f"missing frozen input key(s): {sorted(missing)}")

    authorization = frozen_inputs["application_authorization"]
    if not isinstance(authorization, dict):
        raise GeneratorInputError("application_authorization must be a mapping")
    if set(authorization) != S.APPLICATION_AUTHORIZATION_KEYS:
        raise GeneratorInputError(
            "application_authorization keys must be exactly "
            f"{sorted(S.APPLICATION_AUTHORIZATION_KEYS)}"
        )
    decision_id = authorization.get("decision_id")
    if not isinstance(decision_id, str) or not decision_id.strip():
        raise GeneratorInputError("application_authorization.decision_id must be a string")
    if authorization.get("authorization_status") != "granted":
        raise GeneratorInputError(
            "application_authorization.authorization_status must be 'granted'; "
            "application authority is WITHHELD"
        )
    # THE HARD GATE, enforced at generation as well as at validation.
    if decision_id not in S.APPLICATION_AUTHORIZATION_REGISTRY:
        raise GeneratorInputError(
            f"application-authorization decision '{decision_id}' is not registered; "
            "application authority is WITHHELD (XASSET-0021 §O double gate)"
        )

    head = frozen_inputs["schema_accepted_head"]
    if not isinstance(head, str) or not _COMMIT_RE.match(head):
        raise GeneratorInputError("schema_accepted_head must be a 40-hex commit SHA")

    attributes = frozen_inputs["evidence_attributes"]
    if not isinstance(attributes, dict):
        raise GeneratorInputError("evidence_attributes must be a mapping")
    expected_ids = set(S.FROZEN_EVIDENCE_BY_ID)
    supplied_ids = set(attributes)
    if supplied_ids != expected_ids:
        raise GeneratorInputError(
            "evidence_attributes must cover exactly the frozen snapshot; "
            f"missing={sorted(expected_ids - supplied_ids)} "
            f"extra={sorted(supplied_ids - expected_ids)}"
        )
    for evidence_id, attrs in attributes.items():
        if not isinstance(attrs, dict):
            raise GeneratorInputError(f"evidence_attributes[{evidence_id}] must be a mapping")
        if set(attrs) != EVIDENCE_ATTRIBUTE_KEYS:
            raise GeneratorInputError(
                f"evidence_attributes[{evidence_id}] keys must be exactly "
                f"{sorted(EVIDENCE_ATTRIBUTE_KEYS)}"
            )
        if attrs["classification"] not in S.EVIDENCE_CLASSIFICATION:
            raise GeneratorInputError(
                f"evidence_attributes[{evidence_id}].classification outside vocabulary"
            )
        if attrs["admission"] not in S.EVIDENCE_ADMISSION:
            raise GeneratorInputError(
                f"evidence_attributes[{evidence_id}].admission outside vocabulary"
            )
        if attrs["freshness_state"] not in S.FRESHNESS_STATE:
            raise GeneratorInputError(
                f"evidence_attributes[{evidence_id}].freshness_state outside vocabulary"
            )
        if not isinstance(attrs["forbidden_implications"], list) or not all(
            isinstance(item, str) for item in attrs["forbidden_implications"]
        ):
            raise GeneratorInputError(
                f"evidence_attributes[{evidence_id}].forbidden_implications must be "
                "a list of strings"
            )
    return frozen_inputs


def _build_trace(evidence_ids: list[str]) -> list[dict]:
    """One fully populated trace, in exactly the canonical step order."""
    return [
        {
            "step_id": step_id,
            "step_index": index,
            "inputs_referenced": evidence_ids,
            "output_recorded": S.TRACE_STEP_REQUIRED_OUTPUT[step_id],
        }
        for index, step_id in enumerate(S.CANONICAL_TRACE_STEP_ORDER)
    ]


def generate_application_document(frozen_inputs: dict) -> dict:
    """Build the artifact document deterministically from frozen inputs."""
    inputs = _check_inputs(frozen_inputs)
    attributes = inputs["evidence_attributes"]

    evidence_rows = sorted(S.FROZEN_EVIDENCE)
    evidence_ids = [row[0] for row in evidence_rows]

    evidence_snapshot = []
    for evidence_id, path, sha, content in evidence_rows:
        attrs = attributes[evidence_id]
        evidence_snapshot.append({
            "evidence_id": evidence_id,
            "path": path,
            "sha256": sha,
            "source_content_sha256": content,
            "governing_authority": attrs["governing_authority"],
            "authority_lifecycle": attrs["authority_lifecycle"],
            "permitted_question": attrs["permitted_question"],
            "classification": attrs["classification"],
            "admission": attrs["admission"],
            "freshness_state": attrs["freshness_state"],
            "representation_scope": attrs["representation_scope"],
            "forbidden_implications": list(attrs["forbidden_implications"]),
        })

    # Every sleeve abstains. This is XASSET-0021 §F's already-closed
    # consequence, consumed, not decided here.
    sleeves = [
        {
            "sleeve_id": sleeve_id,
            "admitted_drivers": [],
            "applicable_constraints": [],
            "disclosures": list(evidence_ids),
            "representation_sensitivity": "required_representation_missing",
            "uncertainty_state": "unable_to_determine",
            "sleeve_vs_unassigned": "no_positive_endpoint_authority",
            "conflict_missingness_state": "determinate_plus_indeterminate",
            "outcome_type": "abstain",
            "point_or_range_or_null": None,
            "deterministic_derivation_trace": _build_trace(evidence_ids),
        }
        for sleeve_id in S.CANONICAL_SLEEVE_ORDER
    ]

    # Every pair concludes unable_to_determine, and every driver class is
    # present and indeterminate. XASSET-0021 §D, consumed not decided.
    pairs = []
    for pair_id in S.CANONICAL_PAIR_ORDER:
        left, right = S.CANONICAL_PAIR_MEMBERS[pair_id]
        pairs.append({
            "canonical_pair_id": pair_id,
            "self_sleeve": left,
            "counterpart_sleeve": right,
            "direct_evidence": [],
            "driver_ledger": [
                {
                    "driver_class": driver_class,
                    "direction": "unable_to_determine",
                    "missingness": "missing_no_accepted_record",
                    "conflict_state": "determinate_plus_indeterminate",
                    "evidence_refs": [],
                }
                for driver_class in S.CANONICAL_DRIVER_CLASS_ORDER
            ],
            "missing_conflicting_stale_evidence": [],
            "constraint_effects": [],
            "conclusion": "unable_to_determine",
        })

    return {
        "schema_identity": dict(S.SCHEMA_IDENTITY),
        "methodology_identity": dict(S.METHODOLOGY_IDENTITY),
        "prerequisite_identity": {
            "closure_decision_id": S.CLOSURE_IDENTITY["decision_id"],
            "closure_accepted_head": S.CLOSURE_IDENTITY["accepted_head"],
            "closure_merge_commit": S.CLOSURE_IDENTITY["merge_commit"],
            "schema_decision_id": "XASSET-0022",
            "schema_accepted_head": inputs["schema_accepted_head"],
        },
        "application_authorization": dict(inputs["application_authorization"]),
        "evidence_snapshot_identity": {
            "snapshot_id": S.SNAPSHOT_ID,
            "source_count": S.FROZEN_EVIDENCE_COUNT,
            "source_tree_identity": S.SOURCE_TREE_IDENTITY,
            "evidence_manifest_sha256": S.EVIDENCE_MANIFEST_SHA256,
        },
        "normalized_asset_state": {
            "denominator_identity": S.DENOMINATOR_IDENTITY,
            "separately_governed_liquidity_state": {
                "status": "unresolved_not_entered_into_application_ledger",
                "numeric_value": None,
            },
            "debt_excluded": True,
        },
        "evidence_snapshot": evidence_snapshot,
        "sleeves": sleeves,
        "pairs": pairs,
        "portfolio_reconciliation": {
            "exact_feasible_set_or_point": None,
            "unsized_unassigned_capital": {
                "symbol": S.UNSIZED_UNASSIGNED_CAPITAL_SYMBOL,
                "deployment_status": "prohibited_without_future_governance",
            },
            "constraint_clipping_to_unassigned": [],
            "reconciliation_identity": S.RECONCILIATION_IDENTITY_TEXT,
            "reconciliation_state": "exact_symbolic_identity_holds",
        },
        "reopen_triggers": list(S.CANONICAL_REOPEN_TRIGGER_ORDER),
        "authority_boundary": {
            "provisional_not_adopted": True,
            "no_policy_effect": True,
            "no_level2_effect": True,
            "no_liquidity_or_debt_effect": True,
        },
    }


def generate_application_bytes(frozen_inputs: dict) -> bytes:
    """The one lawful byte form for these frozen inputs."""
    return S.canonical_bytes(generate_application_document(frozen_inputs))


if __name__ == "__main__":
    import sys

    print(
        "level1_application_generator: application authority is WITHHELD "
        f"(registry size {len(S.APPLICATION_AUTHORIZATION_REGISTRY)}); "
        "no artifact can be generated."
    )
    sys.exit(0)
