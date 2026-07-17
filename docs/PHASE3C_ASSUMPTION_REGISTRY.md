# Phase 3C: Assumption Registry

_2026-07-17 · Documentation only. No backtests run. Every configuration value used across `docs/PHASE3C_SCENARIO_CONFIGURATION.md` and every future scenario report, labeled exactly one of three ways. This registry is the single place a future report (or a future reviewing session) checks before citing any number from Phase 3C's results — no value should ever be repeated in a report without also carrying its label from here._

## Labels

- **Known** — directly observed, verified against a real file/data source this session or a prior, still-valid one. Not a model, not a choice.
- **Estimated** — not directly observed, but a reasonable, disclosed approximation derived from Known data plus stated reasoning.
- **Hypothetical** — a simulation-design choice with no claim to represent this account's real history or any observed fact. Chosen for the simulation to be runnable, not because it's believed to be true.

A value's label can change between phases only if new data closes the gap (e.g., if `margin_log.csv` from `MARGIN_DATA_INVENTORY.md`'s collection plan is ever implemented and populated, "complete margin debt/draw timeline" could move from unavailable to Known for *future* windows — never retroactively for this window). Nothing in Phase 3C changes any label from `MARGIN_DATA_INVENTORY.md`'s own A/B/C classification; this registry applies those same three categories, renamed to match this document's requested vocabulary (Known ≈ that document's "A) Observable," Estimated ≈ "B) Reconstructable," and Hypothetical is a new category specific to simulation-design choices that document's schema didn't need).

---

## Registry

| # | Value | Used in | Label | Basis |
|---|---|---|---|---|
| 1 | 63-ticker universe (T1/T2/ETF/band/spec, excl. SPCX/SKHY, no crypto) | All scenarios | **Known** | Verified live: `backtest_regime.universe()` + `load_bars()` against the current `data/backtest/` cache, `MIN_HISTORY=210` |
| 2 | Tier weights (T1 3.35% / T2 1.65% / ETF 2.30% / band 0.75% / spec 1.00%) | All scenarios | **Known** | `targets.yaml`, live production config |
| 3 | Band cap 1.25×, trim RSI 60 | All scenarios | **Known** | `targets.yaml` `gates.trim_rsi`; validated separately in `reports/trim_backtest.md` (KEEP verdict) |
| 4 | 1.8x leverage cap (Scenario B, D) | B, D | **Known** | `targets.yaml` `margin.leverage_cap` — the real, current, doctrine-fixed value |
| 5 | 30% buffer floor | Referenced, not directly simulated | **Known** | `targets.yaml` `margin.buffer_floor_pct` — real doctrine value; NOT computed inside the simulation itself (see #14) |
| 6 | Current real margin debt ($1,628.64) / buffer (61.77%) as of 2026-07-15 | Context only — not a scenario input (every scenario starts from $0, not this real state) | **Known** | `holdings.yaml`, re-verified live this session against `docs/PHASE3C_DATA_VALIDATION_REPORT.md`'s check |
| 7 | Leverage sweep levels: 1.2x, 1.4x, 1.6x, 1.8x, 2.0x | C | **Hypothetical** | Simulation-design choice — a chosen sweep range, not an observation. Range itself matches `PHASE2_IMPLEMENTATION_PLAN.md` §8's named 1.2x-2.0x span (a prior planning choice, not new here). |
| 8 | Monthly $2,000 deposit cadence | All scenarios | **Hypothetical** | Simulation-design choice, reused unchanged from every prior backtest's own `DEPOSIT=2000.0` constant (`backtest_regime.py`) — never claimed to represent this account's real, irregular, unlogged deposit history (`docs/MARGIN_DATA_INVENTORY.md` Category C confirms real deposit history isn't recoverable) |
| 9 | $0 starting capital for every scenario | All scenarios | **Hypothetical** | Simulation-design choice, matches every prior backtest in this repo — deliberately not an attempt to reconstruct this account's real starting point or real margin-discovery moment (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`) |
| 10 | 5.00% APR interest rate, first $1,000 free | B, C, D | **Estimated** | `CLAUDE.md` doctrine text states this as the account's real going-forward rate structure — but the "~" in the doctrine's own phrasing ("~5% APR") is itself a disclosed admission this isn't an exact, dated, sourced figure, and no interest-charge ledger exists to validate it against (`docs/PHASE3C_DATA_VALIDATION_REPORT.md` Missing section). One level more grounded than a pure guess (it's Robinhood's stated term, not invented), one level short of Known (never observed as an actual charged dollar amount). |
| 11 | 2021-2026 time window | All scenarios | **Known** (window bound by data), **Hypothetical** (choice to use the full available window rather than a sub-window) | The window's *existence* is Known (bounded by `data/backtest/`'s actual coverage, verified in the Data Validation Report); the *choice* to run the full window rather than, say, isolating just the 2022 bear stretch is a Hypothetical design decision, matching every prior backtest's own precedent |
| 12 | T1/T2 ceiling and cluster caps excluded from A/B/C/D's simulated trim logic | All scenarios | **Hypothetical** | Scoping decision (this phase) to isolate the leverage-specific question from concentration-risk questions already answered separately (`t1t2_trim_backtest.md`, and the semis/power_infra/oil cap decisions in `CLAUDE.md`'s Decisions Log) |
| 13 | Regime/trend gates excluded | All scenarios | **Known** (matches real current production state) | `regime_backtest.md`/`trend_backtest.md` verdicts already removed these from production — Phase 3C doesn't reintroduce them, so this "assumption" is actually just matching the real, current, already-decided system behavior |
| 14 | `time_near_leverage_cap_pct_proxy` in place of a true buffer% metric | All scenarios (metric, not an input) | **Hypothetical**, explicitly **not** a proxy for a Known quantity | No real Robinhood buffer% formula exists to approximate honestly (`CLAUDE.md`'s "never derive buffer% from a formula" guardrail) — this metric measures a different, exactly-computable quantity (distance to the leverage cap) chosen as the best available stand-in, not an estimate of the real buffer% itself. Mislabeling this as "Estimated" would wrongly imply it approximates a real, known-but-unmeasured buffer% — it does not; the real formula is unknown by design. |
| 15 | Model 0 (no repayment) as production's real current behavior | B (repayment rule), D (control arm) | **Known** | Directly matches `allocate.py`'s actual behavior — `plan()` has no proactive repayment logic anywhere; margin is only ever drawn to fund gaps, confirmed by reading the function during Phase 2D integration work |
| 16 | Model A/B/C repayment mechanics (breach-only / target-leverage / gain-or-concentration-triggered) | D | **Hypothetical** | Simulation-design choices — three named policies to compare, none claimed to be what this account has ever actually done (Model 0 already covers "what this account actually does") |
| 17 | Model B's target leverage fraction | D | **Not yet assigned — Open Item** | Per `PHASE3C_SCENARIO_CONFIGURATION.md`'s Open Items list — D cannot run until this is set and entered here as Hypothetical with a stated value |
| 18 | Model C's gain-trigger %, reset fraction, concentration-trigger threshold | D | **Not yet assigned — Open Item** | Same as #17 |
| 19 | Pre-committed decision thresholds (A: 1.0pp/1.0pp; D: proposed 2.0pp) | A, B, C, D verdicts | **Hypothetical** (A/B/C, matching the repo's standing pattern) / **Proposed, not yet confirmed** (D) | `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1 states these as the standing pattern to carry forward; D's stricter 2.0pp bar is explicitly a proposal in that document, not yet a committed number |
| 20 | $1 min-lot for simulation (vs. production's $25) | All scenarios | **Hypothetical**, deviation from production flagged | Scoping decision, `PHASE3C_SCENARIO_CONFIGURATION.md`'s shared-configuration table — chosen to avoid a min-lot artifact dominating comparisons at small simulated early-window dollar amounts |

---

## What this registry deliberately does not do

- Does not assign values to items #17/#18 (Model B/C thresholds) — those remain **Open Items**, not defaulted, per the standing "never guess a numeric parameter without evidence" rule.
- Does not confirm the pre-committed decision thresholds (#19) as final — A/B/C's 1.0pp/1.0pp is the standing pattern to carry forward by default, but D's 2.0pp is explicitly still a proposal awaiting confirmation.
- Does not run any scenario. This document exists so that when a scenario does run, every number in its resulting report can be traced back to exactly one of these three labels, with no ambiguity about how much weight the number should carry.

Stopping here, alongside `docs/PHASE3C_SCENARIO_CONFIGURATION.md` and `docs/PHASE3C_DATA_VALIDATION_REPORT.md`. No scenarios executed. Awaiting approval and resolution of the Open Items before any Phase 3C scenario runs.
