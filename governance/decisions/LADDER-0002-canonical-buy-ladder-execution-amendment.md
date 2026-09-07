---
decision_id: LADDER-0002
date: 2026-09-07
status: Accepted
category: research_charter
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, NUM-0001, LADDER-0001, PHQ-2026-02, PHQ-2026-07]
supporting_artifact: research/buy_ladder_backtest/PROTOCOL_V2.md
---

## Context

`LADDER-0001` correctly bounded the canonical-roster ladder question, but a
pre-execution review found four design gaps that would make a V1 result less useful
or non-identifiable:

1. arm-specific holdings could feed arm-specific target-gap rankings even though V1
   intended ticker selection to be identical;
2. the repository has no retained point-in-time historical earnings calendar, so the
   promised retrospective earnings gate cannot be reproduced without fabrication;
3. V1 did not reserve a held-out voting window or cost sensitivity; and
4. order activation, gap-through fills, and availability for newly listed names were
   not exact enough for byte-reproducible implementation.

No V1 simulation was run and no result was inspected. The whole-portfolio robustness
program has since retained the exact current-roster price inputs through 2026-07-31,
making a corrected pre-registration possible without acquiring evidence after a
ladder result is known.

## Decision

Adopt `research/buy_ladder_backtest/PROTOCOL_V2.md` as the sole execution protocol
for the one study authorized by LADDER-0001. V1 remains retained but is superseded
for execution.

V2 preserves the original roster, three arms, fixed arm parameters, $2,000 monthly
contribution, 1 pp return threshold, 1 pp drawdown tolerance, segment reporting,
crypto exclusion, and prohibition on automatic policy changes. It makes the study
identifiable and decision-useful by:

- selecting tickers and dollars once through a shared shadow allocator, copied
  exactly to all arms;
- honestly omitting the unavailable historical earnings blackout from every arm,
  while leaving the current production gate untouched;
- freezing 2021-06-01–2023-12-29 as non-voting context and
  2024-04-02–2026-07-31 as the voting holdout;
- adding 0/10/25 bp cost cells, lagged after-tax cash yield, and a paired deterministic
  block-bootstrap confirmation gate; and
- specifying next-session activation, gap-through fills, cycle expiry, 210-session
  availability, deterministic tie-breaking, event order, metric annualization, seed
  20260907, manifests, atomic outputs, and independent reproduction.

## Exact pin

`research/buy_ladder_backtest/PROTOCOL_V2.md`

SHA-256: `717d3436e608440885174fb94a260aa022d3550d6160e5d44ad3dcabb4d1c238`

The protocol was finalized and hashed before this decision record was written. Any
byte change requires another reviewed amendment. No registered execution may begin
until this decision merges and the committed blob matches the pin.

## Authorized next unit

After merge and post-merge verification, one implementation PR may add deterministic
code, configuration, manifests, validation receipts, results, report, and focused
tests only within `research/buy_ladder_backtest/`, plus one root-level focused test if
the repository test layout requires it. Reuse of the already-retained input files is
read-only.

The implementation must first pass a validation-only run that emits no holdout
result. It may then execute one registered run and retain the complete evidence. The
candidate SHA must pass exact-head CI and independent adversarial review before merge.

## Boundaries

This decision changes no target, gate, holding, issuer mapping, production ladder,
allocator, margin parameter, chart authority, or account state. It authorizes no
brokerage access, credential use, order, trade, live recommendation, or current buy
list. Any later adoption requires a separate decision. Stage 1 remains **UNARMED AND
NOT EXECUTABLE**.
