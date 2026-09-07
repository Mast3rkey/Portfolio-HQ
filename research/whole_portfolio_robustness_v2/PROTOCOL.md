# Corrected whole-portfolio robustness protocol

Study: `PORTFOLIO-ROBUSTNESS-V2-0001`

Status: **PREREGISTERED — NOT EXECUTED**

## Decision question

Does one of five fixed, economically interpretable alternatives improve the
current accepted portfolio's held-period risk-adjusted performance and tail
survivability after realistic costs and tax sensitivities, without an
unacceptable return sacrifice? The accepted targets remain the baseline. No
result changes policy automatically.

This is a correction replication. The historical period through 2026-07-31
was exposed by `PORTFOLIO-ROBUSTNESS-0001`, whose evidence was classified
`EVIDENCE_LIMITED_NOT_DECISION_GRADE` by RISK-0005. It is therefore not called
a fresh holdout. The replacement study gets a new identity, freezes its
hypotheses before execution, and must reproduce every admitted input from
pinned source bytes and receipts.

## Portfolio and alternatives

The engine must derive the 100% counterfactual directly from `targets.yaml`
and `gates.yaml`; hand-copied weights and renormalization are prohibited. The
99.25% assigned destination plus the 0.75% unassigned residual reconcile to
100%. RESERVE, CASH, the residual, and all six gated targets remain cash.
Gates never open historically. Capital for a not-yet-lawfully-available active
asset remains cash until the first scheduled rebalance after availability.

The six fixed candidates are BASELINE, BROAD_PLUS_5, DEFENSIVE_PLUS_5,
CRYPTO_HALF, GOLD_PLUS_2, and DIVERSIFIED_BALANCE. Their exact sleeve changes
are in `pre_registration.yaml`. There is no parameter search, ranking-based
winner selection, or refit after seeing a result.

## Evidence admission

Eligible stocks, broad funds, and GLD must use the reconciled LADDER-0003
price selection, bad-tick corrections, and corporate-action registry. The
engine must independently verify the referenced hashes and reconstruct the
selected transforms from retained raw bytes and receipts. RTX begins no
earlier than its lawful identity boundary. Dividends are credited once on the
ex-date from the frozen registry; split-adjusted prices are not total-return
prices. The LADDER-0003 foreign-dividend amendment is also pinned: reported
source-net dividends are normalized to gross entitlement, foreign withholding
and available credit are shown separately, and both the zero-credit and ETN
25% Irish-withholding cases are mandatory sensitivities. If either changes an
apparent winner or adoption gate, the disposition is `UNABLE_TO_DETERMINE`.

Crypto is a new fail-closed gate. BTC, ETH, and SOL require a successor input
disposition that pins raw bytes, receipts, transformation rules, daily
completeness, and an evidence-supported availability boundary. Existing
candidate files alone are not admitted. No stitching, interpolation,
forward-fill, assumed inception date, or silent shortening is allowed. If any
required crypto series cannot pass, the whole study disposition is
`UNABLE_TO_DETERMINE`; the engine may not silently move that sleeve to cash or
drop SOL.

The portfolio valuation calendar is XNYS sessions. Each crypto series is built
from consecutive UTC daily closes; every intervening calendar-day return,
including weekends and exchange holidays, is compounded into the next XNYS
portfolio valuation. Discarding weekend returns or using future UTC closes is
prohibited.

Cash earns lagged DFF on an ACT/360 basis less 25 bps annual operating drag.
The XNYS calendar, DFF, targets, gates, look-through, LADDER-0003 disposition,
actions, and corrections are hash-pinned. Any drift halts before results.

## Evaluation

The common evidence interval is 2021-06-01 through 2026-07-31. The
2021-06-01–2023-12-29 interval is non-voting context; the previously exposed
2024-04-02–2026-07-31 interval is the voting correction replication. Fixed
calendar subperiods cover the 2022 rate/inflation drawdown and each later
calendar year. Expanding-origin, no-refit annual evaluations begin in 2022.
Asset-selected peak/trough windows are prohibited.

This is a current-roster historical counterfactual, not a reconstruction of
what would have been recommended at each historical date. Holding unavailable
weights as cash prevents invented predecessor returns, but does not remove
survivorship or hindsight-selection bias; all outputs must carry that limit.

Primary rebalancing is quarterly at the first available XNYS close; annual
rebalancing is a sensitivity. Every variant is evaluated at 0, 10, and 25 bps
one-way costs and under tax-deferred, taxable-mid, and taxable-high profiles.
Tax lots use HIFO with acquisition dates; losses create no modeled tax credit,
wash-sale benefit is prohibited, dividends and realized gains are taxed when
recognized, and ending unrealized gains are not liquidated. Equities and funds
use ordinary short-/long-term capital-gain treatment, crypto uses the same
property-gain holding-period treatment, and GLD uses the registered
collectibles-rate sensitivity.

Required outputs include daily paths, TWR/CAGR, volatility, downside
deviation, Sharpe, Sortino, Calmar, maximum drawdown and recovery, worst
month/quarter/year, 95% daily CVaR, costs, turnover, taxes, direct and
look-through concentration, and fixed-regime results. Paired stationary-block
bootstrap uses a mean 21-session block, 2,000 draws, and seed 20260907.

## Adoption gate

The default is `RETAIN_BASELINE`. A candidate can only earn
`RECOMMEND_POLICY_REVIEW` if it clears every numeric gate in the preregistration
across the voting interval, context direction, fixed regimes, friction/tax and
cadence cells, bootstrap probabilities, data integrity, and concentration.
A close call or mixed result retains baseline. Even a passing result only
recommends a separate reviewed policy decision.

This study is advisory-only. It uses no account state or broker credentials,
does not authorize a trade or leverage, does not change targets or gates, and
keeps Stage 1 UNARMED and NOT EXECUTABLE.
