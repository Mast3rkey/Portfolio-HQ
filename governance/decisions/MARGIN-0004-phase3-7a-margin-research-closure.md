---
decision_id: MARGIN-0004
date: 2026-07-21
status: Accepted
category: margin_doctrine
related_decisions: [MARGIN-0001, GOV-0001, GOV-0002]
supporting_artifact: docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md
---

## Context

`docs/MARGIN_DOCTRINE.md` (incorporated into the Constitution in full, per
`GOV-0002` level 1) states that whether leverage at the 1.8x level, or any
level, improves risk-adjusted outcomes "has never actually been tested,"
and promises a future dated update once the Margin Intelligence research
program produces that answer. That program — run under the names Track 2
and Phase 3 through Phase 7A — closed on 2026-07-17
(`docs/PHASE5B_GOVERNANCE_DECISION.md`, reaffirmed
`docs/PHASE6B_GOVERNANCE_REASSESSMENT.md`, restated
`docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`). Neither the doctrine page's
promised update, nor a CLAUDE.md Decisions Log entry, nor a
`governance/decisions/` record was ever produced for this closure.

`docs/PHASE5B_GOVERNANCE_DECISION.md` reached a real, evidence-grounded
verdict, but it is the research program's own internal governance
artifact: written 2026-07-17, one day before this repository's ADR
architecture (`GOV-0001`) was adopted, and never filed under
`governance/decisions/`, `decision_log.yaml`, or CLAUDE.md. It is not
illegitimate or meaningless — it is precise, evidence-grounded, and
consistent with every later phase that reaffirmed it — but it is not
indexed as a post-`GOV-0001` accepted decision file. This record performs
that indexing.

Separately, `decision_log.yaml`'s `MARGIN-0001` entry — the decision that
originally adopted the 1.8x cap — carries `status: pending_evidence` with
a comment naming this exact research program ("Track 2") as the open
question on whether the 1.8x level, or any level, is evidence-supported.
Per `governance/decisions/README.md` and `GOV-0001`, `decision_log.yaml` is
the frozen, unchanged historical ledger for pre-`GOV-0001` decisions and is
not edited by this or any future record. `MARGIN-0001` remains exactly as
written — an accurate record of the state of evidence and reasoning at the
time it was made. This record does not alter it; it supersedes only the
*present interpretation* of its pending characterization, by recording
that the research it anticipated has since run and closed.

## Decision

Formally records that the Phase 3–7A margin research program is **closed**,
and that its final governance verdict was to **maintain current doctrine**.

**What Phase 3 tested and found**, precisely (`docs/PHASE3_FINDINGS.md`
§§5–7, window 2021-06-01 to 2026-07-10, 63-ticker universe, hypothetical
$0-start simulation):

- **Unlevered baseline vs. simulated 1.8x leverage** (Scenario A vs. B):
  A — 30.01% annualized TWR, -22.41% MaxDD; B — 35.59% annualized TWR,
  -26.81% MaxDD. In this tested window, **1.8x produced higher annualized
  return and worse maximum drawdown than the unlevered baseline** — both
  gaps (+5.58pp TWR, -4.40pp MaxDD) cleared the pre-committed 1.0pp
  decision threshold. Leverage amplified the outcome in both directions,
  as expected from the doctrine's own mathematical-identity framing — this
  is a confirmation of that identity's mechanical operation, not a
  separate finding about whether 1.8x specifically is a good level.
- **Cap-level sweep, 1.2x/1.4x/1.6x/1.8x/2.0x** (Scenario C): results were
  **identical from 1.4x through 2.0x** (35.59% TWR / -26.81% MaxDD at each
  of 1.4x, 1.6x, 1.8x, and 2.0x) — only 1.2x showed a measurably different
  (lower) result. The cap ceased binding above roughly 1.4x because this
  account's own simulated, deposit-driven margin demand never asked for
  more room than that within the tested window. **The sweep therefore did
  not establish the safety or superiority of 1.6x, 1.8x, or 2.0x under a
  genuinely stressed demand path** — it reports that the cap's specific
  level didn't matter *in this window*, not that any of those levels would
  hold up against demand this window never generated.
- **Repayment-policy line** (Model B profit-harvest, Model C risk-reset,
  carried through Phases 3G, 4A, transaction-cost/tax/stress-regime
  sensitivity, 6A FIFO tax-lot refinement, 7A execution-reality
  assessment): found a real, measurable, monotonic return/drawdown effect
  (Model B) that survived transaction-cost and FIFO-tax-lot sensitivity,
  but the program retained, unresolved, the same five implementation
  blockers named at Phase 5's decision gate throughout every subsequent
  phase: real tax-lot/cost-basis/jurisdiction data, real execution/
  slippage modeling, real broker margin-call/liquidation mechanics, a
  designed human-override workflow, and a market regime this project's
  2021–2026 window does not contain.

**What this means, governance-wise:** the evidence **did not establish an
optimal leverage level, did not establish severe-stress survivability at
any level above 1.4x, and did not support a production or policy change**.
The 1.8x leverage cap and 30% buffer floor remain unchanged as a result —
**because the evidence did not justify a governed change, not because the
numerical level is permanently immune to evidence.**

**No new repayment logic, deployment logic, market-regime leverage,
predictive leverage, discretionary leverage, or Intelligence-controlled
leverage is authorized by this record.** No allocator, `targets.yaml`,
`holdings.yaml`, or `margin_state.py` behavior changes.

`MARGIN-0001` remains untouched in `decision_log.yaml` as an accurate
historical record of the decision and reasoning made on 2026-07-13,
including its `pending_evidence` status, which correctly described the
state of evidence at that time. This record supersedes that pending
characterization **only for present interpretation** — going forward, the
question `MARGIN-0001` flagged as open (whether Track 2 would find the
1.8x level, or any level, evidence-supported) is answered: Track 2 ran,
closed, and the evidence obtained did not justify changing the cap.

**Reopening the numerical-level question** requires fundamentally
different evidence than more simulation on the same 2021–2026 window can
produce — real historical account data, a genuinely severe stress period,
or real broker mechanics data — **and** a new, separately governed
decision. Ordinary parameter relitigation of this question is closed.

## Rationale

This repository draws a explicit line between two different kinds of
claims about margin, and this decision does not blur it:

- **Margin is not alpha and not a timing mechanism** — a mathematical
  identity (leverage multiplies existing returns; it does not generate
  edge), not an empirical claim, and not what this decision addresses.
  This remains fixed doctrine, unaffected by any backtest.
- **Whether carrying leverage at a particular numerical level improves
  risk-adjusted outcomes is an empirical question.** Phase 3 tested that
  question, within a bounded 2021–2026 historical simulation, and
  characterized it precisely: leverage amplified both return and drawdown
  as the identity predicts, and the cap-level sweep could not discriminate
  among 1.4x–2.0x because demand in this window never stressed it that
  far. The evidence neither proved 1.8x optimal nor proved any other level
  safe — it bounded the question without resolving it, which is why the
  governed result was no change, not a re-derivation of the cap from this
  evidence.

`docs/MARGIN_DOCTRINE.md` itself specifies the update mechanism this
decision fulfills (§"How this doctrine gets tested"): a dated entry
recording the research program's answer, the same way every other closed
backtest question is logged. No principle in the doctrine changes as a
result — the cap and floor are retained because this round of evidence did
not clear the bar for changing them, not because the question is
foreclosed from ever being revisited under different evidence. That
distinction is why this is a **doctrine clarification and historical
reconciliation**, not a **constitutional amendment**: Constitution §7
requires stating "what principle is changing and why the prior version no
longer holds," and nothing here meets that bar.

## Alternatives Considered

- **Characterize the numerical-level question as permanently
  doctrine-fixed, immune to any future backtest.** Rejected — that would
  misstate an empirical question as a matter of doctrine identical in kind
  to "margin is not alpha." The cap's specific level is empirically
  testable in principle; this round of evidence simply did not clear the
  bar for changing it. Overstating this as permanent immunity would itself
  be an inaccurate claim this decision exists to avoid introducing.
- **Treat this as a constitutional amendment under Constitution §7.**
  Rejected — no principle changes; the cap and floor are unchanged, and
  the reason they are unchanged is evidentiary insufficiency, not a
  doctrine restatement.
- **Characterize `docs/PHASE5B_GOVERNANCE_DECISION.md` as illegitimate or
  retroactively void for having never been formally filed.** Rejected —
  its reasoning is sound, evidence-grounded, and reaffirmed by every
  subsequent phase; the actual gap is indexing, not legitimacy. This
  record closes that indexing gap rather than relitigating the underlying
  decision.
- **Edit `decision_log.yaml`'s `MARGIN-0001` entry directly (status value
  or inline comment).** Rejected per explicit repository authority —
  `decision_log.yaml` is frozen as the unchanged historical ledger for
  pre-`GOV-0001` decisions (`GOV-0001`, `governance/decisions/README.md`).
  `MARGIN-0001` stays exactly as written; this record supersedes its
  pending characterization for present interpretation only, without
  touching the file itself.
- **Archive the Phase 3–7A documents now.** Out of scope — `GOV-0001`
  already identified this as a separate, larger, cross-reference-heavy
  task and explicitly left it open; this decision does not expand scope to
  cover it.

## Consequences

`docs/MARGIN_DOCTRINE.md` no longer claims leverage-at-a-level is
untested, and no longer carries an unfulfilled forward promise — both
stale passages are corrected to record this closure. CLAUDE.md's Decisions
Log gains one entry indexing this decision. `governance/decisions.yaml`
gains one new row.

**Explicitly unchanged:** the 1.8x leverage cap, the 30% buffer floor, the
no-margin-timing rule, `allocate.py`, `targets.yaml`, `holdings.yaml`,
`margin_state.py`, `margin_simulation.py`, every prior Phase 3–7A
document's own recorded conclusion, `decision_log.yaml` (including
`MARGIN-0001`'s scalar values, comments, and formatting, byte-for-byte),
and the Constitution itself.

**Explicitly not authorized:** any new repayment logic, deployment logic,
market-regime leverage, predictive leverage, discretionary leverage, or
Intelligence-controlled leverage; any allocator or production behavior
change.

Reopening the numerical-level question in the future requires
fundamentally different evidence than this program's simulated
2021–2026 window can produce, and its own new, separately governed
decision — not an ordinary re-run of the same backtest.

This decision becomes effective only when implemented via a reviewed pull
request that merges to `main` — filing it on a branch does not make it
effective, per the same rule `GOV-0002` established for itself.
