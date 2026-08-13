"""Read-only mechanical validator for the RISK-0001 preregistration.

This module validates closed structure and arithmetic only.  It acquires no
data, executes no registered study cell, and imports no portfolio, allocator,
margin, or brokerage module.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent
PREREG_PATH = ROOT / "research/level1_sleeve_robustness/pre_registration.yaml"
PROTOCOL_PATH = ROOT / "research/level1_sleeve_robustness/PROTOCOL_V1.md"

TOP_KEYS = (
    "schema_version", "study_id", "authority", "frozen_cohort",
    "representations", "historical_reference_scenarios", "scenario_states",
    "scenario_magnitudes", "scenario_provenance", "data_sources",
    "fallback_order", "data_gate", "scenario_windows", "missingness_states",
    "alignment_rules", "corporate_action_rules", "comparator",
    "metric_families", "dominance_rule", "point_target_rule",
    "trial_inventory", "rerun_rule", "result_vocabulary", "prohibited_scope",
    "hash_version",
)

EQUITIES = (
    "AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GNRC",
    "GOOGL", "ICE", "ISRG", "KLAC", "LLY", "META", "MSFT", "NVDA",
    "PANW", "PWR", "RKLB", "RTX", "SNPS", "SPGI", "TMO", "TSLA",
    "TSM", "V", "WM",
)
BROAD = ("SPY", "VEA", "VWO")
GOLD = ("GLD", "IAU", "SGOL", "GLDM")
CRYPTO = ("BTC", "ETH", "SOL")
SCENARIOS = ("LOWER", "HISTORICAL_REFERENCE", "HIGHER")
WINDOWS = (
    "ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP", "GFC_2008",
    "Q4_2018", "COVID_2020", "RATE_INFLATION_2022", "CRYPTO_STRESS_2022",
)
MISSINGNESS = (
    "ELIGIBLE", "NOT_APPLICABLE_PRE_INCEPTION", "MISSING_SOURCE_DATA",
    "KNOWN_DATA_GAP", "CORPORATE_ACTION_UNRESOLVED",
    "CONDITIONAL_ASSET_NOT_ACQUIRED", "QUALITY_GATE_FAILED",
)
RESULT_STATES = (
    "provisional_scenario_not_rejected", "policy_review_required",
    "unable_to_determine",
)
PROHIBITED_REPRESENTATIONS = {
    "CASH", "RESERVE", "cash_reserve", "debt_reduction", "residual",
    "unassigned_capital", "margin", "leverage",
}


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _keys(value: Any, expected: tuple[str, ...], where: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{where}: expected mapping")
        return
    actual = tuple(value.keys())
    if actual != expected:
        errors.append(f"{where}: exact keys/order {actual!r} != {expected!r}")


def _exact(actual: Any, expected: Any, where: str, errors: list[str]) -> None:
    if actual != expected:
        errors.append(f"{where}: {actual!r} != {expected!r}")


def _pct(value: str) -> Decimal:
    if not isinstance(value, str) or len(value.split(".")) != 2 or len(value.split(".")[1]) != 2:
        raise ValueError(f"not an exact two-decimal string: {value!r}")
    return Decimal(value)


def validate(data: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    _keys(data, TOP_KEYS, "root", errors)
    if errors:
        return ValidationResult(tuple(errors))

    _exact(data["schema_version"], "1.0", "schema_version", errors)
    _exact(data["study_id"], "RISK-0001", "study_id", errors)
    _exact(data["authority"]["decision"], "RISK-0001", "authority.decision", errors)
    _exact(data["authority"]["architecture"], "XASSET-0019", "authority.architecture", errors)
    _exact(data["authority"]["cohort"], "LEVEL2-0001", "authority.cohort", errors)
    _exact(data["authority"]["execution_authority"], "ONE_LATER_IMPLEMENTATION_RESULTS_PR_ONLY", "authority.execution_authority", errors)
    _exact(data["authority"]["charter_pr_data_acquisition"], "PROHIBITED", "authority.charter_pr_data_acquisition", errors)
    _exact(data["authority"]["charter_pr_study_execution"], "PROHIBITED", "authority.charter_pr_study_execution", errors)
    _exact(data["authority"]["policy_adoption"], "PROHIBITED", "authority.policy_adoption", errors)

    cohort = data["frozen_cohort"]
    _exact(cohort["expected_core_count"], 34, "frozen_cohort.expected_core_count", errors)
    _exact(tuple(cohort["equity_ids"]), EQUITIES, "frozen_cohort.equity_ids", errors)
    _exact(tuple(cohort["broad_market_ids"]), BROAD, "frozen_cohort.broad_market_ids", errors)
    _exact(tuple(cohort["defensive_core_ids"]), ("GLD",), "frozen_cohort.defensive_core_ids", errors)
    _exact(tuple(cohort["crypto_ids"]), CRYPTO, "frozen_cohort.crypto_ids", errors)

    reps = data["representations"]
    _exact(tuple(reps.keys()), ("EQUITY", "FUND_BROAD_MARKET", "FUND_GLD_DEFENSIVE", "CRYPTO", "excluded"), "representations keys", errors)
    _exact(tuple(reps["EQUITY"]["ids"]), EQUITIES, "representations.EQUITY.ids", errors)
    _exact(tuple(reps["FUND_BROAD_MARKET"]["ids"]), BROAD, "representations.FUND_BROAD_MARKET.ids", errors)
    _exact(tuple(reps["FUND_GLD_DEFENSIVE"]["core_ids"] + reps["FUND_GLD_DEFENSIVE"]["conditional_ids"]), GOLD, "representations.FUND_GLD_DEFENSIVE ids", errors)
    _exact(tuple(reps["CRYPTO"]["ids"]), CRYPTO, "representations.CRYPTO.ids", errors)
    _exact(set(reps["excluded"]), PROHIBITED_REPRESENTATIONS, "representations.excluded", errors)
    if reps["EQUITY"]["aggregate_return_series"] != "PROHIBITED":
        errors.append("equity aggregate return must be prohibited")
    if reps["FUND_BROAD_MARKET"]["combined_return_series"] != "PROHIBITED":
        errors.append("broad-market combined return must be prohibited")

    refs = data["historical_reference_scenarios"]
    _exact(refs["classification"], "historical_provisional_reference", "historical reference classification", errors)
    expected_refs = {
        "EQUITY": "18.67", "FUND_BROAD_MARKET": "14.67",
        "FUND_GLD_DEFENSIVE": "16.67", "CRYPTO": "16.67",
    }
    _exact(refs["values_pct"], expected_refs, "historical reference values", errors)
    _exact(tuple(data["scenario_states"]), SCENARIOS, "scenario_states", errors)

    mags = data["scenario_magnitudes"]["values_pct"]
    for family, ref in expected_refs.items():
        _exact(tuple(mags[family].keys()), SCENARIOS, f"{family} scenario keys", errors)
        try:
            r = _pct(ref)
            expected_lower = (r * Decimal("0.80")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            expected_higher = (r * Decimal("1.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            _exact(_pct(mags[family]["LOWER"]), expected_lower, f"{family}.LOWER", errors)
            _exact(_pct(mags[family]["HISTORICAL_REFERENCE"]), r, f"{family}.HISTORICAL_REFERENCE", errors)
            _exact(_pct(mags[family]["HIGHER"]), expected_higher, f"{family}.HIGHER", errors)
        except (ValueError, KeyError) as exc:
            errors.append(f"{family} scenario magnitude: {exc}")

    provenance = data["scenario_provenance"]
    _exact(provenance["relative_perturbation"], "0.20", "relative perturbation", errors)
    for flag in ("calibrated", "evidence_bounded", "optimized", "inherited_from_xasset_0016_r2_r3"):
        _exact(provenance[flag], False, f"scenario_provenance.{flag}", errors)

    windows = data["scenario_windows"]
    _exact(windows["count"], 7, "scenario_windows.count", errors)
    _exact(windows["evaluation_end"], "2026-07-31", "scenario_windows.evaluation_end", errors)
    _exact(tuple(w["id"] for w in windows["windows"]), WINDOWS, "scenario window ids", errors)
    _exact(windows["asset_specific_peak_trough_selection"], "PROHIBITED", "asset peak/trough selection", errors)

    _exact(tuple(data["missingness_states"]["vocabulary"]), MISSINGNESS, "missingness vocabulary", errors)
    crypto_gate = data["data_gate"]["crypto_gate"]
    _exact(crypto_gate["missing_days_allowed_per_registered_window"], 0, "crypto missing threshold", errors)
    _exact(crypto_gate["maximum_contiguous_gap_days"], 0, "crypto gap threshold", errors)
    _exact(crypto_gate["interpolation"], "PROHIBITED", "crypto interpolation", errors)
    _exact(crypto_gate["forward_fill"], "PROHIBITED", "crypto forward fill", errors)

    comparator = data["comparator"]
    for flag in ("strategic_cash", "residual", "funding_destination", "fifth_sleeve", "portfolio_policy"):
        _exact(comparator[flag], False, f"comparator.{flag}", errors)
    _exact(comparator["series"], "DFF", "comparator.series", errors)

    metrics = data["metric_families"]
    _exact(metrics["composite_score"], "PROHIBITED", "metric_families.composite_score", errors)
    _exact(data["dominance_rule"]["minimum_distinct_families_with_strict_improvement"], 2, "dominance minimum families", errors)
    _exact(data["dominance_rule"]["conflict_result"], "unable_to_determine", "dominance conflict", errors)

    inventory = data["trial_inventory"]
    _exact(inventory["representation_count"], 37, "trial representation count", errors)
    _exact(inventory["scenario_count"], 3, "trial scenario count", errors)
    _exact(inventory["window_class_count"], 7, "trial window count", errors)
    derived = inventory["representation_count"] * inventory["scenario_count"] * inventory["window_class_count"]
    _exact(inventory["derived_registered_cell_ceiling"], derived, "trial ceiling", errors)
    _exact(derived, 777, "trial ceiling fixed derivation", errors)
    _exact(inventory["reserve_trials"], 0, "reserve_trials", errors)

    vocab = data["result_vocabulary"]
    _exact(tuple(vocab["result_states"].keys()), RESULT_STATES, "result states", errors)
    _exact(tuple(vocab["review_direction"]), ("lower_exposure", "higher_exposure", None), "review direction", errors)
    _exact(tuple(vocab["point_target_assessment"]), ("not_supported", "not_rejected", "unable_to_determine"), "point target vocabulary", errors)
    _exact(vocab["non_rejection_equals_validation"], False, "non-rejection boundary", errors)
    _exact(vocab["policy_review_equals_automatic_change"], False, "policy review boundary", errors)

    prohibited = set(data["prohibited_scope"])
    required_prohibitions = {
        "FINAL_LEVEL1_TARGETS", "FINAL_LEVEL2_MEMBERSHIP", "LEVEL2_WEIGHTS",
        "OPTIMIZER_OR_WEIGHT_GRID_SEARCH", "RESIDUAL_REDISTRIBUTION",
        "DEBT_OR_MARGIN_ANALYSIS", "LEVERAGE", "TRADES_OR_ORDERS",
        "ALLOCATOR_MUTATION", "TARGETS_YAML_MUTATION", "HOLDINGS_MUTATION",
        "AUTOMATIC_ADOPTION", "UNREGISTERED_TRIALS", "AUTOMATIC_RERUNS",
        "WHOLE_PORTFOLIO_CONSTRUCTION", "WHOLE_100_PERCENT_RECONCILIATION",
    }
    missing = required_prohibitions - prohibited
    if missing:
        errors.append(f"missing prohibited scope values: {sorted(missing)!r}")

    hash_version = data["hash_version"]
    _exact(hash_version["algorithm"], "SHA256", "hash algorithm", errors)
    _exact(hash_version["canonical_bytes"], "RAW_FILE_BYTES_AS_COMMITTED", "hash bytes", errors)
    _exact(hash_version["embedded_self_hash"], False, "embedded self hash", errors)

    return ValidationResult(tuple(errors))


def validate_file(path: Path = PREREG_PATH) -> ValidationResult:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        return ValidationResult(("root: expected mapping",))
    return validate(loaded)


def main() -> int:
    result = validate_file()
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}")
        return 1
    print(f"RISK-0001 preregistration valid; protocol_sha256={sha256_file(PROTOCOL_PATH)}; preregistration_sha256={sha256_file(PREREG_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
