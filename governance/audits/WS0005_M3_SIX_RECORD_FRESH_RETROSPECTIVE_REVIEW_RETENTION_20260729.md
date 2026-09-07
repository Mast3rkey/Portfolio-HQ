# WS-0005 Milestone 3 — Six-Record Fresh-Retrospective-Review Retention (COST, XOM, NVDA, GEV, TMO, TSM)

## 1. Authority and scope

Authorized by the principal's bounded six-record fresh-review retention unit, following
`governance/decisions/OPS-0010-ws0005-lifecycle-ratification-and-retrospective-audit-authorization.md`
(`status: Accepted`, merged via PR #191, merge commit `0863f9dbbb861afd752d0cfeaa28369dd3b321ec`; its
own `status: Accepted` synchronization merged via PR #192, merge commit
`59f7ac56fdb1a4c5b3c0e45d6b545ea88a126ec4`) and the implementation `OPS-0010` §3 authorized: PR #193
(merge commit `760a0d1ba568b90d745c8cd4d3427357ae26bfa3`, reviewed/accepted head
`6eac98c742666d2ea8645427c16b49c994f7d57d`), which combined a retrospective audit of 13 legacy
Company Intelligence records and a lifecycle-only closure of five PR #189 records, and held back
COST, XOM, NVDA, GEV, ISRG, TMO, and TSM pending a fresh, CVX-style independent retrospective
review of each.

PR #193's own retained independent exact-head review
(`https://github.com/Mast3rkey/Portfolio-HQ/pull/193#issuecomment-5117143327`, posted before merge,
anchored to reviewed head `6eac98c742666d2ea8645427c16b49c994f7d57d`) performed exactly that fresh
retrospective review for all 7 held-back tickers. It reported no content-level BLOCKER or MATERIAL
finding for six of them — COST, XOM, NVDA, GEV, TMO, TSM — while finding ISRG genuinely distinct: a
PR #110 refresh with no identifiable governing `PI-####` (or other) authorization anywhere in this
repository, an authority gap the reviewing session explicitly declined to cure and referred to a
future, separate governance decision.

The principal has authorized one bounded six-record fresh-review retention unit for exactly COST,
XOM, NVDA, GEV, TMO, and TSM. **This authorizes filing and synchronizing retained review evidence
only.** It is not principal acceptance of this PR, and it does not authorize: new company research;
Company Intelligence edits; automatic lifecycle promotion before this PR completes its own
lifecycle; resolution of ISRG; Milestone 3 completion; Milestone 4; or any holdings, tier, target,
allocation, or margin change.

**This artifact does not itself promote any record to PROVISIONAL.** Every "eligible pending this
PR's lifecycle" conclusion below is a draft conclusion. It becomes effective only after this
implementation PR (1) receives its own eligible independent exact-head review, (2) completes any
required bounded correction and re-review, (3) receives a separately retained pre-merge `Principal
acceptance:` statement per `OPS-0010` §2, (4) merges at the unchanged accepted head, and (5)
receives immediate post-merge verification.

## 2. Author role and independence limitation

This artifact was authored by the session that opened the implementation PR carrying it. It is
therefore **not** an eligible independent review under `OPS-0007` §1.1 ("a session and model that
did not author or edit the reviewed work") — it cannot supply its own element-1 review requirement
for itself. Its conclusions are a retention synthesis of the already-retained PR #193 review
comment, cross-checked against current repository state via direct git/GitHub inspection — not a
fresh independent assessment of the six companies' content in its own right. Where retained
evidence is described below as sufficient, that rests on the independent reviewing session's own
work (`issuecomment-5117143327`), not on this authoring session's own judgment of the underlying
Company Intelligence content.

## 3. Verified repository base

Independently verified this session, before any edit:

- Repository identity: `Mast3rkey/Portfolio-HQ`.
- `git fetch origin main`; local `HEAD` on branch `claude/six-record-review-retention-4pjtcu`
  confirmed identical to `origin/main` at `760a0d1ba568b90d745c8cd4d3427357ae26bfa3` before any edit
  — matching this task's expected preflight cutoff exactly. Working tree confirmed clean.
- **Zero open pull requests** confirmed via the GitHub API (`list_pull_requests`, `state: open` →
  `[]`) — no overlapping in-flight work.
- PR #193 confirmed `merged: true`, base `59f7ac56fdb1a4c5b3c0e45d6b545ea88a126ec4`, head
  `6eac98c742666d2ea8645427c16b49c994f7d57d`, merge commit
  `760a0d1ba568b90d745c8cd4d3427357ae26bfa3` — independently confirmed present at `origin/main`'s
  tip via `git log`/`git rev-parse`.
- `OPS-0010` confirmed `status: Accepted` in both its own frontmatter
  (`governance/decisions/OPS-0010-ws0005-lifecycle-ratification-and-retrospective-audit-authorization.md`)
  and its corresponding `governance/decisions.yaml` entry.
- The PR #193 review comment
  (`https://github.com/Mast3rkey/Portfolio-HQ/pull/193#issuecomment-5117143327`, id `5117143327`,
  posted 2026-07-29T11:30:44Z) independently re-fetched via `pull_request_read` (`get_comments`) —
  confirmed to exist, attributed to the repository owner account (the same attribution convention
  every prior retained review on this repository uses, since GitHub blocks a formal same-account
  `APPROVE`/`REQUEST_CHANGES` review object here), and anchored explicitly, in its own text, to
  "Exact reviewed head: `6eac98c742666d2ea8645427c16b49c994f7d57d`" — matching PR #193's actual
  merged head exactly.
- A second comment (id `5117275717`, posted 2026-07-29T11:44:25Z, before the merge at 11:44:46Z)
  independently re-fetched and confirmed to carry a `Principal acceptance:` statement for PR #193
  itself, naming the same exact head and explicitly declining to treat the six fresh reviews as
  "effective repository evidence" — distinct from, and not a substitute for, this new PR's own
  required acceptance.
- `governance/decisions/` and `governance/decisions.yaml` reconciled: 46 files (excluding
  `README.md`) = 46 indexed entries, no orphans.
- `intelligence/companies/*.yaml`: 45 files, `intelligence_validator.validate_directory(...)` →
  **45/45 valid**. `intelligence/themes/*.yaml`: **2/2 valid**.
- `freshness_validator.py` → **OK**.
- Full test suite: `python3 -m pytest -q` → **1502 passed**, 0 failed.

## 4. Source-review provenance

**Controlling source**: `https://github.com/Mast3rkey/Portfolio-HQ/pull/193#issuecomment-5117143327`
(comment id `5117143327`), titled "Independent exact-head review — PR #193 (OPS-0010 retrospective
lifecycle audit)," posted 2026-07-29T11:30:44Z, before PR #193's merge (2026-07-29T11:44:46Z).

That review's own reviewer-independence statement: "This is a freshly-invoked Claude Code session
that did not author PR #193, its audit artifact, its `operations/WORKSTREAMS.yaml` synchronization,
its `CLAUDE.md` corrections, or any of the 45 Company Intelligence records under discussion
(including the 7 held-back records fresh-reviewed below). No memory of any of that drafting work."
It further discloses that `pull_request_review_write` was unavailable for a formal same-account
review object on this single-account repository, and that the comment is posted instead "per
`OPS-0007` §1's capability-based standard... as the attributable review record."

The review states its own methodology for the fresh six-plus-ISRG reviews: "methodology:
`PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md` template," running
`intelligence_validator.py`/`freshness_validator.py`/pytest live and independently re-querying
GitHub PR history for each record, rather than citing PR #193's own audit artifact's prior
conclusions.

This artifact treats that comment as the controlling source for what the prior independent
reviewer concluded, preserves its actual meaning per ticker (§7 below), and does not add any
finding absent from it.

## 5. Retention methodology

For each of COST, XOM, NVDA, GEV, TMO, and TSM, this artifact:

1. Extracts the retained per-ticker verdict, findings, and rationale directly from the controlling
   comment's own table and prose (§4 above) — no paraphrase that would change the retained meaning.
2. Independently re-confirms record identity, current tier/target (as existing policy only), and
   validator/freshness status against current repository state (§3).
3. Maps `OPS-0007` §3's five elements per ticker (§8), distinguishing what the retained review
   evidence supports from what only this PR's own future lifecycle can supply.
4. Where the retained comment's own language is internally ambiguous (TSM's verdict label — §7.6),
   states the ambiguity explicitly rather than silently resolving it, and defers resolution to the
   independent reviewer of this new PR.
5. Does not reconstruct any unpublished agent reasoning beyond what the retained comment states, and
   does not add a finding this artifact's author independently discovered — this is a retention
   artifact, not a fresh review.

## 6. Ticker sections

### 6.1 COST

- **YAML**: `intelligence/companies/COST.yaml` — **Markdown**: `intelligence/companies/COST.md`.
- **Governed tier/target (existing policy only)**: T1, 3.35% (`targets.yaml` `tiers.T1`).
- **Review provenance**: fresh retrospective review performed within the retained PR #193 review
  comment (`issuecomment-5117143327`), applying the `PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_
  20260728.md` methodology to COST's *current* merged record.
- **Reviewer-independence statement (from retained evidence)**: "a freshly-invoked Claude Code
  session that did not author PR #193... or any of the 45 Company Intelligence records under
  discussion (including the 7 held-back records fresh-reviewed below)."
- **Retained current-record verdict**: **RETROSPECTIVELY APPROVED**.
- **Retained BLOCKER findings**: none.
- **Retained MATERIAL findings**: "1 MATERIAL = review-provenance only (closed by this review)" —
  the retained review characterizes this as the same review-provenance gap PR #193's own audit
  artifact identified for COST, closed by the fresh review's own act of reviewing, not a defect in
  COST's content.
- **Retained MINOR findings**: 2 — "warehouse count sums to 913 vs. stated 914; one uncited
  membership-fee figure."
- **Retained NOTE findings**: none stated beyond the above in the retained comment's COST row.
- **Schema and validator status**: `intelligence_validator.py` confirms COST valid within the
  current 45/45 run (this session, §3).
- **Freshness state**: present in `intelligence/freshness_registry.yaml`, unaffected by this
  filing.
- **Lifecycle conclusion**: **RETAINED REVIEW SUPPORTS ELIGIBILITY PENDING THIS PR'S LIFECYCLE.**
- **Exact remaining action**: this implementation PR's own independent review, any required bounded
  correction and re-review, a separately retained pre-merge `Principal acceptance:` statement,
  unchanged-head merge, and immediate post-merge verification (§9-§10).

### 6.2 XOM

- **YAML**: `intelligence/companies/XOM.yaml` — **Markdown**: `intelligence/companies/XOM.md`.
- **Governed tier/target (existing policy only)**: band, 0.75% (1.25x cap); member of the `oil`
  correlated-cluster cap (`targets.yaml` `caps.clusters`, XOM + CVX, ≤20% of book).
- **Review provenance**: same retained PR #193 review comment, same methodology, applied to XOM's
  current merged record.
- **Reviewer-independence statement (from retained evidence)**: identical to §6.1 — the same
  session, applying the same independence disclosure across all seven fresh reviews it performed.
- **Retained current-record verdict**: **RETROSPECTIVELY APPROVED**.
- **Retained BLOCKER findings**: none.
- **Retained MATERIAL findings**: none stated for XOM in the retained comment's table (the "Content
  BLOCKER/MATERIAL" column reads "None").
- **Retained MINOR findings**: 3 — "FY2025 payout ratio >100% unflagged; no explicit CVX/`oil`-
  cluster cross-reference; sources not numbered-ledgered in .md."
- **Retained NOTE findings**: none stated beyond the above.
- **Schema and validator status**: confirmed valid within the current 45/45 run (this session, §3).
- **Freshness state**: present in `intelligence/freshness_registry.yaml`, unaffected by this
  filing.
- **Lifecycle conclusion**: **RETAINED REVIEW SUPPORTS ELIGIBILITY PENDING THIS PR'S LIFECYCLE.**
- **Exact remaining action**: same as §6.1 — this implementation PR's own remaining lifecycle
  (§9-§10).

### 6.3 NVDA

- **YAML**: `intelligence/companies/NVDA.yaml` — **Markdown**: `intelligence/companies/NVDA.md`.
- **Governed tier/target (existing policy only)**: T1, 3.35%; member of the `semis`
  correlated-cluster cap (≤25% of book).
- **Review provenance**: same retained PR #193 review comment, same methodology, applied to NVDA's
  current merged record.
- **Reviewer-independence statement (from retained evidence)**: identical to §6.1.
- **Retained current-record verdict**: **RETROSPECTIVELY APPROVED**.
- **Retained BLOCKER findings**: none.
- **Retained MATERIAL findings**: none stated for NVDA.
- **Retained MINOR findings**: 1 — "risk severities arguably understate 54% 3-customer
  concentration + full China foreclosure, both rated \"moderate\"."
- **Retained NOTE findings**: none stated beyond the above.
- **Schema and validator status**: confirmed valid within the current 45/45 run (this session, §3).
- **Freshness state**: present in `intelligence/freshness_registry.yaml`, unaffected by this
  filing.
- **Lifecycle conclusion**: **RETAINED REVIEW SUPPORTS ELIGIBILITY PENDING THIS PR'S LIFECYCLE.**
- **Exact remaining action**: same as §6.1 — this implementation PR's own remaining lifecycle
  (§9-§10).

### 6.4 GEV

- **YAML**: `intelligence/companies/GEV.yaml` — **Markdown**: `intelligence/companies/GEV.md`.
- **Governed tier/target (existing policy only)**: T1, 3.35%; member of the `power_infra`
  correlated-cluster cap (≤20% of book).
- **Review provenance**: same retained PR #193 review comment, same methodology, applied to GEV's
  current merged record.
- **Reviewer-independence statement (from retained evidence)**: identical to §6.1.
- **Retained current-record verdict**: **RETROSPECTIVELY APPROVED**.
- **Retained BLOCKER findings**: none.
- **Retained MATERIAL findings**: "1 MATERIAL = review-provenance only (PI-0020's refresh was
  same-session self-audit, doesn't satisfy independence — closed by this review)" — the retained
  review explicitly ties this to PR #193's own audit-artifact finding that GEV's PR #132 refresh
  self-audit did not satisfy independence, and states its own fresh review closes exactly that gap.
- **Retained MINOR findings**: 2 (count stated in the retained comment's table; the comment's
  prose does not itemize both beyond the table cell "2 MINOR" for GEV — this artifact does not
  invent itemized text the retained comment does not itself provide).
- **Retained NOTE findings**: none itemized beyond the above.
- **Schema and validator status**: confirmed valid within the current 45/45 run (this session, §3).
- **Freshness state**: present in `intelligence/freshness_registry.yaml`, unaffected by this
  filing.
- **Lifecycle conclusion**: **RETAINED REVIEW SUPPORTS ELIGIBILITY PENDING THIS PR'S LIFECYCLE.**
- **Exact remaining action**: same as §6.1 — this implementation PR's own remaining lifecycle
  (§9-§10).

### 6.5 TMO

- **YAML**: `intelligence/companies/TMO.yaml` — **Markdown**: `intelligence/companies/TMO.md`.
- **Governed tier/target (existing policy only)**: T2, 1.65%.
- **Review provenance**: same retained PR #193 review comment, same methodology, applied to TMO's
  current merged record.
- **Reviewer-independence statement (from retained evidence)**: identical to §6.1.
- **Retained current-record verdict**: **RETROSPECTIVELY APPROVED** (the retained comment's
  wording: "Content is internally honest about its own thinness; no capital-allocation/competitor
  discussion").
- **Retained BLOCKER findings**: none.
- **Retained MATERIAL findings**: none — the retained comment explicitly states TMO's "single-source
  sourcing (previously disclosed) assessed as MINOR, not MATERIAL."
- **Retained MINOR findings**: 1 — single-source sourcing, previously disclosed (carried forward
  from the 2026-07-25 Milestones-1/2 inventory audit, per PR #193's own audit artifact §6.12, not
  independently re-assessed by this filing).
- **Retained NOTE findings**: "no capital-allocation/competitor discussion" — recorded by the
  retained review as descriptive content-gap context, not itself classified as a severity-graded
  finding above MINOR.
- **Schema and validator status**: confirmed valid within the current 45/45 run (this session, §3).
- **Freshness state**: present in `intelligence/freshness_registry.yaml`, unaffected by this
  filing.
- **Lifecycle conclusion**: **RETAINED REVIEW SUPPORTS ELIGIBILITY PENDING THIS PR'S LIFECYCLE.**
- **Exact remaining action**: same as §6.1 — this implementation PR's own remaining lifecycle
  (§9-§10).

### 6.6 TSM

- **YAML**: `intelligence/companies/TSM.yaml` — **Markdown**: `intelligence/companies/TSM.md`.
- **Governed tier/target (existing policy only)**: T1, 3.35%; member of the `semis`
  correlated-cluster cap (≤25% of book).
- **Review provenance**: same retained PR #193 review comment, same methodology, applied to TSM's
  current merged record.
- **Reviewer-independence statement (from retained evidence)**: identical to §6.1.
- **Retained current-record verdict — reproduced verbatim, not resolved**: "Content sound, no
  defect (agent labeled it \"CHANGES REQUIRED\" but its own stated rationale is the closed
  review-provenance gap only — \"no line of either file needs to change\"; I treat this as
  substantively equivalent to the other five APPROVED verdicts, flagging the label inconsistency
  itself as a NOTE)."
- **Retained BLOCKER findings**: none — the retained review's own "Content BLOCKER/MATERIAL" column
  for TSM reads "None."
- **Retained MATERIAL findings**: none against content — the retained review's separate prose
  states "for 6 of 7 (COST, XOM, NVDA, GEV, TMO, TSM), no BLOCKER or content-level MATERIAL finding
  survived independent review — each ticker's sole MATERIAL issue was the review-provenance gap the
  audit itself identified," which the retained review's TSM row also applies ("Same review-provenance
  closure as COST/GEV").
- **Retained MINOR findings**: "YAML `risks[]` narrower than MD narrative (corpus-wide convention,
  not TSM-specific)."
- **Retained NOTE findings**: the verdict-label inconsistency itself — see the TSM verdict-handling
  discussion, §7.6, below.
- **Schema and validator status**: confirmed valid within the current 45/45 run (this session, §3).
- **Freshness state**: present in `intelligence/freshness_registry.yaml`, unaffected by this
  filing.
- **Lifecycle conclusion**: **RETAINED REVIEW SUPPORTS ELIGIBILITY PENDING THIS PR'S LIFECYCLE**,
  subject to the unresolved verdict-label inconsistency being addressed as stated in §7.6 — this
  artifact treats the retained review's own synthesis (no content-level BLOCKER/MATERIAL survives,
  substantively equivalent to the other five) as *sufficient to support eligibility pending this
  PR's lifecycle*, while explicitly not resolving the inconsistency itself, per the task's own
  instruction not to silently rewrite it.
- **Exact remaining action**: same as §6.1 — this implementation PR's own remaining lifecycle
  (§9-§10) — **plus** the independent reviewer of this new PR must explicitly state whether it
  accepts the retained synthesis as sufficient or instead performs a fresh exact-record review to
  resolve the inconsistency itself (§7.6).

## 7. TSM verdict-handling — inconsistency preserved, not resolved

The retained review comment reports, for TSM specifically, that the fresh reviewing session
labeled its own finding **"CHANGES REQUIRED"** while stating in the same breath that the
underlying rationale is *only* the already-identified, already-closing review-provenance gap and
that "no line of either file needs to change." This is an internally inconsistent verdict label:
a "CHANGES REQUIRED" label ordinarily implies a required content edit, but the retained text
explicitly disclaims any content edit is needed.

**What is preserved here, verbatim, not silently resolved:**

1. **The original inconsistency**: the reviewing session's own label ("CHANGES REQUIRED") does not
   match its own stated rationale (no content change needed; the only issue is the closed
   review-provenance gap).
2. **The PR #193 reviewer's own retained synthesis**: the same reviewing session explicitly states,
   in its own text, "I treat this as substantively equivalent to the other five APPROVED verdicts,
   flagging the label inconsistency itself as a NOTE" — i.e., the reviewer's own synthesis already
   proposes to treat TSM as equivalent to COST/XOM/NVDA/GEV/TMO's APPROVED outcome, not as a
   distinct, unresolved defect.
3. **Whether that retained synthesis is sufficient for eligibility, or requires fresh resolution**:
   this artifact does not itself decide that question. It records TSM's lifecycle conclusion in
   §6.6 as resting on the retained synthesis (which explicitly treats the inconsistency as a
   labeling NOTE, not a substantive defect) — but requires the independent reviewer of *this* new
   PR to either (a) explicitly accept that synthesis as sufficient before eligibility is treated as
   confirmed, or (b) perform a fresh exact-record review of TSM's current merged content to resolve
   the inconsistency directly, rather than deferring to the prior session's own self-characterized
   NOTE indefinitely.

This artifact does not rewrite "CHANGES REQUIRED" as "APPROVED," and does not rewrite "APPROVED" as
"CHANGES REQUIRED" — both would silently resolve a genuine inconsistency the retained source itself
disclosed. TSM's status in the partition below (§11) is recorded as eligible-pending on the same
basis as the other five, precisely because the retained review's own synthesis says so — not
because this artifact independently re-characterizes the "CHANGES REQUIRED" label as harmless.

## 8. OPS-0007 §3 lifecycle mapping — all six tickers

| Element | COST | XOM | NVDA | GEV | TMO | TSM |
|---|---|---|---|---|---|---|
| 1. Eligible independent exact-head or exact-record review | SATISFIED (retained fresh review, `issuecomment-5117143327`) | SATISFIED | SATISFIED | SATISFIED | SATISFIED | SATISFIED, subject to §7's unresolved label question |
| 2. Correction and re-review, or evidence none required | NOT APPLICABLE — retained review found no content BLOCKER/MATERIAL requiring correction | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | INDETERMINATE — retained review's own label ("CHANGES REQUIRED") is internally inconsistent with its stated rationale; see §7 |
| 3. Principal acceptance | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED |
| 4. Unchanged reviewed and accepted head merged to main | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED |
| 5. Post-merge verification | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED | NOT SATISFIED |

Elements 3, 4, and 5 are **NOT SATISFIED for this new retention unit** for all six tickers, by
design — this draft PR has not yet been reviewed, accepted, merged, or post-merge-verified.
`OPS-0010`'s historical §1 ratification does not apply here: it is bounded to WS-0005 lifecycle
work merged **at or before** `OPS-0010`'s own verified preflight cutoff (`origin/main` at
`decaaa7738e0a54bf05892941061518497777c70`), which predates this new PR entirely, and in any case
this new PR's own principal acceptance must be a freshly retained statement under `OPS-0010` §2's
tightened, mandatory going-forward standard, not an inference from any prior ratification or from
PR #193's own separate acceptance.

Element 2 is marked NOT APPLICABLE for COST, XOM, NVDA, GEV, and TMO because the retained review
found no BLOCKER or MATERIAL content finding requiring a correction pass for those five. For TSM,
element 2 is marked INDETERMINATE rather than SATISFIED or NOT APPLICABLE, precisely because the
retained review's own verdict label creates ambiguity about whether a correction was contemplated
— resolving that ambiguity is left to this new PR's own independent reviewer, per §7.

## 9. Pending-effect boundary

Nothing in this artifact, and nothing in the accompanying `operations/WORKSTREAMS.yaml`
synchronization, makes any of the six tickers effectively PROVISIONAL. Repository truth after PR
#193 remains: 38 effective PROVISIONAL records (27 confirmed + 11 eligible-pending-PR-#193's-own-
lifecycle, which itself completed on PR #193's merge — see §11 below for the corrected accounting);
these six records remain held back despite favorable advisory reviews, pending this new PR's own
full `OPS-0007` §3 lifecycle; ISRG remains held back for a separate authority decision. This
artifact describes the six as **eligible pending this PR's lifecycle**, never as already
PROVISIONAL, effective, or confirmed.

## 10. ISRG exclusion and authority gap

ISRG is explicitly outside this filing's authorized scope. The retained PR #193 review comment
found ISRG's fresh retrospective review genuinely distinct in kind from the other six: **"ISRG
AUTHORITY GAP — GOVERNANCE DECISION REQUIRED."** Its own text: "PR #110's own commit `8c7755e`
discloses the refresh proceeded on 'an unscheduled, principal-authorized evidence refresh prompted
by the tier review' — a conversational-authorization claim, not a citation to a filed decision —
and `PI-0016` already establishes that 'informal chat sign-off does not suffice' for company review
authorization... Content quality does not cure this — a well-written record with no governing
authorization remains an authority gap." This finding independently corroborates PR #193's own
audit artifact, which disclosed the same gap without attempting to resolve it.

This filing does not resolve, research, or otherwise act on the ISRG authority gap. ISRG remains
held back, separately, pending its own future, explicit governance decision — exactly as the task's
authorization states.

## 11. Updated 45-record partition

Programmatically re-derived this session directly from `intelligence/companies/*.yaml` (45 files),
independently verified: union = 45, no overlap, no omission, no duplicate, no extraneous ticker
(script output retained in this session's own working notes; the four sets below are mutually
exclusive and jointly exhaustive over all 45 filenames).

**Set 1 — Confirmed PROVISIONAL, already effective, unchanged by this filing (27 records)**: AVGO,
AMD, MRVL, INTC (Batch 3); ETN, VRT, PWR (Batch 4); MSFT, GOOGL, META, AMZN (Batch 5); V, MA, JPM
(Batch 6); CVX (retrospective review); WDC (2026-07-29 reconciliation); LLY, ABBV, MRK, JNJ, GILD
(Batch 7); IBM, NOW, CRM, ORCL, CRWD, PANW (Batch 8).

**Set 2 — 38-record effective-PROVISIONAL boundary, per this task's own stated repository truth
(11 of the 38 being the records newly eligible via PR #193)**: ASML, AMAT, KLAC, LRCX (Batch 1);
MU, SKHY (Batch 2); CEG, BRK.B, WMT, MLM, AAPL (`PI-0032`, via PR #189). PR #193 itself received an
independent exact-head review (`issuecomment-5117143327`, verdict "PR #193 EXACT-HEAD APPROVED"), a
separately retained pre-merge `Principal acceptance:` statement (`issuecomment-5117275717`, naming
exact head `6eac98c742666d2ea8645427c16b49c994f7d57d`), and merged unchanged at that head
(`760a0d1b`); elements 1-2 for these 11 records were independently mapped SATISFIED per-ticker by
PR #193's own audit artifact (§6.1-6.6, §7 of that artifact). **This filing does not itself
independently re-verify or re-derive whether `OPS-0007` §3 element 5 (post-merge ancestry/scope/
validator/test re-verification) has been separately performed and recorded for these 11 records —
that determination is outside this six-record retention unit's authorized scope.** This artifact
adopts, without re-litigating, the task's own stated repository boundary that 38 records (this Set
1's 27 plus this Set 2's 11) are the current effective-PROVISIONAL count, and confines its own
independent work to Set 3 (§6-§10) and the ISRG exclusion (Set 4).

**Set 3 — Eligible pending this new PR's own lifecycle (6 records)**: COST, XOM, NVDA, GEV, TMO,
TSM. See §6 for each ticker's individual retained-evidence basis and §8 for the element-by-element
mapping. **None of these six is effective PROVISIONAL as of this artifact.**

**Set 4 — Held back for a separate governance authority decision (1 record)**: ISRG. See §10.

**Partition validation**: 27 (Set 1) + 11 (Set 2) + 6 (Set 3) + 1 (Set 4) = **45**, exact, no
overlap, no omission — independently verified this session by direct set comparison against all 45
`intelligence/companies/*.yaml` filenames.

**45 + 17 (`PI-0033` dispositions: 14 new — CAT, GNRC, NFLX, SHOP, UBER, HOOD, RTX, DELL, PLTR,
SPCX, RKLB, TSLA, BABA, UNH; 3 restated — DHR, SYK, EQIX) = 62 governed non-ETF tickers** —
independently reconciled this session against `targets.yaml`'s 65 total tiered tickers minus the 3
ETF names (SPY, QQQ, GLD), exact, zero overlap, zero omission.

## 12. Validation evidence

Run this session, against the verified base commit `760a0d1ba568b90d745c8cd4d3427357ae26bfa3`
(before this implementation's own edits):

- `intelligence_validator.validate_directory('intelligence/companies')` → **45/45 valid**, zero
  errors.
- `intelligence_validator.validate_themes_directory('intelligence/themes')` → **2/2 valid**.
- `freshness_validator.py` → **OK**.
- `python3 -m pytest -q` → **1502 passed**, zero failed.
- `governance/decisions.yaml` reconciliation against `governance/decisions/*.md` (excluding
  `README.md`) → **46 filed = 46 indexed**, no orphans, no missing entries (this implementation
  touches neither file).
- Programmatic 45-record partition validation (§11) → 27 + 11 + 6 + 1 = 45, exact, no overlap, no
  omission.
- 45 + 17 = 62 governed-roster reconciliation (§11) → exact, no overlap, no omission.
- `git diff --check` on this implementation's own changes → clean.
- Protected-path diff (`targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py`,
  `constitution/`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`,
  `governance/decisions/`, `governance/decisions.yaml`, every `intelligence/companies/*.yaml`/
  `*.md` file, every `freshness_*` file, `CLAUDE.md`) against this implementation's own diff →
  **empty** — this implementation touches only this new artifact and `operations/WORKSTREAMS.yaml`.
- Exact changed-file inspection (this implementation's own diff against `origin/main`) → exactly
  the two files named above; no other file touched.

## 13. Exact remaining lifecycle actions

- **For this implementation PR as a whole**: eligible independent exact-head review per `OPS-0007`
  §1; any required bounded correction and exact-head re-review; a separately retained pre-merge
  `Principal acceptance:` statement per `OPS-0010` §2, naming this PR's own exact accepted head;
  merge of the unchanged accepted head; immediate post-merge ancestry/scope/validator/test
  re-verification.
- **For the 11 Set-2 tickers**: post-merge ancestry/scope/validator/test re-verification against
  PR #193's own merged state (`OPS-0007` §3 element 5) — not performed by this artifact, and not
  itself gated on this new PR's own lifecycle, since Set 2's elements 1-4 are already independently
  satisfied by PR #193's own completed lifecycle.
- **For the 6 Set-3 tickers (this filing's subject)**: this new PR's own full lifecycle (above) —
  no ticker-specific gap remains beyond that shared lifecycle, except TSM's verdict-label question
  (§7), which the independent reviewer of this PR must explicitly address.
- **For ISRG**: unchanged — a separate, future, explicit governance decision resolving the PR #110
  authority gap; not begun, not authorized, by this filing.

## 14. Milestone 3 and Milestone 4 boundaries

- **Milestone 3 remains `in_progress`.** This filing does not complete it. `PI-0031` §K's
  seven-criterion completion standard is not evaluated by this artifact — criterion 2 (non-deferred
  T2 coverage) and criterion 3 (`semis`-cluster coverage, WDC) already carried open items unrelated
  to this six-record unit's scope, and criterion 7 (per-record lifecycle completion) is only
  partially advanced by this filing (six of seven previously-held-back tickers now eligible
  pending; ISRG remains held back).
- **Milestone 4 remains unauthorized.** Nothing in this artifact authorizes, implies, or narrows
  the `OPS-0006` §5 gate.
- **No tier, target, holdings, cluster, cap, allocation, margin parameter, or production-code file
  is touched by this artifact or by this implementation unit.**
- **No new company research is performed or authorized by this artifact** — every conclusion above
  rests on the already-retained PR #193 review comment, not on any new assessment of the six
  companies' underlying content.

## Verdict

**This is a draft retention artifact, authored by the implementation PR's own author session, not
yet independently reviewed.** It concludes, on currently retained evidence: COST, XOM, NVDA, GEV,
and TMO are eligible for a PROVISIONAL determination once this implementation PR itself completes
its own independent-review, correction-if-needed, principal-acceptance, merge, and
post-merge-verification lifecycle, with no unresolved content-level BLOCKER or MATERIAL finding
against any of the five. TSM is likewise assessed eligible pending this PR's lifecycle, on the
basis of the retained reviewer's own explicit synthesis that its label inconsistency is
substantively equivalent to an APPROVED verdict — but that inconsistency is preserved, not resolved,
and the independent reviewer of this PR must explicitly address it (§7). ISRG remains held back,
unresolved, pending a separate governance decision. No ticker is declared PROVISIONAL by this
artifact. The 27 records already confirmed PROVISIONAL, and the 11 records whose lifecycle
completed via PR #193's own merge, are unaffected. Milestone 3 remains `in_progress`; Milestone 4
remains unauthorized.
