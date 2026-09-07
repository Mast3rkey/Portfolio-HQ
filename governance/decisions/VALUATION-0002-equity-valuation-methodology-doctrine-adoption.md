---
decision_id: VALUATION-0002
date: 2026-08-08
status: Proposed
category: valuation_methodology_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0005, VALUATION-0001, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: research/equity_valuation_study/METHODOLOGY_EVALUATION_REPORT.md
file: governance/decisions/VALUATION-0002-equity-valuation-methodology-doctrine-adoption.md
---

## Context

### Authority for this unit

`research/equity_valuation_study/PROTOCOL_V1.md` §15 states the study's own output is "a
**prerequisite research input** to, never itself, a resolution of `TIER-0009` §K's identified gap,"
and that methodology selection/adoption "remains its own, separate, later, explicitly authorized
governance decision." `governance/decisions/VALUATION-0001-equity-valuation-research-charter.md` §5
restates this identically: a completed report "is a **research input only**, requiring its own
separate, later, independently reviewed and principal-accepted governance decision before any
methodology is selected, adopted, or applied to a real company." This filing is that decision —
bounded, per the same §5 sentence's own two-part structure, to *methodology selection/adoption as
doctrine*. It explicitly does not reach the second, distinct step that same sentence names —
"applied to a real company" — which remains its own further, separately authorized future unit (§6
below).

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` fetched; local branch
  `claude/valuation-methodology-adoption-sdiaof` confirmed identical to `origin/main` at
  `5066168b681a0c720a52b61044f220e38d21ffda`, zero divergence, working tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API before any edit.
- **`VALUATION-0001` (PR #274) and its implementation report (PR #275) both independently confirmed
  merged**, full lifecycle re-verified from GitHub, not taken on the task brief's word — see §9/§10
  below for the complete, independently-reconstructed record. Notably, the task brief's expected
  review/acceptance identifiers for PR #275 were independently reproduced exactly
  (`pullrequestreview-4888768567`, `issuecomment-5226041482`, merge `5066168b...`, merge-commit CI run
  `31256665243` success) — no correction needed there. PR #274's own lifecycle was **not** supplied by
  the task brief and was independently reconstructed in full from the GitHub API (§9).
- **Protocol hash independently recomputed** from this exact working tree:
  `sha256sum research/equity_valuation_study/PROTOCOL_V1.md` →
  `2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980` — matches `VALUATION-0001` §3
  exactly, zero drift since merge.
- **`research/equity_valuation_study/METHODOLOGY_EVALUATION_REPORT.md` confirmed present and read in
  full** (562 lines) — the complete 49-cell matrix, all four RQ findings, and the limitations/
  compliance sections, not sampled.
- **`operations/WORKSTREAMS.yaml`'s `WS-0015` entry, `governance/decisions.yaml`, and this repository's
  `CLAUDE.md` Decisions Log pointer were all found stale** — each was last written while
  `VALUATION-0001`'s governance PR was still in flight (`status: proposed`, `blocker` describing an
  unreviewed PR, `last_verified_main_sha` pointing at a pre-merge commit). This filing performs the
  deferred Lane M synchronization for both merged PRs in one pass (§9–§11), following this
  repository's established convention of folding a prior unit's post-merge verification into the next
  filing that substantively touches the register, rather than opening a dedicated reconciliation PR
  for a routine, no-finding verification.
- **Full repository `pytest` baseline independently reproduced before any edit**: 3341 passed, 0
  failed, 1 pre-existing unrelated `DeprecationWarning` — exact match to both merged PRs' own claims.
- **Decision catalog independently rebuilt**: 95 decisions, 0 issues, before this filing's own new
  entry — exact match to both merged PRs' own claims.

## Decision

**This decision adopts, as governing methodology doctrine, exactly two things the merged
`METHODOLOGY_EVALUATION_REPORT.md` directly supports: (1) that future equity valuation work must use
archetype-differentiated methodology selection, never a single universal method, and (2) the report's
own false-precision-prevention specification (§6 of the report) as binding requirements on any future
company-level application. It adopts nothing else. It does not assign any real company to an
archetype, value any real company, resolve `TIER-0009` §K's `valuation_required` status on any
equity, or authorize any further research, code, or production change.**

### 1. RQ1 finding adopted: archetype-differentiated methodology selection is required doctrine

The report's RQ1 finding (§1 of the report) is adopted as governing doctrine: **no single valuation
methodology may be treated as universally applicable across the canonical equity roster.** The
report's own reasoning is not re-litigated here — it is adopted by reference, unedited: no family
resolves unqualified `defensible` against all seven archetype categories in the closed 49-cell matrix
(report §4), and several families carry structural, not merely inconvenient, incompatibilities with
specific archetypes (e.g., FCFF DCF's unlevered-cash-flow construct against financial intermediation;
earnings/FCF-yield screens' positive-earnings-base requirement against early-stage/binary-outcome
economics). A future application phase — not authorized by this decision, see §6 — must select its
methodology conditioned on a company's economic archetype, never apply one fixed method uniformly.

This is a doctrine adoption, not a restatement requiring independent re-derivation: the report's own
49-cell matrix and per-cell reasoning (§4, §4.1–§4.7) remain the authoritative source and are **bound
by reference here, not copied or re-derived** — matching this repository's own established practice
of binding later governance decisions to an earlier artifact's content rather than restating it
(`TIER-0005` binding to `TIER-0004`'s specification; `TIER-0007` binding to `TIER-0009`'s framework),
a practice adopted specifically because restatement has previously been the source of drift defects in
this repository's own governance history (e.g. `TIER-0004`'s BLOCKING finding, `CLAUDE.md`'s own
correction log). The matrix itself is not edited, extended, or re-scored by this decision.

### 2. Per-family governed role — a closed mapping rule applied to the report's own matrix, not a new score

To satisfy the requirement that each of the seven methodology families carry a governed role (never a
numeric score or ranking), this decision defines one **closed, mechanical mapping rule** from the
report's own closed four-value disposition vocabulary (`defensible` / `defensible_with_adjustment` /
`not_defensible` / `insufficient_evidence_to_determine`) to a five-value **governed-role vocabulary**,
and applies that rule — without altering a single cell's disposition — to the report's unedited §4
matrix and §4.1–§4.7 cell reasoning:

| Report disposition | Governed role |
|---|---|
| `not_defensible` | **Prohibited** for that archetype |
| `defensible_with_adjustment` | **Adjustment-required** for that archetype |
| `defensible`, and the family's own report text (protocol §4's family description, or the cell's own §4.1–§4.7 reasoning) does not characterize the family as a supplementary, cross-check, or "companion, not a replacement" role for that archetype | **Primary candidate** for that archetype |
| `defensible`, but the family's own report text explicitly characterizes it as supplementary, corroborative, or a companion to a different primary method for that archetype, even though the cell itself is rated `defensible` | **Secondary / corroborative** for that archetype |
| `insufficient_evidence_to_determine` | **Insufficient basis for adoption** for that archetype |

Zero cells in the frozen 49-cell matrix resolved `insufficient_evidence_to_determine` (report §4) —
the fifth governed role is preserved doctrine, currently unpopulated, not eliminated; it remains
available without amendment if a future charter amendment ever expands the closed family or archetype
lists into territory the current literature review does not support (protocol §9/§17).

Applying this rule — mechanically, per cell, changing no disposition — to the report's own text
produces the following **per-family governed-role summary** (archetype letters per report §3: A
asset-light platform, B capital-intensive infrastructure, C financial intermediation, D commodity/
cyclical, E early-stage/binary, F diversified/multi-segment, G mature stable compounder). This table
is a mechanical restatement of the mapping rule against unedited report content, not a new judgment —
the report's own §4.1–§4.7 prose remains the citable reasoning behind every entry:

| # | Family | Primary candidate | Secondary / corroborative | Adjustment-required | Prohibited | Insufficient basis |
|---|---|---|---|---|---|---|
| 1 | Asset-based / NAV / SOTP | F | — | B, C, D, E | A, G | — |
| 2 | FCFF DCF | A, G | — | B, D, F | C, E | — |
| 3 | FCFE DCF (DDM/excess-return for C) | A, G | — | B, C, D, F | E | — |
| 4 | Earnings / FCF-yield screens | — | G | A, B, C, D, F | E | — |
| 5 | Relative valuation / multiples | A, B | G | C, D, E, F | — | — |
| 6 | ROIC / reinvestment economics | — | B, G | A, C, D, F | E | — |
| 7 | Scenario / probability-weighted | D, E | — | A, B, C, F, G | — | — |

Two families — 4 (earnings/FCF-yield screens) and 6 (ROIC/reinvestment economics) — never reach
**primary candidate** for any archetype under this mapping, because the report's own protocol-sourced
family description states each is inherently a corroborative input rather than a standalone valuation
method (family 4: "used as a first-pass sanity check, not a substitute for a full intrinsic or
relative valuation," protocol §4 item 4; family 6: "used to assess capital-allocation quality as an
input to, not a replacement for, an intrinsic-value method," protocol §4 item 6) — this is the
report's own family-wide characterization, not an inference invented by this decision. Family 7
(scenario/probability-weighted) reaches **primary candidate** only for archetypes D and E, where the
report's own text explicitly frames it as first-order rather than supplementary ("not merely a
supplementary check," "the strongest, least-qualified fit in the entire matrix"). For every other
archetype (A, B, C, F, G), the report rates family 7 `defensible_with_adjustment`, not `defensible`
(report §4/§4.7) — under the mapping rule's own unconditional `defensible_with_adjustment` →
**Adjustment-required** row (first table above), these five cells are **adjustment-required**, not
secondary/corroborative: the mapping rule's Primary/Secondary distinction applies only to
`defensible`-rated cells, and the report's own language describing one of these five as, for example,
"a disclosed supplement to the DDM/excess-return primary method" (archetype C) names the *content of
the required adjustment* — use alongside, not instead of, a primary method — not a downgrade of its
governed role below adjustment-required. No family is unconditionally prohibited or unconditionally a
primary candidate across all seven archetypes — this table itself is the direct, mechanical expression
of the RQ1 finding adopted in §1: methodology selection remains archetype-conditioned in every case,
never flattened to a single "best method."

### 3. False-precision protections adopted as binding doctrine for any future application

The report's RQ3 specification (report §6) — elaborating protocol §10's five requirements — is adopted
as **binding doctrine on any future company-level valuation application**, not merely as an
implementation's own aspirational target. Bound by reference, unedited:

1. **Mandatory range output, never a single point.** Any future application of a `primary candidate`
   or `adjustment-required` methodology to a real company must report a low/base/high range (or the
   full disclosed scenario set, for family 7) with its governing sensitivity named explicitly — never
   a single number without its range.
2. **Mandatory, per-input, provenance-labeled assumptions ledger**, using exactly the four labels the
   report defines and no others: `market_derived`, `historically_observed`, `analyst_consensus_cited`,
   `assumed_for_illustration`. An assumption without one of these four labels is not a valid output
   under this doctrine.
3. **No fabricated precision** — output precision must be bounded by what the underlying evidence
   actually supports; a wide, honestly-disclosed range is a complete and correct output, not a defect.
4. **A first-class, company-level abstention path is mandatory** — structurally comparable to
   `TIER-0002`'s `unable_to_determine` axis and `XASSET-0002`/`XASSET-0005`'s forced-abstention
   readiness fields already in production in this repository. A future application must be able to
   report "cannot be determined from available evidence" rather than a forced numeric output.
5. **No opaque scoring or composite index, ever, under any future extension.** No machine-learning-
   derived valuation, weighted composite, or single blended "score" across methodology families is
   permitted at any point under this doctrine.

The report's four archetype-specific elaborations (report §6, final bullet list — commodity/cyclical
normalization-basis disclosure; early-stage scenario-probability-weight labeling; financial-
intermediation regulatory/credit-assumption disclosure; diversified/multi-segment per-segment range
disclosure) are likewise adopted, bound by reference to the report's own text, not restated here in
full.

### 4. RQ4 evidence-sufficiency finding — acknowledged as an open gap, not designed here

The report's RQ4 finding (report §7) — that the existing Company Intelligence schema (`docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24) structurally lacks any financial-statement, discount-rate,
peer-set, or scenario-probability field any of the seven families requires — is adopted as an
acknowledged, open doctrine gap. This decision does not design, name, or scope a new evidence category
to close it (report §7's own "Consequence" paragraph states this is "explicitly out of scope for this
protocol... and is not attempted here"; that boundary is preserved unedited). A future application
phase cannot proceed on real company data until that gap is closed by its own, separately authorized,
future governance decision.

### 5. Doctrine adoption does not create allocator-visible authority

Consistent with `PI-0003`'s original doctrine (restated at every Portfolio Intelligence phase since):
adopting a methodology-selection framework and a false-precision specification changes no allocator-
visible field, no `targets.yaml` value, and no `TIER-0009` policy-recommendation-package entry. The
doctrine adopted in §§1–4 above governs *how a future, separately authorized application phase must
be structured if and when it is authorized* — it is not itself an application, and does not by itself
license one to begin.

### 6. Boundary — adopted doctrine vs. future archetype assignment vs. future valuation execution

Three distinct steps exist in this domain, and this decision performs exactly the first:

1. **Methodology doctrine adoption (this decision).** Establishes, as governing doctrine: (a)
   archetype-differentiated selection is required (§1); (b) the per-family governed-role mapping,
   applied to the report's own unedited matrix (§2); (c) the false-precision specification, binding on
   any future application (§3); (d) the acknowledged evidence-category gap (§4).
2. **Real-company archetype-category assignment.** Assigning any canonical-roster company (or any
   other real company) to one of the seven archetype categories (report §3, protocol §5) is **not
   performed, sketched, or implied by this decision** — protocol §12 and report §8's Limitations
   section both bar this outright under the still-fully-effective `VALUATION-0001` charter. This
   remains its own separate, later, explicitly authorized unit, requiring its own governance filing
   naming the company or companies in scope, matching the first-coverage-discipline precedent this
   repository has applied to every prior Company Intelligence expansion (`PI-0003`, `PI-0005`,
   `PI-0007`, `PI-0023`–`PI-0031`, `PI-0036`).
3. **Real-company valuation execution.** Applying any methodology family — even one classified
   `primary candidate` in §2's table — to compute a fair value, price target, expected return, or any
   other quantitative output for any real company is **not performed, sketched, or implied by this
   decision**. This remains its own separate, later, explicitly authorized unit, requiring, at
   minimum: (a) step 2 above to have already occurred for the company in question; (b) the RQ4
   evidence-category gap (§4) to have been separately closed; (c) full compliance with the §3
   false-precision doctrine; and (d) its own independent review and principal acceptance before any
   output is produced, let alone treated as informing `TIER-0009`'s `valuation_required` status.

**Neither step 2 nor step 3 is authorized by this decision.** Both remain exactly as unauthorized as
`VALUATION-0001` §5 and protocol §§11.2/12/15/19 already left them.

### 7. Explicit non-authorizations (restated, not new — this decision creates none of the following)

This decision does not authorize, and creates no basis for inferring authorization of:

- Any archetype-category assignment of any real, named canonical-roster company, or any other real
  company (§6.2).
- Any valuation, fair value, price target, or expected return for any real company (§6.3).
- Any resolution, closure, or narrowing of `TIER-0009` §K's `target_and_range`/
  `maximum_position_size` `valuation_required` status on any of the 27 canonical equities.
- Any target, tier, holdings, gate, cap, cluster, or allocator change of any kind.
- Any chart, technical-indicator, or screenshot-derived input to any part of this doctrine or any
  future application of it (`TIER-0003`'s fundamentals-only boundary is restated, not reopened).
- Any Company/Theme/relationship/classification/reconciliation/recommendation Intelligence record
  creation or edit.
- Any ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content — equity only, per `XASSET-0001` §C/§D, unaffected and unaddressed here.
- Any new research, backtest, or protocol amendment — `PROTOCOL_V1.md` is not edited, extended, or
  reinterpreted by this decision (§8 below); the pinned hash is unchanged.
- Any margin, ladder, brokerage, order, or trade action of any kind.
- Any code, allocator, dashboard, or production-file change of any kind.

### 8. `PROTOCOL_V1.md` and the merged report are preserved unedited

This decision does not touch `research/equity_valuation_study/PROTOCOL_V1.md` or
`research/equity_valuation_study/METHODOLOGY_EVALUATION_REPORT.md`. No protocol amendment is
necessary or performed — this decision adopts doctrine from the report's already-produced,
already-reviewed findings (§§1–4 above), which is precisely the "own, separate, later, explicitly
authorized governance decision" both the protocol (§15) and `VALUATION-0001` (§5) anticipated as the
report's intended next step, not a change to the study's own frozen design. The pinned hash
(`2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980`) is independently reconfirmed
unchanged as of this filing (§ Context, Preflight).

### 9. Lane M — PR #274 (`VALUATION-0001` governance charter) lifecycle, independently reconstructed

Not supplied by the task brief; independently reconstructed in full via the GitHub API this session:

- PR #274, "VALUATION-0001: equity valuation and economic-assessment research charter," base `main` @
  `1921864326f2cc75609b1c91037c24e333c4e3d0`.
- First independent exact-head review: `pullrequestreview-4888034268`, anchored to head
  `be2ca335435a750c5f2359a8c7035274826ea203` — **CHANGES REQUIRED**, 0 BLOCKING / 0 MAJOR / 1 MINOR / 1
  non-actionable NOTE. The MINOR: protocol §6's evidence-boundary clause carried a parenthetical
  mis-attaching a structural-read carve-out for `targets.yaml`/`holdings.yaml`/`gates.yaml`/
  `issuer_lookthrough.yaml` to RQ4, which is defined solely in terms of the Company Intelligence
  schema.
- Bounded correction: commit `69966164d01f038d75bbe9b3d86f93e5ce6ceb36` (`issuecomment-5224700359`) —
  removed the ambiguous parenthetical, stated the four production files are barred outright including
  structure, re-pinned the protocol hash (`80aee45d...` → `2948e4a8...`), appended a `### Correction
  history` section to the decision file. Scoped to exactly 2 files.
- Corrected-head delta review: `pullrequestreview-4888414235`, anchored to
  `69966164d01f038d75bbe9b3d86f93e5ce6ceb36` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0
  BLOCKING / 0 MAJOR / 0 MINOR / 0 new NOTE (the prior review's one non-actionable NOTE — directional
  framing in the archetype descriptions — carried forward unresolved, explicitly non-blocking).
- Principal acceptance: `issuecomment-5225166375`, at exact head
  `69966164d01f038d75bbe9b3d86f93e5ce6ceb36`.
- Merge: `2f47adeafc9703e4074f07951df2a15a407fdc8b`, parents `1921864326f2cc75609b1c91037c24e333c4e3d0`
  and `69966164d01f038d75bbe9b3d86f93e5ce6ceb36` (independently re-confirmed via `git show`; merge-tree
  confirmed byte-identical to the accepted head's own tree via `git diff` — zero drift at merge).
- Merge-commit CI: run `31246702088`, job `93076401495`, `status: completed`/`conclusion: success` (all
  10 steps green, including "Run test suite").

### 10. Lane M — PR #275 (implementation report) lifecycle, independently reconfirmed

Independently reconfirmed via the GitHub API this session (the task brief's expected values were
verified exact, not merely copied):

- PR #275, "VALUATION-0001: equity valuation methodology evaluation report (first implementation
  unit)," base `main` @ `2f47adeafc9703e4074f07951df2a15a407fdc8b`, head
  `728521ad9fd4adc711f96818275331f0a0035adf`, exactly 1 changed file (+562/-0), 1 commit.
- Independent exact-head review: `pullrequestreview-4888768567`, anchored to head
  `728521ad9fd4adc711f96818275331f0a0035adf` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0
  BLOCKING / 0 MAJOR / 0 MINOR / 4 non-actionable NOTE (submitted as a `COMMENT`-type GitHub review due
  to the same-account self-approval platform restriction, disclosed in the review itself as not a
  substantive downgrade). No correction cycle was required.
- Principal acceptance: `issuecomment-5226041482`, at exact head
  `728521ad9fd4adc711f96818275331f0a0035adf`.
- Merge: `5066168b681a0c720a52b61044f220e38d21ffda`, parents
  `2f47adeafc9703e4074f07951df2a15a407fdc8b` and `728521ad9fd4adc711f96818275331f0a0035adf`
  (independently re-confirmed via `git show`; merge-tree confirmed byte-identical to the accepted
  head's own tree via `git diff` — zero drift at merge).
- Merge-commit CI: run `31256665243`, `status: completed`/`conclusion: success`.

Neither PR's own decision-file/index `status: Proposed` is corrected by this filing — both remain a
known, pre-existing, out-of-scope state matching this repository's established two-step
acceptance-recording pattern (`CHART-0001`, `CHART-0002`, `REL-0002`–`REL-0006`, `TIER-0005`,
`TIER-0007`, `TIER-0009`, `TIER-0011`, and now `VALUATION-0001` itself).

### 11. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0015` entry receives the following, additive only — no existing
milestone's own text is edited:

1. A new `valuation0001-governance-pr-merged` gate recording §9's PR #274 facts (superseding, by
   addition not edit, the stale `governance-pr-drafted` gate's implicit "not yet merged" state — that
   gate's own text is left byte-unedited).
2. A new `valuation0001-implementation-report-merged` gate recording §10's PR #275 facts.
3. A new `valuation0002-methodology-doctrine-adoption` gate (`status: in_progress`, `pr: null` — this
   filing does not mark its own unmerged work complete, matching every prior filing's identical
   self-reference discipline in this repository).
4. `status` updated `proposed` → `proposed` (unchanged — doctrine adoption alone does not complete
   `WS-0015`'s own broader charter-and-doctrine objective; a future application-phase authorization,
   if any, remains a separate later step). `priority` remains `secondary`. `dependencies` remains `[]`.
5. `active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`, `blocker`,
   `next_action`, and `authorized_by` updated to this filing's own live state.

No other workstream entry is touched. `WS-0005` and `WS-0014` are unaffected.

### 12. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0002-equity-valuation-methodology-doctrine-adoption.md` (this
   file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0002`).
3. `operations/WORKSTREAMS.yaml` (§11 above).
4. `CLAUDE.md` (one Decisions Log pointer entry).
5. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 95 → 96).

**No other file is touched.** No production code, no `backtest_*.py` script, no dashboard code, no
`holdings.yaml`/`targets.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`, no Intelligence or freshness
content, no Constitution text, no `research/equity_valuation_study/**` file.

### 13. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (`OPS-0009` Lane G — a new governance authorization narrowing no
prior authority but establishing new adopted doctrine, full weight, never reduced), complete any
required bounded correction and exact-head re-review, and receive explicit principal acceptance before
it may be marked ready or merged. **This decision does not mark itself ready and does not authorize
its own merge.** Nothing in §§1–12 above becomes effective, and no future application-phase step may
be proposed as though this doctrine were adopted, until this PR merges to `main`.

## Rationale

**Why adopt doctrine now, rather than waiting for a combined "adoption + application" filing.**
Splitting adoption from application matches this repository's own established discipline of narrow,
separately-authorized units at every layer of the Portfolio Intelligence, relationship-mapping, and
classification programs (`PI-0003` before `PI-0005`; `TIER-0001`/`TIER-0002` design before `TIER-0005`
authorization before the Milestone 6 implementation; `REL-0001` schema-freeze before `REL-0002`
content). Combining adoption with a real company's archetype assignment and valuation in one filing
would repeat exactly the risk `OPS-0006` §2/§3's zero-based discipline and this study's own protocol
§§3/6/12 were built to prevent — treating a still-abstract framework as though it already had a
concrete, evidenced application ready to go, when the RQ4 evidence-category gap (§4) has not been
closed and no company has been screened for archetype fit under any process.

**Why a mapping rule rather than restating the 49-cell matrix.** The report's own matrix (§4) is
already the authoritative, independently-reviewed, citable source (`pullrequestreview-4888768567`
confirmed zero mismatches across all 49 cells between the summary table and per-cell prose). Copying
it into this decision file would create a second copy that could drift from the original under a
future correction to either document — exactly the class of defect `TIER-0004`'s own BLOCKING finding
demonstrated is a live risk in this repository, not a hypothetical one. A closed, three-line mapping
rule applied mechanically to the unedited original avoids that risk while still satisfying the
requirement that each family carry an explicit, non-numeric governed role.

**Why `category: valuation_methodology_governance`, not `research_charter`.** `VALUATION-0001` itself
is correctly categorized `research_charter` (matching `MARGIN-0005`/`LADDER-0001`'s own charter
category). This filing is not a charter — it adopts doctrine from a charter's completed output. This
mirrors the precedent set when `TIER-0001` (the first Milestone-5 design filing, itself a "define,
then later authorize" unit much like this one) established `tier_classification_governance` as its
own category distinct from the `research_charter`/`portfolio_intelligence` categories used elsewhere
in the same governance history, rather than reusing an adjacent category for a decision that plays a
structurally different role.

**Why RQ4's gap is acknowledged, not closed.** Designing a new evidence-category schema is exactly the
kind of implementation work `governance/decisions/README.md`'s own convention, and this repository's
consistent "define, then later authorize implementation" pattern throughout the Company/Theme/
relationship/classification/reconciliation/recommendation Intelligence programs, treats as its own
separate, bounded unit — never folded into the filing that first identifies the need for it.

## Alternatives Considered

- **Adopt a single "best" methodology family instead of an archetype-conditioned set.** Rejected
  outright — the report's own RQ1 finding (§1 of the report, independently reconfirmed in this
  filing's own preflight) establishes that no family is unqualified-`defensible` across all seven
  archetypes; forcing a single winner would directly contradict the report this decision is adopting
  and would repeat the exact "forcing a single mechanism where the evidence does not support one"
  error CLAUDE.md's Guardrails and this repository's Decisions Log (e.g. the band-overlay backtest,
  the regime/trend-gate closures) have consistently rejected.
- **Fold this adoption into a combined filing that also assigns one illustrative company to an
  archetype, "just to show the doctrine works."** Rejected — protocol §12 and report §8 both bar any
  archetype-category assignment of a real company under this charter's authority, "including as a
  'worked example' or 'illustrative application'"; doing so here would violate the still-fully-
  effective `VALUATION-0001` charter this decision operates under, not merely be premature.
  §6 preserves this as its own future, separately authorized step.
- **Wait for RQ4's evidence-category gap to be closed before adopting any doctrine at all.** Rejected
  as unnecessarily conservative — the RQ1 archetype-differentiation finding and the RQ3 false-
  precision specification are both independently actionable doctrine regardless of whether a
  quantitative evidence category exists yet; adopting them now establishes the governing rules a
  future evidence-category design and a future application phase must both conform to, rather than
  leaving that design underspecified until it is separately proposed.
- **Have this filing itself design the RQ4 evidence-category gap's replacement schema.** Rejected —
  outside this filing's own bounded scope (§12); schema design for a new Intelligence-adjacent
  evidence category is its own implementation unit requiring its own review, matching every prior
  Intelligence-schema design decision in this repository's history.

## Consequences

**What changes.** Going forward, any future proposal to apply a valuation methodology to a real
company must (a) select its methodology conditioned on the company's archetype fit, per §2's table and
the report's own matrix, never apply one method uniformly; (b) comply in full with §3's false-
precision doctrine (range output, four-label provenance ledger, no fabricated precision, mandatory
abstention path, no opaque scoring); and (c) separately close the RQ4 evidence-category gap (§4) and
obtain its own archetype-assignment authorization (§6.2) before any valuation execution (§6.3) may
even be proposed. `WS-0015`'s register entry now reflects both merged PRs and this filing's own
doctrine-adoption step.

**What does not change.** No real company has been assigned to an archetype. No real company has been
valued. `TIER-0009` §K's `target_and_range`/`maximum_position_size` `valuation_required` status is
unchanged on all 27 canonical equities. No target, tier, holdings, gate, cap, cluster, allocator,
margin, or ladder value changes. No Company/Theme/relationship/classification/reconciliation/
recommendation Intelligence record changes. `PROTOCOL_V1.md` and `METHODOLOGY_EVALUATION_REPORT.md`
are both unedited. No ETF, crypto, GLD, cash/reserve, or debt-reduction valuation content is created.
No brokerage, order, or trade action of any kind occurs or is authorized. `WS-0005`, `WS-0014`, and
every other workstream are unaffected.
