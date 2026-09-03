# SPGI–MSCI normalized comparison and gate disposition

As of: 2026-09-03 16:08 UTC

Scope: SPGI and MSCI comparison evidence only

Decision effect: retain SPGI's existing gate; no target, holding, order, margin,
brokerage, or Stage-1 change

## Question

Can current primary evidence complete the gate's normalized SPGI-versus-MSCI
valuation, leverage, and growth comparison, and does it also satisfy the
separate requirement for one clean SPGI post-spin quarter?

## Verified reported facts

| Metric | SPGI | MSCI |
|---|---:|---:|
| Q2 revenue | $3.678B Article 11 pro forma, excluding Mobility | $867.0M reported |
| Q2 revenue growth | 11.0% | 12.2% reported and organic |
| Q2 operating margin | 47.8% Article 11 pro forma | 56.2% reported |
| Q2 adjusted profitability | 54.3% adjusted operating margin | 62.1% adjusted EBITDA margin |
| June 30 cash | $4.134B | $0.3564B |
| June 30 debt | $15.170B including $1.981B Mobility-note carrying value | $6.425B principal |

The adjusted-profitability row is not directly comparable because operating
margin and EBITDA margin use different denominators.

## Same-minute market facts

| Metric | SPGI | MSCI |
|---|---:|---:|
| Price | $447.11 | $573.70 |
| Market capitalization | $132.12B | $41.82B |
| Trailing EPS | $16.43 | $18.28 |
| Trailing P/E | 27.21x | 31.38x |

## Derived calculations

- SPGI feed-defined trailing-P/E discount to MSCI: 13.3%. This is not a
  continuing-company multiple because SPGI's trailing denominator may still
  include pre-separation Mobility while its price is ex-Mobility.
- SPGI forward adjusted P/E using issuer-guidance midpoint:
  $447.11 / $17.625 = 25.37x. MSCI supplied no adjusted-EPS guide in the cited
  release, so no forward peer multiple is claimed.
- SPGI provisional continuing-company debt:
  $15.170B - $1.981B Mobility-note carrying value = $13.189B.
- SPGI provisional net debt:
  $13.189B - $4.134B = $9.055B, or 6.9% of market capitalization.
- MSCI net-debt screen:
  $6.425B principal debt - $0.3564B cash = $6.0686B, or 14.5% of market
  capitalization.

The leverage screen mixes SPGI carrying debt and MSCI principal debt because
those are the cleanest disclosed bases available. It is directional, not a
substitute for a common net-debt/EBITDA calculation.

## Issuer claims

- SPGI's 2026 revenue, margin, EPS, and repurchase outlooks are forward-looking.
- MSCI's 3.0x-3.5x debt/adjusted-EBITDA target is a policy target, not a promise
  that future leverage will remain inside the range.

## Analyst interpretation

The comparison requirement is materially advanced but not fully normalized. It
shows SPGI at a lower feed-defined trailing multiple and provisional net-debt
burden, but also at lower Q2 growth and operating margin. The earnings and debt
bases are not fully aligned, so the apparent discount is not standalone
evidence of mispricing.

The clean-quarter requirement is not complete. SPGI's filing says Q3 2026 will
be the first period to present Mobility as discontinued operations across all
comparative periods. Article 11 pro-forma Q2 figures improve comparability but
do not turn Q2 into the required reported post-spin quarter.

Disposition: retain `cash_pending_clearance` and `allow_add: false`. Refresh the
comparison after Q3 results. Do not change the accepted 1.25% target or any
sleeve assignment in this evidence-only unit.

## Sources

- SPGI Q2 2026 Form 10-Q:
  https://www.sec.gov/Archives/edgar/data/64040/000006404026000045/spgi-20260630.htm
- SPGI Q2 2026 earnings release:
  https://www.sec.gov/Archives/edgar/data/64040/000006404026000040/spgi2q2026-earningsrelease.htm
- MSCI Q2 2026 earnings release:
  https://www.sec.gov/Archives/edgar/data/1408198/000140819826000044/exhibit991earningsrelease-.htm
- MSCI Q2 2026 Form 10-Q:
  https://www.sec.gov/Archives/edgar/data/1408198/000140819826000046/msci-20260630.htm
- Market-price snapshot: configured market-data feed, same-minute timestamps
  of 16:08:05 UTC for SPGI and 16:08:47 UTC for MSCI.

## Governance boundary

This artifact is decision evidence only. It does not modify `gates.yaml`,
`targets.yaml`, holdings, concentration policy, allocator behavior, margin
policy, brokerage state, or Stage 1. Stage 1 remains UNARMED and NOT EXECUTABLE.
