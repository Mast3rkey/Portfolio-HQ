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
   The retained SPY row for 2026-02-02 contains an impossible decimal-place low of
   69.005, and the retained NVDA split-date row for 2024-06-10 contains a malformed
   195.95 high. Apply the exact, separately pinned 689.42 and 123.10 corrections
   only after raw-byte reconstruction and before any ladder calculation. Two
   independent retained Yahoo Finance and Nasdaq charting responses corroborate
   each corrected OHLC tuple. The builder must authenticate their exact request,
   status, transport-byte hash and size, retained-file hash and size, symbol, date,
   provider independence, and reconstructed two-decimal OHLC agreement. The one
   repository LF terminator is excluded before the exact transport hash is checked.
   All other unexplained or implausible OHLC rows are fatal.
2. Use `corporate_actions.json`, which contains 381 unique in-window ex-date events.
   It preserves later payment dates as receivables, adds COST on 2026-07-24 using
   the issuer's exact amount/record date plus Nasdaq's T+1 regular-distribution
   ex-date rule, adds the issuer-confirmed ASML 2026-07-28 dividend, resolves ETN's
   2025-11 discrepancy to 2025-11-06, and records the evidence basis for every rate.
3. Exclude the retained event labeled ASML on 2024-12-02 with CUSIP G3730V147. FTAI
   issuer evidence and a filed security-ID mapping identify it as FTAI Aviation
   Series D preferred. The quarantined row remains preserved with its source ID.
4. Treat the Yahoo snapshot only as a result-blind date/type completeness
   cross-check. It cannot override issuer facts or supply a canonical dividend rate.
   Reconstruct the snapshot byte-for-byte from the 25 retained Yahoo responses and
   their pinned receipt manifest; any response, request, roster, count, or transform
   drift is fatal. The comparison found 22 identical symbol signatures and three
   exceptions, all explicitly dispositioned above.
5. Apply the separately pinned foreign-dividend amendment. It reconstructs gross
   entitlement when the retained provider rate is source-net, separates facts from
   assumptions, and models the foreign-tax credit without double-counting source
   withholding. ETN provider gross/net quote changes remain provenance only: the
   baseline consistently assumes the documented U.S.-broker Irish-DWT exemption,
   while a mandatory 25% no-exemption sensitivity applies to the full ETN window.
   The no-credit and ETN no-exemption sensitivities can force
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
   must remain active under optimized Python. The foreign-dividend amendment and
   price-anomaly evidence hashes are also builder preconditions; the builder may
   not bless their current bytes dynamically.

SOL is outside the ladder roster. Its earlier robustness history remains
`EVIDENCE_LIMITED_NOT_DECISION_GRADE`; no pre-2021-06-17 SOLUSD history may be
inferred or stitched. A future whole-portfolio successor must acquire and separately
accept one exact lawful source or abstain, and must disclose that the old holdout is
already exposed.

## Exact pins

| Artifact | SHA-256 |
|---|---|
| `research/buy_ladder_backtest/PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md` | `6f9e335caa5f0733c57932637cca1563a9daeb94a4dcdb81fe51587920f7c60f` |
| `research/buy_ladder_backtest/inputs/price_anomaly_overrides.json` | `9f0a9513b769e036f4d1b209f5d63b6b32893fdc375a319252b5b89dc953c13f` |
| `research/buy_ladder_backtest/inputs/price_correction_receipts.json` | `d770e0d8ea07ae345bde8d4499b2c4db72dc1f531892b1a1c5c60ea027df6004` |
| Price-correction retained-response aggregate (4 files) | `3684b81c6bc0ada674bc180afd5cd12e6a776d311c4b8d94e3672c637d3b5794` |
| `research/buy_ladder_backtest/build_input_disposition.py` | `01a664c1c5bc623b5026cb3137a6694f0a55c3ee730eaad39dc7b82f7508bd7f` |
| `research/buy_ladder_backtest/inputs/input_disposition.json` | `05a86b0f42df6b055532076d2e84e7ac7a460799012402904afe1fcb1e72ab2e` |
| `research/buy_ladder_backtest/inputs/corporate_actions.json` | `79be46b9e64191d4897c5b9ada2c7ba7cfb8c4f86eca4e9ec6943c5895a6d2f1` |
| `research/buy_ladder_backtest/inputs/yahoo_action_crosscheck.json` | `0c154aa9e88d495f23b4d08e82e079b8054524bed5e3921cbaf1bf56f199deb4` |
| `research/buy_ladder_backtest/inputs/yahoo_raw_receipts.json` | `d69c0841fec6416a751a4ff02bac56900ade81f2278d548a5c3b0724f02bfabf` |
| Yahoo raw response aggregate (25 files) | `7f046a416b28b1fbf3392fe5ab449e0ae850f0937690429c7d3cab8d72a6ca78` |

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
