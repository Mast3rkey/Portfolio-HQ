# Phase 3 Scenario Results

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history. Every scenario below simulates a synthetic $0-start account through real historical prices (data/backtest/*.json). See `docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §3/§5 for the required output-language rule this report follows.

_Executed 2026-07-17 at commit `585c117c65fb1c95b661450fcd8347979743818c` (see `docs/PHASE3_EXECUTION_RECORD.md`). Window: 2021-06-01 to 2026-07-10. Universe: 63 tickers. 62 monthly $2,000 deposits. No parameter below was tuned after seeing results — every value was fixed in `docs/PHASE3_SCENARIO_MANIFEST.md` before this run and is restated verbatim here._

## Scenario A vs B — unlevered vs current fixed leverage

| Scenario | Ann. TWR | CAGR | MaxDD | Ann. Vol | Time near cap (proxy) | Final book | Final debt |
|---|---:|---:|---:|---:|---:|---:|---:|
| A — unlevered | 30.01% | 172.15% | -22.41% | 23.43% | 100.0% | $327,180 | $0 |
| B — 1.8x, no repayment | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |

B − A gap: +5.58pp annualized TWR, -4.40pp MaxDD (more negative = worse). Decision threshold: 1.0pp. Gap exceeds the pre-committed threshold — reported as observed, not interpreted or acted on in this document.

## Scenario C — leverage sweep

| Level | Ann. TWR | CAGR | MaxDD | Ann. Vol | Time near cap (proxy) | Final book | Final debt |
|---|---:|---:|---:|---:|---:|---:|---:|
| C-1.2x | 35.03% | 181.54% | -26.81% | 25.72% | 49.0% | $388,860 | $79,763 |
| C-1.4x | 35.59% | 182.69% | -26.81% | 25.87% | 11.3% | $396,976 | $147,745 |
| C-1.6x | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |
| C-1.8x | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |
| C-2.0x | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |

## Scenario D — repayment models

| Model | Ann. TWR | CAGR | MaxDD | Ann. Vol | Time near cap (proxy) | Final book | Final debt |
|---|---:|---:|---:|---:|---:|---:|---:|
| MODEL_0 | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |
| MODEL_A | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |
| MODEL_B | 33.28% | 178.60% | -24.74% | 24.36% | 0.0% | $368,615 | $103,959 |
| MODEL_C | 35.59% | 182.69% | -26.81% | 25.87% | 0.0% | $396,976 | $147,745 |

Gaps vs D-0 (control), decision threshold 2.0pp (TWR OR MaxDD improvement — a decision threshold, not a proof threshold):

| Model | TWR gap vs D-0 | MaxDD gap vs D-0 | Crosses decision threshold? |
|---|---:|---:|---|
| MODEL_A | +0.00pp | +0.00pp | No |
| MODEL_B | -2.32pp | +2.07pp | Yes |
| MODEL_C | +0.00pp | +0.00pp | No |

Reported as observed. No parameter was adjusted, re-run, or swept in response to these numbers — Model B's repay_fraction sweep ({10%, 25%, 50%}) named in the manifest as future work was NOT run here, and no threshold above was chosen after seeing a result.

## Limitations (carried forward, not re-litigated)

- Concentration stress trigger (30%) is not wired into any executable code — Scenario D's concentration-interaction dimension was not exercised (per `PHASE3_EXECUTION_RECORD.md` §4).
- `time_near_leverage_cap_pct_proxy` is NOT a real Robinhood buffer% — see `margin_simulation.py`'s module docstring.
- One window, one mostly-rising sample (2021-2026) — the 2022 stretch is the only real bear-market representation.
- Interest rate (5.00% APR) is Estimated, not Known — no real interest-paid ledger exists to validate it against.
- Model C's trigger requires a >15% net-equity drawdown from this simulated account's own peak — it **fired 0 times in this window**, which is why MODEL_C's row above is identical to MODEL_0's: this diversified 63-ticker portfolio's net equity never drew down >15% from its own peak in 2021-2026, even though individual names (see `reports/t1t2_trim_backtest.md`'s NVDA decomposition, a different test, same window) had far worse single-name drawdowns — portfolio-level diversification smoothed the trigger away. A real, honest finding, not a bug: it says this window doesn't exercise Model C's mechanism, not that the mechanism doesn't work (see the unit/property tests in `test_margin_simulation.py` for that).
- Model B's HWM-gain trigger fired 296 times, repaying $88,516 total across the window — unlike Model C, this window DOES exercise Model B's mechanism (a steadily rising simulated portfolio sets new highs often).

_Advisory-adjacent research only. This report places no orders and makes no recommendation. Execute nothing based on this document alone._
