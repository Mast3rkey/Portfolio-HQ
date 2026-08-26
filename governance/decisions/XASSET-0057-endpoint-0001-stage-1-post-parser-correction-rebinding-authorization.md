---
decision_id: XASSET-0057
date: 2026-08-26
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, XASSET-0055, XASSET-0056, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_parser_correction_rebinding_authorization.py
---

## Context

`XASSET-0056` merged. Its parser correction is now the merged state of
`level1_stage1_execution_authorization.py`, and that module's identity therefore no longer matches
the digest the load-bearing register binds. The mismatch is **deliberate**, it is **fail-closed**,
and `XASSET-0056` expressly refused to repair it.

This is a **design-only Lane G governance authorization** under `OPS-0009`. It grants authority for
exactly one future, separate step-8-equivalent rebinding unit. **It performs no rebinding.**

### Live preflight

Every anchor was independently re-resolved from live git and live GitHub before anything was
edited. Nothing was taken on the authorizing task's word, and no identity below is quoted from a
brief.

| Fact | Verified |
|---|---|
| Base | `583022a5f2106d61f82d270edadd3520d8b0c55d` — GitHub `main`, `origin/main`, the local checkout and this branch's base all equal it |
| PR #357 | **merged**, `state: closed`, `merged_by: Mast3rkey`, `merged_at 2026-08-25T22:47:15Z` |
| Merge shape | GitHub's **normal merge**: exactly two parents, parent 1 `29e4969885970d942a5acecc1424fb2e2b080d60`, parent 2 `f1bf3fd0f1f878ccf9db88f15c48059e5e4637e2` — **in that order** |
| Zero drift at merge | merge tree `8df4624eac7477a7b898e92178bc46be3ff1056b` is **byte-identical** to the accepted head's own tree |
| Clean review | `5024576065` @ `f1bf3fd…`, by `Mast3rkey`, `OWNER` — approving verdict, **0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE** |
| Principal acceptance | `issuecomment-5417902549` — `2026-08-25T22:46:38Z`, strictly after the review and strictly before the merge |
| Post-merge verification | `issuecomment-5417925363` — `2026-08-25T22:48:42Z`, strictly after the merge |
| Merge-commit CI | run `32907801650`, job `97995562890`, `event: push`, `run_attempt: 1`, `completed`/`success`, **both `head_sha` equal to the exact merge SHA**, 10 of 10 steps `success`, **13 284 passed** |
| Final closure | `issuecomment-5418040301` — `2026-08-25T22:59:49Z`, strictly after both the post-merge verification and the CI job's completion at `22:58:06Z` |
| Open pull requests | **zero** |
| Worktree | clean, single worktree, synchronized with `origin/main` |

**`XASSET-0056` is therefore effective**, by complete closure of all seven conditions, in order.

### The fail-closed condition this unit exists to authorize repairing — later, not here

| | SHA-256 | blob |
|---|---|---|
| **Bound** in the load-bearing register | `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541` | `f71b08b4ebe95f161c57cdbb2a924748f13af02d` |
| **Current merged** module | `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5` | `b5622f9e412afd604a11cde04317b79c5e57920a` |

`_verify_git_anchored_identity()` is byte-identical to its base and still raises `enforcement
drift`. Both authorization predicates return `False`. Stage 1 is **NOT EXECUTABLE**.

**This filing does not repair the mismatch, and must not.** The stale digest is the safety property
holding Stage 1 closed; removing it is precisely the act that requires its own authority, its own
review and its own lifecycle.

### The question this unit answers

`XASSET-0056` §H recorded the newly derived identity **for** a later rebinding and stated it "is not
applied by anything here." §J forbade it from performing "a step-8-equivalent rebinding" or
authorizing "link 5, or any successor unit of any kind." Its closure record repeated the point:
"**The successor rebinding is a separate, separately authorized work item** — closing this lifecycle
neither performs it nor authorizes it."

So the successor is **needed and unauthorized**. `XASSET-0048`'s own grant is **spent** — it
authorized *exactly one* rebinding unit, and `XASSET-0049` consumed it. No live authority exists for
another. **This decision supplies it, and nothing else.**

## Decision

### A. Determination — `STEP_8_EQUIVALENT_REBINDING_AUTHORIZED`

Exactly **one** future, separate, bounded pull request may perform the step-8-equivalent rebinding
that reconciles the load-bearing register with the merged `XASSET-0056` bytes.

This determination is **design-only**. It arms nothing, executes nothing, and moves no byte of any
production module. **Merging this decision performs no rebinding.**

The grant is **conditional, not standing**: §F.0 makes a separately authorized, independently
reviewed, principal-accepted, merged, exact-merge-CI-green and lifecycle-closed **parser correction**
a mandatory conjunctive prerequisite, and the present vulnerable module may **never** be rebound.

### B. The authority gap, reproduced from accepted text before anything was authorized

Each line below is quoted from an accepted, merged record, not inferred:

1. `XASSET-0048` §E granted "**exactly one** future, separate, bounded pull request" the rebinding
   authority. That grant is **spent**: `XASSET-0049` is the unit that exercised it, and it is the
   value `AUTHORIZING_DECISION` still carries.
2. `XASSET-0056` §H: the derived identity "is **recorded for** a later, separately authorized
   step-8-equivalent rebinding unit, and is **not applied by anything here**."
3. `XASSET-0056` §J: this decision and implementation must not "**perform a step-8-equivalent
   rebinding**, or re-pin any load-bearing or canonical digest," nor "authorize or perform link 5,
   **or any successor unit of any kind**."
4. `XASSET-0056`'s closure record: "**The successor rebinding is a separate, separately authorized
   work item** — closing this lifecycle neither performs it nor authorizes it."

**Conclusion: no live authority existed.** `XASSET-0056` becoming effective did not create one, and
this filing does not claim that it did. Reading §H's *recording* of an identity as a *grant* to apply
it is exactly the inference §H's own final clause forecloses, and it is refused here in terms.

### C. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

`XASSET-0027` §P.1's exactly-one **evaluation/results** pull request is **not consumed, replaced, or
counted against** by this decision or by the unit it authorizes. It remains reserved and unspent, on
the same three independent grounds `XASSET-0036` recorded: §P.1's own text forbids its PR from making
any production configuration change, while a rebinding is nothing but such a change; the deliverables
differ (outputs versus implementation); and the two sit on **opposite sides of arming**.

### D. Relation to `XASSET-0029` §E — not an activation PR, zero activation authorizations

`XASSET-0029` §E's no-infinite-authorization-regress rule stays **intact and unweakened**. This is
**not** an activation PR: it generates no attestation, arms nothing, and adds **zero** activation
authorizations. `stage_1_executability.executable` stays permanently `false`. Final activation
remains the external one-shot runtime attestation and the operator's act — **never** another merged
authorization PR.

### E. Authority granted — exactly one future, separate rebinding unit

Effective only on this decision's own complete lifecycle closure (§J) **and** on complete
satisfaction of the **conjunctive parser-correction prerequisite in §F.0** — both, not either —
**exactly one** future, separate, bounded pull request may:

1. file its **own** rebinding decision record, under the next `XASSET-####` identifier **verified
   unused against live repository state at the time it is filed** — never predicted, reserved, or
   named here;
2. rebind the effective structural authorization source to that decision, and rebind
   `AUTHORIZING_PULL_REQUEST` and `REVIEWED_BASE_SHA` to that unit's own verified pull request and
   verified base (§F.1, §F.2, §F.3);
3. edit `level1_stage1_execution_authorization.py` **only** to the extent that unit's own
   configuration, identity constants, evidence, refusals and validation require (§F.6);
4. extend `LOAD_BEARING_RELPATHS` **additively** with **every** decision file that makes the newly
   bound bytes lawful — including, at minimum, the parser-governing chain §F.7 enumerates —
   removing nothing (§F.7);
5. amend the canonical artifacts **only** in authorization language, in lockstep, and only to the
   extent the rebinding's own authorization identity requires (§F.8);
6. recompute stale identities and pins **once**, after every authorized byte has stabilized (§F.9);
7. synchronize `governance/decisions.yaml` and the `WS-0014` register, and update the tests that pin
   the values it lawfully changes, **without weakening any of them**.

### F. The required properties of the authorized rebinding

Each is a condition on the authorized unit. **None is satisfied by this filing**, and none may be
waived by the unit that performs it.

**F.0 — The parser defect must be corrected, under separate authority, BEFORE any rebinding.**
This condition is **conjunctive with every other condition in §F**, not an alternative to any of
them, and it is not satisfied by disclosure.

§M records a defect that is **live in the exact bytes this grant would otherwise bind**: at module
identity `12eab05e…604a5` an adverse first formal line whose prefix is *near-canonical but not
canonical* is **skipped**, so a later canonical approval wins. Rebinding those bytes would install a
known-fail-open parser as the **accepted enforcement anchor**. That is refused here in terms.

**The current vulnerable module may never be rebound.** `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5`
is recorded as a **permanent negative pin**: no rebinding under this grant may bind it as any bound
end, at any time, under any reading, however unchanged `main` may be.

**F.0.1 — The defect is a FAMILY, not three code points.**

§M's three homoglyphs are **reproduced examples of one root family**, never its definition. A
read-only audit executed the **unchanged** parser at `12eab05e…604a5` against an adverse first line
followed by a canonical approval, sweeping single-character mutations across the **17 non-space
positions** of the `FORMAL DISPOSITION` prefix. Measured, not asserted:

| Mutation family across the prefix | Result at the unchanged parser |
|---|---|
| Single-character **deletion** | **17 / 17** allowed the later approval to win |
| ASCII **substitution** | **17 / 17** |
| ASCII **insertion** | **16 / 17** |
| **Adjacent transposition** | **17 / 17** (17 distinct-character adjacent pairs) |
| **Unicode / confusable substitution** | **17 / 17** |

The single non-bypassing insertion is position 0 — inserting before the `F` yields
`XFORMAL DISPOSITION:`, in which the canonical prefix **survives intact as a substring**. That line
is therefore **recognized as formal-looking and fails closed as `MALFORMED`**, which stops the parse
so the later approval cannot win.

**Stated precisely, because the distinction matters:** the position-0 line is **not** parsed as the
genuine `CHANGES REQUIRED` disposition. `parse_formal_disposition` returns the module's
`MALFORMED_FORMAL_DISPOSITION` **sentinel object** — not the adverse verdict, and not a string, so
the supporting artifact pins it by **identity** against that sentinel rather than by a literal a
future refactor could reproduce accidentally. Both outcomes prevent the later approval
from winning — so no bypass reopens here — but the mechanism actually measured is **fail-closed
MALFORMED**, and this record describes what was measured rather than what would merely have been
sufficient. An earlier draft of this subsection said the line "is read as a genuine adverse record";
that wording is **withdrawn as inaccurate**. The distinction is pinned by the supporting artifact.

**Consequence, and the point of this subsection: a future correction that merely patches the three
§M code points does NOT satisfy §F.0.** The three are one cell of a much larger matrix, and every
other cell is open.

**F.0.2 — What the separately authorized parser-correction decision must do.**

That decision — which this filing neither writes nor authorizes — must:

1. define a **total, mechanically testable boundary** for what counts as a formal-disposition
   candidate, or a "formal-looking" line, with no residual undefined region;
2. **explicitly disposition** deletion, ASCII substitution, insertion, transposition, and
   non-ASCII/confusable substitution **across the prefix** — each named and decided, never silently
   omitted;
3. guarantee that **every** candidate outside the exact accepted grammar becomes **MALFORMED** and
   **cannot be skipped** such that a later approval wins;
4. preserve **ordinary prose as ABSENT** under a governed, testable rule, so the boundary does not
   collapse into treating all text as formal;
5. prove the rule through the **parser and all three consumer seams**, including **native-`APPROVED`
   rescue** cases;
6. use a **family-by-position adversarial matrix and mutation proof**, not only handpicked literals;
7. retain **exact positive controls** for every accepted form; and
8. complete **both** its own authorization lifecycle **and** its own implementation lifecycle
   (§F.0.3) before any rebinding.

**This filing does not decide that recognition boundary.** Fixing it here would be designing the
correction inside an authorization that expressly withholds it. The boundary is therefore **reserved
to that future decision, which must decide it and prove it** — and **XASSET-0057's rebinding remains
unavailable until that decision's complete lifecycle closes.**

**F.0.3 — TWO lifecycles must close, not one. Merged is not effective.**

This repository's own history is decisive: **`XASSET-0044` and `XASSET-0045` each merged and neither
became effective**, because the exact-merge-CI condition failed (see §F.10, which records both as
**not effective**). "Accepted and merged" therefore does **not** mean effective, and an authorization
that merged with failed merge-CI, or without recorded closure, or on a stale-head review, confers
**nothing**.

Two separate lifecycles must each close **completely and in order**:

**Lifecycle A — the parser-correction AUTHORIZATION decision must itself become EFFECTIVE:**

* A1. independent **FULL** exact-head review under `OPS-0007` §1;
* A2. any bounded correction and **exact-head re-review**, so A1 holds at its **final** accepted
  head — a review anchored to a superseded head does **not** satisfy A1;
* A3. explicit principal exact-head acceptance at that final head;
* A4. normal merge;
* A5. immediate post-merge verification;
* A6. **successful merge-commit CI whose `head_sha` is that authorization's exact merge SHA**;
* A7. final post-CI verification and lifecycle closure.

**Lifecycle B — the parser-correction IMPLEMENTATION, which may not begin until Lifecycle A has
closed in full:**

* B1. the implementation itself, correcting the defect family per §F.0.1–§F.0.2 in
  `level1_stage1_execution_authorization.py`;
* B2. independent **FULL** exact-head review under `OPS-0007` §1;
* B3. any bounded correction and **exact-head re-review**, so B2 holds at its **final** accepted
  head;
* B4. explicit principal exact-head acceptance at that final head;
* B5. normal merge;
* B6. immediate post-merge verification;
* B7. **successful merge-commit CI whose `head_sha` is that implementation's exact merge SHA**;
* B8. final post-CI verification and lifecycle closure.

**None of A1–A7 or B1–B8 is individually sufficient; only complete closure of both lifecycles is.**
Specifically and without exception, **each** of the following fails §F.0: an authorization merged
with **failed** merge-commit CI; an authorization merged with **no recorded closure**; an
authorization whose review anchors to a **stale head**; an authorization whose lifecycle is
otherwise **incomplete**; an implementation begun **before** Lifecycle A closed; and an
implementation whose own B1–B8 has not closed.

**F.0.4 — Where the corrected module's identity lives.**

The corrected module enters the **single ordered identity chain in §F.3 as role 3**. §F.0 states
**no** competing transition table of its own: §F.3's four-role chain is the sole operative statement
of module identity. Role 3's value is **derived** at the parser correction's own merge, never
predicted, exactly as §F.1 requires of every other identity. A rebinding whose bound module identity
equals role 2 — the vulnerable intermediate — **fails this condition outright**.

**This decision does not perform, design, schedule or authorize that parser correction.** It states
only that no rebinding may occur until one exists, is effective, and has closed both lifecycles.

**F.1 — Bind only stabilized, independently reviewed exact bytes.** The rebinding binds exact
git-object identities at its own accepted head and its own merge — never a value asserted in prose,
never a value computed before the bytes stabilized, and never a working-tree value no independent
review saw.

**F.2 — One base rule: equality to the parser-correction merge.**

This condition was reconciled against §F.0. §F.0 makes a separately authorized parser correction a
**mandatory** prerequisite, and any such correction **must** advance `main`. An absolute
"equal this decision's own merge" rule and a mandatory intervening merge cannot both hold, so the
earlier formulation — an absolute equality followed by a generic exception — is **withdrawn and
replaced**. What follows is the **single, unambiguous** future-base rule; there is no other, and no
exception clause qualifies it.

**The authorized unit's base must EQUAL the Lifecycle B implementation's normal-merge commit at
B5** — and nothing else.

The superseded wording said "the exact normal-merge commit that closes the required
parser-correction lifecycle (§F.0 conditions 1–8)". There are no longer generic "§F.0 conditions
1–8": §F.0.3 defines **two** lifecycles, **A1–A7** for the authorization and **B1–B8** for the
implementation, so "the parser-correction lifecycle" was ambiguous between them while exact base
identity is this section's load-bearing subject. That reference is **withdrawn and replaced** by the
following, which names the commit exactly:

1. **Lifecycle A1–A7 must already have closed** in full;
2. **Lifecycle B1–B8 must also have closed** in full;
3. the base must **equal the B5 normal-merge commit** of the Lifecycle B implementation;
4. that **exact B5 merge SHA is the SHA tested by B7** merge-commit CI, and **named by B8** closure —
   the three must be the *same* commit, and the authorized unit must prove it.

**What does NOT qualify**, stated so no reading can substitute one for another:

* **the Lifecycle A authorization merge** — it closes the authorization, not the implementation, and
  the corrected bytes do not exist at it;
* **any pre-implementation commit** — including this decision's own merge, at which the defect is
  still live;
* **any later descendant** of the B5 merge — descent is not identity (see *Equality, not descent*);
* **any unrelated or intervening `main` commit** — no admission path exists (see below).

That identity is **not stated here as a literal SHA and must never be predicted**: the parser
correction has not been written, let alone merged. The authorized unit must **derive the B5 merge
SHA from the completed Lifecycle B and prove the equality from the git object store**, exactly as
§F.1 requires of every other identity.

**Equality, not descent.** *Descends from* proves ancestry; it does not prove scope identity. Under a
descent-only rule any later commit on `main` would qualify while carrying bytes no review ever saw.
Ancestry remains **necessary history and explicitly insufficient authority**: the base must still
descend from this decision's own merge, which must itself be an ancestor of the **B5 implementation
merge** — but descent alone never qualifies a base.

**Any later `main` commit invalidates this grant for that base — with no admission path.** If `main`
carries **any** commit between the **B5 implementation merge** and the authorized unit's base, that unit
**may not proceed on the strength of this authorization**, full stop. There is **no** clause by which
such a commit may be admitted, absorbed, or cured inside `XASSET-0057` — not by separate
authorization, not by a closed identity transition, not by review. The **only** lawful route is a
**new, superseding rebinding authorization** filed and closed on its own.

This is deliberate, and it is the reviewer's own point: an `unless` admission path would reinstate
exactly the absolute-plus-exception structure this section withdrew. Once any intervening commit
exists the base **cannot** equal the **B5 implementation merge**, so an admission clause could only
ever contradict the equality rule or be inoperative. It is therefore **removed**, not narrowed.

The ordering this rule fixes is therefore exactly: this decision's merge → Lifecycle A's complete
closure (A1–A7) → Lifecycle B's complete closure (B1–B8), whose **B5 merge** is the sole qualifying
commit → the authorized rebinding's base, which **equals that B5 merge**. A rebinding based on this
decision's own merge — the state in which the §M defect is still live — **fails this condition**,
and that is precisely the case the earlier formulation wrongly permitted.

A base asserted from a task brief, a summary, or a moving reference is not a verified base.

**F.3 — Exact closed transitions, bound at both ends.** Every value the rebinding moves — each
rebound constant, each hash pin, each identity family member, each `LOAD_BEARING_RELPATHS` membership
change, and the lifecycle anchor itself — must be recorded as an **exact closed transition**: the old
value and the new value, both explicit, both independently proven from the git object store, with the
old value **preserved rather than overwritten** in the record. A value that moves without both ends
bound is drift wearing a rebinding's label.

For the load-bearing module specifically, the earlier "two ends, already known" table is
**withdrawn and replaced**. It named `12eab05e…604a5` as the transition's **New** end while §F.0
simultaneously forbids that identity from ever being bound — a direct contradiction. There are not
two ends; there are **four roles in one ordered chain**, and only the last is ever bound.

**The module identity chain — ordered, closed, and the single operative statement:**

| # | Role | Identity | Status |
|---|---|---|---|
| 1 | **Previously bound** | SHA-256 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`, blob `f71b08b4ebe95f161c57cdbb2a924748f13af02d` | The register's current bound end. **Retained, never discarded.** |
| 2 | **Vulnerable intermediate** | SHA-256 `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5`, blob `b5622f9e412afd604a11cde04317b79c5e57920a` | **Permanent negative / adverse history. NEVER a new bound end**, at any point in the chain, under any reading. |
| 3 | **Parser-corrected** | **Derived** at the parser correction's own merge, only after **both** its lifecycles close (§F.0.3). **Never predicted here.** | Intermediate. Never bound directly; it reaches the register only through role 4's own derivation and proof. |
| 4 | **Final stabilized post-rebinding** | **Derived** after every authorized edit of the rebinding has stabilized (§F.9). **Never predicted here.** | **The one and only new bound end.** |

**Every adjacent transition must be proved**, each end bound and independently derived from the git
object store: **1 → 2**, **2 → 3**, and **3 → 4**. Transition **1 → 2** is proved as *history*, not
as an adoption: role 2 is recorded as the state that existed and was refused, never as a value the
register moves to.

**The final register transition that the rebinding actually performs is `4ff28941…` → role 4**, and
it must be proved as a single closed transition with both ends explicit, the old value **preserved
rather than overwritten**.

**The final bound identity can never be `12eab05e…604a5`.** A rebinding whose bound module identity
equals role 2 **fails outright**, and so does one that binds role 3 without proving role 4, or that
predicts either derived value instead of deriving it.

The lifecycle anchor's three members transition from their present, independently verified values:

| Constant | Old — retained | New |
|---|---|---|
| `AUTHORIZING_DECISION` | `XASSET-0049` | the authorized unit's own decision identifier |
| `AUTHORIZING_PULL_REQUEST` | `349` | that unit's own GitHub-issued number, read back live |
| `REVIEWED_BASE_SHA` | `f052efad38e3d57e3e5615799ac3bcbebe83ff5f` | that unit's own verified base (§F.2) |

**F.4 — The smallest strictly necessary rebinding.** The authorized unit performs the **minimum**
change that reconciles the register with the merged bytes and makes its own newly bound identity
lawful. Convenience edits, opportunistic refactors, cleanups, adjacent improvements and
"while we are here" changes are **outside this grant**. If the unit finds a change it believes
necessary but which is not strictly required by the rebinding, it **stops and discloses**, and does
not decide the question silently.

**F.5 — Preserve the outcome surface's semantics.** The deterministic runner, the result
writer/serializer, the result validator, the universe closure validator, the deterministic derivation
surface, the canonical construction inputs, the frozen construction identities, their **ordering**,
the cardinality **680 / 48**, the aggregate universe hash `73c0965e…5224`, `comparison_subject_kind`,
`unordered_pair_id`, every gate, every disposition rule, the accepted B1 / B2 / B3 semantics, and
every protected portfolio and `risk_lane_boundary` `RISK` path are **preserved unchanged**. The
rebinding binds bytes; **it does not get to move meaning.** Any change to any of them requires its
**own separate, express** authorization and is outside this grant.

**F.6 — Bind canonical, enforcement, and *all* outcome-producing executable bytes.** This is
`XASSET-0030` §G.B's governing invariant, restated unchanged and not narrowed:

> **No outcome-producing executable code may be created, changed, or left outside the bound execution
> identity after the final rebinding and before `ATTEMPT_1`.**

Coverage must be proved by **exact byte identity**, never asserted by naming.

**F.7 — The trust boundary grows to cover the decisions governing the bound bytes; nothing is
removed.** `LOAD_BEARING_RELPATHS` may only be extended. Its present membership is **18**,
independently enumerated at this filing's own base, and it currently binds **eleven** governance
decisions — but **none** of the decisions that authorized and defined the parser semantics. Directly
verified at this base: `XASSET-0053`, `XASSET-0055`, `XASSET-0056` and `XASSET-0057` are all
**absent**. Binding the parser-corrected implementation bytes while leaving their governing decisions
outside the byte-identity boundary would protect the code and not the authority that defines what the
code must do — inconsistent with the direct-membership protection §F.6 asserts, and with the
`XASSET-0041`→`XASSET-0044` precedent, which added the jointly operative correction, implementation,
authorization and rebinding decisions together.

**Direct membership is therefore required**, at minimum, for every one of:

* `governance/decisions/XASSET-0053-…` — the accepted authorization for the parser correction;
* `governance/decisions/XASSET-0055-…` — the accepted verdict-boundary governance;
* `governance/decisions/XASSET-0056-…` — the accepted parser correction as implemented;
* `governance/decisions/XASSET-0057-…` — **this** decision;
* the future **rebinding** decision's own file; and
* **every** future accepted decision that authorizes or implements the §F.0 prerequisite parser
  correction — however many that turns out to be, including any bounded-correction filing in that
  chain.

**`XASSET-0054` remains excluded.** Its identifier is **consumed** and its pull request closed
unmerged, and no decision file for it exists on `main`. It may be admitted **only** if the authorized
unit produces **independent evidence that it is operative** — never on the strength of appearing in a
narrative, a related-decisions list, or this enumeration.

**Citation is not membership.** Naming a decision in `related_decisions`, quoting it, deriving from
it, asserting equivalence with it, inheriting from it, or referring to it in prose is **not** a
substitute for direct membership in `LOAD_BEARING_RELPATHS`. Only a path present in that tuple is
inside the byte-identity boundary.

**The final count is derived, never guessed.** This decision deliberately states **no** predicted
final membership figure: the parser-correction chain's own length is not yet known, so any number
named here would be invented. The authorized unit must **derive the exact final count and the exact
closed membership transition from the actual completed chain** — old membership and new membership
both explicit, both proven from the git object store, per §F.3 — and show that the count increased by
exactly the additions claimed. No existing member may be removed, swapped or traded away.

**F.8 — Canonical amendment in authorization language only.** The canonical artifacts may be amended
only to carry the rebinding's own authorization identity, only in lockstep with each other, and only
to the extent the rebinding requires. No gate, threshold, disposition rule, universe value or
evidence rule may move under cover of a canonical amendment. `stage_1_executability.executable`
stays `false`.

**F.9 — Recompute identities and pins once, and last.** Stale module identities and canonical pins
are recomputed exactly once, strictly after every authorized byte has stabilized, so no pin carried
forward from a superseded head survives into the merged unit.

**F.10 — Preserve all adverse history and every predecessor identity.** `XASSET-0044` and
`XASSET-0045` remain **not effective**; `XASSET-0043` remains **spent**; `XASSET-0040` remains spent
as `STOPPED_BEFORE_ATTESTATION`; `XASSET-0054` remains **consumed and never reused**. Every retained
negative pin — including the five superseded module identities `XASSET-0056` §H carried forward — is
preserved. Both failed merge-commit CI runs and both auditable stop records remain **immutable
adverse history**, and none may be re-run in place, relabelled successful, deleted, suppressed,
waived, or described as passing.

**F.11 — Validation the authorized unit must complete before it is offered for review.** Full
repository suite green; its own focused suite green; **adversarial mutation proofs** demonstrating
its own assertions are non-vacuous, with every probed path restored byte-identically and
SHA-256-verified independently of the probe harness; **exact-head CI** green; a **simulated
normal-merge verification** proving the merge tree is byte-identical to the accepted head's tree with
two ordered parents and zero conflicts; a **working-tree residue check** proving no probe, rehearsal
or scratch artifact survives; and an explicit **zero-write rehearsal** proving both authorization
predicates remain `False`, the lane remains `ABSENT`, `AUTHORIZATION_ROOT` is absent, no results
artifact exists, and `ATTEMPT_1` is intact, unclaimed and unconsumed.

**F.12 — One unit, one pull request, full lifecycle.** The rebinding decision and the rebinding
itself belong in the same coherent pull request, exactly as `XASSET-0037`, `XASSET-0044` and
`XASSET-0049` each were — splitting them produces a decision whose bound bytes do not yet exist, and
a rebinding whose governing text is not yet inside the identity it binds. That pull request must
complete the full seven-condition lifecycle in §J. A future session finding a concrete technical
reason to package this differently must **stop and disclose**, never decide it silently.

### G. Authority withheld — absolute

The grant in §E **does not extend to**, and the authorized unit **must not** perform:

- renewed readiness verification (`XASSET-0030` §G.B step 9 / `XASSET-0041` §I link 3);
- renewed drift verification (§G.B step 10 / link 4);
- **Step 11** in any part (§G.B step 11 / link 5) — `XASSET-0040` stays spent as a stop;
- generating, pre-staging or validating any **attestation**;
- creating `READY`, `CLAIMED` or `COMPLETED` lane state, writing `AUTHORIZATION_ROOT`, or writing the
  lane ledger;
- **arming** Stage 1, or setting `stage_1_executability.executable` to anything but `false`;
- **claiming** or consuming any part of `ATTEMPT_1`;
- evaluating any gate for any registered construction;
- executing Stage 1, or performing any results work;
- producing a `stage1_results.yaml`, a per-construction disposition, a cell outcome or a roll-up;
- acquiring market, fundamental, economic or Stage-2 data, or any Stage 2 work;
- creating any endpoint, bound, point, range, **percentage**, weight, rank, target or allocation;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades or orders;
- reading, listing, opening or substantively reusing any `risk_lane_boundary` protected `RISK` result;
- correcting the parser itself, or making any other non-rebinding change to the merged bytes —
  that correction is a **separate** unit, and §F.0 makes its completed lifecycle a mandatory
  **prerequisite** to the rebinding rather than part of it (§F.0, §M);
- reopening, re-deriving or re-arguing B1, B2 or B3, or `XASSET-0031`'s `G3`;
- resolving `XASSET-0024` §K.1, or amending `XASSET-0020` §E.1;
- consuming any part of `XASSET-0027` §P.1's reserved results PR.

**Links 3, 4 and 5 each require their own separate authority and their own complete lifecycle.**
Completing the rebinding authorizes the next link no more than a clean step-10 result authorized
step 11 — the inference `XASSET-0039` §K already foreclosed and `XASSET-0041` §I restated.

### H. Packaging — one authorization, one rebinding unit

This decision grants authority and performs no production mutation. The rebinding is a separate unit,
in a separate pull request, with its own decision record, its own review and its own lifecycle.

Its scope here is deliberately minimal: this decision file, its mechanism-based supporting test
module, the decision catalog row, and the factual `WS-0014` synchronization the register's own live
fields require. Advancing the register's shared `active_branch` / `active_pr` /
`last_verified_main_sha` fields necessarily re-anchors the coupled predecessor suite that pins them
onto this unit as the named successor, retaining the predecessor's own values as negative pins so the
fields stay bound at **both** ends; that is disclosed as consequential, not silent, and **no pinned
value is weakened or removed**.

### I. Fail-closed

Every unobtainable fact is an **error**, never silent agreement. Ambiguity, drift, a competing
worktree, a dirty tree, an unexpected open pull request, or any condition that would require
expanding this authority is a **stop**, not a judgement call. This applies to the authorized unit
exactly as it applied to this filing.

### J. Effectivity — the rebinding may not begin before this lifecycle closes

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own
   run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request authorizes nothing; a green PR-head CI
run does not; principal acceptance does not; merge does not; and post-merge verification without a
successful exact merge-commit CI run does not. **Only complete closure of all seven does.**

These seven mirror the repository's own committed definition —
`level1_stage1_execution_authorization.REQUIRED_LIFECYCLE_GATES`, a **six-element tuple**. The tuple
is not itself a repository path; the **module that contains it**,
`level1_stage1_execution_authorization.py`, is one of the eighteen load-bearing paths. **That module
is cited only and is byte-unchanged by this filing.** Conditions 5–7 are that tuple's last three
members; condition 2 is the exact-head discipline `OPS-0009` §6 applies to condition 1.
`XASSET-0035`'s own lifecycle omission — an enumeration naming four of six gates — is not repeated.

**Merging this decision performs no rebinding and arms nothing.**

### K. This filing can attain both green PR-head and green merge-commit CI

The condition both `XASSET-0044` and `XASSET-0045` permanently failed is condition 6, so this filing
states its attainability rather than assuming it. This unit adds one decision file, one test module,
one catalog row, and factual register and coupled-suite synchronization. It changes **no** production
module, **no** canonical artifact, **no** validator, **no** runner and **no** universe value. Its
supporting artifact proves its historical claims over **immutable commit ranges only**, and the full
repository suite is additionally run at a **simulated merged-`main` state where `HEAD` equals
`origin/main`** — the exact ref position that broke PR #345's assertions — before this filing is
offered for review.

No statement anywhere in this decision disclaims the ability to obtain successful merge-commit CI at
its own exact merge SHA. Such a statement would make §J.6 unreachable by construction, which is the
deadlock `XASSET-0045` shipped at its first reviewed head, and it is refused here in terms.

### L. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED` or `COMPLETED`
lane state; creates no `AUTHORIZATION_ROOT`; arms and executes no Stage 1; creates no Stage-1 runner,
result writer, serializer, result validator or `stage1_results.yaml`; consumes nothing of
`ATTEMPT_1`; **evaluates no gate for any construction and asserts no per-construction outcome**;
closes no gate on satisfaction and changes no gate's class, index, question, controlling authority or
failure disposition; **performs no rebinding**, corrects no parser, corrects no validator, extends no
`LOAD_BEARING_RELPATHS`, edits `level1_stage1_execution_authorization.py` **not at all**, and moves no
lifecycle anchor; **amends no canonical file and changes no hash pin, universe, cardinality,
`comparison_subject_kind`, `unordered_pair_id` or construction identity**; performs no part of
`XASSET-0030` §G.B steps 9, 10 or 11 and enters none of them; treats neither `XASSET-0044` nor
`XASSET-0045` as effective and revives neither `XASSET-0040` nor either stopped lifecycle; reuses
neither `XASSET-0054` nor any consumed identifier; consumes no part of `XASSET-0027` §P.1's reserved
results PR; acquires no market, fundamental, economic or Stage-2 data; resolves `XASSET-0024` §K.1
neither way and leaves `XASSET-0020` §E.1 unamended; reopens neither B1, B2 nor B3, and leaves
`XASSET-0031`'s `G3` untouched; grants no Stage 2 and no application authority; selects no sleeve and
creates no endpoint, bound, point, range, **percentage**, weight, rank, target or allocation; weakens
no validator and no test; **reads, lists, opens or references no `risk_lane_boundary` protected result
path** and reuses no `RISK` scenario, value, parameter, window or result; changes no `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap or margin
state; authorizes no chart, ladder, deployment, trade, order or brokerage action; and rewrites no
accepted history.

**Stage 1 remains UNARMED and NOT EXECUTABLE. The lane is ABSENT. `ATTEMPT_1` is intact, unclaimed
and unconsumed.**

### M. Disclosed — a reproduced, unresolved finding in the bytes this grant would have bound

A **post-merge** automated review, `5025021718`, was submitted by `chatgpt-codex-connector[bot]`
(`author_association: NONE`) at `2026-08-25T22:49:47Z` — **after** the merge at `22:47:15Z` and after
the post-merge verification at `22:48:42Z`, and **before** the final closure at `22:59:49Z`. It is
therefore **not** part of the accepted `XASSET-0056` lifecycle, and it did not participate in the
independent review chain that produced verdict `5024576065`.

It reports a residual prefix-tampering bypass. Under this repository's own standing guardrail —
*verify before acting on external review* — the claim was **executed against the merged bytes rather
than believed or dismissed**, read-only, through the pure parsing function alone:

| Probe | Result at merged `12eab05e…` |
|---|---|
| `FORMAL DISP` + U+039F + `SITION:` adverse first line, then a canonical approval | adverse line **skipped**; the later approval wins |
| U+0410 CYRILLIC CAPITAL A in the prefix, same shape | adverse line **skipped**; the later approval wins |
| U+0130 LATIN CAPITAL I WITH DOT in the prefix, same shape | adverse line **skipped**; the later approval wins |
| A homoglyph in the **verdict** rather than the prefix | correctly adverse — **no** bypass |
| A homoglyph prefix **alone**, with no later approval | returns no verdict — **no** direct authentication |

**The finding reproduces, and it is bounded.** The failure family is a *first-formal-line skip* when a
prefix-interior homoglyph's uppercase form remains non-ASCII, so the wide resemblance view deletes it
instead of recognising it. A tampered prefix still **cannot** directly authenticate.

Three consequences, stated rather than left implicit:

1. **This filing does not repair it, and is not authorized to.** Correcting the parser is a
   production change to a load-bearing path, and it needs its own authorization, its own review and
   its own lifecycle — the same route `XASSET-0053` §C and `XASSET-0055` §H established. **§F.0
   makes that correction a mandatory conjunctive prerequisite to any rebinding under this grant**,
   and §F.3 pins these defective bytes as **role 2** — permanent adverse history that may never
   be a bound end. **These three homoglyphs are reproduced EXAMPLES, not the defect's
   definition**: §F.0.1 records a measured sweep showing that deletion, ASCII substitution,
   insertion, transposition and confusable substitution across the prefix nearly all produce
   the same skip, so §F.0.2 requires the future correction to decide and prove a **total
   recognition boundary** rather than patch three code points.
2. **It does not make Stage 1 executable, and does not weaken any conclusion above.** The digest is
   stale, both predicates are `False`, the lane is `ABSENT`, and `ATTEMPT_1` is unconsumed.
3. **It is not disposed of by being disclosed, and disclosure is not a safety precondition.**
   The earlier text treated a parser correction as a *contingency* — something that, **if** it
   landed, would trip the drift rule. That was backwards, and it left the more dangerous case open:
   with **no** correction there is **no** intervening commit, so nothing fired, and the rebinding
   would have proceeded against the known-defective bytes. **§F.0 now makes the correction
   mandatory and §F.2 anchors the rebinding base to that correction's own merge.** A rebinding based
   on this decision's own merge — the state in which this defect is still live — **fails §F.2**.
   Any commit landing between the parser-correction merge and the rebinding base remains
   unadmitted drift and a **stop** unless separately authorized and bound at both ends under §F.3.

Nothing here rules on whether the reported behaviour should be corrected, or how. That question is
**open, unresolved, and outside this grant.**

## Rationale

The programme is in the state that most reliably produces an unauthorized action: a **known
defect**, a **known fix**, an **obvious next step**, and **no live authority for it**. `XASSET-0048`'s
grant is spent. `XASSET-0056` refused the successor three separate times — in §H, in §J, and in its
closure record — and each refusal was written by the unit best positioned to grant it. Treating any
of those as an implicit grant would convert a deliberate withholding into its opposite.

The base rule is stated as **equality** rather than descent for the reason `XASSET-0048` first gave
and this filing does not dilute: descent proves ancestry, not scope. Under a descent-only rule, any
future commit on `main` would qualify, and the rebinding would silently bind bytes no review of this
grant ever examined. The homoglyph finding in §M makes that risk concrete rather than theoretical —
a parser correction is a genuinely plausible next commit on `main`, and it is precisely the kind of
change a descent-only rule would let a rebinding absorb without review.

Closed transitions bound at both ends exist because a rebinding that overwrites a predecessor
identity destroys the evidence needed to detect a substitution. Preserving the old value costs one
line and converts an unfalsifiable claim into a checkable one.

Minimality (§F.4) is stated as an operative condition rather than a preference because a rebinding
touches the one module the whole fail-closed boundary rests on. The safe posture when scope is
uncertain is to stop and disclose, not to resolve it in the direction of more change.

## Alternatives considered

| Alternative | Rejected because |
|---|---|
| Treat `XASSET-0056` §H's recorded identity as the grant | §H's own final clause says it "is **not applied by anything here**," and §J forbids the successor outright. This is the exact inference the text forecloses. |
| Treat `XASSET-0048` §E as still live | It granted **exactly one** unit and `XASSET-0049` consumed it. Reusing a spent grant is the failure mode `XASSET-0043`'s spend record exists to prevent. |
| Repair the stale digest in this filing | That **is** the rebinding. Performing it here would make this decision its own authority — the regress `XASSET-0029` §E forbids. |
| Fold the §M parser finding into this grant | It is a production correction to a load-bearing path, not a rebinding. Bundling it would widen a minimal authorization into an unreviewed parser change. |
| Leave the §M correction as a *contingency* (the original text) | The drift rule fired only in the **safer** case — a fix landing first — and stayed silent in the **more dangerous** one, where no fix lands, nothing drifts, and the known-defective bytes become the accepted enforcement anchor. Disclosure is not a safety precondition. |
| Withdraw the rebinding grant entirely until a parser correction is effective | Equivalent in safety to §F.0's conjunctive prerequisite, but it discards the authority derivation, the closed-transition discipline and the boundary work, forcing them to be re-derived later from scratch. The prerequisite achieves the same refusal while keeping the analysis intact. |
| Keep an absolute "equal this decision's merge" rule plus a generic exception | A mandatory parser-correction merge **must** advance `main`, so the absolute rule and the required intervening merge cannot both hold. An absolute-plus-exception formulation reads as two rules and invites a successor to satisfy the wrong one. §F.2 states exactly one. |
| Predict the corrected module digest or the final `LOAD_BEARING_RELPATHS` count now | Neither exists. The correction is unwritten and the chain's length unknown, so any value stated here would be a guess wearing a pin's clothing — the exact failure §F.1 exists to prevent. Both are required to be **derived** from completed lifecycles. |
| Admit the parser-governing decisions by citation or equivalence rather than membership | Only a path inside `LOAD_BEARING_RELPATHS` is inside the byte-identity boundary. Citation protects nothing. |
| Say nothing about the §M finding | It reproduces in the bytes this grant would have bound, and §F.2 turns on whether a correction lands first. Silence would leave the authorized unit unable to recognise the drift condition. |
| Allow the base to merely descend from this merge | Descent admits arbitrary unreviewed bytes; §F.2's equality rule is the whole point. |
| Split the future decision and its rebinding across two PRs | Produces a decision whose bound bytes do not exist and a rebinding whose governing text sits outside the identity it binds. |

## Consequences

One future, separate, bounded pull request may perform the step-8-equivalent rebinding, under §F's
conditions and §G's withholdings, and **only after both**: this decision's own seven-condition
lifecycle closes in full, **and** the §F.0 parser-correction prerequisite is complete through all
eight of its own conditions. The grant is conditional, not standing.

Until then the load-bearing digest stays stale **by design**, `_verify_git_anchored_identity()` keeps
raising `enforcement drift`, both authorization predicates stay `False`, the lane stays `ABSENT`,
`AUTHORIZATION_ROOT` stays absent, no results artifact exists, `ATTEMPT_1` stays intact and
unconsumed, the universe stays **680 / 48 / `73c0965e…5224`**, and **Stage 1 remains UNARMED and NOT
EXECUTABLE**.

The §M finding remains open and unresolved. It is disclosed, reproduced and bounded here; it is
neither repaired nor authorized to be repaired by this decision. What **has** changed is its
standing: it is no longer merely disclosed but is a **hard blocking prerequisite** — the defective
identity `12eab05e…604a5` is a permanent negative pin that no rebinding under this grant may ever
bind, and the rebinding's own base is anchored to the correction's merge rather than to this one's.
