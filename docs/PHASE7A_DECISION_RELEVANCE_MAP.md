# Phase 7A: Decision Relevance Map

> **⚠️ Synthesis only — no simulation, no code.** Maps execution-reality findings already established in `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md`, `docs/PHASE7A_BROKER_MECHANICS_ASSUMPTION_REGISTRY.md`, and `docs/PHASE7A_DATA_AVAILABILITY_ASSESSMENT.md` to the prior research conclusions they could affect. Does not change any prior conclusion, does not change `docs/PHASE5B_GOVERNANCE_DECISION.md`'s decision, and does not authorize any production, advisory, or repayment behavior.

_Written 2026-07-17, per `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §6d. Sources: the three Phase 7A documents above, `docs/PHASE5_DECISION_GATE_REVIEW.md`, `docs/PHASE5B_GOVERNANCE_DECISION.md`, `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md`. Every figure below is quoted from an already-committed source, not recomputed._

---

## Mapping table

| Execution Reality Item | Prior Finding Affected | Potential Impact Type | Current Evidence State | Governance Relevance |
|---|---|---|---|---|
| 1. Maintenance margin concentration escalation | Phase 4A's zero forced-deleveraging-events finding (the disqualifying leg of its "Evidence inconclusive" gate); `docs/PHASE5_DECISION_GATE_REVIEW.md`'s blocker list | **Narrow** — does not invalidate Phase 4A's recorded outcome (pre-committed, not reopened), but narrows how much weight "zero forced events" should carry as evidence of low real concentration risk, since the simulator has no mechanism that could ever detect a real, concentration-triggered maintenance escalation | Mechanism confirmed real and sourced (FINRA Rule 4210(g)(8)); Robinhood's specific house percentage(s) not yet obtained (`DATA_AVAILABILITY_ASSESSMENT.md` item 2 — obtainable with effort) | Does not reopen Phase 4A or change Phase 5B; flagged as the highest-relevance open item for any *future*, separately-approved concentration research cycle |
| 2. Forced liquidation mechanics | Every MaxDD figure across Phase 3/4A/6A; Model B/C's implicit framing that debt reduction only ever happens via a proactive policy choice | **Narrow** — does not invalidate any computed MaxDD number as a description of the simulated price path, but narrows the interpretation that a simulated MaxDD represents what this account would actually experience, since a real forced liquidation at a bad moment could crystallize a loss the simulator's daily mark-to-market recovery assumption never represents | General mechanism confirmed (no notice, no guaranteed cure period); specific sizing algorithm Permanently unavailable (`DATA_AVAILABILITY_ASSESSMENT.md` item 4) | Does not change any prior recorded MaxDD figure or Phase 5B; the proprietary sizing algorithm's unresolvability means this item cannot be fully closed by any future research effort |
| 3. Liquidation sequencing | Repayment behavior realism generally; Phase 6A's FIFO lot-selection realism specifically (which lots get sold depends on which tickers get trimmed) | **Only adds uncertainty** — no evidence found suggests real sequencing would systematically move any tested outcome in a particular direction | Broker discretion confirmed; specific algorithm Permanently unavailable | Does not change any prior finding; the simulator's pro-rata assumption remains disclosed as a simplification, unchanged in status |
| 4. Intraday margin timing | The once-per-simulated-day settlement assumption underlying every Phase 3–6A scenario | **Only adds uncertainty** — a granularity gap, not a directional one | Real timing confirmed to not guarantee next-day resolution; exact checkpoint mechanics Obtainable with effort, not yet obtained | Does not change any prior finding |
| 5. Execution costs/slippage | Transaction-cost sensitivity (`docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md`); Model B turnover findings (`docs/results/PHASE3_MODEL_B_ANALYSIS.md`) | **Only adds uncertainty** — the already-tested passes found erosion immaterial at every magnitude tested; real spread data could narrow or widen confidence but is not expected, on current evidence, to reverse the finding | No real bid/ask or fill data obtained; Obtainable with effort via a paid data source this project doesn't currently use (`DATA_AVAILABILITY_ASSESSMENT.md` item 7) | Does not change the closed transaction-cost or stress-timing findings (see "Items Already Closed" below) |
| 6. Borrowing-rate variability | Phase 3C's interest-rate assumption (`docs/PHASE3C_ASSUMPTION_REGISTRY.md` #10, previously labeled Estimated) and Phase 3G's interest-rate sensitivity sweep | **Narrow** — the flat 5% APR assumption is confirmed real and close to (modestly below) this account's actual applicable tier (~5.75% at this account's debt scale), narrowing rather than overturning an assumption already partially tested by Phase 3G's own sensitivity dimension | Current tiered structure confirmed (Publicly available, `REGISTRY.md` item 5); historical rate variation across the 2021–2026 simulated window not yet obtained (Obtainable with effort) | Does not change any Phase 3 result; upgrades one input's confidence level only |
| 7. Portfolio margin status | The 1.8x leverage cap's real-world meaning; every scenario's implicit standard-Reg-T-margin framing | **Only adds uncertainty**, on current evidence — `CLAUDE.md`'s doctrine text is already consistent with standard margin, so confirmation would most likely narrow rather than overturn the working assumption. **Note:** if this account were found to actually use portfolio margin, the impact type would be materially larger (a risk-based capacity calculation is a structurally different mechanism than a flat leverage ratio) — but nothing in current evidence suggests that outcome, so this is recorded as a low-probability tail case, not a live concern | This account's actual enrollment status Obtainable with effort (account-specific, resolvable directly by the account holder, not a research task) | Does not change any prior finding on current evidence |
| 8. Tax lot realism | Phase 6A's own result (`docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md`) and Phase 6B's "Evidence does not support changing research assumptions" outcome | **Already resolved** to the extent this research line intended — see "Items Already Closed" below | FIFO-realistic taxable base computed and compared against the prior upper bound; materiality classification unchanged at 25%/50% `repay_fraction`, remained sub-material at 10% | Already fully accounted for in `docs/PHASE6B_GOVERNANCE_REASSESSMENT.md`; not reopened by this document |

---

## Items With Potential Interpretation Impact

Only two items in this map are classified above as capable of narrowing (not invalidating, not strengthening in the sense of adding new support) how a prior finding should be read, rather than merely adding an unresolved uncertainty band around it:

- **Maintenance margin concentration escalation (item 1).** Phase 4A's "Evidence inconclusive" outcome hinged specifically on zero forced-deleveraging events being observed. This item establishes that the simulator's leverage-cap mechanism structurally cannot detect the one real, sourced brokerage mechanism (concentration-triggered maintenance escalation) most likely to produce a real analog of that event type. This does not mean Phase 4A's zero-events observation was wrong — it was computed correctly against the harness as built — it means the observation may carry less weight as evidence of *low real risk* than it would if the harness could represent this mechanism at all.
- **Forced liquidation mechanics (item 2).** Every MaxDD figure this project has ever produced describes a simulated price path with no risk of broker-initiated forced selling at an inopportune moment. This is a structural property of every scenario across Phase 3, 4A, and 6A alike, not specific to any one `repay_fraction` or Model choice.

Both items are narrowing findings, not invalidating ones: neither one reopens a pre-committed, closed backtest verdict, and neither changes a single previously reported number.

## Items That Only Reduce Uncertainty

Five items are classified as adding or narrowing uncertainty without any plausible path to reversing a prior conclusion, on current evidence:

- **Liquidation sequencing (item 3)** — no directional evidence either way.
- **Intraday margin timing (item 4)** — a granularity gap only.
- **Execution costs/slippage (item 5)** — already-tested passes found this immaterial; real data would refine, not reverse, that finding.
- **Borrowing-rate variability (item 6)** — narrows an already-tested assumption toward a slightly more precise, still-immaterial figure.
- **Portfolio margin status (item 7)** — current evidence favors the existing working assumption; the low-probability tail case is noted but not treated as a live concern.

## Items Already Closed

Three lines of research are explicitly not reopened by this document, each for a specific, stated reason:

- **Tax-lot modeling (Phase 6A).** Closed per `docs/PHASE6B_GOVERNANCE_REASSESSMENT.md`'s outcome ("Evidence does not support changing research assumptions"). The FIFO-realistic figure was computed, compared against the prior upper bound, and materiality classification did not change at any tested fraction. Nothing in this Phase 7A research line — which addresses execution/broker mechanics, a distinct subject from cost-basis/tax realism — bears on that already-answered question.
- **Transaction-cost sensitivity.** Closed per `docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md` — erosion immaterial at every tested magnitude (0/5/15bps), three orders of magnitude below the observed TWR/MaxDD gaps. Item 5 above (execution costs/slippage) revisits the *data quality* behind that finding's cost assumption, not the finding itself; per this project's standing "answer it once, don't relitigate without new evidence" discipline, revisiting data quality is not new evidence until real spread/fill data is actually obtained and shown to matter.
- **Stress timing analysis.** Closed per `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md` — repayment dollar volume structurally under-represented inside detected real stress windows at every `repay_fraction` (5.9–6.9% vs. a 12.2% base rate); threshold exposure 0.0% throughout. This Phase 7A research line's items 3/4/5 (sequencing, intraday timing, execution costs) touch adjacent execution-mechanics questions but do not reopen the specific, already-answered question of *when* Model B's trigger fires relative to detected stress.

## Governance Boundary

- **`docs/PHASE5B_GOVERNANCE_DECISION.md`'s decision remains unchanged.** "Maintain current doctrine" stands exactly as recorded; this document evaluates and maps evidence, it does not re-decide anything.
- **This document does not authorize advisory behavior, production changes, leverage changes, or repayment deployment of any kind.** `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, and `CLAUDE.md`'s Decisions Log are all untouched by this document and by every Phase 7A document before it.
- **Any future change requires a separate governance review.** If either of the two items flagged in "Items With Potential Interpretation Impact" is ever pursued further (e.g., successfully obtaining Robinhood's actual house maintenance percentage), the resulting evidence would require its own future, explicitly-approved governance synthesis before bearing on any decision — this map itself is not that review, and does not pre-authorize one.

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure — every number above is quoted from an already-committed source.
- Does not change `docs/PHASE5B_GOVERNANCE_DECISION.md`'s decision, or any other prior document's recorded conclusion, including Phase 4A's "Evidence inconclusive" outcome.
- Does not reopen the tax-lot, transaction-cost, or stress-timing questions.
- Does not modify `margin_simulation.py` or any other code, and does not touch any production file.
- Does not recommend pursuing any specific unresolved item over another, and does not authorize any next step beyond this synthesis.

Stopping here. This closes the Phase 7A research line's four planned deliverables (research plan, evidence inventory, broker mechanics registry, data availability assessment, decision relevance map). Awaiting direction on next steps.
