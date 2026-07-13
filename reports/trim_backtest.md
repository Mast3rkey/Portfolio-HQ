# Trim backtest — is 1.25x / RSI 60 the right profit-taking rule?
_2026-07-13 · window 2021-06-01 → 2026-07-10 · 37 band/spec tickers · $2,000/mo × 62 deposits_

**Pre-committed rule (fixed before results):** adopt an alternative only if it beats BOTH the current rule (A) and never-trim (D) by >1.0pp annualized TWR; D beating A by the same margin means trims are drag; inside the threshold = no change. One test, one verdict.

| Arm | Ann. TWR | Final value | MaxDD | Trims | $ trimmed | Largest final position |
|-----|---------:|------------:|------:|------:|----------:|-----------------------:|
| A — current (1.25x / RSI 60) | 32.60% | $395,471 | -24.6% | 82 | $156,009 | KLAC 3.6% |
| B — tighter (1.15x / RSI 55) | 32.50% | $393,189 | -24.5% | 153 | $195,686 | PLTR 3.6% |
| C — looser (1.40x / RSI 65) | 32.85% | $398,382 | -25.2% | 51 | $131,430 | AMAT 4.1% |
| D — never trim (control) | 39.25% | $493,511 | -28.6% | 0 | $0 | RKLB 12.6% |
| E — mechanical 1.25x, no RSI gate | 32.73% | $396,760 | -24.3% | 130 | $183,218 | PLTR 3.6% |

Gaps vs current (A): B−A: -0.10pp · C−A: +0.26pp · D−A: +6.65pp · E−A: +0.13pp

## Verdict
**TRIMS ARE DRAG — never-trim beats the current rule by >1.0pp annualized. TWR says drop the trim; concentration-control value must be weighed separately before acting.**

_One window, one mostly-rising sample. The threshold exists because a small edge in one sample is noise, not signal. Trims also serve concentration control, which TWR alone doesn't price._
