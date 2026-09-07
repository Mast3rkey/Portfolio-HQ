---
decision_id: XASSET-0015
date: 2026-08-11
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0007, TIER-0009, REL-0001, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0012, XASSET-0013, XASSET-0014, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, VALUATION-0006, VALUATION-0007, CONTENDER-0001, CONTENDER-0002, CONTENDER-0003, PHQ-2026-01, PHQ-2026-02, NUM-0001]
supporting_artifact: null
file: governance/decisions/XASSET-0015-ws0014-level1-policy-adoption-content-authorization.md
---

## Context

### Authority for this unit

The human repository principal explicitly authorized exactly **one bounded Stage 4b governance
filing** naming the exact sleeve population a future Stage 4c implementation may populate under
`XASSET-0014`'s already-accepted, already-merged Stage 4a policy-adoption methodology. This filing
is **authorization only** — it populates no `policy_adoption` record, assigns no sleeve an actual
Portfolio Function Status, Capital Eligibility, or Sizing Readiness disposition, creates no numeric
weight or target of any kind, and authorizes no allocation check. It is Stage 4b of `XASSET-0012`
§10's own four-stage sequence (Stage 1 — methodology, complete; Stage 2 — content authorization,
complete; Stage 3 — implementation, complete; Stage 4 — policy adoption, itself sub-staged by
`XASSET-0014` into Stage 4a — methodology, complete; **Stage 4b — content authorization, this
unit**; Stage 4c — future implementation), mirroring `XASSET-0013`'s own identical role for Stage 2
one layer down.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/stage-4b-policy-adoption-auth-0wgz6j`, working tree clean at session start.
- **`origin/main` fetched and reconciled.** Local `HEAD` and `origin/main` both confirmed identical
  at `f3e067fd217ef4ea4800951d663f7c89e0c7d257` — matching the directive's own stated SHA exactly.
  This is `PR #304`'s own merge commit (parents `9d70f592939156e5418a8ae706854868775009a7` — the
  base, `PR #303`'s own merge commit — and `ab93baf3e73a7237bae6c673fb45eda26c62a86f` — `PR #304`'s
  own head), independently re-confirmed via `git log --pretty='%H %P'`.
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #304`'s full lifecycle independently re-verified via the GitHub API, not assumed**: `merged:
  true`, `merged_by: Mast3rkey`, base `9d70f592939156e5418a8ae706854868775009a7`, two commits (one
  original submission plus one bounded-correction round, independently confirmed via `git log`
  showing `e246ea7` then `ab93baf`), merged via merge commit
  `f3e067fd217ef4ea4800951d663f7c89e0c7d257`. Both check-run layers independently re-fetched via the
  GitHub API: the PR head's own check run (`93897989474`, anchored to `ab93baf`) and the merge
  commit's own separate, distinct check run (`93905807614`, anchored to `f3e067f` directly) — both
  `status: completed`/`conclusion: success`.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **111 decisions, `issues == ()`**, reconciling exactly against `governance/decisions.yaml`'s own
  111 rows and `PR #304`'s own stated figure. `XASSET-0001` through `XASSET-0014` and
  `CONTENDER-0001` through `CONTENDER-0003` all present. **`XASSET-0015` independently confirmed the
  next unused identifier** — zero matches anywhere in `governance/decisions.yaml` or via
  full-repository grep.
- **`XASSET-0014` read directly, in full — decision file and its own supporting artifact**
  (`governance/audits/WS0014_LEVEL1_POLICY_ADOPTION_METHODOLOGY_DESIGN_20260811.md`), not summarized
  from memory or from the directive's own paraphrase. Its Stage 4a methodology — the three
  independent, non-collapsible axes (Portfolio Function Status, Capital Eligibility, Sizing
  Readiness), the three lawful Axis A evidentiary bases (relationship-record finding; generalized
  `CLAUDE.md` doctrine citation; the new structural `targets.yaml`-destination-category basis), the
  mechanical Axis B derivation, the Axis C mechanism incorporating the per-sleeve relationship-
  coverage ledger (`sealed_determined` / `sealed_unresolved` / `deferred_disclosed`), the
  `stronger_evidence_maturity` mechanical-prohibition rule, the `cash_reserve` non-settlement
  requirement, the Level 1/Level 2 boundary, the zero-numeric-field posture, the exact future Stage
  4c deliverable shape, the eleven-condition gate to numeric Level 1 sizing, and the twenty-four-
  point future validator/test specification — is the exact controlling text this filing binds to by
  reference below, without redesigning any of it.
- **`XASSET-0013` and `XASSET-0012` (decision files and `XASSET-0012`'s own supporting artifact) read
  directly, in full**, confirming the exact seven sealed `sleeve_relationship` pairs, the exact eight
  deliberately deferred pairs (grouped in three disclosed classes), and `XASSET-0012` §2's own fixed
  six-sleeve-to-`asset_class` mapping table — the governing input to `XASSET-0014`'s own Basis 3.
- **`XASSET-0001` §E/§J re-read**, confirming this filing sits entirely inside the Level 1
  sleeve-allocation layer, authorizes no Level 2 instrument-level content of any kind, and does not
  authorize `XASSET-0001` §J step 9 (numeric Level 1 sizing) — `XASSET-0014` §15's own eleven-
  condition gate remains only partially advanced by this filing (condition 2 of eleven; see §M
  below), never satisfied in full by it.
- **Every sealed Stage 1–3 synthesis record independently re-opened this session, not trusted from
  any prior summary**: all six `sleeve_profile` records directly read
  (`intelligence/level1_sleeve_synthesis/profiles/{equity,fund_broad_market,fund_gld_defensive,
  crypto,cash_reserve,debt_reduction}.yaml`) — `evidence_coverage_profile` confirmed
  `substantially_computed_with_disclosed_gaps` for the first five and `forced_abstention` for
  `debt_reduction` alone, `record_status: sealed` on all six, matching `XASSET-0014`'s own Preflight
  table exactly, field-for-field. All seven sealed `sleeve_relationship` records directly read
  (`intelligence/level1_sleeve_synthesis/relationships/*.yaml`) — `primary_disposition` and
  `favored_sleeve_id` confirmed to match `XASSET-0014`'s own Preflight table exactly for every pair:
  `cash_reserve_debt_reduction: unable_to_determine`; `cash_reserve_equity: role_preserving`;
  `crypto_equity: stronger_evidence_maturity` (favoring `equity`); `crypto_fund_gld_defensive:
  coexistence_supported`; `debt_reduction_equity: role_preserving`; `equity_fund_broad_market:
  stronger_evidence_maturity` (favoring `equity`); `equity_fund_gld_defensive: role_preserving`. Live
  `targets.yaml` independently re-parsed this session: `asset_class` counts confirmed `equity: 27`,
  `fund: 4` (SPY, VEA, VWO, GLD), `crypto: 3`, `reserve: 1`, `cash: 1` — five of six sleeves carry at
  least one live destination row (`equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto`,
  `cash_reserve`); `debt_reduction` carries zero, confirming `XASSET-0014` §3.2 Basis 3's own stated
  availability/unavailability split exactly.
- **`operations/WORKSTREAMS.yaml`'s `WS-0014` full live entry independently re-read**: `status:
  proposed`, `priority: secondary`, `dependencies: [WS-0005]`. Forty-nine milestone gates recorded
  through `xasset0014-level1-policy-adoption-methodology-design` (`status: in_progress`, `pr:
  null`) — stale as of this session's start, since `PR #304` is, in fact, fully merged (see above);
  §O below synchronizes it without editing any prior gate's own text. `active_branch:
  claude/level-1-policy-adoption-design-9w9gvr`, `active_pr: null`, `last_verified_main_sha:
  9d70f592939156e5418a8ae706854868775009a7` — one merge behind the current tip; also synchronized.
  `intelligence/level1_sleeve_synthesis/policy_adoption/` independently confirmed **absent** — no
  Stage 4b or Stage 4c content exists anywhere in the repository prior to this filing.

## Decision

### A. What this filing authorizes — content-population targeting only, not implementation

This filing authorizes exactly one future, separate, bounded Stage 4c implementation PR to populate
the `policy_adoption` records named below, plus the manifest, validator(s), and test suite
`XASSET-0014` §21 already specifies. It does not itself populate any record, compute any Axis A/B/C
value, cite any evidentiary basis, or produce any role/eligibility/readiness finding. No
methodology field, vocabulary value, derivation rule, or scan design from `XASSET-0014` is
redesigned, expanded, or narrowed by this filing.

### B. Exact Stage 4c population — all six sleeves, none deferred

The future implementation may populate exactly **six** `policy_adoption` records — one per
`sleeve_id`, matching `XASSET-0012` §2's closed six-value taxonomy exactly:

| # | `sleeve_id` |
|---|---|
| 1 | `equity` |
| 2 | `fund_broad_market` |
| 3 | `fund_gld_defensive` |
| 4 | `crypto` |
| 5 | `cash_reserve` |
| 6 | `debt_reduction` |

No sleeve is deferred, omitted, or held back from this population. This determination follows
directly from independently re-verifying, sleeve by sleeve, that every one of the six can be
**lawfully evaluated** under `XASSET-0014`'s own mechanism to a specific, well-defined Axis A/B/C
outcome — including, where the sealed evidence warrants it, an honestly disclosed
`function_status_unresolved`, `not_yet_eligible`, or `sizing_blocked` result — never that every
sleeve is expected to reach a favorable disposition. `XASSET-0014` §5.1's own corrected
relationship-coverage-ledger rule guarantees this mechanically: the seven sealed
`sleeve_relationship` records plus `XASSET-0013` §E's own eight explicitly-named deferred pairs
together account for all fifteen `C(6,2)` possible pairs with zero gap (independently re-verified
this session: `7 + 8 = 15`, matching the closed set exactly) — so no sleeve's Axis C computation can
ever encounter an unaccounted-for pair, and no sleeve is structurally blocked from producing *some*
valid, fully-derived Stage 4c record. **This is the same "default to the full authorized population
unless a sleeve genuinely cannot be evaluated" test `XASSET-0006` already applied for the four
functional-doctrine capital-use types and `XASSET-0013` §B already applied for the six sleeve
profiles** — no sleeve was found here that fails it.

**This filing does not itself determine, adopt, or predict what any sleeve's actual Axis A, Axis B,
or Axis C value will be.** Every scenario described in §C–§E below is a reachability/mechanism
determination only, illustrative and non-adopted, in the same spirit as `XASSET-0014` §§3.3/7.1/7.2/
22's own explicitly-labeled illustrative traces — never a disposition this filing assigns.

### C. Sleeve-by-sleeve evaluability determination

For each sleeve, the question this filing answers is narrow: *can a future Stage 4c drafting session
lawfully reach a fully-derived, non-fabricated Axis A/B/C outcome for this sleeve today, using only
the sealed Stage 1–3 evidence `XASSET-0014` §1 inventories as the sole permitted input?* Not: *is
this sleeve sizing-ready, or likely to be found role-legitimate?*

- **`equity`** — Axis A: two independent lawful bases available (Basis 1 — three sealed
  `role_preserving` findings naming it: `cash_reserve_equity`, `debt_reduction_equity`,
  `equity_fund_gld_defensive`; Basis 3 — live `targets.yaml` `equity` rows, 27, independently
  reconfirmed this session). Axis B: mechanically derived from `evidence_coverage_profile:
  substantially_computed_with_disclosed_gaps` — a closed, always-populated field, zero drafting
  discretion. Axis C: relationship-coverage ledger fully accounted, 5 of 5 pairs `sealed_determined`
  (against every other sleeve), zero `sealed_unresolved`, zero `deferred_disclosed` — the ledger
  itself is complete and evaluable regardless of what Axis A/B ultimately resolve to. **Fully
  evaluable.**
- **`fund_broad_market`** — Axis A: Basis 1 unavailable (its one sealed relationship,
  `equity_fund_broad_market`, resolves `stronger_evidence_maturity`, mechanically barred from
  supplying Axis A grounds by `XASSET-0014` §6); Basis 2 not asserted (no dedicated, directly-
  quotable `CLAUDE.md` passage for this sleeve specifically is identified by either `XASSET-0014` or
  this filing — none is manufactured here either); **Basis 3 available** — live `targets.yaml` `fund`
  rows scoped to SPY/VEA/VWO, independently reconfirmed this session, closing exactly the gap
  `XASSET-0014`'s own bounded correction (Finding MAJOR-1) resolved. A future Stage 4c session may
  cite Basis 3 and reach `function_confirmed_distinct`, or may independently judge the evidence
  insufficient and reach `function_status_unresolved` instead — this filing adopts neither outcome,
  only confirms the evidentiary path to evaluate the question at all now exists. Axis B: mechanically
  derived from `evidence_coverage_profile: substantially_computed_with_disclosed_gaps`. Axis C:
  ledger fully accounted, 1 of 5 `sealed_determined` (against `equity`), 4 of 5 `deferred_disclosed`
  (against `fund_gld_defensive`/`crypto`/`cash_reserve`/`debt_reduction`, `XASSET-0013` §E class 1) —
  a complete, evaluable ledger that mechanically caps this sleeve at `sizing_conditionally_ready` at
  best under §5's own rule, never `sizing_ready`, regardless of Axis A/B. **Fully evaluable, with a
  structurally capped Axis C ceiling disclosed, not concealed.**
- **`fund_gld_defensive`** — Axis A: three independent bases available (Basis 1 — two sealed findings,
  `crypto_fund_gld_defensive: coexistence_supported` and `equity_fund_gld_defensive:
  role_preserving`; Basis 2 — the "GLD does the ballast job bonds would" passage `XASSET-0013` §D
  already cited, available illustratively per `XASSET-0014` §3.2; Basis 3 — live `targets.yaml` `fund`
  row scoped to GLD). Axis B: mechanically derived from `evidence_coverage_profile:
  substantially_computed_with_disclosed_gaps`. Axis C: ledger fully accounted, 2 of 5
  `sealed_determined` (against `equity`, `crypto`), 3 of 5 `deferred_disclosed` (against
  `fund_broad_market`/`cash_reserve`/`debt_reduction`, classes 1–2). **Fully evaluable.**
- **`crypto`** — Axis A: two bases available (Basis 1 — one sealed finding,
  `crypto_fund_gld_defensive: coexistence_supported`; Basis 3 — live `targets.yaml` `crypto` rows,
  BTC/ETH/SOL). Axis B: mechanically derived from `evidence_coverage_profile:
  substantially_computed_with_disclosed_gaps` — note the profile's own already-sealed
  `abstention_index[]` entries (2, including the sleeve-wide `cross_coin_correlation_status:
  not_yet_measured` forced abstention) do not change Axis B's closed-vocabulary derivation, only
  contribute to Axis C's disclosed-caveat trail via the sealed relationship record's own secondary
  conditions. Axis C: ledger fully accounted, 2 of 5 `sealed_determined` (against `equity`,
  `fund_gld_defensive`), 3 of 5 `deferred_disclosed` (against `fund_broad_market`/`cash_reserve`/
  `debt_reduction`, classes 1/3). **Fully evaluable.**
- **`cash_reserve`** — Axis A: two bases available (Basis 1 — one sealed finding, `cash_reserve_
  equity: role_preserving`; Basis 3 — live `targets.yaml` `cash`+`reserve` rows). Axis B: mechanically
  derived from `evidence_coverage_profile: substantially_computed_with_disclosed_gaps`. Axis C:
  ledger fully accounted, 1 of 5 `sealed_determined` (against `equity`), 1 of 5 `sealed_unresolved`
  (against `debt_reduction`, the sealed `unable_to_determine` finding), 3 of 5 `deferred_disclosed`
  (against `fund_broad_market`/`fund_gld_defensive`/`crypto`, classes 1–3) — the presence of a
  `sealed_unresolved` pair is itself a fully-derivable, disclosable Axis C outcome under §5's own
  mechanical rule (forces `sizing_blocked`), not a barrier to evaluation. The mandatory `cash_reserve`
  consolidation-non-settlement note (`XASSET-0014` §9/§14) does not require the underlying `CASH`/
  `RESERVE` question to be resolved before this sleeve can be evaluated — it requires the opposite:
  that the record explicitly disclose the question remains open. **Fully evaluable.**
- **`debt_reduction`** — Axis A: two bases available (Basis 1 — one sealed finding, `debt_reduction_
  equity: role_preserving`, independently sufficient on its own; Basis 2 — the leverage-cap/buffer-
  floor/forced-de-lever doctrine passage `XASSET-0014` §7.1 already illustrates, available but not
  load-bearing given Basis 1 alone suffices); Basis 3 **unavailable** (no `targets.yaml` row exists
  for this sleeve, independently reconfirmed this session — `XASSET-0012` §2 records it as "none
  (margin lever)"). Axis B: mechanically derived from `evidence_coverage_profile: forced_abstention`
  — a closed, always-populated field value, itself a fully-derived, disclosable outcome, not an
  evaluation failure. Axis C: ledger fully accounted, 1 of 5 `sealed_determined` (against `equity`),
  1 of 5 `sealed_unresolved` (against `cash_reserve`), 3 of 5 `deferred_disclosed` (against
  `fund_broad_market`/`fund_gld_defensive`/`crypto`, classes 1–3). **Fully evaluable** — see §D below
  for the dedicated, high-scrutiny treatment this sleeve requires.

### D. `debt_reduction` — high-scrutiny determination, included precisely so the distinction is recorded

`debt_reduction` is **not** deferred merely because its own `evidence_coverage_profile` is
`forced_abstention`, its Axis B computation will very likely mechanically resolve `not_yet_eligible`,
or its Axis C computation will very likely mechanically resolve `sizing_blocked`. Deferring it on
those grounds would defeat the entire purpose `XASSET-0014` was built for: its own Rationale states
explicitly that a single collapsed verdict field "could only represent one of two true facts" for
exactly this sleeve, and its own §7.1 worked illustration exists specifically to demonstrate that
`debt_reduction` can be simultaneously role-legitimate (a real, sealed `role_preserving` finding
against `equity`, independently sufficient for Axis A) **and** evidence-blocked (`forced_abstention`
on Axis B, mechanically forcing `sizing_blocked` on Axis C) — both facts visible at once, neither
silently discarding the other. A Stage 4b filing that excluded `debt_reduction` from the authorized
population specifically because its likely mechanical outcome is unfavorable on two of three axes
would reintroduce, at the population-selection layer, exactly the single-collapsed-judgment failure
mode `XASSET-0014`'s three-axis architecture exists to prevent at the record layer. Including it is
not an act of optimism about its eventual disposition — it is the only way this filing's own
population choice does not itself pre-judge an outcome `XASSET-0014` reserved to Stage 4c.

No missing research is fabricated by including `debt_reduction`: this filing performs no economic-
assessment work of its own, does not close `DEBT_REDUCTION.yaml`'s own forced `assessment_required`
sub-fields (`avoided_borrowing_cost_readiness`, `survivability_and_buffer_benefit_readiness`), and
does not assert that Axis B's eventual mechanical value will resolve favorably or unfavorably — only
that the sleeve's own sealed evidence today is sufficient for a future Stage 4c session to compute
and disclose whatever that mechanical value actually is.

### E. `fund_broad_market` — high-scrutiny determination, Basis 3 confirmed load-bearing and non-automatic

`XASSET-0014`'s own bounded correction specifically repaired Axis A reachability for
`fund_broad_market` by adding Basis 3 (structural `targets.yaml`-destination-category membership).
This filing independently re-verifies, rather than assumes, that the corrected three-basis rule
actually resolves the gap: `fund_broad_market`'s live `targets.yaml` `asset_class: fund` scope,
restricted to SPY/VEA/VWO per `XASSET-0012` §2's own fixed table, is confirmed populated (3 of the 4
live `fund` rows; the fourth, GLD, belongs to `fund_gld_defensive`). Basis 3 is available.

This filing does **not** convert Basis 3 into an automatic positive Axis A result. `XASSET-0014` §3.2
states explicitly that Basis 3 is a categorical, structural-existence check only — it establishes
that the evidentiary *path* to `function_confirmed_distinct` now exists, never that a future Stage 4c
session is thereby required, or even presumptively expected, to reach that value. A future Stage 4c
drafting session evaluating `fund_broad_market` retains full discretion to independently judge the
available evidence — including the sleeve's own single sealed relationship record
(`equity_fund_broad_market: stronger_evidence_maturity`, mechanically excluded from supplying
grounds), the disclosed `overlap_or_duplication_disclosed` coordination flag against `equity`
(`XASSET-0014` §10, a Axis C caveat only, never an Axis A subtraction), and Basis 3's own structural
fact — and may reach `function_confirmed_distinct`, `function_status_unresolved`, or (in the
structurally unreachable-today case per `XASSET-0014` §3.3) `unable_to_determine`, exactly as the
sealed evidence and the mechanism's own rules dictate. Nothing in this filing narrows that
discretion or pre-selects an outcome.

### F. Relationship-coverage ledger readiness — reused, not redesigned

Every sleeve's own relationship-coverage ledger (`XASSET-0014` §5.1/§14) is fully computable by a
future Stage 4c implementation directly from the seven sealed `sleeve_relationship` records and
`XASSET-0013` §E's own eight explicitly-named, closed deferred-pair classification — independently
re-verified this session, pair by pair, against both the live sealed records and `XASSET-0013`'s own
text (§ Preflight above): zero pairs exist outside that closed 7 + 8 = 15 set, so no sleeve's ledger
can ever encounter an unrecognized pair. This filing does not reopen, expand, or reclassify any of
the eight deferred pairs, and does not authorize any new relationship research — the ledger mechanism
itself, exactly as `XASSET-0014` §5.1 designed it, is what a future Stage 4c implementation must
apply mechanically to the population named in §B above; this filing supplies no new ledger content.

### G. `stronger_evidence_maturity` non-influence — restated, not reopened

The mechanical prohibition `XASSET-0014` §6 establishes — no Axis A, B, or C computation may read
`favored_sleeve_id`; a lower-maturity sleeve may still reach `function_confirmed_distinct`; a
higher-maturity sleeve may still fail Axis C — is restated here as a binding condition on the
population this filing authorizes, not redesigned. A future Stage 4c implementation must build the
counterfactual-masking non-influence proof `XASSET-0014` §6/§21 item 5 requires (every sleeve's axis
values recomputed with every `stronger_evidence_maturity` relationship record's `favored_sleeve_id`
masked, confirmed byte-identical to the unmasked computation) plus the defensive presence-independent
regression guard (§21 item 24), across all six sleeves this filing authorizes — including `equity`,
the sleeve both `stronger_evidence_maturity` records currently favor, whose own eventual Axis A/B/C
values must be provably independent of that favored status by the same mechanical test applied to
every other sleeve.

### H. `blocking_evidence[]` / deferred-pair disclosure — restated, not reopened

A future Stage 4c implementation must populate `blocking_evidence[]` (non-empty wherever Axis C
resolves `sizing_blocked` or `sizing_conditionally_ready`), `unresolved_relationships[]` (every
relationship reference whose own `primary_disposition == unable_to_determine`), and the full
`relationship_coverage_ledger[]` (all five pairs per sleeve, per §F above) for **every** sleeve in
the population this filing authorizes — no sleeve, and no individual pair within a sleeve's own
ledger, may be silently treated as clean, favorable, or resolved. A `deferred_disclosed` pair is
never treated as equal to, or better than, a `sealed_determined` one; a `sealed_unresolved` pair is
never treated as equal to, or better than, a `deferred_disclosed` one — the strict severity ordering
`XASSET-0014` §5/§5.1 already establishes is restated, not altered, here. This filing does not
authorize research to close any of the eight deferred pairs (§F above) — every one of them remains
disclosed as deferred in the Stage 4c record of every sleeve it touches.

### I. `cash_reserve` — combined-family treatment restated, no resolution authorized

`cash_reserve`'s future Stage 4c record must carry the mandatory `cash_reserve_consolidation_note`
`XASSET-0014` §9/§14 requires — a non-empty rationale field preserving, in substance, that `CASH` and
`RESERVE` remain an unresolved, undifferentiated combined family (`XASSET-0008` §N's own
principal-directed provenance finding, `CASH_LIKE_CAPITAL.yaml`'s own sealed non-settlement framing)
and that this Stage 4 record's own combined treatment does not itself settle that question. This
filing authorizes no target of any kind for `cash_reserve`, resolves no aspect of the `CASH`/
`RESERVE` consolidation question, and does not reopen `XASSET-0008` §N.

### J. `crypto` / `fund_gld_defensive` — preserved, not extended

The sealed `crypto_fund_gld_defensive.yaml` finding (`coexistence_supported`), its BTC-specific
inflation-narrative basis (`GLD.yaml`/`BTC.yaml` both `historically_mixed_or_inconsistent`;
`ETH.yaml`/`SOL.yaml` both diverging at `historically_weakly_associated`), and the sleeve-wide,
sub-field-level forced abstention on `crypto`'s own `cross_coin_correlation_status` (`not_yet_
measured` on all three sealed coins) are preserved exactly as Stage 3 sealed them. This filing
performs no re-derivation, infers no crypto target of any kind, and infers no GLD target of any kind.

### K. Level 1 / Level 2 boundary — no instrument-level authority of any kind

This filing authorizes sleeve-level population only. No future Stage 4c implementation acting under
this authorization may choose, weight, or size an individual equity, ETF, or coin — no choice between
SPY, VEA, and VWO within `fund_broad_market`; no choice between BTC, ETH, and SOL within `crypto`; no
individual-instrument weight of any kind, anywhere. This restates `XASSET-0014` §12's own reuse of
the `XASSET-0012` §9 item 9 leakage scan, unmodified — no new leakage-check logic is invented here.

### L. Numeric-sizing gate — status after this filing, unweakened

`XASSET-0014` §15's own eleven-condition gate to numeric Level 1 sizing is **not amended, loosened,
or reordered by this filing**. This filing satisfies, at most, condition 2 alone ("a future, separate
Stage 4b content-authorization filing has named the exact sleeve population a Stage 4c implementation
may populate") — and only once this filing is itself merged, independently reviewed, and
principal-accepted, mirroring condition 1's own requirement for `XASSET-0014` itself. Every other
condition remains entirely unsatisfied by this filing: condition 3 (a future Stage 4c implementation
populating every authorized sleeve) has not occurred; condition 4 (every sleeve's Axis A/B/C
disposition explicit) has not occurred; condition 5 (`blocking_evidence[]` fully populated and
disclosed) has not occurred; condition 6 (`debt_reduction`'s own actual, future-determined
disposition explicit) has not occurred; condition 7 (`cash_reserve`'s consolidation-non-settlement
note actually populated) has not occurred; condition 8 (the counterfactual-masking non-influence
proof actually passing) has not occurred; condition 9 (a future Stage 4 validator module built,
reviewed, and passing) has not occurred; condition 10 (an audit trail proving every `sizing_ready`
disposition independently satisfies all four of §5's own conditions) has not occurred; condition 11
(every sleeve's relationship-coverage ledger fully populated with zero pairs silently treated as
clean) has not occurred. Satisfying all eleven remains necessary, never sufficient, for a future,
wholly separate, explicitly authorized filing to begin numeric Level 1 sleeve-level sizing
(`XASSET-0001` §J step 9) — this filing does not itself authorize that work under any circumstance.

### M. Allocation-check boundary — reaffirmed, not touched

A real, deployment-relevant allocation check remains authorized by nothing in this filing. It
remains downstream, in strict order, of: actual Stage 4 adoption (Stage 4b — this filing, plus a
future, separately authorized and completed Stage 4c); Level 1 numeric sleeve sizing (§L above, its
own separate future authorization); Level 2 instrument selection/sizing within each sleeve's approved
budget; required risk/overlap validation; and unlevered-portfolio validation. `OPS-0007` §5's own
narrow, scenario-only, cash-only, zero-margin allocation-check display bridge is a separate,
already-bounded authorization this filing neither reactivates, expands, nor references as a
shortcut around any of the above.

### N. Exact future Stage 4c deliverables

A future, separate, bounded Stage 4c implementation PR — gated on this filing's own merge,
independent review, and principal acceptance — may create exactly:

- up to six `intelligence/level1_sleeve_synthesis/policy_adoption/<SLEEVE_ID>.yaml` records, one per
  sleeve named in §B, in the exact field shape `XASSET-0014` §14 already specifies (`sleeve_id`,
  `schema_version`, `profile_reference`, `relationship_references[]`, `portfolio_function_status`,
  `function_rationale`, `abstention_index[]`, `capital_eligibility_status`,
  `sizing_readiness_status`, `blocking_evidence[]`, `unresolved_relationships[]`,
  `relationship_coverage_ledger[]`, `overlap_coordination_notes[]`, `cash_reserve_consolidation_note`
  — the `cash_reserve` record only, `record_status`, and the standard sealing/provenance fields) —
  no field added, removed, or redefined by this filing;
- one `COHORT_MANIFEST.yaml` for the new `policy_adoption/` sub-namespace, parallel to (never merged
  with) `profiles/`'s and `relationships/`'s own existing manifests;
- a dedicated Stage 4 validator (a new module, or a clearly separated Stage 4 section of
  `level1_sleeve_synthesis_validator.py` — the implementing session's own choice to justify, mirroring
  `XASSET-0006` §A point 3's and `XASSET-0013` §K's identical deferral), plus its full focused/
  adversarial test suite, bound to `XASSET-0014` §21's own twenty-four-point specification exactly
  (§O below);
- the required additive `operations/WORKSTREAMS.yaml` synchronization documenting the implementation's
  own confirmed lifecycle, per this repository's established Lane M convention.

No weight, no target percentage, no Level 2 content, and no eighth `sleeve_relationship` record of
any kind may be created by that future implementation.

### O. Future validator/test requirements — bound by reference, not redesigned

The future Stage 4c implementation must satisfy `XASSET-0014` §21's own complete twenty-four-point
validator/test specification in full, restated here as a binding condition on this filing's own
authorization rather than reproduced verbatim: closed schema with extra-key rejection at every
nesting level; exactly six closed `sleeve_id` values with at most one Stage 4c record per sleeve;
live, independent recomputation of every `profile_reference`/`relationship_references[]` hash, never
trusted from a stored value; mechanical Axis B re-derivation with a dedicated rejection test in both
directions; the `stronger_evidence_maturity` counterfactual-masking non-influence proof plus its
presence-independent defensive regression guard; mechanical Axis C consistency checks, including
relationship-coverage-ledger completeness (exact five-pair enumeration per sleeve, live cross-
reference against the sealed seven and the disclosed eight, the `deferred_disclosed`-caps-at-
`sizing_conditionally_ready` rule); a zero-numeric-fields scan (digit and spelled-out-magnitude
both); a zero-score/rank/composite-key scan; the Level 1/Level 2 leakage scan (§K above); a
directive/trading-language scan; a chart-domain-terminology scan; the `CASH`/`RESERVE`-distinction-
language scan; Stage 4's own materially separate bounded-conclusion scan (distinct from Stage 1–3's
blanket eligibility-language ban); the comparative-investment-superiority scan; adversarial test
coverage for ordering, negation, punctuation, conjunction, active/passive voice, euphemistic
paraphrase, hidden-sizing phrasing, and score/rank language, each with mandatory false-positive
guards; a zero-contender/QQQ-citation scan; a protected-path/byte-identity test across all thirteen
`XASSET-0012` §1 input layers plus the six `sleeve_profile` and seven `sleeve_relationship` records
themselves; manifest reconciliation; non-cascading abstention discipline; the Basis 3 mechanical
check (live `targets.yaml` cross-check, with rejection of any citation referencing evidence-maturity
or per-instrument-weight fields, and a dedicated test proving Basis 3 is correctly unavailable for
`debt_reduction`); the generalized Basis 2 structural-non-emptiness check; and the full
relationship-coverage-ledger completeness test set. No point in this specification is loosened,
tightened, or reinterpreted by this filing — this filing's own contribution is naming the exact
population (§B) that specification must be run against, nothing more.

### P. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry gains exactly one additive milestone gate,
`xasset0015-stage4b-policy-adoption-content-authorization` (`status: in_progress`, `pr: null` — this
filing does not mark its own unmerged work complete), plus one additive Lane M gate,
`xasset0014-post-merge-verification`, recording — without editing the
`xasset0014-level1-policy-adoption-methodology-design` gate's own historical text — that `PR #304`
is fully merged, confirmed above, and that its head check run is green. The workstream's ordinary
self-reference fields (`active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`)
are updated to this filing's own live state. No prior gate's own text is edited, and the
`roadmap_preservation`/`completion_criteria`/`blocker`/`next_action` fields are left exactly as
found, per the directive's own minimality instruction — the two new gates above already convey this
filing's own current facts. `WS-0014`'s own `status: proposed`/`priority: secondary`/`dependencies:
[WS-0005]` are unedited. `WS-0005` and `WS-0015` (the equity-valuation workstream, an unrelated
identifier collision-checked and confirmed distinct from this decision's own `XASSET-0015` ID) are
unaffected by this filing.

### Q. Explicit non-authorization

This filing authorizes **content-population targeting only** — exact record identities, nothing
else. It does not authorize:

- population of any Stage 4 (`policy_adoption`) record of any kind, for any sleeve, by this filing
  itself;
- any actual Portfolio Function Status, Capital Eligibility, or Sizing Readiness disposition for
  `equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto`, `cash_reserve`, or `debt_reduction`;
- any sleeve weight, sleeve budget, or sleeve allocation percentage of any kind;
- any instrument weight or Level 2 sizing decision of any kind;
- any portfolio in/out, eligibility, promotion, or demotion decision beyond the bounded, categorical,
  non-numeric Axis A/B/C schema `XASSET-0014` already designed;
- resolution of `debt_reduction`'s own economic-assessment forced-abstention state, or of the
  `CASH`/`RESERVE` consolidation question (`XASSET-0008` §N, not reopened);
- research on, or reclassification of, any of the eight deferred `sleeve_relationship` pairs
  `XASSET-0013` §E named — no ninth `sleeve_relationship` record, and no reclassification of an
  existing pair's coverage state, is authorized by this filing;
- any broader contender-registry sweep, `VRT`/`WMT` capital-priority conclusion, or `QQQ`/ETF-scope
  revisit;
- any real, live, scenario, or deployment-relevant allocation check;
- any chart evidence, buy-ladder work, backtesting, monitoring, or sell-discipline rule;
- any allocator, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `margin_state.py`, or `levels.py` change;
- any hardening, expansion, or weakening of any existing repository validator, including
  `level1_sleeve_synthesis_validator.py`;
- any dashboard change;
- any tier/target/holdings/gate/cap/cluster/order/trade change of any kind;
- numeric Level 1 sleeve-level sizing of any kind (`XASSET-0001` §J step 9) — remains gated on
  `XASSET-0014` §15's own eleven conditions, at most one of which this filing partially advances
  (§L above).

## Rationale

`XASSET-0014` §K/§23 defined Stage 4's own internal sub-sequence — Stage 4a (methodology, complete),
Stage 4b (content authorization, this unit), Stage 4c (future implementation), numeric Level 1 sizing
(its own separate, later authorization entirely) — and stated explicitly that Stage 4b must "name the
exact sleeve population a Stage 4c implementation may populate... before any record is drafted,"
mirroring `XASSET-0012`→`XASSET-0013`'s own directly analogous precedent one layer down. This filing
performs exactly that naming step, and no more, following the same "define, then authorize content,
then implement" sequence this repository has used at every prior milestone-scale undertaking
(`TIER-0001`→`TIER-0005` before Milestone 6; `REL-0001`→`REL-0002` before the first relationship
batch; `XASSET-0005`→`XASSET-0006`/`XASSET-0007` before functional-doctrine and overlap-model
content; `XASSET-0010`→`XASSET-0011` before six-instrument economic-assessment content;
`XASSET-0012`→`XASSET-0013` before Stage 3 synthesis content).

Authorizing all six sleeves, rather than a narrower subset, follows directly from applying
`XASSET-0014`'s own corrected mechanism to the live sealed data: every sleeve's relationship-coverage
ledger is fully accounted for (the 7 sealed + 8 disclosed-deferred = 15 closed set has zero gaps),
every sleeve's Axis B is mechanically derivable from an already-populated `evidence_coverage_profile`
field, and every sleeve now has at least one lawful Axis A evidentiary basis available
(`XASSET-0014` §3.3's own six-sleeve reachability audit, independently re-verified here). Where the
resulting Stage 4c record for a given sleeve is likely to disclose a genuine limitation — most
concretely `debt_reduction`'s forced-abstained Axis B/C and `fund_broad_market`'s structurally capped
Axis C — that is exactly the honest disclosure `XASSET-0014`'s own three-axis, non-collapsing design
exists to produce, not a reason to withhold the sleeve from the authorized population. Excluding a
sleeve on the anticipated shape of its own future disposition would itself be an unauthorized,
premature policy judgment this filing has no authority to make — `XASSET-0014` §M already bars this
filing from assigning any actual disposition, and selectively deferring a sleeve for that reason
would be the same act by omission.

## Alternatives Considered

**Defer `debt_reduction` from the Stage 4c population, given its forced-abstained evidence base.**
Rejected — §D above traces the reasoning in full: `XASSET-0014`'s entire three-axis design exists
specifically to represent `debt_reduction`'s own live case (role-legitimate, evidence-blocked)
honestly rather than force it into a single collapsed verdict; deferring it at the Stage 4b
population-selection layer would defeat that purpose exactly as thoroughly as collapsing its axes
would have. `XASSET-0013` §B's own analogous decision (populating `debt_reduction`'s Stage 1–3
profile despite its thin evidence, rather than omitting the sleeve entirely) is the direct precedent
this filing follows one layer up.

**Defer `fund_broad_market` pending a future relationship batch closing one or more of its four
`deferred_disclosed` pairs, since its Axis C is structurally capped below `sizing_ready` regardless.**
Rejected — a structurally capped Axis C ceiling is itself a fully-derivable, disclosable outcome
(`sizing_conditionally_ready` at best), not an evaluation failure; `XASSET-0014` §5.1 was built
specifically to represent this case (see the identical treatment already applied to `crypto`,
`fund_gld_defensive`, and `cash_reserve`, none of which reach a full `sealed_determined` ledger
either). Deferring `fund_broad_market` on this basis alone, while including the other four
non-`equity` sleeves that share the identical structural constraint, would be an arbitrary,
unprincipled distinction with no basis in `XASSET-0014`'s own mechanism.

**Authorize a narrower population — e.g., the five sleeves with a live `targets.yaml` row, deferring
`debt_reduction` alone as the sole sleeve lacking Basis 3.** Rejected — Basis 3's unavailability for
`debt_reduction` does not mean Axis A is unreachable for it; Basis 1 (a sealed `role_preserving`
finding) and Basis 2 (a genuine, quotable doctrine passage) both remain independently available and
sufficient, per `XASSET-0014` §3.2/§3.3/§7.1's own explicit text. Using Basis 3's structural
inapplicability to a margin-lever sleeve as grounds for exclusion would conflate "this sleeve has no
`targets.yaml` destination row" (a true, disclosed structural fact) with "this sleeve cannot be
evaluated" (false) — exactly the error this filing's own §D determination guards against.

**Authorize Stage 4c's own implementation directly in this same filing**, rather than deferring it to
its own future unit. Rejected outright per the directive's own explicit instruction and
`XASSET-0012`→`XASSET-0013`→[Stage 3 implementation]'s own directly analogous three-step precedent
one layer down: a Stage 4b filing must name the population before a Stage 4c session drafts a single
record against real evidence, matching the same sequencing discipline every prior stage of this
undertaking has followed.

**Reclassify or research one or more of the eight `XASSET-0013` §E deferred relationship pairs as
part of this filing**, to give a sleeve like `fund_broad_market` a stronger Axis C ceiling before
Stage 4c populates its record. Rejected outright — the directive's own explicit minimality
instruction bars this, and doing so would blur Stage 2/3's own already-closed relationship-batch
scope into a Stage 4b content-authorization filing that has no authority over Stage 1–3's own record
population at all; any future relationship batch closing a deferred pair remains its own separate,
future, explicitly authorized unit.

## Consequences

**Changes as a direct result of this decision**: the existence of one retained, exact six-sleeve
`policy_adoption` population authorization (no sleeve deferred), bound by reference to
`XASSET-0014`'s already-accepted Stage 4a methodology with no restatement or redesign; one
sleeve-by-sleeve evaluability determination independently re-verifying `XASSET-0014` §3.3's own
reachability audit against the live sealed data; two dedicated high-scrutiny determinations
(`debt_reduction`, `fund_broad_market`) explaining why each is included rather than deferred; a
restated, unweakened eleven-condition numeric-sizing gate status (at most condition 2 partially
advanced, ten conditions entirely unsatisfied); confirmation, via two additive
`operations/WORKSTREAMS.yaml` gates, that `XASSET-0014`'s own authorized methodology (`PR #304`) is
fully merged and its head CI check is green; five rejected alternatives recorded for future
reference.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin
behavior; the 1.8x leverage cap or 30% margin-buffer floor; any Company, Theme, relationship,
classification, valuation-archetype, valuation-evidence, valuation-result, ETF-classification,
crypto-classification, functional-doctrine, overlap-model, economic-assessment,
instrument-economic-assessment, contender-evaluation, `sleeve_profile`, or `sleeve_relationship`
record's content; any current cash balance, reserve level, GLD holding, or margin-debt figure;
`WS-0005`'s completed, `status: complete` state; `WS-0014`'s own `status: proposed`/`priority:
secondary` (this filing adds two additive gates, it does not begin execution or change the
workstream's own status/priority); or any brokerage, trading, or order-related capability. Completing
this unit does not itself populate any Stage 4 record for any sleeve, does not authorize a Stage 4c
implementation to begin without its own further merge/review/acceptance of this filing first, and
does not authorize numeric Level 1 or Level 2 sizing of any kind, or any allocation check — each
requires its own separate, explicit, future principal authorization, per `XASSET-0012` §10's own
unedited four-stage sequence, `XASSET-0014` §K/§15/§23's own unedited Stage 4 sub-sequence and
eleven-condition gate, and `XASSET-0001` §J's own dependency-ordered roadmap.
