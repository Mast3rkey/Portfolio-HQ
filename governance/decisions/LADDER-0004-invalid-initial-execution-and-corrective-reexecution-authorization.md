---
decision_id: LADDER-0004
date: 2026-09-07
status: Accepted
category: research_integrity_correction
related_decisions: [GOV-0001, GOV-0002, OPS-0009, NUM-0001, LADDER-0001, LADDER-0002, LADDER-0003]
supporting_artifact: null
---

## Context

The first attempted LADDER V2 execution was retained on closed, unmerged
[PR #384](https://github.com/Mast3rkey/Portfolio-HQ/pull/384).
Its final reviewed head was
`c435243376b1ed761ac4c0f5e69281fcbbce4d45`; the implementation code was frozen at
`a304fdbcee8e7db0ff1507cee8bd341bc0ec2f9a`; and its result commit was
`636abcc3bec4ecc762029d9732cde40d66f15487`.  The attempt reported
`RETAIN_BASELINE`, but exact-head adversarial review found that the retained bundle
did not satisfy the required-output and validation provisions of
`PROTOCOL_V2.md`.  PR #384 was therefore closed without merge, and its result must
not be treated as the one valid registered run.

The material defects were:

1. no attributed equity, broad-fund, or gold segment results;
2. no cumulative-contribution, deployment-delay, unfilled-capital, concentration,
   target-deviation, or complete scoped clip/block metrics;
3. lifetime transaction, deployment, cost, and dividend totals repeated into each
   reporting window instead of window-scoped values;
4. no non-voting price-only TWR diagnostic;
5. a manifest commitment to `portfolio_paths.json` without the artifact itself;
6. validation that checked selected transform hashes but did not actively perform
   LADDER-0003's mandatory raw-page and receipt reconstruction; and
7. tests too weak to establish selector equivalence, event ordering, split and tax
   semantics, DFF lag, cash-flow-adjusted TWR, bootstrap and gate boundaries,
   output recomputation, exact reproducibility, or tamper refusal.

The invalid attempt is preserved by PR number, immutable commit identities, review
comment
[`5574233731`](https://github.com/Mast3rkey/Portfolio-HQ/pull/384#issuecomment-5574233731),
and these retained artifact hashes:

| Artifact at PR #384 head | SHA-256 |
|---|---|
| `execution/bootstrap.json` | `cce1eadc20b104623c761275e75427fa648193a77a4c9b0ce1f43fafb3c8baaf` |
| `execution/cycles.json` | `7ab8654cbf730473862f8efcd07876dfa93cc75f503d99162e496979de7b8b49` |
| `execution/disposition.json` | `b6ecceb15024dfa10bad4499bd43e1b41c52f5f85f7b98b16b13f9b649c7b127` |
| `execution/input_manifest.json` | `2d678a239786849fb29c878c9dcb03d9df9acdd5ba730dc07f10bc6a6506f224` |
| `execution/metrics.json` | `33bc1d7ecd3fee14ccf827aa04c0a5c72b0211f8c2d8199617e4addbe994fb8d` |
| `execution/sensitivities.json` | `5f11e9a000bc26bd5c43c276c82a491d4546ecbd2b1c00784eb9ac3fe1199238` |

`portfolio_paths.json` has no retained blob on that head.  Its manifest-only hash,
`ad1c154e654d2ddfccc1cf67c43de237e2b7c929e47c9b7931398f0a91347054`, is not
evidence that the artifact was preserved.

## Decision

Classify the PR #384 attempt and every metric, gate, narrative, and disposition it
emitted as **INVALID AND NON-DECISION-GRADE**.  It does not close LADDER V2 because
PROTOCOL_V2 §12 closes the study only after one *valid* registered run.  It does,
however, expose the voting holdout.  This decision supplies the separate reviewed
authority required by §12 for exactly one corrective execution under the controls
below.

The correction may change implementation, validation, tests, reports, and output
schema only as mechanically required to implement the already-frozen protocol.  It
may not change or reinterpret the roster, targets, arms, ladder levels, windows,
selected input bytes, anomaly corrections, corporate actions, friction cells, tax
assumptions, contribution amount, protected weight, minimum lot, adoption
inequalities, bootstrap method, resample count, or seed.  It may not acquire later
data.  No implementation choice may be selected because it improves or harms a
particular arm after the exposed result.

## Corrective lifecycle

One replacement implementation PR is authorized, with two irreversible phases:

1. **Result-free implementation phase.** Complete the engine, result validator,
   full synthetic/non-holdout test matrix, and a validation receipt that contains no
   holdout metric or disposition.  Validation must execute LADDER-0003's pinned
   builder in an isolated temporary reconstruction workspace and prove exact byte
   identity for every selected transform and retained action/cross-check artifact.
   Freeze the candidate code SHA and obtain successful exact-head CI plus an
   independent adversarial review before corrective execution.
2. **Single corrective execution phase.** Without changing reviewed code,
   configuration, or inputs, execute once and append the complete atomic output
   bundle, including daily paths.  An independent delta review must recompute
   manifests, selector identity, window and segment metrics, price-only diagnostics,
   bootstrap results, gates, sensitivities, and narrative before merge.  Any code or
   input change after execution makes the corrective attempt invalid; another
   execution would require a new decision.

The replacement must retain an explicit pointer to this decision and PR #384, and
must state that the holdout was previously exposed.  It may report
`RETAIN_BASELINE`, `INSUFFICIENT_EVIDENCE`, or a protocol-supported challenger only
from the corrected outputs.  The preliminary PR #384 ranking cannot confirm or veto
the corrected result.

## Boundaries

This decision changes no production target, gate, holding, issuer mapping, ladder,
allocator, margin policy, chart scope, account state, or accepted baseline.  It
authorizes no brokerage access, credential use, order, trade, current buy list, or
automatic adoption.  Stage 1 remains **UNARMED AND NOT EXECUTABLE**.
