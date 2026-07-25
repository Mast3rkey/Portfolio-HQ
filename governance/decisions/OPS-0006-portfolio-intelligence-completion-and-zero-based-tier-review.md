---
decision_id: OPS-0006
date: 2026-07-25
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0003, OPS-0004, OPS-0005, GOV-0001, GOV-0002, GOV-0003, PI-0001, PI-0006, PI-0011, PI-0016, ONTO-0001, TGT-0001, NUM-0001]
supporting_artifact: operations/WORKSTREAMS.yaml
---

## Context

`OPS-0001` recorded three durable planning intents without scoping or authorizing any of
them — WS-0002 (unified core architecture and optimization audit), WS-0003 (daily
allocation-check UX, dependent on WS-0002), and WS-0004 (guardrail-calibration research,
dependent on WS-0001 reaching a stopping point). `OPS-0002`/`OPS-0003`/`OPS-0004`/`OPS-0005`
then scoped, audited, reactivated, and reconciled WS-0002 in successive narrow steps, most
recently `OPS-0005` (PR #149, merged at `536e71f58857f2e55d98169b2e829e392c27a016`), which
reactivated WS-0002 for exactly one bounded slice: a read-only, stdout-only status/report
layer displaying facts `allocate.py`, `margin_state.py`, `intelligence_report.py`, and the
`freshness_*` modules already compute. No implementation PR for that slice exists yet.

None of WS-0001 through WS-0004 has ever had, as its governing purpose, understanding the
portfolio's ~65 holdings and crypto sleeve as one connected economic system from first
principles, independent of the tier/target/role labels already assigned to them. The closest
prior attempt — the 2026-07-19 "T1 AI-infra cluster cap: scanned and declined" entry in
CLAUDE.md's Decisions Log — found T1 42.1% of book against a 30.15% target, the 7-name
AI-infrastructure subset alone at 31.2%, and explicitly named the root cause as structural
("T1 and T2 have no trim rule at all... That's a bigger doctrine question... flagged, not
implemented same-session"). The follow-up `t1t2_trim_backtest.md`/CLAUDE.md entry closed only
the *return* question for a mechanical T1/T2 ceiling and explicitly left the concentration's
*capital-impairment* question open, calling it "a separate, still-open judgment." Company and
Theme Intelligence (`PI-0001` through `PI-0022`) now covers seven companies (COST, GEV, ISRG,
NVDA, TMO, TSM, XOM) and two themes (`ai_infrastructure`, `life_sciences_tools_medtech`) out of
roughly sixty-five governed equity/ETF holdings plus the crypto sleeve — each record produced
through its own separately authorized, bounded, one-company-at-a-time pilot under `PI-0016`'s
standing methodology. No workstream or decision anywhere treats *completing* that coverage,
*mapping* how covered and uncovered holdings relate to each other economically, and *revisiting
the tier architecture itself from evidence rather than from the labels already assigned* as one
connected, sequenced body of work with its own governing purpose.

The principal has explicitly authorized establishing exactly that workstream now, as a
governance-only filing: no research performed, no code implemented, no holdings, targets,
tiers, allocation rules, margin rules, or Intelligence behavior changed. This decision is that
filing.

Separately, `OPS-0005`'s independent Fable review (review `4779232640`, delta reviews
`4779242761`/`4779247070`) closed its one blocking finding (F-1) before merge but left two
non-blocking findings open for the ordinary first post-merge register sync: **F-2** —
`operations/WORKSTREAMS.yaml`'s WS-0002 `authorized_by` field read "this session" with no
session identifier, weaker attribution than `OPS-0003`'s own entry ("session dcblbf,
2026-07-24") or `OPS-0004`'s retained-artifact discipline; the PR's own commit trailers and
the review's provenance disclosure identify the authoring session as `session_01RwQaRKJASFVViAP2nbVA73`.
**F-3** — WS-0002's `active_branch`/`active_pr: 149` and its `phase-two-reactivation-authorized`
milestone (`status: drafted`) were accurate at PR #149's pre-merge head but become stale by
construction the instant it merges, per `OPS-0001`'s own rule that these fields "hold only
currently-live work" and that "a merged historical PR belongs under `milestones` or
`evidence_refs`, never in these two fields" — the same self-staling pattern `OPS-0003` already
resolved for WS-0002 after PR #143 merged. PR #149 is now confirmed merged
(`mcp__github__pull_request_read`: `merged: true`, `merged_at: 2026-07-25T12:28:19Z`, merge
commit `536e71f58857f2e55d98169b2e829e392c27a016`, matching `origin/main`'s current tip exactly).
Both findings are non-blocking and were explicitly deferred to "the ordinary first post-merge
register sync" — this filing is that sync, reconciling only F-2 and F-3, exactly as those
reviews anticipated. Neither finding touches `OPS-0005`'s substance; its accepted text is not
reopened, edited, or superseded by this reconciliation.

## Decision

### 1. New primary workstream established — WS-0005

`operations/WORKSTREAMS.yaml` gains a new entry, **WS-0005 — Portfolio Intelligence
Completion, Relationship Mapping, and Zero-Based Tier Architecture Review**, `status:
authorized`, `priority: primary`. Its governing purpose, stated exactly:

> Understand every asset from first principles, understand how the assets interact, and use
> that evidence to design the simplest defensible portfolio-role, capital-priority, tier,
> target, and review framework.

WS-0005 is distinct from, and does not duplicate, any existing workstream: WS-0002 (as
reactivated by `OPS-0005`) is a *read-only status/report layer* displaying facts already
computed by existing components — it answers "what does the system currently compute,"
not "is what it computes the right thing to compute." WS-0003 is deferred UX work contingent
on WS-0002. WS-0004 is a narrow, still-dormant research question about exactly two numeric
guardrails (the 1.8x leverage cap, the 30% buffer floor) — WS-0005 does not touch either
number and is not a backdoor into WS-0004's scope. WS-0005 is the first workstream whose
governing purpose is understanding the portfolio's economic structure and the tier
architecture built on top of it, from evidence rather than from the labels already assigned.

### 2. Existing policy stays authoritative; not presumed correct during research

Existing tiers, targets, roles, caps, and position sizes (`targets.yaml`, `holdings.yaml`,
every accepted governance decision, the Constitution, and CLAUDE.md's current parameters)
**remain the current operating policy in full force** until formally superseded through their
own governed procedure — nothing in WS-0005 changes, suspends, or conditions any of them.
Simultaneously, and without contradiction: **existing policy must not be treated as
presumptively correct evidence during WS-0005's own research process.** A holding's current
tier, target weight, or "core" label is a policy fact to be recorded and later reconciled
against (§3 below) — it is never itself a reason a research conclusion agrees with that
policy. This mirrors, at the portfolio-architecture level, the same discipline `PI-0016`
already applies at the single-company level (a standing review methodology that evaluates a
company on its own evidence, not on its existing roster placement) and the same evidentiary
posture `GOV-0003` established for margin-timing research (permission to question a fixed
posture's evidence base without permission to act on a mere hunch).

### 3. Zero-based / blinded-review protocol

Any future WS-0005 research (once separately authorized per §5) must follow this protocol:

- **Sealed historical baseline.** Before any first-principles research begins on a given
  asset or on the portfolio's structure, the current governed tier, target, role, cluster,
  cap, and applicable policy for every in-scope holding is captured verbatim from
  `targets.yaml`/`holdings.yaml`/CLAUDE.md/`governance/decisions/` into a dated baseline
  record, sealed and set aside — not consulted again until reconciliation (below).
- **Research from first principles.** Each asset is researched on its own economic merits —
  what it does, how it makes money, its competitive position, its risks — independent of
  where it currently sits in the tier structure.
- **Conclusions before comparison.** Initial company-level and portfolio-level conclusions
  (proposed economic role, relationship map, candidate classification) are formed and
  recorded **before** the sealed baseline is reopened.
- **Unblind only at reconciliation.** The baseline is unsealed only at the dedicated
  reconciliation milestone (§4, Milestone 7) — never earlier, and never partially.
- **Explicit agreement/disagreement record.** Reconciliation states, for every holding where
  the researched conclusion and the current policy diverge, both positions side by side —
  agreement is recorded as explicitly as disagreement, not left implicit.
- **No silent inheritance.** An old classification, tier, or "core" label is never carried
  into a proposed framework merely because it already exists — every proposed classification
  must trace to evidence gathered under the blind protocol, or be explicitly and separately
  justified as unchanged.

### 4. Roadmap — nine sequential milestones (scope ceiling, not a grant to execute)

The following milestones define the **maximum future scope** WS-0005 may ever cover. Naming
them here authorizes **none of their execution** — see §5. Each is recorded in
`operations/WORKSTREAMS.yaml` at `status: proposed`, `pr: null`.

1. **Baseline and inventory.** Inventory every currently governed holding and asset type;
   capture current tier/target/role/cluster/cap/applicable policy; record the baseline
   separately from any blind research conclusion; identify missing, duplicated, ambiguous, or
   stale records.
2. **Intelligence coverage and freshness audit.** For every equity, ETF, crypto asset, cash
   position, hedge, or other governed asset: Intelligence coverage present/missing, freshness,
   evidence quality, missing primary-source research, required review priority, and explicit
   inability-to-conclude where evidence is insufficient.
3. **Intelligence completion.** Bounded, research-only PRs completing or refreshing records in
   coherent batches, each addressing (when applicable): what the business does; why it may
   deserve a portfolio role; economic function; moat/competitive position; financial quality;
   management and capital allocation; growth drivers; key customers/suppliers/partners/
   competitors; major risks; thesis-break conditions; replacement candidates; opportunity
   cost; what exposure disappears if the asset is removed. Advisory only — cannot change
   policy.
4. **Portfolio relationship mapping.** Economic systems; common demand drivers; customer/
   supplier dependencies; direct competition; complementary relationships; duplicated
   exposure; shared geopolitical/interest-rate/commodity/regulatory/technology-cycle/
   liquidity risk; correlated thesis failure; missing portfolio functions; next-best
   alternatives. Structural/economic overlap is kept explicitly distinct from measured
   historical price correlation (the existing `caps.clusters` mechanism) — the two are never
   combined into a single unsupported score.
5. **Zero-based classification and tier-architecture review.** What questions the current
   tier system answers; where it mixes unrelated concepts; whether one tier label is
   adequate; the smallest set of candidate frameworks the evidence supports; candidate
   separation, where useful and not required merely because listed, of economic role,
   business quality, thesis uncertainty, capital priority, position boundaries, overlap
   constraints, and review cadence; rejection of unnecessary complexity; no single mechanical
   conviction score substituting for judgment.
6. **Blind classification.** Apply the candidate framework(s) without using current tiers or
   targets as desired answers. No repository policy mutation.
7. **Baseline reconciliation.** Unblind the sealed baseline (§3) and compare current-vs-
   researched role, tier-vs-proposed capital priority, target-vs-evidence-supported range,
   cluster-vs-relationship-map, caps-vs-portfolio-level risk, and review cadence-vs-thesis
   uncertainty. Every proposed difference states evidence, reasoning, uncertainty, opportunity
   cost, controlling policy, and required governance action.
8. **Policy recommendation package.** Advisory recommendations only, covering portfolio roles,
   tier/replacement classification architecture, capital-priority rules, targets/target
   ranges, maximum position sizes, economic-system/overlap limits, monitoring frequency,
   thesis-break review rules, and add/hold/trim/exit-review discipline.
9. **Independent review and later adoption.** Independent Fable review of research coverage,
   relationship methodology, zero-based protocol adherence, candidate tier architecture, the
   policy recommendation package, evidence-versus-judgment separation, and absence of hidden
   scoring or allocator coupling. Any adoption requires its own separate accepted governance
   decision and a later, separately authorized implementation PR.

### 5. This filing authorizes documentation and framework only

**This decision authorizes exactly: the existence of WS-0005, its governing purpose, the §3
protocol, and the §4 roadmap as a scope ceiling.** It authorizes **zero milestone execution** —
including Milestone 1's baseline capture. No research has been performed, no Intelligence
record has been created or modified, no company or theme has been selected for review, no
inventory has been produced, and no code has been written under this filing. Every future
milestone — Milestone 1 included — requires its own separate, later, explicit principal
authorization and its own bounded implementation or research PR before any work begins,
following exactly the discipline `PI-0016` already established for single-company reviews
("every future company review still requires its own separate, filed, repository-auditable
research authorization... informal chat sign-off does not suffice") and `MARGIN-0005`'s own
charter-then-gate structure (a charter names a bounded program; each stage inside it still
requires its own review before advancing). **No later phase becomes authorized merely because
an earlier milestone is complete** — closing Milestone 1 does not itself open Milestone 2, and
so on through Milestone 9.

### 6. Explicit prohibitions

This decision does not authorize, and no future WS-0005 milestone may be read to authorize
without its own separate governance decision naming it explicitly:

- changing current tiers, targets, target ranges, or holdings;
- buying, selling, or placing any order;
- modifying allocation formulas or recommendations;
- creating a computed conviction score that controls capital;
- automatic ranking or aggregation that determines policy;
- Intelligence directly controlling targets, tiers, buys, trims, margin, or allocator output;
- modifying margin governance (the 1.8x leverage cap and 30% buffer floor are unchanged and
  outside this filing's scope entirely);
- any `MARGIN-0005` S3 trial, simulation, or research execution;
- WS-0002 Phase Two (or any later phase) dashboard/status-layer implementation;
- WS-0003 or any default-daily-workflow change;
- production coupling between Intelligence and the allocator;
- any generated report replacing an authoritative file (`targets.yaml`/`holdings.yaml`/
  CLAUDE.md remain sole authority throughout);
- unrelated cleanup.

### 7. Priority and sequencing

1. **WS-0005 becomes the sole `priority: primary` workstream**, per `OPS-0001`'s at-most-one-
   primary rule.
2. **WS-0001 moves to `priority: secondary`.** This is a sequencing action only, identical in
   kind to `OPS-0002` item 3's prior WS-0001 sequencing hold — every existing
   `governing_authority`, `authorized_scope`, `prohibited_scope`, milestone record,
   `evidence_refs`, and `completion_criteria` is preserved exactly, unchanged. **No S3
   authorization is granted, withdrawn, or altered by this reordering** — WS-0001's S3 gate
   remains exactly as unauthorized and deferred as it already was; this decision does not
   reach it.
3. **WS-0002 remains `priority: secondary`, `status: authorized`, unchanged in substance.**
   `OPS-0005`'s Phase Two grant is not narrowed, withdrawn, or accelerated — the single bounded
   implementation PR it authorizes may still be opened at any time under its own terms; this
   decision does not require it to wait for WS-0005, only records that WS-0005, not WS-0002,
   is now the primary workstream.
4. **Portfolio understanding (WS-0005) precedes**, as a sequencing preference rather than a
   withdrawal of any existing authority: final tier design, target changes, unlevered
   portfolio stress testing, monitoring/sell-discipline adoption, and any margin-research or
   margin-policy reconsideration (WS-0004, still dormant and still contingent on its own
   separate future research charter).
5. **No later WS-0005 phase becomes authorized merely because an earlier milestone
   completes** — restated from §5, because it governs sequencing as much as authorization.

### 8. PR #149 / WS-0002 operational reconciliation (F-2, F-3)

Both findings are located in `operations/WORKSTREAMS.yaml`'s WS-0002 entry (verified directly
from PR #149's retained review comments — `mcp__github__pull_request_read`, reviews
`4779232640`/`4779242761`/`4779247070` — not assumed):

- **PR #149 recorded merged.** `merged_at: 2026-07-25T12:28:19Z`, merge commit
  `536e71f58857f2e55d98169b2e829e392c27a016` (confirmed identical to `origin/main`'s current
  tip). The `phase-two-reactivation-authorized` milestone's `status` moves from `drafted` to
  `merged`, `date` updated to `2026-07-25`.
- **F-3 — stale active-work fields cleared.** `active_branch` and `active_pr` move to `null`
  (PR #149 is merged, not live), per `OPS-0001`'s rule that these fields hold only currently-
  live work — the identical correction `OPS-0003` already made for WS-0002 after PR #143
  merged.
- **F-2 — attribution strengthened.** `authorized_by` is corrected from the unattributed
  "this session" to name the authoring session identifier
  (`session_01RwQaRKJASFVViAP2nbVA73`, per PR #149's commit trailers and review
  `4779242761`'s provenance disclosure) alongside the existing durable-authority citation
  (`OPS-0005`), matching `OPS-0003`'s own attribution pattern.
- **`last_verified_main_sha`/`last_verified_date` refreshed** to `origin/main`'s current tip
  and today's date, reflecting this filing's own preflight verification.
- **Nothing else about the WS-0002 entry changes** — `status: authorized`, `priority:
  secondary`, `authorized_scope`, `prohibited_scope`, other milestones, `evidence_refs`,
  `next_action`, `completion_criteria`, and `blocker` are all preserved verbatim.
- **`OPS-0005`'s accepted decision text is not reopened, edited, or superseded** by this
  reconciliation — only the operational register fields it always anticipated would need an
  ordinary post-merge sync (its own §6: "Any integration... requires its own separate future
  governance decision," and `OPS-0001`'s pre-existing active-field rule) are updated. This
  mirrors exactly how `OPS-0003` reconciled WS-0002's fields after PR #143 merged without
  reopening `OPS-0002`.

## Rationale

This follows the same charter-then-gate discipline `MARGIN-0005` established for margin
research and `PI-0016` established for single-company review: name the governing purpose,
the evidentiary protocol, and the full roadmap up front so a future session cannot invent
scope, while gating every actual unit of work — including the first, lowest-risk one — behind
its own separate authorization. The zero-based/blinded protocol (§3) is the direct portfolio-
architecture-level application of the same discipline `PI-0016`'s standing methodology already
applies per company (evaluate on evidence, not on existing placement) and the same posture
`GOV-0003` used to open bounded margin-timing research without granting any conclusion in
advance. Treating existing policy as authoritative-but-not-presumptively-correct (§2) resolves
what could otherwise read as a contradiction: `GOV-0002`'s precedence hierarchy makes
`targets.yaml` and accepted decisions controlling for *operation*, while `PI-0016`/`GOV-0003`
already establish that a *research* process may question the evidence behind a controlling
policy without thereby weakening its operational authority — WS-0005 states this distinction
explicitly rather than leaving it implicit. Naming WS-0005 primary and WS-0001 secondary (§7)
is a pure sequencing act, identical in kind and reversibility to `OPS-0002` item 3's prior
WS-0001 hold and `OPS-0003`'s subsequent restoration — it changes priority, not authority,
exactly as `OPS-0001`'s at-most-one-primary rule requires when a new primary workstream is
created. Reconciling F-2/F-3 in this same filing, rather than a separate one, follows
`OPS-0004`'s own precedent of folding a narrow, previously-flagged register correction into the
next filing that touches the same file, rather than leaving a known non-blocking finding open
indefinitely.

## Alternatives Considered

- **Authorize Milestone 1 (baseline capture) to begin immediately, since it is read-only
  inventory with no judgment involved.** Rejected — the task authorizing this filing states
  plainly "do not perform the research in this session," and `PI-0016`'s own discipline treats
  "informal... sign-off" as insufficient for any future company-level work; extending that same
  caution to the first portfolio-level milestone is the more conservative and more consistent
  reading. Nothing prevents a fast, narrowly-scoped follow-on authorization for Milestone 1
  specifically.
- **Fold WS-0005 into WS-0002 as a new phase, rather than a separate workstream.** Rejected —
  WS-0002 (as reactivated by `OPS-0005`) is scoped narrowly and specifically to a read-only
  status/report *display* layer; its governing question is "what does the system currently
  compute," not "is what it computes the right thing to compute or organize." Conflating the
  two would either narrow WS-0005's actual purpose to fit WS-0002's existing bounded grant, or
  silently expand WS-0002 beyond what `OPS-0005` authorized — both worse than a clearly
  separate workstream with its own governing purpose.
- **Leave WS-0001 at `priority: primary` and make WS-0005 `priority: secondary`.** Rejected —
  the principal's authorization explicitly states the new workstream becomes primary; `OPS-
  0001`'s at-most-one-primary rule means one of the two must move, and WS-0001's own research
  substance, milestones, and evidence are completely unaffected by a priority change, exactly
  as they were through the OPS-0002→OPS-0003 primary/secondary cycle already recorded in this
  log.
- **Treat this filing as also authorizing a first real company or theme review under the new
  workstream, to give it concrete momentum.** Rejected — explicitly out of scope; the task
  authorizing this filing is governance-only, and `PI-0016`'s standing methodology already
  requires any such review to name its own subject and rationale in its own future filing.
- **Reopen and edit `OPS-0005`'s accepted text to fold in the F-2/F-3 correction, rather than
  reconciling only the register.** Rejected — `OPS-0005` is `status: Accepted`; per
  `governance/decisions/README.md`, substance is not edited after acceptance, and neither
  finding touches `OPS-0005`'s granted authority, scope, or supersession language — only two
  register fields both reviews explicitly deferred to "the ordinary first post-merge register
  sync."
- **Add a fifth file (a dedicated blueprint document) for the roadmap and protocol, mirroring
  `docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md`.** Rejected for this filing — unlike
  WS-0002's architecture (which needed a long-form blueprint precisely because it described a
  three-layer runtime architecture with implementation-relevant detail), WS-0005's roadmap and
  protocol are governance policy statements, not implementation specifications, and fit
  entirely within this decision file's own sections at a length consistent with `OPS-0002`/
  `OPS-0005` themselves. A future milestone-specific authorization may introduce its own
  supporting document if that milestone's scope justifies one; none is required to establish
  the workstream itself.

## Consequences

Going forward: WS-0005 exists as the sole `priority: primary` workstream, with a governing
purpose, a zero-based/blinded-review protocol, and a nine-milestone roadmap recorded as a
scope ceiling — no milestone, including the first, is authorized to execute by this filing.
WS-0001 moves to `priority: secondary` with its MARGIN-0005 research authority, milestones,
and S3 gate completely unchanged. WS-0002 remains `priority: secondary`, `status: authorized`,
with `OPS-0005`'s Phase Two grant fully intact and un-narrowed. WS-0003 and WS-0004 are
untouched. `operations/WORKSTREAMS.yaml`'s WS-0002 entry is synchronized to live GitHub truth
(PR #149 merged, `active_branch`/`active_pr` cleared, milestone status corrected, attribution
strengthened) without reopening `OPS-0005`'s accepted text. No allocator, `targets.yaml`,
`holdings.yaml`, margin rule, Company/Theme Intelligence record, or production code is touched
by this decision. This decision and the corresponding `operations/WORKSTREAMS.yaml`
synchronization become effective only when this exact implementing pull request merges to
`main` — not when pushed, and not merely when opened as a draft. The next concrete step is
principal review of this draft PR — not research, not implementation, and not merge.
