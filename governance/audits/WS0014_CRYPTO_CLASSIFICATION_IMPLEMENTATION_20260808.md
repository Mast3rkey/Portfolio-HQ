# WS-0014 Crypto Classification Implementation — retained artifact

**Filed under**: `XASSET-0004` (`governance/decisions/XASSET-0004-ws0014-crypto-classification-content-authorization.md`)
**Date**: 2026-08-08
**Scope**: `XASSET-0004` §A — the one future, separate, bounded crypto classification (blind-classification
content) implementation PR it authorized, covering all three canonical crypto destinations (BTC, ETH, SOL)
under `XASSET-0002`'s already-accepted crypto framework. This artifact is the retained narrative record of
that implementation, matching the `XASSET-0003`→`PR #270`→`WS0014_ETF_CLASSIFICATION_IMPLEMENTATION_20260807.md`
precedent.

---

## 1. Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/btc-eth-sol-classification-snl488` (the pre-designated branch for this session, per the task's own
  Git Development Branch Requirements — not a freshly-created branch, since the branch already existed and
  already matched `origin/main` exactly), working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD`, `origin/main`, and GitHub `main` all identical at
  `7b9af50af001ed0db5933a6d65b18b19f9952ffc` — `PR #271`'s own merge commit (`XASSET-0004`).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #271` (`XASSET-0004`) independently re-confirmed in full**: accepted head
  `8341b428c51b9a83878ec3ab81bdf5a613945b20`, independent exact-head review (`pullrequestreview-4887313482`),
  principal acceptance (`issuecomment-5223248900`), merge (merge commit
  `7b9af50af001ed0db5933a6d65b18b19f9952ffc`), merge-commit CI (workflow run `31227835940`, job
  `93025582179`, `status: completed` / `conclusion: success`).
- **`XASSET-0002` (plus its supporting artifact) and `XASSET-0004` read in full this session** — not
  summarized from memory. `XASSET-0002`'s supporting artifact §4 (crypto framework field-by-field design),
  §6 (shared envelope), §8 (validator specification), and §9 (test specification) are the controlling text
  this implementation binds to, per `XASSET-0004` §B's binding-by-reference table.
- **`targets.yaml` independently re-read**: exactly three `asset_class: crypto` rows in `destination:` —
  `BTC` (2.00%), `ETH` (1.50%), `SOL` (0.50%) — zero drift from `XASSET-0004`'s own stated population.
- **`holdings.yaml` independently re-read**: `crypto_shares:` carries exactly `BTC`, `ETH`, `SOL` — no
  fourth coin.
- **`intelligence/contenders/registry.yaml` independently re-read**: `BTC`, `ETH`, `SOL` each carry
  `asset_type: crypto`, `primary_disposition: requires_research`, `classification_exists: false` prior to
  this implementation; `ZORA`, `WIF`, `BONK`, `PEPE`, and `HYPE` each carry
  `primary_disposition: explicitly_deferred_or_excluded` and are confirmed absent from both `targets.yaml`
  and `holdings.yaml`.
- **No `intelligence/crypto_classification/` directory, no crypto classification content of any kind**,
  independently reconfirmed absent from the repository before this implementation's first write.
- **`etf_classification_validator.py` and one ETF record (`SPY.yaml`, `GLD.yaml`) read in full this session**
  as the direct structural precedent for storage convention, sealing mechanics, hashing, and manifest
  reconciliation — `XASSET-0004` §A.4 leaves the choice of shared-helper reuse versus a fresh, dedicated
  validator to the implementing session; this implementation builds a fresh, dedicated
  `crypto_classification_validator.py` (duplication over a shared-helper module — see §5 below for the
  reasoning, matching this repository's own "each Intelligence schema owns its own validator" convention).
- **Decision catalog independently rebuilt**: 93 decisions, `issues == ()` at the starting head — no new
  governance decision is authorized or filed by this implementation (`XASSET-0004` §J: "creation of
  `intelligence/crypto_classification/` or any file inside it" requires no new decision, per the
  `TIER-0005`→Milestone-6-implementation and `XASSET-0003`→`PR #270` precedent).

No condition met a Stop bar (`XASSET-0004` §H). This implementation proceeded.

## 2. Evidence-gathering methodology

Every primary protocol-documentation source attempted was blocked by this environment's network egress
policy, matching this repository's own extensively disclosed prior access-failure pattern (the identical
finding `PR #270`'s ETF implementation recorded for `www.ssga.com`/`www.sec.gov`/`www.spdrgoldshares.com`):

| Domain attempted | Result |
|---|---|
| `bitcoin.org` | `EGRESS_BLOCKED` |
| `ethereum.org` | `EGRESS_BLOCKED` |
| `solana.com` | `EGRESS_BLOCKED` |
| `www.coingecko.com` | `EGRESS_BLOCKED` |

All substantive evidence was therefore gathered via `WebSearch` aggregation — every `provenance.sources`
entry discloses this honestly (`source_type: secondary`, `access_status: consulted_via_search_aggregation`
for actual cited content; `source_type: primary`, `access_status: attempted_not_directly_inspected` for the
four blocked domains above, each with a `limitation` field naming the specific block). One genuine primary
source *was* directly inspected per coin: `CLAUDE.md`'s own Portfolio Doctrine section, cited as the source
for each record's `custody_and_counterparty_risk.custody_model: exchange_custodied` fact — `XASSET-0004`
§C explicitly names "the account's own actual, factual custody arrangement (Robinhood custody, per
CLAUDE.md's Portfolio Doctrine)" as a permitted, non-speculative structural input, and this implementation
cites it as `access_status: directly_inspected` since the file was read directly in-session, not
search-aggregated.

Roughly a dozen targeted `WebSearch` queries were run across the three coins, covering: consensus mechanism
and network security (BTC); active-address/adoption trend (BTC); market capitalization, trading volume, and
exchange-listing breadth (all three); SEC/CFTC regulatory classification (all three, converging on one
shared 2026-03-17 finding); Bitcoin's 21-million supply cap and halving schedule; Bitcoin Script's
non-Turing-complete design versus Ethereum's EVM; EIP-1559 fee burn and Ethereum's supply dynamics; Ethereum
staking yield, validator count, and Lido liquid-staking/smart-contract-risk profile; Ethereum DeFi TVL and
DEX volume; Solana's Proof of History / Tower BFT consensus design and the pending Alpenglow upgrade;
Solana's inflation schedule, staking yield, and fee-burn mechanism (including the disclosed pending SIMD-0550/
SIMD-0553 governance proposals); Solana market capitalization, trading volume, and the disclosed DEX-volume
dispersion; and Solana daily-active-user/TPS network-usage trends.

Two genuine cross-source numeric ranges were disclosed rather than collapsed to a single false-precision
figure: Ethereum's staking APY/validator-count/staked-percentage figures (which vary modestly by measurement
date and data provider) and Solana's market-capitalization/trading-volume figures (same). One genuine,
disclosed tension in the underlying evidence, not smoothed over: Bitcoin's hash rate reached an all-time
high (>1 exahash/second) in mid-2026 while active-address counts were separately reported at year lows —
recorded as `declining_or_stagnant_usage` on the specific `adoption_trend_category` vocabulary (a
usage/adoption axis, not a network-security axis), with the divergence disclosed in full in both the
per-record `uncertainty_summary` and its `cross_asset_handoff` projection.

## 3. Blindness / contamination boundary confirmed observed

Per `XASSET-0004` §D, no record's judgment axes (`network_fundamentals`, `economic_model`,
`liquidity_and_market_structure`, `custody_and_counterparty_risk`, `regulatory_and_structural_uncertainty`)
consumed `holdings.yaml`'s `crypto_shares:` quantities, `targets.yaml`'s `target_pct` values, CLAUDE.md's
crypto sleeve sizing doctrine (the 10% conviction-sizing target, the BTC-reserve rebuild instruction, or any
related sleeve-composition commentary), conviction-sizing policy of any kind, historical trading or
execution commentary, chart signals, or valuation output — independently confirmed via a full re-read of
all three sealed records and a repository-wide grep for `target_pct`/`conviction`/`portfolio_role_ref`
inside `intelligence/crypto_classification/`, zero matches. Population identity (`BTC`/`ETH`/`SOL`, excluding
`ZORA`/`WIF`/`BONK`/`PEPE`/`HYPE`) was verified from `targets.yaml`'s `destination:` list and the contender
registry only, per `XASSET-0004` §D's explicit permission.

## 4. Correlation/volatility and valuation boundaries confirmed observed

Per `XASSET-0004` §E, no new correlation study, numeric coefficient computation, or market-data expansion
beyond §C's evidence standard was performed. All three records carry
`correlation_and_volatility.cross_coin_correlation_status: not_yet_measured`, the one governed default value
this implementation is authorized to use — independently re-verified via `crypto_classification_validator.py`'s
own dedicated forced-value check (`_FORCED_CORRELATION_STATUS`), which rejects the schema's second closed-
vocabulary value (`measured_elsewhere_cross_reference_required`) outright at this implementation, since no
separately-authorized correlation study exists yet to reference. No numeric correlation coefficient field
exists anywhere in the schema or in any of the three records. `historical_volatility_category` was populated
from ordinary historical price-data evidence under §C (a categorical fact about each coin's own price
history, explicitly distinct from a cross-coin statistical study per §E) — `high_volatility` for BTC and
ETH, `extreme_volatility` for SOL, reflecting SOL's own disclosed May-2026 82% two-week DEX-volume swing and
its narrower, shorter-established liquidity profile relative to BTC/ETH.

Per `XASSET-0004` §F, `valuation_and_economic_assessment_readiness.status: valuation_required` is forced on
all three records, zero exception — independently re-verified via a dedicated validator test
(`test_valuation_status_forced_value_violation_rejected` and the real-repository
`test_real_repository_valuation_forced_default` test). No fair value, expected return, target price,
`target_pct`, target range, maximum position size, score, rank, or buy/add/hold/trim/exit recommendation of
any kind appears anywhere in any record.

## 5. Why a fresh, dedicated validator rather than reusing `etf_classification_validator.py`'s helpers

`XASSET-0004` §A.4 explicitly leaves this determination to the implementing session ("that determination
belongs to the implementing session, not to this filing"). This implementation builds
`crypto_classification_validator.py` as a fully independent module, importing nothing from
`etf_classification_validator.py`, for the same reason this repository's existing Intelligence validators
(`classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`,
`relationship_validator.py`, `contender_registry_validator.py`, `etf_classification_validator.py` itself)
each own their own schema logic rather than sharing a generic base: the two schemas' closed-key sets, axis
names, and forbidden-leakage lists are asset-type-specific enough (six axis names differ entirely between
the two frameworks; the crypto schema authorizes zero numeric fields where the ETF schema authorizes
exactly one) that a shared-helper module would itself need asset-type parameterization, and the resulting
indirection would be harder to audit than two structurally-similar-but-independent modules. The two
sibling modules' mutual forbidden-key sets are cross-checked for consistency by a dedicated test
(`test_crypto_and_etf_forbidden_leakage_sets_are_complementary`), guarding against silent drift between them
without coupling their import graphs.

## 6. Lessons carried forward from `PR #270`'s own review history, built in from the start

Per `XASSET-0004` §G, three specific defect classes `PR #270`'s own independent-review chain found (and
`etf_classification_validator.py`'s docstring now names as its own v1.1 bounded correction) were built into
this implementation from the start, not discovered the expensive way a second time:

1. **Every required envelope field gets an independent presence/type check.** `structural_risk_flags` is
   checked for its own absence/wrong-type as a dedicated error, separate from the projection-consistency
   comparison against its source axis fields — mirrors the exact fix `etf_classification_validator.py`'s
   v1.1 correction made.
2. **Every forbidden-text pattern has its own dedicated test.** All seven forbidden-recommendation-shaped-
   phrase regexes, all eight directive words, and all seventeen chart-domain terms are each individually
   parametrized in `test_crypto_classification_validator.py` (`test_forbidden_recommendation_shaped_phrase_
   rejected`, `test_directive_word_leakage_rejected`, `test_chart_terminology_leakage_rejected`) — not
   merely an implemented-but-untested scan mechanism.
3. **`abstention_index` is independently cross-checked against every genuine abstention actually present.**
   `_check_abstention_index_completeness` requires every literal `unable_to_determine` value across all six
   axes to have a matching `abstention_index` entry — built in from the start, with a dedicated test
   (`test_abstention_index_missing_entry_for_real_abstention_rejected`) proving it, rather than discovered
   as a post-review correction.

This implementation also discloses, rather than silently resolves, the crypto-specific analogue of the same
`not_yet_measured`-versus-formal-abstention ambiguity `etf_classification_validator.py`'s docstring names for
the ETF sleeve's `tracking_quality_category` field: `correlation_and_volatility.cross_coin_correlation_
status`'s `not_yet_measured` value is treated as a forced, determined default (per §4 above), not an
`abstention_index`-eligible abstention — a dedicated test
(`test_not_yet_measured_is_not_treated_as_an_abstention_index_entry`) pins this behavior explicitly rather
than leaving it to fall out of the implementation incidentally.

Two false-positive risks were found and fixed during drafting, before any validator correction cycle was
needed: the word-boundary directive-word scan (required by `XASSET-0004` §G, mirroring
`recommendation_validator.py`'s design) legitimately caught ordinary English usage of "add" (in "add
implementation detail") and "wait" (in "62-day, 8-hour wait") in early drafts of the BTC/ETH/SOL prose —
resolved by rewriting the prose ("additional implementation detail", "queue delay") rather than weakening
the scan, matching the discipline `XASSET-0003`/`PR #270` established of keeping the validator strict and
adjusting record content instead. Two dedicated regression tests
(`test_directive_scan_does_not_false_positive_on_holdings_noun`,
`test_directive_scan_does_not_false_positive_on_additional_or_waited`) pin this behavior for future
implementations of either schema.

## 7. Per-coin classification results

**BTC**: `network_fundamentals.consensus_mechanism: proof_of_work`,
`adoption_trend_category: declining_or_stagnant_usage` (the disclosed hash-rate-ATH-versus-active-address-
lows tension, §2 above). `economic_model.supply_model: fixed_capped_supply`,
`fee_accrual_applicable: false`, `staking_applicable: false` (Bitcoin has no protocol-level fee accrual to
holders and no native staking — a structural fact, not an evidence gap). `liquidity_and_market_structure.
liquidity_tier: high_liquidity` (~$1.5-1.6T market capitalization, ~40% market dominance, 500+ trading
platforms). `custody_and_counterparty_risk.custody_model: exchange_custodied`,
`smart_contract_risk_category: base_layer_minimal_smart_contract_surface` (Bitcoin Script is deliberately
non-Turing-complete, used chiefly for multisig/timelocks/HTLCs, not a general smart-contract platform).
`correlation_and_volatility.historical_volatility_category: high_volatility`,
`cross_coin_correlation_status: not_yet_measured`. `regulatory_and_structural_uncertainty.
disclosed_regulatory_matter_exists: true`, `structural_uncertainty_category: disclosed_and_unresolved` (the
2026-03-17 SEC/CFTC joint digital-commodity classification, with its own disclosed unresolved CFTC-spot-
market-authority gap). `evidence_quality.primary_source_coverage: partial`.

**ETH**: `network_fundamentals.consensus_mechanism: proof_of_stake`, `adoption_trend_category:
growing_usage` (validator count and staked-ETH climbing steadily; DeFi TVL rising). `economic_model.
supply_model: disinflationary_schedule` (EIP-1559's demand-sensitive base-fee burn against ongoing
validator issuance — net supply direction genuinely varies period to period, disclosed as such rather than
asserted as a fixed schedule like Bitcoin's halving), `fee_accrual_applicable: true` (base-fee burn plus
priority fees/MEV to validators), `staking_applicable: true` (~2.78-3.3% APY across ~897K-1.24M validators).
`liquidity_and_market_structure.liquidity_tier: high_liquidity` (~$229B market capitalization, #2 by market
cap). `custody_and_counterparty_risk.custody_model: exchange_custodied`,
`smart_contract_risk_category: smart_contract_platform_material_surface` (Turing-complete EVM/Solidity,
substantial DeFi ecosystem). `correlation_and_volatility.historical_volatility_category: high_volatility`,
`cross_coin_correlation_status: not_yet_measured`. `regulatory_and_structural_uncertainty.
disclosed_regulatory_matter_exists: true`, `structural_uncertainty_category: disclosed_and_unresolved` (same
2026-03-17 finding, with the staking-specific interpretation directly on-point given ETH's own
`staking_applicable: true`). `evidence_quality.primary_source_coverage: partial`.

**SOL**: `network_fundamentals.consensus_mechanism: other_consensus` (a disclosed drafting judgment — Proof
of History plus Tower BFT proof-of-stake is a materially distinct hybrid design from a "plain"
proof-of-stake network, not a claim any source disputes Solana's proof-of-stake foundation; the pending
Alpenglow upgrade replacing this design entirely is disclosed as a forward-looking architectural fact),
`adoption_trend_category: growing_usage` (daily active users/addresses and transaction throughput at or
near all-time highs). `economic_model.supply_model: disinflationary_schedule` (inflation decreasing 15%
year-over-year toward a 1.5% terminal rate), `fee_accrual_applicable: true` (50% base-fee burn, with two
disclosed pending governance proposals — SIMD-0550/SIMD-0553 — that would materially change the mechanism if
adopted, recorded as pending, not yet adopted), `staking_applicable: true` (~5.5% APY, roughly two-thirds of
supply staked). `liquidity_and_market_structure.liquidity_tier: high_liquidity` (~$41.8-47B market
capitalization, with a disclosed dispersion between overall trading liquidity and a specific meme-coin
venue's DEX-volume swing — a genuine, disclosed nuance, not averaged away). `custody_and_counterparty_risk.
custody_model: exchange_custodied`, `smart_contract_risk_category: smart_contract_platform_material_surface`
(Sealevel/Rust-based smart-contract platform). `correlation_and_volatility.historical_volatility_category:
extreme_volatility` (the DEX-volume swing and SOL's generally higher beta relative to BTC/ETH),
`cross_coin_correlation_status: not_yet_measured`. `regulatory_and_structural_uncertainty.
disclosed_regulatory_matter_exists: true`, `structural_uncertainty_category: disclosed_and_unresolved` (same
2026-03-17 finding, staking interpretation directly on-point). `evidence_quality.primary_source_coverage:
partial`.

## 8. Full validation results

- `crypto_classification_validator.py` `OK (4 result(s))` (three records plus the manifest).
- `classification_validator.py` `OK (28 result(s))`; `reconciliation_validator.py` `OK (27 tickers)`;
  `recommendation_validator.py` `OK (27 tickers)`; `relationship_validator.py` `OK (13 record(s))`;
  `intelligence_validator.py` clean; `freshness_validator.py` `OK`; `contender_registry_validator.py`
  `OK (84 entries)`; `etf_classification_validator.py` `OK (5 result(s))` — all seven pre-existing
  validators unaffected by this implementation.
- `test_crypto_classification_validator.py`: **133 focused tests**, all passing.
- Full repository `pytest` suite: **3332 passed, 0 failed** (3199 pre-existing baseline plus 133 new
  tests), one pre-existing, unrelated `DeprecationWarning` (`intelligence_classification_sanitizer.py`'s
  own `\d`-escape docstring warning, disclosed in this repository's own history since the Milestone 6
  correction chain).
- Decision catalog unchanged at **93 decisions, `issues == ()`** — no new governance decision filed by this
  implementation.
- Repository-wide YAML/YML parsing: 0 errors. Repository-wide JSON parsing: 0 errors.
- `git diff --check`: clean.
- Protected-path scan: zero diff on `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `allocate.py`, `margin_state.py`, `levels.py`, every existing `intelligence/etf_classification/` file,
  every existing `intelligence/classification|companies|themes|relationships|reconciliation|recommendations|
  contenders/` file, and `governance/decisions/`.
- Exactly one `priority: primary` workstream (unaffected — `WS-0005` remains `secondary` per `TIER-0013`;
  `WS-0014` remains `status: proposed`/`priority: secondary`, unedited by this implementation).
- Changed-file inventory: `intelligence/crypto_classification/BTC.yaml`,
  `intelligence/crypto_classification/ETH.yaml`, `intelligence/crypto_classification/SOL.yaml`,
  `intelligence/crypto_classification/COHORT_MANIFEST.yaml`, `crypto_classification_validator.py`,
  `test_crypto_classification_validator.py`, this retained audit, `operations/WORKSTREAMS.yaml`,
  `CLAUDE.md` — nine files, the smallest coherent scope for this implementation.

## 9. What this implementation does not do

No Milestone-7-style completion determination for WS-0014 step 5 is performed or claimed by this filing —
that remains its own separate, later, explicit principal authorization once this implementation merges,
matching the `TIER-0005`→Milestone-6→`TIER-0006` and `XASSET-0003`→`PR #270`→(no completion determination
filed for step 4 as of this implementation's own starting head) precedent. No cash/reserve/GLD/debt
functional doctrine, no cross-asset overlap/concentration/opportunity-cost synthesis, no sleeve-level or
instrument-level sizing, no chart evidence of any kind, and no tier/target/holdings/gate/cap/cluster/
allocator/margin/ladder/order/trade change is authorized, implied, or performed by this implementation.
`WS-0014` items 2 and 6 through 14 remain wholly unauthorized. This session does not review its own PR,
mark it ready, merge it, or post principal acceptance.
