---
decision_id: OPS-0013
date: 2026-08-01
status: Accepted
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0009, OPS-0011, OPS-0012, PHQ-2026-01]
supporting_artifact: null
---

## Context

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ` (remote `origin`).
- **`origin/main` fetched**; this filing's base is
  `6db533338d3958233a23a09c375b91a5df9b00a9` (merge commit of PR #211,
  `OPS-0012`). **Local branch, `origin/main`, and this filing's base are
  identical** — no divergence, confirmed via `git merge-base --is-ancestor`.
  **Working tree confirmed clean** on branch
  `claude/governance-decision-explorer-auth-2tuet0`, created directly from
  `origin/main`.
- **Exactly one open pull request** in the repository: **PR #212**
  ("Dashboard 2.0: modern responsive visual redesign (OPS-0012 first pass)"),
  `draft: true`, `merged: false`, `mergeable_state: clean`, head
  `925d09bb22fdbc2b9e717bab1c224752d2c35d38`, base `main` at
  `6db533338d3958233a23a09c375b91a5df9b00a9`, 6 files changed
  (`portfolio_hq/dashboard/render.py`,
  `portfolio_hq/dashboard/assets/dashboard.css`,
  `test_portfolio_hq_dashboard.py`, `docs/PORTFOLIO_HQ_DASHBOARD.md`,
  `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md`, `operations/WORKSTREAMS.yaml`).
  **PR #212 is the only active Dashboard 2.0 implementation work** — this is
  confirmed, not assumed, by the branch/PR scan below.
- **A live repository-wide scan for any existing Governance Decision
  Explorer or "Repository Explorer" filing or implementation** was performed
  this session: `search_pull_requests` for `"Governance Decision Explorer"
  OR "Repository Explorer"` → zero results; `search_code` for `"Decision
  Explorer"` and separately for `"Repository Explorer" OR "Drill-Down
  Architecture Audit"` → zero results; a full branch listing (108 branches)
  was inspected by name and none references a decision explorer or
  repository explorer; `governance/audits/` and a repository-wide
  case-insensitive grep of `governance/`, `docs/`, and `operations/` for
  "repository explorer" / "drill-down" / "drilldown" → zero hits. **No
  existing Governance Decision Explorer filing or implementation exists
  anywhere in this repository.** This filing does not proceed on the
  strength of a prior audit it cannot itself verify — see the disclosure
  immediately below.
- **No retained "Dashboard Repository Explorer and Drill-Down Architecture
  Audit" artifact exists in this repository.** The task that produced this
  filing describes such an audit as already completed and as the source of
  the "Governance Decision Explorer is the safest first slice" conclusion.
  This session found no `governance/audits/` file, no decision-file
  reference, and no other repository record of that audit. Consistent with
  `OPS-0011`'s own precedent for disclosing unretained, second-hand review
  provenance (its "Independent-review provenance, disclosed precisely"
  section) rather than silently treating an externally asserted finding as
  independently verified: **this decision treats "Governance Decision
  Explorer first" as principal direction for this filing, not as a
  retained, independently reproducible audit conclusion.** Nothing below
  depends on the audit's existence — the capability grant is justified on
  this filing's own merits (§Rationale), and would stand unchanged whether
  or not that audit is ever located or retained.
- **`OPS-0013` confirmed the next unused identifier** — checked live against
  both `governance/decisions/` (55 non-`README` files; highest filed
  `OPS-####` is `OPS-0012`; highest `PI-####` is `PI-0035`) and
  `governance/decisions.yaml` (55 entries, independently re-parsed via
  `yaml.safe_load` and reconciled 1:1 against the directory listing — no
  orphan on either side).
- **The complete current dashboard package read at this exact head**:
  `portfolio_hq/dashboard/{__init__.py, __main__.py, cli.py, model.py,
  provenance.py, render.py, server.py, assets/dashboard.css}`,
  `docs/PORTFOLIO_HQ_DASHBOARD.md`, `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md`,
  and `test_portfolio_hq_dashboard.py`. Confirmed directly from the code:
  `model.py`'s `DecisionRow` dataclass currently carries only
  `decision_id`, `date`, `status`, `category`, `file` — **no
  `related_decisions`, `supporting_artifact`, decision body text, or
  cross-link data is loaded today**; `render.py`'s `_governance()` renders
  only a flat table of the latest 25 decisions with no per-decision detail
  view, no hash-based routing, and no Markdown rendering of any kind
  anywhere in the package. **A Governance Decision Explorer is new
  capability, not a restatement of anything already built.**
- **This filing does not touch PR #212 or any dashboard production code.**
  PR #212's branch (`claude/dashboard-2-visual-redesign-xd0pip`) was not
  fetched, checked out, read for editing, or modified in any way by this
  session.

### Why this capability, and why now

`OPS-0011` authorized a read-only, repository-native dashboard; `OPS-0012`
authorizes a visual redesign of that same dashboard's presentation layer.
Neither authorizes any new *drill-down* capability — the Governance section
`OPS-0012` §3 describes ("accepted decisions, workstream state, and items
requiring attention where already represented by repository truth") is
scoped to what the existing view-model already exposes, which today is a
flat index table. Reading a decision's actual reasoning today requires
opening its `.md` file directly in the repository — the dashboard cannot
show a decision's content, its authority status, or its relationship to
other decisions.

This repository's decision corpus is large (55 filed decisions as of this
session, several exceeding 10,000 words with nested amendments and
supersession clauses) and its governance conventions are precise but easy to
misstate secondhand (e.g. the narrow-supersession convention `OPS-0007`/
`OPS-0009` restate explicitly; the "record never originates authority" rule
`OPS-0001`/`OPS-0011` both apply to `operations/WORKSTREAMS.yaml`). A
read-only, safely-rendered, in-document way to browse and cross-reference
that corpus — without inventing any new authority, without inferring
supersession the text doesn't state, and without leaving the one-file,
read-only, loopback-only dashboard capability `OPS-0011`/`OPS-0012` already
bound — is a natural, narrow first drill-down slice. Following this
repository's own precedent of authorizing a named, bounded module *before*
it is built (`PI-0002`, `PI-0011`, `AUTO-0002`/`AUTO-0003`, `OPS-0005` §3,
`OPS-0011`, `OPS-0012`), this decision is that authorization for exactly
one slice: the Governance Decision Explorer.

## Decision

**OPS-0013 authorizes one later, separate implementation PR to add a
Governance Decision Explorer to the existing single generated dashboard
HTML.** It authorizes a capability and a bounded scope, never a specific
diff. This filing creates no dashboard code, no loader module, no test, and
touches only the governance package named in §13. Implementation does not
begin in this session, and this filing does not touch PR #212 or any
dashboard production code.

### 1. Finding

- `OPS-0011`/`OPS-0012` authorize a read-only dashboard and its visual
  redesign, but neither authorizes any decision drill-down capability —
  confirmed directly from `model.py`/`render.py` at this filing's exact
  head (§Preflight).
- No existing filing, branch, or PR proposes a Governance Decision Explorer
  or any other repository "explorer" capability (§Preflight).
- Following this repository's "authorize the module before it is built"
  precedent, this new capability increment requires its own advance
  authorization, exactly as `OPS-0011` and `OPS-0012` each required for
  their own increments.

### 2. Grant — authorized Governance Decision Explorer capability

Authorizes the future implementation to extend the existing single
generated dashboard HTML so a user can:

1. Browse all governance decisions from the existing decision index.
2. Click a decision ID.
3. Open an in-document decision detail view.
4. Read the decision's committed Markdown content, rendered safely (§5).
5. See, for the selected decision: decision ID; title; date; status;
   category; related decisions; supporting artifact or evidence pointer;
   source file; provenance and hash; authority/lifecycle label (§6); and
   warnings where a decision is narrowed, superseded, historical, or
   non-authoritative in part.
6. Follow clickable related-decision links.
7. Return through breadcrumbs, back links, or browser hash history.
8. Open the original committed source artifact where supported locally.

The explorer must remain inside the one master static/offline HTML
artifact `OPS-0011` §2.2 already established — not a second document, not a
second generator.

### 3. Navigation architecture

**Authorized:**

- hash-based in-document routes, e.g. `#/decision/OPS-0011`,
  `#/decision/PI-0035`;
- pre-rendered decision detail sections (server/build-time rendered into
  the one static document — never fetched);
- minimal vanilla JavaScript for view switching and hash synchronization,
  consistent with `OPS-0011`/`OPS-0012`'s existing "no new data-fetching,
  no new calculation" JavaScript boundary;
- native links and browser back/forward behavior;
- breadcrumb navigation;
- native `<details>`/`<summary>` disclosure where useful;
- client-side substring search and filtering over pre-rendered decision
  metadata (§9).

**Not authorized:**

- a client-side framework;
- a database;
- network fetch of any kind;
- a second generated site;
- multiple HTML pages;
- an external router;
- a hosted service.

### 4. Source and model scope

Authorizes new read-only model support for:

- `governance/decisions.yaml`;
- `governance/decisions/*.md`;
- existing `related_decisions` fields;
- `supporting_artifact` fields;
- decision-file frontmatter;
- decision source paths;
- repository provenance and SHA-256 hashes.

The implementation may add:

- a small dedicated decision loader module;
- new immutable view-model structures;
- safe Markdown-to-HTML rendering, or a deliberately constrained renderer;
- build-time cross-link indexes;
- graceful unavailable/malformed states, matching the existing defensive
  loader discipline already present throughout `model.py` (missing/
  malformed input → recorded warning, dashboard still renders).

**The implementation must not infer supersession merely from dates or
IDs.** Where supersession or narrowing is only expressed in prose (as most
of this repository's own narrow-supersession clauses are — see `OPS-0007`
§2, `OPS-0009` Rationale, both of which state explicitly that a narrowing
decision does not change the superseded decision's `status` field): the
implementation must display the literal decision content, show related
decisions, and avoid claiming a structured supersession relationship
unless repository authority (an explicit `status: Superseded` frontmatter
value, or equivalently explicit sourced text) supports it.

### 5. Security requirements

The future implementation must treat committed Markdown as **untrusted
display input** — authored across dozens of sessions over this
repository's history, never assumed safe merely because it is committed.
Required:

- HTML escaping, or a tightly constrained safe Markdown renderer;
- no raw HTML execution;
- no script execution;
- no event-handler attributes;
- no `javascript:` links;
- no `<iframe>`;
- no remote image loading;
- no external CSS;
- no external scripts;
- no network requests;
- no mutation controls.

**All existing `OPS-0011` boundaries remain binding, unweakened, restated
here as this decision's own operative text** (matching the discipline
`OPS-0012` §5 already applied): read-only; recommendation-only;
loopback-only; GET-only; no brokerage; no orders; no secrets; no repository
mutation; no second allocator; one canonical generator; one master HTML
file.

### 6. Authority and lifecycle labeling

Every decision detail view must clearly distinguish:

- Accepted authority;
- Proposed or unmerged material;
- historical context;
- narrowed or partially superseded clauses;
- supporting evidence;
- audits and review artifacts;
- non-authoritative generated indexes.

**The dashboard must never imply that:**

- `operations/WORKSTREAMS.yaml` creates authority;
- `governance/decisions.yaml` is itself the substantive authority;
- a supporting artifact is policy;
- a historical decision remains fully controlling when later authority
  narrows it.

This restates, for the decision-explorer view specifically, the same
"the register never originates authority" principle `OPS-0001` established
for `operations/WORKSTREAMS.yaml` and `OPS-0011` §9 already applied to the
dashboard generally — extended here explicitly to `governance/
decisions.yaml`, whose own README (read this session) already states it is
"a generated index... never the primary record, the `.md` files are."

### 7. Progressive disclosure

Requires four levels:

- **Level 1** — decision summary in the Governance view (the existing
  index-table row).
- **Level 2** — concise decision detail: metadata; status; short context;
  related decisions; authority warning.
- **Level 3** — full, safely rendered decision body.
- **Level 4** — original source file and supporting evidence/provenance
  links.

### 8. Accessibility

Requires:

- keyboard-operable hash navigation;
- semantic links and headings;
- one logical page `<h1>`;
- correct heading hierarchy within detail views;
- visible focus;
- `aria-current` for active navigation;
- meaningful link text;
- accessible `<details>`/`<summary>` controls;
- no custom keyboard recreation where native elements suffice;
- responsive mobile layout;
- no page-level horizontal scrolling;
- reduced-motion support;
- readable long decision IDs, paths, hashes, and titles.

### 9. Search and filter scope

Authorizes simple local filtering by: decision ID; title; category; status;
related decision ID; keyword contained in pre-rendered metadata or body
text.

**Not authorized:** semantic search, embeddings, external indexing,
AI-generated summaries, or automatic ranking.

### 10. First implementation limit

The later implementation PR must prove the pattern end-to-end for all
current governance decisions, but **must remain limited to the Governance
Decision Explorer**. It must not add: Company Intelligence detail pages;
Theme pages; a backtest explorer; a workstream detail explorer; an evidence-
package browser beyond links/provenance; allocation logs; relationship
graphs; portfolio rankings; buy ladders; live prices; or cash or margin
recommendations.

### 11. Sealed and sensitive data boundary

Restated as a general dashboard rule, applying to this and every future
dashboard slice: **`research/margin_target_study/data/untouched_sealed/`
must never be read, indexed, listed, hashed for display, summarized, or
exposed by any dashboard path.** This Governance Decision Explorer
implementation must not access that directory at all — it has no reason to,
since its scope is `governance/decisions.yaml` and `governance/
decisions/*.md` only, but the boundary is restated explicitly per this
repository's "restate hard boundaries as standalone text" discipline
(`OPS-0009` §11, `OPS-0011` §5, `OPS-0012` §5).

### 12. Future phases — identified, not authorized

This decision identifies, and explicitly does **not** authorize
implementation of: Company/Holding detail pages; a Theme explorer; a
Backtest/study explorer; Workstream detail pages; an evidence/provenance
explorer; global cross-domain search. Each remains a separate future phase
requiring its own separate governance decision, exactly as `OPS-0011` §9
and `OPS-0012` §13 each required for their own next increments.

### 13. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/OPS-0013-governance-decision-explorer-authorization.md`
   (this file).
2. `governance/decisions.yaml` (index: one new entry).
3. `operations/WORKSTREAMS.yaml` (`WS-0007`: one new milestone recording
   this authorization — no existing milestone or field is edited or
   removed).
4. `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` (one new section recording the
   approved Governance Decision Explorer architecture — §§1–9 describing
   the merged Dashboard 1.0 architecture, and §9's Dashboard 2.0 direction,
   are unedited).
5. `CLAUDE.md` (one Decisions Log entry recording this filing, per this
   repository's established convention).

**No other file is touched.** No dashboard production code, test, asset,
generated artifact, `holdings.yaml`, `targets.yaml`, allocator, margin, or
Intelligence file is created or modified. **PR #212 and its branch
(`claude/dashboard-2-visual-redesign-xd0pip`) are untouched by this
filing.**

### 14. Workstream treatment

`WS-0007` ("Repository-native Portfolio-HQ dashboard") is the correct and
only host for this scope, per `OPS-0011` §6's established rule that no
other workstream may host dashboard/status-layer work. This filing adds
**one new milestone** to the existing `WS-0007` entry recording:

- Governance Decision Explorer authorization proposed;
- implementation not started;
- PR #212 remains separate and unaffected;
- the explorer implementation is gated on: this decision's own independent
  exact-head review; explicit principal acceptance; merge; and post-merge
  verification.

**No existing `WS-0007` field or milestone is edited, reordered, or
removed** — this filing is strictly additive, matching the discipline
`OPS-0012` §12 already applied to its own Phase 2 milestone addition. The
explorer is **not** marked authorized by this milestone; it becomes
authorized only when this governance PR merges, per `OPS-0009` §9's
merge-and-post-merge-verification discipline.

### 15. Review and merge gate

This governance PR must remain in draft, gain its own independent
exact-head review from an eligible reviewer under `OPS-0007` §1, complete
any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. It
does not mark itself ready and does not authorize its own merge. Per
`OPS-0009` §1 this is **Lane G — full weight, never reduced.**

The future implementation PR requires, separately and in addition:
exact-head independent review under `OPS-0007` §1, retained as a GitHub
review thread or a `governance/audits/` artifact; a bounded correction pass
resolving every material finding; scope verification against §§3–5, §9–11
of this decision; verification that no dashboard-package boundary
established by `OPS-0011`/`OPS-0012` is weakened; dedicated tests and
exact-head CI passing; explicit principal acceptance at the exact final
head; and immediate post-merge ancestry/scope/validator/test verification
(`OPS-0009` §9). **This decision's merge is a necessary precondition for
the implementation PR's merge, never a substitute for any item above.**

### 16. Effectivity

- This decision becomes effective **only when its own governance pull
  request merges to `main`** — not when pushed, and not when opened as a
  draft.
- Frontmatter `status: Accepted` follows this repository's established
  filing convention (`OPS-0007`, `OPS-0009`, `OPS-0011`, `OPS-0012` were
  each committed with that status inside their own unmerged draft PRs),
  paired with this explicit effectivity clause. **It is not a claim that
  independent review or principal acceptance has occurred** — neither has,
  as of this filing.
- No implementation work is authorized before that merge.
- Completing this authorization authorizes no further explorer phase
  (§12) and no default-daily-workflow integration.

## Rationale

**Why a new decision rather than stretching `OPS-0011`/`OPS-0012`.**
`OPS-0011` capped itself at one capability class and one implementation PR;
`OPS-0012` capped itself at one visual-redesign pass. Both are complete or
in progress on their own terms — `OPS-0012` merged, its implementation
(PR #212) is a bounded correction pass in flight. A decision drill-down
capability is new scope by the same self-imposed caps both decisions
already used, not a correction to either — the correct instrument is a new
decision, exactly as `OPS-0012` was for `OPS-0011`.

**Why capability-and-scope authorization, not diff approval.** This
repository's precedent authorizes a named, bounded module or scope before
it is built and separates that authorization from the implementation's own
independent review (`OPS-0007` §1, `OPS-0009` §2, `OPS-0011`/`OPS-0012`
Rationale). This decision follows the identical shape: a capability grant
(§2), a navigation-architecture boundary (§3), a model/source scope (§4),
security requirements (§5), authority-labeling requirements (§6),
disclosure levels (§7), accessibility requirements (§8), a search-scope
boundary (§9), an explicit first-implementation limit (§10), a sealed-data
restatement (§11), and named future phases that are identified but not
authorized (§12) — leaving exact implementation to a later, separately
reviewed PR.

**Why untrusted-Markdown treatment is required, not optional.** This
repository's own decision corpus spans dozens of authoring sessions over
several months, using prose (not a machine-checked schema) to express
narrowing, supersession, and historical status. Rendering that prose
safely — escaped or through a constrained renderer, with no script/event-
handler/iframe/remote-resource execution — is the only way to add a
Markdown-rendering capability without introducing exactly the kind of
client-side authority (`OPS-0011` §5's "no browser-side portfolio
authority") this dashboard has never permitted.

**Why supersession must never be inferred.** `OPS-0007` §2 and `OPS-0009`
Rationale both state explicitly that this repository's narrow-supersession
convention leaves the superseded decision's `status` field unchanged
(`Accepted`, not `Superseded`) even when a later decision narrows it in
prose. A drill-down view that inferred "superseded" from a later decision
existing, a later date, or a higher ID number would misstate this
repository's own settled convention and could mislead a reader into
believing a decision no longer controls when, in fact, only one clause of
it does. §4's prohibition exists specifically to prevent the explorer from
manufacturing a structured claim the underlying text does not make.

**Why the sealed-data boundary is restated here even though this slice
never approaches it.** This repository's practice (`OPS-0009` §11,
`OPS-0011` §5, `OPS-0012` §5) is to restate hard boundaries as each
decision's own standalone operative text rather than leave them to
cross-reference alone, precisely so a future implementation session reading
only this file has the complete boundary in front of it.

**Why the disclosed audit gap does not weaken this authorization.** This
filing's own preflight found no retained "Repository Explorer and
Drill-Down Architecture Audit" artifact anywhere in this repository. Rather
than silently treating the task's assertion of a completed audit as
verified fact — which `OPS-0011`'s own precedent (disclosing PR #199's
reviewer provenance as second-hand and unverified) counsels against — this
filing discloses the gap plainly and grounds the capability grant on this
decision's own stated reasoning instead, which stands independently of
whether that audit is ever located.

## Alternatives Considered

- **Fold this authorization into a bounded correction of `OPS-0012` or
  PR #212.** Rejected — `OPS-0012` is `status: Accepted` and merged;
  `governance/decisions/README.md` forbids editing accepted substance, and
  a new drill-down capability is new scope, not a correction to a visual
  redesign already in flight. Touching PR #212 at all would also violate
  this session's explicit instruction to leave it untouched.
- **Authorize a broader "repository explorer" capability spanning
  Company Intelligence, themes, backtests, and workstreams in one filing.**
  Rejected — over-broad by the same reasoning `OPS-0011`/`OPS-0012` each
  used to cap themselves at one capability/one pass; §12 names each of
  those as an identified, separately-authorizable future phase instead.
- **Treat the reported "completed Repository Explorer audit" as verified
  and cite its conclusions as controlling evidence.** Rejected — no such
  artifact exists anywhere in this repository (§Preflight); citing an
  unretained, unverifiable audit as evidence would repeat exactly the
  provenance gap `OPS-0004` Finding FA-1 identified and closed for review
  attribution. The capability grant instead stands on this decision's own
  stated Rationale.
- **Allow supersession to be inferred from decision ID ordering or date
  proximity, to make the detail view more informative.** Rejected — this
  repository's own convention (`OPS-0007` §2, `OPS-0009` Rationale)
  deliberately leaves a narrowed decision's `status` unchanged; an
  inference rule would contradict that convention and could misstate which
  decisions currently control.
- **Permit a lightweight client-side Markdown library instead of a
  constrained renderer or escaping.** Rejected — `OPS-0011` §5 already
  prohibits any external script or CDN dependency; a bundled third-party
  Markdown library would also need its own security review of its HTML-
  sanitization behavior, which this filing does not perform and does not
  authorize. §5 requires escaping or a "deliberately constrained" renderer
  built and reviewed as part of the implementation PR itself.
- **Authorize implementation to begin in this same session.** Rejected —
  explicitly out of scope per this session's own instruction, and
  inconsistent with `OPS-0007` §1 / `OPS-0009` §2: this decision has not
  been independently reviewed or principal-accepted, and collapsing
  authorization with implementation would let an unreviewed filing confer
  merge authority on code nobody has yet reviewed.

## Consequences

**Authorized, effective on this decision's merge:** one Governance Decision
Explorer capability as scoped in §§2–12, delivered through exactly one
future, separate, bounded implementation PR, under the fully-restated
`OPS-0011` mandatory boundaries in §5 and the review/merge gate in §15; and
one new milestone on the existing `WS-0007` register entry recording this
authorization as proposed pending merge.

**Unchanged by this decision:** `OPS-0001` through `OPS-0012` in full,
unedited — including `OPS-0011`'s complete capability-class grant and
`OPS-0012`'s Dashboard 2.0 visual-redesign authorization and its in-flight
implementation (PR #212, left entirely untouched by this filing); `WS-0002`,
`WS-0003`, `WS-0005`, and `WS-0006` in full; every tier, target, role,
cluster, cap, and holding in `targets.yaml` and `holdings.yaml`;
`allocate.py`, `margin_state.py`, every Intelligence record and validator,
and every existing test; the 1.8x leverage cap and 30% buffer floor;
`MARGIN-0005`'s charter and trial ceiling; `PHQ-2026-01`'s approved
architecture and its seven gated names; and `OPS-0006`'s Milestone 4-9
boundary.

**PR #212 is untouched by this filing** — its state (open, draft, unmerged,
head `925d09bb22fdbc2b9e717bab1c224752d2c35d38`) is exactly as found at
this decision's preflight, and proceeds entirely on its own separate
`OPS-0012` §11 lifecycle, unaffected by anything in this decision.

**No trade, order, holdings reconciliation, gated-name activation, target
change, allocator change, margin change, or dashboard code change is
authorized or implied.** The next concrete step is this governance PR's own
independent exact-head review, per §15 — not implementation, not any change
to PR #212 or dashboard code, and not merge.
