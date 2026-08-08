---
decision_id: VALUATION-0004
date: 2026-08-08
status: Proposed
category: valuation_evidence_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0002, XASSET-0005, VALUATION-0001, VALUATION-0002, VALUATION-0003, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/VALUATION-0004-rq4-evidence-architecture-governance.md
---

## Context

### Authority for this unit

`governance/decisions/VALUATION-0002-equity-valuation-methodology-doctrine-adoption.md` §4 adopts the
report's RQ4 finding as an "acknowledged, open doctrine gap" and states explicitly: "This decision
does not design, name, or scope a new evidence category to close it... A future application phase
cannot proceed on real company data until that gap is closed by its own, separately authorized,
future governance decision." `VALUATION-0002` §6.3 restates the same boundary as a precondition on
real-company valuation execution: that execution requires, at minimum, "(b) the RQ4 evidence-category
gap (§4) to have been separately closed." `governance/decisions/VALUATION-0003-equity-valuation-
archetype-assignment-authorization.md` §L restates the identical non-authorization ("RQ4
evidence-category schema design — remains its own separate, later, explicitly authorized unit
(`VALUATION-0002` §4/§6.3)") and its Rationale independently confirms archetype assignment and RQ4
evidence-category design answer two different evidence questions that must not be conflated. This
filing is that separate, later, explicitly authorized unit — for the design/authorization step only,
per §K below.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` fetched; local branch
  `claude/valuation-0004-evidence-governance-noucj9` confirmed identical to `origin/main` at
  `a8dfd0d1f30eb9d5759f874de1932bb49da98385`, zero divergence, working tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API before any edit — no competing active
  mutation lane.
- **PR #279 (`VALUATION-0003`-authorized archetype-assignment implementation) independently
  reconfirmed merged**, full lifecycle re-verified from GitHub, not taken on the task brief's word —
  see §M below for the complete, independently-reconstructed record, including the corrected final
  archetype distribution and evidence-quality figures (which differ from the pre-correction figures
  still recorded in `operations/WORKSTREAMS.yaml`'s existing `valuation0003-archetype-assignment-
  implementation` gate — corrected additively in §N, that gate's own text left byte-unedited).
- **A read-only completion-determination review, independently re-run this session, confirmed no
  dedicated `VALUATION-0003` retrospective completion filing is required** before proceeding: unlike
  `WS-0005`'s numbered-milestone chain (`PI-0031`→`PI-0037`, `REL-0001`→`REL-0006`, `TIER-0007`→
  `TIER-0008`, `TIER-0009`→`TIER-0010`, each pairing an authorization/implementation with its own
  dedicated completion-determination decision), `WS-0015`'s `VALUATION-####` chain is a sequential,
  non-milestone research-and-doctrine program (charter → report → doctrine adoption → archetype
  authorization → archetype implementation → this filing), and this repository's own established
  practice for that shape (`XASSET-0002`→`XASSET-0003`→`XASSET-0004`→`XASSET-0005`, `CHART-0001`→
  `CHART-0002`) folds each prior unit's post-merge Lane M facts forward into the next substantive
  filing rather than opening a dedicated retrospective decision for a routine, no-finding
  verification. This filing performs that fold (§M/§N).
- **`research/equity_valuation_study/PROTOCOL_V1.md` and `METHODOLOGY_EVALUATION_REPORT.md` read in
  full this session** — RQ4's finding (report §7) and its own stated boundary ("designing that
  evidence category is explicitly out of scope for this protocol... and is not attempted here; this
  finding only identifies that the gap exists and characterizes its shape") independently reconfirmed
  unedited. Protocol hash independently recomputed:
  `sha256sum research/equity_valuation_study/PROTOCOL_V1.md` →
  `2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980` — matches `VALUATION-0001` §3
  exactly, zero drift.
- **`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24 read this session** to confirm the frozen Company
  Intelligence schema's own field list structurally lacks every quantitative category this filing
  governs (§9's field list is narrative/qualitative only: `sector`, `industry`, `competitive_
  advantages[]`, `risks[]`, `catalysts[]`, `conviction`, `portfolio_role_ref`, `review` — no financial-
  statement, discount-rate, peer-set, or scenario field anywhere), confirming RQ4's finding remains
  accurate and that this filing's companion architecture cannot be satisfied by extending that frozen
  schema (§20's explicit prohibitions independently reconfirmed unaffected by anything in this filing).
- **`operations/WORKSTREAMS.yaml`'s `WS-0015` entry found stale**: `active_branch`/`active_pr` point at
  PR #279's own branch/number, and the `valuation0003-archetype-assignment-implementation` gate's own
  description still carries the pre-correction archetype distribution (`A:6 B:5 C:2 D:3 E:1 F:8 G:2`)
  superseded by the correction described in PR #279's own bounded-correction section. This filing
  performs the deferred Lane M synchronization (§M/§N), additively, without editing that gate's own
  text.
- **Full repository `pytest` baseline independently reproduced before any edit**: 3524 passed, 0
  failed, 1 pre-existing unrelated `DeprecationWarning` — exact match to PR #279's own final claim.
- **Decision catalog independently rebuilt**: 97 decisions, 0 issues, before this filing's own new
  entry.
- **Zero `intelligence/valuation_evidence/` (or similarly named) directory exists anywhere in the
  repository** at this commit — confirmed by direct filesystem search. No prior filing has proposed,
  named, or scoped a quantitative evidence category.

## Decision

**This decision governs the structure and rules for a new, separate, roster-agnostic quantitative
valuation-evidence architecture — closing RQ4's identified gap at the governance-design level — and
authorizes exactly one future, separate, bounded implementation PR to build the schema, its validator,
and its test suite as an empty/scaffold structure. It does not populate any real company's quantitative
evidence, perform any valuation, or authorize valuation execution. Implementation does not begin in
this session.**

### A. What is authorized

One future, separate, bounded implementation PR that creates: (1) the schema structure defined in §C–§J
below as a companion evidence architecture, roster-agnostic and reusable for the current 27 canonical
equities, the 26 already-researched non-canonical Company Intelligence contenders, and any future
equity contender; (2) a dedicated validator enforcing that structure and every false-precision/
provenance rule in §E/§F; (3) that validator's focused test suite; and, at most, an empty or synthetic-
fixture-only scaffold state — **no real company's quantitative evidence file is created or populated
by that implementation PR** (§P). That future PR requires its own full independent-review/correction/
re-review/principal-acceptance/merge/post-merge-verification lifecycle under `OPS-0007` §1 / `OPS-0009`
Lane G before any of it is authoritative. Nothing in §§B–L below is itself a schema, a validator, or a
populated record — this filing specifies what a later implementation must build.

### B. Companion architecture — a new evidence layer, not an amendment to Company Intelligence

The new evidence category lives in its own directory, filesystem-is-the-index, matching this
repository's established convention for a structured-judgment-record axis (`intelligence/
classification/`, `intelligence/etf_classification/`, `intelligence/crypto_classification/`,
`intelligence/valuation_archetype/` — single-YAML-per-ticker, not the paired-YAML+Markdown Company
Intelligence convention, since this is structured quantitative evidence, not a narrative thesis
document): **`intelligence/valuation_evidence/<TICKER>.yaml`**, plus one `COHORT_MANIFEST.yaml`.

**The frozen Company Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24) is not
modified, extended, or reinterpreted by this decision or by the future implementation it authorizes.**
RQ4's own finding (report §7) already establishes why: that schema's field list is deliberately
narrative/qualitative (business-model thesis, risks, catalysts, competitive advantages) and any
attempt to bolt structured, dated, per-period financial figures onto it would either violate §20's
explicit prohibitions or force a schema redesign this filing has no authority to perform (`PI-0001`'s
freeze, restated at every subsequent Portfolio Intelligence phase, remains fully controlling and
untouched). The new layer is additive and one-way-referencing only: a `valuation_evidence` record may
cite a `TICKER` that also carries a Company Intelligence record, a Milestone 6 classification record,
and a `valuation_archetype` record, but none of those records reference or depend on the new evidence
layer, and the new layer never writes to, or is written to by, any of them.

**Roster-agnostic by design, populated by nobody under this filing.** The schema itself carries no
population restriction to the 27 canonical equities — it must be equally usable, without modification,
for any of the 26 researched non-canonical Company Intelligence contenders (`PI-0032`/`PI-0033`'s own
roster) or any future equity contender the `CONTENDER-####` registry (`WS-0014` item 1) identifies.
This filing authorizes **zero population of any ticker under any circumstance** (§P) — roster-
agnosticism is a structural design requirement on the schema, not an authorization to populate beyond
the 27.

### C. Minimum evidence domains the schema must represent

The future implementation's schema must be capable of representing, within one reusable structure
(never seven archetype-specific schemas), at minimum:

1. Financial-statement history (income statement, cash-flow statement, balance sheet line items) as a
   dated, period-indexed series.
2. Revenue, earnings, and free-cash-flow evidence.
3. Margin evidence (gross, operating, net, or segment-level as disclosed).
4. Capital expenditure, reinvestment, and capital-intensity evidence.
5. Invested-capital and return-on-invested-capital-related evidence.
6. Balance-sheet evidence (assets, liabilities, equity as disclosed).
7. Cash, debt, and net-debt evidence.
8. Share-count and dilution evidence (basic, diluted, and any disclosed dilutive-instrument detail).
9. Segment-level economic evidence (§H below).
10. A structural distinction between **reported** and **derived** values, on every individual figure —
    never only at the record level.
11. A structural distinction between **annual, quarterly, and trailing-twelve-month (TTM)** periods.
12. **As-of** and **fiscal-period** dates, kept structurally distinct from the record's own review/
    citation/`sealed_at` dates (RQ4's own gap: the frozen Company Intelligence schema has no field for
    this distinction at all).
13. Restatement state (whether a given period's figures have been restated, and from what).
14. Market-observed inputs intended for later use by a valuation methodology (e.g., an observed share
    price or trading-derived figure) — evidence only, never a computed valuation output.
15. Discount-rate components as individually sourced inputs, never a single opaque rate (§I).
16. Peer-set evidence and its provenance (§J).
17. Scenario-variable evidence (§K).
18. Provenance and uncertainty on every quantitative fact.
19. Disclosed evidence conflicts — never silently reconciled.
20. Unavailable or insufficient evidence — a first-class abstention, never a fabricated figure.

**No actual company value is chosen, described, or implied anywhere in this decision.** Every domain
above is a structural capability requirement on the future schema, not a populated example.

### D. Archetype / methodology compatibility — bound by reference, not restated

The schema must be capable of supplying the evidence categories each of the seven methodology families
`VALUATION-0002` §2 requires for its governed role against each of the seven archetype categories
(protocol §5, bound by reference — not restated here): asset-based/NAV/SOTP evidence (§C.6, §C.9);
FCFF/FCFE DCF evidence (§C.1–§C.4, §I); earnings/FCF-yield evidence (§C.2); relative-valuation/
multiples evidence (§J); ROIC/reinvestment evidence (§C.5, §C.4); and scenario/probability-weighted
evidence (§K). This decision does not perform, re-derive, or restate `VALUATION-0002` §2's per-family
governed-role table or the report's own 49-cell matrix (report §4) — it is cited by reference only, to
confirm the evidence domains in §C are sufficient in kind (not in populated content) to support every
`primary candidate` and `adjustment-required` cell that table identifies. **This decision performs no
valuation of any kind and selects no methodology for any company** — it governs evidence structure
only.

### E. False-precision controls adopted into evidence governance

`VALUATION-0002` §3's false-precision doctrine is adopted here, unedited, as binding on the evidence
layer specifically (not merely on a future application's final output, which §3 already covers):

1. Every dated/as-of input must carry its own as-of date (§C.12) — no undated figure is a valid
   evidence entry.
2. Every quantitative fact must carry source provenance (§F) — no unsourced figure is a valid evidence
   entry.
3. Every fact must be marked **reported** or **derived** (§C.10) — a derived value with no `reported`
   counterpart requires a disclosed derivation method; an unmarked value is invalid.
4. Derived values require a disclosed derivation note stating the method and inputs used to derive
   them — a derived figure with no derivation disclosure is invalid.
5. Conflicting evidence (e.g., two sources disclosing different figures for the same period and line
   item) must be disclosed as a conflict, never silently resolved in one direction (matching this
   repository's established practice, e.g. `VWO`'s disclosed China-weight conflict in `XASSET-0003`'s
   implementation, and `VALUATION-0003` §H's identical `disclosed_evidence_conflicts` requirement for
   the archetype layer).
6. Stale values must be flagged as such — the validator must compute or verify a staleness signal
   relative to each fact's own as-of date and the record's own freshness state (structurally comparable
   to this repository's existing `intelligence_report.collect_staleness_findings` discipline, reused by
   pattern, not by import coupling).
7. Unavailable or insufficient data produces a first-class abstention on the affected evidence domain —
   never a fabricated figure, never a forced non-null value where the honest state is "not available."
8. Scenario probabilities, wherever they eventually appear in a populated record, require an explicit
   provenance label from the closed four-value vocabulary (§F.2) — this decision does not itself assign
   any probability to any scenario for any company (§K, §P).
9. **No single opaque discount-rate field.** The schema must decompose a discount-rate estimate into its
   individually sourced components (§I) — never one unexplained number.
10. **No unsupported point precision.** Any populated numeric evidence field must carry precision no
    finer than its own source actually supports — this decision does not invent a numeric rounding or
    significant-figure rule beyond that principle; a specific rounding/precision convention, if one is
    ever needed, is a future implementation detail bound by this principle, not a threshold this filing
    invents without authority (matching `NUM-0001`'s own discipline against unsupported numeric
    parameters).

### F. Provenance vocabulary — reused, not invented

1. **Source provenance**, reusing exactly this repository's own existing, live vocabulary
   (`etf_classification_validator.py`/`crypto_classification_validator.py`, independently confirmed
   this session): `source_type` — `primary` or `secondary`; `access_status` — `directly_inspected`,
   `consulted_via_search_aggregation`, or `attempted_not_directly_inspected`. No new source-provenance
   vocabulary is invented; the future implementation must reuse these exact string values.
2. **Assumption/scenario provenance**, reusing exactly `VALUATION-0002` §3's own four-label vocabulary,
   unedited: `market_derived`, `historically_observed`, `analyst_consensus_cited`,
   `assumed_for_illustration`. This extends `NUM-0001`'s existing provenance-classification discipline
   into this new domain, matching `VALUATION-0002` §3's own stated extension — not a fifth, sixth, or
   renamed label.
3. Every discount-rate component (§I), peer-set entry (§J), and scenario variable (§K) must carry one
   of the four §F.2 labels; every raw financial-statement or market-observed fact (§C.1–§C.14) must
   carry the §F.1 `source_type`/`access_status` pair. The two vocabularies serve different evidence
   classes and are not interchangeable.

### G. Source hierarchy — governance principles, not company data

The future implementation's evidence-sourcing discipline must distinguish, at minimum, the following
source classes in descending reliability order, with honest fallback disclosure required at every step
(never silent substitution of a lower-reliability source for a higher one without disclosure):

1. Company/regulatory primary filings (e.g., SEC 10-K/10-Q/8-K or the equivalent non-U.S. regulatory
   filing).
2. Company earnings releases and investor presentations.
3. Market and regulatory data (e.g., observable market prices, published regulatory/rate data).
4. Secondary aggregators (financial-data platforms, news aggregation).
5. Analyst/consensus data, explicitly labeled as such (never presented as company-disclosed fact).

**This decision does not create a "primary-only or abstain forever" rule.** Matching this repository's
own extensively disclosed history of primary-source access failures (Company Intelligence, Milestone 6,
ETF/crypto classification, the archetype layer itself), a future population phase must be permitted to
fall back to a lower-reliability source class **with honest, explicit disclosure of that fallback and
its `access_status`** — never blocked outright from recording any evidence at all merely because a
primary source was unreachable. What is prohibited is presenting a lower-reliability source's content
as though it carried a higher source class's provenance label.

### H. Time-series requirement — no invented minimum length

The schema must structurally support **multiple periods** per company (§C.11) — a single-period record
would not satisfy any of the seven methodology families' own data requirements (report §5's table). This
decision does **not** invent a hard minimum number of historical periods (e.g., "at least five years"),
because no existing repository authority (protocol, `VALUATION-0001`/`0002`/`0003`, `NUM-0001`) sets one
for this domain, and inventing one here would itself be exactly the kind of unsupported numeric
parameter `NUM-0001`'s provenance-classification discipline exists to prevent. **Minimum-history-length
policy is left to the future population authorization** (§P) — the schema/validator implementation
authorized here must support an arbitrary number of periods (including zero, structurally, pending an
abstention) without hardcoding a minimum, and any future population-phase authorization may set its own
minimum with its own disclosed justification at that time.

### I. Discount-rate evidence — separated from discount-rate policy

Evidence and methodology policy are kept structurally separate. The schema may store **sourced,
individually-provenanced inputs**, at minimum: a risk-free-rate observation; cost-of-debt evidence;
tax-rate data (effective and/or statutory, disclosed as such); capital-structure facts (observed
debt/equity mix); and a beta observation, structurally present but explicitly conditional — usable only
once a future methodology-application decision defines its estimation window and reference index (this
filing does not define one). **This decision does not decide**, and the future implementation may not
decide on this filing's authority: the actual equity-risk-premium value to use, the beta estimation
window or reference index, the exact WACC computation policy, or the capital-structure weighting
convention. Those remain later, separately authorized application-phase policy decisions — this filing
governs only that the underlying inputs have a structural home, each individually sourced and
provenance-labeled (§F), never pre-combined into a single opaque discount-rate figure (§E.9).

### J. Peer-set evidence — structure only, no peers selected

The schema must support, per company: a list of peer **candidates** (identity only — ticker or company
name); a comparability rationale for each candidate; source provenance (§F.1) and an as-of date for
each; an explicit inclusion or exclusion status per candidate with its own rationale; and a first-class
abstention (**no valid peer set could be identified**) when no defensible comparable set exists. **This
decision selects no peer for any company** — the structure exists so a future, separately authorized
population phase can record peer-set evidence and its reasoning transparently, not so this filing can
pre-select comparators.

### K. Scenario evidence — structure only, no probabilities assigned

The schema must support, per company: named scenario variables and their evidence basis; a provenance
label from the closed §F.2 four-value vocabulary for every scenario input; and an explicit "unable to
determine a defensible scenario set" abstention. Consistent with `VALUATION-0002` §3's own RQ3
elaboration for archetype E ("every scenario's probability weight must itself carry a provenance
label... an undisclosed or unlabeled probability weight reintroduces exactly the false precision this
specification exists to prevent"), the schema's scenario-probability field, wherever the future
implementation places it, must be structurally present but is **not populated with any value for any
company by this decision or by the schema/validator implementation it authorizes** (§P) — assigning an
actual probability weight to an actual scenario for an actual company is real-company valuation-relevant
judgment, not scaffold structure, and remains its own future, separately authorized population/
application step.

### L. Segment / sum-of-the-parts (SOTP) evidence — structure only, no SOTP performed

The schema must support, per company, a list of disclosed business segments, each carrying: segment-
level revenue, profit, and cash-flow evidence where disclosed; shared or unallocated cost evidence;
intersegment-elimination evidence; and a segment-level abstention (**segment data unavailable or
insufficiently granular**) where a company does not disclose segment-level detail adequate to populate
the above. This directly supports `VALUATION-0002` §3's own archetype-F elaboration ("a segment-level
sum-of-the-parts output must disclose each segment's own range and assumptions ledger separately") for
a future application phase — **this decision performs no sum-of-the-parts valuation of any kind for any
company.**

### M. Lane M — PR #279 (`VALUATION-0003`-authorized archetype-assignment implementation) lifecycle,
independently re-verified and recorded

Independently re-verified via the GitHub API this session, not assumed:

- PR #279, "WS-0005/WS-0015: VALUATION-0003 archetype assignment for all 27 canonical equities," base
  `main` @ `0d0252021ded7f18a44c8688148606c9ee39fad4`, head
  `7d9634c6d8c1d455cd24ed769574605dbec302e7`, 35 changed files, 3 commits.
- Original independent exact-head review: `pullrequestreview-4889352085`, anchored to head
  `8dc8250c577713f946834bd16bf57df442cccad4` — **CHANGES REQUIRED**, 0 BLOCKING / 4 MAJOR / 5 MINOR / 5
  NOTE, targeting substantive archetype-judgment quality (ASML primary/secondary ordering, RKLB's
  unmentioned Iridium acquisition, SPGI's secondary-C fit against protocol §5's literal definition,
  and cross-shard evidence-quality-tier inconsistency), not mechanics (which the same review
  independently verified clean: live PR/CI state, 35-file inventory with zero protected-path touches,
  full `pytest`, all 9 pre-existing validators plus the new `valuation_archetype_validator.py`, 183/183
  new tests, and two independently-implemented leak scanners both returning zero leaks).
- Bounded correction: commit `7d9634c6d8c1d455cd24ed769574605dbec302e7` — reordered ASML's primary/
  secondary (D/B → B/D) grounded in the ticker's own permitted `risks[]` evidence; added RKLB's Iridium
  disclosure to its rationale/archetype-F test; reordered SPGI's secondary (C → A) against protocol §5's
  literal archetype-C definition; removed three unsupported secondaries (KLAC `A`, LLY `E`, GNRC `B`);
  inline-caveated WM's revenue-mix reliance; and derived/applied a documented source-access-disclosure
  rule recalibrating evidence quality cohort-wide.
- Corrected-head delta review: `pullrequestreview-4889412082`, anchored exactly to
  `7d9634c6d8c1d455cd24ed769574605dbec302e7` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0
  BLOCKING / 0 MAJOR / 0 MINOR surviving — independently re-verified all three MAJOR resolutions on
  their own textual merits (not merely by trusting the correction's own claim) and independently
  re-derived the corrected evidence-quality distribution.
- Principal acceptance: `issuecomment-5227655923`, at exact head
  `7d9634c6d8c1d455cd24ed769574605dbec302e7`.
- Exact-head CI: run `31271248381`, job `93137498061`, `status: completed`/`conclusion: success`.
- Merge: `a8dfd0d1f30eb9d5759f874de1932bb49da98385`, parents
  `0d0252021ded7f18a44c8688148606c9ee39fad4` and `7d9634c6d8c1d455cd24ed769574605dbec302e7`
  (independently re-confirmed via `git show`; merge-tree confirmed byte-identical to the accepted
  head's own tree — zero drift at merge, independently re-confirmed via `git diff`).
- Merge-commit CI: run `31273622505`, `status: completed`/`conclusion: success`.
- **Corrected final archetype-cohort figures, independently re-derived from the merged
  `intelligence/valuation_archetype/*.yaml` records this session, not merely copied from the PR body**:
  primary distribution `A:6 · B:6 · C:2 · D:2 · E:1 · F:8 · G:2`; secondary present on 19/27; zero
  abstentions; evidence quality `comprehensive:12 · partial:4 · limited:11 · blocked:0`.

### N. Register synchronization (Lane M, this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0015` entry receives, additive only — no existing gate's own text
edited:

1. A new `valuation0003-archetype-assignment-implementation-post-merge-verification` gate recording
   §M's independently reconfirmed PR #279 facts in full, including the corrected final distribution —
   this corrects the stale pre-correction distribution still recorded in the existing `valuation0003-
   archetype-assignment-implementation` gate's own text without editing that gate.
2. A new `valuation0004-rq4-evidence-architecture-governance` gate (`status: in_progress`, `pr: null` —
   this filing does not mark its own unmerged work complete, matching every prior filing's identical
   self-reference discipline in this repository).
3. `status` remains `proposed` (governing the RQ4 evidence architecture does not itself complete
   `WS-0015`'s own broader charter-and-doctrine objective — a future schema/validator implementation,
   and any further future application-phase authorization, remain separate later steps). `priority`
   remains `secondary`. `dependencies` remains `[]`.
4. `active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`, `blocker`,
   `next_action`, `completion_criteria`, and `authorized_by` updated to this filing's own live state.

No other workstream entry is touched. `WS-0005` and `WS-0014` are unaffected.

### O. RQ4 closure semantics — precise, staged, not conflated

Four distinct states exist in this domain. This decision reaches exactly the first:

1. **RQ4 evidence architecture governed (this decision).** Establishes, as governing design: the
   companion schema's location and roster-agnostic scope (§B); the minimum evidence domains it must
   represent (§C); its archetype/methodology-compatibility requirement, bound by reference (§D); the
   false-precision controls binding on the evidence layer (§E); the reused provenance vocabularies (§F);
   the source hierarchy (§G); the no-invented-minimum-history rule (§H); the discount-rate evidence/
   policy boundary (§I); the peer-set evidence rule (§J); the scenario evidence rule (§K); the segment/
   SOTP evidence rule (§L); and the validator contract (§Q) a future implementation must satisfy.
2. **Schema/validator/test implementation merged (a future, separate PR — not this filing).** RQ4's gap
   as `VALUATION-0002` §4 and §6.3 use the term — "the RQ4 evidence-category gap... separately
   closed" — is satisfied **only once that future implementation PR merges to `main`** with a working
   schema, a closed-schema validator, and passing tests, per §P. **This filing's own governance-design
   step does not itself satisfy `VALUATION-0002` §6.3(b)'s closure condition** — the narrower, more
   auditable reading is adopted deliberately: a design document is not evidence infrastructure a
   valuation application could actually use. Until that future PR merges, `VALUATION-0002` §6.3(b)
   remains unsatisfied for every company.
3. **Real-company evidence population (a further, separately authorized, later unit — not authorized
   by this filing or by the implementation it authorizes).** Even once state 2 is reached, no company's
   quantitative evidence exists until a future population-phase authorization is separately proposed,
   reviewed, and accepted — matching this repository's own first-coverage-discipline precedent for
   every prior Intelligence-adjacent content expansion.
4. **Valuation execution authorized (a further, separately authorized, later unit, requiring states 2
   and 3 for the company in question, plus `VALUATION-0002` §6.3(a)/(c)/(d)).** Not reached, not
   approached, not implied by this filing.

**This filing claims only state 1.** It does not claim state 2, 3, or 4 for any company, and does not
claim that satisfying state 1 shortens, narrows, or pre-commits the scope of states 2–4's own future
authorizations.

### P. Future implementation authority — bounded to schema/validator/tests, no population

The one future implementation PR this decision authorizes (§A) may create: the `intelligence/
valuation_evidence/` directory structure and its YAML schema (§B–§L); a dedicated
`valuation_evidence_validator.py` (§Q); that validator's focused test suite, using synthetic fixtures
only; and, if a scaffold artifact is structurally necessary to prove the schema round-trips (e.g., to
demonstrate the abstention path or a minimal multi-period structure), **synthetic, clearly-labeled
fixture data only, never a real company's actual figures** — the same synthetic-fixture-only
discipline this repository has already applied to every validator test suite in this program
(`classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`,
`relationship_validator.py`, `etf_classification_validator.py`, `crypto_classification_validator.py`,
`valuation_archetype_validator.py`). **That implementation PR may not create, populate, or seed any
`intelligence/valuation_evidence/<TICKER>.yaml` record for any real company — the 27 canonical
equities, the 26 researched non-canonical contenders, or any other ticker — under any circumstance.**
Real-company population requires its own separate, later, explicitly authorized unit (§O.3), matching
this repository's own bounded-scaffold-then-content precedent (`REL-0001`'s schema/taxonomy freeze
before `REL-0002`'s first content batch; `TIER-0004`'s design before `TIER-0005`'s fresh authorization
before the Milestone 6 implementation itself).

### Q. Validator contract required of the future implementation

The future implementation's `valuation_evidence_validator.py` must, at minimum:

- Enforce closed schema at every level (top-level record, each period entry, each line-item entry,
  each discount-rate component, each peer-set entry, each scenario entry, the manifest) — reject extra
  keys, not merely check for missing ones (learning directly from this repository's own disclosed
  `contender_registry_validator.py` MAJOR finding on exactly this defect class).
- Enforce strict types on every field (dates as dates, provenance labels from the closed §F.1/§F.2
  vocabularies only, `reported`/`derived` markers, boolean abstention flags).
- Require provenance (§F) on every populated quantitative fact — reject a figure with no source.
- Enforce chronological/logical date ordering where applicable (e.g., a period's `as_of_date` not
  preceding its own `fiscal_period_end_date`).
- Compute or verify a stale-state signal per §E.6, rather than trusting a self-declared flag alone —
  learning directly from `reconciliation_validator.py`'s own disclosed MINOR defense-in-depth gap (a
  self-declared boolean checked without an independent recomputation).
- Enforce the reported-vs-derived marker (§C.10/§E.3) and require a derivation note whenever a value is
  marked `derived` (§E.4).
- Require disclosure, never silent resolution, of any recorded evidence conflict (§E.5).
- Support and correctly validate the abstention path on every evidence domain (§C.20, §E.7, §H, §J, §K,
  §L) — an abstained domain must be structurally distinguishable from a populated one, matching
  `TIER-0004` §F's and `VALUATION-0003` §H's identical rule for their own abstention paths.
- Require every evidence domain the archetype/methodology-compatibility table (§D) identifies as
  necessary for at least one `primary candidate`/`adjustment-required` cell to have a structural home
  in the schema — a completeness check against `VALUATION-0002` §2's own table, not a new judgment.
- **Reject any fair-value, price-target, or expected-return output field anywhere in the schema** — an
  independently-derived free-text and key-name scan for prohibited valuation-output language, chart-
  domain terms, and directive/trading language, built as its own materially different mechanism from
  any strip/redaction logic elsewhere in the implementation (never the same function called twice, per
  `TIER-0004`'s own corrected lesson on false independence claims).
- Enforce zero coupling of any kind to `targets.yaml`, `holdings.yaml`, `gates.yaml`,
  `issuer_lookthrough.yaml`, `allocate.py`, or `margin_state.py` — zero import coupling, zero
  target/tier/gate/cap/cluster/allocator/margin field anywhere in the schema.
- Run clean against every applicable pre-existing repository validator, the full `pytest` suite,
  repo-wide YAML/YML and JSON parsing, `git diff --check`, an exact changed-file inventory, and a full
  protected-path scan (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`,
  `gates.yaml`, `issuer_lookthrough.yaml`, every existing `intelligence/**` record, `docs/
  PORTFOLIO_INTELLIGENCE_SPEC.md`, `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, every other
  `governance/decisions/*.md` — zero diff on all of them) before it may be marked ready.
- Achieve decision-catalog reconciliation and exact-head CI green before the implementation PR may be
  marked ready.

### R. Non-authority — explicit, exhaustive

This decision authorizes no:

- Fair value, price target, expected return, or upside/downside calculation for any real company.
- Actual DCF computation, actual peer selection, actual discount-rate value, or actual scenario
  probability for any real company.
- Real-company evidence population of any kind, in the schema this filing governs or any other —
  states 2 and 3 of §O are not reached by this filing.
- Resolution, closure, or narrowing of `TIER-0009` §K's `valuation_required` status on any equity.
- Target, tier, holdings, gate, capital-priority, cap, cluster, or allocator change of any kind.
- Margin policy, buy-ladder, chart ingestion, or chart interpretation of any kind.
- `CONTENDER-0003` or any further contender-registry regeneration/legacy-recovery work.
- Any ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content — remains `WS-0014`/`XASSET-0001` §C/§D's own separate, unaffected scope.
- Any overlap/concentration modeling, cross-asset synthesis, or unlevered-versus-levered allocation
  testing — remains `XASSET-0005`'s own separate, unaffected scope.
- Any order or trade.
- Any edit to `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `docs/
  PORTFOLIO_INTELLIGENCE_SPEC.md`, `VALUATION-0001`, `VALUATION-0002`, or `VALUATION-0003`.
- Any actual schema, validator, or test code — this filing authorizes a future implementation; it
  performs none of that work itself.

### S. Whole-universe boundary — restated, not narrowed

This filing is equity valuation **evidence governance** only. The 27 canonical equities carrying a
sealed `valuation_archetype` record do not define the final Portfolio-HQ contender universe: the
`CONTENDER-####` registry-regeneration and legacy-history-recovery work (`WS-0014` item 1), the 26
already-researched non-canonical Company Intelligence contenders, and any future equity contender all
remain within scope of the schema this decision governs (§B) — but none of them is populated,
researched, or evaluated by this filing. ETF, cryptocurrency, and other non-equity methodology remain
`WS-0014`/`XASSET-0001`'s own separate governance track, unaffected here. Final portfolio synthesis —
overlap/concentration modeling, cross-asset opportunity-cost comparison, sleeve- and instrument-level
sizing — remains a distinct, later, cross-asset step (`XASSET-0001` §J, `XASSET-0005`), not addressed
or advanced by this filing.

### T. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0004-rq4-evidence-architecture-governance.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0004`).
3. `operations/WORKSTREAMS.yaml` (§N above).
4. `CLAUDE.md` (one Decisions Log pointer entry).
5. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 97 → 98).

**No other file is touched.** No production code, no `intelligence/**` record, no `PROTOCOL_V1.md`,
`METHODOLOGY_EVALUATION_REPORT.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` change, no `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml` change.

### U. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1 (`OPS-0009` Lane G — new authorization, full weight, never reduced),
complete any required bounded correction and exact-head re-review, and receive explicit principal
acceptance before it may be marked ready or merged. **This decision does not mark itself ready and does
not authorize its own merge.** No evidence-architecture implementation PR may open, and §§A–S above are
not effective, until this PR merges to `main`.

## Rationale

**Why govern the evidence architecture now, separately from the schema/validator implementation.**
Matches this repository's own established "define, then later authorize implementation" discipline at
every layer of the Portfolio/Theme/relationship/classification/reconciliation/recommendation/archetype
Intelligence programs (`REL-0001` before `REL-0002`; `TIER-0001`/`TIER-0002` before `TIER-0005`;
`XASSET-0002` before `XASSET-0003`; `VALUATION-0002` before `VALUATION-0003`, which this filing itself
mirrors one layer deeper). Combining architecture design with implementation in one filing would
collapse a design decision (what must the evidence category be able to represent) into an
implementation decision (the exact YAML keys and validator logic) before either has been independently
reviewed on its own terms — exactly the risk this repository's own governance history has repeatedly
avoided at this program's every prior layer.

**Why a new, separate companion schema rather than extending the frozen Company Intelligence schema.**
RQ4's own finding (report §7) already establishes the two evidence classes are structurally distinct —
narrative/qualitative (existing) versus dated, per-period, provenance-labeled quantitative (missing) —
and `PI-0001`'s freeze (restated at every subsequent Portfolio Intelligence phase, most recently
`PI-0034`) remains fully controlling: the Company Intelligence schema is frozen doctrine, reconsiderable
only through its own new documented architectural decision backed by materially changed evidence.
Proposing a companion, one-way-referencing evidence layer — the same architectural move this
repository already made for Theme Intelligence (`PI-0006`), relationship mapping (`REL-0001`), Milestone
6 classification (`TIER-0002`), ETF/crypto classification (`XASSET-0002`), and the archetype layer
itself (`VALUATION-0003`) — avoids reopening that freeze while still closing RQ4's gap.

**Why the schema/validator/test implementation is authorized without any population, rather than
combining schema-building with a first real-company evidence batch.** Mirrors `REL-0001`'s own
"inventory-only, no relationship content" split from `REL-0002`'s first content batch, and
`VALUATION-0003`'s own split of "archetype-assignment authorization" from its later implementation.
Population requires real, external, per-company financial-statement and market data research — a
materially different risk class from schema/validator scaffold work, and outside what this filing's own
authorization from the principal covers (the task explicitly defaults to "schema + validator first;
population later under separately bounded authorization"). Combining them here would also pre-empt a
future population-phase authorization's own opportunity to set minimum-history-length policy (§H) and
select which tickers to populate first, exactly the kind of scope-narrowing decision `PI-0024`'s "no
license to silently narrow the batch" discipline and this repository's first-coverage precedent both
reserve for their own separate filing.

**Why RQ4 closure is claimed only at the design-governance stage, not the "gap closed" stage
`VALUATION-0002` §6.3(b) uses.** The task's own instruction to prefer the narrower, more auditable claim
where the sequencing is ambiguous is adopted deliberately: `VALUATION-0002` §4's phrase, "closed by its
own, separately authorized, future governance decision," is most naturally read as closed by a decision
that actually produces usable evidence infrastructure — a governance-design document alone does not
give a future valuation application anything to read evidence from. Claiming full closure here would
overstate what this filing accomplishes and could be cited later as though `VALUATION-0002` §6.3(b)'s
precondition were already satisfied when no schema yet exists on `main`. §O's four-stage breakdown
exists specifically to prevent that conflation.

**Why `category: valuation_evidence_governance`, a new category distinct from `VALUATION-0002`'s
`valuation_methodology_governance` and `VALUATION-0003`'s `valuation_archetype_governance`.**
`VALUATION-0002` adopts methodology-selection doctrine; `VALUATION-0003` authorizes archetype-assignment
work; this filing governs a structurally distinct third act — the design of a quantitative evidence
architecture neither of the prior two decisions performs or authorizes — matching the precedent
`TIER-0001` established when it took its own new category (`tier_classification_governance`) for a
decision playing a structurally different role in the same overall program, and that `VALUATION-0002`'s
own Rationale explicitly cites as the model for this exact situation.

## Alternatives Considered

- **Combine RQ4 evidence-architecture governance with the future schema/validator implementation in one
  filing.** Rejected — this repository's own established "define, then later authorize implementation"
  discipline (see Rationale) treats architecture design and code implementation as separate review
  units at every prior layer of this program; no exception is warranted here.
- **Combine schema/validator implementation authorization with a first real-company evidence population
  batch, "to prove the schema works on a real example."** Rejected outright — this filing's own
  authorizing task explicitly bars it ("Do not authorize real-company population unless the live
  governance analysis clearly shows that combining schema implementation and population is necessary
  and safe" — no such showing exists; population requires materially different, external-research-risk
  work), and doing so would also violate `VALUATION-0002` §6.2/§6.3's own explicit sequencing (archetype
  assignment, then RQ4 closure, then valuation execution — evidence population sits logically between
  RQ4 closure and valuation execution, not folded into the closure step itself).
- **Extend the frozen Company Intelligence schema directly with new quantitative fields instead of a
  separate companion structure.** Rejected — `PI-0001`'s freeze remains fully controlling and this
  filing has no authority to reopen it; every structurally analogous evidence-category need in this
  repository's history (Theme Intelligence, relationships, Milestone 6 classification, ETF/crypto
  classification, the archetype layer) has been resolved with a new companion structure, never a
  Company Intelligence schema amendment.
- **Invent a hard minimum historical-period-length requirement now, to give the future implementation a
  concrete target.** Rejected — no existing repository authority sets one for this domain, and
  `NUM-0001`'s own provenance-classification discipline treats an unsupported numeric parameter as its
  own defect class; the schema's own multi-period support (§H) does not require a minimum to be
  structurally sound, and a future population-phase authorization is the correct place to set one with
  its own disclosed justification.
- **Decide actual discount-rate policy (ERP value, beta window, WACC weighting convention) now, so the
  evidence schema and the policy are defined together.** Rejected — the task's own explicit boundary
  (§I) reserves this to later application policy, and doing so here would exceed a design-governance
  filing's own bounded scope into methodology-application territory `VALUATION-0002` §6.3 already
  reserves for a separate, later, explicitly authorized unit.

## Consequences

**What changes.** A future, separate implementation PR may now be opened to build the `intelligence/
valuation_evidence/` schema, its validator, and its test suite as an empty/scaffold structure — but only
after this governance PR itself is independently reviewed and principal-accepted. Once that future
implementation merges, `VALUATION-0002` §6.3(b)'s RQ4-closure precondition on real-company valuation
execution is satisfied for the first time — but real-company evidence population (§O.3) and valuation
execution (§O.4) each remain their own further, separately authorized, later units. `WS-0015`'s register
entry reflects PR #279's confirmed merge (with the corrected final archetype-cohort figures) and this
filing's own evidence-architecture-governance step.

**What does not change.** No real company's quantitative evidence exists or is populated. No real
company is valued. No fair value, price target, expected return, discount rate, peer set, or scenario
probability is assigned to any real company. `TIER-0009` §K's `target_and_range`/
`maximum_position_size` `valuation_required` status is unchanged on all 27 canonical equities.
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `PROTOCOL_V1.md`, and `METHODOLOGY_EVALUATION_REPORT.md` are all
unedited. No target, tier, holdings, gate, cap, cluster, allocator, margin, or ladder value changes. No
Company/Theme/relationship/classification/reconciliation/recommendation/archetype Intelligence record
changes. No chart evidence of any kind is consumed. `CONTENDER-0003`, ETF/crypto evaluation, and
cross-asset synthesis remain unaddressed. `WS-0005` and `WS-0014` are unaffected.

---

No company was valued and no quantitative valuation evidence was populated. `VALUATION-0004` governs
the RQ4 evidence architecture only. The 27-company cohort remains a bounded first equity-valuation
cohort, not the exhaustive Portfolio-HQ contender universe.
