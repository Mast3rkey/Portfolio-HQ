# Portfolio Measurement Foundation

## Purpose

This layer creates the minimum evidence needed to distinguish investment return,
external contributions, margin financing, and actual borrowing cost. It is
descriptive and advisory-only. It does not alter holdings, targets, gates,
recommendations, margin policy, or execution state.

## Canonical ledgers

| Ledger | Records | Explicitly excludes |
|---|---|---|
| `performance_log.csv` | Timestamped net equity, gross holdings, margin debt, cash, whole-book value, and optional benchmarks | Fabricated values and stale cash/margin observations |
| `cashflow_log.csv` | External deposits and withdrawals with immediately-before/after whole-book valuations | Margin draws, margin paydowns, trades, dividends, and estimated flows |
| `margin_log.csv` | Every manual debt/buffer sync and the inferred debt delta class | A claim that the displayed buffer is independently derivable |
| `interest_log.csv` | Actual broker interest charges and statement periods | Estimated or simulated interest |

All four files are durable evidence. Writers validate finite numeric domains,
use LF line endings, and fail closed on malformed schemas. Cash-flow timestamps
must be strictly increasing. Existing rows are never silently revised.

## Exact TWR requirement

An external flow breaks the return measurement period. Exact TWR therefore needs
the whole-book value immediately before and after each flow:

```text
deposit:    book_after = book_before + amount
withdrawal: book_after = book_before - amount
```

The logger accepts a maximum one-cent reconciliation difference. Each subperiod
return is linked geometrically. If timestamps collide, a valuation is missing,
or a flow fails the identity, exact TWR is unavailable. The system never chooses
an assumed flow timing, Modified Dietz weight, or reconstructed historical value
and labels it exact.

Historical `performance_log.csv` rows lack timestamped whole-book evidence and
remain useful only for the older directional comparison. Exact TWR begins with
the first two complete post-implementation observations.

## Operational commands

```bash
python allocate.py update-margin <debt> <buffer_pct> [note]
python allocate.py log-cashflow <deposit|withdrawal> <amount> \
    <book_before> <book_after> [note]
python allocate.py log-interest <amount> <period_start> <period_end> [note]
python allocate.py --performance
```

The values must come from the account holder's broker evidence. `book_before`
and `book_after` mean the same whole-book identity used by Portfolio-HQ:
invested holdings + cash - margin debt.

## Margin interpretation

`update-margin` compares the new debt with the prior recorded debt:

- higher debt: `draw`
- lower debt: `paydown`
- unchanged debt: `resync`
- no valid prior debt: `initial_sync`

Every row retains the broker-displayed buffer and a source label. This history is
necessary for later shadow margin research, but it does not authorize borrowing.
Stage 1 remains unarmed and no command in this layer places an order.
