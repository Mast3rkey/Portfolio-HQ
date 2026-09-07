"""Package-integrity tests for the CHART-0002 Batch 1 evidence packages
(governance/evidence/CHART-0002/<ticker>-daily-2026-08-01/, 19 tickers,
daily 1D timeframe only, Stage 1 only).

These tests verify each retained package's internal consistency (file
count, hash reconciliation, required fields, fact/interpretation
separation, and the draft-stage governance invariants CHART-0002 requires)
plus cohort-level completeness (the immutable 19-name/1D cohort, shard
union, no Stage 2 record) -- they do not import or couple to allocate.py,
margin_state.py, levels.py, intelligence_validator.py, dashboard code, or
brokerage code, matching this batch's own no-coupling scope.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

CHART_0002_ROOT = Path(__file__).parent / "governance" / "evidence" / "CHART-0002"
COHORT_MANIFEST_PATH = CHART_0002_ROOT / "COHORT_BATCH1_19_DAILY.yaml"

TICKERS = [
    "AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GOOGL", "ISRG",
    "KLAC", "LLY", "META", "MSFT", "NVDA", "PANW", "PWR", "TMO", "TSM", "V",
]

SHARDS = {
    "shard_1": ["AMZN", "ASML", "AVGO", "CEG", "COST"],
    "shard_2": ["ETN", "GEV", "GOOGL", "ISRG", "KLAC"],
    "shard_3": ["LLY", "META", "MSFT", "NVDA", "PANW"],
    "shard_4": ["PWR", "TMO", "TSM", "V"],
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _pkg_dir(ticker: str) -> Path:
    return CHART_0002_ROOT / f"{ticker.lower()}-daily-2026-08-01"


def _record(ticker: str) -> dict:
    with open(_pkg_dir(ticker) / "record.yaml") as f:
        return yaml.safe_load(f)


def _manifest(ticker: str) -> dict:
    with open(_pkg_dir(ticker) / "MANIFEST.json") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def cohort() -> dict:
    with open(COHORT_MANIFEST_PATH) as f:
        return yaml.safe_load(f)


# ── cohort shape ─────────────────────────────────────────────────────────

def test_cohort_manifest_parses(cohort):
    assert isinstance(cohort, dict)


def test_cohort_has_exactly_19_tickers(cohort):
    assert cohort["ticker_count"] == 19
    assert cohort["tickers"] == TICKERS
    assert len(set(cohort["tickers"])) == 19


def test_cohort_timeframe_is_1d_only(cohort):
    assert cohort["timeframe"] == "1D"


def test_cohort_shards_match_expected(cohort):
    assert cohort["shards"] == SHARDS


def test_union_of_shards_equals_cohort_no_dup_no_missing_no_extra(cohort):
    union = [t for shard in SHARDS.values() for t in shard]
    assert sorted(union) == sorted(TICKERS)
    assert len(union) == len(set(union)) == 19
    assert set(union) == set(cohort["tickers"])


def test_no_extra_package_directories_beyond_the_19():
    subdirs = sorted(p.name for p in CHART_0002_ROOT.iterdir() if p.is_dir())
    expected = sorted(f"{t.lower()}-daily-2026-08-01" for t in TICKERS)
    assert subdirs == expected


def test_cohort_packages_list_matches_19_tickers(cohort):
    pkg_tickers = sorted(p["ticker"] for p in cohort["packages"])
    assert pkg_tickers == sorted(TICKERS)
    assert len(cohort["packages"]) == 19


def test_cohort_marks_stage_1_only_no_stage_2(cohort):
    assert cohort["stage"] == "Stage 1 only"
    assert "not" in cohort["stage_2_status"].lower()


def test_cohort_privacy_summary_all_19_username_exception(cohort):
    priv = cohort["privacy"]
    assert priv["reviewed_images"] == 19
    assert priv["username_exception_images"] == 19
    assert priv["redacted_images"] == 0
    assert priv["other_privacy_issue_images"] == 0


def test_cohort_layer_a_preflight_clean(cohort):
    layer_a = cohort["layer_a_preflight"]
    assert layer_a["result"] == "clean"
    assert layer_a["errors"] == 0
    assert layer_a["disk_file_count"] == 220
    assert layer_a["ticker_count"] == 55


def test_cohort_governed_consequence_none(cohort):
    assert cohort["governed_consequence"] == "none"
    assert cohort["portfolio_policy_effect"] == "none"


def test_cohort_git_lfs_not_used(cohort):
    assert cohort["retention"]["git_lfs_present"] is False
    assert cohort["retention"]["git_lfs_required"] is False


# ── per-package tests (parametrized across all 19 tickers) ─────────────

@pytest.mark.parametrize("ticker", TICKERS)
class TestPerPackage:
    def test_package_contains_exactly_one_image_plus_three_required_files(self, ticker):
        files = sorted(_pkg_dir(ticker).iterdir())
        names = {p.name for p in files}
        assert names == {f"{ticker}__2026-08-01__1D.png", "record.yaml", "MANIFEST.json", "README.md"}

    def test_record_yaml_and_manifest_json_parse(self, ticker):
        record = _record(ticker)
        manifest = _manifest(ticker)
        assert isinstance(record, dict)
        assert isinstance(manifest, dict)

    def test_record_has_required_top_level_sections(self, ticker):
        record = _record(ticker)
        for key in (
            "record_id", "identity_and_capture", "privacy_and_redaction",
            "content", "thesis_relationship", "prohibited_uses",
            "provenance", "lifecycle",
        ):
            assert key in record, f"{ticker} record.yaml missing required section: {key}"

    def test_ticker_and_timeframe_correct(self, ticker):
        record = _record(ticker)
        manifest = _manifest(ticker)
        ident = record["identity_and_capture"]
        assert ident["ticker"] == ticker
        assert ident["timeframe"] == "daily (1D)"
        assert manifest["ticker"] == ticker
        assert manifest["timeframe"] == "1D"

    def test_content_fields_are_separate_nonempty_lists(self, ticker):
        content = _record(ticker)["content"]
        for key in ("visible_facts", "observations", "inferences", "uncertainties"):
            assert key in content
            assert isinstance(content[key], list)
            assert len(content[key]) > 0
        lists = [content[k] for k in ("visible_facts", "observations", "inferences", "uncertainties")]
        assert len({id(lst) for lst in lists}) == 4

    def test_governed_consequence_is_none(self, ticker):
        record = _record(ticker)
        assert record["thesis_relationship"]["governed_consequence"] == "none"
        manifest = _manifest(ticker)
        assert manifest["governed_consequence"] == "none"

    def test_prohibited_uses_include_controlling_safeguards(self, ticker):
        record = _record(ticker)
        prohibited = " ".join(str(x).lower() for x in record["prohibited_uses"])
        for phrase in ("allocator", "ladder-0001", "intelligence", "score", "signal", "execution", "tier"):
            assert phrase in prohibited, f"{ticker}: prohibited_uses missing {phrase}"

    def test_retained_image_hash_matches_actual_file(self, ticker):
        img_path = _pkg_dir(ticker) / f"{ticker}__2026-08-01__1D.png"
        assert img_path.is_file()
        actual = _sha256(img_path)
        record = _record(ticker)
        manifest = _manifest(ticker)
        assert record["identity_and_capture"]["retained_image_sha256"] == actual
        assert manifest["retained_sha256"] == actual

    def test_source_and_retained_hashes_equal_no_redaction(self, ticker):
        """Batch 1 uses the explicit per-image username exception (no
        redaction) -- unlike CHART-0001's NVDA package, source and
        retained hashes must be IDENTICAL."""
        record = _record(ticker)
        manifest = _manifest(ticker)
        ident = record["identity_and_capture"]
        assert ident["governed_source_sha256"] == ident["retained_image_sha256"]
        assert manifest["governed_source_sha256"] == manifest["retained_sha256"]
        assert manifest["transformation_history"] == []

    def test_privacy_status_passed_with_username_exception(self, ticker):
        record = _record(ticker)
        manifest = _manifest(ticker)
        assert record["privacy_and_redaction"]["status"] == "passed"
        assert record["privacy_and_redaction"]["username_exception_applied"] is True
        assert record["privacy_and_redaction"]["redactions_applied"] == []
        assert manifest["username_exception_applied"] is True

    def test_privacy_note_discloses_formal_per_image_approval(self, ticker):
        record = _record(ticker)
        note = record["privacy_and_redaction"]["username_exception_note"].lower()
        assert "formal" in note
        assert "per-image" in note or "per image" in note
        assert "nichmasters" in note.lower() or "watermark/username" in note

    def test_no_other_privacy_issue_disclosed(self, ticker):
        record = _record(ticker)
        notes = record["privacy_and_redaction"]["privacy_review_notes"].lower()
        assert "no account balance" in notes
        assert "no account balance, position, order, or margin" in notes or (
            "no account balance" in notes and "order" in notes
        )

    def test_manifest_generated_hashes_match_actual_bytes(self, ticker):
        manifest = _manifest(ticker)
        for name in ("record.yaml", "README.md"):
            actual = _sha256(_pkg_dir(ticker) / name)
            assert manifest["generated_file_hashes"][name] == actual, f"{ticker}: stale hash for {name}"

    def test_no_absolute_user_path_committed(self, ticker):
        for path in _pkg_dir(ticker).iterdir():
            if path.suffix.lower() == ".png":
                continue
            text = path.read_text(errors="ignore")
            assert "/Users/nickmasters" not in text, f"{ticker}: {path.name} contains an absolute user path"
            assert "/Users/" not in text, f"{ticker}: {path.name} contains an absolute path under /Users/"

    def test_draft_stage_lifecycle_not_prematurely_marked_accepted(self, ticker):
        """This PR has not been reviewed or merged -- records must not
        claim accepted/merged status prematurely."""
        record = _record(ticker)
        assert record["lifecycle"]["lifecycle_status"] == "draft"
        assert record["provenance"]["reviewer"] is None
        assert record["provenance"]["merged_pr"] is None
        assert record["provenance"]["post_merge_verification"] is None

    def test_no_advisory_recommendation_present(self, ticker):
        record = _record(ticker)
        assert record["thesis_relationship"]["advisory_recommendation"].strip().lower().startswith("none")

    def test_no_stage_2_marker_in_record(self, ticker):
        record = _record(ticker)
        text = json.dumps(record).lower()
        assert "stage 2" not in text or "no stage 2" in text or "does not" in text

    def test_related_intelligence_record_path_matches_ticker(self, ticker):
        record = _record(ticker)
        assert record["thesis_relationship"]["related_intelligence_record"] == f"intelligence/companies/{ticker}.yaml"
        assert (Path(__file__).parent / "intelligence" / "companies" / f"{ticker}.yaml").is_file()


# ── prohibited-scope regression checks ──────────────────────────────────

def test_no_second_timeframe_anywhere_in_batch():
    for ticker in TICKERS:
        files = list(_pkg_dir(ticker).glob("*.png"))
        assert len(files) == 1
        assert files[0].name.endswith("__1D.png")


def test_no_prohibited_portfolio_field_in_any_record():
    for ticker in TICKERS:
        text = json.dumps(_record(ticker)).lower()
        # the word "target" only appears in the benign "target_pct"/"targets.yaml" context
        for banned in ("buy recommendation", "sell recommendation", "trade signal", "price target:"):
            assert banned not in text, f"{ticker}: prohibited phrase {banned!r} found"


def test_cohort_bytes_within_disclosed_storage_threshold(cohort):
    # CHART-0002 amendment's disclosed ~250MB repository-size stopping condition
    assert cohort["retention"]["total_retained_bytes"] < 250 * 1024 * 1024
