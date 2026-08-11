"""Tests for contender_evaluation_validator.py (WS-0014 VRT/WMT
contender-competition pilot schema, CONTENDER-0003 scope).

Every schema/behavior test below constructs its own synthetic fixture --
no real record's judgment content is asserted against except the small,
explicitly-labeled real-repository directory-scan section near the
bottom, which exercises the two real sealed records (VRT, WMT) authored
under this implementation PR.

No third contender, no additional-equity/ETF/crypto/functional-doctrine/
overlap-model content, and no capital-priority conclusion is ever
constructed by any fixture in this file -- CONTENDER-0003's own SS G
boundary is a governing constraint on this test suite's own content, not
merely on the module under test.
"""

from __future__ import annotations

import ast
import copy
import subprocess
from pathlib import Path

import pytest
import yaml

import contender_evaluation_validator as cev

REPO_ROOT = Path(__file__).resolve().parent


# ── fixtures ─────────────────────────────────────────────────────────────

def _provenance(*, n: int = 1) -> dict:
    sources = []
    for i in range(n):
        sources.append({
            "source_identifier": f"intelligence/companies/SYNTH{i}.yaml",
            "source_type": "secondary",
            "as_of_date": "2026-07-26",
            "access_status": "directly_inspected",
        })
    return {"sources": sources}


def _structural_reference(ticker: str) -> dict:
    comparator = cev.AUTHORIZED_COMPARATOR_MAP[ticker]
    path = REPO_ROOT / cev._VALUATION_ARCHETYPE_DIR / f"{comparator}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    from valuation_archetype_validator import canonical_record_hash as archetype_hash
    return {
        "source_schema": "valuation_archetype",
        "source_file": f"{cev._VALUATION_ARCHETYPE_DIR}/{comparator}.yaml",
        "referenced_content_sha256": archetype_hash(data),
    }


def _archetype_assessment(*, primary: str = "B", secondary: str | None = None) -> dict:
    return {
        "primary_archetype": primary,
        "secondary_archetype": secondary,
        "rationale": "Synthetic rationale describing a reinvestment-intensive industrial model.",
    }


def _evidence_quality_assessment(*, coverage: str = "partial") -> dict:
    return {
        "primary_source_coverage": coverage,
        "uncertainty_statement": "Synthetic uncertainty statement noting an unresolved item.",
    }


def _methodology_applicability_reference(archetype: str = "B") -> dict:
    from valuation_result_validator import governed_role_for
    ref = {"archetype": archetype}
    for family_id in cev._FAMILY_IDS:
        ref[family_id] = governed_role_for(family_id, archetype)
    return ref


def _evidence_parity_finding(*, finding: str = "comparable_evidence_depth") -> dict:
    return {
        "finding": finding,
        "rationale": "Synthetic rationale comparing evidence completeness only.",
    }


def _valid_record(ticker: str = "VRT", **overrides) -> dict:
    comparator = cev.AUTHORIZED_COMPARATOR_MAP[ticker]
    archetype = "B" if ticker == "VRT" else "G"
    data = {
        "schema_version": cev.SCHEMA_VERSION,
        "contender_symbol": ticker,
        "canonical_comparator_symbol": comparator,
        "provenance": _provenance(),
        "comparator_structural_reference": _structural_reference(ticker),
        "archetype_assessment": _archetype_assessment(primary=archetype),
        "evidence_quality_assessment": _evidence_quality_assessment(),
        "methodology_applicability_reference": _methodology_applicability_reference(archetype),
        "evidence_parity_finding": _evidence_parity_finding(),
        "abstention_index": [],
        "lifecycle_status": "sealed",
        "sealed_at": "2026-08-10T23:00:00Z",
        "governing_decisions": ["CONTENDER-0003"],
        "drafting_session_or_shard_id": "test-shard",
        "cohort_manifest_entry": f"intelligence/contender_evaluation/COHORT_MANIFEST.yaml#{ticker}",
        "content_sha256": "placeholder",
    }
    data.update(overrides)
    data["content_sha256"] = cev.canonical_record_hash(data)
    return data


def _sealed(data: dict) -> dict:
    """Recompute content_sha256 after a mutation, so the fixture stays
    internally consistent unless a test explicitly wants a stale hash."""
    out = copy.deepcopy(data)
    out["content_sha256"] = cev.canonical_record_hash(out)
    return out


# ── valid baseline ───────────────────────────────────────────────────────

def test_valid_vrt_record_passes():
    errors = cev.validate_contender_evaluation_data(_valid_record("VRT"), expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []


def test_valid_wmt_record_passes():
    errors = cev.validate_contender_evaluation_data(_valid_record("WMT"), expected_ticker="WMT", repo_root=REPO_ROOT)
    assert errors == []


# ── population: exactly {VRT, WMT} ──────────────────────────────────────

def test_third_ticker_rejected():
    data = _valid_record("VRT")
    data["contender_symbol"] = "NVDA"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="NVDA", repo_root=REPO_ROOT)
    assert any("not in the CONTENDER-0003-authorized population" in e for e in errors)


def test_arbitrary_non_authorized_ticker_rejected():
    data = _valid_record("VRT")
    data["contender_symbol"] = "SNDK"
    data["canonical_comparator_symbol"] = "GEV"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="SNDK", repo_root=REPO_ROOT)
    assert any("not in the CONTENDER-0003-authorized population" in e for e in errors)


def test_authorized_population_constant_is_exactly_vrt_wmt():
    assert cev.AUTHORIZED_POPULATION == frozenset({"VRT", "WMT"})


def test_manifest_missing_ticker_rejected(tmp_path):
    records_dir = tmp_path / "contender_evaluation"
    records_dir.mkdir()
    vrt = _valid_record("VRT")
    (records_dir / "VRT.yaml").write_text(yaml.safe_dump(vrt), encoding="utf-8")
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "CONTENDER-0003",
        "cohort": [{
            "contender_symbol": "VRT", "canonical_comparator_symbol": "GEV",
            "shard_id": "s", "sealed_at": "2026-08-10T23:00:00Z",
            "content_sha256": vrt["content_sha256"], "schema_version": "1.0",
            "governing_decision": "CONTENDER-0003",
            "record_path": "intelligence/contender_evaluation/VRT.yaml",
        }],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = cev.validate_cohort_manifest(records_dir / "COHORT_MANIFEST.yaml", records_dir)
    assert not result.valid
    assert any("missing authorized ticker" in e for e in result.errors)


def test_manifest_extra_ticker_rejected(tmp_path):
    records_dir = tmp_path / "contender_evaluation"
    records_dir.mkdir()
    rows = []
    for ticker in ("VRT", "WMT"):
        rec = _valid_record(ticker)
        (records_dir / f"{ticker}.yaml").write_text(yaml.safe_dump(rec), encoding="utf-8")
        rows.append({
            "contender_symbol": ticker, "canonical_comparator_symbol": cev.AUTHORIZED_COMPARATOR_MAP[ticker],
            "shard_id": "s", "sealed_at": "2026-08-10T23:00:00Z",
            "content_sha256": rec["content_sha256"], "schema_version": "1.0",
            "governing_decision": "CONTENDER-0003",
            "record_path": f"intelligence/contender_evaluation/{ticker}.yaml",
        })
    # a third, unauthorized row referencing a nonexistent file
    rows.append({
        "contender_symbol": "SNDK", "canonical_comparator_symbol": "WDC",
        "shard_id": "s", "sealed_at": "2026-08-10T23:00:00Z",
        "content_sha256": "0" * 64, "schema_version": "1.0",
        "governing_decision": "CONTENDER-0003",
        "record_path": "intelligence/contender_evaluation/SNDK.yaml",
    })
    manifest = {"schema_version": "1.0", "governing_decision": "CONTENDER-0003", "cohort": rows}
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = cev.validate_cohort_manifest(records_dir / "COHORT_MANIFEST.yaml", records_dir)
    assert not result.valid
    assert any("non-authorized ticker" in e for e in result.errors)


def test_manifest_duplicate_ticker_rejected(tmp_path):
    records_dir = tmp_path / "contender_evaluation"
    records_dir.mkdir()
    vrt = _valid_record("VRT")
    wmt = _valid_record("WMT")
    (records_dir / "VRT.yaml").write_text(yaml.safe_dump(vrt), encoding="utf-8")
    (records_dir / "WMT.yaml").write_text(yaml.safe_dump(wmt), encoding="utf-8")
    row = lambda t, rec: {
        "contender_symbol": t, "canonical_comparator_symbol": cev.AUTHORIZED_COMPARATOR_MAP[t],
        "shard_id": "s", "sealed_at": "2026-08-10T23:00:00Z",
        "content_sha256": rec["content_sha256"], "schema_version": "1.0",
        "governing_decision": "CONTENDER-0003",
        "record_path": f"intelligence/contender_evaluation/{t}.yaml",
    }
    manifest = {
        "schema_version": "1.0", "governing_decision": "CONTENDER-0003",
        "cohort": [row("VRT", vrt), row("VRT", vrt), row("WMT", wmt)],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = cev.validate_cohort_manifest(records_dir / "COHORT_MANIFEST.yaml", records_dir)
    assert not result.valid
    assert any("duplicate contender_symbol" in e for e in result.errors)


def test_orphan_sealed_record_with_no_manifest_entry_rejected(tmp_path):
    records_dir = tmp_path / "contender_evaluation"
    records_dir.mkdir()
    vrt = _valid_record("VRT")
    wmt = _valid_record("WMT")
    (records_dir / "VRT.yaml").write_text(yaml.safe_dump(vrt), encoding="utf-8")
    (records_dir / "WMT.yaml").write_text(yaml.safe_dump(wmt), encoding="utf-8")
    manifest = {
        "schema_version": "1.0", "governing_decision": "CONTENDER-0003",
        "cohort": [{
            "contender_symbol": "VRT", "canonical_comparator_symbol": "GEV",
            "shard_id": "s", "sealed_at": "2026-08-10T23:00:00Z",
            "content_sha256": vrt["content_sha256"], "schema_version": "1.0",
            "governing_decision": "CONTENDER-0003",
            "record_path": "intelligence/contender_evaluation/VRT.yaml",
        }],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = cev.validate_cohort_manifest(records_dir / "COHORT_MANIFEST.yaml", records_dir)
    assert not result.valid
    assert any("sealed record(s) on disk with no manifest entry" in e for e in result.errors)
    assert any("WMT" in e for e in result.errors if "no manifest entry" in e)


# ── comparator map ───────────────────────────────────────────────────────

def test_vrt_to_gev_accepted():
    errors = cev.validate_contender_evaluation_data(_valid_record("VRT"), expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []


def test_wmt_to_cost_accepted():
    errors = cev.validate_contender_evaluation_data(_valid_record("WMT"), expected_ticker="WMT", repo_root=REPO_ROOT)
    assert errors == []


def test_swapped_comparator_rejected():
    data = _valid_record("VRT")
    data["canonical_comparator_symbol"] = "COST"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("canonical_comparator_symbol must be" in e for e in errors)


def test_wrong_comparator_ticker_rejected():
    data = _valid_record("WMT")
    data["canonical_comparator_symbol"] = "AMZN"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="WMT", repo_root=REPO_ROOT)
    assert any("canonical_comparator_symbol must be" in e for e in errors)


def test_stale_structural_reference_hash_rejected():
    data = _valid_record("VRT")
    data["comparator_structural_reference"]["referenced_content_sha256"] = "0" * 64
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("referenced_content_sha256 is stale" in e for e in errors)


def test_structural_reference_wrong_source_file_rejected():
    data = _valid_record("VRT")
    data["comparator_structural_reference"]["source_file"] = "intelligence/valuation_archetype/COST.yaml"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("source_file must be" in e for e in errors)


def test_structural_reference_wrong_schema_rejected():
    data = _valid_record("VRT")
    data["comparator_structural_reference"]["source_schema"] = "classification"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("source_schema must be" in e for e in errors)


def test_structural_reference_nonexistent_comparator_file_reported():
    data = _valid_record("VRT")
    data["comparator_structural_reference"]["source_file"] = "intelligence/valuation_archetype/DOES_NOT_EXIST.yaml"
    data = _sealed(data)
    fake_root = REPO_ROOT  # comparator lookup is keyed off contender_symbol, not source_file
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=fake_root)
    # source_file mismatch is itself flagged; the hash still verifies against the real GEV.yaml
    assert any("source_file must be" in e for e in errors)


# ── schema: missing/extra keys at every nesting level ───────────────────

def test_missing_top_level_key_rejected():
    data = _valid_record("VRT")
    del data["archetype_assessment"]
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("missing top-level key" in e for e in errors)


def test_extra_top_level_key_rejected():
    data = _valid_record("VRT")
    data["extra_field"] = "smuggled"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("unrecognized key" in e for e in errors)


def test_extra_key_in_provenance_source_rejected():
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["fair_value"] = "smuggled"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("provenance.sources[0]" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_structural_reference_rejected():
    data = _valid_record("VRT")
    data["comparator_structural_reference"]["extra"] = "smuggled"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("comparator_structural_reference" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_archetype_assessment_rejected():
    data = _valid_record("VRT")
    data["archetype_assessment"]["score"] = 5
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("archetype_assessment" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_evidence_quality_assessment_rejected():
    data = _valid_record("VRT")
    data["evidence_quality_assessment"]["extra"] = "smuggled"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("evidence_quality_assessment" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_methodology_applicability_reference_rejected():
    data = _valid_record("VRT")
    data["methodology_applicability_reference"]["extra"] = "adjustment_required"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("methodology_applicability_reference" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_evidence_parity_finding_rejected():
    data = _valid_record("VRT")
    data["evidence_parity_finding"]["rank"] = 1
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("evidence_parity_finding" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_abstention_index_entry_rejected():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION,
        "reason": "Insufficient evidence.", "composite": "smuggled",
    }]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("abstention_index[0]" in e and "unrecognized key" in e for e in errors)


def test_extra_key_in_manifest_row_rejected(tmp_path):
    records_dir = tmp_path / "contender_evaluation"
    records_dir.mkdir()
    vrt = _valid_record("VRT")
    wmt = _valid_record("WMT")
    (records_dir / "VRT.yaml").write_text(yaml.safe_dump(vrt), encoding="utf-8")
    (records_dir / "WMT.yaml").write_text(yaml.safe_dump(wmt), encoding="utf-8")
    row = lambda t, rec: {
        "contender_symbol": t, "canonical_comparator_symbol": cev.AUTHORIZED_COMPARATOR_MAP[t],
        "shard_id": "s", "sealed_at": "2026-08-10T23:00:00Z",
        "content_sha256": rec["content_sha256"], "schema_version": "1.0",
        "governing_decision": "CONTENDER-0003",
        "record_path": f"intelligence/contender_evaluation/{t}.yaml",
    }
    bad_row = row("VRT", vrt)
    bad_row["overall_risk"] = "smuggled"
    manifest = {
        "schema_version": "1.0", "governing_decision": "CONTENDER-0003",
        "cohort": [bad_row, row("WMT", wmt)],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = cev.validate_cohort_manifest(records_dir / "COHORT_MANIFEST.yaml", records_dir)
    assert not result.valid
    assert any("unrecognized key" in e for e in result.errors)


def test_extra_key_in_manifest_top_level_rejected(tmp_path):
    records_dir = tmp_path / "contender_evaluation"
    records_dir.mkdir()
    manifest = {"schema_version": "1.0", "governing_decision": "CONTENDER-0003", "cohort": [], "extra": True}
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = cev.validate_cohort_manifest(records_dir / "COHORT_MANIFEST.yaml", records_dir)
    assert not result.valid
    assert any("unrecognized key" in e for e in result.errors)


# ── invalid enum values / archetype vocabulary ──────────────────────────

def test_invalid_primary_archetype_rejected():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = "H"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("primary_archetype invalid" in e for e in errors)


def test_secondary_archetype_equal_to_primary_rejected():
    data = _valid_record("VRT")
    data["archetype_assessment"]["secondary_archetype"] = "B"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("must not equal primary_archetype" in e for e in errors)


def test_secondary_archetype_cannot_itself_be_abstention():
    data = _valid_record("VRT")
    data["archetype_assessment"]["secondary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("secondary_archetype invalid" in e for e in errors)


def test_secondary_archetype_forced_null_on_primary_abstention():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = "F"
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION, "reason": "No evidence.",
    }]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("secondary_archetype must be null when primary_archetype is the abstention value" in e for e in errors)


def test_invalid_primary_source_coverage_rejected():
    data = _valid_record("VRT")
    data["evidence_quality_assessment"]["primary_source_coverage"] = "excellent"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("primary_source_coverage invalid" in e for e in errors)


def test_invalid_evidence_parity_finding_rejected():
    data = _valid_record("VRT")
    data["evidence_parity_finding"]["finding"] = "clearly_better"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("finding invalid" in e for e in errors)


def test_invalid_source_type_rejected():
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["source_type"] = "tertiary"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("source_type invalid" in e for e in errors)


def test_invalid_access_status_rejected():
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["access_status"] = "fully_memorized"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("access_status invalid" in e for e in errors)


def test_lifecycle_status_must_be_sealed():
    data = _valid_record("VRT")
    data["lifecycle_status"] = "draft"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("lifecycle_status invalid" in e for e in errors)


def test_governing_decisions_must_be_exactly_contender_0003():
    data = _valid_record("VRT")
    data["governing_decisions"] = ["CONTENDER-0002"]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("governing_decisions must be" in e for e in errors)


# ── methodology_applicability_reference: mechanical lookup only ─────────

def test_methodology_reference_wrong_family_role_rejected():
    data = _valid_record("VRT")
    data["methodology_applicability_reference"]["family_5_relative_valuation"] = "prohibited"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("family_5_relative_valuation must be" in e for e in errors)


def test_methodology_reference_archetype_mismatch_rejected():
    data = _valid_record("VRT")
    data["methodology_applicability_reference"]["archetype"] = "G"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("archetype must equal archetype_assessment.primary_archetype" in e for e in errors)


def test_methodology_reference_required_when_archetype_determined():
    data = _valid_record("VRT")
    data["methodology_applicability_reference"] = None
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("must be a mapping" in e for e in errors)


def test_methodology_reference_must_be_null_on_archetype_abstention():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION, "reason": "No evidence.",
    }]
    # deliberately leave methodology_applicability_reference populated (should be rejected)
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("must be null when" in e and "methodology_applicability_reference" in e for e in errors)


@pytest.mark.parametrize("archetype", sorted(cev._ARCHETYPE_LETTERS))
def test_methodology_reference_matches_governed_role_table_for_every_archetype(archetype):
    from valuation_result_validator import governed_role_for
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = archetype
    data["archetype_assessment"]["secondary_archetype"] = None
    data["methodology_applicability_reference"] = _methodology_applicability_reference(archetype)
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []
    for family_id in cev._FAMILY_IDS:
        assert data["methodology_applicability_reference"][family_id] == governed_role_for(family_id, archetype)


# ── numeric leakage: digits, percent, ratios, magnitude comparisons ────

@pytest.mark.parametrize("text", [
    "Revenue grew 26% organic year over year.",
    "Backlog reached $15 billion in the quarter.",
    "Net leverage was approximately 0.2x at quarter end.",
    "Book-to-bill ratio of 2.9x.",
    "933 warehouses across several countries.",
    "A 2:1 ratio of product to service revenue.",
])
def test_bare_digit_leakage_caught_in_rationale(text):
    data = _valid_record("VRT")
    data["archetype_assessment"]["rationale"] = text
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("numeric-leakage:bare-digit" in e for e in errors)


@pytest.mark.parametrize("text", [
    "The comparator's evidence base is three times richer than the contender's.",
    "Revenue effectively doubled over the period described.",
    "The contender's margin profile roughly tripled in scope.",
    "A twofold increase in evidence completeness was disclosed.",
    "The gap has since halved according to disclosed commentary.",
])
def test_written_out_magnitude_comparison_caught(text):
    data = _valid_record("VRT")
    data["evidence_parity_finding"]["rationale"] = text
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("numeric-leakage:written-out-magnitude-word" in e for e in errors)


@pytest.mark.parametrize("text", [
    "Uncertainty remains about the precise scope of a disclosed item.",
    "The evidence base discloses no margin or leverage figures at all.",
    "A materially deeper sourcing chain underlies this comparator's own record.",
])
def test_numeric_scan_false_positive_guards(text):
    """Legitimate qualitative language with no digit and no magnitude
    word must validate cleanly -- the numeric scan must not over-trigger
    on ordinary prose."""
    findings = cev._numeric_leakage_scan(text)
    assert findings == []


# ── numeric leakage: spelled-out cardinal numbers (MAJOR-3) ────────────
# Reviewer-found live violation: "three reported operating segments" in
# WMT.yaml passed clean despite the schema's own zero-numeric-field,
# no-carve-out rule -- the magnitude-comparison scan above catches
# "three times" but not an ordinary spelled-out count.

@pytest.mark.parametrize("word", [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "dozen", "hundred", "thousand", "million", "billion",
])
def test_spelled_out_cardinal_standalone_caught(word):
    findings = cev._numeric_leakage_scan(f"This record discloses {word} named risk items.")
    assert "numeric-leakage:spelled-out-cardinal-number" in findings, word


@pytest.mark.parametrize("text", [
    "given Walmart's three reported operating segments",
    "a metric-basis ambiguity in one segment's loss guidance",
    "revenue exceeding one hundred million in the disclosed period",
    "a dozen named risks were disclosed",
    "Two comparators were named in the committee review.",
    "three, four, or five named items were disclosed",  # punctuation/conjunction variant
    "three-segment structure disclosed in the filing",  # hyphen/compound form
])
def test_spelled_out_cardinal_punctuation_conjunction_hyphen_variants_caught(text):
    findings = cev._numeric_leakage_scan(text)
    assert "numeric-leakage:spelled-out-cardinal-number" in findings, text


def test_spelled_out_cardinal_caught_in_real_field_scan():
    data = _valid_record("WMT")
    data["archetype_assessment"]["rationale"] = "Walmart reports three operating segments."
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="WMT", repo_root=REPO_ROOT)
    assert any("numeric-leakage:spelled-out-cardinal-number" in e for e in errors)


@pytest.mark.parametrize("text", [
    "given Walmart's multiple reported operating segments",
    "an unquantified customer-concentration gap flagged by outside commentary",
    "a named comparator in GEV's own committee review",
    "several named risk items were disclosed",
])
def test_cardinal_scan_false_positive_guards_for_reworded_real_text(text):
    """The exact reworded replacement phrases used in the real VRT/WMT
    records (after this correction) must validate cleanly -- proving the
    fix, not merely the mechanism."""
    findings = cev._numeric_leakage_scan(text)
    assert findings == [], text


def test_cardinal_scan_bounded_vocabulary_documented_precision_tradeoff():
    """A bounded closed vocabulary (not a general NLP number parser, per
    the operator's own explicit instruction) necessarily accepts some
    imprecision at its edges -- "one" as a non-numeric determiner inside
    an idiom like "no one factor" is caught even though it isn't a
    genuine numeric claim. Documented here as an accepted, disclosed
    tradeoff (this schema's own narrow technical domain rarely needs
    that construction; the real VRT/WMT records use neither), not
    silently left for a future session to rediscover as a surprise."""
    findings = cev._numeric_leakage_scan("no one factor drives this characterization")
    assert "numeric-leakage:spelled-out-cardinal-number" in findings


def test_date_fields_are_not_scanned_for_numeric_leakage():
    """as_of_date/sealed_at legitimately contain digits (ISO dates) and
    must never be scanned by the numeric-leakage check -- only the three
    narrative rationale/uncertainty/finding-rationale fields are."""
    data = _valid_record("VRT")
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []  # sealed_at, as_of_date, governing_decisions all contain digits


# ── directive/trading language -- word-boundary matched ────────────────

@pytest.mark.parametrize("word,sentence", [
    ("buy", "Investors should not buy or sell based on this record."),
    ("sell", "This record does not sell any recommendation."),
    ("add", "Nothing here should add exposure of any kind."),
    ("hold", "This finding does not direct anyone to hold a position."),
    ("trim", "No trim action is implied by this comparison."),
    ("exit", "No exit decision is made or implied here."),
    ("wait", "This record does not say to wait before acting."),
])
def test_directive_words_caught_active_negated_variants(word, sentence):
    findings = cev._prohibited_content_scan(sentence)
    assert any(f"directive-word:\\b{word}\\b" in f for f in findings)


def test_directive_word_add_does_not_false_positive_on_address():
    findings = cev._prohibited_content_scan("This record does not address that question.")
    assert findings == []


def test_directive_word_exit_does_not_false_positive_on_exiting():
    findings = cev._prohibited_content_scan("The comparator is not exiting this business line.")
    # "exiting" contains "exit" but word-boundary matching requires \bexit\b;
    # "exiting" has no boundary between "exit" and "ing", so it must not match.
    assert not any("directive-word:\\bexit\\b" in f for f in findings)


def test_directive_word_hold_does_not_false_positive_on_holdings():
    findings = cev._prohibited_content_scan("This does not describe portfolio holdings of any kind.")
    assert not any("directive-word:\\bhold\\b" in f for f in findings)


def test_stage_legitimate_taxonomy_use_whitelisted():
    findings = cev._prohibited_content_scan("Archetype E describes an early-stage business model.")
    assert not any("directive-word" in f and "stage" in f for f in findings)


def test_bare_stage_word_still_caught():
    findings = cev._prohibited_content_scan("This record does not say to stage a purchase.")
    assert any("directive-word:\\bstage\\b" in f for f in findings)


# ── promotion/replace/supersede/displace + score/rank/composite ────────

@pytest.mark.parametrize("text", [
    "VRT should be promoted into the canonical roster.",
    "This finding supports promoting the contender.",
    "WMT should replace COST in the portfolio.",
    "The contender's evidence supersedes the comparator's own record.",
    "This assessment would displace the comparator entirely.",
    "VRT should be added to the canonical 27.",
])
def test_promotion_language_caught_active_passive_variants(text):
    findings = cev._promotion_language_scan(text)
    assert findings, f"expected a promotion-language finding for: {text!r}"


def test_promotion_language_negated_variant_still_caught():
    """A negated assertion still contains the same forbidden verb -- this
    scan is a bounded term-list match, not a sentiment classifier, so a
    negation does not exempt the sentence (matching the operator's own
    'negated variants must still be caught' instruction)."""
    findings = cev._promotion_language_scan("This record does not promote VRT into any roster.")
    assert findings


@pytest.mark.parametrize("key_name", ["score", "rank", "priority_index", "composite", "ranking", "overall_score"])
def test_score_rank_composite_key_names_rejected_anywhere_in_tree(key_name):
    data = _valid_record("VRT")
    data["evidence_parity_finding"][key_name] = "smuggled"
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("forbidden score/rank/composite-shaped key name" in e for e in errors) or any(
        "unrecognized key" in e for e in errors
    )


def test_score_key_nested_deep_in_abstention_index_caught():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION,
        "reason": "No evidence.", "rank": 1,
    }]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("rank" in e and ("forbidden score/rank" in e or "unrecognized key" in e) for e in errors)


# ── comparative-investment-superiority: a materially separate scan ─────

@pytest.mark.parametrize("text", [
    "VRT is the better investment.",
    "WMT offers the stronger investment case.",
    "VRT should outperform GEV.",
    "GEV is inferior to VRT.",
    "WMT is preferable to COST.",
    "VRT has the superior business.",
    "COST is a weaker investment than WMT.",
])
def test_comparative_superiority_positive_examples_caught(text):
    findings = cev._comparative_superiority_scan(text)
    assert findings, f"expected a comparative-superiority finding for: {text!r}"


@pytest.mark.parametrize("text", [
    "VRT's evidence base is less mature than GEV's.",
    "Both records share the same primary archetype.",
    "Evidence completeness differs between the two records.",
    "Insufficient evidence exists to support a parity determination.",
    "The contender's evidence base is materially less mature than the comparator's.",
])
def test_comparative_superiority_false_positive_guards(text):
    """Legitimate descriptive language about evidence completeness,
    maturity, archetype classification, or abstention must validate
    cleanly -- CONTENDER-0003 SS F's own explicit adversarial requirement."""
    findings = cev._comparative_superiority_scan(text)
    assert findings == []


def test_comparative_superiority_scan_is_a_separate_mechanism_from_promotion_scan():
    """A comparative-superiority claim naming no action/score must be
    caught by the superiority scan but NOT by the promotion-language
    scan -- proving the two are materially separate mechanisms, not one
    scan reused twice (CONTENDER-0003 SS F's own explicit instruction)."""
    text = "VRT is the better investment."
    assert cev._comparative_superiority_scan(text)
    assert cev._promotion_language_scan(text) == []


def test_promotion_scan_catches_action_language_superiority_scan_does_not():
    text = "VRT should be promoted into the canonical roster."
    assert cev._promotion_language_scan(text)
    assert cev._comparative_superiority_scan(text) == []


def test_comparative_superiority_scan_applied_to_archetype_and_evidence_parity_rationale_only():
    data = _valid_record("VRT")
    data["archetype_assessment"]["rationale"] = "This ticker has the superior business model."
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("comparative-superiority" in e for e in errors)

    data2 = _valid_record("VRT")
    data2["evidence_parity_finding"]["rationale"] = "This ticker is the better investment overall."
    data2 = _sealed(data2)
    errors2 = cev.validate_contender_evaluation_data(data2, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("comparative-superiority" in e for e in errors2)


def test_comparative_superiority_scan_not_applied_to_uncertainty_statement():
    """CONTENDER-0003 SS F scopes the comparative-superiority scan to
    archetype_assessment.rationale and evidence_parity_finding.rationale
    specifically -- evidence_quality_assessment.uncertainty_statement is
    not in scope for this particular check (it is still scanned for
    every other prohibited-content category)."""
    data = _valid_record("VRT")
    data["evidence_quality_assessment"]["uncertainty_statement"] = (
        "This record's evidence is the better investment case, hypothetically."
    )
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert not any("comparative-superiority" in e for e in errors)


# ── comparative-superiority / promotion: broadened vulnerability-class ─
# coverage (MAJOR-4). An independent exact-head review constructed fresh
# adversarial variants not present in the original test suite and found
# 6-10 of 11 comparative-superiority constructions, and all 8 promotion
# constructions, returned []. These tests lock in the fix and probe
# negation/punctuation/conjunction/active-passive/subject-object variants
# beyond the review's own examples.

@pytest.mark.parametrize("text", [
    "more attractive investment", "less compelling investment",
    "the best choice between the two", "should beat the comparator",
    "the weaker long-term holding", "a higher-quality investment",
    "a top pick", "the more compelling opportunity",
    "the worse of the two options", "a more attractive holding",
    "the smarter investment choice",
])
def test_comparative_superiority_broadened_review_examples_caught(text):
    findings = cev._comparative_superiority_scan(text)
    assert findings, f"expected a comparative-superiority finding for: {text!r}"


@pytest.mark.parametrize("text", [
    "GEV should be removed in favor of VRT", "VRT ought to take GEV's place",
    "a better fit for the canonical roster", "deserves a spot among the canonical holdings",
    "recommends adding VRT to the portfolio", "merits inclusion in the targets file",
    "swapping GEV for VRT", "demoting GEV in favor of the contender",
])
def test_promotion_broadened_review_examples_caught(text):
    findings = cev._promotion_language_scan(text)
    assert findings, f"expected a promotion-language finding for: {text!r}"


@pytest.mark.parametrize("text", [
    # negation -- a bounded term-list match, not a sentiment classifier;
    # a negated sentence still contains the same forbidden term.
    "This is not the more attractive investment on a closer look.",
    "VRT is not obviously the smarter investment choice here.",
    "GEV was not swapped out for anything in this record.",
    # punctuation variants
    "the weaker, long-term holding, on balance",
    "a higher-quality investment; disclosed only as a hypothetical",
    "GEV should be removed, in favor of VRT, per this framing",
    # conjunction variants
    "VRT and GEV were compared, and VRT emerged as the more attractive holding",
    "neither a top pick nor an obvious laggard, and yet described as such",
    # active/passive variants
    "the contender was described as a more attractive investment by the analysis",
    "the analysis described the contender as a more attractive investment",
    "GEV was removed from consideration in favor of the contender",
    "the drafting removed GEV from consideration in favor of the contender",
    # subject/object inversion
    "compared to GEV, VRT is a more attractive holding",
    "VRT, compared to GEV, is a more attractive holding",
])
def test_comparative_and_promotion_scans_catch_variant_phrasings(text):
    findings = cev._comparative_superiority_scan(text) + cev._promotion_language_scan(text)
    assert findings, f"expected a finding for: {text!r}"


@pytest.mark.parametrize("text", [
    # allowed evidence-completeness/archetype language, restated with the
    # broadened vocabulary now active -- must still validate cleanly
    "the contender's evidence base is materially less mature than the comparator's",
    "both records share the same primary archetype",
    "insufficient evidence exists to support a parity determination",
    "the contender's evidence quality is limited relative to the comparator's comprehensive coverage",
    "archetype B was assigned based on the disclosed reinvestment profile",
    "the comparator's own record discloses a richer sourcing chain",
])
def test_broadened_scans_still_pass_legitimate_descriptive_language(text):
    findings = cev._comparative_superiority_scan(text) + cev._promotion_language_scan(text)
    assert findings == [], f"unexpected finding(s) for legitimate text: {text!r} -> {findings}"


# ── comparative-superiority / promotion: residual bypass closure (round 2,
# delta review MAJOR-4) ─────────────────────────────────────────────────
# A delta review confirmed MAJOR-1/2/3 and the MINOR resolved but found
# exactly two reproducible residual bypasses: "looks weaker on a relative
# basis" (comparative-superiority, no trailing noun -- the round-1 fix's
# adj-noun pattern never matches a bare verb+adjective+relative-suffix
# construction) and "inclusion should be reconsidered in favor of"
# (promotion-language, no promote/replace/remove/demote/swap/add verb --
# the round-1 fix never covered inclusion/reconsideration/precedence
# language). These tests lock in the closure of both, and the explicit
# allowed/prohibited boundary the delta review required: comparative
# EVIDENCE quality/maturity language stays allowed; comparative
# INVESTMENT/PORTFOLIO quality or inclusion judgment is rejected.

@pytest.mark.parametrize("text", [
    "looks weaker on a relative basis",
    "appears stronger relative to",
    "seems weaker than",
    "looks more attractive relative to",
    "appears less compelling than",
])
def test_bypass_a_comparative_relative_construction_now_caught(text):
    findings = cev._comparative_superiority_scan(text)
    assert findings, f"expected a comparative-superiority finding for: {text!r}"


@pytest.mark.parametrize("text", [
    "inclusion should be reconsidered in favor of",
    "inclusion should favor",
    "reconsider inclusion in favor of",
    "should be included instead of",
    "should remain included over",
    "inclusion is preferred over",
    "should take precedence over",
])
def test_bypass_b_inclusion_precedence_construction_now_caught(text):
    findings = cev._promotion_language_scan(text)
    assert findings, f"expected a promotion-language finding for: {text!r}"


@pytest.mark.parametrize("text", [
    "GEV looks weaker on a relative basis compared to VRT",
    "VRT appears stronger relative to GEV",
    "WMT seems weaker than COST as an investment",
    "the relatively weaker holding",
    "a relatively superior investment",
    "COST looks more attractive relative to WMT",
    "GEV appears less compelling than VRT",
])
def test_round2_comparative_prohibited_adversarial_matrix_caught(text):
    findings = cev._comparative_superiority_scan(text)
    assert findings, f"expected a comparative-superiority finding for: {text!r}"


@pytest.mark.parametrize("text", [
    "inclusion should be reconsidered in favor of VRT",
    "GEV's inclusion should be reconsidered in favor of VRT",
    "VRT should be included instead of GEV",
    "inclusion should favor WMT over COST",
    "WMT should take precedence over COST in the portfolio",
    "COST should remain excluded in favor of WMT",
    "VRT is preferred for inclusion over GEV",
    # reversed subject/object
    "in favor of VRT, GEV's inclusion should be reconsidered",
    "COST, not WMT, should remain excluded in favor of the contender",
])
def test_round2_promotion_inclusion_prohibited_adversarial_matrix_caught(text):
    findings = cev._promotion_language_scan(text)
    assert findings, f"expected a promotion-language finding for: {text!r}"


@pytest.mark.parametrize("text", [
    # comparative EVIDENCE quality/maturity language stays allowed -- the
    # explicit distinguishing boundary the delta review required.
    "evidence quality looks weaker because the source set is incomplete",
    "evidence maturity is relatively weaker",
    "the evidence quality is relatively stronger",
    "this contender has weaker evidence coverage than the comparator",
    "the evidence base is thinner for this contender",
    "sourcing reliability is comparatively lower for this record",
])
def test_round2_evidence_quality_comparison_language_stays_allowed(text):
    findings = cev._comparative_superiority_scan(text) + cev._promotion_language_scan(text)
    assert findings == [], f"unexpected finding(s) for legitimate text: {text!r} -> {findings}"


def test_round2_exclude_scope_does_not_false_positive_on_real_vrt_text():
    # The exclude pattern is deliberately scoped to require a co-occurring
    # "in favor of" -- an unscoped bare "exclude" pattern was found, during
    # this fix's own design, to false-positive on VRT.yaml's legitimate
    # "excluded from this assessment's reasoning" (excluded from the
    # analysis, not a comparator-inclusion judgment). This test pins that
    # scoping decision directly against the real record's own text.
    texts = [
        "and which is accordingly excluded from this assessment's reasoning "
        "-- placing overall coverage between the comprehensive and limited tiers.",
        "and an unsubstantiated backlog figure explicitly excluded from "
        "this assessment's own reasoning.",
    ]
    for text in texts:
        findings = cev._comparative_superiority_scan(text) + cev._promotion_language_scan(text)
        assert findings == [], f"unexpected finding(s) for legitimate real-record text: {text!r} -> {findings}"


def test_round2_comparative_and_promotion_scans_remain_materially_separate_mechanisms():
    # A comparative-only construction must never trigger the promotion
    # scan, and a promotion-only construction must never trigger the
    # comparative scan -- proving the two round-2 extensions did not
    # collapse the two scans into one shared mechanism.
    comparative_only = "looks weaker on a relative basis"
    assert cev._comparative_superiority_scan(comparative_only)
    assert cev._promotion_language_scan(comparative_only) == []

    promotion_only = "inclusion should be reconsidered in favor of the contender"
    assert cev._promotion_language_scan(promotion_only)
    assert cev._comparative_superiority_scan(promotion_only) == []


# ── provenance free-text scan coverage (MAJOR-2) ────────────────────────
# An independent exact-head review found provenance.sources[].
# source_identifier/.limitation received zero content-safety scanning of
# any kind -- a real, populated schema field (both real records use
# `limitation` substantively) where an injected capital-priority/
# promotion/superiority/policy-leak sentence produced zero findings.

def test_provenance_limitation_rejects_injected_promotion_and_superiority_sentence():
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["limitation"] = (
        "VRT is the better investment and should be promoted into the canonical 27; "
        "conviction is High per portfolio_role_ref."
    )
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("provenance.sources[0].limitation" in e for e in errors)
    assert any("policy-leak" in e for e in errors)
    assert any("promotion-language" in e for e in errors)
    assert any("comparative-superiority" in e for e in errors)


def test_provenance_source_identifier_rejects_injected_promotion_and_superiority_sentence():
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["source_identifier"] = (
        "VRT is a top pick and deserves a spot among the canonical holdings"
    )
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("provenance.sources[0].source_identifier" in e for e in errors)


@pytest.mark.parametrize("phrase", [
    "conviction", "portfolio_role_ref", "target_pct", "targets.yaml", "primary_disposition",
])
def test_provenance_limitation_rejects_policy_leak(phrase):
    data = _valid_record("WMT")
    data["provenance"]["sources"][0]["limitation"] = f"This note mentions {phrase} directly."
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="WMT", repo_root=REPO_ROOT)
    assert any("policy-leak" in e for e in errors)


@pytest.mark.parametrize("phrase", [
    "a support level near recent lows", "a bullish MACD signal", "considered oversold",
])
def test_provenance_limitation_rejects_chart_domain(phrase):
    data = _valid_record("WMT")
    data["provenance"]["sources"][0]["limitation"] = f"This does not rely on {phrase}."
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="WMT", repo_root=REPO_ROOT)
    assert any("chart-domain" in e for e in errors)


def test_provenance_limitation_rejects_numeric_leakage_no_carve_out():
    """limitation is a narrative field -- numeric leakage applies with no
    carve-out, unlike source_identifier (a legitimate path/ID field)."""
    data = _valid_record("WMT")
    data["provenance"]["sources"][0]["limitation"] = "Cited for three named comparators."
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="WMT", repo_root=REPO_ROOT)
    assert any("numeric-leakage:spelled-out-cardinal-number" in e for e in errors)


def test_provenance_source_identifier_exempt_from_numeric_leakage():
    """A real repository path legitimately and unavoidably contains
    digits (a decision ID like PI-0019) -- source_identifier is exempt
    from the numeric-leakage scan specifically, unlike limitation."""
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["source_identifier"] = (
        "governance/decisions/PI-0019-gev-committee-review-authorization.md"
    )
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert not any("numeric-leakage" in e for e in errors)


def test_provenance_source_identifier_and_limitation_exempt_from_directive_word_scan():
    """Citation-field exemption, matching the established repository
    precedent (functional_doctrine_validator.py's _CITATION_FIELD_NAMES):
    only the directive-word scan is exempted for these two fields -- a
    legitimate path/note should never be penalized for an incidental
    'add'/'hold'-shaped substring. Every other scan still applies."""
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["source_identifier"] = "intelligence/companies/VRT.yaml"
    data["provenance"]["sources"][0]["limitation"] = (
        "This source does not directly address the customer-concentration gap."
    )
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert not any("directive-word" in e for e in errors)


def test_provenance_legitimate_source_identifier_and_limitation_false_positive_guards():
    """Real, legitimate citation-shaped strings -- exactly the kind this
    schema actually uses -- must validate cleanly."""
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["source_identifier"] = (
        "governance/decisions/PI-0020-gev-intelligence-refresh-authorization.md"
    )
    data["provenance"]["sources"][0]["limitation"] = (
        "Cited for process-only comparator context, not a capital-priority finding about VRT."
    )
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []


def test_provenance_limitation_must_be_non_empty_string_when_present():
    data = _valid_record("VRT")
    data["provenance"]["sources"][0]["limitation"] = ""
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("limitation must be a non-empty string" in e for e in errors)


# ── chart-domain and policy-leak scans ──────────────────────────────────

@pytest.mark.parametrize("phrase", [
    "a support level near recent lows", "breakout above resistance",
    "the moving average crossed", "an RSI reading below thirty",
    "a bullish MACD signal", "a candlestick reversal pattern",
    "a classic chart pattern", "standard technical analysis",
    "considered oversold", "considered overbought",
    "a Fibonacci retracement", "elevated volume profile", "a price target range",
])
def test_chart_domain_terms_caught(phrase):
    findings = cev._prohibited_content_scan(f"This record does not rely on {phrase}.")
    assert any("chart-domain" in f for f in findings)


@pytest.mark.parametrize("phrase", [
    "conviction", "portfolio_role_ref", "target_pct", "targets.yaml",
    "holdings.yaml", "gates.yaml", "next_gate", "allow_add",
    "issuer_lookthrough.yaml", "primary_disposition", "case_for_review",
])
def test_policy_leak_terms_caught(phrase):
    findings = cev._prohibited_content_scan(f"This mentions {phrase} directly.")
    assert any("policy-leak" in f for f in findings)


def test_gate_legitimate_technical_use_whitelisted():
    findings = cev._prohibited_content_scan("This describes a gate-all-around transistor structure.")
    assert "bare-gate-word" not in findings


def test_bare_gate_word_still_caught():
    findings = cev._prohibited_content_scan("Whether the comparator's own gate should reopen is not addressed here.")
    assert "bare-gate-word" in findings


# ── abstention: missing reason, valid abstention, index reconciliation ─

def test_abstention_missing_reason_rejected():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = [{"field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION, "reason": ""}]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("abstention_index[0].reason must be a non-empty string" in e for e in errors)


def test_valid_archetype_abstention_accepted():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["archetype_assessment"]["rationale"] = "No sufficient evidence was located for an archetype call."
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION,
        "reason": "Evidence base does not support a determined archetype call.",
    }]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []


def test_valid_evidence_parity_abstention_accepted():
    data = _valid_record("VRT")
    data["evidence_parity_finding"]["finding"] = cev._EVIDENCE_PARITY_ABSTENTION
    data["evidence_parity_finding"]["rationale"] = "Evidence on both sides is too thin to compare."
    data["abstention_index"] = [{
        "field": "finding", "value": cev._EVIDENCE_PARITY_ABSTENTION,
        "reason": "Evidence base on both sides is too thin for a parity call.",
    }]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []


def test_abstention_index_missing_entry_for_real_abstention_rejected():
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = []  # forgot to index the real abstention
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("abstention_index is missing an entry for field 'primary_archetype'" in e for e in errors)


def test_abstention_index_entry_for_non_abstained_field_rejected():
    """The converse direction of bidirectional reconciliation: an index
    entry claiming an abstention that is not actually present in the
    record must also be rejected."""
    data = _valid_record("VRT")  # fully determined, no abstention anywhere
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION, "reason": "Not real.",
    }]
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert any("not genuinely abstained" in e for e in errors)


def test_non_cascading_archetype_abstention_does_not_force_evidence_parity_abstention():
    """SS C.3: an abstention on one field never forces or implies a
    value on another. Archetype abstains; evidence_parity_finding
    remains independently determined."""
    data = _valid_record("VRT")
    data["archetype_assessment"]["primary_archetype"] = cev._ARCHETYPE_ABSTENTION
    data["archetype_assessment"]["secondary_archetype"] = None
    data["methodology_applicability_reference"] = None
    data["abstention_index"] = [{
        "field": "primary_archetype", "value": cev._ARCHETYPE_ABSTENTION, "reason": "No evidence.",
    }]
    # evidence_parity_finding stays determined -- not forced to abstain too
    data = _sealed(data)
    errors = cev.validate_contender_evaluation_data(data, expected_ticker="VRT", repo_root=REPO_ROOT)
    assert errors == []


# ── protected records: byte-identity ────────────────────────────────────

def _resolve_pr_base_sha(cwd: Path = REPO_ROOT) -> str | None:
    """Resolve this branch's actual PR base commit from live repository
    truth -- git merge-base HEAD origin/main -- rather than a hard-coded
    SHA that goes stale the moment the branch is rebased or main moves
    forward. Returns None (causing the calling test to skip, not fail)
    if origin/main is not a resolvable ref in this environment -- e.g. a
    detached clone with no remote configured -- since that is an
    environment precondition this test suite does not manage, not a
    content defect. Deliberately does NOT use local `main`: this
    repository's own history discloses local `main` can diverge
    substantially from `origin/main` (stale local branches, never
    force-pushed), which would silently resolve to the wrong base.

    `cwd` defaults to the real repository root but accepts any git
    working directory -- exercised directly against synthetic,
    disposable repositories by the lifecycle-invariant tests below, so
    the actual resolution mechanism (not a reimplementation of it) is
    what gets proven correct in both the active-feature-branch and
    post-merge-main states."""
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


_PROTECTED_INTELLIGENCE_AND_GOVERNANCE_PATHS = [
    "intelligence/companies/GEV.yaml", "intelligence/companies/GEV.md",
    "intelligence/companies/COST.yaml", "intelligence/companies/COST.md",
    "intelligence/valuation_archetype/GEV.yaml", "intelligence/valuation_archetype/COST.yaml",
    "intelligence/classification/GEV.yaml", "intelligence/classification/COST.yaml",
    "governance/decisions/PI-0019-gev-committee-review-authorization.md",
    "governance/decisions/PI-0020-gev-intelligence-refresh-authorization.md",
    "governance/decisions/PI-0021-cost-committee-review-authorization.md",
    "governance/decisions/PI-0022-cost-intelligence-refresh-authorization.md",
]

_PROTECTED_INTELLIGENCE_BROAD_PATHS = [
    "intelligence/classification", "intelligence/companies", "intelligence/themes",
    "intelligence/relationships", "intelligence/valuation_archetype",
    "intelligence/valuation_evidence", "intelligence/valuation_results",
    "intelligence/functional_doctrine", "intelligence/overlap_model",
    "intelligence/economic_assessment", "intelligence/etf_classification",
    "intelligence/crypto_classification", "intelligence/instrument_economic_assessment",
    "intelligence/reconciliation", "intelligence/recommendations", "intelligence/contenders",
]


def _assert_no_base_to_head_diff(paths: list[str]) -> None:
    """True PR-range comparison (base..HEAD), not a working-tree check --
    a MINOR finding from an independent exact-head review: git status
    --porcelain only ever compares the working tree to HEAD, so it would
    show clean even for a protected file modified AND committed earlier
    within this same PR's own commit history. git diff <base>..HEAD
    catches that; git status never can, regardless of how carefully it
    is invoked."""
    base_sha = _resolve_pr_base_sha()
    if base_sha is None:
        pytest.skip("origin/main not resolvable in this environment -- cannot compute a true PR-base diff")
    result = subprocess.run(
        ["git", "diff", "--exit-code", f"{base_sha}..HEAD", "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"unexpected changes under protected paths between base {base_sha} and HEAD:\n{result.stdout}"
    )


def test_protected_intelligence_and_governance_records_untouched():
    """Zero diff on GEV/COST Company Intelligence, their sealed
    valuation_archetype/classification records, and the four cited
    PI-0019/0020/0021/0022 governance decisions, across this PR's entire
    base..HEAD range -- not merely the current working tree."""
    _assert_no_base_to_head_diff(_PROTECTED_INTELLIGENCE_AND_GOVERNANCE_PATHS)


def test_protected_intelligence_records_broadly_untouched():
    # only new, untracked contender_evaluation/ files may appear anywhere
    # under intelligence/ as a result of this implementation -- none of
    # these paths are contender_evaluation, so any hit here is a real defect.
    _assert_no_base_to_head_diff(_PROTECTED_INTELLIGENCE_BROAD_PATHS)


def _init_synthetic_repo(tmp_path: Path):
    """A minimal, disposable git repository used to prove
    _resolve_pr_base_sha's actual behavioral invariant deterministically
    -- independent of this real repository's own PR/merge lifecycle,
    which is exactly the coupling that made the historical-SHA version
    of this test go stale the moment PR #299 merged (main advanced past
    the hard-coded base, so HEAD == origin/main and merge-base correctly
    returned the new tip -- not a defect, the documented, anticipated
    lifecycle transition). `refs/remotes/origin/main` is written
    directly via `update-ref`, standing in for a real remote-tracking
    ref without needing actual remote wiring."""
    def run(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, capture_output=True, text=True, check=True,
        )
    run("init", "-q")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "Test")
    return run


def test_resolve_pr_base_sha_returns_true_divergence_point_on_diverged_branch(tmp_path):
    """Behavioral invariant A -- active feature branch: when HEAD has
    diverged from origin/main by one or more new commits, the resolver
    must return the actual common ancestor (the true PR base), never
    silently compare HEAD to itself. This is the safety property the
    protected-path tests above depend on."""
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
    """Behavioral invariant B -- post-merge main: when HEAD and
    origin/main point at the identical commit (no divergence -- exactly
    the state this real repository is in immediately after a PR merges),
    the resolver may legitimately return that same commit. Asserting
    this directly, rather than against a fixed historical SHA, is what
    keeps this test from going stale the next time main advances."""
    run = _init_synthetic_repo(tmp_path)
    (tmp_path / "file.txt").write_text("content\n")
    run("add", "-A")
    run("commit", "-q", "-m", "sole commit, HEAD and origin/main coincide")
    sole_sha = run("rev-parse", "HEAD").stdout.strip()
    run("update-ref", "refs/remotes/origin/main", sole_sha)

    resolved = _resolve_pr_base_sha(cwd=tmp_path)
    assert resolved == sole_sha


def test_base_to_head_diff_mechanism_detects_a_synthetic_protected_path_change(tmp_path):
    """Proves the mechanism itself would catch a real base-vs-HEAD
    difference, not merely that today's clean diff produces no output --
    a synthetic-but-real two-commit repository stands in for this PR's
    own history, since mutating the real repository's protected paths
    even transiently is not an acceptable way to test this."""

    def run(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, capture_output=True, text=True, check=True,
        )

    run("init", "-q")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "Test")
    protected = tmp_path / "intelligence" / "companies" / "GEV.yaml"
    protected.parent.mkdir(parents=True)
    protected.write_text("original: true\n")
    run("add", "-A")
    run("commit", "-q", "-m", "base commit")
    base_sha = run("rev-parse", "HEAD").stdout.strip()

    # Simulate origin/main pointing at the base commit, matching this
    # synthetic repo's own shape (no real 'origin' remote needed for the
    # diff mechanism itself -- git diff <sha>..HEAD works on any two
    # resolvable refs, which is exactly what _assert_no_base_to_head_diff
    # relies on).
    protected.write_text("original: true\nmutated: true\n")
    run("add", "-A")
    run("commit", "-q", "-m", "protected-path mutation, committed within the simulated PR")
    head_sha = run("rev-parse", "HEAD").stdout.strip()

    result = subprocess.run(
        ["git", "diff", "--exit-code", f"{base_sha}..{head_sha}", "--",
         "intelligence/companies/GEV.yaml"],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode != 0, "the base..HEAD diff mechanism failed to detect a real committed protected-path change"
    assert "mutated" in result.stdout

    # And the working-tree-only check this MINOR finding replaced would
    # have missed it entirely, since both commits are already committed
    # and the working tree is clean relative to HEAD -- demonstrating
    # exactly why git status --porcelain was insufficient.
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=tmp_path, capture_output=True, text=True, check=True,
    )
    assert status.stdout.strip() == "", "sanity check: working tree should be clean at HEAD"


def test_protected_paths_untouched_by_this_module_import():
    protected = ["targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
                 "allocate.py", "margin_state.py", "levels.py"]
    hashes_before = {}
    for rel in protected:
        p = REPO_ROOT / rel
        if p.is_file():
            hashes_before[rel] = p.read_bytes()

    cev.validate_contender_evaluation_directory(REPO_ROOT / "intelligence" / "contender_evaluation", repo_root=REPO_ROOT)

    for rel, before in hashes_before.items():
        assert (REPO_ROOT / rel).read_bytes() == before, f"{rel} was mutated"


def test_canonical_validators_not_modified_by_this_pilot():
    """CONTENDER-0003 SS I bars any hardening/expansion/weakening of the
    existing canonical validators -- a live sanity check (via AST, not a
    raw substring search, since this module's own docstring legitimately
    discusses those modules in prose) that this module never *imports*
    classification_validator.py or valuation_evidence_validator.py at
    all -- only the two explicitly authorized read-only helpers
    (valuation_archetype_validator.canonical_record_hash,
    valuation_result_validator.governed_role_for) are imported."""
    source = (REPO_ROOT / "contender_evaluation_validator.py").read_text()
    tree = ast.parse(source)
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module)
    assert "classification_validator" not in imported_names
    assert "valuation_evidence_validator" not in imported_names
    # confirm the two explicitly-authorized read-only helpers ARE the
    # only cross-schema imports actually present (positive control)
    assert imported_names & {"valuation_archetype_validator", "valuation_result_validator"} == {
        "valuation_archetype_validator", "valuation_result_validator",
    }


# ── zero import coupling with allocate.py/margin_state.py ──────────────

def test_validator_module_imports_neither_allocate_nor_margin_state():
    source = (REPO_ROOT / "contender_evaluation_validator.py").read_text()
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
        assert "contender_evaluation_validator" not in source


# ── real-repository directory scan (the two real sealed records) ───────

def test_real_repository_contender_evaluation_directory_validates_clean():
    result = cev.validate_contender_evaluation_directory(
        REPO_ROOT / "intelligence" / "contender_evaluation", repo_root=REPO_ROOT,
    )
    if not result.valid:
        details = "\n".join(
            f"[{r.source}] {e}" for r in result.results if not r.valid for e in r.errors
        )
        pytest.fail(f"real contender_evaluation directory failed validation:\n{details}")
    assert result.record_count == 3  # VRT.yaml, WMT.yaml, COHORT_MANIFEST.yaml


def test_real_directory_contains_exactly_vrt_and_wmt():
    records_dir = REPO_ROOT / "intelligence" / "contender_evaluation"
    on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    assert on_disk == {"VRT", "WMT"}


def test_real_vrt_record_matches_governed_role_table():
    from valuation_result_validator import governed_role_for
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / "VRT.yaml").read_text())
    archetype = data["archetype_assessment"]["primary_archetype"]
    for family_id in cev._FAMILY_IDS:
        assert data["methodology_applicability_reference"][family_id] == governed_role_for(family_id, archetype)


def test_real_wmt_record_matches_governed_role_table():
    from valuation_result_validator import governed_role_for
    data = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / "WMT.yaml").read_text())
    archetype = data["archetype_assessment"]["primary_archetype"]
    for family_id in cev._FAMILY_IDS:
        assert data["methodology_applicability_reference"][family_id] == governed_role_for(family_id, archetype)


def test_real_records_carry_zero_numeric_fields_in_narrative_text():
    for ticker in ("VRT", "WMT"):
        data = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / f"{ticker}.yaml").read_text())
        for text in (
            data["archetype_assessment"]["rationale"],
            data["evidence_quality_assessment"]["uncertainty_statement"],
            data["evidence_parity_finding"]["rationale"],
        ):
            assert cev._numeric_leakage_scan(text) == [], f"{ticker}: numeric leakage in {text!r}"


def test_real_records_carry_no_capital_priority_conclusion():
    """A structural sanity check on the real corpus mirroring CONTENDER-
    0003 SS G's own restated prohibition -- no promotion or comparative-
    superiority language anywhere in either real record's free text."""
    for ticker in ("VRT", "WMT"):
        data = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / f"{ticker}.yaml").read_text())
        for text in (
            data["archetype_assessment"]["rationale"],
            data["evidence_parity_finding"]["rationale"],
        ):
            assert cev._comparative_superiority_scan(text) == [], f"{ticker}: superiority language in {text!r}"
            assert cev._promotion_language_scan(text) == [], f"{ticker}: promotion language in {text!r}"


def test_real_records_reference_the_correct_comparator():
    vrt = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / "VRT.yaml").read_text())
    wmt = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / "WMT.yaml").read_text())
    assert vrt["canonical_comparator_symbol"] == "GEV"
    assert wmt["canonical_comparator_symbol"] == "COST"


def test_real_manifest_reconciles_against_real_records():
    result = cev.validate_cohort_manifest(
        REPO_ROOT / "intelligence" / "contender_evaluation" / "COHORT_MANIFEST.yaml",
        REPO_ROOT / "intelligence" / "contender_evaluation",
    )
    assert result.valid, result.errors


def test_hashes_are_deterministic_across_repeated_calls():
    for ticker in ("VRT", "WMT"):
        data = yaml.safe_load((REPO_ROOT / "intelligence" / "contender_evaluation" / f"{ticker}.yaml").read_text())
        h1 = cev.canonical_record_hash(data)
        h2 = cev.canonical_record_hash(data)
        assert h1 == h2 == data["content_sha256"]
