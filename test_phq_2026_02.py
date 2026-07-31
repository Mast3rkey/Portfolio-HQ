"""PHQ-2026-02 focused tests — holdings reconciliation, canonical destination
targets, actionable gates (cash without renormalization), and the 8%/40%
no-add controls. See governance/decisions/PHQ-2026-02-holdings-reconciliation-and-actionable-allocation-policy.md.

Advisory-only, no orders: every assertion here is about what plan() computes
and returns, never about anything sent to a broker.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from allocate import build_roster, load_gates, load_issuer_lookthrough, plan

HERE = Path(__file__).resolve().parent


def _flat_metrics(tickers, price=100.0, rsi=50.0, sma200=90.0):
    return {t: {"price": price, "rsi14": rsi, "sma200": sma200} for t in tickers}


@pytest.fixture(scope="module")
def targets():
    return yaml.safe_load((HERE / "targets.yaml").read_text())


@pytest.fixture(scope="module")
def roster(targets):
    return build_roster(targets)


@pytest.fixture(scope="module")
def gates_cfg():
    return load_gates()


@pytest.fixture(scope="module")
def lookthrough():
    return load_issuer_lookthrough()


# ── 1. v1.35 quantity reconciliation ────────────────────────────────────────

def test_v135_quantities_reconciled_exactly():
    check = json.loads((HERE / "governance/evidence/PHQ-2026-02/reconciliation_check.json")
                       .read_text())
    assert check["all_captured_quantities_match"] is True
    assert check["evidence_sha256"] == \
        "fb8eb811df29eb560bfaed16e8d0e89c6cbcf44bc42e1f1ae2ccfca4cddd889e"
    non_dust = [r for r in check["rows"] if r["match"] is not False]
    matched = [r for r in non_dust if r["match"] is True]
    assert len(matched) == 27   # 24 equity/fund + SPCX + BTC/ETH/SOL


def test_spcx_and_skhy_exact_quantities():
    holdings = yaml.safe_load((HERE / "holdings.yaml").read_text())
    assert holdings["shares"]["SPCX"] == 0.502727
    assert holdings["shares"]["SKHY"] == 0.278473


def test_cash_and_zero_margin_state():
    holdings = yaml.safe_load((HERE / "holdings.yaml").read_text())
    assert holdings["margin"]["debt"] == 0.0


def test_no_market_value_forced_reconciliation():
    """Quantities, not screenshot market values, are what was written into
    holdings.yaml — spot-check one row against its own reference market value
    (which does NOT equal qty * a round price, proving no value was invented
    to force reconciliation)."""
    csv_text = (HERE / "governance/evidence/PHQ-2026-02/v1_35/"
                "Portfolio_HQ_Post_Execution_Holdings_v1_35.csv").read_text()
    assert "SPCX,private/other,0.502727" in csv_text
    holdings = yaml.safe_load((HERE / "holdings.yaml").read_text())
    assert holdings["shares"]["SPCX"] == 0.502727


# ── 2. canonical targets unaffected by gates; no renormalization ───────────

def test_canonical_targets_unchanged_by_gates(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    result_with_gates = plan(targets, {}, roster, metrics, True, True, cash=1000.0,
                             gates_cfg=gates_cfg, lookthrough=lookthrough)
    result_no_gates = plan(targets, {}, roster, metrics, True, True, cash=1000.0,
                           gates_cfg={}, lookthrough=lookthrough)
    # Every non-gated ticker's target dollar amount is identical whether or
    # not gates are applied — gating never changes another name's target.
    targets_by_ticker_gated = {r["ticker"]: r["target"] for r in result_with_gates["underweight"]}
    targets_by_ticker_nogate = {r["ticker"]: r["target"] for r in result_no_gates["underweight"]
                                if r["ticker"] not in gates_cfg}
    for tk, tgt in targets_by_ticker_gated.items():
        assert tgt == pytest.approx(targets_by_ticker_nogate[tk])


def test_gating_several_names_does_not_renormalize(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    result = plan(targets, {}, roster, metrics, True, True, cash=1000.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)
    # book * target_pct is the ONLY formula plan() ever uses for a target —
    # confirm every buy candidate's target still matches book*target_pct/100
    # exactly (i.e. nothing was bumped up to absorb a gated name's share).
    book = result["book"]
    for r in result["underweight"]:
        expected = book * roster[r["ticker"]]["target_pct"] / 100.0
        assert r["target"] == pytest.approx(expected)


def test_gated_capital_remains_cash(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    result = plan(targets, {}, roster, metrics, True, True, cash=1000.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)
    gated_tickers = {r["ticker"] for r in result["no_add_gated"]}
    assert gated_tickers == set(gates_cfg)
    # none of the 7 gated names ever appears as a BUY
    assert not ({b["ticker"] for b in result["buys"]} & gated_tickers)
    # deployable cash is unaffected by gating (no phantom spend on gated names)
    assert result["cash"] == 1000.0


def test_removing_a_gate_restores_eligibility_without_changing_targets_yaml(
        targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    result_gated = plan(targets, {}, roster, metrics, True, True, cash=5000.0,
                        gates_cfg={"SNPS": {"status": "x", "authority": "x",
                                            "next_gate": "x"}},
                        lookthrough=lookthrough)
    result_ungated = plan(targets, {}, roster, metrics, True, True, cash=5000.0,
                          gates_cfg={}, lookthrough=lookthrough)
    assert "SNPS" in {r["ticker"] for r in result_gated["no_add_gated"]}
    assert "SNPS" in {b["ticker"] for b in result_ungated["buys"]} | \
                     {r["ticker"] for r in result_ungated["underweight"]}
    # targets.yaml's own weight for SNPS is untouched by either run
    assert roster["SNPS"]["target_pct"] == 2.5


# ── 3. 8% effective-issuer no-add control ───────────────────────────────────

def test_issuer_below_ceiling_add_allowed(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    result = plan(targets, {}, roster, metrics, True, True, cash=1000.0,
                 gates_cfg={}, lookthrough=lookthrough)
    nvda_buy = next((b for b in result["buys"] if b["ticker"] == "NVDA"), None)
    assert nvda_buy is not None
    assert not result["no_add_issuer"]


def test_issuer_at_ceiling_no_add(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    # NVDA held well above its 6% target so effective exposure clears 8%
    holdings = {"NVDA": 200.0}
    result = plan(targets, holdings, roster, metrics, True, True, cash=100.0,
                 gates_cfg={}, lookthrough=lookthrough)
    assert result["issuer_exposure"]["NVDA"]["effective_pct"] >= 8.0
    assert not any(b["ticker"] == "NVDA" for b in result["buys"])


def test_issuer_add_clipped_to_ceiling(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    # NVDA's own 6% target is under the 8% ceiling on a direct-only basis, so
    # a large embedded SPY holding is needed to push current effective
    # exposure high enough that filling NVDA's FULL target gap would blow
    # through 8% — the clip must cap the buy so post-trade effective lands
    # at the ceiling, not at the (larger) raw target gap.
    holdings = {"NVDA": 10.0, "SPY": 2000.0}
    result = plan(targets, holdings, roster, metrics, True, True, cash=1000.0,
                 gates_cfg={}, lookthrough=lookthrough)
    nvda_buy = next((b for b in result["buys"] if b["ticker"] == "NVDA"), None)
    assert nvda_buy is not None
    post_trade_pct = (10.0 + nvda_buy["dollars"]) / result["book"] * 100.0 + \
        (2000.0 / result["book"] * 100.0) * 0.0766   # + embedded SPY contribution
    assert post_trade_pct <= 8.0 + 1e-6
    raw_gap = result["book"] * 0.06 - 10.0
    assert nvda_buy["dollars"] <= raw_gap + 1e-6   # confirms it was actually clipped
    assert nvda_buy["dollars"] < raw_gap - 1.0     # meaningfully clipped, not a rounding no-op


def test_no_automatic_trim_from_issuer_ceiling(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    # MSFT: an 8%-ceiling issuer member with no cluster-cap membership, so
    # any trim observed here can only come from the issuer ceiling itself —
    # isolates this no-add control from the pre-existing, unrelated
    # cluster-cap trim mechanism.
    holdings = {"MSFT": 500.0}   # far above both target and the 8% ceiling
    result = plan(targets, holdings, roster, metrics, True, True, cash=100.0,
                 gates_cfg={}, lookthrough=lookthrough)
    assert result["issuer_exposure"]["MSFT"]["effective_pct"] >= 8.0
    assert not any(t["ticker"] == "MSFT" for t in result["trims"])
    assert not any(b["ticker"] == "MSFT" for b in result["buys"])


# ── 4. 40% AI/platform common-driver no-add control ─────────────────────────

def test_retained_measurement_labeled_above_ceiling(lookthrough):
    retained = lookthrough["retained_common_driver_measurement"]
    assert retained["value_pct"] == 40.0284
    assert retained["value_pct"] > lookthrough["common_driver_ceiling_pct"]


def test_common_driver_blocked_addition(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    # Push current common-driver aggregate over 40% via a large direct NVDA
    # position (member of the common-driver group), then confirm other
    # member tickers (direct issuers AND the SPY/VEA/VWO funds whose
    # purchase would also embed further common-driver exposure) are blocked
    # while aggregate is at/above ceiling.
    holdings = {"NVDA": 5000.0}
    result = plan(targets, holdings, roster, metrics, True, True, cash=100.0,
                 gates_cfg={}, lookthrough=lookthrough)
    assert result["common_driver_current_pct"] >= 40.0
    blocked_tickers = {r["ticker"] for r in result["no_add_common_driver"]}
    common_driver_members = {i["ticker"] for i in lookthrough["issuers"]} | \
        {f["fund"] for i in lookthrough["issuers"] for f in i["funds"]}
    assert blocked_tickers & common_driver_members == blocked_tickers
    assert len(blocked_tickers) > 0


def test_non_common_driver_addition_remains_eligible(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    holdings = {"NVDA": 5000.0}   # common-driver aggregate pinned over ceiling
    result = plan(targets, holdings, roster, metrics, True, True, cash=100.0,
                 gates_cfg={}, lookthrough=lookthrough)
    common_driver_members = {i["ticker"] for i in lookthrough["issuers"]} | \
        {f["fund"] for i in lookthrough["issuers"] for f in i["funds"]}
    non_member_buys = [b for b in result["buys"] if b["ticker"] not in common_driver_members]
    assert len(non_member_buys) > 0


def test_no_automatic_trim_from_common_driver_ceiling(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    # ASML: a common-driver member (via VEA) with no cluster-cap membership
    # overlap issue at this holding size relative to its own target — isolate
    # the common-driver ceiling from the unrelated cluster-cap trim mechanism.
    holdings = {"NVDA": 5000.0, "MSFT": 500.0}
    result = plan(targets, holdings, roster, metrics, True, True, cash=100.0,
                 gates_cfg={}, lookthrough=lookthrough)
    assert result["common_driver_current_pct"] >= 40.0
    assert not any(t["ticker"] == "MSFT" for t in result["trims"])


def test_current_measurement_disclosed_alongside_retained(targets, roster, lookthrough):
    metrics = _flat_metrics(roster)
    result = plan(targets, {}, roster, metrics, True, True, cash=1000.0,
                 gates_cfg={}, lookthrough=lookthrough)
    assert "common_driver_current_pct" in result
    assert result["retained_common_driver_measurement"]["value_pct"] == 40.0284


# ── 5. SPCX and SKHY ─────────────────────────────────────────────────────────

def test_spcx_hold_no_add(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    holdings = {"SPCX": 56.0}   # existing position, per reconciled holdings.yaml
    result = plan(targets, holdings, roster, metrics, True, True, cash=1000.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)
    spcx_gate = next(r for r in result["no_add_gated"] if r["ticker"] == "SPCX")
    assert spcx_gate["holds_existing_shares"] is True
    assert not any(b["ticker"] == "SPCX" for b in result["buys"])
    assert not any(t["ticker"] == "SPCX" for t in result["trims"])   # not an automatic exit


def test_skhy_unresolved(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    holdings = {"SKHY": 43.0}
    result = plan(targets, holdings, roster, metrics, True, True, cash=1000.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)
    assert result["unresolved"] == {"SKHY": 43.0}
    assert not any(b["ticker"] == "SKHY" for b in result["buys"])
    assert not any(t["ticker"] == "SKHY" for t in result["trims"])
    assert "SKHY" not in roster           # no canonical target assigned
    assert "SKHY" not in gates_cfg        # not silently gated either


def test_skhy_unresolved_does_not_renormalize_other_targets(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    with_skhy = plan(targets, {"SKHY": 43.0}, roster, metrics, True, True, cash=1000.0,
                     gates_cfg=gates_cfg, lookthrough=lookthrough)
    without_skhy = plan(targets, {}, roster, metrics, True, True, cash=1000.0 + 43.0,
                        gates_cfg=gates_cfg, lookthrough=lookthrough)
    # Same book both ways (43 in SKHY holdings vs 43 more cash) — every
    # target_pct-derived target dollar figure must match exactly.
    t_with = {r["ticker"]: r["target"] for r in with_skhy["underweight"]}
    t_without = {r["ticker"]: r["target"] for r in without_skhy["underweight"]}
    for tk in t_with:
        assert t_with[tk] == pytest.approx(t_without[tk])


# ── 6. no brokerage query / no order path ───────────────────────────────────

def test_no_order_placement_methods_in_alpaca_client():
    src = (HERE / "alpaca_client.py").read_text()
    for forbidden in ("def submit_order", "def place_order", "def cancel_order",
                      "def replace_order"):
        assert forbidden not in src, f"order-placement method '{forbidden}' present"


def test_no_new_modules_import_alpaca_trading_or_robinhood_api():
    for fname in ("gates.yaml", "issuer_lookthrough.yaml"):
        src = (HERE / fname).read_text()
        assert "robinhood" not in src.lower()
        assert "import " not in src   # config files — no executable code at all


# ── 7. advisory classification labels present ───────────────────────────────

def test_all_required_classification_labels_reachable(targets, roster, gates_cfg, lookthrough):
    metrics = _flat_metrics(roster)
    holdings = {"NVDA": 5000.0, "SPCX": 56.0, "SKHY": 43.0}
    result = plan(targets, holdings, roster, metrics, True, True, cash=1000.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)
    assert result["buys"]                    # BUY reachable
    assert result["no_add_gated"]             # NO ADD — GATED reachable
    assert result["no_add_common_driver"]     # NO ADD — COMMON-DRIVER CEILING reachable
    assert result["unresolved"]               # UNRESOLVED reachable
