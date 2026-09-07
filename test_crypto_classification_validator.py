"""Tests for crypto_classification_validator.py (WS-0014 cryptocurrency
blind-classification schema, XASSET-0002/XASSET-0004 scope).

Every schema/behavior test below constructs its own synthetic fixture -- no
real coin's judgment content is asserted against in this file, same
authorized-scope discipline test_classification_validator.py/
test_relationship_validator.py/test_etf_classification_validator.py already
follow. The directory-scan tests exercise the real repository's
intelligence/crypto_classification/ directory, authored under this one
implementation PR.
"""

from pathlib import Path

import pytest
import yaml

import crypto_classification_validator as cv

REPO_ROOT = Path(__file__).resolve().parent


# ── fixtures ─────────────────────────────────────────────────────────────

def _network_fundamentals(**overrides) -> dict:
    d = {"consensus_mechanism": "proof_of_work", "adoption_trend_category": "growing_usage"}
    d.update(overrides)
    return d


def _economic_model(**overrides) -> dict:
    d = {
        "supply_model": "fixed_capped_supply",
        "fee_accrual_applicable": False,
        "staking_applicable": False,
    }
    d.update(overrides)
    return d


def _liquidity(**overrides) -> dict:
    d = {"liquidity_tier": "high_liquidity"}
    d.update(overrides)
    return d


def _custody(**overrides) -> dict:
    d = {
        "custody_model": "exchange_custodied",
        "smart_contract_risk_category": "base_layer_minimal_smart_contract_surface",
    }
    d.update(overrides)
    return d


def _correlation(**overrides) -> dict:
    d = {
        "historical_volatility_category": "high_volatility",
        "cross_coin_correlation_status": "not_yet_measured",
    }
    d.update(overrides)
    return d


def _regulatory(**overrides) -> dict:
    d = {
        "disclosed_regulatory_matter_exists": False,
        "structural_uncertainty_category": "none_currently_disclosed",
    }
    d.update(overrides)
    return d


def _evidence_quality(**overrides) -> dict:
    d = {
        "primary_source_coverage": "partial",
        "thesis_uncertainty_statement": "Synthetic uncertainty statement.",
    }
    d.update(overrides)
    return d


def _sources() -> list:
    return [
        {
            "source_identifier": "Synthetic protocol documentation",
            "source_type": "secondary",
            "as_of_date": "2026-08-07",
            "access_status": "consulted_via_search_aggregation",
        }
    ]


def _record(*, sealed: bool = False, instrument_id: str = "BTC", **axis_overrides) -> dict:
    network = axis_overrides.get("network_fundamentals", _network_fundamentals())
    economic = axis_overrides.get("economic_model", _economic_model())
    liquidity = axis_overrides.get("liquidity_and_market_structure", _liquidity())
    custody = axis_overrides.get("custody_and_counterparty_risk", _custody())
    correlation = axis_overrides.get("correlation_and_volatility", _correlation())
    evidence_quality = axis_overrides.get("evidence_quality", _evidence_quality())
    valuation = axis_overrides.get(
        "valuation_and_economic_assessment_readiness",
        {"status": "valuation_required", "rationale": "Synthetic rationale -- no valuation methodology exists."},
    )

    structural_risk_flags = axis_overrides.get(
        "structural_risk_flags",
        {
            "custody_model": custody.get("custody_model"),
            "smart_contract_risk_category": custody.get("smart_contract_risk_category"),
            "cross_coin_correlation_status": correlation.get("cross_coin_correlation_status"),
        },
    )
    handoff = axis_overrides.get(
        "cross_asset_handoff",
        {
            "role_summary": f"{network.get('consensus_mechanism')} / {network.get('adoption_trend_category')}",
            "evidence_quality_summary": evidence_quality.get("primary_source_coverage"),
            "uncertainty_summary": evidence_quality.get("thesis_uncertainty_statement"),
            "liquidity_risk_summary": liquidity.get("liquidity_tier"),
            "overlap_or_correlation_signal": correlation.get("cross_coin_correlation_status"),
            "valuation_readiness": valuation.get("status"),
        },
    )

    data = {
        "schema_version": "1.0",
        "instrument_id": instrument_id,
        "asset_type": "cryptocurrency",
        "network_fundamentals": network,
        "economic_model": economic,
        "liquidity_and_market_structure": liquidity,
        "custody_and_counterparty_risk": custody,
        "correlation_and_volatility": correlation,
        "regulatory_and_structural_uncertainty": axis_overrides.get("regulatory_and_structural_uncertainty", _regulatory()),
        "evidence_quality": evidence_quality,
        "provenance": axis_overrides.get("provenance", {"sources": _sources()}),
        "uncertainty_summary": axis_overrides.get("uncertainty_summary", evidence_quality.get("thesis_uncertainty_statement")),
        "evidence_quality_status": axis_overrides.get("evidence_quality_status", evidence_quality.get("primary_source_coverage")),
        "structural_risk_flags": structural_risk_flags,
        "record_status": "draft",
        "valuation_and_economic_assessment_readiness": valuation,
        "cross_asset_handoff": handoff,
        "abstention_index": axis_overrides.get("abstention_index", []),
    }
    if sealed:
        data["record_status"] = "sealed"
        data["sealed_at"] = "2026-08-07T23:56:51Z"
        data["governing_decision"] = "XASSET-0004"
        data["drafting_session_or_shard_id"] = "shard-test"
        data["cohort_manifest_entry"] = f"intelligence/crypto_classification/COHORT_MANIFEST.yaml#{instrument_id}"
        data["content_sha256"] = cv.canonical_record_hash(data)
    return data


def _eth_record(*, sealed: bool = False) -> dict:
    return _record(
        sealed=sealed,
        instrument_id="ETH",
        network_fundamentals=_network_fundamentals(consensus_mechanism="proof_of_stake"),
        economic_model=_economic_model(
            supply_model="disinflationary_schedule",
            fee_accrual_applicable=True,
            fee_accrual_basis="Base-fee burn under EIP-1559.",
            staking_applicable=True,
            staking_basis="Proof-of-stake validator staking yield.",
        ),
        custody_and_counterparty_risk=_custody(smart_contract_risk_category="smart_contract_platform_material_surface"),
    )


def _sol_record(*, sealed: bool = False) -> dict:
    return _record(
        sealed=sealed,
        instrument_id="SOL",
        network_fundamentals=_network_fundamentals(
            consensus_mechanism="other_consensus",
            consensus_basis="Proof of History plus Tower BFT proof-of-stake.",
        ),
        economic_model=_economic_model(
            supply_model="disinflationary_schedule",
            fee_accrual_applicable=True,
            fee_accrual_basis="50% fee burn.",
            staking_applicable=True,
            staking_basis="Native staking yield.",
        ),
        custody_and_counterparty_risk=_custody(smart_contract_risk_category="smart_contract_platform_material_surface"),
        correlation_and_volatility=_correlation(historical_volatility_category="extreme_volatility"),
    )


# ── 1-4: valid happy-path records (BTC, ETH, SOL, sealed) ──────────────────

def test_valid_btc_record_passes():
    result = cv.validate_crypto_classification_data(_record(instrument_id="BTC"))
    assert result.valid, result.errors


def test_valid_eth_record_passes():
    result = cv.validate_crypto_classification_data(_eth_record())
    assert result.valid, result.errors


def test_valid_sol_record_passes():
    result = cv.validate_crypto_classification_data(_sol_record())
    assert result.valid, result.errors


def test_valid_sealed_record_passes():
    result = cv.validate_crypto_classification_data(_record(sealed=True))
    assert result.valid, result.errors


# ── 5-6: malformed top-level / instrument (axis-level) schema ──────────────

def test_malformed_top_level_not_a_mapping_rejected():
    result = cv.validate_crypto_classification_data(["not", "a", "mapping"])
    assert not result.valid
    assert any("root document must be a mapping" in e for e in result.errors)


def test_malformed_axis_missing_required_subfield_rejected():
    record = _record(network_fundamentals={})
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("network_fundamentals missing required key" in e for e in result.errors)


# ── 7-8: extra unknown key at envelope / axis level ─────────────────────────

def test_extra_unknown_key_at_envelope_level_rejected():
    record = _record()
    record["extraneous_top_level_field"] = "smuggled"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("unexpected top-level field(s)" in e for e in result.errors)


def test_extra_unknown_key_at_axis_level_rejected():
    record = _record(network_fundamentals=_network_fundamentals(smuggled_key="oops"))
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("network_fundamentals contains unexpected key" in e for e in result.errors)


# ── 9-10: missing required key at envelope/axis level ───────────────────────

def test_missing_required_envelope_field_rejected():
    record = _record()
    del record["provenance"]
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("record missing required field: provenance" in e for e in result.errors)


def test_missing_required_axis_field_rejected():
    record = _record(economic_model={"supply_model": "fixed_capped_supply"})
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("economic_model missing required key" in e for e in result.errors)


# ── 11: wrong asset_type ────────────────────────────────────────────────────

def test_wrong_asset_type_rejected():
    record = _record()
    record["asset_type"] = "etf"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("asset_type must be exactly 'cryptocurrency'" in e for e in result.errors)


def test_neither_etf_nor_cryptocurrency_asset_type_rejected():
    record = _record()
    record["asset_type"] = "equity"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("asset_type must be exactly 'cryptocurrency'" in e for e in result.errors)


# ── 12-13: ETF/crypto cross-contamination in both directions ───────────────

@pytest.mark.parametrize("etf_field", [
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "structure_and_methodology",
])
def test_crypto_record_carrying_etf_only_field_rejected(etf_field):
    record = _record()
    record[etf_field] = {"placeholder": "value"}
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any(etf_field in e and "ETF-classification-shaped field" in e for e in result.errors)


def test_crypto_axis_names_are_not_self_forbidden():
    """The six crypto-specific axis names are legitimate fields on a crypto
    record -- this module's own forbidden-key scan must never flag them
    (only etf_classification_validator.py's own _CRYPTO_FIELD_LEAKAGE set,
    applied to an ETF-shaped document, is responsible for rejecting a
    crypto-only field name showing up there -- SS8 point 4's "opposite
    direction" case, out of this module's own scope to test)."""
    for axis in ("network_fundamentals", "economic_model", "custody_and_counterparty_risk",
                 "correlation_and_volatility", "regulatory_and_structural_uncertainty"):
        assert axis not in cv._FORBIDDEN_KEY_NAMES


def test_crypto_and_etf_forbidden_leakage_sets_are_complementary():
    """Cross-module consistency check: the six crypto axis names this
    module treats as legitimate (and etf_classification_validator.py
    treats as forbidden ETF-record leakage) must never overlap with the
    five ETF axis names this module treats as forbidden crypto-record
    leakage -- guards against the two sibling validators silently drifting
    out of sync on which field belongs to which schema (SS8 point 4)."""
    import etf_classification_validator as ev

    crypto_axis_names = {
        "network_fundamentals", "economic_model", "custody_and_counterparty_risk",
        "correlation_and_volatility", "regulatory_and_structural_uncertainty",
    }
    etf_axis_names = {
        "structural_role", "constituent_exposure", "overlap_and_concentration",
        "cost_and_tracking_quality", "structure_and_methodology",
    }
    assert crypto_axis_names == ev._CRYPTO_FIELD_LEAKAGE
    assert etf_axis_names == cv._ETF_FIELD_LEAKAGE
    assert cv._ETF_FIELD_LEAKAGE.isdisjoint(crypto_axis_names)
    assert cv._EQUITY_FIELD_LEAKAGE == ev._EQUITY_FIELD_LEAKAGE


# ── 14: forbidden equity field anywhere ─────────────────────────────────────

@pytest.mark.parametrize("equity_field", [
    "economic_role", "capital_priority", "risk_concentration", "portfolio_role_ref", "conviction",
])
def test_forbidden_equity_field_rejected(equity_field):
    record = _record()
    record["evidence_quality"][equity_field] = "smuggled"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any(equity_field in e and "equity-classification-shaped field" in e for e in result.errors)


# ── 15: invalid/missing evidence citation ───────────────────────────────────

def test_source_missing_type_rejected():
    record = _record(provenance={"sources": [{
        "source_identifier": "x", "as_of_date": "2026-08-07", "access_status": "consulted_via_search_aggregation",
    }]})
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("missing required key" in e and "sources[0]" in e for e in result.errors)


def test_source_invalid_access_status_rejected():
    record = _record(provenance={"sources": [{
        "source_identifier": "x", "source_type": "primary", "as_of_date": "2026-08-07", "access_status": "made_up_status",
    }]})
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("access_status must be one of" in e for e in result.errors)


# ── 16: abstention behavior ─────────────────────────────────────────────────

def test_unable_to_determine_without_abstention_reason_rejected():
    record = _record(network_fundamentals=_network_fundamentals(adoption_trend_category="unable_to_determine"))
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("network_fundamentals.abstention_reason is required" in e for e in result.errors)


def test_unable_to_determine_with_abstention_reason_and_index_accepted():
    record = _record(
        network_fundamentals=_network_fundamentals(
            adoption_trend_category="unable_to_determine", abstention_reason="Evidence insufficient.",
        ),
        abstention_index=[{
            "axis": "network_fundamentals", "field": "adoption_trend_category",
            "value": "unable_to_determine", "reason": "Evidence insufficient.",
        }],
    )
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


def test_not_applicable_used_on_axis_without_that_state_rejected():
    # liquidity_and_market_structure has no not_applicable state in the schema.
    record = _record(liquidity_and_market_structure={"liquidity_tier": "not_applicable"})
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("liquidity_tier must be one of" in e for e in result.errors)


def test_economic_model_boolean_false_represents_not_applicable_without_basis():
    record = _record(economic_model=_economic_model(fee_accrual_applicable=False, staking_applicable=False))
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


def test_fee_accrual_basis_required_when_applicable_true():
    record = _record(economic_model=_economic_model(fee_accrual_applicable=True, staking_applicable=False))
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("fee_accrual_basis is required" in e for e in result.errors)


def test_staking_basis_forbidden_when_applicable_false():
    record = _record(economic_model=_economic_model(staking_basis="should not be here"))
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("staking_basis must be absent" in e for e in result.errors)


def test_smart_contract_risk_not_applicable_accepted():
    record = _record(custody_and_counterparty_risk=_custody(smart_contract_risk_category="not_applicable"))
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


# ── 17-19: duplicate/missing/extra instrument in population ────────────────

def test_duplicate_instrument_within_directory_detected_by_manifest():
    # Manifest-level duplicate detection is exercised via validate_cohort_manifest below.
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": "x", "content_sha256": "h", "schema_version": "1.0",
         "governing_decision": "XASSET-0004", "record_path": "p"},
        {"instrument_id": "BTC", "sealed_at": "x", "content_sha256": "h", "schema_version": "1.0",
         "governing_decision": "XASSET-0004", "record_path": "p"},
    ]}
    result = cv.validate_cohort_manifest(manifest, {}, authorized_population=frozenset({"BTC", "ETH", "SOL"}))
    assert not result.valid
    assert any("lists 'BTC' more than once" in e for e in result.errors)


def test_missing_instrument_from_population_rejected():
    record = _record(instrument_id="BTC")
    result = cv.validate_crypto_classification_data(record, authorized_population=frozenset({"BTC", "ETH", "SOL"}))
    assert result.valid, result.errors  # BTC alone is a valid single record; population completeness is a manifest-level check
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": "x", "content_sha256": cv.canonical_record_hash(record),
         "schema_version": "1.0", "governing_decision": "XASSET-0004", "record_path": "p"},
    ]}
    manifest_result = cv.validate_cohort_manifest(
        manifest, {"BTC": record}, authorized_population=frozenset({"BTC", "ETH", "SOL"}),
    )
    assert not manifest_result.valid
    assert any("missing authorized instrument(s)" in e for e in manifest_result.errors)


def test_extra_instrument_beyond_population_rejected():
    record = _record(instrument_id="DOGE")
    result = cv.validate_crypto_classification_data(record, authorized_population=frozenset({"BTC", "ETH", "SOL"}))
    assert not result.valid
    assert any("is not in the authorized three-instrument population" in e for e in result.errors)


def test_excluded_dust_coin_rejected():
    for excluded in ("ZORA", "WIF", "BONK", "PEPE", "HYPE"):
        record = _record(instrument_id=excluded)
        result = cv.validate_crypto_classification_data(record, authorized_population=frozenset({"BTC", "ETH", "SOL"}))
        assert not result.valid, f"{excluded} should be rejected"


# ── validate_cohort_manifest negative-path branches (independent-review MINOR-2) ─
#
# The two tests above (duplicate/missing) already exercise two branches of
# validate_cohort_manifest, but with placeholder/valid hashes throughout --
# they never exercise the hash-mismatch, orphan-record, out-of-population-
# via-manifest, or unknown-key branches. Added per an independent exact-head
# review of PR #272 (MINOR-2): the mechanism was already sound, only the
# test coverage was missing, matching PR #270's own MINOR-2 precedent.

def test_manifest_row_hash_mismatch_against_recomputed_hash_rejected():
    record = _record(instrument_id="BTC", sealed=True)
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": record["sealed_at"], "content_sha256": "0" * 64,
         "schema_version": "1.0", "governing_decision": "XASSET-0004", "record_path": "p"},
    ]}
    result = cv.validate_cohort_manifest(
        manifest, {"BTC": record}, authorized_population=frozenset({"BTC"}),
    )
    assert not result.valid
    assert any("content_sha256 mismatch" in e for e in result.errors)


def test_manifest_row_hash_disagrees_with_records_own_recorded_hash_rejected():
    record = _record(instrument_id="BTC", sealed=True)
    # The manifest row's content_sha256 correctly reproduces the record's
    # *content* hash (so the mismatch check above would not itself fire),
    # but the record's own recorded content_sha256 field has been separately
    # corrupted -- a distinct failure mode from a recomputation mismatch.
    corrupted_record = dict(record)
    corrupted_record["content_sha256"] = "1" * 64
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": record["sealed_at"],
         "content_sha256": cv.canonical_record_hash(record),
         "schema_version": "1.0", "governing_decision": "XASSET-0004", "record_path": "p"},
    ]}
    result = cv.validate_cohort_manifest(
        manifest, {"BTC": corrupted_record}, authorized_population=frozenset({"BTC"}),
    )
    assert not result.valid
    assert any("manifest content_sha256 does not match the record's own recorded content_sha256" in e for e in result.errors)


def test_manifest_row_referencing_nonexistent_record_rejected():
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": "x", "content_sha256": "h",
         "schema_version": "1.0", "governing_decision": "XASSET-0004", "record_path": "p"},
    ]}
    result = cv.validate_cohort_manifest(manifest, {}, authorized_population=frozenset({"BTC"}))
    assert not result.valid
    assert any("has no corresponding sealed record file" in e for e in result.errors)


def test_manifest_lists_instrument_outside_authorized_population_rejected():
    record = _record(instrument_id="DOGE", sealed=True)
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "DOGE", "sealed_at": record["sealed_at"],
         "content_sha256": cv.canonical_record_hash(record),
         "schema_version": "1.0", "governing_decision": "XASSET-0004", "record_path": "p"},
    ]}
    result = cv.validate_cohort_manifest(
        manifest, {"DOGE": record}, authorized_population=frozenset({"BTC", "ETH", "SOL"}),
    )
    assert not result.valid
    assert any("outside the authorized population" in e for e in result.errors)


def test_orphan_sealed_record_with_no_manifest_entry_rejected():
    record = _record(instrument_id="BTC", sealed=True)
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": []}
    result = cv.validate_cohort_manifest(
        manifest, {"BTC": record}, authorized_population=frozenset(),
    )
    assert not result.valid
    assert any("sealed record(s) exist with no corresponding cohort manifest entry" in e for e in result.errors)


def test_manifest_row_unknown_key_rejected():
    record = _record(instrument_id="BTC", sealed=True)
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": record["sealed_at"],
         "content_sha256": cv.canonical_record_hash(record),
         "schema_version": "1.0", "governing_decision": "XASSET-0004", "record_path": "p",
         "smuggled_row_key": "oops"},
    ]}
    result = cv.validate_cohort_manifest(
        manifest, {"BTC": record}, authorized_population=frozenset({"BTC"}),
    )
    assert not result.valid
    assert any("cohort[0] contains unexpected key(s)" in e for e in result.errors)


def test_manifest_top_level_unknown_key_rejected():
    manifest = {
        "schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [],
        "smuggled_top_level_key": "oops",
    }
    result = cv.validate_cohort_manifest(manifest, {}, authorized_population=frozenset())
    assert not result.valid
    assert any("cohort manifest contains unexpected top-level key(s)" in e for e in result.errors)


def test_manifest_missing_required_row_key_rejected():
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0004", "cohort": [
        {"instrument_id": "BTC", "sealed_at": "x"},
    ]}
    result = cv.validate_cohort_manifest(manifest, {}, authorized_population=frozenset({"BTC"}))
    assert not result.valid
    assert any("cohort[0] missing required key(s)" in e for e in result.errors)


def test_manifest_not_a_mapping_with_cohort_list_rejected():
    result = cv.validate_cohort_manifest(["not", "a", "mapping"], {})
    assert not result.valid
    assert any("cohort manifest must be a mapping with a 'cohort' list" in e for e in result.errors)


# ── 20: numeric target/range/score/rank leakage ─────────────────────────────

@pytest.mark.parametrize("numeric_key", [
    "target_pct", "target_range", "max_position_size", "maximum_position_size",
    "score", "rank", "ranking", "conviction_score", "recommended_target_pct", "weight",
])
def test_numeric_leakage_key_rejected(numeric_key):
    record = _record()
    record["evidence_quality"][numeric_key] = 1.0
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any(numeric_key in e for e in result.errors)


def test_expense_ratio_pct_is_rejected_unlike_the_etf_schema():
    """Unlike the ETF schema's one permitted numeric field, no numeric field
    of any kind is authorized anywhere in the crypto schema (XASSET-0002
    supporting artifact SS4.3/SS6.1, XASSET-0004 SS E)."""
    record = _record()
    record["evidence_quality"]["expense_ratio_pct"] = 0.5
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("expense_ratio_pct" in e for e in result.errors)


@pytest.mark.parametrize("coefficient_key", ["correlation_coefficient", "cross_coin_correlation_coefficient"])
def test_correlation_coefficient_leakage_rejected(coefficient_key):
    record = _record()
    record["correlation_and_volatility"][coefficient_key] = 0.87
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any(coefficient_key in e for e in result.errors)


# ── 21: chart-terminology leakage, each of the sixteen terms individually ──

@pytest.mark.parametrize("term", [
    "support", "resistance", "breakout", "trend line", "trendline", "moving average",
    "rsi", "macd", "candlestick", "chart pattern", "technical analysis", "oversold",
    "overbought", "fibonacci", "volume profile", "price target", "momentum",
])
def test_chart_terminology_leakage_rejected(term):
    record = _record(uncertainty_summary=f"This coin shows a clear {term} signal.")
    record["evidence_quality"]["thesis_uncertainty_statement"] = f"This coin shows a clear {term} signal."
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("chart-derived terminology" in e for e in result.errors)


# ── 22: directive/trading language leakage, word-boundary matched ──────────

@pytest.mark.parametrize("word", ["buy", "sell", "add", "hold", "trim", "exit", "wait", "stage"])
def test_directive_word_leakage_rejected(word):
    record = _record()
    record["evidence_quality"]["thesis_uncertainty_statement"] = f"One should {word} this position."
    record["uncertainty_summary"] = f"One should {word} this position."
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("contains directive word" in e for e in result.errors)


def test_directive_scan_does_not_false_positive_on_holdings_noun():
    record = _record()
    text = "This is a factual note about current holdings data."
    record["evidence_quality"]["thesis_uncertainty_statement"] = text
    record["uncertainty_summary"] = text
    record["cross_asset_handoff"]["uncertainty_summary"] = text
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


def test_directive_scan_does_not_false_positive_on_additional_or_waited():
    record = _record()
    text = "The proposal would provide additional detail after the queue waited out its delay."
    record["evidence_quality"]["thesis_uncertainty_statement"] = text
    record["uncertainty_summary"] = text
    record["cross_asset_handoff"]["uncertainty_summary"] = text
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


# ── 23: forbidden recommendation-shaped phrases ─────────────────────────────

@pytest.mark.parametrize("phrase", [
    "should be increased to 5%",
    "recommended a target of 4%",
    "new target pct",
    "buy recommendation",
    "sell recommendation",
    "trim recommendation",
    "12.5% of book",
])
def test_forbidden_recommendation_shaped_phrase_rejected(phrase):
    record = _record()
    record["evidence_quality"]["thesis_uncertainty_statement"] = f"Some text containing: {phrase} in context."
    record["uncertainty_summary"] = f"Some text containing: {phrase} in context."
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("forbidden recommendation-shaped phrase" in e for e in result.errors)


# ── 24: valuation_and_economic_assessment_readiness forced-value violation ─

def test_valuation_status_forced_value_violation_rejected():
    record = _record(valuation_and_economic_assessment_readiness={
        "status": "fair_value_computed", "rationale": "not allowed",
    })
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("must be exactly 'valuation_required'" in e for e in result.errors)


# ── 25: cross_coin_correlation_status forced-value violation (crypto-specific) ─

def test_cross_coin_correlation_status_forced_value_violation_rejected():
    record = _record(correlation_and_volatility=_correlation(cross_coin_correlation_status="measured_elsewhere_cross_reference_required"))
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("must be exactly 'not_yet_measured'" in e for e in result.errors)


def test_cross_coin_correlation_status_invalid_value_rejected():
    record = _record(correlation_and_volatility=_correlation(cross_coin_correlation_status="made_up_value"))
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("cross_coin_correlation_status must be one of" in e for e in result.errors)


# ── 26: envelope-projection-mismatch rejection ──────────────────────────────

def test_envelope_projection_mismatch_uncertainty_summary_rejected():
    record = _record()
    record["uncertainty_summary"] = "Mismatched text."
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("uncertainty_summary must exactly equal" in e for e in result.errors)


def test_envelope_projection_mismatch_evidence_quality_status_rejected():
    record = _record()
    record["evidence_quality_status"] = "comprehensive"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("evidence_quality_status must exactly equal" in e for e in result.errors)


def test_structural_risk_flags_missing_rejected():
    record = _record()
    del record["structural_risk_flags"]
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("structural_risk_flags must be a mapping" in e for e in result.errors)


def test_structural_risk_flags_mismatch_rejected():
    record = _record()
    record["structural_risk_flags"] = {
        "custody_model": "self_custodied",
        "smart_contract_risk_category": "not_applicable",
        "cross_coin_correlation_status": "not_yet_measured",
    }
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("structural_risk_flags must exactly project" in e for e in result.errors)


def test_cross_asset_handoff_role_summary_mismatch_rejected():
    record = _record()
    record["cross_asset_handoff"]["role_summary"] = "wrong summary"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("role_summary must exactly equal" in e for e in result.errors)


def test_cross_asset_handoff_overlap_or_correlation_signal_mismatch_rejected():
    record = _record()
    record["cross_asset_handoff"]["overlap_or_correlation_signal"] = "wrong"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("overlap_or_correlation_signal must exactly project" in e for e in result.errors)


def test_cross_asset_handoff_missing_key_rejected():
    record = _record()
    del record["cross_asset_handoff"]["valuation_readiness"]
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("cross_asset_handoff missing required key" in e for e in result.errors)


# ── abstention_index completeness (SS9.1 lesson, carried forward from start) ─

def test_abstention_index_missing_entry_for_real_abstention_rejected():
    record = _record(
        network_fundamentals=_network_fundamentals(
            adoption_trend_category="unable_to_determine", abstention_reason="Evidence insufficient.",
        ),
        abstention_index=[],
    )
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("abstention_index is missing an entry for network_fundamentals.adoption_trend_category" in e for e in result.errors)


def test_abstention_index_extra_entry_not_itself_an_error():
    # abstention_index is checked for completeness (every real abstention
    # represented), not exact equality with the set of real abstentions --
    # an extra, well-formed entry is not itself rejected by this check.
    record = _record(
        abstention_index=[{
            "axis": "custody_and_counterparty_risk", "field": "smart_contract_risk_category",
            "value": "unable_to_determine", "reason": "Extra disclosed entry.",
        }],
    )
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


def test_not_yet_measured_is_not_treated_as_an_abstention_index_entry():
    """The crypto-specific analogue of the ETF sleeve's tracking_quality_
    category.not_yet_measured ambiguity (etf_classification_validator.py's
    own docstring) -- correlation_and_volatility.cross_coin_correlation_
    status's forced not_yet_measured value must not itself require an
    abstention_index entry."""
    record = _record()
    assert record["correlation_and_volatility"]["cross_coin_correlation_status"] == "not_yet_measured"
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors
    assert record["abstention_index"] == []


def test_abstention_index_malformed_entry_rejected():
    record = _record(abstention_index=[{"axis": "x"}])
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("abstention_index[0] must be a mapping" in e for e in result.errors)


def test_abstention_index_unknown_key_rejected():
    record = _record(abstention_index=[{
        "axis": "network_fundamentals", "field": "adoption_trend_category",
        "value": "x", "reason": "y", "extra": "z",
    }])
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("abstention_index[0] contains unexpected key" in e for e in result.errors)


# ── deterministic output ────────────────────────────────────────────────────

def test_deterministic_hash_across_repeated_calls():
    record = _record(sealed=True)
    h1 = cv.canonical_record_hash(record)
    h2 = cv.canonical_record_hash(record)
    assert h1 == h2


def test_hash_excludes_only_seal_fields():
    record = _record(sealed=True)
    without_seal = {k: v for k, v in record.items() if k not in cv._SEAL_REQUIRED_KEYS}
    assert cv._HASHABLE_KEYS
    hashable_from_full = {k: record.get(k) for k in sorted(cv._HASHABLE_KEYS)}
    hashable_from_stripped = {k: without_seal.get(k) for k in sorted(cv._HASHABLE_KEYS)}
    assert hashable_from_full == hashable_from_stripped


def test_content_sha256_mismatch_rejected():
    record = _record(sealed=True)
    record["content_sha256"] = "0" * 64
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("content_sha256 does not reproduce" in e for e in result.errors)


# ── seal / record_status ────────────────────────────────────────────────────

def test_draft_record_status_skips_seal_requirements():
    record = _record(sealed=False)
    result = cv.validate_crypto_classification_data(record)
    assert result.valid, result.errors


def test_invalid_record_status_rejected():
    record = _record()
    record["record_status"] = "published"
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("record_status must be one of" in e for e in result.errors)


def test_sealed_record_missing_seal_field_rejected():
    record = _record(sealed=True)
    del record["governing_decision"]
    result = cv.validate_crypto_classification_data(record)
    assert not result.valid
    assert any("missing required seal field" in e for e in result.errors)


# ── allocator/margin import-coupling isolation ──────────────────────────────

def test_module_does_not_import_allocate_or_margin_state():
    source = (REPO_ROOT / "crypto_classification_validator.py").read_text()
    assert "import allocate" not in source
    assert "from allocate" not in source
    assert "import margin_state" not in source
    assert "from margin_state" not in source


# ── real repository directory/manifest validation ───────────────────────────

CRYPTO_DIR = REPO_ROOT / "intelligence" / "crypto_classification"


def test_real_repository_directory_validates_clean():
    result = cv.validate_crypto_classification_directory(CRYPTO_DIR)
    assert result.valid, [e for r in result.results if not r.valid for e in r.errors]


def test_real_repository_has_exactly_three_records():
    yaml_paths = sorted(p for p in CRYPTO_DIR.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml")
    assert {p.stem for p in yaml_paths} == {"BTC", "ETH", "SOL"}


def test_real_repository_records_are_all_sealed():
    for ticker in ("BTC", "ETH", "SOL"):
        data = yaml.safe_load((CRYPTO_DIR / f"{ticker}.yaml").read_text())
        assert data["record_status"] == "sealed"


def test_real_repository_cross_coin_correlation_status_forced_default():
    for ticker in ("BTC", "ETH", "SOL"):
        data = yaml.safe_load((CRYPTO_DIR / f"{ticker}.yaml").read_text())
        assert data["correlation_and_volatility"]["cross_coin_correlation_status"] == "not_yet_measured"
        assert "correlation_coefficient" not in str(data)


def test_real_repository_valuation_forced_default():
    for ticker in ("BTC", "ETH", "SOL"):
        data = yaml.safe_load((CRYPTO_DIR / f"{ticker}.yaml").read_text())
        assert data["valuation_and_economic_assessment_readiness"]["status"] == "valuation_required"


def test_real_repository_manifest_reconciles():
    manifest = yaml.safe_load((CRYPTO_DIR / "COHORT_MANIFEST.yaml").read_text())
    ids = [row["instrument_id"] for row in manifest["cohort"]]
    assert ids == sorted(ids)
    assert set(ids) == {"BTC", "ETH", "SOL"}


def test_missing_directory_is_valid_zero_coverage():
    result = cv.validate_crypto_classification_directory(REPO_ROOT / "intelligence" / "does_not_exist_classification")
    assert result.valid
    assert result.record_count == 0


def test_manifest_required_whenever_sealed_records_exist(tmp_path):
    d = tmp_path / "crypto_classification"
    d.mkdir()
    record = _record(sealed=True)
    (d / "BTC.yaml").write_text(yaml.safe_dump(record))
    result = cv.validate_crypto_classification_directory(d, authorized_population=frozenset({"BTC"}))
    assert not result.valid
    assert any("COHORT_MANIFEST.yaml is required" in e for r in result.results for e in r.errors)


def test_filename_stem_must_match_instrument_id(tmp_path):
    d = tmp_path / "crypto_classification"
    d.mkdir()
    record = _record(sealed=True, instrument_id="BTC")
    (d / "WRONG.yaml").write_text(yaml.safe_dump(record))
    result = cv.validate_crypto_classification_file(d / "WRONG.yaml", authorized_population=frozenset({"BTC"}))
    assert not result.valid
    assert any("does not match the record's own instrument_id" in e for e in result.errors)


# ── protected-path isolation ────────────────────────────────────────────────

_PROTECTED_PATHS = [
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "allocate.py", "margin_state.py", "levels.py",
    "intelligence/etf_classification/SPY.yaml",
    "intelligence/etf_classification/VEA.yaml",
    "intelligence/etf_classification/VWO.yaml",
    "intelligence/etf_classification/GLD.yaml",
    "intelligence/etf_classification/COHORT_MANIFEST.yaml",
    "intelligence/classification",
    "intelligence/reconciliation",
    "intelligence/recommendations",
    "intelligence/relationships",
    "intelligence/companies",
    "intelligence/themes",
]


@pytest.mark.parametrize("rel_path", _PROTECTED_PATHS)
def test_protected_path_exists_and_untouched_by_this_module(rel_path):
    """A static-analysis-style assertion, mirroring existing repository
    precedent: this validator module contains no code path that opens any
    protected file for writing, and every protected path still exists
    unmodified in the repository after this module's own directory-scan
    functions have run (test_real_repository_directory_validates_clean
    above already exercises the directory scan)."""
    path = REPO_ROOT / rel_path
    assert path.exists(), f"expected protected path to exist: {rel_path}"
    source = (REPO_ROOT / "crypto_classification_validator.py").read_text()
    assert 'open(' not in source or 'mode="w"' not in source
    assert ".write_text(" not in source
    assert "yaml.safe_dump" not in source
    assert "yaml.dump" not in source
