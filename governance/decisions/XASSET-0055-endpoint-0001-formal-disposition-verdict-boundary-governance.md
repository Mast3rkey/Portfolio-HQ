---
decision_id: XASSET-0055
date: 2026-08-24
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_verdict_boundary_governance.py
---

## Context

**This is a governance-only filing.** It changes no production code, and it resolves a conflict
inside `XASSET-0053`'s own conjunctive requirements that no implementation can satisfy. It then
authorizes exactly one future replacement parser-correction implementation, and nothing downstream.

`XASSET-0053` remains the accepted authority for the parser-contract correction. This decision does
not repeal it, does not reopen its §C permitted set, and does not widen its scope. It governs one
question §D leaves in contradiction, and removes one unauthorized rule a failed implementation
introduced.

### Live preflight

Performed against live git and live GitHub before any file was written. Every value independently
re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `683c324629544a84d2cf75ebca37325e3375c479` |
| This filing's base | the same, unchanged — nothing from PR #355 merged |
| Authorization module at that base | SHA-256 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`, blob `f71b08b4ebe95f161c57cdbb2a924748f13af02d` |
| PR #355 | **closed, unmerged**, branch and history preserved |
| Reviews on PR #355 | FULL `5008847293` (1 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE) at head `15dde3c8…`; DELTA `5010334966` (1 BLOCKING / 1 MAJOR / 0 MINOR / 0 NOTE) at head `148a1584…` |
| Decision catalog at base | **155** entries, `XASSET-0053` last, `issues == ()` |
| Next unused identifier | **`XASSET-0055`** — derived, not assumed (below) |
| Lane · `AUTHORIZATION_ROOT` · `stage1_results.yaml` · `ATTEMPT_1` | `ABSENT` · absent · absent · intact, unclaimed |
| Both authorization predicates | **`False`** |
| Frozen universe | **680** constructions / **48** cells |

### Identifier derivation

`XASSET-0055` was derived, not predicted. `main`'s catalog and decisions directory reach
`XASSET-0053`. `XASSET-0054` exists **only** on PR #355's preserved branch, which is closed
unmerged — its identifier is treated as **consumed** and is not reused, so a reader following the
closed branch is never confused about which `XASSET-0054` is meant. A scan of every reachable
commit tree and all **249** remote refs found `XASSET-0055` nowhere, and it appears nowhere in the
working tree. `XASSET-0099` and `XASSET-9999` were investigated and are synthetic negative-case
test fixtures, not decisions.

**Disclosed limitation.** This checkout is a shallow clone (oldest reachable commit
`fe34ac1f…`, 2026-07-12), and GitHub code search returns HTTP 403 under this environment's proxy
policy. The derivation rests on the committed catalog — an authoritative in-tree index complete
regardless of clone depth — plus the decisions directory, the register, the working tree, all
reachable history, and all remote refs.

## Decision

### A. Determination — `FORMAL_DISPOSITION_VERDICT_BOUNDARY_GOVERNED`

`XASSET-0053` §D contains a genuine contradiction for one specific input class. This decision
resolves it by explicit governed rule rather than by another parser heuristic, restores one
requirement a failed implementation regressed, and authorizes exactly one replacement
implementation.

### B. The conflict, established from the governing text and reproduced

Both DELTA findings were independently reproduced against the real module before this filing.

**Finding 1 — reproduced.** `FORMAL DISPOSITION: <approval> DO NOT MERGE` returns a `str`, not
`MALFORMED_FORMAL_DISPOSITION`, in both accepted wrapper forms. Exact comparison keeps it from
authenticating, but §D.9/§D.17/§D.19 are conjunctive and require MALFORMED.

**Finding 2 — reproduced, and it is a real regression.** At PR #355's first reviewed head,
`FORMAL DISPOSITION: approved` returned the exact string `approved`. At its corrected head a
lower-case heuristic made it MALFORMED. Five previously-parseable canonical verdicts were tested
and **all five regressed**. §D.1 requires the existing unformatted canonical line to parse
*exactly as it does today*, additively, never as a replacement.

**The conflict itself.** Consider two lines:

```
FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED
FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE DO NOT MERGE
```

The first is a genuine verdict — it is the literal verdict of both reviews on PR #355. The second is
an approval with appended operative prose. Under an **open** verdict vocabulary they share every
syntactic feature: prefix, upper case throughout, no delimiter, ordinary words, no distinguishing
token shape. **No syntactic rule can accept the first and reject the second.**

Therefore, simultaneously:

* **(i)** §D.1, §D.3 and §D.14 require arbitrary existing canonical verdicts to keep parsing — an
  **open verdict channel**, with no new disposition-vocabulary rule; and
* **(ii)** §D.9, §D.17 and §D.19 require **all** trailing prose to become MALFORMED.

For the no-delimiter case, (i) and (ii) **cannot both hold**. Every possible heuristic must violate
one. PR #355 demonstrated both failure directions: its first head violated (ii) by disclosure, its
second violated (i) by regression. **The conflict is in the governing text, not in any
implementation**, which is why it is resolved here rather than in code.

### C. The governed resolution — the verdict boundary, stated explicitly

For a line already established as one of the two accepted wrapper forms (§D.2, §D.16), and after
any recognized separator suffix has been **validated** as finding-count metadata (§E):

1. **The entire remaining post-prefix region is the verdict, returned verbatim.** It is not
   truncated, normalized, replaced, canonicalized, fuzzy-matched, or coerced. §D.3 is unchanged.
2. **Exact equality applies to that entire region.** Comparison against
   `APPROVING_REVIEW_DISPOSITION` is over the whole verdict, never a prefix or substring of it.
   §D.5 is unchanged.
3. **Appended text can therefore never authenticate as approval.** Any character appended after the
   approval makes the region unequal to `APPROVING_REVIEW_DISPOSITION`, at the parser and at all
   three consumers. This is a property of exact equality, not of a heuristic, and it holds for text
   in any case, of any length, in either wrapper form.
4. **Syntactically undetectable trailing text with no delimiter is rejected by verdict inequality,
   not falsely classified MALFORMED.** Where no delimiter marks a boundary and the verdict channel
   is open, no rule can locate the boundary; the parser must not pretend it can. It returns the
   region verbatim and lets inequality reject it.
5. **This is an explicit governed rule, not an undocumented exception.** For the no-delimiter class
   only, §D.9's undifferentiated "must not parse" is **narrowed** to "must not authenticate, and
   must not be truncated". §D.9, §D.17 and §D.19 continue to require MALFORMED in full for every
   class where a boundary **is** syntactically locatable — leading prose, every unsupported
   decoration, and every arbitrary separator suffix.

**Scope of the narrowing, stated exactly.** It reaches **only** input where all of the following
hold: the line is in an accepted wrapper form; no recognized separator is present; and the trailing
text is not otherwise distinguishable from verdict text. It reaches nothing else. It is not a
licence to accept any other unsupported shape, and it does not weaken any other clause.

**What this costs, stated plainly.** A reviewer who writes an approval and appends words to it
produces a line that is refused by inequality rather than flagged as malformed. The refusal is
equally fail-closed; the *diagnostic* is weaker. That is the price of an open verdict channel, and
it is paid deliberately rather than concealed.

### D. The lower-case heuristic is removed and prohibited

PR #355's `any(character.islower() for character in verdict)` rule is **unauthorized** and must not
appear in the replacement implementation. It was a disposition-vocabulary rule §D.14 forbids, and it
regressed §D.1. Prior mixed-case and lower-case canonical-line behaviour is **restored**: a plain
line such as `FORMAL DISPOSITION: approved` returns exactly `approved`, as it did before.

No successor may reintroduce an uppercase-only verdict grammar, or any equivalent
case-, length-, or word-count-based verdict rule, without its own separate governance decision.

**A test may not authorize the production behaviour it asserts.** PR #355 changed a test's
expectation and labelled the change "strengthened". The DELTA review was right that this ratified an
unauthorized production change. Recorded here so the pattern is recognizable, not repeated.

### E. What is preserved from PR #355 — proven, and to be carried forward

The DELTA review independently confirmed this work: *"the original separator-authentication bypass
is closed: arbitrary separator suffixes are no longer discarded, earliest-separator handling closes
the mixed-separator escape, and the new real-consumer tests cover all four separators in both
accepted wrapper forms."* It is preserved as governed requirement:

1. **Recognized separator suffixes must be validated as finding-count metadata**, never discarded
   unread. The grammar is the narrowest the governed text and the durable record support:

   ```
   count_list := count ( "/" count )*
   count      := <digits> <space> <CATEGORY>
   CATEGORY   in { BLOCKING, MAJOR, MINOR, NOTE }
   ```

2. **An arbitrary separator suffix fails MALFORMED.** `<approval> | CHANGES REQUIRED` and every
   equivalent must stop classification, for every recognized separator, in both wrapper forms.
3. **Earliest-separator handling is preserved.** The earliest recognized separator in the region
   governs, not the first in tuple order — otherwise `<approval> | CHANGES REQUIRED — 0 BLOCKING`
   escapes.
4. **The recognized separator tuple is unchanged** (`—`, `--`, ` - `, `|`). The finding is about
   what may follow a separator, not which are recognized.

### F. What is preserved from `XASSET-0053` unchanged

Exactly the two accepted wrapper forms — the plain canonical line and the precisely balanced
whole-line Markdown-bold wrapper — and no others (§D.2, §D.16). Exact comparison with
`APPROVING_REVIEW_DISPOSITION` (§D.5). First-formal-line governance (§D.4). Independent rejection of
native `CHANGES_REQUESTED` (§D.6). Adverse verdicts adverse in both forms (§D.7). Leading prose,
headings, blockquotes, bullets, code fences, and unbalanced/nested/partial emphasis all MALFORMED
(§D.8, §D.9, §D.10). The ABSENT/MALFORMED distinction observable through all three consumers, with
MALFORMED never rescued by a native `APPROVED` state and each consumer's ABSENT policy preserved
(§D.19). The three-call-site boundary and the §C permitted set.

**The open verdict channel is preserved.** No closed vocabulary, no case rule, no length rule.

### G. Why a closed verdict vocabulary was rejected

A closed vocabulary would resolve the conflict cleanly — with a known verdict set, trailing prose is
detectable and §D.9 satisfiable in full. It is rejected on evidence, not preference.

**The evidence.** `XASSET-0053` §B.7's own scan enumerated **34** `FORMAL DISPOSITION:` lines across
PRs #337–#353 — 20 plain, 8 balanced-bold, 6 heading-form. It enumerated **lines, not verdicts**;
no machine-readable verdict list has ever existed in this repository. Scanning `main`'s own committed
record for verdict strings in narrative use finds at least four distinct ones —
`APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE`, `CHANGES REQUIRED`, `BOUNDED CORRECTION REQUIRED`,
`DELTA APPROVED` — and that record is prose describing past reviews, not an authority a parser could
be built against.

**The decisive fact.** Both reviews on PR #355 carry the verdict `BOUNDED CORRECTION REQUIRED`. A
closed vocabulary built from `XASSET-0053`'s own §B.7 line scan would have had to enumerate verdicts
that scan never extracted, and any list assembled before those reviews would have **refused the very
reviews that found the defect**. A vocabulary that refuses its own governing reviews is not safer.

**Stated honestly:** `BOUNDED CORRECTION REQUIRED` is not novel — it appears six times in `main`'s
register as narrative description of earlier reviews. What is absent is any *enumeration* a closed
implementation could have been built from. The claim is that the verdict set is **undocumented and
demonstrably still growing in use**, not that this particular string had never been seen.

**Therefore:** a closed vocabulary is not adopted, and §C's inequality rule governs instead. Should
a future decision wish to close the vocabulary, it must first enumerate the permitted verdicts
exhaustively from durable evidence, prove backward compatibility against every line in the record,
and accept that every future verdict then requires a governance amendment. That is a real option;
it is simply not taken here, and not taken silently.

### H. Authority granted — exactly one future replacement implementation

One future, separate, bounded parser-correction implementation PR is authorized. It supersedes and
replaces PR #355, which is closed unmerged. It **may**, and only in service of this defect:

1. Implement the correction `XASSET-0053` §C already authorizes, within that §C permitted set
   unchanged — `parse_formal_disposition()`, the minimal result representation, **at most one**
   newly introduced narrow helper, and the minimum necessary lines in the three named consumers.
2. Implement §E's separator-suffix validation and earliest-separator handling.
3. Implement §C's governed verdict boundary.
4. **Remove the lower-case heuristic** and restore prior mixed/lower-case canonical-line behaviour
   per §D.
5. Add the adversarial tests §I requires, and record its own bounded scope in the catalog and the
   register.

That authority ends there. **No fourth call site. No second helper. No general parsing framework.
No change to any other existing production function. No closed verdict vocabulary. No new
case-, length-, or word-count-based verdict rule.**

### I. Validation the replacement implementation must satisfy

1. **Parser-level behavioural tests** for every class: both accepted wrapper forms; every recognized
   separator; validated finding-count suffixes including review `5000581301`'s byte-for-byte line;
   arbitrary separator suffixes MALFORMED; earliest-separator ordering; leading prose and every
   unsupported decoration MALFORMED; ABSENT preserved; and §C's boundary rule, including a case
   proving a mixed-case canonical verdict parses exactly as before.
2. **All-three-consumer behavioural tests** — `_derive_pr337_actor_ratification()`,
   `verify_lifecycle_against_truth()`, `_verify_selected_review_is_final()` — driven on their real
   authenticated seams, not the parser alone (§D.15).
3. **Mutation probes** covering each accepted, adverse, malformed, absent, consumer, call-site,
   scope-boundary, and separator-bypass class, plus a probe proving the lower-case heuristic cannot
   be reintroduced without failing. Every probed file restored byte-identically by SHA-256.
4. **Non-vacuity** measured against the exact base.
5. **Simulated normal merge** with a tree byte-identical to the offered head.
6. **Full repository suite and exact-head CI**, the CI job log decoded independently.
7. **A zero-write end-to-end rehearsal** proving the corrected parser is exercised through the real
   consumer paths while writing no authorization state: no lane record, no `AUTHORIZATION_ROOT`, no
   attestation, no claim, no results file, and both authorization predicates still `False`
   afterwards.

### I-bis. Predecessor suites re-anchored, never weakened

`active_branch`, `active_pr` and `last_verified_main_sha` are WS-0014's **single shared** live
self-reference fields under `OPS-0001`'s Active-GitHub-fields rule. Advancing them onto this unit
therefore falsified assertions in ten predecessor suites that named the previously-live unit, plus
two catalog-tail assertions in `XASSET-0053`'s own suite. Verified, not assumed: all of them pass
at the base `683c3246...` and fail only under this unit's lawful advance.

Every one was **re-anchored** onto a closed immutable anchor, following the remedy this programme
already established when `XASSET-0043`/`XASSET-0044` re-anchored the `XASSET-0042` suite. Each
superseded value is retained beside the new one as a **negative pin**, so the field stays bound at
**both** ends and a silent revert to any finished unit's state still fails. There is deliberately
no `XASSET0054` generation: `XASSET-0054`'s pull request #355 was closed unmerged, so it never
became `main` state and has no merge SHA to pin.

Two assertions could not be re-pointed at the same value and were instead re-anchored at the
durable fact underneath them: `XASSET-0053`'s own `active_pr` assertion now reads that unit's own
**gate** (which does not move and still carries the real number GitHub issued, never its sentinel),
and its catalog-tail assertions now name the successor set explicitly rather than being relaxed to
"present somewhere in the list".

Each was re-anchored and **never deleted, skipped, xfailed or relaxed**, and no re-anchored suite is
a `LOAD_BEARING_RELPATHS` entry, so the module's trust boundary is untouched and no rebinding is
implied. `test_level1_stage1_verdict_boundary_governance.py` pins each of these properties
mechanically, including that every re-anchored suite's assertion count only grew.

### J. The replacement implementation changes a load-bearing byte

`level1_stage1_execution_authorization.py` is `LOAD_BEARING_RELPATHS[0]`. The replacement
implementation will change it, so its bound digest will again go stale by design. **That drift is
the fail-closed hand-off to a later, separately authorized step-8-equivalent rebinding unit.** The
replacement implementation must **not** re-pin it, and this decision authorizes no rebinding.

### K. This decision, and the implementation it authorizes, **must not**:

- perform, arm, claim, execute, or complete any part of ENDPOINT-0001 Stage 1;
- create an attestation, `AUTHORIZATION_ROOT`, lane state, `READY`, claim, or completion record;
- consume, claim, or touch `ATTEMPT_1`;
- **perform a step-8-equivalent rebinding**, or re-pin any load-bearing or canonical digest;
- perform readiness verification or a drift check;
- authorize or perform link 5, or any successor unit of any kind;
- edit any historical review, comment, acceptance record, or closure record;
- modify any runner, result validator, universe module, canonical artifact, or protected portfolio
  path;
- weaken any adverse-review rejection, any validator, or any test;
- change any construction identity, universe membership, ordering, or cardinality;
- acquire market, fundamental, economic, or Stage-2 data;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` artifact; or
- create any endpoint, bound, point, range, percentage, weight, rank, target, ladder, or trade.

**This filing modifies no production code.** `level1_stage1_execution_authorization.py` is
byte-unchanged from its base.

### L. Lifecycle

Effective only on complete closure of all seven conditions, in order: independent **FULL** exact-head
review under `OPS-0007` §1; any bounded correction and exact-head re-review; principal exact-head
acceptance; normal merge; immediate post-merge verification; successful merge-commit CI whose
`head_sha` is the exact merge SHA; and final post-CI verification and lifecycle closure.

## Rationale

The reviewer's instruction was explicit: *"If the current open-verdict contract and §D.9 cannot both
be satisfied, stop rather than guess."* Two implementations had already guessed, in opposite
directions, and each broke the requirement the other honoured. A third guess would have been a third
failure.

The conflict is real and demonstrable, so the honest move is to decide *which* requirement governs
the ambiguous case and say so in governed text. §C does that in one direction rather than the other,
for one reason: the open verdict channel is load-bearing for the review process itself. Reviews in
this repository invent verdicts as they need them — `BOUNDED CORRECTION REQUIRED` is the verdict of
the two reviews that found these very defects. A parser that refuses unfamiliar verdicts would
refuse the reviews that keep it honest. Weakening a *diagnostic* on one narrow class is a smaller
loss than that.

The cost is stated rather than hidden, because the failure this decision exists to correct was
precisely a residual described as compliance. Whether it is bearable is now a reviewable governance
question with the boundary written down, instead of an implementation detail discovered in review.

## Alternatives considered

**A closed verdict vocabulary.** The only clean resolution of the conflict, and genuinely tempting.
Rejected on the evidence in §G: no enumeration has ever existed, the set is demonstrably still in
motion, and a list built from `XASSET-0053`'s own scan would have refused that scan's own successor
reviews. Left available to a future decision willing to enumerate exhaustively and accept amendment
on every new verdict.

**Another parser heuristic.** Rejected outright — the point of this filing. Any heuristic must
violate (i) or (ii); both directions have now been tried and independently rejected.

**Repealing or rewriting `XASSET-0053` §D.9.** Rejected as too broad. §D.9 is correct for every class
where a boundary is locatable, which is most of them. Only the no-delimiter class is narrowed, and
only with the boundary stated.

**Amending PR #355 in place with a third attempt.** Rejected. The DELTA review found the
implementation departing from its sole authority; the fix is new authority, not another commit under
the old one. PR #355 is closed unmerged with its branch preserved so its proven separator work is
not lost.

**Reusing the `XASSET-0054` identifier.** Rejected. It is consumed by a closed, preserved branch;
reusing it would make two different decisions share one identifier in the retained record.

## Consequences

The verdict boundary is governed explicitly, so a replacement implementation can satisfy its
authority in full rather than trading one clause against another. The lower-case heuristic is
prohibited and prior canonical-line behaviour restored. PR #355's separator-suffix validation —
independently confirmed correct — is carried forward as governed requirement rather than discarded
with the PR.

**Nothing became effective from PR #355.** `main` is unchanged, and the authorization module there
remains at SHA-256 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The replacement implementation will change a
load-bearing byte and therefore requires a later, separately authorized rebinding, an external
one-shot pre-execution attestation, and a lawful `READY` lane before anything can execute. Each is
its own authority. `ATTEMPT_1` remains intact, unclaimed, and unconsumed.
