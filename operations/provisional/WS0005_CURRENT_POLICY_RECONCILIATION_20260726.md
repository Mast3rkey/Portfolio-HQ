# WS-0005 Current-Policy vs. Provisional-Scenario Reconciliation

**PROVISIONAL, ADVISORY.** Companion to `WS0005_PRELIMINARY_PORTFOLIO_ARCHITECTURE_20260726.md`.
Covers exactly the 17 ACCEPTED/PROVISIONAL-Intelligence holdings — the only
holdings this preliminary pass reasoned about a candidate role/tier/target
for. The other 48 roster entries are addressed in
`WS0005_COVERAGE_GAP_REGISTER_20260726.md` instead, with current policy
preserved exactly and unreasoned-about.

**Reading the "possible later advisory output" column:** this describes what
`allocate.py`'s existing gap/cap/trim logic *could* mechanically produce if
this scenario file were ever run — it is not itself a recommendation, and no
such run has occurred. "None expected" means the point target equals the
current target, so no scenario-specific deviation exists to produce a
different output than an official run already would.

## Reconciliation table

| Ticker | Evidence status | Current role/tier | Candidate role/tier | Current target | Candidate range | Point target | Δ | Confidence | Evidence authority |
|---|---|---|---|---|---|---|---|---|---|
| TSM | ACCEPTED | Core AI-infra foundry / T1 | Same — dominant leading-edge/advanced-packaging foundry, high switching costs | 3.35% | 3.00%–3.75% | 3.35% | 0.00pp | High | `PI-0012`/`PI-0013` |
| COST | ACCEPTED | Consumer-membership compounder / T1 | Same — committee-reviewed, "Keep current policy" | 3.35% | 3.10%–3.60% | 3.35% | 0.00pp | High | `PI-0003`/`TGT-0002`/`PI-0021`/`PI-0022` |
| NVDA | ACCEPTED | AI-compute merchant-silicon leader / T1 | Same — committee-reviewed, "Keep current policy" | 3.35% | 3.10%–3.60% | 3.35% | 0.00pp | High | `PI-0007`/`PI-0017`/`PI-0018` |
| GEV | ACCEPTED | AI-infra power-buildout / T1 | Same — committee-reviewed, "Keep current policy" despite Medium conviction | 3.35% | 2.85%–3.35% | 3.35% | 0.00pp | Medium (committee-affirmed) | `PI-0007`/`PI-0019`/`PI-0020` |
| ISRG | ACCEPTED | Surgical-robotics platform leader / T2 | Same — broad-based multi-metric growth, High conviction | 1.65% | 1.55%–2.00% | 1.65% | 0.00pp | High | `PI-0011`-era + refresh |
| TMO | ACCEPTED | Life-sciences-tools diversified / T2 | Same — positive but comparatively muted segment growth | 1.65% | 1.35%–1.65% | 1.65% | 0.00pp | Medium | `PI-0009` |
| XOM | ACCEPTED | Advantaged-production oil major / band | Same — strong production growth balanced by cyclicality | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0005` |
| ASML | PROVISIONAL | EUV lithography monopoly / T1 | Same — genuine, well-evidenced monopoly; Medium not High on export-control/geopolitical exposure | 3.35% | 2.75%–3.35% | 3.35% | 0.00pp | Medium (first-coverage, no committee review yet) | `PI-0023` |
| AMAT | PROVISIONAL | Broadest-coverage semis-equipment maker / band | Same — largest US equipment maker, record trajectory, China-revenue concentration risk | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0023` |
| KLAC | PROVISIONAL | Process-control/inspection leader / band | Same — dominant niche, highest gross margin in Batch 1, 17-year dividend streak | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0023` |
| LRCX | PROVISIONAL | Etch/deposition leader / band | Same — leading plasma-etch/thin-film position, most concentrated memory-cycle exposure in Batch 1 | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0023` |
| MU | PROVISIONAL | Fast-growing HBM #2/#3 challenger / band | Same — fastest-growing HBM share of three merchant DRAM makers, severe historical cyclicality | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0024` |
| SKHY | PROVISIONAL | HBM market-leader ADR / band | Same — reported HBM share leader, ADR-structure risk unique among covered holdings | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0024` |
| AVGO | PROVISIONAL | AI-accelerator design + recurring software / T2 | Same tier — evidence trends toward stronger end of T2 range (see narrative note below) | 1.65% | 1.65%–2.10% | 1.65% | 0.00pp | High (first-coverage, no committee review yet) | `PI-0025` |
| AMD | PROVISIONAL | Diversified CPU/GPU/embedded designer / band | Same — broadest single-name diversification in Batch 3, distant #2 in AI accelerators | 0.75% | 0.60%–0.85% | 0.75% | 0.00pp | Medium | `PI-0025` |
| MRVL | PROVISIONAL | AI-networking/custom-silicon specialist / band | Same — strong growth, severe simultaneous legacy-segment contraction, disputed customer signal | 0.75% | 0.55%–0.85% | 0.75% | 0.00pp | Medium | `PI-0025` |
| INTC | PROVISIONAL | IDM foundry-turnaround / spec (fixed) | Same — strongest-yet turnaround evidence, explicit 14A pause contingency | 1.00% (fixed) | 0.75%–1.00% | 1.00% | 0.00pp | Medium | `PI-0025` |

**Column totals:** current target sum (17 holdings) = 28.70pp. Point-target
sum = 28.70pp. **Δ = 0.00pp — reconciles exactly.**

## Narrative note: AVGO/TMO directional observation (not implemented)

AVGO's evidence (Q2 FY2026 AI-semiconductor revenue +143% YoY, an improving
A-/BBB+ credit trajectory, and a recurring-software segment none of its
immediate T2 peers carry) trends toward the stronger end of a plausible T2
range. TMO's evidence (positive but comparatively muted FY2025 segment
growth across all four disclosed segments) trends toward the more moderate
end of its own range. **This directional difference is recorded here as a
qualitative observation only and is not implemented as a target change**,
because `targets.yaml`'s T2 tier applies one uniform `weight_pct` to all 14
T2 tickers — a single-ticker differentiated weight is not expressible in the
current schema without either a full tier reassignment (a larger claim than
this preliminary pass makes) or a schema change (out of scope, not
authorized). See `WS0005_PRELIMINARY_PORTFOLIO_ARCHITECTURE_20260726.md`'s
Methodology section for the full reasoning. Both point targets remain 1.65%.

## Unresolved evidence carried forward (not smoothed over)

- **AMD**: the ">10% two-customer" FY2025 revenue-concentration claim remains
  explicitly UNRESOLVED per `AMD.yaml`/`.md` — neither confirmed nor refuted.
- **INTC**: the exact US government ownership percentage is reported
  inconsistently across four values (9%, 9.9%, 10%, 8.4%) per `INTC.yaml`/`.md`.
- **MRVL**: the Amazon-Trainium competitive-loss signal remains actively
  disputed (a reported downgrade's loss claim versus a named JPMorgan
  contrarian view) per `MRVL.yaml`/`.md`.
- **ASML/AMAT/KLAC/LRCX**: each Batch 1 record's own disclosed evidentiary
  gaps (per-company figure disputes, e.g. KLAC's process-control market-share
  range) remain unresolved, per `intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` §11.
- **MU/SKHY**: MU's customer/hyperscaler revenue concentration was not found
  in Batch 2's research pass at all — an evidentiary gap, not evidence of low
  concentration, per `intelligence/BATCH2_MEMORY_COMPARISON.md` §12.

None of these unresolved items changed a candidate range or point target in
this pass — each record's own conviction rating already accounts for the
disclosed uncertainty, and this reconciliation does not re-weight beyond what
each record's own rationale already reasoned through.

## Possible later advisory output (descriptive only, per holding)

Since every point target in this scenario equals the current production
target for all 17 covered holdings, a future scenario allocation run using
this file would be expected to produce **the same advisory buy/underweight/
blocked/trim output as an official run** for every one of these 17 tickers —
no scenario-specific deviation exists to produce a different result. This is
itself disclosed as the honest consequence of this pass's zero-target-change
finding, not omitted to avoid the question the task's own template raises.
