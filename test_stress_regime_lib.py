"""Tests for stress_regime_lib.py. All synthetic fixtures except the
load_aligned_ohlcv() smoke test, which reads the real cached QQQ.json
(already used by every prior Phase 3 backtest) to confirm real data
loads correctly -- not a dependency on run_stress_regime_sensitivity.py
having been run."""

import pytest

from stress_regime_lib import (
    EventStressSplit,
    base_rate_days_in_stress,
    day_in_any_window,
    detect_stress_days,
    load_aligned_ohlcv,
    nearest_window_distance,
    regime_conditional_cost,
    split_events_by_stress_window,
    stress_windows_from_days,
)


# ── load_aligned_ohlcv ──────────────────────────────────────────────────────

def test_load_aligned_ohlcv_real_data_smoke_test():
    calendar = ["2021-06-01", "2021-06-02", "2021-06-03"]
    data = load_aligned_ohlcv("QQQ", calendar)
    assert set(data.keys()) == {"h", "l", "c", "v"}
    for field in data:
        assert len(data[field]) == 3
        assert all(v is not None for v in data[field])  # real trading days, real data


def test_load_aligned_ohlcv_forward_fills_missing_date():
    calendar = ["2021-06-01", "2099-01-01"]  # second date has no real bar
    data = load_aligned_ohlcv("QQQ", calendar)
    assert data["c"][1] == data["c"][0]  # forward-filled from the last real value


# ── detect_stress_days ───────────────────────────────────────────────────────

def _flat_series(n, close=100.0, high=101.0, low=99.0, volume=1000.0):
    return [high] * n, [low] * n, [close] * n, [volume] * n


def test_detect_stress_days_no_stress_on_flat_series():
    highs, lows, closes, volumes = _flat_series(80)
    flags = detect_stress_days(highs, lows, closes, volumes, trailing_window=60)
    assert not any(flags)  # constant range/volume never exceeds its own trailing average


def test_detect_stress_days_first_trailing_window_days_never_flagged():
    highs, lows, closes, volumes = _flat_series(30)
    flags = detect_stress_days(highs, lows, closes, volumes, trailing_window=60)
    assert len(flags) == 30
    assert not any(flags)  # insufficient history for any day to be evaluated


def test_detect_stress_days_flags_volatility_spike():
    highs, lows, closes, volumes = _flat_series(65)
    # spike the range on day 64 (last day) well above the trailing average
    highs[64] = 130.0
    lows[64] = 70.0
    flags = detect_stress_days(highs, lows, closes, volumes, trailing_window=60,
                               volatility_multiplier=1.5)
    assert flags[64] is True
    assert not any(flags[:64])


def test_detect_stress_days_flags_liquidity_drop():
    highs, lows, closes, volumes = _flat_series(65)
    volumes[64] = 100.0  # far below the trailing average of 1000
    flags = detect_stress_days(highs, lows, closes, volumes, trailing_window=60,
                               liquidity_fraction=0.7)
    assert flags[64] is True


def test_detect_stress_days_handles_none_values_without_crashing():
    highs, lows, closes, volumes = _flat_series(65)
    closes[64] = None
    flags = detect_stress_days(highs, lows, closes, volumes, trailing_window=60)
    assert flags[64] is False  # can't evaluate a day with missing data -- not flagged


# ── stress_windows_from_days ─────────────────────────────────────────────────

def test_stress_windows_basic_run():
    flags = [False, False, True, True, True, False, False]
    windows = stress_windows_from_days(flags, min_window_days=3, merge_gap_days=5)
    assert windows == [(2, 4)]


def test_stress_windows_discards_short_runs():
    flags = [False, True, True, False, False]  # only 2 days, below min_window_days=3
    windows = stress_windows_from_days(flags, min_window_days=3, merge_gap_days=5)
    assert windows == []


def test_stress_windows_merges_close_runs():
    flags = [True, True, True, False, False, True, True, True]  # gap of 2 days
    windows = stress_windows_from_days(flags, min_window_days=3, merge_gap_days=5)
    assert windows == [(0, 7)]  # merged into one


def test_stress_windows_does_not_merge_distant_runs():
    flags = ([True] * 3 + [False] * 10 + [True] * 3)
    windows = stress_windows_from_days(flags, min_window_days=3, merge_gap_days=5)
    assert windows == [(0, 2), (13, 15)]


def test_stress_windows_empty_input():
    assert stress_windows_from_days([], min_window_days=3) == []


def test_stress_windows_all_flagged_to_end_of_series():
    flags = [False, False, True, True, True]
    windows = stress_windows_from_days(flags, min_window_days=3, merge_gap_days=5)
    assert windows == [(2, 4)]


# ── day_in_any_window / nearest_window_distance ─────────────────────────────

def test_day_in_any_window():
    windows = [(5, 10), (20, 25)]
    assert day_in_any_window(7, windows) is True
    assert day_in_any_window(15, windows) is False
    assert day_in_any_window(20, windows) is True  # boundary inclusive
    assert day_in_any_window(25, windows) is True  # boundary inclusive


def test_nearest_window_distance_inside_is_zero():
    assert nearest_window_distance(7, [(5, 10)]) == 0


def test_nearest_window_distance_outside():
    assert nearest_window_distance(15, [(5, 10), (20, 25)]) == 5  # 5 away from day 10 and day 20


def test_nearest_window_distance_no_windows_returns_sentinel():
    assert nearest_window_distance(5, []) == 10**9


# ── split_events_by_stress_window ───────────────────────────────────────────

def test_split_events_basic():
    events = [
        {"kind": "repayment", "day": 3, "amount": 100.0},
        {"kind": "repayment", "day": 7, "amount": 200.0},  # inside window (5,10)
        {"kind": "deposit", "day": 8, "amount": 2000.0},  # wrong kind, excluded
    ]
    split = split_events_by_stress_window(events, windows=[(5, 10)])
    assert len(split.in_window) == 1
    assert len(split.outside_window) == 1
    assert split.total_amount == pytest.approx(300.0)
    assert split.in_window_amount == pytest.approx(200.0)
    assert split.outside_window_amount == pytest.approx(100.0)
    assert split.in_window_dollar_fraction == pytest.approx(200.0 / 300.0)


def test_split_events_no_matching_events_zero_fraction():
    split = split_events_by_stress_window([], windows=[(5, 10)])
    assert split.total_amount == 0.0
    assert split.in_window_dollar_fraction == 0.0


def test_split_events_respects_custom_kind():
    events = [{"kind": "custom", "day": 5, "amount": 50.0}]
    split = split_events_by_stress_window(events, windows=[(5, 10)], kind="custom")
    assert split.in_window_amount == pytest.approx(50.0)


# ── base_rate_days_in_stress ────────────────────────────────────────────────

def test_base_rate_days_in_stress_basic():
    windows = [(0, 9)]  # 10 days
    assert base_rate_days_in_stress(windows, n_days=100) == pytest.approx(10.0)


def test_base_rate_days_in_stress_no_windows():
    assert base_rate_days_in_stress([], n_days=100) == 0.0


def test_base_rate_days_in_stress_clips_to_n_days():
    windows = [(90, 150)]  # extends beyond n_days
    rate = base_rate_days_in_stress(windows, n_days=100)
    assert rate == pytest.approx(10.0)  # only days 90-99 count


def test_base_rate_days_in_stress_zero_days_is_zero():
    assert base_rate_days_in_stress([(0, 5)], n_days=0) == 0.0


# ── regime_conditional_cost ──────────────────────────────────────────────────

def test_regime_conditional_cost_applies_base_rate_outside_window():
    events = [{"kind": "repayment", "day": 50, "amount": 1000.0}]  # outside (5,10)
    cost = regime_conditional_cost(events, windows=[(5, 10)], base_bps=15.0, stress_multiplier=3.0)
    assert cost == pytest.approx(1.5)  # 15bps of 1000


def test_regime_conditional_cost_applies_multiplied_rate_inside_window():
    events = [{"kind": "repayment", "day": 7, "amount": 1000.0}]  # inside (5,10)
    cost = regime_conditional_cost(events, windows=[(5, 10)], base_bps=15.0, stress_multiplier=3.0)
    assert cost == pytest.approx(4.5)  # 45bps of 1000


def test_regime_conditional_cost_negative_inputs_raise():
    events = [{"kind": "repayment", "day": 1, "amount": 100.0}]
    with pytest.raises(ValueError):
        regime_conditional_cost(events, [], base_bps=-1.0, stress_multiplier=1.0)
    with pytest.raises(ValueError):
        regime_conditional_cost(events, [], base_bps=1.0, stress_multiplier=-1.0)


def test_regime_conditional_cost_ignores_non_matching_kind():
    events = [{"kind": "deposit", "day": 7, "amount": 1000.0}]
    cost = regime_conditional_cost(events, windows=[(5, 10)], base_bps=15.0, stress_multiplier=3.0)
    assert cost == 0.0
