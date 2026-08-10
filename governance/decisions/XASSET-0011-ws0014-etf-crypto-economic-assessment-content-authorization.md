---
decision_id: XASSET-0011
date: 2026-08-10
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, VALUATION-0001, VALUATION-0002, VALUATION-0004, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002]
supporting_artifact: null
file: governance/decisions/XASSET-0011-ws0014-etf-crypto-economic-assessment-content-authorization.md
---

## Context

### Authority for this unit

`XASSET-0010` designed, as text only, a closed economic-assessment methodology for exactly six
already-classified instruments — `SPY`, `VEA`, `VWO` (ETF) and `BTC`, `ETH`, `SOL` (crypto) — closing the
remainder of `XASSET-0005` §5 step 2's own restated sequence ("perform asset-appropriate valuation/economic
assessment") that `XASSET-0008`/`XASSET-0009` left open (`GLD`/`CASH_LIKE_CAPITAL` only). `XASSET-0010` §A
names five stages and states plainly that it authorizes stage 1 (methodology design) only: stage 2 ("future,
separate content authorization — not performed here; requires its own future, explicit principal
authorization, mirroring `XASSET-0003`'s/`XASSET-0004`'s/`XASSET-0009`'s own role for the ETF, crypto, and
GLD/CASH_LIKE_CAPITAL content steps") is exactly this filing. This filing is the direct analogue of
`XASSET-0003`, `XASSET-0004`, and `XASSET-0009` for this economic-assessment content step — authorization
only, binding by reference to `XASSET-0010`'s already-accepted design, no restatement, no redesign.

**Batching determination — one filing, one future implementation PR, both asset classes, no split
required.** `XASSET-0010` §D.7 explicitly left open whether a future content-authorization filing would
cover all six instruments in one unit, split by asset type (mirroring `XASSET-0003`/`XASSET-0004`'s own
separate-content precedent), or some other bounded split — "that remains the future authorization filing's
own choice to make and justify." The controlling principal has explicitly directed exactly one combined
authorization here, and the repository's own precedent supports it: `XASSET-0010` designed **one shared
envelope and one shared structural-reference mechanism** across both sub-populations (`XASSET-0010` §D,
supporting artifact §4) and explicitly names **one dedicated validator module**
(`instrument_economic_assessment_validator.py`, `XASSET-0010` §J, supporting artifact §9) covering all six
`instrument_id` values under one `asset_type`-conditional schema — not two independently-shaped classification
frameworks that happen to share a filing. This is structurally the same shape `XASSET-0006` used for the
four-type functional-doctrine population and `XASSET-0009` used for the two-subject `GLD`/`CASH_LIKE_CAPITAL`
population (one shared schema, one validator, one authorization, one implementation PR) — not the
`XASSET-0002`→`XASSET-0003`+`XASSET-0004` shape, which split two genuinely separate, asset-type-specific
**classification** frameworks each with their own full, independent field set at the classification layer.
Splitting this filing into an ETF-only and a crypto-only authorization would fragment one already-unified
envelope/validator specification for no review benefit, the same reasoning `XASSET-0009`'s own Rationale
already applied to the smaller `GLD`/`CASH_LIKE_CAPITAL` population, here applied to a six-member population
sharing the identical structural-reference mechanism and validator module.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0011-etf-crypto-content-auth-7a3e84`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `5b2e3be1419cc54ed7c5903960e38d5b44dbc2ec` — the merge commit of `PR #295` (`XASSET-0010`'s own
  methodology-design filing).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #295`'s full lifecycle independently re-verified via the GitHub API, not assumed**: merged
  (`merged: true`, `merged_by: Mast3rkey`), head `bd04cda9eaa12c4a7da269a27b963eb222010f33`, base `main` @
  `3a7c89e6f4137c7ee37c643af1dc3f6a58d4912c`, 6 changed files, 1 commit, merge commit
  `5b2e3be1419cc54ed7c5903960e38d5b44dbc2ec` (parents independently confirmed via `git log --pretty`).
  **`XASSET-0010` is therefore merged and effective** — the closed six-instrument methodology design is
  live, accepted specification.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`, `active_branch:
  claude/etf-crypto-assessment-methodology-7ybkis`, `active_pr: None`, `last_verified_main_sha:
  3a7c89e6f4137c7ee37c643af1dc3f6a58d4912c`, `last_verified_date: "2026-08-10"` — the
  `last_verified_main_sha` field is itself stale relative to `PR #295`'s own now-confirmed merge (the same
  self-referential pattern this repository's convention explicitly defers to "the next filing that
  substantively touches the workstream"), and its most recent milestone,
  `xasset0010-etf-crypto-economic-assessment-methodology-design`, is `status: in_progress`, `pr: None` —
  this filing performs the deferred synchronization (§F below) without editing that milestone's own text.
- **Decision catalog independently rebuilt**: **106 decisions, `issues == ()`** at the starting head, 106
  non-`README.md` files in `governance/decisions/` reconciling 1:1. `XASSET-0011` confirmed the next unused
  identifier — zero matches in `governance/decisions.yaml`, zero matching filename in
  `governance/decisions/`, for the literal string `XASSET-0011`. `governance/decisions/README.md`'s own
  rule ("a new prefix is chosen only when a genuinely new decision domain needs one") is satisfied by
  continuing the existing `XASSET-####` series — this filing is the direct continuation of `XASSET-0010`
  §A stage 2, not a genuinely new decision domain, mirroring `XASSET-0003`'s, `XASSET-0004`'s,
  `XASSET-0006`'s, `XASSET-0007`'s, and `XASSET-0009`'s identical continuation.
- **`XASSET-0001` (§B, §J), `XASSET-0002` (as the direct ETF+crypto classification-batching precedent),
  `XASSET-0006`/`XASSET-0007` (as the four-type/ten-dimension combined-authorization precedent),
  `XASSET-0009` (in full, as the direct two-subject economic-assessment content-authorization precedent),
  and `XASSET-0010` (decision file and supporting artifact, in full) read directly this session**, not
  summarized from memory.
- **`OPS-0007` (capability-based review standard, §1) and `OPS-0009` (Lean Delivery lifecycle, Lane G) read
  directly this session** — this filing is classified Lane G (governance authorization) throughout,
  matching every prior `XASSET-####` content authorization.
- **`intelligence/etf_classification/{SPY,VEA,VWO}.yaml` and `intelligence/crypto_classification/
  {BTC,ETH,SOL}.yaml` independently re-read directly**: all six confirmed `record_status: sealed`,
  `valuation_and_economic_assessment_readiness.status: valuation_required`, unedited since `XASSET-0010`'s
  own Preflight recorded them.
- **`intelligence/economic_assessment/{GLD,CASH_LIKE_CAPITAL}.yaml` and `economic_assessment_validator.py`
  independently confirmed unaffected** — byte-unedited, unreferenced by anything this filing does.
- **`intelligence/instrument_economic_assessment/` confirmed absent** — no directory, no file, anywhere in
  the repository, at this session's own starting head.
- **`intelligence/overlap_model/{defensive_offset_interface,crypto_correlation_interface}.yaml`
  independently confirmed**: both still `computation_status: not_yet_computable_interface_only`,
  unconditional, unaffected by `PR #295`'s own merge.
- **`intelligence/contenders/registry.yaml` independently re-checked**: `QQQ`'s own entry confirms
  `primary_disposition: benchmark_or_index` — unaddressed by this filing, exactly as `XASSET-0010` §B
  excludes it.
- **Full repository `pytest`** (`test_portfolio_hq_dashboard_decisions.py`, the decision-catalog-count-
  sensitive suite) independently re-run this session at the starting head, matching the expected
  post-`PR #295` baseline.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing does two things, in one bounded PR:

1. **Performs the ordinary `WS-0014` self-reference synchronization** (`active_branch`,
   `last_verified_main_sha`, `last_verified_date`) plus one additive Lane M fold-forward gate recording
   `PR #295`'s own confirmed merge state — without editing the
   `xasset0010-etf-crypto-economic-assessment-methodology-design` gate's own historical text.
2. **Authorizes exactly one future, separate, bounded ETF+crypto instrument economic-assessment (content)
   implementation pull request**, covering all six instruments — `SPY`, `VEA`, `VWO`, `BTC`, `ETH`, `SOL` —
   in one implementation, under the exact schema, evidence, sequencing, abstention, structural-reference,
   and validator/test controls already specified and accepted through `XASSET-0010`. It performs no
   population itself, creates no `instrument_economic_assessment` record or validator, and implements no
   `intelligence/instrument_economic_assessment/` content.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007` §1), any
required bounded correction and re-review, explicit principal acceptance, merge, and post-merge
verification — the same lifecycle every prior filing in this chain has followed — may proceed to:

1. Draft and seal one `instrument_economic_assessment` record for each of the six fixed instruments named in
   `XASSET-0010` §B — `SPY`, `VEA`, `VWO`, `BTC`, `ETH`, `SOL` — zero exclusions, zero additions. No `GLD`,
   `CASH_LIKE_CAPITAL`, `DEBT_REDUCTION`, `QQQ`, or any seventh instrument may be introduced without its own
   separate, future, explicit authorization (`XASSET-0010` supporting artifact §9 point 1's own closed-
   population rule).
2. Gather the evidence each of the six instruments' own substantive axis needs — `SPY`'s, `VEA`'s, and
   `VWO`'s own sourced cost/tracking-quality comparisons within their respective fund categories (feeding
   `cost_and_tracking_quality_economic_significance`); `BTC`'s, `ETH`'s, and `SOL`'s own sourced historical
   equity-market-drawdown behavior and historical inflation-sensitivity narrative (feeding
   `macro_behavioral_characterization`'s two sub-fields) — per the six named, unanswered research questions
   `XASSET-0010` §I / supporting artifact §7 identifies without answering. Where evidence is insufficient
   for any axis or sub-field on any instrument, the implementation must use the framework's own abstention
   path (`unable_to_determine` with a required `abstention_reason`) rather than fill the gap — an
   abstaining record is an honest, complete, sealed outcome, not a defect requiring correction.
3. Create the appropriate `COHORT_MANIFEST.yaml` for the six sealed records under a new, separate directory,
   `intelligence/instrument_economic_assessment/` (`XASSET-0010` §J), matching every prior classification/
   economic-assessment framework's own manifest convention.
4. Build `instrument_economic_assessment_validator.py` — the one dedicated validator module `XASSET-0010`
   §J / supporting artifact §9 already names — and its dedicated test file, per the full sixteen-point
   validator specification and full test-item list (supporting artifact §9/§9.1/§10).
5. Use a single implementation pass covering all six instruments across both asset types (no per-instrument
   PR structure; no multi-shard isolation apparatus of any kind beyond ordinary internal drafting
   organization) — the population is fixed, small, and shares one envelope and one validator module,
   matching `XASSET-0006`'s and `XASSET-0009`'s own identical determination for their own comparably-sized
   shared-schema populations.
6. Stop after any subset of the six records, without a separate pilot authorization, if a systemic schema,
   evidence, or contamination defect is discovered — an internal stop-and-fix condition within the one
   authorized implementation PR, not a license to split into a second governance filing or a per-instrument
   PR structure.

**No cross-coin correlation study, coefficient, or claim of any kind is authorized by this filing** — the
future implementation must never assert, in any field or free-text rationale, that `BTC`/`ETH`/`SOL` are or
are not correlated with each other, and must never populate a numeric correlation coefficient (`XASSET-0010`
§F, supporting artifact §6.1/§9 point 11's own binding rule). **No `GLD`, `CASH_LIKE_CAPITAL`, or
`DEBT_REDUCTION` economic-assessment content of any kind is authorized by this filing** — all three remain
separately governed and untouched: `GLD`/`CASH_LIKE_CAPITAL` already sealed under `XASSET-0008`/`XASSET-0009`
(`PR #294`, unaffected here); `DEBT_REDUCTION`'s own gap belongs to the separately governed margin/leverage-
policy track (`XASSET-0010` §B). **No overlap-model content, no equity-`VALUATION-####` extension, and no
`QQQ` or any other future ETF/crypto candidate** is authorized by this filing.

### B. Binding specification — by reference, not restatement

The implementation PR must follow `XASSET-0010`'s specification exactly, as accepted and merged at
`bd04cda9eaa12c4a7da269a27b963eb222010f33` (`PR #295`). This filing does not redesign, loosen, tighten, or
restate that specification in its own words beyond the index below — the implementation session has no
discretion to depart from it:

| Control | Governing section (`XASSET-0010 §N` citations refer to the decision file; `AA §N` citations refer to the supporting artifact, `governance/audits/WS0014_ETF_CRYPTO_INSTRUMENT_ECONOMIC_ASSESSMENT_METHODOLOGY_DESIGN_20260810.md`) |
|---|---|
| Exactly six `instrument_id` values across two `asset_type` values (`etf`: `SPY`/`VEA`/`VWO`; `cryptocurrency`: `BTC`/`ETH`/`SOL`); no `GLD`, `CASH_LIKE_CAPITAL`, `DEBT_REDUCTION`, or `QQQ` | `XASSET-0010` §B; `AA` §9 point 1 |
| Shared envelope (`schema_version`, `instrument_id`, `asset_type`, `structural_reference`, the one asset-type-conditional substantive axis, `evidence_quality`, `provenance`, `uncertainty_summary`, `evidence_quality_status`, `record_status`, `cross_asset_handoff`, `abstention_index`, seal metadata) — closed set, no unknown key permitted at the top level | `XASSET-0010` §D.1; `AA` §4.1 |
| One ETF-shared axis, `cost_and_tracking_quality_economic_significance` (closed vocabulary `in_line_with_category` \| `elevated_vs_category` \| `favorable_vs_category` \| `unable_to_determine`, required `rationale`, required `abstention_reason` on abstention, no `not_applicable` path, no bare numeric-percent token anywhere in free text) — required on `etf`, forbidden on `cryptocurrency` | `XASSET-0010` §E; `AA` §5.2 |
| One crypto-shared compound axis, `macro_behavioral_characterization`, two independently-abstainable sub-fields — `historical_equity_market_drawdown_behavior` (closed vocabulary `historically_uncorrelated_or_negatively_correlated` \| `historically_mixed` \| `historically_positively_correlated` \| `unable_to_determine`, mandatory non-empty `single_asset_disclosure`) and `historical_inflation_sensitivity_narrative` (closed vocabulary `historically_positively_associated` \| `historically_mixed_or_inconsistent` \| `historically_weakly_associated` \| `unable_to_determine`) — required on `cryptocurrency`, forbidden on `etf` | `XASSET-0010` §F; `AA` §6.2 |
| Structural reference — one pin per instrument, never a duplicate mechanism: `SPY`/`VEA`/`VWO` pin to their own `intelligence/etf_classification/<TICKER>.yaml` via `etf_classification_validator.canonical_record_hash()` (`etf_classification_validator.py:322`); `BTC`/`ETH`/`SOL` pin to their own `intelligence/crypto_classification/<TICKER>.yaml` via `crypto_classification_validator.canonical_record_hash()` (`crypto_classification_validator.py:347`) — both live-recomputed on every validator run, rejecting a stale or wrong-schema reference | `XASSET-0010` §D.2; `AA` §3 |
| Zero numeric field anywhere, no carve-out of any kind (stricter than the ETF classification framework's own scoped `expense_ratio_pct` exception) — an already-sealed numeric structural fact may be referenced only by structural hash/source pin, never restated as a literal number anywhere in this schema's own free text | `XASSET-0010` §D.3; `AA` §5.2, §9 point 6 |
| Evidence/contamination boundary — no live `holdings.yaml` value, no `targets.yaml` `target_pct`, no live `margin_state.py` output, no current dollar balance as evidence for any judgment axis; existing mechanisms may be cited structurally where genuinely relevant, creating no investment-policy authority under this schema | `XASSET-0010` §D.4 |
| `evidence_quality` (unchanged shape from every prior framework) — `comprehensive`/`partial`/`limited`, required `thesis_uncertainty_statement` | `XASSET-0010` §D.5; `AA` §4.4 |
| Synthesis handoff — `cross_asset_handoff` carries exactly three fields (`economic_characterization_summary`, `evidence_quality_summary`, `uncertainty_summary` — no `deployability_summary` field for this population); may never carry a target weight, rank, IN/OUT signal, buy/sell/hold/trim/exit/wait/stage signal, sleeve percentage, trade-timing recommendation, leverage amount, or numeric coefficient of any kind | `XASSET-0010` §D.6; `AA` §4.6 |
| GLD/overlap-model/crypto-correlation non-duplication — every `BTC`/`ETH`/`SOL` `historical_equity_market_drawdown_behavior` sub-field must carry a mandatory, non-empty `single_asset_disclosure` stating the finding is single-asset and historical only, never a computed whole-portfolio diversification-benefit or cross-asset-correlation finding; that remains `XASSET-0007`'s own sealed `defensive_offset_interface`/`crypto_correlation_interface` dimensions' job, both still forced `not_yet_computable_interface_only`, unaffected here | `XASSET-0010` §H; `AA` §7 (non-duplication boundary) |
| Cross-coin-correlation boundary — a genuine `BTC`/`ETH`/`SOL` correlation study, if ever performed, requires its own separate, bounded, pre-registered research charter matching `MARGIN-0005`'s/`LADDER-0001`'s own precedent; not authorized, designed, or implied by this filing or the implementation it authorizes | `XASSET-0010` §F; `AA` §6.1 |
| Future research interface — six named, unanswered questions (`SPY`'s, `VEA`'s, `VWO`'s own cost/tracking-quality significance; `BTC`'s, `ETH`'s, `SOL`'s own historical drawdown behavior and historical inflation-sensitivity narrative) — this filing conducts no research toward any of them and does not authorize the future implementation to treat any as already answered | `XASSET-0010` §I; `AA` §7 |
| `GLD`/`CASH_LIKE_CAPITAL` boundary — permanently separate schema/directory/validator, not reopened, not migrated, not extended by this filing or the implementation it authorizes | `XASSET-0010` §G |
| Portfolio-selection boundary — evidence → cross-asset opportunity-cost synthesis (`XASSET-0001` §E/§F, wholly undesigned) → an explicit human-approved adoption decision → only then, governed IN/OUT membership; completing all six records, however completely, does not select the portfolio | `AA` §8 |
| Validator specification (16 points, `AA` §9: exact 6-instrument/2-asset-type population enforcement; closed schema at every level rejecting extra keys, not just missing ones; `asset_type`-conditional shape enforcement; `structural_reference` live-hash enforcement selecting the correct `canonical_record_hash()` function by `asset_type`; no cross-schema field-name leakage — equity/ETF-classification/crypto-classification/functional-doctrine/overlap-model/`economic_assessment` key names forbidden; zero numeric field with no carve-out; no chart-evidence leakage; no directive/trading-language leakage — the shared eight words, word-boundary matched; no predictive-language leakage, scoped to the two crypto historical sub-fields; crypto/overlap-model non-duplication check; cross-coin-correlation non-leakage — a materially independent mechanism from the numeric-pattern scan; evidence/provenance validation; allocator/margin import decoupling; abstention independently checked; `abstention_index` independently reconciled, never a self-declared flag trusted alone; deterministic generation and protected-path isolation) plus §9.1's five explicitly carried-forward lessons | `AA` §9, §9.1 |
| Test specification (`AA` §10's full item list: happy-path per instrument across both asset types; malformed/extra/missing keys at every level; wrong `instrument_id`/`asset_type` mismatch rejection in both directions; `cost_and_tracking_quality_economic_significance`/`macro_behavioral_characterization` asset-type-conditional presence/absence rejection in both directions; `structural_reference` hash independently verified via a live recompute, including a synthetic stale-hash test for each `source_schema` value and a live test against each real sealed classification record; cross-schema field-name leakage per source schema; numeric-field leakage per named term with no positive-acceptance test; chart-terminology leakage per term; directive/trading-language leakage per word including a false-positive guard; predictive-language leakage per term, scoped correctly; crypto/overlap-model non-duplication; cross-coin-correlation leakage per named pattern individually, plus a positive test confirming single-asset-only discussion is accepted; abstention behavior including non-cascading; `abstention_index` reconciliation in both directions; deterministic output; protected-path isolation including `GLD.yaml`/`CASH_LIKE_CAPITAL.yaml` themselves, unreferenced, never modified; allocator/margin import-coupling isolation) | `AA` §10 |

Nothing in this table is amended, expanded, or narrowed by this filing. Any future session finding a genuine
ambiguity or gap in `XASSET-0010`'s specification must return for its own separate governance correction —
not resolve it unilaterally inside the implementation PR.

### C. Evidence standard and stop conditions (binding on the future implementation)

The implementing session must use only the evidence `XASSET-0010` §I / supporting artifact §7 identify —
sourced, dated, citable comparisons and historical/academic/industry-analysis material for the six named
research questions — and must never use a live `holdings.yaml`/`targets.yaml`/`margin_state.py` value as
evidence for any judgment axis (§B above). Where evidence is insufficient, `unable_to_determine` with a
specific `abstention_reason` is the required, complete outcome for that axis or sub-field; **this filing does
not authorize any research beyond what is needed to answer the six named questions, and does not pre-decide
whether every instrument reaches a determined (non-abstained) result.**

The implementation PR must stop immediately and disclose, never silently work around: population drift (a
seventh instrument appearing to be needed, or any of the six ceasing to apply); any equity-, ETF-
classification-, crypto-classification-, functional-doctrine-, overlap-model-, or `economic_assessment`
(`GLD`/`CASH_LIKE_CAPITAL`)-shaped field leakage; any numeric score/rank/target/expected-return/hurdle-rate/
correlation-coefficient leakage of any kind; any chart-domain leakage; any predictive/forecast-language
leakage inside either crypto sub-field; any attempt to compute, duplicate, or preempt
`defensive_offset_interface`'s or `crypto_correlation_interface`'s own portfolio-level findings; any attempt
to assert or imply a cross-coin correlation claim or coefficient; any duplication or re-derivation of a
sealed field from any referenced classification record rather than citing it by hash; any protected-path
mutation; or any unexpected target, holdings, gate, cap, cluster, allocator, margin, ladder, order, or trade
change.

### D. Independent review requirement (binding on the future implementation)

The implementation PR's independent exact-head review must verify, at minimum: the exact six-instrument/
two-asset-type population; the exact changed-file inventory; schema conformance for all six records,
including the correct `asset_type`-conditional shape of the one substantive axis and the structural-reference
mechanism selecting the correct `canonical_record_hash()` function; abstention validity and non-cascading
behavior; every `structural_reference`'s live hash recompute and absence of every cross-schema key name
inside any record; the mandatory `single_asset_disclosure` on every populated
`historical_equity_market_drawdown_behavior` sub-field; the dedicated, materially independent cross-coin-
correlation non-leakage scan and at least one positive single-asset-only-discussion test; the validator and
its tests against `XASSET-0010` supporting artifact §9/§10's full specification, including §9.1's five
explicitly carried-forward lessons; CI; protected-path isolation; absence of any `GLD`/`CASH_LIKE_CAPITAL`/
`DEBT_REDUCTION`/`QQQ`/overlap-model content of any kind; absence of any cross-asset synthesis, sleeve
target, or instrument target; and absence of any policy mutation. Any correction requires its own fresh
exact-head delta review before principal acceptance.

### E. Boundaries restated, unweakened

**`GLD`/`CASH_LIKE_CAPITAL`**: permanently separate, sealed schema (`XASSET-0008`/`XASSET-0009`, `PR #294`)
— not reopened, not migrated, not extended by this filing or the implementation it authorizes.

**`DEBT_REDUCTION`**: remains entirely outside this filing's scope, exactly as `XASSET-0010` §B excludes it —
its own economic-assessment gap belongs to the separately governed margin/leverage-policy track (the 1.8x
leverage cap, the 30% buffer floor, `MARGIN-0005`'s own bounded research charter), untouched by this filing
or the implementation it authorizes.

**Overlap model**: `XASSET-0007`'s own content step is already separately authorized and fully implemented
(`PR #292`) — unaffected, untouched, and not reopened by this filing. `defensive_offset_interface`'s and
`crypto_correlation_interface`'s own forced `not_yet_computable_interface_only` values are independently
reconfirmed this session and are not loosened by this filing or the implementation it authorizes.

**Cross-coin correlation**: remains a separate, future, bounded, pre-registered research charter's own
question — not authorized, designed, or implied by this filing.

**`QQQ`**: not a canonical destination, not classified, carries `primary_disposition: benchmark_or_index` —
unaddressed by this filing and by the implementation it authorizes.

### F. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **`active_branch` set to this filing's own branch, `last_verified_main_sha` updated**
   `3a7c89e6f4137c7ee37c643af1dc3f6a58d4912c` → `5b2e3be1419cc54ed7c5903960e38d5b44dbc2ec`, and
   **`last_verified_date` updated** to this filing's own date.
2. **One new additive gate, `xasset0010-post-merge-verification`**, recording — without editing the
   `xasset0010-etf-crypto-economic-assessment-methodology-design` gate's own historical text — that
   `PR #295` is fully merged (Preflight above gives the confirmed chain).
3. **One additive gate, `xasset0011-etf-crypto-economic-assessment-content-authorization`**, recording this
   filing's own branch and PR number — `status: in_progress`, **not** `status: complete`, since this
   filing's own governance PR is itself unmerged, unreviewed, and unaccepted, matching every prior filing's
   identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: `XASSET-0010`'s own methodology design is
   merged and effective; this filing, once merged, authorizes exactly one future ETF+crypto instrument
   economic-assessment content implementation PR covering `SPY`/`VEA`/`VWO`/`BTC`/`ETH`/`SOL`;
   `DEBT_REDUCTION` economic assessment, the `CASH`/`RESERVE` consolidation question, `QQQ`/any future
   candidate expansion, a future cross-coin correlation study, and every other remaining `WS-0014` item
   remain wholly unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`,
`completion_criteria`, `roadmap_preservation`) is changed. `WS-0005` and `WS-0015` are not touched by this
filing.

### G. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder
change; any trade or order; any chart use of any kind; any buy/sell/hold/trim/exit/wait/stage recommendation
or directive of any kind; population of any `instrument_economic_assessment` record by this filing itself;
creation of `intelligence/instrument_economic_assessment/` or any file inside it; any validator or test
implementation; any economic finding, categorical or otherwise, for `SPY`, `VEA`, `VWO`, `BTC`, `ETH`, or
`SOL`; any cross-coin correlation study, coefficient, or claim of any kind; any edit to `GLD.yaml`,
`CASH_LIKE_CAPITAL.yaml`, `economic_assessment_validator.py`, or any sealed ETF/crypto classification record;
any resolution of any sealed classification record's forced `valuation_and_economic_assessment_readiness.
status`; any `DEBT_REDUCTION` economic-assessment methodology or content; any overlap-model dimension
computation or edit of any kind; any cross-asset opportunity-cost synthesis; any Level 1 sleeve or Level 2
instrument sizing; any `QQQ` or other future ETF/crypto candidate expansion; and any edit to `XASSET-0001`
through `XASSET-0010`'s own text.

### H. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index row);
(3) `operations/WORKSTREAMS.yaml` (`WS-0014` only — the §F updates); (4) `CLAUDE.md` (one concise Decisions
Log pointer entry); (5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-count
assertions, 106→107, made stale by this filing's own new row). No supporting audit artifact is created —
`XASSET-0010` and its supporting artifact already contain the complete accepted process specification for the
ETF/crypto instrument economic-assessment schema, and restating it in a second retained document would
duplicate content rather than add evidence, matching `XASSET-0003`'s, `XASSET-0004`'s, `XASSET-0006`'s, and
`XASSET-0009`'s own identical determination. No `intelligence/` company, theme, relationship, classification,
reconciliation, recommendation, contender, ETF-classification, crypto-classification, functional-doctrine,
overlap-model, economic-assessment, valuation-archetype, valuation-evidence, or valuation-results file; no
`targets.yaml`/`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`; and no production allocator/margin
code is touched.

### I. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its exact
head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. This session does not review its own
work, mark it ready, merge it, or post principal acceptance. Nothing in this decision becomes effective until
this governance PR merges to `main` — including the authorization in §A, which the future implementation
session may not rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `XASSET-0010` already carries a complete specification
for every schema, evidence, sequencing, and validator control the ETF/crypto instrument economic-assessment
methodology needs. Re-deriving or rephrasing that content here would introduce exactly the kind of drift
risk this repository's own review history has repeatedly demonstrated is not hypothetical — the smaller and
more reliable move is to bind the future implementation to `XASSET-0010`'s own text by reference, unchanged.

**Why this filing authorizes all six instruments in one PR, not split by asset type.** `XASSET-0010` designed
one shared envelope and one shared structural-reference mechanism, and explicitly names one dedicated
validator module covering both sub-populations under one `asset_type`-conditional schema — not two
independently-shaped classification frameworks that happen to share a filing. This is the identical shape
`XASSET-0006` (four functional-doctrine types) and `XASSET-0009` (two economic-assessment subjects) already
used for one combined authorization and one combined implementation PR, not the `XASSET-0002`→
`XASSET-0003`+`XASSET-0004` shape, which split two genuinely separate, fully independent classification-layer
frameworks each with their own complete field set. Splitting this filing would fragment one already-unified
envelope/validator specification for no review benefit — the controlling principal's own explicit directive
matches the repository's own established pattern for this shape of population.

**Why the two evidence-sufficiency boundaries (cross-coin correlation, the six unanswered research questions)
are restated rather than resolved by this filing.** Resolving either here would exceed this filing's own
authorization-only scope — `XASSET-0010` §F/§I and supporting artifact §6.1/§7 already reserve those
determinations to a future, separate research charter (correlation) or to the drafting session under
independent review (the six questions), not to a governance-authorization filing that performs no drafting or
research of its own.

## Alternatives Considered

- **Split into two separate authorization filings, one for the ETF sub-population and one for the crypto
  sub-population.** Rejected — see Rationale; `XASSET-0010` designed one shared envelope and one validator
  module, not two independent frameworks; splitting would fragment it for no review benefit, unlike the
  genuine `XASSET-0002`→`XASSET-0003`+`XASSET-0004` split, which separated two structurally distinct
  classification frameworks.
- **Combine this authorization with content in one PR**, matching several smaller Company Intelligence
  batches' combined-filing precedent (`REL-0002`, `PI-0036`, `PI-0038`). Rejected — `XASSET-0010`'s own
  stage-separation rule (§A) and `XASSET-0001` §J's separation rule both require content to follow its own
  separate authorization and implementation lifecycle, matching `XASSET-0003`'s, `XASSET-0004`'s, and
  `XASSET-0009`'s own identical treatment, not the smaller-batch pattern used for an already-proven equity
  framework.
- **Attempt a cross-coin correlation study, or answer one of the six named research questions, in this
  filing.** Rejected — this filing performs no drafting and has no evidence-gathering authority of its own;
  forcing either here would itself be the "force a value merely to fill the record" failure mode
  `XASSET-0010`'s own design exists to prevent, and a correlation study specifically requires its own
  separate, bounded, pre-registered charter this filing does not attempt to substitute for.
- **Create a retained audit artifact restating `XASSET-0010`'s process specification.** Rejected —
  `XASSET-0010` and its supporting artifact are themselves the retained, accepted specification; a second
  document repeating it would be redundant, not additive, matching `XASSET-0003`'s, `XASSET-0004`'s,
  `XASSET-0006`'s, and `XASSET-0009`'s own identical determination.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded ETF+crypto instrument
economic-assessment content implementation PR covering all six instruments (`SPY`, `VEA`, `VWO`, `BTC`,
`ETH`, `SOL`), bound exactly to `XASSET-0010`'s specification per §A–E above, gated on its own full
independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle; one
additive Lane M fold-forward gate (`PR #295`'s own confirmed post-merge state); the
`xasset0011-etf-crypto-economic-assessment-content-authorization` gate transitioning to `status: in_progress`
recording this filing as underway; `WS-0014`'s ordinary self-reference synchronization.

**Not authorized by this filing, now or ever without a further separate decision:** population of any
`instrument_economic_assessment` record; any economic finding, categorical or otherwise, for `SPY`, `VEA`,
`VWO`, `BTC`, `ETH`, or `SOL`; any cross-coin correlation study, coefficient, or claim of any kind; any edit
to `GLD.yaml`, `CASH_LIKE_CAPITAL.yaml`, `economic_assessment_validator.py`, or any sealed ETF/crypto
classification record; any resolution of any sealed classification record's forced `valuation_and_economic_
assessment_readiness.status`; any `DEBT_REDUCTION` economic-assessment methodology or content; any
overlap-model dimension computation or edit of any kind; any cross-asset opportunity-cost synthesis; any
Level 1 sleeve or Level 2 instrument sizing; any `QQQ` or other future ETF/crypto candidate expansion; any
validator or test implementation; any edit to `XASSET-0001` through `XASSET-0010`'s own text; and any
tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification/functional-doctrine/overlap-model/
economic-assessment/valuation-archetype/valuation-evidence/valuation-results record, byte-for-byte, including
all six sealed ETF/crypto classification records this filing structurally references (referenced, never
modified) and both sealed `GLD`/`CASH_LIKE_CAPITAL` economic-assessment records; all ten sealed overlap-model
dimension records, including `defensive_offset_interface`'s and `crypto_correlation_interface`'s own forced
`not_yet_computable_interface_only` values; `XASSET-0001` through `XASSET-0010`'s own accepted text and
scope, in full, unedited; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `levels.py`, `margin_state.py`; the 1.8x leverage cap and 30% margin-buffer floor; `WS-0005`'s
completed, `status: complete` state; `WS-0015`'s own live state; `WS-0014`'s own `status: proposed`/
`priority: secondary`.

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ is
not a 27-stock system, and this filing's own bounded six-instrument content authorization does not narrow
that fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical equities;
contender-registry regeneration and legacy-history recovery; `QQQ` and any other future ETF or crypto
candidate expansion; equity Stage-4 valuation execution beyond the sealed 27-company cohort; `DEBT_REDUCTION`
economic assessment; whether `CASH`/`RESERVE` should ultimately be consolidated (`XASSET-0008` §N); the
future `SPY`/`VEA`/`VWO`/`BTC`/`ETH`/`SOL` economic-assessment content implementation this filing's own
authorization would draw on; a future cross-coin correlation study; cross-asset opportunity-cost synthesis;
Level 1 sleeve allocation; Level 2 instrument allocation; `CHART-0003` and any remaining governed chart
ingestion; ladder/deployment integration; unlevered testing; margin/leverage-policy review; monitoring/sell
discipline; final integration and audit; and any true whole-universe allocation test.
