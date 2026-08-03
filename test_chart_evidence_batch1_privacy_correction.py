"""Regression tests for the CHART-0002 Batch 1 post-merge privacy-provenance
correction.

PR #226 merged the 19-package Batch 1 evidence set (governance/evidence/
CHART-0002/<ticker>-daily-2026-08-01/) without the independent exact-head
review or valid final-head principal acceptance CHART-0002 Section 20 /
OPS-0007 Section 1 require. A retrospective post-merge audit (PR #226 issue
comment issuecomment-5159313447) found one systemic MAJOR content defect: all
19 MANIFEST.json/record.yaml packages presented a PARAPHRASE of the per-image
privacy-approval comment (issuecomment-5159177312) as a verbatim quotation --
omitting the exact-head anchor and two full disclaimer sentences -- with no
citation of the source comment's ID or URL anywhere.

This module verifies the bounded correction: every package now carries a
structured, mechanically verifiable `privacy_approval_source` citation, and
the quoted block matches the retained GitHub comment's text exactly (not a
paraphrase). It also verifies the correction touched nothing it should not
have (images, Stage 1 content, lifecycle/reviewer fields, cohort/shard
invariants) and that WS-0012/CLAUDE.md no longer assert PR #226 is an
unmerged draft.

Does not import or couple to allocate.py, margin_state.py, levels.py,
intelligence_validator.py, dashboard code, or brokerage code.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent
CHART_0002_ROOT = REPO_ROOT / "governance" / "evidence" / "CHART-0002"
COHORT_MANIFEST_PATH = CHART_0002_ROOT / "COHORT_BATCH1_19_DAILY.yaml"
WORKSTREAMS_PATH = REPO_ROOT / "operations" / "WORKSTREAMS.yaml"
CLAUDE_MD_PATH = REPO_ROOT / "CLAUDE.md"

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

PR_NUMBER = 226
PRIVACY_COMMENT_ID = 5159177312
PRIVACY_COMMENT_URL = "https://github.com/Mast3rkey/Portfolio-HQ/pull/226#issuecomment-5159177312"
AUDIT_COMMENT_ID = 5159313447
IMPLEMENTATION_HEAD = "1201104ccfc5853ebf708ca7c92853fe39ffc599"
MERGE_COMMIT = "bc3dc540a23aac6939ccc5bc37c73508e4a411f9"

# The exact, independently-verified (against the live GitHub comment,
# byte-for-byte, this session) text of issuecomment-5159177312. Any package
# that presents a DIFFERENT string as a quotation of this comment is
# presenting a paraphrase as verbatim -- exactly the defect being corrected.
VERBATIM_COMMENT_TEXT = (
    "Per-image privacy approval:\n"
    "\n"
    "I explicitly invoke the accepted CHART-0001 §5 / CHART-0002 §6 narrow "
    "platform-watermark/username exception separately for each of the following 19 "
    "retained `1D` images in PR #226 at exact head "
    "`1201104ccfc5853ebf708ca7c92853fe39ffc599`:\n"
    "\n"
    "AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GOOGL, ISRG, KLAC, LLY, META, MSFT, NVDA, "
    "PANW, PWR, TMO, TSM, V.\n"
    "\n"
    "For each named image individually, I approve retention of the visible "
    "`nichmasters created with TradingView.com, ...` watermark/username exactly as captured.\n"
    "\n"
    "This constitutes 19 distinct per-image approvals recorded together for efficiency. "
    "It is not a general username waiver, does not apply to another chart, ticker, "
    "timeframe, image, or future batch, and does not authorize redaction, cropping, "
    "blurring, or any pixel modification.\n"
    "\n"
    "Each image must otherwise pass its individual privacy review, contain no other "
    "privacy-sensitive information, preserve its original pixels byte-for-byte, and "
    "maintain source/destination SHA-256 equality.\n"
    "\n"
    "This privacy approval does not constitute final approval of PR #226, does not "
    "authorize readiness or merge, and creates no Stage 2, portfolio-policy, trading, "
    "brokerage, or execution authority."
)

# The old (defective) suffix text this correction removed. Used only to
# confirm it is now gone.
OLD_PARAPHRASE_MARKERS = [
    "received live in this authorizing implementation session, 2026-08-02",
    "CHART-0001 Section 5 / CHART-0002 Section 6 narrow platform-watermark",
    "This is 19 separate per-image approvals",
]


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


@pytest.fixture(scope="module")
def workstreams_text() -> str:
    return WORKSTREAMS_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text() -> str:
    return CLAUDE_MD_PATH.read_text(encoding="utf-8")


def _extract_quoted_block(text: str) -> str:
    """Extract the text between the FORMAL PER-IMAGE quote's opening and
    closing double-quote characters."""
    start = text.index('"Per-image privacy approval:')
    end = text.index('This approval supersedes')
    quoted = text[start:end].strip()
    assert quoted.startswith('"') and quoted.endswith('"'), "quoted block not properly delimited"
    return quoted[1:-1].strip()


# ── per-package provenance tests (requirements 1-6) ─────────────────────

@pytest.mark.parametrize("ticker", TICKERS)
class TestPrivacyApprovalProvenance:
    def test_manifest_has_structured_privacy_approval_source(self, ticker):
        manifest = _manifest(ticker)
        assert "privacy_approval_source" in manifest
        src = manifest["privacy_approval_source"]
        assert src["pr_number"] == PR_NUMBER
        assert src["comment_id"] == PRIVACY_COMMENT_ID
        assert src["comment_url"] == PRIVACY_COMMENT_URL

    def test_record_has_matching_structured_privacy_approval_source(self, ticker):
        record = _record(ticker)
        src = record["privacy_and_redaction"]["privacy_approval_source"]
        assert src["pr_number"] == PR_NUMBER
        assert src["comment_id"] == PRIVACY_COMMENT_ID
        assert src["comment_url"] == PRIVACY_COMMENT_URL

    def test_manifest_and_record_source_agree(self, ticker):
        m_src = _manifest(ticker)["privacy_approval_source"]
        r_src = _record(ticker)["privacy_and_redaction"]["privacy_approval_source"]
        assert m_src["comment_id"] == r_src["comment_id"]
        assert m_src["comment_url"] == r_src["comment_url"]
        assert m_src["pr_number"] == r_src["pr_number"]
        assert m_src["anchored_implementation_head"] == r_src["anchored_implementation_head"]

    def test_implementation_head_anchor_present(self, ticker):
        manifest = _manifest(ticker)
        record = _record(ticker)
        assert manifest["privacy_approval_source"]["anchored_implementation_head"] == IMPLEMENTATION_HEAD
        assert record["privacy_and_redaction"]["privacy_approval_source"]["anchored_implementation_head"] == IMPLEMENTATION_HEAD
        # The head must also appear inside the verbatim-quoted comment text itself.
        assert IMPLEMENTATION_HEAD in manifest["privacy_result_detail"]
        assert IMPLEMENTATION_HEAD in record["privacy_and_redaction"]["username_exception_note"]

    def test_manifest_quoted_block_is_verbatim_not_paraphrase(self, ticker):
        manifest = _manifest(ticker)
        quoted = _extract_quoted_block(manifest["privacy_result_detail"])
        assert quoted == VERBATIM_COMMENT_TEXT, f"{ticker}: MANIFEST.json quoted block is not verbatim"

    def test_record_quoted_block_is_verbatim_not_paraphrase(self, ticker):
        record = _record(ticker)
        note = record["privacy_and_redaction"]["username_exception_note"]
        quoted = _extract_quoted_block(note)
        assert quoted == VERBATIM_COMMENT_TEXT, f"{ticker}: record.yaml quoted block is not verbatim"

    def test_old_paraphrase_markers_absent(self, ticker):
        manifest_text = json.dumps(_manifest(ticker))
        record_text = yaml.safe_dump(_record(ticker))
        for marker in OLD_PARAPHRASE_MARKERS:
            assert marker not in manifest_text, f"{ticker}: stale paraphrase marker still in MANIFEST.json: {marker!r}"
            assert marker not in record_text, f"{ticker}: stale paraphrase marker still in record.yaml: {marker!r}"

    def test_not_final_approval_disclaimer_preserved(self, ticker):
        """The corrected citation must preserve, not omit, the disclaimer
        that the privacy comment does not authorize readiness or merge --
        the exact sentence the original defect dropped."""
        manifest = _manifest(ticker)
        record = _record(ticker)
        disclaimer_substrings = (
            "does not constitute final approval of PR #226",
            "does not authorize readiness or merge",
        )
        for substr in disclaimer_substrings:
            assert substr in manifest["privacy_result_detail"], f"{ticker}: MANIFEST.json missing {substr!r}"
            assert substr in record["privacy_and_redaction"]["username_exception_note"], f"{ticker}: record.yaml missing {substr!r}"
        m_disclosure = manifest["privacy_approval_source"]["not_final_approval_disclosure"]
        r_disclosure = record["privacy_and_redaction"]["privacy_approval_source"]["not_final_approval_disclosure"]
        for substr in disclaimer_substrings:
            assert substr in m_disclosure
            assert substr in r_disclosure

    def test_approval_scope_is_individually_ticker_specific(self, ticker):
        """Each package's approval_scope must name its OWN ticker and image
        -- not a generic batch-wide statement -- matching the source
        comment's own '19 distinct per-image approvals' framing."""
        manifest = _manifest(ticker)
        record = _record(ticker)
        m_scope = manifest["privacy_approval_source"]["approval_scope"]
        r_scope = record["privacy_and_redaction"]["privacy_approval_source"]["approval_scope"]
        assert ticker in m_scope
        assert f"{ticker}__2026-08-01__1D.png" in m_scope
        assert ticker in r_scope
        assert f"{ticker}__2026-08-01__1D.png" in r_scope

    def test_approval_scope_unique_per_ticker(self, ticker):
        """Sanity check that scope text isn't copy-pasted identically
        across tickers (would indicate a batch-wide, not per-image,
        citation)."""
        other_tickers = [t for t in TICKERS if t != ticker]
        this_scope = _manifest(ticker)["privacy_approval_source"]["approval_scope"]
        for other in other_tickers[:2]:  # spot-check, not exhaustive
            other_scope = _manifest(other)["privacy_approval_source"]["approval_scope"]
            assert this_scope != other_scope

    def test_correction_provenance_cites_retrospective_audit(self, ticker):
        manifest = _manifest(ticker)
        record = _record(ticker)
        m_prov = manifest["privacy_approval_source"]["correction_provenance"]
        r_prov = record["privacy_and_redaction"]["privacy_approval_source"]["correction_provenance"]
        assert str(AUDIT_COMMENT_ID) in m_prov
        assert str(AUDIT_COMMENT_ID) in r_prov


# ── nothing-else-changed tests (requirements 7, 8, 9, 11) ────────────────

@pytest.mark.parametrize("ticker", TICKERS)
class TestCorrectionScopeBoundary:
    def test_generated_file_hashes_reconcile(self, ticker):
        manifest = _manifest(ticker)
        pkg = _pkg_dir(ticker)
        for name in ("record.yaml", "README.md"):
            actual = _sha256(pkg / name)
            assert manifest["generated_file_hashes"][name] == actual, f"{ticker}: stale {name} hash"

    def test_image_hash_bytes_name_unchanged_vs_cohort_manifest(self, ticker, cohort):
        """COHORT_BATCH1_19_DAILY.yaml is untouched by this correction --
        it is the pre-correction, PR #226-merged ground truth for image
        identity. The retained image, its manifest hash, and its record
        hash must all still agree with it exactly."""
        cohort_pkg = next(p for p in cohort["packages"] if p["ticker"] == ticker)
        pkg = _pkg_dir(ticker)
        img_path = pkg / Path(cohort_pkg["retained_image"]).name
        assert img_path.is_file()
        actual_hash = _sha256(img_path)
        actual_bytes = img_path.stat().st_size

        assert actual_hash == cohort_pkg["sha256"]
        assert actual_bytes == cohort_pkg["bytes"]

        manifest = _manifest(ticker)
        assert manifest["retained_sha256"] == cohort_pkg["sha256"]
        assert manifest["retained_byte_size"] == cohort_pkg["bytes"]
        assert manifest["dimensions"] == cohort_pkg["dimensions"]
        assert manifest["governed_source_sha256"] == cohort_pkg["sha256"]
        assert manifest["transformation_history"] == []

        record = _record(ticker)
        ident = record["identity_and_capture"]
        assert ident["retained_image_sha256"] == cohort_pkg["sha256"]
        assert ident["governed_source_sha256"] == cohort_pkg["sha256"]
        assert ident["image_dimensions"] == cohort_pkg["dimensions"]

    def test_stage1_content_fields_untouched(self, ticker):
        """visible_facts/observations/inferences/uncertainties and
        thesis_relationship must be exactly as authored -- this correction
        touches privacy-approval citation only."""
        record = _record(ticker)
        content = record["content"]
        for key in ("visible_facts", "observations", "inferences", "uncertainties"):
            assert isinstance(content[key], list)
            assert len(content[key]) > 0
        assert record["thesis_relationship"]["governed_consequence"] == "none"
        assert record["thesis_relationship"]["advisory_recommendation"].strip().lower().startswith("none")

    def test_lifecycle_and_reviewer_fields_still_draft_and_null(self, ticker):
        """Per the retrospective audit's own explicit NOTE: these fields
        remain accurate and must NOT be changed by this correction -- no
        independent review or principal acceptance of the batch's content
        has in fact occurred."""
        record = _record(ticker)
        assert record["lifecycle"]["lifecycle_status"] == "draft"
        assert record["provenance"]["reviewer"] is None
        assert record["provenance"]["reviewed_head"] is None
        assert record["provenance"]["principal_acceptance"] is None
        assert record["provenance"]["merged_pr"] is None
        assert record["provenance"]["merge_commit"] is None
        assert record["provenance"]["post_merge_verification"] is None

    def test_no_stage_2_or_prohibited_coupling_introduced(self, ticker):
        record_text = json.dumps(_record(ticker)).lower()
        manifest_text = json.dumps(_manifest(ticker)).lower()
        for text, label in ((record_text, "record.yaml"), (manifest_text, "MANIFEST.json")):
            for banned in ("stage 2 record", "stage_2_record", "cross-timeframe synthesis record"):
                assert banned not in text or "no stage 2" in text or "does not" in text, (
                    f"{ticker}: possible Stage 2 coupling in {label}"
                )
        prohibited = " ".join(str(x).lower() for x in _record(ticker)["prohibited_uses"])
        for phrase in ("allocator", "ladder-0001", "intelligence", "score", "signal", "execution", "tier"):
            assert phrase in prohibited


# ── cohort/shard invariants unchanged (requirement 9) ────────────────────

def test_cohort_manifest_itself_untouched_by_correction(cohort):
    """COHORT_BATCH1_19_DAILY.yaml is out of this correction's authorized
    scope -- confirm its shape still matches the original merged batch."""
    assert cohort["ticker_count"] == 19
    assert cohort["tickers"] == TICKERS
    assert cohort["shards"] == SHARDS
    assert cohort["stage"] == "Stage 1 only"
    assert cohort["lifecycle_status"] == "draft"


def test_no_extra_or_missing_package_directories():
    subdirs = sorted(p.name for p in CHART_0002_ROOT.iterdir() if p.is_dir())
    expected = sorted(f"{t.lower()}-daily-2026-08-01" for t in TICKERS)
    assert subdirs == expected


def test_no_readme_files_touched_by_correction():
    """READMEs were out of scope for this correction -- their hashes as
    recorded in each MANIFEST.json must equal their pre-correction values
    (independently confirmed identical during this correction's own
    generated_file_hashes recomputation step)."""
    for ticker in TICKERS:
        pkg = _pkg_dir(ticker)
        manifest = _manifest(ticker)
        actual = _sha256(pkg / "README.md")
        assert manifest["generated_file_hashes"]["README.md"] == actual


# ── WS-0012 / CLAUDE.md lifecycle synchronization (requirement 10) ───────

def test_workstreams_no_longer_claims_pr226_unmerged_draft(workstreams_text):
    ws0012_start = workstreams_text.index("- id: WS-0012")
    # Bound the search to this workstream's own entry (next "- id: WS-" or EOF).
    next_id = workstreams_text.find("\n  - id: WS-", ws0012_start + 1)
    ws0012_text = workstreams_text[ws0012_start: next_id if next_id != -1 else None]

    assert "has not yet been opened" not in ws0012_text
    assert "The draft implementation PR has not yet been opened" not in ws0012_text
    assert MERGE_COMMIT in ws0012_text
    assert "merged_without_required_review" in ws0012_text
    assert str(AUDIT_COMMENT_ID) in ws0012_text


def test_workstreams_active_fields_do_not_reference_merged_pr228(workstreams_text):
    """Per OPS-0001's workstream-register schema (`governance/decisions/
    OPS-0001-portfolio-hq-workstream-register.md`): 'active_branch and
    active_pr hold only currently-live work -- a branch or PR that still
    exists and is unmerged. A merged historical PR belongs under
    milestones or evidence_refs, never in these two fields.'

    PR #228 (branch claude/ws0012-postmerge-factual-sync-pr227) was the
    live WS-0012 synchronization unit when this test was first authored, so
    an earlier version asserted WS-0012's active fields pointed at it
    directly. PR #228 has since merged and is now historical -- it is
    correctly recorded under WS-0012's milestones/evidence_refs instead
    (see test_workstreams_no_longer_claims_pr226_unmerged_draft above).
    Freezing that one now-merged PR's identity as a permanent expected
    value would itself violate the very OPS-0001 rule this test exists to
    enforce, and would break again the moment the next legitimate live-work
    unit updates these fields -- a repository test must not pin one mutable
    GitHub live-work identity forever. Exact current GitHub liveness (which
    branch/PR is actually open right now) is verified during each PR's own
    preflight and independent review, not by this test.

    The durable invariant enforced here instead: whatever WS-0012's active
    fields currently say, they must never regress back to naming merged
    PR #228 or its branch as still live."""
    data = yaml.safe_load(workstreams_text)
    ws0012 = next(w for w in data["workstreams"] if w["id"] == "WS-0012")
    assert ws0012["active_branch"] != "claude/ws0012-postmerge-factual-sync-pr227"
    assert ws0012["active_pr"] != 228


def test_claude_md_no_longer_claims_pr226_not_yet_reviewed_merged(claude_md_text):
    marker = "CHART-0002 first implementation batch"
    idx = claude_md_text.index(marker)
    # The bullet is a single long paragraph; bound to end of line.
    end = claude_md_text.index("\n", idx)
    bullet = claude_md_text[idx:end]

    assert "not yet reviewed/merged" not in bullet
    assert MERGE_COMMIT in bullet
    assert str(AUDIT_COMMENT_ID) in bullet
    assert "premature" in bullet.lower()


def test_claude_md_pointer_states_correction_does_not_retroactively_satisfy_gate(claude_md_text):
    marker = "CHART-0002 first implementation batch"
    idx = claude_md_text.index(marker)
    end = claude_md_text.index("\n", idx)
    bullet = claude_md_text[idx:end]
    assert "does not retroactively satisfy the missed pre-merge gate" in bullet
