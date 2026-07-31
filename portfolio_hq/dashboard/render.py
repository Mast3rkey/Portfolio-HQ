"""Render a DashboardModel to a single self-contained HTML document.

Deterministic given the model (the only non-deterministic value, generation
time, lives on the model already). All dynamic text is HTML-escaped. No
external CSS/JS/fonts/CDN/analytics — the stylesheet is inlined and the only
script is a tiny optional progressive-enhancement helper (collapse/sort) that
the page works completely without.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from .model import DashboardModel, GatedName, HoldingRow, MarginInfo

_ASSETS = Path(__file__).resolve().parent / "assets"

# Optional, progressive-enhancement only. The page is fully usable with JS
# disabled: <details> handles collapsing natively; a sortable header's text is
# still plain, readable column-header text without it. Each sortable header's
# markup is a real <button> inside the <th> (native keyboard/focus/click
# semantics, no manual role/tabindex reimplementation); this script only wires
# up the click handler and maintains aria-sort on the <th> itself.
_JS = """
(function () {
  document.querySelectorAll('table[data-sortable] thead th').forEach(function (th, idx) {
    var btn = th.querySelector('button.th-sort');
    if (!btn) { return; }
    function sort() {
      var table = th.closest('table');
      var tbody = table.tBodies[0];
      var rows = Array.prototype.slice.call(tbody.rows);
      var ascending = th.getAttribute('aria-sort') !== 'ascending';
      rows.sort(function (a, b) {
        var x = a.cells[idx] ? a.cells[idx].getAttribute('data-sort') || a.cells[idx].textContent : '';
        var y = b.cells[idx] ? b.cells[idx].getAttribute('data-sort') || b.cells[idx].textContent : '';
        var nx = parseFloat(x), ny = parseFloat(y);
        var cmp = (!isNaN(nx) && !isNaN(ny)) ? (nx - ny) : x.localeCompare(y);
        return ascending ? cmp : -cmp;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
      table.querySelectorAll('thead th').forEach(function (h) { h.removeAttribute('aria-sort'); });
      th.setAttribute('aria-sort', ascending ? 'ascending' : 'descending');
    }
    btn.addEventListener('click', sort);
  });
})();
"""


def _esc(value: object) -> str:
    return escape("" if value is None else str(value))


def _fmt_num(value: float | None, digits: int = 6) -> str:
    if value is None:
        return '<span class="unavailable">—</span>'
    return _esc(f"{value:,.{digits}f}".rstrip("0").rstrip(".") or "0")


def _fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None:
        return '<span class="unavailable">—</span>'
    return _esc(f"{value:.{digits}f}%")


def _notice_html(model: DashboardModel) -> str:
    if not model.notices:
        return '<p class="unavailable">No warnings or blockers detected.</p>'
    parts = []
    # Order: blockers, warnings, info.
    for group in (model.blockers, model.warnings, model.infos):
        for n in group:
            parts.append(
                f'<div class="notice {_esc(n.severity)}" role="note">'
                f'<div class="n-title">{_esc(n.title)}</div>'
                f'<div class="n-detail">{_esc(n.detail)}</div></div>'
            )
    return "\n".join(parts)


def _overview(model: DashboardModel) -> str:
    p = model.provenance
    worktree_badge = (
        '<span class="badge warning">dirty</span>'
        if p.dirty
        else '<span class="badge ok">clean</span>'
    )
    commit = _esc(p.commit_short or "unknown")
    cards = f"""
    <div class="cards">
      <div class="card"><div class="label">Source commit</div>
        <div class="value"><code>{commit}</code> {worktree_badge}</div>
        <div class="sub">branch <code>{_esc(p.branch or "?")}</code></div></div>
      <div class="card"><div class="label">Generated</div>
        <div class="value">{_esc(p.generated_at_iso)}</div>
        <div class="sub">UTC, at build time</div></div>
      <div class="card"><div class="label">Holdings effective</div>
        <div class="value">{_esc(model.holdings_effective_date or "unknown")}</div>
        <div class="sub">{_esc(model.holdings_effective_source)}</div></div>
      <div class="card"><div class="label">Controlling policy</div>
        <div class="value">{_esc(", ".join(model.controlling_decisions) or "—")}</div>
        <div class="sub">accepted governance decisions</div></div>
    </div>"""
    return f"""
    <section id="overview" aria-labelledby="overview-h">
      <h2 id="overview-h">Overview</h2>
      <p class="lede">Read-only snapshot derived entirely from this repository's
        committed state. It places no orders and connects to no brokerage.</p>
      {cards}
      <h3>Warnings &amp; blockers</h3>
      {_notice_html(model)}
    </section>"""


def _portfolio(model: DashboardModel) -> str:
    rows = []
    for h in model.holdings:
        if h.kind == "manual":
            qty_cell = '<span class="unavailable">n/a</span>'
            val_cell = _fmt_num(h.manual_value, 2)
            sort_key = h.manual_value or 0
        else:
            qty_cell = _fmt_num(h.quantity, 6)
            val_cell = '<span class="unavailable">offline</span>'
            sort_key = h.quantity or 0
        rows.append(
            f"<tr><th scope=\"row\">{_esc(h.ticker)}</th>"
            f"<td>{_esc(h.kind)}</td>"
            f"<td>{_esc(h.tier or '—')}</td>"
            f'<td class="num" data-sort="{_esc(sort_key)}">{qty_cell}</td>'
            f'<td class="num">{val_cell}</td></tr>'
        )
    equity_n = sum(1 for h in model.holdings if h.kind == "equity")
    crypto_n = sum(1 for h in model.holdings if h.kind == "crypto")
    return f"""
    <section id="portfolio" aria-labelledby="portfolio-h">
      <h2 id="portfolio-h">Portfolio</h2>
      <p class="lede">{equity_n} equity position(s) and {crypto_n} crypto
        position(s), by share/coin count from <code>holdings.yaml</code>.
        Live market values are <strong>not</strong> computed by this offline
        dashboard.</p>
      <div class="table-scroll">
      <table data-sortable>
        <caption>Positions — quantities are authoritative; dollar values require a networked allocator run.</caption>
        <thead><tr>{"".join(
            f'<th scope="col"{cls}><button type="button" class="th-sort">{label}</button></th>'
            for label, cls in (
                ("Ticker", ""), ("Kind", ""), ("Tier", ""),
                ("Quantity", ' class="num"'), ("Market value", ' class="num"'),
            )
        )}</tr></thead>
        <tbody>{''.join(rows) or '<tr><td colspan="5" class="unavailable">No positions found.</td></tr>'}</tbody>
      </table>
      </div>
    </section>"""


def _targets(model: DashboardModel) -> str:
    tier_rows = []
    for t in model.tiers:
        cap = f"{t.cap_multiple:g}×" if t.cap_multiple and t.cap_multiple != 1.0 else "—"
        flags = "fixed" if t.fixed else "—"
        tier_rows.append(
            f"<tr><th scope=\"row\">{_esc(t.name)}</th>"
            f'<td class="num">{_fmt_pct(t.weight_pct)}</td>'
            f"<td>{_esc(cap)}</td><td>{_esc(flags)}</td>"
            f'<td class="num">{len(t.tickers)}</td>'
            f"<td>{_esc(', '.join(t.tickers))}</td></tr>"
        )
    sleeve = _fmt_pct(model.crypto_sleeve_pct)
    return f"""
    <section id="targets" aria-labelledby="targets-h">
      <h2 id="targets-h">Targets</h2>
      <p class="lede">Canonical tier structure from <code>targets.yaml</code> —
        the sole authoritative target file. Current-vs-target dollar comparison
        is intentionally omitted: it needs live prices and reconciled holdings
        this dashboard does not have. Gated cash is never renormalized into
        other positions (see Gates &amp; Open Decisions).</p>
      <div class="table-scroll">
      <table>
        <caption>Tier targets (per-name weight of book).</caption>
        <thead><tr><th scope="col">Tier</th><th scope="col" class="num">Weight</th>
          <th scope="col">Cap</th><th scope="col">Sizing</th>
          <th scope="col" class="num"># names</th><th scope="col">Tickers</th></tr></thead>
        <tbody>{''.join(tier_rows)}</tbody>
      </table>
      </div>
      <p>Crypto sleeve target: <strong>{sleeve}</strong> of book (tracked, not traded by the allocator).</p>
    </section>"""


def _allocation(model: DashboardModel) -> str:
    reasons = "".join(f"<li>{_esc(r)}</li>" for r in model.allocation_unavailable_reasons)
    return f"""
    <section id="allocation" aria-labelledby="allocation-h">
      <h2 id="allocation-h">Allocation Check</h2>
      <p class="lede">No current allocation recommendation is available from this
        dashboard.</p>
      <div class="notice info" role="note">
        <div class="n-title">Recommendation unavailable — controlling state is
          incomplete or requires live data</div>
        <div class="n-detail">This read-only presentation layer deliberately does
          not run the allocator or build a second one. It never produces
          executable orders. To get a current, advisory-only recommendation, run
          <code>python allocate.py --review</code> (or <code>--cash X</code>) in a
          networked session after reconciling holdings.</div>
      </div>
      <ul>{reasons}</ul>
    </section>"""


def _concentration(model: DashboardModel) -> str:
    m = model.margin
    cluster_rows = "".join(
        f"<tr><th scope=\"row\">{_esc(c.name)}</th>"
        f'<td class="num">{_fmt_pct(c.pct, 1)}</td>'
        f'<td class="num">{len(c.tickers)}</td>'
        f"<td>{_esc(', '.join(c.tickers))}</td></tr>"
        for c in model.clusters
    )
    floor_state = m.below_buffer_floor
    if floor_state is True:
        floor_badge = '<span class="badge blocker">below floor</span>'
    elif floor_state is False:
        floor_badge = '<span class="badge ok">above floor</span>'
    else:
        floor_badge = '<span class="badge muted">unknown</span>'
    stale_badge = (
        f'<span class="badge warning">stale ({m.age_days}d)</span>'
        if m.stale
        else ('<span class="badge muted">age unknown</span>' if m.age_unverifiable
              else '<span class="badge ok">fresh</span>')
    )
    return f"""
    <section id="concentration" aria-labelledby="concentration-h">
      <h2 id="concentration-h">Concentration &amp; Risk</h2>
      <p class="lede">Approved limits and margin facts from repository truth only.
        No exposure figure is inferred from Robinhood screenshots or live prices.</p>
      <div class="cards">
        <div class="card"><div class="label">Margin debt</div>
          <div class="value">{('$' + format(m.debt, ',.2f')) if m.debt is not None else '—'}</div>
          <div class="sub">synced {_esc(m.synced_at or 'unknown')} {stale_badge}</div></div>
        <div class="card"><div class="label">Buffer</div>
          <div class="value">{_fmt_pct(m.buffer_pct, 2)} {floor_badge}</div>
          <div class="sub">floor {_fmt_pct(m.buffer_floor_pct, 0)} (Robinhood-displayed; verify live)</div></div>
        <div class="card"><div class="label">Leverage cap</div>
          <div class="value">{_esc(f'{m.leverage_cap:g}×') if m.leverage_cap else '—'}</div>
          <div class="sub">gross / net equity — fixed structural ceiling</div></div>
        <div class="card"><div class="label">Single-issuer ceiling</div>
          <div class="value">{_fmt_pct(model.single_issuer_ceiling_pct, 0)}</div>
          <div class="sub">PHQ-2026-01 effective-issuer limit</div></div>
        <div class="card"><div class="label">AI/platform ceiling</div>
          <div class="value">{_fmt_pct(model.ai_platform_ceiling_pct, 0)}</div>
          <div class="sub">{
            ('measured ~' + format(model.ai_platform_measured_pct, '.2f')
             + '% (point-in-time, PHQ-2026-01-derived)')
            if model.ai_platform_measured_pct is not None
            else 'measured figure unavailable — point-in-time, see PHQ-2026-01 evidence'
          }</div></div>
      </div>
      <p class="lede">Leverage ratio and live cluster proximity are not shown:
        they require a live gross valuation this offline dashboard does not compute.</p>
      <div class="table-scroll">
      <table>
        <caption>Correlated-cluster caps (each ≤ its % of book) from <code>targets.yaml</code>.</caption>
        <thead><tr><th scope="col">Cluster</th><th scope="col" class="num">Cap</th>
          <th scope="col" class="num"># names</th><th scope="col">Tickers</th></tr></thead>
        <tbody>{cluster_rows}</tbody>
      </table>
      </div>
    </section>"""


def _gates(model: DashboardModel) -> str:
    gated_rows = "".join(
        f"<tr><th scope=\"row\">{_esc(g.ticker)}</th>"
        f'<td class="num">{_fmt_pct((g.target_weight or 0) * 100, 2) if g.target_weight is not None else "—"}</td>'
        f"<td>{_esc(g.status)}</td>"
        f"<td>{_esc(g.next_gate)}</td></tr>"
        for g in model.gated_names
    )
    skhy = (
        '<div class="notice warning" role="note"><div class="n-title">SKHY unresolved</div>'
        '<div class="n-detail">SKHY is a live band holding but is explicitly not '
        'addressed by PHQ-2026-01 and remains an open item (see CLAUDE.md). It is '
        'not silently brought under any transition architecture.</div></div>'
        if model.skhy_unresolved
        else '<p class="unavailable">SKHY not present in current holdings.</p>'
    )
    spcx = (
        '<div class="notice info" role="note"><div class="n-title">SPCX — HOLD TARGET IN CASH</div>'
        '<div class="n-detail">SPCX is gated: its target capital is held in cash '
        '(no currently approved investable vehicle). This is not a directive to '
        'sell any existing SPCX position. Advisory / governance status only.</div></div>'
    )
    return f"""
    <section id="gates" aria-labelledby="gates-h">
      <h2 id="gates-h">Gates &amp; Open Decisions</h2>
      <p class="lede">{_esc(model.gated_names_source)}. Displayed as governance
        policy — never merged into live holdings or fed to the allocator.</p>
      <div class="table-scroll">
      <table>
        <caption>PHQ-2026-01 gated names — target capital held in cash until each is individually cleared.</caption>
        <thead><tr><th scope="col">Ticker</th><th scope="col" class="num">Target wt</th>
          <th scope="col">Status</th><th scope="col">Next gate / evidence needed</th></tr></thead>
        <tbody>{gated_rows or '<tr><td colspan="4" class="unavailable">Gated-name policy evidence not available.</td></tr>'}</tbody>
      </table>
      </div>
      {spcx}
      {skhy}
    </section>"""


def _research(model: DashboardModel) -> str:
    intel = model.intelligence
    note = (
        f'<div class="notice warning" role="note"><div class="n-title">Degraded</div>'
        f'<div class="n-detail">{_esc(intel.note)}</div></div>'
        if intel.note
        else ""
    )
    overdue = (
        "".join(f"<li><code>{_esc(t)}</code> — {_esc(d)}</li>" for t, d in intel.overdue_reviews)
        or '<li class="unavailable">None overdue.</li>'
    )
    drift = (
        "".join(f"<li><code>{_esc(t)}</code> — {_esc(d)}</li>" for t, d in intel.role_drift_mismatches)
        or '<li class="unavailable">No role drift detected.</li>'
    )
    invalid = (
        ", ".join(intel.schema_invalid) if intel.schema_invalid else "none"
    )
    return f"""
    <section id="research" aria-labelledby="research-h">
      <h2 id="research-h">Research &amp; Freshness</h2>
      <p class="lede">Company / Theme Intelligence coverage and freshness, via the
        repository's own <code>intelligence_report</code> reporting API (read-only).</p>
      {note}
      <div class="cards">
        <div class="card"><div class="label">Company records</div>
          <div class="value">{intel.company_yaml_count}</div>
          <div class="sub">{intel.company_markdown_count} thesis docs</div></div>
        <div class="card"><div class="label">Themes</div>
          <div class="value">{intel.theme_yaml_count}</div>
          <div class="sub">{intel.theme_markdown_count} theme docs</div></div>
        <div class="card"><div class="label">Freshness rows</div>
          <div class="value">{intel.freshness_rows}</div>
          <div class="sub">{intel.monitoring_enabled_rows} monitoring-enabled</div></div>
        <div class="card"><div class="label">Schema-invalid</div>
          <div class="value">{len(intel.schema_invalid)}</div>
          <div class="sub">{_esc(invalid)}</div></div>
      </div>
      <details>
        <summary>Overdue reviews &amp; role drift</summary>
        <h4>Overdue reviews</h4><ul>{overdue}</ul>
        <h4>Portfolio-role drift (advisory — targets.yaml always wins)</h4><ul>{drift}</ul>
      </details>
    </section>"""


def _governance(model: DashboardModel) -> str:
    p = model.provenance
    input_rows = "".join(
        f'<li><span class="fname">{_esc(f.path)}</span> '
        + (
            f'<span class="fhash">sha256:{_esc(f.sha256)} · {f.size_bytes} B</span>'
            if f.exists
            else '<span class="badge warning">missing</span>'
        )
        + "</li>"
        for f in p.inputs
    )
    ws_rows = "".join(
        f"<tr><th scope=\"row\">{_esc(w.ws_id)}</th>"
        f"<td>{_esc(w.title or '—')}</td>"
        f"<td>{_esc(w.status or '—')}</td>"
        f"<td>{_esc(w.priority or '—')}</td></tr>"
        for w in model.workstreams
    )
    dec_rows = "".join(
        f"<tr><th scope=\"row\">{_esc(d.decision_id)}</th>"
        f"<td>{_esc(d.date or '—')}</td>"
        f"<td>{_esc(d.status or '—')}</td>"
        f"<td>{_esc(d.category or '—')}</td></tr>"
        for d in model.decisions[-25:]
    )
    dirty_detail = ""
    if p.dirty:
        lines = "".join(f"<li><code>{_esc(ln)}</code></li>" for ln in p.dirty_paths)
        dirty_detail = (
            '<div class="notice warning" role="note"><div class="n-title">'
            "Uncommitted changes at generation</div><div class=\"n-detail\">"
            "This page is NOT authoritative for any committed state.</div>"
            f"<ul>{lines}</ul></div>"
        )
    return f"""
    <section id="governance" aria-labelledby="governance-h">
      <h2 id="governance-h">Governance &amp; Provenance</h2>
      <p class="lede">Exactly which repository state produced this page.</p>
      <div class="cards">
        <div class="card"><div class="label">Repository</div>
          <div class="value">{_esc(p.repo_name)}</div></div>
        <div class="card"><div class="label">Commit (full)</div>
          <div class="value mono" style="font-size:13px">{_esc(p.commit_display)}</div>
          <div class="sub">{_esc(p.commit_subject or '')}</div></div>
        <div class="card"><div class="label">Committed</div>
          <div class="value">{_esc(p.commit_iso or 'unknown')}</div></div>
      </div>
      {dirty_detail}
      <h3>Authoritative inputs (with content hashes)</h3>
      <ul class="provenance-list">{input_rows}</ul>
      <details>
        <summary>Workstream register ({len(model.workstreams)})</summary>
        <div class="table-scroll"><table>
          <thead><tr><th scope="col">ID</th><th scope="col">Title</th>
            <th scope="col">Status</th><th scope="col">Priority</th></tr></thead>
          <tbody>{ws_rows or '<tr><td colspan="4" class="unavailable">No workstreams parsed.</td></tr>'}</tbody>
        </table></div>
      </details>
      <details>
        <summary>Governance decision index (latest 25 of {len(model.decisions)})</summary>
        <div class="table-scroll"><table>
          <thead><tr><th scope="col">ID</th><th scope="col">Date</th>
            <th scope="col">Status</th><th scope="col">Category</th></tr></thead>
          <tbody>{dec_rows or '<tr><td colspan="4" class="unavailable">No decisions parsed.</td></tr>'}</tbody>
        </table></div>
      </details>
      <details>
        <summary>Historical evidence links (not parsed as current state)</summary>
        <p class="lede">Retained under <code>governance/evidence/PHQ-2026-01/</code>.
          These are point-in-time artifacts; this dashboard links but never derives
          current holdings from them.</p>
        <ul>
          <li><code>governance/evidence/PHQ-2026-01/README.md</code></li>
          <li><code>governance/evidence/PHQ-2026-01/final_due_diligence/</code></li>
          <li><code>governance/evidence/PHQ-2026-01/authority/LIVE_STATE_BOUNDARY.md</code></li>
        </ul>
      </details>
    </section>"""


def _toc() -> str:
    items = [
        ("overview", "Overview"),
        ("portfolio", "Portfolio"),
        ("targets", "Targets"),
        ("allocation", "Allocation Check"),
        ("concentration", "Concentration &amp; Risk"),
        ("gates", "Gates &amp; Decisions"),
        ("research", "Research &amp; Freshness"),
        ("governance", "Governance &amp; Provenance"),
    ]
    return '<nav class="toc" aria-label="Sections">' + "".join(
        f'<a href="#{i}">{label}</a>' for i, label in items
    ) + "</nav>"


def render_html(model: DashboardModel) -> str:
    """Render the model to a complete, offline, self-contained HTML string."""
    css = (_ASSETS / "dashboard.css").read_text()
    p = model.provenance
    n_block = len(model.blockers)
    n_warn = len(model.warnings)
    status_summary = (
        f'<span class="badge blocker">{n_block} blocker(s)</span> '
        if n_block
        else ""
    ) + (
        f'<span class="badge warning">{n_warn} warning(s)</span>'
        if n_warn
        else '<span class="badge ok">no warnings</span>'
    )
    dirty_flag = ' · <span class="badge warning">dirty worktree</span>' if p.dirty else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Portfolio-HQ Dashboard — {_esc(p.commit_short or 'local')}</title>
<style>{css}</style>
</head>
<body>
<a class="skip-link" href="#overview">Skip to content</a>
<header class="statusbar" role="banner">
  <h1>Portfolio-HQ Dashboard</h1>
  <span class="meta">commit <code>{_esc(p.commit_short or 'unknown')}</code>
    on <code>{_esc(p.branch or '?')}</code>{dirty_flag}</span>
  <span class="meta">generated {_esc(p.generated_at_iso)}</span>
  <span class="meta">{status_summary}</span>
</header>
<div class="readonly-banner" role="note">Read-only · recommendation-only · local-only · no brokerage connection · no order path</div>
<main class="wrap" id="main">
  {_toc()}
  {_overview(model)}
  {_portfolio(model)}
  {_targets(model)}
  {_allocation(model)}
  {_concentration(model)}
  {_gates(model)}
  {_research(model)}
  {_governance(model)}
</main>
<footer class="page-footer">
  Portfolio-HQ repository-native dashboard · derived from commit
  <code>{_esc(p.commit_display)}</code> · generated {_esc(p.generated_at_iso)} ·
  This is a presentation layer, not portfolio authority. holdings.yaml,
  targets.yaml, and accepted decisions remain the sole sources of truth.
</footer>
<script>{_JS}</script>
</body>
</html>
"""
