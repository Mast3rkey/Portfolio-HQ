"""Tests for phase4a_lib.py -- Phase 4A execution-layer helpers. All
synthetic fixtures; no dependency on real data/*.json or on
run_phase4a_research.py having been run."""

import pytest

from phase4a_lib import (
    RecoveryInfo,
    apply_synthetic_shock,
    classify_event_repetition,
    classify_gap,
    concentration_series,
    forced_deleveraging_events,
    inflate_weights,
    is_recovery_material,
    ticker_own_max_drawdown,
    time_above_threshold_pct,
    worst_drawdown_recovery,
)


# ── inflate_weights ──────────────────────────────────────────────────────────

def test_inflate_weights_multiplies_named_ticker_only():
    w = {"A": 3.35, "B": 1.65, "C": 1.0}
    out = inflate_weights(w, ["A"], 3.0)
    assert out["A"] == pytest.approx(10.05)
    assert out["B"] == pytest.approx(1.65)  # untouched
    assert out["C"] == pytest.approx(1.0)   # untouched
    assert w["A"] == pytest.approx(3.35)    # original not mutated


def test_inflate_weights_multiple_tickers():
    w = {"A": 1.0, "B": 1.0, "C": 1.0}
    out = inflate_weights(w, ["A", "B"], 2.0)
    assert out["A"] == pytest.approx(2.0)
    assert out["B"] == pytest.approx(2.0)
    assert out["C"] == pytest.approx(1.0)


def test_inflate_weights_ignores_unknown_ticker():
    w = {"A": 1.0}
    out = inflate_weights(w, ["ZZZ"], 5.0)
    assert out == {"A": 1.0}


def test_inflate_weights_negative_multiplier_raises():
    with pytest.raises(ValueError):
        inflate_weights({"A": 1.0}, ["A"], -1.0)


def test_inflate_weights_redistribution_is_mechanical_via_normalization():
    # Confirms the docstring's claim: inflating one ticker's raw weight
    # increases every OTHER ticker's normalized denominator, shrinking
    # their effective share, without any explicit redistribution step.
    w = {"A": 1.0, "B": 1.0}
    inflated = inflate_weights(w, ["A"], 3.0)
    w_sum_before = sum(w.values())
    w_sum_after = sum(inflated.values())
    b_share_before = w["B"] / w_sum_before
    b_share_after = inflated["B"] / w_sum_after
    assert b_share_after < b_share_before


# ── apply_synthetic_shock ────────────────────────────────────────────────────

def test_apply_synthetic_shock_declines_over_duration():
    aligned = {"A": ([100.0] * 10, 0)}
    out = apply_synthetic_shock(aligned, "A", shock_pct=-40.0, start_idx=2, duration_days=4)
    closes = out["A"][0]
    assert closes[0] == 100.0 and closes[1] == 100.0  # untouched before start
    assert closes[2] > closes[3] > closes[4] > closes[5]  # monotonic decline
    assert closes[5] == pytest.approx(60.0, abs=0.5)  # ~-40% by end of duration


def test_apply_synthetic_shock_holds_flat_after_duration():
    aligned = {"A": ([100.0] * 10, 0)}
    out = apply_synthetic_shock(aligned, "A", shock_pct=-50.0, start_idx=0, duration_days=3)
    closes = out["A"][0]
    assert closes[2] == pytest.approx(50.0, abs=0.5)
    assert closes[3] == closes[2]
    assert closes[9] == closes[2]  # held flat, no auto-recovery modeled


def test_apply_synthetic_shock_does_not_mutate_other_tickers():
    aligned = {"A": ([100.0] * 5, 0), "B": ([100.0] * 5, 0)}
    out = apply_synthetic_shock(aligned, "A", shock_pct=-30.0, start_idx=0, duration_days=2)
    assert out["B"][0] == aligned["B"][0]  # B's series untouched
    assert aligned["A"][0] == [100.0] * 5  # original A untouched


def test_apply_synthetic_shock_invalid_duration_raises():
    aligned = {"A": ([100.0] * 5, 0)}
    with pytest.raises(ValueError):
        apply_synthetic_shock(aligned, "A", shock_pct=-10.0, start_idx=0, duration_days=0)


def test_apply_synthetic_shock_negative_start_raises():
    aligned = {"A": ([100.0] * 5, 0)}
    with pytest.raises(ValueError):
        apply_synthetic_shock(aligned, "A", shock_pct=-10.0, start_idx=-1, duration_days=2)


# ── ticker_own_max_drawdown ──────────────────────────────────────────────────

def test_ticker_own_max_drawdown_basic():
    aligned = {"A": ([100.0, 200.0, 50.0, 80.0], 0)}
    dd = ticker_own_max_drawdown(aligned, "A")
    assert dd == pytest.approx(-75.0)  # 200 -> 50


def test_ticker_own_max_drawdown_ignores_none_entries():
    aligned = {"A": ([None, None, 100.0, 40.0], 2)}
    dd = ticker_own_max_drawdown(aligned, "A")
    assert dd == pytest.approx(-60.0)


def test_ticker_own_max_drawdown_no_decline_is_zero():
    aligned = {"A": ([100.0, 110.0, 120.0], 0)}
    assert ticker_own_max_drawdown(aligned, "A") == 0.0


# ── concentration_series ─────────────────────────────────────────────────────

def test_concentration_series_single_ticker():
    tracked = {"A": [50.0, 60.0, 30.0]}
    book = [100.0, 100.0, 100.0]
    series = concentration_series(tracked, book)
    assert series == pytest.approx([50.0, 60.0, 30.0])


def test_concentration_series_sums_multiple_tracked_tickers():
    tracked = {"A": [50.0, 20.0], "B": [10.0, 10.0]}
    book = [100.0, 100.0]
    series = concentration_series(tracked, book)
    assert series == pytest.approx([60.0, 30.0])


def test_concentration_series_zero_book_returns_zero_not_error():
    tracked = {"A": [10.0]}
    book = [0.0]
    assert concentration_series(tracked, book) == [0.0]


def test_concentration_series_empty_tracked_returns_zeros():
    assert concentration_series({}, [100.0, 100.0]) == [0.0, 0.0]


# ── time_above_threshold_pct ─────────────────────────────────────────────────

def test_time_above_threshold_basic():
    assert time_above_threshold_pct([10.0, 20.0, 30.0], threshold=15.0) == pytest.approx(200/3)


def test_time_above_threshold_ignores_none():
    assert time_above_threshold_pct([None, 20.0, None, 5.0], threshold=15.0) == 50.0


def test_time_above_threshold_empty_is_zero():
    assert time_above_threshold_pct([], threshold=1.0) == 0.0


# ── forced_deleveraging_events ───────────────────────────────────────────────

def test_forced_deleveraging_events_detects_breach_days():
    series = [1.0, 1.5, 2.1, 1.9, 1.79]
    events = forced_deleveraging_events(series, leverage_cap=1.8)
    assert events == [2, 3]


def test_forced_deleveraging_events_ignores_none():
    series = [None, 2.5, None]
    assert forced_deleveraging_events(series, leverage_cap=1.8) == [1]


def test_forced_deleveraging_events_none_when_never_breached():
    assert forced_deleveraging_events([1.0, 1.2, 1.5], leverage_cap=1.8) == []


def test_forced_deleveraging_events_ignores_floating_point_noise():
    # Reproduces the real bug found running Phase 4A's own first execution:
    # an "unlevered" scenario's margin_debt residue (~1e-12 after many buy/
    # sell operations) makes leverage compute as slightly above 1.0 exactly
    # (e.g. 1.0000000000000002) despite never actually drawing margin. Must
    # NOT be counted as a forced-deleveraging event.
    series = [1.0, 1.0000000000000002, 1.0, 1.0000000000000004]
    assert forced_deleveraging_events(series, leverage_cap=1.0) == []


def test_forced_deleveraging_events_real_breach_still_detected_past_epsilon():
    # A genuine breach is orders of magnitude larger than the float-noise
    # tolerance and must still be caught.
    series = [1.0, 1.0000000000000002, 1.05, 1.9]
    assert forced_deleveraging_events(series, leverage_cap=1.8) == [3]


# ── classify_event_repetition ────────────────────────────────────────────────

def test_classify_event_repetition_single_event_single_case_not_repeated():
    assert classify_event_repetition({"case1": 1, "case2": 0, "case3": 0}) is False


def test_classify_event_repetition_three_in_one_case_is_repeated():
    assert classify_event_repetition({"case1": 3, "case2": 0}) is True


def test_classify_event_repetition_two_events_in_two_cases_is_repeated():
    assert classify_event_repetition({"case1": 1, "case2": 1, "case3": 0}) is True


def test_classify_event_repetition_zero_everywhere_not_repeated():
    assert classify_event_repetition({"case1": 0, "case2": 0}) is False


# ── worst_drawdown_recovery ───────────────────────────────────────────────────

def test_worst_drawdown_recovery_finds_trough_and_recovers():
    values = [100.0, 120.0, 60.0, 90.0, 125.0]
    r = worst_drawdown_recovery(values)
    assert r.peak_index == 1
    assert r.trough_index == 2
    assert r.peak_value == pytest.approx(120.0)
    assert r.trough_value == pytest.approx(60.0)
    assert r.recovery_index == 4  # first day >= 120.0 after the trough
    assert r.recovery_days == 2


def test_worst_drawdown_recovery_never_recovers():
    values = [100.0, 120.0, 60.0, 70.0]
    r = worst_drawdown_recovery(values)
    assert r.trough_index == 2
    assert r.recovery_index is None
    assert r.recovery_days is None


def test_worst_drawdown_recovery_monotonic_rise_no_drawdown():
    values = [100.0, 110.0, 120.0]
    r = worst_drawdown_recovery(values)
    assert r.trough_index is None
    assert r.recovery_index is None


def test_worst_drawdown_recovery_empty_series():
    r = worst_drawdown_recovery([])
    assert r == RecoveryInfo(None, None, None, None, None, None)


# ── is_recovery_material ─────────────────────────────────────────────────────

def test_is_recovery_material_relative_threshold():
    assert is_recovery_material(stressed_days=30, baseline_days=10) is True  # 3x >= 1.5x
    assert is_recovery_material(stressed_days=12, baseline_days=10) is False  # 1.2x < 1.5x


def test_is_recovery_material_absolute_floor_when_no_baseline():
    assert is_recovery_material(stressed_days=25, baseline_days=None) is True
    assert is_recovery_material(stressed_days=15, baseline_days=None) is False


def test_is_recovery_material_never_recovered_is_false_not_true():
    # "never recovered" is a distinct, more severe finding -- not folded
    # into a bare materiality flag, per the module's documented reasoning.
    assert is_recovery_material(stressed_days=None, baseline_days=10) is False


def test_is_recovery_material_zero_baseline_uses_absolute_floor():
    assert is_recovery_material(stressed_days=25, baseline_days=0) is True
    assert is_recovery_material(stressed_days=15, baseline_days=0) is False


# ── classify_gap ──────────────────────────────────────────────────────────────

def test_classify_gap_material():
    assert classify_gap(2.5) == "material"
    assert classify_gap(-2.5) == "material"


def test_classify_gap_noise():
    assert classify_gap(0.3) == "noise"
    assert classify_gap(-0.5) == "noise"  # exactly at floor counts as noise


def test_classify_gap_suggestive():
    assert classify_gap(1.0) == "suggestive"


def test_classify_gap_exactly_at_material_threshold():
    assert classify_gap(2.0) == "material"
