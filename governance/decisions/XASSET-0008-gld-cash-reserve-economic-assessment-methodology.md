---
decision_id: XASSET-0008
date: 2026-08-09
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, REL-0001, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, VALUATION-0001, VALUATION-0002, VALUATION-0004]
supporting_artifact: governance/audits/WS0014_GLD_CASH_RESERVE_ECONOMIC_ASSESSMENT_METHODOLOGY_DESIGN_20260809.md
file: governance/decisions/XASSET-0008-gld-cash-reserve-economic-assessment-methodology.md
---

## Context

### Authority for this unit

`XASSET-0005` §5 restates a seven-step whole-portfolio sequence and names step 2 — "perform
asset-appropriate valuation/economic assessment" — as "future, separate, undesigned." Every sealed
functional-doctrine record (`CASH.yaml`, `RESERVE.yaml`, `GLD_DEFENSIVE_ROLE.yaml`) carries the identical
forced value `economic_assessment_readiness.status: assessment_required`, stating plainly that no
governed methodology exists to compare that capital-use type's opportunity cost against anything else.
This filing is the first step toward closing that gap for exactly three of the four functional-doctrine
capital-use types — it designs a closed, categorical, single-instrument economic-assessment methodology
for `GLD`, `CASH`, and `RESERVE`. It does not populate any record and does not itself resolve any sealed
record's forced `economic_assessment_readiness` value.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0008-economic-assessment-b5078s`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c` — `XASSET-0007`'s own merge commit (PR #286).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #286`'s full lifecycle independently re-verified via the GitHub API, not assumed**: accepted head
  `cf478cdbcf10fd930d337e74ada9f72a42e09a92` (base `main` @ `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e`);
  single independent exact-head review (`pullrequestreview-4891559425`, **APPROVED FOR PRINCIPAL
  EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE — the reviewer independently
  reconciled the exact 6-file changed inventory, the exact ten-dimension overlap-model population
  against `XASSET-0005` §6.1's own table, the 4/6 `interface_placeholder`/`mechanical_rollup`-or-
  `narrative_evidence` split, the bounded four-location factual correction, the one-direction
  evidence-flow boundary, the deliberate non-loosening of the forced value despite `GLD_DEFENSIVE_
  ROLE.yaml` now existing, `PR #285`'s own full chain, the `WS-0014` Lane M synchronization, the
  decision-catalog delta (101, `issues == ()`), and all 12 repository validators plus the full test
  suite (4042 passed, 0 failed) — all independently reproduced, not read off the PR body); principal
  acceptance (`issuecomment-5231939730`, accepted head `cf478cdbcf10fd930d337e74ada9f72a42e09a92`,
  explicitly re-confirming head/base/`mergeable_state: clean`/6 changed files/1 commit/zero competing
  PRs/clean working tree immediately before posting); merge (merge commit
  `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`, parents `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e` and
  `cf478cdbcf10fd930d337e74ada9f72a42e09a92`, both independently re-confirmed via `git log --pretty`);
  merge-commit CI independently re-fetched — workflow run `31317721215`, run `#575`,
  `head_sha: 67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c` (exact match), `status: completed`,
  `conclusion: success`. `WS-0014` step 7's own content half (overlap-model record population, once a
  future implementation PR performs it) is therefore authorized and awaiting that separate
  implementation — this filing does not touch it.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`, `active_branch:
  claude/xasset-0007-overlap-auth-25p7xx`, `active_pr: null`, `last_verified_main_sha:
  c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e`, `last_verified_date: "2026-08-09"` — stale relative to
  current `main` (`67c62d3...`), since `WS-0014`'s own self-reference fields were last touched by
  `XASSET-0007`'s own governance filing before that PR itself merged. This filing performs the ordinary
  self-reference synchronization (§F below) plus the required Lane M addition confirming `PR #286`'s own
  now-confirmed post-merge state — the `xasset0007-overlap-model-content-authorization` gate's own
  historical text is left unedited, per this repository's established convention.
- **`XASSET-0001` (§A, §D, §E, §F, §J, §M, in full), `XASSET-0005` (decision file plus supporting
  artifact, in full), `XASSET-0006` (in full), and `XASSET-0007` (in full) read directly this session**,
  not summarized from memory.
- **`intelligence/functional_doctrine/{CASH,RESERVE,GLD_DEFENSIVE_ROLE,DEBT_REDUCTION}.yaml` and
  `functional_doctrine_validator.py` independently read directly** — all four confirmed sealed. `RESERVE.
  yaml`'s own `functional_role.role_category: unable_to_determine`, `abstention_reason` text,
  `evidence_quality.thesis_uncertainty_statement`, and `later_governance_action` were each read verbatim
  — no repository evidence anywhere else was found establishing a RESERVE-specific functional purpose
  beyond what that sealed record's own text already discloses; the abstention is preserved, not resolved,
  by this filing (§D of the Decision, §6 of the supporting artifact).
- **`intelligence/etf_classification/GLD.yaml` independently read directly** — confirmed sealed,
  `structural_risk_flags.not_applicable: true`, `cost_and_tracking_quality.expense_ratio_pct: 0.40`,
  `tracking_quality_category: not_yet_measured`, `valuation_and_economic_assessment_readiness.status:
  valuation_required` — every primary source disclosed as `attempted_not_directly_inspected` (this
  environment's network egress policy blocked `ssga.com`/`spdrgoldshares.com`/`sec.gov` outright, per
  that record's own provenance).
- **`functional_doctrine_validator.py`'s own `canonical_record_hash(data: dict) -> str` function
  independently confirmed present** (`functional_doctrine_validator.py:355`) — load-bearing for §4 of the
  supporting artifact's structural-reference design (a future `economic_assessment` record may pin to its
  own corresponding sealed functional-doctrine record by reusing this existing public function, the same
  pattern `GLD_DEFENSIVE_ROLE.yaml` already uses one layer over via
  `etf_classification_validator.canonical_record_hash()`, `etf_classification_validator.py:322`).
- **`VALUATION-0001`, `VALUATION-0002`, and `VALUATION-0004` read directly this session** for the
  design-then-authorize-content separation pattern and false-precision-prevention discipline — not
  imported wholesale; the supporting artifact §1 explains precisely what is and is not reused from that
  series, and why the equity-specific archetype/methodology-matrix machinery does not transfer to a
  fixed three-member population.
- **Decision catalog independently rebuilt**: **101 decisions, `issues == ()`** at the starting head, 101
  non-`README.md` files in `governance/decisions/` reconciling 1:1. `XASSET-0008` confirmed unused: zero
  matches in `governance/decisions.yaml`, zero matches via full-repository grep;
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new decision
  domain needs one") is satisfied by continuing the existing `XASSET-####` series — this filing is the
  direct continuation of `XASSET-0005` §5 step 2's own restated sequence, addressed to the exact three
  capital-use types `XASSET-0005`/`XASSET-0006` already designed and sealed, not a genuinely new decision
  domain, mirroring `XASSET-0002`'s/`XASSET-0005`'s/`XASSET-0006`'s/`XASSET-0007`'s own identical
  continuation of prior `XASSET-0001` §J steps.
- **Full repository `pytest` independently re-run this session: 4042 passed, 0 failed**, matching the
  expected post-`XASSET-0007` baseline exactly.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing designs, as text only — not an authorization, not an adoption, not applied to any real GLD
holding, cash balance, or reserve level — **a closed economic-assessment methodology for exactly three
capital-use types: `CASH`, `RESERVE`, and `GLD_DEFENSIVE_ROLE`**. `DEBT_REDUCTION` is explicitly excluded
(§B). It performs no population, computes no economic finding, and does not itself resolve any sealed
functional-doctrine record's forced `economic_assessment_readiness.status: assessment_required` value.
Full field-by-field detail, closed vocabularies, abstention discipline, structural-reference mechanics,
and the validator/test specification are in the supporting artifact.

### A. Stage separation — five stages, this filing is stage 1 only

1. **Methodology/schema design** — this filing. Designs the closed question set, evidence rules,
   abstention discipline, and structural-reference mechanics. Performs no content.
2. **Future, separate content authorization** — not performed here; requires its own future, explicit
   principal authorization, mirroring `XASSET-0003`'s/`XASSET-0004`'s/`XASSET-0006`'s own role for the
   ETF, crypto, and functional-doctrine content steps.
3. **Future, separate content implementation** — not performed here; the actual drafting and sealing of
   up to three `economic_assessment` records, gated on stage 2's own authorization and its own full
   independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle.
4. **Later cross-asset synthesis** — `XASSET-0001` §E/§F, wholly undesigned, wholly unauthorized by this
   filing or by any future stage-3 content this filing's methodology would produce.
5. **Later explicit policy adoption** — a still-separate, human-approved governance decision, required
   before any evidence this methodology eventually produces may affect any tier, target, holdings, gate,
   cap, cluster, allocator, or margin behavior.

**This filing authorizes stage 1 only.** It does not authorize, begin, schedule, or imply stages 2–5.

### B. Population — exactly three, `DEBT_REDUCTION` explicitly excluded

`CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE` — reusing `XASSET-0005` §3.2's own closed `capital_use_type`
vocabulary, restricted to these three values. `DEBT_REDUCTION` is out of scope: its own economic-
assessment gap (`avoided_borrowing_cost_readiness` / `survivability_and_buffer_benefit_readiness`,
`XASSET-0005` §3.5) belongs to the separately governed margin/leverage-policy track (the 1.8x leverage
cap, the 30% buffer floor, `MARGIN-0005`'s own bounded research charter) — not touched, not reopened, not
weakened by this filing. No equity, ETF beyond GLD (referenced only, §E below), or cryptocurrency
economic assessment is addressed.

### C. Batching — one filing, three capital-use types, no new prefix

All three population members are designed in one filing because they share one schema shape (§E) and the
same classification-hygiene discipline this repository has now applied four times (equity, ETF/crypto,
functional-doctrine, this design) — separating them into three filings would duplicate the shared
abstention/evidence-quality/structural-reference discipline for no review benefit, the same reasoning
`XASSET-0002`'s ETF+crypto batching and `XASSET-0005`'s functional-doctrine+overlap-model batching both
already applied. This filing continues the existing `XASSET-####` series rather than minting a new
prefix — see the Preflight's decision-catalog reconciliation above; `governance/decisions/README.md`'s
own rule is satisfied because this is a direct continuation of `XASSET-0005` §5's own restated sequence,
not a genuinely new decision domain.

### D. RESERVE boundary — abstention preserved, not resolved

`RESERVE.yaml`'s sealed `functional_role.role_category: unable_to_determine` is unchanged by this filing.
No repository evidence independently supports resolving it — confirmed by direct inspection of every
`CLAUDE.md` passage touching `RESERVE`/`CASH` and every other Company/Theme/relationship/classification/
ETF/crypto/functional-doctrine record, none of which narrates a RESERVE-specific functional purpose
beyond the bare label and the mechanical allocator fact it shares with `CASH`. This design:

1. Does **not** infer or assume a RESERVE-specific functional purpose (emergency reserve, margin
   reserve, permanent safety buffer, dry powder, deployment reserve, or any other) anywhere.
2. Designs an explicit abstention-compatible path for RESERVE's economic assessment
   (`deployability_and_optionality`'s own abstention state, supporting artifact §3.2) — RESERVE may
   remain `unable_to_determine` on any axis where evidence is genuinely insufficient, exactly as `CASH`
   or `GLD_DEFENSIVE_ROLE` may.
3. Prohibits inheriting `CASH`'s determined value merely because the two share structural mechanics —
   `deployability_and_optionality` is independently evaluated for RESERVE on its own evidence (supporting
   artifact §3.2's worked example: RESERVE's shared deployment mechanics with `CASH` may support an
   independent determination without first resolving `functional_role`, but the future implementing
   session retains full discretion to abstain on that axis too if it judges the evidence insufficient).
4. Identifies (supporting artifact §6) what future evidence or principal clarification would be required
   to resolve RESERVE's function: either new `CLAUDE.md` doctrine or an explicit principal statement
   naming RESERVE's specific purpose, or an explicit principal statement confirming the abstention should
   stand as permanent governed doctrine — neither performed, invited, or presumed here.
5. Does **not** create a policy answer merely to make the population complete — a RESERVE
   `economic_assessment` record with one or more genuine `unable_to_determine` axes is a fully valid,
   complete, sealed record under this methodology, exactly as much as a fully determined one.

### E. GLD / overlap-model boundary — no duplicate ownership

This methodology may address GLD-specific, single-instrument economic characteristics: cost/tracking-
quality economic significance; historically-grounded inflation-sensitivity characterization, if sourced;
historically-grounded, single-asset crisis/drawdown-behavior characterization, if properly scoped;
deployability/optionality; evidence quality and uncertainty (supporting artifact §3). It does **not**
address, duplicate, or preempt: whole-portfolio volatility/drawdown concentration; quantitative or
portfolio-wide diversification-contribution computation; GLD's measured correlation with Portfolio-HQ's
own current holdings; or `defensive_offset_interface`'s own computation, which remains forced
`not_yet_computable_interface_only` under `XASSET-0005` §6.2's unconditional rule, unchanged by this
filing. Supporting artifact §5 makes this boundary structural, not merely documentary — every future
record populating `historical_equity_drawdown_behavior` must carry an explicit single-asset,
non-portfolio-level disclosure, mechanically enforced by a dedicated future validator scan (supporting
artifact §10 point 11).

GLD's existing sealed functional-doctrine finding (`functional_role.role_category:
defensive_offset_or_ballast`) is evidence this methodology may cite by structural reference; it is not an
adopted portfolio-policy conclusion, and this filing does not treat it as proof of any quantitative
diversification benefit.

### F. CASH and RESERVE boundary — capital-use characterization, not security valuation

`CASH`/`RESERVE` are treated as capital-use categories, never as ordinary securities requiring a
DCF-style valuation. The methodology may characterize, categorically: immediate deployability/
optionality; economic-assessment-readiness disclosure (already sealed, consumed by reference, never
re-derived); uncertainty. It does not invent, and the supporting artifact's validator specification
mechanically forbids: a hurdle rate; a cash expected-return forecast; a target cash percentage; a rank or
score of any kind (supporting artifact §10 point 5).

### G. Zero-numeric default

No new numeric assessment field is authorized anywhere in this schema — stricter than the ETF framework's
own single disclosed-fact carve-out (`expense_ratio_pct`), matching the functional-doctrine and overlap-
model schemas' own zero-numeric-field posture instead. GLD's own sealed `expense_ratio_pct` (and any
other existing sealed numeric structural fact) may be referenced by structural hash/source pin under this
design; it does not become precedent for opening a general numeric assessment schema, and any necessary
future numeric carve-out requires its own explicit, separate authorization.

### H. Structural references — reuse, never duplicate

Where GLD economic assessment relies on `intelligence/etf_classification/GLD.yaml` or
`intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml`, a future implementation must use live
structural-reference/hash-pin semantics, reusing `etf_classification_validator.canonical_record_hash()`
and `functional_doctrine_validator.canonical_record_hash()` — both independently confirmed present and
already relied upon by an existing sealed record — rather than duplicating any sealed field. Supporting
artifact §4 gives the full mechanism, including why a direct pin into `GLD.yaml` (not only a two-hop pin
through `GLD_DEFENSIVE_ROLE.yaml`) is required.

### I. Evidence / contamination boundary

No live account-specific value from `holdings.yaml`, no `target_pct` from `targets.yaml`, no live
`margin_state.py` output, and no current dollar balance may be used as evidence for any judgment axis —
the identical contamination rule `XASSET-0005` §3.6 already established for functional doctrine, applied
here without modification. Existing mechanisms may be cited structurally (e.g., the existence of the 30%
buffer floor, the existence of the deposit/allocation workflow) where genuinely relevant; their current
live outputs create no investment-policy authority under this schema.

### J. Abstention — non-cascading, honestly disclosed

Every substantive axis supports `unable_to_determine` with a required `abstention_reason`; `not_
applicable` is reserved for structurally absent concepts (`instrument_specific_economic_characterization`
on `CASH`/`RESERVE`). One axis's abstention never automatically forces another axis to abstain — tested
explicitly for RESERVE (§D above; supporting artifact §3.2's worked example) and for GLD's own
three-sub-field compound axis (each sub-field independently abstainable, supporting artifact §3.3).
Missing GLD macro evidence (the three named future research questions, §K below) never forces an
invented conclusion — an honest, specific `unable_to_determine` is a complete, valid, sealed outcome.

### K. Future research interface — three named, unanswered questions

Supporting artifact §7 identifies, without answering: GLD's own historical behavior during major
equity-market drawdown periods; GLD's realized tracking quality against its own benchmark; a defensible,
sourced, long-horizon characterization of gold's relationship to inflation regimes. This filing conducts
no research toward any of the three and treats none as already answered.

### L. Synthesis handoff — categorical evidence only

A future `economic_assessment` record's `cross_asset_handoff` envelope may carry only: categorical
economic findings; assessment/completeness status; evidence quality; freshness; uncertainty; abstentions;
structural references. It may never carry: a target weight; a rank; an IN/OUT selection; a buy/sell/hold
signal of any kind; a sleeve percentage; a trade-timing recommendation; a leverage amount. The future
synthesis, not this design, compares competing uses of capital (supporting artifact §8).

### M. Portfolio-selection boundary

Completing economic assessment for `GLD`, `CASH`, and `RESERVE` — however complete — does not select the
portfolio. It creates evidence for a later selection mechanism that does not yet exist:

> evidence → cross-asset opportunity-cost synthesis → explicit human-approved adoption decision → only
> then, governed IN/OUT portfolio membership.

### N. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **One new additive gate, `xasset0007-post-merge-verification`**, recording — without editing the
   `xasset0007-overlap-model-content-authorization` gate's own historical text — that `PR #286` is fully
   merged, reviewed, principal-accepted, and post-merge verified (Preflight above gives the full
   independently re-verified chain). `WS-0014` step 7's own content half is therefore authorized and
   awaiting its own future, separate implementation PR — not begun by this filing.
2. **`active_branch` set to this filing's own branch, `last_verified_main_sha` updated**
   `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e` → `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`, and
   **`last_verified_date` updated** to this filing's own date.
3. **One new additive gate, `xasset0008-gld-cash-reserve-economic-assessment-methodology-design`**,
   recording this filing's own branch and (once it exists) PR number — `status: in_progress`, **not**
   `status: complete`, matching every prior filing's identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: `XASSET-0007`'s own authorization is merged
   (its own future overlap-model content implementation remains separately unauthorized to begin as its
   own PR — that authorization already exists, only the content PR itself does not); this filing, once
   merged, designs but does not authorize a future GLD/CASH/RESERVE economic-assessment content step;
   `DEBT_REDUCTION` economic assessment, the overlap-model content implementation itself, and every other
   remaining `WS-0014` item (steps 2, 8–13 per `XASSET-0001` §J's own numbering) remain wholly
   unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`) is
changed. `WS-0005` and `WS-0015` are not touched by this filing.

## Rationale

**Why this design does not wait for the overlap-model content implementation to actually happen.**
`XASSET-0007` authorizes but does not itself implement overlap-model content — a future, separate
implementation PR remains required. This filing's own scope (GLD/CASH/RESERVE economic-assessment
methodology) is a structurally independent step in `XASSET-0005` §5's seven-step sequence (step 2, versus
overlap modeling's own step 3) — it does not need overlap-model content to exist first, since it consumes
only GLD's already-sealed structural facts (`GLD.yaml`, `GLD_DEFENSIVE_ROLE.yaml`) by direct reference,
never the overlap model's own (still unpopulated) `defensive_offset_interface` dimension. Waiting would
introduce an artificial sequencing dependency this repository's own precedent (`XASSET-0005`'s functional-
doctrine and overlap-model *designs* proceeding in one filing, with their respective *content* steps then
proceeding independently and out of numeric order — functional-doctrine content, `XASSET-0006`, preceded
overlap-model content authorization, `XASSET-0007`, purely because that is the order the principal
authorized them in) does not require.

**Why this design closes only the GLD/CASH/RESERVE slice of step 2, not `DEBT_REDUCTION`'s.**
`DEBT_REDUCTION`'s own economic-assessment gap is inseparable from margin/leverage policy — a track this
repository deliberately keeps under its own separate governance (`MARGIN-0005`'s bounded research
charter, the unchanged 1.8x cap and 30% floor). Folding it into a design filing scoped to non-leveraged
capital-use types would risk exactly the kind of scope-widening this repository's own bounded-unit
discipline (`OPS-0009` Lane G, full weight, never reduced) exists to prevent.

**Why this design borrows the `VALUATION-####` series' discipline but not its machinery.** See supporting
artifact §1 in full. The short version: design-then-authorize-content separation and false-precision-
prevention rules generalize across domains; the 7×7 archetype-methodology matrix does not, because
GLD/CASH/RESERVE have no archetype-differentiation question to research — there are exactly three fixed
capital-use types, each already schema-defined by `XASSET-0005`.

**Why `deployability_and_optionality` is a genuinely new axis, not a restatement of `liquidity_
character`.** `liquidity_character` (already sealed on every functional-doctrine record) answers "is this
capital use convertible to cash." It says nothing about whether being in that state costs or preserves
anything in the ability to actually act on a future opportunity — a question this repository has never
asked anywhere. Re-deriving `liquidity_character` under a new name would add a field with no new
information; `deployability_and_optionality` adds a genuinely new evidence dimension.

**Why RESERVE's abstention is preserved rather than resolved by inference from CASH.** The governing
authorization is explicit and absolute on this point, and `XASSET-0006` §C already established the
"never force a value merely to fill the record" discipline this filing extends one schema further. Two
capital-use types sharing identical mechanical allocator treatment (`RESERVE`/`CASH`, both "never a buy
candidate, definitionally satisfied") does not make their functional purposes identical — treating shared
mechanics as proof of shared function would be exactly the inference `XASSET-0006` § Preflight explicitly
found the account's own doctrine does not support.

## Alternatives Considered

**Design `DEBT_REDUCTION`'s economic-assessment methodology in the same filing, for full step-2
coverage.** Rejected — see Rationale; `DEBT_REDUCTION`'s own gap belongs to the margin/leverage-policy
track, a deliberately separately governed domain this filing does not open.

**Wait for the overlap-model content implementation to merge before filing this design.** Rejected — see
Rationale; the two steps are structurally independent, and `XASSET-0005`/`XASSET-0006`/`XASSET-0007`'s
own out-of-numeric-order content sequencing already establishes that `XASSET-0001` §J's step numbering is
a recommended order, not a strict dependency chain, for genuinely independent steps.

**File three separate methodology-design filings, one per capital-use type.** Rejected — the three share
one schema shape and the same classification-hygiene discipline; separating them would duplicate the
shared abstention/evidence-quality/structural-reference design across three documents for no review
benefit, the same reasoning `XASSET-0002`'s and `XASSET-0005`'s own batching already applied.

**Adopt `VALUATION-0001`'s 7×7 methodology-family-by-archetype matrix, scaled down.** Rejected — see
supporting artifact §1; a matrix built for a methodology-selection-across-archetypes problem does not fit
a fixed, three-member, already-schema-defined population with no archetype-differentiation question.

**Attempt to infer or name a RESERVE-specific functional purpose from CLAUDE.md's overall doctrine tone
(e.g., inferring "margin cushion" from the account's own leveraged posture).** Rejected outright — no
`CLAUDE.md` passage narrates this, and inferring it would be exactly the "force a value merely to fill
the record" failure `XASSET-0006` §C already forecloses, applied here to a governance decision rather than
a content record.

**Design a fourth, `redundancy_or_distinctiveness_characterization` axis comparing CASH and RESERVE
directly.** Rejected — supporting artifact §3.1's disposition table addresses this candidate explicitly:
it would either duplicate RESERVE's own already-abstained `functional_role` question under a different
field name, or implicitly pressure a future drafting session to resolve that question through this new
schema instead of its own proper resolution path (§D above).

## Consequences

**Authorized, effective only on this decision's merge:** the closed GLD/CASH/RESERVE economic-assessment
methodology design in the supporting artifact (three-member population, `deployability_and_optionality`
and `instrument_specific_economic_characterization` axes, two structural-reference mechanisms, combined
validator/test specification); confirmation, via one additive `operations/WORKSTREAMS.yaml` gate entry,
that `XASSET-0007`'s own authorization (PR #286) is fully merged, reviewed, principal-accepted, and
post-merge verified; `WS-0014`'s ordinary self-reference synchronization.

**Not authorized by this filing, now or ever without a further separate decision:** population of any
`economic_assessment` record; any economic finding, categorical or otherwise, for `GLD`, `CASH`, or
`RESERVE`; resolution of `RESERVE.yaml`'s own `functional_role` abstention; any `DEBT_REDUCTION`
economic-assessment methodology; any resolution of any sealed functional-doctrine record's forced
`economic_assessment_readiness.status`; any overlap-model dimension computation (`XASSET-0007`'s own
future, separate content implementation, untouched here); any cross-asset opportunity-cost synthesis;
any Level 1 sleeve or Level 2 instrument sizing; any validator or test implementation; any edit to
`XASSET-0001`, `XASSET-0005`, `XASSET-0006`, or `XASSET-0007`'s own text; and any tier/target/holdings/
role/cluster/cap/gate/allocator/margin/ladder/chart/order/trade change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification/functional-doctrine record, byte-for-byte,
including all four sealed functional-doctrine records and GLD's own sealed ETF classification;
`XASSET-0001` through `XASSET-0007`'s own accepted text and scope, in full, unedited; `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`;
the 1.8x leverage cap and 30% margin-buffer floor; `WS-0005`'s completed, `status: complete` state;
`WS-0015`'s own live state; `WS-0014`'s own `status: proposed`/`priority: secondary`.

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ
is not a 27-stock system, and this filing's own bounded three-capital-use-type methodology design does
not narrow that fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical
equities; contender-registry regeneration and legacy-history recovery; QQQ and any other future ETF
candidate expansion; ETF and crypto economic/valuation methodology; equity Stage-4 valuation execution;
`DEBT_REDUCTION` economic assessment; the overlap-model content implementation itself (`XASSET-0007`'s own
authorized, still-unbegun next step); cross-asset opportunity-cost synthesis; Level 1 sleeve allocation;
Level 2 instrument allocation; `CHART-0003` and any remaining governed chart ingestion; ladder/deployment
integration; unlevered testing; margin/leverage-policy review; monitoring/sell discipline; final
integration and audit; and any true whole-universe allocation test.
