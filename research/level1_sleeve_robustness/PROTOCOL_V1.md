# Level-1 Investable-Sleeve Robustness Study — Protocol V1

Status: frozen governance protocol for `RISK-0001`. This file and
`pre_registration.yaml` authorize nothing independently. The charter is the authority, and the
structured preregistration is canonical for every closed value, vocabulary, threshold, source,
window, and trial count. If this narrative and the structured file differ, execution must stop and a
separate governance correction is required.

The following block is a mechanically checked, non-independent mirror of the canonical
preregistration. It exists only to detect protocol/preregistration drift; it cannot amend the YAML.

<!-- RISK-0001-PROTOCOL-MIRROR-V1
schema_version: "1.0"
study_id: RISK-0001
scenario_states: [LOWER, HISTORICAL_REFERENCE, HIGHER]
consequential_parameter_values:
  RELATIVE_PERTURBATION: "0.20"
  SCENARIO_DECIMAL_PLACES: 2
  SCENARIO_ROUNDING_MODE: ROUND_HALF_UP
  DFF_DAY_COUNT_DENOMINATOR: 360
  DFF_AVAILABILITY_LAG_BUSINESS_DAYS: 1
  DFF_MISSING_DAYS_ALLOWED: 0
  MINIMUM_IMPROVEMENT_FAMILIES: 2
  LOSS_CONTRIBUTION_TOLERANCE_PP: "1.00"
  RECOVERY_BURDEN_TOLERANCE_PPDAYS: "30.00"
  OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP: "1.00"
  EQUITY_MINIMUM_ELIGIBLE: 21
  EQUITY_DIRECTIONAL_BREADTH: "0.75"
  GOLD_PARITY_CORRELATION_MIN: "0.995"
  GOLD_PARITY_RETURN_MAX_PP: "0.50"
  GOLD_PARITY_DRAWDOWN_MAX_PP: "2.00"
  GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED: 0
  CRYPTO_DUPLICATE_TIMESTAMPS_ALLOWED: 0
  CRYPTO_MISSING_DAYS_ALLOWED: 0
  CRYPTO_MAX_CONTIGUOUS_GAP_DAYS: 0
  FORMULA_INTEGRITY_ABSOLUTE_TOLERANCE: "0.000001"
scenario_magnitudes:
  EQUITY: {LOWER: "14.94", HISTORICAL_REFERENCE: "18.67", HIGHER: "22.40"}
  FUND_BROAD_MARKET: {LOWER: "11.74", HISTORICAL_REFERENCE: "14.67", HIGHER: "17.60"}
  FUND_GLD_DEFENSIVE: {LOWER: "13.34", HISTORICAL_REFERENCE: "16.67", HIGHER: "20.00"}
  CRYPTO: {LOWER: "13.34", HISTORICAL_REFERENCE: "16.67", HIGHER: "20.00"}
window_ids: [ASSET_AVAILABLE_HISTORY, FAMILY_COMMON_OVERLAP, GFC_2008, Q4_2018, COVID_2020, RATE_INFLATION_2022, CRYPTO_STRESS_2022]
window_voting_roles:
  ASSET_AVAILABLE_HISTORY: MANDATORY_VOTING
  FAMILY_COMMON_OVERLAP: MANDATORY_VOTING
  GFC_2008: CONDITIONAL_VOTING
  Q4_2018: CONDITIONAL_VOTING
  COVID_2020: CONDITIONAL_VOTING
  RATE_INFLATION_2022: CONDITIONAL_VOTING
  CRYPTO_STRESS_2022: CONDITIONAL_VOTING
source_fallbacks:
  equities_etfs: [ALPACA_MARKET_DATA, YAHOO_FINANCE_CHART, ABSTAIN]
  crypto: [ALPACA_CRYPTO, COINBASE_EXCHANGE, ABSTAIN]
  comparator: [FRED_DFF, ABSTAIN_OPPORTUNITY_COST_CELLS]
  corporate_actions: [ALPACA_CORPORATE_ACTIONS, SEC_EDGAR_OR_ISSUER, ABSTAIN_AFFECTED_CELLS]
data_gate_stages: [GLOBAL_STUDY_INTEGRITY, CELL_DATA_ELIGIBILITY]
voting_families: [PATH_RISK, RECOVERY, OPPORTUNITY_COST]
minimum_improvement_families: 2
total_state_table:
  - {lower: POLICY_REVIEW_REQUIRED, higher: POLICY_REVIEW_REQUIRED, result: unable_to_determine, review_direction: null}
  - {lower: POLICY_REVIEW_REQUIRED, higher: CENTER_NOT_REJECTED, result: policy_review_required, review_direction: lower_exposure}
  - {lower: POLICY_REVIEW_REQUIRED, higher: UNABLE_TO_DETERMINE, result: unable_to_determine, review_direction: null}
  - {lower: CENTER_NOT_REJECTED, higher: POLICY_REVIEW_REQUIRED, result: policy_review_required, review_direction: higher_exposure}
  - {lower: CENTER_NOT_REJECTED, higher: CENTER_NOT_REJECTED, result: provisional_scenario_not_rejected, review_direction: null}
  - {lower: CENTER_NOT_REJECTED, higher: UNABLE_TO_DETERMINE, result: unable_to_determine, review_direction: null}
  - {lower: UNABLE_TO_DETERMINE, higher: POLICY_REVIEW_REQUIRED, result: unable_to_determine, review_direction: null}
  - {lower: UNABLE_TO_DETERMINE, higher: CENTER_NOT_REJECTED, result: unable_to_determine, review_direction: null}
  - {lower: UNABLE_TO_DETERMINE, higher: UNABLE_TO_DETERMINE, result: unable_to_determine, review_direction: null}
point_state_table:
  - {lower: DISPLACES_REFERENCE, higher: DISPLACES_REFERENCE, point_target_assessment: not_supported, method_review_direction: range_or_nonpoint}
  - {lower: DISPLACES_REFERENCE, higher: ADJACENT_MATERIALLY_WORSE, point_target_assessment: not_supported, method_review_direction: range_or_nonpoint}
  - {lower: DISPLACES_REFERENCE, higher: NOT_DISTINGUISHED, point_target_assessment: not_supported, method_review_direction: range_or_nonpoint}
  - {lower: DISPLACES_REFERENCE, higher: UNAVAILABLE, point_target_assessment: unable_to_determine, method_review_direction: null}
  - {lower: ADJACENT_MATERIALLY_WORSE, higher: DISPLACES_REFERENCE, point_target_assessment: not_supported, method_review_direction: range_or_nonpoint}
  - {lower: ADJACENT_MATERIALLY_WORSE, higher: ADJACENT_MATERIALLY_WORSE, point_target_assessment: not_rejected, method_review_direction: null}
  - {lower: ADJACENT_MATERIALLY_WORSE, higher: NOT_DISTINGUISHED, point_target_assessment: not_rejected, method_review_direction: null}
  - {lower: ADJACENT_MATERIALLY_WORSE, higher: UNAVAILABLE, point_target_assessment: unable_to_determine, method_review_direction: null}
  - {lower: NOT_DISTINGUISHED, higher: DISPLACES_REFERENCE, point_target_assessment: not_supported, method_review_direction: range_or_nonpoint}
  - {lower: NOT_DISTINGUISHED, higher: ADJACENT_MATERIALLY_WORSE, point_target_assessment: not_rejected, method_review_direction: null}
  - {lower: NOT_DISTINGUISHED, higher: NOT_DISTINGUISHED, point_target_assessment: not_supported, method_review_direction: range_or_nonpoint}
  - {lower: NOT_DISTINGUISHED, higher: UNAVAILABLE, point_target_assessment: unable_to_determine, method_review_direction: null}
  - {lower: UNAVAILABLE, higher: DISPLACES_REFERENCE, point_target_assessment: unable_to_determine, method_review_direction: null}
  - {lower: UNAVAILABLE, higher: ADJACENT_MATERIALLY_WORSE, point_target_assessment: unable_to_determine, method_review_direction: null}
  - {lower: UNAVAILABLE, higher: NOT_DISTINGUISHED, point_target_assessment: unable_to_determine, method_review_direction: null}
  - {lower: UNAVAILABLE, higher: UNAVAILABLE, point_target_assessment: unable_to_determine, method_review_direction: null}
maximum_registered_cells: 777
rerun_after_results: PROHIBITED
-->

No data is acquired and no study is executed in the charter PR. Execution may begin only after the
charter merges, the charter-pinned SHA-256 values verify against committed raw file bytes, and all
required pre-execution data gates pass.

## 1. Decision question and non-question

The sole question is:

> Does preregistered historical evidence reject the continued plausibility of any
> historical/provisional Level-1 investable-sleeve scenario strongly enough to require a separate
> policy review before replacement sizing, or is the evidence insufficient?

The study does not ask which weight maximizes return, which sleeve should automatically receive
capital, or what any final portfolio weight should be. It does not optimize, rank policy outcomes,
construct a whole portfolio, reconcile 100%, or assign a residual.

## 2. Authority and lifecycle

Controlling boundaries are the Investment Constitution, `GOV-0002`, `GOV-0003`, `OPS-0009`,
`OPS-0014`, `NUM-0001`, effective merged `XASSET-0019`, and frozen research-only `LEVEL2-0001`.
`XASSET-0016` and `XASSET-0018` are historical/mechanical provenance only where `XASSET-0019`
preserves them. `MARGIN-0005` and `LADDER-0001` supply hash, manifest, no-lookahead, trial-accounting,
and bounded-study precedent; neither expands this study into margin or ladder research.

The exact lifecycle is:

`RISK-0001 charter -> charter merge/hash verification -> one authorized data/acquisition/
implementation/results PR -> independent exact-head results review -> principal acceptance/research
merge -> separate replacement Level-1 methodology/policy decision`.

Results never change weights. The later implementation/results PR may acquire and validate data,
execute registered cells once, and report results. It may not mutate production configuration.

## 3. Early-RISK boundary

This is an early sleeve-level challenge, not a portfolio backtest. It does not construct a portfolio,
reconcile 100%, assign residual capital, define cash, select final Level-2 membership, or size
instruments. The preserved downstream order is:

`early RISK -> replacement Level-1 method/provisional sizing -> final Level-2 membership -> Level-2
sizing -> non-adopted candidate 100% reconciliation -> full-portfolio unlevered stress`.

Margin, leverage, debt reduction, and liability-flow controls remain downstream of adopted unlevered
construction. CASH, RESERVE, legacy `cash_reserve`, debt reduction, and unassigned/residual capital
have no representation or proxy in this study.

## 4. Frozen study universe

Exactly four investable families are examined:

1. **EQUITY** — the 27-name `LEVEL2-0001` equity cohort. Before Level-2 internal weights exist, only
   constituent diagnostics are lawful. No equal-weight, market-cap-weight, current-weight, or
   synthetic aggregate equity path may be built.
2. **FUND_BROAD_MARKET** — SPY, VEA, and VWO remain separate representations. No blended series is
   allowed.
3. **FUND_GLD_DEFENSIVE** — GLD is core. IAU, SGOL, and GLDM may enter only as conditional
   representation sensitivity after every preregistered identity, data-quality, and parity gate
   passes. There is no peer ranking or final vehicle selection.
4. **CRYPTO** — BTC, ETH, and SOL remain separate spot representations. No equal-weight,
   market-cap, conviction, or canonical crypto composite is allowed; no staking, lending, or yield is
   modeled.

The structured file freezes exact identities and counts.

## 5. Historical references and scenario construction

The old figures—equity 18.67%, broad market 14.67%, GLD defensive 16.67%, and crypto 16.67%—appear
only as `historical_provisional_reference`. They are historical, computationally derived under
superseded mechanics, provisional, economically unvalidated, not adopted, not baseline policy, not
targets, not optimization anchors, and imply no residual treatment.

Each family has three states: `LOWER`, `HISTORICAL_REFERENCE`, and `HIGHER`. LOWER and HIGHER are a
new symmetric 20% relative perturbation of the historical reference, rounded half-up to two decimal
percentage points. The exact values in `pre_registration.yaml` are frozen before acquisition or
execution.

This 20% perturbation is a `NUM-0001` provisional governance guardrail for this study only. It is not
calibrated, evidence-bounded, optimized, or inherited from XASSET-0016's retired R2/R3 ±2pp effect.
It was selected to apply the same relative challenge to every family without a grid search. It lapses
automatically when the authorized study ends and may not be reused without new authority.

No scenario is a portfolio target. “Percent exposure” is an analytical scale applied separately to
each representation or constituent diagnostic; the study does not say what occupies the rest of an
asset state.

## 6. Result vocabulary and total reduction

Only these family result states exist:

- `provisional_scenario_not_rejected`: the historical reference was not rejected by the dominance
  rule. This is not validation, calibration, policy support, or adoption.
- `policy_review_required`: an adjacent registered scenario dominates the historical reference under
  the preregistered rule. It requires a separate review; it changes nothing automatically.
- `unable_to_determine`: a required data, eligibility, breadth, corporate-action, or representation
  gate prevents a direction.

Where valid, `review_direction` is `lower_exposure`, `higher_exposure`, or `null`.
`point_target_assessment` is `not_supported`, `not_rejected`, or `unable_to_determine`.
`method_review_direction` is `range_or_nonpoint` or `null`. Representation conflict is never averaged
away.

For each candidate direction, every registered voting metric is classified against the historical
reference as `IMPROVES`, `EQUIVALENT`, `WORSENS`, or `UNAVAILABLE`; a lawful pre-inception
conditional window is `NOT_APPLICABLE` and is excluded. Direction and exact metric-specific
tolerances come from the closed registry. Within a metric and then within a family, precedence is
`WORSENS`, `UNAVAILABLE`, `IMPROVES`, `EQUIVALENT`. Thus one worsening vetoes an otherwise favorable
family, and missing mandatory evidence can never become non-rejection.

The three voting families are exactly `PATH_RISK`, `RECOVERY`, and `OPPORTUNITY_COST`. A direction is
`POLICY_REVIEW_REQUIRED` only when none worsens or is unavailable/conflicted and at least two improve.
If all three are available, improvement and worsening are not mixed, and that rule is not met, the
direction is `CENTER_NOT_REJECTED`. Missing, mixed, conflicted, or formula-integrity evidence is
`UNABLE_TO_DETERMINE`. The nine-row directional table reduces LOWER and HIGHER to the published
result and review direction. A separate exhaustive 16-row point-evidence table reduces whether each
adjacent state displaces the reference, is materially worse, is not distinguished, or is unavailable.

## 7. Data-acquisition authority and chronology

The one later implementation/results PR may perform bounded acquisition and validation before trial
execution. The charter PR may not acquire data. Every request must produce a redacted request receipt,
UTC timestamp, response status, page/cursor and terminal pagination marker, raw hash, transformed
hash, coverage, expected/observed counts, gap inventory, identity lineage, corporate-action
disposition, provider/endpoint, license/provenance, and commit-or-quarantine disposition.

Provider fallback follows the structured order and may occur only before registered execution.
Fallback attempts remain logged. A provider may not be changed after results are inspected. A path is
never silently stitched from providers; an affected representation/window uses one disclosed source
or abstains. Secondary sources reconcile; they do not silently replace an input.

Repository licensing policy is unchanged. Alpaca-derived data may be committed only where existing
terms, size, and repository precedent permit. Yahoo and Coinbase fallback payloads are quarantined
and hash-pinned, not committed. Official FRED DFF may be committed as public-domain source material
or retained through a hash-pinned acquisition receipt.

## 8. Exact sources and fallbacks

Equity and ETF primary bars use Alpaca Market Data v2 daily SIP split-adjusted bars. If a complete
representation/window cannot lawfully pass there, the entire affected path may use the preregistered
Yahoo chart fallback, quarantined, with raw close/events construction. Adjusted close is
reconciliation-only.

Crypto primary bars use Alpaca v1beta3 U.S. crypto daily spot bars. Coinbase Exchange daily candles
are the only input fallback and must cover the entire affected representation/window. The opposite
provider may be used for reconciliation. No undisclosed source stitching is allowed.

DFF from official FRED is the only opportunity-cost input. There is no analytical fallback. A missing
DFF input makes affected opportunity-cost cells ineligible; ^IRX or another cash proxy may be retained
only as disclosed reconciliation and is never strategic cash or a fifth sleeve.

Corporate actions use Alpaca v1 records first and SEC/issuer primary evidence for identity, ratio,
entitlement, ticker, spin, and merger resolution. An unresolved period is null, not guessed.

## 9. Total-return construction

Equities and ETFs use one primary method only: split-adjusted, non-total-return prices plus explicit
gross declared cash dividends and explicit corporate actions. A total-return/adjusted-close series may
be quarantined for validation but is never combined with explicit dividends. GLD and gold-peer market
paths already reflect fund expense drag; no expense ratio is subtracted again. Crypto is spot-only.

Dividend cash is credited on the ex-date for the primary path; a pay-date sensitivity may be disclosed
but cannot create an unregistered decision cell. Splits require continuity checks. Spin-offs, ticker
changes, mergers, and legal-entity continuity require explicit evidence.

No synthetic predecessor history is stitched. Specifically: CEG has no pre-standalone history; GEV
has no pre-spin history; RKLB before 2021-08-25 is not RKLB history; RTX predecessor history is not
silently stitched. Unresolved identity/action periods are `CORPORATE_ACTION_UNRESOLVED`.

## 10. Two-stage data gate and missingness

Stage A is the global study-integrity gate. A charter/protocol/preregistration hash mismatch, schema
failure, trial-inventory defect, runner/config identity failure, source-hierarchy drift, global
code/version failure, incomplete study-wide provenance, or incomplete pre-execution eligibility
matrix halts the study and permits zero cells to execute.

Stage B is cell/data eligibility. Source, receipt, coverage/gap, identity/action, total-return,
representation/window-quality, or comparator failures mark only the deterministic cells or metrics
that depend on that input ineligible. All acquisition, validation, and eligibility states are frozen
before the first cell. A SOL gap affects intersecting SOL cells; VEA acquisition failure affects all
VEA cells; an unresolved CEG action affects intersecting CEG cells; a missing required DFF observation
makes affected opportunity-cost metrics unavailable. A conditional gold peer failing admission is
excluded, while an admitted peer that later becomes unavailable propagates `UNAVAILABLE`. No runtime
discretion may promote a cell failure into a global halt or conceal it as sufficient evidence.

The runner may not invent a substitute, silently reduce the universe, treat a missing observation as
zero, interpolate prices, or forward-fill prices.

The closed cell states are `ELIGIBLE`, `NOT_APPLICABLE_PRE_INCEPTION`, `MISSING_SOURCE_DATA`,
`KNOWN_DATA_GAP`, `CORPORATE_ACTION_UNRESOLVED`, `CONDITIONAL_ASSET_NOT_ACQUIRED`, and
`QUALITY_GATE_FAILED`.

Every result table must show eligible versus expected/frozen count, missing and pre-inception names,
censored recoveries, the selection-conditioned-cohort warning, and corporate-action truncations.
Current 27-name equities are not represented as the historical opportunity set.

## 11. Crypto-specific gates

Crypto acquisition requires request and page receipts, terminal pagination proof, UTC normalization,
an expected-day inventory, zero duplicate timestamps, positive and internally valid OHLC, contiguous
gap blocks, and one completed bar for every UTC day in an eligible registered window. The permitted
missing-day and contiguous-gap thresholds are both zero. There is no interpolation, forward fill,
pre-inception fabrication, or undisclosed alternate-source stitch.

The existing SOL aggregate gap must be re-inventoried. Every registered SOL window intersecting an
unresolved day is `KNOWN_DATA_GAP` and ineligible. The crypto family may not average BTC/ETH evidence
over that conflict or silently omit SOL.

Both asset-available-history and lawful complete-common-window analyses are required where eligible.
Drawdown, recovery, fixed stress, opportunity cost, loss contribution, and representation consistency
are reported separately for BTC, ETH, and SOL.

## 12. Cross-asset alignment

Equities and ETFs use official XNYS sessions and closes. Crypto remains a native 24/7 UTC series. The
common comparison timestamp is each official XNYS close in America/New_York. At each such timestamp,
crypto maps only the latest completed UTC daily close at or before the timestamp. Completed weekend
crypto returns not yet mapped are compounded into the next eligible XNYS interval. A future crypto
observation is never mapped backward.

DFF accrues for the exact calendar days between common evaluation timestamps. Native equity/ETF and
crypto paths are retained separately from aligned comparisons. A missing observation is never a zero
return.

## 13. Analytical comparator

DFF is analytical opportunity cost only—not strategic cash, residual, a funding destination, a fifth
sleeve, or policy. It is treated as an annual percent rate. The registered one-business-day lag is
measured from the DFF observation date on the U.S. Federal Reserve Bank business-day calendar; the
observation becomes lawful at 23:59:59 America/New_York on the business date one registered lag day
after that observation date. At an evaluation timestamp the lookup takes the latest observation whose
lawful availability timestamp is at or before the evaluation timestamp. The daily factor is
`1 + (lagged DFF / 100) / 360`, compounded by calendar day. Weekends and holidays use that same
latest lawfully available observation and never perform a forward lookup. The former arbitrary
seven-day tolerance is removed: zero missing required lawfully lagged DFF observations are allowed. Any missing
required observation makes the affected opportunity-cost metric unavailable; no rate is inferred
from future data.

## 14. Windows and held-out language

There are exactly seven window classes and an exact evaluation end of 2026-07-31. The structured file
freezes dates and external/calendar criteria for bounded asset-available history, family-common
overlap, the NBER-defined GFC recession interval, calendar Q4 2018, a predeclared COVID public-health
shock interval, calendar 2022 rate/inflation shock, and the predeclared 2022 Terra/Celsius/FTX crypto
stress interval.

No asset-specific ex-post peak/trough window may be selected. These known events are described as
`preregistered historical replay`, never untouched or prospectively held out. “Protocol-held-out” is
permitted only for genuinely sequestered bytes proven by hash. “Prospective” applies only to future
observations unavailable at freeze.

## 15. Closed metric-to-family map

The study reports no composite score. Every metric has exactly one canonical family, formula,
preference direction, unit, tolerance reference, research-unit/window applicability, voting status,
and missing-result rule in the preregistration. No metric can migrate between families or vote twice.

Path/risk includes maximum drawdown, worst calendar month, worst calendar quarter, fixed stress-window
loss, and annualized volatility. Recovery includes calendar-day recovery duration, recovery/censor
status, and time-underwater area. Opportunity cost is total return relative to compounded lagged DFF.
The three voting paths are defined rather than merely referenced: exposure-scaled drawdown loss is
scenario exposure × absolute max drawdown × 100 percentage points; exposure-scaled stress loss is
scenario exposure × max(0, −stress return) × 100; exposure-scaled underwater burden is scenario
exposure × underwater-area days × 100; and exposure-scaled excess contribution is scenario exposure
× (asset total return − DFF total return) × 100. These formulas fix sign and unit. Raw path metrics,
constituent envelopes, representation checks, and co-behavior remain diagnostic or veto gates, not
extra improvement votes.

Equity adds only cross-sectional diagnostics: eligible breadth counts/proportions, median, P10/P25/
P75/P90, range and dispersion, governed-cluster dispersion, pairwise co-behavior, leave-one-out
sensitivity, and per-constituent loss envelopes. These are not an aggregate sleeve return.

Pairwise Pearson correlation and joint-negative-interval frequency are diagnostics only. They do not
create a new dominance family or a whole-portfolio diversification claim.

## 16. Family-specific interpretation

### Equity

Every return, drawdown, recovery, volatility, stress loss, opportunity-cost, and contribution result
is computed per constituent. The authoritative reducer accepts the exact frozen 27 identities in
canonical order and derives the eligible set, eligibility count, categorical median, and directional
breadth from those constituent states; caller summaries cannot control the result. It then requires
one leave-one-out state for each eligible omitted identity, in canonical order, with no empty,
truncated, duplicate, unknown, or omitted identity set. Family direction requires at least 21 eligible
constituents, at least 75% directional breadth, an agreeing derived median, and direction stable under
every required leave-one-out diagnostic. No aggregate path is lawful.

### Broad market

SPY, VEA, and VWO remain separate. All three are required for family direction. A material directional
difference or conflict makes the family `unable_to_determine`; there is no blended broad-market sleeve.

### GLD defensive

GLD may be evaluated standalone for total return behavior, drawdown, recovery, fixed stress,
opportunity cost, and exposure-scaled loss contribution. It supports no whole-portfolio
diversification claim, final vehicle selection, or final weight. IAU/SGOL/GLDM enter only after the
conditional identity, gap, action, correlation, return-parity, and drawdown-parity evidence is supplied
and independently checked against the registry. They are the only permitted peers; duplicate,
out-of-order, or arbitrary identities are rejected. A failed peer is excluded, while an admitted peer
must be available and agree with GLD or the result becomes unavailable/conflict.

### Crypto

BTC/ETH/SOL remain separate. Both asset-available and family-common evidence must be eligible for a
family direction. All representation directions must agree. Gap or directional conflict makes the
family unable to determine.

## 17. Family, representation, and policy-review reduction

Candidate LOWER or HIGHER is compared only with the same family's historical reference. The two
history windows are mandatory voting evidence; fixed stresses are conditional voting evidence where
lawfully applicable. Within each metric and family the closed precedence rule above applies. Multiple
correlated metrics inside one family count once. A candidate dominates only if no mandatory family
worsens, conflicts, or is unavailable and at least two distinct families strictly improve.

SPY/VEA/VWO and BTC/ETH/SOL are all mandatory: any unavailable representation makes that family
unavailable, and non-identical lawful states are conflict. GLD controls the gold-family result until a
peer passes every admission gate; a failed conditional peer is excluded, but every admitted peer must
remain available and match GLD or the result is unavailable/conflict. Equity requires 21 eligible
constituents, 75% breadth for one state, an agreeing median, and every leave-one-out result unchanged;
failure is unavailable or conflict, never an aggregate return calculation.

The production mapper validates exact closed family, metric, representation, scenario, window,
missingness, directional, and point-state vocabularies before reduction. It obtains every threshold
from the validated canonical preregistration; its public APIs accept evidence, not governance values.
The exact loss and opportunity contribution tolerance is 1.00 percentage point; exposure-scaled
underwater burden uses 30.00 percentage-point-days. Equality at a tolerance is equivalence, and only
a difference strictly beyond it changes direction. The registry also freezes the 21/75% equity gate,
zero crypto missing days, contiguous gaps, and duplicate UTC timestamps, gold parity thresholds and
zero unresolved gold-peer session gaps, DFF actual/360 convention, zero DFF missing observations,
the registered one-business-day DFF lag, two-decimal `ROUND_HALF_UP` scenario convention, the exact
absolute formula-integrity tolerance of 0.000001 output units, and minimum two improvement families.
Every selected constant is separately classified under `NUM-0001` and records supporting evidence,
canonical source, duplicate and fallback locations, hardcoded/config-editable status, binding status,
basis/scope/lapse/reuse, and calibration/evidence status; mathematical counts are
separately identified as derived rather than free parameters.

Monotonicity/formula integrity is recomputed from raw metric values and registered LOWER/reference/
HIGHER exposure values with Decimal arithmetic for all
exposure-scaled voting metrics. A failure makes the direction unable to determine; it is never
repaired after results are visible.

Conflict produces `unable_to_determine`. A `policy_review_required` result initiates only a separate
future review; it never changes policy automatically.

## 18. Closed point-target challenge

The nine-row directional table covers every LOWER/HIGHER directional pair. Exactly one direction
requiring review produces `policy_review_required` in that direction; both directions requiring
review produce `unable_to_determine`, with no selector. Separately, each direction becomes point
evidence `DISPLACES_REFERENCE`, `ADJACENT_MATERIALLY_WORSE` (at least two worsening families and no
improvement), `NOT_DISTINGUISHED`, or `UNAVAILABLE`. The exhaustive 16-row point table makes any
unavailability unable to determine; any displacement makes the point not supported; at least one
materially worse adjacent state with no displacement leaves the point not rejected; and two
undistinguished adjacent states make point precision not supported with `range_or_nonpoint`. This
exhausts the lawful state space and prevents a discretionary fallback.

The study may emit `range_or_nonpoint` as a future method-review direction. It may not create the
replacement method.

## 19. Trial accounting

There are 37 authorized representations for inventory purposes: 27 equity constituents, three broad
funds, GLD plus three conditional gold peers, and three crypto assets. Three scenario states and seven
window classes produce the derived ceiling `37 × 3 × 7 = 777` registered cells. This is an inventory
ceiling, not a tunable budget.

One representation × scenario × window × exact configuration hash × exact data-hash bundle is one
cell. Metrics computed from one path are not separate trials. Failed, discarded, conditional,
pre-inception, and ineligible attempts remain in the ledger. There are zero reserve trials. Unused
capacity lapses and is not reallocated. No post-result cell may be added without a charter amendment.

## 20. Reruns

Default: no rerun after results are observed. A rerun requires a separately accepted charter
amendment or new RISK study and either a material new evidence regime or a separately governed
integrity correction. Discovering a defect does not silently authorize a rerun. Preregistered
fallback retries may occur before registered execution and must be logged.

## 21. Future implementation/results PR deliverables

The one authorized later PR must contain exactly the bounded acquisition receipts, data manifest,
raw/transformed hashes, coverage report, eligibility matrix, committed/quarantined inventory,
deterministic runner, trial ledger, focused tests/validators, per-representation and window results,
dominance/conflict disposition, limitations/survivorship report, final research disposition record,
and proof of protocol/preregistration hash identity.

It must not change production configuration, targets, holdings, gates, issuer look-through,
allocator/execution code, margin code or doctrine, numeric-sizing records/validators, Level-2
evidence, sealed Intelligence, profiles, relationships, or policy-adoption records.

## 22. Absolute prohibited scope

Final Level-1 targets; final Level-2 membership or weights; optimizer/grid search; composite scores;
residual redistribution; strategic cash; debt/margin/leverage; chart/technical signals; trades/orders;
allocator, `targets.yaml`, or `holdings.yaml` mutation; automatic adoption; unregistered trials;
automatic reruns; whole-portfolio construction; whole-100% reconciliation; and residual proxies are
all prohibited.

## 23. Drift prevention and hash rule

The 18.67/14.67/16.67/16.67 figures remain historical reference scenarios only. The former six-way
16.67 baseline and R2/R3 ±2pp have no future sizing authority. Any numerical coincidence in this
study is a new one-study assumption, not inherited authority. Non-rejection is not validation;
policy review is not automatic change; conflicts are not averaged; residual is absent; and no cash,
debt, or margin implication exists.

The charter pins SHA-256 over raw committed bytes for this file and `pre_registration.yaml`. The
later PR must prove exact identity before acquisition or execution. Any content change after charter
merge requires separate governance and a new pin; silent editing voids execution authority.
