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

---

## 9. Dashboard 2.0 — approved first-pass visual redesign (`OPS-0012`)

**Status: authorized design direction for one future, separate,
bounded implementation PR** — not yet implemented, not yet begun. This
section records what `governance/decisions/OPS-0012-dashboard-2-modern-responsive-experience-authorization.md`
authorizes; §§1–8 above describe the merged Dashboard 1.0 architecture and
remain unedited and fully in force — the canonical generator, module
organization, and source-of-truth map are the foundation this redesign
builds on, not something it replaces.

### 9.1 Design direction

A restrained modern financial-application aesthetic, inspired by the
qualities of premium contemporary software without copying any specific
existing product:

- dark charcoal background (not pure black) as the default theme;
- layered surfaces with restrained translucency where supported, degrading
  gracefully where not;
- clean cards — consistent radii, borders, shadows, spacing;
- large, legible summary values; clear section hierarchy;
- system-safe font stacks only — no hosted or bundled font files;
- subtle hover/focus/disclosure/page-entry transitions; calm, not novel —
  no flashing, excessive parallax, gamification, or decoration that
  reduces comprehension;
- a responsive sidebar or compact mobile navigation pattern;
- smooth table/card interactions across desktop, tablet, and phone;
- accessible contrast and visible keyboard focus in both themes.

Exact palette, spacing scale, radii, shadow depth, and animation timing are
left to implementation-time designer discretion within these qualities and
within §1's unchanged authority boundary — `OPS-0012` authorizes a
direction, not fixed design tokens.

### 9.2 Information architecture

Five areas, built only from information the existing `model.py` view-model
and §5's source-of-truth map already expose:

1. **Overview** — repository/portfolio status, high-priority notices,
   portfolio snapshot, governance/workstream summary, Intelligence/
   freshness summary, provenance/generated-at information.
2. **Portfolio** — governed assets and targets: readable desktop table,
   mobile-friendly stacked presentation, existing sorting, clear empty/
   unavailable/warning states.
3. **Intelligence** — current coverage/freshness only; no new research
   conclusions; no automatic scoring or ranking.
4. **Governance** — accepted decisions, workstream state, items requiring
   attention where already represented by repository truth.
5. **System / Provenance** — source files, hashes, branch/commit/dirty
   state, warnings and limitations, and an explicit statement that
   generated HTML is non-authoritative.

No new investment calculation may be added to fill a design card; an
unsupported metric is omitted or labeled unavailable, per §6's existing
disclosure discipline.

### 9.3 Implementation scope (one future PR, within this same package)

Restructured generated HTML; redesigned `assets/dashboard.css`; minimal
local JavaScript for navigation/presentation only (no new data-fetching or
calculation); responsive navigation; semantic sections/client-side views
within the one generated document; redesigned cards/badges/notices/tables/
disclosure panels/provenance sections for the five areas above; accessible
sorting/navigation; subtle animation with `prefers-reduced-motion` support;
responsive desktop/tablet/mobile layouts; dark-mode polish; static-friendly
empty/error/loading states; CSS custom properties for visual consistency;
documentation updates (this file and `docs/PORTFOLIO_HQ_DASHBOARD.md`); and
focused accessibility/rendering tests additive to the existing 52. All
`OPS-0011` mandatory boundaries and prohibitions (§1 above) remain fully
binding, unweakened — no order path, no brokerage call, no repository
mutation, no second allocator, no duplicated governed calculation, no
external asset/CDN/font/script, loopback-only optional server.

### 9.4 Performance and accessibility requirements

**Performance:** one static file, no network dependency; responsive with
the full current repository dataset; no large animation framework; no
unnecessary JavaScript; no layout shifts; fully usable with JavaScript
disabled; reasonably sized generated artifact; fast local build/test.

**Accessibility:** semantic landmarks and correct heading hierarchy;
keyboard-accessible navigation/controls with visible focus; accurate
`aria-current`/`aria-sort`; sufficient contrast with no color-only status
communication; `prefers-reduced-motion` support; usable touch targets;
responsive text with no horizontal page scroll; tables that stay
comprehensible on narrow screens.

### 9.5 Visual acceptance standard

The first Dashboard 2.0 pass succeeds when: a first-time user understands
the major sections without instructions; primary navigation is obvious;
the most important notices and repository status are immediately visible;
desktop and mobile layouts both feel intentionally designed; visual
hierarchy is materially improved over the Dashboard 1.0 foundation;
interaction feels smooth but restrained; no placeholder metric appears as
factual portfolio information; all provenance/safety disclosures remain
accessible; and the principal can run the dashboard locally and give
concrete visual feedback for a later, bounded correction pass.

### 9.6 Lifecycle

`OPS-0012`'s own governance PR requires independent exact-head review,
explicit principal acceptance, merge, and post-merge verification before
the one future implementation PR may open. That implementation PR requires
everything `OPS-0011` §8 already requires (independent review, bounded
correction, scope/dependency-direction verification, dedicated tests,
exact-head CI, principal acceptance, post-merge verification) **plus**
rendered desktop/mobile preview artifacts and explicit principal *visual*
acceptance — new steps specific to a visual redesign. Later visual
corrections proceed only as bounded delta passes, never as a silent second
full redesign under the same authorization.

### 9.7 First implementation pass — as-built record

**Status: implementation PR opened, not yet independently reviewed, not yet
principal-accepted, not yet merged** — this subsection records what the
candidate implementation actually contains, not a new authorization; §§9.1–9.6
above remain the controlling design direction.

- **Same single generator, same package.** `render.py` still consumes only
  the existing `DashboardModel` (`model.py` unchanged); no new investment
  calculation, portfolio fact, or Intelligence conclusion was added anywhere.
  The prior 8-section layout (Overview / Portfolio / Targets / Allocation /
  Concentration / Gates / Research / Governance) is reorganized, with no data
  dropped, into the 5 areas §9.2 authorizes — Targets, Allocation,
  Concentration, and Gates content now live inside **Portfolio**; the former
  Research section is **Intelligence**; Governance keeps decisions and
  workstreams; a new **System / Provenance** area holds input hashes, commit
  metadata, and the historical-evidence links that previously sat at the
  bottom of the single-page Governance section.
- **One `<nav>`, two CSS presentations.** The same sidebar markup renders as
  a sticky left rail ≥900px wide and reflows to a horizontal, scrollable tab
  strip below that — no second nav, no JS-only hamburger drawer (so it never
  needs a JS fallback path of its own).
  Section switching (one view visible at a time, `aria-current` tracking,
  URL-hash sync) is a small, optional script; every section is plain, visible
  document flow when JavaScript is disabled, and the CSS gate that hides
  inactive sections only activates once the script adds a `js-views` class to
  `<html>` at runtime — never server-rendered into the page.
- **Tables stay real `<table>` markup at every width.** Below 700px, each
  `<thead>` is visually hidden (not `display: none`, so it stays in the
  accessibility tree) and each row becomes a bordered card; every `<td>`/row
  `<th>` carries a `data-label` attribute that CSS surfaces via
  `content: attr(data-label)` as the visible label in that stacked view.
- **Dark-first tokens**, overridden under `prefers-color-scheme: light`;
  `prefers-reduced-motion: reduce` collapses all transition/animation
  durations to effectively zero. No hosted font, external stylesheet, script,
  image, or network call was added — verified by the existing
  `test_no_external_asset_references` test, unchanged.
- **No `model.py`/`provenance.py`/`server.py`/`cli.py` change** was needed —
  the existing view-model already exposed everything the five-area layout
  needed.

---

## 10. Governance Decision Explorer — approved first drill-down slice (`OPS-0013`)

**Status: authorized capability for one future, separate, bounded
implementation PR** — not yet implemented, not yet begun. This section
records what `governance/decisions/OPS-0013-governance-decision-explorer-authorization.md`
authorizes. §§1–9 above are **unedited** and remain the foundation this
drill-down slice builds on — one canonical generator, one master HTML
interface, the existing module organization and source-of-truth map, and
(once implemented) Dashboard 2.0's visual system. This is a **data/
navigation** capability increment, distinct from Dashboard 2.0's visual
redesign, and is filed and implemented independently of it — it does not
touch, and is not touched by, PR #212.

### 10.1 What it adds

A read-only way to browse this repository's governance decision corpus
(`governance/decisions.yaml` + `governance/decisions/*.md`) from inside the
one generated dashboard document: click a decision ID, open an in-document
detail view with the decision's safely rendered Markdown content, metadata,
related-decision cross-links, authority/lifecycle labeling, and a path back
to the index (breadcrumb, back link, or hash history). No new investment
fact, portfolio calculation, or Intelligence conclusion is added — this is
presentation of governance text that already exists.

### 10.2 Navigation

Hash-based in-document routes (e.g. `#/decision/OPS-0011`,
`#/decision/PI-0035`), pre-rendered decision detail sections, minimal
vanilla JavaScript for view switching and hash sync, native links and
browser back/forward, breadcrumbs, and native `<details>`/`<summary>`
disclosure. **No client-side framework, database, network fetch, second
generated site, multiple HTML pages, external router, or hosted service.**
Still one static/offline HTML artifact — `OPS-0011` §2.2's "one canonical
generator, one master interface" is unchanged.

### 10.3 Model and loader scope

New read-only model support for `governance/decisions.yaml`'s existing
`related_decisions`/`supporting_artifact` fields, `governance/decisions/
*.md` frontmatter and body content, decision source paths, and provenance/
hashes. May add a small dedicated decision loader module, new immutable
view-model structures, safe Markdown-to-HTML rendering (escaping or a
deliberately constrained renderer — no bundled third-party Markdown
library, per `OPS-0011` §5's no-external-dependency boundary), build-time
cross-link indexes, and graceful unavailable/malformed states matching the
existing defensive-loader discipline already in `model.py`. **Supersession
is never inferred from dates or IDs** — where narrowing or supersession is
only expressed in prose, the implementation displays the literal decision
content and related decisions without asserting a structured relationship
the text doesn't state.

### 10.4 Security — untrusted Markdown

Every decision `.md` file is treated as untrusted display input. Required:
HTML escaping or a tightly constrained safe renderer; no raw HTML or script
execution; no event-handler attributes; no `javascript:` links; no
`<iframe>`; no remote image/CSS/script loading; no network requests; no
mutation controls. Every existing `OPS-0011` boundary (read-only,
recommendation-only, loopback-only, GET-only, no brokerage, no orders, no
secrets, no repository mutation, no second allocator, one generator, one
master file) remains fully binding, unweakened.

### 10.5 Progressive disclosure

Four levels: **(1)** decision summary in the existing Governance index
table; **(2)** concise detail — metadata, status, short context, related
decisions, authority warning; **(3)** full safely rendered decision body;
**(4)** original source file and supporting evidence/provenance links.

### 10.6 Authority and lifecycle labeling

Every decision detail view must distinguish accepted authority, proposed/
unmerged material, historical context, narrowed/partially superseded
clauses, supporting evidence, audits/review artifacts, and non-authoritative
generated indexes — and must never imply that `operations/WORKSTREAMS.yaml`
or `governance/decisions.yaml` themselves originate authority, or that a
supporting artifact is policy, or that a narrowed historical decision
remains fully controlling.

### 10.7 Search and accessibility

Local substring filtering by decision ID, title, category, status, related
decision ID, or body/metadata keyword — no semantic search, embeddings,
external indexing, AI-generated summaries, or automatic ranking. Accessible:
keyboard-operable hash navigation, semantic links/headings, one logical
page `<h1>`, correct heading hierarchy in detail views, visible focus,
`aria-current`, meaningful link text, accessible disclosure controls,
responsive mobile layout with no page-level horizontal scroll, reduced-
motion support, and readable long IDs/paths/hashes/titles.

### 10.8 Scope limit and sealed-data boundary

Limited to the Governance Decision Explorer only for this first
implementation — no Company Intelligence, Theme, backtest, workstream-
detail, or evidence-package explorer; each is a named, unauthorized future
phase. `research/margin_target_study/data/untouched_sealed/` must never be
read, indexed, listed, hashed, summarized, or exposed by any dashboard
path — restated here though this slice has no reason to approach it.

### 10.9 Lifecycle

`OPS-0013`'s own governance PR requires independent exact-head review,
explicit principal acceptance, merge, and post-merge verification before
the one future implementation PR may open. That implementation PR requires
everything `OPS-0011` §8 already requires, plus scope verification against
`OPS-0013` §§3–5 and §§9–11 specifically. Filed and reviewed independently
of `OPS-0012`'s Dashboard 2.0 visual-redesign PR (PR #212) — the two may
land in either order.
