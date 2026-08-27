---
decision_id: XASSET-0059
date: 2026-08-27
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, XASSET-0055, XASSET-0056, XASSET-0057, XASSET-0058, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_formal_disposition_parser_correction_implementation.py
---

## Context

`XASSET-0058` is **EFFECTIVE**. Its Lifecycle A closed in full — independent FULL review
`5034171910`, a bounded fast-forward correction, an exact-head DELTA review `5035960873` at
`e8d53c18…` with **0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**, principal exact-head acceptance
`issuecomment-5432460504`, normal merge `34c45900…`, post-merge verification
`issuecomment-5432479068`, merge-commit CI run `33024792395` / job `98363500732` (both `head_sha`
equal to the exact merge SHA, attempt 1, `completed`/`success`, **14 362 passed**), and final
closure `issuecomment-5432562310` — strictly in that order.

`XASSET-0058` §F authorizes **exactly one** future, separate, bounded implementation unit to build
the recognition boundary it decided. **This is that unit.** It is `XASSET-0058` §G.5 step **B1**.

### Live preflight

Every anchor was independently re-derived from live git and live GitHub before anything was edited.
Nothing was taken on the authorizing task's word.

| Fact | Verified |
|---|---|
| Base | `34c45900ce23742d04d80cf12471c34aabe9682d` — GitHub `main`, `origin/main`, the local checkout and this branch all equal it |
| Merge shape | normal merge, exactly two **ordered** parents `556a43cf…` then `e8d53c18…` |
| Zero drift at merge | merge tree `76e1021499464f4c2152d9e55c0d03b5ea14708c` is **byte-identical** to the accepted head's own tree |
| PR #359 | **merged**, `state: closed`, `merged_by: Mast3rkey` |
| Open pull requests | **zero** |
| `LOAD_BEARING_RELPATHS` | **18**, membership unchanged |
| Module identity at the base | `12eab05e…604a5` — `XASSET-0057` §F.3 **role 2**, the permanent negative pin |
| Stage 1 | `lane state: ABSENT`, `new execution authorized: False`, `AUTHORIZATION_ROOT` absent, `ATTEMPT_1` intact/unclaimed/unconsumed, no results artifact |

**The A3 comment's own "A4" label is a mis-numbering, not a lifecycle gap**: the retained A5
verification and A7 closure records both name it as the principal exact-head acceptance, and the
chronology is strict. `XASSET-0058`'s `status: Proposed` frontmatter follows this repository's
two-step acceptance-recording convention and does not negate §I effectivity; no status-recording
pull request is opened by this unit.

## Decision

### A. Determination — `FORMAL_DISPOSITION_PARSER_CORRECTION_IMPLEMENTED`

`parse_formal_disposition()` now implements `XASSET-0058` §D exactly. The defect family
`XASSET-0057` §F.0 reproduced is **closed**, the residual §D.8 expressly reserved is **preserved**,
and acceptance is **unchanged**.

### B. Reproduction, before anything was edited

`XASSET-0058` §F.0.1's own discipline: the defect was reproduced against the **unchanged merged
bytes** through the real parser and **all three real consumer seams**, including native-`APPROVED`
rescue, before a single production character was changed.

| Adverse first line (followed by a canonical approval) | parser | seam 1 | seam 2 | seam 3 | seam 3 native `APPROVED` |
|---|---|---|---|---|---|
| `FORM:L DISPOSITION: CHANGES REQUIRED` | **APPROVED …** | reached finality | not refused | not refused | not refused |
| `FORM:AL DISPOSITION: CHANGES REQUIRED` | **APPROVED …** | reached finality | not refused | not refused | not refused |
| *(control)* `FORMAL DISPOSITION: CHANGES REQUIRED` | `CHANGES REQUIRED` | stopped | refused | refused | refused |

The complete printable-ASCII family matrix was re-derived rather than copied — **3 264 cells per
presentation, 9 792 across the three governed presentations, 9 450 open** (`BYPASS`), **34 colon
cells with 33 open in every presentation**.

### C. The production change — the smallest complete one authorized

The only production surface touched is `parse_formal_disposition()` in
`level1_stage1_execution_authorization.py`, plus **one** narrowly devoted candidate-recognition
helper and the **three** constants it derives:

* `_is_formal_disposition_candidate(ascii_upper_line, start, end) -> bool`
* `_FORMAL_DISPOSITION_LABEL` — derived from `FORMAL_DISPOSITION_PREFIX`
* `_FORMAL_DISPOSITION_EDIT_BUDGET` — `1`, a `NUM-0001` **class 5 provisional governance guardrail**
* `_ADMISSIBLE_COLON_INDICES` — derived from the label length and the budget, **never literals**

**The helper was justified, not assumed** (§F.2 permits at most one, and only on proof it is
smaller and clearer than inline logic). Inline, the rule would add roughly thirty-five lines two
levels deep inside an already two-hundred-line loop body that four separate reviews have already
found difficult to reason about; as a helper the call site is **one line**, the rule is
independently testable, and its no-verdict property becomes provable from the syntax tree. The
ceiling of one is therefore exactly spent, and a second helper now fails a test.

**Where it runs.** Only on the branch the parser takes when the canonical prefix is **absent from
the ASCII-folded line**. An accepted form always contains that prefix, so it can never reach the
rule — acceptance is untouched **structurally**, not by promise.

**What it does.** For each of the two governed projections, it probes the three admissible colon
indices **directly**, requires a real ASCII colon there, and compares the label before it with the
canonical label under a restricted Damerau / optimal-string-alignment distance capped at one edit.
A qualifying non-exact candidate returns **`MALFORMED`**. It can return nothing else: every
`return` in it is a boolean literal.

**What it is not.** No general Markdown framework, no general Unicode framework, no normalization
table, no confusable map, no third wrapper form, no fourth call site of the parser, and no fuzzy
comparison anywhere in acceptance or verdict determination.

#### C.1 Bounded correction — MAJOR 1 of independent review `5037196415`

Independent FULL exact-head review `5037196415` returned **BOUNDED CORRECTION REQUIRED — 0
BLOCKING / 1 MAJOR / 0 MINOR / 0 NOTE** against head `ebec2f1626e59db587903bcb684fbe4fd600a922`,
and the finding was correct. `XASSET-0058` §D.2 item 3 bounds the rule at three index probes and
three capped comparisons per projection, *"so the rule remains **O(1) in the line's length**"*.
The first implementation **derived its own projection bounds**, scanning every leading ASCII space
and every trailing ASCII space or tab before probing. The rule was therefore linear, and the
docstring's O(1) claim was false. Reproduced here before anything was changed, ten calls each:

| shape | ten calls | vs. the short control |
| --- | ---: | ---: |
| short candidate | 0.000029 s | 1x |
| 2,000,000 leading ASCII spaces | 0.895893 s | **30,442x** |
| 2,000,000 trailing ASCII spaces | 0.829430 s | **28,183x** |
| 2,000,000 trailing ASCII tabs | 0.797732 s | **27,106x** |
| bold, 2,000,000 trailing spaces | 0.806718 s | **27,411x** |
| bold, 2,000,000 leading spaces | 0.867799 s | **29,487x** |

The escaped guard, `test_it_is_flat_in_the_line_length`, lengthened only a **non-space** verdict
suffix — measured here at **1.7x** — on which neither trimming loop iterates. It proved the
*comparison* bounded, never the *rule*.

**No governing conflict exists, and none is claimed.** §D.2 item 1 defines the projections in
terms of §D.1's own `revealed`, and the parser must already derive exactly those bounds for
**acceptance**. Deriving them once, in the per-line prologue, and passing them satisfies item 3
literally: three probes and three capped comparisons, and no scan of the rule's own. The
correction is therefore the one the review itself preferred — *"reusing/precomputing the parser's
already-derived line bounds without an additional unbounded candidate scan"* — and needs no new
authority.

**The correction, in three parts.**

1. `end` — §D.1's trailing bound — is **relocated unchanged** from the accepted-form section into
   the unconditional per-line prologue beside `indent`, which was already computed there for every
   line. Both consumers now read one derivation. The loop's text, its `end > indent` floor and its
   ASCII-space-and-tab-only semantics are byte-identical to the ones it replaces.
2. The rule takes `start` and `end` as **required** parameters and derives neither. No optional
   fallback survives, because a self-deriving path would leave the linear scan in the module.
3. Both projections are carried as `(base, limit)` **offsets** instead of materialized substrings.
   `revealed` is `(start, end)`; the `**` wrapper's enclosed text is `(start + 2, end - 2)`. The
   wrapper test reads exactly four characters; `k < len(P)` becomes the integer test
   `at >= limit`; and `label` is `ascii_upper_line[base:at]`, whose length is exactly `index` and
   so at most `max(_ADMISSIBLE_COLON_INDICES)` characters.

**Projection semantics are unchanged, not relaxed.** `indent` counts leading ASCII spaces only and
`end` trims trailing ASCII spaces and tabs only — character for character what the deleted loops
did. The ASCII fold is length-preserving and the identity outside `a`–`z`, so bounds derived from
the raw line index the folded one exactly. Equivalence was verified over the entire matrix, every
presentation, every seam and both native states: **no cell changed classification**.

**Measured after the correction**, same shapes, same method: **1.02x, 0.82x, 0.67x, 0.78x, 1.16x**
— flat. End to end the parser still costs about 0.34 s on a 2,000,000-character line, because
folding it, building `resembles_prefix` and testing the prefix substring are each Θ(n) and always
were; that cost is the parser's, is unchanged by this correction, and is not what §D.2 bounds.

**The evidence was strengthened, never relabelled.** The escaped guard was **kept** — corrected so
folding sits outside the measurement — and demoted in writing to *supporting evidence*. The proof
is now deterministic instrumentation: a `str` subclass records every character the rule reads, and
the count is asserted **identical** across all eight padding shapes and bounded by a ceiling
**derived** from `_ADMISSIBLE_COLON_INDICES` rather than written down. Two structural guards forbid
the rule from measuring the line at all and pin its single remaining loop to the label; a negative
control proves the `False` path bounded too; parser-level and all-three-seam controls prove padding
changes no outcome; and two new mutation probes — `P26`, which materializes `revealed` for the
wrapper test, and `P27`, which takes the label through an unbounded slice — reintroduce the defect.
Both are deliberately **behaviour-preserving and bound-violating**: every verdict, matrix cell and
seam stays exactly as it is, so only the boundedness guards can catch them. That is precisely the
regression class that escaped, and a probe that also changed an outcome would not test it.

**`P26` then found a second axis this correction had itself missed, and it was fixed rather than
argued away.** On its first run `P26` was reported **MISSED — wrong reason**: it failed the suite,
but only through the harness's own anchor check, never through `TestTheRuleIsBounded`. The cause is
a real distinction the review's own shapes do not separate. Padding sits **outside** `[start, end)`,
so a padded line cannot detect a rule that materializes or scans the region **between** the bounds
— exactly what `revealed` is. The shape set was therefore extended with a second axis: a candidate
carrying a 2,000,000-character **verdict**, plain and bold, and one line long on both axes at once.
`P26` and `P27` are now caught by `TestTheRuleIsBounded` itself, and the work-identity assertion
compares each shape against an explicitly named control of its own presentation rather than one
inferred from its label. The first shape set was insufficient; the finding is recorded here because
it was measured, and because it is the same failure mode — a guard that looks conclusive while
exercising the wrong input — that produced MAJOR 1 in the first place.

**One residue was found and removed, not overlooked.** An earlier mutation run was stopped part-way
so it could be restarted against the final probe set. Because the harness's targets were already
modified by this correction, the interrupted probe's replacement text (`P20`) survived *inside*
those modifications, invisible to `git status`. The anchor check caught it, every probe's
replacement text was then scanned across the worktree, the single residue was restored to its
committed original, and the proof was re-run from clean. No probe was counted while it was present.

#### C.2 Second bounded correction — MAJOR 1 of DELTA review `5041611657`

The bounded correction in §C.1 was **not sufficient**, and the DELTA review's finding is correct.
§C.1 made the helper constant-time by taking `start`/`end` as parameters, relocated the unbounded
trailing-space/tab loop into the parser's unconditional prologue, and called it pre-existing §D.1
work. **It was not pre-existing work on the branch that matters.** At the reviewed predecessor
`ebec2f16…`, a prefix-absent line called the candidate rule and `continue`d *before* the
accepted-form `end` derivation. Proved twice, before editing:

* **statically** — the helper call (L1881) and its `continue` (L1883) both precede
  `end = len(line)` (L1906);
* **at runtime** — traced through the predecessor module, L1881 executes and **L1906 does not**.

So the relocation moved a scan across a function boundary rather than removing it from the
pipeline §D.2 defines from raw `L`. Measured on the rejected head `0082fae…`, through the
**complete** `parse_formal_disposition` — not the helper — three calls each:

| shape | three calls | vs. the short control |
| --- | ---: | ---: |
| short control | 0.000040 s | 1x |
| 2,000,000 leading ASCII spaces | 0.958144 s | **23,943x** |
| 2,000,000 trailing ASCII spaces | 0.844379 s | **21,100x** |
| 2,000,000 trailing ASCII tabs | 0.654908 s | **16,365x** |
| bold, 2,000,000 trailing spaces | 0.853352 s | **21,324x** |
| 2,000,000-character verdict | 0.597983 s | **14,943x** |

And the evidence excluded exactly the disputed work: `_work` derived the bounds **on the counted
object** and then zeroed both counters.

**A lawful code-only correction exists, and no new authority is taken.** The test is whether the
bound can be produced by a traversal that happens anyway. It can. `parse_formal_disposition`
already folds **every character of every line** to decide the canonical prefix — required by
`XASSET-0053`'s own BLOCKING 1, present unchanged in the base module at `34c45900…`, and performed
whether or not candidate recognition exists. The trailing bound now rides that fold: a running
count of the current trailing run of ASCII spaces and tabs, reset by any other character, read off
in O(1) as `max(len(line) - trailing_ws, indent)`. The separate backwards scan is **deleted**, not
moved.

**Measured by traversals, which is what a relocation cannot change:**

| module | constructs traversing `line` in `parse_formal_disposition` |
| --- | ---: |
| base `34c45900…` (no candidate rule at all) | **5** |
| rejected head `0082fae…` | **5** |
| corrected | **4** |

Candidate recognition adds **no** traversal the parser did not already make, and the corrected
parser makes **one fewer** than the base that predates candidate recognition entirely.

**Semantics preserved exactly.** `max(…, indent)` restores the floor the deleted loop's
`end > indent` guard provided; equivalence was proved against the old formulation on every padded
shape and on empty, all-space, all-tab and mixed edge cases, and classification was compared
head-to-head with the rejected module across every shape and both tails: **identical everywhere**.
Through the complete pipeline the corrected parser now costs **0.95x–1.34x** the base parser that
has no candidate rule — a constant factor, not a pass.

**The evidence now measures the complete pipeline.** `_work` no longer resets anything: bounds are
derived from a **separate plain copy**, and the counted object is created afterwards and touched by
nothing but the rule, so its count is the rule's own work from zero. `TestTheRuleIsBounded` is
honestly rescoped in writing to the rule's conditional property, and a new class,
`TestTheCompletePipelineIsBounded`, calls `parse_formal_disposition` itself: a non-vacuity guard
proving the scan detector fires against the **actual rejected source read from git**; the
predecessor-ordering fact that §C.1 got wrong, pinned; no separate trailing-scan construct
surviving; no traversal added beyond the base parser's; the bound provably produced *inside* the
fold and read off in O(1); a runtime trace over every padded shape showing **no trailing scan
executes**; and strictly fewer traversing constructs executing than at the rejected head.

**The new evidence discriminates.** Run against the rejected head `0082fae…`, **13 of its 16 tests
fail**; against the correction, all 16 pass. A new probe, `P28`, restores the exact separate scan —
behaviour-preserving and pipeline-violating, so only these guards can catch it — and is caught for
its intended reason.

**One defect in this round's own evidence, caught by its own guard.** The first version of the
scan detector compared against the wrong escaping of the whitespace literal and silently matched
**nothing**. The non-vacuity guard — which exists precisely to refuse a detector that cannot see
the defect it forbids — failed immediately. The predicate was reshaped around the structure (a
construct indexing the line at a position derived from the trailing bound) rather than one
spelling of it.

### D. Result — the whole matrix, closed

| Family (plain presentation) | Cells | live `BYPASS` | corrected `BYPASS` | corrected `MALFORMED` | corrected `ADVERSE` |
|---|---|---|---|---|---|
| Single-character **deletion** | 17 | 17 | **0** | 17 | 0 |
| ASCII **substitution** (all 95) | 1 598 | 1 581 | **0** | 1 581 | 17 |
| ASCII **insertion** (all 95) | 1 615 | 1 518 | **0** | 1 614 | 1 |
| **Adjacent transposition** | 17 | 17 | **0** | 17 | 0 |
| **Unicode / confusable substitution** | 17 | 17 | **0** | 17 | 0 |
| **TOTAL** | **3 264** | **3 150** | **0** | **3 246** | **18** |

Bold and three-space-indented presentations: **3 264** cells each, **3 150** live `BYPASS`, **0**
corrected `BYPASS`, **3 247** corrected `MALFORMED`, **17** corrected `ADVERSE`. Across the three:
**9 792** cells, **9 450** open before, **0** open after. The **34 colon cells** are **0** open in
every presentation.

**The safety property, stated as the property rather than as a count:** no cell of the exhaustive
matrix, in any governed presentation, lets a later approval win.

### E. The §D.8 residual is preserved exactly

Mutation of the **terminating colon itself** carries no ASCII colon at any admissible index, so it
yields no candidate and remains **ABSENT** — unchanged behaviour, not a new hole, and expressly
outside this unit's grant. This is proved directly rather than assumed, and the two cases are kept
distinguished by the mechanism that separates them:

| | **Internal** colon — CLOSED here | **Terminating** colon — remains ABSENT |
|---|---|---|
| Example | `FORM:L DISPOSITION: CHANGES REQUIRED` | `FORMAL DISPOSITION CHANGES REQUIRED` |
| ASCII colon at an admissible index? | **Yes** | **No** |
| Disposition | **MALFORMED** | **ABSENT**, unchanged |

### F. Everything else that must not have moved, and did not

* **Acceptance** — ten control classes, each returning **exactly** what it returned before,
  including both governed wrapper forms, ASCII upper/lower/mixed case, a validated finding-count
  suffix, and a lower-case verdict returned verbatim.
* **The open verdict vocabulary** and **whole-verdict exact equality** — a never-before-seen verdict
  still returns verbatim; appended text still cannot authenticate.
* **Ordinary prose** — twelve ABSENT control shapes, including headings, blockquotes, bullets,
  malformed emphasis, code fences and prefix-bearing marker lines. **Zero** regressions across
  **410** tracked Markdown files / **131 902** lines and **2 167** tracked text files /
  **375 907** lines; the corpus flags **8** lines, partitioned **2** already `MALFORMED` and **6**
  already verdict-yielding, with an **empty** regression bucket.
* **Real historical lifecycle review bodies** — twelve real first-formal lines from PRs #357, #358
  and #359, exercising three distinct open-vocabulary verdicts, all retained exactly; plus a real
  bot body carrying no formal line, still ABSENT.
* **Seam 3's genuinely-ABSENT policy** — preserved exactly as `XASSET-0053` §D.20.1 left it.

### G. Every attack is refused at all three real consumer seams

Seam 3 over the **whole** matrix in **both** native states; seams 1 and 2 over a **declared,
derived** safety-critical subset whose composition is itself asserted — it contains **every** colon
cell and **every** family-by-position representative. Seam 2's real implementation invokes many
`git` subprocesses per call (measured at ~100 ms), which is why §E.5 mandates a subset there rather
than the whole matrix. Native `APPROVED` rescues nothing at any seam, and known-good controls on
both sides prevent a broken refusal detector from making any of it look green.

### H. Identity — derived, never predicted

`XASSET-0057` §F.3 makes the parser-corrected module **role 3**: *derived at the correction's own
merge, **never predicted here**, and **never bound directly*** — it reaches the register only
through role 4's own derivation and proof. `XASSET-0058` §G.4 says the same.

**No live module digest is recorded anywhere by this unit** — not in this decision, not in
`governance/decisions.yaml`, not in `operations/WORKSTREAMS.yaml`, not in any suite. That is
enforced mechanically, not promised. The vulnerable `12eab05e…604a5` stays a **permanent negative
pin**: it is neither rebound, re-pinned nor repaired, and `LOAD_BEARING_RELPATHS` is unchanged at
**18** in both count and membership.

### I. Coupled suites — re-anchored, never weakened

Eight predecessor suites carried claims written while their own generation was the live one. Each
is re-anchored to the **immutable range it was really about**, and the live delta is pinned
**exactly**, by name:

* *"the correction added no module-level name"* → proved over the immutable range **and** the live
  delta pinned to exactly the four authorized names, so a **fifth** now fails where the superseded
  form could not distinguish it from the first.
* *"this filing changes no production byte"* → proved over that filing's own base-to-merge range;
  measured against a moving `HEAD` it had silently become a claim that no later unit may change one
  either, which would forbid the very correction §F authorizes.
* *"the register records the live module identity"* → **inverted**, because a later accepted
  decision withdrew it: recording that digest now would violate §F.3. The successor rule is
  asserted instead, and it is strictly harder to satisfy — the superseded form passed on any
  occurrence anywhere; this one fails if the value appears at all.
* Defect **reproductions** → re-pointed at the uncorrected base bytes, loaded in memory from the
  git blob, with the **corrected** refusal asserted alongside each. A reproduction that silently
  re-measured the corrected parser would report zero hits and turn its own family counts into
  claims about nothing.

Nothing was deleted, skipped, `xfail`ed or relaxed: every touched suite's `skip`/`xfail` count is
unchanged and its assertion count is greater than or equal to its count at this unit's base, both
enforced by a test.

### J. Authority withheld — absolute

This unit performs **no** step-8-equivalent rebinding, **no** re-pinning, **no** readiness or drift
verification, **no** attestation, **no** arming, **no** lane creation, **no** `ATTEMPT_1` claim,
**no** execution, **no** results generation, **no** allocation, **no** percentage calculation,
**no** trading, and **no** protected `RISK` access. It amends neither `PROTOCOL_V1.md` nor
`pre_registration.yaml`, and closes neither the §D.8 residual nor any boundary past §D.

`stage_1_executability.executable` is `false`, every authorization predicate is `false`,
`AUTHORIZATION_ROOT` is **absent**, the `ATTEMPT_1` lane is **`ABSENT`**, and **Stage 1 remains
UNARMED and NOT EXECUTABLE.**

### K. Lifecycle B, and this unit's place in it

`XASSET-0058` §G.5: **B1** the implementation itself *(this filing)*; **B2** independent **FULL**
exact-head review under `OPS-0007` §1; **B3** any bounded correction and exact-head re-review;
**B4** explicit principal exact-head acceptance; **B5** normal merge; **B6** immediate post-merge
verification; **B7** successful merge-commit CI whose `head_sha` is that exact merge SHA; **B8**
final post-CI verification and lifecycle closure.

**Only B1 is performed here.** This pull request is **draft, open and unmerged**; it is **not**
self-reviewed, **not** principal-accepted, **not** marked ready and **not** merged. Merged is not
effective, and no single step of either lifecycle is individually sufficient.

## Rationale

The defect was fail-closed in name only: a one-character mutation of the label made an adverse
first line **invisible**, so it was skipped as ABSENT and a later, better-formed approval won past
it — the exact `XASSET-0053` §D.17 failure. `XASSET-0058` decided the narrowest rule that closes it
without touching acceptance, and the narrowest correct implementation of that rule is one bounded
classification check on the one branch where the line is already known not to be accepted.

Probing the admissible colon indices **directly** — rather than searching for the first colon — is
what makes the rule robust to an attacker supplying a colon of their own, and it is why the
superseded formulation left 33 of 34 colon cells open.

## Alternatives considered

**Inline the rule instead of adding a helper.** Rejected on the measurement §F.2 requires: the call
site becomes one line instead of thirty-five nested two levels deep, and the no-verdict property
becomes structurally provable rather than argued.

**Close the §D.8 terminating-colon residual too.** Rejected: expressly outside this grant, and
`XASSET-0058` §D.7 measured that the rule which would close it produces a genuine prose regression.

**Record the corrected module identity in the register, as earlier parser units did.** Rejected —
it is forbidden. `XASSET-0057` §F.3 makes it role 3, derived at merge and never predicted.

## Consequences

The defect family is closed at the parser and at all three consumer seams. `XASSET-0057` §F.0's
conjunctive parser-correction prerequisite becomes satisfiable — but is **not** satisfied by this
filing alone: it requires Lifecycle B to close **in full**, and the B5 merge is then the **sole**
qualifying base for the later step-8-equivalent rebinding, which remains `XASSET-0057`'s own
reserved successor unit and is unauthorized here.

**This pull request is PR #360.** It was opened carrying an impossible sentinel, and the real
number GitHub issued was read back live from the API — never guessed — and bound in one
fast-forward follow-up commit. Not merged, not independently reviewed, not principal-accepted
in this session.
