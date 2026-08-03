# Portfolio-HQ dashboard — user guide

A polished, **read-only** dashboard that shows the current state of this
repository — holdings, targets, margin, concentration limits, gated names,
governance, and Intelligence freshness — in one page you open locally.

## What it is

- A repository-native view: everything shown is derived from the repository's
  own committed files plus local `git` metadata.
- A single generator that produces one standalone HTML file, or serves the same
  render on `localhost`.
- Provenance-first: it shows the exact source commit, worktree cleanliness, the
  generation time, and a content hash of every input file it read.

## What it is **not**

- Not a trading tool. It places **no orders** and connects to **no brokerage**.
- Not authoritative state. `holdings.yaml`, `targets.yaml`, and accepted
  decisions remain the sole sources of truth.
- Not a second allocator. It does not compute allocation recommendations; for
  those, run `python allocate.py --review` in a networked session.
- Not online. No CDN, analytics, external fonts/JS/CSS, or network calls. It
  works fully offline and as a `file://` page.

## Authoritative inputs

`holdings.yaml`, `targets.yaml`, `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, `intelligence/` (via the read-only
`intelligence_report` API), and the PHQ-2026-01 **structured** evidence
(gated-name CSV + due-diligence JSON) for point-in-time concentration figures.
Historical HTML is linked as archive only — never parsed. See
`docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` §5 for the full source-of-truth map.

## Stale-state behavior

The dashboard renders even when repository state is incomplete and discloses it
loudly: stale holdings sync, missing/malformed files, a dirty worktree, a buffer
below the floor, and PHQ-2026-02 not yet filed all raise visible banners. It
never guesses and never reconstructs current holdings from historical evidence.

## Commands

Update to the latest committed state first:

```
git pull
```

Build a standalone HTML file:

```
python -m portfolio_hq.dashboard build --output reports/generated/portfolio_hq_dashboard.html
```

Open it (macOS):

```
open reports/generated/portfolio_hq_dashboard.html
```

Serve it locally instead:

```
python -m portfolio_hq.dashboard serve --host 127.0.0.1 --port 8000
```

Then visit `http://127.0.0.1:8000` in your browser.

**Stop the server:** press `Ctrl-C` in the terminal running it.

**Refresh after pulling new changes:** for the static file, re-run the `build`
command. For the server, just reload the browser tab — `serve` rebuilds from
current repository state on every request (no restart needed).

## Output path

By default `build` writes `reports/generated/portfolio_hq_dashboard.html`. That
directory is gitignored — the HTML is regenerated on demand and is never a
source of truth. Use `--stdout` to print the HTML without writing a file.

## Why the dashboard may refuse to produce an allocation recommendation

The Allocation Check section will always show "recommendation unavailable" in
this read-only layer, and that is by design. A current recommendation requires:

1. **Live market data** (Alpaca) that this offline dashboard does not fetch;
2. **Reconciled holdings** — after manual Robinhood execution, `holdings.yaml`
   may be stale, and running gating logic against a stale book manufactures
   false signals;
3. **A live, credentialed allocator run** — `targets.yaml` and `gates.yaml`
   already implement PHQ-2026-01's canonical destination architecture and
   actionable-gate list (migrated by PHQ-2026-02); this dashboard displays
   that configuration but deliberately does not run or duplicate
   `allocate.py`'s recommendation logic itself;
4. A **clean worktree** — a page generated from uncommitted changes is not an
   authoritative snapshot.

When any of these is missing, the honest behavior is disclosure or abstention,
not a fabricated number. Run `python allocate.py --review` in a networked
session for a current, advisory-only recommendation.

## Dashboard 2.0 — navigating the page

The page is organized into five areas, reachable from the left sidebar on a
wide screen or the top tab strip on a narrow one: **Overview**, **Portfolio**,
**Intelligence**, **Governance**, and **System / Provenance**. Clicking a
nav item shows that area and hides the rest — this is a JavaScript
enhancement only. With JavaScript disabled, all five areas render as one
long, anchor-linkable page and nothing is hidden; every fact on the page
is still reachable either way.

Tables narrower than about 700px reflow into a stack of label/value cards
instead of a cramped horizontal table — this is CSS only, the underlying
markup is still a real `<table>` for anything that reads it as one.

The page respects `prefers-reduced-motion`: with that OS/browser setting on,
transitions and the section-switch animation are effectively instant.

## Governance Decision Explorer

Inside the **Governance** area, below the existing flat decision-index
table, a searchable catalog lets you open any accepted governance decision's
complete committed text in place — no second page, no network fetch,
everything pre-rendered into this one file.

- **Browse or search**: the catalog list is filterable by decision ID,
  title, date, status, category, related decision ID, or a keyword from the
  decision's own body text. Search is local substring matching only — no
  semantic search, no ranking, no AI summary.
- **Open a decision**: click an ID to see its metadata, related decisions,
  who references it back, its supporting artifact (if any), its source file
  path and content hash, and its full text, safely rendered from the
  committed Markdown.
- **Deep link**: every decision has a stable address,
  `#/decision/<DECISION_ID>` (e.g. `#/decision/OPS-0013`) — paste it,
  bookmark it, or share it; opening the dashboard at that address jumps
  straight to that decision.
- **Two ledgers, resolved honestly**: a related decision that lives in
  `governance/decisions/` opens as a full record. A related decision that
  only exists in the older `decision_log.yaml` historical ledger (the
  `MARGIN-0001`–`MARGIN-0003` and `PI-0001`–`PI-0009` series) shows as a
  compact historical fact card instead, using that ledger's own
  `pending_evidence` / `active` / `accepted` vocabulary verbatim — it is
  never remapped onto the newer `Proposed` / `Accepted` / `Superseded` /
  `Archived` vocabulary, and never given a fake full-record link.
- **No inferred relationships**: `related_decisions` carries no relationship
  type in this repository's own data. The explorer never labels a link
  "implements," "narrows," "supersedes," or similar — only the neutral
  "References this decision," including for the automatically-computed
  reverse-reference list ("decisions that reference this one"). A later
  date or a higher decision number is never treated as supersession.
- **Untrusted-input treatment**: every decision `.md` file is rendered
  through a small, dependency-free Markdown renderer built for this
  purpose — HTML-escaped by default, with only an explicit allow-list of
  structural/inline transforms (headings, lists, tables, bold/italic,
  inline code, fenced code, decision-ID auto-linking) applied on top. No
  raw HTML, script, event handler, `javascript:` link, `<iframe>`, or
  remote resource from decision content is ever live in the page.
- **No JavaScript required**: every decision's full text is present in the
  static HTML and reachable by anchor even with scripting disabled;
  JavaScript only adds single-decision focusing, hash routing, and the
  search box.

This is presentation and navigation only — see
`docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` §10 for the full authority model,
and `governance/decisions/OPS-0013-governance-decision-explorer-authorization.md`
for what was actually authorized.

## Diagnosing common errors

| Symptom | Cause / fix |
| --- | --- |
| "Git metadata unavailable" banner | Not run from inside the git repo, or `git` missing. Run from the repository root. |
| "dirty worktree" banner | Uncommitted changes at build time. Commit/stash, then rebuild for an authoritative page. |
| "Input file could not be read" | A source YAML/CSV is missing or malformed. The section degrades; fix the file and rebuild. |
| Port already in use (serve) | Pick another `--port`, or stop the process using it. |
| Positions show "offline" market value | Expected — live values need a networked allocator run, not this dashboard. |
