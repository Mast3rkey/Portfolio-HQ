# Portfolio Input Inventory

> **⚠️ Documentation only — no code, no production changes, no recommendations.** Per `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md` (frozen, not modified by this document). This is a factual trace of every input the current allocator (`allocate.py`) consumes, from origin to output. It does not recommend improvements, rank priorities, propose new inputs, create a backlog, or infer any relationship not directly observable in the code. Every claim below is traced to a specific file/function, read directly for this inventory on 2026-07-17.

_Written 2026-07-17. Sources read in full for this inventory: `allocate.py`, `alpaca_client.py`, `indicators.py`, `regime_gate.py`, `earnings.py`, `crypto.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`. `levels.py` and `performance_log.csv` are noted as downstream/adjacent consumers where relevant but were not traced with the same exhaustiveness as the core `plan()`/`render()` path._

## How to read each entry

Every input lists, in order: **Trace** (Origin → Storage → Consumption → Output, the required chain — any link not directly verifiable from the code is marked `Unknown`), then the nine required fields (name is the heading; origin, source file(s), factual status, maintenance type, downstream consumers, verification method, failure mode, confidence follow as labeled fields).

**Status** is one of: Known (directly observed value/mechanism) / Generated (computed by this codebase from other inputs) / Estimated (a labeled approximation, per this project's existing Known/Estimated/Hypothetical convention) / Unknown (cannot be determined from the codebase alone).

**Maintenance type** is one of: manually maintained / imported (live external fetch) / derived (computed from other stored inputs) / runtime-computed (computed fresh every run, never stored).

---

## Universe membership

### 1. Roster ticker list (all tiers combined)

**Trace:** Origin: pasted manually into `targets.yaml`'s `tiers.*.tickers` lists → Storage: `targets.yaml` (git-tracked, plain text) → Consumption: `build_roster()` (allocate.py:55) constructs `{ticker: {tier, weight_pct, fixed, cap_multiple}}`, consumed by `fetch_market()` (which symbols to pull) and `plan()` (every gap/target computation) → Output: every BUY/TRIM/BLOCKED row in `render()`'s table, and `run_levels()`'s rung report.

- **Origin:** Account holder, manual paste into `targets.yaml`.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `build_roster()`, `fetch_market()`, `plan()`, `render()`, `levels.py`'s `run_levels()`.
- **Verification method:** None automated found. No test or runtime check confirms roster tickers are valid, tradeable, or correctly classified.
- **Failure mode if incorrect:** A misspelled/delisted ticker produces a BLOCKED "no-data" row rather than an error (caught in `fetch_market()`'s per-symbol try/except). A ticker placed in the wrong tier receives the wrong target weight with no detection anywhere in the code.
- **Confidence:** High that the mechanism works this way (directly read); Unknown whether the current roster's membership is itself accurate — out of scope for this inventory to judge.

---

## Sleeve assignments

### 2. Crypto sleeve coin list

**Trace:** Origin: manually set `targets.yaml`'s `crypto.coins` → Storage: `targets.yaml` → Consumption: `main()`'s `fetch_crypto()` call (allocate.py:904), `plan()`'s sleeve-gap math (allocate.py:325-337) → Output: `render()`'s crypto sleeve table.

- **Origin:** Account holder, manual edit of `targets.yaml`.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `main()`, `plan()`, `render()`.
- **Verification method:** None automated.
- **Failure mode if incorrect:** A coin listed here with no `coingecko_ids` entry and no Alpaca coverage returns `price: None` (per `fetch_crypto()`'s fallback path), silently showing "n/a" and excluding it from `sleeve_val` — understates the sleeve without any error being raised.
- **Confidence:** High.

### 3. `coingecko_ids` mapping

**Trace:** Origin: manually set `targets.yaml`'s `crypto.coingecko_ids` (currently `{}`) → Storage: `targets.yaml` → Consumption: `fetch_crypto()`'s routing logic (crypto.py:67) → Output: which price source (`"alpaca"` vs `"coingecko"`) each coin's row shows in `render()`.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `fetch_crypto()`.
- **Verification method:** None.
- **Failure mode if incorrect:** A coin needing CoinGecko routing but missing from this map is routed to Alpaca instead, which likely doesn't carry it — silently returns no price rather than an error.
- **Confidence:** High.

---

## Tier assignments

### 4. Per-ticker tier membership (T1/T2/ETF/band/spec)

**Trace:** Origin: which `tiers.<name>.tickers` list a ticker appears in, `targets.yaml` → Storage: `targets.yaml` → Consumption: `build_roster()`'s loop (allocate.py:58-66) assigns `tier` per ticker; `plan()` branches on `meta["tier"]` for trim/cap logic → Output: which trim rule (band 1.25x, spec fixed, T1/T2 1.5x ceiling) applies to that ticker.

- **Origin:** Account holder, manual placement in one of five `targets.yaml` tier lists.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `build_roster()`, `plan()`.
- **Verification method:** None automated. No check that a ticker appears in only one tier list.
- **Failure mode if incorrect:** `build_roster()`'s dict construction (allocate.py:63, `roster[t.upper()] = {...}`) means a ticker listed in two tiers silently takes whichever tier is processed last, per Python dict-key-overwrite semantics applied to YAML key order (T1, T2, ETF, band, spec as written in the file) — this was traced directly from the loop's structure, not inferred.
- **Confidence:** High.

---

## Target weights

### 5. `weight_pct` per tier

**Trace:** Origin: `targets.yaml`'s `tiers.<name>.weight_pct` → Storage: `targets.yaml` → Consumption: `build_roster()` reads it into `roster[t]["weight_pct"]`; `plan()`'s `target_dollars = book * meta["weight_pct"] / 100.0` (allocate.py:197) → Output: every ticker's dollar target, and therefore every gap/BUY/TRIM decision.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `build_roster()`, `plan()`.
- **Verification method:** None automated.
- **Failure mode if incorrect:** Directly and silently mis-sizes every ticker in that tier's target.
- **Confidence:** High.

### 6. `cap_multiple` (band tier)

**Trace:** Origin: `targets.yaml`'s `tiers.band.cap_multiple` (1.25) → Storage: `targets.yaml` → Consumption: `plan()`'s band overweight-trim check (allocate.py:217) and buy-ceiling (`name_ceiling`, allocate.py:268) → Output: whether a band position over 1.25x target gets trimmed, and how high a band buy can run.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`.
- **Verification method:** None.
- **Failure mode if incorrect:** Silently changes when a band position is allowed to run above target vs. gets trimmed.
- **Confidence:** High.

### 7. `fixed` flag (spec tier)

**Trace:** Origin: `targets.yaml`'s `tiers.spec.fixed: true` → Storage: `targets.yaml` → Consumption: `plan()`'s spec-tier ceiling (`name_ceiling = target_dollars`, never above, allocate.py:266) and trim `cap_mult` logic (allocate.py:214-215) → Output: spec positions are never sized above their exact target.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`.
- **Verification method:** None.
- **Failure mode if incorrect:** If flipped to false, spec tickers would gain a `cap_multiple`-based ceiling instead of a hard fixed-at-target one.
- **Confidence:** High.

### 8. `crypto.sleeve_pct`

**Trace:** Origin: `targets.yaml` → Storage: `targets.yaml` → Consumption: `plan()`'s `sleeve_target = book * sleeve_pct / 100.0` (allocate.py:329) → Output: crypto sleeve gap sizing and `render()`'s ON TARGET/OVER/UNDER status line.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`, `render()`.
- **Verification method:** None.
- **Failure mode if incorrect:** Silently mis-sizes the sleeve's target and every displayed gap.
- **Confidence:** High.

---

## Cluster definitions

### 9. Cluster list, names, and `pct` caps (semis / power_infra / oil)

**Trace:** Origin: `targets.yaml`'s `caps.clusters` → Storage: `targets.yaml` → Consumption: `plan()`'s `clusters` list construction (allocate.py:174-176), cluster-value summation, cluster-cap block/trim logic (allocate.py:278-318, 344-357) → Output: cluster-cap BLOCKED rows and mechanical cluster-cap trims.

- **Origin:** Account holder, manual edit — `targets.yaml`'s own comments state each `pct` value derives from a one-time correlation scan and (for `oil`) a stress test performed in a prior session, documented in prose but not re-computed by any code in this repo.
- **Source file(s):** `targets.yaml`.
- **Status:** Known (the configured values); the correlation-scan rationale behind each value is Known only as documentation (`targets.yaml` comments, `CLAUDE.md`'s Decisions Log) — not independently re-verifiable from this codebase's own execution.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`.
- **Verification method:** None automated re-checks the correlation basis; the code only applies the configured `pct` mechanically.
- **Failure mode if incorrect:** An incorrect cap `pct` silently changes how much of the book that cluster can hold before a block/trim fires.
- **Confidence:** High on mechanism; Unknown (not re-verifiable here) whether the underlying correlation scan remains accurate today.

### 10. Cluster ticker membership

**Trace:** Origin: `targets.yaml`'s `caps.clusters[].tickers` → Storage: `targets.yaml` → Consumption: `plan()`'s `tk_clusters` lookup (allocate.py:208, computed independently of `roster`) → Output: which tickers' trims/blocks are attributed to which cluster.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`.
- **Verification method:** None — no check that a cluster's tickers are a subset of the roster tickers; `plan()` computes `tk_clusters` from the `clusters` list independently of `roster` membership (confirmed by reading both computations side by side).
- **Failure mode if incorrect:** A cluster's ticker list and that ticker's tier/roster membership are two independent lists with no cross-check between them anywhere in the code.
- **Confidence:** High.

---

## T1/T2 definitions

### 11. `gates.t1t2_trim_mult`

**Trace:** Origin: `targets.yaml`'s `gates.t1t2_trim_mult` (1.5) → Storage: `targets.yaml` → Consumption: `plan()`'s T1/T2 mechanical trim check, `overweight_limit = target_dollars * t1t2_trim_mult` (allocate.py:232) → Output: mechanical, no-RSI-gated trim of any T1/T2 name above 1.5x its own target.

- **Origin:** Account holder, manual edit — `targets.yaml`'s comment and `CLAUDE.md`'s Decisions Log both state this is a doctrine decision, not a backtest-optimized value.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`.
- **Verification method:** None automated.
- **Failure mode if incorrect:** Directly changes the trigger point for T1/T2 concentration trims.
- **Confidence:** High.

---

## Holdings

### 12. `shares` (ticker → qty)

**Trace:** Origin: real buy/sell/trim on Robinhood → account holder manually pastes via `update-shares` CLI command → Storage: `holdings.yaml`'s `shares:` block → Consumption: `resolve_holdings()` (allocate.py:100-140) live-values every entry (qty × latest Alpaca price) into the `holdings` dict → `plan()`'s every gap/target/trim/cluster computation → Output: every row in `render()`'s table, and every derived value downstream of `gross`/`book`.

- **Origin:** Account holder, manual paste, sourced from a real completed trade.
- **Source file(s):** `holdings.yaml` (stored); `allocate.py`'s `update_shares()` (write path); `resolve_holdings()` (read/live-value path).
- **Status:** Known as recorded — accuracy depends entirely on the account holder pasting correctly; not independently verified against a broker feed anywhere in this codebase.
- **Maintenance type:** Manually maintained (paste-triggered), merge by default (`replace` is opt-in).
- **Downstream consumers:** `resolve_holdings()`, `plan()`, `render()`, `log_performance()`.
- **Verification method:** `update_holdings()`'s `BOOK_CHANGE_WARN_PCT` (30%) sanity check exists — but this check is implemented only in `update_holdings()` (the manual-dollar-value path), **not** in `update_shares()` or `update_crypto_shares()`; confirmed by reading all three functions directly, no equivalent check exists in the latter two.
- **Failure mode if incorrect:** A mistyped share count directly and silently mis-values that position (and thus `gross`, `book`, every target, every gap) on every subsequent run until corrected; no automated check catches a share-count typo specifically.
- **Confidence:** High (mechanism directly observed); the specific gap (no book-swing check on `update-shares`) confirmed by direct code comparison, not inferred.

### 13. `crypto_shares` (coin → qty)

**Trace:** Origin: real crypto buy/sell → manually pasted via `update-crypto-shares` → Storage: `holdings.yaml`'s `crypto_shares:` block → Consumption: `resolve_holdings()` live-values via Alpaca/CoinGecko price → `plan()` → Output: `render()`'s crypto table and sleeve totals.

- **Origin:** Account holder, manual paste.
- **Source file(s):** `holdings.yaml`; `update_crypto_shares()`.
- **Status:** Known as recorded, same accuracy caveat as item 12.
- **Maintenance type:** Manually maintained, merge by default.
- **Downstream consumers:** `resolve_holdings()`, `plan()`, `render()`.
- **Verification method:** Same gap as item 12 — no book-swing sanity check in `update_crypto_shares()`.
- **Failure mode if incorrect:** Same as item 12, scoped to the crypto sleeve.
- **Confidence:** High.

### 14. `holdings` (ticker → manual dollar-value fallback)

**Trace:** Origin: manually pasted via `update-holdings`, used only for positions absent from `shares`/`crypto_shares` — currently `{}` (empty) in the `holdings.yaml` snapshot read for this inventory, meaning no ticker currently relies on this path → Storage: `holdings.yaml`'s `holdings:` block → Consumption: `resolve_holdings()` uses it as the base dict, overridden by any live-priced `shares`/`crypto_shares` entry → `plan()` → Output: `render()`.

- **Origin:** Account holder, manual paste.
- **Source file(s):** `holdings.yaml`; `update_holdings()`.
- **Status:** Known as recorded, when non-empty.
- **Maintenance type:** Manually maintained, merge by default; **does** have the `BOOK_CHANGE_WARN_PCT` sanity check (unlike items 12/13).
- **Downstream consumers:** `resolve_holdings()`, `plan()`, `render()`.
- **Verification method:** `BOOK_CHANGE_WARN_PCT` (30%) check, present in `update_holdings()` specifically.
- **Failure mode if incorrect:** A stale manual value for a position that should have moved to `shares` tracking would silently freeze that position's value at whatever was last pasted.
- **Confidence:** High.

### 15. Margin block: `debt`, `buffer_pct`, `synced_at`

**Trace:** Origin: account holder reads a Robinhood screen → manually types via `update-margin <debt> <buffer_pct>` → Storage: `holdings.yaml`'s `margin:` block → Consumption: `main()` reads `margin_debt`/`margin_buffer_pct` (allocate.py:886-888) → `plan()`'s `margin_capacity()` → `classify_margin_state()` → Output: every margin-gating decision (`forced_delever`, `margin_allowed`) and `render()`'s Margin section.

- **Origin:** Account holder, manual read of a live Robinhood screen, then manual CLI entry.
- **Source file(s):** `holdings.yaml`; `update_margin()`.
- **Status:** `debt`/`buffer_pct` Known as recorded (accuracy depends on correct reading + prompt syncing); `buffer_pct` specifically documented in `holdings.yaml`'s own header comment as **not independently derivable** by this codebase — must be Robinhood's own displayed value, confirmed by that comment to diverge from a simple `(portfolio value − maintenance requirement) / portfolio value` calculation when checked against real screens.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `main()`, `plan()`'s `margin_capacity()`, `classify_margin_state()`, `render()`.
- **Verification method:** `render()` computes `age_days` from `synced_at` and warns if `>= STALE_MARGIN_DAYS` (2 days, allocate.py:528) — the one explicit staleness check found in this codebase for any input.
- **Failure mode if incorrect:** Stale or mistyped debt/buffer directly changes every margin-gating decision and the displayed risk state; the staleness warning is date-based only — it cannot detect a *wrong* value typed the same day it was synced.
- **Confidence:** High.

### 16. Orphan positions (held, not in roster)

**Trace:** Origin: derived — any key present in the resolved `holdings` dict not present in `roster` or `crypto_coins` → Storage: not stored, computed fresh every run → Consumption: `plan()`'s `orphans` computation (allocate.py:375-376) → Output: `render()`'s "Held, not in roster" warning line.

- **Origin:** N/A — a derived fact, not a direct input.
- **Source file(s):** Computed in `plan()`, from `holdings.yaml` + `targets.yaml` together.
- **Status:** Generated.
- **Maintenance type:** Runtime-computed, not stored anywhere.
- **Downstream consumers:** `render()`'s warning line only.
- **Verification method:** None beyond the display warning itself.
- **Failure mode if incorrect:** An orphan position counts toward `gross`/`book` (and therefore every other ticker's target sizing) but has no target of its own and is never a trim/buy candidate — silently permanent unless the roster is edited or the position sold, confirmed directly from `plan()`'s logic (orphans are excluded from the `roster.items()` loop that produces buy/trim candidates).
- **Confidence:** High.

---

## Margin inputs (doctrine-level constraints, distinct from the live-synced values above)

### 17. `margin.leverage_cap`

**Trace:** Origin: `targets.yaml`, doctrine-fixed per `CLAUDE.md` → Storage: `targets.yaml` → Consumption: `plan()`'s `margin_capacity()`, `classify_margin_state()` → Output: the hard ceiling on every margin-funded buy this cycle.

- **Origin:** Account holder / doctrine decision, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained (doctrine-fixed, not backtest-tuned per `CLAUDE.md`'s Decisions Log).
- **Downstream consumers:** `margin_capacity()`, `classify_margin_state()`.
- **Verification method:** None automated.
- **Failure mode if incorrect:** Silently changes every margin-buy ceiling.
- **Confidence:** High.

### 18. `margin.buffer_floor_pct`

**Trace:** Same structure as item 17 → Consumption: `margin_capacity()`'s hard cutoff check (allocate.py:151-153) → Output: forced-delever block when the synced buffer is below this floor.

- **Origin:** Account holder / doctrine decision, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `margin_capacity()`, `classify_margin_state()`.
- **Verification method:** None automated.
- **Failure mode if incorrect:** Silently changes the forced-delever trigger point.
- **Confidence:** High.

### 19. `margin.states.{caution,restricted}` thresholds and `margin.concentration_adjustment`

**Trace:** Origin: intended to be `targets.yaml`'s `margin.states`/`margin.concentration_adjustment` blocks → Storage: **not currently present** — confirmed by direct read of `targets.yaml`'s full `margin:` block, which contains only `leverage_cap` and `buffer_floor_pct` → Consumption: `main()` reads `margin_cfg.get("states", {})` / `.get("concentration_adjustment", {})` (allocate.py:928-931), both resolve to empty dicts, so every threshold passed to `classify_margin_state()` is `None` (or `0.0` for the tightening coefficient) → Output: per `margin_state.py`'s own docstring, a `None` threshold means "this escalation path does not fire" — CAUTION and RESTRICTED are structurally unreachable states in the current configuration; only NORMAL and FORCED_DELEVER can currently be returned.

- **Origin:** Intended account-holder configuration; not yet set.
- **Source file(s):** `targets.yaml` (absent); `allocate.py` (the `.get(..., {})` fallback); `margin_state.py` (the None-means-inactive behavior).
- **Status:** **Unknown / not configured.**
- **Maintenance type:** N/A — not currently populated.
- **Downstream consumers:** `classify_margin_state()`.
- **Verification method:** N/A.
- **Failure mode if incorrect:** Not applicable in the "wrong value" sense — the current, factual state (confirmed by reading `targets.yaml` and `allocate.py` together, not inferred) is that CAUTION/RESTRICTED classification never fires at all today.
- **Confidence:** High that this is the current state.

---

## Constraints

### 20. `gates.min_lot_dollars`, `trend_rsi_override`, `earnings_blackout_days`, `trim_rsi`

**Trace:** Origin: `targets.yaml`'s `gates:` block → Storage: `targets.yaml` → Consumption: `plan()` (buy/trim minimum size; trend-gate RSI override; earnings blackout window; band/spec trim RSI threshold, respectively) → Output: BLOCKED/TRIM rows and threshold behavior throughout `plan()`.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `plan()`.
- **Verification method:** None automated.
- **Failure mode if incorrect:** Each directly and silently shifts its respective gate's trigger point.
- **Confidence:** High.

### 21. `regime_ticker`

**Trace:** Origin: `targets.yaml` (currently QQQ) → Storage: `targets.yaml` → Consumption: `fetch_market()` (which symbol's bars become the regime signal, allocate.py:76-97) → `render()`'s informational display line → Output: the "ABOVE/BELOW 200-EMA" text shown in every report.

- **Origin:** Account holder, manual edit.
- **Source file(s):** `targets.yaml`.
- **Status:** Known.
- **Maintenance type:** Manually maintained.
- **Downstream consumers:** `fetch_market()`, `render()`.
- **Verification method:** None.
- **Failure mode if incorrect:** Confirmed, per `regime_gate.py`'s own docstring and the regime-gate backtest's already-recorded NO-GO verdict, that regime status is informational only and never gates any buy/trim decision in `plan()` — an incorrect `regime_ticker` would only mislabel the display line, not change any allocation outcome. Directly verified by reading `plan()`'s signature: `regime_ok` is accepted as a parameter but never referenced anywhere in `plan()`'s body except being passed through unchanged into the returned result dict.
- **Confidence:** High.

### 22. Hardcoded operational constants (`DAILY_LIMIT=320`, `DAYS_BACK=420`, `STALE_MARGIN_DAYS=2`, `BOOK_CHANGE_WARN_PCT=30.0`)

**Trace:** Origin: hardcoded directly in `allocate.py`, not externalized to `targets.yaml` → Storage: source code only → Consumption: `fetch_market()` (bar-fetch window), `render()` (staleness warning), `update_holdings()` (book-swing check) → Output: how much price history is fetched, and two of this codebase's few built-in sanity checks.

- **Origin:** Written directly into `allocate.py` by whoever last edited it.
- **Source file(s):** `allocate.py`.
- **Status:** Known.
- **Maintenance type:** Manually maintained, but via a code edit rather than a config edit — distinct from every `targets.yaml`/`holdings.yaml` input above.
- **Downstream consumers:** `fetch_market()`, `render()`, `update_holdings()`.
- **Verification method:** None.
- **Failure mode if incorrect:** E.g. `DAYS_BACK=420` too short would starve a newly-listed ticker's 200-SMA of history before it has 200 real trading days. Noted for completeness of the trace even though these sit at the code/config boundary — they gate whether other factual inputs (SMA/RSI) can be computed at all.
- **Confidence:** High.

---

## Market data (runtime, external)

### 23. Daily price bars (OHLCV) per ticker

**Trace:** Origin: Alpaca's free IEX feed → Storage: not persisted, fetched fresh every run → Consumption: `AlpacaPaperClient.get_bars()` (alpaca_client.py:96-106) → `indicators.compute_all()` → `plan()` → Output: `price`, `sma200`, `sma50`, `rsi14`, `atr14` for every ticker, and every price-dependent gate/target/trim decision.

- **Origin:** Alpaca's IEX feed (paper-tier), a live external data source.
- **Source file(s):** `alpaca_client.py` (fetch), `fetch_market()` in `allocate.py` (orchestration).
- **Status:** Known as returned by the feed — but the feed itself is disclosed elsewhere in this project (`CLAUDE.md`'s "Live-priced book" guardrail) as reflecting only the regular 9:30am–4:00pm ET session, frozen outside those hours.
- **Maintenance type:** Imported (live API call every run).
- **Downstream consumers:** `indicators.compute_all()`, `plan()`.
- **Verification method:** `fetch_market()` catches fetch exceptions per-ticker and records an `"error"` string (allocate.py:81-83) rather than crashing; `plan()` surfaces this as a BLOCKED "no-data" row. No cross-check against a second data source anywhere in this codebase.
- **Failure mode if incorrect:** A bad/stale bar silently mis-computes every downstream indicator for that ticker; a fetch failure is caught and surfaced as BLOCKED rather than silently ignored.
- **Confidence:** High.

### 24. Derived indicators: `sma200`, `sma50`, `rsi14`, `atr14`, `price`

**Trace:** Origin: computed from item 23's bars → Storage: not stored, runtime-computed → Consumption: `indicators.py`'s `sma()`/`rsi()`/`atr()`/`last_price()` → `plan()` → Output: trend gate (`price`/`sma200`), trim RSI override, and (for `atr14`) `levels.py`'s rung staging.

- **Origin:** N/A — computed, not sourced.
- **Source file(s):** `indicators.py`.
- **Status:** Generated (known-formula, real-data-derived — Wilder's smoothing for RSI/ATR, per the module's own docstring).
- **Maintenance type:** Runtime-computed, not stored.
- **Downstream consumers:** `plan()` (price/sma200 for the trend gate; rsi14 for trim/override logic); `levels.py` (atr14, not consumed by `plan()` itself — confirmed by grep: `atr14` does not appear in `plan()`'s body).
- **Verification method:** `sma()`/`rsi()`/`atr()` each return `None` if insufficient bars exist (indicators.py:20-21, 27-28, 41), rather than computing a misleading number from a too-short window — the one built-in data-sufficiency check in this file.
- **Failure mode if incorrect:** Insufficient history (e.g. a newly-listed ticker) returns `None`, handled by `plan()`/`render()` as "n/a"/gate-skipped rather than crashing or defaulting to a guessed value.
- **Confidence:** High.

### 25. Regime status (QQQ above/below 200-EMA)

**Trace:** Origin: computed from the regime ticker's bars (item 23, filtered to `regime_ticker`) → Storage: not stored → Consumption: `regime_gate.regime_ok_from_closes()` (called inside `fetch_market()`) → Output: `render()`'s informational display line only.

- **Origin:** N/A — computed.
- **Source file(s):** `regime_gate.py`.
- **Status:** Generated.
- **Maintenance type:** Runtime-computed.
- **Downstream consumers:** `render()`'s regime line only — confirmed **not** consumed by any buy/trim/block decision in `plan()` (see item 21's failure-mode note; verified directly from `plan()`'s signature and body).
- **Verification method:** `regime_known` flag (requires >= 2 closes) prevents a false regime read from too little history.
- **Failure mode if incorrect:** Only the display line would be wrong — no allocation decision is affected, per the code's own structure. This is one of the few inputs this inventory can state, with direct code confirmation, has zero allocation impact if wrong.
- **Confidence:** High.

### 26. Next-earnings-date per ticker

**Trace:** Origin: yfinance (Yahoo Finance data, via `curl_cffi`) → Storage: per-process module-level cache only (`earnings.py`'s `_CACHE` dict, cleared on every fresh run) → Consumption: `days_until_earnings()` → `plan()`'s earnings-blackout gate → Output: BLOCKED "earnings in Nd" rows, or an `"earnings:unavailable"` flag on the ticker's base row.

- **Origin:** yfinance, a live external data source distinct from Alpaca.
- **Source file(s):** `earnings.py`.
- **Status:** Known when a date is returned; explicitly labeled `"earnings:unavailable"` when yfinance returns nothing — never silently treated as safe, per the module's own docstring.
- **Maintenance type:** Imported (live API call, cached per-process run only).
- **Downstream consumers:** `plan()`'s earnings-blackout gate.
- **Verification method:** None beyond the availability flag. `CLAUDE.md`'s Guardrails section documents two specific, already-identified, still-open data-quality issues in this exact input: a network-policy gap causing the weaker `calendar` fallback to be used more often than the primary `get_earnings_dates` source intended, and a since-fixed `BRK.B`→`BRK-B` symbol-mapping issue (fixed in `earnings.py`'s `_YAHOO_SYMBOL` map, confirmed present at line 20).
- **Failure mode if incorrect:** A ticker with unavailable earnings data still becomes a buy candidate — the blackout gate simply cannot fire for it. This is a known, documented, currently-live gap (per `CLAUDE.md`), not a hypothetical one.
- **Confidence:** High on mechanism; Unknown (not re-verifiable from this codebase alone) how often the weaker fallback is actually being used right now — `CLAUDE.md` names this as open, this inventory does not re-verify it.

### 27. Crypto prices

**Trace:** Origin: Alpaca crypto latest-trade endpoint (majors) or CoinGecko simple-price endpoint (coins in `coingecko_ids`) → Storage: not stored → Consumption: `fetch_crypto()` → `resolve_holdings()` (crypto position valuation) → `plan()`'s sleeve math → Output: `render()`'s crypto table and sleeve status.

- **Origin:** Two live external sources, routed per-coin by item 3's mapping.
- **Source file(s):** `crypto.py`.
- **Status:** Known when returned; explicit `error` string when not.
- **Maintenance type:** Imported (live API call every run).
- **Downstream consumers:** `resolve_holdings()`, `plan()`, `render()`.
- **Verification method:** Every failure path returns `price: None` plus an error string rather than crashing or defaulting; no cross-source verification between Alpaca and CoinGecko for any coin.
- **Failure mode if incorrect:** A failed price fetch drops that coin's value out of `sleeve_val` entirely (via `resolve_holdings()`'s `{t: v for t, v in result.items() if v}` filter, allocate.py:140) — silently understates the sleeve, potentially making it look more underweight than it is.
- **Confidence:** High.

---

## Runtime-derived values

### 28. `book` (= net_equity + cash)

**Trace:** Origin: computed in `plan()` from `gross`, `margin_debt`, and `cash` → Storage: not stored, runtime-computed every call → Consumption: every ticker's `target_dollars`, every cluster cap, the crypto sleeve target → Output: the single most-consumed derived value in the system.

- **Origin:** N/A — computed.
- **Source file(s):** `plan()` in `allocate.py` (allocate.py:184).
- **Status:** Generated.
- **Maintenance type:** Runtime-computed.
- **Downstream consumers:** Every target-dollar computation, cluster caps, sleeve target.
- **Verification method:** None beyond its inputs' own checks.
- **Failure mode if incorrect:** Every error in `gross`, `margin_debt`, or `cash` propagates multiplicatively through `book` into every single ticker's target — the point of maximum error amplification in the whole system.
- **Confidence:** High.

### 29. `gross`, `net_equity`, `leverage_current`

**Trace:** Origin: computed in `plan()` from `holdings` (item 12-14) + `margin_debt` (item 15) → Storage: not stored → Consumption: `margin_capacity()`, `classify_margin_state()`, `render()`'s Margin section → Output: leverage/buffer gating decisions and the displayed leverage ratio.

- **Origin:** N/A — computed.
- **Source file(s):** `plan()` (allocate.py:180-181, 377).
- **Status:** Generated.
- **Maintenance type:** Runtime-computed.
- **Downstream consumers:** `margin_capacity()`, `classify_margin_state()`, `render()`.
- **Verification method:** None beyond upstream input checks.
- **Failure mode if incorrect:** Errors in `holdings` or `margin_debt` propagate directly into every margin decision.
- **Confidence:** High.

### 30. `target_dollars`, `gap` per ticker

**Trace:** Origin: computed in `plan()`'s per-ticker loop from `book` and `weight_pct` → Storage: not stored → Consumption: buy/trim/block decision for that ticker, sort order for greedy allocation (allocate.py:341) → Output: the BUY/TRIM/BLOCKED table row for that ticker.

- **Origin:** N/A — computed.
- **Source file(s):** `plan()` (allocate.py:197-199).
- **Status:** Generated.
- **Maintenance type:** Runtime-computed.
- **Downstream consumers:** The full per-ticker decision logic in `plan()`.
- **Verification method:** None.
- **Failure mode if incorrect:** Directly determines which tickers get bought/trimmed/blocked and in what order.
- **Confidence:** High.

### 31. `cluster_value` per cluster

**Trace:** Origin: computed in `plan()`, summed from `holdings` over each cluster's ticker list (item 10) → Storage: not stored → Consumption: cluster-cap block/trim logic → Output: cluster-cap BLOCKED rows and mechanical cluster trims.

- **Origin:** N/A — computed.
- **Source file(s):** `plan()` (allocate.py:187-188).
- **Status:** Generated.
- **Maintenance type:** Runtime-computed.
- **Downstream consumers:** `plan()`'s cluster-cap logic.
- **Verification method:** None.
- **Failure mode if incorrect:** Directly changes whether a cluster is judged over/under its cap.
- **Confidence:** High.

### 32. `concentration_score`, `concentration_source`

**Trace:** Origin: `margin_state.concentration_risk_score()`, computed in `main()` from `cluster_proximities` (itself computed from `plan()`'s `clusters` output, allocate.py:921-925) → Storage: not stored → Consumption: `classify_margin_state()` → Output: the "tightest concentration pressure" line in `render()`'s Margin section.

- **Origin:** N/A — computed.
- **Source file(s):** `margin_state.py` (function), `allocate.py`'s `main()` (call site).
- **Status:** Generated.
- **Maintenance type:** Runtime-computed.
- **Downstream consumers:** `classify_margin_state()`.
- **Verification method:** `concentration_risk_score()` returns `(0.0, None)` for empty input rather than erroring.
- **Failure mode if incorrect:** `main()`'s own comment (allocate.py:919-920) states T1/T2 proximity ratios are **not currently included** in this score — only cluster-cap proximities are — described in the comment as "deferred, not a placeholder." This means concentration pressure from a T1/T2 single-name overweight is not reflected in `concentration_score`, even though the separate T1/T2 ceiling trim mechanism (item 11) exists elsewhere in `plan()`. Quoted directly from the code's own comment, not inferred.
- **Confidence:** High.

### 33. Margin risk state (`NORMAL`/`CAUTION`/`RESTRICTED`/`FORCED_DELEVER`)

**Trace:** Origin: `margin_state.classify_margin_state()`, called in `main()` (allocate.py:932) → Storage: not stored → Consumption: `render()`'s Margin section display → Output: the "Margin risk state: X" line and its reasons/allowed-actions list.

- **Origin:** N/A — computed.
- **Source file(s):** `margin_state.py`.
- **Status:** Generated.
- **Maintenance type:** Runtime-computed, pure function of the inputs above.
- **Downstream consumers:** `render()` only — confirmed, per `margin_state.py`'s own module docstring, this classification is descriptive and cannot itself influence `plan()`'s allocation decisions, since it is computed strictly after `plan()` returns (allocate.py's `main()` calls `plan()` at line 910, then `classify_margin_state()` at line 932 — the ordering itself confirms this).
- **Verification method:** `MarginStateResult.__post_init__` validates `current_state` is one of the four defined states and `allowed_actions` contains only pre-approved action strings (margin_state.py:78-84) — structural validation, not a data-accuracy check.
- **Failure mode if incorrect:** Any error in `gross`/`margin_debt`/`buffer_pct`/`concentration_score` propagates into a wrong displayed risk state, but per the above, never into a wrong allocation decision.
- **Confidence:** High.

---

## Configuration

### 34. CLI arguments (`--cash`, `--margin`, `--review`, `--levels`, `--ticker`, `--performance`)

**Trace:** Origin: typed by the account holder at the command line, per invocation → Storage: not persisted (process-lifetime only) → Consumption: `main()`'s `argparse` block (allocate.py:854-864) → `plan()`'s `cash`/`margin_requested` arguments → Output: deployable buying power for that single run.

- **Origin:** Account holder, per-run manual entry.
- **Source file(s):** `allocate.py`'s `main()`.
- **Status:** Known as typed.
- **Maintenance type:** Manually supplied every invocation.
- **Downstream consumers:** `main()`, `plan()`.
- **Verification method:** `argparse`'s own `float` type coercion is the only check; no bounds check found (e.g. nothing stops `--cash -500`).
- **Failure mode if incorrect:** A typo'd amount directly changes deployable buying power for that run only — not persisted, so a bad run doesn't corrupt any stored state.
- **Confidence:** High.

### 35. `performance_log.csv` (historical net-equity/QQQ/VOO snapshots)

**Trace:** Origin: auto-appended by `log_performance()` after every `allocate.py` run and every `update-*` sync (allocate.py:712, 965) → Storage: `performance_log.csv` → Consumption: `render_performance()` → Output: the trend table shown by `--performance`.

- **Origin:** Not a direct account-holder input — auto-generated from already-resolved `holdings`/`margin_debt`/QQQ/VOO prices at the time of each run.
- **Source file(s):** `performance_log.csv`; `log_performance()`/`render_performance()` in `allocate.py`.
- **Status:** Known as logged — explicitly caveated in `render_performance()`'s own output text as not deposit/withdrawal-adjusted.
- **Maintenance type:** Runtime-computed and auto-appended, not manually edited.
- **Downstream consumers:** `render_performance()`'s trend display only — confirmed not consumed by `plan()` at all (no reference to `PERF_LOG_FILE` or `_read_perf_log()` anywhere in `plan()`).
- **Verification method:** Same-day idempotency (`rows = [r for r in rows if r["date"] != today]` before appending, allocate.py:773) prevents duplicate same-day rows; no other check.
- **Failure mode if incorrect:** A logged value carries forward any upstream error (e.g. a stale margin sync) into the historical trend line, with no way to distinguish "the account really changed" from "an input was wrong that day."
- **Confidence:** High.

---

## What this document deliberately does not do

- Does not recommend any improvement to any input, mechanism, or verification method named above.
- Does not rank these 35 inputs by priority or importance.
- Does not propose any new input, field, or data source.
- Does not create a backlog.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or any other production file.
- Does not infer any relationship not directly traceable to a specific line or function in the code as read on 2026-07-17 — every "Unknown" or "not currently configured" finding above (items 19, part of 9, part of 26) is stated as a fact confirmed by direct reading, not a guess.

Stopping here. Awaiting direction on the next step of the Portfolio Data Workstream.
