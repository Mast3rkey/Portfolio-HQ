# Portfolio HQ — manual-allocation advisor

A **recommendation-only** portfolio allocation and risk-management tool. It
reads your holdings and target tiers, pulls read-only market data from
Alpaca, applies your gates/caps/doctrine, and prints a BUY / TRIM / BLOCKED
table plus a risk summary (margin, concentration, crypto sleeve). **It never
places, modifies, or cancels an order — anywhere.** You execute manually on
Robinhood, then sync the fill back in.

> Safety by construction: `alpaca_client.py` has had all order-placement
> methods **removed**. The project contains no order code. Do not re-add it.

The full reasoning behind every rule below — why each cap exists, what was
tested and rejected, what's a doctrine decision vs. a backtest verdict — lives
in `CLAUDE.md`. That file is the source of truth for *why*; this README is
the source of truth for *how*.

## Repository structure

```
allocate.py        entry point: CLI, allocation/trim logic, rendering, state I/O
levels.py           secondary entry point (--levels): buy-rung staging report
alpaca_client.py    read-only Alpaca paper-account HTTP client
indicators.py        SMA/RSI/ATR/swing-low (pure functions)
earnings.py          yfinance earnings-date lookup, graceful "unavailable" fallback
crypto.py            crypto sleeve pricing (Alpaca majors + CoinGecko fallback)
regime_gate.py        200-day EMA regime check (informational only, see below)
margin_state.py        leverage-cap/buffer-floor math, concentration risk scoring (imported by allocate.py)

targets.yaml          tier structure, weights, caps, gates, margin doctrine (config truth)
holdings.yaml          position state: shares, crypto_shares, margin (rewritten by update-* commands)
CLAUDE.md               doctrine: Decisions Log, Open Items, Guardrails, workflow
decision_log.yaml       historical decision record, PI-000N / MARGIN-000N series (pre-dates the
                        governance/decisions/ layer below; new decisions are not appended here)
constitution/INVESTMENT_CONSTITUTION.md   immutable investment philosophy (rarely amended)
governance/decisions/   structured decision records (ADR-style), one file per decision;
                        every new decision since GOV-0001 (2026-07-18) is filed here

intelligence/companies/     Company Intelligence: per-company research records (implemented, opt-in, advisory-only)
intelligence/themes/        Theme Intelligence: theme-level research records (implemented, opt-in, advisory-only)
intelligence_validator.py   read-only schema validator for intelligence/ (zero coupling with allocate.py/margin_state.py)

backtest_*.py          one-shot backtests, each testing exactly one doctrine question
verify_rungs.py         verification charts for the rung backtest
reports/                backtest verdicts (reports/*.md) + verification charts
data/backtest/           cached daily bars the backtest scripts read (not live data)

test_*.py                unit tests (margin math, cluster/T1T2 trims, live pricing, indicators)
performance_log.csv       daily net-equity-vs-QQQ/VOO snapshot, one row per day
logs/                    per-run Markdown output (gitignored — see "Performance logging" below)
```

## Advisory-only philosophy

This tool computes what a disciplined allocator *would* do — it never acts.
Every gate, cap, and trim rule is mechanical and explainable: given the same
holdings and market data, it always produces the same recommendation, and
every number in the output traces back to a rule you can point to in
`targets.yaml` or `CLAUDE.md`. There is no discretionary judgment, no price
targets, no predictive research baked into the tool itself — see `CLAUDE.md`'s
Guardrails for what's explicitly out of scope and why (several backtests this
system ran on itself showed that added "smart" layers subtract return, not
add it).

## Company & Theme Intelligence (advisory-only)

`intelligence/companies/` holds human-authored, per-company research records
(thesis, risks, catalysts, a conviction rating) — one YAML + one Markdown
file per covered company, validated by `intelligence_validator.py` against
the schema frozen in `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`. Coverage is
opt-in; a company with no file is not an error. The current set of covered
companies is whatever files exist under `intelligence/companies/` — this
README does not restate it as a fixed roster. (As of this writing: COST,
GEV, ISRG, NVDA, TMO, XOM — a snapshot, not a ceiling or a target.)

`intelligence/themes/` holds theme records — shared narrative, evidence,
risks, catalysts, and a closed `lifecycle` vocabulary (no conviction rating,
no numeric score) — one YAML + one Markdown file per theme, frozen by
`decision_log.yaml` PI-0006 and reconciled into the specification by
`governance/decisions/PI-0010-theme-intelligence-spec-reconciliation.md`. A
company references zero or more themes via its own `themes:` field;
authority runs one way only, company → theme (a theme file never lists its
member companies). The current set of themes is whatever files exist under
`intelligence/themes/`. (As of this writing: `ai_infrastructure`, referenced
by GEV and NVDA; `life_sciences_tools_medtech`, referenced by ISRG and TMO —
again a snapshot, not a ceiling.)

**Company and Theme Intelligence have zero authority over allocator
recommendations, targets, tiers, or weights.** `intelligence_validator.py`
has no import relationship with `allocate.py` or `margin_state.py` in
either direction — verified by dedicated isolation tests, not just asserted
in doctrine. Nothing in this repository reads a company's or theme's
thesis, risks, evidence, or conviction/lifecycle value to decide what to
buy, trim, or block.

**Portfolio Intelligence aggregation** — and any theme-level scoring,
ranking, weighting, or allocator-visible integration — remains deferred and
unauthorized. Neither Theme Intelligence nor Portfolio Intelligence
aggregation currently affects allocator behavior.

## Allocation workflow

1. **Deposit or margin draw.** Report the amount and whether it's cash or
   margin-funded buying power (they're gated differently).
2. **Run the allocator:**
   ```bash
   python allocate.py --cash 2000      # deploy new cash → ranked buys
   python allocate.py --margin 1000    # margin-funded buying power (clipped to
                                        # the leverage cap, blocked below the
                                        # buffer floor)
   python allocate.py --review         # rebalance check, no new cash —
                                        # underweights + trim candidates
   python allocate.py --levels         # buy-rung staging report (see below)
   ```
3. **Execute manually on Robinhood.**
4. **Sync fills back** (see "Updating holdings" below).

### How a run computes recommendations

1. Book = live-priced holdings (net equity) + any new cash this cycle.
   Per-ticker target dollars come from that name's tier weight × book.
2. Pull last price, 200-SMA, 50-SMA, RSI(14), ATR(14) per roster ticker via
   Alpaca (free IEX feed); QQQ daily bars for the regime signal.
3. Rank underweight names by dollar gap, then gate in order:
   - **trend** — skip an add on a name below its 200-SMA, unless RSI(14) < 30
     (oversold override).
   - **earnings** — skip an add within 7 calendar days of the next earnings
     date (flagged `earnings:unavailable` if the date can't be resolved).
   - **caps** — correlated-cluster caps (semis ≤25% of book, power_infra
     ≤20%, oil ≤20% — see `targets.yaml`'s `caps.clusters`), band ≤1.25×
     target, spec fixed at target.
4. Greedy-allocate cash to the largest passing gaps, $25 minimum lot.
5. **Trims** (mechanical, no market-timing discretion once triggered):
   - band/spec positions above their cap, opportunistically, only when
     RSI(14) > 60 (trim into strength).
   - a cluster-cap breach, or a **T1/T2 name above 1.5× its own target**
     (the "concentration ceiling") — both mechanical, no RSI gate, floored
     at the name's own tier target.

**Regime status (QQQ vs. its 200-day EMA) is computed and shown every run,
but is informational only — it never blocks or gates a decision.** A 2026
backtest (`reports/regime_backtest.md`) found gating deployment on it cost
2.56pp/yr; the gate was removed from production. `--levels`' stance
computation follows the same rule.

### `--levels` — buy-rung staging

A separate, simpler report: for each roster ticker and the crypto sleeve,
computes three ATR-anchored buy levels below the 50-SMA (L1 shallow → L3 deep,
floored at the 200-SMA) as staging points for manual limit orders. Stamps a
one-word stance (`BUYABLE` / `WAIT` / `BLOCKED` / `NO-DATA`) per name. Same
regime-is-informational-only rule as the main allocator. This tool places no
orders here either — it's staging guidance, not execution.

## Updating holdings

State lives in `holdings.yaml`, in three tracked blocks plus a margin block:

```bash
python allocate.py update-shares          # paste "TICKER qty" lines, Ctrl-D
                                           # (stocks/ETFs — live-priced every
                                           # run via qty × latest Alpaca price)
python allocate.py update-crypto-shares   # paste "COIN qty" lines, Ctrl-D
                                           # (BTC/ETH/SOL — same live-pricing)
python allocate.py update-holdings        # paste "TICKER value" lines, Ctrl-D
                                           # (manual $ fallback — only needed
                                           # for a ticker with no live-price
                                           # coverage, e.g. a very recent listing)
python allocate.py update-margin <debt> <buffer_pct>   # sync from Robinhood's
                                           # own displayed margin screen
```

`update-shares`/`update-crypto-shares`/`update-holdings` **merge** into the
existing state by default — a ticker not mentioned in your paste is left
untouched. Pass `--replace` to instead treat the paste as the complete new
state. **Only `update-holdings` has a safety check** — it aborts and asks for
`--confirm` if the resulting book value would move more than 30% (usually a
sign of a partial-paste wipe rather than an intentional change).
`update-shares --replace` / `update-crypto-shares --replace` have no such
guard — a partial paste there really does wipe every unmentioned position, no
confirmation asked. Use `--replace` on those two with care.

**Margin sync is manual and must use Robinhood's own displayed buffer %** —
`allocate.py`'s own comment in `write_state()` explains why a naive
`(value − maintenance) / value` calculation doesn't reconcile with Robinhood's
real figure (checked twice against live screens). Never derive it.

Every `update-*` command automatically writes a same-day snapshot to
`performance_log.csv` (see below), so state and performance history stay in
sync without a separate step.

## Margin synchronization

Doctrine (from `CLAUDE.md`, enforced in `targets.yaml`'s `margin:` block and
`allocate.py`'s `margin_capacity()`):
- **1.8x fixed structural leverage cap** on gross-position-value / net-equity.
  No discretionary lever-up on a market view — margin is fuel within a fixed
  ceiling, not a timing tool.
- **30% margin-buffer floor**, hard cutoff. Before any margin-funded buy, the
  tool checks the *projected* post-trade buffer; if it would drop below 30%,
  the buy is blocked outright (no partial taper). A buffer already below 30%
  is treated as a forced de-lever signal.
- Buffer % is **synced from Robinhood, never derived** (see above). Every run
  shows the buffer's sync date and warns if it's gone stale
  (`STALE_MARGIN_DAYS`, currently 2 days).

## Performance logging

```bash
python allocate.py --performance        # show the net-equity-vs-QQQ/VOO log
python allocate.py log-performance [note]   # add a snapshot manually (rarely
                                             # needed — every update-* command
                                             # and every allocate.py run already
                                             # auto-snapshots)
```

`performance_log.csv` is a rough directional check, not a precise return
calculation — deposits, withdrawals, and margin draws/paydowns all move net
equity without being backed out, so a big deposit will show up looking like
"growth." Treat divergence from QQQ/VOO as a prompt to look closer, not a
verdict. (A true TWR-based tracker that correctly separates cash-flow effects
from market return is a known gap — see `docs/PORTFOLIO_HQ_AUDIT.md`.)

## Backtesting framework

Six one-shot scripts (`backtest_regime.py`, `backtest_trend.py`,
`backtest_trims.py`, `backtest_weights.py`, `backtest_rungs.py`,
`backtest_t1t2_trim.py`), each testing exactly one doctrine question against
cached historical bars in `data/backtest/` (not live data — this is a
separate flow from the live allocator and never touches `holdings.yaml`).
Every backtest follows the same discipline:

- **Pre-committed decision rule**, fixed *before* results are computed —
  usually "adopt the alternative only if it beats current by more than
  1.0 percentage point annualized TWR."
- **One test, one verdict.** No variant mining, no re-running with tweaked
  parameters after seeing a result.
- **Verdicts are never auto-applied.** A backtest's output is a report
  (`reports/*_backtest.md`); adopting its finding into production always
  means a human reads the report, hand-edits `targets.yaml`, and writes a
  `CLAUDE.md` Decisions Log entry explaining why. This extra step has already
  caught real drift once (a rule shipped slightly different from what was
  tested) — see the Decisions Log's T1/T2 concentration-ceiling entry.
- **Closed questions stay closed.** Every verdict in `CLAUDE.md`'s Decisions
  Log is marked "no re-runs without a new regime in the data" — a small edge
  in one backtested window is noise, not a standing invitation to keep
  testing until a result you like shows up.

Shared math (`twr_annualized`, `max_drawdown`, `rsi_series`, `universe`,
`load_bars`) lives in `backtest_regime.py` and is imported by the others
where the logic is genuinely identical — a couple of scripts keep their own
version of a same-named function where the behavior is deliberately
different (e.g. `backtest_rungs.py`'s `load_bars` can fetch+cache live from
Alpaca on a miss; the shared version only reads an existing cache).

`verify_rungs.py` isn't a backtest itself — it replays `backtest_rungs.py`'s
exact mechanics and renders `reports/verification/*.png` + `*_table.md` so
that backtest's results can be eyeballed against reality.

## Tests

```bash
python3 -m pytest -q
```
Covers the financially consequential code paths — margin math (leverage cap
clipping, buffer-floor hard cutoff), cluster-cap and T1/T2 concentration-
ceiling trims (multi-cluster membership, floor-at-target behavior),
live-holdings price resolution, and the indicator functions (including a
couple of non-obvious verified edge cases, e.g. RSI of a perfectly flat
series is 100.0, not the textbook-intuitive 50) — plus the backtest
libraries, buy-level staging, and Company Intelligence's schema validator
and allocator-isolation guarantees. Run the whole suite rather than naming
individual files here; the file list changes too often to keep in sync.

## Known limitation

Live bars use the **IEX free feed** → volume figures are IEX-only and
under-represent true market volume. The advisor relies entirely on
**price-based** indicators (SMA/RSI/ATR), so this does not affect any gate
or trim decision — nothing in this system reads volume.
