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
3. **Implemented policy** — PHQ-2026-01's architecture is approved but not yet
   implemented in `targets.yaml`, so gated-name/reserve handling has no live
   allocator support;
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

## Diagnosing common errors

| Symptom | Cause / fix |
| --- | --- |
| "Git metadata unavailable" banner | Not run from inside the git repo, or `git` missing. Run from the repository root. |
| "dirty worktree" banner | Uncommitted changes at build time. Commit/stash, then rebuild for an authoritative page. |
| "Input file could not be read" | A source YAML/CSV is missing or malformed. The section degrades; fix the file and rebuild. |
| Port already in use (serve) | Pick another `--port`, or stop the process using it. |
| Positions show "offline" market value | Expected — live values need a networked allocator run, not this dashboard. |
