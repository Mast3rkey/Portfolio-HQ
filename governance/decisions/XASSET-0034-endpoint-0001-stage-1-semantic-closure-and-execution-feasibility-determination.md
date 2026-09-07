---
decision_id: XASSET-0034
date: 2026-08-17
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_semantic_closure_feasibility.py
---

## Context

### Live preflight

Verified against live repository and GitHub state before any mutation, not inherited from any prior
filing's summary:

| Check | Observed |
|---|---|
| GitHub `main` / `origin/main` / local `HEAD` | all `cd126f0ea8d6e3bbdb9e8ee8689de0136272b685` |
| `PR #332` (`XASSET-0033`) | merged, closed, merge commit is that SHA |
| Merge-commit CI | workflow run `32017402494`, `completed` / `success` |
| Open pull requests | **0** |
| Working tree / stash / worktrees | clean / empty / sole worktree |
| `XASSET-0034` | unused (zero matches repository-wide) |
| Canonical `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` **MATCH** |
| Canonical `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` **MATCH** |
| Construction universe | **680** constructions / **48** cells / `73c0965e…5224` **MATCH** |
| `LOAD_BEARING_RELPATHS` | all **6** present, unchanged |
| `new_execution_is_authorized()` | `False` — "no attestation present" |
| Runner / attestation / claim / completion / ledger / `stage1_results.yaml` | **absent** |

**Stage 1 is UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, unconsumed.**

### The question this unit answers

`XASSET-0030` §G.B step 1 requires a successor to "**Resolve all required §G.A semantic/governance
prerequisites**" before the single canonical / enforcement / outcome-producing-code / reauthorization
pass may begin. `XASSET-0032` §N then records that after `XASSET-0031` and itself, "**all six have been
examined and none is closed**."

Read together and literally, those two sentences describe a program that can never enter §G.B — because
`XASSET-0032`'s own Consequences state that two of the six "**cannot be closed by governance at all**."
This unit answers exactly one architecture/sequencing question:

> After `XASSET-0031`, `XASSET-0032`, and `XASSET-0033`, what does "resolve all **required** §G.A
> prerequisites" lawfully require, given that several gate **satisfaction** questions are inherently
> source-, candidate-, or future-snapshot-dependent?

It is a sequencing determination. It closes no gate, evaluates no construction, and creates no rule.

## Decision

### A. Determination — `SEMANTIC_CLOSURE_PARTIAL_THREE_RESIDUAL_BLOCKERS`

**The answer is MIXED (option C), and §G.B is NOT yet unlocked.**

The six §G.A items do not share one status. They divide cleanly along a line accepted authority already
draws but has never been asked to apply to the §G.B entry condition:

| Class | Gates / items | §G.B entry effect |
|---|---|---|
| **Execution-ready governed source-/snapshot-dependent states** | `G3`; `G5`; `G8`; `G9` path 1; `G10` blocker 1 | **No further governance closure is required — or, for `G3`/`G5`/`G9` path 1, possible.** These do not block §G.B. |
| **Genuine residual semantic blockers** | **B1** `G12` tense · **B2** `G10` §H.4 consumption semantics for 360 constructions · **B3** the shared reserved-gate **recording posture** | **These do block §G.B**, because §G.B step 2 reconciles *accepted* semantics and has nothing determinate to reconcile for them. |

**Neither option A nor option B is supportable on the accepted text.** Option A fails because B1, B2 and
B3 are genuine unresolved *semantic* degrees of freedom that no candidate fact could ever settle. Option
B fails because `G3`, `G5` and `G9` path 1 are expressly reserved **to the study**, so demanding their
pre-execution closure is circular — it asks governance to produce what only Stage 1 can produce.

**`XASSET-0030`'s 6/6 gate map is UNCHANGED.** No gate moves partition. `XASSET-0024` §K.1 remains
unresolved, `XASSET-0020` §E.1 unamended, `XASSET-0031`'s `G3` untouched and not used as a premise. This
filing changes no canonical byte, universe, hash pin, load-bearing path, or authorization state.

### B. What this unit reproduced before determining anything

All reproductions used the live committed bytes and the real modules. **No gate was evaluated for any
construction**, and no results document, lane state, or Stage-1 output was created.

**B.1 — The sequencing conflict is real and reproduces from the text.** `XASSET-0030` §G.B step 1 says
"Resolve all required §G.A semantic/governance prerequisites"; `XASSET-0032` §N says all six "have been
examined and none is closed"; `XASSET-0032` Consequences says `G5` and `G9` path 1 "**require a candidate
source and cannot be closed by governance at all** — they are per-candidate study findings, exactly as
`XASSET-0027` §M.4 and `XASSET-0026` §H reserve them." A literal reading of step 1 therefore makes §G.B
unreachable by construction.

**B.2 — The gate result vocabulary is closed to four values.** Canonical
`result_vocabulary.gate_result_vocabulary` is exactly `PASS`, `FAIL`, `UNABLE_TO_DETERMINE`,
`NOT_APPLICABLE`. There is no `SOURCE_DEPENDENT`, `RESERVED`, `DEFERRED`, or `NOT_YET_EVALUABLE` value,
and none may be added at results time.

**B.3 — Deterministic representations for the four states this question asks about already exist.**
Source-dependent inability to determine → `UNABLE_TO_DETERMINE`, which
`disposition_rules.candidate_disposition.precedence` maps to a candidate disposition of the same name.
Prerequisite-blocked → the `BLOCKED_PENDING_SEPARATE_PREREQUISITE` class, whose
`prerequisite_definition` requires `requires_named_dependency: true`. Abstention → eight closed
`mandatory_abstention_conditions` with `abstention_is_a_complete_outcome: true`. Categorical failure →
`BLOCKED_CATEGORICALLY`. **The vocabulary is not the gap.**

**B.4 — Nothing anywhere maps a reserved-satisfiability gate to a gate result.** A targeted search of
both canonical artifacts for any rule of the form "records / must be recorded as `PASS` | `FAIL` |
`UNABLE_TO_DETERMINE`" returns **zero** matches outside the `G2` reading table. The only worked
precedent is `g2_reading_mapping`, which is `G2`-specific by `XASSET-0027` §M.1 and which `XASSET-0032`
expressly declined to generalize ("Adding reading slots would be a new rule").

**B.5 — Stage 1's evaluation object is the frozen specification, and that is settled.** `XASSET-0028` §F,
verbatim: "Stage 1 evaluates whether a **frozen specification** is lawfully satisfiable under the twelve
gates — it does not search the world. Two executors handed the same `construction_id` receive the same
requirement set byte for byte, so a negative means *the registered specification was evaluated and
blocked*, never 'no source this executor happened to find.'" Determinism of *inputs* is therefore already
guaranteed and is not in question anywhere below.

### C. The distinction this determination turns on

Two questions have been travelling together under one word — "resolve" — and separating them is the
whole of this filing:

> **Semantic rule closure** — *what does this gate mean, and what result follows from each observable
> state of its object?* This is governance work. It is closable from accepted text, and where it is not,
> governance must close it before an irreversible run.
>
> **Satisfaction** — *what does this particular specification, source, or snapshot exhibit?* This is the
> study's work. Governance must never manufacture it.

`XASSET-0031` §A already draws exactly this line for `G3` — "the semantic condition **is** exactly
statable, and §C states it. What cannot be closed is whether any construction satisfies it" — and
`XASSET-0032` §C.1 states it as the shared method of all five of its gates: "separate the semantic rule
accepted authority *does* fix from the satisfaction question that depends on a source which does not
exist."

**What has never been decided is which side of that line §G.B step 1's word "required" falls on.** This
filing decides that, and nothing else.

**The rule adopted:** a §G.A prerequisite is **required** for §G.B entry if and only if it is a *semantic
rule* question — one where two conforming executors, given byte-identical frozen inputs, could record
different lawful gate results because accepted authority fixes no mapping. A prerequisite whose only
residue is *satisfaction* is **not** required, because §G.B step 2 reconciles semantics and a
satisfaction finding is not a semantics input.

Two guards, stated so this is not read as a general licence:

1. **Satisfaction is not a licence to decide semantics at run time.** `XASSET-0032`'s Alternatives
   rejected "file nothing and let a Stage-1 executor decide at run time" **outright**, on `ATTEMPT_1`'s
   one-shot character and `execution.rerun_rule.after_outcomes_observed: PROHIBITED`. That rejection is
   preserved in full and is the reason B1–B3 block below. What §D permits is an executor *applying an
   already-fixed rule to an already-frozen object* — not choosing what the rule is.
2. **A satisfaction finding is not a `PASS`.** `XASSET-0030` §E Standard 1 — "(a) a specification
   requiring property P is never by itself (b) proof that P is lawfully satisfiable" — and Standard 2 —
   absence "must be classified … on governed grounds, never inferred from nonexistence alone" — both
   survive unchanged and bind any executor.

### D. Execution-ready — five items that do not block §G.B

Each of the following has its semantic rule closed by accepted authority, and a residue that is
**exclusively** satisfaction. **No determination below closes a gate**; each records that the gate's
remaining openness is not a §G.B entry condition.

**D.1 — `G3`.** Rule closed by `XASSET-0031` §C.1 (the iff-condition on the §C denominator), §C.2 (limb
A barred / limb B not categorically barred), and §C.3 (`G3` is not satisfiable by competent authority).
Residue is satisfaction, and `XASSET-0027` §M.3 assigns it **by name**: "§J.1 identifies the difficulty;
it does not determine that no bridge exists… **the answer is a finding of the study rather than an
assumption of the charter.**" `XASSET-0031` §K.1 adds that judging satisfiability "**is the designed
task**". A governance unit that closed `G3` would be doing precisely what §M.3 forbids.

**D.2 — `G5`.** Rule closed by `XASSET-0032` §D.1 (originate-vs-clip, with every invalidator named).
Residue is satisfaction, reserved by `XASSET-0027` §M.4 **per candidate, on the candidate's own terms**,
with "**No prejudgment is recorded here**." §D.3's finding that the reservation is general — and that the
40 `sleeve_deployability` constructions are **not** presumptively constraint-shaped — is preserved.

**D.3 — `G9` path 1.** Path 2 is **determinately unavailable** (§F.1) and the path-3-versus-prerequisite
tension is **reconciled by both canonical artifacts** (§F.2) — two closed sub-determinations. The residue
is whether a source's own content governs every representation its authority requires, which frozen
requirement **R8** itself declares "**source-dependent**". `XASSET-0026` §H's
`SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED` is the accepted disposition of exactly this residue.

**D.4 — `G8`.** Rule closed by `XASSET-0032` §E.1 (existence **∧** uniqueness; vacuous uniqueness never
satisfies). Residue is the composition of a **future lawful snapshot successor** — a future fact, not a
semantics choice. No governance unit can supply it without creating the successor, which every accepted
authority in this program forbids.

**D.5 — `G10` blocker 1.** "Unresolved" is **defined** (§G.1) and all six canonical pairs are
**determined** under the accepted snapshot (§G.2), from committed text with no protected access. The
residue — pair status under a *successor* snapshot — is the same future fact as D.4.

**D.6 — What D.1–D.5 do not do.** They record no `PASS`, `FAIL`, or `UNABLE_TO_DETERMINE` for any gate or
any construction; they lift no reservation; they close no gate. Every gate above remains **NOT CLOSABLE**
exactly as `XASSET-0030` §E, `XASSET-0031` §I, and `XASSET-0032` §A left it. What changes is only that
their remaining openness is determined **not to be a §G.B entry condition**.

### E. Residual blockers — three, and §G.B may not begin while they stand

Each blocker below is stated against the bar this filing must meet: **exact controlling authority; the
exact unresolved semantic degree of freedom; the material consequence; and why the existing deterministic
vocabulary cannot represent it safely.**

#### E.1 — B1: `G12`'s tense of "could admit"

- **Authority.** `XASSET-0032` §H.4; `XASSET-0033`, verdict `G12_COULD_ADMIT_TENSE_NOT_CLOSABLE`.
- **Degree of freedom.** The candidate-relative clause "a lawful successor **that could admit the
  candidate**" has no fixed tense. `XASSET-0033` confirmed the clause is **operative** (it may not be
  dissolved), that both `XASSET-0026` §G.2 constraint 3 and `XASSET-0027` §P.2 are **ordering statements
  neutral between the readings**, and that **no accepted modal tie-breaker exists**.
- **Consequence.** The readings yield **opposite gate results for all 680** — `FAIL` on the present-tense
  reading, `PASS` on the identifiability conjunct on the forward-looking reading.
- **Why the vocabulary cannot save it.** Both `PASS` and `FAIL` are lawful members of the closed
  vocabulary and nothing selects. Recording `UNABLE_TO_DETERMINE` instead would itself be a third,
  unauthorized choice. `XASSET-0032` §H.5 forecloses the tempting escape: the choice is
  disposition-inert **today** only, and "**would become outcome-determining the moment §K.1 is
  resolved**" — while the gate result must be recorded either way, since
  `record_first_failing_gate_only` is `false`.
- **This is not satisfaction.** No property of any source, snapshot, or specification could settle a
  tense. It is purely a reading of committed text.

#### E.2 — B2: `G10` §H.4 consumption semantics for the 360 `DIRECT_ALTERNATIVE` constructions

- **Authority.** `XASSET-0032` §G.4 blocker 2, verbatim: "No accepted authority fixes whether a
  `DIRECT_ALTERNATIVE` construction with a sleeve counterpart consumes the corresponding §H pair.
  **Both readings are defensible and nothing selects.**"
- **Degree of freedom.** `XASSET-0024` §H.4's test is substance-based ("is not an input to it at all")
  while `unordered_pair_id` is a specification label; the 360 carry a sleeve counterpart but no
  `unordered_pair_id`.
- **Consequence.** `G10` is **categorical**. On the consuming reading, 360 of 680 constructions fail a
  categorical gate, and categorical dominance overrides `G2`'s `UNABLE_TO_DETERMINE` — flipping those
  candidates from `UNABLE_TO_DETERMINE` to `BLOCKED_CATEGORICALLY`, and propagating through
  `derive_cell_outcome` and `derive_roll_up_outcome`. This is the single largest outcome swing among all
  three blockers.
- **Why the vocabulary cannot save it.** Both readings map to lawful values; the vocabulary faithfully
  represents either. The gap is selection, not expression.
- **This is not satisfaction.** It is answerable **today**, from the frozen universe and committed text
  alone, with no source, snapshot, or protected evidence. That is precisely what makes leaving it to an
  executor unlawful under `XASSET-0032`'s own run-time rejection.

#### E.3 — B3: the shared reserved-gate **recording posture**

- **Authority.** `XASSET-0030` §E Standards 1 and 2; `XASSET-0028` §F; canonical
  `result_vocabulary.gate_result_vocabulary`; §B.4 above.
- **Degree of freedom.** For a gate whose satisfiability accepted authority **expressly reserves**
  (`G3` per §M.3, `G5` per §M.4, `G9` path 1 per `XASSET-0026` §H), evaluated against a frozen
  `HYPOTHETICAL_SOURCE_ARCHITECTURE` specification, **no accepted authority states which of the four
  closed values the executor records.** Standard 1 bars `PASS` inferred from the specification's own
  requirement; Standard 2 bars `FAIL` inferred from nonexistence alone — but Standard 2 requires
  "**governed grounds**" to select among categorical, prerequisite, and uncertainty, and for these three
  gates **no governed grounds are stated**. `XASSET-0028` §F's dichotomy ("unlawful on its face is
  categorical; merely unmet today is prerequisite-blocked") does not close it either: `G3` and `G5` are
  **categorical-class** gates, so the prerequisite limb is structurally unavailable to them, and §M.3
  expressly declines to find `G3` unlawful on its face.
- **Consequence.** `UNABLE_TO_DETERMINE` yields a candidate disposition of `UNABLE_TO_DETERMINE`; a
  categorical `FAIL` yields `BLOCKED_CATEGORICALLY`, which dominates. Because `G3`, `G5`, and `G9` are
  each applicable to **all 680**, the divergence is potentially total.
- **Why the vocabulary cannot save it.** Both values exist and both are lawful. §B.3 shows the vocabulary
  is adequate to *express* the state; §B.4 shows nothing *selects* it.
- **This is not satisfaction.** The question is not what any source exhibits. It is what an executor
  records when accepted authority has reserved the answer — a question about the recording contract.

**B3 is the highest-leverage remaining item**, because it is shared across three gates and is the only
one of the three whose resolution would also make D.1–D.3's satisfaction residues safely executable.

#### E.4 — Deliberately **not** created as blockers

Applying §C's bar, the following were each considered and **rejected** as prerequisites, so that this
filing removes work rather than adding it:

| Candidate prerequisite | Why not created |
|---|---|
| Close `G3` satisfiability | `XASSET-0027` §M.3 assigns it to the study; closing it is the act §M.3 forbids |
| Close `G5` constraint-shape per class | `XASSET-0027` §M.4 reserves it per candidate with "no prejudgment"; a class-wide rule would be new authority |
| Close `G9` path 1 self-containment | Frozen `R8` declares it source-dependent; `XASSET-0026` §H already dispositions it |
| Close `G8` successor composition | Requires creating a snapshot successor — forbidden by every accepted authority in this program |
| Close `G10` successor pair status | Same; `XASSET-0021` §D's determination is expressly scoped "under this snapshot" |
| A general gate-modal register rule | `XASSET-0033` §I already discloses this reaches **every** gate including the six recorded closable, and records it as a **caution**, not a recommendation |
| Extend `g2_reading_mapping` to other gates | `XASSET-0032` Alternatives rejected it; `XASSET-0027` §M.1 routes §K.1 through `G2` alone |

### F. Effect on `XASSET-0030` §G.B — not unlocked, and exactly why

**§G.B step 1 is satisfied for `G3`, `G5`, `G8`, `G9`, and `G10` blocker 1, and unsatisfied for B1, B2,
and B3.** The step is therefore **not** met, and §G.B may not begin.

The reason is structural rather than formal. **§G.B step 2 is "Reconcile the final accepted gate
semantics into the canonical Stage-1 artifacts."** Reconciliation is a transcription act: it presupposes
accepted semantics to transcribe. For B1, B2, and B3 there are none — so step 2 would have to *choose*
the semantics it is supposed to *record*, inside an implementation pass, without its own governance
review. That is the same defect `XASSET-0030` §G already corrected once when it moved the validator
conformance correction *out* of first position, and the same one `XASSET-0032` refused when it declined
to close `G12` on either reading.

Steps 3 through 11 inherit the defect: the enforcement layer corrected in step 3 encodes the semantics,
the runner built in step 4 computes them, and the rebinding in step 8 freezes those exact bytes against
a one-shot `ATTEMPT_1`.

**§G.B's own invariant is untouched and restated:** *no outcome-producing executable code may be created,
changed, or left outside the bound execution identity after the final rebinding and before `ATTEMPT_1`.*

### G. What a successor must do — smallest lawful path

Recorded as scope, **not** as authorization, schedule, packaging, or predicted outcome. **This decision
authorizes none of it and performs none of it.**

| Blocker | Smallest corrective | Requires new evidence? |
|---|---|---|
| **B3** | A governed **recording-posture rule** for reserved-satisfiability gates on a frozen hypothetical specification — assembling `XASSET-0030` Standards 1 and 2, `XASSET-0028` §F, and the closed vocabulary into one stated mapping, in the manner `XASSET-0031` §C assembled without adding a rule | **No** |
| **B2** | A governed determination of `XASSET-0024` §H.4 consumption semantics for `DIRECT_ALTERNATIVE` constructions carrying a sleeve counterpart but no `unordered_pair_id` | **No** — decidable from the frozen universe today |
| **B1** | A `G12`-scoped modal statement fixing the tense of "could admit" — `XASSET-0033` §I's own smallest corrective | **No** |

All three are decidable from committed text. **None requires a candidate source, a snapshot successor,
market data, or protected RISK access.** Whether they are filed as one unit or three is left open;
`XASSET-0032` §C's five-question batchability test is the available method and this filing applies it to
nothing.

Two couplings a successor must carry rather than rediscover: closing **B3** does **not** close D.1–D.5's
satisfaction residues, which remain per-candidate study findings; and any corrective reaching
`XASSET-0020` §E.1 fires `G1`'s and `G2`'s `XASSET-0030` §E.1 invalidation triggers and re-derives both.

### H. Invalidation and re-derivation triggers

| Determination | Re-derive if |
|---|---|
| §C's required-versus-not rule | `XASSET-0030` §G.A or §G.B is amended; `XASSET-0027` §M.3 or §M.4's reservations are lifted; `XASSET-0026` §H's disposition changes |
| §D.1 `G3` execution-ready | `XASSET-0027` §M.3 or §J.3 is amended; `XASSET-0031`'s determination is reopened |
| §D.2 `G5` execution-ready | `XASSET-0027` §M.4 is amended; `XASSET-0032` §D.1 is re-derived |
| §D.3 `G9` execution-ready | A Level-1 aggregation/selection rule becomes accepted (**§Q**); frozen `R8` or the canonical `representation` block changes |
| §D.4 / §D.5 successor-dependence | The `XASSET-0021` §C snapshot is lawfully replaced or extended (**§Q**) |
| §E.1 B1 | A governed `G12` modal or tense statement is accepted |
| §E.2 B2 | A governed §H.4 consumption determination is accepted; the universe's `unordered_pair_id` population or `comparison_subject_kind` decomposition changes |
| §E.3 B3 | A governed recording-posture rule is accepted; `XASSET-0030` §E's Standards, `XASSET-0028` §F, or `result_vocabulary.gate_result_vocabulary` changes |
| §F §G.B entry | Any of B1–B3 closes, or any §D item is reclassified |

**A general trigger applies to every row**, matching `XASSET-0030` §E.1 and `XASSET-0032` §M: if either
pinned canonical hash changes, or `XASSET-0019` through `XASSET-0026`'s effective identity changes
(**§Q** in both cases), the whole set is re-derived rather than inherited.

### I. Preserved unchanged

`XASSET-0024` §K.1 unresolved; `XASSET-0020` §E.1 unamended; `XASSET-0031`'s `G3` determination neither
reopened, narrowed, extended, nor used as a premise; `XASSET-0030`'s 6/6 partition, §C enforcement
conformance defect, and §D load-bearing reauthorization dependency all untouched; `XASSET-0032`'s five
determinations and four binding rules (§D.1, §E.1, §H.1, §H.2) intact; `XASSET-0033`'s
`G12_COULD_ADMIT_TENSE_NOT_CLOSABLE` intact; both canonical hash pins; the frozen 680 / 48 universe; the
six load-bearing paths; `abstention_is_a_complete_outcome`; and the `risk_lane_boundary` — whose
`protected_result_path` was **not read, listed, opened, or referenced**, and none of whose scenarios,
values, parameters, windows, or results is reused.

### J. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; arms and executes no Stage 1; creates no Stage-1 runner, result writer, or
`stage1_results.yaml`; consumes nothing of `ATTEMPT_1`; **evaluates no gate for any construction and
asserts no per-construction outcome**; closes, re-derives, reclassifies, or reorders no gate and changes
no gate's class, index, question, controlling authority, or failure disposition; corrects no validator,
extends no `LOAD_BEARING_RELPATHS`, and performs no load-bearing reauthorization or rebinding; amends no
canonical file and changes no hash pin, universe, cardinality, or construction identity; enters no part
of §G.B; acquires no market, fundamental, economic, or Stage-2 data; resolves `XASSET-0024` §K.1 neither
way; grants no Stage 2 and no application authority; creates no representation aggregation or selection
rule; selects no sleeve and creates no endpoint, bound, point, range, percentage, weight, rank, target,
or allocation; weakens no validator or test; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no chart, ladder,
deployment, trade, order, or brokerage action; and rewrites no accepted history.

## Rationale

The bar throughout this program has been `XASSET-0030`'s: not "a competent analyst could answer this",
but that two independent conforming executors, handed byte-identical frozen inputs, must not be able to
select different lawful results — because `ATTEMPT_1` is one-shot and
`execution.rerun_rule.after_outcomes_observed` is `PROHIBITED`.

That bar was applied by `XASSET-0030`, `XASSET-0031`, `XASSET-0032`, and `XASSET-0033` to the question
*is this gate closable?* — and the answer was six times NO. The present question is different, and the
difference had gone unexamined: **a gate can be un-closable for two entirely different reasons**, and
only one of them defeats determinism.

Where the residue is *satisfaction*, executor convergence is not at risk from the gate's openness,
because the object of evaluation is fixed. `XASSET-0028` §F settles this: two executors "handed the same
`construction_id` receive the same requirement set byte for byte", and a negative means "the registered
specification was evaluated and blocked". The frozen specification is the candidate. Nothing about
`G5`'s reservation makes two executors read *different* specifications.

Where the residue is a *semantic rule*, convergence fails outright. `G12`'s two tenses yield opposite
results on the same bytes. `G10`'s two consumption readings flip 360 constructions between
`UNABLE_TO_DETERMINE` and `BLOCKED_CATEGORICALLY`. B3's absent recording posture leaves an executor
choosing, unaided, between an uncertainty value and a categorical one across all 680. These are not facts
awaiting discovery; they are choices awaiting a decision.

The circularity is the finding that forced this filing. `XASSET-0032` states plainly that `G5` and `G9`
path 1 "cannot be closed by governance at all". If §G.B step 1 required their closure, §G.B would be
unreachable — and the program would terminate not on evidence but on a reading of one word. The word is
"**required**", and `XASSET-0030` chose it: not "all", but "all **required**". §C gives it the only
content that leaves both §G.A and §G.B operative — semantic rules are required, satisfaction findings are
not.

That reading is disciplined rather than convenient, and §E is the proof: it *increases* what must be
closed before §G.B, by naming B3 — a blocker no prior filing had isolated, reaching three gates and all
680 constructions. A filing seeking to accelerate would have found two blockers and stopped.

`XASSET-0032`'s outright rejection of "let a Stage-1 executor decide at run time" is preserved exactly.
Nothing here permits an executor to decide what a gate *means*. What §D permits is an executor applying
an already-fixed rule to an already-frozen object — which is not run-time semantics, it is the analytical
act the validator itself describes as the design: "Deciding a gate outcome remains a human/analytical act
performed under the charter."

## Alternatives Considered

**Answer A — `SEMANTICALLY_RESOLVED_FOR_EXECUTION`.** Rejected. It would have unlocked §G.B, and every
§D item genuinely supports it — but B1, B2, and B3 are real, and B2 and B3 are each capable of flipping
hundreds of candidate dispositions between an uncertainty outcome and a categorical one. Choosing A would
have required either not looking for B3 or declaring it immaterial, and §H.5 of `XASSET-0032` already
forecloses the "disposition-inert today" defence.

**Answer B — `PREEXECUTION_CLOSURE_REQUIRED` for all six.** Rejected. `XASSET-0027` §M.3 and §M.4
expressly reserve `G3` and `G5` to per-candidate study findings; `XASSET-0026` §H dispositions `G9` path
1 as source-dependent; `G8` and `G10` blocker 1 need a snapshot successor no accepted authority permits
this program to create. B would make §G.B unreachable in principle — the circularity the objective asked
to be tested for, confirmed rather than assumed.

**Close B3 here by assembling accepted authority.** Seriously considered, and the closest call in this
filing: the assembly is short, and `XASSET-0031` §C is direct precedent for assembling accepted authority
without adding a rule. Rejected on scope. This session's authorized question is a sequencing
determination; a recording-posture rule binds every gate result in an irreversible 680-construction run
and deserves its own independent review anchored to its own head, not a subsection of a filing chartered
to decide something else. Recorded at §G as the smallest and highest-leverage corrective.

**Fold B3 into B1 as one "modal/recording" question.** Rejected: `XASSET-0033` §I already discloses that
a program-wide gate-modal rule would reach **every** gate including the six recorded closable, and
records that reach as a caution. B3 is narrower — reserved-satisfiability gates only — and conflating
them would import that caution needlessly.

**Treat B2 as satisfaction because it concerns 360 specific constructions.** Rejected: `XASSET-0024`
§H.4's consumption test is a reading of accepted authority against a frozen population, decidable today
from committed text with no source and no snapshot. Its object being enumerable does not make it a fact
awaiting discovery.

**Amend `XASSET-0030` §G.A or §G.B in place.** Rejected: both are accepted, this repository records
corrections forward rather than rewriting accepted history, and no amendment is needed — §C interprets
"required", which §G.B step 1 already says.

**File nothing and let `XASSET-0030` §G.B step 1 be read literally.** Rejected: on the literal reading
§G.B is unreachable, which would end the program on a construction rather than on evidence — and would do
so without anyone having stated that conclusion or tested it.

## Consequences

`XASSET-0030` §G.A is now **partitioned rather than pending**. Five of its six items are determined not
to be §G.B entry conditions, and the sixth — `G12` — is one of three named residual blockers. Every gate
remains exactly as `XASSET-0030` §E, `XASSET-0031` §I, `XASSET-0032` §A, and `XASSET-0033` left it.

The practical result is that the remaining path is short and fully specified. Three governance questions
stand between the program and §G.B: a `G12` tense statement, a §H.4 consumption determination, and a
recording-posture rule for reserved-satisfiability gates. **All three are decidable from committed text.
None requires a candidate source, a snapshot successor, market data, or protected RISK access.** No
successor now needs to rediscover which §G.A items can be closed by reading, which cannot be closed at
all, and which were never entry conditions.

The countervailing result is that this filing **raised** the bar it was asked to test. B3 is new, reaches
three gates and all 680 constructions, and would have propagated silently into `XASSET-0030` §G.B step 3's
enforcement layer and step 4's runner had it not been isolated before either was built. That is the case
for having asked the sequencing question before the implementation pass rather than during it.

Stage 1 stays unarmed, `ATTEMPT_1` stays intact, and the program remains where four consecutive negatives
have placed it: cheaper to keep asking than to run once, irreversibly, on semantics nobody fixed.
