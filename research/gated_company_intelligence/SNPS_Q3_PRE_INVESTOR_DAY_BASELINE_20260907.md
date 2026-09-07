# SNPS Q3 pre–Investor Day baseline and gate disposition

As of: 2026-09-07

Scope: SNPS Q3 evidence, earnings quality, capital structure, and dated
valuation screen only

Decision effect: retain SNPS's existing gate; no target, holding, order, margin,
brokerage, or Stage-1 change

## Question

Does the Q3 2026 primary evidence resolve the gate's Ansys-integration,
leverage, GAAP-normalization, and purchase-valuation concerns before the
September 30 Investor Day?

## Verified reported facts

| Metric | Q3 / July 31, 2026 | Evidence note |
|---|---:|---|
| Revenue | $2.477B, +42% YoY | Reported; includes Ansys |
| Design Automation revenue | $2.003B, +53% | Reported segment revenue |
| Design IP revenue | $473.9M, +11% | Reported segment revenue |
| GAAP operating margin | 14.4% | Reported |
| Non-GAAP operating margin | 41.6% | Management-adjusted |
| GAAP diluted EPS | $2.84 | Includes divestiture gain |
| Non-GAAP diluted EPS | $3.91 | Management-adjusted |
| Cash + short-term investments | $3.608B | Reported balance sheet |
| Total debt | $10.037B | Short-term plus long-term debt |
| Derived net debt | $6.430B | Debt less cash and short-term investments |
| Goodwill + net intangibles | $38.293B | 80.2% of total assets |

## EPS-quality bridge

GAAP results include a $425.4M pre-tax Processor IP divestiture gain. The
non-GAAP reconciliation adds back $402.4M of acquired-intangible amortization,
$231.6M of stock compensation, and $2.2M of restructuring charges; removes
$402.6M of acquisition- and divestiture-related gains; and includes $26.9M of
tax adjustments. The resulting non-GAAP EPS is useful as management's operating
view but is not a normalized owner-earnings figure.

## Design IP durability

Q3 improved, but the first nine months remain weak: Design IP revenue was
$1.335B versus $1.345B, adjusted operating income was $302.2M versus $363.1M,
and adjusted margin was approximately 23% versus 27%. The single-quarter
recovery therefore does not yet prove durable economics.

## Integration and capital structure

- The expected restructuring range rose from $300-$350M to $425-$500M.
- Quarterly interest expense was $133.2M.
- The balance sheet carried $26.835B of goodwill and $11.459B of net
  intangibles.
- Fiscal 2026 guidance forecasts approximately $2.8B of operating cash flow and
  $2.6B of free cash flow; these remain management forecasts.

## Dated market and valuation screen

Configured-feed inputs at the September 4, 2026 close: price $393.84, market
capitalization $75.743B, trailing EPS $5.71, and trailing P/E 68.97x.

- Price / FY2026 non-GAAP EPS guide midpoint: 26.13x.
- Market cap / FY2026 free-cash-flow guide: 29.13x.
- Derived enterprise value: $82.173B.
- Enterprise value / FY2026 revenue guide midpoint: 8.46x.
- Enterprise value / FY2026 free-cash-flow guide: 31.60x.

Every denominator except trailing EPS is management guidance, and the revenue
guide includes Ansys plus divestiture effects. These are comparable future
checkpoints, not a normalized valuation or an adoption signal.

## Issuer claims versus analyst interpretation

Issuer forecasts include revenue, margin, EPS, cash-flow, and Ansys contribution
guidance. The calculations above are analyst-derived from those disclosed
inputs. The conclusion that earnings require normalization and that integration
risk remains live is an evidence-based interpretation, not an issuer statement.

## Gate disposition

Retain `cash_pending_clearance` and `allow_add: false`. The official Investor
Day is scheduled for September 30, 2026 at 1:00 p.m. ET; it has not occurred.
After the event, rebuild the valuation using disclosed organic-growth, margin,
synergy, capital-allocation, and deleveraging targets, while retaining
economically real stock compensation and acquisition costs.

Do not change the accepted 2.50% target or any sleeve assignment in this
evidence-only unit.

## Sources

- Synopsys Q3 2026 earnings release:
  https://www.sec.gov/Archives/edgar/data/883241/000119312526368620/d157153dex991.htm
- Synopsys Q3 2026 Form 10-Q:
  https://www.sec.gov/Archives/edgar/data/883241/000088324126000025/snps-20260731.htm
- Synopsys Form 8-K/A restructuring update:
  https://www.sec.gov/Archives/edgar/data/883241/000119312526368858/d135796d8ka.htm
- Synopsys official Investor Day page:
  https://investor.synopsys.com/events-and-presentations/events/event-details/2026/Investor-Day-2026-KNzbA2A1qm/default.aspx
- Market-price snapshot: configured feed, September 4, 2026 U.S. close.

## Governance boundary

This artifact is decision evidence only. It does not modify `gates.yaml`,
`targets.yaml`, holdings, concentration policy, allocator behavior, margin
policy, brokerage state, or Stage 1. Stage 1 remains UNARMED and NOT EXECUTABLE.
