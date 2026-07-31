---
decision_id: OPS-0011
date: 2026-07-31
status: Accepted
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0002, OPS-0005, OPS-0006, OPS-0007, OPS-0009, PI-0011, PHQ-2026-01]
supporting_artifact: null
---

## Context

Reported to this filing session by the principal, and **not seen, verified,
reproduced, or retained here**, an independent review of draft PR #199 ("feat:
repository-native Portfolio-HQ dashboard (read-only)") is said to have
identified a **missing repository authorization** for the dashboard
capability. **This filing takes no position on that implementation's technical
quality** — it neither endorses nor disputes it, and nothing in this decision
may be cited as a finding about PR #199's code. The gap this decision closes is
the missing capability authorization, not any judgment about PR #199's
implementation.

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ` (remote `origin`).
- **`origin/main` fetched and pruned**; this filing's base is
  `9bf2c61ab085bc55448f3cef4cae40f92798bc73` (merge commit of PR #198).
- **Working tree confirmed clean** at that base; this governance branch was
  created directly from `origin/main`.
- **PR #199** confirmed **open, `draft: true`, `merged: false`**, head exactly
  `4f9f6d0633d1be3107a6a6922abc25518b6ece26`, base `main` at `9bf2c61…`;
  13 files changed, all additive except `.gitignore`. Its exact-head CI check
  (`test`, run `30632939240`) is `completed` / `success`. **It carries zero
  GitHub reviews**, and no retained artifact anchored to its head exists under
  `governance/audits/`. **This filing does not modify, review, approve, mark
  ready, or merge it.**
- **PR #199 is the only open pull request** in the repository. No competing or
  overlapping governance PR exists, and no other branch claims this scope.
- **`OPS-0011` confirmed the next unused identifier** — checked live against
  both `governance/decisions/` (48 non-`README` files; highest `OPS-####` is
  `OPS-0010`; highest `PI-####` is `PI-0034`) and `governance/decisions.yaml`
  (48 entries, reconciling exactly). No ambiguity in the sequence.
- **Repository-wide search for prior dashboard authority performed** across
  `governance/`, `constitution/`, `operations/`, `docs/`, and `CLAUDE.md`.
  Every hit is either a *rejection* (`OPS-0001`'s "no duplicate dashboard"),
  a *prohibition* (`OPS-0006` §prohibitions; `operations/WORKSTREAMS.yaml`
  WS-0005 `prohibited_scope`), a *non-goal* (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
  "not a dashboard, UI, or reporting product"), or a *speculative future
  capability* in a non-authoritative audit document
  (`docs/PORTFOLIO_HQ_AUDIT.md`). **No accepted decision authorizes an HTML
  dashboard capability.**
- **`docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` read at PR #199's exact head**, via
  the PR diff, without modifying that branch.

### The authority gap, stated exactly

1. **`WS-0003` ("Daily allocation-check user experience") remains
   `status: proposed`**, with `authorized_scope: "none — durable planning
   intent only"` and a `prohibited_scope` reading "Any presentation, UX, or
   reporting implementation; any allocator output change; this entry
   authorizes recording the intent only." `OPS-0001` established WS-0003 as
   **recording only** and explicitly declined to scope, design, or authorize
   it. WS-0003 therefore authorizes nothing, and its own text says so.
2. **`OPS-0005` §3 explicitly declined a generated report artifact** for
   WS-0002 Phase Two — "No generated or tracked report file is authorized —
   the layer is **stdout-only and display-only**" — while its Alternatives
   Considered left the door open in terms: "nothing prevents a future decision
   from adding one if a real need is demonstrated." `OPS-0005` §4 additionally
   prohibits the Phase Two implementation from "begin[ning] Phase Three, or any
   WS-0003 (daily allocation-check UX) work." A dashboard that writes an HTML
   file is therefore **outside** the only implementation authority WS-0002
   currently holds, not a variation within it.
3. **`OPS-0001` rejected a generated dashboard for the register v1** on
   duplicate-source-of-truth grounds, with the same explicit future-decision
   carve-out ("Nothing prevents a future decision from adding one if a real
   discoverability gap is demonstrated").
4. **`OPS-0006` and `operations/WORKSTREAMS.yaml`'s WS-0005 entry both list
   "WS-0002 Phase Two (or later) dashboard/status-layer implementation" and
   "WS-0003 or default-daily-workflow changes" in prohibited scope** — WS-0005
   cannot host this work either.
5. **This repository's settled precedent authorizes a new module before it is
   implemented**, not after: `PI-0002` (`intelligence_validator.py`),
   `PI-0011` (`intelligence_report.py`), `AUTO-0002`/`AUTO-0003` (the
   `freshness_*` modules), and `OPS-0005` §3 (the Phase Two status module) each
   authorized a named, bounded module in advance.
6. **A design note cannot self-authorize its own implementation.**
   `docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md` is a document produced by the same
   implementation PR it describes; under `GOV-0002`'s precedence hierarchy and
   `OPS-0001`'s "the register never originates authority" principle, a
   `docs/` file is not a source of repository authority. `OPS-0004`'s Finding
   FA-1 closed exactly this category of gap for review provenance; the same
   logic applies to authorization provenance.

Consequently: the capability implemented in PR #199 is **unauthorized, not
disallowed**. Nothing in the Constitution, in `CLAUDE.md`, or in any accepted
decision prohibits a read-only presentation surface over repository truth —
the gap is that no decision has ever affirmatively permitted one. That is a
gap only a new governance decision can close, and this is that decision.

### Independent-review provenance, disclosed precisely

The finding summarized above was **conveyed to this authoring session by the
principal** as the reason this task exists. This session independently
re-derived every element of it against live repository state (§Preflight
above) and states it here on that basis. **No retained independent-review
artifact for PR #199 exists in this repository**, and PR #199 carries zero
GitHub reviews — both independently confirmed this session. The reviewer is
separately reported to have raised **four implementation findings** against
PR #199; **this session has not seen, verified, or reproduced their content,
and this decision neither restates nor resolves them.** Nothing in this
filing may be read as a claim that any independent reviewer has reviewed,
endorsed, or approved **this** governance decision. This decision's own
independent review has not occurred.

## Decision

**OPS-0011 authorizes one bounded capability class — a repository-native,
read-only, local-only Portfolio-HQ dashboard — and the single future
implementation PR that may deliver it.** It authorizes a *capability and a
scope*, never a specific diff. This filing creates no dashboard code, no
generated artifact, and no test; it touches only the governance package named
in §10.

### 1. Finding

- No accepted decision currently authorizes a dashboard capability (§Context).
- `WS-0003` authorizes nothing and prohibits presentation/UX/reporting
  implementation **within WS-0003**; `OPS-0005` §3 declined a generated report
  artifact for WS-0002 Phase Two while expressly leaving a future decision
  free to authorize one; `OPS-0001` did the same for the register.
- A new, explicit decision is therefore required before this capability may be
  implemented or merged. This filing is that decision.
- **PR #199's existence does not alter this finding.** Work performed ahead of
  authorization is not retroactively legitimized by this decision; PR #199
  remains an unapproved candidate implementation subject in full to §8.

### 2. Grant — the authorized capability class

Authorizes **one repository-native Portfolio-HQ dashboard capability**, with
exactly these properties:

1. **One repository-native dashboard capability** — a presentation surface
   over this repository's own committed state, and nothing else.
2. **One canonical generator and one supported master HTML interface.** Not
   two generators, not a family of report formats, not a hand-maintained page.
   The committed artifacts are generator code, template logic, and stylesheet.
3. **Static standalone HTML generation from structured repository sources** —
   YAML, JSON, CSV, and committed Markdown already in the repository, plus
   local `git` metadata. Structured sources only.
4. **An optional local server, authorized only when bound to the loopback
   interface, `127.0.0.1`**, serving the same render. **Binding to `0.0.0.0`,
   a LAN address, or any other externally reachable interface is not
   authorized** — not as a default, not as an option, and not as a
   configurable setting. Loopback is the boundary of the grant, not a
   preference within it. GET-only; mutating HTTP methods rejected.
5. **Read-only presentation of repository truth.** The capability derives no
   new portfolio fact, reuses existing production functions through their
   public API rather than duplicating governed calculations, and writes no
   authoritative file.
6. **Provenance display** — source git commit, branch, dirty-worktree status,
   effective date of the underlying state, and per-input-file provenance
   (path plus content hash) shown on the rendered page.
7. **Prominent stale, missing, or incomplete-state warnings.** A gap is shown
   as a gap, never silently rendered as current — the same discipline
   `OPS-0005` §2/§4 already binds the Phase Two status layer to.
8. **Disclosure or abstention when current allocation truth is unavailable.**
   Where live market data, a reconciled book, or any other precondition for a
   current allocation statement is absent, the capability states that it is
   unavailable and why. It never fabricates, estimates, or back-fills a
   missing measurement to complete a view.
9. **Historical HTML is archive evidence only, never operational input.**
   Retained historical HTML (e.g. under `governance/evidence/`) may be linked
   as an evidence disclosure and must never be parsed, scraped, embedded, or
   read as current state.
10. **Generated output is reproducible and non-authoritative.** The render is
    deterministic given identical repository state, apart from explicitly
    disclosed generation-time metadata; the generated file is disposable and
    is never a source of truth for anything.
11. **Focused tests** covering, at minimum: safety boundaries (no order path,
    no mutation control, loopback-only bind, mutating-method rejection),
    provenance, stale/missing/incomplete-state behavior, accessibility,
    fully offline operation with no external asset dependency, and
    historical-HTML isolation (an explicit test proving no historical HTML is
    read as operational input).
12. **One future bounded implementation PR** — **PR #199 is eligible to be
    that PR** — subject in full to independent exact-head review and explicit
    principal acceptance under §8.

### 3. Permitted implementation scope — exactly one implementation PR

Authorizes **exactly one** implementation pull request, so no later session
may invent additional PRs or phases under this authorization. That one PR may
contain, and nothing else:

1. One dashboard package under a single directory (name decided at
   implementation time following existing convention), containing the
   canonical generator, its view-model, provenance, rendering, optional
   loopback server, CLI entry point, and committed stylesheet source.
2. Its dedicated test module.
3. Usage and design documentation for the capability under `docs/`.
4. The minimal `.gitignore` addition required to keep generated output
   untracked.
5. The ordinary `operations/WORKSTREAMS.yaml` register synchronization
   recording that PR's merge.

**Generated HTML must never be committed.** The single generated artifact the
`build` path may write is untracked and disposable; the `serve` path writes
nothing.

### 4. Mandatory boundaries

The implementation must remain, at all times: advisory; display-only;
read-only; additive; outside `allocate.py`'s calculation path; outside margin
research; and outside the default daily workflow (`run_portfolio_check.sh` or
its successor) until separately authorized.

**Dependency direction (binding, testable):** the dashboard may *read from*
the already-computed public outputs of `allocate.py`, `margin_state.py`,
`intelligence_report.py`, and the `freshness_*` modules — one-directional,
forward only. Those modules, every `intelligence/` production path, and every
`freshness_*` module must **never** import, read, or otherwise depend on the
dashboard package. Any function called on an existing module must be that
module's public API — the same reuse-not-reimplement discipline `PI-0011`
established and `OPS-0005` §4 restated.

### 5. Prohibited scope

The authorized capability, and the implementation PR delivering it, must not:

- create any brokerage connection;
- perform any Robinhood or Alpaca execution;
- create or submit an order, or contain any order path whatsoever;
- mutate `holdings.yaml`, `targets.yaml`, any gate, any accepted decision,
  or `operations/WORKSTREAMS.yaml` from the user interface, by any means;
- grant browser-side portfolio authority — no client-side state that any part
  of the system treats as truth;
- constitute a second allocator;
- duplicate any governed portfolio calculation (tier, target, cap, gate,
  trim, buffer, or leverage logic) in the generator, template, or JavaScript;
- depend on external analytics or any required CDN, remote font, remote
  stylesheet, remote script, or network call of any kind;
- bind its optional server to anything other than the loopback interface
  `127.0.0.1` — `0.0.0.0`, a LAN address, and every other externally reachable
  interface are outside this grant entirely, whether offered as a default, an
  option, a flag, or a configurable setting (§2.4);
- treat generated HTML as repository authority;
- parse historical HTML as current state;
- fabricate a missing measurement;
- silently hide stale or incomplete repository truth;
- automatically change investment policy, by any mechanism; or
- be merged, marked ready, or treated as approved **solely because this
  authorization decision is filed** (§8, §9).

### 6. Relationship to WS-0002/`OPS-0005` and WS-0003 — no rewriting

- **`OPS-0005` is not superseded, narrowed, or reinterpreted.** Its Phase Two
  grant remains exactly as filed: one read-only, **stdout-only** status layer
  with no generated report file, gated on Fable Audit Gate #2 and principal
  acceptance. This decision authorizes a **different, separately scoped**
  capability under its own authority; it does not expand `OPS-0005`'s grant,
  does not satisfy `OPS-0005`'s gate, and does not permit the Phase Two PR to
  produce an HTML artifact. `OPS-0005` §3's own carve-out ("nothing prevents a
  future decision from adding one if a real need is demonstrated") is the
  clause this decision acts under — a separate later decision, exactly as
  contemplated.
- **`WS-0003` is not activated, edited, rescoped, or superseded.** Its
  `status: proposed`, `authorized_scope: "none"`, `prohibited_scope`,
  dependency on WS-0002, and terminal acceptance milestone are all left
  byte-unchanged. Its prohibition binds work performed **under WS-0003**; per
  `OPS-0001`, the register originates no authority in either direction, so it
  neither authorizes nor forbids work authorized elsewhere. **The daily
  allocation-check user experience WS-0003 describes remains deferred and
  unauthorized** — and this decision's §5 disclosure-or-abstention requirement
  keeps the dashboard out of that territory by construction: it may not
  produce a current allocation conclusion where the truth for one is
  unavailable.
- **A new workstream, `WS-0007`, is created** for this capability (§7), so
  that WS-0003's broader future UX planning intent is preserved intact rather
  than quietly repurposed. `OPS-0006`'s and WS-0005's prohibitions on
  "WS-0002 Phase Two (or later) dashboard/status-layer implementation" and
  "WS-0003 changes" are equally unaffected — this work happens under neither
  workstream.

### 7. Workstream treatment

Authorizes one new `operations/WORKSTREAMS.yaml` entry, **`WS-0007` —
Repository-native Portfolio-HQ dashboard**, using only `OPS-0001`'s existing
schema and status vocabulary. No new field and no new status value is created.

Because this governance PR is **unmerged at filing time**, and because
`OPS-0001` forbids an AI session from self-authorizing a workstream to
`authorized` status, the entry is filed at **`status: proposed`**,
`priority: secondary` (WS-0005 retains the sole `priority: primary` slot, per
`OPS-0001`'s at-most-one-primary rule), with `authorized_scope` stated as
*conditional on this decision's merge*.

**The filed `WS-0007` entry records PR #200 — this governance PR — as the
active governance PR (`active_pr: 200`), for as long as this authorization
filing is live. Draft PR #199 is recorded separately, in the dedicated
candidate-implementation milestone, and remains explicitly unapproved.** The
register therefore does not treat PR #199 as the active authorized PR, and
`active_pr` is not to be repointed at it: `OPS-0001` reserves `active_branch`/
`active_pr` for currently-live work under this entry's own authority, which
until merge is this governance filing itself.

**Post-merge synchronization required** (one continuous step, performed
immediately by the merging session per `OPS-0009` §9): flip `WS-0007` to
`status: authorized`, record this decision's merge commit, and update
`last_verified_main_sha`/`last_verified_date`. That transition is a factual
recording of an accomplished merge, not a new authorization.

### 8. Review and merge gate — for both PRs, separately

**This governance PR** must remain in draft, gain its own independent
exact-head review from an eligible reviewer under `OPS-0007` §1, complete any
required bounded correction and exact-head re-review, and receive explicit
principal acceptance before it may be marked ready or merged. It does not mark
itself ready and does not authorize its own merge. Per `OPS-0009` §1 this is
**Lane G — full weight, never reduced.**

**The implementation PR** (PR #199, or a successor) requires, separately and
in addition:

- exact-head independent review by an eligible reviewer under `OPS-0007` §1,
  retained as a GitHub review thread or a `governance/audits/` artifact per
  that directory's convention;
- a bounded correction pass resolving every material finding — **including the
  four findings already reported against PR #199**, which this decision does
  not resolve and does not evaluate;
- an exact-head delta re-review, or a full exact-head re-review where any of
  `OPS-0009` §6's four delta conditions fails;
- scope verification that the merged diff matches §3's file list exactly;
- verification of §4's dependency direction in both directions;
- verification that allocator output is provably unchanged for identical
  inputs, with and without the dashboard package present;
- dedicated tests and exact-head CI passing;
- explicit principal acceptance at the exact final head; and
- immediate post-merge ancestry, scope, validator/test, and clean-`main`
  verification by the merging session (`OPS-0009` §9).

**This decision's merge is a necessary precondition for the implementation
PR's merge, never a substitute for any item above.**

### 9. Authority boundary — what this decision does not do

This decision does **not**:

- approve PR #199's exact code, its design, or any specific line of it — it
  authorizes a capability class and a bounded scope, and PR #199 is a
  candidate implementation that must still independently satisfy §3, §4, §5,
  and §8;
- resolve, evaluate, restate, or waive the four implementation findings
  reported against PR #199;
- manufacture, imply, or substitute for any independent review of this
  decision or of PR #199;
- authorize `PHQ-2026-02` implementation, or any work under it;
- reconcile `holdings.yaml`, or authorize any holdings sync;
- authorize any trade, order, or execution of any kind;
- activate any `PHQ-2026-01` gated name (SNPS, ICE, SPGI, WM, RKLB, TSLA,
  SPCX), whose dispositions are unchanged;
- change any target, tier, role, cluster, cap, or weight;
- change `allocate.py`, `margin_state.py`, margin policy, the 1.8x leverage
  cap, the 30% buffer floor, or any order behavior;
- change `OPS-0005`'s Phase Two grant, `WS-0002`, or `WS-0003`;
- authorize any WS-0005 milestone, research batch, or Intelligence content;
- integrate the dashboard into the default daily workflow — that requires its
  own separate future decision.

### 10. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/OPS-0011-repository-native-dashboard-capability-authorization.md`
   (this file).
2. `governance/decisions.yaml` (index: one new entry).
3. `operations/WORKSTREAMS.yaml` (one new `WS-0007` entry; **no existing entry
   is modified**).
4. `CLAUDE.md` (one Decisions Log entry recording this filing).

**No other file is touched.** No dashboard code, test, asset, generated
artifact, `holdings.yaml`, `targets.yaml`, allocator, margin, or Intelligence
file is created or modified, and PR #199's branch is not touched in any way.

### 11. Effectivity

- This decision becomes effective **only when its own governance pull request
  merges to `main`** — not when pushed, and not when opened as a draft.
- Frontmatter `status: Accepted` follows this repository's established filing
  convention (`OPS-0007`, `OPS-0009`, `PHQ-2026-01` were each committed with
  that status inside their own unmerged draft PRs), paired with this explicit
  effectivity clause. **It is not a claim that independent review or principal
  acceptance has occurred** — neither has, as of this filing.
- No dashboard implementation work is authorized before that merge, and the
  implementation PR may not merge until §8's separate gates complete against
  its own exact head.
- Completing this capability authorizes no further phase, no default-workflow
  integration, and no second interface.

## Rationale

**Why a new decision rather than stretching an existing one.** Every candidate
host fails on its own text, not on interpretation: `WS-0003` authorizes
nothing and says so; `OPS-0005` §3 expressly excludes a generated report file
from the only implementation authority WS-0002 holds; `OPS-0001` rejected a
generated dashboard for the register; `OPS-0006`/WS-0005 prohibit
dashboard/status-layer work outright. Reading any of them as covering this
capability would be exactly the "lower-authority source silently expanding
scope" failure `GOV-0002` and `OPS-0001` both exist to prevent. Two of those
decisions — `OPS-0001` and `OPS-0005` — anticipated this moment in terms and
left a future decision free to act. This is that decision.

**Why capability-class authorization, not diff approval.** This repository's
precedent authorizes a named, bounded module *before* it is built
(`PI-0002`, `PI-0011`, `AUTO-0002`, `AUTO-0003`, `OPS-0005` §3), and separates
that authorization from the implementation's own independent review
(`OPS-0007` §1, `OPS-0009` §2). Collapsing the two would let a filing that
never inspected the code confer merge authority on it — precisely the
provenance failure `OPS-0004` Finding FA-1 identified in a different form.
Keeping them separate is what allows this decision to close the authority gap
without touching PR #199's still-open review, correction, and acceptance
gates.

**Why the capability is constitutionally safe.** Constitution §1 permits a
decision-support advisor that computes recommendations for manual execution;
§4 prohibits standing *predictive* research layers — price targets, opportunity
maps, precomputed recommendations. A read-only render of facts the repository
already contains predicts nothing, scores nothing, and ranks nothing. The
disclosure-or-abstention requirement (§2.8) is what keeps it on that side of
the line: a surface that fabricated an allocation conclusion from incomplete
truth would be a new analysis layer, and is prohibited by §5.

**Why a new workstream rather than activating WS-0003.** WS-0003's objective is
the *daily allocation-check experience*, gated behind WS-0002 determining what
information is economically meaningful — a question WS-0002 has not answered,
since its own Phase Two implementation has not begun. The dashboard is a
different deliverable: it explicitly abstains from producing an allocation
conclusion. Activating WS-0003 for it would rewrite the recorded meaning of a
`proposed` planning intent to fit work it never described, which `OPS-0001`
and `OPS-0006` §16.4 both forbid. A new entry keeps both records honest.

**Why `status: proposed` for `WS-0007` at filing time.** `OPS-0001` states that
an AI session may never self-authorize a workstream to `authorized` — that
transition requires durable accepted governance authority. This decision is
not yet merged, so that authority does not yet exist. Filing at `proposed`
with the post-merge synchronization named explicitly (§7) is the only form
that stays factually accurate while this PR is still a draft.

## Alternatives Considered

- **Activate `WS-0003` with a narrowly bounded authorized scope.** Rejected —
  WS-0003 is a recorded planning intent for the daily allocation-check UX,
  dependent on a WS-0002 conclusion that does not exist. Narrowing it to the
  dashboard would either silently rewrite what WS-0003 means or leave a
  workstream whose scope and title no longer match. Preserving it as broader
  future UX planning, and creating `WS-0007`, keeps prior history intact —
  the treatment `OPS-0001`'s own "not silently rewritten" rule points to.
- **Amend `OPS-0005` to permit a generated HTML artifact under WS-0002 Phase
  Two.** Rejected — `governance/decisions/README.md` forbids editing accepted
  substance, and `OPS-0005`'s stdout-only design was a deliberate choice with
  its own stated rationale (no second artifact to drift). A separate decision
  for a separate capability is the correct instrument, and `OPS-0005` itself
  named it.
- **Approve PR #199's implementation in this same decision, since its CI
  passes and its design note is detailed.** Rejected — explicitly out of scope
  per the principal's instruction, and inconsistent with `OPS-0007` §1 /
  `OPS-0009` §2: a passing CI run is not an independent review, and this
  session did not review that code. Four findings against it are reported and
  unresolved.
- **File a retained artifact under `governance/audits/` recording the review
  finding that prompted this decision.** Rejected — that directory holds
  *independent* reviews retained verbatim from the reviewing session's own
  output. This session authored this filing and did not perform that review;
  filing an authored summary there would create precisely the unattributable
  provenance `OPS-0004` Finding FA-1 exists to prevent. The authority-gap
  analysis lives in this decision's Context and Rationale instead, with the
  review's provenance disclosed as second-hand and unverified.
- **Authorize a broader "presentation and reporting layer" capability class.**
  Rejected — over-broad by the same reasoning `OPS-0005` used to cap itself at
  one PR and `MARGIN-0005` used to cap its trials: one generator, one
  interface, one implementation PR, enumerated file list. A future need for a
  second surface is a future decision.
- **Wait for PR #199's four findings to be resolved before filing this
  authorization.** Rejected — the authority gap is independent of the code's
  quality and blocks the implementation regardless of how those findings are
  resolved. Closing it first lets the correction pass proceed against a known,
  bounded, authorized scope rather than an unbounded one.
- **Do nothing and close PR #199 as unauthorized.** Rejected — nothing in the
  Constitution or any accepted decision prohibits a read-only presentation
  surface; the capability is unauthorized, not disallowed, and the principal
  has directed that the gap be closed rather than the capability abandoned.

## Consequences

**Authorized, effective on this decision's merge:** one repository-native,
read-only Portfolio-HQ dashboard capability as scoped in §2, delivered through
exactly one bounded implementation PR as scoped in §3, under the mandatory
boundaries in §4 and the prohibitions in §5; and one new `WS-0007` register
entry, transitioning from `proposed` to `authorized` in the immediate
post-merge synchronization described in §7.

**Unchanged by this decision:** `OPS-0001` through `OPS-0010` in full,
unedited — including `OPS-0005`'s stdout-only Phase Two grant and its Fable
Audit Gate #2; `WS-0002`, `WS-0003`, `WS-0004`, `WS-0005`, and `WS-0006` in
full; every tier, target, role, cluster, cap, and holding in `targets.yaml`
and `holdings.yaml`; `allocate.py`, `margin_state.py`, every Intelligence
record and validator, and every existing test; the 1.8x leverage cap and 30%
buffer floor; `MARGIN-0005`'s charter and trial ceiling; `PHQ-2026-01`'s
approved architecture, its seven gated names, and its still-unimplemented
target/allocator design note; and `OPS-0006`'s Milestone 4-9 boundary.

**PR #199 is untouched by this filing** — its state (open, draft, unmerged,
head `4f9f6d0633d1be3107a6a6922abc25518b6ece26`, zero GitHub reviews) is
exactly as found at preflight. It remains an unapproved candidate
implementation, gated on its own independent exact-head review, resolution of
its four reported findings, exact-head re-review, explicit principal
acceptance, and post-merge verification (§8) — none of which this decision
performs, shortens, or waives.

**No trade, order, holdings reconciliation, gated-name activation, target
change, allocator change, margin change, or `PHQ-2026-02` work is authorized
or implied.** The next concrete step is this governance PR's own independent
exact-head review, per §8 — not implementation, not correction of PR #199, and
not merge.
