# Portfolio Input Validation Assessment

> **⚠️ Assessment only — no implementation, no validation code, no backlog, no doctrine change.** Per `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`. This document evaluates, for every invariant documented in `docs/PORTFOLIO_INPUT_INVARIANTS.md`, whether future enforcement is warranted — it does not implement, authorize, rank, or schedule anything. `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`, `docs/PORTFOLIO_INPUT_INVENTORY.md`, and `docs/PORTFOLIO_INPUT_INVARIANTS.md` are frozen and unmodified by this document.

_Written 2026-07-17. Item numbers below correspond directly to `docs/PORTFOLIO_INPUT_INVENTORY.md`/`docs/PORTFOLIO_INPUT_INVARIANTS.md`'s 35-item numbering. Every claim below is tied to direct code inspection (re-confirmed this pass), an existing repository document, or an explicit Unknown/Insufficient-evidence classification — never to general software-engineering convention._

---

## 1. Executive Summary

Of the invariants assessed across the 35 inventoried inputs (several inputs carry more than one distinct invariant; 37 individual invariants were assessed from the inventory, plus 2 additional hypothetical extensions considered and rejected on this assessment's own initiative — see §3's "Out of scope items"):

| Classification | Count |
|---|---:|
| Potentially in scope | 14 |
| No enforcement warranted | 13 |
| Insufficient evidence | 10 |
| Out of scope (hypothetical extensions, not from the core 35) | 2 |

**This assessment identifies 14 candidates that could warrant a future, separately-approved enforcement proposal** — listed in full in §4. Every candidate verifies a narrow, already-documented factual invariant (uniqueness, numeric range, source-completeness, or freshness) and none introduces a score, ranking, prediction, or recommendation.

**No finding in this assessment requires a governance or doctrine review.** Every candidate in §4 operates strictly on data-entry/config-consistency facts already established as invariants in the frozen documents; none touches `targets.yaml`'s tier weights, cluster caps, margin doctrine (`leverage_cap`, `buffer_floor_pct`), or any allocation rule. Two items (the accuracy of `margin.leverage_cap`/`buffer_floor_pct` against this account's real brokerage agreement) sit adjacent to the already-closed Phase 5B/Phase 7A margin research line and are classified **Insufficient evidence** precisely because resolving them would require external broker data this codebase has never had — not because they raise a live doctrine question. This assessment does not reopen that closed research.

## 2. Assessment Method

**Governing test**, applied to every invariant: *does a proposed enforcement verify an existing factual input or invariant, or does it introduce a new judgment or decision-maker?* An enforcement that checks whether a stated fact holds (a ticker is unique, a percentage is non-negative, a synced value has an age) is **Potentially in scope**. An enforcement that would require this codebase to originate a new opinion about a security (attractiveness, conviction, likely direction) is **Out of scope**, regardless of how it's framed.

**Evidence standard:** every classification below cites either (a) a specific line/function re-read directly in `allocate.py`/`margin_state.py`/`targets.yaml`/`holdings.yaml` for this assessment, (b) a specific claim already recorded in `docs/PORTFOLIO_INPUT_INVENTORY.md` or `docs/PORTFOLIO_INPUT_INVARIANTS.md`, or (c) an explicit statement that the repository does not contain evidence either way. No classification rests on "this is generally good practice" — that standard is explicitly excluded per this assessment's instructions.

**Why silence alone is not proof enforcement is needed:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` recorded many invariants as **Silent** (no distinguishable signal on violation). Silence is a fact about current behavior, not a verdict on whether that behavior is wrong. Several Silent invariants below are classified **No enforcement warranted** because the underlying premise doesn't hold up under evidence (e.g., item 5's "weights should sum to something" has no supporting evidence — margin-funded allocation can exceed 100% of book by design) or because the missing check would require data this codebase doesn't have (**Insufficient evidence**), not because Silent automatically means "should be Detected."

**Why intentional architecture is not treated as a defect:** Several invariants — regime status never gating a decision, margin-state classification never influencing `plan()`, the absence of `margin.states` config, `concentration_risk_score()`'s cluster-only scope — were already documented in `docs/PORTFOLIO_INPUT_INVARIANTS.md` as **explicit, prevented-by-design** behaviors, each backed by a direct code-structure citation (call ordering, an unreferenced parameter, a module docstring's own stated design). These are re-confirmed, not re-litigated, below and classified **No enforcement warranted** — "enforcing" an architectural invariant that already cannot be violated by construction would add code with no behavior to guard against.

---

## 3. Full Invariant Assessment

Each entry: **Input** (inventory #) → **Invariant** → **Explicit/Implicit** → **Violation handling** (from the invariants doc) → **Plausible consequence** → **Enforcement would...** → **Classification** → **Evidence** → **Further evidence needed**.

### Universe membership

**1a. Roster ticker validity** — Invariant: every roster ticker resolves to real, fetchable data. *Implicit.* Handling: **Detected** (late — `fetch_market()`'s try/except, allocate.py:79-83, surfaces a BLOCKED "no-data" row). Consequence: a bad ticker never silently corrupts other computations; it is visibly blocked every run. Enforcement would: verify an existing fact (does this symbol resolve) — no allocation-behavior change, no doctrine change. **Classification: No enforcement warranted** — current behavior already detects and surfaces the violation every run; the gap is timing (post-hoc vs. at config-edit time), not absence of detection. Evidence: direct read of `fetch_market()`/`plan()`'s BLOCKED-row path. Further evidence needed: none to reach this classification; if timing were later judged material, that would be a fresh, separate assessment.

**1b/4. Ticker belongs to exactly one tier** — Invariant: no ticker appears in more than one `tiers.*.tickers` list. *Implicit.* Handling: **Silent** — `build_roster()`'s dict construction (allocate.py:63) lets a later tier overwrite an earlier one with no signal. Consequence: a duplicated ticker is silently sized/gated using only its last-processed tier's rules; the account holder has no way to discover this from any current output. Enforcement would: verify an existing, already-implicit structural invariant (uniqueness of tier membership); would not alter which tier "wins" today, would not add any judgment about which tier a ticker *should* be in, would not change allocation behavior for any config that doesn't already contain a duplicate. **Classification: Potentially in scope.** Evidence: direct trace of `build_roster()`'s loop and Python dict-overwrite semantics. Further evidence needed: none — the invariant and its current silent-violation path are both directly confirmed in code.

### Sleeve assignments

**2. Crypto coin has a resolvable price source** — Invariant: every `crypto.coins` entry has either Alpaca coverage or a `coingecko_ids` entry. *Implicit.* Handling: **Mixed** (per-coin row Detected via `n/a`; aggregate sleeve total Silent — the coin drops out of `sleeve_val` with no aggregate-level flag, per `resolve_holdings()`'s filter, allocate.py:140). Consequence: the crypto sleeve's displayed total can be silently understated with no warning that it's incomplete, distinct from the per-coin row which does show an error. Enforcement would: verify an existing configuration-completeness fact; no judgment about coin selection or crypto-market view. **Classification: Potentially in scope**, scoped narrowly to *flagging when the aggregate sleeve total is known-incomplete due to a missing price*, not to any coin-selection decision. Evidence: direct read of `resolve_holdings()` and `fetch_crypto()`. Further evidence needed: none for the classification itself.

**3. `coingecko_ids` completeness/correctness of routing** — Invariant: every coin actually requiring CoinGecko is present in the map. *Implicit.* Handling: **Silent** (mis-routed coin looks identical to an unrelated fetch failure). Consequence: a configuration error (missing map entry) is indistinguishable from a transient API outage in the current output. Enforcement would: verify a config-completeness fact only; introduces no new price judgment. **Classification: Potentially in scope**, scoped narrowly to distinguishing "no price source configured" from "price source configured but temporarily unavailable" in the error string shown, not to selecting or validating which coins should be tracked. Evidence: direct read of `fetch_crypto()`'s routing logic. Further evidence needed: none for the classification.

### Tier assignments

*(Item 4 assessed jointly with 1b above — same invariant, same classification.)*

### Target weights

**5a. `weight_pct` individually non-negative / plausible** — Invariant: each tier's `weight_pct` is a sane, non-negative percentage. *Implicit.* Handling: **Silent** (`float(tier.get("weight_pct", 0))`, allocate.py:59, accepts any float including negative). Consequence: a negative or absurd weight directly and silently mis-sizes every ticker in that tier. Enforcement would: verify a narrow numeric-range fact about a config value already entered by the account holder; would not decide what the *correct* weight is, only that a given value is within a sane range (e.g., non-negative). **Classification: Potentially in scope**, scoped strictly to a range check (e.g., non-negative), not to any judgment about what an appropriate weight *should* be.

**5b. Weights collectively "sum to something meaningful"** — Invariant: **no supporting evidence this invariant exists.** `CLAUDE.md`'s own record (the T1 42.1%-of-book-vs.-30.15%-target passage in its Decisions Log) confirms actual tier totals routinely diverge from any fixed sum, and margin-funded allocation is explicitly designed to let total targeted dollars exceed net-equity-based "100%" (per `CLAUDE.md`'s Portfolio Doctrine section on margin as fuel). **Classification: No enforcement warranted** — the premise that weights should sum to a fixed total is not supported by any evidence in this repository; there is no fact here to verify. Evidence: `CLAUDE.md`'s own Decisions Log entry and Portfolio Doctrine section, directly contradicting a fixed-sum assumption. Further evidence needed: none — the absence of a real invariant is itself the finding.

**6. `cap_multiple >= 1.0` (band tier)** — Invariant: a tier's overweight ceiling multiplier should not sit below 1.0 (a ceiling below the target it's supposed to cap is internally inconsistent). *Implicit.* Handling: **Tolerated** (`max(0.0, ...)` prevents a negative allocation but not the underlying inconsistency). Consequence: a misconfigured `cap_multiple < 1.0` would silently produce a ceiling below target with no warning the config itself is self-contradictory. Enforcement would: verify a narrow, self-referential numeric-consistency fact within the config file itself; no market judgment involved. **Classification: Potentially in scope.**

**7. `fixed`/`cap_multiple` intended consistency (spec tier)** — Invariant: a tier marked `fixed: true` is expected to also have `cap_multiple` unset or equal to 1.0 (currently coincidentally true, per direct read of `targets.yaml`'s `spec` block). *Explicit* (both fields are directly coded, but their expected relationship is nowhere stated). Handling: **Tolerated** (today's config happens to be consistent; nothing checks that it stays so). Consequence: if a future edit set `spec.cap_multiple` to something other than 1.0 without also reconsidering `fixed`, the two fields' independent meanings interact unpredictably against reader expectations. Enforcement would: verify a config self-consistency fact (does `cap_multiple` deviate from 1.0 on a `fixed: true` tier), not a market view. **Classification: Potentially in scope.**

**8. `sleeve_pct` sane numeric range** — Same structure as item 5a, scoped to `crypto.sleeve_pct`. **Classification: Potentially in scope**, range check only.

### Cluster definitions

**9. Cluster `pct` cap freshness/re-validation** — Invariant (implied): a cluster cap's `pct`, once set from a correlation scan, should be periodically re-validated against current correlation data. *This invariant is not established anywhere in the repository.* Unlike margin sync data, which has an explicit, coded staleness standard (`STALE_MARGIN_DAYS = 2`), no threshold, cadence, or re-scan trigger for cluster caps exists in any file read for this assessment. **Classification: Insufficient evidence.** Evidence: absence confirmed by direct search — no staleness constant, no `synced_at`-equivalent field, no re-scan schedule anywhere in `targets.yaml`, `allocate.py`, or any doctrine document tied to cluster caps specifically. Further evidence needed: a defined staleness policy (what interval, what re-scan trigger) would first have to be established as doctrine before any enforcement could target it — that policy does not currently exist to enforce.

**10. Cluster ticker ⊆ roster ticker consistency** — Invariant: every ticker in a cluster's list also appears in some tier's roster list. *Implicit.* Handling: **Silent** (`plan()` computes `tk_clusters` from the roster loop's own view of `clusters`, allocate.py:208; nothing checks the reverse direction). Consequence: a cluster ticker absent from every tier list would never be visited by the roster loop and would never be flagged as inconsistent with its own cluster's membership. Enforcement would: verify a purely structural cross-reference between two already-existing config lists; no market judgment. **Classification: Potentially in scope.**

### T1/T2 definitions

**11. `t1t2_trim_mult` uniform across T1/T2** — Invariant: the same multiplier applies to both tiers by design. *Explicit* — directly coded and directly documented in `CLAUDE.md`'s Decisions Log as a deliberate doctrine choice, not an oversight. **Classification: No enforcement warranted** — this is not a violation-prone invariant; it is a stated, intentional, single design choice with no "wrong" state to detect. Evidence: `CLAUDE.md` Decisions Log, quoted directly in `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 11.

### Holdings

**12a/13a. Share/coin count correctness** — Invariant: entered quantities match reality. *Implicit.* Handling: **Silent**/**Tolerated** (no independent source to check against). Consequence: a mistyped quantity mis-values that position with no automated way to detect it from within this codebase. Enforcement would require: an independent source of truth (a live brokerage feed, a trade-confirmation import) that does not exist anywhere in this repository. **Classification: Insufficient evidence.** Evidence: `docs/PORTFOLIO_INPUT_INVENTORY.md` items 12/13 confirm no broker-feed cross-check exists anywhere. Further evidence needed: a real, independently-sourced holdings/trade feed — none exists in this codebase today, and per `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md` (cited in the closed margin research program), this project has never had one.

**12b/13b. Book-swing sanity check parity (`shares`/`crypto_shares` vs. `holdings`)** — Invariant: a large, unexplained book-value swing from a data-entry paste usually indicates a partial-paste error, deserving the same abort-pending-confirmation treatment `update_holdings()` already applies. *Mixed* — explicit and enforced for `holdings` (item 14a); the identical assumption is implicit and unenforced for `shares`/`crypto_shares`, confirmed by direct side-by-side comparison of `update_holdings()` (has `BOOK_CHANGE_WARN_PCT`, allocate.py:602-613) against `update_shares()`/`update_crypto_shares()` (no equivalent check, allocate.py:622-659). Handling: **Silent** for `shares`/`crypto_shares` specifically. Consequence: a fat-fingered share-count paste writes through immediately with no abort/confirm step, unlike an equally large swing entered via `update-holdings`. Enforcement would: verify the *same already-established, already-implemented* fact-check pattern this codebase already applies to a sibling input — no new judgment, no new threshold invented (the 30% figure already exists and is already approved doctrine for this exact purpose in the sibling function). **Classification: Potentially in scope.** Evidence: direct line-by-line comparison of all three `update_*` functions.

**12c/13c. `qty >= 0`** — Invariant: share/coin counts should not be negative (no short position is modeled anywhere in this system). *Implicit.* Handling: **Tolerated** (a negative value flows through to a negative dollar value with no type error). Consequence: a negative quantity (e.g., a sign-flip typo) silently reduces `gross` unexpectedly. Enforcement would: verify a narrow numeric-sign fact about a data-entry field; no market judgment. **Classification: Potentially in scope.**

**14a. `holdings` manual-value book-swing guard** — Already implemented (`BOOK_CHANGE_WARN_PCT`, Detected). **Classification: No enforcement warranted** — the invariant this item names is already enforced; nothing further to assess.

**14b. `holdings` manual-value freshness** — Invariant: a manually-pasted dollar value should carry some indication of how current it is, the way `margin.synced_at` does. *Implicit* (no `synced_at`-equivalent exists for the `holdings` block, confirmed by direct read of `write_state()`, allocate.py:662-712, and `holdings.yaml`'s current schema). Handling: **Silent.** Consequence: a stale manual value (the kind SKHY historically needed, per `CLAUDE.md`'s Decisions Log) could persist indefinitely with zero staleness signal, unlike margin data's explicit 2-day warning. Enforcement would: verify a freshness fact using the *exact same mechanism* already built and approved for margin data — no new judgment, no new doctrine, a direct structural analog to an already-existing, already-approved check. **Classification: Potentially in scope.**

**15a. Margin sync staleness** — Already implemented (`STALE_MARGIN_DAYS`, Detected). **Classification: No enforcement warranted.**

**15b. Same-day margin value correctness** — Invariant: a freshly-synced debt/buffer figure is assumed correct with no independent check. *Implicit.* Handling: **Silent.** Enforcement would require: an independent, same-day source to cross-check against (e.g., a live Robinhood API integration), which does not exist in this codebase and is explicitly, permanently out of reach per `CLAUDE.md`'s "never derive buffer % from a formula, use only the displayed value" guardrail — meaning even a hypothetical enforcement couldn't compute an independent check, only fetch a second observation of the same manually-reported number. **Classification: Insufficient evidence.** Evidence: `holdings.yaml`'s own header comment and `CLAUDE.md`'s explicit prohibition on deriving buffer % independently. Further evidence needed: a live, read-only broker data feed for margin state — does not exist in this project (the existing Alpaca integration is a separate paper-trading account, not a feed for this account's real margin state, confirmed by `alpaca_client.py`'s PAPER_ONLY guard).

**16. Orphan-position warning escalation** — Invariant: an orphan position is already, unconditionally flagged every run (Detected). Whether that flag should escalate, repeat more prominently, or expire is not a factual-verification question — it's a display/UX design choice with no "correct" answer derivable from the code. **Classification: No enforcement warranted** — the underlying fact (orphan exists) is already detected every run; any further "enforcement" here would be a presentation decision, not a new fact-check.

### Margin inputs

**17. `margin.leverage_cap` matches this account's real brokerage terms** — Invariant: the configured 1.8x reflects reality. *Explicit as doctrine, implicit as an ongoing cross-check* (no cross-check exists). Enforcement would require: real, current brokerage-agreement data this codebase has no access to (the same category of gap `docs/PHASE7A_DATA_AVAILABILITY_ASSESSMENT.md` already catalogued for related broker-mechanics questions, in the now-closed margin research program). **Classification: Insufficient evidence.** This does not reopen the closed Phase 5B/7A research — it is recorded here only as a factual gap in *this workstream's* evidence, matching (not reversing) that program's own already-recorded conclusion.

**18. `margin.buffer_floor_pct` matches real terms** — Same structure and classification as item 17.

**19. Missing `margin.states`/`concentration_adjustment` config** — Already established as an **explicit, prevented-by-design architectural invariant**: `margin_state.py`'s own module docstring states directly that a `None` threshold means "this escalation path simply never fires," by design. This is one of the architectural invariants this assessment's own instructions name directly (an example: "intentionally unreachable margin states") and must not be reframed as a validation gap absent direct evidence the code violates its own documented design — no such evidence exists; the code behaves exactly as its docstring says. **Classification: No enforcement warranted.**

### Constraints

**20a. `min_lot_dollars` staleness relative to book size** — Invariant: this value should be revisited once the book crosses a documented size threshold. *Explicit* — `CLAUDE.md`'s Open Items section states the exact trigger directly: "revisit once the book crosses roughly $25,000." Handling: **Tolerated** (the future condition is named, but nothing in code checks the book's current size against it). Enforcement would: verify a single, already-fully-specified factual condition (current book size vs. a documented $25,000 threshold) explicitly named in an already-approved doctrine document — not a new judgment, not a new threshold invented by this workstream. **Classification: Potentially in scope.** Evidence: `CLAUDE.md`'s Open Items, quoted directly.

**20b. `trend_rsi_override`/`earnings_blackout_days`/`trim_rsi` staleness** — Invariant (implied): these thresholds also deserve periodic revisiting. *No equivalent explicit trigger is documented anywhere for these three*, unlike `min_lot_dollars`. **Classification: Insufficient evidence.** Further evidence needed: a documented condition (analogous to `min_lot_dollars`'s $25,000 trigger) under which any of these three should be reconsidered — none currently exists to enforce against.

**21/25. Regime status is informational-only, never gates a decision** — Already established as an explicit, prevented-by-design architectural invariant, directly confirmed by tracing `plan()`'s signature and body (it accepts `regime_ok` but never branches on it) and by `regime_gate.py`'s own docstring citing the regime-gate backtest's recorded NO-GO verdict. This is named directly in this assessment's own instructions as an example architectural invariant not to reframe. **Classification: No enforcement warranted.**

**22. `DAYS_BACK`/`DAILY_LIMIT` sufficiency for new listings** — Invariant: 420 calendar days supplies enough history for a 200-SMA on every roster ticker, including recently-listed ones. Distinguishing "insufficient history because the ticker is genuinely new" from "insufficient history because something is wrong with the data feed" would require an independent listing-date fact this codebase does not store or fetch anywhere (confirmed — no listing-date field exists in `targets.yaml`, `holdings.yaml`, or any fetched Alpaca response consumed by this code). **Classification: Insufficient evidence.** Further evidence needed: an independent per-ticker listing-date source — none exists in this codebase today.

### Market data

**23. Price-bar freshness relative to market-open status** — Invariant: a displayed price should be understood as potentially frozen outside the 9:30am–4:00pm ET regular session (already documented, `CLAUDE.md`'s "Live-priced book" guardrail), but no runtime signal in `allocate.py` itself currently distinguishes a mid-session read from a pre/post-market one. Handling: **Silent at runtime** (the knowledge exists in `CLAUDE.md`, not in the running code). Notably, `alpaca_client.py`'s `get_clock()` method (alpaca_client.py:87-88) already exists and already returns real, live market-open/closed status — confirmed by direct read — but is not called anywhere in `allocate.py`'s live workflow (only in `alpaca_client.py`'s own `__main__` diagnostic block). Enforcement would: verify an existing, already-fetchable external fact (is the market currently open) using a data source this codebase already has wired up but doesn't currently call from the report-generation path; no market judgment, no new data source. **Classification: Potentially in scope.**

**24. Bar quality beyond quantity** — Invariant: individual bar values (not just bar count) are correct. `sma()`/`rsi()`/`atr()` validate count (returning `None` if too few) but nothing validates that any individual bar's OHLCV values are plausible. Enforcement would require: a defined standard for "an implausible bar" (e.g., a price jump beyond some bound) — no such standard exists anywhere in this codebase, and inventing one risks encoding a market-behavior judgment (what counts as "too large a move to be real") rather than verifying a stored fact. **Classification: Insufficient evidence** — both because no existing standard exists to enforce, and because defining one risks drifting toward the judgment side of the governing test; a future assessment would need to establish, first, whether a purely mechanical data-quality check (e.g., cross-provider bar comparison) is even possible without embedding a market-behavior assumption.

**25.** *(assessed jointly with 21 above.)*

**26a. Earnings-unavailable flag** — Already implemented (Detected, explicit per `earnings.py`'s own docstring). **Classification: No enforcement warranted.**

**26b. Earnings-date correctness when present** — Invariant: a returned yfinance date is accurate. Enforcement would require: a second, independent earnings-calendar source to cross-check against — none exists in this codebase (only yfinance is integrated, per direct read of `earnings.py`'s imports). **Classification: Insufficient evidence.** Further evidence needed: a second earnings-data source; none currently integrated.

**27. Crypto price fetch-failure signaling** — Already Detected per-coin (error string shown). Aggregate-level signaling is the same invariant as item 2, already classified **Potentially in scope** there; not reassessed separately here to avoid double-counting the same underlying fact.

### Runtime-derived values

**28/29. `book`, `gross`, `net_equity`, `leverage_current` internal consistency** — These are pure, single-path compositions of already-assessed inputs (items 12-15, 17-18); no second, independent computation of any of these values exists anywhere in this codebase to reconcile against. Enforcement would require inventing a second computation path purely to check the first — not "verifying an existing fact" in the sense the governing test requires, since there is no existing second fact to compare to. **Classification: No enforcement warranted** for all four, distinct from the individual upstream inputs they're built from (which retain their own classifications above).

**30/31. `target_dollars`, `gap`, `cluster_value`** — Same reasoning as 28/29 — pure compositions with no independent check available. **Classification: No enforcement warranted.**

**32. `concentration_score`'s cluster-only scope (T1/T2 excluded)** — Already established as an explicit, intentional, documented scope limitation (the code's own comment: "deferred, not a placeholder," allocate.py:919-920) — named directly in this assessment's instructions as an example architectural invariant ("intentionally deferred T1/T2 concentration integration") not to reframe absent direct evidence of a design violation. No such evidence exists; the code matches its own stated scope exactly. **Classification: No enforcement warranted.**

**33. Margin-state classification never influences allocation** — Already established as explicit, prevented-by-design (call-order proof: `plan()` at allocate.py:910, `classify_margin_state()` strictly after at allocate.py:932; `margin_state.py`'s own docstring: "a risk-governance calculator, not a decision-maker"). Named directly in this assessment's instructions as an example architectural invariant not to reframe. **Classification: No enforcement warranted.**

### Configuration

**34. CLI argument numeric bounds (`--cash`, `--margin` non-negative)** — Invariant: these values represent real dollar amounts and shouldn't be negative. *Implicit* — `argparse`'s `type=float` performs no bounds check (confirmed, allocate.py:855-858). Enforcement would: verify a narrow numeric-sign fact about a per-run CLI input; no market judgment, no persisted-state risk (per-run only, not written to any file). **Classification: Potentially in scope.**

**35. `performance_log.csv` deposit/withdrawal contamination** — The ambiguity is already explicitly disclosed in `render_performance()`'s own output text every time it's shown (Detected, per the invariants document). Actually *resolving* the ambiguity (separating market-driven from deposit-driven equity change) would require capturing deposit-event data this codebase does not currently record anywhere — `log_performance()` stores only `net_equity`/`gross`/`margin_debt`/`qqq_price`/`voo_price`/`note` (confirmed, `PERF_FIELDS`, allocate.py:40) with no deposit-amount field. **Classification: Insufficient evidence.** Further evidence needed: a deposit-event log (amount and date of each deposit/withdrawal) — does not exist anywhere in this codebase today; this is closely related to, but distinct from, the still-open margin-research backlog item (`docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 5) covering margin/cashflow logging specifically.

### Out of scope items

No invariant assessed above required an **Out of scope** classification on its own terms — every invariant traced to a factual, non-judgment question, even where the answer was "insufficient evidence" or "no enforcement warranted." Two related, *hypothetical* extensions were considered and explicitly rejected as Out of scope rather than assessed as candidates, because they would cross the governing test's line even though they arise naturally from the invariants above:

- **A "data quality confidence" score per ticker** (a natural-sounding extension of items 23/24/26b's data-freshness/quality findings) — would require synthesizing multiple factual signals into a single number this codebase would then treat as meaningful, which is a judgment about how much to trust a given data point, not a verification of a single stated fact. **Out of scope.**
- **Automatic staleness-triggered exclusion of a ticker from buy candidacy** (a natural-sounding extension of item 23's market-clock finding) — would change `plan()`'s actual allocation output based on a *new* decision rule (exclude on staleness), not merely surface a fact; that is an allocation-behavior change requiring its own governance review under the charter's own decision boundaries, not a validation item. **Out of scope.**

These are recorded here as explicitly considered and rejected, not as candidates, per the instruction to explicitly distinguish operational-data invariants from anything crossing into judgment.

---

## 4. Candidate Set

Items classified **Potentially in scope**. Each states only the narrow factual invariant that could potentially be enforced — no implementation detail, no ranking, no effort estimate.

1. **Tier uniqueness** (items 1b/4) — a ticker should not appear in more than one tier's `tickers` list.
2. **Crypto sleeve price-source completeness** (item 2) — every `crypto.coins` entry should resolve to a price via Alpaca or `coingecko_ids`, and the aggregate sleeve total should be flagged when it's known-incomplete due to a missing price.
3. **`coingecko_ids` routing completeness** (item 3) — a coin's routing failure should be distinguishable from a transient fetch failure.
4. **`weight_pct` non-negativity** (item 5a) — tier weight percentages should be within a sane numeric range.
5. **`cap_multiple >= 1.0`** (item 6) — a tier's overweight ceiling multiplier should not be configured below 1.0.
6. **`fixed`/`cap_multiple` self-consistency** (item 7) — a `fixed: true` tier's `cap_multiple` deviating from 1.0 could be flagged as a config inconsistency.
7. **`sleeve_pct` sane numeric range** (item 8) — same structure as item 4, scoped to the crypto sleeve percentage.
8. **Cluster ticker ⊆ roster consistency** (item 10) — every ticker in a cluster's list should also appear in some tier's roster list.
9. **Share/coin-count book-swing guard parity** (items 12b/13b) — `update-shares`/`update-crypto-shares` could apply the same already-approved book-swing check `update-holdings` already applies.
10. **Share/coin quantity non-negativity** (items 12c/13c) — entered quantities should not be negative.
11. **`holdings` manual-value freshness signal** (item 14b) — a manually-pasted fallback value could carry the same kind of age/freshness signal `margin.synced_at` already provides.
12. **`min_lot_dollars` vs. the documented $25,000 book-size trigger** (item 20a) — the book's current size could be checked against the threshold `CLAUDE.md` already names explicitly.
13. **Market-open status at report-generation time** (item 23) — the already-available `get_clock()` fact could be surfaced alongside a price to indicate potential staleness.
14. **CLI argument non-negativity** (item 34) — `--cash`/`--margin` values could be checked for a sane (non-negative) sign.

---

## 5. Excluded Items

**No enforcement warranted (13 invariants):** items 1a (already detected, timing-only gap), 5b (no evidence the underlying premise — a fixed weight sum — exists at all), 11 (single intentional doctrine choice, no violation-prone state), 14a/15a (already implemented), 16 (already detected; further "enforcement" would be a presentation choice, not a fact-check), 19 (explicit, prevented-by-design architectural invariant — missing config is a documented, intentional "off" state), 21/25 (explicit, prevented-by-design architectural invariant — regime is structurally incapable of affecting allocation), 26a (already detected), 28/29/30/31 (pure derived compositions with no independent fact to check against), 32 (explicit, intentional, documented scope limitation), 33 (explicit, prevented-by-design architectural invariant — margin-state classification is structurally incapable of affecting allocation).

The largest cluster here — items 19, 21/25, 32, 33 — share a common shape worth naming explicitly: each is an *already-enforced* invariant, enforced not by a validation check but by the code's own structure (a docstring-documented `None`-means-off design, a parameter never referenced in a decision path, a call-order guarantee). Proposing to "enforce" these further would not close any gap, because none exists to close; doing so anyway would risk implying these designs are currently unsafe, which the direct code evidence contradicts.

No item was classified **Out of scope** among the 35 inventoried inputs' own invariants — the two Out-of-scope items recorded (§3, "Out of scope items") are hypothetical extensions this assessment considered and rejected on its own initiative, not items that arose from the invariants documents directly, included for completeness of the governing-test application.

## 6. Evidence Gaps

Items classified **Insufficient evidence**, with exactly what is missing:

- **Cluster cap freshness (item 9):** no defined staleness policy (interval, trigger) exists for cluster-cap values anywhere in this repository — one would need to be established as doctrine before any enforcement could target it.
- **Share/coin count correctness (items 12a/13a):** no independent source of truth (live broker feed, trade-confirmation import) exists to check entered quantities against.
- **Same-day margin-value correctness (item 15b):** no independent, same-day cross-check source exists, and `CLAUDE.md`'s own guardrail against deriving buffer % independently means even a hypothetical check couldn't compute a true independent verification, only re-observe the same manually-reported number.
- **`margin.leverage_cap`/`buffer_floor_pct` vs. real brokerage terms (items 17/18):** requires real brokerage-agreement data this codebase has never had access to — the same category of gap the now-closed Phase 7A research already catalogued; not reopened here, only re-noted as a standing evidentiary gap.
- **Non-`min_lot_dollars` gate staleness (item 20b):** no documented revisit-trigger exists for `trend_rsi_override`/`earnings_blackout_days`/`trim_rsi`, unlike `min_lot_dollars`'s explicit $25,000 trigger.
- **New-listing vs. data-feed-problem disambiguation (item 22):** no independent per-ticker listing-date source exists anywhere in this codebase.
- **Bar-quality validation (item 24):** no existing standard for "an implausible bar" exists, and defining one risks embedding a market-behavior judgment rather than verifying a stored fact.
- **Earnings-date correctness (item 26b):** no second, independent earnings-calendar source is integrated (only yfinance).
- **Deposit/withdrawal contamination in the performance log (item 35):** no deposit-event log (amount, date) exists anywhere in this codebase.

---

## 7. Decision Boundary

- **This document grants no implementation authorization.** Nothing in this assessment may be built, tested, or deployed on the basis of this document alone.
- **No validation work may begin without a separate, explicitly approved proposal.** Each item in §4 is a candidate for a future proposal, not a work order.
- **Each future proposal must identify the exact invariant being enforced** — quoting the specific fact from this document or its source, not a paraphrase or an expanded scope.
- **Each future proposal must prove that it does not introduce a new decision-maker**, using the same governing test applied throughout this document — a proposal that has drifted from "verify a fact" toward "decide something" is out of scope regardless of how it originated.
- **Any allocator-output change requires explicit governance review**, separate from and in addition to this workstream's own charter-compliance check — this document does not substitute for that review, and no candidate in §4 has received it.

---

## What this document deliberately does not do

- Does not implement any validation, in code or otherwise.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or any other production file.
- Does not modify any test.
- Does not modify `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`, `docs/PORTFOLIO_INPUT_INVENTORY.md`, or `docs/PORTFOLIO_INPUT_INVARIANTS.md`.
- Does not propose any new allocation input, scoring system, ranking system, thesis system, or recommendation of any kind.
- Does not change tier membership, universe membership, weights, sleeves, caps, trims, or margin doctrine.
- Does not create a backlog or prioritize the candidate set in §4 — the candidates are listed in the order their underlying inputs appear in the inventory, not by importance.
- Does not label any observation a "bug" — every finding is described in terms of documented invariants and directly-observed code behavior, per the same discipline `docs/PORTFOLIO_INPUT_INVARIANTS.md` already established.
- Does not infer intent where the code or an existing document is silent — every Insufficient-evidence classification states exactly what is missing rather than guessing.

Stopping here. Awaiting direction on whether any candidate in §4 should proceed to a separate, formal proposal — which, per §7, requires its own explicit approval and its own governance review before any implementation begins.
