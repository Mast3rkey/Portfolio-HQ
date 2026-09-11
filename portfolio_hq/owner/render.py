"""Owner-facing HTML for the private interface.

Runtime half of the trust boundary: standard library only. This module imports
no investment code, reads no repository file, and performs no calculation of
its own — it renders values that ``export.py`` already produced from canonical
Portfolio-HQ functions, or says plainly that a value is unavailable.

Presentation rules:

* Every dynamic value is HTML-escaped.
* No external CSS, font, script, image or analytics host: the stylesheet is
  inlined from a local asset and there is no ``<script>`` at all, so the
  interface works with JavaScript disabled and phones nothing home.
* An unavailable value renders as an explicit "not available" state with the
  canonical reason and, where one exists, the action that would resolve it.
  Nothing is filled in with a placeholder number.
* The recommendation-only disclosure is part of the page shell, so it appears
  on every page including the sign-in page.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

_ASSETS = Path(__file__).resolve().parent / "assets"

DISCLOSURE = (
    "Recommendation-only. Portfolio-HQ never places, routes or submits an "
    "order and holds no brokerage connection."
)

_NAV = (
    ("/", "Home"),
    ("/portfolio", "Portfolio"),
    ("/research", "Research"),
    ("/charts", "Charts"),
)


def _esc(value: object) -> str:
    return escape("" if value is None else str(value))


def _unavailable(reason: object, action: object = None) -> str:
    body = f'<p class="unavailable-reason">{_esc(reason)}</p>' if reason else ""
    act = f'<p class="unavailable-action">What would fix it: {_esc(action)}</p>' if action else ""
    return f'<div class="unavailable">Not available.{body}{act}</div>'


def _num(value: object, suffix: str = "", digits: int = 2) -> str:
    if value is None:
        return '<span class="muted">not available</span>'
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float)):
        return _esc(f"{value:,.{digits}f}{suffix}")
    return _esc(f"{value}{suffix}")


def _pct(value: object, digits: int = 2) -> str:
    if value is None:
        return '<span class="muted">not available</span>'
    try:
        return _esc(f"{float(value):.{digits}f}%")
    except (TypeError, ValueError):
        return _esc(str(value))


def _summary_html(field: object) -> str:
    """Render a bounded free-text summary field, marking any shortening.

    Accepts the ``{text, truncated, full_length}`` shape the export produces,
    and tolerates a plain string so an older export still renders.
    """
    if not isinstance(field, dict):
        return _esc(field or "—")
    text = field.get("text")
    if not text:
        return '<span class="muted">—</span>'
    body = _esc(text)
    if field.get("truncated"):
        try:
            full_length = int(field.get("full_length") or 0)
        except (TypeError, ValueError):
            full_length = 0
        note = f"(shortened from {full_length:,} characters)"
        body += f' <span class="muted">{_esc(note)}</span>'
    return body


def _chip(text: str, tone: str = "neutral") -> str:
    return f'<span class="chip {_esc(tone)}">{_esc(text)}</span>'


def _card(title: str, body: str, *, tone: str = "") -> str:
    cls = f"card {tone}".strip()
    return (f'<section class="{_esc(cls)}"><h2>{_esc(title)}</h2>'
            f'<div class="card-body">{body}</div></section>')


def _kv_rows(pairs) -> str:
    rows = "".join(
        f'<div class="kv"><dt>{_esc(label)}</dt><dd>{value}</dd></div>'
        for label, value in pairs
    )
    return f'<dl class="kv-list">{rows}</dl>'


# ── shell ────────────────────────────────────────────────────────────────────

def page(title: str, active: str, body: str, *, signed_in: bool = True) -> str:
    css = (_ASSETS / "owner.css").read_text(encoding="utf-8")
    if signed_in:
        current = ' aria-current="page"'
        nav_items = "".join(
            '<li><a href="{href}"{cur}>{label}</a></li>'.format(
                href=_esc(href), label=_esc(label),
                cur=current if href == active else "")
            for href, label in _NAV
        )
        nav = ('<nav class="tabs" aria-label="Sections"><ul>' + nav_items + "</ul>"
               '<a class="signout" href="/logout">Sign out</a></nav>')
    else:
        nav = ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="referrer" content="no-referrer">
<meta name="color-scheme" content="dark light">
<title>{_esc(title)} — Portfolio-HQ</title>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="brand">Portfolio-HQ</div>
  <p class="disclosure">{_esc(DISCLOSURE)}</p>
</header>
{nav}
<main id="main">{body}</main>
<footer class="foot">
  <p>Private owner interface. Read-only view of accepted repository state plus a
  quarantined chart inbox. {_esc(DISCLOSURE)}</p>
</footer>
</body>
</html>
"""


# ── pages ────────────────────────────────────────────────────────────────────

def login_page(*, error: str | None = None, locked: bool = False) -> str:
    msg = ""
    if locked:
        msg = ('<p class="banner blocker">Too many failed attempts. '
               'Sign-in is temporarily locked on this address.</p>')
    elif error:
        msg = f'<p class="banner blocker">{_esc(error)}</p>'
    body = f"""
{msg}
<section class="card">
  <h2>Sign in</h2>
  <div class="card-body">
    <form method="post" action="/login" class="stack">
      <label for="token">Owner access token</label>
      <input id="token" name="token" type="password" autocomplete="current-password"
             inputmode="text" autocapitalize="off" autocorrect="off" spellcheck="false" required>
      <button type="submit">Sign in</button>
    </form>
    <p class="muted">This interface shows private portfolio information. It is
    not public and is not indexed.</p>
  </div>
</section>
"""
    return page("Sign in", "/login", body, signed_in=False)


def _export_missing_body(what: str) -> str:
    return _unavailable(
        f"The presentation export has not been built, so {what} cannot be shown.",
        "run `python -m portfolio_hq.owner export` against an accepted commit and "
        "redeploy or point the service at the resulting file.",
    )


def _attention_block(export: dict) -> str:
    attention = export.get("attention") or {}
    blockers = attention.get("blockers") or []
    warnings = attention.get("warnings") or []
    infos = attention.get("infos") or []
    if not (blockers or warnings or infos):
        return '<p class="ok">Nothing is currently flagged for attention.</p>'
    out = []
    for tone, label, rows in (("blocker", "Blocking", blockers),
                              ("warning", "Needs attention", warnings),
                              ("info", "For information", infos)):
        for row in rows:
            out.append(
                f'<div class="notice {tone}"><p class="n-title">'
                f'<span class="n-tag">{_esc(label)}</span> {_esc(row.get("title"))}</p>'
                f'<p class="n-detail">{_esc(row.get("detail"))}</p></div>'
            )
    return "".join(out)


def _source_block(export: dict) -> str:
    meta = export.get("meta") or {}
    dirty = meta.get("worktree_dirty")
    return _kv_rows([
        ("Source commit", f'<code>{_esc(meta.get("source_commit") or "unknown")}</code>'),
        ("Branch", _esc(meta.get("branch") or "unknown")),
        ("Working tree", _chip("uncommitted changes", "warning") if dirty
         else _chip("clean", "ok")),
        ("Export built", _esc(meta.get("generated_at") or "unknown")),
    ])


def home_page(export: dict | None, inbox: dict) -> str:
    if export is None:
        body = (_card("What needs your attention",
                      _export_missing_body("portfolio status"))
                + _chart_status_card(inbox))
        return page("Home", "/", body)

    rec = export.get("recommendation_state") or {}
    reasons = rec.get("unavailable_reasons") or []
    if rec.get("allocation_available"):
        rec_body = ('<p>An allocation check can be produced from the currently '
                    'accepted inputs.</p>')
    else:
        rec_body = (
            "<p>No allocation recommendation can be produced right now. "
            "Portfolio-HQ withholds dollar recommendations rather than "
            "estimating them.</p>"
            + (("<ul class='reasons'>"
                + "".join(f"<li>{_esc(r)}</li>" for r in reasons)
                + "</ul>") if reasons else "")
        )

    capital = export.get("capital") or {}
    book = capital.get("book") or {}
    book_body = (
        _unavailable(
            book.get("reason") or "Book value cannot be established.",
            "sync current cash and margin, and provide reconciled position "
            "values, before any dollar figure is shown.",
        )
        if not book.get("available")
        else "<p>Book value inputs are currently reconciled.</p>"
    )

    body = (
        _card("What needs your attention", _attention_block(export))
        + _card("What Portfolio-HQ can recommend right now", rec_body)
        + _card("Book value", book_body)
        + _chart_status_card(inbox)
        + _card("Where this information comes from", _source_block(export))
    )
    return page("Home", "/", body)


def _chart_status_card(inbox: dict) -> str:
    body = _kv_rows([
        ("Charts received", _num(inbox.get("total"), digits=0)),
        ("Quarantined, awaiting review", _num(inbox.get("quarantined"), digits=0)),
        ("Duplicates recorded", _num(inbox.get("duplicates"), digits=0)),
        ("Most recent upload", _esc(inbox.get("latest_received_at") or "none yet")),
    ]) + ('<p class="muted">Every uploaded chart is held as unreviewed evidence. '
          'Uploading a chart changes no target, holding, policy or recommendation.</p>'
          '<p><a class="button" href="/charts">Open the chart inbox</a></p>')
    return _card("Chart inbox", body)


def portfolio_page(export: dict | None) -> str:
    if export is None:
        return page("Portfolio", "/portfolio",
                    _card("Portfolio", _export_missing_body("portfolio targets")))

    level1 = export.get("level1") or {}
    if level1.get("available"):
        sleeves = level1.get("sleeves_pct") or {}
        order = [
            ("direct_equity", "Direct equities"),
            ("broad_market_funds", "Broad-market funds"),
            ("gold_defensive", "Gold"),
            ("crypto", "Crypto"),
            ("cash_and_reserve", "Cash and reserve"),
            ("unallocated", "Unallocated"),
        ]
        rows = "".join(
            f'<tr><th scope="row" data-label="Sleeve">{_esc(label)}</th>'
            f'<td data-label="Accepted target" class="num">{_pct(sleeves.get(key))}</td></tr>'
            for key, label in order if key in sleeves
        )
        recon = level1.get("reconciliation") or {}
        l1_body = (
            f'<table class="grid"><caption class="sr-only">Level-1 sleeve targets</caption>'
            f'<thead><tr><th scope="col">Sleeve</th>'
            f'<th scope="col" class="num">Accepted target</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>'
            f'<p class="muted">Reconciled total '
            f'{_esc(recon.get("total_pct", "—"))}% of book. Accepted policy from '
            f'{_esc(", ".join(level1.get("policy_basis") or []) or "targets.yaml")}. '
            f'These are target weights, not current positions.</p>'
        )
    else:
        l1_body = _unavailable(level1.get("reason"))

    body = (
        _card("Level 1 — what the accepted policy holds, by sleeve", l1_body)
        + _card("Level 2 — accepted instruments", _level2_table(export))
        + _card("Cash, margin and protected capital", _capital_card(export))
        + _card("Concentration limits", _concentration_card(export))
    )
    return page("Portfolio", "/portfolio", body)


def _level2_table(export: dict) -> str:
    rows = export.get("level2") or []
    if not rows:
        return _unavailable("No accepted destination instruments were exported.")
    out = []
    for row in rows:
        if row.get("gated"):
            state = _chip("gated — no adds", "warning")
        elif row.get("held"):
            state = _chip("held", "ok")
        else:
            state = _chip("not held", "neutral")
        qty = row.get("held_quantity")
        qty_html = _num(qty, digits=6) if qty is not None else '<span class="muted">—</span>'
        sleeve = row.get("sleeve") or row.get("asset_class") or "—"
        out.append(
            f'<tr><th scope="row" data-label="Instrument">{_esc(row.get("ticker"))}</th>'
            f'<td data-label="Sleeve">{_esc(sleeve)}</td>'
            f'<td data-label="Accepted target" class="num">{_pct(row.get("target_pct"))}</td>'
            f'<td data-label="Held quantity" class="num">{qty_html}</td>'
            f'<td data-label="State">{state}</td></tr>'
        )
    return (
        '<div class="scroll-x"><table class="grid">'
        '<caption class="sr-only">Accepted instruments and their target weights</caption>'
        '<thead><tr><th scope="col">Instrument</th><th scope="col">Sleeve</th>'
        '<th scope="col" class="num">Accepted target</th>'
        '<th scope="col" class="num">Held quantity</th>'
        '<th scope="col">State</th></tr></thead>'
        f'<tbody>{"".join(out)}</tbody></table></div>'
        '<p class="muted">Held quantity is the last synced share or coin count. '
        'It is not a current market value: no live price is used anywhere in '
        'this interface.</p>'
    )


def _capital_card(export: dict) -> str:
    capital = export.get("capital") or {}
    if not capital.get("available"):
        return _unavailable(capital.get("reason"))

    cash = capital.get("cash") or {}
    margin = capital.get("margin_observation") or {}
    protected = capital.get("protected_percentages") or {}

    if cash.get("usable_as_current"):
        cash_value = (f'{_num(cash.get("balance"))} '
                      f'{_chip("current", "ok")}')
    elif cash.get("balance") is not None:
        cash_value = (f'{_num(cash.get("balance"))} '
                      f'{_chip("dated observation, not current", "warning")}')
    else:
        cash_value = _chip("unknown", "blocker")

    pairs = [
        ("Tracked cash", cash_value),
        ("Cash observed on", _esc(cash.get("synced_at") or "—")),
    ]
    if cash.get("reason"):
        pairs.append(("Cash note", _esc(cash.get("reason"))))
    pairs += [
        ("Margin debt", _num(margin.get("debt"))),
        ("Margin buffer", _pct(margin.get("buffer_pct"))),
        ("Margin observed on", _esc(margin.get("synced_at") or "—")),
        ("Buffer floor", _pct(margin.get("buffer_floor_pct"))),
        ("Leverage cap", _num(margin.get("leverage_cap"), digits=2)),
    ]
    if margin.get("below_buffer_floor"):
        pairs.append(("Buffer status", _chip("below the floor — de-lever", "blocker")))
    if margin.get("reason"):
        pairs.append(("Margin note", _esc(margin.get("reason"))))

    gated_names = protected.get("gated_names") or []
    gated_label = ("Gated targets held as cash"
                   + (f" ({len(gated_names)} name(s))" if gated_names else ""))
    protected_pairs = [
        ("Cash target", _pct(protected.get("cash_pct"))),
        ("Reserve target", _pct(protected.get("reserve_pct"))),
        ("Unallocated remainder", _pct(protected.get("unreconciled_pct"))),
        ("Protected floor (static)", _pct(protected.get("static_protected_pct"))),
        (gated_label, _pct(protected.get("gated_target_pct"))),
    ]
    if protected.get("gated_target_pct_reason"):
        protected_pairs.append(
            ("Gated share note", _esc(protected["gated_target_pct_reason"])))
    if gated_names:
        protected_pairs.append(("Gated names", _esc(", ".join(gated_names))))
    protected_rows = _kv_rows(protected_pairs)

    effective = export.get("holdings_effective") or {}
    return (
        _kv_rows(pairs)
        + "<h3>Protected capital, as a share of book</h3>"
        + protected_rows
        + f'<p class="muted">{_esc(protected.get("note") or "")}</p>'
        + f'<p class="muted">Position freshness: '
          f'{_esc(effective.get("date") or "unknown")} — '
          f'{_esc(effective.get("source") or "source not stated")}.</p>'
    )


def _concentration_card(export: dict) -> str:
    conc = export.get("concentration") or {}
    clusters = conc.get("clusters") or []
    cluster_rows = "".join(
        f'<tr><th scope="row" data-label="Cluster">{_esc(c.get("name"))}</th>'
        f'<td data-label="Cap" class="num">{_pct(c.get("cap_pct"))}</td>'
        f'<td data-label="Members">{_esc(", ".join(c.get("tickers") or []) or "none")}</td></tr>'
        for c in clusters
    )
    table = (
        '<div class="scroll-x"><table class="grid">'
        '<caption class="sr-only">Correlated-cluster caps</caption>'
        '<thead><tr><th scope="col">Cluster</th><th scope="col" class="num">Cap</th>'
        '<th scope="col">Members</th></tr></thead>'
        f'<tbody>{cluster_rows}</tbody></table></div>'
    ) if cluster_rows else '<p class="muted">No cluster caps were exported.</p>'
    return table + _kv_rows([
        ("Single-issuer no-add ceiling", _pct(conc.get("single_issuer_ceiling_pct"))),
        ("AI-platform no-add ceiling", _pct(conc.get("ai_platform_ceiling_pct"))),
        ("AI-platform measured at signing", _pct(conc.get("ai_platform_measured_pct"))),
        ("Crypto sleeve target", _pct(conc.get("crypto_sleeve_pct"))),
    ])


def research_page(export: dict | None) -> str:
    if export is None:
        return page("Research", "/research",
                    _card("Research", _export_missing_body("research status")))

    intel = export.get("intelligence") or {}
    if intel.get("available"):
        overdue = intel.get("overdue_reviews") or []
        invalid = intel.get("schema_invalid") or []
        drift = intel.get("role_drift") or []
        blocks = _kv_rows([
            ("Company records", _num(intel.get("company_records"), digits=0)),
            ("Company notes", _num(intel.get("company_notes"), digits=0)),
            ("Theme records", _num(intel.get("theme_records"), digits=0)),
            ("Companies scanned", _num(intel.get("companies_scanned"), digits=0)),
            ("Freshness rows", _num(intel.get("freshness_rows"), digits=0)),
            ("Monitoring enabled", _num(intel.get("monitoring_enabled_rows"), digits=0)),
        ])
        issues = []
        if overdue:
            issues.append(
                "<h3>Reviews past due</h3><ul>"
                + "".join(f'<li><strong>{_esc(o.get("ticker"))}</strong> — '
                          f'{_esc(o.get("detail"))}</li>' for o in overdue)
                + "</ul>")
        if invalid:
            issues.append("<h3>Records failing schema validation</h3><p>"
                          + _esc(", ".join(invalid)) + "</p>")
        if drift:
            issues.append(
                "<h3>Role drift against accepted targets</h3><ul>"
                + "".join(f'<li><strong>{_esc(d.get("ticker"))}</strong> — '
                          f'{_esc(d.get("detail"))}</li>' for d in drift)
                + "</ul>")
        if not issues:
            issues.append('<p class="ok">No overdue reviews, invalid records or '
                          'role drift were reported.</p>')
        intel_body = blocks + "".join(issues)
    else:
        intel_body = _unavailable(intel.get("note"))

    decisions = export.get("decisions_index") or []
    # The canonical catalog is in filing order (oldest first). The owner cares
    # about what was decided lately, so sort newest-first for display before
    # truncating -- otherwise "the most recent N" would show the oldest N.
    # This is presentation ordering of already-canonical rows, not a second
    # calculation: no field is derived, combined or altered.
    recent = sorted(decisions, key=lambda d: str(d.get("date") or ""), reverse=True)
    shown = recent[:60]
    dec_rows = "".join(
        f'<tr><th scope="row" data-label="Decision">{_esc(d.get("decision_id"))}</th>'
        f'<td data-label="Date">{_esc(d.get("date") or "—")}</td>'
        f'<td data-label="Status">{_esc(d.get("status") or "—")}</td>'
        f'<td data-label="Category">{_esc(d.get("category") or "—")}</td></tr>'
        for d in shown
    )
    dec_body = (
        '<div class="scroll-x"><table class="grid">'
        '<caption class="sr-only">Accepted governance decisions</caption>'
        '<thead><tr><th scope="col">Decision</th><th scope="col">Date</th>'
        '<th scope="col">Status</th><th scope="col">Category</th></tr></thead>'
        f'<tbody>{dec_rows}</tbody></table></div>'
        f'<p class="muted">Showing the {len(shown)} most recently dated of '
        f'{len(decisions)} accepted decisions, newest first. Full decision text '
        f'stays in the repository and in the local Decision Explorer.</p>'
    ) if dec_rows else '<p class="muted">No decisions were exported.</p>'

    workstreams = export.get("workstreams") or []
    ws_rows = "".join(
        f'<tr><th scope="row" data-label="Workstream">{_esc(w.get("id"))}</th>'
        f'<td data-label="Title">{_esc(w.get("title") or "—")}</td>'
        f'<td data-label="Status">{_esc(w.get("status") or "—")}</td>'
        f'<td data-label="Next action">{_summary_html(w.get("next_action"))}</td></tr>'
        for w in workstreams
    )
    shortened = sum(1 for w in workstreams
                    if isinstance(w.get("next_action"), dict)
                    and w["next_action"].get("truncated"))
    source_file = next((w.get("source_file") for w in workstreams
                        if w.get("source_file")), None)
    ws_body = (
        '<div class="scroll-x"><table class="grid">'
        '<caption class="sr-only">Workstreams</caption>'
        '<thead><tr><th scope="col">Workstream</th><th scope="col">Title</th>'
        '<th scope="col">Status</th><th scope="col">Next action</th></tr></thead>'
        f'<tbody>{ws_rows}</tbody></table></div>'
        + (f'<p class="muted">{shortened} next-action note(s) were shortened for '
           f'this summary. The complete text is in '
           f'<code>{_esc(source_file or "operations/WORKSTREAMS.yaml")}</code>.</p>'
           if shortened else "")
    ) if ws_rows else '<p class="muted">No workstreams were exported.</p>'

    body = (
        _card("Research coverage and freshness", intel_body)
        + _card("What is still in progress", ws_body)
        + _card("Accepted decisions", dec_body)
    )
    return page("Research", "/research", body)


_REJECTION_HELP = {
    "empty_payload": "The file had no content. Pick the image again.",
    "payload_too_large": "The image is too large. Export it at a smaller size.",
    "unsupported_media_type": "PNG is the only accepted format. Convert the "
                              "chart to PNG and upload again.",
    "corrupt_or_unreadable_image": "The file looks damaged or incomplete. "
                                   "Re-capture the chart and upload again.",
    "invalid_ticker": "Pick an instrument from the list.",
    "invalid_timeframe": "Pick a timeframe from the list.",
}


def charts_page(export: dict | None, records: list[dict], *,
                flash: dict | None = None) -> str:
    request = (export or {}).get("chart_request") or {}
    tickers = request.get("eligible_tickers") or []
    timeframes = request.get("accepted_timeframes") or []

    banner = ""
    if flash:
        if flash.get("kind") == "accepted":
            banner = (
                f'<p class="banner ok"><strong>Received.</strong> '
                f'{_esc(flash.get("message"))}</p>'
            )
        elif flash.get("kind") == "duplicate":
            banner = (
                f'<p class="banner warning"><strong>Already received.</strong> '
                f'{_esc(flash.get("message"))}</p>'
            )
        else:
            help_text = _REJECTION_HELP.get(str(flash.get("reason")), "")
            banner = (
                f'<p class="banner blocker"><strong>Not accepted.</strong> '
                f'{_esc(flash.get("message"))} {_esc(help_text)}</p>'
            )

    if tickers:
        options = "".join(
            f'<option value="{_esc(t)}">{_esc(t)}</option>' for t in tickers
        )
        ticker_field = (
            '<label for="ticker">Instrument (optional)</label>'
            f'<select id="ticker" name="ticker"><option value="">Not specified</option>'
            f'{options}</select>'
        )
    else:
        ticker_field = ('<p class="muted">The accepted instrument list is not '
                        'available, so a chart cannot be tagged with a ticker '
                        'right now. You can still upload it.</p>')

    if timeframes:
        tf_options = "".join(
            f'<option value="{_esc(t)}">{_esc(t)}</option>' for t in timeframes
        )
        tf_field = (
            '<label for="timeframe">Timeframe (optional)</label>'
            f'<select id="timeframe" name="timeframe">'
            f'<option value="">Not specified</option>{tf_options}</select>'
        )
    else:
        tf_field = ""

    upload = f"""
<form method="post" action="/charts/upload" enctype="multipart/form-data" class="stack">
  <label for="chart">Chart image (PNG)</label>
  <input id="chart" name="chart" type="file" accept="image/png" required>
  <p class="muted">PNG only. A PNG is refused unless its own bytes are a complete, undamaged PNG, whatever the file is named. Convert a JPEG chart to PNG on your own machine first; this service never converts anything for you.</p>
  {ticker_field}
  {tf_field}
  <button type="submit">Upload chart</button>
</form>
<p class="muted">{_esc(request.get("instructions") or "")}</p>
<p class="muted">{_esc(request.get("note") or "")}</p>
"""

    body = (
        banner
        + _card("Send a chart", upload)
        + _card("What happens to an uploaded chart", """
<ol class="steps">
  <li><strong>Received.</strong> The image is stored privately, exactly as sent,
      with its hash, size, dimensions and receipt time.</li>
  <li><strong>Quarantined.</strong> It is held as unreviewed, untrusted evidence.
      Nothing reads it automatically.</li>
  <li><strong>Reviewed later.</strong> Interpretation is a separate, reviewed step
      that has not been built yet.</li>
</ol>
<p class="muted">Uploading a chart does not change any holding, target, sleeve weight, policy, cap, margin setting or recommendation, and never creates an order.</p>""")
        + _card("Charts received", _records_table(records))
    )
    return page("Charts", "/charts", body)


def _records_table(records: list[dict]) -> str:
    if not records:
        return '<p class="muted">No charts have been uploaded yet.</p>'
    rows = []
    for record in records:
        state = record.get("state")
        if state == "duplicate":
            state_chip = _chip("duplicate of an earlier upload", "warning")
        else:
            state_chip = _chip("quarantined — awaiting review", "ok")
        dims = record.get("image_width"), record.get("image_height")
        dim_text = (f"{dims[0]}x{dims[1]}"
                    if all(isinstance(d, int) for d in dims) else "—")
        digest = str(record.get("content_sha256") or "")
        flags = []
        if record.get("display_filename_sanitized"):
            flags.append("filename cleaned")
        if record.get("declared_extension_matches_content") is False:
            flags.append("extension did not match content")
        rows.append(
            f'<tr><th scope="row" data-label="Received">'
            f'{_esc(record.get("received_at"))}</th>'
            f'<td data-label="State">{state_chip}</td>'
            f'<td data-label="Instrument">{_esc(record.get("declared_ticker") or "—")}</td>'
            f'<td data-label="Timeframe">{_esc(record.get("declared_timeframe") or "—")}</td>'
            f'<td data-label="File">{_esc(record.get("display_filename"))}</td>'
            f'<td data-label="Type">{_esc(record.get("media_type"))} · {_esc(dim_text)}</td>'
            f'<td data-label="Content hash"><code>{_esc(digest[:12])}</code></td>'
            f'<td data-label="Notes">{_esc("; ".join(flags) or "—")}</td></tr>'
        )
    return (
        '<div class="scroll-x"><table class="grid">'
        '<caption class="sr-only">Charts received into the inbox</caption>'
        '<thead><tr><th scope="col">Received</th><th scope="col">State</th>'
        '<th scope="col">Instrument</th><th scope="col">Timeframe</th>'
        '<th scope="col">File</th><th scope="col">Type</th>'
        '<th scope="col">Content hash</th><th scope="col">Notes</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def error_page(status: int, message: str, *, signed_in: bool = False) -> str:
    body = _card(f"{status}", f'<p>{_esc(message)}</p>'
                              '<p><a class="button" href="/">Back to Home</a></p>')
    return page(str(status), "/", body, signed_in=signed_in)
