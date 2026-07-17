# Phase 7A: Data Availability Assessment

> **⚠️ Documentation only — no simulation, no code.** Assesses which execution-reality questions can actually be resolved with available information, using only findings already established in `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md`, `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md`, and `docs/PHASE7A_BROKER_MECHANICS_ASSUMPTION_REGISTRY.md`. Introduces no new broker-behavior claim, proposes no implementation, and does not modify any prior research conclusion.

_Written 2026-07-17, per `docs/PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §6c. This document answers a feasibility question — "could this be found out" — not a results question; it does not itself resolve any item, only classifies how resolvable each one is._

## Labels

- **Publicly available** — already found and cited in the evidence inventory or registry, or clearly obtainable via the same public sources without further effort.
- **Obtainable with effort** — the data exists and is not proprietary-internal, but was not retrieved this session (blocked by tooling, requires the account holder's own records, requires a paid data source, or requires directly contacting the broker).
- **Permanently unavailable** — proprietary internal broker logic; no public source addresses it and none is expected to.

---

## Broker mechanics

### 1. Liquidation sequencing

1. **Question:** Which positions Robinhood actually sells first, and in what order, when liquidating.
2. **Current evidence:** Robinhood retains full discretion; customer has none (`EVIDENCE_INVENTORY.md` §2 item 1, sources S1/S3). No source states the actual sequencing algorithm.
3. **Availability classification:** **Permanently unavailable.**
4. **Additional data required:** N/A — this is internal risk-system logic; no public disclosure obligation covers the specific algorithm.
5. **Resolving it could:** Remain permanently unresolved.

### 2. Maintenance margin requirements

1. **Question:** Robinhood's actual house maintenance percentage(s), and the specific conditions under which the FINRA-sourced concentration escalation (50–100% for positions >50% of equity) actually triggers at this brokerage.
2. **Current evidence:** The regulatory mechanism (FINRA Rule 4210, 25% floor + concentration escalation) is confirmed (`REGISTRY.md` item 2, source S6). Robinhood's own house requirements are confirmed to exist and can exceed the floor, but the specific numeric value(s) were not found — this session's tooling could not fetch the full PDF disclosure/agreement documents directly (403 responses on S1/S3).
3. **Availability classification:** **Obtainable with effort** — the mechanism is public; the specific numbers are disclosed to customers in documents this session's tooling failed to retrieve, not proprietary information withheld from the public entirely.
4. **Additional data required:** A successful full-text read of the Robinhood Margin Disclosure Statement and Customer Margin Account Agreement (S1, S3) — via a browser session, a different fetch method, or the account holder's own document access — plus, ideally, confirmation of whether/how the concentration escalation has actually applied to this account's own positions historically (a question the account holder, not public documentation, could answer).
5. **Resolving it could:** **Change interpretation** — this is the item flagged in `REGISTRY.md` as highest relevance to Phase 4A's concentration findings.

### 3. Intraday margin calls

1. **Question:** The exact timing mechanics of a margin call (checkpoint frequency, specific cutoff times, how "typically intraday, up to 1 business day" resolves in practice).
2. **Current evidence:** No guaranteed extension; deposits typically resolve intraday but can take up to one business day (`EVIDENCE_INVENTORY.md` §2 item 3, sources S1/S4).
3. **Availability classification:** **Obtainable with effort** — likely documented in more detail in the full disclosure/agreement PDFs (S1, S3) than the support-article summaries this session could retrieve, or answerable by directly contacting Robinhood support.
4. **Additional data required:** Same PDF-access gap as item 2, plus potentially a direct support inquiry, since exact checkpoint mechanics may not be published even in the full legal documents.
5. **Resolving it could:** Only reduce uncertainty — no evidence found suggests this timing difference would systematically favor or disfavor any tested outcome, only add granularity to a known gap.

### 4. Forced liquidation timing/rules

1. **Question:** Whether Robinhood liquidates the minimum needed to cure a deficiency or a larger buffer amount, and the actual timing rules governing when forced liquidation begins after a call is issued.
2. **Current evidence:** Confirmed to occur without notice or guaranteed cure period, at Robinhood's discretion (`EVIDENCE_INVENTORY.md` §2 item 4, sources S1/S3). The sizing rule (minimum-to-cure vs. buffer) was not found.
3. **Availability classification:** **Permanently unavailable** for the specific sizing algorithm (internal risk-system logic, same category as item 1); **Obtainable with effort** for any further general timing detail the full legal documents might contain beyond what the support articles state.
4. **Additional data required:** For the timing detail: the same PDF full-text read as items 2/3. For the sizing algorithm itself: none exists — this is not a data-collection gap, it is a proprietary-logic gap.
5. **Resolving it could:** **Change interpretation** for the general mechanism (already confirmed, per `REGISTRY.md` item 4) — but the specific sizing algorithm's own unresolvability means the *degree* of that interpretive change cannot be further refined by more research.

### 5. Portfolio margin eligibility/mechanics

1. **Question:** Whether this specific account uses, or is eligible for, Robinhood's portfolio margin offering rather than standard Reg T margin.
2. **Current evidence:** Reg T's standard 50% initial margin baseline is confirmed (`EVIDENCE_INVENTORY.md` §2 item 7, source S7). This account's actual enrollment status was not established by any public source.
3. **Availability classification:** **Obtainable with effort** — this is account-specific information the account holder has direct access to (via the Robinhood app's account settings or support), not proprietary broker-internal logic. It was simply never queried, because this research pass used only public sources per its own scope (`PHASE7A_EXECUTION_REALITY_RESEARCH_PLAN.md` §5).
4. **Additional data required:** A direct check of this account's own margin account type/settings, or a support inquiry — not a public-research task at all.
5. **Resolving it could:** Only reduce uncertainty — `CLAUDE.md`'s doctrine text is already consistent with standard margin, so a confirmation would narrow rather than overturn the current working assumption; a contrary finding (this account is on portfolio margin) would be a more significant change, but nothing in current evidence suggests that outcome is likely.

## Execution

### 6. Actual fill prices

1. **Question:** What price this account's real trades actually filled at, versus the simulator's assumed same-day close price.
2. **Current evidence:** None — this project has never had access to this account's real trade history (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`, reaffirmed unchanged by every subsequent phase including this one).
3. **Availability classification:** **Obtainable with effort** — this data exists (as the account holder's own trade confirmations/statements) but has never been supplied to this project, distinct from data that is inherently unobtainable.
4. **Additional data required:** The account holder's own historical trade confirmations or account statements, if ever supplied.
5. **Resolving it could:** Only reduce uncertainty for past trades already executed; it could not retroactively validate or invalidate any *simulated* scenario, since every Phase 3–6A scenario uses a synthetic $0-start account, never this account's real trade history.

### 7. Bid/ask spread behavior

1. **Question:** Real historical bid/ask spread width for the tickers this project simulates, especially during volatile periods.
2. **Current evidence:** None obtained in this pass — explicitly carried forward, unresolved, from `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md`, which used a real-OHLCV-derived volatility/liquidity *proxy*, never actual quoted spread data (`REGISTRY.md` item 8).
3. **Availability classification:** **Obtainable with effort** — historical NBBO/quote-level data exists commercially from market-data vendors, but is not part of this project's current data source (Alpaca's free daily-bar tier, which provides OHLCV only, no bid/ask).
4. **Additional data required:** A paid historical quote-data subscription or a different data provider than this project currently uses.
5. **Resolving it could:** Only reduce uncertainty — the already-tested cost-sensitivity passes found erosion immaterial at every tested magnitude; real spread data could narrow or widen that finding's confidence but is not expected, on current evidence, to reverse it.

### 8. Slippage during stress

1. **Question:** This account's own real slippage (difference between intended and executed price) during genuinely volatile periods.
2. **Current evidence:** None — same gap as item 6 (no real trade history) combined with item 7 (no real quote data).
3. **Availability classification:** **Obtainable with effort**, for the same reason as item 6 (this account's own trade records, if ever supplied) — bounded by the same limits as item 7 for any broader, non-account-specific slippage pattern.
4. **Additional data required:** Same as items 6 and 7, combined.
5. **Resolving it could:** Only reduce uncertainty, for the same reasons as items 6/7.

### 9. Order execution timing

1. **Question:** Real latency between placing an order and it filling, for this account's actual trades.
2. **Current evidence:** None specific to this account. General structural context already established: this tool is advisory-only with manual execution (`REGISTRY.md` item 7) — real timing already includes human decision latency beyond any broker-side execution speed.
3. **Availability classification:** **Obtainable with effort** for order-level timestamps (via this account's own trade confirmations, if supplied); **Permanently unavailable** for any sub-order routing/execution detail (e.g., payment-for-order-flow routing specifics), which is proprietary to the broker and market makers, not disclosed to retail customers at that level of granularity.
4. **Additional data required:** This account's own trade confirmation timestamps, for the obtainable portion only.
5. **Resolving it could:** Only reduce uncertainty — and only for the order-level timing question; the deeper routing-mechanics question remains permanently unresolved regardless of effort.

## Financing

### 10. Borrowing-rate history

1. **Question:** Whether/how Robinhood's margin interest rate changed across the 2021–2026 window every Phase 3–6A simulation uses, versus the flat 5% assumption applied throughout.
2. **Current evidence:** Only a current snapshot (as of December 2025, per source S5) — no historical rate series was sought or found in this pass.
3. **Availability classification:** **Obtainable with effort** — historical snapshots of Robinhood's public rate-disclosure pages likely exist via web archival services, and any past rate-change announcements would be publicly dateable, but neither was retrieved in this pass.
4. **Additional data required:** Archived historical versions of Robinhood's margin-rates disclosure page/announcements across the 2021–2026 window.
5. **Resolving it could:** Only reduce uncertainty — Phase 3G already tested an interest-rate sensitivity dimension on the existing flat-rate assumption; a real historical rate series would refine, not overturn, an already-partially-tested input.

### 11. Margin interest variability

1. **Question:** The current tiered rate structure's exact breakpoints and rates.
2. **Current evidence:** Already resolved this session — confirmed tiered (not flat), first $1,000 free, ~5.75% up to $50,000, stepping down at higher balances (`REGISTRY.md` item 5, source S5).
3. **Availability classification:** **Publicly available** — already obtained.
4. **Additional data required:** None for the current structure; see item 10 for the separate historical-variation question.
5. **Resolving it could:** Only reduce uncertainty — already resolved to the extent public information allows; this account's real debt scale places it entirely within the lowest, most-relevant tier.

---

## Findings That Are Resoluble

Items where additional (obtainable) effort could materially improve confidence, ranked by relevance flagged in `REGISTRY.md`:

- **Maintenance margin requirements (item 2)** — the highest-value target: a successful full-text read of Robinhood's actual disclosure/agreement documents, or a direct support inquiry, could resolve the specific house percentage(s) and concentration-escalation trigger conditions that this session's tooling could not retrieve.
- **Forced liquidation timing detail (item 4, partial)** — the general timing mechanics (not the proprietary sizing algorithm) may be further clarified by the same document access.
- **Portfolio margin eligibility (item 5)** — trivially resolvable by the account holder directly, not a research-effort question at all.
- **Actual fill prices, slippage, order timing (items 6/8/9, partial)** — resolvable only to the extent the account holder supplies real trade records; bounded by what those records actually contain.
- **Bid/ask spread data (item 7)** — resolvable with a paid data source this project does not currently use.
- **Borrowing-rate history (item 10)** — resolvable via web-archive research, not yet attempted.

## Findings That Are Structurally Unresolvable

Items where no amount of research can reproduce the broker's proprietary internal behavior:

- **Liquidation sequencing algorithm (item 1)** — internal risk-system logic, not published, no disclosure obligation covers it.
- **Forced liquidation sizing algorithm (item 4, the algorithm itself, distinct from general timing)** — same category as item 1.
- **Sub-order routing/execution mechanics (item 9, the routing-detail portion)** — proprietary to the broker and market makers, not disclosed to retail customers at that granularity by any regulatory requirement found.

## Decision Relevance

**No availability finding in this document changes `docs/PHASE5B_GOVERNANCE_DECISION.md`'s "maintain current doctrine" decision.** This document assesses *feasibility* — what could in principle be found out — not results; no new data was actually obtained beyond what `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md` already recorded. The two items flagged as capable of changing interpretation (maintenance margin requirements, forced liquidation rules) remain only **partially** resoluble even with further effort — their core proprietary mechanics (items 1 and 4's sizing/sequencing algorithms) are structurally unresolvable regardless of how much additional effort is applied, which means no realistic future research pass on this subject could fully close them. This bounds, but does not itself execute, any future research decision — whether to pursue the "obtainable with effort" items above is a separate, future choice, not authorized or recommended by this assessment.

---

## What this document deliberately does not do

- Does not introduce any broker-behavior claim beyond what `docs/PHASE7A_EXECUTION_REALITY_EVIDENCE_INVENTORY.md` and `docs/PHASE7A_BROKER_MECHANICS_ASSUMPTION_REGISTRY.md` already established.
- Does not propose implementation of any data-collection effort, document-retrieval attempt, or account-holder inquiry — it only classifies feasibility.
- Does not modify any prior research conclusion, including `docs/PHASE5B_GOVERNANCE_DECISION.md`'s decision or `docs/PHASE4A_RESEARCH_REPORT.md`'s "Evidence inconclusive" outcome.
- Does not change `margin_simulation.py` or any other code, and does not touch any production file.
- Does not recommend pursuing any specific "obtainable with effort" item over another.

Stopping here. Awaiting direction on the next Phase 7A deliverable (decision relevance synthesis, if not already sufficiently covered above).
