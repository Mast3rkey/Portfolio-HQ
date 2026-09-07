# Transaction Cost Sensitivity Analysis — Research Plan

> **⚠️ Hypothetical, simulated — a design document, not a result.** No cost analysis has been run. Every number this plan will eventually produce describes a synthetic $0-start account simulated through real historical prices, with a further hypothetical cost assumption layered on top — never a claim about this account's real trading costs. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies to every output this plan produces.

_Written 2026-07-17, per `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 1 ("Transaction cost sensitivity for repayment-model turnover"), ranked highest priority in that backlog. Documentation only — no code, no tests, no production files touched. Do not implement until this plan is approved._

---

## 1. Sources reviewed

`docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` (item 1's scoping: "Small effort... apply a disclosed bps assumption to the already-measured turnover totals... pure post-processing of data already collected"), `docs/results/PHASE3_MODEL_B_ANALYSIS.md` (the existing turnover measurement this plan extends), `docs/PHASE3_SENSITIVITY_PLAN.md` (Model B's original 10%/25%/50% `repay_fraction` sweep design, whose already-collected results this plan reuses), `docs/PHASE4_READINESS_REVIEW.md` §"Transaction cost sensitivity" (the original flag: "does not exist anywhere in this repo... a real, quantifiable, currently-invisible cost"). Also read `margin_simulation.py`'s `_fund_repayment()` directly to confirm the exact trading mechanics being priced (see §3 below).

## 2. Goal

Determine how transaction costs affect the **interpretation** of Model B's already-observed repayment behavior — not whether Model B should be adopted, tuned, or preferred at any particular `repay_fraction`. This is a re-interpretation of existing evidence under a new, disclosed assumption, not a new experiment.

## 3. What is actually being priced

`_fund_repayment()` (read directly for this plan, not assumed): every Model B repayment event first draws from idle cash, then — since this harness's `min_lot=$1` keeps idle cash near-zero after allocation (`docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4's existing finding) — funds the remainder via a **pro-rata trim across every held position simultaneously**. This means each of the 296 "events" recorded at `repay_fraction=0.25` is not one trade; it is a simultaneous partial sell across however many of the 63 tickers were held and priced that day. This is a real mechanical fact about the harness, confirmed by reading the function, not an assumption.

This matters for cost modeling because two different cost bases are possible:

- **Dollar-volume-based cost** (spread/slippage, expressed in basis points of dollars traded) — insensitive to how many individual tickers a given dollar amount was spread across. This is what this plan will price (§5).
- **Per-trade / fragmentation-sensitive cost** (a minimum fee or spread cost per individual ticker leg) — would require knowing how many tickers were touched per event, which isn't currently logged anywhere (not in `SimulationResult.events`, which records only `{"day", "kind", "amount", "source"}` per event, aggregated across all tickers touched that day). **This plan does not attempt this** — flagged explicitly as an unaddressed dimension, not silently ignored (see §8).

## 4. Why Robinhood's real commission structure doesn't need modeling

`CLAUDE.md`'s doctrine states the account is a Robinhood cash/margin account. Robinhood charges $0 commission on stock/ETF trades — so the "transaction cost" this analysis needs to model is **not** a commission fee (which is genuinely zero and needs no sensitivity range), but the **bid-ask spread and slippage** cost implicit in any trade, which Robinhood's $0-commission structure does not eliminate. `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4 already made this same distinction implicitly ("no transaction-cost or tax-impact model exists... both are silent on trading costs by design, per the account's cash brokerage assumption") — this plan makes it explicit rather than continuing to leave it implicit.

## 5. Cost assumptions to test

Three tiers, applied as basis points (bps) of dollar volume traded (i.e., of each repayment event's `amount`, per `SimulationResult.events`):

| Tier | Value | Why chosen |
|---|---:|---|
| **0 bps** | 0.00% | The control — reproduces every already-published Phase 3 number exactly. Also the closest thing to a **Known** value in this analysis: Robinhood's commission genuinely is $0, so a pure-commission-only cost model would be 0 bps. Included so every other tier's effect is measured as a delta from an already-verified baseline, not a delta from an assumed nonzero floor. |
| **5 bps** | 0.05% | A conservative, low-end spread/slippage estimate for large-cap, high-liquidity names — most of the 63-ticker universe (T1/T2 mega-caps, major ETFs) trades with spreads well under this in practice. Chosen as the "if transaction costs are small, do they still matter" floor case. |
| **15 bps** | 0.15% | A more conservative, stressed-liquidity estimate — representative of wider spreads on the band/spec tier's smaller-cap names, or of any name during a volatile stress period (exactly the kind of period a forced-repayment trim is most likely to coincide with, since Model B's trigger is tied to net-equity highs, but the *portfolio's* overall volatility during any given window isn't uniform). Chosen as the "if costs are meaningfully higher than the optimistic case" ceiling. |

**Labeling:** 0 bps is **Known** (Robinhood's real, documented commission structure). 5 bps and 15 bps are **Hypothetical** — no real spread/slippage data exists anywhere in this system to validate them against (the same epistemic status as Phase 4A's hypothetical shock magnitude, or Phase 3's 5% interest-rate Estimate, one level down from Estimated since there isn't even a disclosed doctrine figure to anchor to — spread cost has never been discussed in `CLAUDE.md` at all). This will be stated in every output this plan produces, per the labeling requirement in §7.

**Not tested:** a per-trade fixed fee (e.g., SEC/FINRA regulatory pass-through fees, which are real but tiny — on the order of fractions of a cent per trade on Robinhood — and, per §3, cannot be modeled accurately without per-ticker-leg trade counts this harness doesn't log). Explicitly out of scope for this pass, not silently assumed zero-impact.

## 6. Method (planned, not yet implemented)

Reuses the existing, unmodified `margin_simulation.py` harness and `ModelBProfitHarvest` policy exactly as already approved — **no engine changes.** The existing `docs/results/PHASE3_SENSITIVITY_RESULTS.json` stores aggregate metrics per `repay_fraction` arm (event count, total repaid, TWR, MaxDD) but not the per-event list needed to compute a properly time-distributed cost — so this plan intends to **re-run** the three already-approved Model B arms (`repay_fraction` = 10%/25%/50%, all other parameters identical to `docs/PHASE3_SCENARIO_MANIFEST.md`'s original values) through the unmodified harness to recover each event's exact day-index and dollar amount, matching Phase 3G's own established pattern of re-running already-approved configurations to extract detail the stored aggregate didn't retain (`run_phase3g_sensitivity.py`'s baseline-verification pattern; `run_phase4a_research.py`'s reuse of `load_real_aligned_data()`). Each re-run's top-line metrics (TWR, MaxDD, event count, total repaid) will be asserted to match the stored `PHASE3_SENSITIVITY_RESULTS.json` values before any cost is applied — the same "verify identical before proceeding" discipline every prior re-run in this project has followed.

**Cost application (planned as a post-hoc, first-order approximation, not a re-simulated cost-aware backtest):** for each repayment event, `cost = bps × event["amount"]`. Total cost per arm/tier = sum of all such costs. This total is subtracted once, as a lump sum, from the arm's final book value, and an approximate cost-adjusted annualized TWR is derived from that adjusted final value (holding the deposit schedule and interim path fixed). **This is explicitly a simplification**, stated here rather than discovered later: it does not compound the cost drag forward (a $1 cost paid in year 1 doesn't itself lose potential future growth in this approximation), and does not re-invest what would, in a fully rigorous model, be a slightly smaller amount available to buy back into positions after each trim. A fully rigorous version (deducting cost inside the simulation loop itself, letting it compound) would require an actual `margin_simulation.py` change and is explicitly **not** in scope for this small, sensitivity-only pass — named here as a possible future refinement, not built now.

## 7. Metrics collected

For each of the 3 `repay_fraction` values × 3 cost tiers (9 cells, plus the 3 already-published 0-bps cells serving as the control row):

- `ann_twr_pct` (cost-adjusted, per §6's approximation) and the **gap versus the 0-bps figure already published** for that same `repay_fraction`.
- `ann_twr_pct` gap versus the D-0 (no-repayment) control, cost-adjusted — the comparison that actually matters for "is Model B still worth discussing once costs are counted," since the original Phase 3E/3G finding was itself a comparison against that control, not against Model B's own zero-cost self.
- Total cost in dollars, and as a % of total gross repaid (i.e., the bps rate itself, restated for readability) and as a % of total deposited capital ($124,000).
- Every cell explicitly labeled with its cost-tier's Known/Hypothetical status per §5.

`max_drawdown_pct` is **not** cost-adjusted in this pass — a lump-sum, lagging cost deduction applied to the final book value does not meaningfully change a *peak-to-trough* calculation computed from the path leading up to that point, and attempting to do so would require the fully-compounded re-simulation explicitly out of scope per §6. This is stated as a scope limitation, not silently omitted.

## 8. Interpretation rules

- **Report the full 3×3 grid every time.** No cell is presented as "the" answer; no `repay_fraction` row is highlighted as preferred.
- **Compare cost-adjusted TWR against the pre-existing 2.0pp/0.5pp materiality bands** already established in `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3 — reused for consistency, not re-derived, matching the "reuse existing thresholds before inventing new ones" instinct this project has followed since Phase 4A adopted Scenario D's 2.0pp bar rather than picking a fresh number.
- **State directionally whether cost erosion scales with `repay_fraction`** (i.e., does the 50% arm's higher turnover — $156,113 total repaid vs. $38,226 at 10% — translate into proportionally larger cost drag) — a factual, mechanical relationship to report, not a judgment about which fraction is "better."
- **Distinguish two separate questions explicitly in any output**: (a) "how much of Model B's already-published TWR shortfall versus the no-repayment control is cost, versus the repayment mechanism's own opportunity cost" and (b) "does the already-published MaxDD improvement still look worthwhile once a hypothetical cost is priced against the TWR side of the trade." These are related but different questions and must not be collapsed into one.
- **The fragmentation gap (§3) must be restated in the results document**, not just this plan — a reader of the eventual results must know the dollar-volume cost model does not capture potential minimum-fee-per-leg effects.

## 9. Materiality thresholds

Reused, not reinvented: **2.0 percentage points** = material TWR gap, **0.5 percentage points** = noise floor, exactly `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3's already-approved values. Applied here to the *cost-adjusted* TWR gap versus the D-0 control (the comparison in §7's second bullet). No new threshold is introduced by this plan.

## 10. What conclusions are, and are not, allowed

**Allowed:**
- Reporting, for each of the 9 cells, whether the cost-adjusted TWR gap versus the no-repayment control remains material, becomes non-material, or was never material to begin with.
- Reporting the dollar and percentage cost figures themselves, clearly labeled Hypothetical (5/15 bps) or Known (0 bps).
- Noting directional relationships (higher `repay_fraction` → higher turnover → higher absolute cost, if that holds mechanically in the data).
- Restating, explicitly, that the fragmentation question (§3/§8) remains unaddressed by this pass.

**Not allowed:**
- Selecting a preferred `repay_fraction`. This analysis exists to re-interpret existing evidence, not to search for a "least-cost" configuration — doing so would be parameter optimization by another name, prohibited by this task's own explicit instruction and by `docs/PHASE3_SENSITIVITY_PLAN.md`'s standing prohibition on the same.
- Recommending Model B for or against production deployment. No finding from this analysis, in either direction, changes `targets.yaml`'s (still entirely `null`) margin schema or `CLAUDE.md`'s Decisions Log — the same standing rule every prior Phase 3/4 document has restated.
- Treating the 5 bps / 15 bps figures as real, measured Robinhood spread costs. They are disclosed assumptions, explicitly one step further removed from doctrine than the 5% interest-rate Estimate, and must be labeled as such in every output.
- Drawing any conclusion about Model C, whose measured repayment activity across every Phase 3G/4A run to date is either zero or too small to have a meaningful dollar-volume-based cost applied to it — Model C is out of scope for this specific analysis, not silently included.
- Modifying `margin_simulation.py`, `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py` to produce this analysis. Per §6, the re-run uses the harness exactly as it exists today.

---

## What this plan deliberately does not do

- Does not run any simulation or cost calculation.
- Does not implement the fully-compounded cost-aware re-simulation named as a future refinement in §6.
- Does not address the per-trade fragmentation cost dimension named in §3.
- Does not select or recommend any `repay_fraction`, cost tier, or deployment decision.
- Does not modify any code or production file.

Stopping here. Awaiting approval before implementation.
