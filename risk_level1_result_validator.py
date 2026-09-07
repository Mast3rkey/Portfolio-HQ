"""Fail-closed RISK-0001 trial/result reconciliation validator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import level1_sleeve_robustness_preregistration_validator as authority
import risk_level1_core as core
import risk_level1_runner as runner


def validate_results() -> tuple[str, ...]:
    errors: list[str] = []
    required = (core.FREEZE_PATH, core.ELIGIBILITY_PATH, core.TRIAL_REGISTRY_PATH,
                runner.EXECUTION_RECEIPT, runner.RAW_EVIDENCE_PATH, runner.CELL_RESULTS_PATH,
                runner.DISPOSITION_PATH, runner.DIAGNOSTICS_PATH, runner.RESULTS_REPORT_PATH,
                runner.LIMITATIONS_PATH)
    for path in required:
        if not path.is_file():
            errors.append(f"required result artifact missing: {path.relative_to(core.ROOT)}")
    if errors:
        return tuple(errors)
    freeze = core.load_json(core.FREEZE_PATH)
    registry = core.load_json(core.TRIAL_REGISTRY_PATH)
    eligibility = core.load_json(core.ELIGIBILITY_PATH)
    execution = core.load_json(runner.EXECUTION_RECEIPT)
    raw = core.load_json(runner.RAW_EVIDENCE_PATH)
    cells = core.load_json(runner.CELL_RESULTS_PATH)
    disposition = core.load_json(runner.DISPOSITION_PATH)
    if execution.get("status") != "COMPLETED_RESULTS_OBSERVED_NO_RERUN_PERMITTED" or execution.get("rerun") != "PROHIBITED":
        errors.append("execution receipt does not close the no-rerun boundary")
    if registry.get("registered_cell_count") != 777 or len(registry.get("records", [])) != 777:
        errors.append("trial registry count is not 777")
    if eligibility.get("registered_cell_count") != 777 or len(eligibility.get("records", [])) != 777:
        errors.append("eligibility count is not 777")
    if cells.get("registered_cell_count") != 777 or len(cells.get("records", [])) != 777:
        errors.append("cell result count is not 777")
    registry_ids = [row["cell_id"] for row in registry["records"]]
    result_ids = [row["cell_id"] for row in cells["records"]]
    if registry_ids != result_ids or len(set(result_ids)) != 777:
        errors.append("trial/result identities do not reconcile exactly in canonical order")
    if any("RESERVE" in row["cell_id"] or "CASH" in row["cell_id"] or "debt" in row["cell_id"].lower() for row in registry["records"]):
        errors.append("prohibited reserve/cash/debt trial detected")
    executed = sum(row["execution_state"] == "ELIGIBLE" for row in cells["records"])
    nulls = 777 - executed
    if cells.get("execution_count") != executed or cells.get("ineligible_or_null_count") != nulls:
        errors.append("cell execution/null counts do not reconcile")
    if execution.get("execution_count") != executed or execution.get("ineligible_or_null_count") != nulls:
        errors.append("execution receipt counts do not reconcile")
    if core.sha256_file(runner.RAW_EVIDENCE_PATH) != execution.get("raw_evidence_sha256"):
        errors.append("raw evidence hash mismatch")
    if core.sha256_file(runner.CELL_RESULTS_PATH) != execution.get("cell_results_sha256"):
        errors.append("cell result hash mismatch")
    if core.sha256_file(runner.DISPOSITION_PATH) != execution.get("disposition_sha256"):
        errors.append("disposition hash mismatch")
    expected_family_keys = list(core.FAMILIES)
    if list(raw.get("families", {})) != expected_family_keys or list(disposition.get("families", {})) != expected_family_keys:
        errors.append("family result population/order mismatch")
    for family in core.FAMILIES:
        try:
            recalculated = authority.evaluate_study_evidence(raw["families"][family])
        except Exception as exc:
            errors.append(f"canonical evaluator rejected retained {family} evidence: {exc}")
            continue
        if recalculated != disposition["families"][family]:
            errors.append(f"canonical evaluator result mismatch for {family}")
    allowed_results = {"provisional_scenario_not_rejected", "policy_review_required", "unable_to_determine"}
    if any(row.get("result") not in allowed_results for row in disposition["families"].values()):
        errors.append("unknown result vocabulary")
    boundary_bools = ("no_policy_effect", "automatic_adoption", "replacement_level1_method_created",
                      "level2_membership_or_sizing_created", "whole_portfolio_constructed",
                      "residual_cash_debt_margin_or_leverage_analyzed")
    expected = (True, False, False, False, False, False)
    if tuple(disposition.get(key) for key in boundary_bools) != expected:
        errors.append("result-to-policy boundary fields mismatch")
    if freeze.get("registered_cell_count") != 777 or freeze.get("stage_a", {}).get("status") != "PASS":
        errors.append("data gate freeze did not pass exact registered inventory")
    return tuple(errors)


def main() -> int:
    errors = validate_results()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    cells = core.load_json(runner.CELL_RESULTS_PATH)
    print(f"RISK-0001 results valid: registered=777 executed={cells['execution_count']} null={cells['ineligible_or_null_count']} canonical reductions reconciled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
