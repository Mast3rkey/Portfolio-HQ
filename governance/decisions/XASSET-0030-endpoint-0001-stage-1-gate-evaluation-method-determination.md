---
decision_id: XASSET-0030
date: 2026-08-16
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_gate_evaluation_determinism.py
---

## Context

### Live preflight

Verified independently before any mutation, against live GitHub and git state rather than inherited
narrative:

| Fact | Verified |
|---|---|
| `origin/main` | `3cc15d58a42e6d56fbe702ccf4f377b60fbb8b0c` |
| PR #329 | open, draft, unmerged, **sole open PR**, 1 ahead / 0 behind |
| Working tree / stash | clean / empty, sole worktree |
| `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` |
| `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` |
| Construction universe | regenerated live: **680** constructions, **48** cells, `73c0965e…5224` |
| `stage_1_executability.executable` | `false` |
| Lane directory / attestation / claim / completion / ledger / `stage1_results.yaml` | **all absent** |
| `new_execution_is_authorized()` | `False` |

**`ATTEMPT_1` is intact, unclaimed, and unconsumed, and remains so after this filing.**

### The question this unit answers

Everything *downstream* of the twelve gate results is deterministic — `map_g2_reading`,
`required_g2_gate_result`, `derive_candidate_disposition`, `derive_cell_outcome`, and
`derive_roll_up_outcome` are closed, order-independent compositions. Nothing produces the gate results
themselves. Because `ATTEMPT_1` is one-shot and `execution.rerun_rule.after_outcomes_observed` is
`PROHIBITED`, that gap cannot be closed ad hoc during execution.

**Can the per-construction gate-evaluation method be made sufficiently deterministic that two
independent conforming executors, given the same frozen construction and the same accepted authority,
must produce the same twelve gate results and §K.1 per-reading fields without inventing economic
judgment — and if so, what is the smallest lawful method?**

### Correction history

**Correction 1** — after independent FULL exact-head review `4947074116` (`CHANGES REQUIRED` —
0 BLOCKING / 2 MAJOR / 2 MINOR / 1 NOTE) at head `ed99315121214f1839c13f9ed364b2a1c88c8971`. Changed:
§C's diagnosis of the canonical/enforcement contradiction, the entire §E gate inventory (7/5 → 6/6),
and §G's successor list.

**Correction 2** — after independent FULL exact-head review `4947130884` (`CHANGES REQUIRED` —
0 BLOCKING / 2 MAJOR / 0 MINOR / 1 NOTE) at head `941852493b36fa75440c78e3b9002f544731a250`, whose
exact-head CI run `31966991534` / job `95213557223` was completed/success. Changed **only** the
successor model: §A and §E now frame the table as a `CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` with
per-gate invalidation triggers in new §E.1, and §G is restructured into semantic prerequisites (G.A)
followed by one canonical/enforcement/reauthorization pass (G.B). **No gate disposition, canonical
semantics, authority interpretation, or substantive methodology determination changed** — the 6/6 map
is identical.

The core negative determination is unchanged and was affirmed by both reviews. Every MAJOR finding was
reproduced against controlling text before any edit.

## Decision

### A. Determination — `GATE_EVALUATION_METHOD_NOT_CLOSABLE`

**The answer is NEGATIVE.** A complete deterministic per-construction gate-evaluation method **cannot
lawfully be closed by this unit**. Six of the twelve gates are closable **under current authority**
against identified accepted feasibility authority; six are not, each for its own recorded reason — and
three of those (`G3`, `G5`, `G12`) are blocked by *express reservations in accepted authority*, not by
mere silence.

**§E's table is a `CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT`, not permanent gate closure.** Each
closable result is reusable without separate re-analysis **only while every controlling authority and
premise listed for that gate in §E.1 remains unchanged**. §E.1 states the invalidation triggers per
gate; several are already `XASSET-0027` §Q reopen triggers, and at least `G1` and `G2` depend on
authority that this decision's own §G semantic prerequisites propose to change.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** This filing changes no canonical byte, no universe, no
hash pin, and no authorization state.

### B. What this unit reproduced before designing anything

All reproductions used the real modules and isolated synthetic fixtures. No results document, lane
state, or Stage-1 output was created.

**B.1 — The §K.1 map consumes readings; it does not produce them.**
`required_g2_gate_result("PASSES", "FAILS")` returns `UNABLE_TO_DETERMINE` and `is_reading_dependent`
returns `True`. Both take the two reading outcomes as *inputs*. The validator says so of itself:
"Deciding a gate outcome remains a human/analytical act performed under the charter; this module only
composes already-decided gate results into a disposition by a fixed rule."

**B.2 — The frozen universe carries no gate outcomes.** Each of the 680 entries carries exactly ten
identity fields. There is no gate outcome anywhere in the universe, in either canonical file, or in any
module.

**B.3 — `G3` admits defensible answers with different dispositions**, and nothing selects between them.

**B.4 — While `G2` is reading-dependent, every categorical failure is unrepresentable *in the current
implementation*.** Holding the reading pair at `(PASSES, FAILS)`, a `FAIL` on **any** of the nine other
categorical gates derives `BLOCKED_CATEGORICALLY`, and
`_validate_stage1_results_against_universe` rejects the document — G1, G3, G4, G5, G6, G7, G8, G10,
G11, all nine, `valid=False`.

### C. Finding 1 — an enforcement defect against controlling canonical semantics

**Corrected after review `4947074116` MAJOR 1.** The prior head described this as an unresolved
election over "which artifact governs." That was wrong: **the repository already answers the precedence
question**, and the corrected diagnosis is narrower and stronger.

**Precedence, verified verbatim from observed bytes:**

| Artifact | Self-declared standing |
|---|---|
| `pre_registration.yaml` line 5 | "This YAML is **canonical** for every closed identity, candidate, gate, ordering, vocabulary, and count." |
| `PROTOCOL_V1.md` lines 5–8 | "This protocol explains the design. **It cannot enlarge or override the YAML.** Where the two appear to differ, **the YAML governs and the difference is a defect requiring a governed correction.**" |
| `level1_endpoint_evidence_preregistration_validator.py` lines 5, 18–19 | "Read-only and mechanical… **Deciding a gate outcome remains a human/analytical act** performed under the charter; this module only composes already-decided gate results." |

**The controlling rule, `XASSET-0027` §M.1, verbatim:**

> "Combined with §I.3.1's candidate precedence, a reading-dependent candidate necessarily records
> `G2 = UNABLE_TO_DETERMINE` and necessarily disposes to `UNABLE_TO_DETERMINE`, **unless a categorical
> gate independently fails** — including when a prerequisite gate also fails."

The canonical YAML (`g2_reading_mapping.reading_dependent_end_to_end_note`) and `PROTOCOL_V1.md` §7.1
state the same clause. So an **accepted governance decision** and **both canonical artifacts** agree
that a reading-dependent candidate disposes to `BLOCKED_CATEGORICALLY` when a categorical gate
independently fails. Only the validator forbids it.

**The two are therefore not peer authorities.** Canonical categorical precedence already controls, and
`PROTOCOL_V1.md` itself pre-labels a divergence of this shape as "a defect requiring a governed
correction." The validator branch at lines 2505–2509 is an **enforcement/implementation conformance
defect against accepted canonical semantics** — not a competing reading requiring a governance
election.

**One distinction must be drawn precisely, because a careless reading of §M.1 could be used to defend
the validator.** §M.1 says the reading-dependent row "maps to `UNABLE_TO_DETERMINE` … **never to
`BLOCKED_CATEGORICALLY`**." That sentence governs the *reading → `G2` gate result* mapping: the reading
pair never makes `G2` itself a categorical `FAIL`. The very next paragraph then fixes the
*candidate-disposition* rule and expressly admits categorical override. The validator's branch keys on
`row["disposition"] == "BLOCKED_CATEGORICALLY"` — the **candidate disposition**, which is exactly the
level at which §M.1 permits it. There is no internal conflict in §M.1; the defect is in the enforcement
layer alone.

**Consequence while the defect stands.** The categorical branch is unreachable, and with it
`XASSET-0027` §J.2's "recorded honestly", §I.2's cell rule, `derive_cell_outcome`'s
`ALL_CANDIDATES_BLOCKED_CATEGORICALLY` branch, and `derive_roll_up_outcome`'s
`NO_CONSTRUCTIBLE_CANDIDATE`. An executor who lawfully reached a categorical result would find it
unpublishable and could infer that the software had settled the question — which is precisely the
outcome canonical precedence forbids.

**This decision does not correct the validator.** That is a load-bearing implementation path (§D), and
correcting it is outside a governance-only unit's scope.

### D. The load-bearing reauthorization dependency — recorded so it is not discovered late

`level1_endpoint_evidence_preregistration_validator.py` and
`level1_construction_universe_closure_validator.py` are both members of
`level1_stage1_execution_authorization.LOAD_BEARING_RELPATHS`. Verified mechanically: the authorization
mechanism hashes the **current working-tree bytes** of each load-bearing path and requires them to equal
the same blob in the **authorized merged `XASSET-0029` tree** (`3cc15d58…`), which must in turn equal
the blob at the independently reviewed head. Both currently match. The failure branch reads:

> `enforcement drift: {path} in the working tree hashes to {working} but the authorized merged tree
> has {merged}; load-bearing code has changed since the authorized merge`

**Therefore any later lawful correction of the Finding 1 defect deliberately creates enforcement drift,
and Stage 1 becomes non-armable until a successor operational-authorization or reconciliation lifecycle
lawfully binds the new load-bearing implementation.** That is a cost of the correction, not an argument
against it — and it is recorded here so the successor scopes it up front rather than discovering it at
arming time. **No such reconciliation is attempted, scoped, or authorized by this decision.**

### E. `CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` — gate-by-gate, re-derived

**This table records what current accepted authority determines today. It is not permanent gate
closure.** A gate marked closable may be reused by a successor without separate re-analysis **only
while every controlling authority and premise named for it in §E.1 remains unchanged**. Where an
upstream authority changes, that gate's result is invalidated and must be re-derived under the
successor authority — it does not survive as a frozen fact.

**Corrected after review `4947074116` MAJOR 2.** The prior head's "7 closable / 5 not" split was
re-derived from first principles rather than preserved. `G1` moved **in**; `G5` and `G12` moved **out**.

Two standards were applied throughout, and the second is the one the prior head failed:

1. **(a) a specification requiring property P** is never by itself **(b) proof that P is lawfully
   satisfiable.** `XASSET-0028` §F puts Stage 1's question at (b). A gate is recorded closable only
   where **accepted authority independent of the frozen specification** establishes satisfiability.
2. **(c) absence of a not-yet-created artifact** must be classified as categorical, prerequisite, or
   uncertainty on governed grounds — never inferred from nonexistence alone.

The feasibility authority relied on is `XASSET-0024` §D's route table, whose "**Lawful in principle?**"
column is an accepted determination distinct from any specification text: `R1` and `R2` are "**YES,
conditionally**" with `R1` marked "**Originate**"; non-routes `N1`–`N8` are "**NO**". `XASSET-0025`'s
`T1`–`T10` criteria map onto the gates, and `XASSET-0027` §F closes **`T5` only** — "It closes nothing
else: `T1`, `T2`, `T3`, `T4`, and `T6` through `T10` are untouched."

| Gate | Class | Closable | Basis — or exact blocker |
|---|---|---|---|
| `G1_DRIVER_SUBJECT_MATTER` | categorical | **YES → `PASS`** | `XASSET-0024` §D independently determines the six are "**subject-matter classes** describing what evidence is about… A qualifying source must therefore be admissible as a DRIVER under at least one of the six **on its own subject matter**." That is authority beyond the frozen `R3`. §M.1 routes §K.1's *magnitude* ambiguity through `G2` specifically, so importing it into `G1` would be a new rule — the prior head's error. |
| `G2_MAGNITUDE_INTRINSICALITY` | categorical | **YES → `UNABLE_TO_DETERMINE`** | `subject_matter = PASSES` (§D operative); `preference_only = FAILS` (§K.1 contrary reading; `PROTOCOL` §7 "no candidate can succeed") → reading-dependent, all 680. §M.1 fixes this as the designed carry point for §K.1. |
| `G3_NORMALIZATION` | categorical | **NO** | Expressly reserved. §J.3: "Whether that suffices to carry a share-of-the-whole statement **is what `G3` tests**." §M.3: "§J.1 identifies the difficulty; **it does not determine that no bridge exists**… the answer is a finding of the study rather than an assumption of the charter." `T1` is untouched by §F. |
| `G4_ORIGIN` | categorical | **YES → `PASS`** | §D's route table affirms `R1`/`R2` lawful in principle and bars `N1`–`N8` by name — an accepted feasibility determination, not the specification restating itself. |
| `G5_CONSTRAINT_SHAPE` | categorical | **NO** | **Expressly reserved — the prior head wrongly marked this `PASS`.** §M.4: "Whether a particular deployability or structural-limit candidate is constraint-shaped in that sense **is exactly what `G5` decides, per candidate, on the candidate's own terms. No prejudgment is recorded here.**" Most acute for `sleeve_deployability`, but the reservation is general. |
| `G6_ROUTE_COMPLIANCE` | categorical | **YES → `PASS`** | Two independent supports: §D's route table (`R1`/`R2` lawful in principle) for `T3`, and `XASSET-0027` §F for `T5` — "**This closes the universal `T5` failure**", fixing that competent Level-1 endpoint authority may extend to a source at its own creation or adoption. |
| `G7_DISCRETION_AND_PROVENANCE` | categorical | **YES → `PASS`** | `XASSET-0024` §E.1: class 4 "**is a lawful route**, and it is not a third route," expressly named permitted by `XASSET-0020` §L and `XASSET-0023` §H.4 item 2; §D fixes classes 1–5 lawful and 6 disqualifying. |
| `G8_UNIQUENESS` | categorical | **NO** | `T6` untouched by §F. Uniqueness is "across the admitted set"; `R6` gives only *source-level* uniqueness, and no admitted set exists. Uniqueness over an empty set is trivially satisfied or unknowable, with no accepted rule selecting. |
| `G9_REPRESENTATION` | prerequisite | **NO** | Path 2 is closable (no Level-1 rule exists — `XASSET-0023` §H.5, `XASSET-0027` §P.2). Path 1 is source-dependent and `R8` expressly "asserts no prior representation rule." Additionally unreconciled: §G path 3 says **mandatory abstention** while the gate's declared failure class is **prerequisite**. `T9` untouched. |
| `G10_PAIR_INDEPENDENCE` | categorical | **NO** | `T10` untouched. §H.4 requires the unresolved pair "is not an input to it at all"; the 120 `PAIR__` constructions are direct pair evidence by definition. Whether a named `XASSET-0020` §H pair is *unresolved* is determined nowhere, and the evidence that would settle it may sit behind the `risk_lane_boundary`. |
| `G11_EXACTNESS_AND_DETERMINISM` | categorical | **YES → `PASS`** | `XASSET-0024` §C fixes the units regime — "carried at **exact source precision or as an exact rational derivation** under `XASSET-0021` §G" — and §D's `R2` row affirms an "exact, single-valued, byte-identically reproducible" derivation lawful in principle. The weakest of the closable set; recorded with its basis rather than asserted. |
| `G12_SNAPSHOT_ADMISSIBILITY_PATH` | prerequisite | **NO** | **The prior head wrongly froze `FAIL` from absence alone.** The gate asks whether a lawful successor is *identifiable*, and the canonical mapping is `G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED`. §P.2 **does** name a required `XASSET-0021` snapshot successor, which supports identifiability — while adding that it "cannot admit evidence that does not yet exist," which bears on the gate's second conjunct "*that could admit the candidate*." No governed definition of "identifiable" exists and nothing fixes the tense of "could admit." Two defensible answers; nonexistence alone is not non-identifiability. |

**Six closable under current authority, six not.** `G3`, `G5` and `G12` are blocked by express
reservations or an undefined governed term; `G8`, `G9` and `G10` by criteria `XASSET-0027` §F leaves
untouched. **`G3` alone is sufficient for the negative determination**, and it survives the
re-derivation unchanged.

#### E.1 Invalidation and re-derivation triggers

Each closable result above is a **current-authority determination**. It may be carried forward without
separate re-analysis only while its controlling authorities and premises hold. If any listed trigger
fires, that gate **must be re-derived** under the successor authority before it is relied on again.
Several triggers are already `XASSET-0027` §Q reopen triggers and are marked **§Q**.

| Gate | Controlling authority / premise | Re-derivation required if |
|---|---|---|
| `G1` | `XASSET-0020` §E.1 DRIVER classes and their scope language; `XASSET-0024` §D's subject-matter determination; `XASSET-0027` §M.1's routing of §K.1 through `G2` alone | §E.1's classes or scope are amended (**§Q**); §D's subject-matter determination is amended or superseded; §M.1's routing changes, or a reading slot is added to `G1` |
| `G2` | `XASSET-0024` §D (operative reading) and §K.1 (contrary reading preserved); `XASSET-0027` §M.1; the canonical `g2_reading_mapping` closed table | §K.1 is resolved or amended in either direction, including a reviewer establishing the contrary reading (**§Q**); §E.1 is clarified in a way that settles magnitude capability (**§Q**); the reading map or its `required_g2_gate_result` coupling changes |
| `G4` | `XASSET-0024` §D's route table (`R1`/`R2` lawful in principle; `N1`–`N8` barred) and §F Limb 2; `XASSET-0023` §H's "no third route" | The route/non-route set or their lawfulness changes; §F's origin limbs are amended; `XASSET-0019`–`XASSET-0026` effective identity changes (**§Q**) |
| `G6` | `XASSET-0024` §D's route table; `XASSET-0023` §H.2 items 1–6 / §H.3 items 1–7; `XASSET-0027` §F's `T5` closure and §D's constitution of `LEVEL1_ENDPOINT_AUTHORITY` | The `R1`/`R2` route contract changes; §H.2/§H.3 conditions are amended; competent-authority terms or `T5`'s closure change; `XASSET-0019`–`XASSET-0026` effective identity changes (**§Q**) |
| `G7` | `NUM-0001` §1 classes and §§6–8; `XASSET-0024` §E.1's class-4 determination and §E.3's eight-item test; `XASSET-0023` §H.4 | `NUM-0001`'s classes, §6, §7 or §8 change (**§Q**); the class-4/class-5 governance requirements or the anti-discretion test change; route-class coherence changes |
| `G11` | `XASSET-0024` §C's units regime and §J.11; `XASSET-0021` §G's exactness/rational-derivation rules; §D's `R2` byte-identical requirement | `XASSET-0021` §G's exactness authority changes, or the snapshot is lawfully replaced or extended (**§Q**); §C's units regime or §J.11 changes; either pinned canonical hash changes (**§Q**) |

**A general trigger applies to every row**: if either pinned canonical hash changes, or
`XASSET-0019` through `XASSET-0026`'s effective identity changes (**§Q** in both cases), the whole
snapshot is re-derived rather than inherited.

**This is not hypothetical.** §G's semantic prerequisite for `G3` contemplates exactly "a narrowly
scoped clarification of `XASSET-0020` §E.1" — the amendment named in `G1`'s and `G2`'s trigger rows.
A successor that unblocks `G3` that way **must re-derive `G1` and `G2`**, and must not carry today's
results forward as settled.

### F. §K.1 is preserved, not resolved

This filing adopts neither §K.1 reading. It records that `XASSET-0024` §D determines the subject-matter
reading *as operative for Outcome A*, that §K.1 preserves the contrary reading and states its
consequence, and that §M.1 fixes the dual-reading fields as the mechanism carrying the question rather
than deciding it — at `G2`, and only at `G2`. No `g2_outcome_under_*` value is asserted for any
construction; no results document exists.

### G. Successor model — semantic prerequisites first, then one reconciliation pass

**Corrected after review `4947130884` MAJOR 2.** The prior head listed prerequisites "ordered by
dependency" and put the validator conformance correction **first**. That ordering is wrong for the
accepted `XASSET-0029` mechanism and would very likely be paid for twice.

**Why the order matters.** `XASSET-0029` binds **both** the canonical `PROTOCOL_V1.md` /
`pre_registration.yaml` pins **and** the load-bearing validators to the authorized merged tree (§D).
A successor that makes Stage 1 deterministic must ultimately be reconciled into the canonical
gate-evaluation contract; if that later changes the canonical artifacts or the validators, an *earlier*
validator-only reauthorization is invalidated by design. **Do not spend one reauthorization lifecycle
on an intermediate enforcement state that a later methodology or canonical change is expected to
supersede.** The correct shape is therefore two classes, not one ordered list.

**None of the following is authorized here.**

#### G.A — Semantic / governance prerequisites (resolve first)

The outcome-determining methodology questions. These are governance work and do not require, and must
not be preceded by, any validator correction or reauthorization lifecycle.

- **`G3` — the `T1`/`T2` share-of-the-whole question**, expressly reserved by §J.3 and §M.3. §K.1 names
  the shape of the smallest corrective: "a narrowly scoped clarification of `XASSET-0020` §E.1 alone."
  **Note the coupling**: that clarification is `G1`'s and `G2`'s §E.1 invalidation trigger, so it
  re-opens both (§E.1).
- **`G5`'s constraint-shape rule** (§M.4) — a governed per-candidate evaluation rule, or an accepted
  determination that none is available.
- **`G12`'s "identifiable"** — a governed definition, including the tense of "could admit the candidate"
  for a source that does not yet exist.
- **`G8`'s uniqueness** over an empty admitted set.
- **`G9`'s representation treatment** — reconciling §G path 3's "mandatory abstention" with the gate's
  declared prerequisite failure class.
- **`G10`'s unresolved-pair question**, within the `risk_lane_boundary`.

**These need not be one filing.** Independent governance questions may be filed separately or lawfully
batched where authority permits; this decision prescribes neither the packaging nor any outcome. Some
may proceed in parallel as read-only or governance work, subject to the repository's one-mutation-lane
discipline.

#### G.B — Final canonical / enforcement / reauthorization reconciliation (one coherent pass)

**Only after the Stage-1 semantic contract is stable enough to execute**, and in this order:

1. Reconcile the final accepted gate semantics into the canonical Stage-1 artifacts as required.
2. Correct the validator's categorical-precedence enforcement defect (§C).
3. Update any validator, generator, or runner implementation the final accepted semantics require.
4. Recompute canonical pins **only after** the final bytes stabilize.
5. Perform **one** successor operational-authorization / load-bearing rebinding lifecycle against the
   final canonical **and** enforcement bytes (§D).
6. Establish runner execution-readiness.
7. Only then may Stage 1 be armed — one-shot arm, claim, and the 680-construction run.

**No early validator-only reauthorization prerequisite exists**, and none is created here. The
conformance defect of §C is real and still requires correction; what changed is *when* — it belongs in
G.B's single pass, not ahead of the semantic questions that determine what the corrected enforcement
must encode.

**This decision authorizes none of G.A or G.B**, and performs no part of either.

### H. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; arms and executes no Stage 1; creates no Stage-1 runner and no `stage1_results.yaml`;
consumes nothing of `ATTEMPT_1`; evaluates no gate for any construction and asserts no per-construction
outcome; corrects no validator and performs no load-bearing reauthorization; acquires no market,
fundamental, economic, or Stage-2 data; amends no canonical file and changes no hash pin, universe,
cardinality, or construction identity; resolves `XASSET-0024` §K.1 neither way and amends no
`XASSET-0020` §E.1 scope; resolves no §J.12, grants no Stage 2, and grants no application authority;
invents no Level-1 representation aggregation or selection rule and designates no CM-14–CM-17
membership; selects no sleeve and creates no endpoint, bound, point, range, percentage, weight, rank,
target, or allocation; reuses no RISK scenario, value, parameter, window, result, or private artifact;
weakens no validator or test; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no chart, ladder,
deployment, trade, order, or brokerage action; and rewrites no accepted history.

## Rationale

The standard was not "a competent analyst could answer the gates." It was that two independent
conforming executors, given identical frozen inputs, must not be able to select different lawful
results. `G3` alone defeats that, and `G5`, `G8`, `G9`, `G10` and `G12` each defeat it independently.

The correction sharpened two things the first head got wrong, and both errors ran in the same
direction — toward overstating what authority establishes.

**Finding 1 was diagnosed too weakly.** Calling it an open election implied the validator's prohibition
had standing equal to an accepted decision and two canonical artifacts. It does not: the YAML is
canonical for gates and vocabularies, the protocol is expressly subordinate and pre-labels this exact
shape of divergence as a defect, and the validator disclaims gate-deciding authority in its own
docstring. Naming it a conformance defect removes an invented governance step and states current truth.

**The gate table was too generous.** Marking `G4`–`G7` and `G11` `PASS` because the frozen
specification requires the tested property is the by-construction inference this decision elsewhere
rejects. Re-deriving each against `XASSET-0024` §D's "lawful in principle" column, §E.1's class-4
determination, §C's units regime and `XASSET-0027` §F's `T5` closure kept five of them — on real
independent authority — and cost `G5`, which §M.4 expressly reserves in the same way §M.3 reserves
`G3`. `G12` likewise could not survive: "no successor exists" is not "no successor is identifiable,"
and the canonical mapping says the gate tests identifiability only.

That the count moved from 7/5 to 6/6 while the conclusion held is the useful result. The negative never
depended on the count; it depends on `G3`. What the count determines is successor scope, and a
successor scoped against the prior table would have inherited two wrong dispositions.

## Alternatives Considered

**Treat Finding 1 as a governance election** (the prior head). Rejected on review: the precedence
question is already answered in committed text, and preserving the election would have manufactured a
governance step while leaving the accepted semantic direction misstated.

**Correct the validator here.** Rejected: it is a load-bearing authorization path (§D), and a
governance-only negative determination is not the vehicle for a change that also requires a
reauthorization lifecycle. Recording the dependency is this unit's remit; discharging it is not.

**Make the validator correction the first successor prerequisite** (correction 1's ordering). Rejected
in correction 2: `XASSET-0029` binds canonical pins *and* load-bearing enforcement to one authorized
tree, so a validator-only reauthorization performed before the semantic questions settle is invalidated
by design as soon as the resulting methodology is reconciled into the canonical artifacts. Sequencing it
into G.B's single pass costs nothing now and saves an entire authorization lifecycle later.

**Treat the 6/6 table as durable closure.** Rejected in correction 2: `G1` rests on `XASSET-0020` §E.1
and `XASSET-0024` §D, and `G2` on §K.1's present unresolved state — both `XASSET-0027` §Q reopen
triggers, and both squarely in the path of the §E.1 clarification §G.A proposes for `G3`. Freezing them
would hand a successor two stale results at exactly the moment their basis changed.

**Preserve the 7/5 table.** Rejected: `G5` and `G12` do not survive their own controlling text, and a
successor scoped against a wrong table is worse than no table.

**Close the method by adopting by-construction inference.** Rejected: `XASSET-0028` §F puts Stage 1's
question at lawful satisfiability, so the inference would convert the twelve gates into a restatement
of the generator.

**Extend dual-reading treatment to `G3`.** Rejected as insufficient rather than wrong: the
subject-matter branch is itself what §J.3 and §M.3 reserve, so the gap relocates instead of closing.

**File nothing and re-attempt Stage 1.** Rejected outright: `ATTEMPT_1` is one-shot and
rerun-after-outcomes is prohibited.

## Consequences

Stage 1 stays unarmed, and the successor model is now both smaller and correctly sequenced: six
semantic questions resolved first — one of them, `G3`, with a corrective §K.1 already names — followed
by a single coherent canonical/enforcement/reauthorization pass, against six gates that **need no
separate work while their controlling authority remains unchanged**.

That last qualifier is the substance of the MAJOR 1 correction, not a hedge. The `G3` corrective most
likely to unblock Stage 1 is an `XASSET-0020` §E.1 clarification, which is precisely `G1`'s and `G2`'s
invalidation trigger. A successor reading the snapshot as frozen closure would carry two stale results
through the very amendment that changed their basis.

The negative outcome remains the honest one, and it is still the cheap one: one governance filing and
two corrections, against a single irreversible execution of a 680-construction study resting on
undisclosed judgments — and now, against a successor sequence that does not pay for reauthorization
twice.
