---
decision_id: MARGIN-0006
date: 2026-09-20
status: Proposed
category: research_scoping
related_decisions: [GOV-0001, GOV-0002, MARGIN-0004, MARGIN-0005, NUM-0001, RISK-0005, PHQ-2026-01, PHQ-2026-08]
supporting_artifact: research/margin_target_study/S3_CURRENT_ARCHITECTURE_PREREGISTRATION.yaml
---

# Current-architecture S3 successor scoping proposal

## Disposition

This is a **result-blind scoping proposal**, not an executable preregistration or charter amendment. The supporting artifact is deliberately `SPECIFICATION_INCOMPLETE`. MARGIN-0005's original 103.25% tier protocol, Track 2 seal beginning 2025-07-01, Track 3 seal beginning 2021-01-01, data, and trial history remain byte-preserved within their original scopes. The current architecture is a flat 99.25% destination; no tier-to-flat mapping is inferred.

No fresh period has been established. The exposure ledger classifies reused margin, whole-portfolio, ladder, and PHQ-matrix periods as exposed/correction evidence. Current-roster coverage remains unresolved, including newer issuers/assets; no asset may be silently dropped and no pre-inception history invented.

## What acceptance would mean

If independently accepted through the repository's normal decision process, acceptance would approve only the documented **scoping findings and missing-decision register**. Reviewer action alone does not change `status: Proposed`; activation requires the accepted decision to be committed and the generated `governance/decisions.yaml` entry updated in that acceptance change. Acceptance would authorize no runner, implementation, acquisition, historical trial, sealed access, candidate freeze, policy adoption, or production change.

A later decision must supply and independently accept a complete successor specification: supported dates and per-asset coverage; initial state; full decision rules and event clock; exact candidate-by-case registry; grounded costs, rates, maintenance proxies and stresses; accounting/tax rules; uncertainty/multiple-testing plan; budget derived from enumeration; hashes; and exact file scope. Only that later decision may authorize implementation. A still-later exact-head gate is required before development execution, and sealed evaluation requires separate authority.

## Approved file scope of this draft only

This draft may change only: this proposed decision; its scoping YAML; the current numeric inventory; the V2 remediation/source ledger; a non-authoritative scoping checklist validator and its tests; the result-free receipt; and the generated decision index. It changes no accepted decision, frozen protocol, research input, production code/configuration, or result.

## R1 integration prerequisite

A result-blind synthetic reproduction shows current research-engine pre-trade wiring can compute R1's trim-funded repay before a same-day deposit arrives. This is an isolated research integration gap, not a claim that production R1 is deployed or broken. Any successor must define separate cash-funded and trim-funded equations and add an integration regression proving deposit receipt precedes cash-funded R1 allocation without a spurious sell/rebuy. A genuine broker/maintenance cure still executes before an unavailable deposit.
