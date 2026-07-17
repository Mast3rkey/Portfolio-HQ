# Phase 3C: Scenario Configuration — Specification

_2026-07-17 · Documentation only. No backtests run. No scenario has been executed against real data. This document fixes every configuration value each of the four `docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` scenarios (A/B/C/D) will run with, BEFORE any run happens — the same pre-committed discipline as every closed backtest in this repo (`rung_backtest.md`, `regime_backtest.md`, `trend_backtest.md`, `weight_backtest.md`, `trim_backtest.md`, `t1t2_trim_backtest.md`). Companion documents: `docs/PHASE3C_DATA_VALIDATION_REPORT.md` (what real data these values are checked against) and `docs/PHASE3C_ASSUMPTION_REGISTRY.md` (every value below, individually labeled Known/Estimated/Hypothetical)._

All four scenarios share one substrate — same universe, same window, same benchmark set, same weight scheme, same trim rule — so only the dimension named in each scenario's own letter (leverage level, or repayment policy) varies between arms. This mirrors every prior backtest's "hold everything constant except the one thing being tested" discipline.

---

## Shared configuration (all scenarios)

| Parameter | Value | Source |
|---|---|---|
| Universe | 63 tickers (T1: 9, T2: 15, ETF: 3, band: 33, spec: 5, minus SPCX/SKHY — insufficient price history, `MIN_HISTORY=210` bars) | `targets.yaml`, verified live via `backtest_regime.universe()` + `load_bars()`: 63 of 65 roster tickers pass the history filter |
| Crypto sleeve | Excluded | Same exclusion as every prior backtest (`rung_backtest.md` through `t1t2_trim_backtest.md`) — crypto has no timing gates, its inclusion would confound leverage-specific comparisons the same way it would confound gate comparisons |
| Time window | 2021 → 2026 (exact start/end dates determined by `data/backtest/*.json` cache alignment at run time — same as every prior backtest; `AAPL.json` spans 2020-07-27 → 2026-07-10, other tickers may start later, the standing `MIN_HISTORY`/eligibility logic in `backtest_regime.setup()` handles this) | `data/backtest/` cache, 65 files, verified present |
| Deposit cadence | $2,000/month, deposit day = first eligible trading day of each calendar month (identical to every prior backtest's `DEPOSIT = 2000.0` monthly cadence) | `backtest_regime.py`'s existing `DEPOSIT` constant, reused unchanged |
| Tier weight scheme | T1 3.35% · T2 1.65% · ETF 2.30% · band 0.75% (cap 1.25×) · spec 1.00% (fixed) | `targets.yaml`, matches `backtest_regime.TIER_WEIGHTS` exactly — already validated separately (`weight_backtest.md`: NO CHANGE verdict) and held constant here, not re-tested |
| Trim rule | band/spec overweight above cap + RSI(14) > 60 → mechanical trim to target | `targets.yaml` `gates.trim_rsi=60`, matches `backtest_regime.BAND_CAP=1.25`/`TRIM_RSI=60.0` — already validated separately (`trim_backtest.md`: KEEP 1.25x/RSI 60 verdict) and held constant, not re-tested |
| T1/T2 concentration ceiling | **Excluded from this run.** `t1t2_trim_backtest.md`'s own universe was the same 63-ticker set and already isolated this rule's effect at zero leverage; re-including it here would confound the leverage-specific question these scenarios exist to answer. Held at "no T1/T2 trim" (matches that backtest's Arm A control) for all of A/B/C/D. | Scoping decision, this document |
| Cluster caps (semis/power_infra/oil) | **Excluded from this run**, same reasoning as the T1/T2 ceiling — these are correlation/concentration risk limits, not leverage policy, and were validated independently of leverage. Test D (Concentration interaction) is the ONLY place cluster-cap proximity re-enters, per `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.D — and even there, only as a `concentration_risk_score()` input, not as an active trim in the simulation itself. | Scoping decision, this document |
| Regime/trend gates | **Excluded** (already dropped from production per `regime_backtest.md`/`trend_backtest.md` verdicts — not re-introduced here) | Matches current production `plan()` behavior |
| Rebalance frequency | Monthly, driven entirely by the deposit cadence — no separate rebalance-only cycle (matches production: `allocate.py` only runs on a deposit or an explicit `--review`, never on a timer) | Doctrine — `CLAUDE.md`'s workflow section |
| Min lot | $1 (not the production $25) for these simulations, to avoid a min-lot artifact dominating a comparison at simulation-scale dollar amounts far below the real account's current size | Scoping decision — flagged as a deviation from production's `min_lot_dollars: 25`, since `CLAUDE.md`'s Open Items already notes $25 "doesn't scale with book size" at small simulated book values early in the window |
| Simulation engine | `margin_simulation.py`'s `simulate()` (Phase 3B) | `margin_simulation.py`, tested (129 passing tests as of Phase 3B) |

---

## A. Unlevered baseline

| Parameter | Value |
|---|---|
| Starting portfolio | $0, first deposit initiates the account (matches every prior backtest's starting assumption — no seed capital) |
| Leverage cap | 1.0x (`scenario_unlevered()`) — margin structurally unavailable |
| Interest assumption | N/A (no debt is ever possible at 1.0x) |
| Repayment rule | N/A |
| Benchmark role | The control every other scenario is compared against for Test A (margin drag) |
| Limitations | None specific beyond the shared limitations below — this is the simplest, most-validated-shape arm (identical in kind to every prior backtest's own baseline) |

## B. Fixed leverage baseline ("current allocation")

| Parameter | Value |
|---|---|
| Starting portfolio | $0 (same as A) |
| Leverage cap | 1.8x — the real, current, doctrine-fixed cap (`targets.yaml` `margin.leverage_cap`) |
| Interest assumption | 5.00% APR, first $1,000 of debt interest-free, simple daily accrual capitalized into the debt balance (`CLAUDE.md` doctrine's stated term — see Assumption Registry for why this is Estimated, not Known) |
| Repayment rule | MODEL_0 — no active repayment policy, matching production's actual current behavior (margin is drawn to fund allocation gaps, never proactively repaid beyond what a real Robinhood trim/paydown already did — this simulation has no analog for an ad hoc real-world paydown decision) |
| Benchmark role | "Current allocation" benchmark named in `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §4 — compared against A for Test A, and is the fixed point Tests B/C/D vary from |
| Limitations | Simulates margin available from day one of a simulated $0-start account; the real account's margin history (discovered mid-course, not present from account inception — see `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`) has no equivalent starting condition. This scenario answers "what if margin had been available and used passively from day one," not "what actually happened to this account." |

## C. Leverage sweep

| Parameter | Value |
|---|---|
| Starting portfolio | $0 (same as A/B), one independent simulation per level (not a single account switching leverage mid-run) |
| Leverage levels | 1.2x, 1.4x, 1.6x, 1.8x, 2.0x — five points, matching the range named in `PHASE2_IMPLEMENTATION_PLAN.md` §8 item 2 (1.2x-2.0x), at 0.2x increments; 1.8x is included so this sweep also reproduces Scenario B as one of its own points (a built-in consistency check between the two scenario families) |
| Interest assumption | Same 5.00% APR / $1,000-free term at every level (interest rate is a broker term, not a function of the chosen cap) |
| Repayment rule | MODEL_0 at every level (isolates the leverage-level effect; repayment variants are Test D's job, not C's) |
| Benchmark role | Gates the CAUTION/RESTRICTED soft-threshold placeholders in `targets.yaml`'s Phase 2 schema (`states.caution.leverage_fraction_of_cap`, `states.restricted.leverage_fraction_of_cap`) — explicitly does **not** re-litigate the 1.8x hard cap itself (doctrine, not backtest-gated, per `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.B) |
| Limitations | Each level is evaluated only against this window's own historical drawdowns (the 2021-2022 bear stretch is, per every prior backtest's standing caveat, the only real bear stretch in the sample) — a level that survives this window's worst case is not proven to survive a worse one. The single-name decomposition method (`worst_case_concentration_impact()`, Phase 3B) is intended to supplement the portfolio-level MaxDD at each level, per Test B's stated method in the framework doc, precisely because portfolio-level MaxDD alone already proved (in `t1t2_trim_backtest.md`'s NVDA case) too smooth to surface a leverage-critical single-name event. |

## D. Repayment models

| Parameter | Value |
|---|---|
| Starting portfolio | $0 (same as A/B/C) |
| Leverage cap | 1.8x, fixed across all four repayment variants — held constant per `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.C, so only repayment behavior varies |
| Interest assumption | Same 5.00% APR / $1,000-free term across all four |
| Repayment rules — four named models, per `margin_simulation.py`'s `scenario_repayment_variants()`: | |
| — MODEL_0 (control) | No active repayment policy — same as Scenario B; the reference point the other three are measured against |
| — MODEL_A | Permanent leverage — repay only the minimum required to clear a hard leverage-cap breach, nothing proactive otherwise |
| — MODEL_B (Profit Harvest) | **Resolved 2026-07-17, see `PHASE3_SCENARIO_MANIFEST.md` §1/§2.** Trigger: new portfolio high-water mark. Repays 25% (sweepable {10%, 25%, 50%}) of gains above the prior HWM. No additional/opportunistic borrowing. |
| — MODEL_C (Risk Reset) | **Resolved 2026-07-17, see `PHASE3_SCENARIO_MANIFEST.md` §1/§2.** Trigger: 15% drawdown from peak. Resets to 1.25x target leverage. Restoration requires both a new equity high and leverage normalized (≤1.25x) since the reset. No dip-buying interpretation — structural guarantee, not yet property-tested (manifest §4). |
| Benchmark role | Gates the repayment waterfall's tiers 2 and 4 (`PHASE2_IMPLEMENTATION_PLAN.md` §6) |
| New metric | "Time near buffer floor" — implemented as `time_near_leverage_cap_pct_proxy` (Phase 3B), NOT a true buffer% derivation; see `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §2/§3 and `margin_simulation.py`'s module docstring for why |
| Limitations | Parameters are resolved (see manifest), but the harness (`margin_simulation.py`) does not yet implement either mechanic — `PHASE3_SCENARIO_MANIFEST.md` §4 names this as required pre-execution work. **D still cannot run until that harness extension exists and has its own passing tests**, same discipline as before, now blocked on implementation rather than parameter choice. |

---

## Shared limitations (apply to all four scenarios)

1. **Hypothetical, not historical.** Every scenario simulates a synthetic $0-start account through real historical prices — none reproduce this account's real, short, largely undocumented margin history (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`). See `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §3/§5 for the output-language rule this implies, and `PHASE3C_DATA_VALIDATION_REPORT.md` for exactly what's real vs. assumed.
2. **One window, one mostly-rising sample.** Every prior backtest in this repo carries this same caveat forward (`regime_backtest.md`, `t1t2_trim_backtest.md`) — 2021-2026 contains one real but not prolonged bear stretch (2022). A leverage policy's true stress test — a sustained, severe bear market — is not well-represented in this data.
3. **No real interest-paid data to validate the 5% APR assumption against** (`docs/MARGIN_DATA_INVENTORY.md` Category C) — every interest-cost number these scenarios produce is only as good as that single disclosed constant.
4. **No real buffer% is computed** — `time_near_leverage_cap_pct_proxy` is a distinct, honestly-scoped substitute, not a Robinhood-methodology buffer% (see Scenario D row above and Phase 3B's module docstring).
5. **Behavioral effects are out of scope**, same standing caveat as every prior backtest — these scenarios report numbers, not the psychological cost of carrying leverage through a drawdown.

---

## Open items — status

- ~~Model B's repayment mechanic/parameter~~ — **resolved 2026-07-17**, `PHASE3_SCENARIO_MANIFEST.md` §1 (HWM-gains-repay, R=25%, sweepable).
- ~~Model C's trigger/target/restoration mechanic~~ — **resolved 2026-07-17**, `PHASE3_SCENARIO_MANIFEST.md` §1 (15% drawdown trigger, 1.25x reset target, new-high + normalized-leverage restoration).
- ~~Volatility-spike triggering for Model C~~ — **resolved by omission, 2026-07-17**: not implemented; Model C's trigger is drawdown-only for this initial parameter set (manifest §3, assumption #4/#7's related scoping). Not silently dropped — recorded as a stated scope decision.
- ~~Concentration-trigger threshold~~ — **resolved 2026-07-17**: 30% cluster concentration, explicitly a test parameter, not doctrine, and explicitly NOT blended into Model C's own trigger (manifest §1/§3, assumption #7).
- ~~Pre-committed decision thresholds for D~~ — **resolved 2026-07-17**: 2.0pp TWR difference OR 2.0pp MaxDD improvement, applied uniformly across D's model comparisons, explicitly labeled a decision threshold not a proof threshold (manifest §1, assumption #8). A/B/C's own thresholds remain the repo's standard 1.0pp/1.0pp pattern, unchanged.

**New blocker, replacing the parameter gap:** `PHASE3_SCENARIO_MANIFEST.md` §4 item 1 — the harness (`margin_simulation.py`) does not yet implement either resolved mechanic. **No scenario runs until that harness-extension work exists and has its own passing tests** (same "tests before integration" discipline as every prior phase), not decided ad hoc when the run happens.
