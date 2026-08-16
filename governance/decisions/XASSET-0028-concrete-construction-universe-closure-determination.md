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
than against any brief: `origin/main` at `e4b6f0b810884fcb73d1b8ee053d8005db532f3e`; working tree
clean; no stash; a single worktree; PR #327 the sole open pull request, at head
`6fc32e184e77f2bc7371f8f73d2818b5a3f4eeb6`, base `e4b6f0b8…`, open / draft / unmerged / mergeable.
Both canonical `ENDPOINT-0001` hashes were recomputed from observed bytes and matched their accepted
`XASSET-0027` pins before amendment. No `stage1_results.yaml` and no `intelligence/level1_application/`
exist.

### The question this unit answers

`XASSET-0027` §P.0, verbatim: **one governance unit whose scope is to determine whether a concrete
construction universe can be closed at all and, if so, to freeze it** — *"including the possibility
that its own answer is negative."*

### The correction this filing makes

A first attempt at this unit answered §P.0 in the **negative**. Independent full exact-head review
`4945473310` returned **CHANGES REQUIRED — 1 BLOCKING / 2 MAJOR / 2 MINOR / 1 NOTE**, finding that the
negative rested on a **stronger closure standard than `XASSET-0027` established**: it required the
registry to contain *every conceivable future source architecture*, when `XASSET-0027` §I.2 ties a
categorical cell negative to **every *registered* construction for that cell**. The review also found
that the filing had discarded the positive research-design authority this unit exists to exercise, and
that `PREREQ-1` had converted `XASSET-0026`'s deliberate evidence-design openness into a requirement
for a separate global comparator ontology without an accepted-text bridge.

**That finding is correct.** The determination has been re-derived from primary authority, and it
**flips**. The negative is not preserved merely because a validator and test suite encoded it.

## Decision

### A. Determination — `CONSTRUCTION_UNIVERSE_CLOSED`

The concrete `ENDPOINT-0001` Stage-1 construction universe **is closed**: a deterministic, finite,
preregistered, grammar-derived universe of **680 registered constructions** across the 48 cells, with
exact identity, binding ordering, derived cardinality, and an aggregate integrity hash.

**Stage 1 is NOT EXECUTED by this filing and remains NOT EXECUTABLE.**

### B. The closure standard actually in force

A finite preregistered study universe is normatively closed by this explicitly authorized governance
act when it is finite, exact-cardinality, completely generated under a **stated governed closure
basis**, frozen before Stage-1 outcomes, deterministic in identity and ordering, byte-identically
reproducible, non-outcome-aware, non-economic in its enumeration mechanism, free of endpoint values
and portfolio-policy choices, complete under its explicit governed study basis, and incapable of
executor additions, omissions, substitutions, or hypothesis mutation.

It is **not** required to exhaust the metaphysical set of every imaginable future source. Governance
preregistration necessarily authors hypotheses; the integrity test is completeness **under a stated
basis**, not omniscience.

### C. The closure basis, derived rather than invented

`XASSET-0027` §I.1 names the dimensions that can inhabit one provenance family. Taken in turn:

| Dimension | Disposition |
|---|---|
| external impositions, calibrations, governance selections, provisional guardrails, prescribed derivations | **already closed** — these *are* the five `(route, NUM-0001 class)` families |
| evidence form | **representation** — preserved as a downstream gate (`G9`), never an identity dimension |
| source identity | never enumerated — no institution, vendor, or document is named anywhere |
| **source architecture** | **frozen into identity** — see §F |
| **comparator architecture** | the one genuinely open dimension — **and accepted authority already closes it** |

`XASSET-0020` §H closes the direct-comparison contract in two parts: exactly **six unordered
sleeve-sleeve pair records** ("`4 choose 2`", binding), and — separately — *"Each of the four sleeves
must **also** be compared directly with `UNSIZED_UNASSIGNED_CAPITAL`."*

The pre-registration's own canonical `driver_class_scope` block already partitions the six `XASSET-0020`
§E.1 DRIVER classes by evidence-item scope. **This filing reads that partition out of the accepted
bytes; it does not author one.**

| DRIVER class | Canonical scope | Comparator architectures |
|---|---|---|
| `portfolio_function` | `ONE_SLEEVE` | 1 — `SELF` |
| `sleeve_deployability` | `ONE_SLEEVE` | 1 — `SELF` |
| `diversification_cobehavior` | `ONE_UNORDERED_PAIR` | 3 — the three other sleeves |
| `valuation_opportunity_cost` | `COMPARISON_SCOPED_COMPARATOR_NOT_FIXED` | 4 — three other sleeves + UAC |
| `downside_path_risk` | `COMPARISON_SCOPED_COMPARATOR_NOT_FIXED` | 4 |
| `recovery` | `COMPARISON_SCOPED_COMPARATOR_NOT_FIXED` | 4 |

**`4 × 2 × 5 × (1 + 4 + 4 + 4 + 3 + 1) = 4 × 2 × 5 × 17 = 680`**

`UNSIZED_UNASSIGNED_CAPITAL` is deliberately **not** a `diversification_cobehavior` comparator: §H's
UAC comparison is not a pair record and carries its own separate conclusion vocabulary, and that
class's canonical scope is `ONE_UNORDERED_PAIR`. Registering it would be *inventing* a construction
rather than enumerating one. The alternative — registering 40 `NOT_APPLICABLE` rows for grid symmetry,
giving 720 — was considered and declined for exactly that reason, and is recorded so the judgment is
checkable rather than silent.

**This answers MAJOR 1.** No comparator rule is supplied. `XASSET-0026` §D said no comparator rule was
supplied *by `XASSET-0026`*; it did not repeal `XASSET-0020` §H's comparison contract, and its own
scope note says comparators "are not fixed **here**." Enumerating §H's mandated comparisons is study
enumeration, not an economic judgment, and no comparator ordering implies sleeve preference.

### D. Construction identity — smallest sufficient

Each construction carries: `construction_id`, `cell_id`, `sleeve`, `bound`, `driver_class`,
`driver_class_scope`, `family_id`, `route`, `num_0001_class`, `comparison_subject_kind`,
`comparator_architecture`, `counterpart`, `unordered_pair_id` (pair-scoped only),
**`source_architecture`**, **`hypothetical_source_requirements`**, `evidence_proposition`,
`representation_posture`, `governing_authority_refs`, and `ordinal`.

Every descriptive field is **generated deterministically from closed identity**. No result-author free
text exists, so two independent executors handed the same `construction_id` necessarily evaluate the
same hypothesis.

**Deliberately excluded from per-construction identity**: admitted/prohibited input classes and the
twelve applicable gate ids. Both are **constant across all 680** and therefore discriminate no
hypothesis; duplicating them into each record would be noise, not identity. They are recorded once, at
universe level, in the determination artifact.

### E. `R2_C2` — a source requirement, never a composed derivation

`XASSET-0023` §H.3 item 3 bars **an application** from composing a derivation the sources do not
prescribe — *"composing one is authorship, not derivation."* It does not bar preregistering the
hypothesis that a **qualifying source must itself prescribe one**. Every `R2_C2` construction therefore
carries exactly that requirement and composes nothing. The generator produces no arithmetic.

### F. Source architecture — frozen into construction identity

**Corrected under review `4946087943` BLOCKING 1.** An earlier head left source architecture open
(`SPANS_…`), silently contradicting the canonical contract. The contradiction is decisive:
`frozen_provenance_requirements` is addressed **by name** to
`THE_FUTURE_CONSTRUCTION_UNIVERSE_CLOSURE_UNIT` — this unit — and is `binding_on_any_future_stage_1`.
It is an instruction to me, not an obstacle. Leaving architecture open left the hypothesis-defining
provenance unfrozen after freeze: exactly the result-time discretion those rules exist to prevent.

**Every registered construction freezes `source_architecture: HYPOTHETICAL_SOURCE_ARCHITECTURE`** plus
deterministically generated `hypothetical_source_requirements`. `source_path` and `source_sha256` are
absent, as `source_architecture_vocabulary.hypothetical_forbids` requires.

**The existing-source half is resolved, not omitted.** `XASSET-0027` §I.1.1, verbatim: the
existing-source corpus "is exactly `XASSET-0021`'s frozen snapshot, and `XASSET-0025` Outcome C already
searched precisely that corpus exhaustively and found no qualifying source; a Stage 1 restricted to it
would re-run an accepted determination and add nothing. **The remaining space is constructions whose
sources do not yet exist.**" Registering existing-source rows would re-litigate an accepted
determination. The source-architecture dimension therefore resolves to exactly **one** lawful value
rather than two — which is why the cardinality is *unchanged by* that resolution rather than *preserved
through* it. The disposition is recorded explicitly, never silently dropped.

**No source-identity search is reintroduced.** The frozen specification is a closed conjunction of
already-accepted conditions (admissibility, single-sleeve bound, subject matter, provenance family,
intrinsicality, the route's own §H.2/§H.3 conditions, the NUM-0001 field set, representation deferred
to `G9`, no barred non-route). It names no institution, vendor, jurisdiction, or document. Stage 1
evaluates whether a **frozen specification** is lawfully satisfiable under the twelve gates — it does
not search the world. Two executors handed the same `construction_id` receive the same requirement set
byte for byte, so a negative means *the registered specification was evaluated and blocked*, never "no
source this executor happened to find." `XASSET-0027` §I.3's **categorical vs. prerequisite**
distinction still does its work: a specification unlawful on its face is categorical; one merely unmet
today is prerequisite-blocked.

**Mechanically coupled.** `frozen_construction_universe()` emits exactly the shape
`validate_stage1_results()` consumes, and `closed_construction_universe()` returns it. One definition
of "construction" survives.

### G. Canonical amendment — lockstep, with preserved lineage

Both canonical files are amended under this decision's successor authority.

**Historical predecessor identity, preserved and never rewritten:**

- `PROTOCOL_V1.md` — `1a7b288718dfc688adb409ea9ecdf0fe5c858a32ee154f4f407c132895f41c8b`
- `pre_registration.yaml` — `bb25b1181c94d4dba2939a634b6fcb894f93597a664d5e91ffdcf021de3d385f`

<!-- XASSET-0028-HASH-PINS-V1
protocol_path: research/level1_endpoint_evidence/PROTOCOL_V1.md
protocol_sha256: 9bb1738a81193fd6640106fa04e1371cb2d75459f40948a3087fb74bffca4034
preregistration_path: research/level1_endpoint_evidence/pre_registration.yaml
preregistration_sha256: 4c3452b69787e9e6f8397758492627fc0e6601c48a7efa373820ffb73119e83e
predecessor_protocol_sha256: 1a7b288718dfc688adb409ea9ecdf0fe5c858a32ee154f4f407c132895f41c8b
predecessor_preregistration_sha256: bb25b1181c94d4dba2939a634b6fcb894f93597a664d5e91ffdcf021de3d385f
-->

- `PROTOCOL_V1.md`: `9bb1738a81193fd6640106fa04e1371cb2d75459f40948a3087fb74bffca4034`
- `pre_registration.yaml`: `4c3452b69787e9e6f8397758492627fc0e6601c48a7efa373820ffb73119e83e`

Version identity moves `ENDPOINT-0001-PREREG-V3` → `V4`, with the predecessor recorded. The
`XASSET-0027` record inside `construction_universe_closure` is retained **verbatim** under
`xasset_0027_predecessor_record` — including its own discipline that neither route was permanently
foreclosed, which `XASSET-0028` now vindicates: one of those very routes was available to a later unit.

**Effectivity.** Until this decision's lifecycle closes, the `XASSET-0027` predecessor identity governs.
The successor identity becomes effective only after all **six** gates: independent full exact-head
review, principal exact-head acceptance, merge, post-merge verification, merge-commit CI success, and
verification of the merged successor hashes and universe hash.

**Corrected under review `4946087943` MAJOR 1.** `lifecycle_effectivity.stage_1_execution_may_begin_only_after`
and `stages.stage_1.executable_only_after` still named the **spent** `XASSET-0027` precondition —
which, with that lifecycle complete and closure now asserted, would have read as already satisfied.
Both now name one exact `XASSET-0028` six-gate successor condition; `STAGE_1_EXECUTION_PRECONDITION`
and both validators follow; the `XASSET-0027` value survives only in explicitly historical predecessor
fields. The closure validator, which required five gates, now requires the same six.

**Fail-closed, not merely documented.** `closed_construction_universe()` now returns the real
680-record universe, so the enforcement machinery is testable — but `validate_stage1_results()`
consults `stage_1_operational_authorization_is_effective()` **first**, which reads the canonical
`stage_1_executability.executable` (false) and refuses. A results author cannot satisfy it from a
results document, and a merge alone cannot flip it. **There is no merge-to-execution gap.**

### H. The stale contradiction — corrected, answering MAJOR 2

`pre_registration.yaml`'s `zero_parameter_declaration.design_consequence` asserted a closed candidate
universe while the same file recorded `NOT_CLOSED`. The prior filing disclosed it but declined to fix
it, reasoning that the hash pin forbade edits. **The pin rule requires a separately accepted amendment;
it does not prohibit one** — and this is that amendment. The sentence is now **true** rather than
merely tolerated. No operative text anywhere says both `NOT_CLOSED` and `CLOSED`; the protocol mirror
agrees with the pre-registration, mechanically enforced.

### I. Structural closure is not authorization

| | |
|---|---|
| Construction universe | **CLOSED** — structural |
| Stage 1 | **NOT EXECUTED**, **NOT EXECUTABLE** — operational |
| Stage 2 | **NOT AUTHORIZED** |
| Application authority | **WITHHELD** |

No `stage1_results.yaml`, execution receipt, acquisition output, or candidate gate result is created.
`stage_1_executability.executable` remains `false` and the validator fails closed on lifecycle
authorization regardless of structural readability.

### J. Preserved unchanged

`XASSET-0024` §K.1 remains **unresolved** with both readings preserved, and no construction identity
assumes either. §J.12 remains **deferred**; no whole-candidate reconciliation enters any construction
identity. Representation remains `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED` — no aggregation rule, no
`CM-14`–`CM-17` designation.

### K. Firewalls

**Magnitude.** No endpoint, bound value, range, point, percentage, target or current allocation, equal
split, residual, midpoint, optimizer output, score, confidence weight, or preferred sleeve. Zero
consequential numeric free parameters under `NUM-0001` §18 — every count is a cardinality derived from
a closed population.

**RISK.** No substantive reuse; `/private/tmp/phq-risk0001-results` not accessed.

**Contamination — answering MINOR 2.** The prior module re-declared a barred-numeral tuple carrying
**four** values where the accepted predecessor protects **five**, with a narrower percentage regex. It
now **delegates to the accepted `scan_for_barred_content`**, so it can never again be weaker than its
predecessor.

**Dashboard — answering MINOR 1.** The unjustified `6_000_000` → `9_000_000` relaxation is **reverted**.
A structural once-per-decision invariant replaces it, parsing the renderer's stable
`data-decision-detail` / `data-decision-id` attributes — not source-Markdown lines.

### L. Absolute non-authorization

Executes no Stage 1 and creates no result artifact; authorizes no Stage 2, empirical work, data
acquisition, backtest, or candidate evaluation; produces no endpoint, bound, point, range, percentage,
weight, target, or allocation and selects, prefers, ranks, sequences, or budgets no sleeve; exercises no
endpoint authority; grants no evidence-admission or application authority; resolves §K.1 neither way and
decides §J.12 neither way; supplies no representation rule; performs no Level-1 or Level-2 sizing;
changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier,
cluster, cap, or margin state; authorizes no chart, ladder, optimizer, deployment, trade, order, or
brokerage action; and rewrites no accepted history.

## Rationale

The prior negative was not wrong to be cautious — it was wrong about which standard applies. Its own
decisive argument was that an authored registry would "relocate the unbounded qualitative search from
results time to freeze time." That argument holds only if the registry's contents are *chosen*. They
are not: every one of the 680 constructions is **generated** by crossing already-closed accepted
vocabularies with an already-closed comparison contract. There is nothing for an author to select, and
nothing for an executor to add, omit, or mutate. The search is not relocated; it is removed.

The clinching evidence is that the accepted pre-registration **already contained** the partition this
closure needs, and said comparators were "not fixed **here**" — leaving them for exactly this unit.

## Alternatives Considered

**Preserve the negative.** Rejected: it rests on a standard `XASSET-0027` §I.2 does not set.

**Register 720 with 40 `NOT_APPLICABLE` rows.** Rejected: §H's UAC comparison is not a pair record.

**Register existing-source constructions too.** Rejected: `XASSET-0025` Outcome C already searched the
frozen snapshot exhaustively, so those rows would re-run an accepted determination. Recorded as an
explicit disposition rather than a silent omission.

**Option B — leave architecture open and amend the canonical provenance model.** Rejected: it would
require amending a contract addressed to this unit, and it establishes closure only if a deterministic
bounded source-search universe can be stated. None exists — that is precisely the unbounded search the
negative filing correctly identified.

**Put input classes and gate ids in each construction.** Rejected: constant across all 680; they
discriminate no hypothesis.

**Hand-author a 680-row registry.** Rejected: a pure generator is the canonical source of identity, and
a duplicated list could drift from it.

## Consequences

Stage 1 gains a registered set to range over, so `XASSET-0027` §I.2's completeness rule becomes
meaningful and the family-slot grid is finally distinguishable from the universe it classified. Stage 1
remains blocked on this decision's lifecycle. Because the central outcome flips and the canonical
architecture materially expands, the pushed head requires a **new independent full exact-head review**,
not a delta.
