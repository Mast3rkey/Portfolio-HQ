# PR #166 Corrected-Head Exact-Head Review

**Reviewer:** GPT-5.6 Thinking  
**Review type:** independent exact-head review  
**PR:** #166  
**Base:** `92ea06705b1707d8b7644e311e4f086f462e9573`  
**Reviewed head:** `6c67eb0573d9482a8bfe6e308cd00a8cd4284aca`  
**Evidence bundle:** `PR166_CORRECTED_DELTA_EVIDENCE_BUNDLE.md`  
**Evidence bundle SHA-256:** `09e3a8bcbaa5ec9ea2a46e09e8bacca33bfc0fee672cdaea2a51c2352358b3ea`  
**Verdict:** **CHANGES REQUIRED**

## Independence and scope

GPT-5.6 Thinking did not author or edit PR #166. This review used the corrected-head evidence bundle and independently inspected official Quanta sources relevant to a surviving material claim.

The prior ETN, VRT, and PWR corrections identified in `PR166_PRIMARY_SOURCE_AUDIT.md` are verified as resolved at the reviewed head, except for the new findings below.

## M5 — Major — PWR’s direct data-center exposure remains materially misstated

The corrected comparison still states:

- “Data-center exposure is entirely indirect”
- PWR “never sells anything to, or installs anything inside, a data center itself”
- PWR’s customers are principally utilities and telecom carriers, distinct from hyperscalers and data-center operators
- PWR’s entire revenue is contract-services work for utilities, telecom carriers, and pipeline operators

These claims are contradicted by official Quanta evidence:

1. Quanta’s 2025 Form 10-K states that it provides design and installation of electrical systems for large load centers, including data centers, and that its customer base includes hyperscalers and technology companies.
2. The same Form 10-K states that the Cupertino Electric acquisition increased demand for Quanta’s critical-path electrical design and installation solutions from the technology and data-center industry.
3. Quanta’s official Cupertino Electric acquisition release states that CEI:
   - has more than 25 years of data-center industry experience;
   - designs and installs critical electrical systems;
   - has installed electrical systems in more than 20 million square feet of data centers;
   - is a custom manufacturer of modular electrical systems for large-scale data centers.

Official sources independently inspected:

- Quanta 2025 Form 10-K:  
  `https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm`
- Quanta acquisition of Cupertino Electric:  
  `https://investors.quantaservices.com/news-events/press-releases/detail/360/quanta-services-acquires-cupertino-electric-inc-a-premier-electrical-infrastructure-solutions-provider-to-the-technology-and-renewable-energy-industries`
- Quanta operating-company profile for Cupertino Electric:  
  `https://www.quantaservices.com/companies/cupertino-electric-inc`

Required correction:

- Correct `PWR.yaml` and `PWR.md` to distinguish:
  - direct in-facility data-center electrical design, installation, commissioning, maintenance, modularization, and modular-electrical-system manufacturing through CEI; and
  - indirect utility/grid exposure through transmission, generation interconnection, substations, and AEP.
- Correct the comparison’s §§2–4 and every other surviving passage that describes PWR’s data-center exposure as entirely indirect, denies inside-the-data-center activity, excludes hyperscalers/technology customers, or treats all revenue as utility/telecom/pipeline contract work.
- Reassess overlap and differentiation conclusions after recognizing that PWR overlaps with ETN/VRT more directly inside the facility than the current comparison states.
- Do not rank companies or recommend a tier, target, cluster, cap, allocation, trade, or margin action.

## M6 — Major — The controlling external audit is referenced as retained but is absent from repository truth

`operations/WORKSTREAMS.yaml` and the PR body repeatedly identify `PR166_PRIMARY_SOURCE_AUDIT.md` as the retained, authority-bearing evidence-recovery artifact. The corrected-head evidence collector found no such file anywhere in the repository.

Because Claude could not inspect the primary sources and the GPT audit is the controlling provenance for the corrections, merging while referencing an absent “retained” artifact would leave a broken evidence chain and an inaccurate repository-state claim.

Required correction:

- Add the original audit, unchanged in substantive content, at:
  `governance/audits/PR166_PRIMARY_SOURCE_AUDIT_20260726.md`
- Add this corrected-head review at:
  `governance/audits/PR166_CORRECTED_HEAD_REVIEW_20260726.md`
- Update references in `operations/WORKSTREAMS.yaml` and the PR body to the exact repository paths.
- Record each artifact’s reviewer, reviewed head, date, verdict, and SHA-256.
- Preserve the provenance split:
  - Claude was access-blocked;
  - GPT-5.6 Thinking independently inspected the named official sources;
  - Claude applied the retained findings without claiming direct inspection.

## m3 — Minor — Cumulative PR statistics and commit count remain stale

The live cumulative state is:

- 10 files changed
- 2,307 insertions
- 5 deletions
- 4 commits

The PR body and `operations/WORKSTREAMS.yaml` state 2,242 insertions and describe the cumulative state as spanning three commits. The missing 65 insertions correspond to the final WORKSTREAMS synchronization commit.

Required correction:

- Replace stale cumulative statistics and commit-count wording with values recomputed after all new correction commits.
- Do not hard-code the current 10/2307/5/4 values after adding the two audit artifacts and PWR correction; recompute final cumulative counts from the new exact head.

## Verified resolved and acceptable at reviewed head

The evidence bundle supports that:

- the prior ETN audit findings are resolved;
- the prior VRT audit findings are resolved;
- PWR manufacturing, employment, collective-bargaining, customer-concentration, customer-mix, and legacy-litigation findings are resolved;
- the comparison no longer relies on the prior ETN/VRT/PWR errors, except for the surviving PWR direct-data-center misstatement above;
- all three conviction ratings were reassessed rather than mechanically copied;
- provenance language correctly distinguishes Claude from GPT inspection;
- freshness rows remain pending and monitoring-disabled;
- GEV remains comparison-only and untouched;
- no holdings, targets, allocator, margin, policy, or trade behavior changed;
- validators passed;
- 1,502 tests passed;
- both `git diff --check` ranges passed;
- exact-head CI succeeded;
- PR #166 remains open, draft, and unmerged.

## Required recovery sequence

1. Retain the original primary-source audit and this corrected-head review under `governance/audits/`.
2. Apply one bounded correction to PWR’s direct data-center exposure and the comparison.
3. Correct WORKSTREAMS and PR-body provenance paths and cumulative statistics.
4. Re-run validators, the full test suite, `git diff --check`, protected-path checks, and exact-head CI.
5. Keep PR #166 draft and unmerged.
6. Collect a fresh independent delta bundle for the new head.
7. GPT-5.6 Thinking performs a final delta review.

No Batch 5, Milestone 4, allocation, margin, policy, readiness, or merge action is authorized by this review.
