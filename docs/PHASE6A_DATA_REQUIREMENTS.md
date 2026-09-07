# Phase 6A: Data Requirements

_2026-07-17 · Documentation only. No code run. Identifies exactly what data Phase 6A's lot-accounting extension needs, what already exists, and what must be newly derived — matching the verification role `docs/PHASE3C_DATA_VALIDATION_REPORT.md` played for Phase 3C, adapted to this phase's narrower scope._

---

## 1. What already exists (no new data source needed)

| Data | Source | Status |
|---|---|---|
| Real historical OHLCV bars (`data/backtest/*.json`) for every simulated ticker | Already cached, already used by every Phase 3/4 scenario | **Available, unchanged** |
| Simulation trading-day calendar (day-index → real calendar date) | Already constructed inside `margin_simulation.py`'s `simulate()` / reused by `backtest_regime.py`'s alignment logic | **Available, unchanged** — this is the exact mapping Phase 6A's holding-period (365-day) classification needs; no new calendar logic required |
| `repay_fraction` sweep event streams (day, amount, kind per event) | `docs/results/PHASE3_SENSITIVITY_RESULTS.json` | **Available, already verified** |
| Prior upper-bound tax figures (the comparison baseline) | `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json` | **Available, already verified** |
| Materiality bands (2.0pp/0.5pp) | `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` | **Available, reused unchanged** |

## 2. What does not exist and must be newly derived (inside the simulation, not sourced externally)

| Data | Why it doesn't exist today | How Phase 6A proposes to derive it |
|---|---|---|
| Per-lot acquisition record (day-index, share quantity, cost-basis price) for every simulated purchase | `simulate()` currently folds every purchase into a single aggregate `shares[ticker]` float (§3 of the plan) — the per-purchase price is computed transiently and discarded | New: append a lot entry at the exact point purchases currently increment the aggregate count (line ~687 of `margin_simulation.py`), with no change to the *quantity* or *timing* of any purchase — purely additive record-keeping |
| Per-sale realized-gain computation | `_fund_repayment()` currently trims `shares[ticker]` proportionally with no reference to acquisition price (§3 of the plan) | New: when a sale occurs, consume lots FIFO (oldest first) until the sold quantity is satisfied, computing `(sale_price − lot_cost_basis_price) × shares_sold_from_lot` per lot consumed, summed to a total realized gain for that sale event |
| Holding period (days elapsed) per consumed lot | Requires knowing both the lot's acquisition day-index and the sale's day-index — the acquisition side doesn't exist yet (see above) | New: `sale_day_idx − lot_acquisition_day_idx`, classified against the 365-day threshold using the already-available day-index-to-date calendar (§1) |

**No data must be sourced from outside this repository.** Every input Phase 6A's lot ledger needs is either already present in the simulation's existing purchase/sale mechanics (share quantities, prices, day indices — all already computed transiently today, just not retained) or is a pure derived computation from those inputs. This is unlike, for example, a hypothetical future "real broker margin behavior" research track, which would require data this project has no path to obtaining at all (see `docs/PHASE5B_GOVERNANCE_DECISION.md` §3's blocker list, item 3).

## 3. What remains unavailable even after Phase 6A (explicitly not solved by this phase)

| Data | Why it stays unavailable |
|---|---|
| This account's real cost basis, real acquisition dates, real lot history | This project has no access to real Robinhood trade-history data — confirmed absent in `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`, unchanged by this phase. Phase 6A's lot ledger is built entirely from the *synthetic* $0-start simulation's own purchase history, never from a real trade record. |
| This account's actual elected lot-consumption convention (FIFO vs. specific-lot) | No record of any such election exists or could exist without real brokerage account data |
| This account's actual marginal tax rate, filing status, state of residence | Never stated in any document this project has access to; explicitly excluded from this phase's scope (federal-only, illustrative rates only) |
| Wash-sale history, AMT/NIIT applicability | Would require full real tax-filing data this project has never had and is not attempting to obtain |

## 4. Validation plan (for the eventual implementation, not yet authorized)

Before any FIFO-lot tax figure is reported, the implementation must demonstrate, in order:

1. **Lot-ledger internal consistency**: sum of all lot share quantities for a ticker at any simulated day equals the existing aggregate `shares[ticker]` value at that same day — a direct, testable invariant that the new tracking hasn't silently diverged from the existing (already-tested) share-count mechanics.
2. **Zero behavioral change when the lot ledger is unconsumed**: every existing test (260, per `docs/PHASE5_DECISION_GATE_REVIEW.md`'s recorded count) passes unchanged, and the already-verified `repay_fraction` arms reproduce their exact stored gross TWR/event counts — the same "verify before proceeding" gate every prior phase in this line has applied before trusting a new figure.
3. **FIFO consumption correctness on a small hand-checkable case**: at least one test constructs a minimal 2-3-lot scenario with known acquisition prices/dates and a known sale, and asserts the computed realized gain and holding-period classification match hand-arithmetic exactly — the same "trace by hand, don't trust the code alone" discipline used to catch the `worst_drawdown_recovery` day-index error in Phase 4A.

## 5. Summary

**No external data acquisition is required for Phase 6A.** Every input the lot-accounting extension needs already exists inside the simulation's current mechanics in transient, unretained form (purchase price, purchase day, sale price, sale day) — the work is retaining and structuring data the engine already computes and discards, not sourcing anything new. This distinguishes Phase 6A sharply from the broker-mechanics blocker (`docs/PHASE5B_GOVERNANCE_DECISION.md` §3, item 3 / `PHASE5_DECISION_GATE_REVIEW.md` §5, item 3), which remains permanently or near-permanently unresolvable within this project's data access — a distinction worth stating plainly since both are "blockers" but of fundamentally different resolvability.

---

## What this document deliberately does not do

- Does not implement the lot ledger or any code.
- Does not run the validation plan in §4 — those are requirements for the eventual implementation phase, not results.
- Does not claim any data listed in §3 will ever become available — those remain named, permanent-or-near-permanent gaps.

Stopping here, alongside `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md` and `docs/PHASE6A_ASSUMPTION_REGISTRY.md`. Awaiting approval before any code is written.
