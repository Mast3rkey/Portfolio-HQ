# Allocator Operational Characteristics

> **⚠️ Observational documentation only.** This document treats `allocate.py` as a fixed system and describes how it behaves, using its actual code path and today's synchronized portfolio state as evidence. It recommends no rule change, proposes no new feature, implements no validation, and does not compare this allocator against any alternative method or discuss investment performance. Every claim below is traced to a specific line/function in the current codebase or to a specific number from today's run — never to general software-engineering convention or investment opinion.

_Written 2026-07-17. Sources: direct re-read of `allocate.py`'s `plan()`/`build_roster()`/`fetch_market()`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, and the same read-only, unmodified-state trace used for today's allocation explanation (`resolve_holdings()`/`plan()` called directly, no cash/margin requested, no file written)._

---

## Part 1 — Execution pipeline

The complete path, in actual code order, for one `allocate.py` run (`main()` → `plan()`, `allocate.py`):

### Setup (once per run, not per ticker)

1. **Load config** (`build_roster()`) — reads `targets.yaml`'s five tier lists into `{ticker: {tier, weight_pct, fixed, cap_multiple}}`. Report-only; no gating.
2. **Fetch market data** (`fetch_market()`) — pulls daily bars per roster ticker plus the regime ticker (QQQ) from Alpaca; computes `price`/`sma200`/`sma50`/`rsi14`/`atr14` per ticker (`indicators.compute_all()`). Report-only; failures are recorded as an `error` string, not raised.
3. **Fetch crypto prices** (`fetch_crypto()`) and **resolve holdings** (`resolve_holdings()`) — live-values every `shares`/`crypto_shares` position. Report-only.
4. **Compute book** — `net_equity = gross − margin_debt`; `book = net_equity + cash`. Feeds every subsequent target computation. Not itself a gate.

### Per-ticker loop (`plan()`, evaluated once for every roster ticker, in this exact order)

| # | Step | Terminates / Continues / Informational |
|---|---|---|
| 5 | Compute `target_dollars`, `current`, `gap`, `price`, `rsi`, `sma200`, `vs200` | Informational (report-only calculation) |
| 6 | Compute `tk_clusters` (which clusters this ticker belongs to) | Informational at this point (consumed later) |
| 7 | **Band/spec trim check**: if tier is band/spec AND `current > overweight_limit` AND `rsi > trim_rsi` (60) → TRIM, stop | **Terminates** evaluation for this ticker on trigger |
| 8 | **T1/T2 concentration ceiling**: if tier is T1/T2 AND `current > target × 1.5` → TRIM, stop | **Terminates** on trigger |
| 9 | **Minimum-lot filter**: if `gap < $25` → stop (silently, no BLOCKED row) | **Terminates** (silent) on trigger |
| 10 | **Data-availability check**: if no price/error → BLOCKED "no-data", stop | **Terminates** on trigger |
| 11 | **Trend gate**: if `price < sma200` AND (`rsi` is None OR `rsi ≥ 30`) → BLOCKED "downtrend", stop | **Terminates** on trigger; oversold override (RSI<30) lets evaluation continue |
| 12 | **Earnings gate**: if earnings date known and `0 ≤ days_until ≤ 7` → BLOCKED "earnings in Nd", stop | **Terminates** on trigger; if date is *unknown*, sets an `earnings:unavailable` flag but **continues** (does not block) |
| 13 | Compute per-name buy ceiling (`max_by_name`) from tier-specific caps | Informational (a bound consumed later, not itself a stop/continue decision) |
| 14 | Appended to `buy_candidates` | Continues to post-loop stages |

### Post-loop stages (once per run)

| # | Step | Terminates / Continues / Informational |
|---|---|---|
| 15 | **Cluster-cap mechanical trim** — for each cluster over its `pct` cap, trims already-eligible (not-yet-trimmed) member tickers largest-overweight-first, floored at each name's own tier target | Acts (produces TRIM rows) only when a cluster is over cap; otherwise no-op |
| 16 | **Crypto sleeve gap check** — if the sleeve is underweight its target, appended as a buy candidate (no trend/RSI/earnings gate applies to it) | Buy-side only — there is no corresponding trim step for the sleeve anywhere in this pipeline |
| 17 | **Greedy allocation** — buy candidates sorted by dollar gap descending; for each, a **per-cluster room check** (BLOCKED if the ticker's cluster has no room left) and a **cash-exhausted check** (BLOCKED once remaining cash/margin < $25) | Terminates a given ticker's buy on trigger; otherwise allocates and continues to the next candidate |
| 18 | **Margin-state classification** (`classify_margin_state()`, called in `main()` strictly *after* `plan()` returns) | **Informational only** — cannot influence any decision above, since `plan()` has already finished |
| 19 | **Regime status** (QQQ vs. 200-EMA) — computed early (step 2) but never referenced anywhere in `plan()`'s body | **Informational only** — confirmed by direct trace: `regime_ok` is accepted as a `plan()` parameter but never branched on |

---

## Part 2 — Today's run

**Official run:** `python allocate.py --margin 4405.25` (2026-07-17, logged to `logs/allocation-2026-07-17T131520.md`).

- **Number of holdings:** 67 (65 roster tickers with a live position + ETH + SOL; BTC listed in the crypto sleeve but currently at $0).
- **Account value used (book):** $6,237–$6,240 across the run and the explanatory re-trace (minor price drift between calls); net equity = book (no new cash this cycle).
- **Cash recognized:** $0 (the deposit was margin-funded buying power, not cash — confirmed from your screenshot: `Cash: $0.00`).
- **Margin requested / allowed:** $4,405.25 requested → $3,734 allowed (clipped by the 1.8x leverage cap; buffer 62.46% was not the binding constraint).
- **Buy candidates that reached the buy-candidate list:** 0.
- **Trim candidates:** 1 (GILD).
- **Skipped candidates:** 29 tickers had a positive (underweight) gap; all 29 were skipped at the minimum-lot filter (step 9 above) before reaching any further gate.
- **Orphan holdings:** 0 — every held ticker/coin maps to a roster tier or the crypto sleeve.
- **Cluster usage:** semis $1,349.93 = 21.6% of book (cap 25%); power_infra $489.51 = 7.8% (cap 20%); oil $208.37 = 3.3% (cap 20%). None breached.
- **Tier usage (ticker counts):** T1=9, T2=15, ETF=3, band=33, spec=5 (65 total).

### Why exactly one trim occurred

Two mechanical trim rules exist that could fire without an RSI condition (cluster caps, T1/T2 ceiling) and one that requires RSI confirmation (band/spec). Today:
- **0 of 65** T1/T2 names exceeded the 1.5x concentration ceiling (closest: MSFT at ~1.43x).
- **0 of 3** clusters exceeded their cap.
- **22 of 38** band/spec tickers exceeded their dollar cap (1.25x for band, 1.0x for spec) — but of those 22, only **1** (GILD, RSI 60.587) also cleared the `rsi > 60` confirmation. The other 21 remain overweight, untrimmed, pending a future run where RSI crosses the threshold.

### Why zero buys occurred

Every one of the 29 tickers with a positive gap had a gap **below the $25 minimum-lot threshold** — the largest was SKHY at $22.86. This is a single, specific, code-traceable reason (step 9 above, `if gap < min_lot: continue`), evaluated *before* the trend gate, the earnings gate, and the cluster/name buy-ceiling checks — none of those three gates was reached by any ticker today, regardless of what they would have decided.

---

## Part 3 — Gate effectiveness (today's run)

| Gate | Securities that reached it | Filtered by it | Action produced today | Informational only? |
|---|---:|---:|---|---|
| Minimum-lot filter | 65 (every roster ticker with a computed gap) | 29 (all positive-gap tickers; the other 36 had a non-positive gap and were already excluded for that reason, not by this filter specifically — see note below) | Silently excluded 29 tickers from buy candidacy | No — structural gate |
| Trend gate | 0 | 0 | None — never reached | No, but inactive today |
| Earnings gate | 0 | 0 | None — never reached | No, but inactive today |
| T1/T2 ceiling | 24 (all T1+T2 tickers) | 0 | None | No — structural gate, dormant today |
| Band/spec trim gate (dollar-cap leg) | 38 (all band+spec tickers) | 22 exceeded the dollar cap | Passed 22 to the RSI check | No — structural gate |
| Band/spec trim gate (RSI leg) | 22 (only those already over the dollar cap) | 21 held (RSI ≤ 60) | **1 trim (GILD)** | No — structural gate, produced today's only action |
| Cluster caps | 3 clusters (65 member-tickers across them) | 0 clusters over cap | None | No — structural gate, dormant today |
| Regime | n/a (computed once, not per-ticker) | n/a | None — cannot produce an action by design | **Yes — confirmed informational only** |
| Margin | n/a (portfolio-level) | Requested $4,405.25 clipped to $3,734 allowed | Would have constrained buy deployment, but 0 buy candidates existed to deploy into | No — structural gate, but had nothing to act on today |

**Note on the minimum-lot row:** 36 of 65 tickers had a non-positive (zero-or-negative) gap and were never buy candidates for that reason alone — they didn't reach the minimum-lot filter as an underweight test, since a negative gap already fails `gap < min_lot` trivially. The precise count of tickers whose *only* obstacle to buy-candidacy was the $25 threshold (i.e., truly underweight but too small a gap) is the 29 reported above.

---

## Part 4 — Operational characteristics

Each statement below is supported by today's run or by a direct code citation; none is a recommendation.

- **Activity today concentrated entirely into a single trim, zero buys.** This is not unusual given the portfolio's current state (Part 2) — with $4,405.25 in requested buying power and $3,734 allowed, 100% of that capacity went unused, not because it was blocked by a gate, but because no candidate cleared the minimum-lot threshold. Deployment and trimming are structurally independent processes in this pipeline — a trim requires no available cash/margin at all (it raises cash by selling), while a buy requires both an eligible candidate *and* deployable capital.
- **Dependence on deposit size:** the minimum-lot filter (step 9) means a deposit's *size* has no bearing on whether a buy occurs if every gap is already below $25 — a $10,000 margin request today would have produced the same zero buys, since the constraint is the gap size, not the available capital. (Traced directly: `buy_candidates` is populated before `cash_left`/`deployable` is ever consulted.)
- **Interaction between portfolio breadth and the minimum-lot threshold:** with 65 roster tickers spread across a $6,240 book (~$96 average position size), day-to-day price movement routinely keeps most gaps inside a $25 band. The wider the roster relative to book size, the more often this condition is expected to recur, purely as an arithmetic consequence of per-name target sizes shrinking as ticker count grows for a fixed book.
- **Interaction between fixed targets and natural market drift:** `target_dollars` is recomputed fresh every run from `book × weight_pct`, while `current` reflects live prices — so a ticker's gap moves for two independent reasons every run: the ticker's own price change, and the *book's* change (which shifts every other ticker's target simultaneously, even those the account holder didn't touch). Today's ETF-tier positions (SPY, QQQ, GLD) illustrate this: all three are overweight with **no mechanical trim rule available to correct it**, confirmed directly — `plan()`'s tier-branch logic only defines trim behavior for `band`/`spec` (dollar-cap+RSI) and `T1`/`T2` (1.5x ceiling); no equivalent branch exists for `ETF`.
- **Expected periods of inactivity:** given the current roster/book-size ratio and the minimum-lot filter, a run producing zero buys (as today did) is a structurally expected, not anomalous, outcome — it recurs whenever most gaps sit inside the $25 band, independent of market direction.
- **Asymmetry between band/spec and the crypto sleeve:** band/spec overweight is correctable by a mechanical trim (gated on RSI); crypto sleeve overweight (today: +1.18pp) has no corresponding trim mechanism anywhere in `plan()` — confirmed by direct code search: the sleeve only ever appears as a buy candidate (step 16), never as a trim source.
- **RSI-gating creates a large pool of "known but unacted" overweight positions.** Today, 21 of 38 band/spec tickers are over their dollar cap yet untrimmed, purely because RSI hasn't crossed 60 — this is a standing, visible characteristic of the RSI-gated design (trims wait for strength), not a malfunction; the dollar-cap-exceeded state and the RSI-confirmed-trim state are two distinct, separately-observable conditions in every run's output.

---

## Part 5 — Unknowns

Operational questions this document cannot answer from code, documentation, today's run, or repository history:

- **How often, in practice, does a run produce zero buys?** No historical log of gate outcomes across prior runs exists in a queryable form — `logs/*.md` files are gitignored (not retained in version control) and `performance_log.csv` records only net equity/gross/margin snapshots, not gate-level detail. **Unknown.**
- **How many of the 21 currently-untrimmed band/spec overweight positions will eventually cross RSI 60, and when?** This depends on future price action this document cannot predict and does not attempt to. **Unknown** (and out of scope to estimate).
- **Whether today's zero-buy, one-trim pattern is typical or unusual relative to this portfolio's history.** No baseline or distribution of past run outcomes is available in the repository to compare against. **Unknown.**
- **What fraction of past deposit cycles were similarly constrained by the minimum-lot filter versus other gates.** Not recorded anywhere. **Unknown.**
- **Whether the ETF tier's lack of a trim rule is a deliberate design omission or an unaddressed gap.** No document (`CLAUDE.md`, `targets.yaml`, code comments) states a reason for the ETF tier's absence of a cap/trim mechanism, unlike the band/spec/T1/T2 rules, which are each explicitly documented with a rationale. **Unknown** — this document does not speculate on intent.

---

## Part 6 — Executive summary

**What today's allocation teaches about how the allocator behaves:** the pipeline evaluates every ticker through a fixed, ordered sequence of terminating and continuing checks; today's specific outcome (one trim, zero buys) resulted from two independent, fully traceable facts — no T1/T2 or cluster-cap breach existed, and exactly one of 22 dollar-cap-exceeding band/spec positions had also cleared its RSI confirmation, while every underweight position's gap fell below the $25 minimum-lot floor before any further gate was even reached.

**Observed behaviors that are intentional architecture** (each backed by explicit code/doctrine evidence, not inferred): the band/spec RSI-gated trim (waits for strength, `CLAUDE.md`-documented); the T1/T2 and cluster-cap mechanical trims (no RSI gate, documented as risk-limit rather than timing decisions); regime status and margin-state classification being structurally incapable of influencing a decision; the crypto sleeve competing only on the buy side with no timing gates (documented Decisions Log entry).

**Observed behaviors that simply emerge from the current rules, without being independently designed for**: the ETF tier having no trim mechanism at all (a consequence of no branch existing for that tier, not a documented choice); the minimum-lot filter's interaction with a 65-ticker roster producing a systematic tendency toward zero-buy runs on a book this size; the pool of "dollar-cap-exceeded but RSI-unconfirmed" band/spec positions (21 today) as a natural, expected byproduct of pairing two independent conditions (a dollar threshold and a momentum threshold) rather than a single combined one.

---

## What this document deliberately does not do

- Does not recommend changing any gate, threshold, or rule.
- Does not propose a new feature, validation, or backlog item.
- Does not compare this allocator to any alternative allocation method.
- Does not discuss or evaluate investment performance.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, `CLAUDE.md`, or any other production or doctrine file.
- Does not speculate where the evidence is silent — every such case is marked Unknown in Part 5.

Stopping here.
