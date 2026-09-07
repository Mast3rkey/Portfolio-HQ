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

## Final reconciliation (2026-07-17)

Per `docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`, the Phase 3–7A margin research program is closed. This is the final status pass on this backlog: every item below is now classified exactly one of **CLOSED** (answered, resolution on record), **CLOSED — NO FURTHER VALUE EXPECTED** (not pursued further, and further pursuit is not expected to produce value relative to its cost — a deliberate, reasoned closure, not an oversight), or **OPEN** (still capable of changing governance, with a stated reason why it isn't already answered and what evidence could change the answer). No new item is created in this pass. Two items previously carried as open backlog priorities are reclassified here for the first time:

- **Item 2** (constructed broad-market stress case) and **item 4** (broader concentration construction sweep) move to **CLOSED — NO FURTHER VALUE EXPECTED**. Phase 7A's execution-reality findings identified the actual highest-relevance gap in the concentration research line as a *representational* one (the simulator has no analog for FINRA's real concentration-triggered maintenance escalation or for forced liquidation at all — `docs/PHASE7A_DECISION_RELEVANCE_MAP.md` item 1), not a *coverage* one (more synthetic severity levels or more concentrated-name picks). Running either item now would add more evidence of the same kind the program has already produced in volume, on a question Phase 7A reframed rather than left open.
- **Item 3** (re-examine the AND-gate's second condition) moves to **CLOSED**. This was, in substance, already done: `docs/PHASE4A_OUTCOME_GATE_REVIEW.md` performed exactly this re-analysis and adopted a widened gate (material gap AND (repeated forced-deleveraging events OR material threshold-exposure degradation)) for future research cycles, explicitly without retroactively reclassifying Phase 4A's own recorded result. This backlog item's question is answered; it was simply never marked closed here.
- **Items 6, 7, 8** (Model C `reset_leverage` sweep, Model C volatility-spike triggering, leverage-cap × concentration sweep) move to **CLOSED — NO FURTHER VALUE EXPECTED**. Per `docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`'s explicit "would not do" list (no further leverage sweep, no further repayment sweep, no further concentration sweep), and each item's own already-recorded Low/Structurally-capped expected value — none has a plausible path to changing governance regardless of effort spent.
- **Item 5** (historical data collection infrastructure) remains **OPEN** — see its updated entry below for why.

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

## 2. A constructed, non-window-dependent market-drawdown stress case — **CLOSED — NO FURTHER VALUE EXPECTED (2026-07-17)**

**Resolution:** Not pursued. Per the "Final reconciliation" section above: Phase 7A's evidence inventory and decision relevance map identified the concentration research line's actual highest-relevance open question as representational (the simulator has no analog for real concentration-triggered maintenance requirements or forced liquidation, `docs/PHASE7A_DECISION_RELEVANCE_MAP.md` item 1) rather than a matter of testing more synthetic severity levels. A broader synthetic shock would add more evidence of a kind this program already has in volume, not resolve the gap Phase 7A actually found. Original question/rationale preserved below for the historical record of why this item was opened.

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

## 3. Re-examine the "Evidence supports" AND-gate's second condition — **CLOSED (2026-07-17)**

**Resolution:** Already done, in substance, by `docs/PHASE4A_OUTCOME_GATE_REVIEW.md` — a formal governance review that performed exactly this re-analysis and adopted a widened outcome gate (material MaxDD gap AND (repeated forced-deleveraging events OR material threshold-exposure degradation)) for future research cycles, per its own explicit non-retroactivity statement: Phase 4A's recorded "Evidence inconclusive" result was not itself reclassified. This backlog item's question was answered before this final reconciliation pass; it was simply never marked closed here. Original question/rationale preserved below for the historical record of why this item was opened.

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

## 4. Broader concentration construction sweep (other names, other clusters, multiple multipliers) — **CLOSED — NO FURTHER VALUE EXPECTED (2026-07-17)**

**Resolution:** Not pursued, same reasoning as item 2 above — Phase 7A reframed the concentration research line's real gap as representational (a missing broker-mechanics analog), not a matter of testing more names/clusters/multipliers with the existing simulator. Original question/rationale preserved below for the historical record of why this item was opened.

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

## 5. Historical data collection infrastructure (margin/cashflow/interest/buffer logs) — **OPEN**

**Why it remains open:** This is the one item in the entire backlog that is not a simulation question — it produces the only kind of evidence `docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md` names as capable of justifying reopening the margin research program at all (real broker records, real fills, real borrowing history — as opposed to more simulation on data this program already has).

**Why it is not already answered:** No margin/cashflow/interest/buffer logging has been implemented. The schema and rationale are fully designed (`docs/MARGIN_DATA_INVENTORY.md`) but nothing has been built — this is a genuine, unstarted gap, not a bookkeeping omission like items 3/9/10 were before their own reconciliation passes.

**What evidence could realistically change the answer:** Starting the log now and letting it accumulate for months to years would eventually answer "what did this account's real margin history actually do" — a question no amount of additional simulation, in this program or any successor, can ever answer instead. Its value is entirely deferred and cannot be accelerated by more research effort today.

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

## 6. Model C `reset_leverage` sensitivity sweep — **CLOSED — NO FURTHER VALUE EXPECTED (2026-07-17)**

**Resolution:** Not pursued. Per `docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`'s explicit "would not do" list (no further repayment/leverage sweep) and this item's own already-recorded Low expected value — Model C's drawdown trigger barely engages in this window at any tested threshold (Phase 3G), and Phase 4A independently found zero forced-deleveraging events across every concentration/stress combination. Sweeping a second parameter on a mechanism that rarely activates has no plausible path to changing governance. Original question/rationale preserved below for the historical record of why this item was opened.

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

## 7. Model C volatility-spike triggering — **CLOSED — NO FURTHER VALUE EXPECTED (2026-07-17)**

**Resolution:** Not pursued, same reasoning as item 6 — building an entirely new trigger mechanic for a policy class that already barely activates on its existing trigger, in the same calm-dominant window, is a high-effort way to most likely reconfirm what Phase 3G/4A already established. Original question/rationale preserved below for the historical record of why this item was opened.

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

## 8. Leverage-cap × concentration combined sweep (Scenario D leverage range) — **CLOSED — NO FURTHER VALUE EXPECTED (2026-07-17)**

**Resolution:** Not pursued. This item's own already-recorded scoring already classified it as **Structurally capped** — no finding here, however dramatic, could change the 1.8x leverage cap without a prior, separate, non-research decision to treat the cap as open to backtest-driven revision, which nothing in this project's doctrine supports (`CLAUDE.md`: "State it, apply it, don't relitigate without a new leverage regime"). Confirmed closed rather than left open, since its ceiling on practical value was already established, not newly discovered. Original question/rationale preserved below for the historical record of why this item was opened.

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

## Items recommended for closure (not backlog — already answered) — **CLOSED**

These appeared in `docs/PHASE4_READINESS_REVIEW.md`'s "special attention" list as open questions. On review, both are better classified as **already resolved by existing doctrine**, not open research questions — listing them as pending backlog items would misrepresent them as awaiting evidence they don't actually need.

- **Whether repayment should be automatic or optional — CLOSED.** `docs/PHASE4_READINESS_REVIEW.md` itself already concluded: in this codebase, "automatic" can only ever mean "surfaced as a recommendation in the advisory output," never unattended execution — order-placement code was deliberately stripped from `alpaca_client.py` and must never be re-added (`CLAUDE.md`'s foundational rule). No simulation result, from Model B/C or Phase 4A, can change that; it is a structural property of the tool, not an open empirical question. If a future decision is needed, it's a design/doctrine discussion, not a backtest.

- **Whether margin should be treated as a portfolio-level risk resource only — CLOSED.** Already the consistent design throughout Phase 2-4 (`margin_state.py`'s `concentration_risk_score()` is explicitly portfolio-level; Model B/C operate on portfolio-level `net_equity`; `worst_case_concentration_impact()`'s own docstring explicitly disclaims any per-position leverage-allocation framing). Phase 4A's design decisions (§3a of the resolution document) reaffirmed this by keeping `margin_state.py`'s scorer read-only/reference-only rather than adapting it toward a per-position view.

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

## Final status (2026-07-17)

_This table supersedes the prior "Recommended priority order" table, which prioritized among open items during active research. The program is now closed (`docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`); every item below carries a final status rather than a ranking. Closed items are retained, not deleted, so the record of what was considered stays complete._

| Item | Final status |
|---|---|
| 1. Transaction cost sensitivity for repayment turnover | **CLOSED** |
| 2. Constructed broad-market stress case (concentration line) | **CLOSED — NO FURTHER VALUE EXPECTED** |
| 3. Re-examine the "Evidence supports" AND-gate's second condition | **CLOSED** |
| 4. Broader concentration construction sweep | **CLOSED — NO FURTHER VALUE EXPECTED** |
| 5. Historical data collection infrastructure | **OPEN** |
| 6. Model C `reset_leverage` sensitivity sweep | **CLOSED — NO FURTHER VALUE EXPECTED** |
| 7. Model C volatility-spike triggering | **CLOSED — NO FURTHER VALUE EXPECTED** |
| 8. Leverage-cap × concentration combined sweep | **CLOSED — NO FURTHER VALUE EXPECTED** |
| 9. Tax treatment sensitivity for repayment-model turnover | **CLOSED** |
| 10. Stress-regime execution assumptions | **CLOSED** |
| Repayment automatic-vs-optional (doctrine reaffirmation) | **CLOSED** |
| Margin as portfolio-level-only resource (doctrine reaffirmation) | **CLOSED** |
| Real historical margin behavior (permanent gap, tracked under item 5) | **OPEN** (via item 5 only — no direct research path) |

**Nine of eleven tracked items are CLOSED; two are OPEN.** Both open items (5, and the permanent-gap note tracked under it) share the same resolution path — historical data logging, not further simulation — and neither is expected to produce value on any timescale shorter than months. No item was removed from this backlog; every item that was ever tracked here retains its final disposition on the record.

## What this document does not do

- Does not commit to building item 5 (data collection infrastructure) — it remains open, not authorized; implementation would still require its own separate approval, per this session's standing rule (it is the one open item that would touch `allocate.py`).
- Does not change any doctrine, any production file, or any prior finding's status.
- Does not treat "CLOSED — NO FURTHER VALUE EXPECTED" as equivalent to "the underlying question doesn't matter" — several of these items (concentration risk, Model C's activation rate) produced real, useful findings before being closed; the classification means further investment in *that specific question* is not expected to add value, not that the question was unimportant to have asked once.
- Does not reopen any Phase 3–7A conclusion.

**Current backlog intentionally contains only questions capable of changing governance.**
