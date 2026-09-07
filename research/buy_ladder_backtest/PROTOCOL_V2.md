# Canonical Buy-Ladder Comparison — Protocol V2

Status: frozen pre-registration; no results have been inspected under this protocol.

Authority: `LADDER-0002`. This protocol supersedes `PROTOCOL_V1.md` for the one
canonical-roster execution authorized by `LADDER-0001`. V1 remains retained as
historical evidence. Nothing here changes production behavior or authorizes a trade.

## 1. Decision question and hypotheses

The decision question is whether the current three-rung ATR method earns its
complexity, on the current eligible roster, relative to a fixed-percentage ladder and
immediate deployment.

- **A — current ATR method:** levels are `SMA50 - {1, 2, 3} * ATR14`; L3 is
  floored at SMA200. Each rung receives one third of the staged dollars.
  The 25% practicality-cap and 60-session swing-low fields are retained as
  informational diagnostics and do not alter a resting limit's fill eligibility.
- **B — fixed-percentage method:** levels are `SMA50 * {0.95, 0.90, 0.85}`.
  Each rung receives one third of the staged dollars. These percentages are a
  bounded research assumption, not calibrated parameters.
- **C — immediate method:** the full staged amount fills at the next-session open.

There is no parameter search and no fourth arm.

- **H0 / default:** retain A unless a challenger clears every adoption gate in §10.
- **H1:** C clears every gate versus A; recommend simplification.
- **H2:** A clears every gate versus both B and C; report stronger evidence for A.
- **H3:** B clears every gate versus both A and C; recommend B for later, separate
  governance consideration.

Failure to clear the gates is `RETAIN_BASELINE` or `INSUFFICIENT_EVIDENCE`, never
evidence that two methods are statistically equivalent.

## 2. Frozen configuration and roster

The configuration snapshot is the tree merged at
`01204a4b2407e83e2ed8cea1404bbf04764032b7`. The implementation must fail closed
unless these byte hashes match:

| File | SHA-256 |
|---|---|
| `targets.yaml` | `69cda30c3f2f7bff00ef4cd3f8f59cda83ece999145e82646ff0987041da874d` |
| `gates.yaml` | `e9a0bcd98a45f75b77e5f60076be34c4eda890255bb9aa0cf1a14868418f2d86` |
| `issuer_lookthrough.yaml` | `6cf4e417e747d9a1ae9621e57d238c685ab593fb65539d561a5d136c7027b0b9` |

The 25 simulated rows, with accepted target weights in percentage points, are:

`NVDA 6.00, TSM 3.50, ASML 2.25, AVGO 3.00, KLAC 1.00, MSFT 5.50,
GOOGL 4.00, AMZN 5.00, META 2.50, PANW 0.50, LLY 3.50, ISRG 3.50,
TMO 3.00, V 2.00, COST 1.25, CEG 1.50, ETN 2.25, GEV 3.00,
GNRC 1.25, PWR 1.25, RTX 0.75, SPY 15.00, VEA 7.00, VWO 1.00,
GLD 4.00`.

Segments are individual equities (21 rows), broad-market funds (SPY/VEA/VWO),
and gold (GLD). Their accepted weights total 83.50%; the residual 16.50% of the
synthetic whole is non-candidate cash, preserving rather than renormalizing the
accepted weights. SNPS, ICE, SPGI, WM, RKLB, and TSLA are gated and excluded.
BTC, ETH, SOL, CASH, and RESERVE are outside this ladder study. A missing or extra
roster row is fatal; unavailable history is handled only by §4.

## 3. Frozen inputs and facts/inference boundary

The implementation reuses the retained, split-adjusted, non-total-return daily OHLC
files at
`research/level1_sleeve_robustness/data/transformed/candidates/alpaca/<TICKER>.json`
and the retained DFF series at
`research/level1_sleeve_robustness/data/raw/fred/DFF.csv`. It must write a manifest
with the SHA-256, provider, adjustment, first/last observation, and row count for
every consumed file before computing results.

The DFF file is already frozen at SHA-256
`a052a99256ac7fdf075911b03496ab14acbcfd76f428137966bc0fd8781c4849`.
The implementation must reject any mismatch before validation or execution.

Market data end is fixed at **2026-07-31**. Later rows, if present, are rejected.
Input facts, computed metrics, and recommendation inference must be stored in
separate fields/files. The engine is offline and deterministic at execution; network,
account, credential, holdings, order, and brokerage access are prohibited.

## 4. Windows, availability, and look-ahead controls

- Context/development: **2021-06-01 through 2023-12-29**. Non-voting.
- Voting holdout: **2024-04-02 through 2026-07-31**. This boundary was fixed
  before any V2 result was computed and matches the first retained GEV observation.
- Regime context: calendar 2022. Non-voting and reported separately.

Indicators and selection on session `t` may use observations only through `t`'s
close. Orders first become active on the next trading session. A ticker is unavailable
until it has 210 prior observations, so GEV necessarily enters the eligible selector
later than the holdout start. The manifest must disclose each ticker's first eligible
decision date. No backfill, proxy history, or silent full-window exclusion is allowed.

## 5. Shared selector: timing is the only arm difference

One whole portfolio is simulated; segment results are attributed from that portfolio,
not created by renormalizing targets. On the first trading session of each calendar
month, a shared shadow allocator receives $2,000. The first contribution initializes
the portfolio from zero. Target gaps are each frozen target percentage multiplied by
post-flow whole-portfolio value, less current position value. The residual 16.50% and
any amount not admitted by positive gaps or constraints remain cash.

The selector runs after that session's close and uses only the shadow portfolio,
never an arm's holdings. The shadow portfolio fills every selected allocation at the
next-session open with zero transaction friction, so it is a deterministic reference
portfolio rather than a fourth reported arm. Its selector decisions therefore remain
identical across all friction cells as well as all reported arms.

The selector uses accepted target weights, largest target-gap dollars first, the $25
minimum lot, and the frozen cluster/effective-issuer/common-driver ceilings. Trend
eligibility is evaluated once in the selector: additions below SMA200 are blocked
unless RSI14 is below 30. The result is copied to every arm. For every
cycle, the resulting ticker list and **cash budget** are byte-identical across A, B,
C, and all friction cells. If they are not, execution fails closed.

Only the new $2,000 contribution is staged each cycle. Cash left by earlier expired
orders stays cash and is not rerouted. This corrects V1's ambiguous arm-dependent gap
ranking, which could have changed both ticker selection and timing at once.

## 6. Earnings-data limitation

The repository does not retain a complete point-in-time historical earnings calendar;
its current earnings adapter exposes current/next events only. The historical earnings
blackout therefore cannot be reconstructed honestly. It is omitted identically from
all arms and the shadow selector, and this limitation must appear in the report.
Current production earnings controls remain unchanged. Fabricated dates, present-day
dates applied retrospectively, or provider history acquired after seeing results are
prohibited.

## 7. Order, fill, expiry, and cash rules

- A/B levels are computed at the monthly selection close and remain fixed for that
  cycle. They are active from the next session through the session before the next
  monthly selection.
- A/B fills use daily OHLC: if `low <= limit`, fill at `min(open, limit)`; otherwise
  the rung remains unfilled. A rung fills at most once. Unfilled rungs expire at cycle
  end and their dollars remain cash.
- C converts each selected cash budget into notional at the next-session open using
  the same cost identity below.
- Each selected cash budget includes friction. At cost rate `c`, filled security
  notional is `cash_budget / (1 + c)` and transaction cost is `notional * c`; the two
  consume the budget exactly. A/B apply this calculation separately to each equal
  one-third rung budget. No cell may create negative cash to pay costs.
- Fractional shares are allowed. No sale, trim, borrowing, shorting, or forced
  liquidation exists in this study.
- Cash accrues daily between market closes at the retained DFF rate available with
  a one-federal-business-day publication lag, less 25 bp annual operating drag, with
  no zero floor. Missing dates use only the last rate already available after that
  lag. Cash interest is reduced by a fixed 24% ordinary-income tax rate.
  These settings match the already-preregistered middle taxable assumptions used by
  the whole-portfolio robustness program; they are held identical across arms.
- Price returns exclude dividends. This biases the absolute return level and is
  reported prominently; arm comparisons remain paired on identical price files.

## 8. Friction cells

The decision cell is **10 bp one-way transaction cost** on filled notional. Mandatory
sensitivity cells are **0 bp and 25 bp**. Costs reduce cash in addition to gross
notional and are applied on every fill through §7's cash-budget identity. No result from a sensitivity cell may replace
the decision cell. Because the study never sells and excludes dividends, capital-gains
and dividend taxes are not applicable; cash-interest tax is specified in §7.

## 9. Required outputs and metrics

For A/B/C, the whole portfolio and attributed segments, each window, and every
friction cell, report:

- annualized TWR/CAGR, cumulative TWR, maximum drawdown, annualized volatility,
  and Sharpe ratio using the lagged DFF series;
- ending value, cumulative contributions, time-weighted cash percentage, cash drag,
  transaction count, deployed dollars, median deployment days, unfilled dollars,
  and unfilled-capital days;
- maximum single-name weight, maximum target deviation, and counts of cluster,
  effective-issuer, and common-driver clips/blocks;
- paired A/B/C cycle allocations proving selector identity.

External contributions occur after the contribution-session close valuation and earn
no return that session. Daily returns and drawdowns use a cash-flow-adjusted TWR index,
never raw account value; the first contribution initializes the index at 1.0. Segment
TWR attributes selected cash budgets and their unfilled cash to the selected segment.
Unassigned whole-portfolio cash is reported only at the whole level. A segment with
fewer than 12 attributed cycles is `INSUFFICIENT_EVIDENCE` for a segment veto.

Also retain daily portfolio paths and a deterministic paired stationary-block
bootstrap of holdout daily return differences: 2,000 resamples, mean block length 21
sessions, fixed seed recorded in the implementation configuration. Report the
probability that each challenger's TWR difference has the claimed sign. There is no
composite score.

## 10. Voting and adoption gates

Only the whole-portfolio voting holdout at 10 bp can initiate a recommendation. A
challenger must:

1. improve annualized TWR over A by **more than 1.00 percentage point**;
2. avoid maximum-drawdown deterioration versus A greater than **1.00 percentage
   point**;
3. preserve the direction of both tests at 0 bp and 25 bp; and
4. have at least **90%** paired-bootstrap probability that its holdout TWR
   difference has the claimed sign.

H2 uses the same gates with A as challenger against both B and C. The 1 pp thresholds
are inherited evidence-bounded governance selections from V1. The 90% probability is
a conservative governance selection, not a claim of statistical significance.

If segments diverge, the report must say so. A sufficiently supported segment vetoes
a whole-portfolio change if the challenger worsens its annualized TWR or MaxDD by more
than 1.00 pp. A segment is not required to show an independently positive 1 pp win;
that would make the single-name GLD diagnostic decide a whole-roster method. Missing required output,
hash drift, non-finite values, selector mismatch, insufficient observations, or a
failed invariant yields `INVALID` or `INSUFFICIENT_EVIDENCE`, never adoption.

## 11. Reproducibility and authorized deliverables

The execution PR may add only deterministic code, configuration, manifest, immutable
results, a plain-language report, and focused tests under
`research/buy_ladder_backtest/`, plus one root-level focused test file if required by
the repository's test layout. The engine must support a validation-only mode that
checks all inputs and invariants without revealing holdout results, followed by one
registered execution that emits the complete outputs atomically.

The implementation must pin the protocol hash, configuration hashes, input manifest,
Python/runtime identity, code commit, seed, and output hashes. Exact reruns must be
byte-identical except for an explicitly separated execution timestamp. Independent
review must recompute manifests, selector identity, metrics, gates, and narrative from
retained artifacts.

## 12. Prohibited effects and closure

No result automatically modifies `levels.py`, `allocate.py`, `targets.yaml`,
`gates.yaml`, `holdings.yaml`, `issuer_lookthrough.yaml`, margin policy, dashboard
behavior, chart scope, or Stage 1. No result is a current buy list, order, price target,
or promise of return. Gated/speculative/crypto holdings remain ineligible for this
study. Stage 1 remains **UNARMED AND NOT EXECUTABLE**.

After one valid registered run, the study closes. Any rerun, parameter change, later
data end, new arm, or production adoption requires a separate reviewed decision.
