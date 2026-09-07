# Phase 7A — Execution Reality Research Plan

> **⚠️ Planning document, not a result.** No simulation has been run, no broker data has been collected, and no code has been written. This document defines what research is needed to determine whether the simulated margin-repayment mechanics this project has studied since Phase 3 correspond to real brokerage execution — it does not itself answer that question.

_Written 2026-07-17, per direct instruction following `docs/PHASE6B_GOVERNANCE_REASSESSMENT.md`'s "Evidence does not support changing research assumptions" outcome, which named four of five governance blockers as entirely untouched by Phase 6A: real execution/slippage modeling, real broker margin behavior, human workflow design, and regime diversity. This plan addresses the first two of those directly. Documentation only — no code, no broker integration, no production files, no doctrine changes. Do not implement until this plan is approved._

---

## 1. Sources reviewed

`docs/PHASE5B_GOVERNANCE_DECISION.md` (§3's evaluation of Decision 2, which named "real execution/slippage modeling" and "real broker margin behavior" as two of the five blockers preventing advisory-only expansion; §5's blocker list, items 2 and 3 specifically), `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` (§8's remaining-unknowns list, which explicitly carries forward "execution-layer realism... and real broker margin mechanics" as untouched by the tax-lot work), `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` (the "Phase 6A reconciliation" section's reassessment of execution modeling and broker mechanics as "already named, tracked blockers in the Phase 5 governance documents... not new research questions this backlog needs to independently number" — this plan is that tracked blocker becoming a formally scoped research item), and `margin_simulation.py` itself, read directly to confirm the current simulated mechanics this plan evaluates against reality (§3 below).

## 2. Research question

**"What parts of the simulated margin repayment process are realistic, unknown, or structurally different from actual brokerage execution?"**

This is explicitly a **classification** question, not a correction or calibration question. It does not ask "how do we make the simulator match Robinhood exactly" — it asks which of the simulator's existing mechanics have a real-world analog worth trusting, which are genuinely unknown (no data exists either way), and which are known to diverge structurally (the simulator does something a real broker provably does not, or vice versa). This mirrors the classification discipline every prior phase in this line has used (Known/Estimated/Hypothetical labeling) applied to a new subject: not the simulation's *financial* assumptions (tax rate, cost basis, deposit cadence — already covered), but its *execution-mechanics* assumptions.

**Why this closes something the prior research line could not.** Every simulation in Phases 3–6A shares one property: repayment execution is assumed to work exactly as `margin_simulation.py` implements it — cash-first funding, pro-rata trim across positions, fill at that day's close, no slippage, no broker-side rejection or delay. No document in this project has ever asked whether that assumption is itself realistic. The tax-lot work (Phase 6A) made the *tax* side of a repayment event more realistic; it left the *execution* side of that same event exactly as unexamined as it was in Phase 3B.

## 3. Known (simulator behavior, verified by direct code read)

These are facts about what `margin_simulation.py` actually does — not claims about what a real broker does. Listed here as the baseline this research classifies against.

- **Cash-first repayment.** `_fund_repayment()` draws from idle cash before selling any position (`from_cash = min(cash, repay)`).
- **Pro-rata trimming.** When cash is insufficient, the remaining amount is raised by selling the same fraction (`frac = still_needed / gross`) of every held position simultaneously — never a targeted sale of one position, never a largest-position-first or smallest-position-first rule.
- **Event timing.** Two distinct evaluation points exist: `pre_trade_fn` (Model B/C, evaluated on the day's opening mark-to-market state, before that day's deposit/allocation) and `repayment_fn` (Model 0/A, evaluated after deposit-allocation). Both types of repayment execute and settle same-day, at that day's close price, with no execution delay.
- **Lot consumption behavior (Phase 6A addition).** FIFO — oldest lot consumed first — applied identically regardless of which ticker, position size, or market condition is involved.
- **No rejection, no partial fill, no execution failure of any kind, anywhere in the engine.** Every repayment that is requested is fully funded, every day, unconditionally (bounded only by available cash + saleable position value, never by a broker-side constraint).
- **No margin-call mechanic at all.** The simulator's only leverage-related enforcement is `_leverage_capped_margin()`, which *prevents new margin draws* from exceeding the cap — it has no separate, distinct "maintenance call" concept, no intraday check, and no forced-liquidation-at-a-worse-price behavior. A breach of the cap (e.g., from a price decline on already-drawn debt) is never itself detected or acted on by the engine outside of whatever a specific repayment policy (Model A/B/C) chooses to do about it.

## 4. Unknown (named, not yet researched)

Each item below is a genuine gap this plan exists to investigate — not a claim about which way the answer will go.

1. **Broker liquidation sequencing.** When Robinhood force-liquidates to meet a margin call, what determines sale order (largest position, most liquid position, most recently purchased, account holder's stated preference, something else)? The simulator's pro-rata assumption is a modeling convenience, explicitly disclosed as such (`_fund_repayment()`'s own docstring: "a disclosed simplification, not itself a strategic decision") — never claimed to match a real sequencing rule.
2. **Maintenance margin calculation differences.** Real brokers typically apply per-position maintenance requirements (higher for volatile/concentrated names, sometimes house requirements above the regulatory 25% minimum) rather than a single portfolio-level leverage ratio. The simulator's single aggregate leverage cap is a simplification of unknown fidelity to this.
3. **Intraday margin calls.** The simulator evaluates and settles everything once per simulated trading day, at the close. Real margin calls can be issued and require action *intraday*, sometimes with same-day (not next-day) deadlines. Whether this timing difference matters for any conclusion this project has drawn is unknown.
4. **Forced liquidation rules.** Beyond sequencing (item 1): does a broker liquidate the *minimum* needed to cure a call (closer to the simulator's behavior) or a larger buffer amount? Is there a grace period, and if so how long?
5. **Spread/slippage behavior during stress.** Named already in `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md`'s own scope and left explicitly unresolved by that phase (which used a real-OHLCV-derived *proxy*, never real bid-ask or fill data) — carried forward here as still open, not re-litigated.
6. **Borrowing-rate variability.** `CLAUDE.md`'s doctrine text itself flags the ~5% APR figure as approximate ("~5% APR" — already registered as **Estimated**, not Known, in `docs/PHASE3C_ASSUMPTION_REGISTRY.md` #10). Whether the rate varies with debt size, market conditions, or account tier over time is unknown.
7. **Portfolio margin differences.** Robinhood's standard margin account uses Reg T rules; portfolio margin (a different, risk-based methodology available to larger/qualifying accounts) computes buying power and maintenance requirements differently. Whether this account uses or could use portfolio margin, and whether that would change any prior finding's applicability, is unknown.

## 5. Scope

**Research only.** This plan produces documentation — an evidence inventory, an assumptions registry, and a decision-relevance assessment. It does not:

- Integrate with any broker API or Robinhood-specific data source.
- Modify `margin_simulation.py`, `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py`.
- Change any repayment mechanic, trigger, or parameter in Model 0/A/B/C.
- Propose a new simulator feature (e.g., "add a maintenance-margin submodule") — if the research below identifies that a specific mechanic is both unknown *and* material to a prior conclusion, that would be a **separate**, future, explicitly-approved implementation phase, not an automatic next step from this plan.
- Recommend any doctrine change, leverage-cap change, or production behavior change of any kind.

**What "research" means here, concretely:** primarily a **documentation and inventory exercise**, not a simulation-execution exercise like Phases 3–6A. The evidence available is not backtestable historical price data (this project's usual evidentiary base) — it is publicly available broker policy documentation (Robinhood's margin disclosure/agreement documents, FINRA/Reg T public rules) and this project's own already-recorded assumptions about borrowing costs and leverage mechanics. Where no public documentation answers a question (e.g., Robinhood's specific internal liquidation-sequencing algorithm, which brokers do not typically publish), that item is recorded as **permanently or near-permanently unresearchable from outside the brokerage**, the same category `docs/PHASE5_DECISION_GATE_REVIEW.md` already used for real historical margin behavior.

## 6. Required outputs

Four deliverables, each with a defined shape, to be produced if this plan is approved for execution:

### 6a. Evidence inventory

A structured list of every source consulted (Robinhood's public margin disclosure documents, FINRA Rule 4210, Regulation T, any other publicly available regulatory or brokerage-published material) with, for each source: what it actually states, what question from §4 it bears on, and how directly (a source stating a specific numeric maintenance requirement is direct evidence; a source describing general margin-call *concepts* without brokerage-specific detail is indirect/contextual evidence only).

### 6b. Broker-mechanics assumptions registry

Following this project's standing three-label discipline (`docs/PHASE3C_ASSUMPTION_REGISTRY.md`'s Known/Estimated/Hypothetical pattern, reused unchanged), one row per §4 item (and any sub-questions the evidence inventory surfaces), classified as:
- **Known** — directly stated in a source found during 6a, specific to this account's actual broker (Robinhood) where possible.
- **Estimated** — a reasonable, disclosed inference from general regulatory rules (Reg T, FINRA) where Robinhood-specific documentation doesn't exist or wasn't found, with the inference's basis stated.
- **Hypothetical / Unresearchable** — no public source addresses it at all (e.g., internal liquidation-sequencing logic); explicitly named as a permanent-or-near-permanent gap, not silently assumed.

### 6c. Data availability assessment

For each §4 item: is the needed information (i) publicly documented and findable, (ii) not published but could plausibly be obtained by contacting the broker or reading account-specific agreement documents this account holder has access to, or (iii) not obtainable by any means available to this project (proprietary broker logic). This directly determines whether an item is closeable now, closeable with more effort, or permanently open — the same three-tier structure `docs/PHASE6A_DATA_REQUIREMENTS.md` used for tax-lot data, applied here to a genuinely different data-availability profile (that phase found *zero* external data was needed; this one is likely to find the opposite for several items).

### 6d. Decision relevance

For each §4 item found to be Known or Estimated (6b), an explicit statement of which prior research conclusion, if any, it bears on — and whether resolving it would plausibly change that conclusion's materiality classification, or is merely descriptive context with no effect on any number this project has already produced. This is the step that prevents this research from becoming an open-ended "learn everything about margin mechanics" exercise: every finding must trace back to a specific prior conclusion it either strengthens, weakens, or leaves untouched.

## 7. Materiality and interpretation discipline (reused, not reinvented)

- The existing 2.0pp material / 0.5pp noise floor bands (`docs/PHASE4A_MATERIALITY_THRESHOLDS.md`) apply if and only if this research produces a *quantifiable* figure comparable to a prior TWR/MaxDD gap (e.g., if real maintenance-margin requirements imply a materially different effective leverage cap than 1.8x, that comparison would use the existing bands). Most of §4's items are not expected to produce a directly quantifiable figure at all — they are mechanics/timing/sequencing questions, not parameter values — so this plan does not assume every item will resolve into a number.
- Interpretation language, when this plan is executed, must use the same "Evidence shows / Evidence does not show / Remaining unknowns" framing established in `docs/PHASE6A_TAX_LOT_EVIDENCE_RECORD.md` §7, not "we found" or "we confirmed."

## 8. Allowed conclusions (for the eventual execution, not this plan)

- Classifying each §4 item as Known/Estimated/Hypothetical-Unresearchable, with the evidence basis stated.
- Stating which prior research conclusion (if any) each classified item bears on, and whether the gap is currently material to that conclusion or merely descriptive.
- Recommending, if evidence supports it, which specific unresolved item(s) would be highest-value to pursue further (e.g., contacting the broker directly for maintenance-requirement specifics) — as a **research prioritization observation**, not a broker-integration or production authorization.

## 9. Prohibited conclusions

- **No broker integration of any kind** — this plan and its execution produce documentation, never a live data connection, API integration, or automated broker query.
- **No production changes** — `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py` remain untouched by this plan and its execution.
- **No strategy changes** — Model 0/A/B/C mechanics, `repay_fraction` values, the 1.8x leverage cap, and the 30% buffer floor are not modified, tuned, or re-evaluated for change by this research.
- **No doctrine change** — `CLAUDE.md`'s Decisions Log is not touched by this plan or its execution.
- **No recommendation for or against Model B, any `repay_fraction`, or any repayment mechanic** — this research evaluates execution-mechanics realism, not repayment-policy merit; those are separate questions this project has already closed once (`docs/PHASE6B_GOVERNANCE_REASSESSMENT.md`) and does not reopen here.
- **No claim that a Known/Estimated broker-mechanics fact retroactively changes any prior simulation result** — if a gap is found to be material to a prior conclusion (per §6d), that is itself a new, separate finding requiring its own future research/decision cycle, not an automatic correction applied here.

---

## What this plan deliberately does not do

- Does not consult, query, or integrate with any broker system or API.
- Does not modify `margin_simulation.py` or any other code.
- Does not change any repayment mechanic, parameter, or the leverage cap.
- Does not recommend a repayment policy or change any doctrine.
- Does not assume every §4 item will resolve into a quantifiable figure — most are expected to remain qualitative (mechanics/sequencing/timing) findings.

Stopping here. Awaiting approval before implementation (§6's four deliverables).
