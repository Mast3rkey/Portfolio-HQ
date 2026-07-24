---
decision_id: OPS-0002
date: 2026-07-24
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, GOV-0001, GOV-0002, GOV-0003, MARGIN-0005]
supporting_artifact: docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md
---

_**2026-07-24 correction (same-day, pre-audit, pre-merge):** the first version
of this decision and its supporting blueprint incorrectly described
Company/Theme Intelligence as permanently limited to annotating or explaining
allocator output, with no path to influence targets, tiers, clusters, or
capital-priority policy. That has been corrected throughout item 1 and the
Rationale/Alternatives/Consequences sections below, and throughout the
blueprint's §§3–7, §10, and §12: Intelligence is the intended primary
analytical and organizational basis for **recommending** target/tier/cluster/
capital-priority policy changes, subject always to principal review, required
governance approval, and a separate bounded implementation PR before any such
recommendation reaches the allocator. This correction is made directly in this
still-unmerged, still-unaudited, never-yet-opened-PR decision record rather
than by superseding filing, per `governance/decisions/README.md`'s narrow-
correction convention — no independent audit has yet occurred against any
version of this decision, so there is no settled prior audit finding this
correction could contradict. Nothing else in this decision changes._

## Context

`OPS-0001` established `operations/WORKSTREAMS.yaml` as a coordination-only register
and, under principal authorization, recorded three durable planning intents —
including WS-0002, "Unified Portfolio-HQ core architecture and optimization audit"
— at `status: recommended`, `authorized_scope: none`, explicitly stating that "a
future, separately filed decision must scope and authorize the audit itself before
any work begins." That future decision is this one.

The principal has since explicitly authorized converting a completed planning
review into a durable blueprint, formally scoping WS-0002 planning and independent
audit, reprioritizing planning as the current primary workstream ahead of further
WS-0001 implementation, and establishing a future end-to-end allocation-check
acceptance milestone — while explicitly withholding authorization for
implementation, allocator changes, portfolio-policy changes, research execution,
Intelligence expansion, trades, or orders, and requiring that the implementing PR
remain draft and unmerged until independently audited by Fable or another
explicitly authorized high-capability reviewer.

This decision is that scoping action. It does not itself perform, or authorize
performing, any of the withheld categories above.

## Decision

1. **Planning baseline adopted.** `docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md`
   is adopted as the *proposed* WS-0002 planning baseline — a draft
   architecture/scope/sequencing document, independently re-verified against the
   live repository during this session, not an implementation and not itself
   authoritative over any other file. It documents a three-layer architecture:

   - **Layer 1 — authoritative deterministic allocation core**: holdings,
     accepted targets/tiers, accepted concentration/margin policy, live market
     data, and the allocator. At runtime this layer consumes only accepted
     governed policy and verified state; it never imports or interprets raw
     Intelligence.
   - **Layer 2 — Intelligence, portfolio organization, and policy-
     recommendation layer**: Company/Theme Intelligence, research evidence,
     freshness, uncertainty, thesis-break conditions, structural/economic
     overlap, measured return correlation, and opportunity-cost context. This
     layer is the intended primary analytical and organizational basis for
     **recommending** changes to portfolio role, tiers, per-holding targets,
     target weights, concentration clusters, and capital-priority policy —
     each recommendation carrying evidence, reasoning, uncertainty,
     alternatives, and thesis-break conditions. Every such recommendation
     remains advisory until accepted through governance; none is effective
     merely because it exists, and none may be imported by `allocate.py` or
     used at runtime to recalculate any allocator output.
   - **Layer 3 — principal decision, policy adoption, and manual execution**:
     the principal reviews a Layer 2 recommendation, accepts/rejects/narrows/
     defers it, authorizes any required governance decision and a bounded
     policy PR, after which the deterministic allocator applies the newly
     accepted policy as an ordinary input; execution stays manual in
     Robinhood, with fills and state synced back afterward.

   The blueprint states this as a governed policy-development loop (evidence →
   Intelligence synthesis → portfolio-level organization and comparison →
   target/tier/cluster/policy recommendation → principal and governance
   approval → governed policy update → deterministic allocation → manual
   execution → state reconciliation) — never a runtime Intelligence-to-
   allocator coupling. It also documents an Intelligence-value assessment
   framework centered on this policy-recommendation role (not merely "does it
   move allocator math"); an opportunity-cost principle distinguishing runtime
   allocation under currently accepted policy from periodic governed review of
   whether that policy should change, while preserving largest-dollar-gap-first
   as the sole mechanical runtime capital-priority rule; a terminal end-to-end
   allocation-check acceptance milestone that visibly separates actions valid
   under current accepted policy from advisory policy-review recommendations
   requiring separate approval; and efficiency/return-contribution operating
   principles for future planning and implementation work generally.

2. **WS-0002 reprioritized.** `operations/WORKSTREAMS.yaml`'s WS-0002 entry moves
   to `status: review`, `priority: primary`. Its authorized scope is exactly:
   completion of the planning package named in (1), independent high-capability
   audit of it, reconciliation of that audit's findings, and principal acceptance
   of the resulting planning baseline. **No implementation authority is granted.**
   WS-0002 no longer depends on WS-0001 reaching a stopping point first — the
   principal has explicitly reprioritized it sooner, which is the exact override
   condition OPS-0001's own WS-0002 entry already contemplated.

3. **WS-0001 sequencing hold.** `operations/WORKSTREAMS.yaml`'s WS-0001 entry
   moves to `priority: secondary`. `status` remains `in_progress`, and every
   existing `governing_authority`, `authorized_scope`, `prohibited_scope`,
   `milestones`, `evidence_refs`, `next_action` (the read-only S2/G2 scope
   determination), and `completion_criteria` is preserved exactly, unchanged.
   A principal sequencing hold applies to further WS-0001 *implementation* —
   specifically, opening the final authorized S2 PR — until the WS-0002 planning
   package and its first independent audit (item 4 below) are complete, unless
   the principal separately authorizes proceeding sooner. **This is a sequencing
   preference, not a finding that MARGIN-0005 is cancelled, technically defective,
   or complete**, and this decision does not claim any of those.

4. **Independent audit gate.** This decision's exact implementing pull request,
   at its exact head commit, requires an independent high-capability audit —
   currently intended to be performed by Fable, or another explicitly authorized
   high-capability reviewer — before the WS-0002 planning package may be accepted
   or any WS-0002 implementation may begin. Two further audit checkpoints are
   recorded as material and future only, not triggered by this filing: after
   material architecture implementation and before it becomes the default
   workflow; and before final end-to-end acceptance (the milestone in the
   blueprint's §6). Routine edits, mechanical register updates, small bug fixes,
   and ordinary test-only corrections do not require this audit.

5. **Scope withheld, restated.** This decision authorizes no implementation, no
   allocator/`targets.yaml`/`holdings.yaml`/`margin_state.py` change, no actual
   portfolio-policy change, no portfolio-level Intelligence engine, no computed
   conviction or opaque scoring, no research execution, no Intelligence-record
   expansion, no trade, and no order. **Item 1 defines Intelligence's intended
   future recommending role — it does not exercise that role**: no Company or
   Theme Intelligence record is created, modified, or acted upon by this
   decision, and no actual tier/target/cluster/capital-priority recommendation
   is made, reviewed, or accepted here. The implementing pull request must
   remain in **draft** state and **unmerged** until the audit in item 4 is
   complete.

6. **Register does not originate authority.** `operations/WORKSTREAMS.yaml` is
   updated to reflect items 2–3 as a coordination record — the same
   non-originating role OPS-0001 already assigns it. This decision file, not the
   register, is the authority for the priority and scope change; if the register
   and this decision ever appear to diverge, this decision (and any future
   decision that explicitly supersedes it) controls.

7. **Future supersession required.** Any future change to the three-layer
   architecture, the terminal acceptance milestone definition stated in the
   blueprint, or the WS-0001/WS-0002 priority ordering set here requires its own
   explicit, separately filed governance decision that supersedes this one or the
   blueprint by name — never a silent edit to `operations/WORKSTREAMS.yaml` or the
   blueprint file alone.

## Rationale

Mirrors the discipline OPS-0001 and GOV-0002 already applied to coordination and
precedence decisions: a scoping/priority action does not itself implement
anything, and its effect is gated on merge. Here that gate is deliberately
stronger — merge is additionally conditioned on an independent audit — because
this filing simultaneously reprioritizes two active workstreams and adopts a
durable architecture document; the stakes justify the extra check the same way
GOV-0002's own operational-precedence hierarchy reserved the heaviest process for
the changes with the widest blast radius. Preserving WS-0001's authority,
milestones, and next action verbatim follows Constitution §5's own reasoning
(state a limit, apply it, don't relitigate without new evidence) applied here to
*authorization*, not just risk parameters — nothing about MARGIN-0005's evidence
or gate status has changed; only sequencing has. The Constitution §6 discipline
("verify before acting on external review") governs how the supporting blueprint
was built: it does not carry forward any unseen prior report's conclusions,
because that report's content was not available to this session — see the
blueprint's own §0.

The Layer 2 recommending role (item 1) is deliberately narrower than either of
the two failure modes it sits between: it is not the permanent, runtime-only
annotation layer the first draft of this decision incorrectly described, and it
is not a live coupling that lets Intelligence output change allocator behavior
directly, which PI-0001's advisory-only architecture and Constitution §4's
no-predictive-research boundary both already forbid. The corrected role is the
one that already exists implicitly in this repository's own practice —
TGT-0001/TGT-0002 show tier/target changes already flowing through principal
review and a governance decision before `targets.yaml` changes — this decision
and the blueprint simply name that existing pattern as Layer 2's intended
purpose, rather than inventing a new mechanism.

## Alternatives Considered

- **Leave WS-0002 at `recommended`/`authorized_scope: none`.** Rejected — the
  principal explicitly authorized scoping planning and audit now; OPS-0001's own
  text anticipated exactly this future decision.
- **Authorize WS-0002 for implementation directly, skipping the audit gate.**
  Rejected — exceeds the principal's explicit authorization, which is bounded to
  planning-package review and independent audit only.
- **Mark WS-0001 `status: cancelled`, `blocked`, or `complete`.** Rejected —
  explicitly prohibited by the principal's authorization; WS-0001's substance,
  authority, and evidence are unaffected by this filing, only its relative
  priority and near-term sequencing are.
- **Correct the BTC `holdings.yaml`/`CLAUDE.md`/`targets.yaml` wording conflict in
  this same PR.** Rejected — outside this filing's four authorized paths; recorded
  in the blueprint (§9) as an open item requiring its own separately verified
  reconciliation.
- **Require the independent audit for every future WS-0002-adjacent edit.**
  Rejected — disproportionate under the blueprint's own efficiency principles
  (§7); only three material gates are recorded, and routine/mechanical changes are
  explicitly exempted.
- **Create additional workstreams for Fable auditing, branch cleanup, the
  end-to-end milestone, or Intelligence expansion.** Rejected — explicitly out of
  scope per the principal's authorization; none is created by this filing.
- **Keep WS-0002 dependent on WS-0001 reaching a stopping point.** Rejected — the
  principal's explicit reprioritization is the exact override condition
  OPS-0001's original WS-0002 entry already named ("unless the principal
  explicitly reprioritizes this workstream sooner").
- **Leave Intelligence architecturally permanently display-only (the original
  draft's error).** Rejected on principal correction — casting Layer 2 as
  annotation-beside-the-allocator-forever, with no path to influence policy at
  all, understated what Intelligence is intended to do (recommend governed
  target/tier/cluster/capital-priority changes) and was corrected in place
  (see the dated correction note above) rather than left standing.
- **Let Layer 2 recommendations reach the allocator directly, or through a
  computed score, without principal/governance gating.** Rejected — this is
  the opposite failure mode from the one just corrected, and remains
  prohibited by PI-0001's advisory-only architecture and Constitution §4; the
  corrected item 1 recommending role is intentionally bounded by "The essential
  distinction" in the blueprint's §3, not a step toward this alternative.

## Consequences

Going forward: WS-0002 is the current primary workstream, scoped exactly to
completing and auditing this planning package; WS-0001 continues to hold all of
its existing MARGIN-0005 research authority, with its next implementation step
held pending WS-0002's planning-and-audit completion or a separate principal
authorization to proceed sooner. No allocator, `targets.yaml`, `holdings.yaml`,
`margin_state.py`, Constitution, existing accepted governance decision, Intelligence
record or schema, or MARGIN-0005 protocol/pre-registration file is changed by this
decision. This decision, `operations/WORKSTREAMS.yaml`'s corresponding field
changes, and the blueprint it names become effective only once this exact
implementing pull request merges to `main` — and that pull request must remain in
draft state, unmerged, until the independent audit named in item 4 is complete
against its exact head commit. The next concrete step is that audit — not
implementation, and not merge.
