# Phase 3 Decision Gate

> **⚠️ Hypothetical, simulated — this gate approves nothing about this account's real history.** Every finding referenced below comes from a synthetic $0-start account simulated through real historical prices. This document's sole purpose is to state, in one place, exactly what evidence exists, what it shows, what it does not show, and — explicitly — what has and has NOT been decided as a result. It is a checkpoint, not a decision. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies here too.

_Written 2026-07-17, after Phase 3F review. No simulation was run to produce this document; no simulation logic was modified. This is a synthesis and gate-check of work already done, not new research._

---

## 1. Evidence completed

**Phase 3A — Evidence framework** (`docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md`): defined four questions (Test A margin drag, Test B sustainability, Test C repayment policy, Test D concentration interaction), data availability, output-language rules, and the benchmark framework. No code, no data pulled.

**Phase 3B — Simulation harness** (`margin_simulation.py`, `test_margin_simulation.py`): isolated, hypothetical-only simulation engine. Built and unit-tested on synthetic data only — no real scenarios run at this phase.

**Phase 3C — Scenario preparation** (`docs/PHASE3C_SCENARIO_CONFIGURATION.md`, `docs/PHASE3C_DATA_VALIDATION_REPORT.md`, `docs/PHASE3C_ASSUMPTION_REGISTRY.md`): fixed every configuration value for Scenarios A/B/C/D, re-verified all underlying data live (65 price files, 63 eligible tickers, live `targets.yaml`/`holdings.yaml` state), and labeled every parameter Known/Estimated/Hypothetical. Left Model B/C's mechanics as open items.

**Phase 3D — Model B/C implementation** (`margin_simulation.py` extended): resolved Model B (Profit Harvest: HWM trigger, 25% of gains repaid) and Model C (Risk Reset: 15% drawdown trigger, 1.25x reset target, dual restoration condition) per `docs/PHASE3_SCENARIO_MANIFEST.md`. Two real formula bugs found and fixed during implementation (HWM tracked on `book` vs `net_equity`; trim-funded vs cash-funded target-leverage math). Structural "no leverage increase" guarantee added and property-tested. 142 tests passing, no production files touched.

**Phase 3E — Execution** (`run_phase3e_scenarios.py`, `docs/results/PHASE3_SCENARIO_RESULTS.md`, `docs/results/phase3_scenario_results.json`): ran Scenarios A, B, C (5-level sweep), and D (4 repayment models) against real historical prices — 63-ticker universe, 2021-06-01 to 2026-07-10, 62 monthly $2,000 deposits, commit `585c117`. Configuration printed and asserted against the manifest/execution record before running.

**Phase 3F — Review and findings** (`docs/PHASE3_FINDINGS.md`, `docs/results/PHASE3_MODEL_B_ANALYSIS.md`): consolidated all of the above into one readable record; produced a detailed per-event analysis of Model B's 296 repayment events, without tuning parameters or running new scenarios.

**Scenarios executed:** A (unlevered), B (1.8x, no repayment), C-1.2x/1.4x/1.6x/1.8x/2.0x, D-MODEL_0 (control), D-MODEL_A (permanent leverage), D-MODEL_B (profit harvest), D-MODEL_C (risk reset). **Not executed:** Test D from the evidence framework (concentration interaction) — no code exists for the 30% concentration stress trigger.

**Findings:** summarized in §2 below, detailed in `docs/PHASE3_FINDINGS.md` §6 and `docs/results/PHASE3_SCENARIO_RESULTS.md`.

## 2. Confirmed findings

These are observations from one simulated window — confirmed as *observed in this run*, not confirmed as general truths about margin, this account, or any future period.

**Margin drag (Test A, Scenario A vs B):** in this window, the simulated 1.8x-levered account returned more (35.59% vs 30.01% ann. TWR, +5.58pp) and drew down more (-26.81% vs -22.41% MaxDD, -4.40pp) than the unlevered control. Both gaps exceed the repo's standard 1.0pp decision threshold. Leverage amplified the outcome in both directions — it did not, in this window, provide return without a corresponding drawdown cost.

**Leverage sweep behavior (Test B, Scenario C):** results were identical across 1.4x, 1.6x, 1.8x, and 2.0x — only 1.2x showed a measurably different (lower) result. The simulated account's own deposit-driven margin demand never asked for more capacity than roughly a 1.4x cap already provides in this window. This says the specific level of the cap between 1.4x and 2.0x didn't matter *in this window* — it is not a finding that 2.0x is safe, since the mechanism was never actually stressed against that ceiling here.

**Model B findings (Test C, Scenario D-B):** fired 296 times, repaid $88,516.45 gross, reduced final debt by $43,786 net versus the no-repayment control (roughly half the gross figure, since the account's normal margin draws continue independently). Cost 2.32pp of annualized TWR, bought 2.07pp of MaxDD improvement — crosses the 2.0pp decision threshold in both directions. A simple TWR/|MaxDD| ratio (1.345 vs 1.328 control) favors Model B marginally, offered as one lens, not a verdict — the single-name-decomposition step this repo's precedent (`t1t2_trim_backtest.md`'s NVDA case) applies before any adoption decision has not been performed for Model B.

**Model C non-trigger finding (Test C, Scenario D-C):** the 15% net-equity drawdown trigger fired **zero times** in this window — verified directly via event count, not inferred from identical output numbers. This diversified 63-ticker simulated portfolio never drew down more than 15% from its own peak in 2021-2026, even though individual names (e.g. NVDA, per `reports/t1t2_trim_backtest.md`'s decomposition of the same window) fell far more. This is a real finding about diversification smoothing away the trigger in this specific window — not evidence the mechanism is broken; `test_margin_simulation.py`'s unit and property tests already prove Model C's logic behaves correctly in isolation.

## 3. Unknowns

Named explicitly so they are never silently assumed answered by the above:

- **Concentration interaction** — the 30% cluster-concentration stress trigger from `docs/PHASE3_SCENARIO_MANIFEST.md` has no implementation. Whether concentration should ever tighten real deployable margin capacity (versus only a display state, its current status) is completely untested.
- **True interest cost** — every scenario used a 5.00% APR assumption (Estimated, not Known). No interest-paid ledger exists anywhere in this system to validate that figure against. The real cost of carry could differ from what these results assume.
- **Transaction costs** — no trading-cost or slippage model exists anywhere in this harness, in `allocate.py`, or in this repo generally. Model B's ~71%-of-deposited-capital turnover (`docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4) is reported with zero cost attached to it — a real-world version of this policy would incur trading costs this analysis cannot price.
- **Tax effects** — entirely absent. Repeated trim-and-repay cycles (Model B, Model C) would realize gains/losses in a real taxable context; nothing in this project has ever modeled tax consequences, and this phase does not begin to.
- **Real historical margin behavior** — this account's actual margin debt has been observed at only 7 discrete points, confined to a 3-day window in July 2026 (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`). None of Phase 3's simulated results describe what this account's real leverage history would have produced, because that history does not exist in recoverable form. This is not a gap Phase 3 can close — it is a permanent limitation of the available data, restated from Phase 3A onward.

## 4. Explicit statements

- **No doctrine changes are approved.** Nothing in Phase 3A-3F alters any entry in `CLAUDE.md`'s Decisions Log. The 1.8x leverage cap and 30% buffer floor remain doctrine-fixed, unchanged, and unrelitigated by this work.
- **No leverage cap changes are approved.** The leverage sweep (Scenario C) is reported as observed only (§2) — no new cap value has been adopted, proposed for adoption, or written into `targets.yaml`. `targets.yaml`'s live `margin.leverage_cap` remains 1.8, untouched throughout Phase 3.
- **No repayment parameters have been changed.** Model B's `repay_fraction` remains at its initial 25% value — the `{10%, 25%, 50%}` sweep named in the manifest as future work has not been run. Model C's `drawdown_trigger_pct` (15.0) and `reset_leverage` (1.25) are unchanged from their initial values. No repayment model has been enabled in production — `targets.yaml`'s proposed margin schema (`states`, `concentration_adjustment`, repayment sub-keys) remains entirely absent from the live file, exactly as it has been since Phase 2.

## What this gate deliberately does not do

- Does not run any simulation. No new arms, no re-runs, no sensitivity tests.
- Does not modify `margin_simulation.py`, `allocate.py`, `targets.yaml`, or `holdings.yaml`.
- Does not decide whether to proceed to parameter sensitivity testing, whether to implement the concentration-interaction dimension, or whether to adopt any finding into doctrine — those are separate, future approval steps, not exercised here.

Stopping here. This gate is a checkpoint only. Awaiting direction before any parameter sensitivity work begins.
