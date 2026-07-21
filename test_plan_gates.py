"""Focused regression coverage for allocate.plan()'s gate/ordering branches
that had no deterministic test before this module:

  A. largest-dollar-gap allocation ordering + cash exhaustion
  B. the 200-SMA trend gate's blocking branch
  C. the earnings-blackout blocking branch
  D. the band/spec RSI-hot opportunistic trim

Every fixture here uses synthetic tickers/targets/metrics only — no
network, no real ticker calendars, no current-date dependence. The
repo-root conftest.py's autouse `no_live_earnings_lookup` fixture already
keeps the earnings lookup out of these tests by default (see conftest.py
for why patching `allocate.days_until_earnings` is the correct target);
section C overrides it explicitly per-case to drive the gate itself.

Cluster caps and the T1/T2 concentration ceiling are deliberately kept out
of every fixture below (neutral, non-T1/T2 tier names, no caps.clusters
entries) since those mechanisms already have dedicated coverage in
test_margin.py — mixing them in here would obscure which gate a given
assertion is actually proving.
"""

import allocate
from allocate import build_roster, plan


def _targets(ticker, tier_name="TX", weight_pct=50.0, gates=None):
    return {
        "tiers": {tier_name: {"weight_pct": weight_pct, "tickers": [ticker]}},
        "caps": {"clusters": []},
        "gates": {
            "min_lot_dollars": 1, "trend_rsi_override": 30,
            "earnings_blackout_days": 7, "trim_rsi": 60,
            "t1t2_trim_mult": 100.0,
            **(gates or {}),
        },
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def _multi_tier_targets(weights: dict[str, float]):
    """One neutral tier per ticker, each with its own weight_pct — lets a
    single plan() call carry several independently-sized dollar gaps."""
    return {
        "tiers": {
            f"TX_{tk}": {"weight_pct": w, "tickers": [tk]}
            for tk, w in weights.items()
        },
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                  "earnings_blackout_days": 7, "trim_rsi": 60,
                  "t1t2_trim_mult": 100.0},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def _metrics(tickers, price=100.0, rsi=50.0, sma200=90.0):
    return {t: {"price": price, "rsi14": rsi, "sma200": sma200} for t in tickers}


# ── A. largest-dollar-gap ordering + cash exhaustion ────────────────────────

def test_gap_ordering_fills_largest_first_partial_second_blocks_third():
    # weight_pcts sum to 140% of book so total demand always exceeds cash,
    # forcing a genuine partial fill + exhaustion rather than "everyone
    # fits" (with holdings=0, book == cash exactly, so total gap ==
    # cash * sum(weight_pct)/100 — that must exceed cash for this to bite).
    targets = _multi_tier_targets({"AAA": 60.0, "BBB": 50.0, "CCC": 30.0})
    roster = build_roster(targets)
    # Insertion order deliberately reversed vs. expected gap-descending
    # output order (CCC, BBB, AAA) — insertion order must not leak through.
    holdings = {"CCC": 0.0, "BBB": 0.0, "AAA": 0.0}
    metrics = _metrics(["CCC", "BBB", "AAA"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    # book = 100 (cash only, no holdings/margin) -> AAA target 60, BBB 50, CCC 30.
    buys = result["buys"]
    assert [b["ticker"] for b in buys] == ["AAA", "BBB"]  # largest gap first
    assert buys[0]["dollars"] == 60.0                      # AAA fully funded
    assert buys[1]["dollars"] == 40.0                      # BBB: only the $40 left
    assert result["cash_left"] == 0.0

    blocked_by_ticker = {r["ticker"]: r for r in result["blocked"]}
    assert "CCC" in blocked_by_ticker
    assert blocked_by_ticker["CCC"]["reason"] == "cash exhausted"
    assert blocked_by_ticker["CCC"]["dollars"] == 0


def test_gap_ordering_independent_of_dict_insertion_order():
    # Same fixture as above, but every dict built in ascending-gap order
    # (the opposite of the previous test) — output order must be identical.
    targets = _multi_tier_targets({"AAA": 60.0, "BBB": 50.0, "CCC": 30.0})
    roster = build_roster(targets)
    holdings = {"CCC": 0.0, "AAA": 0.0, "BBB": 0.0}
    metrics = _metrics(["BBB", "AAA", "CCC"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert [b["ticker"] for b in result["buys"]] == ["AAA", "BBB"]


# ── B. 200-SMA trend gate ────────────────────────────────────────────────

def test_trend_gate_blocks_downtrend_with_rsi_at_or_above_override():
    targets = _targets("XTR", weight_pct=50.0)
    roster = build_roster(targets)
    holdings = {"XTR": 0.0}
    metrics = {"XTR": {"price": 80.0, "rsi14": 35.0, "sma200": 100.0}}  # RSI 35 >= 30 override

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["buys"] == []
    blocked = result["blocked"]
    assert len(blocked) == 1
    assert blocked[0]["ticker"] == "XTR"
    assert blocked[0]["dollars"] == 0
    assert "downtrend" in blocked[0]["reason"]
    assert "px -20.0%" in blocked[0]["reason"]     # (80/100 - 1) * 100
    assert "RSI 35" in blocked[0]["reason"]


def test_trend_gate_passes_downtrend_with_rsi_strictly_below_override():
    targets = _targets("XTR", weight_pct=50.0)
    roster = build_roster(targets)
    holdings = {"XTR": 0.0}
    metrics = {"XTR": {"price": 80.0, "rsi14": 25.0, "sma200": 100.0}}  # RSI 25 < 30 override

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["blocked"] == []
    buys_by_ticker = {b["ticker"]: b for b in result["buys"]}
    assert "XTR" in buys_by_ticker
    assert buys_by_ticker["XTR"]["dollars"] == 50.0   # full target, cash not a constraint here


# ── C. earnings blackout ─────────────────────────────────────────────────

def test_earnings_none_does_not_block_and_preserves_unavailable_flag():
    targets = _targets("EARN", weight_pct=50.0)
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    # conftest.py's autouse fixture already returns None here; no override needed.

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["blocked"] == []
    buys_by_ticker = {b["ticker"]: b for b in result["buys"]}
    assert buys_by_ticker["EARN"]["dollars"] == 50.0
    assert buys_by_ticker["EARN"]["reason"] == "earnings:unavailable"


def test_earnings_inside_blackout_window_blocks(monkeypatch):
    targets = _targets("EARN", weight_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 3)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["buys"] == []
    blocked_by_ticker = {r["ticker"]: r for r in result["blocked"]}
    assert "earnings in 3d" in blocked_by_ticker["EARN"]["reason"]


def test_earnings_outside_blackout_window_permits(monkeypatch):
    targets = _targets("EARN", weight_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 8)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["blocked"] == []
    buys_by_ticker = {b["ticker"]: b for b in result["buys"]}
    assert buys_by_ticker["EARN"]["dollars"] == 50.0
    assert buys_by_ticker["EARN"]["reason"] == ""   # no flag set when de is a known, safe value


def test_earnings_blackout_lower_boundary_zero_blocks(monkeypatch):
    targets = _targets("EARN", weight_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 0)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    blocked_by_ticker = {r["ticker"]: r for r in result["blocked"]}
    assert "earnings in 0d" in blocked_by_ticker["EARN"]["reason"]


def test_earnings_blackout_upper_boundary_exact_days_blocks(monkeypatch):
    targets = _targets("EARN", weight_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 7)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    blocked_by_ticker = {r["ticker"]: r for r in result["blocked"]}
    assert "earnings in 7d" in blocked_by_ticker["EARN"]["reason"]


def test_earnings_blackout_one_day_past_upper_boundary_permits(monkeypatch):
    targets = _targets("EARN", weight_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 8)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["blocked"] == []
    assert {b["ticker"] for b in result["buys"]} == {"EARN"}


# ── D. band/spec RSI-hot opportunistic trim ──────────────────────────────

def _band_targets(weight_pct=20.0, trim_rsi=60.0):
    return {
        "tiers": {"band": {"weight_pct": weight_pct, "cap_multiple": 1.25,
                           "tickers": ["BND"]}},
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                  "earnings_blackout_days": 7, "trim_rsi": trim_rsi,
                  "t1t2_trim_mult": 100.0},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        "crypto": {},
    }


def test_band_overweight_hot_rsi_trims_to_own_target():
    targets = _band_targets(weight_pct=20.0, trim_rsi=60.0)
    roster = build_roster(targets)
    # holdings-only book (no cash): book = 30 -> target = 6, overweight_limit
    # (band's hardcoded 1.25x) = 7.5; current 30 is well above it.
    holdings = {"BND": 30.0}
    metrics = {"BND": {"price": 100.0, "rsi14": 70.0, "sma200": 90.0}}

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    trims_by_ticker = {t["ticker"]: t for t in result["trims"]}
    assert set(trims_by_ticker) == {"BND"}
    assert trims_by_ticker["BND"]["dollars"] == 24.0   # trimmed to target (6), not to 1.25x (7.5)
    assert "1.25x target" in trims_by_ticker["BND"]["reason"]
    assert "RSI 70.0>60" in trims_by_ticker["BND"]["reason"]


def test_band_overweight_rsi_exactly_at_threshold_does_not_trim():
    targets = _band_targets(weight_pct=20.0, trim_rsi=60.0)
    roster = build_roster(targets)
    holdings = {"BND": 30.0}   # same overweight setup as above
    metrics = {"BND": {"price": 100.0, "rsi14": 60.0, "sma200": 90.0}}  # RSI == threshold, not >

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    assert result["trims"] == []


def test_band_at_cap_hot_rsi_does_not_trim():
    targets = _band_targets(weight_pct=20.0, trim_rsi=60.0)
    roster = build_roster(targets)
    # cash makes up the rest of book so current can be pinned exactly to its
    # own overweight_limit: book=100 (BND 25 + cash 75) -> target=20,
    # overweight_limit=20*1.25=25 -> current(25) is AT the limit, not over it.
    holdings = {"BND": 25.0}
    metrics = {"BND": {"price": 100.0, "rsi14": 90.0, "sma200": 90.0}}

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=75.0)

    assert result["trims"] == []


# ── NUM-0001 P1-2: band trim must use the configured cap_multiple ──────────
# plan() previously hardcoded 1.25 in the trim-branch overweight_limit and
# reason string, ignoring band.cap_multiple already resolved into `cap_mult`
# one line earlier (and already used correctly by the buy-side ceiling). A
# cap_multiple other than 1.25 (e.g. 1.40) previously desynchronized the buy
# ceiling from the trim threshold; it must now control both identically.

def test_band_custom_cap_multiple_controls_trim_threshold_and_reason():
    targets = _band_targets(weight_pct=20.0, trim_rsi=60.0)
    targets["tiers"]["band"]["cap_multiple"] = 1.40
    roster = build_roster(targets)
    # book=100 (BND 40 + cash 60) -> target=20, overweight_limit=20*1.40=28;
    # current (40) is above it.
    holdings = {"BND": 40.0}
    metrics = {"BND": {"price": 100.0, "rsi14": 70.0, "sma200": 90.0}}

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=60.0)

    trims_by_ticker = {t["ticker"]: t for t in result["trims"]}
    assert set(trims_by_ticker) == {"BND"}
    assert trims_by_ticker["BND"]["dollars"] == 20.0   # trimmed to target (20), not to 1.40x (28)
    assert "1.40x target" in trims_by_ticker["BND"]["reason"]
    assert "RSI 70.0>60" in trims_by_ticker["BND"]["reason"]


def test_band_custom_cap_multiple_exactly_at_boundary_not_trimmed():
    targets = _band_targets(weight_pct=20.0, trim_rsi=60.0)
    targets["tiers"]["band"]["cap_multiple"] = 1.40
    roster = build_roster(targets)
    # book=100 (BND 28 + cash 72) -> target=20, overweight_limit=20*1.40=28
    # exactly -- current is AT the configured boundary, not over it.
    holdings = {"BND": 28.0}
    metrics = {"BND": {"price": 100.0, "rsi14": 90.0, "sma200": 90.0}}

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=72.0)

    assert result["trims"] == []
