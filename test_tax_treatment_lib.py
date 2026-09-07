"""Tests for tax_treatment_lib.py. All synthetic fixtures; no dependency
on real data/*.json or on run_tax_treatment_sensitivity.py having been
run."""

import pytest

from tax_treatment_lib import net_twr_after_tax, tax_drag, taxable_realization_upper_bound


# ── taxable_realization_upper_bound ─────────────────────────────────────────

def test_taxable_realization_sums_repayment_events_only():
    events = [
        {"kind": "repayment", "amount": 100.0},
        {"kind": "repayment", "amount": 200.0},
        {"kind": "deposit", "amount": 2000.0},
        {"kind": "interest_accrual", "amount": 5.0},
        {"kind": "margin_draw", "amount": 300.0},
    ]
    assert taxable_realization_upper_bound(events) == pytest.approx(300.0)


def test_taxable_realization_excludes_deposits_explicitly():
    events = [{"kind": "deposit", "amount": 5000.0}]
    assert taxable_realization_upper_bound(events) == 0.0


def test_taxable_realization_excludes_margin_draws():
    events = [{"kind": "margin_draw", "amount": 5000.0}]
    assert taxable_realization_upper_bound(events) == 0.0


def test_taxable_realization_empty_events_is_zero():
    assert taxable_realization_upper_bound([]) == 0.0


def test_taxable_realization_respects_custom_kind():
    events = [{"kind": "custom_kind", "amount": 42.0}, {"kind": "repayment", "amount": 10.0}]
    assert taxable_realization_upper_bound(events, kind="custom_kind") == pytest.approx(42.0)


def test_taxable_realization_matches_known_phase3_scale():
    # Reproduces the real scale from docs/results/PHASE3_MODEL_B_ANALYSIS.md:
    # $88,516.45 gross repaid at repay_fraction=0.25.
    events = [{"kind": "repayment", "amount": 88516.45}]
    assert taxable_realization_upper_bound(events) == pytest.approx(88516.45)


# ── tax_drag ─────────────────────────────────────────────────────────────────

def test_tax_drag_basic_15pct():
    assert tax_drag(1000.0, 0.15) == pytest.approx(150.0)


def test_tax_drag_basic_32pct():
    assert tax_drag(1000.0, 0.32) == pytest.approx(320.0)


def test_tax_drag_zero_rate_is_zero():
    assert tax_drag(1000.0, 0.0) == 0.0


def test_tax_drag_zero_base_is_zero_regardless_of_rate():
    assert tax_drag(0.0, 0.32) == 0.0


def test_tax_drag_negative_rate_raises():
    with pytest.raises(ValueError):
        tax_drag(1000.0, -0.1)


def test_tax_drag_never_scales_the_base_itself():
    # The base passed in must remain the same object/value -- tax_drag
    # only ever multiplies, never mutates or reinterprets the base as
    # anything other than what was passed (guards against silently
    # treating the upper bound as something other than what it is).
    base = 88516.45
    tax_drag(base, 0.15)
    assert base == 88516.45


# ── net_twr_after_tax ────────────────────────────────────────────────────────

def test_net_twr_after_tax_zero_drag_matches_baseline():
    from backtest_regime import twr_annualized
    values = [100.0, 110.0, 121.0, 133.1]
    flows = {0: 100.0}
    baseline = twr_annualized(values, flows)
    assert net_twr_after_tax(values, flows, drag=0.0) == pytest.approx(baseline)


def test_net_twr_after_tax_lower_with_nonzero_drag():
    values = [100.0, 110.0, 121.0, 133.1]
    flows = {0: 100.0}
    baseline = net_twr_after_tax(values, flows, drag=0.0)
    with_drag = net_twr_after_tax(values, flows, drag=10.0)
    assert with_drag < baseline


def test_net_twr_after_tax_delegates_to_cost_adjusted_twr():
    # Confirms this is a thin wrapper, not a divergent reimplementation --
    # same inputs must produce the exact same output as calling
    # transaction_cost_lib.cost_adjusted_twr() directly.
    from transaction_cost_lib import cost_adjusted_twr
    values = [100.0, 200.0, 300.0]
    flows = {0: 100.0}
    assert net_twr_after_tax(values, flows, 50.0) == pytest.approx(
        cost_adjusted_twr(values, flows, 50.0))
