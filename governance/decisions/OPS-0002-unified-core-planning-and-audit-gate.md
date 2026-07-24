---
decision_id: OPS-0002
date: 2026-07-24
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, GOV-0001, GOV-0002, GOV-0003, MARGIN-0005]
supporting_artifact: docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md
---

## Context

A prior, read-only Sonnet planning session produced a comprehensive
system map, authority map, gap register, and phased roadmap for WS-0002
("Unified Portfolio-HQ core architecture and optimization audit"), the
workstream `OPS-0001` recorded as `recommended`/`secondary`/
`authorized_scope: none` pending its own future scoping decision. That
session made no repository change. The principal has since reviewed that
report and explicitly authorized converting it into a durable,
repository-native planning baseline, formally scoping WS-0002's planning
and independent-audit phase, reprioritizing it ahead of the in-progress
MARGIN-0005 research program (WS-0001) for this phase only, and recording
the future end-to-end allocation-check acceptance milestone WS-0003
already anticipates as its terminal item. This decision, and the blueprint
it names as supporting artifact, are the result — reverified against the
live repository at `69723a69bb863cc792ac3f09818be64fe628ffd4` rather than
copied from the prior report's conclusions.

## Decision

Establishes `docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md` as the
**proposed planning baseline for WS-0002** — a three-layer architecture
(authoritative deterministic allocation core; advisory decision-context
layer; human decision and manual-execution layer), a corrected assessment
of Company/Theme Intelligence's contribution, a restated opportunity-cost
doctrine, a defined-but-not-yet-reached end-to-end allocation-check
acceptance milestone, explicit efficiency/return-contribution operating
principles, and a durable independent-audit-gate practice. Full content in
the supporting artifact; not restated here.

**This decision authorizes exactly:**

1. Filing the blueprint and this decision record as a **draft, unmerged**
   planning package.
2. **Review of that package by an independent, high-capability
   auditor — currently intended to be Fable, named generically so the
   practice survives a future model change** — against the exact commit
   that introduces it.
3. Reconciliation of that audit's findings (accepted, corrected, or
   explicitly declined with stated reasoning).
4. The `operations/WORKSTREAMS.yaml` field changes enumerated below.

**This decision does not authorize:** any architecture implementation;
any change to `allocate.py`, `margin_state.py`, `targets.yaml`, or
`holdings.yaml`; any change to the Constitution or any existing accepted
governance decision; any Intelligence-record or Intelligence-schema
change; any MARGIN-0005 research execution, simulation run, or trial
consumption; any trade or order. Implementation of anything the blueprint
describes requires (a) the independent audit above, (b) reconciliation of
its findings, and (c) its own separate, future principal authorization of
implementation scope — all three, not any one alone.

**Priority reprioritization (principal decision, recorded here):**

- **WS-0002** — `status: review`, `priority: primary`. Authorized scope:
  planning-package review, independent audit, and finding reconciliation
  only. No implementation authority.
- **WS-0001** (MARGIN-0005) — remains `status: in_progress`, becomes
  `priority: secondary`. Every element of its existing research authority,
  milestones, completion criteria, and its exact S2/G2 `next_action` text
  is preserved unchanged. A principal sequencing hold is recorded: the
  final authorized S2 implementation PR is held pending WS-0002's planning
  package completion and its first independent audit, unless the principal
  separately authorizes proceeding sooner. **MARGIN-0005 is not cancelled,
  not blocked by a technical defect, and not complete** — only its next
  implementation step is sequenced behind this planning/audit phase.
- Exactly one workstream carries `priority: primary` at a time — verified
  true after this change (`OPS-0001`'s own rule, unchanged).

**End-to-end allocation-check milestone:** recorded as WS-0003's terminal
acceptance milestone (per the blueprint §7), not as a new workstream —
defined now so future implementation phases have a fixed destination,
**not yet reached**, and not authorized to be built toward by this
decision alone.

**Register-only, non-originating:** exactly as `OPS-0001` established,
`operations/WORKSTREAMS.yaml` **coordinates** this priority and scope
decision; it does not **originate** it — the authority is this decision
record. A future session must still verify the register's cached fields
against live repository and GitHub state before acting on them, per
`OPS-0001`'s unchanged verify-before-transition rule.

**Supersession:** any future change to the architecture this blueprint
describes requires either a new, explicitly superseding version of the
blueprint or a new governance decision that explicitly supersedes this
one — never a silent edit to either after acceptance.

**No prior accepted decision is rewritten.** `GOV-0001`, `GOV-0002`,
`GOV-0003`, `MARGIN-0004`, `MARGIN-0005`, `TGT-0001`, `TGT-0002`,
`NUM-0001`, `ONTO-0001`, every `PI-####`/`AUTO-####` decision, and
`OPS-0001` itself are unchanged by this filing. This decision extends the
`OPS-0001` register pattern; it does not amend `OPS-0001`'s own text.

## Rationale

`OPS-0001` explicitly anticipated this exact sequence: WS-0002 "is not
scoped, designed, or authorized to execute... each requires its own future,
separate authorization before any work begins," and its `next_action`
stated plainly that "a future, separately filed decision must scope and
authorize the audit itself before any work begins." This decision is that
filing. Reprioritizing WS-0002 ahead of WS-0001 for the planning/audit
phase specifically — while leaving WS-0001's own research authority,
milestones, and next action completely untouched — follows `OPS-0001`'s own
stated escape hatch: WS-0002's blocker was "recommended... unless the
principal explicitly reprioritizes this workstream sooner." The principal
has now done exactly that, explicitly and in writing. Requiring an
independent audit before any implementation follows the same
verify-before-acting discipline Constitution §6 and `OPS-0001` both already
apply to external or lower-confidence claims — a prior Sonnet-only planning
pass, however thorough, is exactly the kind of claim that discipline exists
to check before it becomes the basis for building anything.

## Alternatives Considered

- **Authorize WS-0002 implementation directly, skipping a separate
  audit gate.** Rejected — the principal's own authorization explicitly
  requires the draft PR to remain unmerged until independently audited;
  skipping that would exceed the scope actually granted.
- **Leave WS-0001 as `priority: primary` and treat WS-0002 planning as a
  parallel, non-competing lane (the prior report's own recommendation).**
  Rejected as the operative choice here — superseded by the principal's
  explicit reprioritization instruction, which this decision implements
  precisely rather than substituting a different judgment for it.
- **Create a separate Fable-audit workstream, a separate end-to-end
  allocation-check workstream, a branch-cleanup workstream, a
  standalone SHA-refresh PR, or an Intelligence-expansion workstream.**
  Rejected — each fails the "demonstrated need" bar this register already
  applies; each is instead folded into an existing workstream's milestones
  or into this session's routine field verification, per the blueprint's
  §11.
- **Correct the BTC `holdings.yaml`/`CLAUDE.md`/`targets.yaml` factual
  conflict in this same PR.** Rejected — `CLAUDE.md` and `targets.yaml` are
  explicitly out of scope for this filing; the conflict is recorded (§3 of
  the blueprint) for a separately verified factual reconciliation before
  the next relevant allocation workflow change.
- **Treat the prior Sonnet report's conclusions as authoritative and copy
  them forward without reverification.** Rejected per the principal's
  explicit instruction — every material fact in the supporting blueprint
  was independently reverified against the live repository at this
  session's base commit before being restated.

## Consequences

Going forward: WS-0002 is the primary, active workstream for planning,
architecture, scope, sequencing, and independent audit — nothing more.
WS-0001 continues exactly as before in every respect except priority and
the recorded sequencing hold on its next implementation PR. WS-0003's
terminal milestone is now defined, still unreached, still not authorized
for implementation. No code, config, Intelligence record, or research file
changes as a result of this decision. This filing opens a **draft, unmerged**
pull request only — conversation approval authorizes the content of this
exact decision; it does not make the register changes or this document
effective, and does not authorize implementation, until (a) the independent
audit above is performed against the draft PR's head commit, (b) its
findings are reconciled, and (c) the principal separately authorizes an
implementation scope. The PR must not be marked ready for review or merged
by this session.
