---
decision_id: XASSET-0058
date: 2026-08-26
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, XASSET-0055, XASSET-0056, XASSET-0057, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_formal_disposition_parser_correction_authorization.py
---

## Context

`XASSET-0057` is **effective**. Its §F.0 makes a separately authorized, independently reviewed,
principal-accepted, merged, exact-merge-CI-green and lifecycle-closed **parser correction** a
mandatory conjunctive prerequisite to any step-8-equivalent rebinding, and it expressly declined to
write, design or authorize that correction:

> **This filing does not decide that recognition boundary.** Fixing it here would be designing the
> correction inside an authorization that expressly withholds it. The boundary is therefore
> **reserved to that future decision, which must decide it and prove it**.

**This is that decision.** It is a **design-only Lane G governance authorization** under `OPS-0009`,
and it is the **Lifecycle A** authorization `XASSET-0057` §F.0.3 requires. It **performs no parser
correction**: it decides the recognition boundary, proves the boundary against real evidence, and
grants authority for **exactly one** future, separate implementation unit (Lifecycle B).

### Live preflight

Every anchor below was independently re-resolved from live git and live GitHub before anything was
edited. Nothing was taken on the authorizing task's word, and no identity is quoted from a brief.

| Fact | Verified |
|---|---|
| Base | `556a43cf91679d3e8ca95703c8d49e672b662b73` — GitHub `main`, `origin/main`, the local checkout and this branch's base all equal it |
| PR #358 | **merged**, `state: closed`, `merged_by: Mast3rkey`, `merged_at 2026-08-26T13:14:53Z` |
| Merge shape | GitHub's **normal merge**: exactly two parents, parent 1 `583022a5f2106d61f82d270edadd3520d8b0c55d`, parent 2 `53d2d3d770f379393a1a3fde4408915c9fcf81f0` — **in that order** |
| Zero drift at merge | merge tree `0c7b738c22c2a0f3bbdfa9cbcea3971a7029307f` is **byte-identical** to the accepted head's own tree; the accepted-head-to-merge diff is **empty** |
| Clean review | `5030740306` @ `53d2d3d…`, by `Mast3rkey`, `OWNER` — approving verdict, **0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE** |
| Principal acceptance | `issuecomment-5425835377` — `2026-08-26T13:13:45Z`, by `Mast3rkey`, `OWNER`, strictly after the review and strictly before the merge |
| Void actor comment | `issuecomment-5425816981` — `claude[bot]`, `author_association: NONE`-class `CONTRIBUTOR`, `13:12:20Z` — **VOID, never acceptance**, recorded so it can never be mistaken for one |
| Post-merge verification | `issuecomment-5425857818` — `2026-08-26T13:15:39Z`, strictly after the merge |
| Merge-commit CI | run `32973075626`, job `98191135804`, `event: push`, `run_attempt: 1`, `completed`/`success`, **both `head_sha` equal to the exact merge SHA**, 10 of 10 steps `success`, **13 635 passed**, **295 tracked YAML files** |
| Final closure | `issuecomment-5426014312` — `2026-08-26T13:28:20Z`, strictly after both the post-merge verification and the CI job's completion at `13:25:43Z` |
| Strict chronology | acceptance `13:13:45Z` → merge `13:14:53Z` → verification `13:15:39Z` → CI completion `13:25:43Z` → closure `13:28:20Z` |
| Open pull requests | **zero** |
| Worktree | clean, synchronized with `origin/main` |

**`XASSET-0057` is therefore effective**, by complete closure of all seven conditions, in order.

### The fail-closed condition this unit exists to authorize repairing — later, not here

| | SHA-256 | blob |
|---|---|---|
| **Bound** in the load-bearing register | `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541` | `f71b08b4ebe95f161c57cdbb2a924748f13af02d` |
| **Current merged** module | `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5` | `b5622f9e412afd604a11cde04317b79c5e57920a` |

The mismatch is **deliberate** and **fail-closed**. All three authorization predicates return
`False`, the lane is `ABSENT`, `AUTHORIZATION_ROOT` is absent, `ATTEMPT_1` is intact and unclaimed,
`LOAD_BEARING_RELPATHS` holds **18** paths, and no `stage1_results.yaml` exists.
**This filing repairs none of that, and must not.**

`12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5` is `XASSET-0057` §F.0's
**permanent negative pin**. This decision reaffirms it and adds nothing that could bind it.

## Decision

### A. Determination — `FORMAL_DISPOSITION_PARSER_CORRECTION_AUTHORIZED`

Exactly **one** future, separate, bounded pull request may implement the formal-disposition parser
correction that `XASSET-0057` §F.0.2 requires.

This determination is **design-only**. It arms nothing, executes nothing, moves no byte of any
production module, and performs **no** rebinding. **Merging this decision corrects no parser.**

### B. The authority this filing rests on, quoted rather than inferred

1. `XASSET-0057` §F.0: the parser defect "must be corrected, under separate authority, **BEFORE**
   any rebinding", and the condition "is not satisfied by disclosure".
2. `XASSET-0057` §F.0.2: the separately authorized parser-correction decision "must" define a
   total, mechanically testable boundary and satisfy eight enumerated obligations.
3. `XASSET-0057` §F.0.3: **two** lifecycles must close — **A1–A7** for this authorization, then
   **B1–B8** for the implementation. "Accepted and merged" does **not** mean effective.
4. `XASSET-0057` §M: "Nothing here rules on whether the reported behaviour should be corrected, or
   how. That question is **open, unresolved, and outside this grant.**"

`XASSET-0057` is the live authority for **this** filing's existence. It is **not** authority for the
implementation, which §F.0.3 places behind this decision's own complete A1–A7 closure.

### C. The defect family, reproduced before anything was decided

Per this repository's standing *verify before acting on external review* guardrail, the whole family
was **executed against the merged bytes**, read-only, before any boundary was chosen. Nothing below
is quoted from `XASSET-0057`; every figure was re-measured this session.

**The swept region** is derived, not assumed: the canonical prefix `FORMAL DISPOSITION:` minus its
terminating colon — the 18-character label `FORMAL DISPOSITION`, which has exactly **17 non-space
positions** and exactly **17 distinct-character adjacent pairs**.

Each probe is an **adverse first formal line** followed by a **canonical approval**, so a *skip*
means the later approval wins.

| Mutation family across the 17 positions | n | bypass at `parse_formal_disposition` | bypass at seam 2 | bypass at seam 3 | bypass at seam 3 with native `APPROVED` |
|---|---|---|---|---|---|
| Single-character **deletion** | 17 | **17** | 17 | 17 | 17 |
| ASCII **substitution** | 17 | **17** | 17 | 17 | 17 |
| ASCII **insertion** | 17 | **16** | 16 | 16 | 16 |
| **Adjacent transposition** | 17 | **17** | 17 | 17 | 17 |
| **Unicode / confusable substitution** | 17 | **17** | 17 | 17 | 17 |
| **TOTAL** | **85** | **84** | **84** | **84** | **84** |

The measurements reproduce `XASSET-0057` §F.0.1 exactly. The one non-bypassing cell is **insertion
at position 0**: `XFORMAL DISPOSITION:` leaves the canonical prefix intact as a substring, so
`parse_formal_disposition` returns the `MALFORMED_FORMAL_DISPOSITION` **sentinel object** — not the
adverse verdict — and the parse stops. That is **fail-closed MALFORMED**, exactly as §F.0.1 records
it, and the supporting artifact pins it by **identity** against the sentinel.

**Root cause, stated exactly.** Acceptance and resemblance are decided by two different views of the
line. The resemblance view

```
FORMAL_DISPOSITION_PREFIX in "".join(c for c in line.upper() if " " <= c <= "~")
```

requires the canonical prefix as an **exact substring** of the projected line. Every mutation that
breaks that exact substring — a dropped character, a swapped character, a transposed pair, or a
non-ASCII lookalike that the printable-ASCII projection **deletes** — makes the line invisible to
the resemblance test, so it is skipped as ABSENT rather than failing closed. The three homoglyphs
`XASSET-0057` §M reproduced are **one cell** of that matrix; 84 of 85 cells behave identically.

### D. THE RECOGNITION BOUNDARY — decided here

`XASSET-0057` §F.0.2 requires this decision to **decide** the boundary, not restate the
requirement. It is decided below, and it was **selected by measurement**, not by preference:
two candidate rules were specified in full and evaluated against the mutation matrix, the
repository's whole prose corpus and the real historical lifecycle corpus before either was adopted
(§D.7).

#### D.1 — Acceptance is UNCHANGED. Not narrowed, not widened, not restated as a new rule.

The future implementation may not alter, in any direction:

* the exact accepted grammar;
* the existing ASCII case compatibility — ASCII upper, lower and mixed case remain interchangeable,
  and a non-ASCII character never becomes an ASCII prefix letter;
* the exactly **two** accepted wrapper forms already governed by `XASSET-0053` §D.2/§D.16 — the
  plain canonical line, and a precisely balanced whole-line Markdown-bold pair whose enclosed text
  is itself a plain canonical line and carries no further `*`;
* the rule that acceptance consults the **ASCII-folded view only**;
* the **open** verdict vocabulary, and whole-verdict **exact equality** as the approval boundary
  (`XASSET-0055` §C). The verdict is never normalized, replaced, truncated, case-folded,
  fuzzy-matched, canonicalized or coerced.

**Fuzzy matching is confined to CLASSIFICATION and is forbidden in ACCEPTANCE.** No approximate
comparison of any kind may participate in deciding whether a line is accepted or what its verdict
is.

#### D.2 — The candidate rule, stated exactly

A **formal-disposition candidate** is a line a reviewer would read as a formal record but which is
not the exact accepted grammar. The rule is evaluated **only** on the branch the parser takes when
the canonical prefix is **absent from the ASCII-folded line** — so it can never be reached by an
accepted form.

For a raw line `L`:

1. **Projections.** Let `indent` be the count of leading **ASCII spaces** in `L`, and let
   `revealed` be `L` with those leading ASCII spaces and any trailing ASCII spaces and tabs
   removed. The projections of `L` are `revealed`, and — only when
   `len(revealed) >= 4 and revealed.startswith("**") and revealed.endswith("**")` —
   additionally `revealed[2:-2]`. **No third projection exists.** These are exactly the two
   governed wrapper forms of §D.1; the candidate rule adds no new wrapper and recognizes none.

2. **Label window.** For each projection `P`, let `j` be the index of the **first ASCII colon**
   `U+003A` in `P`, searched **only within the closed window `P[:20]`**. If no such colon exists in
   that window, `P` yields no candidate.

3. **Length gate.** If `abs(j - 18) > 1`, `P` yields no candidate. (`18` is
   `len("FORMAL DISPOSITION")`; a label within one edit of it has length 17, 18 or 19, so its
   terminating colon can only sit at index 17, 18 or 19. The window in step 2 is therefore closed
   at 20 without loss, and the rule is **O(1) in the line's length**.)

4. **Bounded comparison.** `P` is a candidate iff

   ```
   osa(ascii_fold(P[:j]), "FORMAL DISPOSITION") <= 1
   ```

   where `ascii_fold` is the same ASCII-only case fold acceptance already uses, and `osa` is the
   **restricted Damerau / optimal-string-alignment** distance in which deletion, insertion,
   substitution and **adjacent transposition** each cost exactly `1`. The comparison is **capped at
   1** and never explores beyond the cap.

5. `L` is a candidate iff **any** of its projections is.

**The edit budget is exactly one.** `1` is a **`NUM-0001` class 5 provisional governance
guardrail**, not an empirically calibrated value: it is the smallest budget that closes the entire
measured family (§C), and it is the largest budget for which the measured false-positive count over
both corpora is zero (§D.5). It is reviewed if a future measured mutation family requires two or
more edits, or if a measured prose regression appears at one.

#### D.3 — What every mutation family becomes. Each named and decided.

| Family | Disposition under the rule | Cells caught |
|---|---|---|
| Single-character **deletion** in the label | **MALFORMED** | **17 / 17** |
| ASCII **substitution** in the label | **MALFORMED** | **17 / 17** |
| ASCII **insertion** in the label | **MALFORMED** | **17 / 17** |
| **Adjacent transposition** in the label | **MALFORMED** | **17 / 17** |
| **Unicode / confusable substitution** in the label | **MALFORMED** | **17 / 17** |
| **TOTAL** | | **85 / 85** |

Measured identically at **85 / 85** for the plain line, for the `**bold-wrapped**` line, and for the
line indented by three ASCII spaces — **255 / 255** across the three governed presentations.

**Every candidate outside the exact accepted grammar becomes `MALFORMED_FORMAL_DISPOSITION`, and a
MALFORMED first formal line STOPS the parse.** No later, better-formed line can win past it. This is
`XASSET-0053` §D.17's existing rule, now reached by the family that previously escaped it.

#### D.4 — Multiple-edit and out-of-bound cases are DISPOSITIONED, not left undefined

A projection whose label is **more than one edit** from the canonical label, or whose label length
is outside `{17, 18, 19}`, or which carries no ASCII colon within the closed window, is **NOT a
candidate**. It receives the parser's existing ABSENT treatment, unchanged. The rule is **total**:
every line falls in exactly one of the two classes, and no input is undefined.

#### D.5 — Ordinary prose stays ABSENT. Measured, not asserted.

| Corpus | Size | Lines that are **ABSENT today** and would become **MALFORMED** |
|---|---|---|
| Every line of every tracked repository Markdown file — *409 files / **131 143 lines** at this filing's base, the corpus the boundary was selected against; **410 files / 131 685 lines** at this filing's own head, which additionally includes this decision file itself. **Zero** either way — the supporting artifact measures the live corpus, so it proves the self-inclusive figure* | 409→410 files, **131 143→131 685 lines** | **0** |
| Every line of every real review and comment body on PRs 320–358 — *measured live in this filing session; network-dependent and therefore not re-derivable offline, so the supporting artifact proves the Markdown corpus above plus every real review-body line committed in this repository's own fixtures* | 317 bodies, **19 741 lines** | **0** |

On the real historical corpus the **whole-body** verdict is unchanged for **317 / 317** bodies: all
**27** bodies that authenticate today still authenticate, and all **54** bodies carrying an adverse
or other verdict today still carry it. Headings, blockquotes, bullets, malformed emphasis, code
fences and prefix-bearing marker lines all keep their existing dispositions.

Every line the rule flags is accounted for, in both corpora, with nothing left in an unexplained
residue:

| | Markdown corpus | Real corpus |
|---|---|---|
| Flagged **and already `MALFORMED` today** — unchanged, not regressions | **2** | **9** |
| Flagged **and already yielding a verdict today** — the rule never reaches them, because the hook sits on a branch an accepted form cannot take (§D.2, §D.6) | **6** | **87** |
| Flagged **and `ABSENT` today** — the only category that would be a regression | **0** | **0** |

Independently verified on **both** corpora, not only one: **zero** verdict-yielding lines lack the
canonical prefix in the ASCII fold, so no accepted line can reach the candidate branch at all.

#### D.6 — Candidate recognition can NEVER authenticate

Stated as an operative prohibition on the future implementation, not as a hoped-for property:

* the candidate rule may **only** cause additional **fail-closed MALFORMED** results;
* it may **never** produce, repair, normalize, complete or coerce an approving verdict, nor any
  verdict at all;
* it operates on the **prefix/label** boundary only and **never** on the verdict region;
* it is **deterministic**, **bounded**, and mechanically specified;
* it introduces **no** general Unicode framework, **no** general Markdown framework, **no**
  normalization table, **no** confusable map, and **no** third wrapper form.

A tampered prefix could not directly authenticate before this correction and must not afterwards.

#### D.7 — The rejected alternative, recorded because it was measured

A second rule was specified in full and evaluated identically: compare bounded **leading windows**
`P[:18]`, `P[:19]`, `P[:20]` against the 19-character prefix **including** its colon. It also caught
**85 / 85** of the required cells and additionally caught mutation **of the colon itself** — but it
produced a genuine prose regression: a line reading `formal disposition but is not in an accepted
form …` is **ABSENT today** and would become **MALFORMED** under it, because dropping the colon is a
one-edit difference indistinguishable from ordinary prose that simply begins with those two words.

`XASSET-0057` §F.0.2 item 4 requires that ordinary prose be **preserved as ABSENT** so the boundary
does not collapse into treating all text as formal. The adopted rule scores **0** regressions on
both corpora; the alternative scores **1**. The adopted rule was selected on that measurement.

#### D.8 — The residual, explicitly dispositioned rather than silently omitted

Mutation **of the terminating colon itself** — deleting it, or replacing it with any other
character, ASCII or not — is **decided as ABSENT**, deliberately.

**The reasoning, stated so it can be reviewed rather than assumed.** The accepted grammar requires
the colon; the colon is what makes a line present as a *labelled record* rather than as a sentence
that happens to begin with two ordinary English words. A line with no ASCII colon at the label
boundary is, by the repository's own accepted grammar, **not an attempt at the formal grammar** — so
treating it as a failed attempt would be the boundary collapse §F.0.2 item 4 forbids.

Three properties are recorded honestly:

1. This is **unchanged behaviour**, not a new hole: `FORMAL DISPOSITION CHANGES REQUIRED` and
   `FORMAL DISPOSITION; CHANGES REQUIRED` are ABSENT today and remain ABSENT.
2. It is **outside the family `XASSET-0057` §F.0.1 measured**, whose swept region is the 18-character
   label and whose five families are fully closed at 85 / 85.
3. A case-based discriminator would separate the attack from the prose — but `XASSET-0055` §D
   **removes and PROHIBITS** case-, length- and word-count-based rules in this parser, so that route
   is closed by accepted authority and was not taken.

Whether this residual should itself be closed, and by what mechanism, is **open, unresolved and
outside this grant**. It may not be closed inside the Lifecycle B implementation without its own
separate authorization.

### E. Required evidence and positive controls for the Lifecycle B implementation

The implementation must **prove** the boundary, not describe it:

1. **Family-by-position matrices** for all five families, at every position, driven through the real
   `parse_formal_disposition` — never a re-implementation.
2. **Exact positive controls** for every accepted form: the plain canonical line, the whole-line
   bold pair, ASCII upper/lower/mixed case, an adverse canonical verdict, and a canonical line with
   a validated finding-count suffix. Each must return **exactly** what it returns today.
3. **Ordinary-prose ABSENT controls**, including headings, blockquotes, bullets, malformed emphasis,
   code fences and prefix-bearing marker lines.
4. **Every real historical lifecycle review body** retains its existing verdict.
5. **All three consumer seams** — `_derive_pr337_actor_ratification`,
   `verify_lifecycle_against_truth` and `_verify_selected_review_is_final` — must refuse every
   attack, driven through the real seams.
6. **Native-`APPROVED` rescue** must fail: a MALFORMED body is refused whatever the native state,
   and seam 3's genuinely-**ABSENT** policy is **preserved exactly** as `XASSET-0053` §D.20.1 left
   it.
7. **Structural proof** that the candidate mechanism cannot return or create a verdict.
8. **No fourth call site** of `parse_formal_disposition`, and no general parsing framework.
9. **Counts derived** from the iterated mappings, never separately maintained literals.
10. **Known-bad controls for every detector**, and **mutation proof** that each check fails when
    removed — including at least one probe per family and one per positive-control class.

**Vacuity is prohibited**, restated as operative text: no `or True`; no exhaustive `x == y or
x != y`; no assertion satisfiable by its own source text; no test that re-implements the production
detector and compares it with itself; no existence-only lifecycle or vocabulary guard. Each mutation
must independently exercise its intended requirement **and fail for the intended reason**.

### F. Authority granted — exactly one future, separate implementation unit

Effective only on this decision's own complete Lifecycle A closure (§I), **exactly one** future,
separate, bounded pull request may:

1. correct `parse_formal_disposition()` in `level1_stage1_execution_authorization.py` to implement
   §D, and nothing else in that function;
2. add **at most one** narrowly devoted candidate-recognition helper, and **only** if the
   implementing session proves it smaller and clearer than inline logic — otherwise the logic stays
   inline;
3. add its own supporting test module, and update the existing parser suites to pin the values it
   lawfully changes **without weakening any of them**;
4. synchronize `governance/decisions.yaml` and the `WS-0014` register.

**The three consumer seams already exist and already enforce the MALFORMED/ABSENT distinction.**
They are therefore **out of scope**: the implementation may **not** reopen
`_derive_pr337_actor_ratification`, `verify_lifecycle_against_truth` or
`_verify_selected_review_is_final` unless read-only reproduction proves a consumer change strictly
necessary — in which case it must **stop and disclose** rather than proceed. Tests may and must
drive all three seams **without editing them**.

### G. The required properties of the authorized implementation

**G.1 — It may not begin before this decision is EFFECTIVE.** Not merged: **effective**, by complete
Lifecycle A closure (§I). `XASSET-0044` and `XASSET-0045` each merged and neither became effective.

**G.2 — Its base.** It must base **exactly** on this authorization's own normal-merge commit, unless
a separately governed rule accepted later explicitly says otherwise. If `main` carries **any**
intervening commit, the unit **stops and discloses**; it does not proceed, absorb or cure.

**G.3 — The vulnerable identity is preserved as adverse history.**
`12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5` remains `XASSET-0057` §F.0's
permanent negative pin. The implementation **does not** rebind it, **does not** re-pin it, and
**does not** repair the register mismatch — those are `XASSET-0057`'s reserved successor unit, not
this chain.

**G.4 — Its corrected identity is DERIVED, never predicted.** The corrected module's SHA-256 is
computed **once, after every authorized byte has stabilized**, at the implementation's own merge.
It is `XASSET-0057` §F.3's **role 3**, and it is stated nowhere in advance.

**G.5 — It must close its own Lifecycle B in full**, per `XASSET-0057` §F.0.3:

* **B1.** the implementation itself;
* **B2.** independent **FULL** exact-head review under `OPS-0007` §1;
* **B3.** any bounded correction and **exact-head re-review**, so B2 holds at its **final** accepted
  head;
* **B4.** explicit principal exact-head acceptance at that final head;
* **B5.** normal merge;
* **B6.** immediate post-merge verification;
* **B7.** **successful merge-commit CI whose `head_sha` is that implementation's exact merge SHA**;
* **B8.** final post-CI verification and lifecycle closure.

**The B5 normal-merge commit is the SHA tested by B7 and named by B8 — the same commit, and the unit
must prove it.** That B5 merge is the **sole** qualifying base for the later `XASSET-0057`
step-8-equivalent rebinding, per `XASSET-0057` §F.2.

**G.6 — Both lawful review paths, and only those two.** Either a **clean FULL** exact-head review at
the **unchanged** final accepted head, with no correction and **no** re-review; or a **FULL** review
at the original head, a **continuous** fast-forward correction chain, and an exact-head **DELTA**
re-review at the **final** accepted head. The original FULL-reviewed head is preserved **separately**
from the final DELTA-reviewed head; neither is rewritten to the other. A re-review recorded without
a chain is incoherent and is refused.

**G.7 — Chronology is DERIVED from ISO-8601 instants**, never asserted: review → acceptance → merge
→ post-merge verification; CI completion after merge; closure **strictly** after both. Missing,
malformed, **equal-where-strict-order-is-required**, reversed and mismatched instants are all
refused.

**G.8 — Lifecycle A and Lifecycle B stay separate.** Merged is not effective. Neither lifecycle's
closure implies the other's, and **no** single step of either is individually sufficient.

### H. Authority withheld — absolute

The authorized implementation may **not**:

* perform, or authorize, the step-8-equivalent **rebinding** — that remains `XASSET-0057`'s own
  reserved successor unit, unauthorized here;
* re-pin or extend `LOAD_BEARING_RELPATHS`, or change any load-bearing or canonical digest;
* bind, rebind, or repair `12eab05e…604a5`, or repair the register mismatch;
* amend `PROTOCOL_V1.md` or `pre_registration.yaml`;
* alter acceptance, the accepted wrapper forms, the verdict vocabulary, whole-verdict exact
  equality, or ASCII case compatibility (§D.1);
* introduce fuzzy matching, normalization or coercion anywhere in acceptance or verdict
  determination (§D.1, §D.6);
* close the §D.8 residual, or widen the boundary past §D;
* add a fourth call site of `parse_formal_disposition`, or a general parsing framework;
* touch `AUTHORIZATION_ROOT`, the lane, the ledger, `ATTEMPT_1`, or any execution artifact;
* generate an attestation, arm Stage 1, claim the attempt, execute, or produce results;
* perform readiness or drift verification, data acquisition, allocation or trading, or access
  protected `RISK` paths;
* weaken, delete, skip, `xfail` or bypass any test or validator.

### H.1 — Scope of this filing, and the coupled suites it re-anchors

This filing changes **no production byte**. Its change set is exactly eighteen files: this
decision, its supporting artifact, `governance/decisions.yaml`, `operations/WORKSTREAMS.yaml`,
`test_portfolio_hq_dashboard_decisions.py`, and **thirteen** predecessor suites.

`WS-0014`'s `active_branch`, `active_pr` and `last_verified_main_sha` are **single shared live
self-reference fields** under `OPS-0001`'s Active-GitHub-fields rule, so they lawfully name
whichever unit is live. Every suite that pinned the previous generation's values is therefore
**re-anchored, never weakened**: the new value becomes the positive pin, the superseded value is
**retained beside the new one as a negative pin** rather than deleted — so each field stays bound
at **both** ends and a silent revert to finished work still fails — and each suite's own **gate**,
which does not move, remains the durable anchor for what the assertion was really protecting.

**Nothing was deleted, skipped, `xfail`ed or relaxed.** Every re-anchored suite's assertion count
is greater than or equal to its count at this filing's base, its `skip`/`xfail` count is
unchanged, and **no re-anchored suite is a load-bearing path** — re-anchoring a bound path would
silently invalidate the module's own trust boundary and require a rebinding this filing is not
authorized to perform. The supporting artifact enforces every clause of this paragraph
mechanically, including that the re-anchoring is **non-vacuous** at the base.

### I. Effectivity — this decision's own Lifecycle A

This decision is **not** effective on merge alone. It becomes effective only on complete closure of
all seven, in order:

* **A1.** independent **FULL** exact-head review under `OPS-0007` §1;
* **A2.** any bounded correction and **exact-head re-review**, so A1 holds at its **final** accepted
  head — a review anchored to a superseded head does **not** satisfy A1;
* **A3.** explicit principal exact-head acceptance at that final head, authored by the principal
  account with `author_association: OWNER` and **no** `[bot]` suffix;
* **A4.** normal merge;
* **A5.** immediate post-merge verification;
* **A6.** **successful merge-commit CI whose `head_sha` is this decision's exact merge SHA** — a
  green PR-head run is **not** a substitute;
* **A7.** final post-CI verification and lifecycle closure.

**None of A1–A7 is individually sufficient.** An authorization merged with failed merge-commit CI,
merged with no recorded closure, reviewed at a stale head, or otherwise incomplete confers
**nothing**, and the Lifecycle B implementation may not begin.

### J. Fail-closed

If any condition in §§D–I cannot be satisfied, the correct outcome is to **stop and disclose**, not
to proceed on a narrowed reading. Nothing in this decision creates a path by which Stage 1 becomes
executable, and nothing in it is satisfied by disclosure.

### K. Absolute non-authorization

This decision, and the implementation it authorizes, **do not**: arm Stage 1; generate an
attestation; create a lane; claim `ATTEMPT_1`; execute any construction; produce, write or validate
any result; perform any rebinding, re-pinning, readiness verification or drift verification; acquire
data; change `stage_1_executability.executable`, which stays permanently `false`; add any activation
authorization; alter any target, tier, holding, cap, cluster, gate, allocator or margin behaviour;
recommend or place any order; or access protected `RISK` paths.

`XASSET-0029` §E's no-infinite-authorization-regress rule stays **intact and unweakened**. This is
**not** an activation PR. Final activation remains the external one-shot runtime attestation and the
operator's act — **never** another merged authorization PR.

`XASSET-0027` §P.1's exactly-one **evaluation/results** pull request is **not consumed, replaced or
counted against** by this decision or by the unit it authorizes. It remains reserved and unspent.

## Rationale

`XASSET-0057` closed a real gap by making the parser correction a mandatory prerequisite to
rebinding — and then, correctly, refused to design the correction inside the authorization that
withheld it. That left the programme in a precise state: a **measured** defect, a **required** fix,
an **explicit** eight-point specification for it, and **no live authority** to write it. This filing
supplies exactly that authority and nothing else.

The one thing this decision could not defer is the **boundary itself**. §F.0.2 item 1 requires a
total, mechanically testable definition with no residual undefined region, and a specification that
merely repeated the requirement would hand the implementing session an open design question at the
moment it is least able to answer it carefully. So the boundary is decided here, chosen by
measurement over two fully specified alternatives, and proved against 150 884 real corpus lines
before adoption.

The boundary is deliberately **asymmetric**. Acceptance is untouched, exact and ASCII-only;
recognition is bounded, fuzzy and classification-only. That asymmetry is the whole safety property:
fuzziness that can only ever add a fail-closed refusal cannot manufacture an approval, whereas
fuzziness in acceptance is exactly the failure `XASSET-0055` §D removed and prohibited. Keeping the
two apart — and saying so in operative text rather than in commentary — is what makes an
approximate comparison safe to introduce at all.

The §D.8 residual is recorded rather than engineered away for the same reason. Closing it needs
either a case-based discriminator that accepted authority prohibits, or a rule that reclassifies
ordinary English prose as a failed formal record — which is the boundary collapse §F.0.2 item 4
exists to prevent. Between an unchanged, already-ABSENT shape and a measured prose regression, the
honest choice is the unchanged shape plus an explicit, reviewable statement of why.

## Alternatives considered

**Restate `XASSET-0057` §F.0.2 and leave the boundary to the implementation.** Rejected: §F.0.2
requires the *decision* to define the boundary, and deferring it would reproduce the exact defect
`XASSET-0057` was written to prevent — an obvious next step with no decided specification behind it.

**Adopt the leading-window rule that also catches colon mutation (§D.7).** Rejected on measurement:
it introduces a genuine ABSENT→MALFORMED prose regression, which §F.0.2 item 4 forbids. Recorded
rather than omitted, because it was fully specified and measured before rejection.

**Patch the three `XASSET-0057` §M homoglyphs.** Rejected in terms by §F.0.1: they are one cell of
an 85-cell matrix, and 84 cells bypass.

**Widen the resemblance projection to keep non-ASCII characters instead of deleting them.**
Rejected: it addresses only the confusable family, leaves deletion, substitution, insertion and
transposition entirely open, and moves a Unicode-wide operation back into a decision path
`XASSET-0055` §D deliberately narrowed.

**Combine this authorization with its implementation in one pull request.** Rejected in terms:
`XASSET-0057` §F.0.3 requires **two** lifecycles, and B1 may not begin before A7 closes.

**Repair the register mismatch here, since the correction is now authorized.** Rejected: the
rebinding is `XASSET-0057`'s own separately reserved successor unit, and §F.2 anchors its base to
the **B5 implementation merge**, which does not yet exist.

## Consequences

`XASSET-0057` §F.0's Lifecycle A now has a filed authorization. When — and only when — this
decision's own A1–A7 close in full, exactly one implementation unit may begin, under §§D–H, and must
close its own B1–B8. That B5 merge then becomes the sole qualifying base for `XASSET-0057`'s
step-8-equivalent rebinding.

Until then nothing changes. The register digest stays stale, all three authorization predicates stay
`False`, the lane stays `ABSENT`, `ATTEMPT_1` stays unclaimed and unconsumed, `LOAD_BEARING_RELPATHS`
stays at 18, and **Stage 1 remains UNARMED and NOT EXECUTABLE**.
