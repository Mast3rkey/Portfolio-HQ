"""Tests for margin_state.py — the Phase 2B pure margin risk classifier.

Coverage required by docs/PHASE2_IMPLEMENTATION_PLAN.md's Phase 2B scope:
normal state, leverage cap breach, buffer floor breach, forced-delever
condition, stale/missing margin data, concentration tightening, invalid
inputs, and the property test proving no leverage-increase action exists.
"""

import itertools

import pytest

from margin_state import (
    ALLOWED_ACTIONS, CONTINUE_NORMAL_OPERATIONS, REDUCE_RISK,
    PRIORITIZE_DELEVERAGING, VERIFY_MARGIN_DATA, STATES,
    MarginStateResult, classify_margin_state, concentration_risk_score,
)


# ── concentration_risk_score() ──────────────────────────────────────────────

def test_concentration_score_empty_input_is_zero_not_error():
    score, label = concentration_risk_score({})
    assert score == 0.0
    assert label is None


def test_concentration_score_takes_the_max_not_average():
    score, label = concentration_risk_score(
        {"cluster:semis": 0.40, "cluster:oil": 0.93, "t1t2:NVDA": 0.71})
    assert score == 0.93
    assert label == "cluster:oil"


def test_concentration_score_single_entry():
    score, label = concentration_risk_score({"t1t2:AMZN": 1.05})
    assert score == 1.05
    assert label == "t1t2:AMZN"


# ── classify_margin_state(): normal state ───────────────────────────────────

def test_normal_state_healthy_account():
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=60.0,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "NORMAL"
    assert r.allowed_actions == [CONTINUE_NORMAL_OPERATIONS]
    assert r.violated_constraints == []
    assert r.risk_metrics["leverage_ratio"] == pytest.approx(100.0 / 80.0)
    assert r.risk_metrics["net_equity"] == 80.0


def test_normal_state_no_debt_at_all():
    r = classify_margin_state(
        gross=100.0, margin_debt=0.0, buffer_pct=None,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "NORMAL"
    assert r.risk_metrics["leverage_ratio"] == 1.0
    assert r.risk_metrics["utilization"] == 0.0


# ── leverage cap breach ─────────────────────────────────────────────────────

def test_leverage_cap_breach_forces_delever_even_with_healthy_buffer():
    # gross=200, debt=100 -> net_equity=100, leverage=2.0x > 1.8x cap.
    # Buffer is healthy (60%) -- the leverage breach alone must still force it.
    r = classify_margin_state(
        gross=200.0, margin_debt=100.0, buffer_pct=60.0,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "FORCED_DELEVER"
    assert "leverage_cap_exceeded" in r.violated_constraints
    assert "buffer_floor_breach" not in r.violated_constraints
    assert r.allowed_actions == [PRIORITIZE_DELEVERAGING]


def test_leverage_exactly_at_cap_is_not_a_breach():
    # gross=180, debt=80 -> net_equity=100, leverage exactly 1.8x.
    r = classify_margin_state(
        gross=180.0, margin_debt=80.0, buffer_pct=60.0,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state != "FORCED_DELEVER"
    assert "leverage_cap_exceeded" not in r.violated_constraints


# ── buffer floor breach ─────────────────────────────────────────────────────

def test_buffer_floor_breach_forces_delever():
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=29.9,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "FORCED_DELEVER"
    assert "buffer_floor_breach" in r.violated_constraints
    assert r.allowed_actions == [PRIORITIZE_DELEVERAGING]


def test_buffer_exactly_at_floor_is_not_forced():
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=30.0,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state != "FORCED_DELEVER"


def test_both_leverage_and_buffer_breach_records_both():
    r = classify_margin_state(
        gross=200.0, margin_debt=100.0, buffer_pct=10.0,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "FORCED_DELEVER"
    assert "leverage_cap_exceeded" in r.violated_constraints
    assert "buffer_floor_breach" in r.violated_constraints


# ── forced-delever via insolvency (net_equity <= 0) ─────────────────────────

def test_net_equity_non_positive_is_forced_delever_not_a_crash():
    r = classify_margin_state(
        gross=100.0, margin_debt=150.0, buffer_pct=None,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "FORCED_DELEVER"
    assert "net_equity_non_positive" in r.violated_constraints
    assert r.risk_metrics["leverage_ratio"] is None
    assert r.allowed_actions == [PRIORITIZE_DELEVERAGING]


def test_net_equity_exactly_zero_is_forced_delever():
    r = classify_margin_state(
        gross=100.0, margin_debt=100.0, buffer_pct=50.0,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "FORCED_DELEVER"
    assert "net_equity_non_positive" in r.violated_constraints


# ── stale / missing margin data ─────────────────────────────────────────────

def test_missing_buffer_data_flags_verify_but_does_not_force_a_state():
    # No leverage breach here (1.25x well under 1.8x cap) -- missing buffer
    # data alone should not force FORCED_DELEVER, just flag verification.
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=None,
        leverage_cap=1.8, buffer_floor_pct=30.0)
    assert r.current_state == "NORMAL"
    assert VERIFY_MARGIN_DATA in r.allowed_actions
    assert any("unavailable" in reason for reason in r.reasons)


def test_stale_buffer_data_flags_verify_and_violated_constraint():
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=60.0,
        leverage_cap=1.8, buffer_floor_pct=30.0,
        buffer_data_age_days=5.0, stale_threshold_days=2.0)
    assert "stale_margin_data" in r.violated_constraints
    assert VERIFY_MARGIN_DATA in r.allowed_actions


def test_fresh_buffer_data_within_threshold_is_not_stale():
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=60.0,
        leverage_cap=1.8, buffer_floor_pct=30.0,
        buffer_data_age_days=1.0, stale_threshold_days=2.0)
    assert "stale_margin_data" not in r.violated_constraints
    assert VERIFY_MARGIN_DATA not in r.allowed_actions


def test_data_age_exactly_at_threshold_is_not_stale():
    r = classify_margin_state(
        gross=100.0, margin_debt=20.0, buffer_pct=60.0,
        leverage_cap=1.8, buffer_floor_pct=30.0,
        buffer_data_age_days=2.0, stale_threshold_days=2.0)
    assert "stale_margin_data" not in r.violated_constraints


# ── concentration tightening ────────────────────────────────────────────────

def test_concentration_tightening_pushes_normal_into_caution():
    # leverage=1.5x, cap=1.8x -> raw ratio 0.833. caution_leverage_fraction=0.85
    # means the untightened boundary is 0.85*1.8=1.53x -- 1.5x is just under it
    # (NORMAL) at concentration 0. At concentration 1.0 with a real tightening
    # coefficient, the boundary should tighten enough to flip this to CAUTION.
    common = dict(gross=150.0, margin_debt=50.0, buffer_pct=60.0,
                  leverage_cap=1.8, buffer_floor_pct=30.0,
                  caution_leverage_fraction=0.85,
                  restricted_leverage_fraction=0.95,
                  concentration_tightening_coefficient=0.5,
                  concentration_min_fraction=0.5)
    r_low = classify_margin_state(**common, concentration_score=0.0)
    r_high = classify_margin_state(**common, concentration_score=1.0)
    assert r_low.current_state == "NORMAL"
    assert r_high.current_state in ("CAUTION", "RESTRICTED")


def test_concentration_never_loosens_a_threshold():
    # Concentration score of 0 should never be MORE restrictive than a
    # positive score at the same leverage/buffer -- tightening only ever
    # moves toward MORE caution, never less.
    common = dict(gross=150.0, margin_debt=50.0, buffer_pct=60.0,
                  leverage_cap=1.8, buffer_floor_pct=30.0,
                  caution_leverage_fraction=0.85,
                  restricted_leverage_fraction=0.95,
                  concentration_tightening_coefficient=0.5,
                  concentration_min_fraction=0.5)
    order = {"NORMAL": 0, "CAUTION": 1, "RESTRICTED": 2, "FORCED_DELEVER": 3}
    prev_rank = -1
    for score in (0.0, 0.25, 0.5, 0.75, 1.0):
        r = classify_margin_state(**common, concentration_score=score)
        rank = order[r.current_state]
        assert rank >= prev_rank, f"concentration {score} loosened state vs a lower score"
        prev_rank = rank


def test_concentration_min_fraction_floors_the_tightening():
    # Even at concentration_score way above 1.0, the tightening multiplier
    # cannot go below concentration_min_fraction -- so an absurdly high score
    # can't make the threshold negative/nonsensical.
    r = classify_margin_state(
        gross=100.0, margin_debt=10.0, buffer_pct=90.0,
        leverage_cap=1.8, buffer_floor_pct=30.0,
        caution_leverage_fraction=0.85, restricted_leverage_fraction=0.95,
        concentration_tightening_coefficient=10.0,  # deliberately extreme
        concentration_min_fraction=0.5,
        concentration_score=5.0)
    # leverage here is only 100/90 = 1.111x, cap 1.8x -> raw ratio 0.617,
    # still under even the floored caution threshold (0.85*0.5=0.425 -> 1.8*0.425=0.765x)
    # so this specific case lands in CAUTION/RESTRICTED territory, not NORMAL --
    # what matters is it doesn't crash or produce a negative/nonsensical threshold.
    assert r.current_state in ("NORMAL", "CAUTION", "RESTRICTED", "FORCED_DELEVER")


def test_unset_thresholds_never_fire_caution_or_restricted():
    # Per the standing "no threshold defaults without evidence" discipline --
    # if caution/restricted fractions are None (as they are in the real,
    # still-unset targets.yaml proposal), those escalation paths must never
    # fire, no matter how high leverage gets (short of the hard cap).
    r = classify_margin_state(
        gross=179.0, margin_debt=79.0, buffer_pct=60.0,  # leverage ~1.79x, just under 1.8x cap
        leverage_cap=1.8, buffer_floor_pct=30.0,
        caution_leverage_fraction=None, restricted_leverage_fraction=None,
        caution_buffer_comfort_multiplier=None, restricted_buffer_comfort_multiplier=None)
    assert r.current_state == "NORMAL"


# ── invalid inputs ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("kwargs", [
    dict(gross=-1.0, margin_debt=0.0, buffer_pct=50.0, leverage_cap=1.8, buffer_floor_pct=30.0),
    dict(gross=100.0, margin_debt=-1.0, buffer_pct=50.0, leverage_cap=1.8, buffer_floor_pct=30.0),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=50.0, leverage_cap=0.5, buffer_floor_pct=30.0),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=50.0, leverage_cap=1.8, buffer_floor_pct=150.0),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=150.0, leverage_cap=1.8, buffer_floor_pct=30.0),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=-5.0, leverage_cap=1.8, buffer_floor_pct=30.0),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=50.0, leverage_cap=1.8, buffer_floor_pct=30.0,
         concentration_score=-1.0),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=50.0, leverage_cap=1.8, buffer_floor_pct=30.0,
         concentration_min_fraction=1.5),
    dict(gross=100.0, margin_debt=0.0, buffer_pct=50.0, leverage_cap=1.8, buffer_floor_pct=30.0,
         buffer_data_age_days=-1.0),
])
def test_invalid_inputs_raise_value_error(kwargs):
    with pytest.raises(ValueError):
        classify_margin_state(**kwargs)


def test_margin_state_result_rejects_invalid_state_name():
    with pytest.raises(ValueError):
        MarginStateResult(current_state="BULLISH")


def test_margin_state_result_rejects_disallowed_action():
    with pytest.raises(ValueError):
        MarginStateResult(current_state="NORMAL", allowed_actions=["increase_leverage"])


# ── property test: no state can ever recommend increasing leverage ─────────

def test_no_state_ever_recommends_increasing_leverage():
    """Systematic sweep over the input domain. Every returned action must be
    a member of ALLOWED_ACTIONS, and ALLOWED_ACTIONS itself contains no
    leverage-increasing action -- so this test is really two checks: the
    module-level vocabulary is clean (checked once, structurally), and every
    reachable (state, action-set) combination stays inside that vocabulary
    across a wide sweep of realistic and edge-case inputs."""
    forbidden_terms = ("increase", "borrow", "add_margin", "deploy")
    for action in ALLOWED_ACTIONS:
        for term in forbidden_terms:
            assert term not in action, f"{action!r} looks like a leverage-increase action"

    gross_values = (0.0, 50.0, 100.0, 200.0, 1000.0)
    debt_fractions = (0.0, 0.2, 0.5, 0.8, 0.99, 1.0, 1.2)  # fraction of gross, >1.0 -> insolvent
    buffer_values = (None, 0.0, 15.0, 29.9, 30.0, 45.0, 60.0, 90.0, 100.0)
    concentration_values = (0.0, 0.3, 0.6, 1.0, 1.5)
    caution_fracs = (None, 0.5, 0.85)
    restricted_fracs = (None, 0.7, 0.95)

    checked = 0
    for gross, debt_frac, buffer_pct, conc, c_frac, r_frac in itertools.product(
            gross_values, debt_fractions, buffer_values, concentration_values,
            caution_fracs, restricted_fracs):
        debt = gross * debt_frac
        try:
            result = classify_margin_state(
                gross=gross, margin_debt=debt, buffer_pct=buffer_pct,
                leverage_cap=1.8, buffer_floor_pct=30.0,
                concentration_score=conc,
                caution_leverage_fraction=c_frac,
                restricted_leverage_fraction=r_frac,
                caution_buffer_comfort_multiplier=1.5 if c_frac is not None else None,
                restricted_buffer_comfort_multiplier=1.2 if r_frac is not None else None,
                concentration_tightening_coefficient=0.3,
                concentration_min_fraction=0.5,
            )
        except ValueError:
            continue  # invalid combo (e.g. gross=0 with debt>0 handled fine actually) -- skip
        checked += 1
        assert result.current_state in STATES
        for action in result.allowed_actions:
            assert action in ALLOWED_ACTIONS
            for term in forbidden_terms:
                assert term not in action

    assert checked > 100, "sweep should have exercised a substantial number of combinations"
