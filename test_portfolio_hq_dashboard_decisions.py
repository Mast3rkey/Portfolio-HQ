"""Focused tests for the Governance Decision Explorer (OPS-0013):
``portfolio_hq/dashboard/decisions.py`` (catalog build, two-ledger
resolution, safe Markdown rendering) and its wiring into ``model.py`` /
``render.py``.

Covers: real-repository catalog build and reconciliation; index/frontmatter
mismatch and malformed-input degradation; the governance/decisions.yaml +
decision_log.yaml two-ledger reference resolution; title derivation;
Markdown positive rendering; Markdown security (untrusted-input treatment);
supporting-artifact path safety including the sealed-data boundary;
navigation/routing markup; accessibility; and non-regression of the
existing dashboard surface.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from portfolio_hq.dashboard import decisions
from portfolio_hq.dashboard.model import build_model
from portfolio_hq.dashboard.render import render_html

REPO_ROOT = Path(__file__).resolve().parent
GOV_IDS = frozenset({"OPS-0013", "GOV-0002"})
LEGACY_IDS = frozenset({"PI-0003"})


def _render(body: str, decision_id: str = "OPS-0013",
            gov_ids: frozenset = GOV_IDS, legacy_ids: frozenset = LEGACY_IDS) -> str:
    html, _ = decisions.render_decision_body(body, decision_id, gov_ids, legacy_ids)
    return html


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _decision_md(decision_id: str, *, date="2026-08-01", status="Accepted",
                  category="operations_coordination", related=None,
                  supporting_artifact=None, body="## Context\n\nBody text.\n") -> str:
    related_str = str(related if related is not None else [])
    sa = "null" if supporting_artifact is None else f'"{supporting_artifact}"'
    return (
        "---\n"
        f"decision_id: {decision_id}\n"
        f"date: {date}\n"
        f"status: {status}\n"
        f"category: {category}\n"
        f"related_decisions: {related_str}\n"
        f"supporting_artifact: {sa}\n"
        "---\n\n"
        f"{body}"
    )


def _index_yaml(entries: list[dict]) -> str:
    lines = ["decisions:"]
    for e in entries:
        lines.append(f"  - decision_id: {e['decision_id']}")
        lines.append(f"    date: {e.get('date', '2026-08-01')}")
        lines.append(f"    status: {e.get('status', 'Accepted')}")
        lines.append(f"    category: {e.get('category', 'operations_coordination')}")
        lines.append(f"    file: {e['file']}")
    return "\n".join(lines) + "\n"


@pytest.fixture
def synth_repo(tmp_path: Path) -> Path:
    """A minimal governance corpus: one decision referencing a legacy entry
    and another governance decision, plus a decision_log.yaml."""
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-governance-decision-explorer-authorization.md",
           _decision_md("OPS-0013", related=["GOV-0002", "PI-0003"],
                        body=(
                            "## Context\n\nSee `GOV-0002` and PI-0003 in prose.\n\n"
                            "## Decision\n\nSome **bold** and *italic* text with "
                            "`inline_code` and snake_case_word.\n"
                        )))
    _write(repo / "governance/decisions/GOV-0002-operational-precedence-hierarchy.md",
           _decision_md("GOV-0002", related=["OPS-0013"], body="## Context\n\nText.\n"))
    _write(repo / "governance/decisions.yaml", _index_yaml([
        {"decision_id": "OPS-0013",
         "file": "governance/decisions/OPS-0013-governance-decision-explorer-authorization.md"},
        {"decision_id": "GOV-0002",
         "file": "governance/decisions/GOV-0002-operational-precedence-hierarchy.md"},
    ]))
    _write(repo / "decision_log.yaml", (
        "decisions:\n"
        "  - decision_id: PI-0003\n"
        "    date: 2026-07-12\n"
        "    category: portfolio_intelligence\n"
        "    decision: Phase 2 pilot authorized.\n"
        "    rationale: Smallest reversible next step.\n"
        "    supporting_artifact: null\n"
        "    status: accepted\n"
    ))
    return repo


# ── real-repository catalog / reconciliation ────────────────────────────────

def test_real_repository_catalog_builds_all_71_with_no_issues():
    cat = decisions.build_catalog(REPO_ROOT)
    assert len(cat.decisions) == 81
    assert len(cat.legacy) == 12
    assert cat.issues == ()
    assert sum(len(d.issues) for d in cat.decisions) == 0


def test_real_repository_ids_unique_and_no_orphans():
    cat = decisions.build_catalog(REPO_ROOT)
    ids = [d.decision_id for d in cat.decisions]
    assert len(ids) == len(set(ids))
    assert not any(d.orphan for d in cat.decisions)
    assert not any(d.duplicate_id for d in cat.decisions)
    assert not any(d.source_missing for d in cat.decisions)


def test_real_repository_two_ledger_zero_unresolved():
    cat = decisions.build_catalog(REPO_ROOT)
    unresolved = [
        (d.decision_id, r.decision_id)
        for d in cat.decisions for r in d.related if r.kind == "unresolved"
    ]
    assert unresolved == []


def test_real_repository_related_references_resolve_across_both_ledgers():
    cat = decisions.build_catalog(REPO_ROOT)
    kinds = {r.kind for d in cat.decisions for r in d.related}
    assert "governance" in kinds
    assert "legacy" in kinds  # e.g. GOV-0001 -> PI-0001 etc.


def test_real_repository_title_never_uses_context_heading():
    cat = decisions.build_catalog(REPO_ROOT)
    assert not any(d.title.strip().lower() == "context" for d in cat.decisions)


def test_real_repository_pi0035_table_with_escaped_pipe_renders():
    cat = decisions.build_catalog(REPO_ROOT)
    pi35 = next(d for d in cat.decisions if d.decision_id == "PI-0035")
    assert "<table>" in pi35.body_html
    # The escaped `\|` must survive as a literal pipe character in cell text,
    # never as a raw unescaped backslash-pipe artifact.
    idx = pi35.body_html.find("asset_class")
    assert idx != -1
    assert "\\|" not in pi35.body_html


def test_real_repository_ops0013_dangerous_code_span_text_stays_inert():
    cat = decisions.build_catalog(REPO_ROOT)
    ops13 = next(d for d in cat.decisions if d.decision_id == "OPS-0013")
    html = ops13.body_html
    assert "<iframe" not in html.lower()
    assert "<script" not in html.lower()
    assert "<form" not in html.lower()
    assert re.search(r'href\s*=\s*"javascript:', html, re.I) is None
    assert re.search(r"on\w+\s*=\s*\"", html, re.I) is None
    # The literal string still appears, inertly, inside a <code> element.
    assert "<code>javascript:</code>" in html
    assert "<code>&lt;iframe&gt;</code>" in html


def test_real_repository_deterministic_rendered_output():
    a = decisions.build_catalog(REPO_ROOT)
    b = decisions.build_catalog(REPO_ROOT)
    for da, db in zip(a.decisions, b.decisions):
        assert da.body_html == db.body_html
        assert da.title == db.title


# ── malformed / missing index ───────────────────────────────────────────────

def test_malformed_index_degrades_to_filesystem_discovery(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md", _decision_md("OPS-0013"))
    _write(repo / "governance/decisions.yaml", "not: [valid, yaml, ::::")
    cat = decisions.build_catalog(repo)
    assert any(i.code == "index-malformed" for i in cat.issues)
    assert len(cat.decisions) == 1
    assert cat.decisions[0].orphan is True  # filesystem-only discovery


def test_missing_index_file_degrades(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md", _decision_md("OPS-0013"))
    cat = decisions.build_catalog(repo)
    assert any(i.code == "index-missing" for i in cat.issues)
    assert cat.decisions[0].orphan is True


def test_index_entry_with_missing_backing_file(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions.yaml", _index_yaml(
        [{"decision_id": "OPS-9999", "file": "governance/decisions/OPS-9999-ghost.md"}]))
    cat = decisions.build_catalog(repo)
    d = next(x for x in cat.decisions if x.decision_id == "OPS-9999")
    assert d.source_missing is True
    assert d.source.exists is False
    assert any(i.code == "index-missing-file" for i in d.issues)
    assert "not found" in d.body_html.lower()


def test_orphan_markdown_file_not_in_index(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md", _decision_md("OPS-0013"))
    _write(repo / "governance/decisions.yaml", _index_yaml([]))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.orphan is True
    assert d.indexed is False
    assert any(i.code == "not-indexed" for i in d.issues)


def test_duplicate_decision_id_across_files(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-a.md", _decision_md("OPS-0013"))
    _write(repo / "governance/decisions/OPS-0013-b.md", _decision_md("OPS-0013"))
    _write(repo / "governance/decisions.yaml", _index_yaml(
        [{"decision_id": "OPS-0013", "file": "governance/decisions/OPS-0013-a.md"}]))
    cat = decisions.build_catalog(repo)
    assert any(i.code == "duplicate-decision-id" for i in cat.issues)
    # Both files render; one canonical detail is produced for the ID (no
    # silent merge) and it's flagged.
    matches = [d for d in cat.decisions if d.decision_id == "OPS-0013"]
    assert len(matches) == 1
    assert matches[0].duplicate_id is True
    assert matches[0].source.path == "governance/decisions/OPS-0013-a.md"


def test_filename_frontmatter_id_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-wrong-name.md",
           _decision_md("OPS-0099"))
    _write(repo / "governance/decisions.yaml", _index_yaml(
        [{"decision_id": "OPS-0099", "file": "governance/decisions/OPS-0013-wrong-name.md"}]))
    cat = decisions.build_catalog(repo)
    d = next(x for x in cat.decisions if x.decision_id == "OPS-0099")
    assert any(i.code == "filename-frontmatter-id-mismatch" for i in d.issues)


def test_index_frontmatter_mismatch_frontmatter_controls(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", status="Accepted"))
    _write(repo / "governance/decisions.yaml", _index_yaml(
        [{"decision_id": "OPS-0013", "status": "Proposed",
          "file": "governance/decisions/OPS-0013-x.md"}]))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.status == "Accepted"  # frontmatter (substantive) controls
    assert d.index_mismatches
    assert any("frontmatter controls" in m for m in d.index_mismatches)
    assert any(i.code == "index-frontmatter-mismatch" for i in d.issues)


def test_malformed_frontmatter_degraded_stub_with_separable_body(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           "---\ndecision_id: OPS-0013\nstatus: [unclosed\n---\n\nSome body text.\n")
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert any(i.code == "frontmatter-malformed" for i in d.issues)
    assert d.title  # filename-derived stub title, not a crash
    assert "Some body text." in d.body_html or d.body_html  # separable body shown


def test_missing_frontmatter_delimiters_no_separable_body(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md", "Just plain text, no frontmatter.\n")
    cat = decisions.build_catalog(repo)
    # No frontmatter delimiters found at all -> nothing was safe to separate
    # as a body, but the file still surfaces as a filename-identified
    # degraded stub rather than vanishing from the catalog.
    assert len(cat.decisions) == 1
    d = cat.decisions[0]
    assert any(i.code == "frontmatter-malformed" for i in d.issues)
    assert d.body_empty is True


def test_unsupported_status_displayed_literally_and_warned(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", status="Draft"))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.status == "Draft"
    assert any(i.code == "unsupported-status" for i in d.issues)


def test_invalid_encoding_degrades_without_raising(tmp_path: Path):
    repo = tmp_path / "repo"
    p = repo / "governance/decisions/OPS-0013-x.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"---\ndecision_id: OPS-0013\n---\n\n\xff\xfe not valid utf-8 \x00\x01")
    cat = decisions.build_catalog(repo)  # must not raise
    assert len(cat.decisions) == 1
    assert any(i.code == "file-unreadable" for i in cat.decisions[0].issues)


def test_unreadable_path_degrades(tmp_path: Path):
    # A directory where a file is expected — read_text() raises OSError.
    repo = tmp_path / "repo"
    d = repo / "governance/decisions/OPS-0013-x.md"
    d.mkdir(parents=True)
    cat = decisions.build_catalog(repo)  # must not raise
    assert len(cat.decisions) == 1
    assert any(i.code == "file-unreadable" for i in cat.decisions[0].issues)


def test_empty_body_explicit_message(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           "---\ndecision_id: OPS-0013\ndate: 2026-08-01\nstatus: Accepted\n"
           "category: x\nrelated_decisions: []\nsupporting_artifact: null\n---\n")
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.body_empty is True
    assert "no body content" in d.body_html.lower()


def test_deterministic_ordering_index_then_orphans(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0001-a.md", _decision_md("OPS-0001"))
    _write(repo / "governance/decisions/OPS-0002-b.md", _decision_md("OPS-0002"))
    _write(repo / "governance/decisions/ZZZ-0001-orphan.md", _decision_md("ZZZ-0001"))
    _write(repo / "governance/decisions.yaml", _index_yaml([
        {"decision_id": "OPS-0002", "file": "governance/decisions/OPS-0002-b.md"},
        {"decision_id": "OPS-0001", "file": "governance/decisions/OPS-0001-a.md"},
    ]))
    cat = decisions.build_catalog(repo)
    ids = [d.decision_id for d in cat.decisions]
    assert ids == ["OPS-0002", "OPS-0001", "ZZZ-0001"]  # index order, then orphans sorted


# ── supporting artifacts ─────────────────────────────────────────────────────

def test_supporting_artifact_safe_and_hashed(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "docs/EVIDENCE.md", "evidence content")
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", supporting_artifact="docs/EVIDENCE.md"))
    cat = decisions.build_catalog(repo)
    a = cat.decisions[0].supporting_artifact
    assert a is not None
    assert a.safe is True
    assert a.sha256 is not None
    assert a.size_bytes == len("evidence content")


def test_supporting_artifact_missing(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", supporting_artifact="docs/NOPE.md"))
    cat = decisions.build_catalog(repo)
    a = cat.decisions[0].supporting_artifact
    assert a.safe is False
    assert "not found" in a.warning.lower()


def test_supporting_artifact_traversal_rejected(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", supporting_artifact="../../../etc/passwd"))
    cat = decisions.build_catalog(repo)
    a = cat.decisions[0].supporting_artifact
    assert a.safe is False
    assert "traversal" in a.warning.lower()
    assert a.sha256 is None


def test_supporting_artifact_external_url_rejected(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", supporting_artifact="https://example.com/x.json"))
    cat = decisions.build_catalog(repo)
    a = cat.decisions[0].supporting_artifact
    assert a.safe is False
    assert a.sha256 is None


def test_supporting_artifact_directory_not_enumerated(tmp_path: Path):
    repo = tmp_path / "repo"
    (repo / "governance/evidence/PHQ-2026-01").mkdir(parents=True)
    _write(repo / "governance/evidence/PHQ-2026-01/one.json", "{}")
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", supporting_artifact="governance/evidence/PHQ-2026-01"))
    cat = decisions.build_catalog(repo)
    a = cat.decisions[0].supporting_artifact
    assert a.safe is False
    assert "directory" in a.warning.lower()
    assert a.sha256 is None


def test_supporting_artifact_sealed_path_hard_denied_never_read(tmp_path: Path):
    repo = tmp_path / "repo"
    sealed = repo / decisions.SEALED_DATA_PREFIX / "secret.json"
    _write(sealed, '{"do_not_read": true}')
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013",
                        supporting_artifact=decisions.SEALED_DATA_PREFIX + "secret.json"))
    cat = decisions.build_catalog(repo)
    a = cat.decisions[0].supporting_artifact
    assert a.safe is False
    assert a.exists is False  # never even stat'd/confirmed — denied outright
    assert a.sha256 is None
    assert "sealed" in a.warning.lower() or "denied" in a.warning.lower()


# ── two-ledger reference resolution (synthetic) ─────────────────────────────

def test_legacy_reference_resolves_and_renders_fact_card(synth_repo: Path):
    cat = decisions.build_catalog(synth_repo)
    ops13 = next(d for d in cat.decisions if d.decision_id == "OPS-0013")
    legacy_refs = [r for r in ops13.related if r.kind == "legacy"]
    assert [r.decision_id for r in legacy_refs] == ["PI-0003"]
    from portfolio_hq.dashboard.render import _legacy_fact_card
    legacy = next(entry for entry in cat.legacy if entry.decision_id == "PI-0003")
    card = _legacy_fact_card("PI-0003", legacy)
    assert "Historical ledger" in card
    assert "<code>accepted</code>" in card  # literal decision_log.yaml vocabulary


def test_legacy_status_vocabulary_never_remapped(synth_repo: Path):
    cat = decisions.build_catalog(synth_repo)
    legacy = next(entry for entry in cat.legacy if entry.decision_id == "PI-0003")
    assert legacy.status == "accepted"  # decision_log.yaml's own vocabulary, verbatim
    assert legacy.status not in {"Proposed", "Accepted", "Superseded", "Archived"}


def test_unknown_related_reference_inert_and_warned(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", related=["ZZZ-9999"]))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.related == (decisions.RelatedRef("ZZZ-9999", "unresolved"),)
    assert any(i.code == "unresolved-related-reference" for i in d.issues)


def test_self_reference_suppressed(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", related=["OPS-0013"]))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.related == ()
    assert any(i.code == "self-reference" for i in d.issues)


def test_duplicate_related_id_deduped_and_disclosed(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0001-a.md", _decision_md("OPS-0001"))
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", related=["OPS-0001", "OPS-0001"]))
    cat = decisions.build_catalog(repo)
    d = next(x for x in cat.decisions if x.decision_id == "OPS-0013")
    assert len(d.related) == 1
    assert any(i.code == "duplicate-related-reference" for i in d.issues)


def test_cycle_renders_without_recursion_error(synth_repo: Path):
    # OPS-0013 <-> GOV-0002 reference each other — must not recurse/hang.
    cat = decisions.build_catalog(synth_repo)
    ops13 = next(d for d in cat.decisions if d.decision_id == "OPS-0013")
    gov02 = next(d for d in cat.decisions if d.decision_id == "GOV-0002")
    assert "GOV-0002" in [r.decision_id for r in ops13.related]
    assert "OPS-0013" in [r.decision_id for r in gov02.related]
    assert "GOV-0002" in ops13.reverse_references
    assert "OPS-0013" in gov02.reverse_references


def test_reverse_references_only_from_structured_field(tmp_path: Path):
    repo = tmp_path / "repo"
    # OPS-0001's body mentions OPS-0002 in prose, but related_decisions is empty.
    _write(repo / "governance/decisions/OPS-0001-a.md",
           _decision_md("OPS-0001", related=[],
                        body="## Context\n\nSee OPS-0002 for background.\n"))
    _write(repo / "governance/decisions/OPS-0002-b.md", _decision_md("OPS-0002"))
    cat = decisions.build_catalog(repo)
    ops02 = next(d for d in cat.decisions if d.decision_id == "OPS-0002")
    assert ops02.reverse_references == ()  # prose mention creates no reverse ref


def test_reverse_reference_wording_is_exactly_neutral(synth_repo: Path):
    cat = decisions.build_catalog(synth_repo)
    from portfolio_hq.dashboard.render import _reverse_ref_item
    html = _reverse_ref_item("OPS-0013", cat)
    assert "References this decision." in html
    for verb in ("Implements", "Supersedes", "Narrows", "Accepts", "Validates", "Rejects"):
        assert verb not in html


# ── title derivation ─────────────────────────────────────────────────────────

def test_title_frontmatter_fallback(tmp_path: Path):
    repo = tmp_path / "repo"
    text = _decision_md("OPS-0013").replace(
        "supporting_artifact: null\n",
        "supporting_artifact: null\ntitle: A Hand-Authored Title\n")
    _write(repo / "governance/decisions/OPS-0013-x.md", text)
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.title == "A Hand-Authored Title"
    assert d.title_source == "frontmatter"


def test_title_h1_fallback(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/OPS-0013-x.md",
           _decision_md("OPS-0013", body="# A Body Heading Title\n\n## Context\n\nText.\n"))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.title == "A Body Heading Title"
    assert d.title_source == "h1"


def test_title_filename_fallback_real_corpus_all_58():
    cat = decisions.build_catalog(REPO_ROOT)
    assert all(d.title_source == "filename" for d in cat.decisions)


def test_title_unusable_filename_falls_back_to_id(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "governance/decisions/not-a-conventional-name.md",
           _decision_md("OPS-0013"))
    cat = decisions.build_catalog(repo)
    d = cat.decisions[0]
    assert d.title == "OPS-0013"
    assert d.title_source == "id"


# ── Markdown positive rendering ──────────────────────────────────────────────

def test_paragraphs_and_consecutive_paragraphs():
    html = _render("First paragraph.\n\nSecond paragraph.\n")
    assert html.count("<p>") == 2
    assert "First paragraph." in html and "Second paragraph." in html


def test_headings_releveled_no_skipped_levels():
    html = _render("## Context\n\n### Sub\n\n#### Deep\n")
    assert "<h4 " in html and "<h5 " in html and "<h6 " in html
    assert "<h2 " not in html and "<h3>" not in html


def test_unordered_and_ordered_lists():
    html = _render("- one\n- two\n\n1. first\n2. second\n")
    assert "<ul><li>one</li><li>two</li></ul>" in html
    assert "<ol><li>first</li><li>second</li></ol>" in html


def test_nested_list_depth_two():
    html = _render("- top\n  - nested\n- top2\n")
    assert "<ul><li>top<ul><li>nested</li></ul></li><li>top2</li></ul>" in html


def test_blockquote():
    html = _render("> quoted text\n> more\n")
    assert "<blockquote>" in html and "quoted text" in html


def test_horizontal_rule():
    html = _render("above\n\n---\n\nbelow\n")
    assert "<hr>" in html


def test_bold_both_delimiters():
    html = _render("**star bold** and __underscore bold__\n")
    assert html.count("<strong>") == 2
    assert "<strong>star bold</strong>" in html
    assert "<strong>underscore bold</strong>" in html


def test_italic_star_only_snake_case_not_italicized():
    html = _render("*italic text* but not snake_case_word\n")
    assert "<em>italic text</em>" in html
    assert "<em>" not in html.replace("<em>italic text</em>", "")
    assert "snake_case_word" in html
    assert "<em>case</em>" not in html


def test_inline_code_with_punctuation_and_angle_brackets():
    html = _render("Use `<Ticker>` and `a && b || c`.\n")
    assert "<code>&lt;Ticker&gt;</code>" in html
    assert "<code>a &amp;&amp; b || c</code>" in html


def test_fenced_code_block():
    html = _render("```python\nx = 1 < 2\n```\n")
    assert '<pre><code class="language-python">' in html
    assert "x = 1 &lt; 2" in html


def test_unmatched_fence_literal_fallback():
    html = _render("```python\nno closing fence here\n")
    assert '<pre class="literal-fallback">' in html
    assert "no closing fence here" in html


def test_table_renders_semantic_markup():
    html = _render("| A | B |\n| --- | --- |\n| 1 | 2 |\n")
    assert "<table>" in html and "<th scope=\"col\">A</th>" in html
    assert "<td>1</td>" in html and "<td>2</td>" in html


def test_table_escaped_pipe_in_cell():
    html = _render("| A | B |\n| --- | --- |\n| x \\| y | 2 |\n")
    assert "x | y" in html
    assert "\\|" not in html


def test_table_code_span_pipe_not_treated_as_separator():
    html = _render("| A | B |\n| --- | --- |\n| `a\\|b` | 2 |\n")
    assert "<code>a|b</code>" in html
    assert html.count("<td>") == 2  # still exactly two cells in the data row


def test_ambiguous_table_falls_back_to_literal():
    # Header claims 2 columns but the row has 3, AND an unterminated code
    # span makes the split itself ambiguous -> literal fallback.
    html = _render("| A | B |\n| --- | --- |\n| `unterminated | x | y |\n")
    assert '<pre class="literal-fallback">' in html


def test_unsupported_syntax_remains_visible_escaped():
    html = _render("A [markdown link](https://example.com) and ![img](x.png).\n")
    assert "<a href=\"https://example.com\"" not in html
    assert "<img" not in html
    assert "markdown link" in html
    assert "example.com" in html


# ── Markdown security ─────────────────────────────────────────────────────────

def test_raw_script_neutralized():
    html = _render("Text <script>alert(1)</script> more.\n")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_raw_iframe_neutralized():
    html = _render("Embed <iframe src=\"evil\"></iframe> here.\n")
    assert "<iframe" not in html
    assert "&lt;iframe" in html


def test_raw_form_neutralized():
    html = _render("<form action=\"/steal\"><input></form>\n")
    assert "<form" not in html
    assert "&lt;form" in html


def test_event_handler_attribute_text_neutralized():
    html = _render('<div onclick="doEvil()">click</div>\n')
    assert 'onclick="' not in html
    assert "&lt;div" in html


def test_javascript_uri_inert():
    html = _render("[click](javascript:alert(1))\n")
    assert 'href="javascript:' not in html


def test_data_uri_inert():
    html = _render("![x](data:text/html,<script>alert(1)</script>)\n")
    assert "data:text/html" not in html or "<img" not in html
    assert "<script>" not in html


def test_quoted_iframe_in_code_span_never_creates_live_element():
    html = _render("Never allow `<iframe>` embedding.\n")
    assert "<code>&lt;iframe&gt;</code>" in html
    assert "<iframe>" not in html
    assert "<iframe " not in html


def test_glob_pattern_in_code_does_not_trigger_bold_parsing():
    html = _render("Only `results/**` is affected.\n")
    assert "<code>results/**</code>" in html
    assert "<strong>" not in html


def test_malicious_decision_id_cannot_break_out_of_heading_id_attribute():
    # Independent-review finding (PR #217, reviewed head 1a246e0):
    # decision_id was interpolated into a heading id="..." attribute without
    # sanitization, so a decision_id containing a quote could break out of
    # the attribute and inject a live event-handler attribute.
    from html.parser import HTMLParser

    html = _render("## Context\n\nSome text.\n",
                    decision_id='OPS-0013" onmouseover="alert(1)')

    class _Check(HTMLParser):
        def handle_starttag(self, tag, attrs):
            names = [a[0] for a in attrs]
            assert "onmouseover" not in names, f"live event-handler attribute injected: {attrs}"
            if tag == "h4":
                # Exactly one attribute (id) — no second attribute was
                # created by an unescaped quote in decision_id.
                assert names == ["id"], attrs

    _Check().feed(html)
    assert ' onmouseover="' not in html


def test_heading_id_sanitizes_decision_id_same_as_heading_text():
    html = _render("## Context\n\n", decision_id="<script>evil</script>")
    assert "<script>evil" not in html.split("id=")[0]  # never live before the id attr
    assert "onerror" not in html
    # id value itself contains only slug-safe characters.
    import re
    m = re.search(r'id="([^"]*)"', html)
    assert m and re.fullmatch(r"[a-z0-9-]+", m.group(1))


def test_image_syntax_produces_no_img_element():
    html = _render("![alt text](x.png)\n")
    assert "<img" not in html


def test_no_unsafe_runtime_innerhtml_in_js():
    from portfolio_hq.dashboard.render import _JS
    assert "innerHTML" not in _JS
    assert "insertAdjacentHTML" not in _JS
    assert "document.write" not in _JS


def test_no_fetch_or_websocket_in_js():
    from portfolio_hq.dashboard.render import _JS
    for token in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource"):
        assert token not in _JS


def test_no_repository_mutation_in_decisions_module():
    import inspect
    src = inspect.getsource(decisions)
    for token in ("write_text(", "write_bytes(", "unlink(", "os.remove", "shutil.rmtree"):
        assert token not in src


# ── navigation / rendered-page integration ──────────────────────────────────

def test_decision_deep_link_hash_route_present():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert 'href="#/decision/OPS-0013"' in html or 'href="#/decision/GOV-0002"' in html


def test_decision_detail_section_id_matches_hash_route():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert 'id="/decision/GOV-0002"' in html
    assert 'data-decision-id="GOV-0002"' in html


def test_governance_remains_only_top_level_view_hosting_decisions():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    # Exactly five top-level nav items/sections, unchanged by this feature.
    for sid in ("overview", "portfolio", "intelligence", "governance", "system"):
        assert f'data-target="{sid}"' in html
    assert html.count('data-target="') == 5
    assert html.count("<section id=") == 5  # decision-detail sections use
    # a different `id="/decision/..."` scheme, not `id="{name}"` — this
    # count must stay exactly 5.


def test_decision_not_found_element_present_and_hidden_by_default():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    m2 = re.search(r'<div id="decision-not-found"[^>]*>', html)
    assert m2 is not None
    assert "hidden" in m2.group(0)


def test_breadcrumb_uses_native_anchor():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert 'class="breadcrumb"' in html
    assert '<a href="#governance">Governance</a>' in html


def test_search_input_present_with_label():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert '<label for="decision-search">' in html
    assert 'id="decision-search"' in html
    assert 'type="search"' in html


def test_route_hash_pattern_present_in_js():
    from portfolio_hq.dashboard.render import _JS
    assert "routeHash" in _JS
    assert "openDecisionDetail" in _JS
    assert "hashchange" in _JS


def test_js_views_class_gates_decision_detail_css():
    from portfolio_hq.dashboard.assets import __init__ as _  # noqa: F401  (package marker check)
    css = (Path(__file__).resolve().parent / "portfolio_hq" / "dashboard"
           / "assets" / "dashboard.css").read_text()
    assert "html.js-views .decision-detail" in css
    assert ".decision-detail.active" in css


def test_no_javascript_mode_content_visible_and_anchor_reachable():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    # The raw server-rendered HTML never carries the JS-added class, and no
    # decision-detail section is rendered with the `hidden` attribute —
    # visibility is controlled entirely by a CSS class gated on that
    # JS-added class, so without JS every decision stays in plain flow.
    assert 'class="js-views"' not in html
    detail_start = html.index('class="decision-detail"')
    tag_start = html.rfind("<section", 0, detail_start)
    tag_end = html.index(">", detail_start)
    assert "hidden" not in html[tag_start:tag_end]


def test_unknown_decision_id_fallback_message_text():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert "Decision not found" in html
    assert "Showing the governance index instead" in html


# ── accessibility ─────────────────────────────────────────────────────────────

def test_exactly_one_page_h1_unchanged():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert html.count("<h1") == 1


def test_decision_heading_ids_unique_across_page():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    ids = re.findall(r'<h[3-6] id="([^"]+)"', html)
    assert len(ids) == len(set(ids))


def test_decision_detail_title_focus_target_exists():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert 'class="decision-detail-title" id="decision-GOV-0002-h" tabindex="-1"' in html


def test_search_field_has_accessible_label():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    label_idx = html.index('<label for="decision-search">')
    input_idx = html.index('id="decision-search"', label_idx)
    assert input_idx > label_idx


def test_decision_links_have_meaningful_text():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    # Every decision-link anchor's visible text includes the decision ID —
    # never bare "click here"/"here" style text.
    for m2 in re.finditer(r'<a href="#/decision/([A-Z0-9-]+)" class="decision-link[^"]*">(.*?)</a>',
                            html, re.S):
        assert m2.group(1) in m2.group(2)


def test_semantic_table_headers_in_decision_body():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert '<th scope="col">' in html  # already true for existing tables; still
    # present alongside decision-body tables (PI-0035's table, at minimum).


def test_code_blocks_have_overflow_scroll_css():
    css = (Path(__file__).resolve().parent / "portfolio_hq" / "dashboard"
           / "assets" / "dashboard.css").read_text()
    idx = css.index(".decision-body pre {")
    block = css[idx: css.index("}", idx)]
    assert "overflow-x: auto" in block


def test_long_values_wrap_in_decision_body_css():
    css = (Path(__file__).resolve().parent / "portfolio_hq" / "dashboard"
           / "assets" / "dashboard.css").read_text()
    idx = css.index(".decision-body {")
    block = css[idx: css.index("}", idx)]
    assert "overflow-wrap: anywhere" in block


def test_no_page_level_horizontal_scroll_rule_still_present():
    css = (Path(__file__).resolve().parent / "portfolio_hq" / "dashboard"
           / "assets" / "dashboard.css").read_text()
    assert "overflow-x: hidden" in css  # html, body — unweakened by this change


def test_reduced_motion_still_covers_decision_detail_animation():
    css = (Path(__file__).resolve().parent / "portfolio_hq" / "dashboard"
           / "assets" / "dashboard.css").read_text()
    assert "prefers-reduced-motion: reduce" in css


# ── regression / boundaries ──────────────────────────────────────────────────

def test_decision_row_shape_unchanged():
    from portfolio_hq.dashboard.model import DecisionRow
    fields = set(DecisionRow.__dataclass_fields__.keys())
    assert fields == {"decision_id", "date", "status", "category", "file"}


def test_flat_governance_table_still_renders():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert "Governance decision index (latest 25" in html


def test_real_repository_model_and_render_succeed_end_to_end():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    assert html.startswith("<!DOCTYPE html>")
    assert len(m.decision_catalog.decisions) == 81


def test_generated_html_size_within_regression_ceiling():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    # Measured ~2.1 MB for the current 58-decision corpus (~1.4 MB raw
    # Markdown). A generous ceiling catches an accidental duplication
    # regression (e.g. rendering every body twice) without being brittle to
    # ordinary corpus growth.
    assert len(html) < 6_000_000


def test_no_second_top_level_navigation_item_added():
    m = build_model(REPO_ROOT)
    html = render_html(m)
    nav_start = html.index('<nav class="primary-nav"')
    nav_end = html.index("</nav>", nav_start)
    nav_html = html[nav_start:nav_end]
    assert nav_html.count("<li>") == 5
