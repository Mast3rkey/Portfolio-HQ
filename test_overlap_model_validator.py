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
import subprocess
from pathlib import Path

import pytest
import yaml

import overlap_model_validator as ov

REPO_ROOT = Path(__file__).resolve().parent


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
    """Zero diff on every existing intelligence/classification|companies|
    themes|relationships|etf_classification|crypto_classification|
    functional_doctrine/ record and COHORT_MANIFEST.yaml -- checked via a
    live git status, not merely a file-content snapshot, so a
    staged-but-uncommitted change would also be caught."""
    result = subprocess.run(
        [
            "git", "status", "--porcelain", "--",
            "intelligence/etf_classification", "intelligence/crypto_classification",
            "intelligence/classification", "intelligence/companies", "intelligence/themes",
            "intelligence/relationships", "intelligence/functional_doctrine",
        ],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert result.stdout.strip() == "", f"unexpected changes under protected intelligence paths:\n{result.stdout}"


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
