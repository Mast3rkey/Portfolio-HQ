# WM discount-rate and valuation review — 2026-09-07

## Decision and scope

This review closes the explicit discount-rate evidence gap in the WM company
record. It is a sensitivity analysis for the existing initiation gate, not an
allocation optimization, target change, trade instruction, or execution
authorization.

**Disposition:** retain `cash_pending_clearance` and `allow_add: false`. The
accepted 0.75% WM target remains protected cash while the gate is closed. The
stale `next_gate` review condition is refreshed, but no change is made to the
gate status, `allow_add`, `targets.yaml`, holdings, margin policy, or any
Stage-1 artifact.

The reason is narrower than “WM is expensive.” At the 2026-09-04 close, WM's
peer-relative multiples did not look uniquely excessive, but a transparent
equity cash-flow DCF reached the market price only in the optimistic case. The
base and downside cases remained materially below the market, and 70–79% of
modeled value came from the terminal value. That combination does not provide
a robust margin of safety for initial deployment.

## Evidence hierarchy and inputs

| Input | Value | Classification and source |
|---|---:|---|
| 2026 WM free-cash-flow guidance | $3.75B–$3.85B | Issuer-reported, non-GAAP; [WM Q2 2026 release](https://investors.wm.com/news-releases/news-release-details/wm-announces-second-quarter-2026-earnings), 2026-07-28 |
| Diluted shares used in the model | 402.4M | Issuer-reported Q2 weighted-average diluted shares; same release |
| 10-year Treasury yield | 4.78% | U.S. Treasury par yield on 2026-09-04; [official daily curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=202609&type=daily_treasury_yield_curve) |
| Implied equity-risk premium | 4.28% | Damodaran country-risk dataset, published 2026-08-01; [NYU source](https://pages.stern.nyu.edu/~adamodar/) |
| Environmental & Waste Services beta | 0.95 regression / 0.82 corrected | 53-company industry set; [Damodaran industry beta dataset](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html), accessed 2026-09-07 |
| WM market price / equity capitalization | $218.99 / $87.941B | 2026-09-04 close; current market-data observation captured 2026-09-07 |
| RSG price / capitalization / trailing P/E | $222.71 / $68.512B / 31.55x | 2026-09-04 close; current market-data observation captured 2026-09-07 |
| WCN price / capitalization / trailing P/E | $164.87 / $41.853B / 39.73x | 2026-09-04 close; current market-data observation captured 2026-09-07 |

WM defines free cash flow as cash from operations less capital expenditures
plus proceeds from divestitures and other asset sales. It is after interest and
tax, so this review uses it as an **FCFE proxy**, but it is not literally cash
available for distribution and it is not a substitute for a full balance-sheet
forecast. The company definition is non-GAAP; debt repayment, dividends, and
repurchases remain separate uses of cash.

## Discount rate

The base cost of equity uses the Capital Asset Pricing Model:

`4.78% risk-free rate + 0.95 beta × 4.28% ERP = 8.85%`.

The model does not use WM's unusually low recent realized beta as permission
to lower the hurdle. Weekly total-return estimates from the repository's WM
and SPY series through 2026-07-31 were approximately 0.01 over two years, 0.07
over three years, 0.32 over five years, and 0.54 over ten years. Those estimates
are reproducible cross-checks, but their instability and low recent
correlation make them unsuitable as the sole forward discount-rate input.

The sensitivity range therefore uses:

- 8.29% in the optimistic case: 4.78% risk-free rate plus 0.82 corrected
  industry beta times 4.28% ERP;
- 8.85% in the base case: the formula above; and
- 10.06% in the downside case: 4.78% plus a deliberately conservative 1.10
  beta times a 4.80% ERP.

These are scenario assumptions, not forecasts and not an assertion that one
number is the company's “true” required return.

## FCFE-proxy DCF

For each case, the model grows the selected 2026 FCF guidance point for five
years, discounts those cash flows at the scenario cost of equity, and applies
the Gordon-growth formula to year six. Equity value is divided by 402.4M
shares. No in-sample parameter search was performed.

| Case | 2026 FCF | Five-year growth | Cost of equity | Terminal growth | Value/share | Vs. $218.99 | Terminal-value share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Downside | $3.75B | 4.0% | 10.06% | 2.25% | $131.36 | -40.01% | 70.0% |
| Base | $3.80B | 6.0% | 8.846% | 2.50% | $177.24 | -19.06% | 75.4% |
| Optimistic | $3.85B | 8.0% | 8.2896% | 2.75% | $222.56 | +1.63% | 78.7% |

The 4–8% explicit growth range is a disclosed sensitivity, not an extrapolation
of 2026's unusually strong FCF growth. Management's 2026 guidance benefits from
capital-spending normalization and integration progress; treating that step-up
as a perpetual growth rate would be unsupported.

## Peer cross-check

The peer comparison is deliberately secondary to the DCF because each issuer
uses its own adjusted FCF definition.

| Company | 2026 FCF midpoint | Equity capitalization | Forward FCF yield | Trailing P/E |
|---|---:|---:|---:|---:|
| WM | $3.800B | $87.941B | 4.32% | 31.69x |
| RSG | $2.558B | $68.512B | 3.73% | 31.55x |
| WCN | $1.425B | $41.853B | 3.40% | 39.73x |

RSG guidance comes from its [Q2 2026 release](https://investor.republicservices.com/news-releases/news-release-details/republic-services-inc-reports-second-quarter-2026-results), and WCN guidance
from its [Q2 2026 release](https://investors.wasteconnections.com/news/news-details/2026/Waste-Connections-Reports-Second-Quarter-2026-Results-and-Raises-Full-Year-Outlook/default.aspx).
GFL was reviewed but excluded from the table because current GAAP net income
was negative and the available market snapshot did not supply a comparable
capitalization; its [Q2 2026 release](https://investors.gflenv.com/English/news/news-details/2026/GFL-Environmental-Reports-Second-Quarter-2026-Results-and-Raises-Full-Year-2026-Guidance/default.aspx)
reports adjusted FCF guidance but does not cure that comparability problem.

**Inference:** WM's FCF yield is better than RSG's and WCN's on these inputs,
and its trailing P/E is roughly level with RSG's and below WCN's. The peer
screen therefore does not support the stronger claim that WM is uniquely
overvalued. It also does not supply an absolute margin of safety: the whole
peer set can be richly valued, and issuer-defined FCF is not standardized.

## Facts, calculations, and judgment

- **Facts:** the issuer guidance, Treasury yield, published industry beta and
  ERP, observed closing prices, market capitalizations, and peer guidance.
- **Calculations:** CAPM rates, FCF yields, DCF present values, per-share
  values, market-price gaps, and terminal-value shares.
- **Judgment:** the explicit growth, beta/ERP stress, and terminal-growth
  ranges; the conclusion that a gate should require resilience beyond the
  optimistic endpoint.

## Gate test and falsification

The valuation portion of the current gate is **researched but not cleared**.
The conclusion should be revisited if updated issuer evidence or a materially
lower price produces an adequate positive margin to value in the base case
while remaining survivable in the downside case. The Q3 2026 release should
also be used to re-anchor FCF, Healthcare Solutions integration, leverage, and
the delayed RNG connections.

The conclusion is falsified if a corrected input, model error, or comparable
primary-source cash-flow definition materially raises both base and downside
values. A single optimistic scenario, sell-side target, or peer premium is not
sufficient evidence by itself.

Until then: preserve the existing target as policy baseline, keep its capital
in protected cash, and do not issue an add or execution recommendation.
