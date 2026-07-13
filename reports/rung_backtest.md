# Rung backtest — do buy rungs deserve to exist?
_2026-07-12 · window 2021-06-01 → 2026-07-10 · 65 tickers · $2,000/mo × 62 deposits_

**Pre-committed rule (fixed before results):** adopt B only if it beats both A and C by >1.0pp annualized TWR; C beating A by the same margin kills the rung module; inside the threshold = no change. One test, one verdict.

| Arm | Ann. TWR | Final value | Deposited | MaxDD | Fill rate | Avg fill discount |
|-----|---------:|------------:|----------:|------:|----------:|------------------:|
| A — current rungs | 29.35% | $340,655 | $124,000 | -23.7% | 41% | +5.50% |
| B — S/R rungs | 29.05% | $340,225 | $124,000 | -23.7% | 36% | +5.64% |
| C — market-buy | 30.12% | $342,991 | $124,000 | -23.8% | — | — |

**C − A gap (does rung-waiting cost money?): +0.77pp annualized**
B − A: -0.30pp · B − C: -1.07pp

## Verdict
**NO CHANGE — all arms within the pre-committed noise threshold (1.0pp). Keep it simple; question closed.**

_One 6-year, mostly-rising window = one sample. The threshold exists because a small edge in one sample is noise, not signal._
