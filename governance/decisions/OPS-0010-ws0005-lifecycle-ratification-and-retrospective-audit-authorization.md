---
decision_id: OPS-0010
date: 2026-07-29
status: Proposed
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0004, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0005, PI-0007, PI-0009, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027, PI-0028, PI-0029, PI-0030, PI-0031, PI-0032, PI-0033]
supporting_artifact: null
---

## Context

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin/main` fetched.** `git fetch origin main` returned `270b471..decaaa7 main -> origin/main`;
  `git rev-parse origin/main` confirmed `decaaa7738e0a54bf05892941061518497777c70`, matching this
  filing's expected preflight cutoff exactly. Local `HEAD` on the designated branch,
  `claude/ops-0010-governance-decision-xo6hhl`, confirmed identical to `origin/main` before any edit.
  Working tree confirmed clean.
- **`decaaa7738e0a54bf05892941061518497777c70` is PR #190's merge commit** — confirmed via
  `git log --oneline` ("Merge pull request #190: Milestone 3 lifecycle reconciliation: PI-0033
  audit, WDC PROVISIONAL determination"). PR #190 is present on `main` at the tip.
- **Zero open pull requests** confirmed via the GitHub API at this filing's preflight; no branch or
  in-flight work overlapping this filing's scope.
- **`governance/decisions.yaml` and `governance/decisions/` independently reconciled**: 45 files
  under `governance/decisions/` (excluding `README.md`) = 45 entries in `governance/decisions.yaml`,
  no orphans, highest filed `PI-####` is `PI-0033`, highest `OPS-####` is `OPS-0009`. **`OPS-0010`
  confirmed the next unused decision number** in its series, checked live against both the directory
  and the index, not assumed.
- **`intelligence/companies/` independently confirmed to hold 45 files, all valid**
  (`intelligence_validator.py`), matching `operations/WORKSTREAMS.yaml`'s own WS-0005 entry's
  27 + 18 = 45 partition exactly (see below).
- **`constitution/INVESTMENT_CONSTITUTION.md`, `GOV-0002`, `OPS-0004`, `OPS-0007`, `OPS-0008`,
  `OPS-0009`, `PI-0031`, `PI-0032`, `PI-0033`, `governance/decisions.yaml`,
  `operations/WORKSTREAMS.yaml`, `CLAUDE.md`, the retained CVX retrospective-audit precedent
  (`governance/audits/PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md`), and the retained
  18-record audit and lifecycle-design conclusions already recorded in `operations/WORKSTREAMS.yaml`'s
  WS-0005 entry (the 2026-07-29 "Milestone 3 lifecycle and factual-state reconciliation" passage) were
  all read in full this session** — not relied on from memory — to confirm `OPS-0007` §3's five-part
  PROVISIONAL definition, `OPS-0008`'s Research Wave Protocol v1, `OPS-0009`'s lane discipline (this
  filing is Lane G throughout — full weight, no reduction), `PI-0031` §K's Milestone 3 completion
  standard, and the exact current partition of the 45 Company Intelligence records.
- **No repository truth conflicts with the principal's stated premise or with the approved design.**

### The 27/18 partition this decision responds to

`operations/WORKSTREAMS.yaml`'s WS-0005 entry, in its 2026-07-29 reconciliation passage (itself
independently re-verified this session against `intelligence/companies/*.yaml`), records that of the
45 current Company Intelligence records:

- **27 are confirmed PROVISIONAL under `OPS-0007` §3** — each with retained evidence of all five
  required elements recorded elsewhere in the register: AVGO, AMD, MRVL, INTC (Batch 3); ETN, VRT,
  PWR (Batch 4); MSFT, GOOGL, META, AMZN (Batch 5); V, MA, JPM (Batch 6); CVX (via the retained
  retrospective review, `PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md`); WDC (via the
  2026-07-29 reconciliation); LLY, ABBV, MRK, JNJ, GILD (Batch 7); IBM, NOW, CRM, ORCL, CRWD, PANW
  (Batch 8).
- **18 remain unresolved against `OPS-0007` §3's specific five-element test** — not found deficient,
  merely never individually re-evaluated against that test:
  - **13 legacy records** — ASML, AMAT, KLAC, LRCX (Batch 1); MU, SKHY (Batch 2); COST, XOM, NVDA,
    GEV, ISRG, TMO, TSM (the pre-`OPS-0007` first-coverage pilots, `PI-0003`/`PI-0005`/`PI-0007`/
    `PI-0009`/`PI-0012`-`PI-0013`) — reviewed and merged under the review process in force before
    `OPS-0007`'s 2026-07-26 adoption, and never mapped against `OPS-0007` §3's specific five-element
    test by any retained entry.
  - **5 PR #189 records** — CEG, BRK.B, WMT, MLM, AAPL (`PI-0032`'s five governed-holding units,
    merged via PR #189 alongside WDC, with no PROVISIONAL determination recorded for them anywhere
    in the register, unlike WDC's own companion unit from the same PR).

27 + 18 = 45, exhaustive and mutually exclusive, independently re-confirmed this session by direct
set comparison against `intelligence/companies/*.yaml`.

### Principal design approval

The principal approved the following design for this filing, in these terms:

> "Approve the OPS-0010 design: ratify past acceptance, tighten future acceptance retention, use one
> combined 13-record retrospective audit, and include the five PR #189 lifecycle closures in the same
> implementation unit."

**This approval authorizes drafting OPS-0010. It does not constitute acceptance of this decision's
final text, does not authorize its merge, does not declare any record PROVISIONAL, does not close
Milestone 3, and does not authorize Milestone 4.** This filing performs no research, no audit, and no
lifecycle determination itself — it authorizes exactly one later, separate implementation unit to
perform the retrospective audit and factual synchronization described below.

## Decision

**OPS-0010 does exactly four things: (1) a one-time, explicit principal ratification of the
convention this repository's own register has already applied ad hoc across Batches 3-6 and WDC, but
scoped narrowly to supply only one of `OPS-0007` §3's five PROVISIONAL elements; (2) a tightened,
mandatory retention standard for every future WS-0005 lifecycle merge's principal-acceptance evidence;
(3) authorization of exactly one later, separate implementation unit performing a combined
retrospective audit of the 13 legacy records and a lifecycle-only closure of the 5 PR #189 records;
and (4) an explicit statement of what remains outstanding after that unit completes.** This filing
itself creates no Company Intelligence record, no audit artifact, no factual synchronization, and
performs no research or review of any kind — it authorizes the governance-authorization package only,
named in full in §10.

### 1. Historical acceptance ratification

**A one-time, explicit principal governance act**, effective on this decision's own merge, ratifying
the following as satisfying `OPS-0007` §3 element 3 (explicit principal acceptance, at the exact final
head) for WS-0005 lifecycle work merged **on or before this decision's verified preflight cutoff**
(`origin/main` at `decaaa7738e0a54bf05892941061518497777c70`, 2026-07-29):

**Ratified historical convention**: an eligible independent, exact-head review under `OPS-0007` §1,
followed by a same-account merge, with **no intervening commit between the reviewed head and the
merged head**, is ratified as satisfying element 3 for WS-0005 lifecycle work merged at or before the
cutoff above.

This ratification is framed, deliberately, as **a new explicit principal governance act performed by
this decision** — not as a finding that historic merge metadata independently proved acceptance on its
own terms, and not as a retroactive reinterpretation of what a bare merge action always meant. The
register's own prior entries (Batches 3-6, and the 2026-07-29 WDC determination) treated this pattern
as satisfying element 3 by inference from repeated internal precedent; this decision replaces that
inference with an actual, dated, principal-authorized ratification, closing the same category of
evidentiary gap `OPS-0004`'s Finding FA-1 identified for PR #143's review claim — but for the
acceptance step rather than the review step.

**This ratification supplies `OPS-0007` §3 element 3 only.** It does not:

- establish that elements 1 (eligible independent exact-head review), 2 (bounded correction and
  exact-head re-review where required), 4 (merge to `main` at that exact head), or 5 (post-merge
  ancestry/scope/validator/test re-verification) were satisfied for any record — each of those must
  still be independently confirmed, per record, exactly as `OPS-0007` §3 already requires;
- declare any of the 18 currently unresolved tickers PROVISIONAL — a ratified element 3 is necessary
  but never sufficient on its own, exactly as `OPS-0007` §3 already states for every element
  individually;
- reopen, downgrade, or in any way alter the status of the 27 records already confirmed PROVISIONAL —
  their existing determinations stand exactly as recorded, untouched by this ratification;
- replace the CVX-style retrospective audit required, per §3.A below, for any of the 13 legacy
  records where historic evidence proves insufficient to confirm elements 1, 2, 4, or 5 on the
  existing record alone.

### 2. Future acceptance retention standard

**Effective on this decision's own merge**, for every WS-0005 lifecycle merge occurring **after**
OPS-0010 itself merges, `OPS-0007` §3 element 3 (explicit principal acceptance, at the exact final
head) is satisfied only by a **separately retained statement**, labeled exactly:

> Principal acceptance:

That retained statement must, in every case:

1. **Identify the exact accepted head SHA** — the precise commit that is being accepted, not a branch
   name, a PR number alone, or a description of the change.
2. **Be distinguishable from the independent-review verdict** — a reviewer's "APPROVED" or equivalent
   conclusion is not, by itself, a principal-acceptance statement, regardless of how the review is
   retained.
3. **Be distinguishable from the mechanical merge action** — the act of clicking merge, or of a merge
   commit landing on `main`, is not, by itself, a principal-acceptance statement; this is the exact
   evidentiary gap the historical convention in §1 above required this decision's own explicit
   ratification to close, and going forward the retained statement must exist independently of that
   mechanical act.
4. **Exist in one of**: a retained PR comment; an accepted decision artifact; or a merge message,
   provided the merge message itself is generated or supported by this repository's own tooling in a
   way that reliably carries the statement forward (a bare default merge-commit message, with no such
   support, does not qualify).
5. **Reflect an actual principal instruction** — never manufactured, inferred, or paraphrased by an
   authoring or reviewing session on the principal's behalf.
6. **Precede the merge** — the statement must exist before the merge action, not be reconstructed or
   backfilled afterward.
7. **Never be inferred merely from silence, timing, or merge metadata** — the same-account,
   no-intervening-commit pattern ratified historically in §1 is retired as a going-forward evidentiary
   substitute the moment this decision merges; from that point, only an actual retained statement
   meeting items 1-6 above satisfies element 3.

**OPS-0010's own eventual acceptance must use this method.** Before this governance PR may be marked
ready or merged, a retained "Principal acceptance:" statement meeting all seven requirements above,
identifying this decision's own exact accepted head SHA, must exist — see §11.

### 3. Retrospective implementation authorization

**Authorizes exactly one later, separate implementation unit** (not opened by this filing) containing
parts A through D below, gated on this governance decision's own independent review, principal
acceptance under §2's new standard, and merge — required to stay in draft state until that review
lands.

#### A. Combined retrospective audit — the 13 legacy records

**One combined retrospective audit artifact**, filed under `governance/audits/`, containing
**independent per-ticker sections** for exactly these 13 records:

ASML, AMAT, KLAC, LRCX, MU, SKHY, COST, XOM, NVDA, GEV, ISRG, TMO, TSM.

Each ticker's section must separately record, at minimum:

1. **Record identity** — exact file paths, current content hash or equivalent identity check.
2. **Original implementation and authority provenance** — the governing `PI-####` authorization, the
   implementation PR number, and the merge commit that landed the record on `main`.
3. **Review evidence** — whatever independent review evidence exists for that record (a retained
   GitHub review/comment, a `governance/audits/` artifact, or an explicit, disclosed absence of
   either).
4. **Correction history** — any bounded correction or re-review the record underwent, or an explicit
   statement that none occurred.
5. **Element-by-element `OPS-0007` §3 mapping** — a separate determination for each of the five
   elements (eligible independent exact-head review; bounded correction and exact-head re-review
   where a material finding required one; explicit principal acceptance at the exact final head, per
   this decision's §1 ratification where applicable; merge to `main` at that exact head; post-merge
   ancestry/scope/validator/test re-verification), each marked satisfied, not satisfied, or unable to
   be determined from existing evidence.
6. **Conclusion** — PROVISIONAL (all five elements satisfied), not yet PROVISIONAL (one or more
   elements unresolved), or held back (a specific material defect found, per the exception process in
   §6 below).
7. **Findings** — by severity, per `OPS-0007` §1.8's classification discipline.
8. **Exact missing action when unresolved** — for any record not reaching a PROVISIONAL conclusion,
   the audit must state precisely what would resolve it (e.g., "no retained review artifact exists;
   requires a fresh CVX-style retrospective review of the current merged record before a PROVISIONAL
   conclusion can be reached"), not merely note that it is unresolved.

**When historic evidence is insufficient to confirm one or more of `OPS-0007` §3's elements for a
given ticker, the implementation must perform a fresh, CVX-style retrospective review of that
ticker's current merged record** — the same method, and the same retained-artifact convention, already
established and retained at `governance/audits/PR181_CVX_RETROSPECTIVE_INDEPENDENT_REVIEW_20260728.md`
(reviewer identity and independence; repository and PR identification; exact SHAs; evidence-artifact
identity; review date; exact reviewed file set; methods and validations; findings by severity; explicit
distinction between whether an event actually occurred and whether it was previously retained; a
verdict; and an explicit statement of the scope of authority created — none beyond the retrospective
determination itself) — before that ticker's record may be concluded PROVISIONAL. Applying that fresh
review is not optional where historic evidence is insufficient; it is the same standard CVX itself was
held to.

**One defective ticker must be held back without blocking the others.** If the audit finds a specific,
material defect in any one of the 13 records that cannot be resolved through the audit artifact and
the factual synchronization in §3.C alone, that ticker's conclusion is held back — disclosed, not
silently PROVISIONAL — while the remaining twelve proceed to whatever conclusion their own evidence
supports. A single defective record never blocks or delays the other twelve.

#### B. Lifecycle-only closure — the five PR #189 records

**One lifecycle-only closure section**, addressing exactly: CEG, BRK.B, WMT, MLM, AAPL.

This section **may reuse** the already-retained PR #189 review, correction, exact-head delta review,
unchanged-head merge, and post-merge verification evidence — it is not required to re-perform any of
that work. It must:

1. **Apply this decision's §1 ratification only to element 3** (explicit principal acceptance) for
   these five records, exactly as it applies to the 13 legacy records.
2. **Independently map the other four elements** (eligible independent exact-head review; bounded
   correction and exact-head re-review where required; merge to `main` at the exact reviewed head;
   post-merge ancestry/scope/validator/test re-verification) against the retained PR #189 evidence —
   not assumed satisfied merely because §1's ratification resolves element 3.
3. **Authorize no new substantive company research** for any of the five — this is a lifecycle
   determination exercise applied to already-drafted, already-merged content, not a research
   authorization or a reopening of `PI-0032`'s substance.

#### C. Factual synchronization

**One factual synchronization**, within the same implementation unit, of:

1. `operations/WORKSTREAMS.yaml` — recording the audit's and closure section's actual conclusions,
   using only `OPS-0001`'s existing schema and status vocabulary.
2. **The Milestone 3 criterion-7 partition** — updating the register's own 27/18 accounting to reflect
   whatever new PROVISIONAL determinations, unresolved statuses, or held-back defects this unit's audit
   and closure section actually produce. This synchronization records the unit's own conclusions; it
   does not itself perform, substitute for, or pre-judge those conclusions.
3. **The register's verified-`main`-SHA reference** — refreshed to the implementation unit's own
   confirmed post-merge state.

#### D. Three CLAUDE.md Decisions Log corrections

**Three narrow, stale-wording-only corrections** to CLAUDE.md's own Decisions Log, within the same
implementation unit, for exactly:

- `OPS-0009` — currently described as "proposed (not yet accepted or merged)" in CLAUDE.md, when the
  decision is `status: Accepted` and merged.
- `PI-0032` — same stale "proposed (not yet accepted or merged)" wording, when `status: Accepted` and
  merged.
- `PI-0033` — same stale wording, when `status: Accepted` and merged.

Each correction updates only the stale proposed/unmerged characterization and points the reader to the
controlling decision file and the live register — it does not restate, summarize, or alter the
substance of any of the three decisions, and does not add narrative content beyond what is needed to
correct the stale status wording. **These three corrections belong exclusively to the later authorized
implementation unit — this governance filing does not make them itself** (see §10).

### 4. Later completion boundary

Stated explicitly, controlling over any contrary inference:

- **OPS-0010 does not complete Milestone 3.**
- **The retrospective implementation unit authorized by §3 does not automatically complete Milestone
  3** — even a fully successful audit and closure section, resolving every one of the 18 currently
  unresolved records to PROVISIONAL, does not by itself satisfy `PI-0031` §K's seven-criterion
  completion standard (which requires, among other things, every non-deferred T2 company covered and
  every active cluster member covered — conditions this filing does not evaluate or affect).
- **A separate, later Milestone 3 completion determination remains mandatory**, evaluating all seven
  of `PI-0031` §K's criteria together, exactly as `PI-0031`, `PI-0032`, and `PI-0033` already state.
- **Milestone 4 remains unauthorized** — nothing in this decision, or in the implementation unit it
  authorizes, authorizes, implies, or narrows the gate `OPS-0006` §5 established for it.

### 5. Current-status protection

This decision, and the implementation unit it authorizes, must preserve:

- **The 27 currently recorded PROVISIONAL tickers, without reopening or downgrading any of them.**
- **The 18 currently unresolved tickers, without prematurely promoting any of them** — a PROVISIONAL
  conclusion for any of the 18 is reached only through the audit or closure-section process in §3, per
  ticker, on its own evidence; none is promoted by this decision's own text.
- **`PI-0033`'s status as `Accepted`**, unedited.
- **Every current tier, target, holding, weight, cluster, cap, allocation, margin parameter, and
  safeguard**, exactly as currently governed.

### 6. Allowed implementation files, and the narrow exception process

The implementation unit authorized by §3 may change only:

1. **One new `governance/audits/` retrospective artifact** (the combined 13-record audit plus the
   5-record lifecycle-only closure section — one artifact, or a small number of directly related
   artifacts if the audit's own CVX-style fresh-review sub-steps for individual tickers require
   separate retained files, consistent with the CVX precedent's own single-artifact convention where
   evidence permits it).
2. **`operations/WORKSTREAMS.yaml`** — the factual synchronization described in §3.C.
3. **`CLAUDE.md`** — exactly the three stale-wording corrections described in §3.D, no other edit.

**Company Intelligence YAML or Markdown files remain prohibited**, unless the retrospective audit
discovers a specific material defect that cannot be resolved through the audit artifact and the
factual synchronization alone. **Any such exception must be**: disclosed explicitly in the audit
artifact, naming the exact defect and why the audit/synchronization route is insufficient; independently
reviewed under `OPS-0007` §1, anchored to the exact head containing the proposed content fix; and held
back from every unrelated ticker — a defect found in one record's YAML/Markdown never authorizes
touching any other record's content, and never authorizes new substantive research beyond the minimum
correction the defect requires.

### 7. Prohibited scope

This decision, and the implementation unit it authorizes, prohibit, under any interpretation:

- Any change to `targets.yaml`.
- Any change to `holdings.yaml`.
- Any tier, target, weight, cluster, or cap change.
- Any allocation or `allocate.py` change.
- Any margin or `margin_state.py` change.
- Any other production-code change.
- Any weakening of any existing test.
- Any trading or order execution.
- Any new company research (beyond the narrow, disclosed, independently-reviewed exception process in
  §6).
- Any automatic ranking, scoring, or aggregation of any company, batch, or finding.
- Any declaration that Milestone 3 is complete.
- Any Milestone 4 work.
- Any automatic promotion of a record to PROVISIONAL status outside the per-ticker, evidence-based
  process in §3.A/§3.B.
- Reopening, editing, or reinterpreting the substance of any accepted decision (`PI-0031`, `PI-0032`,
  `PI-0033`, `OPS-0007`, `OPS-0008`, `OPS-0009`, or any other) — this decision narrowly ratifies one
  evidentiary convention (§1) and tightens one going-forward standard (§2); it edits, supersedes, or
  reinterprets no other decision's substance.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any investment recommendation of any kind.

### 8. Review and lifecycle requirements

For **both** this governance decision and the later implementation unit authorized by §3:

1. **Eligible independent, exact-head review**, per `OPS-0007` §1's twelve-point capability-based
   standard.
2. **Bounded correction and exact-head re-review** for any material (Blocking or Major) finding, per
   `OPS-0009` §6's four-condition delta-review test — any doubt defaults to a full re-review, per
   `OPS-0009` §10.
3. **Explicit, separately retained principal acceptance**, per this decision's own §2 standard —
   identifying the exact accepted head SHA, distinguishable from the review verdict and the merge
   action, preceding the merge.
4. **Merge of the unchanged, accepted exact head** — no edit between the accepted head and the merged
   commit.
5. **Immediate post-merge ancestry, scope, validation, and cleanliness verification**, performed by the
   same session that merges, per `OPS-0009` §9 — never deferred to a later, unrelated session.

**A tool failure is not an empty result.** Where a validator, test run, or review tool fails to
execute, that failure must be disclosed and resolved before treating its absence as a passing or
negative finding. **Missing evidence is not passing evidence.** An element of `OPS-0007` §3, or a
control listed in this section, that cannot be confirmed from available evidence is recorded as
unresolved — never silently treated as satisfied.

### 9. Stopping condition

This decision's own authority, and the implementation unit's authority under it, stop when:

- The 13 legacy records have each received an individual lifecycle determination (PROVISIONAL, not
  yet PROVISIONAL with a stated missing action, or held back as defective).
- The five PR #189 records have each received a retained lifecycle determination under §3.B.
- The Milestone 3 criterion-7 partition is synchronized to reflect those determinations.
- The three CLAUDE.md stale entries are corrected.
- All implementation validation and post-merge checks required by §8 are complete.

**This decision does not authorize the subsequent Milestone 3 completion decision** — that remains a
separate, later, explicit governance act, exactly as §4 states.

### 10. Governance package scope (this filing)

This filing — the governance-authorization PR itself, not the later implementation unit — touches
exactly:

1. `governance/decisions/OPS-0010-ws0005-lifecycle-ratification-and-retrospective-audit-authorization.md`
   (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `OPS-0010`).

**No other file is touched by this governance filing.** In particular: **no `operations/WORKSTREAMS.yaml`
change is made here** — recording that this draft PR exists is administrative churn this filing avoids,
consistent with `OPS-0009`'s Lane M discipline that a register update records an already-true,
already-verified fact, not a still-pending draft authorization; and **no `CLAUDE.md` change is made
here** — the three stale-wording corrections named in §3.D belong exclusively to the later authorized
retrospective implementation unit, not to this authorization filing. No Company Intelligence record, no
audit artifact, and no test or validator file is created, modified, or authorized to be created by this
filing.

### 11. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own eligible independent review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review per
`OPS-0009` §6, and receive a separately retained **"Principal acceptance:"** statement meeting every
requirement of this decision's own §2 — identifying this decision's exact accepted head SHA — before it
may be marked ready or merged. **Nothing in §§1-9 becomes effective until this governance PR merges to
`main`.** This decision does not mark itself, or authorize marking itself, ready for merge, and does not
begin the retrospective implementation unit authorized in §3 — that unit's own PR is not opened by this
filing.

## Rationale

**Why ratify the historical convention explicitly, rather than leave it resting on inference.** The
register has already, four times over (Batches 3-6) plus once more for WDC, treated a same-account,
no-intervening-commit merge as the retained evidence of principal acceptance — a convention that
worked in practice but was never itself the product of an explicit principal governance act; it was an
inference the register drew and then repeated. `OPS-0004`'s own Finding FA-1 already established, for
the review step, that a claim resting only on inferred or unretained provenance is a gap worth closing
even when the underlying substance is sound. The same logic applies here to the acceptance step: rather
than continuing to treat repeated internal precedent as self-validating, this decision converts that
precedent into an actual, dated, bounded principal ratification — narrowly scoped to element 3 alone,
exactly matching what the historical pattern could actually evidence, and no more.

**Why the ratification is bounded to on-or-before-cutoff work only.** A ratification of unlimited
duration would quietly re-authorize the same lighter evidentiary standard indefinitely, defeating the
point of tightening it. Bounding it to work merged at or before this decision's own verified preflight
cutoff closes the historical gap without extending the lighter standard forward.

**Why a separately retained "Principal acceptance:" statement, going forward.** The same reasoning
`OPS-0009` §9 applied to post-merge verification timing — that a control's value depends on it actually
happening at the right moment, not on a later inference that it must have happened — applies here to
acceptance. A merge action alone conflates three distinct facts (a reviewer's verdict, a mechanical git
action, and an actual principal decision) into one event; requiring a separately retained statement
keeps those three facts separately falsifiable, exactly as `OPS-0007` §3 already treats review, merge,
and post-merge verification as separate, individually necessary elements.

**Why one combined 13-record audit, not 13 separate audits.** The 13 legacy records already share the
same open question (never individually mapped against `OPS-0007` §3's specific five-element test) and
the same era of evidence (pre-`OPS-0007` review process) — a single combined artifact with independent
per-ticker sections, exactly the shape `OPS-0008` §7 already prefers for retained evidence, avoids
thirteen near-duplicate audit filings while still requiring each ticker's own separate, individually
falsifiable conclusion.

**Why the five PR #189 records get a lifecycle-only closure, not a fresh audit.** Unlike the 13 legacy
records, PR #189's review, correction, delta review, and merge are all recently retained and directly
available — the same evidence base the WDC determination (the sixth unit from the same PR) already
drew on successfully. Requiring a fresh CVX-style review for these five would duplicate work the
existing retained evidence already supports; a lifecycle-only mapping exercise, applying this
decision's own §1 ratification to element 3 and independently confirming the other four from the
already-retained PR #189 record, is the proportionate instrument — the same "SHA-only reuse" economy
`OPS-0009` §4 already establishes for other frozen, already-validated evidence.

**Why the CVX-style fresh review is required, not optional, where historic evidence is insufficient.**
CVX itself was held to exactly this standard — its own PROVISIONAL determination came only after a
dedicated, independently-authored retrospective review, not from inference alone. Applying a looser
standard to the 13 legacy records than was applied to CVX would treat older, less-examined records more
generously than a newer one that received more scrutiny — backwards from what evidentiary rigor
requires.

**Why the three CLAUDE.md corrections are authorized here but deferred to the implementation unit.**
The stale wording is a narrow, disclosed, non-authority-bearing factual correction — exactly `OPS-0009`
Lane M territory — but making it in this governance-authorization filing would blur this filing's own
narrow scope (ratification and authorization only) with content that logically belongs alongside the
factual synchronization it is correcting toward. Filing it in the same implementation unit as the
audit and the register synchronization keeps all three "record what is now actually true" actions
together, and keeps this authorization filing itself touching only the two files named in §10.

## Alternatives Considered

- **Leave the historical acceptance convention as inferred precedent, with no explicit ratification.**
  Rejected — the same reasoning `OPS-0004` applied to the review-provenance gap applies here; an
  inference repeated five times is still an inference, not a governance act, and the principal's own
  approved design calls for ratifying it explicitly.
- **Apply the tightened future-acceptance standard retroactively to the 13 legacy and 5 PR #189
  records, requiring a fresh "Principal acceptance:" statement for each.** Rejected — this is precisely
  what §1's ratification exists to avoid; the historical convention is ratified as sufficient for
  element 3 specifically because demanding a fresh statement for already-merged work would be
  retroactive rule-tightening with no evidentiary benefit for work already actually accepted and
  merged under the prior, working convention.
- **Perform 18 separate, individual audits (13 legacy plus 5 PR #189) rather than one combined
  artifact plus one closure section.** Rejected per the principal's approved design and on the merits
  — see Rationale; the 13 share an evidentiary posture that supports one combined artifact, while the
  5 PR #189 records' recent, directly available evidence supports a lighter lifecycle-only closure
  rather than a full audit.
- **Authorize the retrospective implementation unit to also touch Company Intelligence content freely,
  in case the audit finds something worth correcting.** Rejected — this repository's own established
  discipline (`PI-0031`-`PI-0033`, `OPS-0008` §12) never grants open-ended content-editing authority
  alongside a lifecycle/audit authorization; the narrow, disclosed, independently-reviewed exception
  process in §6 is the correct, bounded instrument for the rare case where a defect actually requires
  it.
- **Fold the three CLAUDE.md corrections into this governance-authorization filing itself.** Rejected
  per explicit instruction and on the merits — those corrections depend on facts (which records
  actually reach PROVISIONAL) that this filing does not itself determine; making them here would risk
  the correction preceding, rather than following, the synchronization it is meant to reflect.
- **Declare Milestone 3 complete, or authorize Milestone 4, once the 18 unresolved records are
  resolved.** Rejected — explicitly outside the principal's approved design and outside this decision's
  own stated boundary in §4; `PI-0031` §K's seven-criterion test governs Milestone 3 completion, and
  this filing neither performs nor shortcuts that evaluation.

## Consequences

**Authorized, effective on this decision's merge:** a one-time, explicit principal ratification of the
historical WS-0005 acceptance convention, scoped to `OPS-0007` §3 element 3 only, for work merged at or
before this decision's verified preflight cutoff (§1); a tightened, mandatory "Principal acceptance:"
retention standard for every WS-0005 lifecycle merge from this point forward, applying to this
decision's own eventual acceptance (§2); and authorization of exactly one later, separate
implementation unit performing a combined retrospective audit of 13 legacy records, a lifecycle-only
closure of 5 PR #189 records, a factual synchronization of the register and the criterion-7 partition,
and three narrow CLAUDE.md corrections (§3), bounded by the file list in §6, the prohibitions in §7,
and the review discipline in §8.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; `allocate.py`, `margin_state.py`, `intelligence_validator.py`,
`intelligence_report.py`, every freshness module, and every existing test; every existing Company/Theme
Intelligence record, **including all 27 currently PROVISIONAL records and all 18 currently unresolved
records** — none is reopened, downgraded, or promoted by this decision's own text; the frozen Company
Intelligence schema; the 1.8x leverage cap and 30% buffer floor; `PI-0031`, `PI-0032`, and `PI-0033`'s
own substance and `status: Accepted`, unedited; `OPS-0006`'s Milestone 4-9 authorization boundary;
`MARGIN-0005`'s research charter and trial ceiling.

**No audit, no closure determination, and no factual synchronization has been performed by this
filing.** The later implementation unit authorized in §3 may begin only after this decision itself
merges under the full review and acceptance discipline in §8/§11, and even a fully successful
implementation unit does not itself complete Milestone 3 or authorize Milestone 4 — a separate, later,
explicit completion determination against `PI-0031` §K's seven criteria remains mandatory, exactly as
§4 states.
