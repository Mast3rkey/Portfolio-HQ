---
decision_id: XASSET-0056
date: 2026-08-25
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, XASSET-0055, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_formal_disposition_parser_correction.py
---

## Context

This is the **single replacement parser-correction implementation** authorized by `XASSET-0055`
§H, implementing the correction `XASSET-0053` §C authorizes, within that §C permitted set
unchanged. It supersedes and replaces PR #355, which is closed unmerged and whose identifier
`XASSET-0054` remains **consumed** and is not reused.

### Live preflight

Every anchor was independently re-resolved before anything was edited, and nothing was taken on
the authorizing task's word:

| Fact | Verified |
|---|---|
| Base | `29e4969885970d942a5acecc1424fb2e2b080d60` — GitHub `main`, `origin/main`, local `main`, the working checkout and this branch's base all equal it |
| PR #356 | **merged**, closed, by GitHub's **normal merge**: exactly 2 parents, parent 1 `683c324629544a84d2cf75ebca37325e3375c479`, parent 2 `199555351c16e7066822aad175663eec60f15f63`; merge tree `fe36da825841b42ea90c22fedc1d6c660d72c8ca` **byte-identical** to the accepted head's tree |
| Lifecycle | all **seven** `XASSET-0055` §L conditions durably closed — review `5011963664` at the exact head (0/0/0/0, so no correction round was owed), acceptance `issuecomment-5401019956`, post-merge verification `issuecomment-5401096085`, merge-commit CI run `32774900386` / job `97583599765` with `head_sha` **equal to the exact merge SHA**, closure `issuecomment-5401242275` |
| Open pull requests | **zero** |
| Worktree | clean, sole worktree, no competing mutation lane |
| The §H grant | **unexercised** — the module is byte-identical to its base and the parser still carries its uncorrected contract |
| Stage 1 | **UNARMED and NOT EXECUTABLE**; both predicates `False`; lane `ABSENT`; `AUTHORIZATION_ROOT`, claim, completion and ledger all **absent**; `ATTEMPT_1` intact, unclaimed, unconsumed; no `stage1_results.yaml` anywhere |
| Module identity at base | SHA-256 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`, blob `f71b08b4ebe95f161c57cdbb2a924748f13af02d` — matching exactly |

One anchor needed reconciliation and is disclosed rather than glossed: local `refs/heads/main`
was a **stale bookmark** at `cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6` — **0 ahead, 11 behind**,
a strict ancestor, with a reflog showing it was only ever created from `origin/main` and never
written to. It carried no local-only commit and was fast-forwarded to the base before work began.

### Identifier derivation

`XASSET-0056` was derived, never assumed, from all five required sources: the live catalog
(reaching `XASSET-0055`), `governance/decisions/`, `operations/WORKSTREAMS.yaml`, the complete
reachable history after `git fetch --unshallow` (1 133 commits), and all **607** remote refs.
`XASSET-0054` appears in history, in the register and on a preserved remote branch but **never in
the catalog** — it is consumed by closed-unmerged PR #355 and is not reused here.

### The defects, reproduced before anything was edited

All seven were reproduced read-only against the exact base, and the load-bearing one was
reproduced at its **real consumer seam**, not against the parser alone:

1. Review `5000581301`'s legitimate whole-line bold form returned `None`.
2. `str | None` could not separate ABSENT from MALFORMED / UNSUPPORTED — both were `None`.
3. Arbitrary separator suffixes were **discarded unread**: `<approval> | CHANGES REQUIRED`
   authenticated as the approval.
4. The mixed-separator / tuple-order bypass authenticated
   `<approval> | CHANGES REQUIRED — 0 BLOCKING`.
5. Mixed-case and lower-case canonical verdicts returned their exact original text — the
   behaviour PR #355 regressed and `XASSET-0055` §D restores.
6. Approval followed by undelimited text already failed by whole-verdict inequality.
7. All three consumers hold **different** ABSENT policies, and in
   `_verify_selected_review_is_final()` a native `APPROVED` state rescued a `None` verdict —
   rescuing MALFORMED exactly as it rescued ABSENT.

**A test expectation was never used as authority for a production change.** `XASSET-0055` and
`XASSET-0053` are the authority throughout; §D of `XASSET-0055` records that rule and this filing
observes it.

## Decision

### A. Determination — `FORMAL_DISPOSITION_PARSER_CORRECTION_IMPLEMENTED`

The correction is implemented within the `XASSET-0053` §C permitted set, satisfying every clause
of §D and every requirement of `XASSET-0055` §C, §D, §E and §I.

### B. What changed in production — exhaustively

Exactly **four** existing top-level definitions in `level1_stage1_execution_authorization.py`
changed, and exactly **one** was added. Nothing else in the module, and no other production file,
changed at all. This is asserted mechanically by AST comparison against the base, not claimed.

1. `parse_formal_disposition()`.
2. The minimal result representation: **one sentinel**, `MALFORMED_FORMAL_DISPOSITION`, with its
   private singleton type `_MalformedFormalDisposition`. `None` continues to mean ABSENT, so every
   consumer's existing ABSENT policy is preserved **literally** rather than re-derived.
3. **Zero new helpers.** The ceiling §C sets is one; the helper is "an option, not an
   entitlement", and the whole correction fits inside `parse_formal_disposition()` without one.
   Zero is strictly smaller than the permitted maximum.
4. The minimum necessary lines in exactly the three named consumers —
   `_derive_pr337_actor_ratification()`, `verify_lifecycle_against_truth()` and
   `_verify_selected_review_is_final()`.

**No fourth call site. No second helper. No general parsing framework. No other existing
production function changed.** `NATIVE_ADVERSE_REVIEW_STATES`, `NATIVE_NON_ADVERSE_REVIEW_STATES`,
`APPROVING_REVIEW_DISPOSITION`, `FORMAL_DISPOSITION_PREFIX`, `LOAD_BEARING_RELPATHS`,
`AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST` and `REVIEWED_BASE_SHA` are byte-identical to
the base. Review selection, chronology, pagination, exhaustion, reviewer identity, attribution,
lifecycle evidence, fingerprinting, gates, universe, runner, validator and attestation behaviour
are all untouched.

### C. The parser's governed behaviour

* **Exactly two accepted wrapper forms** (§D.2, §D.16): the plain canonical line, and a precisely
  balanced **whole-line** Markdown-bold pair whose enclosed text is itself a plain canonical line
  and carries no further `*`.
* **First-formal-line governance preserved** (§D.4), and a formal-looking line that is not in an
  accepted form **stops the parse** rather than being skipped (§D.17).
* **The verdict is returned verbatim** — never normalized, coerced, canonicalized, fuzzy-matched,
  truncated or case-folded (§D.3), and the vocabulary stays **open**.
* **Exact comparison** against `APPROVING_REVIEW_DISPOSITION` over the **whole** verdict (§D.5,
  `XASSET-0055` §C.2), so appended text can never authenticate — a property of exact equality.
* **Undelimited trailing text is rejected by inequality**, not falsely classified MALFORMED
  (`XASSET-0055` §C.4).
* **Every recognized separator suffix is validated** as `count ( "/" count )*` where
  `count := digits SPACE CATEGORY` and `CATEGORY ∈ {BLOCKING, MAJOR, MINOR, NOTE}`; an arbitrary
  suffix is MALFORMED (§E.1, §E.2).
* **The earliest recognized separator governs**, never tuple order (§E.3).
* **The recognized separator tuple is byte-unchanged** (§E.4): `"—"`, `"--"`, `" - "`, `"|"`.
* **The lower-case heuristic is absent and prohibited** (`XASSET-0055` §D). Mixed-case and
  lower-case canonical verdicts return exactly as written. No case, length or word-count rule
  exists anywhere in the parser, asserted against the shipped source.

### D. The ABSENT / MALFORMED distinction, enforced at all three consumers

* `_derive_pr337_actor_ratification()` — refuses MALFORMED **explicitly**, before and
  independently of the inequality check, so refusal is not an incidental side effect.
* `verify_lifecycle_against_truth()` — MALFORMED gets its **own distinct error**; the ABSENT
  branch is preserved **verbatim**, byte for byte.
* `_verify_selected_review_is_final()` — MALFORMED fails closed **before any native-state
  branch**, so a native `APPROVED` can never rescue it (§D.20.2), while a genuinely ABSENT
  disposition with a native `APPROVED` state keeps its existing non-adverse policy exactly
  (§D.20.1). Ordering is asserted structurally, not merely by behaviour.

### E. One disclosed behavioural addition beyond the demonstrated defect

`XASSET-0053` §D.17 and §D.18.7 require **code-fenced** lines to fail closed. At the base a fenced
line parsed as an ordinary canonical line, so a fenced approval authenticated. Closing this needs
one boolean of line context inside the existing loop — no helper, no state machine, no framework —
and it is implemented. It is disclosed here as a real behavioural change rather than folded
silently into "the correction", because it fixes a shape the demonstrated defect did not itself
exhibit. A fenced sample **below** an operative first line is unaffected, which is the real shape
of review `5004478133`.

### F. Blast radius, measured rather than asserted

Every real lifecycle review body was parsed under both the base module and the corrected module.
**Exactly one changed**: review `5000581301`, from `None` to its correct approving verdict — the
defect this correction exists to fix. Reviews `4974291044`, `5004478133` (which itself quotes a
fenced disposition sample), `5004859164`, `5005144938` and `5011963664` parse **identically**.

### G. The predecessor suites were re-anchored, never weakened

Advancing this unit necessarily falsified assertions in three predecessor suites: `XASSET-0053`'s
own suite (11), `XASSET-0055`'s own suite (5), and the PR #337 actor-evidence suite (1). Each was
**re-anchored onto an immutable closed lifecycle fact** — its own unit's merge SHA — rather than
against a live working tree that a lawful successor now also occupies:

* `XASSET-0053`'s suite anchors at `683c324629544a84d2cf75ebca37325e3375c479` (PR #354's merge).
* `XASSET-0055`'s suite anchors at `29e4969885970d942a5acecc1424fb2e2b080d60` (PR #356's merge),
  and its `_changed_paths()` now measures its own closed `base..merge` range, which contains
  exactly the 15 files that PR reported.
* The defect-reproduction assertions were **not** relaxed to text matches: the historical module
  is imported and its parser executed, so the reproduction stays behavioural.
* **Every superseded value is retained as a negative pin**, so each field is bound at both ends
  and a silent revert of the authorized correction still fails.
* The PR #337 suite deliberately reads the **live** module digest so it fails when the register
  goes stale; the register therefore records the new identity, with the superseded identity
  retained beside it.

**Nothing was deleted, skipped, `xfail`ed, weakened, or replaced by a looser presence check.**
Every re-anchored suite's assertion count only grew, and no re-anchored suite is a
`LOAD_BEARING_RELPATHS` entry, so the module's trust boundary is untouched.

### H. The load-bearing digest is now stale — by design, and NOT repaired

`level1_stage1_execution_authorization.py` is `LOAD_BEARING_RELPATHS[0]`. This correction changes
it, so its bound digest is stale:

| | |
|---|---|
| At the bound merge | SHA-256 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`, blob `f71b08b4ebe95f161c57cdbb2a924748f13af02d` |
| Derived here | SHA-256 `88ada2e2ffaa0131a155e22019ee96b70bc9a0670550e4ca4a22726b9b54bcd9`, blob `c207aa911ed689eed122c28a4b0619ed57a22a4b` |

That divergence is the **fail-closed hand-off** `XASSET-0055` §J describes. `_verify_git_anchored_identity()`
is byte-identical to the base and still raises `enforcement drift`. Both authorization predicates
remain `False` and Stage 1 remains **NOT EXECUTABLE**.

**This filing performs no rebinding and no re-pinning.** `AUTHORIZING_DECISION` stays
`XASSET-0049`, `AUTHORIZING_PULL_REQUEST` stays `349`, `REVIEWED_BASE_SHA` stays
`f052efad38e3d57e3e5615799ac3bcbebe83ff5f`. The newly derived identity above is **recorded for**
a later, separately authorized step-8-equivalent rebinding unit, and is not applied by anything
here.

### I. Validation

| Check | Result |
|---|---|
| New adversarial suite | **206 tests**, all passing |
| Non-vacuity against the exact base | **88 of 206 fail** at the unchanged base `29e4969…` |
| Mutation probes | **19 / 19 caught, 0 missed** — every probed file restored byte-identically and SHA-256-verified |
| Real-review blast radius | 6 real bodies parsed under both modules; **exactly one** changes |
| Zero-write rehearsal | all three consumer paths exercised; no lane record, no `AUTHORIZATION_ROOT`, no attestation, no claim, no results file; both predicates still `False` |
| Re-anchored predecessor suites | assertion counts only grew; no deletion, skip, `xfail` or relaxation |

### J. This decision, and this implementation, **must not** and do not:

- perform, arm, claim, execute or complete any part of ENDPOINT-0001 Stage 1;
- create an attestation, `AUTHORIZATION_ROOT`, lane state, `READY`, claim or completion record;
- consume, claim or touch `ATTEMPT_1`;
- **perform a step-8-equivalent rebinding**, or re-pin any load-bearing or canonical digest;
- perform readiness verification or a drift check;
- authorize or perform link 5, or any successor unit of any kind;
- edit any historical review, comment, acceptance record or closure record;
- modify any runner, result validator, universe module, canonical artifact or protected
  portfolio path;
- weaken any adverse-review rejection, any validator or any test;
- change any construction identity, universe membership, ordering or cardinality;
- acquire market, fundamental, economic or Stage-2 data;
- read, list, open or substantively reuse any `risk_lane_boundary` protected `RISK` artifact; or
- create any endpoint, bound, point, range, percentage, weight, rank, target, ladder or trade.

### K. Lifecycle

Effective only on complete closure of all seven conditions, in order: independent **FULL**
exact-head review under `OPS-0007` §1; any bounded correction and exact-head re-review; principal
exact-head acceptance; normal merge; immediate post-merge verification; successful merge-commit CI
whose `head_sha` is the exact merge SHA; and final post-CI verification and lifecycle closure.

**This filing does not mark its own unit complete.** It is opened as a **draft**, is not
self-reviewed, is not principal-accepted, and is not merged in the session that authored it.

## Rationale

The conflict `XASSET-0055` resolved was real, and its resolution is what makes this
implementation expressible at all: with an open verdict vocabulary a genuine multiword verdict and
an approval with appended undelimited prose are not syntactically separable, so no heuristic can
divide them. §C's answer — return the whole region and let exact equality refuse it — keeps the
refusal fail-closed while giving up only diagnostic precision for that one class. This
implementation takes that answer literally rather than reintroducing a heuristic under another
name, which is precisely how PR #355 failed.

The sentinel was chosen over a typed result or an added enum value because it is the smallest of
the three routes §C permits and because it leaves `None` meaning exactly what it meant before, so
the three consumers' ABSENT policies are preserved by construction rather than by re-derivation.
Zero helpers were introduced because the whole correction fits in one function; the permitted
ceiling of one is a maximum, not a target.

## Alternatives considered

**A closed verdict vocabulary.** Rejected — `XASSET-0055` §G already rejected it on evidence, and
any list assembled before the PR #355 reviews would have refused those reviews' own verdict.

**A typed result object.** Rejected as larger than a sentinel for no gain: it would have changed
what `None` means at all three consumers and forced their ABSENT policies to be rewritten rather
than preserved.

**One narrow helper for the suffix grammar.** Rejected: it would have consumed the single
permitted helper for something §C describes as devoted solely to the ABSENT/MALFORMED distinction,
and the validation is four lines inline.

**Leaving the code-fence gap and disclosing it.** Rejected: §D.17 and §D.18.7 name code-fenced
lines explicitly, one boolean closes it, and disclosing a requirement as a limitation when it is
cheaply satisfiable is not the honest trade.

## Consequences

The parser now authenticates review `5000581301` correctly, refuses every unsupported shape fail
closed, validates rather than discards separator suffixes, and separates ABSENT from MALFORMED
end to end. Exactly one real review's parse changes.

The bound load-bearing digest is stale and **stays** stale. Stage 1 remains UNARMED and NOT
EXECUTABLE, `ATTEMPT_1` remains intact and unclaimed, and the later rebinding that would reconcile
the digest remains a separate, unauthorized future unit.
