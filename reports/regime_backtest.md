# Regime-gate backtest — does the QQQ 200-EMA gate earn its keep?
_2026-07-14 · window 2021-06-01 → 2026-07-10 · 63 tickers (T1-spec, no crypto) · $2,000/mo × 62 deposits_

**Pre-committed rule (fixed before results):** adopt B (drop the gate) only if it beats A by >1.0pp annualized TWR; A beating B by the same margin means the gate earns its keep; inside the threshold = no change. Weight scheme and trim rule held at current production values throughout. One test, one verdict.

| Arm | Ann. TWR | Final value | MaxDD | Deposits held back |
|-----|---------:|------------:|------:|--------------------:|
| A — current (regime gate ON) | 25.49% | $292,409 | -20.1% | 15 |
| B — no regime gate | 28.05% | $309,136 | -20.5% | 0 |

B − A gap: +2.56pp annualized

## Verdict
**DROP THE GATE — no-gate (B) beats current (A) by >1.0pp annualized. The regime gate is cash drag.**

_One window, one mostly-rising sample with only brief bearish stretches — the regime gate's real test is a sustained bear market, which this window barely contains. The threshold exists because a small edge here is noise, not signal._
