# Margin Intelligence Engine — Design Document

_2026-07-17 · Revision 2 — reframed explicitly as risk governance, not timing, per direct instruction. Planning/design pass only, no code changed. Inspection basis (unchanged from Rev 1): `CLAUDE.md` doctrine + Decisions Log, `allocate.py`'s `margin_capacity()`, `targets.yaml`'s `margin:` block, `holdings.yaml`'s live margin state, all six `backtest_*.py` scripts, `test_margin.py` (12 tests, all passing)._

**Governing constraint, stated once and held throughout this document:** margin intelligence is a **risk governance system**. It answers "how much risk is this account currently carrying, and what does that require" — never "does now look like a good time to borrow more." Every component below is checked against that line before it's included.

---

## 1. Architecture proposal

Four components, each a pure function or a thin composition of pure functions, mirroring how `margin_capacity()` itself is built — no hidden state, no I/O inside the math, same testability bar as everything else in this system.

```
                     ┌─────────────────────────┐
holdings.yaml ──────▶│  RiskInputs (assembly)   │◀────── targets.yaml (caps, thresholds)
(debt, buffer_pct)   │  gross, net_equity,      │
                     │  cluster values, T1/T2   │
                     │  current/target ratios   │
                     └───────────┬─────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 ▼                               ▼
   ┌─────────────────────────┐    ┌──────────────────────────┐
   │ ConcentrationRisk (§5)   │    │  margin_capacity()        │
   │  -> single risk score,   │    │  (EXISTING, unchanged)     │
   │  portfolio-level only    │    │  -> net_equity, allowed,   │
   └───────────┬─────────────┘    │     forced, block_reason   │
               │                   └─────────────┬─────────────┘
               └───────────────┬─────────────────┘
                                ▼
                  ┌──────────────────────────┐
                  │  MarginStateClassifier     │
                  │  -> Normal / Elevated /    │
                  │     Forced Deleveraging    │
                  └───────────┬───────────────┘
                                ▼
                  ┌──────────────────────────┐
                  │  RepaymentCalculator        │
                  │  (only invoked when state   │
                  │   is Elevated or Forced)    │
                  │  -> recommended paydown $,   │
                  │     or trim-proceeds split   │
                  └───────────┬───────────────┘
                                ▼
                      render() displays state +
                      recommendation (informational
                      unless Forced, which already
                      blocks margin buys today)
```

**Design principle behind this shape:** `margin_capacity()` is not modified — it already correctly answers "how much margin is allowed right now" and every existing test depends on its exact current signature and behavior. The new components sit *around* it, consuming its outputs (`net_equity`, `forced_delever`) and `holdings.yaml`/`targets.yaml` inputs it doesn't currently need, and producing a state label + an optional dollar recommendation that `render()` displays. This keeps the blast radius of Phase 2 confined to new, additive code plus one new field on the existing return contract, rather than touching the load-bearing function itself.

**Why ConcentrationRisk is a separate component from MarginStateClassifier:** concentration (cluster caps, T1/T2 ceiling proximity) is portfolio composition risk; leverage/buffer is capital structure risk. They're related — a concentrated book under leverage is the exact tail scenario `t1t2_trim_backtest.md`'s NVDA decomposition surfaced — but they're measured from different inputs and should stay independently testable. The classifier combines them; it doesn't compute them.

---

## 2. Data requirements

| Data | Source | Already available? | Notes |
|---|---|---|---|
| Margin debt | `holdings.yaml` → `margin.debt` | Yes | Synced manually via `update-margin`, never derived. |
| Buffer % | `holdings.yaml` → `margin.buffer_pct` | Yes | Robinhood-displayed only, per standing doctrine. |
| Margin sync date | `holdings.yaml` → `margin.synced_at` | Yes | Already used for the existing staleness warning (`STALE_MARGIN_DAYS`). |
| Gross holdings value | Computed live every run (`resolve_holdings()`) | Yes | No new fetch needed. |
| Net equity | `gross − debt` | Yes | Already computed in `margin_capacity()`. |
| Leverage cap, buffer floor | `targets.yaml` → `margin:` | Yes | Existing config. |
| Cluster values + caps | Computed live in `plan()` (`cluster_value`, `caps.clusters`) | Yes | Already used for cluster-cap trims. |
| T1/T2 current/target ratios | Computed live in `plan()` (the ceiling check) | Yes | Already used for the T1/T2 ceiling trim. |
| **New:** state thresholds (Normal/Elevated boundary) | `targets.yaml` → new `margin:` sub-keys | **No — needs to be added** | See Formulas §3; must be explicit config, not a hardcoded constant, matching how `leverage_cap`/`buffer_floor_pct` are already externalized. |
| **New:** repayment target buffer (how far above the floor a recommended paydown should restore to) | `targets.yaml` → new `margin:` sub-key | **No — needs to be added** | Prevents a paydown recommendation that lands exactly at the floor and immediately re-triggers on the next price wiggle. |
| **New:** repayment-redirect fraction (Section 4's proportional trim-proceeds rule) | `targets.yaml` → new `margin:` sub-key | **No — needs a backtest verdict before any default is chosen** | Do not default this to a guessed number; Phase 3 below exists specifically to produce evidence for it. |
| **New:** historical daily account-value series for backtesting | `data/backtest/*.json` (existing cache) + a to-be-built margin/debt simulation layer | **Partially** — price data exists; there is no historical margin-debt or buffer series anywhere, live or cached | This is the biggest data gap. Backtesting margin behavior requires *simulating* debt/leverage/buffer through the historical window — the account's real margin history before 2026-07-13 isn't reconstructable (`CLAUDE.md`: the debt was "discovered," not tracked from origin). All margin backtests will simulate a hypothetical account running the rule being tested from day one of the window, the same way every existing backtest simulates a hypothetical portfolio — not attempt to replay this specific account's real history. |

No new external data source is required — no new API, no new vendor. The one real gap is a simulated-margin-state layer inside the backtest framework, which is new code, not new data.

---

## 3. Formulas

All formulas here are either (a) already implemented and unchanged, cited for completeness, or (b) new and marked as such.

**Leverage ratio** (existing, `margin_capacity()`):
```
leverage = gross / net_equity          where net_equity = gross − margin_debt
```

**Margin utilization** (new — how much of the *allowed* margin is actually drawn, distinct from leverage itself):
```
utilization = margin_debt / max_allowed_debt
where max_allowed_debt = leverage_cap × net_equity − (gross − margin_debt)
                        = leverage_cap × net_equity − net_equity
                        = net_equity × (leverage_cap − 1)
```
i.e., `utilization = margin_debt / (net_equity × (leverage_cap − 1))`. This is the cleanest single number for "how much of the structural ceiling is in use" — 0% means no margin drawn, 100% means exactly at the cap, >100% means over the cap (should not occur given `margin_capacity()`'s existing clipping, but is a valid computed value for display/diagnostics).

**Concentration risk score** — `ConcentrationRisk`, new, addresses Goal 5 (Section 5 below has the full design; formula here for completeness):
```
proximity(cluster) = cluster_value / cluster_cap_dollars           (dimensionless, ~0 to 1+)
proximity(T1/T2 name) = (current / target) / t1t2_trim_mult        (dimensionless, ~0 to 1+)

concentration_score = max( all proximity(cluster), all proximity(T1/T2 name) )
```
A single number: how close is the *tightest currently active constraint* to breaching. 1.0 means some cap is exactly at its limit; below 1.0 means every cap has room; the formula deliberately takes the **max**, not an average, because portfolio risk is dominated by its worst concentration, not its typical one — consistent with how `t1t2_trim_backtest.md` singled out NVDA specifically rather than reporting an average T1/T2 overweight.

**Margin state classification** — new:
```
inner_threshold = leverage_cap × base_fraction × (1 − k × concentration_score)
                   floored at leverage_cap × min_fraction

where base_fraction (e.g. 0.80) and min_fraction (e.g. 0.50) and k (e.g. 0.25)
are explicit targets.yaml constants, not hardcoded

state =
  Forced Deleveraging   if buffer_pct < buffer_floor_pct               (existing rule, unchanged)
  Elevated              if leverage > inner_threshold
                         OR buffer_pct < buffer_floor_pct × comfort_multiplier   (e.g. 1.5×)
  Normal                otherwise
```
The `(1 − k × concentration_score)` term is the whole mechanism for Goal 5: a concentrated book tightens the Normal→Elevated boundary — the *same* leverage ratio is treated as riskier when the portfolio is concentrated than when it's diversified — without ever computing or displaying a per-ticker leverage number. Concentration modulates the *threshold*, not the *leverage calculation itself*, which stays a pure account-level ratio.

**Repayment amount** — new (only computed when state ≠ Normal):
```
target_buffer_pct = buffer_floor_pct × repayment_target_multiplier   (e.g. 1.5x → 45% if floor is 30%)

recommended_paydown = margin_debt − debt_at_target_buffer

# Robinhood's buffer formula isn't independently derivable (documented, standing
# constraint in write_state()'s comment) — so this cannot be solved in closed
# form from buffer_pct alone. Two honest options, not one guessed formula:
#   (a) leverage-based proxy: solve for the debt level that would bring
#       leverage down to inner_threshold instead of solving for buffer directly,
#       and clearly label the output as a leverage-based estimate, not a
#       buffer-based guarantee.
#   (b) display a recommended payment RANGE bounded by the leverage-based
#       estimate on one side, and flag "verify resulting buffer on Robinhood
#       after any paydown" the same way every margin-buy warning already
#       does for buffer accuracy.
# Recommend (b) — it's honest about the real constraint instead of presenting
# a precise-looking number built on an admittedly unreconciled formula.
```

**Repayment-redirect (trim proceeds → debt)** — new, parameterized, value TBD by backtest:
```
if state == Elevated:
    to_debt = trim_proceeds × redirect_fraction     (redirect_fraction from targets.yaml,
                                                       chosen by Phase 3's backtest, not guessed)
    to_redeploy = trim_proceeds × (1 − redirect_fraction)
elif state == Forced:
    to_debt = trim_proceeds                          (100% — consistent with the existing
                                                       "no margin-funded buying, full stop"
                                                       treatment of Forced Deleveraging)
    to_redeploy = 0
else:  # Normal
    to_debt = 0
    to_redeploy = trim_proceeds                       (current behavior, unchanged)
```

**New backtest metrics** (all new, none exist in the repo today — confirmed via grep):
```
daily_return[i] = value[i] / value[i-1] - 1                  (excluding deposit-flow days,
                                                                same convention as twr_annualized)
volatility_annualized = stdev(daily_return) × sqrt(252)

sharpe = (annualized_TWR - risk_free_rate) / volatility_annualized
         risk_free_rate = 0.0, explicitly, disclosed in every report header
         (see Rev 1 §9 — a real T-bill rate is its own undisclosed assumption
         if picked silently; 0% is the honest default until decided otherwise)

time_underwater = count(value[i] < running_max(value[0..i])) / len(value)

leverage_exposure_series[i] = gross[i] / net_equity[i]   (full time series, not just its max —
                                                            "how often did this arm run hot"
                                                            is a different question from
                                                            "how hot did it get once")
```

---

## 4. Test plan

**Pure-function unit tests (write before any integration, same discipline as `test_margin.py`'s existing 7 for `margin_capacity()`):**

| Function | Test cases required |
|---|---|
| `concentration_risk_score()` | All clusters/T1T2 names under cap → score < 1.0, matches the single tightest name. Exactly one cluster at cap → score == 1.0. Empty roster/no clusters → score == 0.0 (not an error, not None). |
| `classify_margin_state()` | Buffer below floor → Forced, regardless of leverage. Leverage above inner threshold, buffer healthy → Elevated. Both healthy → Normal. Concentration score at max (1.0) tightens the boundary — a leverage level that would be Normal at concentration 0.0 becomes Elevated at concentration 1.0 (this is the one test that directly verifies Goal 5's mechanism works). Boundary values (exactly at `inner_threshold`, exactly at `buffer_floor_pct × comfort_multiplier`) — same "exactly at floor is not forced" precedent `test_margin.py` already set. |
| `recommended_paydown()` | Forced state with a known debt/leverage produces the expected leverage-based estimate. Normal/Elevated states return `None`/no recommendation (only Forced computes a hard number, per the architecture). |
| `repayment_split()` | Normal → 100% redeploy. Elevated → split matches `redirect_fraction` exactly, for at least two different fraction values (proves it's parameterized, not hardcoded). Forced → 100% to debt. |
| New backtest metrics (`volatility`, `sharpe`, `time_underwater`) | Each against a **hand-computed small example** before trusting it in a real backtest — same standard `test_indicators.py`'s RSI-of-flat-series case was built to enforce. E.g., volatility of a constant-return series should be 0; Sharpe of a series with 0% return and 0% risk-free rate should be 0 (or explicitly undefined/None if volatility is 0 — decide and test the divide-by-zero case explicitly, don't let it silently produce `inf`/`NaN`). |

**Backtests (formalized from Rev 1's evaluation, three arms confirmed in-scope):**

1. **Sustainable leverage caps** — is the current fixed 1.8x cap actually sustainable, or does it produce dangerous single-position outcomes under historical stress. Arms: A (no margin, cash-only baseline) vs. B (current: fixed 1.8x cap, static) vs. C (mechanical concentration-adjusted cap — the `inner_threshold` formula above, applied as an actual leverage ceiling rather than just a state-classification boundary, i.e. testing whether the Goal-5 mechanism should also throttle *deployment*, not just *display*, an open design question this backtest can help answer). **Pre-committed rule:** adopt C over B only if it improves MaxDD by >1.0pp without costing more than 1.0pp of TWR (the `t1t2_trim_backtest.md` asymmetric-tolerance pattern, appropriate here since the whole point of C is trading a little return for materially less tail risk).

2. **Forced deleveraging avoidance** — does *any* tested rule (A/B/C above, plus the repayment arms below) reduce the frequency or severity of hitting the Forced state, versus just hitting it and reacting. **Metric, new and central to this arm specifically:** count of Forced-state trigger events per arm, and the deployment-cash lost while Forced (days blocked × average deployable dollars) — this arm is explicitly about avoidance, so time-in-Forced-state is the primary metric, not TWR.

3. **Repayment policies** — Rev 1's arm 5, unchanged: A (no repayment redirect, current) vs. B/C/D (redirect fractions, e.g. 25%/50%/100%, only while Elevated). **Pre-committed rule:** same TWR/MaxDD tolerance pattern, plus the new time-underwater and leverage-exposure-series metrics, plus **interest cost avoided** (debt × ~5% APR × time carried) as a directly dollar-denominated secondary metric this system has never measured before.

4. **Margin drag vs. unlevered baseline** — the most fundamental question, restated from Rev 1's arm 2 with a sharper name: does carrying margin at all, under every governance rule this design proposes, beat a pure cash-only account on a risk-adjusted basis (Sharpe, not just raw TWR) — margin costs real interest (~5% APR) and adds tail risk; the question this arm answers is whether the current doctrine's premise ("margin as fuel within a fixed cap") is actually supported by evidence or just inherited from the debt already existing when discovered. **This should run first, before 1-3** — if margin doesn't clear a risk-adjusted bar at all, the other three arms are optimizing a mechanism that maybe shouldn't exist at its current size in the first place.

**Explicitly not in the test plan** (per the reaffirmed constraint): no arm tests margin deployment as a function of regime, volatility, drawdown-as-entry-signal, or valuation. If a future arm's design would only make sense by reading current price direction as a buy/hold signal for *borrowed* capital specifically, it does not belong in this framework, full stop — this is the line the whole document is built to hold.

---

## 5. Portfolio risk contribution without ticker-level leverage (Goal 5, full design)

The naive framing — "how much leverage does each ticker have" — is wrong on its face: margin debt is a single account-wide liability against the whole portfolio's collateral value, not a loan against any specific position. Robinhood doesn't allocate the debt to AAPL vs. NVDA, and neither should this system. Assigning a per-ticker leverage figure would be inventing a number that doesn't correspond to anything real in the account.

What's real and worth capturing instead: **some holdings, by virtue of their concentration, make the account's existing leverage more dangerous than others would at the same leverage ratio.** This is exactly the NVDA finding in `t1t2_trim_backtest.md` — the account-level leverage (1.44x) was unremarkable, but NVDA's own position size (2.14x its target) combined with its own historical worst-case drawdown (-66.4%) made *that specific concentration*, under the account's *actual* (unremarkable) leverage, into a forced-liquidation-territory risk. The insight isn't "NVDA has 1.44x leverage" (meaningless) — it's "the account's leverage, applied to a book this concentrated in one name, is riskier than the same leverage applied to a diversified book."

**The design (formalized above in Section 3, restated here as the concept):**
- `concentration_risk_score()` reads the *existing* cluster caps and T1/T2 ceiling infrastructure — it introduces no new position-level risk math, only aggregates outputs that `plan()` already computes for an unrelated purpose (deciding whether to trim).
- The score is portfolio-level: one number, "how close is the tightest constraint," never a per-ticker output.
- That single number feeds the margin state classifier's *threshold*, not the leverage calculation. Leverage stays `gross / net_equity`, computed exactly as today, for the whole account. Concentration only ever makes the state boundary *tighter* (never looser — there is no direction in which high concentration should widen how much leverage is treated as "fine"), which keeps this squarely a risk-reduction mechanism, not a new lever-up justification.
- This is fully backward-compatible with every existing cap: it doesn't change what a cluster cap or the T1/T2 ceiling *does* (they still trim exactly as they do today, independent of margin state) — it only changes what the *margin state display* says given that those caps are currently near their limits.

---

## 6. Implementation phases

Numbered and gated — each phase produces a concrete artifact (tests passing, or a backtest verdict) before the next phase starts, matching the Phase 1 cleanup's "small, logically grouped, verified before proceeding" discipline.

**Phase 2a — Pure functions + unit tests, zero integration.**
`concentration_risk_score()`, `classify_margin_state()`, `recommended_paydown()`, `repayment_split()`, plus the new backtest metrics (`volatility`, `sharpe`, `time_underwater`, leverage-exposure series). All in isolation, all tested per Section 4's table, none called from `plan()`/`render()`/any backtest yet. Deliverable: a new test file (or extension of `test_margin.py`) with every case in Section 4's table passing.

**Phase 2b — Backtest simulation layer.**
The one real new-code item Section 2 flagged: a way to simulate a hypothetical margin-debt/leverage/buffer trajectory through the historical bar-cache window, since no real historical margin series exists to replay. Deliverable: a shared simulation function (candidate home: alongside the other shared helpers in `backtest_regime.py`) that the four backtest arms in Section 4 can all build on, with its own test verifying it produces sane leverage/debt values given a known synthetic price path before it's trusted for the real arms.

**Phase 2c — Run the four backtests, in the order Section 4 specifies (margin-drag-vs-baseline first).**
Each gets its own script (`backtest_margin_drag.py`, `backtest_margin_sustainability.py`, `backtest_margin_forced_deleverage.py`, `backtest_margin_repayment.py` — one file per question, matching the existing convention), its own pre-committed threshold stated before results, its own report in `reports/`. Deliverable: four verdicts, each written up in `CLAUDE.md`'s Decisions Log the way every prior backtest has been — including an honest "no change" outcome if that's what the evidence shows, exactly as `weight_backtest.md` and `t1t2_trim_backtest.md`'s return-question arms did.

**Phase 2d — Informational integration only.**
Wire `concentration_risk_score()` and `classify_margin_state()` into `render()` as a new display line (state label, informational), with **no behavior change** — margin buys/blocks still come entirely from the existing, unmodified `margin_capacity()`. This phase is intentionally separable from anything that changes what the system *does*, so it can ship even if Phase 2c's backtests are still in progress or produce mixed results.

**Phase 2e — Behavioral integration, only for verdicts that survived Phase 2c.**
If (and only if) a backtest supports it: wire `recommended_paydown()` into the existing Forced-state message (upgrading it from a block notice to a block notice + a number), and/or wire `repayment_split()` into `plan()`'s trim-proceeds handling at the backtest-chosen `redirect_fraction`. Each is its own commit. Neither ships without its own passing backtest verdict and its own Decisions Log entry, per the standing "verdicts are never auto-applied" rule.

**Phase 2f — Doctrine + README update.**
`CLAUDE.md` gets explicit new lines for the state definitions and repayment rule (matching the T1/T2 ceiling entry's precision about what was/wasn't backtested). `README.md`'s margin section gets updated to describe the shipped states/repayment behavior — done as its own step so it can't drift the way the pre-Phase-1 README did.

---

## 7. Conflicts with existing doctrine

Reaffirming Rev 1's findings under the sharper "risk governance only" framing this revision was built around — nothing here has softened, if anything it's more explicit:

1. **No "Opportunistic" state, no lever-up-on-signal logic, anywhere in this revision.** Every state transition and every formula in Sections 3-5 moves in the risk-reducing direction only (tighter thresholds under concentration, redirect-to-debt under elevated leverage) — there is no formula in this document that widens the leverage ceiling or loosens a threshold in response to any market condition.
2. **Backtest arms "margin only during drawdowns" and "margin deployment based on regime" remain excluded, not merely deprioritized.** They're not in Section 4's four-arm test plan at all. Restated per the explicit new instruction: this isn't a scheduling choice, it's a scope boundary.
3. **The repayment-redirect fraction and the concentration-adjusted leverage cap (arm 1's Arm C) are both parameterized, evidence-gated values — no default is proposed in this document.** Picking either number without Section 4's backtests would itself be a small, unearned timing-adjacent judgment call; the design deliberately leaves both blank pending evidence.
4. **The repayment-amount formula (Section 3) is honest about a real limitation** — Robinhood's buffer formula can't be independently derived (standing, documented constraint), so the recommendation is framed as a leverage-based estimate with a verify-on-Robinhood caveat, not a precise-looking number built on a formula this codebase has already found doesn't reconcile.
5. **Margin drag vs. unlevered baseline (Section 4, arm 4) is sequenced first, ahead of the sustainability/repayment arms, on purpose** — it's the test that could, in principle, produce evidence *against* carrying margin at all. Sequencing it last would have looked like optimizing a foregone conclusion; sequencing it first keeps the process honest about the fact that "margin is allowed" was a 2026-07-13 doctrine choice made when the debt was discovered already existing, not a choice made *because* evidence supported it.

---

Nothing in this document has been implemented. Awaiting your decision on what from the six-phase plan (Section 6) gets built, and in what order.
