"""Closed validator for LEVEL2-0001's selection-only research cohort freeze.

The YAML artifact is the sole authority-bearing cohort record.  This module
therefore validates exact populations and closed vocabularies rather than
trying to infer policy meaning from prose.  It is read-only and has no import
coupling to allocation, margin, holdings, targets, or brokerage code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parent
ARTIFACT_PATH = Path("governance/evidence/LEVEL2-0001/RESEARCH_COHORT_FREEZE.yaml")
SCHEMA_VERSION = "1.0"
DECISION_ID = "LEVEL2-0001"
SOURCE_COMMIT_SHA = "013c7ab5e10c8007af0d47822c6888771b594f2e"

DISPOSITIONS = (
    "RESEARCH_COHORT_INCLUDED",
    "CONDITIONAL",
    "ABSTAIN_INSUFFICIENT_EVIDENCE",
    "EXCLUDED_FROM_CURRENT_RESEARCH_COHORT",
)

REASON_CODES = (
    "CLOSED_GOVERNED_EQUITY_EVIDENCE_POPULATION",
    "ASSET_APPROPRIATE_GOVERNED_EVIDENCE_AVAILABLE",
    "CONTENDER_PILOT_ONLY",
    "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY",
    "FRESHNESS_REVIEW_REQUIRED",
    "GOVERNED_PARITY_NOT_REACHED",
    "RESEARCH_NOT_YET_AUTHORIZED",
    "GOVERNED_DEFERMENT_OR_EXCLUSION",
    "BENCHMARK_ONLY",
    "NON_INVESTABLE_ACCOUNTING_ROW",
    "UNIDENTIFIED_LEGACY_POPULATION",
)

CAVEAT_CODES = (
    "CURRENT_MEMBERSHIP_NOT_EVIDENCE",
    "CURRENT_HOLDING_NOT_EVIDENCE",
    "CURRENT_CONFIGURATION_NOT_EVIDENCE",
    "PARTIAL_VALUATION_GAPS_PRESERVED",
    "FRESHNESS_AND_ACCESS_GAPS_PRESERVED",
    "SPGI_NO_POLICY_CONCLUSION_PRESERVED",
    "LEGACY_COMPLETENESS_GAP_PRESERVED",
    "NONCANONICAL_POPULATION_PRESERVED",
    "DOMESTIC_BETA_DUPLICATION_DISCLOSED",
    "DEVELOPED_EX_US_DISTINCTION_DISCLOSED",
    "EMERGING_MARKET_DISTINCTION_DISCLOSED",
    "FINAL_VEHICLE_UNRESOLVED",
    "MIXED_HISTORICAL_PROTECTION_EVIDENCE",
    "ELEVATED_COST_VS_NAMED_PEERS",
    "CROSS_COIN_CORRELATION_UNRESOLVED",
    "SOL_DRAWDOWN_EVIDENCE_ABSTENTION",
    "INTERNAL_WEIGHTING_METHOD_UNRESOLVED",
    "PILOT_NOT_CAPITAL_PRIORITY_AUTHORITY",
    "NORMALIZED_IDENTITY_UNRESOLVED",
)

PRESERVATION_ASSERTIONS = (
    "CURRENT_MEMBERSHIP_NOT_EVIDENCE",
    "CURRENT_HOLDING_NOT_EVIDENCE",
    "CURRENT_CONFIGURATION_NOT_EVIDENCE",
    "PARTIAL_VALUATION_GAPS_PRESERVED",
    "FRESHNESS_AND_ACCESS_GAPS_PRESERVED",
    "SPGI_NO_POLICY_CONCLUSION_PRESERVED",
    "LEGACY_COMPLETENESS_GAP_PRESERVED",
    "NONCANONICAL_POPULATION_PRESERVED",
)

AUTHORITY_BOUNDARY = {
    "research_examination": "PERMITTED",
    "final_portfolio_membership": "NOT_ESTABLISHED",
    "level2_selection_policy": "NOT_ESTABLISHED",
    "instrument_sizing": "NOT_ESTABLISHED",
    "capital_priority": "NOT_ESTABLISHED",
    "current_portfolio_configuration": "UNCHANGED",
    "transaction_authority": "PROHIBITED",
    "backtest_authority": "SEPARATE_AUTHORIZATION_REQUIRED",
    "portfolio_adoption": "PROHIBITED",
}

EQUITIES = (
    "AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GNRC", "GOOGL",
    "ICE", "ISRG", "KLAC", "LLY", "META", "MSFT", "NVDA", "PANW", "PWR",
    "RKLB", "RTX", "SNPS", "SPGI", "TMO", "TSLA", "TSM", "V", "WM",
)
BROAD_MARKET = ("SPY", "VEA", "VWO")
DEFENSIVE = ("GLD",)
CRYPTO = ("BTC", "ETH", "SOL")
CORE = EQUITIES + BROAD_MARKET + DEFENSIVE + CRYPTO

ABSTAINED = {
    "AAPL": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "ABBV": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "AMAT": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "AMD": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "BRK.B": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "CRM": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "CRWD": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "CVX": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "GILD": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "IBM": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "INTC": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "JNJ": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "JPM": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "LRCX": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "MA": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "MLM": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "MRK": ("FRESHNESS_REVIEW_REQUIRED", "requires_freshness_review"),
    "MRVL": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "MU": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "NOW": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "ORCL": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "SKHY": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "SNDK": ("RESEARCH_NOT_YET_AUTHORIZED", "requires_research"),
    "WDC": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
    "XOM": ("GOVERNED_PARITY_NOT_REACHED", "evaluation_ready"),
}

EXCLUDED = {
    "BABA": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "BONK": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "CAT": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "CASH": ("NON_INVESTABLE_ACCOUNTING_ROW", "synthetic_or_test_fixture"),
    "DELL": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "DHR": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "EQIX": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "HOOD": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "HYPE": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "LHX": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "NFLX": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "PEPE": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "PLTR": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "QQQ": ("BENCHMARK_ONLY", "benchmark_or_index"),
    "RESERVE": ("NON_INVESTABLE_ACCOUNTING_ROW", "synthetic_or_test_fixture"),
    "SHOP": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "SPCX": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "SYK": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "UBER": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "UNH": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "VMC": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "WIF": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
    "ZORA": ("GOVERNED_DEFERMENT_OR_EXCLUSION", "explicitly_deferred_or_excluded"),
}

CONDITIONAL = {
    "VRT": ("VRT", None, "EQUITY", "CONTENDER_PILOT_ONLY"),
    "WMT": ("WMT", None, "EQUITY", "CONTENDER_PILOT_ONLY"),
    "IAU": ("IAU", None, "DEFENSIVE_FUND", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "SGOL": ("SGOL", None, "DEFENSIVE_FUND", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "GLDM": ("GLDM", None, "DEFENSIVE_FUND", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "SPY_PEER_VANGUARD_SP500_ETF": (None, "Vanguard's S&P 500 ETF", "BROAD_MARKET_FUND_REFERENCE", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "SPY_PEER_ISHARES_CORE_SP500_ETF": (None, "iShares Core S&P 500 ETF", "BROAD_MARKET_FUND_REFERENCE", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "VEA_PEER_ISHARES_CORE_MSCI_EAFE_ETF": (None, "iShares Core MSCI EAFE ETF", "BROAD_MARKET_FUND_REFERENCE", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "VEA_PEER_SCHWAB_INTERNATIONAL_EQUITY_ETF": (None, "Schwab International Equity ETF", "BROAD_MARKET_FUND_REFERENCE", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "VWO_PEER_ISHARES_CORE_MSCI_EMERGING_MARKETS_ETF": (None, "iShares Core MSCI Emerging Markets ETF", "BROAD_MARKET_FUND_REFERENCE", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
    "VWO_PEER_SCHWAB_EMERGING_MARKETS_EQUITY_ETF": (None, "Schwab Emerging Markets Equity ETF", "BROAD_MARKET_FUND_REFERENCE", "NAMED_CATEGORY_PEER_LACKS_GOVERNED_PARITY"),
}

EQUITY_CAVEATS = (
    "CURRENT_MEMBERSHIP_NOT_EVIDENCE",
    "CURRENT_HOLDING_NOT_EVIDENCE",
    "CURRENT_CONFIGURATION_NOT_EVIDENCE",
    "PARTIAL_VALUATION_GAPS_PRESERVED",
    "FRESHNESS_AND_ACCESS_GAPS_PRESERVED",
)
EQUITY_EVIDENCE_REFS = (
    "equity_classification_manifest",
    "equity_valuation_archetype_manifest",
    "equity_valuation_evidence_manifest",
    "equity_valuation_results_manifest",
)
BROAD_MARKET_EVIDENCE_REFS = (
    "etf_classification_manifest",
    "instrument_economic_assessment_manifest",
)
CRYPTO_CAVEATS = (
    "CROSS_COIN_CORRELATION_UNRESOLVED",
    "INTERNAL_WEIGHTING_METHOD_UNRESOLVED",
)
CRYPTO_EVIDENCE_REFS = (
    "crypto_classification_manifest",
    "instrument_economic_assessment_manifest",
)

# Exact row-level authority is expressed through the smallest governed
# archetypes, then expanded across every identity.  This is intentionally not a
# copy of the artifact: the checked-in YAML must reconcile to these independent
# deterministic expectations before it can act as closed authority.
CORE_ROW_AUTHORITY = {
    **{ticker: (EQUITY_CAVEATS, EQUITY_EVIDENCE_REFS) for ticker in EQUITIES if ticker != "SPGI"},
    "SPGI": (
        EQUITY_CAVEATS + ("SPGI_NO_POLICY_CONCLUSION_PRESERVED",),
        EQUITY_EVIDENCE_REFS + ("equity_recommendation_package",),
    ),
    "SPY": (
        ("DOMESTIC_BETA_DUPLICATION_DISCLOSED", "FINAL_VEHICLE_UNRESOLVED"),
        BROAD_MARKET_EVIDENCE_REFS,
    ),
    "VEA": (
        ("DEVELOPED_EX_US_DISTINCTION_DISCLOSED", "FINAL_VEHICLE_UNRESOLVED"),
        BROAD_MARKET_EVIDENCE_REFS,
    ),
    "VWO": (
        ("EMERGING_MARKET_DISTINCTION_DISCLOSED", "FINAL_VEHICLE_UNRESOLVED"),
        BROAD_MARKET_EVIDENCE_REFS,
    ),
    "GLD": (
        (
            "MIXED_HISTORICAL_PROTECTION_EVIDENCE",
            "ELEVATED_COST_VS_NAMED_PEERS",
            "FINAL_VEHICLE_UNRESOLVED",
        ),
        (
            "etf_classification_manifest",
            "functional_doctrine_manifest",
            "gld_economic_assessment_manifest",
        ),
    ),
    "BTC": (CRYPTO_CAVEATS, CRYPTO_EVIDENCE_REFS),
    "ETH": (CRYPTO_CAVEATS, CRYPTO_EVIDENCE_REFS),
    "SOL": (
        (
            "CROSS_COIN_CORRELATION_UNRESOLVED",
            "SOL_DRAWDOWN_EVIDENCE_ABSTENTION",
            "INTERNAL_WEIGHTING_METHOD_UNRESOLVED",
        ),
        CRYPTO_EVIDENCE_REFS,
    ),
}

CONDITIONAL_ROW_AUTHORITY = {
    **{
        candidate: (
            ("PILOT_NOT_CAPITAL_PRIORITY_AUTHORITY",),
            ("contender_evaluation_manifest",),
        )
        for candidate in ("VRT", "WMT")
    },
    **{
        candidate: (
            ("FINAL_VEHICLE_UNRESOLVED",),
            ("gld_economic_assessment_manifest",),
        )
        for candidate in ("IAU", "SGOL", "GLDM")
    },
    **{
        candidate: (
            ("NORMALIZED_IDENTITY_UNRESOLVED", "FINAL_VEHICLE_UNRESOLVED"),
            ("instrument_economic_assessment_manifest",),
        )
        for candidate in tuple(CONDITIONAL)[5:]
    },
}

SOURCE_PINS = {
    "equity_classification_manifest": ("intelligence/classification/COHORT_MANIFEST.yaml", "c6fa21b25ff0b45d3f0ed578cd003fc679ff0f216b97f126498594b0cbca2e79"),
    "equity_valuation_archetype_manifest": ("intelligence/valuation_archetype/COHORT_MANIFEST.yaml", "754821895934a956633022014054a8e7f0355c4adc91ca3aadeb8d5bce438da3"),
    "equity_valuation_evidence_manifest": ("intelligence/valuation_evidence/COHORT_MANIFEST.yaml", "2498650ac6c671b418a566c1692e99a2cbe2306703d2c2427ad9df06a8c1926b"),
    "equity_valuation_results_manifest": ("intelligence/valuation_results/COHORT_MANIFEST.yaml", "2f402e3c20b4ecc83d30cae2eb389c82ccba4c2a5ebf1a0d00e8cb15cf8be85f"),
    "equity_recommendation_package": ("intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml", "84e65c40065cf678ad373d899014fddc0737fdba3b4c915a6f3cab7f28fc7752"),
    "etf_classification_manifest": ("intelligence/etf_classification/COHORT_MANIFEST.yaml", "d82238d80533a554f080aee6523f6d10ebb65baadd9fb0af5f16ffac0a06144c"),
    "crypto_classification_manifest": ("intelligence/crypto_classification/COHORT_MANIFEST.yaml", "332ba25c5d6ad06bc9180a38b98fa762379f784bb5fe3f58b1f57d872715139b"),
    "gld_economic_assessment_manifest": ("intelligence/economic_assessment/COHORT_MANIFEST.yaml", "6a46b40ca0287c1a2ebe56725ab64fb13af3fd5f184015dd005400be060dfc58"),
    "instrument_economic_assessment_manifest": ("intelligence/instrument_economic_assessment/COHORT_MANIFEST.yaml", "50646995bc0062ef41c3222f2f23df7b5b41141fa21cf00c31a642caeddc6826"),
    "contender_evaluation_manifest": ("intelligence/contender_evaluation/COHORT_MANIFEST.yaml", "5b5c5cbec2d9506cbeaa1320fef3f69a6632217b528b0ab68a1dffa9d466822b"),
    "contender_registry": ("intelligence/contenders/registry.yaml", "e534989e100c881213548331dae820172b513b2016db20d8df0a23c799c75c9a"),
    "functional_doctrine_manifest": ("intelligence/functional_doctrine/COHORT_MANIFEST.yaml", "ae2573c98f4b24ff5a9d9e4d869b1a253aef979626a75269a80adc7abb2e79bf"),
}

REFREEZE_TRIGGERS = (
    "MATERIAL_POPULATION_CHANGE",
    "NORMALIZED_SAME_ROLE_ALTERNATIVE_REACHES_EQUIVALENT_EVIDENCE",
    "MATERIAL_FRESHNESS_OR_ACCESS_CORRECTION",
    "CANDIDATE_REACHES_GOVERNED_PARITY",
    "PINNED_SOURCE_HASH_CHANGE",
    "FINAL_LEVEL2_MEMBERSHIP_DECISION",
)

TOP_LEVEL_KEYS = {
    "schema_version", "decision_id", "freeze_status", "authority_scope",
    "source_commit_sha", "authority_boundary", "disposition_vocabulary",
    "reason_code_vocabulary", "caveat_code_vocabulary", "preservation_assertions",
    "cohort_summary", "core_cohort", "conditional_sidecar", "abstained_population",
    "excluded_population", "source_pins", "refreeze_triggers",
}
CORE_ROW_KEYS = {"instrument_id", "sleeve", "disposition", "reason_code", "caveat_codes", "evidence_refs"}
CONDITIONAL_ROW_KEYS = {"candidate_id", "normalized_instrument_id", "source_label", "asset_type", "disposition", "reason_code", "caveat_codes", "evidence_refs"}
REGISTRY_ROW_KEYS = {"instrument_id", "disposition", "reason_code", "source_registry_disposition", "evidence_refs"}
PIN_KEYS = {"pin_id", "source_path", "hash_method", "sha256"}


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def _ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    return [row[key] for row in rows if isinstance(row, dict) and isinstance(row.get(key), str)]


def _check_exact_keys(value: Any, expected: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return
    actual = set(value)
    if actual != expected:
        errors.append(f"{label} keys mismatch: expected {sorted(expected)}, got {sorted(actual)}")


def _check_canonical_list(
    value: Any,
    expected: tuple[str, ...],
    allowed: tuple[str, ...] | dict[str, Any],
    label: str,
    errors: list[str],
) -> None:
    """Enforce type, closure, cardinality, uniqueness, values, and order."""
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return
    all_strings = all(isinstance(item, str) for item in value)
    if not all_strings:
        errors.append(f"{label} must contain only string values")
    else:
        unknown = [item for item in value if item not in allowed]
        if unknown:
            errors.append(f"{label} contains values outside the closed vocabulary: {unknown}")
        if len(value) != len(set(value)):
            errors.append(f"{label} contains duplicate values")
    if len(value) != len(expected):
        errors.append(f"{label} cardinality must equal {len(expected)}")
    if value != list(expected):
        errors.append(f"{label} must equal the exact canonical values and order")


def _walk(value: Any, path: str = ""):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from _walk(child, f"{path}[{idx}]")


def _manifest_ids(repo_root: Path, relative_path: str, id_key: str) -> set[str]:
    data = yaml.safe_load((repo_root / relative_path).read_text(encoding="utf-8"))
    return {row[id_key] for row in data["cohort"]}


def validate_data(data: Any, *, repo_root: Path = REPO_ROOT, verify_sources: bool = True) -> ValidationResult:
    errors: list[str] = []
    _check_exact_keys(data, TOP_LEVEL_KEYS, "top-level", errors)
    if not isinstance(data, dict):
        return ValidationResult(tuple(errors))

    exact_scalars = {
        "schema_version": SCHEMA_VERSION,
        "decision_id": DECISION_ID,
        "freeze_status": "RESEARCH_COHORT_FROZEN",
        "authority_scope": "SELECTION_ONLY_RESEARCH_COHORT",
        "source_commit_sha": SOURCE_COMMIT_SHA,
    }
    for key, expected in exact_scalars.items():
        if data.get(key) != expected:
            errors.append(f"{key} must equal {expected!r}")
    if data.get("authority_boundary") != AUTHORITY_BOUNDARY:
        errors.append("authority_boundary must equal the closed LEVEL2-0001 non-authorization boundary")
    for key, expected in (
        ("disposition_vocabulary", DISPOSITIONS),
        ("reason_code_vocabulary", REASON_CODES),
        ("caveat_code_vocabulary", CAVEAT_CODES),
        ("preservation_assertions", PRESERVATION_ASSERTIONS),
        ("refreeze_triggers", REFREEZE_TRIGGERS),
    ):
        if data.get(key) != list(expected):
            errors.append(f"{key} must equal the closed canonical order")

    expected_summary = {
        "core_total": 34, "equity_total": 27, "broad_market_total": 3,
        "defensive_total": 1, "crypto_total": 3, "conditional_total": 11,
        "named_abstention_total": 25, "excluded_total": 23,
    }
    if data.get("cohort_summary") != expected_summary:
        errors.append("cohort_summary must equal the mechanically derived population counts")

    core = data.get("core_cohort")
    if not isinstance(core, list):
        errors.append("core_cohort must be a list")
        core = []
    for idx, row in enumerate(core):
        _check_exact_keys(row, CORE_ROW_KEYS, f"core_cohort[{idx}]", errors)
    core_rows = [row for row in core if isinstance(row, dict)]
    core_ids = _ids(core, "instrument_id")
    if core_ids != list(CORE):
        errors.append("core_cohort must contain the exact 34 identities in canonical order")
    if len(core_ids) != len(set(core_ids)):
        errors.append("core_cohort contains duplicate identities")
    expected_sleeves = {**{x: "EQUITY" for x in EQUITIES}, **{x: "BROAD_MARKET" for x in BROAD_MARKET}, "GLD": "DEFENSIVE", **{x: "CRYPTO" for x in CRYPTO}}
    for row in core_rows:
        ticker = row.get("instrument_id")
        if not isinstance(ticker, str):
            errors.append("core row instrument_id must be a string")
            continue
        if row.get("sleeve") != expected_sleeves.get(ticker):
            errors.append(f"{ticker}: incorrect sleeve")
        if row.get("disposition") != "RESEARCH_COHORT_INCLUDED":
            errors.append(f"{ticker}: core disposition must be RESEARCH_COHORT_INCLUDED")
        expected_reason = "CLOSED_GOVERNED_EQUITY_EVIDENCE_POPULATION" if ticker in EQUITIES else "ASSET_APPROPRIATE_GOVERNED_EVIDENCE_AVAILABLE"
        if row.get("reason_code") != expected_reason:
            errors.append(f"{ticker}: incorrect inclusion reason")
        authority = CORE_ROW_AUTHORITY.get(ticker)
        if authority is None:
            errors.append(f"{ticker}: no canonical row authority exists")
        else:
            expected_caveats, expected_refs = authority
            _check_canonical_list(
                row.get("caveat_codes"), expected_caveats, CAVEAT_CODES,
                f"{ticker}: caveat_codes", errors,
            )
            _check_canonical_list(
                row.get("evidence_refs"), expected_refs, SOURCE_PINS,
                f"{ticker}: evidence_refs", errors,
            )
    by_core = {row["instrument_id"]: row for row in core_rows if isinstance(row.get("instrument_id"), str)}
    spgi_caveats = by_core.get("SPGI", {}).get("caveat_codes")
    if not isinstance(spgi_caveats, list) or "SPGI_NO_POLICY_CONCLUSION_PRESERVED" not in spgi_caveats:
        errors.append("SPGI must preserve its no_policy_conclusion caveat")
    sol_caveats = by_core.get("SOL", {}).get("caveat_codes")
    if not isinstance(sol_caveats, list) or "SOL_DRAWDOWN_EVIDENCE_ABSTENTION" not in sol_caveats:
        errors.append("SOL must preserve its drawdown-evidence abstention")
    for ticker in CRYPTO:
        caveats = by_core.get(ticker, {}).get("caveat_codes")
        required = ("CROSS_COIN_CORRELATION_UNRESOLVED", "INTERNAL_WEIGHTING_METHOD_UNRESOLVED")
        if not isinstance(caveats, list) or any(caveat not in caveats for caveat in required):
            errors.append(f"{ticker}: unresolved crypto correlation/internal weighting caveats missing")

    conditional = data.get("conditional_sidecar")
    if not isinstance(conditional, list):
        errors.append("conditional_sidecar must be a list")
        conditional = []
    for idx, row in enumerate(conditional):
        _check_exact_keys(row, CONDITIONAL_ROW_KEYS, f"conditional_sidecar[{idx}]", errors)
    conditional_rows = [row for row in conditional if isinstance(row, dict)]
    conditional_ids = _ids(conditional, "candidate_id")
    if conditional_ids != list(CONDITIONAL):
        errors.append("conditional_sidecar must contain the exact 11 candidates in canonical order")
    for row in conditional_rows:
        cid = row.get("candidate_id")
        if not isinstance(cid, str):
            errors.append("conditional row candidate_id must be a string")
            continue
        expected = CONDITIONAL.get(cid)
        observed = (row.get("normalized_instrument_id"), row.get("source_label"), row.get("asset_type"), row.get("reason_code"))
        if observed != expected:
            errors.append(f"{cid}: conditional identity/type/reason does not match the governed source representation")
        if row.get("disposition") != "CONDITIONAL":
            errors.append(f"{cid}: disposition must remain CONDITIONAL")
        authority = CONDITIONAL_ROW_AUTHORITY.get(cid)
        if authority is None:
            errors.append(f"{cid}: no canonical conditional row authority exists")
        else:
            expected_caveats, expected_refs = authority
            _check_canonical_list(
                row.get("caveat_codes"), expected_caveats, CAVEAT_CODES,
                f"{cid}: conditional caveat_codes", errors,
            )
            _check_canonical_list(
                row.get("evidence_refs"), expected_refs, SOURCE_PINS,
                f"{cid}: conditional evidence_refs", errors,
            )

    abstained = data.get("abstained_population")
    _check_exact_keys(abstained, {"named_instruments", "legacy_population"}, "abstained_population", errors)
    named = abstained.get("named_instruments", []) if isinstance(abstained, dict) else []
    if not isinstance(named, list):
        errors.append("abstained_population.named_instruments must be a list")
        named = []
    for idx, row in enumerate(named):
        _check_exact_keys(row, REGISTRY_ROW_KEYS, f"abstained_population.named_instruments[{idx}]", errors)
    named_rows = [row for row in named if isinstance(row, dict)]
    if _ids(named, "instrument_id") != list(ABSTAINED):
        errors.append("named abstentions must contain the exact 25 identities in canonical order")
    for row in named_rows:
        ticker = row.get("instrument_id")
        if not isinstance(ticker, str):
            errors.append("named abstention instrument_id must be a string")
            continue
        if (row.get("reason_code"), row.get("source_registry_disposition")) != ABSTAINED.get(ticker):
            errors.append(f"{ticker}: abstention reason/source disposition mismatch")
        if row.get("disposition") != "ABSTAIN_INSUFFICIENT_EVIDENCE" or row.get("evidence_refs") != ["contender_registry"]:
            errors.append(f"{ticker}: abstention envelope mismatch")
    expected_legacy = {
        "population_id": "PRE_PHQ_2026_02_UNIDENTIFIED_LEGACY",
        "disposition": "ABSTAIN_INSUFFICIENT_EVIDENCE",
        "reason_code": "UNIDENTIFIED_LEGACY_POPULATION",
        "reported_count_class": "APPROXIMATELY_41",
        "recovery_status": "UNAVAILABLE_IN_CURRENT_CLONE",
        "evidence_refs": ["contender_registry"],
    }
    if not isinstance(abstained, dict) or abstained.get("legacy_population") != expected_legacy:
        errors.append("legacy_population must preserve the closed approximately-41 abstention")

    excluded = data.get("excluded_population")
    if not isinstance(excluded, list):
        errors.append("excluded_population must be a list")
        excluded = []
    for idx, row in enumerate(excluded):
        _check_exact_keys(row, REGISTRY_ROW_KEYS, f"excluded_population[{idx}]", errors)
    excluded_rows = [row for row in excluded if isinstance(row, dict)]
    if _ids(excluded, "instrument_id") != list(EXCLUDED):
        errors.append("excluded_population must contain the exact 23 identities in canonical order")
    for row in excluded_rows:
        ticker = row.get("instrument_id")
        if not isinstance(ticker, str):
            errors.append("excluded instrument_id must be a string")
            continue
        if (row.get("reason_code"), row.get("source_registry_disposition")) != EXCLUDED.get(ticker):
            errors.append(f"{ticker}: exclusion reason/source disposition mismatch")
        if row.get("disposition") != "EXCLUDED_FROM_CURRENT_RESEARCH_COHORT" or row.get("evidence_refs") != ["contender_registry"]:
            errors.append(f"{ticker}: current-freeze exclusion envelope mismatch")

    population_sets = [set(core_ids), {"VRT", "WMT"}, set(_ids(named, "instrument_id")), set(_ids(excluded, "instrument_id"))]
    for i, left in enumerate(population_sets):
        for right in population_sets[i + 1:]:
            if left & right:
                errors.append(f"population overlap: {sorted(left & right)}")
    if {"QQQ", "CASH", "RESERVE"} & set(core_ids):
        errors.append("QQQ/CASH/RESERVE may not enter the core research cohort")

    pins = data.get("source_pins")
    if not isinstance(pins, list):
        errors.append("source_pins must be a list")
        pins = []
    for idx, row in enumerate(pins):
        _check_exact_keys(row, PIN_KEYS, f"source_pins[{idx}]", errors)
    pin_rows = [row for row in pins if isinstance(row, dict)]
    if _ids(pins, "pin_id") != list(SOURCE_PINS):
        errors.append("source_pins must contain the exact canonical pin set and order")
    for row in pin_rows:
        pin_id = row.get("pin_id")
        if not isinstance(pin_id, str):
            errors.append("source pin pin_id must be a string")
            continue
        expected = SOURCE_PINS.get(pin_id)
        if expected and (row.get("source_path"), row.get("sha256")) != expected:
            errors.append(f"{pin_id}: source path/hash pin mismatch")
        if row.get("hash_method") != "SHA256_FILE_BYTES":
            errors.append(f"{pin_id}: hash_method must be SHA256_FILE_BYTES")
        if verify_sources and expected:
            path = repo_root / expected[0]
            if not path.is_file():
                errors.append(f"{pin_id}: pinned source missing: {expected[0]}")
            elif sha256(path.read_bytes()).hexdigest() != row.get("sha256"):
                errors.append(f"{pin_id}: live source hash does not reconcile")

    for path, value in _walk(data):
        if isinstance(value, float):
            errors.append(f"{path}: floating-point values are prohibited")
        if isinstance(value, str) and re.search(r"\d+(?:\.\d+)?%", value):
            errors.append(f"{path}: percentage-shaped strings are prohibited")
        if isinstance(value, dict):
            for key in value:
                lowered = str(key).lower()
                if any(token in lowered for token in ("target", "weight", "rank", "score", "percentage", "pct")):
                    errors.append(f"{path or 'top-level'}: prohibited sizing/ranking key {key!r}")

    if verify_sources:
        manifest_checks = (
            ("intelligence/classification/COHORT_MANIFEST.yaml", "ticker", set(EQUITIES)),
            ("intelligence/valuation_archetype/COHORT_MANIFEST.yaml", "ticker", set(EQUITIES)),
            ("intelligence/valuation_evidence/COHORT_MANIFEST.yaml", "ticker", set(EQUITIES)),
            ("intelligence/valuation_results/COHORT_MANIFEST.yaml", "ticker", set(EQUITIES)),
            ("intelligence/etf_classification/COHORT_MANIFEST.yaml", "instrument_id", {"GLD", "SPY", "VEA", "VWO"}),
            ("intelligence/crypto_classification/COHORT_MANIFEST.yaml", "instrument_id", set(CRYPTO)),
            ("intelligence/economic_assessment/COHORT_MANIFEST.yaml", "analytical_subject", {"GLD", "CASH_LIKE_CAPITAL"}),
            ("intelligence/instrument_economic_assessment/COHORT_MANIFEST.yaml", "instrument_id", {"SPY", "VEA", "VWO", "BTC", "ETH", "SOL"}),
            ("intelligence/contender_evaluation/COHORT_MANIFEST.yaml", "contender_symbol", {"VRT", "WMT"}),
        )
        for path, key, expected in manifest_checks:
            try:
                observed = _manifest_ids(repo_root, path, key)
            except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
                errors.append(f"{path}: unable to reconcile manifest identities: {exc}")
            else:
                if observed != expected:
                    errors.append(f"{path}: governed manifest population mismatch")
        try:
            registry = yaml.safe_load((repo_root / "intelligence/contenders/registry.yaml").read_text(encoding="utf-8"))
            registry_map = {row["canonical_symbol"]: row["primary_disposition"] for row in registry["entries"]}
        except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
            errors.append(f"contender registry reconciliation failed: {exc}")
        else:
            represented = set(core_ids) | {"VRT", "WMT"} | set(ABSTAINED) | set(EXCLUDED)
            if set(registry_map) != represented:
                errors.append("the 84-name contender registry is not exactly dispositioned by the freeze")
            for ticker, (_, source_disposition) in {**ABSTAINED, **EXCLUDED}.items():
                if registry_map.get(ticker) != source_disposition:
                    errors.append(f"{ticker}: live registry disposition changed")

    return ValidationResult(tuple(errors))


def validate_file(path: Path | None = None, *, repo_root: Path = REPO_ROOT) -> ValidationResult:
    artifact = path or (repo_root / ARTIFACT_PATH)
    try:
        data = yaml.safe_load(artifact.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return ValidationResult((f"unable to load {artifact}: {exc}",))
    return validate_data(data, repo_root=repo_root, verify_sources=True)


def main() -> int:
    result = validate_file()
    if result.valid:
        print("OK (34 core; 11 conditional; 25 named abstentions; 23 excluded)")
        return 0
    for error in result.errors:
        print(f"ERROR: {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
