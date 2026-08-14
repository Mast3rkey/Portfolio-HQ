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

PARAMETER_KEYS = (
    "parameter_id", "value", "unit", "num_0001_class", "contextual_class",
    "selection_basis", "evidence_status", "supporting_evidence",
    "canonical_source", "duplicate_locations", "fallback_locations",
    "hardcoded_or_config_editable", "binding_status", "binding_scope",
    "valid_for_study_id", "lapse_condition", "reuse_rule", "calibrated",
    "evidence_bounded",
)
PARAMETER_SPECS = {
    "RELATIVE_PERTURBATION": ("0.20", "PROPORTION", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "SCENARIO_DECIMAL_PLACES": (2, "DECIMAL_PLACES", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "SCENARIO_ROUNDING_MODE": ("ROUND_HALF_UP", "DECIMAL_ROUNDING_MODE", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "DFF_DAY_COUNT_DENOMINATOR": (360, "DAYS", "EXTERNALLY_IMPOSED"),
    "DFF_AVAILABILITY_LAG_BUSINESS_DAYS": (1, "US_FEDERAL_RESERVE_BANK_BUSINESS_DAYS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
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
    "GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED": (0, "REQUIRED_XNYS_SESSIONS_PER_REGISTERED_WINDOW", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED": (0, "DUPLICATE_UTC_TIMESTAMPS_PER_REGISTERED_WINDOW", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "CRYPTO_MISSING_DAYS_ALLOWED": (0, "UTC_DAYS_PER_REGISTERED_WINDOW", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS": (0, "UTC_DAYS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    "FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE": ("0.000001", "ABSOLUTE_OUTPUT_UNITS", "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
}
PARAMETER_GOVERNANCE = {
    "RELATIVE_PERTURBATION": ("SYMMETRIC_COARSE_SENSITIVITY_WITHOUT_GRID_SEARCH", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "SCENARIO_CONSTRUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "SCENARIO_DECIMAL_PLACES": ("DETERMINISTIC_PERCENTAGE_POINT_REPORTING_PRECISION", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "SCENARIO_MAGNITUDE_DERIVATION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "SCENARIO_ROUNDING_MODE": ("DETERMINISTIC_TIE_BREAKING_FOR_DECIMAL_PERCENTAGE_POINTS", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "SCENARIO_MAGNITUDE_DERIVATION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "DFF_DAY_COUNT_DENOMINATOR": ("DFF_MONEY_MARKET_ACTUAL_360_QUOTATION_CONVENTION", "CONVENTION_NOT_CALIBRATION", "DFF_DAILY_ACCRUAL", "REVALIDATE_CONVENTION_UNDER_NEW_AUTHORITY"),
    "DFF_AVAILABILITY_LAG_BUSINESS_DAYS": ("CONSERVATIVE_NO_LOOKAHEAD_AVAILABILITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "DFF_LAWFUL_AVAILABILITY_TIMESTAMP", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "DFF_MISSING_DAYS_ALLOWED": ("NO_IMPUTATION_OF_MISSING_COMPARATOR_OBSERVATIONS", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "AFFECTED_OPPORTUNITY_COST_METRIC_WINDOWS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "MINIMUM_IMPROVEMENT_FAMILIES": ("MULTIDIMENSION_CONFIRMATION_WITHOUT_METRIC_WEIGHTING", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "DIRECTIONAL_AND_POINT_EVIDENCE_REDUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "LOSS_CONTRIBUTION_TOLERANCE_PP": ("MATERIAL_DIFFERENCE_GUARDRAIL_FOR_EXPOSURE_SCALED_LOSS", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "PATH_RISK_METRICS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "RECOVERY_BURDEN_TOLERANCE_PPDAYS": ("MATERIAL_DIFFERENCE_GUARDRAIL_FOR_EXPOSURE_SCALED_UNDERWATER_BURDEN", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "RECOVERY_METRICS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP": ("MATERIAL_DIFFERENCE_GUARDRAIL_FOR_EXPOSURE_SCALED_EXCESS_RETURN", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "OPPORTUNITY_COST_METRICS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "EQUITY_MINIMUM_ELIGIBLE": ("THREE_QUARTERS_OF_FROZEN_27_ROUNDED_UP", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "EQUITY_REPRESENTATION_REDUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "EQUITY_DIRECTIONAL_BREADTH": ("SUPERMAJORITY_DIRECTIONAL_CONSISTENCY_WITHOUT_AGGREGATE_PATH", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "EQUITY_REPRESENTATION_REDUCTION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_PARITY_CORRELATION_MIN": ("STRICT_SAME_EXPOSURE_REPRESENTATION_PARITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_PARITY_RETURN_MAX_PP": ("STRICT_SAME_EXPOSURE_RETURN_PARITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_PARITY_DRAWDOWN_MAX_PP": ("STRICT_SAME_EXPOSURE_PATH_PARITY_GUARDRAIL", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED": ("COMPLETE_CONDITIONAL_GOLD_PEER_PATH_WITHOUT_IMPUTATION", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "CONDITIONAL_GOLD_PEER_ADMISSION", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED": ("UNIQUE_UTC_DAILY_PATH_IDENTITY_REQUIRED", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "CRYPTO_CELL_ELIGIBILITY", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "CRYPTO_MISSING_DAYS_ALLOWED": ("COMPLETE_24_7_PATH_REQUIRED_WITHOUT_IMPUTATION", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "CRYPTO_CELL_ELIGIBILITY", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS": ("COMPLETE_24_7_PATH_REQUIRED_WITHOUT_IMPUTATION", "CONSERVATIVE_INTEGRITY_GUARDRAIL", "CRYPTO_CELL_ELIGIBILITY", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
    "FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE": ("SIX_DECIMAL_EXACTNESS_CHECK_WITHOUT_MASKING_MATERIAL_FORMULA_ERROR", "NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED", "EXPOSURE_SCALED_FORMULA_IDENTITY_CHECKS", "NEW_GOVERNANCE_AUTHORITY_REQUIRED"),
}

PARAMETER_SUPPORT = {
    "RELATIVE_PERTURBATION": "NONE_DOCTRINE_ONE_STUDY_SENSITIVITY",
    "SCENARIO_DECIMAL_PLACES": "NONE_DOCTRINE_DETERMINISTIC_DECIMAL_CONVENTION",
    "SCENARIO_ROUNDING_MODE": "NONE_DOCTRINE_DETERMINISTIC_DECIMAL_CONVENTION",
    "DFF_DAY_COUNT_DENOMINATOR": "FRED_DFF_SERIES_QUOTATION_CONVENTION",
    "DFF_AVAILABILITY_LAG_BUSINESS_DAYS": "MARGIN_0005_NO_LOOKAHEAD_PRECEDENT",
    "DFF_MISSING_DAYS_ALLOWED": "NONE_DOCTRINE_NO_IMPUTATION",
    "MINIMUM_IMPROVEMENT_FAMILIES": "NONE_DOCTRINE_MULTIFAMILY_CONFIRMATION",
    "LOSS_CONTRIBUTION_TOLERANCE_PP": "NONE_DOCTRINE_ONE_STUDY_MATERIALITY",
    "RECOVERY_BURDEN_TOLERANCE_PPDAYS": "NONE_DOCTRINE_ONE_STUDY_MATERIALITY",
    "OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP": "NONE_DOCTRINE_ONE_STUDY_MATERIALITY",
    "EQUITY_MINIMUM_ELIGIBLE": "NONE_DOCTRINE_COHORT_COVERAGE_GATE",
    "EQUITY_DIRECTIONAL_BREADTH": "NONE_DOCTRINE_CROSS_SECTIONAL_SUPERMAJORITY",
    "GOLD_PARITY_CORRELATION_MIN": "NONE_DOCTRINE_CONDITIONAL_REPRESENTATION_PARITY",
    "GOLD_PARITY_RETURN_MAX_PP": "NONE_DOCTRINE_CONDITIONAL_REPRESENTATION_PARITY",
    "GOLD_PARITY_DRAWDOWN_MAX_PP": "NONE_DOCTRINE_CONDITIONAL_REPRESENTATION_PARITY",
    "GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED": "NONE_DOCTRINE_CONDITIONAL_REPRESENTATION_PARITY",
    "CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED": "NONE_DOCTRINE_COMPLETE_CRYPTO_PATH",
    "CRYPTO_MISSING_DAYS_ALLOWED": "NONE_DOCTRINE_COMPLETE_CRYPTO_PATH",
    "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS": "NONE_DOCTRINE_COMPLETE_CRYPTO_PATH",
    "FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE": "NONE_DOCTRINE_DETERMINISTIC_DECIMAL_INTEGRITY",
}
PARAMETER_DUPLICATES = (
    "level1_sleeve_robustness_preregistration_validator.py::PARAMETER_SPECS_AND_MECHANICAL_VALIDATION",
    "research/level1_sleeve_robustness/PROTOCOL_V1.md::RISK-0001-PROTOCOL-MIRROR-V1",
    "governance/decisions/RISK-0001-level1-investable-sleeve-robustness-charter.md::NUM-0001_PROVENANCE_NARRATIVE",
)

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
        "comparator": ("series", "role", "strategic_cash", "residual", "funding_destination", "fifth_sleeve", "portfolio_policy", "annual_rate_unit", "accrual_convention", "day_count_parameter_id", "daily_factor", "availability_lag_parameter_id", "availability_origin", "business_calendar", "lawful_availability_timestamp", "lookup_rule", "calendar_day_rule", "missing_rate_parameter_id", "missing_rate_rule", "evaluation_alignment"),
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
        (data["data_gate"]["gld_conditional_peer_gate"], ("required", "unresolved_required_session_gaps_parameter_id", "requirements", "failure_state"), "data_gate.gld_conditional_peer_gate"),
        (data["data_gate"]["crypto_gate"], ("utc_normalization", "expected_calendar", "duplicate_timestamps_parameter_id", "missing_days_parameter_id", "maximum_contiguous_gap_parameter_id", "ohlc_rules", "pagination_completeness", "interpolation", "forward_fill", "fabricated_pre_inception", "undisclosed_alternate_source_stitching", "known_sol_gap_rule"), "data_gate.crypto_gate"),
        (data["result_reduction"]["canonical_states"], ("observation", "family", "directional", "point_evidence"), "result_reduction.canonical_states"),
        (data["result_reduction"]["observation_rule"], ("HIGHER", "LOWER", "missing_state"), "result_reduction.observation_rule"),
        (data["result_reduction"]["metric_window_reduction"], ("ordered_precedence", "NOT_APPLICABLE", "zero_applicable_observations", "mandatory_window_unavailable", "conditional_window_missing_data_or_quality_failure"), "result_reduction.metric_window_reduction"),
        (data["result_reduction"]["family_metric_reduction"], ("ordered_precedence", "mandatory_voting_metric_unavailable", "conditional_voting_metric_not_applicable_for_all_lawful_representations", "zero_applicable_voting_metrics", "non_voting_metrics"), "result_reduction.family_metric_reduction"),
        (data["result_reduction"]["representation_reduction"], ("FUND_BROAD_MARKET", "CRYPTO", "FUND_GLD_DEFENSIVE", "EQUITY"), "result_reduction.representation_reduction"),
        (data["scenario_provenance"]["rounding"], ("decimal_places_parameter_id", "mode_parameter_id"), "scenario_provenance.rounding"),
        (data["result_reduction"]["monotonicity"], ("designated_metrics", "rule", "tolerance_parameter_id", "failure_effect"), "result_reduction.monotonicity"),
        (data["result_reduction"]["directional_policy_review"], ("mandatory_veto_families", "minimum_improvement_parameter_id", "policy_review_required", "center_not_rejected", "unable_to_determine", "no_metric_weighting", "representation_conflict_veto"), "result_reduction.directional_policy_review"),
        (data["result_reduction"]["point_evidence_rule"], ("minimum_worsening_parameter_id", "DISPLACES_REFERENCE", "ADJACENT_MATERIALLY_WORSE", "NOT_DISTINGUISHED", "UNAVAILABLE"), "result_reduction.point_evidence_rule"),
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
    _exact(provenance["rounding"], {"decimal_places_parameter_id": "SCENARIO_DECIMAL_PLACES", "mode_parameter_id": "SCENARIO_ROUNDING_MODE"}, "scenario rounding authority", errors)
    _exact((provenance["lapse"], provenance["reuse"]), ("AUTOMATIC_ON_AUTHORIZED_STUDY_COMPLETION", "REQUIRES_NEW_GOVERNANCE_AUTHORITY"), "scenario governance", errors)
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
        expected_context = "ENGINEERING_CONSTANT" if pid == "FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE" else "RESEARCH_ASSUMPTION"
        _exact(record["contextual_class"], expected_context, f"{pid}.contextual_class", errors)
        _exact(record["valid_for_study_id"], "RISK-0001", f"{pid}.valid_for_study_id", errors)
        _exact(record["lapse_condition"], "AUTHORIZED_STUDY_COMPLETION", f"{pid}.lapse_condition", errors)
        _exact(record["calibrated"], False, f"{pid}.calibrated", errors)
        _exact(record["evidence_bounded"], False, f"{pid}.evidence_bounded", errors)
        basis, evidence, scope, reuse = PARAMETER_GOVERNANCE[pid]
        _exact((record["selection_basis"], record["evidence_status"], record["binding_scope"], record["reuse_rule"]), (basis, evidence, scope, reuse), f"{pid}.governance", errors)
        _exact(record["supporting_evidence"], PARAMETER_SUPPORT[pid], f"{pid}.supporting_evidence", errors)
        _exact(record["canonical_source"], f"research/level1_sleeve_robustness/pre_registration.yaml::consequential_parameter_registry.parameters[{pid}]", f"{pid}.canonical_source", errors)
        _exact(tuple(record["duplicate_locations"]), PARAMETER_DUPLICATES, f"{pid}.duplicate_locations", errors)
        _exact(record["fallback_locations"], [], f"{pid}.fallback_locations", errors)
        _exact(record["hardcoded_or_config_editable"], "CONFIG_EDITABLE_ONLY_THROUGH_SEPARATE_GOVERNANCE", f"{pid}.hardcoded_or_config_editable", errors)
        _exact(record["binding_status"], "BINDING_FOR_AUTHORIZED_RISK_0001_STUDY", f"{pid}.binding_status", errors)
    perturbation = Decimal(str(_param(data, "RELATIVE_PERTURBATION")))
    decimal_places = _param(data, "SCENARIO_DECIMAL_PLACES")
    rounding_mode = _param(data, "SCENARIO_ROUNDING_MODE")
    _exact(rounding_mode, "ROUND_HALF_UP", "scenario rounding mode", errors)
    quantum = Decimal(1).scaleb(-decimal_places)
    for family, ref_text in refs.items():
        ref = Decimal(ref_text)
        expected = {
            "LOWER": (ref * (Decimal(1) - perturbation)).quantize(quantum, rounding=ROUND_HALF_UP),
            "HISTORICAL_REFERENCE": ref,
            "HIGHER": (ref * (Decimal(1) + perturbation)).quantize(quantum, rounding=ROUND_HALF_UP),
        }
        actual = data["scenario_magnitudes"]["values_pct"][family]
        for state in SCENARIOS:
            if not isinstance(actual[state], str) or not re.fullmatch(rf"\d+\.\d{{{decimal_places}}}", actual[state]):
                errors.append(f"scenario_magnitudes.{family}.{state}: exact registered-decimal string required")
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
    _closed(rr["point_evidence_rule"], {"minimum_worsening_parameter_id": "MINIMUM_IMPROVEMENT_FAMILIES", "DISPLACES_REFERENCE": "DIRECTIONAL_STATE_POLICY_REVIEW_REQUIRED", "ADJACENT_MATERIALLY_WORSE": "DIRECTIONAL_STATE_CENTER_NOT_REJECTED_AND_AT_LEAST_MINIMUM_IMPROVEMENT_FAMILIES_COUNT_WORSENS_AND_ZERO_IMPROVES", "NOT_DISTINGUISHED": "DIRECTIONAL_STATE_CENTER_NOT_REJECTED_AND_ADJACENT_MATERIALLY_WORSE_RULE_NOT_MET", "UNAVAILABLE": "DIRECTIONAL_STATE_UNABLE_TO_DETERMINE"}, "point evidence rule", errors)
    actual_table = tuple((r["lower"], r["higher"], r["result"], r["review_direction"]) for r in rr["total_state_table"])
    _exact(actual_table, TOTAL_STATE_TABLE, "total state table", errors)
    actual_point_table = tuple((r["lower"], r["higher"], r["point_target_assessment"], r["method_review_direction"]) for r in rr["point_state_table"])
    _exact(actual_point_table, POINT_STATE_TABLE, "point state table", errors)
    _closed(rr["observation_rule"], {"HIGHER": {"IMPROVES": "CANDIDATE_MINUS_REFERENCE_GREATER_THAN_TOLERANCE", "EQUIVALENT": "ABS_CANDIDATE_MINUS_REFERENCE_LESS_THAN_OR_EQUAL_TO_TOLERANCE", "WORSENS": "CANDIDATE_MINUS_REFERENCE_LESS_THAN_NEGATIVE_TOLERANCE"}, "LOWER": {"IMPROVES": "REFERENCE_MINUS_CANDIDATE_GREATER_THAN_TOLERANCE", "EQUIVALENT": "ABS_CANDIDATE_MINUS_REFERENCE_LESS_THAN_OR_EQUAL_TO_TOLERANCE", "WORSENS": "REFERENCE_MINUS_CANDIDATE_LESS_THAN_NEGATIVE_TOLERANCE"}, "missing_state": "UNAVAILABLE_UNLESS_CONDITIONAL_WINDOW_IS_NOT_APPLICABLE_PRE_INCEPTION"}, "observation rule", errors)
    _closed(rr["monotonicity"], {"designated_metrics": ["EXPOSURE_SCALED_DRAWDOWN_LOSS", "EXPOSURE_SCALED_STRESS_LOSS", "EXPOSURE_SCALED_UNDERWATER_BURDEN", "EXPOSURE_SCALED_EXCESS_CONTRIBUTION"], "rule": "RECOMPUTE_EACH_VALUE_FROM_RAW_METRIC_AND_REGISTERED_EXPOSURE_WITH_DECIMAL_ARITHMETIC_AND_VERIFY_FORMULA_IDENTITY", "tolerance_parameter_id": "FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE", "failure_effect": "DIRECTIONAL_UNABLE_TO_DETERMINE"}, "monotonicity", errors)
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
    _closed(gate["crypto_gate"], {"utc_normalization": "REQUIRED", "expected_calendar": "EVERY_UTC_DAY_IN_REGISTERED_WINDOW", "duplicate_timestamps_parameter_id": "CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED", "missing_days_parameter_id": "CRYPTO_MISSING_DAYS_ALLOWED", "maximum_contiguous_gap_parameter_id": "CRYPTO_MAX_CONTIGUOUS_GAP_DAYS", "ohlc_rules": ["FINITE", "POSITIVE", "LOW_LE_MIN_OPEN_CLOSE", "HIGH_GE_MAX_OPEN_CLOSE", "HIGH_GE_LOW"], "pagination_completeness": "REQUIRED", "interpolation": "PROHIBITED", "forward_fill": "PROHIBITED", "fabricated_pre_inception": "PROHIBITED", "undisclosed_alternate_source_stitching": "PROHIBITED", "known_sol_gap_rule": "REINVENTORY_418_DAY_AGGREGATE_GAP_AND_MARK_EVERY_INTERSECTING_WINDOW_INELIGIBLE"}, "crypto gate", errors)
    _exact(gate["gld_conditional_peer_gate"], {"required": False, "unresolved_required_session_gaps_parameter_id": "GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED", "requirements": ["COMPLETE_IDENTITY_AND_INCEPTION", "ZERO_UNRESOLVED_REQUIRED_SESSION_GAPS", "COMPLETE_DIVIDEND_SPLIT_ACTION_TREATMENT", "OVERLAP_TOTAL_RETURN_CORRELATION_AT_LEAST_GOLD_PARITY_CORRELATION_MIN", "OVERLAP_ANNUALIZED_RETURN_DIFFERENCE_AT_MOST_GOLD_PARITY_RETURN_MAX_PP", "OVERLAP_MAX_DRAWDOWN_DIFFERENCE_AT_MOST_GOLD_PARITY_DRAWDOWN_MAX_PP"], "failure_state": "CONDITIONAL_ASSET_NOT_ACQUIRED"}, "gold conditional peer gate", errors)
    _exact(_param(data, "GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED"), 0, "gold unresolved gaps", errors)
    _exact(_param(data, "CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED"), 0, "crypto duplicate timestamps", errors)
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
    _closed(comparator, {"series": "DFF", "role": "ANALYTICAL_OPPORTUNITY_COST_ONLY", "strategic_cash": False, "residual": False, "funding_destination": False, "fifth_sleeve": False, "portfolio_policy": False, "annual_rate_unit": "PERCENT", "accrual_convention": "SIMPLE_ACTUAL_360_COMPOUNDED_BY_CALENDAR_DAY", "day_count_parameter_id": "DFF_DAY_COUNT_DENOMINATOR", "daily_factor": "ONE_PLUS_LAWFULLY_AVAILABLE_LAGGED_DFF_PERCENT_DIVIDED_BY_100_DIVIDED_BY_DAY_COUNT_DENOMINATOR", "availability_lag_parameter_id": "DFF_AVAILABILITY_LAG_BUSINESS_DAYS", "availability_origin": "DFF_OBSERVATION_DATE", "business_calendar": "US_FEDERAL_RESERVE_BANK_BUSINESS_DAYS", "lawful_availability_timestamp": "23:59:59_AMERICA_NEW_YORK_ON_THE_BUSINESS_DATE_ONE_REGISTERED_LAG_AFTER_OBSERVATION_DATE", "lookup_rule": "LATEST_DFF_OBSERVATION_WHOSE_LAWFUL_AVAILABILITY_TIMESTAMP_IS_AT_OR_BEFORE_EVALUATION_TIMESTAMP", "calendar_day_rule": "WEEKENDS_AND_HOLIDAYS_USE_LATEST_LAWFULLY_AVAILABLE_LAGGED_DFF_WITH_NO_FORWARD_LOOKUP", "missing_rate_parameter_id": "DFF_MISSING_DAYS_ALLOWED", "missing_rate_rule": "ANY_MISSING_REQUIRED_LAGGED_OBSERVATION_MAKES_AFFECTED_OPPORTUNITY_COST_METRIC_UNAVAILABLE", "evaluation_alignment": "ACCRUE_EXACT_CALENDAR_DAYS_BETWEEN_COMMON_EVALUATION_TIMESTAMPS"}, "comparator", errors)
    _exact(_param(data, "DFF_AVAILABILITY_LAG_BUSINESS_DAYS"), 1, "DFF availability lag", errors)
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
        "consequential_parameter_values": {
            record["parameter_id"]: record["value"]
            for record in data["consequential_parameter_registry"]["parameters"]
        },
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


class RuntimeAuthorityError(ValueError):
    """A runtime observation does not conform to frozen canonical authority."""


def _runtime_authority() -> dict[str, Any]:
    result = validate_repository()
    if result.errors:
        raise RuntimeAuthorityError("canonical RISK-0001 authority is invalid: " + "; ".join(result.errors))
    loaded = yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))
    if type(loaded) is not dict:
        raise RuntimeAuthorityError("canonical preregistration is not a mapping")
    return loaded


def _runtime_decimal(value: Any, where: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise RuntimeAuthorityError(f"{where}: exact decimal-compatible scalar required")
    try:
        parsed = Decimal(str(value))
    except ArithmeticError as exc:
        raise RuntimeAuthorityError(f"{where}: invalid decimal") from exc
    if not parsed.is_finite():
        raise RuntimeAuthorityError(f"{where}: finite decimal required")
    return parsed


def _runtime_mapping(value: Any, keys: Sequence[str], where: str) -> Mapping[str, Any]:
    if type(value) is not dict or tuple(value) != tuple(keys):
        raise RuntimeAuthorityError(f"{where}: exact keys/order {tuple(keys)!r} required")
    return value


def _runtime_state(value: Any, vocabulary: Sequence[str], where: str) -> str:
    if type(value) is not str or value not in vocabulary:
        raise RuntimeAuthorityError(f"{where}: unknown state {value!r}")
    return value


def _registered_representations(data: Mapping[str, Any], family: str) -> tuple[str, ...]:
    if family == "EQUITY":
        return tuple(data["representations"][family]["ids"])
    if family in ("FUND_BROAD_MARKET", "CRYPTO"):
        return tuple(data["representations"][family]["ids"])
    if family == "FUND_GLD_DEFENSIVE":
        section = data["representations"][family]
        return tuple(section["core_ids"] + section["conditional_ids"])
    raise RuntimeAuthorityError(f"unknown research family {family!r}")


def _validate_observation_identity(
    data: Mapping[str, Any],
    research_family: str,
    representation_id: str,
    scenario_id: str,
    metric_id: str,
    window_id: str,
) -> Mapping[str, Any]:
    metrics = {record["metric_id"]: record for record in data["metric_families"]["metrics"]}
    if metric_id not in metrics:
        raise RuntimeAuthorityError(f"unknown metric_id {metric_id!r}")
    if research_family not in FAMILIES:
        raise RuntimeAuthorityError(f"unknown research_family {research_family!r}")
    if representation_id not in _registered_representations(data, research_family):
        raise RuntimeAuthorityError(f"unknown representation_id {representation_id!r} for {research_family}")
    if scenario_id not in ("LOWER", "HIGHER"):
        raise RuntimeAuthorityError(f"unknown comparison scenario_id {scenario_id!r}")
    if window_id not in WINDOWS:
        raise RuntimeAuthorityError(f"unknown window_id {window_id!r}")
    return metrics[metric_id]


def _derive_formula_values(
    data: Mapping[str, Any],
    research_family: str,
    representation_id: str,
    scenario_id: str,
    metric_id: str,
    window_id: str,
    raw_operands: Mapping[str, Any] | None,
    reported_candidate: Decimal | str | int | None,
    reported_reference: Decimal | str | int | None,
    missingness_state: str,
) -> tuple[Decimal | None, Decimal | None, tuple[Decimal, ...] | None]:
    """Derive the only result-driving values from canonical raw operands.

    Retained candidate/reference fields are reporting checks only.  They are
    reconciled to the derived values and never drive classification.
    """
    metric = _validate_observation_identity(
        data, research_family, representation_id, scenario_id, metric_id, window_id
    )
    designated = tuple(data["result_reduction"]["monotonicity"]["designated_metrics"])
    if metric_id not in designated or metric["voting_status"] not in ("MANDATORY_VOTING", "CONDITIONAL_VOTING"):
        raise RuntimeAuthorityError(f"metric {metric_id} is not an applicable formula-bearing voting metric")
    _runtime_state(missingness_state, MISSINGNESS, "missingness_state")
    if missingness_state != "ELIGIBLE":
        if raw_operands is not None or reported_candidate is not None or reported_reference is not None:
            raise RuntimeAuthorityError("ineligible formula observation requires null operands and reporting values")
        return None, None, None

    operand_keys = {
        "EXPOSURE_SCALED_DRAWDOWN_LOSS": ("drawdown",),
        "EXPOSURE_SCALED_STRESS_LOSS": ("stress_return",),
        "EXPOSURE_SCALED_UNDERWATER_BURDEN": ("underwater_area_days",),
        "EXPOSURE_SCALED_EXCESS_CONTRIBUTION": ("asset_total_return", "comparator_total_return"),
    }
    operands = _runtime_mapping(raw_operands, operand_keys[metric_id], f"{metric_id}.raw_operands")
    values = tuple(_runtime_decimal(operands[key], f"{metric_id}.{key}") for key in operand_keys[metric_id])
    if metric_id == "EXPOSURE_SCALED_DRAWDOWN_LOSS":
        if values[0] > 0:
            raise RuntimeAuthorityError("drawdown operand must be zero or negative")
        raw_metric_value = abs(values[0])
    elif metric_id == "EXPOSURE_SCALED_STRESS_LOSS":
        raw_metric_value = max(Decimal("0"), -values[0])
    elif metric_id == "EXPOSURE_SCALED_UNDERWATER_BURDEN":
        if values[0] < 0:
            raise RuntimeAuthorityError("underwater-area operand must be nonnegative")
        raw_metric_value = values[0]
    else:
        raw_metric_value = values[0] - values[1]

    scenario_exposure = _runtime_decimal(
        data["scenario_magnitudes"]["values_pct"][research_family][scenario_id],
        f"{research_family}.{scenario_id} exposure",
    )
    reference_exposure = _runtime_decimal(
        data["scenario_magnitudes"]["values_pct"][research_family]["HISTORICAL_REFERENCE"],
        f"{research_family}.HISTORICAL_REFERENCE exposure",
    )
    candidate = scenario_exposure * raw_metric_value
    reference = reference_exposure * raw_metric_value
    reported_candidate_value = _runtime_decimal(reported_candidate, "reported_candidate")
    reported_reference_value = _runtime_decimal(reported_reference, "reported_reference")
    tolerance = _runtime_decimal(
        _param(data, "FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE"), "formula tolerance"
    )
    if abs(reported_candidate_value - candidate) > tolerance:
        raise RuntimeAuthorityError("reported candidate does not reconcile to canonical formula operands")
    if abs(reported_reference_value - reference) > tolerance:
        raise RuntimeAuthorityError("reported reference does not reconcile to canonical formula operands")
    return candidate, reference, values


def _classify_observation(
    data: Mapping[str, Any],
    research_family: str,
    representation_id: str,
    scenario_id: str,
    metric_id: str,
    window_id: str,
    candidate: Decimal | str | int | None,
    reference: Decimal | str | int | None,
    missingness_state: str,
) -> str:
    """Private state classifier; authoritative use is through evaluate_study_evidence."""
    metric = _validate_observation_identity(
        data, research_family, representation_id, scenario_id, metric_id, window_id
    )
    _runtime_state(missingness_state, MISSINGNESS, "missingness_state")
    candidate_value = None if candidate is None else _runtime_decimal(candidate, "candidate")
    reference_value = None if reference is None else _runtime_decimal(reference, "reference")
    if missingness_state == "ELIGIBLE" and (candidate_value is None or reference_value is None):
        raise RuntimeAuthorityError("eligible observation requires candidate and reference values")
    if missingness_state != "ELIGIBLE" and (candidate_value is not None or reference_value is not None):
        raise RuntimeAuthorityError("ineligible observation values must be null")
    parameter_id = metric["equivalence_parameter_id"]
    if parameter_id is None or metric["direction_of_preference"] not in ("HIGHER", "LOWER"):
        raise RuntimeAuthorityError(f"metric {metric_id} is not a classified voting metric")
    if missingness_state == "NOT_APPLICABLE_PRE_INCEPTION":
        return "NOT_APPLICABLE"
    if missingness_state != "ELIGIBLE":
        return "UNAVAILABLE"
    tolerance = _runtime_decimal(_param(data, parameter_id), parameter_id)
    delta = candidate_value - reference_value
    if abs(delta) <= tolerance:
        return "EQUIVALENT"
    if metric["direction_of_preference"] == "HIGHER":
        return "IMPROVES" if delta > tolerance else "WORSENS"
    return "IMPROVES" if -delta > tolerance else "WORSENS"


def _reduce_states(states: Iterable[str]) -> str:
    """Private precedence helper for already-validated observation states."""
    values = list(states)
    for index, state in enumerate(values):
        _runtime_state(state, OBSERVATION_STATES, f"states[{index}]")
    applicable = [state for state in values if state != "NOT_APPLICABLE"]
    if not applicable:
        return "UNAVAILABLE"
    for state in ("WORSENS", "UNAVAILABLE", "IMPROVES", "EQUIVALENT"):
        if state in applicable:
            return state
    raise RuntimeAuthorityError("closed observation reduction has no state")


def _admitted_gold_peers(data: Mapping[str, Any], evidence: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    expected_keys = (
        "peer_id", "identity_and_inception", "unresolved_required_session_gaps",
        "dividend_split_action_treatment", "overlap_total_return_correlation",
        "overlap_annualized_return_difference_pp", "overlap_max_drawdown_difference_pp",
    )
    canonical_peers = tuple(data["representations"]["FUND_GLD_DEFENSIVE"]["conditional_ids"])
    seen: list[str] = []
    admitted: list[str] = []
    for index, raw in enumerate(evidence):
        record = _runtime_mapping(raw, expected_keys, f"gold_peer_evidence[{index}]")
        peer = record["peer_id"]
        if peer not in canonical_peers or peer in seen:
            raise RuntimeAuthorityError(f"gold_peer_evidence[{index}]: unknown or duplicate peer {peer!r}")
        if canonical_peers.index(peer) < len(seen) or (seen and canonical_peers.index(peer) <= canonical_peers.index(seen[-1])):
            raise RuntimeAuthorityError("gold peer evidence must use canonical IAU, SGOL, GLDM order")
        seen.append(peer)
        if record["identity_and_inception"] not in ("COMPLETE", "INCOMPLETE"):
            raise RuntimeAuthorityError("gold identity/inception status is outside closed vocabulary")
        if record["dividend_split_action_treatment"] not in ("COMPLETE", "INCOMPLETE"):
            raise RuntimeAuthorityError("gold action-treatment status is outside closed vocabulary")
        gaps = record["unresolved_required_session_gaps"]
        if type(gaps) is not int or gaps < 0:
            raise RuntimeAuthorityError("gold unresolved gap count must be a nonnegative integer")
        passes = (
            record["identity_and_inception"] == "COMPLETE"
            and gaps == int(_param(data, "GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED"))
            and record["dividend_split_action_treatment"] == "COMPLETE"
            and _runtime_decimal(record["overlap_total_return_correlation"], "gold correlation") >= _runtime_decimal(_param(data, "GOLD_PARITY_CORRELATION_MIN"), "gold correlation minimum")
            and abs(_runtime_decimal(record["overlap_annualized_return_difference_pp"], "gold return difference")) <= _runtime_decimal(_param(data, "GOLD_PARITY_RETURN_MAX_PP"), "gold return maximum")
            and abs(_runtime_decimal(record["overlap_max_drawdown_difference_pp"], "gold drawdown difference")) <= _runtime_decimal(_param(data, "GOLD_PARITY_DRAWDOWN_MAX_PP"), "gold drawdown maximum")
        )
        if passes:
            admitted.append(peer)
    return tuple(admitted)


def _reduce_representations(
    data: Mapping[str, Any],
    family: str,
    states: Mapping[str, str],
    gold_peer_evidence: Sequence[Mapping[str, Any]] = (),
) -> str:
    """Private representation reducer; it is not an authoritative entry point."""
    if family == "FUND_BROAD_MARKET":
        required = tuple(data["representations"][family]["ids"])
        if gold_peer_evidence:
            raise RuntimeAuthorityError("gold peer evidence is invalid for broad market")
    elif family == "CRYPTO":
        required = tuple(data["representations"][family]["ids"])
        if gold_peer_evidence:
            raise RuntimeAuthorityError("gold peer evidence is invalid for crypto")
    elif family == "FUND_GLD_DEFENSIVE":
        required = ("GLD",) + _admitted_gold_peers(data, gold_peer_evidence)
    else:
        raise RuntimeAuthorityError(f"unsupported representation family {family!r}")
    mapping = _runtime_mapping(states, required, f"{family}.states")
    values = [_runtime_state(mapping[rep], FAMILY_STATES, f"{family}.{rep}") for rep in required]
    if any(value in ("UNAVAILABLE", "CONFLICT") for value in values):
        return "UNAVAILABLE" if "UNAVAILABLE" in values else "CONFLICT"
    return values[0] if len(set(values)) == 1 else "CONFLICT"


def _reduce_equity(
    data: Mapping[str, Any],
    constituent_states: Sequence[tuple[str, str]],
    leave_one_out_states: Sequence[tuple[str, str]],
) -> str:
    """Private cross-sectional reducer; all summaries are derived here."""
    if type(constituent_states) not in (list, tuple) or type(leave_one_out_states) not in (list, tuple):
        raise RuntimeAuthorityError("equity inputs must be ordered sequences")
    identities = [item[0] for item in constituent_states if type(item) in (list, tuple) and len(item) == 2]
    if len(identities) != len(constituent_states) or tuple(identities) != tuple(data["frozen_cohort"]["equity_ids"]):
        raise RuntimeAuthorityError("constituent states must contain the exact frozen 27-name cohort in canonical order")
    values: list[str] = []
    for ticker, state in constituent_states:
        values.append(_runtime_state(state, ("IMPROVES", "EQUIVALENT", "WORSENS", "UNAVAILABLE"), f"equity.{ticker}"))
    eligible = [(ticker, state) for (ticker, _), state in zip(constituent_states, values) if state != "UNAVAILABLE"]
    eligible_ids = tuple(ticker for ticker, _ in eligible)
    loo_ids = [item[0] for item in leave_one_out_states if type(item) in (list, tuple) and len(item) == 2]
    if len(loo_ids) != len(leave_one_out_states) or tuple(loo_ids) != eligible_ids:
        raise RuntimeAuthorityError("leave-one-out states must contain each eligible omitted identity exactly once in canonical order")
    loo_values = [_runtime_state(state, ("IMPROVES", "EQUIVALENT", "WORSENS", "UNAVAILABLE"), f"equity_loo.{ticker}") for ticker, state in leave_one_out_states]
    minimum = int(_param(data, "EQUITY_MINIMUM_ELIGIBLE"))
    if len(eligible) < minimum:
        return "UNAVAILABLE"
    ordered_states = ("WORSENS", "EQUIVALENT", "IMPROVES")
    ordered_values = sorted((state for _, state in eligible), key=ordered_states.index)
    center_left = ordered_values[(len(ordered_values) - 1) // 2]
    center_right = ordered_values[len(ordered_values) // 2]
    if center_left != center_right:
        return "CONFLICT"
    median_state = center_left
    counts = {state: ordered_values.count(state) for state in ordered_states}
    max_count = max(counts.values())
    winners = [state for state, count in counts.items() if count == max_count]
    if len(winners) != 1:
        return "CONFLICT"
    winner = winners[0]
    breadth = Decimal(counts[winner]) / Decimal(len(eligible))
    if breadth < _runtime_decimal(_param(data, "EQUITY_DIRECTIONAL_BREADTH"), "equity breadth"):
        return "CONFLICT"
    if median_state != winner or any(state != winner for state in loo_values):
        return "CONFLICT"
    return winner


def _directional_disposition(
    data: Mapping[str, Any],
    family_states: Mapping[str, str],
) -> str:
    """Private directional reducer for internally derived family states."""
    mapping = _runtime_mapping(family_states, VOTING_FAMILIES, "mandatory family states")
    values = [_runtime_state(mapping[family], FAMILY_STATES, f"family_states.{family}") for family in VOTING_FAMILIES]
    if any(value in ("UNAVAILABLE", "CONFLICT") for value in values):
        return "UNABLE_TO_DETERMINE"
    if "IMPROVES" in values and "WORSENS" in values:
        return "UNABLE_TO_DETERMINE"
    minimum = int(_param(data, "MINIMUM_IMPROVEMENT_FAMILIES"))
    if "WORSENS" not in values and values.count("IMPROVES") >= minimum:
        return "POLICY_REVIEW_REQUIRED"
    return "CENTER_NOT_REJECTED"


def _point_evidence(
    data: Mapping[str, Any],
    family_states: Mapping[str, str],
) -> str:
    """Private point-state reducer using the same evidence as direction."""
    mapping = _runtime_mapping(family_states, VOTING_FAMILIES, "mandatory family states")
    values = [_runtime_state(mapping[family], FAMILY_STATES, f"family_states.{family}") for family in VOTING_FAMILIES]
    directional_state = _directional_disposition(data, family_states)
    if directional_state == "POLICY_REVIEW_REQUIRED":
        return "DISPLACES_REFERENCE"
    if directional_state == "UNABLE_TO_DETERMINE":
        return "UNAVAILABLE"
    minimum_worsening = int(_param(data, data["result_reduction"]["point_evidence_rule"]["minimum_worsening_parameter_id"]))
    if values.count("WORSENS") >= minimum_worsening and "IMPROVES" not in values:
        return "ADJACENT_MATERIALLY_WORSE"
    return "NOT_DISTINGUISHED"


def _final_disposition(
    data: Mapping[str, Any],
    lower: str,
    higher: str,
    lower_point: str,
    higher_point: str,
) -> dict[str, str | None]:
    """Private pure table lookup for canonical states derived by the evaluator."""
    _runtime_state(lower, DIRECTIONAL_STATES, "lower directional state")
    _runtime_state(higher, DIRECTIONAL_STATES, "higher directional state")
    _runtime_state(lower_point, POINT_EVIDENCE_STATES, "lower point state")
    _runtime_state(higher_point, POINT_EVIDENCE_STATES, "higher point state")
    result_rows = data["result_reduction"]["total_state_table"]
    point_rows = data["result_reduction"]["point_state_table"]
    result_row = next(row for row in result_rows if row["lower"] == lower and row["higher"] == higher)
    point_row = next(row for row in point_rows if row["lower"] == lower_point and row["higher"] == higher_point)
    return {
        "result": result_row["result"],
        "review_direction": result_row["review_direction"],
        "point_target_assessment": point_row["point_target_assessment"],
        "method_review_direction": point_row["method_review_direction"],
    }


def _observation_plan(data: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    stress_windows = tuple(
        window["id"] for window in data["scenario_windows"]["windows"]
        if window["class"] == "FIXED_STRESS"
    )
    plan: list[tuple[str, str]] = []
    for metric in data["metric_families"]["metrics"]:
        if metric["voting_status"] not in ("MANDATORY_VOTING", "CONDITIONAL_VOTING"):
            continue
        for window in metric["applicable_windows"]:
            if window == "FIXED_STRESS":
                plan.extend((metric["metric_id"], window_id) for window_id in stress_windows)
            else:
                plan.append((metric["metric_id"], window))
    return tuple(plan)


def _mandatory_metric_for_family(data: Mapping[str, Any], voting_family: str) -> tuple[str, str]:
    for metric in data["metric_families"]["metrics"]:
        if metric["family"] == voting_family and metric["voting_status"] == "MANDATORY_VOTING":
            return metric["metric_id"], metric["applicable_windows"][0]
    raise RuntimeAuthorityError(f"no mandatory metric for voting family {voting_family}")


def _derive_direction(
    data: Mapping[str, Any],
    research_family: str,
    scenario_id: str,
    block: Mapping[str, Any],
    gold_peer_evidence: Sequence[Mapping[str, Any]],
    admitted_gold: Sequence[str],
) -> tuple[str, str, dict[tuple[str, str, str, str, str], tuple[str, tuple[Decimal, ...] | None]]]:
    block = _runtime_mapping(
        block,
        ("observations", "equity_leave_one_out"),
        f"directions.{scenario_id}",
    )
    if type(block["observations"]) is not list:
        raise RuntimeAuthorityError(f"directions.{scenario_id}.observations must be a list")
    if type(block["equity_leave_one_out"]) is not list:
        raise RuntimeAuthorityError(f"directions.{scenario_id}.equity_leave_one_out must be a list")
    if research_family == "FUND_GLD_DEFENSIVE":
        representations = ("GLD",) + tuple(admitted_gold)
    else:
        representations = _registered_representations(data, research_family)
    plan = _observation_plan(data)
    expected_identities = tuple(
        (scenario_id, research_family, representation, metric_id, window_id)
        for representation in representations
        for metric_id, window_id in plan
    )
    observation_keys = (
        "scenario_id", "research_family", "representation_id", "metric_id",
        "window_id", "raw_operands", "reported_candidate", "reported_reference",
        "missingness_state",
    )
    actual_identities: list[tuple[str, str, str, str, str]] = []
    metric_states: dict[str, dict[str, list[str]]] = {
        representation: {} for representation in representations
    }
    primitive_chain: dict[
        tuple[str, str, str, str, str], tuple[str, tuple[Decimal, ...] | None]
    ] = {}
    metric_lookup = {metric["metric_id"]: metric for metric in data["metric_families"]["metrics"]}
    for index, raw in enumerate(block["observations"]):
        record = _runtime_mapping(raw, observation_keys, f"directions.{scenario_id}.observations[{index}]")
        identity = (
            record["scenario_id"], record["research_family"], record["representation_id"],
            record["metric_id"], record["window_id"],
        )
        actual_identities.append(identity)
        candidate, reference, normalized_operands = _derive_formula_values(
            data,
            record["research_family"],
            record["representation_id"],
            record["scenario_id"],
            record["metric_id"],
            record["window_id"],
            record["raw_operands"],
            record["reported_candidate"],
            record["reported_reference"],
            record["missingness_state"],
        )
        state = _classify_observation(
            data,
            record["research_family"],
            record["representation_id"],
            record["scenario_id"],
            record["metric_id"],
            record["window_id"],
            candidate,
            reference,
            record["missingness_state"],
        )
        if record["research_family"] != research_family:
            raise RuntimeAuthorityError(
                f"directions.{scenario_id}.observations[{index}] research family mismatch"
            )
        if record["scenario_id"] != scenario_id:
            raise RuntimeAuthorityError(
                f"directions.{scenario_id}.observations[{index}] scenario mismatch"
            )
        if record["representation_id"] not in representations:
            raise RuntimeAuthorityError(
                f"directions.{scenario_id}.observations[{index}] uses an inactive representation"
            )
        chain_identity = (
            "OBSERVATION", record["research_family"], record["representation_id"],
            record["metric_id"], record["window_id"],
        )
        if chain_identity in primitive_chain:
            raise RuntimeAuthorityError("duplicate canonical formula observation identity")
        primitive_chain[chain_identity] = (record["missingness_state"], normalized_operands)
        metric_states[record["representation_id"]].setdefault(record["metric_id"], []).append(state)
    if tuple(actual_identities) != expected_identities:
        raise RuntimeAuthorityError(
            f"directions.{scenario_id}.observations must contain the exact canonical identity population/order"
        )

    representation_family_states: dict[str, dict[str, str]] = {}
    for representation in representations:
        voting: dict[str, list[str]] = {family: [] for family in VOTING_FAMILIES}
        for metric_id, states in metric_states[representation].items():
            applicable = [state for state in states if state != "NOT_APPLICABLE"]
            if not applicable:
                continue
            metric_state = _reduce_states(states)
            voting[metric_lookup[metric_id]["family"]].append(metric_state)
        representation_family_states[representation] = {
            family: _reduce_states(states) if states else "UNAVAILABLE"
            for family, states in voting.items()
        }

    if research_family != "EQUITY" and block["equity_leave_one_out"]:
        raise RuntimeAuthorityError("equity leave-one-out evidence is prohibited outside EQUITY")

    family_states: dict[str, str] = {}
    if research_family == "EQUITY":
        loo_keys = (
            "scenario_id", "research_family", "omitted_id", "metric_id",
            "window_id", "raw_operands", "reported_candidate", "reported_reference",
            "missingness_state",
        )
        expected_loo: list[tuple[str, str, str, str, str]] = []
        constituent_by_family: dict[str, list[tuple[str, str]]] = {}
        for voting_family in VOTING_FAMILIES:
            constituent_states = [
                (ticker, representation_family_states[ticker][voting_family])
                for ticker in representations
            ]
            constituent_by_family[voting_family] = constituent_states
            metric_id, window_id = _mandatory_metric_for_family(data, voting_family)
            expected_loo.extend(
                (scenario_id, research_family, ticker, metric_id, window_id)
                for ticker, state in constituent_states if state != "UNAVAILABLE"
            )
        loo_by_family: dict[str, list[tuple[str, str]]] = {family: [] for family in VOTING_FAMILIES}
        actual_loo: list[tuple[str, str, str, str, str]] = []
        for index, raw in enumerate(block["equity_leave_one_out"]):
            record = _runtime_mapping(raw, loo_keys, f"directions.{scenario_id}.equity_leave_one_out[{index}]")
            identity = (
                record["scenario_id"], record["research_family"], record["omitted_id"],
                record["metric_id"], record["window_id"],
            )
            actual_loo.append(identity)
            candidate, reference, normalized_operands = _derive_formula_values(
                data,
                record["research_family"],
                record["omitted_id"],
                record["scenario_id"],
                record["metric_id"],
                record["window_id"],
                record["raw_operands"],
                record["reported_candidate"],
                record["reported_reference"],
                record["missingness_state"],
            )
            state = _classify_observation(
                data,
                record["research_family"],
                record["omitted_id"],
                record["scenario_id"],
                record["metric_id"],
                record["window_id"],
                candidate,
                reference,
                record["missingness_state"],
            )
            chain_identity = (
                "EQUITY_LEAVE_ONE_OUT", record["research_family"], record["omitted_id"],
                record["metric_id"], record["window_id"],
            )
            if chain_identity in primitive_chain:
                raise RuntimeAuthorityError("duplicate equity leave-one-out formula identity")
            primitive_chain[chain_identity] = (record["missingness_state"], normalized_operands)
            voting_family = metric_lookup[record["metric_id"]]["family"]
            loo_by_family[voting_family].append((record["omitted_id"], state))
        if tuple(actual_loo) != tuple(expected_loo):
            raise RuntimeAuthorityError(
                f"directions.{scenario_id}.equity_leave_one_out must contain the exact derived population/order"
            )
        family_states = {
            family: _reduce_equity(data, constituent_by_family[family], loo_by_family[family])
            for family in VOTING_FAMILIES
        }
    else:
        for voting_family in VOTING_FAMILIES:
            states = {
                representation: representation_family_states[representation][voting_family]
                for representation in representations
            }
            family_states[voting_family] = _reduce_representations(
                data,
                research_family,
                states,
                gold_peer_evidence if research_family == "FUND_GLD_DEFENSIVE" else (),
            )

    directional = _directional_disposition(data, family_states)
    point = _point_evidence(data, family_states)
    return directional, point, primitive_chain


def evaluate_study_evidence(raw_evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Authoritative RISK-0001 evidence-to-final-result production entry point.

    The exact caller contract contains primitive observations only.  Derived family,
    directional, point, admission, breadth, median, monotonicity, integrity, and
    final states are intentionally absent and are recomputed under pinned authority.
    """
    data = _runtime_authority()
    root = _runtime_mapping(
        raw_evidence,
        ("study_id", "research_family", "gold_peer_evidence", "directions"),
        "raw_evidence",
    )
    if root["study_id"] != data["study_id"]:
        raise RuntimeAuthorityError(f"unknown study_id {root['study_id']!r}")
    research_family = root["research_family"]
    if research_family not in FAMILIES:
        raise RuntimeAuthorityError(f"unknown research_family {research_family!r}")
    if type(root["gold_peer_evidence"]) is not list:
        raise RuntimeAuthorityError("gold_peer_evidence must be a list")
    if research_family != "FUND_GLD_DEFENSIVE" and root["gold_peer_evidence"]:
        raise RuntimeAuthorityError("gold_peer_evidence is prohibited outside FUND_GLD_DEFENSIVE")
    admitted_gold = _admitted_gold_peers(data, root["gold_peer_evidence"])
    directions = _runtime_mapping(root["directions"], ("LOWER", "HIGHER"), "directions")
    derived = {
        scenario: _derive_direction(
            data,
            research_family,
            scenario,
            directions[scenario],
            root["gold_peer_evidence"],
            admitted_gold,
        )
        for scenario in ("LOWER", "HIGHER")
    }
    lower_direction, lower_point, lower_chain = derived["LOWER"]
    higher_direction, higher_point, higher_chain = derived["HIGHER"]
    if lower_chain != higher_chain:
        raise RuntimeAuthorityError(
            "LOWER and HIGHER must use the same canonical primitive path and missingness evidence"
        )
    final = _final_disposition(
        data,
        lower_direction,
        higher_direction,
        lower_point,
        higher_point,
    )
    return {
        "study_id": data["study_id"],
        "research_family": research_family,
        "directional_states": {"LOWER": lower_direction, "HIGHER": higher_direction},
        "point_states": {"LOWER": lower_point, "HIGHER": higher_point},
        **final,
    }


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
