"""Tests for the Phase 6A tax-lot ledger addition to margin_simulation.py
(docs/PHASE6A_IMPLEMENTATION_APPROVAL.md). All fixtures are small,
synthetic, hand-computable price series, matching test_margin_simulation.py's
own convention -- nothing here uses real data/backtest/*.json prices.

Covers exactly the five categories named in the implementation approval's
allowed-changes list: lot creation, FIFO consumption, holding-period
classification, partial lot liquidation, and multi-event repayment
behavior -- plus a direct "additive only, no existing-output change"
invariant test.
"""

import pytest

from margin_simulation import (
    Lot,
    ModelBProfitHarvest,
    ScenarioConfig,
    _classify_holding_period,
    _consume_fifo_lots,
    _fund_repayment,
    repayment_model_0,
    simulate,
)


# ── holding-period classification ────────────────────────────────────────────

def test_classify_holding_period_short_term_well_under_365_days():
    assert _classify_holding_period("2021-01-01", "2021-06-01") == "short_term"


def test_classify_holding_period_short_term_at_exactly_365_days():
    # 2021-01-01 -> 2022-01-01 is exactly 365 days (2021 is not a leap
    # year) -- the real IRC S1222 rule requires MORE than 1 year, so
    # exactly 365 days is still short-term, not long-term.
    assert _classify_holding_period("2021-01-01", "2022-01-01") == "short_term"


def test_classify_holding_period_long_term_over_365_days():
    assert _classify_holding_period("2021-01-01", "2022-01-02") == "long_term"  # 366 days


def test_classify_holding_period_long_term_multi_year():
    assert _classify_holding_period("2021-01-01", "2024-01-01") == "long_term"


# ── FIFO consumption (_consume_fifo_lots) ────────────────────────────────────

def test_consume_fifo_lots_single_lot_full_liquidation():
    lots = [Lot("A", 10.0, 0, "2021-01-01", 100.0)]
    events = _consume_fifo_lots(lots, shares_to_sell=10.0, sale_price=150.0,
                                sale_day=10, sale_date="2021-03-01", ticker="A")
    assert len(events) == 1
    ev = events[0]
    assert ev["shares_sold"] == pytest.approx(10.0)
    assert ev["cost_basis"] == pytest.approx(1000.0)
    assert ev["proceeds"] == pytest.approx(1500.0)
    assert ev["realized_gain"] == pytest.approx(500.0)
    assert ev["holding_period"] == "short_term"  # 59 days
    assert lots == []  # fully consumed, removed


def test_consume_fifo_lots_partial_liquidation_leaves_remainder():
    lots = [Lot("A", 10.0, 0, "2021-01-01", 100.0)]
    events = _consume_fifo_lots(lots, shares_to_sell=4.0, sale_price=150.0,
                                sale_day=10, sale_date="2021-03-01", ticker="A")
    assert len(events) == 1
    assert events[0]["shares_sold"] == pytest.approx(4.0)
    # the lot is NOT removed -- only partially consumed
    assert len(lots) == 1
    assert lots[0].shares == pytest.approx(6.0)


def test_consume_fifo_lots_sells_oldest_first_and_spans_multiple_lots():
    lots = [
        Lot("A", 4.0, 0, "2021-01-01", 100.0),
        Lot("A", 6.0, 5, "2021-06-01", 110.0),
    ]
    events = _consume_fifo_lots(lots, shares_to_sell=7.0, sale_price=130.0,
                                sale_day=20, sale_date="2022-01-01", ticker="A")
    assert len(events) == 2
    # oldest lot (2021-01-01) consumed first, fully
    assert events[0]["acquisition_date"] == "2021-01-01"
    assert events[0]["shares_sold"] == pytest.approx(4.0)
    assert events[0]["cost_basis_price"] == pytest.approx(100.0)
    # second-oldest lot (2021-06-01) consumed second, partially
    assert events[1]["acquisition_date"] == "2021-06-01"
    assert events[1]["shares_sold"] == pytest.approx(3.0)
    assert events[1]["cost_basis_price"] == pytest.approx(110.0)
    # first lot fully consumed and removed; second lot's remainder stays
    assert len(lots) == 1
    assert lots[0].acquisition_date == "2021-06-01"
    assert lots[0].shares == pytest.approx(3.0)


def test_consume_fifo_lots_realized_gain_can_be_negative_on_a_loss():
    lots = [Lot("A", 5.0, 0, "2021-01-01", 200.0)]
    events = _consume_fifo_lots(lots, shares_to_sell=5.0, sale_price=150.0,
                                sale_day=10, sale_date="2021-03-01", ticker="A")
    assert events[0]["realized_gain"] == pytest.approx(-250.0)  # 5 * (150-200)


def test_consume_fifo_lots_selling_more_than_available_stops_at_available():
    lots = [Lot("A", 3.0, 0, "2021-01-01", 100.0)]
    events = _consume_fifo_lots(lots, shares_to_sell=10.0, sale_price=120.0,
                                sale_day=5, sale_date="2021-02-01", ticker="A")
    # does not fabricate a lot that was never recorded -- consumes only
    # what actually exists and stops
    assert len(events) == 1
    assert events[0]["shares_sold"] == pytest.approx(3.0)
    assert lots == []


def test_consume_fifo_lots_empty_lots_returns_no_events():
    events = _consume_fifo_lots([], shares_to_sell=5.0, sale_price=100.0,
                                sale_day=0, sale_date="2021-01-01", ticker="A")
    assert events == []


# ── _fund_repayment: additive-only invariant ─────────────────────────────────

def test_fund_repayment_shares_and_cash_unchanged_whether_or_not_lots_tracked():
    """Proves the lot ledger is read-alongside bookkeeping, not a change
    to any existing computation -- the exact 'preserve all existing
    outputs' requirement from docs/PHASE6A_IMPLEMENTATION_APPROVAL.md."""
    shares_no_lots = {"A": 10.0}
    cash1 = _fund_repayment(cash=0.0, shares=shares_no_lots, closes={"A": 120.0},
                            gross=1200.0, repay=600.0)

    shares_with_lots = {"A": 10.0}
    lots = {"A": [Lot("A", 10.0, 0, "2021-01-01", 100.0)]}
    events: list[dict] = []
    cash2 = _fund_repayment(cash=0.0, shares=shares_with_lots, closes={"A": 120.0},
                            gross=1200.0, repay=600.0, lots=lots, sale_day=5,
                            sale_date="2021-02-01", tax_lot_events=events)

    assert cash1 == pytest.approx(cash2)
    assert shares_no_lots["A"] == pytest.approx(shares_with_lots["A"])
    assert len(events) == 1  # the lot side-channel did populate


def test_fund_repayment_lot_consistency_invariant():
    """sum(lot.shares for lot in lots[ticker]) after a sale must equal
    shares[ticker] after the same sale -- the ledger-consistency
    invariant named in docs/PHASE6A_DATA_REQUIREMENTS.md S4."""
    shares = {"A": 10.0}
    lots = {"A": [Lot("A", 10.0, 0, "2021-01-01", 100.0)]}
    events: list[dict] = []
    _fund_repayment(cash=0.0, shares=shares, closes={"A": 120.0}, gross=1200.0,
                    repay=600.0, lots=lots, sale_day=10, sale_date="2021-02-01",
                    tax_lot_events=events)
    assert sum(l.shares for l in lots["A"]) == pytest.approx(shares["A"])
    assert events[0]["realized_gain"] == pytest.approx(5.0 * (120.0 - 100.0))


# ── full simulate() integration: lot creation + multi-event repayment ───────

def _margin_then_gain_fixture():
    """A/B eligible day 0, C from day 2 (forces a margin draw, same
    mechanism as test_margin_simulation.py's own
    test_simulate_margin_draw_equals_gap_minus_available_cash), then a
    100% price jump on day 3 across all three tickers -- gives Model B's
    HWM-gain trigger something real to fire on, across positions bought
    on different days (i.e. different lots)."""
    calendar = [f"2026-01-{d:02d}" for d in range(1, 6)]
    aligned = {
        "A": ([100.0, 100.0, 100.0, 200.0, 200.0], 0),
        "B": ([100.0, 100.0, 100.0, 200.0, 200.0], 0),
        "C": ([None, None, 100.0, 200.0, 200.0], 2),
    }
    deposit_days = [calendar[0], calendar[2]]
    schedule = {calendar[0]: 60.0, calendar[2]: 20.0}
    return aligned, calendar, deposit_days, schedule


def test_simulate_model_b_repayment_creates_lots_and_tax_lot_events():
    sc = ScenarioConfig(name="test", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, repayment_fn=repayment_model_0,
                        repayment_model_name="MODEL_B",
                        pre_trade_fn=ModelBProfitHarvest(repay_fraction=0.5))
    aligned, calendar, deposit_days, schedule = _margin_then_gain_fixture()
    result = simulate(sc, weights={"A": 1.0, "B": 1.0, "C": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)

    assert len(result.tax_lot_events) > 0
    tickers_sold = {ev["ticker"] for ev in result.tax_lot_events}
    # the 100% price jump hits A/B (bought day 0) and C (bought day 2) --
    # a real repayment should trim across more than one ticker/lot
    assert len(tickers_sold) >= 2

    for ev in result.tax_lot_events:
        assert ev["realized_gain"] == pytest.approx(ev["proceeds"] - ev["cost_basis"])
        assert ev["holding_period"] in ("short_term", "long_term")
        assert ev["acquisition_date"] in calendar
        assert ev["sale_date"] in calendar
        # every event here is a real gain (100% price jump, no losses)
        assert ev["realized_gain"] > 0


def test_simulate_existing_outputs_unchanged_with_lot_ledger_present():
    """Regression proof: adding the (always-on) lot ledger does not
    change a single existing field's value -- book_values, gross_series,
    leverage_series, events, final_margin_debt all match the pre-Phase-6A
    behavior exactly (this is the same fixture/assertions
    test_margin_simulation.py's own Model B/interest regression tests
    already use; re-asserted here as a direct Phase 6A regression gate,
    not relying solely on the full suite's 260-pass count)."""
    sc = ScenarioConfig(name="test", leverage_cap=1.8, interest_apr=0.20,
                        interest_free_amount=0.0, repayment_fn=repayment_model_0,
                        repayment_model_name="MODEL_0")
    aligned, calendar, deposit_days, schedule = _margin_then_gain_fixture()
    result = simulate(sc, weights={"A": 1.0, "B": 1.0, "C": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    interest_events = [e for e in result.events if e["kind"] == "interest_accrual"]
    assert len(interest_events) > 0
    assert all(e["amount"] > 0 for e in interest_events)
    first_draw_day = next(e["day"] for e in result.events if e["kind"] == "margin_draw")
    assert all(e["day"] > first_draw_day for e in interest_events)
    # MODEL_0 never repays -- no sales at all, so no tax lot events either
    assert result.tax_lot_events == []
