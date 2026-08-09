---
decision_id: XASSET-0007
date: 2026-08-09
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0004, TIER-0005, TIER-0007, TIER-0009, REL-0001, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006]
supporting_artifact: null
file: governance/decisions/XASSET-0007-ws0014-overlap-model-content-authorization.md
---

## Context

### Authority for this unit

`XASSET-0005` designed, as text only, a ten-dimension cross-asset overlap/concentration-model
architecture (`XASSET-0001` §J step 7's shape-only portion), batched in the same filing as the
functional-doctrine architecture design under §J's explicit permission to batch "cash/GLD/debt doctrine
+ overlap-model **architecture** (steps 6–7) — permitted to batch only where no asset-specific judgment
occurs." `XASSET-0006` then authorized functional-doctrine **content** only (step 6's content half) and
explicitly, repeatedly deferred overlap-model content to "a separate, future, unfiled `XASSET-0007`
authorization, never combined with this filing" (`XASSET-0006` §A, §G, Rationale, Consequences). This
filing is that authorization — the direct analogue of `XASSET-0003`/`XASSET-0004` for the overlap-model
content step, and the second of the two content authorizations `XASSET-0005`'s own batched design
filing always required to follow it separately (matching `XASSET-0002` → `XASSET-0003` + `XASSET-0004`
exactly).

**Packaging determination, reverified directly against `XASSET-0001` §J and `XASSET-0006`'s own text**:
functional-doctrine content (already authorized and implemented — `XASSET-0006`, PR #284/#285, both
merged) and overlap-model content are two genuinely separate content domains sharing only a batched
*design* filing (`XASSET-0005`), exactly as ETF and crypto content shared only their batched design
filing (`XASSET-0002`). This filing authorizes **overlap-model content only**. It touches no
functional-doctrine record, validator, or test file.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/xasset-0007-overlap-auth-25p7xx`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e` — the `XASSET-0006`-authorized functional-doctrine content
  implementation's own merge commit (PR #285).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #285`'s full lifecycle independently re-verified via the GitHub API, not assumed**: accepted
  head `6b01003e2ff01cec4b8570982e762c74ec88994e`; original independent exact-head review
  (`pullrequestreview-4891363944`, CHANGES REQUIRED — 0 BLOCKING / 0 MAJOR / 1 MINOR / 0 NOTE, a
  documentation-accuracy defect: the retained audit and `CLAUDE.md` described the directive-word
  citation exemption as covering three fields when the shipped `functional_doctrine_validator.py` only
  exempts two — `source_identifier`/`limitation`, with `hard_constraint_status.constraint_source`
  actually scanned like any other field); bounded correction (commit
  `6b01003e2ff01cec4b8570982e762c74ec88994e`, exactly two prose files changed, no code/test/record
  impact); independent exact-head delta review (`pullrequestreview-4891429831`, **APPROVED FOR
  PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE); principal acceptance
  (`issuecomment-5231735706`, accepted head `6b01003e2ff01cec4b8570982e762c74ec88994e`); merge (merge
  commit `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e`, parents
  `e172e4168108d58f5eb295130e741c1fed87d954` and `6b01003e2ff01cec4b8570982e762c74ec88994e`, both
  independently re-confirmed via `git show -s --format='%H %P'`, merge-tree confirmed byte-identical to
  the accepted head's own tree — zero drift at merge). WS-0014 step 6's own content half
  (functional-doctrine record population) is therefore complete and merged.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id:
  WS-0014`): `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`, `active_branch:
  claude/functional-doctrine-ws-0014-sczqi8`, `active_pr: 285`, `last_verified_main_sha:
  e172e4168108d58f5eb295130e741c1fed87d954`, `last_verified_date: "2026-08-09"` — stale relative to
  current `main` (`c90eb6f...`), since `WS-0014`'s own self-reference fields were last touched by
  `XASSET-0006`'s governance filing before PR #285 (the implementation) actually merged; this filing
  performs the ordinary self-reference synchronization (§F below) plus the required Lane M addition
  confirming PR #285's own confirmed post-merge state — the `xasset0006-functional-doctrine-
  content-implementation` gate's own historical text is left unedited, per this repository's
  established convention.
- **`XASSET-0001` (§D, §E, §F, §J, §M, in full), `XASSET-0005` (decision file plus supporting artifact,
  in full), and `XASSET-0006` (in full) read directly this session**, not summarized from memory.
- **`intelligence/functional_doctrine/{CASH,RESERVE,GLD_DEFENSIVE_ROLE,DEBT_REDUCTION}.yaml` and
  `functional_doctrine_validator.py` independently read** — all four sealed, `record_status: sealed`
  confirmed. **A fact worth disclosing, not a reason to change anything today**: `XASSET-0005` §6.1's
  own table describes the `defensive_offset_interface` dimension's source mechanism
  (`GLD_DEFENSIVE_ROLE`/`capital_preservation_character`) as "currently unpopulated (no record exists),
  so this dimension has nothing to point at yet" — that framing narrative is now stale, since
  `GLD_DEFENSIVE_ROLE.yaml` exists and is sealed as of `XASSET-0006`'s own merged implementation
  (`functional_role.role_category: defensive_offset_or_ballast`,
  `capital_preservation_character.capital_preservation_category:
  market_exposed_via_referenced_structural_asset`). **This does not change the governing rule**:
  `XASSET-0005` §6.2 forces `computation_status: not_yet_computable_interface_only` on every
  `interface_placeholder` dimension "today, with no exception" — an unconditional schema rule, not a
  fact contingent on whether a record happens to exist to point at. This filing does not amend that
  forced-value rule (doing so would be a schema redesign, which neither `XASSET-0005`'s own
  Consequences section nor this filing's own bounded authorization scope permits) — it is disclosed
  here as a preflight fact for the future implementing session's own awareness, kept entirely separate
  from the bounded factual correction in the next preflight bullet.
- **`issuer_lookthrough.yaml`, `targets.yaml`'s `caps.clusters` and `destination:` weights, and
  `intelligence/relationships/` (all 13 sealed records) independently re-read** — confirmed live as the
  cited `source_mechanism` targets for the six `mechanical_rollup`/`narrative_evidence` dimensions
  (`XASSET-0005` §6.1's table).
- **`margin_state.py` independently re-read in full**: `classify_margin_state()` remains a pure
  calculator with no persisted output artifact — confirming `XASSET-0005` §7 point 12's rule (cite,
  never import) is the only workable evidence path for `leverage_debt_interaction`.
- **A genuine, disclosed, unresolved stale-wording defect in `XASSET-0005`'s own supporting artifact,
  independently reconfirmed by direct inspection this session — three occurrences at §6.2, exactly as
  `XASSET-0006` disclosed (lines 513–518 and 531 of the file as currently committed), plus a fourth,
  same-class occurrence in §8's test specification (line 684) that `XASSET-0006` did not itself name**:
  §6.2 twice states "the two `interface_placeholder` dimensions," naming only
  `crypto_correlation_interface` and `defensive_offset_interface`, and once states "the five
  `mechanical_rollup`/`narrative_evidence` dimensions" — all three stale from before `XASSET-0005`'s own
  first bounded correction added `geographic_currency_exposure` and
  `whole_portfolio_volatility_drawdown_concentration`, raising the corrected §6.1 table (independently
  re-tallied this session, dimension-by-dimension) to **4 `interface_placeholder` dimensions**
  (`crypto_correlation_interface`, `defensive_offset_interface`, `geographic_currency_exposure`,
  `whole_portfolio_volatility_drawdown_concentration`) **and 6 `mechanical_rollup`/`narrative_evidence`
  dimensions** (`issuer_overlap_etf_lookthrough`, `economic_role_overlap`, `correlated_loss_mechanisms`,
  `sleeve_concentration`, `etf_direct_equity_duplication`, `leverage_debt_interaction`) — 10 total,
  matching the population `XASSET-0005`'s own corrected text states everywhere else. The fourth
  occurrence, independently found this session (not previously disclosed by `XASSET-0006`, which named
  only the three §6.2 instances): §8's test-specification item "`overlap_model` `computation_status`
  forced-value violation: `crypto_correlation_interface` or `defensive_offset_interface` carrying any
  value other than `not_yet_computable_interface_only` rejected" likewise names only two of the four
  dimensions the forced-value rule actually governs — the identical stale-enumeration defect, one
  section over, in the artifact's own required test inventory rather than its field-by-field design
  prose. **Governing determination**: all four occurrences are purely factual/editorial — each is a
  direct enumeration or count of entries in `XASSET-0005` §6.1's own table, a table this session
  independently re-verified is itself already correct and complete (corrected by `XASSET-0005`'s own
  first bounded correction). Fixing the count to match a table the design filing itself already states
  is factual reconciliation, not architectural redesign — no dimension is added, removed, renamed, or
  given a different `dimension_type`, `source_mechanism`, or forced value; the correction changes
  nothing about *what* is forced or *why*, only which of the four already-forced dimensions the prose
  and the test-specification item actually name. Per this filing's own bounded authorization scope,
  this correction is folded in below (§B) as the smallest possible textual fix to `XASSET-0005`'s
  supporting artifact — the decision file's own Decision/Rationale/Alternatives/Consequences text is
  untouched, and the schema, closed vocabularies, forced-value rule, evidence sourcing, and validator/
  test specification are otherwise unedited.
- **Decision catalog independently rebuilt**: **100 decisions, `issues == ()`** at the starting head,
  100 non-`README.md` files in `governance/decisions/` reconciling 1:1. `XASSET-0007` confirmed unused:
  zero matches in `governance/decisions.yaml`, zero matches via full-repository grep;
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new
  decision domain needs one") is satisfied by continuing the existing `XASSET-####` series — this
  filing is the direct continuation of `XASSET-0001` §J step 7's content half, not a genuinely new
  decision domain, mirroring `XASSET-0003`'s/`XASSET-0004`'s/`XASSET-0006`'s identical continuation of
  steps 4, 5, and 6.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing does three things, in one bounded PR:

1. **Performs the ordinary `WS-0014` self-reference synchronization** (`active_branch`,
   `last_verified_main_sha`, `last_verified_date`) reflecting this session's own live-state
   verification, plus one additive Lane M gate confirming `PR #285`'s own now-confirmed post-merge
   state — no prior gate's historical text is edited (§F below).
2. **Corrects, as a narrowly bounded factual reconciliation, the four stale dimension-count/enumeration
   occurrences in `XASSET-0005`'s own supporting artifact §6.2 and §8** disclosed above — "two" → "four"
   (naming all four `interface_placeholder` dimensions) and "five" → "six" (naming the count of
   `mechanical_rollup`/`narrative_evidence` dimensions), plus the §8 test-item's own two-dimension
   enumeration corrected to name all four forced-value dimensions. No other text in `XASSET-0005`'s
   decision file or supporting artifact is touched (§B below).
3. **Authorizes exactly one future, separate, bounded overlap-model (content) implementation pull
   request**, covering all ten dimensions under the exact schema, evidence, sequencing, and
   validator/test controls already specified and accepted through `XASSET-0005` (as corrected by item 2
   above). It performs no population itself, creates no overlap-model record or validator, and
   implements no `intelligence/overlap_model/` content.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007` §1),
any required bounded correction and re-review, explicit principal acceptance, merge, and post-merge
verification — the same lifecycle every prior filing in this chain has followed — may proceed to:

1. Draft and seal one overlap-model record for each of the ten fixed `dimension_id` values named in
   `XASSET-0005` §6.1's table (as corrected by §B below) — `issuer_overlap_etf_lookthrough`,
   `economic_role_overlap`, `correlated_loss_mechanisms`, `sleeve_concentration`,
   `etf_direct_equity_duplication`, `crypto_correlation_interface`, `defensive_offset_interface`,
   `leverage_debt_interaction`, `geographic_currency_exposure`,
   `whole_portfolio_volatility_drawdown_concentration` — zero exclusions, zero additions. No eleventh
   dimension may be introduced without its own separate schema-amendment decision (`XASSET-0005` §6.3's
   own structural no-composite/no-ninth-record-type rule, applied here to forbid an unauthorized
   eleventh record on the same reasoning).
2. For each of the four `interface_placeholder` dimensions (`crypto_correlation_interface`,
   `defensive_offset_interface`, `geographic_currency_exposure`,
   `whole_portfolio_volatility_drawdown_concentration`), set `computation_status` to the forced value
   `not_yet_computable_interface_only`, with no exception — this remains true regardless of whether a
   dimension's own cited `source_mechanism` (e.g., `defensive_offset_interface`'s
   `GLD_DEFENSIVE_ROLE`/`capital_preservation_character` citation) now points at a populated,
   sealed record, per the preflight disclosure above. Changing this forced value for any dimension
   requires its own separate, future, explicit schema-amendment decision — not a determination this
   filing or the implementation it authorizes may make.
3. For each of the six `mechanical_rollup`/`narrative_evidence` dimensions
   (`issuer_overlap_etf_lookthrough`, `economic_role_overlap`, `correlated_loss_mechanisms`,
   `sleeve_concentration`, `etf_direct_equity_duplication`, `leverage_debt_interaction`), the
   implementation may set `computation_status: computed_from_existing_mechanism` once it actually
   performs the cited rollup or cross-reference against that dimension's own named `source_mechanism`
   — `issuer_lookthrough.yaml` for `issuer_overlap_etf_lookthrough`; Company Intelligence
   `economic_role`, ETF `structural_role.role_category`, and crypto `network_fundamentals` for
   `economic_role_overlap`; `intelligence/relationships/` for `correlated_loss_mechanisms`;
   `targets.yaml`'s `destination:` weights aggregated by `asset_class` for `sleeve_concentration`; the
   ETF framework's own `overlap_and_concentration` axis for `etf_direct_equity_duplication`; and a
   **cited, never recomputed**, `margin_state.classify_margin_state()` run for
   `leverage_debt_interaction` — never a new measurement invented outside those named mechanisms
   (`XASSET-0005` §6.1's own table is the exhaustive source-mechanism list; a dimension record whose
   `source_mechanism` names anything else is not authorized, per `XASSET-0005` §6.2's own rule).
4. If, for any of the six dimensions, the implementation determines the evidence available today is
   insufficient to actually perform the rollup or cross-reference with confidence, it must disclose that
   as a genuine gap in `uncertainty_or_gap_disclosure` and leave `computation_status` at
   `requires_future_authorization` rather than force a value — the identical abstention-over-inference
   discipline `XASSET-0005` §3.6 and `XASSET-0006` §C already apply to functional doctrine, restated
   here for the overlap model's own single judgment field.
5. Create the appropriate cohort manifest for the ten sealed records, matching every prior
   classification framework's own `COHORT_MANIFEST.yaml` convention (`XASSET-0005` §6.2's
   `record_status` sealing discipline; §7 point 13's determinism requirement).
6. Build `overlap_model_validator.py` and its dedicated test file. `XASSET-0006` §A point 3 explicitly
   left the question of whether a shared-helper module between `functional_doctrine_validator.py` and
   a future overlap-model validator is warranted to "whichever content authorization is exercised
   second" — this filing is that second authorization, and it makes the same determination `XASSET-0006`
   made for its own relationship to the (at the time nonexistent) ETF/crypto validators: the
   implementing session decides, at implementation time, whether a small shared envelope-level helper
   module is warranted, or whether two fully independent validator modules (mirroring
   `etf_classification_validator.py`/`crypto_classification_validator.py`'s own sibling-module
   precedent) better serve this repository's established one-schema-one-validator-module norm — this
   filing does not pre-decide it, and either outcome is within this authorization's scope provided the
   functional-doctrine schema, its sealed records, and its existing validator are not modified.
7. Use a single implementation pass covering all ten dimensions (no per-dimension PR structure; no
   multi-shard isolation apparatus of any kind) — the population is fixed and small (ten), and
   `XASSET-0002`'s and `XASSET-0006`'s own Rationale sections already established that shard isolation
   is unnecessary at comparable or smaller scale for the ETF (≤4), crypto (3), and functional-doctrine
   (4) sleeves; this filing makes the same determination binding for the overlap model's own
   ten-record population, which is still well within the range those prior determinations already
   covered.
8. Stop after the first record, without a separate pilot authorization, if a systemic schema, evidence,
   or contamination defect is discovered — an internal stop-and-fix condition within the one authorized
   implementation PR, not a license to split into a second governance filing or a per-dimension PR
   structure.

**No functional-doctrine content of any kind is authorized or re-authorized by this filing** — `CASH`,
`RESERVE`, `GLD_DEFENSIVE_ROLE`, and `DEBT_REDUCTION` are already sealed and complete
(`XASSET-0006`/PR #285, merged). This filing does not touch `intelligence/functional_doctrine/`,
`functional_doctrine_validator.py`, or `test_functional_doctrine_validator.py` in any way.

**The overlap model computes evidence, not policy.** Every one of the ten records this filing authorizes
is an input to a future, separately authorized cross-asset synthesis (`XASSET-0001` §E/§F, `WS-0014`
item 9 — wholly unauthorized here) — never itself an allocation decision, a target, a tier, a cap, a
trade recommendation, a composite score, or a ranking engine. Even a fully populated set of ten records
changes zero holdings, targets, caps, clusters, allocator logic, margin behavior, or trades until (1) a
separate future synthesis authority reads them, and (2) a still-separate, human-approved policy decision
adopts any resulting policy change. This one-direction evidence flow is enforced structurally by
`XASSET-0005` §6's own design (no shared envelope across the ten records; no `cross_asset_handoff`
sub-object; no composite score field anywhere) and restated here as this filing's own binding
authorization boundary, not merely a design preference the implementation might relax.

### B. Binding specification — by reference, not restatement, plus the bounded factual correction

The implementation PR must follow `XASSET-0005`'s specification exactly, as accepted and merged at
`1921864326f2cc75609b1c91037c24e333c4e3d0`, **as corrected by this filing** in the four locations named
in the Preflight above. This filing does not redesign, loosen, tighten, or otherwise restate that
specification in its own words beyond the index below and the bounded correction — the implementation
session has no discretion to depart from either:

| Control | Governing section (all `XASSET-0005 §N` citations refer to its supporting artifact, `governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_ARCHITECTURE_DESIGN_20260808.md`, unless the decision file itself is cited) |
|---|---|
| 10-dimension population, zero exclusions, zero additions, no composite record | `XASSET-0005` §6.1 (as corrected by this filing), §6.3 |
| Shared schema across all ten dimension records: `dimension_id`, `schema_version`, `dimension_type` (`mechanical_rollup` \| `narrative_evidence` \| `interface_placeholder`), `source_mechanism`, `computation_status` (`computed_from_existing_mechanism` \| `not_yet_computable_interface_only` \| `requires_future_authorization`), `evidence_or_source_refs`, `output_shape` (categorical only, no numeric field), `uncertainty_or_gap_disclosure`, `later_governance_action`, `record_status` — no `abstention_index`, no `cross_asset_handoff` sub-object (§6.2's own explicit design choices) | `XASSET-0005` §6.2 (as corrected by this filing) |
| Forced `computation_status: not_yet_computable_interface_only` on all four `interface_placeholder` dimensions, zero exception, unconditional on whether a cited source record exists | `XASSET-0005` §6.2 (as corrected by this filing) |
| `computation_status: computed_from_existing_mechanism` permitted only for the six `mechanical_rollup`/`narrative_evidence` dimensions, only once the implementation actually performs the cited rollup/cross-reference against the exact `source_mechanism` §6.1's table names — never a new measurement | `XASSET-0005` §6.1, §6.2 |
| No composite overlap or risk score anywhere, at any level — enforced structurally (no shared envelope, no natural home for a rollup field) and by a dedicated forbidden-pattern validator scan across the full ten-record set | `XASSET-0005` §6.3 |
| Zero numeric fields anywhere, with no carve-out of any kind (stricter than the ETF framework's own scoped `expense_ratio_pct` exception) | `XASSET-0005` §3.3 (closing statement, applies identically to §6), Rationale |
| No cross-schema field-name leakage — no equity- (`economic_role`, `capital_priority`, `risk_concentration`), ETF- (`structural_role`, `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`), crypto- (`network_fundamentals`, `economic_model`, `liquidity_and_market_structure`, `custody_and_counterparty_risk`, `correlation_and_volatility`, `regulatory_and_structural_uncertainty`), or functional-doctrine-shaped (`capital_use_type`, `functional_role`, `hard_constraint_status`, `economic_assessment_readiness`, `liquidity_character`, `capital_preservation_character`, `freshness_state`, `structural_reference`, `abstention_index`) field name anywhere in an overlap-model record | `XASSET-0005` §7 point 4 |
| Allocator/margin decoupling — zero import coupling with `allocate.py`/`margin_state.py` in either direction; `leverage_debt_interaction` may **cite** `margin_state.py`'s output in prose/`evidence_or_source_refs`, the validator module never imports it | `XASSET-0005` §7 point 12 |
| No chart-evidence leakage; no directive/trading-language leakage (the shared eight words — `buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`, word-boundary matched — the four extra debt/cash-specific verbs `repay`/`redeploy`/`fund`/`draw` are functional-doctrine-specific and not required here, though including them is not prohibited if the implementation shares a helper module) | `XASSET-0005` §7 points 9, 10 |
| Deterministic generation; protected-path isolation on `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing `intelligence/classification\|companies\|themes\|relationships\|etf_classification\|crypto_classification\|functional_doctrine/` record, `COHORT_MANIFEST.yaml`, and every existing governance decision file | `XASSET-0005` §7 points 13, 14 |
| Closed schema at every level, rejecting extra keys, not just missing ones (the `contender_registry_validator.py` MAJOR-finding lesson) | `XASSET-0005` §7 point 2, §8.1 |
| Test specification (overlap-model-relevant items: happy-path per `dimension_id`; malformed/extra/missing keys at every level; wrong `dimension_id`; forbidden numeric/score leakage per named term with no positive-acceptance test; the forbidden composite-overlap-score pattern tested against the full ten-record set together, not one record in isolation; cross-schema field-name leakage per source schema; duplicate/missing/extra `dimension_id` against the named population; chart-terminology leakage per term; directive/trading-language leakage per word (the shared eight, plus a false-positive guard for ordinary "fund"/"funded" usage in a citation string if the debt/cash verbs are shared with the functional-doctrine module); the `computation_status` forced-value violation test **on all four `interface_placeholder` dimensions, not merely two** (as corrected by this filing); determinism; protected-path isolation; allocator/margin import-coupling isolation) | `XASSET-0005` §8 (as corrected by this filing), §8.1's four explicitly carried-forward lessons |
| Not applicable to this implementation — functional-doctrine-only controls (`capital_use_type`-conditional shape enforcement, `hard_constraint_status`/`economic_assessment_readiness` independence, `structural_reference`/GLD hash-pin enforcement, `provenance.sources` type/access-status validation, abstention/`abstention_index` behavior) | `XASSET-0005` §7 points 3, 5, 8, 11; §8's functional-doctrine-specific items — already implemented, unaffected, and not touched by this filing |

**The bounded factual correction, applied to `governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_
OVERLAP_CONCENTRATION_ARCHITECTURE_DESIGN_20260808.md` only** (the decision file `XASSET-0005-
functional-doctrine-and-overlap-concentration-architecture.md` is not edited by this filing — its own
Decision/Rationale/Alternatives/Consequences text already states the population correctly as "ten"
throughout, per its own second bounded correction):

1. §6.2, `computation_status` field description — **old**: "For the two `interface_placeholder`
   dimensions (`crypto_correlation_interface`, `defensive_offset_interface`), this field is **forced**
   to `not_yet_computable_interface_only` today... For the five `mechanical_rollup`/`narrative_evidence`
   dimensions, a future implementation may set `computed_from_existing_mechanism`..." — **corrected**:
   "For the four `interface_placeholder` dimensions (`crypto_correlation_interface`,
   `defensive_offset_interface`, `geographic_currency_exposure`,
   `whole_portfolio_volatility_drawdown_concentration`), this field is **forced** to
   `not_yet_computable_interface_only` today... For the six `mechanical_rollup`/`narrative_evidence`
   dimensions, a future implementation may set `computed_from_existing_mechanism`...".
2. §6.2, `uncertainty_or_gap_disclosure` field description — **old**: "for the two
   `interface_placeholder` dimensions, this is where the genuine gap... is stated plainly" —
   **corrected**: "for the four `interface_placeholder` dimensions, this is where the genuine gap... is
   stated plainly".
3. §8, test-specification item — **old**: "`overlap_model` `computation_status` forced-value violation:
   `crypto_correlation_interface` or `defensive_offset_interface` carrying any value other than
   `not_yet_computable_interface_only` rejected" — **corrected**: "`overlap_model` `computation_status`
   forced-value violation: any of the four `interface_placeholder` dimensions
   (`crypto_correlation_interface`, `defensive_offset_interface`, `geographic_currency_exposure`,
   `whole_portfolio_volatility_drawdown_concentration`) carrying any value other than
   `not_yet_computable_interface_only` rejected".

**Why this is factual reconciliation, not architectural redesign**: all three corrected passages are
direct enumerations or counts of entries in `XASSET-0005` §6.1's own dimension table — a table this
filing's own preflight independently re-tallied and confirmed already correct and complete (corrected
by `XASSET-0005`'s own first bounded correction, which added `geographic_currency_exposure` and
`whole_portfolio_volatility_drawdown_concentration` as `interface_placeholder` dimensions but did not
propagate that addition into §6.2's or §8's own later prose). No dimension is added, removed, renamed,
merged, or given a different `dimension_type`, `source_mechanism`, `computation_status` forced value, or
test requirement by this correction — it changes only which of the four already-forced dimensions the
prose and the test-specification item name, bringing both into agreement with the table both are
supposed to describe. This preserves historical auditability: the correction is recorded here, in a
new, separate, later filing, exactly the pattern `XASSET-0005`'s own two prior bounded corrections
(recorded in that filing's own Context and the supporting artifact's own §0) and `XASSET-0006`'s own
disclosure (recorded in its Preflight) already established — a stale count is disclosed, then corrected
by the next filing whose own scope genuinely needs the corrected text to be accurate, never silently
rewritten as though the original had always read that way.

### C. Evidence standard (binding on the future implementation)

The implementing session must use only the evidence sources each dimension's `source_mechanism`
actually names (`XASSET-0005` §6.1's table, §B above): file paths, module public functions, and schema
fields already governed elsewhere in this repository — never a new correlation study, a new relationship
inference, a new cluster-cap determination, or any other primary research. `leverage_debt_interaction`
may cite `margin_state.classify_margin_state()`'s **existence and closed output vocabulary**
(`NORMAL`/`CAUTION`/`RESTRICTED`/`FORCED_DELEVER`), never a live numeric run result computed at
implementation time, mirroring `XASSET-0005` §3.6's identical contamination rule for functional
doctrine. Where a dimension's own named `source_mechanism` genuinely has nothing to compute from yet
(the four `interface_placeholder` dimensions, per the forced value in §A point 2 and §B above) or the
implementation determines the cited mechanism's current state is insufficient to perform a confident
rollup (§A point 4), the framework's own `requires_future_authorization`/disclosure path is the correct
outcome — never a forced or invented value. This filing pre-decides no dimension's actual
`computation_status` beyond the four forced-value dimensions §A point 2 and §B name explicitly; the six
`mechanical_rollup`/`narrative_evidence` dimensions' actual states are determined by the implementing
session's own evidence-gathering, subject to independent review.

### D. Stop conditions (binding on the future implementation)

The implementation PR must stop immediately and disclose, never silently work around: population drift
(an eleventh dimension appearing to be needed, or one of the ten ceasing to apply); any equity-, ETF-,
crypto-, or functional-doctrine-shaped field leakage; any numeric score/rank/target/avoided-cost
leakage of any kind; any composite-overlap-score field of any kind; any chart-domain leakage; any
attempt to force `computed_from_existing_mechanism` on a dimension whose cited `source_mechanism`
cannot actually support it; any attempt to change the forced `not_yet_computable_interface_only` value
on any of the four `interface_placeholder` dimensions; any attempt to determine GLD's actual portfolio
role, an avoided-borrowing-cost figure, or any economic-assessment conclusion (all remain out of this
filing's scope, per `XASSET-0005` §5's own restated seven-step sequencing doctrine); any attempt to
perform cross-asset synthesis, sleeve-level, or instrument-level sizing of any kind; any `margin_state.py`
import into the validator module; any protected-path mutation; or any unexpected target, holdings,
gate, cap, cluster, allocator, margin, ladder, order, or trade change.

### E. Independent review requirement (binding on the future implementation)

The implementation PR's independent exact-head review must verify, at minimum: the exact ten-dimension
population against the corrected `XASSET-0005` §6.1 table; the exact changed-file inventory; schema
conformance for every record; the forced `not_yet_computable_interface_only` value on all four
`interface_placeholder` dimensions with zero exception; for any `mechanical_rollup`/`narrative_evidence`
dimension marked `computed_from_existing_mechanism`, that the cited `source_mechanism` was genuinely
consulted and the record's own evidence citation is traceable to it, not fabricated; absence of a
composite score anywhere, tested against the full ten-record set; absence of any cross-schema field-name
leakage; the validator and its tests against `XASSET-0005`'s supporting artifact §7/§8's full
overlap-model-applicable specification (§B above), including §8.1's four explicitly carried-forward
lessons; CI; protected-path isolation, explicitly including zero diff on
`intelligence/functional_doctrine/*.yaml`; absence of any functional-doctrine content of any kind;
absence of any cross-asset synthesis, sleeve target, instrument target, or GLD/DEBT_REDUCTION economic
determination; and absence of any policy mutation. Any correction requires its own fresh exact-head
delta review before principal acceptance.

### F. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **One new additive gate, `xasset0006-implementation-post-merge-verification`**, recording — without
   editing the `xasset0006-functional-doctrine-content-implementation` gate's own historical text — that
   `PR #285` is fully merged, reviewed, corrected, principal-accepted, and post-merge verified (§ Preflight
   above gives the full independently re-verified chain). Step 6 of `XASSET-0001` §J (functional-doctrine
   record population) is therefore complete.
2. **`active_branch` set to this filing's own branch, `last_verified_main_sha` updated**
   `e172e4168108d58f5eb295130e741c1fed87d954` → `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e`, and
   **`last_verified_date` updated** to this filing's own date — the ordinary self-reference refresh every
   substantive `WS-0014` filing performs.
3. **One new additive gate, `xasset0007-overlap-model-content-authorization`**, recording this filing's
   own branch and (once it exists) PR number — `status: in_progress`, **not** `status: complete`, since
   this filing's own governance PR is itself unmerged, unreviewed, and unaccepted, matching every prior
   filing's identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: step 6 (functional-doctrine content) is
   complete and merged (PR #285); this filing, once merged, authorizes exactly one future overlap-model
   content implementation PR (the content half of step 7 / item 9 of the §I list); items 9
   (cross-asset synthesis, renumbered from the prior entry's own item 9 label, which referred to §J's
   step 8 — see §J's own dependency list for the authoritative 0–13 numbering) through 13 remain wholly
   unauthorized, as do step 2 (additional-equity cohorts) and any economic-assessment step.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`)
is changed — this filing does not begin execution and does not alter the workstream's own standing.
`WS-0015` is not touched by this filing (no genuinely established fold-forward reason or authority
exists for this unrelated `WS-0014` unit to edit it).

### G. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/
ladder change; any trade or order; any chart use of any kind; any buy/sell/hold/trim/exit/wait/stage
recommendation or directive of any kind; population of any overlap-model record by this filing itself;
computation of any of the ten dimensions' actual value by this filing itself; GLD's actual functional/
defensive-role determination (already recorded, not decided, by the sealed `GLD_DEFENSIVE_ROLE.yaml`
record `XASSET-0006` sealed — this filing does not revisit or re-derive it); any valuation or
economic-assessment methodology; any avoided-borrowing-cost calculation; any cross-asset overlap,
concentration, or opportunity-cost synthesis (`XASSET-0001` §E/§F, item 9 of §I's roadmap — wholly
unauthorized here); any sleeve-level or instrument-level sizing; creation of `intelligence/
overlap_model/` or any file inside it; any validator implementation; any resolution of which of the six
`mechanical_rollup`/`narrative_evidence` dimensions' evidence is actually sufficient (§C preserves this
for the implementing session); any change to `XASSET-0001`, `XASSET-0006`, or their own text; and any
edit to `XASSET-0005`'s decision file or supporting artifact beyond the four narrowly bounded factual
corrections named in §B.

### H. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0014` only — the §F updates); (4) `CLAUDE.md` (one concise
Decisions Log pointer entry); (5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded
decision-catalog-count assertions, 100→101, made stale by this filing's own new row); (6)
`governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_ARCHITECTURE_DESIGN_20260808.md`
(the four narrowly bounded factual corrections in §B, nothing else in that file touched). No new
supporting audit artifact is created — `XASSET-0005`'s own supporting artifact, as corrected, already
contains the complete accepted process specification for the overlap model, and restating it in a
second retained document would duplicate content rather than add evidence, matching `XASSET-0003`'s,
`XASSET-0004`'s, and `XASSET-0006`'s own identical determination for their own content authorizations.
No `intelligence/` company, theme, relationship, classification, reconciliation, recommendation,
contender, ETF-classification, crypto-classification, or functional-doctrine file; no `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`; and no production allocator/margin code is
touched.

### I. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This session does not
review its own work, mark it ready, merge it, or post principal acceptance. Nothing in this decision
becomes effective until this governance PR merges to `main` — including the authorization in §A and the
correction in §B, neither of which the future implementation session may rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `XASSET-0005` already carries a complete,
independently reviewed (two correction rounds, one MAJOR and two MINOR findings all resolved),
principal-accepted, merged, and post-merge-verified specification for the overlap model's schema,
evidence, dimension list, and validator/test controls. Re-deriving or rephrasing that content here would
introduce exactly the kind of drift risk this repository's own review history has repeatedly
demonstrated is not hypothetical — the smaller and more reliable move is to bind the future
implementation to `XASSET-0005`'s own text by reference, corrected only where a genuine, narrow,
independently-verified factual staleness would otherwise mislead the implementing session into building
a test or field description that omits two of the four dimensions the forced-value rule actually
governs.

**Why this filing authorizes overlap-model content only, not any further functional-doctrine work.**
Functional-doctrine content is already complete (`XASSET-0006`, PR #284/#285, merged) — there is nothing
further to authorize on that side of `XASSET-0005`'s batched design, and this filing's own bounded
scope (§H) accordingly touches no functional-doctrine file.

**Why the four stale-count occurrences are corrected here rather than left disclosed-only, unlike
`XASSET-0006`'s own treatment of the same defect.** `XASSET-0006` correctly declined to correct
`XASSET-0005`'s supporting artifact, because the defect "bears entirely on the overlap model... not on
any functional-doctrine content this filing authorizes" and "correcting it would be an out-of-scope
edit to a different filing's own supporting artifact, better handled as part of the future `XASSET-0007`
overlap-model-content authorization's own preflight, when that filing will need to read and rely on
§6.2's own accurate counts directly." This filing is exactly that future authorization, and it does
need to read and rely on §6.2's own accurate counts directly — leaving the stale "two"/"five" wording
uncorrected while binding a future implementation to it by reference (§B) would hand that implementation
an authoritative-looking specification that omits two of the four dimensions its own forced-value rule
governs, a defect this filing's own preflight found and can close with a purely mechanical, verifiably
correct fix. The fourth occurrence (§8's own test-specification item) was independently found during
this session's own preflight, not previously disclosed by `XASSET-0006` — corrected on the identical
factual-reconciliation reasoning, since leaving it uncorrected while fixing the other three would
produce an internally inconsistent artifact (accurate field-by-field design prose, still-incomplete test
inventory) and risk a future implementation writing a test that verifies the forced value on only two of
the four dimensions it actually governs.

**Why the `GLD_DEFENSIVE_ROLE`-now-exists fact is disclosed but does not change the forced
`not_yet_computable_interface_only` value.** `XASSET-0005` §6.2's own forced-value rule for the four
`interface_placeholder` dimensions is unconditional ("today, with no exception") — it does not read as
"forced only until a cited source record happens to exist." Treating the record's own existence as
license to compute `defensive_offset_interface` today would be a substantive schema loosening this
filing has no authority to make; `XASSET-0005`'s own Consequences section reserves any such change to
its own future, separate schema-amendment decision. Disclosing the fact without acting on it follows
the identical discipline `XASSET-0006` §C already applied to `RESERVE`'s and `DEBT_REDUCTION`'s own
evidence-sufficiency questions: state what is known, preserve the governing rule, defer any change of
the rule itself to its own separate authorization.

**Why the shared-validator-module determination is left to the implementing session.** `XASSET-0006` §A
point 3 explicitly reserved this determination to "whichever content authorization is exercised
second" — this filing is that authorization, and the same reasoning applies in the other direction now
that `functional_doctrine_validator.py` already exists: whether a small shared envelope-level helper
module (mirroring, e.g., a hypothetical shared classification-hygiene utility) is warranted, or whether
two fully independent modules (mirroring `etf_classification_validator.py`/
`crypto_classification_validator.py`'s own established sibling-module precedent) better serve this
repository's norm, is an implementation-architecture judgment best made once the actual overlap-model
validator code is being written against the actual sealed records — not a design constraint this
authorization filing should pre-impose without seeing that code.

**Why the one-direction evidence-flow boundary is restated as this filing's own binding authorization,
not merely inherited from `XASSET-0005`'s design.** `XASSET-0005` §6's structural choices (no shared
envelope, no `cross_asset_handoff` object, no composite score) already enforce this mechanically for the
schema itself — but the authorization filing that actually permits real evidence to be written into ten
real records is the appropriate place to also state, in its own words, the governance-level consequence
of that structure: that populated evidence, however complete, creates no allocation authority on its
own. This mirrors `CONTENDER-0001`'s own "contender status creates evaluation eligibility only" durable
language and `XASSET-0001` §L's identical pattern of restating a structural guarantee as explicit
governance prose at the point where real content first becomes possible.

## Alternatives Considered

- **Combine this authorization with overlap-model content in one PR**, matching several smaller Company
  Intelligence batches' combined-filing precedent (`REL-0002`, `PI-0036`, `PI-0038`). Rejected —
  `XASSET-0005`'s own Consequences section and `XASSET-0001` §J's separation rule both require content to
  follow its own separate authorization and implementation lifecycle, matching `XASSET-0003`'s,
  `XASSET-0004`'s, and `XASSET-0006`'s own identical treatment of ETF, crypto, and functional-doctrine
  content, not the smaller-batch pattern used for an already-proven equity framework.
- **Leave the stale "two"/"five" wording disclosed-only, exactly as `XASSET-0006` left it.** Rejected —
  see Rationale; this filing is the specific future unit `XASSET-0006` itself named as the correct place
  to fix it, since this filing's own binding-by-reference table (§B) would otherwise propagate a
  materially incomplete specification to a real implementation.
- **Correct the stale wording via an edit to `XASSET-0005`'s own decision file text** rather than only its
  supporting artifact. Rejected — the decision file's own Decision/Rationale/Alternatives/Consequences
  text already states the population correctly as "ten" throughout (confirmed by this filing's own
  preflight); only the supporting artifact carries the four stale occurrences, so only it needs the
  correction.
- **Treat the `GLD_DEFENSIVE_ROLE`-now-exists fact as license to permit `computed_from_existing_mechanism`
  on `defensive_offset_interface` today.** Rejected outright — see Rationale; `XASSET-0005`'s own forced
  value is unconditional, and loosening it is a schema-amendment decision this filing has no authority to
  make.
- **Pre-decide the shared-validator-module architecture question in this filing**, rather than leaving it
  to the implementing session. Rejected — `XASSET-0006` §A point 3 already reserved this determination to
  the second content authorization, and pre-imposing an architecture choice without seeing the actual
  validator code being written would risk exactly the kind of premature specification this filing's own
  Rationale (on why it authorizes rather than redesigns) argues against.
- **Create a retained audit artifact restating `XASSET-0005`'s process specification for this filing's own
  supporting evidence.** Rejected — `XASSET-0005` and its (now corrected) supporting artifact are
  themselves the retained, accepted specification; a second document repeating it would be redundant, not
  additive, matching `XASSET-0003`'s, `XASSET-0004`'s, and `XASSET-0006`'s own identical determination.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded overlap-model
content implementation PR covering all ten dimensions (`issuer_overlap_etf_lookthrough`,
`economic_role_overlap`, `correlated_loss_mechanisms`, `sleeve_concentration`,
`etf_direct_equity_duplication`, `crypto_correlation_interface`, `defensive_offset_interface`,
`leverage_debt_interaction`, `geographic_currency_exposure`,
`whole_portfolio_volatility_drawdown_concentration`), bound exactly to `XASSET-0005`'s specification as
corrected per §A–E above, gated on its own full independent-review/correction/re-review/
principal-acceptance/merge/post-merge-verification lifecycle; the `xasset0007-overlap-model-content-
authorization` gate transitioning to `status: in_progress` recording this filing as underway; the
`xasset0006-implementation-post-merge-verification` gate confirming step 6's own completion; `WS-0014`'s
ordinary self-reference synchronization; four narrowly bounded factual corrections to `XASSET-0005`'s
supporting artifact §6.2/§8, disclosed above with old and new wording both preserved for the historical
record.

**Not authorized by this filing, now or ever without a further separate decision:** population of any
overlap-model record by this filing itself; computation of any dimension's actual value by this filing
itself; loosening the forced `not_yet_computable_interface_only` value on any `interface_placeholder`
dimension; GLD's actual portfolio-policy defensive role beyond what `GLD_DEFENSIVE_ROLE.yaml` already
records; any valuation or economic-assessment methodology; any avoided-borrowing-cost calculation; any
cross-asset overlap, concentration, or opportunity-cost synthesis; any sleeve-level or instrument-level
sizing; any validator implementation; any redesign of `XASSET-0005`'s schema, closed vocabularies, or
forced values beyond the four bounded factual corrections in §B; any edit to `XASSET-0001` or
`XASSET-0006`'s own text; and any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/
trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification/functional-doctrine Intelligence record,
byte-for-byte; the contender registry; `XASSET-0001`'s and `XASSET-0006`'s own accepted text and scope,
in full, unedited; `XASSET-0005`'s own decision file text and every part of its supporting artifact
beyond the four bounded factual corrections in §B; `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the 1.8x leverage cap and 30%
margin-buffer floor; the Constitution; `WS-0005`'s completed, `status: complete` state; `WS-0015`'s own
live state (not touched by this filing); `WS-0014`'s own `status: proposed`/`priority: secondary`
(unedited by this filing).

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ
is not a 27-stock system, and this filing's own bounded ten-record authorization does not narrow that
fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical equities;
contender-registry regeneration and legacy-history recovery (`CONTENDER-0002`'s own disclosed gap); QQQ
and any other future ETF candidate expansion; ETF and crypto economic/valuation methodology; equity
Stage-4 valuation execution (`VALUATION-0005`'s own bounded 27-company cohort, not the exhaustive
universe); any economic assessment of `CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE`/`DEBT_REDUCTION` beyond the
already-sealed forced-abstention functional-doctrine content; cross-asset opportunity-cost synthesis;
Level 1 sleeve allocation; Level 2 instrument allocation; `CHART-0003` and any remaining governed chart
ingestion, including higher-timeframe chart governance and fresh execution-time charts; ladder/
deployment integration; unlevered testing; margin/leverage-policy review; monitoring/sell discipline;
final integration and audit; and any true whole-universe allocation test.
