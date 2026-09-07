# Corrective canonical buy-ladder comparison

Disposition: **RETAIN_BASELINE**

This is advisory research only. It is not a current buy list, order, trade, target change, or automatic policy adoption.

## Voting holdout at 10 bps

| Arm | Annualized TWR | Maximum drawdown |
|---|---:|---:|
| A_ATR | 16.18% | -11.62% |
| B_FIXED | 13.97% | -9.34% |
| C_IMMEDIATE | 21.57% | -17.19% |

## Segment divergence

| Segment | 10 bps TWR leader | Veto-eligible cycles |
|---|---|---:|
| equity | C_IMMEDIATE | 24 |
| broad_funds | C_IMMEDIATE | 3 |
| gold | C_IMMEDIATE | 5 |

## Decision controls

Pairwise winner(s): none.
Apparent 10 bps leader: C_IMMEDIATE.
Eligible segment vetoes: 0.
Tax sensitivities changing a winner or gate: 0.

The historical earnings blackout is omitted identically because the repository has no complete point-in-time calendar.
The voting holdout was exposed by invalid PR #384; that preliminary result is excluded and cannot confirm or veto this corrected result.
Stage 1 remains **UNARMED AND NOT EXECUTABLE**.

