---
decision_id: VALUATION-0006
date: 2026-08-09
status: Proposed
category: valuation_application_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0002, XASSET-0005, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/VALUATION-0006-stage4-methodology-application-policy-and-result-architecture.md
---

## Context

### Authority for this unit

`governance/decisions/VALUATION-0002-equity-valuation-methodology-doctrine-adoption.md` §6.3 states that
real-company valuation execution requires, at minimum: "(a) [archetype assignment] to have already
occurred for the company in question; (b) the RQ4 evidence-category gap (§4) to have been separately
closed; (c) full compliance with the §3 false-precision doctrine; and (d) its own independent review and
principal acceptance before any output is produced." `VALUATION-0004` §O's four-state framework records
that RQ4 closure (state 2, schema/validator/test merged) was reached by PR #281; `VALUATION-0005` then
authorized and PR #283 implemented state 3 (real-company evidence population) for the 27 canonical
equities. `VALUATION-0004` §I explicitly reserved discount-rate **policy** (as opposed to discount-rate
**evidence**) to "a later, separately authorized application-phase policy decision — this filing governs
only that the underlying inputs have a structural home." `VALUATION-0004` §J/§K reserve peer-selection and
scenario-probability-assignment **policy** identically. `TIER-0009` §K independently confirms "no such
framework currently exists anywhere in this repository" and that `target_and_range`/`maximum_position_size`
stay doctrinally forced to `valuation_required` "until one is separately proposed, researched, and
accepted through its own future governance decision." This filing is that separate, later, explicitly
authorized methodology-application-policy-and-result-architecture unit — for the design/authorization
step only, per §V below. It does not itself reach `VALUATION-0002` §6.3(c)/(d) or perform any state-4
work under `VALUATION-0004` §O's numbering (restated one layer forward as §T below).

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` fetched; local branch
  `claude/valuation-0006-stage-4-design-bov9rs` confirmed identical to `origin/main` at
  `b3fb5325cac5736daf59a109ebc5e1daa1704297` (the merge commit of PR #287/`XASSET-0008`), zero divergence,
  working tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API before any edit — no competing active
  mutation lane.
- **PR #283 (`VALUATION-0005`-authorized Stage-3 evidence-population implementation) independently
  reconfirmed merged**, full lifecycle re-verified from the GitHub API, not taken on any prior summary's
  word — see §Q below for the complete, independently-reconstructed record, including a resolved
  bounded-correction round on the retained audit's own segment/market-observed coverage counts (the 27
  sealed evidence records themselves were never touched by that correction).
- **`research/equity_valuation_study/PROTOCOL_V1.md` and `METHODOLOGY_EVALUATION_REPORT.md` read in full
  this session** — the seven methodology families (protocol §4), seven archetype categories A–G
  (protocol §5), the closed 49-cell four-value disposition matrix (protocol §7), and the predictive-
  research prohibition (protocol §1/§3/§12) independently reconfirmed unedited. Protocol hash
  independently recomputed: `sha256sum research/equity_valuation_study/PROTOCOL_V1.md` →
  `2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980` — matches `VALUATION-0001` §3 and
  every subsequent filing's own independent recomputation, zero drift.
- **`VALUATION-0002` read in full this session** — its §2 per-family governed-role table (bound by
  reference below, not restated), its §3 false-precision doctrine (bound by reference, cited exactly),
  and its §6.3 three-step boundary (quoted above) independently reconfirmed unedited.
- **`VALUATION-0004` read in full this session** — its §I/§J/§K/§L evidence-vs-policy boundaries (discount
  rate, peer set, scenario, segment/SOTP) independently reconfirmed to reserve exactly the policy
  questions this filing now answers, and no others.
- **`VALUATION-0005` read in full this session, plus its populated output independently verified against
  live repository data, not against the decision file's own claims**:
  - `intelligence/valuation_evidence/` independently confirmed to contain exactly 27 ticker YAML files
    plus `COHORT_MANIFEST.yaml` — `AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC,
    LLY, META, MSFT, NVDA, PANW, PWR, RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM` — exact match to the
    27-name cohort `VALUATION-0005`/`PI-0037`/`TIER-0008` all independently derive from `targets.yaml`.
  - **`discount_rate_evidence` independently confirmed abstained on all 27 of 27 records (100%)**, every
    one carrying a non-empty `abstention_reason` — a disclosed Stage-3 scope limitation, not a schema
    defect (see §D below).
  - **Zero populated `probability_weight` anywhere across all 27 records** — independently confirmed by a
    recursive key search across the full corpus.
  - **Zero applied/selected peer set anywhere** — every `peer_set_evidence.candidates[].inclusion_status`
    value across the corpus is `included`; no field anywhere indicates a peer was actually selected for
    use in a computation (see §F below).
  - **`segment_evidence` per-segment entries independently confirmed to use only `segment_name`,
    `revenue`, `profit` in the live corpus** (the fourth allowed key, `cash_flow`, is schema-permitted but
    unused in this cohort); **zero occurrence of `segment_assets` or `segment_capex`** anywhere — see §P
    below (non-blocking).
  - **No `evidence_quality`/`primary_source_coverage` field exists anywhere in the Stage-3 schema or its
    27 populated records** — independently confirmed absent, not merely uniform. The closest structural
    analog is each record's own `uncertainty_summary` and per-domain `provenance.access_status`
    (`consulted_via_search_aggregation` for essentially the entire corpus, per PR #283's own disclosed
    WebFetch-blocked scope limitation) — see §I below for how this filing's evidence-quality policy is
    built from those existing fields rather than a nonexistent one.
- **`valuation_evidence_validator.py` and `valuation_archetype_validator.py` read in full this session** —
  their shared `canonical_record_hash()` pattern (sorted-key JSON canonicalization over every field except
  the five seal fields, SHA-256), their closed-schema/extra-key-rejection discipline, their independent
  second-stage free-text scan discipline, and `valuation_evidence_validator.validate_authorized_cohort()`'s
  exact missing/extra-ticker-only design (an abstained record still counts as "present") are all bound by
  reference below (§K/§L), not redesigned. Neither module imports `allocate.py` or `margin_state.py` in
  either direction — independently reconfirmed.
- **`NUM-0001` and `governance/decisions/README.md` read in full this session** — the six-class numeric-
  parameter-provenance taxonomy (§1 below cites it directly per parameter) and the decision-filing
  conventions (kebab-slug filename, frontmatter schema, never edit a file's substance after
  `status: Accepted`, a new category minted only when a decision plays a structurally distinct role)
  independently reconfirmed and applied.
- **`OPS-0007` §1 and `OPS-0009` read in full this session** — the twelve-point capability-based
  independent-review standard and Lane G's "always full weight, never reduced" rule (§U below) bind this
  filing exactly as they bound every prior `VALUATION-####`/`TIER-####`/`REL-####`/`XASSET-####` filing.
- **`TIER-0009` §K read and quoted directly** (Context above) — independently reconfirmed unedited, still
  the controlling statement that no valuation framework exists and that `G.4`/`G.5` remain
  `valuation_required` pending a future, separately accepted governance decision.
- **Decision catalog independently rebuilt before this filing's own new entry**: 102 decisions, 0 issues
  (`portfolio_hq.dashboard.decisions.build_catalog('.')`).
- **`test_portfolio_hq_dashboard_decisions.py` independently inspected**: two hardcoded assertions
  (`test_real_repository_catalog_builds_all_71_with_no_issues` line 108,
  `test_real_repository_model_and_render_succeed_end_to_end` line 925) currently assert `== 102`; both
  require bumping to `103` (§U below).
- **Full repository `pytest` baseline independently reproduced before any edit**: 4042 passed, 0 failed, 1
  pre-existing unrelated `DeprecationWarning` (`intelligence_classification_sanitizer.py`).
- **Zero `intelligence/valuation_results/` (or similarly named) directory exists anywhere in the
  repository** at this commit — confirmed by direct filesystem search. No prior filing has proposed,
  named, or scoped a valuation-**result** category; only the evidence category (`VALUATION-0004`) and the
  archetype category (`VALUATION-0003`) exist today.

## Decision

**This decision governs Stage-4 equity valuation methodology-application policy (the conventions a
future valuation execution must follow for discount-rate construction, terminal value, peer-set
selection, scenario-probability assignment, evidence-quality treatment, sensitivity/range construction,
and conflict/abstention handling) and the structure of a new, separate, roster-agnostic valuation-**result**
architecture — and authorizes exactly one future, separate, bounded implementation PR to build that
result schema, its validator, and its test suite as an empty/synthetic-fixture-only scaffold. It values
no real company, produces no real fair-value range, populates no real valuation-result record, and does
not itself authorize real-company valuation execution. Implementation does not begin in this session.**

### A. What is authorized

One future, separate, bounded implementation PR that creates: (1) the result-schema structure defined in
§K–§L below, roster-agnostic and reusable beyond the current 27-name cohort; (2) a dedicated
`valuation_result_validator.py` (deliberately **not** an extension of `valuation_evidence_validator.py`,
which is evidence-only and must continue to reject valuation-output content per its own §Q design — see
§L) enforcing every structural, compatibility, and false-precision rule in §K/§L/§M below; (3) that
validator's focused test suite, using synthetic fixtures only, exactly matching this program's own
established discipline for every prior scaffold-stage validator (`classification_validator.py`,
`etf_classification_validator.py`, `crypto_classification_validator.py`, `valuation_archetype_validator.py`,
`valuation_evidence_validator.py`). **No real company's valuation-result file is created or populated by
that implementation PR** (§S). That future PR requires its own full independent-review/correction/
re-review/principal-acceptance/merge/post-merge-verification lifecycle under `OPS-0007` §1 / `OPS-0009`
Lane G before any of it is authoritative. Nothing in §§B–P below is itself a schema, a validator, or a
populated record — this filing specifies what a later implementation must build, and what a still-later,
separately authorized execution unit must follow when it eventually populates real records.

### B. Companion result architecture — a new layer, one-way referencing only

The new result category lives in its own directory, filesystem-is-the-index, matching this repository's
established convention for a structured-judgment-record axis (`intelligence/classification/`,
`intelligence/etf_classification/`, `intelligence/crypto_classification/`, `intelligence/valuation_archetype/`,
`intelligence/valuation_evidence/` — single-YAML-per-ticker, no paired Markdown, since this is structured
quantitative output, not a narrative thesis document): **`intelligence/valuation_results/<TICKER>.yaml`**,
plus one `COHORT_MANIFEST.yaml`. The frozen Company Intelligence schema, the Stage-2 archetype schema, and
the Stage-3 evidence schema are none of them modified, extended, or reinterpreted by this decision. The new
layer is additive and one-way-referencing only: a `valuation_results` record cites a `TICKER`'s already-
sealed `valuation_archetype` record and already-sealed `valuation_evidence` record by pinned content hash
(§K), but neither of those upstream records ever references or depends on the result layer, and the result
layer never writes to, or is written to by, any of them. **Roster-agnostic by design, populated by nobody
under this filing** — the schema carries no population restriction to the 27 canonical equities (§S), and
this filing authorizes zero population of any ticker under any circumstance.

### C. Methodology-application policy — index of the seventeen governed conventions

Every convention below binds **by reference** to `VALUATION-0002` §2's already-accepted per-family
governed-role table and §3's already-accepted false-precision doctrine — neither is redesigned,
re-derived, or restated in full here. Each item carries its `NUM-0001` provenance class (§1 below cites the
class definitions directly); items with material design depth receive their own lettered deep-dive section
(cross-referenced). **No numeric value is assigned to any real company by any item below.**

1. **Risk-free-rate handling.** The evidence itself (a sourced yield observation) is `NUM-0001` class 1,
   externally imposed — the system does not choose the rate, the market does. The *convention* selecting
   which maturity/instrument to cite (a sovereign benchmark yield matched to the valuation's functional
   currency, e.g. the 10-year U.S. Treasury yield for a USD valuation) is class 5, provisional governance
   guardrail — a widely-used equity-research convention, not evidence-tested against alternatives within
   this repository. Deep dive: §D.
2. **Equity-risk-premium (ERP) handling.** No single ERP value is selected by this decision — class 6,
   unsupported/unclassified, deliberately left unclassified rather than forced into a class it does not
   earn. Policy requires every ERP figure a future execution uses to carry one of `VALUATION-0002` §3's
   four provenance labels (`market_derived` for an implied/forward-looking ERP, `historically_observed`
   for a long-run realized ERP, or `analyst_consensus_cited`) — `assumed_for_illustration` is disallowed
   for ERP specifically, since an illustrative ERP would make every downstream range illustrative rather
   than evidence-grounded. Deep dive: §D.
3. **Beta estimation window.** Class 5, provisional governance guardrail — minimum observation window of
   two years (104 weekly or 24 monthly return observations, whichever periodicity the sourced beta
   observation actually reports — this policy does not fabricate a periodicity the source doesn't supply).
   Deep dive: §D.
4. **Beta reference index.** Class 5, provisional governance guardrail — a broad, market-capitalization-
   weighted index matched to the company's primary listing currency and exchange, disclosed explicitly by
   name in every beta observation's provenance. Deep dive: §D.
5. **WACC construction.** Class 2, mathematically derived — WACC is a capital-structure-weighted
   combination of an already-sourced, already-labeled cost of equity (CAPM-style: risk-free rate + beta ×
   ERP, each individually provenanced per items 1–4) and after-tax cost of debt (item 7). The formula
   itself is mechanical; every input feeding it must independently satisfy its own provenance rule. No
   single opaque WACC field may exist without its component inputs also being individually visible
   (`VALUATION-0004` §E.9, restated). Deep dive: §D.
6. **Capital-structure weighting.** Class 1/5 — market-value-based weights when both debt and equity
   market values are observable (class 1, externally imposed by observed market data); a disclosed
   fallback to book-value weights when market values for debt are not observable (class 5, provisional
   guardrail, explicitly flagged as a lower-fidelity substitute, never silently presented as market-value-
   based). Deep dive: §D.
7. **Cost-of-debt treatment.** Class 1, externally imposed/observed — a sourced issuer credit-spread or
   effective yield-to-maturity figure; no invented default spread. Deep dive: §D.
8. **Tax-rate handling.** Reuses the Stage-3 schema's existing `tax_rate_type` (`effective`/`statutory`)
   distinction unedited — class 1, externally imposed/observed; no new vocabulary invented. Deep dive: §D.
9. **Terminal-value / terminal-growth discipline.** Two-part rule: terminal growth **must never exceed the
   same valuation's own sourced discount-rate input** — class 2, mathematically derived (a perpetuity-
   growth model diverges or becomes economically nonsensical otherwise; this is a mathematical necessity,
   not a governance preference). A softer convention — terminal growth should not exceed a disclosed
   long-run risk-free-rate or real-GDP-growth proxy — is class 5, provisional guardrail, an industry norm
   this repository has not evidence-tested. No fixed percentage ceiling (e.g., "2.5%") is invented here.
   Deep dive: §E.
10. **Peer-candidate → applied-peer-set selection.** Procedural rule, class 4, evidence-bounded governance
    selection: the future execution session may select its **applied** comparable set only from among the
    tickers already present in the referenced Stage-3 `peer_set_evidence.candidates[]` with
    `inclusion_status: included`; it may **exclude** a Stage-3-included candidate at execution time with a
    disclosed rationale, but may **never add** a candidate not already sourced at Stage-3 — new peer
    research is an evidence-population action, not an execution action, preserving the evidence/execution
    separation this repository's whole program is built on. Deep dive: §F.
11. **Minimum peer-set sufficiency / thin-peer-set abstention.** Class 5, provisional governance guardrail
    — a minimum of **two** applied comparable peers is required before relative valuation (family 5) may
    be treated as reaching a `completed` result for that company; below that, the family may be applied
    only as a disclosed corroborative data point inside a `partial` result, never as the sole basis for a
    `completed` one. Directly motivated by a real finding in the live Stage-3 corpus (§F). Deep dive: §F.
12. **Scenario-probability assignment discipline.** Procedural, class 4 — the future execution session may
    assign a probability weight only to a scenario already named in the referenced Stage-3
    `scenario_evidence.scenarios[]`; it may never invent a new scenario at execution time (mirrors item 10
    exactly, one layer over). Deep dive: §G.
13. **Probability coherence requirements.** Class 5, provisional guardrail — when every scenario in an
    applied set carries a probability weight, those weights must sum to within a disclosed ±0.02 tolerance
    of 1.0; a scenario set that is explicitly disclosed as non-exhaustive (does not claim to enumerate
    every plausible outcome) is exempt from the sum-to-1.0 requirement but must say so explicitly. Deep
    dive: §G.
14. **Evidence-quality / source-quality treatment.** Procedural, no numeric parameter — reuses
    `VALUATION-0004` §G's existing source hierarchy and its explicit "no primary-only-or-abstain-forever
    rule" (bound by reference, not restated); since the entire live Stage-3 corpus is presently
    `source_type: secondary`, a policy requiring primary sourcing to proceed would make Stage-4 execution
    permanently impossible on the current evidence base. Deep dive: §I.
15. **Sensitivity / range construction.** Reuses `VALUATION-0002` §3's already-adopted mandatory
    range-not-point requirement unedited; the procedural addition here is which sensitivity axis (axes)
    must be named per family — class 4, evidence-bounded governance selection, since the report's own
    archetype-specific elaborations (adopted by `VALUATION-0002` §3) already identify the governing
    sensitivity per family/archetype pairing. Deep dive: §J.
16. **Conflict propagation from Stage-3 evidence.** Procedural, no numeric parameter — any
    `disclosed_conflicts` entry or domain-level abstention in the referenced Stage-3 record that bears on
    an applied family's inputs must be carried forward into the result record's own
    `conflicts_carried_forward`/`uncertainty_summary`, never silently dropped or resolved in one direction.
    Deep dive: §J.
17. **Explicit company-level abstention rules.** Procedural, no numeric parameter — the closed three-value
    `result_status` vocabulary (§K) and its exact triggering conditions. Deep dive: §J.

### D. Discount-rate policy — construction convention, not a real number, and a disclosed prerequisite gap

The discount-rate **evidence** structure (`discount_rate_evidence`'s five components) was already governed
by `VALUATION-0004` §I and implemented by `VALUATION-0004`'s own Stage-2 PR. This section governs
discount-rate **policy** — how a future execution combines those sourced components into a usable discount
rate, per items 1–8 above:

1. **Cost of equity** = risk-free rate (item 1) + beta observation (items 3–4) × equity risk premium
   (item 2). A CAPM-style construction is adopted as the **default** convention because it is the only
   combination the Stage-3 schema's five existing components (§I above) structurally support without
   inventing a sixth evidence category this filing has no authority to create — it is not asserted as the
   only academically defensible model, merely the one the existing evidence architecture already supports.
2. **After-tax cost of debt** = cost of debt observation (item 7) × (1 − tax rate, item 8). Mechanical,
   class 2.
3. **WACC** = capital-structure-weighted (item 6) blend of the two. Mechanical, class 2, once every input
   is individually sourced and provenanced.
4. **No single opaque `discount_rate`/`wacc` field may exist in a populated result record without its
   component inputs also being individually visible** — restated from `VALUATION-0004` §E.9, now binding
   on the result layer specifically (the evidence layer's own `_FORBIDDEN_DISCOUNT_RATE_KEYS` structural
   ban on `discount_rate`/`wacc`/`equity_risk_premium`/`erp`/`cost_of_capital` as raw *evidence* fields is
   unaffected; the result layer may report a **computed** WACC value, but only alongside its full component
   breakdown, never in isolation — see §K/§L).
5. **A financial-intermediation archetype (protocol archetype C) may require a different cost-of-equity
   construction** (e.g., a dividend-discount or excess-return approach, per `VALUATION-0002` §2's own
   "FCFE DCF (DDM/excess-return for C)" family naming) rather than a pure CAPM blend — this filing does not
   design that variant's own internal mechanics; it is disclosed as an open sub-question a future
   execution session must address on its own evidence, using the same risk-free-rate/beta/ERP component
   inputs already governed above, and must disclose which construction it used and why.

**Disclosed prerequisite gap, not closed by this filing.** `discount_rate_evidence` is independently
confirmed abstained on all 27 of 27 current Stage-3 records (Preflight above). Under this policy's own
abstention rules (§J), **any future Stage-4 execution attempting family 2 (FCFF DCF) or family 3 (FCFE
DCF) — the Primary family for archetype categories A and G, 8 of the 27 sealed archetype records per §N's
independently re-derived corrected distribution — would be structurally forced to `partial` or
`unable_to_determine` for the discount-rate-dependent portion of its output**, until a future, separate
discount-rate-evidence population unit (extending Stage-3's own domain, not this filing, and not
necessarily even the schema this filing governs) populates that domain for the company in question. This
filing does not authorize, schedule, or perform that population — it only states the consequence
explicitly so a future reader does not discover it by surprise mid-execution.

### E. Terminal-value / terminal-growth discipline

Restating item 9 with its full reasoning: the hard rule (terminal growth must not exceed the same
valuation's own sourced discount rate) is a mathematical necessity of the perpetuity-growth model, not a
policy preference — a terminal growth rate at or above the discount rate makes the model's terminal-value
term diverge or turn negative, an internally inconsistent output no amount of disclosure can rescue. The
softer convention (terminal growth should not exceed a disclosed long-run risk-free-rate or real-GDP-growth
proxy) is adopted as a **provisional guardrail** (`NUM-0001` class 5) rather than a fixed invented
percentage, because no evidence internal to this repository has tested one specific ceiling number against
alternatives (matching `VALUATION-0004` §H's identical refusal to invent an unsupported minimum-history
length, and `VALUATION-0005` §D's identical class-5 treatment of its own five-year guardrail). **Review
condition** (evidence-driven, per `NUM-0001` §6): revisit if a future execution unit finds the discount-
rate-relative ceiling alone insufficiently constraining in practice (e.g., producing an implausibly wide
range for a mature-compounder archetype), or if a future, separately authorized valuation-methodology
study produces range-establishing evidence supporting a specific fixed ceiling — either of which would
support reclassifying a revised convention under `NUM-0001` class 3 or 4, not merely re-asserting class 5
with a different number.

For archetype F (diversified/multi-segment, the Primary family for asset-based/NAV/SOTP), a segment-level
sum-of-the-parts output must apply this same terminal-growth discipline **independently, per segment** —
never a single blended terminal-growth assumption smeared across structurally different segments —
restating `VALUATION-0004` §L's own archetype-F elaboration (adopted by `VALUATION-0002` §3 by reference to
the report, not restated there in full), extended here from an evidence rule into an execution-policy rule.

### F. Peer-set selection discipline

Restating item 10 in full: Stage-3 evidence records a **candidate** peer set with a comparability rationale,
provenance, and an `included`/`excluded` disposition per candidate (`VALUATION-0004` §J, implemented by
`VALUATION-0005`/PR #283). None of that is an **applied** peer set — no field anywhere in the live corpus
indicates a peer was actually selected for use in a relative-valuation computation (Preflight above,
independently reconfirmed). This filing's policy: a future execution session's applied comparable set is a
**subset** of the referenced record's `included` candidates, never a superset. Excluding a Stage-3-included
candidate at execution time is permitted with a disclosed rationale (e.g., a candidate that reads as
comparable in business description but proves, on closer multiple-construction inspection, to differ
materially in capital structure, growth stage, or scale); **adding** a candidate not already present in the
Stage-3 record is prohibited — a future execution session that believes a materially better comparable
exists must request a Stage-3 evidence-population extension for that ticker, not silently expand the
applied set beyond what evidence governance already sourced and reviewed.

**Minimum-sufficiency guardrail (item 11), directly motivated by a real finding in the live corpus.** The
independent review of PR #283 flagged, as a non-blocking NOTE, that TSM's sole Stage-3 peer candidate
(ASML) is "a value-chain supplier relationship, not a competitive/valuation comparable" — a real, disclosed
thinness case, not a hypothetical one. This filing's policy converts that observed risk into a mechanical
rule: relative valuation (family 5) may reach `result_status: completed` only with **at least two** applied
comparable peers; with zero or one, the family may still be reported, but only inside a `partial` result as
a disclosed corroborative data point, never as sole support for a `completed` determination. `NUM-0001`
class 5, provisional guardrail — two is a defensible minimum for "comparable set," not an evidence-tested
optimum. **Review condition**: revisit once a future execution unit's own experience across the cohort
shows the two-peer floor is systematically too strict (forcing an unwarranted number of archetype-B/G
relative-valuation results into `partial`) or too permissive (a two-peer set still producing implausibly
wide multiple dispersion), either of which would support reclassification under `NUM-0001` class 3 or 4.

### G. Scenario-probability assignment discipline

Restating items 12–13 in full: Stage-3's `scenario_evidence.scenarios[]` supplies named variables and their
evidence basis, with a `probability_weight` field that is schema-present but populated for zero real
companies today (Preflight above, independently reconfirmed — the key does not appear with a non-null value
anywhere in the live corpus). This filing's policy mirrors §F exactly, one layer over: a future execution
session may assign a probability weight only to a scenario **already named** in the referenced Stage-3
record; inventing a new scenario at execution time is prohibited for the identical reason new-peer addition
is prohibited in §F — scenario **identification** is an evidence-population action (would require new
research into what outcomes are plausible), while probability **assignment** is an execution-policy
judgment applied to already-sourced possibilities.

**Coherence requirement**: when every scenario in an applied set carries a weight, the set must sum to
within a disclosed ±0.02 tolerance of 1.0 — `NUM-0001` class 5, a rounding-error allowance, not an
evidence-derived figure. A scenario set explicitly disclosed as non-exhaustive is exempt from summing to
1.0, but the record must say so in `uncertainty_summary` rather than silently presenting an incomplete set
as though it were complete. Every populated `probability_weight` must carry one of `VALUATION-0002` §3's
four provenance labels (§C item 2's restriction against `assumed_for_illustration`-only ERP does **not**
apply here — an illustrative scenario-probability weight is permitted, provided it is honestly labeled as
such, since scenario analysis for archetype E (early-stage/binary-outcome) inherently trades in disclosed
judgment under genuine uncertainty, matching the report's own RQ3 elaboration for archetype E, adopted by
`VALUATION-0002` §3 by reference, not restated there in full: "every scenario's probability weight must
itself carry a provenance label... an undisclosed or unlabeled probability weight reintroduces exactly the
false precision this specification exists to prevent").

### H. Predictive-research boundary — restated, not reopened

Nothing in §§D–G authorizes, and no future execution unit under this filing's authority may perform, any
historical backtest of a discount rate, terminal-growth assumption, peer multiple, or scenario probability
against **subsequent stock-price performance**, under any framing. `PROTOCOL_V1` §1/§3/§12's predictive-
research prohibition (bound by reference, quoted in full at `VALUATION-0001` §3 and every subsequent
filing) is unedited and fully controlling. A future execution unit's discount rate, terminal growth, peer
set, and scenario probabilities are **inputs to a present-value estimate**, never a forecast calibrated or
validated against what a stock price actually did afterward.

### I. Evidence-quality and source-quality treatment

Restating item 14: the live Stage-3 corpus is, without exception, `source_type: secondary`,
`access_status: consulted_via_search_aggregation` (Preflight above) — no primary-sourced fact exists
anywhere in the 27-record cohort today. `VALUATION-0004` §G's own governing text is directly on point and
is bound by reference, not restated in full: "This decision does not create a 'primary-only or abstain
forever' rule... a future population phase must be permitted to fall back to a lower-reliability source
class with honest, explicit disclosure of that fallback and its `access_status` — never blocked outright
from recording any evidence at all merely because a primary source was unreachable." This filing extends
that same discipline to execution: a future Stage-4 result may be built entirely on `secondary`,
`consulted_via_search_aggregation` evidence, provided the result record's own `evidence_quality_summary`
(§K) discloses that sourcing tier honestly and the result's `uncertainty_summary` states plainly that no
primary-sourced input backs the range. **No numeric confidence-discount formula is invented here** — this
filing does not require the range to be mechanically "widened by X% for secondary sourcing," since no
evidence establishes what X should be and inventing one would itself be exactly the false-precision defect
this whole doctrine exists to prevent (`NUM-0001` class 6, unsupported, deliberately not attempted).
Instead: **where a Stage-3 `disclosed_conflicts` entry or domain-level abstention bears materially on an
applied family's own required inputs, that family may not reach `completed` for that company** — a
qualitative, mechanically-checkable proxy for "insufficient evidence quality to proceed cleanly," rather
than a fabricated numeric discount.

### J. Sensitivity, range construction, conflict propagation, and abstention (items 15–17)

**Sensitivity/range (item 15).** `VALUATION-0002` §3's mandatory range-not-point requirement is restated,
not re-derived: every applied family's output must be a low/base/high range (or, for family 7, the full
disclosed scenario set per §G) with its governing sensitivity named explicitly. The report's own archetype-
specific sensitivity elaborations (adopted by `VALUATION-0002` §3 by reference — commodity/cyclical
normalization-basis disclosure for D; early-stage scenario-probability-weight labeling for E; financial-
intermediation regulatory/credit-assumption disclosure for C; diversified/multi-segment per-segment range
disclosure for F) govern which sensitivity a future execution must name for that archetype; this filing
does not invent a fifth elaboration or override any of the four.

**Conflict propagation (item 16).** Any `disclosed_conflicts` entry, or any domain-level abstention, in the
referenced Stage-3 evidence record that bears on an applied family's own required inputs must appear in the
result record's own `conflicts_carried_forward` list (a structured pointer back to the specific Stage-3
conflict/abstention, never a restatement of its content) and must be reflected in `uncertainty_summary` —
never silently dropped, never silently resolved in one direction by the execution session's own unstated
judgment. This directly extends `VALUATION-0004` §E.5's identical evidence-layer rule one layer downstream.

**Abstention (item 17) — the closed `result_status` vocabulary and its triggering conditions**, exactly
three values, mirroring this repository's established three-tier structural pattern (`sealed`/`draft`-style
lifecycle states plus a first-class "cannot determine" path, matching `TIER-0002`'s `unable_to_determine`
axis and `VALUATION-0003`'s `unable_to_determine_archetype`):

- **`completed`** — at least one methodology family whose governed role for the ticker's own sealed
  archetype is Primary candidate or Secondary/corroborative (per `VALUATION-0002` §2, bound by reference)
  reached a populated range with every required input for that family sourced, provenanced, and free of a
  material bearing conflict/abstention per §I. Other applied families may remain `partial` or unapplied
  without preventing an overall `completed` status, provided at least one qualifying family is clean.
- **`partial`** — at least one family was attempted and produced a disclosed range, but no family reaching
  `completed`'s own bar exists — e.g., every attempted family has a material bearing conflict/abstention
  (the discount-rate gap in §D is the concrete, presently-universal example), or only a family whose
  governed role is Adjustment-required could be completed while every Primary/Secondary family for that
  archetype remains blocked.
- **`unable_to_determine`** — no family could produce even a partial range. Triggering conditions include:
  the ticker's own sealed archetype record itself carries `primary_archetype: unable_to_determine_archetype`
  (methodology compatibility cannot even be looked up, §M); or every methodology family whose governed role
  for the ticker's archetype is anything other than Prohibited/Insufficient basis for adoption is blocked by
  an evidence-domain abstention with no populated inputs at all. A non-empty `abstention_reason` is required
  whenever `result_status` is `partial` or `unable_to_determine`.

**No fourth value, no numeric confidence score, and no blended composite across `result_status` values is
ever computed** — restating `VALUATION-0002` §3's absolute "no opaque scoring or composite index, ever,
under any future extension" one final time, now binding explicitly on the result layer's own top-level
status field, not merely on the numeric range beneath it.

### K. Valuation-result schema — field architecture

The future implementation's `intelligence/valuation_results/<TICKER>.yaml` must represent, at minimum:

1. **Identity/envelope**: `schema_version`, `ticker`, `asset_class` (forced `equity` for this cohort,
   structurally roster-agnostic beyond it, matching `valuation_evidence_validator.py`'s own design).
2. **Governing authority**: a `governing_decision` list citing this decision (`VALUATION-0006`) and, once
   it exists, the future execution-authorization decision (§T) — never a value populated before that future
   decision is itself accepted.
3. **`archetype_reference`** — `{source_file, content_sha256}`, the pinned hash of the referenced sealed
   `intelligence/valuation_archetype/<TICKER>.yaml` record, independently recomputed at validation time via
   a **read-only** call to `valuation_archetype_validator.canonical_record_hash()` — never a duplicated
   copy of the archetype record's own `primary_archetype`/`secondary_archetype` fields (which the validator
   instead reads live from the pinned file itself, so the two records can never silently drift apart).
4. **`evidence_reference`** — `{source_file, content_sha256}`, the identical pinning pattern against the
   referenced sealed `intelligence/valuation_evidence/<TICKER>.yaml` record, via a read-only call to
   `valuation_evidence_validator.canonical_record_hash()`.
5. **`as_of_date`** — the valuation's own as-of date, independently distinct from the referenced evidence
   record's own `as_of_date`/`fiscal_period_end_date` fields (a valuation may post-date its evidence).
6. **`methodology_families_applied`** — a list, one entry per applied family, each carrying: `family_id`
   (closed vocabulary, exactly the seven protocol §4 short names —
   `family_1_asset_based_sotp`, `family_2_fcff_dcf`, `family_3_fcfe_dcf`,
   `family_4_earnings_fcf_yield`, `family_5_relative_valuation`, `family_6_roic_reinvestment`,
   `family_7_scenario_probability_weighted`); `governed_role` (the exact five-value `VALUATION-0002` §2
   vocabulary — Primary candidate / Secondary-corroborative / Adjustment-required / Prohibited /
   Insufficient basis for adoption — live-cross-checked against the pinned archetype, §M); `family_status`
   (`completed`/`partial`/`unable_to_determine`, family-level, distinct from the record's own top-level
   `result_status`); `valuation_range` (§K.7); `assumptions_ledger` entries specific to that family (§K.8).
7. **`valuation_range`**, per applied family — never a single point: `{low, base, high}` for a standard
   DCF/multiples/ROIC-style output, or a full `scenario_outcomes[]` list (each carrying its own value,
   optional `probability_weight`, and provenance label per §G) for family 7 — plus a mandatory
   `unit_and_basis` field (e.g. "USD per diluted share, equity value" vs. "USD per diluted share, enterprise
   value ÷ diluted shares" — the two are never conflated) and a mandatory `governing_sensitivity` field
   naming the assumption(s) the range is most sensitive to, per §J.
8. **`assumptions_ledger`** — one entry per governing assumption actually used (discount-rate components,
   terminal growth, applied peers, scenario probabilities, and any other named input), each carrying:
   `assumption_name`, `value`, `provenance_label` (exactly `VALUATION-0002` §3's four labels, no others),
   and a `source_or_derivation_note`.
9. **`sensitivity_disclosure`** — free text or a small structured table naming which assumption(s) most
   move the range, per family, matching the report's own archetype-specific elaborations (§J).
10. **`uncertainty_summary`** — record-level free text; must disclose secondary-only sourcing (§I) and any
    material conflict carried forward (§J) whenever applicable.
11. **`evidence_quality_summary`** — built entirely from the referenced Stage-3 evidence record's own
    existing `provenance.access_status` values and `abstention_index`, never a newly-invented numeric
    score; a projection, not a recomputation.
12. **`conflicts_carried_forward`** — structured pointers into the referenced Stage-3 record's own
    `disclosed_conflicts` entries and domain-level abstentions bearing on this result (§J).
13. **`result_status`** — the closed three-value vocabulary (§J), record-level.
14. **`abstention_reason`** — required non-empty whenever `result_status` is `partial` or
    `unable_to_determine`; structurally absent when `completed` (matching `TIER-0004` §F's and
    `VALUATION-0003` §H's identical abstention-path rule).
15. **`cross_asset_handoff`** — a small envelope of **read-only projections** of already-computed fields
    above (ticker, asset_class, result_status, a compact per-family governed-role/status echo, the
    evidence-quality-summary echo) sufficient for a later, separately authorized cross-asset synthesis
    (`XASSET-0001`/`XASSET-0005`, unaffected and not advanced by this filing) to consume without that
    future synthesis needing to re-open or re-derive this record's own internals — matching the identical
    `cross_asset_handoff` envelope pattern already used by the ETF/crypto/functional-doctrine schemas.
16. **Lifecycle/seal fields**: `record_status`, `sealed_at`, `governing_decision` (seal-field usage,
    distinct from item 2's list — matching the existing seal-field naming convention), `drafting_session_or_
    shard_id`, `content_sha256`, `cohort_manifest_entry` — the identical five-field seal-exclusion set every
    prior validator in this program already uses for `canonical_record_hash()`.

**Structurally, mechanically forbidden anywhere in this schema** (§L enforces): a fair value, price target,
or expected-return field presented without its own range/basis; an opaque composite score or blended
cross-family "final number"; a universal ranking score; any buy/sell/add/trim/hold-directive/target-weight/
max-position field; any chart, technical-indicator, or timing field; any coupling to `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, or `margin_state.py`.

### L. Result-validator future contract

The future implementation's `valuation_result_validator.py` — its own dedicated module, **not** an
extension of `valuation_evidence_validator.py`, which remains evidence-only and must continue to reject
valuation-output content as its own §Q design already requires — must, at minimum:

- Enforce closed schema at every level (top-level record, each family entry, each range/scenario-outcome
  entry, each assumptions-ledger entry, the manifest) — reject extra keys, not merely missing ones,
  learning directly from this repository's own disclosed `contender_registry_validator.py` MAJOR finding
  and the archetype/evidence validators' own already-applied fix for the identical class of defect.
- **Independently recompute, never merely trust**, both `archetype_reference.content_sha256` and
  `evidence_reference.content_sha256` via read-only calls to `valuation_archetype_validator.
  canonical_record_hash()` and `valuation_evidence_validator.canonical_record_hash()` respectively — a hash
  mismatch is a hard validation failure, not a warning.
- Enforce range-not-point structure: reject a `valuation_range` entry that supplies only a single point
  with no `low`/`high` (or no `scenario_outcomes[]` for family 7); enforce `low ≤ base ≤ high` where all
  three are populated, with an explicit, disclosed exception path for a scenario-style range that has no
  single "base" (§K.7).
- **Enforce methodology/archetype compatibility** as a live cross-check against `VALUATION-0002` §2's own
  per-family, per-archetype governed-role table (§M) — reject any `methodology_families_applied` entry
  whose `governed_role` is Prohibited or Insufficient basis for adoption for the ticker's own pinned
  primary archetype; reject a `governed_role` value that does not match what the table independently
  produces for that archetype/family pairing (never trust a self-declared `governed_role` string alone).
- Require a `provenance_label` from `VALUATION-0002` §3's exact four-value vocabulary on every assumptions-
  ledger entry — reject an unlabeled assumption.
- Enforce the peer-set (§F) and scenario (§G) subset rules: every applied peer identity and every scenario
  name referenced in a result record must appear among the pinned Stage-3 evidence record's own `included`
  peer candidates / named scenarios respectively — a mechanically checkable, live cross-reference against
  the pinned evidence file, not a self-declared claim.
- Enforce scenario-probability coherence (§G): where every scenario in an applied set carries a weight, the
  sum must fall within the disclosed ±0.02 tolerance of 1.0, unless the set is explicitly disclosed
  non-exhaustive.
- Support and correctly validate the three-value `result_status`/`abstention_reason` path (§J), matching
  every prior abstention-path validator in this program.
- Require `conflicts_carried_forward` to be non-empty whenever the pinned evidence record's own
  `disclosed_conflicts`/domain abstentions bear materially on an applied family — a live cross-check, not a
  self-declared flag alone (learning directly from `reconciliation_validator.py`'s own disclosed MINOR
  defense-in-depth gap and this program's now-standard "a self-declared boolean is not a substitute for an
  independent recomputation" discipline).
- Enforce `cross_asset_handoff` envelope read-only-projection consistency: every summary field checked
  against its own source field elsewhere in the record, never independently computed (the identical
  discipline `recommendation_validator.py`'s own `SS G.6` live-recompute rule and every subsequent
  cross-asset-handoff-bearing schema in this program already applies).
- **Reject any fair-value/price-target/expected-return/opaque-score output field structurally forbidden by
  §K**, plus an independently-derived free-text scan for prohibited recommendation-shaped phrases, chart-
  domain terminology, and word-boundary-matched directive/trading language (`buy`/`sell`/`add`/`hold`/
  `trim`/`exit`/`wait`/`stage`, so "holdings" never false-positives on "hold") — built as its own
  materially different mechanism from any strip/redaction logic elsewhere in the implementation, never the
  same function called twice, per `TIER-0004`'s own corrected lesson on false independence claims (and
  learning directly from the two adjacency/proximity defects `VALUATION-0004`'s own PR #281 delta reviews
  found and fixed in its own free-text scan design — a bounded 0–4 token lookahead near a real figure, not
  bare-word matching, and tolerant of inserted words/alternate verb tense without ever using an unbounded
  wildcard).
- Enforce zero coupling of any kind to `targets.yaml`, `holdings.yaml`, `gates.yaml`,
  `issuer_lookthrough.yaml`, `allocate.py`, or `margin_state.py` — zero import coupling, zero target/tier/
  gate/cap/cluster/allocator/margin field anywhere in the schema.
- Support an opt-in, non-schema-narrowing cohort-completeness function mirroring `valuation_evidence_
  validator.validate_authorized_cohort()`'s exact design (missing/extra-ticker check only, an abstained
  record still counts as present, reused population source via `relationship_validator.
  load_canonical_universe()` or a future execution-authorization decision's own named cohort) — deferred to
  whatever future execution-authorization decision actually names a real cohort (§T); this filing's own
  schema/validator implementation remains roster-agnostic, matching `valuation_evidence_validator.py`'s own
  design precedent exactly.
- Run clean against every applicable pre-existing repository validator, the full `pytest` suite, repo-wide
  YAML/YML and JSON parsing, `git diff --check`, an exact changed-file inventory, and a full protected-path
  scan (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`,
  `issuer_lookthrough.yaml`, every existing `intelligence/**` record, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
  `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, every other `governance/decisions/*.md` — zero diff
  on all of them) before it may be marked ready.
- Achieve decision-catalog reconciliation and exact-head CI green before the implementation PR may be
  marked ready.

### M. Archetype/methodology compatibility enforcement

Restating §L's core requirement in full: a result record may only apply a methodology family whose
governed role — per `VALUATION-0002` §2's already-accepted, unedited, bound-by-reference table — for the
ticker's own pinned `primary_archetype` is Primary candidate, Secondary/corroborative, or Adjustment-
required. A family whose governed role for that archetype is Prohibited or Insufficient basis for adoption
may **never** appear in `methodology_families_applied`, structurally, mechanically, at validation time —
not merely discouraged by prose. Where a ticker's `secondary_archetype` is also populated, the future
execution session may additionally consider that archetype's own governed-role table entries as
**corroborative context only** (never elevating a family that is Prohibited under the primary archetype
merely because it would be permitted under the secondary one) — this filing does not design a blended
primary/secondary compatibility rule beyond that single, narrow, corroborative-only allowance, since
inventing one would risk quietly circumventing the primary-archetype-governs rule `VALUATION-0002` §1
already established as the reason archetype-differentiated methodology selection exists at all.

**Compact restatement of `VALUATION-0002` §2's own table, presented here only to ground §N's batching
rationale below — a mechanical restatement of the already-accepted table, not a new judgment, not an
amendment**: no family reaches Primary candidate for archetype C (financial intermediation) under the
current, unedited table — every family for C resolves to Adjustment-required, Prohibited, or (for family 4)
Secondary/corroborative-adjacent treatment is unavailable since family 4 never reaches Primary for any
archetype. Families 2 and 3 (FCFF/FCFE DCF) reach Primary only for A and G. Family 1 (asset-based/NAV/SOTP)
reaches Primary only for F. Family 5 (relative valuation/multiples) reaches Primary for A and B. Family 7
(scenario/probability-weighted) reaches Primary only for D and E. Families 4 and 6 never reach Primary for
any archetype (inherently corroborative, per the protocol's own family descriptions).

### N. Execution batching design — evaluated, not authorized

This section evaluates the shape a future execution-authorization decision (§T) should consider — it
authorizes no execution and populates no result for any ticker.

**Options evaluated, per the authorizing task's own four candidates:**

1. **One 27-name execution cycle.** Rejected as the recommended default — it collapses five structurally
   different judgment/failure modes (a DCF-primary cohort, a multiples-primary cohort, a SOTP-primary
   cohort, a scenario-primary cohort, and a no-clean-primary-family cohort) into one review unit, exactly
   the risk `OPS-0008`'s own Research Wave Protocol was adopted to avoid for content batches of comparable
   scale, and the identical reasoning `VALUATION-0003` §G already applied when it sharded its own 27-name
   archetype-assignment implementation into five internal review shards rather than one undifferentiated
   pass.
2. **Method-homogeneous batches.** **Recommended.** Grouping by which methodology family reaches Primary
   candidate for the ticker's own sealed archetype (§M's compact restatement) produces four natural
   cohorts from the corrected 27-name archetype distribution (`A:6 · B:6 · C:2 · D:2 · E:1 · F:8 · G:2`,
   independently re-derived from the merged `intelligence/valuation_archetype/*.yaml` records per §Q):
   - **DCF/compounder cohort** — archetypes A + G (8 tickers), family 2/3 primary.
   - **SOTP/diversified cohort** — archetype F (8 tickers), family 1 primary.
   - **Relative-valuation/adjustment cohort** — archetypes B + C (8 tickers), family 5 primary for B; no
     family reaches Primary for C, requiring materially more careful, adjustment-required-heavy treatment —
     grouped with B rather than left as its own 2-ticker unit, since both share the "not DCF-primary, not
     SOTP-primary, not scenario-primary" failure mode and a 2-name-only governance unit would be
     disproportionately thin relative to `OPS-0008`'s own 5-6-name default wave size.
   - **Scenario/cyclical-binary cohort** — archetypes D + E (3 tickers), family 7 primary. Deliberately
     smaller than the other three, justified as an intentional use of the smaller-wave exception this
     repository has already exercised for a genuinely small, coherent group with no larger natural
     grouping available (matching `PI-0031`/`REL-0005`'s own single-name and small-cohort precedent for
     an analogous "no larger coherent group exists" situation).
   Total: 8 + 8 + 8 + 3 = 27, matching the full cohort exactly, zero overlap, zero omission.
3. **Archetype batches (seven, one per A–G letter).** Rejected as needlessly fragmented relative to option
   2 — archetypes A and G share an identical Primary family (2/3), and B and C, while sharing no Primary
   family, share the identical "no clean single-family Primary path" failure mode that argues for grouped,
   not split, review attention; splitting into seven batches purely by letter would produce two 1-2-ticker
   batches (C, E) with no coherent additional review benefit over the four-cohort grouping in option 2.
4. **Per-ticker execution.** Rejected outright — this repository's own established practice for every
   comparable-scale content-population program in this domain (`VALUATION-0003`'s archetype assignment,
   `VALUATION-0005`'s evidence population) has consistently used internally sharded batch cycles, never a
   27-PR-per-ticker design; per-ticker execution would multiply governance overhead (28× the review/
   correction/acceptance/merge/post-merge-verification cycle) without a corresponding gain in review
   quality, and directly contradicts `OPS-0008`'s own explicit rejection of exactly this overhead pattern.

**This filing recommends, but does not authorize, four method-homogeneous execution batches** (DCF/
compounder; SOTP/diversified; relative-valuation/adjustment; scenario/cyclical-binary), internally sharded
for drafting efficiency within each batch, one primary authoring session per batch mutating the repository,
matching `VALUATION-0003` §G's and `CHART-0002`'s own established shard-review architecture. **Exact
per-ticker batch membership is deferred to the future execution-authorization decision (§T)** — this
filing works from the already-published aggregate archetype distribution and does not itself re-open or
re-derive individual ticker-to-archetype assignments beyond what is already sealed and public in
`intelligence/valuation_archetype/`.

### O. Blindness / sanitizer decision

**Full Milestone-6-style blind-drafting with a dedicated sanitizer is not required for Stage-4 execution,
by design, for the majority of the work — but a narrower, targeted isolation rule is required for two
specific, genuinely anchoring-vulnerable judgment sub-steps.** Reasoning:

Archetype assignment (`VALUATION-0003`) required full blind sharding because it was a discrete, categorical
taxonomy judgment ("which of seven buckets does this business belong in") highly vulnerable to a single
anchor — a session that already knows a ticker's `portfolio_role_ref`/`conviction.rating`/target weight
could easily rationalize a categorical fit toward whatever the existing policy already implies. Stage-3
evidence population (`VALUATION-0005` §M) required **no** sanitizer, explicitly, because it is objective,
externally-sourced financial fact — a revenue figure or a segment's disclosed profit is not a judgment call
the way an archetype label is, and `VALUATION-0005`'s own precedent ("Stage-3 evidence is objective
financial fact, not a policy-contamination-risk judgment call the way archetype/tier assignment was") is
directly on point and independently re-confirmed sound by this filing.

Stage-4 execution sits between these two precedents, closer to the evidence-population end than the
archetype-assignment end, for three independent reasons: (1) every numeric input feeding a Stage-4 range is
itself drawn from already-sealed, already-redacted-of-policy Stage-3/Stage-2 evidence, or from external
market data sourced at execution time — none of it is `portfolio_role_ref`/`conviction`/target-weight text
sitting in the same file the way Milestone 6's own three disclosed correction rounds found; (2)
`VALUATION-0002` §3's mandatory range-plus-sensitivity-plus-provenance-ledger doctrine structurally
constrains how far a single judgment call can move a final output — a WACC built from four individually
sourced, individually provenanced components is materially harder to silently anchor than a bare category
label; (3) the compatibility enforcement in §M mechanically forecloses the most severe form of policy-
driven bias (applying a Prohibited family to make a holding "look" more favorably valued) at the validator
level, independent of any human or session-level discipline.

**However, two specific sub-judgments remain genuinely, non-hypothetically anchoring-vulnerable and are
not adequately constrained by §M's mechanical compatibility check alone**: (a) **applied-peer-set
selection** (§F) — which Stage-3-included candidates actually get used, and which get excluded with a
"disclosed rationale" that could easily be reverse-engineered to produce a more flattering multiple; and
(b) **scenario-probability assignment** (§G) — which named scenario gets more weight, a judgment as
subjective and single-scalar-movable as a conviction rating itself. **Minimum necessary isolation rule,
adopted for exactly these two sub-steps and no others**: the future execution session performing either
judgment must not have `portfolio_role_ref`, `conviction.rating`, `target_pct`, current holding size, or
`gates.yaml` status open, cited, or referenced while making that specific call, and the resulting written
rationale must independently justify the choice from Stage-3 evidence and market/peer facts alone — an
explicit "why this peer / this probability weight, sourced from evidence, not from portfolio status"
disclosure requirement, mechanically checkable by the same free-text/keyword-absence scan pattern §L
already requires for prohibited output content, extended to scan the peer-exclusion and scenario-weight
rationale fields specifically for portfolio-policy vocabulary. This is a documentation/procedure-level
isolation requirement, not a full sanitizer-and-blind-shard architecture — deliberately the smallest
sufficient control given the actual, disclosed size of the risk, avoiding the over-engineering `OPS-0008`
§12 already warns this repository's own protocol design against.

### P. Segment/SOTP evidence — a disclosed, non-blocking finding, not a schema amendment

Independently confirmed this session (Preflight above): the live `segment_evidence` schema's
`_SEGMENT_ENTRY_ALLOWED_KEYS` supports exactly `segment_name`, `revenue`, `profit`, `cash_flow` — no
`segment_assets` or `segment_capex` key exists anywhere, and none appears in any of the 27 populated
records. Per the authorizing task's own explicit stop condition, this filing evaluated whether this is a
**blocking** deficiency requiring a human-governance amendment decision, and finds it is **not**: a
segment-level sum-of-the-parts application (archetype F's Primary family, family 1) can be constructed from
segment revenue/profit/cash-flow alone via a relative-valuation-style per-segment multiple approach
(applying a sourced peer/industry multiple to each segment's own disclosed revenue or profit, per §F's own
peer-selection discipline, extended to the segment level) — a segment-level asset-based/replacement-cost
approach specifically would additionally require segment-level asset evidence this schema does not carry,
but that narrower sub-case is handled cleanly by this filing's own existing abstention path (§J): a future
execution session lacking segment-level asset evidence for a specific segment discloses that gap and
abstains on the asset-based sub-method for that segment, without blocking the SOTP family as a whole or the
family's other segments. **No schema amendment to `VALUATION-0004`/`VALUATION-0005`'s already-accepted
evidence architecture is proposed or authorized by this filing.** This finding is recorded here, disclosed,
and left for a future evidence-population or schema-review session to revisit only if real execution
experience against archetype-F tickers demonstrates the gap is more material in practice than this
filing's own analysis concludes.

### Q. Lane M — PR #283 (`VALUATION-0005`-authorized Stage-3 evidence-population implementation) lifecycle,
independently re-verified and recorded

Independently re-verified via the GitHub API this session, not assumed:

- PR #283, "WS-0015: VALUATION-0005 Stage-3 — equity valuation evidence population (27 companies)," base
  `main` @ `272c0e770c16afefe68c5396e7d4e661283b35db`, head `ff4becc8eb4f6129f78f1361ac4d3bee37eb80bd`, 35
  changed files, 4 commits.
- Original independent exact-head review: `pullrequestreview-4890579208`, anchored to head
  `e81596a5c47689bb85672e381ffe1785193cf8ef` — **CHANGES REQUIRED**, 0 BLOCKING / 2 MAJOR / 1 MINOR / 2
  NOTE — both MAJOR findings targeted the retained audit document's own narrative miscounts (segment
  coverage stated 18/9, actually 14/13, with ICE mislabeled abstained and COST/ETN omitted from the table;
  market-observed coverage stated 25/2, actually 24/3, omitting GOOGL's genuine domain-level abstention),
  not the underlying sealed evidence records, manifest, generator, validator, or tests, which the same
  review independently verified sound throughout (including a byte-for-byte regeneration check against
  `ticker_data.py` and a live re-search confirming the Visa/Amazon fabrication-risk spot-checks were not
  errors). The one MINOR finding was a stale PR-body file/commit count.
- Bounded correction: commit `ff4becc8eb4f6129f78f1361ac4d3bee37eb80bd` — corrected the retained audit's
  §6.2/§6.3/§7 segment and market-observed counts and abstention tables to the mechanically recomputed
  14/13 and 24/3 figures; corrected the PR body's own file/commit counts. **No sealed evidence record,
  manifest, generator, validator, or test changed** — independently reconfirmed via `git diff`.
- Corrected-head delta review: `pullrequestreview-4890605238`, anchored exactly to
  `ff4becc8eb4f6129f78f1361ac4d3bee37eb80bd` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING
  / 0 MAJOR / 0 MINOR / 0 new NOTE — independently reproduced both corrected counts against the live sealed
  records, confirmed the correction touched exactly one file, and confirmed zero diff on every sealed
  record/manifest/generator/validator/test.
- Principal acceptance: `issuecomment-5229973691`, at exact head `ff4becc8eb4f6129f78f1361ac4d3bee37eb80bd`.
- Exact-head CI: run `31296610587`, job `93202615822`, `status: completed`/`conclusion: success`.
- Merge: `b97ad2a2a23554b6072340ebff9ceddc799b1a22`, parents
  `272c0e770c16afefe68c5396e7d4e661283b35db` and `ff4becc8eb4f6129f78f1361ac4d3bee37eb80bd`
  (independently re-confirmed via `git show --no-patch --format='%H %P'`).
- Merge-commit CI: run `31297094534`, `status: completed`/`conclusion: success` (independently re-fetched
  and matched to the merge SHA's own `head_commit`, distinct from the exact-head CI run above).
- **Post-merge validation independently reproduced this session**: `valuation_evidence_validator.py` →
  `OK (28 result(s))`; `test_valuation_evidence_validator.py` → 329 passed; full repository `pytest` → 3853
  passed, 0 failed at that commit (later independently re-confirmed at 4042 passed, 0 failed at this
  filing's own current head, after `XASSET-0006`/`XASSET-0007`/`XASSET-0008`'s own intervening merges);
  decision catalog independently rebuilt at 99 decisions, 0 issues at that commit.

### R. Register synchronization (Lane M, this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0015` entry receives, additive only — no existing gate's own text
edited:

1. A new `valuation0005-stage3-implementation-post-merge-verification` gate recording §Q's independently
   reconfirmed PR #283 facts in full, including the corrected final segment/market-observed coverage
   figures — this corrects the stale pre-correction narrative counts without editing the existing
   `valuation0005-stage3-implementation` gate's own text.
2. A new `valuation0006-methodology-application-policy-and-result-architecture` gate (`status: in_progress`,
   `pr: null` — this filing does not mark its own unmerged work complete, matching every prior filing's
   identical self-reference discipline in this repository).
3. `status` remains `proposed`. `priority` remains `secondary`. `dependencies` remains `[]`.
4. `active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`, `blocker`, `next_action`,
   `completion_criteria`, and `authorized_by` updated to this filing's own live state.

No other workstream entry is touched. `WS-0005` and `WS-0014` are unaffected.

### S. Non-authority — explicit, exhaustive

This decision authorizes no:

- Fair value, price target, expected return, or upside/downside calculation for any real company.
- Actual DCF computation, actual peer selection applied to a computation, actual discount-rate value,
  actual WACC, actual beta, actual ERP value, actual terminal growth rate, or actual scenario probability
  for any real company.
- Real-company valuation-result population of any kind, in the schema this filing governs or any other.
- Resolution, closure, or narrowing of `TIER-0009` §K's `valuation_required` status on any equity.
- Discount-rate-evidence population for any real company (§D's disclosed prerequisite gap remains
  unclosed by this filing).
- Any amendment to `VALUATION-0004`/`VALUATION-0005`'s already-accepted Stage-3 evidence schema, including
  the segment-evidence key set disclosed non-blocking in §P.
- Target, tier, holdings, gate, capital-priority, cap, cluster, or allocator change of any kind.
- Margin policy, buy-ladder, chart ingestion, or chart interpretation of any kind.
- `CONTENDER-0003` or any further contender-registry regeneration/legacy-recovery work.
- Any ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content — remains `WS-0014`/`XASSET-0001` §C/§D's own separate, unaffected scope.
- Any overlap/concentration modeling, cross-asset synthesis, or unlevered-versus-levered allocation
  testing — remains `XASSET-0005`'s own separate, unaffected scope.
- Any order or trade.
- Any historical backtest of a discount rate, terminal-growth assumption, peer multiple, or scenario
  probability against subsequent stock-price performance, under any framing (§H).
- Any edit to `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
  `VALUATION-0001`, `VALUATION-0002`, `VALUATION-0003`, `VALUATION-0004`, or `VALUATION-0005`.
- Any actual schema, validator, or test code — this filing authorizes a future implementation; it
  performs none of that work itself.

### T. Stage-4 closure semantics — precise, staged, not conflated

Four distinct states exist in this domain, extending `VALUATION-0004` §O one layer forward. This decision
reaches exactly the first:

1. **Stage-4 methodology-application policy and result architecture governed (this decision).** Establishes
   the seventeen governed conventions (§C–§J), the result-schema architecture (§K), the validator contract
   (§L), archetype/methodology compatibility enforcement (§M), the recommended (not authorized) execution-
   batching design (§N), the blindness/isolation decision (§O), and the disclosed, non-blocking segment/
   SOTP finding (§P).
2. **Result schema/validator/test implementation merged (a future, separate PR — not this filing).**
   Mirrors `VALUATION-0004` §O's identical state-2 discipline: this filing's own governance-design step does
   not itself supply usable result infrastructure — a design document alone gives a future valuation
   execution nothing to write into. Until that future PR merges, no result record of any kind can exist.
3. **Discount-rate-evidence population and any other real-company evidence-population extension a future
   execution unit finds it needs (a further, separately authorized, later unit — not authorized by this
   filing or by the implementation it authorizes).** §D's disclosed prerequisite gap remains open.
4. **Real-company valuation execution authorized (a further, separately authorized, later unit, requiring
   states 2 and 3 for the company/family in question, plus `VALUATION-0002` §6.3(a)/(c)/(d), plus its own
   independent review and principal acceptance before any output is produced).** Not reached, not
   approached, not implied by this filing. A separate future decision — provisionally identified as
   `VALUATION-0007`, or whichever `VALUATION-####` identifier is next unused at the time it is actually
   filed — must authorize the real-company execution population after this decision (`VALUATION-0006`) is
   merged and independently accepted, and after state 2 (schema/validator/test implementation) is itself
   merged and independently accepted.

**This filing claims only state 1.** It does not claim state 2, 3, or 4 for any company, and does not claim
that satisfying state 1 shortens, narrows, or pre-commits the scope of states 2–4's own future
authorizations — including §N's own recommended (not authorized) batching shape, which a future execution-
authorization decision remains free to adopt, modify, or reject on its own merits.

### U. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0006-stage4-methodology-application-policy-and-result-architecture.md`
   (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0006`).
3. `operations/WORKSTREAMS.yaml` (§R above).
4. `CLAUDE.md` (one Decisions Log pointer entry).
5. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 102 → 103, exactly the
   two hardcoded assertions independently located this session at
   `test_real_repository_catalog_builds_all_71_with_no_issues` and
   `test_real_repository_model_and_render_succeed_end_to_end`).

**No other file is touched.** No production code, no `intelligence/**` record, no `PROTOCOL_V1.md`,
`METHODOLOGY_EVALUATION_REPORT.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` change, no `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml` change.

### V. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1 (`OPS-0009` Lane G — new authorization, full weight, never reduced), complete
any required bounded correction and exact-head re-review, and receive explicit principal acceptance before
it may be marked ready or merged. **This decision does not mark itself ready and does not authorize its own
merge.** No result-architecture implementation PR may open, and §§A–T above are not effective, until this
PR merges to `main`.

## Rationale

**Why govern methodology-application policy and result architecture now, separately from the schema/
validator implementation and from any execution.** Matches this repository's own established "define, then
later authorize implementation, then later still authorize population/execution" discipline applied at
every prior layer of this program: `VALUATION-0002` (methodology doctrine) before `VALUATION-0003`
(archetype authorization) before its own implementation; `VALUATION-0004` (evidence-architecture governance)
before its own implementation before `VALUATION-0005` (evidence-population authorization) before its own
implementation. This filing mirrors that exact discipline one layer deeper — governance-design, then
implementation, then (in a still-later, separately authorized filing) execution — rather than collapsing
policy design, schema/validator code, and real-company output into one review unit before any of the three
has been independently reviewed on its own terms.

**Why a new, separate result category rather than extending the evidence or archetype schemas.** The
result layer answers a structurally distinct question from either upstream layer — "what does a
methodology, applied under governed conventions, actually produce" — not "what business-model category does
this company fit" (archetype) or "what raw financial facts exist" (evidence). Every structurally analogous
need in this repository's history (Theme Intelligence, relationship mapping, Milestone 6 classification,
ETF/crypto classification, the archetype layer, the evidence layer itself) has been resolved with its own
new companion structure, never an amendment to an existing one — this filing follows that precedent exactly.

**Why discount-rate/terminal-value/peer-selection/scenario-probability policy is designed now, at the
application-policy layer, rather than left for a future execution filing to invent ad hoc.** `VALUATION-0004`
§I/§J/§K each explicitly reserved these exact questions to "a later, separately authorized application-
phase policy decision" — this filing is that decision. Designing the conventions now, under full Lane G
review, prevents a future execution-authorization filing from having to invent load-bearing numeric/
procedural conventions under the time pressure of also trying to get real company output reviewed and
accepted — separating "what convention governs" from "did we apply it correctly to this company" the same
way this repository has separated every other design-then-population pair in this program.

**Why method-homogeneous batching (§N) is recommended over a single 27-name cycle or per-archetype/per-
ticker fragmentation.** The four cohorts this filing derives directly track genuinely different judgment/
failure modes (DCF-primary vs. SOTP-primary vs. relative-valuation/adjustment-heavy vs. scenario-primary),
matching `OPS-0008`'s own Research Wave Protocol reasoning for why a single undifferentiated pass over a
comparable-scale population under-serves review quality, while avoiding the opposite failure of
fragmenting into seven thin per-archetype batches (two of which would be 1-2-ticker units with no
coherence benefit over the four-cohort grouping) or twenty-seven single-ticker units (rejected outright by
this repository's own established batch-cycle practice for content-population work at this scale).

**Why the two-peer minimum (§F) and the ±0.02 probability-coherence tolerance (§G) are `NUM-0001` class 5,
not class 3 or 4.** Neither figure is derived from range-establishing evidence internal to this repository
— `VALUATION-0004` §H and `VALUATION-0005` §D already established the discipline of declining to invent an
unsupported numeric parameter and instead adopting a disclosed, provisional, reviewable guardrail with an
explicit evidence-driven revisit condition; this filing applies that identical discipline to every new
numeric convention it introduces, rather than presenting any of them as though they were empirically
optimized.

**Why full blind-drafting/sanitizer architecture is not adopted for the whole of Stage-4 execution, but a
narrower isolation rule is adopted for applied-peer-set selection and scenario-probability assignment
specifically.** §O's own analysis is not restated here — the short version is that Stage-4 execution's
inputs are already-sealed, already-redacted-of-policy evidence plus external market data, materially unlike
archetype assignment's own vulnerability to a single categorical anchor, while two specific sub-judgments
remain genuinely anchoring-vulnerable and warrant a targeted, disclosure-based control rather than either
no control at all or the full Milestone-6-style architecture `VALUATION-0005` §M already found unnecessary
for the adjacent, less judgment-heavy evidence-population step.

**Why `category: valuation_application_governance`, a new category distinct from every prior `VALUATION-####`
category.** `VALUATION-0002` adopts methodology-selection doctrine; `VALUATION-0003` authorizes archetype-
assignment work; `VALUATION-0004` governs evidence architecture; `VALUATION-0005` authorizes evidence
population. This filing governs a structurally distinct fifth act — application-policy design and a new
result architecture, performed by none of the prior four — matching the precedent `TIER-0001` established
(`tier_classification_governance`) and that `VALUATION-0002`'s and `VALUATION-0004`'s own Rationale sections
each explicitly cite as the model for exactly this situation.

## Alternatives Considered

- **Combine methodology-application-policy governance with the future schema/validator implementation in
  one filing.** Rejected — this repository's own established "define, then later authorize implementation"
  discipline (see Rationale) treats policy design and code implementation as separate review units at
  every prior layer of this program; no exception is warranted here.
- **Combine this filing with a real-company execution-authorization decision, "to save a governance
  cycle."** Rejected outright — the authorizing task's own explicit boundary bars any real-company
  valuation, and doing so would also violate `VALUATION-0002` §6.3's own explicit sequencing (archetype
  assignment, then RQ4 closure, then evidence population, then application-policy design, then execution —
  execution sits logically after policy design, never folded into the design step itself).
- **Invent a fixed numeric ERP value, terminal-growth ceiling, or discount-rate default now, so a future
  execution unit has a concrete number to start from.** Rejected — no existing repository evidence supports
  a single specific number for any of these over real, tested alternatives; `NUM-0001`'s own provenance-
  classification discipline treats an unsupported numeric parameter as its own defect class, and this
  filing's own consistent practice (§D, §E, §F, §G) is to design the *convention* for sourcing/combining
  these inputs, never the number itself.
- **Adopt full Milestone-6-style blind-drafting/sanitizer architecture for all of Stage-4 execution, "to be
  safe."** Rejected as disproportionate to the disclosed, analyzed risk (§O) — `VALUATION-0005` §M already
  established that objective, externally-sourced evidence work does not require this repository's heaviest
  contamination-control architecture, and this filing's own analysis finds Stage-4 execution sits closer to
  that end of the spectrum than to archetype assignment's end, warranting a narrower, targeted control
  instead of the heaviest available one by default.
- **Amend the Stage-3 evidence schema now to add `segment_assets`/`segment_capex` fields, closing the
  disclosed gap in §P pre-emptively.** Rejected — the authorizing task's own explicit stop condition
  requires treating this as a human-governance decision only if the gap is genuinely blocking; this filing's
  own analysis (§P) finds it is not, since the abstention path already handles the narrower asset-based
  sub-case cleanly, and amending an already-accepted evidence schema without a demonstrated blocking need
  would exceed this filing's own bounded design-governance scope.
- **Design a numeric confidence-discount formula for secondary-only sourcing (§I), so evidence-quality
  treatment produces a quantitative adjustment rather than a qualitative gate.** Rejected — no evidence
  establishes what such a discount factor should be, and inventing one would itself be exactly the kind of
  false precision `VALUATION-0002` §3's doctrine exists to prevent; the qualitative "may not reach
  `completed` while a material conflict/abstention bears on required inputs" rule achieves the same
  protective effect without fabricating a number.

## Consequences

**What changes.** A future, separate implementation PR may now be opened to build the `intelligence/
valuation_results/` schema, its dedicated validator, and its test suite as an empty/scaffold structure —
but only after this governance PR itself is independently reviewed and principal-accepted. Once that future
implementation merges, this filing's methodology-application-policy conventions (§§C–J), result-schema
architecture (§K), validator contract (§L), and compatibility-enforcement rule (§M) become the binding
specification any future real-company execution must follow. `WS-0015`'s register entry reflects PR #283's
confirmed merge (with the corrected final segment/market-observed coverage figures) and this filing's own
methodology-application-policy-and-result-architecture step.

**What does not change.** No real company's valuation-result record exists or is populated. No real company
is valued. No fair value, price target, expected return, discount rate, WACC, beta, ERP, terminal growth
rate, applied peer set, or scenario probability is assigned to any real company. `discount_rate_evidence`
remains abstained for all 27 canonical equities' Stage-3 records — this filing does not populate it.
`TIER-0009` §K's `target_and_range`/`maximum_position_size` `valuation_required` status is unchanged on all
27 canonical equities. `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `docs/
PORTFOLIO_INTELLIGENCE_SPEC.md`, and `VALUATION-0001` through `VALUATION-0005` are all unedited. No target,
tier, holdings, gate, cap, cluster, allocator, margin, or ladder value changes. No Company/Theme/
relationship/classification/reconciliation/recommendation/archetype/evidence Intelligence record changes.
No chart evidence of any kind is consumed. `CONTENDER-0003`, ETF/crypto evaluation, and cross-asset
synthesis remain unaddressed. `WS-0005` and `WS-0014` are unaffected.

---

**No company was valued.** `VALUATION-0006` governs Stage-4 methodology-application policy and
valuation-result architecture only; real-company valuation execution remains separately unauthorized. The
27-company cohort remains a bounded first equity-valuation cohort, not the exhaustive Portfolio-HQ
contender universe.
