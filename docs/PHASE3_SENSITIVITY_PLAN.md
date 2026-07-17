# Phase 3G: Sensitivity Testing Plan

> **⚠️ Hypothetical, simulated — a design document, not a result.** No simulation described here has been run. This document specifies what will be swept, what will be held constant, what will be measured, and how the output will be read — fixed BEFORE execution, per the same pre-committed discipline as every closed backtest in this repo. When these sweeps eventually run, every result they produce remains a hypothetical simulation of a synthetic $0-start account through real historical prices — see `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies to every sweep in this plan.

_Written 2026-07-17, following `docs/PHASE3_DECISION_GATE.md`'s approval to proceed to sensitivity-design work. No simulations run. No simulation code modified. No production files touched. This document is Phase 3G-design only — Phase 3G-execution is a separate, later, explicitly-approved step._

---

## Why sensitivity testing, and why now

Every threshold Phase 3E ran with — Model B's `repay_fraction=0.25`, Model C's `drawdown_trigger_pct=15.0`, and a single `interest_apr=0.05` — was explicitly a single initial value, not a chosen-because-tested value (`docs/PHASE3_SCENARIO_MANIFEST.md` §1: "sweepable {10%, 25%, 50%}... not swept here"). The Decision Gate (`docs/PHASE3_DECISION_GATE.md` §4) confirmed no repayment parameter has been changed and no doctrine decision has been made. Sensitivity testing exists to answer one question per dimension: **does the Phase 3E finding hold across a reasonable range of this parameter, or was it an artifact of the one value tested?** It is diagnostic, not optimization — this plan explicitly forbids picking whichever value in a sweep produces the "best" result and calling that a finding (see each dimension's Interpretation rules, and the standing prohibition in the closing section).

Three independent dimensions, run separately (not as a combinatorial grid — see Scope note below):

---

## 1. Model B harvest sensitivity

**Variable changed:** `ModelBProfitHarvest`'s `repay_fraction` parameter — the share of any fresh net-equity gain (above the prior high-water mark) repaid toward margin debt.

**Values:** 10%, 25%, 50% — exactly the sweep set named in `docs/PHASE3_SCENARIO_MANIFEST.md` §1 ("sweepable {10%, 25%, 50%}"). 25% is the value already run in Phase 3E (`docs/results/PHASE3_SCENARIO_RESULTS.md`'s D-B row / `docs/results/PHASE3_MODEL_B_ANALYSIS.md`) — that existing result is reused for the 25% arm, not re-run, when this sweep eventually executes.

**Variables held constant:**
- Universe (63 tickers), window (2021-06-01 to 2026-07-10), deposit cadence ($2,000/mo), tier weights, band/spec trim rule — the full shared configuration from `docs/PHASE3C_SCENARIO_CONFIGURATION.md`.
- Leverage cap: 1.8x (Scenario D's fixed level).
- Interest: 5.00% APR, $1,000 free (this phase's default — see §3 for the separate interest dimension; not varied simultaneously with `repay_fraction`, per the standing "one thing varies" discipline).
- Model C: not active in this sweep — Model B is tested in isolation, same as Phase 3E's D-B arm (no combined Model B+C scenario is in scope for this plan).
- The HWM-tracking mechanism itself (net_equity-based, evaluated pre-trade) — unchanged, only the harvest fraction varies.

**Metrics collected** (per arm, from `SimulationResult.metrics()` plus the event-level detail `docs/results/PHASE3_MODEL_B_ANALYSIS.md` already demonstrated extracting):
- `ann_twr_pct`, `max_drawdown_pct`, `annualized_volatility_pct`, `cagr_pct`
- `final_margin_debt`, and net debt reduction versus the D-0 (no-repayment) control
- `n_repayment_events`, `total_repaid` (gross), mean/median/max event size
- TWR/|MaxDD| ratio (the same simple lens `PHASE3_MODEL_B_ANALYSIS.md` §7 used, explicitly labeled there as one lens, not a verdict — same label applies here)

**Interpretation rules:**
- Report all three arms' full metrics table — no arm is dropped, hidden, or presented as the "recommended" one.
- Compare each arm against the D-0 control using the same 2.0pp decision threshold already established for Scenario D (`docs/PHASE3_SCENARIO_MANIFEST.md` §1) — a decision threshold, not a proof threshold, restated identically here.
- Look for **monotonicity**: does the TWR cost and MaxDD benefit scale roughly with `repay_fraction` (10% costs least/helps least, 50% costs most/helps most, 25% in between)? A non-monotonic result (e.g., 25% doing worse on both axes than 10% AND 50%) would be a flag to investigate the mechanism, not to pick a different favorite.
- Explicitly forbidden: selecting the fraction with the best TWR/|MaxDD| ratio and reporting that as "the answer." The purpose of this sweep is to characterize sensitivity, not to search for an optimum — see the closing section.
- If the 25%-arm reused result and a hypothetical freshly-re-run 25% arm would differ (they should not, since nothing about the simulation changed), that would indicate non-determinism in the harness — a bug to report, not a sensitivity finding.

---

## 2. Model C drawdown trigger sensitivity

**Variable changed:** `ModelCRiskReset`'s `drawdown_trigger_pct` parameter — the net-equity drawdown-from-peak threshold that activates a reset.

**Values:** 10%, 12.5%, 15%, 20% — four points bracketing the 15% value already run in Phase 3E (which found the trigger fired zero times in this window, `docs/PHASE3_FINDINGS.md` §6). The lower values (10%, 12.5%) are included specifically because the 15% non-trigger finding raised the natural next question: does a looser (lower) threshold ever fire in this window, or is this window's simulated portfolio simply too diversified/too smooth for ANY reasonable drawdown trigger to activate? 20% is included as the symmetric wider point, to confirm the trigger stays silent as expected when loosened further in the other direction.

**Variables held constant:**
- Same shared configuration as §1.
- `reset_leverage`: 1.25x, unchanged (this dimension varies only the trigger sensitivity, not the reset target — a combined trigger×target sweep is out of scope for this plan).
- Leverage cap: 1.8x.
- Interest: 5.00% APR, $1,000 free (default, not varied simultaneously).
- Model B: not active in this sweep — Model C tested in isolation, matching Phase 3E's D-C arm.
- Restoration logic (new-high AND leverage-normalized) — unchanged.

**Metrics collected:**
- Same core set as §1 (`ann_twr_pct`, `max_drawdown_pct`, `annualized_volatility_pct`, `cagr_pct`, `final_margin_debt`).
- **`n_reset_events`** (how many times `drawdown_trigger_pct` was crossed and a reset activated) — the single most important metric for this sweep, since Phase 3E's 15% arm reported exactly zero.
- If `n_reset_events > 0` for any arm: `total_repaid` at reset, and days spent with `effective_leverage_cap` tightened to 1.25x (a direct measure of how long the policy constrained capacity once triggered).

**Interpretation rules:**
- The primary question this sweep answers is binary per arm: **did the trigger fire at all in this window, at this threshold?** Report this first, before any return/drawdown comparison — a threshold that never fires cannot meaningfully be compared on TWR/MaxDD grounds (its result is definitionally identical to the no-repayment control, exactly as 15% already showed).
- If NONE of 10%/12.5%/15%/20% ever fire, the finding is that **this specific simulated window's diversified-portfolio-level drawdown never approaches even the loosest tested threshold** — a statement about this window's character (consistent with the single-window/mostly-rising-sample caveat carried through every prior document), not a statement that Model C's mechanism doesn't work at any threshold in any window.
- If some arms fire and others don't, report the crossover point precisely (which threshold is the first, moving from 20% down to 10%, to actually activate) — this is diagnostic information about how close this window's worst drawdown came to each threshold, not a signal to adopt whichever threshold "worked."
- Explicitly forbidden: lowering the threshold further in a follow-up run specifically to force a trigger and then treating that forced trigger's results as informative about Model C's real-world behavior. If 10% still doesn't fire, that is the finding — it does not license an unplanned 5% arm.

---

## 3. Interest sensitivity

**Variable changed:** `interest_apr` — the annual interest rate applied to margin debt above `interest_free_amount`.

**Values:** 0%, 5%, 8%. 5% is the value already run throughout Phase 3E (Estimated, per `docs/PHASE3C_ASSUMPTION_REGISTRY.md` #10 — doctrine's own "~5%" is not an exact, dated, sourced figure). 0% isolates the pure leverage-mechanics effect with financing cost removed entirely — answers "how much of Phase 3E's margin-drag finding (§Test A, `docs/PHASE3_FINDINGS.md` §6) is attributable to the cost of borrowing itself, versus the structural effect of carrying more invested capital." 8% is a plausible stress case above the doctrine estimate, bracketing the uncertainty already disclosed around the 5% figure.

**Variables held constant:**
- Same shared configuration as §1/§2.
- `interest_free_amount`: $1,000, unchanged.
- Leverage cap: 1.8x.
- Repayment model: this dimension is run against the **Scenario B configuration (MODEL_0, no repayment)** as its primary application — isolating the interest-cost effect from any repayment-model interaction. A secondary note: because interest cost changes `margin_debt`'s trajectory, it could in principle also shift when Model B/C's HWM or drawdown triggers activate — that interaction is NOT tested by this dimension (it would be a fourth, combinatorial dimension, out of scope for this plan, see Scope note below); if pursued later it needs its own design document, not folded silently into this one.

**Metrics collected:**
- `ann_twr_pct`, `max_drawdown_pct`, `annualized_volatility_pct`, `cagr_pct`, `final_margin_debt`.
- Cumulative interest accrued over the window (sum of `interest_accrual` events) — the direct cost-of-carry figure this dimension exists to quantify.
- The A-vs-B gap (unlevered vs. 1.8x-levered TWR difference) recomputed at each interest rate, to see how sensitive Phase 3E's headline margin-drag finding (+5.58pp TWR, -4.40pp MaxDD at 5% APR) is to the rate assumption specifically.

**Interpretation rules:**
- Report the A-vs-B TWR/MaxDD gap at all three rates side by side — this is the primary output of this dimension, more so than any single scenario's absolute numbers.
- If the gap direction (levered beats unlevered on TWR, loses on MaxDD) holds at all three rates, that strengthens confidence the Test A finding isn't purely a function of an optimistically-low interest assumption. If the gap direction reverses at 8% (levered no longer beats unlevered on TWR), that is itself the finding — report it plainly, do not treat it as a reason to discard the 8% arm as "unrealistic."
- Explicitly forbidden: treating 0% as a preferred/base case because it produces the largest TWR advantage for leverage — 0% is a decomposition tool (isolating pure leverage mechanics from financing cost), not a claim about the account's real financing terms. The 5% arm remains the primary reference point (it's Estimated doctrine, not a guess pulled from this sweep).

---

## Scope note: no combinatorial grid

This plan runs three **independent, one-dimensional** sweeps (3 + 4 + 3 = 10 new arms total, each varying exactly one parameter against the shared Phase 3E baseline configuration), not a combined grid (e.g., not Model B repay_fraction × interest rate × Model C trigger simultaneously). This matches every prior backtest's "hold everything constant except the one thing being tested" discipline (`docs/PHASE3C_SCENARIO_CONFIGURATION.md`'s shared-configuration table exists for exactly this reason). A combinatorial sensitivity analysis, if ever warranted, is a separate, larger design effort requiring its own plan and its own approval — not an implicit extension of this one.

## Standing prohibitions (restated, apply to every dimension above)

- **Do not run simulations as part of producing this document.** This plan is design-only; execution is a separate, future, explicitly-approved phase (Phase 3G-execution, not yet started).
- **Do not modify `margin_simulation.py`, `allocate.py`, `targets.yaml`, or `holdings.yaml`** to produce or, later, to execute this plan — all three sweeps use parameters already exposed by `ModelBProfitHarvest.__init__()`, `ModelCRiskReset.__init__()`, and `ScenarioConfig.interest_apr`/`scenario_fixed_leverage()`'s existing signatures. No new code surface is required.
- **Do not optimize.** No dimension's interpretation rules permit selecting a "winning" parameter value and proposing it for adoption. Each sweep's output is a sensitivity characterization — does the Phase 3E finding hold, weaken, strengthen, or reverse across the range — not a search for a better number. Adopting any parameter value into `targets.yaml`'s (still entirely `null`) margin schema remains a separate, explicit, future decision, gated the same way every other doctrine change in this project has been (see `docs/PHASE3_DECISION_GATE.md` §4).
- **Every result, when this plan eventually executes, carries `HYPOTHETICAL_LABEL` and passes `render_metrics()`'s banned-phrase enforcement**, unchanged from Phase 3E's pattern.

Stopping here. No simulations run, no code modified, no production files touched. Awaiting approval before Phase 3G-execution begins.
