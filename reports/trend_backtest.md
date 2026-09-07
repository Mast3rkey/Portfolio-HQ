# Trend-gate backtest — does the per-ticker 200-SMA gate earn its keep?
_2026-07-14 · window 2021-06-01 → 2026-07-10 · 63 tickers (T1-spec, no crypto) · $2,000/mo × 62 deposits_

**Pre-committed rule (fixed before results):** adopt B (drop the gate) only if it beats A by >1.0pp annualized TWR; A beating B by the same margin means the gate earns its keep; inside the threshold = no change. Weight scheme and trim rule held at current production values; no regime gate in either arm (dropped from production 2026-07-14, before this test). One test, one verdict.

Unlike the regime gate (held deposits as cash — pure drag), a trend-gate block only *redirects* money to the next-ranked gap, still fully invested — so the two arms differ only in *which* names got bought on blocked days.

| Arm | Ann. TWR | Final value | MaxDD | Trims | Buy attempts blocked |
|-----|---------:|------------:|------:|------:|---------------------:|
| A — current (trend gate ON, RSI<30 override) | 27.64% | $302,437 | -20.3% | 60 | 930 |
| B — no trend gate | 28.05% | $309,136 | -20.5% | 64 | 0 |

B − A gap: +0.41pp annualized

## Verdict
**NO CHANGE — within the pre-committed noise threshold (1.0pp). Trend gate stays; question closed.**

_One window, one mostly-rising sample with a single real bear stretch (2022) — the trend gate's actual test case. The threshold exists because a small edge here is noise, not signal._
