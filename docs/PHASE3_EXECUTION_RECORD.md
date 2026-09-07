# Phase 3 Execution Record

> **⚠️ Hypothetical, simulated — not a claim about this account's real history.** Every scenario this record covers simulates a synthetic $0-start account through real historical prices. None of it reconstructs this account's real, short, largely undocumented margin history (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`). No result derived under this record may be described as what margin, leverage, or any repayment model "would have made" — see `docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §3 and `margin_simulation.py`'s `BANNED_PHRASES` enforcement for the required framing. This disclaimer applies to every scenario run logged under this record, present and future, not only the entries that exist at the time of writing.

_Created 2026-07-17. Documentation only — this is a pre-execution snapshot of the exact code, tests, and parameters that will govern Phase 3 scenario runs. No scenario has been executed as of this writing. Do not alter simulation logic to produce this record — every value below was read from the repo as it exists at the commit stated, not adjusted to fit._

---

## 1. Code state

| Item | Value |
|---|---|
| Commit hash | `585c117c65fb1c95b661450fcd8347979743818c` |
| Branch | `claude/earnings-gate-aapl-nvda-q0tjut` |
| Commit date | 2026-07-17 04:25:44 +0000 |
| Commit subject | "Phase 3D: implement finalized Model B/C mechanics in margin_simulation.py" |
| Python | 3.11.15 |

Any scenario execution logged against this record must be run at this exact commit (or a later one, explicitly noted as such) — if `margin_simulation.py`, `backtest_regime.py`, or any dependency changes after this record is written, a fresh execution record is required before running further scenarios, not a silent reuse of this one.

## 2. Test suite result

**142 passed**, 0 failed, 0 skipped, full repo suite (`python3 -m pytest -q`), run at the commit above. Breakdown relevant to the simulation harness specifically: `test_margin_simulation.py` — 55 passed, covering `PortfolioState`, the re-derived leverage-cap math, `ModelBProfitHarvest`/`ModelCRiskReset` (unit + state-leak + property tests), the four scenario builders, `simulate()` end-to-end, output-language enforcement, and three regression tests proving Scenarios A/B/C's exact pre-refactor numeric output is unchanged after the Phase 3D stateful-policy refactor.

No test was added, removed, or modified to produce this record — this is the same 142 reported at the end of the Phase 3D implementation turn, re-verified fresh for this record rather than carried over from memory.

## 3. Scenario versions

Per `docs/PHASE3_SCENARIO_MANIFEST.md` (finalized parameters) and `docs/PHASE3C_SCENARIO_CONFIGURATION.md` (shared configuration), as implemented in `margin_simulation.py` at the commit above:

| Scenario | Builder | Repayment mechanism | Implementation status |
|---|---|---|---|
| A — Unlevered baseline | `scenario_unlevered()` | N/A (leverage_cap=1.0) | Implemented, tested (Phase 3B, regression-verified Phase 3D) |
| B — Fixed leverage baseline | `scenario_fixed_leverage(1.8, ...)` | MODEL_0 (none) | Implemented, tested (Phase 3B, regression-verified Phase 3D) |
| C — Leverage sweep | `scenario_leverage_sweep([1.2, 1.4, 1.6, 1.8, 2.0], ...)` | MODEL_0 at every level | Implemented, tested (Phase 3B, regression-verified Phase 3D) |
| D — Repayment models | `scenario_repayment_variants(leverage_cap=1.8, ...)` | MODEL_0 (control), MODEL_A, MODEL_B (`ModelBProfitHarvest`), MODEL_C (`ModelCRiskReset`) | Implemented, tested (Phase 3D) |

## 4. Parameters

Restated from `docs/PHASE3_SCENARIO_MANIFEST.md` §1 and `docs/PHASE3C_SCENARIO_CONFIGURATION.md`, exactly as coded at the commit above — not re-derived, not adjusted.

### Shared (all scenarios)
- Universe: 63 tickers, verified live at this commit via `backtest_regime.universe()` + `load_bars()` (`MIN_HISTORY=210`) — 63 of 65 roster tickers pass; SPCX and SKHY excluded for insufficient history.
- No crypto sleeve.
- Deposit cadence: $2,000/month (`backtest_regime.DEPOSIT`).
- Tier weights: T1 3.35% / T2 1.65% / ETF 2.30% / band 0.75% / spec 1.00% (`backtest_regime.TIER_WEIGHTS`, matches `targets.yaml` live).
- Trim rule: band cap 1.25×, spec fixed at target, RSI(14) > 60 (`backtest_regime.BAND_CAP`/`TRIM_RSI`).
- T1/T2 concentration ceiling and cluster caps (semis/power_infra/oil): excluded from the simulated trim logic (scoping decision, `PHASE3C_SCENARIO_CONFIGURATION.md`).
- Regime/trend gates: excluded (matches current production — already dropped per `regime_backtest.md`/`trend_backtest.md`).
- Min lot: $1 for simulation purposes (deviates from production's $25 — documented deviation, `PHASE3C_SCENARIO_CONFIGURATION.md`).
- Interest: 5.00% APR, first $1,000 of debt interest-free (Estimated, not Known — see `PHASE3C_ASSUMPTION_REGISTRY.md` #10).

### Scenario C — leverage sweep levels
`1.2x, 1.4x, 1.6x, 1.8x, 2.0x`.

### Scenario D — repayment models

| Model | Parameters as coded |
|---|---|
| MODEL_0 | none |
| MODEL_A | `leverage_cap=1.8` (breach-clearing only) |
| MODEL_B (`ModelBProfitHarvest`) | `repay_fraction=0.25` (initial run; sweepable `{0.10, 0.25, 0.50}` not yet run) |
| MODEL_C (`ModelCRiskReset`) | `drawdown_trigger_pct=15.0`, `reset_leverage=1.25` |

Concentration stress trigger (30% of book, per cluster): defined in the manifest as a Test D interaction-analysis parameter, **not yet wired into any executable code** — `margin_simulation.py` has no concentration-scoring integration as of this commit. Any scenario run claiming to exercise the concentration-interaction dimension before that integration exists would be describing something that isn't implemented; this record states that gap explicitly so it can't be silently assumed present in a later summary.

### Decision threshold
2.0 percentage points TWR difference OR 2.0 percentage points MaxDD improvement, applied uniformly across Scenario D's model comparisons — a **decision threshold, not a proof threshold** (per explicit instruction, `PHASE3_SCENARIO_MANIFEST.md` §1). Scenarios A/B/C use the repo's standard 1.0pp/1.0pp pattern.

## 5. Data sources

| Source | Detail |
|---|---|
| Price history | `data/backtest/*.json` — 65 files present at this commit, one per roster ticker. Verified live: `AAPL.json` spans 2020-07-27 → 2026-07-10, 1,496 daily bars. |
| Universe/weights/caps | `targets.yaml`, read live at this commit (not modified by this record or by Phase 3B/3C/3D). |
| Real margin state (context only, not a scenario input) | `holdings.yaml`'s `margin` block — last confirmed in `PHASE3C_DATA_VALIDATION_REPORT.md`: debt $1,628.64, buffer 61.77%, synced 2026-07-15. No scenario in this record starts from this state; every scenario starts from $0 (Hypothetical, per `PHASE3C_ASSUMPTION_REGISTRY.md` #9). |
| Interest rate term | `CLAUDE.md` doctrine text ("~5% APR, first $1,000 free") — Estimated, not a data feed; no interest-charge ledger exists to validate it against (`PHASE3C_DATA_VALIDATION_REPORT.md`, Missing section). |
| Simulation engine | `margin_simulation.py` at commit `585c117` (this record's stated commit). |

No data source has changed since `docs/PHASE3C_DATA_VALIDATION_REPORT.md` was written — this record does not re-run that validation, it relies on that document's findings, current as of this commit.

## 6. Execution date

**No scenario has been executed as of this record's creation date, 2026-07-17.** This section exists as a template row to be filled in at the time a scenario is actually run — left blank here deliberately, not populated with a placeholder date that could be mistaken for a real one:

| Scenario/model run | Execution date | Executed by | Result artifact |
|---|---|---|---|
| _(none yet)_ | — | — | — |

---

## What this record deliberately does not do

- Does not run any scenario. No arms, no numbers, no verdicts.
- Does not modify `margin_simulation.py`, `allocate.py`, `targets.yaml`, or `holdings.yaml`.
- Does not implement the concentration stress trigger (30%) — flagged in §4 as not yet wired into executable code.
- Does not sweep Model B's `repay_fraction` — only the single initial 25% configuration is recorded as ready to run.

Stopping here for review, per instruction. No scenarios executed.
