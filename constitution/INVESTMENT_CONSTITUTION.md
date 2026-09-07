# Investment Constitution

_Adopted 2026-07-18 (`governance/decisions/GOV-0001-governance-architecture-adopted.md`). Distills principles already adopted in CLAUDE.md's Decisions Log — this document originates nothing new. It exists so the **why** behind the system's non-negotiable rules survives independent of any specific numeric value, ticker, or gate implementation._

**This Constitution is the highest-authority statement of the system's durable governing principles.** CLAUDE.md is the operational synthesis and current-parameter record — current parameters, workflow, and the full narrative Decisions Log live there and change as the portfolio does. CLAUDE.md operates under this Constitution, not alongside or above it. This document changes rarely, and only through its own amendment process (§7). If this document and a lower-authority source conflict, this document remains controlling; a material, task-relevant conflict must be surfaced, and the affected mutation is blocked until the lower-authority source is corrected or this document is amended through §7. Recency or specificity never permits a lower-authority source to override it. See §8 and `governance/decisions/GOV-0002-operational-precedence-hierarchy.md`.

**Two domain constitutions extend this one by reference, not duplication**: `docs/MARGIN_DOCTRINE.md` (margin philosophy, in full) and `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` (Company/Theme Intelligence's non-negotiables, §20/24). Their content is not repeated here — this document states the same underlying principles at a higher level and points to them for the complete argument.

---

## 1. What this tool is

A decision-support advisor, not a trading system. It computes recommendations; a human executes every trade manually. Order-placement methods are deliberately absent from `alpaca_client.py` and are not to be reintroduced. Tool output is combined with judgment, not substituted for it — and the tool is expected to push back when its own operator breaks the system's own rules, not defer silently.

## 2. Manual execution over automation — why, not just what

This is not a stylistic preference. In June 2026 a band-overlay automated-trading backtest returned 227% against a 422% buy-and-hold baseline on the same basket — a NO-GO result stated plainly: elaborate analysis layers were anti-predictive, and whatever edge existed lived entirely in the base signal, not in the automation wrapped around it. Every later "should we add a new analysis/research/thesis layer" question in this system's history has been checked against that result first. It is the empirical grounding for Principle 4 below, not an assumption.

## 3. Margin is risk governance, not alpha

Margin only amplifies whatever edge the underlying portfolio already has — it is not itself a source of edge. This is a mathematical identity, not an empirical claim, and no evidence changes it.

Discretionary or predictive judgment may never increase leverage beyond a governed recommendation or the fixed cap, and may never bypass the buffer floor or a repayment rule — this remains absolute. The operator may always decline a recommendation, use less margin than recommended or allowed, or repay more or sooner than any rule requires: discretion in this system is asymmetric, always available to reduce risk, never available to exceed a governed limit.

Separately: whether a rules-based, pre-registered, evidence-gated conditional rule — keyed to observable account- or market-state conditions, evaluated net of financing cost and realistic risk constraints — outperforms a fixed posture is an open empirical question, not a closed one. It may be researched only under its own separately governed research charter, and adopted only through its own separate governance decision meeting this system's existing evidentiary bar. Opening a research charter authorizes nothing on its own.

Margin interest is a guaranteed cost, treated as a hurdle rate, never a rounding error. The 1.8x leverage cap and 30% buffer floor remain unchanged by this amendment. Any conditional rule later adopted operates strictly inside those limits — no dynamic rule may raise the cap or lower the floor; changing either requires its own separate future constitutional or governance decision. A high buffer, a low maintenance ratio, or any other favorable-looking account signal is never, by itself, automatic permission to borrow more.

The full doctrine lives in `docs/MARGIN_DOCTRINE.md`, brought into conformance with this amendment (`governance/decisions/GOV-0003-margin-conditional-research-permitted.md`).

## 4. No predictive research

No price targets, no "opportunity maps," no standing research or scoring layer that runs ahead of a deposit and tells the operator what to buy before there's money to allocate. Opportunities are computed at runtime, on deposit day, from live data and current gaps against target — never precomputed, never speculative. A proposal to add a new analysis, research, or thesis-generation system must be checked against Principle 2's evidence first.

A bounded, retrospective, pre-registered backtest into whether a rules-based conditional margin-deployment or repayment rule would have historically produced a better net risk-adjusted outcome is not, by itself, the standing predictive layer this principle excludes — provided it produces no live signal, opportunity map, price target, opaque score, continuous indicator, or precomputed recommendation, and authorizes no automation or production behavior on its own. Any operational rule such research might suggest requires its own separate governance decision, under the same evidentiary bar as every rule in this system; recommendation-only, manual execution is unaffected throughout and after any such research.

## 5. Fixed, mechanical, no-exception limits

Certain risk limits in this system are doctrine, not backtest verdicts, and are deliberately immune to discretionary override: the leverage cap, the buffer floor, the correlated-cluster caps, and the T1/T2 concentration ceiling all share this shape. They exist because the cost of a wrong tail-risk call under leverage outweighs the value of flexibility, and because a single overweight, correlated, or over-leveraged position compounding unchecked is a forced-liquidation risk no time-weighted-return backtest can price. State the limit, apply it, and don't relitigate it without a genuinely new leverage regime in the data — not a new opinion about the current one.

## 6. Verify before acting on external review

Any claim about this repository's code, data, or behavior that originates outside a live session with real file and data access — a different chat, an outside review, an uploaded document — is treated as unverified until confirmed directly against the actual code or file. This has caught concrete errors before (a stale price, a wrong assumed function return value) and applies to every future external input the same way, including this document's own future amendments.

## 7. Amendment process

This document changes less often, and with more deliberation, than an ordinary committee decision. An amendment requires its own governance decision (see `governance/decisions/`), explicitly categorized as a constitutional amendment rather than an ordinary decision, and must state what principle is changing and why the prior version no longer holds. It is not amended as a side effect of an unrelated policy change, a new company review, or a new tier decision — those operate at the Policy and Company/Theme layers below this one and do not, by themselves, alter anything here.

## 8. Operational precedence

CLAUDE.md is this system's operational synthesis — current parameters, workflow, and narrative decision index — not a superior authority. Where sources conflict, higher authority remains controlling; a lower-authority source cannot override, amend, or silently supersede a higher one. A material, task-relevant conflict blocks the affected mutation until it is reconciled. The lower-authority source is corrected to match, unless the higher-authority source is itself amended through its own governed process. Recency or specificity never permits a lower-authority source to override a higher one. The complete operational precedence hierarchy, and its full conflict-resolution rules, are stated in `governance/decisions/GOV-0002-operational-precedence-hierarchy.md`, not reproduced here.

---

_Changelog: 2026-07-18 — initial adoption (GOV-0001). 2026-07-20 — introduction conflict sentence revised, §8 (Operational precedence) added; complete cross-document authority hierarchy stated in `governance/decisions/GOV-0002-operational-precedence-hierarchy.md` (GOV-0002). 2026-07-21 — §3 narrowed to permit bounded, evidence-gated conditional-margin research under separate governance while preserving the no-alpha identity, asymmetric operator discretion, and the unchanged 1.8x cap/30% buffer floor; §4 gained a narrow carve-out for exactly that research (`governance/decisions/GOV-0003-margin-conditional-research-permitted.md`)._
