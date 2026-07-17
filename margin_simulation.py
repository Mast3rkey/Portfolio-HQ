"""
margin_simulation.py — isolated hypothetical margin-policy simulation harness.

Phase 3B of the Margin Intelligence Engine work
(docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md). This module exists ONLY to run
assumption-driven, hypothetical simulations of margin policies through REAL
historical price data (data/backtest/*.json). It produces no live
recommendations and is never imported by allocate.py or any live-trading
path.

Explicitly does NOT modify, import from, or depend on:
  - allocate.py       (the live advisory engine)
  - targets.yaml       (live config)
  - holdings.yaml       (live state)
  - margin_state.py     (the live risk-governance classifier)

The leverage-cap math in `_leverage_capped_margin()` below is deliberately
RE-DERIVED, not imported from allocate.py's margin_capacity() — this keeps
the module fully isolated per the Phase 3B scope. The formula matches
margin_capacity()'s leverage-cap term exactly; if that function's formula
ever changes, this one must be updated by hand, on purpose, as a conscious
decision — not silently via a shared import.

## Why no buffer_pct

CLAUDE.md's standing guardrail: "Never derive Robinhood's buffer % from a
formula — use only the displayed value." That rule governs LIVE decisions,
where a real Robinhood screen exists to read. In a hypothetical simulation
of historical prices there is no broker screen to read at all, so the rule
literally cannot be followed or violated here — there is nothing to defer
to. Rather than inventing an unvalidated buffer%-lookalike formula and
risking it being mistaken for the real thing in a future report, this
module computes a distinctly-named, honestly-scoped proxy instead:
`time_near_leverage_cap_pct_proxy` (see `time_near_leverage_cap()`) —
distance to the LEVERAGE CAP, which is the one hard structural constraint
this module can compute exactly. It is never called "buffer_pct" or
compared numerically against a real synced buffer_pct value anywhere in
this module.

## Required output language

Every result carries `HYPOTHETICAL_LABEL`. `render_metrics()` refuses to
render (raises ValueError) if the assembled text contains any of
`BANNED_PHRASES` — see docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md §3.

## Reuse

TWR and MaxDD reuse backtest_regime.py's existing, already-tested
`twr_annualized()`/`max_drawdown()` rather than re-deriving them — same
dedup discipline as every other backtest module in this repo
(backtest_t1t2_trim.py, backtest_trims.py, etc. already import shared
primitives from backtest_regime.py this same way).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from typing import Callable

from backtest_regime import max_drawdown, twr_annualized

HYPOTHETICAL_LABEL = "hypothetical, simulated"

BANNED_PHRASES = (
    "margin would have made",
    "leverage would have made",
    "margin made",
    "leverage made",
    "margin increased returns by",
    "leverage increased returns by",
)

REQUIRED_FRAMING_TEMPLATE = (
    "Under these assumptions, a simulated investor following this policy "
    "through {window} historical prices would have experienced {outcome}."
)


# ── portfolio state (value object) ──────────────────────────────────────────

@dataclass(frozen=True)
class PortfolioState:
    """Point-in-time snapshot of the simulated portfolio. A value object,
    not the mutable simulation ledger — `simulate()` below owns the
    mutable cash/shares/margin_debt bookkeeping and constructs one of
    these each day for repayment-model functions and metrics to consume.

    Fields match docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md's required
    "Portfolio state" concept list exactly: gross exposure, net equity,
    margin debt, leverage ratio, cash, positions.
    """
    day_index: int
    cash: float
    positions: dict[str, float]      # ticker -> shares held
    margin_debt: float
    gross: float                     # market value of held positions only (cash excluded — matches doctrine's "gross holdings.yaml total")

    @property
    def net_equity(self) -> float:
        return self.gross - self.margin_debt

    @property
    def leverage_ratio(self) -> float | None:
        ne = self.net_equity
        return (self.gross / ne) if ne > 0 else None

    @property
    def book(self) -> float:
        """net_equity + cash — matches allocate.py's plan() 'book = net
        equity (+ new deposit)' doctrine term exactly; this is the value
        TWR/CAGR/MaxDD are computed against."""
        return self.net_equity + self.cash


# ── leverage-cap math (isolated re-derivation, see module docstring) ───────

def _leverage_capped_margin(gross: float, margin_debt: float, cash: float,
                            leverage_cap: float, requested: float) -> float:
    """Same leverage-cap clipping term as allocate.py's margin_capacity(),
    deliberately re-derived rather than imported (module isolation)."""
    net_equity = gross - margin_debt
    max_by_leverage = max(0.0, leverage_cap * (net_equity + cash) - gross - cash)
    return min(requested, max_by_leverage)


# ── repayment models (pure functions) ───────────────────────────────────────
# Every model has signature (state, prior_gross) -> dollars to repay today.
# Model-specific thresholds are bound via functools.partial at scenario-
# construction time — no numeric default is baked into any model function
# itself, per the standing "never guess a parameter without evidence" rule;
# every threshold must be supplied explicitly by the caller.

def repayment_model_0(state: PortfolioState, prior_gross: float | None) -> float:
    """Model 0 — no active repayment policy (the control). Debt only ever
    changes via new margin draws funding buys; this function never
    proactively repays anything, and performs no breach check at all —
    distinct from Model A below, which checks for a breach but otherwise
    also does nothing."""
    return 0.0


def repayment_model_a(state: PortfolioState, prior_gross: float | None, *,
                      leverage_cap: float) -> float:
    """Model A — permanent leverage: repay only the minimum required to
    clear a hard leverage-cap breach, nothing proactive otherwise."""
    if state.margin_debt <= 0:
        return 0.0
    lr = state.leverage_ratio
    if lr is None or lr <= leverage_cap:
        return 0.0
    target_debt = state.gross - state.gross / leverage_cap
    return max(0.0, state.margin_debt - target_debt)


REPAYMENT_MODEL_NAMES = ("MODEL_0", "MODEL_A", "MODEL_B", "MODEL_C")


# ── stateful repayment/reset policies (Phase 3D) ────────────────────────────
#
# Model B and Model C, per docs/PHASE3_SCENARIO_MANIFEST.md's finalized
# mechanics, both require cross-day memory (a running net-equity high-water
# mark; for Model C, also a reset_active flag and the pre-drawdown HWM the
# account must exceed to restore normal capacity). The old Phase 3B
# `repayment_model_b()`/`repayment_model_c()` (target-leverage-threshold and
# single-day-gain-trigger mechanics respectively) are REMOVED — the manifest
# explicitly supersedes both, and leaving two different "Model B/C"
# implementations in this module would be a real footgun for a future run.
# `repayment_model_0` and `repayment_model_a` above are unchanged.
#
# "Equity" high-water mark is tracked on NET_EQUITY (gross - margin_debt),
# NOT `book` (net_equity + cash), correcting a conflation the manifest's own
# formula (§2) had: tracking on `book` would count an un-invested cash
# deposit as an instant "gain," so Model B could repay debt against money
# that was never a market gain at all. net_equity is deposit-neutral by
# construction (cash only enters net_equity once it's converted into gross
# exposure via a buy).
#
# Both policies are evaluated once per day, at the TOP of simulate()'s loop,
# using that day's OPENING mark-to-market state — yesterday's shares priced
# at today's close, before today's interest accrual, deposit, or allocation.
# This is deliberate: evaluating after the deposit-allocation step (as the
# old post-allocation repayment_fn slot does, still used by Model 0/A)
# would let Model C's reset trigger lever up to the scenario's normal cap
# on the very day a reset fires, then immediately force-sell the excess
# back down again — same-day churn with no purpose. Evaluating at the top
# lets Model C declare `effective_leverage_cap` BEFORE that day's buying
# happens, so a reset constrains the day's own allocation instead of
# reacting to it after the fact.
#
# A fresh instance of either policy must be constructed for every
# simulate() run — reusing one instance across two separate runs would leak
# state (a stale HWM, a stuck reset_active flag) between them. See
# test_margin_simulation.py's leak tests.

@dataclass
class RepaymentDecision:
    """Return type for the pre-trade hook (`ScenarioConfig.pre_trade_fn`).
    `repay_amount` is always >= 0 — no policy in this module can ever
    return a negative value here, and simulate() additionally clamps
    anything a future policy might try (constraint #3: no model may
    recommend increasing leverage — a negative repay would be an implicit
    borrow). `effective_leverage_cap`, if not None, is the leverage cap
    simulate() uses for THIS DAY's deposit-driven allocation only, in
    place of the scenario's normal `leverage_cap` — simulate() further
    clamps this to `min(effective_leverage_cap, scenario.leverage_cap)`,
    so no policy can ever raise capacity above the scenario's own hard
    cap, only tighten it."""
    repay_amount: float = 0.0
    effective_leverage_cap: float | None = None


class ModelBProfitHarvest:
    """Model B — Profit Harvest, finalized mechanics
    (docs/PHASE3_SCENARIO_MANIFEST.md §1/§2, initial repay_fraction=0.25,
    sweepable {0.10, 0.25, 0.50} in a future run — not swept here).

    Trigger: today's net_equity sets a new high-water mark versus every
    prior day this instance has seen. On a new-high day, repay
    `repay_fraction` of the fresh gain (today's net_equity minus the
    prior HWM) toward margin debt. Never repays more than current
    margin_debt, and never returns a negative amount (never an implicit
    borrow) — "no additional borrowing" is satisfied structurally: this
    policy's `effective_leverage_cap` is always None (it never tightens
    OR loosens the scenario's normal cap), and `repay_amount` is always
    >= 0, so it can only ever reduce debt, never increase capacity.
    """

    def __init__(self, repay_fraction: float = 0.25):
        if not (0.0 <= repay_fraction <= 1.0):
            raise ValueError(f"repay_fraction must be in [0, 1], got {repay_fraction}")
        self.repay_fraction = repay_fraction
        self._hwm: float | None = None

    def __call__(self, state: PortfolioState, prior_gross: float | None) -> RepaymentDecision:
        ne = state.net_equity
        if self._hwm is None:
            self._hwm = ne
            return RepaymentDecision()
        if ne > self._hwm:
            gain = ne - self._hwm
            self._hwm = ne
            repay = max(0.0, min(state.margin_debt, self.repay_fraction * gain))
            return RepaymentDecision(repay_amount=repay)
        return RepaymentDecision()


class ModelCRiskReset:
    """Model C — Risk Reset, finalized mechanics
    (docs/PHASE3_SCENARIO_MANIFEST.md §1/§2, initial parameters:
    drawdown_trigger_pct=15.0, reset_leverage=1.25).

    Trigger: net_equity drawdown from this instance's own running
    high-water mark exceeds `drawdown_trigger_pct`. On first crossing
    (fires ONCE per drawdown episode, not every day the account remains
    below threshold — docs/PHASE3_SCENARIO_MANIFEST.md §3 assumption #4),
    immediately deleverages to `reset_leverage` (repays the minimum
    needed so gross/net_equity == reset_leverage) and enters a reset
    state that tightens `effective_leverage_cap` to `reset_leverage` for
    every subsequent day until BOTH restoration conditions hold: (a) a
    NEW all-time high (net_equity exceeds the PRE-drawdown HWM, not
    merely recovers to it) and (b) leverage has been at or below
    `reset_leverage` continuously since the reset (checked each day the
    reset is active, not just at restoration time — the same clamp that
    tightens the cap while active also keeps this condition satisfied
    unless a future policy change reintroduces opportunistic drawing).

    No dip-buying interpretation: `effective_leverage_cap` while active
    is always `reset_leverage` (never higher) or, once restored, None
    (defers to the scenario's own cap) — this policy never returns a cap
    HIGHER than `reset_leverage` while `reset_active` is True, so the
    drawdown trigger can only ever tighten deployable capacity, never
    loosen it as a reaction to the dip itself. Restoration is gated on a
    NEW high, not on the dip ending — a partial recovery back toward the
    old peak is not, by construction, treated as a buy signal.
    """

    def __init__(self, drawdown_trigger_pct: float = 15.0, reset_leverage: float = 1.25,
                epsilon: float = 1e-9):
        if not (0.0 < drawdown_trigger_pct < 100.0):
            raise ValueError(f"drawdown_trigger_pct must be in (0, 100), got {drawdown_trigger_pct}")
        if reset_leverage < 1.0:
            raise ValueError(f"reset_leverage must be >= 1.0, got {reset_leverage}")
        self.drawdown_trigger_pct = drawdown_trigger_pct
        self.reset_leverage = reset_leverage
        self.epsilon = epsilon
        self._hwm: float | None = None
        self.reset_active = False
        self._pre_drawdown_hwm: float | None = None

    def __call__(self, state: PortfolioState, prior_gross: float | None) -> RepaymentDecision:
        ne = state.net_equity
        self._hwm = ne if self._hwm is None else max(self._hwm, ne)

        repay_amount = 0.0

        if not self.reset_active and self._hwm > 0:
            drawdown_pct = (self._hwm - ne) / self._hwm * 100.0
            if drawdown_pct > self.drawdown_trigger_pct:
                self._pre_drawdown_hwm = self._hwm
                self.reset_active = True
                lr = state.leverage_ratio
                if lr is not None and lr > self.reset_leverage and state.gross > 0:
                    # NOT `gross - gross/reset_leverage` (that assumes gross
                    # stays fixed while only debt drops, true only if the
                    # repayment is funded entirely from idle cash). This
                    # harness's actual funding mechanism (_fund_repayment)
                    # sells assets when cash is insufficient -- a $1 trim
                    # reduces gross by $1 AND debt by $1 together, leaving
                    # net_equity (gross - debt) unchanged by the trim
                    # itself. Under that funding path, leverage after
                    # repaying R is (gross-R)/net_equity (net_equity is
                    # invariant to a trim-funded paydown), so hitting the
                    # target requires R = gross - reset_leverage*net_equity,
                    # not the fixed-gross formula. If cash happens to cover
                    # some or all of R, net_equity rises instead (debt drops
                    # with no offsetting gross drop) and the realized
                    # leverage ends up BELOW reset_leverage, never above it
                    # — this formula is exact for pure-trim funding and
                    # conservative (over-deleverages, never under-) whenever
                    # cash is available too. See test_model_c_reset_hits_
                    # exact_target_leverage_when_trim_funded.
                    repay_amount = max(0.0, state.gross - self.reset_leverage * state.net_equity)

        if self.reset_active:
            new_all_time_high = (self._pre_drawdown_hwm is not None
                                 and ne > self._pre_drawdown_hwm)
            lr = state.leverage_ratio
            leverage_normalized = lr is None or lr <= self.reset_leverage + self.epsilon
            if new_all_time_high and leverage_normalized:
                self.reset_active = False
                self._pre_drawdown_hwm = None
                return RepaymentDecision(repay_amount=repay_amount, effective_leverage_cap=None)
            return RepaymentDecision(repay_amount=repay_amount,
                                     effective_leverage_cap=self.reset_leverage)
        return RepaymentDecision(repay_amount=repay_amount, effective_leverage_cap=None)


# ── scenario configuration ──────────────────────────────────────────────────

@dataclass
class ScenarioConfig:
    name: str
    leverage_cap: float                  # 1.0 == unlevered (Scenario A)
    interest_apr: float
    interest_free_amount: float
    repayment_fn: Callable[[PortfolioState, float | None], float] = repayment_model_0
    repayment_model_name: str = "MODEL_0"
    pre_trade_fn: Callable[[PortfolioState, float | None], RepaymentDecision] | None = None


def scenario_unlevered(name: str = "A") -> ScenarioConfig:
    """Scenario A — unlevered baseline."""
    return ScenarioConfig(name=f"{name} — unlevered baseline", leverage_cap=1.0,
                          interest_apr=0.0, interest_free_amount=0.0,
                          repayment_fn=repayment_model_0,
                          repayment_model_name="MODEL_0")


def scenario_fixed_leverage(leverage_cap: float, interest_apr: float,
                            interest_free_amount: float, name: str = "B") -> ScenarioConfig:
    """Scenario B — current (or any single) fixed leverage cap, no
    proactive repayment (Model 0 — matches production's actual current
    behavior, which never proactively pays down margin)."""
    return ScenarioConfig(
        name=f"{name} — leverage {leverage_cap:.2f}x, no repayment",
        leverage_cap=leverage_cap, interest_apr=interest_apr,
        interest_free_amount=interest_free_amount,
        repayment_fn=repayment_model_0, repayment_model_name="MODEL_0")


def scenario_leverage_sweep(levels: list[float], interest_apr: float,
                            interest_free_amount: float) -> list[ScenarioConfig]:
    """Scenario C — leverage sweep. One ScenarioConfig per level, all on
    Model 0 (no repayment) so only the leverage cap itself varies."""
    return [scenario_fixed_leverage(lv, interest_apr, interest_free_amount,
                                    name=f"C-{lv:.2f}x")
            for lv in levels]


def scenario_repayment_variants(leverage_cap: float, interest_apr: float,
                                interest_free_amount: float,
                                model_a_cfg: dict | None = None,
                                model_b_cfg: dict | None = None,
                                model_c_cfg: dict | None = None) -> list[ScenarioConfig]:
    """Scenario D — repayment policy comparison, all four models at the
    same fixed leverage_cap so only repayment behavior varies. Each
    model's config dict is REQUIRED (no defaults) if that model is to be
    included — pass None to skip a model. Model B/C's config dicts are
    passed as constructor kwargs to the stateful `ModelBProfitHarvest`/
    `ModelCRiskReset` policies (e.g. `model_b_cfg={"repay_fraction": 0.25}`,
    `model_c_cfg={"drawdown_trigger_pct": 15.0, "reset_leverage": 1.25}`) —
    NOT bound via functools.partial onto a stateless function, since both
    now require a fresh, per-run stateful instance (see the module-level
    comment above ModelBProfitHarvest)."""
    out = [ScenarioConfig(
        name="D-0 — no active repayment policy (control)",
        leverage_cap=leverage_cap, interest_apr=interest_apr,
        interest_free_amount=interest_free_amount,
        repayment_fn=repayment_model_0, repayment_model_name="MODEL_0")]
    if model_a_cfg is not None:
        out.append(ScenarioConfig(
            name="D-A — permanent leverage (forced-breach repay only)",
            leverage_cap=leverage_cap, interest_apr=interest_apr,
            interest_free_amount=interest_free_amount,
            repayment_fn=partial(repayment_model_a, leverage_cap=leverage_cap),
            repayment_model_name="MODEL_A"))
    if model_b_cfg is not None:
        out.append(ScenarioConfig(
            name="D-B — profit harvest", leverage_cap=leverage_cap,
            interest_apr=interest_apr, interest_free_amount=interest_free_amount,
            repayment_fn=repayment_model_0,
            pre_trade_fn=ModelBProfitHarvest(**model_b_cfg),
            repayment_model_name="MODEL_B"))
    if model_c_cfg is not None:
        out.append(ScenarioConfig(
            name="D-C — risk reset", leverage_cap=leverage_cap,
            interest_apr=interest_apr, interest_free_amount=interest_free_amount,
            repayment_fn=repayment_model_0,
            pre_trade_fn=ModelCRiskReset(**model_c_cfg),
            repayment_model_name="MODEL_C"))
    return out


# ── metrics (pure functions) ────────────────────────────────────────────────

def cagr(start_value: float, end_value: float, years: float) -> float:
    if start_value <= 0 or years <= 0:
        return 0.0
    return ((end_value / start_value) ** (1.0 / years) - 1.0) * 100.0


def annualized_volatility(daily_values: list[float], flows: dict[int, float]) -> float:
    rets = []
    for i in range(1, len(daily_values)):
        prev = daily_values[i - 1]
        if prev <= 0:
            continue
        f = flows.get(i, 0.0)
        rets.append((daily_values[i] - f) / prev - 1.0)
    if len(rets) < 2:
        return 0.0
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    return (var ** 0.5) * (252.0 ** 0.5) * 100.0


def time_near_leverage_cap(leverage_series: list[float | None], leverage_cap: float,
                           near_cap_fraction: float = 0.9) -> float:
    """Proxy for 'time near buffer floor' (see module docstring for why a
    real buffer%-based metric is not computed here). Returns the percent
    of valid days where leverage_ratio exceeded `near_cap_fraction` of the
    leverage cap — the honest, computable analog to "how much of the time
    was this policy running close to its hard structural limit."""
    valid = [lv for lv in leverage_series if lv is not None]
    if not valid:
        return 0.0
    near = sum(1 for lv in valid if lv > near_cap_fraction * leverage_cap)
    return near / len(valid) * 100.0


def worst_case_concentration_impact(position_weight_pct: float,
                                    position_max_drawdown_pct: float,
                                    leverage_ratio: float | None) -> float:
    """Same decomposition method docs/PHASE2_IMPLEMENTATION_PLAN.md's
    t1t2_trim_backtest.md precedent used for NVDA: one position's own
    worst historical drawdown, amplified by the account's leverage ratio,
    expressed as an impact on NET EQUITY — not portfolio-level MaxDD,
    which smooths a single concentrated name's real worst case away (the
    exact failure mode that precedent was built to correct for).

    position_weight_pct: that position's weight as % of GROSS (not book).
    position_max_drawdown_pct: that position's own historical peak-to-
        trough decline, as a negative or positive percentage (sign
        ignored — magnitude only).
    leverage_ratio: current gross/net_equity; None or <=0 treated as 1.0
        (unlevered) rather than raising, since 'no leverage' is a valid,
        common state to evaluate this metric at.
    """
    lr = leverage_ratio if (leverage_ratio and leverage_ratio > 0) else 1.0
    position_impact_on_gross = position_weight_pct / 100.0 * abs(position_max_drawdown_pct) / 100.0
    return position_impact_on_gross * lr * 100.0


# ── simulation engine ────────────────────────────────────────────────────────

@dataclass
class SimulationResult:
    label: str
    scenario_name: str
    repayment_model_name: str
    leverage_cap: float
    book_values: list[float]
    gross_series: list[float]
    leverage_series: list[float | None]
    flows: dict[int, float]
    events: list[dict]
    final_margin_debt: float
    deposit_total: float
    tracked_values: dict[str, list[float]] = field(default_factory=dict)

    def metrics(self, near_cap_fraction: float = 0.9,
               concentration_inputs: dict | None = None) -> dict:
        years = len(self.book_values) / 252.0
        start = self.book_values[0] if self.book_values else 0.0
        end = self.book_values[-1] if self.book_values else 0.0
        m = {
            "label": self.label,
            "scenario": self.scenario_name,
            "repayment_model": self.repayment_model_name,
            "ann_twr_pct": twr_annualized(self.book_values, self.flows),
            "cagr_pct": cagr(start, end, years),
            "max_drawdown_pct": max_drawdown(self.book_values),
            "annualized_volatility_pct": annualized_volatility(self.book_values, self.flows),
            "time_near_leverage_cap_pct_proxy": time_near_leverage_cap(
                self.leverage_series, self.leverage_cap, near_cap_fraction),
            "final_book_value": end,
            "final_margin_debt": self.final_margin_debt,
            "deposit_total": self.deposit_total,
        }
        if concentration_inputs:
            m["worst_case_concentration_impact_pct"] = worst_case_concentration_impact(
                **concentration_inputs)
        return m


def _fund_repayment(cash: float, shares: dict[str, float], closes: dict[str, float],
                    gross: float, repay: float) -> float:
    """Fund `repay` dollars toward a margin paydown: idle cash first, then
    a pro-rata trim across all priced positions. Mutates `shares` in
    place (reassigns share counts down). Returns the updated cash value.
    Shared by both the pre-trade hook (Model B/C) and the post-allocation
    repayment_fn slot (Model 0/A) — a single funding mechanism, not two
    slightly-different ones."""
    from_cash = min(cash, repay)
    cash -= from_cash
    still_needed = repay - from_cash
    if still_needed > 0 and gross > 0:
        # proceeds go straight to the paydown, never touch idle cash — a
        # disclosed simplification, not a strategic decision.
        frac = min(1.0, still_needed / gross)
        for s in list(shares):
            px = closes.get(s)
            if px is None or shares[s] <= 0:
                continue
            sell_val = shares[s] * px * frac
            shares[s] -= sell_val / px
    return cash


def simulate(scenario: ScenarioConfig, weights: dict[str, float],
            aligned: dict[str, tuple[list[float | None], int | None]],
            calendar: list[str], deposit_days: list[str],
            deposit_amount: float | None = 0.0, min_lot: float = 25.0,
            deposit_schedule: dict[str, float] | None = None,
            track_tickers: list[str] | None = None) -> SimulationResult:
    """Run one scenario through aligned historical (or synthetic, for
    tests) daily closes.

    `aligned`: {ticker: (closes_list_aligned_to_calendar, first_eligible_
    index_or_None)} — same shape backtest_regime.py's setup() already
    produces, so a real run can reuse that function directly (see
    `load_real_aligned_data()` below); tests construct this dict by hand
    with small synthetic series.

    Deposits are allocated by weighted dollar-gap, same greedy pattern as
    backtest_regime.simulate() and allocate.py's plan() — largest gap
    first, funded by cash then margin up to that day's EFFECTIVE leverage
    cap. Repayment is funded first from any uninvested cash, then via a
    pro-rata trim across all held positions if cash alone is insufficient
    (`_fund_repayment()`) — a disclosed simplification, not itself a
    strategic decision this harness makes.

    Two independent repayment/reset mechanisms can be attached to a
    scenario, evaluated at different points in the day (see the
    module-level comment above ModelBProfitHarvest for the full
    rationale):
      - `scenario.repayment_fn` — the original Phase 3B slot, evaluated
        AFTER deposit-allocation. Model 0/A use this; both are stateless.
      - `scenario.pre_trade_fn` — the Phase 3D addition, evaluated at the
        TOP of the day (before interest/deposit/allocation), on OPENING
        mark-to-market state. Returns a `RepaymentDecision` that can both
        repay debt immediately AND declare an `effective_leverage_cap`
        that constrains THIS DAY's deposit-driven allocation. Model B/C
        use this — both are stateful (see ModelBProfitHarvest/
        ModelCRiskReset), so a fresh instance is required per simulate()
        run. Whatever `effective_leverage_cap` a policy requests, this
        function clamps it to `min(requested, scenario.leverage_cap)` —
        a structural guarantee that no policy can ever raise capacity
        above the scenario's own hard cap, only tighten it.

    `deposit_amount` is the flat amount used on every day in
    `deposit_days` unless `deposit_schedule` (a {date_str: amount} map)
    supplies a specific override for that day — real deposit history is
    irregular (per docs/MARGIN_DATA_INVENTORY.md's Category C), so a
    future Phase 3C run may want a non-flat cadence.

    `track_tickers` (Phase 4A addition): optional list of tickers whose
    daily dollar value (shares held x that day's close) is recorded into
    the returned SimulationResult.tracked_values. Added because no
    existing output exposes PER-TICKER value over time — only aggregate
    gross/book/leverage series — and concentration measurement
    (docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md) genuinely
    cannot be derived externally without it (unlike everything else
    Phase 4A needed, which is computable from already-exposed series —
    see phase4a_lib.py). Defaults to None: when omitted, tracked_values
    is an empty dict and every other code path is byte-for-byte
    unchanged — this is a pure addition, not a behavior change, to the
    existing 156-test-covered engine (see
    test_regression_scenario_*_unchanged in test_margin_simulation.py
    for the pre-existing regression-proof pattern this follows).
    """
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    margin_debt = 0.0
    book_values: list[float] = []
    gross_series: list[float] = []
    leverage_series: list[float | None] = []
    flows: dict[int, float] = {}
    events: list[dict] = []
    prior_gross: float | None = None
    tracked_values: dict[str, list[float]] = {t: [] for t in (track_tickers or [])}

    for i, d in enumerate(calendar):
        elig = [s for s in aligned if aligned[s][1] is not None and i >= aligned[s][1]]
        closes = {s: aligned[s][0][i] for s in elig
                 if aligned[s][0][i] is not None}
        gross = sum(shares.get(s, 0.0) * px for s, px in closes.items())

        # ---- pre-trade hook (Model B/C only; None for Model 0/A) -----------
        # Evaluated on TODAY's OPENING mark-to-market state -- yesterday's
        # shares priced at today's close, before interest/deposit/trade --
        # see the module-level comment above ModelBProfitHarvest for why.
        effective_leverage_cap_today = scenario.leverage_cap
        if scenario.pre_trade_fn is not None:
            state_pre = PortfolioState(day_index=i, cash=cash, positions=dict(shares),
                                       margin_debt=margin_debt, gross=gross)
            decision = scenario.pre_trade_fn(state_pre, prior_gross)
            pre_repay = max(0.0, min(decision.repay_amount, margin_debt))
            if pre_repay > 0:
                cash = _fund_repayment(cash, shares, closes, gross, pre_repay)
                margin_debt -= pre_repay
                gross = sum(shares.get(s, 0.0) * closes.get(s, 0.0) for s in shares)
                events.append({"day": i, "kind": "repayment", "amount": pre_repay,
                              "source": "pre_trade"})
            if decision.effective_leverage_cap is not None:
                # constraint #3 (no model may recommend increasing leverage),
                # enforced structurally here, not merely trusted per-policy:
                # a pre-trade hook can only ever TIGHTEN today's cap, never
                # loosen it past the scenario's own.
                effective_leverage_cap_today = min(decision.effective_leverage_cap,
                                                   scenario.leverage_cap)

        # ---- daily interest accrual, capitalized into margin_debt --------
        if margin_debt > 0 and scenario.interest_apr > 0:
            taxable_debt = max(0.0, margin_debt - scenario.interest_free_amount)
            interest = taxable_debt * (scenario.interest_apr / 365.0)
            if interest > 0:
                margin_debt += interest
                events.append({"day": i, "kind": "interest_accrual", "amount": interest})

        # ---- deposit + weighted-gap allocation ----------------------------
        todays_deposit = (deposit_schedule or {}).get(d, deposit_amount or 0.0)
        if d in dep_set and todays_deposit > 0:
            cash += todays_deposit
            flows[i] = todays_deposit
            events.append({"day": i, "kind": "deposit", "amount": todays_deposit})

            net_equity = gross - margin_debt
            margin_allowed = _leverage_capped_margin(
                gross, margin_debt, cash, effective_leverage_cap_today, requested=float("inf"))
            buying_power = cash + margin_allowed
            book = net_equity + cash
            w_sum = sum(weights.get(s, 0.0) for s in elig if s in closes)
            if w_sum > 0 and buying_power >= min_lot:
                targets = {s: book * weights.get(s, 0.0) / w_sum
                          for s in elig if s in closes}
                gaps = sorted(
                    ((targets[s] - shares.get(s, 0.0) * closes[s], s) for s in targets),
                    reverse=True)
                remaining = buying_power
                for gap, s in gaps:
                    if gap < min_lot or remaining < min_lot:
                        continue
                    spend = min(gap, remaining)
                    shares[s] = shares.get(s, 0.0) + spend / closes[s]
                    remaining -= spend
                spent = buying_power - remaining
                from_cash = min(cash, spent)
                from_margin = max(0.0, spent - from_cash)
                cash -= from_cash
                if from_margin > 0:
                    margin_debt += from_margin
                    events.append({"day": i, "kind": "margin_draw", "amount": from_margin})

        # ---- repayment policy ----------------------------------------------
        gross = sum(shares.get(s, 0.0) * closes.get(s, 0.0) for s in shares)
        state = PortfolioState(day_index=i, cash=cash, positions=dict(shares),
                               margin_debt=margin_debt, gross=gross)
        repay = scenario.repayment_fn(state, prior_gross)
        repay = max(0.0, min(repay, margin_debt))
        if repay > 0:
            cash = _fund_repayment(cash, shares, closes, gross, repay)
            margin_debt -= repay
            events.append({"day": i, "kind": "repayment", "amount": repay,
                          "source": "post_allocation"})

        # ---- mark to market --------------------------------------------------
        gross = sum(shares.get(s, 0.0) * closes.get(s, 0.0) for s in shares)
        net_equity = gross - margin_debt
        book_values.append(net_equity + cash)
        gross_series.append(gross)
        leverage_series.append((gross / net_equity) if net_equity > 0 else None)
        for t in tracked_values:
            tracked_values[t].append(shares.get(t, 0.0) * closes.get(t, 0.0))
        prior_gross = gross

    return SimulationResult(
        label=HYPOTHETICAL_LABEL,
        scenario_name=scenario.name,
        repayment_model_name=scenario.repayment_model_name,
        leverage_cap=scenario.leverage_cap,
        book_values=book_values,
        gross_series=gross_series,
        leverage_series=leverage_series,
        flows=flows,
        events=events,
        final_margin_debt=margin_debt,
        deposit_total=sum(flows.values()),
        tracked_values=tracked_values,
    )


# ── real-data loading (Phase 3C will use this; not exercised by Phase 3B) ──

def load_real_aligned_data():
    """Thin wrapper around backtest_regime.py's existing setup() so a
    future Phase 3C run reuses the identical universe/alignment/deposit-
    calendar logic every other backtest in this repo already uses, rather
    than re-deriving it. NOT called by this module's own tests (Phase 3B
    scope is harness + unit tests on synthetic data only, per
    "do not begin interpreting results yet") — provided here so Phase 3C
    doesn't have to duplicate this wiring."""
    import backtest_regime as br
    tiers, aligned, regime_closes, calendar, deposit_days = br.setup()
    weights = {t: br.TIER_WEIGHTS[tiers[t]] for t in tiers}
    aligned_2 = {s: (closes, first_elig) for s, (closes, rsi, first_elig) in aligned.items()}
    return weights, aligned_2, calendar, deposit_days


# ── output-language enforcement ─────────────────────────────────────────────

def _assert_no_banned_language(text: str) -> None:
    lowered = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            raise ValueError(
                f"Output contains banned phrase {phrase!r} — required framing is "
                "\"Under these assumptions, a simulated investor following this "
                "policy through <window> historical prices would have experienced "
                "<outcome>.\" (docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md §3)")


def render_metrics(metrics: dict, assumptions: dict) -> str:
    """Render one scenario's metrics as text, enforcing the required
    hypothetical-labeling and banned-language rules before returning.
    Raises ValueError rather than silently stripping banned language —
    a caller that trips this should fix the input, not have it masked."""
    lines = [
        f"**⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's real "
        "history — see docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md §3/§5.",
        "",
        "Assumptions: " + "; ".join(f"{k}={v}" for k, v in assumptions.items()),
        "",
    ]
    for k, v in metrics.items():
        lines.append(f"- {k}: {v}")
    text = "\n".join(lines)
    _assert_no_banned_language(text)
    return text
