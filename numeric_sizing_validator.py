"""Read-only validator for XASSET-0018 schema-2.0 Level-1 numeric sizing.

The validator first runs the authoritative profile, relationship, and policy
validators.  It then reconstructs the complete permitted numeric-sizing
payload from those validated structured sources.  Stored records are compared
recursively with that reconstruction; unrestricted prose is therefore not an
authority surface and coordinated rehashing cannot legitimize invalid content.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
import re
from typing import Any

import yaml

from level1_sleeve_synthesis_validator import (
    canonical_record_hash,
    compute_axis_b,
    compute_expected_sizing_readiness,
    compute_live_relationship_ledger,
    validate_policy_adoption_directory,
    validate_sleeve_profile_directory,
    validate_sleeve_relationship_directory,
)

SCHEMA_VERSION = "2.0"
NUMERIC_DIR = Path("intelligence/level1_sleeve_synthesis/numeric_sizing")
PROFILE_DIR = Path("intelligence/level1_sleeve_synthesis/profiles")
POLICY_DIR = Path("intelligence/level1_sleeve_synthesis/policy_adoption")
RELATIONSHIP_DIR = Path("intelligence/level1_sleeve_synthesis/relationships")

SLEEVE_ORDER = (
    "cash_reserve",
    "crypto",
    "debt_reduction",
    "equity",
    "fund_broad_market",
    "fund_gld_defensive",
)
PRESERVED_ASSIGNED = (
    "crypto",
    "equity",
    "fund_broad_market",
    "fund_gld_defensive",
)
PRESERVED_BLOCKED = ("cash_reserve", "debt_reduction")
RULE_ORDER = ("R2", "R3")
CONDITION_TYPE_ORDER = (
    "evidence_partial_present",
    "forced_abstention_present",
    "overlap_or_duplication_disclosed",
)
RELATIONSHIP_ORDER = (
    "cash_reserve_debt_reduction",
    "cash_reserve_equity",
    "crypto_equity",
    "crypto_fund_gld_defensive",
    "debt_reduction_equity",
    "equity_fund_broad_market",
    "equity_fund_gld_defensive",
)
R3_EVIDENCE_RELATIONSHIPS = tuple(
    relation for relation in RELATIONSHIP_ORDER
    if relation != "cash_reserve_debt_reduction"
)
GOVERNING_DECISIONS = ["XASSET-0016", "XASSET-0017", "XASSET-0018"]
SHARD_ID = "xasset-0018-numeric-sizing-structural-replacement"
READY = {"sizing_conditionally_ready", "sizing_ready"}
BASELINE = Decimal("16.67")
INCREMENT = Decimal("2.00")
TOTAL = Decimal("100.00")

RECORD_KEYS = (
    "schema_version", "sleeve_id", "source_authority",
    "numeric_target_status", "provisional_target_pct",
    "starting_baseline_pct", "applied_adjustments",
    "governing_rule_ids", "target_classification", "review_conditions",
    "uncertainty_assertions", "comparative_provenance",
    "blocking_reason_refs", "authority_boundaries", "record_status",
    "sealed_at", "governing_decisions", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
)
MANIFEST_KEYS = (
    "schema_version", "governing_decisions", "cohort",
    "portfolio_reconciliation",
)
SOURCE_AUTHORITY_KEYS = (
    "source_validation_profile", "source_validation_required",
    "numeric_source_field_allowlist", "profile_references",
    "policy_adoption_references", "relationship_references",
)
AUTHORITY_REFERENCE_KEYS = (
    "source_kind", "source_record_id", "source_path",
    "source_content_sha256",
)
TRIGGER_REFERENCE_KEYS = AUTHORITY_REFERENCE_KEYS + ("selector", "projection")
UNCERTAINTY_REFERENCE_KEYS = TRIGGER_REFERENCE_KEYS + (
    "selector_key", "counterpart_sleeve_id",
)
ADJUSTMENT_KEYS = (
    "governing_rule_id", "direction", "magnitude_pct", "evidence_refs",
)
ASSERTION_KEYS = ("assertion_type", "source_ref", "numeric_effect")
COMPARATIVE_KEYS = (
    "counterpart_sleeve_id", "target_relation", "self_rule_states",
    "counterpart_rule_states", "differing_rule_ids", "cancellation_status",
)
BLOCKING_KEYS = (
    "reason_code", "other_sleeve_id", "source_kind", "source_record_id",
    "source_path", "source_content_sha256", "source_entry_selector",
)
BOUNDARY_KEYS = (
    "scope_level", "policy_status", "level_2_sizing_authority",
    "allocation_check_authority", "portfolio_config_mutation_authority",
    "brokerage_execution_authority", "margin_or_leverage_input",
    "chart_or_deployment_input",
)
MANIFEST_ROW_KEYS = (
    "sleeve_id", "record_path", "content_sha256", "schema_version",
    "governing_decisions", "numeric_target_status",
    "drafting_session_or_shard_id", "sealed_at",
)
RECONCILIATION_KEYS = (
    "sum_of_assigned_targets_pct", "unsized_reserved_capital_pct",
    "portfolio_total_pct", "reconciliation_identity_holds",
    "assigned_record_count", "blocked_record_count", "residual_classification",
)
RESIDUAL_KEYS = (
    "residual_type", "sleeve_id", "cash_reserve_equivalence",
    "redistribution_status", "policy_target_status",
)

REVIEW_CONDITIONS = [
    {"condition_type": "first_descriptive_risk_analysis", "governed_subject": "provisional_target"},
    {"condition_type": "first_targeted_sizing_backtest", "governed_subject": "provisional_target"},
    {"condition_type": "material_sleeve_population_change", "governed_subject": "provisional_target"},
    {"condition_type": "material_relationship_accounting_change", "governed_subject": "provisional_target"},
    {"condition_type": "baseline_specific_evidence_or_calibration_study", "governed_subject": "starting_baseline"},
    {"condition_type": "increment_specific_evidence_or_calibration_study", "governed_subject": "adjustment_increment"},
]
AUTHORITY_BOUNDARIES = {
    "scope_level": "level_1_sleeve_only",
    "policy_status": "provisional_not_adopted",
    "level_2_sizing_authority": "prohibited",
    "allocation_check_authority": "prohibited",
    "portfolio_config_mutation_authority": "prohibited",
    "brokerage_execution_authority": "prohibited",
    "margin_or_leverage_input": "prohibited",
    "chart_or_deployment_input": "prohibited",
}
BLOCKING_REASON_ORDER = {
    "axis_b_not_eligible": 0,
    "sealed_unresolved_relationship": 1,
    "deferred_relationship_pair": 2,
    "secondary_condition_present": 3,
}
PRESERVED_TARGETS = {
    "equity": "18.67",
    "fund_broad_market": "14.67",
    "fund_gld_defensive": "16.67",
    "crypto": "16.67",
}
PERCENT_RE = re.compile(r"^[0-9]+\.[0-9]{2}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


class SourceValidationError(ValueError):
    """The upstream authority chain is invalid or outside the preservation fence."""


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _source_path(kind: str, record_id: str) -> str:
    roots = {
        "sleeve_profile": PROFILE_DIR,
        "policy_adoption": POLICY_DIR,
        "sleeve_relationship": RELATIONSHIP_DIR,
    }
    return str(roots[kind] / f"{record_id}.yaml")


def _source_errors(repo_root: Path) -> list[str]:
    results = (
        ("profile", validate_sleeve_profile_directory(repo_root / PROFILE_DIR, repo_root=repo_root)),
        ("relationship", validate_sleeve_relationship_directory(repo_root / RELATIONSHIP_DIR, repo_root=repo_root)),
        ("policy_adoption", validate_policy_adoption_directory(repo_root / POLICY_DIR, repo_root=repo_root)),
    )
    errors: list[str] = []
    for kind, directory_result in results:
        for result in directory_result.results:
            errors.extend(f"{kind} source [{result.source}]: {error}" for error in result.errors)
    return errors


def _load_exact_sources(repo_root: Path) -> dict[str, dict[str, dict]]:
    errors = _source_errors(repo_root)
    if errors:
        raise SourceValidationError("\n".join(errors))
    sources = {"sleeve_profile": {}, "policy_adoption": {}, "sleeve_relationship": {}}
    for sleeve_id in SLEEVE_ORDER:
        sources["sleeve_profile"][sleeve_id] = _load(repo_root / PROFILE_DIR / f"{sleeve_id}.yaml")
        sources["policy_adoption"][sleeve_id] = _load(repo_root / POLICY_DIR / f"{sleeve_id}.yaml")
    for relation_id in RELATIONSHIP_ORDER:
        relation = _load(repo_root / RELATIONSHIP_DIR / f"{relation_id}.yaml")
        pair = relation["sleeve_pair"]
        derived_id = f"{pair['sleeve_a']}_{pair['sleeve_b']}"
        if derived_id != relation_id:
            raise SourceValidationError(f"relationship identity mismatch: {relation_id} != {derived_id}")
        sources["sleeve_relationship"][relation_id] = relation
    return sources


def _authority_ref(sources: dict, kind: str, record_id: str) -> dict:
    data = sources[kind][record_id]
    return {
        "source_kind": kind,
        "source_record_id": record_id,
        "source_path": _source_path(kind, record_id),
        "source_content_sha256": canonical_record_hash(data),
    }


def _trigger_ref(sources: dict, kind: str, record_id: str, selector: str, projection: str) -> dict:
    return {
        **_authority_ref(sources, kind, record_id),
        "selector": selector,
        "projection": projection,
    }


def _uncertainty_ref(
    sources: dict,
    kind: str,
    record_id: str,
    selector: str,
    projection: str,
    selector_key: dict | None,
    counterpart_sleeve_id: str | None,
) -> dict:
    return {
        **_trigger_ref(sources, kind, record_id, selector, projection),
        "selector_key": selector_key,
        "counterpart_sleeve_id": counterpart_sleeve_id,
    }


def _other_endpoint(relation: dict, sleeve_id: str) -> str:
    pair = relation["sleeve_pair"]
    if pair["sleeve_a"] == sleeve_id:
        return pair["sleeve_b"]
    if pair["sleeve_b"] == sleeve_id:
        return pair["sleeve_a"]
    raise ValueError(f"{sleeve_id} is not an endpoint")


def derive_rule_states(values: dict[str, int]) -> dict[str, str]:
    """Apply the strict unique-extreme rule, with ties suppressing a fire."""
    if not values:
        raise ValueError("rule population cannot be empty")
    low, high = min(values.values()), max(values.values())
    low_unique = list(values.values()).count(low) == 1
    high_unique = list(values.values()).count(high) == 1
    return {
        sleeve_id: (
            "up" if value == low and low_unique
            else "down" if value == high and high_unique
            else "no_fire"
        )
        for sleeve_id, value in values.items()
    }


def distinct_condition_breadth(condition_groups: list[list[str]]) -> int:
    """R3 counts distinct governed types, never repeated occurrences."""
    return len({condition for group in condition_groups for condition in group})


def derive_numeric_state(repo_root: Path, *, enforce_preservation: bool = True) -> dict:
    """Validate sources and independently derive Axis B/C, R2, R3, and targets."""
    sources = _load_exact_sources(repo_root)
    sizing: dict[str, str] = {}
    for sleeve_id in SLEEVE_ORDER:
        profile = sources["sleeve_profile"][sleeve_id]
        policy = sources["policy_adoption"][sleeve_id]
        axis_b = compute_axis_b(profile["evidence_coverage_profile"])
        ledger = compute_live_relationship_ledger(sleeve_id, repo_root)
        sizing[sleeve_id] = compute_expected_sizing_readiness(
            policy["portfolio_function_status"], axis_b, ledger
        )
    assigned = tuple(sleeve_id for sleeve_id in SLEEVE_ORDER if sizing[sleeve_id] in READY)
    blocked = tuple(sleeve_id for sleeve_id in SLEEVE_ORDER if sizing[sleeve_id] not in READY)
    if enforce_preservation and (assigned != PRESERVED_ASSIGNED or blocked != PRESERVED_BLOCKED):
        raise SourceValidationError(
            f"XASSET-0018 preservation fence changed: assigned={assigned}, blocked={blocked}"
        )

    deferred_counts = {
        sleeve_id: sum(
            entry["coverage_state"] == "deferred_disclosed"
            for entry in sources["policy_adoption"][sleeve_id]["relationship_coverage_ledger"]
        )
        for sleeve_id in assigned
    }
    condition_groups: dict[str, list[list[str]]] = {sleeve_id: [] for sleeve_id in assigned}
    for relation_id in R3_EVIDENCE_RELATIONSHIPS:
        relation = sources["sleeve_relationship"][relation_id]
        for sleeve_id in assigned:
            pair = relation["sleeve_pair"]
            if sleeve_id in (pair["sleeve_a"], pair["sleeve_b"]):
                condition_groups[sleeve_id].append(relation["secondary_conditions"])
    condition_sets = {
        sleeve_id: {condition for group in condition_groups[sleeve_id] for condition in group}
        for sleeve_id in assigned
    }
    breadth = {
        sleeve_id: distinct_condition_breadth(condition_groups[sleeve_id])
        for sleeve_id in assigned
    }
    r2 = derive_rule_states(deferred_counts)
    r3 = derive_rule_states(breadth)
    rule_states = {sleeve_id: {"R2": r2[sleeve_id], "R3": r3[sleeve_id]} for sleeve_id in assigned}
    targets: dict[str, str] = {}
    for sleeve_id in assigned:
        net = Decimal("0.00")
        for state in rule_states[sleeve_id].values():
            if state == "up":
                net += INCREMENT
            elif state == "down":
                net -= INCREMENT
        targets[sleeve_id] = f"{(BASELINE + net).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN):.2f}"
    if enforce_preservation and targets != PRESERVED_TARGETS:
        raise SourceValidationError(f"XASSET-0018 numeric preservation fence changed: {targets}")
    return {
        "sources": sources,
        "sizing": sizing,
        "assigned": assigned,
        "blocked": blocked,
        "deferred_counts": deferred_counts,
        "condition_sets": condition_sets,
        "breadth": breadth,
        "rule_states": rule_states,
        "targets": targets,
    }


def _source_authority(state: dict) -> dict:
    sources = state["sources"]
    return {
        "source_validation_profile": "profile_relationship_policy_chain_v1",
        "source_validation_required": True,
        "numeric_source_field_allowlist": "axis_b_c_r2_r3_structured_fields_v1",
        "profile_references": [_authority_ref(sources, "sleeve_profile", sid) for sid in SLEEVE_ORDER],
        "policy_adoption_references": [_authority_ref(sources, "policy_adoption", sid) for sid in SLEEVE_ORDER],
        "relationship_references": [_authority_ref(sources, "sleeve_relationship", rid) for rid in RELATIONSHIP_ORDER],
    }


def _adjustments(state: dict, sleeve_id: str) -> list[dict]:
    sources = state["sources"]
    result: list[dict] = []
    for rule_id in RULE_ORDER:
        direction = state["rule_states"][sleeve_id][rule_id]
        if direction == "no_fire":
            continue
        if rule_id == "R2":
            refs = [
                _trigger_ref(
                    sources, "policy_adoption", assigned_id,
                    "relationship_coverage_ledger.deferred_disclosed_count", "integer_count",
                )
                for assigned_id in state["assigned"]
            ]
        else:
            refs = [
                _trigger_ref(
                    sources, "sleeve_relationship", relation_id,
                    "secondary_conditions.distinct_type_set", "sorted_secondary_condition_type_set",
                )
                for relation_id in R3_EVIDENCE_RELATIONSHIPS
            ]
        result.append({
            "governing_rule_id": rule_id,
            "direction": direction,
            "magnitude_pct": "2.00",
            "evidence_refs": refs,
        })
    return result


def _policy_assertions(state: dict, sleeve_id: str) -> list[dict]:
    sources = state["sources"]
    policy = sources["policy_adoption"][sleeve_id]
    entries = sorted(
        policy["blocking_evidence"],
        key=lambda entry: (
            BLOCKING_REASON_ORDER[entry["reason_type"]],
            SLEEVE_ORDER.index(entry["other_sleeve_id"]) if entry["other_sleeve_id"] else -1,
        ),
    )
    return [
        {
            "assertion_type": "policy_blocking_evidence",
            "source_ref": _uncertainty_ref(
                sources, "policy_adoption", sleeve_id,
                "policy.blocking_evidence.entry", "reason_code_counterpart_reference_state",
                {"reason_code": entry["reason_type"], "other_sleeve_id": entry["other_sleeve_id"]},
                entry["other_sleeve_id"],
            ),
            "numeric_effect": "none",
        }
        for entry in entries
    ]


def _relationship_assertions(state: dict, sleeve_id: str) -> list[dict]:
    sources = state["sources"]
    secondary: list[dict] = []
    maturity: list[dict] = []
    for relation_id in RELATIONSHIP_ORDER:
        relation = sources["sleeve_relationship"][relation_id]
        pair = relation["sleeve_pair"]
        if sleeve_id not in (pair["sleeve_a"], pair["sleeve_b"]):
            continue
        counterpart = _other_endpoint(relation, sleeve_id)
        for condition_type in CONDITION_TYPE_ORDER:
            if condition_type in relation["secondary_conditions"]:
                secondary.append({
                    "assertion_type": "relationship_secondary_condition",
                    "source_ref": _uncertainty_ref(
                        sources, "sleeve_relationship", relation_id,
                        "relationship.secondary_conditions.entry", "condition_presence",
                        {"condition_type": condition_type}, counterpart,
                    ),
                    "numeric_effect": "none",
                })
        if relation["primary_disposition"] == "stronger_evidence_maturity":
            maturity.append({
                "assertion_type": "stronger_evidence_maturity",
                "source_ref": _uncertainty_ref(
                    sources, "sleeve_relationship", relation_id,
                    "relationship.primary_disposition.stronger_evidence_maturity", "presence_only",
                    None, counterpart,
                ),
                "numeric_effect": "none",
            })
    return secondary + maturity


def _profile_assertions(state: dict, sleeve_id: str) -> list[dict]:
    sources = state["sources"]
    specs: list[tuple[str, str, str]] = []
    abstentions = sources["sleeve_profile"][sleeve_id]["abstention_index"]
    if sleeve_id == "equity":
        equity_predicates = (
            lambda entry: entry.get("source_layer") == "valuation_results"
            and entry.get("field_path") == "result_status" and entry.get("value") == "partial",
            lambda entry: entry.get("source_layer") == "valuation_evidence"
            and entry.get("field_path") == "discount_rate_evidence" and entry.get("value") == "abstained",
        )
        if any(sum(bool(predicate(entry)) for entry in abstentions) != 1 for predicate in equity_predicates):
            raise SourceValidationError("equity profile assertion selector did not resolve exactly once")
        specs.extend((
            ("level2_valuation_coverage_gap", "profile.abstention.equity_valuation_result_partial", "presence_only"),
            ("level2_valuation_coverage_gap", "profile.abstention.equity_discount_rate_abstained", "presence_only"),
        ))
    elif sleeve_id == "crypto":
        correlation_matches = [
            entry for entry in abstentions
            if entry.get("source_layer") == "crypto_classification"
            and entry.get("field_path") == "correlation_and_volatility.cross_coin_correlation_status"
            and entry.get("value") == "not_yet_measured"
        ]
        divergence_matches = [
            entry for entry in abstentions
            if entry.get("source_layer") == "instrument_economic_assessment"
            and entry.get("value") == "unable_to_determine"
            and isinstance(entry.get("field_path"), str)
            and len(entry["field_path"].split(".")) == 3
            and entry["field_path"].endswith(
                ".macro_behavioral_characterization.historical_equity_market_drawdown_behavior"
            )
        ]
        if len(correlation_matches) != 1 or len(divergence_matches) != 1:
            raise SourceValidationError("crypto profile assertion selector did not resolve exactly once")
        specs.extend((
            ("crypto_cross_coin_correlation_abstention", "profile.abstention.crypto_cross_coin_correlation_not_yet_measured", "presence_only"),
            ("crypto_per_coin_historical_divergence", "profile.abstention.crypto_historical_behavior_divergence_present", "presence_only"),
        ))
    return [
        {
            "assertion_type": assertion_type,
            "source_ref": _uncertainty_ref(
                sources, "sleeve_profile", sleeve_id, selector, projection, None, None
            ),
            "numeric_effect": "none",
        }
        for assertion_type, selector, projection in specs
    ]


def _uncertainty_assertions(state: dict, sleeve_id: str) -> list[dict]:
    return (
        _policy_assertions(state, sleeve_id)
        + _relationship_assertions(state, sleeve_id)
        + _profile_assertions(state, sleeve_id)
    )


def _blocking_reason_refs(state: dict, sleeve_id: str) -> list[dict]:
    sources = state["sources"]
    policy = sources["policy_adoption"][sleeve_id]
    entries = sorted(
        policy["blocking_evidence"],
        key=lambda entry: (
            BLOCKING_REASON_ORDER[entry["reason_type"]],
            SLEEVE_ORDER.index(entry["other_sleeve_id"]) if entry["other_sleeve_id"] else -1,
            (
                entry["reference"]["record_path"].rsplit("/", 1)[-1].removesuffix(".yaml")
                if entry["reference"] else ""
            ),
        ),
    )
    result: list[dict] = []
    for entry in entries:
        reason = entry["reason_type"]
        reference = entry["reference"]
        relation_id = None
        mode = "none"
        if reference is not None:
            relation_id = reference["record_path"].rsplit("/", 1)[-1].removesuffix(".yaml")
            mode = "sealed_relationship_hash_pin"
            if relation_id not in RELATIONSHIP_ORDER:
                raise SourceValidationError(f"unknown blocking relationship reference: {relation_id}")
            expected_reference = _authority_ref(sources, "sleeve_relationship", relation_id)
            if (
                reference.get("record_path") != expected_reference["source_path"]
                or reference.get("referenced_content_sha256") != expected_reference["source_content_sha256"]
            ):
                raise SourceValidationError(f"stale blocking relationship reference: {sleeve_id}/{relation_id}")
        legal = (
            reason == "axis_b_not_eligible" and entry["other_sleeve_id"] is None and reference is None
            or reason == "deferred_relationship_pair" and entry["other_sleeve_id"] is not None and reference is None
            or reason in {"sealed_unresolved_relationship", "secondary_condition_present"}
            and entry["other_sleeve_id"] is not None and reference is not None
        )
        if not legal:
            raise SourceValidationError(f"illegal blocking selector combination: {sleeve_id}/{reason}")
        result.append({
            "reason_code": reason,
            "other_sleeve_id": entry["other_sleeve_id"],
            **_authority_ref(sources, "policy_adoption", sleeve_id),
            "source_entry_selector": {
                "reason_type": reason,
                "other_sleeve_id": entry["other_sleeve_id"],
                "reference_mode": mode,
                "relationship_record_id": relation_id,
            },
        })
    return result


def _comparative_rows(state: dict, sleeve_id: str) -> list[dict]:
    rows: list[dict] = []
    self_target = Decimal(state["targets"][sleeve_id])
    self_states = state["rule_states"][sleeve_id]
    for counterpart in state["assigned"]:
        if counterpart == sleeve_id:
            continue
        counterpart_target = Decimal(state["targets"][counterpart])
        counterpart_states = state["rule_states"][counterpart]
        relation = "lower" if self_target < counterpart_target else "higher" if self_target > counterpart_target else "equal"
        differing = [rule for rule in RULE_ORDER if self_states[rule] != counterpart_states[rule]]
        cancellation = "none" if not differing else "cancelled_to_equal" if relation == "equal" else "not_cancelled"
        rows.append({
            "counterpart_sleeve_id": counterpart,
            "target_relation": relation,
            "self_rule_states": {rule: self_states[rule] for rule in RULE_ORDER},
            "counterpart_rule_states": {rule: counterpart_states[rule] for rule in RULE_ORDER},
            "differing_rule_ids": differing,
            "cancellation_status": cancellation,
        })
    return rows


def build_expected_records(repo_root: Path, sealed_at: str) -> tuple[dict[str, dict], dict]:
    """Build the complete authoritative corpus in memory; never writes files."""
    state = derive_numeric_state(repo_root)
    source_authority = _source_authority(state)
    records: dict[str, dict] = {}
    for sleeve_id in SLEEVE_ORDER:
        assigned = sleeve_id in state["assigned"]
        adjustments = _adjustments(state, sleeve_id) if assigned else []
        record = {
            "schema_version": SCHEMA_VERSION,
            "sleeve_id": sleeve_id,
            "source_authority": source_authority,
            "numeric_target_status": "provisional_target_assigned" if assigned else "no_provisional_target_pending_axis_c",
            "provisional_target_pct": state["targets"][sleeve_id] if assigned else None,
            "starting_baseline_pct": "16.67" if assigned else None,
            "applied_adjustments": adjustments,
            "governing_rule_ids": [adjustment["governing_rule_id"] for adjustment in adjustments],
            "target_classification": "provisional_governance_guardrail" if assigned else None,
            "review_conditions": REVIEW_CONDITIONS if assigned else [],
            "uncertainty_assertions": _uncertainty_assertions(state, sleeve_id) if assigned else [],
            "comparative_provenance": _comparative_rows(state, sleeve_id) if assigned else [],
            "blocking_reason_refs": [] if assigned else _blocking_reason_refs(state, sleeve_id),
            "authority_boundaries": AUTHORITY_BOUNDARIES,
            "record_status": "sealed",
            "sealed_at": sealed_at,
            "governing_decisions": GOVERNING_DECISIONS,
            "drafting_session_or_shard_id": SHARD_ID,
            "content_sha256": "",
            "cohort_manifest_entry": f"{NUMERIC_DIR}/COHORT_MANIFEST.yaml#{sleeve_id}",
        }
        record["content_sha256"] = canonical_record_hash(record)
        records[sleeve_id] = record

    assigned_sum = sum(Decimal(state["targets"][sid]) for sid in state["assigned"])
    residual = (TOTAL - assigned_sum).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "governing_decisions": GOVERNING_DECISIONS,
        "cohort": [
            {
                "sleeve_id": sleeve_id,
                "record_path": f"{NUMERIC_DIR}/{sleeve_id}.yaml",
                "content_sha256": records[sleeve_id]["content_sha256"],
                "schema_version": SCHEMA_VERSION,
                "governing_decisions": GOVERNING_DECISIONS,
                "numeric_target_status": records[sleeve_id]["numeric_target_status"],
                "drafting_session_or_shard_id": SHARD_ID,
                "sealed_at": sealed_at,
            }
            for sleeve_id in SLEEVE_ORDER
        ],
        "portfolio_reconciliation": {
            "sum_of_assigned_targets_pct": f"{assigned_sum:.2f}",
            "unsized_reserved_capital_pct": f"{residual:.2f}",
            "portfolio_total_pct": "100.00",
            "reconciliation_identity_holds": True,
            "assigned_record_count": len(state["assigned"]),
            "blocked_record_count": len(state["blocked"]),
            "residual_classification": {
                "residual_type": "unsized_unassigned_capital",
                "sleeve_id": None,
                "cash_reserve_equivalence": "prohibited",
                "redistribution_status": "prohibited_without_future_governance",
                "policy_target_status": "not_a_target",
            },
        },
    }
    return records, manifest


def _valid_utc_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _compare_exact(actual: Any, expected: Any, where: str, errors: list[str]) -> None:
    if type(actual) is not type(expected):
        errors.append(f"{where}: type mismatch ({type(actual).__name__} != {type(expected).__name__})")
        return
    if isinstance(expected, dict):
        if list(actual) != list(expected):
            errors.append(f"{where}: key set/order mismatch ({list(actual)!r} != {list(expected)!r})")
        for key in expected.keys() & actual.keys():
            _compare_exact(actual[key], expected[key], f"{where}.{key}", errors)
    elif isinstance(expected, list):
        if len(actual) != len(expected):
            errors.append(f"{where}: list cardinality mismatch ({len(actual)} != {len(expected)})")
        for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
            _compare_exact(actual_item, expected_item, f"{where}[{index}]", errors)
    elif actual != expected:
        errors.append(f"{where}: value mismatch ({actual!r} != {expected!r})")


def validate(repo_root: Path) -> list[str]:
    errors: list[str] = []
    records_dir = repo_root / NUMERIC_DIR
    try:
        files = sorted(path for path in records_dir.glob("*.yaml") if path.name != "COHORT_MANIFEST.yaml")
        file_ids = tuple(path.stem for path in files)
        if set(file_ids) != set(SLEEVE_ORDER) or len(file_ids) != len(SLEEVE_ORDER):
            errors.append(f"numeric_sizing population mismatch: {file_ids!r}")
        actual_records = {path.stem: _load(path) for path in files}
        sealed_values = {
            record.get("sealed_at") for record in actual_records.values() if isinstance(record, dict)
        }
        if len(sealed_values) != 1:
            errors.append("all six records must share exactly one sealed_at value")
            sealed_at = "invalid"
        else:
            sealed_at = next(iter(sealed_values))
        if not _valid_utc_timestamp(sealed_at):
            errors.append(f"sealed_at is not RFC-3339 UTC: {sealed_at!r}")
        expected_records, expected_manifest = build_expected_records(repo_root, sealed_at)
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError, SourceValidationError) as exc:
        return [f"authoritative source/reconstruction failure: {exc}"]

    for sleeve_id in SLEEVE_ORDER:
        actual = actual_records.get(sleeve_id)
        if actual is None:
            continue
        _compare_exact(actual, expected_records[sleeve_id], sleeve_id, errors)
        if not isinstance(actual.get("content_sha256"), str) or not HASH_RE.fullmatch(actual["content_sha256"]):
            errors.append(f"{sleeve_id}.content_sha256: invalid lexical form")
        elif canonical_record_hash(actual) != actual["content_sha256"]:
            errors.append(f"{sleeve_id}.content_sha256: canonical hash mismatch")

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    if not manifest_path.is_file():
        errors.append("manifest missing")
    else:
        try:
            actual_manifest = _load(manifest_path)
            _compare_exact(actual_manifest, expected_manifest, "manifest", errors)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"manifest load failed: {exc}")
    return errors


if __name__ == "__main__":
    repository = Path(__file__).resolve().parent
    validation_errors = validate(repository)
    if validation_errors:
        print("numeric_sizing_validator: FAILED")
        for validation_error in validation_errors:
            print(f"  - {validation_error}")
        raise SystemExit(1)
    print("numeric_sizing_validator: OK (6 schema-2.0 records; live Axis B/C, R2/R3, and reconciliation rederived)")
