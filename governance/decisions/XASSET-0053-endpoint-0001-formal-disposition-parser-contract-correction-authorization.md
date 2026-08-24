---
decision_id: XASSET-0053
date: 2026-08-24
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_parser_contract_correction_authorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as
authoritative over every fact supplied to this session. Every value below was independently
re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6` |
| Worktree / stash / worktrees | clean; no stash; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| Later commits on `main` | **none** |
| PR #353 | closed, **merged**, not draft; `merged_by` `Mast3rkey`; 15 files; 4 commits |
| PR #353 base · accepted head | `8def8bd096b4edecbf10fc20870a6d03b6cb56fe` · `8f1cc608e1219b2cb9fcbf8f8f42a24fbd0f131c` |
| `XASSET-0052` lifecycle closure | [`#issuecomment-5389700733`](https://github.com/Mast3rkey/Portfolio-HQ/pull/353#issuecomment-5389700733) — all seven §N conditions closed; merge-commit CI run `32679424717` / job `97293351500`, `head_sha` the exact merge SHA |
| **Failed link-5 determination** | [`#issuecomment-5389820540`](https://github.com/Mast3rkey/Portfolio-HQ/pull/353#issuecomment-5389820540) — **`STOPPED_BEFORE_ATTESTATION`**, never edited (`created_at` == `updated_at`), authored by `Mast3rkey`, body SHA-256 `4ee46f3f23e6ab25c45e395b4193e886b5e1ffc176b296aabf0d19f6691702f2` |
| The defective-but-substantively-approving review | PR #349 review `5000581301`, `commit_id` `b2059e80101fc6457f4004939d7d12886e6feedf`, author `Mast3rkey`, body SHA-256 `6a221d8a36ae8c00e057c763c175879556133569b645b5302ca142fa1001177a` |
| Authorization module blob at the stop | `f71b08b4ebe95f161c57cdbb2a924748f13af02d` — identical at `HEAD`, in the tree, and in the worktree |
| The effective `XASSET-0049` bound merge | `a941455491cc5e4d3d868775fb6b4b88f0fe2ce3` — parents `f052efad38e3d57e3e5615799ac3bcbebe83ff5f` → `b2059e80101fc6457f4004939d7d12886e6feedf`, no third; tree `b7015b271362ae0c2fe663e8bfda9c6d10de5e7e` |
| `LOAD_BEARING_RELPATHS` | **18**, unique, each present, each byte-identical to the bound merge — 0 mismatches of 18 |
| Canonical pins | `1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84` and `898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f`, matching their files exactly |
| Frozen universe | **680** constructions / **48** cells / `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` |
| Module constants | `AUTHORIZING_DECISION` `XASSET-0049`; `AUTHORIZING_PULL_REQUEST` `349`; `REVIEWED_BASE_SHA` `f052efad…`; `REQUIRED_LIFECYCLE_GATES` **6** |
| Lane state · execution | `ABSENT`, all four lane paths and `AUTHORIZATION_ROOT` absent · `new_execution_is_authorized()` **`False`** · `active_execution_is_authorized()` **`False`** |
| `stage1_results.yaml` | **absent** — zero matches anywhere in the tree |
| Seven protected portfolio paths | byte-identical to the bound merge |
| `XASSET-0053` | **unused** — zero occurrences in the tracked tree, the decisions directory, the catalog, the register, all reachable history, and every remote branch |
| Decision catalog | **154** entries, unique, `XASSET-0052` last, `issues == ()` |
| Register | exactly **zero** `priority: primary` workstreams; `WS-0014` at `proposed` / `secondary` |

**One disclosed shallowness.** This checkout is a shallow clone; `git rev-parse
--is-shallow-repository` returns `true`, and 1,157 commits are reachable, back to 2026-07-12. That
window contains the entire `XASSET-####` series — `git log --all -S"XASSET-0001"` reaches the
series' own originating commit — so the `XASSET-0053`-is-unused check covers every commit in which
any `XASSET-####` decision could have been introduced. It is recorded as a limitation rather than
presented as a complete-history guarantee, and the check is corroborated independently by the
tracked tree, the decisions directory, the catalog, the register, and a scan of every remote branch.

### The question this decision answers

`XASSET-0052`'s single authorized link-5 unit ran and reached a terminal **`STOPPED_BEFORE_ATTESTATION`**
(§K.1). It stopped on **one** condition, and that condition is a **parser-contract mismatch inside a
load-bearing module**, not a governance-evidence gap, not an adverse review, and not drift in any
byte, pin, universe, or lane.

Nothing in the repository is currently authorized to correct it. `XASSET-0052` §H forbids the
link-5 unit from correcting, reverting, regenerating, or re-pinning any defect it finds, and §J
states the consequence directly:

> remediation requires **separately authorized things**, each with its own governance authority and
> its own lifecycle … **None of those is authorized by this decision, and none becomes authorized by
> the link-5 unit discovering that it is needed. Finding the work is not authority to do the work.**

**This decision is the authority for exactly the first of those things — the parser-contract
correction — and nothing else.**

## Decision

### A. Determination — `FORMAL_DISPOSITION_PARSER_CONTRACT_CORRECTION_AUTHORIZED`

**Exactly one** future, separate, bounded **parser-contract correction unit** is authorized, to make
`parse_formal_disposition()` in `level1_stage1_execution_authorization.py` recognise the exact
legitimate Markdown formatting demonstrated by PR #349 review `5000581301`, **without weakening
adverse-review rejection in any respect**.

**This filing is design-only. It performs none of that work.** It edits no module, corrects no
parser, changes no load-bearing byte, and produces no attestation, lane, claim, execution, or
artifact. Merging it corrects nothing and arms nothing.

#### A.1 — The distinction any summary of this filing must preserve

Stated once, in a form meant to be quoted verbatim, because the failure mode `XASSET-0052`'s own
independent review caught — a summary that collapses "performs none of it" into "authorizes none of
it" — applies here identically:

> `XASSET-0053` **authorizes** exactly one future, separate **parser-contract correction unit**, but
> **this filing performs none of that work**, and the correction is **not exercisable unless and
> until §J's seven conditions close**.

**The parser correction never belongs inside a "not authorized" list.** It is exactly what this
decision is the authority for. Every enumeration of what is withheld — §F, §K, the `WS-0014` gate,
and any pull-request summary or report describing this filing — must place it on the
**authorized-but-unperformed** side of that line.

**Three claims are therefore prohibited anywhere in this filing's governed text, its register entry,
its pull-request body, and any report describing it:**

1. that the parser correction is "not authorized by this filing itself" — this filing *is* its
   authority source;
2. that this filing adds "zero correction authority" — it adds exactly one, which is its entire
   purpose. The correct and narrower statement is that it adds **zero committed activation factors**
   and performs **zero correction acts**;
3. that this filing performed, corrected, rebound, armed, claimed, executed, or produced anything —
   it did none of those.

### B. The defect, reproduced independently before this filing was authored

Nothing below is asserted on the strength of the link-5 stop report. Each item was re-derived in
this session against live GitHub and the exact `main` tree.

**B.1 — The review record.** PR #349 review `5000581301` is real, belongs to PR #349, was authored
by `Mast3rkey`, was submitted `2026-08-22T16:34:47Z`, and carries `commit_id`
`b2059e80101fc6457f4004939d7d12886e6feedf` — the exact accepted head. Its body contains **exactly
one** line naming a formal disposition, and that line is:

```
**FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**
```

The wrapper is a **precisely balanced, whole-line** Markdown-bold pair: the line begins with `**`,
ends with `**`, and the enclosed text contains no further `*` character.

**B.2 — The parser contract.** `parse_formal_disposition()`, read verbatim from the exact `main`
tree at `cc1d1b62…`, skips any line for which
`stripped.upper().startswith(FORMAL_DISPOSITION_PREFIX)` is false, with
`FORMAL_DISPOSITION_PREFIX == "FORMAL DISPOSITION:"`. For the line above that predicate is
**`False`**, because the first two characters are `**`. The function therefore returns **`None`**.

**B.3 — The substantive verdict.** Removing **exactly the balanced outer `**` markers**, in memory
only and altering nothing on GitHub or on disk, yields
`'APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE'` — **exactly** `APPROVING_REVIEW_DISPOSITION`.

**B.4 — The public failure.** `build_authorization_payload()` followed by
`validate_authorization_document()`, run read-only with no attestation and no lane state written,
returns `valid = False` with **exactly one** error:

```
governance truth: review 5000581301 carries no parseable 'FORMAL DISPOSITION:' line,
so its verdict cannot be authenticated
```

Every other gate the mechanism checks passed — finality, actor identity, chronology, merge structure
and zero-drift, post-merge verification, merge-commit CI run/job pairing, git-anchored identity,
successor-rebinding identity, closure, canonical pins, universe identity, and load-bearing byte
identity.

**B.5 — No admissible alternative.** PR #349's complete review list was retrieved (2 reviews; a
short page proves exhaustion rather than truncation, and a failed page would have returned `None`
and failed closed). Exactly one review sits at the accepted head — the one above. The only other,
`5000502119`, fails harder: wrong head, a parsed disposition of `CHANGES REQUIRED`, **and** the
finality gate independently failing closed on the same unparseable line.

**B.6 — What this is, and is not.** This is a **formatting/parser-contract mismatch**. It is
**not** an adverse review, **not** a governance-evidence gap of the kind `XASSET-0041` §I link 1
corrected, and **not** drift: the module blob `f71b08b4ebe95f161c57cdbb2a924748f13af02d`, all 18
load-bearing paths, both canonical pins, the frozen universe, and the seven protected portfolio
paths were all verified byte-identical, and the lane was verified `ABSENT` throughout.

### C. Authority granted — exactly one future, separate parser-contract correction unit

The future unit **may**, and only in service of this defect:

1. **Modify `parse_formal_disposition()`** in `level1_stage1_execution_authorization.py` so that the
   exact legitimate formatting demonstrated by review `5000581301` yields its correct approving
   verdict.
2. **Add or extend focused adversarial tests** proving the corrected behaviour and the preserved
   rejections §D requires.
3. **Record its own bounded scope** in the catalog, the register, and its own pull-request evidence,
   following the repository's ordinary governance-implementation conventions.

**That authority ends there.** No other module, function, validator, runner, universe module,
canonical artifact, or protected path may be touched, and no other behaviour of the authorization
mechanism may be altered.

### D. The required safety boundary — conjunctive, and every clause binding

The future correction **must** satisfy **all** of the following. Failure on any one is a defect in
the correction, not a permitted trade-off.

**D.1 — Continue accepting the existing unformatted canonical line.** A body whose formal line is
already `FORMAL DISPOSITION: …`, with no emphasis markers, must parse exactly as it does today. The
correction is additive to the accepted grammar, never a replacement of it.

**D.2 — Accept only a precisely balanced, whole-line Markdown-bold wrapper** around the same
formal-disposition grammar the unformatted line already uses — that is, the exact shape review
`5000581301` demonstrates: the stripped line begins with the bold marker, ends with the matching
bold marker, and the enclosed text is itself a well-formed formal-disposition line. No other
formatting is admitted by this authorization.

**D.3 — Normalize formatting before extracting the verdict; never normalize or replace the
verdict itself.** The correction may strip the balanced wrapper to reveal the underlying line, and
must then extract the verdict from that revealed line by the existing rule. It may **not** rewrite,
substitute, canonicalize, fuzzy-match, or coerce the verdict text, and it may **not** map a
non-approving verdict onto an approving one under any circumstance.

**D.4 — Preserve "first formal disposition line governs."** The first qualifying line still decides,
and a later line — wrapped or unwrapped — may never override it.

**D.5 — Preserve exact comparison with `APPROVING_REVIEW_DISPOSITION`.** The extracted verdict must
still be compared for exact equality against
`APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE`. Substring, prefix, case-insensitive, or
similarity comparison is prohibited.

**D.6 — Preserve independent rejection of native `CHANGES_REQUESTED`.** The GitHub-native adverse
state remains adverse on its own footing, evaluated independently of body grammar, exactly as
`NATIVE_ADVERSE_REVIEW_STATES` provides today.

**D.7 — Reject wrapped or unwrapped `CHANGES REQUIRED`.** A bolded adverse formal line must be
parsed as adverse, not made unparseable and not made approving. Adding wrapper recognition must not
create a new way for an adverse review to escape detection.

**D.8 — Reject approval text appearing only as a substring, quotation, explanation, heading, code
sample, suffix, or later prose.** The `MAJOR 1` finding that produced the current first-line
contract — review `4946464366`, where `APPROVING_REVIEW_DISPOSITION in body` let an adverse review
pass because later explanatory text quoted the approval phrase — must remain closed in every one of
those forms.

**D.9 — Reject leading or trailing operative prose around the formal line.** The wrapper exception
admits emphasis markers only. A line carrying additional operative words before or after the formal
disposition is not the demonstrated shape and must not parse.

**D.10 — Reject unbalanced, nested, partial, repeated, or ambiguous emphasis markers.** An opening
marker with no matching close, a closing marker with no matching open, nested or doubled wrappers,
a wrapper on one side only, or any construction whose intended verdict is not unambiguous must fail
closed rather than be guessed at.

**D.11 — Preserve every surrounding protection unchanged.** Review identity, accepted-head identity,
chronology, finality, pagination and exhaustion semantics, reviewer identity derivation,
attribution, lifecycle evidence, and record fingerprinting all remain exactly as they are. The
correction touches the disposition *parse* and nothing else.

**D.12 — Add behavioral and mutation tests** proving that the exact historical review
`5000581301` changes from **unparseable** to **correctly approving**, while adverse and ambiguous
variants remain rejected. The suite must cover, at minimum, each of D.1 and D.6 through D.10 as its
own directly-exercised case, and must fail if any of them regresses.

**D.13 — Do not edit review `5000581301`, any historical review, comment, acceptance record, or
closure record as the remediation.** The durable record is evidence, not a repair surface. Editing
it would destroy the very artifact the correction exists to authenticate, and is prohibited outright.

**D.14 — Do not repair any other parser, and do not broaden the accepted review grammar beyond what
this demonstrated mismatch requires.** No other formatting convention, no other emphasis style, no
other disposition vocabulary, and no other parsing surface is in scope. A second genuine mismatch,
if one is ever demonstrated, is its own separate authorization.

### E. This filing does not restore operational authority, and cannot

Stated plainly, because the nearest inference a successor could draw is that correcting the parser
re-opens the road to Stage 1:

`parse_formal_disposition()` lives in `level1_stage1_execution_authorization.py`, which is
**load-bearing path #1** of the eighteen the `XASSET-0048` / `XASSET-0049` step-8-equivalent
rebinding bound. Correcting it **necessarily changes a load-bearing byte**, which means the
corrected module is no longer the module that rebinding bound. That is not a side effect to be
managed — it is the defining consequence, and §H states what follows from it.

### F. Authority withheld — absolute

The parser-correction unit, and this filing, **must not**:

- perform, arm, claim, execute, or complete any part of `XASSET-0041` §I link 5 / `XASSET-0030`
  §G.B step 11;
- create an attestation, `AUTHORIZATION_ROOT`, lane state, `READY`, claim, completion, ledger entry,
  or `stage1_results.yaml`;
- consume, claim, or touch `ATTEMPT_1`, or open or consume `XASSET-0027` §P.1's reserved results PR;
- **perform a step-8-equivalent rebinding**, or alter `AUTHORIZING_DECISION`,
  `AUTHORIZING_PULL_REQUEST`, `REVIEWED_BASE_SHA`, or `LOAD_BEARING_RELPATHS`;
- perform renewed readiness verification or a renewed drift check;
- authorize any successor unit of any kind;
- edit any historical review, comment, acceptance record, or closure record;
- modify any runner, result validator, universe module, canonical artifact, or protected portfolio
  path (`allocate.py`, `margin_state.py`, `levels.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`,
  `issuer_lookthrough.yaml`);
- weaken any adverse-review rejection, any validator, or any test;
- change any construction identity, universe membership, ordering, cardinality, or universe hash;
- reopen, re-derive, or re-argue B1, B2, B3, any gate semantics, `XASSET-0030`'s 6/6 gate map,
  `XASSET-0024` §K.1, or `XASSET-0020` §E.1;
- acquire market, fundamental, economic, or Stage-2 data, or perform any Stage 2 work;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result;
- create any endpoint, bound, point, range, percentage, weight, rank, target, ladder, or allocation,
  or authorize any chart, deployment, trade, order, or brokerage action.

**Additionally, and specific to this filing: `XASSET-0053` performs no part of the correction it
authorizes.** It modifies `level1_stage1_execution_authorization.py` not at all, and every one of the
eighteen load-bearing paths, both canonical pins, the frozen universe, and the seven protected
portfolio paths is byte-identical at this filing's head to the `XASSET-0049` bound merge.

### G. Fail-closed

Any drift, missing evidence, unexpected state, authentication failure, continuity gap, lane
mismatch, validation failure, or state the correction unit cannot determine with certainty **stops
it**. It must report the exact condition, change nothing further, and not proceed. **Uncertainty is
failure.** The unit is an implementer under exact conditions, never a remediator of anything beyond
§C's grant: if it finds a second defect, that is a finding to report, not work to perform.

### H. Downstream consequences — stated explicitly

These are the operative consequences of this authorization, and none may be read as softened by a
clean correction.

1. **The future parser correction requires its own separately reviewed and accepted implementation
   PR.** This filing authorizes it; it does not perform it, pre-approve it, or shorten its lifecycle.
   That PR carries its own independent FULL exact-head review under `OPS-0007` §1, its own bounded
   correction and exact-head re-review if required, its own explicit principal exact-head acceptance,
   its own normal merge, its own post-merge verification, its own successful merge-commit CI at the
   exact merge SHA, and its own final post-CI verification and lifecycle closure.

2. **Because that implementation will change a load-bearing authorization module, it cannot itself
   restore operational authority.** A corrected `level1_stage1_execution_authorization.py` is, by
   construction, no longer byte-identical to the module the `XASSET-0049` bound merge bound. Merging
   the correction therefore leaves the trust boundary pointing at bytes that no longer exist, and
   **arms nothing**. A correction that appeared to restore authority would be a defect, not a
   success.

3. **A later step-8-equivalent rebinding requires its own separately authorized and performed
   lifecycle**, of the same kind and rigour as `XASSET-0048` / `XASSET-0049`, and it must be based
   on the parser correction's **actual eventual normal merge identity, derived after that merge —
   never a predicted SHA.** No merge identity for the correction appears anywhere in this text, and
   none may be invented, pre-computed, or asserted before GitHub records it.

4. **Renewed readiness verification, renewed drift verification, and a fresh link-5 authorization
   each remain separately unauthorized**, and each requires its own authority and its own separate
   operational unit. Completing any one of them authorizes none of the others, and completing all of
   them authorizes link 5 only through a new decision of link 5's own.

5. **`XASSET-0052` remains effective as a historical decision, but its one-shot operational grant is
   spent** as `STOPPED_BEFORE_ATTESTATION`. It is not revived, reinterpreted, extended, or re-opened
   here; its file is not edited, its `status` is not changed, and its terminal record at
   [`#issuecomment-5389820540`](https://github.com/Mast3rkey/Portfolio-HQ/pull/353#issuecomment-5389820540)
   stands exactly as posted.

6. **Stage 1 remains UNARMED and NOT EXECUTABLE; `ATTEMPT_1` remains intact, unclaimed, and
   unconsumed.** At this filing, and immediately after its merge, `new_execution_is_authorized()`
   returns `False`, `active_execution_is_authorized()` returns `False`, the lane is `ABSENT`, and
   `stage_1_executability.executable` is `false`.

### I. Packaging and evidence

This is **one** governance-only authorization filing, delivered as **one** draft pull request that
makes no production change. Its outcome is recorded in the ordinary way: an author report and a
request for an independent FULL exact-head review on its own pull request.

Its pull-request number is never predicted. A unique, non-colliding negative sentinel is committed
first, the draft is opened, GitHub's issued number is read back from the live API, and the sentinel
is replaced through a **fast-forward** follow-up commit — no force-push, no amended history. The
sentinel is retained afterwards as a **negative** pin, so a silent revert to the unbound state fails
rather than passing unnoticed.

### J. Effectivity — the correction unit may not begin before this lifecycle closes

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the exact resulting merge — the repository's own six
`REQUIRED_LIFECYCLE_GATES` plus `OPS-0009` §6's exact-head discipline:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own
   run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this PR authorizes nothing; a green PR-head CI run does
not; principal acceptance does not; merge does not; and post-merge verification without a successful
exact merge-commit CI run does not. **Only complete closure of all seven does** — and even then,
what becomes authorized is one future correction unit bounded by §§C–G, which must still satisfy
every clause of §D.

### K. Absolute non-performance

**This section is about what this filing does not *do*, and about authority it does not *grant*. It
is never a denial of the one thing §A authorizes.** Per §A.1, the parser correction itself must not
appear below as unauthorized; it is authorized by §A and merely unperformed and not yet exercisable.

This decision corrects no parser and edits no module; changes no `LOAD_BEARING_RELPATHS`, canonical
file, hash pin, `AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST`, or `REVIEWED_BASE_SHA`; performs
no rebinding, no readiness verification, and no drift check; generates no attestation and creates no
`AUTHORIZATION_ROOT`, `READY`, `CLAIMED`, or `COMPLETED` lane state or ledger entry; arms, claims,
completes, executes, or recovers no Stage-1 execution; performs no part of `XASSET-0041` §I link 5 or
`XASSET-0030` §G.B step 11 and authorizes no new link-5 unit; evaluates no gate for any registered
construction and asserts no per-construction outcome; creates no `stage1_results.yaml` and no runner,
result validator, or other production or outcome-producing code; changes no construction identity,
universe membership, ordering, cardinality, or universe hash; consumes nothing of `ATTEMPT_1`;
acquires no market, fundamental, economic, or Stage-2 data and performs no Stage 2 work; reads,
lists, opens, or references no `risk_lane_boundary` protected `RISK` result; edits no historical
review, comment, acceptance record, or closure record; resolves `XASSET-0024` §K.1 neither way and
amends no `XASSET-0020` §E.1 scope; reopens, re-derives, or re-argues no gate semantics and neither
B1, B2, nor B3; consumes no `XASSET-0027` §P.1 results PR; weakens no validator or test; modifies no
research, intelligence, or protected portfolio path; creates no endpoint, bound, point, range,
percentage, weight, rank, target, or allocation; changes no `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes
no chart, ladder, deployment, trade, order, or brokerage action; and rewrites no accepted history.

## Rationale

**Why a governance filing at all, for what looks like a one-line parser fix.** The function sits
inside the module that authenticates every Stage-1 lifecycle gate, and it is load-bearing path #1.
Any edit to it invalidates the step-8-equivalent rebinding and changes what the trust boundary
covers. `XASSET-0052` §J anticipated exactly this and said so in terms: remediation requires
separately authorized things, and *finding the work is not authority to do the work*. Treating this
as a trivial fix would be the one move that quietly breaks the boundary the whole `ENDPOINT-0001`
programme exists to hold.

**Why the correction is narrow rather than a general Markdown-tolerant parse.** The current
first-line contract exists because of a real, reproduced failure: review `4946464366` found that
`APPROVING_REVIEW_DISPOSITION in body` let an adverse review pass whenever later explanatory text
quoted the approval phrase. Every relaxation of a disposition parser is a candidate re-opening of
that hole. Admitting exactly one shape — a precisely balanced, whole-line bold wrapper around the
same grammar, demonstrated by a real record — is the smallest change that clears the demonstrated
mismatch, and §D.7 through §D.10 exist so that admitting it cannot become a new escape route.

**Why normalization is confined to formatting.** Stripping a wrapper reveals a line; it must never
edit a verdict. A parser that could rewrite verdict text could turn `CHANGES REQUIRED` into
something else, which is the failure the whole gate is built to prevent. §D.3 draws that line
explicitly so a future implementer cannot reach it by a convenience helper.

**Why editing the review is prohibited rather than merely discouraged.** It would be the fastest
"fix" available and the most destructive: the durable record is the evidence the gate authenticates,
and a repository that repairs its own evidence when the evidence is inconvenient has no
authentication left. §D.13 forecloses it outright.

**Why the downstream chain is spelled out.** The nearest wrong inference is that a clean parser
correction restores the road to Stage 1. It cannot: correcting the module changes a bound byte, so
the correction's own merge leaves the trust boundary stale by construction. Saying that plainly —
and requiring the later rebinding to derive the correction's real merge identity after the fact
rather than predicting it — is what keeps the chain honest instead of appearing continuous.

## Alternatives Considered

| Alternative | Why rejected |
|---|---|
| Edit review `5000581301` to unbolded text and re-run link 5 | §D.13, Rationale. It destroys the authenticated artifact and makes the durable record a repair surface. The record is evidence, not a fixture. |
| Treat the bolded line as an adverse or absent review and stop permanently | §B. The verdict is substantively the approving one; the mismatch is formatting. Permanently refusing a legitimate approval because of emphasis markers is a defect, not caution. |
| Relax the parser to `APPROVING_REVIEW_DISPOSITION in body` | Rationale, §D.8. That is precisely the hole review `4946464366` found and the first-line contract closed. |
| Accept arbitrary Markdown emphasis (`*`, `_`, `__`, headings, code spans) | §D.2, §D.14. Only one shape is demonstrated. Broadening to shapes no record exhibits invents grammar and widens the attack surface for nothing. |
| Fix the parser inside the future link-5 unit | `XASSET-0052` §H, §J. That unit is expressly forbidden from correcting, rebinding, or repairing, and a repair immediately before a non-rerunnable claim is the worst possible moment for a load-bearing edit. |
| Bundle the correction, the rebinding, and a fresh link-5 authorization into one filing | §H. Each is a distinct authority with its own lifecycle, and the rebinding cannot even be specified until the correction's real merge identity exists. Batching them would let one review cover a module edit, a trust-boundary rebinding, and an irreversible execution grant. |
| Predict the correction's merge SHA so the rebinding can be authorized now | §H.3. A predicted merge identity is an unverifiable constant; the rebinding must derive it after the normal merge. |
| Revive `XASSET-0052` rather than file separately | §H.5. Its grant is one-shot and spent as a stop; topping it up would make "one-shot" meaningless, and its own §K made every terminal outcome end in report-and-stop. |
| Correct the parser and also harden neighbouring parsers while the module is open | §D.14, §F. Scope creep inside a load-bearing module is how a bounded correction becomes an unreviewable one. |

## Consequences

On complete closure of this decision's §J lifecycle — and not before — **exactly one** future,
separate, bounded parser-contract correction unit becomes authorized: to make
`parse_formal_disposition()` recognise the exact balanced whole-line Markdown-bold formatting
demonstrated by PR #349 review `5000581301`, bounded by §§C–G, required to satisfy every clause of
§D, and fail-closed on anything it cannot determine with certainty.

That correction, when it happens, **will change a load-bearing byte and therefore cannot restore
operational authority by itself**. A step-8-equivalent rebinding, renewed readiness verification, a
renewed drift check, and a fresh link-5 authorization each remain separately unauthorized and each
require their own authority, their own lifecycle, and their own separate operational unit — with the
rebinding bound to the correction's actual eventual merge identity, derived after the fact.

`XASSET-0052` remains effective as a historical decision and its one-shot operational grant remains
**spent** as `STOPPED_BEFORE_ATTESTATION`. `XASSET-0027` §P.1 remains **one, unspent**.

This filing creates no production or outcome-producing code and modifies no canonical, load-bearing,
research, intelligence, portfolio, or protected path. **Merging it corrects nothing and arms
nothing.** At this filing, and immediately after its merge, **Stage 1 remains UNARMED and NOT
EXECUTABLE. Lane state remains `ABSENT`. `ATTEMPT_1` is intact, unclaimed, and unconsumed.**
