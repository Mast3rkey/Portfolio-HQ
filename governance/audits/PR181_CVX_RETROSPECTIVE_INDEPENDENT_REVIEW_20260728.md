# PR #181 CVX Retrospective Independent Review

**Proposed filename:** governance/audits/PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md

## 1. Reviewer identity and independence

An independent Claude Code session, launched specifically and solely to perform
this retrospective review of PR #181. This session did not author PR #181, its
CVX Company Intelligence records, its comparison artifact, its evidence-recovery
audit, or any commit therein. This session performed no repository edits, opened
no branch, commit, PR, GitHub review, or comment, and created no governance
authorization. Independence from authorship is satisfied per `OPS-0007` §1.

## 2. Repository and PR

Repository: `Mast3rkey/Portfolio-HQ`
PR: #181, "WS-0005 Milestone 3 Batch 9: CVX Company Intelligence (PI-0031)"

## 3. SHAs

- Base: `e1fa0739ad83f52686597f3b5f5e4ee577160f77` (PR #180's merge commit)
- Reviewed head: `a79d237cc53f7b623814e3177dfc124d36c6377a`
- Merge commit: `173fef53e73f0e9df86df4a81c38464167d2bbf4` (parents:
  `e1fa0739ad83f52686597f3b5f5e4ee577160f77`,
  `a79d237cc53f7b623814e3177dfc124d36c6377a`)
- `origin/main` at time of this review: `8768bfddd288bd493357b943d076dd12413b7b7f`
- Confirmed: reviewed head is a direct parent of the merge commit; the merge
  tree is byte-identical to the reviewed head's tree; none of the 7
  implementation files has changed between the merge commit and current
  `origin/main`.

## 4. Evidence-artifact identity

Filename (not committed to this repository, principal-supplied implementation
input per PR #181's own disclosure): `CVX_PRIMARY_SOURCE_EVIDENCE_RECOVERY_20260728_v3.yaml`
Recomputed SHA-256 by this review: **not independently recomputable** — the raw
bundle is not retained in-repo (consistent with Batch 5/6/8 precedent). This
review instead verified internal consistency: the SHA-256
`8256231340142d35289a5336bc2162c575164fe1df3db39ee4ecb6a20fb75203` is cited
identically across the retained audit, CVX.yaml, CVX.md, the comparison
artifact, and the PR/commit messages, and the retained audit documents a
methodologically sound independent-recomputation process (checksum, line/word/
byte counts, source/claim counts, reciprocal-pair counts, zero orphans, zero
duplicates, all recomputed via direct YAML parsing) performed by the
implementing session before use. No condition requiring broader evidence
inspection was present (hash match confirmed consistent throughout; no
retained-validation gap; no claim found outside the evidence envelope; no
source conflict; no specific factual concern raised).

## 5. Review date

2026-07-28

## 6. Exact reviewed file set

- intelligence/companies/CVX.yaml
- intelligence/companies/CVX.md
- intelligence/BATCH9_OIL_CLUSTER_COMPARISON.md
- intelligence/freshness_registry.yaml
- intelligence/freshness_checkpoints.yaml
- operations/WORKSTREAMS.yaml
- governance/audits/CVX_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260728.md

Confirmed exact match to PI-0031's authorized file set; no discrepancy.

## 7. Methods and validations

- `git diff`/`git merge-base --is-ancestor`/`git log` ancestry and tree-identity
  checks (base, head, merge, current main).
- `intelligence_validator.py` run in an isolated worktree at the exact reviewed
  head: 39/39 Company Intelligence records valid.
- `freshness_validator.py` run at exact head: OK.
- Full pytest suite run at exact head: 1502/1502 passed (14.94s).
- `git diff --check` base→head: clean.
- GitHub check run `90355149232` ("test") on this head: `success`.
- Protected-path diff (targets.yaml, holdings.yaml, allocate.py, margin_state.py,
  XOM.yaml/.md, CLAUDE.md, constitution/, governance/decisions/, spec docs)
  base→head: empty.
- `git diff` on XOM.yaml/XOM.md base→head: empty (unmodified).
- Text scan for rank/score-family language in the four new/changed content
  files: 9 matches, all negation/prohibition context.
- Decision-index reconciliation at exact PR head: 42 filed = 42 indexed.
- Schema/vocabulary spot-checks: `portfolio_role_ref: band` and
  `conviction.rating: Medium` cross-checked against `targets.yaml`
  (`band` tier; `oil` cluster `[XOM, CVX]` @ 20%) and PI-0004's closed
  four-value conviction vocabulary — both compliant.
- `pull_request_read` (GitHub API): confirmed zero reviews, zero comments on
  PR #181; confirmed zero open PRs repository-wide (no overlap).
- No check claimed as passed without being run or inspected in this session.

## 8. Findings by severity

**BLOCKER:** none.

**MATERIAL:** none against the CVX research, comparison artifact, schema,
validators, tests, or authorization scope.

**MINOR / NOTE:**
1. (NOTE — review-retention gap, closed by this artifact) PR #181 carries zero
   retained GitHub reviews or comments. `PI-0031` §H.7–9/§J required an eligible
   independent `OPS-0007` §1 review, anchored to the exact merged head, retained
   before merge; none exists for PR #181 on GitHub. `operations/WORKSTREAMS.yaml`'s
   own CVX-implementation register entry still states the PR is "not merged…
   none of which has occurred yet," which is now factually stale — the PR has
   merged. This mirrors `OPS-0004`'s FA-1 finding on PR #143 exactly: a gap in
   retained review *provenance*, not a finding that the underlying work is
   defective. This document is filed as the missing retained, attributable
   independent review.
2. (NOTE) The raw evidence-recovery bundle YAML is not committed to this
   repository — only the audit `.md` summarizing/verifying it is retained,
   consistent with Batch 5/6/8's identical convention.
3. (NOTE) `CVX.yaml`'s `sources[]` lists 5 citations against the underlying
   bundle's 7 source IDs; verified as a reasonable consolidation (shared SEC
   accession numbers for the 10-K index/document pair and the 8-K/Exhibit 99.1
   pair), not a provenance loss.

## 9. Event occurrence vs. prior retention — explicit distinction

The independent structural/byte-level verification described in the retained
audit (§2 of `CVX_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260728.md`) is found,
on its own internal evidence, to have actually occurred at implementation time —
its methodology, granularity, and specificity are consistent with the identical
convention already established and separately audited in Batches 5, 6, and 8.
What was *not* retained before this review is an independent, attributable,
GitHub-anchored review-and-acceptance record for the implementation PR itself
(PR #181) — a distinct fact from whether the underlying evidence-recovery work
happened. This review supplies that missing retained record; it does not
allege, and finds no evidence for, the underlying CVX research being unsound.

## 10. Verdict

**PR #181 CVX EXACT-HEAD RETROSPECTIVELY APPROVED**

## 11. Scope of authority created

This artifact creates no investment, allocation, margin, trading, tier, target,
cluster, cap, holdings, allocator, Milestone 4, tenth-Milestone-3-batch, or
further-research authority of any kind. It is a retrospective review-retention
record only, closing the specific `OPS-0007` review-retention gap identified
above for PR #181. Any use of the CVX Company Intelligence record for anything
beyond that record's own stated, bounded, advisory scope requires its own
separate, future, explicit governance authorization, exactly as `PI-0031`,
`OPS-0007`, and `OPS-0008` already require.
