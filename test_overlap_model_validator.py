"""Tests for overlap_model_validator.py (WS-0014 cross-asset overlap/
concentration-model schema, XASSET-0005/XASSET-0007 scope).

Every schema/behavior test below constructs its own synthetic fixture -- no
real dimension's populated evidence content is asserted against beyond the
directory-scan tests, which exercise the real repository's
intelligence/overlap_model/ directory, authored under this one
implementation PR.

Functional-doctrine schema (XASSET-0005 supporting artifact S3) tests are
explicitly out of scope for this file -- that schema is validated entirely
by functional_doctrine_validator.py/test_functional_doctrine_validator.py,
untouched by this PR.
"""

from __future__ import annotations

import ast
import copy
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import overlap_model_validator as ov

REPO_ROOT = Path(__file__).resolve().parent
#: This file's own source, read by the AST hygiene checks below so they inspect the
#: real suite rather than a re-implementation of it.
SUITE_SOURCE_PATH = Path(__file__).resolve()


# ── fixtures ─────────────────────────────────────────────────────────────

def _record(dimension_id: str = ov.SLEEVE_CONCENTRATION, **overrides) -> dict:
    # Fall back to sleeve_concentration's own dimension_type/source_mechanism
    # when the caller supplies an out-of-population dimension_id on purpose
    # (a rejection-path fixture) -- the record must still be constructible.
    known = dimension_id in ov._DIMENSION_TYPE_BY_ID
    d = {
        "dimension_id": dimension_id,
        "schema_version": "1.0",
        "dimension_type": ov._DIMENSION_TYPE_BY_ID[dimension_id] if known else ov._MECHANICAL_ROLLUP,
        "source_mechanism": sorted(ov._CANONICAL_SOURCE_MECHANISMS[dimension_id]) if known else ["placeholder-mechanism"],
        "computation_status": (
            ov._NOT_YET_COMPUTABLE_INTERFACE_ONLY
            if dimension_id in ov.INTERFACE_PLACEHOLDER_DIMENSIONS
            else ov._COMPUTED_FROM_EXISTING_MECHANISM
        ),
        "evidence_or_source_refs": ["synthetic-fixture-pointer-one", "synthetic-fixture-pointer-two"],
        "output_shape": "Synthetic description of a future categorical output shape.",
        "uncertainty_or_gap_disclosure": "Synthetic disclosed evidence gap for this fixture.",
        "later_governance_action": "none",
        "record_status": "draft",
    }
    d.update(overrides)
    return d


def _sealed(base_dimension_id: str = ov.SLEEVE_CONCENTRATION, **overrides) -> dict:
    dimension_id = overrides.get("dimension_id", base_dimension_id)
    d = _record(base_dimension_id, record_status="sealed")
    d["dimension_id"] = dimension_id
    d.pop("record_status")
    content_hash = ov.canonical_record_hash({**d, "record_status": "sealed"})
    d.update({
        "record_status": "sealed",
        "sealed_at": "2026-08-10T00:00:00Z",
        "governing_decision": "XASSET-0007",
        "drafting_session_or_shard_id": "test-shard",
        "content_sha256": content_hash,
        "cohort_manifest_entry": f"intelligence/overlap_model/COHORT_MANIFEST.yaml#{dimension_id}",
    })
    d.update(overrides)
    return d


# ── happy path, one per dimension_id (draft) ────────────────────────────

@pytest.mark.parametrize("dimension_id", sorted(ov.AUTHORIZED_POPULATION))
def test_happy_path_draft_record_valid_for_every_dimension(dimension_id):
    result = ov.validate_overlap_model_data(_record(dimension_id))
    assert result.valid, result.errors


@pytest.mark.parametrize("dimension_id", sorted(ov.AUTHORIZED_POPULATION))
def test_happy_path_sealed_record_valid_for_every_dimension(dimension_id):
    result = ov.validate_overlap_model_data(_sealed(dimension_id))
    assert result.valid, result.errors


# ── malformed root / missing required field ─────────────────────────────

def test_non_dict_root_rejected():
    result = ov.validate_overlap_model_data(["not", "a", "mapping"])
    assert not result.valid
    assert any("must be a mapping" in e for e in result.errors)


@pytest.mark.parametrize("field_name", [
    "dimension_id", "schema_version", "dimension_type", "source_mechanism",
    "computation_status", "evidence_or_source_refs", "output_shape",
    "uncertainty_or_gap_disclosure", "later_governance_action",
])
def test_missing_required_field_rejected(field_name):
    d = _record()
    del d[field_name]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any(field_name in e for e in result.errors)


def test_missing_record_status_rejected():
    d = _record()
    del d["record_status"]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── extra/unknown key rejection at top level ─────────────────────────────

def test_extra_top_level_key_rejected():
    d = _record(smuggled_extra_field="anything")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("smuggled_extra_field" in e for e in result.errors)


def test_no_abstention_index_field_on_this_schema():
    """S6.2's own explicit design choice -- unlike the functional-doctrine
    schema's several independently-abstaining axes, this schema has no
    abstention_index rollup."""
    d = _record(abstention_index=[])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("abstention_index" in e for e in result.errors)


def test_no_cross_asset_handoff_field_on_this_schema():
    """S6.2's own explicit design choice -- unlike the instrument-level ETF/
    crypto/functional-doctrine records, this schema has no
    cross_asset_handoff sub-object."""
    d = _record(cross_asset_handoff={"role_summary": "x"})
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("cross_asset_handoff" in e for e in result.errors)


# ── wrong dimension_id ───────────────────────────────────────────────────

def test_wrong_dimension_id_outside_closed_population_rejected():
    d = _record(dimension_id="not_a_real_dimension")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("not in the authorized ten-dimension population" in e for e in result.errors)


def test_empty_dimension_id_rejected():
    d = _record(dimension_id="")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── dimension_type / dimension_id lock ──────────────────────────────────

def test_wrong_dimension_type_value_rejected():
    d = _record(dimension_type="not_a_real_type")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("dimension_type must be one of" in e for e in result.errors)


def test_dimension_type_mismatched_against_dimension_id_rejected():
    d = _record(ov.SLEEVE_CONCENTRATION, dimension_type=ov._INTERFACE_PLACEHOLDER)
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("dimension_type must be exactly" in e for e in result.errors)


@pytest.mark.parametrize("dimension_id", sorted(ov.INTERFACE_PLACEHOLDER_DIMENSIONS))
def test_interface_placeholder_dimension_type_locked(dimension_id):
    d = _record(dimension_id, dimension_type=ov._MECHANICAL_ROLLUP)
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── computation_status forced-value violation, all four interface_placeholder
#    dimensions individually (XASSET-0007 SS B's own corrected test item) ───

@pytest.mark.parametrize("dimension_id", sorted(ov.INTERFACE_PLACEHOLDER_DIMENSIONS))
@pytest.mark.parametrize("bad_status", [
    ov._COMPUTED_FROM_EXISTING_MECHANISM, ov._REQUIRES_FUTURE_AUTHORIZATION,
])
def test_interface_placeholder_forced_value_violation_all_four_dimensions(dimension_id, bad_status):
    d = _record(dimension_id, computation_status=bad_status)
    result = ov.validate_overlap_model_data(d)
    assert not result.valid, f"{dimension_id} with {bad_status} should have been rejected"
    assert any("must be exactly" in e and "interface_placeholder" in e for e in result.errors)


@pytest.mark.parametrize("dimension_id", sorted(ov._MECHANICAL_OR_NARRATIVE_DIMENSIONS))
def test_mechanical_or_narrative_dimension_cannot_use_forced_interface_value(dimension_id):
    d = _record(dimension_id, computation_status=ov._NOT_YET_COMPUTABLE_INTERFACE_ONLY)
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("reserved for the four interface_placeholder" in e for e in result.errors)


@pytest.mark.parametrize("dimension_id", sorted(ov._MECHANICAL_OR_NARRATIVE_DIMENSIONS))
@pytest.mark.parametrize("status", [
    ov._COMPUTED_FROM_EXISTING_MECHANISM, ov._REQUIRES_FUTURE_AUTHORIZATION,
])
def test_mechanical_or_narrative_dimension_accepts_either_non_forced_value(dimension_id, status):
    d = _record(dimension_id, computation_status=status)
    result = ov.validate_overlap_model_data(d)
    assert result.valid, result.errors


def test_wrong_computation_status_value_rejected():
    d = _record(computation_status="not_a_real_status")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("computation_status must be one of" in e for e in result.errors)


def test_gld_defensive_role_now_existing_does_not_loosen_forced_value():
    """XASSET-0007 SS A point 2/SS D: the forced value stays
    not_yet_computable_interface_only even though GLD_DEFENSIVE_ROLE.yaml
    now exists and is sealed -- a record attempting to loosen it must still
    be rejected."""
    d = _record(ov.DEFENSIVE_OFFSET_INTERFACE, computation_status=ov._COMPUTED_FROM_EXISTING_MECHANISM)
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── source_mechanism: closed per-dimension canonical set, exact match ──────

def test_unauthorized_source_mechanism_rejected():
    d = _record(source_mechanism=["some_file_never_named_in_the_design.yaml"])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("must equal exactly" in e for e in result.errors)


def test_source_mechanism_subset_rejected():
    """economic_role_overlap names three mechanisms -- a record citing only
    one is not authorized (must equal the full canonical set exactly)."""
    d = _record(ov.ECONOMIC_ROLE_OVERLAP, source_mechanism=["intelligence/classification/<TICKER>.yaml:economic_role"])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_source_mechanism_with_extra_uncited_mechanism_rejected():
    d = _record(source_mechanism=[*sorted(ov._CANONICAL_SOURCE_MECHANISMS[ov.SLEEVE_CONCENTRATION]), "an_extra_uncited_file.yaml"])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_source_mechanism_duplicate_entry_rejected():
    canonical = sorted(ov._CANONICAL_SOURCE_MECHANISMS[ov.SLEEVE_CONCENTRATION])
    d = _record(source_mechanism=[*canonical, canonical[0]])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("duplicate" in e for e in result.errors)


def test_source_mechanism_empty_list_rejected():
    d = _record(source_mechanism=[])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_source_mechanism_wrong_dimension_cross_pollination_rejected():
    """Citing crypto_correlation_interface's own canonical mechanism on a
    sleeve_concentration record is not authorized -- source_mechanism is
    tied to the specific dimension_id, not interchangeable."""
    d = _record(
        ov.SLEEVE_CONCENTRATION,
        source_mechanism=sorted(ov._CANONICAL_SOURCE_MECHANISMS[ov.CRYPTO_CORRELATION_INTERFACE]),
    )
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── evidence_or_source_refs / output_shape ──────────────────────────────

def test_evidence_or_source_refs_empty_list_rejected():
    d = _record(evidence_or_source_refs=[])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_evidence_or_source_refs_non_string_entry_rejected():
    d = _record(evidence_or_source_refs=["fine", 42])
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_output_shape_empty_string_rejected():
    d = _record(output_shape="")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_uncertainty_or_gap_disclosure_empty_string_rejected():
    d = _record(uncertainty_or_gap_disclosure="   ")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_later_governance_action_empty_string_rejected():
    d = _record(later_governance_action="")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_later_governance_action_literal_none_accepted():
    d = _record(later_governance_action="none")
    result = ov.validate_overlap_model_data(d)
    assert result.valid, result.errors


# ── forbidden numeric/score/avoided-cost key leakage, individually ─────────

@pytest.mark.parametrize("key", sorted(ov._NUMERIC_LEAKAGE_KEYS))
def test_forbidden_numeric_leakage_key_rejected_individually(key):
    d = _record()
    d["evidence_or_source_refs"] = [{"pointer": "x", key: 5}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid, f"{key} should have been rejected"
    assert any(key in e for e in result.errors)


def test_no_positive_numeric_acceptance_test_exists_for_this_schema():
    """Unlike the ETF framework's own scoped expense_ratio_pct exception,
    this design carries zero numeric-field carve-outs of any kind
    (XASSET-0005 supporting artifact S3.3's closing statement, applied
    identically to S6) -- confirmed structurally: none of the schema's nine
    named substantive fields is itself numeric."""
    assert not any(k in ov._NUMERIC_LEAKAGE_KEYS for k in ov._SUBSTANTIVE_FIELDS)


# ── forbidden composite-overlap-score pattern, individually and across
#    the full ten-record set together ────────────────────────────────────

@pytest.mark.parametrize("key", sorted(ov._COMPOSITE_SCORE_KEYS))
def test_forbidden_composite_score_key_rejected_individually(key):
    d = _record()
    d["evidence_or_source_refs"] = [{"note": "x", key: 1}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid, f"{key} should have been rejected"


def test_forbidden_composite_score_rejected_across_full_ten_record_set(tmp_path):
    """S6.3 point 2: the scan runs against the full ten-record set together,
    not merely within one record in isolation -- exercised here via the
    directory-level validator with a synthetic ten-record cohort, one of
    which smuggles a composite key."""
    records = {dim: _sealed(dim) for dim in ov.AUTHORIZED_POPULATION}
    poisoned_id = ov.SLEEVE_CONCENTRATION
    poisoned = copy.deepcopy(records[poisoned_id])
    poisoned["evidence_or_source_refs"] = [{"overlap_index": 1}]
    # recompute the seal hash so this synthetic record's own per-file check
    # passes cleanly and the composite key is caught by the combined-set
    # scan specifically, not merely the ordinary per-record scan.
    unsealed = {k: v for k, v in poisoned.items() if k not in ov._SEAL_REQUIRED_KEYS}
    unsealed["record_status"] = "sealed"
    poisoned["content_sha256"] = ov.canonical_record_hash(unsealed)
    records[poisoned_id] = poisoned

    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0007",
        "cohort": [
            {
                "dimension_id": dim,
                "sealed_at": rec["sealed_at"],
                "content_sha256": rec["content_sha256"],
                "schema_version": rec["schema_version"],
                "governing_decision": rec["governing_decision"],
                "record_path": f"intelligence/overlap_model/{dim}.yaml",
            }
            for dim, rec in records.items()
        ],
    }
    d = tmp_path / "overlap_model"
    d.mkdir()
    for dim, rec in records.items():
        (d / f"{dim}.yaml").write_text(yaml.safe_dump(rec, sort_keys=False))
    (d / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))

    result = ov.validate_overlap_model_directory(d)
    assert not result.valid
    all_errors = [e for r in result.results for e in r.errors]
    assert any("overlap_index" in e for e in all_errors)


# ── cross-schema field-name leakage, per source schema ──────────────────

@pytest.mark.parametrize("key", sorted(ov._EQUITY_FIELD_LEAKAGE))
def test_equity_shaped_field_leakage_rejected(key):
    d = _record()
    d["evidence_or_source_refs"] = [{key: "leaked"}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any(key in e and "equity" in e for e in result.errors)


@pytest.mark.parametrize("key", sorted(ov._ETF_FIELD_LEAKAGE))
def test_etf_shaped_field_leakage_rejected(key):
    d = _record()
    d["evidence_or_source_refs"] = [{key: "leaked"}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any(key in e and "ETF" in e for e in result.errors)


@pytest.mark.parametrize("key", sorted(ov._CRYPTO_FIELD_LEAKAGE))
def test_crypto_shaped_field_leakage_rejected(key):
    d = _record()
    d["evidence_or_source_refs"] = [{key: "leaked"}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any(key in e and "crypto" in e for e in result.errors)


@pytest.mark.parametrize("key", sorted(ov._FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE))
def test_functional_doctrine_shaped_field_leakage_rejected(key):
    d = _record()
    d["evidence_or_source_refs"] = [{key: "leaked"}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any(key in e and "functional-doctrine" in e for e in result.errors)


def test_forbidden_key_leakage_detected_at_nested_depth():
    d = _record()
    d["evidence_or_source_refs"] = [{"nested": {"deeper": [{"conviction": "leaked"}]}}]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── duplicate / missing / extra dimension_id against the named population ──

def test_duplicate_dimension_id_in_manifest_rejected(tmp_path):
    records = {dim: _sealed(dim) for dim in ov.AUTHORIZED_POPULATION}
    manifest_rows = [
        {
            "dimension_id": dim,
            "sealed_at": rec["sealed_at"],
            "content_sha256": rec["content_sha256"],
            "schema_version": rec["schema_version"],
            "governing_decision": rec["governing_decision"],
            "record_path": f"intelligence/overlap_model/{dim}.yaml",
        }
        for dim, rec in records.items()
    ]
    manifest_rows.append(manifest_rows[0])  # duplicate
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0007", "cohort": manifest_rows}
    result = ov.validate_cohort_manifest(manifest, records)
    assert not result.valid
    assert any("more than once" in e for e in result.errors)


def test_missing_dimension_id_from_manifest_rejected():
    records = {dim: _sealed(dim) for dim in ov.AUTHORIZED_POPULATION}
    del records[ov.SLEEVE_CONCENTRATION]
    manifest_rows = [
        {
            "dimension_id": dim,
            "sealed_at": rec["sealed_at"],
            "content_sha256": rec["content_sha256"],
            "schema_version": rec["schema_version"],
            "governing_decision": rec["governing_decision"],
            "record_path": f"intelligence/overlap_model/{dim}.yaml",
        }
        for dim, rec in records.items()
    ]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0007", "cohort": manifest_rows}
    result = ov.validate_cohort_manifest(manifest, records)
    assert not result.valid
    assert any("missing authorized dimension_id" in e for e in result.errors)


def test_extra_dimension_id_beyond_population_rejected():
    records = {dim: _sealed(dim) for dim in ov.AUTHORIZED_POPULATION}
    extra = _sealed(ov.SLEEVE_CONCENTRATION, dimension_id="eleventh_unauthorized_dimension")
    records["eleventh_unauthorized_dimension"] = extra
    manifest_rows = [
        {
            "dimension_id": dim,
            "sealed_at": rec["sealed_at"],
            "content_sha256": rec["content_sha256"],
            "schema_version": rec["schema_version"],
            "governing_decision": rec["governing_decision"],
            "record_path": f"intelligence/overlap_model/{dim}.yaml",
        }
        for dim, rec in records.items()
    ]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0007", "cohort": manifest_rows}
    result = ov.validate_cohort_manifest(manifest, records, authorized_population=ov.AUTHORIZED_POPULATION)
    assert not result.valid
    assert any("outside the authorized population" in e for e in result.errors)


def test_orphan_sealed_record_with_no_manifest_entry_rejected():
    records = {dim: _sealed(dim) for dim in ov.AUTHORIZED_POPULATION}
    manifest_rows = [
        {
            "dimension_id": dim,
            "sealed_at": rec["sealed_at"],
            "content_sha256": rec["content_sha256"],
            "schema_version": rec["schema_version"],
            "governing_decision": rec["governing_decision"],
            "record_path": f"intelligence/overlap_model/{dim}.yaml",
        }
        for dim, rec in records.items()
        if dim != ov.SLEEVE_CONCENTRATION
    ]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0007", "cohort": manifest_rows}
    result = ov.validate_cohort_manifest(manifest, records, authorized_population=None)
    assert not result.valid
    assert any("no corresponding cohort manifest entry" in e for e in result.errors)


def test_manifest_hash_mismatch_rejected():
    records = {dim: _sealed(dim) for dim in ov.AUTHORIZED_POPULATION}
    manifest_rows = [
        {
            "dimension_id": dim,
            "sealed_at": rec["sealed_at"],
            "content_sha256": "0" * 64,
            "schema_version": rec["schema_version"],
            "governing_decision": rec["governing_decision"],
            "record_path": f"intelligence/overlap_model/{dim}.yaml",
        }
        for dim, rec in records.items()
    ]
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0007", "cohort": manifest_rows}
    result = ov.validate_cohort_manifest(manifest, records)
    assert not result.valid
    assert any("content_sha256 mismatch" in e for e in result.errors)


def test_manifest_row_missing_required_key_rejected():
    manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0007", "cohort": [{"dimension_id": ov.SLEEVE_CONCENTRATION}]}
    result = ov.validate_cohort_manifest(manifest, {})
    assert not result.valid
    assert any("missing required key" in e for e in result.errors)


def test_manifest_top_level_not_a_mapping_rejected():
    result = ov.validate_cohort_manifest(["not", "a", "mapping"], {})
    assert not result.valid


# ── chart-terminology leakage, per term ──────────────────────────────────

@pytest.mark.parametrize("term", ov._CHART_TERMS)
def test_chart_terminology_leakage_rejected(term):
    d = _record(uncertainty_or_gap_disclosure=f"This dimension shows a clear {term} pattern.")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid, f"{term} should have been rejected"


# ── directive/trading-language leakage, per word ─────────────────────────

@pytest.mark.parametrize("word", ov._DIRECTIVE_WORDS)
def test_directive_word_leakage_rejected(word):
    d = _record(later_governance_action=f"A future unit should {word} accordingly.")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid, f"{word} should have been rejected"


def test_directive_word_false_positive_guard_holdings_not_flagged():
    d = _record(uncertainty_or_gap_disclosure="This dimension cross-references the account's own holdings.yaml equivalent facts.")
    result = ov.validate_overlap_model_data(d)
    assert result.valid, result.errors


def test_directive_word_false_positive_guard_address_not_flagged():
    d = _record(later_governance_action="A future unit would need to address this evidence gap.")
    result = ov.validate_overlap_model_data(d)
    assert result.valid, result.errors


def test_directive_word_false_positive_guard_exiting_not_flagged():
    d = _record(uncertainty_or_gap_disclosure="No instrument is exiting the canonical roster as a result of this dimension.")
    result = ov.validate_overlap_model_data(d)
    assert result.valid, result.errors


# ── forbidden recommendation-shaped phrases ──────────────────────────────

def test_forbidden_recommendation_phrase_rejected():
    d = _record(later_governance_action="This dimension recommends a target of the sleeve.")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_forbidden_percent_of_book_pattern_rejected():
    d = _record(uncertainty_or_gap_disclosure="The sleeve sits at 12.5% of book today.")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── filename stem match ──────────────────────────────────────────────────

def test_filename_stem_mismatch_rejected(tmp_path):
    p = tmp_path / "wrong_filename.yaml"
    p.write_text(yaml.safe_dump(_sealed(ov.SLEEVE_CONCENTRATION), sort_keys=False))
    result = ov.validate_overlap_model_file(p)
    assert not result.valid
    assert any("does not match the record's own dimension_id" in e for e in result.errors)


def test_missing_file_rejected(tmp_path):
    result = ov.validate_overlap_model_file(tmp_path / "does_not_exist.yaml")
    assert not result.valid


def test_empty_file_rejected(tmp_path):
    p = tmp_path / "empty.yaml"
    p.write_text("")
    result = ov.validate_overlap_model_file(p)
    assert not result.valid


def test_malformed_yaml_rejected(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("dimension_id: [unterminated")
    result = ov.validate_overlap_model_file(p)
    assert not result.valid


# ── seal / hash behavior ─────────────────────────────────────────────────

def test_draft_record_skips_seal_checks():
    d = _record(record_status="draft")
    result = ov.validate_overlap_model_data(d)
    assert result.valid, result.errors


def test_sealed_record_missing_seal_field_rejected():
    d = _sealed()
    del d["sealed_at"]
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


def test_sealed_record_wrong_content_hash_rejected():
    d = _sealed()
    d["content_sha256"] = "0" * 64
    result = ov.validate_overlap_model_data(d)
    assert not result.valid
    assert any("does not reproduce" in e for e in result.errors)


def test_wrong_record_status_value_rejected():
    d = _record(record_status="published")
    result = ov.validate_overlap_model_data(d)
    assert not result.valid


# ── determinism ───────────────────────────────────────────────────────────

def test_canonical_hash_deterministic():
    d = _sealed()
    h1 = ov.canonical_record_hash(d)
    h2 = ov.canonical_record_hash(copy.deepcopy(d))
    assert h1 == h2


def test_canonical_hash_excludes_seal_fields():
    d = _sealed()
    without_seal = {k: v for k, v in d.items() if k not in ov._SEAL_REQUIRED_KEYS}
    assert ov.canonical_record_hash(d) == ov.canonical_record_hash(without_seal)


def test_canonical_hash_changes_on_content_change():
    d = _sealed()
    mutated = copy.deepcopy(d)
    mutated["uncertainty_or_gap_disclosure"] = "A materially different disclosed gap."
    assert ov.canonical_record_hash(d) != ov.canonical_record_hash(mutated)


def test_repeated_directory_validation_deterministic():
    r1 = ov.validate_overlap_model_directory(REPO_ROOT / "intelligence" / "overlap_model")
    r2 = ov.validate_overlap_model_directory(REPO_ROOT / "intelligence" / "overlap_model")
    assert r1.valid == r2.valid
    assert [e for r in r1.results for e in r.errors] == [e for r in r2.results for e in r.errors]


# ── allocator/margin import-coupling isolation ─────────────────────────────

def test_validator_module_imports_neither_allocate_nor_margin_state():
    """Static-analysis-style check confirming the validator module imports
    neither allocate.py nor margin_state.py, in either direction (XASSET-
    0005 supporting artifact SS7 point 12)."""
    source = (REPO_ROOT / "overlap_model_validator.py").read_text()
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
        assert "overlap_model_validator" not in source


def _imported_module_names(source: str) -> set[str]:
    tree = ast.parse(source)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_validator_module_has_zero_import_coupling_with_functional_doctrine_validator():
    """XASSET-0006 SS A point 3's own determination, made by this filing as
    'the second content authorization exercised': two fully independent
    sibling modules, mirroring etf_classification_validator.py/
    crypto_classification_validator.py's own established precedent -- no
    shared helper module, no import in either direction. Checked via actual
    AST import statements, not a raw substring search -- this module's own
    docstring legitimately *names* functional_doctrine_validator.py in
    prose (explaining scope), which a substring check would misflag."""
    overlap_source = (REPO_ROOT / "overlap_model_validator.py").read_text()
    fd_source = (REPO_ROOT / "functional_doctrine_validator.py").read_text()
    assert "functional_doctrine_validator" not in _imported_module_names(overlap_source)
    assert "overlap_model_validator" not in _imported_module_names(fd_source)


# ── protected-path isolation ─────────────────────────────────────────────

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

    ov.validate_overlap_model_directory(REPO_ROOT / "intelligence" / "overlap_model")

    for rel, before in hashes_before.items():
        assert (REPO_ROOT / rel).read_bytes() == before, f"{rel} was mutated"


def test_protected_intelligence_records_untouched():
    """No pre-existing record under any of these directories is modified,
    renamed, or deleted -- new records (e.g. a future, separately
    authorized WS-0005-successor equity/relationship cohort under
    intelligence/companies|relationships/) are permitted, since these
    directories are not permanently closed. Repaired from a raw `git
    status --porcelain` check (XASSET-0012 bounded correction, MAJOR-1
    item F): the raw form could not distinguish a legitimate future
    addition from an unauthorized modification of existing content and
    would false-fail the moment either directory legitimately grew, the
    same defect class an independent exact-head review found in the
    now-repaired governance/decisions check below."""
    _assert_no_unauthorized_change_since_base([
        "intelligence/etf_classification", "intelligence/crypto_classification",
        "intelligence/classification", "intelligence/companies", "intelligence/themes",
        "intelligence/relationships", "intelligence/functional_doctrine",
    ])


# ── PR-base-relative protected-path checks (additions permitted, existing
#    content must never be modified/renamed/deleted) -- XASSET-0012 bounded
#    correction, MAJOR-1: repairs (not deletes) the governance-decisions
#    protection this file's own PR #292 commit originally added, reusing
#    the base-diff resolution pattern PR #300 already established in
#    test_contender_evaluation_validator.py rather than inventing a new
#    one. A local copy is kept here, not imported cross-file, matching
#    this repository's own established per-file helper convention (each
#    validator's test suite owns its own copy of the constants/helpers it
#    needs). ──────────────────────────────────────────────────────────

def _resolve_pr_base_sha(cwd: Path = REPO_ROOT) -> str | None:
    """Resolve this branch's actual PR base commit from live repository
    truth -- git merge-base HEAD origin/main -- rather than a hard-coded
    SHA that goes stale the moment the branch is rebased or main moves
    forward. Returns None (causing the calling check to skip, not fail)
    if origin/main is not a resolvable ref in this environment, since
    that is an environment precondition this test suite does not manage,
    not a content defect. Deliberately does NOT use local `main`, which
    this repository's own history discloses can diverge from
    `origin/main`. `cwd` defaults to the real repository root but accepts
    any git working directory, exercised directly against synthetic,
    disposable repositories by the behavioral-invariant tests below."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", "origin/main"],
            cwd=cwd, capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    result = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=cwd, capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.strip()


def _blob_at(repo_root: Path, revision: str, relpath: str) -> str | None:
    """The git blob id of ``relpath`` at ``revision``, or None if it is not present there.

    Used to prove a one-use modification allowance against real object identities rather than
    against a path string, so an allowance cannot outlive the exact transition it was granted for.
    """
    result = subprocess.run(
        ["git", "rev-parse", f"{revision}:{relpath}"],
        cwd=repo_root, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def _worktree_blob(repo_root: Path, relpath: str) -> str | None:
    """The git blob id of the file as it exists ON DISK right now.

    The diff this guard reads compares base against the WORKING TREE, so the "new" side of an
    authorized transition must be read from disk too. Reading HEAD instead would let an
    uncommitted rewrite of the allow-listed file pass while HEAD still held the authorized blob --
    the same class of gap as the path-only allowance this replaces.
    """
    result = subprocess.run(
        ["git", "hash-object", "--", relpath],
        cwd=repo_root, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def _assert_no_unauthorized_change_since_base(
    paths: list[str],
    repo_root: Path = REPO_ROOT,
    authorized_modifications: dict[str, dict[str, str]] | None = None,
) -> None:
    """A file that already existed at this PR's base commit must never be
    modified, renamed, copied, type-changed, or deleted between base and
    the current working tree (covering both this PR's own committed
    history and any not-yet-committed local change, so this still
    functions as a local pre-commit check, not merely a post-commit-CI
    one) -- but a file that did NOT exist at base (git diff status `A`,
    added) is always permitted, since authoring new content under these
    directories is the routine, expected, authorized behavior of a
    correctly-scoped future session. Skips (never silently passes as a
    false green) when origin/main is not resolvable in this environment."""
    base_sha = _resolve_pr_base_sha(cwd=repo_root)
    if base_sha is None:
        pytest.skip("origin/main not resolvable in this environment -- cannot compute a true PR-base diff")
    result = subprocess.run(
        ["git", "diff", "--name-status", base_sha, "--", *paths],
        cwd=repo_root, capture_output=True, text=True, check=True,
    )
    allowed = authorized_modifications or {}

    def _is_violation(line: str) -> bool:
        status, _, rest = line.partition("\t")
        if status.startswith("A"):
            return False
        # A rename or copy carries two paths and is NEVER permitted by this allowance, which names
        # one file. ``rest`` therefore has to be exactly one known path to be considered at all.
        transition = allowed.get(rest.strip())
        if transition is None:
            return True
        # MAJOR 2: exact ONE-USE proof. The allowance holds only for this pull request's own base
        # AND only for the single old -> new blob transition it was granted for. Every conjunct is
        # required; any mismatch -- including an unresolvable blob -- is a violation, not a pass.
        if base_sha != transition["base_sha"]:
            return True
        if _blob_at(repo_root, base_sha, rest.strip()) != transition["old_blob"]:
            return True
        if _worktree_blob(repo_root, rest.strip()) != transition["new_blob"]:
            return True
        return False

    violations = [
        line for line in result.stdout.splitlines()
        if line.strip() and _is_violation(line)
    ]
    assert violations == [], (
        f"unauthorized modification/rename/deletion of pre-existing content since base {base_sha}:\n"
        + "\n".join(violations)
    )


#: The ONE pre-existing governance decision a merged, effective authority permits this branch to
#: modify. ``XASSET-0043`` SS-I.2 -- accepted, merged, and in force -- offers the separately
#: authorized rebinding unit a choice of "(a) **amend** ``XASSET-0042``'s declaration ... or
#: (b) **retire** the current-identity role from ``XASSET-0042`` -- re-anchoring its declaration
#: to the closed head range it truthfully describes", and requires the choice to be argued.
#: ``XASSET-0044`` SS-H takes (b) and argues it, so re-anchoring that file's prose is authorized
#: content, not an unauthorized modification.
#:
#: This is deliberately an exact single-path allow-list rather than a relaxed status filter: every
#: other pre-existing decision stays protected exactly as before, and a second modified file --
#: including a different XASSET decision -- still fails. It follows this check's own established
#: repair-not-delete precedent, recorded in the docstring below: a guard correct for one PR's
#: scope, which a later lawfully-broader session outgrows, is narrowed to the real authority
#: rather than removed.
#: MAJOR 2 (review 4986931575): a PATH is not a one-use authority. The allow-list was exact by
#: path but bound to nothing else, so it survived this pull request forever -- reproduced before
#: this correction against a synthetic later PR whose base already contained this rebinding and
#: which rewrote the same decision again: the guard passed. XASSET-0043 SS-I.2 authorizes ONE
#: transition, so the allowance now names that transition exactly: this pull request's own base,
#: the blob that file had AT that base, and the single blob it may become. A later PR has a
#: different base and, at that base, already holds the new blob -- so neither conjunct can hold
#: again and the exception cannot be reused, without deleting, skipping, or relaxing the guard.
AUTHORIZED_DECISION_MODIFICATIONS = {
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md": {
        "base_sha": "0709d2f05ab031ecb6f69c40465ed4a227983aed",
        "old_blob": "e4cda7a5042da68f347598a62d9e6d5cfc40ae55",
        "new_blob": "b08a625a5adb840e9576e5cd9218be24e63bd57e",
    },
}


# ── BLOCKING 1 (review 4989608238): the HISTORICAL proof needs IMMUTABLE anchors ────────
#
# ``test_real_repository_governance_decisions_pass_the_repaired_check`` asserted that the
# one-use allowance above was EXACTLY EXERCISED -- a genuinely valuable property, and the
# reason the allowance cannot linger as dead permission. But it resolved the range it
# measured through ``_resolve_pr_base_sha``, i.e. ``git merge-base(HEAD, origin/main)``.
# That base MOVES. On PR #344's own branch it was ``0709d2f0…`` and the assertion held; on
# merged ``main`` the merge-base of HEAD and origin/main IS the merge commit, so the
# comparison is empty, ``modified == []``, and the assertion fails describing nothing real.
# It could only fail AFTER its own merge, which is why every pre-merge check passed.
#
# The subject of this assertion is HISTORY -- a transition inside a closed, merged pull
# request -- so it is now anchored to that closed range by exact object identity and reads
# no moving reference at all. ``_resolve_pr_base_sha`` is deliberately UNCHANGED and still
# serves ``_assert_no_unauthorized_change_since_base``, whose subject genuinely is "this
# working tree versus this PR's base" and for which a live base is correct.
#
# Repaired under fresh, explicit principal authorization, recorded in ``XASSET-0045``. The
# repair is narrower than the original: every conjunct the old check proved is still
# proved, and the merge's parentage and tree identity are now proved as well.

#: PR #344's base -- the ``XASSET-0043`` merge, and the closed range's first endpoint.
CLOSED_RANGE_BASE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: PR #344's accepted head -- the exact commit its final clean review examined.
CLOSED_RANGE_ACCEPTED_HEAD = "9c2821ab9e0e0dff09f5a03da5a6034775b00750"
#: PR #344's merge commit.
CLOSED_RANGE_MERGE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
CLOSED_RANGE_MERGE_TREE = "bd9ce6694261a7b4fb664a5121d04571f9606924"


def _commit_exists(repo_root: Path, sha: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=repo_root, capture_output=True, text=True,
    ).returncode == 0


def _assert_authorized_decision_transitions_over_closed_range(
    *,
    base_sha: str,
    accepted_head: str,
    merge_sha: str,
    merge_tree: str,
    authorized: dict[str, dict[str, str]] = AUTHORIZED_DECISION_MODIFICATIONS,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Prove the one-use governance-decision allowance over an IMMUTABLE closed range.

    Every anchor is an explicit argument. Nothing here reads ``HEAD``, ``origin/main``,
    ``merge-base``, or any other reference that moves as the repository advances, so the
    property is invariant on the PR branch, on merged ``main`` where ``HEAD == origin/main``,
    and after ``main`` advances further.

    An unresolvable object is a REFUSAL, never a skip -- the caller is responsible for
    deciding whether a genuinely truncated checkout is an environment precondition.

    Returns the list of paths proven modified, so the caller can require the allowance to
    have been exactly exercised rather than carried as dead permission.
    """
    # -- the range and the merge must actually exist -------------------------------------
    for label, sha in (
        ("base", base_sha), ("accepted head", accepted_head), ("merge", merge_sha),
    ):
        assert _commit_exists(repo_root, sha), (
            f"closed-range {label} {sha} is not a resolvable commit in this repository"
        )

    # -- the merge must have exactly two parents, in the correct order -------------------
    parents = subprocess.run(
        ["git", "rev-list", "--parents", "-n", "1", merge_sha],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout.split()
    assert parents[0] == merge_sha, parents
    assert len(parents) == 3, (
        f"merge {merge_sha} must have exactly two parents, found {len(parents) - 1}: {parents[1:]}"
    )
    assert parents[1] == base_sha, (
        f"merge {merge_sha} first parent is {parents[1]}, expected base {base_sha}"
    )
    assert parents[2] == accepted_head, (
        f"merge {merge_sha} second parent is {parents[2]}, expected accepted head {accepted_head}"
    )

    # -- zero merge drift: accepted-head tree and merge tree are byte-identical -----------
    head_tree = subprocess.run(
        ["git", "rev-parse", f"{accepted_head}^{{tree}}"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout.strip()
    real_merge_tree = subprocess.run(
        ["git", "rev-parse", f"{merge_sha}^{{tree}}"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert head_tree == merge_tree, (
        f"accepted-head tree {head_tree} is not the expected {merge_tree}"
    )
    assert real_merge_tree == merge_tree, (
        f"merge tree {real_merge_tree} is not the expected {merge_tree} -- merge drift"
    )

    # -- the closed-range diff itself ----------------------------------------------------
    result = subprocess.run(
        ["git", "diff", "--name-status", base_sha, accepted_head, "--", "governance/decisions"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    )
    modified: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        status, _, rest = line.partition("\t")
        # An ADDITION is always permitted -- authoring a new decision is the routine,
        # expected behavior of a governance-authoring session. Unchanged rule.
        if status.startswith("A"):
            continue
        path = rest.strip()
        transition = authorized.get(path)
        assert transition is not None, (
            f"expected only newly-added or separately-authorized governance decisions, "
            f"found: {line}"
        )
        # A rename or copy carries TWO tab-separated paths, so it can never match a
        # single known path above; a delete or type-change is refused here.
        assert status == "M", (
            f"only a MODIFICATION may be authorized here, never a rename, copy, delete "
            f"or type-change: {line}"
        )
        # The allowance is bound to ONE transition. Each conjunct is independently
        # required, and both ends are read from the CLOSED RANGE -- never the working
        # tree, which is not what a historical proof is about.
        assert transition["base_sha"] == base_sha, (
            f"allowance for {path} is bound to base {transition['base_sha']}, "
            f"not to the range base {base_sha}"
        )
        assert _blob_at(repo_root, base_sha, path) == transition["old_blob"], (
            f"{path} at range base is not the authorized old blob {transition['old_blob']}"
        )
        assert _blob_at(repo_root, accepted_head, path) == transition["new_blob"], (
            f"{path} at range head is not the authorized new blob {transition['new_blob']}"
        )
        modified.append(path)

    # The authorized exception must be genuinely exercised, not carried as dead permission.
    assert modified == list(authorized), (
        f"the authorized modification set is not exactly what the closed range changed: {modified}"
    )
    return modified


def test_governance_decision_files_untouched():
    """No pre-existing governance/decisions/*.md file is modified, renamed,
    or deleted by this PR -- the newly authorized decision file(s) this PR
    itself adds are permitted (git diff status `A`), since authoring a new
    decision is the entire point of a governance-authoring session.
    Repaired (not deleted) from a raw `git status --porcelain -- governance
    /decisions` check originally added by PR #292 (XASSET-0007's own
    content implementation), which was correct for that one PR's own
    zero-governance-touch scope but structurally could not survive any
    future governance-authoring session -- an independent exact-head
    review of XASSET-0012 (pullrequestreview-4902959254, MAJOR finding)
    found the original deletion unjustified and required a repair using
    PR #300's own already-established base-diff resolution pattern
    instead. This corrects XASSET-0012's own earlier, inaccurate claim
    that deletion "matches PR #300's exact class of fix" -- PR #300
    repaired an analogous stale assertion by resolving it dynamically
    against live PR-base state, it did not remove the protection; this
    correction now does the same."""
    _assert_no_unauthorized_change_since_base(
        ["governance/decisions"], authorized_modifications=AUTHORIZED_DECISION_MODIFICATIONS
    )


def _init_synthetic_repo(tmp_path: Path):
    """A minimal, disposable git repository used to prove
    _resolve_pr_base_sha's and _assert_no_unauthorized_change_since_base's
    own behavioral invariants deterministically -- independent of this
    real repository's own PR/merge lifecycle, mirroring
    test_contender_evaluation_validator.py's own identical fixture."""
    def run(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, capture_output=True, text=True, check=True,
        )
    run("init", "-q")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "Test")
    return run


def test_resolve_pr_base_sha_returns_true_divergence_point_on_diverged_branch(tmp_path):
    """When HEAD has diverged from origin/main by one or more new commits
    (an active feature/governance branch), the resolver must return the
    actual common ancestor, never silently compare HEAD to itself."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "file.txt").write_text("base\n")
    run("add", "-A")
    run("commit", "-q", "-m", "base commit")
    base_sha = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", base_sha)

    (tmp_path / "file.txt").write_text("base\nfeature work\n")
    run("add", "-A")
    run("commit", "-q", "-m", "feature-branch commit, diverged from origin/main")
    head_sha = run("rev-parse", "HEAD").stdout.strip()

    resolved = _resolve_pr_base_sha(cwd=tmp_path)
    assert resolved == base_sha
    assert resolved != head_sha


def test_resolve_pr_base_sha_returns_head_when_head_equals_origin_main(tmp_path):
    """When HEAD and origin/main coincide (no divergence -- immediately
    after a PR merges), the resolver may legitimately return that same
    commit, computed dynamically rather than against a fixed SHA."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "file.txt").write_text("content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "sole commit, HEAD and origin/main coincide")
    sole_sha = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", sole_sha)

    resolved = _resolve_pr_base_sha(cwd=tmp_path)
    assert resolved == sole_sha


def test_unauthorized_change_since_base_permits_a_new_file_addition(tmp_path):
    """Adversarial case (MAJOR-1 validation item, and the exact failure
    mode being repaired): a new file added since base under a protected
    directory -- e.g. this PR's own newly authored governance decision --
    must never fail this check."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "protected").mkdir()
    (tmp_path / "protected" / "EXISTING.md").write_text("original content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "base commit")
    base_sha = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", base_sha)

    (tmp_path / "protected" / "NEW-0001.md").write_text("newly authorized content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "add a new, authorized record")

    _assert_no_unauthorized_change_since_base(["protected"], repo_root=tmp_path)  # must not raise


def test_unauthorized_change_since_base_catches_a_synthetic_modification(tmp_path):
    """Adversarial case: a pre-existing file's content is modified since
    base -- must be caught, proving the mechanism itself (not merely
    today's clean real-repository diff) actually detects the violation
    class it exists to prevent."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "protected").mkdir()
    (tmp_path / "protected" / "EXISTING.md").write_text("original content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "base commit")
    base_sha = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", base_sha)

    (tmp_path / "protected" / "EXISTING.md").write_text("silently rewritten content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "unauthorized modification of existing content")

    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(["protected"], repo_root=tmp_path)


def test_unauthorized_change_since_base_catches_a_synthetic_deletion(tmp_path):
    """Adversarial case: a pre-existing file is deleted since base -- must
    also be caught, not just modifications (git diff status `D`, not
    `A`)."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "protected").mkdir()
    (tmp_path / "protected" / "EXISTING.md").write_text("original content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "base commit")
    base_sha = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", base_sha)

    (tmp_path / "protected" / "EXISTING.md").unlink()
    run("add", "-A")
    run("commit", "-q", "-m", "unauthorized deletion of existing content")

    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(["protected"], repo_root=tmp_path)


def test_unauthorized_change_since_base_skips_when_origin_main_unresolvable(tmp_path):
    """No always-pass/blanket-skip masquerading as a real check: a genuine
    environment precondition failure (no origin/main ref at all) must
    produce an explicit pytest.skip, never a silent success."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "file.txt").write_text("content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "sole commit, no origin/main ref configured")

    with pytest.raises(pytest.skip.Exception):
        _assert_no_unauthorized_change_since_base(["file.txt"], repo_root=tmp_path)


def test_real_repository_governance_decisions_pass_the_repaired_check():
    """Real-repository proof (not synthetic) that the one-use governance-decision
    allowance was EXACTLY EXERCISED -- anchored to the immutable closed range of the
    merged PR #344, not to any moving reference.

    Re-anchored under review 4989608238's BLOCKING 1 and fresh explicit principal
    authorization (see ``XASSET-0045``). The property proved is strictly larger than
    before: the closed-range diff, the one-use blob transition at BOTH range endpoints,
    the merge's exact two-parent ordering, and byte-identical accepted-head/merge trees.

    Invariant by construction on the PR branch, on merged ``main`` where
    ``HEAD == origin/main``, and after ``main`` advances -- proved directly by
    ``test_closed_range_proof_is_invariant_to_head_and_origin_main``.
    """
    present = [
        _commit_exists(REPO_ROOT, sha)
        for sha in (CLOSED_RANGE_BASE_SHA, CLOSED_RANGE_ACCEPTED_HEAD, CLOSED_RANGE_MERGE_SHA)
    ]
    if not any(present):
        pytest.skip("PR #344's closed range is not present in this checkout")
    modified = _assert_authorized_decision_transitions_over_closed_range(
        base_sha=CLOSED_RANGE_BASE_SHA,
        accepted_head=CLOSED_RANGE_ACCEPTED_HEAD,
        merge_sha=CLOSED_RANGE_MERGE_SHA,
        merge_tree=CLOSED_RANGE_MERGE_TREE,
    )
    assert modified == list(AUTHORIZED_DECISION_MODIFICATIONS)


def test_the_repaired_check_reads_no_moving_reference():
    """The repair's whole point: neither the historical assertion nor the helper it
    delegates to may consult ``HEAD``, ``origin/main``, or ``merge-base``. Checked over
    the parsed AST rather than by substring scan, so the explanatory comments above --
    which necessarily NAME those references -- cannot make this pass or fail."""
    source = SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for name in (
        "_assert_authorized_decision_transitions_over_closed_range",
        "test_real_repository_governance_decisions_pass_the_repaired_check",
    ):
        node = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == name
        )
        literals = {
            c.value for c in ast.walk(node)
            if isinstance(c, ast.Constant) and isinstance(c.value, str)
        }
        for moving in ("HEAD", "origin/main", "merge-base"):
            assert moving not in literals, f"{name} still consults {moving!r}"
        called = {
            c.func.id for c in ast.walk(node)
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
        }
        assert "_resolve_pr_base_sha" not in called, f"{name} still calls _resolve_pr_base_sha"


def test_resolve_pr_base_sha_is_still_used_by_the_working_tree_guard():
    """The repair removed the moving resolver from the HISTORICAL assertion only. The
    live working-tree guard's subject genuinely is "this working tree versus this PR's
    base", for which a live base is correct -- so the resolver must survive there, not be
    deleted repository-wide."""
    source = SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    node = next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == "_assert_no_unauthorized_change_since_base"
    )
    called = {
        c.func.id for c in ast.walk(node)
        if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
    }
    assert "_resolve_pr_base_sha" in called


# ── the repaired closed-range proof: refusals, and invariance to moving refs ─────────────
#
# Every refusal below drives the REAL helper through its real public signature. The
# synthetic cases build a disposable repository so the diff itself can be controlled
# (status, blob ends, omission, an extra modified decision) -- things the real closed
# range cannot be made to exhibit without rewriting history.


def _synthetic_closed_range(tmp_path: Path, *, second_decision: bool = False):
    """A disposable base -> head -> merge shaped exactly like a real governance PR.

    Returns ``(run, anchors, authorized)`` where ``anchors`` carries the closed range and
    ``authorized`` is the one-use allowance proven over it.
    """
    run = _init_synthetic_repo(tmp_path)
    decisions = tmp_path / "governance" / "decisions"
    decisions.mkdir(parents=True)
    kept = decisions / "KEEP-0001.md"
    kept.write_text("untouched pre-existing decision\n")
    target = decisions / "TARGET-0001.md"
    target.write_text("original\n")
    if second_decision:
        (decisions / "OTHER-0001.md").write_text("another pre-existing decision\n")
    run("add", "-A")
    run("commit", "-q", "-m", "base")
    base = run("rev-parse", "HEAD").stdout.strip()

    target.write_text("authorized rewrite\n")
    if second_decision:
        (decisions / "OTHER-0001.md").write_text("unauthorized rewrite\n")
    (decisions / "NEW-0002.md").write_text("newly authored decision\n")
    run("add", "-A")
    run("commit", "-q", "-m", "head")
    head = run("rev-parse", "HEAD").stdout.strip()

    # A real two-parent merge, built with plumbing so no working tree is disturbed.
    tree = run("rev-parse", f"{head}^{{tree}}").stdout.strip()
    merge = run("commit-tree", tree, "-p", base, "-p", head, "-m", "merge").stdout.strip()

    anchors = {
        "base_sha": base,
        "accepted_head": head,
        "merge_sha": merge,
        "merge_tree": tree,
    }
    authorized = {
        "governance/decisions/TARGET-0001.md": {
            "base_sha": base,
            "old_blob": run("rev-parse", f"{base}:governance/decisions/TARGET-0001.md").stdout.strip(),
            "new_blob": run("rev-parse", f"{head}:governance/decisions/TARGET-0001.md").stdout.strip(),
        },
    }
    return run, anchors, authorized


def _prove(tmp_path: Path, anchors, authorized):
    return _assert_authorized_decision_transitions_over_closed_range(
        authorized=authorized, repo_root=tmp_path, **anchors
    )


def test_synthetic_closed_range_proof_passes_on_a_well_formed_range(tmp_path):
    """The positive control: without it, every refusal below could pass vacuously."""
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    assert _prove(tmp_path, anchors, authorized) == ["governance/decisions/TARGET-0001.md"]


def test_closed_range_proof_refuses_an_unresolvable_object(tmp_path):
    """An unresolvable anchor is a REFUSAL, never a silent skip.

    ``pytest.raises(AssertionError)`` alone is NOT sufficient here: ``pytest.skip`` raises a
    ``BaseException`` subclass, so a helper downgraded from "refuse" to "skip" would mark this
    test SKIPPED and leave the suite green. The skip path is therefore an explicit failure.
    """
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    anchors["accepted_head"] = "0" * 40
    try:
        _prove(tmp_path, anchors, authorized)
    except AssertionError as exc:
        assert "not a resolvable commit" in str(exc)
    except BaseException as exc:  # noqa: BLE001 -- pytest.skip.Exception is a BaseException
        pytest.fail(
            f"an unresolvable anchor must REFUSE, not raise {type(exc).__name__}: {exc}"
        )
    else:
        pytest.fail("an unresolvable anchor was accepted")


def test_closed_range_proof_refuses_a_deletion_of_the_allow_listed_path(tmp_path):
    """The ``status == "M"`` conjunct, reached only for the ALLOW-LISTED path.

    A deletion or rename of any OTHER decision is refused earlier, by the membership check,
    so neither exercises the status rule. Deleting the one allow-listed file is the case that
    does -- and it must still be refused, because an allowance to MODIFY is not an allowance
    to remove.
    """
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    (tmp_path / "governance" / "decisions" / "TARGET-0001.md").unlink()
    run("add", "-A")
    run("commit", "-q", "-m", "delete the allow-listed decision")
    head = run("rev-parse", "HEAD").stdout.strip()
    tree = run("rev-parse", "HEAD^{tree}").stdout.strip()
    anchors = {
        "base_sha": anchors["base_sha"],
        "accepted_head": head,
        "merge_tree": tree,
        "merge_sha": run(
            "commit-tree", tree, "-p", anchors["base_sha"], "-p", head, "-m", "m",
        ).stdout.strip(),
    }
    with pytest.raises(AssertionError, match="only a MODIFICATION may be authorized"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_base_endpoint(tmp_path):
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    anchors["base_sha"] = anchors["accepted_head"]
    with pytest.raises(AssertionError):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_head_endpoint(tmp_path):
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    anchors["accepted_head"] = anchors["base_sha"]
    with pytest.raises(AssertionError):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_second_parent(tmp_path):
    """A merge whose second parent is not the accepted head is refused, even when the
    tree happens to match."""
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    # A DISTINCT decoy commit: git collapses two identical -p arguments into one parent,
    # which would test the parent-count branch instead of the parent-identity branch.
    decoy = run(
        "commit-tree", anchors["merge_tree"], "-p", anchors["base_sha"], "-m", "decoy",
    ).stdout.strip()
    assert decoy != anchors["accepted_head"]
    wrong = run(
        "commit-tree", anchors["merge_tree"],
        "-p", anchors["base_sha"], "-p", decoy, "-m", "wrong second parent",
    ).stdout.strip()
    anchors["merge_sha"] = wrong
    with pytest.raises(AssertionError, match="second parent"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_reversed_parent_order(tmp_path):
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    reversed_merge = run(
        "commit-tree", anchors["merge_tree"],
        "-p", anchors["accepted_head"], "-p", anchors["base_sha"], "-m", "reversed",
    ).stdout.strip()
    anchors["merge_sha"] = reversed_merge
    with pytest.raises(AssertionError, match="first parent"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_parent_count(tmp_path):
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    single = run(
        "commit-tree", anchors["merge_tree"], "-p", anchors["base_sha"], "-m", "one parent",
    ).stdout.strip()
    anchors["merge_sha"] = single
    with pytest.raises(AssertionError, match="exactly two parents"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_merge_tree_drift(tmp_path):
    """A merge that did not carry exactly what was reviewed is refused."""
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    drifted_tree = run("rev-parse", f"{anchors['base_sha']}^{{tree}}").stdout.strip()
    drifted = run(
        "commit-tree", drifted_tree,
        "-p", anchors["base_sha"], "-p", anchors["accepted_head"], "-m", "drifted merge",
    ).stdout.strip()
    anchors["merge_sha"] = drifted
    with pytest.raises(AssertionError, match="merge drift"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_expected_tree(tmp_path):
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    anchors["merge_tree"] = "1" * 40
    with pytest.raises(AssertionError, match="accepted-head tree"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_old_blob(tmp_path):
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    path = "governance/decisions/TARGET-0001.md"
    authorized[path] = {**authorized[path], "old_blob": "2" * 40}
    with pytest.raises(AssertionError, match="authorized old blob"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_wrong_new_blob(tmp_path):
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    path = "governance/decisions/TARGET-0001.md"
    authorized[path] = {**authorized[path], "new_blob": "3" * 40}
    with pytest.raises(AssertionError, match="authorized new blob"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_an_allowance_bound_to_another_base(tmp_path):
    """The one-use binding: an allowance granted for a different base cannot be reused."""
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    path = "governance/decisions/TARGET-0001.md"
    authorized[path] = {**authorized[path], "base_sha": "4" * 40}
    with pytest.raises(AssertionError, match="bound to base"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_deletion(tmp_path):
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    (tmp_path / "governance" / "decisions" / "KEEP-0001.md").unlink()
    run("add", "-A")
    run("commit", "-q", "-m", "delete a pre-existing decision")
    anchors["accepted_head"] = run("rev-parse", "HEAD").stdout.strip()
    anchors["merge_tree"] = run("rev-parse", "HEAD^{tree}").stdout.strip()
    anchors["merge_sha"] = run(
        "commit-tree", anchors["merge_tree"],
        "-p", anchors["base_sha"], "-p", anchors["accepted_head"], "-m", "m",
    ).stdout.strip()
    with pytest.raises(AssertionError, match="newly-added or separately-authorized"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_rename(tmp_path):
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    decisions = tmp_path / "governance" / "decisions"
    (decisions / "KEEP-0001.md").rename(decisions / "KEEP-0001-renamed.md")
    run("add", "-A")
    run("commit", "-q", "-m", "rename a pre-existing decision")
    anchors["accepted_head"] = run("rev-parse", "HEAD").stdout.strip()
    anchors["merge_tree"] = run("rev-parse", "HEAD^{tree}").stdout.strip()
    anchors["merge_sha"] = run(
        "commit-tree", anchors["merge_tree"],
        "-p", anchors["base_sha"], "-p", anchors["accepted_head"], "-m", "m",
    ).stdout.strip()
    with pytest.raises(AssertionError):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_an_extra_modified_decision(tmp_path):
    """A second modified pre-existing decision is never covered by a one-path allowance."""
    _run, anchors, authorized = _synthetic_closed_range(tmp_path, second_decision=True)
    with pytest.raises(AssertionError, match="newly-added or separately-authorized"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_refuses_a_dead_allowance(tmp_path):
    """An allowance the range never exercised is dead permission, and is refused."""
    run, anchors, authorized = _synthetic_closed_range(tmp_path)
    # A range in which TARGET-0001.md is untouched: base -> a head that only ADDS.
    decisions = tmp_path / "governance" / "decisions"
    (decisions / "TARGET-0001.md").write_text("original\n")
    (decisions / "ADDED-0003.md").write_text("only an addition\n")
    run("add", "-A")
    run("commit", "-q", "-m", "addition only, allowance unexercised")
    head = run("rev-parse", "HEAD").stdout.strip()
    tree = run("rev-parse", "HEAD^{tree}").stdout.strip()
    anchors = {
        "base_sha": anchors["base_sha"],
        "accepted_head": head,
        "merge_tree": tree,
        "merge_sha": run(
            "commit-tree", tree, "-p", anchors["base_sha"], "-p", head, "-m", "m",
        ).stdout.strip(),
    }
    with pytest.raises(AssertionError, match="not exactly what the closed range changed"):
        _prove(tmp_path, anchors, authorized)


def test_closed_range_proof_permits_additions(tmp_path):
    """Additions remain treated by the existing rule -- permitted, never counted as a
    modification. The well-formed range already contains one (`NEW-0002.md`)."""
    _run, anchors, authorized = _synthetic_closed_range(tmp_path)
    assert _prove(tmp_path, anchors, authorized) == ["governance/decisions/TARGET-0001.md"]


def _shared_clone(tmp_path: Path) -> Path:
    """An isolated clone with its OWN refs, borrowing this repository's object store.

    Isolation matters: `git worktree` shares the ref namespace, so moving `origin/main`
    inside one would move it for the real repository too.
    """
    dst = tmp_path / "clone"
    result = subprocess.run(
        ["git", "clone", "--quiet", "--shared", "--no-checkout", str(REPO_ROOT), str(dst)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"could not create an isolated clone: {result.stderr.strip()}")
    return dst


@pytest.mark.parametrize("scenario", ["branch", "merged_main", "later_main"])
def test_closed_range_proof_is_invariant_to_head_and_origin_main(tmp_path, scenario):
    """The repaired property must hold identically on the PR branch, on merged ``main``
    where ``HEAD == origin/main`` (the exact condition that broke the old guard), and
    after ``main`` advances beyond the merge.

    Run against a real repository whose ``HEAD`` and ``origin/main`` are genuinely moved,
    in an ISOLATED clone so the real repository's refs are never touched.
    """
    if not _commit_exists(REPO_ROOT, CLOSED_RANGE_MERGE_SHA):
        pytest.skip("PR #344's merge is not present in this checkout")
    clone = _shared_clone(tmp_path)

    def git(*args) -> str:
        return subprocess.run(
            ["git", *args], cwd=clone, capture_output=True, text=True, check=True,
        ).stdout.strip()

    if scenario == "branch":
        head = CLOSED_RANGE_ACCEPTED_HEAD
        main = CLOSED_RANGE_BASE_SHA
    elif scenario == "merged_main":
        head = main = CLOSED_RANGE_MERGE_SHA
    else:
        tree = git("rev-parse", f"{CLOSED_RANGE_MERGE_SHA}^{{tree}}")
        later = subprocess.run(
            ["git", "commit-tree", tree, "-p", CLOSED_RANGE_MERGE_SHA, "-m", "later main"],
            cwd=clone, capture_output=True, text=True, check=True,
            env={**os.environ,
                 "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                 "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
        ).stdout.strip()
        head = main = later

    git("update-ref", "HEAD", head)
    git("update-ref", "refs/remotes/origin/main", main)
    assert git("rev-parse", "HEAD") == head
    assert git("rev-parse", "origin/main") == main
    if scenario != "branch":
        # The exact condition that made the old moving-anchor guard collapse.
        assert git("merge-base", "HEAD", "origin/main") == git("rev-parse", "HEAD")

    modified = _assert_authorized_decision_transitions_over_closed_range(
        base_sha=CLOSED_RANGE_BASE_SHA,
        accepted_head=CLOSED_RANGE_ACCEPTED_HEAD,
        merge_sha=CLOSED_RANGE_MERGE_SHA,
        merge_tree=CLOSED_RANGE_MERGE_TREE,
        repo_root=clone,
    )
    assert modified == list(AUTHORIZED_DECISION_MODIFICATIONS)


def test_the_invariance_scenarios_cover_branch_merged_and_later_main():
    """Coverage pin. Dropping a scenario from the parametrisation would silently stop
    proving the very condition the repair exists for -- merged ``main``, where the old
    guard collapsed -- while the remaining scenarios kept passing."""
    source = SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    node = next(
        n for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.FunctionDef)
        and n.name == "test_closed_range_proof_is_invariant_to_head_and_origin_main"
    )
    scenarios: set[str] = set()
    for decorator in node.decorator_list:
        for arg in getattr(decorator, "args", []):
            if isinstance(arg, (ast.List, ast.Tuple)):
                scenarios |= {
                    e.value for e in arg.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)
                }
    assert scenarios == {"branch", "merged_main", "later_main"}, scenarios


def _live_ref(name: str) -> str | None:
    """The real repository's current value for a ref, or None if unresolvable.

    Deliberately returns whatever the ref happens to be. Nothing in this file may require
    a LIVE ref to equal a HISTORICAL commit: `origin/main` lawfully advances every time a
    pull request merges, including this one.
    """
    result = subprocess.run(
        ["git", "rev-parse", name], cwd=REPO_ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def test_the_invariance_simulation_does_not_mutate_the_real_repository_refs(tmp_path):
    """Isolation, proved as a BEFORE/AFTER invariant rather than a fixed value.

    Superseding ``test_the_real_repository_refs_were_not_disturbed_by_the_invariance_
    simulation``, which asserted ``origin/main == CLOSED_RANGE_MERGE_SHA``. That was true
    only while this branch sat over PR #344's merge: once THIS pull request merges,
    ``origin/main`` lawfully becomes ITS merge, the ref still resolves, and the equality
    fails -- recreating the very merge-CI deadlock the closed-range repair exists to
    remove. Reproduced before correcting, in an isolated successor-merge clone.

    The property actually worth protecting is not the ref's VALUE but that the isolated
    simulation does not TOUCH it. `git worktree` shares the ref namespace, so a simulation
    built that way really would move the real `origin/main`; a clone does not. That is
    what is asserted here, against whatever the refs happen to be.
    """
    before = {name: _live_ref(name) for name in ("HEAD", "origin/main")}
    if before["origin/main"] is None:
        pytest.skip("origin/main not resolvable in this environment")
    if not _commit_exists(REPO_ROOT, CLOSED_RANGE_MERGE_SHA):
        pytest.skip("PR #344's merge is not present in this checkout")

    # Exercise the SAME isolated-simulation code path the invariance test uses, including
    # the ref moves that would be destructive if the isolation were wrong.
    clone = _shared_clone(tmp_path)
    successor = _simulated_successor_merge(clone)
    for ref, value in (("HEAD", successor), ("refs/remotes/origin/main", successor)):
        subprocess.run(
            ["git", "update-ref", ref, value], cwd=clone, capture_output=True, text=True, check=True,
        )
    assert _git_in(clone, "rev-parse", "origin/main") == successor

    after = {name: _live_ref(name) for name in ("HEAD", "origin/main")}
    assert after == before, (
        f"the isolated simulation mutated the real repository's refs: {before} -> {after}"
    )


def _git_in(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _working_clone(tmp_path: Path) -> Path:
    """An isolated clone WITH a working tree, checked out at this branch's content.

    Separate from ``_shared_clone`` (``--no-checkout``): the ref-state regression below
    runs a real nested pytest inside the clone, which needs the files on disk.
    """
    dst = tmp_path / "working-clone"
    result = subprocess.run(
        ["git", "clone", "--quiet", "--shared", str(REPO_ROOT), str(dst)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"could not create an isolated working clone: {result.stderr.strip()}")
    return dst


def _simulated_successor_merge(repo: Path) -> str:
    """A REAL two-parent merge of this branch into PR #344's merge, built with plumbing.

    This is what ``origin/main`` becomes once THIS pull request merges normally.
    """
    head_tree = _git_in(repo, "rev-parse", f"{_LOCAL_HEAD_FOR_SIMULATION}^{{tree}}")
    return subprocess.run(
        ["git", "commit-tree", head_tree,
         "-p", CLOSED_RANGE_MERGE_SHA, "-p", _LOCAL_HEAD_FOR_SIMULATION,
         "-m", "simulated successor merge"],
        cwd=repo, capture_output=True, text=True, check=True,
        env={**os.environ,
             "GIT_AUTHOR_NAME": "sim", "GIT_AUTHOR_EMAIL": "sim@sim",
             "GIT_COMMITTER_NAME": "sim", "GIT_COMMITTER_EMAIL": "sim@sim"},
    ).stdout.strip()


#: This branch's own current commit, resolved live. Used ONLY to build simulated ref
#: states; never asserted to equal anything.
_LOCAL_HEAD_FOR_SIMULATION = _live_ref("HEAD") or CLOSED_RANGE_MERGE_SHA


#: The real-repository tests whose behaviour must not depend on where HEAD or origin/main
#: point. Run as a nested pytest inside an isolated clone under each ref state below.
REF_STATE_SENSITIVE_TESTS = (
    "test_real_repository_governance_decisions_pass_the_repaired_check",
    "test_the_repaired_check_reads_no_moving_reference",
    "test_governance_decision_files_untouched",
    "test_the_invariance_simulation_does_not_mutate_the_real_repository_refs",
)


@pytest.mark.parametrize(
    "ref_state", ["branch", "merged_main_at_pr344", "later_main", "pr345_successor_merge"]
)
def test_relevant_tests_pass_under_every_real_repository_ref_state(tmp_path, ref_state):
    """The regression review 4993351528 required: run the ref-sensitive tests for real,
    under each ref state this branch will actually pass through, and require them to pass.

    The WORKING TREE is always this branch's content -- the tests under examination are
    this PR's own. Only ``HEAD`` and ``origin/main`` move, so ref position is isolated as
    the single variable. ``pr345_successor_merge`` is the state that exposed the defect:
    under the superseded assertion this scenario FAILED, because live ``origin/main`` had
    lawfully advanced past PR #344's merge.
    """
    if not _commit_exists(REPO_ROOT, CLOSED_RANGE_MERGE_SHA):
        pytest.skip("PR #344's merge is not present in this checkout")
    clone = _working_clone(tmp_path)
    _git_in(clone, "checkout", "--quiet", "--detach", _LOCAL_HEAD_FOR_SIMULATION)
    # The suite under examination is THIS working tree's, which during a correction is
    # ahead of the last commit. Copying it in keeps the regression honest about the code
    # actually being reviewed rather than about the previous commit's version.
    shutil.copy2(SUITE_SOURCE_PATH, clone / SUITE_SOURCE_PATH.name)

    if ref_state == "branch":
        head, main = _LOCAL_HEAD_FOR_SIMULATION, CLOSED_RANGE_MERGE_SHA
    elif ref_state == "merged_main_at_pr344":
        head = main = CLOSED_RANGE_MERGE_SHA
    elif ref_state == "later_main":
        tree = _git_in(clone, "rev-parse", f"{CLOSED_RANGE_MERGE_SHA}^{{tree}}")
        head = main = subprocess.run(
            ["git", "commit-tree", tree, "-p", CLOSED_RANGE_MERGE_SHA, "-m", "later main"],
            cwd=clone, capture_output=True, text=True, check=True,
            env={**os.environ,
                 "GIT_AUTHOR_NAME": "sim", "GIT_AUTHOR_EMAIL": "sim@sim",
                 "GIT_COMMITTER_NAME": "sim", "GIT_COMMITTER_EMAIL": "sim@sim"},
        ).stdout.strip()
    else:
        head = main = _simulated_successor_merge(clone)

    # Move the refs WITHOUT touching the working tree, so the files under test stay this
    # branch's own while `git rev-parse` reports the simulated state.
    _git_in(clone, "update-ref", "HEAD", head)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", main)
    assert _git_in(clone, "rev-parse", "HEAD") == head
    assert _git_in(clone, "rev-parse", "origin/main") == main
    if ref_state == "pr345_successor_merge":
        assert main != CLOSED_RANGE_MERGE_SHA, "the successor state must advance past PR #344"

    node_ids = [f"{Path(__file__).name}::{name}" for name in REF_STATE_SENSITIVE_TESTS]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", *node_ids],
        cwd=clone, capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"ref state {ref_state!r} (HEAD={head}, origin/main={main}) broke the "
        f"ref-sensitive tests:\n{result.stdout[-4000:]}\n{result.stderr[-2000:]}"
    )


#: Git subcommands that write refs. A simulation must never run one against the real
#: repository -- `git worktree` shares the ref namespace, so an `update-ref` inside one
#: really does move the REAL `origin/main`. That happened once during this work and had to
#: be repaired; this refuses the shape statically, before any damage.
REF_MUTATING_GIT_SUBCOMMANDS = frozenset(
    {"update-ref", "branch", "reset", "checkout", "worktree"}
)


def real_repo_ref_mutation_offenders(source: str) -> list[str]:
    """Calls in ``source`` that would write a ref in the REAL repository.

    A shared, module-level detector -- not a private helper and not re-implemented inside
    its own proof -- so disabling it makes its self-test fail rather than silently pass.
    """
    # A container constructor is a VOCABULARY declaration, not an invocation -- without
    # this the detector flags its own REF_MUTATING_GIT_SUBCOMMANDS definition.
    containers = {"frozenset", "set", "list", "tuple", "dict"}
    offenders: list[str] = []
    for call in (c for c in ast.walk(ast.parse(source)) if isinstance(c, ast.Call)):
        if isinstance(call.func, ast.Name) and call.func.id in containers:
            continue
        literals = {
            a.value for a in ast.walk(call)
            if isinstance(a, ast.Constant) and isinstance(a.value, str)
        }
        if "worktree" in literals:
            offenders.append(f"worktree created at line {call.lineno}")
            continue
        if not (literals & REF_MUTATING_GIT_SUBCOMMANDS):
            continue
        # "Targets the real repository" covers both call shapes used in this file:
        # ``subprocess.run(..., cwd=REPO_ROOT)`` and ``_git_in(REPO_ROOT, ...)``.
        targets_real_repo = any(
            kw.arg == "cwd" and isinstance(kw.value, ast.Name) and kw.value.id == "REPO_ROOT"
            for kw in call.keywords
        ) or (
            bool(call.args)
            and isinstance(call.args[0], ast.Name)
            and call.args[0].id == "REPO_ROOT"
        )
        if targets_real_repo:
            offenders.append(f"ref-mutating git call against REPO_ROOT at line {call.lineno}")
    return offenders


def live_ref_frozen_comparison_offenders(source: str) -> list[str]:
    """Functions in ``source`` that compare a LIVE ref to a frozen historical constant.

    "Resolves a LIVE ref" means, precisely: the function calls ``_live_ref``, or runs a
    ``rev-parse`` with ``cwd=REPO_ROOT``. Merely naming ``REPO_ROOT`` is not enough -- the
    ref-state regression legitimately names the frozen constants while resolving refs only
    inside an isolated clone, and must not be flagged.

    Shared and module-level for the same reason as above.
    """
    frozen = {
        "CLOSED_RANGE_BASE_SHA", "CLOSED_RANGE_ACCEPTED_HEAD",
        "CLOSED_RANGE_MERGE_SHA", "CLOSED_RANGE_MERGE_TREE",
    }
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef):
            continue
        resolves_live_ref = False
        for call in (c for c in ast.walk(node) if isinstance(c, ast.Call)):
            if isinstance(call.func, ast.Name) and call.func.id == "_live_ref":
                resolves_live_ref = True
                break
            call_literals = {
                a.value for a in ast.walk(call)
                if isinstance(a, ast.Constant) and isinstance(a.value, str)
            }
            if "rev-parse" in call_literals and any(
                kw.arg == "cwd" and isinstance(kw.value, ast.Name) and kw.value.id == "REPO_ROOT"
                for kw in call.keywords
            ):
                resolves_live_ref = True
                break
        if not resolves_live_ref:
            continue
        for compare in (c for c in ast.walk(node) if isinstance(c, ast.Compare)):
            operands = [compare.left, *compare.comparators]
            if any(isinstance(o, ast.Name) and o.id in frozen for o in operands):
                offenders.append(f"{node.name}:{compare.lineno}")
    return offenders


def test_no_simulation_writes_a_ref_in_the_real_repository():
    assert real_repo_ref_mutation_offenders(
        SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    ) == []


def test_the_ref_mutation_detector_actually_detects(tmp_path):
    """Falsifiability proof, run through the REAL detector.

    Without this, neutering the detector (emptying its subcommand set, or making its loop
    unreachable) leaves a guard that reports "clean" because it inspects nothing.
    """
    bad_worktree = 'subprocess.run(["git", "worktree", "add", d], cwd=other)'
    bad_update = 'subprocess.run(["git", "update-ref", "HEAD", x], cwd=REPO_ROOT)'
    bad_positional = '_git_in(REPO_ROOT, "update-ref", "refs/remotes/origin/main", x)'
    clean_kw = 'subprocess.run(["git", "update-ref", "HEAD", x], cwd=clone)'
    clean_positional = '_git_in(clone, "update-ref", "refs/remotes/origin/main", x)'
    vocabulary_only = 'frozenset({"update-ref", "worktree"})'
    assert real_repo_ref_mutation_offenders(bad_worktree) != []
    assert real_repo_ref_mutation_offenders(bad_update) != []
    assert real_repo_ref_mutation_offenders(bad_positional) != []
    assert real_repo_ref_mutation_offenders(clean_kw) == []
    assert real_repo_ref_mutation_offenders(clean_positional) == []
    assert real_repo_ref_mutation_offenders(vocabulary_only) == []
    # And it genuinely parsed this suite's own real source, rather than something empty.
    source = SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    assert len([c for c in ast.walk(ast.parse(source)) if isinstance(c, ast.Call)]) > 200


def test_no_test_requires_a_live_ref_to_equal_a_historical_commit():
    """Mutation pin for the defect class itself.

    A function that resolves a LIVE ref against the real repository may not compare that
    result to any frozen closed-range constant. That is what the superseded assertion did,
    and it is what makes a test pass before a merge and fail after it.
    """
    assert live_ref_frozen_comparison_offenders(
        SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    ) == []


def test_the_live_ref_comparison_detector_actually_detects():
    """Falsifiability proof, run through the REAL detector -- the superseded assertion's
    own shape must be flagged, and the legitimate isolated-clone shape must not."""
    offending = (
        "def bad():\n"
        "    r = subprocess.run(['git', 'rev-parse', 'origin/main'], cwd=REPO_ROOT)\n"
        "    assert r.stdout.strip() == CLOSED_RANGE_MERGE_SHA\n"
    )
    via_helper = (
        "def bad2():\n"
        "    assert _live_ref('origin/main') == CLOSED_RANGE_MERGE_SHA\n"
    )
    legitimate = (
        "def fine():\n"
        "    m = _git_in(clone, 'rev-parse', 'origin/main')\n"
        "    assert m != CLOSED_RANGE_MERGE_SHA\n"
    )
    assert live_ref_frozen_comparison_offenders(offending) != []
    assert live_ref_frozen_comparison_offenders(via_helper) != []
    assert live_ref_frozen_comparison_offenders(legitimate) == []


def test_the_ref_state_regression_covers_every_state_this_branch_will_pass_through():
    """Coverage pin. Dropping ``pr345_successor_merge`` would silently stop proving the
    exact state in which the superseded assertion failed."""
    source = SUITE_SOURCE_PATH.read_text(encoding="utf-8")
    node = next(
        n for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.FunctionDef)
        and n.name == "test_relevant_tests_pass_under_every_real_repository_ref_state"
    )
    states: set[str] = set()
    for decorator in node.decorator_list:
        for arg in getattr(decorator, "args", []):
            if isinstance(arg, (ast.List, ast.Tuple)):
                states |= {
                    e.value for e in arg.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)
                }
    assert states == {
        "branch", "merged_main_at_pr344", "later_main", "pr345_successor_merge"
    }, states
    # The successor state must be REQUIRED to advance past PR #344's merge, or it silently
    # degrades into a second copy of the pre-merge state.
    advances = [
        c for c in ast.walk(node)
        if isinstance(c, ast.Compare)
        and any(isinstance(op, ast.NotEq) for op in c.ops)
        and any(
            isinstance(o, ast.Name) and o.id == "CLOSED_RANGE_MERGE_SHA"
            for o in [c.left, *c.comparators]
        )
    ]
    assert advances, "nothing requires the successor ref state to advance past PR #344"


def test_this_suites_new_ref_state_assertions_are_not_vacuous():
    """No ``assert ... or True``-style disjunct and no bare truthy constant may hide a
    disabled guard anywhere in this file. Checked over the parsed AST, not by substring
    scan -- a text search would flag the comments that explain the rule."""
    tree = ast.parse(SUITE_SOURCE_PATH.read_text(encoding="utf-8"))
    asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert len(asserts) > 150, len(asserts)
    for node in asserts:
        test = node.test
        if isinstance(test, ast.Constant):
            pytest.fail(f"bare constant assertion at line {node.lineno}")
        if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
            for value in test.values:
                if isinstance(value, ast.Constant) and bool(value.value):
                    pytest.fail(f"constant-truthy disjunct at line {node.lineno}")


# ── no dimension_type / source_mechanism confusion between mechanical and
#    interface_placeholder dimensions ────────────────────────────────────

def test_source_mechanism_canonical_sets_are_disjoint_per_dimension_where_expected():
    """Sanity check on the module's own constants -- issuer_overlap and
    sleeve_concentration cite genuinely different mechanisms."""
    assert ov._CANONICAL_SOURCE_MECHANISMS[ov.ISSUER_OVERLAP_ETF_LOOKTHROUGH] != ov._CANONICAL_SOURCE_MECHANISMS[ov.SLEEVE_CONCENTRATION]


def test_all_ten_dimensions_have_a_canonical_source_mechanism_entry():
    assert set(ov._CANONICAL_SOURCE_MECHANISMS) == ov.AUTHORIZED_POPULATION


def test_dimension_type_by_id_covers_exactly_the_population():
    assert set(ov._DIMENSION_TYPE_BY_ID) == ov.AUTHORIZED_POPULATION


def test_interface_placeholder_and_mechanical_or_narrative_partition_the_population():
    assert ov.INTERFACE_PLACEHOLDER_DIMENSIONS | ov._MECHANICAL_OR_NARRATIVE_DIMENSIONS == ov.AUTHORIZED_POPULATION
    assert ov.INTERFACE_PLACEHOLDER_DIMENSIONS & ov._MECHANICAL_OR_NARRATIVE_DIMENSIONS == frozenset()
    assert len(ov.INTERFACE_PLACEHOLDER_DIMENSIONS) == 4
    assert len(ov._MECHANICAL_OR_NARRATIVE_DIMENSIONS) == 6


# ── real repository directory scan ───────────────────────────────────────

def test_real_repository_overlap_model_directory_all_valid():
    result = ov.validate_overlap_model_directory(REPO_ROOT / "intelligence" / "overlap_model")
    assert result.valid, [e for r in result.results for e in r.errors if not r.valid]


def test_real_repository_overlap_model_directory_has_exactly_ten_records():
    result = ov.validate_overlap_model_directory(REPO_ROOT / "intelligence" / "overlap_model")
    # 10 per-record results + 1 manifest result + (no combined-scan failure
    # entry appended, since the real corpus is clean).
    record_results = [r for r in result.results if r.source and r.source.endswith(".yaml") and "COHORT_MANIFEST" not in r.source]
    assert len(record_results) == 10


def test_real_repository_every_authorized_dimension_present_and_sealed():
    directory = REPO_ROOT / "intelligence" / "overlap_model"
    present = set()
    for dimension_id in ov.AUTHORIZED_POPULATION:
        path = directory / f"{dimension_id}.yaml"
        assert path.is_file(), f"{dimension_id}.yaml missing from the real repository"
        data = yaml.safe_load(path.read_text())
        assert data["dimension_id"] == dimension_id
        assert data["record_status"] == "sealed"
        present.add(dimension_id)
    assert present == ov.AUTHORIZED_POPULATION


def test_real_repository_four_interface_placeholder_dimensions_forced_correctly():
    directory = REPO_ROOT / "intelligence" / "overlap_model"
    for dimension_id in ov.INTERFACE_PLACEHOLDER_DIMENSIONS:
        data = yaml.safe_load((directory / f"{dimension_id}.yaml").read_text())
        assert data["computation_status"] == ov._NOT_YET_COMPUTABLE_INTERFACE_ONLY
        assert data["dimension_type"] == ov._INTERFACE_PLACEHOLDER


def test_real_repository_six_mechanical_or_narrative_dimensions_not_forced():
    directory = REPO_ROOT / "intelligence" / "overlap_model"
    for dimension_id in ov._MECHANICAL_OR_NARRATIVE_DIMENSIONS:
        data = yaml.safe_load((directory / f"{dimension_id}.yaml").read_text())
        assert data["computation_status"] != ov._NOT_YET_COMPUTABLE_INTERFACE_ONLY
        assert data["dimension_type"] in (ov._MECHANICAL_ROLLUP, ov._NARRATIVE_EVIDENCE)


def test_real_repository_no_numeric_field_anywhere():
    """Independent structural re-scan of the real sealed corpus for any
    bare int/float value anywhere in the document tree -- this design
    carries zero numeric fields, with no carve-out of any kind."""
    directory = REPO_ROOT / "intelligence" / "overlap_model"

    def _walk(value):
        if isinstance(value, dict):
            for v in value.values():
                yield from _walk(v)
        elif isinstance(value, list):
            for v in value:
                yield from _walk(v)
        else:
            yield value

    for dimension_id in ov.AUTHORIZED_POPULATION:
        data = yaml.safe_load((directory / f"{dimension_id}.yaml").read_text())
        for value in _walk(data):
            assert not isinstance(value, (int, float)) or isinstance(value, bool), (
                f"{dimension_id}.yaml carries a bare numeric value {value!r} -- zero numeric "
                f"fields are permitted on this schema, with no carve-out"
            )


def test_real_repository_defensive_offset_interface_cites_gld_but_stays_forced():
    """The specific, explicitly-disclosed scenario XASSET-0007 SS A point 2
    names: GLD_DEFENSIVE_ROLE.yaml now exists and is sealed, but this
    dimension's own forced computation_status is unconditional on that
    fact."""
    directory = REPO_ROOT / "intelligence" / "overlap_model"
    data = yaml.safe_load((directory / "defensive_offset_interface.yaml").read_text())
    assert data["computation_status"] == ov._NOT_YET_COMPUTABLE_INTERFACE_ONLY
    assert any("GLD_DEFENSIVE_ROLE" in ref for ref in data["evidence_or_source_refs"])


def test_real_repository_manifest_reconciles_bidirectionally():
    directory = REPO_ROOT / "intelligence" / "overlap_model"
    manifest = yaml.safe_load((directory / "COHORT_MANIFEST.yaml").read_text())
    manifest_ids = {row["dimension_id"] for row in manifest["cohort"]}
    assert manifest_ids == ov.AUTHORIZED_POPULATION
    for row in manifest["cohort"]:
        record = yaml.safe_load((directory / f"{row['dimension_id']}.yaml").read_text())
        assert row["content_sha256"] == record["content_sha256"]
        assert row["content_sha256"] == ov.canonical_record_hash(record)


# =============================================================================================
# MAJOR 2 (independent FULL review 4986931575): the one-use allowance must EXPIRE.
#
# Reproduced before correcting: a synthetic later PR whose base already contained this rebinding,
# and which rewrote the same XASSET-0042 decision again, PASSED -- turning a one-transition
# authority into standing permission. These prove it cannot happen again, without deleting,
# skipping, xfailing, or broadly relaxing the guard.
# =============================================================================================


def _repo_with_decision(tmp_path: Path, content: str):
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "governance/decisions").mkdir(parents=True)
    (tmp_path / _ALLOWED_DECISION_PATH).write_text(content)
    run("add", "-A")
    run("commit", "-q", "-m", "base")
    base = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", base)
    return run, base


_ALLOWED_DECISION_PATH = (
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md"
)


def test_the_decision_allowance_names_an_exact_one_use_transition():
    """Not a path. A base, an old blob, and the single new blob it may become."""
    assert set(AUTHORIZED_DECISION_MODIFICATIONS) == {_ALLOWED_DECISION_PATH}
    transition = AUTHORIZED_DECISION_MODIFICATIONS[_ALLOWED_DECISION_PATH]
    assert set(transition) == {"base_sha", "old_blob", "new_blob"}
    assert transition["base_sha"] == "0709d2f05ab031ecb6f69c40465ed4a227983aed"
    assert transition["old_blob"] != transition["new_blob"]


def test_the_allowance_matches_this_pull_requests_real_objects():
    """Independently re-derived from the object store, not asserted."""
    transition = AUTHORIZED_DECISION_MODIFICATIONS[_ALLOWED_DECISION_PATH]
    assert _blob_at(REPO_ROOT, transition["base_sha"], _ALLOWED_DECISION_PATH) == transition["old_blob"]
    assert _worktree_blob(REPO_ROOT, _ALLOWED_DECISION_PATH) == transition["new_blob"]


def test_a_later_pr_modifying_the_same_decision_is_refused(tmp_path):
    """THE finding. A future base already carries the new content, so the allowance is spent."""
    run, base = _repo_with_decision(tmp_path, "content as this rebinding left it\n")
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("rewritten by an unrelated later PR\n")
    run("add", "-A")
    run("commit", "-q", "-m", "later PR rewrites the same decision again")
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path,
            authorized_modifications=AUTHORIZED_DECISION_MODIFICATIONS,
        )


def test_a_wrong_base_alone_refuses_even_with_matching_blobs(tmp_path):
    """Each conjunct is independently required: the base must be THIS pull request's own."""
    run, base = _repo_with_decision(tmp_path, "anything\n")
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("changed\n")
    run("add", "-A")
    run("commit", "-q", "-m", "modify")
    forged = {
        _ALLOWED_DECISION_PATH: {
            "base_sha": base,  # the synthetic base, NOT the bound one
            "old_blob": _blob_at(tmp_path, base, _ALLOWED_DECISION_PATH),
            "new_blob": _worktree_blob(tmp_path, _ALLOWED_DECISION_PATH),
        }
    }
    # With the transition's own base, blobs matching, it is permitted...
    _assert_no_unauthorized_change_since_base(
        ["governance/decisions"], repo_root=tmp_path, authorized_modifications=forged,
    )
    # ...and with any other base recorded, it is refused, blobs notwithstanding.
    wrong_base = dict(forged[_ALLOWED_DECISION_PATH], base_sha="0" * 40)
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path,
            authorized_modifications={_ALLOWED_DECISION_PATH: wrong_base},
        )


def test_a_different_new_blob_at_the_right_base_is_refused(tmp_path):
    """The allowance permits ONE destination, not any edit of the allow-listed path."""
    run, base = _repo_with_decision(tmp_path, "original\n")
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("some OTHER destination\n")
    run("add", "-A")
    run("commit", "-q", "-m", "modify to an unauthorized destination")
    transition = {
        _ALLOWED_DECISION_PATH: {
            "base_sha": base,
            "old_blob": _blob_at(tmp_path, base, _ALLOWED_DECISION_PATH),
            "new_blob": "0" * 40,  # the authorized destination, which this is not
        }
    }
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path, authorized_modifications=transition,
        )


def test_an_uncommitted_rewrite_of_the_allow_listed_path_is_refused(tmp_path):
    """The diff reads the WORKING TREE, so the new side must be read from disk. Reading HEAD
    instead would let an uncommitted rewrite pass while HEAD still held the authorized blob."""
    run, base = _repo_with_decision(tmp_path, "original\n")
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("authorized destination\n")
    run("add", "-A")
    run("commit", "-q", "-m", "the authorized modification")
    transition = {
        _ALLOWED_DECISION_PATH: {
            "base_sha": base,
            "old_blob": _blob_at(tmp_path, base, _ALLOWED_DECISION_PATH),
            "new_blob": _worktree_blob(tmp_path, _ALLOWED_DECISION_PATH),
        }
    }
    _assert_no_unauthorized_change_since_base(
        ["governance/decisions"], repo_root=tmp_path, authorized_modifications=transition,
    )
    # Now rewrite it on disk only, leaving HEAD holding the authorized blob.
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("smuggled, uncommitted\n")
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path, authorized_modifications=transition,
        )


def test_a_second_decision_file_is_still_refused(tmp_path):
    """The allowance names one file. Another pre-existing decision stays protected."""
    run, base = _repo_with_decision(tmp_path, "original\n")
    other = "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
    (tmp_path / other).write_text("pre-existing\n")
    run("add", "-A")
    run("commit", "-q", "-m", "second decision at base")
    base2 = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", base2)
    (tmp_path / other).write_text("rewritten\n")
    run("add", "-A")
    run("commit", "-q", "-m", "rewrite the OTHER decision")
    transition = {
        _ALLOWED_DECISION_PATH: {
            "base_sha": base2,
            "old_blob": _blob_at(tmp_path, base2, _ALLOWED_DECISION_PATH),
            "new_blob": _worktree_blob(tmp_path, _ALLOWED_DECISION_PATH),
        }
    }
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path, authorized_modifications=transition,
        )


def test_a_wrong_old_blob_at_the_right_base_is_refused(tmp_path):
    """Mutation C17. Each conjunct is INDEPENDENTLY required: even with the correct base and the
    correct destination blob, an allowance whose recorded old blob is not what the file actually
    held at that base is refused. Without this the allowance would survive any future base whose
    content happened to differ, which is exactly the reusability being closed."""
    run, base = _repo_with_decision(tmp_path, "original\n")
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("authorized destination\n")
    run("add", "-A")
    run("commit", "-q", "-m", "the authorized modification")
    real_old = _blob_at(tmp_path, base, _ALLOWED_DECISION_PATH)
    real_new = _worktree_blob(tmp_path, _ALLOWED_DECISION_PATH)
    # Correct base, correct destination -> permitted.
    _assert_no_unauthorized_change_since_base(
        ["governance/decisions"], repo_root=tmp_path,
        authorized_modifications={
            _ALLOWED_DECISION_PATH: {
                "base_sha": base, "old_blob": real_old, "new_blob": real_new,
            }
        },
    )
    # Same base, same destination, WRONG recorded starting point -> refused.
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path,
            authorized_modifications={
                _ALLOWED_DECISION_PATH: {
                    "base_sha": base, "old_blob": "0" * 40, "new_blob": real_new,
                }
            },
        )


def test_an_unresolvable_blob_on_either_side_is_refused(tmp_path):
    """An allowance that cannot be PROVEN is refused, never passed. This covers the case where a
    recorded object simply is not resolvable in the repository being checked."""
    run, base = _repo_with_decision(tmp_path, "original\n")
    (tmp_path / _ALLOWED_DECISION_PATH).write_text("destination\n")
    run("add", "-A")
    run("commit", "-q", "-m", "modify")
    assert _blob_at(tmp_path, base, "governance/decisions/DOES-NOT-EXIST.md") is None
    with pytest.raises(AssertionError, match="unauthorized modification"):
        _assert_no_unauthorized_change_since_base(
            ["governance/decisions"], repo_root=tmp_path,
            authorized_modifications={
                _ALLOWED_DECISION_PATH: {
                    "base_sha": base,
                    "old_blob": None,      # unresolvable / unrecorded
                    "new_blob": _worktree_blob(tmp_path, _ALLOWED_DECISION_PATH),
                }
            },
        )
