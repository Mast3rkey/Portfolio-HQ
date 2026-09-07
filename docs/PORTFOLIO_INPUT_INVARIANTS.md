# Portfolio Input Invariants

> **⚠️ Documentation only — no code, no production changes, no validation proposals.** Per `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md` (frozen, not modified). This document records what the current allocator (`allocate.py`) *assumes* about each input inventoried in `docs/PORTFOLIO_INPUT_INVENTORY.md` — not what it should assume, not what would be better. Every assumption below is either explicit (stated directly in code, comments, or `CLAUDE.md`) or implicit (never stated, inferred only from how the code behaves when the assumption is violated). No recommendation to add validation, strengthen a check, or change behavior appears anywhere in this document.

_Written 2026-07-17. Item numbers below correspond directly to `docs/PORTFOLIO_INPUT_INVENTORY.md`'s 35-item numbering — this document does not re-derive origin/storage/consumption (already traced there); it adds the assumption/explicit-implicit/violation-handling layer only. Sources re-read for this pass: `allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, `CLAUDE.md`, plus the inventory document itself._

## Violation-handling vocabulary

- **Prevented** — the code structurally cannot accept the violating state (e.g., a value is clamped, or a type error would stop execution before a bad value is used).
- **Detected** — the violation is checked for and surfaced (a warning, an error string, a distinct BLOCKED row) at or before the point the bad input would otherwise cause silent harm.
- **Tolerated** — the code has an explicit fallback path for the violation (doesn't crash, doesn't silently corrupt other data) but does not surface a warning to the reader.
- **Silent** — the violation produces no distinguishable signal at all; the output looks the same as if the assumption had held.

A single input can have more than one assumption, and different assumptions about the same input can fall into different categories — each is recorded separately below.

---

## Summary table (illustrative subset)

| Input | Assumption | Explicit? | Violation handling |
|---|---|---|---|
| Tier membership (item 4) | Each ticker appears in exactly one tier list | Implicit | Silent — last-processed tier silently wins |
| Share counts (items 12-13) | Entered counts are correct; large changes are intentional | Mixed | `holdings` fallback guarded (30% check); `shares`/`crypto_shares` unguarded |
| Margin state config (item 19) | Missing CAUTION/RESTRICTED config means those states are intentionally off | Explicit | Prevented-by-design — `None` config is a defined "path does not fire" behavior, not a crash |
| Regime status (item 21/25) | Informational only, never gates a decision | Explicit | Prevented-by-design — `plan()`'s body never branches on `regime_ok` |
| Margin sync freshness (item 15) | Debt/buffer stay accurate until re-synced | Explicit (partial) | Detected for staleness (2-day age check); Silent for a same-day wrong value |
| Concentration score scope (item 32) | Portfolio concentration pressure = cluster-cap proximity only | Explicit | Prevented-by-design — code comment states T1/T2 is "deferred, not a placeholder" |
| Cluster/tier weight sums | Percentages entered are individually and collectively sane | Implicit | Silent — no sum-to-100%, no range check anywhere |

The full 35-item breakdown follows.

---

## Universe membership

### 1. Roster ticker list

- **Assumption A:** Every string in a tier's `tickers` list is a valid, tradeable symbol recognized by both Alpaca and yfinance.
  - **Explicit?** Implicit — never stated, never validated at config-load time.
  - **Violation handling:** **Detected**, but late — `fetch_market()`'s per-symbol try/except (allocate.py:79-83) catches a fetch failure and records an `"error"` string; `plan()` then surfaces this as a BLOCKED "no-data" row. The violation is visible in the output, but only after a full run, not at the point the ticker was added.
- **Assumption B:** A ticker belongs to exactly one tier.
  - **Explicit?** Implicit — no code or comment states this; inferred entirely from `build_roster()`'s dict-construction behavior.
  - **Violation handling:** **Silent** — a ticker listed in two tiers is overwritten in `roster` by whichever tier is processed last (YAML key order: T1, T2, ETF, band, spec); no warning, no error, no trace in any output that this happened.

---

## Sleeve assignments

### 2. Crypto sleeve coin list

- **Assumption:** Every coin in `crypto.coins` either has Alpaca coverage or a `coingecko_ids` entry.
  - **Explicit?** Implicit.
  - **Violation handling:** **Mixed.** The per-coin display row is **Detected** (`render()` shows `n/a (error)` with the specific error string). The aggregate consequence is **Silent** — `resolve_holdings()`'s `{t: v for t, v in result.items() if v}` filter (allocate.py:140) drops the failed coin from the dict entirely, so `sleeve_val` is quietly understated with no aggregate-level warning that the sleeve total itself is incomplete.

### 3. `coingecko_ids` mapping

- **Assumption:** The mapping is complete and correctly routes every coin that actually needs CoinGecko.
  - **Explicit?** Implicit.
  - **Violation handling:** **Silent.** A coin needing CoinGecko routing but missing from this map is routed to Alpaca instead (`fetch_crypto()`'s `alpaca_coins = [c for c in coins if c not in coingecko_ids]`, crypto.py:67); if Alpaca doesn't carry it, the resulting `n/a` looks identical to any other fetch failure — nothing distinguishes "wrong routing" from "the API is down."

---

## Tier assignments

### 4. Per-ticker tier membership

Same as item 1, Assumption B — restated here for completeness since it is fundamentally a tier-assignment invariant, not a universe-membership one:

- **Assumption:** Each ticker's tier placement is singular and intentional.
  - **Explicit?** Implicit.
  - **Violation handling:** **Silent** (see item 1B for the exact mechanism).

---

## Target weights

### 5. `weight_pct` per tier

- **Assumption:** The five tier weights, applied across each tier's roster size, are individually sane (non-negative, not absurdly large) and collectively produce a total allocation the account holder intends.
  - **Explicit?** Implicit — no sum-to-100%-equivalent check, no range check, anywhere in `build_roster()` or `plan()`.
  - **Violation handling:** **Silent.** An incorrect `weight_pct` — including a negative one, which nothing in `float(tier.get("weight_pct", 0))` (allocate.py:59) rejects — flows directly into `target_dollars = book * weight_pct / 100.0` with no bound.

### 6. `cap_multiple` (band tier)

- **Assumption:** `cap_multiple >= 1.0` (a ceiling should not sit below the target it's supposed to cap).
  - **Explicit?** Implicit.
  - **Violation handling:** **Tolerated.** `max_by_name = max(0.0, name_ceiling - current)` (allocate.py:271) prevents a negative buy-ceiling from becoming a negative allocation, but a `cap_multiple < 1.0` would still silently produce a ceiling below the target with no warning that the configuration is internally inconsistent.

### 7. `fixed` flag (spec tier)

- **Assumption:** `fixed: true` and the tier's own `cap_multiple` (defaulting to 1.0 when unset, allocate.py:61) are expected to agree — both currently produce the same "never above target" behavior for `spec`.
  - **Explicit?** Explicit — directly coded as two parallel conditions (`meta["fixed"]` and `meta["cap_multiple"]`) that happen to coincide for the current config.
  - **Violation handling:** **Tolerated** — if `fixed` were removed from `spec`'s config, the tier's ceiling behavior would be unaffected today only because `cap_multiple` also defaults to 1.0; this coincidence is not itself checked or asserted anywhere.

### 8. `crypto.sleeve_pct`

- **Assumption:** The value is a sane percentage of book (implicitly 0–100, though nothing enforces even a positive number).
  - **Explicit?** Implicit.
  - **Violation handling:** **Silent** — flows directly into `sleeve_target = book * sleeve_pct / 100.0` (allocate.py:329) with no bound.

---

## Cluster definitions

### 9. Cluster `pct` caps

- **Assumption:** Each cluster's `pct` cap continues to reflect real correlation risk over time — i.e., the correlation scan behind each value (documented in `targets.yaml`'s comments as a one-time, trailing-~1yr analysis) remains valid indefinitely.
  - **Explicit?** Mixed — the *origin* of each value is explicitly documented (comments cite the scan and its date); the *ongoing validity* of that value is an implicit, unstated assumption with no expiry or re-check mechanism.
  - **Violation handling:** **Silent.** Unlike margin sync data (item 15), which has an explicit `synced_at`/staleness check, cluster cap values carry no age or re-validation signal anywhere in the code — a correlation regime shift would never be flagged by this system on its own.

### 10. Cluster ticker membership

- **Assumption:** A cluster's ticker list is consistent with (a subset of, or at least overlapping) the roster's tier lists.
  - **Explicit?** Implicit.
  - **Violation handling:** **Silent** — `plan()` computes `tk_clusters` (allocate.py:208) by checking cluster membership against the *roster* loop's own tickers, but nothing checks the reverse: whether every ticker in a cluster's list actually appears in some tier. A cluster ticker absent from every tier list would simply never be visited by the roster loop and would never be flagged as inconsistent.

---

## T1/T2 definitions

### 11. `gates.t1t2_trim_mult`

- **Assumption:** The same multiplier (1.5x) is the correct concentration ceiling for both T1 and T2 tiers, despite their different weight sizes (3.35% vs. 1.65% of book).
  - **Explicit?** Explicit — directly coded as a single shared threshold applied to `meta["tier"] in ("T1", "T2")` (allocate.py:231), and documented in `CLAUDE.md`'s Decisions Log as a deliberate doctrine choice ("same treatment as the cluster caps"), not an oversight.
  - **Violation handling:** Not applicable in the prevented/detected/tolerated/silent sense — there is no "violation" of a shared-threshold design choice; recorded here only as an explicit, uniform assumption worth naming.

---

## Holdings

### 12. `shares` (ticker → qty)

- **Assumption A:** Entered share counts are correct.
  - **Explicit?** Implicit.
  - **Violation handling:** **Silent** for a plausible-looking wrong number (e.g., a digit transposition that still looks like a reasonable share count); **Tolerated** for an implausible one only in the narrow sense that the system won't crash, but nothing distinguishes a wrong value from a right one computationally.
- **Assumption B:** A large change in a position's value between syncs is intentional (a real trade), not a data-entry error.
  - **Explicit?** Mixed — this exact assumption is explicitly checked and enforced for the `holdings` manual-fallback path (item 14) via `BOOK_CHANGE_WARN_PCT`, but the corresponding check does **not** exist for `shares` — confirmed by direct comparison of `update_holdings()` (has the check, allocate.py:602-613) against `update_shares()` (no equivalent check anywhere in its body, allocate.py:622-639).
  - **Violation handling:** **Silent** for `shares` specifically — a fat-fingered share-count paste that swings the book by more than 30% would write through immediately with no abort/confirm step, unlike the same-magnitude swing via `update-holdings`, which is **Detected** and blocked pending `--confirm`.
- **Assumption C:** `qty >= 0` (no short position is modeled).
  - **Explicit?** Implicit — `_parse_ticker_value_pairs()` (allocate.py:562-583) accepts any float, including negative.
  - **Violation handling:** **Tolerated** — a negative qty would produce a negative dollar value in `resolve_holdings()` and flow into `gross`/`book` without a type error, but nothing flags it as an unusual state.

### 13. `crypto_shares` (coin → qty)

- Same three assumptions as item 12, with the same classifications — `update_crypto_shares()` (allocate.py:642-659) has no book-swing check either, confirmed by the same direct comparison.

### 14. `holdings` (manual dollar-value fallback)

- **Assumption A:** A large book-value swing from a manual paste is usually a partial-paste wipe, not an intended change.
  - **Explicit?** Explicit — directly coded and commented (`BOOK_CHANGE_WARN_PCT`'s own comment: "a big book-value swing usually means a partial-paste wipe," allocate.py:602).
  - **Violation handling:** **Detected** — `update_holdings()` aborts and writes nothing if the swing exceeds 30% and `--confirm` wasn't passed (allocate.py:607-613).
- **Assumption B:** A manually-pasted value remains accurate until explicitly re-pasted — no automatic staleness expiry.
  - **Explicit?** Implicit — no `synced_at`-equivalent field exists for the `holdings` block (unlike `margin`, item 15).
  - **Violation handling:** **Silent** — a value pasted once and never updated carries no age indicator anywhere in `render()`'s output, unlike margin data's explicit staleness warning.

### 15. Margin block (`debt`, `buffer_pct`, `synced_at`)

- **Assumption A:** The synced debt/buffer values remain accurate until re-synced, and staleness beyond a threshold is worth flagging.
  - **Explicit?** Explicit — `STALE_MARGIN_DAYS` and its check are directly coded and produce a specific warning message (allocate.py:528-535).
  - **Violation handling:** **Detected** for staleness by date (a sync older than 2 days triggers a visible warning in every report).
- **Assumption B:** A same-day-synced value is correct.
  - **Explicit?** Implicit — no independent check validates a freshly-typed debt/buffer figure against any other source.
  - **Violation handling:** **Silent** — a mistyped number entered the same day it's "synced" passes the staleness check trivially and is treated as fully trustworthy by every downstream computation.

### 16. Orphan positions

- **Assumption:** The account holder will notice and act on (or consciously accept) a position held outside the roster.
  - **Explicit?** Explicit — `render()` unconditionally displays a "Held, not in roster" warning line whenever `orphans` is non-empty (allocate.py:495-498).
  - **Violation handling:** **Detected** (the warning fires every run, every time) but not **Prevented** — nothing stops an orphan from persisting indefinitely across any number of runs; the system has no escalation, repeat-warning intensification, or expiry for this state.

---

## Margin inputs

### 17. `margin.leverage_cap`

- **Assumption:** The configured value matches this account's actual, current real-world margin agreement/doctrine.
  - **Explicit?** Explicit as a doctrine constant (`CLAUDE.md`'s Decisions Log states it directly and calls it fixed, "no discretion, no timing, no exceptions"); implicit that it stays synchronized with reality, since nothing in this codebase cross-checks it against any broker-supplied figure (a gap already surfaced structurally, from a different angle, in `docs/PHASE7A_BROKER_MECHANICS_ASSUMPTION_REGISTRY.md`'s maintenance-margin item).
  - **Violation handling:** **Silent** — if this account's real, effective leverage constraint ever differed from 1.8x, nothing in `allocate.py` or `margin_state.py` would detect the mismatch; both simply trust the configured value.

### 18. `margin.buffer_floor_pct`

- Same assumption structure and classification as item 17.

### 19. `margin.states`/`concentration_adjustment` (currently absent)

- **Assumption:** The absence of these config blocks means CAUTION/RESTRICTED escalation is intentionally disabled, not an oversight or a bug.
  - **Explicit?** Explicit — `margin_state.py`'s own module docstring states this design directly: "if a caller passes None for a threshold, that escalation path simply never fires... this module does not invent a number the project's own discipline says shouldn't exist yet."
  - **Violation handling:** **Prevented-by-design** — this is the one case in this inventory where a missing input is handled by an explicit, documented, intentional fallback rather than a crash, a silent wrong computation, or an unflagged gap. Whether the *current absence itself* reflects an active, ongoing decision or a stalled one is Unknown from the code alone — the code only confirms the mechanism is deliberate, not why the config remains unset today.

---

## Constraints

### 20. `gates.min_lot_dollars`, `trend_rsi_override`, `earnings_blackout_days`, `trim_rsi`

- **Assumption:** These threshold values remain appropriate as the book's size and composition change over time.
  - **Explicit?** Mixed — for `min_lot_dollars` specifically, this exact assumption is already named explicitly *outside* the code, in `CLAUDE.md`'s Open Items ("`min_lot_dollars` ($25) doesn't scale with book size... revisit once the book crosses roughly $25,000"). The other three thresholds carry the same implicit assumption with no equivalent documented trigger.
  - **Violation handling:** **Tolerated** for `min_lot_dollars` — the project has already identified the future condition under which this assumption would break, but no code enforces or checks it (it is a documented future manual review, not an automated one). **Silent** for the other three — no equivalent documentation or check exists.

### 21. `regime_ticker` / regime status

- **Assumption:** Regime status is informational only and must never influence a buy/trim/block decision.
  - **Explicit?** Explicit — both in code structure (confirmed directly: `plan()` accepts `regime_ok` as a parameter but never branches on it anywhere in its body) and in documentation (`regime_gate.py`'s docstring cites the regime-gate backtest's 2.56pp/yr NO-GO finding as the reason).
  - **Violation handling:** **Prevented-by-design** — there is no code path by which a wrong or missing regime read could alter an allocation outcome; the only possible failure is a mislabeled display line.

### 22. Hardcoded operational constants

- **Assumption:** `DAYS_BACK=420`/`DAILY_LIMIT=320` supply enough history for every roster ticker's 200-SMA, including newly-listed ones.
  - **Explicit?** Implicit — no comment ties these specific numbers to "must cover 200 trading days plus buffer," though the value (420 calendar days ≈ 288 trading days) is evidently sized with that in mind.
  - **Violation handling:** **Tolerated** — a ticker with insufficient history simply gets `None` for `sma200`/`rsi14` (per item 24's graceful-degradation behavior) rather than a wrong number; this is visible in output as "n/a" but is not a distinct warning naming *why* (no message says "this ticker doesn't have enough history yet" versus any other reason a value might be `None`).

---

## Market data (runtime, external)

### 23. Daily price bars

- **Assumption:** The Alpaca IEX feed's most recent bar reflects a current, tradeable price at the moment the report is read.
  - **Explicit?** Explicit as documentation (`CLAUDE.md`'s "Live-priced book" guardrail states directly that the feed is frozen outside the 9:30am–4:00pm ET regular session); implicit at runtime — no code in `allocate.py` checks market-open status or bar recency before using a price.
  - **Violation handling:** **Silent at runtime** — a report run pre-market or after-hours uses the same code path as one run mid-session, with no in-tool flag distinguishing "this price may be stale by up to several hours." The knowledge that this can happen exists in `CLAUDE.md`, not in the running code.

### 24. Derived indicators

- **Assumption:** The bars array is chronologically ordered and free of erroneous individual values (a bad print, a bad split adjustment, etc.).
  - **Explicit?** Implicit — `sma()`/`rsi()`/`atr()` validate *quantity* of bars (returning `None` if too few) but not *quality* of any individual bar's value.
  - **Violation handling:** **Prevented** for insufficient quantity (graceful `None`, not a crash or a wrong number). **Silent** for a bad individual bar value that doesn't reduce the count below the required minimum — it would simply be averaged/smoothed in like any other data point.

### 25. Regime status

- Same assumption and classification as item 21 (explicit, prevented-by-design).

### 26. Next-earnings-date

- **Assumption A:** When yfinance cannot determine a date, treating the ticker as "unknown" (not "safe to buy") is the correct default.
  - **Explicit?** Explicit — the module's own docstring states this directly ("we return None and the caller reports the ticker as 'earnings: unavailable' rather than silently treating it as safe").
  - **Violation handling:** **Detected** — the `earnings:unavailable` flag is visible on the ticker's row.
- **Assumption B:** When yfinance *does* return a date, that date is correct.
  - **Explicit?** Implicit — no cross-check against a second source.
  - **Violation handling:** **Silent** — a wrong-but-present earnings date would gate (or fail to gate) a buy with no indication anything might be off, and `CLAUDE.md`'s Guardrails section already separately documents that the primary data source is not always reachable in this environment, meaning the *weaker* fallback source may be silently in use more often than intended — itself an instance of this same assumption being violated in a way the running code cannot detect.

### 27. Crypto prices

- Same structure as item 2 — routing assumption (item 3) plus a fetch-success assumption, both already covered above.

---

## Runtime-derived values

### 28. `book`

- **Assumption:** `gross`, `margin_debt`, and `cash` are each individually correct at computation time.
  - **Explicit?** Implicit — `book` is a pure aggregation with no independent sanity check of its own (e.g., no plausibility bound against a prior run's book value).
  - **Violation handling:** **Silent** — this is the point of maximum error amplification in the system (as already noted in the inventory): every upstream Silent violation (items 5, 9, 12A/C, 17/18, 20) compounds here with no additional check and no additional visibility.

### 29. `gross`, `net_equity`, `leverage_current`

- Same aggregation-level assumption and classification as item 28.

### 30. `target_dollars`, `gap`

- **Assumption:** `book` and `weight_pct` are each correct; this is purely compositional.
  - **Explicit?** N/A — no assumption of its own beyond composition of already-covered inputs.
  - **Violation handling:** Inherits its upstream inputs' classifications; adds none of its own.

### 31. `cluster_value`

- Same as item 30, composed from item 10's assumption.

### 32. `concentration_score`, `concentration_source`

- **Assumption:** Portfolio concentration risk is adequately represented by cluster-cap proximity alone, without T1/T2 single-name proximity.
  - **Explicit?** Explicit — the code comment states directly this is "deferred, not a placeholder" (allocate.py:919-920), i.e., a conscious, acknowledged scope limitation, not an unnoticed gap.
  - **Violation handling:** **Prevented-by-design**, in the sense that the *scope* is intentional and documented; the *consequence* (a T1/T2 concentration state that the separate mechanical trim (item 11) is actively correcting for could still show as `concentration_score = 0` if no cluster cap happens to be under simultaneous pressure) is not itself flagged anywhere as a known blind spot in the displayed score.

### 33. Margin risk state

- **Assumption:** This classification must never be capable of influencing an allocation decision — descriptive only.
  - **Explicit?** Explicit — enforced structurally by call order (`plan()` at allocate.py:910, `classify_margin_state()` at allocate.py:932 — strictly after) and by `margin_state.py`'s own module docstring ("a risk-governance calculator, not a decision-maker").
  - **Violation handling:** **Prevented-by-design** — there is no code path by which this classification could feed back into `plan()`'s own logic, since `plan()` has already returned by the time it's computed.

---

## Configuration

### 34. CLI arguments

- **Assumption:** Values typed at the command line are sane (no negative cash/margin request, no absurd magnitude).
  - **Explicit?** Implicit — `argparse`'s `type=float` is the only check found; no `min`/bounds validation.
  - **Violation handling:** **Silent** for magnitude/sign; a bad value flows directly into `plan()`'s `cash`/`margin_requested` parameters.

### 35. `performance_log.csv`

- **Assumption:** Net-equity changes between snapshots partly reflect market performance and partly reflect deposits/withdrawals/margin activity, and a reader needs to distinguish the two manually.
  - **Explicit?** Explicit — `render_performance()` states this directly and prominently in its own output text every time it's rendered (allocate.py:822-826): "a big deposit between snapshots will show up as 'growth' that has nothing to do with market performance."
  - **Violation handling:** **Detected**, in the sense that the ambiguity itself is disclosed every time the log is displayed — but the underlying deposit/withdrawal/margin-activity contamination in any given number is never itself separated out; the code discloses the limitation without resolving it.

---

## What this document deliberately does not do

- Does not recommend adding validation, a sanity check, or a warning anywhere.
- Does not propose extending `update-shares`/`update-crypto-shares` to match `update-holdings`'s book-swing check, even where the asymmetry is directly identified.
- Does not propose populating `margin.states`/`concentration_adjustment`, even though their absence is documented here as a specific, confirmed configuration state.
- Does not rank these invariants by importance or risk.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or any other production file.
- Does not infer any assumption beyond what the code's actual behavior, when traced, demonstrates — every "Implicit" classification above reflects an absence of any check found by direct reading, not a guess about intent.

Stopping here. Per the charter's own filter — "does this improve the accuracy of an existing input, or does it introduce a new judgment" — deciding whether any of the Silent/Tolerated items above warrant a validation (which would need to itself pass that same filter, e.g. a duplicate-ticker check verifies an existing invariant rather than adding judgment) is a separate, future decision, not made or proposed here.
