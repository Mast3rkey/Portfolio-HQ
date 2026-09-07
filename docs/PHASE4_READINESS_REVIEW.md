# Phase 4 Readiness Review — Evidence Review and Governance Checkpoint

> **⚠️ Hypothetical, simulated.** This document reviews evidence that is itself entirely hypothetical — synthetic $0-start accounts simulated through real historical prices, never a reconstruction of this account's real margin history. Nothing in this review changes that character. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which governs every finding referenced below.

_Written 2026-07-17. No code written. No production files touched. No `targets.yaml` or `allocate.py` changes. This is a synthesis and governance checkpoint over documents already produced (`docs/PHASE3_FINDINGS.md`, `docs/PHASE3_DECISION_GATE.md`, `docs/PHASE3_SENSITIVITY_PLAN.md`, `docs/results/PHASE3_MODEL_B_ANALYSIS.md`, `docs/PHASE3_EXECUTION_RECORD.md`), plus the sensitivity execution results those documents' own successor (`docs/PHASE3_SENSITIVITY_RESULTS.md`, `docs/results/PHASE3_SENSITIVITY_RESULTS.json`) actually produced under the reviewed plan — not requested explicitly in this review's source list, but included because omitting real, already-committed evidence that directly bears on findings strength would make this review incomplete on its own terms. All five requested documents were re-read in full to produce this synthesis, not assumed from memory._

---

## Category definitions (used throughout)

- **A. Evidence-backed facts** — directly observed, verified against the actual repo/code/data, not a simulation output. E.g., "the universe is 63 tickers," "the commit hash is X."
- **B. Simulation observations** — real numbers this simulation harness produced, honestly reported, but describing a hypothetical synthetic account, not this account's real history, and bounded to one window.
- **C. Design proposals** — mechanisms that exist as tested code (`ModelBProfitHarvest`, `ModelCRiskReset`, the concentration-stress concept) but have no live deployment status and no adoption decision behind them.
- **D. Doctrine changes requiring approval** — anything that would alter `CLAUDE.md`'s Decisions Log, `targets.yaml`'s live configuration, or `allocate.py`'s behavior. **None exist in Phase 3.** Every item below that could eventually become a D is currently a B or C.

---

## 1. What findings are strong enough to become doctrine?

**None.** No finding produced in Phase 3A-3G meets this repo's own bar for a doctrine decision. Every prior doctrine change in `CLAUDE.md`'s Decisions Log that was backtest-derived (the trim thresholds, the gate removals, the weight scheme) followed a specific pattern this project itself established: a pre-committed threshold, a single test with a single verdict, and — critically — a leverage/single-name decomposition check before anything with forced-selling implications was adopted (`trim_backtest.md`'s never-trim-vs-RKLB precedent; `t1t2_trim_backtest.md`'s NVDA -66.4% decomposition). Phase 3's Model B and Model C results have not yet had that decomposition step applied (`docs/results/PHASE3_MODEL_B_ANALYSIS.md` §7 states this explicitly: "the single-name-decomposition step... has not been done here"). Crossing a decision threshold (Model B's -2.32pp/+2.07pp gap crosses the pre-committed 2.0pp bar) is a **necessary** condition for considering adoption in this project's own established practice, never a **sufficient** one by itself — every prior adoption also required the decomposition check to pass. That check has not been run for anything in Phase 3.

## 2. What findings are observations only?

Everything substantive Phase 3 produced. Restated, each explicitly bounded to the one window tested (2021-06-01 to 2026-07-10):

- **Margin drag (Test A):** the simulated 1.8x-levered account beat the unlevered control on TWR (+5.58pp) and lost on MaxDD (-4.40pp) at the baseline 5% interest assumption. The direction held across the full interest sensitivity range (0%/5%/8%: +5.97pp/+5.58pp/+5.35pp), narrowing but not reversing as the rate rose.
- **Leverage sweep (Test B):** results were identical from 1.4x through 2.0x — the account's own margin demand in this window never asked for more capacity than ~1.4x already provides. This is a statement about demand in this window, not a stress test of the cap itself.
- **Model B sensitivity:** monotonic across 10%/25%/50% repay_fraction — TWR cost and MaxDD benefit both scale with the fraction (-0.98pp/-2.32pp/-3.56pp TWR; +0.97pp/+2.07pp/+3.16pp MaxDD). Turnover scales from 30.8% to 125.9% of total deposited capital across the same sweep — a real, growing, entirely unpriced cost.
- **Model C sensitivity:** the most consequential new observation from Phase 3G. At 15%/20% drawdown thresholds the trigger fired once each, needing zero repayment (matching Phase 3E's original "identical to control" finding). At 10%/12.5% the trigger fired 10 and 7 times respectively — previously unknown, only surfaced by the sensitivity sweep. Portfolio-level MaxDD stayed essentially flat across all four thresholds despite the differing activation counts, echoing the same "portfolio-level MaxDD is too smooth to show single-name/single-episode effects" pattern this repo's `t1t2_trim_backtest.md` already established in an unrelated context.

## 3. What questions remain unanswered?

- **Concentration interaction (Test D from the original evidence framework).** Zero code exists for the 30% cluster-concentration stress trigger. This is not a thin result — it is a complete absence of evidence. `docs/PHASE3_EXECUTION_RECORD.md` §4 flagged this at execution time; `docs/PHASE3_DECISION_GATE.md` §3 restated it; it remains true today.
- **Whether Model C's mechanism does anything useful in a real stress episode.** The 10%/12.5% firings are the first evidence the mechanism activates at all in real price data, but none of the four thresholds tested produced a scenario severe enough to show what "no dip-buying" restoration behavior looks like over a sustained, deep drawdown — this window's worst episodes are still comparatively mild at the portfolio level.
- **True interest cost, transaction costs, tax effects** — all three remain entirely unaddressed (see §5 below, each treated in more depth).
- **Whether the identical-MaxDD-despite-different-activation-counts pattern in the Model C sweep is itself meaningful** (does it mean the mechanism doesn't affect risk in a way this metric can see, or does it mean this specific window's MaxDD episode occurs at a moment none of these thresholds' interventions touch?) — this has not been decomposed and is an open analytical question, not just a missing-data question.
- **Whether Model B and Model C would behave differently, or interact, if both were active simultaneously** — never tested; `docs/PHASE3_SENSITIVITY_PLAN.md`'s scope note explicitly excluded combinatorial runs.

## 4. What should NOT be implemented yet?

- **Any repayment model as a live, active behavior in `allocate.py` or `targets.yaml`.** Neither Model B nor Model C has cleared the single-name-decomposition bar this project requires before adopting anything with forced-selling implications.
- **Any change to the 1.8x leverage cap, in either direction.** The leverage sweep is inconclusive above 1.4x (§2) — there is no evidence basis to move the cap up, and no finding in Phase 3 argued for moving it down either.
- **The concentration-stress trigger, in any form** — it has no implementation, no test coverage, and (per `docs/PHASE3_DECISION_GATE.md` §3) no evidence at all, not even hypothetical evidence.
- **Any parameter value from the sensitivity sweep treated as "the calibrated one."** `docs/PHASE3_SENSITIVITY_PLAN.md`'s interpretation rules, and `docs/PHASE3_SENSITIVITY_RESULTS.md`'s own restated rules, both explicitly forbid selecting a winner from these sweeps. Nothing has changed that.
- **Turnover-generating mechanisms of any kind (Model B and Model C both qualify) until a transaction-cost model exists.** Deploying either live, even provisionally, before that model exists means deploying something whose real cost cannot currently be estimated at all — not "estimated imprecisely," genuinely absent.

## 5. Additional evidence required before changing:

**Margin leverage cap:** a leverage sweep run against a window, or a synthetic stress construction, that actually forces the account's margin demand past 1.4x — the current sweep never tests what 1.6x-2.0x do under real pressure because demand never reached that high in this window. Also requires the concentration-interaction test (an over-concentrated position under higher leverage is exactly the scenario the cap exists to guard against, and that interaction is entirely untested). The cap is currently doctrine (`CLAUDE.md`: "no discretion, no timing, no exceptions"), and per that document's own stated posture, changing it needs a leverage-regime change, not a single backtest window's result — Phase 3 has not supplied one.

**Repayment rules:** the single-name-decomposition check (§1) for both Model B and Model C, run the same way `t1t2_trim_backtest.md` ran it for NVDA — identify each model's own worst-case single-episode impact under leverage, not just the portfolio-aggregate MaxDD number, which this review's §2/§3 already flagged as potentially too smooth to show what matters here. Also requires: a transaction-cost sensitivity pass (see below) before any turnover-generating model can be responsibly evaluated, and a decision — not yet made, see §6 below — on whether repayment should ever be automatic versus advisory-only.

**Allocation logic (`allocate.py`):** no evidence in Phase 3 argues for any change here at all. `allocate.py`'s `plan()`, `margin_capacity()`, and every trim rule were explicitly held constant throughout every scenario (`docs/PHASE3C_SCENARIO_CONFIGURATION.md`'s shared configuration) specifically so Phase 3 would never produce evidence bearing on allocation logic changes. If allocation-logic changes are ever motivated by margin research, that would require a new, separately-scoped evidence effort — Phase 3's design cannot supply it.

**Concentration controls:** everything. No trigger, no test, no simulated result, no sensitivity sweep. This is the single largest evidence gap Phase 3 leaves behind, restated for the third time across three documents (`PHASE3_EXECUTION_RECORD.md`, `PHASE3_DECISION_GATE.md`, this review) specifically so it cannot be quietly treated as covered by adjacent work.

## Special attention items

**Concentration interaction testing:** see §3/§4/§5 above — this is the most complete gap in the whole Phase 3 evidence base, not a partial one. Before Phase 4 does anything with concentration and margin together, this needs actual implementation and its own execution record, manifest, and sensitivity design, the same rigor Model B/C received in Phase 3B-3G.

**Transaction cost sensitivity:** does not exist anywhere in this repo — not in `margin_simulation.py`, not in `allocate.py`'s live logic, not in any prior backtest (`trim_backtest.md`, `t1t2_trim_backtest.md`, etc. are all silent on trading costs, consistent with the account's cash-brokerage assumption, but Model B/C's *margin-repayment-driven* turnover is qualitatively different — it's forced, mechanical, and now measured at 30.8%-125.9% of deposited capital, `docs/PHASE3_SENSITIVITY_RESULTS.md` §1). This is a real, quantifiable, currently-invisible cost. Before any repayment model is taken seriously as a candidate for deployment, a cost-sensitivity pass (even a simple fixed-bps-per-trade assumption, clearly labeled Hypothetical, mirroring how the 5% interest assumption is labeled Estimated) should be added and run the same way the interest-rate sensitivity dimension was.

**Whether repayment should be automatic or optional:** **this question has not been addressed anywhere in Phase 3 and has no answer in this evidence base.** Every document reviewed treats Model B/C purely as *simulation policies* — what a hypothetical account following a stated rule would experience — never as a *live recommendation mechanism*. `margin_state.py`'s existing, already-integrated `classify_margin_state()` (Phase 2D) only ever produces risk-state labels and advisory text in `allocate.py`'s render output; it recommends nothing that executes automatically, consistent with `CLAUDE.md`'s foundational rule that this tool never places orders and is advisory only. If Model B or Model C were ever adopted, "automatic" in this codebase can only ever mean "surfaced as a recommendation in the advisory output," never "executed without the user's manual action" — the order-placement code was deliberately stripped from `alpaca_client.py` and must never be re-added. This question needs its own explicit design discussion before Phase 4, not an implicit default.

**Whether margin should be treated as a portfolio-level risk resource only:** the evidence to date is consistent with this framing but has not tested it directly. `margin_state.py`'s concentration scoring is explicitly documented as portfolio-level, never per-ticker (`docs/MARGIN_DOCTRINE.md`'s ✅/❌ checklist). Model B and Model C both operate on portfolio-level net_equity, never on individual positions. Nothing in Phase 3 has tested or proposed a per-position margin-allocation concept, and nothing should — that would be a fundamentally different, riskier design (assigning leverage to specific names rather than treating debt as an account-wide liability) that this project's `concentration_risk_score()` docstring already explicitly disclaims ("does NOT answer 'how much leverage does NVDA have'... margin debt is an account-wide liability with no real per-position allocation"). This framing should be explicitly reaffirmed, not silently assumed, before Phase 4 proceeds.

---

## Summary table

| | Status |
|---|---|
| A. Evidence-backed facts | Universe (63 tickers), window (2021-06-01 to 2026-07-10), test counts (156 passing), commit provenance, what code does/doesn't exist (concentration trigger absent) |
| B. Simulation observations | Margin drag direction/magnitude, leverage sweep flatness above 1.4x, Model B monotonicity + turnover cost, Model C's newly-surfaced 10%/12.5% activations — all window-bounded, all hypothetical |
| C. Design proposals | `ModelBProfitHarvest`, `ModelCRiskReset` (tested code, no deployment decision), the 30% concentration stress concept (no code at all) |
| D. Doctrine changes requiring approval | **None exist.** No leverage cap change, no repayment rule change, no allocation logic change, no concentration control has been proposed for adoption by any Phase 3 document, and this review proposes none either. |

## What this review deliberately does not do

- Does not write or modify any code.
- Does not touch `targets.yaml`, `allocate.py`, `margin_state.py`, or any other production file.
- Does not run any new simulation.
- Does not recommend a specific next action for Phase 4 — it states what evidence is missing before specific categories of change (leverage cap, repayment rules, allocation logic, concentration controls) could be responsibly considered, and leaves the decision of what to do next to a separate, explicit approval step.

Stopping here. This is a governance checkpoint only. Awaiting direction before Phase 4 begins.
