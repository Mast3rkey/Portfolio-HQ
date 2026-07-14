"""Tests for the July 2026 margin doctrine: leverage cap + buffer floor
(margin_capacity) and the semis-cluster mechanical trim (plan()).

These cover the most financially consequential code in the repo — added
after a system audit found no automated coverage existed for either.
"""

from allocate import build_roster, margin_capacity, plan


# ── margin_capacity() ────────────────────────────────────────────────────────

def test_healthy_buffer_clips_to_leverage_cap():
    # gross=100, debt=0 -> net_equity=100. Cap 1.8x -> allowed margin = 80.
    net_equity, allowed, forced, reason = margin_capacity(
        gross=100.0, margin_debt=0.0, cash=0.0, leverage_cap=1.8,
        buffer_pct=50.0, buffer_floor_pct=30.0, margin_requested=200.0)
    assert net_equity == 100.0
    assert allowed == 80.0
    assert forced is False
    assert "leverage cap" in reason


def test_request_under_cap_is_not_clipped():
    net_equity, allowed, forced, reason = margin_capacity(
        gross=100.0, margin_debt=0.0, cash=0.0, leverage_cap=1.8,
        buffer_pct=50.0, buffer_floor_pct=30.0, margin_requested=10.0)
    assert allowed == 10.0
    assert forced is False
    assert reason == ""


def test_buffer_below_floor_forces_zero_hard_cutoff():
    # Buffer floor is a hard cutoff, not a taper — any request is fully blocked.
    net_equity, allowed, forced, reason = margin_capacity(
        gross=100.0, margin_debt=20.0, cash=0.0, leverage_cap=1.8,
        buffer_pct=29.9, buffer_floor_pct=30.0, margin_requested=1.0)
    assert allowed == 0.0
    assert forced is True
    assert "forced de-lever" in reason


def test_buffer_exactly_at_floor_is_not_forced():
    _, allowed, forced, _ = margin_capacity(
        gross=100.0, margin_debt=20.0, cash=0.0, leverage_cap=1.8,
        buffer_pct=30.0, buffer_floor_pct=30.0, margin_requested=1.0)
    assert forced is False
    assert allowed == 1.0


def test_unsynced_buffer_skips_buffer_gate_applies_leverage_only():
    # buffer_pct=None means "never synced" — don't silently treat as safe or
    # forced; leverage cap still applies on its own.
    # gross=180, debt=80 -> net_equity=100, already exactly at the 1.8x cap.
    net_equity, allowed, forced, reason = margin_capacity(
        gross=180.0, margin_debt=80.0, cash=0.0, leverage_cap=1.8,
        buffer_pct=None, buffer_floor_pct=30.0, margin_requested=50.0)
    assert net_equity == 100.0
    assert forced is False
    assert allowed == 0.0  # already at 1.8x with no cash added, no room left
    assert "leverage cap" in reason


def test_cash_deposit_grows_allowed_margin_room():
    # New cash grows net_equity, which grows the leverage-cap ceiling too.
    # gross=180, debt=80 -> net_equity=100 before the deposit.
    net_equity, allowed, forced, _ = margin_capacity(
        gross=180.0, margin_debt=80.0, cash=100.0, leverage_cap=1.8,
        buffer_pct=50.0, buffer_floor_pct=30.0, margin_requested=1000.0)
    assert net_equity == 100.0
    # cap: 1.8*(100+100) - 180 - 100 = 360-280 = 80
    assert allowed == 80.0


def test_already_over_cap_allows_nothing_more():
    # gross=200, debt=100 -> net_equity=100, current leverage already 2.0x > 1.8x cap.
    _, allowed, forced, reason = margin_capacity(
        gross=200.0, margin_debt=100.0, cash=0.0, leverage_cap=1.8,
        buffer_pct=50.0, buffer_floor_pct=30.0, margin_requested=10.0)
    assert allowed == 0.0
    assert forced is False
    assert "leverage cap" in reason


# ── cluster caps mechanical trim (plan()) ───────────────────────────────────

def _base_targets(semis_cluster_pct=10.0, extra_clusters=None):
    return {
        "tiers": {
            "T1": {"weight_pct": 20.0, "tickers": ["DDD"]},
            "T2": {"weight_pct": 5.0, "tickers": ["AAA"]},
            "T3": {"weight_pct": 2.0, "tickers": ["CCC"]},
            "band": {"weight_pct": 3.0, "cap_multiple": 1.25, "tickers": ["BBB"]},
        },
        "caps": {"clusters": [{"name": "semis", "pct": semis_cluster_pct,
                              "tickers": ["AAA", "BBB", "CCC"]}]
                             + (extra_clusters or [])},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7, "trim_rsi": 60},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def _cluster_value(result, name):
    return next(c["value"] for c in result["clusters"] if c["name"] == name)


def _flat_metrics(tickers, rsi=50):
    return {t: {"price": 100.0, "rsi14": rsi, "sma200": 90.0} for t in tickers}


def test_semis_cluster_trim_largest_overweight_first_floored_at_own_target():
    targets = _base_targets(semis_cluster_pct=10.0)
    # T1 DDD isn't a semis ticker: at its own target, untouched.
    # T2 AAA: target 5, current 30 -> overweight 25, no per-tier trim mechanism.
    # band BBB: target 3, cap_multiple 1.25 -> overweight_limit 3.75; current 25
    #   with RSI 70 fires the regular trim down to target (3), dollars=22.
    # T3 CCC: target 2, current 25 -> overweight 23, no per-tier trim mechanism.
    holdings = {"AAA": 30.0, "BBB": 25.0, "CCC": 25.0, "DDD": 20.0}
    roster = build_roster(targets)
    metrics = _flat_metrics(["AAA", "BBB", "CCC", "DDD"])
    metrics["BBB"]["rsi14"] = 70  # hot enough to fire the regular band trim

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    # book = 100 (no cash/margin). cap = 10% of 100 = 10.
    trims_by_ticker = {t["ticker"]: t for t in result["trims"]}
    assert set(trims_by_ticker) == {"AAA", "BBB", "CCC"}

    assert trims_by_ticker["BBB"]["dollars"] == 22.0
    assert "RSI" in trims_by_ticker["BBB"]["reason"]

    # AAA (overweight 25) ranked ahead of CCC (overweight 23) -> AAA fully
    # trimmed to its own target first, cluster settles exactly at the 10 cap.
    assert trims_by_ticker["AAA"]["dollars"] == 25.0
    assert trims_by_ticker["CCC"]["dollars"] == 23.0
    assert "semis cluster cap" in trims_by_ticker["AAA"]["reason"]
    assert "semis cluster cap" in trims_by_ticker["CCC"]["reason"]

    assert _cluster_value(result, "semis") == 10.0  # exactly at cap, nothing left over


def test_semis_cluster_under_cap_generates_no_trim():
    targets = _base_targets(semis_cluster_pct=90.0)  # cap far above current value
    holdings = {"AAA": 30.0, "BBB": 25.0, "CCC": 25.0, "DDD": 20.0}
    roster = build_roster(targets)
    metrics = _flat_metrics(["AAA", "BBB", "CCC", "DDD"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    assert result["trims"] == []
    assert _cluster_value(result, "semis") == 80.0  # AAA+BBB+CCC, untouched


def test_semis_cluster_trim_leaves_residual_when_overweight_insufficient():
    # Cap breach bigger than total available overweight -> trims everything
    # it can, leaves the rest as a visible residual rather than over-trimming.
    targets = _base_targets(semis_cluster_pct=1.0)  # cap tiny relative to book
    holdings = {"AAA": 30.0, "BBB": 25.0, "CCC": 25.0, "DDD": 20.0}
    roster = build_roster(targets)
    metrics = _flat_metrics(["AAA", "BBB", "CCC", "DDD"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    # Every semis name gets trimmed to its own target (max possible), but the
    # 1% cap (=$1) still isn't reachable since fair-share targets alone sum
    # above it (AAA target 5 + BBB target 3 + CCC target 2 > 1).
    assert _cluster_value(result, "semis") > 1.0
    trimmed_tickers = {t["ticker"] for t in result["trims"]}
    assert trimmed_tickers == {"AAA", "BBB", "CCC"}


def test_two_independent_clusters_trim_separately():
    # A second cluster (disjoint tickers) should be evaluated on its own cap,
    # independent of the first.
    targets = _base_targets(semis_cluster_pct=90.0,  # semis cluster: no breach
                            extra_clusters=[{"name": "power", "pct": 10.0,
                                            "tickers": ["DDD"]}])
    # book = 5+3+2+25 = 35. DDD is T1 (weight 20 -> target 7.0) with no per-tier
    # trim mechanism of its own; the "power" cluster caps it at 10% of book
    # (=3.5), tighter than DDD's own-target floor (7.0) -> trims down to the
    # floor (own target), leaving a residual above the nominal cap dollars.
    holdings = {"AAA": 5.0, "BBB": 3.0, "CCC": 2.0, "DDD": 25.0}
    roster = build_roster(targets)
    metrics = _flat_metrics(["AAA", "BBB", "CCC", "DDD"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    trims_by_ticker = {t["ticker"]: t for t in result["trims"]}
    assert set(trims_by_ticker) == {"DDD"}
    assert "power cluster cap" in trims_by_ticker["DDD"]["reason"]
    assert _cluster_value(result, "power") == 7.0     # floored at DDD's own target
    assert _cluster_value(result, "semis") == 10.0     # AAA+BBB+CCC, untouched (well under 90% cap)


def test_ticker_in_two_clusters_blocked_by_either():
    # A ticker in two clusters needs room in BOTH to buy.
    targets = _base_targets(semis_cluster_pct=90.0,
                            extra_clusters=[{"name": "power", "pct": 4.0,
                                            "tickers": ["AAA"]}])
    # AAA (T2, target 5) is underweight at current=0 -> wants a full $5 buy,
    # but the "power" cluster caps AAA's cluster at 4% of book (=4).
    holdings = {"AAA": 0.0, "BBB": 0.0, "CCC": 0.0, "DDD": 0.0}
    roster = build_roster(targets)
    metrics = _flat_metrics(["AAA", "BBB", "CCC", "DDD"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0, margin_requested=0.0)

    buys_by_ticker = {b["ticker"]: b for b in result["buys"]}
    assert buys_by_ticker["AAA"]["dollars"] == 4.0   # clipped by the tighter "power" cap, not semis
