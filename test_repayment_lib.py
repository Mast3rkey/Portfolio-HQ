"""Tests for repayment_lib.py (MARGIN-0005 G2B repayment-policy library).

All fixtures here are small, synthetic, hand-computable states — never real
`data/backtest/*.json` prices, never a registered Study A/B/C configuration.
Nothing in this file creates `trial_ledger.jsonl` or `candidate_freeze.yaml`,
touches any of the 300 registered trial slots, or reads untouched-test data.
The two `simulate()` smoke tests near the bottom exist only to prove this
library's `RepaymentDecision` output is literally engine-compatible — they
are not a Study A run.
"""

import ast
import functools
import inspect
import math
import os

import pytest

from margin_simulation import (
    LEVERAGE_TARGET_HARD_MAX,
    LEVERAGE_TARGET_HARD_MIN,
    ModelBProfitHarvest,
    PortfolioState,
    RepaymentDecision,
    ScenarioConfig,
    scenario_fixed_leverage,
    simulate,
)

import repayment_lib
from repayment_lib import (
    MODEL_B_REFERENCE_REPAY_FRACTION,
    REPAYMENT_FAMILY_CATEGORY,
    IntelligenceAdvisorySemantic,
    R6MaintenanceDeterioration,
    RepaymentCategory,
    RepaymentFamily,
    r1_deposits_first,
    r2_dividends_first,
    r3_governed_trims_first,
    r4_borrowing_cost_hurdle,
    r5_trend_vol_deterioration,
    r7_intelligence_advisory,
    r8_restore_to_target_only,
    r9_full_repayment_to_unlevered,
    rb_model_b_profit_harvest,
)


# ── fixtures / helpers ───────────────────────────────────────────────────────

def _ps(day_index=0, cash=0.0, positions=None, margin_debt=0.0, gross=0.0,
       maintenance_excess=None):
    return PortfolioState(day_index=day_index, cash=cash,
                          positions=positions or {}, margin_debt=margin_debt,
                          gross=gross, maintenance_excess=maintenance_excess)


def _levered_state(leverage, net_equity=100.0, day_index=0,
                   maintenance_excess=None):
    """A state at an exact leverage ratio over the given net_equity, funded
    entirely by margin debt (no idle cash)."""
    gross = leverage * net_equity
    margin_debt = gross - net_equity
    return _ps(day_index=day_index, positions={"X": 1.0},
              margin_debt=margin_debt, gross=gross,
              maintenance_excess=maintenance_excess)


DEBT_FREE = _ps(gross=100.0, margin_debt=0.0, positions={"X": 1.0})


# ── isolation / import-boundary tests ────────────────────────────────────────

def test_module_source_imports_only_approved_dependencies():
    tree = ast.parse(open(repayment_lib.__file__).read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert imported <= {"margin_simulation", "math", "enum", "types", "__future__"}
    forbidden = {"allocate", "margin_state", "os", "sys", "pathlib", "io",
                "json", "shutil", "requests", "urllib", "socket", "yaml",
                "sqlite3", "subprocess", "alpaca_client"}
    assert imported & forbidden == set()


def test_module_has_no_filesystem_or_network_io():
    src = open(repayment_lib.__file__).read()
    for token in ("open(", "requests.", "urllib", "socket.", "yaml.safe_load",
                 "subprocess."):
        assert token not in src, token


def test_module_does_not_import_or_define_liquidation_mechanics():
    assert not hasattr(repayment_lib, "LiquidationConfig")
    assert not hasattr(repayment_lib, "_execute_forced_liquidation")


def test_no_scoring_ranking_or_pooling_function_exists():
    public = [n for n in dir(repayment_lib) if not n.startswith("_")]
    banned = ("rank", "score", "aggregate", "combine", "pool")
    offending = [n for n in public if any(b in n.lower() for b in banned)]
    assert offending == []


def test_module_has_no_top_level_side_effecting_statements():
    # No reload here (deliberately): reloading a module that defines an
    # Enum swaps in a *new* class object, and anything imported from the
    # module before the reload (e.g. this test file's own `from
    # repayment_lib import IntelligenceAdvisorySemantic`) would then fail
    # `isinstance` checks against the reloaded class for the rest of the
    # test session -- a self-inflicted cross-test hazard, not a real
    # side-effect concern. Static inspection proves the same property
    # (no top-level Call other than the read-only MappingProxyType
    # construction, which performs no I/O) without that hazard.
    tree = ast.parse(open(repayment_lib.__file__).read())
    allowed_calls_at_top_level = {"MappingProxyType"}
    for node in tree.body:
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                func = child.func
                name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
                assert name in allowed_calls_at_top_level, (
                    f"unexpected top-level call {name!r} -- possible import side effect")


def test_no_trial_or_freeze_artifacts_exist_after_importing_repayment_lib():
    research_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "research", "margin_target_study")
    assert not os.path.exists(os.path.join(research_dir, "trial_ledger.jsonl"))
    assert not os.path.exists(os.path.join(research_dir, "candidate_freeze.yaml"))


def test_no_production_module_imports_repayment_lib():
    for path in ("allocate.py", "margin_state.py"):
        tree = ast.parse(open(path).read())
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
        assert "repayment_lib" not in names


def test_r7_signature_has_no_ticker_or_recipient_parameter():
    params = inspect.signature(r7_intelligence_advisory).parameters
    for forbidden_name in ("ticker", "tickers", "recipient", "security"):
        assert forbidden_name not in params


# ── T-5: repayment invariants ────────────────────────────────────────────────

def _sample_decisions():
    """One representative decision from every family, under both a
    leverage-breach state and a non-breach state, for the cross-family
    invariant sweep below."""
    breach = _levered_state(1.8, maintenance_excess=-5.0)
    calm = _levered_state(1.1, maintenance_excess=500.0)
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=100.0,
                                    staged_fraction_per_week=0.25)
    rb = rb_model_b_profit_harvest()
    rb(_ps(day_index=0, gross=100.0, margin_debt=0.0), None)  # seed HWM
    decisions = []
    for state in (breach, calm):
        decisions.append(r1_deposits_first(state, is_deposit_day=True,
                                           target_leverage=1.25))
        decisions.append(r1_deposits_first(state, is_deposit_day=False,
                                           target_leverage=1.25))
        decisions.append(r2_dividends_first(state, dividend_cash=10.0))
        decisions.append(r3_governed_trims_first(state, trim_proceeds=10.0))
        decisions.append(r4_borrowing_cost_hurdle(
            state, effective_apr=0.09, hurdle=0.08, available_cash=10.0))
        decisions.append(r5_trend_vol_deterioration(
            state, trend_deteriorated=True, vol_deteriorated=False))
        decisions.append(r7_intelligence_advisory(
            state, semantic=IntelligenceAdvisorySemantic.WHOLE_CYCLE_DRAW_FREEZE,
            flag_active=True))
        decisions.append(r7_intelligence_advisory(
            state, semantic=IntelligenceAdvisorySemantic.ACCOUNT_LEVEL_REPAYMENT_ADVISORY,
            flag_active=True, target_leverage=1.0))
        decisions.append(r8_restore_to_target_only(state, target_leverage=1.25))
        decisions.append(r9_full_repayment_to_unlevered(state, triggered=True))
        decisions.append(r9_full_repayment_to_unlevered(state, triggered=False))
    decisions.append(r6(_levered_state(1.5, maintenance_excess=10.0, day_index=0)))
    decisions.append(rb(_levered_state(1.5, day_index=1), None))
    return decisions


def test_no_family_ever_returns_a_negative_repay_amount():
    for d in _sample_decisions():
        assert d.repay_amount >= 0.0


def test_no_family_ever_sets_the_draw_capable_leverage_target_field():
    # This module deliberately never sets RepaymentDecision.leverage_target
    # (see module docstring) -- only repay_amount/effective_leverage_cap,
    # neither of which can command an autonomous margin draw.
    for d in _sample_decisions():
        assert d.leverage_target is None


def test_every_emitted_leverage_cap_is_within_governed_bounds():
    for d in _sample_decisions():
        if d.effective_leverage_cap is not None:
            assert LEVERAGE_TARGET_HARD_MIN <= d.effective_leverage_cap <= LEVERAGE_TARGET_HARD_MAX


@pytest.mark.parametrize("requested_target", [1000.0, 1.8000001, -5.0, 0.0, 0.999])
def test_extreme_or_out_of_range_targets_are_always_clamped(requested_target):
    d = r8_restore_to_target_only(_levered_state(1.8), target_leverage=requested_target)
    assert LEVERAGE_TARGET_HARD_MIN <= d.effective_leverage_cap <= LEVERAGE_TARGET_HARD_MAX


def test_lower_scenario_cap_is_respected_even_when_target_requests_1_8x():
    d = r8_restore_to_target_only(_levered_state(1.8), target_leverage=1.8,
                                  scenario_cap=1.25)
    assert d.effective_leverage_cap == pytest.approx(1.25)


def test_repayment_decisions_are_deterministic_for_pure_functions():
    state = _levered_state(1.6)
    a = r8_restore_to_target_only(state, target_leverage=1.25)
    b = r8_restore_to_target_only(state, target_leverage=1.25)
    assert a.repay_amount == b.repay_amount
    assert a.effective_leverage_cap == b.effective_leverage_cap
    assert a.leverage_target == b.leverage_target


def test_no_family_can_weaken_the_engine_hard_bounds():
    # Even a call that asks for something absurd never escapes [1.0, 1.8].
    d = r1_deposits_first(_levered_state(1.8), is_deposit_day=True,
                          target_leverage=99.0, scenario_cap=99.0)
    assert d.effective_leverage_cap == pytest.approx(LEVERAGE_TARGET_HARD_MAX)


# ── category registry / categorical separation ───────────────────────────────

def test_category_mapping_matches_protocol_labels_exactly():
    expected = {
        RepaymentFamily.R1_DEPOSITS_FIRST: RepaymentCategory.CASH_FLOW_PRIORITY,
        RepaymentFamily.R2_DIVIDENDS_FIRST: RepaymentCategory.CASH_FLOW_PRIORITY,
        RepaymentFamily.R3_GOVERNED_TRIMS_FIRST: RepaymentCategory.CASH_FLOW_PRIORITY,
        RepaymentFamily.R4_BORROWING_COST_HURDLE: RepaymentCategory.COST_TRIGGERED,
        RepaymentFamily.R5_TREND_VOL_DETERIORATION: RepaymentCategory.STATE_TRIGGERED,
        RepaymentFamily.R6_MAINTENANCE_DETERIORATION: RepaymentCategory.STATE_TRIGGERED,
        RepaymentFamily.R7_INTELLIGENCE_ADVISORY: RepaymentCategory.ADVISORY,
        RepaymentFamily.R8_RESTORE_TO_TARGET_ONLY: RepaymentCategory.POSTURE_DEFINING,
        RepaymentFamily.R9_FULL_REPAYMENT_TO_UNLEVERED: RepaymentCategory.POSTURE_DEFINING,
        RepaymentFamily.RB_MODEL_B_PROFIT_HARVEST: RepaymentCategory.PROFIT_PATH,
    }
    assert dict(REPAYMENT_FAMILY_CATEGORY) == expected


def test_category_mapping_is_read_only():
    with pytest.raises(TypeError):
        REPAYMENT_FAMILY_CATEGORY[RepaymentFamily.R1_DEPOSITS_FIRST] = RepaymentCategory.ADVISORY


def test_rb_is_structurally_and_categorically_distinct_from_r8():
    rb = rb_model_b_profit_harvest()
    assert isinstance(rb, ModelBProfitHarvest)
    assert callable(rb)
    assert not isinstance(r8_restore_to_target_only, ModelBProfitHarvest)
    assert (REPAYMENT_FAMILY_CATEGORY[RepaymentFamily.RB_MODEL_B_PROFIT_HARVEST]
            != REPAYMENT_FAMILY_CATEGORY[RepaymentFamily.R8_RESTORE_TO_TARGET_ONLY])


def test_all_six_categories_are_represented_and_distinct_bucket_membership():
    buckets = {}
    for family, category in REPAYMENT_FAMILY_CATEGORY.items():
        buckets.setdefault(category, set()).add(family)
    assert buckets[RepaymentCategory.CASH_FLOW_PRIORITY] == {
        RepaymentFamily.R1_DEPOSITS_FIRST, RepaymentFamily.R2_DIVIDENDS_FIRST,
        RepaymentFamily.R3_GOVERNED_TRIMS_FIRST}
    assert buckets[RepaymentCategory.COST_TRIGGERED] == {RepaymentFamily.R4_BORROWING_COST_HURDLE}
    assert buckets[RepaymentCategory.STATE_TRIGGERED] == {
        RepaymentFamily.R5_TREND_VOL_DETERIORATION, RepaymentFamily.R6_MAINTENANCE_DETERIORATION}
    assert buckets[RepaymentCategory.ADVISORY] == {RepaymentFamily.R7_INTELLIGENCE_ADVISORY}
    assert buckets[RepaymentCategory.POSTURE_DEFINING] == {
        RepaymentFamily.R8_RESTORE_TO_TARGET_ONLY, RepaymentFamily.R9_FULL_REPAYMENT_TO_UNLEVERED}
    assert buckets[RepaymentCategory.PROFIT_PATH] == {RepaymentFamily.RB_MODEL_B_PROFIT_HARVEST}


# ── R1 — deposits first ──────────────────────────────────────────────────────

def test_r1_non_deposit_day_is_always_a_no_op():
    d = r1_deposits_first(_levered_state(1.8), is_deposit_day=False,
                          target_leverage=1.25)
    assert d == RepaymentDecision()


def test_r1_deposit_day_below_target_repays_nothing_but_caps_buying():
    d = r1_deposits_first(_levered_state(1.1), is_deposit_day=True,
                          target_leverage=1.25)
    assert d.repay_amount == pytest.approx(0.0)
    assert d.effective_leverage_cap == pytest.approx(1.25)


def test_r1_deposit_day_above_target_repays_exact_trim_funded_amount():
    state = _levered_state(1.8, net_equity=100.0)  # gross=180, debt=80
    d = r1_deposits_first(state, is_deposit_day=True, target_leverage=1.25)
    assert d.repay_amount == pytest.approx(180.0 - 1.25 * 100.0)  # 55.0
    assert d.effective_leverage_cap == pytest.approx(1.25)


def test_r1_boundary_exactly_at_target_plus_dead_band_does_not_repay():
    state = _levered_state(1.25, net_equity=100.0)
    d = r1_deposits_first(state, is_deposit_day=True, target_leverage=1.25,
                          dead_band=0.0)
    assert d.repay_amount == pytest.approx(0.0)


def test_r1_is_deposit_day_must_be_a_real_bool():
    with pytest.raises(TypeError):
        r1_deposits_first(_levered_state(1.5), is_deposit_day=1,
                          target_leverage=1.25)


# ── R2 — dividends first (T-D5 focus) ────────────────────────────────────────

def test_r2_debt_free_never_repays_dividend_reinvests():
    d = r2_dividends_first(DEBT_FREE, dividend_cash=50.0)
    assert d.repay_amount == pytest.approx(0.0)


def test_r2_partially_indebted_all_dividend_cash_pays_debt():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r2_dividends_first(state, dividend_cash=30.0)
    assert d.repay_amount == pytest.approx(30.0)


def test_r2_dividend_greater_than_debt_pays_exactly_the_debt():
    state = _ps(margin_debt=20.0, gross=120.0)
    d = r2_dividends_first(state, dividend_cash=50.0)
    assert d.repay_amount == pytest.approx(20.0)
    # the 30.0 remainder is never claimed by this decision -- it stays
    # ordinary cash for the caller to reinvest, satisfying "reinvested
    # only at debt = 0" without double counting.
    assert d.repay_amount < 50.0


def test_r2_reinvest_control_never_repays_regardless_of_debt():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r2_dividends_first(state, dividend_cash=30.0, reinvest=True)
    assert d.repay_amount == pytest.approx(0.0)


def test_r2_zero_dividend_is_a_no_op():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r2_dividends_first(state, dividend_cash=0.0)
    assert d == RepaymentDecision()


@pytest.mark.parametrize("margin_debt,dividend_cash", [
    (0.0, 0.0), (0.0, 25.0), (40.0, 0.0), (40.0, 10.0),
    (40.0, 40.0), (40.0, 100.0), (100.0, 1e6),
])
def test_r2_never_duplicates_or_loses_a_dollar(margin_debt, dividend_cash):
    state = _ps(margin_debt=margin_debt, gross=margin_debt + 100.0)
    d = r2_dividends_first(state, dividend_cash=dividend_cash)
    assert d.repay_amount <= dividend_cash
    assert d.repay_amount <= margin_debt


def test_r2_rejects_negative_dividend_cash():
    with pytest.raises(ValueError):
        r2_dividends_first(_ps(margin_debt=10.0), dividend_cash=-1.0)


def test_r2_rejects_non_finite_dividend_cash():
    with pytest.raises(ValueError):
        r2_dividends_first(_ps(margin_debt=10.0), dividend_cash=math.nan)
    with pytest.raises(ValueError):
        r2_dividends_first(_ps(margin_debt=10.0), dividend_cash=math.inf)


def test_r2_rejects_boolean_dividend_cash():
    with pytest.raises(TypeError):
        r2_dividends_first(_ps(margin_debt=10.0), dividend_cash=True)


# ── R3 — governed trims first ────────────────────────────────────────────────

def test_r3_trim_below_debt_pays_it_all_toward_debt():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r3_governed_trims_first(state, trim_proceeds=40.0)
    assert d.repay_amount == pytest.approx(40.0)


def test_r3_trim_above_debt_caps_at_outstanding_debt():
    state = _ps(margin_debt=40.0, gross=200.0)
    d = r3_governed_trims_first(state, trim_proceeds=100.0)
    assert d.repay_amount == pytest.approx(40.0)


def test_r3_debt_free_is_a_no_op():
    d = r3_governed_trims_first(DEBT_FREE, trim_proceeds=100.0)
    assert d.repay_amount == pytest.approx(0.0)


def test_r3_zero_proceeds_is_a_no_op():
    state = _ps(margin_debt=40.0, gross=200.0)
    d = r3_governed_trims_first(state, trim_proceeds=0.0)
    assert d == RepaymentDecision()


def test_r3_rejects_negative_proceeds():
    with pytest.raises(ValueError):
        r3_governed_trims_first(_ps(margin_debt=10.0), trim_proceeds=-1.0)


# ── R4 — borrowing-cost hurdle (boundary focus) ──────────────────────────────

def test_r4_at_exact_hurdle_boundary_does_not_trigger():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r4_borrowing_cost_hurdle(state, effective_apr=0.06, hurdle=0.06,
                                available_cash=50.0)
    assert d.repay_amount == pytest.approx(0.0)


def test_r4_epsilon_above_hurdle_triggers():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r4_borrowing_cost_hurdle(state, effective_apr=0.06 + 1e-9, hurdle=0.06,
                                available_cash=50.0)
    assert d.repay_amount == pytest.approx(50.0)


@pytest.mark.parametrize("hurdle", [0.06, 0.08])
def test_r4_both_registered_hurdle_values(hurdle):
    state = _ps(margin_debt=10.0, gross=200.0)
    below = r4_borrowing_cost_hurdle(state, effective_apr=hurdle - 0.01,
                                     hurdle=hurdle, available_cash=100.0)
    above = r4_borrowing_cost_hurdle(state, effective_apr=hurdle + 0.01,
                                     hurdle=hurdle, available_cash=100.0)
    assert below.repay_amount == pytest.approx(0.0)
    assert above.repay_amount == pytest.approx(10.0)


def test_r4_debt_free_never_triggers():
    d = r4_borrowing_cost_hurdle(DEBT_FREE, effective_apr=0.20, hurdle=0.06,
                                available_cash=50.0)
    assert d.repay_amount == pytest.approx(0.0)


def test_r4_zero_available_cash_is_a_no_op_even_above_hurdle():
    state = _ps(margin_debt=100.0, gross=200.0)
    d = r4_borrowing_cost_hurdle(state, effective_apr=0.20, hurdle=0.06,
                                available_cash=0.0)
    assert d.repay_amount == pytest.approx(0.0)


def test_r4_rejects_negative_apr():
    with pytest.raises(ValueError):
        r4_borrowing_cost_hurdle(_ps(margin_debt=10.0), effective_apr=-0.01,
                                 hurdle=0.06, available_cash=10.0)


# ── R5 — trend/vol deterioration (all four trigger combinations) ────────────

@pytest.mark.parametrize("trend_bad,vol_bad,expect_trigger", [
    (False, False, False),
    (True, False, True),
    (False, True, True),
    (True, True, True),
])
def test_r5_all_frozen_trigger_combinations(trend_bad, vol_bad, expect_trigger):
    state = _levered_state(1.5)
    d = r5_trend_vol_deterioration(state, trend_deteriorated=trend_bad,
                                   vol_deteriorated=vol_bad)
    if expect_trigger:
        assert d.repay_amount > 0.0
        assert d.effective_leverage_cap == pytest.approx(LEVERAGE_TARGET_HARD_MIN)
    else:
        assert d == RepaymentDecision()


def test_r5_repays_to_exactly_1_00x_when_triggered():
    state = _levered_state(1.6, net_equity=100.0)
    d = r5_trend_vol_deterioration(state, trend_deteriorated=True,
                                   vol_deteriorated=False)
    assert d.repay_amount == pytest.approx(60.0)  # (1.6 - 1.0) * 100


def test_r5_rejects_non_bool_flags():
    with pytest.raises(TypeError):
        r5_trend_vol_deterioration(_levered_state(1.5), trend_deteriorated=1,
                                   vol_deteriorated=False)


# ── R6 — maintenance-excess deterioration (staged weekly) ────────────────────

def test_r6_requires_floor_explicitly_no_default():
    with pytest.raises(TypeError):
        R6MaintenanceDeterioration(band_above_floor_pp=10.0,
                                   staged_fraction_per_week=0.25)


def test_r6_raises_when_maintenance_excess_is_none():
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=10.0,
                                    staged_fraction_per_week=0.25)
    with pytest.raises(ValueError):
        r6(_ps(margin_debt=100.0, gross=200.0, maintenance_excess=None))


def test_r6_excess_above_threshold_is_a_no_op():
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=10.0,
                                    staged_fraction_per_week=0.25)
    d = r6(_ps(margin_debt=100.0, gross=200.0, maintenance_excess=11.0))
    assert d == RepaymentDecision()


def test_r6_excess_exactly_at_threshold_does_not_trigger():
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=10.0,
                                    staged_fraction_per_week=0.25)
    d = r6(_ps(margin_debt=100.0, gross=200.0, maintenance_excess=10.0))
    assert d == RepaymentDecision()


def test_r6_debt_free_never_triggers_even_below_threshold():
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=10.0,
                                    staged_fraction_per_week=0.25)
    d = r6(_ps(margin_debt=0.0, gross=200.0, maintenance_excess=-50.0))
    assert d == RepaymentDecision()


def test_r6_stages_25_percent_of_current_shortfall_on_first_trigger():
    # threshold = floor(0) + band(100) = 100; excess=20 -> shortfall=80
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=100.0,
                                    staged_fraction_per_week=0.25)
    d = r6(_ps(day_index=0, margin_debt=1000.0, gross=2000.0,
              maintenance_excess=20.0))
    assert d.repay_amount == pytest.approx(0.25 * 80.0)  # 20.0


def test_r6_does_not_restage_within_the_same_week():
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=100.0,
                                    staged_fraction_per_week=0.25, week_days=7)
    first = r6(_ps(day_index=0, margin_debt=1000.0, gross=2000.0,
                  maintenance_excess=20.0))
    second = r6(_ps(day_index=3, margin_debt=1000.0, gross=2000.0,
                    maintenance_excess=20.0))
    assert first.repay_amount > 0.0
    assert second.repay_amount == pytest.approx(0.0)


def test_r6_restages_after_a_full_week_elapses():
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=100.0,
                                    staged_fraction_per_week=0.25, week_days=7)
    r6(_ps(day_index=0, margin_debt=1000.0, gross=2000.0, maintenance_excess=20.0))
    third_week = r6(_ps(day_index=7, margin_debt=1000.0, gross=2000.0,
                       maintenance_excess=30.0))
    assert third_week.repay_amount == pytest.approx(0.25 * (100.0 - 30.0))  # 17.5


def test_r6_two_fresh_instances_given_identical_call_sequences_are_identical():
    seq = [
        _ps(day_index=0, margin_debt=1000.0, gross=2000.0, maintenance_excess=20.0),
        _ps(day_index=3, margin_debt=1000.0, gross=2000.0, maintenance_excess=25.0),
        _ps(day_index=7, margin_debt=1000.0, gross=2000.0, maintenance_excess=30.0),
    ]
    r6_a = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=100.0,
                                      staged_fraction_per_week=0.25)
    r6_b = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=100.0,
                                      staged_fraction_per_week=0.25)
    results_a = [r6_a(s).repay_amount for s in seq]
    results_b = [r6_b(s).repay_amount for s in seq]
    assert results_a == results_b


def test_r6_rejects_staged_fraction_out_of_range():
    with pytest.raises(ValueError):
        R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=10.0,
                                   staged_fraction_per_week=1.5)


def test_r6_rejects_non_positive_week_days():
    with pytest.raises(ValueError):
        R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=10.0,
                                   staged_fraction_per_week=0.25, week_days=0)


# ── R7 — Intelligence advisory (Study D semantics only) ──────────────────────

def test_r7_inactive_flag_is_always_a_no_op_regardless_of_semantic():
    for semantic in IntelligenceAdvisorySemantic:
        d = r7_intelligence_advisory(_levered_state(1.8), semantic=semantic,
                                     flag_active=False, target_leverage=1.0)
        assert d == RepaymentDecision()


def test_r7_annotation_only_control_is_always_a_no_op_even_when_active():
    d = r7_intelligence_advisory(
        _levered_state(1.8), semantic=IntelligenceAdvisorySemantic.ANNOTATION_ONLY_CONTROL,
        flag_active=True)
    assert d == RepaymentDecision()


def test_r7_whole_cycle_draw_freeze_caps_at_current_leverage_no_repay():
    state = _levered_state(1.5)
    d = r7_intelligence_advisory(
        state, semantic=IntelligenceAdvisorySemantic.WHOLE_CYCLE_DRAW_FREEZE,
        flag_active=True)
    assert d.repay_amount == pytest.approx(0.0)
    assert d.effective_leverage_cap == pytest.approx(1.5)


def test_r7_whole_cycle_draw_freeze_with_no_leverage_defaults_to_1_00x_cap():
    state = _ps(gross=0.0, margin_debt=0.0)  # net_equity 0 -> leverage_ratio None
    d = r7_intelligence_advisory(
        state, semantic=IntelligenceAdvisorySemantic.WHOLE_CYCLE_DRAW_FREEZE,
        flag_active=True)
    assert d.effective_leverage_cap == pytest.approx(LEVERAGE_TARGET_HARD_MIN)


def test_r7_account_level_advisory_requires_explicit_target():
    with pytest.raises(ValueError):
        r7_intelligence_advisory(
            _levered_state(1.8),
            semantic=IntelligenceAdvisorySemantic.ACCOUNT_LEVEL_REPAYMENT_ADVISORY,
            flag_active=True)


def test_r7_account_level_advisory_matches_repay_to_target_arithmetic():
    state = _levered_state(1.8, net_equity=100.0)
    d = r7_intelligence_advisory(
        state, semantic=IntelligenceAdvisorySemantic.ACCOUNT_LEVEL_REPAYMENT_ADVISORY,
        flag_active=True, target_leverage=1.25)
    r8_equivalent = r8_restore_to_target_only(state, target_leverage=1.25)
    assert d.repay_amount == pytest.approx(r8_equivalent.repay_amount)


def test_r7_rejects_non_enum_semantic():
    with pytest.raises(TypeError):
        r7_intelligence_advisory(_levered_state(1.5), semantic="whole_cycle_draw_freeze",
                                 flag_active=True)


# ── R8 — restore-to-target-only ──────────────────────────────────────────────

def test_r8_never_repays_below_governed_target():
    state = _levered_state(1.1)  # already below the 1.25 target
    d = r8_restore_to_target_only(state, target_leverage=1.25)
    assert d.repay_amount == pytest.approx(0.0)
    assert d.effective_leverage_cap == pytest.approx(1.25)


def test_r8_repays_excess_above_target():
    state = _levered_state(1.8, net_equity=100.0)
    d = r8_restore_to_target_only(state, target_leverage=1.25)
    assert d.repay_amount == pytest.approx(55.0)


def test_r8_dead_band_absorbs_small_breaches():
    state = _levered_state(1.30, net_equity=100.0)
    d = r8_restore_to_target_only(state, target_leverage=1.25, dead_band=0.10)
    assert d.repay_amount == pytest.approx(0.0)


def test_r8_boundary_at_1_00x_and_1_80x():
    at_min = r8_restore_to_target_only(_levered_state(1.0), target_leverage=1.0)
    at_max = r8_restore_to_target_only(_levered_state(1.8), target_leverage=1.8)
    assert at_min.effective_leverage_cap == pytest.approx(1.0)
    assert at_max.effective_leverage_cap == pytest.approx(1.8)


# ── R9 — full repayment to 1.00x ─────────────────────────────────────────────

def test_r9_not_triggered_is_a_no_op():
    d = r9_full_repayment_to_unlevered(_levered_state(1.8), triggered=False)
    assert d == RepaymentDecision()


def test_r9_triggered_repays_exactly_the_outstanding_debt():
    state = _levered_state(1.6, net_equity=100.0)
    d = r9_full_repayment_to_unlevered(state, triggered=True)
    assert d.repay_amount == pytest.approx(state.margin_debt)
    assert d.effective_leverage_cap == pytest.approx(1.0)


def test_r9_triggered_but_debt_free_repays_nothing():
    d = r9_full_repayment_to_unlevered(DEBT_FREE, triggered=True)
    assert d.repay_amount == pytest.approx(0.0)


def test_r9_rejects_non_bool_triggered():
    with pytest.raises(TypeError):
        r9_full_repayment_to_unlevered(_levered_state(1.5), triggered=1)


# ── R-B — Model B profit-harvest reference ───────────────────────────────────

def test_rb_pins_the_registered_repay_fraction():
    rb = rb_model_b_profit_harvest()
    assert isinstance(rb, ModelBProfitHarvest)
    assert rb.repay_fraction == pytest.approx(MODEL_B_REFERENCE_REPAY_FRACTION)
    assert MODEL_B_REFERENCE_REPAY_FRACTION == pytest.approx(0.10)


def test_rb_returns_a_fresh_instance_every_call():
    a = rb_model_b_profit_harvest()
    b = rb_model_b_profit_harvest()
    assert a is not b
    a(_ps(day_index=0, gross=100.0, margin_debt=0.0), None)
    a(_ps(day_index=1, gross=150.0, margin_debt=0.0), None)  # new HWM on `a`
    # `b` has seen nothing -- its own first call still just seeds its HWM.
    first_call_b = b(_ps(day_index=0, gross=150.0, margin_debt=0.0), None)
    assert first_call_b.repay_amount == pytest.approx(0.0)


def test_rb_delegates_to_the_real_engine_formula_not_a_duplicate():
    # Construct the engine's own class directly with the same fraction and
    # confirm identical behavior across an identical call sequence --
    # proves delegation rather than a parallel reimplementation.
    reference = ModelBProfitHarvest(repay_fraction=MODEL_B_REFERENCE_REPAY_FRACTION)
    via_lib = rb_model_b_profit_harvest()
    seq = [
        _ps(day_index=0, gross=100.0, margin_debt=0.0),
        _ps(day_index=1, gross=150.0, margin_debt=40.0),
        _ps(day_index=2, gross=140.0, margin_debt=40.0),
        _ps(day_index=3, gross=200.0, margin_debt=40.0),
    ]
    for state in seq:
        a = reference(state, None)
        b = via_lib(state, None)
        assert a.repay_amount == pytest.approx(b.repay_amount)


# ── debt-free behavior sweep across every repay-style family ────────────────

def test_all_repay_style_families_are_inert_against_a_debt_free_account():
    assert r1_deposits_first(DEBT_FREE, is_deposit_day=True,
                             target_leverage=1.0).repay_amount == pytest.approx(0.0)
    assert r2_dividends_first(DEBT_FREE, dividend_cash=100.0).repay_amount == pytest.approx(0.0)
    assert r3_governed_trims_first(DEBT_FREE, trim_proceeds=100.0).repay_amount == pytest.approx(0.0)
    assert r4_borrowing_cost_hurdle(
        DEBT_FREE, effective_apr=0.5, hurdle=0.06,
        available_cash=100.0).repay_amount == pytest.approx(0.0)
    assert r5_trend_vol_deterioration(
        DEBT_FREE, trend_deteriorated=True, vol_deteriorated=True
    ).repay_amount == pytest.approx(0.0)
    r6 = R6MaintenanceDeterioration(floor=0.0, band_above_floor_pp=1000.0,
                                    staged_fraction_per_week=0.25)
    assert r6(PortfolioState(day_index=0, cash=0.0, positions={}, margin_debt=0.0,
                             gross=100.0, maintenance_excess=-500.0)
             ).repay_amount == pytest.approx(0.0)
    assert r8_restore_to_target_only(
        DEBT_FREE, target_leverage=1.0).repay_amount == pytest.approx(0.0)
    assert r9_full_repayment_to_unlevered(
        DEBT_FREE, triggered=True).repay_amount == pytest.approx(0.0)


# ── engine interoperability smoke tests (synthetic only, not a Study run) ──

def _tiny_synthetic_fixture():
    aligned = {
        "A": ([100.0, 100.0, 100.0, 100.0, 100.0], 0),
        "B": ([100.0, 100.0, 100.0, 100.0, 100.0], 0),
    }
    calendar = [f"2026-01-{d:02d}" for d in range(1, 6)]
    deposit_days = [calendar[0]]
    weights = {"A": 1.0, "B": 1.0}
    return aligned, calendar, deposit_days, weights


def test_r8_is_wired_compatible_with_simulate_as_a_pre_trade_fn():
    aligned, calendar, deposit_days, weights = _tiny_synthetic_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    sc.pre_trade_fn = functools.partial(r8_restore_to_target_only,
                                        target_leverage=1.25)
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=100.0, min_lot=1.0)
    for lr in result.leverage_series:
        if lr is not None:
            assert lr <= 1.25 + 1e-6


def test_rb_is_wired_compatible_with_simulate_as_a_pre_trade_fn():
    aligned, calendar, deposit_days, weights = _tiny_synthetic_fixture()
    sc = scenario_fixed_leverage(1.8, interest_apr=0.0, interest_free_amount=0.0)
    sc.pre_trade_fn = rb_model_b_profit_harvest()
    result = simulate(sc, weights, aligned, calendar, deposit_days,
                      deposit_amount=100.0, min_lot=1.0)
    assert result.final_margin_debt >= 0.0
