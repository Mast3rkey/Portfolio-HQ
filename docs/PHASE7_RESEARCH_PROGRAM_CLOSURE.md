# Phase 7 — Research Program Closure

> **⚠️ Executive summary, not a new evidence document.** This document runs no simulation, computes no new figure, and changes no code. Every finding cited below is quoted from an already-committed source. It exists to let a future reader understand the entire margin research program without reading the 40+ documents it produced.

_Written 2026-07-17. Closes the Margin Intelligence Engine research program that ran across Phases 3–7A. Documentation only — no code, no production files, no doctrine change._

---

## 1. Original research questions

The program began with one question, stated across `docs/PHASE2_IMPLEMENTATION_PLAN.md` and `docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md`: **should this account's margin usage follow a proactive repayment policy, and if so, does the evidence support one?** That question fanned out, phase by phase, into a defined set of sub-questions, each opened only when a prior answer surfaced it:

1. Do simulated repayment policies (Model B: profit harvest; Model C: risk reset) change return/drawdown outcomes at all? (Phase 3)
2. Is any observed effect sensitive to the policy's own parameters? (Phase 3G)
3. Does concentration change the risk profile of margin usage? (Phase 4A)
4. Does the observed Model B effect survive real-world friction — transaction costs, taxes, and stress-period timing? (Phase 3/6A cost, tax, and stress passes)
5. Given all of that evidence, what — if anything — should change in production? (Phase 5)
6. Does a more realistic tax-lot model change the answer? (Phase 6A)
7. Does the simulator's execution model correspond to real brokerage mechanics? (Phase 7A)

## 2. Questions answered

- **Does Model B change outcomes?** Yes. First observed in Phase 3E (repay_fraction=0.25: 33.28% TWR vs. 35.59% control, −2.32pp; −24.74% MaxDD vs. −26.81%, +2.07pp improvement), confirmed monotonic across 10%/25%/50% in Phase 3G.
- **Do transaction costs erase the effect?** No. Erosion at 0/5/15bps was three orders of magnitude smaller than the observed gaps, at every `repay_fraction` (`docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md`).
- **Does repayment activity cluster during market stress?** No — the opposite. Model B's high-water-mark trigger structurally favors calm/rising periods; only 5.9–6.9% of repayment dollars fell inside detected real stress windows against a 12.2% base rate (`docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md`).
- **Does the QQQ-below-200-EMA regime gate or the 200-SMA trend gate help?** No — both closed with "no change/drop the gate" verdicts under this project's pre-committed-threshold discipline (`docs/PHASE4_READINESS_REVIEW.md`'s cited backtests), though these predate and are outside the Phase 3–7A margin program proper.
- **Does the T1/T2 concentration ceiling's return case justify a trim rule?** No — `docs/results/t1t2_trim_backtest.md`'s verdict (referenced throughout Phase 4A) found no return case, though the *capital-impairment* case was separately, non-empirically decided as doctrine.
- **Does realistic FIFO lot accounting change the tax finding's materiality classification?** No — it narrowed the magnitude substantially (57–62% smaller taxable base at every `repay_fraction`) but did not flip "material" to "non-material" at the 25%/50% fractions, or "suggestive" to "material" at 10% (`docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md`).

## 3. Questions partially answered

- **Does tax friction matter?** Partially. The worst-case upper bound found it can materially change the effect's magnitude (`docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md`); Phase 6A's FIFO refinement confirmed the direction and materiality survive under a more realistic accounting method, but this account's actual real cost basis, elected lot convention, tax rate, and jurisdiction remain entirely unknown — the answer is bounded, not exact.
- **Does concentration change margin risk?** Partially. Phase 4A found a material MaxDD gap (−5.14pp) on its core comparison but zero forced-deleveraging events, landing on "Evidence inconclusive" under its own pre-committed gate. A subsequent governance review (`docs/PHASE4A_OUTCOME_GATE_REVIEW.md`) found the gate's second condition was too narrow (one of three relevant signals it had already collected), adopted a wider gate for *future* cycles only, and explicitly did not retroactively reclassify Phase 4A's own recorded result.
- **Does the simulator's execution model match real brokerage behavior?** Partially. Phase 7A confirmed several real mechanisms (concentration-triggered maintenance escalation, no-notice forced liquidation, tiered borrowing rates) that the simulator has no analog for, but could not obtain Robinhood's own specific numeric policies (blocked by tooling, not by requesting deeper documents) and confirmed several items are permanently unresearchable from outside the brokerage (liquidation-sequencing and forced-liquidation-sizing algorithms).

## 4. Questions shown to be unanswerable within this simulator

- **What did this account's real historical margin behavior actually look like?** Never recorded; the only path forward is starting to log it now, which produces value only after months/years of accumulation (`docs/MARGIN_DATA_INVENTORY.md`, `docs/PHASE4_READINESS_REVIEW.md` §3).
- **What is this account's real cost basis, real lot-consumption election, real tax rate, or real jurisdiction?** Genuinely unavailable to a synthetic $0-start simulation, regardless of how realistic its internal mechanics become (`docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` §8).
- **Robinhood's proprietary liquidation-sequencing and forced-liquidation-sizing algorithms.** Not published anywhere, no disclosure obligation covers them, structurally unresolvable by any public research effort (`docs/PHASE7A_DATA_AVAILABILITY_ASSESSMENT.md`, "Findings That Are Structurally Unresolvable").
- **Sub-order routing/execution mechanics.** Proprietary to the broker and market makers; not disclosed to retail customers at that granularity (`docs/PHASE7A_DATA_AVAILABILITY_ASSESSMENT.md` item 9).
- **How this account (or any concentrated/levered account) would behave in a genuinely severe, broad market decline** — this project's 2021–2026 window contains one real but brief bear stretch (2022); every backtest in this program carries that sample-size caveat, restated in nearly every document produced.

## 5. What evidence actually changed understanding

- **The transaction-cost pass** — closed a real open question (does turnover cost matter) with a clear, negligible-effect answer, and in doing so surfaced two better-targeted follow-up questions (tax, stress timing) that turned out to be more consequential than the original cost question itself.
- **The tax-treatment upper-bound pass** — the single most consequential sensitivity finding in the program: unlike transaction costs, tax friction *can* materially change the effect's magnitude, a materially different character of finding than every other friction category tested.
- **Phase 6A's FIFO refinement** — showed the upper bound was a real overstatement (57–62% too high), a genuine update to the program's confidence in its own prior severe assumption, even though it didn't change the governance-relevant conclusion.
- **Phase 4A's outcome-gate review** — found its own pre-committed evidence-classification gate had a real, identifiable coverage gap (using only one of three already-collected corroborating signals), and fixed it for future cycles without retroactively rewriting the historical record — a methodological correction, not a results correction.
- **Phase 7A's evidence inventory** — surfaced two real, sourced brokerage mechanisms (concentration-triggered maintenance escalation; no-notice forced liquidation) that no simulation in this entire program, from Phase 3 through 6A, has ever been able to represent — a structural finding about what this program's evidence can and cannot mean, not a parameter finding.

## 6. What evidence did not change governance

Every other closed question in the program — the return-effect finding itself, the leverage-cap sweep, the repayment-sensitivity sweep, the weight-scheme backtest, the trim-rule backtests, the regime/trend gate backtests, the rung backtest — produced a clear answer that **did not** translate into a production or doctrine change, either because the effect was genuinely absent/immaterial, or because the finding was structurally incapable of overriding an already-fixed doctrine rule (the 1.8x leverage cap and 30% buffer floor are explicitly "no discretion, no timing, no exceptions" per `CLAUDE.md`, regardless of what any backtest shows). The single formal governance decision this program produced — `docs/PHASE5B_GOVERNANCE_DECISION.md`'s "maintain current doctrine" — was reaffirmed, not revised, by every subsequent phase (Phase 6A's tax refinement, Phase 6B's reassessment, Phase 7A's execution-reality findings).

## 7. Final program status

**Closed.** No open research question in this program is currently expected to change governance without new evidence of a fundamentally different kind (real broker records, real account data) than more simulation can produce. `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` is updated separately, alongside this document, to reflect final status on every backlog item.

---

## Timeline of Phases 3–7

| Phase | Subject | Outcome |
|---|---|---|
| 3A–3D | Build the isolated hypothetical margin-simulation harness (`margin_simulation.py`); implement Model B/C mechanics | Harness built, decoupled from production, fully tested |
| 3E–3G | Execute real scenarios; sensitivity-sweep `repay_fraction` and Model C's `drawdown_trigger_pct` | Effect observed and confirmed monotonic |
| — | Transaction-cost sensitivity | Closed: erosion immaterial at every tested magnitude |
| — | Tax-treatment sensitivity (worst-case upper bound) | Closed: friction can be material under a severe upper bound |
| — | Stress-regime execution assumptions | Closed: Model B structurally under-fires during detected real stress |
| 4A | Concentration × margin research | Closed: "Evidence inconclusive" under its own pre-committed gate; gate coverage gap identified and fixed for future cycles only |
| 5A–5B | Evidence-to-decision synthesis and governance decision | Decision: maintain current doctrine; margin remains research-only |
| 6A | Tax-lot / FIFO realized-gain modeling | Closed: taxable base narrowed 57–62%; materiality classification unchanged |
| 6B | Governance reassessment | Outcome: "Evidence does not support changing research assumptions" |
| 7A | Execution-reality research (broker mechanics, execution modeling) | Closed: two real brokerage mechanisms confirmed unrepresented by the simulator; two of the program's proprietary unknowns confirmed structurally unresearchable |

## Evidence vs. governance distinction

This program consistently separated two different kinds of output, and every phase's own documents named the distinction explicitly:

- **Evidence** — a measured, hypothetical/simulated finding about how a simulated policy behaves under a stated set of assumptions. Every evidence document in this program carries the `hypothetical, simulated` label and passes a banned-language check refusing any phrasing that could be read as a claim about this account's real history.
- **Governance** — a decision about what, if anything, evidence justifies changing in production. Exactly two formal governance documents exist in this program (`docs/PHASE5B_GOVERNANCE_DECISION.md`, `docs/PHASE6B_GOVERNANCE_REASSESSMENT.md`), both reaching the same conclusion, and both explicitly distinct in kind from every evidence document that preceded them — no evidence document in this program ever concluded with a production recommendation, and no governance document ever recomputed a figure.

## Production changes made

**None.** `allocate.py`, `targets.yaml`, `holdings.yaml`, and `margin_state.py` were never modified by any phase of this program. Verified via `git diff --stat` before every single commit across all seven phases.

## Doctrine changes made

**None.** `CLAUDE.md`'s Decisions Log gained no new entry from this program. `targets.yaml`'s margin schema remains entirely `null`, exactly as it was before Phase 3 began.

## Simulator improvements made only for measurement

Exactly two additive extensions to `margin_simulation.py` across the entire program, both made only because a specific, named metric was genuinely impossible to derive externally:

1. **`track_tickers` / `tracked_values`** (Phase 4A) — per-ticker daily dollar value, needed for concentration measurement, not derivable from the engine's pre-existing aggregate gross/book/leverage series.
2. **The FIFO lot ledger / `tax_lot_events`** (Phase 6A) — per-lot acquisition/disposal records, needed to move from a worst-case tax upper bound to a realistic realized-gain figure, impossible without tracking data the engine had never retained.

Both were proven, by dedicated regression tests, to change no existing output when unconsumed — additive only, never a behavior change to any prior result.

## Permanent limitations

- This account's real historical margin behavior was never recorded and cannot be reconstructed.
- This account's real cost basis, tax rate, jurisdiction, and lot-consumption election are unknown and unknowable from simulation alone.
- Robinhood's proprietary liquidation-sequencing and forced-liquidation-sizing algorithms are not published and are not expected to become available.
- This project's 2021–2026 price window contains one real, brief bear stretch (2022) — every backtest conclusion in this program is bounded by that sample.
- No simulation in this program has ever modeled, or could model, a broker-initiated forced sale — every MaxDD figure produced describes a simulated price path under the assumption that no such event interrupts it.

---

## Lessons learned

- **Answering a question once, under a pre-committed threshold, and refusing to relitigate it without new evidence, is what actually let this program close.** Every backtest in this line — trims, rungs, regime/trend gates, weights, transaction cost, tax, stress timing, concentration — followed this discipline, and it is the reason the program has a defined endpoint rather than an ever-expanding parameter search.
- **Closing one question reliably surfaced the next, better-targeted one.** The transaction-cost close surfaced tax and stress timing; the tax upper-bound close surfaced the need for lot realism; every friction-category close surfaced the execution-reality question. This chain was productive precisely because each new question was narrower and more specific than the one before it, not broader.
- **A null result (no effect, no change) was treated as being just as valuable as a positive one, consistently, once the three-way outcome framework replaced an earlier positive/inconclusive framing.** This kept the program from either over-claiming a weak signal or discarding a real "nothing here" finding as a failure.
- **The hardest, most consequential gaps this program found were not parameter gaps — they were representational gaps.** Neither more `repay_fraction` sweeps nor more tax-rate tiers would have found the concentration-triggered maintenance escalation or the complete absence of a forced-liquidation mechanic; only asking a structurally different kind of question (what does the simulator not even attempt to represent) surfaced those.
- **A governance decision, once made under a stated evidentiary bar, held up under real pressure to revisit it.** Two separate follow-on research passes (tax-lot realism, execution reality) each produced real, narrowing evidence, and neither one moved the governance decision — which is the discipline working as intended, not a sign the research was wasted.
- **Evidence and governance are different documents for a reason.** Keeping every evidence pass free of production-recommendation language, and every governance document free of new computation, made it possible to trust that a "material" finding in an evidence document was never quietly smuggling in an implementation decision.

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure.
- Does not modify `margin_simulation.py`, `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or `CLAUDE.md`.
- Does not change any prior document's recorded conclusion.
- Does not recommend future work — that is out of scope for a closure document by design.

This closes the Phase 3–7A margin research program.
