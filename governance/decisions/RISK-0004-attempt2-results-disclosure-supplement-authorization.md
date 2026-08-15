---
decision_id: RISK-0004
date: 2026-08-14
status: Proposed
category: research_charter_amendment
related_decisions: [GOV-0001, GOV-0002, GOV-0003, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, LEVEL2-0001, RISK-0001, RISK-0002, RISK-0003]
supporting_artifact: null
file: governance/decisions/RISK-0004-attempt2-results-disclosure-supplement-authorization.md
---

## Context

### Live preflight, parking, sole lane, and identifier

This Lane-G filing began from live-verified repository and GitHub state. GitHub `main`, local
`main`, `origin/main`, and the filing base all resolved to
`b8b7bb715c5ef5e53ed05bfcdedf9750f3e715bf`. PR #316 was open, draft, unmerged, and mergeable at
the exact independently reviewed RESULTS head
`ffbe4d5bebf8fa9c5354c230f41c2bf7f82f065a`. Independent full exact-head RESULTS review
`4941983592` was retained at that head with disposition `CHANGES REQUIRED`: zero BLOCKING, two
MAJOR, zero MINOR, and one NOTE. No result-head drift had occurred.

PR #316 was then closed only for temporary governance parking. Its body durably records that this
is not abandonment, result acceptance, policy adoption, or execution authority, and that the same
PR #316 must be reopened only after this decision receives independent full exact-head review,
principal exact-head acceptance, merge, and immediate post-merge verification. Its remote branch
`codex/risk-0001-attempt2-integrity-correction` remains preserved at exactly
`ffbe4d5bebf8fa9c5354c230f41c2bf7f82f065a`; the branch and result artifacts were not edited,
deleted, rebased, or otherwise changed. The open-PR inventory then became empty, leaving this
governance branch as the sole active mutation lane.

The decision directory, `governance/decisions.yaml`, remote branch names, and live PR inventory
contained no prior `RISK-0004` decision, catalog entry, or RISK-0004 mutation branch/PR. The only
live PR text occurrence was the new temporary-parking notice on PR #316 itself. `RISK-0004` is
therefore the exact unused identifier for this amendment. The primary checkout's pre-existing
untracked `.worktrees/` and `AGENTS.md` paths remain preserved and excluded.

### Controlling authority

The Investment Constitution and `GOV-0002` preserve the authority hierarchy and prevent generated
reports, tests, or implementation code from originating policy. `GOV-0003` leaves all margin hard
limits and separate-research requirements unchanged. `OPS-0009` classifies this as Lane G and
requires full exact-head independent review, retained attribution, principal exact-head acceptance,
merge, and immediate post-merge verification. `OPS-0014` requires one mutation lane and prohibits a
direct-main mutation. `NUM-0001` distinguishes computational conformance from economic validity and
prohibits false precision. `XASSET-0019` keeps replacement Level-1 methodology, final Level-2
membership/sizing, whole-portfolio reconciliation, policy adoption, and margin/debt work downstream
and separately governed.

`RISK-0001`, Protocol V1, and the canonical preregistration require complete result and limitations
disclosure, preserve missingness and representation conflict, and prohibit rerun after results are
observed without separately accepted authority. `RISK-0002` authorized and then consumed exactly one
integrity-corrected attempt 2; it grants no retry, continuation, regeneration, or third attempt.
`RISK-0003` authorized only the completed-state test-harness correction and publication mechanics on
the existing PR #316 while freezing the completed economic/result artifacts. Review `4941983592`
independently confirmed that correction, the execution, the accounting, the canonical reductions,
the frozen bytes, and exact-head CI, but found two mandatory disclosure deficiencies. This decision
is the smallest additional authority for those reporting deficiencies. It does not reopen
`RISK-0001`, `RISK-0002`, `RISK-0003`, Protocol V1, or the preregistration.

### Executed-study boundary

The completed study remains frozen at this exact boundary:

| Field | Frozen fact |
|---|---|
| Attempt | `RISK-0001-EXECUTION-ATTEMPT-002` |
| Historical preexecution head | `ffb314bb56dc8eacd946cd6cbaf650e710130710` |
| Independent preexecution PASS review | `4940565638` |
| Published RESULTS head | `ffbe4d5bebf8fa9c5354c230f41c2bf7f82f065a` |
| Independent full RESULTS review | `4941983592` |
| First registered eligible-cell commencement | `2026-08-14T19:42:17Z` |
| Completion | `2026-08-14T19:44:02Z` |
| Execution status | `COMPLETED_RESULTS_OBSERVED_NO_RERUN_PERMITTED` |
| Registered cells | `777` |
| Executed cells | `609` |
| Governed null/ineligible cells | `168` |
| Reserve cells | `0` |
| Duplicate / missing / extra cells | `0 / 0 / 0` |
| Canonical result validator | `PASS` |
| Attempt-2 authorization | `CONSUMED` |
| Retry / third attempt | `NOT_AUTHORIZED` |
| Policy effect | `NONE` |

The family dispositions are frozen as:

| Family | Disposition |
|---|---|
| `EQUITY` | `unable_to_determine` |
| `FUND_BROAD_MARKET` | `unable_to_determine` |
| `FUND_GLD_DEFENSIVE` | `unable_to_determine` |
| `CRYPTO` | `unable_to_determine` |

### Independent RESULTS review findings

Review `4941983592` found no machine or economic artifact defect. It independently reconciled the
execution, reproduced all four dispositions, confirmed the canonical result validator PASS, matched
every RISK-0003-frozen byte, confirmed focused tests and exact-head CI, and retained the consumed/no-
third-attempt/no-policy boundary. Its two MAJOR findings are reporting and limitations deficiencies:

1. **MAJOR 1 — `RESULTS.md` mandatory disclosure incompleteness.** The frozen report omits 133
   censored recovery observations, the selection-conditioned-cohort warning, affected missing and
   pre-inception representations, corporate-action truncations, and substantive family-result
   traces. The frozen evidence includes SOL with 3 `MISSING_SOURCE_DATA` cells and 9 pre-inception
   cells; known-gap cells for VWO, ETN, GNRC, and WM; 6 `CORPORATE_ACTION_UNRESOLVED` cells for
   SPGI; path-risk/recovery versus opportunity-cost conflict for EQUITY and FUND_GLD_DEFENSIVE;
   FUND_BROAD_MARKET unavailability through VWO; and CRYPTO effects from SOL unavailability and
   representation disagreement.
2. **MAJOR 2 — `LIMITATIONS_AND_SURVIVORSHIP.md` fallback and limitations incompleteness.** Yahoo
   fallback was actually bound to 630 registered cells and Coinbase fallback to 21 registered
   cells, so wording that fallbacks apply “if used” understates actual reliance. The frozen report
   also insufficiently discloses SOL-specific history/missingness; gold-peer outcomes (IAU admitted,
   SGOL failed zero-gap admission, and GLDM correlation `0.9943199989` fell below the `0.995` gate);
   and representation/path sensitivity contributing to family nulls.

The exact defect classification is
`RESULTS_REPORTING_DISCLOSURE_SUPPLEMENT_ONLY`.

## Decision

### 1. Findings and defect boundary

This decision explicitly finds:

1. the attempt-2 execution itself reconciled;
2. canonical result validation passed;
3. the four `unable_to_determine` dispositions were independently reproduced;
4. no machine or economic artifact defect was found;
5. the two MAJOR findings concern mandatory reporting and limitations disclosure only;
6. no rerun or result recomputation is authorized or necessary; and
7. every frozen result artifact remains historical byte-identical evidence.

The findings do not convert a reporting omission into an execution failure. They also do not permit
the missing disclosures to be supplied by rewriting the frozen historical reports.

### 2. Exact authority granted

Only after this decision receives independent full exact-head review, principal exact-head
acceptance, merge, and immediate post-merge verification, it authorizes exactly **one** later bounded,
byte-preserving reporting/disclosure supplementation on the same existing PR #316.

That later correction may:

1. create one or more **new** reporting/disclosure supplement or addendum files addressing review
   `4941983592`;
2. update PR #316's body factually to reference the supplements and the continuing lifecycle
   boundary;
3. update factual `operations/WORKSTREAMS.yaml` lifecycle state if required;
4. add directly necessary tests or validators only if required to mechanically verify the new
   supplement against already-frozen machine artifacts, and only with an explicit written
   justification tied to this authority; and
5. publish the supplement on the same existing results PR.

Additive supplements are required over modification of historical result reports. Every supplement
must identify itself conspicuously as post-review reporting/disclosure, name review `4941983592`,
and state that it is additive explanation of already-frozen evidence rather than a regenerated or
recomputed result.

If additive reporting cannot close both MAJOR findings without crossing any prohibition in this
decision, work must stop for new authority.

### 3. Frozen historical artifacts and byte-equality gate

The following eight artifacts are frozen at these exact SHA-256 identities:

| Artifact | SHA-256 |
|---|---|
| Attempt-2 approval receipt | `ec9dd6aeb4b8f5751ea8679c700723203b20777e89623b52882508a0a144b2cd` |
| Completed execution receipt | `9d72f2b461e7834d24b3cadac0ebd5572e10c89519ae863b4ec7cc241158ac24` |
| `raw_evidence.json` | `eae2f5e54950efbe5fe97016d688b09529507c915658fed020e94568171c1cbc` |
| `cell_results.json` | `c5f6d8b0f24dee69ca0c398a42071ddbec04eddb0baeef014f6fb89932111b61` |
| `disposition.json` | `364a324c6dad68d84ee5126600e2caef6ac6d3253c739e6ed55773325107e5d5` |
| `diagnostics.json` | `f1c5d08fdebb368472c5e07a4c485d3c8356ed3c7116737dc6ba348d17ce5b04` |
| `RESULTS.md` | `2a6b814e8df578bbc30c4bf2c40e05815df48cf0d1c2308630b7f7042ff207bc` |
| `LIMITATIONS_AND_SURVIVORSHIP.md` | `28eb4796d371ffb527845b8539b5cbb14493a191452b2f37bca4956a21971deb` |

The future implementation must prove before/after equality for every hash above at each material
boundary: before merging updated `main` into the result branch, after that merge, after supplement
creation, before commit, and at the final pushed exact head. Any mismatch stops publication and
grants no repair, rewrite, regeneration, or recomputation authority.

The original `RESULTS.md` and `LIMITATIONS_AND_SURVIVORSHIP.md` must not be rewritten merely to make
review pass. They remain frozen historical evidence beside the new supplement.

### 4. Authorized supplement content and semantics

The future supplement may factually summarize already-existing governed machine evidence necessary
to close the two findings, including:

- exact `777 / 609 / 168` accounting and zero reserve/duplicate/missing/extra accounting;
- null/ineligible categories and the exact 133 censored recovery observations;
- named missing, pre-inception, known-gap, and corporate-action-affected representations;
- actual Yahoo/Coinbase provider/fallback usage;
- gold-peer admission outcomes;
- representation/path sensitivity and the selection-conditioned/survivorship warning;
- a factual trace of each family disposition from frozen result/reduction evidence; and
- the explicit no-rerun, consumed-attempt, no-third-attempt, and no-policy boundaries.

The supplement is disclosure, not a new result. It may not recompute a disposition, reinterpret
evidence to create a different result, add a metric or trial, change a threshold/scenario/window,
change provider/data, manufacture missing evidence, create a numeric allocation recommendation, or
strengthen `unable_to_determine` into a policy conclusion.

### 5. Required family-trace boundary

The supplement may explain only the following factual traces from the frozen artifacts:

- **EQUITY:** mixed direction between path-risk/recovery and opportunity-cost evidence leads to
  `unable_to_determine`.
- **FUND_BROAD_MARKET:** mandatory representation consistency is affected by VWO unavailability,
  with conflicting or unavailable directional evidence, leading to `unable_to_determine`.
- **FUND_GLD_DEFENSIVE:** GLD/IAU evidence includes opposing path-risk/recovery and opportunity-cost
  directions; SGOL/GLDM admission limits remain disclosed; the result is `unable_to_determine`.
- **CRYPTO:** SOL historical unavailability plus BTC/ETH representation disagreement where present
  leads to `unable_to_determine`.

These are explanatory traces only. They are not recommendations, target implications, or authority
to choose among the adjacent scenarios.

### 6. Absolute prohibited scope

This decision authorizes no execution, continuation, restart, retry, third attempt, cell
recomputation, result regeneration, raw-evidence mutation, cell-result mutation, disposition
mutation, diagnostics mutation, historical `RESULTS.md` mutation, historical
`LIMITATIONS_AND_SURVIVORSHIP.md` mutation, approval/execution-receipt mutation, Stage-A or
preexecution-metadata mutation, protocol/preregistration/configuration/eligibility/registry change,
provider/fallback change, reacquisition, methodology/metric/scenario/window/threshold change,
production runner/core/acquisition/evaluator/reducer/result-validator change, family-disposition
change, Level-1 or Level-2 sizing, membership/holdings/targets change, cash/liquidity policy,
debt/margin/leverage policy, charts/ladders, policy adoption, or brokerage/order authority.

No test or supplement validator may become authority to alter frozen evidence or production result
logic. No disclosure finding, validation failure, or review outcome creates additional execution or
correction capacity.

### 7. Publication path after effectiveness

Only after this decision becomes effective, the future author must proceed in this order:

1. reopen the same PR #316;
2. reactivate its existing result branch as the sole mutation lane;
3. fetch updated `main` and merge it into that branch without rebasing;
4. verify all eight frozen artifact hashes before and after the main merge;
5. add only the authorized new reporting supplement/addendum file or files and any explicitly
   justified mechanical supplement validator/tests;
6. verify all eight frozen artifacts remain byte-identical;
7. run applicable focused disclosure validation;
8. run the canonical result validator unchanged;
9. run full `pytest` once on the final candidate;
10. run repository validators/parsers, `git diff --check`, and protected-path/no-recomputation scans;
11. commit and push to the same PR #316;
12. obtain exact-head CI and stop;
13. start a new independent **full** exact-head RESULTS review, not a delta review unless controlling
    doctrine explicitly permits one;
14. obtain principal exact-head RESULTS acceptance only after a clean review;
15. merge PR #316 only through the normal lifecycle and immediately post-merge verify it; and
16. only then may a separately authorized replacement Level-1 methodology begin.

The new supplement is substantive result-reporting evidence, so full results review is the default.
This authoring session may not perform that review, accept results, mark PR #316 ready, or merge it.

### 8. Governance package and effectiveness

This governance-only filing touches exactly:

1. this decision;
2. `governance/decisions.yaml`;
3. `operations/WORKSTREAMS.yaml`; and
4. the two mechanical decision-count assertions in
   `test_portfolio_hq_dashboard_decisions.py`.

It contains no result-supplement implementation, RISK implementation/test artifact, receipt,
execution artifact, result artifact, protocol, preregistration, registry, data, economic
reinterpretation, or portfolio-policy change.

This decision remains proposed and ineffective until its own independent full exact-head review,
principal exact-head acceptance, merge, and immediate post-merge verification complete. Filing,
CI, or review alone does not make the supplement authority effective. The author stops after the
draft governance PR is open and exact-head CI succeeds. The author does not self-review, mark ready,
merge, reopen PR #316, reactivate its branch, author the supplement, or execute/recompute any RISK
cell.

## Rationale

Attempt 2 completed once and produced a canonically validated, independently reproduced result
record. The review found omissions in how that frozen record was disclosed, not a defect in the
machine evidence or reductions. Rewriting the frozen reports would erase their historical identity;
rerunning would violate the consumed-attempt boundary. A separately governed, additive, hash-
guarded supplement is therefore the smallest remedy that can satisfy Protocol V1's disclosure
requirements while preserving the study exactly as executed.

## Alternatives Considered

**Rewrite the frozen reports.** Rejected. The original report bytes are historical evidence and
must remain independently verifiable at their retained hashes.

**Rerun or recompute the study.** Rejected. No machine/economic defect exists, attempt-2 authority is
consumed, results were observed, and no third attempt is authorized.

**Treat the omissions as immaterial and accept the results.** Rejected. Protocol V1 makes the
missingness, censoring, selection-conditioning, corporate-action, fallback, and representation
disclosures mandatory, and independent review correctly withheld acceptance.

**Create a replacement results PR.** Rejected. Historical preexecution ancestry and the completed
results lifecycle remain bound to the same PR #316 and its preserved branch.

**Allow a delta review by default.** Rejected. The supplement is new substantive result-reporting
evidence. `OPS-0009`'s conservative escalation requires a new full exact-head RESULTS review unless
controlling review doctrine expressly establishes that all delta-review conditions hold.

## Consequences

If this decision completes its lifecycle, exactly one additive reporting-supplement correction may
be made on the same PR #316 while all eight frozen artifacts remain byte-identical. The supplement
may close only review `4941983592`'s two MAJOR disclosure findings. Attempt 2 remains completed and
consumed, no retry or third attempt exists, all four family dispositions remain
`unable_to_determine`, and no policy effect is created.

If additive disclosure is insufficient, or any frozen hash changes, work stops for new authority.
