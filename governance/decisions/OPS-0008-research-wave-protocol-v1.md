---
decision_id: OPS-0008
date: 2026-07-26
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0006, OPS-0007, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027]
supporting_artifact: null
---

## Context

A separate, explicitly bounded proposal-only session (this repository's WS-0005 Research Wave
Protocol design and zero-based Batch 5 scope review) audited the lifecycle every completed
Milestone 3 batch actually used. Finding, independently verified against live GitHub state at that
session's preflight: Batch 2 (MU, SKHY) consumed governance PR #157, implementation PR #158, and a
dedicated register-synchronization PR #159 that changed nothing but `operations/WORKSTREAMS.yaml`
prose recording PR #158's already-complete merge and post-merge verification. Batch 3 (AVGO, AMD,
MRVL, INTC) followed the same three-PR shape (#160, #161, #163/#164 for the architecture-package
reconciliation chain). Batch 4 (ETN, VRT, PWR) used governance PR #165, implementation PR #166 (with
two in-PR correction passes), and a fourth, dedicated post-merge reconciliation PR #167 that again
changed nothing but retained-artifact placement and register prose. In every case the
register-synchronization PR was reviewed, accepted, and merged — proper process, no defect — but it
existed solely to record a fact (the prior PR's merge and post-merge verification), not to change
research substance. That is proportional overhead per batch, not a batch-size effect: a 5-6-company
batch under the same shape costs the same fixed round-trips for materially more coverage.

Separately, Batch 4's implementation PR (#166) required a mid-flight correction: an independent
exact-head review found a `PI-0026` §D stop-condition violation — research had proceeded to
completion after determining no primary source could be opened, rather than stopping for principal
direction. The correction that followed required a one-time, ad hoc principal authorization for a
specific evidence-recovery method (a retained GPT-5.6 Thinking primary-source audit). That method
worked, and the retained artifacts (`governance/audits/PR166_PRIMARY_SOURCE_AUDIT_20260726.md`,
`governance/audits/PR166_CORRECTED_HEAD_REVIEW_20260726.md`) are exactly the kind of evidence this
repository already values — but requiring a fresh, one-off principal sign-off for the same recovery
pattern on every future batch is the same category of avoidable per-batch friction as the
reconciliation-PR pattern above, given that Batch 1, Batch 2, and Batch 4 have now each independently
hit blocked primary-source access as their normal, expected condition, not an edge case.

The principal reviewed that session's Research Wave Protocol v1 proposal, obtained an independent
review from GPT-5.6 Thinking, and approved the protocol with four amendments: (1) file the protocol
and the next batch authorization as two separate decision documents in one governance PR, rather
than one combined filing; (2) adopt a default two-PR lifecycle (authorization PR, implementation PR)
followed by mandatory but read-only post-merge verification, with no routine third
reconciliation PR; (3) make the source-readiness gate a mandatory stop-before-drafting checkpoint,
with a standing (not per-batch) pre-authorization for evidence-recovery via an eligible independent
reviewer when Claude's own session access is blocked; (4) a specific, narrower Batch 5 scope
(addressed in `PI-0027`, filed alongside this decision, not restated here).

**Preflight for this filing** (independently verified, not assumed): `origin/main` fetched and
pruned; local and remote `main` confirmed identical at `1aba3e74d3847aa278b774f3b0956c786b6ee480`
(the merge commit of PR #167, itself confirmed merged via the GitHub API — state `closed`,
`merged: true`, `merged_at: 2026-07-26T18:42:15Z`); zero open pull requests exist; working tree
clean; `governance/decisions.yaml` carries exactly 36 entries, highest `PI-####` is `PI-0026`,
highest `OPS-####` is `OPS-0007` — confirming `OPS-0008` as the next unused number in its series.
`intelligence_validator.py` run directly against `intelligence/companies/` independently confirms 20
files, all valid. This decision creates no Company Intelligence record, comparison artifact,
freshness row, or research finding of any kind, and reviews, corrects, marks ready, or merges
nothing beyond itself.

## Decision

**OPS-0008 adopts the Research Wave Protocol v1, prospectively, for WS-0005 Milestone 3 batches
authorized from this decision's own merge forward.** It does not reopen, reclassify, or apply any
new requirement retroactively to Batches 1-4 (`PI-0023`/`PI-0024`/`PI-0025`/`PI-0026`), each of which
remains valid and complete exactly as reviewed, accepted, and merged under the discipline in force
when it was filed. This decision itself creates no Company Intelligence record, comparison
artifact, freshness row, test, or validator, and authorizes no research. Batch 5's specific company
scope is authorized separately, in `PI-0027`, filed in the same governance PR as this decision but
kept as its own file per the principal's first amendment.

### 1. Default wave size and coherence requirement

Default wave size for a future Milestone 3 batch is **5-6 companies**. A smaller wave is permitted
only when: primary-source accessibility is unusually weak across the candidate group; a company's
complexity (multi-segment conglomerate, foreign-issuer structure) would make combining it with
others unsafe for review quality; the candidate companies are not, on closer analysis, genuinely
coherent; or the review surface at 5-6 would be unsafe for a single implementation PR to carry
responsibly. A larger wave is never chosen merely to move faster.

Every wave requires a documented common economic mechanism — not merely the same GICS sector label,
the same current tier, the same correlated-cluster-cap membership, or similar historical price
behavior (`PI-0026` §C.13 already had to make exactly this argument explicitly for `power_infra`;
this section makes that requirement standing rather than ad hoc). The batch's own governance
authorization must state: business-function similarities and differences among the companies;
value-chain positions; shared risks and dependencies; substitutes; which exposure is duplicated
across the batch and which is genuinely distinct per company.

### 2. Source-readiness gate — mandatory stop-before-drafting, with standing evidence-recovery pre-authorization

Before any company-record content is drafted, the implementing session must attempt direct
primary-source access for every company in the batch (SEC Form 10-K/10-Q/8-K or the foreign-issuer
equivalent; official earnings releases and call materials; official investor presentations; relevant
regulatory/government documents) and produce a source-access manifest per company: exact
document/URL/date targeted, access status, and exact sections needed.

**If primary-source access is blocked for one or more companies in the batch, the implementing
session must stop before drafting substantive economic content for those companies** — it may not
proceed to draft on secondary or WebSearch-only evidence and rely on a later correction pass to fix
it, the pattern that produced the `PI-0026` §D violation in Batch 4. This reverses the
draft-then-correct sequence Batches 1, 2, and 4 each actually followed.

**Standing pre-authorization for evidence recovery**: when primary access is blocked, the
implementing session may engage an eligible independent reviewer (per `OPS-0007` §1's capability
standard — Fable, an independent ChatGPT/GPT-5.6-Thinking-class session, or any other reviewer
meeting every §1 requirement) to perform a primary-source evidence-recovery audit for the blocked
companies, and may incorporate that audit's findings before resuming drafting. This recovery method
is now standing and pre-authorized by this decision — it does not require a fresh, one-off principal
authorization for each future batch that needs it, unlike the ad hoc authorization Batch 4 required.
It remains bounded: exactly the batch's own named companies; sourcing and factual recovery only, no
tier/target/cluster/ranking/margin/allocator authority of any kind; the audit is retained verbatim
under `governance/audits/` per the existing convention; every fact recovered this way is still
subject to the same fact/inference/uncertainty/source-type/access-status separation discipline as
every other requirement in this protocol.

If even an evidence-recovery pass cannot establish sufficient primary evidence for a company, the
existing `PI-0023`-`PI-0026` §D rule still applies unchanged: try reasonable official alternatives,
then stop, disclose exactly what failed, and return for explicit principal direction. This gate
authorizes a recovery method — it does not authorize silently proceeding on secondary evidence alone
when even recovery fails.

### 3. Parallel research / central integration

Parallel per-company evidence collection is permitted. One integrating author or session must
reconcile conflicting facts, apply the schema consistently, separate fact from inference from
uncertainty from judgment, preserve disconfirming evidence, write every company record and the wave
comparison artifact, and confirm no company in the authorized batch is silently omitted.

### 4. Implementation lifecycle — default two-PR lifecycle, read-only post-merge verification, no routine third PR

Default lifecycle for a future Milestone 3 batch: **(1)** one governance-authorization PR (a
`PI-####` batch decision) that creates no research content itself; **(2)** one implementation PR
carrying the complete company/theme content through its own full cycle — draft, independent
exact-head review, bounded correction if a material (Blocking or Major) finding survives, exact-head
delta re-review, explicit principal acceptance, merge.

After the implementation PR merges, **mandatory post-merge verification** — ancestry (reviewed head
is the merge commit's direct parent), scope (merged diff matches exactly the authorized file list),
validator and full-suite re-run, and protected-path byte-identity confirmation — must still be
performed. **By default this verification is read-only and does not require its own dedicated
reconciliation PR.** It is instead recorded as part of: **(a)** the Preflight/Context section of the
next batch's own governance-authorization filing — the exact pattern `PI-0024`, `PI-0025`, and
`PI-0026` already used to confirm the prior batch's merge state before proceeding — or **(b)**, if no
next batch is imminent within a reasonable window, a minimal `operations/WORKSTREAMS.yaml` update
bundled into the next PR that already needs to touch that file for another reason. **A dedicated
reconciliation PR, filed solely to record that a prior PR merged and was verified, is the exception,
not the routine default** — it is filed only when post-merge verification actually discovers a
material factual discrepancy requiring correction.

This does not weaken any verification substance — every check Batches 1-4's reconciliation PRs
performed still must be performed and still must be recorded before a batch's Company Intelligence
is treated as PROVISIONAL under `OPS-0007` §3 (which independently requires post-merge ancestry,
scope, validator, and test re-verification with `operations/WORKSTREAMS.yaml` synchronized — that
requirement is unchanged by this decision). What changes is only the packaging: recorded, not
re-proven through a dedicated pull request.

### 5. Review standard

Unchanged from `OPS-0007` §1's twelve-point capability-based standard, adopted here by reference:
independence from authorship; exact-head anchoring; sufficient repository/controlling-authority
access; sufficient web/research capability; primary-source-inspection attempts with disclosed
blocks; fact/inference/evidence-type separation; validator/test verification; severity
classification; retained attribution (GitHub review or `governance/audits/` artifact); disclosure of
model/session/access-limits/head/verdict; bounded correction plus exact-head re-review for material
findings; explicit principal acceptance before merge, at the exact head. No weakening of any of the
twelve points.

### 6. Acceptance standard

Unchanged from existing practice, restated for completeness: primary-source discipline; claim-level
provenance; thesis-break conditions; current-policy baseline disclosed as historical only, never as
research evidence; next-best-capital-alternative discussion where applicable; margin-relevant
factual evidence only, never a leverage or deployment recommendation; external-opportunity leads
disclosed as unauthorized future candidates only; full validators and tests passing; independent
exact-head review; explicit principal approval; post-merge verification per §4 above.

### 7. Retained evidence

`governance/audits/` remains the retention convention for full review and audit artifacts. Future
register entries should reference a retained artifact by path and checksum rather than re-pasting its
full body into `operations/WORKSTREAMS.yaml` prose — the register's WS-0005 entry has grown very
large from doing exactly that across Batches 2-4; referencing, not restating, keeps future
register-sync edits smaller without losing provenance.

### 8. Tooling opportunity — proposal only, not authorized here

A future, narrow, read-only tool that mechanically assembles exact-head SHA, diff scope against an
authorized-file list, check-run conclusion, protected-path byte-identity comparison, and decision-
registry filed-versus-indexed counts — the handful of facts every batch PR body in this history
hand-computes and restates — is a plausible efficiency candidate for research substance, not review
substance, and is not authorized, scoped, or built by this decision. Any such tool requires its own
future, separate proposal and authorization.

### 9. Stopping condition

This protocol should not be made more complex than this decision states. If a future batch requires
a third, dedicated reconciliation PR because post-merge verification finds a genuine material
discrepancy, that is the exception working correctly — it is not, by itself, grounds to add a
standing fourth process step. If the default two-PR lifecycle needs a third PR on two or more
consecutive batches for reasons other than a genuine material discrepancy, or if an eligible reviewer
flags a coherence or evidence-quality regression traceable to this protocol, that is the trigger to
revisit this decision — via its own future governance filing, not a silent drift back toward the
prior four-PR pattern.

### 10. Governance package scope (this filing)

This decision, filed in the same governance PR as `PI-0027` but as its own separate file per the
principal's amendment, touches exactly: this `OPS-0008` file; `governance/decisions.yaml` (index
regeneration — two new entries, `OPS-0008` and `PI-0027`); `operations/WORKSTREAMS.yaml` (WS-0005
Milestone 3 gate: record both this protocol's adoption and `PI-0027`'s batch authorization, using
only `OPS-0001`'s existing schema and status vocabulary); `CLAUDE.md` (two Decisions Log entries, one
per decision). **No other file is touched by this governance filing.** No Company Intelligence
record, comparison artifact, freshness row, or test/validator file is created or authorized to be
created by this filing.

### 11. Effectiveness, review, and merge gates

This governance PR (carrying both this decision and `PI-0027`) must remain in draft state, gain its
own independent eligible review anchored to its exact head per `OPS-0007` §1, complete any required
bounded correction and exact-head re-review, and receive explicit principal acceptance before it may
be marked ready or merged. Nothing in this decision becomes effective until the PR merges to `main`.
This decision does not itself authorize Batch 5 research implementation — that requires `PI-0027`
(in the same PR) to also merge, and even then only a later, separate implementation PR — not opened
by this filing — may begin, itself gated on its own review cycle under §§2-6 above.

### 12. Hard boundaries

The following boundaries were previously stated only by cross-reference to `OPS-0006`/`OPS-0007`
and to this decision's own Consequences section. They are restated here as this protocol's own
explicit, standalone operative limits — added following an independent exact-head review that
found relying on cross-reference alone insufficient for a durable, prospective protocol document —
so that no future batch session can read this protocol as silently granting any of the following:

- **No scoring, ranking, composite index, or automatic aggregation** of any company, batch, or
  research finding, under any interpretation of this protocol.
- **No automatic tier, target, role, cluster, cap, holdings, allocation, margin, or execution
  recommendation** may be generated or implied by any wave conducted under this protocol.
- **No Intelligence output produced under this protocol may directly control allocator or margin
  behavior** — Company/Theme Intelligence remains advisory input to human judgment only, never a
  mechanically load-bearing input to `allocate.py`, `margin_state.py`, or any production path.
- **No trade or order capability** exists, or is created, by any wave conducted under this
  protocol, its source-readiness gate, its evidence-recovery method, or its review cycle.
- **Every future research wave still requires its own separate, explicit, later governance
  decision** naming its own companies — adopting this protocol does not itself authorize any wave,
  including a first, second, or any subsequent one; a wave's own `PI-####` authorization remains
  the sole source of that wave's scope, exactly as `OPS-0006` §5 already requires.
- **No Milestone 4 (relationship mapping), any later WS-0005 milestone, or any `OPS-0007` §8 step-I
  authority is created by this protocol** — this decision governs only the shape of future
  Milestone 3 waves; it neither advances nor authorizes any milestone or step beyond Milestone 3.
- **An evidence-recovery session engaged under §2's standing pre-authorization has sourcing and
  factual-recovery authority only** — it gains no tier, target, cluster, ranking, margin, allocator,
  or other policy authority of any kind, exactly as §2 already states and is restated here as a
  standalone boundary for emphasis.
- **Stale, incomplete, or inaccessible evidence may require disclosure, a pause in drafting, or
  abstention from a conclusion — never an automatic policy change.** Consistent with `OPS-0006`
  §14's evidence-validity boundary, staleness or an evidentiary gap discovered under this protocol
  is never itself a trigger for a tier, target, trim, exit, or margin-policy action.

These boundaries narrow nothing already stated elsewhere in this protocol or in `OPS-0006`/
`OPS-0007` — they make explicit, as this protocol's own standalone text, limits that previously
existed only by inference or cross-reference.

## Rationale

**Why a default two-PR lifecycle with read-only post-merge verification, not three or four.** The
audit in Context above shows every completed batch's third (or fourth) PR existed to record a fact
already true at the prior PR's merge — not to change anything. `OPS-0007` §3's PROVISIONAL
definition already requires post-merge verification to happen; nothing in this repository's doctrine
required it to happen via its own dedicated PR. Folding that verification into the next filing that
already needs to touch the register removes a fixed, proportional cost from every batch without
removing the verification itself.

**Why stop-before-drafting, not draft-then-correct.** Batch 4's own correction history is the direct
evidence: proceeding to draft under blocked access, then correcting after an independent review
caught the §D violation, cost a full extra review-correction-re-review cycle inside PR #166. Stopping
before drafting turns a late, expensive correction into an early, cheap manifest check — the same
economic logic as source-readiness gates in any other engineering-review discipline.

**Why standing pre-authorization for evidence recovery, not a fresh sign-off each time.** Batch 1,
Batch 2, and Batch 4 each independently hit the same condition (primary-source domains blocked at the
network/proxy level for this session). Requiring a new, ad hoc principal authorization for the same
recovery method every time it recurs is friction with no additional safeguard value — the guardrails
that actually matter (eligible-reviewer capability per `OPS-0007` §1, bounded scope to the batch's
own named companies, retained artifacts, no tier/target/ranking authority) are preserved unchanged
and apply whether the authorization is standing or ad hoc.

**Why two separate decision files in one PR, not one combined filing.** The principal's own
amendment, following GPT-5.6 Thinking's review: a protocol adopted prospectively for all future
batches and a single batch's company-specific scope are different kinds of decisions with different
future amendment paths — a later batch may need to reference or narrowly supersede one without
touching the other, which is cleaner with `governance/decisions/README.md`'s own one-file-per-
decision convention followed literally, even when two decisions are filed and reviewed together.

## Alternatives Considered

- **Keep the observed three-to-four-PR-per-batch pattern.** Rejected — demonstrated proportional
  overhead with no corresponding quality benefit; every dedicated reconciliation PR in this
  repository's history recorded a fact, it never changed one.
- **Keep draft-then-correct for blocked primary sources.** Rejected — Batch 4's own correction
  history is direct evidence of its cost; stopping before drafting is strictly cheaper for the same
  outcome.
- **Require a fresh principal authorization for every future evidence-recovery instance.** Rejected
  — the principal's own explicit direction, and the repeated (not edge-case) nature of blocked
  primary-source access across three of four completed batches; the safeguards that matter are
  preserved through `OPS-0007` §1 eligibility and bounded scope, not through per-instance sign-off.
- **Combine the protocol and Batch 5's scope into one filing** (this session's original proposal).
  Rejected per the principal's explicit amendment, following GPT-5.6 Thinking's review — two separate
  files, reviewed together in one PR, better preserves independent future amendability.
- **Eliminate post-merge verification's substance, not just its packaging.** Rejected — never
  proposed and explicitly not what this decision does; §4 states the verification itself is
  unchanged, only whether it needs its own PR.

## Consequences

**Authorized, effective on this decision's merge:** the Research Wave Protocol v1 described in §§1-9
above, governing WS-0005 Milestone 3 batches authorized from this point forward. `PI-0027` (Batch 5)
is authorized separately, in its own file, filed in this same governance PR.

**Unchanged by this decision:** `PI-0023`, `PI-0024`, `PI-0025`, and `PI-0026`, each `status:
Accepted` and unedited, and each batch's own completed lifecycle and PROVISIONAL status; `OPS-0007`'s
twelve-point review standard and five-part PROVISIONAL definition; every existing tier, target, role,
cluster, cap, and holding in `targets.yaml`/`holdings.yaml`; `allocate.py`, `margin_state.py`, every
existing Company/Theme Intelligence record, and every existing test; the 1.8x leverage cap and 30%
buffer floor; `OPS-0006`'s Milestone 4-9 authorization boundary; `MARGIN-0005`'s research charter and
trial ceiling.

**No research has been conducted, and no Company Intelligence record, comparison artifact, or
freshness row is created by this decision.** A future Milestone 3 batch proceeds under this protocol
only once its own separate governance authorization (starting with `PI-0027`, filed alongside this
decision) is itself independently reviewed, principal-accepted, and merged.
