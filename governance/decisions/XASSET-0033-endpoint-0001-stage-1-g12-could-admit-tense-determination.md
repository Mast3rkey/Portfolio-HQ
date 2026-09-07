---
decision_id: XASSET-0033
date: 2026-08-17
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_g12_could_admit_tense.py
---

## Context

### Live preflight

Verified independently before any mutation, against live GitHub and git state rather than inherited
narrative:

| Fact | Verified |
|---|---|
| GitHub `main` / `origin/main` / local `HEAD` | all `eebc4d6642353d50807f0f40f8a3ceed5ef8d97c` |
| PR #331 (`XASSET-0032`) | merged; `eebc4d66…` is its merge commit |
| Merge-commit CI | run `31988605930`, `head_sha` `eebc4d66…`, completed/**success** |
| Open PRs | **zero** |
| Working tree / stash / worktrees | clean / empty / sole worktree |
| `XASSET-0033` identifier | unused anywhere in the repository |
| `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` |
| `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` |
| Construction universe | regenerated live: **680** constructions, `73c0965e…5224` |
| `LOAD_BEARING_RELPATHS` | exactly the six `XASSET-0029` paths |
| `stage1_results.yaml` / runner | **absent** |
| `new_execution_is_authorized()` | `(False, 'no attestation present … There is no merge-to-execution gap')` |

**`ATTEMPT_1` is intact, unclaimed, and unconsumed, and remains so after this filing.**

### The question this unit answers

`XASSET-0032` §H determined `G12_SNAPSHOT_ADMISSIBILITY_PATH` **NOT CLOSABLE**, closing its floor
(§H.1, nonexistence of a successor is never by itself `FAIL`), its scope (§H.2, identifiability only,
never full §J.1 admission), and its named dependency (§H.3). It left exactly one blocker: **the tense
of "could admit"**, recorded at §H.4 as two grounded readings producing opposite results.

This unit takes that single surviving blocker and asks:

> Under already-accepted authority, can "Is a lawful `XASSET-0021` snapshot successor **identifiable**
> that **could admit** the candidate" be deterministically assigned one temporal reading such that two
> independent conforming executors, handed the same frozen inputs, cannot lawfully return opposite
> `G12` results?

---

## Decision

### A. Verdict

**`G12_COULD_ADMIT_TENSE_NOT_CLOSABLE`.**

`G12` remains **NOT CLOSABLE** and its `XASSET-0032` classification is unchanged. The blocker is,
however, **materially narrowed**: this unit closes one further sub-question (§C), and removes both
texts previously recorded as *supports for* the present-tense reading by showing they are **neutral**
between the readings rather than supports for either (§E). What survives is smaller and stated exactly
at §G.

**This is a negative determination reached on the authority, not a deferral for convenience.** Closure
was tested seriously and at length (§F), and the asymmetry between the two readings is now large. It is
not large enough to make the competing reading *unlawful*, which is the bar closure requires.

### B. The ambiguity, reproduced from canonical bytes

Canonical gate text, `pre_registration.yaml` `gate_sequence.gates[11]`, verbatim:

> `gate_id: G12_SNAPSHOT_ADMISSIBILITY_PATH`
> `question:` Is a lawful XASSET-0021 snapshot successor identifiable that could admit the candidate,
> noting that no snapshot successor is created, extended, or authorized by this program?
> `controlling_authority: XASSET-0024_J_1_AND_J_2_AND_XASSET_0026_G_2_CONSTRAINT_3`
> `failure_disposition: BLOCKED_PENDING_SEPARATE_PREREQUISITE`

Six distinguishable questions live in that sentence. Accepted authority answers five:

| # | Question | Status |
|---|---|---|
| 1 | Must a successor **exist**? | **Closed** — no. `XASSET-0032` §H.1: nonexistence is never by itself `FAIL` |
| 2 | What does **identifiable** require? | **Closed at its floor** — a namable dependency; `XASSET-0032` §H.1/§H.3 |
| 3 | Is the named dependency identified? | **Closed** — yes; `XASSET-0032` §H.3 |
| 4 | Does `G12` test full §J.1 admissibility? | **Closed** — no, identifiability only; `XASSET-0032` §H.2 |
| 5 | Is the candidate-relative clause **operative**? | **Closed by this unit** — yes; §C below |
| 6 | Is "could admit" evaluated **now** or **in the ordered sequence**? | **OPEN** — §G below |

### C. The clause is operative — the dissolution route is closed

A successor might be tempted to dissolve the tense question by deleting its subject, because
`PROTOCOL_V1.md` states `G12` twice **without** the candidate-relative clause:

- §6 gate table, row 12: "a lawful snapshot successor is identifiable (`J.1`, `J.2`)";
- §6.1: "`G12` records whether a snapshot successor is *identifiable*."

Neither shortens the gate. `PROTOCOL_V1.md`'s own opening states the precedence, verbatim:

> `research/level1_endpoint_evidence/pre_registration.yaml` is canonical for every closed identity,
> candidate, gate, ordering, vocabulary, and count. **This protocol explains the design. It cannot
> enlarge or override the YAML.** Where the two appear to differ, the YAML governs and the difference
> is a defect requiring a governed correction.

The YAML is canonical **for gates** by name, and the YAML carries the clause. A shorter restatement in
a document that cannot override the YAML does not delete a conjunct from it.

> **Therefore: "that could admit the candidate" is operative gate text. `G12` may not be evaluated as
> bare successor-identifiability with the candidate-relative conjunct dropped.** This forecloses
> resolving `G12` by dissolution, and it is recorded here so the shorter §6/§6.1 phrasings are not
> later mistaken for the gate.

This is **not** a defect finding against `PROTOCOL_V1.md`. §6 is a summary table and §6.1 is an
explanatory gloss on the *categorical/prerequisite* distinction; neither purports to restate the gate
in full, and abbreviation is not divergence. No governed correction is triggered.

### D. The two readings

**Present-tense / current-candidate-capability.** The identifiable successor must be able to admit the
candidate as it stands at evaluation time. Every registered construction freezes
`source_architecture: HYPOTHETICAL_SOURCE_ARCHITECTURE` — canonically, sources that "do not yet exist"
— so no successor could admit any of them now. Yields `FAIL` for all 680.

**Forward-looking / ordered-successor-capability.** The separately authorized successor is
*identifiable* because accepted ordering positions it to admit the evidence once the evidence exists.
Existence now is not required. Yields `PASS` on the identifiability conjunct.

### E. What this unit closes: both texts cited for the present-tense reading are neutral

`XASSET-0032` §H.4 recorded the present-tense reading as "supported by `XASSET-0026` §G.2 constraint 3
and `XASSET-0027` §P.2". Both were re-read in full, in their own sections, rather than as the extracted
sentence they share. **Neither is a capability verdict. Both are ordering statements, and an ordering
statement is consistent with either reading.**

**E.1 — `XASSET-0026` §G.2 constraint 3 is, by its own section heading, an ordering constraint.** §G.2
is titled "**Four ordering constraints that do bind, on every packaging.**" Constraint 3's own title is
"**Snapshot successor after evidence, before any application.**" Its operative sentence is paired:
"A snapshot successor cannot admit evidence that does not yet exist, **and no application may read the
evidence before it does**" — two halves bracketing the successor's *position*, between evidence and
application. `XASSET-0026` then says so explicitly: "unlike the first two, **the third's position in
the sequence *is* fixed**."

**E.2 — `XASSET-0027` §P.2's clause is a sequencing qualifier in a list of required future units.**
§P.2 is titled "**Separately required successors, none authorized here.** Named so they are not
discovered late", and each bullet pairs a required future successor with a note on when it becomes
required or operable. Read in that column:

| Bullet | Its qualifier |
|---|---|
| endpoint-admission validator | "**if and when a candidate source exists to test**" |
| §J.12 reconciliation determination | "**at the first later stage where actual candidate endpoint values or sets coexist**" |
| **`XASSET-0021` snapshot successor** | "**which cannot admit evidence that does not yet exist**" |
| Level-1 aggregation or selection rule | "**only if and when a candidate source is not self-contained**" |

The `G12` clause occupies the same grammatical slot as three explicit timing qualifiers. It says *when*
the successor becomes operable, not *whether* one is identifiable today.

**E.3 — Why this is a narrowing and not a closure.** The ordering character cuts both ways, and this
unit refuses to overstate it. A present-tense proponent may reason *from* the ordering: because the
successor must follow the evidence, and the evidence does not exist, no lawful successor could admit
this candidate now. That inference is available. What is **not** available is citing §G.2 constraint 3
or §P.2 as *independent affirmative support* for the present-tense reading, because in their own
sections both are neutral as to how a gate asked **before** the evidence exists must be answered.

> **Therefore: the present-tense reading's affirmative authority support reduces to the gate's own
> unglossed modal, plus the frozen `source_architecture` identity field.** That is materially less than
> `XASSET-0032` §H.4 recorded, and it is the whole of this unit's positive contribution to the balance.

### F. What supports the forward-looking reading, and why it still falls short

**F.1 — The canonical Stage-1 evaluation register.** Two statements in the **gate-canonical YAML**
describe what Stage 1 evaluates:

> `stage_1.description`: "A deterministic, per-candidate evaluation of whether a lawful
> endpoint-supporting evidence construction **is identifiable for that candidate** under accepted
> authority… **Stage 1 evaluates constructibility** over the Stage-1-testable subset of XASSET-0024
> §J. It does not build, acquire, estimate, or admit anything."

> `no_source_identity_note`: "Stage 1 evaluates whether the frozen specification is **lawfully
> satisfiable** under the twelve gates; it does not search the world for an organisation. **A negative
> therefore means the registered specification was evaluated and blocked**, never 'no source this
> executor happened to find'."

Alongside `acquires_data: false` and `produces_admissible_evidence: false`, these describe a
**constructibility/satisfiability** register — modal and forward-looking — covering "the twelve gates".

**F.2 — §J's own frame.** `XASSET-0024` §J is titled "Minimum evidence properties for the next research
or authority unit" and opens "A future unit seeking a lawful Level-1 bound **must produce a source**
satisfying all of the following." §J.2 requires the source to be "Present in `XASSET-0021` §§C.2–C.3,
or in a snapshot **lawfully replaced or extended by a separate future authorization**." §J.1 and §J.2
are thus requirements on a **future produced source**, evaluated when it is produced.

**F.3 — Why this does not reach the closure bar.** Closure requires showing the competing reading
**unlawful**, not merely worse supported. Three honest obstacles remain:

1. **The register statements describe Stage 1, not a gate-level modal rule.** `stage_1.description` and
   `no_source_identity_note` say what Stage 1 evaluates; neither says "therefore every gate question's
   modal is read counterfactually." Bridging that gap is an inference — a good one, and this unit
   records it as such rather than as authority.
2. **The gate's own words are canonical and operative (§C).** An executor reading "could admit" in a
   present register is reading the governing artifact on its face, against a frozen identity field
   (`source_architecture`, `source_architecture_selectable_at_result_time: false`) they are entitled to
   read. Removing the *supports* for a reading does not make the reading unlawful.
3. **A universal structural negative is not itself disqualifying.** The tempting objection — that
   present-tense would fail all 680 identically and so cannot be right — is unavailable.
   `XASSET-0025` §D already establishes exactly that shape as acceptable: "any source outside the
   frozen snapshot fails **T8** under existing authority regardless of its other properties … This is
   not a finding about any particular source; it is the shape of the current authority." Present-tense
   `G12` would be a second instance, and `BLOCKED_PENDING_SEPARATE_PREREQUISITE` for all 680 is a
   coherent, honest Stage-1 outcome, not an absurdity.

### G. The exact surviving degree of freedom

> **No accepted text defines the modal "could", states a gate-level tense or modal rule, or ranks the
> canonical Stage-1 register statements (§F.1) above the `G12` question's own unglossed wording (§C).**

Two conforming executors may therefore still lawfully diverge:

| Executor | Reads the modal against | `G12` result | Ground, and why it is not unlawful |
|---|---|---|---|
| **A** | the state of the world at execution time | `FAIL`, all 680 | The operative clause on its face plus the frozen `HYPOTHETICAL_SOURCE_ARCHITECTURE` identity field. Does not violate `XASSET-0032` §H.1 (its ground is *candidate* nonexistence, not *successor* nonexistence) or §H.2 |
| **B** | lawful satisfiability of the frozen specification | `PASS` on the identifiability conjunct | §F.1's register, §F.2's frame, and §H.1/§H.3's named ordered dependency |

**Executor A's ground is narrower than it was before this filing** — §E strips both cited supports —
but it is not foreclosed.

### H. Corrections to prior basis statements, classification unchanged

Recorded in this unit's own text; **no prior decision's text is edited**, per the repository's
never-silently-rewrite convention. Each narrows a basis while leaving its classification untouched —
the same pattern `XASSET-0032` §H applied to `XASSET-0030`.

| # | Prior statement | Correction | Classification |
|---|---|---|---|
| H.1 | `XASSET-0032` §H.4: the present-tense reading is "supported by `XASSET-0026` §G.2 constraint 3 and `XASSET-0027` §P.2" | Both are ordering statements, neutral between the readings, not affirmative supports for present-tense (§E) | `G12` **NOT CLOSABLE** — unchanged |
| H.2 | `XASSET-0032` §H.3: "`PROTOCOL_V1.md` §12 records the dependency order" | The quoted sentence is at `PROTOCOL_V1.md` **§17** ("Lifecycle and downstream boundary", line 524); §12 is "Parameters, and why there are none". The **quotation is accurate**; only the section number is wrong | `G12` **NOT CLOSABLE** — unchanged; §H.3's substance stands |

Neither correction fires any `XASSET-0032` §E.1 invalidation trigger, and neither disturbs the
`XASSET-0030` 6/6 partition.

### I. The smallest distinct future authority required

**Smallest sufficient corrective — a `G12`-scoped modal statement.** One governed sentence fixing
whether `G12`'s "could admit" is evaluated against execution-time world state or against lawful
satisfiability of the frozen construction specification. It requires **no new evidence**, no
methodology amendment, no change to `G12`'s wording, and no snapshot successor. It touches one gate.

**A broader corrective would also work, at a materially wider blast radius.** A program-wide statement
of the gate-question modal register would resolve `G12` and would sit naturally beside §F.1's existing
Stage-1 register statements — but it would bear on **every** gate, including the six the
`XASSET-0030` snapshot records as closable, and would therefore be an invalidation trigger for that
partition. It is recorded here as an available option and as a **caution**, not a recommendation.

**Neither is authorized, drafted, scoped, or begun by this filing.**

### J. Preservation and non-authorization

- The `XASSET-0030` **6/6 gate partition is unchanged**. `G1`, `G2`, `G4`, `G6`, `G7`, and `G11` are
  **not re-derived**, and nothing here fires an `XASSET-0032` §E.1 invalidation trigger.
- `XASSET-0031`'s `G3` determination is **neither reopened nor used as a premise**.
- `XASSET-0032`'s `G5`, `G8`, `G9`, `G10` determinations are **untouched and not used as premises**.
  Its `G12` classification is **preserved**, with the basis narrowed at §E/§H.
- `XASSET-0020` §E.1 is **not amended**; `XASSET-0024` §K.1 is **not resolved**.
- **No snapshot successor** is created, extended, replaced, identified as existing, or authorized.
- **No gate is evaluated for any construction.** No candidate disposition, cell outcome, or roll-up is
  produced. No `stage1_results` document exists or is authorized.
- **Stage 1 remains NOT EXECUTABLE and UNARMED.** No arming, attestation, lane, claim, completion,
  ledger entry, or runner. `ATTEMPT_1` is intact and unconsumed.
- **No canonical byte, hash pin, universe entry, or `LOAD_BEARING_RELPATHS` member is changed.** No
  protected `RISK-0001` evidence path is read or referenced.
- **No portfolio effect of any kind**: no sleeve membership or weighting, no Level-2 change, no
  `targets.yaml` / `holdings.yaml` / `gates.yaml` mutation, no allocator, margin, ladder, chart, order,
  or trade change.

---

## Rationale

`XASSET-0032` left `G12` with one blocker and called it "the honest hard case." Taking a single
sentence as a whole unit was therefore the right shape: there was no second question to batch, and the
`XASSET-0030` §G.B canonical/enforcement pass remains separately reserved.

The unit's real work was **reading the cited authority in its own sections rather than as the sentence
it shares**. "A snapshot successor cannot admit evidence that does not yet exist" appears in two
accepted decisions, and in both it sits inside an explicitly ordering frame — §G.2's own heading names
its four items ordering constraints; §P.2's own heading names its bullets separately required
successors, three of the four carrying overt timing qualifiers. An extracted sentence looks like a
capability verdict; the same sentence in its section is a statement about position in a sequence. That
distinction is the filing's principal finding, and it is the reason the balance between the two
readings has shifted even though the verdict has not.

Closure was genuinely attempted, not gestured at. The strongest available case — §F.1's canonical
register plus §F.2's future-source frame plus §E's removal of the competing supports — is a strong
case. It was rejected against the standard this task set and this series has followed: the competing
reading must be shown **unlawful**, not merely less attractive. Three obstacles survived (§F.3), and
the third is the sharpest: `XASSET-0025` §D forecloses the intuitive "it cannot be that a gate fails
every candidate" objection, because this repository has already accepted a gate of exactly that shape.
A reading that produces an uncomfortable but coherent structural negative is not thereby unlawful.

The instruction not to choose a tense because it is the smallest corrective or because it would unlock
`G12` was treated as binding, and it bit. The forward-looking reading is the one this unit would adopt
if adoption were on offer, and it is also the reading that unlocks the gate — which is precisely why it
needed the higher bar rather than the lower one. Recording it as "better supported, not established"
is the honest result.

§C was added because the tense question has an escape hatch that would look like a solution: two
`PROTOCOL_V1.md` restatements omit the very clause whose tense is at issue. Left unrecorded, a
successor could resolve `G12` by quietly dropping the conjunct. The precedence rule closes that route
in one line, and the point is worth pinning even though it resolves nothing on its own.

---

## Alternatives Considered

**Close `G12` on the forward-looking reading.** Rejected — the reasoning is at §F.3. It is the better
reading; it is not established as the only lawful one. Adopting it here would have converted an
inference from Stage-1-level register statements into a gate-level rule that no accepted text states.

**Close `G12` on the present-tense reading.** Rejected more firmly. After §E, its affirmative support
reduces to the gate's bare modal and a frozen identity field, while the canonical register statements
point the other way. It survives as *lawful*, not as *correct*.

**Dissolve the clause using `PROTOCOL_V1.md` §6/§6.1.** Rejected and expressly foreclosed at §C. The
YAML governs gates and carries the conjunct; a summary table cannot delete it.

**Record `PROTOCOL_V1.md` §6/§6.1 as a defect requiring governed correction.** Rejected. The
precedence rule makes a *difference* a defect, and abbreviation in a summary row and an explanatory
gloss is not a difference in what the gate requires. Manufacturing a defect finding would create
correction work with no semantic content.

**Treat `CLOSURE_DETERMINATION_V1.yaml` as fixing the modal.** Rejected as unnecessary and as the wrong
artifact to lean on. Its satisfiability sentence sits in a field named `no_source_identity_reason`,
whose function is to bound source search. The materially stronger version of the same statement is in
the gate-canonical YAML itself (§F.1), which is where this filing sources it — and even there it falls
short for the reason at §F.3 item 1.

**Recommend the program-wide modal-register corrective as the smallest next step.** Rejected. It would
resolve `G12`, but it would reach every gate including the six currently recorded as closable. The
`G12`-scoped corrective is strictly smaller and is named as the smallest at §I, with the broader option
disclosed as a caution rather than suppressed.

**Correct `XASSET-0032`'s text in place.** Rejected. Both corrections at §H are recorded in this
unit's own text, leaving the prior decision unedited — the convention `XASSET-0032` itself followed
when it corrected three `XASSET-0030` basis statements.

---

## Consequences

`G12` remains **NOT CLOSABLE**, and with it the `XASSET-0030` §G.A prerequisite set remains open. All
six of that snapshot's non-closable gates stand; `XASSET-0030`'s single-gate sufficiency for the
negative is unaffected.

What changed is the **shape of the remaining work on `G12`**. Before this filing, the blocker was
stated as two readings each with cited authority support. After it, one reading's cited supports are
shown neutral, the competing conjunct is confirmed operative, and the surviving degree of freedom is a
single undefined modal (§G). The corrective named at §I is correspondingly narrow: one governed
sentence, no new evidence, no methodology amendment, one gate.

Successors should note three things. First, §E's method — reading a cited sentence in its own section
rather than as an extract — was productive here and the remaining blockers on `G5`, `G8`, `G9`, and
`G10` have not been re-examined that way. Second, the `XASSET-0030` §G.B canonical/enforcement/
outcome-producing-code/reauthorization pass remains reserved and unbegun, and `XASSET-0030` §C's
recorded enforcement conformance defect is untouched by this filing. Third, `XASSET-0032` §H.5's
disposition-inertness observation still holds and still is not a licence: while `G2` remains
`UNABLE_TO_DETERMINE` for all 680, either `G12` reading yields the same candidate disposition, but
every applicable gate must still be evaluated and recorded, and a gate that is disposition-inert today
becomes outcome-determining the moment `XASSET-0024` §K.1 is resolved.

**Stage 1 remains UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is unclaimed. No portfolio, allocation,
target, holding, gate, margin, ladder, chart, order, or trade state is changed or authorized by this
filing.**
