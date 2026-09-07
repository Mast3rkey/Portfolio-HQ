# Phase 6A — Tax Lot & Realized Gain Modeling: Research Plan

> **⚠️ Hypothetical, simulated — a design document, not a result.** No simulation-engine change has been made and no tax calculation has been run. This document defines the scope of a research-only extension to `margin_simulation.py`. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which will apply to every eventual output.

_Written 2026-07-17. Direct follow-up to `docs/PHASE5B_GOVERNANCE_DECISION.md`, which named tax-lot realism as the highest-value blocker to the "maintain current doctrine" decision. Per explicit instruction: research-only extension, no production files, no doctrine changes, no parameter selection. This plan, `docs/PHASE6A_ASSUMPTION_REGISTRY.md`, and `docs/PHASE6A_DATA_REQUIREMENTS.md` must all be produced and approved before any code is written._

---

## 1. Sources reviewed

`docs/PHASE5_DECISION_GATE_REVIEW.md` (§5, naming "real tax-lot accounting" as blocker #1), `docs/PHASE5B_GOVERNANCE_DECISION.md` (§3's evaluation of Decision 2, which cited the tax-lot gap as a direct reason advisory-only expansion is not yet supported), `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` and `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md`/`.json` (the worst-case upper-bound analysis this phase exists to test against a more realistic model — not to replace or invalidate), `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` (§5, listing "actual cost basis" as still unknown), and `margin_simulation.py` itself, read directly to confirm the current data model (§3 below).

## 2. Objective

**Research question:** *How much of the Model B tax effect, as measured by the worst-case upper-bound tax-sensitivity pass, survives realistic per-lot cost-basis and holding-period accounting?*

This is a **narrowing** question, not a new one. `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md` already established that under a deliberately severe upper bound (100% of every repayment dollar treated as realized gain, all-short-term or all-long-term bracketing), tax friction can materially change the magnitude of the Model B effect (at 50%/32%, gap widened from −3.56pp to −7.45pp). That finding was explicitly flagged, at the time, as a ceiling — "the true tax drag (accounting for basis) is somewhere at or below the reported figure" (`TAX_TREATMENT_SENSITIVITY_PLAN.md` §8). Phase 6A exists to find out *how far* below, using an actual reconstructed cost basis and actual holding-period classification instead of a disclosed worst case.

This closes a gap neither the transaction-cost nor the original tax-sensitivity pass could close: both explicitly required *zero* simulation-engine change (`TAX_TREATMENT_SENSITIVITY_PLAN.md` §3: "a rigorous realized-gain tax calculation requires per-lot cost-basis tracking... `margin_simulation.py` does not track this... extending this would be a genuine simulation-engine change"). Phase 6A's entire purpose is to make that specific, previously-declined extension — deliberately, disclosed, and scoped narrowly, following the same "extend only when a named capability genuinely doesn't exist elsewhere" precedent already used once for Phase 4A's `track_tickers` parameter.

## 3. Current state of the simulation engine (Known, verified directly)

Read directly from `margin_simulation.py`:

- `simulate()` maintains `shares: dict[str, float]` — an **aggregate share count per ticker only**. No acquisition price, no acquisition date, no lot structure exists anywhere in the current engine.
- Purchases occur at line ~687: `shares[s] = shares.get(s, 0.0) + spend / closes[s]` — a share count increment, with the day's close price used only transiently to compute the share quantity, then discarded. The purchase price is never stored.
- Sales occur in `_fund_repayment()` (line 527): `shares[s] -= sell_val / px` — a proportional trim across all held tickers, again with no reference to *which* shares (by acquisition) are being sold.
- **Conclusion: there is currently no way, even in principle, to compute a realized gain for any sale** — not approximately, not with an upper bound baked into the engine, nothing. The upper-bound approach in the prior tax pass existed specifically because this gap made anything more precise impossible without an engine change.

## 4. Scope: what Phase 6A adds, and only that

**Adds, to the simulation layer only:**
- A per-ticker lot ledger: each purchase event recorded as a discrete lot (`day_idx`, `shares`, `cost_basis_price`), appended to a list rather than folded into an aggregate count.
- A consumption convention for sales (§6 — FIFO, the only convention this plan proposes, see rationale there) that removes shares from the oldest lot(s) first and computes realized gain (`sale_price − cost_basis_price`) per share sold, summed per sale event.
- A day-index-to-calendar-date mapping (already implicit in the existing simulation calendar) used to classify each realized lot as short-term (≤365 days between acquisition and sale) or long-term (>365 days) — an actual classification, not a bracketed assumption.
- New fields on `SimulationResult` (or an equivalent output structure) to expose, per repayment event: realized gain amount, and its short-term/long-term split — the two quantities the prior tax pass could not produce and had to bound instead.

**Does not add:**
- Any change to `ModelBProfitHarvest`, `ModelCRiskReset`, or any trigger/decision mechanic — repayment *timing* and *amount* are unchanged; only what happens to the *shares sold to fund* a repayment (which specific lot, and its realized gain) is newly tracked.
- Any change to `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or `CLAUDE.md`.
- Any tax-rate selection, `repay_fraction` selection, or parameter optimization — the same three `repay_fraction` values (10%/25%/50%) already approved are reused, not re-swept.
- Any claim about this account's actual real-world cost basis — lots are constructed entirely from the simulation's own synthetic $0-start purchase history (the same synthetic account every Phase 3/4 scenario already uses), never from this account's real Robinhood trade history, which this project has never had access to (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`).

## 5. Known vs. Unknown

### Known (already established, reused without re-deriving)

- The existing `repay_fraction` sweep (10%/25%/50%) and its already-verified event streams, gross TWR, and MaxDD figures (`docs/results/PHASE3_SENSITIVITY_RESULTS.json`).
- The prior tax-sensitivity pass's upper-bound figures, as the explicit comparison baseline this phase exists to narrow, not replace (`docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json`).
- `margin_simulation.py`'s current share-tracking mechanics (§3), confirmed by direct code read this session.
- The materiality bands (2.0pp material / 0.5pp noise floor), reused per every prior sensitivity pass.

### Unknown, and how this plan handles each

- **This account's real cost basis, real acquisition dates, real lot history.** Genuinely and permanently unavailable to this harness — the simulation is, and remains, a synthetic $0-start account. Phase 6A does not attempt to reconstruct real basis; it computes a **simulated, internally-consistent** basis from the synthetic account's own simulated purchase history. This is a meaningfully different (and more defensible) quantity than the prior pass's 100%-gain upper bound, but it is still not this account's real tax situation — the label discipline in `docs/PHASE6A_ASSUMPTION_REGISTRY.md` makes this distinction explicit for every output.
- **Lot consumption convention (FIFO vs. LIFO vs. specific-lot vs. average-cost).** Real brokerages (including Robinhood) typically default to FIFO unless the account holder elects otherwise, and no document in this project states an election was ever made. **This plan adopts FIFO** as the default, disclosed convention — see §6 for the rationale and the explicit acknowledgment that this is a modeling choice, not a confirmed fact about this account.
- **Actual federal/state tax rates.** Unchanged from the prior pass — still illustrative (0%/15%/32%), still federal-only, still explicitly not this account's confirmed rate. Phase 6A does not attempt to resolve this Unknown; it exists to resolve the *cost-basis* Unknown only.
- **Wash-sale rules, tax-loss harvesting interactions, AMT, NIIT, or any other tax-code complexity beyond basic short/long-term capital gains classification.** Explicitly out of scope — adding these would compound assumption count without addressing the specific, named blocker (basis and holding period) this phase targets.

## 6. Lot consumption convention: FIFO, disclosed rationale

FIFO (first-in-first-out) is proposed as the sole consumption convention this phase implements, for three stated reasons:

1. It is the IRS default and Robinhood's stated default absent an explicit specific-identification election — the most defensible "no information to the contrary" choice, not an arbitrary one.
2. It is the simplest convention to implement correctly and verify with tests — consistent with this project's standing preference for the smallest correct extension over a more elaborate one (the same preference that kept `track_tickers` minimal in Phase 4A).
3. Testing multiple conventions (FIFO vs. specific-lot optimization, e.g. "always sell the highest-basis lot first to minimize gain") would drift toward exactly the kind of tax-optimization research this project has repeatedly and explicitly declined to pursue (`CLAUDE.md`'s Decisions Log pattern of closing questions rather than proliferating variants). FIFO is modeled because it is the realistic default, not because it is favorable or unfavorable to Model B's measured effect.

**This plan does not propose a specific-lot or LIFO sensitivity case.** If FIFO's result turns out to matter to a future governance decision, a convention-sensitivity extension would be its own future request, not assumed here.

## 7. Metrics and comparison structure

For each `repay_fraction` ∈ {10%, 25%, 50%}, three parallel figures, all already-established formats:

1. **Gross Model B result** (unchanged, reused from `docs/results/PHASE3_SENSITIVITY_RESULTS.json`).
2. **Upper-bound tax-adjusted result** (unchanged, reused from `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json` — the comparison baseline).
3. **FIFO-lot tax-adjusted result** (new): realized gain computed per-event from the lot ledger (§4), short/long-term classified by actual elapsed days, taxed at the same illustrative 0%/15%/32% tiers used previously — but now applied only to the *actual computed gain*, not 100% of the trimmed dollar amount.

Reported per cell: gross TWR, upper-bound-tax TWR, FIFO-tax TWR, and the **gap-narrowing measurement** — how much of the upper-bound tax effect (§2's original question) is attributable to the 100%-gain assumption specifically, isolated by comparing (control − upper-bound) against (control − FIFO-lot).

Materiality classification (2.0pp/0.5pp) applied to both the upper-bound and FIFO-lot gaps independently, using the existing bands, not new ones.

## 8. Allowed conclusions

- Whether the FIFO-lot tax-adjusted gap remains material, becomes non-material, or was never material at the 2.0pp/0.5pp bands, for each `repay_fraction` × tax-tier cell.
- What fraction of the originally-observed upper-bound tax effect is attributable to the 100%-gain assumption versus genuinely realized gain under a realistic lot model.
- Whether the short/long-term mix, once actually computed rather than bracketed, falls closer to the prior pass's all-LT or all-ST bound, or somewhere between.
- Restating explicitly which Unknowns from §5 remain open after this phase (state tax, actual real-world basis, actual real-world rate/filing status, wash-sale/AMT/NIIT complexity).

## 9. Prohibited conclusions

- **No repayment policy recommendation** — matching every prior sensitivity pass in this line, verbatim.
- **No selection or ranking of `repay_fraction`** — the sweep is reused exactly, not re-tuned.
- **No claim that FIFO is this account's actual, elected lot convention** — it is the disclosed default assumption per §6, not a confirmed fact.
- **No claim that the resulting basis/gain figures represent this account's real cost basis** — they are computed from the simulation's own synthetic purchase history, never from real trade data.
- **No doctrine change of any kind** — `targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py`, `CLAUDE.md` all remain untouched by this plan and its eventual execution.
- **No expansion into wash-sale rules, AMT, NIIT, state tax, or lot-convention sensitivity (LIFO/specific-lot)** — all explicitly out of scope per §5/§6; a future request, not assumed here.

## 10. Implementation constraints (for the eventual coding phase, not yet authorized)

- The lot ledger and FIFO consumption logic are additive to `margin_simulation.py` — existing behavior (share totals, portfolio valuation, leverage computation, every existing test) must remain byte-for-byte unchanged when the new tracking is not consumed by a caller, following the exact backward-compatibility bar `track_tickers` was held to in Phase 4A (`test_simulate_default_track_tickers_is_empty_and_behavior_unchanged` is the precedent test shape).
- Before any new tax-adjusted figure is trusted, the same "verify before proceeding" discipline applies: re-run the existing `repay_fraction` arms and confirm gross TWR/event counts still match `docs/results/PHASE3_SENSITIVITY_RESULTS.json` exactly, with the lot ledger active but unconsumed by the comparison.
- Full test suite (260 tests, growing) must pass with zero regressions before any commit.
- `_assert_no_banned_language()` and hypothetical/simulated labeling apply to every new output, unchanged.

---

## What this plan deliberately does not do

- Does not modify `margin_simulation.py` or any other code — this is the design document, not the implementation.
- Does not run any tax calculation or lot-accounting simulation.
- Does not select a `repay_fraction`, tax rate, or lot convention as "the" answer — FIFO is disclosed as the sole modeled convention, not chosen as correct.
- Does not recommend a repayment policy or change any doctrine.
- Does not expand scope beyond cost-basis/holding-period realism — every other Unknown named in §5 remains explicitly open.

Stopping here, alongside `docs/PHASE6A_ASSUMPTION_REGISTRY.md` and `docs/PHASE6A_DATA_REQUIREMENTS.md`. Awaiting approval before any code is written.
