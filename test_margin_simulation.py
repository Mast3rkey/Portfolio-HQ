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
    ModelBProfitHarvest,
    ModelCRiskReset,
    PortfolioState,
    RepaymentDecision,
    ScenarioConfig,
    _assert_no_banned_language,
    _leverage_capped_margin,
    annualized_volatility,
    cagr,
    render_metrics,
    repayment_model_0,
    repayment_model_a,
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


# ── Model B — Profit Harvest (stateful, finalized mechanics) ───────────────
# docs/PHASE3_SCENARIO_MANIFEST.md §1/§2: trigger on a new net-equity HWM,
# repay repay_fraction (default 0.25) of the fresh gain, never borrow.

def test_model_b_first_call_establishes_hwm_no_repayment():
    policy = ModelBProfitHarvest(repay_fraction=0.25)
    s = PortfolioState(0, cash=0.0, positions={}, margin_debt=100.0, gross=1000.0)
    decision = policy(s, prior_gross=None)
    assert decision.repay_amount == 0.0
    assert decision.effective_leverage_cap is None
    assert policy._hwm == pytest.approx(900.0)  # net_equity = 1000-100


def test_model_b_repays_fraction_of_gain_above_hwm():
    policy = ModelBProfitHarvest(repay_fraction=0.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=100.0, gross=1000.0)
    policy(s1, prior_gross=None)  # hwm = 900

    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=100.0, gross=1100.0)
    decision = policy(s2, prior_gross=None)  # net_equity = 1000, gain = 100
    assert decision.repay_amount == pytest.approx(25.0)  # 25% of 100
    assert decision.effective_leverage_cap is None  # never tightens/loosens the cap
    assert policy._hwm == pytest.approx(1000.0)


def test_model_b_no_new_high_no_repayment():
    policy = ModelBProfitHarvest(repay_fraction=0.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0)
    policy(s1, prior_gross=None)  # hwm = 1000

    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=0.0, gross=950.0)
    decision = policy(s2, prior_gross=None)
    assert decision.repay_amount == 0.0


def test_model_b_never_repays_more_than_current_debt():
    policy = ModelBProfitHarvest(repay_fraction=1.0)  # repay 100% of any gain
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=10.0, gross=1000.0)
    policy(s1, prior_gross=None)  # hwm = 990

    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=10.0, gross=1500.0)
    decision = policy(s2, prior_gross=None)  # gain = 500, 100% = 500, but debt is only 10
    assert decision.repay_amount == pytest.approx(10.0)


def test_model_b_invalid_repay_fraction_raises():
    with pytest.raises(ValueError):
        ModelBProfitHarvest(repay_fraction=1.5)
    with pytest.raises(ValueError):
        ModelBProfitHarvest(repay_fraction=-0.1)


def test_model_b_fresh_instance_per_run_no_state_leak():
    # Reusing one instance across two separate "runs" would leak the HWM
    # from the first run into the second -- this proves a FRESH instance
    # starts clean, which is the documented contract (module docstring).
    run1 = ModelBProfitHarvest(repay_fraction=0.25)
    run1(PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0), None)
    run1(PortfolioState(1, cash=0.0, positions={}, margin_debt=0.0, gross=2000.0), None)
    assert run1._hwm == pytest.approx(2000.0)

    run2 = ModelBProfitHarvest(repay_fraction=0.25)
    decision = run2(PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0), None)
    assert run2._hwm == pytest.approx(1000.0)  # not 2000 -- no leakage from run1
    assert decision.repay_amount == 0.0  # first call, HWM-establishing, never repays


# ── Model C — Risk Reset (stateful, finalized mechanics) ───────────────────
# docs/PHASE3_SCENARIO_MANIFEST.md §1/§2: trigger on a 15% net-equity
# drawdown from peak, deleverage to 1.25x, restore only on a NEW high AND
# leverage normalized.

def test_model_c_no_trigger_below_drawdown_threshold():
    policy = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0)
    policy(s1, None)  # hwm = 1000
    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=0.0, gross=900.0)  # -10%
    decision = policy(s2, None)
    assert decision.repay_amount == 0.0
    assert decision.effective_leverage_cap is None
    assert policy.reset_active is False


def test_model_c_triggers_and_hits_exact_target_leverage_when_trim_funded():
    # gross=1000, debt=500 -> net_equity=500 (hwm). Then gross drops to
    # 700 (>15% net_equity drawdown: net_equity would be 200, an 60% drop)
    # -- leverage before reset = 700/200 = 3.5x, well above the 1.25x
    # target. Verifies the trim-funded-exact formula (module comment on
    # ModelCRiskReset.__call__): repay = gross - reset_leverage*net_equity.
    policy = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0)
    policy(s1, None)  # hwm = 500

    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0)
    decision = policy(s2, None)
    assert policy.reset_active is True
    expected_repay = 700.0 - 1.25 * 200.0  # gross - reset_leverage*net_equity
    assert decision.repay_amount == pytest.approx(expected_repay)
    assert decision.effective_leverage_cap == pytest.approx(1.25)

    # simulate the trim-funded paydown by hand: gross and debt both drop
    # by repay_amount (see the "no idle cash" funding path), net_equity
    # is invariant to that trim -- confirms the resulting leverage is
    # EXACTLY 1.25x, not merely "reduced."
    new_gross = 700.0 - decision.repay_amount
    new_debt = 500.0 - decision.repay_amount
    assert new_gross / (new_gross - new_debt) == pytest.approx(1.25, abs=1e-9)


def test_model_c_no_repay_needed_if_already_under_target_after_crash():
    # A severe crash can push leverage BELOW the reset target even before
    # any repayment (gross falls faster than debt, but debt is small
    # enough relative to gross that leverage doesn't spike) -- reset still
    # activates (drawdown trigger fired) and tightens the cap, but there
    # is nothing to repay.
    policy = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=6.0, gross=200.0)
    policy(s1, None)  # hwm = 194

    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=6.0, gross=52.0)  # net_equity=46, drawdown 76%
    decision = policy(s2, None)
    assert policy.reset_active is True
    # leverage = 52/46 = 1.13x, already below 1.25 -> nothing to repay
    assert decision.repay_amount == 0.0
    assert decision.effective_leverage_cap == pytest.approx(1.25)


def test_model_c_fires_once_per_drawdown_episode_not_every_day_below():
    policy = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0)
    policy(s1, None)  # hwm = 500
    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0)
    d2 = policy(s2, None)
    assert d2.repay_amount > 0  # the actual reset trim happens once, here

    # still deep in drawdown the next day -- must NOT repay again
    s3 = PortfolioState(2, cash=0.0, positions={}, margin_debt=500.0 - d2.repay_amount,
                        gross=700.0 - d2.repay_amount)
    d3 = policy(s3, None)
    assert d3.repay_amount == 0.0
    assert d3.effective_leverage_cap == pytest.approx(1.25)  # cap stays tightened


def test_model_c_restoration_requires_both_new_high_and_normalized_leverage():
    policy = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    s1 = PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0)
    policy(s1, None)  # hwm = 500 = pre_drawdown_hwm once triggered
    s2 = PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0)
    policy(s2, None)  # triggers, reset_active=True

    # Case 1: leverage normalized but NOT a new high -> stays active
    s3 = PortfolioState(2, cash=0.0, positions={}, margin_debt=100.0, gross=350.0)  # ne=250 < 500 hwm, lev=1.4
    d3 = policy(s3, None)
    assert policy.reset_active is True
    assert d3.effective_leverage_cap == pytest.approx(1.25)

    # Case 2: new high but leverage NOT normalized -> stays active
    s4 = PortfolioState(3, cash=0.0, positions={}, margin_debt=400.0, gross=1000.0)  # ne=600 > 500 hwm, lev=1.667
    d4 = policy(s4, None)
    assert policy.reset_active is True
    assert d4.effective_leverage_cap == pytest.approx(1.25)

    # Case 3: BOTH conditions met -> restores
    s5 = PortfolioState(4, cash=0.0, positions={}, margin_debt=100.0, gross=700.0)  # ne=600 > 500 hwm, lev=1.167
    d5 = policy(s5, None)
    assert policy.reset_active is False
    assert d5.effective_leverage_cap is None


def test_model_c_invalid_params_raise():
    with pytest.raises(ValueError):
        ModelCRiskReset(drawdown_trigger_pct=0.0)
    with pytest.raises(ValueError):
        ModelCRiskReset(drawdown_trigger_pct=150.0)
    with pytest.raises(ValueError):
        ModelCRiskReset(reset_leverage=0.5)


def test_model_c_fresh_instance_per_run_no_state_leak():
    run1 = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    run1(PortfolioState(0, cash=0.0, positions={}, margin_debt=500.0, gross=1000.0), None)
    run1(PortfolioState(1, cash=0.0, positions={}, margin_debt=500.0, gross=700.0), None)
    assert run1.reset_active is True

    run2 = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=1.25)
    d = run2(PortfolioState(0, cash=0.0, positions={}, margin_debt=0.0, gross=1000.0), None)
    assert run2.reset_active is False  # not leaked from run1
    assert d.repay_amount == 0.0


# ── Property test: leverage can never increase during a Model C reset ─────
# The single required guarantee named explicitly in the task: "no dip-
# buying interpretation." Proven structurally, not just asserted for one
# fixture -- sweeps a grid of gross/debt/drawdown combinations and checks
# the invariant holds in every one.

def test_model_c_effective_leverage_cap_never_exceeds_reset_leverage_while_active():
    reset_leverage = 1.25
    policy = ModelCRiskReset(drawdown_trigger_pct=15.0, reset_leverage=reset_leverage)
    grosses = [100.0, 500.0, 1000.0, 5000.0]
    debts = [0.0, 10.0, 100.0, 500.0, 900.0]
    n_checked = 0
    for gross in grosses:
        for debt in debts:
            if debt >= gross:
                continue
            state = PortfolioState(0, cash=0.0, positions={}, margin_debt=debt, gross=gross)
            decision = policy(state, None)
            n_checked += 1
            if policy.reset_active:
                assert decision.effective_leverage_cap is not None
                assert decision.effective_leverage_cap <= reset_leverage + 1e-9
    assert n_checked > 0


def test_simulate_never_lets_effective_cap_exceed_scenario_cap_regardless_of_policy():
    # Structural guarantee enforced in simulate() itself (not trusted
    # per-policy): even a policy that requested a LOOSER cap than the
    # scenario's own could never actually get it. A fake policy here
    # deliberately tries to loosen (requests cap=99.0, far above any
    # scenario.leverage_cap) to prove simulate() clamps it regardless.
    class LooseningAttemptPolicy:
        def __call__(self, state, prior_gross):
            return RepaymentDecision(repay_amount=0.0, effective_leverage_cap=99.0)

    sc = ScenarioConfig(name="test", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, repayment_fn=repayment_model_0,
                        repayment_model_name="MODEL_0", pre_trade_fn=LooseningAttemptPolicy())
    aligned = {
        "A": ([100.0] * 3, 0),
        "B": ([100.0] * 3, 0),
        "C": ([100.0] * 3, 2),
    }
    calendar = ["2026-01-01", "2026-01-02", "2026-01-03"]
    result = simulate(sc, weights={"A": 1.0, "B": 1.0, "C": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=[calendar[0], calendar[2]],
                      deposit_amount=None, min_lot=1.0,
                      deposit_schedule={calendar[0]: 60.0, calendar[2]: 20.0})
    # leverage never exceeds the scenario's own 1.8x cap, despite the
    # policy's attempt to loosen it to 99.0
    assert all(lv is None or lv <= 1.8 + 1e-6 for lv in result.leverage_series)


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
        model_a_cfg={}, model_b_cfg={"repay_fraction": 0.25},
        model_c_cfg={"drawdown_trigger_pct": 15.0, "reset_leverage": 1.25})
    names = [s.repayment_model_name for s in scs]
    assert names == ["MODEL_0", "MODEL_A", "MODEL_B", "MODEL_C"]
    b_scenario = next(s for s in scs if s.repayment_model_name == "MODEL_B")
    c_scenario = next(s for s in scs if s.repayment_model_name == "MODEL_C")
    assert isinstance(b_scenario.pre_trade_fn, ModelBProfitHarvest)
    assert isinstance(c_scenario.pre_trade_fn, ModelCRiskReset)
    # Model 0/A variants use the old post-allocation repayment_fn slot,
    # not the new pre_trade_fn hook -- unchanged plumbing.
    zero_scenario = next(s for s in scs if s.repayment_model_name == "MODEL_0")
    a_scenario = next(s for s in scs if s.repayment_model_name == "MODEL_A")
    assert zero_scenario.pre_trade_fn is None
    assert a_scenario.pre_trade_fn is None


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


def _margin_then_crash_fixture():
    """A eligible from day 0, B from day 2 (forces a $245 margin draw on
    day 2, same delayed-eligibility mechanism as
    test_simulate_margin_draw_equals_gap_minus_available_cash), then a 5x
    price jump on day 2 followed by a 25% crash on day 3 -- gives Model
    C's drawdown trigger something real to fire on (net-equity drawdown
    from the day-2 peak comfortably exceeds 15%), while leverage stays
    meaningfully above the 1.25x reset target at the moment it fires
    (verified via a standalone probe before this fixture was written)."""
    common = [100.0, 100.0, 500.0, 375.0, 375.0]
    aligned = {"A": (common, 0), "B": (common, 2)}
    calendar = [f"2026-01-{d:02d}" for d in range(1, 6)]
    deposit_days = [calendar[0], calendar[2]]
    schedule = {calendar[0]: 100.0, calendar[2]: 10.0}
    return aligned, calendar, deposit_days, schedule


def test_simulate_repayment_model_c_reduces_final_debt_vs_model_0():
    aligned, calendar, deposit_days, schedule = _margin_then_crash_fixture()
    weights = {"A": 1.0, "B": 1.0}

    sc_control = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    result_control = simulate(sc_control, weights=weights, aligned=aligned,
                              calendar=calendar, deposit_days=deposit_days,
                              deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result_control.final_margin_debt == pytest.approx(245.0)  # sanity: matches the probe

    scs = scenario_repayment_variants(
        leverage_cap=1.8, interest_apr=0.0, interest_free_amount=0.0,
        model_c_cfg={"drawdown_trigger_pct": 15.0, "reset_leverage": 1.25})
    sc_c = next(s for s in scs if s.repayment_model_name == "MODEL_C")
    result_c = simulate(sc_c, weights=weights, aligned=aligned, calendar=calendar,
                        deposit_days=deposit_days, deposit_amount=None, min_lot=1.0,
                        deposit_schedule=schedule)

    assert result_c.final_margin_debt < result_control.final_margin_debt
    assert result_c.final_margin_debt == pytest.approx(80.3125)  # exact value from the probe
    # leverage hits exactly the 1.25x reset target once the trim-funded
    # paydown completes (day 3 onward)
    assert result_c.leverage_series[3] == pytest.approx(1.25)
    assert result_c.leverage_series[4] == pytest.approx(1.25)


def test_simulate_repayment_model_b_reduces_debt_on_new_highs():
    # Reuse the delayed-eligibility margin-draw fixture (100->200 rise,
    # no crash) -- a pure rally, ideal for exercising Model B's HWM-gain
    # trigger without Model C's drawdown mechanics ever engaging.
    aligned, calendar, deposit_days, schedule = _margin_then_gain_fixture()
    weights = {"A": 1.0, "B": 1.0, "C": 1.0}

    sc_control = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    result_control = simulate(sc_control, weights=weights, aligned=aligned,
                              calendar=calendar, deposit_days=deposit_days,
                              deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result_control.final_margin_debt > 0  # sanity: fixture actually draws margin

    scs = scenario_repayment_variants(
        leverage_cap=1.8, interest_apr=0.0, interest_free_amount=0.0,
        model_b_cfg={"repay_fraction": 0.5})
    sc_b = next(s for s in scs if s.repayment_model_name == "MODEL_B")
    result_b = simulate(sc_b, weights=weights, aligned=aligned, calendar=calendar,
                        deposit_days=deposit_days, deposit_amount=None, min_lot=1.0,
                        deposit_schedule=schedule)

    assert result_b.final_margin_debt < result_control.final_margin_debt
    repay_events = [e for e in result_b.events if e["kind"] == "repayment"]
    assert len(repay_events) > 0
    assert all(e["source"] == "pre_trade" for e in repay_events)


# ── Regression: A/B/C unchanged after the Phase 3D stateful-policy refactor ─
# Exact numeric snapshots captured from margin_simulation.py BEFORE the
# Phase 3D refactor (ModelBProfitHarvest/ModelCRiskReset, the pre_trade_fn
# hook, _fund_repayment extraction), using this exact fixture. Model 0/A
# and the shared simulate() plumbing were not supposed to change behavior
# for scenarios that never set pre_trade_fn (A/B/C all use Model 0) --
# these tests prove that, to the last cent, rather than just asserting
# "still runs without error."

def _regression_fixture():
    aligned = {
        "A": ([100.0, 100.0, 100.0, 200.0, 200.0], 0),
        "B": ([100.0, 100.0, 100.0, 200.0, 200.0], 0),
        "C": ([None, None, 100.0, 200.0, 200.0], 2),
    }
    calendar = [f"2026-01-{d:02d}" for d in range(1, 6)]
    deposit_days = [calendar[0], calendar[2]]
    schedule = {calendar[0]: 60.0, calendar[2]: 20.0}
    weights = {"A": 1.0, "B": 1.0, "C": 1.0}
    return aligned, calendar, deposit_days, schedule, weights


def test_regression_scenario_unlevered_unchanged():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_unlevered()
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.final_margin_debt == pytest.approx(0.0)
    assert result.metrics()["final_book_value"] == pytest.approx(160.0)
    assert sc.pre_trade_fn is None  # scenario_unlevered() never sets one


def test_regression_scenario_fixed_leverage_unchanged():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.final_margin_debt == pytest.approx(6.673974604366053)
    assert result.metrics()["final_book_value"] == pytest.approx(166.65935872896728)
    assert sc.pre_trade_fn is None


def test_regression_scenario_leverage_sweep_unchanged():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    expected = {
        1.2: (6.673974604366049, 166.6593587289673),
        1.8: (6.673974604366053, 166.65935872896728),
        2.0: (6.673974604366053, 166.65935872896728),
    }
    scs = scenario_leverage_sweep(list(expected), interest_apr=0.20, interest_free_amount=0.0)
    assert len(scs) == len(expected)
    for sc in scs:
        assert sc.pre_trade_fn is None
        result = simulate(sc, weights, aligned, calendar, deposit_days,
                          deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
        exp_debt, exp_book = expected[sc.leverage_cap]
        assert result.final_margin_debt == pytest.approx(exp_debt)
        assert result.metrics()["final_book_value"] == pytest.approx(exp_book)


# ── track_tickers (Phase 4A addition) ───────────────────────────────────────

def test_simulate_default_track_tickers_is_empty_and_behavior_unchanged():
    # track_tickers omitted entirely -- must be byte-for-byte identical to
    # every prior test's behavior (regression proof for the Phase 4A addition).
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.tracked_values == {}
    assert result.final_margin_debt == pytest.approx(6.673974604366053)


def test_simulate_track_tickers_records_daily_dollar_value():
    aligned = {"A": ([100.0, 200.0, 300.0], 0), "B": ([100.0, 100.0, 100.0], 0)}
    calendar = ["2026-01-01", "2026-01-02", "2026-01-03"]
    sc = scenario_unlevered()
    result = simulate(sc, weights={"A": 1.0, "B": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=[calendar[0]],
                      deposit_amount=200.0, min_lot=1.0, track_tickers=["A"])
    assert list(result.tracked_values.keys()) == ["A"]
    assert len(result.tracked_values["A"]) == 3
    # day0: A bought at $100 with half the $200 deposit -> 1.0 share -> $100
    assert result.tracked_values["A"][0] == pytest.approx(100.0)
    # day1: price doubles to $200, still 1.0 share -> $200
    assert result.tracked_values["A"][1] == pytest.approx(200.0)
    # day2: price to $300 -> $300
    assert result.tracked_values["A"][2] == pytest.approx(300.0)


def test_simulate_track_tickers_untracked_ticker_not_included():
    aligned = {"A": ([100.0], 0), "B": ([100.0], 0)}
    calendar = ["2026-01-01"]
    sc = scenario_unlevered()
    result = simulate(sc, weights={"A": 1.0, "B": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=[calendar[0]],
                      deposit_amount=200.0, min_lot=1.0, track_tickers=["A"])
    assert "B" not in result.tracked_values


def test_simulate_track_tickers_zero_before_eligible():
    aligned = {"A": ([100.0, 100.0], 0), "C": ([None, 100.0], 1)}
    calendar = ["2026-01-01", "2026-01-02"]
    sc = scenario_unlevered()
    result = simulate(sc, weights={"A": 1.0, "C": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=[calendar[0]],
                      deposit_amount=100.0, min_lot=1.0, track_tickers=["C"])
    assert result.tracked_values["C"][0] == 0.0  # not eligible yet, no shares


def test_simulate_track_multiple_tickers_sums_independently():
    aligned = {"A": ([100.0], 0), "B": ([100.0], 0)}
    calendar = ["2026-01-01"]
    sc = scenario_unlevered()
    result = simulate(sc, weights={"A": 1.0, "B": 1.0}, aligned=aligned,
                      calendar=calendar, deposit_days=[calendar[0]],
                      deposit_amount=200.0, min_lot=1.0, track_tickers=["A", "B"])
    assert set(result.tracked_values.keys()) == {"A", "B"}
    assert result.tracked_values["A"][0] == pytest.approx(100.0)
    assert result.tracked_values["B"][0] == pytest.approx(100.0)


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
