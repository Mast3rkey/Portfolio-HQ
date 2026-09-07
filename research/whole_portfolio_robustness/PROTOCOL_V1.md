# Current-roster whole-portfolio robustness protocol

## Decision boundary

`PORTFOLIO-ROBUSTNESS-0001` asks whether one of five bounded alternatives
robustly improves the current accepted portfolio after costs, taxes, temporal
splits, regime checks, and block-bootstrap stress. It is a successor to
`RISK-0001`, not another attempt at that study. `RISK-0001` deliberately tested
isolated sleeve representations and excluded the whole portfolio, cash,
reserve, residual capital, and margin. This protocol closes that exact gap.

The accepted targets remain the baseline. Passing the thresholds can only
recommend a separate policy review; it cannot change a target, clear a gate,
authorize margin, or execute a trade. A close call retains the baseline.

## Reconciled baseline

The engine must derive weights from the pinned `targets.yaml` and `gates.yaml`.
It must not rely on a hand-copied list or renormalize the 99.25% assigned target
total. The missing 0.75% is ordinary cash. The six gated targets total 6.75%
and also remain cash. The resulting active-policy counterfactual is:

| Sleeve | Weight |
|---|---:|
| Eligible direct equities | 56.50% |
| SPY / VEA / VWO | 23.00% |
| GLD | 4.00% |
| BTC / ETH / SOL | 4.00% |
| Cash, reserve, unallocated, and gated capital | 12.50% |
| Total | 100.00% |

All six gates stay closed in every variant. The study does not model a future
gate-clearing date because doing so would invent both timing and evidence.

## Hypotheses and variants

The five alternatives were selected for interpretability, not because of any
observed result: move 5 points from eligible single names to broad funds; move
5 points from eligible single names to cash; halve crypto from 4% to 2%; move
2 points from eligible single names to gold; or apply the fixed diversified
combination in the preregistration. Every transfer is pro rata within the
changed source and destination sleeves. There is no weight grid, optimizer,
post-result parameter choice, or synthetic best-of portfolio.

## Historical simulation

The simulation starts each window at $100,000 and uses daily chain-linked TWR
with no external flows or leverage. Quarterly rebalancing is primary; annual
rebalancing is a sensitivity. Equity and ETF paths use split-adjusted prices
plus explicit cash dividends credited once. Crypto is spot only. Cash earns
the already-governed, one-business-day-lagged DFF path less 25 basis points per
year of operating drag.

When a current holding did not yet lawfully exist, its weight remains in cash
until the first scheduled rebalance after inception. That convention avoids
fabricated predecessor history, but it does not eliminate survivorship bias:
the full-history path is a current-roster counterfactual, not evidence that the
portfolio could have been selected at the time. The all-current-assets holdout
therefore carries the most decision weight.

## Evidence partitions

- 2016–2020 is non-voting development context.
- 2021–2023 is confirmation evidence.
- April 2, 2024–July 31, 2026 is the holdout in which every current asset has
  a lawful listing history.
- Annual expanding-origin slices from 2019 onward test temporal stability
  without fitting or changing weights.
- Q4 2018, the 2020 COVID shock, 2022 rate/inflation shock, and 2023–2026
  concentration rally are fixed regime windows. Asset-specific peak/trough
  selection is forbidden.

The execution PR must validate all non-holdout mechanics and freeze its exact
code, config, and inputs before emitting holdout results.

## Frictions and tax sensitivity

Each portfolio is evaluated at 0, 10, and 25 basis points of one-way trading
cost and under quarterly and annual cadence. Tax-deferred, mid-tax, and
conservative high-tax profiles are fixed in the YAML. Taxable paths use HIFO
lots with acquisition dates, debit dividend taxes on the ex-date and realized
gain taxes at rebalances, grant no loss or wash-sale credits, and do not tax
unrealized terminal gains. These are sensitivity models, not a claim about the
user's eventual account type or actual tax liability.

## Metrics and stress

Reporting must cover net TWR/CAGR, volatility, downside deviation,
Sharpe/Sortino/Calmar, maximum drawdown and recovery, worst month/quarter/year,
daily 95% CVaR, turnover, tax and cost drag, and both direct and ETF-lookthrough
concentration. The issuer snapshot is pinned; its point-in-time nature must be
disclosed rather than silently treated as live holdings data.

Paired stationary block bootstrap resamples daily baseline and variant paths
together, with mean block length 21 sessions, 2,000 draws, and seed 20260907.
This preserves serial dependence better than independent-day resampling while
keeping comparisons paired.

## Decision rule

A variant may be recommended for a later policy review only if it passes every
registered gate. In the holdout it may trail baseline net CAGR by no more than
0.50 percentage points per year; must improve both Sharpe and Sortino by at
least 0.05; and must improve either maximum drawdown by at least 2.00 points or
daily 95% CVaR by at least 0.10 point. Direction must confirm in 2021–2023, no
fixed regime's maximum drawdown may worsen by more than 1 point, at least 80%
of eligible tax/cost/cadence cells must agree, bootstrap probabilities must
clear 75%, and all concentration and data-integrity controls must pass.

If no alternative clears all gates, retain the accepted baseline. If evidence
is incomplete, report `UNABLE_TO_DETERMINE`; never turn missingness into a win.

## Safety

This research is network-free at execution, advisory-only, and independent of
holdings, broker credentials, orders, margin, and Stage 1. Stage 1 remains
UNARMED and NOT EXECUTABLE. Charts and fresh account state are intentionally
deferred because neither can change this preregistration.
