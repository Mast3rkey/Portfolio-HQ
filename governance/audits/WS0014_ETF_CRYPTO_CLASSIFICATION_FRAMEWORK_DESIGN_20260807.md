# WS-0014 ETF + Crypto Classification Framework Design — retained artifact

**Filed under**: `XASSET-0002` (`governance/decisions/XASSET-0002-etf-and-crypto-classification-framework-design.md`)
**Date**: 2026-08-07
**Scope**: `XASSET-0001` §C items 2–3 / §J step 3 — structural design of two asset-appropriate blind-classification
frameworks (ETF, cryptocurrency). Design only. No fund or coin is classified by this artifact.

This artifact is the full field-by-field design. The decision file summarizes it and carries the
authorization/consequences text; this document is the retained detail, matching the
`TIER-0001`→`TIER-0002` supporting-artifact precedent.

---

## 1. Why one artifact covers two frameworks

`XASSET-0001` §J explicitly permits this: "structural ETF + crypto framework **design** (step 3) — both
are schema-design exercises, not content research, and may reasonably batch as one architecture unit even
though the two frameworks differ in content." The same section requires, with equal explicitness, that
**design must never be combined with content** ("step 3 must never be combined with step 4 or step 5")
and that **ETF and crypto classification content must never share a filing** ("different asset types,
different evidence standards, never one filing"). This artifact is design only; it authorizes no future
combining of ETF and crypto *content* into one implementation PR — §7 below restates this as a binding
future-lifecycle rule.

## 2. Method: derive axes from decision usefulness, not from the equity schema

`XASSET-0001` §C is unambiguous: forcing ETF or crypto evidence into `TIER-0002`'s four-axis company
schema (`economic_role`, `capital_priority`, `risk_concentration`, `evidence_quality`) is **explicitly
prohibited**. Neither an ETF nor a coin has an issuer, a competitive position, or earnings to assign a
company-shaped "economic role" or "capital priority" to. This design instead asks, axis by axis, the same
question `TIER-0001`/`TIER-0002` asked for equities: *does this axis exist in currently-authoritative
repository evidence, and does representing it as a standing per-instrument fact materially improve a
future portfolio decision that today requires manual cross-referencing or is not represented at all?*
Candidates that fail this test, or that duplicate another axis's evidence source, are merged or dropped
— every merge and drop is justified explicitly below, not asserted.

Two structural moves carry over from the equity design, because they are general classification-hygiene
principles, not equity-specific content:

- **Narrative-judgment axes are kept separate from mechanically-computed axes.** `TIER-0002` separated
  `economic_role`/`capital_priority` (narrative judgment from evidence) from `risk_concentration`
  (a pure computed rollup of `caps.clusters`/`issuer_lookthrough.yaml`/`intelligence/relationships/`).
  Both frameworks below preserve that separation, because it is what makes the judgment-before-rollup
  sequencing in §6 meaningful.
- **Evidence quality and abstention are per-axis disciplines, not a standalone axis.** `TIER-0002`/
  `TIER-0004` treat "uncertainty/abstention" as a capability every axis carries (a required abstention
  state with a stated reason), not an eighth axis bolted on top. This design does the same — there is no
  separate "uncertainty axis"; `evidence_quality` is the one axis that *summarizes* uncertainty at the
  record level, matching `TIER-0002`'s own precedent exactly.

## 3. ETF framework

### 3.1 Candidate axes evaluated (12 named in the authorizing prompt) → 6 designed axes

| Candidate (as named) | Disposition | Reasoning |
|---|---|---|
| structural role | **Kept** → `structural_role` | No existing mechanism represents "what economic job does this fund do" as a standing fact. |
| underlying exposure / constituent look-through | **Merged** → `constituent_exposure` | |
| geographic exposure | **Merged into `constituent_exposure`** | Geography is a property of *what the fund holds*, the same evidence source (fact sheet / prospectus) as underlying exposure. Splitting it into its own axis fragments one evidence read into two fields with no decision-differentiation benefit — same "smallest structure" test `TIER-0001` applied when it rejected a ninth equity axis. |
| sector exposure | **Merged into `constituent_exposure`** | Same reasoning as geographic exposure — one fact-sheet read, one axis. |
| currency exposure | **Merged into `constituent_exposure`** | Currency exposure is a direct, mechanical consequence of geographic exposure for these instruments (VEA/VWO hold foreign-currency-denominated equities; SPY and GLD are USD); it is recorded as a sub-field, not a fourth top-level axis for the same underlying fact pattern. |
| overlap/concentration | **Kept** → `overlap_and_concentration` | Kept **separate** from `constituent_exposure` deliberately — this axis is a **mechanical rollup** (computed from `issuer_lookthrough.yaml`'s `fund_holding_weight` values plus `intelligence/relationships/`), never a narrative judgment. Mixing it with `constituent_exposure` (narrative/evidence-sourced) would blur the judgment-vs-computation boundary §2 exists to preserve. |
| expense ratio | **Merged** → `cost_and_tracking_quality` | |
| tracking quality | **Merged into `cost_and_tracking_quality`** | Expense ratio and tracking difference/error are both the fund's own disclosed execution-quality facts against its stated benchmark — one evidence source (fund provider's own performance/cost disclosure), one axis. |
| liquidity | **Kept** → `liquidity` | Distinct evidence source (trading volume, bid-ask spread, AUM) and a distinct portfolio-risk question (speed of conversion to cash) from cost/tracking — not merged. |
| fund/index structure and methodology | **Kept** → `structure_and_methodology` | Load-bearing precisely because it is what distinguishes GLD (a physically-backed commodity trust, no index, no equity constituents) from SPY/VEA/VWO (index-replicating equity funds) — collapsing this into another axis would erase the one fact that makes GLD's structural treatment different (see §5). |
| evidence quality | **Kept** → `evidence_quality` | Mirrors `TIER-0002`'s equity axis directly — primary-source-coverage summary plus one required uncertainty statement. |
| uncertainty/abstention | **Not a standalone axis** | Per §2 — each of the six axes above carries its own abstention path (§3.3); there is no separate uncertainty axis, matching `TIER-0002`'s own precedent. |

**Result: 6 ETF axes** — `structural_role`, `constituent_exposure`, `overlap_and_concentration`,
`cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`, plus `evidence_quality` (7 fields
total, one of which — `evidence_quality` — is explicitly the uncertainty-summary axis, not a seventh
independent judgment axis).

### 3.2 Field-by-field design

For every axis: **purpose**, **evidence inputs**, **closed vocabulary**, **abstention state**,
**prohibited inference**, **downstream use**.

#### `structural_role`

- **Purpose**: record what portfolio-economic job this fund does, as a categorical fact — the ETF
  analogue of "why does this instrument exist in the portfolio at all," without assigning it a target
  weight or a buy/sell posture.
- **Evidence inputs**: the fund's own prospectus/fact-sheet stated objective and benchmark; `targets.yaml`'s
  existing row for the fund is permitted **only** for symbol identity (never for `target_pct` — see §6's
  contamination rule).
- **Closed vocabulary** (`role_category`): `broad_market_beta` | `developed_ex_us_equity` |
  `emerging_market_equity` | `precious_metals_or_commodity` | `fixed_income` | `other_structural_role`
  (with a required one-sentence `role_basis` for `other_structural_role`, matching `TIER-0004`'s own
  `abstention_reason`-style discipline for an open-ended catch-all).
- **Abstention state**: `unable_to_determine` (evidence insufficient to categorize) with required
  `abstention_reason`. There is no `not_applicable` state for this axis — every fund has *some* structural
  role by definition; the question is only whether current evidence can name it.
- **Prohibited inference**: no target weight, no "this fund deserves X% of book," no buy/sell/hold
  language, no comparison ranking against another fund's role.
- **Downstream use**: feeds the `role` field of the shared cross-asset handoff envelope (§4); is the
  fact a future cash/reserve/GLD/debt functional-doctrine unit (`XASSET-0001` §D) would read to know
  what kind of fund it is deciding a role for — this axis records *what the fund is*, never *what role
  policy should assign it*.

#### `constituent_exposure`

- **Purpose**: record the fund's aggregate geographic, sector, and currency exposure as disclosed
  structural fact — narrative/evidence-sourced, distinct from the mechanical overlap computation below.
- **Evidence inputs**: the fund provider's own published holdings breakdown (geography, sector, currency);
  `issuer_lookthrough.yaml`'s existing `fund_holding_weight` entries are permitted as a corroborating
  source for the equity-constituent portion specifically (SPY/VEA/VWO only — GLD carries none, see §5).
- **Closed vocabulary**: `geographic_concentration` (`domestic_us` | `developed_ex_us` |
  `emerging_markets` | `mixed_diversified` | `not_applicable`), `sector_concentration` (`broad_diversified`
  | `sector_concentrated` | `not_applicable`), `currency_exposure` (`usd_only` | `foreign_currency_mixed`
  | `not_applicable`).
- **Abstention state**: `not_applicable` is a **genuine, distinct** value here — not a synonym for
  `unable_to_determine`. GLD holds physical gold, not equity constituents, so `sector_concentration` and
  the equity-constituent portion of `geographic_concentration` are `not_applicable` for GLD by structural
  fact, not by evidence gap (see §5). `unable_to_determine` (with `abstention_reason`) is reserved for a
  fund whose exposure genuinely should be knowable but isn't, from current evidence.
- **Prohibited inference**: no derived overlap percentage against any individually-held equity (that is
  `overlap_and_concentration`'s job, computed mechanically, never asserted here).
- **Downstream use**: feeds the structural-risk-flag summary in the cross-asset handoff envelope; is a
  required input to any future geographic/currency-exposure accounting `XASSET-0001` §F names as required
  future work (not performed by this design).

#### `overlap_and_concentration`

- **Purpose**: a **mechanical, computed** rollup — never an asserted judgment — of how much this fund's
  constituents already overlap individually-held equities, reusing the existing measurement
  infrastructure rather than duplicating it. Mirrors `TIER-0002`'s `risk_concentration` design exactly:
  compute from already-authoritative files, assert nothing independently of them.
- **Evidence inputs**: `issuer_lookthrough.yaml`'s `fund_holding_weight` entries (the only currently-live
  ETF-constituent-overlap mechanism in this repository); `intelligence/relationships/` records naming this
  fund, if any exist by the time a future implementation runs (none do today — no relationship record
  currently names an ETF or GLD).
- **Closed vocabulary**: a computed boolean `measured_by_existing_mechanism` (true if `issuer_lookthrough.yaml`
  carries at least one constituent weight for this fund) plus a computed `unmeasured_flag` (true if not) —
  directly mirroring `TIER-0002` §3.5's `unmeasured_flag` design and `REL-0007`'s recomputation discipline.
  No new percentage, ceiling, or score is invented here — this axis reports whether the *existing* 8%/40%
  issuer-look-through mechanism already covers this fund, not a new number.
- **Abstention state**: `not_applicable` for a fund with no equity constituents to look through (GLD; see
  §5). There is no `unable_to_determine` state — this axis is purely mechanical (computed from files that
  either contain an entry or don't), so it cannot be "insufficient evidence," only "not applicable" or
  computed.
- **Prohibited inference**: no new cluster cap, no new ceiling, no re-derivation of the 8%/40%
  `issuer_lookthrough.yaml` thresholds — this axis reads that mechanism, it never modifies or duplicates
  it.
- **Downstream use**: the structural-risk-flag half of the cross-asset handoff envelope; directly answers
  the future overlap/concentration-modeling requirement `XASSET-0001` §F names, for the ETF sleeve
  specifically.

#### `cost_and_tracking_quality`

- **Purpose**: record the fund's own disclosed cost (expense ratio) and execution quality (tracking
  difference/error against its own stated benchmark) as plain financial facts.
- **Evidence inputs**: the fund provider's own current expense-ratio disclosure; the fund provider's own
  or a reputable third party's published tracking-difference/tracking-error figure.
- **Closed vocabulary**: `expense_ratio_pct` (a real disclosed percentage — **explicitly permitted** under
  §8's numeric-leakage rule, since this is an inherited financial fact, not a proposed target/score,
  matching how Milestone 6/7/8 already carry real percentages inherited from company disclosures);
  `tracking_quality_category` (`tight_tracking` | `moderate_tracking_deviation` |
  `material_tracking_deviation` | `not_yet_measured`).
- **Abstention state**: `unable_to_determine` with `abstention_reason` if the current expense ratio or
  tracking figure cannot be sourced. No `not_applicable` — every fund, including GLD, has both a real
  expense ratio and a real tracking record against its own benchmark (spot gold, for GLD).
- **Prohibited inference**: no derived "this fund is cheap/expensive relative to X" ranking against
  another fund; the field states the fund's own number, never a comparative verdict.
- **Downstream use**: cost/tracking-quality summary in the cross-asset handoff envelope; direct input to
  a future opportunity-cost comparison (`XASSET-0001` §A/§E), not computed by this design.

#### `liquidity`

- **Purpose**: record how readily this fund can be converted to cash without material value loss —
  distinct from margin-buffer capacity, which is an account-level fact this framework does not touch.
- **Evidence inputs**: the fund's own disclosed average daily trading volume, typical bid-ask spread, and
  total assets under management (AUM), from the fund provider or a reputable market-data source.
- **Closed vocabulary**: `liquidity_tier` (`high_liquidity` | `moderate_liquidity` | `low_liquidity` |
  `unable_to_determine`).
- **Abstention state**: `unable_to_determine` (folded into the vocabulary itself, since liquidity is
  always in-scope for a fund — there is no genuine `not_applicable` case).
- **Prohibited inference**: no derived stress-scenario liquidity estimate, no drawdown-adjusted liquidity
  score — this axis states the fund's own currently observable trading characteristics, nothing modeled.
- **Downstream use**: liquidity-risk-descriptor field of the cross-asset handoff envelope; a required
  future input to `XASSET-0001` §F's whole-portfolio liquidity accounting.

#### `structure_and_methodology`

- **Purpose**: record the fund's own structural and operational mechanics — what kind of instrument it
  actually is, beneath the ticker. This is the axis that keeps GLD from being silently treated as "just
  another equity index fund" (see §5).
- **Evidence inputs**: the fund's own prospectus/structural disclosure — replication method
  (physical/full replication, sampling, synthetic/derivative-based), custodian, creation/redemption
  mechanism, and whether the fund tracks a published index or a raw commodity/spot price.
- **Closed vocabulary**: `replication_method` (`physical_full_replication` | `physical_sampling` |
  `synthetic_derivative_based` | `direct_physical_commodity_holding`); `benchmark_type`
  (`published_market_index` | `spot_commodity_price` | `other_benchmark`, with required `benchmark_basis`
  sentence for `other_benchmark`).
- **Abstention state**: `unable_to_determine` with `abstention_reason`. No `not_applicable` — every fund
  has a real structural mechanism.
- **Prohibited inference**: no judgment on whether the structure is "good" or "risky" relative to another
  fund's structure — this axis states the mechanism, not a verdict on it.
- **Downstream use**: structural-risk-flag input to the cross-asset handoff envelope (a
  `direct_physical_commodity_holding` value is itself a structural fact a future custody/counterparty-risk
  accounting would want to see, distinct from — and this design explicitly does not invent — a
  custody-risk *score*).

#### `evidence_quality`

- **Purpose**: mirrors `TIER-0002`'s equity `evidence_quality` axis directly — a record-level summary of
  how well-sourced the whole record is, plus one required uncertainty statement.
- **Evidence inputs**: a rollup of how many of the six axes above reached a determination versus an
  abstention.
- **Closed vocabulary**: `primary_source_coverage` (`comprehensive` | `partial` | `limited`, reusing the
  exact three-value vocabulary `TIER-0004`/Milestone 6 already established for equities, since it is a
  general evidence-sufficiency concept, not equity-specific content).
- **Abstention state**: this axis cannot itself abstain — a record with insufficient evidence everywhere
  still reports `limited`, it does not decline to report at all. This mirrors Milestone 6's own design
  (every sealed equity record carries an `evidence_quality` value; abstention lives inside the *other*
  axes, not this one).
- **Prohibited inference**: no numeric score derived from the abstention count; `primary_source_coverage`
  is a categorical judgment call by the drafting session, not an arithmetic function of how many axes
  abstained (an arithmetic mapping would itself be exactly the "hidden scoring" §8 prohibits).
- **Downstream use**: the `evidence_quality_status` field of the cross-asset handoff envelope directly.

### 3.3 ETF abstention summary

Two genuinely distinct abstention semantics are used throughout, never conflated:

- **`not_applicable`** — the axis does not exist for this instrument's actual structure (GLD has no
  sector exposure to report; a domestic-only fund has no currency exposure to report). This is a
  structural fact, established once, not a placeholder for missing evidence.
- **`unable_to_determine`** — the axis exists and matters, but current evidence cannot support a
  determination. Always requires an `abstention_reason` sentence, matching `TIER-0004`'s
  `economic_role.unable_to_determine` amendment precedent exactly.

**Abstention does not cascade** — exactly the rule `TIER-0004` established for equities: a bounded
unresolved item on one axis is never automatic grounds for abstaining on another. Each of the six axes is
evaluated on its own evidence sufficiency.

## 4. Crypto framework

### 4.1 Candidate axes evaluated (12 named in the authorizing prompt) → 6 designed axes

| Candidate (as named) | Disposition | Reasoning |
|---|---|---|
| network/protocol fundamentals | **Kept, expanded** → `network_fundamentals` | |
| usage/adoption | **Merged into `network_fundamentals`** | Adoption metrics (active addresses, transaction volume, developer activity) are evidence *for* protocol health, not an economically separate dimension from the protocol itself — one evidence read, one axis, same merge logic as ETF's `constituent_exposure`. |
| fee/revenue economics where applicable | **Merged** → `economic_model` | |
| supply/tokenomics | **Merged into `economic_model`** | |
| staking economics where applicable | **Merged into `economic_model`** | Fee/revenue accrual, issuance/supply schedule, and staking yield are all facets of one question — "how does value accrue to, or dilute, a holder of this token" — and for any single coin, most of these sub-fields will be `not_applicable` together (BTC: no fee-to-holder accrual, no staking; ETH/SOL: both apply). Splitting them into three axes would multiply abstention bookkeeping for no decision benefit. |
| liquidity/market structure | **Kept** → `liquidity_and_market_structure` | Mirrors ETF's `liquidity` axis; kept as its own axis (not merged with economic_model) because it is a distinct evidence source (exchange volume, order-book depth) from the protocol's own tokenomics. |
| custody/counterparty risk | **Kept** → `custody_and_counterparty_risk` | Deliberately **not** merged with liquidity — genuinely distinct risk class (exchange/custodian solvency, smart-contract risk, key-management risk) from market-depth liquidity; conflating them would hide a real risk category the ETF framework doesn't need (funds don't carry smart-contract/self-custody risk) but crypto does. |
| cross-coin correlation | **Merged** → `correlation_and_volatility` | |
| volatility/drawdown behavior | **Merged into `correlation_and_volatility`** | Both are statistical return-behavior facts computed from price history, distinct in kind from every narrative axis above — mirrors the ETF framework's judgment-vs-computation split (`overlap_and_concentration`). Kept as one mechanical axis rather than two, since both draw on the same price-history evidence source. |
| regulatory/structural uncertainty if supported | **Kept, conditional** → `regulatory_and_structural_uncertainty` | Included exactly as named — "if supported." See §4.3 for the explicit conditionality and the guardrail against predictive legal/regulatory forecasting. |
| evidence quality | **Kept** → `evidence_quality` | Mirrors the ETF and equity `evidence_quality` axes. |
| uncertainty/abstention | **Not a standalone axis** | Same reasoning as §3.1 — each axis carries its own abstention path. |

**Result: 6 crypto axes** — `network_fundamentals`, `economic_model`, `liquidity_and_market_structure`,
`custody_and_counterparty_risk`, `correlation_and_volatility`, `regulatory_and_structural_uncertainty`,
plus `evidence_quality` (the uncertainty-summary axis, same 7-field total shape as the ETF framework).

### 4.2 Explicit rejection of equity/company-shaped fields

Per `XASSET-0001` §C's explicit prohibition, the following equity-shaped concepts are **excluded outright**
from this framework, with the reasoning stated so a future implementation cannot silently reintroduce
them by analogy:

- **No `economic_role`/`capital_priority` in `TIER-0002`'s company sense.** A cryptocurrency has no
  issuer, no competitive position relative to other companies, no capital-allocation decision-maker whose
  priorities can be assessed. `network_fundamentals` is the closest analogue and is deliberately
  protocol-shaped (consensus mechanism, decentralization characteristics, protocol governance
  mechanism where one exists) — not company-shaped ("management team quality," "capital allocation
  discipline," "competitive moat") in any respect.
- **No financial-statement-derived fields.** No earnings, no revenue-multiple, no balance-sheet metric —
  none of these exist for a cryptocurrency in the sense they exist for a company. `economic_model`'s
  fee/revenue sub-field records protocol-level fee economics (e.g., transaction fees paid to validators),
  never a company-style income statement.
- **No "risk_concentration" in `TIER-0002`'s cluster/issuer-look-through sense**, because no cluster cap
  or issuer-look-through mechanism currently covers cryptocurrency (`issuer_lookthrough.yaml`'s `funds:`
  list contains only SPY/VEA/VWO). `correlation_and_volatility` is the crypto-appropriate substitute —
  a mechanical, computed statistical-behavior rollup, not a repurposed equity concentration ceiling.
- **Protocol governance is included; corporate governance is not.** A coin's on-chain governance
  mechanism (e.g., proof-of-stake validator set, governance-token voting) is legitimate protocol
  fundamental evidence and belongs in `network_fundamentals`. A judgment resembling "does this protocol
  have good management" is explicitly out of scope — there is no management to assess in the company
  sense.

### 4.3 Field-by-field design

#### `network_fundamentals`

- **Purpose**: record the protocol's own technical and adoption characteristics as categorical fact.
- **Evidence inputs**: the protocol's own published technical documentation (consensus mechanism, network
  security model); publicly available on-chain metrics (active addresses, transaction throughput,
  validator/miner count) and developer-activity indicators from a reputable data source.
- **Closed vocabulary**: `consensus_mechanism` (`proof_of_work` | `proof_of_stake` | `other_consensus`,
  with required `consensus_basis` sentence for `other_consensus`); `adoption_trend_category`
  (`established_high_usage` | `growing_usage` | `declining_or_stagnant_usage` | `unable_to_determine`).
- **Abstention state**: `unable_to_determine` with `abstention_reason` for `adoption_trend_category`.
  `consensus_mechanism` has no abstention path — it is a fixed, publicly documented protocol design
  choice, always determinable for a live network.
- **Prohibited inference**: no prediction of future adoption trajectory, no "this network will win" or
  "this network is technically superior" ranking against another coin — states the current documented
  mechanism and current observable trend category, nothing forward-looking.
- **Downstream use**: `role`-equivalent field of the cross-asset handoff envelope (§4.4) — the closest
  crypto analogue to the ETF framework's `structural_role`, though deliberately named differently to avoid
  implying a false equivalence between "what a fund's benchmark is" and "what a protocol's consensus
  design is."

#### `economic_model`

- **Purpose**: record how value accrues to (or is diluted from) a holder of this token — fee economics,
  supply schedule, and staking yield, where each applies.
- **Evidence inputs**: the protocol's own published tokenomics documentation (issuance schedule, maximum
  supply if any, fee-burn or fee-distribution mechanism); the protocol's own published staking-reward
  mechanism, where one exists.
- **Closed vocabulary**: `supply_model` (`fixed_capped_supply` | `disinflationary_schedule` |
  `uncapped_or_inflationary` | `unable_to_determine`); `fee_accrual_applicable` (boolean) with a required
  `fee_accrual_basis` sentence when true; `staking_applicable` (boolean) with a required
  `staking_basis` sentence when true.
- **Abstention state**: `not_applicable` for `fee_accrual_applicable`/`staking_applicable` when the
  protocol genuinely has no such mechanism (Bitcoin has no protocol-level fee accrual to holders and no
  staking) — a structural fact, not an evidence gap. `unable_to_determine` with `abstention_reason` for
  `supply_model` when current documentation cannot support a categorization.
- **Prohibited inference**: no derived "expected yield" projection, no price-impact estimate from
  supply-schedule facts — the axis records the mechanism as designed, never a forecast of its effect on
  value.
- **Downstream use**: economic-model summary in the cross-asset handoff envelope; a required future input
  to any opportunity-cost comparison between crypto-sleeve deployment and other sleeves (`XASSET-0001`
  §A/§E), not computed here.

#### `liquidity_and_market_structure`

- **Purpose**: record how readily this position can be converted to cash without material value loss, and
  the structural characteristics of where it trades.
- **Evidence inputs**: publicly available trading-volume, order-book-depth, and exchange-listing-breadth
  data from a reputable market-data source.
- **Closed vocabulary**: `liquidity_tier` (`high_liquidity` | `moderate_liquidity` | `low_liquidity` |
  `unable_to_determine`); `market_structure_notes` free-text field (bounded, factual — exchange-listing
  breadth, not a prediction).
- **Abstention state**: `unable_to_determine` (folded into the vocabulary, same as the ETF `liquidity`
  axis — always in-scope, no `not_applicable` case).
- **Prohibited inference**: no stress-scenario liquidity model, no drawdown-adjusted liquidity score.
- **Downstream use**: liquidity-risk-descriptor field of the cross-asset handoff envelope.

#### `custody_and_counterparty_risk`

- **Purpose**: record the structural risks specific to holding a cryptocurrency — custodial arrangement,
  smart-contract exposure, and key-management model — a risk class that genuinely does not exist for an
  equity or a conventional ETF.
- **Evidence inputs**: the account's own actual custody arrangement (as already disclosed in CLAUDE.md's
  Portfolio Doctrine — Robinhood custody for the current crypto sleeve) as a factual, non-speculative
  input; the protocol's own disclosed smart-contract-risk profile (e.g., a base-layer protocol with a
  long, unexploited security track record versus a newer or more complex smart-contract platform).
- **Closed vocabulary**: `custody_model` (`exchange_custodied` | `self_custodied` | `mixed_or_unknown`);
  `smart_contract_risk_category` (`base_layer_minimal_smart_contract_surface` |
  `smart_contract_platform_material_surface` | `not_applicable` | `unable_to_determine`).
- **Abstention state**: `not_applicable` for `smart_contract_risk_category` is reserved for a protocol
  with genuinely no programmable smart-contract layer (e.g., a pure payment/store-of-value base layer);
  `unable_to_determine` with `abstention_reason` otherwise.
- **Prohibited inference**: no security-incident prediction, no "this exchange might fail" speculation —
  states the current custody arrangement and the protocol's documented smart-contract surface, nothing
  predictive about counterparty solvency.
- **Downstream use**: structural-risk-flag input to the cross-asset handoff envelope; a required future
  input to `XASSET-0001` §F's whole-portfolio risk accounting (a risk class ETFs and equities do not
  carry, making its explicit inclusion here — rather than a generic "counterparty risk" field forced onto
  every asset type — a direct product of the asset-appropriate design principle in §2).

#### `correlation_and_volatility`

- **Purpose**: a **mechanical, computed** rollup of this coin's own historical volatility/drawdown
  behavior and its correlation with the other crypto-sleeve members and with broader risk-on equity beta
  — mirrors the ETF framework's `overlap_and_concentration` design: computed, never independently
  asserted.
- **Evidence inputs**: publicly available historical price data for the coin and, where a future
  correlation computation is separately authorized, the other crypto-sleeve members and a broad equity
  benchmark. **This design does not authorize computing a new correlation study** — see §8's explicit
  prohibition; this axis's schema exists so that *if* a future, separately-authorized correlation study
  is conducted (matching `REL-0001` §G/§L's discipline that structural evidence and measured correlation
  stay separate, and that naming a gap does not pre-authorize filling it), its result has a place to live
  without inventing a new schema at that time.
- **Closed vocabulary**: `historical_volatility_category` (`high_volatility` | `extreme_volatility` |
  `unable_to_determine` — crypto's own historical range does not support a `low_volatility` value for any
  currently-held coin, so it is omitted rather than included as a value nothing will ever select);
  `cross_coin_correlation_status` (`not_yet_measured` | `measured_elsewhere_cross_reference_required`) —
  **no numeric correlation coefficient field exists in this schema**; a coefficient, if one is ever
  computed under a separately-authorized future study, is cross-referenced by pointer, never duplicated
  or restated here as a schema value (the same reference-not-restate discipline `OPS-0008` established
  for retained evidence).
- **Abstention state**: `not_yet_measured` is itself the default/abstention value for
  `cross_coin_correlation_status` until a future study exists — there is no separate abstention path
  beyond this vocabulary value.
- **Prohibited inference**: no numeric correlation coefficient, no volatility-adjusted position-size
  recommendation, no "this coin diversifies the sleeve" conclusion — the axis records only whether a
  measurement exists to reference, and (once one exists) points to it.
- **Downstream use**: structural-risk-flag input to the cross-asset handoff envelope; the crypto-specific
  half of `XASSET-0001` §F's required "crypto cross-correlation" future work.

#### `regulatory_and_structural_uncertainty`

- **Purpose**: record genuinely evidenced, currently-disclosed regulatory or structural uncertainty
  affecting this coin — included conditionally, exactly as the authorizing prompt names it ("if
  supported"), never as a predictive forecast.
- **Evidence inputs**: currently-in-force or currently-pending regulatory actions, disclosed as fact with
  a citation (e.g., a named regulatory proceeding, a disclosed exchange-delisting action) — never an
  analyst's or this framework's own prediction of a future regulatory outcome.
- **Closed vocabulary**: `disclosed_regulatory_matter_exists` (boolean) with a required
  `matter_summary_and_citation` sentence when true; `structural_uncertainty_category`
  (`none_currently_disclosed` | `disclosed_and_unresolved` | `unable_to_determine`).
- **Abstention state**: `none_currently_disclosed` is the honest default, not an abstention — most coins,
  most of the time, will carry no currently-disclosed matter, and recording that plainly is the correct
  fact, not a gap. `unable_to_determine` with `abstention_reason` is reserved for a case where evidence
  access itself is the problem (a blocked primary source), distinct from "genuinely nothing disclosed."
- **Prohibited inference**: **this axis may never contain a predictive regulatory or legal opinion** —
  matching CLAUDE.md's own standing guardrail ("No predictive research, price targets, or 'opportunity
  maps'"). Only currently-disclosed, citable matters are permitted; "regulatory risk is likely to
  increase" or any forward-looking regulatory forecast is explicitly prohibited content, not merely
  discouraged.
- **Downstream use**: structural-risk-flag input to the cross-asset handoff envelope.

#### `evidence_quality`

- Identical design to the ETF framework's `evidence_quality` axis (§3.2), reusing the same
  `comprehensive`/`partial`/`limited` vocabulary. Not restated here to avoid duplication — see §3.2.

### 4.4 Crypto abstention summary

Same two-state discipline as §3.3 (`not_applicable` for a structurally absent mechanism — e.g., BTC's
absent staking — versus `unable_to_determine` for an evidence gap on an axis that genuinely applies), and
the same non-cascading rule.

## 5. GLD placement — resolved as Option C, from existing authority

**Determination: GLD receives both (A) structural fund-mechanics treatment under the ETF framework and
(B) its portfolio *role* is explicitly reserved for a future functional defensive-asset doctrine unit —
neither this design nor any future ETF classification built from it may assign GLD's role.**

This is resolved from existing repository authority, not a new principal-level policy call, for three
independently sufficient reasons:

1. **`targets.yaml`'s own config schema already classifies GLD `asset_class: fund`** — identical to
   SPY/VEA/VWO, confirmed by direct inspection (`targets.yaml` line 70: `{ticker: GLD, target_pct: 4.00,
   asset_class: fund}`). Structurally, in the one place this repository's config already draws an
   asset-class line, GLD sits inside the fund category, not a separate one. A fund-structural evaluation
   (cost, tracking versus its own benchmark, replication method, liquidity) is therefore squarely
   in-scope for the ETF framework, on the repository's own existing terms.
2. **`issuer_lookthrough.yaml` already, independently, treats GLD differently from SPY/VEA/VWO** —
   confirmed by direct inspection: every `funds:` entry across all 20+ issuer rows names only `SPY`,
   `VEA`, or `VWO`; GLD never appears as a `fund:` value anywhere in the file, because it holds physical
   gold, not equity constituents. This is exactly why `constituent_exposure` and
   `overlap_and_concentration` (§3.2) both carry a genuine `not_applicable` state, and exactly why GLD
   will use it — a structural fact this repository's own live data already establishes, not an assumption
   this design invents.
3. **`XASSET-0001` §D explicitly separates GLD's *role* question from asset-*structure* classification**:
   "Cash/reserve, GLD/defensive assets, and debt reduction ... require governed functional doctrine as
   competing uses of capital, not classification." This assigns the ballast/defensive-role *judgment*
   to a future, separately authorized functional-doctrine unit (`WS-0014` item 8) — it does not say GLD
   may never be structurally evaluated as the fund product it concretely is. The two questions are
   different in kind: "what does GLD cost, how well does it track spot gold, how is it legally structured"
   are ETF-framework-shaped structural facts; "should the portfolio treat gold as ballast, and how much"
   is a functional-doctrine, competing-use-of-capital judgment `XASSET-0001` §D already assigns
   elsewhere.

**Concretely, when a future ETF-classification implementation eventually covers GLD** (not authorized by
this design — see §7): `structural_role`, `cost_and_tracking_quality`, `liquidity`, and
`structure_and_methodology` all apply and must reach a real determination or a genuine
`unable_to_determine`; `constituent_exposure` and `overlap_and_concentration` are expected to resolve to
`not_applicable` (a physically-backed commodity trust has no sector/geographic/currency constituent
breakdown and no equity-constituent overlap to compute) — that is the correct, evidenced outcome, not a
schema failure. GLD's `structural_role.role_category` value under this framework (most likely
`precious_metals_or_commodity`, though not assigned by this design) is **explicitly not** the same
determination as its future functional-doctrine role (e.g., "defensive ballast") — the former is a
structural-fund-type fact, the latter is a portfolio-role policy judgment reserved to §D's future unit.
This distinction is recorded in the cross-asset handoff envelope as two separate fields for exactly this
reason (§6.1).

No principal stop was required: all three lines of authority above are independently sufficient and
mutually reinforcing, and none of them conflicts with another.

## 6. Shared meta-architecture

### 6.1 Common envelope fields (both frameworks)

| Field | Purpose | Notes |
|---|---|---|
| `instrument_id` | canonical symbol | must resolve against `intelligence/contenders/registry.yaml` if that record exists for the symbol (per `CONTENDER-0002`'s own canonicalization precedent); no new alias mechanism invented. |
| `asset_type` | exactly one of `etf` \| `cryptocurrency` | closed, mandatory, never mixed with an equity or with each other on one record. |
| `schema_version` | framework schema version string | mirrors `TIER-0002`'s classification-record convention. |
| `provenance` | sources list, evidence-access disclosure | each source cited with type (primary/secondary) and access status, mirroring Milestone 6/7/8's disclosed-access-failure convention (`attempted but not directly inspected` is a permitted, honest value). |
| `evidence_quality_status` | copy of the record's own `evidence_quality.primary_source_coverage` value | a read-only projection, never independently computed — see §6.2. |
| `uncertainty_summary` | one required narrative sentence | mirrors Milestone 6/7/8's `thesis_uncertainty_statement` pattern — names the single most significant evidence gap or open question for this instrument. |
| `structural_risk_flags` | asset-appropriate mechanical flags | ETF: `overlap_and_concentration.unmeasured_flag`/`.not_applicable`; crypto: `custody_and_counterparty_risk` category + `correlation_and_volatility.cross_coin_correlation_status` — a read-only projection of already-computed axis values, never a new computation (see §6.2). |
| `record_status` | `draft` \| `sealed` | mirrors Milestone 6's `lifecycle_status` sealing discipline (§9). |
| `valuation_and_economic_assessment_readiness` | forced categorical abstention, asset-appropriate | see §6.3 — the direct analogue of `TIER-0009`'s `valuation_required` forcing. |
| `cross_asset_handoff` | normalized summary object | see §6.4. |
| `abstention_index` | a list of every axis that abstained on this record, with its stated reason | a mechanical rollup of the individual axis abstentions, for a future cross-asset synthesis to scan without re-reading every axis. |

**No numeric score, rank, or target field exists anywhere in this envelope or in either framework's own
axes** — the only numeric fields anywhere in this design are `cost_and_tracking_quality.expense_ratio_pct`
and its tracking-difference companion, both real, disclosed, inherited financial facts (not proposed
values), matching exactly how Milestone 6/7/8 already carry inherited percentages from company
disclosures without those being "scores."

### 6.2 Read-only projection, not new computation

Every envelope field above that summarizes an axis value (`evidence_quality_status`,
`structural_risk_flags`) is **explicitly a copy of an already-computed axis field**, never a new
computation performed at the envelope level. This is a deliberate design constraint, not an
implementation detail: it is the mechanism by which this design guarantees "no hidden scoring" at the
envelope layer — there is nothing for the envelope to compute, only to copy forward. A future validator
(§8) must enforce this by checking envelope-level fields against their source axis fields for exact
consistency, the same reconciliation discipline `TIER-0009`'s `recommendation_validator.py` already
applies to its own aggregate block.

### 6.3 Valuation/economic-assessment-readiness — the asset-appropriate `valuation_required` analogue

`TIER-0009` §G.4/§G.5 forces `primary_status: valuation_required` on every one of the 27 equity records'
`target_and_range`/`maximum_position_size` fields, because **no governed valuation methodology exists
anywhere in this repository for any asset type** — equity, ETF, or crypto alike. This design carries that
exact discipline forward, asset-appropriately named:

- **Field**: `valuation_and_economic_assessment_readiness.status`
- **Closed vocabulary**: exactly one value today — `valuation_required` — with a required `rationale`
  field. No second value exists in the vocabulary yet, matching `TIER-0009`'s own doctrinally-forced,
  zero-exception design (not a placeholder omission — a future governed valuation methodology, once it
  exists, would itself add the value that supersedes this forced default, exactly as `TIER-0009` describes
  for the equity sleeve's own eventual valuation work).
- **Prohibited content**: no fair value, no target price, no `target_pct`, no target range, no maximum
  position size, no score, no rank — enforced identically to `TIER-0009`'s own forced-value mechanical
  check (§8 below specifies the validator requirement).

This directly satisfies the valuation boundary the authorizing prompt requires: framework/classification
→ later asset-specific valuation/economic assessment → later cross-asset synthesis → later sizing, with
no framework record ever short-circuiting that chain.

### 6.4 Cross-asset handoff contract

`cross_asset_handoff` is a normalized, read-only summary sub-object every record (ETF or crypto) carries,
so a future `XASSET-0001` §E/§F synthesis unit can compare across asset types without needing
asset-specific schema knowledge of every framework:

| Handoff field | Sourced from |
|---|---|
| `role_summary` | ETF: `structural_role.role_category`. Crypto: `network_fundamentals.consensus_mechanism` + `adoption_trend_category`. |
| `evidence_quality_summary` | `evidence_quality.primary_source_coverage` (both frameworks). |
| `uncertainty_summary` | the envelope's own `uncertainty_summary` (§6.1), not re-derived. |
| `liquidity_risk_summary` | ETF: `liquidity.liquidity_tier`. Crypto: `liquidity_and_market_structure.liquidity_tier`. |
| `overlap_or_correlation_signal` | ETF: `overlap_and_concentration.unmeasured_flag`/`not_applicable`. Crypto: `correlation_and_volatility.cross_coin_correlation_status`. |
| `valuation_readiness` | `valuation_and_economic_assessment_readiness.status` (§6.3), copied verbatim. |

Every handoff field is a **copy**, never an independent computation (§6.2's rule applies identically
here) — this is what keeps the contract free of hidden scoring: a future synthesis unit reading only the
handoff object sees exactly the same categorical facts a reader of the full record would see, just
normalized into asset-neutral field names for cross-type comparison.

## 7. Batching / future lifecycle — binding rules for what comes next

Restated and made binding for every future `WS-0014` unit building on this design (per `XASSET-0001` §J,
not loosened or reinterpreted):

1. **This design filing is itself the batched design-only unit** `XASSET-0001` §J explicitly permits
   ("ETF + crypto framework design ... may reasonably batch as one architecture unit").
2. **ETF classification content is its own future, separate implementation PR** — never combined with
   this design filing, never combined with crypto classification content.
3. **Crypto classification content is its own future, separate implementation PR** — same rule, opposite
   direction.
4. **Design must never be recombined with content** — no future PR may both revise this schema and
   classify a fund or coin in the same unit; a schema revision, if ever needed, is its own future,
   separately authorized design-amendment unit (matching `TIER-0002`→`TIER-0004`'s own precedent of a
   later, narrow, separately authorized schema amendment — the `economic_role.unable_to_determine`
   addition — rather than folding a schema change into content work).
5. **ETF and crypto content must never share one filing**, even though their designs share one filing —
   different asset types, different evidence standards, `XASSET-0001` §J's own explicit rule, unweakened.
6. **Valuation/economic methodology is later and separate** from both frameworks — neither framework, nor
   any future classification built from it, may itself define or apply a valuation methodology; §6.3's
   forced `valuation_required` state is the explicit marker of that boundary until a future,
   separately-authorized methodology exists.

## 8. Validator specification (for the future implementing PR)

A future implementation must build a validator (or two closely related validators, one per asset type,
sharing envelope-level helpers) enforcing, at minimum:

1. **Exact population enforcement** — whatever population a future classification batch authorization
   names, the validator confirms exactly that set, no more, no fewer (mirrors `classification_validator.py`'s
   27-ticker population check).
2. **Closed schema at every level** — envelope, per-axis, and any nested sub-object (mirrors
   `classification_validator.py`'s and `recommendation_validator.py`'s own hard-won closed-schema
   discipline, including the corrected extra-key check `contender_registry_validator.py`'s own review
   history required — §9.1 below records this as a lesson explicitly carried forward).
3. **Asset-type separation** — an ETF record's `asset_type` must be exactly `etf`, never `cryptocurrency`,
   and vice versa; the validator must reject a record whose axis fields don't match its declared
   `asset_type` (e.g., a `network_fundamentals` field on a record declaring `asset_type: etf`).
4. **No ETF/crypto schema cross-contamination** — an ETF record must never carry a crypto-only field
   (`custody_and_counterparty_risk`, `correlation_and_volatility`, `network_fundamentals`, `economic_model`,
   `regulatory_and_structural_uncertainty`) and a crypto record must never carry an ETF-only field
   (`structural_role`, `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`,
   `structure_and_methodology`) — enforced by the same closed-schema mechanism as point 2, applied
   per-`asset_type`.
5. **No equity-field leakage** — neither schema may ever carry `economic_role`, `capital_priority`,
   `risk_concentration`, or any `TIER-0002`-shaped field name; a dedicated forbidden-key scan (mirroring
   `recommendation_validator.py`'s forbidden-key-name scan) checks for these names anywhere in the
   document tree, not just at the top level.
6. **No numeric score/rank/target leakage** — a forbidden-key scan for `target_pct`, `target_range`,
   `max_position_size`, `score`, `rank`, `conviction_score`, `recommended_target_pct` (the exact exploit
   class `contender_registry_validator.py`'s own review found and fixed — §9.1), applied at every schema
   level; a **scoped** numeric-percent-token check that explicitly permits `expense_ratio_pct` and its
   tracking-difference companion (real disclosed financial facts) while rejecting any percent-shaped value
   attached to a forbidden key.
7. **No chart evidence leakage** — an independent, free-text scan for chart-domain terminology (support/
   resistance, breakout, trend line, moving average, RSI, MACD, candlestick, chart pattern, technical
   analysis, oversold, overbought, Fibonacci, volume profile, price target, momentum), built in from the
   start rather than deferred — directly learning from, and not repeating, `reconciliation_validator.py`'s
   own disclosed defense-in-depth gap (a self-declared `chart_evidence_used` flag enforced without an
   independent scan) that `recommendation_validator.py` already corrected once (§9.1).
8. **Evidence/provenance validation** — every `provenance.sources` entry must carry a type
   (primary/secondary) and access-status field; a record with zero sources is invalid unless every
   substantive axis abstained with a stated reason (mirroring the equity classification pipeline's own
   evidence-citation discipline).
9. **Abstention requirements** — every `unable_to_determine` value must carry a non-empty
   `abstention_reason`; every axis-specific `not_applicable` use must be checked against the closed list
   of axes that genuinely support it (§3.3/§4.4) — a validator must reject `not_applicable` on an axis
   that has no such state defined (e.g., `cost_and_tracking_quality` has no `not_applicable` state; using
   it there is a schema violation, not a valid abstention).
10. **Deterministic generation** — repeated validator runs against the same input produce byte-identical
    results; no `Date.now()`/random-order iteration in any future generator.
11. **Protected-path isolation** — a future implementation's own test suite must assert zero diff on
    `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`,
    `margin_state.py`, `levels.py`, every existing `intelligence/classification|companies|themes|
    relationships/` record, `COHORT_MANIFEST.yaml`, and every existing governance decision file.
12. **Allocator/margin decoupling** — zero import coupling with `allocate.py`/`margin_state.py` in either
    direction, matching every prior Intelligence-adjacent validator in this repository
    (`classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`,
    `relationship_validator.py`, `contender_registry_validator.py`).
13. **Cross-asset policy non-implication** — the validator must confirm that validating an ETF or crypto
    record, by itself, changes nothing about `targets.yaml`'s existing `target_pct` values, `gates.yaml`,
    or any allocator output — a structural assertion (no code path from this validator writes to any of
    those files), not merely a documentation claim.

## 9. Test specification (for the future implementing PR)

A future implementation's focused test suite must cover, at minimum, one test per item below, per asset
type where the item applies to both:

- ETF happy-path record (all six axes present, valid, no abstention) validates clean.
- Crypto happy-path record (all six axes present, valid, no abstention) validates clean.
- Malformed top-level/envelope schema (missing required envelope field) rejected.
- Malformed instrument (axis-level) schema (missing required axis sub-field) rejected.
- Extra unknown key at envelope level rejected (the exact `contender_registry_validator.py` MAJOR-finding
  exploit class, §9.1 — proactively tested here rather than found in a later review).
- Extra unknown key at axis level rejected (same class, applied one level deeper).
- Missing required key at each of envelope/axis levels rejected.
- Wrong `asset_type` value (neither `etf` nor `cryptocurrency`) rejected.
- ETF record carrying a crypto-only field rejected (cross-contamination, point 4).
- Crypto record carrying an ETF-only field rejected (cross-contamination, opposite direction).
- Forbidden equity field (`economic_role`, `capital_priority`, `risk_concentration`) present anywhere in
  either schema rejected.
- Invalid/missing evidence citation (a source with no type or no access-status field) rejected.
- Abstention behavior: `unable_to_determine` without `abstention_reason` rejected; `not_applicable` used
  on an axis that doesn't support it rejected; a fully-populated abstention (all required companion
  fields present) accepted.
- Duplicate instrument entry within one population batch rejected.
- Missing instrument from a named, authorized population rejected.
- Extra instrument beyond a named, authorized population rejected.
- Numeric target/range/max-position-size leakage (`target_pct`, `target_range`, `max_position_size`)
  anywhere in the document rejected.
- Score/rank leakage (`score`, `rank`, `conviction_score`, `recommended_target_pct`) anywhere in the
  document rejected.
- Legitimate disclosed percentage (`expense_ratio_pct`) on a forbidden-key-adjacent field name is
  correctly **accepted**, proving the numeric scan is scoped, not blanket (avoiding the inverse failure
  mode of over-rejecting real financial facts).
- Chart-terminology leakage (each of the sixteen terms individually) rejected, mirroring
  `recommendation_validator.py`'s own individually-proven-caught test design.
- Directive/trading language leakage (buy/sell/add/hold/trim/exit/wait/stage) rejected, mirroring
  `recommendation_validator.py`'s word-boundary-matched design so it does not false-positive on the noun
  "holdings" or a section title.
- `valuation_and_economic_assessment_readiness.status` forced-value violation (any value other than
  `valuation_required`) rejected — the direct crypto/ETF analogue of `recommendation_validator.py`'s own
  G.4/G.5 forced-value check.
- Envelope-level field failing to match its source axis field (§6.2's read-only-projection rule) rejected
  — e.g., `evidence_quality_status` on the envelope not matching `evidence_quality.primary_source_coverage`
  on the axis.
- Deterministic output: two consecutive validator/generator runs against identical input produce
  byte-identical results.
- Protected-path isolation: a dedicated test asserting zero diff on every path named in §8 point 11,
  before and after a synthetic classification run.
- Allocator/margin import-coupling test: a static-analysis-style check (mirroring existing precedent)
  confirming the future validator module imports neither `allocate.py` nor `margin_state.py`.

### 9.1 Lessons explicitly carried forward from prior validator review history

This design deliberately pre-empts three specific defect classes this repository has already found, in
its own review history, in adjacent validators — named here so a future implementation does not
rediscover them the expensive way:

- **Closed-schema checks must reject extra keys, not just missing ones** —
  `contender_registry_validator.py`'s own independent review (`pullrequestreview-4874631727`) found a real
  MAJOR gap where `validate_entry()`/`validate_registry_data()` computed only the `missing` side of a
  schema check, silently accepting smuggled extra keys like `conviction_score`. §8 point 2 and the test
  list above build the extra-key check in from the start.
  designs' own explicit `TIER-0004` correction ("no independent backstop for dangling section-title
  cross-references") — an independent second-stage check must use a **materially different mechanism**
  than the strip/accept logic it is verifying, not merely call the same function twice. §8's forbidden-key
  and chart-terminology scans should be implemented as free-text/structural scans independent of whatever
  per-field acceptance logic a future generator uses.
- **A self-declared boolean flag is not a substitute for an independent scan** — `reconciliation_
  validator.py`'s own disclosed MINOR finding (carried into `TIER-0008`, then explicitly avoided by
  `recommendation_validator.py`'s design) found that a self-declared `chart_evidence_used: false` flag,
  checked without an independent free-text scan, is a defense-in-depth gap. §8 point 7 requires the
  independent scan from the start, not a flag-only check.

## 10. Whole-portfolio sequencing doctrine (preserved, restated for reference)

This design changes nothing about, and explicitly preserves, the seven-step sequence `TIER-0012`/
`TIER-0013` most recently restated and this artifact's own governing filing (`XASSET-0001` §E) first
established:

1. define governed asset-appropriate frameworks for equities (already exists — `TIER-0002`), ETFs, and
   crypto (this design), plus GLD/defensive-asset, cash/reserve, and debt-reduction functional doctrine
   (not designed here — `XASSET-0001` §D, `WS-0014` item 8, future);
2. perform asset-appropriate valuation/economic assessment (future, separate, undesigned — see §6.3);
3. conduct cross-asset opportunity-cost and overlap/concentration synthesis (`XASSET-0001` §E/§F, future);
4. produce Level 1 sleeve targets (`XASSET-0001` §E, future);
5. produce Level 2 instrument targets inside each sleeve (`XASSET-0001` §E, future);
6. ingest and interpret governed chart evidence for applicable market-priced instruments as a
   deployment/timing and technical-risk layer only — never a substitute for fundamental/economic
   selection (`XASSET-0001` §G, `TIER-0003` unweakened, future);
7. perform final synthesis and determine holdings, target weights, deployment sequencing, and execution
   discipline (future).

This design occupies exactly step 1's ETF-and-crypto portion. It does not perform, and does not authorize,
any later step.

## 11. Objective preserved, not invented

This design does not define, redefine, or narrow Portfolio-HQ's governing objective, restated by
`XASSET-0001` §A and unedited here: *maximize long-term portfolio compounding and capital appreciation
within approved risk, liquidity, concentration, leverage, and survival constraints.* Neither framework
above computes an "expected return" or otherwise operationalizes that objective directly — both frameworks
supply the categorical, evidence-based facts a future valuation/economic-assessment step (§6.3, §10 step
2) and a future cross-asset opportunity-cost synthesis (§10 step 3) would need, without themselves
performing either. **The "next-dollar opportunity-cost methodology" `XASSET-0001` §E/§A implies remains
wholly undesigned** — this artifact does not design it, and states explicitly that it is a required future
principal/governance decision before any cross-asset synthesis (`XASSET-0001` §E) may proceed.
