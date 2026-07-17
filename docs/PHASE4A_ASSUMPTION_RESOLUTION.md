# Phase 4A: Assumption Resolution

> **⚠️ Hypothetical, simulated — a design document, not a result.** This document resolves open design questions from `docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md`. It contains no results, runs no simulations, and changes no code. When Phase 4A eventually executes, every output carries `HYPOTHETICAL_LABEL` and passes `margin_simulation.py`'s banned-phrase enforcement — the resolutions below exist specifically to make sure that discipline survives into execution unweakened.

_Written 2026-07-17, resolving `docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md` §6's five open assumptions before any execution harness is built. No code written. No production files touched — `allocate.py`, `targets.yaml`, `holdings.yaml`, and `margin_state.py` are not modified._

---

## 1. Scenario construction

### 1a. How concentration should be increased

**Restate:** Scenario B needs a defined method for constructing "increased concentration" from the current 63-ticker universe/weights.

**Why it matters:** Different construction methods answer different questions. An artificially doubled weight tests a hypothetical extreme; a real, un-trimmed drift (the T1-42.1%-of-book pattern the account actually exhibited before the T1/T2 ceiling was added) tests whether concentration this account has *actually produced* changes the risk picture. Picking the wrong one either overstates realism (synthetic extremes framed as plausible) or understates the question (only testing a mild, already-mitigated case).

**Options:**
1. **Synthetic weight inflation** — pick a T1 name, multiply its target weight by a fixed factor (e.g., 2x or 3x), redistribute the difference proportionally across the rest of the universe.
2. **Un-trimmed historical drift** — run the existing 63-ticker simulation with the T1/T2 ceiling and cluster-cap trims *disabled* (mirroring `t1t2_trim_backtest.md`'s own Arm A control), letting concentration emerge organically from real price appreciation, exactly as it did in the real account before the ceiling was added.
3. **Both, run independently, not blended** — synthetic inflation as the controlled, repeatable stress-testing device named in the research plan's own framing ("a stress-testing device, not a proposal for what concentration should be"), and un-trimmed drift as the real-account-analogous case, reported side by side.

**Recommendation:** **Option 3.** Using only synthetic inflation risks the finding being dismissed as an artificial, un-realistic construction. Using only un-trimmed drift limits the research to whatever concentration this specific window's price action happened to produce, which may not be severe enough to stress-test anything (the same weak-signal risk the research plan already flags for stress case 3's market-drawdown scenario). Running both, clearly labeled and never merged into a single number, preserves the most integrity: each construction is presented for what it is, not blended into an ambiguous composite.

**Approval required:** **Yes.** This determines what Scenario B/C/D actually measure — not an implementation detail.

### 1b. Historical weights, synthetic concentration, or both

**Restate:** Directly follows 1a — same question, restated at the "which data source" level rather than the "which mechanism" level.

**Why it matters:** Duplicate of 1a's core tension; kept as a separate line item only because the task explicitly names it, not because it is a distinct decision from 1a.

**Options:** Same three as 1a.

**Recommendation:** Same as 1a — **both**, reported side by side, never blended.

**Approval required:** **Yes** (resolved together with 1a as one approval, not two).

---

## 2. Stress methodology

### 2a. Historical drawdowns only, or hypothetical shocks allowed

**Restate:** Whether the four required stress cases (§4 of the research plan) may use constructed/hypothetical shock magnitudes, or must be drawn strictly from real historical single-name/cluster/market drawdowns already present in `data/backtest/*.json`.

**Why it matters:** This is the same tension Phase 3's Track 1 (real) vs. Track 2 (hypothetical) split existed to resolve (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md` / `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md`). Historical-only stress is more defensible (it happened) but may not be severe enough — this account's real universe's real worst episode found so far (NVDA's -66.4%, `t1t2_trim_backtest.md`) is already known and would just be re-used, not new evidence. Hypothetical shocks can be calibrated to any severity but invite the risk of being tuned, consciously or not, to produce a desired finding.

**Options:**
1. **Historical only** — every stress case draws its magnitude from a real, already-occurred drawdown in the 63-ticker universe's price history (NVDA's -66.4% for single-name; a real correlated-cluster decline for the multi-name case; the 2022 stretch, thin as it is, for the market case).
2. **Hypothetical only** — every stress case uses a constructed shock, sized independently of any specific real event.
3. **Historical primary, hypothetical secondary, explicitly labeled and never conflated** — the primary evidence uses real historical episodes (option 1); a hypothetical arm may additionally be run to probe severity beyond what history has supplied, but is always reported as clearly and separately labeled hypothetical-severity, following exactly the Track 2 pattern already established.

**Recommendation:** **Option 3.** This mirrors Phase 3's own resolved pattern (Track 1/Track 2 split) rather than inventing a new one, and directly serves the research plan's stated concern about stress case 3's data weakness — a hypothetical severity arm, clearly labeled, lets that specific gap be probed without pretending it's historical.

**Approval required:** **Yes.** Determines the entire evidentiary character of the stress cases.

### 2b. How to label simulated stress results

**Restate:** What text/labeling convention every Phase 4A stress-case output must carry.

**Why it matters:** Phase 3's entire disclosure discipline (`HYPOTHETICAL_LABEL`, `BANNED_PHRASES`, the "Under these assumptions, a simulated investor..." required framing) exists to prevent a hypothetical result from being read as a historical fact. Stress-case results carry extra risk here because they are, by construction, more dramatic than baseline results — exactly the kind of number most likely to be misquoted later if the label doesn't travel with it.

**Options:**
1. Reuse `margin_simulation.py`'s existing `HYPOTHETICAL_LABEL`/`render_metrics()`/`BANNED_PHRASES` machinery unchanged, with an additional explicit tag distinguishing historical-anchored stress (§2a option 1) from hypothetical-severity stress (§2a option 3's secondary arm) — e.g. `stress_source: "historical"` vs. `stress_source: "hypothetical"` in any machine-readable output, mirroring `phase3g_lib.py`'s pattern of small, additive, non-simulation-engine helpers.
2. Invent a new, separate labeling scheme specific to Phase 4A.

**Recommendation:** **Option 1.** No reason exists to invent a new scheme when Phase 3's already-tested one works and is already the established convention across every prior artifact in this project. The only addition needed is the historical-vs-hypothetical stress-source tag from §2a, which is new information (not present in Phase 3's scenarios, which were never stress-constructed), not a new label philosophy.

**Approval required:** **No** — this is confirming reuse of an already-approved mechanism, not introducing a new one. Flagged for completeness, not gated.

---

## 3. Concentration measurement

### 3a. Confirm which existing metrics can be reused

**Restate:** What already-built, already-tested measurement code from Phase 2-3 is available to Phase 4A without modification.

**Options / findings (not a decision point — a factual inventory):**
- `worst_case_concentration_impact()` (`margin_simulation.py`, Phase 3B) — directly reusable as-is. Computes the single-name-decomposition method this whole research question is built around.
- `concentration_risk_score()` (`margin_state.py`, Phase 2B) — reusable as a **reference implementation and conceptual comparison point only**. It is the live system's portfolio-level concentration scorer; Phase 4A can call it read-only to compute what the *live* system would currently report for a given synthetic state, as a comparison against Phase 4A's own findings — but it cannot be imported into a hypothetical simulation loop the way `margin_simulation.py`'s functions can, because doing so would blur the isolation boundary Phase 3B's module docstring explicitly established (`margin_simulation.py` "does NOT modify, import from, or depend on... margin_state.py"). This boundary is not relaxed by this document.
- `time_near_leverage_cap_pct_proxy` / `time_near_leverage_cap()` (Phase 3B) — reusable as-is for the "time above risk thresholds" metric's leverage dimension.
- `_leverage_capped_margin()` (Phase 3B, isolated re-derivation of `allocate.py`'s `margin_capacity()`) — reusable as-is for any "forced deleveraging" measurement, following the same deliberate-re-derivation-not-import pattern already established.

### 3b. Identify anything that would require new methodology

**Restate:** What Phase 4A needs that does not currently exist anywhere in this codebase.

**Findings:**
- **A concentration-tracking mechanism inside the simulation loop itself.** Nothing in `margin_simulation.py` currently tracks per-ticker or per-cluster weight/value as a % of book at each simulated day — `simulate()`'s existing per-day state (`gross`, `margin_debt`, `cash`, `positions`) has the raw ingredients (`positions` is a per-ticker share dict), but no derived concentration percentage is computed or exposed anywhere in `SimulationResult`.
- **Recovery-time measurement.** No existing function computes "days from trough back to pre-stress high" anywhere in this codebase — `ModelBProfitHarvest`/`ModelCRiskReset` track a high-water mark for triggering purposes, but neither exposes a reusable "time since last new high" measurement as output.
- **Forced-deleveraging event counting, specific to a concentration-stress context.** `phase3g_lib.ModelCTriggerLogger` is the closest existing precedent (observing a policy's internal state transitions without altering them) but was built specifically around `ModelCRiskReset`'s reset_active flag — Phase 4A's forced-deleveraging definition (§4 below) is a different condition and needs its own, analogous but new, observer.

**Recommendation:** All new methodology should follow the same pattern `phase3g_lib.py` already established for Phase 3G — small, pure, additive functions/observers operating on `SimulationResult` output (or wrapping an existing policy/state object), never modifying `margin_simulation.py`'s core `simulate()` engine or its existing tested classes. This is a recommendation for *how* new code should be structured when Phase 4A execution is eventually approved — it is not, itself, an approval to write that code now.

**Approval required:** **No decision needed here** — this section is an inventory and a structural recommendation, not a design choice requiring sign-off. (The recommendation's *implementation* still requires the separate execution-phase approval every other Phase 4A code change requires.)

---

## 4. Margin interaction

### 4a. Confirm leverage remains fixed during comparison

**Restate:** Whether Scenarios A/B/C's leverage cap is held constant across the concentration dimension (so only concentration varies, not leverage).

**Resolution:** **Confirmed, not merely proposed.** This follows directly from the research plan's own §4 stress case 4 ("concentration increase without leverage increase") and §2's scenario design (leverage is Scenario D's own distinguishing variable, not A/B/C's). Holding leverage fixed across A/B/C is required for the research question to be answerable at all — varying both concentration and leverage in the same comparison would make it impossible to attribute any risk-profile change to concentration specifically, the same "hold everything constant except the one thing being tested" discipline every backtest in this repo already follows.

**Approval required:** **No** — this is a restatement of the research plan's own already-approved design, not a new decision.

### 4b. Confirm no leverage optimization or new leverage thresholds

**Restate:** Whether Phase 4A may search for or propose a leverage threshold as part of this research.

**Resolution:** **Confirmed prohibited**, directly per the research plan's §5 ("do not add new margin rules," "do not select an optimal concentration level" — the same prohibition extends to leverage thresholds by the identical logic, and is restated here explicitly since the task calls it out separately). Phase 4A's `_leverage_capped_margin()` usage (§3a) is strictly for *measuring* when a fixed, given cap would force deleveraging under concentration stress — never for searching across caps to find a "safer" one. That would be leverage optimization by another name, prohibited by the same reasoning `docs/PHASE3_SENSITIVITY_PLAN.md`'s closing section already applied to Model B/C's parameters.

**Approval required:** **No** — restating an existing prohibition, not introducing a new question.

---

## 5. Scenario D leverage handling

**Restate:** Whether Scenario D (margin exposure during concentration stress) uses the current 1.8x cap only, or a range of caps.

**Why it matters:** The research plan's §6 assumption 5 explicitly flagged that a leverage-cap *range* for Scenario D "would reopen the no-optimization constraint... must be explicitly re-affirmed before any such range is run." This resolution closes that flag rather than leaving it open into execution.

**Options:**
1. **1.8x only** — the real, current, doctrine-fixed cap, matching every other Phase 3/4A scenario's leverage assumption.
2. **A range** (e.g., mirroring Phase 3's own leverage sweep, 1.2x-2.0x) — would let Phase 4A additionally ask "does the concentration-risk gap widen at higher leverage," a real, related, but *distinct* question from this plan's core research question.

**Recommendation:** **Option 1, 1.8x only, for this phase.** The core research question ("does concentration change the risk profile of margin usage") is fully answerable at the account's actual, real, doctrine-fixed cap — introducing a range here does not sharpen the answer to that question, it opens a second question (leverage-concentration interaction *across levels*) that was never in this plan's scope and was explicitly named as requiring its own separate approval. Keeping Scenario D at a single, fixed 1.8x preserves the cleanest possible attribution: any risk-profile difference found is attributable to concentration alone, not to a conflated concentration-and-leverage-level effect.

**Approval required:** **Yes, but resolved by default to Option 1 in this document.** If a leverage range is ever wanted for a related-but-distinct future question, that is explicitly out of scope here and would need its own new research plan, the same way Phase 4A itself required its own plan rather than being folded into Phase 3.

---

## 6. Success/failure criteria

**Restate:** What evidence would demonstrate the research question's answer, in either direction — explicitly not "which strategy wins," since this research produces no strategy to select from.

**Why it matters:** Without a pre-committed definition of what counts as a positive finding, a negative finding, or an inconclusive one, Phase 4A's eventual results could be read into after the fact — exactly the failure mode every pre-committed-threshold backtest in this repo (`trim_backtest.md` through `t1t2_trim_backtest.md`) exists to prevent. This section fixes the criteria *before* any execution, matching that standing discipline.

### What evidence would demonstrate concentration materially changes margin risk

All of the following would need to hold, not just one — a single suggestive number is not sufficient, matching the "necessary but not sufficient" standard `docs/PHASE4_READINESS_REVIEW.md` §1 already applied to Model B/C:

1. **A measurable gap between portfolio-level and single-name-level risk metrics** in Scenario D specifically — e.g., portfolio-level `max_drawdown_pct` looking materially better (smaller in magnitude) than `worst_case_concentration_impact()`'s single-name decomposition for the same run, the same pattern `t1t2_trim_backtest.md`'s NVDA case already demonstrated once.
2. **The gap widens, not just exists, between Scenario A/B (concentration alone, no stress) and Scenario D (concentration + margin + stress)** — demonstrating margin specifically amplifies the risk concentration alone doesn't fully reveal, not just that concentration itself is risky (a materially different, narrower claim than the research question).
3. **Forced-deleveraging events or leverage-threshold breaches occur in Scenario D that do not occur in an equivalent unlevered-but-concentrated scenario** — isolating margin's specific contribution to the finding, not concentration's alone.
4. **The result is not an artifact of a single synthetic construction choice** — i.e., the finding appears under both the synthetic-inflation and un-trimmed-drift constructions (§1), not only one of them, and (where a hypothetical-severity stress arm was run per §2a) is not solely a product of an aggressively-tuned hypothetical shock.

### What evidence would be inconclusive

- A gap exists between portfolio-level and single-name metrics **but does not widen** between the concentration-only scenarios and the margin-plus-stress scenario — suggests concentration itself is the driver, margin's specific contribution is unproven.
- The finding **appears under only one** of the two concentration-construction methods (synthetic-only or drift-only) — suggests the result may be a construction artifact rather than a general finding, same caution the research plan's §5/§6 already built in by requiring both methods be run and compared.
- **No forced-deleveraging or threshold-breach events occur at all** in any Scenario D arm — the same "the trigger never fired" outcome Phase 3G's Model C sweep already produced at higher drawdown thresholds; a real, honest, reportable finding (this window/construction doesn't stress the account enough to show the effect), not evidence the effect doesn't exist, exactly as `docs/PHASE3_FINDINGS.md` §6 and `docs/PHASE4_READINESS_REVIEW.md` §2 already treated Model C's non-firing result.
- **The single historical stress episode available (NVDA-anchored) is the only source of a positive finding**, with no corroboration from the hypothetical-severity arm or the correlated-cluster case — a real finding, but a thin one, requiring the same "one window, one episode" caveat every prior backtest in this repo has carried.

Explicitly, per the task's own framing: **there is no "winning scenario" outcome.** Neither "concentration matters" nor "concentration doesn't materially matter, portfolio-level metrics are sufficient" is a preferred result — both are valid, reportable findings under this framework, and neither would trigger an automatic doctrine change (per the standing rule: any finding, in either direction, requires its own separate, explicit approval step before affecting `targets.yaml`, `allocate.py`, or `CLAUDE.md`'s Decisions Log).

**Approval required:** **Yes.** These criteria govern how Phase 4A's eventual results will be read — they must be fixed now, before execution, exactly as this section states, not adjusted after seeing results.

---

## Summary of approval-required items

| # | Item | Approval required? | Default if unresolved |
|---|---|---|---|
| 1a/1b | Concentration construction: synthetic + un-trimmed drift, both, reported separately | Yes | Not run until approved |
| 2a | Stress methodology: historical primary + optional labeled hypothetical secondary | Yes | Not run until approved |
| 2b | Labeling: reuse existing `HYPOTHETICAL_LABEL`/`BANNED_PHRASES` + new stress-source tag | No (confirmation only) | N/A |
| 3a/3b | Metric reuse/new methodology inventory | No (factual inventory + structural recommendation) | N/A |
| 4a/4b | Leverage fixed across A/B/C; no leverage optimization | No (restates existing plan) | N/A |
| 5 | Scenario D leverage: 1.8x only, no range | Yes (resolved to 1.8x by default in this document) | 1.8x only |
| 6 | Success/inconclusive criteria | Yes | Not run until approved |

## What this document deliberately does not do

- Does not implement any code.
- Does not run any simulation or produce any result.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py`.
- Does not change doctrine in any direction.
- Does not resolve every item unilaterally — items marked "Approval required: Yes" remain open pending explicit sign-off; this document recommends, it does not decide on the user's behalf.

Stopping here. Awaiting approval on the items marked "Yes" above before any Phase 4A execution harness is built.
