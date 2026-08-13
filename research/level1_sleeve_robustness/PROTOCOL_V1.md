# Level-1 Investable-Sleeve Robustness Study — Protocol V1

Status: frozen governance protocol for `RISK-0001`. This file and
`pre_registration.yaml` authorize nothing independently. The charter is the authority, and the
structured preregistration is canonical for every closed value, vocabulary, threshold, source,
window, and trial count. If this narrative and the structured file differ, execution must stop and a
separate governance correction is required.

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

## 6. Result vocabulary

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

## 10. Data gate and missingness

No registered study cell executes until every required core dataset has passed its gates. Failure
makes affected cells ineligible, preserves null/abstention, and may force a family result to
`unable_to_determine`. The runner may not invent a substitute, silently reduce the universe, treat a
missing observation as zero, interpolate prices, or forward-fill prices.

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
sleeve, or policy. It is treated as an annual percent rate, with a one-U.S.-business-day availability
lag. The daily factor is `1 + (lagged DFF / 100) / 360`, compounded by calendar day. Weekends and
holidays use the most recently lawfully available lagged rate. A source gap over seven calendar days
fails affected opportunity-cost cells; no rate is inferred from future data.

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

## 15. Metrics

The study reports no composite score. Exact formulas and annualization conventions are closed in the
preregistration.

Path/risk includes maximum drawdown, worst calendar month, worst calendar quarter, fixed stress-window
loss, and annualized volatility. Recovery includes calendar-day recovery duration, recovery/censor
status, and time-underwater area. Opportunity cost is total return relative to compounded lagged DFF.
Contribution metrics scale losses or excess return by the registered analytical exposure.

Equity adds only cross-sectional diagnostics: eligible breadth counts/proportions, median, P10/P25/
P75/P90, range and dispersion, governed-cluster dispersion, pairwise co-behavior, leave-one-out
sensitivity, and per-constituent loss envelopes. These are not an aggregate sleeve return.

Pairwise Pearson correlation and joint-negative-interval frequency are diagnostics only. They do not
create a new dominance family or a whole-portfolio diversification claim.

## 16. Family-specific interpretation

### Equity

Every return, drawdown, recovery, volatility, stress loss, opportunity-cost, and contribution result
is computed per constituent. Family direction requires at least 21 eligible constituents, at least
75% directional breadth, an agreeing cross-sectional median, and direction stable under every
leave-one-out diagnostic. No aggregate path is lawful.

### Broad market

SPY, VEA, and VWO remain separate. All three are required for family direction. A material directional
difference or conflict makes the family `unable_to_determine`; there is no blended broad-market sleeve.

### GLD defensive

GLD may be evaluated standalone for total return behavior, drawdown, recovery, fixed stress,
opportunity cost, and exposure-scaled loss contribution. It supports no whole-portfolio
diversification claim, final vehicle selection, or final weight. IAU/SGOL/GLDM enter only after the
conditional parity gates pass; any material conflict then makes the family unable to determine.

### Crypto

BTC/ETH/SOL remain separate. Both asset-available and family-common evidence must be eligible for a
family direction. All representation directions must agree. Gap or directional conflict makes the
family unable to determine.

## 17. Dominance and policy-review rule

Candidate LOWER or HIGHER is compared only with the same family's historical reference. Three
independent mandatory families exist: downside path, recovery burden, and opportunity cost. A
candidate dominates only if it is not materially worse in every applicable mandatory family and is
strictly better in at least two distinct families. Multiple correlated metrics inside one family
count once. Representation consistency is a veto, not a fourth improvement count.

The exact 1.00pp contribution tolerances, 30-day recovery tolerance, 10pp equity-breadth tolerance,
and other closed thresholds are uncalibrated one-study `NUM-0001` provisional guardrails. Equality
inside a tolerance is equivalence, not improvement. Monotonicity is required only where exposure
scaling makes it mathematical—loss and opportunity contributions—not for raw return paths.

Conflict produces `unable_to_determine`. A `policy_review_required` result initiates only a separate
future review; it never changes policy automatically.

## 18. Point-target challenge

The study separately asks whether history supports point precision. `not_supported` means eligible
evidence cannot distinguish the reference from both adjacent states or indicates a range/nonpoint
method should be considered. `not_rejected` means the point premise survives the closed rule and at
least one adjacent state is materially worse without conflict; it is not validation. Failed gates or
conflicts produce `unable_to_determine`.

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
