---
decision_id: XASSET-0010
date: 2026-08-10
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, VALUATION-0001, VALUATION-0002, VALUATION-0004, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002]
supporting_artifact: governance/audits/WS0014_ETF_CRYPTO_INSTRUMENT_ECONOMIC_ASSESSMENT_METHODOLOGY_DESIGN_20260810.md
file: governance/decisions/XASSET-0010-etf-crypto-economic-assessment-methodology.md
---

## Context

### Authority for this unit

`XASSET-0005` §5 named "perform asset-appropriate valuation/economic assessment" as step 2 of a
seven-step whole-portfolio sequence, restated by `XASSET-0008` §A as five stages of which only stage 1
(methodology design) is authorized per unit. `XASSET-0008`/`XASSET-0009` closed stage 1 and stage 2/3
for exactly two analytical subjects, `GLD` and `CASH_LIKE_CAPITAL` — and `XASSET-0008`'s own restated
whole-universe boundary (its closing paragraph, unedited) names, among the items still unfinished and
unauthorized by any prior filing: **"ETF and crypto economic/valuation methodology."** Every sealed
ETF and crypto classification record (`intelligence/etf_classification/{SPY,VEA,VWO,GLD}.yaml`,
`intelligence/crypto_classification/{BTC,ETH,SOL}.yaml`) independently carries the identical forced
value `valuation_and_economic_assessment_readiness.status: valuation_required` — confirmed live this
session (below) — stating plainly that no governed methodology exists to compare any of these seven
instruments' opportunity cost against anything else. `GLD`'s own gap is already closed
(`XASSET-0008`/`XASSET-0009`); the remaining six — `SPY`, `VEA`, `VWO`, `BTC`, `ETH`, `SOL` — are the
subject of this filing, per the controlling principal's explicit authorization. This filing designs
methodology only; it does not populate any record and does not resolve any sealed classification
record's forced status.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/etf-crypto-assessment-methodology-7ybkis`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `3a7c89e6f4137c7ee37c643af1dc3f6a58d4912c` — the merge commit of `PR #294` (`XASSET-0009`'s own
  economic-assessment content implementation, GLD/CASH_LIKE_CAPITAL).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **Decision catalog independently rebuilt**: **105 decisions, `issues == ()`** at the starting head.
  `XASSET-0010` confirmed the next unused identifier in the `XASSET-####` series (0001 through 0009 all
  present; `governance/decisions/README.md`'s own rule — a new prefix only for a genuinely new decision
  domain — is satisfied by continuing the existing series, not minting a new one, matching every prior
  `XASSET-####` filing's identical reasoning).
- **Full repository `pytest`**: **95 passed** (`test_portfolio_hq_dashboard_decisions.py`, the
  decision-catalog-count-sensitive suite) independently re-run this session at the starting head.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`. Its `blocker`/`next_action`
  fields confirm `PR #293` (`XASSET-0009`'s authorization) and `PR #294` (its own content
  implementation) both independently confirmed merged by the immediately preceding session, with the
  `xasset0009-economic-assessment-content-implementation` gate itself still `status: in_progress`,
  `pr: 294` — that gate's own review/merge lifecycle is a separate, already-in-flight matter this
  filing does not touch or duplicate; this filing performs the ordinary Lane M fold-forward for that
  confirmed-merged state (§K below) without editing the gate's own historical text.
- **`XASSET-0001` (§C, §D, §E, §F, §J, in full), `XASSET-0002` (in full, as the direct ETF+crypto
  batching precedent), `XASSET-0005` (§3.5, §3.6, §5, §6, §9), and `XASSET-0008`/`XASSET-0009` (in
  full, as the direct GLD/CASH_LIKE_CAPITAL economic-assessment precedent) read directly this session**,
  not summarized from memory.
- **`intelligence/etf_classification/{SPY,VEA,VWO}.yaml` and `intelligence/crypto_classification/
  {BTC,ETH,SOL}.yaml` independently read directly, in full** — all six confirmed `record_status: sealed`,
  `valuation_and_economic_assessment_readiness.status: valuation_required`. `liquidity.liquidity_tier`
  (ETFs) and `liquidity_and_market_structure.liquidity_tier` (crypto) confirmed `high_liquidity` on all
  six — load-bearing for the rejected-question dispositions in §E/§F below. `cost_and_tracking_quality.
  expense_ratio_pct` confirmed present on all three ETF records (SPY 0.0945, VEA 0.03, VWO 0.06),
  `tracking_quality_category: not_yet_measured` on all three. `correlation_and_volatility.
  cross_coin_correlation_status: not_yet_measured` confirmed present on all three crypto records.
- **`etf_classification_validator.canonical_record_hash()` (`etf_classification_validator.py:322`) and
  `crypto_classification_validator.canonical_record_hash()` (`crypto_classification_validator.py:347`)
  independently confirmed present** — both already relied upon by `GLD.yaml`'s own sealed
  `economic_assessment` record's structural reference (`XASSET-0008`/`XASSET-0009`), load-bearing for
  this filing's own structural-reference mechanism (§D below).
- **`intelligence/economic_assessment/{GLD,CASH_LIKE_CAPITAL}.yaml` and `economic_assessment_
  validator.py` independently read directly** — confirmed sealed, byte-unedited, and confirmed the
  existing module's own docstring scopes it explicitly to "the first (and only, per `XASSET-0009`'s own
  bounded authorization) `WS-0014` economic-assessment content batch" — this filing does not extend,
  reuse, or amend that module or that population; both remain untouched (§G below).
- **`intelligence/contenders/registry.yaml` independently re-checked**: `QQQ`'s own entry confirms
  `primary_disposition: benchmark_or_index` — not a canonical destination, not a held instrument, not a
  classified fund. `QQQ` is not addressed by this filing.

## Decision

This filing designs, as text only — not an authorization, not an adoption, not applied to any real
holding — **a closed economic-assessment methodology for exactly six already-classified instruments**:
three ETFs (`SPY`, `VEA`, `VWO`) and three cryptocurrencies (`BTC`, `ETH`, `SOL`). `GLD` and
`CASH_LIKE_CAPITAL` are explicitly excluded — already governed under a separate, sealed methodology
(`XASSET-0008`/`XASSET-0009`), untouched, not reopened (§G). It performs no population, computes no
economic finding for any of the six instruments, and resolves no sealed classification record's forced
`valuation_and_economic_assessment_readiness.status` value. Full field-by-field detail, closed
vocabularies, abstention discipline, structural-reference mechanics, and the validator/test
specification are in the supporting artifact.

### A. Stage separation — five stages, this filing is stage 1 only (reused unchanged from `XASSET-0008` §A)

1. **Methodology/schema design** — this filing. Designs the closed question set, evidence rules,
   abstention discipline, and structural-reference mechanics. Performs no content.
2. **Future, separate content authorization** — not performed here; requires its own future, explicit
   principal authorization, mirroring `XASSET-0003`'s/`XASSET-0004`'s/`XASSET-0009`'s own role for the
   ETF, crypto, and GLD/CASH_LIKE_CAPITAL content steps.
3. **Future, separate content implementation** — not performed here; the actual drafting and sealing of
   up to six `instrument_economic_assessment` records, gated on stage 2's own authorization and its own
   full independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification
   lifecycle.
4. **Later cross-asset synthesis** — `XASSET-0001` §E/§F, wholly undesigned, wholly unauthorized by this
   filing or by any future stage-3 content this filing's methodology would produce.
5. **Later explicit policy adoption** — a still-separate, human-approved governance decision, required
   before any evidence this methodology eventually produces may affect any tier, target, holdings, gate,
   cap, cluster, allocator, or margin behavior.

**This filing authorizes stage 1 only.** It does not authorize, begin, schedule, or imply stages 2–5.

### B. Population — exactly six instruments, `GLD`/`CASH_LIKE_CAPITAL`/`DEBT_REDUCTION`/`QQQ` excluded

**ETF sub-population**: `SPY`, `VEA`, `VWO` — the three currently-classified, non-`GLD` fund
destinations in `targets.yaml`'s `destination:` list.

**Crypto sub-population**: `BTC`, `ETH`, `SOL` — all three currently-classified crypto destinations.

**Excluded, explicitly**:

- **`GLD`** — already governed by its own sealed, closed economic-assessment methodology
  (`XASSET-0008`/`XASSET-0009`), populated and merged. Not reopened, not re-derived, not migrated into
  this filing's schema (§G).
- **`CASH_LIKE_CAPITAL`** and **`DEBT_REDUCTION`** — non-instrument capital-use concepts, out of this
  filing's scope entirely; `CASH_LIKE_CAPITAL` already governed under `XASSET-0008`/`XASSET-0009`,
  `DEBT_REDUCTION`'s own gap remains assigned to the separately governed margin/leverage-policy track
  (unchanged, unreopened).
- **`QQQ`** — not a canonical destination, not classified, carries `primary_disposition:
  benchmark_or_index` in the contender registry (Preflight, above). No future ETF/crypto candidate
  beyond these six named instruments is addressed by this filing.
- **Equities** — the existing `VALUATION-####` series' own methodology/archetype/evidence/execution
  chain remains the sole governed equity-valuation track; this filing extends no equity methodology and
  is not itself extended by any future equity-valuation filing.

### C. Batching — one filing, two asset classes, no new prefix (reusing `XASSET-0002`'s own precedent)

Both sub-populations are designed in one filing for the identical reason `XASSET-0002` batched ETF and
crypto **classification** framework design: they share one method (a shared envelope, a shared
structural-reference mechanism, a shared zero-numeric/evidence-contamination/abstention/synthesis-
handoff discipline) even though their substantive content differs entirely by asset type. Separating
them into two filings would duplicate the shared-envelope and validator/test specification for no review
benefit — the same reasoning `XASSET-0002`'s ETF+crypto classification batching and `XASSET-0008`'s
`GLD`+`CASH_LIKE_CAPITAL` batching both already applied. This filing continues the existing `XASSET-####`
series (Preflight, above) rather than minting a new prefix.

**What this batching does not do**: it does not combine framework **design** with **content** for
either asset type (stage 1 only, §A); it does not combine ETF **content** with crypto **content** in one
future implementation filing unless a later, separate authorization explicitly elects to (mirroring
`XASSET-0003`/`XASSET-0004`'s own precedent of separate content-authorization filings following one
combined design filing — left as an open, future choice, not mandated here, §D.7 below).

### D. Shared methodology — common across both sub-populations

1. **Envelope** (supporting artifact §4): `schema_version`, `instrument_id`, `asset_type` (`etf` |
   `cryptocurrency` — matching the classification layer's own field names exactly, deliberately not
   reusing `XASSET-0008`'s own `analytical_subject` term, since every member of this filing's population
   already has a real classification-layer identity to key from), `structural_reference` (§D.2),
   [the one asset-type-conditional substantive axis, §E/§F], `evidence_quality` (§D.5), `provenance`,
   `uncertainty_summary`, `evidence_quality_status`, `record_status`, `cross_asset_handoff` (§D.6),
   `abstention_index`, plus the standard seal-metadata keys (`sealed_at`, `governing_decision`,
   `drafting_session_or_shard_id`, `content_sha256`, `cohort_manifest_entry`) every prior framework in
   this repository already uses.

2. **Structural reference — one pin per instrument, reuse, never duplicate.** Unlike `GLD` (which needed
   two independent pins — its own ETF classification record and its own functional-doctrine record),
   every instrument in this filing's population has exactly **one** already-sealed classification record
   to pin to. A future implementation must use a single `structural_reference` object per record: `SPY`/
   `VEA`/`VWO` pin to their own `intelligence/etf_classification/<TICKER>.yaml` via
   `etf_classification_validator.canonical_record_hash()`; `BTC`/`ETH`/`SOL` pin to their own
   `intelligence/crypto_classification/<TICKER>.yaml` via `crypto_classification_validator.
   canonical_record_hash()` — both already-existing, already-tested, read-only functions, reused exactly
   as `GLD`'s own record already reuses the first of the two. The reference must independently,
   live-recompute the pinned record's hash on every validator run, rejecting a stale reference — the
   identical enforcement `GLD.yaml`'s own pin already carries.

3. **Zero-numeric default (unchanged from `XASSET-0008` §G).** No new numeric assessment field is
   authorized anywhere in this schema — stricter than the ETF classification framework's own single
   disclosed-fact carve-out (`expense_ratio_pct`). An already-sealed numeric structural fact (e.g. an
   ETF's own expense ratio) may be referenced by structural hash/source pin under this design; it does
   not become precedent for opening a general numeric assessment schema and may never be restated as a
   bare numeric-percent-shaped token anywhere in this schema's own free text.

4. **Evidence / contamination boundary (unchanged from `XASSET-0005` §3.6 / `XASSET-0008` §I).** No
   live account-specific value from `holdings.yaml`, no `target_pct` from `targets.yaml`, no live
   `margin_state.py` output, and no current dollar balance may be used as evidence for any judgment
   axis. Existing mechanisms may be cited structurally where genuinely relevant; their current live
   outputs create no investment-policy authority under this schema.

5. **`evidence_quality` (unchanged shape from every prior framework).** `comprehensive`/`partial`/
   `limited` vocabulary, required `thesis_uncertainty_statement`. Not restated in field-by-field detail
   here; supporting artifact §4.4.

6. **Synthesis handoff — categorical evidence only.** A future `instrument_economic_assessment` record's
   `cross_asset_handoff` envelope may carry only: the one substantive axis's own categorical
   determination (verbatim copy); evidence quality; uncertainty. It may never carry: a target weight; a
   rank; an IN/OUT selection; a buy/sell/hold/trim/exit/wait/stage signal of any kind; a sleeve
   percentage; a trade-timing recommendation; a leverage amount. The future cross-asset synthesis, not
   this design, compares competing uses of capital (`XASSET-0001` §E/§F, unaffected).

7. **Content-authorization batching, left open.** This design does not itself decide whether a future
   content-authorization filing covers all six instruments in one unit, splits by asset type (ETF vs.
   crypto, mirroring `XASSET-0003`/`XASSET-0004`'s own separate-content precedent), or some other bounded
   split — that remains the future authorization filing's own choice to make and justify, exactly as
   `XASSET-0006` §A point 3 left the functional-doctrine-versus-overlap-model validator-module
   architecture question open for the second content authorization to resolve. This filing supplies the
   methodology either shape would draw on unmodified.

### E. ETF-specific methodology (`SPY`, `VEA`, `VWO`)

**Disposition table** (candidate questions evaluated; full reasoning in supporting artifact §5):

| Candidate question | Disposition | Reasoning |
|---|---|---|
| "Is this ETF's cost/tracking-quality profile economically ordinary or notable for its category?" | **Kept** → `cost_and_tracking_quality_economic_significance` | Genuinely new categorical judgment; each record's own sealed `cost_and_tracking_quality.expense_ratio_pct`/`tracking_quality_category` is a structural fact only, never characterized as ordinary/elevated/favorable anywhere today. |
| "How readily can this fund's position be deployed toward a future opportunity?" | **Rejected — already answered at the classification layer** | All three records' own sealed `liquidity.liquidity_tier: high_liquidity` (Preflight, above) already answers this; unlike `GLD`/`CASH_LIKE_CAPITAL` (genuinely non-standard capital-use states), `SPY`/`VEA`/`VWO` are ordinary, highly liquid, market-traded instruments already flowing through the standard `allocate.py` deposit/allocation workflow exactly like any equity — no distinguishing question remains to ask. |
| "How has this fund historically behaved during major equity-market drawdown periods?" | **Rejected — structurally tautological for this population** | `SPY`/`VEA`/`VWO` are each, by their own sealed `structural_role.role_category`, broad equity-market-beta vehicles — asking how equity-market beta behaves during an equity-market drawdown restates the drawdown itself, not a distinguishing ETF-specific economic characteristic. This also avoids extending equity-methodology territory reserved to the `VALUATION-####` series. |
| "Is this fund's constituent look-through overlap with directly held equities economically significant?" | **Rejected — already the overlap model's own mechanism, not duplicated here** | Already computed structurally at the classification layer (`overlap_and_concentration`) and cross-referenced by `XASSET-0007`'s own sealed `issuer_overlap_etf_lookthrough` dimension. A second, narrative overlap judgment here would duplicate, not supplement, an already-governed mechanism. |
| "Does this fund's current market price suggest it is under/overvalued?" | **Rejected outright** | A valuation/price-target question, permanently prohibited by `CLAUDE.md`'s Guardrails, already forced `valuation_required` on every ETF's own sealed classification record. |

**Result: one substantive axis, `cost_and_tracking_quality_economic_significance`** — closed vocabulary
`in_line_with_category` | `elevated_vs_category` | `favorable_vs_category` | `unable_to_determine`
(required `abstention_reason`) — plus `evidence_quality`. No compound axis is needed; unlike `GLD`
(which required three independently-abstainable sub-fields), the ETF sub-population's only genuinely new
question is this one categorical cost/tracking judgment. Full field spec in supporting artifact §5.2.

### F. Crypto-specific methodology (`BTC`, `ETH`, `SOL`)

**Disposition table** (candidate questions evaluated; full reasoning in supporting artifact §6):

| Candidate question | Disposition | Reasoning |
|---|---|---|
| "How has this coin historically behaved during major equity-market drawdown periods?" | **Kept** → `macro_behavioral_characterization.historical_equity_market_drawdown_behavior` | Genuinely new, single-asset, historically-grounded question — directly analogous to `GLD`'s own already-accepted `historical_equity_drawdown_behavior` sub-field, structurally distinct from `XASSET-0007`'s own `defensive_offset_interface` dimension (portfolio-level, still forced `not_yet_computable_interface_only`). |
| "Is this coin's historical relationship with inflation regimes established in citable literature?" | **Kept** → `macro_behavioral_characterization.historical_inflation_sensitivity_narrative` | Directly analogous to `GLD`'s own already-accepted `historical_inflation_sensitivity` sub-field — the "digital gold" narrative is a genuinely citable, debated, sourceable question distinct from a forecast. |
| "Is this coin's cost/expense profile economically ordinary or notable for its category?" | **Rejected — no clean analog exists** | A cryptocurrency carries no expense ratio or fund-tracking-benchmark concept; the investor-facing cost that would be analogous (brokerage spread, execution cost) is a Robinhood-execution question entirely outside this instrument-level economic-assessment methodology's scope. Network-level transaction/fee/staking economics is already a classification-layer question (`economic_model.fee_accrual_applicable`/`staking_applicable`), not a new economic-assessment axis. |
| "How readily can this coin's position be deployed toward a future opportunity?" | **Rejected — already answered at the classification layer** | All three records' own sealed `liquidity_and_market_structure.liquidity_tier: high_liquidity` (Preflight, above) already answers this — identical reasoning to the ETF sub-population's own rejected deployability question. |
| "What is this coin's network/protocol economic significance?" | **Rejected — already fully captured at the classification layer** | `network_fundamentals`/`economic_model` already hold this territory; re-asking it here would duplicate, not supplement, the existing classification schema. |
| "Are `BTC`/`ETH`/`SOL` correlated with each other, and does that inform sizing?" | **Rejected outright — a separate, future, bounded research charter's own question, not this design's** | Each record's own sealed `correlation_and_volatility.cross_coin_correlation_status: not_yet_measured` (Preflight, above) remains classification-layer territory; a genuine cross-coin correlation study, if ever performed, requires its own separate, bounded, pre-registered charter matching `MARGIN-0005`'s/`LADDER-0001`'s own precedent — not authorized, designed, or implied by this filing. |

**Result: one compound substantive axis, `macro_behavioral_characterization`**, mirroring `GLD`'s own
`instrument_specific_economic_characterization` shape — two independently-abstainable sub-fields:

- `historical_equity_market_drawdown_behavior` — closed vocabulary
  `historically_uncorrelated_or_negatively_correlated` | `historically_mixed` |
  `historically_positively_correlated` | `unable_to_determine`, identical vocabulary to `GLD`'s own
  sub-field; mandatory non-empty `single_asset_disclosure` (§H below).
- `historical_inflation_sensitivity_narrative` — closed vocabulary
  `historically_positively_associated` | `historically_mixed_or_inconsistent` |
  `historically_weakly_associated` | `unable_to_determine`, identical vocabulary to `GLD`'s own
  sub-field.

Plus `evidence_quality`. Full field spec in supporting artifact §6.2.

### G. `GLD`/`CASH_LIKE_CAPITAL` boundary — not reopened, not migrated, not extended

`intelligence/economic_assessment/{GLD,CASH_LIKE_CAPITAL}.yaml` and `economic_assessment_validator.py`
are unaffected by this filing in every respect. This filing does not: edit either sealed record; extend
`economic_assessment_validator.py`'s own population beyond its existing, explicitly bounded two
subjects; migrate `GLD`'s existing record into this filing's new schema or directory; or treat this
filing's own new schema as superseding, narrowing, or reinterpreting `XASSET-0008`/`XASSET-0009`'s own
accepted text in any way. The two schemas remain permanently separate — `GLD`/`CASH_LIKE_CAPITAL` under
`economic_assessment_validator.py`'s own `analytical_subject`-keyed schema; `SPY`/`VEA`/`VWO`/`BTC`/
`ETH`/`SOL` under this filing's new `instrument_id`/`asset_type`-keyed schema (§J) — precisely because
`GLD`'s own dual-reference mechanism and `CASH_LIKE_CAPITAL`'s own non-instrument, legacy-reference-list
mechanism do not generalize to a population of instruments that already carry their own single,
unambiguous classification-layer identity.

### H. Crypto / overlap-model non-duplication — mandatory disclosure, reused from `XASSET-0008` §E/§6

Every future `BTC`/`ETH`/`SOL` `instrument_economic_assessment` record's
`historical_equity_market_drawdown_behavior` sub-field must carry an explicit `single_asset_disclosure`
statement — mirroring `GLD`'s own identical requirement — stating that the finding is single-asset and
historical only, and does **not** itself constitute, imply, or substitute for a computed whole-portfolio
diversification-benefit or cross-asset-correlation finding. That remains `XASSET-0007`'s own sealed
`defensive_offset_interface` and `crypto_correlation_interface` dimensions' job — both still forced
`not_yet_computable_interface_only` under `XASSET-0005` §6.2's unconditional rule, unaffected by this
filing.

### I. Future research interface — six named, unanswered questions

Supporting artifact §7 identifies, without answering, one research question per instrument on the sole
substantive axis each carries: `SPY`'s, `VEA`'s, and `VWO`'s own cost/tracking-quality economic
significance (feeds `cost_and_tracking_quality_economic_significance`, three separate determinations);
`BTC`'s, `ETH`'s, and `SOL`'s own historical equity-market-drawdown behavior and historical
inflation-sensitivity characterization (feeds `macro_behavioral_characterization`'s two sub-fields, six
separate determinations across three coins). This filing conducts no research toward any of the six and
treats none as already answered.

### J. Storage and validator specification (for the future implementing PR)

**Storage**: a new, separate directory, `intelligence/instrument_economic_assessment/`, one file per
instrument (`SPY.yaml`, `VEA.yaml`, `VWO.yaml`, `BTC.yaml`, `ETH.yaml`, `SOL.yaml`) plus
`COHORT_MANIFEST.yaml` — filesystem-is-the-index, matching every prior classification/economic-
assessment schema's own convention. Deliberately separate from `intelligence/economic_assessment/`
(§G) — the same "different schema, different directory" convention already applied to
`intelligence/classification/` (equity) versus `intelligence/etf_classification/` versus
`intelligence/crypto_classification/`, three directories for the same conceptual layer split by asset
type.

**Validator**: one new dedicated module, `instrument_economic_assessment_validator.py` (matching this
repository's established one-schema-one-validator-module norm), `asset_type`-conditional shape,
enforcing at minimum (full sixteen-point specification in supporting artifact §9):

1. Exact population enforcement — exactly six `instrument_id` values across the two named `asset_type`
   values, no `GLD`, no seventh/eighth instrument.
2. Closed schema at every level, rejecting extra keys, not just missing ones.
3. `asset_type`-conditional shape enforcement — `cost_and_tracking_quality_economic_significance`
   required on `etf` only, forbidden on `cryptocurrency`; `macro_behavioral_characterization` required
   on `cryptocurrency` only, forbidden on `etf`.
4. `structural_reference` enforcement — a live recompute of the pinned record's hash via the correct
   `canonical_record_hash()` function selected by `asset_type`, rejecting a stale or wrong-schema
   reference.
5. No cross-schema field-name leakage — a forbidden-key scan barring every equity-, ETF-classification-,
   crypto-classification-, functional-doctrine-, overlap-model-, and `economic_assessment`
   (`GLD`/`CASH_LIKE_CAPITAL`)-shaped key name from appearing anywhere in an
   `instrument_economic_assessment` record.
6. Zero numeric field anywhere — the same forbidden-key/forbidden-pattern scan `XASSET-0008` §11 point 6
   specifies, with no carve-out of any kind.
7. No chart-evidence leakage — the same term-list free-text scan every prior validator already uses.
8. No directive/trading-language leakage — a word-boundary-matched scan for the shared eight words.
9. No predictive-language leakage — a dedicated, independent scan for forward-looking terms (`forecast`,
   `predict`, `expected to`, `will likely`, `projected`) inside both crypto sub-fields' own free text.
10. Crypto/overlap-model non-duplication check (§H) — a dedicated scan confirming no `BTC`/`ETH`/`SOL`
    record's `historical_equity_market_drawdown_behavior` is represented as a computed portfolio-level
    correlation or diversification-benefit finding, and that `single_asset_disclosure` is present and
    non-empty.
11. Evidence/provenance validation — every `provenance.sources` entry carries a type and access-status
    field.
12. Allocator/margin decoupling — zero import coupling with `allocate.py`/`margin_state.py` in either
    direction.
13. Deterministic generation — repeated runs against the same input produce byte-identical results.
14. Protected-path isolation — zero diff on `targets.yaml`, `holdings.yaml`, `gates.yaml`,
    `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing
    `intelligence/classification|companies|themes|relationships|etf_classification|crypto_classification|
    functional_doctrine|overlap_model|economic_assessment/` record, and every existing governance
    decision file.
15. Abstention independently checked — `not_applicable` used only where the schema permits it (never on
    the one required substantive axis for either asset type — both `SPY`/`VEA`/`VWO`'s
    `cost_and_tracking_quality_economic_significance` and `BTC`/`ETH`/`SOL`'s
    `macro_behavioral_characterization` sub-fields have some determinate value or an honest
    `unable_to_determine`, never a bare absence).
16. `abstention_index` independently reconciled against every genuine `unable_to_determine` value
    actually present — never a self-declared flag trusted alone, learning directly from
    `etf_classification_validator.py`'s own MINOR-1 finding and `reconciliation_validator.py`'s own
    disclosed MINOR gap.

### K. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **One new additive gate, `xasset0009-implementation-post-merge-verification`**, recording — without
   editing the `xasset0009-economic-assessment-content-implementation` gate's own historical text — that
   `PR #294` is fully merged (merge commit `3a7c89e6f4137c7ee37c643af1dc3f6a58d4912c`), matching the
   already-confirmed-live state this filing's own Preflight independently re-verified. The gate's own
   review/merge lifecycle otherwise remains as that PR's own record states; this filing does not perform
   or claim its independent review.
2. **`active_branch` set to this filing's own branch, `last_verified_main_sha` updated**
   `9fa5ac9370b04c255dee31d183a00db96e7fae09` → `3a7c89e6f4137c7ee37c643af1dc3f6a58d4912c`, and
   **`last_verified_date` updated** to this filing's own date.
3. **One additive gate, `xasset0010-etf-crypto-economic-assessment-methodology-design`**, recording this
   filing's own branch and PR number — `status: in_progress`, **not** `status: complete`, matching every
   prior filing's identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: `XASSET-0009`'s own economic-assessment
   content step (GLD/CASH_LIKE_CAPITAL) is complete and merged; this filing, once merged, designs but
   does not authorize a future ETF/crypto instrument economic-assessment content step for `SPY`/`VEA`/
   `VWO`/`BTC`/`ETH`/`SOL`; `DEBT_REDUCTION` economic assessment, the `CASH`/`RESERVE` consolidation
   question, and every other remaining `WS-0014` item (this entry's own step numbering) remain wholly
   unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`,
`completion_criteria`, `roadmap_preservation`) is changed. `WS-0005` and `WS-0015` are not touched by
this filing.

## Rationale

**Why one filing, two asset classes, no new prefix.** `XASSET-0002` already established the identical
batching precedent for ETF+crypto **classification** design, and `XASSET-0008` already established that
this repository's `XASSET-####` series is the correct continuation point for economic-assessment
methodology specifically (§5 of that filing's own restated sequence). Both are directly on point; no new
architecture is needed to justify batching this filing the same way.

**Why this design does not reuse `economic_assessment_validator.py`'s own schema.** That module's own
docstring explicitly scopes it to "the first (and only, per `XASSET-0009`'s own bounded authorization)"
batch — `GLD` and `CASH_LIKE_CAPITAL` specifically, keyed by `analytical_subject`. Every member of this
filing's own population, by contrast, is a real, already-classified instrument with its own single,
unambiguous classification-layer identity (`instrument_id`) — a materially simpler shape than `GLD`'s own
dual-reference mechanism or `CASH_LIKE_CAPITAL`'s own non-instrument, two-legacy-reference-list
mechanism. Forcing this population into that existing schema would either strip away the genuine
structural difference or silently widen an authorization `XASSET-0009` deliberately bounded to two
subjects — the same reasoning `TIER-0002`/`XASSET-0002` both already applied when declining to force ETF
or crypto evidence into the equity-shaped Company Intelligence schema.

**Why the ETF sub-population gets one axis and the crypto sub-population gets a two-sub-field compound
axis.** The disposition tables (§E, §F) are not symmetric by design choice — they are symmetric in
*method* (every candidate question is evaluated against the same "does this materially improve a future
decision, and is it genuinely new versus already answered at the classification layer" test) but
asymmetric in *result*, because `SPY`/`VEA`/`VWO` are structurally simpler instruments (broad,
diversified, single-currency, high-liquidity index funds with no non-tautological historical-behavior
question available to ask) than `BTC`/`ETH`/`SOL` (assets with a genuinely open, citable, and currently
unanswered "digital gold" macro narrative). Forcing an artificial second axis onto the ETF sub-population
merely to match crypto's shape would violate the controlling directive's own anti-sidetrack rule — "if a
proposed addition does not unblock ETF/crypto economic assessment, omit it."

**Why `deployability_and_optionality` is not reused for any of these six instruments.** `GLD`'s and
`CASH_LIKE_CAPITAL`'s own version of that axis existed because both represent genuinely non-standard
capital-use states (a commodity-backed fund functioning as portfolio ballast; a non-instrument cash-like
capital family) whose "optionality" was not already answered anywhere. Every one of the six instruments
in this filing's own population already carries a sealed, high-liquidity classification-layer finding and
already flows through the ordinary `allocate.py` deposit/allocation workflow exactly like any directly
held equity — reusing the axis here would be pure duplication, not new evidence.

**Why a new directory and a new validator module, rather than extending an existing one.** This
repository's own established convention — `intelligence/classification/` versus
`intelligence/etf_classification/` versus `intelligence/crypto_classification/`, each its own directory
and its own validator for the same conceptual (classification) layer split by asset type — is directly
on point and is reused here for the economic-assessment layer, rather than inventing a different
organizing principle.

## Alternatives Considered

**Extend `economic_assessment_validator.py`'s own schema and population to cover all eight instruments
(`GLD`, `CASH_LIKE_CAPITAL`, plus these six).** Rejected — that module's own docstring and `XASSET-0009`'s
own authorization explicitly bound it to exactly two subjects; silently widening it would exceed this
filing's own authority and would force a materially different reference mechanism (`GLD`'s dual pin;
`CASH_LIKE_CAPITAL`'s two-entry legacy list) onto a population that needs neither.

**File separate ETF-only and crypto-only design filings instead of one combined filing.** Rejected —
`XASSET-0002`'s own precedent for the adjacent classification layer already establishes that batching the
*design* step (never the *content* step) for both asset types in one filing is the correct economy, and
this filing's own §C explicitly does not extend that batching to any future content-authorization step.

**Design a full 7×7-style methodology-family-by-archetype matrix, mirroring the equity `VALUATION-####`
series.** Rejected, matching `XASSET-0008` §1's identical reasoning — six fixed instruments across two
asset types present no archetype-differentiation question requiring a matrix; a closed, per-asset-type
disposition table (§E, §F) is the right-sized tool.

**Give `SPY`/`VEA`/`VWO` a compound axis symmetric with crypto's own two-sub-field shape, inventing a
second ETF-specific question to fill it.** Rejected — no genuinely new, non-duplicative ETF-specific
question survived the disposition table (§E); manufacturing one merely for symmetry would violate the
controlling directive's own instruction to omit any addition that does not unblock ETF/crypto economic
assessment.

**Attempt a cross-coin correlation study for `BTC`/`ETH`/`SOL` as part of this filing, since the
classification layer already flags `cross_coin_correlation_status: not_yet_measured`.** Rejected outright
— a genuine correlation study is a separate, bounded, pre-registered research charter in the shape of
`MARGIN-0005`/`LADDER-0001`, not a categorical schema-design exercise; conflating the two would exceed
this filing's own design-only authorization and duplicate territory this filing explicitly reserves to a
future, separate charter (§F).

**Design the full validator and test code as part of this filing, rather than a specification for a
future implementing PR.** Rejected, matching `TIER-0002`'s and `XASSET-0002`'s own explicit precedent —
a working validator applied against real fund/coin evidence would itself constitute the beginning of
classification content, exceeding this filing's own design-only authorization.

## Consequences

**Authorized, effective only on this decision's merge**: the closed `SPY`/`VEA`/`VWO`/`BTC`/`ETH`/`SOL`
instrument-economic-assessment methodology design in the supporting artifact (six-instrument population
across two asset types, one ETF-shared axis, one crypto-shared compound axis, one shared structural-
reference mechanism, combined validator/test specification); confirmation, via one additive
`operations/WORKSTREAMS.yaml` gate entry, that `XASSET-0009`'s own content-implementation PR (`PR #294`)
is fully merged; `WS-0014`'s ordinary self-reference synchronization.

**Not authorized by this filing, now or ever without a further separate decision**: population of any
`instrument_economic_assessment` record; any economic finding, categorical or otherwise, for `SPY`,
`VEA`, `VWO`, `BTC`, `ETH`, or `SOL`; any equity discount-rate, WACC, beta, ERP, or valuation-methodology
extension; any edit to `GLD.yaml`, `CASH_LIKE_CAPITAL.yaml`, `economic_assessment_validator.py`, or any
sealed ETF/crypto classification record; any cross-coin correlation study or numeric coefficient of any
kind; any resolution of any sealed classification record's forced `valuation_and_economic_assessment_
readiness.status`; any overlap-model dimension computation; any cross-asset opportunity-cost synthesis;
any Level 1 sleeve or Level 2 instrument sizing; any chart evidence of any kind; any validator or test
implementation; any contender-competition, contender-registry, or legacy-history-recovery work; any edit
to `XASSET-0001` through `XASSET-0009`'s own text; and any tier/target/holdings/role/cluster/cap/gate/
allocator/margin/ladder/order/trade change of any kind.

**Unchanged by this decision**: every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification/functional-doctrine/overlap-model/economic-
assessment record, byte-for-byte, including all six sealed classification records this filing structurally
references (referenced, never modified); `XASSET-0001` through `XASSET-0009`'s own accepted text and
scope, in full, unedited; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `levels.py`, `margin_state.py`; the 1.8x leverage cap and 30% margin-buffer floor;
`WS-0005`'s completed, `status: complete` state; `WS-0015`'s own live state; `WS-0014`'s own
`status: proposed`/`priority: secondary`.

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ
is not a 27-stock system, and this filing's own bounded six-instrument methodology design does not narrow
that fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical equities;
contender-registry regeneration and legacy-history recovery; `QQQ` and any other future ETF or crypto
candidate expansion; equity Stage-4 valuation execution beyond the sealed 27-company cohort;
`DEBT_REDUCTION` economic assessment; whether `CASH`/`RESERVE` should ultimately be consolidated
(`XASSET-0008` §N); the future `SPY`/`VEA`/`VWO`/`BTC`/`ETH`/`SOL` economic-assessment content
authorization and implementation this filing's own methodology would draw on; a future cross-coin
correlation study; cross-asset opportunity-cost synthesis; Level 1 sleeve allocation; Level 2 instrument
allocation; `CHART-0003` and any remaining governed chart ingestion; ladder/deployment integration;
unlevered testing; margin/leverage-policy review; monitoring/sell discipline; final integration and audit;
and any true whole-universe allocation test.
