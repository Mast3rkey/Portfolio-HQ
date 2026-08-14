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


def raw_study_evidence(
    research_family: str = "FUND_BROAD_MARKET",
    *,
    overrides: dict[tuple[str, str], str] | None = None,
    gold_peer_evidence: list[dict] | None = None,
) -> dict:
    data = good()
    peers = copy.deepcopy(gold_peer_evidence or [])
    admitted = v._admitted_gold_peers(data, peers)
    if research_family == "FUND_GLD_DEFENSIVE":
        representations = ("GLD",) + admitted
    else:
        representations = v._registered_representations(data, research_family)
    metric_lookup = {metric["metric_id"]: metric for metric in data["metric_families"]["metrics"]}
    overrides = overrides or {}

    def operands_for(metric_id: str, profile: str):
        if profile == "UNAVAILABLE":
            return None, "MISSING_SOURCE_DATA"
        if profile == "PRE_INCEPTION":
            return None, "NOT_APPLICABLE_PRE_INCEPTION"
        if metric_id == "EXPOSURE_SCALED_DRAWDOWN_LOSS":
            return {"drawdown": "-0.10" if profile == "EQUIVALENT" else "-0.50"}, "ELIGIBLE"
        if metric_id == "EXPOSURE_SCALED_STRESS_LOSS":
            return {"stress_return": "-0.10" if profile == "EQUIVALENT" else "-0.50"}, "ELIGIBLE"
        if metric_id == "EXPOSURE_SCALED_UNDERWATER_BURDEN":
            return {"underwater_area_days": "1" if profile == "EQUIVALENT" else "20"}, "ELIGIBLE"
        if metric_id == "EXPOSURE_SCALED_EXCESS_CONTRIBUTION":
            if profile == "OPPORTUNITY_POSITIVE":
                return {"asset_total_return": "1", "comparator_total_return": "0"}, "ELIGIBLE"
            if profile == "OPPORTUNITY_NEGATIVE":
                return {"asset_total_return": "-1", "comparator_total_return": "0"}, "ELIGIBLE"
            return {"asset_total_return": "0", "comparator_total_return": "0"}, "ELIGIBLE"
        raise AssertionError(metric_id)

    def reported_values(scenario: str, metric_id: str, operands: dict | None, missingness: str):
        if missingness != "ELIGIBLE":
            return None, None
        if metric_id == "EXPOSURE_SCALED_DRAWDOWN_LOSS":
            raw_value = abs(Decimal(operands["drawdown"]))
        elif metric_id == "EXPOSURE_SCALED_STRESS_LOSS":
            raw_value = max(Decimal("0"), -Decimal(operands["stress_return"]))
        elif metric_id == "EXPOSURE_SCALED_UNDERWATER_BURDEN":
            raw_value = Decimal(operands["underwater_area_days"])
        else:
            raw_value = Decimal(operands["asset_total_return"]) - Decimal(operands["comparator_total_return"])
        exposures = data["scenario_magnitudes"]["values_pct"][research_family]
        return str(Decimal(exposures[scenario]) * raw_value), str(Decimal(exposures["HISTORICAL_REFERENCE"]) * raw_value)

    directions = {}
    for scenario in ("LOWER", "HIGHER"):
        observations = []
        state_for: dict[tuple[str, str], str] = {}
        for representation in representations:
            for metric_id, window_id in v._observation_plan(data):
                voting_family = metric_lookup[metric_id]["family"]
                default_profile = "EQUIVALENT" if voting_family == "OPPORTUNITY_COST" else "MATERIAL"
                profile = overrides.get((representation, voting_family), default_profile)
                state_for[(representation, voting_family)] = profile
                operands, missingness = operands_for(metric_id, profile)
                candidate, reference = reported_values(scenario, metric_id, operands, missingness)
                observations.append({
                    "scenario_id": scenario,
                    "research_family": research_family,
                    "representation_id": representation,
                    "metric_id": metric_id,
                    "window_id": window_id,
                    "raw_operands": operands,
                    "reported_candidate": candidate,
                    "reported_reference": reference,
                    "missingness_state": missingness,
                })
        loo = []
        if research_family == "EQUITY":
            for voting_family in v.VOTING_FAMILIES:
                metric_id, window_id = v._mandatory_metric_for_family(data, voting_family)
                for ticker in representations:
                    profile = state_for[(ticker, voting_family)]
                    if profile == "UNAVAILABLE":
                        continue
                    operands, missingness = operands_for(metric_id, profile)
                    candidate, reference = reported_values(scenario, metric_id, operands, missingness)
                    loo.append({
                        "scenario_id": scenario,
                        "research_family": research_family,
                        "omitted_id": ticker,
                        "metric_id": metric_id,
                        "window_id": window_id,
                        "raw_operands": operands,
                        "reported_candidate": candidate,
                        "reported_reference": reference,
                        "missingness_state": missingness,
                    })
        directions[scenario] = {
            "observations": observations,
            "equity_leave_one_out": loo,
        }
    return {
        "study_id": "RISK-0001",
        "research_family": research_family,
        "gold_peer_evidence": peers,
        "directions": directions,
    }


def observation(evidence: dict, scenario: str, representation: str, metric: str, window: str) -> dict:
    return next(
        row for row in evidence["directions"][scenario]["observations"]
        if row["representation_id"] == representation
        and row["metric_id"] == metric
        and row["window_id"] == window
    )


@pytest.mark.parametrize("evidence,expected", [
    (raw_study_evidence(), ("policy_review_required", "lower_exposure")),
    (raw_study_evidence(overrides={(rep, family): "EQUIVALENT" for rep in v.BROAD for family in v.VOTING_FAMILIES}), ("provisional_scenario_not_rejected", None)),
    (raw_study_evidence(overrides={(rep, "OPPORTUNITY_COST"): "OPPORTUNITY_POSITIVE" for rep in v.BROAD}), ("unable_to_determine", None)),
    (raw_study_evidence(overrides={(rep, "OPPORTUNITY_COST"): "OPPORTUNITY_NEGATIVE" for rep in v.BROAD}), ("policy_review_required", "lower_exposure")),
])
def test_authoritative_raw_evidence_directional_outcomes(evidence, expected):
    result = v.evaluate_study_evidence(evidence)
    assert (result["result"], result["review_direction"]) == expected


def test_authoritative_raw_evidence_representation_unavailable_and_worsening_vetoes():
    conflict = raw_study_evidence(overrides={("VEA", "PATH_RISK"): "EQUIVALENT"})
    unavailable = raw_study_evidence(overrides={(rep, "OPPORTUNITY_COST"): "UNAVAILABLE" for rep in v.BROAD})
    mixed = raw_study_evidence(overrides={(rep, "OPPORTUNITY_COST"): "OPPORTUNITY_POSITIVE" for rep in v.BROAD})
    for evidence in (conflict, unavailable, mixed):
        result = v.evaluate_study_evidence(evidence)
        assert result["directional_states"]["LOWER"] == "UNABLE_TO_DETERMINE"
        assert result["point_states"]["LOWER"] == "UNAVAILABLE"
        assert result["result"] == "unable_to_determine"


def test_authoritative_raw_evidence_equity_count_and_breadth_controls():
    unavailable = {(ticker, family): "UNAVAILABLE" for ticker in v.EQUITIES[:7] for family in v.VOTING_FAMILIES}
    insufficient = raw_study_evidence("EQUITY", overrides=unavailable)
    breadth = {(ticker, "PATH_RISK"): "EQUIVALENT" for ticker in v.EQUITIES[-7:]}
    breadth_conflict = raw_study_evidence("EQUITY", overrides=breadth)
    for evidence in (insufficient, breadth_conflict):
        result = v.evaluate_study_evidence(evidence)
        assert result["directional_states"]["LOWER"] == "UNABLE_TO_DETERMINE"


def test_authoritative_raw_evidence_gld_admission_and_peer_veto():
    admitted = [passing_gold("IAU")]
    veto = raw_study_evidence(
        "FUND_GLD_DEFENSIVE",
        gold_peer_evidence=admitted,
        overrides={("IAU", "PATH_RISK"): "EQUIVALENT"},
    )
    assert v.evaluate_study_evidence(veto)["result"] == "unable_to_determine"
    failed = passing_gold("IAU")
    failed["overlap_total_return_correlation"] = "0.994"
    excluded = raw_study_evidence("FUND_GLD_DEFENSIVE", gold_peer_evidence=[failed])
    assert v.evaluate_study_evidence(excluded)["review_direction"] == "lower_exposure"


def test_authoritative_raw_evidence_crypto_representation_conflict():
    evidence = raw_study_evidence("CRYPTO", overrides={("SOL", "PATH_RISK"): "EQUIVALENT"})
    assert v.evaluate_study_evidence(evidence)["result"] == "unable_to_determine"


def test_authoritative_raw_evidence_formula_reconciliation_and_cross_direction_consistency():
    evidence = raw_study_evidence()
    evidence["directions"]["LOWER"]["observations"][0]["reported_candidate"] = "999"
    with pytest.raises(v.RuntimeAuthorityError, match="does not reconcile"):
        v.evaluate_study_evidence(evidence)

    evidence = raw_study_evidence()
    evidence["directions"]["HIGHER"]["observations"][0]["raw_operands"]["drawdown"] = "-0.25"
    higher = evidence["directions"]["HIGHER"]["observations"][0]
    higher["reported_candidate"] = "4.4000"
    higher["reported_reference"] = "3.6675"
    with pytest.raises(v.RuntimeAuthorityError, match="same canonical primitive path"):
        v.evaluate_study_evidence(evidence)


def test_reviewer_contradictory_observation_and_formula_chain_rejects():
    evidence = raw_study_evidence()
    row = observation(
        evidence, "LOWER", "SPY", "EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY"
    )
    row["reported_candidate"] = "0"
    row["reported_reference"] = "100"
    with pytest.raises(v.RuntimeAuthorityError, match="does not reconcile"):
        v.evaluate_study_evidence(evidence)

    detached = raw_study_evidence()
    detached["directions"]["LOWER"]["formula_observations"] = [{"raw_metric_value": "1"}]
    with pytest.raises(v.RuntimeAuthorityError, match="exact keys/order"):
        v.evaluate_study_evidence(detached)


@pytest.mark.parametrize("factor", [Decimal("2"), Decimal("0.5")])
def test_changed_formula_operands_cannot_leave_reporting_chain_fixed(factor):
    evidence = raw_study_evidence()
    row = observation(
        evidence, "LOWER", "SPY", "EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY"
    )
    row["raw_operands"]["drawdown"] = str(Decimal(row["raw_operands"]["drawdown"]) * factor)
    with pytest.raises(v.RuntimeAuthorityError, match="does not reconcile"):
        v.evaluate_study_evidence(evidence)


def test_canonical_formula_operands_not_reporting_fields_drive_the_final_result():
    material = v.evaluate_study_evidence(raw_study_evidence())
    small_path = raw_study_evidence(
        overrides={(representation, "PATH_RISK"): "EQUIVALENT" for representation in v.BROAD}
    )
    equivalent = v.evaluate_study_evidence(small_path)
    assert material["result"] == "policy_review_required"
    assert equivalent["result"] == "provisional_scenario_not_rejected"


@pytest.mark.parametrize("metric,window,bad_operands", [
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY", {"stress_return": "-0.50"}),
    ("EXPOSURE_SCALED_STRESS_LOSS", "Q4_2018", {"drawdown": "-0.50"}),
    ("EXPOSURE_SCALED_UNDERWATER_BURDEN", "ASSET_AVAILABLE_HISTORY", {"underwater_area_days": "20", "extra": "0"}),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", "ASSET_AVAILABLE_HISTORY", {"asset_total_return": "0"}),
])
def test_each_formula_metric_has_one_exact_primitive_operand_contract(metric, window, bad_operands):
    evidence = raw_study_evidence()
    row = observation(evidence, "LOWER", "SPY", metric, window)
    row["raw_operands"] = bad_operands
    with pytest.raises(v.RuntimeAuthorityError, match="exact keys/order"):
        v.evaluate_study_evidence(evidence)


@pytest.mark.parametrize("metric,window", [
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY"),
    ("EXPOSURE_SCALED_STRESS_LOSS", "Q4_2018"),
    ("EXPOSURE_SCALED_UNDERWATER_BURDEN", "ASSET_AVAILABLE_HISTORY"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", "ASSET_AVAILABLE_HISTORY"),
])
def test_each_formula_metric_reporting_value_is_reconciled_before_classification(metric, window):
    evidence = raw_study_evidence()
    row = observation(evidence, "LOWER", "SPY", metric, window)
    row["reported_candidate"] = str(Decimal(row["reported_candidate"]) + Decimal("0.01"))
    with pytest.raises(v.RuntimeAuthorityError, match="does not reconcile"):
        v.evaluate_study_evidence(evidence)


@pytest.mark.parametrize("family,peers,scenario,representation,metric,window,location", [
    ("FUND_BROAD_MARKET", None, "LOWER", "VEA", "EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY", "observations"),
    ("FUND_BROAD_MARKET", None, "HIGHER", "VWO", "EXPOSURE_SCALED_STRESS_LOSS", "Q4_2018", "observations"),
    ("CRYPTO", None, "LOWER", "ETH", "EXPOSURE_SCALED_UNDERWATER_BURDEN", "ASSET_AVAILABLE_HISTORY", "observations"),
    ("CRYPTO", None, "HIGHER", "SOL", "EXPOSURE_SCALED_EXCESS_CONTRIBUTION", "FAMILY_COMMON_OVERLAP", "observations"),
    ("FUND_GLD_DEFENSIVE", [passing_gold("IAU")], "LOWER", "IAU", "EXPOSURE_SCALED_DRAWDOWN_LOSS", "FAMILY_COMMON_OVERLAP", "observations"),
    ("EQUITY", None, "HIGHER", "AMZN", "EXPOSURE_SCALED_UNDERWATER_BURDEN", "ASSET_AVAILABLE_HISTORY", "observations"),
    ("EQUITY", None, "LOWER", "AMZN", "EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY", "equity_leave_one_out"),
])
def test_formula_operand_coverage_is_required_for_every_registered_identity(
    family, peers, scenario, representation, metric, window, location
):
    evidence = raw_study_evidence(family, gold_peer_evidence=peers)
    if location == "observations":
        row = observation(evidence, scenario, representation, metric, window)
    else:
        row = next(
            item for item in evidence["directions"][scenario][location]
            if item["omitted_id"] == representation and item["metric_id"] == metric and item["window_id"] == window
        )
    row.pop("raw_operands")
    with pytest.raises(v.RuntimeAuthorityError, match="exact keys/order"):
        v.evaluate_study_evidence(evidence)


def test_historical_reference_and_direction_formula_coverage_cannot_be_omitted_or_added():
    evidence = raw_study_evidence()
    row = evidence["directions"]["LOWER"]["observations"][0]
    row.pop("reported_reference")
    with pytest.raises(v.RuntimeAuthorityError, match="exact keys/order"):
        v.evaluate_study_evidence(evidence)

    evidence = raw_study_evidence()
    evidence["directions"].pop("HIGHER")
    with pytest.raises(v.RuntimeAuthorityError, match="exact keys/order"):
        v.evaluate_study_evidence(evidence)

    evidence = raw_study_evidence()
    evidence["directions"]["HISTORICAL_REFERENCE"] = copy.deepcopy(evidence["directions"]["LOWER"])
    with pytest.raises(v.RuntimeAuthorityError, match="exact keys/order"):
        v.evaluate_study_evidence(evidence)


@pytest.mark.parametrize("attack", [
    "wrong_broad_representation",
    "wrong_crypto_representation",
    "wrong_scenario",
    "wrong_window",
    "wrong_metric",
    "duplicate_record",
    "extra_unreferenced_record",
])
def test_formula_identity_population_attacks_reject_through_public_evaluator(attack):
    family = "CRYPTO" if attack == "wrong_crypto_representation" else "FUND_BROAD_MARKET"
    evidence = raw_study_evidence(family)
    rows = evidence["directions"]["LOWER"]["observations"]
    row = rows[0]
    if attack == "wrong_broad_representation":
        row["representation_id"] = "VEA"
    elif attack == "wrong_crypto_representation":
        row["representation_id"] = "ETH"
    elif attack == "wrong_scenario":
        row["scenario_id"] = "HIGHER"
    elif attack == "wrong_window":
        row["window_id"] = "Q4_2018"
    elif attack == "wrong_metric":
        row["metric_id"] = "EXPOSURE_SCALED_UNDERWATER_BURDEN"
        row["raw_operands"] = {"underwater_area_days": "20"}
    elif attack == "duplicate_record":
        rows.insert(1, copy.deepcopy(row))
    else:
        extra = copy.deepcopy(row)
        extra["window_id"] = "COVID_2020"
        rows.append(extra)
    with pytest.raises(v.RuntimeAuthorityError):
        v.evaluate_study_evidence(evidence)


@pytest.mark.parametrize("missingness", [
    "NOT_APPLICABLE_PRE_INCEPTION",
    "MISSING_SOURCE_DATA",
    "QUALITY_GATE_FAILED",
    "CORPORATE_ACTION_UNRESOLVED",
])
def test_formula_operands_are_absent_only_for_canonical_ineligible_observations(missingness):
    evidence = raw_study_evidence()
    for scenario in ("LOWER", "HIGHER"):
        row = observation(evidence, scenario, "SPY", "EXPOSURE_SCALED_STRESS_LOSS", "GFC_2008")
        row["raw_operands"] = None
        row["reported_candidate"] = None
        row["reported_reference"] = None
        row["missingness_state"] = missingness
    result = v.evaluate_study_evidence(evidence)
    assert result["result"] in ("policy_review_required", "unable_to_determine")


def test_ineligible_formula_observation_rejects_retained_operands_or_values():
    evidence = raw_study_evidence()
    for scenario in ("LOWER", "HIGHER"):
        row = observation(evidence, scenario, "SPY", "EXPOSURE_SCALED_STRESS_LOSS", "GFC_2008")
        row["missingness_state"] = "MISSING_SOURCE_DATA"
        row["reported_candidate"] = None
        row["reported_reference"] = None
    with pytest.raises(v.RuntimeAuthorityError, match="requires null operands"):
        v.evaluate_study_evidence(evidence)


def test_authoritative_evaluator_does_not_accept_derived_state_authority():
    evidence = raw_study_evidence()
    baseline = v.evaluate_study_evidence(evidence)
    assert baseline["point_target_assessment"] == "not_supported"
    for key, value in (
        ("directional_states", {"LOWER": "CENTER_NOT_REJECTED", "HIGHER": "CENTER_NOT_REJECTED"}),
        ("point_states", {"LOWER": "ADJACENT_MATERIALLY_WORSE", "HIGHER": "ADJACENT_MATERIALLY_WORSE"}),
        ("final_disposition", "not_rejected"),
        ("median", "IMPROVES"),
        ("breadth", "1.00"),
        ("monotonicity_ok", True),
        ("formula_integrity_ok", True),
    ):
        attacked = copy.deepcopy(evidence)
        attacked[key] = value
        with pytest.raises(v.RuntimeAuthorityError):
            v.evaluate_study_evidence(attacked)

    for direction_key, value in (
        ("directional_state", "CENTER_NOT_REJECTED"),
        ("point_state", "ADJACENT_MATERIALLY_WORSE"),
        ("median", "IMPROVES"),
        ("breadth", "1.00"),
        ("monotonicity_ok", True),
        ("formula_integrity_ok", True),
    ):
        attacked = copy.deepcopy(evidence)
        attacked["directions"]["LOWER"][direction_key] = value
        with pytest.raises(v.RuntimeAuthorityError):
            v.evaluate_study_evidence(attacked)


def test_authoritative_evaluator_has_no_parameter_override_surface():
    evidence = raw_study_evidence()
    for override in (
        "minimum_improvement_families",
        "minimum_equity_eligible",
        "equity_breadth",
        "gold_parity_threshold",
        "formula_integrity_tolerance",
        "point_worsening_threshold",
    ):
        with pytest.raises(TypeError):
            v.evaluate_study_evidence(evidence, **{override: 0})


@pytest.mark.parametrize("field,value,missingness", [
    ("metric_id", "UNKNOWN_METRIC", "MISSING_SOURCE_DATA"),
    ("representation_id", "UNKNOWN_REPRESENTATION", "MISSING_SOURCE_DATA"),
    ("window_id", "UNKNOWN_WINDOW", "NOT_APPLICABLE_PRE_INCEPTION"),
    ("scenario_id", "UNKNOWN_SCENARIO", "MISSING_SOURCE_DATA"),
])
def test_authoritative_identity_validation_precedes_missingness(field, value, missingness):
    evidence = raw_study_evidence()
    record = evidence["directions"]["LOWER"]["observations"][0]
    record[field] = value
    record["raw_operands"] = None
    record["reported_candidate"] = None
    record["reported_reference"] = None
    record["missingness_state"] = missingness
    with pytest.raises(v.RuntimeAuthorityError):
        v.evaluate_study_evidence(evidence)


def test_authoritative_unknown_failed_gold_peer_rejects_before_gate_exclusion():
    peer = passing_gold("SPY")
    peer["identity_and_inception"] = "INCOMPLETE"
    evidence = raw_study_evidence("FUND_GLD_DEFENSIVE")
    evidence["gold_peer_evidence"] = [peer]
    with pytest.raises(v.RuntimeAuthorityError):
        v.evaluate_study_evidence(evidence)


def test_authoritative_excluded_canonical_gold_peer_observation_rejects_cleanly():
    failed = passing_gold("IAU")
    failed["identity_and_inception"] = "INCOMPLETE"
    evidence = raw_study_evidence("FUND_GLD_DEFENSIVE", gold_peer_evidence=[failed])
    injected = copy.deepcopy(evidence["directions"]["LOWER"]["observations"][0])
    injected["representation_id"] = "IAU"
    evidence["directions"]["LOWER"]["observations"].insert(0, injected)
    with pytest.raises(v.RuntimeAuthorityError, match="inactive representation"):
        v.evaluate_study_evidence(evidence)


def test_authoritative_gold_peer_admission_cannot_be_asserted_by_caller():
    evidence = raw_study_evidence("FUND_GLD_DEFENSIVE")
    peer = passing_gold("IAU")
    peer["peer_admitted"] = True
    evidence["gold_peer_evidence"] = [peer]
    with pytest.raises(v.RuntimeAuthorityError):
        v.evaluate_study_evidence(evidence)


@pytest.mark.parametrize("metric_id,candidate,reference,missingness,expected", [
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", Decimal("11.01"), Decimal("10"), "ELIGIBLE", "IMPROVES"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", Decimal("11.00"), Decimal("10"), "ELIGIBLE", "EQUIVALENT"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", Decimal("8.99"), Decimal("10"), "ELIGIBLE", "WORSENS"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", Decimal("8.99"), Decimal("10"), "ELIGIBLE", "IMPROVES"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", Decimal("9.00"), Decimal("10"), "ELIGIBLE", "EQUIVALENT"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", None, None, "MISSING_SOURCE_DATA", "UNAVAILABLE"),
    ("EXPOSURE_SCALED_STRESS_LOSS", None, None, "NOT_APPLICABLE_PRE_INCEPTION", "NOT_APPLICABLE"),
])
def test_observation_threshold_boundaries_use_canonical_metric_authority(metric_id, candidate, reference, missingness, expected):
    window = "Q4_2018" if metric_id == "EXPOSURE_SCALED_STRESS_LOSS" else "ASSET_AVAILABLE_HISTORY"
    assert v._classify_observation(
        good(), "EQUITY", "AMZN", "LOWER", metric_id, window,
        candidate, reference, missingness,
    ) == expected


def test_metric_and_family_reduction_precedence_and_not_applicable():
    assert v._reduce_states(["EQUIVALENT", "IMPROVES"]) == "IMPROVES"
    assert v._reduce_states(["IMPROVES", "UNAVAILABLE"]) == "UNAVAILABLE"
    assert v._reduce_states(["IMPROVES", "WORSENS"]) == "WORSENS"
    assert v._reduce_states(["NOT_APPLICABLE", "EQUIVALENT"]) == "EQUIVALENT"
    assert v._reduce_states(["NOT_APPLICABLE"]) == "UNAVAILABLE"
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_states(["BOGUS"])


def test_representation_reduction_agreement_whitelist_and_conflict():
    data = good()
    assert v._reduce_representations(data, "FUND_BROAD_MARKET", {x: "IMPROVES" for x in v.BROAD}) == "IMPROVES"
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_representations(data, "FUND_BROAD_MARKET", {"SPY": "IMPROVES", "VEA": "IMPROVES"})
    assert v._reduce_representations(data, "CRYPTO", {"BTC": "IMPROVES", "ETH": "EQUIVALENT", "SOL": "IMPROVES"}) == "CONFLICT"
    assert v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES"}) == "IMPROVES"
    assert v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES"}, [passing_gold("IAU")]) == "IMPROVES"
    assert v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "WORSENS"}, [passing_gold("IAU")]) == "CONFLICT"
    for peer in ("SPY", "BTC", "ARBITRARY"):
        with pytest.raises(v.RuntimeAuthorityError):
            v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES"}, [passing_gold(peer)])
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES"}, [passing_gold("IAU"), passing_gold("IAU")])
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES", "SGOL": "IMPROVES"}, [passing_gold("SGOL"), passing_gold("IAU")])


def test_failed_gold_parity_gate_excludes_peer_but_cannot_admit_state():
    data = good()
    failed = passing_gold("IAU")
    failed["overlap_total_return_correlation"] = "0.994"
    assert v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES"}, [failed]) == "IMPROVES"
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_representations(data, "FUND_GLD_DEFENSIVE", {"GLD": "IMPROVES", "IAU": "IMPROVES"}, [failed])


def test_equity_minimum_breadth_median_and_leave_one_out_are_deterministic():
    data = good()
    states, loo = equity_inputs()
    assert v._reduce_equity(data, states, loo) == "IMPROVES"
    states, loo = equity_inputs(unavailable=7)
    assert v._reduce_equity(data, states, loo) == "UNAVAILABLE"
    mixed = [(ticker, "IMPROVES" if index < 20 else "EQUIVALENT") for index, ticker in enumerate(v.EQUITIES)]
    assert v._reduce_equity(data, mixed, [(ticker, "IMPROVES") for ticker in v.EQUITIES]) == "CONFLICT"
    bad_loo = list(loo)
    bad_loo[-1] = (bad_loo[-1][0], "EQUIVALENT")
    assert v._reduce_equity(data, states, bad_loo) == "UNAVAILABLE"


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
        v._reduce_equity(good(), states, loo)


def test_equity_constituent_population_identity_and_order_are_closed():
    states, loo = equity_inputs()
    states[0] = ("UNKNOWN", "IMPROVES")
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_equity(good(), states, loo)
    states, loo = equity_inputs()
    states.reverse()
    with pytest.raises(v.RuntimeAuthorityError):
        v._reduce_equity(good(), states, loo)


@pytest.mark.parametrize("states,expected", [
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "EQUIVALENT"}, "POLICY_REVIEW_REQUIRED"),
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT"}, "CENTER_NOT_REJECTED"),
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "WORSENS"}, "UNABLE_TO_DETERMINE"),
    ({"PATH_RISK": "WORSENS", "RECOVERY": "WORSENS", "OPPORTUNITY_COST": "EQUIVALENT"}, "CENTER_NOT_REJECTED"),
    ({"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "UNAVAILABLE"}, "UNABLE_TO_DETERMINE"),
])
def test_directional_policy_review_matrix(states, expected):
    assert v._directional_disposition(good(), states) == expected


@pytest.mark.parametrize("offset,accepts", [
    (Decimal("0"), True),
    (Decimal("0.000001"), True),
    (Decimal("0.0000011"), False),
])
def test_formula_reporting_tolerance_boundary_is_canonical(offset, accepts):
    evidence = raw_study_evidence()
    record = evidence["directions"]["LOWER"]["observations"][0]
    record["reported_candidate"] = str(Decimal(record["reported_candidate"]) + offset)
    if accepts:
        assert v.evaluate_study_evidence(evidence)["review_direction"] == "lower_exposure"
    else:
        with pytest.raises(v.RuntimeAuthorityError, match="does not reconcile"):
            v.evaluate_study_evidence(evidence)


@pytest.mark.parametrize("states", [
    {"PATH_RISK": "BOGUS", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT"},
    {"PATH_RISK": "EQUIVALENT", "RECOVERY": "EQUIVALENT"},
    {"PATH_RISK": "EQUIVALENT", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT", "CONTRIBUTION": "IMPROVES"},
])
def test_mandatory_family_population_and_states_fail_closed(states):
    with pytest.raises(v.RuntimeAuthorityError):
        v._directional_disposition(good(), states)


def test_public_mapper_has_no_governance_override_parameters():
    assert tuple(inspect.signature(v.evaluate_study_evidence).parameters) == ("raw_evidence",)
    for removed in (
        "classify_observation", "reduce_states", "reduce_representations", "reduce_equity",
        "validate_formula_integrity", "directional_disposition", "point_evidence", "final_disposition",
    ):
        assert not hasattr(v, removed)
    with pytest.raises(TypeError):
        v.evaluate_study_evidence({}, minimum_improvements=1)


@pytest.mark.parametrize("lower,higher,lower_point,higher_point,expected", [
    ("POLICY_REVIEW_REQUIRED", "CENTER_NOT_REJECTED", "DISPLACES_REFERENCE", "ADJACENT_MATERIALLY_WORSE", ("policy_review_required", "lower_exposure", "not_supported", "range_or_nonpoint")),
    ("CENTER_NOT_REJECTED", "POLICY_REVIEW_REQUIRED", "ADJACENT_MATERIALLY_WORSE", "DISPLACES_REFERENCE", ("policy_review_required", "higher_exposure", "not_supported", "range_or_nonpoint")),
    ("CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", "ADJACENT_MATERIALLY_WORSE", "NOT_DISTINGUISHED", ("provisional_scenario_not_rejected", None, "not_rejected", None)),
    ("CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", "NOT_DISTINGUISHED", "NOT_DISTINGUISHED", ("provisional_scenario_not_rejected", None, "not_supported", "range_or_nonpoint")),
    ("POLICY_REVIEW_REQUIRED", "POLICY_REVIEW_REQUIRED", "DISPLACES_REFERENCE", "DISPLACES_REFERENCE", ("unable_to_determine", None, "not_supported", "range_or_nonpoint")),
    ("UNABLE_TO_DETERMINE", "CENTER_NOT_REJECTED", "UNAVAILABLE", "ADJACENT_MATERIALLY_WORSE", ("unable_to_determine", None, "unable_to_determine", None)),
])
def test_closed_final_and_point_target_matrix(lower, higher, lower_point, higher_point, expected):
    result = v._final_disposition(good(), lower, higher, lower_point, higher_point)
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
def test_private_table_helper_maps_every_canonical_directional_row(row):
    result = v._final_disposition(good(), row[0], row[1], "NOT_DISTINGUISHED", "NOT_DISTINGUISHED")
    assert (result["result"], result["review_direction"]) == (row[2], row[3])


@pytest.mark.parametrize("row", v.POINT_STATE_TABLE)
def test_private_table_helper_maps_every_canonical_point_row(row):
    result = v._final_disposition(good(), "CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", row[0], row[1])
    assert (result["point_target_assessment"], result["method_review_direction"]) == (row[2], row[3])


@pytest.mark.parametrize("replacement", [
    {},
    {"drawdown": "-0.50", "extra": "0"},
    {"wrong_operand": "-0.50"},
    {"drawdown": ["-0.50"]},
])
def test_formula_operand_schema_is_exact_and_closed(replacement):
    evidence = raw_study_evidence()
    evidence["directions"]["LOWER"]["observations"][0]["raw_operands"] = replacement
    with pytest.raises(v.RuntimeAuthorityError):
        v.evaluate_study_evidence(evidence)


def test_point_evidence_reduction_distinguishes_worse_from_indistinguishable():
    worse = {"PATH_RISK": "WORSENS", "RECOVERY": "WORSENS", "OPPORTUNITY_COST": "EQUIVALENT"}
    equivalent = {family: "EQUIVALENT" for family in v.VOTING_FAMILIES}
    improving = {"PATH_RISK": "IMPROVES", "RECOVERY": "IMPROVES", "OPPORTUNITY_COST": "EQUIVALENT"}
    unavailable = {"PATH_RISK": "UNAVAILABLE", "RECOVERY": "EQUIVALENT", "OPPORTUNITY_COST": "EQUIVALENT"}
    assert v._point_evidence(good(), worse) == "ADJACENT_MATERIALLY_WORSE"
    assert v._point_evidence(good(), equivalent) == "NOT_DISTINGUISHED"
    assert v._point_evidence(good(), improving) == "DISPLACES_REFERENCE"
    assert v._point_evidence(good(), unavailable) == "UNAVAILABLE"


def test_validation_does_not_mutate_input():
    data = good()
    before = copy.deepcopy(data)
    v.validate(data)
    assert data == before
