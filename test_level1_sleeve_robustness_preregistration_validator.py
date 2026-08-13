"""Focused mechanical tests for the RISK-0001 closed preregistration."""

from __future__ import annotations

import copy
from pathlib import Path

import yaml

import level1_sleeve_robustness_preregistration_validator as v


ROOT = Path(__file__).resolve().parent


def good() -> dict:
    return yaml.safe_load(v.PREREG_PATH.read_text(encoding="utf-8"))


def errors(data: dict) -> str:
    return "\n".join(v.validate(data).errors)


def test_live_preregistration_is_valid():
    assert v.validate_file().ok


def test_validator_is_read_only_and_hashes_raw_bytes():
    before = v.PREREG_PATH.read_bytes()
    result = v.validate_file()
    after = v.PREREG_PATH.read_bytes()
    assert result.ok
    assert before == after
    assert v.sha256_file(v.PREREG_PATH) == __import__("hashlib").sha256(before).hexdigest()


def test_exact_top_level_schema_is_closed():
    data = good()
    data["extra"] = "forbidden"
    assert "exact keys/order" in errors(data)


def test_wrong_study_or_authority_is_rejected():
    data = good()
    data["study_id"] = "RISK-9999"
    data["authority"]["architecture"] = "XASSET-0018"
    message = errors(data)
    assert "study_id" in message
    assert "authority.architecture" in message


def test_cohort_identity_and_count_are_exact():
    data = good()
    data["frozen_cohort"]["equity_ids"][0] = "AAPL"
    data["frozen_cohort"]["expected_core_count"] = 33
    message = errors(data)
    assert "frozen_cohort.equity_ids" in message
    assert "expected_core_count" in message


def test_equity_aggregate_and_broad_blend_are_prohibited():
    data = good()
    data["representations"]["EQUITY"]["aggregate_return_series"] = "PERMITTED"
    data["representations"]["FUND_BROAD_MARKET"]["combined_return_series"] = "PERMITTED"
    message = errors(data)
    assert "equity aggregate return" in message
    assert "broad-market combined return" in message


def test_cash_debt_residual_margin_exclusions_are_exact():
    data = good()
    data["representations"]["excluded"].remove("RESERVE")
    assert "representations.excluded" in errors(data)


def test_historical_reference_classification_and_values_are_exact():
    data = good()
    data["historical_reference_scenarios"]["classification"] = "baseline_policy"
    data["historical_reference_scenarios"]["values_pct"]["EQUITY"] = "20.00"
    message = errors(data)
    assert "historical reference classification" in message
    assert "historical reference values" in message


def test_scenario_states_are_exact_and_ordered():
    data = good()
    data["scenario_states"] = ["LOWER", "HIGHER", "HISTORICAL_REFERENCE"]
    assert "scenario_states" in errors(data)


def test_scenario_values_are_20_percent_relative_and_two_decimal_strings():
    data = good()
    data["scenario_magnitudes"]["values_pct"]["EQUITY"]["LOWER"] = "16.67"
    assert "EQUITY.LOWER" in errors(data)

    data = good()
    data["scenario_magnitudes"]["values_pct"]["CRYPTO"]["HIGHER"] = 20.0
    assert "exact two-decimal string" in errors(data)


def test_scenario_is_not_claimed_calibrated_optimized_or_inherited():
    for key in ("calibrated", "evidence_bounded", "optimized", "inherited_from_xasset_0016_r2_r3"):
        data = good()
        data["scenario_provenance"][key] = True
        assert f"scenario_provenance.{key}" in errors(data)


def test_exact_seven_windows_and_end_date_are_enforced():
    data = good()
    data["scenario_windows"]["windows"].pop()
    assert "scenario window ids" in errors(data)

    data = good()
    data["scenario_windows"]["evaluation_end"] = "2026-08-13"
    assert "evaluation_end" in errors(data)


def test_asset_specific_peak_trough_selection_is_prohibited():
    data = good()
    data["scenario_windows"]["asset_specific_peak_trough_selection"] = "PERMITTED"
    assert "asset peak/trough selection" in errors(data)


def test_missingness_vocabulary_is_closed():
    data = good()
    data["missingness_states"]["vocabulary"].append("ZERO_RETURN")
    assert "missingness vocabulary" in errors(data)


def test_crypto_gap_thresholds_are_zero_and_no_fill_is_allowed():
    data = good()
    gate = data["data_gate"]["crypto_gate"]
    gate["missing_days_allowed_per_registered_window"] = 1
    gate["maximum_contiguous_gap_days"] = 2
    gate["interpolation"] = "PERMITTED"
    gate["forward_fill"] = "PERMITTED"
    message = errors(data)
    assert "crypto missing threshold" in message
    assert "crypto gap threshold" in message
    assert "crypto interpolation" in message
    assert "crypto forward fill" in message


def test_dff_is_analytical_only_not_cash_or_residual():
    for key in ("strategic_cash", "residual", "funding_destination", "fifth_sleeve", "portfolio_policy"):
        data = good()
        data["comparator"][key] = True
        assert f"comparator.{key}" in errors(data)


def test_composite_score_is_prohibited():
    data = good()
    data["metric_families"]["composite_score"] = "PERMITTED"
    assert "metric_families.composite_score" in errors(data)


def test_dominance_requires_two_independent_families_and_conflict_abstains():
    data = good()
    data["dominance_rule"]["minimum_distinct_families_with_strict_improvement"] = 1
    data["dominance_rule"]["conflict_result"] = "average_representations"
    message = errors(data)
    assert "dominance minimum families" in message
    assert "dominance conflict" in message


def test_trial_inventory_is_37_times_3_times_7_and_has_no_reserve():
    data = good()
    data["trial_inventory"]["derived_registered_cell_ceiling"] = 776
    data["trial_inventory"]["reserve_trials"] = 1
    message = errors(data)
    assert "trial ceiling" in message
    assert "reserve_trials" in message


def test_result_vocabulary_is_closed_and_boundaries_false():
    data = good()
    data["result_vocabulary"]["result_states"]["validated"] = "forbidden"
    data["result_vocabulary"]["non_rejection_equals_validation"] = True
    data["result_vocabulary"]["policy_review_equals_automatic_change"] = True
    message = errors(data)
    assert "result states" in message
    assert "non-rejection boundary" in message
    assert "policy review boundary" in message


def test_required_prohibitions_cannot_be_removed():
    data = good()
    data["prohibited_scope"].remove("WHOLE_PORTFOLIO_CONSTRUCTION")
    assert "missing prohibited scope values" in errors(data)


def test_hash_contract_is_raw_sha256_without_self_hash():
    data = good()
    data["hash_version"]["algorithm"] = "SHA1"
    data["hash_version"]["canonical_bytes"] = "YAML_CANONICALIZED"
    data["hash_version"]["embedded_self_hash"] = True
    message = errors(data)
    assert "hash algorithm" in message
    assert "hash bytes" in message
    assert "embedded self hash" in message


def test_validator_imports_no_production_or_execution_modules():
    source = (ROOT / "level1_sleeve_robustness_preregistration_validator.py").read_text()
    forbidden = ("import allocate", "import margin_state", "import alpaca_client", "import levels")
    assert not any(token in source for token in forbidden)


def test_production_modules_do_not_import_validator():
    needle = "level1_sleeve_robustness_preregistration_validator"
    for name in ("allocate.py", "margin_state.py", "alpaca_client.py", "levels.py"):
        assert needle not in (ROOT / name).read_text(encoding="utf-8")


def test_validation_does_not_mutate_input():
    data = good()
    original = copy.deepcopy(data)
    v.validate(data)
    assert data == original
