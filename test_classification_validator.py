"""Tests for classification_validator.py (WS-0005 Milestone 6 blind-
classification schema, TIER-0002/TIER-0004/TIER-0005 scope).

Every schema/behavior test below constructs its own synthetic fixture --
no real ticker's judgment content is asserted against in this file, same
authorized-scope discipline test_intelligence_validator.py and
test_relationship_validator.py already follow. The directory-scan tests
exercise the real repository's intelligence/classification/ directory,
authored under this one implementation PR.
"""

from pathlib import Path

import pytest
import yaml

import classification_validator as cv


# ── fixtures ─────────────────────────────────────────────────────────────

def _economic_role(**overrides) -> dict:
    role = {
        "economic_system_ref": "AI & Compute Infrastructure",
        "company_role": "compute",
        "role_basis": "Synthetic 10-K segment description, synthetic fiscal year.",
    }
    role.update(overrides)
    return role


def _capital_priority(**overrides) -> dict:
    cp = {
        "status": "maintain_current_weight",
        "comparator_set": ["AAA", "BBB"],
        "rationale": "Synthetic rationale, narrow and evidence-based.",
        "assessed_date": "2026-08-05",
        "assessing_record": None,
    }
    cp.update(overrides)
    return cp


def _risk_concentration(**overrides) -> dict:
    rc = {
        "cluster_cap_membership": [],
        "issuer_lookthrough_membership": False,
        "relationship_record_coverage": [],
        "unmeasured_flag": True,
        "notes": "",
    }
    rc.update(overrides)
    return rc


def _evidence_quality(**overrides) -> dict:
    eq = {
        "primary_source_coverage": "comprehensive",
        "highest_disclosed_risk_severity": "moderate",
        "thesis_uncertainty_statement": "Synthetic uncertainty statement.",
        "review_trigger_notes": "",
    }
    eq.update(overrides)
    return eq


def _record(*, sealed: bool = False, ticker: str = "ZZZZ", **axis_overrides) -> dict:
    data = {
        "schema_version": "1.0",
        "ticker": ticker,
        "economic_role": axis_overrides.get("economic_role", _economic_role()),
        "capital_priority": axis_overrides.get("capital_priority", _capital_priority()),
        "risk_concentration": axis_overrides.get("risk_concentration", _risk_concentration()),
        "evidence_quality": axis_overrides.get("evidence_quality", _evidence_quality()),
        "lifecycle_status": "draft",
    }
    if sealed:
        data["lifecycle_status"] = "sealed"
        data["sealed_at"] = "2026-08-05T00:00:00Z"
        data["governing_decision"] = "TIER-0005"
        data["drafting_session_or_shard_id"] = "shard-test"
        data["cohort_manifest_entry"] = "intelligence/classification/COHORT_MANIFEST.yaml#ZZZZ"
        data["content_sha256"] = cv.canonical_record_hash(data)
    return data


# ── valid record ─────────────────────────────────────────────────────────

def test_valid_draft_record_passes():
    result = cv.validate_classification_data(_record())
    assert result.valid, result.errors


def test_valid_sealed_record_passes():
    result = cv.validate_classification_data(_record(sealed=True))
    assert result.valid, result.errors


# ── missing axis ─────────────────────────────────────────────────────────

def test_missing_axis_fails():
    data = _record()
    del data["risk_concentration"]
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("risk_concentration" in e for e in result.errors)


# ── invalid enum ─────────────────────────────────────────────────────────

def test_invalid_economic_system_ref_fails():
    data = _record(economic_role=_economic_role(economic_system_ref="Not A Real System"))
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("economic_system_ref" in e for e in result.errors)


def test_invalid_capital_priority_status_fails():
    data = _record(capital_priority=_capital_priority(status="buy_more"))
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("capital_priority.status" in e for e in result.errors)


def test_other_escape_economic_system_ref_valid():
    data = _record(economic_role=_economic_role(economic_system_ref="other: Materials & Industrials"))
    result = cv.validate_classification_data(data)
    assert result.valid, result.errors


# ── missing required field ──────────────────────────────────────────────

def test_missing_role_basis_fails():
    role = _economic_role()
    del role["role_basis"]
    result = cv.validate_classification_data(_record(economic_role=role))
    assert not result.valid
    assert any("role_basis" in e for e in result.errors)


def test_missing_thesis_uncertainty_statement_fails():
    eq = _evidence_quality()
    eq["thesis_uncertainty_statement"] = ""
    result = cv.validate_classification_data(_record(evidence_quality=eq))
    assert not result.valid
    assert any("thesis_uncertainty_statement" in e for e in result.errors)


# ── unable_to_determine abstention ──────────────────────────────────────

def test_unable_to_determine_without_abstention_reason_fails():
    role = _economic_role(
        economic_system_ref=cv.ECONOMIC_SYSTEM_ABSTENTION_VALUE,
        evidence_gap_statement="Specific gap statement.",
    )
    result = cv.validate_classification_data(_record(economic_role=role))
    assert not result.valid
    assert any("abstention_reason" in e for e in result.errors)


def test_unable_to_determine_without_evidence_gap_statement_fails():
    role = _economic_role(
        economic_system_ref=cv.ECONOMIC_SYSTEM_ABSTENTION_VALUE,
        abstention_reason="Specific reason.",
    )
    result = cv.validate_classification_data(_record(economic_role=role))
    assert not result.valid
    assert any("evidence_gap_statement" in e for e in result.errors)


def test_valid_unable_to_determine_passes():
    role = _economic_role(
        economic_system_ref=cv.ECONOMIC_SYSTEM_ABSTENTION_VALUE,
        abstention_reason="Disclosed segments span two systems with no evident dominant driver.",
        evidence_gap_statement="A primary-source segment-revenue breakdown would resolve this.",
    )
    result = cv.validate_classification_data(_record(economic_role=role))
    assert result.valid, result.errors


def test_abstention_fields_forbidden_on_determined_record():
    role = _economic_role(abstention_reason="should not be here")
    result = cv.validate_classification_data(_record(economic_role=role))
    assert not result.valid
    assert any("abstention_reason must be absent" in e for e in result.errors)


def test_abstention_does_not_cascade_to_capital_priority():
    # A ticker abstaining on economic_role may still seal a fully-assessed
    # capital_priority -- TIER-0004 Sec6/Sec12.3's non-cascading rule.
    role = _economic_role(
        economic_system_ref=cv.ECONOMIC_SYSTEM_ABSTENTION_VALUE,
        abstention_reason="Reason.",
        evidence_gap_statement="Gap.",
    )
    result = cv.validate_classification_data(
        _record(economic_role=role, capital_priority=_capital_priority(status="case_for_review"))
    )
    assert result.valid, result.errors


# ── numeric score / target_pct leakage ──────────────────────────────────

def test_invalid_numeric_score_top_level_field_fails():
    data = _record()
    data["conviction_score"] = 7.5
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("unexpected top-level field" in e for e in result.errors)


def test_target_pct_leakage_in_capital_priority_fails():
    cp = _capital_priority()
    cp["target_pct"] = 5.0
    result = cv.validate_classification_data(_record(capital_priority=cp))
    assert not result.valid
    assert any("target_pct" in e for e in result.errors)


def test_target_pct_shaped_rationale_fails():
    cp = _capital_priority(rationale="This ticker deserves 5.0% of book as its new target.")
    result = cv.validate_classification_data(_record(capital_priority=cp))
    assert not result.valid
    assert any("rationale must not contain" in e for e in result.errors)


def test_portfolio_role_ref_leakage_in_economic_role_fails():
    role = _economic_role()
    role["portfolio_role_ref"] = "T1"
    result = cv.validate_classification_data(_record(economic_role=role))
    assert not result.valid
    assert any("portfolio_role_ref" in e for e in result.errors)


def test_conviction_leakage_in_capital_priority_fails():
    cp = _capital_priority()
    cp["conviction"] = "High"
    result = cv.validate_classification_data(_record(capital_priority=cp))
    assert not result.valid
    assert any("conviction" in e for e in result.errors)


def test_tier_policy_leakage_via_gates_field_fails():
    role = _economic_role()
    role["gates"] = "cash_pending_clearance"
    result = cv.validate_classification_data(_record(economic_role=role))
    assert not result.valid
    assert any("gates" in e for e in result.errors)


def test_issuer_lookthrough_permitted_in_risk_concentration_but_not_elsewhere():
    # risk_concentration legitimately carries cluster/issuer_lookthrough
    # cross-reference content -- must not be flagged there.
    rc = _risk_concentration(
        cluster_cap_membership=["semis"],
        issuer_lookthrough_membership=True,
        unmeasured_flag=False,
    )
    result = cv.validate_classification_data(_record(risk_concentration=rc))
    assert result.valid, result.errors


# ── chart-domain leakage ────────────────────────────────────────────────

def test_chart_domain_top_level_axis_field_rejected():
    # Chart-domain content could only ever appear as a stray fifth
    # top-level axis (e.g. a "chart_evidence" block) -- caught by the same
    # no-fifth-axis structural check as any other unauthorized top-level
    # field. Mid-record chart *prose* leakage is the sanitizer's job
    # (intelligence_classification_sanitizer.py's defensive chart-domain
    # scan), not this validator's -- this validator checks sealed-record
    # shape, not free-text provenance.
    data = _record()
    data["chart_evidence"] = {"support_level": 123.45}
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("unexpected top-level field" in e and "chart_evidence" in e for e in result.errors)


# ── invalid lifecycle state ──────────────────────────────────────────────

def test_invalid_lifecycle_status_fails():
    data = _record()
    data["lifecycle_status"] = "finalized"
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("lifecycle_status" in e for e in result.errors)


def test_sealed_record_missing_seal_field_fails():
    data = _record(sealed=True)
    del data["governing_decision"]
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("missing required seal field" in e for e in result.errors)


# ── hash reproducibility ────────────────────────────────────────────────

def test_incorrect_record_hash_fails():
    data = _record(sealed=True)
    data["content_sha256"] = "0" * 64
    result = cv.validate_classification_data(data)
    assert not result.valid
    assert any("content_sha256 does not reproduce" in e for e in result.errors)


def test_hash_excludes_seal_block():
    a = _record(sealed=True, ticker="AAAA")
    b = dict(a)
    b["sealed_at"] = "2099-01-01T00:00:00Z"
    b["drafting_session_or_shard_id"] = "a-totally-different-shard"
    # hash computed from the four axes + ticker only -- changing seal
    # metadata alone must not change the recomputed hash.
    assert cv.canonical_record_hash(a) == cv.canonical_record_hash(b)


def test_hash_changes_when_judgment_content_changes():
    a = _record(sealed=True, ticker="AAAA")
    b = _record(ticker="AAAA", economic_role=_economic_role(company_role="a different role"))
    assert cv.canonical_record_hash(a) != cv.canonical_record_hash(b)


# ── cohort manifest ──────────────────────────────────────────────────────

def test_manifest_missing_ticker_detected():
    rec = _record(sealed=True, ticker="AAAA")
    manifest = {"cohort": []}
    result = cv.validate_cohort_manifest(
        manifest, {"AAAA": rec}, canonical_universe=frozenset({"AAAA"}),
    )
    assert not result.valid
    assert any("orphan" in e.lower() or "no corresponding cohort manifest entry" in e for e in result.errors)


def test_manifest_duplicate_ticker_detected():
    rec = _record(sealed=True, ticker="AAAA")
    row = {
        "ticker": "AAAA", "shard_id": "s", "sealed_at": rec["sealed_at"],
        "content_sha256": rec["content_sha256"], "schema_version": "1.0",
        "governing_decision": "TIER-0005", "record_path": "intelligence/classification/AAAA.yaml",
    }
    manifest = {"cohort": [row, dict(row)]}
    result = cv.validate_cohort_manifest(manifest, {"AAAA": rec})
    assert not result.valid
    assert any("more than once" in e for e in result.errors)


def test_manifest_extra_ticker_outside_population_detected():
    rec = _record(sealed=True, ticker="ZZZZ")
    row = {
        "ticker": "ZZZZ", "shard_id": "s", "sealed_at": rec["sealed_at"],
        "content_sha256": rec["content_sha256"], "schema_version": "1.0",
        "governing_decision": "TIER-0005", "record_path": "intelligence/classification/ZZZZ.yaml",
    }
    manifest = {"cohort": [row]}
    result = cv.validate_cohort_manifest(
        manifest, {"ZZZZ": rec}, canonical_universe=frozenset({"AAAA"}),
    )
    assert not result.valid
    assert any("outside the authorized 27-name population" in e for e in result.errors)


def test_manifest_record_pointer_mismatch_detected():
    rec = _record(sealed=True, ticker="AAAA")
    row = {
        "ticker": "AAAA", "shard_id": "s", "sealed_at": rec["sealed_at"],
        "content_sha256": "f" * 64,  # wrong hash
        "schema_version": "1.0", "governing_decision": "TIER-0005",
        "record_path": "intelligence/classification/AAAA.yaml",
    }
    manifest = {"cohort": [row]}
    result = cv.validate_cohort_manifest(manifest, {"AAAA": rec})
    assert not result.valid
    assert any("content_sha256 mismatch" in e for e in result.errors)


# ── extra/missing ticker in a directory scan (synthetic tmp_path) ───────

def test_directory_scan_missing_directory_is_valid_zero_coverage(tmp_path):
    result = cv.validate_classification_directory(tmp_path / "does-not-exist")
    assert result.valid
    assert result.record_count == 0


def test_directory_scan_requires_manifest_when_records_exist(tmp_path):
    rec = _record(sealed=True, ticker="AAAA")
    (tmp_path / "AAAA.yaml").write_text(yaml.safe_dump(rec))
    result = cv.validate_classification_directory(tmp_path)
    assert not result.valid
    assert any("COHORT_MANIFEST.yaml is required" in e for e in result.results[-1].errors)


def test_filename_ticker_mismatch_detected(tmp_path):
    rec = _record(sealed=True, ticker="AAAA")
    (tmp_path / "BBBB.yaml").write_text(yaml.safe_dump(rec))
    result = cv.validate_classification_file(tmp_path / "BBBB.yaml")
    assert not result.valid
    assert any("does not match the record's own ticker" in e for e in result.errors)


# ── isolation: zero import coupling with allocate.py / margin_state.py ──

def test_module_source_never_imports_allocator_or_margin():
    source = Path("classification_validator.py").read_text()
    assert "import allocate" not in source
    assert "from allocate" not in source
    assert "import margin_state" not in source
    assert "from margin_state" not in source


def test_sanitizer_module_never_imports_allocator_or_margin():
    source = Path("intelligence_classification_sanitizer.py").read_text()
    assert "import allocate" not in source
    assert "from allocate" not in source
    assert "import margin_state" not in source
    assert "from margin_state" not in source


# ── real repository: intelligence/classification/ directory (this PR) ───

def test_real_repository_classification_directory_valid_if_present():
    import relationship_validator as rv
    repo_root = Path(__file__).resolve().parent
    canonical = rv.load_canonical_universe(repo_root)
    result = cv.validate_classification_directory(
        repo_root / "intelligence" / "classification", canonical_universe=canonical,
    )
    assert result.valid, [
        (r.source, r.errors) for r in result.results if not r.valid
    ]
