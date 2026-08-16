# PROTOCOL V1 — Level-1 endpoint-evidence program (`ENDPOINT-0001`)

Authorized by `governance/decisions/XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md`.

`research/level1_endpoint_evidence/pre_registration.yaml` is canonical for every closed identity,
cell, gate, ordering, vocabulary, and count. **This protocol explains the design. It cannot enlarge or
override the YAML.** Where the two appear to differ, the YAML governs and the difference is a defect
requiring a governed correction.

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

> For each combination of one sleeve, one bound, and one DRIVER class, determine whether a lawful
> endpoint-supporting evidence **construction** is identifiable at all — and where it is not, record
> the exact first gate that blocks it.

It is deliberately **not** an empirical study, and section 3 explains why that is the honest design
rather than a reduction in ambition.

## 2. The governing question

Reproduced from `XASSET-0025` §K, unmodified, and instantiated identically for every cell:

> For one named Level-1 sleeve, is there directly evidenced, question-matched economic content —
> admissible as a DRIVER under exactly one of `XASSET-0020` §E.1's six classes on its own subject
> matter — that intrinsically establishes a LOWER or an UPPER limit on that sleeve's share of one
> normalized unit of prospective unlevered asset-side capital, at exact precision, from a single
> origin, with no step whose coefficient, ordering, tolerance, cutoff, or selection could have been
> chosen differently?

A **null answer is a complete outcome** (`XASSET-0020` §J.3), not a defect to be patched.

## 3. The central problem, stated before the design rather than after it

**Directional evidence is not automatically magnitude evidence.** A charter that ignored this would
produce qualitative research and then append a percentage to it, which is the precise failure mode
`XASSET-0024` §F and `XASSET-0025` §F exist to prevent.

The problem has a specific shape here, and the design is built around it.

**3.1 — Every DRIVER class is defined on a sleeve or a comparison, not on the whole.** `XASSET-0020`
§E.1's six classes describe a sleeve's job, its opportunity cost against a direct alternative, its
loss path, its recovery, its pair co-behavior, and its deployability. The endpoint quantity, by
contrast, is a share **of one normalized unit** (`XASSET-0024` §C). Evidence naturally arrives in a
sleeve's own terms; the endpoint is stated in the whole's terms.

**3.2 — Bridging those two is exactly where a hidden model would enter.** Converting "this sleeve
does job J" into "this sleeve's share is at least X of the whole" requires something that maps sleeve
economics onto a share of the whole. Any such mapping is a portfolio-construction model, and every
version of one is already barred: an optimizer or grid search, a composite score, a symmetry or
equal-division convention, a midpoint, a default range width, or a residual plug
(`XASSET-0024` §D non-routes N4 and N5; `XASSET-0020` §L and §M).

**3.3 — This program therefore tests the bridge instead of assuming it.** Gate `G3_NORMALIZATION`
asks, per cell, whether the candidate construction would state the §C quantity or only a quantity in
some other denominator. A cell that can only produce a sleeve-internal, within-fund, market-share,
per-share, or leverage-bearing quantity fails there and is recorded as blocked.

**3.4 — One textual observation, recorded as a fact and not as a prediction.** Of the six classes,
`portfolio_function` is the only one whose §E.1 scope language refers to the prospective **portfolio**
("the sleeve's directly evidenced job in the prospective portfolio"). Whether that suffices to carry a
share-of-the-whole statement is exactly what `G3` tests. This observation is about a class, not a
sleeve; it ranks nothing, prefers no sleeve, and predicts no outcome.

**3.5 — What the design refuses to do.** It does not invent an optimizer, score, voting system,
midpoint, residual, symmetry rule, or allocation model, and it does not append a magnitude to a
qualitative finding. Where a class can support direction but not magnitude, that is recorded honestly
at `G2` or `G3` and the cell is not forced into an endpoint-producing role.

## 4. Why Stage 1 acquires no data

`XASSET-0025` Outcome C's binding failures were **T1/T2** (what the evidence measures) and **T5** (who
may certify it) — not data scarcity. Chartering acquisition before determining whether any acquirable
evidence could clear `G2`, `G3`, and `G5` would spend a data program on a question whose blocker may
not be data at all.

Stage 1 answers that first, cheaply, deterministically, and reversibly. **Stage 2 — any empirical or
data-acquiring work — is not authorized by `XASSET-0027`.** It becomes eligible to be *proposed* only
if Stage 1 identifies at least one constructible candidate, and even then requires its own separate,
later, explicitly accepted governance decision. Eligibility is not entitlement.

## 5. Population and cells

Closed, and fixed before evaluation.

| Dimension | Members | Count |
|---|---|---|
| Sleeve | `equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto` | 4 |
| Bound | `LOWER`, `UPPER` | 2 |
| DRIVER class | `portfolio_function`, `valuation_opportunity_cost`, `downside_path_risk`, `recovery`, `diversification_cobehavior`, `sleeve_deployability` | 6 |

One cell is **one sleeve × one bound × one DRIVER class**. The derived ceiling is
`4 × 2 × 6 = 48` cells, with zero reserve. Unused capacity lapses and cannot be reallocated.

**Route (R1/R2) and NUM-0001 class are recorded fields, not cell dimensions.** They are properties of
a candidate construction evaluated inside a cell; making them dimensions would duplicate cells without
adding coverage. Enumerating all six DRIVER classes for every sleeve and bound is what preserves
`XASSET-0026` §I.5's requirement that **no route or class be pre-selected**.

**All four sleeves are covered. Not all four need succeed.** A lawful result may identify a candidate
for one sleeve and none for three. The evidence determines which cells succeed; the author does not.
No sleeve is prioritized, ranked, sequenced, or budgeted ahead of another, and the 48 cells are
evaluated as one closed set precisely so that no ordering can imply preference.

## 6. Gate sequence

Thirteen gates, evaluated in strict ascending index, **first failure wins**. Each gate restates an
already-accepted requirement; none is invented here.

| # | Gate | Tests | Failure |
|---|---|---|---|
| 1 | `G1_DRIVER_SUBJECT_MATTER` | DRIVER-admissible on the evidence's own subject matter (`J.3`) | categorical |
| 2 | `G2_MAGNITUDE_INTRINSICALITY` | quantitative statement intrinsic, not appended (`§D`, `J.4`) | categorical |
| 3 | `G3_NORMALIZATION` | states the §C quantity, not another denominator (`§C`, `§F` Limb 1) | categorical |
| 4 | `G4_ORIGIN` | no barred origin, equal division, symmetry, residual, or reconstruction (`§F` Limb 2, N4/N5/N7) | categorical |
| 5 | `G5_CONSTRAINT_SHAPE` | originates a bound rather than only clipping one (`§F` Limb 4, N1) | categorical |
| 6 | `G6_ROUTE_COMPLIANCE` | R1 in full or R2 in full, R2 source-prescribed with no free step (`J.6`, `H.3` item 7) | categorical |
| 7 | `G7_DISCRETION_AND_PROVENANCE` | NUM-0001 class 1–5; class 4's eight-item test; class 5's label and review condition (`§E.3`, `J.7`) | categorical |
| 8 | `G8_UNIQUENESS` | exactly one lawful value, no tie-break rule (`J.8`) | categorical |
| 9 | `G9_REPRESENTATION` | self-contained (`§G` path 1) or separately ruled (path 2) (`J.9`) | prerequisite |
| 10 | `G10_PAIR_INDEPENDENCE` | unresolved pair not consumed at all (`§H.4`, `J.10`) | categorical |
| 11 | `G11_EXACTNESS_AND_DETERMINISM` | exact precision, no ungoverned rounding, byte-identical (`J.11`) | categorical |
| 12 | `G12_RECONCILIATION_FEASIBILITY` | exact set-valued reconciliation feasible, no plug or proxy (`J.12`) | categorical |
| 13 | `G13_SNAPSHOT_ADMISSIBILITY_PATH` | a lawful snapshot successor is identifiable (`J.1`, `J.2`) | prerequisite |

Two failure dispositions are distinguished deliberately. **Categorical** means no future authorization
can lift the bar — it is a property of what the evidence measures or where it came from.
**Prerequisite** means a named, closeable gap that a separately authorized unit could supply. That
distinction is the same one `XASSET-0025` §I drew when it explained why every cell there was
`NO_CANDIDATE_FOUND` rather than a gap category, and it matters for the same reason: it prevents a
categorical bar from being quietly recorded as a to-do.

`G13` records whether a snapshot successor is *identifiable*. **No snapshot successor is created,
extended, replaced, or authorized by this program** (`XASSET-0026` §G.2 constraint 3).

## 7. The `XASSET-0024` §K.1 open reading

`XASSET-0024` §K.1 records an open question: whether §E.1's six classes are subject-matter classes
capable of housing a magnitude statement, or preference-only classes that cannot. Under the
preference-only reading, both R1 and R2 collapse and **no cell can succeed**.

This program is exactly the unit whose viability turns on that reading, and it **does not resolve it**
— resolving it would be a `XASSET-0020` §E.1 methodology amendment performed inside a research
charter, without its own authorization or review.

Instead, `G2` is evaluated **under both readings**, and every cell records:

- `g2_outcome_under_subject_matter_reading`
- `g2_outcome_under_preference_only_reading`
- `g2_outcome_is_reading_dependent`

A cell that passes `G2` only under the subject-matter reading is recorded as **reading-dependent**,
not as passing. This preserves `XASSET-0024` §K.1, `XASSET-0025` §O.1, and `XASSET-0026` §K.2 exactly
as each left the question, while still producing full information for whichever unit eventually
addresses it.

## 8. Bound and sleeve independence

- **LOWER and UPPER are independently governed.** Each bound's six cells are evaluated on their own;
  no cell outcome may reference the other bound's outcome; neither bound inherits the other's
  representation coverage (`XASSET-0021` §E.2, §F; `XASSET-0024` §J's express answer).
- **No sleeve result is inferred from another's.** No cross-sleeve derivation, sum, residual,
  complement, or reconciliation participates in any outcome.
- **Evidence for LOWER and UPPER may differ** in identity, DRIVER class, route, and NUM-0001 class.

## 9. Roll-up — an existence test, not a score

Each of the 8 (sleeve, bound) units takes its disposition from its own six cells by a fixed precedence
order, frozen before evaluation:

1. any cell `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED` → `CANDIDATE_CONSTRUCTION_IDENTIFIED`
2. else any cell `BLOCKED_PENDING_SEPARATE_PREREQUISITE` → `PREREQUISITE_REQUIRED`
3. else any cell `UNABLE_TO_DETERMINE` → `UNABLE_TO_DETERMINE`
4. else all cells `BLOCKED_CATEGORICALLY` → `NO_CONSTRUCTIBLE_CANDIDATE`

**Each step is an existence quantifier.** No cell is weighted, counted, averaged, ranked, or voted; no
numeric threshold participates; nothing is summed across sleeves. This is why the roll-up is not a
score and cannot become one.

## 10. Point and range

`XASSET-0024` §H.3's RANGE-first posture is carried forward unchanged: RANGE feasibility is
established before POINT feasibility **unless a candidate's evidence uniquely supplies a point**, in
which case the point route remains available on its own terms. Each cell records
`WOULD_SUPPORT_RANGE_ENDPOINT`, `WOULD_SUPPORT_POINT_ENDPOINT`, or `WOULD_SUPPORT_NEITHER`. This is a
sequencing preference and bars nothing.

## 11. Representation

Disposition `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED` (`XASSET-0026` §H) is preserved. The
self-contained path (`XASSET-0024` §G path 1) is preserved wherever lawful and is not narrowed,
disfavoured, or made conditional.

**No representation rule is created, and CM-14 through CM-17 membership is not designated.** A cell
whose candidate would require cross-representation combination records the exact representation
dependency and blocks at `G9` as a prerequisite. The dependency is never silently solved, and no
majority, average, weighting, representative selection, or "most conservative" selection is performed
(`XASSET-0021` §E.3).

## 12. Parameters, and why there are none

Stage 1 introduces **zero consequential numeric parameters** under `NUM-0001` §18's definition. It
applies no threshold, tolerance, cutoff, materiality level, window, weight, coefficient, or score.
Every gate is a qualitative admissibility test drawn from accepted authority; every count in section 5
is derived from the closed population rather than chosen.

The consequence is a design property worth stating plainly: **a study with no free numeric parameter
cannot be tuned toward a preferred outcome**, and there is nothing for a sweep or a
neighboring-parameter robustness check to perturb. The dedicated validator asserts the registry's
parameter list is empty; introducing any parameter requires a separately accepted amendment with new
hash pins.

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

## 15. Execution, stopping, and defects

- **Attempt identity.** Every execution records an attempt id, both observed canonical hashes, and the
  repository head SHA. Unregistered attempts are prohibited. A hash mismatch **voids execution
  authority** and halts.
- **Stopping.** Stage 1 terminates only when all 48 cells carry a recorded outcome. **Early stop on a
  positive finding is prohibited** — it would advantage whichever cell happened to be evaluated first.
  Partial publication is prohibited.
- **No rerun after outcomes are observed.** A rerun requires a separately accepted amendment or a new
  authorized study, on a material new evidence regime or a separately governed integrity correction. A
  discovered defect does not silently authorize a second run: record it, halt, and return for separate
  governance.
- **No history mining.** Gates, cells, and vocabularies are frozen before evaluation. No
  outcome-aware gate change, reordering, reinterpretation, cell addition, or cell removal.
- **Negative-result preservation.** All 48 outcomes are recorded regardless of direction. Suppressing
  any cell outcome is prohibited.

## 16. What the Stage 1 output is not

The results record is a **feasibility finding about constructibility**. It states no endpoint, contains
no share, and is classified **non-DRIVER and non-admissible**.

It may never be cited, admitted, or relied upon as endpoint-supporting evidence. A later filing that
attempted to do so would be manufacturing the very source this program was chartered to test the
feasibility of — and its result schema forbids any numeric sleeve share, bound value, percentage of
the normalized unit, target, weight, composite score, rank, or portfolio reconciliation from appearing
in it at all.

## 17. Downstream boundary

Even a fully successful Stage 1 changes nothing on its own. The path from here remains, in dependency
order and each requiring its own separate authorization:

new evidence → **lawful snapshot successor** → endpoint-capable downstream consumption → application.

`XASSET-0021`'s closure matrix is untouched, `APPLICATION_AUTHORIZATION_REGISTRY` remains empty, no
`intelligence/level1_application/` artifact exists or is authorized, and **application authority
remains WITHHELD**.

<!-- ENDPOINT-0001-PROTOCOL-MIRROR-V1
study_id: ENDPOINT-0001
sleeve_count: 4
bound_count: 2
driver_class_count: 6
cell_ceiling: 48
roll_up_unit_count: 8
gate_count: 13
reserve_cells: 0
consequential_parameter_count: 0
stage_2_authorized: false
hash_version: ENDPOINT-0001-PREREG-V1
-->
