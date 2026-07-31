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
    _write(repo / "targets.yaml", (
        "tiers:\n"
        "  T1:\n"
        "    weight_pct: 3.35\n"
        "    tickers: [NVDA]\n"
        "  band:\n"
        "    weight_pct: 0.75\n"
        "    cap_multiple: 1.25\n"
        "    tickers: [AAPL, SKHY]\n"
        "  spec:\n"
        "    weight_pct: 1.0\n"
        "    fixed: true\n"
        "    tickers: [SPCX]\n"
        "crypto:\n"
        "  sleeve_pct: 10.0\n"
        "  coins: [ETH]\n"
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
    assert m.crypto_sleeve_pct == 10.0
    # roster tier resolved from targets.yaml
    nvda = next(h for h in m.holdings if h.ticker == "NVDA")
    assert nvda.tier == "T1"


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
    assert "<input" not in html
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
    for sid in ("overview", "portfolio", "targets", "allocation",
                "concentration", "gates", "research", "governance"):
        assert f'id="{sid}"' in html
    assert "skip-link" in html  # accessibility skip link
    assert html.count("<main") == 1


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
        # Read-only: POST is rejected.
        req = urllib.request.Request(f"http://127.0.0.1:{port}/", data=b"x", method="POST")
        try:
            urllib.request.urlopen(req, timeout=5)
            post_blocked = False
        except urllib.error.HTTPError as e:
            post_blocked = e.code == 405
        assert post_blocked
    finally:
        httpd.shutdown()
        httpd.server_close()


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
