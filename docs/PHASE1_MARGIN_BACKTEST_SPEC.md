# Phase 1 Research Specification — Margin vs. Unlevered Baseline

_2026-07-17 · Documentation only. No code changes. This is the research specification for the first backtest in the Margin Intelligence research program (see `docs/MARGIN_DOCTRINE.md` for the governing philosophy, `docs/MARGIN_INTELLIGENCE_DESIGN.md` for the full engine design this backtest gates). Governing question: **has margin, at the cost and structure this account actually uses, produced a better risk-adjusted outcome than not using it?** Not implemented until reviewed and approved._

---

## 0. A finding that changes the spec, surfaced before anything else

The request that produced this spec described Portfolio A as "the actual historical portfolio: holdings, contributions, margin debt, interest cost" — implying a literal replay of this account's real history. **That cannot be built.** Checked directly before writing anything else:

- `performance_log.csv` has **4 rows total**, starting 2026-07-13 — the day the existing margin debt was *discovered*, not the day it originated. There is no earlier data.
- The margin debt itself was never tracked from origin. `CLAUDE.md`'s Decisions Log: "Discovered ~$4,423 in existing margin debt... contradicting the prior 'no margin' rule." The debt already existed when found; nothing records when it was drawn, at what price levels, against what holdings, or what it funded.
- `holdings.yaml` stores only **current** position state (`shares`, `crypto_shares`) — there is no historical share-count ledger anywhere in the repo. The current file cannot be "rewound."

**Consequence:** Portfolio A cannot be "this account's real history." Every other backtest in this repo (`backtest_regime.py`, `backtest_trend.py`, `backtest_trims.py`, `backtest_weights.py`, `backtest_rungs.py`, `backtest_t1t2_trim.py`) already resolves an identical problem the same way — none of them replay this account's real deposit/trade history either. They all simulate a **hypothetical portfolio**, running the current production rules (universe, weight scheme, deposit cadence, trim rules) forward through the real historical price window (`data/backtest/*.json`, 2021–2026). Phase 1 uses that same, already-established method. This is not a workaround invented for this spec — it's the existing, proven pattern this whole framework already runs on, applied to a new question.

**What this means concretely:** Portfolio A ("with margin") and Portfolio B ("without margin") are both simulated portfolios, identical in every respect (universe, weights, deposits, trim rules) except for one variable: whether a stated, explicit **margin-draw policy** is active. Section 2 defines that policy precisely, because — unlike the price data — there is no real historical policy to inherit either. The Decisions Log's 1.8x cap was set at "the level already in place when discovered," not derived from a stated draw policy, so Section 2 has to propose one rather than replay one.

---

## 1. Required historical inputs

| Input | Source | Status |
|---|---|---|
| Daily bars, 63 T1-spec tickers, 2021–2026 | `data/backtest/*.json` (existing cache) | **Available**, reused unchanged from every prior backtest. |
| QQQ daily bars (for the volatility/regime-descriptive context, not for gating) | `data/backtest/QQQ.json` | **Available.** |
| Simulated deposit schedule | Reuse `DEPOSIT = 2000.0`, first trading day of each month — the exact convention every existing backtest already uses | **Available, by convention**, not new data. |
| Tier weights, cluster caps, T1/T2 ceiling | `targets.yaml` | **Available** — same production values every backtest holds constant, per the framework's standing "isolate one variable" discipline. |
| Margin interest rate | `CLAUDE.md`: "~5% APR, first $1,000 free" | **Available, but imprecise** — "~5%" is not an exact figure Robinhood publishes as a fixed constant; it moves with the Fed funds rate over time in reality. This backtest will hold it **fixed at 5.00% APR for the entire simulated window**, stated explicitly as a simplifying assumption (Section 2), not a claim that the real rate was constant 2021-2026. |
| Historical margin debt / leverage trajectory | **Does not exist** (Section 0) | **Missing — resolved by simulating a policy, not by sourcing real data (Section 2).** |
| Historical margin-buffer % | **Does not exist** (Robinhood-only, manually synced since 2026-07-14, never logged historically) | **Missing.** Not required for this backtest — buffer % is a Robinhood-specific display figure this simulation cannot reproduce; leverage ratio (gross/net-equity) is used instead throughout, consistent with how every existing margin formula in `margin_capacity()` already treats leverage as the primary computed quantity and buffer as an externally-synced check on it. |

---

## 2. Assumptions (stated explicitly, per the framework's standing discipline of naming every held-constant variable before results exist)

1. **Margin-draw policy for Portfolio A ("with margin"):** on each simulated monthly deposit, if the allocator's gap-fill logic would otherwise leave money on the table (i.e., there are still-underweight names after cash is exhausted) *and* drawing margin would keep leverage at or under the 1.8x cap *and* wouldn't require a buffer check this simulation can't perform (see below) — draw margin to fund the remaining gaps, up to the cap. This mirrors current production's `--margin` mechanism (`margin_capacity()`'s leverage-cap clip) as closely as a simulation without a real buffer feed can. **This is a stated policy choice, not a replay of real decisions** — flagged per Section 0.
2. **No buffer-floor simulation.** The 30% buffer floor is Robinhood's own displayed figure and cannot be derived (`write_state()`'s standing documented constraint: a naive formula doesn't reconcile with Robinhood's real number). This backtest **cannot simulate the buffer floor** and does not claim to — it tests leverage-ratio-gated margin only. This is a real, named limitation, not an oversight: any future backtest of the buffer floor's specific effect needs a different design this spec doesn't attempt.
3. **Interest accrual:** simple daily accrual, `debt_balance × (0.05 / 365)` per day, on the outstanding balance net of the first $1,000 (interest-free per the doctrine's documented term) — i.e., `max(0, debt_balance − 1000) × (0.05/365)` daily, compounding into the debt balance monthly (added to `debt_balance` on the first simulated trading day of each month, consistent with the existing monthly deposit cadence). This is the specific, testable form of "interest drag" the request asked for.
4. **Portfolio B ("unlevered")** runs the identical simulation — same universe, same weights, same deposit schedule, same trim rules — with margin draws disabled entirely: any gap that cash alone can't fund simply goes unfilled that cycle (money redirects to the next-ranked gap, same redirect logic the trend gate already uses elsewhere in this framework, not held as literal idle cash).
5. **Crypto sleeve, trend gate, earnings gate, cluster caps, T1/T2 ceiling all run identically in both arms**, at current production values, exactly as every prior backtest holds non-tested mechanisms constant. The only variable between A and B is the margin-draw policy in assumption 1.
6. **Regime is not a factor in either arm**, consistent with `regime_backtest.md`'s standing verdict and the Margin Doctrine's explicit rejection of regime-gated margin.

---

## 3. Portfolio reconstruction method

Directly reuses `backtest_regime.py`'s existing `setup()` pattern (universe from `targets.yaml`, bars from `data/backtest/`, calendar alignment, monthly deposit-day detection) — no new reconstruction method is needed for the **price/holdings** side of this simulation; only the **margin-draw and interest-accrual** layer is new. This is the "backtest simulation layer" flagged as a gap in `MARGIN_INTELLIGENCE_DESIGN.md` §2 and §6 (Phase 2b) — Phase 1 is where that layer gets built for the first time, scoped narrowly to what this one backtest needs (leverage-gated draws + interest accrual), not built as a speculative general-purpose framework ahead of need.

---

## 4. Interest cost assumptions

Covered precisely in Section 2, assumption 3. Restated as the standalone number the request asked for: **interest drag = cumulative interest accrued and compounded into Portfolio A's debt balance over the full simulated window**, reported both as a total dollar figure and as an annualized drag on TWR (i.e., what Portfolio A's TWR would have been with zero interest cost, for comparison — isolating "did margin itself help" from "did the interest cost eat the benefit").

## 5. Contribution handling

Both arms receive the identical $2,000/month simulated deposit, the same convention every existing backtest in this repo already uses (`DEPOSIT = 2000.0`, first trading day of each month). No contribution difference between arms — the entire comparison isolates the margin-draw policy, nothing else.

## 6. Performance metrics

| Metric | Formula / source | Notes |
|---|---|---|
| CAGR / annualized TWR | `twr_annualized()`, existing, unchanged | Reused directly. |
| Total return | Final value / total deposited − 1 | New, simple, alongside TWR since raw total return and time-weighted return can tell different stories with irregular deposits. |
| Volatility | New — `stdev(daily_return) × sqrt(252)`, per `MARGIN_INTELLIGENCE_DESIGN.md` §3 | Needs its own unit test before use, per that design's Section 4 test plan. |
| Max drawdown | `max_drawdown()`, existing, unchanged | Reused directly. |
| Recovery time | New — for the single largest drawdown event, the number of trading days from trough back to the prior peak value (not "average" — the worst episode is what matters for survivability, consistent with the Margin Doctrine's survivability-first framing) | If the window ends still underwater from the largest drawdown, report "not yet recovered as of window end" explicitly rather than a misleading number. |
| Sharpe-like metric | Per `MARGIN_INTELLIGENCE_DESIGN.md` §3: `(TWR − 0%) / volatility`, risk-free rate fixed at 0% and disclosed | Same formula, same disclosed simplification as the engine design. |
| Worst leverage period | Max value of the leverage time series (Portfolio A only; B is always 0) + the date range it occurred | Descriptive, not gated — just reported. |
| Interest drag | Section 4 | Dollar total + annualized TWR impact. |

## 7. Acceptable conclusions

The request is explicit that all three outcomes are valid findings, not just "adopt" or "reject" — this backtest is diagnostic, not a rule-adoption test in the shape of `trim_backtest.md`. But "diagnostic" doesn't mean unstructured: a pre-committed classification scheme is defined **before** the backtest runs, so the conclusion can't be shaped after seeing the numbers.

**Pre-committed classification, stated now:**
- **Margin net positive:** Portfolio A's Sharpe-like metric exceeds Portfolio B's by more than **0.10** (an arbitrary-but-stated threshold, same spirit as every other backtest's 1.0pp TWR threshold — chosen to be large enough that a marginal, noise-level difference doesn't get over-read either direction) **and** Portfolio A's max drawdown is not more than **5 percentage points** worse than Portfolio B's (a materially worse tail outcome shouldn't be waved through by a Sharpe win alone, same asymmetric-tolerance logic `t1t2_trim_backtest.md` established for MaxDD).
- **Margin neutral / inconclusive:** Sharpe-like metrics within ±0.10 of each other, regardless of which is nominally higher — inside this band, treat it as noise, not a finding either direction.
- **Margin net negative:** Portfolio A's Sharpe-like metric is more than 0.10 *below* Portfolio B's, **or** Portfolio A's max drawdown is more than 5pp worse than B's even if Sharpe looks comparable (a "won on Sharpe, lost on survivability" result counts as net negative under the Margin Doctrine's survivability-first framing, not as a wash).

**What each conclusion means for Phase 2 (Section 8's gate):**
- **Net positive or neutral** → Phase 2 (leverage-level sweep) proceeds as planned, since there's no finding here that argues against continuing to study *what level* of margin is sustainable.
- **Net negative** → Phase 2 does not proceed automatically. Per the request's own framing ("Only after we know margin is useful"), a net-negative Phase 1 result is itself the answer to whether margin has been useful — running a leverage-level sweep in that case would be tuning a mechanism the evidence just argued against, not answering an open question. This becomes a decision point for you, not an automatic next step: continue investigating anyway (e.g., a different repayment discipline might rescue a currently-negative result — that's a legitimate reason to still proceed), or pause the Margin Intelligence build entirely pending that discussion.

---

## 8. Exact artifacts Phase 1 must produce before Phase 2 begins

1. **`backtest_margin_drag.py`** — the simulation script itself, following the established pattern (pre-committed rule stated in the docstring before any result exists, `reports/margin_drag_backtest.md` output), built on `backtest_regime.py`'s shared helpers wherever the logic is genuinely reusable (universe, `twr_annualized`, `max_drawdown`) and new code only for the margin-draw/interest-accrual layer this spec adds.
2. **New, independently tested pure functions** for every new metric (volatility, Sharpe-like, recovery time, interest accrual) — each with its own unit test against a hand-computed small example, per `MARGIN_INTELLIGENCE_DESIGN.md` §4's standing requirement that new financial logic is tested before it's trusted in a real backtest, not after.
3. **`reports/margin_drag_backtest.md`** — the report itself: both arms' full metric table (Section 6), the interest-drag breakdown (Section 4), and an explicit statement of which of the three Section 7 classifications the result falls into.
4. **A `CLAUDE.md` Decisions Log entry**, written in the same style and precision as every prior backtest verdict (including the T1/T2 ceiling entry's standard of stating exactly what was and wasn't tested) — this is the artifact that actually closes the question, not just the report file.
5. **An explicit go/no-go statement for Phase 2**, per Section 7's gate — stated plainly in both the report and the Decisions Log entry, not left implicit in the numbers for a future session to infer.

None of this is built yet. This document is the specification only.

---

## Note on the "next Claude prompt" instruction not to assume an outcome

Restated for the record since it's the operating principle of this entire document: nothing above proposes, hints at, or is structured to favor any particular answer to "is margin useful." The classification thresholds in Section 7 were chosen for symmetry (same ±0.10 band regardless of direction, same 5pp drawdown tolerance regardless of which arm is worse) specifically so the conclusion is determined by the backtest's output, not by this specification's framing.
