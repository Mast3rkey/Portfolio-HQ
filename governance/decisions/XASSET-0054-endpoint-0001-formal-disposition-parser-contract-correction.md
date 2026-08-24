---
decision_id: XASSET-0054
date: 2026-08-24
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_parser_contract_correction.py
---

## Context

**This is an implementation unit, not an authorization filing.** `XASSET-0053` already supplies
the authority, and this decision records the exact scope and lifecycle of the single correction
it authorized. Nothing here grants, widens, or re-derives authority.

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as
authoritative over every fact supplied to this session. Every value was independently
re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `683c324629544a84d2cf75ebca37325e3375c479` |
| Later commits on `main` | **none** |
| Merge structure | parents `cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6` → `90a1f45426b9f1e6aa9a568985d8eacc1cfd97fc`, no third; tree `95f74cc76f75b7be151fe712aecbbc77688bb378` |
| Accepted-head → merge diff | **empty** — zero drift at merge |
| PR #354 | closed, **merged**, not draft; clean exact-head review [`5005144938`](https://github.com/Mast3rkey/Portfolio-HQ/pull/354#pullrequestreview-5005144938); principal acceptance [`#issuecomment-5391819520`](https://github.com/Mast3rkey/Portfolio-HQ/pull/354#issuecomment-5391819520); post-merge verification [`#issuecomment-5391836818`](https://github.com/Mast3rkey/Portfolio-HQ/pull/354#issuecomment-5391836818) |
| Exact-merge CI | run `32699941813` / job `97349267177`, both `head_sha` exactly the merge SHA, `completed` / `success`, all ten steps; log independently decoded — `11929 passed`, zero `FAILED`, zero traceback, zero `##[error]` |
| `XASSET-0053` lifecycle closure | [`#issuecomment-5391908055`](https://github.com/Mast3rkey/Portfolio-HQ/pull/354#issuecomment-5391908055), posted `07:14:24Z`, strictly after CI completion `07:12:51Z` — all seven §J conditions closed, **`XASSET-0053` EFFECTIVE** |
| `XASSET-0053`'s one correction grant | **unexercised at preflight** — module blob still `f71b08b4ebe95f161c57cdbb2a924748f13af02d`, parser signature still `str | None`, exactly three call sites |
| Open pull requests | **zero** |
| Worktree / stash / worktrees | clean; no stash; exactly one worktree; no competing mutation lane |
| Lane state · `AUTHORIZATION_ROOT` · `stage1_results.yaml` | `ABSENT` · absent · absent |
| `ATTEMPT_1` | intact, unclaimed, unconsumed |
| `new_execution_is_authorized()` · `active_execution_is_authorized()` | **`False`** · **`False`** |
| Frozen universe | **680** constructions / **48** cells |
| `LOAD_BEARING_RELPATHS` | **18**, unique, `level1_stage1_execution_authorization.py` first |
| Decision catalog | **155** entries, `XASSET-0053` last, `issues == ()` |
| Register | exactly **zero** `priority: primary` workstreams; `WS-0014` at `proposed` / `secondary` |
| Next unused identifier | **`XASSET-0054`** — derived, not assumed (below) |

### Identifier derivation

`XASSET-0054` was derived from the complete repository and every reachable commit rather than
assumed from sequence: the committed catalog (an authoritative in-tree index of all 155 decisions,
complete regardless of clone depth) carries `XASSET-0001` through `XASSET-0053` contiguously with
no gaps and nothing above; the decisions directory, the register, the tracked tree and all
reachable history agree.

Two apparent hits were **investigated rather than assumed away**. `XASSET-0099` (working tree,
`test_level1_sleeve_synthesis_validator.py`) and `XASSET-9999` (history) are both synthetic
negative-case fixtures asserting a closed `governing_decision` vocabulary — neither is a decision.

**Two disclosed limitations.** This checkout is a shallow clone (`git rev-parse
--is-shallow-repository` returns `true`; oldest reachable commit `9d70f592…`, 2026-08-11), and
`api.github.com/search/code` returned HTTP 403 under this environment's proxy policy, so code
search could not supplement it. The derivation therefore rests on the committed catalog plus the
tracked tree, the decisions directory, the register, and reachable history — recorded as a
limitation, not presented as a complete-history guarantee.

### The defect, reproduced before anything was edited

Read-only. No authorization state was written and no lane was created.

`parse_formal_disposition()` returned `str | None`, so **one** value carried **two** meanings:

* **ABSENT** — the body carries no formal-looking disposition line at all; and
* **MALFORMED / UNSUPPORTED** — a formal-looking line **was** found and refused.

| | Reproduced result |
|---|---|
| **R1** | PR #349 review `5000581301`'s own formal line is a precisely balanced whole-line bold form and parsed to `None` — **unparseable** |
| **R2** | a genuinely absent body and a malformed body both parsed to `None` — **indistinguishable** |
| **R3** | the **real** `_verify_selected_review_is_final()` accepted **both** as non-adverse under a native `APPROVED` state (`errors=0` for each); native `CHANGES_REQUESTED` still rejected independently, as a control |
| **R4** | a naive parser-only repair, executed **in memory only**, returned the approving verdict for a body whose first formal-looking line is `## FORMAL DISPOSITION: CHANGES REQUIRED` — **actively regressing safety** |

**One fixture error, caught and corrected before anything was built on it.** The first reproduction
script tested the body's *first* line. That line is `## Independent exact-head DELTA review — PR
#349` — a heading, not the formal line — which made R1 report the wrong shape and made R4's fixture
wrong. The script was corrected to locate the real formal line (line **8** of the body) before any
conclusion was drawn. It is recorded here because a reproduction that was quietly wrong once is
worth stating plainly, not smoothing over.

**R4 is the reason a parser-only repair was insufficient.** It fixes R1 while introducing a worse
defect: the recorded adverse line is *skipped* so a later approval wins. The distinguishing value
had to exist. That is exactly what `XASSET-0053` §C item 2 anticipated.

## Decision

### A. Determination — `FORMAL_DISPOSITION_PARSER_CONTRACT_CORRECTION_IMPLEMENTED`

The single correction `XASSET-0053` §C authorized is implemented, in exactly its exhaustive
permitted set and nothing else. `XASSET-0053` is this unit's **sole** authority.

### B. What changed inside `level1_stage1_execution_authorization.py`

Exactly the four permitted things, and nothing else.

**1 — `parse_formal_disposition()` modified.** It now returns one of three non-interchangeable
outcomes: a `str` verdict exactly as written; `MALFORMED_FORMAL_DISPOSITION`; or `None` for ABSENT.

**2 — The smallest result representation: one sentinel.** `MALFORMED_FORMAL_DISPOSITION`, a
module-level instance of a `__slots__`-only class carrying no behaviour beyond `__repr__` and
`__bool__`. One added value — the narrowest of the three routes §C item 2 permits.

**3 — Exactly one narrow helper.** `_formal_disposition_line_verdict(stripped)` classifies **one**
already-stripped line. One positional argument; no varargs, keyword-only arguments, or defaults; no
state; no iteration over a body; no regular expressions; no I/O; no `global`/`nonlocal`. It answers
one question about one line. **It is not a parsing framework**, and this is asserted structurally by
test, not claimed in prose.

**4 — The minimum necessary lines in the three named consumers.**

| Consumer | Change | ABSENT policy |
|---|---|---|
| `_derive_pr337_actor_ratification()` | **no logic change** — it reads the parser through an inequality against `APPROVING_REVIEW_DISPOSITION`, so both new outcomes already fail closed; one clarifying comment records that this was **checked, not assumed** | preserved exactly |
| `verify_lifecycle_against_truth()` | one added branch, so MALFORMED reports its own accurate message instead of being described as an adverse verdict | message and policy byte-preserved |
| `_verify_selected_review_is_final()` | one added branch, placed **before** the approving check | ABSENT branch, including the `NATIVE_NON_ADVERSE_REVIEW_STATES` rescue, preserved exactly |

The `_verify_selected_review_is_final()` branch order is deliberate and is asserted by test:
`NATIVE_ADVERSE` → **MALFORMED** → approving → ABSENT. Placing MALFORMED before the approving check
makes "never rescued by a native `APPROVED` state, never skipped for a later approval" **structural
rather than incidental**, and a test proves the `NATIVE_NON_ADVERSE_REVIEW_STATES` rescue appears
only inside the ABSENT branch.

### C. Behaviour, against `XASSET-0053` §D

| Clause | Behaviour |
|---|---|
| D.1 | the plain canonical line is accepted unchanged |
| D.2 | **only** the precisely balanced, whole-line bold wrapper is additionally accepted |
| D.3 | only the wrapper is stripped; the verdict is never normalized, replaced, canonicalized or fuzzy-matched — a near-miss verdict is returned **verbatim** and never snapped to the approval |
| D.4 | the first formal-disposition line still governs |
| D.5 | comparison with `APPROVING_REVIEW_DISPOSITION` stays exact |
| D.6 | native `CHANGES_REQUESTED` remains independently adverse whatever the body says |
| D.7 | plain **and** balanced-bold `CHANGES REQUIRED` both parse as adverse |
| D.8 | approval text as substring, quotation, heading, blockquote or code sample yields **no** verdict |
| D.9 | leading operative prose is MALFORMED |
| D.10 | unbalanced, nested, partial, repeated and ambiguous emphasis all fail closed |
| D.11 | every surrounding protection is unchanged; the fingerprint gate is proven untouched by its own test |
| D.16 | exactly two accepted forms; **twenty** decoration classes each classify MALFORMED |
| D.17 | an unsupported formal-looking line **stops classification** and is never skipped |
| D.19 | ABSENT and MALFORMED are separately observable at **all three** consumers, and MALFORMED fails closed even under native `APPROVED` |

### D. One disclosed behaviour that is fail-closed by a different mechanism

**Trailing operative prose.** A line such as `FORMAL DISPOSITION: <approval> and see below` is not
classified MALFORMED; the separator rule yields a verdict string that is **not** equal to
`APPROVING_REVIEW_DISPOSITION`, so all three consumers fail closed on the inequality instead. The
safety outcome is identical, the mechanism differs, and it is recorded rather than papered over.

The pre-existing finding-count separator rule (`—`, `--`, ` - `, `|`) is **unchanged**. Review
`5000581301`'s own line depends on it, and altering it would be an unrelated behaviour change §C
forbids. It is noted here as pre-existing and deliberately out of scope.

### E. Tests exercise the real production paths

`test_level1_stage1_parser_contract_correction.py` drives all three consumers on their own
authenticated seams, reusing the two established harnesses rather than inventing a third, weaker
stand-in:

* `_verify_selected_review_is_final()` — the real function, with a real review set;
* `verify_lifecycle_against_truth()` — a real authorization payload; and
* `_derive_pr337_actor_ratification()` — the real PR #337 / #341 fixture universe, with a
  fingerprint-repinning helper so the disposition gate proves **its own** mechanism, plus a
  companion test proving the **separate** byte-exact fingerprint gate is untouched by this
  correction.

Every `XASSET-0053` §D.18 and §D.20 case is covered as its own directly-exercised test, including
non-vacuity proofs: the baseline ratification fixture really does ratify, the naive skip-semantics
repair really would have flipped the verdict, and the module really did change.

### F. Re-anchoring the `XASSET-0053` suite — not relaxation

`XASSET-0053`'s own suite is a **pre-correction snapshot**. Eleven assertions read the **working
tree** where they meant *"the module as `XASSET-0053` found and left it"*. Each was re-pointed at a
**closed, immutable anchor** — the base commit, the accepted head, or `XASSET-0053`'s own
lifecycle-closing merge — following the `XASSET-0044` / `XASSET-0043` precedent already applied to
the `XASSET-0042` suite.

**Nothing was deleted, skipped, `xfail`ed, or relaxed.** Every one still compares real bytes, and
against an immutable anchor none can be made to pass by editing a file. Where a live comparison
still had teeth it was **kept and only narrowed to the single lawfully authorized path**, so the
other seventeen `LOAD_BEARING_RELPATHS`, the seven protected portfolio paths and both canonical pins
remain compared **live**. The load-bearing and diff guards each gained a second, immutable half, so
they are strictly stronger than before.

One guard needed more than a re-point. `test_this_decision_is_not_inserted_into_the_mechanism`
asserted `"XASSET-0053" not in src`, which the authorized correction makes false the moment it cites
its authority — and citing the authorizing decision is this module's **universal** convention:
**fifteen** other decision IDs already appear there. It was re-anchored to the closed merge **and**
given a live half checking the property it was really for — the identifier must never enter the
**executable** mechanism, i.e. a bound constant or any operative (non-docstring) string literal,
now checked by AST.

### G. No operational authority is restored, and the pin is deliberately left stale

This correction repairs an authentication **contract**. It arms nothing.

No rebinding. No canonical re-pinning. No readiness or drift verification. No attestation. No lane
creation. No arming. No claim. No execution. No results. No portfolio percentage. No allocation. No
trade.

| Property | State |
|---|---|
| `new_execution_is_authorized()` | **`False`** |
| `active_execution_is_authorized()` | **`False`** |
| `claimed_execution_is_authorized()` | **`False`** |
| `stage_1_executability.executable` | **`false`** |
| Lane state · `AUTHORIZATION_ROOT` | `ABSENT` · absent |
| `ATTEMPT_1` | intact, **unclaimed**, unconsumed |
| `stage1_results.yaml` | absent |
| `AUTHORIZING_DECISION` · `AUTHORIZING_PULL_REQUEST` · `REVIEWED_BASE_SHA` | `XASSET-0049` · `349` · `f052efad…` — unmoved |
| `XASSET-0027` §P.1 | one, **unspent** |

**The module's bound load-bearing digest is NOT re-pinned here.** Re-pinning is the separately
authorized step-8-equivalent rebinding unit's work, and the drift this correction introduces is the
**designed fail-closed hand-off** to it. The corrected identity is recorded below so that unit
receives it exactly.

### H. Corrected module identity, for the separately authorized rebinding unit

```
FINAL_CORRECTED_MODULE_SHA256: dfc081b7179ab1c77dd06c374a29be5c3edc4a342f39be4e966c28cb5f214507
```

Blob `271e8ca60a76a9c7b8b84c5411360d217661f55d`.

The **superseded** pre-correction identity is retained as history and is **not** presented as
current: SHA-256 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`, blob
`f71b08b4ebe95f161c57cdbb2a924748f13af02d`.

### I. This unit, and this filing, **must not**:

- perform, arm, claim, execute, or complete any part of ENDPOINT-0001 Stage 1;
- create an attestation, `AUTHORIZATION_ROOT`, lane state, `READY`, claim, or completion record;
- consume, claim, or touch `ATTEMPT_1`;
- **perform a step-8-equivalent rebinding**, or re-pin any load-bearing or canonical digest;
- repeat readiness verification or a renewed drift check;
- authorize or perform link 5, or any successor unit of any kind;
- edit any historical review, comment, acceptance record, or closure record;
- modify any runner, result validator, universe module, canonical artifact, or protected portfolio
  path;
- weaken any adverse-review rejection, any validator, or any test;
- change any construction identity, universe membership, ordering, or cardinality;
- acquire market, fundamental, economic, or Stage-2 data;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` artifact; or
- create any endpoint, bound, point, range, percentage, weight, rank, target, ladder, or trade.

### J. This unit's own pull request

Pull request **#355**, opened as a draft against `main` at
`683c324629544a84d2cf75ebca37325e3375c479`. The number was **never predicted**: it was committed
as the structurally impossible sentinel `-54`, read back from the live GitHub API after the draft
was opened, and bound in a fast-forward follow-up commit. No history was force-pushed, amended,
squashed, or rewritten.

### K. Lifecycle

Effective only on complete closure of all seven conditions, in order: independent **FULL**
exact-head review under `OPS-0007` §1; any bounded correction and exact-head re-review; principal
exact-head acceptance; normal merge; immediate post-merge verification; successful merge-commit CI
whose `head_sha` is the exact merge SHA; and final post-CI verification and lifecycle closure.

## Rationale

The authority question was already settled. What this unit had to get right was *smallness under a
real hazard*: the obvious repair — teach the parser to strip a bold wrapper — fixes the visible
symptom and silently makes the system **less** safe, because it skips a refused line so a later,
better-formed approval wins. R4 demonstrates that rather than asserting it.

The sentinel is the narrowest thing that makes the hazard expressible. One value, no grammar, no
configuration, no second parser. The single helper earns its place by making the accepted grammar
checkable in one place; it is bounded by structure, not by promise, and its boundedness is asserted
by AST test rather than by comment.

The consumer changes were kept genuinely minimal, including the case where minimal meant **zero**:
`_derive_pr337_actor_ratification()` reads the parser through an inequality, so both new outcomes
already fail closed. Writing a branch there would have been redundant code justified by symmetry.
What it got instead is a comment recording that the coverage was verified, and a test proving it.

Re-anchoring `XASSET-0053`'s suite deserved care, because "the authorized change broke the previous
filing's tests" is exactly the moment a suite gets quietly weakened. It was not. Each assertion was
re-pointed at the immutable anchor it always meant, live comparisons were kept wherever they still
had teeth, and two guards came out strictly stronger than they went in.

## Alternatives considered

**A pure parser-only repair.** Rejected — R4 shows it regresses safety. This is the alternative
`XASSET-0053` §B.9 already reproduced as insufficient, re-confirmed here against the real module.

**A typed result object (`ParsedDisposition(kind, verdict)`).** Rejected as larger than necessary.
Every consumer needs to distinguish exactly three outcomes, two of which are already representable
(`str`, `None`). One sentinel adds the third without changing how the other two are read, and
without touching a single existing comparison.

**Two helpers — one to unwrap, one to classify.** Rejected: §C caps new helpers at one, and one
suffices. Unwrapping and classifying are the same question about the same line.

**Rewriting `_derive_pr337_actor_ratification()` for symmetry.** Rejected. §C authorizes the
*minimum necessary* lines, and the minimum there is none.

**Deleting, `xfail`ing, or loosening the eleven `XASSET-0053` assertions.** Rejected outright. They
are re-anchored to immutable anchors instead, and every one still compares real bytes.

**Re-pinning the module's load-bearing digest here.** Rejected — §I forbids it, and the resulting
drift is the intended fail-closed hand-off, not an oversight.

## Consequences

Review `5000581301`'s shape now authenticates, so the substantive blocker that stopped
`XASSET-0052`'s link-5 unit at `STOPPED_BEFORE_ATTESTATION` is repaired at the contract level.

**That does not arm anything.** The correction changes load-bearing bytes, so the bound digest is
now stale by design, and Stage 1 remains **UNARMED** and **NOT EXECUTABLE** until the separately
authorized step-8-equivalent rebinding unit runs, an external one-shot pre-execution attestation is
produced, and the lane lawfully reaches `READY`. Each of those is its own separate authority.
`ATTEMPT_1` remains intact, unclaimed, and unconsumed.

Every historical GitHub record — review `5000581301` included — is unedited. The durable record is
evidence, not a repair surface.
