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
| `origin/main` = local `HEAD` | `3cc15d58a42e6d56fbe702ccf4f377b60fbb8b0c` |
| Working tree / stash | clean / empty |
| Open PRs | zero |
| Competing mutation worktrees / pushed branches | none — the prior Stage-1 session's branch is absent from `origin` |
| PR #328 | merged / closed |
| Accepted head | `49609c3ff9befe1ba8d0b296da421337b5a425a0` |
| Merge parents | `c51e94609eff7ede2bdfa084844d59b8347561e5`, `49609c3ff9befe1ba8d0b296da421337b5a425a0` |
| Final review `4946790220` | `APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE`, `commit_id` = accepted head |
| Principal acceptance `5308731970` | present, exact head |
| Post-merge verification `5308740682` · closure `5308784921` | present |
| Merge-commit CI run `31962008857` / job `95201259559` | `completed` / `success`, `head_sha` = merge SHA |
| `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` |
| `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` |
| Construction universe | regenerated live: **680** constructions, **48** cells, `73c0965e…5224` |
| `stage_1_executability.executable` | `false` |
| Lane directory / attestation / claim / completion / ledger / `stage1_results.yaml` | **all absent** |
| `new_execution_is_authorized()` | `False` — "no attestation present… There is no merge-to-execution gap" |
| `XASSET-0030` | unused — zero matches repository-wide |

**`ATTEMPT_1` is intact, unclaimed, and unconsumed, and remains so after this filing.**

### The question this unit had to answer

A halted pre-arm review found that everything *downstream* of the twelve gate results is fully
deterministic — `map_g2_reading`, `required_g2_gate_result`, `derive_candidate_disposition`,
`derive_cell_outcome`, and `derive_roll_up_outcome` are closed, order-independent compositions — while
nothing in accepted authority produces the gate results themselves. Because `ATTEMPT_1` is one-shot and
`execution.rerun_rule.after_outcomes_observed` is `PROHIBITED`, that gap cannot be closed ad hoc during
execution.

The question is therefore: **can the per-construction gate-evaluation method be made sufficiently
deterministic that two independent conforming executors, given the same frozen construction and the
same accepted authority, must produce the same twelve gate results and §K.1 per-reading fields without
inventing economic judgment — and if so, what is the smallest lawful method?**

## Decision

### A. Determination — `GATE_EVALUATION_METHOD_NOT_CLOSABLE`

**The answer is NEGATIVE.** A complete deterministic per-construction gate-evaluation method **cannot
lawfully be closed by this unit**. Seven of the twelve gates are closable now and are recorded below so
a successor need not re-derive them. Five are not, for two independent reasons, and one of those reasons
is worse than an open question: it is an open question that implementation currently forecloses in one
direction.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** This filing changes no canonical byte, no universe, no
hash pin, and no authorization state.

### B. What this unit reproduced before designing anything

All four reproductions used the real modules and isolated synthetic fixtures. No results document, lane
state, or Stage-1 output was created.

**B.1 — The §K.1 map consumes readings; it does not produce them.**
`required_g2_gate_result("PASSES", "FAILS")` returns `UNABLE_TO_DETERMINE` deterministically, and
`is_reading_dependent` returns `True`. Both take the two reading outcomes as *inputs*. Nothing in the
closed table, the protocol, or the preregistration yields those two outcomes for a given construction.

**B.2 — The frozen universe carries no gate outcomes.** Each of the 680 entries carries exactly ten
identity fields — `cell_id`, `sleeve`, `bound`, `driver_class`, `family_id`, `route`, `num_0001_class`,
`governing_authority_refs`, `source_architecture`, `hypothetical_source_requirements`. There is no gate
outcome anywhere in the universe, in either canonical file, or in any module.

**B.3 — `G3` admits three defensible answers with different dispositions.** For a fixed frozen
construction, `G3 = PASS` derives `UNABLE_TO_DETERMINE` and `G3 = FAIL` derives `BLOCKED_CATEGORICALLY`.
Nothing selects between them.

**B.4 — and the *severe* finding: while `G2` is reading-dependent, every categorical failure is
unrepresentable.** Holding the reading pair at `(PASSES, FAILS)`, a `FAIL` on **any** of the nine other
categorical gates derives `BLOCKED_CATEGORICALLY`, and
`_validate_stage1_results_against_universe` then **rejects the document**:

```
G1_DRIVER_SUBJECT_MATTER      -> BLOCKED_CATEGORICALLY  valid=False
G3_NORMALIZATION              -> BLOCKED_CATEGORICALLY  valid=False
G4_ORIGIN                     -> BLOCKED_CATEGORICALLY  valid=False
G5_CONSTRAINT_SHAPE           -> BLOCKED_CATEGORICALLY  valid=False
G6_ROUTE_COMPLIANCE           -> BLOCKED_CATEGORICALLY  valid=False
G7_DISCRETION_AND_PROVENANCE  -> BLOCKED_CATEGORICALLY  valid=False
G8_UNIQUENESS                 -> BLOCKED_CATEGORICALLY  valid=False
G10_PAIR_INDEPENDENCE         -> BLOCKED_CATEGORICALLY  valid=False
G11_EXACTNESS_AND_DETERMINISM -> BLOCKED_CATEGORICALLY  valid=False
```

### C. Finding 1 — a canonical/enforcement contradiction, not merely a gap

Both canonical files state the **opposite** of what the validator enforces.

`pre_registration.yaml` → `g2_reading_mapping.reading_dependent_end_to_end_note`, and `PROTOCOL_V1.md`
§7.1, both say verbatim:

> "a reading-dependent candidate necessarily records `G2 = UNABLE_TO_DETERMINE` and therefore
> necessarily disposes to `UNABLE_TO_DETERMINE`, **unless some categorical gate independently fails** —
> including when a prerequisite gate also fails."

`level1_endpoint_evidence_preregistration_validator.py` lines 2505–2509 say:

> "a reading-dependent `G2` outcome may not be recorded as `BLOCKED_CATEGORICALLY` while `XASSET-0024`
> §K.1 remains unresolved"

These are irreconcilable. The canonical text expressly contemplates the categorical outcome the
validator prohibits outright.

**Why this is load-bearing rather than cosmetic.** `XASSET-0024` §D determines the subject-matter
reading and §K.1 records the contrary reading, so the reading pair is `(PASSES, FAILS)` — and therefore
reading-dependent — for every one of the 680 constructions. The entire categorical branch of the
disposition vocabulary is consequently **unreachable**, which in turn makes unreachable:

- `XASSET-0027` §J.2's stated design outcome — a class that supports direction but not magnitude
  "fails at one of those two and is **recorded honestly**";
- `XASSET-0027` §I.2's cell rule — a cell is `BLOCKED_CATEGORICALLY` "only if every registered
  construction for that cell was evaluated and every one was blocked categorically";
- `derive_cell_outcome`'s own `ALL_CANDIDATES_BLOCKED_CATEGORICALLY` branch; and
- `derive_roll_up_outcome`'s `NO_CONSTRUCTIBLE_CANDIDATE` outcome.

**This is worse than an open question.** An executor who resolved `G3` *toward* categorical failure —
the direction `XASSET-0027` §J.1 most plainly points — would find the result unpublishable and could
reasonably infer that `PASS` or `UNABLE_TO_DETERMINE` is therefore the intended answer. That would let
**implementation decide a governance question**, silently, in one direction. Which artifact governs must
be settled by governance, not by which one an executor happened to run.

### D. Finding 2 — `G3`'s share-of-the-whole question is reserved and unanswered

`XASSET-0024` §C fixes the endpoint denominator as "one exact normalized unit of prospective, unlevered,
asset-side capital." Each frozen specification's `R2` requires the source to establish a bound on
**that** quantity. `G3` asks whether that is lawfully satisfiable given the source's subject matter must
be class-D evidence (`R3`).

Accepted authority describes the difficulty precisely and then declines to resolve it:

- `XASSET-0027` §J.1: "**Every one** of §E.1's six DRIVER classes is defined on a sleeve or on a
  comparison; the endpoint is a share **of the whole**. Converting sleeve economics into a share of the
  whole requires a mapping, and every mapping anyone would reach for is already barred by name."
- `XASSET-0027` §J.3: `portfolio_function` is the only class whose §E.1 scope language refers to the
  prospective portfolio — and "**Whether that suffices to carry a share-of-the-whole statement is what
  `G3` tests.**"
- `XASSET-0024` §D determines magnitude-*capability* ("none excludes quantitative content") but
  expressly not share-denomination: "**none is 'sleeve share'**."

So §J.1 is diagnostic, §J.3 is an explicit reservation, and §D settles a different question. The
`(PASS / FAIL / UNABLE_TO_DETERMINE)` choice is outcome-determining and unselected.

**Extending the dual-reading treatment to `G3` does not cure it.** Under the preference-only reading
everything collapses (`PROTOCOL` §7), but the *subject-matter* branch is itself undetermined — that is
exactly what §J.3 reserves. A second reading slot would relocate the gap, not close it.

**This unit cannot lawfully answer it.** Doing so would determine the substantive scope of
`XASSET-0020` §E.1's closed classes. §K.1 itself names the smallest corrective for the adjacent
question — "a narrowly scoped clarification of `XASSET-0020` §E.1 alone" — and `XASSET-0027` §Q makes an
§E.1 amendment its own reopen trigger. That is an `XASSET-0020`-level act, not a Stage-1 method unit's.

### E. Gate-by-gate result

Applying the required distinction throughout: **(a)** the specification requires a property; **(b)**
whether that property is lawfully satisfiable; **(c)** whether absence of a not-yet-created artifact is
categorical, prerequisite, or uncertainty. All 680 constructions are
`HYPOTHETICAL_SOURCE_ARCHITECTURE`, so (a) never by itself answers (b).

| Gate | Class | Closable now | Determination or exact blocker |
|---|---|---|---|
| `G1_DRIVER_SUBJECT_MATTER` | categorical | **NO** | Reading-dependent like `G2` — §D's subject-matter reading admits it; §K.1's contrary reading is that "no admitted item could ever be classified DRIVER for the endpoint question." Only `G2` has a dual-reading slot. |
| `G2_MAGNITUDE_INTRINSICALITY` | categorical | **YES** | `subject_matter = PASSES` (§D, operative); `preference_only = FAILS` (§K.1 contrary reading; `PROTOCOL` §7 "both R1 and R2 collapse and no candidate can succeed") → reading-dependent → `UNABLE_TO_DETERMINE`, all 680. §K.1 preserved, not resolved. |
| `G3_NORMALIZATION` | categorical | **NO** | Finding 2. Expressly reserved to "what `G3` tests"; answered nowhere. |
| `G4_ORIGIN` | categorical | **YES** | `R9` bars every §D non-route N1–N8; a source stating a bound directly is not a barred mechanism → `PASS`. |
| `G5_CONSTRAINT_SHAPE` | categorical | **YES** | Specification originates a bound; §E.2 clipping is the CONSTRAINT path, not this one → `PASS`. |
| `G6_ROUTE_COMPLIANCE` | categorical | **YES** | `R6` requires §H.2 items 1–6 in full (R1) or a source-prescribed §H.3 derivation (`R2_C2`, per `XASSET-0028` §E, which composes nothing) → `PASS`. |
| `G7_DISCRETION_AND_PROVENANCE` | categorical | **YES** | `R7` requires the NUM-0001 §4 field set and excludes class 6; class-4 and class-5 conditions are carried per family → `PASS`. |
| `G8_UNIQUENESS` | categorical | **NO** | Asks for exactly one lawful value "across the admitted set." `R6` gives *source-level* uniqueness only. No admitted set exists, and uniqueness over an empty set is undefined — trivially satisfied or unknowable, with no accepted rule selecting. |
| `G9_REPRESENTATION` | prerequisite | **NO** | Path 2 is closable (no Level-1 rule exists — `XASSET-0023` §H.5, `XASSET-0027` §P.2). Path 1 is source-dependent and `R8` expressly "asserts no prior representation rule." Additionally unreconciled: `XASSET-0024` §G path 3 says **mandatory abstention** while the gate's declared failure class is **prerequisite**. |
| `G10_PAIR_INDEPENDENCE` | categorical | **NO** | §H.4 requires the unresolved pair "is not an input to it at all." The 120 `PAIR__` constructions are direct pair evidence by definition. Whether the named `XASSET-0020` §H pair is *unresolved* is a determination made nowhere — and the evidence that would settle it may itself sit behind the `risk_lane_boundary`. |
| `G11_EXACTNESS_AND_DETERMINISM` | categorical | **YES** | Specification requires exact source precision or an exact rational derivation → `PASS`. |
| `G12_SNAPSHOT_ADMISSIBILITY_PATH` | prerequisite | **YES** | A clean case (c): no lawful `XASSET-0021` snapshot successor exists and none is authorized (`XASSET-0027` §P.2). Absence of a not-yet-created artifact whose declared failure class is prerequisite → `FAIL (prerequisite)`, dependency named, all 680. |

**Seven closable; five not.** The five are not curable by defining a word — each requires a
determination reserved elsewhere.

### F. §K.1 is preserved, not resolved

This filing does not adopt either §K.1 reading. It records that `XASSET-0024` §D determines the
subject-matter reading *as the operative one for Outcome A*, that §K.1 preserves the contrary reading
and states its consequence ("both R1 and R2 would collapse"), and that the dual-reading fields are the
mechanism by which the open question is carried rather than decided. It resolves no reading, amends no
§E.1 scope, and asserts no `g2_outcome_under_*` value for any construction in any results document —
none exists.

### G. The exact successor prerequisites

The smallest set that would unblock a Stage-1 lane, in dependency order:

1. **Resolve the Finding 1 contradiction.** Determine, in governance, whether the canonical
   "unless some categorical gate independently fails" or the validator's prohibition governs, and
   conform the other. Until then the categorical branch is unreachable and one direction of every
   categorical gate is decided by implementation.
2. **Resolve or structurally accommodate Finding 2** — whether, and for which of the six §E.1 classes,
   a source whose subject matter is that class may intrinsically state a §C-denominated
   share-of-the-whole bound. §K.1 names the shape: "a narrowly scoped clarification of `XASSET-0020`
   §E.1 alone."
3. **Then, separably and smaller:** give `G1` a lawful reading treatment; define `G8`'s uniqueness over
   an empty admitted set; reconcile `G9`'s abstention-versus-prerequisite mapping; and determine
   `G10`'s unresolved-pair question within the RISK boundary.

Items 1 and 2 are independent and may be filed separately. Neither is authorized here.

### H. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; arms and executes no Stage 1; creates no Stage-1 runner and no `stage1_results.yaml`;
consumes nothing of `ATTEMPT_1`; evaluates no gate for any construction and asserts no per-construction
outcome; acquires no market, fundamental, economic, or Stage-2 data; amends no canonical file and
changes no hash pin, universe, cardinality, or construction identity; resolves `XASSET-0024` §K.1
neither way and amends no `XASSET-0020` §E.1 scope; resolves §J.12, grants Stage 2, and grants
application authority — none of them; invents no Level-1 representation aggregation or selection rule
and designates no CM-14–CM-17 membership; selects no sleeve and creates no endpoint, bound, point,
range, percentage, weight, rank, target, or allocation; reuses no RISK scenario, value, parameter,
window, result, or private artifact; weakens no validator or test; changes no `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin
state; authorizes no chart, ladder, deployment, trade, order, or brokerage action; and rewrites no
accepted history.

## Rationale

The design standard for this unit was not "a competent analyst could answer the gates." It was that two
independent conforming executors, given identical frozen inputs, must not be able to select different
lawful results. Findings 1 and 2 each independently defeat that standard, and Finding 1 defeats it in
the most damaging way available — not by leaving a question open, but by having software foreclose one
lawful answer while both canonical files say that answer is expected.

Closing the seven determinable gates anyway, and shipping a "mostly deterministic" method, was
available and rejected. A method that is deterministic for seven gates and silently discretionary for
five is not partially safe; it is a method whose single irreversible use would bake five unreviewed
judgments into an unrerunnable record. `execution.rerun_rule.defect_handling` already prescribes the
correct response to exactly this situation: *record the defect, halt, and return for separate
governance.*

Recording the seven that *are* closable is nonetheless the substance of this unit's value: a successor
inherits a five-gate problem rather than a twelve-gate one, and inherits it with the exact controlling
text for each already located.

## Alternatives Considered

**Close the method by adopting by-construction inference** — treat "the frozen specification requires
property P" as establishing "the gate testing P passes." Rejected: `XASSET-0028` §F says Stage 1
evaluates whether a frozen specification is **lawfully satisfiable** under the gates, which is question
(b), not question (a). Adopting the inference would make every gate whose property the generator wrote
into `R1–R9` pass by construction, converting the twelve gates into a restatement of the generator.

**Extend dual-reading treatment to `G3`** (and `G1`). Rejected as insufficient rather than wrong: it
would preserve §K.1 correctly, but the subject-matter branch of `G3` is itself what §J.3 reserves, so
the gap relocates instead of closing. It remains a reasonable component of successor item 2.

**Fix the Finding 1 contradiction here**, by either deleting the validator prohibition or amending the
canonical note. Rejected: both directions are substantive and outcome-determining — one re-enables the
entire categorical branch for 680 constructions, the other forecloses it in canon. Choosing requires
determining which artifact governs, which is precisely the successor question. Reporting a contradiction
is this unit's remit; picking a side is not.

**Resolve `G3` on the §J.1 textual reading** — five classes fail categorically, `portfolio_function`
open. Rejected: §J.1 is framed as "where the difficulty actually is," not as a determination, and §J.3
expressly reserves the question. It is also unrecordable today under Finding 1.

**File nothing and re-attempt Stage 1.** Rejected outright: `ATTEMPT_1` is one-shot and
rerun-after-outcomes is prohibited.

## Consequences

Stage 1 stays unarmed, and the prerequisite blocking it is now specific rather than diffuse: two named
determinations, in dependency order, with their controlling text located and their smallest corrective
shape identified by §K.1's own words. Seven gates will not need re-deriving.

The negative outcome is the honest one, and it is also the cheap one — it costs one governance filing,
where the alternative would have spent the single irreversible execution of a 680-construction study on
five undisclosed judgments.
