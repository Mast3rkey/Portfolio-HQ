"""Render a DashboardModel to a single self-contained HTML document.

Deterministic given the model (the only non-deterministic value, generation
time, lives on the model already). All dynamic text is HTML-escaped. No
external CSS/JS/fonts/CDN/analytics — the stylesheet is inlined and the only
script is a small, optional progressive-enhancement helper (section
switching + column sort) that the page works completely without: every
section is a normal, visible, anchor-linkable part of the page; JavaScript
only adds the single-view "app" feel and live re-sorting on top of that
static document.

Dashboard 2.0 (OPS-0012) reorganizes the same repository-backed facts the
Dashboard 1.0 model already exposed into five areas — Overview, Portfolio,
Intelligence, Governance, System/Provenance — and restyles them. No new
investment calculation, portfolio fact, or Intelligence conclusion is added
here; every value below traces to an existing `DashboardModel` field.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from .model import DashboardModel, GatedName, HoldingRow, MarginInfo

_ASSETS = Path(__file__).resolve().parent / "assets"

# Optional, progressive-enhancement only. The page is fully usable with JS
# disabled: every section is plain, visible document flow reachable by
# anchor link; <details> handles collapsing natively; a sortable header's
# text is still plain, readable column-header text without it. With JS, the
# five sections behave as single-page "views" (one visible at a time, nav
# updates aria-current, the URL hash tracks the active view) and table
# sorting is wired onto the existing real <button> inside each <th> (native
# keyboard/focus/click semantics — no manual role/tabindex reimplementation).
_JS = """
(function () {
  var doc = document.documentElement;
  var sections = Array.prototype.slice.call(
    document.querySelectorAll('main.content section[data-view]'));
  var links = Array.prototype.slice.call(
    document.querySelectorAll('#primary-nav a[data-target]'));

  if (sections.length && links.length) {
    doc.classList.add('js-views');

    function activate(id, opts) {
      opts = opts || {};
      var found = false;
      sections.forEach(function (s) {
        var on = s.id === id;
        if (on) { found = true; }
        s.classList.toggle('active', on);
      });
      if (!found) { sections[0].classList.add('active'); id = sections[0].id; }
      links.forEach(function (a) {
        if (a.getAttribute('data-target') === id) {
          a.setAttribute('aria-current', 'page');
        } else {
          a.removeAttribute('aria-current');
        }
      });
      if (!opts.skipHash && history.replaceState) {
        history.replaceState(null, '', '#' + id);
      }
      if (!opts.skipScroll) { window.scrollTo(0, 0); }
    }

    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('data-target');
        if (!id) { return; }
        e.preventDefault();
        activate(id);
      });
    });

    var initial = (window.location.hash || '').slice(1);
    activate(initial || sections[0].id, {skipHash: true, skipScroll: true});
  }

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

_NAV_ITEMS = (
    ("overview", "Overview", "◇"),
    ("portfolio", "Portfolio", "▦"),
    ("intelligence", "Intelligence", "◈"),
    ("governance", "Governance", "⚖"),
    ("system", "System", "⚙"),
)


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


def _cell(label: str, html: str, *, header: bool = False, num: bool = False,
          sort: object = None) -> str:
    """One <td>/<th> with a data-label for the narrow-viewport stacked
    presentation (see dashboard.css's responsive-table rule)."""
    tag = "th" if header else "td"
    scope = ' scope="row"' if header else ""
    cls = ' class="num"' if num else ""
    sort_attr = f' data-sort="{_esc(sort)}"' if sort is not None else ""
    return f'<{tag}{scope}{cls} data-label="{_esc(label)}"{sort_attr}>{html}</{tag}>'


def _notice_html(notices) -> str:
    icons = {"blocker": "⛔", "warning": "⚠", "info": "ℹ"}
    if not notices:
        return '<p class="unavailable">No warnings or blockers detected.</p>'
    parts = []
    for n in notices:
        icon = icons.get(n.severity, "•")
        parts.append(
            f'<div class="notice {_esc(n.severity)}" role="note">'
            f'<span class="n-icon" aria-hidden="true">{icon}</span>'
            f'<div class="n-body"><div class="n-title">{_esc(n.title)}</div>'
            f'<div class="n-detail">{_esc(n.detail)}</div></div></div>'
        )
    return f'<div class="notice-list">{"".join(parts)}</div>'


def _ordered_notices(model: DashboardModel):
    # blockers, then warnings, then info — most severe first.
    return list(model.blockers) + list(model.warnings) + list(model.infos)


def _sort_headers(labels_and_classes) -> str:
    return "".join(
        f'<th scope="col"{cls}><button type="button" class="th-sort">{label}</button></th>'
        for label, cls in labels_and_classes
    )


# ── Overview ─────────────────────────────────────────────────────────────

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

    n_positions = len(model.holdings)
    n_decisions = len(model.decisions)
    n_ws = len(model.workstreams)
    n_ws_primary = sum(1 for w in model.workstreams if (w.priority or "").lower() == "primary")
    n_overdue = len(model.intelligence.overdue_reviews)
    snapshot = f"""
    <h3>Snapshot</h3>
    <div class="cards">
      <div class="card stat-lg"><div class="label">Positions</div>
        <div class="value">{n_positions}</div>
        <div class="sub">tracked in holdings.yaml</div></div>
      <div class="card stat-lg"><div class="label">Governed targets</div>
        <div class="value">{len(model.tiers)}</div>
        <div class="sub">tier/destination groups</div></div>
      <div class="card stat-lg"><div class="label">Workstreams</div>
        <div class="value">{n_ws}</div>
        <div class="sub">{n_ws_primary} primary</div></div>
      <div class="card stat-lg"><div class="label">Decisions on record</div>
        <div class="value">{n_decisions}</div>
        <div class="sub">accepted governance index</div></div>
      <div class="card stat-lg"><div class="label">Intelligence records</div>
        <div class="value">{model.intelligence.company_yaml_count}</div>
        <div class="sub">{n_overdue} review(s) overdue</div></div>
    </div>"""

    notices = _ordered_notices(model)
    n_block, n_warn = len(model.blockers), len(model.warnings)
    priority_html = (
        f'<h3>High-priority notices</h3>{_notice_html(notices)}'
        if notices
        else '<h3>High-priority notices</h3><p class="unavailable">No warnings or blockers detected.</p>'
    )

    return f"""
    <section id="overview" data-view aria-labelledby="overview-h">
      <div class="view-head">
        <h2 id="overview-h">Overview</h2>
        <p class="lede">Read-only snapshot derived entirely from this
          repository's committed state. It places no orders and connects to
          no brokerage; <strong>{n_block} blocker(s), {n_warn} warning(s)</strong>
          detected at generation time.</p>
      </div>
      <div class="panel">{cards}{snapshot}</div>
      <div class="panel">{priority_html}</div>
      <div class="panel">
        <h3>Non-authoritative</h3>
        <p class="lede">This page is a presentation layer, not portfolio
          authority. <code>holdings.yaml</code>, <code>targets.yaml</code>,
          and accepted governance decisions remain the sole sources of
          truth — see System / Provenance for exactly which committed state
          produced this render.</p>
      </div>
    </section>"""


# ── Portfolio ────────────────────────────────────────────────────────────

def _positions_table(model: DashboardModel) -> str:
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
            "<tr>"
            + _cell("Ticker", _esc(h.ticker), header=True)
            + _cell("Kind", _esc(h.kind))
            + _cell("Tier", _esc(h.tier or "—"))
            + _cell("Quantity", qty_cell, num=True, sort=sort_key)
            + _cell("Market value", val_cell, num=True)
            + "</tr>"
        )
    equity_n = sum(1 for h in model.holdings if h.kind == "equity")
    crypto_n = sum(1 for h in model.holdings if h.kind == "crypto")
    headers = _sort_headers((
        ("Ticker", ""), ("Kind", ""), ("Tier", ""),
        ("Quantity", ' class="num"'), ("Market value", ' class="num"'),
    ))
    return f"""
    <h3>Positions</h3>
    <p class="lede">{equity_n} equity position(s) and {crypto_n} crypto
      position(s), by share/coin count from <code>holdings.yaml</code>.
      Live market values are <strong>not</strong> computed by this offline
      dashboard.</p>
    <div class="table-scroll">
    <table data-sortable>
      <caption>Positions — quantities are authoritative; dollar values require a networked allocator run.</caption>
      <thead><tr>{headers}</tr></thead>
      <tbody>{''.join(rows) or '<tr><td colspan="5" class="unavailable">No positions found.</td></tr>'}</tbody>
    </table>
    </div>"""


def _targets_table(model: DashboardModel) -> str:
    tier_rows = []
    for t in model.tiers:
        cap = f"{t.cap_multiple:g}×" if t.cap_multiple and t.cap_multiple != 1.0 else "—"
        flags = "fixed" if t.fixed else "—"
        tier_rows.append(
            "<tr>"
            + _cell("Tier", _esc(t.name), header=True)
            + _cell("Weight", _fmt_pct(t.weight_pct), num=True)
            + _cell("Cap", _esc(cap))
            + _cell("Sizing", _esc(flags))
            + _cell("# names", str(len(t.tickers)), num=True)
            + _cell("Tickers", _esc(", ".join(t.tickers)))
            + "</tr>"
        )
    sleeve = _fmt_pct(model.crypto_sleeve_pct)
    return f"""
    <h3>Targets</h3>
    <p class="lede">Canonical tier structure from <code>targets.yaml</code> —
      the sole authoritative target file. Current-vs-target dollar comparison
      is intentionally omitted: it needs live prices and reconciled holdings
      this dashboard does not have.</p>
    <div class="table-scroll">
    <table>
      <caption>Tier targets (per-name weight of book).</caption>
      <thead><tr><th scope="col">Tier</th><th scope="col" class="num">Weight</th>
        <th scope="col">Cap</th><th scope="col">Sizing</th>
        <th scope="col" class="num"># names</th><th scope="col">Tickers</th></tr></thead>
      <tbody>{''.join(tier_rows) or '<tr><td colspan="6" class="unavailable">No tiers found.</td></tr>'}</tbody>
    </table>
    </div>
    <p>Crypto sleeve target: <strong>{sleeve}</strong> of book (tracked, not traded by the allocator).</p>"""


def _concentration_block(model: DashboardModel) -> str:
    m = model.margin
    cluster_rows = "".join(
        "<tr>"
        + _cell("Cluster", _esc(c.name), header=True)
        + _cell("Cap", _fmt_pct(c.pct, 1), num=True)
        + _cell("# names", str(len(c.tickers)), num=True)
        + _cell("Tickers", _esc(", ".join(c.tickers)))
        + "</tr>"
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
    ai_sub = (
        ('measured ~' + format(model.ai_platform_measured_pct, '.2f')
         + '% (point-in-time, PHQ-2026-01-derived)')
        if model.ai_platform_measured_pct is not None
        else 'measured figure unavailable — point-in-time, see PHQ-2026-01 evidence'
    )
    return f"""
    <h3>Concentration &amp; risk</h3>
    <p class="lede">Approved limits and margin facts from repository truth
      only. No exposure figure is inferred from Robinhood screenshots or live
      prices; leverage ratio and live cluster proximity are not shown —
      they require a live gross valuation this offline dashboard does not
      compute.</p>
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
        <div class="sub">{ai_sub}</div></div>
    </div>
    <div class="table-scroll">
    <table>
      <caption>Correlated-cluster caps (each ≤ its % of book) from <code>targets.yaml</code>.</caption>
      <thead><tr><th scope="col">Cluster</th><th scope="col" class="num">Cap</th>
        <th scope="col" class="num"># names</th><th scope="col">Tickers</th></tr></thead>
      <tbody>{cluster_rows or '<tr><td colspan="4" class="unavailable">No cluster caps found.</td></tr>'}</tbody>
    </table>
    </div>"""


def _gates_block(model: DashboardModel) -> str:
    gated_rows = "".join(
        "<tr>"
        + _cell("Ticker", _esc(g.ticker), header=True)
        + _cell(
            "Target wt",
            _fmt_pct((g.target_weight or 0) * 100, 2) if g.target_weight is not None else "—",
            num=True,
        )
        + _cell("Status", _esc(g.status))
        + _cell("Next gate / evidence needed", _esc(g.next_gate))
        + "</tr>"
        for g in model.gated_names
    )
    skhy = (
        '<div class="notice warning" role="note">'
        '<span class="n-icon" aria-hidden="true">⚠</span>'
        '<div class="n-body"><div class="n-title">SKHY unresolved</div>'
        '<div class="n-detail">SKHY is a live band holding but is explicitly not '
        'addressed by PHQ-2026-01 and remains an open item (see CLAUDE.md). It is '
        'not silently brought under any transition architecture.</div></div></div>'
        if model.skhy_unresolved
        else '<p class="unavailable">SKHY not present in current holdings.</p>'
    )
    spcx = (
        '<div class="notice info" role="note">'
        '<span class="n-icon" aria-hidden="true">ℹ</span>'
        '<div class="n-body"><div class="n-title">SPCX — HOLD TARGET IN CASH</div>'
        '<div class="n-detail">SPCX is gated: its target capital is held in cash '
        '(no currently approved investable vehicle). This is not a directive to '
        'sell any existing SPCX position. Advisory / governance status only. '
        'Gated cash is never renormalized into other positions.</div></div></div>'
    )
    return f"""
    <h3>Gates &amp; open decisions</h3>
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
    {skhy}"""


def _allocation_disclosure(model: DashboardModel) -> str:
    reasons = "".join(f"<li>{_esc(r)}</li>" for r in model.allocation_unavailable_reasons)
    return f"""
    <details>
      <summary>Why market values &amp; recommendations aren't shown</summary>
      <div class="notice info" role="note">
        <span class="n-icon" aria-hidden="true">ℹ</span>
        <div class="n-body"><div class="n-title">Recommendation unavailable —
          controlling state is incomplete or requires live data</div>
        <div class="n-detail">This read-only presentation layer deliberately
          does not run the allocator or build a second one. It never produces
          executable orders. To get a current, advisory-only recommendation,
          run <code>python allocate.py --review</code> (or <code>--cash X</code>)
          in a networked session after reconciling holdings.</div></div>
      </div>
      <ul>{reasons}</ul>
    </details>"""


def _portfolio(model: DashboardModel) -> str:
    return f"""
    <section id="portfolio" data-view aria-labelledby="portfolio-h">
      <div class="view-head">
        <h2 id="portfolio-h">Portfolio</h2>
        <p class="lede">Governed holdings, targets, concentration limits, and
          gated names — all from repository truth.</p>
      </div>
      <div class="panel">{_positions_table(model)}</div>
      <div class="panel">{_targets_table(model)}</div>
      <div class="panel">{_concentration_block(model)}</div>
      <div class="panel">{_gates_block(model)}{_allocation_disclosure(model)}</div>
    </section>"""


# ── Intelligence ─────────────────────────────────────────────────────────

def _intelligence(model: DashboardModel) -> str:
    intel = model.intelligence
    note = (
        '<div class="notice warning" role="note">'
        '<span class="n-icon" aria-hidden="true">⚠</span>'
        f'<div class="n-body"><div class="n-title">Degraded</div>'
        f'<div class="n-detail">{_esc(intel.note)}</div></div></div>'
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
    invalid = ", ".join(intel.schema_invalid) if intel.schema_invalid else "none"
    return f"""
    <section id="intelligence" data-view aria-labelledby="intelligence-h">
      <div class="view-head">
        <h2 id="intelligence-h">Intelligence</h2>
        <p class="lede">Company / Theme Intelligence coverage and freshness,
          via the repository's own <code>intelligence_report</code> reporting
          API (read-only). No automatic scoring, ranking, or allocator
          coupling — <code>targets.yaml</code> always wins on tier/role.</p>
      </div>
      <div class="panel">
        {note}
        <div class="cards">
          <div class="card stat-lg"><div class="label">Company records</div>
            <div class="value">{intel.company_yaml_count}</div>
            <div class="sub">{intel.company_markdown_count} thesis docs</div></div>
          <div class="card stat-lg"><div class="label">Themes</div>
            <div class="value">{intel.theme_yaml_count}</div>
            <div class="sub">{intel.theme_markdown_count} theme docs</div></div>
          <div class="card stat-lg"><div class="label">Freshness rows</div>
            <div class="value">{intel.freshness_rows}</div>
            <div class="sub">{intel.monitoring_enabled_rows} monitoring-enabled</div></div>
          <div class="card stat-lg"><div class="label">Schema-invalid</div>
            <div class="value">{len(intel.schema_invalid)}</div>
            <div class="sub">{_esc(invalid)}</div></div>
        </div>
        <details>
          <summary>Overdue reviews &amp; role drift</summary>
          <h4>Overdue reviews</h4><ul>{overdue}</ul>
          <h4>Portfolio-role drift (advisory — targets.yaml always wins)</h4><ul>{drift}</ul>
        </details>
      </div>
    </section>"""


# ── Governance ───────────────────────────────────────────────────────────

def _governance(model: DashboardModel) -> str:
    p = model.provenance
    ws_rows = "".join(
        "<tr>"
        + _cell("ID", _esc(w.ws_id), header=True)
        + _cell("Title", _esc(w.title or "—"))
        + _cell("Status", _esc(w.status or "—"))
        + _cell("Priority", _esc(w.priority or "—"))
        + "</tr>"
        for w in model.workstreams
    )
    dec_rows = "".join(
        "<tr>"
        + _cell("ID", _esc(d.decision_id), header=True)
        + _cell("Date", _esc(d.date or "—"))
        + _cell("Status", _esc(d.status or "—"))
        + _cell("Category", _esc(d.category or "—"))
        + "</tr>"
        for d in model.decisions[-25:]
    )
    dirty_detail = ""
    if p.dirty:
        lines = "".join(f"<li><code>{_esc(ln)}</code></li>" for ln in p.dirty_paths)
        dirty_detail = (
            '<div class="notice warning" role="note">'
            '<span class="n-icon" aria-hidden="true">⚠</span>'
            '<div class="n-body"><div class="n-title">'
            "Uncommitted changes at generation</div><div class=\"n-detail\">"
            "This page is NOT authoritative for any committed state.</div>"
            f"<ul>{lines}</ul></div></div>"
        )
    return f"""
    <section id="governance" data-view aria-labelledby="governance-h">
      <div class="view-head">
        <h2 id="governance-h">Governance</h2>
        <p class="lede">Accepted decisions and workstream state — items
          requiring attention, as represented by repository truth.</p>
      </div>
      <div class="panel">
        {dirty_detail or '<p class="unavailable">No uncommitted changes at generation time.</p>'}
        <h3>Workstream register ({len(model.workstreams)})</h3>
        <div class="table-scroll"><table>
          <thead><tr><th scope="col">ID</th><th scope="col">Title</th>
            <th scope="col">Status</th><th scope="col">Priority</th></tr></thead>
          <tbody>{ws_rows or '<tr><td colspan="4" class="unavailable">No workstreams parsed.</td></tr>'}</tbody>
        </table></div>
        <h3>Governance decision index (latest 25 of {len(model.decisions)})</h3>
        <div class="table-scroll"><table>
          <thead><tr><th scope="col">ID</th><th scope="col">Date</th>
            <th scope="col">Status</th><th scope="col">Category</th></tr></thead>
          <tbody>{dec_rows or '<tr><td colspan="4" class="unavailable">No decisions parsed.</td></tr>'}</tbody>
        </table></div>
      </div>
    </section>"""


# ── System / Provenance ──────────────────────────────────────────────────

def _system(model: DashboardModel) -> str:
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
    return f"""
    <section id="system" data-view aria-labelledby="system-h">
      <div class="view-head">
        <h2 id="system-h">System / Provenance</h2>
        <p class="lede">Exactly which repository state produced this page.</p>
      </div>
      <div class="panel">
        <div class="cards">
          <div class="card"><div class="label">Repository</div>
            <div class="value">{_esc(p.repo_name)}</div></div>
          <div class="card"><div class="label">Commit (full)</div>
            <div class="value mono" style="font-size:13px">{_esc(p.commit_display)}</div>
            <div class="sub">{_esc(p.commit_subject or '')}</div></div>
          <div class="card"><div class="label">Committed</div>
            <div class="value">{_esc(p.commit_iso or 'unknown')}</div></div>
          <div class="card"><div class="label">Generated</div>
            <div class="value">{_esc(p.generated_at_iso)}</div>
            <div class="sub">UTC, at build time</div></div>
        </div>
        <h3>Authoritative inputs (with content hashes)</h3>
        <ul class="provenance-list">{input_rows}</ul>
        <details>
          <summary>Historical evidence links (not parsed as current state)</summary>
          <p class="lede">Retained under <code>governance/evidence/PHQ-2026-01/</code>.
            These are point-in-time artifacts; this dashboard links but never
            derives current holdings from them.</p>
          <ul>
            <li><code>governance/evidence/PHQ-2026-01/README.md</code></li>
            <li><code>governance/evidence/PHQ-2026-01/final_due_diligence/</code></li>
            <li><code>governance/evidence/PHQ-2026-01/authority/LIVE_STATE_BOUNDARY.md</code></li>
          </ul>
        </details>
        <p class="lede"><strong>Non-authoritative.</strong> This generated
          HTML file is disposable and reproducible from the state shown
          above; it is never a source of truth for anything, and it writes
          no file back into the repository.</p>
      </div>
    </section>"""


def _nav() -> str:
    current_attr = ' aria-current="page"'
    items = "".join(
        f'<li><a href="#{sid}" data-target="{sid}"{current_attr if i == 0 else ""}>'
        f'<span class="ic" aria-hidden="true">{icon}</span><span>{label}</span></a></li>'
        for i, (sid, label, icon) in enumerate(_NAV_ITEMS)
    )
    return f"""
    <nav class="primary-nav" id="primary-nav" aria-label="Dashboard sections">
      <ul>{items}</ul>
      <div class="nav-foot">Read-only &middot; recommendation-only &middot;
        local-only &middot; no brokerage connection &middot; no order path.</div>
    </nav>"""


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
    dirty_flag = ' <span class="badge warning">dirty worktree</span>' if p.dirty else ""

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
<a class="skip-link" href="#main">Skip to content</a>
<div class="app">
  <header class="topbar" role="banner">
    <div class="brand"><span class="dot" aria-hidden="true"></span><h1>Portfolio-HQ Dashboard</h1></div>
    <span class="meta">commit <code>{_esc(p.commit_short or 'unknown')}</code>
      on <code>{_esc(p.branch or '?')}</code>{dirty_flag}</span>
    <div class="spacer"></div>
    <div class="status-chips">{status_summary}</div>
  </header>
  <div class="readonly-banner" role="note">Read-only &middot; recommendation-only &middot; local-only &middot; no brokerage connection &middot; no order path</div>
  <div class="shell">
    {_nav()}
    <main class="content" id="main">
      <div class="wrap">
        {_overview(model)}
        {_portfolio(model)}
        {_intelligence(model)}
        {_governance(model)}
        {_system(model)}
      </div>
    </main>
  </div>
</div>
<footer class="page-footer">
  Portfolio-HQ repository-native dashboard &middot; derived from commit
  <code>{_esc(p.commit_display)}</code> &middot; generated {_esc(p.generated_at_iso)} &middot;
  This is a presentation layer, not portfolio authority. holdings.yaml,
  targets.yaml, and accepted decisions remain the sole sources of truth.
</footer>
<script>{_JS}</script>
</body>
</html>
"""
