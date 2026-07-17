"""Tests for margin_simulation.py (Phase 3B harness).

All fixtures here are small, synthetic, hand-computable price series —
deliberately NOT the real 65-ticker data/backtest/*.json cache. Phase 3B's
scope is "harness + unit tests," not "run and interpret real scenarios"
(docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md Phase 3C is where real data gets
used). Using synthetic data here keeps that boundary unambiguous — nothing
in this file could be mistaken for an actual Test A-D result.
"""

import pytest

from margin_simulation import (
    BANNED_PHRASES,
    HYPOTHETICAL_LABEL,
    PortfolioState,
    ScenarioConfig,
    _assert_no_banned_language,
    _leverage_capped_margin,
    annualized_volatility,
    cagr,
    render_metrics,
    repayment_model_0,
    repayment_model_a,
    repayment_model_b,
    repayment_model_c,
    scenario_fixed_leverage,
    scenario_leverage_sweep,
    scenario_repayment_variants,
    scenario_unlevered,
    simulate,
    time_near_leverage_cap,
    worst_case_concentration_impact,
)


# ── PortfolioState ───────────────────────────────────────────────────────────

def test_portfolio_state_net_equity_and_leverage():
    s = PortfolioState(day_index=0, cash=10.0, positions={"X": 5.0},
                       margin_debt=40.0, gross=100.0)
    assert s.net_equity == 60.0
    assert s.leverage_ratio == pytest.approx(100.0 / 60.0)
    assert s.book == 70.0  # net_equity + cash


def test_portfolio_state_zero_net_equity_leverage_is_none():
    s = PortfolioState(day_index=0, cash=0.0, positions={}, margin_debt=100.0, gross=100.0)
    assert s.net_equity == 0.0
    assert s.leverage_ratio is None


def test_portfolio_state_negative_net_equity_leverage_is_none():
    s = PortfolioState(day_index=0, cash=0.0, positions={}, margin_debt=150.0, gross=100.0)
    assert s.net_equity == -50.0
    assert s.leverage_ratio is None


# ── leverage-cap math ────────────────────────────────────────────────────────

def test_leverage_capped_margin_matches_allocate_formula_shape():
    # Same numbers as test_margin.py's test_healthy_buffer_clips_to_leverage_cap
    # for allocate.margin_capacity() -- proves the deliberately-re-derived
    # formula here produces the identical result.
    allowed = _leverage_capped_margin(gross=100.0, margin_debt=0.0, cash=0.0,
                                      leverage_cap=1.8, requested=200.0)
    assert allowed == 80.0


def test_leverage_capped_margin_already_over_cap_allows_nothing():
    allowed = _leverage_capped_margin(gross=200.0, margin_debt=100.0, cash=0.0,
                                      leverage_cap=1.8, requested=10.0)
    assert allowed == 0.0


# ── repayment models ─────────────────────────────────────────────────────────

def test_model_0_never_repays():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=1000.0, gross=2000.0)
    assert repayment_model_0(s, prior_gross=1900.0) == 0.0


def test_model_a_no_breach_no_repayment():
    # leverage = 2000/(2000-500) = 1.33x, cap 1.8x -> no breach
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=2000.0)
    assert repayment_model_a(s, prior_gross=None, leverage_cap=1.8) == 0.0


def test_model_a_breach_repays_minimum_to_clear_cap():
    # gross=1000, debt=600 -> net_equity=400, leverage=2.5x > 1.8x cap.
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=600.0, gross=1000.0)
    repay = repayment_model_a(s, prior_gross=None, leverage_cap=1.8)
    assert repay > 0
    target_debt = 1000.0 - 1000.0 / 1.8
    assert repay == pytest.approx(600.0 - target_debt)
    # verify the repayment actually clears the breach
    new_debt = 600.0 - repay
    new_leverage = 1000.0 / (1000.0 - new_debt)
    assert new_leverage <= 1.8 + 1e-9


def test_model_a_zero_debt_no_repayment():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0)
    assert repayment_model_a(s, prior_gross=None, leverage_cap=1.8) == 0.0


def test_model_b_repays_any_excess_above_target_every_day():
    # gross=1000, debt=500 -> leverage=2.0x, target=1.5x -> should repay down to 1.5x
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0)
    repay = repayment_model_b(s, prior_gross=None, target_leverage=1.5)
    assert repay > 0
    new_debt = 500.0 - repay
    assert (1000.0 / (1000.0 - new_debt)) == pytest.approx(1.5, abs=1e-6)


def test_model_b_below_target_no_repayment():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=100.0, gross=1000.0)
    # leverage = 1000/900 = 1.11x, target 1.5x -> already below target
    assert repayment_model_b(s, prior_gross=None, target_leverage=1.5) == 0.0


def test_model_c_triggers_on_gain():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=1000.0, gross=1100.0)
    repay = repayment_model_c(s, prior_gross=1000.0, gain_trigger_pct=5.0, reset_fraction=0.1)
    # (1100-1000)/1000 = 10% > 5% trigger
    assert repay == pytest.approx(100.0)  # 10% of 1000 debt


def test_model_c_no_trigger_below_gain_threshold():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=1000.0, gross=1020.0)
    repay = repayment_model_c(s, prior_gross=1000.0, gain_trigger_pct=5.0, reset_fraction=0.1)
    assert repay == 0.0


def test_model_c_triggers_on_concentration():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=1000.0, gross=1000.0)
    repay = repayment_model_c(s, prior_gross=1000.0, gain_trigger_pct=100.0,
                              reset_fraction=0.2, concentration_score=1.2,
                              concentration_trigger=1.0)
    assert repay == pytest.approx(200.0)


def test_model_c_no_debt_no_repayment_regardless_of_trigger():
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0)
    repay = repayment_model_c(s, prior_gross=500.0, gain_trigger_pct=1.0, reset_fraction=1.0)
    assert repay == 0.0


# ── metrics ──────────────────────────────────────────────────────────────────

def test_cagr_basic_doubling_over_one_year():
    assert cagr(100.0, 200.0, years=1.0) == pytest.approx(100.0)


def test_cagr_zero_start_returns_zero_not_error():
    assert cagr(0.0, 200.0, years=1.0) == 0.0


def test_annualized_volatility_zero_for_constant_series():
    vals = [100.0] * 10
    assert annualized_volatility(vals, {}) == 0.0


def test_annualized_volatility_positive_for_varying_series():
    vals = [100.0, 105.0, 98.0, 110.0, 95.0, 108.0]
    assert annualized_volatility(vals, {}) > 0.0


def test_time_near_leverage_cap_all_days_near():
    series = [1.75, 1.76, 1.79]
    assert time_near_leverage_cap(series, leverage_cap=1.8, near_cap_fraction=0.9) == 100.0


def test_time_near_leverage_cap_no_days_near():
    series = [1.0, 1.1, 1.2]
    assert time_near_leverage_cap(series, leverage_cap=1.8, near_cap_fraction=0.9) == 0.0


def test_time_near_leverage_cap_ignores_none_entries():
    series = [None, 1.75, None, 1.0]
    # 1 of 2 valid entries (1.75) is near cap (0.9*1.8=1.62)
    assert time_near_leverage_cap(series, leverage_cap=1.8, near_cap_fraction=0.9) == 50.0


def test_time_near_leverage_cap_empty_series_is_zero():
    assert time_near_leverage_cap([], leverage_cap=1.8) == 0.0


def test_worst_case_concentration_impact_scales_with_leverage():
    unlevered = worst_case_concentration_impact(
        position_weight_pct=20.0, position_max_drawdown_pct=-50.0, leverage_ratio=1.0)
    levered = worst_case_concentration_impact(
        position_weight_pct=20.0, position_max_drawdown_pct=-50.0, leverage_ratio=2.0)
    assert levered == pytest.approx(unlevered * 2.0)
    assert unlevered == pytest.approx(10.0)  # 20% * 50% * 1.0


def test_worst_case_concentration_impact_none_leverage_treated_as_unlevered():
    a = worst_case_concentration_impact(20.0, -50.0, leverage_ratio=None)
    b = worst_case_concentration_impact(20.0, -50.0, leverage_ratio=1.0)
    assert a == pytest.approx(b)


# ── output-language enforcement ─────────────────────────────────────────────

def test_banned_phrases_are_actually_banned():
    for phrase in BANNED_PHRASES:
        with pytest.raises(ValueError):
            _assert_no_banned_language(f"Report: {phrase} 12%.")


def test_clean_text_passes():
    _assert_no_banned_language("Under these assumptions, a simulated investor "
                               "would have experienced a 12% return.")


def test_render_metrics_includes_hypothetical_label():
    out = render_metrics({"ann_twr_pct": 12.3}, {"leverage_cap": 1.8})
    assert HYPOTHETICAL_LABEL in out
    assert "ann_twr_pct" in out


def test_render_metrics_raises_if_scenario_name_contains_banned_phrase():
    with pytest.raises(ValueError):
        render_metrics({"scenario": "margin would have made 5%"}, {})


# ── scenario builders ────────────────────────────────────────────────────────

def test_scenario_unlevered_has_leverage_cap_one():
    sc = scenario_unlevered()
    assert sc.leverage_cap == 1.0
    assert sc.repayment_model_name == "MODEL_0"


def test_scenario_fixed_leverage_preserves_cap():
    sc = scenario_fixed_leverage(1.8, interest_apr=0.05, interest_free_amount=1000.0)
    assert sc.leverage_cap == 1.8
    assert sc.interest_apr == 0.05


def test_scenario_leverage_sweep_produces_one_per_level():
    levels = [1.2, 1.5, 1.8, 2.0]
    scs = scenario_leverage_sweep(levels, interest_apr=0.05, interest_free_amount=1000.0)
    assert [s.leverage_cap for s in scs] == levels


def test_scenario_repayment_variants_includes_model_0_control_plus_requested():
    scs = scenario_repayment_variants(
        leverage_cap=1.8, interest_apr=0.05, interest_free_amount=1000.0,
        model_a_cfg={}, model_b_cfg={"target_leverage": 1.5},
        model_c_cfg={"gain_trigger_pct": 5.0, "reset_fraction": 0.1})
    names = [s.repayment_model_name for s in scs]
    assert names == ["MODEL_0", "MODEL_A", "MODEL_B", "MODEL_C"]


def test_scenario_repayment_variants_skips_unconfigured_models():
    scs = scenario_repayment_variants(
        leverage_cap=1.8, interest_apr=0.0, interest_free_amount=0.0)
    assert [s.repayment_model_name for s in scs] == ["MODEL_0"]


# ── simulate() end-to-end on synthetic data ─────────────────────────────────

def _flat_aligned(tickers, price=100.0, days=10):
    return {t: ([price] * days, 0) for t in tickers}


def test_simulate_unlevered_never_draws_margin():
    sc = scenario_unlevered()
    aligned = _flat_aligned(["A", "B"], price=100.0, days=5)
    calendar = [f"2026-01-{d:02d}" for d in range(1, 6)]
    result = simulate(sc, weights={"A": 1.0, "B": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=[calendar[0]],
                      deposit_amount=1000.0, min_lot=1.0)
    assert result.final_margin_debt == 0.0
    assert result.label == HYPOTHETICAL_LABEL
    assert all(lv is None or lv <= 1.0 + 1e-9 for lv in result.leverage_series)


def test_simulate_margin_draw_equals_gap_minus_available_cash():
    # Day 0: $60 fully funds A/B 50/50 from cash alone (book == cash, no
    # existing gross yet, so no margin is possible to need).
    # Day 2: C becomes eligible. gross going in = 60 (0.3 sh each of A/B
    # @ $100). deposit +$20 cash -> net_equity=60, cash=20, book=80.
    # 3-way equal-weight target = 80/3 = 26.667 each; A/B are already
    # slightly overweight (30 > 26.667, skipped, not sold), so only C's
    # full $26.667 target must be bought. $20 of that comes from cash,
    # the remaining $6.667 must come from margin (leverage_cap=1.8 leaves
    # ample room: buying_power = 20 + (1.8*(60+20)-60-20) = 20+64 = 84).
    sc = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    aligned = {
        "A": ([100.0] * 3, 0),
        "B": ([100.0] * 3, 0),
        "C": ([100.0] * 3, 2),
    }
    calendar = ["2026-01-01", "2026-01-02", "2026-01-03"]

    # Day 0 only: fund A/B 50/50 from $60 cash (no margin possible yet to need).
    day0 = simulate(sc, weights={"A": 1.0, "B": 1.0}, aligned={
        "A": ([100.0], 0), "B": ([100.0], 0)}, calendar=[calendar[0]],
        deposit_days=[calendar[0]], deposit_amount=60.0, min_lot=1.0)
    assert day0.final_margin_debt == 0.0

    # Full 3-day run: day2 introduces C with only $20 new cash -> forces margin.
    full = simulate(sc, weights={"A": 1.0, "B": 1.0, "C": 1.0}, aligned=aligned,
                    calendar=calendar, deposit_days=[calendar[0], calendar[2]],
                    deposit_amount=None, min_lot=1.0,
                    deposit_schedule={calendar[0]: 60.0, calendar[2]: 20.0})
    assert full.final_margin_debt == pytest.approx(20.0 / 3.0, abs=0.01)


def test_simulate_rising_prices_produce_positive_twr():
    sc = scenario_unlevered()
    aligned = {"A": ([100.0, 110.0, 121.0, 133.1], 0)}
    calendar = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
    result = simulate(sc, weights={"A": 1.0}, aligned=aligned, calendar=calendar,
                      deposit_days=[calendar[0]], deposit_amount=1000.0, min_lot=1.0)
    m = result.metrics()
    assert m["ann_twr_pct"] > 0
    assert m["label"] == HYPOTHETICAL_LABEL


def _margin_then_gain_fixture():
    """A/B eligible from day 0, C from day 2 (forces a $40 margin draw on
    day 2, same mechanism as test_simulate_margin_draw_equals_gap_minus_
    available_cash), then a 100% price jump on day 3 across all three
    tickers -- gives repayment Model C's gain trigger something real to
    fire on, and gives interest something real to accrue against."""
    calendar = [f"2026-01-{d:02d}" for d in range(1, 6)]  # 5 days
    aligned = {
        "A": ([100.0, 100.0, 100.0, 200.0, 200.0], 0),
        "B": ([100.0, 100.0, 100.0, 200.0, 200.0], 0),
        "C": ([None, None, 100.0, 200.0, 200.0], 2),
    }
    deposit_days = [calendar[0], calendar[2]]
    schedule = {calendar[0]: 60.0, calendar[2]: 20.0}
    return aligned, calendar, deposit_days, schedule


def test_simulate_interest_accrues_on_debt_above_free_amount():
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    aligned, calendar, deposit_days, schedule = _margin_then_gain_fixture()
    result = simulate(sc, weights={"A": 1.0, "B": 1.0, "C": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    interest_events = [e for e in result.events if e["kind"] == "interest_accrual"]
    assert len(interest_events) > 0
    assert all(e["amount"] > 0 for e in interest_events)
    # interest can only start accruing on the day AFTER margin_debt first
    # becomes positive (interest is charged on the debt balance entering
    # the day, not on debt drawn that same day)
    first_draw_day = next(e["day"] for e in result.events if e["kind"] == "margin_draw")
    assert all(e["day"] > first_draw_day for e in interest_events)


def test_simulate_repayment_model_reduces_final_debt_vs_model_0():
    aligned, calendar, deposit_days, schedule = _margin_then_gain_fixture()
    weights = {"A": 1.0, "B": 1.0, "C": 1.0}

    sc_control = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    result_control = simulate(sc_control, weights=weights, aligned=aligned,
                              calendar=calendar, deposit_days=deposit_days,
                              deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result_control.final_margin_debt > 0  # sanity: fixture actually draws margin

    scs = scenario_repayment_variants(
        leverage_cap=1.8, interest_apr=0.0, interest_free_amount=0.0,
        model_c_cfg={"gain_trigger_pct": 10.0, "reset_fraction": 0.5})
    sc_c = next(s for s in scs if s.repayment_model_name == "MODEL_C")
    result_c = simulate(sc_c, weights=weights, aligned=aligned, calendar=calendar,
                        deposit_days=deposit_days, deposit_amount=None, min_lot=1.0,
                        deposit_schedule=schedule)

    assert result_c.final_margin_debt < result_control.final_margin_debt


def test_simulate_result_metrics_never_produces_banned_language():
    sc = scenario_fixed_leverage(1.8, interest_apr=0.05, interest_free_amount=1000.0)
    aligned = {"A": ([100.0, 105.0, 95.0, 115.0], 0)}
    calendar = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
    result = simulate(sc, weights={"A": 1.0}, aligned=aligned, calendar=calendar,
                      deposit_days=[calendar[0]], deposit_amount=500.0, min_lot=1.0)
    text = render_metrics(result.metrics(), assumptions={"leverage_cap": sc.leverage_cap})
    _assert_no_banned_language(text)  # should not raise
    assert HYPOTHETICAL_LABEL in text


def test_module_source_never_imports_allocate_or_margin_state():
    import ast
    import margin_simulation
    tree = ast.parse(open(margin_simulation.__file__).read())
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
    assert "allocate" not in imported_modules
    assert "margin_state" not in imported_modules


def test_module_has_no_yaml_config_io():
    # No open()/yaml.safe_load() of targets.yaml or holdings.yaml anywhere
    # in this module -- it consumes only in-memory weights/aligned-price
    # dicts passed in by the caller (see load_real_aligned_data(), which
    # delegates all such I/O to backtest_regime.py, not this module).
    import margin_simulation
    src = open(margin_simulation.__file__).read()
    assert "yaml.safe_load" not in src
    assert "open(HERE" not in src
