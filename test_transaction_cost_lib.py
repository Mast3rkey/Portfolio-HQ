"""Tests for transaction_cost_lib.py. All synthetic fixtures; no
dependency on real data/*.json or on run_transaction_cost_sensitivity.py
having been run."""

import pytest

from transaction_cost_lib import cost_adjusted_twr, event_costs, total_transaction_cost


# ── event_costs ──────────────────────────────────────────────────────────────

def test_event_costs_basic_5bps():
    events = [{"kind": "repayment", "amount": 1000.0}, {"kind": "repayment", "amount": 200.0}]
    costs = event_costs(events, bps=5.0)
    assert costs == pytest.approx([0.5, 0.1])  # 5bps = 0.05%


def test_event_costs_15bps():
    events = [{"kind": "repayment", "amount": 1000.0}]
    assert event_costs(events, bps=15.0) == pytest.approx([1.5])


def test_event_costs_zero_bps_is_zero_cost():
    events = [{"kind": "repayment", "amount": 1000.0}]
    assert event_costs(events, bps=0.0) == pytest.approx([0.0])


def test_event_costs_ignores_non_repayment_events():
    events = [
        {"kind": "deposit", "amount": 2000.0},
        {"kind": "interest_accrual", "amount": 5.0},
        {"kind": "margin_draw", "amount": 300.0},
        {"kind": "repayment", "amount": 100.0},
    ]
    assert event_costs(events, bps=10.0) == pytest.approx([0.1])


def test_event_costs_respects_custom_kind():
    events = [{"kind": "margin_draw", "amount": 100.0}, {"kind": "repayment", "amount": 100.0}]
    assert event_costs(events, bps=10.0, kind="margin_draw") == pytest.approx([0.1])


def test_event_costs_negative_bps_raises():
    with pytest.raises(ValueError):
        event_costs([{"kind": "repayment", "amount": 100.0}], bps=-1.0)


def test_event_costs_empty_events_is_empty_list():
    assert event_costs([], bps=5.0) == []


# ── total_transaction_cost ───────────────────────────────────────────────────

def test_total_transaction_cost_sums_all_events():
    events = [
        {"kind": "repayment", "amount": 1000.0},
        {"kind": "repayment", "amount": 2000.0},
        {"kind": "deposit", "amount": 5000.0},
    ]
    assert total_transaction_cost(events, bps=5.0) == pytest.approx(1.5)  # 0.5 + 1.0


def test_total_transaction_cost_zero_when_no_matching_events():
    events = [{"kind": "deposit", "amount": 1000.0}]
    assert total_transaction_cost(events, bps=15.0) == 0.0


def test_total_transaction_cost_matches_known_phase3g_scale():
    # Reproduces the real order of magnitude from docs/results/PHASE3_
    # SENSITIVITY_RESULTS.json's model_b_sensitivity["0.25"] entry:
    # total_repaid = $88,516.45 across 296 events. At 15bps, total cost
    # should be a small fraction of that, not comparable in magnitude.
    total_repaid = 88516.45
    events = [{"kind": "repayment", "amount": total_repaid}]  # single aggregate event, same total
    cost = total_transaction_cost(events, bps=15.0)
    assert cost == pytest.approx(132.77, abs=0.01)
    assert cost < total_repaid * 0.01  # cost is well under 1% of turnover


# ── cost_adjusted_twr ────────────────────────────────────────────────────────

def test_cost_adjusted_twr_zero_cost_matches_unadjusted():
    from backtest_regime import twr_annualized
    values = [100.0, 110.0, 121.0, 133.1]
    flows = {0: 100.0}
    baseline = twr_annualized(values, flows)
    adjusted = cost_adjusted_twr(values, flows, total_cost=0.0)
    assert adjusted == pytest.approx(baseline)


def test_cost_adjusted_twr_lower_with_nonzero_cost():
    values = [100.0, 110.0, 121.0, 133.1]
    flows = {0: 100.0}
    baseline = cost_adjusted_twr(values, flows, total_cost=0.0)
    with_cost = cost_adjusted_twr(values, flows, total_cost=10.0)
    assert with_cost < baseline


def test_cost_adjusted_twr_does_not_mutate_input_series():
    values = [100.0, 110.0, 121.0]
    original = list(values)
    cost_adjusted_twr(values, {0: 100.0}, total_cost=5.0)
    assert values == original


def test_cost_adjusted_twr_empty_series_returns_zero():
    assert cost_adjusted_twr([], {}, total_cost=10.0) == 0.0


def test_cost_adjusted_twr_only_touches_final_value():
    # First-order approximation per the plan: cost is deducted from the
    # LAST value only, not distributed across the path.
    values = [100.0, 200.0, 300.0]
    adjusted_high_cost = cost_adjusted_twr(values, {0: 100.0}, total_cost=250.0)
    # with a large enough cost, final value goes negative/near-zero,
    # producing a very different (likely much lower) TWR than baseline
    baseline = cost_adjusted_twr(values, {0: 100.0}, total_cost=0.0)
    assert adjusted_high_cost < baseline
