# Research Backlog and Prioritization

> This document answers one question: **given everything learned through Phase 4A, what research question should be answered next?** It is a prioritization exercise, not a roadmap — some items below are recommended for deprioritization or closure, not scheduling. Nothing here is a doctrine change, a code change, or a production-file change. All prior findings referenced remain hypothetical/simulated, per every source document cited.

_Written 2026-07-17, following `docs/PHASE4A_RESEARCH_REPORT.md`'s "Evidence inconclusive" outcome. Sources reviewed: `docs/PHASE4_READINESS_REVIEW.md`, `docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md`, `docs/PHASE4A_ASSUMPTION_RESOLUTION.md`, `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`, `docs/PHASE4A_RESEARCH_REPORT.md`, `docs/results/PHASE4A_RESEARCH_RESULTS.json`, `docs/PHASE3_FINDINGS.md`, `docs/PHASE3_SENSITIVITY_PLAN.md`/`RESULTS.md`, `docs/MARGIN_DATA_INVENTORY.md`, `CLAUDE.md`._

---

## Reassessment (2026-07-17)

Item 1 (transaction cost sensitivity) has been completed — see `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md`/`RESULTS.md` and the consolidated `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md`. Marked **CLOSED** in place below rather than deleted, so the backlog stays a complete record of what was considered, not just what remains open.

Closing item 1 surfaced two new, higher-priority questions that were implicit in its own "what this doesn't resolve" section: **tax treatment** and **stress-regime execution assumptions** — both added below as items 9 and 10, and both ranked ahead of everything except the already-completed item 1. Concentration follow-up work (items 2 and 4) is explicitly **deprioritized further**: Phase 4A already established that concentration can produce a measurable degradation signal, but the evidence bar for changing any control has not been met, and neither item is expected to change that determination — further concentration research is lower-value right now than closing the cost-realism gap on Model B specifically. See the updated priority table at the end of this document.

## Phase 6A reconciliation (2026-07-17)

Items 9 (tax treatment) and 10 (stress-regime execution assumptions) were both completed after this document's prior update and were not marked closed at the time — a bookkeeping gap, not a finding. Both are now marked **CLOSED** below, item 9 including its Phase 6A FIFO-lot refinement (`docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md`).

**Evidence update (Phase 6A, tax-lot / FIFO modeling):**
- The worst-case tax upper bound (item 9's original result) was **materially reduced** by realistic FIFO lot accounting — the taxable base fell 57–62% at every tested `repay_fraction` ($38,226→$14,395 at 10%; $88,516→$38,219 at 25%; $156,113→$67,142 at 50%).
- Tax friction **remained material** for the higher repayment fractions (25%/50%) under every tested rate tier, despite that reduction — the earlier "material" classification did not flip to "noise" or "suggestive."
- At `repay_fraction`=10%, the result **remained inconclusive** in the sense that the gap was already sub-material pre-tax and stayed sub-material ("suggestive," not "material" or "noise") at every FIFO-realistic tax tier — no crossing occurred in either direction.
- **No `repay_fraction` is selected or recommended by this reconciliation.** All three arms remain open findings, reported in full.

**Reassessment of the three named questions:**
- **Do tax lots remain an open blocker?** Narrowed, not eliminated. The worst-case estimate was shown to be a real overstatement, and a more realistic (though still synthetic-account-only) figure now exists — but this account's real cost basis, real elected lot convention, real tax rate, and real jurisdiction remain entirely unknown, unchanged from before Phase 6A (`docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` §8). Tax treatment is no longer the single largest unresolved cost-realism question in this backlog — it has moved from "untested" to "tested, bounded, still incomplete."
- **Does execution modeling remain unresolved?** Yes, unchanged. Item 10's closure tested *timing* (does repayment activity cluster in detected stress windows — it does not) and applied only a flat/regime-conditional bps overlay, never a real slippage or spread-widening model. Real execution realism (actual fill quality, actual spread behavior under stress) remains untouched, per `docs/PHASE5_DECISION_GATE_REVIEW.md` §5's blocker list.
- **Do broker mechanics remain unresolved?** Yes, unchanged and not addressed by this phase at all — real Robinhood margin-call sequencing, maintenance requirements, and forced-liquidation mechanics remain a named, near-permanent gap (`docs/PHASE5_DECISION_GATE_REVIEW.md` §5, item 3; `docs/PHASE5B_GOVERNANCE_DECISION.md` §3's evaluation of Decision 2).

No new numbered backlog item is added for execution modeling or broker mechanics here — both are already named, tracked blockers in the Phase 5 governance documents cited above, not new research questions this backlog needs to independently number. Whether either is worth a dedicated future research track (as opposed to a documentation-only inventory) is a governance sequencing question, not a backlog-prioritization one — out of scope for this reconciliation.

---

## Scoring legend

- **Effort**: Small (hours, reuses existing harness/functions with no new abstraction) / Medium (new derived-metric layer or new scenario construction, still execution-layer) / Large (new simulation dimension, new data, or a combinatorial sweep).
- **Expected value**: Low / Medium / High — how much a clear answer would change what we know or could responsibly decide, not how interesting the question is.
- **Could change doctrine**: Yes / No / Structurally capped (evidence could point somewhere, but an existing doctrine rule already fixes the outcome regardless of what the evidence shows — e.g. the leverage cap is fixed "no discretion, no timing, no exceptions" per `CLAUDE.md`, so no backtest result changes it without "a new leverage regime," which is not a backtest question).

---

## 1. Transaction cost sensitivity for repayment-model turnover — **CLOSED (2026-07-17)**

**Resolution:** Implemented. `docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md`/`.json` found that cost erosion at 0/5/15bps (0bps Known, 5/15bps Hypothetical) was three orders of magnitude smaller than the already-observed Model B TWR/MaxDD gaps, and did not shift materiality classification at any `repay_fraction` × cost-tier combination tested. Consolidated into `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md`. This closes the *bps-based spread/slippage* question specifically — it does **not** close tax treatment, market impact under stress, execution timing, or behavioral friction, each of which is a distinct question (see items 9/10 below, and `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` §4/§5). Original scoring preserved below for the record, not re-evaluated now that it's closed.

**Question:** How much of Model B's (and any future Model C activations') return/drawdown trade-off survives once its measured turnover is actually priced?

**Why it matters:** `docs/results/PHASE3_MODEL_B_ANALYSIS.md` measured Model B's turnover at 30.8%–125.9% of deposited capital across its `repay_fraction` sweep, and explicitly flagged it as **unpriced** — no transaction-cost model exists anywhere in this repo. This is the single largest quantification gap standing between "Model B shows a real MaxDD improvement" and "Model B is worth anything after real trading costs."

**Evidence that exists:** Exact turnover dollar figures per `repay_fraction` value, already computed (`docs/PHASE3_SENSITIVITY_RESULTS.json`). The TWR/MaxDD trade-off at each fraction is also already computed.

**Evidence missing:** Any cost-per-trade assumption at all. Even a simple, clearly-labeled-Hypothetical fixed-bps assumption (mirroring how the 5% interest rate is labeled Estimated) would be new.

**Effort:** **Small.** No new simulation needed — apply a disclosed bps assumption to the already-measured turnover totals in `PHASE3_SENSITIVITY_RESULTS.json` and `PHASE4A_RESEARCH_RESULTS.json`, recompute net TWR after cost. Pure post-processing of data already collected.

**Expected value:** **High.** This is the cheapest possible research dollar in the backlog — it doesn't require running anything new, and it directly answers whether Model B's already-measured "advantage" survives contact with a cost nothing has priced yet.

**Dependencies:** Phase 3G's sensitivity results (done). Phase 4A's turnover-adjacent figures (done, though Phase 4A itself measured zero repayment activity, so this item's real substance is about Model B specifically).

**Could change doctrine:** No — Model B has no live doctrine status to change; this would inform whether it's worth *further* engineering investment, not alter a rule.

**Recommended priority: 1.** Highest value-to-effort ratio in this backlog by a wide margin.

---

## 2. A constructed, non-window-dependent market-drawdown stress case

**Question:** How does the concentrated + levered portfolio behave in a genuinely severe, broad market decline — not the mild 2022 stretch this repo's 2021-2026 window happens to contain?

**Why it matters:** `docs/PHASE4A_RESEARCH_REPORT.md`'s stress case 3 was implemented as a *windowed view* of an existing run (looking at what the concentrated scenario looked like during the control's own worst episode), not an independently constructed shock — explicitly flagged in that report as the weakest of the four required stress cases. Every document in this project going back to `regime_backtest.md` has carried the same "one mostly-rising sample, one brief bear stretch" caveat; this is the first opportunity to construct a stress case that doesn't depend on this window happening to contain one.

**Evidence that exists:** `phase4a_lib.apply_synthetic_shock()` already exists and is tested — applying it to a *single* ticker. Extending it to shock the whole universe simultaneously (or a representative subset) is a natural, small extension of an already-built, already-tested function.

**Evidence missing:** Any run of a genuinely broad, severe, synthetic market decline combined with concentration + margin.

**Effort:** **Medium.** `apply_synthetic_shock()` would need a loop over multiple tickers (or a new sibling function) — small, execution-layer, no `margin_simulation.py` change required (same pattern Phase 4A already established). One or two new scenario runs.

**Expected value:** **Medium-High.** Directly strengthens the weakest leg of Phase 4A's evidence base, and is the most direct way to test whether Phase 4A's "inconclusive" verdict is a real finding about this window's mildness or would look different under real stress — the same "trigger never fired" pattern from Phase 3G's Model C sweep is worth checking doesn't repeat here for the same underlying reason (this window rarely stresses anything hard).

**Dependencies:** Phase 4A's harness and scenario constructions (done).

**Could change doctrine:** No — even a severe finding here would still need to clear the same materiality bar and decision-gate discipline every other finding in this project has, before any doctrine question is even raised.

**Recommended priority: 2.**

---

## 3. Re-examine the "Evidence supports" AND-gate's second condition

**Question:** Is "forced-deleveraging event count" the right second criterion (alongside a material MaxDD gap) for concluding concentration materially changes margin risk — or does it structurally under-fire in this harness for a reason unrelated to the underlying question?

**Why it matters:** Phase 4A found a **material** MaxDD gap (D-hist vs B: −5.14pp) but **zero** forced-deleveraging events, producing "Evidence inconclusive" under the AND-gate defined in `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §5/§8. But `forced_deleveraging_events()` only fires when leverage *passively* exceeds the cap after debt is already drawn — since `simulate()`'s own allocation step already clips new draws to the cap, a passive breach requires gross to fall *after* debt was drawn, which is a narrower condition than "the account is under real, elevated risk." Meanwhile, the **time-above-threshold** metric Phase 4A also collected shows a large, real difference (NVDA time above 1.5x its target share: 61.7% control vs. 100.0% concentrated) that the current AND-gate doesn't use at all. This is a question about whether the *measurement design* is under-detecting a real effect, not about running new simulations.

**Evidence that exists:** All of it — this is entirely a re-analysis of Phase 4A's already-collected `docs/results/PHASE4A_RESEARCH_RESULTS.json`, no new simulation required.

**Evidence missing:** None — this is a methodology question, answerable by re-deriving the outcome classification with an alternative second criterion (e.g., time-above-threshold materiality) and comparing.

**Effort:** **Small.** Pure post-processing of existing JSON output plus a documented rationale for (or against) changing the AND-gate's second condition.

**Expected value:** **Medium.** Could flip Phase 4A's own headline outcome from "inconclusive" to "supports" — not because new evidence appeared, but because the current criterion may be measuring the wrong thing. Worth resolving before investing in item 4 (a broader sweep) or item 2 (a new stress construction), since both would inherit the same potentially-mis-specified gate.

**Dependencies:** Phase 4A results (done).

**Could change doctrine:** No — same reasoning as item 1; this affects how a research finding is *classified*, not any live rule.

**Recommended priority: 3.** Cheap, and arguably should happen before 2 or 4 since it could change how those items' own results get read.

---

## 4. Broader concentration construction sweep (other names, other clusters, multiple multipliers)

**Question:** Does Phase 4A's finding (or lack thereof) generalize beyond NVDA/semis at a single 3.0x/1.8x multiplier, or is it specific to that one pick?

**Why it matters:** `docs/PHASE4A_RESEARCH_REPORT.md`'s own Limitations section flags this directly: "one concentrated single-name pick (NVDA) and one cluster pick (semis) — not a sweep across possible concentrated names or clusters." NVDA was chosen because it's the already-decomposed reference point (`t1t2_trim_backtest.md`), not because it's necessarily representative.

**Evidence that exists:** The full harness (`phase4a_lib.py`, `run_phase4a_research.py`) is already built and generalizes trivially to a different `ticker`/cluster argument — no new code, just new parameter values and more runs.

**Evidence missing:** Results for any other concentrated name, any other cluster (power_infra, oil), or any other multiplier value.

**Effort:** **Medium-Large**, scaling with how many additional names/clusters/multipliers are included — a full combinatorial sweep (multiple names × multiple multipliers × both stress arms) would be Large; a handful of additional single points would be Medium.

**Expected value:** **Medium.** Diminishing returns versus items 1-3 — Phase 4A already established the method and found one real, material single-comparison gap; a broader sweep mostly tests whether that specific finding generalizes, which is useful but not as high-leverage as fixing the measurement question (item 3) or pricing the cost question (item 1) first.

**Dependencies:** Items 2 and 3 arguably should resolve first, so a broader sweep doesn't have to be re-run under a revised stress construction or outcome-classification method.

**Could change doctrine:** No — same structural reasoning as items 1-3; concentration findings inform future research and possibly a future cluster-cap-style doctrine proposal, but no Phase 4-family finding auto-adopts anything.

**Recommended priority: 4.**

---

## 5. Historical data collection infrastructure (margin/cashflow/interest/buffer logs)

**Question:** Not a backtest question — a "what should we start recording today so this becomes answerable from real data in the future" question, already scoped in full in `docs/MARGIN_DATA_INVENTORY.md`'s collection plan (`margin_log.csv`, `cashflow_log.csv`, an interest-charge log, a buffer time series).

**Why it matters:** `docs/PHASE4_READINESS_REVIEW.md` §3 restates this as a **permanent** gap — no amount of simulation research can ever answer "what did this account's real margin history actually do," because that history was never recorded. The only way this gap closes is by starting to log now.

**Evidence that exists:** The full schema and rationale already exist (`docs/MARGIN_DATA_INVENTORY.md`'s "Required future data collection plan" and its engineering-facing summary table). This is designed, not researched — implementation-ready.

**Evidence missing:** N/A — this isn't an evidence-gathering item, it's an evidence-*generating* capability that produces value only after months of accumulation.

**Effort:** **Small** to build (per `MARGIN_DATA_INVENTORY.md`: "simple CSV-append helpers structurally identical to `log_performance()`'s existing pattern"). **Note:** implementing `margin_log.csv` would mean extending `update_margin()` in `allocate.py` — this is the one item in this backlog that would touch a production file, and per this session's standing rule requires explicit authorization before any implementation begins, separate from prioritization.

**Expected value:** **High, but deferred** — the value doesn't materialize until real data accumulates over months; today's marginal value is near zero, next year's could be the only way to ever answer the "real historical margin behavior" question at all.

**Dependencies:** None — can start independently of every other item in this backlog.

**Could change doctrine:** No, not directly — but it's the only item in this entire backlog that could eventually produce evidence strong enough to bear on a real doctrine question, once enough real data exists (a multi-month-to-multi-year horizon).

**Recommended priority: 5.** Not urgent relative to items 1-4 (which use data already on hand), but cheap enough and valuable enough long-term that it shouldn't be pushed indefinitely — the earlier logging starts, the sooner it's useful.

---

## 6. Model C `reset_leverage` sensitivity sweep

**Question:** Does the 1.25x reset target (held fixed throughout Phase 3G's `drawdown_trigger_pct` sweep) itself matter, or would a different reset target change Model C's behavior materially?

**Why it matters:** Named explicitly as untested in `docs/PHASE3_SENSITIVITY_PLAN.md` §2 ("`reset_leverage`: 1.25x, unchanged... a combined trigger×target sweep is out of scope for this plan").

**Evidence that exists:** Phase 3G's full drawdown-trigger sweep, showing the trigger fires only 1-10 times depending on threshold, with essentially zero portfolio-level MaxDD impact even at the highest firing rate (12.5%: 7 fires, 0.00pp MaxDD gap).

**Evidence missing:** Any variation of `reset_leverage` itself.

**Effort:** **Small** — same harness, one more parameter to vary.

**Expected value:** **Low.** Phase 3G already showed Model C's mechanism barely engages in this window even at its most sensitive tested trigger — varying the reset *target* on top of a mechanism that rarely activates is unlikely to surface much, and Phase 4A independently found zero forced-deleveraging events across every concentration/stress combination tested. This window does not appear to stress Model C's mechanism enough for this parameter to matter yet.

**Dependencies:** None new.

**Could change doctrine:** No.

**Recommended priority: 6, likely defer indefinitely** unless item 2's broader stress construction changes the picture (if a real severe shock finally makes Model C fire meaningfully, revisit this then — not before).

---

## 7. Model C volatility-spike triggering

**Question:** Should Model C also trigger on a volatility spike, not just a drawdown, per the original Test C framing in `docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` ("gains, volatility spikes, or concentration increases")?

**Why it matters:** Explicitly named as NOT implemented, in `margin_simulation.py`'s own `ModelCRiskReset` docstring, flagged rather than silently assumed.

**Evidence that exists:** None — no volatility-triggered variant has ever been built or tested.

**Evidence missing:** Everything — this would be new trigger logic, a new parameter, and new test coverage.

**Effort:** **Medium** — a new trigger condition (rolling-window volatility calculation) inside the stateful policy pattern already established for `ModelCRiskReset`.

**Expected value:** **Low**, for the same reason as item 6 — a drawdown-based trigger already barely engages in this window; a volatility-based trigger would very likely show the same pattern (calm window, rare activation), making this a high-effort way to probably reconfirm what's already known.

**Dependencies:** None new.

**Could change doctrine:** No.

**Recommended priority: 7, defer indefinitely** unless a future window/data source materially changes the volatility picture.

---

## 8. Leverage-cap × concentration combined sweep (Scenario D leverage range)

**Question:** Does the concentration-risk finding change at higher leverage levels (e.g., 2.0x instead of 1.8x)?

**Why it matters:** `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §5 explicitly flagged this as reopening "a second, distinct question... never in this plan's scope," deferred rather than answered.

**Evidence that exists:** Phase 3's own leverage sweep (Scenario C) already found results identical from 1.4x-2.0x in this window for the *unconcentrated* portfolio — a hint, not proof, that a concentrated version might show the same flatness.

**Evidence missing:** Any concentration-stress run at a leverage level other than 1.8x.

**Effort:** **Medium** — same harness, sweep the `LEVERAGE_CAP_D` parameter Phase 4A already isolated as a single fixed value.

**Expected value:** **Structurally capped.** Even a dramatic finding here (leverage clearly amplifying concentration risk at 2.0x) would not, by this project's own stated doctrine (`CLAUDE.md`: "State it, apply it, don't relitigate without a new leverage regime"), change the 1.8x cap — leverage-level questions are explicitly doctrine, not backtest-driven, in this codebase. The research would be informative but structurally unable to translate into a production change without a prior, separate, non-research decision to treat the cap as open for backtest-driven revision, which nothing in this project's history supports.

**Dependencies:** Items 2/3 (a properly constructed stress case, and a validated outcome-classification method) should resolve first — running a leverage sweep against a possibly-mis-specified gate or an under-stressed scenario wastes the sweep's value.

**Could change doctrine:** **Structurally capped — No** in practice, per above, regardless of the finding's direction.

**Recommended priority: 8, low priority** — the doctrine-capped ceiling on this item's practical value means it should not be prioritized ahead of items that could actually inform a decision.

---

## Items recommended for closure (not backlog — already answered)

These appeared in `docs/PHASE4_READINESS_REVIEW.md`'s "special attention" list as open questions. On review, both are better classified as **already resolved by existing doctrine**, not open research questions — listing them as pending backlog items would misrepresent them as awaiting evidence they don't actually need.

- **Whether repayment should be automatic or optional.** `docs/PHASE4_READINESS_REVIEW.md` itself already concluded: in this codebase, "automatic" can only ever mean "surfaced as a recommendation in the advisory output," never unattended execution — order-placement code was deliberately stripped from `alpaca_client.py` and must never be re-added (`CLAUDE.md`'s foundational rule). No simulation result, from Model B/C or Phase 4A, can change that; it is a structural property of the tool, not an open empirical question. **Recommend: close, no further research.** If a future decision is needed, it's a design/doctrine discussion, not a backtest.

- **Whether margin should be treated as a portfolio-level risk resource only.** Already the consistent design throughout Phase 2-4 (`margin_state.py`'s `concentration_risk_score()` is explicitly portfolio-level; Model B/C operate on portfolio-level `net_equity`; `worst_case_concentration_impact()`'s own docstring explicitly disclaims any per-position leverage-allocation framing). Phase 4A's design decisions (§3a of the resolution document) reaffirmed this by keeping `margin_state.py`'s scorer read-only/reference-only rather than adapting it toward a per-position view. **Recommend: close as a design principle to explicitly reaffirm in `docs/MARGIN_DOCTRINE.md`** (a small documentation edit, not research) **rather than carry as an open backlog item.**

## 9. Tax treatment sensitivity for repayment-model turnover — **CLOSED (2026-07-17, refined by Phase 6A same day)**

**Resolution:** Implemented in two passes. **Pass 1 (upper bound):** `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md`/`.json` applied a disclosed worst-case assumption (100% of every repaid dollar treated as realized gain) at 0%/15%/32% illustrative rate tiers — found tax friction can materially change the magnitude of Model B's effect (at 50%/32%, gap widened from −3.56pp to −7.45pp). **Pass 2 (Phase 6A, FIFO-realistic):** `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` added a per-ticker FIFO lot ledger (additive-only extension to `margin_simulation.py`) and recomputed the same comparison using actual realized gain (proceeds minus cost basis) instead of the 100%-gain ceiling. Found the taxable base fell 57–62% at every `repay_fraction`, but the materiality classification did not change at the two fractions (25%/50%) where it was material before — tax friction remains a real, evidence-supported finding at those fractions, just smaller in magnitude than the original upper bound suggested. See the "Phase 6A reconciliation" section above for the full evidence summary. **Consolidated record:** `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` (canonical), `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` (pre-Phase-6A snapshot, preserved unedited). Original question/rationale preserved below for the historical record of why this item was opened.

**Question:** Does Model B's (or a future Model C's) TWR/MaxDD trade-off survive once realized gains/losses from its forced trim-and-repay cycles are taxed?

**Why it matters:** Added 2026-07-17, surfaced directly by closing item 1: `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` explicitly scoped out tax effects, and `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` §4 names this as the first of the "non-bps effects" the bps-cost result does not address. Unlike bid-ask spread (small relative to the observed gaps at every tested magnitude), realized-gain tax treatment could plausibly be large — Model B's 296 events at `repay_fraction=0.25` each force a partial sale of appreciated positions (the mechanism only fires on a new net-equity high, i.e. on gains), which is close to a worst case for tax drag (frequent, gain-triggered-by-construction realizations) rather than a typical trading pattern.

**Evidence that exists:** The exact event list (day, dollar amount) for each `repay_fraction` arm is already available from `run_transaction_cost_sensitivity.py`'s re-run — the same event stream the transaction-cost pass already priced could be re-priced with a disclosed tax-rate assumption instead of (or alongside) a bps assumption.

**Evidence missing:** Any tax-rate assumption, any cost-basis tracking (this harness tracks share counts, not per-lot cost basis, so a rigorous realized-gain calculation would need new bookkeeping — see Effort below), and any real data on this account's actual tax situation (short-term vs. long-term treatment, marginal rate) — all necessarily Hypothetical, the same epistemic status as the 5/15bps assumptions.

**Effort:** **Medium.** Unlike the transaction-cost pass (pure post-processing of already-known event dollar amounts), a realized-gain tax estimate needs cost-basis information the harness doesn't currently track per-lot — `simulate()` tracks aggregate share counts per ticker, not when each share was acquired at what price. A rigorous version would need a new, small, additive extension (average-cost-basis tracking per ticker, or a simplifying "average cost basis" approximation that doesn't require full lot-level tracking) — larger than item 1's zero-engine-change scope, but still execution-layer-first per this project's established discipline (extend the engine only if the observation genuinely can't be derived externally, matching Phase 4A's `track_tickers` precedent).

**Expected value:** **High.** Same reasoning as item 1 originally had, but for a cost category plausibly large enough to matter (unlike bps spread, which turned out immaterial at every tested magnitude) — this is the most direct way to test whether Model B's observed advantage is a real, tax-aware advantage or an artifact of a tax-free simulation environment.

**Dependencies:** Item 1 (done — establishes the event-stream/cost-application pattern this item reuses).

**Could change doctrine:** No — same reasoning as item 1; informs whether Model B is worth further investment, doesn't alter any live rule.

**Recommended priority: 1** (of the currently-open items — see the updated table below).

---

## 10. Stress-regime execution assumptions — **CLOSED (2026-07-17)**

**Resolution:** Implemented. `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md`/`.json` detected 21 real stress windows from QQQ's OHLCV data (12.2% of simulated trading days) and found repayment dollar volume is *under-represented* inside those windows at every `repay_fraction` (5.9–6.9% of repaid dollars vs. the 12.2% base rate) — Model B's high-water-mark trigger structurally favors calm/rising periods, not stressed ones. Threshold exposure stayed 0.0% (not material) at every arm. A disclosed regime-conditional cost overlay (3x multiplier inside detected stress windows) added only a few dollars over the flat-rate baseline — materiality classification unchanged from item 1's already-closed result. **This closes the repayment-*timing* question specifically** — it does not model real execution slippage or spread-widening (see the Phase 6A reconciliation section above: execution modeling remains a separate, unresolved blocker). Original question/rationale preserved below for the historical record of why this item was opened.

**Question:** Does the smooth 2021-2026 window hide bad-timing effects that would show up under real stressed-market execution conditions (widened spreads, slippage, delayed fills)?

**Why it matters:** Added 2026-07-17, the second question item 1's closure surfaced: `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` §4 names "market impact under stress" and "execution timing" as unresolved — the tested bps assumption was flat and unconditional, never widening during the account's own worst episodes. This is a distinct question from item 2 in this backlog (a constructed broad-market drawdown stress case for the concentration research line) — this item is about *execution realism* generally (does forced trading during a real stress episode cost more than the calm-market bps rate already tested), not concentration specifically, and could apply to Model B, Model C, or any future mechanical rule.

**Evidence that exists:** The same real 2021-2026 price data every Phase 3/4 scenario already uses; the 2022 stretch (this window's one real, if brief, bear period) as a natural candidate to check whether Model B's events cluster there and whether a stress-conditional cost multiplier (e.g., 2-3x the calm-market bps rate during a defined stress period) would change item 1's conclusion.

**Evidence missing:** Any stress-conditional cost model at all — item 1's cost was flat across the whole window regardless of market conditions.

**Effort:** **Small-Medium.** Reuses item 1's exact event-stream/cost-application pattern; the only new piece is defining a stress-period detector (e.g., "levels of decline from a rolling high" or reusing the existing regime-gate's QQQ-below-200-EMA concept, already computed and available, purely as a read-only reference signal, not reintroducing the removed regime gate as a rule) and applying an elevated bps rate only during those days.

**Expected value:** **Medium-High.** Directly tests whether item 1's "cost doesn't matter" finding is an artifact of this window's calm character (the same concern already raised about the 2021-2026 sample generally) or would hold under real stress-period execution costs too.

**Dependencies:** Item 1 (done). Loosely related to, but independent of, item 2 (the concentration-specific stress case) — could reuse a shared stress-period detector if both are pursued, but neither depends on the other completing first.

**Could change doctrine:** No.

**Recommended priority: 2** (of the currently-open items).

---

## The one permanent, unresearchable item

- **Real historical margin behavior.** `docs/PHASE4_READINESS_REVIEW.md` §3 and `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md` both already established this cannot be closed by more simulation — the real data doesn't exist. The *only* path forward is item 5 (data collection), and even then the payoff is measured in months/years, not this backlog cycle. Listed here for completeness, not as an actionable item.

---

## Recommended priority order (1 = highest value now)

_Updated 2026-07-17 following the Phase 6A reconciliation. Closed items are retained in the table, marked closed, so the sequencing history stays visible._

| Priority | Item | Effort | Value | Doctrine-capped? |
|---|---|---|---|---|
| **CLOSED** | Transaction cost sensitivity for repayment turnover | Small | High | No |
| **CLOSED** | Tax treatment sensitivity for repayment-model turnover (upper bound + Phase 6A FIFO refinement) | Medium | High | No |
| **CLOSED** | Stress-regime execution assumptions | Small-Medium | Medium-High | No |
| 1 | Historical data collection infrastructure | Small (touches `allocate.py` — needs authorization) | High, deferred | No (enables future evidence only) |
| 2 | Re-examine the "Evidence supports" AND-gate | Small | Medium | No |
| 3 | Constructed broad-market stress case (concentration line) | Medium | Medium-High | No |
| 4 | Broader concentration construction sweep | Medium-Large | Medium | No |
| 5 | Model C `reset_leverage` sweep | Small | Low | No |
| 6 | Model C volatility-spike triggering | Medium | Low | No |
| 7 | Leverage-cap × concentration combined sweep | Medium | Structurally capped | Structurally capped |

**Rationale for the reordering:** with items 1, 9, and 10 all now closed, every item in this backlog that used the Model-B-turnover cost-realism line of inquiry (bid-ask spread, tax treatment, execution timing) has been tested exactly once, per this project's standing "answer it once, don't relitigate without new evidence" discipline. Data collection infrastructure (formerly priority 3) moves to priority 1 purely because the items that outranked it are now closed, not because its own effort/value/dependency profile changed. Concentration-line items (formerly priorities 4-6, now 2-4) remain in the same relative order and same reasoning as before: Phase 4A already established concentration can produce a measurable degradation signal, but the evidence bar for changing any control has not been met, and none of these items is expected to change that determination on its own. Items 5-7 remain deprioritized for the same reasons as before (Model C's mechanism shows almost no activity in this window regardless of parameter; the leverage-cap sweep is doctrine-capped regardless of finding). **Note:** execution-realism and broker-mechanics blockers named in the Phase 6A reconciliation section above are not represented as numbered items in this table — they are tracked in `docs/PHASE5_DECISION_GATE_REVIEW.md`'s blocker list, a governance document, not this research-prioritization backlog; whether either becomes a formal backlog item is a future, separate decision.

## What this document does not do

- Does not commit to building any of the above. It is explicitly a prioritization exercise, not a roadmap.
- Does not change any doctrine, any production file, or any prior finding's status.
- Does not resolve item 3's methodology question itself — it identifies the question and recommends it as the next small, cheap analysis, but the actual re-derivation is future work pending approval.
- Does not treat "close, no further research" (the two doctrine-reaffirmation items) as equivalent to "unimportant" — closing an item because it's already answered is itself a useful output of a prioritization pass, not a dismissal.

Stopping here. Awaiting direction on which item, if any, to pursue next.
