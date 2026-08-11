---
decision_id: XASSET-0014
date: 2026-08-11
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0007, TIER-0009, REL-0001, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0012, XASSET-0013, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, VALUATION-0006, VALUATION-0007, CONTENDER-0001, CONTENDER-0002, CONTENDER-0003, PHQ-2026-01, PHQ-2026-02, NUM-0001]
supporting_artifact: governance/audits/WS0014_LEVEL1_POLICY_ADOPTION_METHODOLOGY_DESIGN_20260811.md
file: governance/decisions/XASSET-0014-ws0014-level1-policy-adoption-methodology.md
---

## Context

### Authority for this unit

The human repository principal explicitly authorized exactly **one bounded, design-only governance
filing** defining the methodology for Stage 4 of `XASSET-0012` §10's own four-stage sequence —
"future policy adoption / portfolio selection, if separately authorized." This filing does not
populate a policy-adoption record for any sleeve, does not assign any sleeve a role, eligibility, or
sizing-readiness disposition, does not create any numeric weight or target of any kind, and does not
authorize any allocation check or Level 2 action. It is the first sub-unit of Stage 4 ("Stage 4a"),
mirroring `XASSET-0012`'s own role as Stage 1 of the synthesis sequence.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/level-1-policy-adoption-design-9w9gvr`, working tree clean at session start.
- **`origin/main` fetched and reconciled.** Local branch head and `origin/main` both confirmed
  identical at `9d70f592939156e5418a8ae706854868775009a7` — matching the directive's own stated SHA
  exactly. This is `PR #303`'s own merge commit (parents `cfea220c82bae310f2412804a204e85f257a2782`
  and `0ebf7106fc13247d2d2952cebef253cbc946aa69`, independently re-confirmed via
  `git log --pretty='%H %P'`).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #303`'s full lifecycle independently re-verified via the GitHub API, not assumed**: `merged:
  true`, `merged_by: Mast3rkey`, base `cfea220c82bae310f2412804a204e85f257a2782` (`XASSET-0013`'s own
  merge commit), five commits (one original submission plus four bounded-correction rounds,
  independently confirmed via `git log`), merged via merge commit
  `9d70f592939156e5418a8ae706854868775009a7`. Merge-commit CI independently re-fetched via the GitHub
  API: check run `93857673735`, `status: completed`/`conclusion: success`.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **110 decisions, `issues == ()`**, reconciling exactly against `governance/decisions.yaml`'s own 110
  rows. `XASSET-0001` through `XASSET-0013` and `CONTENDER-0001` through `CONTENDER-0003` all present.
  **`XASSET-0014` independently confirmed the next unused identifier** — zero matches anywhere in
  `governance/decisions.yaml` or via full-repository grep.
- **`XASSET-0012` and `XASSET-0013` read directly, in full** — decision files and `XASSET-0012`'s own
  supporting artifact (not summarized from memory or from the directive's own paraphrase). Their
  Stage 1/Stage 2 content — the six-sleeve taxonomy, the two record types, the closed four-value
  `primary_disposition` vocabulary, the closed three-member `secondary_conditions` set, the
  zero-numeric-field posture, the `sleeve_subject_scope`/abstention-roll-up mechanisms, the
  forbidden-language boundaries, and — critically — `XASSET-0012` §10's own explicit statement that
  "a sleeve profile or relationship record, however complete, creates no allocation, weight,
  eligibility, or trade authority on its own" and that Stage 4 is "future policy adoption / portfolio
  selection, **if separately authorized**" — is the exact controlling text this filing builds Stage 4
  on top of, by reference, without redesigning any of it.
- **`XASSET-0001` read directly, in full**, confirming this filing's Stage 4 mechanism sits entirely
  inside §E's "Level 1 — sleeve allocation" layer (never Level 2), respects §J's explicit sequencing
  rule that "sleeve-level versus instrument-level targets... are sequentially dependent and must not
  be decided in the same filing," and does not authorize step 9 ("sleeve-level candidate targets") of
  §J's own dependency-ordered roadmap — this filing sits strictly between the completed step 8
  (`XASSET-0012`/`XASSET-0013`/`PR #303`) and the still-fully-unauthorized step 9.
- **Every sealed synthesis record independently re-read this session, not trusted from any prior
  summary**: all six `sleeve_profile` records (`equity`, `fund_broad_market`, `fund_gld_defensive`,
  `crypto`, `cash_reserve`: `evidence_coverage_profile: substantially_computed_with_disclosed_gaps`;
  `debt_reduction`: `evidence_coverage_profile: forced_abstention`) and all seven sealed
  `sleeve_relationship` records (`cash_reserve`↔`debt_reduction`: `unable_to_determine`;
  `cash_reserve`↔`equity`, `debt_reduction`↔`equity`, `equity`↔`fund_gld_defensive`:
  `role_preserving`; `crypto`↔`equity`, `equity`↔`fund_broad_market`: `stronger_evidence_maturity`
  favoring `equity`; `crypto`↔`fund_gld_defensive`: `coexistence_supported`) — exact match to the
  directive's own stated expected values, confirmed by directly opening every one of the thirteen
  sealed YAML files, not by grep or summary.
- **`operations/WORKSTREAMS.yaml`'s `WS-0014` full live entry independently re-read**: `status:
  proposed`, `priority: secondary`, `dependencies: [WS-0005]`. Forty-seven milestone gates recorded
  through `xasset0013-level1-synthesis-schema-level-coverage-extension` (`status: in_progress`,
  `pr: null`) — stale as of this session's start, since `PR #303` is, in fact, fully merged (see
  above); §F below synchronizes it without editing any prior gate's own text. `active_branch:
  claude/level1-synthesis-implementation-qzgpua`, `active_pr: null`, `last_verified_main_sha:
  cfea220c82bae310f2412804a204e85f257a2782` — one merge behind the current tip; also synchronized.
  The `roadmap_preservation` field's own sequencing text (finish missing evidence → cross-asset
  synthesis → provisional sleeve/instrument sizing → descriptive risk analysis/targeted backtests →
  ... → unlevered testing → margin/leverage research → monitoring/sell discipline → final
  integration/audit) is read directly and cited by reference in the supporting artifact §17 — not
  edited by this filing.

### Correction history (this filing, same PR)

**Bounded correction, independent exact-head review `pullrequestreview-4909703610` (anchored to the
original head `e246ea77ae6292d5a1dcc4ce652885e93ec153c7`, base unchanged), 0 BLOCKING / 1 MAJOR / 0
MINOR / 4 non-actionable NOTE, CHANGES REQUIRED:**

1. **MAJOR (two connected parts), resolved.** **Part A**: `fund_broad_market` could not reach Axis
   A's `function_confirmed_distinct` value under the original evidentiary-basis rule — its only
   sealed relationship record (`equity_fund_broad_market.yaml`) resolves `stronger_evidence_
   maturity`, mechanically barred from supplying Axis A grounds, and the doctrine-citation path was
   restricted, by the original §14, to `debt_reduction` alone — directly contradicting the original
   §10's own asserted outcome that overlap disclosure "must never force `fund_broad_market`'s Axis A
   below `function_confirmed_distinct`," a claim justified there by citing SPY's own `targets.yaml`
   weight, an individual-instrument fact not among the design's own stated evidentiary bases.
   **Resolved**: a new third Axis A evidentiary basis (structural `targets.yaml`-destination-category
   membership — categorical, sleeve-level, mechanically-checkable, never an individual instrument's
   weight, never a relationship record, never an evidence-maturity value), independently confirmed
   available to `equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto`, and `cash_reserve` (the
   five sleeves with a live `targets.yaml` row per `XASSET-0012` §2), and unavailable to
   `debt_reduction` (no `targets.yaml` row exists). The existing doctrine-citation basis is also
   generalized — no longer restricted to `debt_reduction` alone, available to any sleeve with a
   genuine, directly-quotable `CLAUDE.md` passage, never a fabricated one. §10's specific outcome
   claim is corrected, not merely re-justified, to rely on the new structural basis rather than the
   withdrawn instrument-weight citation. **Part B**: Axis C's original rule inspected only
   relationship records that exist, with no mechanism distinguishing a sealed-but-unresolved pair
   (which correctly blocks) from a pair that was simply never researched (which, under the original
   rule, silently did not block) — inverting `XASSET-0012` §5.2's own "no absence of evidence may
   silently become favorable" principle. **Resolved**: a new per-sleeve relationship-coverage-ledger
   mechanism (supporting artifact §5.1) classifying every one of a sleeve's five possible relationship
   pairs as `sealed_determined`, `sealed_unresolved`, or `deferred_disclosed` (the last drawn only
   from `XASSET-0013` §E's own eight explicitly-named, closed deferred-pair set — never a silently
   invented ninth category), with a `deferred_disclosed` pair capping Axis C at
   `sizing_conditionally_ready` at most, strictly below what a `sealed_unresolved` pair forces
   (`sizing_blocked`) but never treated as equivalent to a clean, fully-covered sleeve. A new eleventh
   sizing-gate condition requires this ledger fully populated for every sleeve before numeric Level 1
   sizing may even be authorized to begin. **Neither resolution weakens the `stronger_evidence_
   maturity` non-influence rule anywhere** — the new structural basis reads no relationship record of
   any kind and is trivially immune to the counterfactual-masking test; a defensive presence-
   independent regression guard was added to the future validator specification per the review's own
   non-blocking NOTE. Full correction narrative, with every affected subsection individually marked,
   in the supporting artifact (preamble plus §§3.2, 3.3, 5.1, 6, 7.1, 7.2, 9, 10, 12, 14, 15, 16, 20,
   21, 22 — the last two newly added, the old §22 "Sequence" renumbered to §23).
2. **Internal-consistency pass, disclosed alongside the MAJOR, not itself a separate finding.** While
   resolving the MAJOR, this session independently found and corrected thirteen pre-existing internal
   cross-reference errors in the supporting artifact (section numbers that pointed to the wrong
   section — e.g. "§12 item 5" where "§21 item 5" was meant, "§18" where "§17" was meant) — none of
   these were part of the review's own stated finding, but each was a genuine defect a future reader
   would have tripped over; fixed as part of the same bounded pass rather than left for a future
   session to rediscover.

All four non-actionable NOTEs (the `roadmap_preservation` field's own pre-existing, not-this-PR's-to-
fix omission of item (10) from its sequencing chain; §7.1's imprecise "only sleeve today" framing,
independently corrected above as part of Part A's own resolution since the same subsection was already
being edited; the ten-condition-gate's own mild, harmless overlap between conditions 4 and 9; the
counterfactual-masking proof's own defensive-strengthening suggestion, implemented above as new
validator item 24) are addressed or carried forward exactly as the review itself characterized them —
none required independent resolution beyond what Part A/B's own corrections already provided.

Exact correction-delta file inventory: `governance/audits/WS0014_LEVEL1_POLICY_ADOPTION_
METHODOLOGY_DESIGN_20260811.md` (substantive — the corrections above), `governance/decisions/
XASSET-0014-*.md` (this section, plus §B/§D/§H/§J summary updates below to match).

## Decision

### A. What this filing does — Stage 4a methodology design only

This filing designs, as text only — not an authorization to populate any record, not a role
disposition, not an eligibility disposition, not a sizing-readiness disposition, not a numeric weight
of any kind — the methodology for a future, separately authorized Stage 4 policy-adoption mechanism
that converts the sealed, descriptive Level 1 sleeve-synthesis evidence (`XASSET-0012`/`XASSET-0013`,
`PR #303`) into governed, non-numeric, sleeve-level policy findings. Full field-by-field design in the
supporting artifact.

### B. Three separated axes, never collapsed into one verdict

- **Axis A — Portfolio Function Status** (`portfolio_function_status`): does this sleeve represent a
  genuine, distinct portfolio function worth carrying forward, eligible for later sizing
  consideration? Closed, three values: `function_confirmed_distinct` / `function_status_unresolved`
  / `unable_to_determine`. Deliberately **not** a four-value vocabulary — no value asserting sleeve
  redundancy exists, because Stage 1–3's own closed `primary_disposition` vocabulary structurally
  cannot produce a redundancy finding today; inventing an unreachable fourth value would be the
  categorical-schema equivalent of `NUM-0001`'s "provisional guardrail no evidence supports"
  anti-pattern. `function_confirmed_distinct` requires one of **three** lawful evidentiary bases,
  corrected and extended by this filing's own bounded correction: a sealed relationship-record
  finding; a directly-quoted `CLAUDE.md` doctrine citation (now available to any sleeve with a
  genuine passage, no longer `debt_reduction`-restricted); or a new structural
  `targets.yaml`-destination-category-membership basis (categorical, sleeve-level, never an
  individual instrument's own weight) — closing the gap that left `fund_broad_market` with zero
  lawful basis under the original design. Full reasoning in supporting artifact §3/§3.1/§3.2/§3.3.
- **Axis B — Capital Eligibility** (`capital_eligibility_status`): is the sleeve's own governed
  evidence base mature enough to be considered as a target-proposal candidate at all? Closed, two
  values, **mechanically derived, never authored**: `eligible_for_target_consideration` /
  `not_yet_eligible`, computed directly from the sleeve's own sealed `evidence_coverage_profile`.
  Deliberately carries **no** abstention value — a pure function of an already-fully-determined input
  needs none. Full reasoning in supporting artifact §4.
- **Axis C — Sizing Readiness** (`sizing_readiness_status`): is the sleeve, and every relationship
  bearing on it, mature enough right now to proceed toward numeric Level 1 work? Closed, three
  values: `sizing_ready` / `sizing_conditionally_ready` / `sizing_blocked`, mechanically derived from
  Axes A and B plus each named relationship record's own current disposition, secondary conditions,
  and — added by this filing's own bounded correction — a per-sleeve relationship-coverage ledger
  (§5.1) distinguishing a sealed-and-determined pair from a sealed-but-unresolved one from a
  deferred-but-disclosed one, so a merely unresearched pair can never be treated more favorably than
  an honestly-disclosed `unable_to_determine` finding. Full reasoning in supporting artifact §5/§5.1.

These three axes are never collapsed into a single field. `debt_reduction`'s own live sealed evidence
is the concrete case that demonstrates why: it can be simultaneously role-legitimate (Axis A) and
sizing-blocked (Axis B/C) — a single verdict field could represent only one of those two true facts.
Supporting artifact §7.1 traces this mechanism, illustratively only; §7.2 (new) traces the identical
demonstration for `fund_broad_market`; no disposition is adopted by this filing for either sleeve or
any other.

### C. `stronger_evidence_maturity` boundary — mechanically prohibited from driving any axis

Restated as an operative rule, not narrative: no Axis A, B, or C computation may read
`favored_sleeve_id`. A lower-maturity sleeve (`debt_reduction`, `fund_broad_market` after this
correction) may still reach `function_confirmed_distinct`; a higher-maturity sleeve (`equity`) may
still fail Axis C under future evidence. The future implementation must build a
counterfactual-masking non-influence proof — every sleeve's axis values recomputed with every
`stronger_evidence_maturity` relationship record's `favored_sleeve_id` masked must be byte-identical
to the unmasked computation — plus, added by this filing's own bounded correction, a defensive
regression guard proving the mere *presence* of a `stronger_evidence_maturity` disposition (not only
its `favored_sleeve_id` value) cannot influence any axis. The new structural Axis A basis (§B above)
reads no relationship record of any kind and is trivially immune to both tests by construction. Full
design in supporting artifact §6.

### D. `role_preserving`/`coexistence_supported` boundary

May supply Axis A's evidentiary basis and contribute Axis C caveats. May never guarantee a positive
target, determine target size, prevent future exclusion under later evidence, or imply equal
weighting. Every Axis A/B/C value is a live-derived computation over currently-sealed evidence, never
a permanent lock. Full detail, including the `fund_broad_market`/`equity` overlap-coordination
treatment (a disclosed caveat only, never a silent subtraction — corrected by this filing's own
bounded correction to rely on the new structural basis rather than an individual instrument's own
`targets.yaml` weight, which was never a valid Axis A input) and the preserved `crypto`/
`fund_gld_defensive` findings (unmodified, no crypto or GLD target inferred), in supporting artifact
§7, §7.1, §7.2, §10, §11.

### E. Abstention, `debt_reduction`, and `cash_reserve` — no answer forced merely because the schema requires one

No Axis A/B/C value may ever be set to avoid an empty field. `unable_to_determine` relationship
results, `forced_abstention` profile states, and every relationship-record secondary condition each
propagate into required, non-empty disclosure fields (`abstention_reason`, `blocking_evidence[]`),
never silently absorbed — and, added by this filing's own bounded correction, a merely-deferred
(never-researched) relationship pair is likewise never silently treated as clean, per the new
per-sleeve relationship-coverage ledger (§5.1). `debt_reduction`'s illustrative mechanism trace
(supporting artifact §7.1) shows it can independently reach `function_confirmed_distinct` on Axis A
(via its sealed `role_preserving` relationship finding alone — `CLAUDE.md`'s own Portfolio Doctrine
supplies an independent, available-but-non-load-bearing second basis for it specifically, corrected
per the review's own non-blocking NOTE) while being mechanically forced to
`not_yet_eligible`/`sizing_blocked` on Axes B/C (its own `forced_abstention` evidence coverage) —
both facts stay visible; neither the schema nor this filing forces a single answer. `cash_reserve` is
represented operationally as one combined family, reusing — not reopening — `XASSET-0008`'s own
principal-directed provenance finding, with a mandatory rationale field explicitly preserving the
underlying `CASH`/`RESERVE` consolidation question as still open. Full detail in supporting artifact
§8, §9.

### F. Level 1 / Level 2 boundary, zero numeric fields, no contender/QQQ reopening

Stage 4 remains sleeve-level only — no individual equity, fund, or coin's own weight, target, or size
may be named by any Stage 4 record; the existing `XASSET-0012` §9 item 9 leakage scan is reused
unmodified. Stage 4 carries no numeric field of any kind — no weight, percentage, score, rank,
confidence number, or range, matching every prior comparison-shaped schema in this repository. This
design operates exclusively on the sealed six-sleeve, seven-relationship population — `VRT`/`WMT`,
the remaining 82 contender-registry entries, and `QQQ` are not reopened, restated not narrowed or
widened from `XASSET-0012` §7. A hash-staleness detection mechanism (already required for every
structural reference) suffices to flag a Stage 4 record whose underlying evidence is later refreshed
— no new re-synthesis trigger is invented. Full detail in supporting artifact §12, §13, §20.

### G. Exact future Stage 4c deliverable — one record per sleeve, up to six

`intelligence/level1_sleeve_synthesis/policy_adoption/<SLEEVE_ID>.yaml`, plus one
`COHORT_MANIFEST.yaml` — a new, third sub-namespace parallel to (never merged with) `profiles/` and
`relationships/`, matching this repository's own settled "different schema shape, different,
cleanly separated directory" convention. A single whole-portfolio decision file was considered and
rejected on the identical grounds `XASSET-0005`'s own Alternatives Considered section already applied
to its own schema. Full field-by-field design in supporting artifact §14.

### H. Gate to numeric Level 1 sizing

Eleven explicit, none satisfied by this filing, conditions that must all hold before a future,
wholly separate, explicitly authorized filing may begin numeric Level 1 sleeve-level sizing
(`XASSET-0001` §J step 9) — spanning this filing's own merge and independent review, a future Stage
4b content-authorization filing, a future Stage 4c implementation covering every authorized sleeve,
full disclosure of every blocking reason (including `debt_reduction`'s own eventual disposition,
`cash_reserve`'s consolidation-non-settlement note, and — the eleventh condition, added by this
filing's own bounded correction — every sleeve's own relationship-coverage ledger fully populated
with zero deferred pair silently treated as clean), the counterfactual non-influence proof, and a
reviewed, passing Stage 4 validator. Satisfying all eleven is necessary, never sufficient, for that
future authorization — this filing does not itself authorize numeric sizing under any circumstance.
Full eleven-point list in supporting artifact §15.

### I. Allocation-check, risk/backtest, chart, and margin/debt sequencing — restated, not invented

A real, deployment-relevant allocation check remains downstream of Stage 4 adoption, Level 1 numeric
sizing, Level 2 instrument sizing, risk/overlap validation, and unlevered-portfolio validation, in
that order; `OPS-0007` §5's own narrow scenario-only allocation-check bridge is not reactivated,
expanded, or referenced as a shortcut. Risk/backtest sequencing reuses `operations/WORKSTREAMS.yaml`'s
own already-recorded `roadmap_preservation` order exactly — targeted backtests are recorded as
occurring **after** provisional sizing, to challenge and refine it, not as a universal precondition to
any sizing at all; this filing does not invent a stricter sequencing than repository doctrine already
states. Chart evidence remains strictly downstream of membership/eligibility/readiness/target
determination, restating `XASSET-0001` §G and `TIER-0003` unweakened. The unlevered portfolio must be
evidenced and judged sound before any margin/leverage research or deployment policy question is
revisited; the 1.8x leverage cap and 30% buffer floor remain unchanged. Full detail in supporting
artifact §16–§19.

### J. Future validator/test specification

A future, separately authorized Stage 4c implementation must build a dedicated validator (or a
clearly separated Stage 4 section of the existing `level1_sleeve_synthesis_validator.py` module),
with zero import coupling to `allocate.py`/`margin_state.py`, covering: closed schema with extra-key
rejection at every level; live hash re-computation of every structural reference; mechanical Axis B
re-derivation; the `stronger_evidence_maturity` counterfactual-masking non-influence proof plus a
defensive presence-independent regression guard (new); mechanical Axis C consistency checks,
including relationship-coverage-ledger consistency; a zero-numeric-fields scan (digit and
spelled-out-magnitude both); a zero-score/rank/composite-key scan; the Level 1/Level 2 leakage scan;
a directive/trading-language scan; a chart-domain-terminology scan; the `CASH`/`RESERVE`-distinction-
language scan; **Stage 4's own materially separate bounded-conclusion scan** (distinct from
Stage 1–3's blanket `XASSET-0012` §8.1 eligibility-language ban, since Stage 4 is explicitly designed
to represent a bounded, closed-vocabulary role/eligibility/readiness judgment — what remains barred
is numeric magnitude, execution/trade directives, over-strong free-text claims, and Level 2 leakage);
the comparative-investment-superiority scan; adversarial test coverage for ordering, negation,
punctuation, conjunction, active/passive voice, euphemistic paraphrase, hidden-sizing phrasing, and
score/rank language, each with mandatory false-positive guards; a zero-contender/QQQ-citation scan; a
protected-path/byte-identity test across all thirteen input layers plus the thirteen Stage 1–3
records themselves; manifest reconciliation; non-cascading abstention discipline; and, added by this
filing's own bounded correction: a Basis 3 mechanical check (live `targets.yaml` cross-check, with
rejection of any citation referencing evidence-maturity or per-instrument-weight fields); a
generalized Basis 2 structural-non-emptiness check; and relationship-coverage-ledger completeness
tests (exact five-pair enumeration per sleeve, live cross-reference against the sealed seven and
`XASSET-0013` §E's own disclosed eight, and the `deferred_disclosed`-caps-at-`sizing_conditionally_
ready` rule). Full twenty-four-point specification in supporting artifact §21, plus a new
axis-interaction adversarial-case table in §22.

### K. Stage 4 sub-sequence — never collapsed

1. **Stage 4a — this design** (`XASSET-0014`). Methodology only.
2. **Stage 4b — future content authorization.** Names the exact sleeve population a Stage 4c
   implementation may populate.
3. **Stage 4c — future implementation/population.** Builds the validator and populates exactly the
   records Stage 4b authorized.
4. **Numeric Level 1 sizing — its own separate, later, wholly distinct future authorization**, gated
   on §H's eleven conditions, not a Stage 4 sub-step at all.

### L. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry gains exactly one additive milestone gate,
`xasset0014-level1-policy-adoption-methodology-design` (`status: in_progress`, `pr: null` — this
filing does not mark its own unmerged work complete), plus one additive Lane M gate,
`xasset0013-implementation-post-merge-verification`, recording — without editing the
`xasset0013-level1-synthesis-implementation`/`-bounded-correction`/`-bounded-correction-round-2`/
`-bounded-same-class-audit`/`-schema-level-coverage-extension` gates' own historical text — that
`PR #303` is fully merged, confirmed above, and that post-merge CI on `main` is green. The
workstream's ordinary self-reference fields (`active_branch`, `active_pr`, `last_verified_main_sha`,
`last_verified_date`) are updated to this filing's own live state. No prior gate's own text is
edited. `WS-0014`'s own `status: proposed`/`priority: secondary`/`dependencies: [WS-0005]` are
unedited. `WS-0005` and `WS-0015` are unaffected by this filing.

### M. Explicit non-authorization

This filing authorizes **methodology design text only**. It does not authorize:

- population of any Stage 4 (`policy_adoption`) record of any kind, for any sleeve;
- any actual role, eligibility, or sizing-readiness disposition for `equity`, `fund_broad_market`,
  `fund_gld_defensive`, `crypto`, `cash_reserve`, or `debt_reduction`;
- any sleeve weight, sleeve budget, or sleeve allocation percentage of any kind;
- any instrument weight or Level 2 sizing decision of any kind;
- any portfolio in/out, eligibility, promotion, or demotion decision beyond the bounded, categorical,
  non-numeric Axis A/B/C schema this filing designs;
- resolution of `debt_reduction`'s own economic-assessment forced-abstention state, or of the
  `CASH`/`RESERVE` consolidation question (`XASSET-0008` §N, not reopened);
- any broader contender-registry sweep, `VRT`/`WMT` capital-priority conclusion, or `QQQ`/ETF-scope
  revisit;
- any real, live, scenario, or deployment-relevant allocation check;
- any chart evidence, buy-ladder work, backtesting, monitoring, or sell-discipline rule;
- any allocator, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `margin_state.py`, or `levels.py` change;
- any hardening, expansion, or weakening of any existing repository validator, including
  `level1_sleeve_synthesis_validator.py`;
- any dashboard change;
- any tier/target/holdings/gate/cap/cluster/order/trade change of any kind.

## Rationale

`XASSET-0012` §10 defined Stage 4 as "future policy adoption / portfolio selection, if separately
authorized" and stated explicitly that a sleeve profile or relationship record, "however complete,
creates no allocation, weight, eligibility, or trade authority on its own" — deliberately leaving
Stage 4's own mechanism entirely undesigned so that the descriptive Stage 1–3 methodology would not be
pressured, under evidentiary or scheduling pressure, into quietly answering an eligibility question it
explicitly declined to answer (`XASSET-0012`'s own Alternatives Considered section records that
rejection directly). Now that Stage 3 is complete and sealed (`PR #303`), that gap is load-bearing:
without a designed Stage 4 mechanism, any future session under pressure to "just produce a number" has
no governed path to do so honestly, and risks either forcing a premature numeric answer or collapsing
role/eligibility/readiness into one field that cannot represent cases like `debt_reduction`'s own
genuine role-legitimate-but-evidence-blocked state. This filing closes that specific, now
load-bearing gap, following the identical "define, then later authorize implementation" pattern this
repository has used at every prior stage of this same Level 1 undertaking (`XASSET-0012` before
Stage 2; `XASSET-0013` before Stage 3) and at every prior milestone-scale undertaking generally
(`TIER-0001`/`TIER-0002` before Milestone 6; `REL-0001` before Milestone 4's content).

Designing three independent, non-collapsible axes rather than one status field follows this
repository's own repeated precedent for separating a primary judgment from its own gating conditions
(`TIER-0009`'s eight-area `primary_status` plus `secondary_conditions`; `VALUATION-0006`'s
`result_status` plus `conflicts_carried_forward`) — generalized here to three fully independent axes
because, unlike those precedents' single-primary-plus-flags shape, Stage 4's three questions
(function, eligibility, readiness) are not merely "one judgment plus caveats" but three separately
reachable, separately blocking findings, exactly as `debt_reduction`'s own live evidence demonstrates.

Deriving Axis B mechanically, with zero drafting-session discretion and no abstention path of its
own, follows this repository's own repeated, hard-won lesson that a field asserting a status must be
independently re-derivable by the validator from the underlying data it claims to summarize, never
merely schema-shape-checked — the exact defect class `reconciliation_validator.py`'s and
`etf_classification_validator.py`'s own disclosed MINOR findings both named, applied here from first
design rather than discovered post-review.

## Alternatives Considered

**Collapse role, eligibility, and sizing readiness into one closed-vocabulary field.** Rejected —
`debt_reduction`'s own live sealed evidence (a real `role_preserving` finding against `equity`,
combined with a fully forced-abstained economic-assessment layer) is a concrete, present-day case a
single field cannot represent without silently discarding one of two true, independently-governed
facts. This is not a hypothetical edge case invented to justify a more complex design — it is the
directive's own named "critical case," live today.

**Include a fourth Axis A value representing a genuine sleeve-redundancy finding.** Rejected —
Stage 1–3's own closed `primary_disposition` vocabulary (`XASSET-0012` §5.1) contains no value that
asserts one sleeve's function is fully subsumed by another's; `stronger_evidence_maturity` is
explicitly, mechanically restricted to an evidence-completeness finding only. A Stage 4 value no
live or currently-reachable Stage 1–3 evidence could ever populate would be an unused escape hatch,
the categorical-schema analogue of the "provisional guardrail no evidence supports" pattern
`NUM-0001` already names as its own defect class for numeric parameters.

**Give Axis B (Capital Eligibility) its own `unable_to_determine` abstention value, matching Axis A
and Axis C for uniformity.** Rejected — `evidence_coverage_profile`, the field Axis B is a pure
function of, is itself already a mechanically-derived, always-populated, closed four-value field with
no abstention state of its own (a profile that could not be evaluated at all would fail to seal in
the first place). Adding an independent abstention path to a field that is a pure function of an
already-fully-determined input would relocate, not resolve, uncertainty that already lives one layer
down — inconsistent with this repository's own "mechanically derived, never self-declared" discipline
applied to its logical conclusion.

**Design and authorize Stage 4b (content authorization) and Stage 4c (implementation) in this same
filing**, rather than deferring them to their own future units. Rejected outright per the directive's
own explicit instruction and `XASSET-0012`→`XASSET-0013`'s own directly analogous precedent one layer
down: a schema must exist and be independently reviewed before it is applied to real sealed evidence
producing an actual role/eligibility/readiness finding for a real sleeve.

**Reuse `XASSET-0012` §8.1's existing eligibility/inclusion-language scan verbatim for Stage 4's own
free-text fields**, rather than designing a materially separate "bounded-conclusion" scan. Rejected —
Stage 1–3's scan exists specifically because Stage 1–3 does not decide eligibility at all; applying
that same blanket ban to Stage 4, whose entire purpose is to represent exactly that kind of bounded,
closed-vocabulary judgment, would make Stage 4's own schema fields unusable in their own supporting
rationale text. Stage 4 instead needs, and this design specifies, a narrower scan barring only what
remains illegitimate even in a policy-adoption context: numeric magnitude, execution/trade
directives, and free text claiming more than the record's own closed-vocabulary fields support.

## Consequences

**Changes as a direct result of this decision**: the existence of one retained Stage 4 methodology —
three independent, non-collapsible axes (Portfolio Function Status, Capital Eligibility, Sizing
Readiness), each with its own closed vocabulary and derivation rule, Axis A now supported by three
lawful evidentiary bases (relationship-record finding, generalized doctrine citation, and a new
structural `targets.yaml`-destination-category basis) and Axis C now incorporating a per-sleeve
relationship-coverage ledger; one retained future record schema
(`intelligence/level1_sleeve_synthesis/policy_adoption/<SLEEVE_ID>.yaml`, extended with a new
`relationship_coverage_ledger[]` field); one retained, now eleven-condition gate that must hold
before numeric Level 1 sizing may even be authorized to begin; one retained, now twenty-four-point
future validator/test specification, including a materially separate bounded-conclusion scan
distinct from Stage 1–3's own eligibility-language ban and a new axis-interaction adversarial-case
table; two illustrative, non-adopted mechanism traces (`debt_reduction`, `fund_broad_market`) showing
how each sleeve's own live evidence would be handled without forcing a premature answer; one bounded
correction round resolving a single MAJOR finding (in two connected parts) from an independent
exact-head review, plus thirteen internal cross-reference corrections found during the same
consistency pass; confirmation, via two additive `operations/WORKSTREAMS.yaml` gates, that
`XASSET-0013`'s own authorized implementation (`PR #303`) is fully merged and post-merge CI on `main`
is green; four rejected alternatives recorded for future reference.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin
behavior; the 1.8x leverage cap or 30% margin-buffer floor; any Company, Theme, relationship,
classification, valuation-archetype, valuation-evidence, valuation-result, ETF-classification,
crypto-classification, functional-doctrine, overlap-model, economic-assessment,
instrument-economic-assessment, contender-evaluation, `sleeve_profile`, or `sleeve_relationship`
record's content; any current cash balance, reserve level, GLD holding, or margin-debt figure;
`WS-0005`'s completed, `status: complete` state; `WS-0014`'s own `status: proposed`/`priority:
secondary` (this filing adds two additive gates, it does not begin execution or change the
workstream's own status/priority); or any brokerage, trading, or order-related capability. Completing
this unit does not itself populate any Stage 4 record for any sleeve, does not authorize a Stage 4b
content-authorization filing or a Stage 4c implementation, does not authorize numeric Level 1 or
Level 2 sizing of any kind, and does not authorize any allocation check — each requires its own
separate, explicit, future principal authorization, per `XASSET-0012` §10's own unedited four-stage
sequence and `XASSET-0001` §J's own dependency-ordered roadmap.
