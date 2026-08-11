# WS-0014 Level 1 Sleeve Policy-Adoption Methodology — Design (Stage 4 of `XASSET-0012` §10)

**Date**: 2026-08-11
**Governing decision**: `governance/decisions/XASSET-0014-ws0014-level1-policy-adoption-methodology.md`
**Status**: Design only. No policy-adoption record is populated by this artifact or its governing
decision. No sleeve receives an actual role, eligibility, or sizing-readiness disposition. No
numeric weight of any kind is created, implied, or authorized.

**Bounded correction (same PR, same day), independent exact-head review `pullrequestreview-4909703610`
(anchored to the original head `e246ea77ae6292d5a1dcc4ce652885e93ec153c7`), 0 BLOCKING / 1 MAJOR / 0
MINOR, CHANGES REQUIRED — resolved by this correction**: the three-axis mechanism was internally
inconsistent in two connected ways, both concretely provable against the real sealed data. **Part
A**: `fund_broad_market` could not reach Axis A's `function_confirmed_distinct` value under the
original two-basis evidentiary rule (its only sealed relationship record resolves
`stronger_evidence_maturity`, mechanically barred from supplying Axis A grounds; the doctrine-citation
path was restricted, by the original §14, to `debt_reduction` alone) — directly contradicting the
original §10's own asserted outcome for that sleeve. **Part B**: Axis C penalized a sealed-but-
unresolved relationship pair while treating an unresearched (deferred) pair as silently clean,
inverting the design's own "no absence of evidence may silently become favorable" principle.
**Resolved without weakening the `stronger_evidence_maturity` non-influence rule anywhere**: a new
third Axis A evidentiary basis (§3.2, structural `targets.yaml`-destination-category membership,
categorical and sleeve-level, never an instrument weight, never a relationship record, never an
evidence-maturity value), a generalized (no longer `debt_reduction`-restricted) doctrine-citation
basis (§3.2), a six-sleeve Axis A reachability audit (§3.3), a corrected §10 outcome claim, a new
per-sleeve relationship-coverage-ledger mechanism distinguishing `sealed_determined`/
`sealed_unresolved`/`deferred_disclosed` (§5.1), a new eleventh sizing gate condition (§15), thirteen
internal cross-reference corrections found during the same consistency pass, and a new
axis-interaction adversarial-case table (§22). Full correction narrative in each affected section
below, each individually marked. No policy-adoption record, Axis A/B/C disposition, Stage 4b, or
Stage 4c work is populated or authorized by this correction — the three-axis architecture itself is
unchanged; only its evidentiary-basis and coverage-completeness rules are extended.

## 0. Purpose and where this sits in the sequence

`XASSET-0012` §10 defined four stages for the Level 1 cross-asset sleeve-synthesis work:

1. Stage 1 — synthesis methodology design (`XASSET-0012`, merged).
2. Stage 2 — synthesis content authorization (`XASSET-0013`, merged).
3. Stage 3 — synthesis implementation/population (`PR #303`, merged: six sealed `sleeve_profile`
   records, seven sealed `sleeve_relationship` records).
4. Stage 4 — **"future policy adoption / portfolio selection, if separately authorized."**
   `XASSET-0012` §10 states explicitly: "A sleeve profile or relationship record, however complete,
   creates no allocation, weight, eligibility, or trade authority on its own."

This artifact is the **first sub-unit of Stage 4** — a bounded, design-only methodology, exactly
mirroring how `XASSET-0012` itself was Stage 1 of the synthesis sequence: define the schema and
mechanism now, before any record is drafted, so that a future, separately authorized Stage 4b
(content authorization, naming exactly which sleeves a Stage 4c implementation may populate) and
Stage 4c (implementation) can proceed without inventing boundary rules under evidentiary pressure.
This artifact performs no Stage 4b or Stage 4c work.

## 1. Live synthesis truth this design is built from

Independently re-derived this session (2026-08-11), not assumed from any prior summary — see the
governing decision's own Preflight for the full reconciliation. Six sealed `sleeve_profile` records:

| `sleeve_id` | `evidence_coverage_profile` | `abstention_index` entries |
|---|---|---|
| `equity` | `substantially_computed_with_disclosed_gaps` | 5 |
| `fund_broad_market` | `substantially_computed_with_disclosed_gaps` | 2 |
| `fund_gld_defensive` | `substantially_computed_with_disclosed_gaps` | 3 |
| `crypto` | `substantially_computed_with_disclosed_gaps` | 2 |
| `cash_reserve` | `substantially_computed_with_disclosed_gaps` | 4 |
| `debt_reduction` | `forced_abstention` | 3 |

Seven sealed `sleeve_relationship` records:

| Pair | `primary_disposition` | `favored_sleeve_id` |
|---|---|---|
| `cash_reserve` ↔ `debt_reduction` | `unable_to_determine` | — |
| `cash_reserve` ↔ `equity` | `role_preserving` | — |
| `crypto` ↔ `equity` | `stronger_evidence_maturity` | `equity` |
| `crypto` ↔ `fund_gld_defensive` | `coexistence_supported` | — |
| `debt_reduction` ↔ `equity` | `role_preserving` | — |
| `equity` ↔ `fund_broad_market` | `stronger_evidence_maturity` | `equity` |
| `equity` ↔ `fund_gld_defensive` | `role_preserving` | — |

Every one of the above is the sole governed input this design's mechanism may ever consume for a
future Stage 4b/4c record — no Company Intelligence field, no contender-registry entry, no
allocator/margin output beyond what `functional_doctrine/DEBT_REDUCTION.yaml` and `CLAUDE.md`'s
Portfolio Doctrine already cite, may be introduced as a new evidentiary input at Stage 4. Stage 4
is strictly downstream of Stage 1–3's own closed vocabulary — it may only ever **derive** a policy
disposition from what Stage 1–3 already found; it may never manufacture a finding Stage 1–3's own
vocabulary structurally cannot produce (see §3.1).

## 2. Why three separated axes, not one collapsed verdict

A single verdict field (e.g., one closed `sleeve_policy_status` covering "should this sleeve get
capital") would conflate three genuinely independent questions that this repository's own
Milestone 7/8 precedent (`TIER-0007`'s `primary_disposition` + `target_context_comparison` as two
separate fields; `TIER-0009`'s eight-area `primary_status` + `secondary_conditions` as two
independent axes) already establishes must stay structurally separate:

- **Does this sleeve represent a real, distinct portfolio function at all** — a qualitative,
  evidence-grounded question about *concept*, answerable today for every sleeve except possibly one
  still-immature case, independent of how well-quantified that sleeve's own economic assessment is.
- **Is the sleeve's own governed evidence base mature enough to even be considered as a
  target-proposal candidate** — a mechanical, evidence-floor question about *data sufficiency*,
  answerable by machine from `evidence_coverage_profile` alone, with zero judgment involved.
- **Is the sleeve, and the network of relationships bearing on it, mature enough right now to
  proceed to an actual numeric percentage** — a process-completeness question about *readiness*,
  which depends on both prior axes plus whether every relationship pair materially touching this
  sleeve has itself been resolved (not `unable_to_determine`) and disclosed (not silently dropped).

Collapsing these into one field would force exactly the failure mode `debt_reduction` demonstrates
live today (§7): a sleeve can be role-legitimate (its function is real and doctrine-documented) while
being simultaneously evidence-ineligible (its own economic-assessment layer is forced-abstained) —
a single verdict field could only represent one of those two true facts, silently discarding the
other. Three independent axes let both facts remain visible at once, exactly the "no absence of
evidence may silently become neutral, favorable, or unfavorable" discipline `XASSET-0012` §5.2
already established for `secondary_conditions`, generalized here to a three-axis structure instead
of a one-status-plus-flags structure, because unlike `XASSET-0012`'s comparative-evidence findings,
Stage 4's three questions are not merely "primary plus caveats" — each is independently reachable
and independently blocking.

## 3. Axis A — Portfolio Function Status ("role adoption")

**Field**: `portfolio_function_status`, closed, exactly one of three values:

1. **`function_confirmed_distinct`** — this sleeve's own governed evidence establishes that the
   sleeve serves a portfolio function not already fully served by another sleeve, and that function
   should remain part of the six-sleeve taxonomy going forward, eligible for later sizing
   consideration. Requires at least one of three lawful evidentiary bases, defined exhaustively in
   §3.2 below — **never** an evidence-maturity finding (§6).
2. **`function_status_unresolved`** — none of §3.2's three bases is available: e.g., every
   relationship record naming this sleeve carries `stronger_evidence_maturity` against it with no
   offsetting finding anywhere, no doctrine citation exists, and the sleeve carries no live
   `targets.yaml` destination-category membership either. This is **not** a demotion and must never
   be represented, in any free text, as one — it means "not yet resolved," nothing more.
3. **`unable_to_determine`** — every governed input this axis depends on is itself abstained or
   forced-abstained (a live state for no sleeve today — see §3.3's reachability audit). Requires a
   non-empty `abstention_reason`.

### 3.1 Deliberately three values, not four — no "function not confirmed" value exists yet

An earlier draft of this design considered a fourth value representing a genuine finding that a
sleeve's function is fully redundant with another's (a true "role rejected" state). **Rejected, for
a structural reason, not a policy preference**: `XASSET-0012` §5.1's own closed four-value
`primary_disposition` vocabulary (`stronger_evidence_maturity` / `role_preserving` /
`coexistence_supported` / `unable_to_determine`) contains **no value that asserts redundancy** —
`stronger_evidence_maturity` is explicitly, mechanically restricted to an evidence-completeness
finding only (§6 below), never an investment-merit or "should be sized larger" claim, and none of
the other three values asserts anything close to "sleeve X's function is fully subsumed by sleeve
Y's." Since Stage 4 may only ever *derive* a disposition from Stage 1–3's own sealed evidence
(§1), and no Stage 1–3 evidence token today, or reachable under the current Stage 1–3 methodology,
can support a redundancy finding, adding a fourth Stage 4 value that no live or future-reachable
input could ever populate would be exactly the "provisional guardrail no evidence supports"
anti-pattern `NUM-0001` names for numeric parameters, generalized here to categorical schema design.
**If a future relationship-methodology amendment (its own separate `XASSET-####` filing) adds a
redundancy-capable value to Stage 1–3's own `primary_disposition` vocabulary, only then would a
fourth Axis A value become well-founded** — recorded here as an explicit, disclosed future
contingency, not designed now.

### 3.2 Three lawful Axis A evidentiary bases, defined exhaustively

**Bounded correction, independent exact-head review `pullrequestreview-4909703610` (anchored to the
original head `e246ea77ae6292d5a1dcc4ce652885e93ec153c7`), MAJOR-1, resolved by this subsection**: the
original design named only two evidentiary bases (relationship-record finding; a `CLAUDE.md`
Portfolio Doctrine citation restricted, by §14's own field-design comment, to `debt_reduction`
alone). The review independently confirmed, against the real sealed data, that `fund_broad_market`'s
only sealed relationship record (`equity_fund_broad_market.yaml`) resolves `stronger_evidence_
maturity` — mechanically barred from supplying Axis A grounds (§6) — and that no other sleeve
currently has a sealed `role_preserving`/`coexistence_supported` finding naming it, so under the
original two-basis rule `fund_broad_market` could never reach `function_confirmed_distinct`,
directly contradicting the outcome the original §10 asserted for it. **Resolved by defining a third,
structurally independent basis (Basis 3) rather than weakening the `stronger_evidence_maturity`
non-influence rule** — the correction the review itself recommended as sound. All three bases:

- **Basis 1 — relationship-record finding (unchanged).** At least one sealed `sleeve_relationship`
  record naming this sleeve resolves `role_preserving` or `coexistence_supported` (§7). Never
  `stronger_evidence_maturity`, by construction (§6).
- **Basis 2 — `CLAUDE.md` doctrine citation (generalized, no longer sleeve-restricted).** A directly
  cited, verbatim-quoted passage from `CLAUDE.md`'s own Portfolio Doctrine or Decisions Log
  establishing this specific sleeve's distinct functional purpose, independent of any relationship
  record. **Available to any of the six sleeves for which such a passage genuinely exists** — the
  original restriction to `debt_reduction` alone was an unprincipled one-off with no doctrinal
  grounding of its own; the same evidentiary logic ("a real, quoted, governed text passage
  independently establishes a distinct function") applies identically regardless of which sleeve it
  concerns. This does **not** lower the bar: a future Stage 4c drafting session may cite this basis
  only where a genuine, directly-quotable passage exists — never an inferred, paraphrased, or
  fabricated one, and never a passage merely restating the sleeve's own name or its `targets.yaml`
  membership (that is Basis 3's job, not Basis 2's). Illustratively (not adopted — §3.3), real
  candidate passages exist today for `debt_reduction` (the 1.8x leverage cap / 30% buffer floor /
  forced-de-lever margin doctrine) and `fund_gld_defensive` (`CLAUDE.md`'s own "GLD does the ballast
  job bonds would" framing, already independently cited by `XASSET-0013` §D); no equally clean,
  dedicated passage is asserted here for `equity`, `fund_broad_market`, or `cash_reserve` — this
  design manufactures no doctrine text that does not already exist.
- **Basis 3 — structural sleeve-definition basis (new).** A sleeve may independently satisfy Axis
  A's evidentiary requirement by citing `XASSET-0012` §2's own accepted, closed sleeve-taxonomy
  table showing that the sleeve maps to at least one currently live `targets.yaml` destination row
  under its own `asset_class` scope. This is a **categorical, sleeve-level, mechanically-checkable
  structural fact** — never an individual instrument's own weight, target percentage, or size (which
  would risk exactly the Level 1/Level 2 leakage §12 exists to prevent). A future Stage 4c drafting
  session citing Basis 3 may name that the sleeve's `asset_class` category is populated in
  `targets.yaml` today; it may **never** cite, quote, or rely on any individual destination row's own
  `target_pct` value, weight, or rank within that category. **Basis 3 is available to `equity`,
  `fund_broad_market`, `fund_gld_defensive`, `crypto`, and `cash_reserve`** — the five sleeves with a
  live `targets.yaml` destination row per `XASSET-0012` §2's own table — and **is not available to
  `debt_reduction`**, which `XASSET-0012` §2 itself records as having no `targets.yaml` row at all
  ("none (margin lever)"); `debt_reduction` continues to rely on Basis 1/Basis 2 exactly as §7.1
  already illustrates, unaffected by this addition.

  **Structurally independent of evidence maturity, by design — verified, not merely asserted.** Basis
  3 depends on exactly two facts: (a) the sleeve's own `asset_class` scope per `XASSET-0012` §2's
  fixed, accepted table (a governance-document fact, never live-recomputed from any sealed record),
  and (b) live confirmation that `targets.yaml` currently carries at least one destination row in
  that scope (a binary existence check, not a completeness or quality measure). Basis 3 reads **no**
  `sleeve_relationship` record of any kind (so it is trivially immune to §6's counterfactual-masking
  test — masking every `favored_sleeve_id` field changes nothing Basis 3 depends on) and **no**
  `evidence_coverage_profile` *value* (only that field's mere existence on a sealed profile, which
  every one of the six profiles already independently guarantees) — so Basis 3 can never be
  conflated with, or read as a proxy for, Axis B's own evidence-maturity-derived eligibility
  determination. A future validator must enforce this mechanically: a Basis 3 citation is rejected
  outright if it references any `evidence_coverage_profile` value, any `favored_sleeve_id`, or any
  individual destination row's own `target_pct` (§21).

### 3.3 Six-sleeve Axis A reachability audit — illustrative only, no disposition adopted

A methodology-reachability check only, per the directive's own explicit instruction — **no Axis A
value is adopted for any sleeve by this filing or by this audit**. For each of the six sleeves, the
lawful evidentiary basis (or bases) currently available under §3.2, traced directly against the
sealed data:

| `sleeve_id` | Basis 1 available? | Basis 2 available? | Basis 3 available? |
|---|---|---|---|
| `equity` | Yes — 3 sealed `role_preserving` findings (`cash_reserve_equity`, `debt_reduction_equity`, `equity_fund_gld_defensive`) | Not asserted here (none needed) | Yes — live `targets.yaml` `equity` rows |
| `fund_broad_market` | **No** — its one sealed relationship (`equity_fund_broad_market`) resolves `stronger_evidence_maturity`, barred by construction | Not asserted here (no dedicated passage identified) | **Yes** — live `targets.yaml` `fund` rows (SPY/VEA/VWO) |
| `fund_gld_defensive` | Yes — 2 sealed findings (`crypto_fund_gld_defensive`: `coexistence_supported`; `equity_fund_gld_defensive`: `role_preserving`) | Yes — the "ballast" passage (illustrative) | Yes — live `targets.yaml` `fund` row (GLD) |
| `crypto` | Yes — 1 sealed finding (`crypto_fund_gld_defensive`: `coexistence_supported`) | Not asserted here (a conviction-sizing passage may exist; not relied upon since Basis 1 already suffices) | Yes — live `targets.yaml` `crypto` rows |
| `cash_reserve` | Yes — 1 sealed finding (`cash_reserve_equity`: `role_preserving`) | Not asserted here (none needed) | Yes — live `targets.yaml` `cash`/`reserve` rows |
| `debt_reduction` | Yes — 1 sealed finding (`debt_reduction_equity`: `role_preserving`) | Yes — the leverage-cap/buffer-floor passage (illustrative, §7.1) | **No** — no `targets.yaml` row exists for this sleeve |

**Before this correction, `fund_broad_market` was the only one of the six sleeves with zero lawful
Axis A basis available under the design's own stated rules** — the exact defect the review's
Finding MAJOR-1 identified. **After this correction, every one of the six sleeves has at least one
lawful basis available**, closing the gap without weakening `stronger_evidence_maturity`'s
non-influence rule anywhere (Basis 3 never reads it; Basis 1/Basis 2 already excluded it). This
table is reachability analysis only — it does not itself populate `portfolio_function_status` for
any sleeve, and a future Stage 4c drafting session must still independently verify, cite, and seal
the actual evidentiary basis it relies on for each sleeve, per the field schema in §14.

## 4. Axis B — Capital Eligibility

**Field**: `capital_eligibility_status`, closed, exactly one of two values, **mechanically derived,
never authored**:

1. **`eligible_for_target_consideration`** — the sleeve's own sealed profile carries
   `evidence_coverage_profile` equal to `fully_computed` or
   `substantially_computed_with_disclosed_gaps`.
2. **`not_yet_eligible`** — the sleeve's own sealed profile carries `evidence_coverage_profile`
   equal to `forced_abstention` or `materially_incomplete`.

**No `unable_to_determine` value exists on this axis**, unlike Axis A and Axis C — a deliberate
asymmetry, not an oversight. `evidence_coverage_profile` is itself already a mechanically-derived,
always-populated, closed four-value field on every sealed profile (`XASSET-0012` §4.2) — it has no
abstention state of its own, because a profile that could not be evaluated at all would fail to seal
in the first place. A field whose entire content is a pure function of an already-fully-determined
input needs no independent abstention path; adding one here would just relocate, not resolve,
whatever uncertainty the underlying `evidence_coverage_profile` field already discloses. This makes
Axis B the one purely mechanical axis in the design — a future validator computes it directly from
the cited profile's own live state, with **zero drafting-session discretion**, matching the
"mechanically derived, never self-declared" discipline `XASSET-0012` §4.2 already established for
its own input field.

## 5. Axis C — Sizing Readiness

**Field**: `sizing_readiness_status`, closed, exactly one of three values, **now incorporating
relationship-coverage completeness (§5.1) as well as relationship disposition**:

1. **`sizing_ready`** — `portfolio_function_status == function_confirmed_distinct` **and**
   `capital_eligibility_status == eligible_for_target_consideration` **and** no relationship record
   naming this sleeve resolves `unable_to_determine` **and** every one of this sleeve's required
   relationship pairs (§5.1) is in the `sealed_determined` coverage state — zero `deferred_disclosed`
   pairs remaining.
2. **`sizing_conditionally_ready`** — both prior axes clear (`function_confirmed_distinct` and
   `eligible_for_target_consideration`), no relationship record naming this sleeve resolves
   `unable_to_determine`, but at least one of: a sealed relationship record naming this sleeve
   carries `evidence_partial_present`, `forced_abstention_present`, or
   `overlap_or_duplication_disclosed`; **or** at least one of this sleeve's required relationship
   pairs (§5.1) is in the `deferred_disclosed` coverage state — numeric sizing work could reasonably
   begin, but only with the specific disclosed caveat(s) and every deferred pair carried forward
   explicitly, never silently dropped or silently treated as clean.
3. **`sizing_blocked`** — either prior axis fails to clear (`portfolio_function_status !=
   function_confirmed_distinct`, or `capital_eligibility_status == not_yet_eligible`), **or** any
   relationship record naming this sleeve resolves `unable_to_determine` (a `sealed_unresolved`
   coverage state, §5.1 — strictly more severe than a `deferred_disclosed` pair, never treated as
   equal to or better than one).

Every `sizing_blocked` or `sizing_conditionally_ready` disposition **requires** a non-empty
`blocking_evidence[]` list — one entry per contributing reason (a failed axis, a specific
`unable_to_determine` relationship, a specific secondary condition, a specific deferred pair) — never
a bare status with no supporting trail. This directly answers the directive's own instruction ("state
exactly what must be true before... numeric target percentages" — §15 below) at the per-sleeve level:
a reader can trace, sleeve by sleeve, exactly which fact is missing.

### 5.1 Relationship coverage completeness — required, deferred, and missing distinguished

**Bounded correction, review `pullrequestreview-4909703610`, MAJOR-1 (second half), resolved by this
subsection**: the original §5 rule inspected only relationship records that *exist* — it had no
mechanism distinguishing a sealed-but-unresolved pair (which actively blocks, per §5 point 3) from a
pair that was simply never sealed at all (which, under the original rule, blocked nothing). The
review correctly identified this as inverting `XASSET-0012` §5.2's own stated principle, restated in
this design's §2 ("no absence of evidence may silently become neutral, favorable, or unfavorable"):
an honestly-disclosed `unable_to_determine` finding was treated strictly worse than a pair that was
simply never researched. **Resolved** by defining, for every sleeve, a closed, exhaustive
**relationship coverage ledger** covering all five of its theoretically possible pairs (against each
of the other five sleeves) — never the hypothetical fifteen `C(6,2)` pairs at large, and never
inventing a future pair beyond what `XASSET-0012`/`XASSET-0013` already authorized or explicitly
deferred:

- **`sealed_determined`** — the pair is one of the seven `XASSET-0013` §C sealed records, and its own
  `primary_disposition != unable_to_determine`.
- **`sealed_unresolved`** — the pair is one of the seven sealed records, and its own
  `primary_disposition == unable_to_determine` (today: `cash_reserve` ↔ `debt_reduction` only).
- **`deferred_disclosed`** — the pair is **not** one of the seven sealed records, but is one of the
  eight pairs `XASSET-0013` §E explicitly named and classified by deferral class (never a pair
  outside that named, closed set of eight — a pair absent from both the sealed seven and the
  disclosed eight would be a hard schema failure for the future validator, not a fourth coverage
  state, since no such pair exists under the current, fully-accounted-for Stage 2/3 population:
  7 sealed + 8 disclosed-deferred = 15, the complete `C(6,2)` set, with zero gaps).

**Per-sleeve coverage, traced against the real sealed data (illustrative only, no disposition
adopted)**: `equity` — 5 of 5 pairs `sealed_determined` (the batch's own "hub," per `XASSET-0013`
§D), zero deferred. `fund_broad_market` — 1 of 5 `sealed_determined` (against `equity`), 4 of 5
`deferred_disclosed` (`XASSET-0013` §E class 1, against `fund_gld_defensive`/`crypto`/
`cash_reserve`/`debt_reduction`). `fund_gld_defensive` — 2 of 5 `sealed_determined` (against
`equity`, `crypto`), 3 of 5 `deferred_disclosed` (§E classes 1–2, against `fund_broad_market`/
`cash_reserve`/`debt_reduction`). `crypto` — 2 of 5 `sealed_determined` (against `equity`,
`fund_gld_defensive`), 3 of 5 `deferred_disclosed` (§E classes 1/3, against `fund_broad_market`/
`cash_reserve`/`debt_reduction`). `cash_reserve` — 1 of 5 `sealed_determined` (against `equity`),
1 of 5 `sealed_unresolved` (against `debt_reduction`), 3 of 5 `deferred_disclosed` (§E classes
1–3, against `fund_broad_market`/`fund_gld_defensive`/`crypto`). `debt_reduction` — 1 of 5
`sealed_determined` (against `equity`), 1 of 5 `sealed_unresolved` (against `cash_reserve`), 3 of 5
`deferred_disclosed` (§E classes 1–3, against `fund_broad_market`/`fund_gld_defensive`/`crypto`).

**Direct consequence, disclosed honestly, not smoothed over**: under this corrected rule, `equity` is
the only one of the six sleeves with zero `deferred_disclosed` pairs today — every other sleeve, even
where Axis A and Axis B both independently clear, is mechanically capped at
`sizing_conditionally_ready` at best (never `sizing_ready`) until a future relationship batch closes
its own remaining deferred pairs. This is not a defect in the mechanism; it is the honest, structural
reflection of `XASSET-0013`'s own explicitly bounded seven-of-fifteen first coverage batch, and it is
exactly the kind of disclosure this repository's own "no absence of evidence may silently become
favorable" principle exists to force into the open rather than leave implicit. A future relationship
batch that seals one of the eight currently-deferred pairs recomputes the affected sleeves'
coverage ledgers and Axis C values from scratch, per the same live-derivation discipline the rest of
this design already applies.

## 6. `stronger_evidence_maturity` — mechanically prohibited from driving any axis

**The boundary, restated as an operative design rule, not narrative**: `stronger_evidence_maturity`
is an evidence-completeness finding only (`XASSET-0012` §5.1 point 1, restated, not reopened). No
field on any Axis A/B/C computation may read `favored_sleeve_id`, and no drafting session may cite a
sleeve's status as `favored_sleeve_id` in a `stronger_evidence_maturity` relationship as grounds for
any of:

- automatically larger allocation (no numeric field exists at Stage 4 at all — §13);
- automatic Axis A inclusion (`function_confirmed_distinct` requires one of §3.2's three lawful
  bases — `stronger_evidence_maturity` supplies none of them, by construction, including the new
  Basis 3, which reads no relationship record of any kind);
- automatic preference in Axis C (`sizing_ready` requires *all four* underlying conditions
  independently — Axis A, Axis B, zero `sealed_unresolved` pairs, and zero `deferred_disclosed`
  pairs, per §5/§5.1 — none of which reference `favored_sleeve_id`).

**A lower-maturity sleeve may still reach `function_confirmed_distinct`** — `debt_reduction`
(§7.1) and `fund_broad_market` (§7.2, only reachable via the new Basis 3 after this correction)
both illustrate this live. **A higher-maturity sleeve may still fail Axis C** — a future
re-population where `equity`'s own relationship coverage develops a fresh `unable_to_determine`
finding would force `equity` itself to `sizing_blocked` regardless of its own `stronger_evidence_
maturity` standing against `crypto`/`fund_broad_market` today.

**Mechanical enforcement, required of the future validator** (folded into §21 item 5): a
counterfactual-masking test — recompute every sleeve's three axis values with every
`stronger_evidence_maturity` relationship record's `favored_sleeve_id` field masked (set to a
sentinel) and confirm **zero** axis value differs from the unmasked computation. This is a
structural non-influence proof, not a drafting convention a reviewer must remember to check by eye.
**Defensive strengthening, per the review's own non-blocking NOTE**: the future validator must also
prove that the mere *presence* of a `stronger_evidence_maturity` disposition — independent of its
`favored_sleeve_id` value — cannot influence any axis, by additionally recomputing every sleeve's
axis values with every `stronger_evidence_maturity` relationship record's `primary_disposition`
itself swapped for a different allowed non-role disposition (e.g. `coexistence_supported`) and
confirming the *other* sleeve's own axis values (the one not directly named by that swapped
disposition's own new evidentiary content) do not change for reasons attributable to the swap alone
— no field in the current schema provides such a hook, so this is a defensive regression guard, not
a fix to a live gap.

## 7. `role_preserving` / `coexistence_supported` — what they authorize and what they do not

These two values **may**:

- supply the evidentiary basis for Axis A's `function_confirmed_distinct` value (§3);
- be cited, jointly with other findings, in a `sizing_conditionally_ready` disposition's
  `blocking_evidence[]`/caveat trail when they co-occur with a secondary condition.

They **may not**:

- guarantee a positive numeric target — no numeric field exists anywhere in this schema (§13);
- determine target size in any way — a `role_preserving` finding says nothing about *how much*
  capital either sleeve should receive, only that neither's evidence base displaces the other's;
- prevent future exclusion if later evidence changes — every Axis A/B/C value is a **live-derived**
  computation over currently-sealed evidence, never a permanent lock; a future re-population (§14)
  that seals a materially different relationship record recomputes every dependent axis from
  scratch, per this repository's own "never silently rewrite, supersede instead" convention applied
  to derived state rather than authored prose;
- imply equal weighting between the two sleeves in any relationship — `role_preserving` and
  `coexistence_supported` are purely qualitative; neither carries, or may be read as carrying, any
  size-comparison information of any kind.

### 7.1 Worked illustration — `debt_reduction`, mechanism trace only, no disposition adopted

`debt_reduction`'s live sealed evidence, traced through the mechanism above (**illustrative only —
this filing performs no Stage 4b/4c population; no value below is adopted by this filing**):

- `debt_reduction_equity.yaml` resolves `role_preserving` — an independent, sealed relationship
  finding (Basis 1, §3.2), entirely separate from `debt_reduction`'s own
  `functional_doctrine/DEBT_REDUCTION.yaml` economic-assessment layer, and independently sufficient
  on its own to satisfy Axis A's evidentiary bar. `CLAUDE.md`'s own Portfolio Doctrine explicitly
  naming margin paydown as a governed capital use (the 1.8x leverage cap, the 30% buffer floor, the
  forced-de-lever guardrail) also supplies a valid, independent Basis 2 citation for
  `debt_reduction` — **available, but not load-bearing for it specifically**, since Basis 1 already
  suffices on its own (corrected per the review's own non-blocking NOTE — the original text's claim
  that `debt_reduction` is "the only sleeve today for which this... path matters" was imprecise:
  `debt_reduction` clears via Basis 1 alone, and Basis 2 is now, after this correction, a generally
  available basis for any sleeve with real, quotable doctrine text, not a `debt_reduction`-specific
  exception). A future Stage 4c implementation would need to independently confirm and cite whichever
  basis it actually relies on, but the mechanism does not structurally block `debt_reduction` from
  `function_confirmed_distinct` merely because its own economic assessment is thin.
- `debt_reduction.yaml`'s own `evidence_coverage_profile` is `forced_abstention` — Axis B's
  mechanical rule (§4) forces `capital_eligibility_status: not_yet_eligible`, with **zero override
  path**, regardless of Axis A's outcome.
- Because Axis B cannot clear, Axis C (§5) is mechanically forced to `sizing_blocked` regardless of
  Axis A — this is exactly the case the directive's own "do not force a capital-policy answer merely
  because the schema requires one" instruction anticipates, and exactly why three independent axes
  (not one collapsed verdict) are required: `debt_reduction` can be simultaneously
  role-legitimate **and** sizing-blocked, both facts staying visible.
- `debt_reduction` very likely requires a separate, future, dedicated evidence unit — specifically,
  closing `DEBT_REDUCTION.yaml`'s own forced `assessment_required` sub-fields
  (`avoided_borrowing_cost_readiness`, `survivability_and_buffer_benefit_readiness`, per
  `XASSET-0006`'s own sealed implementation) — before Axis B could ever clear. This filing does not
  perform, schedule, or authorize that research; it is disclosed here as a foreseeable future
  dependency the mechanism itself surfaces, matching the same "disclosed, not assumed" discipline
  `TIER-0009` §K already applied when it disclosed `target_and_range`/`maximum_position_size` as
  forced `valuation_required` for every equity.

### 7.2 Worked illustration — `fund_broad_market`, mechanism trace only, no disposition adopted

**Added by this bounded correction.** `fund_broad_market`'s live sealed evidence, traced through the
corrected mechanism (**illustrative only — no value below is adopted by this filing**), directly
demonstrating why Finding MAJOR-1's fix (§3.2's Basis 3) was required:

- `equity_fund_broad_market.yaml`, `fund_broad_market`'s **only** sealed relationship record, resolves
  `stronger_evidence_maturity` (favoring `equity`) — mechanically excluded from supplying Axis A
  grounds (§6). No sealed relationship record anywhere names `fund_broad_market` with a
  `role_preserving`/`coexistence_supported` finding — **Basis 1 is unavailable** for this sleeve
  today, a genuinely different situation from every other of the six sleeves (§3.3).
- No dedicated, directly-quotable `CLAUDE.md` doctrine passage specific to the ETF sleeve's own
  distinct function (as opposed to GLD's or debt-reduction's own dedicated passages) is identified or
  asserted by this design — **Basis 2 is not relied upon** for `fund_broad_market`, consistent with
  §3.2's own refusal to manufacture doctrine text that does not exist.
- `fund_broad_market`'s own live `targets.yaml` `asset_class: fund` scope (SPY, VEA, VWO), per
  `XASSET-0012` §2's own accepted mapping table, is independently confirmed live-populated —
  **Basis 3 is available**, on a purely categorical, sleeve-level basis, independent of any
  relationship record's disposition and independent of `evidence_coverage_profile`'s own value. A
  future Stage 4c implementation citing Basis 3 for `fund_broad_market` would name only the
  category's live existence, never SPY's, VEA's, or VWO's own individual `target_pct` value.
- With Basis 3 available, the mechanism no longer structurally forecloses
  `function_confirmed_distinct` for `fund_broad_market` — but this filing does not itself determine
  whether a future Stage 4c drafting session would actually reach that value, only that the
  evidentiary path to do so now exists and is mechanically sound, closing the gap the review's Finding
  MAJOR-1 identified.
- Independently of Axis A, `fund_broad_market`'s own sealed profile carries
  `evidence_coverage_profile: substantially_computed_with_disclosed_gaps` — Axis B (§4) would resolve
  `eligible_for_target_consideration`.
- On Axis C (§5/§5.1), `fund_broad_market` carries 4 of its 5 possible relationship pairs in the
  `deferred_disclosed` coverage state (`XASSET-0013` §E class 1) and 1 `sealed_determined` (against
  `equity`) — even with Axis A and Axis B both clearing, Axis C is mechanically capped at
  `sizing_conditionally_ready` at best, never `sizing_ready`, until a future relationship batch closes
  its remaining deferred pairs. Both facts — a now-reachable Axis A and a structurally capped Axis
  C — stay independently visible, exactly the discipline three separate axes exist to preserve.

## 8. Abstention handling — no answer is forced merely because the schema requires one

- **`unable_to_determine` relationship results** (live example: `cash_reserve` ↔ `debt_reduction`)
  propagate as a required `blocking_evidence[]` entry on **both** named sleeves' Axis C computation,
  independent of what either sleeve's own Axis A/B otherwise resolve to — an unresolved relationship
  is never silently absorbed into a favorable or neutral reading for either party.
- **`forced_abstention` profile state** (live example: `debt_reduction`) mechanically forces Axis B
  to `not_yet_eligible` for that sleeve alone (§4) — it does not, by itself, touch Axis A or any
  other sleeve's own axes.
- **`evidence_partial_present`** on a relationship record naming this sleeve contributes toward, but
  does not by itself force, a `sizing_conditionally_ready` rather than `sizing_ready` reading — it is
  one of the three secondary conditions Axis C's second value checks for (§5).
- **`forced_abstention_present`** on a relationship record naming this sleeve likewise contributes to
  the `sizing_conditionally_ready`/`sizing_blocked` boundary — note that `forced_abstention_present`
  as a *relationship-record* secondary flag (which can arise even from a `role_preserving`/
  `coexistence_supported` primary disposition, e.g. `debt_reduction_equity.yaml` carries it despite
  resolving `role_preserving`) is distinct from a sleeve's own *profile-level*
  `evidence_coverage_profile: forced_abstention` (Axis B) — the two must never be conflated into one
  check; a future validator computes them from different source fields entirely.
- **`unresolved primary evidence`** — any field this design's mechanism depends on that is itself
  unpopulated or unreadable (as opposed to properly abstained) is a hard schema failure for the
  future validator, never silently treated as a passing case.

No Axis A/B/C value may ever be set merely to avoid an empty field — every abstaining or blocked
value requires its own non-empty reason trail (`abstention_reason` for Axis A `unable_to_determine`;
`blocking_evidence[]` for Axis C `sizing_blocked`/`sizing_conditionally_ready`).

## 9. `cash_reserve` — operational combination without resolving the underlying question

Stage 4 represents `cash_reserve` operationally as **one** combined Axis A/B/C determination,
reusing — not reopening — the already-established `CASH`+`RESERVE` combined-family treatment
(`XASSET-0008` §N, `CASH_LIKE_CAPITAL.yaml`'s own sealed record). This does **not** resolve the
underlying, still-open `CASH`/`RESERVE` consolidation question. The future Stage 4c record for
`cash_reserve` must:

- carry a mandatory rationale sentence restating, verbatim in substance, that `CASH` and `RESERVE`
  remain an unresolved, undifferentiated family and that this Stage 4 record's combined treatment
  does not itself settle that question — reusing the exact non-settlement framing
  `CASH_LIKE_CAPITAL.yaml` already uses;
- be mechanically barred, by the same dedicated distinction-language scan `economic_assessment_
  validator.py`'s own `_contains_cash_reserve_distinction_claim()`-shaped check already implements
  for the economic-assessment layer, from ever asserting that `CASH` and `RESERVE` individually
  warrant different Axis A/B/C treatment (§21 item 12).

## 10. `fund_broad_market` / `equity` overlap — disclosed coordination flag, not a subtraction

**Bounded correction, review `pullrequestreview-4909703610`, MAJOR-1, resolved**: the original text
below asserted that overlap disclosure "may never... force `fund_broad_market`'s Axis A below
`function_confirmed_distinct`," justified by citing SPY's own `targets.yaml` weight (an
*individual-instrument* fact, per `XASSET-0013` §D) — a fact the review correctly found was neither
one of §3's then-stated evidentiary bases nor a citable source under §14's own field-design
restriction, and which, worse, was never actually reachable for `fund_broad_market` under the
original two-basis rule at all (§3.3). The specific instrument-weight justification is **withdrawn**
and replaced below with the correct, sleeve-level Basis 3 (§3.2) — the outcome sentence is corrected,
not merely re-justified, since there was no confirmed floor to protect until Basis 3 existed.

`equity_fund_broad_market.yaml`'s own `stronger_evidence_maturity` (favoring `equity`) **must not**
be read as evidence that SPY/VEA/VWO are unnecessary — restating §6's boundary at this specific,
concrete pair. The same relationship record's `overlap_or_duplication_disclosed` secondary condition
(citing the `etf_direct_equity_duplication` overlap-model dimension) may inform Axis C only as a
**disclosed coordination flag** — a `blocking_evidence[]`/caveat entry noting that this sleeve's
eventual Level 1 numeric sizing (a future, separate stage entirely) should be considered jointly
with `equity`'s own sizing rather than independently, given the disclosed overlap. It may **never**:

- silently net or subtract capital from `fund_broad_market`'s own eventual sizing;
- force `fund_broad_market`'s Axis A below whatever value its own lawful evidentiary basis (or bases,
  per §3.2) actually supports — the overlap disclosure is a Axis C caveat only and carries zero Axis
  A authority of any kind. `fund_broad_market`'s own live `targets.yaml asset_class: fund` category
  membership (Basis 3, §3.2/§7.2) — a categorical, sleeve-level structural fact, never an individual
  instrument's own weight — is the evidentiary path available to it, independent of and unaffected by
  the overlap disclosure;
- imply any specific netting formula, ratio, or adjustment of any kind — the flag is descriptive
  only; any actual joint-sizing treatment is Level 1 numeric-sizing content, a wholly separate,
  unauthorized future stage (§15).

## 11. `crypto` / `fund_gld_defensive` — preserved, not extended

The sealed `crypto_fund_gld_defensive.yaml` finding (`coexistence_supported`), its own disclosed
BTC-specific inflation-narrative basis (`GLD.yaml`/`BTC.yaml` both `historically_mixed_or_
inconsistent`; `ETH.yaml`/`SOL.yaml` both diverge at `historically_weakly_associated`), and the
sleeve-wide, sub-field-level forced abstention on `crypto`'s own `cross_coin_correlation_status`
(`not_yet_measured` on all three sealed coins) are preserved by this design exactly as Stage 3 sealed
them — this filing performs no re-derivation, no re-weighting, and infers no crypto target or GLD
target of any kind. `coexistence_supported` may inform Axis A for both sleeves (§3) and may
contribute a caveat to Axis C (§5), identically to `role_preserving`'s own treatment (§7) — it
carries the same "no size, no guarantee, no permanence" restrictions.

## 12. Level 1 / Level 2 boundary

Stage 4 is sleeve-level only, exactly as Stage 1–3 already were. No Stage 4 record of any kind may
name, weight, or size an individual equity ticker, ETF, or coin. The Level 1/Level 2 leakage scan
`XASSET-0012` §9 item 9 already built for Stage 1–3 is reused, unmodified, against Stage 4's own
free-text and structural fields (§21 item 9 below) — this design invents no new leakage-check logic,
it extends an existing one to a new schema.

## 13. Zero numeric fields — no carve-out, restated

Stage 4 carries **no numeric field of any kind** — no weight, no percentage, no score, no rank, no
confidence number, no range, matching `XASSET-0012` §6's identical posture and every prior
comparison-shaped schema in this repository (`XASSET-0005`, `XASSET-0010`, `CONTENDER-0003`). This
is deliberately the strictest possible reading: even a categorical "how close to sizing-ready" scale
mapped to 1–3 would be a hidden score in substance, the same reasoning `XASSET-0012`'s own
Alternatives Considered section already applied and rejected for its own schema.

## 14. Exact future Stage 4c deliverable

**One record per sleeve** (up to six), `intelligence/level1_sleeve_synthesis/policy_adoption/
<SLEEVE_ID>.yaml`, plus one `COHORT_MANIFEST.yaml` — a new, third sub-namespace under
`intelligence/level1_sleeve_synthesis/`, parallel to (never merged with) `profiles/` and
`relationships/`, matching this repository's own settled "different schema shape, different,
cleanly separated directory" convention (`functional_doctrine/` vs. `overlap_model/` vs.
`economic_assessment/`, all closely related, all separately directoried; `XASSET-0012`'s own
`profiles/`/`relationships/` split). **A single whole-portfolio decision file was considered and
rejected** — identical reasoning to `XASSET-0005`'s own rejected single-composite-record
alternative: a single record with a natural place to add "just one more field" is a structurally
weaker guarantee against an accidental composite score than six genuinely independent records, each
separately sealed and separately abstaining.

Field design for the future Stage 4c record:

```
sleeve_id                       # closed, one of the six SS2 values
schema_version
profile_reference                # one hash pin into this sleeve's own sealed sleeve_profile record
relationship_references[]        # hash pins into every sealed sleeve_relationship record naming
                                  #   this sleeve (0-5 today, depending on sleeve)
portfolio_function_status        # closed, Axis A -- SS3
function_rationale               # free text; may cite only: (a) the profile/relationship
                                  #   references above; (b) a direct, verbatim-quoted CLAUDE.md
                                  #   Portfolio Doctrine/Decisions Log citation, available to any
                                  #   sleeve where a genuine passage exists (Basis 2, SS3.2 --
                                  #   corrected by this filing's bounded correction; no longer
                                  #   debt_reduction-only); or (c) this sleeve's own live
                                  #   targets.yaml destination-category membership per XASSET-0012
                                  #   SS2's fixed table (Basis 3, SS3.2, new) -- never an
                                  #   individual instrument's own weight, target, or rank -- no
                                  #   fabricated evidence
abstention_index[]               # non-empty abstention_reason required wherever Axis A ==
                                  #   unable_to_determine
capital_eligibility_status       # closed, Axis B -- SS4, mechanically re-derived at validation
                                  #   time from the cited profile's own live evidence_coverage_
                                  #   profile, never self-declared
sizing_readiness_status          # closed, Axis C -- SS5/SS5.1
blocking_evidence[]              # non-empty wherever Axis C != sizing_ready -- one entry per
                                  #   contributing reason (failed axis / named unresolved
                                  #   relationship / named deferred pair / named secondary
                                  #   condition)
unresolved_relationships[]       # every relationship_references[] entry whose own primary_
                                  #   disposition == unable_to_determine, named explicitly
relationship_coverage_ledger[]   # new, this filing's bounded correction -- exactly five entries
                                  #   (this sleeve's five possible pairs against every other
                                  #   sleeve), each {other_sleeve_id, coverage_state:
                                  #   sealed_determined | sealed_unresolved | deferred_disclosed,
                                  #   reference} -- SS5.1; mechanically enumerated and
                                  #   cross-checked, never self-declared or partially populated
overlap_coordination_notes[]     # optional; disclosed-caveat-only entries per SS10, never a
                                  #   sizing formula
cash_reserve_consolidation_note  # required, cash_reserve record only -- SS9
record_status                    # draft | sealed
sealed_at / governing_decisions / drafting_session_or_shard_id / content_sha256 /
  cohort_manifest_entry
```

`profile_reference` and every `relationship_references[]` entry are live-recomputed via
`level1_sleeve_synthesis_validator.py`'s own `canonical_record_hash()` at validation time, never
trusted from a stored value — the identical discipline every prior structural reference in this
repository already follows.

## 15. Gate to numeric Level 1 sizing — what must be true before a single percentage exists

**Bounded correction, review `pullrequestreview-4909703610`, adopting its own suggested condition,
resolved**: extended from ten to eleven conditions, adding relationship-coverage-ledger completeness
(new condition 11) — the review's own recommended fix for the second half of Finding MAJOR-1, closing
the same gap §5.1's new coverage-ledger mechanism closes at the per-sleeve level, restated here as a
gate-level, whole-population completeness requirement.

Numeric Level 1 sleeve-level sizing (`XASSET-0001` §J step 9, "sleeve-level candidate targets") may
not be authorized to begin until **all** of the following hold, none of them satisfied by this
design filing:

1. This Stage 4 methodology design (this filing) is itself merged, independently reviewed, and
   principal-accepted.
2. A future, separate Stage 4b content-authorization filing has named the exact sleeve population a
   Stage 4c implementation may populate (mirroring `XASSET-0013`'s own role for Stage 2) — matching
   the same design-then-authorize-content sequence throughout this repository.
3. A future, separate Stage 4c implementation has populated a Stage 4 record for **every** sleeve
   the Stage 4b filing authorizes — no sleeve silently omitted, matching `XASSET-0013` §B's own
   "never omit... never force a stronger completeness value than the evidence supports" discipline,
   restated one layer up.
4. Every sleeve's Axis A/B/C disposition is explicit — no sleeve left with an unpopulated or
   defaulted axis value.
5. Every `sizing_blocked` or `sizing_conditionally_ready` sleeve's `blocking_evidence[]` is fully
   populated and disclosed — no hidden blocker, no silently-dropped caveat.
6. `debt_reduction`'s own disposition — whatever a future Stage 4c implementation actually finds it
   to be — is explicit and disclosed, not assumed from this filing's own illustrative trace (§7.1).
   If `debt_reduction` reaches `sizing_blocked`, a future numeric-sizing filing must explicitly
   disclose that it is proceeding without a `debt_reduction` numeric candidate (or with an explicitly
   flagged placeholder/deferred-sizing note) rather than silently dropping the sleeve from the
   taxonomy entirely.
7. `cash_reserve`'s Stage 4 record carries its required consolidation-non-settlement note (§9) —
   numeric sizing for `cash_reserve` may proceed as one combined figure without that being read as
   resolving the underlying `CASH`/`RESERVE` question.
8. The counterfactual-masking non-influence proof (§6) passes for every sleeve — no axis value is
   traceable to a `stronger_evidence_maturity` finding alone.
9. A dedicated future Stage 4 validator module (§21) exists, is independently reviewed, and passes —
   closed schema, mechanical Axis B re-derivation, the non-influence proof, every forbidden-language
   scan (§21), and manifest reconciliation.
10. No sleeve's `sizing_readiness_status` was upgraded by anything other than the mechanical rule in
    §5/§5.1 — a dedicated audit trail (not a drafting-session assertion) proving every `sizing_ready`
    disposition independently satisfies all four of §5's own stated conditions (Axis A, Axis B, zero
    `sealed_unresolved` pairs, zero `deferred_disclosed` pairs).
11. **New, this filing's bounded correction.** For every sleeve, its own `relationship_coverage_
    ledger[]` (§5.1/§14) is fully populated across all five of its possible relationship pairs, with
    zero unaccounted-for pairs and zero pairs silently treated as clean — each pair correctly
    classified `sealed_determined`, `sealed_unresolved`, or `deferred_disclosed` by live
    cross-reference against the seven sealed `sleeve_relationship` records and `XASSET-0013` §E's own
    eight explicitly-named deferred pairs. No sleeve reaches `sizing_ready` with any
    `deferred_disclosed` pair still outstanding — a `deferred_disclosed` pair may support at most
    `sizing_conditionally_ready`, per §5's own mechanical rule.

**Even once all eleven conditions hold, this design filing does not itself authorize numeric Level 1
sizing** — it defines what must be true before a future, wholly separate, explicitly authorized
governance filing (its own `XASSET-####` identifier, its own independent-review lifecycle) may begin
that work. Satisfying this gate is necessary, never sufficient, for that future authorization.

## 16. Allocation-check boundary

A real, deployment-relevant allocation check is **not** authorized merely by this design filing, by
a future Stage 4b content-authorization filing, or by a future Stage 4c implementation. It remains
downstream of, in strict order: actual Stage 4 adoption (Stage 4b + Stage 4c, both separately
authorized and completed); Level 1 numeric sleeve sizing (§15, its own separate future
authorization); Level 2 instrument selection/sizing within each sleeve's approved budget; required
risk/overlap validation and unlevered-portfolio validation (§17); with margin/leverage research
following only after (§19). `OPS-0007` §5's own narrow,
scenario-only, cash-only, zero-margin allocation-check display bridge is a **separate, already-bounded
authorization** that this filing neither reactivates, expands, nor references as a shortcut around
any of the above — it remains exactly as bounded as `OPS-0007` left it.

## 17. Risk/backtest sequencing — using the repository's own already-recorded order

`operations/WORKSTREAMS.yaml`'s own `WS-0014` `roadmap_preservation` field already records a
sequencing principle for this exact question, unedited by this filing, restated here rather than
invented: "finish missing evidence (1)-(3) → broaden contender competition (4) → cross-asset
synthesis (6) → **provisional sleeve/instrument sizing (7)-(8)** → **descriptive risk analysis and
targeted backtests (5),(12)** → chart-informed deployment work (9) → buy ladders (11) → **unlevered
portfolio testing (13)** → revise policy/sizing if evidence requires → margin/leverage research and
backtesting (14) → monitoring/sell discipline (15) → final integration/audit (16)."

This repository's own already-recorded order places targeted backtests **after** provisional sizing,
using them to **challenge and refine** a provisional Level 1/Level 2 sizing rather than as a
universal precondition to any sizing at all — the directive's own instruction not to invent a
stricter sequencing than repository doctrine states is honored by reusing this order exactly, not by
tightening it. Concretely, for Stage 4 and beyond:

- **Before** Level 1 sizing: this Stage 4 gate (§15) must be satisfied in full.
- **After** provisional Level 1/Level 2 sizing exists: descriptive risk analysis and targeted,
  pre-registered backtests (roadmap items 5/12) may challenge or refine it — this is expected,
  recorded doctrine, not a defect in proceeding to provisional sizing first.
- **Before** any decision-ready, final target: unlevered-portfolio testing (item 13) must occur and
  be judged sound, **then** margin/leverage research (item 14, reusing `MARGIN-0005`'s own existing
  charter rather than opening a competing one), **then** monitoring/sell discipline (item 15),
  **then** final integration and independent audit (item 16) — in that order, matching the roadmap
  field's own text exactly.

## 18. Chart/deployment boundary

Restates, does not reopen, `XASSET-0001` §G and `TIER-0003`: fundamentals, classification, and
cross-asset policy (including this Stage 4 mechanism) determine what deserves capital and its
approved limits. Chart evidence remains strictly downstream — it may later inform timing, staging,
cadence, and technical-risk review **within already-approved policy**, once Level 1 and Level 2
targets exist, but it never retroactively determines sleeve membership (Axis A), evidence
eligibility (Axis B), sizing readiness (Axis C), or any fundamental target policy of any kind.

## 19. Margin/debt boundary

Restates the repository's own sequencing: the unlevered portfolio must be evidenced and judged sound
**first** (roadmap item 13); margin/leverage research and stress testing follow **after** (item 14,
reusing `MARGIN-0005`'s already-accepted charter); deployment policy follows that. `debt_reduction`
as a Level 1 capital use **is** allowed to be considered under this Stage 4 mechanism (§7.1
illustrates how) — that is a functional-role question, answerable independent of margin *deployment*
policy, which remains fully downstream and is neither performed, scheduled, nor authorized by
anything in this design. The 1.8x leverage cap and the 30% margin-buffer floor remain unchanged,
provisional, binding guardrails throughout (`NUM-0001`), untouched by this filing.

## 20. Contender/QQQ boundary — no reopening, forward-compatible only

This design operates exclusively on the six-sleeve, seven-relationship population Stage 3 already
sealed. It does not reopen `VRT`/`WMT` (`CONTENDER-0003`), the remaining 82 contender-registry
entries, `QQQ`, or any broader ETF search — restating, not narrowing or widening,
`XASSET-0012` §7's own contender/ETF/QQQ boundary at the Stage 4 layer. The future Stage 4c record
schema (§14) includes no field naming a contender or a ticker outside the sealed six-sleeve
population; a dedicated scan (§21 item 16) enforces this mechanically.

**Forward-compatibility, not expansion**: `XASSET-0012` §7 already states that "a future, separately
authorized synthesis *refresh* may incorporate contender-driven evidence once a capital-priority
conclusion for a specific contender actually exists." Should such a refresh occur, a Stage 4 record
whose underlying `profile_reference` or `relationship_references[]` hash no longer matches the
current sealed state of its cited record becomes **stale by construction** — the future validator's
own live hash re-computation (§14) already catches this as a hard failure, requiring the affected
Stage 4 record to be superseded, never silently left inconsistent. No new field, trigger mechanism,
or re-synthesis authority is created by this filing to handle that case — the existing hash-staleness
detection already suffices, and any actual refresh remains its own future, separately authorized
unit.

## 21. Future validator/test specification

A future, separately authorized Stage 4c implementation must build one dedicated validator module
(or extend `level1_sleeve_synthesis_validator.py` with a clearly separated Stage 4 section — the
implementing session's own choice to justify, mirroring `XASSET-0006` §A point 3's and `XASSET-0013`
§K's identical deferral), with zero import coupling to `allocate.py`/`margin_state.py` in either
direction, at minimum:

1. Closed schema at every nesting level (envelope, `abstention_index` entry, `blocking_evidence`
   entry, `unresolved_relationships` entry, `relationship_coverage_ledger` entry,
   `overlap_coordination_notes` entry, manifest row) — extra-key rejection, not merely missing-key
   checks.
2. Exactly six `sleeve_id` values, closed, matching `XASSET-0012` §2 exactly; at most one Stage 4c
   record per sleeve.
3. Live, independent recomputation of `profile_reference` and every `relationship_references[]`
   hash, never trusting a stored value — a dedicated stale-hash rejection test for each reference
   type, including the staleness-on-refresh case (§20).
4. **Axis B mechanical re-derivation** — a dedicated test proving a record claiming
   `eligible_for_target_consideration` while its cited profile's own live `evidence_coverage_profile`
   shows `forced_abstention`/`materially_incomplete` is rejected, and the converse.
5. **The `stronger_evidence_maturity` counterfactual-masking non-influence proof** (§6) — a dedicated
   test suite running the full six-sleeve axis computation twice (once with every
   `stronger_evidence_maturity` relationship record's `favored_sleeve_id` masked, once unmasked) and
   asserting byte-identical axis outputs both times.
6. **Axis C mechanical consistency** — a dedicated test proving a record claiming `sizing_ready`
   while `portfolio_function_status != function_confirmed_distinct`, or
   `capital_eligibility_status != eligible_for_target_consideration`, or
   `unresolved_relationships[]` is non-empty, or any `relationship_coverage_ledger[]` entry is
   `deferred_disclosed`, is rejected; and that every `sizing_blocked`/`sizing_conditionally_ready`
   record carries a non-empty `blocking_evidence[]`.
7. Zero numeric fields anywhere — a bare-digit/percent/ratio scan **plus** a written-out
   magnitude-comparison-word scan (times/twice/doubled/tripled/-fold/halved), matching
   `XASSET-0012` §9 item 7 exactly.
8. Zero score/rank/composite/weight/priority-index-shaped key name anywhere.
9. Zero `target_pct`/`max_position_size`/tier/gate/cluster/holding-shaped key or value, and zero
   individual equity/fund/coin ticker named as bearing its own weight or size (Level 1/Level 2
   leakage, §12) — structural reference hash pins and identity lists are exempt, matching
   `XASSET-0012` §4.1.1's own precedent, since naming which sealed records a Stage 4 record cites is
   not itself a weight or size claim.
10. Zero word-boundary-matched directive/trading language (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/
    `wait`/`stage`).
11. Zero chart-domain terminology (the same ~16–17-term list every prior `TIER-####`/`XASSET-####`/
    `VALUATION-####` schema already uses).
12. **The `CASH`/`RESERVE`-distinction-language scan** (§9), reusing
    `economic_assessment_validator.py`'s own existing check design rather than inventing a new one.
13. **Stage 4's own bounded-conclusion scan — materially different from Stage 1–3's `XASSET-0012`
    §8.1 blanket eligibility-language ban.** Stage 1–3's schema is barred entirely from any
    portfolio-membership language, because Stage 1–3 does not decide eligibility at all. Stage 4's
    schema is **explicitly designed** to represent a bounded, closed-vocabulary role/eligibility/
    readiness judgment — that distinction is exactly why `XASSET-0012` §10 required Stage 4 to be its
    own, separately authorized stage rather than folded into Stage 1–3. What remains barred, even in
    Stage 4 free text (`function_rationale`, `blocking_evidence[]` entries,
    `overlap_coordination_notes[]`): (a) any numeric magnitude, percentage, or weight of any kind
    attached to a role/eligibility/readiness finding; (b) any trade/order/execution directive
    language, or any claim that a Stage 4 finding alone triggers deployment, an allocation check, or
    Level 2 instrument selection; (c) free text asserting a conclusion stronger than the record's own
    populated closed-vocabulary fields support (no claim of a fourth Axis A value, no permanent/
    irrevocable framing contradicting §7's "never a permanent lock" rule); (d) individual-instrument
    eligibility or target-weight leakage (Level 2 boundary, item 9).
14. **The comparative-investment-superiority scan**, reusing `XASSET-0012` §8's mechanism unmodified,
    applied to Stage 4's own free-text fields.
15. **Adversarial test coverage** for every scan in items 7–14, explicitly probing: word ordering;
    negation; punctuation variants; conjunction-joined phrases; active/passive voice; euphemistic
    inclusion/exclusion paraphrase (the exact vulnerability class `XASSET-0013` §H's own mandatory
    probe already found seven live gaps in for Stage 1–3's analogous scan — a future Stage 4c
    implementation must run the identical probe discipline against its own scans, before push, and
    disclose the result whether clean or not); hidden-sizing phrasing; score/rank language; and
    mandatory false-positive guards proving legitimate descriptive evidence/process/policy language
    still validates cleanly.
16. Zero citation of `intelligence/contender_evaluation/`, `intelligence/contenders/`, or any
    ticker/fund/coin symbol outside the sealed six-sleeve population, and zero `QQQ` reference of any
    kind (§20).
17. A dedicated protected-path/byte-identity test proving every one of the thirteen input layers
    `XASSET-0012` §1 inventories, plus the six `sleeve_profile` and seven `sleeve_relationship`
    records themselves, remains untouched before and after the future Stage 4c implementation —
    matching this repository's established `test_protected_intelligence_records_untouched`
    precedent, repaired (not deleted) per `XASSET-0012`'s own Correction History lesson.
18. Manifest bidirectional reconciliation (hash, duplicate, missing, extra, orphan) for the new
    `policy_adoption/` subdirectory's own `COHORT_MANIFEST.yaml`.
19. Non-cascading abstention discipline — an abstention on one sleeve's axis never forces or implies
    a value on another sleeve's axis, and an abstention on one axis of a given sleeve never cascades
    into a forced value on that same sleeve's other axes beyond the mechanical rules §3–§5 already
    specify explicitly.
20. A dedicated test proving this filing's own eventual future decision file and this artifact remain
    free to use the phrase "policy adoption"/"eligible"/"role" in governance prose without
    self-triggering item 13's scan — the same governance-text-versus-populated-record distinction
    `XASSET-0012` §8.1's own false-positive guard already draws for its analogous boundary.

**Added by this bounded correction (review `pullrequestreview-4909703610`, resolving Finding
MAJOR-1):**

21. **Basis 3 mechanical check** (§3.2) — a dedicated test proving a `function_rationale` citing the
    structural sleeve-definition basis is rejected unless the sleeve's own `targets.yaml
    asset_class` scope, per `XASSET-0012` §2's fixed table, is independently, live-confirmed to
    carry at least one current destination row — never self-declared; a dedicated test proving a
    Basis 3 citation referencing any `evidence_coverage_profile` value, any `favored_sleeve_id`, or
    any individual destination row's own `target_pct` is rejected outright (Basis 3 must never be
    usable as an evidence-maturity or per-instrument-weight proxy); a dedicated test proving Basis 3
    is unavailable for `debt_reduction` (no `targets.yaml` row exists per `XASSET-0012` §2).
22. **Generalized Basis 2 structural requirement** (§3.2) — a dedicated test proving a doctrine
    citation is structurally required to be non-empty and distinct from a generic or templated
    placeholder string for whichever of the six sleeves it is claimed on (no longer
    `debt_reduction`-restricted); the future validator cannot semantically verify `CLAUDE.md` prose
    content, so the genuine correctness burden for a Basis 2 citation rests on Stage 4c's own
    required independent-review process, matching how this repository's existing validators already
    treat every other free-text citation field.
23. **Relationship-coverage-ledger completeness** (§5.1) — a dedicated test proving every sleeve's
    `relationship_coverage_ledger[]` enumerates exactly its own five possible pairs (never fewer,
    never a duplicate, never a sixth); a dedicated test proving each entry's `coverage_state` is
    correctly, live-derived by cross-reference against the seven sealed `sleeve_relationship`
    records and `XASSET-0013` §E's own eight named, closed deferred-pair set (no future pair may be
    silently added to "deferred" without its own governance citation — an unrecognized pair, present
    in neither the sealed seven nor the disclosed eight, is a hard schema failure, not a fourth
    coverage state); a dedicated test proving a sleeve with any `deferred_disclosed` entry cannot
    reach `sizing_ready` (only `sizing_conditionally_ready` at best); a dedicated test proving a
    sleeve with zero `deferred_disclosed` and zero `sealed_unresolved` entries and both prior axes
    clear reaches `sizing_ready` (the `equity` case, illustrative per §5.1).
24. **The `stronger_evidence_maturity` presence-independent non-influence regression guard** (§6) —
    a defensive test, beyond the primary `favored_sleeve_id`-masking proof (item 5), proving that
    swapping a `stronger_evidence_maturity` relationship record's own `primary_disposition` for a
    different allowed non-role disposition does not change any *other* sleeve's axis values for
    reasons attributable to the swap alone — a regression guard against a future schema change
    accidentally introducing a presence-based influence hook, not a fix to any hook that exists
    today.

## 22. Axis-interaction adversarial cases — reachability audit, illustrative only

**Added by this bounded correction, per the directive's own explicit adversarial-case requirement.**
No disposition is adopted for any sleeve by this section — every result below is a methodology
reachability determination only, most already independently verified by the review itself (its own
§24), reproduced here as the design document's own explicit, auditable record so a future reader
never has to re-derive it from the review comment alone.

| Case | Scenario | Axis A | Axis B | Axis C |
|---|---|---|---|---|
| A | Role distinct (Basis 1/2/3) + evidence partial + all required pairs `sealed_determined`, no `unable_to_determine` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` (evidence-partial caveat only) |
| B | Role unresolved (no basis available) + evidence complete | `function_status_unresolved` | (irrelevant — Axis A gate fails) | `sizing_blocked` |
| C | Role distinct + capital forced-abstained | `function_confirmed_distinct` | `not_yet_eligible` | `sizing_blocked` — matches `debt_reduction` exactly (§7.1) |
| D | Role distinct + evidence complete + one required pair `sealed_unresolved` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_blocked` — matches `cash_reserve`/`debt_reduction`'s own live pair exactly (§8) |
| E | `stronger_evidence_maturity` only, no offsetting Basis 1/2/3 evidence | `function_status_unresolved` | (irrelevant) | `sizing_blocked` — was `fund_broad_market`'s exact pre-correction situation; Basis 3 now supplies an independent path (§7.2) |
| F | Role-preserving + overlapping/duplicative sleeve | Axis A clears via Basis 1/3 independent of the overlap | (unaffected) | overlap surfaces only as an Axis C caveat, never a subtraction (§10) |
| G | Role unresolved + zero evidence gaps otherwise | `function_status_unresolved` | `eligible_for_target_consideration` | `sizing_blocked` via the Axis A gate alone — `blocking_evidence` cites only the Axis A gap |
| H | A required pair is `deferred_disclosed` (not in the sealed seven, but named in `XASSET-0013` §E's own eight) | (independent of this case) | (independent of this case) | `sizing_conditionally_ready` at best, never `sizing_ready` — the pair is disclosed, not silently treated as clean (§5.1) |

No case above produces an ambiguous or underived result under the corrected methodology — every
outcome is a deterministic function of the mechanical rules in §3.2/§4/§5/§5.1/§6. Case E is the
concrete, real-data instance of Finding MAJOR-1 this correction resolves (§7.2); Case H is the
concrete, real-data instance of Finding MAJOR-1's second half (every non-`equity` sleeve today, per
§5.1's own per-sleeve table).

## 23. Sequence — Stage 4 itself is not collapsed

1. **Stage 4a — this design** (`XASSET-0014`). Methodology only.
2. **Stage 4b — future content authorization.** A future, separate, bounded filing must name the
   exact sleeve population (up to six) a Stage 4c implementation may populate, before any record is
   drafted — matching `XASSET-0012`→`XASSET-0013`'s own sequence one layer down.
3. **Stage 4c — future implementation/population.** Builds the validator and populates exactly the
   records Stage 4b authorized.
4. **Numeric Level 1 sizing (`XASSET-0001` §J step 9) — its own separate, later, wholly distinct
   future authorization**, gated on §15's eleven conditions, not a Stage 4 sub-step at all.

No sub-stage above may be collapsed into another by this design or by any future filing acting under
it.
