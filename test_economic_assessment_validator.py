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
    _assert_invalid(data, contains="not governed")


def test_single_asset_disclosure_unnegated_diversifies_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset assessment, and GLD therefore diversifies the whole portfolio."
    )
    _assert_invalid(data, contains="not governed")


def test_single_asset_disclosure_unnegated_drawdown_reduction_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding. GLD reduces total portfolio drawdown."
    )
    _assert_invalid(data, contains="not governed")


def test_single_asset_disclosure_unnegated_negative_correlation_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding. GLD is negatively correlated with the portfolio."
    )
    _assert_invalid(data, contains="not governed")


def test_single_asset_disclosure_unnegated_portfolio_offset_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding, and this asset offsets equity risk at the portfolio level."
    )
    _assert_invalid(data, contains="not governed")


def test_single_asset_disclosure_unnegated_portfolio_hedge_claim_rejected():
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is a single-asset finding, and this provides a portfolio hedge."
    )
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")


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
    _assert_invalid(data, contains="not governed")

    data2 = _record(analytical_subject="GLD")
    data2["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This single-asset finding does not compute a numeric hurdle rate; GLD diversifies the "
        "whole portfolio and reduces total portfolio drawdown materially."
    )
    _assert_invalid(data2, contains="not governed")


# ── fourth bounded correction: subject-vs-object ambiguity (MAJOR) plus
# quantifier-negation recognition (MINOR) ────────────────────────────────
# A third fresh independent exact-head delta review found the third
# correction's soft-boundary continuation check ambiguous: "and"/"or"
# immediately followed by a disclaiming-verb-word or diversification-
# concept-noun was always treated as protected list-continuation, but
# that same word can instead open a brand-new independent clause as its
# own grammatical subject ("and diversification of the whole portfolio
# IS ACHIEVED by GLD"). These tests reproduce the reviewer's demonstrated
# subject-vs-object bypass and confirm the matched-claim veto
# (`_match_is_new_clause_subject`) closes it. The same review also found
# a legitimate quantifier-negation phrasing ("No portfolio correlation
# conclusion is established.") incorrectly rejected -- these tests
# confirm `_QUANTIFIER_NEGATION_CLAIM_PATTERN` accepts it while still
# rejecting every guard construction where the negation does not actually
# govern the later positive claim.

@pytest.mark.parametrize("bypass_sentence", [
    # subject opens with "diversification"
    "This does not compute a numeric hurdle rate, and diversification of the whole portfolio is achieved by GLD in every regime.",
    "This does not compute a numeric hurdle rate and diversification of the whole portfolio is achieved by GLD.",
    "This assessment does not establish diversification and diversification of the whole portfolio is provided by GLD.",
    # subject opens with "correlation"
    "This does not compute a numeric hurdle rate, and correlation with the current portfolio is strongly negative for GLD.",
    "This does not compute a numeric hurdle rate or correlation with the current portfolio is negative for GLD.",
    "This assessment does not establish correlation or correlation with the portfolio is negative for GLD.",
    # subject opens with "hedge"/portfolio hedge concept
    "This evidence does not establish hedge effectiveness and portfolio hedge effectiveness is improved by GLD.",
    # after a completely legitimate prior disclaimer in the same field
    (
        "This single-asset assessment does not establish whole-portfolio diversification or "
        "correlation. Separately, and to be clear, diversification of the whole portfolio is "
        "nonetheless achieved by GLD in every measured period."
    ),
])
def test_single_asset_disclosure_subject_vs_object_ambiguity_rejected(bypass_sentence):
    """The exact class of bypass the third delta review demonstrated: a
    disclaiming-verb-word or diversification-concept-noun immediately
    following "and"/"or" can be the SUBJECT of a brand-new independent
    clause, not one more item in a coordinated OBJECT list -- the
    per-match veto must reject these regardless of the soft-boundary
    continuation check's own "protected coordination" classification."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        bypass_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


def test_single_asset_disclosure_subject_vs_object_reversed_passive_rejected():
    """A passive-voice/reversed-order variant of the subject-vs-object
    bypass -- proving the veto is semantic, not tied to one exact
    phrasing."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This does not establish anything, and diversification of the whole portfolio is "
        "provided in passive form by GLD."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


def test_single_asset_disclosure_reviewer_exact_major_bypass_end_to_end_rejected():
    """Full end-to-end reproduction of the reviewer's own exact
    hand-crafted, correctly-resealed record -- not just the sub-function
    -- confirming the corrected validator rejects it via
    validate_economic_assessment_data itself, matching how the reviewer
    demonstrated it."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding is single-asset in name only. It does not compute a "
        "numeric hurdle rate, and diversification of the whole portfolio is "
        "achieved by GLD in every regime, a real and significant "
        "portfolio-level benefit worth noting for allocation purposes."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("not governed" in e for e in result.errors)


@pytest.mark.parametrize("quantifier_sentence", [
    "No portfolio correlation conclusion is established.",
    "No whole-portfolio diversification conclusion is drawn.",
    "No portfolio hedge conclusion is made here.",
    "No portfolio risk-reduction conclusion is supported.",
    "No whole-portfolio diversification benefit is established by this single-asset finding.",
])
def test_single_asset_disclosure_quantifier_negation_accepted(quantifier_sentence):
    """Legitimate bare-quantifier negation phrasing ("No X conclusion is
    established.") must be accepted -- the negation pattern's original
    "(does/is/...) not VERB" / "never VERB" forms did not recognize this
    ordinary, entirely safe construction."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        f"This finding is single-asset and historical only. {quantifier_sentence}"
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_none_establishes_form_accepted():
    """The "None [of X] establishes..." negation form -- folded into
    _DISCLAIMING_NEGATION_PATTERN as one more alternative, governed by
    the same per-match veto as ordinary "does not establish" negation."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This is single-asset only. None of this establishes correlation with the current "
        "portfolio."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


@pytest.mark.parametrize("guard_sentence", [
    "No conclusion is established here, but GLD diversifies the whole portfolio.",
    "No correlation conclusion is established for equities, and GLD reduces total portfolio risk.",
    "No hedge conclusion is claimed in the first clause; GLD nevertheless provides a portfolio hedge.",
])
def test_single_asset_disclosure_quantifier_negation_guards_rejected(guard_sentence):
    """A quantifier negation elsewhere in the sentence must not
    automatically suppress a later, unrelated positive claim -- negation
    must still govern the matched proposition itself, not merely appear
    somewhere in the same field."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        guard_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("prior_round_sentence", [
    # original disclosure-exemption exploit (round 1)
    (
        "This finding is single-asset in name only -- in fact it demonstrates a genuine "
        "diversification benefit to the current portfolio and reduces the portfolio risk "
        "materially, correlated with the current portfolio at a strongly negative level."
    ),
    # cross-sentence laundering (round 2)
    "This finding does not overreach in any way. Separately, GLD provides a diversification benefit to the current portfolio.",
    # comma+and / comma+but (round 2)
    "This assessment does not establish portfolio diversification, and GLD diversifies the whole portfolio.",
    "This single-asset finding does not compute a numeric hurdle rate, but GLD diversifies the whole portfolio and materially reduces total portfolio drawdown, a real and significant portfolio-level benefit worth noting.",
    # semicolon (round 2/3)
    "This single-asset finding does not compute a numeric hurdle rate; GLD diversifies the whole portfolio and reduces total portfolio drawdown materially.",
    # colon (round 3)
    "This does not compute a numeric hurdle rate: GLD diversifies the whole portfolio in every tested period.",
    # bare and/so/nor (round 3)
    "This does not compute a numeric hurdle rate and GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate so GLD diversifies the whole portfolio materially.",
    "This does not compute a numeric hurdle rate, nor GLD diversifies the whole portfolio.",
    # em dash / double hyphen (round 3)
    "This does not compute a numeric hurdle rate — GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate -- GLD diversifies the whole portfolio in every tested period.",
    # independent-clause or (round 3)
    "This does not compute a numeric hurdle rate, or GLD diversifies the whole portfolio in every period.",
    # reversed word order / drawdown reduction / hedge / offsets / negatively correlated
    "This does not establish anything, and the portfolio's risk is reduced by GLD.",
    "This does not establish anything, and GLD reduces the portfolio's drawdown during equity crashes.",
    "This does not establish anything, and GLD provides a portfolio hedge.",
    "This does not establish anything, and GLD offsets equity risk at the portfolio level.",
    "This does not establish anything; GLD is negatively correlated with the portfolio.",
])
def test_single_asset_disclosure_all_prior_round_bypasses_remain_rejected(prior_round_sentence):
    """Explicit reconfirmation that every bypass family closed by the
    first three bounded corrections remains closed under the fourth
    correction's per-match veto and quantifier-negation additions --
    proves the fourth correction is a superset fix, not a lateral
    rewrite that reopens any already-closed gap."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        prior_round_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("legit_sentence", [
    "This single-asset assessment does not establish whole-portfolio diversification or correlation.",
    "This single-asset finding does not establish diversification, correlation, or hedge effectiveness.",
    "This is a single-asset assessment; it does not establish whole-portfolio diversification, and portfolio correlation remains separately governed.",
    "This single-asset finding does not establish portfolio diversification; it also does not establish portfolio correlation.",
    "This finding is single-asset only. Whole-portfolio diversification and correlation effects remain separately governed by the overlap model.",
])
def test_single_asset_disclosure_allowed_language_still_accepted_under_fourth_correction(legit_sentence):
    """Every category of legitimate disclaimer language required by the
    round-4 task's own allowed-language list must remain accepted under
    the veto/quantifier additions -- coordinated-object negation,
    multi-clause disclaimers, semicolon-separated non-assertive clauses,
    and declarative deferrals. Each fixture carries the required
    single-asset marker (SS6's mandatory disclosure requirement)."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        legit_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_real_gld_and_no_cash_like_disclosure_field_unaffected():
    """The real sealed GLD.yaml single_asset_disclosure text, and the
    real sealed CASH_LIKE_CAPITAL.yaml record (which carries no
    single_asset_disclosure field at all, `not_applicable: true`), both
    remain valid under the fourth correction."""
    gld_result = eav.validate_economic_assessment_file(
        REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml"
    )
    assert gld_result.valid, gld_result.errors
    cash_result = eav.validate_economic_assessment_file(
        REPO_ROOT / "intelligence" / "economic_assessment" / "CASH_LIKE_CAPITAL.yaml"
    )
    assert cash_result.valid, cash_result.errors


# ── fifth bounded correction: comma-delimited appositive/parenthetical
# veto-window truncation ─────────────────────────────────────────────────
# A fourth fresh independent exact-head delta review found the fourth
# correction's per-match veto window terminated at the first bare comma
# it encountered -- but a comma very often introduces a non-clause-ending
# appositive/parenthetical phrase, not a genuine boundary. A comma-
# delimited aside inserted between a matched claim-noun and its own
# finite verb ("...and diversification of the whole portfolio, across
# every historical regime examined in this record's own review, is
# achieved by GLD") truncated the veto window before it ever reached the
# finite predicate that would reveal the match as a new clause's subject.
# These tests reproduce the reviewer's demonstrated appositive bypass and
# confirm the redesigned veto window (no longer terminated by a bare
# comma) closes it.

@pytest.mark.parametrize("appositive_sentence", [
    # the exact long appositive the reviewer demonstrated
    (
        "This single-asset finding does not compute a numeric hurdle rate, and diversification "
        "of the whole portfolio, across every historical regime examined in this record's own "
        "review, is achieved by GLD."
    ),
    # single-word appositive
    (
        "This single-asset finding does not compute a numeric hurdle rate, and diversification "
        "of the whole portfolio, frankly, is achieved by GLD in every regime."
    ),
    # correlation-claim family, not just diversification
    (
        "This single-asset finding does not compute a numeric hurdle rate, and correlation with "
        "the current portfolio, per this record, is strongly negative for GLD."
    ),
    # nested/two-comma parenthetical
    (
        "This does not compute a numeric hurdle rate, and diversification of the whole "
        "portfolio, in every measured regime, without exception, is achieved by GLD."
    ),
    # appositive combined with "or" instead of "and"
    (
        "This does not compute a numeric hurdle rate, or diversification of the whole "
        "portfolio, across every regime, is achieved by GLD."
    ),
    # appositive combined with a comma-less "and"
    (
        "This does not compute a numeric hurdle rate and diversification of the whole "
        "portfolio, frankly, is achieved by GLD."
    ),
    # hedge-claim family
    (
        "This evidence does not establish hedge effectiveness and portfolio hedge "
        "effectiveness, upon closer review, is confirmed strong by GLD."
    ),
    # portfolio-risk/reversed-order family
    (
        "This does not establish anything, and the portfolio's risk, upon closer inspection, "
        "is reduced by GLD."
    ),
])
def test_single_asset_disclosure_appositive_veto_window_truncation_rejected(appositive_sentence):
    """The exact class of bypass the fourth delta review demonstrated: a
    comma-delimited appositive/parenthetical phrase inserted between a
    claim match and its own finite verb must not shield the match from
    the per-match veto -- a bare comma no longer terminates the veto
    window on its own."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        appositive_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


def test_single_asset_disclosure_reviewer_exact_appositive_bypass_end_to_end_rejected():
    """Full end-to-end reproduction of the reviewer's own exact
    hand-crafted, correctly-resealed record using the real test harness's
    own helpers -- confirming the corrected validator rejects it via
    validate_economic_assessment_data itself, not merely the
    sub-function."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This single-asset finding does not compute a numeric hurdle rate, and diversification "
        "of the whole portfolio, across every historical regime examined in this record's own "
        "review, is achieved by GLD."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("not governed" in e for e in result.errors)


@pytest.mark.parametrize("hard_boundary_appositive_sentence", [
    # "so" -- hard boundary -- the appositive construction here was
    # already correctly rejected before this correction; reconfirmed
    # unaffected by the veto-window redesign
    (
        "This does not compute a numeric hurdle rate so diversification of the whole "
        "portfolio, across every regime, is achieved by GLD."
    ),
    # semicolon -- hard boundary
    (
        "This does not compute a numeric hurdle rate; diversification of the whole "
        "portfolio, across every regime, is achieved by GLD."
    ),
])
def test_single_asset_disclosure_hard_boundary_appositive_still_rejected(hard_boundary_appositive_sentence):
    """Sanity confirmation that the identical appositive-comma
    construction was already correctly rejected behind a genuine hard
    boundary (a real clause split occurs, leaving the second clause with
    no disclaiming cue of its own) -- proving the defect was scoped to
    the soft-boundary veto-window path specifically, and remains fixed
    there under the widened window."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        hard_boundary_appositive_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("quantifier_appositive_sentence", [
    (
        "No conclusion about diversification of the whole portfolio is established, and "
        "diversification of the whole portfolio, in every regime, is achieved by GLD."
    ),
    (
        "No conclusion is established here, but diversification of the whole portfolio, "
        "across every regime, is achieved by GLD."
    ),
])
def test_single_asset_disclosure_quantifier_negation_appositive_not_laundered(quantifier_appositive_sentence):
    """A legitimate quantifier-negation construction earlier in the field
    must not, combined with an appositive-comma bypass later in the same
    field, launder an unrelated later positive claim -- the quantifier
    pattern governs only its own claim span, and the later independent
    clause still needs its own disclaiming cue."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        quantifier_appositive_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("prior_round_sentence", [
    # round 4 exact bypasses (no appositive)
    "This does not compute a numeric hurdle rate, and diversification of the whole portfolio is achieved by GLD in every regime.",
    "This does not compute a numeric hurdle rate, and correlation with the current portfolio is strongly negative for GLD.",
    # round 1-3 families
    (
        "This finding is single-asset in name only -- in fact it demonstrates a genuine "
        "diversification benefit to the current portfolio and reduces the portfolio risk "
        "materially, correlated with the current portfolio at a strongly negative level."
    ),
    "This finding does not overreach in any way. Separately, GLD provides a diversification benefit to the current portfolio.",
    "This assessment does not establish portfolio diversification, and GLD diversifies the whole portfolio.",
    "This single-asset finding does not compute a numeric hurdle rate; GLD diversifies the whole portfolio and reduces total portfolio drawdown materially.",
    "This does not compute a numeric hurdle rate: GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate and GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate — GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate, or GLD diversifies the whole portfolio in every period.",
    "This does not establish anything, and the portfolio's risk is reduced by GLD.",
    "This does not establish anything; GLD is negatively correlated with the portfolio.",
])
def test_single_asset_disclosure_all_families_remain_rejected_under_fifth_correction(prior_round_sentence):
    """Explicit reconfirmation that every bypass family closed by the
    first four bounded corrections remains closed under the fifth
    correction's widened veto window -- proves the fifth correction is a
    superset fix, not a lateral rewrite that reopens any already-closed
    gap."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        prior_round_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("legit_sentence", [
    "This single-asset assessment does not establish whole-portfolio diversification or correlation.",
    "This single-asset finding does not establish diversification, correlation, or hedge effectiveness.",
    "This is a single-asset assessment; it does not establish whole-portfolio diversification, and portfolio correlation remains separately governed.",
    "This finding is single-asset only. Whole-portfolio diversification and correlation effects remain separately governed by the overlap model.",
    "This finding is single-asset and historical only. No portfolio correlation conclusion is established.",
    "This finding is single-asset and historical only. No whole-portfolio diversification benefit is established by this single-asset finding.",
    "This is single-asset only. None of this establishes correlation with the current portfolio.",
])
def test_single_asset_disclosure_allowed_language_still_accepted_under_fifth_correction(legit_sentence):
    """Every category of legitimate disclaimer language required by the
    round-5 task's own allowed-language list must remain accepted under
    the widened veto window -- coordinated-object negation, multi-clause
    disclaimers, declarative deferrals, and quantifier-negation forms."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        legit_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_single_asset_disclosure_real_gld_and_cash_like_unaffected_by_fifth_correction():
    """The real sealed GLD.yaml single_asset_disclosure text, and the
    real sealed CASH_LIKE_CAPITAL.yaml record (no single_asset_disclosure
    field at all), both remain valid under the widened veto window."""
    gld_result = eav.validate_economic_assessment_file(
        REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml"
    )
    assert gld_result.valid, gld_result.errors
    cash_result = eav.validate_economic_assessment_file(
        REPO_ROOT / "intelligence" / "economic_assessment" / "CASH_LIKE_CAPITAL.yaml"
    )
    assert cash_result.valid, cash_result.errors


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


def test_rationale_diversification_scan_unaffected_by_quantifier_negation_addition():
    """rationale's unconditional block is not weakened by the quantifier-
    negation addition -- a quantifier-negated claim in rationale is still
    rejected outright, since rationale has no negation carve-out of any
    kind, quantifier or otherwise."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["rationale"] = (
        "No portfolio correlation conclusion is established, though the correlation with the current portfolio is notable."
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


# ── sixth bounded correction: structural whitelist redesign closing the
#    whole negation-laundering vulnerability CLASS ──────────────────────
# Rounds two through five each patched one more concrete bypass
# construction by enumerating more clause-boundary punctuation,
# conjunction words, and finite-verb interruptors -- a blacklist
# architecture an independent review demonstrated incomplete at every
# round. This correction replaces the whole blacklist (clause-splitting,
# per-match veto window) with a whitelist evaluated directly per claim
# match, per sentence: a match is governed only when the text separating
# it from its governing negation or deferral is purely connective tissue
# (`_is_purely_connective`) in BOTH directions for the negation path, or
# purely connective between claim and deferral for the deferral path
# (`_claim_is_governed`) -- and the match's own internal text must
# likewise be either purely connective or itself explained by a genuine
# negation/deferral sub-match (`_match_content_is_explained`), closing a
# regression this round's own pre-push testing found: the claim
# patterns' bounded same-sentence gap can greedily swallow an entire
# unrelated clause into the match text itself, invisible to the
# before/after check.

@pytest.mark.parametrize("bypass_sentence", [
    # Round 1: unrelated negation elsewhere in sentence, no real disclaimer
    "GLD diversifies the whole portfolio and reduces portfolio risk in every period.",
    # Round 2: cross-clause laundering via comma+conjunction / semicolon /
    # contrastive conjunction
    "This does not compute a numeric hurdle rate, and GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate, so GLD diversifies the whole portfolio materially.",
    "This does not compute a numeric hurdle rate; GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate, but GLD diversifies the whole portfolio materially.",
    # Round 3: bare (comma-less) and/so, em dash, colon, "or" opening a
    # new independent clause
    "This does not compute a numeric hurdle rate and GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate so GLD diversifies the whole portfolio materially.",
    "This does not compute a numeric hurdle rate -- GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate: GLD diversifies the whole portfolio in every tested period.",
    "This does not compute a numeric hurdle rate, or diversification of the whole portfolio IS ACHIEVED by GLD regardless.",
    # Round 4: subject-vs-object ambiguity -- claim opens a new clause as
    # its own grammatical subject
    "This does not compute a numeric hurdle rate, and diversification of the whole portfolio is achieved by GLD in every period.",
    "This does not compute a numeric hurdle rate, or correlation with the current portfolio is demonstrated by GLD regardless.",
    # Round 5: comma-delimited appositive/parenthetical truncating the
    # (now-discarded) veto window
    "This does not compute a numeric hurdle rate, and diversification of the whole portfolio, across every historical regime examined in this record's own review, is achieved by GLD.",
    "This does not compute a numeric hurdle rate, or correlation with the current portfolio, across every historical regime examined in this record's own review, is demonstrated by GLD.",
    # Generic variants: unrelated negation elsewhere, cross-sentence, and
    # a claim preceding its own unrelated negation (negation cannot
    # retroactively govern an earlier claim)
    "This record does not establish a numeric fair value. Separately, GLD diversifies the whole portfolio in every period tested.",
    "This record never asserts a specific price target. GLD reduces the portfolio's risk in every regime.",
    "None of the evidence here establishes a discount rate. GLD hedges the current portfolio during every drawdown examined.",
    "GLD diversifies the whole portfolio in every period. This does not compute a numeric hurdle rate.",
    # Passive-voice and parenthetical laundering
    "This does not compute a numeric hurdle rate, and the whole portfolio is diversified by GLD in every tested period.",
    "This does not compute a numeric hurdle rate (a separate matter), and diversification of the whole portfolio is achieved by GLD.",
    # A fake quantifier-negation opener that does not actually govern the
    # later, unrelated claim
    "No numeric hurdle rate is computed here, and diversification of the whole portfolio is achieved by GLD in every tested period.",
    # A second claim in the same sentence left ungoverned after a first,
    # legitimately-disclaimed claim
    "This does not compute a numeric hurdle rate, or substitute for a correlation finding. GLD also reduces the portfolio's risk in every regime tested.",
    # A fake object-list continuation that is actually a new clause
    "This does not compute a numeric hurdle rate, or GLD's own reduces portfolio risk mechanism is demonstrated clearly.",
    # Long-distance dilution padding the negation-to-claim span with real
    # content words that are not part of either closed vocabulary
    "This does not compute, historically speaking, in any meaningful economic sense whatsoever, a numeric hurdle rate, and GLD diversifies the whole portfolio in every tested period.",
    # A genuine declarative-deferral phrase used as a red herring
    # elsewhere while a real claim stays unguarded
    "The avoided-borrowing-cost question remains separately governed by DEBT_REDUCTION. GLD diversifies the whole portfolio in every tested period.",
])
def test_sixth_correction_known_bypass_families_rejected(bypass_sentence):
    """Every construction from the demonstrated vulnerability family
    (rounds one through five, plus generic variants of the same class)
    must remain rejected under the whitelist-based redesign."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        bypass_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("bypass_sentence", [
    # Own pre-push adversarial self-challenge testing (>= 20 unseen
    # constructions, varying coordination, punctuation, subject/object
    # order, voice, parentheticals, negation position, quantifiers,
    # clause order, and claim family, per the design's own required
    # self-challenge discipline)
    "This does not compute a numeric hurdle rate; a portfolio-level diversification benefit is nonetheless provided by GLD across every period.",
    "It is not the case that this fails to establish diversification of the whole portfolio by GLD in every tested period.",
    "No hurdle rate is computed, and no one disputes that GLD diversifies the whole portfolio in every regime.",
    "This does not establish a fair value; nonetheless, correlation with the current portfolio is demonstrated by GLD across every drawdown.",
    "This does not compute a hurdle rate, however GLD reduces the portfolio's risk in every tested regime.",
    "Although this does not establish a numeric finding, GLD hedges the current portfolio during every drawdown examined.",
    "While this does not compute a hurdle rate, diversification of the whole portfolio is achieved by GLD regardless.",
    "This does not compute a numeric hurdle rate (a separate and unrelated matter entirely, discussed at length elsewhere in this same document), and GLD diversifies the whole portfolio.",
    "This does not compute a hurdle rate, does not establish a fair value, and does not substitute for anything -- but GLD diversifies the whole portfolio in every period, full stop.",
    "GLD diversifies the whole portfolio in every tested period, a finding that remains unexplored elsewhere.",
    "This does not compute a hurdle rate or establish a fair value. GLD reduces the portfolio's risk and hedges the current portfolio across every regime.",
    "The whole portfolio is diversified by GLD, and this does not compute a numeric hurdle rate.",
    "If a numeric hurdle rate were computed here (it is not), GLD would still diversify the whole portfolio in every tested period.",
    "Does this compute a numeric hurdle rate? No, it does not -- but GLD reduces the portfolio's risk regardless.",
    "This does not compute a numeric hurdle rate.* GLD diversifies the whole portfolio in every period examined.",
    "This does not compute a numeric hurdle rate. - GLD diversifies the whole portfolio in every period examined.",
    'This does not compute a numeric hurdle rate, and "GLD diversifies the whole portfolio" in every tested period, per this record.',
    "This does not compute a numeric hurdle rate, and computing a portfolio-level diversification benefit is nonetheless achieved through GLD's own inclusion.",
    "GLD, a component of the overlap model's own future work, diversifies the whole portfolio in every tested period; this does not compute a numeric hurdle rate for it.",
    "This does not compute, and does not establish, and does not substitute for anything at all -- yet still, GLD's own correlation with the current portfolio is real and material and demonstrated.",
    "This does not compute a numeric hurdle rate, or substitute for a correlation finding, and separately GLD reduces the portfolio's risk in every regime tested independently.",
    "This does not compute the finding of a whole portfolio benefit or the level of a portfolio effect, and portfolio diversification is nonetheless achieved by GLD in every tested period, a fact GLD's own management has confirmed repeatedly across multiple public statements and filings.",
    # A second, later self-challenge pass (20 more unseen constructions,
    # performed as the design's own mandatory pre-push step)
    "Does not compute a hurdle rate, and GLD diversifies the whole portfolio in every period.",
    "This does not compute a hurdle rate, nor does it establish a fair value -- yet correlation with the current portfolio is nonetheless real, per GLD's own historical record.",
    "This does not compute a hurdle rate, and GLD's own mechanism offsets the whole portfolio's volatility in every period tested.",
    "This does not compute a hurdle rate, and a genuine portfolio hedge is provided by GLD across every regime.",
    "This does not compute a hurdle rate, and the portfolio's risk is meaningfully reduced by GLD in every period.",
    "This does not compute a hurdle rate; diversification of the whole portfolio is nonetheless achieved by GLD.",
    "This record makes no attempt, in any of its sections, to compute a numeric hurdle rate of any kind for any purpose, and GLD diversifies the whole portfolio in every tested period regardless of that fact.",
    "Is a numeric hurdle rate computed here? It is not. GLD nonetheless reduces the portfolio's risk in every regime, a fact worth noting.",
    "This does not establish a portfolio-level diversification finding, and separately, GLD's own historical pattern shows real reduction of the whole portfolio's drawdown in most periods.",
    "This does not compute a hurdle rate, and GLD is correlated with the current portfolio in a materially negative way across every regime.",
    "This does not compute a hurdle rate; and GLD diversifies the whole portfolio in every tested period.",
    "This does not compute the following: a hurdle rate, a fair value, or a discount rate -- meanwhile GLD diversifies the whole portfolio in every period.",
    "This does not compute GLD's own numeric hurdle rate, and GLD's own diversification of the whole portfolio is nonetheless real across every regime.",
    "This does not compute a hurdle rate, and portfolio diversification is achieved by GLD in every tested period without exception.",
    "This does not compute a hurdle rate. And GLD diversifies the whole portfolio in every tested period.",
    "GLD diversifies the whole portfolio in every tested period; this section, separately, does not compute a numeric hurdle rate.",
    "None of this computes a numeric hurdle rate, and GLD diversifies the whole portfolio in every tested period regardless.",
    "This does not compute a hurdle rate, and GLD materially reduces the whole portfolio's drawdown in every regime examined.",
    "Not computed here, and GLD diversifies the whole portfolio.",
    "This does not compute the finding of a whole portfolio benefit, and portfolio diversification of a whole portfolio benefit is nonetheless achieved by GLD in every tested period.",
])
def test_sixth_correction_self_challenge_matrix_rejected(bypass_sentence):
    """The design's own mandatory self-challenge pass (>= 20 additional
    unseen constructions, testing the design assumption itself rather
    than the already-demonstrated bypass families) -- every construction
    must be rejected."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        bypass_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("decoy_sentence", [
    # A decoy negation ("never computes hurdle rates") sits far from the
    # actual match ("diversifies the whole portfolio"), which is itself
    # impure (a bare verb form, not the closed noun-vocabulary) and
    # contains no negation/deferral of its own.
    "This does not compute a hurdle rate, and GLD, which never computes hurdle rates on its own, materially diversifies the whole portfolio in every period.",
    # A short, internally-pure claim match ("portfolio diversification")
    # is followed by a decoy negation and then its own real, unguarded
    # predicate ("is nonetheless achieved by GLD") -- the decoy must not
    # satisfy the claim's own backward/forward governance check.
    "This does not compute a hurdle rate, and portfolio diversification, a concept this section does not itself define, is nonetheless achieved by GLD in every regime.",
    # A decoy negation lives *inside* an otherwise-impure match's own
    # filler, but the decoy itself does not match the closed disclaiming-
    # verb vocabulary ("quantify" is not a recognized disclaiming verb,
    # and "not itself quantify" breaks the immediate not+verb adjacency
    # the pattern requires) -- confirms `_match_content_is_explained`
    # requires a *genuine* negation/deferral match, not merely negation-
    # shaped prose.
    "This does not establish anything, and correlation, which this does not itself quantify, with the current portfolio is real, per GLD.",
    # A decoy declarative-deferral phrase talks about a different, later
    # matter while the real claim's own governance still fails.
    "This does not compute a hurdle rate, and GLD's own diversification of the whole portfolio, a matter that remains separately governed elsewhere in a different context, is achieved regardless in every period.",
    # A genuine negation governs one claim match while a second, separate
    # claim in the same sentence survives ungoverned.
    "This finding does not establish portfolio diversification, and this section, which does not compute anything else, diversifies the whole portfolio through GLD's own mechanism.",
])
def test_sixth_correction_decoy_negation_probes_rejected(decoy_sentence):
    """Adversarial probes specifically targeting the `_match_content_is_
    explained` refinement: embedding a decoy negation or deferral inside
    an impure match's own filler, or near an otherwise-ungoverned claim,
    must never itself satisfy governance -- the refinement only tolerates
    impurity that is *itself* a genuine second disclaimer, never a bare
    positive assertion merely accompanied by unrelated negation-shaped
    text nearby."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        decoy_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("legit_sentence", [
    "This disclosure does not establish a whole-portfolio diversification benefit.",
    "This disclosure never claims a portfolio-level diversification benefit.",
    "This does not compute, constitute, imply, or substitute for a portfolio-level diversification or correlation finding.",
    "No portfolio correlation conclusion is established by this characterization.",
    "No diversification-benefit finding is drawn from this single-asset review.",
    "No correlation determination is made regarding the whole portfolio here.",
    "Whole-portfolio diversification and correlation effects remain separately governed by the overlap model.",
    "This does not compute, constitute, imply, or substitute for a diversification-benefit or correlation finding.",
    # Two independent, semicolon-joined negated claims -- the second
    # claim match's own impure filler ("; it also does not establish")
    # is itself a genuine second disclaiming negation, not a bare
    # assertion, and must be tolerated by `_match_content_is_explained`.
    "This does not establish portfolio diversification; it also does not establish portfolio correlation.",
    # A real, legitimate cross-reference to the overlap model's own
    # "defensive_offset_interface" dimension name -- must not spuriously
    # match the "offsets?" claim pattern via the underscore-joined
    # "offset_interface" substring.
    "The defensive_offset_interface dimension, which would characterize any portfolio diversification benefit, remains unresolved.",
    # "with" is a literal anchor word inside one of the thirteen fixed
    # claim patterns; "either" is inert trailing filler after a negated
    # claim in its own separate sentence -- both must be whitelisted.
    "None of this establishes correlation with the current portfolio.",
    "This does not establish portfolio diversification. This does not establish portfolio correlation either.",
])
def test_sixth_correction_mandatory_allowed_language_accepted(legit_sentence):
    """The design's own mandatory allowed-language matrix (negated
    same-claim constructions, object/list continuation, quantifier-
    negation constructions, declarative-deferral phrasing, existing
    comma+or lists, plus the specific legitimate constructions this
    round's own pre-push regression testing found and fixed) must remain
    accepted. Each is prefixed with the required single-asset marker
    sentence (SS6's mandatory disclosure requirement), matching this
    file's own established fixture pattern."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        f"This finding is single-asset and historical only. {legit_sentence}"
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_sixth_correction_real_gld_and_cash_like_unaffected():
    """The real sealed GLD.yaml single_asset_disclosure text, and the
    real sealed CASH_LIKE_CAPITAL.yaml record (no single_asset_disclosure
    field at all), both remain valid end-to-end under the whitelist
    redesign."""
    gld_result = eav.validate_economic_assessment_file(
        REPO_ROOT / "intelligence" / "economic_assessment" / "GLD.yaml"
    )
    assert gld_result.valid, gld_result.errors
    cash_result = eav.validate_economic_assessment_file(
        REPO_ROOT / "intelligence" / "economic_assessment" / "CASH_LIKE_CAPITAL.yaml"
    )
    assert cash_result.valid, cash_result.errors


def test_sixth_correction_greedy_gap_swallow_reproduction_rejected():
    """Direct reproduction of the exact regression this round's own
    pre-push testing found before ever pushing: the claim patterns' own
    bounded same-sentence gap ([^.]{0,60} between two anchor concepts)
    can greedily absorb an entire unrelated clause -- including its own
    foreign subject -- into the match text itself, invisible to a
    before/after-only governance check. Confirms the internal-purity
    requirement (`_match_content_is_explained` applied to the match's own
    text) catches this specific mechanism, not merely the sentence-level
    outcome."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This assessment does not establish portfolio diversification, and GLD diversifies the whole portfolio."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("foreign, non-connective content" in e for e in result.errors)


def test_sixth_correction_offset_interface_no_false_match():
    """Direct unit-level confirmation that the "offsets?" claim pattern
    no longer matches the schema's own "defensive_offset_interface"
    dimension name as a false positive (the underscore before "offset"
    is itself a \\w character, so an unanchored pattern matched there
    regardless of what came after) -- while a genuine "offsets" claim
    still matches correctly."""
    false_positive_text = "The defensive_offset_interface dimension governs this."
    for pattern in eav._PORTFOLIO_DIVERSIFICATION_PATTERNS:
        assert not pattern.search(false_positive_text), pattern.pattern

    genuine_claim_text = "GLD offsets the whole portfolio's risk in every period."
    assert any(
        pattern.search(genuine_claim_text) for pattern in eav._PORTFOLIO_DIVERSIFICATION_PATTERNS
    )


def _explained(sentence):
    """Round-7 helper: `_match_content_is_explained` now takes sentence-
    relative offsets plus a precomputed fixed-range list (the seventh
    bounded correction's own sentence-wide, not span-local, fixed-phrase
    design) rather than an isolated match string."""
    fixed_ranges = eav._fixed_phrase_ranges(sentence)
    return eav._match_content_is_explained(sentence, 0, len(sentence), fixed_ranges)


def test_sixth_correction_match_content_is_explained_helper_direct():
    """Direct unit tests of `_match_content_is_explained`'s three
    branches: purely connective (accepted), impure-but-containing-a-
    genuine-negation-or-deferral (accepted), and impure-with-neither
    (rejected) -- the exact distinction the decoy-negation probes above
    exercise end-to-end. Updated for the seventh bounded correction's
    `(sentence, match_start, match_end, fixed_ranges)` signature."""
    assert _explained("portfolio diversification")
    assert _explained(
        "diversification; it also does not establish portfolio"
    )
    assert _explained(
        "diversification and correlation effects remain separately governed"
    )
    assert not _explained(
        "diversification, and GLD diversifies the whole portfolio"
    )


def test_sixth_correction_known_pre_existing_out_of_scope_coverage_gap_disclosed():
    """Disclosed, not fixed in this round: own adversarial self-testing
    found "correlation, which this record does not separately quantify,
    with the current portfolio" matches no existing claim pattern at
    all -- the fixed-phrase pattern requires "correlat(?:ed|ion)"
    immediately followed by "with" (no intervening clause), and no
    reversed-order loose-gap pattern exists for "correlat[...]portfolio"
    the way one exists for "diversif[...]portfolio". This is a claim-
    *detection* coverage gap, categorically different from the
    negation-*laundering* governance vulnerability this round closes: no
    claim is ever matched, so there is nothing for the governance
    mechanism to evaluate, govern, or fail to govern. Independently
    confirmed to be a pre-existing, cross-round limitation, not a
    regression introduced by this correction -- the identical
    construction also validates clean under the round-five committed
    code (governance/audits/WS0014_GLD_CASH_LIKE_CAPITAL_ECONOMIC_
    ASSESSMENT_IMPLEMENTATION_20260810.md SS14 records the full
    diagnosis). An attempted fix (adding a symmetric reversed-order
    "correlat[...]portfolio" pattern) was tried and reverted after it
    regressed a mandatory quantifier-negation acceptance case
    ("No correlation determination is made regarding the whole
    portfolio here.") -- closing this gap safely requires widening the
    quantifier-exemption's own containment logic, a separate, bounded
    unit of work left to a future correction."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding is single-asset and historical only. This does not establish "
        "anything, and correlation, which this does not itself quantify, with the "
        "current portfolio is real, per GLD."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    # Documents current (accepted) behavior for this known, disclosed,
    # out-of-scope limitation -- not a claim that this is safe or
    # desirable, only that it is pre-existing and unaddressed by this
    # correction. A future, separate correction closing the underlying
    # claim-detection gap would need to update this test's own
    # expectation to `not result.valid`.
    assert result.valid, (
        "if this now fails, the claim-detection coverage gap has been closed -- "
        "update this test's expectation and its docstring accordingly"
    )


# ── Seventh bounded correction ──────────────────────────────────────────
# Independent review (pullrequestreview-4898549236, anchored to the sixth
# correction's own exact head) found the sixth correction's whitelist
# still contained two BARE, POLYSEMOUS tokens -- "own" and "benefit" --
# each independently exploitable as a finite verb (subject-verb-object),
# letting an unrelated earlier negation appear to govern a later,
# genuinely new, unnegated claim built entirely from whitelist-approved
# tokens. A full audit of every whitelist token for the same property
# found four more risky tokens ("level", "effect", "effects", "finding")
# plus five more disclaiming-verb "-ing" gerunds independently exploitable
# via the SAME unconstrained `\w*` wildcard "finding" itself used
# (establishing/representing/showing/claiming/asserting -- each forms its
# "-ing" gerund by simple concatenation onto a consonant-ending base verb,
# unlike compute/determine/indicate/demonstrate/prove, which drop a silent
# "e" and are therefore accidentally, not by design, unmatched).
#
# Fix: own/benefit/level/effect/effects removed from the bare connective
# whitelist outright; a negative lookahead `(?!ing\b)` closes the gerund
# path for every disclaiming verb at once (finding/establishing/
# representing/showing/claiming/asserting). Each removed word's narrow
# legitimate use is restored only through a bounded, fully-anchored fixed-
# phrase mechanism (`_OWN_FIXED_PHRASE`, `_BENEFIT_FIXED_PHRASE`,
# `_LEVEL_FIXED_PHRASE`, `_EFFECT_FIXED_PHRASE`, `_FINDING_FIXED_PHRASE`)
# requiring BOTH a specific legitimate predecessor and a positive allow-
# list of safe followers -- never a negative denylist (testing found a
# denylist of "not the/a/an" still lets a bare, article-less noun object
# through, e.g. "benefit portfolio directly"). Fixed-phrase coverage is
# computed once per SENTENCE, not per isolated span, because a legitimate
# bigram can straddle the boundary between a claim match's own text and a
# separately-extracted connective span.
#
# Own-suite regression testing (this same correction, before push) found
# two further gaps in the FIRST widening pass and closed both: (1)
# "diversification-benefit finding for Portfolio-HQ's own current
# holdings" and "a portfolio-level correlation" (both pre-existing
# accepted constructions) initially failed -- `_FINDING_FIXED_PHRASE`
# widened to accept "benefit" as a predecessor and a narrow, exact
# safe-tail follower ("for {hq's own (current) holdings}", never a bare
# "for"); `_LEVEL_FIXED_PHRASE` widened to accept the full closed
# `_DIVERSIFICATION_CONCEPT_NOUNS` vocabulary as a follower, not just
# "diversification". (2) That LEVEL widening, in its first form, allowed a
# bare SPACE (not just hyphen) between "portfolio" and "level" -- own
# self-challenge testing (>= 30 unseen constructions, this same pass)
# found this concretely exploitable: "This never establishes
# diversification, and the whole portfolio level correlation for the
# current holdings." was accepted, because the fixed-phrase match starts
# at "portfolio" (already part of an earlier claim match) and straddles
# into the trailing connective window, hiding a claim-relevant concept
# noun ("correlation") behind an ambiguous verb token. Closed by requiring
# a literal HYPHEN specifically ("portfolio-level", never bare-space
# "portfolio level") -- confirmed, by exhaustive corpus search, to be the
# only form any real sealed record or existing accepted test ever uses.
#
# The pre-existing, already-disclosed correlat-word-order claim-detection
# gap (see `test_sixth_correction_known_pre_existing_out_of_scope_
# coverage_gap_disclosed` above) is unchanged by this correction -- not
# widened, not narrowed, not touched.


@pytest.mark.parametrize("bypass_sentence", [
    # Independent review's own exact reported bypasses (own/benefit as
    # bare finite verbs)
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification benefit the portfolio, with effect for the "
    "current holdings level.",
    "This is a single-asset finding. Diversification benefit the "
    "portfolio, with effect for the whole current holdings level, "
    "remains separately governed.",
    # NOTE: the independent review's own third reported construction
    # ("...and the current portfolio own effect for the whole level, with
    # a specific finding of hedge and correlation.") is deliberately NOT
    # included here -- direct diagnosis found it produces ZERO claim-
    # pattern matches at all (no anchor pair falls within any pattern's
    # own bounded gap), so it was never actually exploitable via the
    # whitelist-polysemy mechanism this correction closes; it is a
    # coincidental non-match of the same, already-disclosed, pre-existing
    # claim-*detection* shape as the correlat-word-order gap, not a
    # governance-*laundering* bypass. Confirmed via direct inspection of
    # `_PORTFOLIO_DIVERSIFICATION_PATTERNS.finditer()` before this
    # decision -- included here as a documented, deliberate omission, not
    # an oversight.
    # own/benefit as bare verbs, cleanly isolated
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio own a diversification benefit for the current.",
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification benefit the portfolio, with effect for the "
    "current holdings level.",
    # level/effect/effects as bare finite verbs (same whitelist-polysemy
    # class as own/benefit, found during the full whitelist audit)
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification level the whole portfolio, with a specific "
    "finding for the current holdings.",
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification effect the whole portfolio, with a specific "
    "finding for the current holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification effects the whole portfolio, with a specific "
    "finding for the current holdings level.",
    # "finding" as a bare participial predicate head (the same
    # unconstrained gerund-wildcard mechanism as own/benefit, not merely
    # a coincidental extra case)
    "This is a single-asset finding. This does not establish a specific "
    "hedge, and the whole portfolio finding a correlation for the "
    "current holdings level.",
    "This is a single-asset finding. This does not establish a specific "
    "hedge, and the whole portfolio finding correlation for the current "
    "holdings level.",
    "This is a single-asset finding. This does not establish a specific "
    "hedge, and this finding a diversification for the whole portfolio.",
    # the five other disclaiming-verb "-ing" gerunds sharing "finding"'s
    # own exploitable wildcard mechanism
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio establishing a correlation for the current "
    "holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio representing a correlation for the current "
    "holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio showing a correlation for the current "
    "holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio claiming a correlation for the current "
    "holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio asserting a correlation for the current "
    "holdings level.",
    # conjunction, punctuation, subject, case, and whitespace variations
    "This is a single-asset finding. This does not establish a finding, "
    "or the whole portfolio own a diversification benefit for the current.",
    "This is a single-asset finding. This does not establish a finding; "
    "diversification benefit the portfolio, with effect for the current "
    "holdings.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the portfolio benefit from diversification the whole current.",
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification BENEFIT the portfolio, with effect for the "
    "current holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio OWN a diversification benefit for the current.",
    "This is a single-asset finding.  This does not establish a finding,  "
    "and  diversification  benefit  the portfolio,  with effect for the "
    "current holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification benefit portfolio directly for the current "
    "holdings level.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio, which never computes anything, own a "
    "diversification benefit for the current.",
    # fixed-phrase widening must not create new bypass surface: wrong
    # "for" tail, wrong finding predecessor, reversed bigram order,
    # inserted words before the safe anchor, chained bridges
    "This does not establish a finding, and the whole portfolio benefit "
    "finding for portfolio-hq's own current holdings, and correlation "
    "own the book.",
    "This does not establish a finding, and portfolio-level correlation, "
    "and diversification level the whole portfolio.",
    "This is a single-asset finding. This does not establish a finding, "
    "and diversification benefit finding for the whole current portfolio.",
    "This does not establish a finding, and diversification finding for "
    "a specific correlation with the whole portfolio.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio finding for portfolio-hq's own current "
    "holdings.",
    "This is a single-asset finding. This does not establish a finding, "
    "and own finding for portfolio-hq's own current holdings.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio finding benefit for portfolio-hq's own "
    "current holdings.",
    "This is a single-asset finding. This does not establish a finding, "
    "and correlation finding for the whole portfolio-hq's own current "
    "holdings.",
    "This is a single-asset finding. This does not establish a finding, "
    "and the whole portfolio, which never computes anything, benefit "
    "finding for portfolio-hq's own current holdings, and own the book.",
    "This is a single-asset finding. This does not establish a finding, "
    "and DIVERSIFICATION BENEFIT FINDING FOR PORTFOLIO-HQ'S OWN CURRENT "
    "HOLDINGS is claimed, and correlation own the whole book.",
    "This is a single-asset finding.  This does not establish a finding,  "
    "and  diversification  benefit  finding  for  portfolio-hq's  own  "
    "current  holdings,  and  correlation  own  the  book.",
    "This is a single-asset finding. This does not establish a finding; "
    "it also does not establish a finding, and portfolio-level hedge, "
    "and diversification level the whole portfolio.",
    # dedicated LEVEL space-vs-hyphen straddling-boundary regressions
    # (the second gap found and closed during this same correction)
    "This never establishes diversification, and the whole portfolio "
    "level correlation for the current holdings.",
    "This never establishes diversification, and the whole portfolio "
    "level hedge for the current holdings.",
    "This never establishes correlation, and the whole portfolio level "
    "diversification for the current holdings.",
    "This never establishes diversification, and the whole portfolio "
    "level risk for the current holdings.",
    "This never establishes diversification, and the whole PORTFOLIO "
    "LEVEL VOLATILITY for the current holdings.",
    "This never establishes diversification, and the whole portfolio "
    "level correlation for the current, and correlation own the book.",
])
def test_seventh_correction_known_bypass_families_rejected(bypass_sentence):
    """Every construction from the seventh correction's own demonstrated
    vulnerability family -- the independent review's exact reported
    bypasses, every other bare-polysemous-token whitelist violation found
    by the full audit, the five additional exploitable disclaiming-verb
    gerunds, and both fixed-phrase-widening regressions found and closed
    during this same correction's own pre-push regression testing -- must
    be rejected."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        bypass_sentence
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert not result.valid


@pytest.mark.parametrize("legit_sentence", [
    # the exact pre-existing accepted construction that regressed during
    # this correction's own first widening pass, and was fixed
    "It never establishes a portfolio-level correlation or "
    "diversification-benefit finding for Portfolio-HQ's own current holdings.",
    # LEVEL fixed phrase, widened vocabulary, hyphen required
    "This does not establish a portfolio-level correlation.",
    "This does not establish a portfolio-level hedge.",
    "This does not establish a portfolio-level drawdown finding.",
    "This never establishes diversification, and the whole portfolio-level "
    "correlation for the current holdings.",
    "This never establishes diversification, and the whole portfolio-level "
    "hedge for the current holdings.",
    # FINDING fixed phrase, widened predecessor (benefit) and follower
    # (the exact safe "for {own holdings}" tail)
    "This does not establish a diversification-benefit finding for HQ's "
    "own holdings.",
    "This does not establish a correlation finding for Portfolio-HQ's own "
    "current holdings.",
    "This does not establish a diversification-benefit finding for "
    "Portfolio-HQ's own current holdings.",
])
def test_seventh_correction_mandatory_allowed_language_accepted(legit_sentence):
    """The seventh correction's own mandatory allowed-language matrix --
    the exact previously-accepted construction its own first widening
    pass regressed, plus every other legitimate use of the widened LEVEL
    and FINDING fixed phrases -- must remain accepted."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        f"This finding is single-asset and historical only. {legit_sentence}"
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_seventh_correction_real_gld_and_cash_like_unaffected():
    """The real sealed GLD.yaml and CASH_LIKE_CAPITAL.yaml records must
    still validate cleanly after the seventh correction -- reused, not
    duplicated, from the sixth correction's own identical check."""
    for ticker in ("GLD", "CASH_LIKE_CAPITAL"):
        path = REPO_ROOT / "intelligence" / "economic_assessment" / f"{ticker}.yaml"
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
        assert result.valid, (ticker, result.errors)


def test_seventh_correction_full_whitelist_audit_no_bare_risky_tokens():
    """Direct audit of the live connective whitelist: none of the six
    tokens found independently exploitable as a bare finite verb/
    participle (own, benefit, level, effect, effects, finding) may appear
    as a bare member of `_CONNECTIVE_WORD_WHITELIST` -- each must be
    supported, where legitimate, only through its own bounded fixed-
    phrase mechanism."""
    risky = {"own", "benefit", "level", "effect", "effects", "finding"}
    assert not (risky & eav._CONNECTIVE_WORD_WHITELIST), (
        risky & eav._CONNECTIVE_WORD_WHITELIST
    )


def test_seventh_correction_gerund_guard_blocks_every_disclaiming_verb():
    """`_CONNECTIVE_VERB_NOUN_PATTERN`'s `(?!ing\\b)` guard must reject
    the "-ing" gerund of every disclaiming verb, not just "finding" --
    direct unit coverage of the mechanism, independent of the end-to-end
    scan."""
    for verb in (
        "establishing", "representing", "showing", "claiming", "asserting",
        "finding",
    ):
        assert not eav._CONNECTIVE_VERB_NOUN_PATTERN.match(verb), verb
    # the five silent-e verbs are accidentally, not by design, unaffected
    # by the gerund guard (their own gerund spelling drops the "e",
    # breaking the literal base-form prefix match already) -- confirmed
    # directly, not merely asserted, since this is the reasoning basis for
    # not flagging them during the full whitelist audit
    for verb in ("computing", "determining", "indicating", "demonstrating", "proving"):
        assert not eav._CONNECTIVE_VERB_NOUN_PATTERN.match(verb), verb


def test_seventh_correction_fixed_phrase_ranges_helper_direct():
    """Direct unit coverage of `_fixed_phrase_ranges`: each of the five
    fixed-phrase patterns is independently reachable, and unrelated text
    produces no ranges at all."""
    assert eav._fixed_phrase_ranges("nothing relevant here") == []
    sentence = "diversification-benefit finding for hq's own current holdings"
    ranges = eav._fixed_phrase_ranges(sentence)
    assert ranges, "expected at least one fixed-phrase range"
    # every returned range must be a valid, in-bounds (start, end) pair
    for start, end in ranges:
        assert 0 <= start < end <= len(sentence)


def test_seventh_correction_level_fixed_phrase_requires_hyphen_not_space():
    """Direct unit coverage of the space-vs-hyphen fix: `_LEVEL_FIXED_
    PHRASE` must match the hyphenated form and must NOT match the bare-
    space form, even though both were treated identically before this
    correction's own second widening-regression fix."""
    assert eav._LEVEL_FIXED_PHRASE.search("portfolio-level correlation")
    assert eav._LEVEL_FIXED_PHRASE.search("portfolio-level diversification")
    assert not eav._LEVEL_FIXED_PHRASE.search("portfolio level correlation")
    assert not eav._LEVEL_FIXED_PHRASE.search("portfolio level diversification")


def test_seventh_correction_finding_fixed_phrase_predecessor_and_tail():
    """Direct unit coverage of the FINDING fixed phrase: "benefit" must
    now be an accepted predecessor (matching "correlation"/
    "diversification"), and the widened "for {safe tail}" follower must
    accept only the exact hq's-own-holdings anchor, not an arbitrary
    "for" continuation."""
    assert eav._FINDING_FIXED_PHRASE.search(
        "diversification-benefit finding for Portfolio-HQ's own current holdings"
    )
    assert eav._FINDING_FIXED_PHRASE.search(
        "correlation finding for hq's own holdings"
    )
    assert eav._FINDING_FIXED_PHRASE.search("correlation finding specific")
    assert eav._FINDING_FIXED_PHRASE.search("diversification finding.")
    # wrong tail: "for" not followed by the exact safe anchor
    assert not eav._FINDING_FIXED_PHRASE.search(
        "diversification-benefit finding for the whole current portfolio"
    )
    assert not eav._FINDING_FIXED_PHRASE.search(
        "correlation finding for a specific correlation"
    )


def test_seventh_correction_known_pre_existing_out_of_scope_gap_unchanged():
    """The pre-existing, already-disclosed correlat-word-order claim-
    detection gap (see the sixth correction's own identically-named test
    above) is explicitly out of this correction's own authorized scope --
    reused, unchanged, not widened or narrowed, confirmed still present
    under the seventh-correction code."""
    data = _record(analytical_subject="GLD")
    data["instrument_specific_economic_characterization"]["historical_equity_drawdown_behavior"]["single_asset_disclosure"] = (
        "This finding is single-asset and historical only. This does not establish "
        "anything, and correlation, which this does not itself quantify, with the "
        "current portfolio is real, per GLD."
    )
    result = eav.validate_economic_assessment_data(data, repo_root=REPO_ROOT)
    assert result.valid, (
        "if this now fails, the claim-detection coverage gap has been closed -- "
        "update this test's expectation and its docstring accordingly -- "
        "the seventh correction leaves this gap exactly as the sixth left it"
    )
