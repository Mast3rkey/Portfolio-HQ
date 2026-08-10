"""Tests for functional_doctrine_validator.py (WS-0014 functional-doctrine
blind-classification schema, XASSET-0005/XASSET-0006 scope).

Every schema/behavior test below constructs its own synthetic fixture -- no
real capital-use type's judgment content is asserted against in this file,
the same authorized-scope discipline test_classification_validator.py/
test_etf_classification_validator.py/test_crypto_classification_validator.py
already follow. The directory-scan tests exercise the real repository's
intelligence/functional_doctrine/ directory, authored under this one
implementation PR.

Overlap-model schema (XASSET-0005 supporting artifact SS6) tests are
explicitly out of scope for this file -- that schema is not implemented by
this PR and no `intelligence/overlap_model/` file exists.
"""

from __future__ import annotations

import ast
import copy
import subprocess
from pathlib import Path

import pytest
import yaml

import functional_doctrine_validator as fdv

REPO_ROOT = Path(__file__).resolve().parent


# ── fixtures ─────────────────────────────────────────────────────────────

def _functional_role(**overrides) -> dict:
    d = {"role_category": "operational_liquidity_float"}
    d.update(overrides)
    return d


def _hard_constraint_status(**overrides) -> dict:
    d = {"binding": False, "constraint_source": "none_currently_binding"}
    d.update(overrides)
    return d


def _readiness_sub(**overrides) -> dict:
    d = {"status": "assessment_required", "rationale": "Synthetic rationale -- no methodology exists."}
    d.update(overrides)
    return d


def _economic_assessment_readiness(capital_use_type: str = "CASH", **overrides) -> dict:
    if capital_use_type == "DEBT_REDUCTION":
        d = {
            "avoided_borrowing_cost_readiness": _readiness_sub(),
            "survivability_and_buffer_benefit_readiness": _readiness_sub(),
        }
    else:
        d = _readiness_sub()
    d.update(overrides)
    return d


def _liquidity_character(**overrides) -> dict:
    d = {"liquidity_category": "immediately_liquid"}
    d.update(overrides)
    return d


def _capital_preservation_character(**overrides) -> dict:
    d = {"capital_preservation_category": "principal_stable_no_market_risk"}
    d.update(overrides)
    return d


def _freshness_state(**overrides) -> dict:
    d = {"status": "current", "as_of_reference": "Synthetic reference point."}
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
            "as_of_date": "2026-08-09",
            "access_status": "directly_inspected",
        }
    ]


def _structural_reference(*, hash_override: str | None = None) -> dict:
    gld_data = yaml.safe_load((REPO_ROOT / "intelligence" / "etf_classification" / "GLD.yaml").read_text())
    import etf_classification_validator as etf
    live_hash = etf.canonical_record_hash(gld_data)
    return {
        "source_instrument_id": "GLD",
        "source_schema": "etf_classification",
        "source_file": "intelligence/etf_classification/GLD.yaml",
        "referenced_content_sha256": hash_override if hash_override is not None else live_hash,
    }


def _record(*, capital_use_type: str = "CASH", sealed: bool = False, **axis_overrides) -> dict:
    functional_role = axis_overrides.get("functional_role", _functional_role())
    hard_constraint_status = axis_overrides.get("hard_constraint_status", _hard_constraint_status())
    economic_assessment_readiness = axis_overrides.get(
        "economic_assessment_readiness", _economic_assessment_readiness(capital_use_type)
    )
    liquidity_character = axis_overrides.get(
        "liquidity_character",
        _liquidity_character(liquidity_category="not_applicable") if capital_use_type == "DEBT_REDUCTION" else _liquidity_character(),
    )
    capital_preservation_character = axis_overrides.get(
        "capital_preservation_character",
        _capital_preservation_character(capital_preservation_category="reduces_liability_not_an_asset")
        if capital_use_type == "DEBT_REDUCTION" else _capital_preservation_character(),
    )
    freshness_state = axis_overrides.get("freshness_state", _freshness_state())
    evidence_quality = axis_overrides.get("evidence_quality", _evidence_quality())

    structural_risk_flags = axis_overrides.get(
        "structural_risk_flags",
        {
            "binding": hard_constraint_status.get("binding"),
            "capital_preservation_category": capital_preservation_character.get("capital_preservation_category"),
        },
    )
    handoff = axis_overrides.get(
        "cross_asset_handoff",
        {
            "role_summary": functional_role.get("role_category"),
            "evidence_quality_summary": evidence_quality.get("primary_source_coverage"),
            "uncertainty_summary": evidence_quality.get("thesis_uncertainty_statement"),
            "liquidity_risk_summary": liquidity_character.get("liquidity_category"),
            "hard_constraint_signal": {
                "binding": hard_constraint_status.get("binding"),
                "constraint_source": hard_constraint_status.get("constraint_source"),
            },
            "economic_assessment_readiness_summary": economic_assessment_readiness,
        },
    )

    data = {
        "schema_version": "1.0",
        "capital_use_type": capital_use_type,
        "functional_role": functional_role,
        "hard_constraint_status": hard_constraint_status,
        "economic_assessment_readiness": economic_assessment_readiness,
        "liquidity_character": liquidity_character,
        "capital_preservation_character": capital_preservation_character,
        "freshness_state": freshness_state,
        "evidence_quality": evidence_quality,
        "provenance": {"sources": _sources()},
        "evidence_quality_status": evidence_quality.get("primary_source_coverage"),
        "uncertainty_summary": evidence_quality.get("thesis_uncertainty_statement"),
        "structural_risk_flags": structural_risk_flags,
        "record_status": "draft",
        "later_governance_action": "none",
        "abstention_index": axis_overrides.get("abstention_index", []),
        "cross_asset_handoff": handoff,
    }

    if capital_use_type == "GLD_DEFENSIVE_ROLE":
        data["structural_reference"] = axis_overrides.get("structural_reference", _structural_reference())

    if sealed:
        data["record_status"] = "sealed"
        data["sealed_at"] = "2026-08-09T00:00:00Z"
        data["governing_decision"] = "XASSET-0006"
        data["drafting_session_or_shard_id"] = "test-shard"
        data["cohort_manifest_entry"] = f"intelligence/functional_doctrine/COHORT_MANIFEST.yaml#{capital_use_type}"
        data["content_sha256"] = fdv.canonical_record_hash(data)

    return data


def _assert_invalid(data: dict, *, contains: str | None = None) -> fdv.ValidationResult:
    result = fdv.validate_functional_doctrine_data(data)
    assert not result.valid, "expected validation failure but got valid=True"
    if contains is not None:
        assert any(contains in e for e in result.errors), f"{contains!r} not found in {result.errors}"
    return result


# ── happy path, one per capital_use_type ─────────────────────────────────

@pytest.mark.parametrize("capital_use_type", sorted(fdv.AUTHORIZED_POPULATION))
def test_happy_path_per_capital_use_type(capital_use_type):
    data = _record(capital_use_type=capital_use_type, sealed=True)
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


def test_happy_path_draft_no_seal_fields_required():
    data = _record(capital_use_type="CASH", sealed=False)
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


# ── malformed envelope/axis (missing required field) ─────────────────────

@pytest.mark.parametrize("missing_key", [
    "capital_use_type", "schema_version", "functional_role", "hard_constraint_status",
    "economic_assessment_readiness", "liquidity_character", "capital_preservation_character",
    "freshness_state", "evidence_quality", "provenance", "abstention_index",
    "later_governance_action", "structural_risk_flags", "cross_asset_handoff", "record_status",
])
def test_missing_required_top_level_field_rejected(missing_key):
    data = _record(capital_use_type="CASH")
    del data[missing_key]
    _assert_invalid(data)


def test_missing_required_axis_sub_field_rejected():
    data = _record(capital_use_type="CASH")
    del data["functional_role"]["role_category"]
    _assert_invalid(data, contains="functional_role")


# ── extra unknown key at envelope level and axis level ────────────────────

def test_extra_unknown_key_at_envelope_level_rejected():
    data = _record(capital_use_type="CASH")
    data["smuggled_field"] = "anything"
    _assert_invalid(data, contains="smuggled_field")


@pytest.mark.parametrize("axis,bad_key", [
    ("functional_role", "conviction_score"),
    ("hard_constraint_status", "extra_field"),
    ("liquidity_character", "extra_field"),
    ("capital_preservation_character", "extra_field"),
    ("freshness_state", "extra_field"),
    ("evidence_quality", "extra_field"),
])
def test_extra_unknown_key_at_axis_level_rejected(axis, bad_key):
    data = _record(capital_use_type="CASH")
    data[axis][bad_key] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_provenance_source_rejected():
    data = _record(capital_use_type="CASH")
    data["provenance"]["sources"][0]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_structural_reference_rejected():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    data["structural_reference"]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_cross_asset_handoff_rejected():
    data = _record(capital_use_type="CASH")
    data["cross_asset_handoff"]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_structural_risk_flags_rejected():
    data = _record(capital_use_type="CASH")
    data["structural_risk_flags"]["extra"] = "value"
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_abstention_index_entry_rejected():
    data = _record(
        capital_use_type="RESERVE",
        functional_role={"role_category": "unable_to_determine", "abstention_reason": "gap"},
        abstention_index=[{"axis": "functional_role", "field": "role_category", "value": "unable_to_determine", "reason": "gap", "extra": "x"}],
    )
    _assert_invalid(data, contains="unexpected key")


def test_extra_unknown_key_in_manifest_row_rejected():
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0006",
        "cohort": [{
            "capital_use_type": "CASH", "sealed_at": "x", "content_sha256": "x",
            "schema_version": "1.0", "governing_decision": "XASSET-0006",
            "record_path": "intelligence/functional_doctrine/CASH.yaml", "extra": "x",
        }],
    }
    result = fdv.validate_cohort_manifest(manifest, {})
    assert not result.valid
    assert any("unexpected key" in e for e in result.errors)


def test_extra_unknown_key_at_manifest_top_level_rejected():
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": [], "extra": "x"}
    result = fdv.validate_cohort_manifest(manifest, {})
    assert not result.valid
    assert any("unexpected top-level key" in e for e in result.errors)


# ── wrong capital_use_type ────────────────────────────────────────────────

def test_wrong_capital_use_type_rejected():
    data = _record(capital_use_type="CASH")
    data["capital_use_type"] = "SPY"
    _assert_invalid(data, contains="not in the authorized four-type population")


def test_fifth_capital_use_type_value_rejected_even_if_plausible_shaped():
    data = _record(capital_use_type="CASH")
    data["capital_use_type"] = "MARGIN_BUFFER"
    _assert_invalid(data)


# ── economic_assessment_readiness shape enforcement ───────────────────────

def test_single_part_shape_rejected_on_debt_reduction():
    data = _record(capital_use_type="DEBT_REDUCTION")
    data["economic_assessment_readiness"] = _readiness_sub()  # single-part, wrong for DEBT_REDUCTION
    _assert_invalid(data, contains="economic_assessment_readiness")


@pytest.mark.parametrize("capital_use_type", ["CASH", "RESERVE", "GLD_DEFENSIVE_ROLE"])
def test_two_part_shape_rejected_on_non_debt_reduction(capital_use_type):
    data = _record(capital_use_type=capital_use_type)
    data["economic_assessment_readiness"] = {
        "avoided_borrowing_cost_readiness": _readiness_sub(),
        "survivability_and_buffer_benefit_readiness": _readiness_sub(),
    }
    _assert_invalid(data, contains="single-part")


def test_debt_reduction_missing_one_readiness_sub_field_rejected():
    data = _record(capital_use_type="DEBT_REDUCTION")
    del data["economic_assessment_readiness"]["survivability_and_buffer_benefit_readiness"]
    _assert_invalid(data, contains="missing required key")


# ── forced assessment_required value ──────────────────────────────────────

@pytest.mark.parametrize("bad_status", ["assessment_complete", "not_required", "assessment_optional", ""])
def test_economic_assessment_readiness_forced_value_violation_single_part(bad_status):
    data = _record(capital_use_type="CASH")
    data["economic_assessment_readiness"]["status"] = bad_status
    data["cross_asset_handoff"]["economic_assessment_readiness_summary"]["status"] = bad_status
    _assert_invalid(data, contains="assessment_required")


def test_economic_assessment_readiness_forced_value_violation_two_part_avoided_cost():
    data = _record(capital_use_type="DEBT_REDUCTION")
    data["economic_assessment_readiness"]["avoided_borrowing_cost_readiness"]["status"] = "assessment_complete"
    data["cross_asset_handoff"]["economic_assessment_readiness_summary"]["avoided_borrowing_cost_readiness"]["status"] = "assessment_complete"
    _assert_invalid(data, contains="assessment_required")


def test_economic_assessment_readiness_forced_value_violation_two_part_survivability():
    data = _record(capital_use_type="DEBT_REDUCTION")
    data["economic_assessment_readiness"]["survivability_and_buffer_benefit_readiness"]["status"] = "assessment_complete"
    data["cross_asset_handoff"]["economic_assessment_readiness_summary"]["survivability_and_buffer_benefit_readiness"]["status"] = "assessment_complete"
    _assert_invalid(data, contains="assessment_required")


# ── structural_reference presence/absence enforcement ─────────────────────

@pytest.mark.parametrize("capital_use_type", ["CASH", "RESERVE", "DEBT_REDUCTION"])
def test_structural_reference_present_on_non_gld_rejected(capital_use_type):
    data = _record(capital_use_type=capital_use_type)
    data["structural_reference"] = _structural_reference()
    _assert_invalid(data, contains="structural_reference")


def test_structural_reference_missing_on_gld_rejected():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    del data["structural_reference"]
    _assert_invalid(data, contains="structural_reference is required")


@pytest.mark.parametrize("missing_key", sorted(fdv._STRUCTURAL_REFERENCE_REQUIRED_KEYS))
def test_structural_reference_missing_sub_field_rejected(missing_key):
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    del data["structural_reference"][missing_key]
    _assert_invalid(data)


def test_structural_reference_wrong_source_instrument_id_rejected():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    data["structural_reference"]["source_instrument_id"] = "SPY"
    _assert_invalid(data, contains="source_instrument_id")


def test_structural_reference_wrong_source_schema_rejected():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    data["structural_reference"]["source_schema"] = "crypto_classification"
    _assert_invalid(data, contains="source_schema")


def test_structural_reference_wrong_source_file_rejected():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    data["structural_reference"]["source_file"] = "intelligence/etf_classification/SPY.yaml"
    _assert_invalid(data, contains="source_file")


def test_structural_reference_stale_hash_rejected_synthetic():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE", structural_reference=_structural_reference(hash_override="0" * 64))
    result = fdv.validate_functional_doctrine_data(data, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("stale" in e for e in result.errors)


def test_structural_reference_live_hash_matches_real_sealed_gld():
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    result = fdv.validate_functional_doctrine_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_structural_reference_skipped_without_repo_root():
    # In-memory validation with no filesystem access must not attempt the
    # live hash recompute -- a syntactically well-formed but unverifiable
    # hash should not itself cause failure when repo_root is None.
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE", structural_reference=_structural_reference(hash_override="0" * 64))
    result = fdv.validate_functional_doctrine_data(data, repo_root=None)
    assert result.valid, result.errors


# ── ETF axis key name leakage inside GLD_DEFENSIVE_ROLE, one per key ──────

@pytest.mark.parametrize("etf_axis_name", sorted(fdv._ETF_AXIS_KEY_NAMES))
def test_etf_axis_key_name_leakage_in_gld_record_rejected(etf_axis_name):
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    data[etf_axis_name] = {"anything": "value"}
    _assert_invalid(data, contains=etf_axis_name)


# ── hard_constraint_status / economic_assessment_readiness independence ──

def test_hard_constraint_status_and_economic_assessment_readiness_are_independent():
    """Mutating hard_constraint_status must never change economic_assessment_
    readiness's own validation result, and vice versa (XASSET-0005 SS7
    point 5's structural-independence requirement)."""
    base = _record(capital_use_type="CASH")

    def readiness_only_errors(data):
        errors = []
        fdv._validate_economic_assessment_readiness(data["economic_assessment_readiness"], data["capital_use_type"], errors)
        return errors

    def hard_constraint_only_errors(data):
        errors = []
        fdv._validate_hard_constraint_status(data["hard_constraint_status"], errors)
        return errors

    before_readiness = readiness_only_errors(base)
    before_hard_constraint = hard_constraint_only_errors(base)

    mutated = copy.deepcopy(base)
    mutated["hard_constraint_status"]["binding"] = True
    mutated["hard_constraint_status"]["constraint_source"] = "Some new binding constraint."
    assert readiness_only_errors(mutated) == before_readiness

    mutated2 = copy.deepcopy(base)
    mutated2["economic_assessment_readiness"]["status"] = "totally_invalid_value"
    assert hard_constraint_only_errors(mutated2) == before_hard_constraint


def test_hard_constraint_and_readiness_validators_are_separate_functions_with_no_shared_helper():
    """Static-analysis-style check: _validate_hard_constraint_status must
    never call _validate_economic_assessment_readiness (or any readiness
    sub-validator), and vice versa -- proves the independence is structural,
    not merely observed by the mutation test above."""
    import inspect

    hc_source = inspect.getsource(fdv._validate_hard_constraint_status)
    readiness_source = inspect.getsource(fdv._validate_economic_assessment_readiness)
    readiness_sub_source = inspect.getsource(fdv._validate_readiness_sub_object)

    assert "_validate_economic_assessment_readiness" not in hc_source
    assert "_validate_readiness_sub_object" not in hc_source
    assert "_validate_hard_constraint_status" not in readiness_source
    assert "_validate_hard_constraint_status" not in readiness_sub_source


# ── forbidden numeric/score/avoided-cost leakage, no positive-acceptance test ─

@pytest.mark.parametrize("bad_key", sorted(fdv._NUMERIC_LEAKAGE_KEYS))
def test_forbidden_numeric_key_leakage_rejected(bad_key):
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = "none"
    data[bad_key] = 42
    _assert_invalid(data, contains=bad_key)


def test_forbidden_numeric_key_leakage_nested_rejected():
    data = _record(capital_use_type="CASH")
    data["functional_role"]["target_pct"] = 1.0
    _assert_invalid(data, contains="target_pct")


def test_no_numeric_field_carve_out_of_any_kind():
    """Unlike the ETF framework's scoped expense_ratio_pct exception, the
    functional-doctrine schema has zero numeric-field exceptions -- a
    numeric-shaped key is never legitimate anywhere (XASSET-0005 supporting
    artifact SS3.3's closing statement)."""
    assert "expense_ratio_pct" not in fdv._ALL_TOP_LEVEL_KEYS
    for axis_keys in (
        fdv._FUNCTIONAL_ROLE_ALLOWED_KEYS, fdv._HARD_CONSTRAINT_ALLOWED_KEYS,
        fdv._READINESS_SUB_ALLOWED_KEYS, fdv._LIQUIDITY_CHARACTER_ALLOWED_KEYS,
        fdv._CAPITAL_PRESERVATION_CHARACTER_ALLOWED_KEYS, fdv._FRESHNESS_STATE_ALLOWED_KEYS,
        fdv._EVIDENCE_QUALITY_ALLOWED_KEYS,
    ):
        assert not (axis_keys & fdv._NUMERIC_LEAKAGE_KEYS)


# ── cross-schema field-name leakage, one per source schema ────────────────

@pytest.mark.parametrize("equity_key", sorted(fdv._EQUITY_FIELD_LEAKAGE))
def test_equity_field_leakage_rejected(equity_key):
    data = _record(capital_use_type="CASH")
    data[equity_key] = "value"
    _assert_invalid(data, contains=equity_key)


@pytest.mark.parametrize("crypto_key", sorted(fdv._CRYPTO_FIELD_LEAKAGE))
def test_crypto_field_leakage_rejected(crypto_key):
    data = _record(capital_use_type="CASH")
    data[crypto_key] = "value"
    _assert_invalid(data, contains=crypto_key)


@pytest.mark.parametrize("etf_key", sorted(fdv._ETF_AXIS_KEY_NAMES))
def test_etf_field_leakage_rejected_on_non_gld_record_too(etf_key):
    data = _record(capital_use_type="CASH")
    data[etf_key] = "value"
    _assert_invalid(data, contains=etf_key)


# ── abstention behavior ────────────────────────────────────────────────────

def test_unable_to_determine_without_abstention_reason_rejected():
    data = _record(capital_use_type="RESERVE", functional_role={"role_category": "unable_to_determine"})
    _assert_invalid(data, contains="abstention_reason")


def test_unable_to_determine_freshness_without_abstention_reason_rejected():
    data = _record(capital_use_type="DEBT_REDUCTION", freshness_state={"status": "unable_to_determine_freshness", "as_of_reference": "x"})
    _assert_invalid(data, contains="abstention_reason")


def test_not_applicable_on_axis_that_does_not_support_it_rejected_functional_role():
    # functional_role's closed vocabulary has no 'not_applicable' value at all.
    data = _record(capital_use_type="CASH", functional_role={"role_category": "not_applicable"})
    _assert_invalid(data)


def test_not_applicable_liquidity_reserved_for_debt_reduction_rejected_on_cash():
    data = _record(capital_use_type="CASH", liquidity_character={"liquidity_category": "not_applicable"})
    _assert_invalid(data, contains="reserved for DEBT_REDUCTION")


def test_not_applicable_liquidity_permitted_on_debt_reduction():
    data = _record(capital_use_type="DEBT_REDUCTION")
    assert data["liquidity_character"]["liquidity_category"] == "not_applicable"
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


def test_capital_preservation_character_has_no_not_applicable_value():
    assert "not_applicable" not in fdv._CAPITAL_PRESERVATION_CATEGORY_VALUES


def test_hard_constraint_status_has_no_abstention_path():
    assert "abstention_reason" not in fdv._HARD_CONSTRAINT_ALLOWED_KEYS
    assert fdv._UNABLE_TO_DETERMINE_VALUE not in {"binding"}  # binding is boolean-only, sanity


def test_fully_populated_abstention_accepted():
    data = _record(
        capital_use_type="RESERVE",
        functional_role={"role_category": "unable_to_determine", "abstention_reason": "genuine gap"},
        abstention_index=[{"axis": "functional_role", "field": "role_category", "value": "unable_to_determine", "reason": "genuine gap"}],
    )
    data["cross_asset_handoff"]["role_summary"] = "unable_to_determine"
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


def test_abstention_index_missing_entry_for_real_abstention_rejected():
    data = _record(
        capital_use_type="RESERVE",
        functional_role={"role_category": "unable_to_determine", "abstention_reason": "genuine gap"},
        abstention_index=[],
    )
    data["cross_asset_handoff"]["role_summary"] = "unable_to_determine"
    _assert_invalid(data, contains="abstention_index is missing an entry")


def test_abstention_does_not_cascade():
    """An abstention on functional_role must not force or imply abstention
    on any other axis (TIER-0004's established non-cascading precedent)."""
    data = _record(
        capital_use_type="RESERVE",
        functional_role={"role_category": "unable_to_determine", "abstention_reason": "genuine gap"},
        abstention_index=[{"axis": "functional_role", "field": "role_category", "value": "unable_to_determine", "reason": "genuine gap"}],
    )
    data["cross_asset_handoff"]["role_summary"] = "unable_to_determine"
    # liquidity_character and capital_preservation_character remain fully determined
    assert data["liquidity_character"]["liquidity_category"] == "immediately_liquid"
    assert data["capital_preservation_character"]["capital_preservation_category"] == "principal_stable_no_market_risk"
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


# ── duplicate/missing/extra capital_use_type in a manifest ────────────────

def _population_records() -> dict:
    return {
        cut: _record(capital_use_type=cut, sealed=True)
        for cut in fdv.AUTHORIZED_POPULATION
    }


def _manifest_row(rec: dict) -> dict:
    return {
        "capital_use_type": rec["capital_use_type"],
        "sealed_at": rec["sealed_at"],
        "content_sha256": rec["content_sha256"],
        "schema_version": rec["schema_version"],
        "governing_decision": rec["governing_decision"],
        "record_path": f"intelligence/functional_doctrine/{rec['capital_use_type']}.yaml",
    }


def test_manifest_duplicate_entry_rejected():
    records = _population_records()
    rows = [_manifest_row(r) for r in records.values()]
    rows.append(_manifest_row(records["CASH"]))  # duplicate
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": rows}
    result = fdv.validate_cohort_manifest(manifest, records)
    assert not result.valid
    assert any("more than once" in e for e in result.errors)


def test_manifest_missing_entry_from_population_rejected():
    records = _population_records()
    rows = [_manifest_row(r) for k, r in records.items() if k != "DEBT_REDUCTION"]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": rows}
    result = fdv.validate_cohort_manifest(manifest, {k: v for k, v in records.items() if k != "DEBT_REDUCTION"})
    assert not result.valid
    assert any("missing authorized" in e for e in result.errors)


def test_manifest_extra_entry_beyond_population_rejected():
    records = _population_records()
    rows = [_manifest_row(r) for r in records.values()]
    extra_record = _record(capital_use_type="CASH", sealed=True)
    extra_record["capital_use_type"] = "EXTRA_TYPE"
    extra_row = _manifest_row(extra_record)
    rows.append(extra_row)
    records_with_extra = dict(records)
    records_with_extra["EXTRA_TYPE"] = extra_record
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": rows}
    result = fdv.validate_cohort_manifest(manifest, records_with_extra)
    assert not result.valid
    assert any("outside the authorized population" in e for e in result.errors)


def test_manifest_orphan_sealed_record_rejected():
    records = _population_records()
    rows = [_manifest_row(r) for k, r in records.items() if k != "CASH"]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": rows}
    result = fdv.validate_cohort_manifest(manifest, records)
    assert not result.valid
    assert any("no corresponding cohort manifest entry" in e for e in result.errors)


def test_manifest_hash_mismatch_rejected():
    records = _population_records()
    rows = [_manifest_row(r) for r in records.values()]
    rows[0]["content_sha256"] = "0" * 64
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": rows}
    result = fdv.validate_cohort_manifest(manifest, records)
    assert not result.valid


def test_manifest_full_population_valid():
    records = _population_records()
    rows = [_manifest_row(r) for r in records.values()]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0006", "cohort": rows}
    result = fdv.validate_cohort_manifest(manifest, records)
    assert result.valid, result.errors


# ── chart-terminology leakage, one per term ────────────────────────────────

@pytest.mark.parametrize("term", fdv._CHART_TERMS)
def test_chart_terminology_leakage_rejected(term):
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = f"This mentions {term} in prose."
    _assert_invalid(data, contains="chart-derived terminology")


# ── directive/trading-language leakage, one per word ───────────────────────

@pytest.mark.parametrize("word", fdv._DIRECTIVE_WORDS)
def test_directive_word_leakage_rejected(word):
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = f"You should {word} this position now."
    _assert_invalid(data, contains="directive word")


def test_directive_word_false_positive_guard_fund_in_citation_string():
    """'fund'/'funded' inside a provenance citation string (pure
    bibliographic text, not judgment prose) must not be flagged -- the
    exact false-positive-guard test XASSET-0005 supporting artifact SS8
    requires, mirroring real content: GLD's own sealed ETF record cites
    "SPDR Gold Shares (GLD) fund page" verbatim."""
    data = _record(capital_use_type="GLD_DEFENSIVE_ROLE")
    data["provenance"]["sources"][0]["source_identifier"] = "SPDR Gold Shares (GLD) fund page, a fund of gold, fully funded"
    result = fdv.validate_functional_doctrine_data(data, repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_directive_word_false_positive_guard_limitation_field_citation():
    data = _record(capital_use_type="CASH")
    data["provenance"]["sources"][0]["limitation"] = "This fund's own disclosure was limited."
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


def test_directive_word_fund_still_flagged_outside_citation_fields():
    """The exemption is narrowly scoped to source_identifier/limitation --
    'fund' as an actual directive verb elsewhere in the document must still
    be caught."""
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = "A future session should fund this reserve immediately."
    _assert_invalid(data, contains="directive word")


def test_directive_word_hold_does_not_false_positive_on_holdings():
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = "See holdings.yaml for context; none required by this record."
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


def test_directive_word_exit_does_not_false_positive_on_exiting():
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = "No position is exiting or being exited by this record."
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


def test_directive_word_draw_does_not_false_positive_on_withdrawals():
    data = _record(capital_use_type="CASH")
    data["later_governance_action"] = "Recent withdrawals do not change this record's own facts."
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


# ── envelope-level read-only-projection consistency ────────────────────────

def test_role_summary_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    data["cross_asset_handoff"]["role_summary"] = "leverage_reduction"
    _assert_invalid(data, contains="role_summary")


def test_evidence_quality_summary_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    data["cross_asset_handoff"]["evidence_quality_summary"] = "comprehensive"
    _assert_invalid(data, contains="evidence_quality_summary")


def test_uncertainty_summary_envelope_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    data["evidence_quality"]["thesis_uncertainty_statement"] = "Something else entirely."
    _assert_invalid(data, contains="uncertainty_summary")


def test_liquidity_risk_summary_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    data["cross_asset_handoff"]["liquidity_risk_summary"] = "not_applicable"
    _assert_invalid(data, contains="liquidity_risk_summary")


def test_hard_constraint_signal_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    data["cross_asset_handoff"]["hard_constraint_signal"]["binding"] = True
    _assert_invalid(data, contains="hard_constraint_signal")


def test_hard_constraint_signal_never_merged_with_readiness_summary():
    """Structural proof the two handoff fields are separate objects with no
    shared key (SS3.3's "never merged" requirement)."""
    assert not (fdv._HARD_CONSTRAINT_SIGNAL_ALLOWED_KEYS & fdv._READINESS_SUB_ALLOWED_KEYS)


def test_economic_assessment_readiness_summary_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    # Full replacement (not an in-place mutation of the shared object the
    # fixture builder points both fields at) -- otherwise mutating one
    # would mutate the other and the two would stay equal.
    data["cross_asset_handoff"]["economic_assessment_readiness_summary"] = {
        "status": "assessment_required", "rationale": "A completely different rationale text.",
    }
    _assert_invalid(data, contains="economic_assessment_readiness_summary")


def test_structural_risk_flags_mismatch_rejected():
    data = _record(capital_use_type="CASH")
    data["structural_risk_flags"]["binding"] = not data["structural_risk_flags"]["binding"]
    _assert_invalid(data, contains="structural_risk_flags")


def test_structural_risk_flags_absent_entirely_rejected():
    """A required envelope field needs its own independent presence/type
    check -- etf_classification_validator.py's own disclosed MINOR-1
    lesson, applied here from the start (XASSET-0005 supporting artifact
    SS8.1)."""
    data = _record(capital_use_type="CASH")
    del data["structural_risk_flags"]
    _assert_invalid(data, contains="structural_risk_flags must be a mapping")


# ── hard_constraint_status.binding/constraint_source consistency ─────────

def test_hard_constraint_binding_true_requires_non_empty_source():
    data = _record(capital_use_type="CASH", hard_constraint_status={"binding": True, "constraint_source": "none_currently_binding"})
    _assert_invalid(data, contains="constraint_source")


def test_hard_constraint_binding_false_requires_literal_none_currently_binding():
    data = _record(capital_use_type="CASH", hard_constraint_status={"binding": False, "constraint_source": "Some citation."})
    _assert_invalid(data, contains="none_currently_binding")


# ── deterministic output ──────────────────────────────────────────────────

def test_deterministic_validation_output():
    data = _record(capital_use_type="DEBT_REDUCTION", sealed=True)
    r1 = fdv.validate_functional_doctrine_data(copy.deepcopy(data), repo_root=REPO_ROOT)
    r2 = fdv.validate_functional_doctrine_data(copy.deepcopy(data), repo_root=REPO_ROOT)
    assert r1.valid == r2.valid == True
    assert r1.errors == r2.errors == []


def test_canonical_record_hash_deterministic():
    data = _record(capital_use_type="CASH", sealed=True)
    h1 = fdv.canonical_record_hash(data)
    h2 = fdv.canonical_record_hash(data)
    assert h1 == h2


def test_canonical_record_hash_excludes_only_seal_fields():
    data = _record(capital_use_type="CASH", sealed=True)
    mutated = copy.deepcopy(data)
    mutated["sealed_at"] = "2099-01-01T00:00:00Z"
    mutated["governing_decision"] = "SOMETHING-ELSE"
    mutated["drafting_session_or_shard_id"] = "different-shard"
    mutated["cohort_manifest_entry"] = "different#entry"
    assert fdv.canonical_record_hash(mutated) == fdv.canonical_record_hash(data)

    mutated2 = copy.deepcopy(data)
    mutated2["functional_role"]["role_category"] = "leverage_reduction"
    assert fdv.canonical_record_hash(mutated2) != fdv.canonical_record_hash(data)


# ── seal / content hash reproduction ───────────────────────────────────────

def test_sealed_record_content_hash_must_reproduce():
    data = _record(capital_use_type="CASH", sealed=True)
    data["content_sha256"] = "0" * 64
    _assert_invalid(data, contains="does not reproduce")


def test_draft_record_does_not_require_seal_fields():
    data = _record(capital_use_type="CASH", sealed=False)
    for k in fdv._SEAL_REQUIRED_KEYS:
        assert k not in data
    result = fdv.validate_functional_doctrine_data(data)
    assert result.valid, result.errors


# ── filename stem matching ─────────────────────────────────────────────────

def test_filename_stem_mismatch_rejected(tmp_path):
    data = _record(capital_use_type="CASH", sealed=True)
    path = tmp_path / "WRONG_NAME.yaml"
    path.write_text(yaml.safe_dump(data))
    result = fdv.validate_functional_doctrine_file(path)
    assert not result.valid
    assert any("does not match" in e for e in result.errors)


def test_filename_stem_match_accepted(tmp_path):
    data = _record(capital_use_type="CASH", sealed=True)
    path = tmp_path / "CASH.yaml"
    path.write_text(yaml.safe_dump(data))
    result = fdv.validate_functional_doctrine_file(path)
    assert result.valid, result.errors


def test_malformed_yaml_file_rejected(tmp_path):
    path = tmp_path / "CASH.yaml"
    path.write_text(": not: valid: yaml: [")
    result = fdv.validate_functional_doctrine_file(path)
    assert not result.valid


def test_missing_file_rejected(tmp_path):
    result = fdv.validate_functional_doctrine_file(tmp_path / "DOES_NOT_EXIST.yaml")
    assert not result.valid


def test_empty_file_rejected(tmp_path):
    path = tmp_path / "CASH.yaml"
    path.write_text("")
    result = fdv.validate_functional_doctrine_file(path)
    assert not result.valid


# ── protected-path isolation ────────────────────────────────────────────────

_PROTECTED_PATHS = [
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "allocate.py", "margin_state.py", "levels.py",
]


def test_protected_paths_untouched_by_this_module_import():
    """Importing/using this validator module must never mutate any
    protected repository path (XASSET-0005 supporting artifact SS7 point
    14)."""
    hashes_before = {}
    for rel in _PROTECTED_PATHS:
        p = REPO_ROOT / rel
        if p.is_file():
            hashes_before[rel] = p.read_bytes()

    fdv.validate_functional_doctrine_directory(REPO_ROOT / "intelligence" / "functional_doctrine", repo_root=REPO_ROOT)

    for rel, before in hashes_before.items():
        assert (REPO_ROOT / rel).read_bytes() == before, f"{rel} was mutated"


def test_protected_intelligence_records_untouched():
    """Zero diff on every existing intelligence/classification|companies|
    themes|relationships|etf_classification|crypto_classification/ record
    and COHORT_MANIFEST.yaml -- checked via a live git status/diff, not
    merely a file-content snapshot, so a staged-but-uncommitted change
    would also be caught."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "intelligence/etf_classification", "intelligence/crypto_classification",
         "intelligence/classification", "intelligence/companies", "intelligence/themes", "intelligence/relationships"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert result.stdout.strip() == "", f"unexpected changes under protected intelligence paths:\n{result.stdout}"


# ── allocator/margin import-coupling isolation ─────────────────────────────

def test_validator_module_imports_neither_allocate_nor_margin_state():
    """Static-analysis-style check confirming the validator module imports
    neither allocate.py nor margin_state.py, in either direction (XASSET-
    0005 supporting artifact SS7 point 12)."""
    source = (REPO_ROOT / "functional_doctrine_validator.py").read_text()
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
        assert "functional_doctrine_validator" not in source


# ── real repository directory scan ──────────────────────────────────────────

def test_real_repository_functional_doctrine_directory_all_valid():
    result = fdv.validate_functional_doctrine_directory(
        REPO_ROOT / "intelligence" / "functional_doctrine", repo_root=REPO_ROOT,
    )
    assert result.valid, [
        (r.source, r.errors) for r in result.results if not r.valid
    ]


def test_real_repository_functional_doctrine_directory_exact_population():
    result = fdv.validate_functional_doctrine_directory(
        REPO_ROOT / "intelligence" / "functional_doctrine", repo_root=REPO_ROOT,
    )
    assert result.record_count == 5  # 4 capital-use-type records + 1 manifest result


def test_real_functional_doctrine_files_exact_four_capital_use_types():
    directory = REPO_ROOT / "intelligence" / "functional_doctrine"
    yaml_files = sorted(p.stem for p in directory.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml")
    assert set(yaml_files) == fdv.AUTHORIZED_POPULATION


def test_real_functional_doctrine_overlap_model_directory_is_a_sibling_not_a_subject():
    """`intelligence/overlap_model/` is now populated (XASSET-0007's own
    authorized content implementation) -- this test no longer asserts its
    absence (that assertion was accurate only for the functional-doctrine-
    only implementation scaffold this file was originally authored under,
    the same scaffold-superseded-by-authorized-content pattern already
    applied elsewhere in this repository, e.g. the ETF/crypto/valuation
    validators' own TestZeroRealCompanyPopulation -> TestAuthorizedCohort
    Population precedent). What remains true, and is what this test now
    asserts: this module (`functional_doctrine_validator.py`) validates
    `intelligence/functional_doctrine/` only -- it has no knowledge of, and
    performs no validation against, `intelligence/overlap_model/`, which is
    validated entirely by its own sibling module, `overlap_model_validator
    .py` (test_overlap_model_validator.py's own scope)."""
    overlap_model_dir = REPO_ROOT / "intelligence" / "overlap_model"
    assert overlap_model_dir.exists() and overlap_model_dir.is_dir()
    result = fdv.validate_functional_doctrine_directory(overlap_model_dir, repo_root=REPO_ROOT)
    # A directory containing only overlap-model records (none of which
    # carries a capital_use_type field) is not a valid functional-doctrine
    # directory from this module's own point of view -- each of the ten
    # files correctly fails to parse as a functional-doctrine record,
    # confirming this module performs no cross-schema validation of
    # overlap-model content, not merely that it happens not to have been
    # pointed there.
    assert not result.valid


def test_real_gld_defensive_role_structural_reference_matches_live_gld():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "GLD_DEFENSIVE_ROLE.yaml").read_text())
    import etf_classification_validator as etf
    gld_data = yaml.safe_load((REPO_ROOT / "intelligence" / "etf_classification" / "GLD.yaml").read_text())
    live_hash = etf.canonical_record_hash(gld_data)
    assert data["structural_reference"]["referenced_content_sha256"] == live_hash


def test_real_reserve_functional_role_is_abstained():
    """Confirms the genuine, disclosed RESERVE evidence-sufficiency
    determination (XASSET-0006 SS C.1) was actually resolved via
    abstention, not a forced value."""
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "RESERVE.yaml").read_text())
    assert data["functional_role"]["role_category"] == "unable_to_determine"
    assert data["functional_role"]["abstention_reason"]


def test_real_debt_reduction_freshness_state_is_abstained():
    """Confirms the genuine, disclosed DEBT_REDUCTION evidence-sufficiency
    determination (XASSET-0006 SS C.2) was actually resolved via
    abstention, not a forced citation of a live-state field."""
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "DEBT_REDUCTION.yaml").read_text())
    assert data["freshness_state"]["status"] == "unable_to_determine_freshness"
    assert data["freshness_state"]["abstention_reason"]


def test_real_cash_functional_role_is_determined_not_abstained():
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "functional_doctrine" / "CASH.yaml").read_text())
    assert data["functional_role"]["role_category"] != "unable_to_determine"


def test_real_no_overlap_model_field_names_appear_anywhere_in_functional_doctrine_records():
    overlap_field_names = {
        "dimension_id", "dimension_type", "source_mechanism", "computation_status",
        "evidence_or_source_refs", "output_shape", "uncertainty_or_gap_disclosure",
    }
    directory = REPO_ROOT / "intelligence" / "functional_doctrine"
    for p in directory.glob("*.yaml"):
        data = yaml.safe_load(p.read_text())

        def walk(v):
            if isinstance(v, dict):
                for k, vv in v.items():
                    assert k not in overlap_field_names, f"{p.name} leaks overlap-model field {k!r}"
                    walk(vv)
            elif isinstance(v, list):
                for item in v:
                    walk(item)

        walk(data)
