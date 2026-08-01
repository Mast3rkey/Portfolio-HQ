---
decision_id: OPS-0012
date: 2026-08-01
status: Accepted
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0005, OPS-0006, OPS-0007, OPS-0009, OPS-0011, PHQ-2026-01]
supporting_artifact: null
---

## Context

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ` (remote `origin`).
- **`origin/main` fetched**; this filing's base is `f86fd98f38067ad53ab52c982356058ffefbbb38`
  (merge commit of PR #210, "WS-0007 `active_pr` self-reference correction").
  **Local branch, `origin/main`, and this filing's base are identical** —
  no divergence. **Working tree confirmed clean** on branch
  `claude/dashboard-2-governance-auth-5a8n9h`, created directly from
  `origin/main`.
- **PR #210 confirmed merged** (`WS-0005: record ISRG's completed post-merge
  verification`, itself the last of a short chain closing the ISRG
  post-merge-verification and `WS-0007` `active_pr` self-reference gaps).
- **Zero open pull requests** in the repository at preflight — confirmed via
  a live `state: open` query. No competing or overlapping dashboard
  governance work, no open implementation branch for a second dashboard
  surface, and no in-flight PR of any kind this filing could conflict with.
- **`OPS-0012` confirmed the next unused identifier** — checked live against
  both `governance/decisions/` (54 non-`README` files; highest filed
  `OPS-####` is `OPS-0011`; highest `PI-####` is `PI-0035`) and
  `governance/decisions.yaml` (54 entries, reconciling exactly, verified by
  direct set comparison of filenames against indexed `file:` values — no
  orphan on either side).
- **`WS-0007` ("Repository-native Portfolio-HQ dashboard") confirmed
  `status: complete`, `priority: secondary`.** Its single authorized
  implementation PR (`PR #199`, merge commit
  `30c9e1bb5aa67a3fe47b176922dcdc7d6b4de000`) merged 2026-07-31 after
  independent exact-head review, resolution of every reported finding,
  explicit principal acceptance, and immediate post-merge verification. Its
  `completion_criteria` — one bounded implementation PR merging under the
  full lifecycle — is satisfied and is **not reopened or edited by this
  filing.**
- **The complete current dashboard package read at this exact head**:
  `portfolio_hq/dashboard/{__init__.py, __main__.py, cli.py, model.py,
  provenance.py, render.py, server.py, assets/dashboard.css}` (2,509 lines
  across the package plus its dedicated test module),
  `docs/PORTFOLIO_HQ_DASHBOARD.md` (user guide), and
  `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` (design note / source-of-truth
  map). `test_portfolio_hq_dashboard.py` (597 lines, 52 tests) re-run this
  session: **52/52 passed.** The provenance and security boundaries
  (`OPS-0011` §§2, 4, 5, restated in full in this decision's own §5) were
  independently re-confirmed present in the merged code: loopback-only
  server binding enforced at `cli.py` argument-parse time, GET-only routing
  with mutating methods rejected by `server.py`, no external asset or
  network dependency in `render.py`/`assets/dashboard.css`, and
  `model.py` reusing `allocate.build_roster` / `intelligence_report.*`
  rather than duplicating governed calculations.
- **Full validation baseline re-run this session, at this exact head**:
  `python3 -m pytest test_portfolio_hq_dashboard.py -q` → **52 passed**;
  `python3 -m pytest -q` (full suite) → **1601 passed**; `intelligence_validator.py`
  → OK; `freshness_validator.py` → OK; `governance/decisions.yaml`
  reconciliation → 54 filed = 54 indexed, no orphans; `git diff --check` →
  clean (verified again after this filing's own edits, §Validation below).
- **No overlapping dashboard work found.** No open PR, no unmerged branch
  under active development, and no other governance filing currently
  proposes a second dashboard interface, generator, or visual layer. This
  filing is the first proposal of a Dashboard 2.0 visual pass.

### Why a new decision, not an edit to `OPS-0011`

`governance/decisions/README.md` forbids editing a decision's substance
after `status: Accepted`. `OPS-0011` authorized exactly one capability class
and exactly one implementation PR (its §2.12, §3 preamble); that single PR
has merged and `WS-0007`'s completion criteria are satisfied. A second,
visually comprehensive redesign of the same capability is new scope, not a
correction to the first — it requires its own decision under the same
"authorize the module before it is built" discipline `OPS-0011` itself
followed (`PI-0002`, `PI-0011`, `AUTO-0002`/`AUTO-0003`, `OPS-0005` §3
precedent, restated at `OPS-0011` Rationale). `OPS-0011` is **not
superseded, narrowed, or reinterpreted** by this filing — every boundary it
established for the dashboard capability class remains binding in full
(§5 below cross-references rather than restates them).

### Principal direction

The principal has explicitly directed that the dashboard be redesigned
through rapid visual iteration toward a modern, smooth, premium,
user-friendly, easy-to-navigate, easy-to-understand experience that is
responsive on desktop and mobile, visually polished, calm rather than
noisy, dark-first, features subtle animation, strong typography and
spacing, clear visual hierarchy, and is suitable for frequent daily use. The
principal authorizes the designer to take reasonable visual liberties
within the safety and governance boundaries this decision restates, and
expects to inspect the rendered result and refine it through later bounded
correction passes rather than have every visual detail pre-specified here.

## Decision

**OPS-0012 authorizes one bounded design direction and one future,
separate, bounded implementation PR — "Dashboard 2.0" — that
comprehensively redesigns the presentation layer of the already-authorized
`WS-0007` repository-native dashboard capability.** It authorizes a design
direction, an information architecture, and an implementation scope —
never a specific diff, and never a pixel-level specification. This filing
creates no dashboard code, no generated artifact, no CSS, and no test; it
touches only the governance package named in §9.

### 1. Finding

- `WS-0007`'s single authorized implementation PR (`OPS-0011` §3) has
  merged and its completion criteria are satisfied (§Preflight). No further
  dashboard scope is currently authorized.
- The principal has directed a comprehensive visual redesign, exceeding
  what a bounded correction to the existing render could deliver, and has
  explicitly authorized reasonable visual liberties within governance
  bounds.
- Per the same precedent `OPS-0011` itself followed, a new capability
  increment — here, a visual/UX redesign pass, not a new data capability —
  requires its own advance authorization before implementation, not a
  retroactive one.

### 2. Grant — approved design direction

Authorizes a **restrained modern financial-application aesthetic**,
inspired by the qualities of premium contemporary software without copying
any specific existing product, targeting:

- a dark charcoal background rather than pure black, as the default theme;
- layered surfaces with restrained translucency where the browser supports
  it, degrading gracefully where it does not;
- clean cards with consistent corner radii, borders, shadows, and spacing;
- large, legible summary values with clear section hierarchy;
- polished typography using system-safe font stacks only (no hosted or
  bundled font files — §5 restates this as a hard boundary, not a
  preference);
- subtle hover, focus, disclosure, and page-entry transitions — calm, not
  novel; no flashing, excessive parallax, gamification, or decorative
  effect that reduces comprehension;
- a responsive sidebar or compact mobile navigation pattern;
- smooth table and card interactions, with excellent desktop, tablet, and
  phone behavior;
- accessible contrast and visible keyboard focus in both light and dark
  presentations (`OPS-0011` §2.11 already requires accessibility tests;
  §7 below is specific to this visual pass).

The implementation should feel fast and calm. Designer discretion on exact
palette, spacing scale, radii, shadow depth, and animation timing is
authorized within these qualities and within §5's boundaries; this filing
does not fix numeric design-token values.

### 3. Information architecture for the first pass

Authorizes a visual and navigational redesign of the dashboard's existing
information into five clearly labeled areas, built **only from information
already available through the current dashboard model** (`model.py`'s
existing view-model and the source-of-truth map in
`docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` §5, both unchanged by this filing):

1. **Overview** — repository and portfolio status, high-priority notices,
   portfolio snapshot, governance/workstream summary, Intelligence/freshness
   summary, provenance and generated-at information.
2. **Portfolio** — current governed assets and targets in a readable
   desktop table with a mobile-friendly stacked presentation, sorting where
   already supported (the existing `data-sortable` mechanism), and clear
   empty/unavailable/warning states.
3. **Intelligence** — current coverage and freshness information already
   available via `intelligence_report.*`; no new research conclusions; no
   automatic scoring or ranking.
4. **Governance** — accepted decisions, workstream state, and items
   requiring attention where already represented by repository truth.
5. **System / Provenance** — source files, hashes, branch/commit/dirty
   state, warnings and limitations, and a clear statement that generated
   HTML is non-authoritative.

**No new investment calculation may be added merely to fill a design
card.** If the current model cannot support a desired metric, the
implementation must omit it or label it unavailable rather than inventing
it — the same disclosure-or-abstention discipline `OPS-0011` §2.8 already
binds the capability to.

### 4. Permitted implementation scope — exactly one future implementation PR

Authorizes **exactly one** future, separate implementation pull request —
not opened, not begun, and not scoped to any exact diff by this filing.
That PR may comprehensively change the presentation layer within the
existing repository-native dashboard capability, and may include:

- restructuring the generated HTML;
- redesigning `assets/dashboard.css` (or its successor stylesheet source);
- adding minimal local JavaScript for navigation and presentation
  interactions only — no new data-fetching, no new calculation;
- responsive navigation (sidebar / compact mobile pattern per §2);
- semantic page sections or client-side views within the one generated HTML
  document (`OPS-0011` §2.2's "one canonical generator, one master
  interface" is unchanged — this is still a single generated document, not
  a second interface);
- redesigned cards, badges, notices, tables, disclosure panels, and
  provenance sections for the five areas in §3;
- accessible sorting and navigation, subtle animations and transitions, and
  reduced-motion handling (§7);
- responsive desktop/tablet/mobile layouts and dark-mode polish;
- empty/error/loading-style states suitable for static generation;
- visual consistency tokens implemented as CSS custom properties;
- documentation updates (`docs/PORTFOLIO_HQ_DASHBOARD.md`,
  `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md`);
- focused accessibility and rendering tests, additive to the existing 52.

This PR must remain **within** the existing `portfolio_hq/dashboard`
package and generator (`OPS-0011` §2.2) — it is a visual and structural
redesign of that one capability, not a second dashboard, a second
generator, or a parallel interface.

### 5. Mandatory boundaries — `OPS-0011` restated in full, unweakened

Every protection `OPS-0011` established for the dashboard capability class
remains fully binding on this redesign, without exception. Restated here as
this decision's own operative text (not left to cross-reference alone,
matching the discipline `OPS-0009` §11 already applies to its own hard
boundaries):

- read-only; recommendation-only; advisory; display-only; additive; outside
  `allocate.py`'s calculation path; outside margin research; and outside
  the default daily workflow until separately authorized (`OPS-0011` §4);
- **one** repository-native dashboard capability, **one** canonical
  generator, **one** supported master HTML interface (`OPS-0011` §2.1–2.2);
- static standalone HTML from structured repository sources plus local
  `git` metadata (`OPS-0011` §2.3);
- the optional local server bound **only** to `127.0.0.1` — binding to
  `0.0.0.0`, a LAN address, or any other externally reachable interface is
  not authorized, not as a default, not as an option, and not as a
  configurable setting (`OPS-0011` §2.4, §5); GET-only, mutating methods
  rejected;
- no brokerage connection; no Robinhood or Alpaca query; no order path of
  any kind (`OPS-0011` §5);
- no secrets, no credential field, no authentication surface;
- no repository mutation from the dashboard — no `<form>`, no write path to
  `holdings.yaml`, `targets.yaml`, any gate, any accepted decision, or
  `operations/WORKSTREAMS.yaml` (`OPS-0011` §5);
- no second allocator; no duplicated governed calculation (tier, target,
  cap, gate, trim, buffer, or leverage logic) in the generator, template,
  redesigned CSS, or new JavaScript (`OPS-0011` §4, §5);
- no automatic Intelligence scoring, ranking, or policy coupling
  (`OPS-0011` §5; §3 above restates this for the Intelligence area
  specifically);
- no change to `holdings.yaml`, `targets.yaml`, any gate, any cluster cap,
  margin policy, or allocation behavior of any kind;
- generated HTML remains non-authoritative and gitignored — the visual
  redesign changes presentation, never this status (`OPS-0011` §2.10,
  §3 "Generated HTML must never be committed");
- no hosted fonts, remote scripts, remote icons, analytics, tracking, or
  telemetry — system fonts, embedded/local CSS, and simple inline or
  locally generated visual assets only (`OPS-0011` §5).

### 6. Performance requirements

The future implementation must:

- load as one static file without network dependencies;
- remain responsive with the full current repository dataset;
- avoid large animation frameworks and unnecessary JavaScript;
- avoid layout shifts;
- remain usable when JavaScript presentation enhancements fail (the
  existing "the page is fully usable with JS disabled" discipline in
  `render.py`'s `_JS` docstring is preserved, not weakened, by this visual
  pass);
- keep the generated artifact reasonably sized;
- preserve fast local build and test performance.

### 7. Accessibility requirements

The future implementation must provide:

- semantic landmarks and correct heading hierarchy;
- keyboard-accessible navigation and controls with visible focus states;
- accurate `aria-current` and `aria-sort` where applicable;
- sufficient contrast, with no color-only status communication;
- reduced-motion support (respecting `prefers-reduced-motion`);
- usable touch targets;
- responsive text without horizontal page scrolling;
- tables that remain comprehensible on narrow screens.

### 8. Visual acceptance standard

The first Dashboard 2.0 implementation pass is successful when:

- a first-time user can understand the dashboard's major sections without
  instructions;
- the primary navigation is obvious;
- the most important notices and repository status are immediately
  visible;
- desktop and mobile layouts both feel intentionally designed;
- visual hierarchy is materially improved over the current (Dashboard 1.0)
  foundation;
- interaction feels smooth but restrained;
- no placeholder metric appears as factual portfolio information;
- all provenance and safety disclosures remain accessible;
- the principal can run the dashboard locally and provide concrete visual
  feedback for a later, bounded correction pass.

### 9. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/OPS-0012-dashboard-2-modern-responsive-experience-authorization.md`
   (this file).
2. `governance/decisions.yaml` (index: one new entry).
3. `operations/WORKSTREAMS.yaml` (`WS-0007`: one new milestone recording
   this authorization, and the minimum field updates — `status`,
   `authorized_scope`, `prohibited_scope`, `next_action`,
   `completion_criteria`, `blocker`, `last_verified_main_sha`,
   `last_verified_date`, `authorized_by` — needed to describe the new,
   still-conditional Phase 2 scope. **No existing milestone, and no fact
   about the completed Phase 1/`PR #199`, is edited or removed.**).
4. `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` (one new section recording the
   approved Dashboard 2.0 design direction, information architecture, and
   implementation requirements — §§1–8 describing the merged Dashboard 1.0
   architecture are **unedited**, since the canonical generator, module
   organization, and source-of-truth map they describe remain the
   foundation this redesign builds on).
5. `CLAUDE.md` (one Decisions Log entry recording this filing, per this
   repository's established convention).

**No other file is touched. No dashboard production code, test, asset,
generated artifact, `holdings.yaml`, `targets.yaml`, allocator, margin, or
Intelligence file is created or modified.** Dashboard coding does not begin
in this session.

### 10. Explicitly not authorized

This decision does **not** authorize, and the future implementation PR must
not include:

- new portfolio calculations, a portfolio-health score, an investment
  ranking, a buy ladder, or a deployment recommendation;
- live prices or any brokerage data of any kind;
- any cash-allocation behavior or margin deployment;
- automatic alerts or background monitoring;
- hosted deployment, public access, LAN access, or authentication;
- new Intelligence conclusions, or any Intelligence-to-allocator coupling;
- any target, tier, gate, cluster, or policy change;
- `WS-0005` Milestone 4 relationship-mapping implementation;
- charts or relationship graphs requiring invented or ungoverned data;
- any visual claim unsupported by the current dashboard model;
- a second dashboard interface, a second generator, or default-daily-workflow
  integration (`run_portfolio_check.sh` or its successor) — each would
  require its own separate future governance decision, exactly as
  `OPS-0011` §9 already held for the first pass.

### 11. Implementation lifecycle

Requires, in order:

1. this governance/design authorization PR;
2. independent exact-head review under `OPS-0007` §1's capability-based
   standard;
3. explicit principal acceptance of this governance filing;
4. merge and immediate post-merge verification (`OPS-0009` §9);
5. one separate, bounded implementation PR (§4);
6. rendered desktop and mobile preview artifacts, provided with that PR for
   principal inspection;
7. focused accessibility and presentation tests, additive to the existing
   52;
8. full applicable validation (dashboard test module, full suite, exact-head
   CI);
9. independent exact-head implementation review under `OPS-0007` §1;
10. explicit principal **visual** acceptance — not merely a code-correctness
    acceptance, given the nature of this change;
11. merge and immediate post-merge verification;
12. any later visual corrections proceed only as bounded delta passes
    (`OPS-0009` §1 Lane C), never as a silent second full redesign under
    this same authorization.

This governance PR itself must remain in draft, gain its own independent
exact-head review from an eligible reviewer under `OPS-0007` §1, complete
any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. It
does not mark itself ready and does not authorize its own merge. Per
`OPS-0009` §1 this is **Lane G — full weight, never reduced.**

The future implementation PR requires, separately and in addition,
everything `OPS-0011` §8 already requires of the dashboard's implementation
PR (exact-head independent review, retained attribution, a bounded
correction pass resolving every material finding, scope verification
against §4/§9 of this decision, verification of `OPS-0011` §4's dependency
direction, verification that allocator output is provably unchanged for
identical inputs, dedicated tests and exact-head CI passing, explicit
principal acceptance at the exact final head, and immediate post-merge
ancestry/scope/validator/test verification) — plus the rendered
desktop/mobile preview artifacts and explicit principal **visual**
acceptance named in §11 items 6 and 10 above, which are new requirements
specific to a visual redesign and have no equivalent in `OPS-0011`'s
original data-capability authorization.

**This decision's merge is a necessary precondition for the future
implementation PR's merge, never a substitute for any item above.**

### 12. Workstream treatment

`WS-0007` is the correct and only host for this scope — it already governs
"Repository-native Portfolio-HQ dashboard" as a capability, and
`OPS-0011` §6 already established that no other workstream (`WS-0002`,
`WS-0003`, `WS-0005`) may host dashboard/status-layer work. This filing
therefore adds **one new milestone** to the existing `WS-0007` entry rather
than creating a new workstream, per this repository's own smallest-unit
discipline (`OPS-0001`'s register conventions; the `WS-0002`
multi-phase precedent, where `OPS-0005`'s Phase Two reactivation extended
the same entry rather than opening a new one).

Because this governance PR is **unmerged at filing time**, and because
`OPS-0001` forbids an AI session from self-authorizing a workstream to
`authorized` status, `WS-0007`'s top-level `status` is set to
**`proposed`** for the duration of this filing — describing the new,
conditional Phase 2 scope only. **This is not a reopening or edit of
Phase 1's substance**: every existing `WS-0007` milestone (`PR #200`
capability authorization, `PR #199` candidate identification,
independent review/correction/merge) is left byte-unchanged, and
`authorized_scope`/`prohibited_scope` are updated additively to describe
Phase 1 as complete/historical and Phase 2 as conditional on this
decision's own merge — the same additive-not-rewriting discipline
`OPS-0011` §6 applied to `WS-0003`.

**Post-merge synchronization required** (one continuous step, performed
immediately by the merging session per `OPS-0009` §9): flip `WS-0007`
back to `status: authorized` for the new Phase 2 scope, record this
decision's merge commit, and update `last_verified_main_sha`/
`last_verified_date`. That transition is a factual recording of an
accomplished merge, not a new authorization.

### 13. Authority boundary — what this decision does not do

This decision does **not**:

- approve any specific visual design, code, palette, or line of a future
  implementation — it authorizes a design direction and a bounded scope,
  and any future implementation PR must still independently satisfy §§2–8
  and the full lifecycle in §11;
- open, begin, or scope an exact diff for the future implementation PR;
- narrow, reinterpret, or weaken any `OPS-0011` boundary — §5 restates them
  in full, it does not relax them;
- authorize `WS-0005` Milestone 4, any research batch, or any Intelligence
  content;
- change `OPS-0005`'s Phase Two grant, `WS-0002`, or `WS-0003`;
- authorize any trade, order, holdings reconciliation, gated-name
  activation, target/tier/role/cluster/cap/margin change, or
  `PHQ-2026-01`/`PHQ-2026-02` implementation of any kind;
- integrate the dashboard into the default daily workflow.

### 14. Effectivity

- This decision becomes effective **only when its own governance pull
  request merges to `main`** — not when pushed, and not when opened as a
  draft.
- Frontmatter `status: Accepted` follows this repository's established
  filing convention (`OPS-0007`, `OPS-0009`, `OPS-0011`, `PHQ-2026-01`
  through `PHQ-2026-05` were each committed with that status inside their
  own unmerged draft PRs), paired with this explicit effectivity clause.
  **It is not a claim that independent review or principal acceptance has
  occurred** — neither has, as of this filing.
- No dashboard implementation work is authorized before that merge, and the
  future implementation PR may not merge until §11's separate gates
  complete against its own exact head.
- Completing this authorization authorizes no further phase, no
  default-workflow integration, and no second interface.

## Rationale

**Why a new decision rather than stretching `OPS-0011`.** `OPS-0011`
capped itself deliberately at one capability class and one implementation
PR (its own Rationale: "over-broad by the same reasoning `OPS-0005` used to
cap itself at one PR and `MARGIN-0005` used to cap its trials"). That PR
has merged. A comprehensive visual redesign is new scope by that same
self-imposed cap, not a correction — the correct instrument is a new
decision, exactly as `OPS-0011` itself was for the original capability gap.

**Why capability-and-direction authorization, not diff or pixel approval.**
This repository's precedent authorizes a named, bounded module or scope
*before* it is built and separates that authorization from the
implementation's own independent review (`OPS-0007` §1, `OPS-0009` §2,
`OPS-0011` Rationale). A visual redesign is harder to bound with the same
precision as a data capability, so this decision bounds it the way the
principal's own direction is structured: a design-quality target (§2), an
information architecture (§3), a permitted scope (§4), and unweakened
safety boundaries (§5) — leaving exact visual execution to the
implementation session and the principal's later inspection (§11 items 6
and 10), rather than pre-specifying colors or spacing values that would
constrain rapid iteration without adding real safety.

**Why the redesign is constitutionally safe.** Constitution §1 permits a
decision-support advisor that computes recommendations for manual
execution; §4 prohibits standing *predictive* research layers. A visual
redesign of an existing read-only render changes no computation and adds
no prediction, score, or ranking — §3's "no new investment calculation to
fill a design card" and §10's explicit exclusions are what keep this
redesign on that side of the line, the same reasoning `OPS-0011`'s
Rationale already established for the underlying capability.

**Why `WS-0007`, not a new workstream.** `OPS-0011` §6 already established
that `WS-0002`, `WS-0003`, and `WS-0005` may not host dashboard work, and
that a dedicated workstream is the correct home. `WS-0007` already is that
workstream; the `WS-0002` multi-phase precedent (`OPS-0005` extending the
same entry rather than opening a new one for Phase Two) is the closest
analog, and the smallest-unit discipline this repository applies
throughout favors extending the existing entry over duplicating its
history in a new one.

**Why the visual redesign needs its own principal acceptance step, not
just correctness review.** Code correctness and governance-boundary
compliance are necessary but not sufficient for a request whose entire
purpose is subjective visual quality ("modern," "premium," "calm"). §11
therefore names rendered preview artifacts and explicit principal *visual*
acceptance as first-class lifecycle steps, distinct from and additional to
the ordinary code-review gate `OPS-0007` §1 already requires.

## Alternatives Considered

- **Amend `OPS-0011` directly to add a second implementation PR.**
  Rejected — `governance/decisions/README.md` forbids editing accepted
  substance, and `OPS-0011` deliberately capped itself at one PR with its
  own stated rationale. A separate decision for a separate scope is the
  correct instrument, matching `OPS-0011`'s own treatment of `OPS-0005`
  and `MARGIN-0005`.
- **Pre-specify exact design tokens (hex colors, spacing scale, font
  sizes) in this decision.** Rejected — the principal explicitly asked for
  rapid visual iteration with designer discretion within safety bounds;
  fixing numeric values here would convert a governance authorization into
  a design spec no future session could improve on without another
  governance cycle, defeating the stated purpose.
- **Authorize implementation to begin in this same session.** Rejected —
  explicitly out of scope per the task's own instruction, and inconsistent
  with `OPS-0007` §1 / `OPS-0009` §2: this decision has not been
  independently reviewed or principal-accepted, and collapsing
  authorization with implementation would let an unreviewed filing confer
  merge authority on code nobody has yet reviewed.
- **Create a new workstream (`WS-0010`) instead of extending `WS-0007`.**
  Rejected — `OPS-0011` §6 already reserved this exact capability under
  `WS-0007`; a new workstream would duplicate history the existing entry
  already carries and would require its own justification for why
  `WS-0007` is insufficient, which does not exist.
- **Authorize a broader "visual design system" capability spanning future
  dashboards or other surfaces.** Rejected — over-broad by the same
  reasoning `OPS-0011` used to cap itself: one capability, one redesign
  pass, one future PR, enumerated file list. A future need for a second
  surface or a reusable design system is a future decision.
- **Skip the rendered-preview / visual-acceptance step and rely on the
  ordinary code-review gate alone.** Rejected — a redesign's success
  criterion is subjective visual quality, which code review alone cannot
  verify; §11 names preview artifacts and explicit visual acceptance as
  their own steps precisely because code correctness does not imply visual
  success.

## Consequences

**Authorized, effective on this decision's merge:** one Dashboard 2.0
design direction and information architecture as scoped in §§2–3,
delivered through exactly one future, separate, bounded implementation PR
as scoped in §4, under the fully-restated `OPS-0011` mandatory boundaries
in §5, the performance and accessibility requirements in §§6–7, the visual
acceptance standard in §8, and the twelve-step implementation lifecycle in
§11; and one new milestone on the existing `WS-0007` register entry,
transitioning from `complete` (Phase 1, unedited) to `proposed` (Phase 2,
this filing) and, on merge, to `authorized` (Phase 2, conditional) in the
immediate post-merge synchronization described in §12.

**Unchanged by this decision:** `OPS-0001` through `OPS-0011` in full,
unedited — including `OPS-0011`'s complete capability-class grant, its
mandatory boundaries and prohibitions (restated, not altered, in §5), and
`WS-0007`'s completed Phase 1 milestones (`PR #200`, `PR #199`); `OPS-0005`'s
stdout-only Phase Two grant; `WS-0002`, `WS-0003`, `WS-0005`, and `WS-0006`
in full; every tier, target, role, cluster, cap, and holding in
`targets.yaml` and `holdings.yaml`; `allocate.py`, `margin_state.py`, every
Intelligence record and validator, and every existing test; the 1.8x
leverage cap and 30% buffer floor; `MARGIN-0005`'s charter and trial
ceiling; `PHQ-2026-01`'s approved architecture and its seven gated names;
and `OPS-0006`'s Milestone 4-9 boundary.

**Dashboard production code is untouched by this filing** — the
`portfolio_hq/dashboard` package remains exactly as merged at `PR #199`'s
head (`700f913e851fce6f6e82c2a328f17e295339615a`). No investment behavior,
allocator output, margin computation, or Intelligence content changes as a
result of this decision. The next concrete step is this governance PR's
own independent exact-head review, per §11 — not implementation, not any
change to dashboard code, and not merge.
