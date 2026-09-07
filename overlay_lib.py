"""
overlay_lib.py — MARGIN-0005 research-only Study A margin-overlay decision
library (S2, third and final authorized S2 PR under the charter's <=3
ceiling; scope per `research/margin_target_study/S2_G2_SCOPE_DETERMINATION.md`
§5, item 3 — "permitted but not strictly required for G2," needed instead
for Study A to ever execute at S3).

Authorized by `governance/decisions/MARGIN-0005-margin-target-research-charter.md`
(charter §4, "Research package" row) and `PROTOCOL_V2.md` §5 (Study A arms
A-6 through A-11) / §13.

## Scope

Implements the six Study A overlay families that depend on a mechanical
market/account SIGNAL rather than a pure account-state posture (the
account-state-only families — R1-R9 — already live in `repayment_lib.py`;
this module is their signal-driven counterpart, exactly the split
`repayment_lib.py`'s own docstring calls out: "Computing those external
signals (SMA/vol from price series...) is explicitly NOT this module's
job — that belongs to `overlay_lib.py`"):

  * **A-6** trend-controlled (`benchmark_close_gt_200sma_t_minus_1`)
  * **A-7** volatility-targeted (63-day realized vol, account or benchmark source)
  * **A-8** staged pullback (fixed drawdown-tranche schedule)
  * **A-9** crash-only (single drawdown trigger, repay-priority recovery)
  * **A-10** market-regime (200-EMA risk-on/off)
  * **A-11** trend+vol combined (surviving A-6/A-7 grid points only)

Each decision function is a PURE function of an explicit, caller-supplied
t-1 signal value (T-4: "pure functions of t-1 state") and returns a
`margin_simulation.RepaymentDecision` with `leverage_target` set — directly
consumable by `ScenarioConfig.pre_trade_fn` — ALWAYS clamped to
`[1.0, 1.8]` (T-4), reusing the engine's own governed
`LEVERAGE_TARGET_HARD_MIN`/`LEVERAGE_TARGET_HARD_MAX` constants rather than
redefining them (same reuse discipline `repayment_lib.py` already
established).

The signal-SERIES builders below (`sma_series`, `realized_vol_series`,
`drawdown_from_peak_series`, `ema_series`) are a small, deliberate,
dependency-free reimplementation over the `list[float]` closes shape this
research harness uses (`margin_simulation.simulate()`'s own `aligned`
convention) — NOT a reuse of `indicators.py`'s bar-dict, single-point-
lookup API, which is shaped for a different call pattern (one live value
from a truncated bar list) than what a full backtest loop needs (a
day-by-day signal series with t-1 lag structurally baked into the series
itself). This mirrors `margin_simulation.py`'s own precedent of
deliberately re-deriving `_leverage_capped_margin()` rather than importing
`allocate.py`'s `margin_capacity()` — reuse where the shape genuinely
fits (`backtest_regime.twr_annualized`/`max_drawdown`), re-derive where it
doesn't, on purpose, disclosed here rather than silently forced.

Zero import relationship with `allocate.py`/`margin_state.py` in either
direction. No file or network I/O anywhere in this module — every signal
arrives as an explicit, in-memory `list[float]` supplied by the caller
(a future `run_study_a.py`, S3 scope, not built here). Never calls
`margin_simulation.simulate()`; never touches `trial_ledger.jsonl` or
`candidate_freeze.yaml`; consumes zero of the 300-run trial ceiling.

`dead_band` on every decision function defaults to `0.05` — the frozen
`pre_registration.yaml` `studies.study_a.mechanics.dead_band` value, which
applies to every Study A arm alike (unlike, say, R6's maintenance-proxy
floor, which the frozen documents explicitly leave UNSET) — so defaulting
to it here is citing a pinned number, not guessing one.
"""

from __future__ import annotations

import math

from margin_simulation import (
    LEVERAGE_TARGET_HARD_MAX,
    LEVERAGE_TARGET_HARD_MIN,
    RepaymentDecision,
)

# Frozen pre_registration.yaml studies.study_a.mechanics.dead_band.
STUDY_A_DEAD_BAND = 0.05


def _clamp_leverage(target: float, scenario_cap: float = LEVERAGE_TARGET_HARD_MAX) -> float:
    """Every leverage target this module emits passes through here —
    clamped to [1.00, min(scenario_cap, 1.80)], never violable regardless
    of what any overlay computes (T-4)."""
    if not math.isfinite(target):
        raise ValueError(f"target must be finite, got {target}")
    if not math.isfinite(scenario_cap) or scenario_cap < LEVERAGE_TARGET_HARD_MIN:
        raise ValueError(f"scenario_cap must be finite and >= {LEVERAGE_TARGET_HARD_MIN}, got {scenario_cap}")
    return min(max(target, LEVERAGE_TARGET_HARD_MIN), scenario_cap, LEVERAGE_TARGET_HARD_MAX)


# ═════════════════════════════════════════════════════════════════════════
# Signal-series builders — t-1 lag structurally baked in: series[i] uses
# only closes[0 .. i-1], never closes[i] or later (T-2: no-lookahead).
# ═════════════════════════════════════════════════════════════════════════

def sma_series(closes: list[float], window: int) -> list[float | None]:
    """Trailing simple-moving-average series. `series[i]` is the mean of
    `closes[i-window:i]` (strictly ending at i-1) when `i >= window`, else
    `None`. Implemented as a running sum with an O(1) update per step
    (add the newly-in-range close, subtract the one that just fell out of
    the trailing window) — equivalent to, and checked against, the
    direct-slice definition above."""
    if window <= 0:
        raise ValueError(f"window must be > 0, got {window}")
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0:
        return out
    running = 0.0
    for i in range(1, n):
        running += closes[i - 1]
        if i > window:
            running -= closes[i - 1 - window]
        if i >= window:
            out[i] = running / window
    return out


def ema_series(closes: list[float], window: int) -> list[float | None]:
    """Trailing exponential-moving-average series (standard `2/(window+1)`
    smoothing), same t-1 lag convention as `sma_series()`: `series[i]`
    reflects data strictly through `closes[i-1]`. Seeded with a simple
    average of the first `window` closes once available, then
    exponentially smoothed forward — `series[i] is None` for `i < window`."""
    if window <= 0:
        raise ValueError(f"window must be > 0, got {window}")
    n = len(closes)
    out: list[float | None] = [None] * n
    if n <= window:
        return out
    alpha = 2.0 / (window + 1.0)
    seed = sum(closes[:window]) / window
    out[window] = seed
    prev = seed
    for i in range(window + 1, n):
        prev = alpha * closes[i - 1] + (1.0 - alpha) * prev
        out[i] = prev
    return out


def trend_above_sma_series(closes: list[float], window: int = 200) -> list[bool | None]:
    """A-6 signal: `closes[i-1] > sma_series[i]` (both strictly t-1
    information) — `None` until both are available."""
    sma = sma_series(closes, window)
    n = len(closes)
    out: list[bool | None] = [None] * n
    for i in range(1, n):
        if sma[i] is not None:
            out[i] = closes[i - 1] > sma[i]
    return out


def risk_on_series(closes: list[float], window: int = 200) -> list[bool | None]:
    """A-10 signal: `closes[i-1] > ema_series[i]` (200-EMA risk-on/off),
    same t-1 lag convention as `trend_above_sma_series()`."""
    ema = ema_series(closes, window)
    n = len(closes)
    out: list[bool | None] = [None] * n
    for i in range(1, n):
        if ema[i] is not None:
            out[i] = closes[i - 1] > ema[i]
    return out


def realized_vol_series(closes: list[float], window: int = 63, *,
                        annualization_days: int = 252) -> list[float | None]:
    """Trailing annualized realized-volatility series: the sample standard
    deviation of simple daily returns over the `window` returns strictly
    ending at day i-1, annualized by `sqrt(annualization_days)`. `None`
    until `window` returns are available (requires `window + 1` prior
    closes). `closes` may be the account's own book series or a
    benchmark's price series (`source in {account, benchmark}` per
    `pre_registration.yaml` A7_vol_target) — this function is source-
    agnostic; the caller decides which series to pass in."""
    if window <= 1:
        raise ValueError(f"window must be > 1, got {window}")
    n = len(closes)
    returns = [closes[k] / closes[k - 1] - 1.0 for k in range(1, n)] if n > 1 else []
    out: list[float | None] = [None] * n
    for i in range(n):
        # returns available strictly before day i are returns[0 .. i-2]
        # (returns[k] = closes[k]/closes[k-1]-1 is "known" as of day k,
        # i.e. strictly before day k+1) — the trailing `window` of those
        # ending at i-1 requires i-1 >= window, i.e. i >= window + 1.
        if i >= window + 1:
            r = returns[i - 1 - window:i - 1]
            mean = sum(r) / window
            var = sum((x - mean) ** 2 for x in r) / (window - 1)
            out[i] = math.sqrt(var) * math.sqrt(annualization_days)
    return out


def drawdown_from_peak_series(closes: list[float]) -> list[float | None]:
    """`series[i]` = `closes[i-1] / running_peak(closes[0..i-1]) - 1.0`
    (always <= 0), `None` for `i == 0` (no prior data)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    peak = None
    for i in range(1, n):
        px = closes[i - 1]
        peak = px if peak is None else max(peak, px)
        out[i] = px / peak - 1.0
    return out


# ═════════════════════════════════════════════════════════════════════════
# Overlay decision functions — pure, t-1-signal-driven leverage targets.
# ═════════════════════════════════════════════════════════════════════════

def overlay_a6_trend(trend_above_sma: bool, *, l_hi: float,
                     dead_band: float = STUDY_A_DEAD_BAND,
                     scenario_cap: float = LEVERAGE_TARGET_HARD_MAX) -> RepaymentDecision:
    """A-6 — trend-controlled: `l_hi` in `{1.10, 1.25, 1.50}` above the
    benchmark's 200-SMA (t-1), else `1.00` (`pre_registration.yaml`
    `A6_trend`)."""
    target = l_hi if trend_above_sma else LEVERAGE_TARGET_HARD_MIN
    return RepaymentDecision(leverage_target=_clamp_leverage(target, scenario_cap),
                            dead_band=dead_band)


def overlay_a7_vol_target(current_vol: float, *, sigma_target: float, l_max: float,
                          dead_band: float = STUDY_A_DEAD_BAND,
                          scenario_cap: float = LEVERAGE_TARGET_HARD_MAX) -> RepaymentDecision:
    """A-7 — volatility-targeted: `target = sigma_target / current_vol`,
    capped at `l_max` (`pre_registration.yaml` A7_vol_target: `sigma_target
    in {0.10, 0.15}`, `L_max in {1.25, 1.50}`). A non-positive
    `current_vol` (a degenerate/zero-history input) is treated as "no
    volatility observed to scale against" and targets `l_max` directly —
    the ceiling the arm's own grid already defines, not an unbounded value."""
    if sigma_target <= 0:
        raise ValueError(f"sigma_target must be > 0, got {sigma_target}")
    if l_max <= 0:
        raise ValueError(f"l_max must be > 0, got {l_max}")
    raw = l_max if current_vol <= 0 else sigma_target / current_vol
    target = min(raw, l_max)
    return RepaymentDecision(leverage_target=_clamp_leverage(target, scenario_cap),
                            dead_band=dead_band)


def overlay_a8_staged_pullback(drawdown: float, *, tranches: dict[float, float],
                               dead_band: float = STUDY_A_DEAD_BAND,
                               scenario_cap: float = LEVERAGE_TARGET_HARD_MAX
                               ) -> RepaymentDecision:
    """A-8 — staged pullback: `tranches` maps a (negative) drawdown
    threshold to its target leverage, e.g. `{-0.10: 1.10, -0.15: 1.25,
    -0.20: 1.40}` (`pre_registration.yaml` A8_staged_pullback). The target
    is the DEEPEST breached tranche's leverage (`drawdown <= threshold`,
    most negative threshold that still qualifies); `1.00` if no tranche is
    breached. Because the target is a pure function of the current
    drawdown alone, recovery above every threshold naturally repays back
    to `1.00` ("repay on recovery") without any separate stateful logic."""
    if not tranches:
        raise ValueError("tranches must be non-empty")
    for th in tranches:
        if th >= 0:
            raise ValueError(f"tranche thresholds must be negative drawdowns, got {th}")
    breached = [th for th in tranches if drawdown <= th]
    target = tranches[min(breached)] if breached else LEVERAGE_TARGET_HARD_MIN
    return RepaymentDecision(leverage_target=_clamp_leverage(target, scenario_cap),
                            dead_band=dead_band)


def overlay_a9_crash_only(drawdown: float, *, trigger_drawdown: float, l_star: float,
                          recovered: bool,
                          dead_band: float = STUDY_A_DEAD_BAND,
                          scenario_cap: float = LEVERAGE_TARGET_HARD_MAX
                          ) -> RepaymentDecision:
    """A-9 — crash-only: at `drawdown <= trigger_drawdown` (e.g. -0.20),
    target `l_star` in `{1.25, 1.50}`; `recovered` (the caller's own
    "drawdown recovered to within -5% of peak" computation, per
    `pre_registration.yaml` A9_crash_only's `repay_priority_recovery:
    -0.05`) forces the target back to `1.00` with repay priority,
    overriding a still-negative-but-recovering drawdown. Neither trigger
    active: no-op posture at `1.00`.

    ## Calling contract (F-3 clarification) — `drawdown` is TROUGH-anchored
    during a held episode, not the raw current-day value

    This function is pure and stateless (T-4) — it holds no memory of
    a prior call — so the CALLER (a future `run_study_a.py`, S3 scope) is
    responsible for supplying two distinct, independently-tracked t-1
    quantities on every call, not one shared "current drawdown" value:

    * `drawdown` — during an ACTIVE, still-held crash episode (from the
      day the trigger first fires until `recovered` goes `True`), this
      must be the EPISODE'S TROUGH: the deepest (most negative)
      `drawdown_from_peak_series()` value observed since the trigger
      fired, monotonically updated to a new low on any day price falls
      further, and otherwise held flat through interim bounces. Before any
      trigger and after an episode exits/resets, it is simply the current
      day's drawdown (trough and current coincide when there is no held
      episode). This is deliberately NOT the raw current-day drawdown
      throughout a held episode — see the naive-interpretation warning
      below.
    * `recovered` — a SEPARATE flag the caller derives from the ACTUAL
      CURRENT drawdown (not the trough) crossing the `-0.05`
      `repay_priority_recovery` threshold: `True` from the first day
      current drawdown rises to `>= -0.05` and LATCHED there until the
      next trigger (a new episode, trough resets to that day's drawdown).

    **Why**: `pre_registration.yaml`'s A-9 design deliberately holds
    leverage at `l_star` through the WHOLE episode down to a much
    shallower `-0.05` recovery point, not merely while today's drawdown
    happens to sit below the `-0.20` trigger. A **naive interpretation**
    that feeds this function the raw, un-anchored current-day drawdown on
    every call gets this wrong: once price bounces from a -30% trough to,
    say, -15% (still well short of the -5% recovery bar), `drawdown <=
    trigger_drawdown` (`-0.15 <= -0.20`) is `False`, and with `recovered`
    still `False` the function falls through to the `1.00` no-op branch —
    prematurely de-levering mid-episode, a full crash-recovery cycle
    before the registered design intends. Passing the trough (still
    `-0.30`) instead correctly keeps the `elif` branch active and holds
    `l_star` until `recovered` itself flips. See
    `test_overlay_a9_full_episode_trough_anchored_vs_naive_current_drawdown`
    in `test_overlay_lib.py` for a complete no-trigger -> trigger -> trough
    -> partial-recovery -> repay-priority -> reset episode trace, run
    against both interpretations, pinning the trough-anchored contract as
    correct and the naive one as wrong at the partial-recovery step.

    This module remains library-level and explicit-input-only by design —
    it does not itself track trough state or implement a runner; that
    bookkeeping is S3 scope, deliberately kept out of this pure function."""
    if trigger_drawdown >= 0:
        raise ValueError(f"trigger_drawdown must be a negative drawdown, got {trigger_drawdown}")
    if l_star <= 0:
        raise ValueError(f"l_star must be > 0, got {l_star}")
    if recovered:
        target = LEVERAGE_TARGET_HARD_MIN
    elif drawdown <= trigger_drawdown:
        target = l_star
    else:
        target = LEVERAGE_TARGET_HARD_MIN
    return RepaymentDecision(leverage_target=_clamp_leverage(target, scenario_cap),
                            dead_band=dead_band)


def overlay_a10_regime(risk_on: bool, *, l_hi: float,
                       dead_band: float = STUDY_A_DEAD_BAND,
                       scenario_cap: float = LEVERAGE_TARGET_HARD_MAX) -> RepaymentDecision:
    """A-10 — market-regime: `l_hi` in `{1.10, 1.25}` while `risk_on`
    (200-EMA regime signal, `risk_on_series()` above), else `1.00`
    (`pre_registration.yaml` A10_regime)."""
    target = l_hi if risk_on else LEVERAGE_TARGET_HARD_MIN
    return RepaymentDecision(leverage_target=_clamp_leverage(target, scenario_cap),
                            dead_band=dead_band)


def overlay_a11_trend_plus_vol(trend_above_sma: bool, current_vol: float, *,
                               sigma_target: float, l_hi: float, l_max: float,
                               dead_band: float = STUDY_A_DEAD_BAND,
                               scenario_cap: float = LEVERAGE_TARGET_HARD_MAX
                               ) -> RepaymentDecision:
    """A-11 — trend+vol combined (`pre_registration.yaml` A11_trend_plus_vol:
    "surviving A6/A7 grid points only"): while `trend_above_sma`, target is
    the LESSER of A-6's `l_hi` and A-7's `sigma_target / current_vol` (both
    capped at `l_max`) — the combined rule never levers up further than
    either individual survivor alone would; `1.00` when the trend signal is
    off, matching A-6's own off-state."""
    if not trend_above_sma:
        target = LEVERAGE_TARGET_HARD_MIN
    else:
        vol_target = l_max if current_vol <= 0 else min(sigma_target / current_vol, l_max)
        target = min(l_hi, vol_target)
    return RepaymentDecision(leverage_target=_clamp_leverage(target, scenario_cap),
                            dead_band=dead_band)
