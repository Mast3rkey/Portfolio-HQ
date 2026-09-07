# Phase 6B — Governance Reassessment

> **⚠️ Governance synthesis, not a re-run.** This document runs no simulation, computes no new figure, and changes no code. It evaluates whether Phase 6A's evidence changes the Phase 5B governance decision. Every figure below is quoted from an already-committed source, cited inline. `targets.yaml`'s margin schema remains entirely `null`; `CLAUDE.md`'s Decisions Log is unchanged; nothing in `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py` is touched by this document.

_Written 2026-07-17. Direct follow-up to `docs/PHASE5B_GOVERNANCE_DECISION.md` and `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md`, per explicit instruction to evaluate — not re-litigate — the governance decision in light of Phase 6A's evidence. Sources reviewed: `docs/PHASE5B_GOVERNANCE_DECISION.md`, `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md`, `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md`, `docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md`, `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md`. Documentation only — no code, no simulation, no production files touched._

**No production adoption question is evaluated here.** This document evaluates only whether Phase 6A's evidence changes the *research-assumption/evidence-classification* picture that fed Phase 5B — not whether Model B should be adopted, at any `repay_fraction`, under any circumstance.

---

## 1. Question 1 — Did realistic tax-lot accounting materially change the evidence classification?

**No, not the classification itself — only the magnitude underlying it.**

Quoting `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` §7 directly:

| repay_fraction | Upper-bound taxable base | FIFO-realistic taxable base | Reduction | Gross gap | Gap @ 15% (FIFO) | Gap @ 32% (FIFO) |
|---:|---:|---:|---:|---:|---:|---:|
| 10% | $38,225.89 | $14,394.88 | 62.3% | −0.98pp (suggestive) | −1.12pp (suggestive) | −1.29pp (suggestive) |
| 25% | $88,516.45 | $38,219.04 | 56.8% | −2.32pp (material) | −2.73pp (material) | −3.20pp (material) |
| 50% | $156,112.51 | $67,142.08 | 57.0% | −3.56pp (material) | −4.31pp (material) | −5.18pp (material) |

The taxable base fell 57–62% at every fraction — a real, substantial narrowing of the prior upper bound. But the **materiality classification** (material / suggestive / noise, per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`'s reused 2.0pp/0.5pp bands) did not cross a boundary at any fraction: 25%/50% were material before and remain material; 10% was suggestive before and remains suggestive. No cell flipped from material to non-material, and none flipped from non-material to material.

## 2. Question 2 — Does the evidence support maintaining current doctrine, advisory-only monitoring, or opening a future pilot design?

**Maintaining current doctrine.** Working through `docs/PHASE5B_GOVERNANCE_DECISION.md` §3's three named options against the updated evidence:

- **Decision 1 (maintain current doctrine):** Still the exact match. Phase 6A did not remove or resolve any of the five blockers §3 of that document cited — it *narrowed* one of them (the tax-lot upper bound was shown to be conservative), but did not close it: this account's real cost basis, real elected lot convention, real tax rate, and real jurisdiction remain entirely unknown (`docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` §8). A narrower estimate is not a resolved unknown.
- **Decision 2 (advisory-only expansion):** Still not supported. `PHASE5B_GOVERNANCE_DECISION.md` §3 specifically flagged that surfacing a hypothetical repayment figure inside the real workflow, before the tax-lot and execution-modeling blockers are resolved, risks presenting a severe-assumption hypothetical as an actionable number. Phase 6A improved the tax-lot assumption's realism but did not eliminate its hypothetical status (still a synthetic-account-only FIFO reconstruction, not this account's real basis) — the specific risk §3 named is reduced in degree, not removed in kind.
- **Decision 3 (authorize future pilot design):** Still premature, for the same reason as before — sequencing pilot-design work ahead of knowing whether the remaining blockers (execution modeling, broker mechanics) are even resolvable would risk designing around requirements that may not survive contact with those open questions.

**No option selection changes.** The evidence base grew narrower and more precise in one dimension (tax realism); it did not grow in the dimensions (execution, broker mechanics, real account data) that would be needed to justify a different option.

## 3. Question 3 — Which blockers remain unresolved?

Restating `docs/PHASE5_DECISION_GATE_REVIEW.md` §5's five blockers against Phase 6A's actual effect on each:

| Blocker | Status after Phase 6A |
|---|---|
| 1. Real tax-lot accounting | **Narrowed, not resolved.** A realistic-mechanics (FIFO) model now exists, built from synthetic data — this account's real cost basis, real convention, real rate, and real jurisdiction are still entirely unknown. |
| 2. Real execution/slippage modeling | **Unchanged, unresolved.** Item 10 (stress-regime execution assumptions) tested repayment *timing* relative to detected stress windows, not real fill quality or spread behavior — Phase 6A did not touch this blocker at all. |
| 3. Real broker margin behavior under extreme events | **Unchanged, unresolved.** Not addressed by Phase 6A in any respect. |
| 4. Human override / execution workflow design | **Unchanged, unresolved.** Not addressed by Phase 6A in any respect. |
| 5. Different market regimes not represented in the tested window | **Unchanged, unresolved.** Phase 6A reused the same 2021–2026 window as every other pass in this research line; no new regime data was introduced. |

**Four of five blockers are entirely untouched by Phase 6A.** Only blocker 1 moved, and it moved from "untested" to "tested, bounded, still incomplete" — not to "resolved."

## 4. Question 4 — What evidence would still be required before any production behavior changes?

Not a new list — the same one `docs/PHASE5_DECISION_GATE_REVIEW.md` §5 already named, still standing in full:

1. This account's actual real cost basis, real lot-consumption election, real marginal tax rate, and real jurisdiction — none of which any simulation, however realistic its *mechanics*, can supply; only real account/tax data can.
2. A real execution/slippage model, or at minimum real evidence about historical fill quality during genuine stress (not a proxy-detected, disclosed-multiplier overlay).
3. A documented (not necessarily production-integrated) inventory of Robinhood's actual margin-call sequencing, maintenance requirements, and forced-liquidation mechanics.
4. A designed human-override workflow appropriate to whatever decision option (Decision 2 or 3 from §2) is eventually pursued, if either ever is.
5. Ideally, evidence from a market regime this project's current 2021–2026 window does not contain — though this is a standing, structural limitation of using historical backtesting at all, not something any single research pass can resolve.

None of these five is advanced by adding more Model B parameter sensitivity, more `repay_fraction` sweeps, or further tax-model refinement on the same synthetic data. The research angle that could still move blocker 1 forward (further tax-lot realism, e.g. a specific-lot or LIFO sensitivity check) would still be bounded by the same synthetic-account ceiling every prior pass in this line has disclosed — it narrows further, it does not resolve.

---

## 5. Preserved constraints (restated, unchanged by this document)

- No automatic repayment — order-placement code remains stripped from `alpaca_client.py`, unaffected by any finding in this research line.
- No leverage-cap change — the 1.8x structural cap remains a read-only reference throughout every scenario in this project.
- No production margin schema change — `targets.yaml`'s margin schema remains entirely `null`.
- No strategy parameter selection — no `repay_fraction`, tax rate, or lot convention is chosen as "the" answer anywhere in this document.

## 6. Outcome

**Evidence does not support changing research assumptions.**

Phase 6A's evidence narrowed the tax-lot cost estimate — a real, useful refinement — but did not cross a materiality boundary, did not resolve any of the four other named blockers, and did not surface a reason to revisit any prior research-cycle's methodology or the assumptions underlying it. This is not "Evidence supports changing research assumptions" (nothing here calls for revisiting how prior passes measured what they measured), and it is not "Evidence inconclusive" (the finding is clear and directly answers the question Phase 6A was built to ask — it simply doesn't change what that answer implies for governance).

**No production behavior changes authorized.**

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or `CLAUDE.md`.
- Does not change any prior research document's recorded conclusion, including `docs/PHASE5B_GOVERNANCE_DECISION.md`'s own decision (which this document evaluates, and reaffirms, but does not edit).
- Does not evaluate production adoption of Model B, any `repay_fraction`, or any repayment mechanic.
- Does not open Phase 7 or any further research cycle — that remains a separate, future decision.

Stopping here.
