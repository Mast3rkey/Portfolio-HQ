# Phase 4A Outcome Gate Review

> **⚠️ Hypothetical, simulated — a governance review, not a re-run.** This document reviews whether Phase 4A's evidence-classification gate measured the intended research question. It does not run any simulation, does not change any code, and does not retroactively change Phase 4A's recorded outcome. Every figure cited below is quoted from `docs/PHASE4A_RESEARCH_REPORT.md` and `docs/results/PHASE4A_RESEARCH_RESULTS.json` as already produced and committed.

_Written 2026-07-17, per `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 3 ("Re-examine the 'Evidence supports' AND-gate's second condition"), promoted to its own governance review at explicit request rather than folded into a future research cycle. Documentation only — no code, no tests, no production files touched._

---

## 1. Original Phase 4A research question

Per `docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md` §1: **"Does concentration materially change the risk profile of margin usage?"** — more precisely, whether `margin_state.py`'s existing portfolio-level concentration scoring (already established as display-only, never affecting real deployable capacity) understates risk that a single-name-level view would catch, the same failure mode `t1t2_trim_backtest.md`'s NVDA decomposition already demonstrated once in a different context, and that `docs/PHASE3_SENSITIVITY_RESULTS.md`'s Model C sweep arguably showed a second time (flat portfolio MaxDD despite materially differing trigger-activation counts).

This is explicitly framed as a **diagnostic** question ("does portfolio-level risk measurement need to account for concentration, on the evidence"), not a design question about what to do if the answer is yes.

## 2. Original success criteria

Per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6 (as revised to the three-way outcome framework) and `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §8, the criteria actually implemented in `run_phase4a_research.py` and recorded in `docs/results/PHASE4A_RESEARCH_RESULTS.json`:

- **"Evidence supports"** required a material MaxDD gap (≥2.0pp, per the materiality doc's §3, itself reused from Scenario D's already-approved decision threshold) **AND** repeated forced-deleveraging events (per §5's definition: ≥3 events in one stress case, or events in ≥2 of the 4 required stress cases) — both conditions, not either alone, per §5's explicit "necessary, not sufficient" framing for event count.
- **"Evidence does not support"** required every relevant gap at or below the 0.5pp noise floor, with no event repetition.
- **"Evidence inconclusive"** covered everything else.

Recovery-time materiality (§7 of the materiality doc: ≥1.5x baseline or ≥20 absolute trading days) was collected and reported but **was never wired into the outcome-gate's supports/does-not-support/inconclusive logic** — `run_phase4a_research.py`'s `write_outputs()` computes `recovery_material_d_hist`/`recovery_material_d_hyp` and includes them in the JSON payload and the report's narrative text, but the `outcome` variable itself is derived from `any_material_gap and repeated` (MaxDD gap + event count only). This is confirmed directly from the driver's source, not inferred.

**Time-above-threshold exposure** (§6 of the materiality doc — the ≥5%-of-days floor for a leverage/concentration threshold breach to count as material exposure) was likewise collected — reported in `docs/PHASE4A_RESEARCH_REPORT.md`'s "Time above concentration thresholds" table — but **was also never wired into the outcome gate at all.** No materiality classification (per §6's own 5%-of-days floor) was even applied to these numbers in the driver; they were reported as raw percentages only.

## 3. Actual observed evidence

Quoted directly from `docs/results/PHASE4A_RESEARCH_RESULTS.json`'s `materiality_evaluation` block and `docs/PHASE4A_RESEARCH_REPORT.md`:

### MaxDD differences

| Comparison | Gap | Classification |
|---|---:|---|
| B (concentration alone) vs. A (control) | −0.65pp | suggestive |
| D-hist (concentration + margin + historical stress) vs. B | **−5.14pp** | **material** |
| D-hyp (concentration + margin + hypothetical stress) vs. B | −0.91pp | suggestive |

The core research-question comparison (adding margin to an already-concentrated position under real stress) **did clear the material threshold**, by a wide margin (−5.14pp against a 2.0pp bar — more than 2.5x the threshold, not a borderline case).

### Threshold exposure (time-above-threshold)

| Scenario | NVDA time above 1.5x target share | Semis time above 25% cluster cap |
|---|---:|---:|
| A (control) | 61.7% | 14.0% |
| B (synthetic concentration) | 100.0% | 100.0% |
| D (concentration + margin) | 100.0% | 100.0% |

Both concentration constructions (single-name and cluster) show the account spending **100% of simulated days** above the reused reference thresholds once concentration is introduced, versus 61.7%/14.0% at baseline — a large, unambiguous shift by any reasonable reading, and one that clears the materiality doc's own §6 floor (≥5% of days) by a wide margin in every arm where it was measured. This metric was never given a pass/fail classification in the driver, but the raw numbers are not ambiguous.

### Forced-deleveraging events

**Zero, in every scenario, every stress case:** `stress_case_1_historical=0`, `stress_case_1_hypothetical=0`, `stress_case_2_cluster=0`, `stress_case_4_concentration_only=0` (the last is zero by construction — that stress case is defined as unlevered, so no leverage cap exists to breach). `events_repeated: False`. This was the sole disqualifying factor in the "Evidence inconclusive" determination — the MaxDD condition cleared, the event condition did not.

### Recovery metrics

D-hist recovery: 33 simulated trading days. D-hyp recovery: 28 days. A (baseline) recovery: 25 days. Neither comparison (33 vs. 25, or 28 vs. 25) reaches the materiality doc's §7 bar (≥1.5x baseline, or ≥20 absolute days when no baseline exists — here a baseline does exist, so the relative test applies: 33/25 ≈ 1.32x, 28/25 = 1.12x, both below 1.5x). Both correctly classified `False` by `is_recovery_material()`.

## 4. Did the gate capture the intended risk?

Working through the three framings the task asks for directly, in order:

### Did it capture the intended risk?

**Partially.** The MaxDD-gap leg of the gate worked exactly as designed and produced a real, material, unambiguous signal (−5.14pp, more than double the threshold) on the one comparison that most directly represents the research question (concentration + margin + real historical stress, versus concentration alone). That is a genuine success of the gate's first condition — it did not fail to detect the effect where the effect was, by this measure, clearly present.

### Was it too narrow?

**Yes, in one specific, identifiable way.** The gate's second condition (forced-deleveraging event repetition) operationalizes only one of at least three plausible "the risk materialized" signals this research plan itself specified as required metrics (§3 of the research plan: margin leverage path / forced deleveraging events / time above risk thresholds / recovery time, alongside MaxDD). Of those, only forced-deleveraging events was made a *gating* condition; time-above-threshold and recovery time were collected and reported but never given decisive weight. This is not a threshold-calibration problem (the 2.0pp/0.5pp/repetition-count numbers from `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` are not being questioned here) — it is a **coverage** problem: the gate used one out of several already-collected, relevant signals as its second necessary condition, and the one it picked happens to be structurally hard to trigger in this harness for a reason unrelated to whether real risk materialized.

Specifically: `forced_deleveraging_events()` detects a *passive* breach — leverage exceeding the cap because gross fell after debt was already drawn. But `simulate()`'s own allocation step already clips every new margin draw to the leverage cap in real time (`_leverage_capped_margin()`, called on every deposit day) — so a passive breach requires a very particular sequence (debt drawn while concentrated, then a price decline severe enough to push leverage over the cap on an *already-existing* debt balance) rather than any general "the account is under elevated risk" condition. The time-above-threshold metric, by contrast, directly captures sustained elevated exposure (100% of days above the reference threshold, vs. 61.7%/14.0% at baseline) without requiring that specific sequence — and shows a much larger, more consistent signal across every concentrated arm than the event-count metric ever could, structurally, in this harness's mechanics.

### Does it remain appropriate as designed?

**Not without change, for future research using this pattern.** The MaxDD-gap leg is sound and should be retained. The event-count leg, as the *sole* second condition, is too narrow given what this harness can and cannot produce — it is not that repetition-of-events is a bad idea, it is that forced-deleveraging events specifically is too narrow a definition of "risk materializing" to serve alone as the swing factor between "supports" and "inconclusive," when two other already-collected, already-materiality-classified-in-spirit metrics (time-above-threshold, recovery time) were sitting unused in the same JSON output.

## 5. Outcome category

**Modify future research criteria.**

Not "Keep current gate" — the coverage gap identified in §4 is specific, identifiable, and grounded directly in data this research itself already collected, not a speculative concern. Not "Evidence remains insufficient" — this is not a data problem (more scenarios, more windows, more constructions); it is a problem with which already-collected signals the gate's second condition was allowed to use. Sufficient evidence exists to identify the fix; it just was not implemented in the first pass.

**Recommended modification (for a future, separately-approved research cycle — not implemented here):** widen the "Evidence supports" second condition from *forced-deleveraging events alone* to *forced-deleveraging events OR time-above-threshold materiality* (using the materiality doc's own already-defined §6 floor, ≥5% of days above a reference threshold), evaluated with the same "material MaxDD gap AND (at least one corroborating exposure signal)" structure the original gate used — preserving the "necessary but not sufficient" discipline (a MaxDD gap alone still would not be enough) while no longer relying on a single narrow event-type as the only possible corroboration.

## 6. Explicit non-retroactivity statement

**Phase 4A's recorded outcome — "Evidence inconclusive" — is not changed by this review and remains the official result of that research cycle.** `docs/PHASE4A_RESEARCH_REPORT.md` and `docs/results/PHASE4A_RESEARCH_RESULTS.json` are not edited by this document. This review identifies that the gate *used to produce* that outcome had a coverage gap worth fixing for future work — it does not assert that Phase 4A's own classification was computed incorrectly given the gate as it was actually built and pre-committed, nor does it re-run Phase 4A's data through a hypothetical revised gate to produce an alternate headline number. Doing so would itself violate the same pre-committed-threshold discipline this project has followed since `rung_backtest.md` — a gate is fixed before results, not adjusted after, even when the adjustment is well-motivated. If a revised gate is approved for future use, it applies to *future* research cycles, not a retroactive recomputation of this one.

## What this review deliberately does not do

- Does not modify `run_phase4a_research.py`, `phase4a_lib.py`, `margin_simulation.py`, or any other code.
- Does not re-run any simulation.
- Does not change Phase 4A's recorded outcome, report, or JSON output.
- Does not propose any new production rule, margin rule, or concentration control.
- Does not itself implement the recommended gate modification — that is future work, gated on its own explicit approval, per the same discipline every other change in this project has followed.

Stopping here. Awaiting direction on whether to adopt the "modify future research criteria" recommendation before any future Phase 4-family research cycle.

## Adoption (2026-07-17)

**The "Modify future research criteria" recommendation above is adopted, for future research cycles only.** Recorded formally in `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §8b and `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6's update note — both updated alongside this adoption, both preserving §8a/the original §6 text as the unedited historical record of what actually governed Phase 4A.

**Previous criteria** (unchanged historical record, still what produced Phase 4A's "Evidence inconclusive" outcome): material gap AND repeated forced-deleveraging events.

**Future criteria** (effective for research cycles after this adoption): material gap AND (repeated forced-deleveraging events **OR** material threshold-exposure degradation, per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §6).

This adoption is explicitly a **future research-methodology change, not a retroactive reclassification** — restating §6 above: `docs/PHASE4A_RESEARCH_REPORT.md` and `docs/results/PHASE4A_RESEARCH_RESULTS.json` are not edited, not recomputed, and Phase 4A's recorded outcome is not altered by this adoption. No code was changed to record this adoption. No production file, and no entry in `CLAUDE.md`'s Decisions Log, was touched — this governs future *research methodology* only, not production doctrine, and remains subject to the same "any finding requires its own separate approval before affecting production" rule every other document in this project has stated.
