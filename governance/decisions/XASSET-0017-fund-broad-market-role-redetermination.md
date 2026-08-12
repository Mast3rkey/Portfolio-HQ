---
decision_id: XASSET-0017
date: 2026-08-12
status: Proposed
category: level1_policy_adoption_redetermination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0007, TIER-0009, TIER-0011, REL-0001, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0012, XASSET-0013, XASSET-0014, XASSET-0015, XASSET-0016, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, VALUATION-0006, VALUATION-0007, CONTENDER-0001, CONTENDER-0002, CONTENDER-0003, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04, NUM-0001, TGT-0001]
supporting_artifact: governance/audits/WS0014_FUND_BROAD_MARKET_ROLE_REDETERMINATION_20260812.md
file: governance/decisions/XASSET-0017-fund-broad-market-role-redetermination.md
---

## Context

### Authority for this unit

The human repository principal explicitly authorized exactly **one bounded, evidence-only unit** that
re-applies `XASSET-0014`'s own already-accepted, unedited Axis A/B/C policy-adoption methodology to
one already-sealed sleeve, `fund_broad_market`, using only already-sealed evidence. This filing does
**not** redesign `XASSET-0014`/`XASSET-0015`'s methodology or population authorization, does **not**
touch `XASSET-0016`'s own numeric-sizing methodology, does **not** compute any Level 1 percentage or
populate any `numeric_sizing` record, does **not** select or size any Level 2 instrument (`SPY`/`VEA`/
`VWO`), and does **not** reopen `QQQ`, any contender-registry entry, or any deferred relationship pair.
It answers exactly one question, honestly, without a pre-selected outcome: does `fund_broad_market`'s
own already-sealed evidence now support a `portfolio_function_status` of `function_confirmed_distinct`,
or should it remain `function_status_unresolved`? The principal's own stated purpose for the timing:
resolving the eligible-sleeve population **before** any Level 1 numeric-sizing work begins avoids
forcing an unnecessary re-derivation later — `XASSET-0016` (Stage 5's own methodology/authorization
filing) is confirmed merged, but no `numeric_sizing` record of any kind has yet been populated under
it, making this the correct, and only, moment to perform this redetermination cleanly.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/xasset-0017-broad-market-role-w3eoks`, working tree clean at session start.
- **`origin/main`/local `HEAD` reconciled.** Both confirmed identical at
  `8886187d268bf1a7fede8ec5853cdcc32f24a020` — `PR #307`'s own merge commit (parents
  `0dc3f33c5fa539b2d44fb1579ab23df8cb730a4a`, `XASSET-0015`'s own merge commit, and
  `3fc164b524d2f3993e7392dc9d4679af7e7360c0`, `PR #307`'s own head), independently re-confirmed via
  `git show -s --format='%H %P'`.
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #307` (`XASSET-0016`) independently re-confirmed merged** via the GitHub API:
  `merged: true`, `merged_by: Mast3rkey`, base `0dc3f33c5fa539b2d44fb1579ab23df8cb730a4a`, four commits
  (one original submission plus three bounded-correction rounds), merged via merge commit
  `8886187d268bf1a7fede8ec5853cdcc32f24a020`.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **113 decisions, `issues == ()`**, reconciling exactly against `governance/decisions.yaml`'s own 113
  rows. **`XASSET-0017` independently confirmed the next unused identifier** — zero matches anywhere
  in `governance/decisions.yaml` or via full-repository grep.
- **`XASSET-0014` (decision file and its own supporting artifact) and `XASSET-0015` read directly, in
  full, not summarized from memory.** `XASSET-0014`'s own three lawful Axis A evidentiary bases
  (relationship-record finding; `CLAUDE.md` doctrine citation; structural `targets.yaml`-destination-
  category membership), its own §7.2 illustrative `fund_broad_market` trace, its own §10
  overlap-coordination boundary rule (overlap/individual-instrument weakness is an Axis C caveat only,
  never a lawful ground for suppressing Axis A), and its own §5/§5.1 mechanical Axis C derivation are
  the exact controlling text this filing applies, unedited. `XASSET-0015` §E's own text — "a future
  Stage 4c drafting session evaluating `fund_broad_market` retains full discretion to independently
  judge the available evidence... nothing in this filing narrows that discretion or pre-selects an
  outcome" — is independently re-confirmed as the specific, standing delegation this filing exercises.
  Neither decision file is edited by this filing.
- **The live, sealed `fund_broad_market.yaml` `policy_adoption` record independently read and
  reproduced in full before any edit**: `portfolio_function_status: function_status_unresolved`,
  `capital_eligibility_status: eligible_for_target_consideration`,
  `sizing_readiness_status: sizing_blocked`. Its own `function_rationale` independently confirmed: Basis
  1 unavailable (the sole sealed relationship, `equity_fund_broad_market`, resolves
  `stronger_evidence_maturity`); Basis 2 not asserted (no dedicated `CLAUDE.md` passage identified);
  Basis 3 available (live `targets.yaml` `fund` rows scoped to `SPY`/`VEA`/`VWO`) but judged
  insufficient **in complete isolation, with no offsetting evidence anywhere in this sleeve's own
  sealed corpus identified at that time** — the prior drafting session's own words, quoted verbatim in
  this filing's own supporting artifact. The record's own text explicitly, independently confirms this
  redetermination is lawful: "a future drafting session could also reach a different judgment on
  today's identical evidence base within that same delegated discretion, since `XASSET-0015` SS E's own
  text does not pre-select an outcome."
- **Every input this redetermination reads independently re-hashed and confirmed byte-unchanged since
  the prior determination**: the `fund_broad_market` `sleeve_profile` record
  (`referenced_content_sha256: 2ed99d67847a9aea644be6867c53cac15b5870eff84ea759ab87a7a3a2d49de1`) and
  the `equity_fund_broad_market` `sleeve_relationship` record
  (`referenced_content_sha256: 8667974b8e08926173ffb9819e4418a06fe2731b0983883fab062e8a272ed0f8`) —
  both hashes match the values already cited in the prior sealed record exactly, confirming this is a
  pure re-exercise of discretion on unchanged evidence, never triggered by new Stage 1–3 content.
  `targets.yaml`'s own live `fund` rows independently re-confirmed: `SPY`/`VEA`/`VWO`/`GLD`, three of
  the four scoped to `fund_broad_market` per `XASSET-0012` §2's own fixed table, unchanged.
- **`operations/WORKSTREAMS.yaml`'s `WS-0014` full live entry independently re-read**: `status:
  proposed`, `priority: secondary`, `dependencies: [WS-0005]`. Fifty-seven milestone gates recorded
  through `xasset0016-level1-numeric-sizing-methodology-and-authorization` (`status: in_progress`,
  `pr: null`) — stale as of this session's start, since `PR #307` is, in fact, fully merged (see
  above); §I below synchronizes it without editing any prior gate's own text. `active_branch:
  claude/xasset-0016-level1-sizing-q19xci`, `active_pr: null`, `last_verified_main_sha:
  0dc3f33c5fa539b2d44fb1579ab23df8cb730a4a` — one merge behind the current tip; also synchronized.
  `intelligence/level1_sleeve_synthesis/numeric_sizing/` independently confirmed **absent** — no Stage
  5 content exists anywhere in the repository, confirming this redetermination lands before any
  downstream numeric-sizing work exists to be disturbed, exactly the timing the principal's own
  authorizing directive named as the reason for doing this now.

## Decision

### A. What this filing does — a bounded Axis A/B/C redetermination for one sleeve, using existing evidence only

This filing re-applies `XASSET-0014`'s own accepted, unedited Axis A/B/C methodology to
`fund_broad_market`'s own already-sealed `policy_adoption` record, exercising the same delegated
discretion `XASSET-0015` §E already, explicitly reserved for exactly this situation — not a new grant
of Stage 4 authority, not a schema change, not a re-authorization of any other sleeve's own record. No
other sleeve's `policy_adoption` record is touched. No `sleeve_profile` or `sleeve_relationship` record
is touched. Full evidentiary walk-through — `SPY`/`VEA`/`VWO` role-level evidence, the overlap-model
records, and the geographic/currency interface gap — in the supporting artifact §§2–6.

### B. Reproducing the prior block, and confirming it is reopenable discretion, not a hard rule

The prior determination rested on a single, disclosed, general epistemic-sufficiency judgment: Basis 3
(the sleeve's own live `targets.yaml fund` category membership) is a bare categorical/structural fact,
and the prior drafting session judged that fact, standing alone with "no offsetting evidence anywhere
in this sleeve's own sealed corpus," insufficient to reach `function_confirmed_distinct`. This was not
a mechanically forced outcome — nothing in `XASSET-0014`'s own text imposes a two-basis corroboration
requirement, and `Basis 3` is, by `XASSET-0014` §3.2's own explicit design, independently sufficient in
principle for every sleeve it is available to, exactly as it already is, unaccompanied by any other
basis, for `crypto` (`function_confirmed_distinct` via Basis 1 **or** Basis 3, either alone sufficient)
and `cash_reserve` (same shape). `XASSET-0015` §E's own text confirms this was a discretionary,
reopenable judgment call, not a hard rule: "nothing in this filing narrows that discretion or
pre-selects an outcome," and the sealed record's own rationale independently states a future session
"could also reach a different judgment on today's identical evidence base." Full basis-by-basis
reproduction in the supporting artifact §1.

### C. `SPY`/`VEA`/`VWO` role-level evidence — heterogeneity, not uniformity

Independently re-read this session: `SPY` (`role_category: broad_market_beta`, `domestic_us`,
`usd_only`) carries the weakest individual economic showing in the sleeve — its own sealed
instrument-economic-assessment record resolves `elevated_vs_category` on cost/tracking, and it is the
subject of the sleeve's own only disclosed overlap flag. `VEA` (`role_category:
developed_ex_us_equity`, `developed_ex_us`, `foreign_currency_mixed`) and `VWO` (`role_category:
emerging_market_equity`, `emerging_markets`, `foreign_currency_mixed`) each carry a materially
different geographic/currency exposure category from both `SPY` and from the equity sleeve's own
predominantly domestically-listed, individually-researched common-stock roster — `VEA` resolves
`favorable_vs_category` and `VWO` resolves `in_line_with_category` on their own respective cost
comparisons. This heterogeneity is not new evidence introduced at this layer — it is already disclosed,
descriptively, inside `fund_broad_market`'s own already-sealed `sleeve_profile` record (a permitted
Stage 4 input under `XASSET-0014` §1, not a new one), whose own `economic_role_summary` states the
sleeve "cover[s] domestic, developed-ex-domestic, and emerging equity exposure." `XASSET-0014`'s own
three-basis rule is a sleeve-level, not an instrument-level, test — it nowhere requires every
instrument within a sleeve to independently clear Axis A on its own, and `SPY`'s own weaker showing and
the disclosed overlap are, by `XASSET-0014` §10's own binding rule, an Axis C caveat only, never a
lawful ground for suppressing Axis A. Full instrument-by-instrument treatment in the supporting
artifact §§2–4.

### D. Geographic/currency interface gap and the ETF/direct-equity overlap boundary — neither promoted, neither used to suppress

The `geographic_currency_exposure` overlap-model dimension remains, correctly, unpromoted: its own
sealed record still resolves `computation_status: not_yet_computable_interface_only` — no
whole-portfolio geographic/currency rollup mechanism exists, and this filing does not build one, invent
one, or treat the gap as resolved. The per-instrument geographic/currency facts already sealed on
`SPY`/`VEA`/`VWO`'s own `etf_classification` records remain available and were read as role-level
context, exactly as `XASSET-0014` §1 already permits via the sleeve profile's own evidentiary chain; no
whole-portfolio finding is asserted anywhere in this filing. The `etf_direct_equity_duplication` and
`issuer_overlap_etf_lookthrough` dimensions remain, correctly, real, mechanically computed, and
descriptive/coordination evidence only — `XASSET-0014` §10's own rule, restated and applied, not
reopened: overlap disclosure "may never... force `fund_broad_market`'s Axis A below whatever value its
own lawful evidentiary basis actually supports." No "overlap implies rejection" inference is drawn
anywhere in this filing. Full treatment in the supporting artifact §§5–6.

### E. Axis A redetermination

`portfolio_function_status` is redetermined from `function_status_unresolved` to
`function_confirmed_distinct`, on **Basis 3** (structural `targets.yaml`-destination-category
membership) — the same, unchanged, categorical fact already available before this filing — **informed**
by `fund_broad_market`'s own already-sealed profile content, which discloses that this sleeve's covered
funds span a heterogeneous set of geographic/currency exposure categories, genuinely and structurally
distinct in kind from the equity sleeve's own single-name, individually-researched approach.
`SPY`'s own individually weaker showing and the disclosed `equity`/`fund_broad_market` overlap are
explicitly, per §D above, **not** used to suppress this finding — they remain Axis C caveats. Basis 1
remains unavailable (unchanged: the sleeve's sole sealed relationship still resolves
`stronger_evidence_maturity`, mechanically excluded by construction). Basis 2 remains not asserted (no
genuine, dedicated `CLAUDE.md` passage for this sleeve is identified or manufactured). Full rationale,
matching the sealed record's own `function_rationale` field verbatim in substance, in the supporting
artifact §7.

### F. Axis B and Axis C mechanically re-derived, not authored

Axis B (`capital_eligibility_status`) is **unchanged**: `eligible_for_target_consideration`, a pure
function of the sleeve's own unchanged `evidence_coverage_profile`
(`substantially_computed_with_disclosed_gaps`), independently re-verified live against
`fund_broad_market.yaml`'s own sealed `sleeve_profile` record. Axis C (`sizing_readiness_status`) is
**mechanically recomputed**, per `XASSET-0014` §5/§5.1's own unedited rule
(`portfolio_function_status == function_confirmed_distinct` and `capital_eligibility_status ==
eligible_for_target_consideration`, zero `sealed_unresolved` relationship pairs, at least one
`deferred_disclosed` pair present), from `sizing_blocked` to **`sizing_conditionally_ready`** — never
`sizing_ready`, since four of this sleeve's own five possible relationship pairs (against
`fund_gld_defensive`, `crypto`, `cash_reserve`, `debt_reduction`) remain `deferred_disclosed`, unchanged
and not researched or closed by this filing. `blocking_evidence[]` is correspondingly re-derived: the
prior axis-level `axis_a_unresolved` entry is removed (no longer true); the one `secondary_condition_
present` entry (against `equity`) and the four `deferred_relationship_pair` entries are retained, each
independently re-verified live against the seven sealed `sleeve_relationship` records and `XASSET-0013`
§E's own eight named, closed deferred-pair set. `relationship_coverage_ledger[]`, `unresolved_
relationships[]`, and `overlap_coordination_notes[]` are unchanged in substance (ledger states do not
depend on Axis A). Confirmed by direct execution of `level1_sleeve_synthesis_validator.py`'s own live
mechanical checks against the resealed record — see §J below.

### G. Numeric-sizing-eligibility consequence — categorical only, no computation performed

`fund_broad_market` moves, categorically, from the population of sleeves `XASSET-0016`'s own decision
file described as "sizing_blocked" (`fund_broad_market`, `cash_reserve`, `debt_reduction`) into the
population it described as "sizing_conditionally_ready" (`equity`, `fund_gld_defensive`, `crypto`) —
the live sealed corpus now reads **four** sizing_conditionally_ready sleeves (`equity`,
`fund_gld_defensive`, `crypto`, `fund_broad_market`) and **two** sizing_blocked sleeves (`cash_reserve`,
`debt_reduction`). This filing computes **no** R2/R3 trigger state, **no** provisional target
percentage, **no** reserved-capital reconciliation figure, and **no** Level 2 instrument weight of any
kind — those remain exclusively `XASSET-0016`'s own future, separately authorized Stage 5
implementation's own work, entirely untouched here.

### H. Level 1/Level 2 boundary and `QQQ`/contender boundary — restated, not touched

`SPY`/`VEA`/`VWO`'s own individual weight, selection, or sizing within `fund_broad_market` remains a
wholly separate, later, unauthorized Level 2 question — this filing names them only as identity
references (the sleeve's own already-fixed `asset_class`/ticker scope, per `XASSET-0014` §3.2's own
Basis 3 ticker-scoping mechanism), never as bearers of any weight, target, or size of any kind, and the
Level 2 leakage scan (`level1_sleeve_synthesis_validator.py`'s own unmodified `_stage4_level2_weight_
patterns`) independently confirms zero such leakage in the resealed record. `QQQ`, the remaining
contender-registry entries, and every deferred relationship pair are not reopened, restated, researched,
or closed by this filing — `fund_broad_market`'s own four `deferred_disclosed` pairs remain exactly as
`XASSET-0013` §E left them.

### I. Supersession mechanism — reseal in place, cite by decision-ID, no validator change

Independently confirmed via direct inspection of `level1_sleeve_synthesis_validator.py`: this schema
has **no** `superseded`/versioned `record_status` value (`_LIFECYCLE_VALUES = {"draft", "sealed"}`,
unchanged) and its own `validate_policy_adoption_data()` **hard-locks** `governing_decisions` to
exactly `{"XASSET-0014", "XASSET-0015"}` (an equality check, not a subset check) — adding `XASSET-0017`
to that field would itself require a validator change this filing declines to make, since the smaller,
correct mechanism already exists and needs no widening. `XASSET-0014` §7's own text already frames
every Axis A/B/C value as "a live-derived computation over currently-sealed evidence, never a permanent
lock," recomputed "from scratch" by a future re-population — the record's own designed nature, not
authored, immutable prose. Accordingly, the **narrowest correct mechanism** is applied: the sealed
`fund_broad_market.yaml` record is resealed in place with its redetermined Axis A/B/C values, a new
`sealed_at`/`content_sha256`/`drafting_session_or_shard_id`, and `governing_decisions` left **unchanged**
at `["XASSET-0014", "XASSET-0015"]` (the methodology and population-authorization filings that actually
grant Stage 4 authority) — `XASSET-0017` is cited, and the prior determination's own outcome and
reasoning are preserved, entirely within the record's own `function_rationale` free-text field, using
the decision-ID citation pattern the validator's own free-text scan already, explicitly whitelists
(`_DECISION_ID_LEGITIMATE_USE_PATTERN`). Git history and this decision's own text independently
preserve the full prior state for audit — the prior sealed content (`content_sha256:
b922e68d769d6e3611ae6f3c59344816e7a28a13eca8624ac32dfc6aadd38788`) remains permanently retrievable from
version control; nothing is silently discarded. Zero diff to `level1_sleeve_synthesis_validator.py`
itself. Full reasoning, including the alternatives considered and rejected, in the supporting artifact
§8.

### J. Validator/test impact — no validator change, three fixture-value test updates

`level1_sleeve_synthesis_validator.py` already, correctly, mechanically supports either outcome for
`fund_broad_market` (Basis 3's live availability makes `function_confirmed_distinct` a validator-
admissible value; the mechanism was never hardcoded to force `function_status_unresolved`) — confirmed
by running the actual validator against the resealed record, which passes clean with **zero** code
changes: `level1_sleeve_synthesis_validator.py` run standalone this session: `OK (7 profile result(s),
8 relationship result(s), 7 policy_adoption result(s))`. Three pre-existing tests in
`test_level1_sleeve_synthesis_validator.py` hardcoded the prior real-corpus fixture value for
`fund_broad_market` (`test_axis_a_outcomes_exactly_as_derived`, `test_axis_c_outcomes_exactly_as_
derived`, and a non-cascading-abstention proof test renamed from `test_fund_broad_market_axis_a_
unresolved_does_not_touch_other_sleeves_axis_a` to `test_fund_broad_market_axis_a_does_not_touch_
other_sleeves_axis_a`) — each updated to the newly authorized live value, following this repository's
own established scaffold-superseded-by-authorized-content precedent (e.g. `PR #270`'s/`PR #272`'s own
`TestZeroRealCompanyPopulation` → `TestAuthorizedCohortPopulation` pattern); no test was weakened, and
the renamed test's own proof shape (one sleeve's Axis A cannot cascade into another's) is unaffected by
which value it holds.

### K. Explicit non-authorization

This filing authorizes redetermination of `fund_broad_market`'s own Axis A/B/C values only. It does
**not** authorize:

- any numeric Level 1 sleeve-level target, percentage, or reserved-capital figure of any kind, for
  `fund_broad_market` or any other sleeve;
- any `intelligence/level1_sleeve_synthesis/numeric_sizing/` record population — `XASSET-0016`'s own
  future, separate implementation remains wholly unauthorized to begin by this filing;
- any `XASSET-0016` R2/R3 trigger-state inference, live or otherwise;
- any Level 2 instrument selection or weight, for `SPY`, `VEA`, `VWO`, or any other instrument;
- any `QQQ`/ETF-scope revisit, or research on any contender-registry entry;
- any redetermination of any OTHER sleeve's own `policy_adoption` record (`equity`, `fund_gld_
  defensive`, `crypto`, `cash_reserve`, `debt_reduction` are all untouched, byte-identical);
- any research on, or closure of, any of `fund_broad_market`'s own four `deferred_disclosed`
  relationship pairs;
- any resolution of `debt_reduction`'s own economic-assessment forced-abstention state, or of the
  `CASH`/`RESERVE` consolidation question;
- any `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`,
  `margin_state.py`, or `levels.py` change;
- any allocation check of any kind, live or scenario;
- any chart evidence, buy-ladder work, backtesting, monitoring, or sell-discipline rule;
- any tier/target/holdings/gate/cap/cluster/order/trade change of any kind.

## Rationale

`XASSET-0015` §E deliberately, explicitly preserved standing discretion for a future drafting session
to reach a different Axis A judgment for `fund_broad_market` on unchanged evidence — an unusual, named
exception to this repository's otherwise-standard "closed question, no re-runs without a new regime in
the data" discipline (e.g. every closed backtest in the Decisions Log). That preservation exists
precisely because the prior determination was disclosed, honestly, as a conservative discretionary
judgment call resting on treating Basis 3 in complete isolation — not as a mechanically forced or
evidentiarily compelled outcome. Exercising that reserved discretion now, before any numeric Level 1
sizing work begins, avoids exactly the "unnecessary re-derivation" cost the principal's own authorizing
directive named: had this redetermination happened after `XASSET-0016`'s own future Stage 5
implementation populated a `numeric_sizing` record treating `fund_broad_market` as `sizing_blocked`,
that record would itself require its own future re-derivation once the sleeve's own eligibility
changed — strictly worse than resolving the eligible-sleeve population first. The specific finding this
filing reaches — that a sleeve-level Axis A judgment should weigh the sleeve's own disclosed internal
heterogeneity (here, genuinely distinct geographic/currency exposure in two of three covered
instruments) rather than being anchored to its weakest individual instrument, with that weaker showing
correctly relegated to an Axis C caveat per `XASSET-0014` §10's own binding rule — is a direct,
principled application of rules `XASSET-0014` already adopted, not a new rule invented here.

## Alternatives Considered

**Leave `fund_broad_market` at `function_status_unresolved`, treating the original determination as
settled.** Rejected — `XASSET-0015` §E's own text explicitly, deliberately reserved ongoing discretion
for exactly this sleeve on exactly this question; treating the original determination as closed would
read that reservation out of the governing text. Nothing evidentiary has changed since the original
determination (every input hash independently reconfirmed unchanged, §Preflight above), but `XASSET-
0015` §E's own reservation was never conditioned on new evidence — it was conditioned on a future
session's own independent judgment, exactly what this filing performs.

**Manufacture a fourth Axis A evidentiary basis from the instrument-level `SPY`/`VEA`/`VWO` economic-
assessment and classification records, read directly rather than through the sleeve profile's own
summary.** Rejected — `XASSET-0014` §1's own text restricts Stage 4's evidentiary consumption to the
sleeve_profile/sleeve_relationship record pair (plus the two named, narrow exceptions for `CLAUDE.md`
doctrine and `functional_doctrine/DEBT_REDUCTION.yaml`); the deeper instrument-level records are
Stage-1-adjacent inputs `XASSET-0013`'s own Stage 3 implementation already synthesized into the
sleeve_profile's own `economic_role_summary` — reading that summary (an already-permitted Stage 4
input) is the correct evidentiary path; reading the instrument-level records directly, and treating
them as an independent basis, would exceed §1's own stated evidentiary boundary and manufacture a
basis `XASSET-0014` §3.2 does not define.

**Require instrument-level unanimity across `SPY`/`VEA`/`VWO` before Axis A may clear.** Rejected —
`XASSET-0014`'s own three-basis rule, and Basis 3 specifically, operate at the sleeve level; nothing in
the governing text conditions a sleeve-level Axis A finding on every individual instrument within that
sleeve independently satisfying the same bar, and the Level 1/Level 2 boundary this repository has
maintained throughout this undertaking counsels against inventing an instrument-level unanimity
requirement that would functionally collapse Level 1 and Level 2 questions together.

**Treat the disclosed `etf_direct_equity_duplication`/`issuer_overlap_etf_lookthrough` overlap, or
`SPY`'s own weaker individual cost/tracking showing, as grounds to affirm `function_status_unresolved`.**
Rejected outright — `XASSET-0014` §10's own binding rule states overlap disclosure "may never... force
`fund_broad_market`'s Axis A below whatever value its own lawful evidentiary basis actually supports";
using it to suppress Axis A here would directly contradict already-accepted, controlling text.

**Add `governing_decisions: XASSET-0017` to the resealed record, widening the validator's own exact-set
check.** Rejected — the smaller, correct mechanism (citing `XASSET-0017` within the record's own
`function_rationale` free text, already a validator-permitted pattern) fully preserves provenance
without touching validator code; widening a hard-locked mechanical check for one redetermination event
would be a disproportionate, unnecessary schema change for a fact this repository's own git history and
decision-file narrative already preserve completely.

**Create a new, separate, versioned record (e.g. `fund_broad_market_v2.yaml`) rather than reseal in
place.** Rejected — this schema has no versioning concept anywhere (`COHORT_MANIFEST.yaml` expects
exactly one record per `sleeve_id`, mechanically enforced), and `XASSET-0014` §7's own text already
frames every Axis A/B/C value as a live-derived computation recomputed from scratch on re-population,
not an append-only historical ledger — inventing a versioning scheme here would contradict the record
type's own designed nature and require its own separate schema-design authorization this filing does
not have.

## Consequences

**Changes as a direct result of this decision**: `fund_broad_market`'s own sealed `policy_adoption`
record — `portfolio_function_status` from `function_status_unresolved` to `function_confirmed_distinct`
(Basis 3, informed by this sleeve's own already-sealed profile content); `capital_eligibility_status`
unchanged (`eligible_for_target_consideration`); `sizing_readiness_status` mechanically recomputed from
`sizing_blocked` to `sizing_conditionally_ready`; `blocking_evidence[]` correspondingly re-derived (the
axis-level entry removed, the secondary-condition and four deferred-pair entries retained);
`relationship_coverage_ledger[]`/`unresolved_relationships[]`/`overlap_coordination_notes[]` unchanged
in substance; `sealed_at`/`content_sha256`/`drafting_session_or_shard_id` updated;
`governing_decisions` unchanged. The corresponding `COHORT_MANIFEST.yaml` entry updated to match. Three
pre-existing tests in `test_level1_sleeve_synthesis_validator.py` updated to the newly authorized live
fixture values (net test count unchanged: 763 before, 763 after). Two additive
`operations/WORKSTREAMS.yaml` gates on the existing `WS-0014` entry (`xasset0016-post-merge-
verification`, `xasset0017-broad-market-role-redetermination`), plus append-only narrative updates to
the `next_action`/`blocker` fields and refreshed `active_branch`/`last_verified_main_sha`/
`last_verified_date` self-reference fields — no prior gate's own text edited. The population of sleeves
the live sealed corpus reads as `sizing_conditionally_ready` grows from three to four (`equity`,
`fund_gld_defensive`, `crypto`, `fund_broad_market`); `cash_reserve` and `debt_reduction` remain
`sizing_blocked`, unaffected.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin
behavior; the 1.8x leverage cap or 30% margin-buffer floor; `XASSET-0014`'s or `XASSET-0015`'s own
text (both remain unedited, controlling authority); `level1_sleeve_synthesis_validator.py`'s own code
(zero diff); any OTHER sleeve's own `policy_adoption`, `sleeve_profile`, or `sleeve_relationship`
record; any ETF-classification, crypto-classification, instrument-economic-assessment, overlap-model,
functional-doctrine, or economic-assessment record; `XASSET-0016`'s own decision file or supporting
artifact text (both remain unedited — its own now-stale three/three point-in-time citation is
disclosed, not corrected, per this repository's established never-silently-rewrite convention); any
numeric Level 1 or Level 2 sizing content, populated or authorized; any allocation check; `WS-0005`'s
completed, `status: complete` state; or `WS-0014`'s own `status: proposed`/`priority: secondary` (this
filing adds two additive gates, it does not begin execution or change the workstream's own status/
priority). Completing this unit does not itself authorize `XASSET-0016`'s own future Stage 5
implementation, does not compute any percentage for any sleeve, and does not authorize any allocation
check — each requires its own separate, explicit, future principal authorization, per `XASSET-0012`
§10's own unedited four-stage sequence, `XASSET-0014` §15's own unedited eleven-condition numeric-
sizing gate, and `XASSET-0001` §J's own dependency-ordered roadmap.
