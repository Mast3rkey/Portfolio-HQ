# WS-0005 Coverage-Gap Register

**PROVISIONAL, ADVISORY.** Companion to `WS0005_PRELIMINARY_PORTFOLIO_ARCHITECTURE_20260726.md`.
Every holding in `holdings.yaml`'s `shares:` block **without** a qualifying
ACCEPTED or PROVISIONAL Company Intelligence record — 45 companies plus 3
ETFs, 48 entries total. **No candidate here is ranked for capital
allocation.** Current role, tier, and target are preserved **exactly** for
every entry in this register, labeled `temporary current-policy baseline —
not independently re-derived` throughout — this register does not infer, and
this package does not treat, the existing policy as correct for any of them.

## Why these 48 are not independently re-derived (applies uniformly unless noted)

No Company Intelligence record exists for these tickers because no WS-0005
Milestone-3 research batch has yet been authorized covering them. `PI-0023`
(Batch 1), `PI-0024` (Batch 2), and `PI-0025` (Batch 3) each named an exact,
bounded company list — none of these 48 tickers was included in any of the
three. Coverage for any of them requires its own future, separately
authorized Milestone-3 batch (or, for the three T1 megacaps MSFT/GOOGL/META,
potentially a dedicated `PI-0016`-style committee review given their scale)
— this register does not select, propose, or authorize any such batch; it
only records the gap.

## T1 tier (0.75%–0.25pp confidence-weighted risk band; 3.35% target each)

| Ticker | Current target | Missing research | Material risk of relying on baseline | Could a gap materially affect a future scenario result? | Future research trigger |
|---|---|---|---|---|---|
| MSFT | 3.35% | Full Company Intelligence record | **Highest-priority gap in the register** — MSFT is a top-5-by-weight T1 holding with no independent evidence check at all; `CLAUDE.md`'s own Decisions Log already flags T1 as "7-of-9 names in the identified AI-infrastructure grouping," a concentration finding that predates any of MSFT's own economics being independently verified | Yes — MSFT is large enough that a materially adverse finding could argue for a real target change, unlike most band-tier gaps | Milestone-3 batch or dedicated committee review authorization |
| GOOGL | 3.35% | Full Company Intelligence record | Same AI-infra-grouping concentration finding as MSFT; no independent verification of GOOGL's own AI-capex-cycle exposure exists | Yes | Milestone-3 batch or dedicated committee review authorization |
| META | 3.35% | Full Company Intelligence record | Same AI-infra-grouping concentration finding; META recurs as a named customer across all three semis-batch comparison artifacts (a demand-side counterparty to holdings this repository has researched) without META's own supply/demand economics ever being independently verified | Yes | Milestone-3 batch or dedicated committee review authorization |
| LLY | 3.35% | Full Company Intelligence record | GLP-1/obesity-drug franchise concentration and patent-cliff timing are unverified by this repository | Yes | Milestone-3 batch or dedicated committee review authorization |
| V | 3.35% | Full Company Intelligence record | Payments-network economics, regulatory/interchange-fee risk unverified | Yes | Milestone-3 batch or dedicated committee review authorization |

## T2 tier (1.65% target each)

| Ticker | Current target | Notable gap-specific context |
|---|---|---|
| AMZN | 1.65% | Named repeatedly as a hyperscaler customer/counterparty across AVGO, MRVL, and MU/SKHY's own Company Intelligence records (Trainium program, AWS demand) without AMZN's own economics being independently verified — a real informational asymmetry given how much of this repository's semis-cluster research assumes AMZN as a stable demand source |
| CEG | 1.65% | Power/utility economics, nuclear-relicensing and AI-datacenter power-purchase-agreement exposure unverified |
| PWR | 1.65% | Member of the governed `power_infra` cluster cap (with GEV) but has no own-name Intelligence record despite GEV's own record existing |
| DHR | 1.65% | Life-sciences-tools diversified peer to TMO (which is ACCEPTED) — no independent verification of DHR's own segment mix or China exposure |
| SYK | 1.65% | Named as a considered-but-deferred candidate in `PI-0014`'s bounded evidence review; still no filed record |
| MA | 1.65% | Payments-network peer to V; same unverified regulatory/interchange exposure |
| BRK.B | 1.65% | Named as a comparator in COST's own `PI-0021` committee review; conglomerate-scale economics unverified in their own right |
| WMT | 1.65% | Named as a comparator in COST's own `PI-0021` committee review; own-name economics unverified |
| EQIX | 1.65% | Data-center REIT — direct AI-infrastructure real-estate exposure, thematically adjacent to `ai_infrastructure` but no own-name record or theme membership |
| MLM | 1.65% | Aggregates/infrastructure economics unverified; absorbed VMC's exposure per the 2026-07-13 consolidation decision but no dedicated record exists |
| AAPL | 1.65% | Promoted band→T2 as a doctrine decision (see `CLAUDE.md` Decisions Log); own-name Intelligence never filed |

*(All T2 gaps: missing full Company Intelligence record; material risk is
moderate-to-high given T2's meaningful per-name weight; future trigger:
Milestone-3 batch or committee-review authorization.)*

## Band tier (0.75% target each, cap 1.25×) — 25 tickers

| Ticker | Notable gap-specific context |
|---|---|
| WDC | **Explicitly excluded from Batch 2 (`PI-0024`)** on the finding that its post-Sandisk-separation HDD business is a different economic function from the DRAM/NAND/HBM bet MU/SKHY examine — `targets.yaml`'s stale MU/WDC cluster comment (identified, not corrected, per `PI-0024` §E) remains an open, separate, unauthorized factual-reconciliation item, distinct from a coverage gap |
| VRT, ETN | `power_infra` cluster-cap members alongside GEV/PWR; no own-name records |
| CAT | Explicitly considered and excluded from the `power_infra` cap on fundamental-fit grounds (`CLAUDE.md` Decisions Log) — still uncovered |
| GNRC, IBM, NOW, CRM, ORCL, NFLX, SHOP, CRWD, PANW, UBER, JPM, HOOD, DELL | No Intelligence record; no batch has ever named any of these |
| CVX | `oil` cluster-cap member alongside XOM (ACCEPTED); no own-name record despite the cap's own derivation resting partly on XOM's researched drawdown history |
| RTX, ABBV, MRK, JNJ, GILD, UNH | No Intelligence record; no batch has ever named any of these |
| BABA | Foreign-issuer/China-domiciled exposure entirely unverified by this repository — arguably a higher-priority gap than most band names given the geopolitical-exposure pattern already documented for MU/SKHY/AVGO/AMD |

*(All band gaps: missing full Company Intelligence record; material risk is
generally lower per-name given band's smaller 0.75% weight, except BABA
(geopolitical) and cluster-cap members (VRT/ETN/CAT/CVX) where a cap-level
finding could matter even at small per-name weight; future trigger:
Milestone-3 batch authorization.)*

## Spec tier (1.00% fixed target each) — 4 tickers

| Ticker | Notable gap-specific context |
|---|---|
| SPCX | No Intelligence record; private/pre-IPO-adjacent structure may complicate standard evidence-gathering |
| RKLB | Explicitly named in `CLAUDE.md`'s own `trim_backtest.md` Decisions Log entry (RKLB's realized -28.6% drawdown at ~3.6x intended size was the disqualifying case for the never-trim backtest arm) — a name this repository already has real risk evidence about, but no formal Company Intelligence record |
| TSLA | Explicitly considered and excluded from the `power_infra` cluster cap on fundamental-fit grounds; no own-name record |
| PLTR | No Intelligence record; no batch has ever named this ticker |

*(All spec gaps: missing full Company Intelligence record; spec's fixed,
non-cap-exceeding sizing limits downside from a coverage gap somewhat versus
band; future trigger: Milestone-3 batch authorization.)*

## ETF sleeve (2.30% target each) — 3 tickers, structurally different category

| Ticker | Why not applicable in the same sense |
|---|---|
| SPY, QQQ, GLD | Index/commodity-tracking funds, not operating companies — the Company Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`) is built for company-level economic/competitive/risk analysis, which does not map cleanly onto a passive fund. This register does not propose a Company Intelligence record for any of the three; it records their absence from any evidence-gathering process only for completeness. No material risk beyond the fund's own well-known, broadly-disclosed tracking characteristics. |

## Crypto sleeve — not applicable to this register

BTC/ETH/SOL are governed by the crypto sleeve (`targets.yaml`'s `crypto:`
block), a fundamentally different allocation mechanism (aggregate sleeve gap,
not per-coin target) — outside this register's company-level scope entirely,
consistent with every prior WS-0005 milestone's own scoping.
