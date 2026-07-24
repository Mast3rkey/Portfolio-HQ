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


# ═════════════════════════════════════════════════════════════════════════════
# MARGIN-0005 G2A — additive engine capabilities (charter §4; PROTOCOL_V2 §13).
# Everything below tests the G2A additions and their output-neutrality. These
# are G2 engine-integrity tests on synthetic data — NOT registered Study A/B/C
# trials; no trial_ledger.jsonl exists or is created, and zero of the 300
# registered configurations are consumed by anything in this file.
# ═════════════════════════════════════════════════════════════════════════════

import ast as _ast
import hashlib as _hashlib
import inspect as _inspect
import json as _json
import os as _os

from margin_simulation import (
    LEVERAGE_TARGET_HARD_MAX,
    LEVERAGE_TARGET_HARD_MIN,
    LiquidationConfig,
    _rate_for_date,
)

_RESEARCH_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                              "research", "margin_target_study")


# ── output neutrality when every new input is absent ────────────────────────

def test_g2a_output_neutrality_legacy_fields_unchanged_when_new_inputs_absent():
    # The exact pinned pre-G2A regression values (test_regression_scenario_
    # fixed_leverage_unchanged) must still hold with no new input supplied,
    # and the new daily-path outputs must exist without altering them.
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.final_margin_debt == pytest.approx(6.673974604366053)
    assert result.metrics()["final_book_value"] == pytest.approx(166.65935872896728)
    # new series populated, correct lengths, inert values
    n = len(calendar)
    assert len(result.debt_series) == n
    assert len(result.cash_series) == n
    assert len(result.interest_series) == n
    assert result.debt_series[-1] == pytest.approx(result.final_margin_debt)
    assert result.maintenance_excess_series == [None] * n
    assert result.dividend_credit_series == [0.0] * n
    assert result.corporate_action_credit_series == [0.0] * n
    assert result.liquidation_events == []
    # no new event kinds appear without new inputs
    kinds = {e["kind"] for e in result.events}
    assert kinds <= {"deposit", "margin_draw", "interest_accrual", "repayment"}


def test_g2a_explicit_none_inputs_identical_to_omitted():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    a = simulate(sc, weights, aligned, calendar, deposit_days,
                 deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    b = simulate(sc, weights, aligned, calendar, deposit_days,
                 deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                 daily_rates=None, dividend_events=None, corporate_action_events=None)
    assert a.book_values == b.book_values
    assert a.events == b.events
    assert a.final_margin_debt == b.final_margin_debt


# ── variable-rate daily accrual (point-in-time step function) ───────────────

def _levered_flat_fixture():
    """A eligible day 0, B day 2 -- forces a margin draw on day 2 (same
    delayed-eligibility mechanism as the pre-existing fixtures), flat
    prices so interest arithmetic is hand-computable."""
    aligned = {"A": ([100.0] * 5, 0), "B": ([100.0] * 5, 2)}
    calendar = [f"2026-02-{d:02d}" for d in range(1, 6)]
    deposit_days = [calendar[0], calendar[2]]
    schedule = {calendar[0]: 60.0, calendar[2]: 20.0}
    weights = {"A": 1.0, "B": 1.0}
    return aligned, calendar, deposit_days, schedule, weights


def test_g2a_daily_rates_step_function_accrual():
    aligned, calendar, deposit_days, schedule, weights = _levered_flat_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    # rate 36.5%/yr from day 0, stepping to 73%/yr on day 4 -> daily rates
    # of exactly 0.1% then 0.2% of the debt entering the day
    rates = {calendar[0]: 0.365, calendar[4]: 0.730}
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      daily_rates=rates)
    draw = next(e for e in result.events if e["kind"] == "margin_draw")
    debt0 = draw["amount"]
    assert debt0 > 0
    ints = [e for e in result.events if e["kind"] == "interest_accrual"]
    # debt drawn on day 2 -> accrual on days 3 and 4 only
    assert [e["day"] for e in ints] == [3, 4]
    assert ints[0]["amount"] == pytest.approx(debt0 * 0.365 / 365.0)
    debt_after_day3 = debt0 + ints[0]["amount"]
    assert ints[1]["amount"] == pytest.approx(debt_after_day3 * 0.730 / 365.0)
    # interest_series mirrors the events
    assert result.interest_series[3] == pytest.approx(ints[0]["amount"])
    assert result.interest_series[4] == pytest.approx(ints[1]["amount"])


def test_g2a_daily_rates_constant_equals_flat_apr():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc_flat = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    flat = simulate(sc_flat, weights, aligned, calendar, deposit_days,
                    deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    sc_zero = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    varied = simulate(sc_zero, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      daily_rates={calendar[0]: 0.20})
    assert varied.final_margin_debt == pytest.approx(flat.final_margin_debt)
    assert varied.book_values == pytest.approx(flat.book_values)


def test_g2a_daily_rates_no_lookahead_future_rate_change_cannot_affect_past():
    aligned, calendar, deposit_days, schedule, weights = _levered_flat_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    base = simulate(sc, weights, aligned, calendar, deposit_days,
                    deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                    daily_rates={calendar[0]: 0.365})
    bumped = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      daily_rates={calendar[0]: 0.365, calendar[4]: 9.999})
    # days 0-3 byte-identical; only day 4 may differ
    assert base.book_values[:4] == bumped.book_values[:4]
    assert base.interest_series[:4] == bumped.interest_series[:4]
    assert bumped.interest_series[4] > base.interest_series[4]


def test_g2a_rate_lookup_uses_most_recent_at_or_before_date_only():
    dates = ["2026-01-01", "2026-01-10"]
    rates = {"2026-01-01": 0.05, "2026-01-10": 0.07}
    assert _rate_for_date(dates, rates, "2026-01-01") == 0.05
    assert _rate_for_date(dates, rates, "2026-01-09") == 0.05   # no interpolation
    assert _rate_for_date(dates, rates, "2026-01-10") == 0.07   # on the observation date
    assert _rate_for_date(dates, rates, "2027-12-31") == 0.07
    with pytest.raises(ValueError):
        _rate_for_date(dates, rates, "2025-12-31")  # before first observation


def test_g2a_daily_rates_empty_dict_rejected():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    with pytest.raises(ValueError):
        simulate(sc, weights, aligned, calendar, deposit_days,
                 deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                 daily_rates={})


def test_g2a_first_1000_free_tier_applies_under_daily_rates():
    # Debt below the free tier accrues nothing; only the excess accrues.
    # Fixture arithmetic: day 0 buys A $3,000 cash; day 2's $500 deposit
    # leaves B's $1,750 target gap funded $500 cash + $1,250 margin ->
    # debt $1,250, of which only $250 is above the $1,000 free tier.
    aligned = {"A": ([100.0] * 4, 0), "B": ([100.0] * 4, 2)}
    calendar = [f"2026-03-{d:02d}" for d in range(1, 5)]
    schedule = {calendar[0]: 3000.0, calendar[2]: 500.0}
    sc = ScenarioConfig(name="free-tier", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=1000.0)
    r = simulate(sc, {"A": 1.0, "B": 1.0}, aligned, calendar,
                 deposit_days=[calendar[0], calendar[2]],
                 deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                 daily_rates={calendar[0]: 0.365})
    draw = next(e for e in r.events if e["kind"] == "margin_draw")
    assert draw["amount"] == pytest.approx(1250.0)
    ints = [e for e in r.events if e["kind"] == "interest_accrual"]
    assert len(ints) == 1
    assert ints[0]["day"] == 3
    assert ints[0]["amount"] == pytest.approx((1250.0 - 1000.0) * 0.365 / 365.0)


# ── explicit dividend cash ───────────────────────────────────────────────────

def test_g2a_dividend_cash_credited_exactly_once():
    aligned = {"A": ([100.0] * 4, 0)}
    calendar = [f"2026-04-{d:02d}" for d in range(1, 5)]
    sc = scenario_unlevered()
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                      dividend_events={calendar[2]: {"A": 2.5}})
    # 1.0 share held from day 0 -> $2.50 credited once, on day 2, never again
    div_events = [e for e in result.events if e["kind"] == "dividend"]
    assert len(div_events) == 1
    assert div_events[0]["day"] == 2
    assert div_events[0]["amount"] == pytest.approx(2.5)
    assert sum(result.dividend_credit_series) == pytest.approx(2.5)
    assert result.dividend_credit_series[2] == pytest.approx(2.5)
    # the credit lands in book value (return component)
    assert result.book_values[2] == pytest.approx(102.5)
    assert result.book_values[3] == pytest.approx(102.5)


def test_g2a_dividend_not_credited_for_unheld_or_not_yet_bought_shares():
    aligned = {"A": ([100.0] * 3, 0), "B": ([100.0] * 3, 0)}
    calendar = [f"2026-04-{d:02d}" for d in range(1, 4)]
    sc = scenario_unlevered()
    # dividend on day 0 for A: credited BEFORE the deposit-driven buy, so
    # zero shares are held at credit time -> no credit. Dividend for a
    # never-held ticker Z -> no credit either.
    result = simulate(sc, {"A": 1.0, "B": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                      dividend_events={calendar[0]: {"A": 5.0, "Z": 9.9}})
    assert [e for e in result.events if e["kind"] == "dividend"] == []
    assert sum(result.dividend_credit_series) == 0.0


def test_g2a_dividend_cash_is_return_not_external_flow():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = [f"2026-04-{d:02d}" for d in range(1, 4)]
    sc = scenario_unlevered()
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                      dividend_events={calendar[1]: {"A": 1.0}})
    # flows records only the deposit -- the dividend is NOT a flow, so TWR
    # counts it as return
    assert result.flows == {0: 100.0}
    assert result.metrics()["ann_twr_pct"] > 0.0


def test_g2a_no_total_return_price_path_exists_in_primary_engine():
    # Structural bar (protocol T-D4 direction, engine side): the primary
    # engine accepts prices only through `aligned` and dividend income only
    # as explicit cash -- no simulate() parameter or module symbol offers a
    # TR-price input.
    params = _inspect.signature(simulate).parameters
    for name in params:
        lowered = name.lower()
        assert "total" not in lowered and "tr_" not in lowered
    import margin_simulation
    module_symbols = [n for n in dir(margin_simulation) if not n.startswith("__")]
    for n in module_symbols:
        assert "total_return" not in n.lower()


# ── explicit non-cash corporate actions (A-17 valuation) ────────────────────

def test_g2a_corporate_action_ratio_valuation_and_cash_in_lieu():
    # 7 shares held, ratio 1/3, child close $30: entitlement 2 1/3 units,
    # credited ENTIRELY as cash = 7 x (1/3) x 30 = $70 -- the fractional
    # 1/3 unit is inherently cash-in-lieu because the whole entitlement is
    # cash and no child position is created.
    aligned = {"A": ([10.0] * 3, 0)}
    calendar = [f"2026-05-{d:02d}" for d in range(1, 4)]
    sc = scenario_unlevered()
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=70.0, min_lot=1.0,
                      corporate_action_events={
                          calendar[1]: [{"ticker": "A", "ratio": 1.0 / 3.0,
                                         "unit_value": 30.0}]})
    ca_events = [e for e in result.events if e["kind"] == "corporate_action_credit"]
    assert len(ca_events) == 1
    assert ca_events[0]["amount"] == pytest.approx(7.0 * (1.0 / 3.0) * 30.0)
    assert sum(result.corporate_action_credit_series) == pytest.approx(70.0)
    # no child position appears
    assert set(result.tracked_values) == set()
    assert result.book_values[1] == pytest.approx(70.0 + 70.0)


def test_g2a_corporate_action_no_holding_no_credit():
    aligned = {"A": ([10.0] * 2, 0)}
    calendar = ["2026-05-01", "2026-05-02"]
    sc = scenario_unlevered()
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=50.0, min_lot=1.0,
                      corporate_action_events={
                          calendar[1]: [{"ticker": "Z", "ratio": 0.5, "unit_value": 40.0}]})
    assert [e for e in result.events if e["kind"] == "corporate_action_credit"] == []
    assert sum(result.corporate_action_credit_series) == 0.0


# ── maintenance-excess proxy ─────────────────────────────────────────────────

def _maintenance_25pct(position_values):
    return 0.25 * sum(position_values.values())


def _levered_state_fixture():
    """A day 0, B day 2; deposit 60 then 20 -> after day 2: gross 100,
    debt 20, net equity 80, leverage 1.25 (hand-derived; matches the
    pre-existing margin-draw fixture arithmetic). Flat prices."""
    aligned = {"A": ([100.0] * 5, 0), "B": ([100.0] * 5, 2)}
    calendar = [f"2026-06-{d:02d}" for d in range(1, 6)]
    deposit_days = [calendar[0], calendar[2]]
    schedule = {calendar[0]: 60.0, calendar[2]: 20.0}
    weights = {"A": 1.0, "B": 1.0}
    return aligned, calendar, deposit_days, schedule, weights


def test_g2a_maintenance_excess_series_computed_daily():
    aligned, calendar, deposit_days, schedule, weights = _levered_state_fixture()
    sc = ScenarioConfig(name="maint", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=_maintenance_25pct)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    # day 0: gross 60, debt 0, ne 60 -> excess = 60 - 15 = 45
    assert result.maintenance_excess_series[0] == pytest.approx(45.0)
    # day 2 on: gross 100, debt 20, ne 80 -> excess = 80 - 25 = 55
    assert result.maintenance_excess_series[2] == pytest.approx(55.0)
    assert result.maintenance_excess_series[4] == pytest.approx(55.0)
    # legacy outputs unaffected by observation alone
    assert result.final_margin_debt == pytest.approx(20.0)
    assert result.liquidation_events == []


def test_g2a_maintenance_fn_absent_series_is_none_and_behavior_pinned():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.maintenance_excess_series == [None] * len(calendar)
    assert result.final_margin_debt == pytest.approx(6.673974604366053)


def test_g2a_margin_draws_blocked_while_opening_maintenance_excess_negative():
    # Requirement deliberately > gross (generic callback, synthetic unit
    # test): opening excess is negative on day 2, so the deposit that day
    # may invest CASH only -- no margin draw. The control run (no
    # maintenance fn) draws $20 of margin from the identical fixture.
    aligned, calendar, deposit_days, schedule, weights = _levered_state_fixture()
    control = simulate(scenario_fixed_leverage(1.8, interest_apr=0.0,
                                               interest_free_amount=0.0),
                       weights, aligned, calendar, deposit_days,
                       deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert any(e["kind"] == "margin_draw" for e in control.events)

    sc = ScenarioConfig(name="blocked", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: 1.1 * sum(pv.values()))
    blocked = simulate(sc, weights, aligned, calendar, deposit_days,
                       deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert not any(e["kind"] == "margin_draw" for e in blocked.events)
    assert blocked.final_margin_debt == 0.0


# ── forced liquidation ───────────────────────────────────────────────────────

def _breach_fixture(sequencing, same_day=False, cure_multiplier=1.25):
    """Levered state (gross 100, debt 20, ne 80 after day 2) with a 90%
    maintenance requirement: end-of-day-2 excess = 80 - 90 = -10 ->
    shortfall 10, cure 12.50 at multiplier 1.25."""
    aligned, calendar, deposit_days, schedule, weights = _levered_state_fixture()
    sc = ScenarioConfig(
        name=f"liq-{sequencing}", leverage_cap=1.8, interest_apr=0.0,
        interest_free_amount=0.0,
        maintenance_requirement_fn=lambda pv: 0.9 * sum(pv.values()),
        liquidation=LiquidationConfig(cure_multiplier=cure_multiplier,
                                      sequencing=sequencing, same_day=same_day))
    return sc, weights, aligned, calendar, deposit_days, schedule


def test_g2a_forced_liquidation_cure_sizing_and_next_session_timing():
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture("pro_rata")
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    # breach detected at day 2 close (excess -10); cure executes day 3
    shortfall_ev = next(e for e in result.events if e["kind"] == "maintenance_shortfall")
    assert shortfall_ev["day"] == 2
    assert shortfall_ev["shortfall"] == pytest.approx(10.0)
    assert shortfall_ev["cure_target"] == pytest.approx(12.5)   # 10 x 1.25
    assert len(result.liquidation_events) == 1
    liq = result.liquidation_events[0]
    assert liq["day"] == 3
    assert liq["trigger_day"] == 2
    assert liq["same_day"] is False
    assert liq["sold_total"] == pytest.approx(12.5)
    assert liq["debt_repaid"] == pytest.approx(12.5)
    # post-cure: gross 87.5, debt 7.5, ne 80 -> excess 80 - 78.75 = +1.25
    assert result.maintenance_excess_series[3] == pytest.approx(1.25)
    assert result.debt_series[3] == pytest.approx(7.5)


def test_g2a_forced_liquidation_same_day_stress_mode():
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture(
        "pro_rata", same_day=True)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    liq = result.liquidation_events[0]
    assert liq["day"] == 2          # executes the trigger day itself
    assert liq["trigger_day"] == 2
    assert liq["same_day"] is True
    # day-2 close series already reflect the cure
    assert result.debt_series[2] == pytest.approx(7.5)
    assert result.maintenance_excess_series[2] == pytest.approx(1.25)


def test_g2a_liquidation_pro_rata_sequencing_sells_proportionally():
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture("pro_rata")
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    sold = result.liquidation_events[0]["sold_by_ticker"]
    # positions at execution: A $60, B $40 of gross 100 -> 12.5 pro-rata
    assert sold["A"] == pytest.approx(12.5 * 0.60)
    assert sold["B"] == pytest.approx(12.5 * 0.40)


def test_g2a_liquidation_largest_first_sequencing_sells_largest_position_only():
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture("largest_first")
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    sold = result.liquidation_events[0]["sold_by_ticker"]
    # A ($60) is largest and fully covers the $12.50 cure -> B untouched
    assert sold == {"A": pytest.approx(12.5)}


def test_g2a_liquidation_never_increases_leverage():
    for sequencing in ("pro_rata", "largest_first"):
        for same_day in (False, True):
            sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture(
                sequencing, same_day=same_day)
            result = simulate(sc, weights, aligned, calendar, deposit_days,
                              deposit_amount=None, min_lot=1.0,
                              deposit_schedule=schedule)
            assert result.liquidation_events, (sequencing, same_day)
            for liq in result.liquidation_events:
                pre, post = liq["pre_leverage"], liq["post_leverage"]
                if pre is not None and post is not None:
                    assert post <= pre + 1e-9, (sequencing, same_day)


def test_g2a_liquidation_requires_maintenance_fn():
    sc = ScenarioConfig(name="bad", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        liquidation=LiquidationConfig(cure_multiplier=1.25,
                                                      sequencing="pro_rata"))
    aligned = {"A": ([100.0], 0)}
    with pytest.raises(ValueError):
        simulate(sc, {"A": 1.0}, aligned, ["2026-01-01"], ["2026-01-01"],
                 deposit_amount=100.0, min_lot=1.0)


def test_g2a_liquidation_config_validation():
    with pytest.raises(ValueError):
        LiquidationConfig(cure_multiplier=0.9, sequencing="pro_rata")
    with pytest.raises(ValueError):
        LiquidationConfig(cure_multiplier=1.25, sequencing="alphabetical")


# ── generalized pre-trade leverage-target hook ───────────────────────────────

class _FixedTargetPolicy:
    """Test-only pure policy: command a constant leverage target."""
    def __init__(self, target, dead_band=0.0):
        self.target = target
        self.dead_band = dead_band

    def __call__(self, state, prior_gross):
        return RepaymentDecision(leverage_target=self.target, dead_band=self.dead_band)


def _target_hook_scenario(target, leverage_cap=1.8, dead_band=0.0):
    return ScenarioConfig(name=f"target-{target}", leverage_cap=leverage_cap,
                          interest_apr=0.0, interest_free_amount=0.0,
                          pre_trade_fn=_FixedTargetPolicy(target, dead_band))


def test_g2a_leverage_target_draws_toward_target():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = [f"2026-07-{d:02d}" for d in range(1, 4)]
    sc = _target_hook_scenario(1.5)
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    # deposit buys $100 cash-funded; the target pass draws $50 of margin
    # to reach gross 150 = 1.5 x ne 100
    assert result.final_margin_debt == pytest.approx(50.0)
    assert result.leverage_series[-1] == pytest.approx(1.5)
    assert any(e["kind"] == "margin_draw" for e in result.events)


def test_g2a_leverage_target_repays_down_when_above_target():
    # Start levered at 1.5x via the target hook, then a policy that
    # switches its target to 1.1 -> engine repays down to exactly 1.1
    # (trim-funded arithmetic).
    class SwitchingPolicy:
        def __call__(self, state, prior_gross):
            target = 1.5 if state.day_index < 2 else 1.1
            return RepaymentDecision(leverage_target=target)

    aligned = {"A": ([100.0] * 4, 0)}
    calendar = [f"2026-07-{d:02d}" for d in range(1, 5)]
    sc = ScenarioConfig(name="switch", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, pre_trade_fn=SwitchingPolicy())
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    assert result.leverage_series[1] == pytest.approx(1.5)
    assert result.leverage_series[2] == pytest.approx(1.1)
    repays = [e for e in result.events if e["kind"] == "repayment"]
    assert repays and repays[0]["source"] == "pre_trade"


def test_g2a_leverage_target_always_constrained_to_1_0_to_1_8():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = [f"2026-07-{d:02d}" for d in range(1, 4)]
    # a policy demanding 5.0x on a scenario whose own cap is ALSO loose
    # (2.5) still gets clamped to the 1.8 hard bound
    sc_high = _target_hook_scenario(5.0, leverage_cap=2.5)
    high = simulate(sc_high, {"A": 1.0}, aligned, calendar,
                    deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    assert all(lv is None or lv <= LEVERAGE_TARGET_HARD_MAX + 1e-9
               for lv in high.leverage_series)
    assert high.leverage_series[-1] == pytest.approx(1.8)
    # a policy demanding 0.3x is clamped to 1.0 -- fully de-levered, never
    # a forced under-1.0 state
    sc_low = _target_hook_scenario(0.3)
    low = simulate(sc_low, {"A": 1.0}, aligned, calendar,
                   deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    assert low.final_margin_debt == pytest.approx(0.0)
    assert all(lv is None or lv <= 1.0 + 1e-9 for lv in low.leverage_series)
    assert LEVERAGE_TARGET_HARD_MIN == 1.0 and LEVERAGE_TARGET_HARD_MAX == 1.8


def test_g2a_leverage_target_dead_band_suppresses_small_moves():
    # At exactly 1.5x, a 1.52 target with a 0.05 dead band must neither
    # draw nor repay.
    class BandedPolicy:
        def __call__(self, state, prior_gross):
            return RepaymentDecision(leverage_target=1.52, dead_band=0.05) \
                if state.day_index >= 1 else RepaymentDecision(leverage_target=1.5)

    aligned = {"A": ([100.0] * 4, 0)}
    calendar = [f"2026-07-{d:02d}" for d in range(1, 5)]
    sc = ScenarioConfig(name="band", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, pre_trade_fn=BandedPolicy())
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    assert result.leverage_series[0] == pytest.approx(1.5)
    # after day 0, no further draws or repayments
    later = [e for e in result.events
             if e["day"] > 0 and e["kind"] in ("margin_draw", "repayment")]
    assert later == []
    assert result.leverage_series[-1] == pytest.approx(1.5)


def test_g2a_leverage_target_none_changes_nothing():
    aligned, calendar, deposit_days, schedule, weights = _regression_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.20, interest_free_amount=0.0)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.final_margin_debt == pytest.approx(6.673974604366053)


# ── structural no-lookahead (engine-wide) ────────────────────────────────────

def test_g2a_perturbing_future_prices_cannot_change_past_outputs():
    aligned, calendar, deposit_days, schedule, weights = _levered_state_fixture()
    sc = ScenarioConfig(name="nl", leverage_cap=1.8, interest_apr=0.05,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=_maintenance_25pct,
                        pre_trade_fn=_FixedTargetPolicy(1.3))
    base = simulate(sc, weights, aligned, calendar, deposit_days,
                    deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                    dividend_events={calendar[1]: {"A": 0.5}})
    perturbed_aligned = {
        "A": ([100.0, 100.0, 100.0, 100.0, 37.0], 0),   # only day 4 differs
        "B": ([100.0] * 5, 2),
    }
    sc2 = ScenarioConfig(name="nl", leverage_cap=1.8, interest_apr=0.05,
                         interest_free_amount=0.0,
                         maintenance_requirement_fn=_maintenance_25pct,
                         pre_trade_fn=_FixedTargetPolicy(1.3))
    pert = simulate(sc2, weights, perturbed_aligned, calendar, deposit_days,
                    deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                    dividend_events={calendar[1]: {"A": 0.5}})
    assert base.book_values[:4] == pert.book_values[:4]
    assert base.debt_series[:4] == pert.debt_series[:4]
    assert [e for e in base.events if e["day"] < 4] == \
           [e for e in pert.events if e["day"] < 4]


# ── determinism ──────────────────────────────────────────────────────────────

def test_g2a_deterministic_under_fixed_inputs():
    sc_args = dict(name="det", leverage_cap=1.8, interest_apr=0.0,
                   interest_free_amount=0.0,
                   maintenance_requirement_fn=_maintenance_25pct)
    aligned, calendar, deposit_days, schedule, weights = _levered_state_fixture()
    kwargs = dict(deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                  daily_rates={calendar[0]: 0.05},
                  dividend_events={calendar[3]: {"A": 1.0}},
                  corporate_action_events={calendar[4]: [
                      {"ticker": "A", "ratio": 0.1, "unit_value": 20.0}]})
    r1 = simulate(ScenarioConfig(**sc_args, pre_trade_fn=_FixedTargetPolicy(1.4)),
                  weights, aligned, calendar, deposit_days, **kwargs)
    r2 = simulate(ScenarioConfig(**sc_args, pre_trade_fn=_FixedTargetPolicy(1.4)),
                  weights, aligned, calendar, deposit_days, **kwargs)
    assert r1.book_values == r2.book_values
    assert r1.debt_series == r2.debt_series
    assert r1.cash_series == r2.cash_series
    assert r1.interest_series == r2.interest_series
    assert r1.events == r2.events
    assert r1.maintenance_excess_series == r2.maintenance_excess_series


# ── hypothetical-label / banned-phrase safeguards with G2A features on ──────

def test_g2a_label_and_banned_phrase_guard_hold_with_new_features_active():
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture("pro_rata")
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      dividend_events={calendar[1]: {"A": 0.25}})
    assert result.label == HYPOTHETICAL_LABEL
    text = render_metrics(result.metrics(), assumptions={"leverage_cap": 1.8})
    _assert_no_banned_language(text)
    assert HYPOTHETICAL_LABEL in text


# ── untouched-test isolation (structural) ────────────────────────────────────

def test_g2a_engine_module_cannot_touch_files_or_sealed_archive():
    # The engine performs no file/network I/O at all: it imports none of
    # the modules that could open the sealed archive (tarfile) or any file
    # (os/pathlib/io/json), and its code contains no open() call. Data
    # reaches it only in memory. This structurally proves normal G2
    # development paths through this engine cannot access the sealed
    # untouched archive.
    import margin_simulation
    tree = _ast.parse(open(margin_simulation.__file__).read())
    imported = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, _ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    forbidden = {"tarfile", "os", "pathlib", "io", "json", "shutil",
                 "subprocess", "urllib", "requests"}
    assert imported & forbidden == set(), imported & forbidden
    open_calls = [n for n in _ast.walk(tree)
                  if isinstance(n, _ast.Call)
                  and isinstance(n.func, _ast.Name) and n.func.id == "open"]
    assert open_calls == []


def test_g2a_dev_price_cache_contains_no_bar_after_development_boundary():
    # The development-visible research price files must remain truncated at
    # the Track 2 boundary -- the G1 seal held through G2A.
    prices_dir = _os.path.join(_RESEARCH_DIR, "data", "prices")
    assert _os.path.isdir(prices_dir)
    boundary = "2025-06-30"
    checked = 0
    for fname in sorted(_os.listdir(prices_dir)):
        if not fname.endswith(".json"):
            continue
        with open(_os.path.join(prices_dir, fname)) as f:
            doc = _json.load(f)
        last_date = doc["bars"][-1]["t"][:10]
        assert last_date <= boundary, (fname, last_date)
        checked += 1
    assert checked == 63


def test_g2a_sealed_archive_opened_only_at_the_seal_creation_site():
    # data_acquisition.py may touch tarfile only inside acquire_prices()
    # (seal creation). No other function -- and therefore no G2
    # development path -- opens the archive; unsealing is a G4-runner act.
    path = _os.path.join(_RESEARCH_DIR, "data_acquisition.py")
    tree = _ast.parse(open(path).read())
    offenders = []

    def scan(node, owner):
        for child in _ast.iter_child_nodes(node):
            child_owner = child.name if isinstance(
                child, (_ast.FunctionDef, _ast.AsyncFunctionDef)) else owner
            if isinstance(child, _ast.Attribute) and isinstance(child.value, _ast.Name) \
                    and child.value.id == "tarfile":
                if owner != "acquire_prices":
                    offenders.append((owner, child.attr))
            scan(child, child_owner)

    scan(tree, "<module>")
    assert offenders == [], offenders


def test_g2a_sealed_index_boundary_and_archive_hash_intact():
    sealed_dir = _os.path.join(_RESEARCH_DIR, "data", "untouched_sealed")
    with open(_os.path.join(sealed_dir, "SEALED_INDEX.json")) as f:
        idx = _json.load(f)
    assert idx["meta"]["boundary"] == "2025-06-30"
    h = _hashlib.sha256()
    with open(_os.path.join(sealed_dir, "untouched_prices.tar.gz"), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    # byte-level integrity only -- the archive is never opened here
    assert h.hexdigest() == idx["meta"]["archive_sha256"]


def test_g2a_no_trial_ledger_exists_zero_registered_trials_consumed():
    # G2A runs engine-integrity tests only; the registered-trial ledger
    # must not exist until Study runs are separately authorized (G3).
    assert not _os.path.exists(_os.path.join(_RESEARCH_DIR, "trial_ledger.jsonl"))
    assert not _os.path.exists(_os.path.join(_RESEARCH_DIR, "candidate_freeze.yaml"))


# ── the G2A rate pin (assumptions-ledger A-23) ───────────────────────────────

def test_g2a_pinned_spread_observation_set_matches_recorded_hash():
    import yaml
    with open(_os.path.join(_RESEARCH_DIR, "assumptions_ledger.yaml")) as f:
        ledger = yaml.safe_load(f)
    a23 = next(a for a in ledger["assumptions"] if a["id"] == "A-23")
    frozen = a23["frozen_observation_set"]
    obs = frozen["observations"]
    assert len(obs) == 4
    assert [o["date"] for o in obs] == \
        ["2020-12-21", "2022-11-03", "2025-12-15", "2026-07-22"]
    assert [o["implied_spread_pp"] for o in obs] == [2.41, 2.67, 2.11, 1.37]
    recomputed = _hashlib.sha256(
        _json.dumps(obs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert recomputed == frozen["canonical_json_sha256"]
    # the two in-development-window DFF legs match the committed dataset
    with open(_os.path.join(_RESEARCH_DIR, "data", "rates", "dff.json")) as f:
        dff = {r["date"]: r["rate_pct"] for r in _json.load(f)["rates"]}
    assert dff["2020-12-21"] == pytest.approx(obs[0]["dff_pct"])
    assert dff["2022-11-03"] == pytest.approx(obs[1]["dff_pct"])


# ═════════════════════════════════════════════════════════════════════════════
# MARGIN-0005 G2A remediation (post-independent-review corrective commit).
# Three engine corrections, each addressing one independent-review finding:
#   (2) dividend entitlement must survive same-day liquidation/trim, not use
#       post-mutation shares;
#   (3) the maintenance-excess proxy must count idle cash (full account-
#       equity identity), not net_equity alone;
#   (4) forced liquidation must never fire against a debt-free account, and
#       a malformed/non-finite/negative maintenance requirement must raise.
# Still G2 engine-integrity tests on synthetic data — NOT registered Study
# A/B/C trials; no trial_ledger.jsonl exists or is created here.
# ═════════════════════════════════════════════════════════════════════════════

from margin_simulation import _account_equity, _validated_maintenance_requirement


# ── (2) dividend entitlement survives same-day liquidation/trim ─────────────

def test_g2a_dividend_entitlement_survives_pending_liquidation_on_event_date():
    # A next-session (pending) liquidation queued from yesterday's breach
    # executes at the very top of the event date's own loop iteration --
    # BEFORE the dividend used to be credited under the pre-remediation
    # code (which read `shares` post-mutation). A holder of record at the
    # OPENING of the event date (= end of the prior day, since nothing
    # else happens overnight) must still receive the dividend even though
    # the morning's cure trims that same position.
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture("pro_rata")
    control = simulate(sc, weights, aligned, calendar, deposit_days,
                       deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                       track_tickers=["A"])
    assert control.liquidation_events and control.liquidation_events[0]["day"] == 3
    pre_liquidation_a_shares = control.tracked_values["A"][2] / 100.0  # EOD day2 = opening day3

    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      dividend_events={calendar[3]: {"A": 1.0}})
    div_events = [e for e in result.events if e["kind"] == "dividend"]
    assert len(div_events) == 1
    assert div_events[0]["day"] == 3
    assert div_events[0]["amount"] == pytest.approx(pre_liquidation_a_shares * 1.0)
    # sanity: the same-morning liquidation really did trim A -- proving this
    # test would have failed under the pre-remediation post-mutation read
    assert result.liquidation_events[0]["sold_by_ticker"].get("A", 0.0) > 0
    assert result.dividend_credit_series[3] == pytest.approx(div_events[0]["amount"])


def test_g2a_dividend_entitlement_survives_same_day_stress_liquidation_on_event_date():
    sc, weights, aligned, calendar, deposit_days, schedule = _breach_fixture(
        "pro_rata", same_day=True)
    control = simulate(sc, weights, aligned, calendar, deposit_days,
                       deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                       track_tickers=["A"])
    assert control.liquidation_events and control.liquidation_events[0]["day"] == 2
    opening_day2_a_shares = control.tracked_values["A"][1] / 100.0  # EOD day1 = opening day2

    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      dividend_events={calendar[2]: {"A": 2.0}})
    div_events = [e for e in result.events if e["kind"] == "dividend"]
    assert len(div_events) == 1
    assert div_events[0]["day"] == 2
    assert div_events[0]["amount"] == pytest.approx(opening_day2_a_shares * 2.0)
    # the same-day stress liquidation still fires later that same day
    assert result.liquidation_events and result.liquidation_events[0]["day"] == 2


def test_g2a_dividend_entitlement_survives_pre_trade_trim_on_event_date():
    class SwitchingPolicy:
        def __call__(self, state, prior_gross):
            target = 1.5 if state.day_index < 2 else 1.1
            return RepaymentDecision(leverage_target=target)

    aligned = {"A": ([100.0] * 4, 0)}
    calendar = [f"2026-07-{d:02d}" for d in range(1, 5)]
    sc = ScenarioConfig(name="switch-div", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, pre_trade_fn=SwitchingPolicy())
    control = simulate(sc, {"A": 1.0}, aligned, calendar,
                       deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                       track_tickers=["A"])
    assert any(e["kind"] == "repayment" and e["day"] == 2 for e in control.events)
    opening_day2_a_shares = control.tracked_values["A"][1] / 100.0  # EOD day1 = opening day2

    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                      track_tickers=["A"],
                      dividend_events={calendar[2]: {"A": 0.10}})
    div_events = [e for e in result.events if e["kind"] == "dividend"]
    assert len(div_events) == 1
    assert div_events[0]["day"] == 2
    assert div_events[0]["amount"] == pytest.approx(opening_day2_a_shares * 0.10)
    # the pre-trade trim really did reduce A's holding that same day
    assert result.tracked_values["A"][2] < opening_day2_a_shares * 100.0


def test_g2a_dividend_entitlement_not_retroactive_for_same_day_acquisition():
    # A deposit-driven buy happens strictly AFTER the dividend block in the
    # day loop, so shares acquired today (or a ticker never held before
    # today) cannot receive today's dividend -- this already held under the
    # pre-remediation code (the buy always came after the credit); the
    # opening-snapshot fix must not change that.
    aligned = {"A": ([100.0] * 3, 0), "B": ([100.0] * 3, 0)}
    calendar = [f"2026-04-{d:02d}" for d in range(1, 4)]
    sc = scenario_unlevered()
    result = simulate(sc, {"A": 1.0, "B": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                      dividend_events={calendar[0]: {"A": 5.0, "Z": 9.9}})
    assert [e for e in result.events if e["kind"] == "dividend"] == []
    assert sum(result.dividend_credit_series) == 0.0


def test_g2a_dividend_and_corporate_action_and_interest_reconcile_on_a_shared_day():
    # Multiple event kinds on one day, each credited independently, exactly
    # once, distinctly sized, none conflated with another.
    aligned, calendar, deposit_days, schedule, weights = _levered_flat_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.365, interest_free_amount=0.0)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule,
                      dividend_events={calendar[3]: {"A": 1.0}},
                      corporate_action_events={calendar[3]: [
                          {"ticker": "A", "ratio": 0.05, "unit_value": 40.0}]})
    day3 = 3
    kinds = [e["kind"] for e in result.events if e["day"] == day3]
    assert "interest_accrual" in kinds
    assert "dividend" in kinds
    assert "corporate_action_credit" in kinds
    div = next(e for e in result.events if e["kind"] == "dividend")
    ca = next(e for e in result.events if e["kind"] == "corporate_action_credit")
    interest = next(e for e in result.events
                    if e["kind"] == "interest_accrual" and e["day"] == day3)
    assert div["amount"] == pytest.approx(0.6 * 1.0)
    assert ca["amount"] == pytest.approx(0.6 * 0.05 * 40.0)
    assert div["amount"] != ca["amount"]
    assert result.dividend_credit_series[day3] == pytest.approx(div["amount"])
    assert result.corporate_action_credit_series[day3] == pytest.approx(ca["amount"])
    assert result.interest_series[day3] == pytest.approx(interest["amount"])
    # each kind credited exactly once anywhere in the run -- no duplicate
    assert len([e for e in result.events if e["kind"] == "dividend"]) == 1
    assert len([e for e in result.events if e["kind"] == "corporate_action_credit"]) == 1


# ── (3) maintenance-excess proxy counts idle cash (account-equity identity) ─

def test_g2a_account_equity_helper_matches_documented_identity():
    assert _account_equity(gross=150.0, cash=12.0, margin_debt=40.0) == pytest.approx(122.0)
    assert _account_equity(gross=0.0, cash=0.0, margin_debt=0.0) == 0.0


def test_g2a_maintenance_equity_includes_idle_cash_prevents_artificial_breach():
    # A dividend lands on a non-deposit day (calendar[1]) and is NOT
    # reinvested (no allocation runs on a non-deposit day), so it sits as
    # genuinely idle cash -- exactly the case the pre-remediation
    # net_equity-only formula ignored.
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2026-09-01", "2026-09-02", "2026-09-03"]
    sc = ScenarioConfig(name="cash-cushion", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: 1.05 * sum(pv.values()))
    result = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                      dividend_events={calendar[1]: {"A": 50.0}})
    # day0: fully invested, gross 100, cash 0 -> equity 100, requirement
    # 105 -> a real breach (no cash cushion yet)
    assert result.maintenance_excess_series[0] == pytest.approx(100.0 - 105.0)
    assert result.maintenance_excess_series[0] < 0
    # day1: $50 idle dividend cash -> equity 100 + 50 = 150, requirement
    # 105 -> the cash cushion ALONE flips this from breach to no-breach
    assert result.cash_series[1] == pytest.approx(50.0)
    assert result.maintenance_excess_series[1] == pytest.approx(150.0 - 105.0)
    assert result.maintenance_excess_series[1] > 0


def test_g2a_idle_cash_partially_cures_shortfall_and_correctly_sizes_liquidation():
    # A price crash creates a real maintenance breach on day 2. A dividend
    # that landed (and sat idle) on day 1 -- before the crash -- cushions
    # the day-2 breach by exactly its own dollar amount: smaller shortfall,
    # smaller cure_target, smaller liquidation -- not a full cure, a partial
    # one, and the resulting liquidation is correctly sized to the reduced
    # shortfall.
    class Day0OnlyTarget:
        def __call__(self, state, prior_gross):
            if state.day_index == 0:
                return RepaymentDecision(leverage_target=1.5)
            return RepaymentDecision()

    aligned = {"A": ([100.0, 100.0, 60.0, 60.0], 0)}
    calendar = ["2026-11-01", "2026-11-02", "2026-11-03", "2026-11-04"]
    sc = ScenarioConfig(name="crash", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, pre_trade_fn=Day0OnlyTarget(),
                        maintenance_requirement_fn=lambda pv: 0.5 * sum(pv.values()),
                        liquidation=LiquidationConfig(cure_multiplier=1.0,
                                                      sequencing="pro_rata", same_day=True))
    baseline = simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                        deposit_amount=100.0, min_lot=1.0)
    cushioned = simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                         deposit_amount=100.0, min_lot=1.0,
                         dividend_events={calendar[1]: {"A": 2.0}})

    dividend_amount = 2.0 * 1.5  # 1.5 shares (from the 1.5x day-0 draw) x $2/share
    b_first = next(e for e in baseline.events if e["kind"] == "forced_liquidation")
    c_first = next(e for e in cushioned.events if e["kind"] == "forced_liquidation")
    assert b_first["day"] == c_first["day"] == 2
    assert c_first["shortfall"] == pytest.approx(b_first["shortfall"] - dividend_amount)
    assert c_first["cure_target"] == pytest.approx(b_first["cure_target"] - dividend_amount)
    assert c_first["sold_total"] < b_first["sold_total"]
    assert c_first["shortfall"] > 0   # still a real, partial breach -- not fully cured


def test_g2a_dividend_cash_affects_maintenance_equity_exactly_once():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2026-12-01", "2026-12-02", "2026-12-03"]
    sc = ScenarioConfig(name="div-maint", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: 0.5 * sum(pv.values()))
    no_div = simulate(sc, {"A": 1.0}, aligned, calendar,
                      deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    with_div = simulate(sc, {"A": 1.0}, aligned, calendar,
                        deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                        dividend_events={calendar[1]: {"A": 3.0}})
    # gross/debt paths identical -- the dividend is pure idle cash, no
    # position or debt effect
    assert no_div.gross_series == with_div.gross_series
    assert no_div.debt_series == with_div.debt_series
    assert with_div.maintenance_excess_series[0] == pytest.approx(
        no_div.maintenance_excess_series[0])
    # from day 1 on, the excess differs by EXACTLY the dividend amount,
    # once -- not re-applied or compounding day over day
    for i in (1, 2):
        assert with_div.maintenance_excess_series[i] == pytest.approx(
            no_div.maintenance_excess_series[i] + 3.0)


def test_g2a_corporate_action_cash_affects_maintenance_equity_exactly_once():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2026-12-01", "2026-12-02", "2026-12-03"]
    sc = ScenarioConfig(name="ca-maint", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: 0.5 * sum(pv.values()))
    no_ca = simulate(sc, {"A": 1.0}, aligned, calendar,
                     deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0)
    with_ca = simulate(sc, {"A": 1.0}, aligned, calendar,
                       deposit_days=[calendar[0]], deposit_amount=100.0, min_lot=1.0,
                       corporate_action_events={calendar[1]: [
                           {"ticker": "A", "ratio": 0.02, "unit_value": 25.0}]})
    ca_amount = 1.0 * 0.02 * 25.0   # 1.0 share held (single-ticker full-cash buy)
    assert no_ca.gross_series == with_ca.gross_series
    assert no_ca.debt_series == with_ca.debt_series
    for i in (1, 2):
        assert with_ca.maintenance_excess_series[i] == pytest.approx(
            no_ca.maintenance_excess_series[i] + ca_amount)


def test_g2a_zero_idle_cash_reproduces_prior_maintenance_calculation():
    # In a fixture where cash happens to be exactly 0 at every observation
    # point (the pre-existing test_g2a_maintenance_excess_series_computed_
    # daily fixture), the new account-equity formula must reproduce the
    # exact pre-remediation pinned values -- proving the correction is a
    # pure extension, not a change, when there is no cash to count.
    aligned, calendar, deposit_days, schedule, weights = _levered_state_fixture()
    sc = ScenarioConfig(name="maint", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=_maintenance_25pct)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=None, min_lot=1.0, deposit_schedule=schedule)
    assert result.cash_series[0] == pytest.approx(0.0)
    assert result.cash_series[2] == pytest.approx(0.0)
    assert result.cash_series[4] == pytest.approx(0.0)
    assert result.maintenance_excess_series[0] == pytest.approx(45.0)
    assert result.maintenance_excess_series[2] == pytest.approx(55.0)
    assert result.maintenance_excess_series[4] == pytest.approx(55.0)


# ── (4) forced liquidation never fires at zero debt; malformed input raises ─

def test_g2a_pathological_requirement_at_zero_debt_never_liquidates():
    # A single-ticker deposit never draws margin (target always equals
    # cash in hand -- see the pre-existing fixtures), so debt is 0
    # throughout. Even an absurdly tight (but well-formed: finite,
    # non-negative, numeric) requirement must never trigger a forced sale
    # -- there is no borrowed exposure to call. The proxy value is still
    # computed and reported for observability.
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2027-01-01", "2027-01-02", "2027-01-03"]
    sc = ScenarioConfig(name="zero-debt-pathological", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: 100.0 * sum(pv.values()),
                        liquidation=LiquidationConfig(cure_multiplier=1.25,
                                                      sequencing="pro_rata"))
    result = simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                      deposit_amount=100.0, min_lot=1.0)
    assert result.liquidation_events == []
    assert result.final_margin_debt == 0.0
    assert all(e["kind"] != "forced_liquidation" for e in result.events)
    assert all(e["kind"] != "maintenance_shortfall" for e in result.events)
    assert all(x is not None and x < 0 for x in result.maintenance_excess_series)


def test_g2a_debt_crossing_exactly_to_zero_during_cure_stops_further_liquidation():
    # An aggressive same-day cure sells the ENTIRE position, fully
    # extinguishing debt in one shot (debt lands exactly at 0.0). Even
    # though the (pathological) requirement stays enormous relative to
    # whatever gross remains, no further liquidation may occur once debt
    # is 0 -- the loop must converge, not repeat.
    class Day0OnlyTarget:
        def __call__(self, state, prior_gross):
            if state.day_index == 0:
                return RepaymentDecision(leverage_target=1.5)
            return RepaymentDecision()

    aligned = {"A": ([100.0, 100.0, 60.0, 60.0, 60.0], 0)}
    calendar = [f"2027-02-{d:02d}" for d in range(1, 6)]
    sc = ScenarioConfig(name="wipe-debt", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0, pre_trade_fn=Day0OnlyTarget(),
                        maintenance_requirement_fn=lambda pv: 100.0 * sum(pv.values()),
                        liquidation=LiquidationConfig(cure_multiplier=1.0,
                                                      sequencing="pro_rata", same_day=True))
    result = simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                      deposit_amount=100.0, min_lot=1.0)
    assert result.debt_series[0] == pytest.approx(0.0)   # wiped same day it was drawn
    assert result.final_margin_debt == 0.0
    assert len(result.liquidation_events) == 1            # exactly one -- no repeat cascade
    assert all(d == pytest.approx(0.0) for d in result.debt_series)


def test_g2a_maintenance_requirement_nan_and_infinity_raise():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2027-01-01", "2027-01-02", "2027-01-03"]
    for bad in (float("nan"), float("inf"), float("-inf")):
        sc = ScenarioConfig(name="bad", leverage_cap=1.8, interest_apr=0.0,
                            interest_free_amount=0.0,
                            maintenance_requirement_fn=lambda pv, b=bad: b)
        with pytest.raises(ValueError):
            simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                    deposit_amount=100.0, min_lot=1.0)


def test_g2a_maintenance_requirement_negative_raises():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2027-01-01", "2027-01-02", "2027-01-03"]
    sc = ScenarioConfig(name="neg", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: -5.0)
    with pytest.raises(ValueError):
        simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                deposit_amount=100.0, min_lot=1.0)


def test_g2a_maintenance_requirement_non_numeric_raises():
    aligned = {"A": ([100.0] * 3, 0)}
    calendar = ["2027-01-01", "2027-01-02", "2027-01-03"]
    sc = ScenarioConfig(name="str-bad", leverage_cap=1.8, interest_apr=0.0,
                        interest_free_amount=0.0,
                        maintenance_requirement_fn=lambda pv: "not-a-number")
    with pytest.raises(ValueError):
        simulate(sc, {"A": 1.0}, aligned, calendar, deposit_days=[calendar[0]],
                deposit_amount=100.0, min_lot=1.0)


def test_g2a_validated_maintenance_requirement_helper_accepts_valid_input():
    assert _validated_maintenance_requirement(lambda pv: 42.0, {}) == pytest.approx(42.0)
    assert _validated_maintenance_requirement(lambda pv: 0, {}) == pytest.approx(0.0)
