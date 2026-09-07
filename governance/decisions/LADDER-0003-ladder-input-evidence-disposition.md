---
decision_id: LADDER-0003
date: 2026-09-07
status: Accepted
category: research_evidence_disposition
related_decisions: [GOV-0001, GOV-0002, OPS-0009, NUM-0001, RISK-0001, RISK-0002, RISK-0005, LADDER-0001, LADDER-0002]
supporting_artifact: research/buy_ladder_backtest/inputs/input_disposition.json
---

## Context

`LADDER-0002` halted validation and execution until one result-blind decision
selected exact price files, reconciled corporate actions, enforced identity and
availability boundaries, and disposed of the prior SOL coverage defect. That gate
was necessary because the completed whole-portfolio run used source selections that
conflicted with its inventory and did not establish action completeness.

The reconciliation was performed without implementing or inspecting a ladder arm.
The retained Alpaca action request used the price end date as the action endpoint,
although that endpoint filters on provider processing date. An entitlement with an
in-window ex-date and an August processing or payment date could therefore be absent
from a terminal response. The known July 2026 ASML and COST omissions reproduce this
coverage failure.

## Decision

Accept the input disposition and action ledger under these exact conditions:

1. Use the 25 retained Alpaca SIP, split-adjusted, non-total-return OHLC files pinned
   in `input_disposition.json`. Every series ends on 2026-07-31. CEG and GEV retain
   their actual later availability; no proxy or backfill is permitted. RTX rows may
   be admitted only from the 2021-06-01 study start, after its 2020-04-03 identity
   floor, and predecessor stitching remains prohibited. The builder must reconstruct
   every selected transform exactly from its raw terminal page and acquisition receipt.
2. Use `corporate_actions.json`, which contains 381 unique in-window ex-date events.
   It preserves later payment dates as receivables, adds the issuer-confirmed COST
   2026-07-23 and ASML 2026-07-28 dividends, resolves ETN's 2025-11 discrepancy to
   2025-11-06, and records the evidence basis for every dividend rate.
3. Exclude the retained event labeled ASML on 2024-12-02 with CUSIP G3730V147. FTAI
   issuer evidence and a filed security-ID mapping identify it as FTAI Aviation
   Series D preferred. The quarantined row remains preserved with its source ID.
4. Treat the Yahoo snapshot only as a result-blind date/type completeness
   cross-check. It cannot override issuer facts or supply a canonical dividend rate.
   The comparison found 22 identical symbol signatures and three exceptions, all
   explicitly dispositioned above.
5. Apply the separately pinned foreign-dividend amendment. It reconstructs gross
   entitlement when the retained provider rate is source-net, separates facts from
   assumptions, and models the foreign-tax credit without double-counting source
   withholding. A no-credit sensitivity is mandatory and can force
   `INSUFFICIENT_EVIDENCE`.
6. Select actions by ex-date entitlement within 2021-06-01 through 2026-07-31 from
   evidence known as of 2026-09-07. A provider process date after the price window
   does not exclude the event. Any later-discovered in-window event, unresolved
   action row, file drift, extra/missing ticker, or security-ID mismatch is fatal.
7. Verify the frozen acquisition inventory plus the complete 66-file raw and
   963-file receipt aggregates before selecting any input. Reconstruct the upstream
   820-row action transform from 28 terminal raw pages and receipts, then reconstruct
   all 25 selected price transforms from 25 terminal raw pages and receipts. Exact
   canonical byte identity with each retained transform is required. These checks
   must remain active under optimized Python.

SOL is outside the ladder roster. Its earlier robustness history remains
`EVIDENCE_LIMITED_NOT_DECISION_GRADE`; no pre-2021-06-17 SOLUSD history may be
inferred or stitched. A future whole-portfolio successor must acquire and separately
accept one exact lawful source or abstain, and must disclose that the old holdout is
already exposed.

## Exact pins

| Artifact | SHA-256 |
|---|---|
| `research/buy_ladder_backtest/PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md` | `c6e44d91aaa022f7159cd40f4df0c3cfc2b8fabfbed50044b83299f229647e81` |
| `research/buy_ladder_backtest/build_input_disposition.py` | `f3996075c763c3b81b8a9e56ac248540b3e6aa5c9f0b806855247f9851d9c746` |
| `research/buy_ladder_backtest/inputs/input_disposition.json` | `bf8280a4d99c1584b307c606bbe32a6cc53d7b224e307164acf04b5100443e21` |
| `research/buy_ladder_backtest/inputs/corporate_actions.json` | `4cd066e9ef72041941ab59a283bc5b2aa61351979f47356c27a9ec4c06c9b828` |
| `research/buy_ladder_backtest/inputs/yahoo_action_crosscheck.json` | `3a2a7b7604a43bd97a485065b0e59af11e8fd65c3c487a012c0c1ad0f6496544` |

The disposition also pins each of the 25 OHLC hashes, the retained upstream action
registry, the acquisition inventory, every selected raw page and receipt, and the
complete raw/receipt aggregates. Any byte change requires another reviewed decision.

## Authorized next unit

After merge and post-merge verification, one implementation PR may add the V2
engine, validation-only receipt, registered run, results, report, and focused tests.
The engine may verify these already-frozen paths and hashes but may not choose or
repin inputs. Validation must emit no holdout result before the one registered run.

## Boundaries

This decision changes no accepted target, gate, holding, production ladder,
allocator, margin parameter, chart authority, or account state. It does not rehabilitate
the old whole-portfolio result. It authorizes no brokerage access, credential use,
order, trade, live recommendation, or leverage. Stage 1 remains **UNARMED AND NOT
EXECUTABLE**.
