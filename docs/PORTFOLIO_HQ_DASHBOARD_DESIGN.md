# Portfolio-HQ dashboard — design note & source-of-truth map

**Read-only presentation workstream.** This note describes a repository-native
dashboard that renders the repository's own committed state. It changes no
investment policy, so the design note and its implementation land in the same
PR (the whole surface is read-only). It authorizes and performs **no** change to
`holdings.yaml`, `targets.yaml`, accepted decisions, `operations/WORKSTREAMS.yaml`,
allocator behavior, margin behavior, or any order path.

Distinct from **WS-0002 Phase Two** (OPS-0005), which is a *stdout-only* status
layer explicitly prohibited from producing any generated report file. This
dashboard is the HTML/localhost presentation surface — a different deliverable,
not owned by any open workstream or PR at the time it was built. It is delivered
as a **draft** PR for independent review before any merge.

---

## 1. Authority & boundary

| Property | Guarantee |
| --- | --- |
| Recommendation-only | Displays only advisory language that already originates from repository logic; produces no orders. |
| Read-only | Never writes an authoritative file. `build` writes exactly one gitignored HTML artifact; `serve` writes nothing. |
| Local-only | Server binds `127.0.0.1` by default (never `0.0.0.0`). No CDN/analytics/external JS/CSS/fonts. Works offline and as a `file://`. |
| No brokerage | No Alpaca call, no Robinhood connection, no credential field, no network at all. |
| No mutation | No `<form>`, `<input>`, Buy/Sell/Submit control, or POST/PUT/DELETE endpoint (the server rejects them 405). |
| Intelligence ≠ policy | Intelligence is shown as advisory; `targets.yaml` always wins on tier/role. |
| No silent renormalization | Gated cash is shown as gated; never redistributed into other positions. |

## 2. One canonical generator, one master interface

There is exactly one generator (`portfolio_hq/dashboard`) and one supported
interface (the generated HTML page / the localhost view of the same render).
The build is **not** hand-maintained: the committed artifacts are the generator
code, template logic, and stylesheet — never a checked-in HTML file. Generated
HTML lives only under the gitignored `reports/generated/` and is disposable.

Retained historical HTML (e.g. under `governance/evidence/PHQ-2026-01/`) is
**archive-only**: it is *linked* from a single secondary "Historical evidence"
disclosure inside Governance & Provenance, and is **never** parsed, embedded,
scraped, or used as a current data source. Point-in-time figures the dashboard
does surface (the PHQ-2026-01 concentration ceilings and measured AI/platform
estimate) are read from the accepted decision's **structured JSON** evidence
(`lookthrough_summary`), not from any HTML, and are labelled point-in-time.

## 3. Static build & local serve

```
python -m portfolio_hq.dashboard build --output reports/generated/portfolio_hq_dashboard.html
open reports/generated/portfolio_hq_dashboard.html          # macOS
python -m portfolio_hq.dashboard serve --host 127.0.0.1 --port 8000
```

`serve` rebuilds from current repository state on each request (a browser
refresh reflects the latest state) and writes nothing. The build is
deterministic except for the single disclosed generation-timestamp field.

## 4. Module organization

| File | Role |
| --- | --- |
| `portfolio_hq/dashboard/model.py` | View-model: loads repository files, reuses production functions, computes notices. No I/O writes. |
| `portfolio_hq/dashboard/provenance.py` | Git commit/branch/dirty status + input-file content hashes. |
| `portfolio_hq/dashboard/render.py` | Pure model → HTML. Escapes all dynamic text; inlines CSS; one optional progressive-enhancement script. |
| `portfolio_hq/dashboard/server.py` | Loopback-only HTTP server; GET-only; rejects mutating methods. |
| `portfolio_hq/dashboard/cli.py` / `__main__.py` | `build` / `serve` commands. |
| `portfolio_hq/dashboard/assets/dashboard.css` | Committed stylesheet source (inlined at build). |

Calculations are **reused, not duplicated**: roster construction
(`allocate.build_roster`), margin-sync age (`allocate._margin_buffer_age_days`),
and Intelligence coverage/staleness/role-drift (`intelligence_report.*`). The
dashboard builds **no** second allocator and duplicates no policy/allocation
logic in the template or JavaScript. It deliberately does **not** compute an
allocation recommendation (that needs live market data + reconciled holdings);
it surfaces a labelled "unavailable" explanation instead.

## 5. Source-of-truth map (every major section → one authoritative source)

| Section | Displayed field(s) | Authoritative source | Notes |
| --- | --- | --- | --- |
| Overview | source commit, branch, dirty status, generated-at | local `git` metadata | generation time is the only non-deterministic field |
| Overview | holdings effective date | `holdings.yaml` `margin.synced_at` | disclosed as the sync anchor |
| Overview | controlling policy | `governance/decisions.yaml` | decision index |
| Portfolio | positions, quantities, tier | `holdings.yaml` (`shares`/`crypto_shares`/`holdings`) + `targets.yaml` (tier via `build_roster`) | live $ values intentionally not computed |
| Targets | tier weights, caps, sizing, crypto sleeve | `targets.yaml` | sole authoritative target file |
| Allocation Check | (none — "unavailable") | n/a | requires live Alpaca + reconciled holdings; never produced here |
| Concentration & Risk | margin debt/buffer/floor/leverage cap | `holdings.yaml` `margin`, `targets.yaml` `margin` | leverage ratio needs live gross → omitted |
| Concentration & Risk | cluster caps | `targets.yaml` `caps.clusters` | |
| Concentration & Risk | 8% / 40% ceilings, measured ≈40.03% | PHQ-2026-01 **structured JSON** `lookthrough_summary` | point-in-time; policy constants as fallback |
| Gates & Decisions | gated names, status, next gate | PHQ-2026-01 gated-disposition **CSV** | governance policy; never merged into holdings |
| Gates & Decisions | SPCX hold-in-cash, SKHY unresolved | accepted decision text + `holdings.yaml` presence | advisory/governance status only |
| Research & Freshness | coverage, staleness, role drift, freshness rows | `intelligence_report.*` API + `intelligence/freshness_registry.yaml` | read-only reporting API |
| Governance & Provenance | decisions, workstreams, input hashes, commit | `governance/decisions.yaml`, `operations/WORKSTREAMS.yaml`, git | historical HTML linked, not parsed |

No displayed current-state field depends on any historical HTML file. Data that
exists only in historical HTML is classified historical and non-controlling
(linked in the Evidence Archive disclosure); the small number of point-in-time
figures the dashboard does show are migrated from the corresponding **structured**
evidence (JSON/CSV), with provenance (the file is content-hashed in the panel).

## 6. Stale / incomplete state behavior

The dashboard renders even when inputs are missing, malformed, stale, or
incomplete, and discloses it prominently rather than hiding it:

- stale/unverifiable holdings sync → warning banner;
- missing/unparseable file → warning banner, section degrades gracefully;
- dirty worktree or unavailable git metadata → warning + "not authoritative";
- buffer below floor → blocker banner (forced de-lever), from repository truth only;
- PHQ-2026-02 absent → info banner;
- allocation always labelled "unavailable" with reasons;
- PHQ-2026-01 approved-but-not-implemented → info banner.

## 7. Testing strategy

`test_portfolio_hq_dashboard.py` covers source loading, missing/malformed YAML,
stale-holdings and missing-PHQ-2026-02 warnings, dirty-worktree provenance,
exact-commit rendering, gated-cash / SPCX / SKHY / no-renormalization framing,
HTML escaping, offline (no external asset) rendering, no-order/mutation controls,
deterministic rendering modulo timestamp, structural HTML assertions, the CLI
build/serve surface, localhost-only server binding, and an explicit test proving
retained historical HTML is never read as operational input.

## 8. Accessibility & responsive layout

Semantic landmarks (`header`/`main`/`section`/`nav`/`footer`), a skip link,
`th[scope]` table headers with captions, keyboard-operable sortable headers with
visible focus states, sufficient contrast in light and dark (system-preference)
themes, and a responsive card/table layout for desktop and tablet. No large UI
framework is added for theming.
