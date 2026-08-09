---
decision_id: XASSET-0006
date: 2026-08-09
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0004, TIER-0005, TIER-0007, TIER-0009, REL-0001, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005]
supporting_artifact: null
file: governance/decisions/XASSET-0006-ws0014-functional-doctrine-content-authorization.md
---

## Context

### Authority for this unit

`XASSET-0005` designed, as text only, a shared functional-doctrine schema for exactly four capital-use
types (`CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, `DEBT_REDUCTION`) and a separate ten-dimension
overlap/concentration-model architecture, batching both designs in one filing under `XASSET-0001` §J's
explicit permission to batch "cash/GLD/debt doctrine + overlap-model **architecture** (steps 6–7) —
permitted to batch only where no asset-specific judgment occurs." `XASSET-0005`'s own Consequences
section states plainly that completing that design "does not itself authorize populating any `CASH`,
`RESERVE`, `GLD_DEFENSIVE_ROLE`, or `DEBT_REDUCTION` functional-doctrine record, computing any of the
ten overlap/concentration dimensions, cross-asset synthesis... or the final independent audit — each
requires its own separate, explicit, future principal authorization." `XASSET-0001` §J's own separation
rule is independently on point: "framework design versus blind-classification execution... must never be
combined" — restated here for functional doctrine and the overlap model exactly as it already governed
the ETF and crypto sleeves (`XASSET-0002` designed both frameworks in one filing; `XASSET-0003` and
`XASSET-0004` then separately authorized ETF and crypto classification *content*, each its own filing,
never combined with each other or with the design). This filing is the direct analogue of `XASSET-0003`/
`XASSET-0004` for the functional-doctrine content step — authorization only, binding by reference to
`XASSET-0005`'s already-accepted design, no restatement, no redesign.

**Packaging determination, reverified directly against `XASSET-0001` §J and `XASSET-0005`'s own
Consequences section**: functional-doctrine content (`CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE`/
`DEBT_REDUCTION` population) and overlap-model content (the ten dimensions' computation) are two
genuinely separate asset-appropriate content domains sharing only a batched *design* filing — the same
relationship ETF and crypto content had to their own shared design filing (`XASSET-0002`). Matching that
precedent exactly, this filing authorizes **functional-doctrine content only**. A future, separate
`XASSET-0007` filing will authorize overlap-model content once this filing's own authorized functional-
doctrine implementation has merged (the overlap model's `defensive_offset_interface` dimension reads from
a populated `GLD_DEFENSIVE_ROLE` record once one exists — sequencing that dimension's eventual
computation after this filing's own content, though `XASSET-0007`'s own authorization does not depend on
that sequencing to be filed). `XASSET-0006` and `XASSET-0007` are not combined in this or any filing.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0006-functional-doctrine-5mkxyl`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `b97ad2a2a23554b6072340ebff9ceddc799b1a22` — the `VALUATION-0005`-authorized Stage-3 quantitative
  equity valuation-evidence-population implementation's own merge commit (PR #283).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #273`'s full lifecycle independently re-verified via the GitHub API, not assumed**: accepted head
  `8415c82ec82bbd4a99a1c0961184200290945350`; three independent reviews —
  `pullrequestreview-4887790034` (CHANGES REQUIRED, 0 BLOCKING / 1 MAJOR / 0 MINOR / 1 non-actionable
  NOTE, the overlap-model nine-vs-eight-dimension coverage-gap finding), `pullrequestreview-4887859729`
  (CHANGES REQUIRED, 0 BLOCKING / 0 MAJOR / 2 MINOR / 1 non-actionable NOTE), and
  `pullrequestreview-4887894742` (**APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR
  / 0 MINOR / 1 non-actionable NOTE, at exact head `8415c82e...`) — confirmed the correct, real final
  review; principal acceptance (`issuecomment-5224205559`, accepted head
  `8415c82ec82bbd4a99a1c0961184200290945350`); merge (merge commit
  `1921864326f2cc75609b1c91037c24e333c4e3d0`, parents `e5446cd5c4bfce744691fd1914ec8ef098286839` and
  `8415c82ec82bbd4a99a1c0961184200290945350`, both independently re-confirmed via `git show -s
  --format='%H %P'`); merge-commit CI independently re-fetched — workflow run `31236387352`, job
  `93049536968`, `status: completed`/`conclusion: success`. This confirmation was already recorded in
  `operations/WORKSTREAMS.yaml`'s `xasset0005-implementation-post-merge-verification` gate (`status:
  complete`, `pr: 273`) by the `VALUATION-0001` filing that followed `XASSET-0005` — independently
  re-confirmed accurate and current this session; not re-added.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`, `active_branch: null`,
  `active_pr: null`, `last_verified_main_sha: 1921864326f2cc75609b1c91037c24e333c4e3d0`,
  `last_verified_date: "2026-08-08"` — stale relative to current `main` (`b97ad2a2...`), since
  `WS-0014`'s own self-reference fields were last touched by `XASSET-0005` (PR #273) and no
  `WS-0014`-substantive filing has landed since; this filing performs the ordinary, expected
  self-reference synchronization as part of its own live-state update (§F), following this repository's
  established convention that each substantive filing touching a workstream refreshes that workstream's
  own `last_verified_main_sha`/`last_verified_date` — not a Lane M correction of any stale content
  (`XASSET-0005`'s own gates are accurate as filed; nothing about them requires correction).
- **`WS-0015`'s live state independently read and left untouched**: `VALUATION-0005` (PR #283) is
  `WS-0015`'s own latest substantive filing and is the correct owner of any further `WS-0015` Stage-3
  self-reference synchronization — this filing does not touch `WS-0015` (no genuinely established
  fold-forward reason or authority exists for this filing, an unrelated `WS-0014` unit, to edit it).
- **`XASSET-0001` (in full) and `XASSET-0005` (decision file plus supporting artifact, in full) read
  directly this session**, not summarized from memory — the exact functional-doctrine field names,
  closed vocabularies, and the `structural_reference`/`canonical_record_hash()` mechanism (§B below) are
  drawn from `XASSET-0005` supporting artifact §§3.1–3.6, not reconstructed.
- **`targets.yaml` independently re-read**: `RESERVE` (`target_pct: 4.00, asset_class: reserve`), `CASH`
  (`target_pct: 1.00, asset_class: cash`), and `GLD` (`target_pct: 4.00, asset_class: fund`) confirmed at
  their current lines, zero drift from `XASSET-0005`'s own stated population — `DEBT_REDUCTION` has no
  `targets.yaml` row (it is not a destination weight; it is a use of capital the functional-doctrine
  schema itself represents, per `XASSET-0005` §3.2's `capital_use_type` design).
- **`holdings.yaml` independently re-read**: `margin.debt: 0.0`, `margin.buffer_pct: 100.0`,
  `margin.synced_at: 2026-07-31` — a genuine, dated, governed evidence point exists for margin state
  today, preserved (not pre-decided) as the `DEBT_REDUCTION` `freshness_state` evidence question §C
  below leaves open.
- **`intelligence/etf_classification/GLD.yaml` and `etf_classification_validator.py` independently
  re-read**: the sealed GLD structural record and its `canonical_record_hash()` function (line 322 in
  the current file) both confirmed present, unchanged since `XASSET-0002`/`XASSET-0003`'s own sealing —
  the exact reference target `XASSET-0005` §3.4's `structural_reference` mechanism requires a future
  `GLD_DEFENSIVE_ROLE` record to pin against.
- **`CLAUDE.md`'s own Portfolio Doctrine and Decisions Log independently re-read for GLD- and
  RESERVE-specific evidence**: `CLAUDE.md`'s "Second concentration cap added: power_infra" Decisions Log
  entry states, verbatim, that a full-book sector audit found "zero fixed-income exposure (correct given
  ~5% margin cost, not a gap to fill — GLD does the ballast job bonds would)" — real, citable,
  functional-role evidence for `GLD_DEFENSIVE_ROLE` that a future implementation may draw on. No
  comparable functional-role narrative exists anywhere in `CLAUDE.md` for `RESERVE` specifically, beyond
  `targets.yaml`'s own mechanical-allocator-level "never a buy candidate, definitionally satisfied"
  comment — an allocator-behavior fact, not a functional-role narrative. This asymmetry is preserved,
  not resolved, by this filing (§C below).
- **A genuine, unresolved stale-wording defect independently found in `XASSET-0005`'s own supporting
  artifact, confirmed by direct inspection, not touched by either of `XASSET-0005`'s own two bounded
  corrections**: `governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_ARCHITECTURE_
  DESIGN_20260808.md` §6.2 (the overlap model's field-by-field design section) still reads, at three
  separate points (lines 513, 518, 531 of that file as currently committed), "the two
  `interface_placeholder`" dimensions and "the five `mechanical_rollup`/`narrative_evidence`" dimensions
  — both stale counts from before `XASSET-0005`'s own first bounded correction added
  `geographic_currency_exposure` and `whole_portfolio_volatility_drawdown_concentration`, raising the
  corrected §6.1 table (independently re-tallied this session) to **6 `mechanical_rollup`/
  `narrative_evidence` dimensions and 4 `interface_placeholder` dimensions** (10 total). `XASSET-0005`'s
  two correction rounds fixed §6.1's own table and the decision file's separate summary prose, but never
  touched these three §6.2 references. **This filing does not opportunistically amend `XASSET-0005`** —
  no repository convention requires or permits a functional-doctrine-content-only authorization to edit a
  design filing's own supporting artifact, and doing so here would exceed this filing's own bounded
  scope. This is recorded here as a known, disclosed, unresolved factual/design-text inconsistency, to be
  addressed in the future `XASSET-0007` overlap-model-content authorization's own preflight — not a
  reason to implement any part of the overlap model under this filing.
- **Decision catalog independently rebuilt**: **99 decisions, `issues == ()`** at the starting head, 99
  non-`README.md` files in `governance/decisions/` reconciling 1:1. `XASSET-0006` confirmed unused: zero
  matches in `governance/decisions.yaml`, zero matches via full-repository grep;
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new decision
  domain needs one") is satisfied by continuing the existing `XASSET-####` series — this filing is the
  direct continuation of `XASSET-0001` §J step 6's content half, not a genuinely new decision domain,
  mirroring `XASSET-0003`'s and `XASSET-0004`'s identical continuation of steps 4 and 5.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing does two things, in one bounded PR:

1. **Performs the ordinary `WS-0014` self-reference synchronization** (`active_branch`,
   `last_verified_main_sha`, `last_verified_date`) reflecting this session's own live-state
   verification — no prior gate's historical text is edited; no Lane M correction is required, since
   `XASSET-0005`'s own gates were found accurate as filed (§I below).
2. **Authorizes exactly one future, separate, bounded functional-doctrine (content) implementation pull
   request**, covering all four capital-use types under the exact schema, evidence, sequencing,
   abstention, GLD-reference, and validator/test controls already specified and accepted through
   `XASSET-0005`. It performs no population itself, creates no functional-doctrine record or validator,
   and implements no `intelligence/functional_doctrine/` content.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007` §1),
any required bounded correction and re-review, explicit principal acceptance, merge, and post-merge
verification — the same lifecycle every prior filing in this chain has followed — may proceed to:

1. Draft and seal one functional-doctrine record for each of the four fixed capital-use types named in
   `XASSET-0005` §3.2 — `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, `DEBT_REDUCTION` — zero exclusions, zero
   additions. No fifth `capital_use_type` value may be introduced without its own separate
   schema-amendment decision (`XASSET-0005` §3.2's own explicit rule).
2. Create the appropriate cohort manifest for the four sealed records, matching every prior
   classification framework's own `COHORT_MANIFEST.yaml` convention (`XASSET-0005` §3.3's `record_status`
   sealing discipline; §7 point 13's determinism requirement).
3. Build `functional_doctrine_validator.py` (or the smallest validator structure `XASSET-0005`'s
   supporting artifact §7 already specifies, if a future implementation determines a shared-helper module
   with the overlap-model validator is warranted once `XASSET-0007` exists — that determination belongs
   to whichever content authorization is exercised second, not to this filing, matching the identical
   deferral `XASSET-0003` §A point 3 already used for the ETF/crypto validator relationship) and its
   dedicated test file.
4. Use a single implementation pass covering all four capital-use types (no per-type PR structure; no
   multi-shard isolation apparatus of any kind) — the population is fixed and small (four), and
   `XASSET-0002`'s own Rationale already established that shard isolation is unnecessary at this scale
   for the ETF sleeve (≤4 instruments); this filing makes the same determination binding for the
   functional-doctrine sleeve's identical four-record population.
5. Stop after the first record, without a separate pilot authorization, if a systemic schema, evidence,
   or contamination defect is discovered — an internal stop-and-fix condition within the one authorized
   implementation PR, not a license to split into a second governance filing or a per-type PR structure.

**No overlap-model content of any kind is authorized by this filing.** Computing any of the ten
dimensions `XASSET-0005` §6 designed requires its own separate, future, explicit authorization
(`XASSET-0007`, not yet filed) and its own separate implementation PR — this filing does not combine,
foreshadow, or pre-stage it, and a functional-doctrine implementation PR authorized here must not create,
populate, or compute any `intelligence/overlap_model/` file or record under any circumstance.

### B. Binding specification — by reference, not restatement

The implementation PR must follow `XASSET-0005`'s specification exactly, as accepted and merged at
`1921864326f2cc75609b1c91037c24e333c4e3d0`. This filing does not redesign, loosen, tighten, or restate
that specification in its own words beyond the index below — the implementation session has no
discretion to depart from it:

| Control | Governing section (all `XASSET-0005 §N` citations below refer to `XASSET-0005`'s supporting artifact, `governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_ARCHITECTURE_DESIGN_20260808.md`, unless the decision file itself is cited) |
|---|---|
| 4-capital-use-type population, zero exclusions, zero additions | This filing §A, cross-checked against `XASSET-0005` §3.2's closed `capital_use_type` vocabulary at implementation time |
| Shared schema across all four types: 6 substantive axes (`functional_role`, `hard_constraint_status`, `economic_assessment_readiness`, `liquidity_character`, `capital_preservation_character`, `freshness_state`) plus `evidence_quality` — no seventh substantive axis, no numeric field of any kind, no score, no ranking formula, no target percentage, no avoided-borrowing-cost figure | `XASSET-0005` §3.1, §3.2 (frozen by that filing's own acceptance) |
| Method: narrative-judgment fields kept separate from mechanically-computed/citation-backed fields — `hard_constraint_status` structurally, mechanically independent of `economic_assessment_readiness` (§7 point 5's dedicated validator requirement, separate code paths, no cross-derivation) | `XASSET-0005` §2, §3.2 (`hard_constraint_status`), §3.3 (dual, never-merged envelope projections) |
| `capital_use_type`-conditional shape: `economic_assessment_readiness` is single-part `{status, rationale}` for `CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE`; two-part (`avoided_borrowing_cost_readiness`, `survivability_and_buffer_benefit_readiness`, each independently forced, never blended) for `DEBT_REDUCTION` only — the validator rejects either shape appearing on the wrong type | `XASSET-0005` §3.2 (`economic_assessment_readiness`), §3.5 (full split rationale) |
| `economic_assessment_readiness` forced to exactly one value, `assessment_required`, in every `status` sub-field across both shapes, zero exception — no opportunity-cost figure, no avoided-interest number, no target allocation percentage, no ranking against another capital-use type | `XASSET-0005` §3.2, matching `XASSET-0002` §6.3's/`TIER-0009`'s identical forced-value precedent |
| `structural_reference` — required, all four sub-fields present, when and only when `capital_use_type: GLD_DEFENSIVE_ROLE`; forbidden (rejected as an unknown key) on `CASH`/`RESERVE`/`DEBT_REDUCTION`. `source_instrument_id: "GLD"`, `source_schema: "etf_classification"`, `source_file: "intelligence/etf_classification/GLD.yaml"`, `referenced_content_sha256` computed via a **read-only call** to `etf_classification_validator.canonical_record_hash()` against the live sealed GLD record — never a newly invented hashing scheme, never a duplicated or re-derived copy of any of GLD's own seven ETF-framework fields. None of the ETF framework's six axis key names (`structural_role`, `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`) may appear anywhere in a `GLD_DEFENSIVE_ROLE` record, at any nesting level | `XASSET-0005` §3.4 (full mechanism), §7 point 8 (validator enforcement) |
| Abstention discipline — `not_applicable` for a structurally absent concept (e.g., `DEBT_REDUCTION`'s own `liquidity_character`), `unable_to_determine`/`unable_to_determine_freshness` for a genuine evidence gap, always with a required `abstention_reason`; abstention does not cascade between axes; per-axis abstention-availability table (`hard_constraint_status` has no abstention path at all — it is a citation-backed structural fact, not a judgment that can be under-evidenced) | `XASSET-0005` §3.2 (per-field abstention state), §3.6 |
| Contamination rule — no judgment axis (`functional_role`, `hard_constraint_status`, `economic_assessment_readiness`, `liquidity_character`, `capital_preservation_character`) may be drafted from `holdings.yaml`'s actual cash/reserve dollar figures, `targets.yaml`'s `target_pct` values, `margin_state.py`'s live account-specific numeric output (`leverage_ratio`, `utilization`, actual dollar buffer), or any chart/technical signal — only the **existence** of a governed mechanism may be cited, never the **current live value** of an account-specific number that mechanism computes | `XASSET-0005` §3.6 |
| Shared envelope (`capital_use_type`, `schema_version`, `provenance`, `evidence_quality_status`, `uncertainty_summary`, `structural_risk_flags`, `record_status`, `structural_reference` — present only on `GLD_DEFENSIVE_ROLE`, `later_governance_action`, `abstention_index`) plus the two deliberately un-merged handoff projections (`hard_constraint_signal`; `economic_assessment_readiness_summary`) and the shared asset-neutral projections (`role_summary`, `evidence_quality_summary`, `uncertainty_summary`, `liquidity_risk_summary`) — every summary field a read-only copy of an already-computed axis field, never independently computed | `XASSET-0005` §3.3, §4 |
| Zero numeric fields anywhere in either the envelope or any axis, with **no** carve-out of any kind (stricter than the ETF framework's own scoped `expense_ratio_pct` exception) | `XASSET-0005` §3.3 (closing statement), Rationale ("Why the functional-doctrine and overlap schemas carry zero numeric fields") |
| Validator specification (14 points: exact 4-type population enforcement; closed schema at every level rejecting extra keys, not just missing ones; `capital_use_type`-conditional shape enforcement; no cross-schema field-name leakage — equity/ETF/crypto axis names forbidden; `hard_constraint_status`/`economic_assessment_readiness` structural independence, dedicated test, separate code paths; no numeric score/rank/target/avoided-cost leakage with zero carve-out; no composite-overlap-score leakage — not applicable to a functional-doctrine-only implementation, restated for completeness since the validator module may share helpers with a future overlap-model validator; `GLD_DEFENSIVE_ROLE` structural-reference enforcement including a live hash recompute; no chart-evidence leakage; no directive/trading-language leakage — the shared eight words plus `repay`/`redeploy`/`fund`/`draw`, word-boundary matched; evidence/provenance validation; allocator/margin import decoupling — zero import of `allocate.py`/`margin_state.py` in either direction, citation in prose only; deterministic generation; protected-path isolation) | `XASSET-0005` §7 (points 1–6, 8–14 apply directly to functional doctrine; point 7's composite-overlap-score scan is overlap-model-specific and out of this filing's scope) |
| Test specification (functional-doctrine-relevant items: happy-path per capital-use type; malformed envelope/axis; extra/missing keys at every level — the `contender_registry_validator.py` MAJOR-finding exploit class; wrong `capital_use_type`; `economic_assessment_readiness` shape-mismatch rejection in both directions; `structural_reference` present-on-wrong-type and missing-on-`GLD_DEFENSIVE_ROLE` rejection; stale-hash rejection against a live recompute of the real sealed GLD record; each of the six ETF axis key names individually rejected inside a `GLD_DEFENSIVE_ROLE` record; `hard_constraint_status`/`economic_assessment_readiness` independence test; forbidden numeric/score/avoided-cost leakage per named term, with no positive-acceptance test of any kind; cross-schema field-name leakage per source schema; abstention behavior including the per-axis availability table; duplicate/missing/extra `capital_use_type` against the named population; chart-terminology leakage per term; directive/trading-language leakage per word including the four debt/cash-specific verbs and a false-positive guard for ordinary "fund"/"funded" usage in a citation string; forced `assessment_required` violation on either shape; envelope-projection-mismatch rejection; determinism; protected-path isolation; allocator/margin import-coupling isolation) | `XASSET-0005` §8 (the functional-doctrine-applicable subset — overlap-model-only test items, e.g. the ten-dimension composite-score scan and the `computation_status` forced-value test, are out of this filing's scope), §8.1's four explicitly carried-forward lessons |
| Batching/future-lifecycle rules — content never recombined with design; functional-doctrine and overlap-model content never share one filing; a schema revision, if ever needed, is its own future, separately authorized design-amendment unit | `XASSET-0005` Rationale, Alternatives Considered; `XASSET-0001` §J's separation rule |

Nothing in this table is amended, expanded, or narrowed by this filing. Any future session finding a
genuine ambiguity or gap in `XASSET-0005`'s specification must return for its own separate governance
correction — not resolve it unilaterally inside the implementation PR. This includes the stale
"two"/"five" wording in `XASSET-0005`'s supporting artifact §6.2, disclosed above — it bears on the
overlap model, not this filing's own functional-doctrine content, and is explicitly preserved for
`XASSET-0007`'s own preflight rather than resolved here.

### C. Evidence standard (binding on the future implementation) — two open factual questions preserved, not pre-decided

The implementing session must use only appropriate functional-doctrine evidence: `targets.yaml`'s own
row (symbol/`asset_class` identity only, never `target_pct`, per `XASSET-0005` §3.6); `CLAUDE.md`'s own
Portfolio Doctrine, Guardrails, and Decisions Log text, cited as evidence where it already states a
relevant fact, never restated as this record's own invented judgment; for `GLD_DEFENSIVE_ROLE`, GLD's own
already-sealed ETF structural record, consumed exclusively through the `structural_reference` hash-pin
mechanism (§B); for `DEBT_REDUCTION`, the **existence** of the 1.8x leverage cap and 30% buffer floor
governed by `CLAUDE.md`'s Portfolio Doctrine, never the current live numeric value `margin_state.py`
would compute from today's account state. Where evidence is insufficient for a given axis, the
implementation must use the framework's own abstention path (§B) rather than filling the gap — an axis
abstaining on one or more of the four types is an honest outcome, not a defect requiring correction. This
filing preserves, rather than settles, two evidence-sufficiency questions this session's own preflight
found genuinely open (§ Preflight above):

1. **`RESERVE`'s `functional_role`.** Repository evidence may not clearly distinguish `RESERVE`'s
   functional role beyond its asset-class/ticker label and the mechanical-allocator-level fact that it is
   "never a buy candidate, definitionally satisfied" — a fact about allocator behavior, not about what
   portfolio job `RESERVE` does. No `CLAUDE.md` passage narrates a `RESERVE`-specific functional purpose
   the way "GLD does the ballast job bonds would" narrates `GLD_DEFENSIVE_ROLE`'s. The implementation must
   either make a defensible, cited `capital_preservation_buffer` determination (`XASSET-0005` §3.2's
   `functional_role` closed vocabulary) grounded in actual repository text, or abstain
   `unable_to_determine` with a specific `abstention_reason` naming the evidence gap. **It must never
   force a value merely to fill the record.** This filing does not pre-decide which outcome is correct —
   that determination belongs to the implementing session's own evidence-gathering, subject to
   independent review.
2. **`DEBT_REDUCTION`'s `freshness_state`.** No persisted, dated `margin_state.py` run artifact exists
   anywhere in this repository — `margin_state.py`'s own `classify_margin_state()` is a pure calculator
   with no output-file side effect, independently confirmed this session by direct source inspection.
   `holdings.yaml` does carry a dated `margin.synced_at: 2026-07-31` field, a genuine governed evidence
   point recording when the account's margin state was last synced from Robinhood — but whether that
   field is an "appropriate governed dated margin-sync artifact" in the sense `XASSET-0005` §3.2's
   `freshness_state` design requires (as opposed to a live-state field that itself falls under §3.6's
   contamination rule against citing account-specific current values) is a judgment this filing does not
   make. The implementation must either cite that field, or an equivalently appropriate governed dated
   artifact, as the `as_of_reference` for a `current`/`stale_needs_refresh` determination, or abstain
   `unable_to_determine_freshness` if no such citation can be made without crossing §3.6's contamination
   boundary. This filing does not pre-decide which outcome is correct.

If the implementing session determines that gathering adequate evidence for any axis on any of the four
types requires research authority beyond what this filing and `XASSET-0005` already grant, it must stop
and disclose that as a genuine blocker rather than substitute an invented value or a forced determination
without disclosure.

### D. Stop conditions (binding on the future implementation)

The implementation PR must stop immediately and disclose, never silently work around: population drift (a
fifth `capital_use_type` appearing to be needed, or one of the four ceasing to apply, since the
implementation may begin some time after this filing merges); any equity-, ETF-, or crypto-shaped field
leakage; any overlap-model field leakage (`dimension_id`, `dimension_type`, `computation_status`,
`source_mechanism`, `output_shape`, `evidence_or_source_refs`, `uncertainty_or_gap_disclosure`, or any
other `XASSET-0005` §6 field name); any numeric score/rank/target/avoided-cost leakage of any kind; any
chart-domain leakage; any attempt to compute or populate any of the ten overlap-model dimensions; any
attempt to blend `DEBT_REDUCTION`'s two-part `economic_assessment_readiness` into one figure; any attempt
to depart from the forced `assessment_required` state; any duplication or re-derivation of GLD's own
sealed ETF structural fields inside a `GLD_DEFENSIVE_ROLE` record, rather than referencing them by hash;
any citation of a `margin_state.py`-computed live account-specific numeric value as functional-doctrine
evidence; any protected-path mutation; or any unexpected target, holdings, gate, cap, cluster, allocator,
margin, ladder, order, or trade change.

### E. Independent review requirement (binding on the future implementation)

The implementation PR's independent exact-head review must verify, at minimum: the exact four-type
population; the exact changed-file inventory; schema conformance for every record, including the correct
`capital_use_type`-conditional `economic_assessment_readiness` shape; abstention validity and
non-cascading behavior, including the per-axis availability table and the specific `RESERVE`/
`DEBT_REDUCTION` evidence-sufficiency determinations named in §C (whether each was resolved with a
defensible citation or a genuine abstention, never a forced, uncited value); `structural_reference`'s
full mechanism — presence exactly on `GLD_DEFENSIVE_ROLE`, the live hash recompute against
`etf_classification_validator.canonical_record_hash()`, and absence of every ETF axis key name anywhere
in that record; `hard_constraint_status`/`economic_assessment_readiness` structural independence,
including the dedicated mutation test; the forced `assessment_required` state on all four records with
zero exception; the envelope's read-only-projection consistency; the validator and its tests against
`XASSET-0005`'s supporting artifact §7/§8's full functional-doctrine-applicable specification, including
§8.1's four explicitly carried-forward lessons; CI; protected-path isolation; absence of any overlap-model
content of any kind; absence of any cross-asset synthesis, sleeve target, or instrument target; and
absence of any policy mutation. Any correction requires its own fresh exact-head delta review before
principal acceptance.

### F. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **`active_branch` set to this filing's own branch, `last_verified_main_sha` updated**
   `1921864326f2cc75609b1c91037c24e333c4e3d0` → `b97ad2a2a23554b6072340ebff9ceddc799b1a22`, and
   **`last_verified_date` updated** to this filing's own date — the ordinary self-reference refresh every
   substantive `WS-0014` filing performs, not a correction of any prior gate's own content.
2. **One new additive gate, `xasset0006-functional-doctrine-content-authorization`**, recording this
   filing's own branch and (once it exists) PR number — `status: in_progress`, **not** `status:
   complete`, since this filing's own governance PR is itself unmerged, unreviewed, and unaccepted,
   matching every prior filing's identical discipline in this chain.
3. **`blocker` and `next_action` updated** to state plainly: steps 6–7's shared design (`XASSET-0005`) is
   complete and merged (PR #273); this filing, once merged, authorizes exactly one future functional-
   doctrine content implementation PR (the content half of step 6 / item 8 of the `§I` list);
   overlap-model content (the content half of step 7 / item 9) remains separately, wholly unauthorized
   and requires its own future `XASSET-0007` filing; items 9 (cross-asset synthesis) through 14 remain
   wholly unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`) is
changed — this filing does not begin execution and does not alter the workstream's own standing.
`WS-0015` is not touched by this filing (§ Preflight above).

### G. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder
change; any trade or order; any chart use of any kind; any buy/sell/hold/trim/exit/wait/stage/repay/
redeploy/fund/draw recommendation or directive of any kind; any overlap-model content of any kind (any of
the ten dimensions `XASSET-0005` §6 designed); GLD's actual functional/defensive-role determination
beyond what a future implementation may cite as evidence (this filing does not itself determine GLD's
role, and neither does the implementation it authorizes settle the question for the overlap model's own
`defensive_offset_interface` dimension, which remains `XASSET-0007`'s scope); any valuation or
economic-assessment methodology; any avoided-borrowing-cost calculation; any cross-asset overlap,
concentration, or opportunity-cost synthesis; any sleeve-level or instrument-level sizing; population of
any functional-doctrine record by this filing itself; creation of `intelligence/functional_doctrine/` or
any file inside it; any sanitized evidence package (none is required or authorized — the same
`XASSET-0002`/`XASSET-0003` determination that the equity pipeline's redaction apparatus does not
transfer applies here, since no functional-doctrine evidence source embeds portfolio-policy content in
the way Company Intelligence records do); any validator implementation; any resolution of the two
evidence-sufficiency questions §C preserves; any correction of the stale wording in `XASSET-0005`'s
supporting artifact §6.2 disclosed above; or any edit to `XASSET-0001`, `XASSET-0005`, or its supporting
artifact's own text.

### H. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index row);
(3) `operations/WORKSTREAMS.yaml` (`WS-0014` only — the §F updates); (4) `CLAUDE.md` (one concise
Decisions Log pointer entry); (5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded
decision-catalog-count assertions, 99→100, made stale by this filing's own new row). No supporting audit
artifact is created — `XASSET-0005`'s own supporting artifact already contains the complete accepted
process specification for the functional-doctrine schema, and restating it in a second retained document
would duplicate content rather than add evidence, matching `XASSET-0003`'s and `XASSET-0004`'s own
identical determination for the ETF and crypto content authorizations. No `intelligence/` company, theme,
relationship, classification, reconciliation, recommendation, contender, ETF-classification, or
crypto-classification file; no `targets.yaml`/`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`; and
no production allocator/margin code is touched.

### I. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This session does not
review its own work, mark it ready, merge it, or post principal acceptance. Nothing in this decision
becomes effective until this governance PR merges to `main` — including the authorization in §A, which
the future implementation session may not rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `XASSET-0005` already carries a complete,
independently reviewed (two correction rounds, one MAJOR and two MINOR findings all resolved),
principal-accepted, merged, and post-merge-verified specification for every schema, evidence, sequencing,
and validator control functional-doctrine content needs. Re-deriving or rephrasing that content here
would introduce exactly the kind of drift risk this repository's own review history has repeatedly
demonstrated is not hypothetical (`XASSET-0002`'s two MAJOR findings, a phantom numeric field and a
roadmap-numbering inconsistency replicated across three files; `XASSET-0005`'s own supporting artifact
§6.2 stale-wording defect disclosed above, missed by two full correction rounds) — the smaller and more
reliable move is to bind the future implementation to `XASSET-0005`'s own text by reference, unchanged.

**Why this filing authorizes functional-doctrine content only, not overlap-model content.** `XASSET-0001`
§J's separation rule ("framework design versus blind-classification execution... must never be combined")
applies with equal force whether the underlying framework covers one asset type (ETF, crypto) or, as
here, a shared four-type schema plus a separate ten-dimension model that happened to be designed in the
same filing. `XASSET-0005` itself batched the *design* of both under §J's explicit permission for
shape-only work with no asset-specific judgment — but populating a `GLD_DEFENSIVE_ROLE` record and
computing the `sleeve_concentration` dimension are two different content acts requiring two different
evidence standards, two different validator specifications' worth of testing, and, per the direct
ETF/crypto precedent (`XASSET-0002` → `XASSET-0003` + `XASSET-0004`, never combined), two different
authorization filings. Combining them here would repeat the exact batching `XASSET-0001` §J singles out
as prohibited for content, not merely discouraged.

**Why implementation is not folded into this same filing.** This mirrors `XASSET-0003`'s and
`XASSET-0004`'s own identical reasoning: a framework's first-ever content application follows the
`TIER-0004`→`TIER-0005`→separate-Milestone-6-implementation pattern (design, then a dedicated
authorization filing, then a separate implementation PR) rather than the smaller combined-filing pattern
used for incremental content batches under an already-proven framework (`REL-0002`, `PI-0036`) —
functional-doctrine classification is the first-ever application of a brand-new framework, not an
incremental batch under one with existing content precedent.

**Why the two evidence-sufficiency questions (`RESERVE`'s `functional_role`, `DEBT_REDUCTION`'s
`freshness_state`) are preserved rather than settled by this filing.** Settling either here would exceed
this filing's own authorization-only scope — determining whether `RESERVE` deserves a cited
`capital_preservation_buffer` role or must abstain, or whether `holdings.yaml`'s `margin.synced_at` field
is an appropriate freshness citation or itself crosses the contamination boundary, is exactly the kind of
evidence-application judgment `XASSET-0005` §3.6 and this filing's own §C reserve to the drafting session
under independent review, not to a governance-authorization filing that performs no drafting of its own.
Pre-deciding either would also risk exactly the "force a value merely to fill the record" failure mode
this filing's own §C explicitly forecloses.

**Why the stale `XASSET-0005` §6.2 wording is disclosed but not corrected here.** The defect bears
entirely on the overlap model (dimension counts), not on any functional-doctrine content this filing
authorizes — correcting it would be an out-of-scope edit to a different filing's own supporting artifact,
better handled as part of the future `XASSET-0007` overlap-model-content authorization's own preflight,
when that filing will need to read and rely on §6.2's own accurate counts directly.

## Alternatives Considered

- **Combine this authorization with functional-doctrine content in one PR**, matching several smaller
  Company Intelligence batches' combined-filing precedent (`REL-0002`, `PI-0036`, `PI-0038`). Rejected —
  `XASSET-0005`'s own Consequences section and `XASSET-0001` §J's separation rule both require content to
  follow its own separate authorization and implementation lifecycle, matching `XASSET-0003`'s and
  `XASSET-0004`'s own identical treatment of ETF and crypto content, not the smaller-batch pattern used
  for an already-proven equity framework.
- **Authorize both functional-doctrine content and overlap-model content in this same filing**, since both
  were designed together in `XASSET-0005`. Rejected outright — see Rationale; the two are separate content
  domains requiring separate evidence standards and separate review, and combining them would repeat the
  exact batching the ETF/crypto precedent (`XASSET-0002` → separately, `XASSET-0003`/`XASSET-0004`)
  already rejected for content.
- **Resolve the `RESERVE`/`DEBT_REDUCTION` evidence-sufficiency questions in this filing**, stating outright
  which vocabulary value each should receive. Rejected — this filing performs no drafting and has no
  evidence-gathering authority of its own; forcing an answer here would itself be the "force a value
  merely to fill the record" failure mode the functional-doctrine design exists to prevent.
- **Correct `XASSET-0005`'s supporting artifact §6.2 stale wording in this filing**, since it was found
  during this filing's own preflight. Rejected — the defect is entirely overlap-model-scoped and out of
  this functional-doctrine-only filing's bounded package (§H); correcting a different filing's own
  supporting artifact here would exceed this filing's own scope for no functional-doctrine benefit.
- **Create a retained audit artifact restating `XASSET-0005`'s process specification for this filing's own
  supporting evidence.** Rejected — `XASSET-0005` and its supporting artifact are themselves the retained,
  accepted specification; a second document repeating it would be redundant, not additive, matching
  `XASSET-0003`'s and `XASSET-0004`'s own identical determination.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded functional-doctrine
content implementation PR covering all four capital-use types (`CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`,
`DEBT_REDUCTION`), bound exactly to `XASSET-0005`'s specification per §A–E above, gated on its own full
independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle; the
`xasset0006-functional-doctrine-content-authorization` gate transitioning to `status: in_progress`
recording this filing as underway; `WS-0014`'s ordinary self-reference synchronization.

**Not authorized by this filing, now or ever without a further separate decision:** overlap-model content
of any kind (any of the ten dimensions `XASSET-0005` §6 designed — that remains `XASSET-0007`'s future,
unfiled scope); GLD's actual functional/defensive-role determination for the overlap model's own
`defensive_offset_interface` dimension; population of any functional-doctrine record by this filing
itself; any sanitized evidence package; any validator implementation; any edit to `XASSET-0001`,
`XASSET-0005`, or its supporting artifact's own text, including the disclosed stale wording; any
valuation or economic-assessment methodology; any avoided-borrowing-cost calculation; any cross-asset
overlap, concentration, or opportunity-cost synthesis; any sleeve-level or instrument-level sizing; and
any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification Intelligence record, byte-for-byte; the contender
registry; `XASSET-0001`'s and `XASSET-0005`'s own accepted text and scope, in full, unedited (including
the disclosed §6.2 stale wording, left exactly as found); `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s
completed, `status: complete` state; `WS-0015`'s own live state (not touched by this filing); `WS-0014`'s
own `status: proposed`/`priority: secondary` (unedited by this filing).

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ
is not a 27-stock system, and this filing's own bounded four-record authorization does not narrow that
fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical equities;
contender-registry regeneration and legacy-history recovery (`CONTENDER-0002`'s own disclosed gap); QQQ
and any other future ETF candidate expansion; ETF and crypto economic/valuation methodology; equity
Stage-4 valuation execution (`VALUATION-0005`'s own bounded 27-company cohort, not the exhaustive
universe); `XASSET-0007`'s own future overlap-model content; cross-asset opportunity-cost synthesis; any
economic assessment of `CASH`/`RESERVE`/`DEBT_REDUCTION` beyond this filing's own forced-abstention
functional-doctrine content; Level 1 sleeve allocation; Level 2 instrument allocation; `CHART-0003` and
any remaining governed chart ingestion, including higher-timeframe chart governance and fresh
execution-time charts; ladder/deployment integration; unlevered testing; margin/leverage-policy review;
monitoring/sell discipline; final integration and audit; and any true whole-universe allocation test.
