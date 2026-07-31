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

import allocate
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


def test_spcx_and_skhy_pre_exit_quantities_retained_as_evidence():
    """SPCX/SKHY's PHQ-2026-02 reconciled quantities (0.502727 / 0.278473)
    are frozen historical evidence, not live holdings.yaml facts, following
    PHQ-2026-04's factual sync of the principal's verified manual exit of
    both names (see governance/decisions/PHQ-2026-04-skhy-spcx-post-execution-factual-synchronization.md)."""
    holdings = yaml.safe_load((HERE / "holdings.yaml").read_text())
    assert "SPCX" not in holdings["shares"]
    assert "SKHY" not in holdings["shares"]


def test_cash_and_zero_margin_state():
    holdings = yaml.safe_load((HERE / "holdings.yaml").read_text())
    assert holdings["margin"]["debt"] == 0.0


def test_no_market_value_forced_reconciliation():
    """Quantities, not screenshot market values, are what was written into
    holdings.yaml — spot-check one row against its own reference market value
    (which does NOT equal qty * a round price, proving no value was invented
    to force reconciliation). The frozen v1.35 evidence CSV's own SPCX row is
    checked directly (unaffected by SPCX's later PHQ-2026-04 exit); the live
    holdings.yaml spot-check uses AMZN instead of SPCX since SPCX is no
    longer a holding post-exit."""
    csv_text = (HERE / "governance/evidence/PHQ-2026-02/v1_35/"
                "Portfolio_HQ_Post_Execution_Holdings_v1_35.csv").read_text()
    assert "SPCX,private/other,0.502727" in csv_text
    holdings = yaml.safe_load((HERE / "holdings.yaml").read_text())
    assert holdings["shares"]["AMZN"] == 0.423377


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
    # none of the gated names ever appears as a BUY (6 post PHQ-2026-04's
    # retirement of SPCX's gate after its verified exit -- originally 7)
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

def test_spcx_fully_exited_no_target_no_gate(targets, roster, gates_cfg):
    """Replaces the historical test_spcx_hold_no_add, which tested SPCX's
    pre-exit held/gated state. PHQ-2026-04 retired SPCX's targets.yaml row
    and gates.yaml hold_no_add entry after the principal's verified manual
    exit (0 sh remaining) — SPCX is no longer a canonical target or a gated
    name."""
    assert "SPCX" not in roster
    assert "SPCX" not in gates_cfg


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


# ── 8. MAJOR 1 (independent review, PR #202): gates.yaml fails loudly ──────
# load_gates() must never silently return {} for missing/unreadable/
# malformed/structurally-invalid gates.yaml -- an empty fallback would let a
# normally-gated ticker (e.g. SPCX) become an ordinary, unflagged BUY
# candidate with no warning anywhere in output.

def test_gates_missing_file_raises_and_names_gates_yaml(tmp_path, monkeypatch):
    monkeypatch.setattr(allocate, "GATES_FILE", tmp_path / "does_not_exist.yaml")
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_unreadable_path_raises(tmp_path, monkeypatch):
    # A directory where a file is expected reliably raises OSError on
    # read_text() without needing unsafe chmod/permission changes.
    bad_path = tmp_path / "gates.yaml"
    bad_path.mkdir()
    monkeypatch.setattr(allocate, "GATES_FILE", bad_path)
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_malformed_yaml_raises(tmp_path, monkeypatch):
    bad_path = tmp_path / "gates.yaml"
    bad_path.write_text("gates: [ticker: SPCX\n  status: broken indentation :::")
    monkeypatch.setattr(allocate, "GATES_FILE", bad_path)
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_wrong_top_level_type_raises(tmp_path, monkeypatch):
    bad_path = tmp_path / "gates.yaml"
    bad_path.write_text("- just\n- a\n- list\n")   # not a mapping at all
    monkeypatch.setattr(allocate, "GATES_FILE", bad_path)
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_missing_gates_key_raises(tmp_path, monkeypatch):
    bad_path = tmp_path / "gates.yaml"
    bad_path.write_text("not_gates: []\n")   # valid YAML, wrong top-level key
    monkeypatch.setattr(allocate, "GATES_FILE", bad_path)
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_entries_not_a_list_raises(tmp_path, monkeypatch):
    bad_path = tmp_path / "gates.yaml"
    bad_path.write_text("gates: {ticker: SPCX}\n")   # a mapping, not a list
    monkeypatch.setattr(allocate, "GATES_FILE", bad_path)
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_entry_missing_ticker_raises(tmp_path, monkeypatch):
    bad_path = tmp_path / "gates.yaml"
    bad_path.write_text("gates:\n  - status: cash_pending_clearance\n")   # no ticker field
    monkeypatch.setattr(allocate, "GATES_FILE", bad_path)
    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.load_gates()


def test_gates_valid_configuration_loads_correctly(tmp_path, monkeypatch):
    good_path = tmp_path / "gates.yaml"
    good_path.write_text(
        "gates:\n"
        "  - ticker: SPCX\n"
        "    status: hold_no_add\n"
        "    authority: PHQ-2026-01\n"
        "    allow_add: false\n"
        "    next_gate: test\n")
    monkeypatch.setattr(allocate, "GATES_FILE", good_path)
    loaded = allocate.load_gates()
    assert loaded == {"SPCX": {"ticker": "SPCX", "status": "hold_no_add",
                               "authority": "PHQ-2026-01", "allow_add": False,
                               "next_gate": "test"}}


def test_spcx_never_a_buy_candidate_when_gate_loading_fails(tmp_path, monkeypatch):
    """Proves the fail-loud behavior actually protects the allocator: with a
    broken gates.yaml, main()'s production path raises before plan() ever
    runs, so no recommendation -- gated or otherwise -- is ever produced
    using an unverified empty gate set."""
    import sys
    import yaml as _yaml

    targets_file = tmp_path / "targets.yaml"
    holdings_file = tmp_path / "holdings.yaml"
    broken_gates_file = tmp_path / "gates.yaml"
    with targets_file.open("w") as f:
        _yaml.safe_dump({
            "destination": [{"ticker": "SPCX", "target_pct": 5.0, "asset_class": "equity"}],
            "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7},
            "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
        }, f)
    with holdings_file.open("w") as f:
        _yaml.safe_dump({
            "holdings": {}, "shares": {"SPCX": 1.0}, "crypto_shares": {},
            "margin": {"debt": 0.0, "buffer_pct": 100.0, "synced_at": "2026-07-31"},
        }, f)
    # gates.yaml simply absent -> load_gates() must raise before any output.

    monkeypatch.setattr(allocate, "TARGETS_FILE", targets_file)
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", holdings_file)
    monkeypatch.setattr(allocate, "GATES_FILE", broken_gates_file)
    monkeypatch.setattr(sys, "argv", ["allocate.py", "--review", "--no-log"])

    with pytest.raises(ValueError, match="gates.yaml"):
        allocate.main()


# ── 9. MAJOR 2 (independent review, PR #202): gated/non-tradable rows can
# never enter a mechanical cluster trim, even if misconfigured into one ──

def _cluster_membership_targets(members, cap_pct=5.0):
    return {
        "destination": [
            {"ticker": tk, "target_pct": 5.0, "asset_class": asset_class}
            for tk, asset_class in members
        ],
        "caps": {"clusters": [{"name": "testcluster", "pct": cap_pct,
                              "tickers": [tk for tk, _ in members]}]},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }


def test_gated_ticker_in_cluster_is_never_trimmed():
    targets = _cluster_membership_targets([("SPCX", "equity"), ("NORM", "equity")])
    roster = build_roster(targets)
    gates_cfg = {"SPCX": {"status": "hold_no_add", "authority": "PHQ-2026-01",
                          "next_gate": "test"}}
    # Both way overweight vs. a tight 5% cap -- SPCX (gated) must never be a
    # trim candidate; NORM (ungated) legitimately fires the cluster trim.
    holdings = {"SPCX": 500.0, "NORM": 500.0}
    metrics = _flat_metrics(["SPCX", "NORM"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                 gates_cfg=gates_cfg, lookthrough={})

    assert not any(t["ticker"] == "SPCX" for t in result["trims"])
    assert any(t["ticker"] == "NORM" for t in result["trims"])


def test_gated_production_ticker_cannot_be_mechanically_trimmed_via_cluster(targets, gates_cfg, lookthrough):
    """Uses the real, production targets.yaml/gates.yaml. SNPS (still gated,
    still carries a real destination row) is not currently a member of any
    cluster, but this proves the guard holds even if a future edit
    mistakenly adds a gated name to one. Formerly used SPCX for this —
    PHQ-2026-04 removed SPCX's own destination row after its verified exit,
    so SPCX can no longer serve as this test's subject."""
    mutated = json.loads(json.dumps(targets))   # deep copy, safe to mutate
    mutated["caps"]["clusters"].append(
        {"name": "misconfigured_test_cluster", "pct": 0.01, "tickers": ["SNPS"]})
    roster = build_roster(mutated)
    holdings = {"SNPS": 5000.0}   # wildly overweight vs. any real target
    metrics = _flat_metrics(["SNPS"])
    result = plan(mutated, holdings, roster, metrics, True, True, cash=0.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)

    assert not any(t["ticker"] == "SNPS" for t in result["trims"])


def test_cash_in_cluster_is_never_trimmed():
    targets = _cluster_membership_targets([("CASH", "cash"), ("NORM", "equity")])
    roster = build_roster(targets)
    holdings = {"CASH": 500.0, "NORM": 500.0}
    metrics = _flat_metrics(["NORM"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                 gates_cfg={}, lookthrough={})

    assert not any(t["ticker"] == "CASH" for t in result["trims"])


def test_reserve_in_cluster_is_never_trimmed():
    targets = _cluster_membership_targets([("RESERVE", "reserve"), ("NORM", "equity")])
    roster = build_roster(targets)
    holdings = {"RESERVE": 500.0, "NORM": 500.0}
    metrics = _flat_metrics(["NORM"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                 gates_cfg={}, lookthrough={})

    assert not any(t["ticker"] == "RESERVE" for t in result["trims"])


def test_normal_tradable_cluster_member_still_trims_as_governed():
    targets = _cluster_membership_targets([("NORM", "equity")], cap_pct=1.0)
    roster = build_roster(targets)
    holdings = {"NORM": 100.0}   # target=5 (5% of book 100), cap_dollars=1
    metrics = _flat_metrics(["NORM"])
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                 gates_cfg={}, lookthrough={})

    trimmed = next((t for t in result["trims"] if t["ticker"] == "NORM"), None)
    assert trimmed is not None
    assert trimmed["dollars"] == 95.0   # trimmed to its own target (5), floored there


def test_multi_cluster_membership_remains_deterministic_with_gated_member():
    # NORM is in two clusters; SPCX (gated) shares one of them. Repeated runs
    # must produce identical output, and SPCX must never appear in trims in
    # either.
    targets = {
        "destination": [
            {"ticker": "NORM", "target_pct": 5.0, "asset_class": "equity"},
            {"ticker": "SPCX", "target_pct": 5.0, "asset_class": "equity"},
        ],
        "caps": {"clusters": [
            {"name": "clusterA", "pct": 1.0, "tickers": ["NORM", "SPCX"]},
            {"name": "clusterB", "pct": 1.0, "tickers": ["NORM"]},
        ]},
        "gates": {"min_lot_dollars": 1, "trend_rsi_override": 30,
                 "earnings_blackout_days": 7},
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }
    roster = build_roster(targets)
    gates_cfg = {"SPCX": {"status": "hold_no_add", "authority": "PHQ-2026-01",
                          "next_gate": "test"}}
    holdings = {"NORM": 100.0, "SPCX": 100.0}
    metrics = _flat_metrics(["NORM", "SPCX"])

    result_a = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                    gates_cfg=gates_cfg, lookthrough={})
    result_b = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                    gates_cfg=gates_cfg, lookthrough={})

    assert result_a["trims"] == result_b["trims"]   # deterministic
    assert not any(t["ticker"] == "SPCX" for t in result_a["trims"])
    assert any(t["ticker"] == "NORM" for t in result_a["trims"])


def test_no_gated_or_nontradable_row_ever_in_trims_real_config(targets, gates_cfg, lookthrough):
    """Stress the real production config/gates with every gated ticker and
    every reserve/cash row heavily overweight -- none may ever appear as a
    trim recommendation."""
    roster = build_roster(targets)
    non_tradable = {tk for tk, meta in roster.items()
                    if meta["asset_class"] in ("reserve", "cash")} | set(gates_cfg)
    holdings = {tk: 100000.0 for tk in roster}   # everything wildly overweight
    metrics = _flat_metrics(roster)
    result = plan(targets, holdings, roster, metrics, True, True, cash=0.0,
                 gates_cfg=gates_cfg, lookthrough=lookthrough)

    trimmed_tickers = {t["ticker"] for t in result["trims"]}
    assert not (trimmed_tickers & non_tradable)


# ── 10. MAJOR 3 + destination-row validation (independent review, PR #202) ──
# build_roster() must validate every destination row at parse time: exact,
# case-sensitive asset_class vocabulary, and well-formed ticker/target_pct.

def _row(ticker="AAA", target_pct=5.0, asset_class="equity"):
    row = {}
    if ticker is not _MISSING:
        row["ticker"] = ticker
    if target_pct is not _MISSING:
        row["target_pct"] = target_pct
    if asset_class is not _MISSING:
        row["asset_class"] = asset_class
    return row


_MISSING = object()


def _targets_with_rows(*rows):
    return {"destination": list(rows), "caps": {"clusters": []},
            "gates": {"min_lot_dollars": 1}, "margin": {"leverage_cap": 1.8,
            "buffer_floor_pct": 30.0}}


@pytest.mark.parametrize("asset_class", ["equity", "fund", "crypto", "reserve", "cash"])
def test_every_currently_valid_asset_class_accepted(asset_class):
    targets = _targets_with_rows(_row(asset_class=asset_class))
    roster = build_roster(targets)
    assert roster["AAA"]["asset_class"] == asset_class


def test_missing_asset_class_rejected():
    targets = _targets_with_rows(_row(asset_class=_MISSING))
    with pytest.raises(ValueError, match="asset_class"):
        build_roster(targets)


def test_null_asset_class_rejected():
    targets = _targets_with_rows(_row(asset_class=None))
    with pytest.raises(ValueError, match="asset_class"):
        build_roster(targets)


def test_blank_asset_class_rejected():
    targets = _targets_with_rows(_row(asset_class=""))
    with pytest.raises(ValueError, match="asset_class"):
        build_roster(targets)


def test_whitespace_only_asset_class_rejected():
    targets = _targets_with_rows(_row(asset_class="   "))
    with pytest.raises(ValueError, match="asset_class"):
        build_roster(targets)


def test_unknown_asset_class_rejected():
    targets = _targets_with_rows(_row(asset_class="bond"))
    with pytest.raises(ValueError, match="asset_class"):
        build_roster(targets)


def test_wrong_case_reserve_rejected_not_normalized():
    targets = _targets_with_rows(_row(asset_class="Reserve"))
    with pytest.raises(ValueError, match="asset_class"):
        build_roster(targets)


def test_cash_and_reserve_remain_non_tradable():
    targets = _targets_with_rows(
        _row(ticker="CASHROW", asset_class="cash"),
        _row(ticker="RESERVEROW", asset_class="reserve"))
    roster = build_roster(targets)
    holdings = {}
    metrics = {}
    result = plan(targets, holdings, roster, metrics, True, True, cash=1000.0,
                 gates_cfg={}, lookthrough={})
    assert not any(b["ticker"] in ("CASHROW", "RESERVEROW") for b in result["buys"])
    assert not any(u["ticker"] in ("CASHROW", "RESERVEROW") for u in result["underweight"])


def test_missing_ticker_rejected():
    targets = _targets_with_rows(_row(ticker=_MISSING))
    with pytest.raises(ValueError, match="ticker"):
        build_roster(targets)


def test_blank_ticker_rejected():
    targets = _targets_with_rows(_row(ticker="   "))
    with pytest.raises(ValueError, match="ticker"):
        build_roster(targets)


def test_duplicate_ticker_rejected():
    targets = _targets_with_rows(_row(ticker="DUP"), _row(ticker="DUP"))
    with pytest.raises(ValueError, match="duplicate"):
        build_roster(targets)


def test_missing_target_pct_rejected():
    targets = _targets_with_rows(_row(target_pct=_MISSING))
    with pytest.raises(ValueError, match="target_pct"):
        build_roster(targets)


def test_non_numeric_target_pct_rejected():
    targets = _targets_with_rows(_row(target_pct="a lot"))
    with pytest.raises(ValueError, match="target_pct"):
        build_roster(targets)


def test_negative_target_pct_rejected():
    targets = _targets_with_rows(_row(target_pct=-1.0))
    with pytest.raises(ValueError, match="target_pct"):
        build_roster(targets)


def test_invalid_row_error_identifies_the_offending_row():
    targets = _targets_with_rows(_row(ticker="GOOD"), _row(ticker="BAD", asset_class="bogus"))
    with pytest.raises(ValueError, match=r"row #1.*BAD|BAD.*row #1"):
        build_roster(targets)


def test_real_targets_yaml_passes_all_validation(targets):
    # The canonical v1.30 config (36 rows post PHQ-2026-04's removal of
    # SPCX's row after its verified exit -- originally 37) must validate
    # cleanly -- proves the new validation doesn't reject legitimate,
    # already-approved destination rows.
    roster = build_roster(targets)
    assert len(roster) == 36
