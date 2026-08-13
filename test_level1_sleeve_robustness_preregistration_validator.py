"""Adversarial tests for the fail-closed RISK-0001 authority and result mapper."""

from __future__ import annotations

import copy
import hashlib
import inspect
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

import level1_sleeve_robustness_preregistration_validator as v


ROOT = Path(__file__).resolve().parent


def good() -> dict:
    return yaml.safe_load(v.PREREG_PATH.read_text(encoding="utf-8"))


def rejects(data: dict) -> str:
    result = v.validate(data)
    assert not result.ok
    return "\n".join(result.errors)


def test_live_preregistration_and_repository_hash_contract_are_valid():
    assert v.validate_file().ok
    assert v.validate_repository().ok


def test_validator_is_read_only_and_imports_no_production_modules():
    before = v.PREREG_PATH.read_bytes()
    assert v.validate_repository().ok
    assert v.PREREG_PATH.read_bytes() == before
    source = (ROOT / "level1_sleeve_robustness_preregistration_validator.py").read_text()
    assert not any(token in source for token in ("import allocate", "import margin_state", "import alpaca_client", "import levels"))


def test_production_modules_do_not_import_validator():
    needle = "level1_sleeve_robustness_preregistration_validator"
    for name in ("allocate.py", "margin_state.py", "alpaca_client.py", "levels.py"):
        assert needle not in (ROOT / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("mutation", [
    lambda d: d["authority"].__setitem__("optimizer_authority", "PERMITTED"),
    lambda d: d["authority"].pop("question_id"),
    lambda d: d["authority"].__setitem__("policy_adoption", "PERMITTED"),
    lambda d: d["representations"].__setitem__("fifth_family", {}),
    lambda d: d["data_gate"].__setitem__("runtime_override", True),
    lambda d: d["metric_families"]["metrics"][0].__setitem__("extra_vote", True),
    lambda d: d["metric_families"]["metrics"][0].pop("formula"),
    lambda d: d["scenario_windows"]["windows"][0].__setitem__("end", ["2026-07-31"]),
    lambda d: d["fallback_order"].__setitem__("crypto", {"provider": "ALPACA_CRYPTO"}),
])
def test_recursive_schema_closure_rejects_extra_missing_enum_and_type_substitution(mutation):
    data = good()
    mutation(data)
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: next(r for r in d["consequential_parameter_registry"]["parameters"] if r["parameter_id"] == "RELATIVE_PERTURBATION").__setitem__("value", "0.02"),
    lambda d: d["scenario_states"].append("EXTREME"),
    lambda d: d.__setitem__("scenario_states", ["HISTORICAL_REFERENCE", "LOWER", "HIGHER"]),
    lambda d: d["scenario_magnitudes"]["values_pct"]["EQUITY"].__setitem__("LOWER", "14.95"),
    lambda d: d["scenario_provenance"].__setitem__("optimized", True),
])
def test_scenario_authority_and_derived_arithmetic_are_exact(mutation):
    data = good()
    mutation(data)
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: d["fallback_order"]["equities_etfs"].__setitem__(1, "STOOQ"),
    lambda d: d["fallback_order"]["crypto"].__setitem__(1, "KRAKEN"),
    lambda d: d["fallback_order"]["crypto"].append("KRAKEN"),
    lambda d: d["fallback_order"].__setitem__("crypto", list(reversed(d["fallback_order"]["crypto"]))),
    lambda d: d["data_sources"]["equities_etfs"]["primary"].__setitem__("provider", "UNAUTHORIZED"),
])
def test_source_hierarchy_is_exact_and_ordered(mutation):
    data = good()
    mutation(data)
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: d["data_gate"]["integrity_rules"].__setitem__("no_zero_return_standins", False),
    lambda d: d["data_gate"]["integrity_rules"].__setitem__("no_interpolation", False),
    lambda d: d["data_gate"]["integrity_rules"].__setitem__("no_forward_fill_prices", False),
    lambda d: d["data_gate"]["integrity_rules"].__setitem__("no_silent_universe_reduction", False),
    lambda d: d["data_gate"]["CELL_DATA_ELIGIBILITY"]["gates"].remove("REPRESENTATION_WINDOW_QUALITY"),
    lambda d: d["data_gate"]["GLOBAL_STUDY_INTEGRITY"].__setitem__("failure_effect", "CELL_INELIGIBLE"),
    lambda d: d["data_gate"]["CELL_DATA_ELIGIBILITY"].__setitem__("failure_effect", "GLOBAL_HALT"),
])
def test_two_stage_data_gate_is_closed(mutation):
    data = good()
    mutation(data)
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: d["scenario_windows"]["windows"][2].__setitem__("start", "2008-01-01"),
    lambda d: d["scenario_windows"]["windows"].append(copy.deepcopy(d["scenario_windows"]["windows"][-1])),
    lambda d: d["scenario_windows"]["windows"].pop(),
    lambda d: d["scenario_windows"].__setitem__("windows", list(reversed(d["scenario_windows"]["windows"]))),
    lambda d: d["scenario_windows"]["windows"][0].__setitem__("voting_role", "DIAGNOSTIC_ONLY"),
])
def test_window_dates_population_order_and_roles_are_exact(mutation):
    data = good()
    mutation(data)
    rejects(data)


def test_corporate_action_ineligibility_and_no_stitching_are_exact():
    data = good()
    data["corporate_action_rules"]["unresolved_period"] = "ELIGIBLE"
    data["corporate_action_rules"]["synthetic_predecessor_stitching"] = "PERMITTED"
    message = rejects(data)
    assert "unresolved action" in message
    assert "predecessor stitching" in message


@pytest.mark.parametrize("parameter_id,field,value", [
    ("DFF_MISSING_DAYS_ALLOWED", "value", 7),
    ("LOSS_CONTRIBUTION_TOLERANCE_PP", "value", "2.00"),
    ("RECOVERY_BURDEN_TOLERANCE_PPDAYS", "selection_basis", "POST_HOC"),
    ("GOLD_PARITY_CORRELATION_MIN", "binding_scope", "NON_BINDING"),
    ("CRYPTO_MISSING_DAYS_ALLOWED", "reuse_rule", "AUTOMATIC_REUSE"),
    ("MINIMUM_IMPROVEMENT_FAMILIES", "calibrated", True),
])
def test_num_0001_registry_values_and_provenance_are_closed(parameter_id, field, value):
    data = good()
    record = next(r for r in data["consequential_parameter_registry"]["parameters"] if r["parameter_id"] == parameter_id)
    record[field] = value
    rejects(data)


@pytest.mark.parametrize("parameter_id,field,value", [
    ("DFF_AVAILABILITY_LAG_BUSINESS_DAYS", "value", 2),
    ("SCENARIO_DECIMAL_PLACES", "value", 3),
    ("SCENARIO_ROUNDING_MODE", "value", "ROUND_HALF_EVEN"),
    ("FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE", "value", "0.01"),
    ("GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED", "value", 1),
    ("CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED", "value", 1),
    ("RELATIVE_PERTURBATION", "supporting_evidence", ""),
    ("EQUITY_MINIMUM_ELIGIBLE", "duplicate_locations", []),
    ("EQUITY_DIRECTIONAL_BREADTH", "fallback_locations", ["UNDECLARED"]),
    ("GOLD_PARITY_CORRELATION_MIN", "hardcoded_or_config_editable", "RUNTIME_OVERRIDE_ALLOWED"),
    ("GOLD_PARITY_RETURN_MAX_PP", "binding_status", "NON_BINDING"),
    ("GOLD_PARITY_DRAWDOWN_MAX_PP", "lapse_condition", "NEVER"),
    ("CRYPTO_MISSING_DAYS_ALLOWED", "reuse_rule", "AUTOMATIC_REUSE"),
    ("FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE", "calibrated", True),
    ("MINIMUM_IMPROVEMENT_FAMILIES", "evidence_bounded", True),
])
def test_complete_num_0001_metadata_is_fail_closed(parameter_id, field, value):
    data = good()
    record = next(r for r in data["consequential_parameter_registry"]["parameters"] if r["parameter_id"] == parameter_id)
    record[field] = value
    rejects(data)


def test_parameter_record_missing_metadata_and_duplicate_id_reject():
    data = good()
    data["consequential_parameter_registry"]["parameters"][0].pop("supporting_evidence")
    rejects(data)
    data = good()
    data["consequential_parameter_registry"]["parameters"][1]["parameter_id"] = "RELATIVE_PERTURBATION"
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: d["metric_families"]["metrics"].pop(),
    lambda d: d["metric_families"]["metrics"].append(copy.deepcopy(d["metric_families"]["metrics"][-1])),
    lambda d: d["metric_families"]["metrics"][5].__setitem__("family", "CONTRIBUTION"),
    lambda d: d["metric_families"]["metrics"][5].__setitem__("voting_status", "NON_VOTING_DIAGNOSTIC"),
    lambda d: d["metric_families"]["metrics"][5].__setitem__("materiality_parameter_id", "UNDEFINED_TOLERANCE"),
    lambda d: d["metric_families"]["metrics"][5].__setitem__("formula", "UNDEFINED_FORMULA"),
    lambda d: d["metric_families"]["family_order"].__setitem__(1, "PATH_RISK"),
])
def test_metric_population_mapping_voting_and_tolerance_references_are_closed(mutation):
    data = good()
    mutation(data)
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: next(r for r in d["consequential_parameter_registry"]["parameters"] if r["parameter_id"] == "MINIMUM_IMPROVEMENT_FAMILIES").__setitem__("value", 1),
    lambda d: d["result_reduction"]["metric_window_reduction"]["ordered_precedence"].remove("WORSENS"),
    lambda d: d["result_reduction"]["directional_policy_review"].__setitem__("representation_conflict_veto", False),
    lambda d: d["result_reduction"]["total_state_table"][0].__setitem__("review_direction", "lower_exposure"),
    lambda d: d["result_reduction"]["total_state_table"][2].__setitem__("result", "policy_review_required"),
    lambda d: d["result_reduction"]["point_state_table"][10].__setitem__("point_target_assessment", "not_rejected"),
])
def test_dominance_mixed_direction_insufficiency_and_point_mapping_are_closed(mutation):
    data = good()
    mutation(data)
    rejects(data)


@pytest.mark.parametrize("mutation", [
    lambda d: d["trial_inventory"].__setitem__("derived_registered_cell_ceiling", 778),
    lambda d: d["trial_inventory"].__setitem__("reserve_trials", 1),
    lambda d: d["trial_inventory"].__setitem__("metrics_from_same_path_are_new_trials", True),
    lambda d: d["trial_inventory"].__setitem__("failed_discarded_ineligible_attempts_remain_accounted", False),
    lambda d: d["trial_inventory"].__setitem__("cell_identity", "REPRESENTATION_SCENARIO_WINDOW_ONLY"),
])
def test_trial_inventory_has_no_778th_reserve_metric_or_unhashed_cell(mutation):
    data = good()
    mutation(data)
    rejects(data)


def test_rerun_and_policy_expansion_are_rejected():
    data = good()
    data["rerun_rule"]["after_results_observed"] = "PERMITTED"
    rejects(data)
    data = good()
    data["prohibited_scope"].remove("REPLACEMENT_LEVEL1_METHOD_CREATION")
    data["prohibited_scope"].remove("RESIDUAL_REDISTRIBUTION")
    data["prohibited_scope"].remove("DEBT_OR_MARGIN_ANALYSIS")
    rejects(data)


def _copy_authority(tmp_path: Path) -> tuple[Path, Path, Path]:
    protocol = tmp_path / "PROTOCOL_V1.md"
    prereg = tmp_path / "pre_registration.yaml"
    decision = tmp_path / "decision.md"
    protocol.write_bytes(v.PROTOCOL_PATH.read_bytes())
    prereg.write_bytes(v.PREREG_PATH.read_bytes())
    decision.write_bytes(v.DECISION_PATH.read_bytes())
    return prereg, protocol, decision


def test_protocol_byte_tamper_rejects(tmp_path):
    prereg, protocol, decision = _copy_authority(tmp_path)
    protocol.write_bytes(protocol.read_bytes() + b"\nTAMPER\n")
    assert "protocol SHA-256 pin" in "\n".join(v.validate_repository(prereg, protocol, decision).errors)


def test_preregistration_byte_tamper_rejects(tmp_path):
    prereg, protocol, decision = _copy_authority(tmp_path)
    prereg.write_bytes(prereg.read_bytes() + b"\n# byte tamper\n")
    assert "preregistration SHA-256 pin" in "\n".join(v.validate_repository(prereg, protocol, decision).errors)


def test_charter_pin_tamper_and_stale_pin_reject(tmp_path):
    prereg, protocol, decision = _copy_authority(tmp_path)
    text = decision.read_text()
    text = text.replace(v.sha256_file(protocol), "a" * 64, 1)
    decision.write_text(text)
    assert "protocol SHA-256 pin" in "\n".join(v.validate_repository(prereg, protocol, decision).errors)


def test_coordinated_illegal_content_and_rehash_still_rejects(tmp_path):
    prereg, protocol, decision = _copy_authority(tmp_path)
    data = yaml.safe_load(prereg.read_text())
    data["authority"]["optimizer_authority"] = "PERMITTED"
    prereg.write_text(yaml.safe_dump(data, sort_keys=False))
    text = decision.read_text()
    old = v.extract_charter_pins(decision)[0]["preregistration_sha256"]
    text = text.replace(old, hashlib.sha256(prereg.read_bytes()).hexdigest())
    decision.write_text(text)
    message = "\n".join(v.validate_repository(prereg, protocol, decision).errors)
    assert "authority" in message and "exact keys/order" in message


def test_protocol_preregistration_mirror_mismatch_rejects_even_with_rehashed_pin(tmp_path):
    prereg, protocol, decision = _copy_authority(tmp_path)
    protocol.write_text(protocol.read_text().replace("MINIMUM_IMPROVEMENT_FAMILIES: 2", "MINIMUM_IMPROVEMENT_FAMILIES: 1"))
    pins = v.extract_charter_pins(decision)[0]
    decision.write_text(decision.read_text().replace(pins["protocol_sha256"], v.sha256_file(protocol)))
    assert "protocol mirror" in "\n".join(v.validate_repository(prereg, protocol, decision).errors)


def formula_observations(*, corrupt: bool = False) -> list[dict]:
    data = good()
    rows = []
    windows = ("ASSET_AVAILABLE_HISTORY", "Q4_2018", "ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP")
    for metric_id, window_id in zip(data["result_reduction"]["monotonicity"]["designated_metrics"], windows):
        values = dict(data["scenario_magnitudes"]["values_pct"]["EQUITY"])
        rows.append({
            "metric_id": metric_id,
            "family": "EQUITY",
            "representation_id": "AMZN",
            "window_id": window_id,
            "raw_metric_value": "1",
            "scenario_values": values,
        })
    if corrupt:
        rows[0]["scenario_values"]["LOWER"] = "14.940002"
    return rows


def equity_inputs(state: str = "IMPROVES", unavailable: int = 0):
    states = [(ticker, "UNAVAILABLE" if index < unavailable else state) for index, ticker in enumerate(v.EQUITIES)]
    eligible = [(ticker, state) for ticker, observed in states if observed != "UNAVAILABLE"]
    return states, eligible


def passing_gold(peer: str) -> dict:
    return {
        "peer_id": peer,
        "identity_and_inception": "COMPLETE",
        "unresolved_required_session_gaps": 0,
        "dividend_split_action_treatment": "COMPLETE",
        "overlap_total_return_correlation": "0.995",
        "overlap_annualized_return_difference_pp": "0.50",
        "overlap_max_drawdown_difference_pp": "2.00",
    }


@pytest.mark.parametrize("metric_id,candidate,reference,missingness,expected", [
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", Decimal("11.01"), Decimal("10"), "ELIGIBLE", "IMPROVES"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", Decimal("11.00"), Decimal("10"), "ELIGIBLE", "EQUIVALENT"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", Decimal("8.99"), Decimal("10"), "ELIGIBLE", "WORSENS"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", Decimal("8.99"), Decimal("10"), "ELIGIBLE", "IMPROVES"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", Decimal("9.00"), Decimal("10"), "ELIGIBLE", "EQUIVALENT"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", None, Decimal("10"), "MISSING_SOURCE_DATA", "UNAVAILABLE"),
    ("EXPOSURE_SCALED_STRESS_LOSS", None, None, "NOT_APPLICABLE_PRE_INCEPTION", "NOT_APPLICABLE"),
])
def test_observation_threshold_boundaries_use_canonical_metric_authority(metric_id, candidate, reference, missingness, expected):
    assert v.classify_observation(metric_id, candidate, reference, missingness) == expected


def test_metric_and_family_reduction_precedence_and_not_applicable():
    assert v.reduce_states(["EQUIVALENT", "IMPROVES"]) == "IMPROVES"
    assert v.reduce_states(["IMPROVES", "UNAVAILABLE"]) == "UNAVAILABLE"
    assert v.reduce_states(["IMPROVES", "WORSENS"]) == "WORSENS"
    assert v.reduce_states(["NOT_APPLICABLE", "EQUIVALENT"]) == "EQUIVALENT"
    assert v.reduce_states(["NOT_APPLICABLE"]) == "UNAVAILABLE"
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_states(["BOGUS"])


def test_representation_reduction_agreement_whitelist_and_conflict():
    assert v.reduce_representations("FUND_BROAD_MARKET", {x: "IMPROVES" for x in v.BROAD}) == "IMPROVES"
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_representations("FUND_BROAD_MARKET", {"SPY": "IMPROVES", "VEA": "IMPROVES"})
    assert v.reduce_representations("CRYPTO", {"BTC": "IMPROVES", "ETH": "EQUIVALENT", "SOL": "IMPROVES"}) == "CONFLICT"
    assert v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES"}) == "IMPROVES"
    assert v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES"}, [passing_gold("IAU")]) == "IMPROVES"
    assert v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "WORSENS"}, [passing_gold("IAU")]) == "CONFLICT"
    for peer in ("SPY", "BTC", "ARBITRARY"):
        with pytest.raises(v.RuntimeAuthorityError):
            v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES"}, [passing_gold(peer)])
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES"}, [passing_gold("IAU"), passing_gold("IAU")])
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES", "SGOL": "IMPROVES"}, [passing_gold("SGOL"), passing_gold("IAU")])


def test_failed_gold_parity_gate_excludes_peer_but_cannot_admit_state():
    failed = passing_gold("IAU")
    failed["overlap_total_return_correlation"] = "0.994"
    assert v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES"}, [failed]) == "IMPROVES"
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_representations("FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES"}, [failed])


def test_equity_minimum_breadth_median_and_leave_one_out_are_deterministic():
    states, loo = equity_inputs()
    assert v.reduce_equity(states, loo) == "IMPROVES"
    states, loo = equity_inputs(unavailable=7)
    assert v.reduce_equity(states, loo) == "UNAVAILABLE"
    mixed = [(ticker, "IMPROVES" if index < 20 else "EQUIVALENT") for index, ticker in enumerate(v.EQUITIES)]
    assert v.reduce_equity(mixed, [(ticker, "IMPROVES") for ticker in v.EQUITIES]) == "CONFLICT"
    bad_loo = list(loo)
    bad_loo[-1] = (bad_loo[-1][0], "EQUIVALENT")
    assert v.reduce_equity(states, bad_loo) == "UNAVAILABLE"


@pytest.mark.parametrize("mutator", [
    lambda loo: loo.clear(),
    lambda loo: loo.__setitem__(slice(None), loo[:1]),
    lambda loo: loo.__setitem__(1, loo[0]),
    lambda loo: loo.__setitem__(0, ("UNKNOWN", "IMPROVES")),
    lambda loo: loo.pop(),
])
def test_equity_leave_one_out_population_attacks_reject(mutator):
    states, loo = equity_inputs()
    mutator(loo)
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_equity(states, loo)


def test_equity_constituent_population_identity_and_order_are_closed():
    states, loo = equity_inputs()
    states[0] = ("UNKNOWN", "IMPROVES")
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_equity(states, loo)
    states, loo = equity_inputs()
    states.reverse()
    with pytest.raises(v.RuntimeAuthorityError):
        v.reduce_equity(states, loo)


@pytest.mark.parametrize("states,expected", [
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "EQUIVALENT"}, "POLICY_REVIEW_REQUIRED"),
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT"}, "CENTER_NOT_REJECTED"),
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "WORSENS"}, "UNABLE_TO_DETERMINE"),
    ({"PATH_RISK": "WORSENS", "RECOVERY": "WORSENS", "OPPORTUNITY_COST": "EQUIVALENT"}, "CENTER_NOT_REJECTED"),
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "UNAVAILABLE"}, "UNABLE_TO_DETERMINE"),
])
def test_directional_policy_review_matrix(states, expected):
    assert v.directional_disposition(states, formula_observations()) == expected


def test_formula_integrity_is_derived_not_caller_asserted():
    assert v.validate_formula_integrity(formula_observations())
    assert not v.validate_formula_integrity(formula_observations(corrupt=True))
    states = {"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "EQUIVALENT"}
    assert v.directional_disposition(states, formula_observations(corrupt=True)) == "UNABLE_TO_DETERMINE"


@pytest.mark.parametrize("states", [
    {"PATH_RISK": "BOGUS", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT"},
    {"PATH_RISK": "EQUIVALENT", "RECOVERY": "EQUIVALENT"},
    {"PATH_RISK": "EQUIVALENT", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT", "CONTRIBUTION": "IMPROVES"},
])
def test_mandatory_family_population_and_states_fail_closed(states):
    with pytest.raises(v.RuntimeAuthorityError):
        v.directional_disposition(states, formula_observations())


def test_public_mapper_has_no_governance_override_parameters():
    assert tuple(inspect.signature(v.reduce_equity).parameters) == ("constituent_states", "leave_one_out_states")
    assert tuple(inspect.signature(v.directional_disposition).parameters) == ("family_states", "formula_observations")
    assert tuple(inspect.signature(v.point_evidence).parameters) == ("family_states", "formula_observations")
    with pytest.raises(TypeError):
        v.directional_disposition({family: "IMPROVES" for family in v.VOTING_FAMILIES}, formula_observations(), minimum_improvements=1)
    states, loo = equity_inputs()
    with pytest.raises(TypeError):
        v.reduce_equity(states, loo, minimum_eligible=1)
    with pytest.raises(TypeError):
        v.reduce_equity(states, loo, median_state="IMPROVES")
    with pytest.raises(TypeError):
        v.reduce_equity(states, loo, breadth=Decimal("0.01"))
    with pytest.raises(TypeError):
        v.point_evidence({family: "WORSENS" for family in v.VOTING_FAMILIES}, formula_observations(), minimum_worsening=1)
    with pytest.raises(TypeError):
        v.directional_disposition({family: "IMPROVES" for family in v.VOTING_FAMILIES}, formula_observations(), monotonicity_ok=True)
    with pytest.raises(TypeError):
        v.directional_disposition({family: "IMPROVES" for family in v.VOTING_FAMILIES}, formula_observations(), formula_integrity=True)


@pytest.mark.parametrize("lower,higher,lower_point,higher_point,expected", [
    ("POLICY_REVIEW_REQUIRED", "CENTER_NOT_REJECTED", "DISPLACES_REFERENCE", "ADJACENT_MATERIALLY_WORSE", ("policy_review_required", "lower_exposure", "not_supported", "range_or_nonpoint")),
    ("CENTER_NOT_REJECTED", "POLICY_REVIEW_REQUIRED", "ADJACENT_MATERIALLY_WORSE", "DISPLACES_REFERENCE", ("policy_review_required", "higher_exposure", "not_supported", "range_or_nonpoint")),
    ("CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", "ADJACENT_MATERIALLY_WORSE", "NOT_DISTINGUISHED", ("provisional_scenario_not_rejected", None, "not_rejected", None)),
    ("CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", "NOT_DISTINGUISHED", "NOT_DISTINGUISHED", ("provisional_scenario_not_rejected", None, "not_supported", "range_or_nonpoint")),
    ("POLICY_REVIEW_REQUIRED", "POLICY_REVIEW_REQUIRED", "DISPLACES_REFERENCE", "DISPLACES_REFERENCE", ("unable_to_determine", None, "not_supported", "range_or_nonpoint")),
    ("UNABLE_TO_DETERMINE", "CENTER_NOT_REJECTED", "UNAVAILABLE", "ADJACENT_MATERIALLY_WORSE", ("unable_to_determine", None, "unable_to_determine", None)),
])
def test_closed_final_and_point_target_matrix(lower, higher, lower_point, higher_point, expected):
    result = v.final_disposition(lower, higher, lower_point, higher_point)
    assert tuple(result.values()) == expected


def test_all_nine_directional_combinations_have_exactly_one_state_row():
    observed = {(row[0], row[1]) for row in v.TOTAL_STATE_TABLE}
    expected = {(lower, higher) for lower in v.DIRECTIONAL_STATES for higher in v.DIRECTIONAL_STATES}
    assert observed == expected
    assert len(v.TOTAL_STATE_TABLE) == 9


def test_all_sixteen_point_evidence_combinations_have_exactly_one_state_row():
    observed = {(row[0], row[1]) for row in v.POINT_STATE_TABLE}
    expected = {(lower, higher) for lower in v.POINT_EVIDENCE_STATES for higher in v.POINT_EVIDENCE_STATES}
    assert observed == expected
    assert len(v.POINT_STATE_TABLE) == 16


@pytest.mark.parametrize("row", v.TOTAL_STATE_TABLE)
def test_every_canonical_directional_table_row_is_used_by_production_mapper(row):
    result = v.final_disposition(row[0], row[1], "NOT_DISTINGUISHED", "NOT_DISTINGUISHED")
    assert (result["result"], result["review_direction"]) == (row[2], row[3])


@pytest.mark.parametrize("row", v.POINT_STATE_TABLE)
def test_every_canonical_point_table_row_is_used_by_production_mapper(row):
    result = v.final_disposition("CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", row[0], row[1])
    assert (result["point_target_assessment"], result["method_review_direction"]) == (row[2], row[3])


@pytest.mark.parametrize("mutation", [
    lambda rows: rows[0].__setitem__("window_id", "UNKNOWN_WINDOW"),
    lambda rows: rows[0].__setitem__("family", "CASH"),
    lambda rows: rows[0].__setitem__("representation_id", "SPY"),
    lambda rows: rows[0]["scenario_values"].__setitem__("FOURTH_SCENARIO", "1"),
    lambda rows: rows[0].__setitem__("metric_id", "UNKNOWN_METRIC"),
])
def test_formula_evidence_vocabularies_are_closed(mutation):
    rows = formula_observations()
    mutation(rows)
    with pytest.raises(v.RuntimeAuthorityError):
        v.validate_formula_integrity(rows)


def test_point_evidence_reduction_distinguishes_worse_from_indistinguishable():
    worse = {"PATH_RISK": "WORSENS", "RECOVERY": "WORSENS", "OPPORTUNITY_COST": "EQUIVALENT"}
    equivalent = {family: "EQUIVALENT" for family in v.VOTING_FAMILIES}
    improving = {"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "EQUIVALENT"}
    unavailable = {"PATH_RISK": "UNAVAILABLE", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT"}
    assert v.point_evidence(worse, formula_observations()) == "ADJACENT_MATERIALLY_WORSE"
    assert v.point_evidence(equivalent, formula_observations()) == "NOT_DISTINGUISHED"
    assert v.point_evidence(improving, formula_observations()) == "DISPLACES_REFERENCE"
    assert v.point_evidence(unavailable, formula_observations()) == "UNAVAILABLE"


def test_validation_does_not_mutate_input():
    data = good()
    before = copy.deepcopy(data)
    v.validate(data)
    assert data == before
