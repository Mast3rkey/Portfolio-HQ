---
decision_id: XASSET-0026
date: 2026-08-15
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0016, XASSET-0018, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, LEVEL2-0001, RISK-0001, RISK-0002, RISK-0003, RISK-0004]
supporting_artifact: null
file: governance/decisions/XASSET-0026-level1-endpoint-evidence-program-shape-and-sleeve-selection-basis.md
---

## Context

XASSET-0025 is effective (PR #324, accepted head `a2ebf6e3f466d6f954d084e717600bab2dd6e5be`, merge
`99873d39c3e967d7a772ae65526349fb01a0a7e3`). Its Outcome C —
`NO_QUALIFYING_ENDPOINT_SOURCE_IN_ACCEPTED_CORPUS` — determined that no accepted source supplies a
qualifying Level-1 sleeve-share bound for any sleeve on either bound, all eight cells
`NO_CANDIDATE_FOUND`, and that two things are therefore missing and are **distinct requirements**:
purpose-built endpoint evidence, and competent Level-1 endpoint authority.

XASSET-0025 §O.5 then recorded, deliberately, that accepted authority does not settle their mandatory
ordering or packaging, and declined to settle it — reasoning that "a filing that disclaims creating
anything should not narrow a future unit's lawful option set as a side effect of describing a gap."

That leaves the program unable to describe the next expensive commitment. Three questions stand
between XASSET-0025 and any charter, and none is answerable by simply beginning:

> How many sleeves must the first purpose-built endpoint-evidence program cover, and on what basis?
> Must evidence and authority be separate lifecycles, and in what order?
> Must a representation rule exist before purpose-built endpoint evidence does?

Each is a question about accepted authority rather than about evidence, and each is therefore
answerable now, cheaply, before anything is commissioned. This filing answers them. It is
governance-only: it reads accepted authority and determines what that authority already permits,
forbids, and leaves open. It creates no endpoint, selects no sleeve, commissions and runs no
research, grants no authority, defines no representation rule, and extends no snapshot.

**Preflight, independently re-verified this session, not inherited.** GitHub `main`, `origin/main`,
and local `HEAD` all at `99873d39c3e967d7a772ae65526349fb01a0a7e3`; working tree clean; zero open
pull requests; no competing mutation lane; PR #324 confirmed merged via the GitHub API with parents
`4ec64c13552c101e6e132c295617789926b5066a` and `a2ebf6e3f466d6f954d084e717600bab2dd6e5be`, and
merge-commit CI run `31908670754` `completed` / `success` at that exact `head_sha`; decision catalog
127 rows with `issues == ()`; `XASSET-0026` confirmed unused repository-wide;
`level1_application_schema.APPLICATION_AUTHORIZATION_REGISTRY` confirmed empty
(`MappingProxyType({})`); no `intelligence/level1_application/` artifact; the XASSET-0021 §N matrix
unchanged at 14 / 14 / 2 with `application_time_author_or_reviewer_judgment_remaining: 2`. Every
premise below was re-read from the merged accepted sources themselves rather than from any prior
session's summary. Two read-only preflights described to this session were treated as planning
observations only and are not repository authority; where their framing and the accepted text
diverge, the accepted text controls and §E records the divergence.

## Decision

### A. Lifecycle, authority, and controlling identity

`OPS-0009` Lane G, governance-only. Effective on merge of this filing after its own independent
exact-head review, principal exact-head acceptance, and immediate post-merge verification. Until then
it determines nothing.

Controlling upstream identity, unedited by this filing: XASSET-0019, XASSET-0020, XASSET-0021,
XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, NUM-0001, LEVEL2-0001, and the accepted RISK
corpus. Where this filing and any of them appear to differ, they control and this filing is wrong.

### B. Scope

In scope: determining, from accepted authority alone, (i) what the lawful *unit* of endpoint-supporting
evidence actually is; (ii) whether any accepted, non-convenience basis lawfully selects a sleeve or a
proper subset of sleeves today; (iii) the coverage shape of the first purpose-built endpoint-evidence
program; (iv) whether accepted authority fixes an ordering or a packaging between evidence and
authority, addressing XASSET-0025 §O.5 as far as that authority permits; (v) whether a representation
rule must precede purpose-built endpoint evidence; (vi) the architectural constraints the smallest
lawful successor program must carry; and (vii) the exact next authorized successor action.

Out of scope and not performed: any endpoint, bound, percentage, range, or sizing; any sleeve
selection or preference; any research, data acquisition, backtest, research design, protocol,
pre-registration, or research charter; any methodology amendment; any representation rule or
representation-set designation; any snapshot extension or schema successor; any application authority
or registry population; any Level-2 work; any liquidity determination; any RISK rerun, refresh, third
attempt, or lapsed-parameter reuse. `/private/tmp/phq-risk0001-results` was not accessed.

**Sleeve-agnosticism was maintained procedurally, not merely asserted.** Every candidate selection
basis in §E was tested against all four sleeves under the identical standard before any disposition
was recorded, and §E.7 states the one asymmetry the corpus contains and why it again does not select.

### C. The endpoint quantity and sleeve ontology, adopted unchanged

XASSET-0024 §C's definition of the endpoint quantity is adopted verbatim by reference and is not
restated, reinterpreted, or narrowed: **a LOWER or UPPER bound on one named sleeve's share of one
exact normalized unit of prospective, unlevered, asset-side capital**, excluding debt, debt reduction,
margin buying power, leverage, and buffer state, with `UNSIZED_UNASSIGNED_CAPITAL` as the unresolved
complement and never an endpoint source or residual plug.

The four Level-1 sleeves are XASSET-0020 §B's closed set: `equity`, `fund_broad_market`,
`fund_gld_defensive`, and `crypto`. The six unordered pairs are XASSET-0020 §H's closed set.

**One consequence of §C carries through every determination below and is stated once here.** However
an endpoint is admitted, and under whichever DRIVER class, *the bound it states is always about one
named sleeve*. Evidence whose subject matter is a pair may support such a bound; it may never yield a
relative ranking, a comparative score, or a split between two sleeves in place of a bound. A relative
statement is not an endpoint.

### D. Determination A — evidence-item scope and endpoint/output coverage are different questions

XASSET-0025 §J determined that the future research question can be *stated* sleeve-agnostically but
its *evidence* cannot be, because "There is no sleeve-independent DRIVER class." That is correct and
was re-verified directly this session against XASSET-0020 §E.1. What that observation governs, and
what it does not, has to be stated carefully, because the two are easy to run together and running
them together would impose a research-design constraint accepted authority does not supply.

**The two questions.** (a) The minimum *subject-matter scope of an individual DRIVER evidence item* —
what a single admissible item must be about. (b) The *endpoint/output coverage of a program* — for how
many sleeves a program is attempting to produce bounds. These are independent, and §C already fixes
the bridge between them: a bound always states the §C quantity **for one named sleeve**, and evidence
whose subject matter is a comparison or a pair may support such a bound.

Read exactly as XASSET-0020 §E.1 states them, and recording only what its own words fix:

| # | DRIVER class | §E.1's own scope language | Minimum evidence-item subject-matter scope |
|---|---|---|---|
| 1 | `portfolio_function` | "**the sleeve's** directly evidenced job in the prospective portfolio" | **One sleeve** |
| 2 | `valuation_opportunity_cost` | "the cost of assigning the marginal dollar **here rather than to the direct alternative**" | **Comparison-scoped**; the lawful comparator is *not* fixed to a second sleeve by §E.1 |
| 3 | `downside_path_risk` | "**directly comparable** loss shape, depth, or path evidence" | **Comparison-scoped**; comparator not fixed by §E.1 |
| 4 | `recovery` | "**directly comparable** recovery or time-underwater evidence" | **Comparison-scoped**; comparator not fixed by §E.1 |
| 5 | `diversification_cobehavior` | "**direct pair evidence** about duplication, shared loss mechanisms, or offset behavior" | **One unordered pair** — the only class §E.1 expressly fixes to a pair |
| 6 | `sleeve_deployability` | "**sleeve-level** convertibility, lockup, or implementation friction" | **One sleeve** |

**Why the comparator is left unresolved rather than assumed to be a second sleeve.** XASSET-0020 §H
provides that "Each of the four sleeves must also be compared directly with
`UNSIZED_UNASSIGNED_CAPITAL`," which is a direct alternative that is not a sleeve. "The direct
alternative" and "directly comparable" are therefore not textually synonymous with "a second
investable sleeve," and this filing does not make them so. What the lawful comparator may be for a
given item is a property of an evidence design that does not exist; **no comparator rule is supplied,
narrowed, or implied here.**

**Two consequences, both stated so a successor does not infer a third.**

1. **Comparative or pair-subject evidence does not oblige a program to produce a bound for the other
   side of the comparison.** A program whose output target is one sleeve may lawfully gather direct
   comparisons between that sleeve and its alternatives; using such evidence creates no second sleeve
   output. This follows from §C and is stated here because the contrary reading is the natural one.
2. **No DRIVER class is closed to a program by its output coverage alone.** This filing determines no
   restriction of the admissible class set based on how many sleeves a program targets, and none
   should be read into the table above — it records evidence-item subject matter only.

**What remains genuinely open.** Which DRIVER class will admit any future endpoint-supporting evidence
is a property of an evidence design that does not yet exist, and no accepted authority fixes it now.
Program *coverage*, by contrast, is answerable today, because it turns on selection authority rather
than on evidence design — which is §E's question, not this one's.

### E. Determination B — no accepted, non-convenience basis selects a sleeve or a subset today

Every candidate basis reachable from accepted authority or from the planning material described to
this session was tested and is recorded, including those that returned nothing, so that "rejected" is
verifiable rather than assumed.

**E.1 — Express declination by both immediate predecessors.** XASSET-0024 §B states "**No sleeve is
selected, preferred, or examined ahead of any other by this filing**," and its Alternatives Considered
rejected "Begin with a single sleeve, or with GLD as the narrowest representation case" on the ground
that doing so "would have been sleeve selection without authority." XASSET-0025 §J states "**No first
sleeve is selected here, and none is compelled**," and its Alternatives Considered rejected naming a
first sleeve because "No accepted evidence compels one." No accepted decision anywhere selects,
prefers, ranks, or sequences a sleeve.

**E.2 — Evidence coverage, maturity, availability, or tractability. Not an accepted economic selection
basis.** This is the class of basis a successor is most likely to reach for, and what accepted text
establishes about it must be stated exactly, without extension. XASSET-0020 §D provides that "research
volume, evidence maturity, or a need to make totals balance is **never an answer**" to the
marginal-capital question, and §F.2's sleeve-function row provides that "Evidence coverage, maturity,
`sizing_readiness`, and capital eligibility **may not imply size or preference**."

Those clauses bar **economic allocation inference**. Their consequence here is therefore precise and
limited: none of these properties supplies an accepted economic basis for preferring one sleeve, and
none may be permitted to imply size or preference. A subset selection resting on them would have no
accepted economic basis today, which is sufficient for this filing's question.

**What this filing does not determine, and expressly declines to.** It does not determine that these
properties are categorically unlawful grounds on which a future, separately authorized governance act
could sequence or scope research for operational reasons — cost, availability, tractability, or
currentness — while expressly quarantining that sequencing from any economic preference or sizing
inference. Research sequencing is not itself sizing, and no accepted text this filing located converts
operational sequencing into economic preference. Whether such an act is sound, and what non-preference
firewall it would need, are questions for that act on its own stated terms and its own review. Nothing
here forecloses it; see §E.8.

**E.3 — Canonical sleeve order. Expressly foreclosed.** XASSET-0020 §L classifies "Canonical pair and
sleeve orders" as an "Engineering/procedural constant over the closed ontology," binding "for
determinism; **no economic effect**." Selecting `equity` because it is first in XASSET-0020 §B's
canonical list would convert a determinism constant into an economic selection basis, which that row
forecloses in terms.

**E.4 — Missing-pair structure.** XASSET-0020 §I records that the accepted non-RISK relationship
corpus contains no direct `fund_broad_market` ↔ `fund_gld_defensive` and no direct
`fund_broad_market` ↔ `crypto` record; this session verified the four existing four-sleeve pair
records and the two absences directly. That structure identifies one sleeve as the most
pair-incomplete, and does **not** select it, for three independent reasons: the missing-pair rule
governs *pair conclusions in a future application*, not endpoint admissibility; XASSET-0024 §H.4 and
§J.10 require an endpoint to be **pair-independent** — not to consume an unresolved pair as an input
at all — so pair completeness does not bear on endpoint qualification either way; and selecting on
"most gaps" would rest on evidence coverage, which supplies no accepted economic selection basis
(§E.2).

**E.5 — Representation tractability.** The planning material described to this session observed that a
self-contained source may be structurally easier for one sleeve and structurally hardest for another,
and expressly flagged that this is not authority to select. That is correct, and it is §E.2's point
in another form: tractability is a property of evidence availability, which supplies no accepted
economic selection basis. Rejected as a basis for this filing's determination; §E.2's second paragraph
governs what a future authorized act may separately consider.

**E.6 — DRIVER-class asymmetry across sleeves.** Tested directly rather than assumed: all four sleeves
carry a profile record in the frozen snapshot under XASSET-0020 §F.2's sleeve-function row, so the two
single-sleeve DRIVER classes at §D apply to all four alike. No sleeve is structurally advantaged or
disadvantaged in class availability. No basis.

**E.7 — The one genuine asymmetry in the corpus, restated and again declined.** XASSET-0025 §J found
that `GLD_FUNCTION` is the only §C.2 row whose source-owned currentness state is `current`, every other
row lacking a governed currentness rule. That finding is accurate and is not reopened. It again does
not select, for the reasons XASSET-0025 gave — the same row states the source "cannot establish
relative preference or an endpoint," XASSET-0020 §F.2 forbids it from proving a sleeve weight, and it
carries no numeric value of any kind. Those reasons are sufficient on their own. §E.2 adds only that
currentness, being an evidence-quality property, supplies no accepted economic selection basis
either.

**E.8 — Principal or governance selection.** A future, explicit, separately filed and separately
reviewed governance act *could* select a sleeve on a stated basis, and XASSET-0025 §J expressly
preserves sleeve selection as "a separate, later, explicitly authorized act." No such act exists, and
this filing is not one. This is the only route by which a proper subset could lawfully arise, and it is
recorded as available rather than exercised.

**Disposition.** **No accepted basis lawfully selects any sleeve or any proper subset of sleeves
today.** Every basis reachable from accepted authority is either expressly foreclosed (§§E.1, E.3),
without any accepted economic selection basis (§§E.2, E.5, E.7), structurally irrelevant to endpoint
admissibility (§E.4), or absent (§E.6). The one lawful route to a subset (§E.8) requires an act that
does not exist.

**This is a present-tense determination about the accepted corpus, not a permanent bar.** It records
that nothing today supplies a basis, and expressly not that nothing ever could. §E.8 remains open, and
§E.2's second paragraph preserves a distinct question this filing does not reach.

### F. Determination C — program shape

The outcome vocabulary is closed to exactly four values, and exactly one is selected:

- `SINGLE_SLEEVE_PROGRAM_ON_ACCEPTED_SELECTION_BASIS` — one sleeve, with an identified accepted,
  non-convenience basis selecting it;
- `MULTI_SLEEVE_SUBSET_PROGRAM_ON_ACCEPTED_SELECTION_BASIS` — a proper subset, on the same standard;
- `ALL_FOUR_SLEEVE_SELECTION_FREE_PROGRAM` — coverage of the complete closed sleeve ontology, requiring
  no selection act;
- `PREREQUISITE_REQUIRED_BEFORE_PROGRAM_SHAPE_DETERMINABLE` — accepted authority cannot lawfully
  determine program shape and a named prerequisite must precede the question.

**Outcome: C — `ALL_FOUR_SLEEVE_SELECTION_FREE_PROGRAM`.**

The first purpose-built Level-1 endpoint-evidence program must be scoped across all four sleeves. The
determination rests on three grounds, each independently sufficient:

1. **Narrowing requires an authority that does not exist.** Every proper subset — one sleeve or
   several — is reachable only through a selection act, and §E establishes that no accepted basis
   supplies one today. A program scoped to a subset today would be carrying an
   unauthorized selection inside a research design, where it would be far harder to see and refuse than
   in a governance filing.
2. **All-four coverage is the unique selection-free coverage.** Covering XASSET-0020 §B's complete
   closed ontology is not a choice among sleeves; it is the absence of one. Nothing is preferred,
   ranked, or sequenced by it.
3. **It is this program's own established practice under the same constraint.** XASSET-0024 settled
   endpoint-basis feasibility "at that level" because it is "common to all four sleeves," and
   XASSET-0025 inspected all four "under the identical test before any result was recorded," producing
   a uniform eight-cell matrix. Neither found the absence of a selection basis a reason to abstain from
   its question; both answered it across all four.

**The smallest lawful program is the widest coverage, and that is not a paradox.** "Smallest" is
constrained by lawfulness, not by cost. Narrowing is the act that requires new authority; widening
requires none. A successor that wants a narrower program does not need a cheaper research design — it
needs a separate, filed, reviewed selection decision, and §E.8 is the only route to one.

**F.1 — A narrow *outcome* is available without any selection act, and this is the practically
decisive point.** All-four *coverage* does not mean four bounds must be produced. XASSET-0020 §J.3
makes abstention "a complete governed outcome, not a defect to be patched," and XASSET-0025 §K states
that "A null answer to this question is a complete outcome." A program scoped across all four sleeves
that finds qualifying evidence producible for one sleeve and null for three has produced a lawful,
complete result — and the sleeve it landed on was chosen **by the evidence**, not by an author. That
is the difference between an evidence-determined narrow result and an authored narrow scope, and it is
the whole reason all-four coverage costs the program nothing it would otherwise have kept.

**F.2 — What all-four coverage does not license.** It is coverage, not aggregation. The program may not
target, constrain, or reconcile a sum across the four sleeves; may not derive any sleeve's bound as the
complement or residual of the others; may not divide the unit evenly or by any symmetry convention; and
may not produce a ranking, tally, or score across sleeves. XASSET-0020 §C provides that the four sleeve
outputs are not required to exhaust the unit, §K makes the complement `UNSIZED_UNASSIGNED_CAPITAL`, and
§M with XASSET-0024 §D non-routes N4 and N5 bar midpoints, symmetry conventions, residuals, and plugs
by name. Each sleeve's each bound must be independently governed, per XASSET-0021 §E.2 and §F and
XASSET-0024 §J's express answer that endpoint independence "is affirmatively required."

### G. Determination D — ordering and packaging under XASSET-0025 §O.5

XASSET-0025 §O.5 recorded both ordering and packaging as unresolved. This filing **preserves both**,
and adds what accepted authority does fix: a set of ordering constraints anchored on the
endpoint-stating source rather than on the sequence between the two missing requirements.

**G.1 — Ordering between evidence production and authority constitution: `REMAINS_UNRESOLVED`.**
Accepted authority does not fix which of the two missing requirements must come first, and this filing
does not fix it either. XASSET-0025 §O.5's posture is preserved, not closed.

The reason is that the accepted ordering constraints attach to a *third* thing — the endpoint-stating
or endpoint-prescribing governed source — rather than to the sequence between evidence and authority:

- **The endpoint-stating source must itself be under competent Level-1 authority.** XASSET-0023 §H.2
  item 3 requires that "the stating source's accepted/effective authority must extend to fixing a
  Level-1 sleeve share," and XASSET-0024 §J.5 repeats that the stating authority's accepted/effective
  scope must so extend. This is a requirement on the source that states or prescribes the endpoint, not
  merely a condition satisfied by whichever authority later admits a pre-existing document. A bound
  stated under an incompetent scope is not cured by later admission.
- **Underlying research and evidence production are a different act.** Nothing in accepted authority
  requires the underlying study, data, or analysis to have been performed under Level-1 endpoint
  authority. What must be under competent authority is the governed source that states or prescribes
  the endpoint. Underlying work may therefore precede the constitution of that authority; it is the
  endpoint-stating step that may not.
- **For NUM-0001 class 4, the value selection must follow the evidence.** XASSET-0024 §E.3 item 3
  requires the record to state "the defensible range or constraint **the evidence established**,"
  together with the chosen value and the economic reason for it. A selection cannot reference a range
  the evidence has not yet established. This constrains when the **selection** happens — not when the
  **authority** is constituted.

Those constraints all order other acts *relative to the endpoint-stating source*. None of them orders
**authority constitution relative to evidence production**, which is the question XASSET-0025 §O.5
actually left open. The texts XASSET-0025 cited for that proposition were re-read this session and
still do not fix it: XASSET-0024 §J is titled "Minimum evidence properties for the next research **or
authority** unit," expressly contemplating either as next; XASSET-0024 §I states the gap
conjunctively without ordering; and XASSET-0021 §O lists evidence admission and endpoint authority
together and fixes no sequence.

**This filing therefore declines to close that gap by inference.** An earlier draft of this decision
determined `NO_MANDATORY_GLOBAL_ORDERING` on the reasoning that the two route families constrain the
order in opposite directions. That reasoning does not hold: it treated the competence requirement as
attaching at admission rather than to the stating source, and it applied class 4's evidence-first
requirement to class 5 as well. Both premises are corrected above and at §G.2, and the determination
they supported is withdrawn rather than re-derived on other grounds. Whether some future filing can
affirmatively resolve the ordering is left exactly where XASSET-0025 left it.

**G.2 — Four ordering constraints that do bind, on every packaging.** These are derived from accepted
authority and hold regardless of how the successor packages its work:

1. **Evidence before selection, for NUM-0001 class 4 only.** The evidence establishing the defensible
   range must exist and be identified at the time a competent authority records NUM-0001 §7's triple —
   the evidence-established range, the chosen value, and the stated economic reason for that value.
   (XASSET-0024 §E.3 item 3; NUM-0001 §7, §8.) **This constraint does not extend to class 5.** NUM-0001
   §1 defines class 5 as a *provisional governance guardrail*, and NUM-0001 §6 states its own
   requirements: an explicit "provisional, not empirically calibrated" label and a stated review
   condition, which may be calendar-based, event-driven, or evidence-driven. NUM-0001 §7 is the
   class-4 requirement and is not imposed on class 5. XASSET-0023 §H.4 item 3 requires a class-4 **or**
   class-5 value to have been selected by an effective governance authority competent for Level-1
   endpoints; that shared requirement does not make class 5 evidence-bounded, and no evidence-established
   range is required for it.
2. **Competent authority no later than the endpoint-stating source.** Competent Level-1 endpoint
   authority must extend to the source that states or prescribes the endpoint, at that source's own
   creation or adoption. (XASSET-0023 §H.2 item 3; XASSET-0024 §J.5.) Underlying research or analysis
   may precede that authority; the endpoint-stating step may not, and later admission does not cure a
   source stated under an incompetent scope.
3. **Snapshot successor after evidence, before any application.** Newly produced evidence is admissible
   only from XASSET-0021 §§C.2–C.3 or from "a snapshot lawfully replaced or extended by a separate
   future authorization"; XASSET-0021 §C.1 forbids an application from silently adding a later file,
   refreshed observation, or new source class. A snapshot successor cannot admit evidence that does not
   yet exist, and no application may read the evidence before it does. (XASSET-0024 §J.2; XASSET-0023
   §H.1 item 2.)
4. **Everything before the application.** The selection is made "outside and before the application";
   the application transcribes and never selects. (XASSET-0024 §E.2.)

**Constraint 3 names a third structural prerequisite that XASSET-0025 §O.5's two-requirement framing
does not cover.** XASSET-0025 §I states the gap as evidence and authority; XASSET-0025 §M item 4
separately lists a lawful snapshot successor. Both are right, and the successor unit needs them read
together: there are **three** structurally distinct missing pieces, not two, and unlike the first two,
the third's position in the sequence *is* fixed — unlike the ordering between evidence production and
authority constitution, which §G.1 leaves unresolved.

**G.3 — Packaging: `PACKAGING_REMAINS_AT_SUCCESSOR_ELECTION`. Preserved, not narrowed.** Whether
qualifying evidence and competent authority are obtained through one lifecycle or through separate
ones is **not** fixed by accepted authority, and is not fixed here. XASSET-0025 §O.5's supporting
citations were independently re-read this session and are accurate: XASSET-0024 §J is titled "Minimum
evidence properties for the next research **or authority** unit"; XASSET-0024 §I states the gap
conjunctively without ordering; XASSET-0021 §O lists evidence admission and endpoint authority together
and fixes no sequence; and XASSET-0024 §K.2 draws its line between governance-time and application-time
discretion rather than between one filing and two.

A combined lifecycle therefore remains lawful **if** the resulting record independently satisfies
NUM-0001 provenance, evidence admission under XASSET-0020 §F.1, XASSET-0024 §J.1–§J.12, the §E.3
anti-discretion test, and every independence and scope requirement those impose — exactly the proviso
XASSET-0025 §O.5 already stated. One addition, derived rather than invented: XASSET-0024 §K.2's answer
to the circularity objection is that the relocated act becomes "subject to independent exact-head
review, principal acceptance, and merge." A combined record therefore does not escape that discipline
by being one document; its evidence half and its authority half must each survive the same independent
review, and neither may be treated as certified by the other's presence in the same file.

**No combination is authorized by this filing, and no packaging is preferred, recommended, or
prescribed by it.**

### H. Determination E — representation architecture is source-dependent and required of nothing now

**No representation rule must be created before purpose-built endpoint evidence exists.**

XASSET-0024 §G fixes three paths and only three: a **self-contained** source whose own governed content
directly governs every representation its own authority requires, so that no cross-representation
combination is performed at all; a **separately ruled** path under an accepted Level-1 aggregation or
selection rule; and otherwise **mandatory abstention**. Path 1 requires no rule to exist. Requiring a
rule first would therefore foreclose path 1 for no reason accepted authority supplies, and would
pre-fix a representation universe before the source that would consume it is known.

XASSET-0023 §H.5 is the governing text on what is actually missing, and it is precise: executed
representation-sensitivity evidence exists inside the accepted RISK corpus; what does not exist
anywhere at Level 1 is an accepted cross-representation **aggregation or selection** rule; and "A
successor unit must therefore be scoped to supply the missing rule under its own authority, not to
re-discover evidence that already exists." XASSET-0024 §G leaves that rule's creation "to a unit scoped
for it" and does not authorize it.

**Disposition: `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`.** A Level-1 representation rule becomes
*required* only if and when a candidate source is not self-contained under XASSET-0024 §G path 1.
Its necessity, its scope, and the representations it would have to map are all properties of a source
that does not yet exist. Creating one now would be a Level-1 methodology amendment performed inside
a shape determination, without its own authorization or review.

**H.1 — The self-contained path is preserved wherever lawful.** XASSET-0024 §G path 1 is not
narrowed, disfavoured, or made conditional by this filing, and a successor program is not required to
plan around its unavailability.

**H.2 — CM-14 through CM-17 are untouched.** This filing designates no representation membership for
`equity`, `fund_broad_market`, `fund_gld_defensive`, or `crypto`; chooses among no instruments; builds
no composite; and resolves no representation gap. All four rows remain exactly as accepted, and remain
*latent* blockers on any future non-self-contained candidate, as XASSET-0025 §L records. No accepted
authority requires their designation for this determination, and none is performed.

### I. Determination F — the smallest lawful next program architecture

The constraints below are assembled from accepted authority and add none. A successor program is
lawful only if it carries all of them. They are stated so that the successor's design can be checked
against them rather than argued about.

1. **Coverage.** All four sleeves (§F). No proper subset absent a separate §E.8 selection decision.
2. **Outcome.** Per-sleeve and per-bound, with null a complete outcome (§F.1). No sleeve's result may
   be inferred from another's.
3. **Bound independence.** LOWER and UPPER independently governed, for each sleeve, from sources that
   may differ in identity and NUM-0001 class; neither derived from the other; neither inheriting the
   other's representation coverage. (XASSET-0021 §E.2, §F; XASSET-0024 §J's express answer.)
4. **Single-sleeve bounds only.** Whatever DRIVER class admits the evidence, the bound states the §C
   quantity for one named sleeve — never a ranking, split, or relative statement (§C).
5. **Route and class open.** Both R1 and R2 preserved; NUM-0001 classes 1–5 preserved; class 6
   disqualifying. No route or class is pre-selected (§D, §G.1). (XASSET-0024 §D, §J.7.)
6. **No sum, residual, symmetry, or equal division.** (§F.2; XASSET-0020 §C, §K, §M; XASSET-0024 §D
   non-routes N4, N5.)
7. **Pair independence.** No endpoint may consume an unresolved pair as an input at all;
   direction-invariance by independence, never direction-robustness by inspection. (XASSET-0024 §H.4,
   §J.10; XASSET-0020 §I.)
8. **Representation.** Self-contained path preserved; no rule assumed, required, or pre-fixed;
   abstention mandatory where §G path 1 fails and no accepted rule exists (§H).
9. **Snapshot successor.** Any newly produced evidence requires a lawfully authorized snapshot
   extension or replacement before admission; it may not be silently added (§G.2 constraint 3).
10. **Sequencing preference carried forward unchanged.** XASSET-0024 §H.3's RANGE-first determination
    stands: the POINT route's additional blocker is RISK pair determinacy, which no endpoint research
    can address and which the consumed RISK-0001 authority cannot supply. RANGE feasibility should be
    established first unless the evidence uniquely supplies a point.
11. **No barred origin.** XASSET-0025 §F's firewall results apply in full and are not re-litigated by
    scope: the historical provisional target family, the historical residual, the historical equal
    baseline, the fixed adjustment increment, the historical R2/R3 constructs, current targets,
    holdings, weights, tiers, and gates remain barred by origin, and clearing XASSET-0022 §R's literal
    scan is a floor rather than the boundary.
12. **No RISK reuse.** All twenty consequential parameters remain lapsed and reuse-barred in their own
    recorded terms; no family may be re-questioned; no third attempt exists.

### J. The exact next authorized successor action

Stated so the successor is unambiguous. **This filing does not authorize, commission, schedule, or
partially grant it**, and identifying it creates no entitlement to it — the same posture XASSET-0024 §J
and XASSET-0025 §K each took toward the unit they identified.

> **One explicitly authorized Lane G governance unit whose scope is to constitute competent Level-1
> endpoint authority, to charter the all-four-sleeve endpoint-evidence program against XASSET-0025
> §K's question, or to do both — its packaging and internal ordering at its own lawful election under
> §G.3, subject to §G.2's four binding constraints and §I's twelve architectural constraints. The
> ordering between the two, per §G.1, is not fixed by accepted authority and is not fixed here.**

A charter, if that is the election, additionally requires what XASSET-0025 §K already names and this
filing does not supply: a justified research design, a protocol, pre-registration, provenance rules,
trial bounds, and its own authorization. An authority-constituting filing, if that is the election,
must define the competence it confers in terms of the §C quantity; it may constitute that competence
without exercising it, and for a NUM-0001 class-4 bound it may not record a value selection before the
evidence establishing the range exists (§G.2 constraint 1).

**J.1 — No sequencing preference is offered, and none should be inferred.** §G.1 leaves the ordering
between evidence production and authority constitution unresolved, and this filing supplies no
observation, recommendation, or cost comparison that would favour either election. Any view about
which order risks or costs less is for the successor to form and justify on its own evidence.

### K. Recorded rather than resolved

**K.1 — Which DRIVER class the future evidence will fall under is not determined here, and cannot be.**
§D establishes that the class fixes the lawful evidence unit, and the class is a property of evidence
that does not exist. This filing determines coverage, which is answerable now because it turns on
selection authority rather than on evidence design. It does not determine the evidence design.

**K.2 — XASSET-0024 §K.1's open reading is neither resolved nor relied upon.** Whether XASSET-0020
§E.1's six classes house a magnitude statement remains open. This filing's determinations are stable
under both readings: the absence of a selection basis (§E), the ordering analysis (§G), and the
representation disposition (§H) are each independent of whether any class can carry a magnitude. §D's
scope table reads only the classes' *scope* language, not their capacity to carry a magnitude.

**K.3 — Whether the two currently absent direct pairs bear on a pair-scoped endpoint route.** If future
evidence were admitted under one of §D's four comparative classes for a pair with no direct record, it
would face XASSET-0020 §I's bar on transitive fill and §G.2 constraint 3's snapshot requirement
together. Nothing here determines how that interacts, because no such candidate exists. Recorded so it
is not discovered late.

**K.4 — Not reopened here.** XASSET-0023 §G's Level-2 subset question; §J.1's XASSET-0021 §O
strict-conjunction tension; §J.2's gold-representation labelling difference; XASSET-0024 §K.2's
circularity discussion beyond §G.3's narrow addition; and XASSET-0025 §J's `GLD_FUNCTION` currentness
finding beyond §E.7's restatement. None bears on any determination above, and none is resolved.

### L. Effect on the closure matrix and application authority

No XASSET-0021 §N row is reclassified. The matrix stands exactly as accepted at 14
`CLOSED_DETERMINISTICALLY` / 14 `APPLICATION_MUST_ABSTAIN` / 2 `SEPARATE_PREREQUISITE_REQUIRED`, with
`application_time_author_or_reviewer_judgment_remaining: 2`. CM-07 through CM-19, CM-25, and CM-26
remain `APPLICATION_MUST_ABSTAIN`; this filing supplies no endpoint, no pair evidence, and no
representation rule, and changes nothing about them.

**Application authority remains WITHHELD.** XASSET-0021 §O's double gate is untouched, XASSET-0022 §P's
mechanical enforcement is untouched, `APPLICATION_AUTHORIZATION_REGISTRY` remains empty, and no
`intelligence/level1_application/` artifact exists or is authorized. No all-abstention application is
authorized either. Nothing in §§C–K may be read as granting, implying, scheduling, or partially
granting application authority.

### M. Governance package and WORKSTREAMS synchronization

This filing touches exactly four tracked files: this decision; `governance/decisions.yaml` (one catalog
row); `operations/WORKSTREAMS.yaml` (additive XASSET-0025 post-merge closeout and XASSET-0026 lane
facts, every prior gate's own text byte-unchanged); and `test_portfolio_hq_dashboard_decisions.py` (the
two mechanical decision-count assertions, 127 → 128).

No supporting artifact is created. This is a governance determination, not a research result, and its
complete reasoning and citations are contained here — matching XASSET-0021 through XASSET-0025, each of
which carried comparable analytical weight with `supporting_artifact: null`. No Intelligence, research,
schema, generator, validator, allocator, target, holding, gate, margin, chart, ladder, or protected
portfolio file is changed.

### N. Reopen triggers

Reopen XASSET-0026 if: XASSET-0019's, XASSET-0020's, XASSET-0021's, XASSET-0022's, XASSET-0023's,
XASSET-0024's, or XASSET-0025's effective identity changes; XASSET-0020 §B's sleeve ontology, §E.1's
driver classes and their scope language, §F.2's source registry, §H's pair set, §I's missing-pair rule,
or §L's endpoint or canonical-order rows are amended; a governance decision selects a sleeve or a
subset under §E.8; a Level-1 endpoint authority is constituted; any XASSET-0021 §C path or hash
changes, or the snapshot is lawfully replaced or extended; a Level-1 cross-representation aggregation
or selection rule becomes accepted; a direct pair record is added for either currently absent pair;
separate governance grants reuse authority over any lapsed RISK parameter, or a new RISK study is
chartered; NUM-0001's classes, §6, §7, or §8 requirements change; a reviewer establishes XASSET-0024
§K.1's contrary reading of §E.1; or the liquidity or Level-2 architecture changes a boundary relied on
here.

### O. Absolute non-authorization

This decision creates no endpoint, bound, point, range, percentage, weight, target, or allocation, and
selects, prefers, ranks, or sequences no sleeve; performs, commissions, and authorizes no research,
endpoint research, research charter, research design, protocol, pre-registration, data acquisition,
backtest, evidence admission, direct-pair study, representation study, or RISK study; produces no
evidence conclusion or historical anchor; grants no endpoint authority, no evidence-admission
authority, and no application authority, including for an abstention-only application, and populates no
authorization registry; creates no application artifact or directory; extends, replaces, or amends no
XASSET-0021 snapshot; amends no methodology and supplies no representation rule, representation set,
equity aggregation, fund or gold peer selection, or crypto composite, and designates no CM-14, CM-15,
CM-16, or CM-17 membership; performs no Level-1 sizing and no Level-2 membership or sizing; makes no
liquidity determination; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no chart, ladder,
optimizer, deployment, trade, order, or brokerage action; adopts no portfolio policy; creates no
XASSET-0022 schema or version successor; grants no reuse authority over any lapsed RISK parameter or
result and no authority to re-question any RISK family; accesses, reruns, refreshes, or reuses no
RISK-0001 execution artifact; rehabilitates no barred historical or current value; edits no accepted
decision; and rewrites no accepted history.

## Rationale

XASSET-0025 ended with a verified null and three open questions, and the temptation at this point is to
treat the open questions as the successor's problem and start commissioning. That would repeat the
failure XASSET-0024's Context names: an expensive step taken before the cheap step that determines
whether it is lawful. Program shape, ordering, and representation timing are all questions about
accepted authority, not about evidence. They cost one governance filing to answer and they change what
the next unit is allowed to do. Answering them first is the same discipline XASSET-0024 applied to
feasibility and XASSET-0025 applied to sourcing.

The finding that carried the shape determination is that narrowing, not widening, is the act requiring
authority. The intuitive framing — that a four-sleeve program is large and expensive and a one-sleeve
program is the modest place to start — inverts the actual constraint. A one-sleeve program is not
smaller in the sense that matters; it is a program carrying an unauthorized selection, and carrying it
in a research design rather than in a governance filing, where it would be considerably harder for a
reviewer to see. Recording that the smallest *lawful* program is the widest coverage is worth more than
another restatement that no sleeve is selected, because it tells a successor exactly what it would have
to obtain in order to narrow, and from whom.

What makes all-four coverage cost the program nothing is §F.1, and that section was the one most worth
getting right. Coverage and outcome are different things. A program scoped across four sleeves that
finds evidence producible for one has produced a complete lawful result under XASSET-0020 §J.3, and the
sleeve it landed on was chosen by the evidence rather than by an author. Every practical benefit a
successor might want from a one-sleeve scope is available through an evidence-determined narrow
outcome, without the selection act. The two look similar from the outside and are entirely different in
provenance, which is precisely the distinction this program exists to preserve.

§E.2 required care in the opposite direction from the one first attempted. XASSET-0020 §D bars research
volume and evidence maturity from answering the marginal-capital question, and §F.2 bars evidence
coverage and maturity from implying size or preference — so every convenience basis a successor might
reach for is an evidence-quality property that supplies no accepted *economic* selection basis. An
earlier draft of this filing went a step further and treated those clauses as an affirmative doctrinal
bar on choosing research order or scope for operational reasons, bridging the gap with the assertion
that the program has no mechanism to quarantine such sequencing from preference. That bridge was this
filing's own, not accepted authority's, and it would have created a new prohibition by extension —
narrowing a future governance act's option set on reasoning the upstream methodology does not supply.
The corrected §E.2 states only what the clauses establish and expressly leaves the sequencing question
to a future act on its own terms. The determination does not depend on the stronger reading: what
carries §F is the absence of any accepted basis today, not a permanent bar.

The ordering question at §G.1 was the hardest part, and an earlier draft of this filing got it wrong in
a way worth recording. It determined that no global ordering is mandatory, reasoning that the two route
families constrain the order in opposite directions: competence tested at admission rather than
production, so work may precede its authority; but a class-4 or class-5 selection must reference an
evidence-established range, so evidence must precede that selection. Both premises were defective.
XASSET-0023 §H.2 item 3 and XASSET-0024 §J.5 require the *stating source's* authority to be competent —
a requirement on the source that states the endpoint, not a condition curable by later admission — and
NUM-0001 §7's evidence-established-range triple is the class-4 requirement, which NUM-0001 §6 does not
impose on class 5's provisional guardrail. Corrected, the constraints all order other acts relative to
the endpoint-stating source and none orders authority constitution against evidence production, which
is the question actually left open. The right move was therefore to withdraw the determination rather
than re-derive it on other grounds: XASSET-0025 read the same texts and found they fix nothing here,
and closing that gap by inference is exactly what a filing that creates nothing should not do. What
survives is more useful than the withdrawn conclusion — the constraints that genuinely bind, stated
precisely, with the open question left visibly open. Packaging stayed open for the
reason XASSET-0025 gave and this filing had no better one: nothing fixes it, and narrowing a lawful
option set as a side effect of describing a gap is exactly what a filing that creates nothing should
not do.

Constraint 3 at §G.2 is the piece XASSET-0025's own framing does not surface. Its §I states the gap as
two requirements and its §M lists the snapshot successor separately; both are accurate, and read apart
they leave a successor with a two-item mental model and a third prerequisite it will meet late. The
snapshot successor's position in the sequence is the one thing about the ordering that *is* fixed, and
stating it alongside the two unfixed orderings is more useful than stating it in a roadmap list.

Representation timing needed a determination rather than deferral because deferral has a direction. Had
this filing said nothing, a successor could reasonably have concluded that the missing Level-1
aggregation rule is a prerequisite and built one first — which would pre-fix a representation universe
before the source that would consume it is known, and would foreclose XASSET-0024 §G path 1 for a
source that might never have needed a rule at all. Saying explicitly that the requirement is
source-dependent preserves path 1 and keeps the rule where XASSET-0023 §H.5 and XASSET-0024 §G both
left it: with a unit scoped for it, under its own authority.

## Alternatives Considered

- **Determine `PREREQUISITE_REQUIRED_BEFORE_PROGRAM_SHAPE_DETERMINABLE`, on the ground that shape is
  evidence-design-dependent.** Rejected, and this was the substantive call. §D does establish that the
  lawful evidence *unit* is class-determined and that the class cannot be fixed yet — but *coverage*
  does not turn on the class. It turns on whether a lawful selection basis exists, which is a question
  about accepted authority and is fully answerable today. Abstaining would have left a successor free to
  read narrowing as available, when narrowing in fact requires an authority that does not exist. That is
  the more dangerous error, and it is abstention as a substitute for analysis of exactly the kind
  XASSET-0024 and XASSET-0025 each rejected in their own contexts.
- **Select one sleeve, on the `GLD_FUNCTION` currentness asymmetry.** Rejected. XASSET-0025 §J already
  declined it, the same snapshot row states the source "cannot establish relative preference or an
  endpoint," and §E.2 establishes independently that currentness is an evidence-quality property that
  XASSET-0020 §F.2 bars from implying preference. It would also have been the second filing in a row to
  identify the asymmetry and the first to act on it, without any new authority in between.
- **Select one sleeve on representation tractability, since a self-contained source is structurally
  easier for some sleeves than others.** Rejected. This is the planning material's own observation,
  which expressly flagged that it is not authority to select, and it is §E.2's bar in another form.
  Choosing the sleeve whose evidence is easiest to obtain is choosing on evidence availability.
- **Select one sleeve by canonical order, as a neutral tie-break.** Rejected, and expressly foreclosed:
  XASSET-0020 §L classifies canonical sleeve order as a determinism constant with "no economic effect."
  A neutral-looking tie-break that assigns economic consequence to a procedural constant is not neutral.
- **Scope the program to one pair rather than one sleeve, since four of six DRIVER classes are
  pair-scoped.** Rejected. It has the identical defect one step over: selecting which of the six
  canonical pairs to cover requires a basis, and none exists. It would additionally have foreclosed the
  two single-sleeve classes for any sleeve outside the chosen pair.
- **Mandate separate lifecycles for evidence and authority, as the conservative default.** Rejected.
  "Conservative" here means narrowing a successor's lawful option set without authority to do so, and
  §G.1 establishes that mandating either order would foreclose one of the two lawful route families.
  XASSET-0025 §O.5 declined to narrow for the same reason and this filing found no better one.
- **Mandate evidence-first, since a class-4 selection cannot reference a range that does not exist.**
  Rejected. That constraint is real and is recorded at §G.2 constraint 1, but it binds class 4 and class
  5 only. Generalizing it would have foreclosed the class-1, class-2, and class-3 routes, where the
  competence requirement attaches to the source's admission instead.
- **Supply the missing Level-1 representation rule now, since XASSET-0023 §H.5 identifies it as the
  missing piece.** Rejected. It is a Level-1 methodology amendment requiring its own authorization and
  review, XASSET-0024 §G expressly leaves it to a unit scoped for it, and creating it here would
  pre-fix a representation universe before the source that would consume it exists — potentially
  foreclosing §G path 1 for a source that would never have needed it.
- **Designate CM-14 through CM-17 membership to make the future program concrete.** Rejected and
  expressly outside scope. No accepted authority requires it for this determination, and designating
  representations is the substance of the rule §H declines to write.
- **Write the research charter here, since the shape is now determined.** Rejected. XASSET-0025 §K
  already identifies the exact question; a charter additionally requires a justified research design, a
  protocol, pre-registration, provenance rules, and trial bounds, resting on a different evidentiary
  basis than reading accepted text, and requires its own authorization.
- **Create a supporting audit artifact.** Rejected. The determinations and their citations are the
  decision, and XASSET-0021 through XASSET-0025 each carried comparable analytical weight with
  `supporting_artifact: null`.

## Consequences

The next unit now knows, before spending anything, that the first purpose-built Level-1
endpoint-evidence program must be scoped across all four sleeves; that this is not a preference for
breadth but the absence of an authority to narrow; that narrowing requires a separate filed and
reviewed selection decision under §E.8 and is available on no other basis; and that every convenience
basis it might reach for — availability, maturity, tractability, currentness, pair completeness,
canonical order — is barred by express clauses rather than merely disfavoured.

It knows that all-four coverage costs it nothing it would otherwise have kept, because a narrow
*outcome* remains available through evidence rather than through scope, and a null for three sleeves is
a complete governed result. It knows that an individual DRIVER item's minimum subject-matter scope and a
program's endpoint/output coverage are different questions, that comparative or pair-subject evidence
may support a bound for one named sleeve without obliging a second sleeve output, and that no DRIVER
class is closed to a program by its output coverage alone.

It knows that the ordering between evidence production and authority constitution remains unresolved,
and why: every accepted ordering constraint attaches to the endpoint-stating source rather than to the
sequence between those two acts. It knows the four constraints that do bind regardless — including that
competent authority must extend to the endpoint-stating source at its own creation or adoption, that
NUM-0001 §7's evidence-first requirement is class-4 only, and the one XASSET-0025's two-requirement
framing does not surface: a lawful snapshot successor must follow the evidence and precede any
application. It knows packaging remains its
own lawful election, that a combined lifecycle is permitted but escapes no review, and that no
representation rule is required before evidence exists because the self-contained path remains open.

Nothing about the portfolio changes. Application authority remains withheld, the closure matrix stands
at 14 / 14 / 2, the authorization registry remains empty, no application artifact exists, the
XASSET-0021 snapshot is unextended, and no endpoint, range, percentage, weight, target, allocation, or
trade is created, recommended, or authorized. XASSET-0019 through XASSET-0025, NUM-0001, LEVEL2-0001,
the RISK corpus, `intelligence/`, `research/`, and every protected portfolio file are byte-unchanged.
