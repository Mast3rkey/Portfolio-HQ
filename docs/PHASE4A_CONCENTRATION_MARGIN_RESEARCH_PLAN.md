# Phase 4A: Concentration × Margin Research Plan

> **⚠️ Hypothetical, simulated — a design document, not a result.** No simulation described here has been run. Every scenario this plan eventually produces will simulate a synthetic account through real historical prices — never this account's real history. When this plan executes, every output carries `HYPOTHETICAL_LABEL` and passes `margin_simulation.py`'s banned-phrase enforcement, the same discipline Phase 3 established. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies here too.

_Written 2026-07-17, per `docs/PHASE4_READINESS_REVIEW.md`'s finding that concentration interaction is the single largest gap in the Phase 3 evidence base ("zero code exists... not a partial result, a complete absence of evidence"). No code written. No production files touched — `allocate.py`, `targets.yaml`, `holdings.yaml`, and `margin_state.py` are not modified by this document._

---

## 1. Research question

**Does concentration materially change the risk profile of margin usage?**

More precisely: `margin_state.py`'s existing `concentration_risk_score()` already scores portfolio-level concentration (cluster-cap proximity, T1/T2 ceiling proximity) as an input to margin-state classification — but that scoring only ever affects the *display state* (Phase 2D confirmed this is display-only), never `margin_capacity()`'s actual deployable capacity, and it operates on cluster/tier aggregates, never a single name's own worst-case behavior. This research asks whether that portfolio-level view is *sufficient*, or whether it systematically understates risk that a single-name-level view would catch — the same failure mode `t1t2_trim_backtest.md` already found once, in an unrelated context (portfolio-level MaxDD too smooth to show NVDA's own -66.4% peak-to-trough), and that `docs/PHASE3_SENSITIVITY_RESULTS.md`'s Model C sweep arguably showed again (portfolio-level MaxDD unchanged across four different trigger-activation counts).

This is a diagnostic question, not a design question. The plan does not ask "how should concentration affect margin capacity" — it asks "does it need to, on the evidence."

## 2. Test design

Four scenarios, sharing the same substrate wherever possible (universe, window, deposit cadence, weights) so only the concentration/leverage dimension named in each scenario's own letter varies — same discipline as Phase 3's Scenario A-D shared-configuration pattern (`docs/PHASE3C_SCENARIO_CONFIGURATION.md`).

**A. Current portfolio construction (control).** The existing 63-ticker T1/T2/ETF/band/spec universe and tier weights (`backtest_regime.TIER_WEIGHTS`, matching `targets.yaml` live), unlevered or at the standard 1.8x cap (both variants run, matching Phase 3's own A/B pair) — this is Phase 3E's Scenario A/B, reused as this plan's baseline rather than re-derived, exactly as Phase 3G reused and verified Phase 3E's Scenario B for its interest-rate baseline.

**B. Same portfolio with increased concentration.** The same universe and starting weights, but with one or more positions' weights artificially inflated (a synthetic concentration increase — e.g., doubling or tripling a single T1 name's target weight while proportionally reducing others, or simulating a name that was never trimmed back to target the way `t1t2_trim_backtest.md`'s Arm A — no T1/T2 trim — showed T1 drifting to 42.1% of book in the real account). This isolates concentration's effect *without* touching leverage — same leverage cap as Scenario A, only the weight distribution changes.

**C. Same portfolio with concentrated largest-holding stress.** Scenario B's concentrated weighting, run through a synthetic or historically-anchored stress path specifically on the largest/most concentrated holding (not the whole portfolio) — isolates what happens when the concentration risk actually materializes as a single-name event, independent of margin.

**D. Same portfolio with margin exposure during concentration stress.** Scenario C's concentrated-holding stress, but with margin active (1.8x cap, matching Scenario A's levered variant) — the combination this whole research question exists to test. This is where the "does portfolio-level margin state understate risk" question gets its actual test: does `time_near_leverage_cap_pct_proxy` or `concentration_risk_score()`'s existing portfolio-level view look calm while a single concentrated position under leverage is actually in forced-liquidation territory (the same disqualifying condition `t1t2_trim_backtest.md`'s NVDA decomposition already established at the account's real leverage level)?

## 3. Metrics

Per scenario, per arm, superset of Phase 3's existing metric set (`SimulationResult.metrics()`) plus concentration-specific additions:

| Metric | Source | Notes |
|---|---|---|
| `ann_twr_pct` | `twr_annualized()` (existing, reused) | |
| `cagr_pct` | `cagr()` (existing, reused) | |
| `max_drawdown_pct` | `max_drawdown()` (existing, reused) | Portfolio-level — expected to be the metric that UNDERSTATES risk if this research's hypothesis holds; report alongside single-name decomposition, never alone |
| Margin leverage path | `leverage_series` (existing) | Full daily series, not just final/summary — needed to see whether leverage spikes coincide with the concentration-stress episode specifically |
| Forced deleveraging events | New derived metric, same pattern as `phase3g_lib.ModelCTriggerLogger` | Count and timing of any point where simulated leverage would breach the 1.8x cap or force a sell under stress — reuses `margin_capacity()`'s existing leverage-cap math conceptually (re-derived in the harness per `margin_simulation.py`'s existing isolation pattern, not imported from `allocate.py`) |
| Time above risk thresholds | New derived metric | Days spent above configurable leverage/concentration thresholds (e.g., `time_near_leverage_cap_pct_proxy`'s existing pattern, extended to also track cluster/single-name concentration thresholds) |
| Largest single-name contribution to loss | `worst_case_concentration_impact()` (existing, `margin_simulation.py`) | The exact decomposition method already built and tested in Phase 3B — this research is close to its first real application beyond the unit tests |
| Recovery time | New derived metric | Days from a stress episode's trough back to the pre-stress high-water mark — same HWM-tracking concept `ModelBProfitHarvest`/`ModelCRiskReset` already use, applied here as a measurement, not a trigger |

No new metric requires modifying `margin_simulation.py`'s existing classes — every "new derived metric" above is achievable the same way Phase 3G's `phase3g_lib.py` extracted derived metrics from already-produced `SimulationResult` objects (events, `leverage_series`, `book_values`) without touching the simulation engine itself. This plan does not commit to file-naming or module structure for that derivation layer — that is an implementation detail for the (separate, future, not-yet-approved) execution phase.

## 4. Required stress cases

Four cases, each applied within Scenarios C/D above (Scenarios A/B carry no stress event by design — they establish the concentration baseline before any stress is applied):

1. **Single largest holding drawdown.** The concentrated position (Scenario B/C's inflated-weight name) undergoes a severe, isolated decline while the rest of the portfolio is comparatively flat — the cleanest test of single-name concentration risk in isolation.
2. **Multiple correlated holdings drawdown.** Extends case 1 to a cluster (e.g., simulating the existing `semis` cluster — ASML/TSM/NVDA/AVGO/AMD/MU/MRVL/KLAC/LRCX/AMAT/WDC/INTC/SKHY — moving together) declining together, testing whether the *existing* cluster-cap concept (already live in `targets.yaml`, unmodified by this plan) is itself sufficient, or whether a correlated-but-uncapped or partially-capped group still produces understated portfolio-level risk.
3. **Market drawdown with concentrated exposure.** A broad market decline (all positions falling, not just the concentrated one/cluster) layered on top of the Scenario B/C concentration — tests whether concentration risk compounds with, rather than is dominated by, systematic risk. This is the scenario closest to a real bear-market stress test, and the one Phase 3's own window (2021-2026, "one real but brief bear stretch," per every prior document's standing caveat) is weakest at supplying real historical material for — flagged here, addressed in §6.
4. **Concentration increase without leverage increase.** The pure isolation case: weights become more concentrated (Scenario B) but the leverage cap and actual margin usage stay exactly as in Scenario A — tests whether concentration alone (with no margin change at all) already produces a risk-profile difference portfolio-level metrics would miss, before margin is even added to the picture (Scenario D). This case directly probes the research question's cleanest form.

## 5. Explicitly avoid

Restated as hard constraints on this research, not soft preferences — matching the discipline `docs/PHASE3_SENSITIVITY_PLAN.md` and `docs/PHASE3_DECISION_GATE.md` already established for Model B/C:

- **Do not create a concentration penalty formula.** This research measures whether a gap exists between portfolio-level and single-name-level risk views — it does not design a formula to close that gap. If a gap is found, closing it is a separate, later, explicitly-approved design effort (the same sequencing Phase 3 followed: evidence framework → manifest → implementation → execution → sensitivity → readiness review, each its own approval gate).
- **Do not add new margin rules.** `margin_capacity()` and `margin_state.py`'s classifier are read-only reference points for this research, not modification targets. This plan produces evidence about them, not changes to them.
- **Do not change cluster caps.** The existing semis/power_infra/oil caps (25%/20%/20%, `targets.yaml`) are used as-is, as real reference points (e.g., in stress case 2), never adjusted as part of this research.
- **Do not select an optimal concentration level.** There is no "right" concentration level this research is designed to find. Scenario B's concentration increase is a stress-testing device, not a proposal for what the portfolio's actual concentration should be.

## 6. Available data, missing data, assumptions requiring approval

### Available
- Real historical price data for all 65 roster tickers (`data/backtest/*.json`), same substrate every Phase 3 scenario used.
- Real cluster definitions and caps (`targets.yaml`'s `caps.clusters`) — semis (13 names, 25% cap), power_infra (4 names, 20% cap), oil (2 names, 20% cap) — usable as-is for stress case 2's "existing cluster-cap sufficiency" question.
- Real T1 tier composition (9 names: ASML, TSM, MSFT, GOOGL, META, NVDA, GEV, LLY, V) — a real, already-flagged concentration point (`CLAUDE.md`'s Decisions Log: "T1 is already 7-of-9 names one AI-infrastructure trade," correlation-scanned at 0.302 avg and explicitly declined as a cluster-cap candidate on weak-mechanism grounds, per the "T1 AI-infra cluster cap: scanned and declined" entry) — a documented, real starting point for Scenario B's concentration construction, not an invented one.
- `worst_case_concentration_impact()` and the single-name decomposition method, already built and unit-tested in Phase 3B (`margin_simulation.py`, `test_margin_simulation.py`).
- NVDA's own real historical decomposition already computed once (`t1t2_trim_backtest.md`: 2.14x target, -66.4% peak-to-trough at the account's 1.44x leverage) — a real, reusable reference point for calibrating what a "severe single-name stress" looks like in this universe, not a number this plan needs to re-derive from scratch.

### Missing
- **A concentration-scoring integration in `margin_simulation.py`.** `concentration_risk_score()` exists in `margin_state.py` (the live classifier), not in the simulation harness — this research needs its own concentration-tracking mechanism inside the simulation engine (Scenario B/C/D all require knowing simulated cluster/single-name concentration at each point in time), which does not currently exist there. This is new harness work the execution phase will need, not something this plan can borrow from Phase 2D's integration (that integration is display-only, in `allocate.py`, and explicitly out of scope to modify here).
- **A defined method for constructing the "increased concentration" weighting in Scenario B.** Multiple reasonable constructions exist (double one name's weight, let a name run un-trimmed the way T1 did in the real account, synthetically add a new maximally-correlated position) — this plan does not choose one; that choice is a design decision the execution phase needs, requiring its own approval (see below).
- **A defined severity for the stress cases (§4).** "Severe decline" is not yet quantified — whether stress case 1 uses NVDA's real -66.4% figure, a different real historical single-name drawdown from the 63-ticker universe, or a synthetic constructed shock is undecided.
- **Correlation data for constructing stress case 2's "multiple correlated holdings" beyond the already-scanned semis/power_infra/oil clusters** — if this research wants to test an *uncapped* correlated group (to see whether the cluster-cap concept itself has coverage gaps), a fresh correlation scan would be needed, following the same one-time-scan methodology `CLAUDE.md`'s Decisions Log already used for semis/power_infra/oil/the declined T1 AI-infra cluster — not yet performed for this purpose.
- **A window or synthetic construction for stress case 3** that actually supplies a severe systematic drawdown — Phase 3's 2021-2026 window is, per every prior document's standing caveat, weak on this specifically. Whether to extend the data window (if older cached data exists), use a different historical stretch, or construct a synthetic shock is undecided.

### Assumptions requiring approval before execution
1. Which construction method Scenario B uses for "increased concentration" (see Missing, above) — a real design choice, not a technical detail.
2. What severity and source (real historical vs. synthetic) each of the four stress cases uses.
3. Whether stress case 2's correlated-group construction reuses the existing capped clusters only, or extends to a fresh, uncapped correlation scan.
4. How "forced deleveraging" is operationalized as a measurable event in the harness (a specific leverage-breach definition, re-derived independently the way `_leverage_capped_margin()` already is, not imported from `allocate.py`).
5. Whether Scenario D's margin exposure uses the same 1.8x cap as Phase 3, or a range — and if a range, this reopens the "not a parameter sweep for optimization" constraint (§5) that must be explicitly re-affirmed before any such range is run.

None of these five are decided by this document. Each requires its own explicit approval, the same gating pattern `docs/PHASE3_SCENARIO_MANIFEST.md` used for Model B/C's mechanics before Phase 3D implemented them.

---

## What this plan deliberately does not do

- Does not implement any concentration-scoring code in `margin_simulation.py` or anywhere else.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py`.
- Does not choose Scenario B's concentration-construction method, the stress cases' severity, or any other unresolved item in §6 — those remain open, named, and awaiting approval.
- Does not propose a concentration penalty formula, a margin rule, a cluster-cap change, or an "optimal" concentration level, per §5.
- Does not run any simulation. No code, no tests, no execution.

Stopping here. This is a research design document only. Awaiting approval and resolution of §6's open items before any Phase 4A execution work begins.
