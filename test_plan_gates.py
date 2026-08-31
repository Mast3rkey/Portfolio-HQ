"""Focused regression coverage for allocate.plan()'s gate/ordering branches
that had no deterministic test before this module:

  A. largest-dollar-gap allocation ordering + cash exhaustion
  B. the 200-SMA trend gate's blocking branch
  C. the earnings-blackout blocking branch
  D. PHQ-2026-02: no RSI-only opportunistic trim exists in the canonical
     destination architecture (retired policy proof -- see below)

Every fixture here uses synthetic tickers/targets/metrics only -- no
network, no real ticker calendars, no current-date dependence. The
repo-root conftest.py's autouse `no_live_earnings_lookup` fixture already
keeps the earnings lookup out of these tests by default (see conftest.py
for why patching `allocate.days_until_earnings` is the correct target);
section C overrides it explicitly per-case to drive the gate itself.

Cluster caps are deliberately kept out of every fixture below (neutral
tickers, no caps.clusters entries) since that mechanism has dedicated
coverage in test_margin.py -- mixing it in here would obscure which gate a
given assertion is actually proving.

PHQ-2026-02 migrated every fixture in this module from the retired tiered
(T1/T2/ETF/band/spec) targets.yaml schema to the canonical `destination:`
list schema (see governance/decisions/PHQ-2026-02-holdings-reconciliation-and-actionable-allocation-policy.md).
Section D previously covered the band/spec RSI-hot opportunistic trim,
which PHQ-2026-02 retired along with the tier concept it was defined in
terms of -- it is replaced below with tests proving that retirement, not
migrated to keep the old behavior alive.
"""

import allocate
from allocate import build_roster, plan


def _targets(ticker, target_pct=50.0, gates=None):
    return {
        "destination": [{"ticker": ticker, "target_pct": target_pct, "asset_class": "equity"}],
        "caps": {"clusters": []},
        "gates": {
            "min_lot_dollars": 1, "trend_rsi_override": 30,
            "earnings_blackout_days": 7,
            **(gates or {}),
        },
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }


def _multi_targets(weights: dict[str, float]):
    """One destination row per ticker, each with its own target_pct -- lets
    a single plan() call carry several independently-sized dollar gaps."""
    return {
        "destination": [
            {"ticker": tk, "target_pct": w, "asset_class": "equity"}
            for tk, w in weights.items()
        ],
        "caps": {"clusters": []},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                  "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }


def _metrics(tickers, price=100.0, rsi=50.0, sma200=90.0):
    return {t: {"price": price, "rsi14": rsi, "sma200": sma200} for t in tickers}


# ── A. largest-dollar-gap ordering + cash exhaustion ────────────────────────

def test_gap_ordering_fills_largest_first_partial_second_blocks_third():
    # RE-EXPRESSED, assertions unchanged. The old fixture summed target_pcts to
    # 140% of book so that total demand exceeded cash. A destination total above
    # 100% is now a hard configuration error -- the canonical architecture
    # cannot promise more capital than exists -- so the same condition is
    # produced the way a real book produces it: a large HELD position makes
    # book > cash. PAD holds $900 against a $860 target (overweight, so never a
    # buy candidate), cash is $100, book is $1,000, and AAA/BBB/CCC's targets
    # are the identical $60/$50/$30 the assertions below already expect.
    targets = _multi_targets({"AAA": 6.0, "BBB": 5.0, "CCC": 3.0, "PAD": 86.0})
    roster = build_roster(targets)
    # Insertion order deliberately reversed vs. expected gap-descending
    # output order (CCC, BBB, AAA) — insertion order must not leak through.
    holdings = {"CCC": 0.0, "BBB": 0.0, "AAA": 0.0, "PAD": 900.0}
    metrics = _metrics(["CCC", "BBB", "AAA", "PAD"])

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
    targets = _multi_targets({"AAA": 6.0, "BBB": 5.0, "CCC": 3.0, "PAD": 86.0})
    roster = build_roster(targets)
    holdings = {"CCC": 0.0, "AAA": 0.0, "BBB": 0.0, "PAD": 900.0}
    metrics = _metrics(["BBB", "AAA", "CCC", "PAD"])

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert [b["ticker"] for b in result["buys"]] == ["AAA", "BBB"]


# ── B. 200-SMA trend gate ────────────────────────────────────────────────

def test_trend_gate_blocks_downtrend_with_rsi_at_or_above_override():
    targets = _targets("XTR", target_pct=50.0)
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
    targets = _targets("XTR", target_pct=50.0)
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
    targets = _targets("EARN", target_pct=50.0)
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
    targets = _targets("EARN", target_pct=50.0, gates={"earnings_blackout_days": 7})
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
    targets = _targets("EARN", target_pct=50.0, gates={"earnings_blackout_days": 7})
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
    targets = _targets("EARN", target_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 0)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    blocked_by_ticker = {r["ticker"]: r for r in result["blocked"]}
    assert "earnings in 0d" in blocked_by_ticker["EARN"]["reason"]


def test_earnings_blackout_upper_boundary_exact_days_blocks(monkeypatch):
    targets = _targets("EARN", target_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 7)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    blocked_by_ticker = {r["ticker"]: r for r in result["blocked"]}
    assert "earnings in 7d" in blocked_by_ticker["EARN"]["reason"]


def test_earnings_blackout_one_day_past_upper_boundary_permits(monkeypatch):
    targets = _targets("EARN", target_pct=50.0, gates={"earnings_blackout_days": 7})
    roster = build_roster(targets)
    holdings = {"EARN": 0.0}
    metrics = _metrics(["EARN"])
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: 8)

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=100.0)

    assert result["blocked"] == []
    assert {b["ticker"] for b in result["buys"]} == {"EARN"}


# ── D. PHQ-2026-02: no RSI-only opportunistic trim survives ────────────────
# The prior band/spec tier carried its own opportunistic RSI-hot trim,
# independent of any cluster-cap breach. The canonical destination
# architecture has no tier concept, and PHQ-2026-02 does not invent an
# equivalent per-name trim rule in its place (see the governance filing's
# "Retired by this migration" section) — an overweight, hot-RSI destination
# row outside any correlated-cluster cap must simply never trim.

def _overweight_targets(target_pct=20.0):
    return {
        "destination": [{"ticker": "OWT", "target_pct": target_pct, "asset_class": "equity"}],
        "caps": {"clusters": []},   # deliberately not a member of any cluster
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                  "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }


def test_overweight_hot_rsi_position_outside_any_cluster_is_never_trimmed():
    targets = _overweight_targets(target_pct=20.0)
    roster = build_roster(targets)
    # book=30 (holdings only, no cash) -> target=6; current=30 is 5x target,
    # RSI is maximally "hot" (90) -- under the retired band/spec rule this
    # would have trimmed. Under the canonical architecture, with OWT in no
    # cluster, nothing mechanically trims an overweight position at all.
    holdings = {"OWT": 30.0}
    metrics = {"OWT": {"price": 100.0, "rsi14": 90.0, "sma200": 90.0}}

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    assert result["trims"] == []
    assert not any(b["ticker"] == "OWT" for b in result["buys"])   # overweight, not a buy either


def test_massively_overweight_position_at_any_rsi_still_not_trimmed():
    # RSI at the opposite extreme (cold, 10) -- proves the absence of a trim
    # isn't accidentally RSI-gated the other direction either; there is
    # simply no per-name opportunistic trim mechanism left to fire.
    targets = _overweight_targets(target_pct=5.0)
    roster = build_roster(targets)
    holdings = {"OWT": 100.0}   # book=100 -> target=5, current is 20x target
    metrics = {"OWT": {"price": 100.0, "rsi14": 10.0, "sma200": 90.0}}

    result = plan(targets, holdings, roster, metrics, regime_ok=True,
                 regime_known=True, cash=0.0)

    assert result["trims"] == []
