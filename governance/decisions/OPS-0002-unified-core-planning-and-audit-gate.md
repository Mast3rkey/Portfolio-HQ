---
decision_id: OPS-0002
date: 2026-07-24
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, GOV-0001, GOV-0002, GOV-0003, MARGIN-0005]
supporting_artifact: docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md
---

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
   authoritative over any other file. It documents: a three-layer architecture
   (authoritative deterministic allocation core / advisory decision-context layer
   / human decision and manual-execution layer); an Intelligence-value assessment
   framework that does not equate "no allocator coupling" with "no value"; an
   opportunity-cost principle preserving largest-dollar-gap-first as the sole
   mechanical capital-priority rule; a terminal end-to-end allocation-check
   acceptance milestone definition; and efficiency/return-contribution operating
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
   allocator/`targets.yaml`/`holdings.yaml`/`margin_state.py` change, no
   portfolio-policy change, no research execution, no Intelligence expansion, no
   trade, and no order. The implementing pull request must remain in **draft**
   state and **unmerged** until the audit in item 4 is complete.

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
