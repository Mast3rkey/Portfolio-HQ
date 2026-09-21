#!/usr/bin/env python3
"""Check narrow authority/status predicates in the incomplete S3 scope file.

This non-authoritative checklist does not validate narrative facts, evidence
provenance/admissibility, policy correctness, or execution readiness.
"""
from __future__ import annotations

import math
from pathlib import Path
import sys
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "research/margin_target_study/S3_CURRENT_ARCHITECTURE_PREREGISTRATION.yaml"
EXPECTED_ID = "MARGIN-CURRENT-S3-SCOPE-0001"
EXPECTED_STATUS = "SPECIFICATION_INCOMPLETE_NOT_AUTHORIZED_NOT_EXECUTABLE"
EXPECTED_GAPS = {
    "FEASIBLE_COMMON_DATES_AND_PER_ASSET_COVERAGE",
    "CURRENT_FLAT_BASELINE_VERSION_AND_HASHES",
    "FULL_CANDIDATE_DECISION_RULES_INCLUDING_STATE_VARIABLES_LAGS_AND_TARGETS",
    "INITIAL_CAPITAL_CASH_DEBT_AND_NO_BORROWING_CONTROL_SEMANTICS",
    "DEPOSIT_EVENT_ORDER_AND_R1_CASH_FUNDED_VERSUS_TRIM_FUNDED_FORMULAS",
    "RATE_SERIES_SPREAD_FLOOR_AND_POINT_IN_TIME_AVAILABILITY",
    "MAINTENANCE_PROXY_MAPPING_NOT_BROKER_BUFFER_EQUIVALENCE",
    "EXACT_STRESS_TIMING_SEVERITY_AND_COMBINATIONS",
    "TAX_COST_BASIS_TRANSACTION_COST_AND_DIVIDEND_ACCOUNTING",
    "ASSET_ELIGIBILITY_GATED_CASH_AND_NEWER_ASSET_TREATMENT",
    "ENUMERATED_CANDIDATE_X_COST_X_CASHFLOW_X_RATE_X_MAINTENANCE_REGISTRY",
    "TRIAL_BUDGET_DERIVED_FROM_ENUMERATED_REGISTRY",
    "ACCEPTANCE_STATISTICS_UNCERTAINTY_MULTIPLE_TESTING_AND_THRESHOLD_SENSITIVITY",
    "HOLDOUT_STATUS_AND_ANY_LAWFUL_FUTURE_EVALUATION_SCOPE",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _finite(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, int):
        return value.bit_length() <= 1024
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(_finite(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and _finite(item) for key, item in value.items())
    return False


def validate(path: Path = REGISTER) -> list[str]:
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception as exc:
        return [f"cannot load unique-key YAML: {exc}"]
    if not isinstance(data, dict) or not _finite(data):
        return ["register must be a finite mapping with string keys"]
    errors: list[str] = []
    if data.get("study_id") != EXPECTED_ID:
        errors.append("wrong scoping identity")
    if data.get("status") != EXPECTED_STATUS:
        errors.append("register must remain specification-incomplete and unauthorized")
    if data.get("artifact_role") != "RESULT_BLIND_SCOPING_REGISTER_NOT_A_FROZEN_PREREGISTRATION":
        errors.append("artifact role overstates scoping authority")
    gaps = data.get("required_unresolved_decisions")
    if (not isinstance(gaps, list)
            or not all(isinstance(gap, str) for gap in gaps)
            or len(gaps) != len(set(gaps))
            or set(gaps) != EXPECTED_GAPS):
        errors.append("missing, duplicate, or changed unresolved-decision register")
    exposure = data.get("exposure_and_coverage_ledger")
    if not isinstance(exposure, dict):
        errors.append("exposure ledger must be a mapping")
    else:
        track_2 = exposure.get("original_margin_track_2")
        fresh = exposure.get("successor_fresh_period")
        if not isinstance(track_2, dict):
            errors.append("original Track 2 exposure record must be a mapping")
        elif track_2.get("original_untouched_start") != "2025-07-01":
            errors.append("original Track 2 seal changed")
        if not isinstance(fresh, dict):
            errors.append("successor fresh-period record must be a mapping")
        elif fresh.get("status") != "NONE_ESTABLISHED":
            errors.append("successor fresh-period claim is prohibited")
    execution = data.get("execution")
    if not isinstance(execution, dict) or any(execution.get(key) is not False for key in (
        "implementation_authorized", "historical_execution_authorized", "sealed_access_authorized"
    )) or execution.get("runner_command") != "NONE":
        errors.append("implementation/execution/sealed access must remain prohibited with no runner")
    candidate_registry = data.get("candidate_registry")
    if not isinstance(candidate_registry, dict) or candidate_registry.get("status") != "NOT_DEFINED":
        errors.append("candidate registry must remain undefined")
    trial_budget = data.get("trial_budget")
    if not isinstance(trial_budget, dict) or trial_budget.get("status") != "NOT_DEFINED":
        errors.append("trial budget must remain undefined")
    return errors


def main() -> int:
    errors = validate()
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("PASS: scoping authority/status checklist predicates hold; narrative facts are unchecked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
