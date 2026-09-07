---
decision_id: MARGIN-0004
date: 2026-07-21
status: Accepted
category: margin_doctrine
related_decisions: [GOV-0003, MARGIN-0001, MARGIN-0002, MARGIN-0003]
supporting_artifact: docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md
---

## Context

`governance/decisions/GOV-0003-margin-conditional-research-permitted.md`
narrowed Constitution §3/§4 to permit bounded, evidence-gated research
into conditional margin deployment/repayment rules, and named "a future,
separate, revised MARGIN-0004 workstream" as the vehicle to reconcile the
already-closed Phase 3–7A margin research program's closure
(`docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`) against that narrowing. A
companion PR (#117) had earlier proposed a MARGIN-0004 entry recording
that closure under the doctrine's prior, absolute framing; GOV-0003
closed PR #117 unmerged (branch preserved, untouched by this decision)
specifically because it argued from language this decision now
supersedes. This decision is that reconciliation, and only that
reconciliation — it does not establish any new research framework,
shared data model, or charter.

GOV-0003's own Consequences section explicitly reserved two passages in
`docs/MARGIN_DOCTRINE.md` — "The system's job, precisely" bullet 1, and
the closing "How this doctrine gets tested, and how it can change"
section — "exactly as they read today, for the future, separate,
revised MARGIN-0004 workstream." Both passages describe the
margin-drag-vs-unlevered question as untested ("this has never actually
been tested... Phase 1... exists specifically to close this gap") and
promise a future dated update "once Phase 1 produces that answer." Phase
3–7A's Test A produced the evidence that section anticipated, and
`docs/PHASE5B_GOVERNANCE_DECISION.md` recorded what that evidence
justified for production — but neither fact was ever written back into
these two passages, leaving them stale relative to the repository's own
history.

## Decision

**A. What Phase 3–7A tested** (preserved without reclassification and
summarized below; `docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md` remains the
canonical source — this entry summarizes, it does not replace or
duplicate it): margin-drag-vs-unlevered
baseline (+5.58pp TWR / -4.40pp MaxDD, a scenario configured with a
1.8x leverage cap versus an unlevered baseline, hypothetical/
simulated, 2021–2026 window); a 1.2x–2.0x leverage-level sweep (flat
above 1.4x in this window); Model B profit-harvest repayment (monotonic
across repay_fraction 10/25/50%: -0.98/-2.32/-3.56pp TWR, +0.97/+2.07/
+3.16pp MaxDD); Model C risk-reset repayment (zero triggers at 15%/20%
drawdown thresholds); transaction-cost sensitivity (immaterial at
0/5/15bps); tax-treatment sensitivity (material at repay_fraction
25%/50% under FIFO-realistic accounting); stress-regime timing (Model B
structurally under-fires in real detected stress windows); concentration
× margin interaction (Phase 4A: "Evidence inconclusive" under its own
pre-committed gate); and execution-reality/broker-mechanics research
(Phase 7A: two real, unmodeled brokerage mechanisms confirmed — FINRA
Rule 4210(g)(8) concentration-triggered maintenance escalation, and
no-notice forced liquidation).

**B. What Phase 3–7A did not test** (excluded by its own stated charter,
not a gap discovered later): any conditional or timing-based deployment
rule, account-state- or market-state-keyed; any repayment rule keyed to
margin risk-state (Elevated/Forced) rather than pure profit
high-water-mark; recurring or interrupted deposit-cadence interaction
with any margin policy; asset-eligibility (which holdings may receive
margin-funded capital); initial-margin, maintenance-margin,
buying-power, and liquidation-mechanics modeled as distinct concepts
rather than one leverage-cap clip; a financing-duration metric
independent of interest-cost totals; and dividend cash flows as a
repayment-capacity input — Phase 3–7A did not model dividend cash flows
as a repayment-capacity input (a statement about this research program's
charter, not a claim that no dividend information appears anywhere else
in this repository for other purposes).

**C. What GOV-0003 changed:** it did not invalidate, reopen, or
retroactively reclassify any Phase 3–7A finding or verdict — the
program's scope boundary (excluding conditional/timing-based deployment)
was a correct statement of its own charter, not an error. GOV-0003
opened a new, narrower, and previously out-of-charter question: whether
a rules-based, pre-registered, evidence-gated conditional deployment or
repayment rule can outperform the current fixed posture — researchable
only under its own future, separate charter, adoptable only through its
own future, separate governance decision.

**D. What remains unchanged:** the 1.8x leverage cap; the 30% buffer
floor; recommendation-only, manual execution; no live signal, no
opportunity map, no precomputed recommendation; no allocator behavior
change; no code change; `targets.yaml`, `holdings.yaml`, `allocate.py`,
`margin_state.py`, `margin_simulation.py`, `alpaca_client.py`, every test
file, `decision_log.yaml`, and every Phase 3–7A evidence artifact. Both
numerical thresholds were originally adopted as provisional governance
guardrails, not derived from this or any backtest, and remaining
unchanged in this decision does not mean either has been empirically
proven safe, optimal, sufficient, or permanently immune from
reconsideration — changing either threshold, if ever proposed, requires
its own future, separate, explicitly governed research and approval, and
this decision neither begins nor authorizes that research.

## Rationale

Constitution §6 requires verifying claims before acting on them, and by
the same logic this repository has already applied to external review
claims, a repository's own doctrine text should stay consistent with
what the repository's own settled history actually shows. Leaving "this
has never actually been tested" standing after Phase 3–7A generated the
evidence the doctrine had promised to record — evidence `docs/
PHASE5B_GOVERNANCE_DECISION.md` went on to evaluate, and on which basis
it maintained the then-current production posture — and leaving a
promised dated update unwritten after that evidence already existed, is
stale institutional memory, not a live claim. Correcting it is a
documentation-accuracy act, not a new research or policy decision, and
not a claim that the mixed evidence amounts to a simple proof: nothing
about the 1.8x cap, the 30% floor, or any production behavior changes as
a result.

## Alternatives Considered

- **Leave both `docs/MARGIN_DOCTRINE.md` passages as-is, since GOV-0003
  already narrowed the doctrine elsewhere.** Rejected — GOV-0003
  explicitly reserved these two passages for this decision rather than
  editing them itself, precisely because they needed the closure record
  this decision provides, not just the timing-principle narrowing
  GOV-0003 supplied.
- **Combine this reconciliation with freezing a new Capital Efficiency
  Framework in one decision.** Rejected on prior review — reconciling a
  finished program and opening a new research domain are different
  governance acts with different authority requirements; combining them
  risks the new domain inheriting authorization it never separately
  earned. The framework, if pursued, is its own future, separate
  decision.
- **Rewrite the 2026-07-13 CLAUDE.md "Margin doctrine revised" entry in
  place.** Rejected — that entry's substance (rejecting discretionary
  margin-timing) remains true and unedited; a new, dated, linked entry
  in the same Decisions Log is the correct mechanism, consistent with
  how every other clarifying addition in this repository's history has
  been handled.

## Consequences

**This decision authorizes exactly:**
- The reconciliation record in A–D above.
- The correction to `docs/MARGIN_DOCTRINE.md`'s "The system's job,
  precisely" bullet 1.
- The addition to `docs/MARGIN_DOCTRINE.md`'s "How this doctrine gets
  tested, and how it can change" closing section.
- One new, dated CLAUDE.md Decisions Log entry, appended after the
  existing GOV-0003 entry, that does not rewrite or erase the original
  2026-07-13 entry.
- The `governance/decisions.yaml` index entry for this ADR.

**This decision explicitly withholds:**
- CAPITAL-0001 or any Capital Efficiency Framework freeze.
- Any shared data-model freeze.
- Margin Deployment Research or Margin Repayment Research charters.
- Any future decision-ID reservation beyond this one.
- Any simulation run or new metric.
- Any broker-observation infrastructure.
- Any allocator behavior, `targets.yaml`, or `holdings.yaml` change.
- Any live recommendation.

No new non-governance artifact, code file, research output, or
operational data file is authorized.

Explicitly unchanged: the 1.8x leverage cap, the 30% buffer floor,
`decision_log.yaml` (byte-identical), `targets.yaml`, `holdings.yaml`,
`allocate.py`, `margin_state.py`, `margin_simulation.py`,
`alpaca_client.py`, every existing test, every Phase 3–7A artifact,
`intelligence/`, `reports/`.

This decision becomes effective only when its implementing PR merges to
`main`.
