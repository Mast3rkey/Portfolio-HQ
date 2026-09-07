# Weight backtest — is the current tier-weight structure arbitrary?
_2026-07-14 · window 2021-06-01 → 2026-07-10 · 63 tickers (T1-spec, no crypto) · $2,000/mo × 62 deposits_

**Pre-committed rule (fixed before results):** adopt an alternative only if it beats current AND every other arm by >1.0pp annualized TWR. Band 1.25x / spec fixed / RSI-60 trim rule held constant across all arms — only the tier-weight scheme varies. One test, one verdict.

| Arm | Ann. TWR | Final value | MaxDD | Trims |
|-----|---------:|------------:|------:|------:|
| A — current (T1 3.35 / T2 1.65 / ETF 2.30 / band 0.75 / spec 1.00) | 28.05% | $309,136 | -20.5% | 64 |
| B — equal-weight (all tickers identical) | 28.41% | $322,124 | -21.8% | 84 |
| C — flatter gradation (T1 2.00 / T2 1.50 / ETF 2.00 / band 1.00 / spec 1.00) | 27.83% | $309,718 | -20.9% | 72 |
| D — steeper gradation (T1 5.00 / T2 1.20 / ETF 2.30 / band 0.40 / spec 0.60) | 28.80% | $308,434 | -20.2% | 31 |

Gaps vs current (A): B−A: +0.37pp · C−A: -0.21pp · D−A: +0.75pp

## Verdict
**NO CHANGE — all arms within the pre-committed noise threshold (1.0pp). Current weighting stays; question closed.**

_One window, one mostly-rising sample. The threshold exists because a small edge in one sample is noise, not signal. Tier weight is also conviction sizing, not just a return-maximization input — even a winning alternative here wouldn't automatically override what specific names you believe in._
