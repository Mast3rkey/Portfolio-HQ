# Phase 7A: Broker Mechanics Assumption Registry

> **⚠️ Documentation only — no simulation, no code.** Uses only findings already established in `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md`; introduces no new broker-behavior claim beyond what that document already sourced. Does not modify `docs/PHASE3C_ASSUMPTION_REGISTRY.md`, `docs/PHASE6A_ASSUMPTION_REGISTRY.md`, or any other prior registry — this is a new, separate registry for a new subject (execution-mechanics realism), not a revision of any existing one.

_Written 2026-07-17, per `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §6b. Same three-plus-one label discipline as every prior registry in this project (`docs/PHASE3C_ASSUMPTION_REGISTRY.md`, `docs/PHASE6A_ASSUMPTION_REGISTRY.md`), extended with the fourth category `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §6b itself defined for this specific subject: Permanently Unresearchable (no public source addresses it and none is expected to)._

## Labels

- **Known** — directly sourced in `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md`, citation traceable to a specific source.
- **Estimated** — a reasonable, disclosed inference from Known data, not itself directly stated.
- **Hypothetical** — a simulation-design choice with no claim to represent real broker behavior (used here for `margin_simulation.py`'s own modeling choices, not for broker facts).
- **Permanently Unresearchable** — no public source addresses it; internal to the brokerage, not expected to ever become available to this project.

---

## 1. Liquidation sequencing

| Field | Content |
|---|---|
| **Assumption/mechanic** | Which positions get sold, and in what order, when a repayment or forced sale is funded by trimming held positions. |
| **Simulator treatment today** | Pro-rata: `_fund_repayment()` sells the same fraction of every held position simultaneously (`margin_simulation.py`). |
| **Real-world evidence status** | Robinhood's disclosure confirms it retains full discretion and the customer has none (`PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md` §2 item 1, sources S1/S3). The specific algorithm is not published anywhere found. |
| **Classification** | **Known** that broker discretion exists and pro-rata is not confirmed as the real rule; **Permanently Unresearchable** for the specific sequencing algorithm itself. |
| **Decision relevance** | **Affects Phase 3 and Phase 6A.** Phase 3's `_fund_repayment()` mechanics underlie every Model B/C simulation; Phase 6A's FIFO realized-gain figures depend on *which* lots get sold, which depends on which tickers get trimmed, which depends on this sequencing assumption. **Adds uncertainty only** — no evidence suggests a specific real sequencing rule that would predictably move results in either direction; the simulator's own docstring already discloses pro-rata as "a simplification, not itself a strategic decision," and this registry does not change that disclosure's accuracy. |

## 2. Maintenance margin requirements

| Field | Content |
|---|---|
| **Assumption/mechanic** | The rule determining when an account is under-margined and must post more collateral or be liquidated. |
| **Simulator treatment today** | A single, uniform, portfolio-level `leverage_cap` (1.8x) — no per-position or concentration-aware maintenance concept anywhere in `margin_simulation.py`. |
| **Real-world evidence status** | FINRA Rule 4210 sets a 25% minimum maintenance floor for long equity, **and** a real, sourced concentration-based escalation — a position exceeding 50% of account equity can require 50–100% maintenance margin at broker discretion (Rule 4210(g)(8)/NTM 09-53) (`EVIDENCE_INVENTORY.md` §2 item 2, source S6). Robinhood's own house requirements can exceed the regulatory floor further, but the specific house percentage(s) were not found (S1/S2). |
| **Classification** | **Known** that a concentration-triggered maintenance escalation mechanism exists at the regulatory level; **Unknown** the exact percentages Robinhood applies and when the escalation actually triggers in practice at this brokerage. |
| **Decision relevance** | **Affects Phase 4A most directly, and Phase 5B by extension.** Phase 4A's concentration research measured zero forced-deleveraging events across every tested scenario, using a harness whose only leverage enforcement is the uniform 1.8x cap — it has no mechanism that could ever detect a concentration-triggered maintenance call, because no such mechanism exists in the simulator at all. **This could change interpretation, not merely add uncertainty**: if a real concentrated position (e.g., NVDA at the 2.14x-of-target level `t1t2_trim_backtest.md` and `PHASE4A_RESEARCH_REPORT.md` both examined) would trigger a real, tighter, concentration-specific maintenance requirement that the simulator cannot represent, Phase 4A's "Evidence inconclusive" outcome — which hinged specifically on zero forced-deleveraging events — may understate real concentration risk rather than correctly finding no effect. This is the single highest-relevance item in this registry. |

## 3. Intraday margin calls

| Field | Content |
|---|---|
| **Assumption/mechanic** | Whether a margin deficiency must be cured same-day/intraday or can wait until the next simulated trading day. |
| **Simulator treatment today** | Once-per-simulated-day evaluation and settlement, entirely at that day's close — no intraday check exists anywhere in `margin_simulation.py`. |
| **Real-world evidence status** | Robinhood's disclosure confirms no guaranteed extension of time on a margin call, and deposits to resolve a call "typically" resolve intraday but can take up to one business day (`EVIDENCE_INVENTORY.md` §2 item 3, sources S1/S4). |
| **Classification** | **Known** that real margin-call timing does not match the simulator's once-daily cycle; **Unknown** the exact intraday checkpoint frequency or cutoff mechanics. |
| **Decision relevance** | **Affects Phase 3 (all scenarios) and Phase 6A.** Every simulated repayment event's day-index and dollar amount assumes a single daily settlement point. **Adds uncertainty only** — no evidence found suggests this timing difference would systematically favor or disfavor any tested `repay_fraction` or Model B/C outcome; it is a granularity gap, not a directional one. |

## 4. Forced liquidation rules

| Field | Content |
|---|---|
| **Assumption/mechanic** | Whether and how a broker can sell positions without the account holder's initiation, to cure a margin deficiency. |
| **Simulator treatment today** | **No forced-liquidation mechanic exists anywhere in `margin_simulation.py`.** Debt is only ever repaid when a specific policy (Model A/B/C) proactively chooses to; a cap breach from a price decline on already-drawn debt is never itself detected or corrected by the engine. |
| **Real-world evidence status** | Robinhood's disclosure confirms it may forcibly liquidate "regardless of your intent to satisfy a margin call... with or without your prior approval," with no guaranteed cure period (`EVIDENCE_INVENTORY.md` §2 item 4, sources S1/S3). |
| **Classification** | **Known** that this is a real, confirmed brokerage mechanic entirely absent from the simulator; **Unknown** the specific sizing rule (minimum-to-cure vs. buffer amount) Robinhood applies when it does liquidate. |
| **Decision relevance** | **Affects Phase 3, Phase 4A, and Phase 6A.** This is the most structurally significant gap in the registry: every MaxDD figure this project has ever produced (Phase 3's D-0 control, every Model B/C arm, Phase 4A's concentration constructions) assumes the account rides out a drawdown exactly as simulated, with no risk of a real, broker-initiated forced sale crystallizing a loss at a worse moment than the simulator's own daily mark-to-market. **This could change interpretation, not merely add uncertainty**, for the same reason as item 2 — it is the mechanism by which a real concentration or leverage breach would actually resolve in practice, and the simulator cannot represent it at all, in any scenario, regardless of `repay_fraction` or Model choice. |

## 5. Borrowing-rate variability

| Field | Content |
|---|---|
| **Assumption/mechanic** | The margin interest rate applied to outstanding debt. |
| **Simulator treatment today** | A flat `INTEREST_APR` (5% in every Phase 3–6A run), with the first $1,000 interest-free — matching `CLAUDE.md`'s doctrine text. |
| **Real-world evidence status** | Confirmed tiered, not flat: first $1,000 free, then ~5.75% up to $50,000, stepping down at higher balances (`EVIDENCE_INVENTORY.md` §2 item 6, source S5, dated as of December 2025 by the source and subject to change without notice). |
| **Classification** | **Known** (upgraded from `PHASE3C_ASSUMPTION_REGISTRY.md` #10's prior "Estimated" flat-5% label — this registry does not edit that document, but records the upgrade here for this new registry's own purposes). |
| **Decision relevance** | **Affects Phase 3 (interest accrual in every scenario).** This account's real debt scale (well under $50,000 throughout every simulated window, and its actual current ~$1,600 balance) falls entirely within the lowest confirmed tier (~5.75%), close to but modestly above the simulator's flat 5% assumption. **Adds uncertainty only, and only a small amount** — Phase 3G already tested an interest-rate sensitivity dimension (`interest_sensitivity` in `docs/results/PHASE3_SENSITIVITY_RESULTS.json`), so this item narrows an already-partially-tested assumption rather than surfacing an entirely new one. |

## 6. Portfolio margin

| Field | Content |
|---|---|
| **Assumption/mechanic** | Whether this account's margin capacity is computed under standard Reg T rules (flat 50% initial / 25%+ maintenance) or a risk-based portfolio margin methodology. |
| **Simulator treatment today** | Implicitly assumes standard-margin-style mechanics — a single fixed leverage ratio, not a risk-based haircut calculation. |
| **Real-world evidence status** | Regulation T's standard 50% initial margin requirement is confirmed (`EVIDENCE_INVENTORY.md` §2 item 7, source S7). Whether this account uses or qualifies for Robinhood's portfolio margin offering was not established by any source consulted. |
| **Classification** | **Known** for the Reg T standard-margin baseline; **Unknown** whether it applies to this specific account rather than a portfolio-margin regime. |
| **Decision relevance** | **Affects Phase 3 and Phase 5B (the 1.8x leverage cap's real-world meaning).** `CLAUDE.md`'s doctrine text describes this account's margin usage in terms consistent with standard margin (a flat leverage cap, a flat buffer percentage), which is suggestive but not confirmed. **Adds uncertainty only** — no evidence found indicates this account is actually on portfolio margin; absent contrary evidence, the standard-margin assumption underlying every prior simulation remains the best-supported one, not a confirmed fact. |

## 7. Execution timing differences

| Field | Content |
|---|---|
| **Assumption/mechanic** | The gap between a trading decision and an actual, filled trade. |
| **Simulator treatment today** | Instant, full fill at that simulated day's close price, every time, for every trade in every scenario — no latency, no partial fill, no failure. |
| **Real-world evidence status** | Not a broker-specific finding from this pass's sources — this is a structural property already acknowledged by this project's own doctrine: `CLAUDE.md` states orders are placed manually on Robinhood by the account holder, not automatically, meaning real execution timing already includes human decision and action latency beyond even what an automated broker's own execution speed would add. No new source contradicts or quantifies this. |
| **Classification** | **Known** as a structural, already-acknowledged property of this tool's design (advisory-only, manual execution) — not a new finding from this registry, but restated here because it belongs in the same "simulator vs. reality" inventory as every other item. |
| **Decision relevance** | **Affects every phase equally (Phase 3, 4A, 5B, 6A) and changes no interpretation.** This is not new uncertainty — `CLAUDE.md`'s "NEVER places orders... I execute manually" framing already exists specifically because of this gap, and no simulation in this project has ever claimed to model real-time execution. Recorded for completeness, not as a new open question. |

## 8. Slippage/spread behavior during stress

| Field | Content |
|---|---|
| **Assumption/mechanic** | How much a trade's real execution price differs from the simulator's reference close price, especially during volatile or illiquid conditions. |
| **Simulator treatment today** | `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md`'s disclosed, bounded regime-conditional cost multiplier (a hypothetical overlay on detected real-OHLCV stress windows) — never a measured bid-ask spread or fill-price observation. |
| **Real-world evidence status** | Not investigated in this pass — explicitly carried forward, unresolved, from `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §4 item 5's own scoping, which deferred this to avoid re-litigating the already-closed stress-regime item. No new source was sought here. |
| **Classification** | **Unknown**, unchanged from before this registry. |
| **Decision relevance** | **Affects Phase 3 (transaction-cost sensitivity) and the stress-regime item.** Both already found cost erosion immaterial at every tested magnitude, using disclosed, bounded, non-measured assumptions. **Adds uncertainty only** — no evidence in this pass moves this finding in either direction; real spread behavior during genuine stress remains unmeasured by this project. |

---

## Summary

| # | Item | Classification | Could change interpretation? |
|---|---|---|---|
| 1 | Liquidation sequencing | Known (discretion exists) / Permanently Unresearchable (algorithm) | No — adds uncertainty only |
| 2 | Maintenance margin requirements | Known (mechanism) / Unknown (specifics) | **Yes — highest relevance item** |
| 3 | Intraday margin calls | Known (mismatch) / Unknown (specifics) | No — adds uncertainty only |
| 4 | Forced liquidation rules | Known (mechanism) / Unknown (sizing) | **Yes — second-highest relevance item** |
| 5 | Borrowing-rate variability | Known | No — narrows an already-tested assumption |
| 6 | Portfolio margin | Known (Reg T baseline) / Unknown (this account's status) | No — adds uncertainty only |
| 7 | Execution timing differences | Known (already-acknowledged design property) | No — restates an existing disclosure |
| 8 | Slippage/spread during stress | Unknown | No — adds uncertainty only, unchanged from before |

---

## What this document deliberately does not do

- Does not introduce any broker-behavior claim not already sourced in `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md`.
- Does not modify `docs/PHASE3C_ASSUMPTION_REGISTRY.md`, `docs/PHASE6A_ASSUMPTION_REGISTRY.md`, or any other prior registry.
- Does not convert any identified simulator gap into a recommendation, a code change, or a production-behavior proposal.
- Does not change `docs/PHASE5B_GOVERNANCE_DECISION.md`'s "maintain current doctrine" decision — items 2 and 4 are flagged as capable of changing *interpretation* of a prior finding, which is a distinct, narrower claim than changing a governance decision; whether either actually does so is a future, separate assessment (`docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §6d), not this document.
- Does not select, rank, or recommend a `repay_fraction`, lot convention, or leverage-cap change.

Stopping here. Awaiting direction on the next Phase 7A deliverable (data availability assessment / decision relevance synthesis).
