# Phase 5 — Decision Gate Synthesis: Evidence-to-Decision Review

> **⚠️ Governance synthesis, not a re-run.** This document runs no simulation, computes no new figure, and changes no code. Every number below is quoted from an already-committed source, cited inline. It converts a completed evidence stack into an explicit decision framework — it does not itself make a production decision. `targets.yaml`'s margin schema remains entirely `null`; `CLAUDE.md`'s Decisions Log is unchanged; nothing in `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py` is touched by this document.

_Written 2026-07-17. Bridges the completed Phase 3/4A margin research line to a governance decision, per explicit request: "the next document should not be another research plan, it should be a decision-gate synthesis." Documentation only._

---

## 1. Evidence inventory

Summary of completed work only — no new analysis performed here.

| Phase | Document(s) | Question | Result |
|---|---|---|---|
| 3A–3D | `PHASE2_IMPLEMENTATION_PLAN.md`, `PHASE3C_*`, `MARGIN_INTELLIGENCE_DESIGN.md` | Build an isolated, hypothetical margin-repayment simulation harness | `margin_simulation.py` built, decoupled from production files, Model B (profit harvest) and Model C (risk reset) implemented |
| 3E | `PHASE3_FINDINGS.md`, `PHASE3_EXECUTION_RECORD.md` | Do repayment policies change simulated outcomes vs. no-repayment control? | Yes — Model B (25%): 33.28% TWR vs. 35.59% control (−2.32pp), −24.74% MaxDD vs. −26.81% (+2.07pp improvement). Both cross the pre-committed 2.0pp threshold. |
| 3F | `docs/results/PHASE3_MODEL_B_ANALYSIS.md` | What do repayment events actually look like? | 296 events, $88,516.45 gross repaid, $43,786.24 net debt reduction (roughly half — a brake, not an elimination policy) |
| 3G | `PHASE3_SENSITIVITY_PLAN.md`/`RESULTS.md` | Is the effect sensitive to `repay_fraction` and Model C's `drawdown_trigger_pct`? | Monotonic across 10/25/50% — effect scales with intensity, no non-monotonicity found |
| Transaction cost | `TRANSACTION_COST_SENSITIVITY_PLAN.md`/`RESULTS.md` | Do trading costs erase the effect? | No — even at a 15bps ceiling, erosion was three orders of magnitude smaller than the observed gap; materiality classification never changed |
| Tax sensitivity | `TAX_TREATMENT_SENSITIVITY_PLAN.md`/`RESULTS.md` | Does tax friction erase or shrink the effect? | Magnitude-changing, not effect-erasing — at 50%/32% worst-case upper bound, gap widened from −3.56pp to −7.45pp |
| Stress-regime | `STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md`/`RESULTS.md` | Does repayment behave differently under detected market stress? | Model B rarely operates during stress — 5.9–6.9% of repayment dollars fell inside detected stress windows vs. a 12.2% base rate; threshold exposure stayed 0.0% at every arm |
| 4A | `PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md`, `PHASE4A_RESEARCH_REPORT.md`, `PHASE4A_OUTCOME_GATE_REVIEW.md` | Does concentration change the risk profile of margin usage? | Evidence inconclusive under the pre-committed gate (material MaxDD gap, −5.14pp, but zero forced-deleveraging events); outcome-gate review found a real coverage gap and adopted a revised gate for *future* cycles only — Phase 4A's own recorded result was not retroactively changed |

No new simulation was run to produce this table; every figure is quoted from the cited document.

## 2. What the evidence supports

- Margin repayment policies (Model B specifically) produce a **measurable, monotonic, simulated tradeoff** between annualized TWR and MaxDD, observed consistently from first execution (3E) through every subsequent sensitivity dimension.
- That tradeoff **persisted under every tested friction assumption except one**: transaction costs (tested, negligible), and stress-window timing (tested, the mechanism is naturally stress-averse) did not erode it; tax friction (tested, bounded upper-bound only) can materially change its *magnitude*, not its direction or existence.
- Model B's trigger structure (high-water-mark / fresh-gains-based) has a **demonstrated, mechanism-level operating profile**: it fires in calm/rising conditions and is structurally quiet during detected stress. This is a property of the mechanism, confirmed by direct measurement (§ stress-regime results), not an artifact of one simulation run.
- The concentration question (4A) surfaced a **real, material MaxDD signal** on its core comparison (−5.14pp, more than double the pre-committed threshold) even though the overall outcome landed "inconclusive" on the narrower originally-specified gate — and that gate's own coverage gap has already been identified and addressed for future cycles (not retroactively, per its own non-retroactivity statement).

## 3. What the evidence does not support

Explicitly, none of the following are authorized, implied, or brought closer by this evidence stack:

- **No production repayment rule.** No `repay_fraction`, trigger threshold, or repayment model has been selected, ranked, or recommended at any point in this research line — every sensitivity pass explicitly reported the full grid without picking a winner.
- **No leverage increase.** The 1.8x structural cap and 30% buffer floor are untouched inputs throughout every scenario; none of this research argues for or against their level.
- **No margin schema activation.** `targets.yaml`'s margin schema remains entirely `null`, exactly as it has been since before Phase 3 began.
- **No parameter selection.** `repay_fraction`, `drawdown_trigger_pct`, cost tier, tax tier, and stress-detection parameters were all tested as disclosed grids, never optimized or chosen.
- **No automatic execution.** Nothing in this research line proposes, designs, or moves toward order placement of any kind — the standing doctrine (`CLAUDE.md`: "This tool NEVER places orders") is untouched by every document in this line.

## 4. Decision options

This is the layer the prior research phases deliberately did not produce — a decision framework, not a fact.

### Option A — Maintain current doctrine

**Meaning:** Keep margin repayment research-only. `targets.yaml` unchanged. Margin schema stays inactive. The evidence stack is retained as a reference but has no live effect on any workflow output.

**Consistent with:** every "no doctrine recommendation" statement already on record (`PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` §6, `STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md`'s prohibited-conclusions section, `PHASE4A_RESEARCH_REPORT.md`). Requires no new work of any kind.

### Option B — Allow advisory-only monitoring

**Meaning:** `allocate.py`'s output could, in principle, include a hypothetical repayment-scenario calculation alongside the existing allocation table (e.g., "if Model B were active at 25%, it would suggest repaying $X this cycle") — purely informational, no order-adjacent effect, human decision still required for every action, `holdings.yaml`/margin state still updated only via the existing manual sync workflow.

**Not yet justified by the evidence stack as recorded:** this would be a production-file change (`allocate.py`) and would require its own separate implementation approval, UI/output design, and — per the remaining blockers in §5 — real tax-lot and execution-cost data to avoid presenting hypothetical figures as actionable ones.

### Option C — Prepare a future controlled pilot

**Meaning:** Only if a materially stronger evidence threshold is met later (see §5): a narrowly scoped, explicitly approved, separately validated pilot — still manual execution, still advisory-only per the tool's core identity, no automatic deployment under any circumstance.

**Gated on:** resolution of at least the tax-lot and execution-slippage blockers below; this option is not actionable today and is recorded here only as a named possibility, not a proposal.

This document does not select among A/B/C. That selection, if made, is itself a governance decision requiring its own explicit approval step — see §6.

## 5. Remaining blockers

Carried forward from `PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` §5 and `STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md`'s "does not resolve" section, consolidated:

1. **Real tax-lot accounting.** The harness has no cost-basis tracking; the tax sensitivity pass used a disclosed, deliberately severe upper bound (100% of every repayment event treated as realized gain), never an estimate of this account's actual liability.
2. **Real execution/slippage modeling.** Every trade in every scenario, calm or stressed, is assumed to fill instantly at that day's close. The stress-regime pass's regime-conditional cost overlay is a disclosed, bounded hypothetical multiplier (3x), not a validated real-world value.
3. **Real broker margin behavior during extreme events.** No document in this line has modeled margin-call mechanics, forced-liquidation sequencing, or Robinhood-specific margin policy under stress — the simulation's leverage-cap clipping is a simplified, self-consistent rule, not a broker-behavior model.
4. **Human override / execution workflow.** No document has addressed how a human would actually act on a repayment signal inside the existing manual Robinhood-execution workflow (`CLAUDE.md`'s Workflow section) — this is a process design question, not a research question, and has not been touched.
5. **Different market regimes not represented in the tested window.** Every backtest and simulation in this line uses the same 2021–2026 real-price window (with the same single real bear stretch, 2022) already flagged as a sample-size caveat in nearly every prior document (e.g., `t1t2_trim_backtest.md`, `trim_backtest.md`). No claim in this line generalizes beyond that window.

## 6. Final decision statement

**The evidence stack is sufficient to inform governance discussion but insufficient to authorize production behavior.**

Four economic-friction questions (return effect, transaction cost, tax, stress timing) have each been tested exactly once, under pre-committed thresholds, with no parameter selection — closing the research-loop discipline this project has followed since the original band-overlay/rung/regime/trend/weight backtests. A fifth question (concentration) surfaced a real signal on its core comparison but landed on a narrower originally-specified gate's "inconclusive," with the gate's own coverage gap already identified and corrected for future use, not retroactively applied.

None of this, individually or cumulatively, changes `targets.yaml`, `allocate.py`, `holdings.yaml`, `margin_state.py`, or `CLAUDE.md`. No option in §4 is selected by this document. What exists now is a **decision framework**, not a decision.

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure — every number in §1–§3 is quoted from an already-committed source.
- Does not select Option A, B, or C from §4.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or `CLAUDE.md`.
- Does not change any prior document's own recorded conclusion, including Phase 4A's "Evidence inconclusive" result.
- Does not open Phase 5B (governance decision) or Phase 5C (additional research) — per the explicit instruction, only one of those should open next, not both, and neither opens automatically from this document.

Stopping here. Awaiting direction on whether to open Phase 5B or Phase 5C.
