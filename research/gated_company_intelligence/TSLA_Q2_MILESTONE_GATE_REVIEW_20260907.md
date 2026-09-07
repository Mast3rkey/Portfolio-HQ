# TSLA Q2 and milestone gate review

As of: 2026-09-07

Scope: Q2 primary evidence, issuer milestone status, capital quality, and dated
valuation screen

Decision effect: retain TSLA's existing gate; no target, holding, order, margin,
brokerage, or Stage-1 change

## Question

Do Tesla's Q2 2026 results satisfy the accepted requirement to activate only
under the milestone framework and a fresh valuation review?

## Evidence limitation that controls the answer

The repository's gate does not identify the accepted milestone framework or
its thresholds. This means the gate cannot be independently reproduced from
durable policy evidence. Absence of a defined framework is not permission to
substitute one after observing the results.

Tesla's SEC-filed 2025 CEO performance award is the closest direct issuer
framework because it measures the same decision-relevant axes: vehicle scale,
FSD subscriptions, robots, Robotaxi commercial scale, and adjusted EBITDA.
Using it as a diagnostic is analyst interpretation, not a claim that it was the
gate author's intended framework.

## Verified reported facts

| Metric | Q2 / June 30, 2026 | Evidence note |
|---|---:|---|
| Revenue | $28.236B, +26% YoY | Reported |
| GAAP gross profit / margin | $4.751B / 16.8% | Reported |
| GAAP operating income / margin | $398M / 1.4% | Down 57% YoY |
| GAAP common net income | $1.114B | Reported |
| Adjusted EBITDA / margin | $3.273B / 11.6% | Management-adjusted |
| Operating cash flow | $4.697B | Reported |
| Capital expenditures | $5.789B | Reported |
| Derived free cash flow | $(1.092)B | CFO less capex |
| Cash + short-term investments | $43.524B | Reported |
| Debt and finance leases | $9.342B | Current plus non-current |
| Vehicle deliveries | 480,126 | 9.7M cumulative |
| Active FSD subscriptions | 1.48M | Reported |
| Energy storage deployments | 13.5 GWh | Up 41% |

## Closest issuer-framework diagnostic

| Operational milestone | Q2 evidence | Disposition |
|---|---:|---|
| 20M cumulative Tesla vehicles delivered | 9.7M | Not achieved |
| 10M active FSD subscriptions | 1.48M | Not achieved |
| 1M bots delivered | Initial lines being installed; no delivery count | Not evidenced |
| 1M Robotaxis in commercial operation | Seven metros; no fleet count | Not evidenced |
| First adjusted-EBITDA threshold: $50B | $15.322B trailing four quarters | Not achieved |

Tesla identified only the 20M-vehicle milestone as probable over the award term
for accounting purposes. Probable over the term is not achieved as of the
measurement date. Tesla did not report any operational milestone as achieved.

The Robotaxi claim requires care: the shareholder update described the Bay Area
service as supervised with a safety driver and six other metros as ramping
unsupervised. Service availability in seven metros is not equivalent to one
million commercially operating Robotaxis.

## Capital quality and reported earnings

Q2 free cash flow was negative because capital expenditures exceeded operating
cash flow. Management expects 2026 capex above $25B. Q2 regulatory-credit
revenue fell 67% to $146M.

GAAP common net income included a $1.005B unrealized gain on Tesla's SpaceX
investment, while the Q2 tax provision included a $274M benefit from releasing
a California deferred-tax valuation allowance. Tesla invested $2.00B in
SpaceX common stock in the first half. These are disclosed facts; treating them
as non-operating or non-recurring for a normalized model would require a
separate valuation methodology.

The CEO award covers 423.7M restricted shares. Tesla reported $9.82B of
unrecognized compensation for the milestone considered probable and
$105.82B–$120.37B associated with milestones considered not probable. Q2
stock-based compensation was $1.151B. The SG&A increase included a $283M
increase in stock-based compensation, primarily related to the award; Tesla
separately reported $267M of Q2 award expense. A future per-share valuation
must model dilution and compensation rather than ignoring them.

## Dated market and valuation screen

Configured-feed inputs at the September 4, 2026 U.S. close were price $354.08
and market capitalization $1.253T. June 30 cash and debt produce derived net
liquidity of $34.182B and enterprise value of $1.219T.

- Market capitalization / trailing revenue: 12.10x.
- Enterprise value / trailing revenue: 11.77x.
- Enterprise value / trailing GAAP operating income: 278.9x.
- Current price / old illustrative SOTP high endpoint: 5.89x.

The sealed 2026-08-10 SOTP used simple revenue multiples and stale secondary
inputs. It is not a decision-grade intrinsic-value result, and the 5.89x
comparison is a limitation diagnostic rather than a price target or short
thesis.

No new DCF or segment SOTP is presented because credible segment cash-flow
forecasts, a defended discount rate, and bounded autonomy/robotics probabilities
are absent. The correct analytical result is abstention, not false precision.

## Facts, management claims, and interpretation

Financial statements, operating counts, program descriptions, award terms, and
accounting probability assessments are issuer-reported. Adjusted EBITDA is
management-adjusted. Free cash flow, net liquidity, trailing sums, and valuation
multiples are analyst calculations. The framework mapping and gate disposition
are analyst judgments.

## Gate disposition

Retain `cash_pending_clearance` and `allow_add: false`.

1. The repository does not identify the accepted milestone framework, so the
   gate is not reproducible on a literal reading.
2. Under the closest direct issuer framework, no operational milestone is
   reported achieved.
3. A dated market screen is available, but a decision-grade intrinsic valuation
   is not.

Do not change the accepted 0.50% target or deploy the cash reserved for it.
Future evidence can reopen review but cannot automatically authorize an add.

## Sources

- Tesla Q2 2026 earnings release / shareholder update:
  https://www.sec.gov/Archives/edgar/data/1318605/000162828026049213/exhibit991.htm
- Tesla Q2 2026 Form 10-Q:
  https://www.sec.gov/Archives/edgar/data/1318605/000162828026049270/tsla-20260630.htm
- Market-price snapshot: configured feed, September 4, 2026 U.S. close.

## Governance boundary

This artifact is decision evidence only. It does not modify `gates.yaml`,
`targets.yaml`, holdings, concentration policy, allocator behavior, margin
policy, brokerage state, or Stage 1. Stage 1 remains UNARMED and NOT EXECUTABLE.
