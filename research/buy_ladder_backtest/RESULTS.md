# Canonical buy-ladder V2 registered result

## Disposition

**RETAIN_BASELINE.** None of the three preregistered arms passed every adoption
gate against both alternatives. The result does not authorize a production change,
current buy, order, target change, or trade. Stage 1 remains **UNARMED AND NOT
EXECUTABLE**.

## Voting holdout (2024-04-02 through 2026-07-31, 10 bp)

| Arm | Annualized TWR | Cumulative TWR | Max drawdown | Ending value |
|---|---:|---:|---:|---:|
| A — current ATR ladder | 16.18% | 41.76% | -11.62% | $192,678 |
| B — fixed 5/10/15% ladder | 13.97% | 35.58% | -9.34% | $180,813 |
| C — immediate deployment | 21.57% | 57.54% | -17.19% | $224,279 |

Immediate deployment produced the strongest return, but its maximum drawdown was
5.58 percentage points worse than A and 7.85 points worse than B. Both exceed the
preregistered one-point deterioration ceiling, so C fails even though its paired
bootstrap sign probabilities were 93.75% versus A and 95.2% versus B. A exceeded B
on annualized return by 2.20 points, but cannot pass against C. No arm wins both
pairwise comparisons.

The same ordering and failed drawdown gates persisted at 0 and 25 bp. The no-foreign-
tax-credit and ETN no-exemption sensitivities did not change the apparent leader.
Accordingly the foreign-dividend amendment does not force an insufficient-evidence
disposition.

## Interpretation

The test does not support replacing the accepted ATR ladder. It also does not show
that A is universally best: C's higher return came with materially worse downside,
while B's smaller drawdown came with meaningfully lower return. This is the outcome
the preregistered multi-metric gates were designed to distinguish from an in-sample
winner selection.

The repository lacks a complete point-in-time historical earnings calendar, so the
historical earnings blackout was omitted identically from every arm. Results use
synthetic monthly contributions, fractional shares, retained split-adjusted OHLC,
reconciled cash dividends, and the protocol's taxable-middle approximations; they
are research evidence, not a forecast or account-specific recommendation.

Machine-readable inputs, daily paths, cycle allocations, metrics, bootstrap draws,
tax sensitivities, and the fail-closed disposition are retained in `execution/`.
