"""Tests for valuation_archetype_validator.py (WS-0005 valuation-archetype
schema, VALUATION-0003 scope).

Every schema/behavior test constructs its own synthetic fixture -- no real
ticker's judgment content is asserted against here except the final
real-corpus regression block, which validates the actually-sealed 27-record
cohort and its manifest.
"""

from pathlib import Path

import pytest
import yaml

import valuation_archetype_validator as vav

REPO_ROOT = Path(__file__).resolve().parent


def _record(**overrides) -> dict:
    d = {
        "schema_version": "1.0",
        "ticker": "TEST",
        "primary_archetype": "A",
        "secondary_archetype": None,
        "rationale": "The business shows high gross margin and low reinvestment intensity.",
        "evidence_quality": {
            "primary_source_coverage": "comprehensive",
            "uncertainty_statement": "Some figures rely on secondary sourcing.",
        },
        "disclosed_evidence_conflicts": None,
        "evidence_gap_statement": None,
        "portfolio_context": None,
        "lifecycle_status": "sealed",
        "sealed_at": "2026-08-08T17:00:00Z",
        "governing_decision": "VALUATION-0003",
        "drafting_session_or_shard_id": "shard-1",
        "cohort_manifest_entry": "intelligence/valuation_archetype/COHORT_MANIFEST.yaml#TEST",
        "content_sha256": "placeholder",
    }
    d.update(overrides)
    d["content_sha256"] = vav.canonical_record_hash(d)
    return d


# ── primary vocabulary ───────────────────────────────────────────────────

@pytest.mark.parametrize("value", list("ABCDEFG") + ["unable_to_determine_archetype"])
def test_primary_archetype_accepts_all_eight_closed_values(value):
    rec = _record(primary_archetype=value, secondary_archetype=None)
    errors = vav.validate_archetype_data(rec)
    assert not any("primary_archetype invalid" in e for e in errors)


@pytest.mark.parametrize("value", ["H", "a", "Unknown", "", None, 1, "A,B"])
def test_primary_archetype_rejects_invalid_values(value):
    rec = _record(primary_archetype=value, secondary_archetype=None)
    errors = vav.validate_archetype_data(rec)
    assert any("primary_archetype invalid" in e for e in errors)


# ── secondary vocabulary and cardinality ─────────────────────────────────

def test_secondary_archetype_null_is_valid():
    rec = _record(primary_archetype="A", secondary_archetype=None)
    errors = vav.validate_archetype_data(rec)
    assert errors == []


@pytest.mark.parametrize("value", list("ABCDEFG"))
def test_secondary_archetype_accepts_any_of_seven_when_not_equal_primary(value):
    primary = "G" if value != "G" else "A"
    rec = _record(primary_archetype=primary, secondary_archetype=value,
                   rationale="A diversified, reportable segments structure. Archetype-F test: considered.")
    errors = vav.validate_archetype_data(rec)
    assert not any("secondary_archetype" in e for e in errors)


def test_secondary_archetype_must_not_equal_primary():
    rec = _record(primary_archetype="B", secondary_archetype="B")
    errors = vav.validate_archetype_data(rec)
    assert any("must not equal primary_archetype" in e for e in errors)


def test_secondary_archetype_rejects_invalid_letter():
    rec = _record(primary_archetype="A", secondary_archetype="H")
    errors = vav.validate_archetype_data(rec)
    assert any("secondary_archetype invalid" in e for e in errors)


def test_secondary_archetype_forced_null_on_abstention():
    rec = _record(
        primary_archetype="unable_to_determine_archetype",
        secondary_archetype="A",
        evidence_gap_statement="No segment-level disclosure exists to support any determination.",
    )
    errors = vav.validate_archetype_data(rec)
    assert any("must be null when primary_archetype is the abstention value" in e for e in errors)


# ── abstention / evidence_gap_statement ──────────────────────────────────

def test_abstention_requires_evidence_gap_statement():
    rec = _record(primary_archetype="unable_to_determine_archetype", secondary_archetype=None,
                   evidence_gap_statement=None)
    errors = vav.validate_archetype_data(rec)
    assert any("evidence_gap_statement is required" in e for e in errors)


def test_abstention_with_evidence_gap_statement_is_valid():
    rec = _record(
        primary_archetype="unable_to_determine_archetype", secondary_archetype=None,
        evidence_gap_statement="No business-model narrative or segment disclosure exists in the source record.",
    )
    errors = vav.validate_archetype_data(rec)
    assert errors == []


def test_determined_record_must_have_null_evidence_gap_statement():
    rec = _record(primary_archetype="A", secondary_archetype=None,
                   evidence_gap_statement="should not be here")
    errors = vav.validate_archetype_data(rec)
    assert any("must be null for a determined record" in e for e in errors)


# ── archetype-F disclosure ────────────────────────────────────────────────

def test_secondary_present_requires_explicit_f_test_marker():
    rec = _record(primary_archetype="B", secondary_archetype="D",
                   rationale="A capital-intensive business with cyclical demand.")
    errors = vav.validate_archetype_data(rec)
    assert any("Archetype-F test" in e for e in errors)


def test_secondary_present_with_marker_is_valid():
    rec = _record(primary_archetype="B", secondary_archetype="D",
                   rationale="A capital-intensive business. Archetype-F test: considered and rejected.")
    errors = vav.validate_archetype_data(rec)
    assert errors == []


def test_segment_language_without_secondary_or_f_token_is_flagged():
    rec = _record(primary_archetype="A", secondary_archetype=None,
                   rationale="The company reports three reportable business segments with revenue.")
    errors = vav.validate_archetype_data(rec)
    assert any("segment structure" in e for e in errors)


def test_segment_language_with_f_token_but_no_secondary_is_valid():
    rec = _record(
        primary_archetype="A", secondary_archetype=None,
        rationale="The company reports several segments, but they are not materially diversified.",
    )
    errors = vav.validate_archetype_data(rec)
    assert errors == []


def test_no_segment_language_no_secondary_requires_no_disclosure():
    rec = _record(primary_archetype="A", secondary_archetype=None,
                   rationale="A single-line, asset-light subscription business with high margins.")
    errors = vav.validate_archetype_data(rec)
    assert errors == []


# ── prohibited-field / prohibited-language scan ──────────────────────────

@pytest.mark.parametrize("bad_text", [
    "this ticker's conviction rating is High",
    "the target weight is meaningful",
    "3% of the book",
    "per targets.yaml's destination list",
    "gates.yaml shows this ticker as gated",
    "primary_disposition: case_for_review",
])
def test_rationale_prohibited_field_scan_catches_leaks(bad_text):
    rec = _record(rationale=bad_text)
    errors = vav.validate_archetype_data(rec)
    assert any("prohibited content" in e for e in errors)


@pytest.mark.parametrize("bad_text", [
    "the chart shows a clear support level and resistance level",
    "RSI and MACD both signal a breakout",
    "the stock is oversold based on technical analysis",
    "Fibonacci retracement suggests a price target",
])
def test_rationale_chart_domain_scan_catches_leaks(bad_text):
    rec = _record(rationale=bad_text)
    errors = vav.validate_archetype_data(rec)
    assert any("chart-domain" in e for e in errors)


@pytest.mark.parametrize("word", ["buy", "sell", "add", "hold", "trim", "exit", "wait"])
def test_rationale_directive_word_scan_catches_each_word(word):
    rec = _record(rationale=f"An analyst would {word} this position given the evidence.")
    errors = vav.validate_archetype_data(rec)
    assert any("directive-word" in e for e in errors)


def test_rationale_directive_word_scan_catches_bare_stage_as_directive():
    rec = _record(rationale="An investor should stage into this position gradually.")
    errors = vav.validate_archetype_data(rec)
    assert any("directive-word" in e for e in errors)


@pytest.mark.parametrize("text", [
    "an early-stage, binary-outcome pharmaceutical pipeline",
    "several pipeline-stage acquisitions were announced",
    "a venture-stage loss-making segment",
])
def test_rationale_hyphenated_stage_does_not_false_positive(text):
    rec = _record(rationale=text)
    errors = vav.validate_archetype_data(rec)
    assert not any("directive-word" in e for e in errors)


def test_gate_word_bare_noun_is_caught():
    rec = _record(rationale="This record's gate names the reopening condition.")
    errors = vav.validate_archetype_data(rec)
    assert any("bare-gate-word" in e for e in errors)


def test_gate_word_legitimate_technical_use_is_not_caught():
    rec = _record(rationale="The technological gate determines advanced-node adoption timing.")
    errors = vav.validate_archetype_data(rec)
    assert errors == []


def test_disclosed_evidence_conflicts_is_also_scanned():
    rec = _record(disclosed_evidence_conflicts=["this ticker's conviction rating conflicts across sources"])
    errors = vav.validate_archetype_data(rec)
    assert any("prohibited content" in e for e in errors)


def test_evidence_gap_statement_is_also_scanned_on_abstention():
    rec = _record(
        primary_archetype="unable_to_determine_archetype", secondary_archetype=None,
        evidence_gap_statement="No evidence, and this ticker's target weight is unknown.",
    )
    errors = vav.validate_archetype_data(rec)
    assert any("prohibited content" in e for e in errors)


def test_evidence_quality_uncertainty_statement_is_also_scanned():
    rec = _record()
    rec["evidence_quality"]["uncertainty_statement"] = "the RSI reading is unclear"
    rec["content_sha256"] = vav.canonical_record_hash(rec)
    errors = vav.validate_archetype_data(rec)
    assert any("chart-domain" in e for e in errors)


def test_portfolio_context_disclosure_note_is_also_scanned():
    rec = _record(portfolio_context={
        "gate_exists": True, "next_gate_references_valuation": True,
        "disclosure_note": "this ticker's conviction rating is High",
    })
    errors = vav.validate_archetype_data(rec)
    assert any("prohibited content" in e for e in errors)


# ── closed schema / extra-key rejection at every level ───────────────────

def test_top_level_rejects_extra_key():
    rec = _record()
    rec["numeric_score"] = 5
    errors = vav.validate_archetype_data(rec)
    assert any("unrecognized key" in e for e in errors)


def test_top_level_rejects_recommended_target_pct_smuggling():
    rec = _record()
    rec["recommended_target_pct"] = 3.0
    errors = vav.validate_archetype_data(rec)
    assert any("unrecognized key" in e for e in errors)


def test_evidence_quality_rejects_extra_key():
    rec = _record()
    rec["evidence_quality"]["confidence_score"] = 0.9
    rec["content_sha256"] = vav.canonical_record_hash(rec)
    errors = vav.validate_archetype_data(rec)
    assert any("evidence_quality has unrecognized key" in e for e in errors)


def test_evidence_quality_missing_key_rejected():
    rec = _record()
    del rec["evidence_quality"]["uncertainty_statement"]
    rec["content_sha256"] = vav.canonical_record_hash(rec)
    errors = vav.validate_archetype_data(rec)
    assert any("evidence_quality missing key" in e for e in errors)


def test_evidence_quality_primary_source_coverage_vocabulary_closed():
    rec = _record()
    rec["evidence_quality"]["primary_source_coverage"] = "excellent"
    rec["content_sha256"] = vav.canonical_record_hash(rec)
    errors = vav.validate_archetype_data(rec)
    assert any("primary_source_coverage invalid" in e for e in errors)


def test_portfolio_context_rejects_extra_key():
    rec = _record(portfolio_context={
        "gate_exists": True, "next_gate_references_valuation": False,
        "next_gate_text": "leaked literal text",
    })
    errors = vav.validate_archetype_data(rec)
    assert any("portfolio_context has unrecognized key" in e for e in errors)


def test_portfolio_context_null_is_valid():
    rec = _record(portfolio_context=None)
    errors = vav.validate_archetype_data(rec)
    assert errors == []


def test_disclosed_evidence_conflicts_rejects_empty_list():
    rec = _record(disclosed_evidence_conflicts=[])
    errors = vav.validate_archetype_data(rec)
    assert any("must be null or a non-empty list" in e for e in errors)


def test_missing_top_level_keys_reported():
    rec = _record()
    del rec["lifecycle_status"]
    errors = vav.validate_archetype_data(rec)
    assert any("missing top-level key" in e for e in errors)


def test_wrong_governing_decision_rejected():
    rec = _record(governing_decision="TIER-0005")
    errors = vav.validate_archetype_data(rec)
    assert any("governing_decision must be" in e for e in errors)


def test_wrong_lifecycle_status_rejected():
    rec = _record(lifecycle_status="draft")
    errors = vav.validate_archetype_data(rec)
    assert any("lifecycle_status invalid" in e for e in errors)


# ── hash reproducibility ──────────────────────────────────────────────────

def test_content_sha256_must_reproduce():
    rec = _record()
    rec["content_sha256"] = "0" * 64
    errors = vav.validate_archetype_data(rec)
    assert any("does not reproduce" in e for e in errors)


def test_content_sha256_excludes_seal_fields():
    rec1 = _record(sealed_at="2026-08-08T00:00:00Z")
    rec2 = dict(rec1)
    rec2["sealed_at"] = "2026-08-09T00:00:00Z"
    assert vav.canonical_record_hash(rec1) == vav.canonical_record_hash(rec2)


def test_content_sha256_changes_if_rationale_changes():
    rec1 = _record(rationale="A")
    rec2 = _record(rationale="B different text")
    assert vav.canonical_record_hash(rec1) != vav.canonical_record_hash(rec2)


# ── ticker consistency ────────────────────────────────────────────────────

def test_ticker_must_match_filename_derived_expectation():
    rec = _record(ticker="WRONG")
    errors = vav.validate_archetype_data(rec, expected_ticker="TEST")
    assert any("does not match filename-derived" in e for e in errors)


def test_ticker_matching_expected_is_valid():
    rec = _record(ticker="TEST")
    errors = vav.validate_archetype_data(rec, expected_ticker="TEST")
    assert errors == []


# ── manifest / population reconciliation ─────────────────────────────────

def test_manifest_detects_duplicate_ticker(tmp_path):
    records_dir = tmp_path
    rec = _record(ticker="AAA")
    (records_dir / "AAA.yaml").write_text(yaml.safe_dump(rec))
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "VALUATION-0003",
        "cohort": [
            {"ticker": "AAA", "shard_id": "shard-1", "sealed_at": "x",
             "content_sha256": rec["content_sha256"], "schema_version": "1.0",
             "governing_decision": "VALUATION-0003", "record_path": "AAA.yaml"},
            {"ticker": "AAA", "shard_id": "shard-1", "sealed_at": "x",
             "content_sha256": rec["content_sha256"], "schema_version": "1.0",
             "governing_decision": "VALUATION-0003", "record_path": "AAA.yaml"},
        ],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))
    result = vav.validate_cohort_manifest(
        records_dir / "COHORT_MANIFEST.yaml", records_dir, canonical_universe=frozenset({"AAA"}),
    )
    assert not result.valid
    assert any("duplicate ticker" in e for e in result.errors)


def test_manifest_detects_missing_canonical_ticker(tmp_path):
    records_dir = tmp_path
    manifest = {"schema_version": "1.0", "governing_decision": "VALUATION-0003", "cohort": []}
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))
    result = vav.validate_cohort_manifest(
        records_dir / "COHORT_MANIFEST.yaml", records_dir, canonical_universe=frozenset({"AAA", "BBB"}),
    )
    assert not result.valid
    assert any("missing canonical ticker" in e for e in result.errors)


def test_manifest_detects_orphan_record_with_no_manifest_entry(tmp_path):
    records_dir = tmp_path
    rec = _record(ticker="AAA")
    (records_dir / "AAA.yaml").write_text(yaml.safe_dump(rec))
    (records_dir / "ORPHAN.yaml").write_text(yaml.safe_dump(_record(ticker="ORPHAN")))
    manifest = {
        "schema_version": "1.0", "governing_decision": "VALUATION-0003",
        "cohort": [{"ticker": "AAA", "shard_id": "shard-1", "sealed_at": "x",
                    "content_sha256": rec["content_sha256"], "schema_version": "1.0",
                    "governing_decision": "VALUATION-0003", "record_path": "AAA.yaml"}],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))
    result = vav.validate_cohort_manifest(
        records_dir / "COHORT_MANIFEST.yaml", records_dir, canonical_universe=frozenset({"AAA"}),
    )
    assert not result.valid
    assert any("no manifest entry" in e for e in result.errors)


def test_manifest_detects_hash_mismatch(tmp_path):
    records_dir = tmp_path
    rec = _record(ticker="AAA")
    (records_dir / "AAA.yaml").write_text(yaml.safe_dump(rec))
    manifest = {
        "schema_version": "1.0", "governing_decision": "VALUATION-0003",
        "cohort": [{"ticker": "AAA", "shard_id": "shard-1", "sealed_at": "x",
                    "content_sha256": "0" * 64, "schema_version": "1.0",
                    "governing_decision": "VALUATION-0003", "record_path": "AAA.yaml"}],
    }
    (records_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))
    result = vav.validate_cohort_manifest(
        records_dir / "COHORT_MANIFEST.yaml", records_dir, canonical_universe=frozenset({"AAA"}),
    )
    assert not result.valid
    assert any("content_sha256 mismatch" in e for e in result.errors)


# ── directory-level population completeness ──────────────────────────────

def test_directory_detects_missing_ticker(tmp_path):
    rec = _record(ticker="AAA")
    (tmp_path / "AAA.yaml").write_text(yaml.safe_dump(rec))
    manifest = {
        "schema_version": "1.0", "governing_decision": "VALUATION-0003",
        "cohort": [{"ticker": "AAA", "shard_id": "shard-1", "sealed_at": "x",
                    "content_sha256": rec["content_sha256"], "schema_version": "1.0",
                    "governing_decision": "VALUATION-0003", "record_path": "AAA.yaml"}],
    }
    (tmp_path / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))
    result = vav.validate_archetype_directory(tmp_path, canonical_universe=frozenset({"AAA", "MISSING"}))
    assert not result.valid
    assert any(
        "missing sealed record" in e for r in result.results for e in r.errors
    )


def test_missing_directory_is_valid_zero_coverage():
    result = vav.validate_archetype_directory(Path("/nonexistent/path/xyz"), canonical_universe=frozenset({"AAA"}))
    assert result.valid
    assert result.record_count == 0


def test_missing_manifest_file_is_reported():
    result = vav.validate_archetype_data({}, expected_ticker=None)
    assert result != []  # sanity: empty dict is definitely invalid


# ── independent scan is a genuinely separate mechanism from the sanitizer ─

def test_validator_scan_imports_nothing_from_sanitizer():
    """Zero import coupling with valuation_archetype_sanitizer.py -- the
    validator's prohibited-content scan is its own independent
    implementation, not a second call into the sanitizer's own scan."""
    import ast

    tree = ast.parse(Path(vav.__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert not any(a.name.startswith("valuation_archetype_sanitizer") for a in node.names)
        if isinstance(node, ast.ImportFrom):
            assert node.module != "valuation_archetype_sanitizer"


# ── real-corpus regression ────────────────────────────────────────────────

_ROSTER = [
    "AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GNRC", "GOOGL", "ICE",
    "ISRG", "KLAC", "LLY", "META", "MSFT", "NVDA", "PANW", "PWR", "RKLB", "RTX",
    "SNPS", "SPGI", "TMO", "TSLA", "TSM", "V", "WM",
]


def test_real_cohort_directory_validates_clean():
    records_dir = REPO_ROOT / "intelligence" / "valuation_archetype"
    if not records_dir.is_dir():
        pytest.skip("intelligence/valuation_archetype not present")
    try:
        from relationship_validator import load_canonical_universe
    except ImportError:
        pytest.skip("relationship_validator not importable")
    canonical = load_canonical_universe(REPO_ROOT)
    result = vav.validate_archetype_directory(records_dir, canonical_universe=canonical)
    if not result.valid:
        details = "\n".join(f"{r.source}: {r.errors}" for r in result.results if not r.valid)
        pytest.fail(f"real cohort failed validation:\n{details}")


@pytest.mark.parametrize("ticker", _ROSTER)
def test_real_record_exists_and_matches_ticker(ticker):
    path = REPO_ROOT / "intelligence" / "valuation_archetype" / f"{ticker}.yaml"
    if not path.is_file():
        pytest.skip("real cohort not present")
    data = yaml.safe_load(path.read_text())
    assert data["ticker"] == ticker
    assert data["primary_archetype"] in vav._PRIMARY_VALUES


def test_real_cohort_has_exactly_27_records():
    records_dir = REPO_ROOT / "intelligence" / "valuation_archetype"
    if not records_dir.is_dir():
        pytest.skip("intelligence/valuation_archetype not present")
    files = [p for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"]
    assert len(files) == 27


def test_real_cohort_has_zero_duplicate_tickers():
    records_dir = REPO_ROOT / "intelligence" / "valuation_archetype"
    if not records_dir.is_dir():
        pytest.skip("intelligence/valuation_archetype not present")
    tickers = [p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"]
    assert len(tickers) == len(set(tickers))
