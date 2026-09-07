# Phase 7A — Execution Reality Evidence Inventory

> **⚠️ Documentation only — no simulation, no code.** This document inventories publicly available evidence about real brokerage margin mechanics, for comparison against the simulated mechanics `margin_simulation.py` already implements (§3 of `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md`). It does not run anything, does not change `margin_simulation.py` or any other code, and does not alter `docs/PHASE5B_GOVERNANCE_DECISION.md`'s "maintain current doctrine" decision. Nothing here infers unrecorded broker behavior — every claim below is either directly sourced (cited inline) or explicitly marked Unknown/Unresearchable.

_Written 2026-07-17, per `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §6a's evidence-inventory deliverable. Sources: Robinhood's own published support articles and legal/disclosure documents, FINRA's public rulebook, and Regulation T (12 CFR Part 220). All sources are publicly available; none required brokerage account access or non-public data. Retrieved 2026-07-17 — Robinhood may change these figures/policies at its own discretion without notice (several sources below say so explicitly), so every figure here should be treated as a snapshot, not a permanent fact._

---

## 1. Sources consulted

| # | Source | Type | Publicly available? |
|---|---|---|---|
| S1 | [Robinhood Financial and Robinhood Securities Margin Disclosure Statement](https://cdn.robinhood.com/assets/robinhood/legal/RHF%20and%20RHS%20Margin%20Disclosure%20Statement.pdf) (PDF) | Brokerage-specific legal disclosure | Yes |
| S2 | [What's the total maintenance requirement?](https://robinhood.com/us/en/support/articles/margin-maintenance/) — Robinhood support article | Brokerage-specific | Yes |
| S3 | [ROBINHOOD CUSTOMER MARGIN ACCOUNT AGREEMENT](https://cdn.robinhood.com/assets/robinhood/legal/RHS%20Customer%20Margin%20Account%20Agreement.pdf) (PDF) | Brokerage-specific legal agreement | Yes |
| S4 | [What does it mean if I get a margin call?](https://robinhood.com/us/en/support/articles/margin-calls/) — Robinhood support article | Brokerage-specific | Yes |
| S5 | [Robinhood margin rates](https://robinhood.com/us/en/support/articles/margin-rates/) — Robinhood support article | Brokerage-specific | Yes |
| S6 | [FINRA Rule 4210: Margin Requirements](https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210) | Regulatory (SRO rule, applies to all FINRA member brokers, including Robinhood) | Yes |
| S7 | [Regulation T — 12 CFR Part 220](https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-220) | Regulatory (Federal Reserve Board rule) | Yes |
| S8 | [Futures deficits and margin calls](https://robinhood.com/us/en/support/articles/futures-deficits-and-margin-calls/) — Robinhood support article | Brokerage-specific (futures accounts — this account does not trade futures; included for contrast only, see §2 item 3) | Yes |

**Note on access:** S1–S5 and S8 (Robinhood's own pages) returned HTTP 403 when fetched directly by this session's tooling — the content cited below comes from search-result summaries of those pages, not a direct full-document fetch. This is disclosed as a real limitation on source directness: the citations are accurate to the search tool's extraction of each page's content, not independently re-verified against the raw page. This is a materially weaker evidentiary basis than this project's usual "read the actual file" discipline (e.g., reading `margin_simulation.py` directly) and is flagged here rather than presented as equivalent-strength evidence.

## 2. Findings by research question (per `PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §4)

### 1. Broker liquidation sequencing

**Known:** Robinhood's own disclosure states the customer is "not entitled to choose which securities or other assets in your account(s) are liquidated or sold to meet a margin call" (S1), and that Robinhood "may forcibly liquidate all or part of your account without prior notice... may sell your securities or other assets without contacting you" (S1, S3). This confirms, as a directly sourced fact, that Robinhood retains full discretion over which positions to sell and in what order.

**Unresearchable:** The actual algorithm or policy Robinhood's systems use to decide *which* positions to sell first when liquidating (largest position, most liquid, most recently purchased, or some other rule) is not stated in any source found. This is standard for brokerages — internal liquidation-sequencing logic is not typically published, and no source found (public or brokerage-issued) states Robinhood's specific rule. Classified **Permanently or near-permanently Unresearchable** from outside the brokerage, per `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §5's own anticipated category.

**Comparison to simulator:** `margin_simulation.py`'s `_fund_repayment()` uses pro-rata trimming (an equal fraction of every position). No source found confirms or denies this matches Robinhood's real sequencing — the simulator's own docstring already discloses this as "a simplification, not itself a strategic decision," which this evidence does not contradict or confirm.

### 2. Maintenance margin calculation differences

**Known:** FINRA Rule 4210 sets a **25% minimum maintenance margin** for long equity positions carried in a margin account (S6) — this is a regulatory floor, not a Robinhood-specific number, but it applies to Robinhood as a FINRA member. Separately, Robinhood's own disclosure states it "can change its maintenance margin requirements at any time without prior notice" and may apply "house" requirements above the regulatory minimum (S1, S2).

**Known:** FINRA Rule 4210(g)(8) and related guidance (Notice to Members 09-53) impose **higher maintenance requirements for concentrated positions** — a position representing more than 50% of account equity can require 50–100% maintenance margin at the broker's discretion (S6). This is a real, sourced, and directly relevant divergence from this project's own simulated mechanics: **`margin_simulation.py` has no per-position or concentration-aware maintenance-margin concept at all** — its only leverage enforcement is a single portfolio-level `leverage_cap` (1.8x, applied uniformly regardless of any single position's weight).

**Unknown:** Robinhood's specific "house" maintenance requirement percentage (i.e., the number it actually uses above the 25% FINRA floor) was not found in any source consulted — S1/S2 confirm a house requirement exists and can exceed the regulatory minimum, but neither states the actual current percentage(s) Robinhood applies, or under what conditions the concentration-based escalation (S6) is actually triggered in practice at this brokerage.

### 3. Intraday margin calls

**Known:** Robinhood's disclosure states the customer is "not entitled to an extension of time on a margin call," though an extension "may be available... under certain conditions" at Robinhood's discretion (S1, S4). Search-result summaries of Robinhood's own margin-call support article describe deposits made to resolve a call as "typically resolved intraday" but note this can take "up to 1 business day" (S4). This directly confirms margin calls are not purely a next-day, close-to-close event as `margin_simulation.py` models — real resolution windows can be shorter (same session) than the simulator's once-per-simulated-day settlement cycle.

**Known, by contrast (futures accounts, not this account's actual usage):** Robinhood's futures-specific margin-call process (S8) explicitly distinguishes a same-day "margin call" from a "past-due margin call" issued the next day if unmet, with the account moved to "position closing only" status in between. This is included for contrast only — this account does not trade futures, per `CLAUDE.md`, and this two-stage process is not confirmed to apply to standard equity margin accounts.

**Unresearchable:** The exact timing mechanics (e.g., a specific hour-of-day cutoff, or whether Robinhood's systems check margin requirements continuously intraday versus at fixed checkpoints) were not found in any source consulted.

### 4. Forced liquidation rules

**Known:** Robinhood's disclosure explicitly states it may liquidate "regardless of your intent to satisfy a margin call, in order to protect [its] interests," and does so "with or without your prior approval" (S1, S3). This directly confirms the *possibility* of forced liquidation with no cure-period guarantee — a real, sourced divergence from `margin_simulation.py`, which has **no forced-liquidation mechanic of any kind**: the simulator only ever repays debt when a specific policy (Model A/B/C) proactively chooses to, never as an automatic, broker-initiated response to a cap breach.

**Unknown:** Whether Robinhood, in practice, liquidates the *minimum* amount needed to cure a deficiency (closer to the simulator's own repayment-sizing logic, which computes a minimum-to-target amount in Model A/C) or a larger buffer amount, was not found in any source consulted.

### 5. Spread/slippage behavior during stress

**Not investigated by this pass** — already scoped as carried forward, unresolved, from `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md`/`RESULTS.md`, per `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §4 item 5's own framing ("carried forward here as still open, not re-litigated"). No new source was sought for this item in this pass; it remains **Unknown**, unchanged.

### 6. Borrowing-rate variability

**Known — and a material update to this project's own prior labeling.** Robinhood's margin rates are **tiered**, not flat: the first $1,000 of margin is interest-free (matching `CLAUDE.md`'s existing doctrine text), then approximately 5.75% APR on balances up to $50,000, 5.55% between $50,000–$100,000, and 5.25% between $100,000–$1,000,000, with rates continuing to step down at higher balances (S5, figures dated by the source as of December 2025). The same source states rates "might change at any time without notice."

This directly resolves part of what `docs/PHASE3C_ASSUMPTION_REGISTRY.md` #10 had labeled **Estimated** (the flat "~5% APR" figure) — the rate is confirmed real and tiered, not flat, and the ~5% figure used throughout every Phase 3–6A simulation falls within the lowest, most-applicable tier for this account's debt size (well under $50,000 throughout the entire 2021–2026 simulated window and this account's real current ~$1,600 balance). **This is evidence, not a correction applied to any prior result** — no prior simulation is rerun or amended by this finding; it is recorded here as a new, sourced fact for a future decision-relevance assessment (§6d of the research plan) to evaluate.

### 7. Portfolio margin differences

**Known:** Regulation T (12 CFR Part 220, S7) sets the standard 50% initial margin requirement that has applied since 1974 — this is the Reg T "standard margin" regime, which is what `margin_simulation.py`'s single leverage-cap model most closely resembles in spirit (a fixed ratio, not a risk-based calculation).

**Unknown:** Whether this account uses, or is eligible for, Robinhood's portfolio margin offering (a separate, risk-based methodology distinct from standard Reg T margin) was not established by any source consulted in this pass — no source found confirms Robinhood offers portfolio margin to retail accounts at this account's scale, nor whether this account is enrolled in it. `CLAUDE.md` describes this account's margin usage in terms consistent with standard margin (a flat leverage cap, a flat buffer percentage), which is suggestive but not confirmed.

## 3. Summary classification

| Item | Known | Estimated | Unknown | Permanently Unresearchable |
|---|---|---|---|---|
| 1. Liquidation sequencing | Robinhood has full discretion, customer has none (S1, S3) | — | — | The specific sequencing algorithm |
| 2. Maintenance margin differences | 25% FINRA floor; concentration escalation exists and can reach 50–100% (S6); house requirements exist and can exceed the floor (S1, S2) | — | Robinhood's actual house percentage(s); when concentration escalation triggers in practice | — |
| 3. Intraday margin calls | No guaranteed extension; deposits typically resolve intraday but can take up to 1 business day (S1, S4) | — | Exact timing mechanics / checkpoint frequency | — |
| 4. Forced liquidation rules | Can occur without notice or cure period, at Robinhood's discretion (S1, S3) | — | Minimum-cure vs. buffer-amount liquidation sizing | — |
| 5. Spread/slippage under stress | — | — | Not investigated this pass (carried forward from the stress-regime work) | — |
| 6. Borrowing-rate variability | Tiered rate structure confirmed, ~5.75% at this account's debt scale (S5) | (superseded — was Estimated pre-Phase-7A, now Known) | — | — |
| 7. Portfolio margin | Reg T standard-margin baseline confirmed (S7) | — | Whether this account uses/qualifies for portfolio margin | — |

---

## What this document deliberately does not do

- Does not modify `margin_simulation.py`, `allocate.py`, `targets.yaml`, `holdings.yaml`, or `margin_state.py`.
- Does not change `docs/PHASE5B_GOVERNANCE_DECISION.md`'s "maintain current doctrine" decision.
- Does not infer any broker behavior beyond what a cited source states — every Unknown/Unresearchable item above is left exactly that, not filled in with a plausible guess.
- Does not produce the broker-mechanics assumptions registry (§6b) or the decision-relevance assessment (§6d) required by `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` — those are separate, later deliverables, not attempted here.
- Does not recommend any doctrine change, repayment-policy change, or production behavior change.

Stopping here. Awaiting direction on the next Phase 7A deliverable.
