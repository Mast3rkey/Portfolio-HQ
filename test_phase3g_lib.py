"""Tests for phase3g_lib.py -- the Phase 3G sensitivity-testing
execution-layer helpers. All synthetic fixtures, no real data/*.json
usage and no dependency on run_phase3g_sensitivity.py having been run."""

import pytest

from margin_simulation import ModelCRiskReset, PortfolioState
from phase3g_lib import (
    ModelCTriggerLogger,
    estimate_turnover,
    event_amount_stats,
    gap_vs_baseline,
    twr_maxdd_ratio,
)


# ── ModelCTriggerLogger ──────────────────────────────────────────────────────

def test_trigger_logger_records_activation_day():
    inner = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    logger = ModelCTriggerLogger(inner=inner)

    s0 = PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0)
    logger(s0, None)  # establishes hwm=500, no trigger
    assert logger.n_activations == 0

    s1 = PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0)  # >15% drawdown
    logger(s1, None)
    assert logger.n_activations == 1
    assert logger.activation_days == [1]


def test_trigger_logger_does_not_double_count_while_still_active():
    inner = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    logger = ModelCTriggerLogger(inner=inner)
    logger(PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0), None)
    logger(PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0), None)
    # still deep in drawdown next day -- reset_active stays True, no new activation
    logger(PortfolioState(2, cash=0.0, positions={}, margin_debt=100.0, gross=350.0), None)
    assert logger.n_activations == 1


def test_trigger_logger_counts_a_second_episode_after_restoration():
    inner = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    logger = ModelCTriggerLogger(inner=inner)
    logger(PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0), None)  # hwm=500
    logger(PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0), None)   # ne=200, dd 60% -> trigger
    assert logger.n_activations == 1
    # restore: new high (ne=600 > pre_drawdown_hwm=500) AND leverage normalized
    # (also updates hwm to 600, since hwm tracking runs before the restore check)
    logger(PortfolioState(2, cash=0.0, positions={}, margin_debt=100.0, gross=700.0), None)
    assert inner.reset_active is False
    assert inner._hwm == pytest.approx(600.0)
    # a second, independent drawdown episode from the (now 600) peak:
    # ne=500 here is already a >15% drawdown from 600 (16.67%), so this
    # single day both re-updates nothing (ne < hwm) and crosses the
    # trigger -- the second episode activates on this call, not a later one.
    logger(PortfolioState(3, cash=0.0, positions={}, margin_debt=100.0, gross=600.0), None)
    assert logger.n_activations == 2
    assert logger.activation_days == [1, 3]


def test_trigger_logger_never_activates_no_events_for_flat_series():
    inner = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    logger = ModelCTriggerLogger(inner=inner)
    for i in range(5):
        logger(PortfolioState(i, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0), None)
    assert logger.n_activations == 0
    assert logger.activation_days == []


def test_trigger_logger_delegates_decisions_unchanged():
    # The wrapper must be a pure observer -- decisions must be identical
    # to calling the bare policy directly.
    bare = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    wrapped_inner = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    logger = ModelCTriggerLogger(inner=wrapped_inner)

    states = [
        PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0),
        PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0),
        PortfolioState(2, cash=0.0, positions={}, margin_debt=100.0, gross=700.0),
    ]
    for s in states:
        d_bare = bare(s, None)
        d_wrapped = logger(s, None)
        assert d_bare.repay_amount == pytest.approx(d_wrapped.repay_amount)
        assert d_bare.effective_leverage_cap == d_wrapped.effective_leverage_cap


# ── estimate_turnover ────────────────────────────────────────────────────────

def test_estimate_turnover_basic_ratio():
    assert estimate_turnover(total_repaid=88516.45, total_deposited=124000.0) == pytest.approx(0.7139, abs=1e-3)


def test_estimate_turnover_zero_deposited_returns_zero_not_error():
    assert estimate_turnover(total_repaid=100.0, total_deposited=0.0) == 0.0


def test_estimate_turnover_zero_repaid():
    assert estimate_turnover(total_repaid=0.0, total_deposited=124000.0) == 0.0


# ── event_amount_stats ───────────────────────────────────────────────────────

def test_event_amount_stats_basic():
    events = [
        {"kind": "repayment", "amount": 100.0},
        {"kind": "repayment", "amount": 200.0},
        {"kind": "repayment", "amount": 300.0},
        {"kind": "deposit", "amount": 2000.0},
    ]
    stats = event_amount_stats(events, "repayment")
    assert stats["count"] == 3
    assert stats["total"] == pytest.approx(600.0)
    assert stats["mean"] == pytest.approx(200.0)
    assert stats["median"] == pytest.approx(200.0)
    assert stats["max"] == pytest.approx(300.0)


def test_event_amount_stats_empty_returns_zeros_not_error():
    stats = event_amount_stats([{"kind": "deposit", "amount": 2000.0}], "repayment")
    assert stats == {"count": 0, "total": 0.0, "mean": 0.0, "median": 0.0, "max": 0.0}


def test_event_amount_stats_even_count_median():
    events = [{"kind": "x", "amount": a} for a in (10.0, 20.0, 30.0, 40.0)]
    stats = event_amount_stats(events, "x")
    assert stats["median"] == pytest.approx(25.0)


# ── twr_maxdd_ratio ──────────────────────────────────────────────────────────

def test_twr_maxdd_ratio_basic():
    assert twr_maxdd_ratio(35.59, -26.81) == pytest.approx(35.59 / 26.81)


def test_twr_maxdd_ratio_zero_drawdown_returns_none():
    assert twr_maxdd_ratio(10.0, 0.0) is None


# ── gap_vs_baseline ──────────────────────────────────────────────────────────

def test_gap_vs_baseline():
    assert gap_vs_baseline(33.28, 35.59) == pytest.approx(-2.31, abs=1e-2)
    assert gap_vs_baseline(-24.74, -26.81) == pytest.approx(2.07, abs=1e-2)
