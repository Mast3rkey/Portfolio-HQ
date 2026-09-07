---
decision_id: RISK-0002
date: 2026-08-14
status: Proposed
category: research_charter_amendment
related_decisions: [GOV-0001, GOV-0002, GOV-0003, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, LEVEL2-0001, RISK-0001, MARGIN-0005, LADDER-0001]
supporting_artifact: null
file: governance/decisions/RISK-0002-separately-authorized-integrity-reexecution-amendment.md
---

## Context

### Live preflight and identifier

This Lane-G filing began from live-verified GitHub, repository, and forensic state. GitHub `main`,
local `main`, `origin/main`, and the stopped RISK implementation branch all resolved to
`028ec2e9f2a4c74753414842e3dcc55b11134fff`, the merge commit of PR #314. PR #314 was merged from
exact head `985a315c353250bc330b95593d454d42b1ceaa65`; the open-PR inventory was empty. The decision
catalog and decision directory reconciled at 118 records, and `RISK-0002` had no file, catalog, or
tracked-repository collision. `RISK-0002` is therefore the exact live identifier for this amendment.

The stopped implementation lane is deliberately not the mutation lane for this filing. Its worktree
is `/private/tmp/phq-risk0001-results`, its branch is `codex/risk-0001-data-results`, and its HEAD/base
is the same `028ec2e9f2a4c74753414842e3dcc55b11134fff`. It remains dirty and uncommitted with one
tracked modification, 1,099 nonignored untracked files, 144 material ignored files, and 1,244
material files in total. It has zero commits beyond main, zero pushes, and zero PRs. This filing uses
a separate clean governance worktree and does not edit, stage, stash, reset, rebase, commit, push,
delete, clean, or reuse the stopped lane.

### Controlling authority

The Investment Constitution, `GOV-0002`, `GOV-0003`, `OPS-0009`, `OPS-0014`, `NUM-0001`, effective
merged `XASSET-0019`, frozen research-only `LEVEL2-0001`, and `RISK-0001` remain controlling.
`MARGIN-0005` supplies hash, manifest, preexecution-integrity, and failed-trial-accounting precedent.
`LADDER-0001` demonstrates that a pre-execution correction may replace a pin only before any result
exists; its narrower precedent does not itself authorize this post-marker execution.

`RISK-0001` §14 controls this case: results may not be rerun merely because a defect is discovered,
and another execution requires a separately accepted charter amendment or new RISK authority for a
separately governed integrity correction. This decision is that narrow amendment. It does not edit,
supersede, or loosen `RISK-0001`; it creates one additional authority whose effectiveness is gated on
its own acceptance and merge.

### Failed attempt and observation boundary

The original execution is retrospectively identified as `RISK-0001-EXECUTION-ATTEMPT-001`. It began
when the execution marker was written at `2026-08-14T12:29:28Z` and failed at
`2026-08-14T12:31:36Z`. Stage A passed; Stage B eligibility was frozen at 777 registered cells, of
which 609 were eligible and 168 were pre-execution ineligible/null. No result artifact and no partial
result ledger were persisted. No author-visible metric or result was identified, no result or
conclusion was printed or logged, and no complete four-family disposition or adopted portfolio
conclusion existed.

The exact observation classification is `PARTIAL_INTERNAL_RESULTS_OBSERVED`, not zero-results.
Metrics and the `EQUITY` and `FUND_BROAD_MARKET` family reductions transiently existed in process
memory. The first failure occurred while entering `FUND_GLD_DEFENSIVE` reduction. Because internal
partial computation occurred after the marker, no economic, acquisition, provider, eligibility,
parameter, metric, scenario, window, threshold, methodology, or trial choice may change in response.

## Decision

### 1. Exact RISK-0001 identity is preserved

The already-frozen study identity remains exactly:

| Identity | SHA-256 |
|---|---|
| `RISK-0001` protocol | `90277ad4767e4766d7a38c1199affde66f44e55ff16fd7f73e0894380cf8a425` |
| `RISK-0001` preregistration | `8da1697456e8a8f4a168c99ae8387c77cd023e0e615cf51c78110165223d3c5a` |
| implementation configuration | `9f97162260ca97ef340b56811d8d91009235922cddf478ff39be7270614301de` |
| frozen eligibility matrix | `3854e9203c6b282e3d7c398b19a8f35de6cdad1c291b06456af19fa4d47ed680` |
| frozen trial registry | `8942227dfba3a4fff6b1b94067ad252f0890cfa0959e2939e25ef98036904f51` |
| attempt-1 failed data-gate freeze | `e6a14574e743827c35a0ed99ea3aa186d30125217eb1d121978ee0fb738a05c5` |

`RISK-0002` changes none of these identities, files, economic values, or registered rules. The
protocol, preregistration, implementation configuration, eligibility matrix, and trial registry are
inputs to be identity-verified, not reopened authority.

### 2. Attempt identities and defect classification

The only attempt identities are:

- original failed attempt: `RISK-0001-EXECUTION-ATTEMPT-001`; and
- one future corrected attempt: `RISK-0001-EXECUTION-ATTEMPT-002`.

Attempt 1 is a failed, historically preserved execution with partial internal computation only, no
durable result artifact, no partial result ledger, no author-visible result identified, and no
adopted portfolio conclusion. Its defect is classified exactly
`IMPLEMENTATION_INTEGRITY_ONLY`. The preflight found no authority ambiguity, preregistration defect,
methodology defect, economic-value change, parameter change, metric/window/provider/scenario change,
result-aware acquisition, history mining, or post-result provider substitution.

### 3. Exact defect mechanics

The canonical evaluator intentionally requires each `gold_peer_evidence` mapping to use this exact
registered key order:

1. `peer_id`
2. `identity_and_inception`
3. `unresolved_required_session_gaps`
4. `dividend_split_action_treatment`
5. `overlap_total_return_correlation`
6. `overlap_annualized_return_difference_pp`
7. `overlap_max_drawdown_difference_pp`

The in-memory constructor produced that order. A JSON write using `json.dumps(..., sort_keys=True)`
recursively alphabetized nested keys. JSON load then preserved the wrong serialized order, and the
fail-closed canonical evaluator correctly rejected the record. The defect was deterministic and was
present before the attempt-1 execution marker. It changes serialization structure, not economic
evidence or values. The vulnerability class is every ordered schema-bearing nested mapping that
passes through sorted JSON serialization, not only `gold_peer_evidence`.

The evaluator's exact-order checks are correct authority enforcement. They must not be weakened,
removed, or made order-insensitive as a remedy.

### 4. Forensic preservation of attempt 1

The original stopped worktree and its attempt evidence must remain local forensic evidence and must
not be overwritten or mutated by this amendment or by attempt 2. Its aggregate material identity is:

| Scope | Aggregate SHA-256 |
|---|---|
| all 1,244 material files | `bee2e34fc438d92b51811f756e16a7f474229a4b985114190c3655c1c3c3c63f` |
| raw | `76b9a429d15280b9b16624e66cc80129d2a7359cb12bcc948ed126ad2c19bfb7` |
| receipts | `abf6f603d71f388288a4c3e691e810f683f36fbec2c5d696ef9448551a677ce7` |
| transformed | `955f3cd5a61aa465697b1b128b102114ab97ade549cc3f0196194d1049aec605` |
| quarantine | `17a8cced2e0886165f17d3b2d76844b167b8a02cf1b0b0c1891c315eac2df467` |

The aggregate convention is SHA-256 over the sorted relative-path `shasum -a 256` manifest for the
named scope. Licensed or quarantined bytes are not committed merely to preserve them. Their local
forensic identity and the hashes above are sufficient; repository licensing policy remains
unchanged.

### 5. Frozen-input reuse is mandatory

Attempt 2 must reuse exactly, byte-for-byte or identity-for-identity as applicable:

- raw data bytes, acquisition receipts, and raw hashes;
- transformed data and transformed hashes;
- corporate-action evidence;
- provider and fallback selections;
- the eligibility matrix and every missingness classification;
- the exact protocol and preregistration hashes;
- the exact implementation configuration except for the expressly allowlisted integrity code and
  attempt-2 metadata identities in §7;
- all 777 registered cell identities and every trial-registry entry; and
- every registered window, metric, scenario, threshold, formula, and result rule.

No data may be reacquired, refreshed, substituted, restitched, retransformed, reclassified, or
selected again for attempt 2. This mandatory reuse prevents result-aware reacquisition, history
mining, provider substitution, eligibility drift, and unused-capacity reuse. A hash or identity
mismatch stops the reexecution; it does not authorize repair by changing frozen evidence.

### 6. Attempt-1 artifacts are historical only

Attempt 1's execution receipt, defect record, and data-gate freeze remain preserved as historical
`RISK-0001-EXECUTION-ATTEMPT-001` evidence. They must not be overwritten, renamed into attempt 2,
or reused as attempt-2 attestations. Attempt 1 remains visible in the history even if attempt 2 later
completes successfully.

Attempt 2 must instead generate new, attempt-specific artifacts containing:

- the `RISK-0001-EXECUTION-ATTEMPT-002` identity and new timestamps;
- the corrected-code identity and SHA-256;
- the focused-test identity and SHA-256;
- a new Stage-A integrity attestation binding the corrected code to every unchanged frozen input;
- a new execution receipt; and
- new final result hashes if execution completes.

Nothing else may differ. The attempt-2 Stage-A attestation may reference attempt-1 frozen artifacts
by verified hash, but it may not present an attempt-1 receipt, defect record, or freeze as a newly
generated attempt-2 attestation.

### 7. Exact allowlisted implementation correction

After this amendment completes its full lifecycle, one new clean implementation lane may make only:

1. ordered serialization for exact-schema mappings;
2. corresponding deserialization or round-trip handling where mechanically necessary to preserve
   registered order;
3. the minimum attempt-2 metadata/namespace required by this authority; and
4. focused fixture-only regression and adversarial tests for this vulnerability class.

The expected principal implementation surface is `risk_level1_runner.py` and
`test_risk_level1_implementation.py`. Live implementation truth may justify a different or slightly
expanded file surface only when it is the smallest correction within the same ordered-nested-mapping
vulnerability class and the expansion is explicitly disclosed before execution.

This authority does not permit weakening evaluator order checks; changing the preregistration or any
canonical schema; changing numeric, evidence, or result fields; changing economic calculations; or
changing order-insensitive hash serialization whose canonical identity deliberately uses sorted
keys. The correction must distinguish schema-bearing ordered serialization from canonical
order-insensitive hash serialization.

### 8. Wider vulnerability-class validation

Before attempt 2, focused fixture-only validation must cover `gold_peer_evidence` and every ordered
nested mapping written to and read from JSON by the corrected implementation. It must prove:

- exact expected key order survives deterministic round trip;
- missing keys fail closed;
- extra keys fail closed;
- duplicate keys fail closed where the parser boundary can observe them;
- semantic equality and structural order both hold;
- numeric and result values are immutable across round trip; and
- the canonical evaluator remains fail-closed without weakened order enforcement.

These tests may use fixtures only. They may not load frozen market data, run a registered cell,
compute a RISK metric, reduce a family, or inspect attempt-1 transient results.

### 9. Exact reexecution identity and no new trial capacity

Attempt 2 is the same RISK-0001 study, not a new experiment. It must use identical protocol,
preregistration, configuration, raw/transformed data hashes, corporate-action evidence,
provider/fallback selections, eligibility, missingness, 777 registered cell IDs, windows, metrics,
scenarios, thresholds, formulas, and result rules.

The only lawful differences are `RISK-0002` authority, integrity-corrected code hash, focused-test
hash, attempt-2 Stage-A attestation, attempt ID/timestamps, and final result hashes. Attempt 2 uses the
same 777 registered cell identities. It has zero reserve, replacement, added, alternative, or
unused-capacity trials. No acquisition, provider, fallback, eligibility, parameter, metric, scenario,
window, threshold, methodology, or registered-cell choice may be altered between attempts.

### 10. One separately authorized integrity reexecution

Upon this decision's effectiveness, it authorizes exactly one
`separately_authorized_integrity_reexecution`: a one-time, non-discretionary,
integrity-corrected execution of the already-frozen RISK-0001 study.

This is not a routine rerun, not a retry, not a new study, and not precedent. It does not restore any
general rerun authority. The authority is consumed when attempt 2 begins, defined as the first
registered cell beginning execution after the preexecution gate in §11 passes. A failure before that
point leaves the execution unbegun and blocked; any remediation must remain inside §7, and any head
change requires the entire affected validation and independent preexecution exact-head review to run
again before a cell may execute. Once attempt 2 begins, no second start, continuation from a partial
ledger, regeneration, or third attempt is authorized under `RISK-0002`.

### 11. Preexecution gate

Attempt 2 may not begin until every condition below is complete in order:

1. this RISK-0002 governance PR receives independent full exact-head review;
2. the principal accepts that exact head;
3. the PR merges and post-merge verification succeeds;
4. a new clean implementation lane is created from the amended `main`—never from or inside the
   stopped attempt-1 lane;
5. frozen artifacts are transplanted into the clean lane or referenced from preserved storage and
   every byte/hash/identity in §§1, 4, 5, and 9 revalidates;
6. the allowlisted correction is applied;
7. every fixture-only test in §8 passes;
8. all frozen identity hashes revalidate and a new attempt-2 Stage-A integrity attestation is
   generated; and
9. one independent preexecution full exact-head review confirms that the correction matches §7,
   frozen inputs are unchanged, no result-aware change exists, and no registered cell has executed.

The independent preexecution review must be retained and anchored to the exact corrected
implementation head. CI, fixture tests, or self-review cannot substitute for it. Only after that
review passes may `RISK-0001-EXECUTION-ATTEMPT-002` begin.

### 12. Results lifecycle

After attempt 2 begins, the implementation must execute the frozen cells non-discretionarily and
persist results once. It must open exactly one draft implementation/results PR containing the new
attempt-2 receipt, ledger/results required by RISK-0001, result hashes, limitations, and the preserved
attempt distinction. That exact head requires full independent results review and explicit principal
acceptance of the research record before merge if clean.

No result automatically changes the portfolio. A separate later Level-1 methodology/policy decision
is required before any economic conclusion can become policy. Replacement Level-1 sizing and final
Level-2 membership/sizing remain blocked until the RISK lifecycle lawfully completes.

### 13. Policy boundary and future rerun rule

This amendment creates no target or Level-1 sizing change; no Level-2 membership or sizing; no
residual, cash, or liquidity assignment; no margin, debt, or leverage authority; no optimizer,
portfolio construction, whole-100% reconciliation, allocation check, execution, trading, or
automatic adoption. Recommendation-only manual execution remains unchanged.

After attempt 2 begins, `RISK-0002` grants no further execution. Any later defect, evidence regime,
reacquisition need, methodology change, or proposed repeat requires a new separately accepted RISK
authority. Neither a failed attempt 2 nor an implementation-integrity label creates automatic future
authority.

### 14. Approved files and effectiveness boundary

This governance-only filing touches exactly:

1. this decision;
2. `governance/decisions.yaml`;
3. `operations/WORKSTREAMS.yaml`; and
4. the two mechanical decision-count assertions in `test_portfolio_hq_dashboard_decisions.py`.

It does not modify `RISK-0001`, `PROTOCOL_V1.md`, `pre_registration.yaml`, the RISK preregistration
validator, serializer or implementation code, serializer-defect tests, data, results, eligibility,
the trial registry, or any protected portfolio path.

This decision is proposed authority until its own independent full exact-head review, principal
acceptance, merge, and post-merge verification complete. Filing, CI, or review alone does not make it
effective. The author stops after the draft PR is open and exact-head CI completes successfully; the
author does not self-review, mark ready, principal-accept, merge, begin the serializer correction, or
begin attempt 2.

## Rationale

Attempt 1 crossed the execution marker and produced partial internal computations, so calling it a
zero-result failure or silently rerunning would violate RISK-0001 §14. At the same time, the defect is
deterministic, pre-marker implementation structure: recursive key sorting changed an ordered schema
without changing any economic byte or value. The narrowest honest response is therefore to preserve
attempt 1, prohibit every result-aware choice, reuse the frozen evidence exactly, correct only the
serializer boundary, and require an independent preexecution review before one separately authorized
attempt. This retains the anti-mining and no-rerun protections while allowing the preregistered study
to produce a lawful record.

## Alternatives Considered

**Treat attempt 1 as zero-results and rerun under RISK-0001 alone.** Rejected. Partial internal
results existed, and RISK-0001 expressly says a discovered defect does not authorize another run.

**Amend the preregistration or relax exact-order evaluation.** Rejected. The evaluator correctly
enforced frozen schema; weakening it would convert an implementation defect into methodology drift.

**Reacquire or regenerate inputs in a clean lane.** Rejected. Post-result reacquisition or provider,
eligibility, transformation, or corporate-action changes would create result-aware degrees of
freedom. Exact reuse is load-bearing.

**Continue inside the stopped dirty lane.** Rejected. It is attempt-1 forensic evidence and must not
be overwritten. A clean post-amendment implementation lane is mandatory.

**Authorize reserve trials or repeat on a third failure.** Rejected. RISK-0001 registered exactly
777 cell identities and zero reserve capacity. This amendment authorizes one attempt only.

## Consequences

If this decision completes its lifecycle, exactly one clean implementation lane may apply the
allowlisted integrity correction, pass fixture-only and independent preexecution gates, and begin
`RISK-0001-EXECUTION-ATTEMPT-002`. Attempt 1 remains permanently visible. The study identity and
every economic choice remain unchanged. No policy, sizing, portfolio, margin, debt, leverage,
allocation, or trading authority is created.

If the preexecution gate cannot prove exact frozen-input identity, the work stops. If attempt 2 later
fails after it begins, `RISK-0002` is exhausted and no third attempt is permitted without new
separately accepted authority.
