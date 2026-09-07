---
decision_id: XASSET-0036
date: 2026-08-17
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_gb_executable_package_authorization.py
---

## Context

### Live preflight

Independently verified from live GitHub, live git, and live module state before any file was written.
Nothing below is inherited from a prior session's summary.

| Fact | Verified value |
|---|---|
| GitHub `main`, `origin/main`, local `HEAD` | `ed3f062f86607574291428ea2345d2cba78b3a02` — all three identical |
| That commit's identity | the `XASSET-0035` merge (PR #334), parents `a39f8e13…` and `369139a1…`, both re-derived via `git log --pretty='%H %P'` |
| Merge-tree drift | **zero** — merge tree `0fb7ac35…` is byte-identical to the accepted head's own tree |
| `XASSET-0035` final review | `4951982716`, `APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE`, 0 BLOCKING / 0 MAJOR / 0 MINOR / 1 NOTE |
| `XASSET-0035` merge-commit CI | workflow run `32035476253`, **`head_sha` = `ed3f062f…` = the exact merge SHA**, `completed` / `success` |
| Open pull requests | **0** |
| Working tree · stash · worktrees | clean · empty · sole worktree, no competing mutation lane |
| `XASSET-0036` identifier | unused — 0 hits in `governance/decisions.yaml`, no decision file, no code reference |
| Canonical pins | `PROTOCOL_V1.md` `6c34cbbc…64cb` · `pre_registration.yaml` `6e0c07a8…337c` — **both match** |
| Frozen universe | **680** constructions · **48** cells · `73c0965e…5224` — **match** |
| `LOAD_BEARING_RELPATHS` | exactly **6**, unchanged; **no runner or result-production path among them** |
| `stage_1_executability.executable` | `False`, with `executable_is_never_the_authorization_source: True` |
| `new_execution_is_authorized()` | `(False, …)` — "no attestation present" |
| `AUTHORIZATION_ROOT` (`/var/tmp/phq-endpoint0001-stage1-authorization`) | **absent** |
| `ATTEMPT_1` (`ENDPOINT-0001::STAGE_1::ATTEMPT_1`) | intact, unclaimed, unconsumed |
| ENDPOINT Stage-1 runner · result writer · `stage1_results.yaml` · claim · completion · ledger | **none exists** |

The only `runner`, `result_validator`, and `attestation` modules in the repository
(`risk_level1_runner.py`, `risk_level1_result_validator.py`, `risk_level1_attempt2_attestation.py`)
belong to the separate, protected `RISK-0001` lane. **No `risk_lane_boundary` protected result path was
read, listed, opened, or referenced by this unit**, and none of those modules is an `ENDPOINT-0001`
Stage-1 artifact.

### The question this unit answers

`XASSET-0035`'s lifecycle closed in full, so `XASSET-0030` §G.B is **semantically** unlocked: its step 1
("resolve all required §G.A semantic/governance prerequisites") is satisfied.

A read-only implementation preflight then found that **§G.B is unlocked but not authorized**. Every
filing that named §G.B expressly declined to grant it, and no other accepted decision supplies the
mutation authority §G.B steps 2–7 require. A future implementing session would therefore have to infer
authority from adjacency, roadmap prose, or the word "unlocked" — exactly the inference this program has
refused at every prior step.

This unit closes that gap and does nothing else. **It authorizes; it does not implement.**

### Correction history

**Correction 1** — after independent FULL exact-head review `4952475219` at head
`e8f81f00600375a8c6d4d69177dd2457e966d54b` (`CHANGES REQUIRED` — 0 BLOCKING / 1 MAJOR / 1 MINOR / 1 NOTE).

The review **accepted the core authority determination in full**, and raised no objection to the grant,
the `XASSET-0027` §P.1 separation, the `XASSET-0029` activation model, the steps-2–7 scope, the
steps-8–11 withholding, or the seven-condition effectivity lifecycle. **None of those changed.**

- **MAJOR 1 — resolved by new §F.1.** The original §F banned validating the runner against the real
  680-construction universe outright. That conflated *reading already-frozen identities* with *deriving
  outcomes from them*, and would have made the runner's most important integrity property unprovable at
  its real boundary. §F.1 replaces the categorical ban with a two-sided boundary: read-only,
  non-outcome-producing structural traversal is authorized (§F.1(a)); every outcome-producing act stays
  absolutely prohibited (§F.1(b)). The one-shot `ATTEMPT_1` protection is not weakened.
- **MINOR 1 — PR body only.** The PR body listed "production config" in its absolute withheld summary
  while this decision correctly authorizes the §G.B steps 2/3/5 production-configuration changes.
  Corrected there. **This decision file, `operations/WORKSTREAMS.yaml`, and the `CLAUDE.md` pointer never
  carried that contradiction** — independently verified: in all three, "production configuration change"
  appears only inside the correct §P.1 reconciliation, never in a withheld list.
- **NOTE 1** — non-actionable; every boundary it named is preserved.

## Decision

### A. Determination — `G_B_IMPLEMENTATION_PACKAGE_AUTHORIZED`

**Exactly one future, separate, bounded `XASSET-0030` §G.B implementation PR is authorized**, covering
§G.B **steps 2 through 7** as one coherent pass, effective only on this decision's own complete lifecycle
closure (§H).

**Unlocked is not authorized.** `XASSET-0035` §I removed the semantic blockers; this decision supplies
the mutation authority. Both are required, and neither substitutes for the other.

§G.B **steps 8 through 11 — the successor operational-authorization / load-bearing rebinding lifecycle,
post-rebinding read-only readiness verification, fail-closed drift handling, and the external attestation,
arm, claim, and 680-construction run — are NOT authorized here.** They remain downstream of, and outside,
the implementation PR this decision permits.

### B. The authority gap, reproduced from accepted text before anything was authorized

**B.1 — §G.B is semantically unlocked.** `XASSET-0035` §I: "**§G.B step 1 is now satisfied.**" Its seven
closure conditions are each independently verified above, including condition 6's "successful merge-commit
CI whose `head_sha` is the exact merge SHA."

**B.2 — No accepted decision grants §G.B mutation authority.** Every filing that named §G.B declined it,
verbatim:

| Decision | Operative disclaimer |
|---|---|
| `XASSET-0030` §G.B | "**This decision authorizes none of G.A or G.B**, and performs no part of either." |
| `XASSET-0031` | "**No part of §G.A or §G.B is authorized by this decision, and none is performed.**" |
| `XASSET-0032` §Consequences | leaves "the §G.B invariant intact"; grants nothing |
| `XASSET-0033` | "the `XASSET-0030` §G.B canonical/enforcement pass **remains separately reserved**" |
| `XASSET-0034` §G | "Recorded as scope, **not** as authorization… **This decision authorizes none of it and performs none of it.**" |
| `XASSET-0035` §I | "What the next unit may then do — **recorded as scope, not authorization**, and performed nowhere here." … "**This decision authorizes none of §G.B and performs no part of it.**" (§K: "enters no part of §G.B") |

Six consecutive filings named the work and six declined to authorize it. **The gap is therefore not an
oversight in one filing; it is the deliberate, consistent posture of the whole sequence** — which is
precisely why it must be closed by an express grant rather than assumed closed by exhaustion.

**B.3 — `XASSET-0027` §P.1's one evaluation/results PR cannot absorb §G.B implementation.** §P.1 verbatim:

> "Only then may exactly one later PR deliver the Stage 1 evaluation: every registered construction's
> disposition, the cell outcomes, the roll-ups, the deferred §J.12 record, abstention records, the
> provenance manifest, limitations, focused tests, and hash verification. **That PR may make no
> production configuration change**, must pass `validate_stage1_results()` against the closed universe,
> and its own result lifecycle requires independent exact-head review and principal acceptance."

Three independent grounds, any one sufficient:

1. **The prohibition is dispositive.** §G.B steps 2, 3 and 5 are *production configuration changes* by
   construction — reconciling the two canonical artifacts (both pinned, both load-bearing), correcting a
   load-bearing validator, and extending the trust boundary. §P.1's PR "may make no production
   configuration change." A PR cannot both make those changes and make none.
2. **The deliverable is an output, not an implementation.** §P.1 enumerates dispositions, cell outcomes,
   roll-ups, and a results document. §G.B steps 2–7 produce none of those; they produce the canonical,
   enforcement, and executable machinery *by which* those outputs later become derivable.
3. **They sit on opposite sides of arming.** §P.1's PR "must pass `validate_stage1_results()` against the
   closed universe" — it necessarily carries a real results document, which exists only after lawful
   arming, claim, and execution (§G.B step 11). §G.B steps 2–7 complete strictly *before* the rebinding
   at step 8, which is itself before arming.

**B.4 — `XASSET-0029` §E's no-further-authorization-PR rule does not reach repository implementation
authority.** §E verbatim:

> "Arming is a **runtime operator act**, not a further merged governance PR. `XASSET-0029` is the final
> governance decision required for Stage 1; the generator is then run once, and no additional
> authorization PR is ever required. **The regress terminates because the final step changes no
> repository state.**"

The rule's own stated terminating condition is *a final step that changes no repository state* — the
runtime attestation. §G.B steps 2–7 change repository state extensively, so they are categorically
outside the step §E terminates. And `XASSET-0030` — accepted **after** `XASSET-0029` — expressly
contemplates a successor lifecycle: §D records that a lawful correction "deliberately creates enforcement
drift, and Stage 1 becomes non-armable **until a successor operational-authorization or reconciliation
lifecycle** lawfully binds the new load-bearing implementation," and §G.B step 8 requires "**one**
successor operational-authorization / load-bearing rebinding lifecycle." Accepted authority therefore
already anticipates exactly this sequencing rather than being contradicted by it. §D and §E of
`XASSET-0036` (below) preserve §E unweakened.

**B.5 — The future operational rebinding remains distinct from this implementation authorization.**
§G.B step 8's rebinding is a separate downstream lifecycle against the *merged* bytes of the package
step 7 delivers. Authorizing the package does not authorize the rebinding, and this decision performs
neither.

**Conclusion.** No accepted authority grants the implementation authority §G.B steps 2–7 require. The
gap is real, and this decision closes it narrowly.

### C. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

Stated expressly so no future author reads one permission as the other:

- This decision creates a **pre-execution implementation PR**.
- It **does not consume, replace, amend, or count against** `XASSET-0027` §P.1's exactly-one future
  Stage-1 **evaluation/results** PR.
- §P.1's results PR **remains separately reserved** for the actual 680-construction results, after lawful
  arming and execution, subject to its own §P.1 conditions and its own independent review and principal
  acceptance.
- **No real result artifact may be produced by the implementation PR** — no `stage1_results.yaml`, no
  per-construction disposition, no cell outcome, no roll-up.

After the implementation PR merges, §P.1's PR budget is exactly what it is today: **one, unspent.**

### D. Relation to `XASSET-0029` — this is not an activation PR

- This is **not** an activation PR and **not** an arming step.
- It **generates no attestation**, creates no `READY`, `CLAIMED`, or `COMPLETED` lane state, and creates
  no `AUTHORIZATION_ROOT`.
- `XASSET-0029` §E's no-infinite-regress rule **remains intact and unweakened**. `stage_1_executability.
  executable` stays permanently `false`, and no committed value in this repository authorizes Stage-1
  execution.
- After the authorized implementation package is independently reviewed, principal-accepted, merged, and
  post-merge verified, **and** the required successor operational-rebinding lifecycle (§G.B step 8)
  separately completes, **the final activation remains the external one-shot runtime attestation and the
  operator's act — not another merged activation PR.**

This decision therefore adds one *implementation* authorization to the sequence and adds **zero**
activation authorizations. The regress `XASSET-0029` §E forecloses is not reopened.

### E. Authority granted — exactly one coherent implementation PR

The future implementation PR **may**, and only in service of `XASSET-0030` §G.B steps 2–7:

1. **Reconcile** the final accepted `XASSET-0030`–`XASSET-0035` semantics into
   `research/level1_endpoint_evidence/PROTOCOL_V1.md` and
   `research/level1_endpoint_evidence/pre_registration.yaml` (§G.B step 2).
2. **Correct** the `XASSET-0030` §C enforcement-conformance defect — the validator branch that forbids a
   lawfully-derived `BLOCKED_CATEGORICALLY` disposition, now load-bearing for up to 480 of 680
   constructions per `XASSET-0035` §F.8 — **and only such other conformance defects as the final accepted
   semantics mechanically require** (§G.B step 3).
3. **Implement** the deterministic ENDPOINT Stage-1 execution machinery: the runner, the result
   writer/serializer, a dedicated result validator, and supporting deterministic derivation/integration
   code (§G.B step 4).
4. **Implement** the accepted B1, B2 and B3 semantics **without reopening, re-deriving, or re-arguing
   them** — B1's `G12`-scoped lawful-satisfiability register; B2's "consumes iff both frozen named
   comparison endpoints are sleeves" rule, its 480 consuming / 200 non-consuming inventory, and its
   no-relabelling guard; B3's `UNABLE_TO_DETERMINE` mapping for exactly `G3`, `G5`, and `G9` path 1 **when
   undetermined**, with a determined `G9` path-1 failure remaining prerequisite-blocked.
5. **Modify the existing authorization / trust-boundary implementation only as necessary** to bind all
   outcome-producing executable bytes exactly (§G.B step 5).
6. **Extend `LOAD_BEARING_RELPATHS`** to cover those exact outcome-producing paths — **or** use another
   mechanism **only if** the implementation proves it is the exact authorized equivalent and preserves the
   `XASSET-0030` trust-boundary invariant. **The existing exact-byte load-bearing mechanism is preferred**
   unless a concrete technical reason requires otherwise, and any departure must be argued in the
   implementation PR rather than assumed.
7. **Recompute** successor canonical and code pins and identities **only after** all relevant canonical,
   enforcement, and outcome-producing bytes have stabilized (§G.B step 6).
8. **Add** the focused and adversarial tests, and the factual `operations/WORKSTREAMS.yaml` and decision-
   catalog synchronization, required to validate that package.
9. **Open one draft implementation PR** for independent FULL exact-head review (§G.B step 7).

**The governing invariant is restated unchanged**, and the implementation must satisfy it: *no
outcome-producing executable code may be created, changed, or left outside the bound execution identity
after the final rebinding and before `ATTEMPT_1`.*

### F. Authority withheld — absolute

The authorization in §E **does not extend to**, and the implementation PR **must not** perform:

- generating any real external attestation;
- creating `READY`, `CLAIMED`, or `COMPLETED` lane state, or an `AUTHORIZATION_ROOT`;
- claiming or consuming any part of `ATTEMPT_1`;
- executing any construction, or evaluating any gate for any construction;
- producing a real `stage1_results.yaml` or any real per-construction disposition, cell outcome, or
  roll-up;
- acquiring market, fundamental, economic, or Stage-2 data;
- any Stage 2 work;
- creating any endpoint, bound, point, range, percentage, weight, rank, target, or allocation;
- any Level-2 change;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- reading, listing, opening, or substantively reusing any `risk_lane_boundary` protected `RISK` result;
- resolving `XASSET-0024` §K.1;
- amending `XASSET-0020` §E.1;
- reopening, re-deriving, or re-arguing B1, B2, or B3;
- changing the frozen construction identities, universe, cardinality, or universe hash, unless separately
  authorized;
- performing §G.B steps 8–11.

#### F.1 — The line between structural validation and execution

**Corrected after FULL review `4952475219` MAJOR 1.** The prior head stated a single categorical rule: the
runner could be validated only against synthetic or isolated inputs and could "not run over the real
680-construction universe." That conflated two different operations, and the stricter reading was the
wrong one — it would have made the runner's single most important integrity property unprovable at its
real boundary, and pushed a future author toward either under-testing or inferring an unauthorized
exception.

**Accessing and traversing the frozen construction identities is not execution. Applying gate-evaluation
semantics to those identities to derive Stage-1 outcomes is execution.** The universe is *already frozen*;
reading it changes nothing and produces no outcome. That distinction, not the synthetic/real distinction,
is what protects the one-shot lane.

This is how the program has always in fact behaved: `XASSET-0035` mechanically recomputed the B2
480/200 inventory directly from the merged frozen universe, and this decision's own preflight regenerated
the 680 / 48 / universe hash. Neither consumed `ATTEMPT_1`, because neither evaluated a gate.

**F.1(a) — Authorized: read-only, non-outcome-producing structural validation.** The implementation PR
**may** read and structurally traverse the real frozen construction universe — including through the
actual production traversal seam rather than a synthetic lookalike — to prove properties such as:

- the production traversal consumes exactly all **680** registered construction identities;
- exact canonical ordering;
- zero duplicate, missing, or extra construction;
- immutability of identity fields, and that nothing is relabelled;
- the **680 / 48 / `73c0965e…5224`** universe verification;
- B2's structural **480 consuming / 200 non-consuming** classification, recomputed from frozen identities;
- that the production wiring reaches the frozen universe directly, not a competing hand-built traversal.

This permission is **conditional on the operation remaining read-only and non-outcome-producing**, and it
never extends past that condition.

**F.1(b) — Prohibited: outcome-producing execution.** No such validation, and nothing else in the
implementation PR, may: evaluate or decide any gate (`G1`–`G12`) for a real registered construction;
derive a candidate disposition; derive a cell or roll-up outcome; serialize, persist, or publish a real
Stage-1 result; create `stage1_results.yaml`; create or modify `AUTHORIZATION_ROOT`; create an attestation;
claim `ATTEMPT_1`; write lane state or a ledger entry; acquire market, fundamental, or economic data; or
access protected `RISK` results.

**An actual Stage-1 run over the real 680 — any operation applying gate-evaluation semantics to real
registered constructions and deriving governed Stage-1 outcomes — remains absolutely prohibited** until
the lane is lawfully armed and claimed. It stays downstream of operational rebinding → attestation →
`READY` → lawful claim → execution, exactly as §G.B steps 8–11 require. `ATTEMPT_1` is non-rerunnable, and
this correction does not weaken that protection by one step: it narrows an over-broad ban to the precise
act that would actually consume the lane.

Building and validating against **synthetic or isolated inputs** — the method `XASSET-0030` §B and
`XASSET-0035` both used — remains fully available and is the right tool for gate-semantics testing, where
real identities are neither needed nor permitted.

### G. Packaging — one authorization, one coherent implementation PR

`XASSET-0030` §G.B is expressly "**one coherent pass**," and its own Rationale explains why: an
intermediate reauthorization state that a later change supersedes is paid for twice. The implementation
must therefore proceed as **one** PR executing steps 2–7 coherently where technically safe:

> canonical reconciliation → enforcement correction → runner / result-production implementation →
> trust-boundary extension → final identities and pins → validation and review package

**Not** a separate authorization or a separate PR per component. If the implementing session finds a
concrete technical reason the package cannot lawfully be delivered as one PR, it must **stop and disclose
that finding** rather than silently splitting the package or silently widening its own scope.

Operational rebinding, attestation, arm, claim, and execution remain downstream and outside the
implementation PR.

### H. Effectivity — the §G.B implementation PR may not begin before this lifecycle closes

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own CI run,
   and not a run against any other commit;
7. final post-CI verification and lifecycle closure, including merged-successor identity verification.

**None is individually sufficient.** Opening this PR does not authorize §G.B; a green PR-head CI run does
not; principal acceptance does not; merge does not; and post-merge verification without a successful exact
merge-commit CI run does not. **Only complete closure of all seven does.**

This mirrors `XASSET-0035` §I and, through it, the repository's own committed definition —
`level1_stage1_execution_authorization.REQUIRED_LIFECYCLE_GATES`, a six-element tuple that is itself one
of the six load-bearing paths. **That module is cited only and remains byte-unchanged.**

`XASSET-0035`'s own lifecycle omission — an enumeration that named four of six gates — is not repeated:
conditions 5–7 above are that tuple's last three members, and condition 2 is the exact-head discipline
`OPS-0009` §6 applies to condition 1.

### I. Work deliberately not created

| Candidate requirement | Why not created |
|---|---|
| A further semantic prerequisite | `XASSET-0035` §I closed §G.A; adding one would re-open a resolved partition |
| A separate authorization per §G.B component | §G explains why one coherent pass is required |
| Any redesign of §G.B | `XASSET-0030` §G.B is adopted unchanged and is not re-sequenced |
| Re-analysis of B1 / B2 / B3 | Resolved by `XASSET-0035` §§E–G; §E.4 requires implementing, not revisiting |
| Authorizing §G.B step 8's rebinding | A separate downstream lifecycle (§B.5) |
| Correcting the §C defect here | A load-bearing implementation path; §G.B step 3's work |
| Amending `XASSET-0029` | Unnecessary — §B.4 shows no conflict; §D preserves it unweakened |
| Pre-specifying the runner's design | Beyond what defining authorized scope requires |

### J. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; creates no `AUTHORIZATION_ROOT`; arms and executes no Stage 1; creates no Stage-1 runner,
result writer, serializer, result validator, or `stage1_results.yaml`; consumes nothing of `ATTEMPT_1`;
**evaluates no gate for any construction and asserts no per-construction outcome**; closes no gate on
satisfaction and changes no gate's class, index, question, controlling authority, or failure disposition;
corrects no validator, extends no `LOAD_BEARING_RELPATHS`, and performs no load-bearing reauthorization
or rebinding; **amends no canonical file and changes no hash pin, universe, cardinality,
`comparison_subject_kind`, `unordered_pair_id`, or construction identity**; performs no part of §G.B and
enters none of it; consumes no part of `XASSET-0027` §P.1's reserved results PR; acquires no market,
fundamental, economic, or Stage-2 data; resolves `XASSET-0024` §K.1 neither way and leaves `XASSET-0020`
§E.1 unamended; reopens neither B1, B2, nor B3, and leaves `XASSET-0031`'s `G3` untouched; grants no
Stage 2 and no application authority; creates no representation aggregation or selection rule and
designates no CM-14–CM-17 membership; selects no sleeve and creates no endpoint, bound, point, range,
percentage, weight, rank, target, or allocation; weakens no validator or test; **reads, lists, opens, or
references no `risk_lane_boundary` protected result path** and reuses no `RISK` scenario, value,
parameter, window, or result; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no chart, ladder,
deployment, trade, order, or brokerage action; and rewrites no accepted history.

**Stage 1 remains UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, and unconsumed.**

## Rationale

Six consecutive filings — `XASSET-0030` through `XASSET-0035` — each named `XASSET-0030` §G.B and each
expressly declined to authorize it. That consistency is the point: the sequence deliberately separated
*describing* the work from *permitting* it, so that no session could drift into the canonical, enforcement,
and outcome-producing-code phase on momentum. `XASSET-0035` then closed the last semantic blocker and
stated the consequence precisely — §G.B is unlocked "on complete lifecycle closure" — while still
authorizing none of it.

The result is a program that is semantically ready and procedurally forbidden. That is a correct place to
stop, and exactly the place a governance filing must resolve rather than a future implementer.

**Why an express grant rather than an inference.** The two nearest candidate authorities each fail on
their own terms, not on a technicality. `XASSET-0027` §P.1's single results PR is barred from making any
production configuration change, and §G.B steps 2, 3 and 5 are nothing but production configuration
changes; repurposing it would also spend the one results-PR budget on a package that produces no results.
`XASSET-0029` §E terminates the activation regress on a step that "changes no repository state" — which
the runtime attestation is and §G.B is not. Reading either as covering §G.B would weaken a real safeguard
in order to save one filing.

**Why the grant is bounded to steps 2–7.** `XASSET-0030` §G.B's own correction history shows what goes
wrong otherwise: an earlier head sequenced runner implementation before the rebinding without requiring
the rebinding to cover the runner's bytes, leaving the code that produces all 680 outcomes outside the
bound execution identity against a non-rerunnable `ATTEMPT_1`. Steps 8–11 are the mechanism that closes
that hole. Authorizing them here — before the bytes they must bind even exist — would repeat the same
error one layer out.

**Why one coherent PR.** `XASSET-0030` §G's ordering argument applies unchanged: the canonical artifacts
and the validators are bound together, so an early partial reauthorization is invalidated by design. The
same reasoning that put the enforcement correction *after* the semantic questions puts the whole package
in one pass.

**Why this filing is small.** It adds no analysis, no design, and no prerequisite. `XASSET-0034` §E.4's
discipline — remove successor work rather than add it — is applied by keeping the grant to a scope
statement and a boundary, so the implementing session's first act is implementation rather than another
round of interpretation.

## Alternatives Considered

**Let the implementing session infer authority from `XASSET-0035`'s "§G.B is unlocked."** Rejected. Six
accepted decisions say the opposite in operative text. "Unlocked" describes a satisfied precondition, not
a permission, and a program that has refused inference-by-adjacency at every prior step cannot rely on it
at the step with the largest blast radius.

**Repurpose `XASSET-0027` §P.1's results PR.** Rejected on three independent grounds (§B.3), any one
sufficient. It would additionally consume the reserved results-PR budget for a package that produces no
results, leaving the actual 680-construction evaluation with no authorized vehicle.

**Amend `XASSET-0029` to cover implementation.** Rejected. There is no conflict to resolve — §E's own
terminating condition already excludes state-changing work — so an amendment would edit an accepted
decision to fix a problem it does not have, and would risk weakening the activation-regress bar.

**Authorize all of §G.B steps 2–11 in one grant.** Rejected. Step 8's rebinding must run against
*merged, reviewed* bytes that do not yet exist; authorizing it now would license binding a package before
its identity is fixed, which is the exact failure mode `XASSET-0030` §G.B's own DELTA correction removed.

**Authorize each §G.B component separately.** Rejected by `XASSET-0030` §G's ordering argument: partial
reauthorization states are invalidated by later canonical or enforcement changes and are paid for twice.

**File nothing and let a future session decide.** Rejected. The gap is discovered, reproducible, and
directly on the critical path; leaving it means the next session either stalls or infers. Recording the
finding without resolving it would move the same decision one filing later at no benefit.

## Consequences

**Effective only on complete closure of the seven §H conditions.** Until then the §G.B implementation PR
is **not** authorized to begin, and this decision changes nothing.

Once effective, exactly one `XASSET-0030` §G.B implementation PR may proceed, covering steps 2–7 as one
coherent pass, and carrying its own full lifecycle — independent FULL exact-head review, any bounded
correction and re-review, principal exact-head acceptance, merge, post-merge verification, and merge-commit
CI at the exact merge SHA.

**What remains after that PR merges, unchanged by this decision:** §G.B step 8's successor
operational-authorization / load-bearing rebinding lifecycle; step 9's read-only post-rebinding readiness
verification; step 10's fail-closed drift handling; and step 11's external one-shot attestation, arm,
claim, and 680-construction run. `XASSET-0027` §P.1's evaluation/results PR remains reserved and unspent.

**Explicitly unchanged by this filing:** both canonical pins; the frozen 680 / 48 universe and its hash;
all six `LOAD_BEARING_RELPATHS` and their bytes; `level1_stage1_execution_authorization.py` and both
ENDPOINT validators; `XASSET-0030`'s 6/6 gate map and its §E.1 triggers; `XASSET-0024` §K.1;
`XASSET-0020` §E.1; `XASSET-0031`'s `G3`; `XASSET-0035`'s B1/B2/B3; every `intelligence/` record;
`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`,
`margin_state.py`, `levels.py`; and every accepted decision's status and text.

**Stage 1 remains UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, and unconsumed. No
construction was evaluated, no gate result asserted, and no outcome produced.**
