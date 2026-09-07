# Phase 6A: Assumption Registry

_2026-07-17 · Documentation only. No code run. Every configuration value or modeling choice `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md` proposes, labeled exactly one of three ways, per the same three-label discipline established in `docs/PHASE3C_ASSUMPTION_REGISTRY.md` and reused unchanged by every subsequent plan in this project._

## Labels

- **Known** — directly observed, verified against a real file/data source this session or a prior, still-valid one. Not a model, not a choice.
- **Estimated** — not directly observed, but a reasonable, disclosed approximation derived from Known data plus stated reasoning.
- **Hypothetical** — a simulation-design choice with no claim to represent this account's real history or any observed fact.

---

## Registry

| # | Value / choice | Used in | Label | Basis |
|---|---|---|---|---|
| 1 | `repay_fraction` ∈ {10%, 25%, 50%} | All Phase 6A cells | **Known** | Reused exactly from the already-approved `docs/PHASE3_SENSITIVITY_PLAN.md` sweep — not re-derived or re-tuned |
| 2 | `margin_simulation.py` currently has no per-lot tracking — `shares: dict[str, float]` is an aggregate count only | Motivates the entire phase | **Known** | Verified by direct read of `margin_simulation.py`, line ~687 (purchase) and `_fund_repayment()` line ~527 (sale) — confirmed no acquisition price/date is stored anywhere in the current engine |
| 3 | FIFO lot-consumption convention | New lot ledger's sale logic | **Hypothetical, explicitly disclosed as a modeling choice** | IRS/Robinhood stated default absent an explicit specific-identification election — no document in this project states this account made such an election, so FIFO is the most defensible "no information to the contrary" choice, not a confirmed fact about this account (`PHASE6A_TAX_LOT_MODELING_PLAN.md` §6) |
| 4 | Short/long-term boundary = 365 days from acquisition day-index to sale day-index | Holding-period classification | **Known** (the 365-day/1-year threshold is the actual US federal tax code rule, IRC §1222) applied to **Hypothetical** simulated dates (the underlying acquisition/sale days themselves are synthetic, not real) | The *rule* is Known; the *dates it's applied to* are Hypothetical (synthetic $0-start simulation calendar, same as every prior Phase 3/4 scenario) |
| 5 | Synthetic $0-start purchase history as the sole source of lot data | Every lot ledger entry | **Hypothetical**, matching every prior Phase 3/4A scenario's own starting-condition choice | This account's real Robinhood purchase history/cost basis has never been available to this project (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`) — Phase 6A does not change that; it constructs an internally-consistent *simulated* basis, not a reconstruction of a real one |
| 6 | Tax rate tiers: 0% / 15% / 32% | Applied to FIFO-computed realized gain | **Hypothetical**, unchanged from `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` §6 — illustrative federal brackets, not this account's confirmed rate | Reused exactly, not re-derived — same tiers, now applied to a different (more precise) gain figure |
| 7 | Federal-only tax scope, no state tax | Every tax-adjusted figure | **Known scope limitation**, unchanged from the prior tax pass | State tax is excluded, not assumed zero — same disclosure carried forward verbatim |
| 8 | Account type: standard taxable margin account (not retirement-advantaged) | Applies to every tax-adjusted figure | **Estimated**, unchanged from `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` §4 | Reasonable structural inference (margin borrowing implies a standard taxable account) — not directly stated doctrine, carried forward without re-deriving |
| 9 | Wash-sale rules, AMT, NIIT, tax-loss harvesting: not modeled | Scope boundary | **Known exclusion**, not a silent gap | Explicitly named as out of scope in `PHASE6A_TAX_LOT_MODELING_PLAN.md` §5/§9 — every output must state these remain unaddressed, not implicitly assumed to be zero-impact |
| 10 | Materiality bands: 2.0pp material / 0.5pp noise floor | Classification of every FIFO-lot gap | **Known**, reused unchanged from `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` | No new threshold proposed or derived by this phase |
| 11 | Lot ledger day-index-to-calendar-date mapping | Holding-period elapsed-time computation | **Known** | The simulation's existing trading-day calendar (already used by every Phase 3/4 scenario to align real OHLCV data) provides an exact real-calendar-date mapping for each simulated trading day — no new date source needed |
| 12 | Single lot-consumption convention (FIFO only; no LIFO/specific-lot sensitivity case) | Scope boundary | **Hypothetical scoping decision**, disclosed | `PHASE6A_TAX_LOT_MODELING_PLAN.md` §6 explicitly declines to test alternative conventions this phase, to avoid drifting toward tax-optimization research this project has repeatedly declined to pursue |

---

## What this registry deliberately does not do

- Does not assign a value to any Open Item beyond what `PHASE6A_TAX_LOT_MODELING_PLAN.md` itself already proposes (FIFO, 365-day threshold, 0/15/32% tiers) — every value above is either reused from an already-approved prior document or explicitly proposed and labeled in the plan this registry accompanies.
- Does not run any simulation, lot computation, or tax calculation.
- Does not resolve any of the genuinely Unknown items named in the plan's §5 (real cost basis, real tax rate, state tax, wash-sale/AMT/NIIT) — those remain open, unaddressed by this phase by design.

Stopping here, alongside `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md` and `docs/PHASE6A_DATA_REQUIREMENTS.md`. Awaiting approval before any code is written.
