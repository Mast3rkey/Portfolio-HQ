# WS-0014 ETF Classification Implementation — retained artifact

**Authorized by**: `XASSET-0003` (`governance/decisions/XASSET-0003-ws0014-etf-classification-content-authorization.md`), merged PR #269, merge commit `e764c1b6cb1d12c5a6aed73b0204e09b62c13309`.
**Date**: 2026-08-07
**Scope**: `XASSET-0001` §J step 4 / §I item 5 — ETF blind-classification content for the four canonical fund destinations. No crypto content, no valuation, no GLD functional/defensive-role determination, no cross-asset synthesis, no policy change.

This artifact is the retained implementation record. `XASSET-0002`'s own supporting artifact (`governance/audits/WS0014_ETF_CRYPTO_CLASSIFICATION_FRAMEWORK_DESIGN_20260807.md`) remains the accepted process specification — this document records what was done under it, not a restatement of the specification itself.

## 1. Preflight, independently re-verified this session

- Repository `Mast3rkey/Portfolio-HQ`, branch `claude/etf-classification-content-izagzk` initially, working tree clean at session start; new branch `claude/etf-classification-implementation-3x48kf` created for this implementation.
- `HEAD`/`origin/main`/GitHub `main` all confirmed identical at `e764c1b6cb1d12c5a6aed73b0204e09b62c13309` (`XASSET-0003`'s own merge commit, PR #269) before any file was written.
- Zero open pull requests confirmed live via the GitHub API — no competing mutation lane.
- `XASSET-0002`'s supporting artifact read in full (749 lines) — §3 (ETF field-by-field design), §5 (GLD placement), §6 (shared envelope), §8 (validator spec), §9 (test spec) are the controlling text this implementation binds to.
- `XASSET-0003` read in full — §A (population, single-pass authorization), §B (binding-by-reference table), §C (evidence standard), §D (stop conditions), §E (independent review requirements).
- `targets.yaml` independently re-read: exactly four `asset_class: fund` rows — `SPY` (15.00%), `VEA` (7.00%), `VWO` (1.00%), `GLD` (4.00%). No fifth fund row. Population unchanged since `XASSET-0003`'s own preflight.
- `issuer_lookthrough.yaml` independently re-read: `funds:` entries across all 11 issuer rows name only `SPY`, `VEA`, `VWO` — `GLD` confirmed absent from every fund-carrier reference.
- `intelligence/relationships/*.yaml` grepped for `SPY`/`VEA`/`VWO`/`GLD` — zero matches, confirmed no relationship record currently names any of the four funds.
- `intelligence/contenders/registry.yaml` re-read: `SPY`/`VEA`/`VWO`/`GLD` all `asset_type: fund`, `primary_disposition: requires_research`; `QQQ` carries `primary_disposition: benchmark_or_index`, `current_target: false` — confirmed excluded.
- No `intelligence/etf_classification/` directory existed prior to this implementation.
- Decision catalog independently rebuilt: 92 decisions, `issues == ()` at the starting head.

No condition met a Stop bar (§D). This unit proceeded.

## 2. Single implementation pass, no multi-shard isolation

Per `XASSET-0003` §A.2, `XASSET-0002`'s own Rationale already determined multi-shard isolation unnecessary at this population scale (ETF ≤ 4). Reconfirmed: the population is still exactly four instruments (§1 above) — the determination holds. One drafting pass covered all four instruments; no per-fund PR structure, no sanitization/redaction pipeline (none is required — no ETF evidence source embeds portfolio-policy content, per `XASSET-0002`'s own §5/Rationale).

## 3. Evidence access — disclosed limitation

Every attempted direct fetch of a primary issuer, index-provider, or SEC-filing document was blocked by this environment's network egress policy: `www.ssga.com`, `investor.vanguard.com`, `advisors.vanguard.com`, `www.spdrgoldshares.com`, `www.sec.gov`, `etfdb.com`, and `en.wikipedia.org` all returned `EGRESS_BLOCKED`. This matches this repository's own extensively disclosed prior pattern of primary-source access failures (Batch 1–9 Company Intelligence research, `PI-0038`'s gated-six batch, and others).

All evidence in this implementation was gathered via `WebSearch`, which aggregates and cites underlying sources but does not itself constitute direct inspection of a primary document. Every `provenance.sources` entry in every record is labeled honestly:

- `source_type: primary` + `access_status: attempted_not_directly_inspected` for the issuer/SEC pages that were attempted and blocked (disclosed with the specific blocking domain as the `limitation`).
- `source_type: secondary` + `access_status: consulted_via_search_aggregation` for the actual WebSearch-returned, cited content that supplied every fact used.

Every record's `evidence_quality.primary_source_coverage` is `partial` — not `comprehensive` (no primary document was directly opened) and not `limited` (multi-source, cross-corroborated secondary coverage was obtained across nearly every axis). No evidence was invented, assumed by analogy from another fund, or backfilled from a company's own Company Intelligence record (`XASSET-0003` §C).

One genuine unresolved evidence conflict was found and disclosed rather than silently resolved: VWO's own China country-weight figure was reported inconsistently within the same search aggregation (~20% vs. ~32%) — recorded in the VWO record's `thesis_uncertainty_statement` and the corresponding source's `limitation` field, not averaged or picked.

No axis on any of the four records reached `unable_to_determine`/`not_yet_measured`-as-abstention except `cost_and_tracking_quality.tracking_quality_category`, which is `not_yet_measured` on all four — a precise, sourced tracking-difference figure (distinct from the disclosed expense ratio itself, a cost fact rather than a measured tracking-error figure) could not be located via search aggregation for any of the four funds, and `not_yet_measured` is itself a first-class vocabulary value for exactly this case (`XASSET-0002` supporting artifact §3.2), not an `unable_to_determine` abstention requiring a reason field.

## 4. Per-fund classification summary

All four records: `schema_version: '1.0'`, `asset_type: etf`, `record_status: sealed`, `evidence_quality.primary_source_coverage: partial`, `valuation_and_economic_assessment_readiness.status: valuation_required` (zero exception), `abstention_index: []` (no axis abstained on any record).

| Field | SPY | VEA | VWO | GLD |
|---|---|---|---|---|
| `structural_role.role_category` | `broad_market_beta` | `developed_ex_us_equity` | `emerging_market_equity` | `precious_metals_or_commodity` |
| `constituent_exposure.geographic_concentration` | `domestic_us` | `developed_ex_us` | `emerging_markets` | `not_applicable` |
| `constituent_exposure.sector_concentration` | `broad_diversified` | `broad_diversified` | `broad_diversified` | `not_applicable` |
| `constituent_exposure.currency_exposure` | `usd_only` | `foreign_currency_mixed` | `foreign_currency_mixed` | `usd_only` |
| `overlap_and_concentration.not_applicable` | `false` | `false` | `false` | `true` |
| `overlap_and_concentration.measured_by_existing_mechanism` | `true` | `true` | `true` | absent |
| `cost_and_tracking_quality.expense_ratio_pct` | `0.0945` | `0.03` | `0.06` | `0.40` |
| `cost_and_tracking_quality.tracking_quality_category` | `not_yet_measured` | `not_yet_measured` | `not_yet_measured` | `not_yet_measured` |
| `liquidity.liquidity_tier` | `high_liquidity` | `high_liquidity` | `high_liquidity` | `high_liquidity` |
| `structure_and_methodology.replication_method` | `physical_full_replication` | `physical_full_replication` | `physical_sampling` | `direct_physical_commodity_holding` |
| `structure_and_methodology.benchmark_type` | `published_market_index` | `published_market_index` | `published_market_index` | `spot_commodity_price` |

`overlap_and_concentration` was computed mechanically, after the six judgment fields above sealed, directly from `issuer_lookthrough.yaml`'s live `funds:` entries — SPY/VEA/VWO each carry at least one constituent-weight entry there (fund carriers); GLD carries zero (confirmed §1), correctly resolving `not_applicable: true` per `XASSET-0002` §5's own predicted, evidenced outcome — not a schema failure.

## 5. GLD structural-only boundary — confirmed observed

GLD's record contains no functional-role, defensive-role, ballast, "should be held," or portfolio-allocation content of any kind. `structural_role.role_category` records only the fund-type fact (`precious_metals_or_commodity`); `constituent_exposure`/`overlap_and_concentration` correctly resolve `not_applicable` as GLD's own genuine structural fact (a physically-backed commodity trust has no equity constituents to look through), exactly as `XASSET-0002` §5 predicted before this implementation began. No future functional/defensive-role determination is made, implied, or foreshadowed here — that remains reserved to a fully separate, future, functional-doctrine unit under `XASSET-0001` §D.

## 6. Sequencing — judgment before mechanical rollup

Per `XASSET-0003` §B, the five narrative/evidence-sourced fields (`structural_role`, `constituent_exposure`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`) were drafted from the evidence gathered in §3, and only then was `overlap_and_concentration` computed mechanically from `issuer_lookthrough.yaml`'s live state (§4) — no mechanical result back-propagated into or altered any judgment field.

## 7. Artifact structure and sealing

`intelligence/etf_classification/{GLD,SPY,VEA,VWO}.yaml` — four sealed records, plus `COHORT_MANIFEST.yaml` (schema_version, governing_decision `XASSET-0003`, one row per instrument with `content_sha256` matching each record's own recorded hash). Every record's `content_sha256` excludes only the five seal fields (`sealed_at`, `governing_decision`, `drafting_session_or_shard_id`, `content_sha256`, `cohort_manifest_entry`) and was independently recomputed and verified matching by `etf_classification_validator.py`. `cross_asset_handoff` and the top-level `uncertainty_summary`/`evidence_quality_status`/`structural_risk_flags` fields are read-only projections of their source axis fields, verified for exact consistency (`XASSET-0002` §6.2) — not independently computed.

## 8. Validator and tests

`etf_classification_validator.py` (new): closed schema at every level (envelope, axis, provenance source, manifest row) with extra-key rejection; exact four-instrument population enforcement with explicit `QQQ` rejection; asset-type separation (`etf` only); no equity-field or crypto-field leakage anywhere in the document tree; no numeric score/rank/target-key leakage (scoped to permit the sole legitimate `expense_ratio_pct` field); an independent free-text scan for forbidden recommendation-shaped phrases, directive/trading language (word-boundary matched), and sixteen chart-domain terms; abstention-semantics validation (`not_applicable` vs. `unable_to_determine`, never conflated, never cascading); envelope read-only-projection consistency; forced `valuation_required` check; live mechanical recompute of `overlap_and_concentration` against `issuer_lookthrough.yaml` (never trusting a record's own cached claim); deterministic hashing; manifest bidirectional reconciliation. Zero import coupling with `allocate.py`/`margin_state.py`.

`test_etf_classification_validator.py` (new): 94 focused tests covering happy-path records for all four instruments, malformed top-level/axis schema, extra/missing keys at every level, wrong `asset_type`, equity- and crypto-field leakage, invalid evidence citations, all abstention-semantics paths, duplicate/missing/extra-instrument population checks (including explicit `QQQ` rejection), numeric/score/rank leakage, the scoped `expense_ratio_pct` acceptance test, all sixteen chart terms individually proven caught, all eight directive words individually proven caught (plus a "holdings" noun false-positive guard), forced-`valuation_required` violation, every envelope-projection-mismatch case, hash/manifest mismatch, determinism, protected-path isolation, and an allocator/margin import-coupling check.

## 9. Full validation results (this session)

- `etf_classification_validator.py`: `OK (5 result(s))`
- `classification_validator.py`: `OK (28 result(s))`
- `reconciliation_validator.py`: `OK (27 tickers)`
- `recommendation_validator.py`: `OK (27 tickers)`
- `relationship_validator.py`: `OK (13 record(s))`
- `intelligence_validator.py`: clean (exit 0)
- `freshness_validator.py`: `OK`
- `contender_registry_validator.py`: `OK (84 entries)`
- `test_etf_classification_validator.py`: **94 passed**
- Full repository `pytest`: **3185 passed, 0 failed** (3091 pre-existing baseline + 94 new tests, exact match; 1 pre-existing unrelated deprecation warning)
- `test_portfolio_hq_dashboard_decisions.py`: **95 passed** (decision catalog unchanged at 92 decisions, `issues == ()` — no new governance decision filed by this implementation, matching the `TIER-0005`→Milestone-6-implementation precedent)
- YAML/YML parsing: 141 files, 0 errors. JSON parsing: 178 files, 0 errors.
- `git diff --check`: clean
- Changed-file inventory: exactly 10 files — 2 modified (`CLAUDE.md`, one Decisions Log pointer entry; `operations/WORKSTREAMS.yaml`, the Lane M synchronization and new gates described in §1/§9 above), 8 new (`etf_classification_validator.py`, `test_etf_classification_validator.py`, this retained audit, `intelligence/etf_classification/{COHORT_MANIFEST,GLD,SPY,VEA,VWO}.yaml`)
- Protected-path scan (`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing `intelligence/classification|companies|themes|relationships|reconciliation|recommendations|contenders/` file, `governance/decisions/`, `governance/evidence/`): zero diff
- Zero crypto content anywhere (independently grepped for all five crypto-only field names — zero matches)
- Zero valuation output anywhere (`valuation_and_economic_assessment_readiness.status == valuation_required` on all four records, independently verified)
- Zero `priority: primary` workstreams, unaffected (`WS-0005` remains `secondary` per `TIER-0013`) — corrects this section's own original claim of "exactly one," below

## 10. What this implementation does not do

No crypto classification of any kind (BTC/ETH/SOL untouched, not referenced). No GLD functional/defensive-role determination. No valuation or economic-assessment methodology. No cash/reserve/GLD/debt functional doctrine. No cross-asset overlap, concentration, or opportunity-cost synthesis beyond the one mechanical `overlap_and_concentration` rollup this framework itself authorizes. No sleeve-level or instrument-level sizing. No tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/chart/order/trade change of any kind. No edit to `XASSET-0001`, `XASSET-0002`, `XASSET-0003`, or any of their own text. No new governance decision filed — this is the one implementation PR `XASSET-0003` itself authorized.

This session does not review its own PR, mark it ready, merge it, or post principal acceptance. Draft PR; not merged, not independently reviewed, not principal-accepted in this session — effective only on merge.

## 11. Bounded correction (same day, this PR)

An independent exact-head review of the original head (`d00b374430e22c4d2bdcf4d5a4f86a82488a4cf2`) returned **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE** — 0 BLOCKING / 0 MAJOR / 3 MINOR / 2 NOTE. All three MINOR findings were independently reproduced live before any fix, per this repository's own standing verification discipline.

**MINOR-1, resolved** — `_validate_envelope_projection_consistency`'s `structural_risk_flags` check was gated behind `isinstance(risk_flags, dict)`, so a record with the field omitted entirely silently passed (confirmed live: a draft record missing `structural_risk_flags` validated `valid=True`). Masked for the four real sealed records only because the field is part of `_HASHABLE_KEYS`, so removing it would have broken `content_sha256` reproduction — not a live defect in the shipped content, but a genuine defense-in-depth gap relative to SS8 point 2's closed-schema requirement. Fixed by giving absence/wrong-type its own independent error, and wiring in the previously-unused `_STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS` closed-key check.

**MINOR-2, resolved** — `_FORBIDDEN_TEXT_PATTERNS` (the seven forbidden-recommendation-shaped-phrase regexes) had zero dedicated test coverage, despite SS9 explicitly naming it as its own required test item, distinct from the separately-and-well-tested directive-word and chart-term scans. Confirmed the underlying mechanism was already sound (independently triggered all seven patterns against the live validator before touching anything) — a coverage gap, not a defect. Fixed with seven parametrized tests in `test_etf_classification_validator.py`.

**MINOR-3, resolved, narrowly** — `abstention_index` was checked only for its own internal per-entry shape, never cross-checked against the axes it claims to summarize. Confirmed live: a synthetic record with a real `structural_role.role_category: unable_to_determine` abstention and an empty `abstention_index` validated `valid=True` — the same "self-declared flag, no independent scan" defect class SS9.1 already names as a carried-forward lesson. Fixed with a new `_check_abstention_index_completeness` function requiring every field literally set to `unable_to_determine` to have a matching `abstention_index` entry. **Deliberately left unresolved, per `XASSET-0003` SS B's own instruction not to settle a specification ambiguity unilaterally inside this implementation**: whether `cost_and_tracking_quality.tracking_quality_category`'s separate `not_yet_measured` value — the value all four real records in this batch use, reached because a precise sourced tracking-difference figure could not be located — should also populate `abstention_index` is a genuine ambiguity in `XASSET-0002`'s own text (its "Abstention state" prose for that axis names `unable_to_determine` as the abstention path, while separately listing `not_yet_measured` as a plain vocabulary value). A dedicated test (`test_not_yet_measured_does_not_require_abstention_index_entry`) makes this non-resolution explicit and pins the current behavior; resolving it either way remains a future, separate `XASSET-0002` amendment or governance clarification, not performed here.

**Also corrected, independently caught (not part of the review)**: this artifact's own §9 line claiming "exactly one `priority: primary` workstream (`WS-0005`)" was stale — live `operations/WORKSTREAMS.yaml` confirms zero `priority: primary` workstreams (`WS-0005` transitioned to `secondary` under `TIER-0013`, already true before this PR began). Corrected above.

No content of any of the four sealed records changed by this correction — none uses `unable_to_determine` or omits `structural_risk_flags`, so all four continue to validate clean under the strengthened checks. **Full re-validation at the corrected head**: `etf_classification_validator.py` `OK (5 result(s))`; all seven pre-existing Intelligence validators clean and unaffected; `test_etf_classification_validator.py` **108 passed** (up from 94 — 14 new/updated tests); full repository `pytest` **3199 passed, 0 failed** (3185 + 14, exact match); decision catalog unchanged at **92, `issues == ()`**; `git diff --check` clean; zero diff on every protected path.

This correction does not itself constitute review, mark this PR ready, merge it, or post principal acceptance — requesting a fresh independent exact-head delta review.
