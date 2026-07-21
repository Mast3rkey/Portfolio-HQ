# Numeric Parameter Provenance Audit

> **⚠️ Dated evidence snapshot, not an accepted decision and not a new source of operational authority.** This document classifies consequential numeric parameters found in this repository at one specific commit, using the materiality rule and taxonomy stated below. It changes no parameter, fixes no code, authorizes no research, and does not itself gate, permit, or block any allocation, trim, margin, or recommendation decision.

**Audit date:** 2026-07-21
**Audited `main` SHA:** `0b419765301128223c2f277bd162f38a6e50750c`
**Methodology:** read-only repository inspection (file reads, code tracing, `git log`/`git show`, GitHub PR metadata for historical context only) — no file was edited, no branch was created, no commit was made, no code was fixed, no calibration research was run, and no live Alpaca/brokerage/account-state fetch was performed as part of producing this document.

## Label vocabulary

Every substantive claim below is tagged with exactly one of:

- **VERIFIED** — directly confirmed against live repository content or code behavior during this audit.
- **REPOSITORY CLAIM** — stated in a repository document (a report, a decision record, a code comment) and cited as such, not independently re-derived here.
- **INFERENCE** — a synthesis or conclusion drawn by this audit across multiple sources.
- **UNCERTAINTY** — evidence is genuinely incomplete; stated as an open question, not resolved by inference.
- **RECOMMENDATION** — a suggested next action; not authoritative and not self-executing.
- **PRINCIPAL DECISION** — a point requiring the account holder's explicit sign-off before it can be treated as settled.

## Comprehensiveness disclaimer

This inventory is comprehensive under the materiality rule stated here; it is not a guarantee that no consequential numeric literal was missed.

## Authority disclaimer

This audit is a non-binding evidence snapshot. Current authority remains the Investment Constitution, accepted governance decisions, `targets.yaml`, `holdings.yaml`, and production code plus passing tests within their respective domains. Audit classifications do not supersede those sources.

## Snapshot preservation

This artifact describes repository state at the audited SHA (`0b419765301128223c2f277bd162f38a6e50750c`, 2026-07-21). It must not be silently rewritten later to represent a different repository state. A materially new audit should use a new dated artifact or an explicitly governed dated addendum — later findings do not retroactively alter what this snapshot observed.

Historical PR bodies and prior chat/session text (including PR #117's and #119's descriptions) are referenced in this document only as historical record of what was discussed or merged — never as repository authority. Authority is exclusively the Investment Constitution, `governance/decisions/*.md`, `targets.yaml`, `holdings.yaml`, and production code plus passing tests, per the precedence order `governance/decisions/GOV-0002-operational-precedence-hierarchy.md` establishes.

---

## 1. Methodology and Materiality Rule

This audit inspected `allocate.py`, `margin_state.py`, `indicators.py`, `levels.py`, `regime_gate.py`, `earnings.py`, `crypto.py`, `alpaca_client.py`, every `reports/*_backtest.md` file and its generating script, the full governance-decision corpus (`constitution/`, `governance/decisions/*.md`, `governance/decisions.yaml`, `decision_log.yaml`), `targets.yaml`, `holdings.yaml`, `CLAUDE.md`, and supporting `docs/` artifacts (`MARGIN_DOCTRINE.md`, `ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md`, `ALLOCATOR_UNKNOWNS_EVIDENCE_AUDIT.md`, `PHASE7_RESEARCH_PROGRAM_CLOSURE.md`, `PHASE5B_GOVERNANCE_DECISION.md`, `PORTFOLIO_INTELLIGENCE_SPEC.md`, `INVESTMENT_ONTOLOGY.md`, `FRESHNESS_PLANNER_V1_SPEC.md`).

**Materiality rule:** a numeric literal is *consequential* for this audit's purposes when changing it could materially alter an allocation, recommendation, trim, leverage or survivability outcome, risk classification, research verdict, governance gate, or the validity of an investment-facing output. Excluded from the parameter matrix (but not ignored — see Domain F): loop indices, dict-lookup literals, pure display/formatting numbers, dates/SHAs/decision IDs, and test-fixture-only values with no production code path. Pure engineering constants (HTTP timeouts, retry counts) are listed once in Domain F for completeness but scored for investment impact only where a duplication/drift risk makes them consequential.

---

## 2. Parameter Taxonomy

**Six parameter classes** (a parameter may have multiple contributing components; the record states which component actually selected the binding value):

1. **Externally imposed** — a broker/regulatory/contractual/market-convention constraint the system did not choose.
2. **Mathematically derived** — a reproducible formula over authoritative inputs, with no judgment call in the number itself.
3. **Empirically calibrated** — evidence directly and uniquely selected this specific number as superior to real, tested alternatives.
4. **Evidence-bounded governance selection** — evidence establishes a defensible range, constraint, or trade-off, but does not uniquely select one number; governance selected the exact binding value within that supported space and records the economic reason for that specific selection.
5. **Provisional governance guardrail** — a deliberately conservative interim value adopted under incomplete evidence, explicitly labeled as such, with a stated (calendar-, event-, or evidence-driven) review condition.
6. **Unsupported/unclassified** — fits none of the above: no external source, no derivation, no evidence (bracketed or unique), and no governance record. Distinguishes "never reviewed" from "reviewed and found provisional."

**Contextual classes, kept explicitly separate from the six above:**

- **Observed state** — synced account/portfolio facts (e.g., `holdings.yaml`'s margin debt/buffer/`synced_at`). Requires source, date, and freshness — not provenance classification.
- **Calculated output** — a value derived at runtime from other authoritative inputs (e.g., `target_dollars`, `net_equity`, TGT-0001/0002's disclosed nominal-target-sum arithmetic).
- **Research assumption** — a methodology choice about *how a test was run* (backtest window, deposit cadence, materiality threshold), distinct from the production parameter under test.
- **Engineering constant** — a non-investment literal (HTTP timeout, retry count, floating-point epsilon).
- **Test fixture** — a literal that exists only inside `test_*.py`, never consumed by production code.
- **Dates, identifiers, and formatting values** — SHAs, decision IDs, calendar dates.

---

## 3. Parameter Provenance Matrix

### Domain A — Portfolio Construction

| Parameter | Value | Location | Provenance class(es) — selecting component | Status |
|---|---|---|---|---|
| T1/T2/ETF/band/spec `weight_pct` | 3.35/1.65/2.30/0.75/1.00 | `targets.yaml:14-39` | Provisional governance guardrail — conviction-sizing doctrine selected these; `weight_backtest.md`'s 4-arm sweep found all structures within noise (evidence-bounded, non-selecting) | Active, binding |
| crypto `sleeve_pct` | 10.0% | `targets.yaml:42` | Provisional governance guardrail — doctrine explicitly states this is conviction-sizing, not return-optimized | Active, binding |
| Cluster caps: semis/power_infra/oil | 25%/20%/20% | `targets.yaml:66-101` | Evidence-bounded governance selection — correlation scan and (oil) drawdown-stress arithmetic are mathematically derived *inputs*; the cap level itself is a governance choice matching relative risk budgets across clusters, the selecting component | Active, binding, never backtested for return impact by design |
| `t1t2_trim_mult` | 1.5 | `targets.yaml:115-118` | Provisional governance guardrail — only one multiple was ever tested (vs. no-rule control), no alternative level swept, so no defensible range exists to call this evidence-bounded | Active, binding |
| `min_lot_dollars` | 25 | `targets.yaml:111` | Provisional governance guardrail, self-labeled with a stated $25,000-book revisit condition | Active, binding |
| `band.cap_multiple` | 1.25 | `targets.yaml:25` | Evidence-bounded governance selection — `trim_backtest.md`'s bracketing sweep (1.15x/1.40x tested, both inside the 1.0pp noise threshold) established a defensible range; governance kept the pre-existing value, reasoning that trims are risk control, not a return lever (the selecting component) | Active, binding **on the buy-side ceiling only** — see §5 latent finding |
| TGT-0001 nominal-target-sum ceiling | *(none adopted)* | `governance/decisions/TGT-0001-additive-target-budget-policy.md` | Explicit governance non-decision — a round-number ceiling was considered and declined in favor of a procedural rule (no cluster-target-total may exceed its own cap) | Active as a review-time rule, not a runtime number |

### Domain B — Margin and Capital Survivability

| Parameter | Value | Location | Provenance class(es) — selecting component | Status |
|---|---|---|---|---|
| `leverage_cap` | 1.8x | `targets.yaml:123`; fallback `allocate.py` `margin_capacity()` | **Provisional governance guardrail.** MARGIN-0001 adopted this as "the level in place when the debt was discovered" — a doctrine/continuity choice, not a backtest-derived one. **Not classified as evidence-bounded governance selection.** A later leverage-level sweep (1.2x/1.4x/1.6x/1.8x/2.0x, `docs/results/PHASE3_SCENARIO_RESULTS.md`) is recorded here only as **subsequent, non-selecting evidence**: results were flat/identical from 1.6x–2.0x and worse only at 1.2x, so the sweep failed to distinguish 1.8x from its adjacent tested levels and did not select, validate, optimize, or prove 1.8x safe. `MARGIN-0004`'s authority is carried forward unedited: the number was originally provisional, did not come from a backtest, remains binding, and is not validated merely by remaining unchanged. | Active, binding, hard cap |
| `buffer_floor_pct` | 30.0% | `targets.yaml:124`; fallback in `allocate.py` | **Provisional governance guardrail**, same MARGIN-0001 doctrine origin. Never backtested at any level (no script in this repository computes a buffer%-equivalent). Not evidence-bounded — no sweep of alternative floor levels exists. Remaining unchanged does not mean it has been validated. | Active, binding, hard cutoff |
| Margin interest | ~5% APR, first $1,000 free | `CLAUDE.md`, `docs/MARGIN_DOCTRINE.md` | Externally imposed (Robinhood account terms) | Active — see §4 freshness register; **verification date not recorded anywhere in this repository (UNCERTAINTY)** |
| `STALE_MARGIN_DAYS` | 2 | `allocate.py` (function: staleness check feeding `render()`'s margin-data-age warning); duplicated as `margin_state.py`'s `stale_threshold_days` default (`2.0`) | Provisional governance guardrail — reasonable engineering/safety choice, no config surface, no derivation | Active |
| CAUTION/RESTRICTED margin-state thresholds | Unset (`None`) | `targets.yaml`'s `margin:` block has no `states:`/`concentration_adjustment:` keys | N/A — structurally unreachable | **VERIFIED** dormant this audit (direct trace of `classify_margin_state()`'s call path in `allocate.py` confirms both remain `None`) |
| `concentration_min_fraction` default | 0.5 | `margin_state.py` (function default) and `allocate.py` (fallback read of `concentration_adjustment.min_fraction`) | Provisional governance guardrail (engineering default) | Dormant — `concentration_adjustment` key absent from `targets.yaml` entirely; see §5 latent finding for the `or 0.5` falsy-value handling risk |
| `BOOK_CHANGE_WARN_PCT` | 30.0 | `allocate.py` (`update_holdings()` fat-finger guard) | Provisional governance guardrail (engineering safety constant) | Active |

### Domain C — Allocator and Recommendation Mechanics

| Parameter | Value | Location | Provenance class(es) | Status |
|---|---|---|---|---|
| Gap-fill ranking | Greedy, largest-dollar-gap-first | `allocate.py` `plan()` | Unsupported/unclassified — a design choice never tested against alternative orderings | Active |
| `DAILY_LIMIT` / `DAYS_BACK` | 320 / 420 | `allocate.py` **and** `levels.py` (duplicated verbatim, no shared module) | Engineering constant (contextual class) | Active; canonical owner ambiguous — see §5 |
| `rung_atr_multipliers` | [1.0, 2.0, 3.0] | `targets.yaml:106`; fallback duplicated in `levels.py` (compute path and render-header path) | Evidence-bounded governance selection — `rung_backtest.md` compared this mechanism against two alternatives, all within the 1.0pp threshold; governance kept it (economic reason: no disprovable difference, existing staging mechanism retained) | Active, config-driven, fallback currently matches |
| `practicality_cap_pct` / `swing_low_sessions` | 25 / 60 | `targets.yaml:107-108`; fallback duplicated in `levels.py` | Provisional governance guardrail (untested display/tagging thresholds) | Active, config-driven, fallback currently matches |
| crypto sleeve "on target" tolerance | 0.5 percentage points | `allocate.py` `render()` | Engineering/display constant | Active, cosmetic only |
| ETF tier trim mechanism | **None exists** | `allocate.py` `plan()` — no `"ETF"` branch anywhere in the tier-trim logic | Unsupported/unclassified — `docs/ALLOCATOR_UNKNOWNS_EVIDENCE_AUDIT.md` classifies this "Still Unknown" whether deliberate; real, patterned circumstantial evidence exists on both sides, never resolved by any governance decision | Unaddressed gap, not demonstrated a defect |

### Domain D — Market, Earnings, and Technical Gates

| Parameter | Value | Location | Provenance class(es) | Status |
|---|---|---|---|---|
| RSI period | 14 | `indicators.py` (`rsi()` function and its hardcoded use inside `compute_all()`) | **Unsupported/unclassified** — no config path, no derivation, and only the gate's *existence* (never the period itself) was ever backtested | Active, binding, non-configurable |
| ATR period / SMA 200 / SMA 50 | 14 / 200 / 50 | `indicators.py` `compute_all()` | Unsupported/unclassified, same reasoning | Active, binding, non-configurable |
| RSI flat-series edge case | `avg_loss == 0` → `100.0` | `indicators.py` `rsi()` | Mathematically derived (correct branch of the RSI formula) — **VERIFIED** correct and tested | Active |
| `trend_rsi_override` | 30 | `targets.yaml:112`; fallback in `allocate.py` | Unsupported/unclassified as a specific level — only the gate's on/off state was tested (`trend_backtest.md`), never this threshold itself | Active, config-driven |
| `earnings_blackout_days` | 7 | `targets.yaml:113`; fallback in `allocate.py` | Provisional governance guardrail — declared untestable in `CLAUDE.md` (no historical earnings-date feed for backtesting) | Active, config-driven |
| `trim_rsi` | 60 | `targets.yaml:114`; fallback in `allocate.py` | Evidence-bounded governance selection — `trim_backtest.md`'s bracketing sweep (RSI 55/65 tested, both inside noise threshold) | Active, config-driven |
| `REGIME_EMA_DAYS` | 200 | `regime_gate.py` | Unsupported/unclassified as a level; the gate's existence was tested and removed from the buy path entirely (`regime_backtest.md`) | Display-only, no allocation effect |
| `_YAHOO_SYMBOL` map | `{"BRK.B": "BRK-B"}` | `earnings.py` | Engineering constant (manually maintained allowlist) | Active, fails safe (→ "unavailable"), not fails wrong |
| Market-hours staleness (9:30–4:00 ET) | *(no code guard exists)* | **VERIFIED** — no time-of-day or session check anywhere in `alpaca_client.py`/`allocate.py`/`levels.py`; `get_clock()` exists but is unused for this purpose | Structural data-feed limitation, not a code defect |

### Domain E — Research and Governance Methodology

| Parameter | Value | Location | Provenance class(es) | Status |
|---|---|---|---|---|
| Pre-committed materiality threshold | 1.0 percentage point | `backtest_{trims,rungs,regime,trend,weights}.py` (`ADOPT_THRESHOLD_PP`) | Research assumption (methodology, not a production parameter) — **VERIFIED** matches every report's prose exactly | Active |
| MaxDD tolerance (T1/T2 test only) | 1.0 percentage point | `backtest_t1t2_trim.py` (`MAXDD_TOLERANCE_PP`) | Research assumption | Active |
| `conviction.rating` vocabulary | {Low, Medium, High, Very High} | `intelligence_validator.py` | Provisional governance guardrail, frozen by `PI-0004`, enforced in code | Active, enforced |
| `lifecycle` vocabulary (Theme Intelligence) | {Emerging, Established, Mature, Declining, Archived} | Theme schema, `PI-0006`/`PI-0008` | Provisional governance guardrail, enforced in code | Active, enforced |
| `review.cadence_days` | 90 (uniform across all 7 current company records) | `intelligence/companies/*.yaml` | Provisional governance guardrail (human-set per record; happens to be uniform today, not itself required to be) | Active, none currently overdue — **VERIFIED** by direct arithmetic check |
| PI-0004's risk-vocabulary revisit trigger | "once 3-5 company records exist" | `decision_log.yaml` PI-0004 | Provisional governance guardrail with a stated, event-driven review condition | **VERIFIED met and exceeded** (7 records exist) and not yet re-examined by any subsequent decision |

### Domain F — Engineering Constants (investment-adjacent only)

| Parameter | Value | Note |
|---|---|---|
| Alpaca HTTP timeout / retries / backoff | 30s / 3 / 2s·(attempt+1) | No investment-decision path — resilience only |
| CoinGecko timeouts | 15s / 20s | No investment-decision path |
| `adjustment="split"` default | `alpaca_client.py` `get_bars()` | Has real investment impact if ever bypassed (unadjusted data could corrupt SMA/RSI around split dates); no caller currently overrides it |
| CoinGecko crypto daily-bar window | 365 days (vs. 420 elsewhere) | Currently dead code (`targets.yaml`'s `coingecko_ids: {}` is empty) — would under-serve SMA200 history the moment a coin routes through this path |
| Dollar rounding | `round(x, 2)` | Standard cents precision, immaterial |

---

## 4. External-Term Freshness Register

Only parameters classified **externally imposed** are listed here. No single universal freshness interval is applied — each cadence or stale-threshold is itself consequential and is recorded with its own rationale below.

| Parameter | Source | Observed/verified date | Account applicability | Point-in-time or durable | Refresh owner | Refresh condition | Behavior when stale/unavailable |
|---|---|---|---|---|---|---|---|
| Margin interest rate (~5% APR, first $1,000 free) | Robinhood margin account terms | **UNCERTAIN — no verification date recorded anywhere in this repository** | This specific Robinhood account | Point-in-time (broker-set, can change) but currently documented as if durable | Account holder (no API exposes this rate; Robinhood's own maintenance-ratio internals aren't available via Alpaca per `holdings.yaml`'s own comment) | None stated — **this is itself a gap** | Undefined — no fallback, no warning if the rate has since changed |
| Robinhood-displayed margin buffer % | Robinhood UI, pasted manually | `holdings.yaml`'s `synced_at` field — **VERIFIED** present and populated (2026-07-20 as of this audit's preceding session) | This specific account | Point-in-time by design (a live account state, not a durable term) | Account holder, via the documented `update-margin` workflow | Event-driven — "before any large margin-funded buy" per `CLAUDE.md`; also checked every run against `STALE_MARGIN_DAYS` | `STALE_MARGIN_DAYS` (2 days) triggers a warning banner in `render()` — a working example of the pattern the margin-rate row above lacks |
| Margin debt figure | Robinhood UI, pasted manually | Same `synced_at` field as buffer % | Same | Point-in-time | Account holder | Same event-driven condition | Same staleness warning |

---

## 5. Duplication and Drift Findings

Split explicitly per the audit's own severity discipline: findings where today's configuration **masks** a code-level divergence risk (no current defect demonstrated) vs. findings with a **currently demonstrated** effect. All findings below are the former.

- **Band-tier trim gate hardcodes `1.25`** in the RSI-gated trim branch of `allocate.py`'s `plan()`, instead of reading the `cap_multiple` value already computed one line earlier from `targets.yaml`'s `band.cap_multiple` key (which the buy-side ceiling calculation *does* read correctly). Canonical owner: `targets.yaml:25` (`band.cap_multiple: 1.25`). Duplicate/fallback location: the trim-branch literal in `plan()`. **Masked** — both values are `1.25` today. Consequence if exercised: if `band.cap_multiple` is ever changed, the buy ceiling and the trim gate would desynchronize for the entire band tier (a position could be bought up to the new ceiling and trimmed back down under the old one, or vice versa).
- **`crypto.sleeve_pct` has two independent hardcoded fallbacks for the identical config key**: the gap-computation path in `plan()` defaults to `0` if the key is absent; the display path in `render()` defaults to `10`. Canonical owner: `targets.yaml:42` (`crypto.sleeve_pct: 10.0`). **Masked** — the key is explicitly set today, so both paths agree. Consequence if exercised: a missing/misconfigured key would make the rendered advisory ("vs. 10% target") contradict the actual computed allocation gap (against 0%).
- **`concentration_min_fraction` uses an `x or 0.5` idiom** in the `targets.yaml`-config-reading path in `allocate.py`, which would silently discard an explicitly configured `0.0` (since `0.0` is falsy in Python) rather than treating it as a deliberate "no floor" setting. Canonical owner: would be `targets.yaml`'s (currently nonexistent) `margin.states.concentration_adjustment.min_fraction` key. **Dormant** — the `concentration_adjustment` block does not exist in `targets.yaml` today, so this code path never executes. Consequence if exercised: a future governance decision that explicitly sets this value to `0.0` would have that intent silently overridden to `0.5`.
- **`leverage_cap`/`buffer_floor_pct` fall back to hardcoded `1.8`/`30.0`** in `allocate.py` if `targets.yaml`'s `margin:` block or either key is absent, with no warning distinguishing "explicitly configured" from "config missing, silently defaulted." Canonical owner: `targets.yaml:123-124`. **Masked** — both values are explicitly present and match the fallback today. Consequence if exercised: a corrupted or partially edited margin config block would silently continue operating at the same numbers with no error, for the two most safety-critical parameters in the system.
- **`DAILY_LIMIT`/`DAYS_BACK` (320/420)** are duplicated verbatim across `allocate.py` and `levels.py`, with no shared constants module. Canonical owner: ambiguous by construction — neither file is authoritative over the other. **Masked** — both copies currently agree. Consequence if exercised: the two entry points (`allocate.py`'s main run vs. `levels.py`'s `--levels` staging) could compute different SMA200/RSI/ATR values for the same ticker on the same day if only one copy were ever edited — the same failure class already documented once historically in this repository (`docs/PORTFOLIO_HQ_AUDIT.md`'s regime-gate inconsistency).
- **`levels.py`'s three config fallbacks** (`rung_atr_multipliers`, `practicality_cap_pct`, `swing_low_sessions`) are each duplicated in three places (compute logic, render-header display, and `test_rungs.py`'s hardcoded fixture). Canonical owner: `targets.yaml`'s `levels:` block. **Masked** — all copies currently agree.
- **The backtest data cache (`data/backtest/*.json`) is frozen and stale relative to the live roster**: it includes VMC and TM (both removed from `targets.yaml` 2026-07-13) and excludes SPCX and SKHY entirely (never fetched into the cache). **VERIFIED** by direct comparison against `targets.yaml`'s current roster. Consequence: every "closed" backtest verdict (trim, rung, weight, regime, trend, T1/T2) was run against a roster snapshot that does not match production — a research-integrity fact, with no live-recommendation effect since the allocator does not read this cache at runtime.
- **`trim_backtest.md` claims "37 band/spec tickers"**; reconciling the current roster against the cache's known exclusions yields 36. **UNCERTAIN** — no available record explains the one-ticker gap.
- **All six `reports/*_backtest.md` files were first committed in this repository's single root commit**, even though their internal prose claims dates 5-7 days earlier than that commit. **VERIFIED** by `git log --reverse`. There is no version-control proof the claimed "pre-committed threshold, then run" sequence happened in that order for any of them — it is asserted in prose only.

Multiple verified latent source-of-truth or failure-mode risks currently masked or dormant under the audited configuration are enumerated individually above; none is demonstrated to be presently producing incorrect output.

---

## 6. Severity Findings (P0–P3)

**Severity standard applied:**
- **P0** — a current, demonstrated defect presently capable of producing an unsafe or materially incorrect recommendation, violating a binding safeguard, or threatening capital survivability under current repository state.
- **P1** — a consequential active or latent integrity defect that can materially alter recommendations or safeguards when exercised, but is currently masked, dormant, or not demonstrated to be firing under current state.
- **P2** — a meaningful methodological, duplication, freshness, or workflow weakness with lower immediate investment impact.
- **P3** — documentation or engineering cleanup with limited direct decision impact.

**P0: none demonstrated by this static audit.** No live Alpaca or account-state fetch was performed as part of this audit — this conclusion rests on static configuration/code review only. Current authoritative configuration (`targets.yaml`, `holdings.yaml`) masks every verified fallback and hardcode divergence found; none is shown to be presently producing an incorrect recommendation.

**P1 — latent or conditional findings** (do not imply these are currently firing):

| # | Finding | Conditional-elevation note |
|---|---|---|
| P1-1 | Silent `leverage_cap`/`buffer_floor_pct` fallbacks | Would require a corrupted/malformed `targets.yaml` margin block — not demonstrated |
| P1-2 | Band `cap_multiple` hardcode bypassing config | Would require `band.cap_multiple` to be changed from its current value — not demonstrated |
| P1-3 | Conflicting `crypto.sleeve_pct` fallbacks (0 vs. 10) | Would require the config key to be removed — not demonstrated |
| P1-4 | `concentration_min_fraction` falsy-value handling | Dormant; would require a future `concentration_adjustment` config block with an explicit `0.0` — not demonstrated |
| P1-5 | T1/T2 shipped-vs-tested trim mechanics mismatch | Elevates to P0 only if a live, read-only check shows a current T1/T2 name over 1.5x its target **and** the resulting trim is shown to produce a materially worse outcome than doctrine anticipated. **Not resolved by this audit** — see §7 |

**P2 — meaningful, lower-impact:** the 1.8x leverage cap's evidentiary characterization (real sweep exists, but flat/non-selecting above 1.4x — see Domain B); the 200-day SMA/14-day RSI periods' unsupported/unclassified status; the stale backtest cache; `STALE_MARGIN_DAYS`'s lack of a config surface; PI-0004's unactioned revisit trigger; the ETF tier's absent trim mechanism; `DAILY_LIMIT`/`DAYS_BACK` and rung-config duplication; `docs/MARGIN_DOCTRINE.md`'s stale "proposed" phrasing for the already-executed leverage sweep; the 37-vs-36 ticker count discrepancy.

**P3 — documentation/engineering cleanup:** engineering constants (Domain F); the pre-git-history provenance gap for backtest report dates; `_YAHOO_SYMBOL`'s single-entry allowlist; CoinGecko's currently-dead 365-day window.

**On empirical calibration:** this audit found no reviewed parameter conclusively meeting the full empirical-calibration standard (Class 3). This is a statement about the parameters actually reviewed in this pass, not a categorical claim that no parameter anywhere in the repository could ever meet that standard.

---

## 7. Unresolved Claims Requiring a Later Focused Check

Not resolved by inference in this document:

1. **Current T1/T2 threshold status** — whether any T1/T2 name presently exceeds 1.5x its target. The last documented live run (`docs/ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md`, 2026-07-17) showed 0-of-65 names over the ceiling (closest: MSFT at ~1.43x), but that is a prior snapshot, not a confirmation of current state. Requires a fresh, read-only allocator trace.
2. **Current cluster-cap status** — whether any of the semis/power_infra/oil clusters presently exceeds its cap. Same gap as above; requires the same live check.
3. **Broker-rate verification date** — no record anywhere in this repository states when the ~5% APR / $1,000-free margin-interest figure was last checked against Robinhood's actual current terms.
4. **37-vs-36 backtest roster discrepancy** — `trim_backtest.md`'s claimed ticker count does not reconcile against the current roster minus the cache's known exclusions; no available record explains the gap.
5. **Pre-git backtest ordering limits** — the six backtest reports' claimed dates (2026-07-12 through 2026-07-15) predate this repository's git root commit (2026-07-17); the claimed "pre-committed threshold, then run" sequencing cannot be independently verified from version control for any of them.

---

## What This Document Deliberately Does Not Do

- Does not change, fix, validate, or invalidate any parameter, code path, or configuration value.
- Does not authorize calibration research of any kind (leverage, margin deployment, margin repayment, T1/T2 trim, or otherwise).
- Does not authorize any code change or validator.
- Does not resolve any of the five unresolved claims in §7 by inference.
- Does not become operational authority by virtue of existing — see the authority disclaimer above.
- Is not superseded automatically by a future audit; a materially new snapshot requires its own new dated artifact or governed addendum.
