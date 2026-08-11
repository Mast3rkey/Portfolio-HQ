---
decision_id: XASSET-0012
date: 2026-08-11
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, REL-0001, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, VALUATION-0006, VALUATION-0007, CONTENDER-0001, CONTENDER-0002, CONTENDER-0003, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: governance/audits/WS0014_LEVEL1_CROSS_ASSET_SYNTHESIS_METHODOLOGY_DESIGN_20260811.md
file: governance/decisions/XASSET-0012-ws0014-level1-cross-asset-synthesis-methodology.md
---

## Context

### Authority for this unit

The human repository principal explicitly authorized exactly **one bounded, design-only governance
filing** defining the methodology for a first, provisional Level 1 cross-asset sleeve-allocation
synthesis. This filing does not populate a sleeve profile, a sleeve relationship, any sleeve
weight, any instrument weight, or any portfolio in/out decision. It is Stage 1 of the four-stage
sequence the supporting artifact §10 defines.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/level-1-cross-asset-synthesis-2m35pg`, working tree clean at session start.
- **`origin/main` fetched and reconciled.** Local branch head and `origin/main` both confirmed
  identical at `23b858441ffa822467e493f3328649d2475445c5` — matching the directive's own stated
  SHA exactly.
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **108 decisions, `issues == ()`**. `XASSET-0001` through `XASSET-0011` all present;
  **`XASSET-0012` independently confirmed the next unused identifier** — zero matches in
  `governance/decisions.yaml`, zero matches via full-repository grep.
- **`PR #299`'s full lifecycle independently re-verified via the GitHub API, not assumed**: head
  `931cfe9941b37b7ec0b7b0dde1dacc3026e0cc68`, base `fea335dca89ff7f2e6006d29d26a613bf1b75c21`
  (`CONTENDER-0003`'s own merge commit). `PR #299` delivers exactly what `CONTENDER-0003` §I
  authorizes: `intelligence/contender_evaluation/{VRT,WMT}.yaml` (sealed), `COHORT_MANIFEST.yaml`,
  `contender_evaluation_validator.py`, and its 153-test suite. Merged via merge commit
  `9975c1d5092eca58bc3416d66beacf029d455dff` (parents `fea335dca89ff7f2e6006d29d26a613bf1b75c21` and
  `931cfe9941b37b7ec0b7b0dde1dacc3026e0cc68`, independently re-confirmed via
  `git log --pretty='%H %P'`).
- **`PR #300`'s full lifecycle independently re-verified via the GitHub API**: a narrow post-merge
  CI repair — one test in `test_contender_evaluation_validator.py` had hard-coded `PR #299`'s own
  pre-merge base SHA as the expected return value of `_resolve_pr_base_sha()`; once `PR #299`
  merged, `HEAD == origin/main` and the resolver correctly returned the new tip instead, exactly the
  lifecycle transition the test's own docstring anticipated but had not yet exercised. Not a
  contender-content regression — every sealed `VRT`/`WMT` record, `contender_evaluation_validator.py`,
  every other repository validator, the decision catalog, and YAML/JSON parsing were all
  independently confirmed clean in that PR's own validation. Fixed by replacing the stale
  hard-coded-SHA assertion with two deterministic synthetic-repository tests. Merged via merge
  commit `23b858441ffa822467e493f3328649d2475445c5` (parents
  `9975c1d5092eca58bc3416d66beacf029d455dff` and `f2b32c1dbc4f160fc7df066ede86828b482367c6`) — this
  repository's current `origin/main` tip. Merge-commit CI independently re-fetched via the GitHub
  API: check run `93659202573`, `status: completed`/`conclusion: success`; a second, direct
  check against the merge commit itself (`GET /repos/.../commits/23b8584.../check-runs`) returned
  the identical single green `test` check run — post-merge CI on `main` is green.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `id:
  WS-0014`): `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`. Thirty-seven
  milestone gates recorded through `contender0003-vrt-wmt-implementation`
  (`status: in_progress`, `pr: null`) — stale as of this session's start, since `PR #299` is, in
  fact, fully merged (see above); this filing synchronizes it (§F). `last_verified_main_sha` reads
  `fea335dca89ff7f2e6006d29d26a613bf1b75c21` — two merges behind the current tip; also synchronized.
- **`WS-0005`'s final state independently re-confirmed**: `status: complete`, `priority: secondary`.
  Zero `priority: primary` workstreams currently exist in the repository (a direct grep of every
  `priority:` field in `operations/WORKSTREAMS.yaml`).
- **`XASSET-0001` (in full) and `XASSET-0005` (in full, decision file and supporting artifact) read
  directly**, not summarized from memory — `XASSET-0001` §E's own two-level architecture
  (Level 1 sleeve allocation; Level 2 instrument allocation) and §J's own dependency-order/batching
  rules (steps 9–10 "sequentially dependent and must not be decided in the same filing"; "every
  completion determination... requires its own separate completion-determination filing") are the
  direct controlling text this filing operationalizes at the design layer. `XASSET-0005`'s
  three-part design-only pattern (functional doctrine + overlap model, one filing, zero content) is
  the direct structural precedent this filing follows for the sleeve-synthesis layer.
- **Every sealed Intelligence layer independently inventoried live** (not assumed): 27 equity
  `classification`/`valuation_archetype`/`valuation_evidence`/`valuation_results` records (the last
  independently re-tallied: 18 `completed` / 9 `partial` / 0 `unable_to_determine`); 4
  `etf_classification` records (SPY, VEA, VWO, GLD); 3 `crypto_classification` records; 4
  `functional_doctrine` records (`CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, `DEBT_REDUCTION` — the
  last independently confirmed to carry `economic_assessment_readiness` forced to
  `assessment_required` on both its `avoided_borrowing_cost_readiness` and
  `survivability_and_buffer_benefit_readiness` sub-fields, per `XASSET-0006`'s own sealed
  implementation); 10 `overlap_model` dimension records (independently re-tallied: 6
  `computed_from_existing_mechanism`, 4 `not_yet_computable_interface_only`); 2 `economic_assessment`
  records (GLD, CASH_LIKE_CAPITAL); 6 `instrument_economic_assessment` records (SPY, VEA, VWO, BTC,
  ETH, SOL); 13 `intelligence/relationships/` records; 2 `contender_evaluation` records (VRT, WMT,
  non-canonical); 84-entry `intelligence/contenders/registry.yaml`. Full detail and directory-level
  reconciliation in the supporting artifact §1.
- **Every relevant validator module's `canonical_record_hash()` function confirmed present** via
  direct grep across eleven modules — the uniform, load-bearing cross-schema structural-reference
  mechanism this filing's design reuses exclusively (supporting artifact §1).
- **`targets.yaml`'s `asset_class` vocabulary independently re-read**: `equity | fund | crypto |
  reserve | cash` — five values, `fund` undifferentiated between SPY/VEA/VWO and GLD, confirming
  that the six-sleeve Level 1 taxonomy this filing designs (§B) is a functional layer on top of
  `asset_class`, not a restatement of it (supporting artifact §1).
- **No existing Level 1, sleeve-allocation, or cross-asset-synthesis methodology found anywhere in
  the repository** — a full-repository grep for "Level 1," "sleeve allocation," and
  "cross-asset synthesis" across `governance/decisions/*.md` returns only filings that *name* Level
  1/synthesis as required future work (`XASSET-0001` itself, and every subsequent `XASSET-####`
  content filing's own restated non-authorization boundary) — none that designs it. This filing is
  the first.

### Disclosed correction, unrelated to this filing's own content, found during validation

A full local repository `pytest` run surfaced one genuine, pre-existing test defect in
`test_overlap_model_validator.py::test_governance_decision_files_untouched` — added in the single
commit that delivered `XASSET-0007`'s own overlap-model content implementation (`PR #292`, merged
2026-08-10), asserting via a live `git status --porcelain -- governance/decisions` check that the
working tree carries zero diff under `governance/decisions/`. That assertion was correct for that
specific PR's own diff (a content-implementation PR should never touch a governance decision file)
but is not, and cannot be, an evergreen repository invariant: it fails for *any* future
governance-authoring session, since authoring a new decision file — the entire purpose of such a
session — necessarily changes `git status` under that directory. This filing's own branch is based
on a commit after `PR #292`'s merge and is, by direct git-log inspection, the first
governance-authoring session to run the full suite since that test was added — the first
opportunity for this always-latent defect to surface. Confirmed via full-repository grep that this
one-off pattern exists nowhere else in the test suite (every other protected-path check is correctly
scoped to specific, genuinely-static paths, e.g. `test_protected_intelligence_records_untouched`'s
own live `git status` check against the specific Intelligence directories that legitimately should
never change without their own dedicated content authorization). Resolved by removing the one
over-broad test function — its real, one-time purpose (confirming `PR #292`'s own diff didn't touch
governance decisions) was already served and closed at that PR's own merge; no ongoing protection is
lost, since the genuinely reusable overlap-model protected-path checks in the same file are
unaffected and still pass. Matches `PR #300`'s own immediately-preceding precedent for exactly this
class of fix (a stale, PR-specific test assertion invalidated by a later, legitimate lifecycle
transition) — not a contender/overlap-model content regression, not a weakening of any real
protection, and not a governance-content change. Exact single file touched by this correction:
`test_overlap_model_validator.py` (one function removed, nine lines).

## Decision

### A. What this filing does — methodology design only

This filing designs, as text only — not an authorization to populate any record, not a sleeve
weight, not an instrument weight, not a portfolio in/out decision — the methodology for a future,
separately authorized first Level 1 cross-asset sleeve-allocation synthesis. Full field-by-field
design in the supporting artifact.

### B. Six-sleeve taxonomy

`equity`, `fund_broad_market` (SPY/VEA/VWO), `fund_gld_defensive` (GLD), `crypto` (BTC/ETH/SOL),
`cash_reserve` (`CASH`+`RESERVE`, treated as one combined family per `XASSET-0008`'s own
principal-directed provenance finding — not reopened here), `debt_reduction` (a margin-policy
lever, no `targets.yaml` row). Full mapping table, per-sleeve governed layers, and required-versus-
optional evidence rules in the supporting artifact §§1–2.

### C. Two record types, both reusing already-accepted repository patterns

**Sleeve profile** (`intelligence/level1_sleeve_synthesis/profiles/<SLEEVE_ID>.yaml`, up to six) —
non-comparative, descriptive: an `evidence_layer_references[]` list (layer-scoped, never
per-instrument, keeping Level 1 genuinely sleeve-scoped rather than blurring into Level 2), an
`economic_role_summary` citing only those references, a mechanically-derived, never
self-declared `evidence_coverage_profile` (closed four values:
`fully_computed`/`substantially_computed_with_disclosed_gaps`/`materially_incomplete`/
`forced_abstention`), and a `functional_role_note` for sleeves carrying a functional-doctrine or
economic-assessment layer. Full field design in supporting artifact §4.

**Sleeve relationship** (`intelligence/level1_sleeve_synthesis/relationships/<A>_<B>.yaml`,
alphabetically ordered, up to fifteen pairs) — reuses `REL-0001`'s exact pairwise convention
(deterministic-alphabetical filename, one-way authority, no stored graph). Carries a closed,
four-value `primary_disposition` (`stronger_priority_support` + required `favored_sleeve_id` /
`role_preserving` / `coexistence_supported` / `unable_to_determine`) and a closed,
zero-to-three-member `secondary_conditions` set (`overlap_or_duplication_disclosed` /
`evidence_partial_present` / `forced_abstention_present`) — orthogonal to the primary value, so a
disclosed gap is never allowed to silently disappear behind a favorable or neutral primary finding.
Full field design, the overlap-citation rule (only `computed_from_existing_mechanism` dimensions
may back an overlap finding), and the reasoning behind the four-value (not five- or six-value)
primary vocabulary in supporting artifact §5.

**Full fifteen-pair coverage is not required of the first implementation** — a future
content-authorization filing may bound the first relationship batch, disclosing exactly what is
and is not covered, matching `CONTENDER-0003`'s own two-of-nineteen bounded-pilot precedent.

### D. Zero numeric fields, no carve-out

Both record types carry no numeric field of any kind — stricter than the ETF framework's own
disclosed-fact `expense_ratio_pct` carve-out, matching `XASSET-0005`/`XASSET-0010`/`CONTENDER-0003`'s
identical posture on every prior comparison-shaped schema in this repository. `favored_sleeve_id`
is a categorical identifier, never a magnitude. Full reasoning in supporting artifact §6.

### E. Boundaries restated as binding design rules, not merely narrative

- **Contender boundary**: `intelligence/contender_evaluation/` (`VRT`, `WMT`) and
  `intelligence/contenders/registry.yaml`'s remaining 82 entries are excluded from the first
  synthesis's governed evidence base — neither record type may cite them as a structural reference.
- **ETF/QQQ boundary**: `fund_broad_market`'s population is exactly {SPY, VEA, VWO}; `QQQ`
  (`primary_disposition: benchmark_or_index` in the registry) is not eligible; no record may assert
  or imply the current ETF set is globally optimal.
- **Level 1 / Level 2 boundary**: neither record type may name an individual equity ticker's,
  fund's, or coin's own weight, target, or size — a dedicated leakage scan enforces this
  mechanically (supporting artifact §9 point 9).
- **Portfolio-selection boundary — narrowest design chosen**: the methodology produces comparative
  evidence findings only. No sleeve-level in/out, eligibility, or "should be part of the portfolio"
  disposition is designed or authorized — an eligibility question is not even live for any of the
  six sleeves today (five already exist as live `targets.yaml` rows; the sixth is an existing
  margin-policy lever, not a candidate for admission). The wider alternative (a provisional
  eligibility/inclusion disposition) was weighed and rejected — see Alternatives Considered.

Full detail, including the forbidden-comparative-investment-superiority-language scan (§8) and the
complete sixteen-point future validator/test specification (§9), in the supporting artifact.

### F. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry gains exactly one additive milestone gate,
`xasset0012-level1-sleeve-synthesis-methodology-design` (`status: in_progress`, `pr: null` — this
filing does not mark its own unmerged work complete), plus one additive Lane M gate,
`contender0003-vrt-wmt-implementation-post-merge-verification`, recording — without editing the
`contender0003-vrt-wmt-implementation` gate's own historical text — that `PR #299` and `PR #300`
are both fully merged, confirmed above, and that post-merge CI on `main` is green. The workstream's
ordinary self-reference fields (`active_branch`, `active_pr`, `last_verified_main_sha`,
`last_verified_date`) are updated to this filing's own live state. No prior gate's own text is
edited. `WS-0014`'s own `status: proposed`/`priority: secondary`/`dependencies: [WS-0005]` are
unedited. `WS-0005` and `WS-0015` are unaffected by this filing.

### G. Explicit non-authorization

This filing authorizes **methodology design text only**. It does not authorize:

- population of any `sleeve_profile` or `sleeve_relationship` record of any kind;
- any actual sleeve weight, sleeve budget, or sleeve allocation percentage;
- any instrument weight or Level 2 sizing decision of any kind;
- any portfolio in/out, eligibility, promotion, or demotion decision for any sleeve or instrument;
- any capital-priority conclusion for `VRT`/`GEV` or `WMT`/`COST` (`CONTENDER-0003`'s own boundary,
  restated, not reopened);
- any broader contender-registry sweep beyond `CONTENDER-0003`'s own two-name pilot;
- any `QQQ`/ETF-scope revisit;
- any discount-rate, cross-coin-correlation, `CASH`/`RESERVE`-consolidation, or `DEBT_REDUCTION`
  economic-assessment research;
- any chart evidence, buy-ladder work, backtesting, monitoring, or sell-discipline rule;
- any allocator, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `margin_state.py`, or `levels.py` change;
- any hardening, expansion, or weakening of any existing repository validator;
- any dashboard change;
- any tier/target/holdings/gate/cap/cluster/order/trade change of any kind.

## Rationale

`XASSET-0001` §E defined the two-level allocation architecture and stated that final allocation
"must compare opportunity cost across all governed sleeves," but deliberately did not design how —
its own Alternatives Considered section explicitly rejected attempting to quantify or pre-size
Level 1 in that same filing, reserving the design to its own separate, later unit. Twelve `WS-0014`
content filings since (`XASSET-0002` through `XASSET-0011`, plus `CONTENDER-0002`/`CONTENDER-0003`)
have now populated every input layer a Level 1 synthesis needs — equity, ETF, crypto, GLD,
cash/reserve, and debt-reduction evidence all exist in governed, sealed form — while the synthesis
methodology that would consume them has remained entirely undesigned. This filing closes that one
specific, now load-bearing gap, following the identical "define, then later authorize implementation"
pattern this repository has used for every prior milestone-scale undertaking (`TIER-0001`/
`TIER-0002` before Milestone 6; `REL-0001` before Milestone 4's content; `XASSET-0005` before the
functional-doctrine and overlap-model content). Designing the schema now, before any content work
begins, is strictly cheaper than discovering a boundary gap after real sleeve-comparison content
already exists on the wrong shape — the same reasoning `TIER-0007`'s own Rationale gave for the
equivalent equity-layer design step.

Reusing `REL-0001`'s pairwise-record convention for sleeve relationships and `CONTENDER-0003`'s
evidence-completeness-not-investment-merit disposition design, rather than inventing new
mechanisms for either, follows the directive's own explicit anti-sidetrack instruction ("does an
accepted existing mechanism already solve this?") and this repository's own repeated preference for
extending an established pattern over creating a parallel one (`PI-0006`'s Theme Intelligence
freeze reused Company Intelligence's own file-per-subject convention; `XASSET-0005`'s
`GLD_DEFENSIVE_ROLE` reused a hash-pin reference rather than duplicating GLD's ETF fields).

Choosing the narrowest portfolio-selection-boundary reading (comparative evidence only, no
eligibility disposition) rather than the wider one follows `XASSET-0001` §M's own explicit
non-authorization of "any sleeve-level or instrument-level sizing of any kind" and the observation
that an eligibility question is not even live for five of the six sleeves — narrowing this
filing's own scope costs nothing today and avoids manufacturing an authorization question a future
reader would otherwise have to untangle from the methodology's own design.

## Alternatives Considered

**Design a single composite sleeve-comparison record (one file, all six sleeves, one shared
`priority_matrix` field) rather than separate profile and relationship record types.** Rejected —
`XASSET-0005`'s own Alternatives Considered section already rejected the analogous single-composite-
record design for the overlap model on identical grounds: a single record with a natural place to
add one more field is a structurally weaker guarantee against an accidental composite score than
several genuinely independent records, each separately sealed and separately abstaining.

**Permit the sleeve-relationship schema to carry a bounded numeric "priority confidence" field (e.g.
low/medium/high mapped to 1–3) rather than zero numeric fields.** Rejected — even a small, bounded,
categorical-looking numeric scale is a hidden score in substance if a future reader can sum or rank
it, exactly the failure mode the directive's own §5 prohibits outright; a closed categorical
vocabulary with no numeric backing (§5.1's four-value `primary_disposition`) achieves the same
communicative purpose without that risk.

**Permit the first Level 1 synthesis to also produce a provisional sleeve eligibility/inclusion
disposition** (e.g., "this sleeve should remain in the portfolio" / "this sleeve's continuation
should be reviewed"), rather than comparative evidence findings alone. Rejected as the wider of two
readings of `XASSET-0001` §E's own scope, and unsupported by need: five of the six sleeves are
already live `targets.yaml` rows with no open eligibility question, and the sixth
(`debt_reduction`) is an existing margin-policy lever rather than an admission candidate — a first
synthesis answering a question that is not actually being asked would manufacture, not resolve,
ambiguity, and would sit closer to the portfolio-selection/adoption question `XASSET-0001` §H
reserves to its own separate, much later, explicitly authorized decision.

**Design Level 2 (instrument-level sizing within a sleeve) alongside Level 1 in this same filing**,
since both are named together in `XASSET-0001` §E. Rejected outright per `XASSET-0001` §J's own
explicit sequencing rule: "sleeve-level versus instrument-level targets... are sequentially
dependent and must not be decided in the same filing, since a Level 2 instrument target inside a
sleeve is only meaningful once that sleeve's own Level 1 budget is set." This filing does not even
design Level 1's *content* (no weight), let alone Level 2's.

**Require full fifteen-pair sleeve-relationship coverage in the first content-authorization filing
this design enables**, rather than permitting a bounded first batch. Rejected — matching
`CONTENDER-0003`'s own explicit two-of-nineteen bounded-pilot discipline and `OPS-0008`'s Research
Wave Protocol reasoning (prove the mechanism narrowly before scaling), forcing full coverage before
any implementation has proven the schema against real evidence would repeat the exact anti-pattern
`OPS-0008` was created to prevent.

## Consequences

**Changes as a direct result of this decision**: the existence of one retained sleeve taxonomy (six
`sleeve_id` values, mapped to `targets.yaml`'s `asset_class` and to every relevant governed
Intelligence layer), one retained sleeve-profile schema design, one retained sleeve-relationship
schema design (reusing `REL-0001`'s pairwise convention), one closed four-value primary-disposition
vocabulary and one closed three-member secondary-conditions vocabulary, one zero-numeric-field
posture with no carve-out, one overlap-citation rule restricting evidence to
`computed_from_existing_mechanism` dimensions, and one sixteen-point future validator/test
specification — all recorded in the supporting artifact for a future, separately authorized Stage 2
content-authorization filing to draw on; five rejected alternatives recorded for the same future
reference; confirmation, via two additive `operations/WORKSTREAMS.yaml` gates, that `CONTENDER-0003`'s
own authorized implementation (`PR #299`, corrected by `PR #300`) is fully merged and post-merge CI
on `main` is green.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin
behavior; the 1.8x leverage cap or 30% margin-buffer floor; any Company, Theme, relationship,
classification, valuation-archetype, valuation-evidence, valuation-result, ETF-classification,
crypto-classification, functional-doctrine, overlap-model, economic-assessment,
instrument-economic-assessment, or contender-evaluation record's content; any current cash balance,
reserve level, GLD holding, or margin-debt figure; `WS-0005`'s completed, `status: complete` state;
`WS-0014`'s own `status: proposed`/`priority: secondary` (this filing adds two additive gates, it
does not begin execution or change the workstream's own status/priority); or any brokerage, trading,
or order-related capability. Completing this unit does not itself authorize populating any sleeve
profile or sleeve relationship record, any Level 2 instrument-level design or sizing, cross-asset
opportunity-cost synthesis beyond this bounded methodology, or the final independent audit
(`XASSET-0001` §I item 14) — each requires its own separate, explicit, future principal
authorization, per `XASSET-0001` §J's own dependency-ordered roadmap and `OPS-0006` §16.4's standing
rule that the register never originates authority.
