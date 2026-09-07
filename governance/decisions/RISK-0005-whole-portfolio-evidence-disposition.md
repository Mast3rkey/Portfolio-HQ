---
decision_id: RISK-0005
date: 2026-09-07
status: Accepted
category: research_evidence_disposition
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, RISK-0001, RISK-0002, RISK-0003, RISK-0004, LADDER-0001, LADDER-0002]
supporting_artifact: research/whole_portfolio_robustness/evidence_disposition.json
---

## Context

`PORTFOLIO-ROBUSTNESS-0001` retained one once-only execution and reported
`RETAIN_BASELINE`. A later independent completion audit reproduced four material
input problems that the execution gate did not surface:

1. 23 of 28 consumed datasets differ from the source inventory's selected hashes;
2. 17 of those stock/fund rows retain an unresolved corporate-action mismatch;
3. the SOL confirmation path omits 115 required sessions after its registered
   2021-01-01 inception; and
4. the engine admits pre-2020-04-03 RTX predecessor rows despite a registered
   identity boundary that prohibits predecessor stitching.

The audit also found an externally confirmed ASML dividend with Nasdaq ex-date
2026-07-28 that is absent from the retained action registry. ASML's investor page
records a EUR1.88 dividend, a 2026-08-05 payment date, and a 1.1371 EUR/USD fixing
for New York shares. This shows why hash integrity and the presence of payment dates
cannot establish external action completeness.

The 17 action flags compare action type and ex-date signatures across each
provider's full retained history. The flags do not by themselves establish an
equal-window amount discrepancy. The separately verified ASML omission is the
concrete action-completeness defect.

Transformation fidelity is not the disputed point. The audit reconstructed the
retained Alpaca transforms and action aggregation from their retained raw bytes.
The defect is that the run consumed a different source selection than its inventory,
did not adjudicate conflicting action sets, and substituted provider coverage for
registered inception and identity rules.

## Decision

Classify `PORTFOLIO-ROBUSTNESS-0001` as
`EVIDENCE_LIMITED_NOT_DECISION_GRADE`. Preserve every original protocol,
pre-registration, implementation, validation, execution, result, receipt, and lock
byte. `research/whole_portfolio_robustness/evidence_disposition.json` pins those
bytes and is the current status authority.

The original `RETAIN_BASELINE` text remains part of the historical execution. It
may not be cited as empirical validation or confirmation of the accepted targets.
The targets continue only under their separate accepted policy authority, and the
study adopted no alternative automatically.

The retained metrics are preserved computed outputs. Their reproducibility is
limited to the pinned code, consumed inputs, runtime, and execution evidence; it is
not external validation of those inputs. They do not establish substantive data
integrity, externally complete corporate actions, a complete SOL confirmation path,
or a lawful pre-boundary RTX history. Every portfolio alternative uses the affected
inputs, so no comparative adoption claim is exempted from this qualification. Under
the original protocol's rule for incomplete mandatory evidence, the current
evidentiary conclusion is `UNABLE_TO_DETERMINE`; this does not rewrite the retained
historical disposition.

The registered SOL date is a protocol-defined coverage start, not independently
proved asset inception. The early SOL and RTX defects do not mechanically invalidate
a later independently initialized window by themselves. Every window remains subject
to the shared source-selection and action-completeness qualification.

## Downstream disposition

Ladder validation and execution remain halted. An erratum does not clear
`LADDER-0002`'s input gate. A later, separately reviewed input disposition must,
before any ladder result is computed:

- freeze one exact split-adjusted, non-total-return OHLC path and SHA-256 per ticker;
- reproduce each chosen transform from retained raw bytes and acquisition receipts;
- reconcile split and gross-dividend facts over common lawful provider windows;
- add or explicitly quarantine confirmed missing actions with primary-source
  provenance, including ASML's 2026-07-28 event and its withholding/fee convention;
- enforce issuer-identity boundaries, including RTX on 2020-04-03; and
- distinguish asset inception from provider availability and fail closed on any
  missing post-inception coverage.

Any whole-portfolio recomputation requires a new study or correction identity. Its
already exposed historical holdout must be labeled a correction replication rather
than fresh untouched evidence. No RISK-0001 or PORTFOLIO-ROBUSTNESS-0001 lock may be
reset, no old result may be overwritten, and no affected window may be silently
shortened or dropped.

## Boundaries

This disposition changes no target, gate, holding, issuer mapping, production
allocator, ladder method, margin parameter, account state, or result byte. It
authorizes no brokerage access, credential use, order, trade, leverage, or current
buy list. Stage 1 remains **UNARMED AND NOT EXECUTABLE**.
