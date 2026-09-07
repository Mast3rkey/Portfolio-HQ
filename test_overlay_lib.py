"""Tests for overlay_lib.py (MARGIN-0005 S2, third/final authorized S2 PR).

All fixtures are small, synthetic, hand-computable price series -- never
real data/backtest/*.json prices, never a registered Study A configuration.
Nothing here calls margin_simulation.simulate() as a registered trial or
creates trial_ledger.jsonl/candidate_freeze.yaml.

Import-graph isolation (T-8) and TR-namespace / write-path structural bars
for overlay_lib.py are tested centrally in test_validation_lib.py
(parametrized across every S2 module this PR adds); this file focuses
exclusively on overlay_lib.py's own signal/decision-function behavior.
"""

import math

import pytest

from margin_simulation import LEVERAGE_TARGET_HARD_MAX, LEVERAGE_TARGET_HARD_MIN
from overlay_lib import (
    STUDY_A_DEAD_BAND,
    drawdown_from_peak_series,
    ema_series,
    overlay_a6_trend,
    overlay_a7_vol_target,
    overlay_a8_staged_pullback,
    overlay_a9_crash_only,
    overlay_a10_regime,
    overlay_a11_trend_plus_vol,
    realized_vol_series,
    risk_on_series,
    sma_series,
    trend_above_sma_series,
)


# ═════════════════════════════════════════════════════════════════════════
# Signal-series builders — t-1 lag / no-lookahead (T-2)
# ═════════════════════════════════════════════════════════════════════════

def test_sma_series_hand_computed_example():
    closes = [10.0, 20.0, 30.0, 40.0, 50.0]
    got = sma_series(closes, window=2)
    assert got == [None, None, 15.0, 25.0, 35.0]


def test_sma_series_matches_direct_slice_definition_on_a_longer_series():
    closes = [100.0 + i * (-1) ** i for i in range(60)]
    window = 10
    got = sma_series(closes, window)
    for i in range(window, len(closes)):
        expect = sum(closes[i - window:i]) / window
        assert math.isclose(got[i], expect, rel_tol=1e-9)
    assert all(v is None for v in got[:window])


def test_sma_series_rejects_bad_window():
    with pytest.raises(ValueError):
        sma_series([1.0, 2.0], window=0)


def test_ema_series_seed_uses_only_prior_closes():
    closes = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
    window = 3
    got = ema_series(closes, window)
    assert got[:window] == [None] * window
    assert math.isclose(got[window], sum(closes[:window]) / window)  # seed = simple mean of closes[0:window]
    alpha = 2.0 / (window + 1.0)
    expect_next = alpha * closes[window] + (1 - alpha) * got[window]
    assert math.isclose(got[window + 1], expect_next, rel_tol=1e-9)


def test_ema_series_short_series_returns_all_none():
    assert ema_series([1.0, 2.0], window=5) == [None, None]


def test_trend_above_sma_series_no_lookahead_property():
    # Perturbing the LAST close cannot change any earlier decision -- the
    # defining no-lookahead property (T-2).
    closes = [100.0 + i for i in range(10)]
    base = trend_above_sma_series(closes, window=3)
    perturbed = list(closes)
    perturbed[-1] += 1000.0
    after = trend_above_sma_series(perturbed, window=3)
    assert base[:-1] == after[:-1]


def test_trend_above_sma_series_hand_computed():
    closes = [10.0, 10.0, 10.0, 20.0, 20.0]
    got = trend_above_sma_series(closes, window=2)
    # sma_series(window=2) = [None, None, 10.0, 10.0, 15.0]
    # signal[i] = closes[i-1] > sma[i]
    # i=2: closes[1]=10 > sma[2]=10 -> False
    # i=3: closes[2]=10 > sma[3]=10 -> False
    # i=4: closes[3]=20 > sma[4]=15 -> True
    assert got == [None, None, False, False, True]


def test_risk_on_series_hand_computed_mirrors_ema():
    closes = [10.0, 20.0, 30.0, 100.0]
    window = 2
    ema = ema_series(closes, window)
    got = risk_on_series(closes, window)
    for i in range(len(closes)):
        if ema[i] is None:
            assert got[i] is None
        else:
            assert got[i] == (closes[i - 1] > ema[i])


def test_realized_vol_series_flat_series_is_zero_once_available():
    closes = [100.0] * 20
    got = realized_vol_series(closes, window=5)
    assert got[6] == 0.0
    assert all(v is None for v in got[:6])


def test_realized_vol_series_no_lookahead_property():
    closes = [100.0 + (i % 3) * 2 for i in range(30)]
    base = realized_vol_series(closes, window=5)
    perturbed = list(closes)
    perturbed[-1] *= 5
    after = realized_vol_series(perturbed, window=5)
    assert base[:-1] == after[:-1]


def test_realized_vol_series_rejects_bad_window():
    with pytest.raises(ValueError):
        realized_vol_series([1.0, 2.0, 3.0], window=1)


def test_drawdown_from_peak_series_full_hand_trace():
    closes = [100.0, 110.0, 90.0, 95.0, 80.0]
    got = drawdown_from_peak_series(closes)
    # i=1: px=closes[0]=100, peak=100 -> dd=0/100-... = 100/100-1=0.0
    assert math.isclose(got[1], 0.0)
    # i=2: px=closes[1]=110, peak=max(100,110)=110 -> dd=110/110-1=0.0
    assert math.isclose(got[2], 0.0)
    # i=3: px=closes[2]=90, peak=max(110,90)=110 -> dd=90/110-1
    assert math.isclose(got[3], 90.0 / 110.0 - 1.0)
    # i=4: px=closes[3]=95, peak=max(110,95)=110 -> dd=95/110-1
    assert math.isclose(got[4], 95.0 / 110.0 - 1.0)


# ═════════════════════════════════════════════════════════════════════════
# Overlay decision functions — pure, always within [1.0, 1.8] (T-4)
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("trend,l_hi,expect", [
    (True, 1.10, 1.10), (True, 1.25, 1.25), (True, 1.50, 1.50), (False, 1.50, 1.0),
])
def test_overlay_a6_trend(trend, l_hi, expect):
    d = overlay_a6_trend(trend, l_hi=l_hi)
    assert math.isclose(d.leverage_target, expect)
    assert d.dead_band == STUDY_A_DEAD_BAND


def test_overlay_a6_purity():
    d1 = overlay_a6_trend(True, l_hi=1.25)
    d2 = overlay_a6_trend(True, l_hi=1.25)
    assert d1.leverage_target == d2.leverage_target and d1.dead_band == d2.dead_band


@pytest.mark.parametrize("vol,sigma,l_max,expect", [
    (0.20, 0.10, 1.50, 0.5),   # 0.10/0.20=0.5, below LEVERAGE_TARGET_HARD_MIN -> clamped to 1.0
    (0.05, 0.10, 1.50, 1.50),  # 0.10/0.05=2.0, capped at l_max=1.50
    (0.10, 0.10, 1.25, 1.0),   # exactly 1.0 -> unlevered
    (0.0, 0.10, 1.25, 1.25),   # degenerate zero vol -> targets l_max directly
])
def test_overlay_a7_vol_target(vol, sigma, l_max, expect):
    d = overlay_a7_vol_target(vol, sigma_target=sigma, l_max=l_max)
    assert math.isclose(d.leverage_target, min(max(expect, LEVERAGE_TARGET_HARD_MIN), LEVERAGE_TARGET_HARD_MAX))


def test_overlay_a7_rejects_bad_params():
    with pytest.raises(ValueError):
        overlay_a7_vol_target(0.1, sigma_target=0.0, l_max=1.5)
    with pytest.raises(ValueError):
        overlay_a7_vol_target(0.1, sigma_target=0.1, l_max=0.0)


def test_overlay_a8_staged_pullback_deepest_tranche_wins():
    tranches = {-0.10: 1.10, -0.15: 1.25, -0.20: 1.40}
    assert overlay_a8_staged_pullback(-0.05, tranches=tranches).leverage_target == 1.0
    assert math.isclose(overlay_a8_staged_pullback(-0.12, tranches=tranches).leverage_target, 1.10)
    assert math.isclose(overlay_a8_staged_pullback(-0.18, tranches=tranches).leverage_target, 1.25)
    assert math.isclose(overlay_a8_staged_pullback(-0.25, tranches=tranches).leverage_target, 1.40)


def test_overlay_a8_recovery_repays_to_unlevered():
    tranches = {-0.10: 1.10, -0.20: 1.40}
    deep = overlay_a8_staged_pullback(-0.25, tranches=tranches)
    recovered = overlay_a8_staged_pullback(-0.02, tranches=tranches)
    assert deep.leverage_target > recovered.leverage_target == 1.0


def test_overlay_a8_rejects_nonneg_tranche_threshold():
    with pytest.raises(ValueError):
        overlay_a8_staged_pullback(-0.1, tranches={0.05: 1.1})


def test_overlay_a8_rejects_empty_tranches():
    with pytest.raises(ValueError):
        overlay_a8_staged_pullback(-0.1, tranches={})


def test_overlay_a9_crash_only_triggers_and_recovers():
    below_trigger = overlay_a9_crash_only(-0.25, trigger_drawdown=-0.20, l_star=1.25, recovered=False)
    assert math.isclose(below_trigger.leverage_target, 1.25)
    above_trigger = overlay_a9_crash_only(-0.10, trigger_drawdown=-0.20, l_star=1.25, recovered=False)
    assert below_trigger.leverage_target > 1.0
    assert above_trigger.leverage_target == 1.0
    recovered = overlay_a9_crash_only(-0.22, trigger_drawdown=-0.20, l_star=1.25, recovered=True)
    assert recovered.leverage_target == 1.0  # recovery overrides an otherwise-triggered drawdown


def test_overlay_a9_full_episode_trough_anchored_vs_naive_current_drawdown():
    # F-3: a complete no-trigger -> trigger -> trough -> partial-recovery ->
    # repay-priority -> reset episode, proving the correct calling contract
    # (drawdown = episode trough while held; recovered = a separately
    # tracked current-drawdown-vs-(-0.05) flag) against the documented
    # naive interpretation (feeding raw current-day drawdown throughout).
    trigger_drawdown, l_star = -0.20, 1.25

    def call(drawdown, recovered):
        return overlay_a9_crash_only(drawdown, trigger_drawdown=trigger_drawdown,
                                     l_star=l_star, recovered=recovered).leverage_target

    # Day 0 -- no-trigger state: a mild dip, well short of the -20% trigger.
    assert call(-0.05, recovered=False) == 1.0

    # Day 1 -- trigger at or below -20%: first breach: trough == current == -0.22.
    assert math.isclose(call(-0.22, recovered=False), l_star)

    # Day 2 -- trough deepens further to -0.30 (still no recovery).
    assert math.isclose(call(-0.30, recovered=False), l_star)

    # Day 3 -- partial recovery: current price has bounced to -0.15 (short of
    # the -5% recovery bar), but under the CORRECT contract the caller still
    # passes the EPISODE TROUGH (-0.30, unchanged by an interim bounce) and
    # recovered stays False (current -0.15 has not reached -0.05) -- leverage
    # must remain held at l_star through the whole episode, not just while
    # today's raw drawdown sits below the trigger.
    correct_partial_recovery = call(-0.30, recovered=False)
    assert math.isclose(correct_partial_recovery, l_star), (
        "trough-anchored contract must hold l_star through a partial bounce")

    # The NAIVE interpretation -- feeding the raw current-day drawdown
    # (-0.15) instead of the trough, still with recovered=False -- is
    # documented as WRONG: it prematurely de-levers a full crash-recovery
    # cycle before the registered -5% recovery point is ever reached. This
    # assertion pins that the two interpretations genuinely diverge (not a
    # test of desired behavior for the naive path -- a demonstration of why
    # the docstring's contract matters).
    naive_partial_recovery = call(-0.15, recovered=False)
    assert naive_partial_recovery == 1.0
    assert correct_partial_recovery != naive_partial_recovery

    # Day 4 -- repay-priority state: current drawdown finally reaches -0.04
    # (>= -0.05) -- the caller flips recovered=True. This forces the exit
    # to 1.00 EVEN THOUGH the trough value passed in is still deeply
    # negative (-0.30) -- recovered overrides a "still-negative-but-
    # recovering drawdown" exactly as the base docstring states.
    assert call(-0.30, recovered=True) == 1.0

    # Day 5 -- exit/reset: a new, unrelated mild dip after the episode has
    # fully closed; trough resets to the current (shallow) value for any
    # future episode, recovered is no longer relevant.
    assert call(-0.02, recovered=False) == 1.0


def test_overlay_a9_rejects_bad_params():
    with pytest.raises(ValueError):
        overlay_a9_crash_only(-0.1, trigger_drawdown=0.05, l_star=1.25, recovered=False)
    with pytest.raises(ValueError):
        overlay_a9_crash_only(-0.1, trigger_drawdown=-0.2, l_star=0.0, recovered=False)


@pytest.mark.parametrize("risk_on,l_hi,expect", [(True, 1.10, 1.10), (True, 1.25, 1.25), (False, 1.25, 1.0)])
def test_overlay_a10_regime(risk_on, l_hi, expect):
    d = overlay_a10_regime(risk_on, l_hi=l_hi)
    assert math.isclose(d.leverage_target, expect)


def test_overlay_a11_trend_off_targets_unlevered():
    d = overlay_a11_trend_plus_vol(False, 0.15, sigma_target=0.10, l_hi=1.25, l_max=1.50)
    assert d.leverage_target == 1.0


def test_overlay_a11_takes_the_lesser_of_a6_and_a7():
    # trend on, l_hi=1.50 (A6 side), vol scaling gives 0.10/0.20=0.5 (A7 side,
    # clamped by [1.0, l_max]) -- the combined rule must never exceed the
    # LESSER survivor, here the vol-target leg after its own floor clamp.
    d = overlay_a11_trend_plus_vol(True, 0.20, sigma_target=0.10, l_hi=1.50, l_max=1.50)
    assert math.isclose(d.leverage_target, 1.0)  # min(1.50, clamp(0.5)) -> min(1.50, 1.0) = 1.0
    d2 = overlay_a11_trend_plus_vol(True, 0.05, sigma_target=0.10, l_hi=1.25, l_max=1.50)
    assert math.isclose(d2.leverage_target, 1.25)  # min(1.25, min(2.0,1.50)=1.50) = 1.25


@pytest.mark.parametrize("fn,kwargs", [
    (overlay_a6_trend, dict(trend_above_sma=True, l_hi=1.8)),
    (overlay_a7_vol_target, dict(current_vol=0.01, sigma_target=0.5, l_max=1.8)),
    (overlay_a8_staged_pullback, dict(drawdown=-0.5, tranches={-0.1: 1.8})),
    (overlay_a9_crash_only, dict(drawdown=-0.9, trigger_drawdown=-0.2, l_star=1.8, recovered=False)),
    (overlay_a10_regime, dict(risk_on=True, l_hi=1.8)),
    (overlay_a11_trend_plus_vol, dict(trend_above_sma=True, current_vol=0.01, sigma_target=0.5, l_hi=1.8, l_max=1.8)),
])
def test_every_overlay_leverage_target_stays_within_governed_bounds(fn, kwargs):
    # Even deliberately extreme inputs (l_hi/l_star/l_max all at 1.8, a
    # near-zero vol) must never push leverage_target outside [1.0, 1.8].
    d = fn(**kwargs)
    assert LEVERAGE_TARGET_HARD_MIN <= d.leverage_target <= LEVERAGE_TARGET_HARD_MAX


@pytest.mark.parametrize("fn,kwargs", [
    (overlay_a6_trend, dict(trend_above_sma=True, l_hi=5.0)),
    (overlay_a10_regime, dict(risk_on=True, l_hi=5.0)),
])
def test_overlay_clamps_an_out_of_range_l_hi_to_the_hard_cap(fn, kwargs):
    d = fn(**kwargs)
    assert d.leverage_target == LEVERAGE_TARGET_HARD_MAX


def test_overlay_scenario_cap_can_only_tighten_never_loosen():
    d = overlay_a6_trend(True, l_hi=1.8, scenario_cap=1.2)
    assert d.leverage_target == 1.2
    with pytest.raises(ValueError):
        overlay_a6_trend(True, l_hi=1.5, scenario_cap=0.5)  # below hard min -> rejected
