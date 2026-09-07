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

- **H0 / default:** retain A unless B or C clears every adoption gate against both
  other arms in §10.
- **H1:** C clears every gate versus both A and B; recommend simplification.
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

The implementation uses retained, split-adjusted, non-total-return daily OHLC only
after the evidence-disposition prerequisite below selects and reconciles the exact
files. It also consumes the retained corporate-action file for cash dividends and
splits. It must write a manifest with the SHA-256, provider, adjustment, first/last
observation, and row count for every consumed file before computing results.

The raw DFF file is already frozen at SHA-256
`a052a99256ac7fdf075911b03496ab14acbcfd76f428137966bc0fd8781c4849`.
The validated transformed DFF file at
`research/level1_sleeve_robustness/data/transformed/selected/DFF.json` is frozen at
`a4610d02a33fc4e72eff5c54ba8499b7d0f85e5d828dd054e4158f967b530b5b`.
The XNYS session calendar at
`research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json` is frozen at
`365c740ed489a2804189dee439a8cfe4fd926db1f92957988e51ad91db12fabe`.
The retained source inventory is frozen at
`9b604871e9180e9aa7a7ae298a749050a267ea81a7e402e099d9519a1d979f71` and the
corporate-action file at
`a75341f1279665423722074fbc3c89eed2a0c4708e8aefcd658220c3e7bc83b2`.
The implementation must reject any mismatch before validation or execution.

**Execution prerequisite.** The current inventory selects Yahoo files for much of
the earlier robustness study while the first V2 draft named Alpaca candidate files,
and the inventory records unresolved corporate-action reconciliation mismatches for
17 stock/fund series used by that study. The completed whole-portfolio study also
substituted SOL's provider first observation for its registered lawful inception.
These are known evidence conflicts, not benign provider labels. Before either
validation or execution, a distinct accepted evidence-disposition decision must:

1. reconcile every selected OHLC series with splits and cash-dividend actions,
   selecting one exact split-adjusted, non-total-return OHLC file per ladder ticker;
2. explain or quarantine every source-selection and action mismatch rather than
   choosing whichever source improves a result;
3. dispose of the prior SOL lawful-inception gap without rewriting or rerunning the
   once-only whole-portfolio result; and
4. publish the selected paths and hashes that this protocol's implementation binds.

Absence, drift, or an unresolved row in that disposition is fatal. The disposition
may limit evidence or require abstention; it may not inspect a V2 holdout result,
change this protocol's arms, or silently alter accepted targets.

Market data end is fixed at **2026-07-31**. Later rows, if present, are rejected.
Input facts, computed metrics, and recommendation inference must be stored in
separate fields/files. The engine is offline and deterministic at execution; network,
account, credential, holdings, order, and brokerage access are prohibited.

## 4. Windows, availability, and look-ahead controls

- Context/development: **2021-06-01 through 2023-12-29**. Non-voting.
- Voting holdout: **2024-04-02 through 2026-07-31**. This boundary was fixed
  before any V2 result was computed and matches the first retained GEV observation.
- Regime context: calendar 2022. Non-voting and reported separately.

The frozen XNYS file is the sole master trading calendar and defines each month's first
session. Indicators and selection on session `t` may use observations only through
`t`'s close. Orders first become active on the next XNYS session. A ticker is
unavailable until it has at least 210 completed OHLC rows through `t`, inclusive, so
GEV necessarily enters the eligible selector later than the holdout start. Once a
ticker is eligible, a missing required XNYS OHLC row is fatal. The manifest must
disclose each ticker's first eligible decision date. No backfill, proxy history, or
silent full-window exclusion is allowed.

The simulation begins on 2021-06-01 and carries one continuous portfolio state
through 2026-07-31. Window metrics rebase the TWR index at each window start; they do
not restart holdings or cash. Calendar 2022 is a slice of the continuous context path.

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

The selector uses accepted target weights, largest target-gap dollars first with
ticker ascending as the deterministic tie-break, the $25 minimum lot, and the frozen
cluster/effective-issuer/common-driver ceilings. Position values, whole-portfolio
value, and constraint usage are measured at that selection close after the external
contribution. Trend eligibility is evaluated once in the selector: additions below SMA200 are blocked
unless RSI14 is below 30. The result is copied to every arm. For every
cycle, the resulting ticker list and **cash budget** are byte-identical across A, B,
C, and all friction cells. If they are not, execution fails closed.

The allocation is the frozen production greedy rule applied to synthetic state. Set
`remaining` to $2,000; rank eligible positive gaps as above; then for each candidate
set its cash budget to the minimum of its target gap, `remaining`, and every applicable
cluster, effective-issuer, embedded-fund, and common-driver dollar room. Record the
candidate only when that clipped budget is at least $25, update all running position
and exposure values, subtract it from `remaining`, and continue until the list ends or
`remaining < $25`. A blocked or sub-$25 candidate does not stop later candidates.
Unassigned `remaining` stays cash. Fixed fixtures must prove this independent
implementation matches `allocate.py` at the frozen configuration snapshot.

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
- A cash dividend is earned only on shares held at the preceding XNYS close for an
  action whose `ex_date` is the current session. Gross entitlement is
  `eligible_quantity * rate`; it is credited after marking securities at the
  ex-date close and before final close NAV is recorded, so it first earns cash
  interest in the next close-to-close interval. Because the
  retained action rows do not consistently carry payable dates, this ex-date credit
  is an explicit timing approximation and must be disclosed. Every friction cell
  debits tax at the same time using the preregistered taxable-middle approximation:
  80% qualified at 15% and 20% ordinary at 24%, an effective 16.8% rate. Split
  events must reconcile to the chosen split-adjusted OHLC series and must not be
  applied a second time to simulated quantities. Gross dividends, dividend tax, and
  net dividends are retained by ticker, arm, and session. Missing, duplicate,
  nonpositive, or unreconciled dividend/split facts are fatal.
- Cash accrues daily between market closes at the retained DFF rate available with
  a one-federal-business-day publication lag, less 25 bp annual operating drag, with
  no zero floor. Missing dates use only the last rate already available after that
  lag. An observation becomes lawful after 23:59:59 America/New_York on the next U.S.
  Federal Reserve Bank business day and may first be used on the following calendar
  day. With DFF expressed in percent, the after-tax annual rate is
  `(DFF / 100 - 0.0025) * (1 - 0.24)` and the Actual/360 cash factor over `d` calendar
  days is `(1 + after_tax_annual_rate / 360) ** d`. Cash accrual is posted before any
  next-session open fill; positions and remaining cash are then marked at that
  session's close. The $2,000 monthly contribution is posted only after the first
  session's close valuation and therefore cannot fund a same-session fill.
  These settings match the already-preregistered middle taxable assumptions used by
  the whole-portfolio robustness program; they are held identical across arms.
- Tradable prices remain split-adjusted, non-total-return OHLC. Voting returns include
  each arm's own after-tax dividend entitlement under the rule above. A separate
  price-only diagnostic is reported but is non-voting and cannot initiate or confirm
  a recommendation.

## 8. Friction cells

The decision cell is **10 bp one-way transaction cost** on filled notional. Mandatory
sensitivity cells are **0 bp and 25 bp**. Gross security notional plus transaction
cost equals the cash budget and is applied on every fill through §7's identity. No
result from a sensitivity cell may replace the decision cell. Because the study never
sells, capital-gains tax is not applicable. Dividend and cash-interest taxes are
specified in §7.

## 9. Required outputs and metrics

For A/B/C, the whole portfolio and attributed segments, each window, and every
friction cell, report:

- annualized TWR/CAGR, cumulative TWR, maximum drawdown, annualized volatility,
  and Sharpe ratio using the lagged DFF series;
- ending value, cumulative contributions, time-weighted cash percentage, cash drag,
  transaction count, deployed dollars, median deployment days, unfilled dollars,
  and unfilled-capital days;
- gross dividends, dividend tax, net dividends, and the non-voting price-only TWR
  diagnostic;
- maximum single-name weight, maximum target deviation, and counts of cluster,
  effective-issuer, and common-driver clips/blocks;
- paired A/B/C cycle allocations proving selector identity.

External contributions occur after the contribution-session close valuation and earn
no return that session. Voting daily returns and drawdowns include after-tax dividend
entitlements and use a cash-flow-adjusted total-return TWR index, never raw account
value; the first contribution initializes the index at 1.0. Segment
TWR attributes selected cash budgets and their unfilled cash to the selected segment.
Unassigned whole-portfolio cash is reported only at the whole level. A segment with
fewer than 12 attributed cycles is `INSUFFICIENT_EVIDENCE` for a segment veto.
CAGR uses actual calendar days with a 365.2425-day year. Annualized volatility and
Sharpe use 252 trading sessions; maximum drawdown is computed from the TWR index. For
each XNYS interval, the risk-free return is the gross lawfully lagged DFF Actual/360
factor minus one, without the cash operating drag or tax. Sharpe is the arithmetic
mean of `(portfolio TWR return - risk-free return)` divided by its sample standard
deviation, multiplied by `sqrt(252)`; zero variance yields `UNAVAILABLE`.

Time-weighted cash percentage is the arithmetic mean of close cash divided by close
NAV across the applicable XNYS sessions. `Cash drag` is Arm C cumulative TWR minus the
arm's cumulative TWR in the same window and friction cell and may be negative.
Deployed dollars means gross security notional; unfilled dollars means cumulative
cash budgets that expire unfilled. Unfilled-capital days are each unfilled budget
multiplied by calendar days from activation through fill or expiry. Median deployment
days are calendar days from selection close through fill. Maximum target deviation is
the largest absolute percentage-point difference between a position's close weight
and accepted target after any close.

Also retain daily portfolio paths and a deterministic paired stationary-block
bootstrap of holdout daily return differences: 2,000 resamples, mean block length 21
sessions, fixed seed **20260907**. For each ordered pair, use a separate Python
`random.Random` seed obtained from the first eight bytes of
`SHA256("20260907|challenger|baseline")`, interpreted big-endian. For a path of length
`n`, choose the first paired index with `randrange(n)`; at each later draw restart at
`randrange(n)` when `random() < 1/21`, otherwise advance the prior index by one modulo
`n`. Apply the same sampled indices to both arms, compound each sampled daily-return
path, and report the fraction for which the challenger's cumulative TWR exceeds the
baseline's. There is no composite score.

## 10. Voting and adoption gates

Only the after-tax total-return whole-portfolio voting holdout at 10 bp can initiate
a recommendation. For
each ordered challenger-baseline pair, the challenger must:

1. improve annualized TWR over the baseline by **more than 1.00 percentage point**;
2. avoid maximum-drawdown deterioration versus the baseline greater than **1.00
   percentage point**;
3. preserve the direction of both tests at 0 bp and 25 bp; and
4. have at least **90%** paired-bootstrap probability that its holdout TWR
   difference has the claimed sign.

H1, H2, or H3 is supported only when its named arm passes all four gates against both
other arms. This makes the possible winning-arm recommendation unambiguous. The 1 pp
thresholds are inherited evidence-bounded governance selections from V1. The 90%
probability is a conservative governance selection, not a claim of statistical
significance.

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

The implementation must pin the protocol hash, configuration hashes, accepted
evidence-disposition decision and selected-input manifest, Python/runtime identity,
code commit, seed 20260907, and output hashes. Exact reruns must be
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
