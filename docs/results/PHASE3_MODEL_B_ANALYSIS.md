# Model B (Profit Harvest) — Analysis

> **⚠️ Hypothetical, simulated.** This document analyzes one already-executed Phase 3E simulation run (`docs/results/PHASE3_SCENARIO_RESULTS.md`'s D-B row) in more depth. It does not run a new scenario, does not tune `repay_fraction` away from the approved 25% initial value, and does not change the HWM-gain trigger. All figures below are re-derived from the same, already-approved Model B configuration — same universe, window, deposits, and parameters as Phase 3E — solely to extract per-event detail that the Phase 3E summary tables didn't retain. Nothing here is a claim about this account's real history; see `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies to this document too.

_Written 2026-07-17. Source: `ModelBProfitHarvest(repay_fraction=0.25)`, `docs/PHASE3_SCENARIO_MANIFEST.md` §1, run against the same 63-ticker universe and 2021-06-01 to 2026-07-10 window as Phase 3E, at the same commit (`585c117`). Control for comparison: Scenario B (MODEL_0, no repayment, same 1.8x cap)._

---

## 1. Repayment event count

**296 repayment events** over 1,283 simulated trading days (62 monthly deposits) — Model B's HWM-gain trigger fired on approximately 23% of all trading days, meaning the simulated portfolio set a new net-equity high-water mark on roughly 1 in 4 days across the window. This is a materially rising, materially volatile-around-the-rise simulated portfolio (consistent with the underlying window's own strong bull-market character, `ann_twr_pct` even in the unlevered Scenario A was 30.01%).

One data quality note: the smallest recorded "event" was `2.27e-12` dollars — floating-point noise from a day where net_equity crossed the prior HWM by an amount indistinguishable from zero, not a real economically meaningful repayment. Not filtered out of the 296 count or the totals below (filtering it would itself be a parameter-adjustment-after-seeing-results the scope here prohibits) — flagged so it isn't mistaken for a real, material event.

## 2. Repayment amounts

| Statistic | Value |
|---|---:|
| Count | 296 |
| Total | $88,516.45 |
| Mean | $299.04 |
| Median | $175.64 |
| Min | ~$0 (floating-point noise, see §1) |
| Max | $2,500.46 |

Distribution by size:

| Bucket | Count |
|---|---:|
| < $100 | 99 |
| $100 – $1,000 | 181 |
| $1,000 – $5,000 | 16 |
| $5,000+ | 0 |

Most events are small (61% under $1,000) — consistent with a mechanism that fires on *every* new high, not just large ones; the 25% harvest fraction applied to typically modest day-over-day equity gains produces typically modest repayments. The 16 larger events ($1,000-$5,000) likely correspond to gains realized shortly after a monthly deposit lands and gets deployed, or to sharp multi-day rallies.

## 3. Total debt reduction

Two distinct numbers, not to be conflated:

| Measure | Value | What it means |
|---|---:|---|
| **Gross repaid** via Model B's mechanism | $88,516.45 | Sum of all 296 repayment events — money actively diverted to debt paydown over the window |
| **Net final-debt difference vs. control** | $43,786.24 | (Control's final debt $147,745.28) − (Model B's final debt $103,959.04) |

The net figure is roughly **half** the gross figure because Model B does not stop the account from drawing *new* margin on subsequent deposits — every gross-repaid dollar can be redrawn later if a future deposit's allocation gap needs it and leverage room is available. Model B is a **profit-harvesting brake, not a leverage-elimination policy**: it continuously skims gains into debt reduction, but the account's normal deposit-driven margin-drawing behavior (unchanged, still governed by the scenario's 1.8x cap) continues to operate independently and can re-draw against that freed-up capacity. This is expected given the mechanism as specified (`PHASE3_SCENARIO_MANIFEST.md` §2: "no additional borrowing" means Model B itself never initiates a draw — it says nothing about suppressing the *scenario's normal* deposit-driven draws).

## 4. Turnover impact

Model B's repayments are funded first from idle cash, then via a pro-rata trim across held positions (`margin_simulation._fund_repayment()`). In this harness, idle cash is typically near-zero shortly after each deposit is fully deployed (min_lot=$1, so allocation leaves negligible leftover cash) — meaning **the large majority of the $88,516.45 gross repaid was funded by selling and immediately repurchasing-equivalent-value positions**, i.e., forced turnover, not idle cash sitting on the sidelines. This wasn't measured to the dollar (the harness doesn't separately log the cash-vs-trim split per event), so treat $88,516.45 as an upper-bound estimate of trim-driven turnover, not an exact figure — flagged as a measurement limitation, not asserted as precise.

As a share of activity:
- **$88,516 / $124,000 total deposited** = 71.4% of all capital ever deposited was cycled through a forced-sell-to-repay transaction at some point in the window.
- Spread over the ~5.1-year window, that's roughly **14pp of deposited capital per year** in repayment-driven turnover — a real, ongoing trading cost this analysis does not price (no transaction-cost or tax-impact model exists anywhere in this harness or in `allocate.py`'s live logic; both are silent on trading costs by design, per the account's cash brokerage assumption).

## 5. Return impact

| | Ann. TWR | Gap vs control |
|---|---:|---:|
| Control (D-0, no repayment) | 35.59% | — |
| Model B | 33.28% | **-2.32pp** |

Crosses the 2.0pp decision threshold (§ below). Directionally unsurprising: continuously harvesting gains into debt reduction means less capital stays invested/levered at any given moment than the no-repayment control, and this window was a strongly rising one — the opportunity cost of de-risking shows up directly as lower TWR in a bull window, the same shape of result `trim_backtest.md`'s never-trim control demonstrated for an unrelated mechanism in an unrelated test.

## 6. Drawdown impact

| | MaxDD | Gap vs control |
|---|---:|---:|
| Control (D-0) | -26.81% | — |
| Model B | -24.74% | **+2.07pp** (improvement — less negative) |

Also crosses the 2.0pp decision threshold. A real, measured drawdown improvement — a portfolio carrying less debt through any given point in the window has proportionally less leverage-amplified downside when prices fall, exactly the mechanism the profit-harvest model is designed to produce.

## 7. Risk-adjusted interpretation

A simple TWR/|MaxDD| ratio (higher = more return per unit of realized drawdown in this window, not a Sharpe/Sortino substitute — no volatility-of-returns normalization, no risk-free rate):

| | Ann. TWR | MaxDD | TWR / |MaxDD| |
|---|---:|---:|---:|
| Control (D-0) | 35.59% | -26.81% | 1.328 |
| Model B | 33.28% | -24.74% | 1.345 |

By this specific, simple ratio, Model B comes out **marginally ahead** (1.345 vs 1.328) despite its lower raw TWR — the MaxDD improvement (2.07pp) slightly more than compensates for the return cost (2.32pp) when expressed as a ratio rather than a raw gap. This is offered as one lens, not a verdict: `annualized_volatility_pct` also improved for Model B (24.36% vs 25.87% for control), consistent in direction with the MaxDD finding — a less-levered-on-average path was both less volatile and shallower at its worst point, at the cost of some upside capture in a window that happened to reward staying maximally invested.

**This is not a decision.** Per `docs/PHASE3_FINDINGS.md` §8/§9: whether a 2.32pp return cost is "worth" a 2.07pp drawdown improvement is exactly the kind of judgment call `trim_backtest.md`'s precedent handles by looking at the *leverage-amplified* version of the worse-case scenario, not just the aggregate portfolio number — that decomposition has not been done for Model B here (it would require identifying Model B's own single-name/single-period worst case the way `t1t2_trim_backtest.md` did for NVDA), and doing so is explicitly out of scope for this analysis pass (would require additional computation beyond what Phase 3E already produced, bordering on a new experiment). Flagged as a natural next step, not performed here.

## 8. What this analysis deliberately does not do

- Does not tune `repay_fraction` away from 25% — the `{10%, 25%, 50%}` sweep named in the manifest remains unrun.
- Does not change the HWM trigger mechanism.
- Does not run any new scenario — every number above is derived from the same Model B run already reported in `docs/results/PHASE3_SCENARIO_RESULTS.md`, re-inspected at the event level.
- Does not render a verdict on whether Model B should be adopted. That is an open item (`docs/PHASE3_FINDINGS.md` §9), requiring its own explicit approval step and, per this repo's standing backtest discipline, likely its own single-name-decomposition pass before any adoption decision — the same bar every prior mechanical-rule decision in this project's Decisions Log has cleared.
