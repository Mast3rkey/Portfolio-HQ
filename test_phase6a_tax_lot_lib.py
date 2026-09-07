"""Tests for phase6a_tax_lot_lib.py. All synthetic fixtures — small,
hand-computable tax_lot_events lists, matching this project's convention
for every prior *_lib.py module's own test file."""

import pytest

from phase6a_tax_lot_lib import net_taxable_base, realized_gain_summary


def _ev(proceeds, cost_basis, holding_period, acq="2021-01-01", sale="2021-06-01"):
    return {
        "proceeds": proceeds,
        "cost_basis": cost_basis,
        "realized_gain": proceeds - cost_basis,
        "holding_period": holding_period,
        "acquisition_date": acq,
        "sale_date": sale,
    }


def test_realized_gain_summary_empty_events():
    s = realized_gain_summary([])
    assert s["n_disposal_events"] == 0
    assert s["total_proceeds"] == 0.0
    assert s["total_realized_gain_net"] == 0.0
    assert s["avg_holding_period_days_proceeds_weighted"] == 0.0
    assert s["short_term_gain_pct_of_gains"] == 0.0


def test_realized_gain_summary_basic_gain():
    events = [_ev(1500.0, 1000.0, "short_term")]
    s = realized_gain_summary(events)
    assert s["n_disposal_events"] == 1
    assert s["n_gain_events"] == 1
    assert s["n_loss_events"] == 0
    assert s["total_proceeds"] == pytest.approx(1500.0)
    assert s["total_cost_basis"] == pytest.approx(1000.0)
    assert s["total_realized_gain_net"] == pytest.approx(500.0)
    assert s["total_realized_gains"] == pytest.approx(500.0)
    assert s["total_realized_losses"] == pytest.approx(0.0)
    assert s["short_term_gain_dollars"] == pytest.approx(500.0)
    assert s["short_term_gain_pct_of_gains"] == pytest.approx(100.0)
    assert s["long_term_gain_pct_of_gains"] == pytest.approx(0.0)


def test_realized_gain_summary_mixed_gains_and_losses():
    events = [
        _ev(1500.0, 1000.0, "short_term"),  # +500 gain, ST
        _ev(800.0, 1000.0, "long_term"),    # -200 loss, LT
        _ev(2000.0, 1000.0, "long_term"),   # +1000 gain, LT
    ]
    s = realized_gain_summary(events)
    assert s["n_gain_events"] == 2
    assert s["n_loss_events"] == 1
    assert s["total_realized_gain_net"] == pytest.approx(500.0 - 200.0 + 1000.0)
    assert s["total_realized_gains"] == pytest.approx(1500.0)
    assert s["total_realized_losses"] == pytest.approx(-200.0)
    # ST gain = 500, LT gain = 1000 -- losses excluded from the gain split
    assert s["short_term_gain_dollars"] == pytest.approx(500.0)
    assert s["long_term_gain_dollars"] == pytest.approx(1000.0)
    assert s["short_term_gain_pct_of_gains"] == pytest.approx(500.0 / 1500.0 * 100.0)
    assert s["long_term_gain_pct_of_gains"] == pytest.approx(1000.0 / 1500.0 * 100.0)


def test_realized_gain_summary_holding_period_weighted_by_proceeds():
    # event 1: 5 days held, $1000 proceeds; event 2: 365 days held, $3000 proceeds
    events = [
        _ev(1000.0, 900.0, "short_term", acq="2021-01-01", sale="2021-01-06"),  # 5 days
        _ev(3000.0, 2500.0, "long_term", acq="2021-01-01", sale="2022-01-01"),  # 365 days
    ]
    s = realized_gain_summary(events)
    expected = (5 * 1000.0 + 365 * 3000.0) / (1000.0 + 3000.0)
    assert s["avg_holding_period_days_proceeds_weighted"] == pytest.approx(expected)


def test_net_taxable_base_floors_a_net_loss_at_zero_by_default():
    events = [_ev(800.0, 1000.0, "long_term")]  # -200 net
    assert net_taxable_base(events) == 0.0


def test_net_taxable_base_unfloored_shows_the_negative_value():
    events = [_ev(800.0, 1000.0, "long_term")]  # -200 net
    assert net_taxable_base(events, floor_at_zero=False) == pytest.approx(-200.0)


def test_net_taxable_base_sums_gains_and_losses_net():
    events = [
        _ev(1500.0, 1000.0, "short_term"),  # +500
        _ev(800.0, 1000.0, "long_term"),    # -200
    ]
    assert net_taxable_base(events) == pytest.approx(300.0)
