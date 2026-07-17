# Phase 3 Scenario Manifest

_2026-07-17 · Documentation only. No backtests run, no code changed. This is the authoritative, execution-ready parameter set for Scenarios A/B/C/D — it resolves `docs/PHASE3C_SCENARIO_CONFIGURATION.md`'s Open Items (Model B/C thresholds, decision-threshold confirmation) with the initial values supplied for this phase, and is the document a future execution phase implements and runs against. Supersedes the "Open Items — must resolve before D can run" section of that document for the items resolved below; that document's shared-configuration table (universe, window, weights, trim rule, deposit cadence) is unchanged and still authoritative for everything not restated here._

---

## 1. Parameters

### Shared (all scenarios) — unchanged from `PHASE3C_SCENARIO_CONFIGURATION.md`

63-ticker universe, no crypto, 2021-2026 window, $2,000/mo deposits, current production tier weights (T1 3.35/T2 1.65/ETF 2.30/band 0.75/spec 1.00), band/spec trim rule (1.25×/RSI>60), T1/T2 ceiling and cluster caps excluded from the simulated trim logic, regime/trend gates excluded, $1 min-lot, $0 starting capital. Not repeated in full here — see that document.

### A. Unlevered baseline
No new parameters. `leverage_cap = 1.0`.

### B. Fixed leverage baseline
`leverage_cap = 1.8`, `repayment = MODEL_0` (none). No new parameters.

### C. Leverage sweep
`leverage_cap ∈ {1.2, 1.4, 1.6, 1.8, 2.0}`, `repayment = MODEL_0` at every level. No new parameters.

### D. Repayment models — resolved parameters

| Model | Parameter | Initial value | Sweepable? |
|---|---|---|---|
| MODEL_0 (control) | — | no active repayment | — |
| MODEL_A | breach threshold | leverage_cap (1.8x) — repay only the minimum to clear a breach | No — this is the hard doctrine cap, not a test parameter |
| **MODEL_B — Profit Harvest** | trigger | new portfolio high-water mark (HWM) of book value | No |
| | repay fraction (`R`) | **25%** of gains above the prior HWM | **Yes** — sweep set `{10%, 25%, 50%}`; 25% is this phase's single initial run |
| | borrowing behavior | no additional borrowing — the reset never opportunistically draws margin beyond what deposit-driven allocation gaps already require | No |
| **MODEL_C — Risk Reset** | trigger | portfolio drawdown from its own HWM exceeds **15%** | No |
| | target leverage after reset | **1.25x** | No — fixed for this phase; a future sweep is not scoped here |
| | restoration condition | requires BOTH (a) book value reaches a NEW HWM (exceeds the pre-drawdown peak, not merely recovers to it) AND (b) leverage has remained at or below 1.25x continuously since the reset (this session's specific, dependency-free operationalization of "normalized conditions" — see §3 Assumptions) | No |
| | dip-buying | explicitly **prohibited** — the drawdown trigger may only ever delever (reduce leverage), never justify a margin-funded buy during or immediately after the drawdown | No — structural guarantee, see §5 |

### Concentration (Test D interaction dimension)

| Parameter | Value | Status |
|---|---|---|
| Cluster concentration stress trigger | **30%** of book, for any tracked cluster | **Test parameter, explicitly not doctrine** — distinct from and does not modify the real `targets.yaml` cluster caps (semis 25% / power_infra 20% / oil 20%). This threshold exists only inside Test D's concentration-interaction runs; it never feeds into Model C's drawdown trigger for this phase's initial parameter set (see §3, interpretation note) — conflating the two would blend two separately pre-committed thresholds into one, which the standing "one test one verdict" discipline exists to avoid. |

### Decision threshold (all of A/B/C/D)

**2.0 percentage points TWR difference OR 2.0 percentage points MaxDD improvement** — whichever is met first triggers considering the variant "adopted" for further discussion. Explicitly labeled, per instruction: **a decision threshold, not a proof threshold.** It answers "is the effect large enough, in this one sample window, to be worth acting on" — the same epistemic posture as every "one window, one sample" caveat already standing in this repo's other backtest reports (`regime_backtest.md`, `t1t2_trim_backtest.md`), not a claim of statistical significance or robustness across market regimes. This is stricter than the repo's standard 1.0pp/1.0pp pattern (used for A/B/C, gate/trim/weight questions already closed) because Scenario D's repayment models carry more mechanism risk (proactive selling into a drawdown) than a passive gate or a static weight — same reasoning `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.D originally proposed for the concentration test specifically, now applied uniformly across all of D's repayment-model comparisons per this instruction.

---

## 2. Formulas

Notation: `book(t)` = net_equity(t) + cash(t) (matches `margin_simulation.PortfolioState.book`). `HWM(t)` = running high-water mark of `book`, initialized to `book(0)`.

### Model B — Profit Harvest

```
HWM(0) = book(0)
for each day t:
    if book(t) > HWM(t-1):
        gain          = book(t) - HWM(t-1)
        repay_amount  = R * gain           # R = 0.25 (initial), sweepable {0.10, 0.25, 0.50}
        HWM(t)        = book(t)
    else:
        repay_amount  = 0
        HWM(t)        = HWM(t-1)
    margin_debt(t) = max(0, margin_debt(t) - repay_amount)
```
"No additional borrowing" is satisfied structurally, not as a separate check: `repay_amount` only ever reduces `margin_debt`; nothing in this formula increases it. Margin draws in Model B still occur, exactly as in every other scenario, only through the shared deposit-driven allocation step (funding a computed target gap) — this model does not add a second, opportunistic borrowing path.

### Model C — Risk Reset

```
HWM(0) = book(0)
reset_active = False
pre_drawdown_HWM = None

for each day t:
    HWM(t) = max(HWM(t-1), book(t))
    drawdown(t) = (HWM(t) - book(t)) / HWM(t)   # 0 if book(t) >= HWM(t)

    if not reset_active and drawdown(t) > 0.15:
        # trigger fires ONCE per drawdown episode (on the crossing day only,
        # not every day the account remains >15% below peak) -- see §3.
        pre_drawdown_HWM = HWM(t)
        target_debt = gross(t) - gross(t) / 1.25
        repay_amount = max(0, margin_debt(t) - target_debt)
        margin_debt(t) = margin_debt(t) - repay_amount
        reset_active = True

    if reset_active:
        # restoration: BOTH conditions must hold before margin can be
        # redrawn back toward the scenario's normal 1.8x cap
        new_all_time_high = book(t) > pre_drawdown_HWM
        leverage_normalized = (leverage_ratio(t) is None) or (leverage_ratio(t) <= 1.25 + epsilon)
        if new_all_time_high and leverage_normalized:
            reset_active = False   # deposit-driven allocation may resume drawing up to 1.8x
        else:
            effective_leverage_cap(t) = 1.25   # clamps this day's deposit-driven margin draw, if any
```
While `reset_active` is True, the scenario's deposit-allocation step (shared across all scenarios) uses `effective_leverage_cap = 1.25` instead of the scenario's normal 1.8x — this is the mechanism that satisfies "no dip-buying interpretation" (§5): the account cannot lever back up past the reset target until both restoration conditions are independently met, and even then only back to the scenario's normal cap, never as a reaction to the dip itself (the trigger for resuming normal capacity is a NEW high, i.e. the drawdown being fully over, not the drawdown itself or its depth).

### Concentration stress (Test D, separate run)

```
for each tracked cluster c:
    cluster_pct(t) = cluster_value(t) / book(t) * 100
    stress_event(t, c) = cluster_pct(t) >= 30.0
```
Used only as an input/co-factor for Test D's dedicated concentration-interaction analysis (per `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.D) — not wired into Model C's own trigger condition for this phase's initial run (see §3).

---

## 3. Assumptions

Labeled per `docs/PHASE3C_ASSUMPTION_REGISTRY.md`'s three-way scheme (Known / Estimated / Hypothetical); every new value this manifest introduces is added here rather than silently assumed known.

| # | Assumption | Label | Basis |
|---|---|---|---|
| 1 | Model B repay fraction R = 25% (initial run) | **Hypothetical** | User-supplied initial parameter, explicitly stated as sweepable ({10%, 25%, 50%}) — not derived from any backtest evidence yet |
| 2 | Model C drawdown trigger = 15% | **Hypothetical** | User-supplied initial parameter |
| 3 | Model C target leverage after reset = 1.25x | **Hypothetical** | User-supplied initial parameter |
| 4 | Model C trigger fires once per drawdown episode (not every day below threshold) | **Hypothetical — this session's interpretation, not user-specified** | The instruction said "trigger: 15% portfolio drawdown from peak" without specifying re-fire behavior. Firing once avoids a repeated forced-sell-into-further-decline pattern each day the account remains deep in drawdown, which would itself look like a second, undisclosed policy decision (aggressive compounding delever) rather than the described single reset-and-restore mechanic. Flagged explicitly so a future review can override this interpretation if it doesn't match intent. |
| 5 | "Normalized conditions" operationalized as: leverage has stayed at/below 1.25x continuously since the reset | **Hypothetical — this session's interpretation, not user-specified** | The instruction named "normalized conditions" without a formula. Chose a dependency-free definition (derivable purely from the simulation's own leverage series) over introducing an untested volatility or market-regime metric, which would add a second undocumented model dimension. Flagged for override. |
| 6 | Restoration requires a NEW high (exceeding the pre-drawdown HWM), not merely a recovery back to the old HWM | **Known** — directly follows from the literal instruction text ("requires new equity high"), not an interpretation | User-specified |
| 7 | Concentration stress trigger (30%) is NOT wired into Model C's own trigger for this phase's initial run — reserved for Test D's separate concentration-interaction analysis | **Hypothetical — this session's interpretation, not user-specified** | The instruction listed the 30% concentration trigger under its own heading, separate from Model C's drawdown trigger, and `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §1.D already scopes concentration interaction as its own, later-sequenced test. Blending the two into one trigger would conflate two independently pre-committed thresholds. Flagged for override if the intent was a combined trigger. |
| 8 | Decision threshold (2.0pp TWR OR 2.0pp MaxDD improvement) applies uniformly to all of Scenario D's model comparisons, not only the concentration test | **Hypothetical — this session's interpretation, not user-specified** | The instruction stated the threshold without scoping it explicitly to "D" vs. "concentration only." Applied uniformly since D's models (B, C) share the same proactive-selling mechanism risk that justified the original stricter-than-1.0pp proposal in the framework doc. Flagged for override. |
| 9 | 5.00% APR / $1,000-free interest term, all other shared parameters | Unchanged — see `PHASE3C_ASSUMPTION_REGISTRY.md` | Carried forward, not re-labeled here |

---

## 4. Limitations

1. **Harness gap, not yet closed.** `margin_simulation.py`'s current `repayment_model_b()` (target-leverage-threshold mechanic) and `repayment_model_c()` (single-day-gain/concentration-score trigger mechanic), built in Phase 3B, do **not** implement the HWM-gains-repay and drawdown-triggered-reset-with-restoration mechanics this manifest specifies. This manifest defines the target formulas a future harness-extension phase must implement and test — it does not itself change `margin_simulation.py`. Scenario D cannot execute until that extension exists and has its own passing unit tests, matching the same "tests before integration" discipline used for `margin_state.py` (Phase 2B/2C/2D).
2. **`reset_active`/HWM state is path-dependent, cross-day state** — unlike every pure function in `margin_simulation.py` today, Model C's restoration logic requires carrying `reset_active`, `pre_drawdown_HWM`, and a running `HWM` across days. The current repayment-model function signature (`(state, prior_gross) -> float`, stateless between calls) cannot express this without a signature change or an explicit external state object threaded through `simulate()`. Flagged as a concrete design question the harness-extension phase must resolve, not glossed over.
3. **The "no dip-buying interpretation" guarantee is a design intent, not yet a tested invariant.** `margin_state.py`'s equivalent guarantee ("no state ever recommends increasing leverage") is backed by a 42,525-combination property test (`test_margin_state.py`). Before Model C's harness code is considered trustworthy, an equivalent property test — proving `effective_leverage_cap` during `reset_active` never exceeds 1.25x, and that resumption never occurs on any signal other than a genuine new high plus normalized leverage — must be written and must pass. Not done this phase (documentation only).
4. **One window, one mostly-rising sample**, same standing caveat as every other document in this project — Model C's 15%-drawdown trigger will fire at most once or twice in the 2021-2026 window (the 2022 stretch is the only real candidate), which is a thin sample for judging a reset-and-restore policy's real behavior.
5. **Concentration stress (30%) is a fixed round number, not derived.** Unlike the real cluster caps (semis 25%/power_infra 20%/oil 20%, each individually justified via correlation scans or stress tests per `CLAUDE.md`'s Decisions Log), this 30% figure is stated by the user as an initial test parameter with no derivation — correctly labeled as such (§1), not dressed up as evidence-based.
6. **Model B's "no additional borrowing" clause has not been stress-tested against the shared deposit-allocation step's own margin-drawing behavior** — in principle a large deposit-driven gap could still draw margin up to 1.8x in the same simulated day a HWM-triggered repayment also fires, partially offsetting each other. The formula in §2 is structurally correct (repayment only subtracts, deposit-funding only adds, both apply independently) but the *net* day-to-day debt path this produces has not been traced by hand or tested — a harness-extension-phase unit test should cover this interaction explicitly.

---

## 5. Output metrics

Same metric set `margin_simulation.SimulationResult.metrics()` already produces (Phase 3B), applied to every scenario/model combination in this manifest:

- `ann_twr_pct` — annualized time-weighted return
- `cagr_pct`
- `max_drawdown_pct`
- `annualized_volatility_pct`
- `time_near_leverage_cap_pct_proxy` — NOT a real buffer% derivation (see `PHASE3C_ASSUMPTION_REGISTRY.md` #14); for Scenario D specifically, this metric is measured against each model's own *effective* cap at each point in time (1.8x normally, 1.25x while `reset_active` under Model C), not a single fixed cap — a harness-extension detail to implement, flagged here so it isn't silently measured wrong
- `worst_case_concentration_impact_pct` — single-name/cluster decomposition, on request, using the concentration stress trigger (§1) as its scoring input for Test D's concentration-interaction runs specifically
- `final_book_value`, `final_margin_debt`, `deposit_total` — accounting totals

**New metrics this manifest requires, not yet in `SimulationResult.metrics()`** (harness-extension-phase work):
- `n_hwm_repayments` and `total_repaid_via_hwm` (Model B) — count and dollar total of HWM-triggered repayments, for auditability
- `n_risk_resets` and `days_in_reset_state` (Model C) — how often the 15% trigger fired and how long the account spent under the tightened 1.25x effective cap before restoration
- `pct_of_window_at_effective_cap_below_normal` (Model C) — what fraction of the whole simulation window Model C spent below its normal 1.8x capacity, a direct measure of the policy's cost in foregone leverage capacity, to weigh against any MaxDD improvement it produces

Every report produced from these metrics carries `HYPOTHETICAL_LABEL` and passes `render_metrics()`'s banned-language check, per `PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §3 and `margin_simulation.py`'s existing enforcement — unchanged by this manifest.

---

## What this manifest deliberately does not do

- Does not modify `margin_simulation.py`, `targets.yaml`, `holdings.yaml`, `allocate.py`, or `margin_state.py`.
- Does not run any scenario or produce any result.
- Does not implement the harness extensions named in §4 item 1 or the property test named in §4 item 3 — both are named as required future work, not done here.
- Does not finalize the Model B sweep ({10%, 25%, 50%}) — only the initial 25% run is scoped for this phase; the sweep itself is future work once a single-value run's mechanics are validated.
- Does not treat the 30% concentration figure, the 15% drawdown trigger, the 1.25x reset target, or the 2.0pp decision threshold as anything other than what they're labeled: test parameters and a decision bar, not doctrine, not proof.

Stopping here. No scenarios executed. This manifest, together with `PHASE3C_SCENARIO_CONFIGURATION.md`, `PHASE3C_DATA_VALIDATION_REPORT.md`, and `PHASE3C_ASSUMPTION_REGISTRY.md`, is the complete pre-execution record for Scenarios A-D. Awaiting approval before any harness-extension work (§4 item 1) or actual scenario execution begins.
