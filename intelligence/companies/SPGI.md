# SPGI — S&P Global Inc.

Last updated: 2026-09-03. This refresh directly reads S&P Global and MSCI
SEC-filed Q2 2026 materials, replaces the prior search-snippet evidence posture,
and materially advances the gate's same-date SPGI-versus-MSCI comparison. It does not
change the gate, target, holding, margin policy, or any execution state.

## Decision summary

S&P Global's continuing businesses remain high-quality, scaled information and
market-infrastructure franchises. The Mobility separation is now directly
verified, and the prior valuation-data conflict has been replaced with a
same-minute market snapshot. The comparison is mixed: SPGI has a lower trailing
P/E and a lower provisional net-debt-to-market-cap screen than MSCI, but also
lower reported/pro-forma growth and margin on the closest available measures.

The existing gate remains correct. Its comparison requirement is only partially
resolved, and its other conjunctive requirement — one clean post-spin quarter —
cannot be satisfied before S&P Global reports Q3 2026. Q2 remains a transition
quarter even though the issuer supplied Article 11 pro-forma information.

## Verified facts

### Continuing-company shape and Mobility separation

- The Mobility separation became effective July 1, 2026. S&P Global now reports
  four segments: Ratings, Indices, Energy, and Market Intelligence. Mobility's
  results are included through June 30, 2026; beginning with Q3 2026, its
  historical results will be shown as discontinued operations for all periods.
  [SPGI-P01]
- S&P Global's Q2 release reports GAAP revenue of $4.146 billion, operating
  profit of $1.812 billion, net income attributable to S&P Global of $1.217
  billion, and diluted EPS of $4.12. These figures include Mobility through June
  30 and therefore are not the clean continuing-company quarter required by the
  gate. [SPGI-P02]
- On the issuer's Article 11 pro-forma basis excluding Mobility, Q2 revenue was
  $3.678 billion, up 11%; operating profit was $1.757 billion, up 21%; diluted
  EPS was $4.08, up 26%; and operating margin was 47.8%, up 410 basis points.
  Pro-forma non-GAAP adjusted EPS was $4.83 and adjusted operating margin was
  54.3%. [SPGI-P02]
- The issuer's continuing-operations 2026 outlook calls for revenue growth of
  5.9%-7.9%, organic constant-currency growth of 6%-8%, GAAP EPS of
  $16.35-$16.60, and adjusted EPS of $17.50-$17.75. The issuer explicitly says
  this adjusted guidance is not directly comparable with prior guidance,
  because the prior outlook included a full year of Mobility. [SPGI-P02]

### Cash flow and capital structure

- Q2 free cash flow was $1.330 billion; adjusted free cash flow excluding
  certain items was $1.370 billion. Six-month figures were $2.249 billion and
  $2.362 billion, respectively. These are issuer-defined non-GAAP measures and
  are not used as direct valuation denominators here. [SPGI-P02]
- At June 30, S&P Global reported $4.134 billion of cash and $15.170 billion of
  debt. That debt included $1.981 billion carrying value for three Mobility
  notes with $2.0 billion aggregate principal. The filing states those notes
  became Mobility Global's sole responsibility after separation. [SPGI-P01]
- Subtracting the $1.981 billion Mobility-note carrying value from reported debt
  produces a provisional $13.189 billion continuing-company debt snapshot;
  subtracting cash produces provisional net debt of $9.055 billion. This is a
  derived transition-date screen, not issuer-reported post-spin net debt or a
  normalized leverage ratio.

## Normalized SPGI-versus-MSCI comparison

Market data are a same-minute screen from the configured feed at approximately
16:08 UTC on September 3, 2026. Reported financial metrics are from each
issuer's Q2 2026 SEC-filed materials.

| Metric | SPGI | MSCI | Comparability note |
|---|---:|---:|---|
| Share price | $447.11 | $573.70 | Same-minute market snapshot |
| Market capitalization | $132.12B | $41.82B | Same feed and minute |
| Trailing EPS | $16.43 | $18.28 | Feed-defined trailing basis |
| Trailing P/E | 27.21x | 31.38x | Same feed; 13.3% lower, but SPGI's denominator may still include Mobility |
| Q2 revenue growth | 11.0% pro forma | 12.2% reported/organic | SPGI excludes Mobility |
| Q2 operating margin | 47.8% pro forma | 56.2% reported | Closest available comparison |
| Adjusted profitability | 54.3% operating margin | 62.1% EBITDA margin | Directional only; unlike metrics |
| Net-debt / market-cap screen | 6.9% provisional | 14.5% | Debt measurement bases differ |

Additional valuation context:

- SPGI's September 3 price divided by the midpoint of its issuer-provided 2026
  adjusted-EPS guidance ($17.625) is 25.37x. MSCI did not provide an adjusted
  EPS outlook in the cited Q2 release, so no forward P/E comparison is claimed.
- MSCI reported Q2 revenue of $867.0 million, organic growth of 12.2%, operating
  margin of 56.2%, adjusted EBITDA margin of 62.1%, diluted EPS of $4.69, and
  adjusted EPS of $4.94. [MSCI-P01]
- MSCI reported $356.4 million of cash and $6.425 billion of principal debt,
  equivalent to 3.1x trailing adjusted EBITDA; its stated target is 3.0x-3.5x.
  S&P Global did not disclose a directly comparable post-spin debt/adjusted-
  EBITDA ratio in the cited materials, so none is manufactured. [MSCI-P01]

## Interpretation

The same-date comparison closes the old provider-conflict gap but not the full
normalization gap. SPGI's trailing earnings denominator may still include
pre-separation Mobility while its September 3 stock price is ex-Mobility, so the
13.3% apparent P/E discount is only a screen. SPGI's provisional balance-sheet
burden is lower than MSCI's relative to market capitalization, but that screen
is not a substitute for a comparable net-debt/EBITDA measure.

This supports a `screening-only` valuation posture. It does not prove that SPGI
is undervalued: the forward earnings bases are not equivalent, the post-spin
capital structure is still settling, and the clean post-spin quarter is absent.

## Material risks and open items

1. **Clean-quarter evidence is unavailable.** Q3 2026 will be the first quarter
   presenting Mobility as discontinued operations across comparative periods.
2. **Guidance comparability is limited.** The issuer says current adjusted
   guidance is not directly comparable with the prior Mobility-inclusive view.
3. **Capital allocation may obscure normalization.** S&P Global expects more
   than $7 billion of 2026 repurchases; post-spin leverage and share count must
   be assessed after Q3.
4. **Ratings and index revenue are market-sensitive.** Debt issuance, spreads,
   passive flows, and asset prices can amplify cyclicality.
5. **Non-GAAP metrics are not peer-identical.** SPGI adjusted operating margin
   and MSCI adjusted EBITDA margin must not be treated as the same denominator.
6. **No decision-grade SPGI post-spin debt/EBITDA ratio is available.** The
   provisional calculation is transparent but not a full normalization.

## Relationship to the gate

`gates.yaml` requires both "one clean post-spin quarter" and a normalized
SPGI-versus-MSCI valuation, leverage, and growth comparison. This refresh
materially advances, but does not fully complete, the comparison half because
no common continuing-company earnings multiple is available. It also cannot
complete the clean-quarter half before Q3 reporting. The gate remains `cash_pending_clearance`,
and `allow_add` remains false.

## Investment thesis (descriptive, not a recommendation)

SPGI combines regulated ratings infrastructure, high-margin indices, energy
benchmarks, and embedded data/workflow products. The September 3 comparison
shows a lower trailing multiple and provisional balance-sheet burden than MSCI,
offset by lower observed growth and margin plus unfinished post-spin
normalization. The evidence supports continued monitoring, not a sleeve or
weight change.

Evidence that could change the disposition:

- a clean Q3 continuing-operations report with comparable historical periods;
- a directly reported post-spin debt and leverage position;
- stable or improving organic growth and margins without unexpected stranded
  costs; and
- a refreshed same-basis valuation comparison after Q3 results.

## Review framework

- Cadence: 90 days.
- Next scheduled review: 2026-12-02.
- Unscheduled trigger: Q3 2026 results or any material guidance, capital-
  structure, regulatory, or separation-related change.
- Monitor: continuing-company organic growth, operating margin, adjusted EPS,
  cash conversion, net debt, share count, and SPGI-versus-MSCI valuation.

## Conviction

**Rating: Medium.** Primary-source recovery improves confidence in the factual
baseline, but it does not eliminate the decision-critical missing post-spin
quarter. The rating excludes entry price, target weight, trading, and leverage
instructions.

## Sources

- [SPGI-P01] S&P Global Q2 2026 Form 10-Q, filed July 29, 2026:
  https://www.sec.gov/Archives/edgar/data/64040/000006404026000045/spgi-20260630.htm
- [SPGI-P02] S&P Global Q2 2026 earnings release, filed July 28, 2026:
  https://www.sec.gov/Archives/edgar/data/64040/000006404026000040/spgi2q2026-earningsrelease.htm
- [MSCI-P01] MSCI Q2 2026 earnings release, filed July 28, 2026:
  https://www.sec.gov/Archives/edgar/data/1408198/000140819826000044/exhibit991earningsrelease-.htm
- [MSCI-P02] MSCI Q2 2026 Form 10-Q, filed July 28, 2026:
  https://www.sec.gov/Archives/edgar/data/1408198/000140819826000046/msci-20260630.htm
- Market data: configured feed, approximately 2026-09-03 16:08 UTC.
