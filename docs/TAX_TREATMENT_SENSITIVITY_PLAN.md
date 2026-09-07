# Tax Treatment Sensitivity Analysis — Research Plan

> **⚠️ Hypothetical, simulated — a design document, not a result.** No tax analysis has been run. Every number this plan will eventually produce describes a synthetic $0-start account simulated through real historical prices, with a further hypothetical tax assumption layered on top — never a claim about this account's real tax liability. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies to every output this plan produces.

_Written 2026-07-17, per `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 9 (promoted to priority 1 after item 1's closure). Documentation only — no code, no simulation changes, no production files touched. Do not implement until this plan is approved._

---

## 1. Sources reviewed

`docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` (which named tax treatment as the first of the still-open "non-bps effects" a closed transaction-cost question does not address), `docs/results/PHASE3_MODEL_B_ANALYSIS.md` (the event-level turnover measurement this plan reuses, and the "cash brokerage assumption" language this plan makes explicit — see §4), `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` item 9 (this plan's own scoping origin), and every existing margin research document this reuses without re-deriving: `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md`/`RESULTS.md` (the sibling analysis this plan is structured to match — same event stream, same "verify before applying a new assumption" discipline), `docs/PHASE3_SENSITIVITY_PLAN.md`/`RESULTS.md` (the `repay_fraction` sweep this plan reuses), `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` (the materiality bands this plan reuses rather than re-deriving), `CLAUDE.md` and `docs/MARGIN_DOCTRINE.md` (checked directly — neither mentions tax jurisdiction, account type, or any tax assumption anywhere; confirmed via direct search, not assumed absent).

## 2. Purpose

Define how tax treatment could affect the interpretation of Model B's already-observed repayment-model evidence — narrowly, the same framing `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` used for the transaction-cost question: this plan exists to test whether an unresolved limitation changes a conclusion already on record, not to search for a tax-optimal repayment strategy.

## 3. Hard constraint: no simulation changes

Unlike the transaction-cost pass — where `SimulationResult.events` already carried everything needed (exact day and dollar amount per repayment event) — a **rigorous** realized-gain tax calculation requires per-lot cost-basis tracking (knowing at what price each specific share was bought, so a sale's gain/loss can be computed exactly). `margin_simulation.py` does not track this: `simulate()` maintains only an aggregate share count per ticker, never acquisition price or date per lot. Extending this would be a genuine simulation-engine change.

**This plan is scoped, per explicit instruction, to require no simulation changes at all.** §5 below defines exactly what this constraint permits to be modeled honestly, and what it forecloses.

## 4. Known vs. Unknown

### Known (already established, no new assumption required)

- **Existing simulation mechanics.** `ModelBProfitHarvest`'s trigger (net-equity high-water mark, repay `repay_fraction` of the fresh gain) and `_fund_repayment()`'s funding mechanism (cash first, then pro-rata trim across held positions) — both read directly from `margin_simulation.py`, unchanged by this plan.
- **Existing repayment events.** The exact day-index and dollar amount of every repayment event, for `repay_fraction` ∈ {10%, 25%, 50%}, already produced by `run_transaction_cost_sensitivity.py`'s re-run and verified against `docs/results/PHASE3_SENSITIVITY_RESULTS.json` — the same event stream, reusable without re-running anything new.
- **Existing turnover measurements.** $38,226 / $88,516 / $156,113 gross repaid at 10%/25%/50% respectively (`docs/results/PHASE3_MODEL_B_ANALYSIS.md`, `docs/PHASE3_SENSITIVITY_RESULTS.json`), and the finding that transaction cost at these turnover levels was immaterial (`docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md`).

### Unknown (genuinely unresolvable without new data or an engine change)

- **Tax jurisdiction.** No document in this project states a state of residence, and federal-vs-state tax treatment differs materially (some states have no capital gains tax at all; others tax it as ordinary income). **This plan will model federal treatment only, explicitly excluding state tax** — a disclosed scope limitation, not a silent assumption of zero state tax.
- **Account type assumptions, precisely.** No document explicitly states "this is a standard taxable margin account," but it can be reasonably inferred: margin borrowing is not available in tax-advantaged retirement accounts (IRAs, 401(k)s) under standard brokerage rules, and `CLAUDE.md`/`docs/MARGIN_DOCTRINE.md` describe this account as actively using margin. This inference is **Estimated**, not Known — reasonable and disclosed, not asserted as directly stated doctrine.
- **Realized gain basis.** Without per-lot cost tracking (§3), the actual gain realized by any specific trim is unknowable from this harness. See §5 for how this plan handles that gap honestly rather than guessing a number.
- **Holding period effects.** Short-term (≤1 year, taxed as ordinary income) vs. long-term (>1 year, taxed at preferential capital-gains rates) status depends on exactly when each sold lot was originally purchased — also unknowable without per-lot tracking.

## 5. What can be modeled honestly, and what cannot

### Can be modeled honestly, without any simulation change

A **worst-case, upper-bound** realized-gain approximation: treat 100% of each repayment event's trimmed dollar amount as realized gain (i.e., assume zero return of cost basis), and apply a disclosed federal tax rate to that full amount. This is defensible as an upper bound, not arbitrary, for two stated reasons:

1. It requires no new data this harness doesn't already have — every input (event dollar amounts) is already Known (§4).
2. Model B's trigger fires *only* on a new net-equity high (`ModelBProfitHarvest`'s documented mechanism) — by construction, every triggering day represents the portfolio at a point above every prior high, which is directionally consistent with (though not identical to) a higher-than-average proportion of the trimmed value being gain rather than basis. This does not make the 100%-gain assumption *accurate*, but it makes it a *directionally justified* upper bound rather than an arbitrary one — the same "upper-bound estimate, not an exact figure" honesty standard `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4 already established for turnover itself.

This mirrors the transaction-cost pass's exact method (`event_costs()`-style post-processing of the same already-known event stream) — no new simulation run beyond the same re-run-and-verify pattern already established, applying a rate instead of a bps spread.

### Cannot be modeled without unsupported assumptions

- **An accurate (non-upper-bound) realized-gain dollar figure.** Requires per-lot cost-basis tracking, which requires a simulation-engine change, prohibited by this plan's own scope (§3). Any attempt to approximate this more tightly (e.g., "average cost basis" reconstruction) would itself require tracking data this harness does not currently expose anywhere (not even the per-ticker buy amounts needed to reconstruct an average cost basis externally — `SimulationResult.events` records deposits and margin draws in aggregate, not a per-ticker purchase-price ledger).
- **The true short-term/long-term mix.** Cannot be computed; this plan brackets it instead (§6) rather than guessing a blended assumption.
- **State tax liability.** Excluded entirely (§4) rather than modeled with an invented state.
- **This account's actual marginal tax rate or filing status.** Never asserted; every rate used is explicitly illustrative (§6), not a claim about the real account.

## 6. Sensitivity cases

Two independent dimensions, both bracketing rather than guessing a single point estimate, matching this project's established Track 1/Track 2 and historical-primary/hypothetical-secondary bracketing patterns:

### Tax rate tiers (illustrative federal brackets, all Hypothetical)

| Tier | Rate | Rationale |
|---|---:|---|
| **T0 — no tax** | 0% | Control/baseline — reproduces every already-published pre-tax Model B figure exactly, same role 0bps played in the transaction-cost pass. |
| **T1 — long-term capital gains, illustrative** | 15% | The most common U.S. federal long-term capital gains bracket. Illustrative only — not this account's confirmed rate. |
| **T2 — short-term / ordinary income, illustrative** | 32% | A representative federal ordinary-income marginal bracket (short-term gains are taxed as ordinary income, not at capital-gains rates) — the higher end of this plan's bracket, not a claim about this account's actual bracket. |

### Holding-period assumption (brackets the unknowable true mix, §4/§5)

| Case | Assumption |
|---|---|
| **All-long-term** | Every repayment event's trim is assumed long-term (uses tier T1's rate) — the optimistic bound. |
| **All-short-term** | Every repayment event's trim is assumed short-term (uses tier T2's rate) — the pessimistic bound. |

Combined with the existing `repay_fraction` ∈ {10%, 25%, 50%} dimension (unchanged, not re-swept), this produces a small grid: 3 fractions × (T0 control + all-LT-at-T1 + all-ST-at-T2) = 9 cells, directly comparable in shape to the transaction-cost pass's 3×3 grid.

## 7. Required labels

Every output this plan eventually produces must carry these labels, matching or extending the transaction-cost pass's precedent exactly:

| Item | Label |
|---|---|
| `repay_fraction` values, event dollar amounts, turnover figures | **Known** (already-verified simulation output) |
| Account type (taxable, non-retirement) | **Estimated** (a reasonable, disclosed structural inference from margin usage — not directly stated doctrine) |
| Tax rates (0%/15%/32%) | **Hypothetical** (illustrative federal brackets, not this account's confirmed rate) |
| 100%-of-trim realized-gain assumption | **Hypothetical, explicitly an upper bound** — every output must state this is not an estimate of actual tax owed, only a ceiling |
| Holding-period assumption (all-LT / all-ST) | **Hypothetical**, explicitly a bracket around an unknowable true mix, not a best guess at the true mix |
| Jurisdiction (federal-only, no state) | **Known scope limitation** — state tax is not zero, it is excluded, and every output must say so |

Every result, per the standing project-wide rule, carries `HYPOTHETICAL_LABEL` and passes `_assert_no_banned_language()` unchanged.

## 8. Allowed conclusions

- Reporting, for each of the 9 cells, the cost-adjusted (tax-adjusted) TWR and whether the gap versus the D-0 control remains material, becomes non-material, or was never material — using `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`'s existing 2.0pp/0.5pp bands, reused not re-derived.
- Stating plainly that the 100%-gain assumption is an upper bound, and that the true tax drag (accounting for basis) is somewhere at or below the reported figure — never presenting the upper-bound number as a point estimate.
- Noting whether the previously-established transaction-cost finding's pattern repeats (i.e., whether tax drag, even at the upper bound, is similarly immaterial relative to the observed gaps, or whether it differs materially from the transaction-cost result) — a direct, allowed comparison between the two now-closed-and-open sensitivity passes.
- Restating, explicitly, every item named in §5's "cannot be modeled" list as still open after this analysis.

## 9. Prohibited conclusions

- **No repayment policy recommendation of any kind** — this analysis does not conclude Model B should or should not be used, at any `repay_fraction`, under any tax assumption.
- **No selection or ranking of `repay_fraction` values** — the sweep is reused exactly as already approved; this plan does not re-open or re-tune it.
- **No claim that the 15%/32% figures represent this account's real tax rate**, or that the 100%-gain assumption represents this account's real realized-gain amount.
- **No doctrine change of any kind** — `targets.yaml`'s margin schema, `CLAUDE.md`'s Decisions Log, and every other production/doctrine file remain untouched by this plan and by its eventual execution.
- **No claim about state tax liability**, including no implicit claim that excluding it means it doesn't matter — explicitly the opposite (§4/§7).
- **No implementation of per-lot cost-basis tracking** in this pass — named in §5 as a real limitation and a possible future engine extension, not built now, and not to be silently attempted mid-analysis if the upper-bound approach feels unsatisfying once results are seen.

---

## What this plan deliberately does not do

- Does not run any tax calculation.
- Does not modify `margin_simulation.py` or any other code.
- Does not re-sweep `repay_fraction` — reuses the existing 10%/25%/50% values exactly.
- Does not attempt a more accurate (non-upper-bound) realized-gain calculation — explicitly out of scope per §3/§5.
- Does not recommend a repayment policy or change any doctrine.

Stopping here. Awaiting approval before implementation.
