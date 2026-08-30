---
decision_id: XASSET-0062
date: 2026-08-30
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0004, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0029, XASSET-0030, XASSET-0041, XASSET-0042, XASSET-0044, XASSET-0045, XASSET-0049, XASSET-0050, XASSET-0053, XASSET-0060, XASSET-0061]
supporting_artifact: test_level1_stage1_pr362_lifecycle_provenance_correction.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every value supplied to this session. Every fact below was independently re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `3db918530b10ffc1423ba0b749b086e349a4901d` |
| Worktree | clean; zero open pull requests |
| PR #362 | merged and closed; merge `3db918530b10ffc1423ba0b749b086e349a4901d` |
| PR #362 merge parents | exactly two, in order: `413e033ac33741829168762ab24d73327c047d4b`, then `ccc7f433b06d5114eb7616347ce773ae4f80392c` |
| PR #362 merge drift | **zero** — merge tree `1ccbecec64ba9bae64514443cf26972bde2782a9` byte-identical to the accepted head's tree |
| Independent clean review | `5058418382` — `commit_id` `ccc7f433b06d5114eb7616347ce773ae4f80392c`, APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0/0/0/0 |
| Merge-commit CI | run `33259403778` / job `99118637390` — `push`, attempt 1, `head_sha` **the exact merge SHA**, `completed`/`success`, 10/10 steps |
| Retained "principal acceptance" `5463146940` | derived `user.login` **`claude[bot]`**, `type` **`Bot`**, `author_association` **`CONTRIBUTOR`**, `performed_via_github_app.slug` **`claude`** |
| Immediate post-merge verification comment | **none exists** — no PR #362 issue comment between merge `15:07:49Z` and closure `5463232454` at `15:24:01Z` |
| Independent lifecycle audit | `5466422998` — `Mast3rkey` / `User` / `OWNER`, via `chatgpt-codex-connector`; **2 BLOCKING**; `XASSET-0061 EFFECTIVITY NOT ESTABLISHED` |
| `XASSET-0061` | `status: Proposed`; catalog entry present; **effectivity not established** |
| Lane state | exactly **`ABSENT`**; `AUTHORIZATION_ROOT` and all four lane paths **absent** |
| All three authorization predicates | **`False`** |
| `ATTEMPT_1` | **intact, unclaimed, unconsumed**; no `stage1_results.yaml` anywhere |
| `XASSET-0062` identifier | **unused** — zero occurrences in the catalog, the decision directory, all-refs history, remote branches, and all-state PR history |

`XASSET-0054` is a pre-existing catalog gap with an abandoned `xasset-0054` remote branch. It is **not**
backfilled here; `XASSET-0062` is the next sequential unused identifier.

Read in full before designing: `XASSET-0061` (all of `§§A–L`), `XASSET-0042` (all of `§§A–K`),
`OPS-0004`, `OPS-0007` `§1`, `OPS-0009` `§§1–2`, `§6`, `§9`, and `OPS-0014` `§D`, plus the production
mechanism's own `REQUIRED_LIFECYCLE_GATES`, actor constants, and chronology gates.

### What this unit is

The `Lane G` governance correction the independent audit's "Required next unit" section demands. It
**records** two lifecycle defects, **determines** whether each can lawfully be cured, and **defines**
the one ratification mechanism that may cure the curable one. It rewrites nothing.

## Decision

### A. Determination — `PR362_LIFECYCLE_DEFECTS_RECORDED_XASSET_0061_NOT_EFFECTIVE`

Both audit findings are **independently confirmed and accepted in full**.

1. **Defect 1** — the retained principal acceptance is API-attributed to Claude, not to the principal.
   **Curable in principle**, by a ratification narrowly modelled on `XASSET-0042`, defined in `§G`.
2. **Defect 2** — no retained evidence establishes that an immediate post-merge verification occurred
   when it was required to occur. **Not curable.** `§F` states why, from governing text.

Because `§J` condition 5 is one of seven conjunctive conditions and cannot be established,
**`XASSET-0061` is NOT effective, and cannot be made effective for its own lifecycle.** Its one-shot
link-3 authority is **unavailable and unconsumed**.

#### A.1 — The distinction any summary of this filing must preserve

> `XASSET-0062` **records** two PR #362 lifecycle defects and **determines** that `XASSET-0061` is
> **not effective**. It **defines** a ratification for the acceptance-actor defect only. It does
> **not** restore `XASSET-0061`, does **not** authorize the link-3 readiness verification, and does
> **not** grant any actor, bot, or application standing authority.

**Curing defect 1 does not restore effectivity.** A reader who takes the ratification in `§G` as
re-enabling `XASSET-0061` has inverted this decision. The ratification closes a record-integrity
finding; `§F` independently and separately forecloses effectivity.

### B. The two defects, recorded exactly

Recorded as they are. Nothing here is rewritten, sanitized, softened, or deleted.

**Defect 1 — the acceptance record is bot-attributed.** Comment `5463146940` derives live as
`claude[bot]` / `Bot` / `CONTRIBUTOR`, posted through the `claude` application. Its body asserts that
it records the principal's acceptance verbatim. That assertion may well be true as a matter of fact —
the principal did accept in session — but **body text is not actor evidence**, and this repository's
own mechanism takes identity solely from `_actor_login`, never from prose (`XASSET-0042` `§D` row 3).
No pre-merge record from the principal supplies the missing attribution.

**Defect 2 — no immediate post-merge verification evidence was retained.** PR #362 merged at
`2026-08-29T15:07:49Z`. The next issue comment of any kind is the final closure `5463232454` at
`15:24:01Z`, after merge-commit CI completed at `15:18:50Z`. The closure asserts an earlier check
occurred. **A later assertion cannot independently establish its own timing.**

**Authored by the same session that committed both defects.** This filing is written by the session
that performed the PR #362 merge and posted `5463146940` and `5463232454`. That is disclosed here
rather than left to inference, and it is exactly why this filing may not review, accept, or merge
itself.

### C. A finding the audit did not reach — the derived triple is **not** sufficient

The audit's Blocking 1 rests on `5463146940` deriving as `claude[bot]` / `Bot` / `CONTRIBUTOR`. That
is correct. But re-deriving every PR #362 record and three hundred repository comments shows the
converse does **not** hold: **`Mast3rkey` / `User` / `OWNER` does not establish principal authorship
in this repository.**

| Record | Derived actor | App | Actually authored by |
|---|---|---|---|
| `5458336219`, `5458339193`, `5458342463` (PR #362) | `Mast3rkey` / `User` / `OWNER` | `claude` | **Claude** — each says so in its own body |
| `5460442068`, `5460443686`, `5460445104` (PR #362) | `Mast3rkey` / `User` / `OWNER` | `claude` | **Claude** |
| `5463146940` (PR #362 acceptance) | `claude[bot]` / `Bot` / `CONTRIBUTOR` | `claude` | **Claude** |
| `5449752973` (`XASSET-0060` acceptance, PR #361) | `Mast3rkey` / `User` / `OWNER` | `claude` | **Claude** |
| `5345229177` (`XASSET-0042` ratification, PR #341) | `Mast3rkey` / `User` / `OWNER` | `claude` | posted through the Claude application |
| `5466422998` (this audit) | `Mast3rkey` / `User` / `OWNER` | `chatgpt-codex-connector` | **the independent reviewer** |

Three consequences follow, and each is load-bearing.

1. **What changed in PR #362 was the surface, not the substance.** Claude-posted lifecycle records
   have derived as `Mast3rkey` / `User` / `OWNER` throughout this chain. In PR #362 the credential
   surfaced as `claude[bot]` instead, which is what made the authorship *visible*. The defect the
   audit found is **newly visible, not newly committed**.
2. **`XASSET-0042`'s ratification test would not distinguish these cases.** That mechanism requires
   the ratification's derived `user.login` to be `Mast3rkey`. Every row above except one satisfies
   that. A ratification predicate built on the triple alone is therefore satisfiable by Claude.
3. **The reviewer also derives as `Mast3rkey` / `User` / `OWNER`.** A predicate on the triple alone
   would let the independent reviewer's own comment satisfy a principal-ratification gate, collapsing
   two roles `OPS-0007` `§1`.1 requires to stay separate.

`performed_via_github_app` is therefore **not optional colour** — it is necessary evidence, and `§G`
requires it. **It is not, by itself, sufficient.**

**Corrected by the independent supplement `5060793954`, from a counterexample that did not exist until
the review did.** Review [`5060791095`](https://github.com/Mast3rkey/Portfolio-HQ/pull/363#pullrequestreview-5060791095)
— authored and posted by ChatGPT/Codex — reads back as `Mast3rkey` / `User` / `OWNER` with
`performed_via_github_app` **null**, on `commit_id` `ca099915…`. Those are exactly the four fields an
earlier draft of `§G` required, so that draft's predicate **accepted the independent reviewer**. That
is the very reviewer/principal collapse this filing exists to close.

The root cause is structural, and re-deriving it from live GitHub gives the fix:

| Record type | `performed_via_github_app` key | `issue_url` | `pull_request_url` | `pull_request_review_id` | canonical `url` |
|---|---|---|---|---|---|
| **issue comment** | **present** (null for a direct principal act) | present | absent | absent | `…/issues/comments/<id>` |
| pull-request review | **absent entirely** | absent | present | absent | none |
| review comment | **absent entirely** | absent | present | present | `…/pulls/comments/<id>` |

A `.get()` on an **absent** key returns `None`, so an "app is null" test is **vacuous for every review
and every review comment**. The discriminator is therefore not the app field alone but the **record
kind**, read from canonical API fields. `§G` now requires the app key to be **explicitly present and
null**, and validates the record kind, the repository/PR association, the record id, and a canonical
fingerprint besides.

**The required standard is this repository's own earlier practice, since abandoned.** A first draft of
this section recorded that no comment in the last hundred carried no application, and inferred that a
directly attributable principal comment had never occurred here. Widening the scan to three hundred
comments **disproved that inference**, and the corrected finding is materially stronger.

**Twenty-six** comments carry **no application at all** — direct principal acts — and they include
complete lifecycle records of exactly the shape `§G` requires:

| Record | Date | PR | Kind |
|---|---|---|---|
| `5279583728` | 2026-08-13 | #310 | principal exact-head acceptance |
| `5279649213` | 2026-08-13 | #310 | post-merge verification |
| `5280867232` | 2026-08-13 | #311 | principal exact-head acceptance |
| `5280945019` | 2026-08-13 | #311 | post-merge verification |
| `5289500944` | 2026-08-14 | #314 | principal exact-head acceptance |
| `5289558762` | 2026-08-14 | #314 | post-merge verification |
| `5299933404` | 2026-08-15 | #316 | principal exact-head results acceptance |
| `5301699393` | 2026-08-15 | #319 | principal exact-head acceptance |
| `5301728726` | 2026-08-15 | #319 | post-merge verification |

Every one derives as `Mast3rkey` / `User` / `OWNER` with **no** `performed_via_github_app`. So the
`§G` standard is **not** a novel burden invented by this filing: it is the standard this repository
actually met through 2026-08-15, on both gates, and which later drifted to application-posted records
without any decision authorizing the change. `§I` restores it prospectively rather than inventing it.

**This finding is scoped to PR #362.** That `5449752973` and `5345229177` share this provenance
character is recorded as fact because it is directly relevant to designing a predicate that works.
This filing **does not** reopen, re-adjudicate, void, or reclassify `XASSET-0042`, `XASSET-0060`, or
any other closed unit, and authorizes no successor to do so.

### D. Defect 1 — the `XASSET-0042` precedent, examined narrowly

`XASSET-0042` is the only precedent in this repository for curing a bot-attributed lifecycle record,
and it is examined here **as a precedent for one defect class**, never as a general exception.

What it holds, and what this filing reuses:

- a principal may **ratify history as it stands**, retrospectively — ratifying and rewriting are
  different acts, and only the first is available (`XASSET-0042` Rationale);
- the exception is a **conjunction over independent evidence families**, pinned to one PR's exact
  identities, and yields the all-false result for every other document (`§C`);
- identity comes from `_actor_login` alone, never from body text (`§D` row 3);
- records are authenticated by **canonical-JSON fingerprints**, because token presence authenticated a
  record that explicitly voided itself (`§J` MAJOR 1);
- the ratification must be **retrospective** — strictly postdating the merge it ratifies (`§J` MAJOR 2);
- no bot is ever classified as an accepted actor; there is no allow-list and no trusted-automation
  class (`§D` row 2).

What this filing **adds**, because `§C` shows the precedent is insufficient as written: the
ratification's `performed_via_github_app` must be **absent**. Without that conjunct the predicate is
satisfiable by the very author whose attribution is in question.

What this filing **does not** take from the precedent: `XASSET-0042` cured records that **existed**
with the wrong actor. That is defect 1's shape. It is **not** defect 2's shape, and `§E` explains why
the precedent does not reach it.

### E. Defect 2 — what the governing text actually requires

Two distinct standards apply, and conflating them would either overstate or understate the defect.

**`OPS-0009` `§9` separates the act from its recording.** The verification "must be performed
immediately, by the same session that performs the merge, and must never be deferred to a later,
unrelated session," while "the fact of a completed verification may still be *recorded* via the next
filing that already touches the relevant register... **What changes is *timing*: the check itself is
never left for whoever happens to open the next PR.**"

Under `§9` alone, then, the absence of a separately timestamped comment is **not itself** a packaging
violation. Recorded plainly, because it would be easy — and wrong — to overstate the finding.

**But the evidence of the act's timing is unretained.** The substantive content of a post-merge
verification is re-derivable now and forever, because it rests on immutable facts: two ordered merge
parents, a merge tree byte-identical to the accepted head's, an exact merged file scope, protected-path
byte-identity, and a green CI run pinned to the merge SHA. **The temporal fact is not.** Nothing
retained establishes that those checks were run immediately rather than reconstructed later, and no
future act can change that.

**`OPS-0004` governs exactly this situation and forecloses retroactive cure.** Its Finding FA-1 was a
lifecycle claim resting on unretained prose authored by the same identity as the audited work — this
defect's precise shape. `OPS-0004` item 2 holds: "This decision does not manufacture that missing
retroactive evidence; **it cannot**." It closed the gap "**prospectively**, ... **without claiming to
authenticate the original prose retroactively**," and added a forward rule (item 5) so the gap could
not recur silently. It expressly declined to dispute the underlying work, which independent
verification had found sound.

**`XASSET-0061` `§H` makes the consequence explicit.** "Any... missing evidence, ambiguity, ... or fact
the unit cannot re-derive with certainty" is a stop, and "**Uncertainty is failure.** The unit may not
resolve an ambiguous state in favour of readiness, and may not treat an unobtainable fact as silent
agreement."

**Determination, stated explicitly as required.** A current re-verification plus provenance
reconciliation **cannot lawfully cure the missing immediate-verification evidence.** It can establish
every substantive fact and it can close the gap prospectively; it **cannot** establish that the act
occurred when it was required to occur. Under `OPS-0004`, that is not a gap this or any later filing
is able to close retroactively.

**Two paths are closed, and named so no successor reopens them.** A verification comment posted now
would postdate closure `5463232454`, and the production mechanism requires a closure to postdate the
verification it closes — "a closure cannot precede what it closes." And backdating, relabelling the
later closure as the immediate record, or treating the merging session's own narrative as evidence of
its own timing are each forbidden outright: the first two are fabrication, the third is the exact
failure `OPS-0004` FA-1 identified.

### F. Consequence — `XASSET-0061` is not effective

`§J` of `XASSET-0061` requires **all seven** conditions and states that "**None is individually
sufficient**." Condition 5 cannot be established (`§E`). Condition 3 is defective (`§B`), and although
`§G` can cure it, **curing one conjunct of a conjunction that fails on another changes nothing.**

Therefore, and this is the operative holding:

- **`XASSET-0061` is NOT effective.** Its `§J` lifecycle did not close and cannot be made to have
  closed.
- **Its link-3 authority is unavailable and unconsumed.** No readiness verification may be performed
  under it, and no `PASS` or `FAIL` may be issued under it.
- **`XASSET-0061` is not void, and its reasoning is not disputed.** Its independent review was clean
  at the exact head, its merge is drift-free, and its merge-commit CI is green — all independently
  re-derived above. What failed is lifecycle evidence, not substance. Its `status` therefore remains
  `Proposed`, unchanged by this filing.
- **A future link-3 unit requires a new authorization** with its own clean lifecycle. That unit is
  **not** authorized here, not drafted here, and not scheduled here.

### G. The ratification this correction requires — pinned to this exact history only

One ratification is required **on this corrective pull request**, and it may cure **only** defect 1.

#### G.1 — Record kind: one canonical top-level issue comment on PR #363

The ratification is **exactly one top-level GitHub issue comment on pull request #363**. Its kind and
its repository/PR association are validated from canonical API fields, never inferred from prose:

1. `issue_url` is exactly `https://api.github.com/repos/Mast3rkey/Portfolio-HQ/issues/363`;
2. `url` is exactly `https://api.github.com/repos/Mast3rkey/Portfolio-HQ/issues/comments/<id>`;
3. `html_url` is exactly `https://github.com/Mast3rkey/Portfolio-HQ/pull/363#issuecomment-<id>`;
4. `id` is an integer, and the **same** `<id>` appears in both `url` and `html_url`;
5. the record carries **none** of `pull_request_url`, `pull_request_review_id`, `commit_id`,
   `diff_hunk`, `path`, or `position`.

**Rejected outright by these fields:** pull-request reviews, inline review comments, commit comments,
comments on any other issue or pull request, and records whose canonical URLs are malformed or
disagree with each other or with `id`.

**These fields do not, and cannot, prove live GitHub origin.** A caller can assemble a dictionary that
satisfies every clause above — this filing's own fixtures do exactly that. An earlier draft claimed
these fields reject "any synthetic record a caller assembles"; that claim was **false and is withdrawn**
under DELTA review `5061031729` BLOCKING 2. Origin is established by `§G.9` readback and retained
evidence, never by record shape.

#### G.2 — Actor and provenance: four conjuncts, each necessary, none sufficient alone

1. derived `user.login` is exactly `Mast3rkey`;
2. derived `user.type` is exactly `User`;
3. derived `author_association` is exactly `OWNER`;
4. the `performed_via_github_app` key is **present and null** — not merely absent. An absent key is
   the signature of a review or review comment (`§C`), so absence must fail rather than pass.

`§G.1` and `§G.2` are **conjunctive**. Neither alone is sufficient: `§C`'s counterexample satisfies
`§G.2` and fails `§G.1`.

#### G.3 — Scope: an exact affirmative declaration, parsed, never a substring scan

The ratification governs this exact history and nothing else, pinned to: PR **#362**; accepted head
`ccc7f433b06d5114eb7616347ce773ae4f80392c`; independent review `5058418382`; bot-attributed acceptance
`5463146940`; merge `3db918530b10ffc1423ba0b749b086e349a4901d`; final closure `5463232454`; and the
independent stop `5466422998`.

These pins are **fixed constants of this decision**. An earlier draft passed them in a caller-supplied
dictionary the record never authenticated, so any record could be paired with any scope; that is
removed, and no scope, id, or fingerprint is selectable by a caller of the operational predicate.

**Corrected under DELTA review `5061031729` BLOCKING 2.** An intermediate draft asked only whether each
pin appeared as a **substring** somewhere in the body. The reviewer built a canonical, principal-shaped
issue comment whose body began *"I do NOT ratify or accept anything. References only:"*, listed all
seven pins, and bound it to its own id and its own freshly computed fingerprint — and the complete
predicate returned `True`. A fingerprint authenticates an already-valid record **against later edits**;
it can never make an **initially bound** refusal affirmative, because it is computed over whatever the
body said at binding time. The defect was upstream of the fingerprint, and so is the fix.

The body must now **parse**, in full, as this exact declaration — a header line followed by nine
`key: value` pairs, each key exactly once, every fixed value exact:

```
XASSET-0062 RATIFICATION
action: RATIFY-AND-ACCEPT
pr363_accepted_head: <the exact final PR #363 head, 40 lowercase hex>
pr362_pull_request: 362
pr362_accepted_head: ccc7f433b06d5114eb7616347ce773ae4f80392c
pr362_independent_review: 5058418382
pr362_bot_acceptance: 5463146940
pr362_merge: 3db918530b10ffc1423ba0b749b086e349a4901d
pr362_closure: 5463232454
pr362_independent_stop: 5466422998
```

**Any other line rejects the whole body** — prose, a preamble, a `VOID` marker, a reference list, an
unknown key, a duplicated key, or trailing contradictory material. There is no substring matching
anywhere in the parser. A refusal, a reference-only record, a negated or aliased `action`, a truncated
or extended pin value, and a valid declaration wrapped in contradicting prose **all fail**, and each is
pinned by its own regression.

`pr363_accepted_head` is validated **by form only** — 40 lowercase hex. The repository cannot know its
own future final head, so that value's correctness against the real final head is established by the
`§G.9` readback, never from inside this repository.

**Body text still never establishes actor identity or record kind** — those come solely from the
canonical fields in `§G.1`/`§G.2`.

#### G.4 — Identity binding: read back from GitHub, never committed to this repository

Following the `XASSET-0042` `§J` safeguard this decision reuses — where token presence alone
authenticated a record that explicitly voided itself — the ratification is authenticated by a
**canonical-JSON SHA-256 fingerprint** over its own identity-bearing fields: `id`, `url`, `html_url`,
`issue_url`, `user.login`, `user.type`, `author_association`, `performed_via_github_app`, `created_at`,
and the SHA-256 of the body — sorted keys, fixed separators, never a `repr` of a mapping.

**Corrected under DELTA review `5061031729` BLOCKING 1.** An earlier draft required the operator to
retain that binding "in a further ordinary fast-forward correction commit on this pull request", while
`§J` simultaneously required the ratification to sit at the **final accepted head**. Those two
requirements cannot both hold: the binding commit *changes* the head the ratification just accepted,
which reopens the exact-head requirement, and binding the replacement record changes it again. The
lifecycle could not close. **The binding commit is withdrawn.**

**The binding is never committed to this repository.** `BOUND_RATIFICATION_ID` and
`BOUND_RATIFICATION_FINGERPRINT` are `None` and **stay** `None`; the fingerprint is computed and
compared **outside** the repository, against the record read back from the GitHub API, and retained as
GitHub lifecycle evidence under `§G.9`. The in-repository predicate therefore returns `False` for every
input **by design, permanently** — it establishes the required *shape* and rejects the refusal,
substring, alias, and self-binding classes, and it is never the thing that certifies a live record.

**A dictionary-shape predicate cannot prove live GitHub origin.** This filing's own fixtures are
caller-assembled and satisfy every structural clause, which is precisely why structural completeness is
separated from origin in the mechanism (`_ratification_is_structurally_complete` versus `§G.9`
readback). An earlier `§G.1` sentence claiming canonical fields reject "any synthetic record a caller
assembles" was **false and is withdrawn**.

#### G.5 — Retrospection

The ratification must strictly postdate the PR #362 merge. It ratifies history; it does not manufacture
a pre-merge event, and nothing here weakens any chronology rule.

#### G.6 — Claude must not write or post it

This filing's authoring session does not compose it, does not post it, and posts no text intended to be
adopted as it.

#### G.7 — The independent reviews are review evidence only

`5060791095` and `5060793954` are **independent review evidence and nothing else**. They are **not**
principal acceptance, **not** ratification, and **not** capable of becoming either — under `§G.1` a
pull-request review is a rejected record kind, and under `OPS-0007` `§1`.1 the reviewer is not the
principal. The same holds for every future review on this pull request.

#### G.8 — What it does and does not establish

It establishes that the principal affirms, on the record and under their own attribution, that the
acceptance recorded at `5463146940` reflects their decision at the accepted head. It establishes
**nothing** about defect 2, and it does **not** make `XASSET-0061` effective (`§F`).

#### G.9 — The closed lifecycle sequence

Stated explicitly so nothing is left to inference:

1. The repository reaches its **final clean reviewed head** `H`, with independent exact-head review
   satisfied at `H` and **no further repository commit** contemplated.
2. The principal posts **one** canonical top-level issue comment on PR #363 that **both** accepts that
   exact head `H` **and** ratifies the pinned PR #362 history — a single act, not two. Its body is the
   exact `§G.3` declaration, whose `pr363_accepted_head` field names `H` itself, so the record carries
   its own PR #363 head anchor and the acceptance is auditable against a specific commit.
3. A coordinator **independently reads that comment back from the GitHub API** and retains, as a
   separate GitHub lifecycle-evidence comment: its `id`, `created_at`, canonical-JSON fingerprint,
   record kind, derived actor, `author_association`, and application provenance.
4. **That readback requires no repository commit and does not change the accepted head.** `H` is still
   the head that was reviewed, still the head that was accepted, and still the head that merges.
5. Normal merge, immediate post-merge verification under `§I.2`, merge-commit CI at the exact merge
   SHA, and closure then proceed.

Because acceptance and ratification are **one** record naming `H`, no question arises about whether a
pre-binding ratification survives a later head change: there is no later head change. The single-act
construction is what makes the sequence closed, and it is why the two-act alternative was rejected
rather than merely left undescribed.

### H. No standing authority is created for any actor, bot, or application

Stated absolutely. `claude[bot]`, the `claude` application, `chatgpt-codex-connector[bot]`, the
`chatgpt-codex-connector` application, ChatGPT/Codex, and every other automation are **not** granted
standing to act as the principal, in this filing or by implication from it. No accepted-actor list, no
bot class, and no trusted-automation category is created. `PRINCIPAL_ACCOUNT_LOGIN` and
`LIFECYCLE_OPERATOR_LOGIN` are unchanged. The `§G` mechanism is a **conjunction pinned to one closed
history**; it admits no future document, and it may not be cited as precedent for admitting one.

### I. Forward evidentiary rule — two gates, two roles

Modelled on `OPS-0004` item 5, and prospective only. **Corrected under independent review
`5060791095` MAJOR 1**, which found that an earlier draft applied one direct-principal predicate to
both gates and thereby collapsed two roles `OPS-0009` `§8` keeps distinct.

#### I.1 — Principal exact-head acceptance and the `§G` ratification: principal-only

From this decision's merge forward, a record satisfying a **principal exact-head acceptance** gate, or
the `§G` ratification, is complete only when it satisfies **`§G.1` and `§G.2` in full** — the canonical
top-level issue-comment record kind, and the four actor/provenance conjuncts including a
`performed_via_github_app` key that is **present and null**.

**No application-attributed record can satisfy this gate**, and neither can a pull-request review,
however its actor derives.

#### I.2 — Immediate post-merge verification: principal *or* designated merge coordinator

`OPS-0009` `§8` expressly authorizes "**the principal or a designated merge coordinator**" to mark
ready, merge, and perform post-merge verification, and `§9` requires that verification to be performed
**immediately, by the same session that performs the merge**. Those provisions are **preserved intact
and are not superseded here.**

A record satisfying the **immediate post-merge verification** gate is therefore complete when:

1. it is retained by **either** the principal **or** the designated merge coordinator that actually
   performed the merge;
2. its derived actor and application provenance are **honest** — an application-attributed coordinator
   record must read back as what it is, and must be disclosed as such, never dressed as a principal
   act; and
3. its **GitHub timestamp is strictly after the merge and strictly before final closure**, so its
   timing is established by GitHub's own record rather than by later narrative.

**An application-attributed coordinator record satisfies the verification-evidence role only.** It is
**never** principal acceptance and **never** a `§G` ratification — `§I.1` governs those, exclusively.

**This creates no permanent direct-principal requirement for mechanical post-merge verification.** An
earlier draft did, which would have forced a second synchronous principal record after every merge even
where the authorized coordinator had performed and retained the check — a cross-cutting workflow
restriction outside this unit's scope. Removing a coordinator's authority would require its own
separately authorized amendment expressly superseding `OPS-0009` `§8`; **this filing is not that
amendment.**

#### I.3 — What the rule does not do

Item 2 of the earlier draft — a verification claim made only in a later comment does not by itself
satisfy the gate — is **retained**, and is exactly the PR #362 defect. **This rule is prospective.** It
reopens, re-adjudicates, and reclassifies no closed unit, and the nine historical direct-principal
records in `§C` are cited as evidence of prior practice, never as a demotion of the coordinator role
`OPS-0009` `§8` grants.

### J. Effectivity

Effective only after **all** of the following complete for this decision's final accepted head and the
resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` `§1`;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. **one genuine principal record that both accepts the exact final head and ratifies the pinned
   PR #362 history**, satisfying `§G.1` (canonical top-level issue-comment record kind on PR #363),
   `§G.2` (all four actor/provenance conjuncts, including an app key present and null), and `§G.3`
   (the exact affirmative declaration, whose `pr363_accepted_head` names that final head) in full —
   with its live id, timestamp, canonical-JSON fingerprint and provenance **read back from the GitHub
   API by a coordinator and retained as GitHub lifecycle evidence under `§G.9`, with no repository
   commit and no change to the accepted head**;
4. normal merge;
5. an **actually retained** immediate post-merge verification, satisfying `§I.2` — retained by the
   principal **or** the designated merge coordinator that performed the merge, with honest derived
   provenance, and posted strictly between the merge and the closure so its timing is established by
   GitHub's timestamp and not by narrative;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA**;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request authorizes nothing; a green PR-head CI
run does not; principal acceptance does not; merge does not. Condition 5 is stated in this stronger
form deliberately: it is the defect this filing exists to record, and this filing must not commit it.

**Merging this correction leaves Stage 1 `UNARMED` and `NOT EXECUTABLE`, creates no lane state, claims
no `ATTEMPT_1`, executes nothing, and does not make `XASSET-0061` effective.**

### K. Absolute non-authorization

This decision performs and authorizes no readiness verification and issues no `PASS` or `FAIL`. It
does not restore, revive, or re-enable `XASSET-0061`. It authorizes no link 4 and no link 5. It
generates no `XASSET-0029` attestation; creates no `AUTHORIZATION_ROOT`, `READY`, `CLAIMED` or
`COMPLETED` lane state or ledger entry; arms, claims, completes, executes or recovers nothing; consumes
no part of `ATTEMPT_1`; evaluates no gate for any registered construction; creates no
`stage1_results.yaml`, per-construction disposition, cell outcome or roll-up. It acquires no market,
fundamental, economic or Stage-2 data and reads no protected `RISK` result. It creates no endpoint,
bound, point, range, **percentage**, weight, rank, target or allocation. It changes no byte of
`level1_stage1_execution_authorization.py`, of any of the **twenty-five** load-bearing paths, of
`PROTOCOL_V1.md`, of `pre_registration.yaml`, of the runner, of the result validator, or of the
construction universe; and no byte of `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, the allocator, or margin state. It authorizes no chart, ladder, deployment,
trade, order, or brokerage action. It consumes no part of `XASSET-0027` `§P.1`, which **remains
reserved and unspent**. It corrects no parser and alters no parser semantics. It reopens neither B1,
B2, nor B3. It **authorizes no successor unit of any kind**, including the new link-3 authorization
`§F` says would be required.

## Rationale

The audit is right on both findings, and the more useful question is why the second is harder than the
first.

Defect 1 is a **record-integrity** failure: an act occurred and was recorded under the wrong
attribution. `XASSET-0042` already established that the honest repair is ratification — the principal
affirms the history as it stands, retrospectively, under their own attribution. Nothing is invented.

Defect 2 is an **evidentiary** failure of a different kind: what is missing is not the right label on a
record but the record itself, and specifically its timestamp. `OPS-0004` confronted this exact shape
and was explicit that it "cannot" manufacture missing retroactive evidence. That holding is what makes
this decision's answer unavoidable. Curing defect 2 would require either fabricating a timestamp,
relabelling the later closure as something it is not, or accepting the merging session's own narrative
as evidence of its own timing — and that last is precisely the failure `OPS-0004` FA-1 identified in
a claim that turned out, on independent check, to be substantively correct. Being substantively
correct was not enough there, and is not enough here.

Hence the asymmetry: ratify what can be ratified, and refuse to pretend about the rest. `XASSET-0061`
stays ineffective not because its reasoning is doubted — its review was clean, its merge drift-free,
its CI green — but because effectivity was defined as a conjunction of seven evidenced conditions, and
one of them is permanently unevidenced. A governance system that lets a conjunction pass on six of
seven because the seventh is inconvenient has stopped being one.

`§C` is the part a future session is most likely to need. The obvious repair — "require
`Mast3rkey` / `User` / `OWNER`" — is the repair that does not work here, because Claude's own comments
have derived as exactly that triple throughout this chain, including the acceptance of the immediately
preceding unit and the ratification of the precedent this filing relies on. Only
`performed_via_github_app` separates the principal from the two automations that write in this
repository. Recording that finding is worth more than the ratification it enables.

That section also carries a correction to this filing's own first draft, kept visible rather than
quietly amended. The draft inferred, from a hundred-comment scan, that a direct principal comment had
never occurred here — and a three-hundred-comment scan disproved it. The nine records in `§C`'s table
show the opposite: this repository met the `§G` standard on both gates through 2026-08-15 and then
drifted away from it with no decision authorizing the drift. That reframes `§I.1` from imposing a new
burden to restoring a lapsed one, and it is a better answer than the one the draft would have shipped.

`§I`'s split follows the same discipline in the opposite direction. An earlier draft applied one
direct-principal predicate to both gates, which would have forced a second synchronous principal record
after every merge even where `OPS-0009` `§8`'s designated merge coordinator had performed and retained
the check `§9` requires of it. Tightening the principal gate is this unit's business; silently removing
a coordinator role granted by a different accepted decision is not. The two gates are therefore
separated: `§I.1` stays principal-only and gets stricter, `§I.2` preserves the coordinator role and
constrains it by honest provenance and a GitHub-established timestamp instead.

## Alternatives considered

**Treat the closure comment's assertion as satisfying condition 5.** Rejected. It is the merging
session's own narrative about its own timing, which `OPS-0004` FA-1 refused in materially identical
circumstances, and `XASSET-0061` `§H` independently forbids resolving the ambiguity toward readiness.

**Post an immediate-verification comment now and treat the lifecycle as complete.** Rejected twice
over: it would postdate the closure that already exists, which the production mechanism rejects
outright; and it would assert a timing that did not occur.

**Relabel closure `5463232454` as the immediate verification record.** Rejected. It was posted after
CI, says so, and renaming a record to fit a gate is exactly the history rewriting this filing is
required not to perform.

**Require only `Mast3rkey` / `User` / `OWNER` for the ratification, matching `XASSET-0042`.** Rejected
on evidence — `§C` shows that predicate is satisfiable by Claude and by the independent reviewer.

**Add the app conjunct and stop there.** Rejected on a live counterexample: the independent review
`5060791095` satisfies exactly that predicate. Record kind, canonical repository/PR association, record
id, and a canonical fingerprint are all required besides.

**Keep the caller-supplied scope dictionary.** Rejected — the record never authenticated it, so any
record could be paired with any scope. The pins are now fixed constants of this decision, and the
ratification's own body must name them.

**Apply the direct-principal predicate to post-merge verification too, for consistency.** Rejected —
`OPS-0009` `§8` grants a designated merge coordinator that role and `§9` requires it of whoever merges.
Removing it needs an amendment expressly superseding `OPS-0009`, which this filing is not.

**Void `XASSET-0061`, or mark it `Accepted` on the strength of its clean review and green CI.**
Both rejected. The first overreaches: independent review found its substance sound, and no finding
disputes it. The second is the failure this filing exists to prevent — effectivity is the conjunction,
not the merge.

**Also cure `XASSET-0060` and `XASSET-0042`, whose acceptances share the same provenance character.**
Rejected as scope this filing has no authority over. It is disclosed in `§C` as fact and left to any
separately authorized unit that chooses to take it up.

**Fold the replacement link-3 authorization into this filing, since `§F` shows one is needed.**
Rejected. That is a separate grant requiring its own authority, its own review, and its own lifecycle;
combining them is the collapse `XASSET-0042` and `XASSET-0061` `§K` each forbid.

## Consequences

The PR #362 lifecycle record is accurate for the first time: two defects are recorded as they are, the
curable one has a defined and narrowly pinned ratification, and the incurable one is stated as
incurable rather than quietly assumed closed. `XASSET-0061` remains `Proposed` and **not effective**;
its link-3 authority remains unavailable and unconsumed; the readiness verification remains unperformed
and unauthorized. A future link-3 unit needs a new authorization, which this filing does not grant.

Going forward, `§I.1` requires principal-acceptance and `§G` ratification records to be canonical
top-level issue comments on the pull request in question, carrying direct principal attribution with a
`performed_via_github_app` key present and null — a pull-request review can never satisfy it. `§I.2`
leaves `OPS-0009` `§8`'s designated-merge-coordinator role intact for immediate post-merge
verification, subject to honest provenance and a GitHub-established timestamp strictly between merge
and closure. No closed unit is reopened, reclassified, or disputed by either rule, and `OPS-0009` is
neither narrowed nor superseded.

Stage 1 remains `UNARMED` and `NOT EXECUTABLE`. Lane state remains `ABSENT`. All three authorization
predicates remain `False`. `ATTEMPT_1` remains intact, unclaimed, and unconsumed. `XASSET-0027` `§P.1`
remains one, reserved, and unspent.
