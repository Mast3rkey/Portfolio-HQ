---
decision_id: XASSET-0032
date: 2026-08-17
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_remaining_semantic_gates.py
---

## Context

### Live preflight

Verified independently before any mutation, against live GitHub and git state rather than inherited
narrative:

| Fact | Verified |
|---|---|
| GitHub `main` / `origin/main` / local `HEAD` | all `1d7c61f3a6188cf2df7a7bc0390c269e596ef202` |
| PR #330 (`XASSET-0031`) | merged/closed; parents `3bcb1379…` + `2d3252d4…`; merge tree byte-identical to the accepted head's tree |
| Merge-commit CI | run `31983014229`, `head_sha` `1d7c61f3…`, completed/**success** |
| Open PRs | **zero** |
| Working tree / stash / worktrees | clean / empty / sole worktree |
| `XASSET-0032` identifier | unused anywhere in the repository |
| `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` |
| `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` |
| Construction universe | regenerated live: **680** constructions, **48** cells, `73c0965e…5224` |
| `LOAD_BEARING_RELPATHS` | exactly the six `XASSET-0029` paths, all present |
| Lane directory / attestation / claim / completion / ledger / `stage1_results.yaml` / runner | **all absent** |
| `new_execution_is_authorized()` | `False` — "no attestation present … There is no merge-to-execution gap" |

**`ATTEMPT_1` is intact, unclaimed, and unconsumed, and remains so after this filing.**

### The question this unit answers

`XASSET-0030` determined `GATE_EVALUATION_METHOD_NOT_CLOSABLE` and recorded a
`CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` of six closable gates and six not. `XASSET-0031` then took
the first of the six — `G3` — and returned a bounded negative.

This unit takes the remaining five semantic prerequisites named in `XASSET-0030` §G.A:

**For `G5`, `G8`, `G9`, `G10`, and `G12`, what is the most specific deterministic semantic rule, or the
most exactly bounded non-closability finding, that accepted authority actually supports — such that two
independent conforming executors given identical frozen inputs cannot lawfully select different gate
semantics?**

The objective is not to make any gate `PASS`. Negative findings and abstention are valid outcomes, and
four of the five determinations below are, in substance, refusals to legislate through a reservation.

## Decision

### A. Determination — all five remain `NOT_CLOSABLE`, each with bounded positive sub-determinations

Reusing `XASSET-0030` §E's existing snapshot vocabulary rather than inventing a new one:

| Gate | Class | Determination | What this unit *does* close |
|---|---|---|---|
| `G5_CONSTRAINT_SHAPE` | categorical | **NOT CLOSABLE** — expressly reserved per candidate | The originate-vs-clip rule is exactly statable (§D.1); the reservation is general, not `sleeve_deployability`-specific (§D.3) |
| `G8_UNIQUENESS` | categorical | **NOT CLOSABLE** — depends on a future admitted set | "Exactly one" is existence **∧** uniqueness; vacuous uniqueness never satisfies it (§E.1); the current admitted set contributes **zero** competing lawful values (§E.2) |
| `G9_REPRESENTATION` | prerequisite | **NOT CLOSABLE** — path 1 is irreducibly source-dependent | Path 2 is determinately unavailable (§F.1); the path-3-vs-prerequisite tension is **reconciled by both canonical artifacts** (§F.2) |
| `G10_PAIR_INDEPENDENCE` | categorical | **NOT CLOSABLE** — successor-snapshot- and consumption-dependent | "Unresolved" ≡ pair conclusion `unable_to_determine` (§G.1); **all six** canonical pairs are unresolved under the accepted snapshot, determined from committed text with **no protected-evidence access** (§G.2); the population decomposes 120 / 360 / 200 (§G.3) |
| `G12_SNAPSHOT_ADMISSIBILITY_PATH` | prerequisite | **NOT CLOSABLE** — the tense of "could admit" is unfixed | "Identifiable" ≠ "exists" (§H.1); G12's scope is **identifiability only** and may not absorb full §J.1 admission (§H.2); the named dependency is identified (§H.3) |

**The `XASSET-0030` 6/6 gate map is UNCHANGED.** No gate moves between the closable and not-closable
partitions. No `XASSET-0030` §E.1 invalidation trigger fires, so `G1`, `G2`, `G4`, `G6`, `G7`, and `G11`
are **not** re-derived and are not relied on by anything below.

**`G3` is untouched.** `XASSET-0031`'s `SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE`, its R1/R2
distinction, "no third route", and its source-dependent posture for all six DRIVER classes are
preserved exactly and are not reopened, narrowed, or relied upon as a premise.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** This filing changes no canonical byte, no universe, no
hash pin, no load-bearing path, and no authorization state.

### B. What this unit reproduced before determining anything

All reproductions used the real modules against the live frozen universe and committed bytes. No
results document, lane state, or Stage-1 output was created, and **no gate was evaluated for any
construction**.

**B.1 — All 680 constructions are hypothetical.** `source_architecture` is
`HYPOTHETICAL_SOURCE_ARCHITECTURE` for every entry, without exception. This single fact is the shared
root of all five determinations: every gate below asks a question about "the candidate", and no
candidate source exists whose properties could be inspected.

**B.2 — The comparison architecture decomposes exactly three ways.** Counted mechanically from the
frozen universe:

| `comparison_subject_kind` | `unordered_pair_id` | Count | Driver classes |
|---|---|---|---|
| `SLEEVE_SELF` | absent | **80** | `portfolio_function`, `sleeve_deployability` |
| `DIRECT_ALTERNATIVE` | absent | **480** | `valuation_opportunity_cost`, `downside_path_risk`, `recovery` |
| `UNORDERED_PAIR` | present | **120** | `diversification_cobehavior` |

Of the 480 `DIRECT_ALTERNATIVE` constructions, **120** carry `ALT__UNSIZED_UNASSIGNED_CAPITAL` and
**360** carry another sleeve as `counterpart`. The 120 `UNORDERED_PAIR` constructions distribute
exactly **20 to each** of `XASSET-0020` §H's six canonical unordered pairs.

**B.3 — The admitted set is non-empty, and contains zero lawful endpoint values.** `XASSET-0021`
§§C.2–C.3 admits **21** non-RISK evidence rows and **14** RISK files — **35** admitted items. Against
that, `XASSET-0021` §F states: "**The frozen snapshot contains no such Level-1 endpoint authority for
any sleeve**", and closes point and range eligibility to `APPLICATION_MUST_ABSTAIN` for every sleeve.
These are two different facts and §E below turns on keeping them apart.

**B.4 — Canonical text carries a representation disposition and a non-self-contained handling rule.**
`pre_registration.yaml`'s `representation:` block records `disposition:
SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`, `disposition_source: XASSET-0026_SECTION_H`,
`rule_created_by_this_program: false`, `cm_14_through_cm_17_membership_designated: false`, and
`non_self_contained_handling: NAME_THE_EXACT_DEPENDENCY_AND_BLOCK_PENDING_SEPARATE_PREREQUISITE`.

**B.5 — Nothing anywhere produces a gate result.** Each of the 680 universe entries carries identity
fields only; no gate outcome appears in the universe, in either canonical file, or in any module.
`derive_candidate_disposition` was re-read and **conforms** to canonical precedence (categorical →
uncertainty → prerequisite → all-pass), as do `derive_cell_outcome` and `derive_roll_up_outcome`.

### C. Batchability determination — one coherent unit

Five questions were answered before drafting, and all five permit a single filing.

1. **One shared methodology and authority surface?** **Yes.** All five turn on B.1's single structural
   fact, and all five are resolved by one method: separate the semantic rule accepted authority *does*
   fix from the satisfaction question that depends on a source which does not exist. All five sit on
   the same authority surface — `XASSET-0024` §§F/G/H.4/J.1/J.2/J.8/J.9/J.10, read with `XASSET-0020`,
   `XASSET-0021`, `XASSET-0023`, `XASSET-0025`, `XASSET-0026`, `XASSET-0027`, and the two canonical
   artifacts. `OPS-0009` Lane G throughout.
2. **Would batching create accidental cross-gate policy?** **No.** Each determination below is stated
   on its own controlling authority, with its own reproduction and its own preserved blocker. **No
   determination is used as a premise for any other**, and §I records the interactions that exist as
   observations rather than as derivations.
3. **Would any gate require amending a different controlling decision?** **No.** None of the five
   requires the `XASSET-0020` §E.1 clarification that `XASSET-0024` §K.1 names as `G3`'s corrective, or
   any other amendment. All five are resolved by reading accepted authority, not by changing it.
4. **Would any require protected evidence or a real future candidate?** **No protected evidence.**
   `G10`'s pair-resolution question — which `XASSET-0030` flagged as possibly sitting behind the
   `risk_lane_boundary` — is answered by `XASSET-0021` §D's application rule in committed governance
   text. **The canonical `risk_lane_boundary.protected_result_path` was not read, listed, opened, or
   reproduced anywhere in this filing**, and no such access is needed — this decision deliberately does
   not restate that path's literal value. The *satisfaction* questions do require a real candidate,
   which is precisely why all five remain not closable.
5. **Independently reviewable without hiding separate judgments?** **Yes** — §§D–H are separate
   sections, each with its own authority, reproduction, determination, and preserved blocker, and each
   is separately pinned by tests.

**Choice: ALL-FIVE COHERENT UNIT.** Filing five separate governance PRs would multiply lifecycle
overhead without changing a single conclusion, and would fragment one methodology across five reviews.

### D. `G5_CONSTRAINT_SHAPE` — reserved per candidate

**Canonical definition.** Gate index 5, categorical. Question: "Would the candidate **originate** a
bound, rather than only cap, clip, block, or intersect one that already exists?" Controlling authority
`XASSET-0024_SECTION_F_LIMB_4_AND_NON_ROUTE_N1`. `PROTOCOL_V1.md` §6 restates it as "originates a bound
rather than only clipping one".

**Why `XASSET-0030` classified it not closable.** `XASSET-0027` §M.4, verbatim: "Whether a particular
deployability or structural-limit candidate is constraint-shaped in that sense **is exactly what `G5`
decides, per candidate, on the candidate's own terms. No prejudgment is recorded here.**" That is an
express reservation of the same shape as §M.3's reservation of `G3`, which `XASSET-0031` correctly
declined to legislate through.

**The exact missing semantic input.** Not the rule — the rule is fully stated (§D.1). What is missing is
any accepted authority fixing whether *a given* candidate's content originates or only clips, which is a
property of the candidate's own governed content.

**D.1 — The rule this unit closes.** Assembled from accepted authority; nothing added:

> A candidate satisfies `G5` **only if its own governed content originates the bound** — that is, the
> content itself fixes a value for the `XASSET-0024` §C quantity. A candidate whose content only
> **caps, ceilings, floors-as-limits, blocks, clips, or intersects** an endpoint fails `G5`, however
> exactly that limit is expressed, and no precision, provenance label, or validator success
> rehabilitates it.

Grounded in `XASSET-0024` §F Limb 4 ("A cap, ceiling, floor-as-limit, or concentration boundary that
only blocks, caps, or clips cannot originate a bound however precisely it is expressed"); non-route
**N1** ("Constraint application or bound intersection", lawful in principle: **NO**, "Clip only"),
invalidated by `XASSET-0020` §E.2's "never create preference" and `XASSET-0021` §F's "Bound
intersection **may narrow already-authorized endpoints but may not create one**".

**D.2 — What the rule does not do.** It does not classify any candidate, any DRIVER class, or any of
the 680 constructions. Applying it is the per-candidate act §M.4 reserves.

**D.3 — The reservation is general.** `XASSET-0030` records it as "Most acute for `sleeve_deployability`,
but the reservation is general", and §M.4's own wording — "a particular deployability **or
structural-limit** candidate" — is not confined to one DRIVER class. **This unit records no class-wide
`G5` `PASS` or `FAIL` for any of the six classes**, and expressly does not treat the 40
`sleeve_deployability` constructions as presumptively constraint-shaped. `sleeve_deployability`'s own
canonical scope language is `SLEEVE_LEVEL_CONVERTIBILITY_LOCKUP_OR_IMPLEMENTATION_FRICTION`; whether a
source about convertibility, lockup, or implementation friction originates or only clips is exactly the
per-candidate question, and **deployability evidence is never converted into an allocation rule here**.

**Determination: `G5` NOT CLOSABLE, source-dependent, no prejudgment for any class.**

### E. `G8_UNIQUENESS` — existence conjoined with uniqueness

**Canonical definition.** Gate index 8, categorical. Question: "Would **exactly one** lawful value exist
for this endpoint quantity **across the admitted set**, with no second candidate value resolvable by any
midpoint, average, precedence, or conservatism rule?" Controlling authority `XASSET-0024_J_8`.
`XASSET-0025` criterion **T6**, which `XASSET-0027` §F leaves untouched.

**Why `XASSET-0030` classified it not closable.** Its recorded basis: "Uniqueness is 'across the
admitted set'; `R6` gives only *source-level* uniqueness, and no admitted set exists. Uniqueness over an
empty set is trivially satisfied or unknowable, with no accepted rule selecting."

**E.1 — "Exactly one" is a conjunction, and vacuous uniqueness never satisfies it.** The gate says
"exactly one lawful value **exist**", not "at most one". A candidate therefore satisfies `G8` only if
**both** hold:

> (i) the candidate itself contributes exactly one lawful value for the §C quantity for its own named
> sleeve and bound; **and** (ii) no second lawful value for that same quantity exists anywhere in the
> admitted set at evaluation time.

**Empty-set/vacuous uniqueness is therefore not a `G8` `PASS`.** A state in which zero lawful values
exist fails limb (i) — it is a failure of existence, not a trivial satisfaction of uniqueness. This
disposes of the "trivially satisfied" horn of `XASSET-0030`'s dilemma on the gate's own words, and it is
reinforced by `XASSET-0025` T6's disqualifier list ("A second lawful value; **an open interval with no
member-fixing rule**; any tunable step") and `XASSET-0024` §E.3 item 4 ("**If the authority leaves an
open interval and states no rule fixing a member, no lawful bound exists**").

**E.2 — Correction of a stated ground: an admitted set exists.** `XASSET-0030`'s "no admitted set
exists" is not accurate. `XASSET-0021` §§C.2–C.3 **is** the admitted set and is non-empty — 35 admitted
items (B.3). What is empty is the set of **lawful Level-1 endpoint values within it**: `XASSET-0021` §F
states the frozen snapshot "contains no such Level-1 endpoint authority for any sleeve."

The correction narrows the blocker rather than removing it, and it is load-bearing in one direction: it
establishes that **the current admitted set contributes zero competing lawful values**, so limb (ii)'s
risk cannot arise from the accepted snapshot. It can arise only from whatever a lawful snapshot
successor *additionally* admits.

**E.3 — The surviving blocker.** Limb (ii) is quantified over "the admitted set at evaluation time",
which for every one of the 680 hypothetical constructions is a **successor** snapshot whose composition
is not fixed by any accepted authority. Two constructions in the same cell posit alternative sources for
the same sleeve, bound, and quantity; whether a successor admits one, both, or neither is undetermined,
and if it admits two, both fail `G8` with no midpoint, average, precedence, or conservatism rule
available to resolve them (`XASSET-0024` §E.3 item 7; §H.6 item 5). **`G8` is therefore dependent on the
composition of an admitted set that does not exist.**

**Determination: `G8` NOT CLOSABLE. The semantic rule (E.1) is closed; the satisfaction question is
successor-snapshot-dependent.**

### F. `G9_REPRESENTATION` — one blocker resolved, one preserved

**Canonical definition.** Gate index 9, **prerequisite**. Question: "Would the candidate be
self-contained under `XASSET-0024` §G path 1, **or** covered by a separately accepted Level-1
aggregation or selection rule under path 2?" Controlling authority
`XASSET-0024_SECTION_G_AND_J_9`. `XASSET-0025` criterion **T9**, untouched by `XASSET-0027` §F.

**Why `XASSET-0030` classified it not closable.** Two stated grounds: (a) path 1 is source-dependent and
construction requirement `R8` "expressly asserts no prior representation rule"; and (b) "Additionally
unreconciled: §G path 3 says **mandatory abstention** while the gate's declared failure class is
**prerequisite**."

**F.1 — Path 2 is determinately unavailable, and that is closed.** No accepted Level-1
cross-representation aggregation or selection rule exists anywhere. `XASSET-0023` §H.5 is explicit that
what is missing is "an accepted cross-representation **aggregation or selection** rule, which does not
exist anywhere at Level 1"; `XASSET-0026` §H adopts `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`;
`XASSET-0027` §P.2 names such a rule as a separately required, unauthorized successor; and canonical
`representation.rule_created_by_this_program` is `false` with
`cm_14_through_cm_17_membership_designated: false`. **Under current authority `G9` can be satisfied only
via path 1.** This unit creates no rule and designates no CM-14–CM-17 membership.

**F.2 — Ground (b) is reconciled, not open — and both canonical artifacts say so.** `XASSET-0024` §G
path 3's "mandatory abstention" and the gate's `BLOCKED_PENDING_SEPARATE_PREREQUISITE` failure class
operate at **two different levels** and describe one state:

- `pre_registration.yaml` — `representation.non_self_contained_handling:`
  `NAME_THE_EXACT_DEPENDENCY_AND_BLOCK_PENDING_SEPARATE_PREREQUISITE`, whose note reads "A candidate
  whose construction would require cross-representation combination records the exact representation
  dependency and **fails G9 as a prerequisite**."
- `PROTOCOL_V1.md` §9 — "A candidate requiring cross-representation combination records the exact
  dependency and **fails `G9` as a prerequisite**."
- `mandatory_abstention_conditions` — `REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS`,
  authority `XASSET-0024_SECTION_G_PATH_3`, with `abstention_is_a_complete_outcome: true`.

The **gate-record classification** is prerequisite; the **endpoint-level outcome** is abstention. A
prerequisite-blocked candidate produces no endpoint, which *is* abstention. There is no conflict, and
`pre_registration.yaml` — canonical "for every closed identity, candidate, **gate**, ordering,
vocabulary, and count" — settles the gate record directly. **`XASSET-0030`'s ground (b) is therefore
withdrawn as a blocker.** Categorical dominance is preserved unchanged: where such a candidate also
fails a categorical gate, the categorical disposition dominates and it is not recorded as merely
prerequisite-blocked.

**F.3 — The surviving blocker.** Path 1 asks whether a source's "own governed content directly governs
**every** representation its own authority requires". That is irreducibly a property of the source.
Canonical text says so in terms — every construction's frozen requirement **R8** reads "Representation
admissibility is **source-dependent** and is evaluated by the `G9` gate; this specification asserts no
prior representation rule", and the universe records `representation_posture:
SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`. With all 680 sources hypothetical (B.1), **no `G9` result is
determinable class-wide.** Deriving `PASS` from `R8`'s presence would be the by-construction inference
`XASSET-0030` §E Standard 1 rejects.

**Determination: `G9` NOT CLOSABLE on path 1's source-dependence alone. Path 2's unavailability and the
path-3/prerequisite reconciliation are both closed. No class-wide `PASS` or `FAIL`.**

### G. `G10_PAIR_INDEPENDENCE` — the pair-resolution question is answered; consumption is not

**Canonical definition.** Gate index 10, categorical. Question: "Would the candidate avoid consuming any
**unresolved** pair as an input **at all**, establishing direction-invariance **by independence** rather
than direction-robustness by inspection?" Controlling authority
`XASSET-0024_SECTION_H_4_AND_J_10`. `XASSET-0025` criterion **T10**, untouched by `XASSET-0027` §F.

**Why `XASSET-0030` classified it not closable.** Its recorded basis: "§H.4 requires the unresolved pair
'is not an input to it at all'; the 120 `PAIR__` constructions are direct pair evidence by definition.
**Whether a named `XASSET-0020` §H pair is *unresolved* is determined nowhere**, and the evidence that
would settle it may sit behind the `risk_lane_boundary`."

**G.1 — "Unresolved" is defined by accepted authority.** `XASSET-0020` §I identifies the term directly:
a future application "must record the pair conclusion as `unable_to_determine`. A sleeve range may still
survive that missing pair only when both endpoints are … valid under every possible direction of **the
unresolved pair**." The referent of "the unresolved pair" is the pair whose conclusion is
`unable_to_determine`. Therefore:

> **A pair is *unresolved* for `G10` purposes if and only if its `XASSET-0020` §H pair conclusion is
> `unable_to_determine`.** The other three closed conclusions — `self_preferred`,
> `counterpart_preferred`, `indistinguishable` — are resolved.

**G.2 — Correction of a stated ground: all six pairs are determined, from committed text, with no
protected access.** `XASSET-0021` §D determines the pair conclusion for **all six** canonical pairs
under the accepted snapshot:

- for the four pairs with historical relationship records — `equity__fund_broad_market`,
  `equity__fund_gld_defensive`, `equity__crypto`, `fund_gld_defensive__crypto` — §D's frozen per-driver
  mapping yields "the deterministic pair conclusion `unable_to_determine` under this snapshot. **This is
  an application rule, not a populated pair record**";
- for `fund_broad_market__fund_gld_defensive` and `fund_broad_market__crypto`, "`XASSET-0020` §I already
  closes the application rule: the pair conclusion is `unable_to_determine`."

**All six canonical `XASSET-0020` §H pairs are therefore unresolved under the accepted `XASSET-0021`
§§C.2–C.3 snapshot.** `XASSET-0030`'s "determined nowhere" is corrected.

**This required no protected evidence.** §D's rows for `downside_path_risk` and `recovery` cite RISK
only through its already-accepted, publicly recorded disposition ("every family disposition is
`unable_to_determine`; preserve that state"), which `XASSET-0023` §D.6 and `XASSET-0024` §H.2 likewise
record in committed governance text. **The `risk_lane_boundary` concern is dissolved rather than
crossed**: `protected_result_path` was not read, listed, or referenced, and this unit reuses no RISK
scenario, value, parameter, window, or result.

**G.3 — The population decomposes three ways, and the gap has an exact location.** From B.2:

| Group | Count | On the face of the frozen specification |
|---|---|---|
| `UNORDERED_PAIR` (`diversification_cobehavior`) | **120** | Consumes a **named** canonical §H pair by construction — `unordered_pair_id` set, scope `ONE_UNORDERED_PAIR`, `DIRECT_PAIR_EVIDENCE` |
| `DIRECT_ALTERNATIVE` with a **sleeve** counterpart | **360** | Compares the sleeve against another sleeve, but carries **no** `unordered_pair_id`. Whether that constitutes consuming the corresponding §H pair is **undetermined** |
| `ALT__UNSIZED_UNASSIGNED_CAPITAL` (120) + `SLEEVE_SELF` (80) | **200** | No canonical §H pair implicated on the specification's face — `UNSIZED_UNASSIGNED_CAPITAL` is a separate `XASSET-0020` §H comparison family with its own closed conclusions, not one of the six unordered pairs |

**G.4 — The surviving blockers, exactly two.**

1. **Successor-snapshot dependence.** G.2's determination is expressly scoped "**under this snapshot**".
   Every construction posits admission through a *lawful snapshot successor* (requirement **R1**), and
   `XASSET-0021` §D records that "New direct-pair evidence would be required only to seek a later
   non-abstaining result." Whether any pair is resolved under a successor is therefore undetermined —
   and `G10` turns on the pair's status at evaluation time, not today's.
2. **Consumption semantics for the 360.** `XASSET-0024` §H.4's test is substance-based — the pair "is
   not an input to it at all" — while the universe's `unordered_pair_id` is a specification label. No
   accepted authority fixes whether a `DIRECT_ALTERNATIVE` construction with a sleeve counterpart
   consumes the corresponding §H pair. Both readings are defensible and nothing selects.

**G.5 — What is expressly *not* determined.** The 200-construction group is **not** recorded as `G10`
`PASS`. A specification's silence about pair consumption is not proof that an eventual source consumes
no pair — `XASSET-0030` §E Standard 1 again. The table records a specification fact, nothing more.

**Determination: `G10` NOT CLOSABLE. "Unresolved" is defined (G.1) and all six pairs are determined
under the accepted snapshot (G.2); successor-snapshot status and consumption semantics for 360
constructions remain open.**

### H. `G12_SNAPSHOT_ADMISSIBILITY_PATH` — identifiability is bounded; the tense is not

**Canonical definition.** Gate index 12, **prerequisite**. Question: "Is a lawful `XASSET-0021` snapshot
successor **identifiable** that could admit the candidate, noting that no snapshot successor is created,
extended, or authorized by this program?" Controlling authority
`XASSET-0024_J_1_AND_J_2_AND_XASSET_0026_G_2_CONSTRAINT_3`. The canonical `J.2` mapping is
`G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED`.

**Why `XASSET-0030` classified it not closable.** "No governed definition of 'identifiable' exists and
nothing fixes the tense of 'could admit.' Two defensible answers; nonexistence alone is not
non-identifiability."

**H.1 — "Identifiable" does not mean "exists".** `PROTOCOL_V1.md` §6.1 states it directly: "`G12`
records whether a snapshot successor is *identifiable*. **No snapshot successor is created, extended,
replaced, or authorized by this program**." The same section fixes **Prerequisite** as "closeable by a
named, separately authorized prerequisite … and the dependency **must be named**", and canonical
`prerequisite_definition` requires `requires_named_dependency: true`. A failure class that presupposes a
namable dependency cannot be discharged by the mere nonexistence of that dependency's object.

> **Therefore: the nonexistence of a snapshot successor may never, by itself, be recorded as `G12`
> `FAIL`.** Any executor recording `G12` `FAIL` must state a ground other than "no successor exists".

**H.2 — `G12`'s scope is identifiability only, and may not absorb full §J.1 admission.**
`PROTOCOL_V1.md` §8.1's testability table fixes this: `J.1` admission is "**partially testable** — `G12`
+ the source-currentness rule", and `J.2` snapshot position is "**partially testable** — `G12`,
**identifiability only**". `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED` accordingly means only the
Stage-1-testable subset and "**never** that full §J admissibility has been established".

> **Therefore: `G12` may not be evaluated by importing §J.1's hash-match, validator-pass, or governed-
> freshness conditions.** Those remain untested at Stage 1 by design, and an executor who folded them
> into `G12` would silently convert a partial gate into a full admission test.

**H.3 — The named dependency is identified.** Accepted authority names the successor that would close
`G12`: `XASSET-0024` §J.2 ("a snapshot **lawfully replaced or extended by a separate future
authorization**"), `XASSET-0026` §G.2 constraint 3 ("Snapshot successor after evidence, before any
application"), and `XASSET-0027` §P.2 (a required, unauthorized successor "which cannot admit evidence
that does not yet exist"). `PROTOCOL_V1.md` §12 records the dependency order: "new evidence → **lawful
snapshot successor** → endpoint-capable downstream consumption → application."

**H.4 — The surviving blocker: the tense of "could admit", and what "lawful" means candidate-relatively.**
The gate's relative clause is candidate-relative — a successor "**that could admit the candidate**" —
and accepted authority fixes neither its tense nor its content at identifiability-only scope:

- a **present-tense** reading is supported by `XASSET-0026` §G.2 constraint 3 and `XASSET-0027` §P.2 —
  a successor "cannot admit evidence that does not yet exist", and all 680 sources are hypothetical —
  which yields `FAIL` for all 680;
- a **forward-looking** reading is supported by the same ordering constraint read as a *sequence*
  (evidence → successor → application, which presupposes the successor can admit evidence once it
  exists), by §6.1's identifiability framing, and by H.1's rule that nonexistence is not
  non-identifiability — which yields `PASS` on the identifiability conjunct.

Both are grounded; **nothing in either canonical artifact or any accepted decision selects between
them**, and they produce opposite gate results. `XASSET-0025` §D's structural consequence — "any source
outside the frozen snapshot fails **T8** under existing authority regardless of its other properties …
This is not a finding about any particular source; it is the shape of the current authority" — fixes
what the *prerequisite* is without fixing the gate's *identifiability* answer, because `G12` tests
identifiability rather than present snapshot position (H.2).

**H.5 — A disposition-inertness observation, recorded so it is not mistaken for a licence.** While `G2`
remains `UNABLE_TO_DETERMINE` for all 680 and no categorical gate independently fails, either `G12`
reading yields the same *candidate disposition*, because canonical precedence ranks uncertainty above
prerequisite failure. **This does not make the gate result optional.** Canonical
`gate_sequence.evaluation_requirement` is `EVALUATE_EVERY_APPLICABLE_GATE_BEFORE_CLASSIFYING` with
`record_first_failing_gate_only: false`, and the result schema records every gate. A gate result that is
disposition-inert today would become outcome-determining the moment §K.1 is resolved.

**Determination: `G12` NOT CLOSABLE. Identifiability's floor (H.1) and scope (H.2) are closed and the
dependency is named (H.3); the tense of "could admit" is unfixed.**

### I. Cross-gate interactions — observations, not derivations

Recorded so a successor does not mistake proximity for dependence. **No determination above is used as a
premise for any other.**

- `G8` (E.2) and `G12` (H.3) both concern the snapshot successor, from opposite directions: `G8` asks
  what a successor might *additionally admit*; `G12` asks whether one is *identifiable*. Neither answers
  the other.
- `G9` (F.1) and `G10` (G.4) both remain open on source-dependent grounds, but for different reasons —
  representation self-containment versus pair consumption. Closing either leaves the other untouched.
- `G5` (§D) and `G3` (`XASSET-0031`) share a reservation *shape* — `XASSET-0027` §M.4 and §M.3
  respectively — but not a subject. Nothing in §D bears on `G3`, and `XASSET-0031`'s determination is
  neither relied on nor extended.
- Four of the five gates are categorical (`G5`, `G8`, `G10`) or prerequisite (`G9`, `G12`); this filing
  changes **no** gate's declared class, index, question, controlling authority, or failure disposition.

### J. Corrections to `XASSET-0030` §E basis statements — classification unchanged

Three grounds stated in `XASSET-0030` §E's table are corrected by the readings above. In every case the
**classification is unchanged** — the gate remains not closable — and the correction **narrows** the
blocker rather than reopening the gate.

| Gate | `XASSET-0030` stated ground | Correction | Effect |
|---|---|---|---|
| `G8` | "no admitted set exists" | An admitted set exists and is non-empty (35 items); what is empty is the set of lawful **endpoint values** in it (`XASSET-0021` §F) | Blocker narrowed to successor-snapshot composition (§E.3) |
| `G9` | "Additionally unreconciled: §G path 3 says mandatory abstention while the gate's declared failure class is prerequisite" | Reconciled by **both** canonical artifacts and `XASSET-0026` §H (§F.2) | One of two grounds withdrawn; path-1 source-dependence survives (§F.3) |
| `G10` | "Whether a named `XASSET-0020` §H pair is *unresolved* is determined nowhere, and the evidence … may sit behind the `risk_lane_boundary`" | `XASSET-0020` §I defines the term and `XASSET-0021` §D determines all six under the accepted snapshot, from committed text with no protected access (§§G.1–G.2) | Blocker relocated to successor-snapshot status and consumption semantics (§G.4) |

**`XASSET-0030`'s text is not edited.** Per this repository's never-silently-rewrite convention for
accepted decisions, the corrections are recorded here and its own filing stands as accepted. Its
`CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` partition is unchanged in both membership and count.

### K. Canonical and enforcement conformance — nothing new found

This unit re-read `derive_candidate_disposition`, `derive_cell_outcome`, `derive_roll_up_outcome`, the
`PREREQUISITE_GATES` set, and the reading-dependence branches of
`level1_endpoint_evidence_preregistration_validator.py` against canonical `disposition_rules`.

- **All three derivation functions conform** to canonical precedence, and `PREREQUISITE_GATES` matches
  the canonical prerequisite pair `G9` / `G12` exactly.
- The reading-dependent `BLOCKED_PENDING_SEPARATE_PREREQUISITE` prohibition **conforms** — canonical
  `uncertainty_precedence_note` requires exactly it ("Absent a categorical bar, uncertainty is never
  downgraded").
- The reading-dependent `BLOCKED_CATEGORICALLY` prohibition remains the **enforcement conformance
  defect** `XASSET-0030` §C already recorded. **This unit neither re-derives, expands, narrows, nor
  corrects it**, and adds no new defect of its own.

**No new canonical or enforcement conformance defect was found in the five gates' analysis.** Nothing in
§§D–H requires a canonical amendment; every determination is a reading of text already accepted.

### L. Remaining abstentions, and the named prerequisites that would close each gate

| Gate | What remains open | The named prerequisite |
|---|---|---|
| `G5` | Whether any candidate's content originates rather than clips | A qualifying candidate source, evaluated per candidate under §D.1 — `XASSET-0027` §M.4's reserved act |
| `G8` | Whether a successor snapshot admits a second lawful value for the same quantity | A lawful `XASSET-0021` snapshot successor with known composition |
| `G9` | Whether a candidate source is self-contained under `XASSET-0024` §G path 1 | A qualifying candidate source; **or**, for path 2, a separately accepted Level-1 aggregation/selection rule (`XASSET-0023` §H.5; `XASSET-0027` §P.2) |
| `G10` | Pair status under a successor snapshot; whether a `DIRECT_ALTERNATIVE` construction consumes the corresponding §H pair | A lawful snapshot successor; **and** a governed determination of §H.4 consumption semantics for `DIRECT_ALTERNATIVE` comparisons |
| `G12` | The tense of "could admit", and what "lawful … that could admit the candidate" requires at identifiability-only scope | A governed reading of the `G12` question — the smallest corrective is a clarification of the tense alone, requiring no new evidence |

**`G3` remains open on `XASSET-0031`'s terms and is not restated here.** `XASSET-0024` §K.1 remains
**unresolved**; `XASSET-0020` §E.1 remains **unamended**.

### M. Invalidation and re-derivation triggers for the determinations above

Each §§D–H determination is a **current-authority** reading and must be re-derived if its own basis
changes:

| Determination | Re-derivation required if |
|---|---|
| §D.1 originate-vs-clip rule | `XASSET-0024` §F Limb 4 or non-route `N1` is amended; `XASSET-0020` §E.2 or `XASSET-0021` §F changes; `XASSET-0027` §M.4's reservation is lifted |
| §E.1 existence∧uniqueness rule | `XASSET-0024` §J.8 or §E.3 items 4/7 is amended; `XASSET-0025` T6 changes |
| §E.2 admitted-set fact | The `XASSET-0021` §C snapshot is lawfully replaced or extended (**§Q**), or §F's eligibility closure changes |
| §F.1 path-2 unavailability | A Level-1 cross-representation aggregation or selection rule becomes accepted (**§Q**) |
| §F.2 path-3 reconciliation | The canonical `representation` block, `mandatory_abstention_conditions`, or `PROTOCOL_V1.md` §9 changes; either pinned hash changes (**§Q**) |
| §G.1 "unresolved" definition | `XASSET-0020` §I or §H's closed pair-conclusion vocabulary is amended |
| §G.2 all-six-unresolved fact | The snapshot is lawfully replaced or extended (**§Q**); `XASSET-0021` §D's frozen per-driver mapping changes; separate governance grants reuse authority over any lapsed RISK parameter (**§Q**) |
| §H.1–H.3 identifiability floor, scope, dependency | `PROTOCOL_V1.md` §6.1 or §8.1 changes; the canonical `J.2` mapping changes; `XASSET-0026` §G.2 constraint 3 or `XASSET-0027` §P.2 is amended |

**A general trigger applies to every row**, matching `XASSET-0030` §E.1: if either pinned canonical hash
changes, or `XASSET-0019` through `XASSET-0026`'s effective identity changes (**§Q** in both cases), the
whole set is re-derived rather than inherited.

### N. Successor implementation consequences

`XASSET-0030` §G.A listed six semantic prerequisites. After `XASSET-0031` and this filing, **all six
have been examined and none is closed**; what has changed is that each now has an exactly located
blocker and a named prerequisite (§L) rather than a general reservation.

`XASSET-0030` §G.B is unchanged and remains the correct sequence: semantic prerequisites first, then
**one** canonical / enforcement / outcome-producing-code / reauthorization pass. This filing:

- **builds no runner**, changes no `LOAD_BEARING_RELPATHS`, and amends no `XASSET-0029`;
- **corrects no validator** — §K found no new defect and expressly leaves `XASSET-0030` §C's recorded
  defect for that single pass;
- adds four rules a successor's canonical reconciliation and enforcement layer must encode if the
  corresponding gate is ever closed — §D.1, §E.1, §H.1, and §H.2 — each of which constrains a future
  executor **even while its gate remains open**, because each forbids a reading that would otherwise be
  available;
- leaves the §G.B invariant intact: **no outcome-producing executable code may be created, changed, or
  left outside the bound execution identity after the final rebinding and before `ATTEMPT_1`.**

### O. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; arms and executes no Stage 1; creates no Stage-1 runner and no `stage1_results.yaml`;
consumes nothing of `ATTEMPT_1`; **evaluates no gate for any construction and asserts no
per-construction outcome**; closes, re-derives, reclassifies, or reorders no gate and changes no gate's
class, index, question, controlling authority, or failure disposition; corrects no validator, extends no
`LOAD_BEARING_RELPATHS`, and performs no load-bearing reauthorization; amends no canonical file and
changes no hash pin, universe, cardinality, or construction identity; acquires no market, fundamental,
economic, or Stage-2 data; resolves `XASSET-0024` §K.1 neither way and amends no `XASSET-0020` §E.1
scope; reopens, narrows, or extends no part of `XASSET-0031`'s `G3` determination; resolves no §J.12,
grants no Stage 2, and grants no application authority; invents no Level-1 representation aggregation or
selection rule and designates no CM-14–CM-17 membership; selects no sleeve and creates no endpoint,
bound, point, range, percentage, weight, rank, target, or allocation; **reads, lists, or references no
`risk_lane_boundary` protected result path** and reuses no RISK scenario, value, parameter, window,
result, or private artifact; weakens no validator or test; changes no `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no
chart, ladder, deployment, trade, order, or brokerage action; and rewrites no accepted history.

## Rationale

The standard was `XASSET-0030`'s and `XASSET-0031`'s: not "a competent analyst could answer this gate",
but that two independent conforming executors, given identical frozen inputs, must not be able to select
different lawful semantics. Measured that way, all five gates fail — but they fail at different
distances, and the useful work was locating each distance precisely.

Two of the five were **expressly reserved** and needed only to be respected. `G5`'s §M.4 reservation is
the same instrument as `G3`'s §M.3, and `XASSET-0031` already established that a governance unit does
not legislate through one. What `XASSET-0031` also established is that a reservation on *satisfaction*
does not bar stating the *condition*, and §D.1 does exactly that: the originate-versus-clip rule is
fully available from §F Limb 4, `N1`, §E.2 and §F, and stating it costs nothing while denying a future
executor the freedom to invent a looser one.

Three of the five had grounds that did not survive re-reading, and all three errors ran the same
direction — toward *understating* what accepted authority has already settled. `G8`'s "no admitted set
exists" is contradicted by `XASSET-0021` §§C.2–C.3 itself; the real fact is subtler and more useful, that
the admitted set exists and contributes **zero** competing values, which localizes the entire blocker in
successor composition. `G9`'s path-3 tension is answered identically by both canonical artifacts, which
say in terms that such a candidate "fails `G9` as a prerequisite" — the abstention and the prerequisite
are one state described at the endpoint level and the gate-record level, and reading them as rivals
manufactured an open question. `G10`'s was the largest: `XASSET-0021` §D determines the pair conclusion
for all six canonical pairs deterministically, as an application rule, in committed governance text —
so the question was neither undetermined nor behind the `risk_lane_boundary`, and the boundary concern
dissolved rather than needing to be honoured by abstention.

Correcting three grounds while changing no classification is the result worth stating plainly. A
successor scoped against the uncorrected grounds would have looked for a pair-resolution determination
that already exists, might have sought RISK access it does not need, and would have carried a
representation reconciliation already performed in canonical text. The gates stay shut; the reasons are
now the right ones.

`G12` alone resisted narrowing in the same way, and it is the honest hard case. Its floor and its scope
*are* closeable — nonexistence is not non-identifiability, and `PROTOCOL_V1.md` §8.1 confines the gate to
identifiability only, forbidding an executor from quietly widening it into a full §J.1 admission test.
But the tense of "could admit" has two grounded readings producing opposite results, and the ordering
constraint that supports the forward-looking reading is the same text that supports the present-tense
one. Choosing either would have been legislating, and the §H.5 observation — that today the choice is
disposition-inert — is precisely the kind of fact that makes an unprincipled choice tempting and would
make it dangerous the moment §K.1 resolves.

Batching was chosen on coherence, not convenience. The five share one root cause, one method, and one
authority surface, and the only genuinely separable concern — `G10`'s protected-evidence question —
resolved into *not* requiring protected evidence, which removed the sole reason to split the filing.

## Alternatives Considered

**File five separate governance PRs.** Rejected: identical methodology, identical authority surface, no
cross-gate policy created, and each judgment separately sectioned and separately tested. Five lifecycles
would have changed no conclusion.

**Close `G12` on the forward-looking reading.** Rejected: it would have removed a blocker on a reading
accepted authority does not select, and §H.5 shows the choice is currently disposition-inert — meaning
the only thing it would purchase now is the appearance of progress, at the cost of a legislated
semantics that binds an irreversible one-shot run.

**Close `G12` on the present-tense reading.** Rejected symmetrically. It yields a determinate class-wide
`FAIL`, which is *more* tempting because it looks conservative — but a `FAIL` grounded in a tense
nobody fixed is as much an invention as a `PASS`, and it would collide with H.1's rule that nonexistence
alone is never the ground.

**Record `G10` `PASS` for the 200 constructions with no pair implicated.** Rejected: the specification
constrains subject matter, not every input a future source might consume. That is `XASSET-0030` §E
Standard 1 exactly, and §G.5 says so.

**Record `G10` `FAIL` for the 120 pair constructions.** Rejected: it requires the pairs to be unresolved
*at evaluation time*, and every construction posits a successor snapshot whose pair evidence is
undetermined. Today's unresolved status (§G.2) is scoped "under this snapshot" and does not travel.

**Treat `G9`'s path-3 tension as an open governance election.** Rejected on the same reasoning
`XASSET-0030` §C applied to the validator defect: the precedence question is already answered in
committed canonical text, and preserving the election would have manufactured a governance step while
misstating the accepted direction.

**Correct `XASSET-0030`'s §E text in place.** Rejected: it is an accepted decision, its classification is
unchanged, and this repository's convention is to record corrections forward rather than rewrite
accepted history. §J does that.

**Extend the `G2` dual-reading treatment to these gates.** Rejected as misdirected: `XASSET-0027` §M.1
routes §K.1 through `G2` specifically, and none of the five open questions here is a §K.1 reading
question. Adding reading slots would be a new rule.

**File nothing and let a Stage-1 executor decide at run time.** Rejected outright: `ATTEMPT_1` is
one-shot and `execution.rerun_rule.after_outcomes_observed` is `PROHIBITED`.

## Consequences

`XASSET-0030` §G.A's six semantic prerequisites are now all examined and none is closed — which is the
same headline as before this filing and a materially different starting position for a successor. Each
gate now carries an exactly located blocker, a named prerequisite (§L), and its own re-derivation
trigger (§M), and four new binding rules (§D.1, §E.1, §H.1, §H.2) constrain any future executor even
while their gates remain open.

The cheapest remaining correctives are now visible and unequal. `G12`'s is the smallest by a wide
margin: a governed reading of one clause's tense, requiring no new evidence, no candidate source, and no
snapshot successor. `G9`'s path 2 and `G8`'s and `G10`'s successor dependence all require artifacts that
do not exist. `G5` and `G9` path 1 require a candidate source and cannot be closed by governance at all
— they are per-candidate study findings, exactly as `XASSET-0027` §M.4 and `XASSET-0026` §H reserve
them.

That asymmetry is the practical result. It does not make Stage 1 nearer to executable — `G3` alone still
defeats the method, and five further gates defeat it independently — but it means no successor now needs
to rediscover which of the six can be closed by reading and which cannot be closed at all.

Stage 1 stays unarmed, `ATTEMPT_1` stays intact, and the negative remains the cheap outcome: three
governance filings against a single irreversible 680-construction run resting on semantics that, on
this reading, five separate accepted authorities decline to fix.
