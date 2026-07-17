# Phase 4A Research Report: Concentration x Margin Interaction

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history. Every scenario below simulates a synthetic $0-start account through real historical prices (data/backtest/*.json). See `docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md` for the pre-approved design this run follows, and `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.

_Executed 2026-07-17. Window: 2021-06-01 to 2026-07-10. 62 monthly $2,000 deposits. Concentrated ticker: NVDA (real, already-decomposed reference point, `reports/t1t2_trim_backtest.md`). Correlated cluster: semis (real, existing 25%-cap cluster, `targets.yaml`, unmodified). Scenarios A/B/C run unlevered (leverage_cap=1.0) so only concentration varies; Scenario D is the only place leverage turns on (1.8x, fixed, no sweep) — per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §4/§5._

## Methodology note: "historical drift" construction

`margin_simulation.py`'s `simulate()` implements no trim/rebalance-down logic at all outside an active repayment model (verified before this run; the only sell path is `_fund_repayment()`, unused here since no repayment model runs in any scenario below). Every scenario in this harness already runs "un-trimmed" by construction — there is no separate "disable the trim rule" step to take, because none exists to disable. **Scenario A's own natural, un-inflated NVDA/semis weight trajectory below is this research's "historical drift" evidence** — not a shortcut, a disclosed fact about this harness's actual mechanics.

NVDA baseline target share: **3.73%** of book (time-above-threshold reference, 1.5x this value = **5.60%**, reusing the real T1/T2 ceiling multiplier as a measurement reference only — no rule implemented). NVDA's real historical max drawdown in this window: **-66.4%** (the historical-primary stress magnitude for stress case 1, per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §2a).

## Scenario results

| Scenario | Ann. TWR | MaxDD | Max concentration | Forced-delev. events | Recovery days |
|---|---:|---:|---:|---:|---:|
| A — control (unlevered) | 30.01% | -22.41% | 33.47% | 0 | 25 |
| B-NVDA — synthetic concentration (unlevered) | 32.84% | -23.06% | 25.10% | 0 | 25 |
| B-semis — synthetic cluster concentration (unlevered) | 33.95% | -23.39% | 52.45% | 0 | 25 |
| C-NVDA-hyp — concentration + hypothetical shock (unlevered) | 30.17% | -19.40% | 25.10% | 0 | 27 |
| D-NVDA-hist — concentration + historical stress + 1.8x margin | 39.70% | -28.20% | 24.28% | 0 | 33 |
| D-NVDA-hyp — concentration + hypothetical shock + 1.8x margin | 36.46% | -23.97% | 24.28% | 0 | 28 |
| D-semis-hist — cluster concentration + historical stress + 1.8x margin | 39.04% | -28.09% | 56.58% | 0 | 33 |

## Time above concentration thresholds

| Scenario | NVDA time above 1.5x target share | Semis time above 25% cluster cap |
|---|---:|---:|
| A (control) | 61.7% | 14.0% |
| B (synthetic concentration) | 100.0% | 100.0% |
| D (concentration + margin) | 100.0% | 100.0% |

## Required stress cases

1. **Single largest holding drawdown** — historical primary: NVDA's real -66.4% decline, embedded in B-NVDA/D-NVDA-hist's real price data. Hypothetical secondary (robustness only, per the stress methodology hierarchy): a constructed -40% shock over 15 days, C-NVDA-hyp/D-NVDA-hyp.
2. **Multiple correlated holdings drawdown** — B-semis/D-semis-hist, using the real, existing semis cluster (unmodified cap, used only as a measurement reference in the time-above-threshold table above).
3. **Market drawdown with concentrated exposure** — see the dedicated section below; measured as a windowed view of D-NVDA-hist's own series, not a separate simulation run.
4. **Concentration increase without leverage increase** — directly the A vs. B-NVDA comparison (both unlevered): MaxDD gap -0.65pp, classified **suggestive** against the 2.0pp/0.5pp materiality bands.

### Stress case 3 detail: market drawdown with concentrated exposure

Control's (Scenario A) own worst portfolio-level drawdown episode troughs at simulated day index 968. At that same point in D-NVDA-hist (concentrated + margin), NVDA concentration was **17.49% of book**, leverage was **1.300x** — i.e., what the concentrated, levered account looked like during the account's own worst broad-market episode in this window, not a separately constructed shock.

## Materiality evaluation

Per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`: material threshold 2.0pp, noise floor 0.5pp, forced-deleveraging repetition = ≥3 events in one stress case OR events in ≥2 of the 4 stress cases.

| Comparison | MaxDD gap | Classification |
|---|---:|---|
| B (concentration alone) vs. A (control) | -0.65pp | suggestive |
| D-hist (concentration+margin+historical stress) vs. B | -5.14pp | material |
| D-hyp (concentration+margin+hypothetical stress) vs. B | -0.91pp | suggestive |

Forced-deleveraging events by stress case: stress_case_1_historical=0; stress_case_1_hypothetical=0; stress_case_2_cluster=0; stress_case_4_concentration_only=0. Repeated (per §5's definition): **False**.

Recovery materiality: D-hist vs. A baseline recovery — **False** (D-hist recovery: 33, A baseline recovery: 25). D-hyp vs. A baseline recovery — **False** (D-hyp recovery: 28).

## Outcome: **Evidence inconclusive**

Per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6's three-way framework: "Evidence supports" requires a material MaxDD gap AND repeated forced-deleveraging events (both, not either alone, per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §5's necessary-not-sufficient framing). "Evidence does not support" requires every relevant gap at or below the noise floor with no event repetition. Anything else is "Evidence inconclusive." **This outcome is not a doctrine change, is not a recommendation, and does not modify any production file** — per the standing rule, acting on it (in either direction) requires its own separate, explicit approval step.

## Limitations

- **One window, one construction per dimension.** 2021-2026, one concentrated single-name pick (NVDA) and one cluster pick (semis) — not a sweep across possible concentrated names or clusters.
- **Numeric parameters (3.0x NVDA multiplier, 1.8x semis multiplier, -40%/15-day hypothetical shock) were chosen this session**, flagged explicitly as session choices per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md`'s disclosure discipline, not separately pre-approved beyond the general Phase 4A execution go-ahead.
- **The hypothetical shock has no modeled recovery** — it holds the shocked price level flat for the remainder of the series (`apply_synthetic_shock()`'s documented simplification), which differs from the historical-primary arm where NVDA's real price path does recover.
- **Time-above-threshold reference values (1.5x NVDA target share, 25% semis cap) are existing real doctrine numbers reused for MEASUREMENT ONLY** — no rule was implemented, no cap was changed.
- **`margin_state.py`'s `concentration_risk_score()` was not called** — per the resolution document, that scorer stays read-only/reference-only and is not imported into this isolated simulation harness.
- No transaction-cost or tax model exists anywhere in this repo — any forced-deleveraging or stress-driven trading implied by this research's findings carries the same unpriced-cost caveat `docs/PHASE4_READINESS_REVIEW.md` already raised for Model B/C.

_Advisory-adjacent research only. This report places no orders and makes no recommendation. Execute nothing based on this document alone._
