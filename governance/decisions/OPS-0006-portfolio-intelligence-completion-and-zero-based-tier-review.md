---
decision_id: OPS-0006
date: 2026-07-25
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0003, OPS-0004, OPS-0005, GOV-0001, GOV-0002, GOV-0003, PI-0001, PI-0006, PI-0011, PI-0016, ONTO-0001, TGT-0001, NUM-0001, MARGIN-0001, MARGIN-0003, MARGIN-0004, MARGIN-0005]
supporting_artifact: operations/WORKSTREAMS.yaml
---

_**Amendment — 2026-07-25 (same-day, pre-merge, pre-review):** the initial version of this
decision authorized WS-0005's existence, governing purpose, protocol, and nine-milestone
roadmap, but authorized **zero** milestone execution — including Milestone 1's baseline
capture. On review before any independent audit occurred (confirmed: PR #150 carries zero
GitHub reviews at the time of this amendment), the principal identified two scope problems:
(1) the roadmap did not explicitly require future Intelligence and relationship research to
preserve evidence that may later matter to margin/leverage-risk analysis, and (2) authorizing
zero milestone execution would force a second governance decision immediately after this one
merges, merely to perform a read-only factual inventory and coverage audit — the safest
possible unit of work in the entire roadmap. This amendment corrects both, in place, per
`governance/decisions/README.md`'s narrow-correction convention and the same same-day,
pre-merge, pre-audit pattern `OPS-0002` already used for its own in-place correction ("no
independent audit has yet occurred against any version of this decision, so there is no
settled prior audit finding this correction could contradict"). Specifically, this amendment:
(a) authorizes exactly **Milestones 1 and 2** — baseline/inventory and Intelligence
coverage/freshness audit — as one bounded first audit PR, effective upon this decision's own
merge; (b) adds an explicit, clearly-separated margin-relevant-evidence requirement to the
still-unauthorized future Intelligence-completion milestone (3) and a portfolio-level
margin-preparation requirement to the still-unauthorized future relationship-mapping milestone
(4), each bounded by explicit non-authorization prohibitions; (c) clarifies the zero-based
protocol (§3) to state a policy discipline rather than an unenforceable literal-blindness
claim. Milestones 3 through 9 remain roadmap-only and unauthorized; nothing about WS-0005's
`priority: primary` status, WS-0001's secondary sequencing, WS-0002's unaffected `OPS-0005`
grant, or the F-2/F-3 register reconciliation changes. Every section below reflects the
amended, current state — the superseded zero-execution text is not reproduced verbatim here,
consistent with how `OPS-0002`'s own in-place correction was handled, since no independent
review of the prior text exists for a future reader to reconcile against._

_**Second amendment — 2026-07-25 (same-day, pre-merge, pre-review; PR #150 still carries zero
GitHub reviews at the time of this amendment):** adds new §9, "Zero-based future margin-policy
review," stating explicitly how WS-0005's zero-based principle (§2, §3) applies to the 1.8x
leverage cap and 30% buffer floor specifically — both remain binding operational guardrails
until formally superseded, while simultaneously being provisional, doctrine-status baseline
values (per `NUM-0001`) that a future, separately authorized margin study must not treat as
pre-defended assumptions or as constraints on which candidate policies it may examine on paper,
subject to the one stated exception already in Constitution §3: no live system may exceed or
disregard either value before a replacement policy is formally accepted and implemented. §9
authorizes no research, no `MARGIN-0005` S3 or successor study, no margin-policy recommendation,
and no change to either parameter — it restates and applies `GOV-0003`'s already-accepted
research-then-adopt discipline to WS-0005's specific framing, rather than creating a new path
to changing the cap or floor. Per `governance/decisions/README.md`'s narrow-correction
convention and the same same-day, pre-merge, pre-audit pattern used for the first amendment
above, this is made in place rather than by superseding filing._

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

This protocol is a **research discipline**, not a claim of literal information blindness the
repository can technically enforce — any session or reviewer that has done ordinary repository
preflight has already read `targets.yaml`, `holdings.yaml`, and CLAUDE.md's current parameters,
and cannot be made to forget them. The protocol's force comes from what it requires a
researcher to *do* with that unavoidable prior exposure, not from a pretense that the exposure
doesn't exist. Any future WS-0005 research (once separately authorized per §5) must follow it:

- **Baseline preserved as comparison, not as evidence.** Before any first-principles research
  begins on a given asset or on the portfolio's structure, the current governed tier, target,
  role, cluster, cap, and applicable policy for every in-scope holding is captured verbatim
  from `targets.yaml`/`holdings.yaml`/CLAUDE.md/`governance/decisions/` into a dated baseline
  record, kept **for later comparison only**. It must never be treated, during the research
  itself, as evidence, a desired answer, or a presumption of correctness — a holding's current
  label is a fact to reconcile against, never a reason a conclusion agrees with it.
- **Research from first principles.** Each asset is researched on its own economic merits —
  what it does, how it makes money, its competitive position, its risks — independent of
  where it currently sits in the tier structure.
- **Conclusions formed independently, before formal comparison.** Initial company-level and
  portfolio-level conclusions (proposed economic role, relationship map, candidate
  classification) are recorded on their own evidentiary merits **before** the dedicated
  reconciliation step below formally compares them against the preserved baseline — even
  though the researcher was never literally unaware the baseline existed.
- **Explicit comparison at reconciliation.** The formal current-vs-researched comparison
  happens only at the dedicated reconciliation milestone (§4, Milestone 7) — not earlier, and
  not partially — so that every holding's old and new conclusions are compared once, together,
  on the record, rather than piecemeal.
- **Explicit agreement/disagreement record.** Reconciliation states, for every holding where
  the researched conclusion and the current policy diverge, both positions side by side —
  agreement is recorded as explicitly as disagreement, not left implicit.
- **No silent inheritance.** An old classification, tier, or "core" label is never carried
  into a proposed framework merely because it already exists — every proposed classification
  must trace to evidence gathered under this protocol, or be explicitly and separately
  justified as unchanged.
- **Accepted history is not erased.** This protocol governs how *new* research conclusions
  are formed and compared — it does not delete, rewrite, or reinterpret any existing accepted
  governance decision, CLAUDE.md Decisions Log entry, or Company/Theme Intelligence record;
  every prior decision remains intact and citable exactly as `governance/decisions/README.md`
  already requires.

### 4. Roadmap — nine sequential milestones (scope ceiling; Milestones 1-2 authorized to execute, 3-9 are not)

The following milestones define the **maximum future scope** WS-0005 may ever cover. Naming
them here authorizes execution of **only Milestones 1 and 2** — see §5. Milestones 3 through 9
remain roadmap items only. Each is recorded in `operations/WORKSTREAMS.yaml`; Milestones 1-2 at
`status: authorized`, Milestones 3-9 at `status: proposed`, all `pr: null` (none has been
executed by this filing).

1. **Baseline and inventory** *(authorized — see §5)*. Enumerate every currently governed
   asset (every equity, ETF, band/spec name, and the crypto sleeve); identify asset type;
   capture the existing governed role, tier, target, cluster, cap, and relevant operating
   policy for each as a historical comparison baseline, per §3; preserve that policy without
   treating it as presumptively correct; identify missing, duplicated, ambiguous, or
   inconsistent asset records.
2. **Intelligence coverage and freshness audit** *(authorized — see §5)*. For every asset
   inventoried in Milestone 1: identify whether a Company/Theme Intelligence record exists;
   identify record type and the applicable schema section; record freshness and evidence
   quality; identify missing primary-source evidence; identify incomplete or stale research;
   identify assets for which no supportable conclusion can yet be reached; recommend the
   sequence of later Milestone-3 research batches. **This milestone must not complete or
   rewrite any company Intelligence record** — it audits coverage and freshness, it does not
   produce or edit content.
3. **Intelligence completion** *(not authorized)*. Bounded, research-only PRs completing or
   refreshing records in coherent batches, each addressing (when applicable): what the business
   does; why it may deserve a portfolio role; economic function; moat/competitive position;
   financial quality; management and capital allocation; growth drivers; key
   customers/suppliers/partners/competitors; major risks; thesis-break conditions; replacement
   candidates; opportunity cost; what exposure disappears if the asset is removed. Advisory
   only — cannot change policy.

   **Margin-relevant evidence requirement (clearly separated from the above).** For every
   asset, this future milestone's research must also capture applicable evidence that may
   later matter to margin or leverage-risk analysis: earnings and cash-flow cyclicality;
   operating and financial leverage; balance-sheet strength; refinancing and funding risk;
   sensitivity to interest rates, commodities, foreign exchange, regulation, economic activity,
   technology cycles, and capital-spending cycles; severe drawdown drivers; event and
   overnight-gap risk; liquidity and position-exit considerations; customer, supplier,
   counterparty, and jurisdiction concentration; speed and detectability of thesis
   deterioration; temporary impairment versus permanent thesis failure; relationships with
   other holdings that could cause simultaneous losses; and characteristics that could become
   materially more dangerous when financed with borrowed money. **This is advisory evidence for
   possible later margin research only.** It must not: recommend using margin; calculate a safe
   leverage level; rank assets for margin deployment; modify margin policy; modify allocator
   output; substitute for current broker maintenance requirements; substitute for account-level
   holdings or margin state; authorize `MARGIN-0005` S3; or consume a margin trial.
4. **Portfolio relationship mapping** *(not authorized)*. Economic systems; common demand
   drivers; customer/supplier dependencies; direct competition; complementary relationships;
   duplicated exposure; shared geopolitical/interest-rate/commodity/regulatory/
   technology-cycle/liquidity risk; correlated thesis failure; missing portfolio functions;
   next-best alternatives. Structural/economic overlap is kept explicitly distinct from
   measured historical price correlation (the existing `caps.clusters` mechanism) — the two are
   never combined into a single unsupported score.

   **Portfolio-level margin preparation (clearly separated from the above).** This future
   milestone must also require identification of: common drawdown drivers; stress-period
   concentration; simultaneous thesis-failure pathways; liquidity and gap-risk clusters;
   potentially prolonged recovery periods; economic exposures that appear diversified by ticker
   but are concentrated in substance; and portfolio losses that borrowing could amplify. It must
   require explicit separation among company-level risk, economic-system risk, portfolio-level
   risk, and margin-amplified risk. **This analysis must not be converted into a leverage
   recommendation** of any kind.

   **Future evidence register.** This future milestone must produce a clearly separated
   margin-relevance evidence register, for possible later use by an explicitly authorized
   `MARGIN-0005` S3 or successor study. The register is factual and advisory; it does not itself
   authorize a study; it does not consume a trial; it does not change current margin doctrine
   (the 1.8x leverage cap and 30% buffer floor are untouched throughout); and live broker and
   portfolio state must be sourced separately, fresh, at the time of any future study — the
   register is not a substitute for that live sync.
5. **Zero-based classification and tier-architecture review** *(not authorized)*. What
   questions the current tier system answers; where it mixes unrelated concepts; whether one
   tier label is adequate; the smallest set of candidate frameworks the evidence supports;
   candidate separation, where useful and not required merely because listed, of economic role,
   business quality, thesis uncertainty, capital priority, position boundaries, overlap
   constraints, and review cadence; rejection of unnecessary complexity; no single mechanical
   conviction score substituting for judgment.
6. **Blind classification** *(not authorized)*. Apply the candidate framework(s) without using
   current tiers or targets as desired answers, per §3. No repository policy mutation.
7. **Baseline reconciliation** *(not authorized)*. Formally compare the Milestone-1 baseline
   (§3) against current-vs-researched role, tier-vs-proposed capital priority,
   target-vs-evidence-supported range, cluster-vs-relationship-map, caps-vs-portfolio-level
   risk, and review cadence-vs-thesis uncertainty. Every proposed difference states evidence,
   reasoning, uncertainty, opportunity cost, controlling policy, and required governance
   action.
8. **Policy recommendation package** *(not authorized)*. Advisory recommendations only,
   covering portfolio roles, tier/replacement classification architecture, capital-priority
   rules, targets/target ranges, maximum position sizes, economic-system/overlap limits,
   monitoring frequency, thesis-break review rules, and add/hold/trim/exit-review discipline.
9. **Independent review and later adoption** *(not authorized)*. Independent Fable review of
   research coverage, relationship methodology, zero-based protocol adherence, candidate tier
   architecture, the policy recommendation package, evidence-versus-judgment separation, and
   absence of hidden scoring or allocator coupling. Any adoption requires its own separate
   accepted governance decision and a later, separately authorized implementation PR.

### 5. Authorization boundary — Milestones 1-2 authorized upon effectiveness; 3-9 remain roadmap only

**This decision authorizes: the existence of WS-0005, its governing purpose, the §3 protocol,
the §4 roadmap as a scope ceiling, and — as of this amendment — execution of exactly
Milestones 1 and 2**, effective the moment this decision's own implementing pull request
merges to `main` (§9, unchanged). No research has been performed and no code has been written
under this filing itself — this decision authorizes a later, separate implementation or
research PR to do that work; it does not do it here.

- **Milestones 1 and 2 are authorized upon OPS-0006 becoming effective.** No further governance
  decision is required to open that work.
- **They should normally be completed in one bounded audit PR**, since both are read-only
  factual inventory/audit work over the same asset list and naturally belong together — unless
  that implementation PR's own preflight demonstrates that combined scope is unsafe (for
  example, an asset count or evidence volume that makes one PR unreviewable), in which case it
  may split into two, still covering only Milestones 1 and 2, nothing more.
- **The first audit PR may create exactly one retained advisory audit artifact** (e.g. under
  `intelligence/reports/` or a comparable location matching existing repository convention) **and
  its dedicated tests or validators, only where repository convention requires them** — mirroring
  how `PI-0011`/`AUTO-0002` each added a narrow, single-purpose module with its own tests, not a
  general-purpose framework.
- **It must not complete or rewrite any company Intelligence record.** Milestone 2 audits
  coverage and freshness; it does not produce Milestone-3 content.
- **Milestones 3 through 9 remain roadmap items only.** Naming them in §4 authorizes none of
  their execution.
- **Completion of Milestones 1 and 2 does not automatically authorize Milestone 3.** Starting
  Intelligence-completion batches, relationship conclusions, tier redesign, policy
  recommendations, or adoption each requires its own separate, later, explicit principal
  authorization and its own bounded implementation or research PR — following exactly the
  discipline `PI-0016` already established for single-company reviews ("every future company
  review still requires its own separate, filed, repository-auditable research authorization...
  informal chat sign-off does not suffice") and `MARGIN-0005`'s own charter-then-gate structure
  (a charter names a bounded program; each stage inside it still requires its own review before
  advancing).
- **Current tiers and targets remain operational until formally superseded** — nothing about
  Milestones 1-2's execution changes, suspends, or conditions any accepted policy; per §2, they
  remain the current operating policy in full force throughout and after this work.

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
- any `MARGIN-0005` S3 trial, simulation, or research execution, and no consumption of any of
  its 300-run trial ceiling;
- recommending the use of margin, calculating a safe leverage level, or ranking assets for
  margin deployment — the §4 Milestone-3/4 margin-relevant evidence and future evidence
  register are factual and advisory only, never a leverage recommendation;
- substituting the future evidence register, or any WS-0005 output, for current broker
  maintenance requirements or for live, freshly synced account-level holdings/margin state —
  any future margin study must source that state separately, at the time of the study;
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

### 9. Zero-based future margin-policy review

This section states, for the avoidance of doubt where WS-0005's zero-based principle (§2, §3)
intersects the account's margin parameters, exactly how those parameters are and are not to be
treated once a future margin study is separately authorized (`WS-0004`, or a `MARGIN-0005`
successor). It grants no research authority itself — see the explicit non-authorizations below.

- **The current governed margin parameters remain binding operational safety guardrails until
  formally superseded.** The 1.8x leverage cap and the 30% buffer floor (`targets.yaml`'s
  `margin:` block; Constitution §3/§5; `MARGIN-0001` and its accepted successors) continue to
  govern every live trade, buy, and de-lever decision exactly as they do today. Nothing in this
  section, or in WS-0005 generally, changes that.
- **They are simultaneously provisional historical baseline values, not empirically validated,
  optimal, or permanent desired outcomes.** Per `NUM-0001`'s own provenance classification,
  both are recorded as *provisional governance guardrails* — doctrine decisions, not backtest
  verdicts (Constitution §5: "state the limit, apply it, and don't relitigate it without a
  genuinely new leverage regime in the data"). That doctrine status is exactly why they are not
  to be treated, in any future separately authorized research, as: assumptions that research
  must defend; or constraints on which candidate policies a separately authorized margin study
  may examine. The sole exception, stated in Constitution §3 itself and restated here for
  clarity: **no live system may exceed or disregard the current cap or floor before a
  replacement policy is formally accepted and implemented** — this is a bound on production
  behavior, never on what a bounded research charter may examine on paper.
- **Sequencing.** Restating and applying §7 item 4: any future margin research proceeds from
  first principles only after WS-0005's portfolio Intelligence, relationship mapping, policy
  review, and unlevered stress-analysis work are sufficiently complete. This is the same
  sequencing preference already recorded in §7 item 4, made explicit here because it bears
  directly on how any future margin study's evidence base is built.
- **What a future, separately authorized margin study should compare** (naming candidate
  dimensions, not commissioning the study): no-margin operation; the current policy;
  alternative leverage ceilings; alternative buffer requirements; concentration-adjusted or
  asset-sensitive risk limits; deployment, holding, repayment, and deleveraging rules; broker
  maintenance and liquidation mechanics; financing cost; and liquidity, gap, recovery-duration,
  and permanent-loss risk.
- **No preferential treatment for the incumbent values.** The current 1.8x and 30% figures may
  appear in that future study as historical baselines — they must not be treated as desired
  answers, and must not receive preferential treatment merely because they are already
  implemented. This is the same evidentiary discipline §2/§3 already state for tiers and
  targets, applied here explicitly to the two margin parameters because of their doctrine
  status under Constitution §5.

**This decision does not:**

- change either current parameter (the 1.8x leverage cap and 30% buffer floor are unchanged by
  this filing, exactly as every prior margin-related decision in this log has stated);
- supersede `MARGIN-0001` or any later accepted margin decision (`MARGIN-0003`, `MARGIN-0004`,
  `MARGIN-0005`, `GOV-0003`, `NUM-0001`);
- authorize `MARGIN-0005` S3 or a successor study;
- authorize any margin-policy recommendation;
- authorize any production change;
- consume any research trial (zero of `MARGIN-0005`'s 300-run trial ceiling is spent by this
  filing, exactly as §6 already states for the whole of WS-0005).

**Any decision to retain, replace, tighten, or loosen the current margin parameters requires
its own separate accepted margin-governance decision, filed after the relevant research and
independent review** — the same two-step research-then-adopt discipline `GOV-0003` already
established and `MARGIN-0005` already operates under; this section applies that discipline
explicitly to WS-0005's zero-based framing, it does not create a new or different path to
changing either parameter.

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

**On the amendment specifically:** authorizing Milestones 1-2 as one bounded first audit unit,
rather than leaving all nine milestones unauthorized, follows the same charter-then-gate
proportionality `MARGIN-0005` already applies — a charter may pre-authorize its own lowest-risk
opening gate (there, G0/G1's charter-and-data-adequacy work) without pre-authorizing everything
downstream of it, provided later stages still each require their own review. Milestones 1-2 are
read-only inventory and coverage/freshness audit work — no company judgment, no thesis, no
Intelligence content, no policy conclusion — the same category of work `OPS-0002`'s planning
phase and `MARGIN-0005`'s G1 data-adequacy gate were each pre-authorized to perform without a
separate per-gate decision. Requiring a second governance filing merely to open that
lowest-risk work, as the original version of this decision did, added process without reducing
risk. The margin-relevant-evidence requirement (§4, Milestones 3-4) is added now, at the
roadmap-definition stage, rather than later, because retrofitting an evidence-capture
requirement onto already-completed Milestone-3 research would mean re-reviewing assets a
second time — cheaper to state the requirement before any research begins than after.
Softening §3's blindness language to a research discipline rather than a literal-enforcement
claim corrects an overstatement the original text made: no session can be made to have not
read `targets.yaml`/CLAUDE.md during ordinary preflight, and claiming otherwise would have been
a claim this repository cannot actually verify — the discipline's real force (evidence first,
comparison second, no silent inheritance) is unchanged and restated more precisely.

**On the second amendment (§9) specifically:** the leverage cap and buffer floor occupy a
different governance category than an ordinary tier or target — Constitution §5 names them
doctrine, "deliberately immune to discretionary override," while `GOV-0003` already narrowed
that immunity by exactly one carve-out: bounded, pre-registered, evidence-gated *research* into
whether a conditional rule outperforms the fixed posture is permitted, though "opening a
research charter authorizes nothing on its own" and adoption still requires its own decision.
§9 does not expand that carve-out — it applies it precisely to WS-0005's specific context,
where the zero-based principle (§2/§3) could otherwise be read as ambiguous about whether it
reaches the two margin parameters at all. Leaving that ambiguous would have created a real risk
either direction: a future reader could wrongly conclude WS-0005's zero-based framing quietly
extends to relitigating the cap/floor without `GOV-0003`'s own charter-and-adoption discipline,
or conversely that the cap/floor are so immune to §5 that even a properly chartered future study
could not examine alternative values on paper. §9 forecloses both misreadings with the same
research-then-adopt sequencing `GOV-0003`/`MARGIN-0005` already established, stated here rather
than left to inference.

## Alternatives Considered

- **Leave Milestones 1-2 unauthorized, as the original version of this decision did, and
  require a second governance filing immediately after merge to open them.** Rejected on
  amendment — this was the original design, and the principal identified it as adding an
  unnecessary process step for the single lowest-risk unit of work in the entire roadmap
  (read-only inventory and coverage audit, no judgment, no content). Milestones 3-9 remain
  under the original, more conservative rule precisely because they are not this low-risk.
- **Authorize Milestones 1 through 9 all at once, now that the roadmap is defined.** Rejected —
  far exceeds the principal's authorization for this amendment, which is bounded to exactly the
  first audit unit; every milestone from 3 onward involves either judgment (Intelligence
  content, classification, recommendations) or the margin-relevant evidence capture this same
  amendment newly requires — none of that is safe to pre-authorize sight-unseen.
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
- **Say nothing about the margin parameters in WS-0005's zero-based framing, and let the
  existing `GOV-0003`/Constitution §5 text govern by silent inference.** Rejected on the second
  amendment — leaving the intersection unstated risks exactly the two opposite misreadings §9's
  Rationale describes (silent expansion of the zero-based principle into the cap/floor without
  `GOV-0003`'s charter discipline, or an over-broad reading of §5's "immune to discretionary
  override" that would block even a properly chartered study from examining alternative values
  on paper). Stating it explicitly costs one section and forecloses both.
- **Have §9 itself authorize a margin research charter or name WS-0004 as newly active.**
  Rejected — exceeds what was asked; §9 is confined to stating a framing/sequencing principle
  for *whenever* such research is later, separately authorized, and explicitly enumerates six
  things it does not do, including authorizing any study or trial consumption. WS-0004 remains
  exactly as dormant as `OPS-0001` left it.
- **Let the future study's comparison list (no-margin operation, alternative ceilings/floors,
  concentration-adjusted limits, deployment/repayment rules, broker mechanics, financing cost,
  liquidity/gap/recovery/permanent-loss risk) be open-ended rather than named.** Rejected — an
  unnamed list invites scope creep at the moment a future charter is drafted; naming the
  dimensions now, without commissioning any of them, gives a future charter a concrete starting
  point while still requiring its own full authorization to actually run.

## Consequences

Going forward: WS-0005 exists as the sole `priority: primary` workstream, with a governing
purpose, a zero-based-research-discipline protocol, and a nine-milestone roadmap recorded as a
scope ceiling. **Milestones 1 and 2 (baseline/inventory and Intelligence coverage/freshness
audit) are authorized to execute, in one bounded first audit PR, the moment this decision
merges** — no further governance decision is required to open that specific work. Milestones 3
through 9 remain roadmap items only, each requiring its own separate future authorization;
completing Milestones 1-2 does not itself authorize Milestone 3. The future Milestone-3
Intelligence-completion work and Milestone-4 relationship-mapping work each carry an explicit,
clearly-separated margin-relevant-evidence requirement — factual, advisory, and bounded by
explicit prohibitions against recommending margin use, calculating a safe leverage level,
ranking assets for margin deployment, or substituting for live broker/account state — so that
if `MARGIN-0005` S3 or a successor study is ever separately authorized, relevant evidence is
already gathered rather than needing a second pass over the same assets. **§9 additionally
records, for the avoidance of doubt, that the 1.8x leverage cap and 30% buffer floor remain
binding operational guardrails until formally superseded, while being provisional, doctrine-
status baseline values that a future, separately authorized margin study must evaluate without
pre-defending or preferring — the one Constitution §3 exception (no live system may exceed or
disregard either value before a replacement is formally accepted and implemented) is restated,
not narrowed.** §9 authorizes no research, no `MARGIN-0005` S3 or successor study, no
margin-policy recommendation, no production change, and consumes no research trial; it does
not change either parameter and does not supersede `MARGIN-0001` or any later margin decision.
WS-0001 moves to `priority: secondary` with its MARGIN-0005 research authority, milestones, and
S3 gate completely unchanged. WS-0002 remains `priority: secondary`, `status: authorized`,
with `OPS-0005`'s Phase Two grant fully intact and un-narrowed. WS-0003 and WS-0004 are
untouched. `operations/WORKSTREAMS.yaml`'s WS-0002 entry is synchronized to live GitHub truth
(PR #149 merged, `active_branch`/`active_pr` cleared, milestone status corrected, attribution
strengthened) without reopening `OPS-0005`'s accepted text. No allocator, `targets.yaml`,
`holdings.yaml`, margin rule, Company/Theme Intelligence record, or production code is touched
by this decision. This decision and the corresponding `operations/WORKSTREAMS.yaml`
synchronization become effective only when this exact implementing pull request merges to
`main` — not when pushed, and not merely when opened as a draft. The next concrete step is
principal review of this draft PR — not research, not implementation, and not merge.
