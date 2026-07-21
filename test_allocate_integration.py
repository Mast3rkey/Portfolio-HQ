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
import sys
from datetime import date, timedelta

import pytest
import yaml

import allocate
from allocate import build_roster, plan, render, render_health
from margin_state import (
    ALLOWED_ACTIONS,
    VERIFY_MARGIN_DATA,
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


def _attach_margin_state(result, targets, buffer_data_age_days=None, stale_threshold_days=2.0,
                         buffer_data_unverifiable=False):
    """Reproduces exactly the block added to allocate.py's main() after
    plan() returns — kept in one place so tests exercise the real
    composition (concentration_risk_score -> classify_margin_state) rather
    than a paraphrase of it. Reads plan()'s own `ratio_to_cap` field (added
    for the Health View) rather than recomputing value/(book*pct/100) a
    second time — mirrors main()'s current wiring exactly. `buffer_data_age_days`
    /`buffer_data_unverifiable` mirror main()'s _margin_buffer_age_days()/
    _margin_buffer_age_unverifiable(margin.synced_at) wiring."""
    cluster_proximities = {
        f"cluster:{c['name']}": c["ratio_to_cap"]
        for c in result.get("clusters", [])
        if c.get("ratio_to_cap") is not None
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
        buffer_data_age_days=buffer_data_age_days,
        stale_threshold_days=stale_threshold_days,
        buffer_data_unverifiable=buffer_data_unverifiable,
        caution_leverage_fraction=margin_cfg.get("states", {}).get("caution", {}).get("leverage_fraction_of_cap"),
        restricted_leverage_fraction=margin_cfg.get("states", {}).get("restricted", {}).get("leverage_fraction_of_cap"),
        caution_buffer_comfort_multiplier=margin_cfg.get("states", {}).get("caution", {}).get("buffer_comfort_multiplier"),
        restricted_buffer_comfort_multiplier=margin_cfg.get("states", {}).get("restricted", {}).get("buffer_comfort_multiplier"),
        concentration_tightening_coefficient=margin_cfg.get("concentration_adjustment", {}).get("tightening_coefficient") or 0.0,
        concentration_min_fraction=(
            0.5 if margin_cfg.get("concentration_adjustment", {}).get("min_fraction") is None
            else margin_cfg.get("concentration_adjustment", {})["min_fraction"]),
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


# ── Health View V1: plan() cluster contract (current_pct / ratio_to_cap) ───

def _padded_cluster_targets(cap_pct, t1t2_trim_mult=100.0, weight_pct=10.0):
    return {
        "tiers": {"T1": {"weight_pct": weight_pct, "tickers": ["CLU"]}},
        "caps": {"clusters": [{"name": "testcluster", "pct": cap_pct, "tickers": ["CLU"]}]},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7, "trim_rsi": 60,
                 "t1t2_trim_mult": t1t2_trim_mult},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def test_cluster_below_cap_ratio_and_pct():
    targets = _padded_cluster_targets(cap_pct=20.0)
    roster = build_roster(targets)
    # book = 1000 exactly (CLU 100 + PAD 900, cash/debt both 0)
    holdings = {"CLU": 100.0, "PAD": 900.0}
    metrics = _flat_metrics(["CLU"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert result["book"] == 1000.0
    c = result["clusters"][0]
    assert c["value"] == 100.0
    assert c["current_pct"] == 10.0
    assert c["ratio_to_cap"] == 0.5      # 100 / (1000 * 20%) = 0.5x, below cap
    assert result["trims"] == []        # excess < min_lot -> no mechanical trim


def test_cluster_exactly_at_cap():
    targets = _padded_cluster_targets(cap_pct=20.0)
    roster = build_roster(targets)
    holdings = {"CLU": 200.0, "PAD": 800.0}   # book=1000, cap_dollars=200
    metrics = _flat_metrics(["CLU"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    c = result["clusters"][0]
    assert c["current_pct"] == 20.0
    assert c["ratio_to_cap"] == 1.0
    assert result["trims"] == []        # excess == 0 < min_lot -> no trim


def test_cluster_over_cap_ratio_persists_when_name_already_trimmed_to_own_target():
    # Cluster cap (5%) tighter than the name's own T1 tier weight (10%): even
    # after the T1/T2 ceiling trims CLU down to its own target, that target
    # alone still exceeds the cluster cap, and the cluster-cap mechanism
    # cannot trim a name below its own target -- so the cluster stays
    # genuinely over cap in plan()'s output. Real, reachable config shape,
    # not a fabricated edge case.
    targets = _padded_cluster_targets(cap_pct=5.0, t1t2_trim_mult=1.5, weight_pct=10.0)
    roster = build_roster(targets)
    holdings = {"CLU": 200.0, "PAD": 800.0}   # book=1000, CLU target=100, ceiling=150
    metrics = _flat_metrics(["CLU"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert any(t["ticker"] == "CLU" for t in result["trims"])   # T1/T2 ceiling fired
    c = result["clusters"][0]
    assert c["value"] == 100.0          # trimmed down to CLU's own target, not below
    assert c["current_pct"] == 10.0
    assert c["ratio_to_cap"] == 2.0      # 100 / (1000 * 5%) = 2.0x, still over cap


def test_cluster_ratio_to_cap_none_on_zero_pct():
    targets = _padded_cluster_targets(cap_pct=0.0)
    roster = build_roster(targets)
    holdings = {"CLU": 50.0, "PAD": 950.0}
    metrics = _flat_metrics(["CLU"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    c = result["clusters"][0]
    assert result["book"] > 0
    assert c["current_pct"] == 5.0        # book > 0 -> still computed
    assert c["ratio_to_cap"] is None      # pct <= 0 -> guarded, not fabricated


def test_cluster_current_pct_and_ratio_none_on_zero_book():
    targets = _padded_cluster_targets(cap_pct=20.0)
    roster = build_roster(targets)
    result = plan(targets, {}, roster, {}, True, True, cash=0.0)  # empty holdings -> book 0

    assert result["book"] == 0.0
    c = result["clusters"][0]
    assert c["current_pct"] is None
    assert c["ratio_to_cap"] is None


def test_main_cluster_proximities_reads_ratio_to_cap_not_recomputed():
    # _attach_margin_state (this test file's mirror of main()'s real block)
    # now reads c["ratio_to_cap"] directly. Confirm it matches plan()'s own
    # field value exactly, i.e. there is exactly one formula, owned by plan().
    targets = _padded_cluster_targets(cap_pct=20.0)
    roster = build_roster(targets)
    holdings = {"CLU": 100.0, "PAD": 900.0}
    metrics = _flat_metrics(["CLU"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)
    result = _attach_margin_state(result, targets)

    expected_ratio = result["clusters"][0]["ratio_to_cap"]
    assert result["margin_state"].risk_metrics.get("concentration_score") == expected_ratio


# ── Health View V1: plan() crypto_sleeve contract ──────────────────────────

def _crypto_targets(sleeve_pct=10.0):
    return {
        "tiers": {},
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7, "trim_rsi": 60, "t1t2_trim_mult": 1.5},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {"coins": ["ETH", "SOL"], "sleeve_pct": sleeve_pct},
    }


def test_crypto_sleeve_below_target_gap_at_least_min_lot():
    targets = _crypto_targets()
    roster = build_roster(targets)
    holdings = {"ETH": 30.0, "SOL": 20.0, "PAD": 950.0}   # sleeve=50, book=1000, target=100
    result = plan(targets, holdings, roster, {}, True, True, cash=0.0)

    cs = result["crypto_sleeve"]
    assert cs == {"current": 50.0, "current_pct": 5.0, "target_pct": 10.0, "drift": 50.0}
    assert any(u["ticker"] == "CRYPTO" for u in result["underweight"])  # gap 50 >= min_lot 25


def test_crypto_sleeve_below_target_gap_below_min_lot():
    targets = _crypto_targets()
    roster = build_roster(targets)
    holdings = {"ETH": 50.0, "SOL": 35.0, "PAD": 915.0}   # sleeve=85, book=1000, target=100
    result = plan(targets, holdings, roster, {}, True, True, cash=0.0)

    cs = result["crypto_sleeve"]
    assert cs["current"] == 85.0
    assert cs["drift"] == 15.0    # under target, but gap (15) < min_lot (25)
    assert not any(u["ticker"] == "CRYPTO" for u in result["underweight"])


def test_crypto_sleeve_exactly_at_target():
    targets = _crypto_targets()
    roster = build_roster(targets)
    holdings = {"ETH": 60.0, "SOL": 40.0, "PAD": 900.0}   # sleeve=100, book=1000, target=100
    result = plan(targets, holdings, roster, {}, True, True, cash=0.0)

    cs = result["crypto_sleeve"]
    assert cs["drift"] == 0.0
    assert not any(u["ticker"] == "CRYPTO" for u in result["underweight"])


def test_crypto_sleeve_above_target():
    targets = _crypto_targets()
    roster = build_roster(targets)
    holdings = {"ETH": 90.0, "SOL": 60.0, "PAD": 850.0}   # sleeve=150, book=1000, target=100
    result = plan(targets, holdings, roster, {}, True, True, cash=0.0)

    cs = result["crypto_sleeve"]
    assert cs["current"] == 150.0
    assert cs["current_pct"] == 15.0
    assert cs["drift"] == -50.0   # signed negative = over target
    assert not any(u["ticker"] == "CRYPTO" for u in result["underweight"])


def test_crypto_sleeve_accurate_independent_of_underweight_recommendation():
    # Same sleeve state, two different min_lot thresholds -> the recommendation
    # list (underweight) differs, but crypto_sleeve's own numbers must not.
    holdings = {"ETH": 50.0, "SOL": 35.0, "PAD": 915.0}   # sleeve=85, book=1000, gap=15
    targets_a = _crypto_targets()
    targets_a["gates"]["min_lot_dollars"] = 25    # gap (15) < min_lot -> no CRYPTO row
    targets_b = _crypto_targets()
    targets_b["gates"]["min_lot_dollars"] = 10    # gap (15) >= min_lot -> CRYPTO row appears

    roster = build_roster(targets_a)
    result_a = plan(targets_a, holdings, roster, {}, True, True, cash=0.0)
    result_b = plan(targets_b, holdings, roster, {}, True, True, cash=0.0)

    assert result_a["crypto_sleeve"] == result_b["crypto_sleeve"]
    assert not any(u["ticker"] == "CRYPTO" for u in result_a["underweight"])
    assert any(u["ticker"] == "CRYPTO" for u in result_b["underweight"])


def test_crypto_sleeve_none_when_not_configured():
    targets = _base_targets()   # crypto: {} -- no coins/sleeve_pct configured
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert result["crypto_sleeve"] is None
    assert result["crypto_sleeve_pct"] is None


# ── NUM-0001 P1-3: single canonical crypto.sleeve_pct resolution ───────────
# plan() previously defaulted a missing sleeve_pct to 0 while main()'s result/
# Health-View metadata defaulted the identical key to 10 -- two independent
# fallbacks for one config value. Now there is exactly one resolution
# (`_resolve_crypto_sleeve_pct`), surfaced in the result as
# `crypto_sleeve_pct`, which both plan()'s own gap math and main()'s rendered
# `result["crypto"]["sleeve_pct"]` field read from.

def test_crypto_sleeve_pct_custom_value_used_consistently():
    targets = _crypto_targets(sleeve_pct=17.5)   # deliberately not 10.0 or 0
    roster = build_roster(targets)
    holdings = {"ETH": 60.0, "SOL": 40.0, "PAD": 900.0}   # sleeve=100, book=1000
    result = plan(targets, holdings, roster, {}, True, True, cash=0.0)

    assert result["crypto_sleeve_pct"] == 17.5
    assert result["crypto_sleeve"]["target_pct"] == 17.5   # same resolved value


def test_crypto_sleeve_pct_missing_with_coins_configured_fails_clearly():
    targets = _crypto_targets()
    del targets["crypto"]["sleeve_pct"]
    roster = build_roster(targets)
    holdings = {"ETH": 30.0, "SOL": 20.0}

    with pytest.raises(ValueError, match="sleeve_pct"):
        plan(targets, holdings, roster, {}, True, True, cash=0.0)


def test_crypto_sleeve_pct_non_numeric_fails_clearly():
    targets = _crypto_targets(sleeve_pct="lots")
    roster = build_roster(targets)
    holdings = {"ETH": 30.0, "SOL": 20.0}

    with pytest.raises(ValueError, match="not numeric"):
        plan(targets, holdings, roster, {}, True, True, cash=0.0)


def test_crypto_sleeve_disabled_no_coins_configured_no_error():
    targets = _base_targets()   # crypto: {} -- sleeve genuinely absent/disabled
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert result["crypto_sleeve"] is None
    assert result["crypto_sleeve_pct"] is None


# ── NUM-0001 P1-4: concentration_min_fraction must preserve explicit 0.0 ───
# main()'s `concentration_cfg.get("min_fraction") or 0.5` idiom discarded an
# explicitly configured 0.0 (falsy in Python). `_attach_margin_state` above
# has been updated to mirror the fixed wiring; these tests spy on
# classify_margin_state() to prove the exact kwarg value that reaches it.

def _capture_classify_kwargs(monkeypatch):
    captured = {}
    real = classify_margin_state

    def spy(**kwargs):
        captured.update(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(sys.modules[__name__], "classify_margin_state", spy)
    return captured


def test_concentration_min_fraction_explicit_zero_passes_through_unchanged(monkeypatch):
    captured = _capture_classify_kwargs(monkeypatch)
    targets = _base_targets()
    targets["margin"]["concentration_adjustment"] = {"min_fraction": 0.0}
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    _attach_margin_state(result, targets)

    assert captured["concentration_min_fraction"] == 0.0


def test_concentration_min_fraction_absent_defaults_to_half(monkeypatch):
    captured = _capture_classify_kwargs(monkeypatch)
    targets = _base_targets()   # no concentration_adjustment block at all
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    _attach_margin_state(result, targets)

    assert captured["concentration_min_fraction"] == 0.5


# ── Health View V1: plan() t1t2_proximity contract ─────────────────────────

def _t1t2_proximity_targets(t1t2_trim_mult=1.5):
    return {
        "tiers": {"T1": {"weight_pct": 10.0, "tickers": ["NEUT", "OVER", "UNDER"]}},
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7, "trim_rsi": 60,
                 "t1t2_trim_mult": t1t2_trim_mult},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def test_t1t2_neutral_zone_name_retained_though_invisible_elsewhere():
    targets = _t1t2_proximity_targets()
    roster = build_roster(targets)
    # book=1000 (100+200+50+650 PAD); NEUT target=100, current=130 -> 1.3x,
    # under the 1.5x ceiling (not trimmed) and gap=-30 (not a buy candidate) --
    # previously fell through plan() entirely.
    holdings = {"NEUT": 130.0, "OVER": 200.0, "UNDER": 50.0, "PAD": 620.0}
    metrics = _flat_metrics(["NEUT", "OVER", "UNDER"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert not any(t["ticker"] == "NEUT" for t in result["trims"])
    assert not any(u["ticker"] == "NEUT" for u in result["underweight"])
    assert not any(b["ticker"] == "NEUT" for b in result["blocked"])
    neut = next(p for p in result["t1t2_proximity"] if p["ticker"] == "NEUT")
    assert neut["current"] == 130.0
    assert neut["target"] == 100.0
    assert neut["ratio_to_target"] == pytest.approx(1.3)
    assert neut["ceiling_mult"] == 1.5
    assert neut["ratio_to_ceiling"] == pytest.approx(130.0 / 150.0)


def test_t1t2_over_ceiling_name_also_retained():
    targets = _t1t2_proximity_targets()
    roster = build_roster(targets)
    holdings = {"NEUT": 130.0, "OVER": 200.0, "UNDER": 50.0, "PAD": 620.0}
    metrics = _flat_metrics(["NEUT", "OVER", "UNDER"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    trimmed = next(t for t in result["trims"] if t["ticker"] == "OVER")
    assert trimmed["dollars"] == 100.0   # 200 - target(100)
    over = next(p for p in result["t1t2_proximity"] if p["ticker"] == "OVER")
    assert over["ratio_to_target"] == pytest.approx(2.0)
    assert over["ratio_to_ceiling"] == pytest.approx(200.0 / 150.0)


def test_every_t1t2_ticker_appears_exactly_once_regardless_of_outcome():
    targets = _t1t2_proximity_targets()
    roster = build_roster(targets)
    holdings = {"NEUT": 130.0, "OVER": 200.0, "UNDER": 50.0, "PAD": 620.0}
    # UNDER has no metrics entry -> price is None -> BLOCKED "no-data", which
    # happens strictly before the earnings-gate lookup (no network call).
    metrics = _flat_metrics(["NEUT", "OVER"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    tickers = [p["ticker"] for p in result["t1t2_proximity"]]
    assert sorted(tickers) == ["NEUT", "OVER", "UNDER"]
    assert len(tickers) == len(set(tickers))
    assert any(b["ticker"] == "UNDER" and "no-data" in b["reason"] for b in result["blocked"])
    assert any(t["ticker"] == "OVER" for t in result["trims"])
    assert not any(t["ticker"] == "NEUT" for t in result["trims"] + result["blocked"])


def test_t1t2_zero_target_retains_record_with_none_ratios():
    # book == 0 (empty holdings, no cash/margin) -> every target is 0. A real,
    # reachable state (a wiped/new book), not invented -- see build_roster()'s
    # weight_pct default and margin_capacity()'s own "if net_equity > 0 else
    # None" guard for the repo's established convention on this exact shape
    # of divide-by-zero.
    targets = {
        "tiers": {"T1": {"weight_pct": 10.0, "tickers": ["ZT"]}},
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7, "trim_rsi": 60, "t1t2_trim_mult": 1.5},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }
    roster = build_roster(targets)
    result = plan(targets, {}, roster, {}, True, True, cash=0.0)

    assert result["book"] == 0.0
    zt = next(p for p in result["t1t2_proximity"] if p["ticker"] == "ZT")
    assert zt["current"] == 0.0
    assert zt["target"] == 0.0
    assert zt["ratio_to_target"] is None
    assert zt["ratio_to_ceiling"] is None


# ── Health View V1: render_health() ────────────────────────────────────────

def _health_fixture_result(margin_state_obj="omit"):
    """A hand-built result dict -- no plan()/live client/YAML involved -- to
    prove render_health() is a pure function of `result` alone."""
    result = {
        "book": 1000.0,
        "margin": {
            "gross": 1200.0, "net_equity": 1000.0, "debt": 200.0,
            "buffer_pct": 55.0, "buffer_floor_pct": 30.0,
            "leverage_current": 1.2, "leverage_cap": 1.8,
            "requested": 0.0, "allowed": 0.0, "used": 0.0,
            "forced_delever": False, "block_reason": None,
        },
        "clusters": [
            {"name": "semis", "value": 180.0, "pct": 20.0,
             "current_pct": 18.0, "ratio_to_cap": 0.9},
        ],
        "crypto_sleeve": {"current": 85.0, "current_pct": 8.5,
                          "target_pct": 10.0, "drift": 15.0},
        "t1t2_proximity": [
            {"ticker": "NEUT", "tier": "T1", "current": 130.0, "target": 100.0,
             "ratio_to_target": 1.3, "ceiling_mult": 1.5, "ratio_to_ceiling": 130 / 150},
        ],
    }
    if margin_state_obj != "omit":
        result["margin_state"] = margin_state_obj
    return result


def test_render_health_consumes_hand_built_fixture():
    result = _health_fixture_result(margin_state_obj=None)
    out = render_health(result)
    assert isinstance(out, str) and len(out) > 0


def test_render_health_absent_margin_state_renders_unavailable_marker():
    result = _health_fixture_result(margin_state_obj="omit")
    assert "margin_state" not in result
    out = render_health(result)
    assert "UNAVAILABLE" in out
    assert "Margin risk state" in out


def test_render_health_all_required_sections_and_values_present():
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                  margin_debt=100.0, margin_buffer_pct=50.0)
    result = _attach_margin_state(result, targets)
    out = render_health(result)

    assert "## Margin" in out
    assert "## Margin risk state" in out
    assert "## Clusters" in out
    assert "## Crypto sleeve" in out
    assert "## T1/T2 proximity" in out
    assert f"{result['margin']['leverage_cap']:.2f}x cap" in out
    assert f"{result['margin']['buffer_floor_pct']:.0f}% floor" in out
    for c in result["clusters"]:
        assert c["name"] in out
    for t in result["t1t2_proximity"]:
        assert t["ticker"] in out


def test_render_health_does_not_mutate_result():
    result = _health_fixture_result(margin_state_obj=None)
    before = copy.deepcopy(result)
    render_health(result)
    assert result == before


def test_render_health_repeated_calls_identical_output():
    result = _health_fixture_result(margin_state_obj=None)
    out1 = render_health(result)
    out2 = render_health(result)
    assert out1 == out2


# ── Health View V1: unsynced buffer (buffer_pct is None) ──────────────────

def test_render_health_unsynced_buffer_labeled_not_hidden_as_normal():
    # buffer_pct=None is the real "never synced" shape resolve_holdings/
    # margin_state.py already handle elsewhere -- render_health must not
    # crash, must not print the literal "None%", and must not let the
    # absence of data read as a clean/adequate buffer.
    result = _health_fixture_result(margin_state_obj=None)
    result["margin"]["buffer_pct"] = None
    out = render_health(result)

    assert "None%" not in out
    assert "unsynced" in out
    floor = result["margin"]["buffer_floor_pct"]
    assert f"{floor:.0f}% floor" in out   # the floor itself still renders
    assert "Advisory only. This tool places no orders." in out


# ── Health View V1: CLI path (argparse -> --health -> render_health) ──────

def _cli_targets_and_holdings(tmp_path):
    targets_file = tmp_path / "targets.yaml"
    holdings_file = tmp_path / "holdings.yaml"
    with targets_file.open("w") as f:
        yaml.safe_dump({
            "tiers": {"T1": {"weight_pct": 10.0, "tickers": ["AAA"]}},
            "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7, "trim_rsi": 60,
                     "t1t2_trim_mult": 1.5},
            "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
            "crypto": {},
        }, f)
    with holdings_file.open("w") as f:
        yaml.safe_dump({
            "holdings": {}, "shares": {"AAA": 10.0}, "crypto_shares": {},
            "margin": {"debt": 100.0, "buffer_pct": 50.0, "synced_at": "2026-07-18"},
        }, f)
    return targets_file, holdings_file


def test_health_flag_cli_path_is_read_only(tmp_path, monkeypatch, capsys):
    """Exercises the actual command line path -- argparse -> --health ->
    observational cash/margin handling -> plan() -> render_health() -> print
    -- not just plan()/render_health() called directly, the way the other
    Health View tests do. No real network call: client construction and
    every live-data fetch are replaced with local, no-network fakes; only
    plan() and classify_margin_state() (both pure, already covered by their
    own test suites) run for real, so this test observes the genuine
    composition rather than a paraphrase of it."""
    targets_file, holdings_file = _cli_targets_and_holdings(tmp_path)
    monkeypatch.setattr(allocate, "TARGETS_FILE", targets_file)
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", holdings_file)

    monkeypatch.setattr(allocate, "AlpacaPaperClient", lambda: object())
    monkeypatch.setattr(
        allocate, "fetch_market",
        lambda client, tickers, regime_ticker: (
            {"AAA": {"price": 100.0, "rsi14": 50.0, "sma200": 90.0}}, True, True))
    monkeypatch.setattr(
        allocate, "resolve_holdings",
        lambda client, metrics=None, crypto_prices=None: {"AAA": 1000.0})

    def _forbidden(name):
        def _raise(*a, **k):
            raise AssertionError(f"{name} must not be invoked by --health")
        return _raise

    # No update-* subcommand and no other state-writing entry point may fire.
    for fn in ("update_holdings", "update_shares", "update_crypto_shares",
              "update_margin", "log_performance"):
        monkeypatch.setattr(allocate, fn, _forbidden(fn))
    # The standard allocation report must not be produced in its place.
    monkeypatch.setattr(allocate, "render", _forbidden("render (the standard report)"))

    plan_calls = []
    real_plan = allocate.plan

    def _spy_plan(*args, **kwargs):
        plan_calls.append({"cash": args[6], **kwargs})
        return real_plan(*args, **kwargs)
    monkeypatch.setattr(allocate, "plan", _spy_plan)

    render_health_calls = []
    def _spy_render_health(result):
        render_health_calls.append(result)
        return "SENTINEL_HEALTH_VIEW_OUTPUT"
    monkeypatch.setattr(allocate, "render_health", _spy_render_health)

    monkeypatch.setattr(sys, "argv", ["allocate.py", "--health"])

    allocate.main()   # must complete without raising or sys.exit()

    out = capsys.readouterr().out
    assert "SENTINEL_HEALTH_VIEW_OUTPUT" in out          # render_health()'s own
                                                          # output was printed...
    assert "BUY" not in out and "TRIM" not in out         # ...the standard report's
                                                          # vocabulary was not

    assert len(plan_calls) == 1
    # observational: no deployable cash or margin capacity reaches plan()
    assert plan_calls[0]["cash"] == 0.0
    assert plan_calls[0]["margin_requested"] == 0.0

    assert len(render_health_calls) == 1
    result = render_health_calls[0]
    # render_health() received plan()'s own output, already carried through
    # main()'s post-processing (margin_state attached) -- not a stub.
    assert "margin_state" in result
    assert "t1t2_proximity" in result
    assert "crypto_sleeve" in result


# ── read-only-check-margin-truthfulness correction ─────────────────────────
#
# Covers: (1) --no-log is restricted to --review (a --cash/--margin run or a
# bare invocation must reject it, so it can never bypass the audit trail);
# (2) normal --cash/--margin/--review logging is unchanged; (3) fresh/stale/
# missing/malformed/future margin.synced_at feeding classify_margin_state()
# via _margin_buffer_age_days()/_margin_buffer_age_unverifiable() surfaces
# verify_margin_data correctly with an inclusive >=2-day stale boundary that
# matches render()'s pre-existing banner, never fabricates a numeric age for
# invalid/future dates, and never touches plan()'s own buy/trim/block/
# cash_left/margin decisions -- classify_margin_state() runs strictly after
# plan() returns. (4) the standard review shows each staleness/unverifiable
# explanation exactly once, never duplicated between the banner and the
# classifier's own reason text.

def _review_cli_targets_and_holdings(tmp_path, synced_at="2026-07-18",
                                     debt=100.0, buffer_pct=50.0):
    targets_file = tmp_path / "targets.yaml"
    holdings_file = tmp_path / "holdings.yaml"
    with targets_file.open("w") as f:
        yaml.safe_dump({
            "tiers": {"T1": {"weight_pct": 10.0, "tickers": ["AAA"]}},
            "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7, "trim_rsi": 60,
                     "t1t2_trim_mult": 1.5},
            "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
            "crypto": {},
        }, f)
    with holdings_file.open("w") as f:
        yaml.safe_dump({
            "holdings": {}, "shares": {"AAA": 10.0}, "crypto_shares": {},
            "margin": {"debt": debt, "buffer_pct": buffer_pct, "synced_at": synced_at},
        }, f)
    return targets_file, holdings_file


def _patch_review_cli(monkeypatch, targets_file, holdings_file, logs_dir, perf_log_file):
    monkeypatch.setattr(allocate, "TARGETS_FILE", targets_file)
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", holdings_file)
    monkeypatch.setattr(allocate, "LOGS_DIR", logs_dir)
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log_file)
    monkeypatch.setattr(allocate, "AlpacaPaperClient", lambda: object())
    monkeypatch.setattr(
        allocate, "fetch_market",
        lambda client, tickers, regime_ticker: (
            {"AAA": {"price": 100.0, "rsi14": 50.0, "sma200": 90.0}}, True, True))
    monkeypatch.setattr(
        allocate, "resolve_holdings",
        lambda client, metrics=None, crypto_prices=None: {"AAA": 1000.0})


def _strip_timestamp_line(text):
    return "\n".join(l for l in text.splitlines() if not l.startswith("# Allocation advisory"))


# ── finding 1: --no-log is restricted to --review ──────────────────────────
# required tests 2, 3, 4: bare / --cash / --margin + --no-log all rejected.

@pytest.mark.parametrize("argv_tail", [
    ["--no-log"],
    ["--cash", "500", "--no-log"],
    ["--margin", "500", "--no-log"],
])
def test_no_log_outside_review_is_rejected(argv_tail, monkeypatch, capsys):
    # No TARGETS_FILE/HOLDINGS_FILE/client patching needed: the rejection
    # happens immediately after argparse, before any file or network access.
    monkeypatch.setattr(sys, "argv", ["allocate.py", *argv_tail])
    with pytest.raises(SystemExit) as exc_info:
        allocate.main()
    assert exc_info.value.code == 2   # argparse's own error exit code
    err = capsys.readouterr().err
    assert "--no-log" in err
    assert "--review" in err


# required test 1: --review --no-log remains valid.

def test_review_no_log_is_accepted(tmp_path, monkeypatch, capsys):
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path)
    _patch_review_cli(monkeypatch, targets_file, holdings_file,
                      tmp_path / "logs", tmp_path / "perf.csv")
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review", "--no-log"])
    allocate.main()   # must not raise / exit
    assert "# Allocation advisory" in capsys.readouterr().out


def test_review_no_log_matches_normal_advisory_and_suppresses_writes(tmp_path, monkeypatch, capsys):
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path)
    perf_header = "date,net_equity,gross,margin_debt,qqq_price,voo_price,note\n"

    # -- run 1: normal --review. log_performance replaced with a recording
    # spy (not a real write -- no network/live-holdings resolution here) so
    # this test asserts *that* it was invoked, not its internal correctness
    # (already covered by log_performance's own existing tests).
    logs_dir_a = tmp_path / "logs_a"
    perf_log_a = tmp_path / "perf_a.csv"
    perf_log_a.write_text(perf_header)
    _patch_review_cli(monkeypatch, targets_file, holdings_file, logs_dir_a, perf_log_a)
    calls = []
    monkeypatch.setattr(allocate, "log_performance", lambda *a, **k: calls.append((a, k)))
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review"])
    allocate.main()
    out_normal = capsys.readouterr().out

    assert logs_dir_a.exists() and list(logs_dir_a.glob("allocation-*.md")), \
        "normal --review must still write the timestamped allocation log"
    assert len(calls) == 1, "normal --review must still call log_performance()"

    # -- run 2: --review --no-log. log_performance forbidden outright; any
    # call at all is the bug this correction exists to prevent.
    logs_dir_b = tmp_path / "logs_b"
    perf_log_b = tmp_path / "perf_b.csv"
    perf_log_b.write_text(perf_header)
    _patch_review_cli(monkeypatch, targets_file, holdings_file, logs_dir_b, perf_log_b)

    def _forbidden(*a, **k):
        raise AssertionError("log_performance must not run under --review --no-log")
    monkeypatch.setattr(allocate, "log_performance", _forbidden)
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review", "--no-log"])
    allocate.main()
    out_no_log = capsys.readouterr().out

    assert not logs_dir_b.exists(), "--no-log must not create the logs/ directory at all"
    assert perf_log_b.read_text() == perf_header, \
        "--no-log must leave performance_log.csv byte-identical"

    # Same advisory body in both runs -- the --no-log branch sits strictly
    # after render()/print(out), so content cannot differ by construction;
    # this proves it rather than assuming it. Only the timestamp header line
    # (wall-clock, not content) is allowed to differ between the two runs.
    assert _strip_timestamp_line(out_no_log) == _strip_timestamp_line(out_normal)
    assert "# Allocation advisory" in out_no_log


# required test 5: normal --cash/--margin/--review logging is unchanged
# (without --no-log involved at all).

@pytest.mark.parametrize("argv_tail", [["--cash", "500"], ["--margin", "500"], ["--review"]])
def test_normal_logging_unchanged_without_no_log(argv_tail, tmp_path, monkeypatch, capsys):
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path)
    logs_dir = tmp_path / "logs"
    perf_log = tmp_path / "perf.csv"
    perf_header = "date,net_equity,gross,margin_debt,qqq_price,voo_price,note\n"
    perf_log.write_text(perf_header)
    _patch_review_cli(monkeypatch, targets_file, holdings_file, logs_dir, perf_log)
    calls = []
    monkeypatch.setattr(allocate, "log_performance", lambda *a, **k: calls.append((a, k)))
    monkeypatch.setattr(sys, "argv", ["allocate.py", *argv_tail])
    allocate.main()
    capsys.readouterr()

    assert logs_dir.exists() and list(logs_dir.glob("allocation-*.md"))
    assert len(calls) == 1


# required test 14: the phone script invokes the no-write review path.

def test_run_portfolio_check_script_uses_no_log_review():
    from pathlib import Path
    script = Path(__file__).resolve().parent / "run_portfolio_check.sh"
    text = script.read_text()
    review_lines = [l for l in text.splitlines() if "allocate.py --review" in l]
    assert review_lines, "run_portfolio_check.sh must invoke allocate.py --review"
    assert all("--no-log" in l for l in review_lines), (
        "every allocate.py --review invocation in run_portfolio_check.sh must "
        "use --no-log so the phone check stays genuinely read-only")


# ── finding 2: unified >=2-day staleness boundary ──────────────────────────
# required tests 6, 7, 8: age 1 fresh; age exactly 2 stale + verify_margin_data;
# age > 2 stale. Age 0 included too, matching margin_state.py's own unit
# coverage of the same boundary.

@pytest.mark.parametrize("days_old,expect_stale", [
    (0, False),
    (1, False),
    (2, True),     # inclusive boundary, matches render()'s pre-existing banner
    (5, True),
])
def test_margin_data_staleness_boundary_in_health_view(days_old, expect_stale, tmp_path, monkeypatch, capsys):
    synced_at = (date.today() - timedelta(days=days_old)).isoformat()
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path, synced_at=synced_at)
    _patch_review_cli(monkeypatch, targets_file, holdings_file,
                      tmp_path / "logs", tmp_path / "perf.csv")
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--health"])
    allocate.main()
    out = capsys.readouterr().out

    if expect_stale:
        assert VERIFY_MARGIN_DATA in out
        assert "stale_margin_data" in out
    else:
        assert VERIFY_MARGIN_DATA not in out
        assert "stale_margin_data" not in out
        assert "unverifiable_margin_data" not in out


# ── findings 3 & 4: missing/malformed/future sync dates are unverifiable ───
# required tests 9, 10, 11: each surfaces verify_margin_data without crashing,
# never fabricating a numeric age.

@pytest.mark.parametrize("label,synced_at_factory", [
    ("missing", lambda: None),
    ("malformed", lambda: "not-a-date"),
    ("future", lambda: (date.today() + timedelta(days=3)).isoformat()),
])
def test_unverifiable_sync_dates_surface_verify_margin_data_without_crashing(
        label, synced_at_factory, tmp_path, monkeypatch, capsys):
    targets_file, holdings_file = _review_cli_targets_and_holdings(
        tmp_path, synced_at=synced_at_factory())
    _patch_review_cli(monkeypatch, targets_file, holdings_file,
                      tmp_path / "logs", tmp_path / "perf.csv")
    captured = {}
    def _spy_render_health(result):
        captured["result"] = result
        return "SENTINEL"
    monkeypatch.setattr(allocate, "render_health", _spy_render_health)
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--health"])
    allocate.main()   # must not raise for any of the three synced_at shapes
    assert "SENTINEL" in capsys.readouterr().out

    ms = captured["result"]["margin_state"]
    assert VERIFY_MARGIN_DATA in ms.allowed_actions
    assert "unverifiable_margin_data" in ms.violated_constraints
    assert "stale_margin_data" not in ms.violated_constraints
    assert any("cannot be verified" in r for r in ms.reasons)
    # never fabricate a numeric age for an invalid/missing/future date
    assert not any("day(s) old" in r for r in ms.reasons)


def test_margin_buffer_age_days_fails_safe_on_missing_malformed_and_future():
    assert allocate._margin_buffer_age_days(None) is None
    assert allocate._margin_buffer_age_days("") is None
    assert allocate._margin_buffer_age_days("not-a-date") is None
    assert allocate._margin_buffer_age_days("2026-13-40") is None
    future = (date.today() + timedelta(days=1)).isoformat()
    assert allocate._margin_buffer_age_days(future) is None   # never a fabricated negative age
    assert allocate._margin_buffer_age_days(date.today().isoformat()) == 0


def test_margin_buffer_age_unverifiable_matches_age_days_none():
    today = date.today().isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    assert allocate._margin_buffer_age_unverifiable(today) is False
    assert allocate._margin_buffer_age_unverifiable(None) is True
    assert allocate._margin_buffer_age_unverifiable("garbage") is True
    assert allocate._margin_buffer_age_unverifiable(future) is True


# required test 12: no freshness condition (fresh/stale/missing/malformed/
# future) changes buys, trims, blocked rows, cash_left, margin allowed, or
# margin used -- classify_margin_state() runs strictly after plan() returns.

def test_no_freshness_condition_changes_allocation_or_margin_amounts(tmp_path, monkeypatch, capsys):
    today = date.today().isoformat()
    stale = (date.today() - timedelta(days=5)).isoformat()
    future = (date.today() + timedelta(days=3)).isoformat()
    scenarios = {
        "fresh": today, "stale": stale, "missing": None,
        "malformed": "not-a-date", "future": future,
    }
    captured = {}
    for label, synced_at in scenarios.items():
        targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path, synced_at=synced_at)
        _patch_review_cli(monkeypatch, targets_file, holdings_file,
                          tmp_path / f"logs_{label}", tmp_path / f"perf_{label}.csv")

        def _spy_render_health(result, _label=label):
            captured[_label] = result
            return f"SENTINEL_{_label}"
        monkeypatch.setattr(allocate, "render_health", _spy_render_health)
        monkeypatch.setattr(sys, "argv", ["allocate.py", "--health"])
        allocate.main()   # must not raise for any of the five synced_at shapes
        assert f"SENTINEL_{label}" in capsys.readouterr().out

    baseline = captured["fresh"]
    for label, result in captured.items():
        for key in ("buys", "trims", "blocked", "cash_left"):
            assert result[key] == baseline[key], f"{key} differs for {label!r}"
        assert result["margin"]["allowed"] == baseline["margin"]["allowed"], \
            f"margin allowed differs for {label!r}"
        assert result["margin"]["used"] == baseline["margin"]["used"], \
            f"margin used differs for {label!r}"


def test_buffer_data_age_days_cannot_influence_buys_trims_blocked_cash_left_margin_allowed():
    # Unit-level companion to the CLI test above: directly varies
    # buffer_data_age_days / buffer_data_unverifiable at the plan()+
    # classify_margin_state() layer, proving the post-plan invariant holds
    # independent of any CLI/YAML wiring.
    targets = _base_targets()
    roster = build_roster(targets)
    holdings = {"DDD": 2000.0, "AAA": 500.0}
    metrics = _flat_metrics(["DDD", "AAA"])

    result_a = plan(targets, holdings, roster, metrics, True, True, cash=500.0,
                    margin_debt=100.0, margin_buffer_pct=50.0)
    result_b = plan(targets, holdings, roster, metrics, True, True, cash=500.0,
                    margin_debt=100.0, margin_buffer_pct=50.0)
    result_c = plan(targets, holdings, roster, metrics, True, True, cash=500.0,
                    margin_debt=100.0, margin_buffer_pct=50.0)

    _attach_margin_state(result_a, targets, buffer_data_age_days=0.1,
                         stale_threshold_days=float(allocate.STALE_MARGIN_DAYS))
    _attach_margin_state(result_b, targets, buffer_data_age_days=30.0,
                         stale_threshold_days=float(allocate.STALE_MARGIN_DAYS))
    _attach_margin_state(result_c, targets, buffer_data_unverifiable=True)

    for other in (result_b, result_c):
        assert result_a["buys"] == other["buys"]
        assert result_a["trims"] == other["trims"]
        assert result_a["blocked"] == other["blocked"]
        assert result_a["cash_left"] == other["cash_left"]
        assert result_a["margin"]["allowed"] == other["margin"]["allowed"]
        assert result_a["margin"]["used"] == other["margin"]["used"]

    # sanity: the differing age/unverifiable flag actually reached the
    # classifier (else this test would trivially pass without proving
    # anything about wiring).
    assert "stale_margin_data" not in result_a["margin_state"].violated_constraints
    assert "stale_margin_data" in result_b["margin_state"].violated_constraints
    assert "unverifiable_margin_data" in result_c["margin_state"].violated_constraints


# ── finding 2 (cont'd): standard review shows each staleness/unverifiable
# explanation exactly once -- required test 13.

def test_review_shows_stale_explanation_exactly_once(tmp_path, monkeypatch, capsys):
    stale = (date.today() - timedelta(days=5)).isoformat()
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path, synced_at=stale)
    _patch_review_cli(monkeypatch, targets_file, holdings_file,
                      tmp_path / "logs", tmp_path / "perf.csv")
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review", "--no-log"])
    allocate.main()
    out = capsys.readouterr().out

    assert out.count("day(s) old") == 1


def test_review_shows_unverifiable_explanation_exactly_once(tmp_path, monkeypatch, capsys):
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path, synced_at=None)
    _patch_review_cli(monkeypatch, targets_file, holdings_file,
                      tmp_path / "logs", tmp_path / "perf.csv")
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review", "--no-log"])
    allocate.main()
    out = capsys.readouterr().out

    assert out.count("cannot be verified") == 1
