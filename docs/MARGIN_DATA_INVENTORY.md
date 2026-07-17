# Margin Data Inventory

_2026-07-17 · Documentation only, no code. Classifies every piece of margin-relevant data this system has, could have, or cannot have — the foundation both research tracks (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`, `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md`) are built on. Every item below was checked directly against the repo (git history, `performance_log.csv`, `holdings.yaml`, `CLAUDE.md`) — nothing here is assumed._

---

## A) Observable historical facts

Real, verifiable, already exists — either committed to git or stated as prose fact in `CLAUDE.md`.

**Margin debt/buffer snapshots** — 9 point-in-time syncs are recoverable from git history on `holdings.yaml` (not a continuous series — each is a manually-triggered sync, usually alongside a trim or a deposit clearing):

| Date | Debt | Buffer % | Triggering event (from commit history) |
|---|---:|---:|---|
| 2026-07-13 | $3,449.50 | 56.08% | Post-$50-withdrawal sync (earliest commit in this repo's history) |
| 2026-07-13 | $3,335.38 | 56.61% | VMC exit + paydown |
| 2026-07-13 | $3,299.38 | 56.75% | NOW trim + paydown |
| 2026-07-14 | $2,898.22 | 59.76% | Deposit clearing |
| 2026-07-14 | $2,679.40 | 61.08% | Trim proceeds paydown |
| 2026-07-15 | $2,671.85 | 61.96% | Robinhood screen resync |
| 2026-07-15 | $1,628.64 | 61.77% | T1/T2 concentration-ceiling trims (9 names, ~$1,044) paid down margin |

**Net equity / gross / QQQ / VOO snapshots** — `performance_log.csv`, 3 rows, 2026-07-13 through 2026-07-15 (a 4th same-day row exists in the file's current state but the dedup logic keeps one row per calendar date, so 3 distinct dates are represented).

**One recorded withdrawal**: $50, 2026-07-13, referenced by commit message and `CLAUDE.md`'s "post-BTC-trim, post-withdrawal" line. No other withdrawal is recorded anywhere.

**One recorded pre-repo fact, prose-only, not data**: `CLAUDE.md`'s Decisions Log states the margin debt was originally "discovered" at "~$4,423" before the 2026-07-13 doctrine revision. This is **not a committed data point** — the earliest commit in this repo's entire git history (`466fbce`) already shows $3,449.50, after the $50 withdrawal and evidently after some further, unrecorded change from ~$4,423. The ~$4,423 figure exists only as a remembered/described number in doctrine text, one level less verifiable than everything else in this table. Treat it as a fact about what was once true, not as a data point usable in any calculation.

**Interest rate term**: "~5% APR, first $1,000 free" — stated in `CLAUDE.md` doctrine as a description of Robinhood's terms for this account, not sourced from a rate history. The "~" is itself an admission this isn't an exact, dated figure.

**Current live state** (as of this document): debt $1,628.64, buffer 61.77%, synced 2026-07-15; net equity ~$5,967 per the most recent `performance_log.csv` row.

## B) Reconstructable estimates

Not directly observed, but derivable from A) plus stated, disclosed assumptions — this is the category `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md` lives in entirely.

- **Hypothetical portfolio return with vs. without a stated margin-draw policy**, simulated forward through real historical price data (`data/backtest/*.json`, 2021-2026) using the current production universe/weights/deposit cadence — not this account's real history, a synthetic account running today's rules through real historical prices, exactly like every other backtest in this repo.
- **Interest cost under a fixed-rate assumption** (5.00% APR, held constant for the simulated window, disclosed as a simplification) applied to a simulated debt trajectory.
- **Stress-tested leverage levels** (e.g. the 1.2x-2.0x sweep proposed for a future phase) — hypothetical, evidence-informed, but never a claim about what this account's real history would have shown at those levels.
- **A rough interpolation of the margin trajectory *between* the 7 observed sync points in Table A** — e.g., "debt was probably somewhere between $3,299 and $2,898 in the days between the 07-13 and 07-14 syncs" is a reasonable estimate bounded by real endpoints, but it is an estimate, not an observation, and this document treats it as Category B even though it's anchored to real Category A data points.

## C) Not reconstructable

No method — not a smarter query, not a different assumption, not more compute — recovers these. Naming them explicitly prevents a future session from quietly attempting to "estimate around" a gap that is actually a hard wall.

- **True historical margin utilization before 2026-07-13.** The debt already existed when discovered; nothing records when it was drawn, in what increments, against what buying power, or at what account value/leverage ratio at the time of each draw.
- **Exact historical interest paid.** No interest-charge ledger exists anywhere in this system — not in `holdings.yaml`, not in `performance_log.csv`, not in any commit message. The "~5% APR" term describes the going-forward rate structure, not a record of dollars actually charged.
- **Exact borrowing timeline.** Beyond the 7 discrete sync points in Table A (which capture debt level, not borrowing *events*), there is no record of individual draw transactions.
- **Actual broker margin calls or buffer changes outside the 7 sync points.** Robinhood's buffer % is manually pulled and pasted in; anything that happened to it between syncs (including any moment it may have dipped near or below the 30% floor without being caught) is invisible to this system. This is a real risk-monitoring gap, not just a data gap — see the logging requirements below.
- **Deposit/withdrawal history beyond the single recorded $50 withdrawal.** Deposits are handled conversationally each cycle ("I deposit money and report buying power") and are not logged as discrete, dated, amount-stamped events anywhere persistent. `performance_log.csv`'s net-equity jumps are the only indirect trace, and that log explicitly disclaims itself as unable to distinguish deposit-driven equity growth from market-driven growth (`render_performance()`'s standing caveat).

---

## Required future data collection plan

What needs to start being recorded *today* so this exact question — "has margin helped, on real evidence" — becomes answerable from real data the next time it's asked, rather than needing another hypothetical-simulation workaround.

1. **A dated, append-only margin event log** (new file, e.g. `margin_log.csv`, parallel in spirit to `performance_log.csv`): one row per margin sync, but capturing *why* — draw vs. paydown, amount, triggering event (deposit clearing / trim proceeds / manual paydown / Robinhood-screen resync), not just the resulting debt/buffer snapshot `holdings.yaml` already keeps. The 7 events in Table A above are a good template for the schema, reconstructed retroactively from commit messages — this plan is about not needing to do that reconstruction again.
2. **A dated, append-only deposit/withdrawal log** (new file, e.g. `cashflow_log.csv`): date, amount, direction (deposit/withdrawal), and whether it was cash or margin-funded buying power (the workflow already asks this distinction verbally every cycle per `CLAUDE.md`'s step 1 — this just persists the answer instead of letting it evaporate after the conversation). This single addition would resolve the single biggest Category C gap (`performance_log.csv`'s own standing caveat that deposits/withdrawals aren't backed out of its return figures) as a side effect, not just help future margin research.
3. **An interest-charge log**, populated whenever Robinhood's statement/screen shows actual interest charged (monthly, typically) — even coarse, infrequent entries here would, over a year or two, produce the first real "exact interest paid" data point this system has ever had.
4. **A buffer-percent time series**, not just the debt/buffer pair captured at sync time — even a manually-updated weekly check (paste the buffer screen on a schedule, not only when something else triggers a sync) would materially close the "actual broker margin calls / buffer changes between syncs" gap, since the biggest risk this system currently can't see is a buffer dip *between* syncs.

None of this requires new code beyond simple CSV-append helpers structurally identical to `log_performance()`'s existing pattern — the gap here is a missing habit/schedule, not a missing capability.

## What logging must be added going forward (summary, engineering-facing)

| New artifact | Schema (minimum) | Populated by |
|---|---|---|
| `margin_log.csv` | date, event_type (draw/paydown/resync), amount, resulting_debt, resulting_buffer_pct, trigger | Extend `update_margin()` to append a row every call, using the delta from the prior synced debt to infer draw vs. paydown automatically — no new user input required beyond what `update-margin` already asks for. |
| `cashflow_log.csv` | date, amount, direction (deposit/withdrawal), funding_type (cash/margin) | New, small CLI addition mirroring `update-margin`'s shape — out of scope for this documentation-only phase, flagged here as the concrete next capability this data gap implies. |
| Interest-charge entries | date, amount_charged, statement_period | Manual entry against Robinhood's monthly statement — no automation possible without a data feed this account doesn't have. |
| Buffer time series | date, buffer_pct | Either a disciplined manual habit (paste the buffer screen weekly regardless of whether anything else changed) or, if ever automatable, whatever surface Robinhood exposes it through — not solvable by this codebase alone today. |

This inventory and collection plan is itself the answer to "what would make Track 1 stronger next time" — every Category C item above has a corresponding row here.
