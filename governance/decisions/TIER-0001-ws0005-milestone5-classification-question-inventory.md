---
decision_id: TIER-0001
date: 2026-08-04
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0009, ONTO-0001, PI-0003, PI-0004, PI-0015, PI-0016, PI-0022, PI-0037, REL-0001, REL-0006, TGT-0001, TGT-0002]
supporting_artifact: governance/audits/WS0005_M5_CLASSIFICATION_QUESTION_INVENTORY_20260804.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded WS-0005 Milestone 5
governance-and-inventory PR under a new decision identifier, `TIER-0001`, conditioned on live
verification that the identifier is unused. The stated purpose: determine what the current flat
tier/destination system conflates and what questions a future classification architecture must
answer — using only existing repository evidence, with an explicit design preference for the
smallest architecture that materially improves portfolio decisions, separating concepts only
where doing so changes capital priority, risk interpretation, monitoring, or review cadence, and
rejecting decorative complexity. This authorization is explicitly bounded to Milestone 5's first
unit only; it does not authorize Milestones 6-9.

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local `main` confirmed identical to `origin/main` at
`09fc72b4671fb18d9b3a4c2f1f1141657660ad35`, working tree clean. Zero open pull requests
(`mcp__github__list_pull_requests`, `state: open`, returns `[]`) — no active mutation lane.
`TIER-0001` confirmed unused: zero matches in `governance/decisions.yaml`, zero matches via
`mcp__github__search_code` across the repository, and `governance/decisions/README.md`'s prefix
history names no `TIER-####` series. `PI-0037` (WS-0005 Milestone 3 completion) and `REL-0006`
(WS-0005 Milestone 4 completion) both independently re-confirmed merged and ancestors of the
current tip; `OPS-0016` (PR #236, naming the future application "Eureka") also independently
confirmed merged and folded into the current tip via direct ancestry check
(`git merge-base --is-ancestor 6ea327c7... 09fc72b4...`). `governance/decisions/` carries 71
decision files (excluding `README.md`) against 71 `governance/decisions.yaml` rows — confirmed
1:1 by direct count this session, not copied from a prior filing's stated total.

WS-0005's own register entry confirms: Milestone 1 complete, Milestone 2 complete, Milestone 3
complete (`PI-0037`), Milestone 4 complete (`REL-0006`), Milestones 5-9 `status: proposed`
(unauthorized) prior to this filing. `OPS-0006` §4 item 5 is the sole existing text defining
Milestone 5's scope — quoted in full in the supporting artifact §2 and not restated here.

No existing accepted decision anywhere in `governance/decisions.yaml` authorizes any Milestone 5
execution, proposes a `TIER-####` prefix, or performs a classification-question inventory —
confirmed by full-repository grep for "Milestone 5", "zero-based classification", and
"tier-architecture review" outside `OPS-0006` and `operations/WORKSTREAMS.yaml` itself.

## Decision

This filing does two things, in one combined governance-and-inventory PR, per the principal's
explicit packaging instruction (matching the `REL-0002`/`REL-0003` combined-filing precedent
rather than `REL-0001`'s split-into-two-PRs precedent):

1. **Freezes the exact scope of WS-0005 Milestone 5's first bounded unit** — a read-only
   inventory, against nine candidate classification questions (economic/portfolio role,
   research conviction, capital-allocation priority, risk concentration and overlap,
   dependency/relationship exposure, monitoring intensity, review cadence, implementation
   readiness, uncertainty/evidence quality), of what the current flat `targets.yaml`
   `destination:` representation does and does not already capture, using only already-accepted
   repository evidence. No new company, theme, or relationship research is performed.
2. **Performs that inventory**, retained at
   `governance/audits/WS0005_M5_CLASSIFICATION_QUESTION_INVENTORY_20260804.md` — mapping each of
   the nine axes to existing evidence, distinguishing axes already adequately differentiated in
   practice from axes that are decorative (present in schema but never varied) or duplicative of
   an already-frozen but unused vocabulary (`docs/INVESTMENT_ONTOLOGY.md`), and recommending, as
   text only (not an authorization), that at most four axes — economic role, capital priority
   (already load-bearing and unchanged), risk concentration, and a merged uncertainty/
   evidence-quality axis — warrant a future Milestone-5 framework-design pass.

This decision explicitly does **not**: classify any ticker; propose or draft a candidate final
tier framework; perform blind classification; reconcile the Milestone-1 baseline against
anything; compute a mechanical score of any kind; or authorize Milestone 6 (blind
classification), Milestone 7 (baseline reconciliation), Milestone 8 (policy recommendation
package), or Milestone 9 (independent review and adoption). Existing tiers, targets, roles,
caps, gates, and position sizes remain the current operating policy in full force, unchanged and
unaffected by this filing, per `OPS-0006` §2's zero-based-research-discipline protocol — a
holding's current `target_pct` or `portfolio_role_ref` value is recorded as a policy fact in the
supporting artifact, never treated as evidence for or against any future framework.

## Rationale

**Why a new `TIER-####` prefix.** `governance/decisions/README.md`'s convention mints a new
prefix only for a genuinely new decision domain, not pre-declared in advance. `PI-####` is
frozen, one-way, non-relational Company/Theme Intelligence content (`PI-0006`) — Milestone 5's
subject (what the tier/destination *architecture itself* conflates, independent of any single
company's record) does not fit that shape. `REL-####` is specifically pairwise relationship-
record content (`REL-0001`) — unrelated to tier architecture. `CHART-####` and `LADDER-####` are
narrower still (chart evidence, buy-ladder backtesting). `OPS-####` was considered and rejected:
`OPS-0006` already established WS-0005's nine-milestone roadmap as a cross-cutting operational
filing, but every milestone-content unit executed since (Milestone 3's `PI-####` batches,
Milestone 4's `REL-####` filings) has used its own content-specific prefix rather than `OPS-####`
— using `OPS-####` for Milestone 5's actual classification-architecture content would break that
established pattern and misfile classification-domain reasoning under the operations-coordination
domain. `TIER-0001` — naming the domain directly (tier/classification architecture review) —
follows the same minting discipline `LADDER-0001` and `REL-0001` already applied.

**Why combine authorization and inventory in one PR, unlike `REL-0001`.** `REL-0001` split schema-
freeze (governance) from inventory (a later, separate implementation PR) because Milestone 4's
inventory required classifying evidence against a newly-frozen 12-item taxonomy that did not yet
exist at authorization time. Milestone 5's first unit has no equivalent taxonomy-freeze
prerequisite — the nine candidate questions were fully specified by the principal's own
authorization text, so there is no schema gap to close before the inventory can proceed. The
principal explicitly requested one combined PR; `REL-0002`/`REL-0003` already establish precedent
for combining governance authorization and bounded content delivery in a single filing when the
principal so directs.

**Why the inventory reaches the conclusions it does.** See the supporting artifact in full. In
summary: `target_pct` is the sole allocator-visible field and was designed that way deliberately
(`PI-0003`, `ONTO-0001` §F); the other eight candidate axes already exist in some form across
Company Intelligence, the freshness registry, and relationship records, but two (`monitoring_
enabled`, `risks[].status`) are schema-present yet 100% uniform across the entire 47-record
corpus (confirmed live this session) and are therefore decorative rather than load-bearing;
`portfolio_role_ref` carries a stale tier vocabulary that `targets.yaml` itself no longer defines,
a genuine drift rather than a live conflict; and `docs/INVESTMENT_ONTOLOGY.md` already freezes a
conceptual hierarchy (Economic Systems → Company Roles → Company Quality → Capital Priority →
Tier → Target Allocation) and an explicit preserved-distinctions list covering most of the nine
axes, but has zero applied instances anywhere in the repository — meaning a future Milestone-5
framework has an existing, unused scaffold to reconcile with rather than a blank slate to design
from scratch, directly serving the principal's stated preference for the smallest sufficient
architecture.

## Alternatives Considered

- **Defer the inventory to a later, separate implementation PR** (the `REL-0001` pattern). Not
  used because the principal's authorization explicitly requested a combined governance-and-
  inventory PR and no taxonomy-freeze prerequisite exists here that would justify the split.
- **File under `OPS-####`** as a continuation of `OPS-0006`'s own roadmap-defining text. Rejected
  — see Rationale; would break the established content-specific-prefix pattern for milestone
  execution units.
- **Propose a candidate framework in this same filing** (e.g., a concrete four-field schema).
  Rejected — explicitly out of scope for Milestone 5's *first* unit per the authorizing
  instructions ("do not create a candidate final tier framework... do not classify any ticker
  yet"); the supporting artifact's §6 table is a recommendation of which axes merit further
  consideration, not a framework design, and is stated as advisory text rather than an
  authorization of any kind.
- **Retain all nine axes as equally worth pursuing.** Rejected — the evidence (uniform
  `monitoring_enabled`/`status` values, `implementation readiness` being process metadata rather
  than an economic ticker property) does not support treating all nine as equally live; naming
  that explicitly serves the principal's "reject decorative complexity" instruction more directly
  than a neutral nine-way list would.

## Consequences

**Changes as a direct result of this decision:** the existence of a retained, evidence-grounded
inventory artifact answering what the current flat representation does and does not capture; a
narrowed candidate set (at most four axes) for any future Milestone-5 framework-design unit to
consider; explicit disclosure of two decorative fields (`monitoring_enabled`, `risks[].status`)
and one stale-vocabulary field (`portfolio_role_ref`) for future correction consideration; and
six named unresolved questions requiring their own future principal judgment before any framework
is drafted.

**Does not change:** any tier, target, cap, cluster, gate, or holding; any allocator or margin
behavior; any Company, Theme, or relationship record's content; `docs/INVESTMENT_ONTOLOGY.md`'s
frozen text; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s frozen schema; WS-0005's top-level `status`
(remains `in_progress`, since Milestones 6-9 remain unauthorized); or any brokerage, trading, or
order-related capability. Completing this unit does not itself authorize a second Milestone 5
unit, a candidate framework design, or any later milestone — each requires its own separate,
explicit, future principal authorization, per `OPS-0006` §16.4's standing rule that the register
never originates authority and no completion claim may be inferred beyond what was actually
authorized and delivered.
