"""
repayment_lib.py — MARGIN-0005 research-only repayment-policy library (G2B).

Authorized by `governance/decisions/MARGIN-0005-margin-target-research-charter.md`
(charter §4, "Research package" row) as part of the S2 allowance of <=3 narrow
engine/lib/test PRs (protocol `research/margin_target_study/PROTOCOL_V2.md`
§19, stage S2 -> gate G2). This is the second such PR (G2A, the engine
extensions in `margin_simulation.py`, is already merged).

## Scope

Implements the frozen repayment families R1-R9 and the Model B reference path
(R-B) from PROTOCOL_V2.md §5.A.8 / `pre_registration.yaml`
`studies.study_a.repayment_policies`, as PURE, DETERMINISTIC functions (or,
where the protocol itself requires cross-day memory — R6's weekly staging,
R-B's high-water mark — small stateful classes with the same `__call__(state,
...)` shape the engine's own `ModelBProfitHarvest`/`ModelCRiskReset` already
use). Nothing here is wired into `margin_simulation.simulate()` — that
wiring, and any actual Study A run, is out of scope for this PR (future S3
work, `run_study_a.py`, not authorized here). This module is a decision
layer only: given an already-computed `PortfolioState` (and, for the few
families that need it, an already-computed external signal — a dividend
credit amount, a trim-proceeds amount, a trend/vol flag, an Intelligence
flag decision), it returns a `RepaymentDecision` expressing what that one
family would do. Computing those external signals (SMA/vol from price
series, dividend calendars, Intelligence flag adjudication) is explicitly
NOT this module's job — that belongs to `overlay_lib.py` / `dividend_ledger.py`
/ future Intelligence-side tooling, keeping this library narrowly scoped to
"given the state and the signal, what does this repayment family do to debt
and leverage capacity."

## Isolation (charter §4 / protocol §13)

Zero import relationship with `allocate.py` or `margin_state.py` in either
direction. No filesystem or network I/O. No import of broker clients,
account-state loaders, Intelligence records, or registered-trial runners.
Nothing in production imports this module. Importing this module has no
side effects and creates no artifact (no `trial_ledger.jsonl`, no
`candidate_freeze.yaml`) — it is pure code, exactly like
`margin_simulation.py` itself.

The only import from `margin_simulation.py` is the small set of
research-facing types/constants the charter names as reusable:
`PortfolioState`, `RepaymentDecision`, `ModelBProfitHarvest`, and the
governed `LEVERAGE_TARGET_HARD_MIN`/`LEVERAGE_TARGET_HARD_MAX` constants
(1.0 / 1.8 — reused, not redefined).

## Never borrows: a deliberate design choice on which `RepaymentDecision`
## field each family uses

`RepaymentDecision.leverage_target` (the G2A generalized hook) is
deliberately NEVER set by anything in this module. In `simulate()`, setting
`leverage_target` does two things: it repays down toward the target when
opening leverage is above it, AND it can command a fresh margin DRAW
(through the same weighted-gap allocator) when opening leverage is below
the target by more than the dead band (see the "leverage-target draw
toward target" block in `margin_simulation.simulate()`). That second half
is exactly what requirement (7) — "no repayment family may independently
authorize borrowing or increase leverage" — forbids. Every family below
therefore expresses itself using only two fields that cannot do that:
`repay_amount` (always >= 0; can only ever reduce debt) and
`effective_leverage_cap` (a same-day CEILING on deposit-driven buying
power; on a non-deposit day it is inert, and on a deposit day it can only
ever tighten capacity, never trigger a draw by itself — a draw still
requires an actual deposit and the normal weighted-gap allocator). This is
why R1/R8/R9/R5/R7's account-level-advisory semantic compute an explicit
dollars-to-repay amount themselves (`_plan_repay_to_target`) rather than
handing a bare target to the engine's own draw-capable hook.

## Numeric parameters

Every numeric parameter a family needs is either (a) reused directly from
`margin_simulation.py`'s own governed constants (1.0 / 1.8), (b) a value
the frozen `pre_registration.yaml` states explicitly (R4's {6%, 8%} hurdle
values, R6's `band_above_floor_pp: 10` / `staged_fraction_per_week: 0.25`,
R-B's `repay_fraction: 0.10`), or (c) a value with NO fixed level in the
frozen documents at all (R6's maintenance-excess-proxy `floor` itself —
`assumptions_ledger.yaml` A-03/A-23 record it as explicitly UNSET at G2A,
"any floor value used later must be fixed and NUM-0001-classified before
any Study A/B/C run"). Category (c) parameters are REQUIRED, no-default
keyword arguments here — this library never invents a number for them; it
is the caller's job, at actual study-run time, to supply a
NUM-0001-classified value. No parameter in this module has a silently
baked-in default beyond what `margin_simulation.py` itself already
defaults (e.g. `RepaymentDecision.dead_band`'s own default of 0.0).

## Categorical separation (protocol §5.A.8, binding on all reporting)

R1-R3 (cash-flow-priority), R4 (cost-triggered), R5-R6 (state-triggered),
R7 (advisory), R8-R9 (posture-defining), and R-B (profit-path) are
different kinds of rules and are never pooled, averaged, or ranked as one
family here. `REPAYMENT_FAMILY_CATEGORY` below is a plain, read-only
label map for documentation/testing — there is no scoring, ranking, or
aggregation function anywhere in this module, deliberately.

## R7 / Study D advisory boundary

`r7_intelligence_advisory()` takes `flag_active` as an OPAQUE boolean the
caller has already decided (e.g. from a human-authored, source-pinned
`intelligence_flag_events.yaml` entry, per protocol §6 — reading and
adjudicating that ledger is not this module's job). This function computes
no historical Intelligence signal, ranking, opportunity/conviction/regime
score, or per-ticker effect; it only ever tightens capacity or repays
toward an account-level target, at whole-cycle/account granularity, per
the three semantics the charter and protocol permit and no others.

## Hard risk cures / forced liquidation

Owned entirely by the engine (`margin_simulation.py`'s maintenance-excess
proxy and forced-liquidation mechanics) and always execute first, outside
and prior to anything in this module. Nothing here references, calls,
duplicates, or reorders that mechanism.

## Timing convention (G2A, unmodified)

`simulate()`'s documented same-day ordering — dividend/corporate-action
entitlement uses the OPENING holdings snapshot; same-day return-component
cash (dividends, corporate actions) is credited AFTER the pre-trade hook
runs — is unchanged by this PR and is not redesigned here.
`r2_dividends_first()` accordingly takes the day's already-credited
dividend cash amount as an explicit input rather than trying to observe it
through the pre-trade hook's pre-credit state.

All results expressed via this module inherit `margin_simulation.py`'s
`HYPOTHETICAL_LABEL` framing — nothing here is a live recommendation, and
nothing here is wired to run against real account state.
"""

from __future__ import annotations

import math
from enum import Enum
from types import MappingProxyType

from margin_simulation import (
    LEVERAGE_TARGET_HARD_MAX,
    LEVERAGE_TARGET_HARD_MIN,
    ModelBProfitHarvest,
    PortfolioState,
    RepaymentDecision,
)

# Pinned by pre_registration.yaml studies.study_a.repayment_policies.families
# .RB_model_b_profit_harvest_reference.repay_fraction — the ONE registered
# R-B configuration. Deliberately NOT the engine's own Phase-3 default of
# 0.25 (ModelBProfitHarvest.__init__'s default is a different, earlier
# study's value; MARGIN-0005 pins its own reference configuration).
MODEL_B_REFERENCE_REPAY_FRACTION = 0.10


# ── family / category identity (documentation + test scaffolding only —
#    no scoring, ranking, or pooling logic anywhere below) ──────────────────

class RepaymentFamily(str, Enum):
    R1_DEPOSITS_FIRST = "R1"
    R2_DIVIDENDS_FIRST = "R2"
    R3_GOVERNED_TRIMS_FIRST = "R3"
    R4_BORROWING_COST_HURDLE = "R4"
    R5_TREND_VOL_DETERIORATION = "R5"
    R6_MAINTENANCE_DETERIORATION = "R6"
    R7_INTELLIGENCE_ADVISORY = "R7"
    R8_RESTORE_TO_TARGET_ONLY = "R8"
    R9_FULL_REPAYMENT_TO_UNLEVERED = "R9"
    RB_MODEL_B_PROFIT_HARVEST = "R-B"


class RepaymentCategory(str, Enum):
    CASH_FLOW_PRIORITY = "cash_flow_priority"
    COST_TRIGGERED = "cost_triggered"
    STATE_TRIGGERED = "state_triggered"
    ADVISORY = "advisory"
    POSTURE_DEFINING = "posture_defining"
    PROFIT_PATH = "profit_path"


# Read-only: protocol §5.A.8's category labels, exactly. Never mutated,
# never turned into a numeric weight or rank.
REPAYMENT_FAMILY_CATEGORY = MappingProxyType({
    RepaymentFamily.R1_DEPOSITS_FIRST: RepaymentCategory.CASH_FLOW_PRIORITY,
    RepaymentFamily.R2_DIVIDENDS_FIRST: RepaymentCategory.CASH_FLOW_PRIORITY,
    RepaymentFamily.R3_GOVERNED_TRIMS_FIRST: RepaymentCategory.CASH_FLOW_PRIORITY,
    RepaymentFamily.R4_BORROWING_COST_HURDLE: RepaymentCategory.COST_TRIGGERED,
    RepaymentFamily.R5_TREND_VOL_DETERIORATION: RepaymentCategory.STATE_TRIGGERED,
    RepaymentFamily.R6_MAINTENANCE_DETERIORATION: RepaymentCategory.STATE_TRIGGERED,
    RepaymentFamily.R7_INTELLIGENCE_ADVISORY: RepaymentCategory.ADVISORY,
    RepaymentFamily.R8_RESTORE_TO_TARGET_ONLY: RepaymentCategory.POSTURE_DEFINING,
    RepaymentFamily.R9_FULL_REPAYMENT_TO_UNLEVERED: RepaymentCategory.POSTURE_DEFINING,
    RepaymentFamily.RB_MODEL_B_PROFIT_HARVEST: RepaymentCategory.PROFIT_PATH,
})


# ── validation helpers (fail loudly on malformed input, same discipline as
#    margin_simulation._validated_maintenance_requirement) ──────────────────

def _validate_bool(name: str, value) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _validate_finite(name: str, value) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value}")
    return value


def _validate_nonnegative(name: str, value) -> float:
    value = _validate_finite(name, value)
    if value < 0:
        raise ValueError(f"{name} must be >= 0, got {value}")
    return value


def _clamp_leverage(target, scenario_cap=LEVERAGE_TARGET_HARD_MAX) -> float:
    """Every leverage-related value this module emits passes through here:
    clamped to [1.00, min(scenario_cap, 1.80)] — requirement (8), never
    violable by any family regardless of what it is asked to target."""
    target = _validate_finite("target_leverage", target)
    scenario_cap = _validate_finite("scenario_cap", scenario_cap)
    if scenario_cap < LEVERAGE_TARGET_HARD_MIN:
        raise ValueError(
            f"scenario_cap must be >= {LEVERAGE_TARGET_HARD_MIN}, got {scenario_cap}")
    return min(max(target, LEVERAGE_TARGET_HARD_MIN),
               scenario_cap, LEVERAGE_TARGET_HARD_MAX)


def _plan_repay_to_target(state: PortfolioState, target_leverage,
                          *, scenario_cap=LEVERAGE_TARGET_HARD_MAX,
                          dead_band: float = 0.0) -> tuple[float, float]:
    """Shared ceiling-style repay-to-target arithmetic used by every
    posture/state-triggered family below (R1, R5, R7's account-level-
    advisory, R8, R9). Returns `(clamped_target, repay_amount)`.

    Never borrows: `repay_amount` is always >= 0 and this function alone
    decides it — it is never handed to the engine's draw-capable
    `leverage_target` hook (see the module docstring). Never repays below
    the target: below-target leverage (or a debt-free / non-positive-
    equity account) always yields `repay_amount == 0.0`. Uses the same
    trim-funded exact-de-lever identity as `ModelCRiskReset`/the engine's
    own leverage-target block: at leverage L over net_equity NE,
    gross = L * NE, so repaying to target T requires
    R = gross - T * NE = (L - T) * NE, floored at 0 and capped at the
    actual outstanding debt (can never repay more than exists to repay)."""
    target = _clamp_leverage(target_leverage, scenario_cap)
    dead_band = _validate_nonnegative("dead_band", dead_band)
    ne = state.net_equity
    if ne <= 0 or state.margin_debt <= 0:
        return target, 0.0
    lr = state.leverage_ratio
    if lr is None or lr <= target + dead_band:
        return target, 0.0
    repay = state.gross - target * ne
    return target, max(0.0, min(repay, state.margin_debt))


# ── R1 — deposit-cash repayment routing ─────────────────────────────────────

def r1_deposits_first(state: PortfolioState, prior_gross: float | None = None, *,
                      is_deposit_day: bool,
                      target_leverage: float,
                      scenario_cap: float = LEVERAGE_TARGET_HARD_MAX,
                      dead_band: float = 0.0) -> RepaymentDecision:
    """R1 — "Each deposit pays debt to the arm's governed target exposure
    before any purchase" (protocol §5.A.8). Fires only on deposit days
    (`is_deposit_day`, supplied by the caller — this module does not
    itself know the deposit calendar); a non-deposit day is a pure no-op,
    which is exactly what distinguishes this cash-flow-priority family
    from the always-on posture families (R8/R9). On a firing day, repays
    any excess above `target_leverage` (never below it) and caps that same
    day's deposit-driven buying at the same target via
    `effective_leverage_cap` — together, "pays down to target before any
    purchase" and "purchases don't exceed target either."

    `prior_gross` is accepted, positionally, purely for call-signature
    compatibility with the engine's `ScenarioConfig.pre_trade_fn` slot
    (`Callable[[PortfolioState, float | None], RepaymentDecision]`, see
    `simulate()`'s call site) — this family does not use it."""
    is_deposit_day = _validate_bool("is_deposit_day", is_deposit_day)
    if not is_deposit_day:
        return RepaymentDecision()
    target, repay = _plan_repay_to_target(
        state, target_leverage, scenario_cap=scenario_cap, dead_band=dead_band)
    return RepaymentDecision(repay_amount=repay, effective_leverage_cap=target)


# ── R2 — dividend-cash routing (with the frozen reinvest control) ───────────

def r2_dividends_first(state: PortfolioState, prior_gross: float | None = None, *,
                       dividend_cash: float,
                       reinvest: bool = False) -> RepaymentDecision:
    """R2 — "All dividend cash pays debt while debt > 0; reinvested only
    at debt = 0 (control: reinvest)" (protocol §5.A.8;
    `pre_registration.yaml` `R2_dividends_first: {control: reinvest}`).

    `dividend_cash` is the day's already-credited dividend cash amount
    (the engine's own `dividend_credit_series` entry for this day) —
    supplied explicitly rather than observed, preserving the G2A timing
    convention that same-day dividend cash is credited AFTER the
    pre-trade hook runs (see module docstring).

    `reinvest=True` is the family's own registered control configuration:
    dividend cash is never diverted to debt regardless of debt level (a
    pure no-op here — the cash simply remains in the normal cash pool for
    the ordinary deposit/gap-machine path to reinvest, unchanged by this
    function).

    `reinvest=False` (the treatment): while margin_debt > 0, dividend cash
    pays debt, up to the lesser of the dividend cash or the outstanding
    debt — never more (T-D5: never a duplicate or lost dollar; the
    remainder, if `dividend_cash > margin_debt`, is left as ordinary cash
    to reinvest once debt is cleared, satisfying "reinvested only at debt
    = 0" for that remainder without this function needing to track it
    further). At debt = 0, this function always returns `repay_amount =
    0.0` — the XOR is exhaustive: every dollar either reduces debt or is
    left to reinvest, never both, never neither."""
    dividend_cash = _validate_nonnegative("dividend_cash", dividend_cash)
    reinvest = _validate_bool("reinvest", reinvest)
    if reinvest or dividend_cash <= 0 or state.margin_debt <= 0:
        return RepaymentDecision()
    repay = min(dividend_cash, state.margin_debt)
    return RepaymentDecision(repay_amount=repay)


# ── R3 — governed-trim proceeds routing ─────────────────────────────────────

def r3_governed_trims_first(state: PortfolioState, prior_gross: float | None = None, *,
                            trim_proceeds: float) -> RepaymentDecision:
    """R3 — "Production-rule trim proceeds (cluster-cap, T1/T2 ceiling,
    band/spec RSI) pay debt before re-entering the gap machine" (protocol
    §5.A.8). `trim_proceeds` is the day's already-realized trim cash
    (computing which production trims fired, and for how much, is not
    this module's job). While margin_debt > 0, proceeds pay debt up to
    the outstanding balance; any remainder is left as ordinary cash for
    the gap machine, matching "before re-entering the gap machine" — the
    portion that could pay debt does so first, and only the leftover
    re-enters."""
    trim_proceeds = _validate_nonnegative("trim_proceeds", trim_proceeds)
    if trim_proceeds <= 0 or state.margin_debt <= 0:
        return RepaymentDecision()
    repay = min(trim_proceeds, state.margin_debt)
    return RepaymentDecision(repay_amount=repay)


# ── R4 — borrowing-cost hurdle ───────────────────────────────────────────────

def r4_borrowing_cost_hurdle(state: PortfolioState, prior_gross: float | None = None, *,
                             effective_apr: float,
                             hurdle: float,
                             available_cash: float) -> RepaymentDecision:
    """R4 — "Effective APR > H in {6%, 8%} -> all cash flows divert to
    repayment until APR <= H or debt = 0" (protocol §5.A.8;
    `pre_registration.yaml` `R4_cost_hurdle: {apr_hurdle: [0.06, 0.08]}`).
    A rate-LEVEL trigger, strictly greater-than: at `effective_apr ==
    hurdle` exactly, the family is NOT triggered ("until APR <= H" — H
    itself is inside the non-diverting region). `hurdle` is a required,
    no-default argument — this module does not itself pick between the
    two registered values (or invent a third)."""
    effective_apr = _validate_nonnegative("effective_apr", effective_apr)
    hurdle = _validate_nonnegative("hurdle", hurdle)
    available_cash = _validate_nonnegative("available_cash", available_cash)
    if effective_apr <= hurdle or state.margin_debt <= 0 or available_cash <= 0:
        return RepaymentDecision()
    repay = min(available_cash, state.margin_debt)
    return RepaymentDecision(repay_amount=repay)


# ── R5 — trend/volatility deterioration ─────────────────────────────────────

def r5_trend_vol_deterioration(state: PortfolioState, prior_gross: float | None = None, *,
                               trend_deteriorated: bool,
                               vol_deteriorated: bool,
                               scenario_cap: float = LEVERAGE_TARGET_HARD_MAX
                               ) -> RepaymentDecision:
    """R5 — "Benchmark < 200-SMA (t-1) OR 63-day vol > 1.5x trailing-3-yr
    median -> repay to 1.00x; re-lever only per the arm's own rule after
    clearing" (protocol §5.A.8). The two boolean conditions are computed
    by the caller (SMA/vol series belong to `overlay_lib.py`, not this
    module) and combined here with the protocol's own OR. "Re-lever only
    per the arm's own rule after clearing" means this family does nothing
    at all once neither condition holds — it never re-levers itself, by
    design (a pure no-op, not a target it drifts back toward)."""
    trend_deteriorated = _validate_bool("trend_deteriorated", trend_deteriorated)
    vol_deteriorated = _validate_bool("vol_deteriorated", vol_deteriorated)
    if not (trend_deteriorated or vol_deteriorated):
        return RepaymentDecision()
    target, repay = _plan_repay_to_target(
        state, LEVERAGE_TARGET_HARD_MIN, scenario_cap=scenario_cap, dead_band=0.0)
    return RepaymentDecision(repay_amount=repay, effective_leverage_cap=target)


# ── R6 — maintenance-excess deterioration (stateful: weekly staging) ────────

class R6MaintenanceDeterioration:
    """R6 — "Proxy excess < floor + 10pp band -> staged repayment (25% of
    shortfall per week)" (protocol §5.A.8; `pre_registration.yaml`
    `R6_maintenance_deterioration: {band_above_floor_pp: 10,
    staged_fraction_per_week: 0.25}`).

    `floor` (the maintenance-excess-proxy floor itself) has NO fixed
    numeric level anywhere in the frozen protocol/pre-registration —
    `assumptions_ledger.yaml` A-03/A-23 record it as explicitly UNSET,
    "any floor value used later must be fixed and NUM-0001-classified
    before any Study A/B/C run." This class therefore requires it as a
    no-default constructor argument; it never invents one.
    `band_above_floor_pp`/`staged_fraction_per_week` are likewise
    required, no-default arguments — callers are expected to pass the
    pre-registered 10.0 / 0.25, but this class does not silently assume
    them.

    Reads `state.maintenance_excess` (the engine's own opening
    maintenance-excess-proxy field, populated only when the scenario
    configures a `maintenance_requirement_fn`) — raises if it is `None`
    rather than silently no-op'ing, since that would mask a real wiring
    gap (this family cannot be evaluated at all without the proxy).

    Staging cadence: the protocol says "per week" but the only time
    signal `PortfolioState` exposes is `day_index` (a simulation-day
    counter over the trading-day calendar, not a calendar date — the
    engine does not thread the actual date string into `PortfolioState`).
    This class disclosedly treats "one week" as `week_days` (default 7)
    elapsed simulation days since the last staged repayment — the
    coarsest, most literal reading available through the existing
    interface, not a new calibrated number (a 7-day week is a
    unit-definition, the same kind of fixed constant as the engine's own
    `/ 365.0` daily-interest-accrual divisor). Each qualifying week, the
    shortfall (`floor + band - current excess`) is RECOMPUTED from the
    current proxy reading (not fixed at first trigger) — the simplest
    reading of "25% of shortfall per week" that requires no extra state
    beyond a last-fired day index, converging the excess back toward the
    threshold in successive 25% steps."""

    def __init__(self, *, floor: float, band_above_floor_pp: float,
                staged_fraction_per_week: float, week_days: int = 7):
        self.floor = _validate_finite("floor", floor)
        self.band_above_floor_pp = _validate_nonnegative(
            "band_above_floor_pp", band_above_floor_pp)
        staged_fraction_per_week = _validate_finite(
            "staged_fraction_per_week", staged_fraction_per_week)
        if not (0.0 <= staged_fraction_per_week <= 1.0):
            raise ValueError(
                "staged_fraction_per_week must be in [0, 1], got "
                f"{staged_fraction_per_week}")
        self.staged_fraction_per_week = staged_fraction_per_week
        if isinstance(week_days, bool) or not isinstance(week_days, int) or week_days <= 0:
            raise ValueError(f"week_days must be a positive int, got {week_days!r}")
        self.week_days = week_days
        self._last_repay_day: int | None = None

    def __call__(self, state: PortfolioState,
                prior_gross: float | None = None) -> RepaymentDecision:
        if state.maintenance_excess is None:
            raise ValueError(
                "R6MaintenanceDeterioration requires state.maintenance_excess "
                "(the scenario must configure maintenance_requirement_fn) — "
                "None means no maintenance-excess proxy was computed this day")
        if state.margin_debt <= 0:
            return RepaymentDecision()
        threshold = self.floor + self.band_above_floor_pp
        if state.maintenance_excess >= threshold:
            return RepaymentDecision()
        if (self._last_repay_day is not None
                and (state.day_index - self._last_repay_day) < self.week_days):
            return RepaymentDecision()
        shortfall = threshold - state.maintenance_excess
        repay = max(0.0, min(state.margin_debt,
                             self.staged_fraction_per_week * shortfall))
        self._last_repay_day = state.day_index
        return RepaymentDecision(repay_amount=repay)


# ── R7 — Intelligence advisory (freeze / repay), Study D semantics only ─────

class IntelligenceAdvisorySemantic(Enum):
    """The exact three researchable semantics protocol §6 permits — no
    ticker-level recipient veto exists anywhere in this module."""
    ANNOTATION_ONLY_CONTROL = "annotation_only_control"
    WHOLE_CYCLE_DRAW_FREEZE = "whole_cycle_draw_freeze"
    ACCOUNT_LEVEL_REPAYMENT_ADVISORY = "account_level_repayment_advisory"


def r7_intelligence_advisory(state: PortfolioState, prior_gross: float | None = None, *,
                             semantic: IntelligenceAdvisorySemantic,
                             flag_active: bool,
                             target_leverage: float | None = None,
                             scenario_cap: float = LEVERAGE_TARGET_HARD_MAX
                             ) -> RepaymentDecision:
    """R7 — Study D advisory lane (protocol §6; `pre_registration.yaml`
    `R7_intelligence_advisory: {classification: prospective_shadow_only,
    historical_configs: 0}`). `flag_active` is an OPAQUE boolean the
    caller has already decided from a dated, human-authored,
    source-pinned flag record — this function computes no historical
    Intelligence signal, ranking, score, or per-ticker effect of its own,
    and never reads any Intelligence record.

    - `ANNOTATION_ONLY_CONTROL`: always a no-op by definition — "a dated
      risk flag attached to an otherwise valid mechanical action without
      changing it."
    - `WHOLE_CYCLE_DRAW_FREEZE`: when the flag is active, suppresses the
      entire new-margin draw for the cycle by capping today's
      `effective_leverage_cap` at the account's CURRENT leverage (no
      forced sale — a freeze, not a repayment). All-or-nothing at cycle
      (account) level; there is no per-security variant of this call.
    - `ACCOUNT_LEVEL_REPAYMENT_ADVISORY`: when the flag is active,
      hypothetically recommends repayment to `target_leverage` (the
      protocol's own "governed target exposure, or 1.00x" — this function
      requires the caller to say which explicitly; it does not pick one
      of the two permitted readings on its own).

    An inactive flag is always a no-op regardless of semantic — Study D
    is prospective-shadow-only and consumes zero historical trial
    budget; nothing here fires without an externally-supplied flag."""
    flag_active = _validate_bool("flag_active", flag_active)
    if not isinstance(semantic, IntelligenceAdvisorySemantic):
        raise TypeError(
            f"semantic must be an IntelligenceAdvisorySemantic, got {semantic!r}")
    if not flag_active or semantic is IntelligenceAdvisorySemantic.ANNOTATION_ONLY_CONTROL:
        return RepaymentDecision()
    if semantic is IntelligenceAdvisorySemantic.WHOLE_CYCLE_DRAW_FREEZE:
        current = state.leverage_ratio
        if current is None:
            current = LEVERAGE_TARGET_HARD_MIN
        cap = _clamp_leverage(current, scenario_cap)
        return RepaymentDecision(effective_leverage_cap=cap)
    # ACCOUNT_LEVEL_REPAYMENT_ADVISORY
    if target_leverage is None:
        raise ValueError(
            "account_level_repayment_advisory requires an explicit "
            "target_leverage (the arm's governed target exposure, or "
            "1.00x per protocol §6) — never silently defaulted")
    target, repay = _plan_repay_to_target(
        state, target_leverage, scenario_cap=scenario_cap, dead_band=0.0)
    return RepaymentDecision(repay_amount=repay, effective_leverage_cap=target)


# ── R8 — restore-to-target-only ─────────────────────────────────────────────

def r8_restore_to_target_only(state: PortfolioState, prior_gross: float | None = None, *,
                              target_leverage: float,
                              scenario_cap: float = LEVERAGE_TARGET_HARD_MAX,
                              dead_band: float = 0.0) -> RepaymentDecision:
    """R8 — "Repay only leverage above the arm's governed L*; never below
    it by rule" (protocol §5.A.8). Posture-defining: unlike R1, this
    family is evaluated every day, not gated on deposit days — it is the
    arm's standing ceiling, always repaying excess above `target_leverage`
    (never a draw when below it — `_plan_repay_to_target` returns
    `repay_amount == 0.0` in that case) and always capping the same day's
    buying power at the target via `effective_leverage_cap` (harmless on
    a non-deposit day; on a deposit day, prevents that day's purchases
    from pushing leverage back above target)."""
    target, repay = _plan_repay_to_target(
        state, target_leverage, scenario_cap=scenario_cap, dead_band=dead_band)
    return RepaymentDecision(repay_amount=repay, effective_leverage_cap=target)


# ── R9 — full repayment to 1.00x ─────────────────────────────────────────────

def r9_full_repayment_to_unlevered(state: PortfolioState, prior_gross: float | None = None, *,
                                   triggered: bool) -> RepaymentDecision:
    """R9 — "Any trigger under the paired arm's rule repays to zero debt;
    re-deployment only via the arm's deployment rule" (protocol §5.A.8).
    `triggered` is the paired arm's own condition (evaluated by the
    caller — R9 is a posture an arm invokes, not a self-triggering rule);
    when true, repays fully to leverage 1.00x (mathematically exactly
    `margin_debt`, since at leverage L over net_equity NE, gross - 1.0*NE
    == (gross - NE) == margin_debt) and caps that day's buying at 1.00x
    too, so re-deployment genuinely waits for "the arm's own deployment
    rule" rather than this family re-levering on its own the same day."""
    triggered = _validate_bool("triggered", triggered)
    if not triggered:
        return RepaymentDecision()
    target, repay = _plan_repay_to_target(
        state, LEVERAGE_TARGET_HARD_MIN,
        scenario_cap=LEVERAGE_TARGET_HARD_MAX, dead_band=0.0)
    return RepaymentDecision(repay_amount=repay, effective_leverage_cap=target)


# ── R-B — Model B profit-harvest reference path ─────────────────────────────

def rb_model_b_profit_harvest() -> ModelBProfitHarvest:
    """R-B — "Legacy 10%-of-fresh-HWM-gain harvest; one reference
    configuration (Phase 3G established the dose-response)" (protocol
    §5.A.8; `pre_registration.yaml`
    `RB_model_b_profit_harvest_reference: {repay_fraction: 0.10, configs:
    1}`). Delegates entirely to the existing engine implementation
    (`margin_simulation.ModelBProfitHarvest`) rather than duplicating its
    high-water-mark formula — this factory only pins the one registered
    `repay_fraction` value. A fresh instance is returned on every call
    (required — `ModelBProfitHarvest` is stateful; reusing one instance
    across two separate simulation runs would leak high-water-mark state
    between them, same caveat as the engine's own module comment).

    Categorically distinct from R8/R9 (protocol §5.A.8's binding
    "categorical separation"): R-B repays a FRACTION of a fresh
    new-high-water-mark GAIN (a path artifact — "never equated with
    thesis completion"), never restores toward a governed leverage
    target, and is inherently STATEFUL (a running high-water mark), unlike
    every pure R1-R5/R7-R9 function in this module."""
    return ModelBProfitHarvest(repay_fraction=MODEL_B_REFERENCE_REPAY_FRACTION)
