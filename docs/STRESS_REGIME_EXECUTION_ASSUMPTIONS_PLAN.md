# Stress-Regime Execution Assumptions — Research Plan

> **⚠️ Hypothetical, simulated — a design document, not a result.** No stress-regime analysis has been run. Every number this plan will eventually produce describes a synthetic $0-start account simulated through real historical prices, with a further hypothetical execution-friction assumption layered on top during detected stress periods — never a claim about this account's real trading conditions. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies to every output this plan produces.

_Written 2026-07-17, per `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 10, elevated to priority 2 in that document and confirmed as the highest-information-value next question in `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md`'s closing discussion. Documentation only — no code, no simulation changes, no production files touched. Do not implement until this plan is approved._

---

## 1. Research objective

### What question this closes

**How would repayment mechanics behave during adverse market regimes where drawdown, volatility, liquidity pressure, and portfolio stress occur simultaneously?** More precisely: does Model B's already-established friction profile (transaction cost, tax) change in *character* — not just magnitude at a flat rate — when repayment events are examined specifically at the moments they actually occur relative to real market stress, rather than treated as uniformly distributed across a calm-and-stressed window alike.

### Why transaction costs and taxes do not answer it

Both prior sensitivity passes applied their assumption **uniformly across the entire event stream**, regardless of when each event occurred:

- `docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md` applied a flat bps rate to every repayment event, whether it happened during a calm month or (if it did at all) during the account's own worst episode.
- `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md` did the same with a flat tax rate.

Neither pass asked two questions this plan exists to ask:

1. **Timing**: do Model B's repayment events cluster during, before, or after real market stress at all — or does the mechanism (triggered only by a new net-equity high) structurally tend to fire during *calm, rising* periods, making the stress-timing question close to moot for Model B specifically? This is an empirical question about *when* events happen, not *how much* each one costs — neither prior pass measured it.
2. **Regime-conditional friction magnitude**: even if events do occur during stress, is a flat bps/tax-rate assumption realistic for those specific days, or does real-market friction (spread widening, reduced liquidity, slower fills) plausibly scale up exactly when a forced trade is least convenient to execute? Both prior passes were silent on this by construction, applying the same rate everywhere.

This is also distinct from the *concentration* research line's own stress case (`docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 2/5, `docs/PHASE4A_RESEARCH_REPORT.md`'s stress case 3) — that work tests whether a *concentrated position* behaves worse under margin during a market decline. This plan tests whether the *repayment mechanism's own execution* behaves differently under stress, for Model B specifically (or any future mechanical rule with the same shape) — a related but separate question, not to be conflated or merged with the concentration line's own stress construction.

## 2. Known vs. Unknown

### Known

- **Existing repayment events.** The exact day-index and dollar amount of every Model B repayment event, for `repay_fraction` ∈ {10%, 25%, 50%}, already produced and verified in `docs/results/PHASE3_SENSITIVITY_RESULTS.json`, reused (not re-simulated) by both prior sensitivity passes and reusable again here without any new simulation run.
- **Repayment mechanics.** `ModelBProfitHarvest`'s trigger condition (fires only on a new net-equity high-water mark) — read directly from `margin_simulation.py`, unchanged. This mechanic itself is directly relevant to §1's timing question: a mechanism that only fires on new highs has a structural bias toward firing during rising, not falling, periods — a real, Known fact about the mechanism, not a hypothesis this plan needs to test from scratch.
- **Leverage constraints.** `_leverage_capped_margin()`'s existing leverage-cap clipping logic and the fixed 1.8x cap used throughout every prior Model B scenario — read directly, unchanged, not re-examined or re-swept by this plan.
- **Existing simulation framework.** `margin_simulation.py`'s `simulate()` engine, entirely unmodified — this plan, like the two before it, requires re-running already-approved scenario configurations only to recover per-event detail, never changing how they execute.

### Unknown

- **True liquidity conditions.** No live order-book, bid-ask, or market-depth data exists anywhere in this repo for any historical date. `data/backtest/*.json` bars carry `v` (volume) and `h`/`l` (intraday high/low) alongside the `c` (close) every prior Phase 3/4 script has used exclusively — real, historical, already-cached data, confirmed present by direct inspection, but volume and range are *proxies* for liquidity/volatility, not direct measurements of spread or depth.
- **Bid/ask expansion during stress.** No real spread data exists at any granularity (the same gap `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` §4 already established for the calm-market case) — whether spreads widen during detected stress periods, and by how much, is unknowable from this repo's data and will remain a disclosed Hypothetical assumption if modeled at all.
- **Execution slippage during stress.** This harness (like every prior Phase 3/4 scenario) assumes instant, full execution at that day's close price, with no slippage modeled ever, calm or stressed. This plan does not resolve that — it is named here as a standing, unresolved simplification, not solved by this research.
- **Investor behavior effects.** Whether a real human executing Model B's mechanical trims would behave differently (delay, override, panic-sell alongside the mechanical trim) during a real stress episode is unknowable from any data this project has — the same category of gap `regime_backtest.md`'s and `t1t2_trim_backtest.md`'s own behavioral caveats have already named for other mechanisms.

## 3. Stress scenarios

Two tiers, mirroring the historical-primary/hypothetical-secondary hierarchy `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` and `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` both already used, extended here with an explicit prohibition list per this plan's own instruction.

### Historical-primary: real stress-period detection, no invented events

A stress-period detector built entirely from **real, already-cached OHLCV data** (`data/backtest/*.json`'s `h`, `l`, `v` fields — confirmed present, never previously used by any Phase 3/4 script, which have all read `c` only) — for example, days where a ticker's `(h - l) / c` (intraday range as a fraction of close, a realized-volatility proxy) or portfolio-level aggregate volatility exceeds its own historical norm, and/or `v` falls below a trailing average (a liquidity-pressure proxy). This detector identifies **when real stress occurred**, using real historical facts — it does not construct or assume any event that didn't happen. Model B's already-known event timestamps (§2) are then cross-referenced against these detected windows to answer the timing question directly: do repayment events cluster inside, outside, or independently of detected stress periods.

This tier requires **no simulation change** — it operates entirely on the raw cached price files and the already-known event list, external to `simulate()`.

### Hypothetical-secondary: regime-conditional friction multiplier, explicitly bounded

Once real stress periods are identified (historical-primary, above), a **disclosed, explicitly Hypothetical** multiplier (e.g., 2x-3x the already-approved 5bps/15bps transaction-cost tiers, or the already-approved 15%/32% tax tiers) may be applied *only* to repayment events falling inside a detected stress window, leaving events outside those windows at the already-tested flat rates. This tests "if friction really is worse during stress" as an explicit sensitivity, not a claim. The multiplier value itself is a disclosed assumption requiring its own approval before use — this plan does not fix a specific value, only the structure (a bounded multiplier applied conditionally, not an unconditional new baseline rate).

### Explicit prohibitions on scenario construction

- **Do not invent fake historical events.** No synthetic crash, no constructed price path for any ticker, unlike `phase4a_lib.apply_synthetic_shock()`'s approach in the concentration research line (deliberately not reused here — that tool exists for a different research question, per §1's scope note). Every "stress period" in this plan is a real, detected historical date range, or it doesn't exist in this plan's evidence.
- **Do not assume unsupported liquidity conditions.** Volume and intraday range are real, cached, historical data — legitimate to use as *proxies*. They are not bid-ask spread data, and no output may present a proxy-derived figure as if it were measured spread/depth.
- **Do not assume execution guarantees.** This plan does not claim, model, or imply that a repayment trim would actually fill at the assumed price (shocked or not) during a real stress episode — the instant-fill-at-close simplification (§2) remains an acknowledged, unresolved limitation throughout, not something this plan's hypothetical multiplier "fixes."

## 4. Metrics

Reusing existing derived-metric functions wherever they already exist, adding only what genuinely doesn't:

| Metric | Source |
|---|---|
| TWR impact | `backtest_regime.twr_annualized()`, reused via `transaction_cost_lib.cost_adjusted_twr()`'s existing pattern (already reused twice, by the cost and tax passes) |
| MaxDD | `backtest_regime.max_drawdown()`, unchanged |
| Recovery time | `phase4a_lib.worst_drawdown_recovery()`, already built and tested in Phase 4A, directly reusable |
| **Repayment timing relative to drawdown** (new) | Requires a new, small, execution-layer function comparing each repayment event's day-index against the nearest detected stress window and/or the portfolio's own drawdown trough (`worst_drawdown_recovery()`'s `trough_index`, already available) — a distance-in-days or inside/outside-window classification, not a new engine capability |
| **Turnover concentration** (new, and explicitly distinct from Phase 4A's *position*-concentration metrics — a different meaning of "concentration," disambiguated here to avoid confusion with `docs/PHASE4A_RESEARCH_REPORT.md`'s NVDA/semis work) | What fraction of total repaid dollars occurs inside detected stress windows versus outside them — a new, small function over the already-known event list and the historical-primary detector's output, no engine change |
| Threshold exposure | `phase4a_lib.time_above_threshold_pct()`, already built, reusable for leverage or stress-detector-derived series |

No metric in this list requires a `margin_simulation.py` change — every one operates on already-exposed `SimulationResult` fields (`events`, `book_values`, `leverage_series`) or the raw cached price files, matching this plan's "no simulation changes" constraint exactly.

## 5. Materiality

**Reused, not reinvented**, per this plan's explicit instruction:

- **2.0pp material / 0.5pp noise floor** for TWR/MaxDD gaps — `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3, unchanged.
- **≥5%-of-days threshold-exposure bar** — §6 of the same document, reused for the new turnover-concentration and threshold-exposure metrics.
- **Recovery materiality (≥1.5x baseline or ≥20 absolute trading days)** — §7 of the same document, reused for the recovery-time metric.
- **The adopted future outcome gate** — per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s adoption (recorded in `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §8b): "Evidence supports" requires a material gap AND (repeated forced-deleveraging events OR material threshold-exposure degradation). This plan's research cycle is exactly the kind of *future* cycle that adoption was written for — it applies here by default, not Phase 4A's original, narrower AND-only gate.

**No new success criteria, threshold value, or materiality band is introduced by this plan.**

## 6. Prohibited conclusions

Explicitly, per this plan's own instruction:

- **No selecting repayment parameters** — `repay_fraction` remains at its already-approved 10%/25%/50% values, reused exactly, never re-swept or narrowed to a preferred value by this analysis.
- **No recommending implementation** — this plan does not conclude Model B (or any repayment mechanism) should be deployed, adjusted, or avoided in production, under any stress-regime finding in either direction.
- **No changing doctrine** — `targets.yaml`'s margin schema remains entirely `null`; `CLAUDE.md`'s Decisions Log is untouched by this plan or its eventual execution.
- **No changing leverage caps** — the 1.8x cap is Known (§2), read-only, and not a variable this plan tests, sweeps, or proposes adjusting, under any stress finding.

Also carried forward from §3's prohibitions, restated here as conclusions (not just construction) constraints:

- No claim that a volume/range-derived proxy constitutes measured liquidity or spread data.
- No claim that any hypothetical friction multiplier represents a validated or expected real-world value.
- No claim that this harness's instant-fill-at-close assumption has been resolved or validated by this analysis.

---

## What this plan deliberately does not do

- Does not run any stress-detection, timing, or friction-multiplier calculation.
- Does not modify `margin_simulation.py`, `phase4a_lib.py`, `transaction_cost_lib.py`, `tax_treatment_lib.py`, or any other code.
- Does not fix a specific hypothetical-secondary multiplier value — that remains an open parameter requiring its own approval before use, named but not decided here.
- Does not merge with, or duplicate, the concentration research line's own market-drawdown stress case (`docs/PHASE4A_RESEARCH_REPORT.md` stress case 3, `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 2/5) — related, deliberately kept separate.
- Does not select, recommend, or change any repayment parameter, doctrine entry, or leverage cap.

Stopping here. Awaiting approval before implementation.
