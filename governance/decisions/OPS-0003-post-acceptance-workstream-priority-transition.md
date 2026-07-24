---
decision_id: OPS-0003
date: 2026-07-24
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, GOV-0002, GOV-0003, MARGIN-0005]
supporting_artifact: operations/WORKSTREAMS.yaml
---

## Context

`OPS-0002` adopted the WS-0002 planning baseline (`docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md`),
moved WS-0002 to `status: review`/`priority: primary`, and placed WS-0001 (the MARGIN-0005 research
program) at `priority: secondary` under a principal sequencing hold pending exactly two things: "the
WS-0002 planning package and its first independent audit." OPS-0002 item 4 named that audit as the
one required gate before WS-0002's planning baseline could be accepted or any implementation
authorized.

That audit has since occurred and closed. PR #143 ("OPS-0002: WS-0002 unified-core planning baseline,
priority reprioritization, audit gate") carried the planning package and OPS-0002 itself through an
independent Fable audit (disposition: REMEDIATION REQUIRED, no Blocking finding — F1 disposed via
PR #142's closure, F2–F4 disposed by reconciliation commit `263b64b`), a confirming Fable delta
re-review against that exact head, and explicit principal acceptance of both conclusions. PR #143
merged to `main` at `3c31c2e9d36d55defc95d89c90ab041f31abf251`. The condition OPS-0002 item 3 named
for lifting WS-0001's sequencing hold — "the WS-0002 planning package and its first independent
audit" being complete — is therefore satisfied, as a plain fact about what PR #143 already did, not
a new judgment this decision introduces.

The principal has now explicitly authorized a narrow follow-on filing that: records the WS-0002
planning phase as complete (scoped to exactly what OPS-0002 authorized — the planning package,
its audit, reconciliation, and acceptance — not to any implementation); restores WS-0001 to
`priority: primary` now that its sequencing condition is met; synchronizes
`operations/WORKSTREAMS.yaml` to live repository truth; produces a read-only determination of
whether the one remaining authorized S2 implementation PR can close the MARGIN-0005 G2 gate; adds a
narrow dated acceptance note to the blueprint; and records the ordinary CLAUDE.md/governance-index
entries. This decision is that filing. It does not authorize implementation, research execution,
trial consumption, WS-0002 architecture implementation, or any allocator/holdings/targets/tiers/
clusters/margin/Intelligence/BTC/production-code/trade/order change.

## Decision

**Narrow supersession.** OPS-0003 supersedes OPS-0002 items 2 and 3 only with respect to the
WS-0001/WS-0002 priority ordering, the satisfied sequencing hold, and the completed WS-0002
planning-phase lifecycle state. OPS-0002 items 1, 4, 5, 6, and 7, its three-layer architecture, its
implementation prohibitions, and its audit gates remain fully effective and are not superseded.

Specifically:

1. **WS-0002 planning-and-audit phase recorded complete.** `operations/WORKSTREAMS.yaml`'s WS-0002
   entry moves to `status: complete`, meaning **exactly and only** the OPS-0002-authorized planning
   package, its independent audit, finding reconciliation, and principal acceptance — the work PR #143
   carried out and merged. This is not a claim that any WS-0002 *implementation* has occurred, begun,
   or is authorized; OPS-0002 item 5's implementation prohibitions continue to apply in full. WS-0002
   also moves to `priority: secondary` — its authorized planning work is done; nothing further is
   pending on it that would justify holding `priority: primary`. `active_branch` and `active_pr` are
   set to `null` (PR #143 is merged, not live). Any future Layer 2 architecture implementation
   remains within WS-0002's scope in name, but requires its own new, explicit governance decision to
   reactivate and authorize it — this decision does not do so, and does not lower that bar.

2. **WS-0001 priority restored.** `operations/WORKSTREAMS.yaml`'s WS-0001 entry returns to
   `priority: primary`, `status: in_progress` (unchanged). Every existing `governing_authority`,
   `authorized_scope`, `prohibited_scope`, `milestones` (G0–G2B, all merged and unchanged),
   `evidence_refs`, and `completion_criteria` is preserved exactly as OPS-0002 left them — nothing
   about MARGIN-0005's authority, evidence, or gate status changes here, only sequencing. The
   register's `blocker` field is updated to record, as fact, that the OPS-0002 sequencing condition
   was satisfied by PR #143 and that this decision restores primary priority — replacing the now-
   obsolete "held pending WS-0002 planning-and-audit completion" language, which no longer describes
   the current state. **This decision does not itself authorize opening the final S2 implementation
   PR named in WS-0001's `next_action`** — that PR requires its own separate future principal
   authorization, exactly as it already did under OPS-0002, unchanged by this filing.

3. **OPS-0002's sequencing-hold condition recorded satisfied.** As a factual matter: OPS-0002 item 3
   held further WS-0001 implementation "pending completion of the WS-0002 planning package and its
   first independent audit... unless the principal separately authorizes proceeding sooner." PR #143's
   merge completed that planning package and its audit. This decision records that the condition is
   met — it does not waive, shortcut, or reinterpret it.

4. **Register does not originate authority.** As under OPS-0001 and OPS-0002, `operations/
   WORKSTREAMS.yaml` remains a coordination record, not an authority source. This decision file is
   the authority for the transitions above; if the register and this decision ever appear to diverge,
   this decision (or any future decision that explicitly supersedes it) controls.

5. **Scope withheld, restated.** This decision authorizes no final S2 implementation PR, no
   simulation, no registered study run, no trial consumption (zero of the 300-run ceiling is spent by
   this filing; `trial_ledger.jsonl` and `candidate_freeze.yaml` remain absent), no WS-0002
   architecture implementation, and no allocator/`holdings.yaml`/`targets.yaml`/tier/cluster/margin/
   Intelligence/BTC/production-code change, trade, or order. The S2/G2 scope-determination document
   this decision's implementing PR also adds
   (`research/margin_target_study/S2_G2_SCOPE_DETERMINATION.md`) is itself read-only analysis — it
   recommends a scope for a possible later PR and does not open, authorize, or begin one.

6. **Blueprint status note.** This decision authorizes exactly one further change: a short, dated
   status note added to `docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md`, placed above the document's
   existing historical draft-status paragraph, stating that the planning baseline was independently
   audited, accepted, and merged through PR #143. No other blueprint text — including §§1–12's
   substantive architecture — is authorized to change by this decision.

7. **Future supersession required.** As under OPS-0002 item 7: any future change to the three-layer
   architecture, the terminal acceptance milestone, or the WS-0001/WS-0002 priority ordering set here
   requires its own explicit, separately filed governance decision that supersedes this one or
   OPS-0002 by name — never a silent edit to `operations/WORKSTREAMS.yaml` or either document alone.

## Rationale

This is a sequencing-and-recording action, not a new grant of authority — the same discipline
OPS-0002 itself applied to WS-0001/WS-0002's prior transition. OPS-0002 named a specific, checkable
condition ("the WS-0002 planning package and its first independent audit") for restoring WS-0001's
priority; PR #143 satisfied that condition in fact, and this decision's only substantive act is
recording that satisfaction and its consequence. Preserving WS-0001's authority, milestones, and
`next_action` verbatim follows the same reasoning OPS-0002 itself invoked (Constitution §5: state a
limit, apply it, don't relitigate without new evidence) — nothing about MARGIN-0005's evidence or
gate status has changed since OPS-0002; only sequencing has, twice now, in opposite directions, each
time exactly as the register's own text anticipated. Marking WS-0002 `complete` rather than leaving
it at `review` reflects that its own authorized scope (planning, audit, reconciliation, acceptance)
is, as a fact, now fully executed — leaving it at `review` after PR #143's merge would understate
what has already happened, while marking it `complete` in a way that implied implementation authority
would overstate it; the explicit "planning-and-audit phase only" qualifier is what keeps the label
accurate in both directions. The S2/G2 scope determination is commissioned here because WS-0001's own
`next_action` already named it as the correct next step once sequencing allowed it, and restoring
WS-0001 to primary without first producing that determination would leave the workstream primary
with no clear next action beyond it.

## Alternatives Considered

- **Leave WS-0002 at `status: review`.** Rejected — PR #143's merge means the planning-and-audit
  work OPS-0002 scoped is factually complete, not still under review; leaving it at `review`
  misdescribes the current state.
- **Mark WS-0002 `status: superseded` or delete its entry.** Rejected — WS-0002 as a workstream is
  not cancelled or replaced; its planning phase is complete and its future Layer 2 implementation
  remains a live, named future possibility pending its own authorization. `complete` (planning-phase
  scoped) is the accurate label, not `superseded`.
- **Authorize WS-0002 implementation directly in this filing, since planning is accepted.** Rejected
  — exceeds the principal's explicit authorization here, which is bounded to the transition,
  synchronization, scope-determination, and narrow blueprint note described above; OPS-0002 item 5's
  implementation prohibition is explicitly preserved, not lifted.
- **Authorize the final S2 implementation PR directly, since WS-0001 sequencing is restored and the
  scope determination recommends a scope.** Rejected — explicitly withheld by the principal's
  authorization; the scope determination is read-only analysis for a *later* authorization, not this
  one.
- **Rewrite OPS-0002 in place instead of filing a superseding decision.** Rejected — OPS-0002 is
  `status: Accepted`; per `governance/decisions/README.md`'s convention, its substance is not edited
  after acceptance. A narrowly-scoped superseding decision (this file) is the correct instrument,
  exactly as OPS-0002 itself anticipated in its own item 7.
- **Supersede all of OPS-0002.** Rejected — OPS-0002 items 1, 4, 5, 6, and 7, its three-layer
  architecture, its implementation prohibitions, and its audit gates are unaffected by anything this
  decision does; a blanket supersession would overstate this filing's actual scope.

## Consequences

Going forward: WS-0001 is again the sole `priority: primary` workstream; WS-0002's planning-and-audit
phase is recorded complete with no implementation authority attached; `operations/WORKSTREAMS.yaml`
reflects live repository and GitHub truth (PR #143 merged, no live branch/PR on WS-0002, WS-0001's
next action informed by the new scope determination); the blueprint carries one short acceptance
note with no substantive change to §§1–12; and a read-only S2/G2 scope determination exists for a
future, separate principal decision to act on or not. No allocator, `targets.yaml`, `holdings.yaml`,
`margin_state.py`, Constitution, existing accepted governance decision, Intelligence record or
schema, or MARGIN-0005 protocol/pre-registration file is changed by this decision. This decision,
`operations/WORKSTREAMS.yaml`'s corresponding field changes, the blueprint note, and the scope
determination become effective only once this exact implementing pull request merges to `main` — and
per the principal's session rules, that pull request opens as a **draft** and is not marked ready or
merged within this session. The next concrete step is principal review of this draft PR — not
implementation, and not merge.
