"""Focused tests for the repository-native Portfolio-HQ dashboard.

Covers: source loading, malformed/missing YAML, stale-holdings and
missing-PHQ-2026-02 warnings, dirty-worktree provenance, exact commit
rendering, gated-cash / SPCX / SKHY presentation, no-renormalization framing,
HTML escaping, offline (no external asset) rendering, localhost-only server
binding, absence of any order/mutation control, deterministic rendering after
normalizing the disclosed timestamp, structural HTML assertions, the CLI
build/serve surface, and — per the source-of-truth integrity review — proof
that no retained historical HTML is read as operational input.
"""

from __future__ import annotations

import re
import subprocess
import threading
import urllib.request
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from portfolio_hq.dashboard import build_model, render_html
from portfolio_hq.dashboard import model as model_mod
from portfolio_hq.dashboard import provenance as prov_mod
from portfolio_hq.dashboard.cli import main as cli_main
from portfolio_hq.dashboard.server import _make_handler

REPO_ROOT = Path(__file__).resolve().parent
FIXED_NOW = datetime(2026, 7, 31, 12, 0, 0, tzinfo=timezone.utc)


# ── fixtures ─────────────────────────────────────────────────────────────────

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """A minimal but structurally valid repository with a real git history."""
    repo = tmp_path / "repo"
    repo.mkdir()

    _write(repo / "holdings.yaml", (
        "margin:\n"
        "  debt: 1590.4\n"
        "  buffer_pct: 63.12\n"
        "  synced_at: 2026-07-22\n"
        "holdings: {}\n"
        "shares:\n"
        "  AAPL: 0.31741\n"
        "  SKHY: 0.278473\n"
        "  NVDA: 0.98\n"
        "crypto_shares:\n"
        "  ETH: 0.09\n"
    ))
    # Canonical v1.30 destination-architecture shape (PHQ-2026-02) — matches
    # current main's real targets.yaml: a flat `destination:` list, no
    # `tiers:`/`crypto:` blocks (both retired; BTC/ETH/SOL each get their own
    # destination row instead of an aggregate crypto sleeve).
    _write(repo / "targets.yaml", (
        "destination:\n"
        "  - ticker: NVDA\n"
        "    target_pct: 3.35\n"
        "    asset_class: equity\n"
        "  - ticker: AAPL\n"
        "    target_pct: 0.75\n"
        "    asset_class: equity\n"
        "  - ticker: SKHY\n"
        "    target_pct: 0.75\n"
        "    asset_class: equity\n"
        "  - ticker: SPCX\n"
        "    target_pct: 1.0\n"
        "    asset_class: equity\n"
        "  - ticker: ETH\n"
        "    target_pct: 1.5\n"
        "    asset_class: crypto\n"
        "caps:\n"
        "  clusters:\n"
        "    - name: semis\n"
        "      pct: 25.0\n"
        "      tickers: [NVDA, SKHY]\n"
        "gates:\n"
        "  min_lot_dollars: 25\n"
        "margin:\n"
        "  leverage_cap: 1.8\n"
        "  buffer_floor_pct: 30.0\n"
    ))
    _write(repo / "governance/decisions.yaml", (
        "decisions:\n"
        "  - decision_id: PHQ-2026-01\n"
        "    date: 2026-07-30\n"
        "    status: Accepted\n"
        "    category: portfolio_construction_governance\n"
        "    file: governance/decisions/PHQ-2026-01.md\n"
    ))
    _write(repo / "operations/WORKSTREAMS.yaml", (
        "workstreams:\n"
        "  - id: WS-0005\n"
        "    title: Zero-based tier review\n"
        "    status: authorized\n"
        "    priority: primary\n"
        "    next_action: Continue milestone 3.\n"
    ))
    gated = (repo / "governance/evidence/PHQ-2026-01/final_due_diligence"
             / "Portfolio_HQ_Gated_Name_Disposition_v1_32.csv")
    _write(gated, (
        "ticker,target_weight,status,reason,next_gate,evidence\n"
        "SPCX,0.0075,HOLD TARGET IN CASH,Private security,Require an investable vehicle,cash\n"
        "RKLB,0.005,HOLD TARGET IN CASH,Execution risk,Require Q2 results,record revenue\n"
    ))
    _write(repo / "intelligence/freshness_registry.yaml", (
        "schema_version: 1\n"
        "tickers:\n"
        "  - ticker: NVDA\n"
        "    monitoring_enabled: false\n"
    ))
    (repo / "intelligence/companies").mkdir(parents=True)
    (repo / "intelligence/themes").mkdir(parents=True)

    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")
    return repo


# ── source loading & warnings ────────────────────────────────────────────────

def test_source_loading_reads_repository_state(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    tickers = {h.ticker for h in m.holdings}
    assert {"AAPL", "SKHY", "NVDA", "ETH"} <= tickers
    assert m.margin.debt == 1590.4
    assert m.margin.buffer_pct == 63.12
    # Aggregate crypto sleeve retired by PHQ-2026-02 — canonical destination
    # architecture gives BTC/ETH/SOL their own destination row instead, so
    # targets.yaml carries no `crypto:` block and this stays None.
    assert m.crypto_sleeve_pct is None
    # Per-name tier retired by PHQ-2026-02 — the canonical destination schema
    # has no tier concept (allocate.build_roster() returns only target_pct/
    # asset_class per row), so this proves the dashboard reflects that
    # absence rather than resolving a stale or fabricated tier label.
    nvda = next(h for h in m.holdings if h.ticker == "NVDA")
    assert nvda.tier is None


def test_missing_yaml_degrades_with_warning(tmp_repo: Path):
    (tmp_repo / "holdings.yaml").unlink()
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert any("could not be read" in n.title.lower() or "not found" in n.detail.lower()
               for n in m.warnings)
    # Still renders.
    assert "<html" in render_html(m).lower()


def test_malformed_yaml_degrades_without_raising(tmp_repo: Path):
    (tmp_repo / "targets.yaml").write_text("tiers: [unclosed\n  bad: :::\n")
    m = build_model(tmp_repo, now=FIXED_NOW)  # must not raise
    assert render_html(m)  # renders something


def test_stale_holdings_warning(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.margin.stale is True
    assert any("not be reconciled" in n.title.lower() for n in m.warnings)


def test_fresh_holdings_no_stale_warning(tmp_repo: Path):
    today = model_mod.date.today().isoformat()
    txt = (tmp_repo / "holdings.yaml").read_text().replace("2026-07-22", today)
    (tmp_repo / "holdings.yaml").write_text(txt)
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.margin.stale is False
    assert not any("not be reconciled" in n.title.lower() for n in m.warnings)


def test_missing_phq_2026_02_warning(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.phq_2026_02_filed is False
    assert any("PHQ-2026-02" in n.title for n in m.notices)


def test_phq_2026_02_present_suppresses_warning(tmp_repo: Path):
    dec = tmp_repo / "governance/decisions.yaml"
    dec.write_text(dec.read_text() + (
        "  - decision_id: PHQ-2026-02\n"
        "    date: 2026-08-01\n"
        "    status: Accepted\n"
        "    category: portfolio_construction_governance\n"
        "    file: governance/decisions/PHQ-2026-02.md\n"
    ))
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.phq_2026_02_filed is True
    assert not any("PHQ-2026-02" in n.title for n in m.notices)


def test_lookthrough_json_missing_from_disk_warns_visibly(tmp_repo: Path):
    # tmp_repo deliberately never creates the due-diligence JSON — the
    # fallback ceilings (8%/40%) are in effect and must not be silent.
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.ai_platform_measured_pct is None
    assert any("look-through evidence unreadable" in n.title.lower()
               for n in m.warnings)
    assert any("8% / 40%" in n.detail for n in m.warnings)


def _write_due_diligence_json(repo: Path, body: str) -> Path:
    path = (repo / "governance/evidence/PHQ-2026-01/final_due_diligence"
            / "Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json")
    _write(path, body)
    return path


def test_lookthrough_json_present_and_valid_suppresses_warning(tmp_repo: Path):
    _write_due_diligence_json(tmp_repo, (
        "{\"lookthrough_summary\": {"
        "\"approved_single_issuer_ceiling\": 0.08, "
        "\"approved_ai_platform_common_driver_ceiling\": 0.40, "
        "\"effective_ai_platform_common_driver_estimate\": 0.4003}}"
    ))
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.ai_platform_measured_pct == pytest.approx(40.03)
    assert not any("look-through evidence unreadable" in n.title.lower()
                   for n in m.warnings)


def test_lookthrough_json_malformed_warns_visibly(tmp_repo: Path):
    _write_due_diligence_json(tmp_repo, "{not: valid json or yaml::")
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.ai_platform_measured_pct is None
    assert any("look-through evidence unreadable" in n.title.lower()
               for n in m.warnings)


def test_lookthrough_json_present_but_missing_summary_key_warns(tmp_repo: Path):
    _write_due_diligence_json(tmp_repo, "{\"some_other_key\": true}")
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.ai_platform_measured_pct is None
    assert any("look-through evidence unreadable" in n.title.lower()
               for n in m.warnings)


def test_buffer_below_floor_is_blocker(tmp_repo: Path):
    txt = (tmp_repo / "holdings.yaml").read_text().replace("63.12", "22.0")
    (tmp_repo / "holdings.yaml").write_text(txt)
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.margin.below_buffer_floor is True
    assert any("below floor" in n.title.lower() for n in m.blockers)


# ── provenance ───────────────────────────────────────────────────────────────

def test_dirty_worktree_warning_and_flag(tmp_repo: Path):
    (tmp_repo / "untracked_scratch.txt").write_text("scratch")
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.provenance.dirty is True
    assert any("dirty worktree" in n.title.lower() for n in m.warnings)
    assert "dirty" in render_html(m)


def test_clean_worktree_no_dirty_warning(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.provenance.dirty is False
    assert not any("dirty worktree" in n.title.lower() for n in m.warnings)


def test_exact_commit_rendered(tmp_repo: Path):
    full_sha = subprocess.run(
        ["git", "-C", str(tmp_repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.provenance.commit_sha == full_sha
    html = render_html(m)
    assert full_sha in html  # exact 40-char commit is in the provenance panel


def test_git_unavailable_degrades(tmp_path: Path):
    # A directory that is not a git repo.
    plain = tmp_path / "plain"
    plain.mkdir()
    _write(plain / "holdings.yaml", "margin: {debt: 0, buffer_pct: 99, synced_at: 2026-07-22}\n")
    _write(plain / "targets.yaml", "tiers: {}\nmargin: {leverage_cap: 1.8, buffer_floor_pct: 30}\n")
    m = build_model(plain, now=FIXED_NOW)
    assert m.provenance.git_available is False
    assert any("git metadata unavailable" in n.title.lower() for n in m.warnings)


# ── gated cash / SPCX / SKHY / no-renormalization ────────────────────────────

def test_gated_names_displayed_as_cash(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    gt = {g.ticker for g in m.gated_names}
    assert {"SPCX", "RKLB"} <= gt
    html = render_html(m)
    assert "HOLD TARGET IN CASH" in html


def test_spcx_hold_no_add_language(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "SPCX" in html
    assert "not a directive to" in html.lower() or "not sell" in html.lower() \
        or "hold target in cash" in html.lower()


def test_skhy_unresolved_presentation(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.skhy_unresolved is True
    assert "SKHY unresolved" in render_html(m)


def test_no_renormalization_language(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "renormaliz" in html.lower()  # explicit "never renormalized" framing


def test_gated_evidence_never_merged_into_holdings(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    holding_tickers = {h.ticker for h in m.holdings}
    # SPCX/RKLB are gated-policy rows; they are NOT injected as holdings.
    assert "RKLB" not in holding_tickers  # not in the fixture's shares
    assert m.gated_names_source.lower().startswith("phq-2026-01")


# ── allocation check ─────────────────────────────────────────────────────────

def test_allocation_unavailable_and_no_order_language(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.allocation_available is False
    assert m.allocation_unavailable_reasons
    html = render_html(m)
    assert "Recommendation unavailable" in html


# ── HTML safety / offline / escaping ─────────────────────────────────────────

def test_html_escaping_of_injected_content(tmp_repo: Path):
    # Inject an XSS-ish string via a workstream title.
    ws = tmp_repo / "operations/WORKSTREAMS.yaml"
    ws.write_text(
        "workstreams:\n"
        "  - id: WS-0099\n"
        "    title: \"<script>alert('x')</script> & <b>bold</b>\"\n"
        "    status: authorized\n"
        "    priority: primary\n"
    )
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "<script>alert('x')</script>" not in html
    assert "&lt;script&gt;alert" in html


def test_no_external_asset_references(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    # No external network resources of any kind.
    assert "https://" not in html
    assert "http://" not in html
    assert "//cdn" not in html
    assert "<link" not in html  # no external stylesheet
    assert re.search(r'src\s*=\s*["\']https?:', html) is None


def test_no_order_or_mutation_controls(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW)).lower()
    assert "<form" not in html
    # The only <input> this dashboard may ever contain is the Governance
    # Decision Explorer's local, read-only search box (OPS-0013 section 9):
    # type="search", never inside a <form>, so it can never submit or mutate
    # anything. Any other <input> type (text/submit/button/checkbox/etc.)
    # would be a regression toward an order or mutation control.
    for m in re.finditer(r"<input\b[^>]*>", html):
        assert 'type="search"' in m.group(0), m.group(0)
    for word in (">buy<", ">sell<", ">submit<", "onclick=\"buy", "place order"):
        assert word not in html


def test_deterministic_render_modulo_timestamp(tmp_repo: Path):
    a = render_html(build_model(tmp_repo, now=FIXED_NOW))
    b = render_html(build_model(tmp_repo, now=datetime(2030, 1, 1, tzinfo=timezone.utc)))
    norm = lambda s: re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", "<TS>", s)
    assert norm(a) == norm(b)


def test_structural_html_assertions(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert html.startswith("<!DOCTYPE html>")
    assert html.count("<html") == 1 and html.count("</html>") == 1
    assert '<html lang="en">' in html
    # Dashboard 2.0: five-area information architecture (OPS-0012 section 3).
    for sid in ("overview", "portfolio", "intelligence", "governance", "system"):
        assert f'id="{sid}"' in html
        assert f'<section id="{sid}" data-view' in html
    assert "skip-link" in html  # accessibility skip link
    assert html.count("<main") == 1


# ── Dashboard 2.0: information architecture, navigation, accessibility ──────

def test_five_navigation_areas_exist(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    for sid in ("overview", "portfolio", "intelligence", "governance", "system"):
        assert f'data-target="{sid}"' in html
    assert html.count('data-target="') == 5


def test_active_navigation_semantics(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    nav_start = html.index('<nav class="primary-nav"')
    nav_end = html.index("</nav>")
    nav_html = html[nav_start:nav_end]
    # Exactly one nav link is aria-current="page" at render time (Overview,
    # the first/default view); JS updates this at runtime on click. (The CSS
    # `a[aria-current="page"]` selector legitimately contains the same
    # substring, so this is scoped to the <nav> markup, not the whole page.)
    assert nav_html.count('aria-current="page"') == 1
    idx = nav_html.index('aria-current="page"')
    assert 'data-target="overview"' in nav_html[max(0, idx - 200):idx + 40]


def test_semantic_landmarks_present(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert 'role="banner"' in html
    assert "<nav " in html
    assert '<main class="content" id="main">' in html
    assert "<footer" in html
    assert html.count("<h1") == 1


def test_heading_hierarchy_no_skipped_levels(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    # One h1; each of the five sections has exactly one h2; h3/h4 only appear
    # nested under a section (never before the first h2 or h1).
    assert html.count("<h1") == 1
    assert html.count("<h2 ") == 5
    first_h1 = html.index("<h1")
    first_h2 = html.index("<h2 ")
    first_h3 = html.index("<h3")
    assert first_h1 < first_h2 < first_h3


def test_responsive_viewport_meta_present(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html


def test_reduced_motion_css_present(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "prefers-reduced-motion: reduce" in html


def test_visible_focus_styles_present(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "focus-visible" in html
    assert "outline: 3px solid var(--accent)" in html or "outline: 2px solid var(--accent)" in html


def test_narrow_viewport_css_avoids_page_horizontal_scroll(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "overflow-x: hidden" in html  # html, body
    assert "max-width: 700px" in html  # responsive table stacking breakpoint
    assert "max-width: 900px" in html  # sidebar -> top tab strip breakpoint


def test_desktop_and_mobile_nav_structures_present(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    # Desktop: sticky sidebar. Mobile: same <nav>, reflowed to a horizontal
    # tab strip under the 900px breakpoint — one nav, two CSS presentations.
    assert 'class="primary-nav" id="primary-nav"' in html
    assert ".primary-nav ul {" in html  # desktop column layout rule
    assert "flex-direction: row;" in html  # mobile: reflows to a row


def test_js_enhanced_nav_has_static_fallback(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    # The rendered <html ...> opening tag never ships with the JS-added class
    # baked in — every section is plain, visible document flow unless the
    # script runs and adds `js-views` itself. The CSS only hides a section
    # when that class is present on <html> (progressive enhancement, not a
    # default-hidden state).
    assert html.startswith('<!DOCTYPE html>\n<html lang="en">')
    assert 'class="js-views"' not in html  # never server-rendered; JS-only
    assert html.count('<section id=') == 5
    assert "html.js-views main.content section" in html  # CSS gate, JS-only


def test_generated_html_states_non_authoritative(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "non-authoritative" in html.lower()
    assert "not a source of truth" in html.lower() or "never a source of truth" in html.lower()


def test_mobile_table_stacking_uses_data_label(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert 'data-label="Ticker"' in html
    assert "content: attr(data-label)" in html


# ── Dashboard 2.0 bounded correction: long-value wrap safety ────────────────
#
# Regression coverage for the two MATERIAL findings from the independent
# exact-head review of PR #212: (1) long, unbroken repository-backed values
# (file paths, hashes, branch names) forced real page-level horizontal
# overflow on the System / Provenance view at mobile widths, because the
# flex items holding them refused to shrink below their content's intrinsic
# width; (2) three mandatory safety-disclosure text areas rendered below
# WCAG AA contrast in both themes. Both were verified fixed via a local
# rendered-browser check (headless Chromium, 1440px/390px, dark/light, all
# five views, including a synthetic ~190-character unbroken value injected
# into both the provenance list and the dirty-worktree notice) — that
# verification isn't part of the committed suite because this repository's
# CI (`requirements.txt`, `.github/workflows/ci.yml`) has no browser
# tooling installed and none is added here. The tests below are the
# strongest deterministic (no-browser) equivalent: they check the actual
# CSS wrap-capability rules and recompute real WCAG contrast ratios from
# the stylesheet's own token values, so both would fail if either fix were
# silently reverted or weakened later.

def _css_text() -> str:
    return (Path(__file__).resolve().parent / "portfolio_hq" / "dashboard"
            / "assets" / "dashboard.css").read_text()


def _css_rule_block(css: str, selector_prefix: str) -> str:
    """Return the `{ ... }` body of the first rule whose selector text
    starts with `selector_prefix` (e.g. '.provenance-list .fname {')."""
    idx = css.index(selector_prefix)
    end = css.index("}", idx)
    return css[idx:end]


def test_long_value_css_rules_allow_shrinking_and_wrapping():
    css = _css_text()

    fname_rule = _css_rule_block(css, ".provenance-list .fname {")
    assert "min-width: 0" in fname_rule
    assert "overflow-wrap: anywhere" in fname_rule
    assert "max-width: 100%" in fname_rule

    fhash_rule = _css_rule_block(css, ".provenance-list .fhash {")
    assert "min-width: 0" in fhash_rule
    assert "overflow-wrap: anywhere" in fhash_rule
    assert "max-width: 100%" in fhash_rule

    # code/.mono carries the dirty-worktree path list and other inline
    # repository-backed values outside the provenance list specifically.
    code_rule = _css_rule_block(css, "code, .mono {")
    assert "overflow-wrap: anywhere" in code_rule
    assert "max-width: 100%" in code_rule

    # Mobile card-stacked table cells (below the 700px breakpoint) are
    # themselves flex containers and share the same shrink/overflow risk
    # for an unusually long cell value.
    mobile_cell_rule = _css_rule_block(css, ".table-scroll td, .table-scroll th {")
    assert "overflow-wrap: anywhere" in mobile_cell_rule


def test_long_unbroken_dirty_path_is_rendered_fully_not_truncated(tmp_repo: Path):
    """A pathologically long, unbroken (no spaces) untracked filename — the
    same shape of value that broke the mobile System/Provenance view before
    this correction — must appear in the rendered HTML complete and
    unmodified. The fix relies on CSS wrapping, not truncation: asserting
    the full value survives byte-for-byte guards against a future 'fix'
    that silently truncates or elides provenance data instead of wrapping
    it (explicitly prohibited by the correction's own instructions).
    """
    long_name = ("Extraordinarily_Long_Unbroken_RepositoryBackedValue_"
                 + ("X" * 120) + "_end.txt")
    (tmp_repo / long_name).write_text("scratch")
    m = build_model(tmp_repo, now=FIXED_NOW)
    assert m.provenance.dirty is True
    # dirty_paths holds raw `git status --porcelain` lines (e.g. "?? name"),
    # not bare filenames.
    assert any(long_name in p for p in (m.provenance.dirty_paths or [])), (
        m.provenance.dirty_paths)
    html = render_html(m)
    assert long_name in html  # present in full — not truncated, not elided


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        c_norm = c / 255
        return c_norm / 12.92 if c_norm <= 0.03928 else ((c_norm + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def _contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = _relative_luminance(_hex_to_rgb(hex1))
    l2 = _relative_luminance(_hex_to_rgb(hex2))
    l1, l2 = max(l1, l2), min(l1, l2)
    return (l1 + 0.05) / (l2 + 0.05)


def _parse_root_color_vars(css: str, *, light: bool) -> dict[str, str]:
    """Extract `--name: #hex;` custom-property values from the dashboard
    stylesheet's default (dark) `:root` block, or from its
    `@media (prefers-color-scheme: light) { :root { ... } }` override."""
    if light:
        media_start = css.index("@media (prefers-color-scheme: light)")
        block_start = css.index(":root", media_start)
    else:
        block_start = css.index(":root")
    open_brace = css.index("{", block_start)
    depth, i = 0, open_brace
    while True:
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    block = css[open_brace:i]
    return dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})", block))


def test_safety_disclosure_text_meets_wcag_aa_contrast_both_themes():
    """The mandatory read-only / recommendation-only / local-only / no-
    brokerage-connection / no-order-path disclosure — rendered in
    `.readonly-banner`, `.primary-nav .nav-foot`, and `footer.page-footer`
    — must meet WCAG AA (>= 4.5:1) for normal-size text against its actual
    background, in both the dark (default) and light
    (`prefers-color-scheme: light`) themes. This recomputes the real ratio
    from the stylesheet's own current token values rather than only
    checking which token name is referenced, so it fails if the *color
    values* regress even without a token rename.
    """
    css = _css_text()
    dark_vars = _parse_root_color_vars(css, light=False)
    light_vars = _parse_root_color_vars(css, light=True)

    # (selector prefix, the CSS variable supplying this rule's real
    # background — verified by direct inspection of the stylesheet).
    checks = [
        (".readonly-banner {", "--surface"),
        (".primary-nav .nav-foot {", "--surface"),
        ("footer.page-footer {", "--bg"),  # no own background; inherits body's
    ]
    for selector, bg_var in checks:
        block = _css_rule_block(css, selector)
        match = re.search(r"color:\s*var\((--[\w-]+)\)", block)
        assert match, f"no `color: var(--...)` found in {selector!r}"
        fg_var = match.group(1)
        for theme_name, theme_vars in (("dark", dark_vars), ("light", light_vars)):
            fg_hex = theme_vars[fg_var]
            bg_hex = theme_vars[bg_var]
            ratio = _contrast_ratio(fg_hex, bg_hex)
            assert ratio >= 4.5, (
                f"{selector!r} in the {theme_name} theme: {fg_var}={fg_hex} "
                f"on {bg_var}={bg_hex} is only {ratio:.2f}:1, below the "
                f"WCAG AA 4.5:1 minimum for normal-size text"
            )


# ── measured AI/platform figure: point-in-time qualification ─────────────────

def test_measured_ai_platform_figure_qualified_as_point_in_time(tmp_repo: Path):
    _write_due_diligence_json(tmp_repo, (
        "{\"lookthrough_summary\": {"
        "\"approved_ai_platform_common_driver_ceiling\": 0.40, "
        "\"effective_ai_platform_common_driver_estimate\": 0.4003}}"
    ))
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "measured ~40.03%" in html
    # The qualifier must sit with the measured figure itself, not only appear
    # in the (unrelated) fallback branch shown when no figure is available.
    idx = html.index("measured ~40.03%")
    nearby = html[idx:idx + 120]
    assert "point-in-time" in nearby
    assert "PHQ-2026-01" in nearby


def test_measured_ai_platform_figure_absent_still_qualified(tmp_repo: Path):
    # No due-diligence JSON at all (tmp_repo's default) — the "no figure"
    # branch must still say point-in-time / point to the evidence.
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "measured figure unavailable" in html
    assert "point-in-time" in html


# ── sortable table headers: real <button> + aria-sort, not role="button" ─────

def test_sortable_headers_use_button_not_role_attribute(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert 'role="button"' not in html
    assert html.count('<button type="button" class="th-sort">') == 5
    assert "aria-sort" in _JS_BLOCK(html)


def _JS_BLOCK(html: str) -> str:
    start = html.index("<script>")
    end = html.index("</script>", start)
    return html[start:end]


def test_sortable_js_manages_aria_sort_not_manual_keyboard_handling(tmp_repo: Path):
    js = _JS_BLOCK(render_html(build_model(tmp_repo, now=FIXED_NOW)))
    assert "setAttribute('aria-sort'" in js
    assert "button.th-sort" in js
    # No hand-rolled keyboard activation — a real <button> gets that for free.
    assert "keydown" not in js


# ── source-of-truth integrity: no historical HTML as operational input ───────

def test_no_html_files_in_declared_inputs():
    assert not any(str(p).lower().endswith(".html") for p in model_mod.INPUT_FILES)


def test_declared_inputs_are_structured_sources_only():
    allowed = (".yaml", ".yml", ".csv", ".json", ".md")
    assert all(str(p).lower().endswith(allowed) for p in model_mod.INPUT_FILES)


def test_due_diligence_json_is_a_declared_input():
    # The structured evidence backing the 8%/40% ceilings and the measured
    # AI/platform figure must itself be provenance-hashed and disclosed, not
    # read invisibly out-of-band.
    assert model_mod.DUE_DILIGENCE_JSON_REL in model_mod.INPUT_FILES


def test_due_diligence_json_hashed_in_provenance(tmp_repo: Path):
    _write_due_diligence_json(tmp_repo, "{\"lookthrough_summary\": {}}")
    m = build_model(tmp_repo, now=FIXED_NOW)
    matching = [i for i in m.provenance.inputs
                if i.path == model_mod.DUE_DILIGENCE_JSON_REL]
    assert len(matching) == 1
    assert matching[0].exists is True
    assert matching[0].sha256 is not None


def test_historical_html_not_parsed_or_embedded(tmp_repo: Path):
    """A booby-trapped historical HTML file under governance/evidence carrying a
    unique sentinel must never appear in the model or the rendered output, and
    must never be part of the provenance input lineage."""
    sentinel = "SENTINEL_HISTORICAL_HTML_DO_NOT_READ_9f3a"
    evil = (tmp_repo / "governance/evidence/PHQ-2026-01/final_due_diligence"
            / "Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.html")
    _write(evil, f"<html><body><h1>{sentinel}</h1><p>account_equity: 999999</p></body></html>")
    # Re-commit so the tree is clean and the .html is tracked but ignored by loaders.
    _git(tmp_repo, "add", "-A")
    _git(tmp_repo, "commit", "-qm", "add historical html")

    m = build_model(tmp_repo, now=FIXED_NOW)
    html = render_html(m)
    assert sentinel not in html
    assert "999999" not in html
    # The .html is not among the hashed provenance inputs.
    assert not any(str(f.path).lower().endswith(".html") for f in m.provenance.inputs)


def test_provenance_inputs_have_no_html(tmp_repo: Path):
    m = build_model(tmp_repo, now=FIXED_NOW)
    for f in m.provenance.inputs:
        assert not str(f.path).lower().endswith(".html")


# ── server: localhost-only binding, read-only ────────────────────────────────

def test_server_binds_localhost_and_serves(tmp_repo: Path):
    handler = _make_handler(tmp_repo)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    assert httpd.server_address[0] == "127.0.0.1"
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
            assert "Portfolio-HQ Dashboard" in body
        # 404 for anything but root.
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/secret", timeout=5)
            raised = False
        except urllib.error.HTTPError as e:
            raised = e.code == 404
        assert raised
        # Read-only: every mutating method is rejected, not just POST.
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}/", data=b"x", method=method)
            try:
                urllib.request.urlopen(req, timeout=5)
                blocked = False
            except urllib.error.HTTPError as e:
                blocked = e.code == 405
            assert blocked, f"{method} was not rejected with 405"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_overview_shows_notice_counts_and_provenance_stays_visible(tmp_repo: Path):
    html = render_html(build_model(tmp_repo, now=FIXED_NOW))
    assert "blocker(s)" in html and "warning(s)" in html
    assert "Authoritative inputs" in html
    assert "sha256:" in html


# ── CLI smoke tests ──────────────────────────────────────────────────────────

def test_cli_build_writes_file(tmp_repo: Path, tmp_path: Path, capsys):
    out = tmp_path / "out" / "dash.html"
    rc = cli_main(["--repo-root", str(tmp_repo), "build", "--output", str(out)])
    assert rc == 0
    assert out.exists()
    assert out.read_text().startswith("<!DOCTYPE html>")


def test_cli_build_stdout(tmp_repo: Path, capsys):
    rc = cli_main(["--repo-root", str(tmp_repo), "build", "--stdout"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "<!DOCTYPE html>" in captured.out


def test_cli_serve_help_smoke():
    # `serve` is a subcommand; verify the parser wires it up without binding.
    from portfolio_hq.dashboard.cli import build_parser
    parser = build_parser()
    ns = parser.parse_args(["serve", "--host", "127.0.0.1", "--port", "0"])
    assert ns.host == "127.0.0.1"
    assert ns.command == "serve"


def test_default_server_host_is_loopback():
    from portfolio_hq.dashboard.cli import build_parser
    ns = build_parser().parse_args(["serve"])
    assert ns.host == "127.0.0.1"  # never 0.0.0.0 by default


@pytest.mark.parametrize("host", ["127.0.0.1", "::1", "localhost", "127.4.5.6"])
def test_cli_accepts_loopback_host_variants(host):
    # OPS-0011 authorizes loopback only, not one specific literal — 127.0.0.1
    # is the default, but any loopback address/hostname must still work.
    from portfolio_hq.dashboard.cli import build_parser
    ns = build_parser().parse_args(["serve", "--host", host])
    assert ns.host == host


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.5", "10.0.0.1", "::", "example.com"])
def test_cli_rejects_non_loopback_host(host, capsys):
    # OPS-0011: binding to 0.0.0.0, a LAN address, or any other externally
    # reachable interface must not be configurable — enforced at parse time
    # so `serve()` is never reached with such a value.
    from portfolio_hq.dashboard.cli import build_parser
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["serve", "--host", host])
    assert "OPS-0011" in capsys.readouterr().err


# ── integration against the real repository ──────────────────────────────────

def test_real_repository_model_builds():
    m = build_model(REPO_ROOT, now=FIXED_NOW)
    html = render_html(m)
    assert html.startswith("<!DOCTYPE html>")
    assert m.provenance.repo_name == "Portfolio-HQ"
    assert m.gated_names  # PHQ-2026-01 gated names present
    assert m.ai_platform_measured_pct is not None  # read from structured JSON evidence
