# Phase 4A: Materiality Thresholds

> **⚠️ Hypothetical, simulated — a design document, not a result.** No simulation described here has been run for Phase 4A. This document fixes numeric thresholds BEFORE any execution, per the standing pre-committed-threshold discipline this repo has followed since `rung_backtest.md`. Every number below is chosen for stated reasons, anchored where possible in real, already-collected Phase 3 evidence — never picked to produce a convenient answer.

_Written 2026-07-17, required companion to `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6, added per explicit approval feedback: "Before building the execution harness, require Claude to define what constitutes a 'material' change. Not in terms of optimization, but statistical and practical significance." Documentation only — no code, no tests, no production files touched._

---

## 1. Why classical statistical significance doesn't apply

`margin_simulation.py`'s `simulate()` is deterministic: a given scenario configuration run against a fixed price history produces exactly one number, every time (proven directly by Phase 3G's own verification asserts — the 25%/15%/5% "reused" arms matched Phase 3E's stored results to within `1e-6`). There is no sampling distribution, no repeated trials, no standard error to compute. A p-value or confidence interval computed from a single deterministic run would be meaningless — there is nothing to compute it against.

What Phase 4A *can* establish, and what this document defines instead, is **practical significance**: is an observed gap large enough, relative to gaps this same harness already produces from changes that are NOT the effect under study, to be distinguishable from that background variation? This is the same spirit as a noise floor in signal processing — not a statistical test, but an empirically-grounded bar.

## 2. Noise floor — empirically derived from Phase 3's own data

Rather than inventing a noise-floor number, this section derives one from real, already-collected evidence: how much did TWR/MaxDD move in Phase 3G's sensitivity sweep from changes that are either (a) expected to have only a small, known effect, or (b) surprisingly did not move a metric much despite a real, structural change occurring.

| Observed case | Change | TWR gap | MaxDD gap | Interpretation |
|---|---|---:|---:|---|
| Interest rate 5%→8% (`docs/results/PHASE3_SENSITIVITY_RESULTS.json`, interest_sensitivity) | +3 percentage points of financing cost, a real, structural, expected-to-matter change | -0.24pp | -0.08pp | A genuine, real cost mechanism, moving in the expected direction, produces gaps well under 0.5pp for a 3-point rate change |
| Model C drawdown_trigger_pct 15%→12.5% (same file, model_c_sensitivity) | Trigger fires 7 times instead of 1 — a real, structural change in how often the mechanism activates | -0.50pp | 0.00pp | 7 real trigger activations moved MaxDD by exactly zero and TWR by half a point |
| Model C drawdown_trigger_pct 15%→10% | Trigger fires 10 times instead of 1 | -0.56pp | -0.00pp | 10 real trigger activations, still ~0pp MaxDD impact |

**Noise floor, set from this evidence: gaps smaller than 0.5 percentage points (TWR or MaxDD) are treated as within the harness's own background variation** — not distinguishable, on this evidence, from a mechanism that is real but simply doesn't move the portfolio-level number much. This is a conservative (i.e., harder-to-clear) floor: the interest-rate case shows a *known-real* mechanism producing sub-0.5pp gaps, so a Phase 4A finding below 0.5pp cannot be confidently attributed to concentration rather than to ordinary harness-level variation of this same size.

This floor applies to `ann_twr_pct`, `max_drawdown_pct`, and `cagr_pct` gaps. It does not apply to `n_reset_activations`/event counts (§3) or to `worst_case_concentration_impact_pct` (§4), each of which needs its own materiality treatment because they are not continuously-varying return/drawdown percentages.

## 3. Materiality threshold — primary risk metric (MaxDD gap)

**A MaxDD gap of ≥2.0 percentage points, between the relevant comparison pair, is required for that specific criterion to count as material.**

Chosen for consistency with Scenario D's already-approved decision threshold (`docs/PHASE3_SCENARIO_MANIFEST.md` §1: "2.0 percentage points... a decision threshold, not a proof threshold"), not derived fresh — reusing an already-approved bar is more defensible than inventing a second, different number for a closely related question, and this repo's standing practice (`docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.D) already reasoned that higher-mechanism-risk questions deserve at least this bar, sometimes stricter. Concentration-and-margin interaction is at least as consequential as the repayment-model question that bar was originally set for.

Gaps between 0.5pp (the noise floor, §2) and 2.0pp are **reported but not counted as material** — visible in the results, explicitly labeled "suggestive, below the materiality bar," neither dismissed nor treated as evidence.

## 4. Materiality threshold — single-name/cluster decomposition gap

`worst_case_concentration_impact()`'s output is not a return/drawdown percentage in the same sense as §2/§3 — it's a magnitude-of-impact figure derived from a position's own historical worst drawdown scaled by leverage (`docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md`'s framing, and `t1t2_trim_backtest.md`'s NVDA precedent: 2.14x target, -66.4% own drawdown, decomposed against the account's 1.44x leverage). The materiality question here is: **does the single-name-decomposed figure exceed the portfolio-level MaxDD by more than the §3 threshold (2.0pp) applied to this comparison specifically** — i.e., is the "hidden" risk a single-name view reveals large enough, relative to what the portfolio-level number already shows, to be a materially different picture, not just a modestly bigger one.

## 5. Materiality threshold — forced-deleveraging events

**A single, isolated forced-deleveraging event is NOT material by itself.** This directly answers the approval feedback's example question ("does one forced deleveraging event count?"). No — for two independent reasons:

1. Phase 3G's own evidence (§2's table) shows that even 7-10 real trigger activations produced ~0pp portfolio-level MaxDD movement — so event count alone, without a corroborating MaxDD/TWR gap clearing §2/§3's thresholds, does not establish materiality on its own.
2. A single event could plausibly be a construction artifact (a single day's price noise crossing a threshold) rather than a genuine risk-relevant episode.

**"Repeated" is defined as: ≥3 forced-deleveraging events within a single stress episode, OR forced-deleveraging events occurring in ≥2 of the 4 required stress cases** (`docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md` §4). This threshold is itself calibrated against the Phase 3G evidence: 7-10 activations (well above 3) still failed to move MaxDD materially in that context, so event-count materiality is treated as a **necessary, not sufficient**, condition — it must combine with a §3/§4 gap clearing its own threshold, exactly matching `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6's existing "all conditions must hold, not just one" structure. Event count and drawdown-gap materiality are companion criteria, not substitutes for each other.

## 6. Materiality threshold — time above risk thresholds

**A risk-threshold breach (leverage above a stated level, or concentration above a stated level) occupying fewer than 5% of the scenario's total simulated trading days is treated as non-material** — a brief, transient crossing, not a sustained risk exposure. This mirrors `time_near_leverage_cap_pct_proxy`'s existing design intent (a *proportion of the window*, not a raw day count, since raw day counts aren't comparable across scenarios with different total lengths).

## 7. Materiality threshold — recovery time

**Recovery time in a concentration/margin-stressed scenario must exceed the equivalent unstressed or lower-concentration baseline's own recovery time by at least 50% (1.5×), or by an absolute minimum of 20 trading days if the baseline has no comparable recovery episode to measure against, to be treated as material.** A small numeric difference in "days back to a new high" for a noisy simulated price series is easily within ordinary path-dependent variation; a threshold proportional to the baseline (rather than an absolute number alone) avoids treating a short baseline recovery's small absolute difference as equivalent to a long baseline recovery's same absolute difference.

## 8. How these thresholds combine with the three-way outcome framework

### 8a. Criteria as used for Phase 4A (historical record — unchanged)

Applying `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6 (as revised) directly, this is the gate `run_phase4a_research.py` actually implemented and that produced Phase 4A's recorded "Evidence inconclusive" outcome (`docs/PHASE4A_RESEARCH_REPORT.md`, `docs/results/PHASE4A_RESEARCH_RESULTS.json`):

- **Evidence supports** requires the §3/§4 gap threshold (2.0pp) to clear AND the §5 event-repetition threshold to clear, together, not either alone — per §5's explicit "necessary, not sufficient" framing.
- **Evidence does not support** requires every relevant gap to fall at or below the §2 noise floor (0.5pp), consistently across both construction methods (synthetic and drift, per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §1).
- **Evidence inconclusive** covers everything in between: gaps in the 0.5pp-2.0pp suggestive band, results that clear a threshold under only one construction method, or event counts that clear §5's repetition bar without a corresponding gap clearing §3/§4 (echoing the real Phase 3G Model C pattern this document's own noise floor was derived from).

This subsection is preserved as-is and is not edited by 8b below — it is the historical description of what actually governed Phase 4A's result.

### 8b. Adopted criteria for future research cycles (2026-07-17)

Per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s governance review, approved for **future** research only (see that document's §6 non-retroactivity statement and its new "Adoption" section below):

**Previous criteria:** material gap AND repeated forced-deleveraging events.

**Future criteria:** material gap AND (repeated forced-deleveraging events **OR** material threshold-exposure degradation, using the §6 time-above-threshold bar above — a risk-threshold breach occupying ≥5% of the scenario's simulated trading days).

Rationale (from `docs/PHASE4A_OUTCOME_GATE_REVIEW.md` §4): the MaxDD-gap leg of the gate worked as designed and is unchanged. The event-count leg, used alone as the sole second condition, was too narrow — a coverage problem, not a threshold-calibration problem. `forced_deleveraging_events()` detects only one specific failure mode (a passive breach: leverage exceeding the cap because gross fell *after* debt was already drawn, a narrow sequence given `simulate()`'s own allocation step already clips new draws to the cap in real time). Phase 4A's own already-collected time-above-threshold data showed a much larger, more consistent signal across every concentrated arm (100.0% of simulated days above the reference threshold once concentrated, versus 61.7%/14.0% at baseline) than the event-count metric could ever produce in this harness's mechanics — a real, relevant, already-materiality-defined (§6) signal that the original gate simply never consulted.

The revised second condition preserves the "necessary, not sufficient" structure exactly — a material MaxDD gap alone still does not qualify as "Evidence supports" on its own; it must still be corroborated by at least one of the two now-available exposure signals, not by the MaxDD gap in isolation.

**This is a future research-methodology change, not a retroactive reclassification.** Phase 4A's own recorded outcome ("Evidence inconclusive") is not recomputed, and this adoption does not edit `docs/PHASE4A_RESEARCH_REPORT.md` or `docs/results/PHASE4A_RESEARCH_RESULTS.json` in any way — see `docs/PHASE4A_OUTCOME_GATE_REVIEW.md` §6 for the full non-retroactivity reasoning, which this adoption inherits unchanged. A gate is fixed before results for whichever research cycle uses it; adopting a revised gate now applies it prospectively, the same discipline every pre-committed threshold in this project has followed since `rung_backtest.md`.

## 9. These thresholds are fixed, not adjustable after seeing results

Consistent with every pre-committed-threshold backtest in this repo: once Phase 4A execution begins, none of the numbers in this document may be revised to fit an observed result. If a threshold turns out to be poorly calibrated once real Phase 4A data exists (e.g., the 0.5pp noise floor proves too loose or too tight against Phase 4A's own specific metric distributions, which may differ from Phase 3G's), that is itself a finding to report honestly — a reason to note the threshold's limitation in the results writeup, not a reason to silently move it.

---

## What this document deliberately does not do

- Does not run any simulation or produce any Phase 4A result.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py`.
- Does not invent thresholds without a stated reason — every number here is either reused from an already-approved Phase 3 bar (2.0pp) or derived from real, cited Phase 3G evidence (0.5pp noise floor, the 3-event/2-stress-case repetition bar).
- Does not resolve `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §1/§2/§6's own approval-required items — this document only adds the materiality layer those items' criteria depend on.

Stopping here. Awaiting approval on this document alongside `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §1, §2a, §6, and §7 before any Phase 4A execution harness is built.
