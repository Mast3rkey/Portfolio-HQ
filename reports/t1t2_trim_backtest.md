# T1/T2 trim backtest — should core-conviction overweight ever get capped?
_2026-07-15 · window 2021-06-01 -> 2026-07-10 · 63 tickers (T1-spec, no crypto; 24 in T1/T2) · $2,000/mo x 62 deposits_

**Pre-committed rule (fixed before results):** adopt B or C only if it beats A by >1.0pp annualized TWR **and** doesn't widen MaxDD beyond 1.0pp versus A -- a TWR win bought with a materially deeper drawdown doesn't count, per the trim_backtest.md precedent (never-trim won on raw TWR there but was rejected on leverage/forced-selling grounds). Arm D (AI-infra cluster cap) only runs if |C-B| > 1.0pp -- no point testing a third shape if the first two already agree. Weight scheme, band/spec trim rule (1.25x/RSI>60), and the trend gate (200-SMA, RSI<30 override) held at current production values in every arm -- only the T1/T2 trim variant changes. One test, one verdict.

Arm D did not run: |C-B| = 0.00pp (<= 1.0pp threshold).

| Arm | Ann. TWR | Final value | MaxDD | T1/T2 trims | $ trimmed | T1/T2 final % of book |
|-----|---------:|------------:|------:|------------:|----------:|-----------------------:|
| A — current (no T1/T2 trim, control) | 27.64% | $302,437 | -20.3% | 0 | $0 | 65.1% |
| B — mechanical 1.5x, no RSI gate | 27.66% | $302,743 | -20.1% | 14 | $7,768 | 62.8% |
| C — 1.5x, gated off below own 200-SMA (no forced sell into weakness) | 27.66% | $302,743 | -20.1% | 14 | $7,768 | 62.8% |

Gaps vs current (A): B-A: +0.02pp · C-A: +0.02pp
MaxDD vs current (A): B-A: +0.15pp · C-A: +0.15pp

## Verdict
**NO CHANGE — all arms within the pre-committed noise threshold (1.0pp). No T1/T2 trim rule adopted; question closed.**

_One window, one mostly-rising sample with a single real bear stretch (2022). A T1/T2 trim rule's real test is exactly that kind of drawdown -- trimming a core-conviction name mid-selloff is a materially different failure mode than trimming a speculative band/spec name that ran hot, which is why this is a new test and not a rerun of trim_backtest.md. MaxDD reported alongside TWR because that tension is the whole reason this backtest exists._
