---
decision_id: TGT-0001
date: 2026-07-20
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, MARGIN-0001, PI-0001]
supporting_artifact: null
---

## Context

No prior accepted decision governs how the aggregate nominal target sum
changes when a ticker is promoted, demoted, added, or removed. Individual
roster/tier changes have been approved one at a time (see Prior-Decision
Supersession below) with no standing rule for what happens to the sum of
`targets.yaml`'s per-tier weights as those individual changes accumulate.

Recomputed directly from the current `targets.yaml` at filing time: T1
(9 tickers × 3.35%) 30.15% + T2 (15 tickers × 1.65%) 24.75% + ETF
(3 tickers × 2.30%) 6.90% + band (33 tickers × 0.75%) 24.75% + spec
(5 tickers × 1.00%) 5.00% + crypto sleeve 10.0% = **101.55%** of book. This
is the configured nominal target sum, not a holdings figure and not a
margin figure.

Existing runtime cluster controls (`targets.yaml`'s `caps.clusters`, the
T1/T2 concentration ceiling) operate on **live holdings values** computed
by `allocate.py` at run time — they block a buy when no room remains and
mechanically trim an actual breach. Nothing in the existing code path
normalizes, caps, or even sums the *configured* aggregate target weights
across tiers; `targets.yaml` is free-form config, and 101.55% is simply
what the current roster's individual weights happen to add up to, not a
number any code checks.

An input-validation assessment of `targets.yaml`/`allocate.py` was produced
as supporting evidence for this filing. It is evidence only — a data point
about current code behavior — and originates no doctrine of its own; every
doctrinal statement in this decision is stated and justified on its own
terms below, not inherited from that assessment.

A principal-supplied "Target-Budget and Leverage Semantics" analysis was
conversational deliberative context that led to this filing. It is not a
repository artifact, is not cited as one, and carries no authority beyond
having prompted this ADR — this document, not that conversation, is the
governance record.

## Decision

1. **Target and roster changes are additive by default.** A promotion,
   demotion, addition, or removal of a ticker is evaluated and approved on
   its own merits; no universal mechanically offsetting demotion or removal
   is required as a precondition.
2. **Each change requires individual approval.** Additive-by-default does
   not mean automatic — every tier/roster change remains its own decision,
   made the same way tier placements have always been made in this
   repository (see Prior-Decision Supersession).
3. **An offset is not universally required.** No standing rule forces a
   proposal to remove or shrink another position to "pay for" a new or
   promoted one.
4. **Several proposed changes must be analyzed cumulatively**, not
   independently, when more than one is under consideration at once — see
   the Mandatory Disclosure Template's combined-consequences requirement
   below.
5. **No advisory research artifact automatically changes `targets.yaml`.**
   Company Intelligence, Theme Intelligence, and any other advisory layer
   remain exactly as bounded by `PI-0001` and its successors: `targets.yaml`
   is sole authority for tier weights, and nothing in this decision changes
   that.
6. **No separate nominal-target ceiling is adopted now.** This decision
   does not fix a maximum for the configured nominal target sum.
7. **Lack of a ceiling is not permission for unreviewed expansion.** Not
   adopting a numeric ceiling is a decision to govern cumulative growth
   through mandatory disclosure and individual review (items 2 and 4
   above), not a decision to leave it ungoverned. A proposal that grows the
   nominal target sum still requires the same individual approval and
   cumulative-disclosure discipline as any other change under this policy.

### Comparable scale, different control layers

The configured nominal target sum divided by 100, and the 1.8x structural
leverage cap, are dimensionally comparable gross/book multiples — both
express a ratio of hypothetical-or-actual gross position value to book
(net equity). That comparability is arithmetic only, and the two numbers
mean different things:

- The nominal target sum is **declarative configuration** — the sum of
  what `targets.yaml` currently says each tier should hold, nothing more.
- The implied fully-filled gross exposure (nominal target sum ÷ 100, as a
  multiple of book) is a **hypothetical configuration consequence** — what
  gross exposure would result if every target were simultaneously filled
  to exactly 100% of its own weight, which is not how the allocator
  operates in debt-free cash-only conditions (see Cash-Only Behavior).
- The leverage cap is a **hard capacity ceiling** — a mechanical, enforced
  limit on actual gross-position-value ÷ net-equity, checked against the
  most recently synced Robinhood buffer before any margin-funded buy, per
  the unchanged margin doctrine in `CLAUDE.md`.

Being below the leverage cap does not establish that any given nominal
target configuration is prudent or authorized — the cap is a ceiling on
borrowed capacity, not a stamp of approval on target design. Symmetrically,
the nominal target sum being above 100% does not automatically request or
use margin — see Margin Separation below.

### Mandatory disclosure template

Every future proposal to add, promote, demote, or remove a ticker (or any
combination thereof) must include:

- ticker;
- current and proposed sleeve;
- current and proposed target percentage;
- percentage-point change;
- total nominal target percentage before and after;
- amount above or below 100% before and after;
- implied fully-filled gross-exposure multiple before and after;
- theoretical additional gross exposure above book at a clearly
  timestamped current-book snapshot;
- source and freshness of that book snapshot;
- an explicit statement that the disclosure does not request or authorize
  margin;
- whether the gap between the complete target set and debt-free cash-only
  capacity widens or narrows;
- combined cumulative consequences when multiple changes are proposed
  together or in close succession;
- trim-regime consequences (band/spec RSI-gated trims, cluster-cap
  mechanical trims, T1/T2 concentration-ceiling mechanical trims);
- cluster-target totals before and after, for every cluster the affected
  ticker(s) belong to.

A proposal must never describe itself, or be described, as automatically
"requiring margin" — margin is a separate human input each cycle (see
Margin Separation).

### Ex-ante cluster-compatibility rule

This is a **new governance admission rule**, not a description of existing
allocator behavior. Current allocator behavior, unchanged by this
decision:

- uses live cluster values (holdings market value at run time), not
  configured target weights;
- blocks a live buy when no cluster room remains;
- mechanically trims an actual cluster breach, no RSI gate;
- does not reject a `targets.yaml` configuration merely because its
  configured cluster target weights sum above that cluster's cap — the
  code has no such check today.

New governance rule, effective for every future roster/tier proposal:

- calculate the affected cluster(s)' configured target-weight totals
  before and after the proposed change;
- a proposal that would place a configured cluster target total above that
  cluster's existing cap (`targets.yaml`'s `caps.clusters[].pct`) is **not
  approvable as written**;
- an unapprovable proposal may be revised by using a lower tier, fewer
  promotions, an explicit offset elsewhere in the same cluster, or by
  opening a separately governed cluster-cap review (the same kind of
  correlation-scan-and-derive process used for the semis/power_infra/oil
  caps);
- overall leverage capacity (the 1.8x cap, or headroom under it) never
  overrides this rule — cluster-target compatibility and leverage capacity
  are independent checks, and passing one never substitutes for the other;
- no allocator code changes as a result of this rule — it is a
  proposal-review-time governance check, applied before a change is
  approved, not a runtime mechanism.

### Margin separation

- Target and roster changes do not request, recommend, authorize, size, or
  determine margin use — a promotion never requests, authorizes, or
  recommends margin.
- Margin remains a separate human input entered per deposit/allocation
  cycle (`--margin X`), exactly as `CLAUDE.md`'s Workflow section already
  states.
- The 1.8x leverage cap and 30% buffer floor remain unchanged, still
  fixed, mechanical, and non-discretionary, per the unchanged margin
  doctrine.
- The existing fixed structural-capacity doctrine (no margin-timing
  model, no "right time to borrow" discretion) remains authoritative and
  is not reopened by this decision.
- Current account margin debt is **portfolio state**, tracked in
  `holdings.yaml` and recomputed from source on every run. It is neither
  zero nor altered, interpreted, or referenced numerically by this
  decision — this decision is about declarative target configuration, a
  distinct concept from actual debt outstanding.

The following concepts are kept separate throughout this decision and must
be kept separate in every future disclosure made under it: existing margin
debt (portfolio state) · current-cycle margin requested (human input) ·
current-cycle margin allowed (capacity, i.e. the leverage-cap/buffer-floor
clip) · current-cycle margin used (an allocation outcome) · nominal target
sum (declarative configuration) · implied fully-filled gross exposure
(hypothetical configuration consequence).

### Cash-only behavior

The configured nominal target sum is already 101.55% of book. That
configuration does not itself request, authorize, recommend, size, or
determine margin use. In debt-free cash-only operation, the complete
target set may not be simultaneously filled; some targets may remain
underfilled and continue competing through the existing largest-gap-first
mechanism (`allocate.py`'s `plan()`, unchanged by this decision).

### Prior-decision supersession

Future changes to the following names must identify and explicitly
supersede the applicable prior reasoning before a new placement or
retention decision is filed:

- **AMZN** — kept at T2, not promoted to T1 (PR #18, merged 2026-07-13:
  "Resolve AMZN and VMC Open Items").
- **AVGO** — kept at T2, not promoted to T1 (PR #58, merged 2026-07-14:
  "Tier-fit scan: promote AAPL to T2, keep AVGO at T2").
- **AAPL** — promoted band → T2 (PR #58, same merge, same session).

This list is **not necessarily exhaustive** of every prior placement or
retention decision this policy could apply to — it names the three
decisions identified at filing time as carrying reasoning a future
proposal is most likely to encounter. A future proposal touching any other
previously-decided placement is equally bound to identify and supersede
that placement's own recorded reasoning, whether or not it appears in this
list.

## Rationale

`targets.yaml` has no existing fixed-sum invariant and the code performs
no normalization of aggregate target weights — 101.55% is simply what the
current roster adds up to, not a number bounded or checked anywhere today.
Because nothing governs it, the cumulative effect of future individual
tier/roster changes on that sum is presently ungoverned: nothing today
would surface, at proposal time, whether a string of individually
reasonable promotions was quietly compounding the nominal target sum
upward. Mandatory disclosure (this decision's Mandatory Disclosure
Template) makes that cumulative effect visible at the point of each
decision, without requiring any code change or runtime enforcement.

The principal's judgment, exercised in approving this policy, is to govern
future tier and roster changes through additive, case-by-case,
individually-approved decisions rather than through a universal offset
requirement or a new numeric ceiling — the same posture this repository
has already used for every individual tier decision to date (AMZN, AVGO,
AAPL). The mandatory ex-ante cluster-compatibility review is retained as a
distinct, non-optional check because it protects a separate,
already-established concentration-risk boundary (the correlated-cluster
caps) that a purely additive, disclosure-only policy would not otherwise
touch — a proposal can be individually well-reasoned and still push a
cluster's configured total past its cap, which is precisely the failure
mode this rule exists to catch before approval rather than after a live
breach forces a mechanical trim.

The historical observation that live T1 holdings reached 42.1% of book
against a 30.15% configured target (see `CLAUDE.md`'s "T1 AI-infra
cluster cap: scanned and declined" entry) is not evidence of prior
additive nominal-target drift — the T1 target weights that produced 30.15%
did not themselves drift; the *holdings* diverged from *target* through
ordinary price appreciation with no T1/T2 trim rule in place at the time.
It is cited here only as evidence that actual holdings can diverge
materially from configured targets, which is exactly why independent,
live-data runtime controls (the cluster caps, the T1/T2 concentration
ceiling) exist alongside — not in place of — target-level governance.

## Alternatives Considered

- **Universal budget-neutrality** (every roster/tier change must be offset
  elsewhere so the nominal target sum never grows). Rejected: this would
  force cosmetically-motivated trims or demotions to make room for
  independently-justified promotions, coupling two decisions that may have
  nothing to do with each other and creating pressure to weaken a good
  proposal's sizing just to satisfy an accounting identity rather than an
  investment judgment.
- **Adopting a separate numeric ceiling now** (e.g., capping the nominal
  target sum at some fixed percentage of book). Rejected for this filing:
  no evidence-based level has been derived, and inventing one without the
  same derivation discipline used for the cluster caps (correlation scan,
  stress test) would be an arbitrary number dressed as a control. This is
  not a permanent rejection — a future decision may adopt one if evidence
  supports a specific level.
- **Core-versus-margin-overlay architecture** (splitting the roster into a
  debt-free "core" book and a separately governed margin-funded overlay).
  Rejected for this filing: this would be a materially larger structural
  change to how `targets.yaml`/`allocate.py` represent the book, well
  beyond what this decision's scope (target-budget governance for roster
  changes) requires, and duplicates capacity control the leverage cap and
  buffer floor already provide.
- **No governance/disclosure requirement** (leave roster/tier changes
  exactly as informally decided as they have been). Rejected: this is the
  status quo this decision was raised to correct — the cumulative-effect
  visibility gap identified in Context and Rationale would remain
  unaddressed.

None of these alternatives is foreclosed permanently; each could be
revisited by a future decision if the evidence or circumstances that
disqualified it here change.

## Consequences

This decision changes no code and no configuration. Confirmed unchanged:
current ticker assignments; current target weights; cluster-cap numbers;
the 1.8x leverage cap; the 30% buffer floor; `allocate.py` allocator
behavior; trim behavior (band/spec RSI-gated, cluster-cap mechanical,
T1/T2 concentration-ceiling mechanical); crypto sleeve policy; regime-gate
behavior (informational only, per the regime-gate backtest verdict); live
account state; and the recommendation-only, manual-execution model — this
tool still never places orders.

Going forward, every future roster/tier-change proposal must satisfy the
Mandatory Disclosure Template and the Ex-Ante Cluster-Compatibility Rule
above before approval. `governance/decisions.yaml` gains one new row for
this entry. `CLAUDE.md`'s Decisions Log gains one short pointer entry. No
separate nominal-target ceiling exists as a result of this decision, and
that absence is not itself authorization for automatic or unreviewed
cumulative expansion of the nominal target sum — every change remains
individually approved under items 2 and 4 of the Decision section above.
