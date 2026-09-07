# Phase 3 Findings

> **⚠️ Hypothetical, simulated.** Every number in this document describes a synthetic $0-start account simulated through real historical prices — none of it describes this account's real margin history. This account's real margin debt has been observed at only 7 discrete points, all within a 3-day window in July 2026 (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`), and leverage never approached the 1.8x cap during that observed window. **Nothing below should ever be phrased as a direct causal claim that leverage or margin itself produced a given return figure for this real account.** The required framing throughout is: "under these assumptions, a simulated investor following this policy through [window] historical prices experienced [outcome]." See `docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §3/§5 for the full list of disallowed phrasings and the required alternative.

_Written 2026-07-17, consolidating Phase 3A (evidence framework) through Phase 3E (execution) into a single findings record. Supersedes no prior document — `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md`, `PHASE3_SCENARIO_MANIFEST.md`, `PHASE3_EXECUTION_RECORD.md`, and `docs/results/PHASE3_SCENARIO_RESULTS.md` remain the detailed source-of-record for each phase; this document is the readable summary that ties them together. No simulation logic was modified to produce this document._

---

## 1. Experiment scope

Phase 3 asked four questions, defined in `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1:

- **Test A (margin drag)** — would the account's strategy have performed better unlevered? → Scenario A vs B.
- **Test B (sustainability)** — what leverage levels survive this window's historical drawdowns? → Scenario C.
- **Test C (repayment policy)** — when does paying down margin improve risk-adjusted outcomes? → Scenario D.
- **Test D (concentration interaction)** — does concentration risk affect real deployable margin capacity? → **Not executed.** The 30% concentration stress trigger named in `PHASE3_SCENARIO_MANIFEST.md` was never wired into any executable code (`PHASE3_EXECUTION_RECORD.md` §4), so Phase 3E's run covers Tests A/B/C only. Test D remains open.

This document reports what Phase 3E actually ran — Scenarios A, B, C, and D's four repayment models (MODEL_0/A/B/C) — against Tests A, B, and C above. It does not answer Test D.

## 2. Universe

63 tickers — the current T1/T2/ETF/band/spec roster (`targets.yaml`), minus SPCX and SKHY (insufficient price history, `MIN_HISTORY=210` bars). Verified live at execution time via `backtest_regime.universe()` + `load_bars()`. No crypto sleeve. Same universe, weights (T1 3.35%/T2 1.65%/ETF 2.30%/band 0.75%/spec 1.00%), and band/spec trim rule (1.25×/RSI>60) as every prior backtest in this repo.

## 3. Dates

**Window: 2021-06-01 to 2026-07-10** — 1,283 trading days, 62 monthly $2,000 deposits ($124,000 total deposited across the window). This window is set by data availability (`data/backtest/*.json`'s actual coverage and each ticker's own eligibility, per `backtest_regime.setup()`'s existing alignment logic) and each of the 63 tickers' `MIN_HISTORY=210`-bar eligibility — not chosen to include or exclude any particular market event.

**Execution date: 2026-07-17**, at commit `585c117c65fb1c95b661450fcd8347979743818c` (Phase 3D). Full provenance in `docs/PHASE3_EXECUTION_RECORD.md`.

## 4. Assumptions

Restated from `docs/PHASE3C_ASSUMPTION_REGISTRY.md` and `docs/PHASE3_SCENARIO_MANIFEST.md` §3 — labeled Known / Estimated / Hypothetical, not re-derived here:

| Assumption | Value | Label |
|---|---|---|
| Starting capital | $0 for every scenario | Hypothetical |
| Deposit cadence | $2,000/month | Hypothetical |
| Interest rate | 5.00% APR, first $1,000 free | Estimated (doctrine's own "~5%" admits it isn't exact; no interest-paid ledger exists to check it against) |
| Min lot | $1 (deviates from production's $25) | Hypothetical, disclosed deviation |
| Leverage cap (B, D) | 1.8x | Known (matches `targets.yaml` live) |
| Leverage sweep levels (C) | 1.2x, 1.4x, 1.6x, 1.8x, 2.0x | Hypothetical |
| Model B repay fraction | 25% (sweep {10%, 25%, 50%} not run) | Hypothetical, this session's initial parameter |
| Model C drawdown trigger / reset leverage | 15% / 1.25x | Hypothetical, this session's initial parameters |
| Decision thresholds | A/B/C: 1.0pp (repo standard); D: 2.0pp (explicitly a decision threshold, not a proof threshold) | Hypothetical |
| T1/T2 ceiling, cluster caps, regime/trend gates | Excluded from simulated trim logic | Scoping decision, isolates the leverage-specific question |

## 5. Scenarios tested

| Scenario | Configuration | Status |
|---|---|---|
| A — Unlevered baseline | leverage_cap=1.0 | Executed |
| B — Fixed leverage | leverage_cap=1.8, MODEL_0 | Executed |
| C — Leverage sweep | 5 levels, MODEL_0 at each | Executed |
| D-0 — No active repayment (control) | leverage_cap=1.8 | Executed |
| D-A — Permanent leverage | forced-breach repay only | Executed |
| D-B — Profit Harvest | 25% of gains above HWM | Executed |
| D-C — Risk Reset | 15% drawdown trigger, 1.25x target | Executed |

Configuration was printed and asserted against `PHASE3_SCENARIO_MANIFEST.md`/`PHASE3_EXECUTION_RECORD.md` before execution (`run_phase3e_scenarios.py`'s `print_and_confirm_configuration()`).

## 6. Results

Full tables in `docs/results/PHASE3_SCENARIO_RESULTS.md`; summarized here.

**A vs B (Test A — margin drag):**

| | Ann. TWR | MaxDD |
|---|---:|---:|
| A — unlevered | 30.01% | -22.41% |
| B — 1.8x levered | 35.59% | -26.81% |
| Gap (B−A) | +5.58pp | -4.40pp |

Both gaps exceed the 1.0pp decision threshold. In this window, the simulated levered account both returned more AND drew down more — leverage amplified the outcome in both directions, exactly as doctrine describes it (`CLAUDE.md`: "leverage amplifies whatever edge already exists... it is not itself a source of edge").

**C — leverage sweep (Test B — sustainability):**

Results are **identical from 1.4x upward** in this window (35.59% TWR / -26.81% MaxDD at 1.4x, 1.6x, 1.8x, and 2.0x alike) — the leverage-cap constraint stops binding above roughly 1.4x for this universe and period; the account's own deposit-driven margin demand never asked for more than a ~1.4x ceiling would allow. Only 1.2x showed a measurably different (lower) result. This says the specific *level* of the cap between 1.4x and 2.0x didn't matter in this window — it does not test the cap's behavior in a scenario that would actually draw it that far (a data/window limitation, not a result about the cap being safe at 2.0x).

**D — repayment models (Test C — repayment policy):**

| Model | TWR gap vs D-0 | MaxDD gap vs D-0 | Crosses 2.0pp threshold? |
|---|---:|---:|---|
| D-A (permanent leverage) | +0.00pp | +0.00pp | No |
| D-B (profit harvest) | -2.32pp | +2.07pp (improvement) | **Yes** |
| D-C (risk reset) | +0.00pp | +0.00pp | No |

- **D-A identical to control**: no hard leverage-cap breach ever occurred in this simulated run, so Model A's forced-breach-only logic never had anything to do.
- **D-B crosses the decision threshold**: fired 296 times, repaid $88,516 total (gross), for a net $43,786 lower final debt than the control ($103,959 vs $147,745). Cost 2.32pp of annualized TWR, bought a 2.07pp MaxDD improvement. Full breakdown in `docs/results/PHASE3_MODEL_B_ANALYSIS.md`.
- **D-C identical to control, verified**: the 15% net-equity drawdown trigger fired **zero times** in this window — confirmed directly via event count, not inferred from identical numbers. This diversified 63-ticker portfolio's net equity never fell more than 15% from its own peak in 2021-2026, even though individual names had far worse drawdowns (`reports/t1t2_trim_backtest.md`'s NVDA decomposition, same window: -66.4% peak-to-trough on that single name). This is a real finding about diversification smoothing the trigger away, not evidence the mechanism is broken — `test_margin_simulation.py`'s unit and property tests already prove the mechanism works correctly in isolation.

## 7. Limitations

- **One window, one mostly-rising sample.** 2021-2026 contains one real but brief bear stretch (2022) — the standing caveat on every backtest in this repo. Model C's trigger never firing is a direct symptom: this window doesn't contain a portfolio-level drawdown severe enough to test that mechanism.
- **Concentration interaction (Test D from the evidence framework) was not executed** — the 30% cluster stress trigger has no code behind it yet.
- **Leverage sweep is inconclusive above 1.4x** for the reason stated in §6 — this window's deposit-driven margin demand never asked for more room than that, so C doesn't actually test 1.6x-2.0x's behavior under real stress within this account's demand pattern.
- **`time_near_leverage_cap_pct_proxy` is not a real Robinhood buffer%** — see `margin_simulation.py`'s module docstring; never compare it numerically against a real synced buffer_pct.
- **Interest rate is Estimated, not Known** — no real interest-paid ledger exists to check the 5.00% APR assumption against.
- **Every scenario starts from $0** — none of this reconstructs the real account's actual margin-discovery moment or its real (short, 3-day-observed) leverage history.
- **No parameter was tuned after seeing results.** Model B's `{10%, 25%, 50%}` repay-fraction sweep remains unrun, by design — running it now, after seeing that 25% crosses the threshold, would not be "more evidence," it would be parameter search dressed as a backtest.

## 8. Disclaimer

**This document, and everything in `docs/results/PHASE3_SCENARIO_RESULTS.md` and `docs/results/PHASE3_MODEL_B_ANALYSIS.md`, is hypothetical and simulated.** It describes what a simulated $0-start account, following stated rules, experienced when run against real historical prices — not this account's real history, not a prediction, not a recommendation. No result here is, or should be treated as, a doctrine decision. Adopting any of Model B, Model C, a different leverage cap, or any threshold observed in this phase into `CLAUDE.md`'s Decisions Log or `targets.yaml`'s live configuration requires an explicit, separate approval step — this document reports findings, it does not decide anything.

## 9. Open items

- Test D (concentration interaction) remains unexecuted — no code exists to run it.
- Model B's decision-threshold crossing (§6) is reported, not acted on — whether to adopt Model B's profit-harvest mechanic into `targets.yaml`'s (still entirely `null`) margin schema is an open question for a future, explicit approval step, not decided here.
- Model C's mechanism is untested by this window (zero triggers) — whether it "works" in the sense of improving outcomes during a real drawdown remains unanswered by this data, not falsified by it.
- The leverage sweep (C) needs a window or universe that actually stresses margin demand past ~1.4x before it can say anything about 1.6x-2.0x specifically.
