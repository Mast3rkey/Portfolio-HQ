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

## What this verdict does and doesn't cover
The MaxDD column above is **aggregate-portfolio-level** -- the same quantity `trim_backtest.md` showed is *not* where concentration risk actually shows up. That test's override of its own raw TWR result (never-trim won by +6.65pp but was rejected anyway) was built on a **single-name** decomposition: RKLB balloon to 12.6% of the sleeve (3.6x its target) with its own -28.6% drawdown vs the portfolio's -24.6%, translated through leverage to ~-46% vs ~-39% on net equity. This test's near-identical aggregate MaxDD across arms (-20.3% vs -20.1%) does **not** by itself show whether an individual T1/T2 name reaches a comparably dangerous concentration under Arm A's no-trim control. Running the same decomposition here:

| Arm | Hottest T1/T2 name | Peak multiple of target | Name's own MaxDD | Est. net-equity DD at 1.44x |
|-----|---------------------|-------------------------:|------------------:|----------------------------------------------:|
| A | NVDA (T1) | 2.14x | -66.4% | -95.6% |
| B | NVDA (T1) | 1.80x | -66.4% | -95.6% |
| C | NVDA (T1) | 1.80x | -66.4% | -95.6% |

NVDA's own -66.4% peak-to-trough (its real 2021-2022 correction) is severe enough that the linear leverage-translation used above and in `trim_backtest.md` (drawdown x leverage multiple) **stops being a valid approximation near this magnitude** -- a >69% levered loss on a name that size implies forced liquidation / a buffer-floor breach well before the full move plays out, not a literal -95.6% mark. The honest reading isn't the number itself, it's that **NVDA at 2.14x its T1 target is large enough that its own historical worst-case, under this account's actual leverage, is wipeout-territory** -- qualitatively different from a diversified portfolio-level -20% MaxDD, and exactly the asymmetry a portfolio-level MaxDD number cannot show.

**This backtest closes the *return* case for a T1/T2 trim rule, not the *capital-impairment* case** -- same distinction the regime-gate entry drew between "cash drag, fully priced by TWR" and "capital impairment, not priced by TWR." If the hottest single-name concentration above is meaningfully worse than the account's own leverage math tolerates, that's a reason to revisit this question even though the aggregate return/MaxDD numbers say no change -- the same way leverage overrode trim_backtest.md's raw result. **The verdict above (no T1/T2 trim rule adopted) still stands for the return question; whether T1's real-world concentration deserves a trim on capital-impairment grounds is a separate judgment this backtest surfaces the numbers for but does not itself settle.**
