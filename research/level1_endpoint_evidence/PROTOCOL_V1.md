# PROTOCOL V1 — Level-1 endpoint-evidence program (`ENDPOINT-0001`)

Authorized by `governance/decisions/XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md`.

`research/level1_endpoint_evidence/pre_registration.yaml` is canonical for every closed identity,
candidate, gate, ordering, vocabulary, and count. **This protocol explains the design. It cannot
enlarge or override the YAML.** Where the two appear to differ, the YAML governs and the difference is
a defect requiring a governed correction.

`ENDPOINT-0001` is a **study identifier only**. It is not a governance decision prefix, and no
`ENDPOINT-####` decision series is created, implied, or reserved.

This document contains no endpoint, no bound, no percentage, no sleeve share, and no study result.

---

## 1. What this program is for

`XASSET-0025` Outcome C found that no accepted source supplies a qualifying Level-1 sleeve-share bound
for any sleeve, and that two things are missing: qualifying evidence, and competent authority.
`XASSET-0026` determined the lawful shape of the first purpose-built program to address the first of
those: **all four sleeves, no sleeve selected**.

This program is that program's first stage. Its job is narrow and specific:

> For every registered construction — each classified by one sleeve, one bound, one DRIVER class, and
> one lawful provenance family — determine whether a lawful endpoint-supporting evidence
> **construction** is identifiable at all, and where it is not, record every gate that blocks it.

It is deliberately **not** an empirical study, and section 4 explains why that is the honest design
rather than a reduction in ambition.

**Stage 1 is not executable under this charter.** The architecture below — families, gates,
disposition rules, reading map, deferrals, provenance requirements, and firewall — is what
`XASSET-0027` establishes. What it does **not** establish is a concrete construction universe over
which that architecture could run. Section 5.3 states why, and section 5.5 names the smallest
separately authorized step required to close it.

## 2. The governing question

Reproduced from `XASSET-0025` §K, unmodified, and instantiated identically for every candidate:

> For one named Level-1 sleeve, is there directly evidenced, question-matched economic content —
> admissible as a DRIVER under exactly one of `XASSET-0020` §E.1's six classes on its own subject
> matter — that intrinsically establishes a LOWER or an UPPER limit on that sleeve's share of one
> normalized unit of prospective unlevered asset-side capital, at exact precision, from a single
> origin, with no step whose coefficient, ordering, tolerance, cutoff, or selection could have been
> chosen differently?

A **null answer is a complete outcome** (`XASSET-0020` §J.3), not a defect to be patched.

## 3. The central problem, stated before the design rather than after it

**Directional evidence is not automatically magnitude evidence.** A charter that ignored this would
produce qualitative research with a percentage appended — the precise failure mode `XASSET-0024` §F
and `XASSET-0025` §F exist to prevent.

**3.1 — Every DRIVER class is defined on a sleeve or a comparison, not on the whole.** `XASSET-0020`
§E.1's six classes describe a sleeve's job, its opportunity cost against a direct alternative, its
loss path, its recovery, its pair co-behavior, and its deployability. The endpoint quantity, by
contrast, is a share **of one normalized unit** (`XASSET-0024` §C).

**3.2 — Bridging those two is exactly where a hidden model would enter.** Any mapping from sleeve
economics onto a share of the whole is a portfolio-construction model, and every version is already
barred: an optimizer or grid search, a composite score, a symmetry or equal-division convention, a
midpoint, a default range width, or a residual plug (`XASSET-0024` §D non-routes N4 and N5;
`XASSET-0020` §L and §M).

**3.3 — This program therefore tests the bridge instead of assuming it.** `G3_NORMALIZATION` asks, per
candidate, whether the construction would state the §C quantity or only a quantity in some other
denominator. A candidate that can only produce a sleeve-internal, within-fund, market-share,
per-share, or leverage-bearing quantity fails there and is recorded as blocked.

**3.4 — One textual observation, recorded as a fact and not as a prediction.** Of the six classes,
`portfolio_function` is the only one whose §E.1 scope language refers to the prospective **portfolio**
("the sleeve's directly evidenced job in the prospective portfolio"). Whether that suffices to carry a
share-of-the-whole statement is exactly what `G3` tests. This observation is about a class, not a
sleeve; it ranks nothing, prefers no sleeve, and predicts no outcome.

**3.5 — What the design refuses to do.** It does not invent an optimizer, score, voting system,
midpoint, residual, symmetry rule, or allocation model, and it does not append a magnitude to a
qualitative finding. Where a class can support direction but not magnitude, that is recorded honestly
at `G2` or `G3` and the candidate is not forced into an endpoint-producing role.

## 4. Why Stage 1 acquires no data

`XASSET-0025` Outcome C's binding failures were **T1/T2** (what the evidence measures) and **T5** (who
may certify it) — not data scarcity. Chartering acquisition before determining whether any acquirable
evidence could clear `G2`, `G3`, and `G5` would spend a data program on a question whose blocker may
not be data at all.

**Stage 2 — any empirical or data-acquiring work — is not authorized by `XASSET-0027`.** It becomes
eligible to be *proposed* only if Stage 1 identifies at least one constructible candidate, and even
then requires its own separate, later, explicitly accepted governance decision. Eligibility is not
entitlement.

## 5. Population, provenance families, and why the construction universe is not closed

### 5.1 The four classifying dimensions, each closed by accepted authority

| Dimension | Members | Count | Closed by |
|---|---|---|---|
| Sleeve | `equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto` | 4 | `XASSET-0019`; `XASSET-0020` §B |
| Bound | `LOWER`, `UPPER` | 2 | `XASSET-0024` §C |
| DRIVER class | `portfolio_function`, `valuation_opportunity_cost`, `downside_path_risk`, `recovery`, `diversification_cobehavior`, `sleeve_deployability` | 6 | `XASSET-0020` §E.1 — "six closed classes" |
| Provenance family | `R1_C1`, `R1_C3`, `R1_C4`, `R1_C5`, `R2_C2` | 5 | `XASSET-0023` §H + §H.4 item 3 |

### 5.2 Why the provenance families are exactly five, and why that is not this filing's invention

`XASSET-0023` §H says of the two origination routes: **"There is no third route."** §H.4 item 3 then
fixes route-class coherence exactly: *"A §H.3 derivation is NUM-0001 class 2. A §H.2 statement may
carry class 1, 3, 4, or 5."* Class 6 is disqualifying under §H.4 item 2.

The lawful `(route, NUM-0001 class)` pairs are therefore closed by accepted authority at exactly five:

| Family | Route | Class | Name |
|---|---|---|---|
| `R1_C1` | R1 | 1 | externally imposed |
| `R1_C3` | R1 | 3 | empirically calibrated |
| `R1_C4` | R1 | 4 | evidence-bounded governance selection |
| `R1_C5` | R1 | 5 | provisional governance guardrail |
| `R2_C2` | R2 | 2 | mathematically derived |

This program **enumerates** them. It does not select among them, rank them, invent one, or exclude
one — which is what preserves `XASSET-0026` §I.5's requirement that no route or class be pre-selected.

A construction outside those five would necessarily be one of `XASSET-0024` §D's non-routes **N1–N8**,
which are barred origination mechanisms rather than provenance families; they are listed in the
preregistration as excluded and are barred before evaluation rather than registered.

**What closing this vocabulary does and does not establish.** A family is a *classification of
provenance*, not a hypothesis. `XASSET-0023` §H.2 states the conditions under which an endpoint is
uniquely stated, and §H.3 the conditions for a source-prescribed derivation. Both are **constraint
sets, not generators** — satisfying a constraint set does not enumerate the objects that satisfy it.
Many distinct source identities, source architectures, comparator architectures, evidence forms,
external impositions, calibrations, governance selections, provisional guardrails, and prescribed
derivations can all inhabit the same family. Closing the family vocabulary therefore closes the
provenance classification and leaves the construction universe open.

### 5.3 Why the construction universe is not closed, and why Stage 1 is therefore not executable

The `4 × 2 × 6 × 5 = 240` product is a **family slot grid**: `48` cells × `5` provenance families,
`slot_id = {sleeve}::{bound}::{driver_class}::{family_id}`. It is exhaustive over the four closed
dimensions and is **not** exhaustive over constructions. Two analysts could occupy the same slot while
evaluating materially different source architectures. The grid is a classification scaffold for a
future construction universe; it is not that universe, and it is expressly **not a trial ceiling**.

Two routes to a genuinely closed universe were considered, and **neither is available to this
charter**:

- **A concrete finite registry.** Not closeable **by this charter from the currently accepted corpus
  alone**. The existing-source corpus is exactly `XASSET-0021`'s frozen snapshot, and `XASSET-0025`
  Outcome C already searched precisely that corpus exhaustively and found no qualifying source, so a
  Stage 1 restricted to it would re-run an accepted determination and add nothing. The remaining space
  is constructions whose sources do **not** yet exist, and accepted authority does not enumerate the
  concrete hypothetical source or construction architectures such a registry would need. Designing and
  freezing them would itself be substantive research-design work, reserved to the separately authorized
  §5.5 closure unit. **This charter does not determine whether that unit can or cannot successfully
  preregister a finite hypothetical-architecture registry** — only that this charter cannot close one
  now.
- **A deterministic construction grammar.** Likewise unavailable **from accepted authority as it
  stands**: no accepted decision supplies a finite grammar producing concrete source or derivation
  architectures, §H.2 and §H.3 are constraint sets, and the `(route, class)` product is a provenance
  classification rather than a construction grammar. Whether a lawful grammar could be designed is
  again a question for the §5.5 unit, not one answered here.

The route taken is therefore the third one: **an honest prerequisite**. `Stage 1 is NOT EXECUTABLE.`
No 240-slot run may be performed, and no such run could establish exhaustive non-constructibility,
because the slots bound provenance families rather than hypotheses. **A negative outcome is preferable
to invented completeness**, so this charter records that the universe is not closed rather than
manufacturing a registry it cannot support.

### 5.4 The completeness rule — what a negative would mean, once a universe exists

Once — and only once — a concrete construction universe is closed by its own separately authorized
unit, a cell may be recorded `BLOCKED_CATEGORICALLY` **only if every registered construction for that
cell was evaluated and every one returned `BLOCKED_CATEGORICALLY`**. Until that closure exists the
rule has no registered set to range over, which is one of the mechanical reasons Stage 1 cannot run.

**A negative on a family slot is not a negative on the family.** It would mean only that no
construction the executor considered within that provenance family qualified. It does not establish
that no construction within that family could qualify, and it may never be reported as exhaustive
non-constructibility.

**All four sleeves are covered; not all four need succeed.** A lawful result may identify a candidate
for one sleeve and none for the other three. The evidence determines which succeed. Nothing
prioritizes, ranks, sequences, or budgets a sleeve, and the family slot grid is one closed
classification precisely so that no ordering can imply preference.

### 5.5 The smallest separately authorized next step

**One governance unit whose scope is to determine whether a concrete construction universe can be
closed at all and, if so, to freeze it** (`CONCRETE_CONSTRUCTION_UNIVERSE_PREREGISTRATION`). That unit
must confront the open-hypothetical problem directly and must state its own answer, including that the
answer may itself be negative. This charter does not pre-decide it, does not choose among the
possibilities that unit may consider, and does not schedule it.

## 6. Gate sequence

Twelve gates, each restating an already-accepted requirement; none is invented here.

| # | Gate | Tests | Failure class |
|---|---|---|---|
| 1 | `G1_DRIVER_SUBJECT_MATTER` | DRIVER-admissible on the evidence's own subject matter (`J.3`) | categorical |
| 2 | `G2_MAGNITUDE_INTRINSICALITY` | quantitative statement intrinsic, not appended — under **both** §K.1 readings (`§D`, `J.4`) | categorical (see §7) |
| 3 | `G3_NORMALIZATION` | states the §C quantity, not another denominator (`§C`, `§F` Limb 1) | categorical |
| 4 | `G4_ORIGIN` | no barred origin, equal division, symmetry, residual, or reconstruction (`§F` Limb 2) | categorical |
| 5 | `G5_CONSTRAINT_SHAPE` | originates a bound rather than only clipping one (`§F` Limb 4, N1) | categorical |
| 6 | `G6_ROUTE_COMPLIANCE` | its own family's route in full, including competent stating authority (`J.5`, `J.6`) | categorical |
| 7 | `G7_DISCRETION_AND_PROVENANCE` | its own family's class coherently; class-4 eight-item test; class-5 label + review condition (`J.7`) | categorical |
| 8 | `G8_UNIQUENESS` | exactly one lawful value, no tie-break rule (`J.8`) | categorical |
| 9 | `G9_REPRESENTATION` | self-contained (`§G` path 1) or separately ruled (path 2) (`J.9`) | prerequisite |
| 10 | `G10_PAIR_INDEPENDENCE` | unresolved pair not consumed at all (`§H.4`, `J.10`) | categorical |
| 11 | `G11_EXACTNESS_AND_DETERMINISM` | exact precision, no ungoverned rounding, byte-identical (`J.11`) | categorical |
| 12 | `G12_SNAPSHOT_ADMISSIBILITY_PATH` | a lawful snapshot successor is identifiable (`J.1`, `J.2`) | prerequisite |

**Every applicable gate is evaluated before a candidate is classified.** `first_failing_gate_id`
survives only as a reporting convenience computed *after* the disposition is already fixed; it never
participates in classification.

### 6.1 What "categorical" means, precisely

**Categorical** = *not closeable by a named prerequisite while the currently accepted methodology
remains unchanged.* It does **not** mean permanently impossible under all future governance: a later
accepted methodology amendment can change a currently categorical rule, and such an amendment is
already an `XASSET-0027` reopen trigger. **Prerequisite** = closeable by a named, separately authorized
prerequisite without any methodology amendment, and the dependency must be named.

`G12` records whether a snapshot successor is *identifiable*. **No snapshot successor is created,
extended, replaced, or authorized by this program** (`XASSET-0026` §G.2 constraint 3).

## 7. The `XASSET-0024` §K.1 open reading

§K.1 records an open question: whether §E.1's six classes are subject-matter classes capable of
housing a magnitude statement, or preference-only classes that cannot. Under the preference-only
reading, both R1 and R2 collapse and **no candidate can succeed**.

This program is exactly the unit whose viability turns on that reading, and it **does not resolve it**
— resolving it would be a `XASSET-0020` §E.1 methodology amendment performed inside a research
charter, without its own authorization or review.

`G2` is therefore evaluated **under both readings**, each recorded from the closed vocabulary
`PASSES` / `FAILS` / `UNABLE_TO_DETERMINE`, and mapped by a closed table:

| Subject-matter reading | Preference-only reading | `G2` effective outcome | Required `G2` gate result | Reading-dependent |
|---|---|---|---|---|
| `PASSES` | `PASSES` | `PASSES` | `PASS` | no |
| `FAILS` | `FAILS` | `FAILS_CATEGORICALLY` | `FAIL` | no |
| **`PASSES`** | **`FAILS`** | **`UNABLE_TO_DETERMINE`** | **`UNABLE_TO_DETERMINE`** | **yes** |
| `FAILS` | `PASSES` | `INCOHERENT_REJECTED` | `RECORD_REJECTED` | no |
| `UNABLE_TO_DETERMINE` | any | `UNABLE_TO_DETERMINE` | `UNABLE_TO_DETERMINE` | no |
| any | `UNABLE_TO_DETERMINE` | `UNABLE_TO_DETERMINE` | `UNABLE_TO_DETERMINE` | no |

The third row is the load-bearing one. **An unresolved methodology reading is not a categorical
impossibility**, so a reading-dependent candidate maps to `UNABLE_TO_DETERMINE` — a governed
uncertainty outcome — never to `BLOCKED_CATEGORICALLY`. Calling it categorical would assert that
accepted authority has settled §K.1 against the subject-matter reading, which it expressly has not.

The fourth row is a recording defect, not an outcome: the preference-only reading is strictly narrower
than the subject-matter reading, so passing the narrower while failing the broader is incoherent and
is rejected rather than mapped.

### 7.1 The mapping is coupled to the recorded gate result, not annotated beside it

The **Required `G2` gate result** column is an **enforced identity**. A results record whose recorded
`G2` gate result disagrees with what its own two reading fields map to is rejected. Without that
coupling the table would be decorative: a record could carry the reading-dependent pair while
recording `G2` as `PASS`, and the candidate would derive to `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED` — the
exact outcome the open §K.1 reading is supposed to make impossible.

With the coupling in place and §9's candidate precedence, a reading-dependent candidate necessarily
records `G2 = UNABLE_TO_DETERMINE` and therefore necessarily disposes to `UNABLE_TO_DETERMINE`, unless
some categorical gate independently fails — **including when a prerequisite gate also fails**. That is
the end-to-end guarantee the closed table promises.

## 8. What Stage 1 tests, and what it defers

### 8.1 The Stage-1-testable subset

`CONSTRUCTIBLE_CANDIDATE_IDENTIFIED` means **"a construction candidate satisfying the Stage-1-testable
subset of `XASSET-0024` §J.1–§J.12"** — never that full §J admissibility has been established. The
result schema forbids any claim of full §J.1–§J.12 compliance.

| §J item | Stage-1 status | Basis |
|---|---|---|
| J.1 admission | partially testable | `G12` + the source-currentness rule |
| J.2 snapshot position | partially testable | `G12`, identifiability only |
| J.3 DRIVER classification | testable | `G1` |
| J.4 question identity | testable | `G2`, `G3`, `G4`, `G5` |
| J.5 competent authority | testable | `G6` |
| J.6 route compliance | testable | `G6` |
| J.7 provenance | testable | `G7` |
| J.8 uniqueness | testable | `G8` |
| J.9 representation closure | testable | `G9` |
| J.10 pair independence | testable | `G10` |
| J.11 exactness and determinism | testable | `G11` |
| **J.12 reconciliation feasibility** | **not yet determinable — deferred** | whole-candidate prerequisite |

### 8.2 Why J.12 cannot be a per-candidate gate

`XASSET-0024` §J.12 requires **exact set-valued reconciliation under `XASSET-0020` §K**. §K defines
that identity jointly:

> `UNSIZED_UNASSIGNED_CAPITAL = normalized_asset_unit − separately_governed_liquidity_asset − sum(admitted_sleeve_points)`

and, for ranges, over "the exact feasible set of sleeve vectors inside the admitted endpoints," with a
negative complement invalidating the candidate. **It is inherently a whole-candidate, cross-sleeve
condition.**

Stage 1 produces no endpoint value, prohibits cross-sleeve and cross-bound reference, and forbids any
share from appearing in its result. There is therefore nothing from which an exact reconciliation could
be computed, and any Stage-1 verdict on it would require assuming future endpoint values or other
sleeves' outcomes.

J.12 is accordingly **removed from the per-candidate gate sequence** and recorded as
`NOT_YET_DETERMINABLE_DEFERRED`, to be cleared at the first later, separately authorized stage where
actual candidate endpoint values or sets coexist. **Introducing cross-sleeve arithmetic into Stage 1
merely to let a reconciliation gate return a verdict is prohibited** — it would breach the
single-sleeve bound rule, the cross-sleeve prohibition, and the no-endpoint-value rule at once.

## 9. Disposition — deterministic and order-independent

Three levels, each a quantifier over a closed set. **No disposition depends on gate order, candidate
order, or cell order.**

**Candidate** — universal over its own gate results, **categorical dominates, then uncertainty**:

1. any categorical gate failure → `BLOCKED_CATEGORICALLY`
2. else any gate `UNABLE_TO_DETERMINE` → `UNABLE_TO_DETERMINE`
3. else any prerequisite gate failure → `BLOCKED_PENDING_SEPARATE_PREREQUISITE`
4. else → `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED`

A candidate failing **both** a prerequisite gate and any categorical gate is `BLOCKED_CATEGORICALLY`,
never prerequisite-blocked. Closing the named prerequisite would leave the categorical defect standing,
so recording it as a closeable to-do would misstate the evidence. Evaluating every applicable gate
before classifying is precisely what stops this depending on which gate is reached first.

### 9.0 Why uncertainty outranks a prerequisite failure

The ordering of steps 2 and 3 is **logical, not stylistic**. A categorical bar may dominate uncertainty
because the candidate is barred whatever the uncertainty resolves to. A prerequisite failure may not,
because **closing the named prerequisite cannot resolve the uncertainty.**

Concretely: a candidate whose `G2` is `UNABLE_TO_DETERMINE` because `XASSET-0024` §K.1 is unresolved,
and whose `G9` representation also fails, is not merely waiting on a representation rule. Supplying
that rule would leave §K.1 exactly as unresolved. Recording it as `BLOCKED_PENDING_SEPARATE_PREREQUISITE`
would convert an open methodology question into a closeable to-do — the prerequisite would be closed,
the candidate re-evaluated, and the uncertainty would still be there. **Absent a categorical bar,
uncertainty is never downgraded.**

This ordering governs a **single candidate's own gate results only**. Cell and roll-up precedence are
unchanged existential tests, because a *different* candidate that is determinately prerequisite-blocked
can legitimately keep a cell open even while another candidate in that cell is uncertain.

**Cell** — existential over its own five family-slot candidate dispositions:

1. any `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED` → `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED`
2. else any `BLOCKED_PENDING_SEPARATE_PREREQUISITE` → `BLOCKED_PENDING_SEPARATE_PREREQUISITE`
3. else any `UNABLE_TO_DETERMINE` → `UNABLE_TO_DETERMINE`
4. else (all five categorical) → `BLOCKED_CATEGORICALLY`

**Roll-up** — existential over its own six cell outcomes: `CANDIDATE_CONSTRUCTION_IDENTIFIED` →
`PREREQUISITE_REQUIRED` → `UNABLE_TO_DETERMINE` → `NO_CONSTRUCTIBLE_CANDIDATE`.

### 9.1 The quantifier asymmetry is deliberate

Candidate disposition is **universal over gates** while cell outcome is **existential over
candidates**. A candidate is blocked if any one of its gates blocks it; a cell is open if any one of
its lawful families survives. Both are quantifier tests over closed sets, and **neither weights,
counts, averages, ranks, or votes**. No numeric threshold participates anywhere, which is why none of
this is a score and none of it can become one.

## 10. Point and range

`XASSET-0024` §H.3's RANGE-first posture is carried forward unchanged: RANGE feasibility is
established before POINT feasibility **unless a candidate's evidence uniquely supplies a point**, in
which case the point route remains available on its own terms. Each candidate records
`WOULD_SUPPORT_RANGE_ENDPOINT`, `WOULD_SUPPORT_POINT_ENDPOINT`, or `WOULD_SUPPORT_NEITHER`. This is a
sequencing preference and bars nothing.

## 11. Representation

Disposition `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED` (`XASSET-0026` §H) is preserved. The
self-contained path (`XASSET-0024` §G path 1) is preserved wherever lawful and is not narrowed,
disfavoured, or made conditional.

**No representation rule is created, and CM-14 through CM-17 membership is not designated.** A
candidate requiring cross-representation combination records the exact dependency and fails `G9` as a
prerequisite; the dependency is never silently solved, and no majority, average, weighting,
representative selection, or "most conservative" selection is performed (`XASSET-0021` §E.3). Where
such a candidate **also** fails any categorical gate, §9's categorical dominance applies and it is not
recorded as merely prerequisite-blocked; where it instead carries any `UNABLE_TO_DETERMINE`, §9.0's
uncertainty precedence applies and it is likewise not recorded as merely prerequisite-blocked.

## 12. Parameters, and why there are none

Stage 1 introduces **zero consequential numeric parameters** under `NUM-0001` §18's definition — no
threshold, tolerance, cutoff, materiality level, window, weight, coefficient, or score. Every gate is
a qualitative admissibility test drawn from accepted authority; every count in §5 is derived from the
closed populations rather than chosen.

**A study with no free numeric parameter cannot be tuned toward a preferred outcome.** The validator
asserts the parameter registry is empty; introducing any parameter requires a separately accepted
amendment with new hash pins.

The *qualitative* search surface is a different matter, and §5.3 states it plainly: the family
vocabulary is closed, but the construction universe is not, so the executor's choice of which
constructions to try is **not** yet closed either. That is precisely why Stage 1 is not executable and
why closing the construction universe is the named prerequisite rather than an optional refinement.

For the same reason, **out-of-sample and walk-forward discipline is `NOT_APPLICABLE` to Stage 1** —
there is no sample, no held-out period, and no fitted quantity, so a split would be a ritual with no
object. Both disciplines are **required of any future Stage 2**.

## 13. Prohibited inputs

The complete `XASSET-0025` §F firewall applies. No barred historical value, residual, assigned sum,
equal baseline, fixed adjustment increment, `R2`/`R3` construct, current target, holding, weight,
tier, gate, cluster cap, issuer ceiling, RISK scenario magnitude, lapsed RISK parameter, gold-parity
threshold, chart or technical value, margin/leverage/buffer state, within-fund or market composition
share, unaggregated per-share valuation, or decision-prose value — **including `XASSET-0027`'s own
prose** — may be used, anchored to, initialized from, centered on, sanity-checked against, or
reverse-engineered toward.

Barred values are referenced **by name rather than reproduced**: writing a barred numeral into this
protocol would introduce the very anchor the firewall exists to exclude. `XASSET-0025` §F records
their exact locations for anyone who needs them.

Clearing a literal-string scan is a **floor, not the boundary** (`XASSET-0024` §F Limb 2;
`XASSET-0023` §H.2 item 6). `G4` tests origin, not spelling — a freshly computed equal split is barred
exactly as a historical one is.

## 14. RISK boundary

RISK-0001 Attempt 2 is complete. No retry, no Attempt 3, no family re-question, and no parameter reuse
without separate authority. `/private/tmp/phq-risk0001-results` is never accessed, modified, deleted,
cleaned, reset, stashed, rebased, or repurposed. Accepted RISK evidence may be cited only within its
accepted historical meaning.

## 15. Execution, provenance, stopping, and defects

- **Attempt identity.** Every execution records an attempt id, both observed canonical hashes, and the
  repository head SHA. Unregistered attempts are prohibited. A hash mismatch **voids execution
  authority** and halts.
- **Per-candidate provenance.** Every candidate result carries its `construction_id`, `cell_id`,
  sleeve, bound, DRIVER class, `family_id`, route, `NUM-0001` class, governing authority references,
  full gate results, both categorical and prerequisite failure lists, and its `source_architecture`.
  A candidate that consults an actual admitted source is `EXISTING_SOURCE_ARCHITECTURE` and **must**
  carry that source's exact path and SHA-256; a candidate describing the shape a future source would
  need is `HYPOTHETICAL_SOURCE_ARCHITECTURE`, carries a stated requirements description, and **must
  not** carry a path or hash. Most such candidates will be hypothetical, because `XASSET-0025`
  Outcome C found no qualifying source exists.
- **Frozen provenance, not results-time authorship.** For an existing-source architecture, the exact
  `source_path` and `source_sha256` must be **frozen before execution** as part of the construction
  identity, and the recorded digest must be **recomputed from the observed file bytes and match**.
  Accepting a syntactically valid path plus an arbitrary 64-hex string validates shape, not identity.
  For a hypothetical architecture, the requirements must likewise be frozen before execution: a
  non-empty string authored in the results document is not a preregistration. A result author may
  report a frozen architecture but may never invent or alter one. **No architecture is currently
  frozen**, because no construction universe exists — which is the direct mechanical reason no results
  document can satisfy these requirements today.
- **Stopping.** Stage 1 terminates only when every registered construction in the closed construction
  universe carries a recorded disposition. That registered set is supplied by the future closure unit,
  **not** by the 240 family slots, so the rule currently ranges over nothing. **Early stop on a
  positive finding is prohibited** — it would advantage whichever candidate happened to be evaluated
  first and would make a negative elsewhere unexhaustive. Partial publication is prohibited.
- **No rerun after outcomes are observed.** A rerun requires a separately accepted amendment or a new
  authorized study, on a material new evidence regime or a separately governed integrity correction. A
  discovered defect does not silently authorize a second run: record it, halt, and return for separate
  governance.
- **No history mining.** Gates, candidates, and vocabularies are frozen before evaluation. No
  outcome-aware gate change, reordering, reinterpretation, candidate addition, or candidate removal.
- **Negative-result preservation.** Every registered construction's disposition is recorded regardless
  of direction. Suppressing any is prohibited.

## 16. What the Stage 1 output is not

The results record is a **feasibility finding about constructibility over the Stage-1-testable subset
of `XASSET-0024` §J**. It states no endpoint, contains no share, and is classified **non-DRIVER and
non-admissible**.

It may never be cited, admitted, or relied upon as endpoint-supporting evidence, and it may not claim
full §J.1–§J.12 compliance. A later filing attempting either would be manufacturing the very source
this program was chartered to test the feasibility of.

## 17. Lifecycle and downstream boundary

`XASSET-0027` becomes operationally effective **only after all five of**: accepted independent
exact-head review; principal exact-head acceptance; merge; immediate post-merge verification; and
successful merge-commit CI — with the merged canonical hashes verified from the merged commit.
**Merge alone is not sufficient.**

**Lifecycle closure does not make Stage 1 executable.** It makes this architecture effective. Stage 1
additionally requires a **closed concrete construction universe**, which `XASSET-0027` does not create
and does not authorize anyone to create; that requires its own separate unit (§5.5). Both conditions
are necessary, and no Stage-1 mutation lane may open until both are met.

Even a fully successful Stage 1 would change nothing on its own. The path from here remains, in
dependency order and each requiring its own separate authorization:

new evidence → **lawful snapshot successor** → endpoint-capable downstream consumption → application.

`XASSET-0021`'s closure matrix is untouched, `APPLICATION_AUTHORIZATION_REGISTRY` remains empty, no
`intelligence/level1_application/` artifact exists or is authorized, and **application authority
remains WITHHELD**.

## Amendment — `XASSET-0028` successor identity

**Amended by `XASSET-0028`.** `XASSET-0027` recorded that the concrete construction universe was
`NOT_CLOSED` and that Stage 1 was therefore not executable. `XASSET-0028` is the separately accepted
amendment `XASSET-0027`'s own pin rule requires, and it **closes that universe**: a deterministic,
finite, preregistered, grammar-derived universe of **680 registered constructions** across the 48
cells, with exact identity, ordering, cardinality, and an aggregate integrity hash.

The closure basis supplies **no new comparator rule**. It enumerates `XASSET-0020` §H's already-closed
direct-comparison contract — six unordered sleeve-sleeve pairs, plus a mandated direct comparison of
each sleeve with `UNSIZED_UNASSIGNED_CAPITAL` — crossed with the pre-registration's own canonical
`driver_class_scope` partition. Nothing is selected, ranked, preferred, invented, or excluded.

Every registered construction freezes its **source architecture** —
`HYPOTHETICAL_SOURCE_ARCHITECTURE` — together with deterministically generated
`hypothetical_source_requirements`, as `frozen_provenance_requirements` (addressed by name to this
unit) requires. `source_path` and `source_sha256` are absent, per `hypothetical_forbids`. The
existing-source half is not omitted but **already resolved**: `XASSET-0027` §I.1.1 records that
`XASSET-0025` Outcome C exhaustively searched `XASSET-0021`'s frozen snapshot and that "the remaining
space is constructions whose sources do not yet exist." No source identity is searched for, so a
negative means the frozen specification was evaluated, not that an executor failed to find something.

**Structural closure is not operational authorization.** Stage 1 is **NOT EXECUTED** by `XASSET-0028`
and remains **NOT EXECUTABLE** until `XASSET-0028`'s own lifecycle closes in full — all six gates:
independent full exact-head review, principal exact-head acceptance, merge, post-merge verification,
merge-commit CI success, and verification of the merged successor hashes and universe hash. That one
six-gate condition is the sole operative Stage-1 execution precondition; the `XASSET-0027` condition
is spent and retained only as predecessor history. There is no merge-to-execution gap.

Predecessor canonical identity remains auditable and is never rewritten. Until `XASSET-0028` is
effective, the `XASSET-0027` predecessor identity governs; after it, the successor identity governs.

`XASSET-0024` §K.1 remains **unresolved** with both readings preserved, §J.12 remains **deferred**,
representation remains `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`, Stage 2 remains **unauthorized**,
and application authority remains **WITHHELD**.

<!-- ENDPOINT-0001-PROTOCOL-MIRROR-V1
study_id: ENDPOINT-0001
sleeve_count: 4
bound_count: 2
driver_class_count: 6
construction_family_count: 5
cell_count: 48
family_slot_count: 240
roll_up_unit_count: 8
gate_count: 12
consequential_parameter_count: 0
stage_1_executable: false
construction_universe_closed: true
registered_construction_count: 680
construction_universe_sha256: 73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224
stage_1_structurally_closed: true
stage_1_operationally_authorized: false
stage_2_authorized: false
j12_deferred: true
hash_version: ENDPOINT-0001-PREREG-V4
predecessor_hash_version: ENDPOINT-0001-PREREG-V3
-->
