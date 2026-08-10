# WS-0014 Overlap-Model Content Implementation — retained artifact

**Filed under**: `XASSET-0007` (`governance/decisions/XASSET-0007-ws0014-overlap-model-content-authorization.md`)
**Date**: 2026-08-10
**Scope**: implementation only — no new governance decision. `XASSET-0007` is the sole authorization
for this unit (merged via PR #286, merge commit `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`).

This artifact is a factual implementation record, matching the `WS0014_ETF_CLASSIFICATION_
IMPLEMENTATION_20260807.md`/`WS0014_CRYPTO_CLASSIFICATION_IMPLEMENTATION_20260808.md`/
`WS0014_FUNCTIONAL_DOCTRINE_IMPLEMENTATION_20260809.md` precedent — it does not itself authorize
anything; it documents what this one implementation PR did, against the specification `XASSET-0005`
(as corrected by `XASSET-0007` §B) already accepted.

---

## 1. Starting state, independently verified

- Repository: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0007-overlap-model-mqov2k`.
- `HEAD`, `origin/main`, and the current branch all confirmed identical at
  `957d14b7d3ac8e299b3c966d7aeed00f85c03ae0` (`PR #291`'s own merge commit — the immediately prior
  Stage-4 equity valuation-result population lifecycle) before this session's first edit.
- Zero open pull requests confirmed live via the GitHub API.
- `XASSET-0007` independently reconfirmed merged and effective: `governance/decisions.yaml` and
  `operations/WORKSTREAMS.yaml`'s own `xasset0007-post-merge-verification` gate both record accepted
  head `cf478cdbcf10fd930d337e74ada9f72a42e09a92`, merge commit
  `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`, independent review `pullrequestreview-4891559425`
  (APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0/0/0/0), principal acceptance
  `issuecomment-5231939730`, and merge-commit CI success (workflow run `31317721215`).
- `intelligence/overlap_model/` confirmed absent before this implementation began.
- `XASSET-0005` (decision file plus supporting artifact, in full, including both bounded corrections and
  `XASSET-0007`'s own four-location factual correction) and `XASSET-0007` (in full) read directly this
  session.

## 2. What this implementation delivers

Exactly the population `XASSET-0005` §6.1 (as corrected) names — ten sealed dimension records plus one
cohort manifest under `intelligence/overlap_model/`, a new dedicated `overlap_model_validator.py`, and
its own focused test suite (`test_overlap_model_validator.py`). No eleventh dimension, no ninth record
type, no composite.

| `dimension_id` | `dimension_type` | `computation_status` |
|---|---|---|
| `issuer_overlap_etf_lookthrough` | `mechanical_rollup` | `computed_from_existing_mechanism` |
| `economic_role_overlap` | `narrative_evidence` | `computed_from_existing_mechanism` |
| `correlated_loss_mechanisms` | `narrative_evidence` | `computed_from_existing_mechanism` |
| `sleeve_concentration` | `mechanical_rollup` | `computed_from_existing_mechanism` |
| `etf_direct_equity_duplication` | `mechanical_rollup` | `computed_from_existing_mechanism` |
| `leverage_debt_interaction` | `mechanical_rollup` | `computed_from_existing_mechanism` |
| `crypto_correlation_interface` | `interface_placeholder` | `not_yet_computable_interface_only` (forced) |
| `defensive_offset_interface` | `interface_placeholder` | `not_yet_computable_interface_only` (forced) |
| `geographic_currency_exposure` | `interface_placeholder` | `not_yet_computable_interface_only` (forced) |
| `whole_portfolio_volatility_drawdown_concentration` | `interface_placeholder` | `not_yet_computable_interface_only` (forced) |

Six reached `computed_from_existing_mechanism`; four remain forced `not_yet_computable_interface_only`
— exactly the 6/4 split `XASSET-0005` §6.1's corrected table specifies, independently re-derived from
that table before drafting began, not assumed.

## 3. Source mechanism used per dimension (`XASSET-0005` §6.1, as corrected)

Every `source_mechanism` citation on every record is drawn from a closed, per-dimension canonical set
(`overlap_model_validator._CANONICAL_SOURCE_MECHANISMS`) that must equal — not merely overlap with —
the mechanism(s) §6.1's table names for that `dimension_id`. No dimension cites a mechanism the design
did not already identify.

1. **`issuer_overlap_etf_lookthrough`** — `issuer_lookthrough.yaml` (the existing 8% issuer-ceiling /
   40% common-driver-ceiling mechanism and its own 11-issuer, PHQ-2026-01-sourced constituent-weight
   snapshot).
2. **`economic_role_overlap`** — three mechanisms: `intelligence/classification/<TICKER>.yaml:
   economic_role` (the `TIER-0002` four-axis equity schema, not `intelligence/companies/`, which carries
   a different, PI-0001-governed schema with no `economic_role` field), ETF `structural_role.
   role_category`, and crypto `network_fundamentals`.
3. **`correlated_loss_mechanisms`** — `intelligence/relationships/` (the 13 sealed pairwise records,
   `REL-0001` through `REL-0007`'s closed twelve-item taxonomy).
4. **`sleeve_concentration`** — `targets.yaml:destination[].asset_class` (the 37-row destination list,
   plus `caps.clusters` for the equity sleeve's own three sub-groupings).
5. **`etf_direct_equity_duplication`** — the ETF framework's own sealed `overlap_and_concentration`
   axis, per fund (SPY, VEA, VWO, GLD).
6. **`crypto_correlation_interface`** — crypto `correlation_and_volatility.cross_coin_correlation_
   status` (forced `not_yet_measured` on all three sealed coin records — nothing to compute from yet).
7. **`defensive_offset_interface`** — `GLD_DEFENSIVE_ROLE.yaml:capital_preservation_character` (now
   sealed and populated, per `XASSET-0006`'s own merged implementation — see §5 below for why this does
   not loosen the forced value).
8. **`leverage_debt_interaction`** — two mechanisms: `margin_state.py:classify_margin_state` (existence
   and closed four-state vocabulary, cited, never recomputed) and `DEBT_REDUCTION.yaml:hard_constraint_
   status` (the sealed functional-doctrine record's own binding-`true` citation of the 1.8x leverage cap
   and 30% buffer floor).
9. **`geographic_currency_exposure`** — the ETF framework's own `constituent_exposure.geographic_
   concentration`/`.currency_exposure` fields, populated per-instrument for all four ETF records — but
   with no whole-portfolio aggregation mechanism to roll them up across sleeves, and no comparable axis
   on any equity or crypto instrument at all.
10. **`whole_portfolio_volatility_drawdown_concentration`** — crypto `correlation_and_volatility.
    historical_volatility_category` (populated per-coin for all three) — but with no comparable axis on
    any equity or ETF instrument, and no cross-sleeve aggregation mechanism.

## 4. Six computed / four forced — and why

For each of the six `mechanical_rollup`/`narrative_evidence` dimensions, `computed_from_existing_
mechanism` was set only after this session genuinely consulted the cited mechanism (reading
`issuer_lookthrough.yaml` in full; reading representative `intelligence/classification|etf_
classification|crypto_classification` records for their role-equivalent fields; reading all 13
`intelligence/relationships/` records' own existence and taxonomy; reading `targets.yaml`'s full
`destination:` list and `caps.clusters`; reading all four ETF records' `overlap_and_concentration`;
reading `margin_state.py` in full and the sealed `DEBT_REDUCTION.yaml`) and produced a genuine,
evidence-grounded categorical synthesis in `evidence_or_source_refs`/`output_shape`/`uncertainty_or_
gap_disclosure` — never a new numeric measurement (forbidden entirely on this schema, §6 below), and
never an invented mechanism outside what §6.1's table names.

The four `interface_placeholder` dimensions were left exactly where `XASSET-0005` §6.1/§6.2 (as
corrected) require: `computation_status: not_yet_computable_interface_only`, unconditional, with the
genuine gap stated plainly in `uncertainty_or_gap_disclosure` (no cross-coin correlation study
authorized anywhere; no whole-portfolio geographic/currency or volatility/drawdown aggregation
mechanism exists; and — the one case requiring explicit reasoning, not just citation — `defensive_
offset_interface`'s own cited source record, `GLD_DEFENSIVE_ROLE.yaml`, now exists and is sealed.

## 5. Why `defensive_offset_interface` stays forced despite `GLD_DEFENSIVE_ROLE.yaml` now existing

`XASSET-0007` §A point 2 and §D state this explicitly and unconditionally: the forced value applies
"today, with no exception... unconditional on whether the dimension's own cited `source_mechanism` now
points at a populated, sealed record." `XASSET-0006`'s own merged implementation (PR #285) sealed
`GLD_DEFENSIVE_ROLE.yaml` after `XASSET-0005`'s design was already accepted — a fact this filing's own
preflight disclosed but explicitly did not act on, since loosening the forced value would be a schema
amendment neither `XASSET-0005`'s own Consequences section nor `XASSET-0007`'s own bounded authorization
permits. This implementation mechanically enforces that unconditional rule via `overlap_model_
validator.py`'s own two-way `dimension_type` ↔ `computation_status` lock (a record whose `dimension_
type` is `interface_placeholder` must carry the forced value, and vice versa) — a defensive tightening,
never a loosening, of the one-way rule §6.2's own text states. `defensive_offset_interface.yaml`'s own
`evidence_or_source_refs` cites `GLD_DEFENSIVE_ROLE.yaml`'s real, populated
`capital_preservation_category` finding (`market_exposed_via_referenced_structural_asset`) — disclosing
that the pointer now has something real to eventually point at — while its `computation_status` stays
`not_yet_computable_interface_only`, exactly as required.

## 6. Zero numeric fields, no composite score, no cross-schema leakage

- **Zero numeric fields anywhere, no carve-out of any kind** — stricter than the ETF framework's own
  scoped `expense_ratio_pct` exception (`XASSET-0005` §3.3/§6, `XASSET-0007` §B's binding table).
  Independently re-scanned this session: none of the schema's nine substantive fields is itself numeric,
  and the validator's forbidden-key scan runs recursively through every nested string/list/dict value in
  every record.
- **No composite overlap or risk score anywhere** — enforced both structurally (no shared envelope
  across the ten records, per `XASSET-0005` §6.3 point 1) and by a dedicated forbidden-pattern scan
  (`composite_score`, `overall_risk`, `aggregate_concentration`, `overlap_index`, `risk_rank`, or any
  bare `score`/`rank`/`index` key) run both per-record and across the full ten-record set together
  (`overlap_model_validator.validate_overlap_model_directory`'s own combined-scan pass).
- **No cross-schema field-name leakage** — equity- (`economic_role`, `capital_priority`, `risk_
  concentration`, `portfolio_role_ref`, `conviction`, `economic_system_ref`), ETF- (`structural_role`,
  `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`,
  `structure_and_methodology`), crypto- (`network_fundamentals`, `economic_model`, `liquidity_and_
  market_structure`, `custody_and_counterparty_risk`, `correlation_and_volatility`, `regulatory_and_
  structural_uncertainty`), and functional-doctrine-shaped (`capital_use_type`, `functional_role`,
  `hard_constraint_status`, `economic_assessment_readiness`, `liquidity_character`, `capital_
  preservation_character`, `freshness_state`, `structural_reference`, `abstention_index`) key names are
  all independently, individually tested and confirmed absent from every one of the ten sealed records.
- **No `abstention_index`, no `cross_asset_handoff`** — `XASSET-0005` §6.2's own explicit design choices
  for this schema, confirmed absent by dedicated tests.

## 7. Validator architecture

`XASSET-0006` §A point 3 explicitly left the shared-module-versus-two-independent-modules determination
to "whichever content authorization is exercised second" — this implementation is that second
authorization exercised, and it makes the same determination `XASSET-0006` itself already made for its
own relationship to the ETF/crypto validators: **two fully independent sibling modules**, mirroring
`etf_classification_validator.py`/`crypto_classification_validator.py`'s own established precedent. Zero
import coupling between `overlap_model_validator.py` and `functional_doctrine_validator.py`, in either
direction — independently verified via AST-based import inspection (`test_validator_module_has_zero_
import_coupling_with_functional_doctrine_validator`), not a raw substring search (this module's own
docstring legitimately *names* `functional_doctrine_validator.py` in prose, explaining scope — a
substring check would have misflagged that).

`overlap_model_validator.py` reuses the general validation *pattern* every prior Intelligence framework
validator in this repository already established (canonical hashing excluding only the five seal fields;
closed schema at every level with extra-key rejection, not just missing-key checks; an independent
free-text scan for forbidden phrases, directive words, and chart terminology; filesystem-as-index
directory validation treating a missing directory as valid zero-coverage state; bidirectional manifest
reconciliation) — while implementing a schema genuinely smaller and flatter than every prior framework's
own (no envelope, no conditional per-type shape, no provenance-with-access-status object, no structural-
reference hash-pin mechanism), matching `XASSET-0005` §6.2's own deliberately simpler design for this
one dimension-record schema.

## 8. Test inventory

`test_overlap_model_validator.py` — 199 focused tests: happy path for every one of the ten `dimension_
id` values (both draft and sealed); malformed root/envelope rejection; missing required field rejection
(each of the nine substantive fields individually, plus `record_status`); extra-key rejection at the top
level, and the two schema-design-choice tests confirming `abstention_index`/`cross_asset_handoff` are
themselves rejected as unknown keys on this schema; wrong/empty `dimension_id` rejection; wrong
`dimension_type` rejection and the two-way `dimension_type`↔`dimension_id` lock; the forced-value
violation test on **all four** `interface_placeholder` dimensions individually, both non-forced values
tested against each (`XASSET-0007` §B's own corrected test-specification item, which named only two
dimensions before correction); the converse test that no `mechanical_rollup`/`narrative_evidence`
dimension may use the forced interface-only value; the explicit `GLD_DEFENSIVE_ROLE`-now-exists
non-loosening test; unauthorized/subset/superset/duplicate/cross-dimension `source_mechanism` rejection;
`evidence_or_source_refs`/`output_shape`/`uncertainty_or_gap_disclosure`/`later_governance_action`
empty-value rejection; forbidden numeric-leakage-key rejection, individually, for every named term, with
an explicit test confirming this schema carries zero positive-numeric-acceptance test (unlike the ETF
framework's own `expense_ratio_pct` carve-out); forbidden composite-score-key rejection individually,
plus the dedicated across-the-full-ten-record-set test; cross-schema field-name leakage, individually,
per source schema (equity/ETF/crypto/functional-doctrine); nested-depth leakage detection; duplicate/
missing/extra `dimension_id` in the cohort manifest; manifest hash mismatch; malformed manifest row;
non-mapping manifest; chart-terminology leakage per term; directive-word leakage per word, plus three
false-positive guards (`holdings`, `address`, `exiting`); forbidden recommendation-shaped-phrase and
percent-of-book-pattern rejection; filename-stem mismatch, missing-file, empty-file, and malformed-YAML
rejection; draft-record seal-check skip; sealed-record missing-seal-field and wrong-hash rejection;
wrong `record_status` value rejection; deterministic hashing (three angles: repeat calls, seal-field
exclusion, content-change sensitivity) and deterministic repeated directory validation; the allocator/
margin-state import-coupling isolation test (AST-based, both directions) and the functional-doctrine
sibling-module isolation test; protected-path isolation (both the seven named production files and every
existing `intelligence/` framework's own records, via live `git status`); a `governance/decisions`
untouched check; module-constant self-consistency checks (population coverage, the interface-placeholder/
mechanical-or-narrative partition); and eleven real-repository directory-scan tests (exact ten-record
population and seal state; the four forced dimensions' actual values; the six non-forced dimensions'
actual values; a zero-numeric-value structural re-scan of the real sealed corpus; the explicit
`defensive_offset_interface`-cites-GLD-but-stays-forced check against the real file; and bidirectional
manifest/hash reconciliation against the real corpus).

## 9. Manifest / hash reconciliation

`intelligence/overlap_model/COHORT_MANIFEST.yaml` lists all ten `dimension_id` values exactly once each,
each row's `content_sha256` independently recomputed (via `overlap_model_validator.canonical_record_
hash`) and confirmed to match both the manifest row and the sealed record's own `content_sha256` field —
zero mismatches. `overlap_model_validator.py` run standalone against the real directory:
`overlap_model_validator: OK (11 result(s))` (10 records + 1 manifest check).

## 10. No-generator decision

Per `XASSET-0007` §A point 7, a single implementation pass with no per-dimension PR structure and no
multi-shard isolation apparatus was used — the population is fixed and small (ten), matching `XASSET-
0002`'s and `XASSET-0006`'s own established determination that shard isolation is unnecessary at
comparable or smaller scale (ETF ≤4, crypto 3, functional-doctrine 4). No generator module was built —
the ten records were hand-drafted (via a one-time, non-committed local script computing each record's own
`content_sha256` deterministically through the real `overlap_model_validator.canonical_record_hash`
function, then validated clean before being written to disk) since the population is fixed, small, and
not expected to be regenerated on a recurring basis, matching this repository's own established
precedent that a generator is reserved for populations large enough, or recurring enough, to warrant one
(contrast `contender_registry_generator.py`'s 84-entry, regeneratable population).

## 11. Disclosed necessary correction outside `intelligence/overlap_model/`

One pre-existing test, `test_functional_doctrine_validator.py::test_real_functional_doctrine_no_
overlap_model_directory_exists`, asserted `intelligence/overlap_model/` does not exist — accurate only
before this authorized content existed, and made stale by this implementation's own authorized creation
of that directory. Renamed and rewritten to assert the directory now exists, and that `functional_
doctrine_validator.py` correctly performs no cross-schema validation against it (pointing the
functional-doctrine validator at a directory of overlap-model records — none of which carries a
`capital_use_type` field — correctly fails, confirming no accidental cross-schema acceptance) — the same
scaffold-superseded-by-authorized-content pattern already applied repeatedly elsewhere in this
repository's own history (e.g. the ETF/crypto/valuation validators' own `TestZeroRealCompanyPopulation`
→ `TestAuthorizedCohortPopulation` precedent). No `intelligence/functional_doctrine/` data file, no
`functional_doctrine_validator.py` logic, and no other test in that file was touched.

## 12. Protected-path scan

Zero diff (`git status --porcelain`) on: `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_
lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing `intelligence/
classification|companies|themes|relationships|reconciliation|recommendations|contenders|etf_
classification|crypto_classification|valuation_archetype|valuation_evidence|valuation_results|
functional_doctrine/` record, every existing `governance/decisions/*.md` file, and `governance/
decisions.yaml`.

## 13. Full validation

- `overlap_model_validator.py` standalone: `OK (11 result(s))`.
- `functional_doctrine_validator.py` and all twelve other pre-existing repository validators
  (`classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`,
  `relationship_validator.py`, `intelligence_validator.py`, `freshness_validator.py`, `contender_
  registry_validator.py`, `etf_classification_validator.py`, `crypto_classification_validator.py`,
  `valuation_archetype_validator.py`, `valuation_evidence_validator.py`, `valuation_result_validator.py`)
  all clean and unaffected.
- `test_overlap_model_validator.py`: 199/199 passed.
- Full repository `pytest`: **4417 passed, 0 failed** (4218 pre-existing baseline + 199 new, exact
  match; 1 pre-existing, unrelated `DeprecationWarning`).
- Decision catalog (`portfolio_hq.dashboard.decisions.build_catalog`): **104 decisions, `issues == ()`**
  — unchanged; no new governance decision filed by this implementation.
- Repo-wide YAML/YML parse: 245 files, 0 errors. JSON parse: 178 files, 0 errors.
- `git diff --check`: clean.
- Exact changed-file inventory: 11 new files under `intelligence/overlap_model/` (10 dimension records +
  `COHORT_MANIFEST.yaml`), `overlap_model_validator.py` (new), `test_overlap_model_validator.py` (new),
  this retained audit (new), `test_functional_doctrine_validator.py` (modified — §11 above),
  `operations/WORKSTREAMS.yaml` (modified — Lane M synchronization), `CLAUDE.md` (modified — one
  Decisions Log pointer entry). **17 files total** — differs from the task's own pre-computed 16-file
  estimate by exactly the one disclosed, necessary `test_functional_doctrine_validator.py` correction
  (§11), which that estimate could not have anticipated.

## 14. Explicit non-authority

This implementation performs no cross-asset synthesis, determines no GLD portfolio-policy defensive role
beyond what `GLD_DEFENSIVE_ROLE.yaml` already sealed, computes no avoided-borrowing-cost or economic-
assessment conclusion, and changes no tier/target/holdings/role/cluster/cap/gate/allocator/margin/
ladder/chart/order/trade. Every one of the ten records this implementation delivers is an input to a
future, separately authorized cross-asset synthesis (`XASSET-0001` §E/§F, `WS-0014` item 9 — wholly
unauthorized here) — never itself an allocation decision.

## 15. Whole-project boundary (unchanged by this implementation)

Still unfinished, still unauthorized here: the 26 researched non-canonical equities; contender-registry
regeneration and legacy-history recovery; QQQ and any other future ETF candidate expansion; ETF and
crypto economic/valuation methodology; equity Stage-4 valuation execution beyond the sealed 27-company
cohort; any economic assessment of `CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE`/`DEBT_REDUCTION` beyond the
already-sealed forced-abstention functional-doctrine content; cross-asset opportunity-cost synthesis;
Level 1 sleeve allocation; Level 2 instrument allocation; `CHART-0003` and any remaining governed chart
ingestion; ladder/deployment integration; unlevered testing; margin/leverage-policy review; monitoring/
sell discipline; final integration and audit; and any true whole-universe allocation test.

This implementation populates only the `XASSET-0007` governed overlap-model evidence layer. It does not
perform cross-asset synthesis, determine portfolio weights, change any holding/target/tier/gate/
allocation, or authorize any trade.
