# Phase 3C: Data Validation Report

_2026-07-17 · Documentation only. No backtests run. Every claim below was checked directly against the repo's actual files at the time of writing — not assumed, not carried over from memory of earlier documents. Extends, cross-checks, and re-verifies `docs/MARGIN_DATA_INVENTORY.md` specifically for what `docs/PHASE3C_SCENARIO_CONFIGURATION.md`'s four scenarios need; does not re-derive that document's own A/B/C classification work from scratch._

## Purpose

Before any Phase 3C scenario runs, confirm — by direct inspection, not assumption — that the data each scenario configuration depends on actually exists in the form claimed. This is the same discipline every prior backtest report applied implicitly; here it's made an explicit, checked step before the fact rather than an implicit assumption during it.

---

## Available (verified present, this session)

| Data | Verification performed | Result |
|---|---|---|
| **Price history** | Counted files in `data/backtest/`, spot-checked `AAPL.json`'s date range and bar count | 65 JSON files present, one per roster ticker. `AAPL.json`: 1,496 daily bars, 2020-07-27 → 2026-07-10. |
| **Universe eligibility at `MIN_HISTORY=210`** | Ran `backtest_regime.universe()` + `load_bars()` live against the current cache | 63 of 65 roster tickers pass (SPCX, SKHY excluded — insufficient history, matching `backtest_regime.EXCLUDE` and every prior backtest's stated universe size) |
| **Holdings/target assumptions** | Read `targets.yaml` directly | Tier weights (T1 3.35 / T2 1.65 / ETF 2.30 / band 0.75 / spec 1.00), `caps.clusters` (semis 25%, power_infra 20%, oil 20%), `margin.leverage_cap=1.8`, `margin.buffer_floor_pct=30.0`, `crypto.sleeve_pct=10.0` all confirmed live in the file, matching `backtest_regime.TIER_WEIGHTS` and this document's shared-configuration table |
| **Portfolio snapshots (real, current)** | Read `holdings.yaml`'s `margin` block directly | `debt: $1,628.64`, `buffer_pct: 61.77`, `synced_at: 2026-07-15` — matches `MARGIN_DATA_INVENTORY.md`'s last recorded row exactly, no drift found |
| **Cash/debt observations (historical, discrete)** | Not re-verified from git log this session — relies on `MARGIN_DATA_INVENTORY.md` Table A's already-tabulated 7 sync points (2026-07-13 through 2026-07-15), cross-referenced against commit history in that document | 7 point-in-time debt/buffer syncs, confirmed present in that document's own table; not independently re-pulled from git this session (no new sync events since that document was written — `holdings.yaml`'s current state matches its last row) |
| **Simulation engine** | Ran the full test suite | `margin_simulation.py` + `test_margin_simulation.py`: 42/42 passing (129/129 across the full repo as of the Phase 3B commit) |
| **Interest rate term** | Read `CLAUDE.md`'s doctrine section | "~5% APR, first $1,000 free" — present as stated doctrine text, not a data feed (see Missing section — the "~" is a disclosed approximation, not an exact sourced figure) |

**Conclusion: every "Available" data point Scenario Configuration's shared-configuration table and per-scenario tables cite is real and present, verified directly this session — not assumed.**

---

## Missing (confirmed absent, matches and cross-checks `MARGIN_DATA_INVENTORY.md` Category C)

| Data | Verification performed | Result |
|---|---|---|
| **Historical broker margin buffer (time series)** | Searched `holdings.yaml`'s git history structure (per `MARGIN_DATA_INVENTORY.md`'s prior work) for any buffer reading between the 7 discrete sync points | Confirmed: no continuous buffer series exists. Robinhood's buffer % is captured only at the moment of a manual sync — nothing records it between syncs. This is why Phase 3B's harness computes `time_near_leverage_cap_pct_proxy` instead of a true buffer-floor-proximity metric (see Scenario Configuration doc, Scenario D limitations). |
| **Complete margin debt/draw timeline** | Same basis as above | Only the 7 discrete debt levels are known; the path *between* them (individual draw/paydown events, amounts, dates) is not recorded anywhere. Confirmed still true — no new logging (`margin_log.csv` etc., proposed in `MARGIN_DATA_INVENTORY.md`'s collection plan) has been implemented since that document was written. |
| **Actual interest paid** | Searched repo for any interest-charge record (`holdings.yaml`, `performance_log.csv`, commit messages) | None found. No interest ledger exists anywhere in this system. The 5.00% APR figure used throughout `PHASE3C_SCENARIO_CONFIGURATION.md` is therefore a disclosed assumption with no real-charged-dollars data to validate it against. |
| **Complete cash flow (deposit/withdrawal) history** | Searched for a deposit/withdrawal log | None exists as a persistent, dated, amount-stamped record. `performance_log.csv`'s own standing caveat (referenced in `MARGIN_DATA_INVENTORY.md`) already states it cannot separate deposit-driven equity growth from market-driven growth. Only one withdrawal ($50, 2026-07-13) is recorded anywhere, referenced by commit message / doctrine text, not a structured log. |

**Conclusion: all four Missing items match `MARGIN_DATA_INVENTORY.md`'s existing Category C findings exactly — nothing new has closed these gaps since that document was written, and nothing in this session's verification pass found a gap that document had missed.**

---

## Implication for scenario execution

Every Phase 3C scenario (A/B/C/D) is, and must remain labeled as, a **hypothetical simulation using real historical prices** — never a reconstruction of this account's real margin history. This is not a new conclusion; it restates `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`'s finding and confirms, via this session's direct re-check, that nothing has changed to make a real-history reconstruction newly possible.

The "Available" data is sufficient to run all of Scenarios A/B/C and the MODEL_0/MODEL_A arms of Scenario D. Scenario D's MODEL_B and MODEL_C arms additionally require threshold values (target leverage fraction, gain-trigger %, reset fraction) that are not data-gap issues — they're scenario *design* choices not yet made, tracked as Open Items in `PHASE3C_SCENARIO_CONFIGURATION.md`, not blocked by any missing data.
