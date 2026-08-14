---
decision_id: RISK-0003
date: 2026-08-14
status: Proposed
category: research_charter_amendment
related_decisions: [GOV-0001, GOV-0002, GOV-0003, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, LEVEL2-0001, RISK-0001, RISK-0002]
supporting_artifact: null
file: governance/decisions/RISK-0003-postexecution-test-harness-lifecycle-correction-authorization.md
---

## Context

### Live preflight, sole lane, and identifier

This Lane-G filing began from live-verified repository and GitHub state. GitHub `main`, local
`main`, `origin/main`, and the filing base all resolved to
`e4d9fd69467755b7aa974c39dcb107e388910c52`, the merge commit of RISK-0002 PR #315. PR #316 was
the sole open pull request, remained draft and unmerged, and still resolved to the independently
approved preexecution head `ffb314bb56dc8eacd946cd6cbaf650e710130710`. No postexecution commit
had been pushed to it.

PR #316 was therefore closed only for temporary lifecycle parking, with an explicit retained note
that the same PR must be reopened after this decision is independently reviewed, principal-accepted,
merged, and post-merge verified. Its remote branch
`codex/risk-0001-attempt2-integrity-correction` remains intact at exactly
`ffb314bb56dc8eacd946cd6cbaf650e710130710`; the branch was not modified or deleted. The open-PR
inventory then became empty, leaving this governance branch as the sole active mutation lane.

The former attempt-2 author worktree `/private/tmp/Portfolio-HQ` is an inactive evidence store. The
original failed forensic lane `/private/tmp/phq-risk0001-results` remains forbidden. Neither location
was entered, inspected, listed for economic content, edited, cleaned, reset, stashed, rebased,
committed, pushed, deleted, or repurposed during this filing. The primary checkout's pre-existing
untracked `.worktrees/` and `AGENTS.md` paths are preserved and excluded.

The full tracked-repository collision scan, decision directory, and decision catalog contained no
`RISK-0003`. `RISK-0001` and `RISK-0002` are the only existing RISK decisions. `RISK-0003` is
therefore the exact available identifier for this amendment.

### Controlling authority

The Investment Constitution and `GOV-0002` preserve the authority hierarchy and prohibit a test or
implementation surface from originating policy. `GOV-0003` leaves all margin hard limits and
separate-research requirements unchanged. `OPS-0009` classifies this as full Lane G: exact-head
independent review, retained attribution, principal exact-head acceptance, merge, and immediate
post-merge verification are mandatory. `OPS-0014` requires the sole mutation lane and prohibits any
direct-main mutation. `NUM-0001` distinguishes computational conformance from economic validity.
`XASSET-0019` keeps replacement Level-1 methodology, Level-2 membership/sizing, portfolio
reconciliation, policy adoption, and margin/debt work downstream and separately governed.

`RISK-0001` §14 and Protocol V1 §20 prohibit a rerun after results are observed merely because a
defect is found. The RISK preregistration likewise sets `after_results_observed: PROHIBITED`, gives
zero reserve capacity, and requires separately accepted RISK authority for a governed correction.
`RISK-0002` §10 consumed its only attempt-2 authority when the first registered attempt-2 cell began;
§13 expressly grants no further execution and requires new separately accepted RISK authority for
any later defect. This decision is that new authority, but it authorizes no execution, continuation,
restart, retry, recomputation, result regeneration, or third attempt.

### Executed-study boundary

The executed study is frozen at this exact boundary:

| Field | Frozen fact |
|---|---|
| Attempt | `RISK-0001-EXECUTION-ATTEMPT-002` |
| Preexecution approved head | `ffb314bb56dc8eacd946cd6cbaf650e710130710` |
| Independent preexecution review | `4940565638` |
| First eligible-cell commencement | `2026-08-14T19:42:17Z` |
| Completion | `2026-08-14T19:44:02Z` |
| Status | `COMPLETED_RESULTS_OBSERVED_NO_RERUN_PERMITTED` |
| Registered cells | `777` |
| Executed cells | `609` |
| Preexecution-ineligible/null cells | `168` |
| Reserve cells | `0` |
| Duplicate / missing / extra cells | `0 / 0 / 0` |
| Attempt-2 authorization | `CONSUMED` |
| Third attempt | `NOT_AUTHORIZED` |
| Policy adoption | `NONE` |

The canonical result validator reconciled all registered identities and reductions. The completed
family dispositions are exactly:

| Family | Disposition |
|---|---|
| `EQUITY` | `unable_to_determine` |
| `FUND_BROAD_MARKET` | `unable_to_determine` |
| `FUND_GLD_DEFENSIVE` | `unable_to_determine` |
| `CRYPTO` | `unable_to_determine` |

The registered execution completed. Canonical result validation passed. Publication then stopped
because mandatory postexecution full `pytest` reported **58 failed / 6663 passed**. All 58 failures
were lifecycle-incompatible assertions in `test_risk_level1_implementation.py` that continued to
require the lawfully created attempt-2 approval receipt, consumed/completed marker-execution receipt,
and canonical results namespace to be absent. No economic computation, canonical reduction, result
validator, family-disposition, registered-cell-accounting, or data-integrity failure was identified.

The defect classification is exactly
`POSTEXECUTION_TEST_HARNESS_LIFECYCLE_CORRECTION_ONLY`. It concerns validation and publication
mechanics after a completed execution; it does not reopen any executed-study choice. The 58 failures
do not authorize rerun, recomputation, regeneration, mutation, or a third attempt. Every completed
economic/result artifact remains frozen evidence and unpublished/unaccepted.

No durably retained raw full-pytest output artifact or hash was supplied to this governance lane,
and the inactive evidence store may not be inspected to invent one. This decision therefore records
only the verified aggregate `58 failed / 6663 passed` and the verified common failure class. It makes
no claim that a complete raw failure transcript was retained.

## Decision

### 1. Exact authority granted

After this decision receives a new independent full exact-head review, principal exact-head
acceptance, merge, and immediate post-merge verification, it authorizes exactly **one** later bounded
implementation on the existing PR #316 branch. That implementation may correct only the
postexecution test-harness lifecycle defect needed to validate and publish the already-completed,
byte-preserved attempt-2 results. It may not recompute or alter them.

The later implementation may modify only:

1. `test_risk_level1_implementation.py`;
2. directly necessary factual provenance/reporting surfaces required to distinguish the historical
   preexecution focused-test identity from the corrected postexecution focused-test identity;
3. the already-generated preserved result, receipt, and marker artifacts, staged and committed
   intentionally only if every byte remains exactly identical to the frozen hashes in §4;
4. factual PR #316 body/reporting; and
5. factual `operations/WORKSTREAMS.yaml` synchronization if required by this merged authority.

No implementation correction is included in this governance PR. If the test-only correction is
insufficient, the later author must stop for new authority rather than expand scope.

### 2. Required PREEXECUTION and completed POSTEXECUTION semantics

The corrected harness must distinguish lifecycle state explicitly.

A valid **PREEXECUTION** state requires:

- no production attempt-2 approval receipt;
- no marker or execution receipt; and
- no results namespace.

A valid **COMPLETED POSTEXECUTION** state requires:

- exactly one governed attempt-2 approval receipt;
- exactly one consumed/completed marker-execution receipt;
- the complete canonical results namespace; and
- mutually consistent attempt, preexecution head, independent review, hashes, registered/executed/
  ineligible counts, order, consumed status, and timestamps.

The harness must always fail closed for results without an execution receipt; an execution receipt
without approval; a partial result namespace; wrong attempt; contradictory consumed status;
impossible timestamps; hash drift; changed trial counts or order; duplicate result artifacts; a
missing canonical result artifact; or result bytes changed from the frozen hashes.

### 3. Exact correction requirements

The one authorized correction must:

1. distinguish PREEXECUTION from lawfully COMPLETED POSTEXECUTION state;
2. require receipt, marker/execution receipt, and results absent in preexecution state;
3. require exactly the governed receipt, consumed/completed marker-execution receipt, and canonical
   result namespace present in completed postexecution state;
4. preserve fail-closed behavior for malformed, tampered, contradictory, duplicate, partial, or
   impossible lifecycle states;
5. use fixtures and temporary paths instead of requiring the real completed production namespace to
   be absent;
6. never invoke preparation, acquisition, or execution;
7. create a separate corrected POSTEXECUTION focused-test identity and SHA-256;
8. preserve the original preexecution focused-test SHA-256 as historical provenance;
9. prove before/after byte-hash equality for every preserved result, receipt, and marker artifact;
   and
10. permit full `pytest`, exact-head CI, and a new independent full exact-head RESULTS review.

### 4. Frozen historical provenance

The later implementation and all publication reporting must preserve at least:

| Identity | SHA-256 / value |
|---|---|
| RISK-0002 accepted head | `cc6248fed90d6f3899fbbaa68236fe306efce1d9` |
| RISK-0002 merge | `e4d9fd69467755b7aa974c39dcb107e388910c52` |
| Attempt-2 preexecution head | `ffb314bb56dc8eacd946cd6cbaf650e710130710` |
| Attempt-2 preexecution review | `4940565638` |
| Stage-A attestation | `c3c96e50631aaa42de2c6225b2ff1803daa8ead432676579290ae6f01c07ee6c` |
| Preexecution metadata | `85d604deffa35603d40391a34c311ad1c342dc05ebb113e5d385eca7ca33ccbe` |
| Original code bundle | `d4934b6505dc0ee740d8b9bf37d6d0c816d354cca97fba794838ccf40640b9ef` |
| Original preexecution focused tests | `b7689e4d26992ecb8604204acad7b23a55a6d761ff8d1767f8a7cad877f02285` |
| Attempt-2 approval receipt | `ec9dd6aeb4b8f5751ea8679c700723203b20777e89623b52882508a0a144b2cd` |
| Completed execution receipt | `9d72f2b461e7834d24b3cadac0ebd5572e10c89519ae863b4ec7cc241158ac24` |
| `raw_evidence.json` | `eae2f5e54950efbe5fe97016d688b09529507c915658fed020e94568171c1cbc` |
| `cell_results.json` | `c5f6d8b0f24dee69ca0c398a42071ddbec04eddb0baeef014f6fb89932111b61` |
| `disposition.json` | `364a324c6dad68d84ee5126600e2caef6ac6d3253c739e6ed55773325107e5d5` |
| `diagnostics.json` | `f1c5d08fdebb368472c5e07a4c485d3c8356ed3c7116737dc6ba348d17ce5b04` |
| `RESULTS.md` | `2a6b814e8df578bbc30c4bf2c40e05815df48cf0d1c2308630b7f7042ff207bc` |
| `LIMITATIONS_AND_SURVIVORSHIP.md` | `28eb4796d371ffb527845b8539b5cbb14493a191452b2f37bca4956a21971deb` |

The first-cell and completion timestamps, `777 / 609 / 168` accounting, zero reserve and zero
duplicate/missing/extra accounting, four `unable_to_determine` family dispositions, consumed-attempt
status, no-third-attempt boundary, no-policy-adoption boundary, and `58 failed / 6663 passed`
publication-blocker fact are equally frozen provenance. The original preexecution focused-test hash
must remain recorded even after a separate corrected postexecution hash is created.

### 5. No production-code or study-identity authority

This decision does **not** authorize edits to:

- `risk_level1_runner.py`;
- `risk_level1_core.py`;
- `risk_level1_acquisition.py`;
- `risk_level1_result_validator.py`;
- any production evaluation or reduction code;
- `PROTOCOL_V1.md` or `pre_registration.yaml`;
- configuration, source/provider/fallback selection, eligibility, missingness, registry, trial
  inventory, scenario, metric, window, threshold, formula, or family-disposition logic; or
- Stage-A or preexecution metadata identity.

The test harness may validate the frozen production outputs. It may not become authority to change
them.

### 6. Absolute prohibited scope

Absolutely prohibited are any registered-cell execution, continuation, restart, retry, third attempt,
recomputation, result regeneration, result mutation, receipt mutation, execution-receipt mutation,
marker-history rewrite, Stage-A rewrite, preexecution-metadata rewrite, raw/transformed/receipt/
quarantine data change, reacquisition, provider/fallback change, protocol or preregistration change,
trial-registry or eligibility change, methodology/metric/scenario/window/threshold change,
family-disposition or economic-interpretation change, holdings/targets/tiers change, Level-1 or
Level-2 sizing, cash/liquidity policy, margin/leverage/debt policy, charts/ladders, portfolio-policy
adoption, and brokerage/order capability.

No receipt, marker, result, or historical artifact may be rewritten merely to satisfy a test. No
failure of the bounded correction creates authority to repair production code, rerun the study, or
publish a changed result.

### 7. Publication path after effectiveness

Only after this decision is independently reviewed, principal-accepted, merged, and post-merge
verified, the later implementation must proceed in this order:

1. reopen the same PR #316;
2. reactivate `/private/tmp/Portfolio-HQ` as the sole mutation lane;
3. fetch updated `main`;
4. merge the RISK-0003 `main` merge commit into the PR #316 branch, without rebasing;
5. preserve `ffb314bb56dc8eacd946cd6cbaf650e710130710` as historical ancestry;
6. verify before/after byte equality for every preserved result, receipt, and marker artifact;
7. apply only the authorized test-harness correction;
8. create the new postexecution focused-test hash while preserving the historical preexecution hash;
9. stage the already-existing ignored result artifacts intentionally without modifying their bytes;
10. run the corrected focused suite;
11. run the canonical result validator unchanged;
12. run full `pytest`;
13. run repository validators, parsers, diff checks, and protected-path scans;
14. commit and push to the same PR #316 branch;
15. obtain exact-head CI;
16. stop for a new independent full exact-head RESULTS review;
17. obtain principal exact-head acceptance only after a clean RESULTS review;
18. merge PR #316 only after acceptance and the normal lifecycle; and
19. perform immediate post-merge verification in the merge session.

No rebase is permitted. No other PR may replace #316. Reopening #316 before this decision becomes
effective is prohibited.

### 8. Governance package scope and effectiveness

This governance-only filing touches exactly:

1. this decision;
2. `governance/decisions.yaml`;
3. `operations/WORKSTREAMS.yaml`; and
4. the two mechanical decision-count assertions in
   `test_portfolio_hq_dashboard_decisions.py`.

It contains no RISK implementation, test-harness correction, receipt, marker, execution artifact,
result artifact, protocol, preregistration, registry, data, economic interpretation, or production
file from the parked worktree. It changes no portfolio policy.

This decision remains proposed and ineffective until its own independent full exact-head review,
principal exact-head acceptance, merge, and immediate post-merge verification complete. The author
stops after the draft governance PR is open and exact-head CI succeeds. The author does not self-
review, mark ready, principal-accept, merge, reopen PR #316, reactivate the evidence store, apply the
test correction, publish results, or execute any RISK cell.

## Rationale

Attempt 2 completed exactly once and produced a canonically validated, internally reconciled result
record. The only publication blocker is that preexecution-focused tests incorrectly treat lawful
postexecution artifacts as forbidden. Treating those assertions as execution failure would erase the
completed lifecycle boundary and create an unlawful rerun path. Treating them as harmless and
publishing without a clean full suite would weaken the repository's fail-closed publication gate.

The narrow correction is therefore to preserve every completed byte and every consumed-attempt fact,
teach fixture-based tests to distinguish two lawful lifecycle states, retain historical test identity,
and require a new exact-head RESULTS review. This corrects validation mechanics without creating a
single new economic degree of freedom.

## Alternatives Considered

**Rerun attempt 2 or authorize attempt 3.** Rejected. Attempt 2 completed, results were observed, its
authority is consumed, and RISK-0002 §13 expressly grants no further execution.

**Delete or rename completed artifacts so preexecution tests pass.** Rejected. That would mutate or
conceal frozen evidence and falsify the lifecycle state.

**Change production code or the canonical result validator.** Rejected. No production or economic
failure was identified; changing those surfaces would exceed the defect class.

**Publish despite 58 failing tests.** Rejected. Exact-head full-suite validation is a mandatory
publication control, and the lawful remedy is a bounded lifecycle-aware harness correction.

**Create a new results PR.** Rejected. RISK-0002 authorized the existing implementation/results PR,
and preservation of its approved preexecution ancestry and review provenance requires reopening the
same PR #316.

## Consequences

If this decision completes its lifecycle, one test-only, postexecution-only correction may make the
already-completed result package publishable without changing any evidence byte or executed-study
fact. PR #316 remains parked until then. Attempt 2 remains consumed, no third attempt exists, and all
results remain unpublished and unaccepted pending corrected exact-head CI, a new independent full
RESULTS review, and later principal acceptance.

If the bounded test correction cannot establish the required lifecycle semantics and byte-identity
proofs without touching prohibited production or study surfaces, work stops for new authority.
