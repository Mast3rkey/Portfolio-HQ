"""Tests for economic_assessment_validator.py (WS-0014 GLD/CASH_LIKE_
CAPITAL economic-assessment schema, XASSET-0008/XASSET-0009 scope).

Every schema/behavior test below constructs its own synthetic fixture --
no real analytical subject's judgment content is asserted against in this
file except the small, explicitly-labeled real-repository directory-scan
section at the bottom, which exercises the two real sealed records
authored under this implementation PR.

DEBT_REDUCTION's own economic-assessment gap remains entirely out of
scope for this module and this file -- no third analytical_subject value
is authorized, and no DEBT_REDUCTION-shaped fixture is constructed here
except as a rejected-value test case.
"""

from __future__ import annotations

import ast
import copy
import subprocess
from pathlib import Path

import pytest
import yaml

import economic_assessment_validator as eav
import etf_classification_validator as etf
import functional_doctrine_validator as fdv

REPO_ROOT = Path(__file__).resolve().parent


# ── fixtures ─────────────────────────────────────────────────────────────

def _deployability(**overrides) -> dict:
    d = {
        "deployability_category": "high_optionality_low_friction",
        "rationale": "Synthetic rationale -- no structural constraint identified.",
    }
    d.update(overrides)
    return d


def _cost_tracking(**overrides) -> dict:
    d = {
        "significance_category": "in_line_with_category",
        "rationale": "Synthetic rationale -- comparable to category peers.",
    }
    d.update(overrides)
    return d


def _inflation_sensitivity(**overrides) -> dict:
    d = {
        "sensitivity_category": "historically_mixed_or_inconsistent",
        "rationale": "Synthetic rationale -- sourced material diverges by horizon.",
    }
    d.update(overrides)
    return d


def _drawdown_behavior(**overrides) -> dict:
    d = {
        "behavior_category": "historically_mixed",
        "rationale": "Synthetic rationale -- mixed pattern across historical episodes.",
        "single_asset_disclosure": (
            "This finding is single-asset and historical only; it does not compute a "
            "whole-portfolio finding."
        ),
    }
    d.update(overrides)
    return d


def _instrument_specific_gld(**overrides) -> dict:
    d = {
        "cost_and_tracking_economic_significance": _cost_tracking(),
        "historical_inflation_sensitivity": _inflation_sensitivity(),
        "historical_equity_drawdown_behavior": _drawdown_behavior(),
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
            "source_identifier": "Synthetic governing-doctrine citation",
            "source_type": "primary",
            "as_of_date": "2026-08-10",
            "access_status": "directly_inspected",
        }
    ]


def _structural_reference_etf(*, hash_override: str | None = None) -> dict:
    gld_data = yaml.safe_load((REPO_ROOT / "intelligence" / "etf_classification" / "GLD.yaml").read_text())
    live_hash = etf.canonical_record_hash(gld_data)
    return {
        "source_instrument_id": "GLD",
        "source_schema": "etf_classification",
        "source_file": "intelligence/etf_classification/GLD.yaml",
        "referenced_content_sha256": hash_override if hash_override is not None else live_hash,
    }


def _structural_reference_fd(*, hash_override: str | None = None) -> dict:
    gdr_data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "GLD_DEFENSIVE_ROLE.yaml").read_text())
    live_hash = fdv.canonical_record_hash(gdr_data)
    return {
        "source_capital_use_type": "GLD_DEFENSIVE_ROLE",
        "source_schema": "functional_doctrine",
        "source_file": "intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml",
        "referenced_content_sha256": hash_override if hash_override is not None else live_hash,
    }


def _legacy_reference(capital_use_type: str, *, hash_override: str | None = None) -> dict:
    path = REPO_ROOT / "intelligence" / "functional_doctrine" / f"{capital_use_type}.yaml"
    data = yaml.safe_load(path.read_text())
    live_hash = fdv.canonical_record_hash(data)
    return {
        "source_capital_use_type": capital_use_type,
        "source_schema": "functional_doctrine",
        "source_file": f"intelligence/functional_doctrine/{capital_use_type}.yaml",
        "referenced_content_sha256": hash_override if hash_override is not None else live_hash,
    }


def _legacy_references(**overrides_by_type) -> list:
    return [
        _legacy_reference("CASH", **overrides_by_type.get("CASH", {})),
        _legacy_reference("RESERVE", **overrides_by_type.get("RESERVE", {})),
    ]


def _record(*, analytical_subject: str = "GLD", sealed: bool = False, **overrides) -> dict:
    deployability = overrides.get("deployability_and_optionality", _deployability())
    if analytical_subject == "GLD":
        instrument_specific = overrides.get("instrument_specific_economic_characterization", _instrument_specific_gld())
    else:
        instrument_specific = overrides.get("instrument_specific_economic_characterization", {"not_applicable": True})
    evidence_quality = overrides.get("evidence_quality", _evidence_quality())

    handoff = overrides.get(
        "cross_asset_handoff",
        {
            "deployability_summary": deployability.get("deployability_category"),
            "instrument_specific_summary": instrument_specific,
            "evidence_quality_summary": evidence_quality.get("primary_source_coverage"),
            "uncertainty_summary": evidence_quality.get("thesis_uncertainty_statement"),
        },
    )

    data = {
        "schema_version": "1.0",
        "analytical_subject": analytical_subject,
        "deployability_and_optionality": deployability,
        "instrument_specific_economic_characterization": instrument_specific,
        "evidence_quality": evidence_quality,
        "provenance": {"sources": _sources()},
        "evidence_quality_status": evidence_quality.get("primary_source_coverage"),
        "uncertainty_summary": evidence_quality.get("thesis_uncertainty_statement"),
        "record_status": "draft",
        "later_governance_action": "none",
        "abstention_index": overrides.get("abstention_index", []),
        "cross_asset_handoff": handoff,
    }

    if analytical_subject == "GLD":
        data["structural_reference_etf_classification"] = overrides.get(
            "structural_reference_etf_classification", _structural_reference_etf()
        )
        data["structural_reference_functional_doctrine"] = overrides.get(
            "structural_reference_functional_doctrine", _structural_reference_fd()
        )
    elif analytical_subject == "CASH_LIKE_CAPITAL":
        data["legacy_structural_references"] = overrides.get("legacy_structural_references", _legacy_references())

    if sealed:
        data["record_status"] = "sealed"
        data["sealed_at"] = "2026-08-10T00:00:00Z"
        data["governing_decision"] = "XASSET-0009"
        data["drafting_session_or_shard_id"] = "test-shard"
        data["cohort_manifest_entry"] = f"intelligence/economic_assessment/COHORT_MANIFEST.yaml#{analytical_subject}"
        data["content_sha256"] = eav.canonical_record_hash(data)

    return data


def _assert_invalid(data: dict, *, contains: str | None = None, repo_root=None) -> eav.ValidationResult:
    result = eav.validate_economic_assessment_data(data, repo_root=repo_root)
    assert not result.valid, "expected validation failure but got valid=True"
    if contains is not None:
        assert any(contains in e for e in result.errors), f"{contains!r} not found in {result.errors}"
    return result


# ── happy path, one per analytical_subject ──────────────────────────────

@pytest.mark.parametrize("analytical_subject", sorted(eav.AUTHORIZED_POPULATION))
def test_happy_path_per_analytical_subject(analytical_subject):
    data = _record(analytical_subject=analytical_subject, sealed=True)
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_happy_path_draft_no_seal_fields_required():
    data = _record(analytical_subject="GLD", sealed=False)
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


# ── malformed envelope/axis (missing required field) ─────────────────────

@pytest.mark.parametrize("missing_key", [
    "analytical_subject", "schema_version", "deployability_and_optionality",
    "instrument_specific_economic_characterization", "evidence_quality", "provenance",
    "abstention_index", "later_governance_action", "cross_asset_handoff", "record_status",
])
def test_missing_required_top_level_field_rejected(missing_key):
    data = _record(analytical_subject="GLD")
    del data[missing_key]
    _assert_invalid(data)


def test_missing_required_axis_sub_field_rejected():
    data = _record(analytical_subject="GLD")
    del data["deployability_and_optionality"]["deployability_category"]
    _assert_invalid(data, contains="deployability_and_optionality")


def test_missing_required_compound_sub_field_rejected():
    data = _record(analytical_subject="GLD")
    del data["instrument_specific_economic_characterization"]["historical_inflation_sensitivity"]
    _assert_invalid(data, contains="missing required sub-field")


# ── extra unknown key at every level ────────────────────────────────────

def test_extra_unknown_key_at_envelope_level_rejected():
    data = _record(analytical_subject="GLD")
    data["smuggled_field"] = "anything"
    _assert_invalid(data, contains="smuggled_field")


def test_extra_unknown_key_in_deployability_rejected():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["extra"] = "x"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_instrument_specific_compound_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["extra_sub_field"] = {}
    _assert_invalid(data, contains="unexpected key")


@pytest.mark.parametrize("sub_field", [
    "cost_and_tracking_economic_significance", "historical_inflation_sensitivity",
    "historical_equity_drawdown_behavior",
])
def test_extra_unknown_key_in_instrument_specific_sub_field_rejected(sub_field):
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"][sub_field]["extra"] = "x"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_evidence_quality_rejected():
    data = _record(analytical_subject="GLD")
    data["evidence_quality"]["extra"] = "x"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_provenance_source_rejected():
    data = _record(analytical_subject="GLD")
    data["provenance"]["sources"][0]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_structural_reference_etf_rejected():
    data = _record(analytical_subject="GLD")
    data["structural_reference_etf_classification"]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_structural_reference_fd_rejected():
    data = _record(analytical_subject="GLD")
    data["structural_reference_functional_doctrine"]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_legacy_structural_reference_entry_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["legacy_structural_references"][0]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_cross_asset_handoff_rejected():
    data = _record(analytical_subject="GLD")
    data["cross_asset_handoff"]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_abstention_index_entry_rejected():
    data = _record(
        analytical_subject="GLD",
        abstention_index=[{"axis": "deployability_and_optionality", "field": "deployability_category", "value": "unable_to_determine", "reason": "gap", "extra": "x"}],
    )
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_manifest_row_rejected():
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0009",
        "cohort": [{
            "analytical_subject": "GLD", "sealed_at": "x", "content_sha256": "x",
            "schema_version": "1.0", "governing_decision": "XASSET-0009",
            "record_path": "intelligence/economic_assessment/GLD.yaml", "extra": "x",
        }],
    }
    result = eav.validate_cohort_manifest(manifest, {})
    assert not result.valid
    assert any("unexpected key" in e for e in result.errors)


def test_extra_unknown_key_at_manifest_top_level_rejected():
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0009", "cohort": [], "extra": "x"}
    result = eav.validate_cohort_manifest(manifest, {})
    assert not result.valid
    assert any("unexpected top-level key" in e for e in result.errors)


# ── wrong analytical_subject ─────────────────────────────────────────────

@pytest.mark.parametrize("bad_value", ["SPY", "CASH", "RESERVE", "DEBT_REDUCTION", "GLD_DEFENSIVE_ROLE", ""])
def test_wrong_analytical_subject_rejected(bad_value):
    data = _record(analytical_subject="GLD")
    data["analytical_subject"] = bad_value
    _assert_invalid(data)


# ── structural-reference / legacy-reference population-conditional shape ──

def test_legacy_structural_references_present_on_gld_rejected():
    data = _record(analytical_subject="GLD")
    data["legacy_structural_references"] = _legacy_references()
    _assert_invalid(data, contains="legacy_structural_references is forbidden")


def test_structural_reference_etf_missing_on_gld_rejected():
    data = _record(analytical_subject="GLD")
    del data["structural_reference_etf_classification"]
    _assert_invalid(data, contains="structural_reference_etf_classification is required")


def test_structural_reference_fd_missing_on_gld_rejected():
    data = _record(analytical_subject="GLD")
    del data["structural_reference_functional_doctrine"]
    _assert_invalid(data, contains="structural_reference_functional_doctrine is required")


def test_legacy_structural_references_missing_on_cash_like_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    del data["legacy_structural_references"]
    _assert_invalid(data, contains="legacy_structural_references is required")


def test_structural_reference_etf_present_on_cash_like_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["structural_reference_etf_classification"] = _structural_reference_etf()
    _assert_invalid(data, contains="structural_reference_etf_classification is forbidden")


def test_structural_reference_fd_present_on_cash_like_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["structural_reference_functional_doctrine"] = _structural_reference_fd()
    _assert_invalid(data, contains="structural_reference_functional_doctrine is forbidden")


def test_legacy_structural_references_wrong_count_too_few_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["legacy_structural_references"] = [_legacy_reference("CASH")]
    _assert_invalid(data, contains="exactly two entries")


def test_legacy_structural_references_wrong_count_too_many_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["legacy_structural_references"] = _legacy_references() + [_legacy_reference("CASH")]
    _assert_invalid(data)


def test_legacy_structural_references_duplicate_type_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["legacy_structural_references"] = [_legacy_reference("CASH"), _legacy_reference("CASH")]
    _assert_invalid(data)


def test_legacy_structural_references_missing_reserve_entry_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["legacy_structural_references"] = [_legacy_reference("CASH"), _legacy_reference("CASH")]
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("missing entry" in e or "duplicate" in e for e in result.errors)


# ── instrument_specific_economic_characterization not_applicable shape ────

def test_instrument_specific_populated_on_cash_like_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["instrument_specific_economic_characterization"] = _instrument_specific_gld()
    _assert_invalid(data)


def test_instrument_specific_not_applicable_on_gld_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"] = {"not_applicable": True}
    _assert_invalid(data, contains="must be a populated compound object")


def test_instrument_specific_not_applicable_false_on_cash_like_rejected():
    """A self-declared flag is not a substitute for an independent check
    -- not_applicable must be independently verified against
    analytical_subject, never merely trusted (etf_classification_
    validator.py's own disclosed MINOR-1 lesson, applied here)."""
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["instrument_specific_economic_characterization"] = {"not_applicable": False}
    _assert_invalid(data, contains="must be exactly")


def test_instrument_specific_extra_key_alongside_not_applicable_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["instrument_specific_economic_characterization"] = {"not_applicable": True, "extra": "x"}
    _assert_invalid(data, contains="unexpected key")


# ── structural-reference / legacy-reference hash verification ───────────

def test_structural_reference_etf_stale_hash_rejected():
    data = _record(analytical_subject="GLD", structural_reference_etf_classification=_structural_reference_etf(hash_override="0" * 64))
    _assert_invalid(data, contains="is stale", repo_root=REPO_ROOT)


def test_structural_reference_fd_stale_hash_rejected():
    data = _record(analytical_subject="GLD", structural_reference_functional_doctrine=_structural_reference_fd(hash_override="0" * 64))
    _assert_invalid(data, contains="is stale", repo_root=REPO_ROOT)


def test_legacy_reference_cash_stale_hash_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL", legacy_structural_references=_legacy_references(CASH={"hash_override": "0" * 64}))
    _assert_invalid(data, contains="is stale", repo_root=REPO_ROOT)


def test_legacy_reference_reserve_stale_hash_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL", legacy_structural_references=_legacy_references(RESERVE={"hash_override": "0" * 64}))
    _assert_invalid(data, contains="is stale", repo_root=REPO_ROOT)


def test_structural_reference_etf_wrong_source_instrument_id_rejected():
    ref = _structural_reference_etf()
    ref["source_instrument_id"] = "SPY"
    data = _record(analytical_subject="GLD", structural_reference_etf_classification=ref)
    _assert_invalid(data, contains="source_instrument_id")


def test_structural_reference_fd_wrong_capital_use_type_rejected():
    ref = _structural_reference_fd()
    ref["source_capital_use_type"] = "CASH"
    data = _record(analytical_subject="GLD", structural_reference_functional_doctrine=ref)
    _assert_invalid(data, contains="source_capital_use_type")


def test_legacy_reference_wrong_source_capital_use_type_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["legacy_structural_references"] = [
        {**_legacy_reference("CASH"), "source_capital_use_type": "GLD_DEFENSIVE_ROLE"},
        _legacy_reference("RESERVE"),
    ]
    _assert_invalid(data)


def test_no_repo_root_skips_hash_recompute_but_still_requires_non_empty_string():
    data = _record(analytical_subject="GLD")
    result = eav.validate_economic_assessment_data(data, repo_root=None)
    assert result.valid, result.errors


# ── cross-schema field-name leakage ──────────────────────────────────────

@pytest.mark.parametrize("equity_key", sorted(eav._EQUITY_FIELD_LEAKAGE))
def test_equity_field_leakage_rejected(equity_key):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"][equity_key] = "x"
    _assert_invalid(data, contains="forbidden key name")


@pytest.mark.parametrize("etf_key", sorted(eav._ETF_FIELD_LEAKAGE))
def test_etf_field_leakage_rejected(etf_key):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"][etf_key] = "x"
    _assert_invalid(data, contains="forbidden key name")


@pytest.mark.parametrize("crypto_key", sorted(eav._CRYPTO_FIELD_LEAKAGE))
def test_crypto_field_leakage_rejected(crypto_key):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"][crypto_key] = "x"
    _assert_invalid(data, contains="forbidden key name")


@pytest.mark.parametrize("fd_key", sorted(eav._FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE))
def test_functional_doctrine_field_leakage_rejected(fd_key):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"][fd_key] = "x"
    _assert_invalid(data, contains="forbidden key name")


@pytest.mark.parametrize("overlap_key", sorted(eav._OVERLAP_MODEL_FIELD_LEAKAGE))
def test_overlap_model_field_leakage_rejected(overlap_key):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"][overlap_key] = "x"
    _assert_invalid(data, contains="forbidden key name")


# ── numeric-field leakage (SS11 point 6) -- no carve-out, no positive test ─

@pytest.mark.parametrize("numeric_key", sorted(eav._NUMERIC_LEAKAGE_KEYS))
def test_numeric_field_leakage_rejected(numeric_key):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"][numeric_key] = 1
    _assert_invalid(data, contains="forbidden key name")


def test_bare_numeric_percent_token_rejected_in_free_text():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "This is roughly 4% of book, for illustration."
    _assert_invalid(data, contains="numeric-percent-shaped token")


def test_bare_numeric_percent_token_rejected_with_no_carveout_even_when_citing_a_real_disclosed_fact():
    """SS11 point 6: no carve-out of any kind -- stricter than the ETF
    framework's own scoped expense_ratio_pct exception."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["cost_and_tracking_economic_significance"]["rationale"] = (
        "GLD's own expense ratio of 0.40% is higher than peers."
    )
    _assert_invalid(data, contains="numeric-percent-shaped token")


# ── chart-terminology leakage ────────────────────────────────────────────

@pytest.mark.parametrize("term", eav._CHART_TERMS)
def test_chart_terminology_leakage_rejected(term):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = f"Evidence involving {term} was considered."
    _assert_invalid(data, contains="chart-derived terminology")


# ── directive/trading-language leakage ───────────────────────────────────

@pytest.mark.parametrize("word", eav._DIRECTIVE_WORDS)
def test_directive_word_leakage_rejected(word):
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = f"One should {word} this position."
    _assert_invalid(data, contains="directive word")


def test_directive_word_false_positive_guard_citation_field():
    data = _record(analytical_subject="GLD")
    data["provenance"]["sources"][0]["source_identifier"] = "SPDR Gold Shares (GLD) fund page"
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_directive_word_hold_does_not_false_positive_on_holdings():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "Consistent with the family's holdings profile."
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_directive_word_exit_does_not_false_positive_on_exiting():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "No structural barrier prevents exiting this position at will."
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_directive_word_add_does_not_false_positive_on_address():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "This does not address a currently-advisable-deployment question."
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_directive_word_still_flagged_outside_citation_fields():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "Investors should buy this fund."
    _assert_invalid(data, contains="directive word")


# ── predictive-language leakage (scoped to two GLD sub-fields only) ──────

@pytest.mark.parametrize("term", eav._PREDICTIVE_TERMS)
def test_predictive_language_leakage_rejected_inflation_sensitivity(term):
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_inflation_sensitivity"]["rationale"] = (
        f"It is {term} to remain positively associated."
    )
    _assert_invalid(data, contains="forward-looking term")


@pytest.mark.parametrize("term", eav._PREDICTIVE_TERMS)
def test_predictive_language_leakage_rejected_drawdown_behavior(term):
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"] = (
        f"Gold is {term} to behave defensively in the next drawdown."
    )
    _assert_invalid(data, contains="forward-looking term")


def test_predictive_language_scan_not_applied_outside_the_two_scoped_sub_fields():
    """The predictive-language scan is deliberately scoped to exactly
    historical_inflation_sensitivity and historical_equity_drawdown_
    behavior -- it must not fire on deployability_and_optionality's own
    free text (SS11 point 11's own 'scoped correctly' requirement)."""
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "This capital is expected to remain deployable."
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


# ── overlap-model (defensive_offset_interface) non-duplication ──────────

def test_overlap_model_non_duplication_diversification_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"] = (
        "Gold provides a diversification benefit to the current portfolio during drawdowns."
    )
    _assert_invalid(data, contains="whole-portfolio diversification")


def test_overlap_model_non_duplication_correlation_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"] = (
        "Gold is uncorrelated with the current portfolio's own holdings."
    )
    _assert_invalid(data, contains="whole-portfolio diversification")


def test_single_asset_disclosure_missing_rejected():
    data = _record(analytical_subject="GLD")
    del data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"]
    _assert_invalid(data, contains="single_asset_disclosure")


def test_single_asset_disclosure_missing_marker_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding does not constitute a portfolio-level determination."
    )
    _assert_invalid(data, contains="single-asset")


def test_single_asset_disclosure_real_disclaimer_text_accepted_negation_aware():
    """The required disclosure field's own job is to name and disclaim
    the portfolio-level boundary using this vocabulary -- a genuine
    disclaiming negation ("does not... constitute...") preceding the
    claim, within the same sentence, is accepted. Bounded-correction
    regression: single_asset_disclosure IS scanned (unlike the original
    design's full exemption), but negation-awareness keeps this real
    disclaimer text valid."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding is single-asset and historical only. It does not compute, constitute, "
        "imply, or substitute for a whole-portfolio diversification-benefit or correlation "
        "finding specific to Portfolio-HQ's own current holdings."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


# ── bounded correction: single_asset_disclosure negation-aware scan ─────
# An independent exact-head review (PR #294) found the original design's
# full exemption of single_asset_disclosure too broad -- a hand-crafted
# record could bury a real, unnegated portfolio-level claim inside it and
# validate clean. These tests reproduce the reviewer's demonstrated bug
# and confirm the corrected, negation-aware, sentence-scoped scan closes
# it without breaking the real sealed record's own disclaimer text.

def test_single_asset_disclosure_reviewer_crafted_attack_rejected():
    """The exact hand-crafted attack the independent review demonstrated
    passed validation before this correction -- must now be rejected."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding is single-asset in name only -- in fact it demonstrates a genuine "
        "diversification benefit to the current portfolio and reduces the portfolio risk "
        "materially, correlated with the current portfolio at a strongly negative level."
    )
    _assert_invalid(data, contains="not accompanied")


def test_single_asset_disclosure_unnegated_diversifies_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset assessment, and GLD therefore diversifies the whole portfolio."
    )
    _assert_invalid(data, contains="not accompanied")


def test_single_asset_disclosure_unnegated_drawdown_reduction_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding. GLD reduces total portfolio drawdown."
    )
    _assert_invalid(data, contains="not accompanied")


def test_single_asset_disclosure_unnegated_negative_correlation_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding. GLD is negatively correlated with the portfolio."
    )
    _assert_invalid(data, contains="not accompanied")


def test_single_asset_disclosure_unnegated_portfolio_offset_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding, and this asset offsets equity risk at the portfolio level."
    )
    _assert_invalid(data, contains="not accompanied")


def test_single_asset_disclosure_unnegated_portfolio_hedge_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding, and this provides a portfolio hedge."
    )
    _assert_invalid(data, contains="not accompanied")


@pytest.mark.parametrize("boundary_sentence", [
    "This is a single-asset historical characterization.",
    "This does not establish whole-portfolio diversification.",
    "This does not establish portfolio correlation.",
    "This does not resolve defensive_offset_interface.",
    "Whole-portfolio effects remain separately governed and unmeasured.",
])
def test_single_asset_disclosure_allowed_boundary_language_accepted(boundary_sentence):
    """Required boundary/disclosure language -- none of it references a
    substantive portfolio-level finding, so none should be rejected."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        f"This finding is single-asset and historical only. {boundary_sentence}"
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_never_negation_form_accepted():
    """The 'never' branch of the disclaiming-negation pattern, not just
    'does not' -- a genuine disclaimer phrased differently must still be
    accepted."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset, historical characterization. It never establishes a "
        "portfolio-level correlation or diversification-benefit finding for Portfolio-HQ's own current holdings."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_negation_does_not_launder_across_sentences():
    """Sentence-scoping must not let an unrelated negation elsewhere in
    the field excuse a real, unnegated claim in a different sentence --
    a fixed-character-window design (the reviewer's own naive suggestion)
    could be fooled by padding; sentence-scoping must not be."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding does not overreach in any way. Separately, GLD provides a diversification "
        "benefit to the current portfolio."
    )
    _assert_invalid(data, contains="not accompanied")


# ── second bounded correction: clause-scoped negation (not merely
# sentence-scoped) ────────────────────────────────────────────────────────
# A fresh independent exact-head delta review (pullrequestreview-4896559501)
# found the first correction's sentence-scoped negation check could still
# be bypassed: a genuine negation in one clause of a sentence can "shield"
# an unnegated whole-portfolio claim in a *different* clause of the same
# sentence, joined by a comma+conjunction, semicolon, or contrastive
# conjunction. These tests reproduce the reviewer's demonstrated bypass
# constructions and confirm the corrected, clause-scoped scan closes it.

@pytest.mark.parametrize("laundering_sentence", [
    "This assessment does not establish portfolio diversification, and GLD diversifies the whole portfolio.",
    "This assessment does not establish portfolio correlation; GLD is negatively correlated with the portfolio.",
    "This single-asset evidence does not resolve diversification, but GLD provides a portfolio hedge.",
    "This single-asset evidence does not establish diversification, but GLD provides a portfolio hedge.",
    "This finding does not compute a whole-portfolio diversification benefit, but gold reduces portfolio risk during equity drawdowns.",
    "This finding does not establish a portfolio-level diversification benefit; gold offsets portfolio risk during equity drawdowns.",
])
def test_single_asset_disclosure_same_sentence_cross_clause_laundering_rejected(laundering_sentence):
    """The exact class of bypass the independent review demonstrated:
    a genuine negation in one clause must not shield an unnegated
    whole-portfolio claim in a different clause of the same sentence."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        laundering_sentence
    )
    _assert_invalid(data, contains="not accompanied")


@pytest.mark.parametrize("laundering_sentence", [
    "This does not establish anything, and GLD reduces the portfolio's drawdown during equity crashes.",
    "This does not establish anything, and GLD offers a portfolio hedge against equity declines.",
    "This does not establish anything, and GLD offsets the portfolio's equity risk.",
    "This does not establish anything, and the portfolio's risk is reduced by GLD.",
])
def test_single_asset_disclosure_laundered_claim_variants_rejected(laundering_sentence):
    """Nearby variants of the laundering construction -- proving the fix
    is semantic (clause-scoped negation), not hardcoded to the reviewer's
    two exact example strings."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        laundering_sentence
    )
    _assert_invalid(data, contains="not accompanied")


@pytest.mark.parametrize("legit_sentence", [
    "This single-asset assessment does not establish whole-portfolio diversification or correlation.",
    "This does not establish portfolio diversification; it also does not establish portfolio correlation.",
    "This does not establish portfolio diversification. This does not establish portfolio correlation either.",
    "Whole-portfolio diversification and correlation effects remain separately governed by the overlap model.",
    "The defensive_offset_interface dimension, which would characterize any portfolio diversification benefit, remains unresolved.",
])
def test_single_asset_disclosure_clause_scoped_legitimate_disclaimers_accepted(legit_sentence):
    """Legitimate disclaimer constructions -- single-clause, semicolon-
    joined with both clauses non-assertive, two wholly separate negative
    sentences, and declarative-deferral phrasing -- must still validate
    clean under the clause-scoped design. Each is prefixed with the
    required single-asset marker sentence (SS6's mandatory disclosure
    requirement), matching test_single_asset_disclosure_allowed_boundary_
    language_accepted's own established fixture pattern."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        f"This finding is single-asset and historical only. {legit_sentence}"
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_multi_clause_disclaimer_with_deferral_accepted():
    """A multi-clause disclaimer where the second, comma+and-joined clause
    defers to governance rather than repeating a negation -- the
    declarative-deferral cue, not just the negation-verb cue, must satisfy
    the same-clause disclaiming-cue check."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset assessment; it does not establish whole-portfolio "
        "diversification, and portfolio correlation remains separately governed."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_negation_still_does_not_launder_across_sentences_clause_scoped():
    """The first correction's own cross-sentence laundering guard must
    still hold under the clause-scoped rewrite -- a negation in an earlier
    sentence must not excuse an unnegated claim in a wholly separate later
    sentence, regardless of clause boundaries within either one."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding does not overreach in any way. Separately, GLD provides a diversification "
        "benefit to the current portfolio."
    )
    _assert_invalid(data, contains="not accompanied")


def test_rationale_diversification_scan_still_unconditional_after_clause_scoping():
    """rationale's unconditional-block behavior (no negation or deferral
    carve-out of any kind) must remain unchanged by the clause-scoping
    rewrite, which touches only single_asset_disclosure's own scan."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"] = (
        "This does not establish that gold diversifies the whole portfolio, and portfolio "
        "effects remain separately governed."
    )
    _assert_invalid(data, contains="whole-portfolio diversification")


def test_single_asset_disclosure_real_disclaimer_text_accepted_clause_scoped():
    """The real sealed record's own single_asset_disclosure text (a
    semicolon-joined, multi-verb-list disclaimer) must still validate
    clean under the clause-scoped rewrite -- confirms the comma+'or'
    exclusion from the clause-boundary pattern was the correct fix for
    the regression the clause-scoping design first introduced."""
    data = yaml.safe_load(
        (REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml").read_text()
    )
    disclosure = data["instrument_specific_economic_characterization"][
        "historical_equity_drawdown_behavior"
    ]["single_asset_disclosure"]
    assert "does not compute, constitute, imply, or substitute" in disclosure
    errors: list[str] = []
    eav._scan_overlap_model_non_duplication(
        {"rationale": "", "single_asset_disclosure": disclosure}, errors
    )
    assert errors == []


# ── third bounded correction: matched-claim-scoped clause detection
# (broader boundary constructions, not merely a bigger punctuation list)
# ────────────────────────────────────────────────────────────────────────
# A second fresh independent exact-head delta review found the clause-
# scoped design's boundary detection recognized only a fixed subset of
# English clause boundaries -- ordinary, non-adversarial constructions
# (a comma-less bare "and"/"so"/"nor", an em dash/double hyphen, a colon,
# and "or" introducing a genuinely new independent clause) could all still
# bypass it. These tests reproduce the reviewer's demonstrated
# constructions and confirm the redesigned, matched-claim-scoped clause
# detection (`_split_clauses`, hard vs. soft boundary distinction) closes
# the whole vulnerability class rather than one more punctuation form.

@pytest.mark.parametrize("laundering_sentence", [
    "This does not compute a numeric hurdle rate and GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate so GLD diversifies the whole portfolio materially.",
    "This does not compute a numeric hurdle rate, nor GLD diversifies the whole portfolio.",
    "This does not compute a numeric hurdle rate — GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate -- GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate, or GLD diversifies the whole portfolio in every period.",
    "This does not compute a numeric hurdle rate: GLD diversifies the whole portfolio in every tested period.",
])
def test_single_asset_disclosure_broader_clause_boundary_laundering_rejected(laundering_sentence):
    """The exact class of bypass the second delta review demonstrated:
    a bare conjunction (no comma required), an em dash, a double hyphen,
    an independent-clause "or", and a colon must all be recognized as
    genuine clause boundaries, closing the specific gap left by the prior
    correction's narrower, punctuation-enumerated boundary pattern."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        laundering_sentence
    )
    _assert_invalid(data, contains="not accompanied")


@pytest.mark.parametrize("laundering_sentence", [
    "This does not establish anything and GLD reduces the portfolio's risk materially.",
    "This does not establish anything, or GLD offers a portfolio hedge against equity declines.",
    "This does not establish anything -- GLD offsets equity risk at the portfolio level.",
    "This does not establish anything; GLD is negatively correlated with the portfolio.",
    "This does not establish anything, or GLD diversifies the whole portfolio.",
])
def test_single_asset_disclosure_broader_boundary_claim_variants_rejected(laundering_sentence):
    """Nearby variants combining each newly-recognized boundary form with
    a different prohibited claim (reduces-risk/hedge/offsets/negatively-
    correlated/diversifies) -- proving the redesigned mechanism is
    semantic and generalizes across boundary form and claim wording
    together, not hardcoded to any one combination."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        laundering_sentence
    )
    _assert_invalid(data, contains="not accompanied")


@pytest.mark.parametrize("legit_sentence", [
    "This does not establish diversification, correlation, or hedge effectiveness.",
    "This single-asset assessment does not establish whole-portfolio diversification or correlation.",
])
def test_single_asset_disclosure_or_joined_object_list_still_accepted(legit_sentence):
    """The exact false-positive risk this correction's own redesign must
    avoid: "or" joining items within the SAME closed disclaiming-verb-
    word or diversification-concept-noun list (the object of a single
    negated verb) must remain a protected, non-boundary "or" -- distinct
    from an "or" that introduces a genuinely new independent clause."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        f"This finding is single-asset and historical only. {legit_sentence}"
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_real_disclaimer_verb_list_or_survives_broader_boundaries():
    """The real sealed record's own comma+'or' disclaiming-verb list
    ("does not compute, constitute, imply, or substitute for...") and its
    comma+'or' diversification-concept-noun list ("diversification-
    benefit or correlation finding") must both still survive as protected
    coordination under the broadened hard/soft boundary redesign -- not
    merely under the narrower second-correction pattern that first
    motivated excluding "or" from splitting altogether."""
    data = yaml.safe_load(
        (REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml").read_text()
    )
    disclosure = data["instrument_specific_economic_characterization"][
        "historical_equity_drawdown_behavior"
    ]["single_asset_disclosure"]
    assert "does not compute, constitute, imply, or substitute" in disclosure
    assert "diversification-benefit or correlation finding" in disclosure
    errors: list[str] = []
    eav._scan_overlap_model_non_duplication(
        {"rationale": "", "single_asset_disclosure": disclosure}, errors
    )
    assert errors == []


def test_single_asset_disclosure_prior_correction_bypasses_still_rejected_under_redesign():
    """Both of the second delta review's own exact bypass constructions
    (comma+'but', bare semicolon) must remain rejected under the third
    correction's redesigned clause detection -- confirms the redesign is
    a superset fix, not a lateral rewrite that reopens an already-closed
    gap."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This single-asset finding does not compute a numeric hurdle rate, but GLD diversifies "
        "the whole portfolio and materially reduces total portfolio drawdown, a real and "
        "significant portfolio-level benefit worth noting."
    )
    _assert_invalid(data, contains="not accompanied")

    data2 = _record(analytical_subject="GLD")
    data2["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This single-asset finding does not compute a numeric hurdle rate; GLD diversifies the "
        "whole portfolio and reduces total portfolio drawdown materially."
    )
    _assert_invalid(data2, contains="not accompanied")


def test_rationale_diversification_scan_still_unconditional_no_negation_carveout():
    """rationale keeps its original, stricter, unconditional-block
    behavior -- unlike single_asset_disclosure, a negated claim in
    rationale is still rejected, since rationale is never expected to
    discuss the portfolio-level boundary at all."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"] = (
        "This does not establish that gold diversifies the whole portfolio."
    )
    _assert_invalid(data, contains="whole-portfolio diversification")


def test_real_gld_rationale_contains_no_portfolio_language_unaffected_by_broadened_patterns():
    """The real sealed record's own rationale text (which legitimately
    uses the word 'hedge' in a non-portfolio sense -- 'not a clean hedge
    relationship') must remain unaffected by the broadened pattern set,
    since it never mentions 'portfolio' at all."""
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml").read_text())
    rationale = data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"]
    assert "portfolio" not in rationale.lower()
    errors: list[str] = []
    eav._scan_overlap_model_non_duplication({"rationale": rationale, "single_asset_disclosure": "placeholder single-asset text"}, errors)
    assert errors == []


# ── CASH-vs-RESERVE distinction leakage (SS11 point 15) ──────────────────

def test_distinction_leakage_reserve_functions_as_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["deployability_and_optionality"]["rationale"] = "RESERVE functions as a dedicated safety buffer."
    _assert_invalid(data, contains="individually warrant")


def test_distinction_leakage_cash_is_used_for_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["deployability_and_optionality"]["rationale"] = "CASH is used for near-term operational needs."
    _assert_invalid(data)


def test_distinction_leakage_different_purpose_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["deployability_and_optionality"]["rationale"] = "CASH and RESERVE serve a different purpose within the book."
    _assert_invalid(data)


def test_distinction_leakage_reserve_is_intended_for_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["deployability_and_optionality"]["rationale"] = "RESERVE is intended for drawdown protection specifically."
    _assert_invalid(data)


def test_distinction_leakage_individually_warrants_rejected():
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["deployability_and_optionality"]["rationale"] = "RESERVE individually warrants a lower optionality rating."
    _assert_invalid(data)


def test_distinction_leakage_only_fires_on_cash_like_capital_records():
    """The scan is scoped to CASH_LIKE_CAPITAL records only -- a GLD
    record's own free text is not scanned for this pattern (it has
    nothing to do with CASH/RESERVE)."""
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["rationale"] = "RESERVE functions as a dedicated safety buffer."
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_neutral_dual_citation_of_cash_and_reserve_accepted():
    """Positive test: a record that cites both legacy identifiers
    neutrally, without asserting a distinction, is accepted (SS12's own
    required positive test)."""
    data = _record(analytical_subject="CASH_LIKE_CAPITAL")
    data["deployability_and_optionality"]["rationale"] = (
        "This family combines the legacy CASH and RESERVE identifiers, both already-sealed as "
        "immediately liquid, and is evaluated here as one combined, undifferentiated whole."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


# ── abstention behavior ──────────────────────────────────────────────────

def test_unable_to_determine_without_abstention_reason_rejected():
    data = _record(analytical_subject="GLD", deployability_and_optionality=_deployability(deployability_category="unable_to_determine"))
    _assert_invalid(data, contains="abstention_reason")


def test_abstention_reason_present_without_unable_to_determine_rejected():
    data = _record(analytical_subject="GLD")
    data["deployability_and_optionality"]["abstention_reason"] = "should not be here"
    _assert_invalid(data, contains="must be absent")


def test_fully_abstained_gld_record_accepted_as_sealed_eligible():
    data = _record(
        analytical_subject="GLD",
        deployability_and_optionality=_deployability(deployability_category="unable_to_determine", abstention_reason="no evidence"),
        instrument_specific_economic_characterization=_instrument_specific_gld(
            cost_and_tracking_economic_significance=_cost_tracking(significance_category="unable_to_determine", abstention_reason="no evidence"),
            historical_inflation_sensitivity=_inflation_sensitivity(sensitivity_category="unable_to_determine", abstention_reason="no evidence"),
            historical_equity_drawdown_behavior=_drawdown_behavior(behavior_category="unable_to_determine", abstention_reason="no evidence"),
        ),
        abstention_index=[
            {"axis": "deployability_and_optionality", "field": "deployability_category", "value": "unable_to_determine", "reason": "no evidence"},
            {"axis": "instrument_specific_economic_characterization.cost_and_tracking_economic_significance", "field": "significance_category", "value": "unable_to_determine", "reason": "no evidence"},
            {"axis": "instrument_specific_economic_characterization.historical_inflation_sensitivity", "field": "sensitivity_category", "value": "unable_to_determine", "reason": "no evidence"},
            {"axis": "instrument_specific_economic_characterization.historical_equity_drawdown_behavior", "field": "behavior_category", "value": "unable_to_determine", "reason": "no evidence"},
        ],
        sealed=True,
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_abstention_index_missing_entry_for_real_abstention_rejected():
    data = _record(
        analytical_subject="GLD",
        deployability_and_optionality=_deployability(deployability_category="unable_to_determine", abstention_reason="no evidence"),
        abstention_index=[],
    )
    _assert_invalid(data, contains="abstention_index is missing an entry")


def test_abstention_does_not_cascade_between_deployability_and_instrument_specific():
    data = _record(
        analytical_subject="GLD",
        deployability_and_optionality=_deployability(deployability_category="unable_to_determine", abstention_reason="no evidence"),
        abstention_index=[{"axis": "deployability_and_optionality", "field": "deployability_category", "value": "unable_to_determine", "reason": "no evidence"}],
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_abstention_does_not_cascade_between_instrument_specific_sub_fields():
    data = _record(
        analytical_subject="GLD",
        instrument_specific_economic_characterization=_instrument_specific_gld(
            historical_inflation_sensitivity=_inflation_sensitivity(sensitivity_category="unable_to_determine", abstention_reason="no evidence"),
        ),
        abstention_index=[{"axis": "instrument_specific_economic_characterization.historical_inflation_sensitivity", "field": "sensitivity_category", "value": "unable_to_determine", "reason": "no evidence"}],
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_non_cascading_abstention_cash_like_capital_determined_regardless_of_reserve_yaml_own_abstention():
    """SS12's own required non-cascading test: a synthetic CASH_LIKE_
    CAPITAL record with deployability_and_optionality determined
    validates clean regardless of RESERVE.yaml's own separately-sealed
    functional_role abstention -- this schema imposes no cross-schema
    cascade."""
    reserve_data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "RESERVE.yaml").read_text())
    assert reserve_data["functional_role"]["role_category"] == "unable_to_determine"

    data = _record(analytical_subject="CASH_LIKE_CAPITAL", sealed=True)
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors
    assert data["deployability_and_optionality"]["deployability_category"] != "unable_to_determine"


# ── manifest reconciliation ───────────────────────────────────────────────

def test_manifest_duplicate_entry_rejected():
    gld = _record(analytical_subject="GLD", sealed=True)
    manifest = {
        "schema_version": "1.0", "governing_decision": "XASSET-0009",
        "cohort": [
            {"analytical_subject": "GLD", "sealed_at": gld["sealed_at"], "content_sha256": gld["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "intelligence/economic_assessment/GLD.yaml"},
            {"analytical_subject": "GLD", "sealed_at": gld["sealed_at"], "content_sha256": gld["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "intelligence/economic_assessment/GLD.yaml"},
        ],
    }
    result = eav.validate_cohort_manifest(manifest, {"GLD": gld})
    assert not result.valid
    assert any("more than once" in e for e in result.errors)


def test_manifest_missing_entry_from_population_rejected():
    gld = _record(analytical_subject="GLD", sealed=True)
    manifest = {
        "schema_version": "1.0", "governing_decision": "XASSET-0009",
        "cohort": [{"analytical_subject": "GLD", "sealed_at": gld["sealed_at"], "content_sha256": gld["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "intelligence/economic_assessment/GLD.yaml"}],
    }
    result = eav.validate_cohort_manifest(manifest, {"GLD": gld})
    assert not result.valid
    assert any("missing authorized" in e for e in result.errors)


def test_manifest_extra_entry_beyond_population_rejected():
    gld = _record(analytical_subject="GLD", sealed=True)
    manifest = {
        "schema_version": "1.0", "governing_decision": "XASSET-0009",
        "cohort": [{"analytical_subject": "SPY", "sealed_at": "x", "content_sha256": "x", "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "x"}],
    }
    result = eav.validate_cohort_manifest(manifest, {"SPY": {}}, authorized_population=eav.AUTHORIZED_POPULATION)
    assert not result.valid
    assert any("outside the authorized population" in e for e in result.errors)


def test_manifest_orphan_sealed_record_rejected():
    gld = _record(analytical_subject="GLD", sealed=True)
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0009", "cohort": []}
    result = eav.validate_cohort_manifest(manifest, {"GLD": gld}, authorized_population=frozenset())
    assert not result.valid
    assert any("no corresponding cohort manifest entry" in e for e in result.errors)


def test_manifest_hash_mismatch_rejected():
    gld = _record(analytical_subject="GLD", sealed=True)
    manifest = {
        "schema_version": "1.0", "governing_decision": "XASSET-0009",
        "cohort": [{"analytical_subject": "GLD", "sealed_at": gld["sealed_at"], "content_sha256": "0" * 64, "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "intelligence/economic_assessment/GLD.yaml"}],
    }
    result = eav.validate_cohort_manifest(manifest, {"GLD": gld})
    assert not result.valid
    assert any("content_sha256 mismatch" in e for e in result.errors)


def test_manifest_full_population_valid():
    gld = _record(analytical_subject="GLD", sealed=True)
    cash_like = _record(analytical_subject="CASH_LIKE_CAPITAL", sealed=True)
    manifest = {
        "schema_version": "1.0", "governing_decision": "XASSET-0009",
        "cohort": [
            {"analytical_subject": "GLD", "sealed_at": gld["sealed_at"], "content_sha256": gld["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "intelligence/economic_assessment/GLD.yaml"},
            {"analytical_subject": "CASH_LIKE_CAPITAL", "sealed_at": cash_like["sealed_at"], "content_sha256": cash_like["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0009", "record_path": "intelligence/economic_assessment/CASH_LIKE_CAPITAL.yaml"},
        ],
    }
    result = eav.validate_cohort_manifest(manifest, {"GLD": gld, "CASH_LIKE_CAPITAL": cash_like})
    assert result.valid, result.errors


# ── envelope projection consistency ──────────────────────────────────────

def test_deployability_summary_mismatch_rejected():
    data = _record(analytical_subject="GLD")
    data["cross_asset_handoff"]["deployability_summary"] = "moderate_optionality"
    _assert_invalid(data, contains="deployability_summary")


def test_instrument_specific_summary_mismatch_rejected():
    data = _record(analytical_subject="GLD")
    data["cross_asset_handoff"]["instrument_specific_summary"] = {"not_applicable": True}
    _assert_invalid(data, contains="instrument_specific_summary")


def test_evidence_quality_summary_mismatch_rejected():
    data = _record(analytical_subject="GLD")
    data["cross_asset_handoff"]["evidence_quality_summary"] = "comprehensive"
    _assert_invalid(data, contains="evidence_quality_summary")


def test_uncertainty_summary_envelope_mismatch_rejected():
    data = _record(analytical_subject="GLD")
    data["cross_asset_handoff"]["uncertainty_summary"] = "different text"
    _assert_invalid(data, contains="uncertainty_summary")


def test_cross_asset_handoff_absent_entirely_rejected():
    data = _record(analytical_subject="GLD")
    del data["cross_asset_handoff"]
    _assert_invalid(data, contains="cross_asset_handoff")


def test_cross_asset_handoff_missing_one_required_key_rejected():
    data = _record(analytical_subject="GLD")
    del data["cross_asset_handoff"]["evidence_quality_summary"]
    _assert_invalid(data, contains="missing required key")


# ── deterministic output / canonical hashing ─────────────────────────────

def test_deterministic_validation_output():
    data = _record(analytical_subject="GLD", sealed=True)
    r1 = eav.validate_economic_assessment_data(copy.deepcopy(data), repo_root=REPO_ROOT)
    r2 = eav.validate_economic_assessment_data(copy.deepcopy(data), repo_root=REPO_ROOT)
    assert r1.valid == r2.valid == True
    assert r1.errors == r2.errors == []


def test_canonical_record_hash_deterministic():
    data = _record(analytical_subject="GLD", sealed=True)
    h1 = eav.canonical_record_hash(data)
    h2 = eav.canonical_record_hash(data)
    assert h1 == h2


def test_canonical_record_hash_excludes_only_seal_fields():
    data = _record(analytical_subject="GLD", sealed=True)
    mutated = copy.deepcopy(data)
    mutated["sealed_at"] = "2099-01-01T00:00:00Z"
    mutated["governing_decision"] = "SOMETHING-ELSE"
    mutated["drafting_session_or_shard_id"] = "different-shard"
    mutated["cohort_manifest_entry"] = "different#entry"
    assert eav.canonical_record_hash(mutated) == eav.canonical_record_hash(data)

    mutated2 = copy.deepcopy(data)
    mutated2["deployability_and_optionality"]["deployability_category"] = "moderate_optionality"
    assert eav.canonical_record_hash(mutated2) != eav.canonical_record_hash(data)


def test_sealed_record_content_hash_must_reproduce():
    data = _record(analytical_subject="GLD", sealed=True)
    data["content_sha256"] = "0" * 64
    _assert_invalid(data, contains="does not reproduce")


def test_draft_record_does_not_require_seal_fields():
    data = _record(analytical_subject="GLD", sealed=False)
    for k in eav._SEAL_REQUIRED_KEYS:
        assert k not in data
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


# ── filename stem matching ─────────────────────────────────────────────────

def test_filename_stem_mismatch_rejected(tmp_path):
    data = _record(analytical_subject="GLD", sealed=True)
    path = tmp_path / "WRONG_NAME.yaml"
    path.write_text(yaml.safe_dump(data))
    result = eav.validate_economic_assessment_file(path)
    assert not result.valid
    assert any("does not match" in e for e in result.errors)


def test_filename_stem_match_accepted(tmp_path):
    data = _record(analytical_subject="GLD", sealed=True)
    path = tmp_path / "GLD.yaml"
    path.write_text(yaml.safe_dump(data))
    result = eav.validate_economic_assessment_file(path)
    assert result.valid, result.errors


def test_malformed_yaml_file_rejected(tmp_path):
    path = tmp_path / "GLD.yaml"
    path.write_text(": not: valid: yaml: [")
    result = eav.validate_economic_assessment_file(path)
    assert not result.valid


def test_missing_file_rejected(tmp_path):
    result = eav.validate_economic_assessment_file(tmp_path / "DOES_NOT_EXIST.yaml")
    assert not result.valid


def test_empty_file_rejected(tmp_path):
    path = tmp_path / "GLD.yaml"
    path.write_text("")
    result = eav.validate_economic_assessment_file(path)
    assert not result.valid


def test_missing_directory_is_valid_zero_coverage_state(tmp_path):
    result = eav.validate_economic_assessment_directory(tmp_path / "does_not_exist")
    assert result.valid
    assert result.record_count == 0


# ── protected-path isolation ────────────────────────────────────────────────

_PROTECTED_PATHS = [
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "allocate.py", "margin_state.py", "levels.py",
]


def test_protected_paths_untouched_by_this_module_import():
    hashes_before = {}
    for rel in _PROTECTED_PATHS:
        p = REPO_ROOT / rel
        if p.is_file():
            hashes_before[rel] = p.read_bytes()

    eav.validate_economic_assessment_directory(REPO_ROOT / "intelligence" / "economic_assessment", repo_root=REPO_ROOT)

    for rel, before in hashes_before.items():
        assert (REPO_ROOT / rel).read_bytes() == before, f"{rel} was mutated"


def test_protected_intelligence_records_untouched():
    """Zero diff on every existing intelligence/classification|companies|
    themes|relationships|etf_classification|crypto_classification|
    functional_doctrine|overlap_model/ record -- checked via a live git
    status, so a staged-but-uncommitted change would also be caught.
    CASH.yaml/RESERVE.yaml/GLD.yaml/GLD_DEFENSIVE_ROLE.yaml explicitly
    included -- referenced by hash pin, never modified."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--",
         "intelligence/etf_classification", "intelligence/crypto_classification",
         "intelligence/classification", "intelligence/companies", "intelligence/themes",
         "intelligence/relationships", "intelligence/functional_doctrine", "intelligence/overlap_model"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert result.stdout.strip() == "", f"unexpected changes under protected intelligence paths:\n{result.stdout}"


# ── allocator/margin import-coupling isolation ─────────────────────────────

def test_validator_module_imports_neither_allocate_nor_margin_state():
    source = (REPO_ROOT / "economic_assessment_validator.py").read_text()
    tree = ast.parse(source)
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module)
    assert "allocate" not in imported_names
    assert "margin_state" not in imported_names


def test_allocate_and_margin_state_do_not_import_this_validator():
    for module_file in ("allocate.py", "margin_state.py"):
        path = REPO_ROOT / module_file
        if not path.is_file():
            continue
        source = path.read_text()
        assert "economic_assessment_validator" not in source


# ── real repository directory scan ──────────────────────────────────────────

def test_real_repository_economic_assessment_directory_all_valid():
    result = eav.validate_economic_assessment_directory(
        REPO_ROOT / "intelligence" / "economic_assessment", repo_root=REPO_ROOT,
    )
    assert result.valid, [(r.source, r.errors) for r in result.results if not r.valid]


def test_real_repository_economic_assessment_directory_exact_population():
    manifest_path = REPO_ROOT / "intelligence" / "economic_assessment" / "COHORT_MANIFEST.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    subjects = {row["analytical_subject"] for row in manifest["cohort"]}
    assert subjects == eav.AUTHORIZED_POPULATION


def test_real_economic_assessment_files_exact_two_analytical_subjects():
    directory = REPO_ROOT / "intelligence" / "economic_assessment"
    stems = {p.stem for p in directory.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    assert stems == eav.AUTHORIZED_POPULATION


def test_real_gld_structural_references_match_live_sealed_records():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml").read_text())
    gld_etf = yaml.safe_load((REPO_ROOT / "intelligence" / "etf_classification" / "GLD.yaml").read_text())
    gdr_fd = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "GLD_DEFENSIVE_ROLE.yaml").read_text())
    assert data["structural_reference_etf_classification"]["referenced_content_sha256"] == etf.canonical_record_hash(gld_etf)
    assert data["structural_reference_functional_doctrine"]["referenced_content_sha256"] == fdv.canonical_record_hash(gdr_fd)


def test_real_cash_like_capital_legacy_references_match_live_sealed_records():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "CASH_LIKE_CAPITAL.yaml").read_text())
    cash_fd = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "CASH.yaml").read_text())
    reserve_fd = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "RESERVE.yaml").read_text())
    refs = {r["source_capital_use_type"]: r for r in data["legacy_structural_references"]}
    assert refs["CASH"]["referenced_content_sha256"] == fdv.canonical_record_hash(cash_fd)
    assert refs["RESERVE"]["referenced_content_sha256"] == fdv.canonical_record_hash(reserve_fd)


def test_real_gld_record_has_zero_abstentions():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml").read_text())
    assert data["abstention_index"] == []


def test_real_cash_like_capital_record_has_zero_abstentions():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "CASH_LIKE_CAPITAL.yaml").read_text())
    assert data["abstention_index"] == []


def test_real_cash_like_capital_record_never_asserts_a_cash_reserve_distinction():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "CASH_LIKE_CAPITAL.yaml").read_text())
    errors: list[str] = []
    eav._scan_distinction_leakage(data, "CASH_LIKE_CAPITAL", errors)
    assert errors == []


def test_real_gld_record_carries_single_asset_disclosure():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml").read_text())
    disclosure = data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"]
    assert "single-asset" in disclosure.lower() or "single asset" in disclosure.lower()


def test_real_no_overlap_model_field_names_appear_anywhere_in_economic_assessment_records():
    for subject in sorted(eav.AUTHORIZED_POPULATION):
        data = yaml.safe_load((REPO_ROOT / "intelligence" / "economic_assessment" / f"{subject}.yaml").read_text())
        errors: list[str] = []
        eav._scan_forbidden_keys(data, subject, errors)
        assert errors == [], (subject, errors)


def test_real_defensive_offset_interface_dimension_unaffected_and_still_forced():
    """XASSET-0009 SSF: this filing's own implementation must not loosen
    defensive_offset_interface's own forced not_yet_computable_
    interface_only value."""
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "overlap_model" / "defensive_offset_interface.yaml").read_text())
    assert data["computation_status"] == "not_yet_computable_interface_only"


def test_real_debt_reduction_functional_doctrine_record_unaffected():
    """DEBT_REDUCTION's own economic-assessment gap remains entirely
    outside this implementation's scope -- its sealed functional-
    doctrine record's forced readiness values are untouched."""
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "DEBT_REDUCTION.yaml").read_text())
    assert data["economic_assessment_readiness"]["avoided_borrowing_cost_readiness"]["status"] == "assessment_required"
    assert data["economic_assessment_readiness"]["survivability_and_buffer_benefit_readiness"]["status"] == "assessment_required"
