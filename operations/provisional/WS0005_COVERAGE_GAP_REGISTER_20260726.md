# WS-0005 Coverage-Gap Register

**PROVISIONAL, ADVISORY.** Companion to `WS0005_PRELIMINARY_PORTFOLIO_ARCHITECTURE_20260726.md`.

**Bounded correction note (this revision):** an independent ChatGPT review
(review `4781581139`, verdict CHANGES REQUIRED) found the prior revision
grouped multiple tickers into single rows and omitted required fields for
the T2/band/spec/ETF sections. This revision gives **every one of the 45
uncovered company holdings its own explicit row with all nine required
fields**, and treats the 3 ETFs as a **separate structural category** with
their own full disposition — never presented as "uncovered companies."

## Roster counts (corrected)

- **65** total share-target roster entries (`holdings.yaml`'s `shares:` block).
- **62** are company holdings.
  - **17** carry qualifying Company Intelligence (13 ACCEPTED + 4
    PROVISIONAL — see `WS0005_CURRENT_POLICY_RECONCILIATION_20260726.md`).
  - **45** are covered in this register as NOT INDEPENDENTLY RE-DERIVED.
- **3** are ETFs (SPY, QQQ, GLD), a structurally separate category, covered
  in its own section below.

**No candidate in this register is ranked for capital allocation.** Every
row's current role, tier, and target is preserved **exactly**, labeled
`temporary current-policy baseline — not independently re-derived` — this
register does not infer, and this package does not treat, the existing
policy as correct for any of them. Any language below describing a gap as
having greater or lesser materiality reflects **research-coverage urgency
only** — it is not a capital ranking and does not select, authorize, or
imply any future research batch.

## Why these 45 are not independently re-derived (uniform reason, applies to every row unless a row states otherwise)

No Company Intelligence record exists for these tickers because no WS-0005
Milestone-3 research batch has yet been authorized covering them. `PI-0023`
(Batch 1), `PI-0024` (Batch 2), and `PI-0025` (Batch 3) each named an exact,
bounded company list — none of these 45 tickers was included in any of the
three. Coverage for any of them requires its own future, separately
authorized Milestone-3 batch (or, for the largest T1 megacaps, potentially a
dedicated `PI-0016`-style committee review) — this register does not select,
propose, or authorize any such batch; it only records the gap, per ticker.

## T1 tier — 5 uncovered company holdings (3.35% target each)

| Ticker | Current target | Current role/tier baseline | Label | Missing research | Material risk of relying on baseline | Could the gap materially affect a future scenario result? | Future research trigger |
|---|---|---|---|---|---|---|---|
| MSFT | 3.35% | T1 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (economic role, competitive position, financial quality, AI-capex exposure, cloud/enterprise-software concentration, risks) | High materiality because of existing portfolio weight — MSFT is a top-tier T1 holding with no independent evidence check at all; recurs as a named AI-infrastructure/hyperscaler counterparty across all three completed semis-batch comparison artifacts without its own economics ever being verified | Yes — a materially adverse finding could argue for a real target change, unlike most smaller-weight gaps | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only — not a batch selection or authorization) |
| GOOGL | 3.35% | T1 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | High materiality because of existing portfolio weight — same AI-infrastructure-concentration finding as MSFT (`CLAUDE.md` Decisions Log's own "7-of-9 T1 names" observation); GOOGL's TPU/AI-capex economics are referenced by name in TSM's and AVGO's own records without independent verification of GOOGL itself | Yes | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only) |
| META | 3.35% | T1 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | High materiality because of existing portfolio weight — same T1 AI-infra-concentration finding; META recurs as a named hyperscaler customer across AVGO's and AMD's own records without its own supply/demand economics being independently verified | Yes | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only) |
| LLY | 3.35% | T1 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (GLP-1/obesity-drug franchise concentration, patent-cliff timing, pipeline durability) | High materiality because of existing portfolio weight; no other pharmaceutical holding provides a cross-check on LLY's own franchise-concentration risk | Yes | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only) |
| V | 3.35% | T1 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (payments-network economics, interchange-fee regulatory risk, MA overlap) | High materiality because of existing portfolio weight; MA (also uncovered, T2) shares the same regulatory exposure with no independent verification of either | Yes | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only) |

## T2 tier — 11 uncovered company holdings (1.65% target each)

| Ticker | Current target | Current role/tier baseline | Label | Missing research | Material risk of relying on baseline | Could the gap materially affect a future scenario result? | Future research trigger |
|---|---|---|---|---|---|---|---|
| AMZN | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate-high materiality — named repeatedly as a hyperscaler customer/counterparty across AVGO's, MRVL's, and MU/SKHY's own records (AWS Trainium program, AWS demand) without AMZN's own economics ever being independently verified; a real informational asymmetry given how much semis-cluster research assumes AMZN as a stable demand source | Yes | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only) |
| CEG | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (power/utility economics, nuclear-relicensing status, AI-datacenter power-purchase-agreement exposure) | Moderate materiality | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| PWR | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate materiality — `power_infra` cluster-cap member alongside GEV (covered); no own-name record despite GEV's own record existing and informing the cluster-cap's derivation | Possibly — cluster-cap-level findings could matter even at moderate per-name weight | Milestone-3 batch authorization (research-coverage urgency only) |
| DHR | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate materiality — life-sciences-tools diversified peer to TMO (covered); no independent verification of DHR's own segment mix or China exposure | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| SYK | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate materiality — named as a considered-but-deferred candidate in `PI-0014`'s bounded evidence review; still no filed record | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| MA | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (payments-network economics, regulatory/interchange exposure) | Moderate materiality — same regulatory-exposure category as V (uncovered, T1) | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| BRK.B | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (conglomerate-scale economics, capital-allocation history) | Moderate materiality — named as a comparator in COST's own `PI-0021` committee review; own-name economics never independently verified in their own right | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| WMT | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate materiality — named as a comparator in COST's own `PI-0021` committee review; own-name economics never independently verified | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| EQIX | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (data-center REIT economics, AI-infrastructure real-estate exposure) | Moderate materiality — thematically adjacent to `ai_infrastructure` (no theme membership or own-name record exists) | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| MLM | 1.65% | T2 core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (aggregates/infrastructure economics) | Moderate materiality — absorbed VMC's exposure per the 2026-07-13 consolidation decision but no dedicated record exists for the combined position | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| AAPL | 1.65% | T2 core holding (promoted band→T2, doctrine decision) | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate-high materiality given portfolio scale, though the promotion itself was a considered doctrine decision, not an unexamined default | Possibly | Milestone-3 batch or dedicated committee-review authorization (research-coverage urgency only) |

## Band tier — 25 uncovered company holdings (0.75% target each, cap 1.25×)

| Ticker | Current target | Current role/tier baseline | Label | Missing research | Material risk of relying on baseline | Could the gap materially affect a future scenario result? | Future research trigger |
|---|---|---|---|---|---|---|---|
| WDC | 0.75% | band core holding, `semis` cluster-cap member | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (post-Sandisk-separation HDD-storage economics) | Moderate — **explicitly excluded from Batch 2** (`PI-0024`) on the finding that its post-separation HDD business is a different economic function from the DRAM/NAND/HBM bet MU/SKHY examine; `targets.yaml`'s stale MU/WDC cluster comment (identified, not corrected, per `PI-0024` §E) remains a separate, unauthorized factual-reconciliation item, distinct from this coverage gap | Low-moderate | Milestone-3 batch authorization, separate from the unrelated `targets.yaml` comment correction (research-coverage urgency only) |
| VRT | 0.75% | band core holding, `power_infra` cluster-cap member | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate — `power_infra` cluster-cap member alongside GEV (covered) and PWR/ETN (also uncovered) | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| ETN | 0.75% | band core holding, `power_infra` cluster-cap member | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate — same `power_infra` cluster-cap exposure as VRT | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| CAT | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low-moderate — explicitly considered and excluded from the `power_infra` cluster cap on fundamental-fit grounds (`CLAUDE.md` Decisions Log); still uncovered as a standalone holding | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| GNRC | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| IBM | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| NOW | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| CRM | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| ORCL | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| NFLX | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| SHOP | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| CRWD | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| PANW | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| UBER | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| JPM | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (bank-specific financial and regulatory-capital analysis) | Low-moderate — financial-sector holdings carry structurally different risk factors (regulatory capital, credit cycle) than the industrial/tech names dominating this register | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| HOOD | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| CVX | 0.75% | band core holding, `oil` cluster-cap member | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate — `oil` cluster-cap member alongside XOM (covered); no own-name record despite the cap's own derivation resting partly on XOM's researched drawdown history | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| RTX | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| ABBV | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| MRK | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| JNJ | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| GILD | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| UNH | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |
| BABA | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record (foreign-issuer/China-domiciled structure and economics) | Moderate — geopolitical/China-domiciled exposure entirely unverified by this repository, a materially different risk category than most other band names given the geopolitical-exposure pattern already documented for MU/SKHY/AVGO/AMD | Possibly | Milestone-3 batch authorization (research-coverage urgency only) |
| DELL | 0.75% | band core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low | Milestone-3 batch authorization (research-coverage urgency only) |

## Spec tier — 4 uncovered company holdings (1.00% fixed target each)

| Ticker | Current target | Current role/tier baseline | Label | Missing research | Material risk of relying on baseline | Could the gap materially affect a future scenario result? | Future research trigger |
|---|---|---|---|---|---|---|---|
| SPCX | 1.00% (fixed) | spec core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low-moderate — private/pre-IPO-adjacent structure may complicate standard evidence-gathering | Low (spec's fixed sizing already caps this holding at exactly target) | Milestone-3 batch authorization (research-coverage urgency only) |
| RKLB | 1.00% (fixed) | spec core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Moderate — `CLAUDE.md`'s own `trim_backtest.md` Decisions Log entry documents a realized -28.6% drawdown at ~3.6x intended size for this name specifically, but no formal Company Intelligence record exists to contextualize that history | Low (spec's fixed sizing already caps this holding at exactly target) | Milestone-3 batch authorization (research-coverage urgency only) |
| TSLA | 1.00% (fixed) | spec core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low-moderate — explicitly considered and excluded from the `power_infra` cluster cap on fundamental-fit grounds; still uncovered as a standalone holding | Low (spec's fixed sizing already caps this holding at exactly target) | Milestone-3 batch authorization (research-coverage urgency only) |
| PLTR | 1.00% (fixed) | spec core holding | temporary current-policy baseline — not independently re-derived | Full Company Intelligence record | Low | Low (spec's fixed sizing already caps this holding at exactly target) | Milestone-3 batch authorization (research-coverage urgency only) |

## ETF baseline — 3 roster entries, a separate structural category (2.30% target each)

**These are not "uncovered companies."** Index/commodity-tracking funds are
a structurally different category from an operating company — the Company
Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`) is built for
company-level economic role, competitive position, and business-risk
analysis, which does not map onto a passive fund's actual risk profile
(tracking error, expense ratio, underlying-index composition, liquidity of
the fund itself — not a company's competitive moat or balance sheet). This
section gives each ETF its own full, explicit disposition rather than
folding them into the company register.

| Ticker | Current target | ETF role | Why Company Intelligence is structurally inapplicable | Baseline treatment | Relevant fund-level research gap, if any | Could this materially affect a future scenario result? | Future review trigger |
|---|---|---|---|---|---|---|---|
| SPY | 2.30% | Broad US large-cap equity index exposure (ETF sleeve) | Tracks a diversified index (S&P 500), not a single operating company; no competitive position, management team, or balance sheet of its own to analyze under the Company Intelligence schema | temporary current-policy baseline — no Company Intelligence record authorized or applicable | None material identified — SPY's tracking characteristics, expense ratio, and liquidity are broadly disclosed and well-established | No — SPY's role is diversified market-beta exposure, not a name-specific thesis this scenario reasons about | None specific to this register; any future review would be fund-level (expense ratio change, tracking-error anomaly), not company-research-driven |
| QQQ | 2.30% | Nasdaq-100 index exposure (ETF sleeve); also the account's `regime_ticker` for informational 200-EMA display | Same as SPY — tracks an index, not a single company | temporary current-policy baseline — no Company Intelligence record authorized or applicable | None material identified | No | None specific to this register |
| GLD | 2.30% | Gold-commodity-tracking exposure (ETF sleeve) | Tracks a physical commodity price, not a company at all — the Company Intelligence schema's economic-role/competitive-position/business-risk fields do not apply to a commodity-tracking instrument in any form | temporary current-policy baseline — no Company Intelligence record authorized or applicable; structurally inapplicable, not merely unresearched | None material identified — GLD's physical-backing and tracking mechanics are well-established and disclosed by the fund | No | None specific to this register |
