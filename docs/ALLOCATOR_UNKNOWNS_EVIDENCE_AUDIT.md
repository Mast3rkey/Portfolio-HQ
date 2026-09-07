# Allocator Unknowns — Evidence Audit

> **⚠️ Historical intent and evidence audit only.** This document classifies the five Unknowns recorded in `docs/ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md` using direct repository evidence — git history, commit messages, `CLAUDE.md`'s Decisions Log, backtest reports, tests, and code. It authorizes no implementation, changes no code/config/doctrine/account state, and does not use general investing or software-design convention to infer intent. Classification is descriptive, not a recommendation.

_Written 2026-07-17. `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`, `docs/PORTFOLIO_INPUT_INVENTORY.md`, `docs/PORTFOLIO_INPUT_INVARIANTS.md`, `docs/PORTFOLIO_INPUT_VALIDATION_ASSESSMENT.md`, `docs/PORTFOLIO_VALIDATION_GOVERNANCE.md`, and `docs/ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md` are frozen and unmodified by this document. Evidence gathered via: full `git log`/`git show`/`git blame` inspection of this repository's entire tracked history (138 commits), direct re-read of `CLAUDE.md`, `README.md`, `targets.yaml`, `allocate.py`, `reports/trim_backtest.md`, `reports/weight_backtest.md`, `docs/PHASE3_FINDINGS.md`, `docs/PHASE3_SCENARIO_MANIFEST.md`, and a full-text search of every tracked `.py`/`.md` file for the relevant terms._

**Foundational evidence fact, applying to every item below:** this repository's git history begins at commit `466fbce` ("Sync margin after $50 withdrawal (#13)"), which already contains a fully-formed `allocate.py` (617 lines), `targets.yaml`, and `CLAUDE.md` with the five-tier structure, the `$25` minimum lot, the band/spec RSI-gated trim rule, and the ETF tier's cap-less definition all already present. **No commit in this repository's history introduces any of these three mechanics — they predate this repository's tracked history entirely.** This is stated once here and applies to every relevant item below rather than being repeated per-item.

---

## Unknown 1: How often, in practice, does a run produce zero buys?

1. **Exact Unknown as stated:** "How often, in practice, does a run produce zero buys? No historical log of gate outcomes across prior runs exists in a queryable form."
2. **Relevant current behavior:** each `allocate.py` run writes a timestamped Markdown report to `logs/`, but `.gitignore` line 14 excludes `logs/` entirely from version control (confirmed by direct read of `.gitignore`).
3. **Current code path:** `main()`, allocate.py — `LOGS_DIR.mkdir(exist_ok=True)` then `log_path.write_text(out + "\n")`; `performance_log.csv` (tracked) records only `date, net_equity, gross, margin_debt, qqq_price, voo_price, note` — no buy/trim/block counts (confirmed by `PERF_FIELDS`, allocate.py:40).
4. **Earliest traceable introduction:** `logs/` gitignoring is present in the very first commit's `.gitignore`; `performance_log.csv`'s schema was introduced in commit `d648e1b` ("Add performance log: net equity vs QQQ/VOO (#20)") and has not changed its field list since (confirmed: no commit modifies `PERF_FIELDS`).
5. **Relevant commit/historical documentation:** `d648e1b`'s commit message describes the log's purpose as "net equity vs QQQ/VOO," not gate-outcome tracking — the log was never scoped to answer this question.
6. **Evidence the behavior was deliberate:** the choice to gitignore `logs/` while tracking `performance_log.csv` is a clear, deliberate split (two different files, two different `.gitignore` treatments) — but no document states *why* gate-level history specifically was excluded from the tracked log.
7. **Evidence it was expected to be completed later:** none found.
8. **Evidence contradicting current behavior:** none — the split is consistent across the entire repository history.
9. **Final classification: Still Unknown.**
10. **Confidence: High** (that the classification is correct — the absence of retained data is unambiguous and total).
11. **Evidence still needed:** a retained, queryable history of gate-level outcomes (buy/trim/block counts) across many runs — none exists and none can be reconstructed from `logs/` (gitignored, not retained) or `performance_log.csv` (wrong schema).

## Unknown 2: How many of the 21 currently-untrimmed band/spec overweight positions will eventually cross RSI 60, and when?

1. **Exact Unknown as stated:** as titled above.
2. **Relevant current behavior:** `ModelB`... *(not applicable — this is the live allocator, not the margin research harness)*. In `plan()`, a band/spec position over its dollar cap remains untrimmed indefinitely until a future run finds `rsi14 > 60` on that same day's data (allocate.py's band/spec trim branch, re-evaluated fresh every run).
3. **Current code path:** the band/spec trim check (`plan()`, allocate.py, step 7 in `docs/ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md` Part 1) — stateless, no memory of prior runs, no tracking of "days since first became overweight."
4. **Earliest traceable introduction:** predates this repository's history (see foundational fact above).
5. **Relevant commit/historical documentation:** `reports/trim_backtest.md` (analyzed in depth under "RSI-withheld overweights" below) is the closest relevant document but answers a different question (whether the *rule* is worth keeping), not a forecast of *when* any specific name will cross the threshold.
6. **Evidence the behavior was deliberate:** the RSI-gated design itself is deliberate (see the dedicated section below); but *this specific Unknown* — a forward-looking prediction — is not a design-intent question at all.
7. **Evidence it was expected to be completed later:** not applicable.
8. **Evidence contradicting current behavior:** not applicable.
9. **Final classification: Still Unknown.**
10. **Confidence: High** — this question is categorically unanswerable from repository evidence, since it asks about future, not-yet-occurred price action.
11. **Evidence still needed:** future daily price/RSI data for each of the 21 tickers — does not exist yet by definition, cannot be sourced from this repository at any point before it happens.

## Unknown 3: Whether today's zero-buy, one-trim pattern is typical or unusual relative to this portfolio's history

1. **Exact Unknown as stated:** as titled above.
2. **Relevant current behavior:** each run is stateless with respect to prior runs' gate outcomes (see Unknown 1).
3. **Current code path:** same as Unknown 1 — no code path retains or compares cross-run statistics.
4. **Earliest traceable introduction:** N/A — absence of a feature, not a behavior with an origin commit.
5. **Relevant commit/historical documentation:** none found addressing typical vs. atypical run outcomes.
6. **Evidence the behavior was deliberate:** none.
7. **Evidence it was expected to be completed later:** none.
8. **Evidence contradicting current behavior:** none.
9. **Final classification: Still Unknown.**
10. **Confidence: High.**
11. **Evidence still needed:** the same retained gate-outcome history named in Unknown 1's evidence gap, applied across a large enough sample to establish a baseline distribution.

## Unknown 4: What fraction of past deposit cycles were similarly constrained by the minimum-lot filter versus other gates

1. **Exact Unknown as stated:** as titled above.
2. **Relevant current behavior:** identical data gap as Unknowns 1 and 3 — no gate-attribution history is retained.
3. **Current code path:** same as above.
4. **Earliest traceable introduction:** N/A.
5. **Relevant commit/historical documentation:** `CLAUDE.md`'s Open Items section (present since the first commit, `466fbce`) states: *"`min_lot_dollars` ($25) doesn't scale with book size — fine at today's ~$5,600 book (~0.45%), but revisit once the book crosses roughly $25,000... not needed now."* This is directly relevant *context* — it documents the threshold's intended relationship to book size — but does not address, and cannot resolve, the specific question of historical constraint *frequency*, which requires run-by-run gate data this repository does not retain.
6. **Evidence the behavior was deliberate:** the $25 figure's relationship to book size is documented (see full analysis under "minimum-lot inactivity" below); the *frequency* question specifically is not addressed by any document.
7. **Evidence it was expected to be completed later:** the Open Items entry documents an intended *future revisit* of the threshold's value (not its historical frequency of binding) once book size crosses $25,000 — a related but distinct question.
8. **Evidence contradicting current behavior:** none.
9. **Final classification: Still Unknown.**
10. **Confidence: High.**
11. **Evidence still needed:** retained per-run gate-attribution data (which gate excluded which candidate, run over run) — does not exist.

## Unknown 5: Whether the ETF tier's lack of a trim rule is a deliberate design omission or an unaddressed gap

See the full dedicated audit below — summarized here per the required format.

1. **Exact Unknown as stated:** as titled above.
2. **Relevant current behavior:** `plan()`'s tier-branch logic defines trim behavior only for `band`/`spec` (dollar-cap + RSI) and `T1`/`T2` (1.5x ceiling, no RSI); no branch exists for `ETF` anywhere in the function.
3. **Current code path:** allocate.py `plan()`, lines ~213-237 (trim checks) — confirmed by direct re-read: the `if meta["tier"] in ("band", "spec"):` and `if meta["tier"] in ("T1", "T2"):` blocks are the only trim branches; no `elif`/additional branch references `"ETF"` anywhere in the function or file.
4. **Earliest traceable introduction:** predates this repository's history (foundational fact above) — the first commit's `targets.yaml` already lists ETF with a `weight_pct` and no `cap_multiple`, and the first commit's `CLAUDE.md` already describes the tier structure as *"**ETF** (SPY/QQQ/GLD) @ 2.3% · **band** @ 0.75% (cap 1.25×)"* — ETF's weight is stated with no cap annotation, immediately adjacent to band's weight, which explicitly carries one.
5. **Relevant commit/historical documentation:** detailed below.
6. **Evidence the behavior was deliberate:** circumstantial but non-trivial — see below.
7. **Evidence it was expected to be completed later:** none found.
8. **Evidence contradicting current behavior:** none found.
9. **Final classification: Still Unknown** (highest-confidence "Unknown" of the five in terms of the surrounding evidence being genuinely closer to a determination, but not crossing the bar this audit's own discipline requires — see below).
10. **Confidence: Medium** (higher than Unknowns 1-4, because the negative evidence here is unusually specific and patterned, not merely an absence of any record).
11. **Evidence still needed:** an explicit statement, from the account holder or a governance document, of intended ETF-tier treatment (permanent/accumulation-only holding, allocation-guide-only weight, or an unconsidered gap) — no such statement exists anywhere in this repository.

---

## Special focus: ETF-tier trim behavior — full audit

**Whether ETF positions were intentionally designed as permanent or accumulation-only holdings:** No document states this. `CLAUDE.md`'s Portfolio Doctrine describes ETFs (SPY/QQQ/GLD) only as one of the "5-sleeve structure" weights, with GLD separately noted (in the power_infra cap Decisions Log entry) as doing "the ballast job bonds would" — a functional description of *why GLD is held*, not a statement about whether its weight is a hard ceiling or a soft guide.

**Whether any document states that ETFs may remain above target:** No document states this affirmatively either. The absence is symmetric — nothing says ETFs must be trimmed, and nothing says they're allowed to run over.

**Whether ETF trim logic existed in an earlier implementation:** Cannot be determined — this repository's history begins with the mechanic already absent, and no prior repository/version is available to inspect.

**Whether tests encode the absence of ETF trimming:** No. A full-text search of every `test_*.py` file in this repository for "ETF" returns zero matches. The absence is untested, not asserted.

**Whether the tier was excluded deliberately from band/spec trimming:** ETF is structurally excluded by construction — the `if meta["tier"] in ("band", "spec"):` condition simply does not include `"ETF"` as a possible value. This is unambiguous *as a code fact*. Whether the *exclusion itself* was a deliberate design choice (as opposed to ETF simply never being considered when that branch was written) cannot be determined from the code alone.

**Whether any Decisions Log entry addressed ETF overweights:** No. A full-text search of `CLAUDE.md`'s Decisions Log for "ETF" returns only the power_infra cap entry, which mentions ETF solely as one of "the existing six (T1/T2/ETF/band/spec/crypto)" tiers when confirming no *new tier* was warranted — it does not address ETF overweight, ETF trimming, or ETF cap policy at all.

**Whether the band-overlay backtest or another study evaluated ETF trimming:** No study in this repository evaluated ETF trimming specifically. `reports/trim_backtest.md` — the one backtest that directly tested trim-rule variants — explicitly scopes itself to *"37 band/spec tickers"* (its own header, line 2) and never includes ETF, T1, or T2 tickers in its universe. `reports/weight_backtest.md` varies ETF's `weight_pct` across four arms but never varies or tests any *trim* behavior for the ETF tier — it is a target-weight study only. The June 2026 band-overlay backtest predates this repository's tracked history and no report file for it exists here to inspect; `CLAUDE.md`'s own summary of it ("227% vs 422% buy-and-hold... NO-GO on automated trading") describes a general finding against analytical trading layers, not anything specific to ETF trim mechanics.

**Whether current targets imply target weights are allocation guides only or enforceable upper bounds:** The evidence shows this varies *by tier*, not uniformly across the system — and the variation has changed over time via explicit, documented decisions. Band and spec have always carried an explicit, enforceable dollar-cap-based trim (1.25x and 1.0x respectively). T1 and T2 originally had **no enforceable ceiling at all** — their weights were allocation guides only — until commit `c925e82` ("Add T1/T2 concentration ceiling... doctrine decision... a single T1/T2 name at 2x+ target under leverage is a tail/forced-liquidation risk") deliberately converted them into enforceable ceilings, with an explicit rationale, a Decisions Log entry, and dedicated new tests. **This is the single most relevant piece of comparative evidence found**: it demonstrates this project has a real, working precedent for exactly this kind of transition (target-as-guide → target-as-enforced-ceiling), executed with a clear paper trail every time it has happened. ETF has never undergone this transition, and no document explains why not.

**Whether introducing an ETF trim path would change doctrine rather than merely enforce an existing invariant:** Based on the T1/T2 precedent, adding an ETF trim mechanism would be **the same category of change** T1/T2's ceiling was — a new doctrine decision (a new enforceable ceiling replacing a guide-only weight), not the enforcement of an already-existing but merely-unimplemented invariant. No document currently establishes that ETF weights were ever intended as anything other than guides, so there is no existing "invariant" for a trim mechanism to merely enforce. This is stated as a structural observation about what kind of change it would be, not as a recommendation to make it.

**Contextual pattern worth naming precisely:** the two commits that added concentration caps to previously-uncapped exposure (`37a69e7`, `c925e82`) both originated from an explicit, described audit process ("full-book sector audit," "capital-impairment Open Item") and both left a detailed paper trail explaining what was considered and why, including near-miss items explicitly declined with reasons (Materials/Utilities/Real Estate sectors, the enterprise-software cluster, CAT/TSLA). ETF has never appeared in any such audit's considered-and-declined list, despite being one of the six named tiers referenced directly in the power_infra commit's own text. This pattern is circumstantial, not conclusive — it is consistent with either "ETF was never brought up" or "ETF was considered informally but the decision was never written down" — but it is the reason this item's confidence is Medium rather than Low: the negative evidence here is unusually specific, not a generic absence.

**Conclusion for this focus area:** **Still Unknown**, per this audit's own discipline (ambiguity remains Unknown; "Unaddressed implementation gap" requires evidence of an *intended* behavior the code fails to implement, which does not exist here — no document ever states ETF *should* be trimmed). The absence of ETF trimming is **not concluded to be a defect** — this audit finds real, if incomplete, evidence of deliberate tier-by-tier design differentiation (band/spec always capped; T1/T2 later capped via explicit decision; ETF never addressed either way), and finds zero evidence contradicting the current behavior. That combination supports "Still Unknown," not "Unaddressed implementation gap."

---

## Special focus: RSI-withheld overweights — full audit

**Whether deferred trimming until strength is intentional:** Yes — **Intentional architecture**, with direct, strong evidence. `reports/trim_backtest.md` tested five arms against the current rule (A: 1.25x/RSI60), including **Arm E: "mechanical 1.25x, no RSI gate"** — an RSI-gate-free alternative was built, run, and directly compared (32.73% vs. current's 32.60% — a +0.13pp gap, inside the pre-committed 1.0pp noise threshold). The RSI gate was not merely left in place by default; a no-RSI-gate alternative was constructed and found statistically indistinguishable, and the RSI-gated version was explicitly kept.

**Whether indefinite persistence above the cap was considered:** Yes — directly. `reports/trim_backtest.md`'s **Arm D: "never trim (control)"** is exactly this scenario, tested and quantified: never-trim won on raw TWR (+6.65pp vs. current) but let RKLB balloon to 12.6% of the sleeve (vs. current's 3.6% largest final position). `CLAUDE.md`'s Decisions Log entry for this backtest (dated identically, "Trim backtest verdict: KEEP 1.25x / RSI 60, no amendments") explicitly reasons through this exact tradeoff: never-trim's TWR win came from a concentration risk that, "under the account's ~1.6x leverage... is deep enough to threaten the 30% buffer floor and force selling at the bottom" — indefinite persistence was not just considered, it was quantified and explicitly rejected as too risky under leverage, distinct from (and more severe than) the current RSI-gated behavior, where an overweight position persists only *temporarily*, pending an RSI condition, not indefinitely by design.

**Whether the cap is a hard ceiling or an action trigger conditional on RSI:** Confirmed directly from the code (allocate.py: `if current > overweight_limit and rsi is not None and rsi > trim_rsi:`) — the dollar cap is a **necessary but not sufficient trigger condition**, not a hard ceiling. A position can and does remain above its dollar cap indefinitely if RSI never crosses 60. This is the exact, current, unambiguous behavior — not an inference.

**Whether any alternative enforcement was previously tested and rejected:** Yes. Three alternatives were directly tested in `reports/trim_backtest.md`: tighter parameters (Arm B: 1.15x/RSI55, −0.10pp vs. current), looser parameters (Arm C: 1.40x/RSI65, +0.26pp), and the no-RSI-gate mechanical version (Arm E, +0.13pp) — all three fell inside the pre-committed 1.0pp noise threshold and were explicitly not adopted; the current 1.25x/RSI60 configuration was kept without amendment.

**Whether the current behavior matches the documented strategy exactly:** Yes. The trim_backtest.md report, the CLAUDE.md Decisions Log entry summarizing it, and the current `allocate.py`/`targets.yaml` values (`trim_rsi: 60`, `cap_multiple: 1.25`) are fully consistent with each other — no discrepancy found between documented intent and current implementation.

**Classification for this focus area: Intentional architecture. Confidence: High** — this is the best-evidenced item in this entire audit, supported by a dedicated backtest report, a Decisions Log entry, and a direct code match, with no contradicting evidence found anywhere.

---

## Special focus: minimum-lot inactivity — full audit

**Where the $25 value originated:** Cannot be determined — predates this repository's tracked history (foundational fact above). No earlier version of the codebase is available to inspect.

**Whether its interaction with a 65-security portfolio and a ~$6,240 book was anticipated:** No evidence found that this specific interaction (breadth × book size → most gaps falling under $25) was ever anticipated or discussed. The one relevant documented concern (`CLAUDE.md`'s Open Items, present since the first commit) frames the $25 threshold's adequacy purely in terms of **its size relative to total book value** ("$25 drops under ~0.1% of book and stops being a meaningful floor" once book exceeds ~$25,000) — a single-variable framing (book size only) that does not mention roster breadth (ticker count) as a second, independent variable affecting how often the floor binds. At today's $6,240 book, the documented $25,000 revisit-trigger is nowhere close to firing, yet the threshold fully suppressed all buy activity today — a real, evidenced gap between the documented concern (percentage-of-book meaningfulness) and the actual mechanism that produced today's outcome (breadth-driven gap compression).

**Whether it is documented as an operational-noise filter, transaction-efficiency rule, or another purpose:** The clearest documentation is the inline comment in `targets.yaml` itself (present since the first commit): `min_lot_dollars: 25  # do not recommend buys smaller than this` — a bare functional description, not a stated rationale (noise filter vs. transaction cost vs. something else). The Open Items entry's framing (a "meaningful floor" relative to book %) is the closest thing to a stated purpose, and it implies a **noise/materiality filter** (don't bother recommending trivially small buys) rather than a transaction-cost efficiency rule (no document mentions per-trade costs in connection with this threshold — Robinhood's $0 commission is documented elsewhere in `CLAUDE.md` as a separate, Known fact, which would argue against a pure transaction-cost rationale for this specific threshold).

**Whether any portfolio-size assumption accompanied its adoption:** Only the book-value-relative framing above (Open Items entry) — no roster-breadth assumption is documented anywhere.

**Whether prior backtests or simulations assessed allocator inactivity at smaller book sizes:** No. Every backtest in `reports/` (`trim_backtest.md`, `weight_backtest.md`, `rung_backtest.md`, `regime_backtest.md`, `trend_backtest.md`, `t1t2_trim_backtest.md`) simulates a full multi-year deposit sequence (e.g., "$2,000/mo × 62 deposits") starting from **$0**, meaning every backtest passes through a small-book, high-inactivity-risk phase early in its own simulated window — but none of these backtests' reports discuss or measure "how often no buy occurred" as a named output; all report only annualized TWR/MaxDD/trim-count style aggregate statistics for the full window. Confirmed by direct read of both `trim_backtest.md` and `weight_backtest.md`'s result tables — no "zero-buy-day count" or equivalent metric appears in either.

**Whether the current no-buy outcome is consistent with the documented intention:** Partially. The stated intention (a "meaningful floor" relative to book size) is not violated in the narrow sense the Open Items entry frames it — $25 is still a meaningful fraction check relative to a $6,240 book, well below the $25,000 revisit trigger. But the *outcome* the documented intention seems to anticipate (a rare, minor filtering of a few trivially-small gaps) does not match *today's actual outcome* (100% of underweight candidates filtered, zero buys). The single-variable (book-size-only) framing in the documentation does not fully explain or anticipate the specific, breadth-driven mechanism that produced today's result.

**Classification for this focus area: Still Unknown**, specifically as to whether today's *complete* inactivity was itself anticipated — the threshold's *general purpose* (a book-size-relative materiality floor) is documented (**Documented but incomplete** would apply to the threshold's own rationale, since a future revisit condition is explicitly named), but the *breadth-interaction mechanism* that actually produced today's zero-buy outcome is not addressed by that documentation at all, and no evidence establishes whether this specific interaction was ever considered. **Confidence: Medium** — the threshold's general purpose is well-documented (higher confidence than Unknowns 1-4), but the specific question of whether *today's exact failure mode* was anticipated remains genuinely unresolved by any available evidence.

---

## Classification totals

| Classification | Count | Items |
|---|---:|---|
| Intentional architecture | 0 (of the five numbered Unknowns); **1 additional finding outside the five** (RSI-gated deferred trimming, special focus section) | — |
| Documented but incomplete | 0 (of the five numbered Unknowns); **1 additional finding outside the five** (the $25 threshold's general book-size-relative purpose, special focus section) | — |
| Unaddressed implementation gap | 0 | — |
| Still Unknown | **5** | Unknowns 1, 2, 3, 4, 5 |

**Note on scope:** the five numbered Unknowns from `docs/ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md` are all classified **Still Unknown**. The two "special focus" areas requested (RSI-withheld overweights, minimum-lot rationale) surface additional, more specific sub-findings that *do* reach "Intentional architecture" and "Documented but incomplete" respectively — these are reported for completeness within their dedicated sections above, but do not change any of the five numbered Unknowns' own classifications, since each numbered Unknown asks a narrower or differently-scoped question (frequency/timing/typicality, not "is the rule itself intentional") than the special-focus sections examine.

## Governance implications

| Item | Action required to resolve |
|---|---|
| Unknown 1 (zero-buy frequency) | New empirical evidence — would require retaining gate-outcome history across future runs; no code change is needed to begin retaining it, but deciding whether to do so, and how, is outside this audit's scope |
| Unknown 2 (RSI-crossing timing) | No action possible — inherently unknowable in advance |
| Unknown 3 (pattern typicality) | New empirical evidence, same gap as Unknown 1 |
| Unknown 4 (historical min-lot constraint fraction) | New empirical evidence, same gap as Unknown 1 |
| Unknown 5 / ETF trim intent | Documentation clarification only, if pursued — asking the account holder directly whether ETF weights were ever intended as enforceable ceilings is not a code or governance action, merely a clarifying question; if the answer implies a design change, *that* would separately require a doctrine/governance review (per the precedent set by the T1/T2 ceiling's own decision process) |
| RSI-gated trims (special focus) | No action — already resolved, intentional, evidenced |
| Min-lot general purpose (special focus) | No action — already documented, with its own stated future revisit trigger |

**This section does not authorize any of the above actions** — it states what category of effort each would require if pursued, nothing more.

## Trading-readiness implication

**None of the five Unknowns, nor either special-focus finding, makes the current allocator unsafe or invalid for report-only use today.**

Distinguishing the three categories explicitly:

- **Known operational characteristics** (fully resolved, not Unknown at all): the RSI-gated band/spec trim design is intentional and matches its documented, backtested rationale exactly; the minimum-lot threshold's general purpose is documented, even though its interaction with today's specific roster breadth is not.
- **Unresolved design-intent questions**: only Unknown 5 (ETF trim intent) falls in this category — and it concerns whether a *mechanism that does not currently exist* (ETF trimming) should exist, not whether any *existing* mechanism is behaving incorrectly. An absent, never-tested trim rule for one tier is not a correctness failure of the rules that do exist.
- **Demonstrated correctness failures**: **none found**. Every gate traced in `docs/ALLOCATOR_OPERATIONAL_CHARACTERISTICS.md` and re-verified here behaves exactly as its own code and documentation describe. Today's zero-buy, one-trim outcome was produced by the allocator's rules operating exactly as designed, not by a malfunction.

This document gives no investment advice and issues no order instruction of any kind.

---

## What this document deliberately does not do

- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, `CLAUDE.md`, or any other production/configuration file.
- Does not modify any test.
- Does not modify any of the six frozen Portfolio Data Workstream / operational-characteristics documents.
- Does not add ETF trimming, change the RSI threshold, or change the minimum-lot threshold.
- Does not create a backlog, rank future work, or estimate effort.
- Does not propose a thesis, rating, conviction score, prediction, or security ranking of any kind.
- Does not authorize trading or order placement.
- Does not label any observed behavior a "bug" — every classification above follows the discipline stated in the task itself: ambiguity remains Unknown, and "Unaddressed implementation gap" is reserved for cases with direct evidence of an established intended behavior the code fails to implement, which this audit did not find for any of the five items.

Stopping here.
