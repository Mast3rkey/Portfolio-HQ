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

This draft's exact nine paths are: `docs/CURRENT_NUMERIC_POLICY_EVIDENCE_INVENTORY_20260920.md`; `governance/decisions.yaml`; `governance/decisions/MARGIN-0006-current-architecture-s3-successor-proposal.md`; `margin_current_s3_preregistration_validator.py`; `research/current_architecture_readiness/EVIDENCE_AND_INPUT_REMEDIATION.md`; `research/current_architecture_readiness/validation/result_free_validation_receipt.json`; `research/margin_target_study/S3_CURRENT_ARCHITECTURE_PREREGISTRATION.yaml`; `test_margin_current_s3_preregistration.py`; and `test_portfolio_hq_dashboard_decisions.py`. It changes no accepted decision, frozen protocol, research input, production code/configuration, or result.

The checklist validator is intentionally non-authoritative. It checks only the scoping identity/status/role, the exact unresolved-decision labels, selected seal/fresh-period structure, undefined candidate/budget status, and the three execution prohibitions. It does **not** validate the truth, completeness, provenance, or admissibility of narrative exposure, coverage, source, policy, or economic claims; those remain review work.

## R1 integration prerequisite

A result-blind synthetic reproduction shows current research-engine pre-trade wiring can compute R1's trim-funded repay before a same-day deposit arrives. This is an isolated research integration gap, not a claim that production R1 is deployed or broken. Any successor must define separate cash-funded and trim-funded equations and add an integration regression proving deposit receipt precedes cash-funded R1 allocation without a spurious sell/rebuy. A genuine broker/maintenance cure still executes before an unavailable deposit.

## Result-blind accounting and source correction proposed for the successor

The supporting register now records the proposed cost-aware accounting contract, source-tagged event clock, three distinct deployment semantics, synthetic conservation oracle, partial source-derived candidate mapping, and the remaining choices. These additions remain `SPECIFICATION_INCOMPLETE_NOT_AUTHORIZED_NOT_EXECUTABLE`; they are proposed definitions for independent review, not implementation or acceptance.

The original margin-study cost cells are **0/5/15 bps**, from `research/margin_target_study/PROTOCOL_V2.md` §§7–8 and `pre_registration.yaml::metrics.cost_activity`. The prior scoping value 0/10/25 was a source-attribution error imported from the separate whole-portfolio V2 contract and is corrected without modifying either frozen source. Ten bps appears only in the synthetic arithmetic oracle and is not a MARGIN-0005 study cell.

R1 supplies `repay_amount` plus an `effective_leverage_cap`; it supplies neither a leverage target nor a no-borrow guarantee. The successor must keep separate: (a) a proposed cash-only/no-new-draw arm; (b) inherited deposit-day capacity followed by weighted-gap allocation, where capacity is not an actual draw and gaps/lots/gates may bind; and (c) a separately proposed genuine end-cycle target arm. Gross repayment, subsequent same-cycle borrowing, sale/buy costs and sell/rebuy must remain separately visible so a later draw cannot erase the measured repayment treatment.

The original 300-trial allowance remains attached to the original frozen experiment and is not inherited. A successor trial ceiling cannot be stated until full economic configuration tuples exist, nominal duplicates are collapsed by full configuration hash, and path-affecting 0/5/15 cost cases are either enumerated as trials or kept strictly fixed-path analytical post-processing.
