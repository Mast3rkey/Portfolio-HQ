# Corrected whole-portfolio robustness protocol

Study: `PORTFOLIO-ROBUSTNESS-V2-0001`
Status: **PREREGISTERED — NOT EXECUTED**
Correction: **pre-execution contract correction after merged PR #387; no result was inspected and the study identity is preserved.**

## Authority and decision question

This immutable contract asks whether one of five fixed, economically interpretable alternatives improves the current accepted portfolio's held-period risk-adjusted performance and tail survivability after costs and tax sensitivities, without unacceptable return sacrifice. The accepted targets remain the baseline; a passing result can only recommend a separate policy review. It cannot change targets or policy.

The interval is an exposed correction replication, not a fresh holdout. `PORTFOLIO-ROBUSTNESS-0001` was classified `EVIDENCE_LIMITED_NOT_DECISION_GRADE` by RISK-0005. V2 remains unexecuted. This correction resolves the post-merge independent review of PR #387 before any V2 implementation or result.

`pre_registration.yaml` is the executable specification. Its canonical digest covers every parsed key and value except the digest value itself. The validator carries an independently reviewable expected digest, requires the digest machinery and the complete fixed pin registry, and separately pins this protocol. Thus a coherent edit cannot bless itself by editing its own expected digest. Semantic checks provide diagnostics in addition to that full freeze. Any mismatch, malformed YAML, duplicate registry identity, unknown registry member, or non-finite numeric value halts before results under normal and optimized Python.

## Fixed portfolio and alternatives

The engine derives the counterfactual from the pinned `targets.yaml` and `gates.yaml`, without renormalization: 99.25% assigned plus 0.75% residual equals 100%. RESERVE, CASH, residual, and all six gated targets are cash. Gates never open historically. An unavailable active weight stays cash until the first scheduled rebalance after lawful availability.

The only constructions are `BASELINE`, `BROAD_PLUS_5`, `DEFENSIVE_PLUS_5`, `CRYPTO_HALF`, `GOLD_PLUS_2`, and `DIVERSIFIED_BALANCE`, with exact transforms and expected sleeves in YAML. No parameter search, outcome-conditioned selection, ranking, or refit is permitted.

## Evidence and portfolio ledger

Equities, funds, and GLD reuse the pinned LADDER-0003 disposition, corrections, action registry, `PROTOCOL_V2` economics, and foreign-dividend amendment. Split-adjusted price series must not contain distributions. Crypto requires a successor disposition for BTC, ETH, and SOL; absent or incomplete evidence makes the study `UNABLE_TO_DETERMINE`, never a silent drop or cash substitution. The valuation calendar is XNYS sessions, with every intervening UTC crypto daily-close return compounded into the next XNYS value without future data.

### Dividend recognition and settlement

All units are split-normalized. Entitlement equals prior-XNYS-close split-normalized shares times the declared gross dividend. On the ex-date, record exactly once in NAV an **unsettled net receivable**: gross entitlement minus source withholding minus tentative U.S. tax after the allowed same-dividend foreign-tax credit. This is recognition, not spendable cash. On the actual payable date, move that receivable to settled cash with no NAV change and no second tax. Before settlement it cannot fund a rebalance and earns no interest. If still unpaid at evaluation end, it remains in final NAV.

Missing or invalid required amount, split factor, ex-date, or actual payable date halts before results. For one prior-close share, a price moving from 100 to 98 on ex-date with a gross dividend of 2 and the tax-deferred profile produces ex-date NAV 100 and spendable cash 0; on the later payable date cash becomes 2 before other events.

For a common XNYS date, ordering is: begin with prior-close shares and prior settled cash; accrue through the preceding calendar day, once per elapsed calendar day and only on settled cash present at the start of that accrual day; recognize ex-date entitlement/tax into receivables; settle items whose actual payable date is today; value at close; then perform a scheduled close rebalance using settled cash only. A same-day dividend settlement therefore earns no interest for an earlier day. Entitlement therefore always uses prior-close shares and cannot be manufactured by a same-close purchase.

### Cash accrual

Cash return is a research assumption, not personal tax advice, and needs no account input. For every elapsed calendar day, including weekends and holidays, settled cash compounds once using the latest DFF observation lawfully available at that calendar day's start after a one-Federal-Reserve-business-day lag. There is no forward lookup. The annual rate is `(DFF − 0.25 percentage points) × (1 − ordinary_income_rate for the cell's tax profile)`, accrued ACT/360. Unsettled dividend receivables earn nothing. Missing required DFF fails the affected cell and therefore the study closed. The exact formula and event order are frozen in YAML.

## Evaluation cells and primary path

The authoritative primary gate and bootstrap path is **10 bps one-way cost / TAXABLE_MID / quarterly first-available-XNYS-close rebalance**. Sensitivities cannot replace it after outcomes.

The support registry is the exact Cartesian product of costs `{0,10,25}` bps, profiles `{TAX_DEFERRED,TAXABLE_MID,TAXABLE_HIGH}`, and cadences `{QUARTERLY,ANNUAL}`: exactly 18 uniquely identified cells, including the primary. Every alternative is paired with baseline in the same cell and window. Missing, extra, duplicate, malformed, or non-finite cell data fails the study closed.

A cell supports an alternative only when **all** of these signed predicates hold: net-CAGR delta ≥ −0.50 percentage points/year; Sharpe delta ≥ +0.05; Sortino delta ≥ +0.05; and either maximum-drawdown improvement ≥ +2.00 percentage points or daily-CVaR-95 improvement ≥ +0.10 percentage points. Maximum drawdown and CVaR are non-positive returns (zero best, more negative worse); each improvement is `alternative − baseline`, so positive is better. At least 15 of the exact 18 cells must support: the integer rule is `count >= ceil(0.80 × 18) = 15`.

The support count does not replace any main magnitude, context-direction, fixed-regime, bootstrap, integrity, or concentration gate. The primary cell must independently pass the complete main gate and supplies the registered paired stationary-block bootstrap (21-session mean block, 2,000 draws, seed 20260907). Sensitivities are robustness evidence only.

Foreign-dividend cases have a separate veto. Run standard available credit, zero credit alone, ETN 25% Irish withholding alone, and their joint case over all 18 cells. Each separate case and the joint case must preserve the winner and every gate result; otherwise disposition is `UNABLE_TO_DETERMINE`. This preserves both mandatory vetoes and fixes the inventory before results.

## Remaining gates and safety

The exposed voting correction interval is 2024-04-02–2026-07-31; 2021-06-01–2023-12-29 is non-voting context. Fixed calendar regimes, expanding-origin no-refit evaluations, all original numeric return/tail/bootstrap/concentration thresholds, no-loss-credit treatment, HIFO lots, and data-integrity gates remain mandatory. Asset-selected windows are prohibited. A close call or mixed result retains baseline.

The study is advisory-only. It uses no holdings, account state, broker credentials, leverage, order path, or production mutation; changes no targets, gates, allocator, margin doctrine, or Stage 1 state. Stage 1 remains **UNARMED AND NOT EXECUTABLE**. No historical portfolio or ladder outcome may be run under this correction.
