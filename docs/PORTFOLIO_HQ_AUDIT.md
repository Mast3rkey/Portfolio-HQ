# Portfolio HQ — Repository Audit

_2026-07-15 · No code changed as part of this audit. Read-only review of the repository as it exists on `claude/earnings-gate-aapl-nvda-q0tjut` at commit `5550617`._

---

## 1. Repository architecture map

Files grouped by actual role (not by directory — everything lives flat at repo root except `data/`, `reports/`, `logs/`):

**Core engine**
- `allocate.py` (922 lines) — the whole system's entry point. CLI parsing, market-data fetch, allocation/trim logic (`plan()`), Markdown rendering, holdings/margin state I/O, performance logging. Everything funnels through this one file.
- `levels.py` (218 lines) — secondary entry point (`--levels`). Independent buy-rung staging report. Imports `build_roster` from `allocate.py` (a late/deferred import specifically to dodge a circular-import — `allocate.py` doesn't import `levels.py` at module scope, only inside `main()`).

**Data sources (all read-only, all wrapped for graceful degradation)**
- `alpaca_client.py` (138 lines) — Alpaca paper-account HTTP client. Order-placement methods deliberately removed (`PAPER_ONLY` guard on the base URL too).
- `earnings.py` (92 lines) — yfinance earnings-date lookup, `curl_cffi` session pinned to a specific TLS fingerprint to survive this environment's proxy, `_YAHOO_SYMBOL` translation table for symbol mismatches (currently just `BRK.B`→`BRK-B`).
- `crypto.py` (94 lines) — crypto pricing: Alpaca for majors, CoinGecko for anything Alpaca doesn't carry.

**Analytics (pure functions, no I/O)**
- `indicators.py` (78 lines) — SMA/RSI/ATR/swing-low over a bar list. Wilder smoothing. Clean, dependency-light (pandas only), now unit-tested (`test_indicators.py`).
- `regime_gate.py` (62 lines) — 200-day EMA regime check. `regime_ok_from_closes()` is live and used (informational display only, per the 2026-07-14 regime-gate backtest verdict). `load_daily()`/`attach_regime()` are **dead** — see §6.

**Config (YAML, hand-edited, config-is-truth)**
- `targets.yaml` — tier structure, weights, cluster caps, gates, margin doctrine parameters, crypto sleeve config, levels config. This is the single most load-bearing file in the repo.
- `holdings.yaml` — position state: `shares` (ticker→qty, live-priced), `crypto_shares` (coin→qty, live-priced), `holdings` (ticker→manual $ value, fallback for SKHY only), `margin` (debt/buffer_pct/synced_at).

**Doctrine / record**
- `CLAUDE.md` — the actual single source of truth for *why* the system behaves as it does: Decisions Log (closed questions with rationale), Open Items, Guardrails, workflow. This is not a code file but it is load-bearing — several of the code's numeric constants (1.5x T1/T2 ceiling, 1.8x leverage cap, 25%/20%/20% cluster caps) only make sense with this doc alongside them.
- `README.md` — **stale** (see §6). Describes a version of the system from before the regime-gate removal, before cluster caps beyond semis, before the T1/T2 ceiling, before `update-shares`/`update-crypto-shares`/`update-margin`/`--levels`/`--performance` existed.

**Backtesting framework** (one-shot, pre-committed-threshold, "one test one verdict" — never re-run without new data)
- `backtest_regime.py`, `backtest_trend.py`, `backtest_trims.py`, `backtest_weights.py`, `backtest_rungs.py`, `backtest_t1t2_trim.py` — six scripts, each testing exactly one doctrine question, each writing its own `reports/*_backtest.md`. Verdicts already folded into `CLAUDE.md`'s Decisions Log.
- `verify_rungs.py` — diagnostic chart/table generator (not a backtest itself; replays `backtest_rungs.py`'s mechanics and renders `reports/verification/*.png` + `*_table.md` so the rung backtest can be eyeballed against reality). Depends on `matplotlib`, the only file in the repo that does.

**Tests**
- `test_indicators.py`, `test_margin.py`, `test_resolve_holdings.py`, `test_rungs.py` — 38 tests total, all passing. Real unit coverage for the financially consequential code paths (margin math, cluster/T1T2 trims, live-pricing resolution, indicators).

**Generated / cached artifacts** (not source)
- `logs/allocation-*.md`, `logs/levels-*.md` — every run's full output, timestamped. Git-ignored... actually **not** git-ignored currently (see §6 — `logs/` is excluded per `.gitignore` but individual runs are still being referenced from `CLAUDE.md`; worth confirming intent).
- `performance_log.csv` — one row per day, net equity vs QQQ/VOO. Small, committed, append-only.
- `data/backtest/*.json` (12MB) — cached daily bars per ticker, the only input the backtest scripts read. Actively used.
- `data/daily/*.csv`, `data/hourly/*.csv` (~3.5MB combined) — **dead**, see §6.
- `reports/*.md`, `reports/verification/*` — backtest verdicts and their verification charts. Source-of-record, committed.

---

## 2. Data flow

Two independent flows exist. They do not share a code path, only a config/state layer.

### Live advisory flow (`allocate.py`, `levels.py`)

```
targets.yaml ──┐
               ├─→ build_roster() ─┐
holdings.yaml ─┤                   │
               │                   ▼
               │            fetch_market() ──→ Alpaca bars (IEX feed)
               │                   │                  │
               │                   │                  ▼
               │                   │           indicators.compute_all()
               │                   │           (SMA/RSI/ATR per ticker)
               │                   ▼                  │
               │            resolve_holdings() ←───────┘
               │            (qty × live price;         earnings.days_until_earnings()
               │             manual $ fallback           (yfinance, per candidate)
               │             for SKHY only)                      │
               │                   │                              │
               │                   ▼                              ▼
               └──────────→      plan()  ←── margin_capacity() ←── holdings.yaml margin:
                                   │          (leverage cap, buffer floor)
                                   ▼
                              render() ──→ stdout + logs/allocation-*.md
                                   │
                                   ▼
                          log_performance() ──→ performance_log.csv
```

`--levels` is a parallel, simpler flow: `build_roster()` (borrowed from `allocate.py`) → per-ticker bars → `indicators.compute_all()` + `swing_low()` → `compute_levels()` → `stance_for()` → render. It does **not** go through `plan()` — it has its own regime/earnings gating logic, duplicated in spirit (see §6).

State mutation only happens via the `update-*` commands (`update-holdings`, `update-shares`, `update-crypto-shares`, `update-margin`), all of which funnel through `write_state()` → rewrites `holdings.yaml` → triggers an automatic `log_performance()` snapshot. Nothing in the live flow ever writes to `targets.yaml` — tier/cap/gate changes are always a manual edit.

### Backtest flow (`backtest_*.py`)

```
targets.yaml (universe/weights only — caps, T1/T2 ceiling explicitly
              excluded as "new, not historically meaningful")
     │
     ▼
data/backtest/*.json (cached bars, NOT live Alpaca calls)
     │
     ▼
per-arm simulate() ── deposits, trims, buys, day-by-day mark-to-market
     │
     ▼
twr_annualized() + max_drawdown() ──→ verdict() ──→ reports/*_backtest.md
                                                          │
                                                          ▼
                                              (manually) folded into
                                              CLAUDE.md Decisions Log
```

This flow never touches `holdings.yaml`, never calls Alpaca live, and never affects a live run's behavior directly — its *output* (a verdict) becomes a manual doctrine edit to `targets.yaml`'s gates/caps and a `CLAUDE.md` entry. There is no automated link between "backtest says X" and "production does X" — every single adoption so far has been a human-reviewed, hand-edited config change. This is a deliberate, currently-working safety property (no auto-deploy of backtest conclusions) but also means a backtest verdict and the code's actual behavior can silently drift apart, as already happened once this session (§6, T1/T2 ceiling floor-vs-ceiling mismatch).

---

## 3. Module-by-module summary

| Module | Responsibility | Depends on | Depended on by |
|---|---|---|---|
| `allocate.py` | CLI, orchestration, allocation logic, rendering, state I/O, performance log | `alpaca_client`, `indicators`, `regime_gate`, `earnings`, `crypto`, `yaml` | `levels.py` (late import of `build_roster` only), all six `backtest_*.py` reuse its *concepts* but not its code |
| `levels.py` | Buy-rung staging (`--levels`) | `indicators`, `earnings`, `regime_gate`, `crypto`, `allocate.build_roster` | nothing |
| `alpaca_client.py` | Read-only Alpaca HTTP wrapper | `certifi` | `allocate.py`, `levels.py`, `market_hours.py` (dead path), backtests do NOT use it (they use the JSON cache) |
| `earnings.py` | Next-earnings-date lookup, degrades to `unavailable` | `yfinance`, `curl_cffi` | `allocate.py`, `levels.py` |
| `crypto.py` | Crypto sleeve pricing | `certifi` | `allocate.py`, `levels.py` |
| `indicators.py` | SMA/RSI/ATR/swing-low, pure functions | `pandas` | `allocate.py` (via `compute_all()`), `levels.py`, `test_indicators.py` |
| `regime_gate.py` | 200-EMA regime check | `pandas` | `allocate.py`, `levels.py`, `backtest_regime.py` (imports `regime_ok_from_closes`) |
| `market_hours.py` | Market-open gate | `alpaca_client` (lazy import) | **nothing** — dead |
| `backtest_regime.py` | Regime-gate backtest + shared helpers | `yaml`, `regime_gate` | `backtest_trend.py`, `backtest_t1t2_trim.py` (import shared helpers) |
| `backtest_trend.py` | Trend-gate backtest | `backtest_regime` | nothing |
| `backtest_trims.py` | Band/spec trim-rule backtest | `yaml` (self-contained, duplicates helpers) | nothing |
| `backtest_weights.py` | Tier-weight-structure backtest | `yaml` (self-contained, duplicates helpers) | nothing |
| `backtest_rungs.py` | Rung-vs-market-buy backtest | `yaml` (self-contained, duplicates helpers) | `verify_rungs.py` (imports its sim functions directly) |
| `backtest_t1t2_trim.py` | T1/T2 concentration-ceiling backtest | `backtest_regime`, `backtest_trend` | nothing |
| `verify_rungs.py` | Renders verification charts for the rung backtest | `backtest_rungs`, `matplotlib` | nothing |
| `test_*.py` | Unit tests | the module under test | nothing (leaves) |

**Note on `indicators.py`:** verified directly — `allocate.py`'s `fetch_market()` (line 88) calls `compute_all(bars)`, imported from `indicators.py` at the top of the file (line 29). Same function, same formulas, both entry points. No drift. (An earlier draft of this audit flagged this as unconfirmed/possible drift before actually reading `fetch_market()`'s body — corrected here rather than left as an open question, per the repo's own "verify before acting" standard.)

---

## 4. Current strengths

- **Doctrine-as-code discipline is real, not aspirational.** Every mechanical rule (cluster caps, T1/T2 ceiling, margin cap/floor) traces to a `CLAUDE.md` Decisions Log entry with its reasoning, and every backtest follows the same pre-committed-threshold, one-verdict, no-relitigating pattern. This is unusually rigorous for a single-user tool.
- **Advisory-only is enforced structurally, not just by convention.** Order-placement methods are physically absent from `alpaca_client.py`, not merely unused — a future session (or an AI agent) cannot accidentally wire up live trading without first re-adding removed code, which is a deliberate speed bump.
- **Graceful degradation is the default posture across every data source.** Yahoo/yfinance, CoinGecko, and Alpaca bars all fail into an explicit "unavailable"/`None` + error string rather than raising or silently substituting a wrong value. `resolve_holdings()` specifically falls back to the last-known manual value rather than zeroing a position on a transient price-fetch miss.
- **The margin/leverage model is mechanical and testable**, and it has real unit coverage (`test_margin.py`) for the exact scenarios that matter (buffer-floor hard cutoff, leverage-cap clipping, cluster-cap multi-membership).
- **The backtest framework caught its own mistakes twice this session** — the regime gate and trend gate were both *removed* from production because their own backtests said they cost money, which is the opposite of what a system usually does with sunk-cost infrastructure.
- **Config/doctrine separation is clean where it's been applied**: `targets.yaml` is genuinely config-is-truth for tiers/caps/gates, and no live code silently overrides it.

---

## 5. Weaknesses

- **`allocate.py` is a monolith.** 922 lines doing CLI parsing, market-data orchestration, the entire allocation/trim algorithm, Markdown rendering, three different `update-*` state-mutation commands, and performance logging. There is no internal module boundary — `plan()` alone is ~230 lines with margin math, band/spec trims, the new T1/T2 ceiling, cluster-cap trims, crypto-sleeve gap logic, and the greedy buy allocator all in one function body.
- **Two independent gating implementations** (`allocate.py`'s `plan()` and `levels.py`'s `stance_for()`) reimplement earnings-blackout and trend/regime logic separately rather than sharing one gate-evaluation function. They have already drifted (see §6 — `levels.py` still blocks on regime-bearish; `plan()` doesn't).
- **The backtest scripts duplicate ~150 lines of identical helper code four different ways** (`twr_annualized`, `max_drawdown`, `rsi_series`, `universe`, `load_bars` each reimplemented in `backtest_trims.py` and `backtest_weights.py` instead of importing from `backtest_regime.py`, which `backtest_trend.py` and `backtest_t1t2_trim.py` do correctly). Functionally harmless today (each copy is currently identical) but a real risk the next time one needs a bugfix — five files to remember to touch, not one.
- **No structured/queryable decision record.** The Decisions Log is a single wall of prose bullets inside `CLAUDE.md`. It's excellent for a human reading top-to-bottom, but there's no way to programmatically ask "what's the current T1/T2 ceiling multiple and where did it come from" without grep + reading prose. As the log grows, this will only get harder to navigate.
- **`README.md` actively misdescribes the current system** (§6) — a real onboarding hazard for any future session or collaborator who reads it before `CLAUDE.md`.
- **No dedicated risk/health view.** Margin, cluster caps, and the T1/T2 ceiling are each computed and rendered piecemeal inside `render()`'s summary section; there's no single "how much risk is this book actually carrying right now" report that pulls leverage, concentration, and crypto-sleeve drift together with historical context (e.g., "leverage has been rising for N consecutive syncs").

---

## 6. Technical debt (concrete findings)

1. **Dead code, confirmed via grep — nothing else in the repo calls these:**
   - `market_hours.py` (entire file — `market_open()`, `is_market_hours_local()`) — zero callers.
   - `alpaca_client.py`'s `get_account()`, `get_position()` — zero callers (only `get_clock()` is referenced, and only by the also-dead `market_hours.py`).
   - `regime_gate.py`'s `load_daily()` / `attach_regime()` — zero callers. Only `regime_ok_from_closes()` is live.
   - `data/daily/*.csv` (420KB) and `data/hourly/*.csv` (3.1MB) — only ever read by the dead `load_daily()`. ~3.5MB of committed, unused data.
   - These all trace to the same origin per their docstrings ("harvested from trading-intelligence") — remnants of an earlier, more automated predecessor system that were pulled in wholesale and never fully pruned.

2. **`levels.py`'s regime gate is stale relative to `allocate.py`'s.** `stance_for()` still returns `BLOCKED` when `regime_bearish` is true. But the 2026-07-14 regime-gate backtest verdict (`reports/regime_backtest.md`, Decisions Log) explicitly removed this exact gate from `allocate.py`'s `plan()` — "no longer blocks/zeroes deployment when QQQ is below its 200-day EMA." That removal was never mirrored into `levels.py`. Right now the two entry points would give **contradictory advice** in a below-200-EMA market: `allocate.py` says buy the gaps, `--levels` says every name is BLOCKED. This is a real, live inconsistency, not hypothetical — worth fixing regardless of the larger architecture question.

3. **Duplicated backtest helpers** (detailed in §5) — `twr_annualized`, `max_drawdown`, `rsi_series`, `universe`, `load_bars` each exist in 3-4 copies across `backtest_regime.py`, `backtest_trims.py`, `backtest_weights.py`, `backtest_rungs.py`. `backtest_trend.py` and `backtest_t1t2_trim.py` demonstrate the fix already works (`from backtest_regime import (...)`) — the other three just predate that pattern.

4. **`README.md` is stale enough to be actively misleading.** It documents: the regime gate as an active blocking gate (removed 2026-07-14); only the semis cluster cap (two more exist — power_infra, oil); no T1/T2 ceiling; no `update-shares`/`update-crypto-shares`/`update-margin`/`--levels`/`--performance`/`log-performance` commands (all exist and are part of the routine workflow); `holdings.yaml` described as flat `{ticker: value}` when it's actually a three-block structure (`shares`/`crypto_shares`/`holdings`) plus a `margin` block. A new session or collaborator reading `README.md` first would be working from a meaningfully wrong model of the system.

5. **The T1/T2 concentration ceiling shipped a different rule than the one backtested**, and this is already documented honestly in `CLAUDE.md`'s Decisions Log (2026-07-15 entry) — flagging it here only because it's a good illustration of the "backtest verdict ≠ production behavior" gap noted in §2's data-flow section: `t1t2_trim_backtest.md` tested a *ceiling-style* trim (excess above 1.5x trimmed to exactly 1.5x); production ships a *floor-at-target* trim (down to 1.0x, matching the cluster-cap mechanism). The ~0.02pp "basically free" backtest number does not apply to the shipped rule. Already caught and corrected in the log — cited here as a pattern to watch for, since nothing in the tooling would catch this class of drift automatically.

6. **`logs/` — the `.gitignore` origin vs. the workflow's own references need reconciling.** `logs/allocation-*.md` and `logs/levels-*.md` are generated every run and are `.gitignore`d (confirmed: `logs/` appears in `.gitignore`). That's a reasonable default. But it means the "record" of exactly what was recommended on any given day only exists locally, per-session — it doesn't survive a fresh clone or a different machine, unlike `performance_log.csv` (committed) or `CLAUDE.md`'s Decisions Log (committed). If the intent is "logs are disposable, `performance_log.csv` + `CLAUDE.md` are the permanent record," that's fine and consistent — just confirming it's intentional, since a "Portfolio HQ" system with a "capital allocation history" goal (per the long-term vision) will need *some* permanent, structured record of every recommendation, not just the outcome snapshot.

---

## 7. Missing capabilities (vs. the stated long-term vision)

Going through the requested list against what actually exists today:

| Vision capability | Current state |
|---|---|
| Portfolio allocation engine | **Exists** — `allocate.py`'s `plan()`. Mature. |
| Portfolio review engine | **Exists** — `--review` mode. Mature. |
| Risk management | **Partially exists**, fragmented — leverage cap, buffer floor, cluster caps, T1/T2 ceiling are all real and enforced, but there's no single "risk" view; each lives in its own corner of `plan()`/`render()`. |
| Margin intelligence | **Partially exists** — leverage/buffer computed and shown every run, staleness-warned (`STALE_MARGIN_DAYS`). No trend/history view (is buffer rising or falling over time?). |
| Margin repayment recommendations | **Does not exist.** The system currently only *reacts* (block buys, or the guardrail's "recommend de-lever" prose) — it never computes "here's how much to pay down and from where" the way it computes buy/trim dollar amounts. Real gap, and the most concretely actionable missing piece on this list. |
| Performance tracking | **Exists**, basic — `performance_log.csv` + `render_performance()`. Explicitly caveated as "not a precise return calc" (deposits/withdrawals aren't backed out). A true TWR-based live performance tracker (mirroring the backtest framework's own `twr_annualized()`) does not exist for the *real* account. |
| Market regime analysis | **Exists**, informational-only (correctly, per the backtest verdict) — shown but doesn't gate. |
| Position sizing | **Exists** — tier weights are position sizing. |
| Concentration management | **Exists** — cluster caps + T1/T2 ceiling. |
| Investment thesis management | **Does not exist — and building it would contradict standing doctrine.** See the flag below. |
| Decision logging | **Exists, but unstructured** — `CLAUDE.md`'s Decisions Log is prose, not data. See §6.3 and the recommendation in §8. |
| Backtesting framework | **Exists**, mature, well-disciplined. The one part of this vision list that's already best-in-class. |
| Reporting | **Exists, minimal** — per-run Markdown logs + the summary embedded in each `render()` call. No aggregate/trend reporting across runs. |
| Capital allocation history | **Partially exists** — `performance_log.csv` has net-equity snapshots; `logs/*.md` has per-run detail but isn't committed (see §6.6). No unified, queryable "every dollar deployed, when, why" record. |
| Portfolio health dashboard | **Does not exist.** Would naturally combine risk management + margin intelligence + concentration management + performance tracking into one view — see §8 for where this fits in build order. |

### Flag: "Investment thesis management" conflicts with existing doctrine

This is the one item on the long-term-vision list that isn't just "not built yet" — it's something the system has **explicitly and repeatedly declined to build**, on the record, multiple times:

> "No predictive research, price targets, or 'opportunity maps' — the tool computes opportunities at runtime on deposit day." (Guardrails)

> "Proposals to build new analysis/research/thesis systems → cite the Decisions Log first; the backtest showed added layers subtract value." (Guardrails)

> The June 2026 band-overlay backtest (227% vs 422% buy-and-hold) → **NO-GO on automated trading**, explicitly because "elaborate analysis layers were anti-predictive."

> The declined "rationalize all 65 holdings" request and the twice-declined "is this company worth holding" question earlier in this same session — both explicitly rejected as fundamentals/thesis research the system's design deliberately excludes.

"Investment thesis management" as a capability — tracking *why* a position is held, a bull/bear case, a price target, a conviction re-rating over time — is precisely the category of "standing analysis layer" this repo's own Decisions Log has rejected every time it's come up, on the stated grounds that it doesn't improve returns and invites exactly the kind of predictive-research mission creep the tool was built to avoid. Building it would not be a neutral architecture addition; it would be **reversing a standing decision** without new evidence, which the doctrine's own rules (§ Decisions Log framing, "do not relitigate without new evidence") would require calling out explicitly rather than quietly implementing because it appeared on a vision list.

This doesn't mean "decision logging" is off the table — a structured version of what `CLAUDE.md`'s Decisions Log already does (doctrine changes, backtest verdicts, why a cap was added) is a *different* thing from thesis/conviction tracking on individual holdings, and is recommended in §8. The distinction matters: **logging decisions the system already makes is fine; building infrastructure to originate new investment opinions is the thing that's been rejected.**

---

## 8. Recommended implementation order

Ordered by dependency and risk, not by how interesting each item is. Each stage is meant to be shippable and reviewable on its own — nothing here should be a single giant PR.

**Stage 0 — Cleanup (no behavior change, do this first regardless of what comes next)**
1. Delete or explicitly archive dead code: `market_hours.py`, `get_account()`/`get_position()` in `alpaca_client.py`, `load_daily()`/`attach_regime()` in `regime_gate.py`, and `data/daily/`/`data/hourly/`. If any of this is actually wanted for a future capability, keep it — but decide on purpose, not by inertia.
2. Rewrite `README.md` to match current reality (regime gate informational-only, all three cluster caps, T1/T2 ceiling, full command list, actual `holdings.yaml` shape).
3. Fix `levels.py`'s stale regime-block to match `plan()`'s (informational-only, not blocking) — this is a real behavioral bug, not just cleanup, and should probably happen before Stage 0's other items since it's user-facing.
4. Extract the duplicated backtest helpers (`twr_annualized`, `max_drawdown`, `rsi_series`, `universe`, `load_bars`) into one shared module (`backtest_lib.py`, or just finish migrating everything onto `backtest_regime.py`'s existing versions the way `backtest_trend.py` already does).

**Stage 1 — Structure the decision record (foundation for everything else)**
5. Add a structured decisions log — e.g. `decisions/*.yaml` or a single `decisions.jsonl`, one entry per doctrine change/backtest verdict, with fields like `date`, `category`, `summary`, `parameters_changed`, `report_ref`. `CLAUDE.md`'s prose log stays as the human-readable narrative (don't replace it — it's genuinely good writing that a structured format would flatten); the structured version is additive, queryable, and is what a future "health dashboard" or "capital allocation history" view would actually read from.

**Stage 2 — Margin intelligence + repayment (the concretely missing piece)**
6. Margin repayment recommendations: given current debt, buffer, and buffer floor, compute a suggested paydown amount/schedule the same way `plan()` computes buy amounts — mechanical, explainable, advisory-only (no auto-payment, obviously). This is a natural extension of `margin_capacity()`, which already has the core math.
7. Margin/leverage history — extend `performance_log.csv` (or a sibling file) to make "is leverage trending up or down over the last N syncs" answerable without manually scanning CSV rows.

**Stage 3 — Unified risk / health view**
8. A `--health` (or similar) report that pulls together: leverage vs cap, buffer vs floor, every cluster's %-of-book vs cap, T1/T2 names near (not just over) the 1.5x ceiling, crypto sleeve drift, and margin trend from Stage 2. This is mostly *composition* of numbers `plan()` already computes — low new-logic risk, mostly a new render function.

**Stage 4 — True performance tracking**
9. A TWR-based live tracker that correctly backs out deposits/withdrawals/margin draws (the exact caveat `render_performance()` already admits it can't handle). This is real new math, more involved than it sounds — treat it with the same care as `twr_annualized()` in the backtest framework, including a dedicated test.

**Explicitly not recommended without a separate conversation first:**
- Investment thesis management — see §7's flag. Bring this back as its own discussion, not a line item, given it conflicts with standing doctrine.
- Any form of automated "backtest verdict → production config" pipeline. The current human-in-the-loop step (read the report, hand-edit `targets.yaml`, write the Decisions Log entry) is slower but is also what caught the floor-vs-ceiling drift in §6.5 before it went uncorrected — automating it away would remove the exact check that just worked.

---

## 9. Complexity estimates

| # | Item | Complexity | Why |
|---|---|---|---|
| 1 | Delete dead code | Trivial | Deletion + a grep to confirm zero remaining references (already done in this audit). |
| 2 | Rewrite README | Small | Documentation only, no logic. |
| 3 | Fix `levels.py` regime gate | Small | One conditional, mirrors an already-shipped change in `plan()`. |
| 4 | Dedupe backtest helpers | Small–Medium | Mechanical for the pure-math functions (`twr_annualized`, `max_drawdown`); slightly more care needed for `universe()`/`load_bars()` since arg signatures differ slightly between files. |
| 5 | Structured decisions log | Medium | New schema design + a migration pass to backfill existing Decisions Log entries (backfill is optional/gradual — could start structured-only going forward). |
| 6 | Margin repayment recommendations | Medium | New math, but built directly on `margin_capacity()`'s existing model; needs its own test suite given how consequential margin logic is (see `test_margin.py`'s existing bar for rigor). |
| 7 | Margin/leverage history | Small–Medium | Data-plumbing mostly; the interesting part is deciding what "trending" means (window length, smoothing) — a small design decision, not a big build. |
| 8 | Health dashboard/report | Medium | Mostly composition of existing computed values into a new view; the main cost is deciding what belongs and design/render work, not new financial logic. |
| 9 | True TWR performance tracker | Large | Genuinely hard problem (correctly separating market return from cash-flow effects on an account with irregular deposits/withdrawals/margin draws) — this is the most involved item on the list and deserves to be treated like a mini version of the backtest framework, with its own pre-committed correctness tests before trusting the number. |

---

## 10. Risks per recommendation

| # | Item | Risk if done | Risk if *not* done |
|---|---|---|---|
| 1 | Delete dead code | Very low — confirmed zero callers via grep across the whole repo. Only risk is deleting something a *future* plan (e.g. this very roadmap's Stage 2-4) intends to reuse — worth a final check against §8 before deleting, not before this audit's read-only pass. | Continues to cost a few minutes of confusion every time a new session/reviewer encounters `market_hours.py` or the `data/daily` directory and has to determine (again) that it's unused. |
| 2 | Rewrite README | Very low. Pure documentation. | Actively misleads anyone who reads it before `CLAUDE.md` — this is the higher-risk path, not the fix. |
| 3 | Fix `levels.py` regime gate | Low — small, well-understood change mirroring already-shipped logic in `plan()`. | `--levels` continues to give advice contradicting `--review`/`--cash` during any future below-200-EMA stretch — a real, user-facing correctness bug sitting live right now. |
| 4 | Dedupe backtest helpers | Low — the target end-state (`backtest_trend.py`'s import pattern) already exists and works; this is mechanical convergence, not new design. | Next helper bugfix has to remember to touch 4 files instead of 1; a missed one silently produces a wrong backtest verdict that looks identical in shape to a correct one — the worst kind of bug for a system whose credibility depends on backtest rigor. |
| 5 | Structured decisions log | Low-medium — additive, doesn't replace or risk the existing prose log; main risk is scope creep into "let's also make it a general-purpose database" (resist that). | Every future capability that wants to *read* "what's the current T1/T2 multiple and why" (a health dashboard, a repayment recommender that wants to cite doctrine) has to grep prose instead of querying data — compounds with every new capability built on top. |
| 6 | Margin repayment recommendations | Medium — this is real financial logic with real consequences if wrong (recommending too little paydown given a real emergency, or being overly conservative and recommending unnecessary paydowns). Needs `test_margin.py`-grade test coverage before trusting it, same bar as the existing margin code. | The one concretely-requested capability with no current answer — right now the system can tell you you're in trouble (forced de-lever guardrail) but not exactly how to fix it with numbers, which is exactly what this tool does for every *other* decision. |
| 7 | Margin/leverage history | Low. | Minor — "is my leverage trending up" is currently answerable by scrolling `performance_log.csv` manually; a real gap but not a dangerous one. |
| 8 | Health dashboard | Low-medium — mostly composition risk (are all the right numbers actually pulled in, none stale/mismatched) rather than new-logic risk. | Risk stays diffuse rather than concentrated — margin, concentration, and drift are each individually visible today, just not summarized together, so the main cost of not doing this is convenience, not correctness. |
| 9 | True TWR performance tracker | **Medium-high** — this is the riskiest item on the list to get subtly wrong, because a wrong TWR number *looks* authoritative and could quietly mislead a real capital decision (e.g., "the system says I'm beating QQQ" when a calculation error is hiding underperformance). Needs the same "pre-committed, one test, verified against a known case" discipline the backtest framework already uses for itself. | The account's real performance-vs-benchmark comparison stays a rough directional check, explicitly caveated as such — honest but limited. |

---

## Summary

The repository's core (`allocate.py` + `targets.yaml` + `holdings.yaml` + the backtest framework + `CLAUDE.md`'s doctrine) is genuinely solid and shouldn't be rewritten. The real findings from this audit are:

- **A handful of concrete, low-risk cleanup items** (dead code, a stale README, one live behavioral bug in `levels.py`, duplicated backtest helpers) that should happen regardless of what's built next.
- **One genuinely missing, concretely useful capability** — margin repayment recommendations — that fits naturally on top of existing, tested math.
- **One item on the requested vision list that shouldn't be built as specified** — investment thesis management directly contradicts multiple standing, evidence-based doctrine decisions in this same repo, and should come back as its own conversation rather than get built because it appeared on a list.

No code was changed to produce this report. Recommend reviewing the roadmap in §8 together before starting Stage 0.
