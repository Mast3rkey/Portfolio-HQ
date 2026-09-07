# WS-0005 Milestone 3 Criterion-7 Retrospective Lifecycle Audit — 13 Legacy Records + PR #189 Five-Record Lifecycle Closure

**Proposed filename:** `governance/audits/WS0005_M3_CRITERION7_RETROSPECTIVE_LIFECYCLE_AUDIT_20260729.md`

## 1. Authority and scope

Authorized by `governance/decisions/OPS-0010-ws0005-lifecycle-ratification-and-retrospective-audit-authorization.md`
(`status: Accepted`, merged via PR #191, merge commit `0863f9dbbb861afd752d0cfeaa28369dd3b321ec`; its
`status: Accepted` synchronized via PR #192, merge commit `59f7ac56fdb1a4c5b3c0e45d6b545ea88a126ec4`).
`OPS-0010` §3 authorizes exactly one later, separate implementation unit performing: (A) a combined
retrospective audit of the 13 pre-`OPS-0007` legacy Company Intelligence records; (B) a lifecycle-only
closure of the five PR #189 records; (C) factual synchronization of `operations/WORKSTREAMS.yaml`; and
(D) three narrow `CLAUDE.md` stale-wording corrections. This artifact is that audit's (A) and (B)
components. It performs no new company research, edits no Company Intelligence YAML/Markdown, and
authorizes nothing beyond what `OPS-0010` §3/§6/§7 already bound.

**This artifact does not itself promote any record to PROVISIONAL.** Per `OPS-0010`'s own stopping
condition and the implementing task's explicit "current status boundary": the 18 tickers audited here
remain unresolved until the implementation PR carrying this artifact (1) receives its own eligible
independent exact-head review, (2) completes any required bounded correction and re-review, (3) receives
a separately retained pre-merge `Principal acceptance:` statement per `OPS-0010` §2, (4) merges at the
unchanged accepted head, and (5) receives immediate post-merge verification. Every "ELIGIBLE FOR
PROVISIONAL AFTER THIS PR COMPLETES ITS LIFECYCLE" conclusion below is a **draft conclusion**, not an
effective status change.

## 2. Auditor/author role and independence limitation

**This artifact was authored by the same session that opened the implementation PR carrying it.** It is
therefore explicitly **not** an eligible independent review under `OPS-0007` §1.1 ("a session and model
that did not author or edit the reviewed work") — it cannot supply its own element-1 review requirement,
for itself or for any of the 18 tickers it evaluates. Its conclusions are evidence syntheses, drawn from
git history, GitHub PR/review data (via `pull_request_read`), governance decision text, and
`operations/WORKSTREAMS.yaml`'s own retained narrative — not a substitute for the independent,
capability-based review this PR itself still requires before any conclusion here carries repository
authority. Where this artifact concludes a legacy ticker's evidence is already sufficient (Batches 1-2,
PR #189's five), that conclusion rests on **pre-existing, already-retained evidence created by other
sessions at the time of each original merge** (GitHub review comments, dedicated post-merge
reconciliation PRs) — not on this session's own say-so.

## 3. Verified repository base

Independently verified this session, before any edit:

- Repository identity: `Mast3rkey/Portfolio-HQ`.
- `git fetch origin main`; local `HEAD` on branch `claude/ops-0010-retrospective-lifecycle-mehnxc`
  confirmed identical to `origin/main` at `59f7ac56fdb1a4c5b3c0e45d6b545ea88a126ec4` — matching this
  task's expected preflight cutoff exactly.
- Working tree confirmed clean before any edit (`git status`).
- **Zero open pull requests** confirmed via the GitHub API (`list_pull_requests`, `state: open` → `[]`).
- `59f7ac56...` confirmed PR #192's merge commit (`git log --oneline`: "Merge pull request #192 from
  Mast3rkey/claude/ops-0010-status-reconciliation-m3u83t"), itself the parent chain
  `PR #192 (59f7ac5) ← PR #191 (0863f9d) ← PR #190 (decaaa7)`.
- `OPS-0010` confirmed `status: Accepted` in both `governance/decisions/OPS-0010-...md` frontmatter and
  `governance/decisions.yaml`'s corresponding entry.
- `governance/decisions.yaml` reconciled against `governance/decisions/*.md` (excluding `README.md`):
  **46 files = 46 indexed entries, no orphans, no missing files.**
- `intelligence/companies/*.yaml`: **45 files**, `intelligence_validator.validate_directory(...)` →
  **45/45 valid**. `intelligence/themes/*.yaml`: **2/2 valid.**
- `freshness_validator.py` → **OK**.
- Full test suite: `python3 -m pytest -q` → **1502 passed**.
- `45 (Company Intelligence records) + 17 (PI-0033 dispositions: 14 new + 3 restated) = 62`, confirmed
  by independent set comparison against `targets.yaml`'s 65 total tiered tickers minus the 3 ETF names
  (SPY/QQQ/GLD) = 62 non-ETF governed tickers, zero overlap, zero omission (§8 below).

## 4. Methodology

For each of the 18 tickers named in `OPS-0010` §3.A/§3.B, this audit independently gathered (via direct
git history inspection, `pull_request_read` on every implementation PR identified, `governance/decisions/`
and `decision_log.yaml` text, and `operations/WORKSTREAMS.yaml`'s own retained narrative — not assumed
from any prior summary) the following per ticker: record identity; original implementation authority and
PR/commit; every retained GitHub review or `governance/audits/` artifact addressing that PR; correction
history; merge ancestry (direct-parent confirmation via `git log --format="%H %P"`); post-merge
verification evidence; and current freshness-registry state. Each of `OPS-0007` §3's five elements was
then mapped independently per ticker, using exactly the four classifications `SATISFIED` / `NOT
SATISFIED` / `INDETERMINATE` / `NOT APPLICABLE`. No element was inferred as satisfied from another
element, from a batch-level summary alone, or from silence. Where retained evidence was insufficient,
the ticker is held back and the exact missing action is stated — no historic evidence was fabricated or
extrapolated to close a gap.

## 5. OPS-0010 historical-acceptance ratification — how it is applied here

`OPS-0010` §1 ratifies, as a one-time principal governance act, that **"an eligible independent, exact-head
review under `OPS-0007` §1, followed by a same-account merge, with no intervening commit between the
reviewed head and the merged head"** satisfies `OPS-0007` §3 element 3 (explicit principal acceptance) for
WS-0005 lifecycle work merged at or before `OPS-0010`'s verified cutoff. **This ratification's own stated
precondition is the existence of an eligible independent, exact-head review** — where no such review is
retained for a ticker, the ratification has nothing to attach to, and element 3 is not thereby resolved
for that ticker either. This distinction is applied explicitly below:

- For the 11 tickers with a retained, exact-head-anchored independent review (Batches 1-2, PR #189's
  five) followed by a same-account, no-intervening-commit merge, **§1's ratification supplies element 3**
  — elements 1, 2, 4, and 5 are independently mapped on their own evidence, per `OPS-0010`'s own
  instruction that the ratification "does not establish that elements 1, 2, 4, or 5 were satisfied for
  any record."
- For the 7 tickers with **no retained independent review of any kind**, the ratification's own
  precondition is unmet — element 3 is recorded `INDETERMINATE` for these, not `SATISFIED`, pending the
  fresh CVX-style review `OPS-0010` §3.A requires. This is a deliberately more conservative reading than
  simply asserting the ratification covers "everything merged before the cutoff" — it tracks what §1
  actually says the ratification is conditioned on.

## 6. Thirteen independent legacy-ticker sections

### 6.1 — 6.4 Batch 1: ASML, AMAT, KLAC, LRCX (`PI-0023`)

All four share one implementation PR and one review/correction/post-merge-verification chain; no
finding below distinguishes among the four tickers individually because none of the retained evidence
does either.

- **Record identity**: `intelligence/companies/{ASML,AMAT,KLAC,LRCX}.{yaml,md}` — 8 files, all present,
  `intelligence_validator.py` confirms all 4 valid within the current 45/45 run.
- **Original authority**: `governance/decisions/PI-0023-ws0005-milestone3-batch1-semis-equipment.md`
  (`status: Accepted`, 2026-07-25).
- **Implementation PR**: **#154**, merge commit `7f50020e83c6bf3fcf50c2f26a1a0533aaa245af`, parents
  `316dc32da2c42df4759dfae4da1e1741906f7657` (base, `PI-0023`'s own merge commit) and
  `0425f3a30232e06ea97aabec95c07ccc93fcc0e9` (reviewed/corrected head) — **confirmed direct second
  parent** via `git log --format="%H %P" 7f50020e -1`.
- **Review evidence (retained)**: two GitHub reviews on PR #154, independently retrieved via
  `pull_request_read`:
  - Review `4779913553` (`COMMENTED`, anchored to intermediate head `cb5d4e4829653e0e31a255a7f8e9442545cce4e8`) — verdict **"PR #154 CHANGES REQUIRED"**, two blocking findings (B1: unsupported/fabricated attributions in the comparison artifact; B2: stale KLAC gap language), both confined to `intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` — the four company records themselves were not implicated.
  - Review `4780012239` (`COMMENTED`, anchored to `0425f3a30232e06ea97aabec95c07ccc93fcc0e9` — the exact merged head) — verdict **"PR #154 APPROVED WITH NON-BLOCKING FINDINGS"**, confirming B1/B2 resolved, five non-blocking findings remaining (N1-N5), none blocking.
- **Correction history**: one bounded correction commit (`0425f3a3`) resolved both B1 and B2, followed
  by the exact-head delta review above — a complete, retained correction-and-re-review cycle.
- **Merge ancestry**: confirmed direct (above); `git merge-base --is-ancestor 0425f3a3 origin/main` →
  yes.
- **Post-merge verification**: two further, separately merged, separately reviewed reconciliation PRs —
  **PR #155** (merge commit `549e77c0d48d8b55e5b1c0474a375a9d72732c60`) independently re-ran
  `intelligence_validator.py` (11/11 valid), `freshness_validator.py` (OK), full pytest (1502/1502),
  `git diff --check` (clean), and re-confirmed exact-head CI (`30171261993`, success) and protected-path
  zero-touch — itself reviewed by GitHub review `4780123504` (`COMMENTED`, anchored to the exact merged
  head `cdcedb6732cae9b0dabd650ce065f7f0576175e1`), verdict **"PR #155 APPROVED WITH NON-BLOCKING
  FINDINGS."** **PR #156** (merge commit head `6c193823bc57754e42e364ee5ad5edec3ca8baae`) corrected the
  one wording defect PR #155's review flagged, itself reviewed by GitHub review `4780162401`, verdict
  **"PR #156 APPROVED FOR READINESS AND MERGE,"** zero findings.
- **Current freshness state**: `intelligence/freshness_registry.yaml` — all four `monitoring_enabled:
  false`, `checkpoint_status: pending`, `company_record_authority: PI-0023`.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **SATISFIED** | Review `4780012239`, retained, anchored to the exact merged head `0425f3a3`, independent (author identity distinct session per its own disclosure), capability-consistent with `OPS-0007` §1 in substance (Fable, exact-head-anchored, severity-classified, retained). |
| 2. Correction + exact-head re-review where required | **SATISFIED** | Two blocking findings from the full review resolved by commit `0425f3a3`, confirmed by the exact-head delta review above. |
| 3. Principal acceptance at exact final head | **SATISFIED (via `OPS-0010` §1 ratification)** | Merge `7f50020e` parents are base + `0425f3a3` (the reviewed head) with no intervening commit; same-account merge; ratification precondition (an eligible independent exact-head review exists) is met. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED** | Direct-parent ancestry confirmed above. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **SATISFIED** | PR #155/#156, each independently reviewed and merged, performed and recorded exactly this verification; `operations/WORKSTREAMS.yaml` lines ~606-664 record it. |

- **Findings**: none (BLOCKER/MATERIAL/MINOR/NOTE) — all findings from the original review cycle were
  resolved and independently re-confirmed.
- **Retrospective conclusion**: **ELIGIBLE FOR PROVISIONAL AFTER THIS PR COMPLETES ITS LIFECYCLE** (all
  four tickers).
- **Exact smallest missing action**: none beyond this implementation PR's own required
  review/correction/acceptance/merge/post-merge-verification lifecycle (§9 below) — no ticker-specific
  gap remains.

### 6.5 — 6.6 Batch 2: MU, SKHY (`PI-0024`)

- **Record identity**: `intelligence/companies/{MU,SKHY}.{yaml,md}`, both present and valid.
- **Original authority**: `governance/decisions/PI-0024-ws0005-milestone3-batch2-memory.md` (`status:
  Accepted`, 2026-07-25).
- **Implementation PR**: **#158**, merge commit `6740f9eca95303e97368f3d010bf99fba1cb404b`, parents
  `883c8e859616e631617adcf973fc6a6ba93eca44` (base) and `957a223278e154a9bdd20033911cec79f0696c37`
  (reviewed/corrected head) — confirmed direct second parent.
- **Review evidence (retained)**: one GitHub review, `4780782073` (`COMMENTED` — GitHub blocks
  same-account `APPROVE`), anchored to the exact merged head `957a223278e154a9bdd20033911cec79f0696c37`,
  verdict **"APPROVED FOR READINESS AND MERGE."** This review's own body describes an *earlier* review
  (anchored to intermediate head `78d5045`, two Minor findings: MU 10-K citation mislabeling; SKHY
  ADR-premium/conversion staleness) that is **not independently retrievable as its own GitHub review
  object** — PR #158 carries exactly one review artifact. The final, retained review directly
  re-examined and confirmed the correction that resolved both Minor findings.
- **Correction history**: correction commit `957a223278e154a9bdd20033911cec79f0696c37` (touching
  exactly `MU.yaml`, `SKHY.yaml`, `SKHY.md`) resolved the two Minor findings; confirmed by the retained
  exact-head review.
- **Merge ancestry**: confirmed direct (above); `git merge-base --is-ancestor 957a223... origin/main` →
  yes.
- **Post-merge verification**: **PR #159** (merge commit `7c11d90fc8e68670f814ac35d32de693ab166a21`)
  independently re-ran `intelligence_validator.py` (13/13 valid + 2/2 themes), `freshness_validator.py`
  (OK), full pytest (1502/1502), `git diff --check` (clean), decision-index reconciliation (33=33),
  protected-path zero-touch, and re-confirmed exact-head CI (`30184811368`, success) — itself reviewed
  by GitHub review `4780798383`, verdict **"APPROVED FOR READINESS AND MERGE."**
- **Current freshness state**: both `monitoring_enabled: false`, `checkpoint_status: pending`,
  `company_record_authority: PI-0024`.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **SATISFIED** | Review `4780782073`, retained, anchored to the exact merged head. |
| 2. Correction + exact-head re-review where required | **SATISFIED** | Both Minor findings resolved by `957a223`, confirmed at the exact-head review above. |
| 3. Principal acceptance at exact final head | **SATISFIED (via `OPS-0010` §1 ratification)** | Merge parents = base + `957a223` (reviewed head), no intervening commit; ratification precondition met. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED** | Direct-parent ancestry confirmed. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **SATISFIED** | PR #159, independently reviewed and merged, performed and recorded exactly this verification. |

- **Findings**: **MINOR** — the pre-correction review that first identified the two Minor findings is
  described only in the final review's own narrative body, not independently retrievable as its own
  GitHub review object. This does not affect the determination above: the retained, exact-head review
  independently re-examined the corrected content directly, and the findings it originally responded to
  were Minor, not Blocking/Major, so `OPS-0007` §1.11's mandatory-correction trigger would not itself
  have required this cycle — it occurred anyway, as a matter of care.
- **Retrospective conclusion**: **ELIGIBLE FOR PROVISIONAL AFTER THIS PR COMPLETES ITS LIFECYCLE** (both
  tickers).
- **Exact smallest missing action**: none beyond this implementation PR's own lifecycle.

### 6.7 COST (`PI-0003` / `decision_log.yaml`; later `TGT-0002`, `PI-0021`, `PI-0022`)

- **Record identity**: `intelligence/companies/COST.{yaml,md}`, present, valid, `portfolio_role_ref: T1`,
  `conviction.rating: High`.
- **Authority chain**: `decision_log.yaml` PI-0003 (2026-07-17, original pilot authorization) → PR #71
  (creation) → `governance/decisions/TGT-0002-cost-promotion-t2-to-t1.md` (2026-07-20, tier promotion —
  targets `targets.yaml` only, explicitly not the Intelligence record's own review lifecycle) → PR #113
  (subordinate `portfolio_role_ref` sync) → `governance/decisions/PI-0021-cost-committee-review-authorization.md`
  (2026-07-23, research authorization) → `governance/decisions/PI-0022-cost-intelligence-refresh-authorization.md`
  (2026-07-23, refresh authorization) → PR #135 (refresh implementation).
- **Implementation PRs / merge commits**: #71 (`5a1017927d2edae2d1cf3563170289c01e4afab3`, parents
  `4d9fa282...`/`b034bc8e...`, direct second parent confirmed); #113
  (`e6d0dea9eb63207a4af2ec0f1362682c8814d6e4`, parents `277367a7...`/`1c84ea7481...`, direct); #135
  (`c72386b1bea92d96eaeb90d5499ff88792e7d191`, parents `29f09e78...`/`c1bea00c39...`, direct). All
  confirmed ancestors of `origin/main`.
- **Review evidence**: `pull_request_read` (`get_reviews`, `get_comments`) on all three PRs returns
  **zero reviews and zero comments on each**. No `governance/audits/*.md` artifact reviews COST's
  content (the only three artifacts mentioning "COST" are the 2026-07-25 Milestones-1/2 inventory audit —
  a schema/freshness consistency check, not a content review — and two CVX-era artifacts that cite COST
  only as unrelated context). Each PR's commit message self-reports internal test counts (not
  independently re-verified by a separate session). **PR #135's own body explicitly states it "requires
  an independent SHA-pinned review... and must not be merged without the principal's separate explicit
  merge authorization,"** yet merged 17 minutes after opening with zero retained GitHub review or
  comment activity.
- **Correction history**: none found — no follow-up correction commit or PR comment on any of the three
  PRs.
- **Post-merge verification**: none found specific to COST's own record content at any point after any
  of the three merges. `operations/WORKSTREAMS.yaml`'s 2026-07-29 entry (lines 2776-2783) explicitly
  places COST in the 18-record "not yet confirmed" bucket, stating these 13 legacy tickers "have not been
  individually re-evaluated against `OPS-0007` §3's specific five-element test by this entry or any other
  retained entry."
- **Element-by-element `OPS-0007` §3 mapping** (applies across all three merges; no stage improves on
  this):

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained GitHub reviews/comments on PR #71, #113, or #135; no `governance/audits/` artifact substitutes; `OPS-0007` §1.9's "prose authored by the same identity as the reviewed work does not satisfy this requirement" applies directly. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | No review occurred to have surfaced a finding to correct; cannot be assessed absent element 1. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | `OPS-0010` §1's ratification is conditioned on an eligible independent review existing; none is retained, so the ratification does not resolve this element for COST. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED (ancestry only)** | Direct-parent merge ancestry confirmed for all three PRs — a mechanical git fact, independent of whether a review occurred. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | No evidence found; `operations/WORKSTREAMS.yaml` itself states this explicitly. |

- **Findings**: **MATERIAL** — no retained independent review exists for any of COST's three lifecycle
  events (creation, tier-sync, refresh); this is an evidence-retention gap, not a finding against the
  underlying research content, which this audit did not and is not authorized to re-assess.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: a fresh, CVX-style independent retrospective review (per the
  `PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md` method) of the current, merged
  `intelligence/companies/COST.yaml` and `intelligence/companies/COST.md`, performed by an eligible
  reviewer under `OPS-0007` §1 who did not author any of PR #71/#113/#135, before a PROVISIONAL
  conclusion may be reached.

### 6.8 XOM (`PI-0005` / `decision_log.yaml`)

- **Record identity**: `intelligence/companies/XOM.{yaml,md}`, present, valid, `portfolio_role_ref:
  band`, `conviction.rating: Medium`.
- **Authority**: `decision_log.yaml` PI-0005 (2026-07-17). No later refresh or committee-review
  authorization exists for XOM (searched exhaustively; none found).
- **Implementation PR**: **#82**, merge commit `cb603b90d9c3cdf3cdfa67b00b95ae5808857605`, **single
  parent** `ef11c1017594...` — a **squash merge**, not a two-parent merge; there is no separate
  "reviewed head" commit preserved as a distinct ancestor. Confirmed ancestor of `origin/main`.
- **Review evidence**: `pull_request_read` on PR #82 returns **zero reviews and zero comments**. No
  `governance/audits/*.md` artifact reviews XOM's content (the two CVX-era artifacts cite XOM only as
  unmodified comparator context for the `oil` cluster cap, never as a review of XOM's own record).
- **Correction history**: none found.
- **Post-merge verification**: none found specific to XOM at any point; `operations/WORKSTREAMS.yaml`
  places XOM in the 18-record "not yet confirmed" bucket, identically to COST.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained reviews/comments; no substituting audit artifact. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | No review occurred to surface a finding. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | Ratification precondition unmet. |
| 4. Merged to `main` at exact reviewed head | **INDETERMINATE** | The squash merge has no separate "reviewed head" parent to check against — the concept does not map cleanly onto this merge's structure, distinct from a simple pass/fail ancestry check. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | No evidence found. |

- **Findings**: **MATERIAL** — no retained independent review exists for XOM's sole lifecycle event.
  **NOTE** — PR #82 was merged via a single-parent squash commit, structurally different from the
  two-parent merge pattern most later WS-0005 PRs use; a future retrospective review should treat "the
  merged squash commit itself" as the unit under review rather than searching for a separate reviewed-head
  parent that does not exist.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: a fresh, CVX-style independent retrospective review of the current,
  merged `intelligence/companies/XOM.yaml` and `intelligence/companies/XOM.md`, performed by an eligible
  reviewer who did not author PR #82.

### 6.9 NVDA (`PI-0007` original; `PI-0017`/`PI-0018` refresh)

- **Record identity**: `intelligence/companies/NVDA.{yaml,md}`, present, valid, `conviction.rating: High`.
- **Stage A — original creation**: `decision_log.yaml` PI-0007 (2026-07-17, joint with GEV) → **PR #78**,
  merge commit `6794714a9df42114e15bee3b2a6bcd5cb12a4886`, parents `98dd915a...` (base) and
  `1add3a21fb19ab0da15528caa45c4d8ed8b6ba26` (feature head) — confirmed direct second parent, true
  two-parent merge. `pull_request_read` on PR #78 returns **zero reviews and zero comments**. No audit
  artifact. Commit self-reports test counts only.
- **Stage B — refresh**: `governance/decisions/PI-0017-nvda-committee-review-authorization.md` (research
  authorization) → `governance/decisions/PI-0018-nvda-intelligence-refresh-authorization.md` (refresh
  authorization) → **PR #126**, merge commit `5f1aa2b172f5457433e7987620c10e4f6f830a60`, **single
  parent** `ff6606fb812792f1d284d0eaa19c2eb2ad98466c` — a **squash merge**; the commit message's claim of
  "two rounds of independent PR review" cannot be checked against a preserved reviewed-head ancestor,
  because the intermediate commits were squashed away. `pull_request_read` on PR #126 returns **zero
  reviews and zero comments**. `PI-0018`'s own text describes review evidence as principal-supplied,
  SHA256-pinned external artifacts (not committed to this repository, not retained under
  `governance/audits/`) — reviewing the underlying *research packet*, not this implementation PR itself
  as a retained, independently attributable GitHub or repository artifact.
- **Correction history**: none found for Stage A. Stage B's commit message claims a two-round correction
  history, but the underlying commits are not individually inspectable post-squash, and no external
  review artifact is retained in-repo to confirm what was corrected.
- **Post-merge verification**: none found for either stage. The 2026-07-25 Milestones-1/2 inventory audit
  confirms NVDA's record *state* (current, not overdue) but performs no merge-ancestry/scope/validator/test
  re-verification of either PR #78 or PR #126.
- **Element-by-element `OPS-0007` §3 mapping** (both stages considered together; neither individually
  clears the standard):

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained reviews/comments on either PR; Stage B's external audit artifacts are not repository-retained, GitHub-attributable evidence. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | Stage B's correction claim cannot be independently verified against a preserved reviewed head. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | Ratification precondition unmet. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED for Stage A (ancestry only) / INDETERMINATE for Stage B** | Stage A is a true, direct-parent merge; Stage B is a squash merge with no separate reviewed-head parent to check. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | No evidence found for either stage. |

- **Findings**: **MATERIAL** — no retained independent review exists for either NVDA lifecycle stage.
  **NOTE** — the refresh stage's externally-supplied audit artifacts, while methodologically described
  in `PI-0018`'s own text, are not retained in-repo per the `governance/audits/` convention `OPS-0004`
  established; a future fresh review should determine whether those artifacts can be supplied again and
  retained, or whether the fresh review must independently re-derive the same conclusions.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: a fresh, CVX-style independent retrospective review of the current,
  merged `intelligence/companies/NVDA.yaml` and `intelligence/companies/NVDA.md`, performed by an
  eligible reviewer who did not author PR #78 or PR #126.

### 6.10 GEV (`PI-0007` original; `PI-0019`/`PI-0020` refresh)

- **Record identity**: `intelligence/companies/GEV.{yaml,md}`, present, valid, `conviction.rating:
  Medium`.
- **Stage A — original creation**: identical to NVDA's — PR #78, same merge commit `6794714a9d`, same
  ancestry, same absence of review evidence.
- **Stage B — refresh**: `governance/decisions/PI-0019-gev-committee-review-authorization.md` →
  `governance/decisions/PI-0020-gev-intelligence-refresh-authorization.md` → **PR #132**, merge commit
  `d4f8941a1684fa5f8e742f4e89e68bd8a80c4f1f`, parents `e627eb57...` (base) and
  `3246fe0f317c5377ad1c15f17d559d000f03811d` (feature head) — **true, direct two-parent merge**, feature
  branch preserving a real 3-commit correction history (`bb31f46` → `fee8313` "Corrective pass" →
  `3246fe0` "Second corrective pass"). `pull_request_read` on PR #132 returns **zero reviews and zero
  comments**. `PI-0020`'s own Context section states explicitly: **"This session then performed the
  packet's final independent acceptance audit itself, from first principles, in this same session — not
  relying on any prior session's verdict"** — a same-session self-audit, which does not satisfy
  `OPS-0007` §1.1's independence-from-authorship requirement even in substance, regardless of its
  thoroughness.
- **Correction history**: real and preserved (unlike NVDA's squashed Stage B) — two corrective-pass
  commits on the feature branch, addressing an orders mislabel, a restored risk date, EBITDA
  verification, an unresolved Wind EBITDA claim, and date/history consolidation.
- **Post-merge verification**: none found for either stage.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained GitHub reviews/comments on either PR; Stage B's "independent" audit was performed by the same authoring session, which does not satisfy independence-from-authorship. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | A real correction history exists for Stage B, but it responds to the same session's own self-audit, not an independent reviewer's finding, so it does not close element 2 in the `OPS-0007` sense. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | Ratification precondition unmet. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED (ancestry only)** | Both stages are true, direct-parent merges. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | No evidence found for either stage. |

- **Findings**: **MATERIAL** — no retained independent (session-distinct) review exists for either GEV
  lifecycle stage; the refresh's self-audit, however thorough, does not substitute for an independent
  reviewer.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: a fresh, CVX-style independent retrospective review of the current,
  merged `intelligence/companies/GEV.yaml` and `intelligence/companies/GEV.md`, performed by an eligible
  reviewer who did not author PR #78 or PR #132.

### 6.11 ISRG (`PI-0009` original; unauthorized refresh)

- **Record identity**: `intelligence/companies/ISRG.{yaml,md}`, present, valid, `conviction.rating:
  High`.
- **Stage A — original creation**: `decision_log.yaml` PI-0009 (2026-07-18, joint with TMO) → **PR #80**,
  merge commit `16f7817b5f135c9a13c564647e1154f20fb86ee8`, **single parent** `205bb3c81d69b565791d61ec37c6fa82b32b94ed`
  — a **squash merge**. `pull_request_read` on PR #80 returns **zero reviews and zero comments**. No audit
  artifact.
- **Stage B — refresh (PR #110)**: **No governing `PI-####` decision was found for this refresh** —
  searched `governance/decisions/` and `decision_log.yaml` exhaustively for "ISRG"; none exists beyond
  `PI-0009` itself. This is a distinct, additional finding from the review-evidence gap common to the
  other legacy tickers: **ISRG's refresh appears to have proceeded without a governing research or refresh
  authorization decision at all**, unlike NVDA (`PI-0017`/`PI-0018`), GEV (`PI-0019`/`PI-0020`), and COST
  (`PI-0021`/`PI-0022`), each of which has one. Merge commit `19042313909266be5f92f939cfa0bbc2dbca55f9`,
  parents `702823c4...` (base) and `d1112344f9b365898c61b08fa806a718e0060d86` (feature head) — true,
  direct two-parent merge, feature branch preserving a real two-round self-correction history: `32a9469`
  (refresh) → `8c7755e` ("Correct ISRG review characterization... No PI-0009 scheduled-cadence review
  occurred") → `d1112344` (fixing a false "directly rendered" claim about two sources that had actually
  returned HTTP 403). Commit `8c7755e`'s own message is explicit that no scheduled or authorized review
  process governed this refresh. `pull_request_read` on PR #110 returns **zero reviews and zero
  comments**. `intelligence/freshness_registry.yaml`'s `company_record_authority` field for ISRG still
  cites only `PI-0009` — it has never been updated to reflect the PR #110 refresh, consistent with this
  gap.
- **Post-merge verification**: none found for either stage.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained reviews/comments on either PR; Stage B's corrections are self-caught, not independently found. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | Real self-correction history exists for Stage B but responds to no independent finding. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | Ratification precondition unmet; additionally, no governing decision exists for Stage B against which "acceptance" would even be measured. |
| 4. Merged to `main` at exact reviewed head | **INDETERMINATE for Stage A (squash, no separate reviewed head) / SATISFIED (ancestry only) for Stage B** | As stated. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | No evidence found for either stage. |

- **Findings**: **MATERIAL** — no retained independent review exists for either ISRG lifecycle stage.
  **MATERIAL (additional, distinct)** — the PR #110 refresh has no identifiable governing `PI-####`
  authorization anywhere in `governance/decisions/` or `decision_log.yaml`, unlike every other refresh
  examined in this audit; this is a governance-authorization gap, not merely a review-retention gap, and
  is disclosed here rather than resolved — this audit is not authorized to retroactively author or infer
  an authorization for already-merged content, and does not attempt to.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: (a) a fresh, CVX-style independent retrospective review of the
  current, merged `intelligence/companies/ISRG.yaml` and `intelligence/companies/ISRG.md`, performed by
  an eligible reviewer who did not author PR #80 or PR #110; and (b) separately, a principal/governance
  decision on whether the PR #110 refresh's missing authorization requires its own retroactive
  governance filing (analogous to `OPS-0004`'s treatment of PR #143's unretained review claim) — this
  audit discloses the gap and recommends that a future session raise it, but does not itself propose or
  perform that filing.

### 6.12 TMO (`PI-0009`)

- **Record identity**: `intelligence/companies/TMO.{yaml,md}`, present, valid, `conviction.rating:
  Medium`. No refresh has ever occurred — single lifecycle stage only.
- **Authority**: `decision_log.yaml` PI-0009 (2026-07-18, joint with ISRG) → **PR #80** (same merge as
  ISRG's Stage A: commit `16f7817b5f135c9a13c564647e1154f20fb86ee8`, single-parent squash merge, base
  `205bb3c81d69b565791d61ec37c6fa82b32b94ed`).
- **Review evidence**: identical to ISRG Stage A — `pull_request_read` on PR #80 returns **zero reviews
  and zero comments**. No audit artifact. The 2026-07-25 Milestones-1/2 inventory audit
  (`governance/audits/WS0005_MILESTONES1-2_PORTFOLIO_INVENTORY_AUDIT_20260725.md`) separately flags TMO
  as having the thinnest sourcing of the seven companies covered at that time ("1 source" versus 4-15 for
  others) — a disclosed, pre-existing sourcing-depth observation, not itself a lifecycle-review finding,
  and one this audit does not re-litigate or expand on (no new research is authorized).
- **Correction history**: none found.
- **Post-merge verification**: none found.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained reviews/comments; no substituting artifact. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | No review occurred. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | Ratification precondition unmet. |
| 4. Merged to `main` at exact reviewed head | **INDETERMINATE** | Squash merge, no separate reviewed-head parent. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | No evidence found. |

- **Findings**: **MATERIAL** — no retained independent review exists. **NOTE** — pre-existing,
  previously-disclosed thin sourcing (1 source), carried forward from the 2026-07-25 inventory audit, not
  independently re-assessed by this filing.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: a fresh, CVX-style independent retrospective review of the current,
  merged `intelligence/companies/TMO.yaml` and `intelligence/companies/TMO.md`, performed by an eligible
  reviewer who did not author PR #80 — which should also independently assess whether the previously
  disclosed thin sourcing needs to be addressed as part of, or separately from, the review itself.

### 6.13 TSM (`PI-0012`; closure `PI-0013`)

- **Record identity**: `intelligence/companies/TSM.{yaml,md}`, present, valid, `conviction.rating: High`.
  Single lifecycle stage — no refresh has occurred.
- **Authority**: `governance/decisions/PI-0012-ai-compute-committee-review-pilot.md` (research
  authorization) → **PR #97**, merge commit `b10f9250af6cace13dea1c648e594ee866d15c0a`, parents
  `e7012131...` (base) and `07f53fb374823edd36e45f4e3ca49478d2238c2d` (feature head, single commit) —
  true, direct two-parent merge → `governance/decisions/PI-0013-tsm-pilot-review-closure.md` (pilot
  closure, applying `PI-0004`'s five-part "pilot reviewed" test).
- **Review evidence**: `pull_request_read` on PR #97 returns **zero reviews and zero comments**. No
  `governance/audits/*.md` artifact exists. `PI-0013`'s own text is explicit about what its verification
  actually was: **"a same-session, read-only architectural retrospective"** — performed by the same
  session that filed the `PI-0013` closure decision, not a separately identified independent reviewer,
  and producing no retained `governance/audits/` artifact (`supporting_artifact: null`).
- **Correction history**: one factual error (an INTC-related mischaracterization) was caught and fixed
  before merge via a manual internal correction pass described in PR #97's own body — not a
  post-merge, independently-triggered correction-and-re-review cycle.
- **Post-merge verification**: **the strongest partial evidence found among the seven held-back
  tickers** — `PI-0013`'s own text quotes direct re-execution results performed by the closing session:
  `intelligence_validator.validate_company_file(...)` → `valid: True, errors: []`; `python3 -m pytest -q`
  → `498 passed`. This is real, independently-re-run validator/test evidence — but (a) performed by the
  same session that authored the `PI-0013` closure decision, not a separately identified reviewer, (b)
  did not check merge ancestry or diff scope explicitly, and (c) was never recorded in
  `operations/WORKSTREAMS.yaml` (which did not exist until `OPS-0001`, 2026-07-24 — five days after TSM
  merged on 2026-07-19), so the "register synchronized" component of element 5 was never satisfied.
- **Element-by-element `OPS-0007` §3 mapping**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **NOT SATISFIED** | Zero retained GitHub reviews/comments; `PI-0013`'s own "same-session" retrospective does not satisfy independence-from-authorship. |
| 2. Correction + exact-head re-review where required | **INDETERMINATE** | The one correction found was pre-merge and internal, not a response to an independent post-review finding. |
| 3. Principal acceptance at exact final head | **INDETERMINATE** | Ratification precondition unmet. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED (ancestry only)** | True, direct-parent merge, independently confirmed by `PI-0013` itself. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **NOT SATISFIED** | Validator/test re-run occurred (same session) but ancestry/scope were not explicitly checked and `operations/WORKSTREAMS.yaml` was never synchronized to it — the register-synchronization component of element 5 is unmet regardless of the partial validator/test evidence. |

- **Findings**: **MATERIAL** — no retained independent review exists; the same-session validator/pytest
  re-run, while a genuine and disclosed positive fact, does not itself satisfy element 1 or fully satisfy
  element 5.
- **Retrospective conclusion**: **HELD BACK — FRESH RETROSPECTIVE REVIEW REQUIRED.**
- **Exact smallest missing action**: a fresh, CVX-style independent retrospective review of the current,
  merged `intelligence/companies/TSM.yaml` and `intelligence/companies/TSM.md`, performed by an eligible
  reviewer who did not author PR #97 or `PI-0013` — which may reuse `PI-0013`'s own quoted validator/test
  re-run results as a starting point (subject to independent re-confirmation) rather than repeating that
  step from zero.

## 7. PR #189 five-record lifecycle closure — CEG, BRK.B, WMT, MLM, AAPL (`PI-0032`)

This section addresses exactly these five, independently mapped, per `OPS-0010` §3.B — reusing the
already-retained PR #189 review, correction, delta-review, merge, and post-merge-verification evidence
without re-performing that work, and applying `OPS-0010` §1's ratification to element 3 only, exactly as
it was applied to the 13 legacy records above.

**Shared facts** (identical evidentiary basis for all five, since all five merged in one PR under one
review cycle):

- **Record identity**: `intelligence/companies/{CEG,BRK.B,WMT,MLM,AAPL}.{yaml,md}` — 10 files, all
  present, all valid within the current 45/45 run. (`BRK.B` confirmed as the first dotted-ticker filename
  in this repository, matching `targets.yaml`'s own brokerage-convention symbol.)
- **Governing authority**: `governance/decisions/PI-0032-ws0005-milestone3-remaining-governed-holdings-and-sandisk-candidate.md`
  (`status: Accepted`, merged via PR #185, merge commit `25af2afb10ccf947119935173468f9f13b8159e3`) —
  confirmed to authorize exactly these five as independent research units (plus WDC and the Sandisk
  candidate comparison, addressed elsewhere, not by this filing). `governance/decisions/PI-0033-ws0005-milestone3-residual-deferrals.md`,
  filed in the same PR #185, confirmed **not** to touch any of these five — it dispositions fourteen
  unrelated tickers and restates three unrelated deferrals.
- **Distinct PRs confirmed**: **PR #188** (WDC + bounded Sandisk comparison only, merge commit
  `1cbda24bacc803a08433ecf59a88eae68ab441fa`) and **PR #189** (CEG/BRK.B/WMT/MLM/AAPL only, base
  `1cbda24bacc803a08433ecf59a88eae68ab441fa`, 13 files: 5 YAML+MD pairs,
  `intelligence/freshness_registry.yaml`, `intelligence/freshness_checkpoints.yaml`,
  `operations/WORKSTREAMS.yaml`) — independently verified via `pull_request_read` (`get_files`) as two
  separate PRs with non-overlapping ticker scope.
- **Implementation PR**: **#189**, merge commit `4f024f2c97797b34b94df826fa5fb9e1e828dec8`, parents
  `1cbda24bacc803a08433ecf59a88eae68ab441fa` (base, PR #188's merge commit) and
  `ad72b7f7bc99d2e274d89e9a0f887f9e5e7b9ad9` (the corrected, reviewed head) — confirmed direct second
  parent via `git log --format="%H %P" 4f024f2c -1`.
- **Review evidence (retained)**: two PR comments (GitHub blocks same-account formal `APPROVE` review
  objects on this single-account repository — the same substitute pattern used throughout this era, per
  `OPS-0007` §1's own accommodation):
  - `issuecomment-5109989510` (2026-07-28T21:41:59Z, anchored to head `2098584d0e1c5ce5005f180bf863b5d179a74528`)
    — independently re-verified evidence-bundle/validator/test state (45/45 valid, 1502/1502 tests,
    protected paths empty); found **one MATERIAL finding**: `operations/WORKSTREAMS.yaml`'s own commit in
    this PR had wrongly claimed PR #188 "carries zero GitHub reviews... merged without a recorded
    independent review," when PR #188 in fact carries a retained review comment
    (`issuecomment-5109593960`, verdict "PR #188 EXACT-HEAD APPROVED"). Also found 2 MINOR (thin
    margin-relevance framing for BRK.B/AAPL) and 2 NOTE items. **This MATERIAL finding concerned the
    register's own factual claim about PR #188/WDC — not the substantive content of CEG's, BRK.B's,
    WMT's, MLM's, or AAPL's own Company Intelligence records**, which the review did not find deficient.
    Verdict: **"PR #189 CHANGES REQUIRED."**
  - Correction commit `ad72b7f7bc99d2e274d89e9a0f887f9e5e7b9ad9` — touches exactly
    `operations/WORKSTREAMS.yaml`, fixing precisely the mischaracterized PR #188 claim; no ticker
    content file touched.
  - `issuecomment-5111148711` (2026-07-29T00:11:01Z, delta review of the correction) — confirmed the fix,
    no new findings, same 13-file scope, protected paths still empty. Verdict: **"PR #189 CORRECTED
    EXACT-HEAD APPROVED."**
- **Merge ancestry**: confirmed direct above; `git merge-base --is-ancestor ad72b7f7... origin/main` →
  yes.
- **Post-merge verification**: the separate 2026-07-29 `operations/WORKSTREAMS.yaml` reconciliation
  entry (lines 2646-2794, performed by a session distinct from PR #189's authoring session) independently
  re-ran, against current `origin/main`: `intelligence_validator.py` (45/45 valid, including all five of
  these tickers), `freshness_validator.py` (OK), full pytest (1502/1502), decision-index reconciliation
  (45=45 at that point), and a protected-path diff from PR #188's base to current `origin/main` (empty).
  This is the same re-verification basis the same entry used to reach WDC's own PROVISIONAL
  determination — it was performed generically across "all six of `PI-0032`'s governed-holding units,"
  which necessarily includes CEG/BRK.B/WMT/MLM/AAPL, even though that entry's own explicit conclusion
  stopped short of stating a PROVISIONAL determination for these five (the exact gap `OPS-0010` §3.B
  authorizes this section to close).
- **Current freshness state**: all five present in `intelligence/freshness_registry.yaml` and
  `intelligence/freshness_checkpoints.yaml`, `checkpoint_status: pending`, `monitoring_enabled: false`,
  `company_record_authority`/`enrollment_authority: PI-0032`, `enrolled_at: "2026-07-28"` — identical
  shape to WDC's own rows.

**Element-by-element `OPS-0007` §3 mapping (applies identically to CEG, BRK.B, WMT, MLM, and AAPL)**:

| Element | Determination | Basis |
|---|---|---|
| 1. Eligible independent exact-head review | **SATISFIED** | `issuecomment-5111148711`, retained, anchored to the exact merged head `ad72b7f7`, independent, severity-classified. |
| 2. Correction + exact-head re-review where required | **SATISFIED** | The one MATERIAL finding (a register-accuracy issue, not a finding against any of the five companies' own content) was corrected and re-confirmed at the exact head that merged. |
| 3. Principal acceptance at exact final head | **SATISFIED (via `OPS-0010` §1 ratification)** | Merge `4f024f2c` parents = base + `ad72b7f7` (the reviewed/corrected head), no intervening commit; same-account merge; ratification precondition met. |
| 4. Merged to `main` at exact reviewed head | **SATISFIED** | Direct-parent ancestry confirmed. |
| 5. Post-merge ancestry/scope/validator/test re-verification, register synchronized | **SATISFIED** | The 2026-07-29 reconciliation entry performed and recorded exactly this verification against current `origin/main`, covering all five tickers. |

**Findings**: **NOTE** — the one MATERIAL finding PR #189's review surfaced concerned a claim about a
*different* PR (#188/WDC), not these five companies' own content; recorded here explicitly so a future
reader does not mistake "PR #189 had a MATERIAL finding" for a defect in CEG/BRK.B/WMT/MLM/AAPL's own
research. **NOTE** — `operations/WORKSTREAMS.yaml`'s own 2026-07-29 entry explicitly acknowledged, in its
own words, that it performed the WDC determination but left CEG/BRK.B/WMT/MLM/AAPL's equivalent
determination unrecorded — this is exactly the closure `OPS-0010` §3.B and this section perform.

**Retrospective conclusion (each of the five, independently confirmed to share identical evidentiary
basis)**: **ELIGIBLE FOR PROVISIONAL AFTER THIS PR COMPLETES ITS LIFECYCLE.**

**Exact smallest missing action**: none beyond this implementation PR's own required
review/correction/acceptance/merge/post-merge-verification lifecycle (§9 below) — no ticker-specific gap
remains for any of the five.

## 8. Complete criterion-7 partition

Programmatically re-derived this session directly from `intelligence/companies/*.yaml` (45 files) and
cross-checked against `operations/WORKSTREAMS.yaml`'s own existing 27/18 partition — identical, no
discrepancy found.

**Set 1 — Confirmed PROVISIONAL, unchanged by this audit (27 records)**: AVGO, AMD, MRVL, INTC (Batch 3);
ETN, VRT, PWR (Batch 4); MSFT, GOOGL, META, AMZN (Batch 5); V, MA, JPM (Batch 6); CVX (retrospective
review, `PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md`); WDC (2026-07-29 reconciliation); LLY,
ABBV, MRK, JNJ, GILD (Batch 7); IBM, NOW, CRM, ORCL, CRWD, PANW (Batch 8). **This audit reopens,
downgrades, or re-audits none of these 27** — per `OPS-0010`'s explicit current-status-protection
boundary and this implementation's own authorized scope.

**Set 2 — Eligible for PROVISIONAL after this PR completes its own lifecycle (11 records)**: ASML, AMAT,
KLAC, LRCX, MU, SKHY (§6.1-6.6 above); CEG, BRK.B, WMT, MLM, AAPL (§7 above).

**Set 3 — Held back, fresh retrospective review required (7 records)**: COST, XOM, NVDA, GEV, ISRG, TMO,
TSM (§6.7-6.13 above).

**Partition validation**: 27 (Set 1) + 11 (Set 2) + 7 (Set 3) = **45**, matching
`intelligence/companies/*.yaml`'s exact file count. Independently verified by direct set comparison
this session: every one of the 45 filenames appears in exactly one of the three sets; no ticker appears
in more than one set; no ticker is omitted; no extraneous ticker appears in any set.

**PI-0033 disposition reconciliation**: the 45 Company Intelligence records above, plus `PI-0033`'s 17
dispositioned names (14 new: CAT, GNRC, NFLX, SHOP, UBER, HOOD, RTX, DELL, PLTR, SPCX, RKLB, TSLA, BABA,
UNH; 3 restated: DHR, SYK, EQIX), independently re-derived this session against `targets.yaml`'s 65
total tiered tickers minus the 3 ETF names (SPY, QQQ, GLD) = **62 non-ETF governed tickers**. **45 + 17 =
62**, exact, zero overlap between the Company Intelligence set and the PI-0033 disposition set, zero
tickers unaccounted for in either.

## 9. Findings by severity (roll-up across §6-7)

**BLOCKER**: none.

**MATERIAL** (7 instances, one per held-back ticker, plus one additional distinct instance for ISRG):

1. COST — no retained independent review for any of three lifecycle events (PR #71, #113, #135).
2. XOM — no retained independent review for its sole lifecycle event (PR #82).
3. NVDA — no retained independent review for either lifecycle stage (PR #78, #126).
4. GEV — no retained independent review for either lifecycle stage (PR #78, #132); the refresh's
   same-session self-audit does not substitute for independence.
5. ISRG — no retained independent review for either lifecycle stage (PR #80, #110).
6. ISRG (additional, distinct) — the PR #110 refresh has no identifiable governing `PI-####`
   authorization anywhere in this repository's governance record.
7. TMO — no retained independent review for its sole lifecycle event (PR #80).
8. TSM — no retained independent review for its sole lifecycle event (PR #97); the same-session
   validator/pytest re-run described in `PI-0013` is genuine but does not substitute for independence,
   and the register-synchronization component of element 5 was never satisfied.

**MINOR**:

1. Batch 2 (MU, SKHY) — the pre-correction review that first identified two Minor findings is described
   only in the final retained review's own narrative body, not independently retrievable as its own
   GitHub review object; does not affect this audit's ELIGIBLE conclusion (see §6.5-6.6).

**NOTE**:

1. PR #189's one MATERIAL finding concerned an inaccurate claim about a different PR (#188/WDC), not
   CEG/BRK.B/WMT/MLM/AAPL's own content (§7).
2. `operations/WORKSTREAMS.yaml` itself already disclosed, in its own words, that it performed WDC's
   determination but left the other five PR #189 tickers' equivalent determination unrecorded — the gap
   this audit's §7 closes.
3. Several legacy-era PRs (XOM's #82; ISRG's and TMO's shared #80; NVDA's refresh #126) were merged via
   GitHub's single-parent squash mechanism, which structurally lacks a separate "reviewed head" parent —
   a future fresh review of these tickers should treat the merged squash commit itself as the reviewed
   unit rather than search for a nonexistent second parent.
4. TMO's previously-disclosed thin sourcing (1 source, per the 2026-07-25 Milestones-1/2 inventory
   audit) is carried forward here as context, not independently re-assessed — no new research is
   authorized by this filing.

## 10. Held-back records

COST, XOM, NVDA, GEV, ISRG, TMO, TSM — see §6.7-6.13 for each ticker's individual evidence, findings, and
exact missing action. **No held-back ticker blocks any other record's conclusion** — the 11 records in
Set 2 (§8) and the 27 records in Set 1 (§8) are unaffected by these seven tickers' unresolved status.

## 11. Exact remaining actions

- **For the 11 Set-2 tickers**: this implementation PR's own review/correction/acceptance/merge/
  post-merge-verification lifecycle (§12) is the only remaining action — no ticker-specific gap remains.
- **For the 7 Set-3 tickers**: a fresh, CVX-style independent retrospective review of each ticker's
  *current* merged `intelligence/companies/<TICKER>.yaml` and `.md`, performed by an eligible reviewer
  under `OPS-0007` §1 who did not author any of that ticker's implementation PRs, following exactly the
  method and retained-artifact convention `PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md`
  established. Per `OPS-0010` §3.A, this future review "may be performed and retained... by the later
  independent reviewer of this PR when explicitly instructed" — this audit does not perform, and this
  authoring session is not eligible to perform, that fresh review itself.
- **For ISRG specifically, additionally**: disclosure (not resolution) of the missing `PI-####`
  authorization for its PR #110 refresh, for a future principal/governance decision to address on its own
  terms.

## 12. Explicit milestone boundaries

- **Milestone 3 remains `in_progress`.** This audit resolves none of `PI-0031` §K's seven completion
  criteria beyond what `operations/WORKSTREAMS.yaml`'s own 2026-07-29 entry already recorded (criteria
  1-4 and 6 already satisfied as of that entry; criterion 7 remains partially unaudited after this
  artifact — 34 of 45 records now individually mapped to Set 1 or Set 2's evidentiary basis, 7 remain in
  Set 3, and even the 11 Set-2 records require this PR's own completed lifecycle before they count as
  criterion-7-satisfied).
- **This audit artifact does not itself complete criterion 7.** Even a fully successful completion of
  this implementation PR's own lifecycle (review, correction if needed, principal acceptance, merge,
  post-merge verification) would leave the 7 Set-3 tickers' fresh reviews as a separate, later, required
  step before criterion 7 is fully satisfied roster-wide.
- **Milestone 4 remains unauthorized.** Nothing in this artifact authorizes, implies, or narrows the
  `OPS-0006` §5 gate.
- **No tier, target, holdings, cluster, cap, allocation, margin parameter, or production-code file is
  touched by this artifact or by this implementation unit.**
- **No new company research is performed or authorized by this artifact.**

## 13. Validation evidence

Run this session, against the verified base commit `59f7ac56fdb1a4c5b3c0e45d6b545ea88a126ec4` (before
this implementation's own edits) and re-confirmed after this implementation's edits (CLAUDE.md, this
artifact, and `operations/WORKSTREAMS.yaml`):

- `intelligence_validator.validate_directory('intelligence/companies')` → **45/45 valid**, zero errors.
- `intelligence_validator.validate_themes_directory('intelligence/themes')` → **2/2 valid**.
- `freshness_validator.py` → **OK**.
- `python3 -m pytest -q` → **1502 passed**, zero failed.
- `governance/decisions.yaml` reconciliation against `governance/decisions/*.md` (excluding `README.md`)
  → **46 filed = 46 indexed**, no orphans, no missing entries (this implementation touches neither file).
- Programmatic 45-record lifecycle partition validation (§8) → 27 + 11 + 7 = 45, exact, no overlap, no
  omission.
- 45 + 17 = 62 governed-roster reconciliation (§8) → exact, no overlap, no omission.
- `git diff --check` on this implementation's own changes → clean.
- Protected-path diff (`targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py`,
  `constitution/`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`,
  `governance/decisions/`, `governance/decisions.yaml`, every `intelligence/companies/*.yaml`/`*.md`
  file, every `freshness_*` file) against this implementation's own diff → **empty** — this implementation
  touches only `governance/audits/WS0005_M3_CRITERION7_RETROSPECTIVE_LIFECYCLE_AUDIT_20260729.md`,
  `operations/WORKSTREAMS.yaml`, and `CLAUDE.md`, exactly the three files `OPS-0010` §6 authorizes.
- Exact changed-file inspection (this implementation's own diff against `origin/main`) → exactly the
  three files named above; no other file touched.

## Verdict

**This is a draft audit artifact, authored by the implementation PR's own author session, not yet
independently reviewed.** It concludes, on currently retained evidence: 11 of the 18 tickers named in
`OPS-0010` §3.A/§3.B (ASML, AMAT, KLAC, LRCX, MU, SKHY, CEG, BRK.B, WMT, MLM, AAPL) are eligible for a
PROVISIONAL determination once this implementation PR itself completes its own independent-review,
correction-if-needed, principal-acceptance, merge, and post-merge-verification lifecycle; 7 (COST, XOM,
NVDA, GEV, ISRG, TMO, TSM) are held back pending a fresh, CVX-style independent retrospective review of
each ticker's current record, per `OPS-0010` §3.A's own explicit contemplation of exactly this outcome.
No ticker is declared PROVISIONAL by this artifact. The 27 tickers already confirmed PROVISIONAL are
untouched. Milestone 3 remains `in_progress`; Milestone 4 remains unauthorized.
