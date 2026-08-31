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
from datetime import date, datetime, timedelta

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


def _base_targets():
    return {
        "destination": [
            {"ticker": "DDD", "target_pct": 20.0, "asset_class": "equity"},
            {"ticker": "AAA", "target_pct": 5.0, "asset_class": "equity"},
        ],
        "caps": {"clusters": [{"name": "semis", "pct": 10.0, "tickers": ["AAA"]}]},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
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

def _padded_cluster_targets(cap_pct, target_pct=10.0):
    return {
        "destination": [{"ticker": "CLU", "target_pct": target_pct, "asset_class": "equity"}],
        "caps": {"clusters": [{"name": "testcluster", "pct": cap_pct, "tickers": ["CLU"]}]},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
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
    # Cluster cap (5%) tighter than the name's own destination target (10%):
    # the cluster-cap mechanism trims CLU down to its own target and no
    # further -- it never trims a name below its own target -- so once CLU
    # is at target the cluster still exceeds the (very tight) 5% cap, and
    # that persists in plan()'s output rather than being silently resolved.
    # Real, reachable config shape, not a fabricated edge case.
    targets = _padded_cluster_targets(cap_pct=5.0, target_pct=10.0)
    roster = build_roster(targets)
    holdings = {"CLU": 200.0, "PAD": 800.0}   # book=1000, CLU target=100, cap_dollars=50
    metrics = _flat_metrics(["CLU"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert any(t["ticker"] == "CLU" for t in result["trims"])   # cluster cap fired
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


# ── PHQ-2026-02: crypto destination rows (retired the aggregate sleeve) ────
# The prior aggregate 10% crypto sleeve (one shared target_pct across all
# configured coins, competing in plan()'s ranking as a single synthetic
# "CRYPTO" candidate) is retired. Canonical v1.30 gives BTC/ETH/SOL each
# their own independent destination row and target_pct, like any other
# ticker -- no `crypto_sleeve`/`crypto_sleeve_pct` result key exists anymore,
# and no aggregate mechanism can reappear through a compatibility path. Each
# coin still skips the trend/RSI/earnings timing gates (Decisions Log, July
# 2026: "conviction-sizing, not a timing call" -- unchanged by this
# migration, still governed).

def _crypto_targets():
    return {
        "destination": [
            {"ticker": "BTC", "target_pct": 6.0, "asset_class": "crypto"},
            {"ticker": "ETH", "target_pct": 3.0, "asset_class": "crypto"},
            {"ticker": "SOL", "target_pct": 1.0, "asset_class": "crypto"},
            # PAD completes the destination to 100%. Without it this synthetic
            # config allocated only 10% of book, leaving 90% UNRECONCILED --
            # which protected-capital accounting correctly protects, blocking
            # every buy. The 90% was an artifact of a partial fixture, not the
            # behavior these tests exist to check (independent crypto rows).
            {"ticker": "PAD", "target_pct": 90.0, "asset_class": "equity"},
        ],
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }


def test_no_aggregate_crypto_sleeve_key_in_result():
    targets = _crypto_targets()
    roster = build_roster(targets)
    holdings = {"BTC": 30.0, "ETH": 20.0, "SOL": 5.0, "PAD": 945.0}
    result = plan(targets, holdings, roster, {}, True, True, cash=0.0)

    assert "crypto_sleeve" not in result
    assert "crypto_sleeve_pct" not in result


def test_btc_eth_sol_are_independent_destination_rows_with_own_targets():
    targets = _crypto_targets()
    roster = build_roster(targets)
    # book=1000 (BTC30+ETH20+SOL5+PAD945, no cash/margin). BTC target=60
    # (gap 30, buy candidate once cash is available); ETH target=30 (gap 10,
    # below the 25 min_lot -- not a candidate); SOL target=10 (gap 5, below
    # min_lot -- not a candidate). Each gap is independent of the others'
    # holdings/targets.
    holdings = {"BTC": 30.0, "ETH": 20.0, "SOL": 5.0, "PAD": 945.0}
    metrics = {}
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    underweight_by_ticker = {u["ticker"]: u for u in result["underweight"]}
    assert underweight_by_ticker["BTC"]["target"] == 60.0
    assert underweight_by_ticker["BTC"]["gap"] == 30.0
    assert "ETH" not in underweight_by_ticker     # gap (10) < min_lot (25)
    assert "SOL" not in underweight_by_ticker     # gap (5) < min_lot (25)

    # With a deposit sized to fund exactly BTC's own gap, BTC (and only BTC)
    # actually gets bought.
    result_funded = plan(targets, holdings, roster, metrics, True, True, cash=30.0)
    buys_by_ticker = {b["ticker"]: b for b in result_funded["buys"]}
    assert buys_by_ticker["BTC"]["dollars"] == 30.0
    assert "ETH" not in buys_by_ticker
    assert "SOL" not in buys_by_ticker


def test_changing_one_coins_holding_does_not_move_another_coins_target():
    targets = _crypto_targets()
    roster = build_roster(targets)
    metrics = {}

    holdings_a = {"BTC": 30.0, "ETH": 20.0, "SOL": 5.0, "PAD": 945.0}
    holdings_b = {"BTC": 30.0, "ETH": 500.0, "SOL": 5.0, "PAD": 465.0}  # ETH way overweight
    result_a = plan(targets, holdings_a, roster, metrics, True, True, cash=0.0)
    result_b = plan(targets, holdings_b, roster, metrics, True, True, cash=0.0)

    a_by_ticker = {u["ticker"]: u for u in result_a["underweight"]}
    b_by_ticker = {u["ticker"]: u for u in result_b["underweight"]}
    # BTC's own target is unaffected by ETH's holding size in either run.
    assert a_by_ticker["BTC"]["target"] == b_by_ticker["BTC"]["target"] == 60.0


def test_crypto_asset_class_skips_trend_and_earnings_gates():
    targets = _crypto_targets()
    roster = build_roster(targets)
    # BTC priced below its 200-SMA with a hot RSI (would block an equity row)
    # and metrics carries no earnings-safe defaults either -- crypto must
    # still be a plain buy candidate, no BLOCKED row.
    holdings = {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0}
    metrics = {"BTC": {"price": 50.0, "rsi14": 80.0, "sma200": 100.0}}
    result = plan(targets, holdings, roster, metrics, True, True, cash=1000.0)

    assert not any(r["ticker"] == "BTC" for r in result["blocked"])
    assert any(b["ticker"] == "BTC" for b in result["buys"])

# ── main() production-path coverage: concentration_min_fraction wiring ────
# concentration_min_fraction is a still-governed margin_state.py knob,
# unrelated to the retired crypto sleeve -- this drives the actual CLI path
# (argparse -> --health -> plan() -> classify_margin_state() -> render_health())
# with every network/live-data boundary faked out, the same technique
# test_health_flag_cli_path_is_read_only uses above, so it observes
# allocate.py's real composition, not a paraphrase of it. A revert of
# main()'s real wiring (concentration_min_fraction back to `... or 0.5`
# computed elsewhere) could not pass this test unnoticed.

def _min_fraction_targets_and_holdings(tmp_path, min_fraction):
    """min_fraction=None omits margin.concentration_adjustment entirely
    (the "absent" case); any other value sets concentration_adjustment.
    min_fraction explicitly (the "explicit, including 0.0" case)."""
    targets_file = tmp_path / "targets.yaml"
    holdings_file = tmp_path / "holdings.yaml"
    margin_cfg = {"leverage_cap": 1.8, "buffer_floor_pct": 30.0}
    if min_fraction is not None:
        margin_cfg["concentration_adjustment"] = {"min_fraction": min_fraction}
    with targets_file.open("w") as f:
        yaml.safe_dump({
            "destination": [{"ticker": "AAA", "target_pct": 50.0, "asset_class": "equity"}],
            "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7},
            "margin": margin_cfg,
        }, f)
    with holdings_file.open("w") as f:
        yaml.safe_dump({
            "holdings": {}, "shares": {"AAA": 1.0}, "crypto_shares": {},
            # debt=0/buffer=50 keeps margin_capacity()/classify_margin_state()
            # in an unremarkable NORMAL state -- irrelevant to what these
            # tests check, so kept deliberately boring.
            "margin": {"debt": 0.0, "buffer_pct": 50.0, "synced_at": "2026-07-18"},
        }, f)
    return targets_file, holdings_file


def _patch_min_fraction_cli(monkeypatch, targets_file, holdings_file):
    monkeypatch.setattr(allocate, "TARGETS_FILE", targets_file)
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", holdings_file)
    monkeypatch.setattr(allocate, "AlpacaPaperClient", lambda: object())
    monkeypatch.setattr(
        allocate, "fetch_market",
        lambda client, tickers, regime_ticker: (
            {"AAA": {"price": 100.0, "rsi14": 50.0, "sma200": 90.0}}, True, True))
    # AAA=50, book=50, exactly at its 50% target -- no trim/buy noise, a
    # boring, fully-resolved book so the only thing under test is the
    # min_fraction resolution itself.
    monkeypatch.setattr(
        allocate, "resolve_holdings",
        lambda client, metrics=None, crypto_prices=None: {"AAA": 50.0})


def _spy_classify_margin_state(monkeypatch):
    captured = {}
    real = allocate.classify_margin_state

    def spy(**kwargs):
        captured.update(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(allocate, "classify_margin_state", spy)
    return captured


def test_main_production_path_explicit_zero_min_fraction(tmp_path, monkeypatch):
    targets_file, holdings_file = _min_fraction_targets_and_holdings(
        tmp_path, min_fraction=0.0)
    _patch_min_fraction_cli(monkeypatch, targets_file, holdings_file)
    captured_kwargs = _spy_classify_margin_state(monkeypatch)

    render_health_calls = []
    monkeypatch.setattr(
        allocate, "render_health",
        lambda result: (render_health_calls.append(result), "SENTINEL")[1])

    monkeypatch.setattr(sys, "argv", ["allocate.py", "--health"])
    allocate.main()   # the real production path, not a test-side mirror

    assert captured_kwargs["concentration_min_fraction"] == 0.0
    assert len(render_health_calls) == 1


def test_main_production_path_absent_min_fraction_defaults_to_half(
        tmp_path, monkeypatch):
    targets_file, holdings_file = _min_fraction_targets_and_holdings(
        tmp_path, min_fraction=None)
    _patch_min_fraction_cli(monkeypatch, targets_file, holdings_file)
    captured_kwargs = _spy_classify_margin_state(monkeypatch)
    monkeypatch.setattr(allocate, "render_health", lambda result: "SENTINEL")

    monkeypatch.setattr(sys, "argv", ["allocate.py", "--health"])
    allocate.main()

    assert captured_kwargs["concentration_min_fraction"] == 0.5

# ── PHQ-2026-02: no T1/T2 proximity reporting or ceiling survives ─────────
# The prior `t1t2_proximity` result key and its 1.5x concentration-ceiling
# trim were both defined in terms of the T1/T2 tiers the canonical
# destination architecture removed (see the governance filing's "Retired by
# this migration" section) -- neither exists anymore, and no equivalent
# mechanism was invented in their place.

def _proximity_style_targets():
    return {
        "destination": [
            {"ticker": "NEUT", "target_pct": 10.0, "asset_class": "equity"},
            {"ticker": "OVER", "target_pct": 10.0, "asset_class": "equity"},
            {"ticker": "UNDER", "target_pct": 10.0, "asset_class": "equity"},
        ],
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }


def test_no_t1t2_proximity_key_in_result():
    targets = _proximity_style_targets()
    roster = build_roster(targets)
    holdings = {"NEUT": 130.0, "OVER": 200.0, "UNDER": 50.0, "PAD": 620.0}
    metrics = _flat_metrics(["NEUT", "OVER", "UNDER"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert "t1t2_proximity" not in result


def test_over_double_target_name_outside_any_cluster_is_never_trimmed():
    # OVER at 200 vs. its own target of 100 is 2.0x -- well past the retired
    # 1.5x T1/T2 ceiling. OVER is in no cluster in this fixture, so nothing
    # in the canonical architecture mechanically trims it.
    targets = _proximity_style_targets()
    roster = build_roster(targets)
    holdings = {"NEUT": 130.0, "OVER": 200.0, "UNDER": 50.0, "PAD": 620.0}
    metrics = _flat_metrics(["NEUT", "OVER", "UNDER"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0)

    assert not any(t["ticker"] == "OVER" for t in result["trims"])
    assert not any(t["ticker"] == "NEUT" for t in result["trims"])


# ── Health View V1: render_health() ────────────────────────────────────────
# ── Health View V1: render_health() ────────────────────────────────────────

def _health_fixture_result(margin_state_obj="omit"):
    """A hand-built result dict -- no plan()/live client/YAML involved -- to
    prove render_health() is a pure function of `result` alone. PHQ-2026-02:
    no `crypto_sleeve`/`t1t2_proximity` keys (both retired); carries the
    8%/40% no-add ceiling fields plan() now actually returns instead."""
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
        "issuer_exposure": {"NVDA": {"direct_pct": 5.0, "embedded_pct": 1.0,
                                     "effective_pct": 6.0}},
        "issuer_ceiling_pct": 8.0,
        "common_driver_current_pct": 25.0,
        "common_driver_ceiling_pct": 40.0,
        "retained_common_driver_measurement": {
            "value_pct": 40.0284, "measured_at": "2026-07-30",
            "methodology": "canonical v1.30 target-weight-basis look-through, PHQ-2026-01 due diligence",
        },
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
                  margin_debt=100.0, margin_buffer_pct=50.0,
                  lookthrough=allocate.load_issuer_lookthrough())
    result = _attach_margin_state(result, targets)
    out = render_health(result)

    assert "## Margin" in out
    assert "## Margin risk state" in out
    assert "## Clusters" in out
    assert "## 8%/40% no-add ceilings" in out
    # the old section headers (not just a retirement mention) are gone
    assert "## Crypto sleeve" not in out
    assert "## T1/T2 proximity" not in out
    assert f"{result['margin']['leverage_cap']:.2f}x cap" in out
    assert f"{result['margin']['buffer_floor_pct']:.0f}% floor" in out
    for c in result["clusters"]:
        assert c["name"] in out


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
            "destination": [{"ticker": "AAA", "target_pct": 10.0, "asset_class": "equity"}],
            "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7},
            "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
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
    assert "common_driver_current_pct" in result
    assert "issuer_exposure" in result


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
            "destination": [{"ticker": "AAA", "target_pct": 10.0, "asset_class": "equity"}],
            "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7},
            "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
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


# ── controlled clock ───────────────────────────────────────────────────────
# allocate.py reads the wall clock in more than one place per advisory:
# a header line ("# Allocation advisory — <ts>") *and* an unstripped
# timestamp inside the 40% common-driver advisory body ("... + current
# prices, <ts>) vs ..."). _strip_timestamp_line() removes only the header,
# so two back-to-back allocate.main() calls that straddle a one-second
# boundary produce advisories that differ in the *body* — a real, observed
# CI failure on main (run 32603595964 attempt 1, job 97105352737):
#
#     - 22 22:51:54) vs **40
#     + 22 22:51:55) vs **40
#
# That is a defect in the *test*, not in allocate.py: emitting a live
# wall-clock reading in a live advisory is correct production behaviour and
# is deliberately left untouched. Any test that compares two separate
# advisories must therefore control the clock rather than hope the two runs
# land in the same second.

# The instant every frozen-clock test pins allocate.py's wall clock to. Its
# exact value is arbitrary; only its *stability across calls* matters.
_FROZEN_MOMENT = datetime(2026, 8, 22, 22, 51, 54)


def _pin_allocate_clock(monkeypatch, moments):
    """Pin allocate.datetime.now() to a caller-supplied sequence of instants.

    `moments` is a callable taking the 1-based call ordinal and returning the
    datetime that call should observe. Subclassing the real datetime keeps
    every other attribute (strftime, arithmetic, comparison) genuine, so only
    now() is controlled. Returns a list that records each observed instant, so
    a test can assert the clock was actually consumed rather than assuming it.
    """
    observed = []

    class _PinnedClock(datetime):
        _calls = 0

        @classmethod
        def now(cls, tz=None):
            cls._calls += 1
            moment = moments(cls._calls)
            observed.append(moment)
            return moment

    monkeypatch.setattr(allocate, "datetime", _PinnedClock)
    return observed


def _freeze_allocate_clock(monkeypatch, moment=_FROZEN_MOMENT):
    """Pin every allocate.py wall-clock read to one fixed instant."""
    return _pin_allocate_clock(monkeypatch, lambda _ordinal: moment)


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
    # Pin the wall clock for BOTH runs to the same instant. allocate.py emits
    # a timestamp in the advisory *body* as well as the header, so without
    # this the two runs can straddle a one-second boundary and disagree on
    # content that is genuinely identical -- see _pin_allocate_clock above.
    observed_a = _freeze_allocate_clock(monkeypatch)
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
    observed_b = _freeze_allocate_clock(monkeypatch)

    def _forbidden(*a, **k):
        raise AssertionError("log_performance must not run under --review --no-log")
    monkeypatch.setattr(allocate, "log_performance", _forbidden)
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review", "--no-log"])
    allocate.main()
    out_no_log = capsys.readouterr().out

    assert not logs_dir_b.exists(), "--no-log must not create the logs/ directory at all"
    assert perf_log_b.read_text() == perf_header, \
        "--no-log must leave performance_log.csv byte-identical"

    # Both runs observed the clock, and observed only the frozen instant --
    # so the comparison below is a real content comparison under a
    # controlled clock, not a comparison that happened to avoid the race.
    assert set(observed_a) == set(observed_b) == {_FROZEN_MOMENT}
    # Each advisory reads the clock at least twice (header + the in-body
    # common-driver reading), and the normal run reads it exactly once more
    # than the --no-log run -- that extra read is the allocation-log
    # filename, which --no-log correctly never reaches.
    assert len(observed_b) >= 2, "advisory must read the clock in header AND body"
    assert len(observed_a) == len(observed_b) + 1, \
        "--no-log must skip exactly the allocation-log filename timestamp"

    # Same advisory in both runs -- the --no-log branch sits strictly after
    # render()/print(out), so content cannot differ by construction; this
    # proves it rather than assuming it. Under the frozen clock the ENTIRE
    # advisory is compared, header included: nothing is stripped, skipped or
    # normalised away, so no difference anywhere in the body can hide.
    assert out_no_log == out_normal

    # ...and what was compared is the real advisory, not an empty or gutted
    # string: the header and the timestamped common-driver body line -- the
    # exact line the historical race differed on -- are both present.
    assert "# Allocation advisory" in out_no_log
    assert _FROZEN_MOMENT.strftime("%Y-%m-%d %H:%M:%S") in out_no_log
    assert "## 40% AI/platform common-driver exposure" in out_no_log
    assert out_no_log.count(_FROZEN_MOMENT.strftime("%Y-%m-%d %H:%M:%S")) >= 2, \
        "both the header and the in-body wall-clock reading must be compared"


# ── regression cover for the one-second advisory race ──────────────────────
# These guard the repair above. They are deliberately written so that the
# historical defect is *reproduced* rather than merely described.

def _review_advisory_pair(tmp_path, monkeypatch, capsys, moment_normal, moment_no_log):
    """Run `--review` then `--review --no-log`, each under its own pinned
    clock, and return their two advisories (stdout only -- allocate.py sends
    both log-status lines to stderr, so stdout is exactly the advisory)."""
    targets_file, holdings_file = _review_cli_targets_and_holdings(tmp_path)
    perf_header = "date,net_equity,gross,margin_debt,qqq_price,voo_price,note\n"
    outs = []
    for tag, argv_tail, moment in (
        ("a", ["--review"], moment_normal),
        ("b", ["--review", "--no-log"], moment_no_log),
    ):
        perf_log = tmp_path / f"perf_{tag}.csv"
        perf_log.write_text(perf_header)
        _patch_review_cli(monkeypatch, targets_file, holdings_file,
                          tmp_path / f"logs_{tag}", perf_log)
        _freeze_allocate_clock(monkeypatch, moment)
        monkeypatch.setattr(allocate, "log_performance", lambda *a, **k: None)
        monkeypatch.setattr(sys, "argv", ["allocate.py", *argv_tail])
        allocate.main()
        outs.append(capsys.readouterr().out)
    return outs


def test_adjacent_second_advisories_still_differ_after_header_only_stripping(
        tmp_path, monkeypatch, capsys):
    """The historical failure, reproduced deterministically.

    This is the non-vacuity guard: it proves that stripping only the header
    line -- what the test did before this repair -- genuinely fails when the
    two runs land in adjacent seconds. If allocate.py ever stopped emitting a
    second, in-body wall-clock reading, this test would start failing and the
    frozen-clock repair could be revisited.
    """
    earlier = datetime(2026, 8, 22, 22, 51, 54)
    later = datetime(2026, 8, 22, 22, 51, 55)
    out_normal, out_no_log = _review_advisory_pair(
        tmp_path, monkeypatch, capsys, earlier, later)

    # Header-only stripping is NOT sufficient: the advisories still differ.
    assert _strip_timestamp_line(out_no_log) != _strip_timestamp_line(out_normal)

    # ...and they differ on exactly one line: the in-body wall-clock reading.
    differing = [
        (x, y)
        for x, y in zip(_strip_timestamp_line(out_normal).splitlines(),
                        _strip_timestamp_line(out_no_log).splitlines())
        if x != y
    ]
    assert len(differing) == 1, differing
    before, after = differing[0]
    assert earlier.strftime("%Y-%m-%d %H:%M:%S") in before
    assert later.strftime("%Y-%m-%d %H:%M:%S") in after
    # Everything else about that line is identical -- it is a timestamp
    # difference, never a difference in advisory substance.
    assert (before.replace(earlier.strftime("%Y-%m-%d %H:%M:%S"), "")
            == after.replace(later.strftime("%Y-%m-%d %H:%M:%S"), ""))


def test_frozen_clock_makes_the_two_advisories_byte_identical(
        tmp_path, monkeypatch, capsys):
    """The same adjacent-second scenario, repaired: one pinned instant for
    both runs yields byte-identical advisories with nothing stripped."""
    out_normal, out_no_log = _review_advisory_pair(
        tmp_path, monkeypatch, capsys, _FROZEN_MOMENT, _FROZEN_MOMENT)
    assert out_no_log == out_normal


def test_frozen_clock_comparison_ignores_no_advisory_content(
        tmp_path, monkeypatch, capsys):
    """The repair must not work by deleting or blanket-ignoring content.

    Proves the compared advisory is substantial, is compared whole, and
    still contains the exact body line the historical race differed on.
    """
    out_normal, out_no_log = _review_advisory_pair(
        tmp_path, monkeypatch, capsys, _FROZEN_MOMENT, _FROZEN_MOMENT)
    stamp = _FROZEN_MOMENT.strftime("%Y-%m-%d %H:%M:%S")

    # Nothing is stripped: the whole advisory is compared, header included.
    assert out_no_log == out_normal
    assert _strip_timestamp_line(out_normal) != out_normal, \
        "the header line must still be present in the compared text"

    # Real content, not a gutted string.
    assert len(out_normal.splitlines()) > 10
    assert "# Allocation advisory" in out_normal
    assert "## 40% AI/platform common-driver exposure" in out_normal

    # Both wall-clock readings are inside the compared text.
    assert out_normal.count(stamp) == 2
    body_line = next(l for l in out_normal.splitlines()
                     if stamp in l and not l.startswith("# Allocation advisory"))
    assert "current prices" in body_line and "ceiling" in body_line


def test_production_wall_clock_behaviour_is_unchanged(tmp_path, monkeypatch, capsys):
    """allocate.py's live timestamps are production behaviour, not a defect.

    The repair is confined to the tests: unpatched, allocate.datetime is the
    real stdlib class, and when the clock genuinely advances the advisory
    genuinely reports the later instant. Nothing here asks allocate.py to
    stop reading the wall clock.
    """
    # Unpatched, allocate.py holds the real datetime class.
    assert allocate.datetime is datetime

    # And it faithfully reports whatever the clock says -- a later clock
    # produces a later advisory timestamp, in the body as well as the header.
    earlier = datetime(2026, 8, 22, 22, 51, 54)
    later = datetime(2026, 8, 22, 23, 45, 1)
    out_earlier, out_later = _review_advisory_pair(
        tmp_path, monkeypatch, capsys, earlier, later)
    for moment, out in ((earlier, out_earlier), (later, out_later)):
        stamp = moment.strftime("%Y-%m-%d %H:%M:%S")
        assert out.count(stamp) == 2, \
            "allocate.py must still emit both live wall-clock readings"


# required test 5: normal --cash/--margin/--review logging is unchanged
# (without --no-log involved at all).

# `--cash 500` was dropped from this list when the additive --cash deposit
# argument was RETIRED in favour of a tracked total cash balance: the flag now
# exits 2 with a migration message, so asserting it still logs was asserting a
# behavior that no longer exists. The retirement itself is covered by
# test_protected_capital_accounting.py::TestNoDoubleCounting.
@pytest.mark.parametrize("argv_tail", [["--margin", "500"], ["--review"]])
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
