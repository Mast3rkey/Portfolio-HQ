---
decision_id: RISK-0001
date: 2026-08-13
status: Proposed
category: research_charter
related_decisions: [GOV-0001, GOV-0002, GOV-0003, OPS-0009, OPS-0014, NUM-0001, XASSET-0016, XASSET-0018, XASSET-0019, LEVEL2-0001, MARGIN-0005, LADDER-0001]
supporting_artifact: research/level1_sleeve_robustness/PROTOCOL_V1.md
file: governance/decisions/RISK-0001-level1-investable-sleeve-robustness-charter.md
---

## Context

### Live preflight and identifier

This Lane-G filing began only after a live `git pull` and full preflight. GitHub `main`, local
`main`, `origin/main`, and local HEAD all matched
`0962385bf6b1b72cebe8b326da49927977db2912`, the merge commit of PR #313, “XASSET-0019:
amend Level 1 architecture.” PR #313 was independently re-opened read-only and confirmed merged
from exact head `df2cb58c38a87888c476af0743884b8377b354e5` at 2026-08-13T17:40:36Z; its
exact-head CI was complete/successful. The open-PR inventory was empty.

The primary checkout contained only the pre-existing untracked `.worktrees/` and `AGENTS.md`
paths; both are preserved and excluded from this change. Registered additional worktrees were
inspected. They were clean historical/review artifacts associated with already-merged, closed, or
detached work, not live mutation PRs; no overlapping RISK branch or open mutation lane existed.

`RISK-0001` had zero hits in the decision directory, decision catalog, tracked repository, local or
remote branch names, and open PR inventory at mutation time. The catalog and decision directory each
contained exactly 117 decisions and reconciled one-to-one. `RISK-0001` is therefore the first and
correct identifier for the distinct early empirical-risk domain; no prompt-reserved identifier was
assumed without that verification.

`operations/WORKSTREAMS.yaml` correctly retained historical gates but its cached live fields still
named PR #313 and pre-merge main. This filing updates only current factual fields and adds lifecycle
gates; it does not rewrite historical gates.

### Controlling architecture

Effective merged `XASSET-0019` establishes four investable Level-1 sleeves: `equity`,
`fund_broad_market`, `fund_gld_defensive`, and `crypto`. It classifies `debt_reduction` as a
`LIABILITY_FLOW_CONTROL`, leaves CASH/RESERVE and legacy `cash_reserve` unresolved for later
liquidity-role work, and preserves residual capital as `UNSIZED_UNASSIGNED_CAPITAL` with no return,
risk, cash, benchmark, or debt proxy.

It also makes the old six-way 100/6 baseline and R2/R3 ±2pp effect historical only. The current
18.67% / 14.67% / 16.67% / 16.67% investable-sleeve outputs remain reproducible but provisional,
economically unvalidated, not adopted, and barred from future sizing authority. `LEVEL2-0001`
freezes 27 equities, SPY/VEA/VWO, GLD, and BTC/ETH/SOL for research only; it creates no final
membership or Level-2 sizing authority.

This charter is the separate early-RISK authority `XASSET-0019` requires. It challenges rather than
ratifies those historical scenarios, before replacement Level-1 sizing or final Level-2 work.

### Data-readiness basis

Repository-native MARGIN-0005 infrastructure already demonstrates acquisition receipts, raw and
transformed hashes, pagination, no-lookahead checks, quarantined secondary data, point-in-time
dividends/actions, manifests, and DFF handling. Its current cache does not itself satisfy this study:
23 of 27 equities have short local histories; ICE, SNPS, SPGI, and WM are absent; VEA/VWO and long
GLD history are absent; IAU/SGOL/GLDM are absent; BTC/ETH are usable for the shorter window; SOL has
a material aggregate gap; and long stress histories are largely absent. Cross-asset alignment,
breadth, a RISK-specific ledger, and validators do not yet exist. These are acquisition and
implementation needs for the one later PR—not work performed by this charter filing.

## Decision

### 1. Exact question and authority granted

`RISK-0001` adopts and hash-pins the protocol and closed preregistration named below. It authorizes
exactly one later, separate implementation/results PR to:

1. perform the preregistered bounded data acquisition and validation;
2. execute each eligible registered study cell once under the exact pinned configuration;
3. retain failed, ineligible, discarded, and conditional attempts in the trial ledger; and
4. report the closed family dispositions without changing policy.

The sole decision question is:

> Does preregistered historical evidence reject the continued plausibility of any
> historical/provisional Level-1 investable-sleeve scenario strongly enough to require a separate
> policy review before replacement sizing, or is the evidence insufficient?

This charter does not ask which weight maximizes return, which sleeve should automatically receive
capital, or what any final portfolio weight should be.

This charter PR performs no data acquisition, creates no market-data cache, executes no registered
cell, inspects no study result, and produces no research result.

### 2. Canonical protocol and hash pins

The canonical files were finalized before the following hashes were computed. SHA-256 is computed
over raw file bytes exactly as committed:

- `research/level1_sleeve_robustness/PROTOCOL_V1.md`:
  `f4c08e66ca0f38affb3fddcd0fbe8ac0a095b9756648f87d626f419dcbc7a925`
- `research/level1_sleeve_robustness/pre_registration.yaml`:
  `fd7fcf47bab02366a5804aa5546caee8907ad177e62c353775989c333a11b59f`

The structured preregistration is canonical for all closed identities, sources, fallbacks, windows,
thresholds, vocabularies, metrics, and counts. The protocol explains the design but cannot enlarge or
override the YAML. The later PR must verify both exact hashes from the merged charter commit before
data acquisition or execution. Any content change requires a separately accepted governance
amendment with new pins. A mismatch voids execution authority.

### 3. Frozen universe and representation boundary

Exactly four investable families are authorized:

- **EQUITY:** the 27-name `LEVEL2-0001` equity cohort, constituent diagnostics only. No aggregate
  sleeve return exists before Level-2 internal weights.
- **FUND_BROAD_MARKET:** SPY, VEA, and VWO as three separate representations. No combined series.
- **FUND_GLD_DEFENSIVE:** GLD core; IAU, SGOL, and GLDM only as conditional representation
  sensitivity after all preregistered parity gates pass. No ranking or vehicle selection.
- **CRYPTO:** BTC, ETH, and SOL separately. No composite or internal weighting assumption.

CASH, RESERVE, legacy `cash_reserve`, debt reduction, residual/unassigned capital, margin, leverage,
and whole-portfolio construction are excluded.

### 4. Historical-reference treatment

The historical values are present only under the exact classification
`historical_provisional_reference`: equity 18.67%, broad market 14.67%, GLD defensive 16.67%, and
crypto 16.67%. They are historical, computationally derived under superseded future mechanics,
provisional, economically unvalidated, not adopted, not baseline policy, not targets, not
optimization anchors, and imply no residual assignment.

The old six-way 16.67% baseline has no current sizing authority. The old R2/R3 ±2pp effect has no
current numeric sizing authority.

### 5. Scenario construction and NUM-0001 provenance

Each family has exactly `LOWER`, `HISTORICAL_REFERENCE`, and `HIGHER`. LOWER and HIGHER are a new
one-study symmetric 20% relative perturbation, rounded half-up to two decimals:

| Family | LOWER | HISTORICAL_REFERENCE | HIGHER |
|---|---:|---:|---:|
| EQUITY | 14.94% | 18.67% | 22.40% |
| FUND_BROAD_MARKET | 11.74% | 14.67% | 17.60% |
| FUND_GLD_DEFENSIVE | 13.34% | 16.67% | 20.00% |
| CRYPTO | 13.34% | 16.67% | 20.00% |

This is a `NUM-0001` provisional governance guardrail and research assumption for one study. It is
not calibrated, evidence-bounded, optimized, or inherited from XASSET-0016. A common proportional
perturbation applies the same relative challenge without adopting a fixed percentage-point increment
or searching a grid. The values are frozen before acquisition/result inspection, lapse automatically
after the study, and cannot be reused without new authority. They are analytical exposure scales,
not portfolio targets; no destination for the remainder is specified or implied.

### 6. Closed result and point-target vocabulary

The only result states are:

- `provisional_scenario_not_rejected` — the historical reference was not rejected; non-rejection is
  not validation, calibration, support, or adoption;
- `policy_review_required` — an adjacent scenario dominates under the closed rule; a separate policy
  review is required and no automatic change occurs; and
- `unable_to_determine` — data, eligibility, breadth, corporate-action, or representation conflict
  prevents a direction.

`review_direction` is `lower_exposure`, `higher_exposure`, or `null`.
`point_target_assessment` is `not_supported`, `not_rejected`, or `unable_to_determine`.
`method_review_direction` is `range_or_nonpoint` or `null`. The study may suggest that a future method
consider a range/nonpoint representation but may not create that replacement method.

### 7. Data sources, fallbacks, receipts, and disposition

The exact source hierarchy is frozen in the preregistration:

- equities/ETFs: Alpaca v2 daily SIP split-adjusted bars; whole-path Yahoo chart fallback,
  quarantined;
- crypto: Alpaca v1beta3 daily spot bars; whole-path Coinbase Exchange fallback, quarantined;
- opportunity-cost comparator: official FRED DFF, with no analytical substitute;
- actions/identity: Alpaca v1 corporate actions, then SEC/primary issuer evidence; and
- secondary sources: reconciliation only, never silent substitution.

Every acquisition requires provider/endpoint, redacted request and pagination receipts, UTC
timestamps, raw/transformed hashes, coverage, expected/observed counts, gaps, identity lineage,
corporate-action treatment, provenance/licensing, and commit/quarantine disposition. Repository
licensing policy is unchanged. Fallback retries are allowed only before registered execution and must
be logged; no source may be changed after results are seen.

### 8. Data and crypto gates

No registered cell executes until all required data gates pass. A failure makes affected cells
ineligible, preserves null/abstention, and never authorizes substitute data, a silent universe
reduction, interpolation, forward fill, zero-return treatment, or a future observation mapped
backward.

Crypto requires complete page receipts, terminal pagination, UTC normalization, daily expected-day
inventory, zero duplicates, positive/internal OHLC validity, and zero missing expected UTC days in an
eligible registered window. The existing SOL gap must be re-inventoried; every intersecting window is
`KNOWN_DATA_GAP` and ineligible. BTC/ETH evidence may not average away or silently replace SOL.

The exact missingness states are `ELIGIBLE`, `NOT_APPLICABLE_PRE_INCEPTION`,
`MISSING_SOURCE_DATA`, `KNOWN_DATA_GAP`, `CORPORATE_ACTION_UNRESOLVED`,
`CONDITIONAL_ASSET_NOT_ACQUIRED`, and `QUALITY_GATE_FAILED`.

### 9. Return, action, comparator, and alignment rules

Equities and ETFs use split-adjusted non-total-return prices plus explicit gross dividends and
corporate actions. Total-return/adjusted-close data is reconciliation-only and never combined with
explicit dividends. Gold-fund market paths already reflect expense drag; no expense ratio is
subtracted again. Crypto is spot-only with no staking, lending, or yield.

No predecessor stitching is allowed. CEG pre-standalone and GEV pre-spin history are unavailable;
pre-2021-08-25 is not RKLB history; RTX predecessor history is not silently treated as RTX. Ticker
change, spin-off, merger, entitlement, and legal-entity continuity require explicit evidence or the
affected period is unresolved/null.

DFF is analytical opportunity cost only—not cash, residual, a destination, a fifth sleeve, or policy.
It uses a one-U.S.-business-day availability lag and simple actual/360 daily accrual compounded over
calendar days. Gaps over seven calendar days fail affected comparator cells.

Equity/ETF observations use official XNYS sessions and closes. Crypto remains 24/7 UTC; at each XNYS
close only the latest completed UTC daily close at or before that timestamp may map. Weekend crypto
returns compound into the next eligible exchange interval. No future observation maps backward and no
missing observation is zero.

### 10. Exact preregistered windows

There are seven window classes ending 2026-07-31:

1. bounded asset-available history: 2004-11-18 through 2026-07-31, intersected with lawful inception
   and validated coverage;
2. family-common overlap, with exact family starts: equity 2024-04-02, broad market 2007-07-20,
   GLD defensive 2018-06-26, crypto 2021-06-01;
3. GFC/NBER recession: 2007-12-01 through 2009-06-30;
4. Q4 2018: 2018-10-01 through 2018-12-31;
5. COVID public-health shock: 2020-02-01 through 2020-04-30;
6. calendar 2022 rate/inflation shock: 2022-01-01 through 2022-12-31; and
7. 2022 Terra/Celsius/FTX crypto stress: 2022-05-01 through 2022-12-31.

These are external event/calendar windows, not representation-specific ex-post peaks/troughs.
Known events are `preregistered historical replay`, not untouched. Prospective evidence means only
future observations unavailable at freeze.

### 11. Metrics, equity boundary, and representation consistency

No composite score exists. Path/risk includes max drawdown, worst month, worst quarter, fixed stress
loss, and volatility. Recovery includes recovery duration, censor status, and time-underwater area.
Opportunity cost compares with compounded lagged DFF. Contribution scales loss or excess return by
the registered analytical exposure.

Equity permits only per-constituent results, breadth, median/percentiles/range/dispersion, governed-
cluster dispersion, pairwise co-behavior, leave-one-out sensitivity, and constituent loss envelopes.
It prohibits equal-weight, market-cap, current-weight, or synthetic paths. Every table reports eligible
versus expected counts, missing/pre-inception names, censored recoveries, selection-conditioned-cohort
warning, and action truncations. Current cohort membership is not the historical opportunity set.

SPY/VEA/VWO and BTC/ETH/SOL remain separate. Material directional differences make their family
`unable_to_determine`. GLD may be studied standalone; conditional peers may only test representation
sensitivity after their gates pass. No conflict is averaged away.

### 12. Dominance and policy-review rule

LOWER or HIGHER is compared only with the same family's historical reference. Mandatory independent
families are downside path, recovery burden, and opportunity cost. A candidate dominates only when it
is no materially worse across every applicable family and strictly improves at least two distinct
families. Correlated metrics inside one family count once. Representation consistency is a veto, not
an extra improvement count. Monotonicity is required only for mathematically exposure-scaled loss and
opportunity contribution.

The 1.00pp contribution/equivalence tolerances, 30-day recovery tolerance, 10pp equity-breadth
tolerance, 75% equity directional breadth, and 21-constituent minimum are uncalibrated one-study
`NUM-0001` provisional governance guardrails. Conflict produces `unable_to_determine`.

### 13. Trial inventory

The exact derived inventory ceiling is `37 representations × 3 scenarios × 7 windows = 777 cells`:
27 equity constituents + SPY/VEA/VWO + GLD/IAU/SGOL/GLDM + BTC/ETH/SOL. Conditional gold cells are
inside, not added to, the ceiling.

One representation × scenario × window × exact config hash × exact data-hash bundle is one cell.
Metrics from the same path are not new trials. Failed, discarded, conditional, pre-inception, and
ineligible attempts remain accounted. Reserve trials equal zero. Unused capacity lapses and cannot be
reallocated. No new result-aware cell is authorized.

### 14. Rerun rule

There is no rerun after results are observed. A rerun requires a separately accepted charter
amendment or new RISK study and either a material new evidence regime or a separately governed
integrity correction. A discovered defect does not silently authorize a second run. Logged
preregistered fallback retries may occur before registered execution.

### 15. One future implementation/results PR

After this charter's independent exact-head review, principal acceptance, merge, and hash
verification, exactly one later PR may deliver:

- acquisition and pagination receipts;
- a data manifest and raw/transformed hashes;
- coverage and eligibility reports;
- committed/quarantined data inventory;
- deterministic runner and trial ledger;
- focused tests and validators;
- per-representation and window results;
- dominance/conflict disposition;
- limitations and survivorship report;
- final research disposition record; and
- protocol/preregistration hash verification.

It may not make a production configuration change. Independent exact-head review and principal
acceptance remain required for its result lifecycle.

### 16. Absolute prohibited scope and protected paths

Neither this charter nor the later results PR may create final Level-1 targets, final Level-2
membership or weights, an optimizer/grid search, composite score, residual redistribution, strategic
cash, debt/margin/leverage analysis, chart/technical signals, trades/orders, automatic adoption,
unregistered trials, automatic reruns, whole-portfolio construction, 100% reconciliation, or a
residual proxy.

Protected and unchanged: `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, allocator/execution code, `margin_state.py`, `levels.py`, margin doctrine
and parameters, Level-1 numeric records/manifest, `numeric_sizing_validator.py`, profiles,
relationships, policy-adoption records, `LEVEL2-0001` evidence, XASSET-0012 through XASSET-0019, and
sealed Intelligence sources.

### 17. Approved charter files

This filing is limited to:

1. this decision;
2. `research/level1_sleeve_robustness/PROTOCOL_V1.md`;
3. `research/level1_sleeve_robustness/pre_registration.yaml`;
4. `level1_sleeve_robustness_preregistration_validator.py`;
5. `test_level1_sleeve_robustness_preregistration_validator.py`;
6. `governance/decisions.yaml`;
7. `operations/WORKSTREAMS.yaml`; and
8. the two mechanical catalog-count assertions in
   `test_portfolio_hq_dashboard_decisions.py`.

The dedicated validator is read-only and mechanical. It validates closed structure, exact identities,
scenario arithmetic, windows, trial arithmetic, prohibitions, and hash conventions; it cannot acquire
data or execute the study.

### 18. Effectiveness and stop boundary

This is `OPS-0009` Lane G. It must remain a draft PR, receive independent full exact-head review with
retained attribution, complete any required correction and re-review, and receive explicit principal
exact-head acceptance before merge. Filing and CI do not make the charter effective.

The author stops after the clean final branch is pushed, the draft PR exists, and CI on that exact
head completes successfully. The author does not self-review, principal-accept, mark ready, merge,
acquire data, run the study, begin replacement Level-1 sizing, or begin Level-2 sizing.

## Rationale

XASSET-0019 correctly removed future authority from a mechanically reproducible but economically
unvalidated sizing scaffold. The next decision cannot be another point estimate chosen from the same
scaffold; it needs a bounded empirical challenge that preserves nulls, representation conflicts, and
the absence of a lawful whole portfolio. Separate representations prevent an assumed internal weight
from masquerading as evidence. Closed preregistration, hash pins, strict data gates, and one execution
PR prevent result-aware drift while preserving the ability to acquire the missing long histories.

The relative perturbation is intentionally modest in design authority: it supplies three fixed states
without claiming calibration. The dominance rule is likewise a research guardrail, not a policy
utility function. Requiring multiple independent families and no veto-family deterioration prevents a
single attractive return or single risk statistic from controlling the disposition.

## Alternatives Considered

**Reuse ±2pp.** Rejected. XASSET-0019 explicitly removes R2/R3 numeric authority, and inheritance
would blur historical provenance with a new study assumption.

**Search a weight grid or optimize a score.** Rejected. That would answer a prohibited “best weight”
question and make trial accounting result-dependent.

**Build aggregate equity, broad-market, or crypto paths.** Rejected. Level-2 internal weights do not
exist, and representation conflicts are decision-relevant evidence, not noise to average away.

**Assign the remainder to cash, debt, or a benchmark.** Rejected. XASSET-0019 prohibits that plug and
requires a later complete non-adopted candidate before whole-portfolio stress.

**Acquire data in the charter PR.** Rejected. Separating authorization from execution preserves
reviewability and guarantees scenario/window/rule freeze before acquisition and results.

## Consequences

If this charter completes its lifecycle, one bounded implementation/results PR may acquire the named
data and execute the 777-cell maximum inventory exactly once. A null, conflict, or data-gate failure is
a valid result. No result changes production policy. Any replacement Level-1 method, point/range
choice, final Level-2 decision, whole-portfolio candidate, stress test, adoption, or margin/debt work
remains separately governed and downstream.
