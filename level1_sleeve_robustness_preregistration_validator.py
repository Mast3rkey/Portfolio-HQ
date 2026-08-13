"""Fail-closed mechanical validator and result mapper for RISK-0001.

This module validates governance bytes and structured authority only.  It does
not acquire market data, execute a registered cell, or import production code.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml


ROOT = Path(__file__).resolve().parent
PREREG_PATH = ROOT / "research/level1_sleeve_robustness/pre_registration.yaml"
PROTOCOL_PATH = ROOT / "research/level1_sleeve_robustness/PROTOCOL_V1.md"
DECISION_PATH = ROOT / "governance/decisions/RISK-0001-level1-investable-sleeve-robustness-charter.md"

TOP_KEYS = (
    "schema_version", "study_id", "authority", "frozen_cohort", "representations",
    "historical_reference_scenarios", "scenario_states", "scenario_magnitudes",
    "scenario_provenance", "consequential_parameter_registry", "data_sources",
    "fallback_order", "data_gate", "scenario_windows", "missingness_states",
    "alignment_rules", "corporate_action_rules", "comparator", "metric_families",
    "result_reduction", "trial_inventory", "rerun_rule", "result_vocabulary",
    "prohibited_scope", "hash_version",
)
FAMILIES = ("EQUITY", "FUND_BROAD_MARKET", "FUND_GLD_DEFENSIVE", "CRYPTO")
EQUITIES = ("AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GNRC", "GOOGL", "ICE", "ISRG", "KLAC", "LLY", "META", "MSFT", "NVDA", "PANW", "PWR", "RKLB", "RTX", "SNPS", "SPGI", "TMO", "TSLA", "TSM", "V", "WM")
BROAD = ("SPY", "VEA", "VWO")
GOLD = ("GLD", "IAU", "SGOL", "GLDM")
CRYPTO = ("BTC", "ETH", "SOL")
SCENARIOS = ("LOWER", "HISTORICAL_REFERENCE", "HIGHER")
WINDOWS = ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP", "GFC_2008", "Q4_2018", "COVID_2020", "RATE_INFLATION_2022", "CRYPTO_STRESS_2022")
WINDOW_DATES = (
    ("ASSET_AVAILABLE_HISTORY", "2004-11-18", "2026-07-31"),
    ("FAMILY_COMMON_OVERLAP", None, "2026-07-31"),
    ("GFC_2008", "2007-12-01", "2009-06-30"),
    ("Q4_2018", "2018-10-01", "2018-12-31"),
    ("COVID_2020", "2020-02-01", "2020-04-30"),
    ("RATE_INFLATION_2022", "2022-01-01", "2022-12-31"),
    ("CRYPTO_STRESS_2022", "2022-05-01", "2022-12-31"),
)
MISSINGNESS = ("ELIGIBLE", "NOT_APPLICABLE_PRE_INCEPTION", "MISSING_SOURCE_DATA", "KNOWN_DATA_GAP", "CORPORATE_ACTION_UNRESOLVED", "CONDITIONAL_ASSET_NOT_ACQUIRED", "QUALITY_GATE_FAILED")
METRIC_FAMILY_ORDER = ("PATH_RISK", "RECOVERY", "OPPORTUNITY_COST", "CONTRIBUTION", "EQUITY_CROSS_SECTION", "REPRESENTATION", "CO_BEHAVIOR")
VOTING_FAMILIES = ("PATH_RISK", "RECOVERY", "OPPORTUNITY_COST")
OBSERVATION_STATES = ("IMPROVES", "EQUIVALENT", "WORSENS", "UNAVAILABLE", "NOT_APPLICABLE")
FAMILY_STATES = ("IMPROVES", "EQUIVALENT", "WORSENS", "UNAVAILABLE", "CONFLICT")
DIRECTIONAL_STATES = ("POLICY_REVIEW_REQUIRED", "CENTER_NOT_REJECTED", "UNABLE_TO_DETERMINE")
POINT_EVIDENCE_STATES = ("DISPLACES_REFERENCE", "ADJACENT_MATERIALLY_WORSE", "NOT_DISTINGUISHED", "UNAVAILABLE")

PARAMETER_KEYS = ("parameter_id", "value", "unit", "num_0001_class", "contextual_class", "selection_basis", "evidence_status", "binding_scope", "valid_for_study_id", "lapse_condition", "reuse_rule", "canonical_source", "calibrated", "evidence_bounded")
PARAMETER_SPECS = {
    "RELATIVE_PERTURBATION": ("0.20", "PROPORTION", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "DFF_DAY_COUNT_DENOMINATOR": (360, "DAYS", "EXTERNALLY_IMPOSED"),
    "DFF_MISSING_DAYS_ALLOWED": (0, "CALENDAR_DAYS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "MINIMUM_IMPROVEMENT_FAMILIES": (2, "INDEPENDENT_FAMILIES", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "LOSS_CONTRIBUTION_TOLERANCE_PP": ("1.00", "PERCENTAGE_POINTS_OF_UNSPECIFIED_ASSET_STATE", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "RECOVERY_BURDEN_TOLERANCE_PPDAYS": ("30.00", "PERCENTAGE_POINT_DAYS_OF_UNSPECIFIED_ASSET_STATE", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP": ("1.00", "PERCENTAGE_POINTS_OF_UNSPECIFIED_ASSET_STATE", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "EQUITY_MINIMUM_ELIGIBLE": (21, "CONSTITUENTS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "EQUITY_DIRECTIONAL_BREADTH": ("0.75", "PROPORTION_OF_ELIGIBLE_CONSTITUENTS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "GOLD_PARITY_CORRELATION_MIN": ("0.995", "PEARSON_CORRELATION", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "GOLD_PARITY_RETURN_MAX_PP": ("0.50", "ANNUALIZED_RETURN_PERCENTAGE_POINTS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "GOLD_PARITY_DRAWDOWN_MAX_PP": ("2.00", "MAX_DRAWDOWN_PERCENTAGE_POINTS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "CRYPTO_MISSING_DAYS_ALLOWED": (0, "UTC_DAYS_PER_REGISTERED_WINDOW", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS": (0, "UTC_DAYS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
}
PARAMETER_GOVERNANCE = {
    "RELATIVE_PERTURBATION": ("SYMMETRIC_COARSE_SENSITIVITY_WITHOUT_GRID_SEARCH", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "SCENARIO_CONSTRUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "DFF_DAY_COUNT_DENOMINATOR": ("DFF_MONEY_MARKET_ACTUAL_360_QUOTATION_CONVENTION", "CONVENTION_NOT_CALIBRATION", "DFF_DAILY_ACCRUAL", "REVALIDATE_CONVENTION_UNDER_NEW_AUTHORITY"),
    "DFF_MISSING_DAYS_ALLOWED": ("NO_IMPUTATION_OF_MISSING_COMPARATOR_OBSERVATIONS", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "AFFECTED_OPPORTUNITY_COST_METRIC_WINDOWS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "MINIMUM_IMPROVEMENT_FAMILIES": ("MULTIDIMENSION_CONFIRMATION_WITHOUT_METRIC_WEIGHTING", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "DIRECTIONAL_POLICY_REVIEW_TRIGGER", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "LOSS_CONTRIBUTION_TOLERANCE_PP": ("MATERIAL_DIFFERENCE_GUARDRAIL_FOR_EXPOSURE_SCALED_LOSS", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "PATH_RISK_METRICS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "RECOVERY_BURDEN_TOLERANCE_PPDAYS": ("MATERIAL_DIFFERENCE_GUARDRAIL_FOR_EXPOSURE_SCALED_UNDERWATER_BURDEN", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "RECOVERY_METRICS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP": ("MATERIAL_DIFFERENCE_GUARDRAIL_FOR_EXPOSURE_SCALED_EXCESS_RETURN", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "OPPORTUNITY_COST_METRICS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "EQUITY_MINIMUM_ELIGIBLE": ("THREE_QUARTERS_OF_FROZEN_27_ROUNDED_UP", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "EQUITY_REPRESENTATION_REDUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "EQUITY_DIRECTIONAL_BREADTH": ("SUPERMAJORITY_DIRECTIONAL_CONSISTENCY_WITHOUT_AGGREGATE_PATH", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "EQUITY_REPRESENTATION_REDUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_PARITY_CORRELATION_MIN": ("STRICT_SAME_EXPOSURE_REPRESENTATION_PARITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_PARITY_RETURN_MAX_PP": ("STRICT_SAME_EXPOSURE_RETURN_PARITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_PARITY_DRAWDOWN_MAX_PP": ("STRICT_SAME_EXPOSURE_PATH_PARITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "CRYPTO_MISSING_DAYS_ALLOWED": ("COMPLETE_24_7_PATH_REQUIRED_WITHOUT_IMPUTATION", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "CRYPTO_CELL_ELIGIBILITY", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS": ("COMPLETE_24_7_PATH_REQUIRED_WITHOUT_IMPUTATION", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "CRYPTO_CELL_ELIGIBILITY", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
}

METRIC_KEYS = ("metric_id", "family", "formula", "direction_of_preference", "unit", "materiality_parameter_id", "equivalence_parameter_id", "applicable_research_units", "applicable_windows", "voting_status", "missing_result_behavior")
METRIC_SPECS = {
    "MAX_DRAWDOWN": ("PATH_RISK", "HIGHER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "WORST_MONTH": ("PATH_RISK", "HIGHER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "WORST_QUARTER": ("PATH_RISK", "HIGHER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "STRESS_WINDOW_RETURN": ("PATH_RISK", "HIGHER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "VOLATILITY": ("PATH_RISK", "LOWER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "EXPOSURE_SCALED_DRAWDOWN_LOSS": ("PATH_RISK", "LOWER", "LOSS_CONTRIBUTION_TOLERANCE_PP", "LOSS_CONTRIBUTION_TOLERANCE_PP", "MANDATORY_VOTING"),
    "EXPOSURE_SCALED_STRESS_LOSS": ("PATH_RISK", "LOWER", "LOSS_CONTRIBUTION_TOLERANCE_PP", "LOSS_CONTRIBUTION_TOLERANCE_PP", "CONDITIONAL_VOTING"),
    "EXPOSURE_SCALED_UNDERWATER_BURDEN": ("RECOVERY", "LOWER", "RECOVERY_BURDEN_TOLERANCE_PPDAYS", "RECOVERY_BURDEN_TOLERANCE_PPDAYS", "MANDATORY_VOTING"),
    "RECOVERY_DURATION_DAYS": ("RECOVERY", "LOWER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "RECOVERY_CENSOR_STATUS": ("RECOVERY", "NONE", None, None, "NON_VOTING_DIAGNOSTIC"),
    "EXCESS_TOTAL_RETURN": ("OPPORTUNITY_COST", "HIGHER", None, None, "NON_VOTING_DIAGNOSTIC"),
    "EXPOSURE_SCALED_EXCESS_CONTRIBUTION": ("OPPORTUNITY_COST", "HIGHER", "OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP", "OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP", "MANDATORY_VOTING"),
    "CONSTITUENT_LOSS_ENVELOPE": ("CONTRIBUTION", "NONE", None, None, "NON_VOTING_DIAGNOSTIC"),
    "EQUITY_BREADTH_AND_DISPERSION": ("EQUITY_CROSS_SECTION", "NONE", None, None, "NON_VOTING_REDUCTION_GATE"),
    "EQUITY_LEAVE_ONE_OUT_DIRECTION": ("EQUITY_CROSS_SECTION", "NONE", None, None, "NON_VOTING_REDUCTION_GATE"),
    "REPRESENTATION_DIRECTION_CONFLICT": ("REPRESENTATION", "NONE", None, None, "NON_VOTING_VETO"),
    "PAIRWISE_RETURN_CORRELATION": ("CO_BEHAVIOR", "NONE", None, None, "NON_VOTING_DIAGNOSTIC"),
    "JOINT_NEGATIVE_INTERVAL_FREQUENCY": ("CO_BEHAVIOR", "NONE", None, None, "NON_VOTING_DIAGNOSTIC"),
}
METRIC_DETAILS = {
    "MAX_DRAWDOWN": ("MIN_INDEX_OVER_RUNNING_PEAK_MINUS_ONE", "RETURN", ("ALL",), ("ALL",), "REPORT_UNAVAILABLE"),
    "WORST_MONTH": ("LOWEST_CALENDAR_MONTH_COMPOUNDED_TOTAL_RETURN", "RETURN", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "REPORT_UNAVAILABLE"),
    "WORST_QUARTER": ("LOWEST_CALENDAR_QUARTER_COMPOUNDED_TOTAL_RETURN", "RETURN", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "REPORT_UNAVAILABLE"),
    "STRESS_WINDOW_RETURN": ("COMPOUNDED_TOTAL_RETURN_OVER_FIXED_STRESS_WINDOW", "RETURN", ("ALL",), ("FIXED_STRESS",), "REPORT_UNAVAILABLE"),
    "VOLATILITY": ("SAMPLE_STANDARD_DEVIATION_OF_NATIVE_SIMPLE_RETURNS_ANNUALIZED_252_EQUITY_ETF_365_CRYPTO", "ANNUALIZED_VOLATILITY", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "REPORT_UNAVAILABLE"),
    "EXPOSURE_SCALED_DRAWDOWN_LOSS": ("SCENARIO_EXPOSURE_PROPORTION_TIMES_ABSOLUTE_MAX_DRAWDOWN_TIMES_100", "PERCENTAGE_POINTS_OF_UNSPECIFIED_ASSET_STATE", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "FAMILY_UNAVAILABLE"),
    "EXPOSURE_SCALED_STRESS_LOSS": ("SCENARIO_EXPOSURE_PROPORTION_TIMES_MAX_ZERO_MINUS_STRESS_RETURN_TIMES_100", "PERCENTAGE_POINTS_OF_UNSPECIFIED_ASSET_STATE", ("ALL",), ("FIXED_STRESS",), "PRE_INCEPTION_NOT_APPLICABLE_OTHERWISE_FAMILY_UNAVAILABLE"),
    "EXPOSURE_SCALED_UNDERWATER_BURDEN": ("SCENARIO_EXPOSURE_PROPORTION_TIMES_SUM_MAX_ZERO_ONE_MINUS_INDEX_OVER_RUNNING_PEAK_TIMES_INTERVAL_DAYS_TIMES_100", "PERCENTAGE_POINT_DAYS_OF_UNSPECIFIED_ASSET_STATE", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "FAMILY_UNAVAILABLE"),
    "RECOVERY_DURATION_DAYS": ("CALENDAR_DAYS_FROM_DRAWDOWN_PEAK_TO_FIRST_INDEX_AT_OR_ABOVE_PRIOR_PEAK", "CALENDAR_DAYS", ("ALL",), ("ALL",), "REPORT_CENSORED_OR_UNAVAILABLE"),
    "RECOVERY_CENSOR_STATUS": ("RECOVERED_OR_CENSORED_AT_WINDOW_END", "ENUM", ("ALL",), ("ALL",), "REPORT_UNAVAILABLE"),
    "EXCESS_TOTAL_RETURN": ("ASSET_TOTAL_RETURN_MINUS_COMPOUNDED_DFF_TOTAL_RETURN", "RETURN", ("ALL",), ("ALL",), "REPORT_UNAVAILABLE"),
    "EXPOSURE_SCALED_EXCESS_CONTRIBUTION": ("SCENARIO_EXPOSURE_PROPORTION_TIMES_EXCESS_TOTAL_RETURN_TIMES_100", "PERCENTAGE_POINTS_OF_UNSPECIFIED_ASSET_STATE", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "FAMILY_UNAVAILABLE"),
    "CONSTITUENT_LOSS_ENVELOPE": ("MIN_MEDIAN_MAX_OF_PER_CONSTITUENT_EXPOSURE_SCALED_LOSS_WITHOUT_AGGREGATE_PATH", "DISTRIBUTION", ("EQUITY",), ("ALL",), "REPORT_ELIGIBLE_AND_EXPECTED_COUNTS"),
    "EQUITY_BREADTH_AND_DISPERSION": ("COUNT_PROPORTION_MEDIAN_P10_P25_P75_P90_MIN_MAX_IQR_RANGE_CLUSTER_DISPERSION", "DISTRIBUTION", ("EQUITY",), ("ALL",), "APPLY_EQUITY_MINIMUM_ELIGIBLE"),
    "EQUITY_LEAVE_ONE_OUT_DIRECTION": ("REPEAT_EQUITY_DIRECTION_REDUCTION_OMITTING_EACH_ELIGIBLE_CONSTITUENT_ONCE", "STATE_SET", ("EQUITY",), ("ALL",), "FAMILY_UNAVAILABLE_IF_UNSTABLE"),
    "REPRESENTATION_DIRECTION_CONFLICT": ("EXACT_SET_OF_LAWFUL_REPRESENTATION_FAMILY_STATES", "STATE_SET", ("FUND_BROAD_MARKET", "FUND_GLD_DEFENSIVE", "CRYPTO"), ("ALL",), "APPLY_REPRESENTATION_REDUCTION"),
    "PAIRWISE_RETURN_CORRELATION": ("PAIRWISE_PEARSON_NATIVE_DAILY_TOTAL_RETURN_CORRELATION", "CORRELATION", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "REPORT_UNAVAILABLE"),
    "JOINT_NEGATIVE_INTERVAL_FREQUENCY": ("COUNT_BOTH_NEGATIVE_OVER_COMMON_ELIGIBLE_INTERVAL_COUNT", "PROPORTION", ("ALL",), ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP"), "REPORT_UNAVAILABLE"),
}

TOTAL_STATE_TABLE = (
    ("POLICY_REVIEW_REQUIRED", "POLICY_REVIEW_REQUIRED", "unable_to_determine", None),
    ("POLICY_REVIEW_REQUIRED", "CENTER_NOT_REJECTED", "policy_review_required", "lower_exposure"),
    ("POLICY_REVIEW_REQUIRED", "UNABLE_TO_DETERMINE", "unable_to_determine", None),
    ("CENTER_NOT_REJECTED", "POLICY_REVIEW_REQUIRED", "policy_review_required", "higher_exposure"),
    ("CENTER_NOT_REJECTED", "CENTER_NOT_REJECTED", "provisional_scenario_not_rejected", None),
    ("CENTER_NOT_REJECTED", "UNABLE_TO_DETERMINE", "unable_to_determine", None),
    ("UNABLE_TO_DETERMINE", "POLICY_REVIEW_REQUIRED", "unable_to_determine", None),
    ("UNABLE_TO_DETERMINE", "CENTER_NOT_REJECTED", "unable_to_determine", None),
    ("UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE", "unable_to_determine", None),
)
POINT_STATE_TABLE = tuple(
    (lower, higher,
     "unable_to_determine" if "UNAVAILABLE" in (lower, higher) else
     "not_supported" if "DISPLACES_REFERENCE" in (lower, higher) or (lower == higher == "NOT_DISTINGUISHED") else
     "not_rejected",
     None if "UNAVAILABLE" in (lower, higher) or ("ADJACENT_MATERIALLY_WORSE" in (lower, higher) and "DISPLACES_REFERENCE" not in (lower, higher)) else "range_or_nonpoint")
    for lower in POINT_EVIDENCE_STATES for higher in POINT_EVIDENCE_STATES
)

PROHIBITED_SCOPE = ("FINAL_LEVEL1_TARGETS", "FINAL_LEVEL2_MEMBERSHIP", "LEVEL2_WEIGHTS", "OPTIMIZER_OR_WEIGHT_GRID_SEARCH", "COMPOSITE_SCORE", "RESIDUAL_REDISTRIBUTION", "STRATEGIC_CASH_POLICY", "CASH_OR_RESERVE_AS_RESEARCH_SLEEVE", "DEBT_OR_MARGIN_ANALYSIS", "LEVERAGE", "CHART_OR_TECHNICAL_SIGNALS", "TRADES_OR_ORDERS", "ALLOCATOR_MUTATION", "TARGETS_YAML_MUTATION", "HOLDINGS_MUTATION", "AUTOMATIC_ADOPTION", "UNREGISTERED_TRIALS", "AUTOMATIC_RERUNS", "WHOLE_PORTFOLIO_CONSTRUCTION", "WHOLE_100_PERCENT_RECONCILIATION", "RESIDUAL_PROXY_OR_RETURN_SERIES", "REPLACEMENT_LEVEL1_METHOD_CREATION")


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _keys(value: Any, expected: Sequence[str], where: str, errors: list[str]) -> bool:
    if type(value) is not dict:
        errors.append(f"{where}: expected mapping, got {type(value).__name__}")
        return False
    actual = tuple(value.keys())
    if actual != tuple(expected):
        errors.append(f"{where}: exact keys/order {actual!r} != {tuple(expected)!r}")
        return False
    return True


def _list(value: Any, where: str, errors: list[str]) -> bool:
    if type(value) is not list:
        errors.append(f"{where}: expected list, got {type(value).__name__}")
        return False
    return True


def _exact(actual: Any, expected: Any, where: str, errors: list[str]) -> None:
    if type(actual) is not type(expected) or actual != expected:
        errors.append(f"{where}: {actual!r} ({type(actual).__name__}) != {expected!r} ({type(expected).__name__})")


def _closed(value: Any, schema: Any, where: str, errors: list[str]) -> None:
    """Recursively enforce exact keys, list cardinality/order, types, and literals."""
    if type(schema) is dict:
        if not _keys(value, tuple(schema.keys()), where, errors):
            return
        for key, child in schema.items():
            _closed(value[key], child, f"{where}.{key}", errors)
    elif type(schema) is list:
        if not _list(value, where, errors):
            return
        if len(value) != len(schema):
            errors.append(f"{where}: list length {len(value)} != {len(schema)}")
            return
        for index, child in enumerate(schema):
            _closed(value[index], child, f"{where}[{index}]", errors)
    elif isinstance(schema, type):
        if type(value) is not schema:
            errors.append(f"{where}: expected {schema.__name__}, got {type(value).__name__}")
    else:
        _exact(value, schema, where, errors)


def _mapping_schema(data: Mapping[str, Any], keys: Sequence[str]) -> dict[str, type]:
    return {key: type(data[key]) for key in keys}


def _param(data: Mapping[str, Any], parameter_id: str) -> Any:
    for record in data["consequential_parameter_registry"]["parameters"]:
        if record.get("parameter_id") == parameter_id:
            return record.get("value")
    raise KeyError(parameter_id)


def _validate_structural_closure(data: dict[str, Any], errors: list[str]) -> None:
    if not _keys(data, TOP_KEYS, "root", errors):
        return
    fixed_keys = {
        "authority": ("decision", "architecture", "cohort", "numeric_provenance", "lifecycle", "execution_authority", "charter_pr_data_acquisition", "charter_pr_study_execution", "policy_adoption", "computational_authority", "narrative_fields_authoritative", "question_id"),
        "frozen_cohort": ("source", "scope", "expected_core_count", "equity_count", "equity_ids", "broad_market_ids", "defensive_core_ids", "crypto_ids", "final_membership_authority", "level2_sizing_authority"),
        "representations": ("family_order", "EQUITY", "FUND_BROAD_MARKET", "FUND_GLD_DEFENSIVE", "CRYPTO", "excluded"),
        "historical_reference_scenarios": ("classification", "semantics", "values_pct"),
        "scenario_magnitudes": ("unit", "values_pct", "freeze_status", "portfolio_reconciliation", "residual_assignment"),
        "scenario_provenance": ("method", "relative_perturbation_parameter_id", "formula", "rounding", "calibrated", "evidence_bounded", "optimized", "inherited_from_xasset_0016_r2_r3", "lapse", "reuse"),
        "consequential_parameter_registry": ("record_keys", "parameters", "derived_identities"),
        "data_sources": ("equities_etfs", "crypto", "comparator", "corporate_actions", "secondary_reconciliation"),
        "fallback_order": ("equities_etfs", "crypto", "comparator", "corporate_actions", "provider_change_after_result_inspection", "fallback_retry_before_registered_execution"),
        "data_gate": ("stage_order", "GLOBAL_STUDY_INTEGRITY", "CELL_DATA_ELIGIBILITY", "preexecution_freeze", "required_receipts", "integrity_rules", "gld_conditional_peer_gate", "crypto_gate"),
        "scenario_windows": ("count", "evaluation_end", "windows", "asset_specific_peak_trough_selection"),
        "missingness_states": ("vocabulary", "zero_return_standin", "result_table_requirements"),
        "alignment_rules": ("equity_etf_calendar", "equity_etf_observation", "crypto_calendar", "common_evaluation_timestamp", "crypto_mapping", "weekend_crypto_rule", "comparator_interval", "future_observation_mapped_backward", "missing_observation_as_zero", "native_path_reporting"),
        "corporate_action_rules": ("equities_etfs_total_return_method", "total_return_series_combined_with_explicit_dividends", "dividends", "splits", "spin_offs", "ticker_changes", "mergers", "legal_entity_continuity", "listing_inception", "synthetic_predecessor_stitching", "known_boundaries", "unresolved_period", "gold_fund_expense_treatment", "crypto_yield"),
        "comparator": ("series", "role", "strategic_cash", "residual", "funding_destination", "fifth_sleeve", "portfolio_policy", "annual_rate_unit", "accrual_convention", "day_count_parameter_id", "daily_factor", "availability_lag", "calendar_day_rule", "missing_rate_parameter_id", "missing_rate_rule", "evaluation_alignment"),
        "metric_families": ("family_order", "voting_families", "non_voting_families", "metrics", "composite_score"),
        "result_reduction": ("canonical_states", "observation_rule", "metric_window_reduction", "family_metric_reduction", "representation_reduction", "monotonicity", "directional_policy_review", "point_evidence_rule", "total_state_table", "point_state_table"),
        "trial_inventory": ("representation_count", "representation_derivation", "scenario_count", "window_class_count", "derived_registered_cell_ceiling", "formula", "cell_identity", "metrics_from_same_path_are_new_trials", "failed_discarded_ineligible_attempts_remain_accounted", "reserve_trials", "unused_capacity_reallocation", "new_cells_after_results", "conditional_gld_cells_count_inside_ceiling"),
        "rerun_rule": ("after_results_observed", "required_authority", "allowed_basis", "discovered_defect_automatic_rerun", "preregistered_fallback_retries_before_execution", "known_historical_windows_held_out_claim", "terminology", "protocol_held_out", "prospective_evidence"),
        "result_vocabulary": ("result_states", "review_direction", "point_target_assessment", "method_review_direction", "non_rejection_equals_validation", "policy_review_equals_automatic_change"),
        "hash_version": ("algorithm", "canonical_bytes", "authority_pin_location", "embedded_self_hash", "protocol_path", "preregistration_path", "content_change_after_merge"),
    }
    for section, keys in fixed_keys.items():
        _keys(data[section], keys, section, errors)

    nested_keys = (
        (data["representations"]["EQUITY"], ("research_unit", "ids", "aggregate_return_series", "weighting_methods_prohibited"), "representations.EQUITY"),
        (data["representations"]["FUND_BROAD_MARKET"], ("research_unit", "ids", "combined_return_series"), "representations.FUND_BROAD_MARKET"),
        (data["representations"]["FUND_GLD_DEFENSIVE"], ("research_unit", "core_ids", "conditional_ids", "conditional_use", "peer_ranking", "final_vehicle_selection"), "representations.FUND_GLD_DEFENSIVE"),
        (data["representations"]["CRYPTO"], ("research_unit", "ids", "composites_prohibited"), "representations.CRYPTO"),
        (data["data_gate"]["GLOBAL_STUDY_INTEGRITY"], ("failure_effect", "gates"), "data_gate.GLOBAL_STUDY_INTEGRITY"),
        (data["data_gate"]["CELL_DATA_ELIGIBILITY"], ("failure_effect", "gates", "propagation"), "data_gate.CELL_DATA_ELIGIBILITY"),
        (data["data_gate"]["integrity_rules"], ("no_lookahead", "no_interpolation", "no_forward_fill_prices", "no_zero_return_standins", "no_silent_universe_reduction", "no_unregistered_substitute"), "data_gate.integrity_rules"),
        (data["data_gate"]["gld_conditional_peer_gate"], ("required", "requirements", "failure_state"), "data_gate.gld_conditional_peer_gate"),
        (data["data_gate"]["crypto_gate"], ("utc_normalization", "expected_calendar", "duplicate_timestamps_allowed", "missing_days_parameter_id", "maximum_contiguous_gap_parameter_id", "ohlc_rules", "pagination_completeness", "interpolation", "forward_fill", "fabricated_pre_inception", "undisclosed_alternate_source_stitching", "known_sol_gap_rule"), "data_gate.crypto_gate"),
        (data["result_reduction"]["canonical_states"], ("observation", "family", "directional", "point_evidence"), "result_reduction.canonical_states"),
        (data["result_reduction"]["observation_rule"], ("HIGHER", "LOWER", "missing_state"), "result_reduction.observation_rule"),
        (data["result_reduction"]["metric_window_reduction"], ("ordered_precedence", "NOT_APPLICABLE", "zero_applicable_observations", "mandatory_window_unavailable", "conditional_window_missing_data_or_quality_failure"), "result_reduction.metric_window_reduction"),
        (data["result_reduction"]["family_metric_reduction"], ("ordered_precedence", "mandatory_voting_metric_unavailable", "conditional_voting_metric_not_applicable_for_all_lawful_representations", "zero_applicable_voting_metrics", "non_voting_metrics"), "result_reduction.family_metric_reduction"),
        (data["result_reduction"]["representation_reduction"], ("FUND_BROAD_MARKET", "CRYPTO", "FUND_GLD_DEFENSIVE", "EQUITY"), "result_reduction.representation_reduction"),
        (data["result_reduction"]["monotonicity"], ("designated_metrics", "rule", "tolerance", "failure_effect"), "result_reduction.monotonicity"),
        (data["result_reduction"]["directional_policy_review"], ("mandatory_veto_families", "minimum_improvement_parameter_id", "policy_review_required", "center_not_rejected", "unable_to_determine", "no_metric_weighting", "representation_conflict_veto"), "result_reduction.directional_policy_review"),
    )
    for value, keys, where in nested_keys:
        _keys(value, keys, where, errors)

    for family in FAMILIES:
        _keys(data["scenario_magnitudes"]["values_pct"][family], SCENARIOS, f"scenario_magnitudes.values_pct.{family}", errors)
    for record in data["consequential_parameter_registry"]["parameters"]:
        _keys(record, PARAMETER_KEYS, f"parameter[{record.get('parameter_id')}]", errors)
    for record in data["consequential_parameter_registry"]["derived_identities"]:
        _keys(record, ("identity_id", "value", "derivation", "num_0001_class"), f"derived_identity[{record.get('identity_id')}]", errors)
    for window in data["scenario_windows"]["windows"]:
        _keys(window, ("id", "class", "voting_role", "start", "end", "start_by_family", "rule", "criterion"), f"window[{window.get('id')}]", errors)
    for metric in data["metric_families"]["metrics"]:
        _keys(metric, METRIC_KEYS, f"metric[{metric.get('metric_id')}]", errors)
    for row in data["result_reduction"]["total_state_table"]:
        _keys(row, ("lower", "higher", "result", "review_direction"), "result_reduction.total_state_table row", errors)
    for row in data["result_reduction"]["point_state_table"]:
        _keys(row, ("lower", "higher", "point_target_assessment", "method_review_direction"), "result_reduction.point_state_table row", errors)

    # The accepted provider/rule surfaces are exact, not open extension points.
    _closed(data["fallback_order"], {
        "equities_etfs": ["ALPACA_MARKET_DATA", "YAHOO_FINANCE_CHART", "ABSTAIN"],
        "crypto": ["ALPACA_CRYPTO", "COINBASE_EXCHANGE", "ABSTAIN"],
        "comparator": ["FRED_DFF", "ABSTAIN_OPPORTUNITY_COST_CELLS"],
        "corporate_actions": ["ALPACA_CORPORATE_ACTIONS", "SEC_EDGAR_OR_ISSUER", "ABSTAIN_AFFECTED_CELLS"],
        "provider_change_after_result_inspection": "PROHIBITED",
        "fallback_retry_before_registered_execution": "PERMITTED_AND_LOGGED",
    }, "fallback_order", errors)
    _closed(data["data_sources"], {
        "equities_etfs": {
            "primary": {"provider": "ALPACA_MARKET_DATA", "endpoint": "https://data.alpaca.markets/v2/stocks/{symbol}/bars", "parameters": "timeframe=1Day&adjustment=split&feed=sip&limit=10000", "return_input": "SPLIT_ADJUSTED_NON_TOTAL_RETURN_OHLC", "commit_rule": "COMMIT_IF_LICENSE_AND_SIZE_ALLOW_OTHERWISE_QUARANTINE_WITH_HASH"},
            "fallback": {"provider": "YAHOO_FINANCE_CHART", "endpoint": "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}", "parameters": "interval=1d&events=div%2Csplits%2CcapitalGains", "return_input": "SPLIT_ADJUSTED_NON_TOTAL_RETURN_CLOSE_PLUS_EXPLICIT_ACTIONS", "disposition": "QUARANTINE_NOT_COMMITTED", "whole_path_rule": "ONE_PROVIDER_PER_REPRESENTATION_WINDOW_NO_UNDISCLOSED_STITCHING"}},
        "crypto": {
            "primary": {"provider": "ALPACA_CRYPTO", "endpoint": "https://data.alpaca.markets/v1beta3/crypto/us/bars", "parameters": "symbols={symbol}/USD&timeframe=1Day&limit=10000", "market": "SPOT", "commit_rule": "COMMIT_IF_LICENSE_AND_SIZE_ALLOW_OTHERWISE_QUARANTINE_WITH_HASH"},
            "fallback": {"provider": "COINBASE_EXCHANGE", "endpoint": "https://api.exchange.coinbase.com/products/{product}-USD/candles", "parameters": "granularity=86400&start={start}&end={end}", "market": "SPOT", "disposition": "QUARANTINE_NOT_COMMITTED", "whole_path_rule": "ONE_PROVIDER_PER_REPRESENTATION_WINDOW_NO_UNDISCLOSED_STITCHING"}},
        "comparator": {"provider": "FRED", "series": "DFF", "endpoint": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF", "disposition": "COMMIT_OFFICIAL_PUBLIC_DOMAIN_SOURCE_OR_HASH_PINNED_RECEIPT", "analytical_fallback": "NONE"},
        "corporate_actions": {"primary": {"provider": "ALPACA_CORPORATE_ACTIONS", "endpoint": "https://data.alpaca.markets/v1/corporate-actions", "types": ["cash_dividend", "stock_dividend", "split", "spin_off", "merger"]}, "identity_resolution": {"providers": ["SEC_EDGAR", "PRIMARY_ISSUER_INVESTOR_RELATIONS"], "use": "LEGAL_ENTITY_AND_ACTION_RESOLUTION_ONLY"}},
        "secondary_reconciliation": {"providers": ["YAHOO_FINANCE_ADJCLOSE", "ISSUER_FILINGS", "COINBASE_EXCHANGE_OR_ALPACA_OPPOSITE_SOURCE"], "use": "RECONCILIATION_ONLY_NOT_SILENT_INPUT_SUBSTITUTION"},
    }, "data_sources", errors)


def _validate_authority(data: dict[str, Any], errors: list[str]) -> None:
    _exact(data["schema_version"], "2.0", "schema_version", errors)
    _exact(data["study_id"], "RISK-0001", "study_id", errors)
    _closed(data["authority"], {
        "decision": "RISK-0001", "architecture": "XASSET-0019", "cohort": "LEVEL2-0001", "numeric_provenance": "NUM-0001", "lifecycle": "OPS-0009_LANE_G", "execution_authority": "ONE_LATER_IMPLEMENTATION_RESULTS_PR_ONLY", "charter_pr_data_acquisition": "PROHIBITED", "charter_pr_study_execution": "PROHIBITED", "policy_adoption": "PROHIBITED", "computational_authority": "THIS_STRUCTURED_PREREGISTRATION_ONLY", "narrative_fields_authoritative": False, "question_id": "HISTORICAL_PROVISIONAL_SCENARIO_PLAUSIBILITY_CHALLENGE",
    }, "authority", errors)
    cohort = data["frozen_cohort"]
    _exact(tuple(cohort["equity_ids"]), EQUITIES, "frozen_cohort.equity_ids", errors)
    _exact(tuple(cohort["broad_market_ids"]), BROAD, "frozen_cohort.broad_market_ids", errors)
    _exact(tuple(cohort["defensive_core_ids"]), ("GLD",), "frozen_cohort.defensive_core_ids", errors)
    _exact(tuple(cohort["crypto_ids"]), CRYPTO, "frozen_cohort.crypto_ids", errors)
    _exact(cohort["expected_core_count"], 34, "frozen_cohort.expected_core_count", errors)
    _exact(cohort["equity_count"], len(EQUITIES), "frozen_cohort.equity_count", errors)
    _exact((cohort["source"], cohort["scope"], cohort["final_membership_authority"], cohort["level2_sizing_authority"]), ("governance/evidence/LEVEL2-0001/RESEARCH_COHORT_FREEZE.yaml", "RESEARCH_ONLY_NOT_FINAL_MEMBERSHIP", "PROHIBITED", "PROHIBITED"), "frozen cohort authority", errors)
    reps = data["representations"]
    _exact(tuple(reps["family_order"]), FAMILIES, "representations.family_order", errors)
    _exact(tuple(reps["EQUITY"]["ids"]), EQUITIES, "representations.EQUITY.ids", errors)
    _exact(tuple(reps["FUND_BROAD_MARKET"]["ids"]), BROAD, "representations.FUND_BROAD_MARKET.ids", errors)
    _exact(tuple(reps["FUND_GLD_DEFENSIVE"]["core_ids"] + reps["FUND_GLD_DEFENSIVE"]["conditional_ids"]), GOLD, "representations gold ids", errors)
    _exact(tuple(reps["CRYPTO"]["ids"]), CRYPTO, "representations.CRYPTO.ids", errors)
    _exact(tuple(reps["excluded"]), ("CASH", "RESERVE", "cash_reserve", "debt_reduction", "residual", "unassigned_capital", "margin", "leverage"), "representations.excluded", errors)
    _exact(reps["EQUITY"]["aggregate_return_series"], "PROHIBITED", "equity aggregate path", errors)
    _exact(reps["FUND_BROAD_MARKET"]["combined_return_series"], "PROHIBITED", "broad-market blend", errors)
    _closed(reps["EQUITY"], {"research_unit": "CONSTITUENT_DIAGNOSTICS_ONLY", "ids": list(EQUITIES), "aggregate_return_series": "PROHIBITED", "weighting_methods_prohibited": ["EQUAL_WEIGHT", "MARKET_CAP_WEIGHT", "CURRENT_WEIGHT", "SYNTHETIC_REPRESENTATIVE_PATH"]}, "representations.EQUITY", errors)
    _closed(reps["FUND_BROAD_MARKET"], {"research_unit": "SEPARATE_REPRESENTATIONS", "ids": list(BROAD), "combined_return_series": "PROHIBITED"}, "representations.FUND_BROAD_MARKET", errors)
    _closed(reps["FUND_GLD_DEFENSIVE"], {"research_unit": "CORE_PLUS_CONDITIONAL_SENSITIVITY", "core_ids": ["GLD"], "conditional_ids": ["IAU", "SGOL", "GLDM"], "conditional_use": "REPRESENTATION_SENSITIVITY_ONLY", "peer_ranking": "PROHIBITED", "final_vehicle_selection": "PROHIBITED"}, "representations.FUND_GLD_DEFENSIVE", errors)
    _closed(reps["CRYPTO"], {"research_unit": "SEPARATE_REPRESENTATIONS", "ids": list(CRYPTO), "composites_prohibited": ["EQUAL_WEIGHT", "MARKET_CAP", "CONVICTION", "CANONICAL"]}, "representations.CRYPTO", errors)


def _validate_scenarios_registry(data: dict[str, Any], errors: list[str]) -> None:
    refs = {"EQUITY": "18.67", "FUND_BROAD_MARKET": "14.67", "FUND_GLD_DEFENSIVE": "16.67", "CRYPTO": "16.67"}
    _exact(data["historical_reference_scenarios"]["classification"], "historical_provisional_reference", "historical classification", errors)
    _exact(tuple(data["historical_reference_scenarios"]["semantics"]), ("HISTORICAL", "COMPUTATIONALLY_DERIVED_UNDER_SUPERSEDED_MECHANICS", "PROVISIONAL", "ECONOMICALLY_UNVALIDATED", "NOT_ADOPTED", "NOT_BASELINE_POLICY", "NOT_A_TARGET", "NOT_AN_OPTIMIZATION_ANCHOR", "NO_RESIDUAL_ASSIGNMENT"), "historical semantics", errors)
    _exact(data["historical_reference_scenarios"]["values_pct"], refs, "historical values", errors)
    _exact(tuple(data["scenario_states"]), SCENARIOS, "scenario_states", errors)
    provenance = data["scenario_provenance"]
    _exact(provenance["method"], "SYMMETRIC_RELATIVE_PERTURBATION", "scenario provenance method", errors)
    _exact(provenance["relative_perturbation_parameter_id"], "RELATIVE_PERTURBATION", "scenario provenance parameter", errors)
    _exact(provenance["formula"], {"LOWER": "REFERENCE_TIMES_ONE_MINUS_PERTURBATION", "HISTORICAL_REFERENCE": "REFERENCE_UNCHANGED", "HIGHER": "REFERENCE_TIMES_ONE_PLUS_PERTURBATION"}, "scenario formula", errors)
    _exact((provenance["rounding"], provenance["lapse"], provenance["reuse"]), ("ROUND_HALF_UP_TO_TWO_DECIMAL_PERCENTAGE_POINTS", "AUTOMATIC_ON_AUTHORIZED_STUDY_COMPLETION", "REQUIRES_NEW_GOVERNANCE_AUTHORITY"), "scenario governance", errors)
    for field in ("calibrated", "evidence_bounded", "optimized", "inherited_from_xasset_0016_r2_r3"):
        _exact(provenance[field], False, f"scenario_provenance.{field}", errors)
    registry = data["consequential_parameter_registry"]
    _exact(tuple(registry["record_keys"]), PARAMETER_KEYS, "parameter record keys", errors)
    records = registry["parameters"]
    _exact(tuple(r["parameter_id"] for r in records), tuple(PARAMETER_SPECS), "parameter ids/order", errors)
    for record in records:
        pid = record["parameter_id"]
        value, unit, classification = PARAMETER_SPECS[pid]
        _exact(record["value"], value, f"{pid}.value", errors)
        _exact(record["unit"], unit, f"{pid}.unit", errors)
        _exact(record["num_0001_class"], classification, f"{pid}.num_0001_class", errors)
        _exact(record["contextual_class"], "RESEARCH_ASSUMPTION", f"{pid}.contextual_class", errors)
        _exact(record["valid_for_study_id"], "RISK-0001", f"{pid}.valid_for_study_id", errors)
        _exact(record["lapse_condition"], "AUTHORIZED_STUDY_COMPLETION", f"{pid}.lapse_condition", errors)
        _exact(record["calibrated"], False, f"{pid}.calibrated", errors)
        _exact(record["evidence_bounded"], False, f"{pid}.evidence_bounded", errors)
        basis, evidence, scope, reuse = PARAMETER_GOVERNANCE[pid]
        _exact((record["selection_basis"], record["evidence_status"], record["binding_scope"], record["reuse_rule"]), (basis, evidence, scope, reuse), f"{pid}.governance", errors)
        _exact(record["canonical_source"], f"consequential_parameter_registry.{pid}", f"{pid}.canonical_source", errors)
    perturbation = Decimal(str(_param(data, "RELATIVE_PERTURBATION")))
    for family, ref_text in refs.items():
        ref = Decimal(ref_text)
        expected = {
            "LOWER": (ref * (Decimal(1) - perturbation)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "HISTORICAL_REFERENCE": ref,
            "HIGHER": (ref * (Decimal(1) + perturbation)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        }
        actual = data["scenario_magnitudes"]["values_pct"][family]
        for state in SCENARIOS:
            if not isinstance(actual[state], str) or not re.fullmatch(r"\d+\.\d{2}", actual[state]):
                errors.append(f"scenario_magnitudes.{family}.{state}: exact two-decimal string required")
            else:
                _exact(Decimal(actual[state]), expected[state], f"scenario_magnitudes.{family}.{state} derived", errors)
    _exact(tuple(data["scenario_magnitudes"]["values_pct"]), FAMILIES, "scenario magnitude families/order", errors)
    _exact((data["scenario_magnitudes"]["unit"], data["scenario_magnitudes"]["freeze_status"], data["scenario_magnitudes"]["portfolio_reconciliation"], data["scenario_magnitudes"]["residual_assignment"]), ("PERCENT_OF_UNSPECIFIED_ASSET_STATE_EXPOSURE", "IMMUTABLE_AFTER_CHARTER_MERGE", "NOT_PERFORMED", "PROHIBITED"), "scenario magnitude authority", errors)
    identities = tuple((r["identity_id"], r["value"], r["derivation"], r["num_0001_class"]) for r in registry["derived_identities"])
    _exact(identities, (
        ("REPRESENTATION_COUNT", 37, "27_PLUS_3_PLUS_4_PLUS_3", "MATHEMATICALLY_DERIVED"),
        ("SCENARIO_COUNT", 3, "LENGTH_OF_SCENARIO_STATES", "MATHEMATICALLY_DERIVED"),
        ("WINDOW_COUNT", 7, "LENGTH_OF_SCENARIO_WINDOWS", "MATHEMATICALLY_DERIVED"),
        ("MAXIMUM_REGISTERED_CELLS", 777, "REPRESENTATION_COUNT_TIMES_SCENARIO_COUNT_TIMES_WINDOW_COUNT", "MATHEMATICALLY_DERIVED"),
    ), "derived identities", errors)


def _validate_windows_metrics_results(data: dict[str, Any], errors: list[str]) -> None:
    windows = data["scenario_windows"]
    _exact(windows["count"], len(windows["windows"]), "scenario_windows.count derived", errors)
    _exact(tuple((w["id"], w["start"], w["end"]) for w in windows["windows"]), WINDOW_DATES, "window ids/dates/order", errors)
    _exact(tuple(w["voting_role"] for w in windows["windows"]), ("MANDATORY_VOTING", "MANDATORY_VOTING", "CONDITIONAL_VOTING", "CONDITIONAL_VOTING", "CONDITIONAL_VOTING", "CONDITIONAL_VOTING", "CONDITIONAL_VOTING"), "window voting roles", errors)
    _exact(windows["windows"][1]["start_by_family"], {"EQUITY": "2024-04-02", "FUND_BROAD_MARKET": "2007-07-20", "FUND_GLD_DEFENSIVE": "2018-06-26", "CRYPTO": "2021-06-01"}, "family common starts", errors)
    _closed(windows, {"count": 7, "evaluation_end": "2026-07-31", "windows": [
        {"id": "ASSET_AVAILABLE_HISTORY", "class": "ASSET_AVAILABLE", "voting_role": "MANDATORY_VOTING", "start": "2004-11-18", "end": "2026-07-31", "start_by_family": None, "rule": "INTERSECT_WITH_LAWFUL_LISTING_INCEPTION_AND_VALIDATED_COVERAGE", "criterion": "GLD_FIRST_TRADING_DATE_AS_CROSS_FAMILY_MODERN_HISTORY_FLOOR"},
        {"id": "FAMILY_COMMON_OVERLAP", "class": "FAMILY_COMMON", "voting_role": "MANDATORY_VOTING", "start": None, "end": "2026-07-31", "start_by_family": {"EQUITY": "2024-04-02", "FUND_BROAD_MARKET": "2007-07-20", "FUND_GLD_DEFENSIVE": "2018-06-26", "CRYPTO": "2021-06-01"}, "rule": "EXACT_FAMILY_COMMON_START", "criterion": "LATEST_KNOWN_LAWFUL_CORE_OR_CONDITIONAL_INCEPTION_WITHIN_FAMILY"},
        {"id": "GFC_2008", "class": "FIXED_STRESS", "voting_role": "CONDITIONAL_VOTING", "start": "2007-12-01", "end": "2009-06-30", "start_by_family": None, "rule": "FIXED_EVENT_WINDOW", "criterion": "NBER_RECESSION_MONTH_BOUNDARIES_NOT_ASSET_PEAK_TROUGH"},
        {"id": "Q4_2018", "class": "FIXED_STRESS", "voting_role": "CONDITIONAL_VOTING", "start": "2018-10-01", "end": "2018-12-31", "start_by_family": None, "rule": "FIXED_EVENT_WINDOW", "criterion": "CALENDAR_QUARTER"},
        {"id": "COVID_2020", "class": "FIXED_STRESS", "voting_role": "CONDITIONAL_VOTING", "start": "2020-02-01", "end": "2020-04-30", "start_by_family": None, "rule": "FIXED_EVENT_WINDOW", "criterion": "PREDECLARED_PUBLIC_HEALTH_SHOCK_WINDOW_NOT_ASSET_PEAK_TROUGH"},
        {"id": "RATE_INFLATION_2022", "class": "FIXED_STRESS", "voting_role": "CONDITIONAL_VOTING", "start": "2022-01-01", "end": "2022-12-31", "start_by_family": None, "rule": "FIXED_EVENT_WINDOW", "criterion": "CALENDAR_YEAR_RATE_AND_INFLATION_SHOCK"},
        {"id": "CRYPTO_STRESS_2022", "class": "FIXED_STRESS", "voting_role": "CONDITIONAL_VOTING", "start": "2022-05-01", "end": "2022-12-31", "start_by_family": None, "rule": "FIXED_EVENT_WINDOW", "criterion": "PREDECLARED_TERRA_CELSIUS_FTX_EVENT_INTERVAL_NOT_ASSET_PEAK_TROUGH"},
    ], "asset_specific_peak_trough_selection": "PROHIBITED"}, "scenario windows", errors)
    _exact(tuple(data["missingness_states"]["vocabulary"]), MISSINGNESS, "missingness vocabulary", errors)
    _exact(data["missingness_states"]["zero_return_standin"], "PROHIBITED", "missingness zero stand-in", errors)
    _exact(tuple(data["missingness_states"]["result_table_requirements"]), ("ELIGIBLE_COUNT", "EXPECTED_FROZEN_COUNT", "MISSING_NAMES", "PRE_INCEPTION_NAMES", "CENSORED_RECOVERIES", "SELECTION_CONDITIONED_COHORT_WARNING", "CORPORATE_ACTION_TRUNCATIONS"), "result table requirements", errors)
    metrics = data["metric_families"]
    _exact(tuple(metrics["family_order"]), METRIC_FAMILY_ORDER, "metric family order", errors)
    _exact(tuple(metrics["voting_families"]), VOTING_FAMILIES, "voting families", errors)
    _exact(tuple(metrics["non_voting_families"]), METRIC_FAMILY_ORDER[3:], "non-voting families", errors)
    records = metrics["metrics"]
    _exact(tuple(r["metric_id"] for r in records), tuple(METRIC_SPECS), "metric ids/order", errors)
    for metric in records:
        mid = metric["metric_id"]
        family, direction, materiality, equivalence, voting = METRIC_SPECS[mid]
        _exact((metric["family"], metric["direction_of_preference"], metric["materiality_parameter_id"], metric["equivalence_parameter_id"], metric["voting_status"]), (family, direction, materiality, equivalence, voting), f"metric[{mid}] classification", errors)
        formula, unit, units, windows, missing = METRIC_DETAILS[mid]
        _exact((metric["formula"], metric["unit"], tuple(metric["applicable_research_units"]), tuple(metric["applicable_windows"]), metric["missing_result_behavior"]), (formula, unit, units, windows, missing), f"metric[{mid}] definition", errors)
        if materiality is not None and materiality not in PARAMETER_SPECS:
            errors.append(f"metric[{mid}]: undefined materiality parameter {materiality}")
        if equivalence is not None and equivalence not in PARAMETER_SPECS:
            errors.append(f"metric[{mid}]: undefined equivalence parameter {equivalence}")
    rr = data["result_reduction"]
    _exact(tuple(rr["canonical_states"]["observation"]), OBSERVATION_STATES, "observation states", errors)
    _exact(tuple(rr["canonical_states"]["family"]), FAMILY_STATES, "family states", errors)
    _exact(tuple(rr["canonical_states"]["directional"]), DIRECTIONAL_STATES, "directional states", errors)
    _exact(tuple(rr["canonical_states"]["point_evidence"]), POINT_EVIDENCE_STATES, "point evidence states", errors)
    _exact(tuple(rr["directional_policy_review"]["mandatory_veto_families"]), VOTING_FAMILIES, "mandatory veto families", errors)
    _exact(rr["directional_policy_review"]["minimum_improvement_parameter_id"], "MINIMUM_IMPROVEMENT_FAMILIES", "minimum improvement parameter", errors)
    _exact(rr["directional_policy_review"]["representation_conflict_veto"], True, "representation conflict veto", errors)
    _closed(rr["metric_window_reduction"], {"ordered_precedence": ["WORSENS", "UNAVAILABLE", "IMPROVES", "EQUIVALENT"], "NOT_APPLICABLE": "EXCLUDED_FROM_REDUCTION", "zero_applicable_observations": "UNAVAILABLE", "mandatory_window_unavailable": "UNAVAILABLE", "conditional_window_missing_data_or_quality_failure": "UNAVAILABLE"}, "metric/window reduction", errors)
    _closed(rr["family_metric_reduction"], {"ordered_precedence": ["WORSENS", "UNAVAILABLE", "IMPROVES", "EQUIVALENT"], "mandatory_voting_metric_unavailable": "UNAVAILABLE", "conditional_voting_metric_not_applicable_for_all_lawful_representations": "EXCLUDED", "zero_applicable_voting_metrics": "UNAVAILABLE", "non_voting_metrics": "NEVER_CHANGE_FAMILY_STATE"}, "family metric reduction", errors)
    _closed(rr["representation_reduction"], {
        "FUND_BROAD_MARKET": {"mandatory_representations": ["SPY", "VEA", "VWO"], "unavailable_rule": "ANY_UNAVAILABLE_MAKES_FAMILY_UNAVAILABLE", "agreement_rule": "ALL_MANDATORY_STATES_IDENTICAL", "disagreement_rule": "CONFLICT"},
        "CRYPTO": {"mandatory_representations": ["BTC", "ETH", "SOL"], "unavailable_rule": "ANY_UNAVAILABLE_MAKES_FAMILY_UNAVAILABLE", "agreement_rule": "ALL_MANDATORY_STATES_IDENTICAL", "disagreement_rule": "CONFLICT"},
        "FUND_GLD_DEFENSIVE": {"core_representation": "GLD", "core_unavailable_rule": "FAMILY_UNAVAILABLE", "conditional_representations": ["IAU", "SGOL", "GLDM"], "conditional_failed_gate_rule": "EXCLUDE_NOT_VETO", "admitted_peer_unavailable_rule": "FAMILY_UNAVAILABLE", "agreement_rule": "EVERY_ADMITTED_PEER_MATCHES_GLD", "disagreement_rule": "CONFLICT"},
        "EQUITY": {"minimum_eligible_parameter_id": "EQUITY_MINIMUM_ELIGIBLE", "breadth_parameter_id": "EQUITY_DIRECTIONAL_BREADTH", "required_median_state": "SAME_AS_REDUCED_STATE", "leave_one_out_rule": "EVERY_OMISSION_REMAINS_SAME_STATE", "below_minimum_rule": "UNAVAILABLE", "failed_breadth_median_or_leave_one_out_rule": "CONFLICT", "aggregate_path": "PROHIBITED"},
    }, "representation reduction", errors)
    _closed(rr["directional_policy_review"], {"mandatory_veto_families": ["PATH_RISK", "RECOVERY", "OPPORTUNITY_COST"], "minimum_improvement_parameter_id": "MINIMUM_IMPROVEMENT_FAMILIES", "policy_review_required": "NO_WORSENS_NO_UNAVAILABLE_NO_CONFLICT_AND_MINIMUM_DISTINCT_IMPROVING_FAMILIES_MET", "center_not_rejected": "ALL_MANDATORY_FAMILIES_AVAILABLE_NOT_MIXED_IMPROVES_AND_WORSENS_AND_POLICY_REVIEW_RULE_NOT_MET", "unable_to_determine": "ANY_MANDATORY_FAMILY_UNAVAILABLE_OR_CONFLICT_OR_MONOTONICITY_FAILURE_OR_MIXED_IMPROVES_AND_WORSENS", "no_metric_weighting": True, "representation_conflict_veto": True}, "directional policy review", errors)
    _closed(rr["point_evidence_rule"], {"DISPLACES_REFERENCE": "DIRECTIONAL_STATE_POLICY_REVIEW_REQUIRED", "ADJACENT_MATERIALLY_WORSE": "DIRECTIONAL_STATE_CENTER_NOT_REJECTED_AND_AT_LEAST_MINIMUM_IMPROVEMENT_FAMILIES_COUNT_WORSENS_AND_ZERO_IMPROVES", "NOT_DISTINGUISHED": "DIRECTIONAL_STATE_CENTER_NOT_REJECTED_AND_ADJACENT_MATERIALLY_WORSE_RULE_NOT_MET", "UNAVAILABLE": "DIRECTIONAL_STATE_UNABLE_TO_DETERMINE"}, "point evidence rule", errors)
    actual_table = tuple((r["lower"], r["higher"], r["result"], r["review_direction"]) for r in rr["total_state_table"])
    _exact(actual_table, TOTAL_STATE_TABLE, "total state table", errors)
    actual_point_table = tuple((r["lower"], r["higher"], r["point_target_assessment"], r["method_review_direction"]) for r in rr["point_state_table"])
    _exact(actual_point_table, POINT_STATE_TABLE, "point state table", errors)
    _closed(rr["observation_rule"], {"HIGHER": {"IMPROVES": "CANDIDATE_MINUS_REFERENCE_GREATER_THAN_TOLERANCE", "EQUIVALENT": "ABS_CANDIDATE_MINUS_REFERENCE_LESS_THAN_OR_EQUAL_TO_TOLERANCE", "WORSENS": "CANDIDATE_MINUS_REFERENCE_LESS_THAN_NEGATIVE_TOLERANCE"}, "LOWER": {"IMPROVES": "REFERENCE_MINUS_CANDIDATE_GREATER_THAN_TOLERANCE", "EQUIVALENT": "ABS_CANDIDATE_MINUS_REFERENCE_LESS_THAN_OR_EQUAL_TO_TOLERANCE", "WORSENS": "REFERENCE_MINUS_CANDIDATE_LESS_THAN_NEGATIVE_TOLERANCE"}, "missing_state": "UNAVAILABLE_UNLESS_CONDITIONAL_WINDOW_IS_NOT_APPLICABLE_PRE_INCEPTION"}, "observation rule", errors)
    _closed(rr["monotonicity"], {"designated_metrics": ["EXPOSURE_SCALED_DRAWDOWN_LOSS", "EXPOSURE_SCALED_STRESS_LOSS", "EXPOSURE_SCALED_UNDERWATER_BURDEN", "EXPOSURE_SCALED_EXCESS_CONTRIBUTION"], "rule": "RECOMPUTE_EACH_VALUE_FROM_RAW_METRIC_AND_REGISTERED_EXPOSURE_WITH_DECIMAL_ARITHMETIC_AND_VERIFY_FORMULA_IDENTITY", "tolerance": "EXACT_TO_SIX_DECIMAL_PLACES", "failure_effect": "DIRECTIONAL_UNABLE_TO_DETERMINE"}, "monotonicity", errors)
    _exact(metrics["composite_score"], "PROHIBITED", "composite score", errors)


def _validate_gates_rules_inventory(data: dict[str, Any], errors: list[str]) -> None:
    gate = data["data_gate"]
    _exact(tuple(gate["stage_order"]), ("GLOBAL_STUDY_INTEGRITY", "CELL_DATA_ELIGIBILITY"), "data gate stage order", errors)
    _exact(gate["GLOBAL_STUDY_INTEGRITY"]["failure_effect"], "GLOBAL_HALT_ZERO_CELLS_EXECUTE", "global gate effect", errors)
    _exact(tuple(gate["GLOBAL_STUDY_INTEGRITY"]["gates"]), ("CHARTER_PROTOCOL_PREREG_HASH_IDENTITY", "CLOSED_SCHEMA_VALIDATION", "TRIAL_INVENTORY_INTEGRITY", "RUNNER_AND_CONFIG_IDENTITY", "SOURCE_HIERARCHY_INTEGRITY", "GLOBAL_CODE_AND_VERSION_INTEGRITY", "STUDY_WIDE_PROVENANCE_REGISTRY_COMPLETE", "COMPLETE_PREEXECUTION_ELIGIBILITY_MATRIX"), "global gates", errors)
    _exact(gate["CELL_DATA_ELIGIBILITY"]["failure_effect"], "DEPENDENT_REGISTERED_CELLS_INELIGIBLE_ONLY", "cell gate effect", errors)
    _exact(tuple(gate["CELL_DATA_ELIGIBILITY"]["gates"]), ("SOURCE_ACQUISITION_AND_RECEIPTS", "COVERAGE_AND_GAP_VALIDATION", "IDENTITY_AND_CORPORATE_ACTION_RESOLUTION", "TOTAL_RETURN_CONSTRUCTION_VALIDATION", "REPRESENTATION_WINDOW_QUALITY", "COMPARATOR_WINDOW_AVAILABILITY"), "cell gates", errors)
    _exact(gate["CELL_DATA_ELIGIBILITY"]["propagation"], {"SOL_GAP": "INTERSECTING_SOL_CELLS_INELIGIBLE", "VEA_ACQUISITION_FAILURE": "ALL_VEA_CELLS_INELIGIBLE", "CEG_ACTION_UNRESOLVED": "INTERSECTING_CEG_CELLS_INELIGIBLE", "DFF_MISSING_REQUIRED_DAY": "AFFECTED_OPPORTUNITY_COST_METRICS_UNAVAILABLE", "CONDITIONAL_GOLD_PEER_GATE_FAILURE": "PEER_EXCLUDED_AS_CONDITIONAL_ASSET_NOT_ACQUIRED", "MANDATORY_REPRESENTATION_UNAVAILABLE": "FAMILY_STATE_UNAVAILABLE", "REPRESENTATION_CONFLICT": "STUDY_RESULT_UNABLE_TO_DETERMINE"}, "cell gate propagation", errors)
    _exact(gate["preexecution_freeze"], "ALL_ACQUISITION_VALIDATION_AND_ELIGIBILITY_STATES_FROZEN_BEFORE_FIRST_CELL", "preexecution freeze", errors)
    _exact(tuple(gate["required_receipts"]), ("REQUEST_URL_WITH_SECRETS_REDACTED", "REQUEST_TIMESTAMP_UTC", "RESPONSE_STATUS", "PAGE_OR_CURSOR_ID", "NEXT_PAGE_OR_TERMINAL_MARKER", "RAW_SHA256", "TRANSFORMED_SHA256", "COVERAGE_START_END", "EXPECTED_AND_OBSERVED_COUNTS", "GAP_INVENTORY", "IDENTITY_LINEAGE", "CORPORATE_ACTION_DISPOSITION", "PROVIDER_AND_ENDPOINT", "LICENSE_AND_COMMIT_OR_QUARANTINE_DISPOSITION"), "required receipts", errors)
    _exact(gate["integrity_rules"], {"no_lookahead": True, "no_interpolation": True, "no_forward_fill_prices": True, "no_zero_return_standins": True, "no_silent_universe_reduction": True, "no_unregistered_substitute": True}, "data integrity rules", errors)
    _exact(gate["crypto_gate"]["missing_days_parameter_id"], "CRYPTO_MISSING_DAYS_ALLOWED", "crypto missing parameter", errors)
    _exact(gate["crypto_gate"]["maximum_contiguous_gap_parameter_id"], "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS", "crypto gap parameter", errors)
    _exact(gate["crypto_gate"]["interpolation"], "PROHIBITED", "crypto interpolation", errors)
    _exact(gate["crypto_gate"]["forward_fill"], "PROHIBITED", "crypto forward fill", errors)
    _exact(gate["crypto_gate"]["fabricated_pre_inception"], "PROHIBITED", "crypto pre-inception fabrication", errors)
    _exact(gate["crypto_gate"]["undisclosed_alternate_source_stitching"], "PROHIBITED", "crypto source stitching", errors)
    _exact(gate["crypto_gate"]["known_sol_gap_rule"], "REINVENTORY_418_DAY_AGGREGATE_GAP_AND_MARK_EVERY_INTERSECTING_WINDOW_INELIGIBLE", "known SOL rule", errors)
    _closed(gate["crypto_gate"], {"utc_normalization": "REQUIRED", "expected_calendar": "EVERY_UTC_DAY_IN_REGISTERED_WINDOW", "duplicate_timestamps_allowed": 0, "missing_days_parameter_id": "CRYPTO_MISSING_DAYS_ALLOWED", "maximum_contiguous_gap_parameter_id": "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS", "ohlc_rules": ["FINITE", "POSITIVE", "LOW_LE_MIN_OPEN_CLOSE", "HIGH_GE_MAX_OPEN_CLOSE", "HIGH_GE_LOW"], "pagination_completeness": "REQUIRED", "interpolation": "PROHIBITED", "forward_fill": "PROHIBITED", "fabricated_pre_inception": "PROHIBITED", "undisclosed_alternate_source_stitching": "PROHIBITED", "known_sol_gap_rule": "REINVENTORY_418_DAY_AGGREGATE_GAP_AND_MARK_EVERY_INTERSECTING_WINDOW_INELIGIBLE"}, "crypto gate", errors)
    _exact(gate["gld_conditional_peer_gate"], {"required": False, "requirements": ["COMPLETE_IDENTITY_AND_INCEPTION", "ZERO_UNRESOLVED_REQUIRED_SESSION_GAPS", "COMPLETE_DIVIDEND_SPLIT_ACTION_TREATMENT", "OVERLAP_TOTAL_RETURN_CORRELATION_AT_LEAST_GOLD_PARITY_CORRELATION_MIN", "OVERLAP_ANNUALIZED_RETURN_DIFFERENCE_AT_MOST_GOLD_PARITY_RETURN_MAX_PP", "OVERLAP_MAX_DRAWDOWN_DIFFERENCE_AT_MOST_GOLD_PARITY_DRAWDOWN_MAX_PP"], "failure_state": "CONDITIONAL_ASSET_NOT_ACQUIRED"}, "gold conditional peer gate", errors)
    _exact(_param(data, "CRYPTO_MISSING_DAYS_ALLOWED"), 0, "crypto missing days", errors)
    _exact(_param(data, "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS"), 0, "crypto max gap", errors)
    corp = data["corporate_action_rules"]
    _exact(corp["synthetic_predecessor_stitching"], "PROHIBITED", "predecessor stitching", errors)
    _exact(corp["unresolved_period"], "CORPORATE_ACTION_UNRESOLVED_AND_AFFECTED_CELL_INELIGIBLE", "unresolved action effect", errors)
    _exact(corp["known_boundaries"], {"CEG": "PRE_STANDALONE_HISTORY_UNAVAILABLE", "GEV": "PRE_SPIN_HISTORY_UNAVAILABLE", "RKLB": "PRE_2021_08_25_NOT_RKLB_HISTORY", "RTX": "PREDECESSOR_HISTORY_NOT_SILENTLY_STITCHED"}, "known corporate boundaries", errors)
    _closed(corp, {"equities_etfs_total_return_method": "SPLIT_ADJUSTED_PRICES_PLUS_EXPLICIT_DIVIDENDS_AND_ACTIONS", "total_return_series_combined_with_explicit_dividends": "PROHIBITED", "dividends": "GROSS_DECLARED_CASH_CREDITED_ON_EX_DATE_PRIMARY_PAY_DATE_SENSITIVITY_DISCLOSED", "splits": "APPLY_GOVERNED_SPLIT_FACTOR_AND_VERIFY_RETURN_CONTINUITY", "spin_offs": "REQUIRE_PRIMARY_IDENTITY_RATIO_AND_ENTITLEMENT_EVIDENCE_OR_MARK_UNRESOLVED", "ticker_changes": "CONTINUE_ONLY_WITH_PROVED_SAME_LEGAL_ENTITY_LINEAGE", "mergers": "CONTINUE_ONLY_THROUGH_EXPLICIT_GOVERNED_CONSIDERATION_AND_ENTITY_RULE", "legal_entity_continuity": "REQUIRED", "listing_inception": "NO_FABRICATED_PRE_INCEPTION_HISTORY", "synthetic_predecessor_stitching": "PROHIBITED", "known_boundaries": {"CEG": "PRE_STANDALONE_HISTORY_UNAVAILABLE", "GEV": "PRE_SPIN_HISTORY_UNAVAILABLE", "RKLB": "PRE_2021_08_25_NOT_RKLB_HISTORY", "RTX": "PREDECESSOR_HISTORY_NOT_SILENTLY_STITCHED"}, "unresolved_period": "CORPORATE_ACTION_UNRESOLVED_AND_AFFECTED_CELL_INELIGIBLE", "gold_fund_expense_treatment": "OBSERVED_FUND_PATH_ALREADY_INCLUDES_EXPENSE_DRAG_NO_SECOND_SUBTRACTION", "crypto_yield": "SPOT_ONLY_NO_STAKING_LENDING_OR_YIELD"}, "corporate action rules", errors)
    _closed(data["alignment_rules"], {"equity_etf_calendar": "XNYS_OFFICIAL_SESSIONS", "equity_etf_observation": "OFFICIAL_SESSION_CLOSE", "crypto_calendar": "UTC_24_7", "common_evaluation_timestamp": "EACH_XNYS_OFFICIAL_CLOSE_IN_AMERICA_NEW_YORK", "crypto_mapping": "LATEST_COMPLETED_UTC_DAILY_CLOSE_AT_OR_BEFORE_EVALUATION_TIMESTAMP", "weekend_crypto_rule": "COMPOUND_ALL_UNMAPPED_COMPLETED_UTC_DAILY_RETURNS_INTO_NEXT_XNYS_INTERVAL", "comparator_interval": "ACTUAL_CALENDAR_DAYS_BETWEEN_XNYS_EVALUATION_TIMESTAMPS", "future_observation_mapped_backward": "PROHIBITED", "missing_observation_as_zero": "PROHIBITED", "native_path_reporting": "RETAIN_NATIVE_SESSION_OR_UTC_DAY_SERIES_SEPARATELY"}, "alignment rules", errors)
    comparator = data["comparator"]
    _exact(comparator["series"], "DFF", "comparator series", errors)
    for field in ("strategic_cash", "residual", "funding_destination", "fifth_sleeve", "portfolio_policy"):
        _exact(comparator[field], False, f"comparator.{field}", errors)
    _exact(comparator["missing_rate_parameter_id"], "DFF_MISSING_DAYS_ALLOWED", "DFF missing parameter", errors)
    _closed(comparator, {"series": "DFF", "role": "ANALYTICAL_OPPORTUNITY_COST_ONLY", "strategic_cash": False, "residual": False, "funding_destination": False, "fifth_sleeve": False, "portfolio_policy": False, "annual_rate_unit": "PERCENT", "accrual_convention": "SIMPLE_ACTUAL_360_COMPOUNDED_BY_CALENDAR_DAY", "day_count_parameter_id": "DFF_DAY_COUNT_DENOMINATOR", "daily_factor": "ONE_PLUS_LAWFULLY_AVAILABLE_LAGGED_DFF_PERCENT_DIVIDED_BY_100_DIVIDED_BY_DAY_COUNT_DENOMINATOR", "availability_lag": "ONE_US_BUSINESS_DAY_AFTER_OBSERVATION_DATE", "calendar_day_rule": "USE_MOST_RECENT_LAWFULLY_AVAILABLE_LAGGED_DFF_FOR_WEEKENDS_AND_HOLIDAYS", "missing_rate_parameter_id": "DFF_MISSING_DAYS_ALLOWED", "missing_rate_rule": "ANY_MISSING_REQUIRED_LAGGED_OBSERVATION_MAKES_AFFECTED_OPPORTUNITY_COST_METRIC_UNAVAILABLE", "evaluation_alignment": "ACCRUE_EXACT_CALENDAR_DAYS_BETWEEN_COMMON_EVALUATION_TIMESTAMPS"}, "comparator", errors)
    _exact(_param(data, "DFF_MISSING_DAYS_ALLOWED"), 0, "DFF missing days", errors)
    inventory = data["trial_inventory"]
    rep_count = len(EQUITIES) + len(BROAD) + len(GOLD) + len(CRYPTO)
    scenario_count = len(data["scenario_states"])
    window_count = len(data["scenario_windows"]["windows"])
    _exact(inventory["representation_count"], rep_count, "trial representation count derived", errors)
    _exact(inventory["scenario_count"], scenario_count, "trial scenario count derived", errors)
    _exact(inventory["window_class_count"], window_count, "trial window count derived", errors)
    _exact(inventory["derived_registered_cell_ceiling"], rep_count * scenario_count * window_count, "trial ceiling derived", errors)
    _exact(inventory["derived_registered_cell_ceiling"], 777, "trial ceiling", errors)
    _exact(inventory["metrics_from_same_path_are_new_trials"], False, "metrics counted as trials", errors)
    _exact(inventory["failed_discarded_ineligible_attempts_remain_accounted"], True, "failed trials accounting", errors)
    _exact(inventory["reserve_trials"], 0, "reserve trials", errors)
    _exact(inventory["cell_identity"], "REPRESENTATION_TIMES_SCENARIO_TIMES_WINDOW_TIMES_EXACT_CONFIG_HASH_TIMES_DATA_HASH_BUNDLE", "trial cell identity", errors)
    _closed(inventory, {"representation_count": 37, "representation_derivation": {"equity_constituents": 27, "broad_market": 3, "gld_core_and_conditional": 4, "crypto": 3}, "scenario_count": 3, "window_class_count": 7, "derived_registered_cell_ceiling": 777, "formula": "REPRESENTATION_COUNT_TIMES_SCENARIO_COUNT_TIMES_WINDOW_COUNT", "cell_identity": "REPRESENTATION_TIMES_SCENARIO_TIMES_WINDOW_TIMES_EXACT_CONFIG_HASH_TIMES_DATA_HASH_BUNDLE", "metrics_from_same_path_are_new_trials": False, "failed_discarded_ineligible_attempts_remain_accounted": True, "reserve_trials": 0, "unused_capacity_reallocation": "PROHIBITED", "new_cells_after_results": "REQUIRES_CHARTER_AMENDMENT", "conditional_gld_cells_count_inside_ceiling": True}, "trial inventory", errors)
    _exact(tuple(data["prohibited_scope"]), PROHIBITED_SCOPE, "prohibited scope/order", errors)
    rerun = data["rerun_rule"]
    _exact(rerun["after_results_observed"], "PROHIBITED", "rerun after results", errors)
    _exact(rerun["discovered_defect_automatic_rerun"], "PROHIBITED", "defect rerun", errors)
    _closed(rerun, {"after_results_observed": "PROHIBITED", "required_authority": "SEPARATELY_ACCEPTED_CHARTER_AMENDMENT_OR_NEW_RISK_STUDY", "allowed_basis": ["MATERIAL_NEW_EVIDENCE_REGIME", "SEPARATELY_GOVERNED_INTEGRITY_CORRECTION"], "discovered_defect_automatic_rerun": "PROHIBITED", "preregistered_fallback_retries_before_execution": "PERMITTED_IF_LOGGED", "known_historical_windows_held_out_claim": "PROHIBITED", "terminology": "PREREGISTERED_HISTORICAL_REPLAY", "protocol_held_out": "ONLY_IF_GENUINELY_SEQUESTERED_AND_HASH_PROVED", "prospective_evidence": "ONLY_FUTURE_OBSERVATIONS_NOT_AVAILABLE_AT_CHARTER_FREEZE"}, "rerun rule", errors)
    _closed(data["result_vocabulary"], {"result_states": ["provisional_scenario_not_rejected", "policy_review_required", "unable_to_determine"], "review_direction": ["lower_exposure", "higher_exposure", None], "point_target_assessment": ["not_supported", "not_rejected", "unable_to_determine"], "method_review_direction": ["range_or_nonpoint", None], "non_rejection_equals_validation": False, "policy_review_equals_automatic_change": False}, "result vocabulary", errors)


def validate(data: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    if type(data) is not dict:
        return ValidationResult(("root: expected mapping",))
    try:
        _validate_structural_closure(data, errors)
        if tuple(data.keys()) != TOP_KEYS:
            return ValidationResult(tuple(errors))
        _validate_authority(data, errors)
        _validate_scenarios_registry(data, errors)
        _validate_windows_metrics_results(data, errors)
        _validate_gates_rules_inventory(data, errors)
        hv = data["hash_version"]
        _exact(hv["algorithm"], "SHA256", "hash algorithm", errors)
        _exact(hv["canonical_bytes"], "RAW_FILE_BYTES_AS_COMMITTED", "canonical hash bytes", errors)
        _exact(hv["embedded_self_hash"], False, "embedded self hash", errors)
        _closed(hv, {"algorithm": "SHA256", "canonical_bytes": "RAW_FILE_BYTES_AS_COMMITTED", "authority_pin_location": "governance/decisions/RISK-0001-level1-investable-sleeve-robustness-charter.md", "embedded_self_hash": False, "protocol_path": "research/level1_sleeve_robustness/PROTOCOL_V1.md", "preregistration_path": "research/level1_sleeve_robustness/pre_registration.yaml", "content_change_after_merge": "REQUIRES_SEPARATE_GOVERNANCE"}, "hash version", errors)
    except (KeyError, IndexError, TypeError, ValueError, ArithmeticError, AttributeError) as exc:
        errors.append(f"fail-closed structural validation: {type(exc).__name__}: {exc}")
    return ValidationResult(tuple(errors))


def validate_file(path: Path = PREREG_PATH) -> ValidationResult:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return ValidationResult((f"preregistration load failed: {exc}",))
    if type(loaded) is not dict:
        return ValidationResult(("root: expected mapping",))
    return validate(loaded)


HASH_BLOCK_RE = re.compile(r"<!-- RISK-0001-HASH-PINS-V1\n(?P<body>.*?)\n-->", re.DOTALL)
MIRROR_BLOCK_RE = re.compile(r"<!-- RISK-0001-PROTOCOL-MIRROR-V1\n(?P<body>.*?)\n-->", re.DOTALL)


def extract_charter_pins(path: Path = DECISION_PATH) -> tuple[dict[str, str] | None, tuple[str, ...]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, (f"charter pin read failed: {exc}",)
    matches = HASH_BLOCK_RE.findall(text)
    if len(matches) != 1:
        return None, (f"charter hash block count {len(matches)} != 1",)
    try:
        pins = yaml.safe_load(matches[0])
    except yaml.YAMLError as exc:
        return None, (f"charter hash block parse failed: {exc}",)
    expected_keys = ("protocol_path", "protocol_sha256", "preregistration_path", "preregistration_sha256")
    errors: list[str] = []
    if not _keys(pins, expected_keys, "charter hash block", errors):
        return None, tuple(errors)
    for key in ("protocol_sha256", "preregistration_sha256"):
        if not isinstance(pins[key], str) or not re.fullmatch(r"[0-9a-f]{64}", pins[key]):
            errors.append(f"charter hash block {key}: lowercase SHA-256 required")
    return pins, tuple(errors)


def protocol_mirror_expected(data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "study_id": data["study_id"],
        "scenario_states": data["scenario_states"],
        "relative_perturbation": _param(data, "RELATIVE_PERTURBATION"),
        "scenario_magnitudes": data["scenario_magnitudes"]["values_pct"],
        "window_ids": [w["id"] for w in data["scenario_windows"]["windows"]],
        "window_voting_roles": {w["id"]: w["voting_role"] for w in data["scenario_windows"]["windows"]},
        "source_fallbacks": {key: data["fallback_order"][key] for key in ("equities_etfs", "crypto", "comparator", "corporate_actions")},
        "data_gate_stages": data["data_gate"]["stage_order"],
        "voting_families": data["metric_families"]["voting_families"],
        "minimum_improvement_families": _param(data, "MINIMUM_IMPROVEMENT_FAMILIES"),
        "total_state_table": data["result_reduction"]["total_state_table"],
        "point_state_table": data["result_reduction"]["point_state_table"],
        "maximum_registered_cells": data["trial_inventory"]["derived_registered_cell_ceiling"],
        "rerun_after_results": data["rerun_rule"]["after_results_observed"],
    }


def validate_protocol_mirror(protocol_path: Path, data: Mapping[str, Any]) -> ValidationResult:
    try:
        text = protocol_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return ValidationResult((f"protocol mirror read failed: {exc}",))
    matches = MIRROR_BLOCK_RE.findall(text)
    if len(matches) != 1:
        return ValidationResult((f"protocol mirror block count {len(matches)} != 1",))
    try:
        actual = yaml.safe_load(matches[0])
    except yaml.YAMLError as exc:
        return ValidationResult((f"protocol mirror parse failed: {exc}",))
    errors: list[str] = []
    _closed(actual, protocol_mirror_expected(data), "protocol mirror", errors)
    return ValidationResult(tuple(errors))


def validate_repository(prereg_path: Path = PREREG_PATH, protocol_path: Path = PROTOCOL_PATH, decision_path: Path = DECISION_PATH) -> ValidationResult:
    errors = list(validate_file(prereg_path).errors)
    try:
        data = yaml.safe_load(prereg_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return ValidationResult(tuple(errors + [f"repository preregistration load failed: {exc}"]))
    if type(data) is dict:
        try:
            errors.extend(validate_protocol_mirror(protocol_path, data).errors)
        except (KeyError, IndexError, TypeError, ValueError, AttributeError) as exc:
            errors.append(f"protocol mirror fail-closed validation: {type(exc).__name__}: {exc}")
    pins, pin_errors = extract_charter_pins(decision_path)
    errors.extend(pin_errors)
    if pins is not None and not pin_errors:
        expected_protocol = str(Path(pins["protocol_path"]))
        expected_prereg = str(Path(pins["preregistration_path"]))
        _exact(expected_protocol, "research/level1_sleeve_robustness/PROTOCOL_V1.md", "charter protocol path", errors)
        _exact(expected_prereg, "research/level1_sleeve_robustness/pre_registration.yaml", "charter preregistration path", errors)
        try:
            _exact(sha256_file(protocol_path), pins["protocol_sha256"], "protocol SHA-256 pin", errors)
            _exact(sha256_file(prereg_path), pins["preregistration_sha256"], "preregistration SHA-256 pin", errors)
        except OSError as exc:
            errors.append(f"hash input read failed: {exc}")
    return ValidationResult(tuple(errors))


def classify_observation(candidate: Decimal | None, reference: Decimal | None, tolerance: Decimal, direction: str, not_applicable: bool = False) -> str:
    if not_applicable:
        return "NOT_APPLICABLE"
    if candidate is None or reference is None:
        return "UNAVAILABLE"
    delta = candidate - reference
    if abs(delta) <= tolerance:
        return "EQUIVALENT"
    if direction == "HIGHER":
        return "IMPROVES" if delta > tolerance else "WORSENS"
    if direction == "LOWER":
        return "IMPROVES" if -delta > tolerance else "WORSENS"
    raise ValueError("direction must be HIGHER or LOWER")


def reduce_states(states: Iterable[str]) -> str:
    applicable = [state for state in states if state != "NOT_APPLICABLE"]
    if not applicable:
        return "UNAVAILABLE"
    for state in ("WORSENS", "UNAVAILABLE", "IMPROVES", "EQUIVALENT"):
        if state in applicable:
            return state
    raise ValueError(f"unknown state in {applicable!r}")


def reduce_representations(family: str, states: Mapping[str, str], admitted_gold: Sequence[str] = ()) -> str:
    if family == "FUND_BROAD_MARKET":
        required = BROAD
    elif family == "CRYPTO":
        required = CRYPTO
    elif family == "FUND_GLD_DEFENSIVE":
        required = ("GLD",) + tuple(admitted_gold)
    else:
        raise ValueError("family requires equity-specific or supported representation reducer")
    values = [states.get(rep, "UNAVAILABLE") for rep in required]
    if "UNAVAILABLE" in values:
        return "UNAVAILABLE"
    if any(value not in FAMILY_STATES for value in values):
        raise ValueError("unknown family state")
    return values[0] if len(set(values)) == 1 else "CONFLICT"


def reduce_equity(states: Sequence[str], median_state: str, leave_one_out_states: Sequence[str], minimum_eligible: int = 21, breadth: Decimal = Decimal("0.75")) -> str:
    eligible = [state for state in states if state != "UNAVAILABLE"]
    if len(eligible) < minimum_eligible:
        return "UNAVAILABLE"
    counts = {state: eligible.count(state) for state in ("IMPROVES", "EQUIVALENT", "WORSENS")}
    winner = max(counts, key=counts.get)
    if Decimal(counts[winner]) / Decimal(len(eligible)) < breadth:
        return "CONFLICT"
    if median_state != winner or any(state != winner for state in leave_one_out_states):
        return "CONFLICT"
    return winner


def directional_disposition(family_states: Mapping[str, str], minimum_improvements: int = 2, monotonicity_ok: bool = True, representation_conflict: bool = False) -> str:
    values = [family_states.get(family, "UNAVAILABLE") for family in VOTING_FAMILIES]
    if not monotonicity_ok or representation_conflict or any(value in ("UNAVAILABLE", "CONFLICT") for value in values):
        return "UNABLE_TO_DETERMINE"
    if "IMPROVES" in values and "WORSENS" in values:
        return "UNABLE_TO_DETERMINE"
    if "WORSENS" not in values and values.count("IMPROVES") >= minimum_improvements:
        return "POLICY_REVIEW_REQUIRED"
    return "CENTER_NOT_REJECTED"


def point_evidence(family_states: Mapping[str, str], directional_state: str, minimum_worsening: int = 2) -> str:
    if directional_state == "POLICY_REVIEW_REQUIRED":
        return "DISPLACES_REFERENCE"
    if directional_state == "UNABLE_TO_DETERMINE":
        return "UNAVAILABLE"
    values = [family_states.get(family, "UNAVAILABLE") for family in VOTING_FAMILIES]
    if values.count("WORSENS") >= minimum_worsening and "IMPROVES" not in values:
        return "ADJACENT_MATERIALLY_WORSE"
    return "NOT_DISTINGUISHED"


def final_disposition(lower: str, higher: str, lower_point: str, higher_point: str) -> dict[str, str | None]:
    result_row = None
    for row in TOTAL_STATE_TABLE:
        if row[0] == lower and row[1] == higher:
            result_row = row
            break
    if result_row is None:
        raise ValueError("directional states must use the closed vocabulary")
    for row in POINT_STATE_TABLE:
        if row[0] == lower_point and row[1] == higher_point:
            return {"result": result_row[2], "review_direction": result_row[3], "point_target_assessment": row[2], "method_review_direction": row[3]}
    raise ValueError("point evidence states must use the closed vocabulary")


def main() -> int:
    result = validate_repository()
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}")
        return 1
    print(f"RISK-0001 repository authority valid; protocol_sha256={sha256_file(PROTOCOL_PATH)}; preregistration_sha256={sha256_file(PREREG_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
