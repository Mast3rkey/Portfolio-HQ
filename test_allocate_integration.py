"""Phase 2D integration tests: margin_state classification wired into
allocate.py's main()/render() around plan()'s existing output.

Scope: these tests cover exactly what Phase 2D added — a post-hoc
classify_margin_state() call after plan() returns, and a render() addition
nested inside the pre-existing margin-section gate. They do NOT re-test
plan()'s allocation math (test_margin.py already covers margin_capacity()
and the cluster/T1T2 trims) or margin_state.py's classifier internals
(test_margin_state.py already covers those in isolation).
"""

import copy

from allocate import build_roster, plan, render
from margin_state import (
    ALLOWED_ACTIONS,
    classify_margin_state,
    concentration_risk_score,
)


def _base_targets(t1t2_trim_mult=100.0):
    return {
        "tiers": {
            "T1": {"weight_pct": 20.0, "tickers": ["DDD"]},
            "T2": {"weight_pct": 5.0, "tickers": ["AAA"]},
        },
        "caps": {"clusters": [{"name": "semis", "pct": 10.0, "tickers": ["AAA"]}]},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7, "trim_rsi": 60,
                 "t1t2_trim_mult": t1t2_trim_mult},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def _flat_metrics(tickers, rsi=50):
    return {t: {"price": 100.0, "rsi14": rsi, "sma200": 90.0} for t in tickers}


def _attach_margin_state(result, targets):
    """Reproduces exactly the block added to allocate.py's main() after
    plan() returns — kept in one place so tests exercise the real
    composition (concentration_risk_score -> classify_margin_state) rather
    than a paraphrase of it."""
    cluster_proximities = {
        f"cluster:{c['name']}": c["value"] / (result["book"] * c["pct"] / 100.0)
        for c in result.get("clusters", [])
        if c["pct"] > 0 and result["book"] > 0
    }
    score, source = concentration_risk_score(cluster_proximities)
    margin_cfg = targets.get("margin", {}) or {}
    result["margin_state"] = classify_margin_state(
        gross=result["margin"]["gross"],
        margin_debt=result["margin"]["debt"],
        buffer_pct=result["margin"]["buffer_pct"],
        leverage_cap=result["margin"]["leverage_cap"],
        buffer_floor_pct=result["margin"]["buffer_floor_pct"],
        concentration_score=score,
        concentration_source=source,
        caution_leverage_fraction=margin_cfg.get("states", {}).get("caution", {}).get("leverage_fraction_of_cap"),
        restricted_leverage_fraction=margin_cfg.get("states", {}).get("restricted", {}).get("leverage_fraction_of_cap"),
        caution_buffer_comfort_multiplier=margin_cfg.get("states", {}).get("caution", {}).get("buffer_comfort_multiplier"),
        restricted_buffer_comfort_multiplier=margin_cfg.get("states", {}).get("restricted", {}).get("buffer_comfort_multiplier"),
        concentration_tightening_coefficient=margin_cfg.get("concentration_adjustment", {}).get("tightening_coefficient") or 0.0,
        concentration_min_fraction=margin_cfg.get("concentration_adjustment", {}).get("min_fraction") or 0.5,
    )
    return result


# ── no-margin report stays byte-identical ───────────────────────────────────

def test_no_debt_no_request_render_unchanged_by_margin_state_presence():
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result_plain = plan(targets, holdings, roster, metrics, True, True, cash=0.0)
    out_plain = render(copy.deepcopy(result_plain), review=True)

    result_with_ms = _attach_margin_state(copy.deepcopy(result_plain), targets)
    out_with_ms = render(result_with_ms, review=True)

    assert result_plain["margin"]["debt"] == 0.0
    assert result_plain["margin"]["requested"] == 0.0
    assert out_plain == out_with_ms
    assert "Margin risk state" not in out_plain
    assert "## Margin" not in out_plain


# ── margin report includes state information when margin is active ────────

def test_margin_active_report_includes_state_block():
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                  margin_debt=100.0, margin_buffer_pct=80.0)
    result = _attach_margin_state(result, targets)
    out = render(result, review=True)

    assert "## Margin" in out
    assert "Margin risk state:" in out
    ms = result["margin_state"]
    assert ms.current_state in ("NORMAL", "CAUTION", "RESTRICTED", "FORCED_DELEVER")
    assert f"Margin risk state: {ms.current_state}" in out
    assert "Allowed actions:" in out
    for action in ms.allowed_actions:
        assert action in out


def test_forced_delever_state_surfaces_reasons_and_constraints():
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    # buffer below floor -> plan()'s own forced_delever path AND
    # classify_margin_state()'s independent FORCED_DELEVER path should agree.
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                  margin_debt=100.0, margin_buffer_pct=10.0)
    result = _attach_margin_state(result, targets)
    out = render(result, review=True)

    assert result["margin"]["forced_delever"] is True
    assert result["margin_state"].current_state == "FORCED_DELEVER"
    assert "Margin risk state: FORCED_DELEVER" in out
    assert "Violated constraints:" in out
    assert "buffer_floor_breach" in out


# ── no output ever recommends increasing leverage ──────────────────────────

def test_allowed_actions_vocabulary_contains_no_leverage_increase():
    # Static check on the entire action vocabulary margin_state.py can ever
    # emit -- if this passes, no render() output built from it can either.
    forbidden_terms = ("increase_leverage", "borrow_more", "lever_up", "add_margin")
    for action in ALLOWED_ACTIONS:
        for term in forbidden_terms:
            assert term not in action, f"{action!r} looks like a leverage-increase action"


def test_normal_state_render_contains_no_leverage_increase_language():
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                  margin_debt=10.0, margin_buffer_pct=90.0)
    result = _attach_margin_state(result, targets)
    out = render(result, review=True)

    for phrase in ("increase leverage", "borrow more", "lever up", "add margin"):
        assert phrase not in out.lower()


# ── margin_state cannot alter allocation ────────────────────────────────────

def test_margin_state_classification_does_not_mutate_plan_output():
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                  margin_debt=100.0, margin_buffer_pct=50.0)
    before = copy.deepcopy(result)

    _attach_margin_state(result, targets)

    # Every key plan() itself produced is untouched; margin_state is purely additive.
    for key in before:
        assert result[key] == before[key], f"plan() output key {key!r} changed"
    assert set(result.keys()) - set(before.keys()) == {"margin_state"}


def test_margin_state_computed_strictly_after_plan_cannot_influence_buys():
    # Two runs with identical plan() inputs but different downstream
    # concentration/margin config: buys/trims must be identical, since
    # classify_margin_state() is only ever called after plan() returns.
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result_a = plan(targets, holdings, roster, metrics, True, True, cash=500.0,
                    margin_debt=100.0, margin_buffer_pct=50.0)
    result_b = plan(targets, holdings, roster, metrics, True, True, cash=500.0,
                    margin_debt=100.0, margin_buffer_pct=50.0)

    _attach_margin_state(result_a, {**targets, "margin": {**targets["margin"],
                         "concentration_adjustment": {"tightening_coefficient": 5.0, "min_fraction": 0.1}}})
    _attach_margin_state(result_b, targets)

    assert result_a["buys"] == result_b["buys"]
    assert result_a["trims"] == result_b["trims"]
    assert result_a["blocked"] == result_b["blocked"]
    assert result_a["cash_left"] == result_b["cash_left"]
