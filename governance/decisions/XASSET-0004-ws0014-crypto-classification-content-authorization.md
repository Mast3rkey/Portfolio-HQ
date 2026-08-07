---
decision_id: XASSET-0004
date: 2026-08-07
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0004, TIER-0005, TIER-0007, TIER-0009, REL-0001, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002, XASSET-0003]
supporting_artifact: null
file: governance/decisions/XASSET-0004-ws0014-crypto-classification-content-authorization.md
---

## Context

### Authority for this unit

`XASSET-0002`'s own unlettered "Numbering note" paragraph, within its `## Decision` section, states,
verbatim: "crypto classification (§I item 7 / §J step 5) ... require[s] its own separate, future,
explicit principal authorization and independent-review lifecycle, and this filing does not combine,
foreshadow, or pre-stage either." The supporting artifact's §7 restates this as a binding future-lifecycle
rule (points 3 and 5): "Crypto classification content is its own future, separate implementation PR ...
ETF and crypto content must never share one filing." This filing is that separate, future, explicit
authorization for crypto classification content specifically. It authorizes; it does not classify.

This mirrors `XASSET-0003`'s own identical role for the ETF sleeve, one asset type later:
`TIER-0001`/`TIER-0002` designed the equity framework; `TIER-0004` specified population/sequencing/
sealing mechanics; `TIER-0005` authorized — as its own separate filing, zero classification content —
the Milestone 6 implementation. `XASSET-0002` plays the combined `TIER-0002`+`TIER-0004` role for both
the ETF and crypto frameworks in one filing. `XASSET-0003` played `TIER-0005`'s role for ETFs; this
filing plays that same role for crypto: authorization only, binding by reference to the already-accepted
design, no restatement, no redesign.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/xasset-0004-crypto-auth-p78mjm`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD`, `origin/main`, and GitHub `main` (confirmed via
  `list_commits`) all identical at `7441c274f4bfea29da493dc7cfe99373e5f12b17` — `PR #270`'s own merge
  commit (the ETF classification implementation).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #270` independently re-confirmed in full** via the GitHub API, not taken from any prior summary:
  implementation-summary comment (`issuecomment-5222459479`, exact head
  `d00b374430e22c4d2bdcf4d5a4f86a82488a4cf2`); first independent exact-head review
  (`pullrequestreview-4887000299`, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR
  / 3 MINOR / 2 NOTE); one bounded correction (`issuecomment-5222886655`, corrected head
  `67cb63ec406de9634d576a03547a8a25a2c8ce7c`, resolving all three MINOR findings — an independent
  `structural_risk_flags` presence/type check, seven parametrized forbidden-recommendation-phrase tests,
  and a narrow `abstention_index` completeness check that deliberately preserves, rather than resolves,
  the `not_yet_measured`-versus-formal-abstention ambiguity in `XASSET-0002`'s own text); corrected-head
  delta review (`pullrequestreview-4887150210`, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0
  BLOCKING / 0 MAJOR / 0 MINOR / 3 non-actionable NOTE); principal acceptance (`issuecomment-5222997811`,
  accepted head `67cb63ec406de9634d576a03547a8a25a2c8ce7c`); merge (`merged: true`, merge commit
  `7441c274f4bfea29da493dc7cfe99373e5f12b17`, `merged_by: Mast3rkey`, `merged_at:
  2026-08-07T22:54:32Z`, exact 10-file scope independently reconfirmed via `get_commit`); merge-commit CI
  (`workflow run 31225409654`, `head_sha` matching exactly, `status: completed` / `conclusion: success`).
  All independently re-fetched and re-read this session — not inferred from any prior summary. No
  post-merge-verification comment had yet been posted to PR #270 itself; this filing performs that
  post-merge verification as its own Lane M synchronization (§I below).
- **`XASSET-0001`, `XASSET-0002` (plus its supporting artifact), and `XASSET-0003` read in full this
  session** — not summarized from memory. `XASSET-0002`'s supporting artifact §4 (crypto framework
  field-by-field design), §6 (shared envelope), §7 point 3/5, §8 (validator specification), and §9 (test
  specification) are the controlling text this filing binds to (§B below).
- **`targets.yaml` independently re-read**: exactly three `asset_class: crypto` rows in `destination:` —
  `BTC` (2.00%), `ETH` (1.50%), `SOL` (0.50%) — zero drift from `XASSET-0002`'s own stated population
  ("BTC/ETH/SOL each carry their own destination weight").
- **`holdings.yaml` independently re-read**: `crypto_shares:` carries exactly `BTC`, `ETH`, `SOL` — no
  fourth coin.
- **`intelligence/contenders/registry.yaml` independently re-read**: `BTC`, `ETH`, `SOL` each carry
  `asset_type: crypto`, `primary_disposition: requires_research`, `classification_exists: false`,
  `current_holding: true`, `current_target: true` — correctly recording that no crypto-specific evidence
  or classification currently exists, not a blocker to this authorization (`CONTENDER-0001` §L:
  "Contender status creates evaluation eligibility only ... no ... policy ... authority"). `ZORA`, `WIF`,
  `BONK`, `PEPE`, and `HYPE` each carry `primary_disposition: explicitly_deferred_or_excluded` —
  independently confirmed absent from `targets.yaml`'s `destination:` list and from `holdings.yaml`'s
  `crypto_shares:` block (CLAUDE.md's own Standing Queue: HYPE removed from targets July 2026; ZORA/WIF/
  BONK/PEPE are Robinhood's unsellable sub-cent dust, "permanently ignored, never synced") — correctly
  excluded from the authorized population (§A).
- **No `intelligence/crypto_classification/` directory, no crypto classification content of any kind,**
  independently reconfirmed absent from the repository (the only repository-wide match for the string is
  inside `XASSET-0002`'s own supporting artifact prose) — this filing is the first to name that future
  path.
- **Decision catalog independently rebuilt**: **92 decisions, `issues == ()`** at the starting head, 92
  `.md` files in `governance/decisions/` (excluding `README.md`) reconciling 1:1. `XASSET-0004` confirmed
  the next unused identifier in the `XASSET-####` series (only `XASSET-0001`/`XASSET-0002`/`XASSET-0003`
  exist) — the direct continuation of `XASSET-0003`'s own precedent for the crypto sleeve, not a
  genuinely new decision domain, matching the `CONTENDER-0001`→`CONTENDER-0002` and
  `TIER-0004`→`TIER-0005` continuation pattern.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing does two things, in one bounded PR:

1. **Reconfirms (Lane M) that `PR #270`'s ETF classification implementation is fully merged, reviewed,
   corrected, principal-accepted, merged, and now post-merge verified**, via one new additive gate entry
   — no edit to the `xasset0003-etf-classification-implementation` gate's own historical text (§I).
2. **Authorizes exactly one future, separate, bounded crypto classification (blind-classification
   content) implementation pull request**, covering all three canonical crypto destinations under the
   exact population, evidence, sequencing, abstention, correlation-boundary, contamination, and
   validator/test controls already specified and accepted through `XASSET-0002`. It performs no
   classification itself, gathers zero crypto evidence, creates no classification record or validator,
   and implements no `intelligence/crypto_classification/` content.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007` §1),
any required bounded correction and re-review, explicit principal acceptance, merge, and post-merge
verification — the same lifecycle `XASSET-0003`→`PR #270` already completed for the ETF sleeve — may
proceed to:

1. Draft and seal one crypto classification record for each of the three canonical crypto destinations
   named in `targets.yaml`'s `destination:` list — `BTC`, `ETH`, `SOL` — zero exclusions, zero additions.
   `ZORA`, `WIF`, `BONK`, `PEPE`, and `HYPE` are explicitly excluded (§ Preflight): none is a
   `targets.yaml` destination row or a `holdings.yaml` `crypto_shares:` entry, and each carries
   `primary_disposition: explicitly_deferred_or_excluded` in the contender registry.
2. Use a single implementation pass covering all three instruments (no per-coin PR structure; no
   multi-shard isolation apparatus of any kind) — `XASSET-0002`'s own Rationale determined shard
   isolation unnecessary at this population scale (crypto = 3, ETF ≤ 4) for the identical reasons; this
   filing makes that determination binding rather than re-litigating it. If the eligible crypto
   population grows before this authorization is exercised, the implementing session must reconfirm that
   determination still holds before proceeding, and disclose the reconfirmation in the implementation PR
   rather than silently assuming it — the same forward-looking discipline `XASSET-0003` §A point 2
   applied.
3. Gather evidence to populate the seven-field crypto schema (§C below) — this filing authorizes the
   gathering; it gathers none itself.
4. Build exactly one crypto classification validator (or one shared-envelope-helper module plus one
   crypto-specific validator, if it reuses helpers `PR #270`'s `etf_classification_validator.py` already
   built for the shared envelope — that determination belongs to the implementing session, not to this
   filing) and its dedicated test file, per `XASSET-0002`'s supporting artifact §8/§9.
5. Stop after the first instrument, without a separate pilot authorization, if a systemic schema,
   evidence, or contamination defect is discovered — an internal stop-and-fix condition within the one
   authorized implementation PR, not a license to split into a second governance filing or a
   per-instrument PR structure.

**No ETF classification content, edit, or re-classification of any kind is authorized by this filing.**
`SPY`/`VEA`/`VWO`/`GLD`'s sealed records (`PR #270`) are unaffected and must not be touched by any
implementation this filing authorizes.

### B. Binding specification — by reference, not restatement

The implementation PR must follow `XASSET-0002`'s specification exactly, as accepted and merged at
`f06dc014dd61ee00d68155b196642bbb40dc87ee`. This filing does not redesign, loosen, tighten, or restate
that specification in its own words beyond the index below — the implementation session has no
discretion to depart from it:

| Control | Governing section (all `XASSET-0002 §N` citations refer to `XASSET-0002`'s supporting artifact, `governance/audits/WS0014_ETF_CRYPTO_CLASSIFICATION_FRAMEWORK_DESIGN_20260807.md` — `XASSET-0002`'s own decision file uses no numbered or lettered sections) |
|---|---|
| 3-instrument population, zero exclusions, `ZORA`/`WIF`/`BONK`/`PEPE`/`HYPE` explicitly out | This filing §A, cross-checked against `targets.yaml`'s live `destination:` list and `holdings.yaml`'s `crypto_shares:` block at implementation time |
| Seven-field crypto schema (`network_fundamentals`, `economic_model`, `liquidity_and_market_structure`, `custody_and_counterparty_risk`, `correlation_and_volatility`, `regulatory_and_structural_uncertainty`, `evidence_quality`) — no eighth substantive axis, no `economic_role`/`capital_priority` in `TIER-0002`'s company sense, no financial-statement-derived field, no score, no ranking formula, no target percentage, no weighting formula, no buy/sell/hold/trim/exit signal | `XASSET-0002` supporting artifact §4.1–§4.3 (frozen by that filing's own acceptance) |
| Explicit rejection of equity-shaped fields — no `economic_role`/`capital_priority`, no financial-statement metrics, no `TIER-0002`-style cluster/issuer-look-through `risk_concentration` (no such mechanism covers crypto today) | `XASSET-0002` supporting artifact §4.2 |
| Method: narrative-judgment axes (`network_fundamentals`, `economic_model`, `liquidity_and_market_structure`, `custody_and_counterparty_risk`, `regulatory_and_structural_uncertainty`) kept separate from the one mechanically-computed axis (`correlation_and_volatility`); no standalone "uncertainty axis" — `evidence_quality` is the one axis that summarizes uncertainty | `XASSET-0002` supporting artifact §2, §4.3 |
| Permitted inputs / forbidden answer-key inputs — the protocol's own published technical/tokenomics/staking documentation; publicly available on-chain and market-data metrics from a reputable source; the account's own actual, factual custody arrangement (Robinhood custody, per CLAUDE.md's Portfolio Doctrine); currently-disclosed, citable regulatory matters only. `targets.yaml`'s existing row permitted only for symbol identity, **never** for `target_pct`. `holdings.yaml`'s `crypto_shares:` quantities, current crypto sleeve sizing doctrine, conviction-sizing policy, historical trading commentary, chart signals, and valuation output must never be consumed as classification evidence — population identity may be verified from `targets.yaml`/the contender registry only. No chart-domain content in any form. No `conviction`/`portfolio_role_ref`-style policy language of any kind | `XASSET-0002` supporting artifact §4.3 (per-axis evidence-input and prohibited-inference statements), §6.2; this filing's own §D |
| Judgment-before-mechanical-rollup sequencing — the five narrative axes drafted before `correlation_and_volatility` (mechanical) is computed, mirroring `TIER-0002`'s and the ETF framework's identical judgment-before-computation sequencing | `XASSET-0002` supporting artifact §2, §4.3 |
| Abstention discipline — two genuinely distinct semantics (`not_applicable` for a structurally absent mechanism, e.g. BTC's absent staking/fee-accrual; `unable_to_determine`, always with a required `abstention_reason`, for a genuine evidence gap); abstention does not cascade between axes | `XASSET-0002` supporting artifact §4.3, §4.4 |
| `correlation_and_volatility` — **mechanical only, no new correlation study or numeric coefficient computed by this authorization or its implementation.** `cross_coin_correlation_status` retains its governed default/abstention value, `not_yet_measured`, for all three coins unless a separately-authorized future correlation study already exists to cross-reference by pointer — no coefficient is ever duplicated or restated in this schema. `historical_volatility_category` is the one field a future implementation may populate from historical price data directly (closed vocabulary: `high_volatility` \| `extreme_volatility` \| `unable_to_determine` — no `low_volatility` value exists in the schema) | `XASSET-0002` supporting artifact §4.3 ("This design does not authorize computing a new correlation study"); this filing's own §E |
| `regulatory_and_structural_uncertainty` — currently-disclosed, citable matters only; `none_currently_disclosed` is the honest default, not an abstention; **no predictive regulatory or legal forecast of any kind**, matching CLAUDE.md's own standing "No predictive research" guardrail | `XASSET-0002` supporting artifact §4.3 |
| Shared cross-asset-handoff envelope (`instrument_id`, `asset_type: cryptocurrency`, `schema_version`, `provenance`, `evidence_quality_status`, `uncertainty_summary`, `structural_risk_flags`, `record_status`, `valuation_and_economic_assessment_readiness`, `cross_asset_handoff`, `abstention_index`) — every summary field a read-only copy of an already-computed axis value, never independently computed | `XASSET-0002` supporting artifact §6.1, §6.2, §6.4 |
| `valuation_and_economic_assessment_readiness.status` forced to exactly one value, `valuation_required`, on all three records, zero exception — no fair value, expected return, target price, `target_pct`, target range, maximum position size, score, or rank anywhere | `XASSET-0002` supporting artifact §6.3 |
| Numeric-field boundary — neither framework defines a numeric field for crypto analogous to the ETF's `expense_ratio_pct`; no numeric field of any kind is authorized on any crypto axis | `XASSET-0002` supporting artifact §4.3, §6.1 |
| No technical redaction/sanitization pipeline — `XASSET-0002`'s own Rationale determined `TIER-0004`'s file-level redaction-and-reseal apparatus does not transfer, because no crypto Intelligence record exists today and none of the framework's evidence sources embed portfolio-policy text; population identity may be read from `targets.yaml`/the contender registry, but no new technical contamination-control pipeline is required or authorized beyond the plain evidentiary discipline in §D below | `XASSET-0002`'s Rationale ("Why contamination controls are re-derived, not copied from `TIER-0004`") |
| Validator specification (13 points: exact population enforcement, closed schema at every level with extra-key rejection, asset-type separation, no ETF/equity-field leakage, no numeric score/rank/target leakage, independent chart-terminology scan, evidence/provenance validation, abstention requirements including the `not_applicable`-versus-`unable_to_determine` distinction and the closed list of axes that genuinely support `not_applicable`, deterministic generation, protected-path isolation, allocator/margin import decoupling, cross-asset policy non-implication) | `XASSET-0002` supporting artifact §8 |
| Test specification (~24-item inventory: happy-path, malformed top-level/instrument, extra/missing keys at every level, wrong `asset_type`, cross-contamination in both directions — a crypto record carrying an ETF-only field, and vice versa — forbidden equity-field leakage, invalid evidence citation, abstention behavior including the two-semantics distinction, duplicate/missing/extra instrument against the named 3-coin population, numeric/score/rank leakage, chart-terminology leakage per term, directive-language leakage, forced-`valuation_required` violation, envelope-projection-mismatch rejection, determinism, protected-path isolation, allocator/margin import-coupling isolation), including §9.1's three explicitly carried-forward lessons (extra-key rejection, independent-mechanism verification, no self-declared-flag-without-independent-scan) | `XASSET-0002` supporting artifact §9, §9.1 |
| Batching/future-lifecycle rules — design never recombined with content; ETF and crypto content never share one filing; a schema revision, if ever needed, is its own future, separately authorized design-amendment unit | `XASSET-0002` supporting artifact §7 |

Nothing in this table is amended, expanded, or narrowed by this filing. Any future session finding a
genuine ambiguity or gap in `XASSET-0002`'s specification must return for its own separate governance
correction — not resolve it unilaterally inside the implementation PR. This includes the
`not_yet_measured`-versus-formal-abstention ambiguity `PR #270`'s own review chain (MINOR-3) found and
deliberately left open in `XASSET-0002`'s text for the ETF `tracking_quality_category` field — a
structurally identical ambiguity may arise for crypto's own `historical_volatility_category` or
`cross_coin_correlation_status` fields, and the same discipline applies: disclose and pin with a test,
never silently resolve.

### C. Evidence standard (binding on the future implementation)

The implementing session must use only appropriate crypto-classification evidence:

- **Preferred**: the protocol's own official reference/technical documentation (consensus mechanism,
  network security model, tokenomics, staking mechanism where one exists); official foundation or
  core-development team documentation where applicable; authoritative on-chain/network data sources
  (active addresses, transaction throughput, validator/miner count, developer-activity indicators);
  reputable market-data sources for trading-volume, order-book-depth, and exchange-listing-breadth
  evidence; the account's own actual, factual custody arrangement (Robinhood custody, already disclosed
  in CLAUDE.md's Portfolio Doctrine) as a non-speculative structural input; authoritative, currently-in-
  force or currently-pending regulatory disclosures where relevant, each cited.
- **Secondary sources** may be used only under the same honest provenance/access-status discipline
  `PR #270`'s ETF records already established — every source cited with `source_type`
  (primary/secondary), `access_status` (e.g. `attempted_not_directly_inspected` for a blocked primary
  domain, `consulted_via_search_aggregation` for actual cited secondary content), and, where available, an
  as-of/publication date. No secondary aggregation may be silently upgraded to primary-source
  verification.

No evidence may be invented, assumed by analogy from another coin, or backfilled from a company's own
Company Intelligence record. Genuine conflicts across sources (the exact class `PR #270`'s VWO
China-weight finding demonstrated for ETFs) must be disclosed, never silently averaged or resolved. Where
evidence is insufficient for a given axis, the implementation must use the framework's own abstention path
(§B) rather than filling the gap. If the implementing session determines that gathering adequate primary
evidence requires research authority beyond what this filing and `XASSET-0002` already grant, it must
stop and disclose that as a genuine blocker rather than substitute secondary inference for a primary
source without disclosure. This filing gathers no evidence itself.

### D. Blindness / contamination boundary (binding on the future implementation)

Classification judgment on `network_fundamentals`, `economic_model`, `liquidity_and_market_structure`,
`custody_and_counterparty_risk`, and `regulatory_and_structural_uncertainty` must not consume, as
evidence, any of: `holdings.yaml`'s `crypto_shares:` quantities; `targets.yaml`'s `target_pct` values for
BTC/ETH/SOL; CLAUDE.md's crypto sleeve sizing doctrine (the 10% conviction-sizing target, the BTC-reserve
rebuild instruction, or any related sleeve-composition commentary); conviction-sizing policy of any kind;
historical trading or execution commentary; chart signals of any kind; or any valuation output. Population
identity — confirming exactly `BTC`/`ETH`/`SOL` and excluding `ZORA`/`WIF`/`BONK`/`PEPE`/`HYPE` — may be
verified from `targets.yaml`'s `destination:` list and the contender registry only, matching `XASSET-0003`
§B's identical treatment of `targets.yaml` for the ETF sleeve ("permitted only for symbol identity, never
for `target_pct`"). No new technical redaction pipeline is required or authorized (§B) — this is a
plain evidentiary-discipline boundary, the same shape as the one `XASSET-0003`/`PR #270` already applied
successfully to the ETF sleeve without any redaction apparatus, since no crypto Intelligence record exists
today to leak policy content the way a Company Intelligence record could.

### E. Correlation/volatility boundary (binding on the future implementation)

**This filing does not authorize a new correlation study, a numeric correlation coefficient computation,
or any market-data expansion beyond §C's evidence standard.** `correlation_and_volatility.
cross_coin_correlation_status` must retain its governed default value, `not_yet_measured`, for all three
records unless a separately-authorized future correlation study already exists to cross-reference by
pointer — `XASSET-0002`'s own supporting artifact §4.3 is explicit and controlling on this point ("This
design does not authorize computing a new correlation study ... a coefficient, if one is ever computed
under a separately-authorized future study, is cross-referenced by pointer, never duplicated or restated
here"). `historical_volatility_category` (`high_volatility` \| `extreme_volatility` \|
`unable_to_determine`) may be populated from ordinary historical price-data evidence under §C, since it is
a categorical fact about the coin's own price history, not a cross-coin statistical study. No hidden
market-data expansion of any kind is authorized.

### F. Valuation boundary (binding on the future implementation)

`valuation_and_economic_assessment_readiness.status` must be forced to exactly `valuation_required` on
all three records, zero exception. No fair value, expected return, target price, `target_pct`, target
range, maximum position size, score, rank, or buy/add/hold/trim/exit recommendation of any kind may appear
anywhere in any record — the direct crypto analogue of `TIER-0009`'s forced equity `valuation_required`
design and `XASSET-0003`'s identical ETF-sleeve boundary, already proven correct and unweakened by
`PR #270`'s independent review.

### G. Validator/test authority (binding on the future implementation)

The future implementation may build exactly one crypto classification validator and its dedicated test
suite implementing `XASSET-0002`'s specification (§B above), covering at minimum: exact `BTC`/`ETH`/`SOL`
population enforcement; closed schemas at every level (envelope, axis, provenance-source, manifest-row)
with extra-key rejection, not merely missing-key rejection (the exact `contender_registry_validator.py`
exploit class `XASSET-0002` §9.1 names, and the exact defect `PR #270`'s own MINOR-1 finding demonstrated
still needs deliberate, independent enforcement even under an already-accepted specification); asset-type
separation (`asset_type: cryptocurrency`, never mixed with `etf` or an equity); rejection of any ETF-only
field (`structural_role`, `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`,
`structure_and_methodology`) on a crypto record, and rejection of any crypto-only field on an ETF or
equity record; rejection of any `TIER-0002`-shaped equity field (`economic_role`, `capital_priority`,
`risk_concentration`) anywhere in the document tree; rejection of any numeric target/score/rank leakage
(`target_pct`, `target_range`, `max_position_size`, `score`, `rank`, `conviction_score`,
`recommended_target_pct`); an independent, free-text chart-terminology scan (the same sixteen terms
`XASSET-0002` §8 point 7 and `PR #270`'s own validator already enumerate), built in from the start, not
deferred; an independent, word-boundary-matched directive/recommendation-language scan, learning directly
from `PR #270`'s own MINOR-2 finding (a scan mechanism existing without dedicated tests is a coverage gap,
not a defect, but must not be repeated here — dedicated tests for each forbidden pattern are required from
the start); provenance/access-status validation on every source entry; `not_applicable`-versus-
`unable_to_determine` semantics validated against the closed, per-axis list of which state each axis
genuinely supports (§B); `correlation_and_volatility.cross_coin_correlation_status` validated against its
`not_yet_measured` default per §E, with no coefficient field to leak; the forced `valuation_required`
check per §F; manifest/hash reconciliation (mirroring `PR #270`'s `COHORT_MANIFEST.yaml` design);
cross-asset-envelope read-only-projection consistency (every summary field checked against its source
axis field, never independently computed); deterministic generation; protected-path isolation, explicitly
including `intelligence/etf_classification/` and its `COHORT_MANIFEST.yaml` (the four ETF records `PR
#270` sealed must remain byte-identical); and zero import coupling with `allocate.py`/`margin_state.py`.
Also required, learning directly from `PR #270`'s own MINOR-3 finding: any `abstention_index`
completeness check the implementation builds must not silently resolve the `not_yet_measured`-versus-
formal-abstention ambiguity noted in §B — if a crypto-specific analogue of that ambiguity arises (e.g. for
`historical_volatility_category` or a `not_yet_measured`-shaped value elsewhere), it must be disclosed and
pinned by a dedicated test, exactly as `PR #270`'s own corrected validator did for the ETF sleeve, never
decided unilaterally inside the implementation PR.

### H. Stop conditions (binding on the future implementation)

The implementation PR must stop immediately and disclose, never silently work around: population drift (a
fourth coin appearing in `targets.yaml`, or one of the three disappearing, since the implementation may
begin some time after this filing merges); any equity-field leakage (`economic_role`, `capital_priority`,
`risk_concentration`, or any `TIER-0002`-shaped field name); any ETF-field leakage on a crypto record;
any numeric score/rank/target leakage; any chart-domain leakage; any attempt to compute a new correlation
coefficient or conduct a new correlation study; any attempt to depart from the forced `valuation_required`
state; any consumption of `holdings.yaml` quantities, `target_pct` values, sleeve sizing doctrine, or
conviction policy as classification evidence (§D); any protected-path mutation (including any edit to the
four sealed ETF records or `COHORT_MANIFEST.yaml`); or any unexpected target, holdings, gate, cap,
cluster, allocator, margin, ladder, order, or trade change.

### I. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **One new additive gate, `xasset0003-implementation-post-merge-verification`**, recording `PR #270`'s
   confirmed merge (`7441c274f4bfea29da493dc7cfe99373e5f12b17`), full review chain (two rounds, one
   bounded correction resolving 3 MINOR findings, zero unresolved findings at the corrected head),
   principal acceptance, merge-commit CI success, and exact 10-file scope — matching the identical Lane M
   pattern `XASSET-0002`/`XASSET-0003` each applied to their own immediately-preceding merged PR. The
   `xasset0003-etf-classification-implementation` gate's own historical text is left unedited.
2. **`active_pr` updated `270` → this filing's own PR number**, and **`last_verified_main_sha` updated**
   `e764c1b6cb1d12c5a6aed73b0204e09b62c13309` → `7441c274f4bfea29da493dc7cfe99373e5f12b17`.
   `last_verified_date` updated to this filing's own date.
3. **One new additive gate, `xasset0004-crypto-classification-content-authorization`**, recording this
   filing's own branch and (once it exists) PR number — `status: in_progress`, **not** `status:
   complete`, since this filing's own governance PR is itself unmerged, unreviewed, and unaccepted,
   matching every prior filing's identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: step 4 (ETF classification content) is
   complete and merged (`PR #270`); this filing, once merged, authorizes exactly one future crypto
   classification content implementation PR (step 5 of the `§J` roadmap / item 7 of the `§I` list); steps
   6 through 12 remain wholly unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`) is
changed — this filing does not begin execution and does not alter the workstream's own standing.

### J. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder
change; any trade or order; any chart use of any kind; any buy or sell recommendation; any deployment
recommendation; ETF classification content, edit, or re-classification of any kind (`SPY`/`VEA`/`VWO`/
`GLD` unaffected); any valuation or economic-assessment methodology; any cash/reserve/GLD/debt functional
doctrine; any cross-asset overlap, concentration, or opportunity-cost synthesis; any sleeve-level or
instrument-level sizing; classification of any coin by this filing itself; gathering of any crypto
evidence by this filing itself; a new correlation study or numeric coefficient of any kind (§E);
creation of `intelligence/crypto_classification/` or any file inside it; any validator implementation; or
any edit to `XASSET-0001`, `XASSET-0002`, `XASSET-0003`, or their own text.

### K. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index row);
(3) `operations/WORKSTREAMS.yaml` (`WS-0014` only — the §I updates); (4) `CLAUDE.md` (one concise
Decisions Log pointer entry); (5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded
decision-catalog-count assertions, made stale by this filing's own new row). No supporting audit artifact
is created — `XASSET-0002`'s own supporting artifact already contains the complete accepted crypto
process specification (population-scale contamination analysis, validator specification, test
specification), and restating it in a second retained document would duplicate content rather than add
evidence, matching `XASSET-0003`'s own identical determination. No `intelligence/` company, theme,
relationship, classification, reconciliation, recommendation, contender, or ETF-classification file; no
`targets.yaml`/`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`; and no production allocator/margin
code is touched.

### L. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This session does not
review its own work, mark it ready, merge it, or post principal acceptance. Nothing in this decision
becomes effective until this governance PR merges to `main` — including the authorization in §A, which
the future implementation session may not rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `XASSET-0002` already carries a complete,
independently reviewed, principal-accepted, merged specification for every schema, evidence, sequencing,
and validator control crypto classification needs. Re-deriving or rephrasing that content here would
introduce exactly the drift risk `XASSET-0002`'s own two MAJOR findings (during its own review) and
`PR #270`'s own three MINOR findings demonstrated a plausible-sounding restatement or an under-specified
independent check can carry — the smaller and more reliable move is to bind the future implementation to
`XASSET-0002`'s own text by reference, unchanged, exactly as `XASSET-0003` already did successfully for
the ETF sleeve.

**Why implementation is not folded into this same filing.** `XASSET-0002`'s own "Numbering note" and its
supporting artifact §7 are explicit and unambiguous that crypto classification content requires its own
separate authorization and its own separate implementation lifecycle, and that ETF and crypto content must
never share a filing — this is controlling text this filing has no discretion to reinterpret. This also
matches this repository's general pattern for a framework's first-ever content application per asset type
(`TIER-0004`→`TIER-0005`→separate Milestone 6 implementation; `XASSET-0002`→`XASSET-0003`→separate `PR
#270`) over the smaller combined-filing pattern used for incremental content batches under an
already-precedented framework (`REL-0002`, `PI-0036`) — crypto classification is the second-ever
application of the newly-accepted framework (after ETFs), and a genuinely distinct asset type from ETFs,
not an incremental batch under an already-proven crypto-specific pipeline.

**Why the population is bounded to exactly three instruments with no per-instrument PR structure.**
`targets.yaml`'s `destination:` list names exactly three crypto rows today, matching `holdings.yaml`'s
`crypto_shares:` block exactly; `XASSET-0002`'s own Rationale already determined multi-shard isolation
unnecessary at this scale (crypto = 3, ETF ≤ 4, both far below equity Milestone 6's 27-name/five-shard
design). This filing makes that determination binding rather than re-litigating it, while requiring the
implementing session to reconfirm it if the population has grown by the time implementation begins (§A
point 2) — the same forward-looking discipline `XASSET-0003` applied to its own binding-by-reference
table.

**Why the correlation/volatility boundary is stated explicitly rather than left implicit.**
`XASSET-0002`'s supporting artifact §4.3 already prohibits a new correlation study, but this filing states
it as its own binding §E rather than relying on the reader to infer it purely from the referenced table —
matching this repository's own repeated correction history around under-stated scope boundaries
(`XASSET-0002`'s own MAJOR finding on roadmap-numbering ambiguity, and `XASSET-0003`'s explicit
crypto-exclusion statement in its §A/§G, are the most recent direct precedents for why an explicit
sentence is worth stating even when the underlying rule already exists elsewhere).

**Why the blindness/contamination boundary is stated explicitly as its own §D, distinct from the evidence
standard.** `XASSET-0002`'s Rationale already determines that no new technical redaction pipeline is
required, but that determination concerns *mechanism* (no file-level redaction apparatus is needed because
no crypto Intelligence record exists to leak policy content). It does not, by itself, state which specific
repository facts (holdings quantities, sleeve sizing doctrine, conviction policy) must not be consumed as
evidence even in the absence of a redaction pipeline — a plain evidentiary-discipline rule, not a
technical-control rule. Stating it as its own bound section, rather than folding it into §C, keeps the
"what evidence is permitted" question (§C) separate from the "what must never be consumed regardless of
technical safeguards" question (§D), mirroring `TIER-0004`'s own distinction between evidence-standard and
contamination-control sections for the equity sleeve.

**Why no new supporting audit artifact.** Every fact this filing needs — the accepted crypto schema,
evidence standard, sequencing, correlation/volatility boundary, envelope design, and validator/test
specification — already exists in `XASSET-0002`'s merged, reviewed text and its supporting artifact.
Creating a second retained document that restates the same content would violate this repository's own
"reference, don't restate" discipline (`REL-0001`, `PI-0016`, `TIER-0005`, `XASSET-0003`) without adding
verifiable evidence.

## Alternatives Considered

- **Combine this authorization with crypto classification content in one PR**, matching several smaller
  Company Intelligence batches' combined-filing precedent (`REL-0002`, `PI-0036`, `PI-0038`). Rejected —
  `XASSET-0002`'s own "Numbering note" and its supporting artifact §7 explicitly prohibit combining
  design/authorization with content for either asset type; this is controlling text, not a discretionary
  style choice, and `XASSET-0003` already established the same separation for ETFs.
- **Redesign or restate `XASSET-0002`'s crypto specification in this filing's own words**, on the theory
  that a content authorization should be self-contained. Rejected — see Rationale; restatement itself
  introduces drift risk the binding-by-reference table (§B) avoids, and both `XASSET-0002`'s own review
  history and `PR #270`'s own review history demonstrate this is not a hypothetical risk.
- **Authorize a partial crypto population first (e.g., BTC only) as a smaller first batch**, mirroring
  early Company Intelligence research waves. Rejected — crypto classification is not open-ended new-coin
  research; it applies one already-frozen framework to an already-fully-covered, already-small population
  (three instruments) under one already-specified mechanism, so the proportionality concern that justified
  smaller research waves for open-ended ticker discovery does not carry over the same way; `XASSET-0002`'s
  own Rationale already determined a single pass across all three coins is appropriate at this scale, and
  `XASSET-0003`/`PR #270` already validated the identical reasoning for four ETFs.
- **Authorize a new correlation study alongside this content authorization**, since crypto correlation is
  a natural next question once the coins are classified. Rejected outright — `XASSET-0002`'s own
  supporting artifact §4.3 is explicit that no new correlation study is authorized by the framework design
  itself, and this filing has no independent authority to expand that boundary; any future correlation
  study requires its own separate, future, explicit governance decision, matching `REL-0001`'s own
  structural-versus-measured-correlation separation.
- **Create a retained audit artifact restating `XASSET-0002`'s crypto process specification for this
  filing's own supporting evidence.** Rejected — `XASSET-0002` and its supporting artifact are themselves
  the retained, accepted specification; a second document repeating it would be redundant, not additive.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded crypto
classification implementation PR covering all three canonical crypto destinations (`BTC`, `ETH`, `SOL`),
bound exactly to `XASSET-0002`'s specification per §A–H above, gated on its own full
independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle; the
`xasset0003-implementation-post-merge-verification` gate recording `PR #270`'s confirmed state; the
`xasset0004-crypto-classification-content-authorization` gate transitioning to `status: in_progress`
recording this filing as underway; `WS-0014`'s `active_pr`/`last_verified_main_sha` synchronization.

**Not authorized by this filing, now or ever without a further separate decision:** ETF classification
content, edit, or re-classification of any kind; a new correlation study or numeric coefficient of any
kind; classification of any coin by this filing itself; gathering of any crypto evidence by this filing
itself; any validator implementation; any edit to `XASSET-0001`, `XASSET-0002`, `XASSET-0003`, or their own
text; any valuation or economic-assessment methodology; any cash/reserve/GLD/debt functional doctrine; any
cross-asset overlap, concentration, or opportunity-cost synthesis; any sleeve-level or instrument-level
sizing; and any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/trade/brokerage/order
change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification Intelligence record, byte-for-byte; the contender registry;
`XASSET-0001`'s, `XASSET-0002`'s, and `XASSET-0003`'s own accepted text and scope, in full, unedited;
`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`,
`margin_state.py`; the Constitution; `WS-0005`'s completed, `status: complete` state; `WS-0014`'s own
`status: proposed`/`priority: secondary` (unedited by this filing).

This decision becomes effective only when its implementing pull request merges to `main`.
