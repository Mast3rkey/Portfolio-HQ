---
decision_id: XASSET-0028
date: 2026-08-16
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, LEVEL2-0001, RISK-0001]
supporting_artifact: research/level1_construction_universe/CLOSURE_DETERMINATION_V1.yaml
---

## Context

### Live preflight

Verified independently before any file was touched, against live GitHub and the local checkout rather
than against the authorizing brief: `main` and `origin/main` both at
`e4b6f0b810884fcb73d1b8ee053d8005db532f3e`; working tree clean; no stash; a single worktree; **zero**
open pull requests. `XASSET-0027` merged via PR #326 — accepted head
`6d6a5190a682fa4eb30d4abee70a836c24194fe1`, base `e7e9e53dbcdcaaa0ff71f128694028650500c323`, merge
commit parents re-derived from `git log` and matching exactly; final independent review `4945377387`
(APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0 BLOCKING / 0 MAJOR / 0 MINOR / 1 NOTE); principal
acceptance `issuecomment-5305685656`; merge-commit CI run `31926322438` / job `95114383877`, event
`push`, branch `main`, `head_sha` `e4b6f0b8…`, completed / success. `XASSET-0028` was unused in both
repository content and PR search. Both canonical `ENDPOINT-0001` hashes were recomputed from observed
bytes and match their accepted pins. No `stage1_results.yaml` and no `intelligence/level1_application/`
exist.

### The question this unit answers

`XASSET-0027` §P.0, verbatim: **one governance unit whose scope is to determine whether a concrete
construction universe can be closed at all and, if so, to freeze it**
(`CONCRETE_CONSTRUCTION_UNIVERSE_PREREGISTRATION`) — confronting directly that constructions built on
sources which do not yet exist are not enumerated by any accepted decision, and stating its own
answer, **including that its answer may itself be negative**.

`XASSET-0027` deliberately did not pre-decide it. Its own final correction, under independent review,
replaced a permanent-impossibility claim with a present-authority claim and renamed its route keys to
`routes_considered_and_unavailable_to_this_filing`, expressly leaving open whether this unit could
preregister a finite hypothetical-architecture registry. This filing therefore begins with the
question genuinely open in both directions, and neither route was presumed unavailable.

### The gap, reproduced rather than inherited

Four classifying dimensions are closed by accepted authority — 4 sleeves, 2 bounds, 6 DRIVER classes,
5 `(route, NUM-0001 class)` provenance families — yielding 240 family slots over 48 cells. That grid
is **exhaustive over provenance families and not over constructions**. `XASSET-0023` §H.2 and §H.3 are
**constraint sets, not generators**: satisfying a constraint set does not enumerate the objects that
satisfy it. The existing-source corpus is exactly `XASSET-0021`'s frozen snapshot, which
`XASSET-0025` Outcome C already searched exhaustively. What remains is constructions whose sources do
not yet exist.

## Decision

### A. Determination

**`CONSTRUCTION_UNIVERSE_NOT_CLOSED`.** Under the authority available to `XASSET-0028`, a concrete
construction universe for `ENDPOINT-0001` Stage 1 **cannot be closed**. Two independent prerequisites
block it, and neither can be supplied here without performing a methodology amendment reserved to
separate authority. Stage 1 remains **NOT EXECUTABLE**.

The determination is recorded machine-readably at
`research/level1_construction_universe/CLOSURE_DETERMINATION_V1.yaml` and enforced by
`level1_construction_universe_closure_validator.py`.

**The negative is bounded to present authority and is expressly not a claim of permanent
impossibility.** That distinction is not decorative: it is the exact overclaim `XASSET-0027`'s own
independent review caught, and this filing's validator inherits its banned-phrase discipline and
applies it to this decision's own artifact.

### B. The closure test applied

A universe closes only if all five hold. Criteria 2, 4, and 5 were achievable. **Criterion 3 is
decisive** — it is what makes a negative Stage-1 result mean anything, because `XASSET-0027` §I.2
permits `BLOCKED_CATEGORICALLY` only where *every registered construction* for a cell was evaluated
and every one was blocked.

| | Criterion | Satisfiable here |
|---|---|---|
| C1 | Finite, with an exact stated cardinality | **No** |
| C2 | Frozen before any Stage-1 outcome is observed | Yes |
| C3 | **Exhaustive over constructions** — a negative means every construction was tested | **No — decisive** |
| C4 | No executor may invent, omit, substitute, or mutate a construction at result time | Yes |
| C5 | Each construction reproducible from frozen identity | Yes |

### C. Route A — a concrete finite registry

The construction space partitions in two, and the halves fail for **different** reasons. Collapsing
them would have hidden that.

**Existing-source partition — closes, and adds nothing.** Finite, frozen, exactly `XASSET-0021`'s
snapshot. But `XASSET-0025` Outcome C already searched precisely that corpus and found no qualifying
source, and `XASSET-0027` §I.1.1 records as an accepted determination that a Stage 1 restricted to it
would re-run that result. Closing only this half would additionally leave every hypothetical
construction unregistered, so §I.2's negative rule would range over a set that excludes the live
possibility by construction.

**Hypothetical-source partition — does not close**, blocked independently by both §E prerequisites.

### D. Why cleverer specification does not rescue it

This is the reason `PREREQ-2` is a genuine prerequisite and not an implementation inconvenience.

- **Under-specify** — a construction stating less than what determines its own gate outcomes leaves
  the remainder to the executor at evaluation time. That violates C4 and merely *relocates* the
  unbounded qualitative search from results time to freeze time.
- **Over-specify** — a construction stating exactly what determines its gate outcomes fixes its own
  disposition analytically at freeze. Stage 1 becomes vacuous, and the question that matters — whether
  the world admits such a source — goes untested.
- **The middle ground is real.** A stated institutional source type paired with a stated content
  requirement is concrete, non-tautological, and genuinely forces `G2`, `G3`, and `G5` to be
  evaluated. This filing does not pretend otherwise. But the set of such pairs is *exactly* the space
  `PREREQ-2` concerns, and accepted authority supplies no principle from which it could be derived.

**This is not a failure of imagination.** More architectures can plainly be imagined. Completeness,
however, requires a closure *principle*, and no accepted decision supplies one for source
architectures. Absent one, further imagination lengthens a list without ever making it demonstrably
exhaustive — and C3 is a claim about exhaustiveness, not about length.

### E. The two blocking prerequisites — independent, and both required

**They are not alternatives.** Satisfying `PREREQ-1` alone does not enable closure, because
`PREREQ-2` blocks every slot. Satisfying `PREREQ-2` alone does not enable closure for the
comparison-scoped slots. This is stated explicitly so a successor cannot satisfy the narrower one and
report the universe closeable.

**`PREREQ-1` — a comparator admissibility rule. Blocks 120 of 240 slots.** Three DRIVER classes —
`valuation_opportunity_cost`, `downside_path_risk`, `recovery` — are comparison-scoped with **no
comparator fixed**. `XASSET-0026` §D states it in terms: *"What the lawful comparator may be for a
given item is a property of an evidence design that does not exist; no comparator rule is supplied,
narrowed, or implied here."* A concrete construction in those cells must fix a comparator. Supplying
one here would furnish precisely the rule `XASSET-0026` declined to supply — a methodology amendment
to `XASSET-0020` §E.1's scope language — and is substantively an **economic judgment**, since choosing
what the marginal dollar is measured against determines what opportunity cost means. That is the
arbitrary economic assumption this unit is barred from smuggling in.

The blast radius is stated precisely rather than blanket-claimed: `portfolio_function` and
`sleeve_deployability` are sleeve-scoped, and `diversification_cobehavior`'s comparator space is
**already closed** by `XASSET-0020` at exactly six unordered pairs derived as `4 choose 2` and
recorded as binding. Only three of six classes lack a comparator. The 120 figure is
**validator-computed from the accepted family-slot generator**, not asserted.

**`PREREQ-2` — an enumeration principle for hypothetical source architectures. Blocks all 240 slots.**
A separately accepted basis by which the admissible set can be **derived rather than authored**.
Without it, "every registered construction" means only "every construction the registry's author
thought of," and the resulting negative would establish the author's imagination rather than
non-constructibility — the overstated-exhaustiveness failure `XASSET-0027` §L exists to prevent.

### F. Route B — a deterministic construction grammar

Also unavailable. A grammar needs primitives and composition rules. The already-closed dimensions
generate exactly the 240 family slots, which accepted authority records as a classification scaffold
and expressly not a construction universe — **a grammar over only those would relabel the five
provenance families and close nothing**, the precise trap this unit was warned against. Generating
constructions additionally needs primitives for the open dimensions, and accepted authority supplies
none: the comparator is expressly not supplied, and source architecture is a two-value
*provenance-type* vocabulary rather than a set of architectural primitives.

For `R2_C2` the bar is stronger and textual. `XASSET-0023` §H.3 item 3: *"An application may not
compose, select among, or invent a derivation the sources do not prescribe; composing one is
authorship, not derivation."* A grammar that composed derivations would be exactly that barred
authorship.

### G. Two further routes, tested rather than dismissed

**Dominance over a maximally permissive construction.** If one maximal construction per slot dominated
every other, exhaustiveness would follow without enumeration. It fails twice: the gates are not
monotone under any single permissiveness ordering — a source stating more may clear `G2` more readily
while becoming more exposed to `G4`'s barred origins — and, decisively, the maximal element is the
construction *defined* as satisfying every gate, so it passes analytically and cannot establish a
categorical block.

**A finite quotient over gate-outcome vectors.** If constructions partitioned into finitely many
gate-outcome classes, one representative each would suffice. But a logically consistent vector is not
evidence that any source could realize it, and realizability is the question Stage 1 exists to ask.
`G2`, `G3`, and `G5` — the gates `XASSET-0027` §K identifies as binding — turn on what a specific
source would actually state, so the quotient is strictly finer than 240 and depends on the same open
dimensions.

### H. Partial closure — achievable, and expressly not shipped

A registry restricted to the existing-source corpus, or to the three classes with closed comparator
spaces, could be frozen and would satisfy C1, C2, C4, and C5. It still fails C3: the unregistered
remainder would be excluded **by construction rather than evaluated**, so under §I.2 those cells could
not be determined negatively at all. Labelling such a registry a closed construction universe would be
the overstated exhaustiveness §L names. **A determination that closure is unavailable is preferable to
a restricted registry presented as closure.**

### I. The path that requires neither prerequisite

`PREREQ-2` exists only because the relevant sources do not yet exist. If a qualifying source comes into
existence and is lawfully admitted through an `XASSET-0021` snapshot successor, the construction built
on it becomes `EXISTING_SOURCE_ARCHITECTURE` carrying exact path and SHA-256 identity — closed by
**observation rather than enumeration**, and `PREREQ-2` does not arise for it.

This is **not** a prediction that such a source will appear, not a schedule, and not authority to seek,
solicit, or commission one. It does not dissolve `PREREQ-1`, which would still bind a
comparison-scoped construction. It is recorded so the blocker is not mistaken for one that only
governance work can remove.

### J. Disclosed finding — recorded, not corrected

`research/level1_endpoint_evidence/pre_registration.yaml` lines 895–896
(`consequential_parameter_registry.zero_parameter_declaration.design_consequence`) assert that the
candidate universe is closed by a deterministic generator and that the executor selects neither which
constructions to try nor when to stop. That **contradicts the same file** at lines 286–287
(`status: NOT_CLOSED`, `stage_1_executable: false`) and contradicts `XASSET-0027` §I.1.1 and §L. It
appears to be wording that survived `XASSET-0027`'s corrections at a site those corrections did not
reach. The claim does not appear in `PROTOCOL_V1.md`, so the inconsistency is **single-site**.

**Not corrected here.** The file is hash-pinned by `XASSET-0027`; editing it would invalidate an
accepted pin and requires an amendment decision that expressly governs the change. This unit's
authority is to determine closure, not to amend `XASSET-0027`'s canonical files.

**Not an enforcement gap.** The existing preregistration validator independently enforces
`NOT_CLOSED` and `stage_1_executable: false`, and `validate_stage1_results()` fails closed on an empty
closed construction universe, so no execution path is opened. This filing's own validator additionally
rejects any claim of closure over the construction universe or the qualitative search surface, so a
reader acting on the stale sentence is blocked **mechanically**, not merely textually.

### K. Packaging — why no canonical file changed

The determination is **consistent with the accepted canonical bytes**. `pre_registration.yaml` already
records `construction_universe_closure.status: NOT_CLOSED` and `stage_1_executable: false`, and the
existing validator requires `status` to be exactly `NOT_CLOSED`. A negative therefore requires **no
amendment and no re-pinning**; both pins remain valid and are verified from observed bytes by this
unit's validator and tests. A positive determination would have required amending those files and
governing the re-pin explicitly — an asymmetry recorded so a successor does not read this filing as
establishing that closure work never touches canonical bytes.

The determination artifact is sited at `research/level1_construction_universe/` rather than beside the
canonical files, specifically so that `XASSET-0027`'s existing invariant test — that
`research/level1_endpoint_evidence/` contains exactly its two canonical files — **remains true and
unweakened**. No existing test was relaxed.

### L. Adversarial review

Each failure class was tested against the artifact and validator rather than assumed absent: duplicate
or colliding identity; executor-authored free text changing a construction; omitted, duplicated,
extra, or reordered constructions; substituted source path; correct-looking but wrong hash; changed
comparator; route/class and DRIVER-class mismatch; silently solved representation dependency;
historical-anchor contamination; equal-split, residual, and midpoint leakage; result-aware expansion;
hidden consequential parameter; family mistaken for a concrete construction; positive closure claimed
without finite exhaustiveness; **negative closure resting only on lack of imagination**; implicit
§K.1 resolution; premature §J.12 reconciliation; and RISK substantive reuse.

Two controls deserve naming. The **120-slot figure is computed from the accepted generator**, so
PREREQ-1's blast radius cannot drift from the real grid. And the **quotation exemption is narrow**:
disclosing defective text requires reproducing it, so exactly one field path
(`disclosed_findings[N].observed_text`) is exempt from the closure-claim scan — never from the
permanence, percentage, or barred-numeral scans, and never anywhere else. Tests prove both directions.

### M. Preserved, unresolved, and untouched

`XASSET-0024` §K.1 remains **unresolved**, neither resolved nor relied upon; no construction assumes
the subject-matter reading. §J.12 remains **`NOT_YET_DETERMINABLE_DEFERRED`** — no whole-portfolio
reconciliation was inserted to make anything look complete. Representation stays
`SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`; no aggregation or selection rule is supplied and no
CM-14–CM-17 membership is designated. The family-slot grid remains a classification scaffold and not a
trial ceiling. `RISK-0001` Attempt 2 is untouched: no retry, no Attempt 3, no family re-question, no
scenario, threshold, window, representation-value, or parameter-pattern reuse, and
`/private/tmp/phq-risk0001-results` was never accessed, listed, or read.

### N. Zero consequential numeric parameters

This determination introduces none as `NUM-0001` §18 defines the term — no threshold, tolerance,
cutoff, materiality level, window, weight, coefficient, or score. Every count (240, 120, 48, 6, 5, 4,
3, 2) is a cardinality **derived** from an already-closed population by multiplication or counting,
not a value selected here; changing one would be an arithmetic error rather than a re-tuning. No count
was chosen by searching historical outcomes. The validator asserts the parameter registry is empty.

### O. What comes next

1. Independent **full exact-head review** of this PR. Nothing below may begin before this decision's
   own complete lifecycle closes.
2. Neither prerequisite is authorized, scoped, or scheduled here. Each requires its own separately
   accepted governance decision, and `PREREQ-1` is a methodology amendment touching `XASSET-0020`
   §E.1's scope language.
3. Stage 1 remains **NOT EXECUTABLE**. `XASSET-0027` §P.1's two preconditions are unchanged, and this
   filing satisfies neither — it determines that the second cannot presently be satisfied at all.
4. Every successor `XASSET-0027` §P.2 named remains unauthorized and separately required.

### P. Reopen triggers

Reopen `XASSET-0028` if: a comparator admissibility rule is accepted; any principle from which
hypothetical source architectures could be derived is accepted; a qualifying endpoint-stating source
comes into existence and a lawful `XASSET-0021` snapshot successor admits it; either pinned canonical
hash changes or the canonical files are lawfully amended; `XASSET-0020` §E.1's driver classes or
`XASSET-0023` §H's routes are amended; `NUM-0001`'s classes change; `XASSET-0024` §K.1's reading is
established either way; or the disclosed §J stale-text finding is corrected by an amendment decision.

Independently: `XASSET-0027` §Q is triggered by this filing's acceptance, since it reopens on **a §P.0
unit being accepted, whether its answer is that a universe can be closed or that it cannot**.

### Q. Absolute non-authorization

This decision **closes no construction universe**, freezes and registers no construction, and supplies
no comparator rule or enumeration principle; makes Stage 1 no more executable than it already was;
authorizes no Stage 2, no empirical work, no data acquisition, no backtest, no trial, and no candidate
evaluation; produces no endpoint, bound, point, range, percentage, weight, target, or allocation, and
selects, prefers, ranks, sequences, or budgets no sleeve; **exercises no endpoint authority**; grants
no evidence-admission or application authority and creates no application artifact; amends, extends,
or re-pins no canonical file and edits no accepted decision; resolves `XASSET-0024` §K.1 neither way
and decides §J.12 neither way; supplies no representation rule and designates no CM-14 through CM-17;
performs no Level-1 sizing and no Level-2 membership or sizing; makes no liquidity determination;
changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier,
cluster, cap, or margin state; authorizes no chart, ladder, optimizer, deployment, trade, order, or
brokerage action; adopts no portfolio policy; grants no RISK reuse authority and accesses no RISK
execution artifact; and rewrites no accepted history.

## Rationale

`XASSET-0027` left §P.0 genuinely open after its own review corrected an overclaim in the opposite
direction. The honest way to answer it was to attempt closure seriously and report what actually
blocked it — not to inherit a conclusion. Four routes were built out far enough to fail on their
merits, including two the authorizing brief did not name.

The decisive finding is that **exhaustiveness, not finiteness, is the binding constraint**. A finite
registry is easy to write; a registry whose negative *means something* is not. `XASSET-0027` §I.2 ties
`BLOCKED_CATEGORICALLY` to "every registered construction," so a registry assembled from imagined
architectures would convert an unbounded qualitative search into a bounded-looking one without
removing the arbitrariness — it would relocate the defect from results time to freeze time and make it
harder to see. Recording that is more useful than shipping it.

Naming **two independent** prerequisites, rather than one aggregate blocker, is what makes the
negative actionable. `PREREQ-1` is narrow, textual, and directly citable to `XASSET-0026` §D, which
declines to supply the rule in terms. `PREREQ-2` is deeper and applies everywhere. A successor that
solved only the citable one and declared the universe closeable would be wrong, and the decision says
so before that can happen.

The §I dissolution path matters for the same reason the §A permanence bound does: this negative
describes present authority and a present state of the world, and the most likely way it is removed is
not a governance act at all.

## Alternatives Considered

**Ship a restricted registry and call it closure.** Rejected — §H. It would satisfy four of five
criteria and fail the one that matters, and its negative would be unusable for the cells it silently
excluded.

**Fix the comparator myself and close 120 slots.** Rejected — §E. `XASSET-0026` §D expressly declines
to supply, narrow, or imply a comparator rule; supplying one is a methodology amendment and an
economic judgment about what opportunity cost is measured against.

**Restrict comparators to the four sleeves.** Rejected as a narrowing masquerading as a closure.
`XASSET-0026` §D records that `XASSET-0020` §H compares each sleeve with
`UNSIZED_UNASSIGNED_CAPITAL`, "a direct alternative that is not a sleeve," so a sleeve-only comparator
set would exclude constructions accepted authority permits — and a negative over it would be false.

**Declare the hypothetical space empty and close the universe on the existing corpus.** Rejected — it
asserts that no future source could qualify, precisely the permanent-impossibility overclaim
`XASSET-0027`'s review removed, and §Q preserves the openness.

**Correct the §J stale sentence while here.** Rejected — it is hash-pinned by `XASSET-0027`. Disclosed
instead, with a mechanical block against acting on it.

**Amend `pre_registration.yaml` to carry the determination.** Rejected — it would break an accepted
pin for no benefit, since the canonical file already records `NOT_CLOSED`. A separate artifact
verifying the pins is smaller and safer (§K).

**Build a Stage-1 runner interface.** Rejected — the brief permits it only if strictly necessary and
prefers it not be built, and with the universe unclosed there is nothing for a runner to range over.

## Consequences

Stage 1 remains **NOT EXECUTABLE**, now for a determined reason rather than an open one, with two
named prerequisites and one non-governance dissolution path. `ENDPOINT-0001`'s canonical files are
byte-unchanged and their pins remain valid. `XASSET-0027` §Q is triggered by acceptance. The stale
sentence at `pre_registration.yaml:895-896` stands uncorrected and disclosed, mechanically blocked
from being acted on, and available to a future amendment decision. `LEVEL1_ENDPOINT_AUTHORITY` remains
constituted and unexercised; Stage 2 remains unauthorized; application authority remains **WITHHELD**.
