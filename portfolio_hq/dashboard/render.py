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

from .model import DashboardModel, DestinationTarget, GatedName, HoldingRow, MarginInfo

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

  // Governance Decision Explorer (OPS-0013): pre-rendered detail sections,
  // hash-routed (#/decision/ID), toggled the same way top-level views are —
  // a CSS class gated on `js-views`, never the `hidden` attribute, so every
  // decision stays visible and anchor-reachable with JS disabled.
  var decisionSections = Array.prototype.slice.call(
    document.querySelectorAll('[data-decision-detail]'));
  var decisionMap = {};
  decisionSections.forEach(function (s) {
    decisionMap[s.getAttribute('data-decision-id')] = s;
  });
  var catalogPanel = document.getElementById('decision-catalog-panel');
  var notFoundBox = document.getElementById('decision-not-found');

  function activate(id, opts) {
    opts = opts || {};
    var found = false;
    sections.forEach(function (s) {
      var on = s.id === id;
      if (on) { found = true; }
      s.classList.toggle('active', on);
    });
    if (!found && sections.length) { sections[0].classList.add('active'); id = sections[0].id; }
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

  function closeDecisionDetail() {
    decisionSections.forEach(function (s) { s.classList.remove('active'); });
    if (catalogPanel) { catalogPanel.classList.remove('detail-open'); }
  }

  function openDecisionDetail(id, opts) {
    opts = opts || {};
    var sec = decisionMap[id];
    if (!sec) { return false; }
    decisionSections.forEach(function (s) { s.classList.toggle('active', s === sec); });
    if (catalogPanel) { catalogPanel.classList.add('detail-open'); }
    if (notFoundBox) { notFoundBox.hidden = true; }
    if (!opts.skipFocus) {
      var heading = sec.querySelector('.decision-detail-title');
      if (heading) { heading.focus(); }
    }
    return true;
  }

  // Returns true iff `hash` is a well-formed decision route (whether or not
  // that ID resolves) — callers use the return value to decide whether to
  // fall through to the pre-existing top-level-hash handling.
  function routeHash(hash, opts) {
    var m = /^#\\/decision\\/([A-Za-z0-9-]+)$/.exec(hash || '');
    if (!m) { return false; }
    if (sections.length) { activate('governance', {skipHash: true, skipScroll: true}); }
    var found = openDecisionDetail(m[1].toUpperCase(), opts);
    if (!found) {
      closeDecisionDetail();
      if (notFoundBox) { notFoundBox.hidden = false; }
    }
    return true;
  }

  if (sections.length && links.length) {
    doc.classList.add('js-views');

    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('data-target');
        if (!id) { return; }
        e.preventDefault();
        closeDecisionDetail();
        if (notFoundBox) { notFoundBox.hidden = true; }
        activate(id);
      });
    });

    var initialHash = window.location.hash || '';
    if (!routeHash(initialHash)) {
      var initial = initialHash.slice(1);
      activate(initial || sections[0].id, {skipHash: true, skipScroll: true});
    }

    window.addEventListener('hashchange', function () {
      var h = window.location.hash || '';
      if (routeHash(h)) { return; }
      closeDecisionDetail();
      if (notFoundBox) { notFoundBox.hidden = true; }
      var target = h.slice(1);
      if (target === 'governance') {
        var heading = document.getElementById('governance-h');
        if (heading) { heading.setAttribute('tabindex', '-1'); heading.focus(); }
      }
      if (target && document.getElementById(target)) {
        activate(target);
      }
    });
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

  // Decision Explorer local substring search — filters the catalog list by
  // pre-rendered metadata (data-search) and, as a second pass, by the
  // already-pre-rendered detail section's own text content. No fetch, no
  // semantic search, no ranking.
  var searchInput = document.getElementById('decision-search');
  var searchCount = document.getElementById('decision-search-count');
  var listItems = Array.prototype.slice.call(
    document.querySelectorAll('[data-decision-list-item]'));
  if (searchInput && listItems.length) {
    searchInput.addEventListener('input', function () {
      var term = searchInput.value.trim().toLowerCase();
      var shown = 0;
      listItems.forEach(function (li) {
        var meta = li.getAttribute('data-search') || '';
        var match = !term || meta.indexOf(term) !== -1;
        if (!match) {
          var link = li.querySelector('a');
          var id = link ? link.getAttribute('href').replace('#/decision/', '') : '';
          var detail = decisionMap[id];
          if (detail && detail.textContent.toLowerCase().indexOf(term) !== -1) {
            match = true;
          }
        }
        li.hidden = !match;
        if (match) { shown += 1; }
      });
      if (searchCount) {
        searchCount.textContent = shown + ' of ' + listItems.length + ' decision(s) shown.';
      }
    });
  }
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
        <div class="value">{len(model.destination_targets)}</div>
        <div class="sub">destination rows (targets.yaml)</div></div>
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
    dest_rows = []
    for d in model.destination_targets:
        dest_rows.append(
            "<tr>"
            + _cell("Ticker", _esc(d.ticker), header=True)
            + _cell("Target weight", _fmt_pct(d.target_pct), num=True, sort=d.target_pct or 0)
            + _cell("Asset class", _esc(d.asset_class or "—"))
            + "</tr>"
        )
    sleeve = _fmt_pct(model.crypto_sleeve_pct)
    headers = _sort_headers((
        ("Ticker", ""), ("Target weight", ' class="num"'), ("Asset class", ""),
    ))
    return f"""
    <h3>Targets</h3>
    <p class="lede">Canonical destination architecture from
      <code>targets.yaml</code> (PHQ-2026-02) — the sole authoritative target
      file. Each row carries its own target weight and asset class directly;
      the prior T1/T2/ETF/band/spec tier structure was retired and no
      grouping is invented in its place. Current-vs-target dollar comparison
      is intentionally omitted: it needs live prices and reconciled holdings
      this dashboard does not have.</p>
    <div class="table-scroll">
    <table data-sortable>
      <caption>Destination targets — per-name target weight of book ({len(model.destination_targets)} row(s)).</caption>
      <thead><tr>{headers}</tr></thead>
      <tbody>{''.join(dest_rows) or '<tr><td colspan="3" class="unavailable">No destination targets found.</td></tr>'}</tbody>
    </table>
    </div>
    <p>Crypto sleeve target: <strong>{sleeve}</strong> of book — sum of the
      BTC/ETH/SOL destination rows above (tracked, not traded by the allocator).</p>"""


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


def _ticker_gate_notice_html(state) -> str:
    """State-derived notice for one ticker's current gate status — replaces
    a prior hardcoded, unconditional "SPCX — HOLD TARGET IN CASH" notice that
    displayed regardless of whether SPCX was still actually gated (it no
    longer is: PHQ-2026-04 retired its gate after a verified manual exit).
    Reusable for any ticker's TickerCurrentState, not SPCX-specific logic."""
    if state.gates_unavailable:
        # gates.yaml itself failed to load — live_gate is structurally None
        # either way, so it cannot be told apart from "confirmed ungated."
        # Never assert a not-gated claim (or stay silent, which would hide
        # an unconfirmable gate the same way) while citing a file that was
        # never actually read — a page-level warning already discloses the
        # load failure; this is the ticker-specific consequence of it.
        return (
            '<div class="notice warning" role="note">'
            '<span class="n-icon" aria-hidden="true">⚠</span>'
            f'<div class="n-body"><div class="n-title">{_esc(state.ticker)} gate '
            'status could not be determined</div>'
            f'<div class="n-detail">gates.yaml was unavailable or unreadable '
            "when this page was generated (see the warnings above) — this "
            f"dashboard cannot confirm whether {_esc(state.ticker)} is "
            "currently gated. This is not a claim that it is, or is not, "
            "gated.</div></div></div>"
        )
    lg = state.live_gate
    if lg is not None:
        # Currently gated per the live gates.yaml — advisory only, never a
        # sell directive.
        next_gate = f" Next gate: {_esc(lg.next_gate)}." if lg.next_gate else ""
        return (
            '<div class="notice info" role="note">'
            '<span class="n-icon" aria-hidden="true">ℹ</span>'
            f'<div class="n-body"><div class="n-title">{_esc(state.ticker)} — '
            f'{_esc(lg.status or "gated")}</div>'
            f'<div class="n-detail">{_esc(state.ticker)} is currently gated per '
            "gates.yaml: its target capital is held in cash (no currently "
            "approved investable vehicle or activation not yet cleared). This "
            "is not a directive to sell any existing position."
            f"{next_gate} Advisory / governance status only. Gated cash is "
            "never renormalized into other positions.</div></div></div>"
        )
    if state.currently_held or state.has_destination_target:
        # Held and/or carries a destination target, but not currently gated
        # — nothing to disclose here.
        return ""
    # Not gated, not held, no destination target: fully resolved/exited per
    # current repository state (gates.yaml / holdings.yaml / targets.yaml).
    return (
        f'<p class="unavailable">{_esc(state.ticker)} is not currently gated, '
        "held, or targeted (see gates.yaml, holdings.yaml, and targets.yaml). "
        "Prior gating policy for this name is historical — see the Gates "
        "evidence table above and CLAUDE.md's Decisions Log.</p>"
    )


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
    spcx = _ticker_gate_notice_html(model.spcx_state)
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
          run <code>python allocate.py --review</code> in a networked session
          after reconciling holdings and syncing the current total cash balance
          with <code>python allocate.py update-cash &lt;total_balance&gt;</code>.</div></div>
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

_STATUS_BADGE_CLASS = {
    "Accepted": "ok",
    "Proposed": "info",
    "Superseded": "warning",
    "Archived": "muted",
}

_TITLE_SOURCE_LABEL = {
    "frontmatter": "title from frontmatter",
    "h1": "title from the decision's first heading",
    "filename": "title mechanically derived from the filename — not authored prose",
    "id": "no title available — decision ID shown",
}


def _decision_status_badge(status: str | None) -> str:
    if not status:
        return '<span class="badge muted">unknown</span>'
    cls = _STATUS_BADGE_CLASS.get(status, "muted")
    return f'<span class="badge {cls}">{_esc(status)}</span>'


def _decision_catalog_item(d) -> str:
    search_bits = " ".join(
        [
            d.decision_id,
            d.title,
            d.date or "",
            d.status or "",
            d.category or "",
            " ".join(r.decision_id for r in d.related),
        ]
    ).lower()
    flags = []
    if d.source_missing:
        flags.append('<span class="badge blocker">source missing</span>')
    if d.duplicate_id:
        flags.append('<span class="badge warning">duplicate ID</span>')
    if d.orphan and not d.source_missing:
        flags.append('<span class="badge warning">not indexed</span>')
    return f"""
    <li data-decision-list-item data-search="{_esc(search_bits)}">
      <a href="#/decision/{_esc(d.decision_id)}" class="decision-link decision-list-link">
        <span class="d-id">{_esc(d.decision_id)}</span>
        <span class="d-title">{_esc(d.title)}</span>
        <span class="d-meta">{_esc(d.date or '—')} &middot; {_decision_status_badge(d.status)}
          &middot; {_esc(d.category or '—')} {''.join(flags)}</span>
      </a>
    </li>"""


def _legacy_fact_card(decision_id: str, legacy) -> str:
    if legacy is None:
        return (
            f'<li class="unresolved-ref"><span class="badge muted">unresolved</span> '
            f"{_esc(decision_id)} — not found in governance/decisions or "
            "decision_log.yaml</li>"
        )

    def _snip(text: str | None) -> str:
        if not text:
            return "—"
        return _esc(text[:500]) + ("…" if len(text) > 500 else "")

    return f"""
    <li class="legacy-ref-card">
      <span class="badge info" title="Historical ledger entry — decision_log.yaml,
        not a governance/decisions/ record">Historical ledger</span>
      <strong>{_esc(decision_id)}</strong>
      <div class="legacy-fields">
        <span>status (decision_log.yaml vocabulary): <code>{_esc(legacy.status or '—')}</code></span>
        <span>category: <code>{_esc(legacy.category or '—')}</code></span>
        <span>date: {_esc(legacy.date or '—')}</span>
      </div>
      <details><summary>decision_log.yaml text</summary>
        <p>{_snip(legacy.decision_text)}</p>
        <p class="lede">{_snip(legacy.rationale)}</p>
      </details>
    </li>"""


def _related_item_html(ref, catalog) -> str:
    if ref.kind == "governance":
        target = next((d for d in catalog.decisions if d.decision_id == ref.decision_id), None)
        title = f" — {_esc(target.title)}" if target else ""
        return (
            f'<li><a href="#/decision/{_esc(ref.decision_id)}" class="decision-link">'
            f"{_esc(ref.decision_id)}</a>{title}</li>"
        )
    if ref.kind == "legacy":
        legacy = next((entry for entry in catalog.legacy if entry.decision_id == ref.decision_id), None)
        return _legacy_fact_card(ref.decision_id, legacy)
    return (
        f'<li class="unresolved-ref"><span class="badge muted">unresolved</span> '
        f"{_esc(ref.decision_id)} — not found in governance/decisions or "
        "decision_log.yaml</li>"
    )


def _reverse_ref_item(ref_id: str, catalog) -> str:
    target = next((d for d in catalog.decisions if d.decision_id == ref_id), None)
    title = f" — {_esc(target.title)}" if target else ""
    return (
        f'<li><a href="#/decision/{_esc(ref_id)}" class="decision-link">{_esc(ref_id)}</a>'
        f"{title} — References this decision.</li>"
    )


def _artifact_html(a) -> str:
    if a is None:
        return '<p class="unavailable">No supporting artifact declared.</p>'
    if a.safe:
        return (
            f'<p><span class="fname">{_esc(a.declared_path)}</span> '
            f'<span class="fhash">sha256:{_esc(a.sha256)} &middot; {a.size_bytes} B</span> '
            '<span class="badge muted">evidence, not policy</span></p>'
        )
    return (
        f'<p><span class="fname">{_esc(a.declared_path)}</span> '
        f'<span class="badge warning">{_esc(a.warning or "unavailable")}</span></p>'
    )


def _decision_issues_html(issues) -> str:
    if not issues:
        return ""
    items = "".join(f"<li>{_esc(i.message)}</li>" for i in issues)
    return (
        '<div class="notice warning" role="note">'
        '<span class="n-icon" aria-hidden="true">⚠</span>'
        '<div class="n-body"><div class="n-title">Load notes</div>'
        f"<ul>{items}</ul></div></div>"
    )


def _decision_detail_html(d, catalog) -> str:
    related_html = "".join(_related_item_html(r, catalog) for r in d.related) or (
        '<li class="unavailable">None declared.</li>'
    )
    reverse_html = "".join(_reverse_ref_item(r, catalog) for r in d.reverse_references) or (
        '<li class="unavailable">No other decision references this one via '
        "related_decisions.</li>"
    )
    mismatch_html = ""
    if d.index_mismatches:
        items = "".join(f"<li>{_esc(m)}</li>" for m in d.index_mismatches)
        mismatch_html = (
            '<div class="notice warning" role="note">'
            '<span class="n-icon" aria-hidden="true">⚠</span>'
            '<div class="n-body"><div class="n-title">Index / frontmatter mismatch '
            "(frontmatter controls)</div>"
            f"<ul>{items}</ul></div></div>"
        )
    orphan_html = ""
    if d.orphan and not d.source_missing:
        orphan_html = (
            '<div class="notice warning" role="note">'
            '<span class="n-icon" aria-hidden="true">⚠</span>'
            '<div class="n-body"><div class="n-title">Not indexed</div>'
            '<div class="n-detail">This decision file exists on disk but has no '
            "governance/decisions.yaml entry.</div></div></div>"
        )
    source_html = (
        f'<li><span class="fname">{_esc(d.source.path)}</span> '
        + (
            f'<span class="fhash">sha256:{_esc(d.source.sha256)} &middot; '
            f"{d.source.size_bytes} B</span>"
            if d.source.exists and d.source.sha256
            else '<span class="badge blocker">source missing</span>'
            if not d.source.exists
            else '<span class="badge warning">hash unavailable</span>'
        )
        + "</li>"
    )
    title_note = _TITLE_SOURCE_LABEL.get(d.title_source, "")
    return f"""
    <section class="decision-detail" id="/decision/{_esc(d.decision_id)}"
      data-decision-detail data-decision-id="{_esc(d.decision_id)}"
      aria-labelledby="decision-{_esc(d.decision_id)}-h">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="#governance">Governance</a><span aria-hidden="true"> / </span>
        <span aria-current="page">{_esc(d.decision_id)}</span>
      </nav>
      <h3 class="decision-detail-title" id="decision-{_esc(d.decision_id)}-h" tabindex="-1">
        {_esc(d.decision_id)} — {_esc(d.title)}
        <span class="badge muted" title="{_esc(title_note)}">derived title</span>
      </h3>
      <div class="cards decision-meta">
        <div class="card"><div class="label">Date</div><div class="value">{_esc(d.date or '—')}</div></div>
        <div class="card"><div class="label">Status</div><div class="value">{_decision_status_badge(d.status)}</div></div>
        <div class="card"><div class="label">Category</div><div class="value">{_esc(d.category or '—')}</div></div>
      </div>
      {_decision_issues_html(d.issues)}
      {mismatch_html}
      {orphan_html}
      <details open>
        <summary>Authority disclosures</summary>
        <ul>
          <li>This <code>.md</code> file is the substantive decision record.</li>
          <li><code>governance/decisions.yaml</code> is a generated index —
            never the primary record.</li>
          <li>A supporting artifact, if any, is evidence, not policy.</li>
          <li><code>related_decisions</code> carries no recorded relationship
            type — a link means "references," never implements / narrows /
            accepts / supersedes / validates.</li>
          <li>Accepted status does not prove that no later decision narrowed
            part of this decision — read related decisions and CLAUDE.md's
            Decisions Log for the fullest picture.</li>
        </ul>
      </details>
      <h4>Related decisions</h4>
      <ul class="related-list">{related_html}</ul>
      <h4>Referenced by</h4>
      <ul class="reverse-list">{reverse_html}</ul>
      <h4>Supporting artifact</h4>
      {_artifact_html(d.supporting_artifact)}
      <h4>Source</h4>
      <ul class="provenance-list">{source_html}</ul>
      <h4>Decision body</h4>
      <div class="decision-body">{d.body_html}</div>
      <p><a href="#governance" class="back-link">&larr; Back to Governance</a></p>
    </section>"""


def _decision_explorer_html(model: DashboardModel) -> str:
    catalog = model.decision_catalog
    catalog_issue_html = ""
    if catalog.issues:
        items = "".join(f"<li>{_esc(i.message)}</li>" for i in catalog.issues)
        catalog_issue_html = (
            '<div class="notice warning" role="note">'
            '<span class="n-icon" aria-hidden="true">⚠</span>'
            '<div class="n-body"><div class="n-title">Decision catalog load notes</div>'
            f"<ul>{items}</ul></div></div>"
        )
    items_html = "".join(_decision_catalog_item(d) for d in catalog.decisions)
    details_html = "".join(_decision_detail_html(d, catalog) for d in catalog.decisions)
    return f"""
    <h3>Decision Explorer</h3>
    <p class="lede">Browse, search, and open the complete committed text of
      every governance decision. Presentation and navigation only — no
      ranking, no relationship type beyond "references," and no
      supersession inferred from a date or an ID.</p>
    {catalog_issue_html}
    <div id="decision-not-found" class="notice warning" hidden role="note">
      <span class="n-icon" aria-hidden="true">⚠</span>
      <div class="n-body"><div class="n-title">Decision not found</div>
        <div class="n-detail">That decision ID was not found in this catalog.
          Showing the governance index instead. <a href="#governance">Return
          to Governance</a>.</div></div>
    </div>
    <div id="decision-catalog-panel">
      <div class="search-field">
        <label for="decision-search">Search decisions</label>
        <input type="search" id="decision-search" autocomplete="off"
          placeholder="Search by ID, title, date, status, category, related ID, or body text&hellip;">
      </div>
      <p id="decision-search-count" class="lede">{len(catalog.decisions)} decision(s).</p>
      <ul class="decision-catalog-list">{items_html or '<li class="unavailable">No decisions found.</li>'}</ul>
    </div>
    <div class="decision-detail-container">{details_html}</div>"""


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
      <div class="panel">{_decision_explorer_html(model)}</div>
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
