from copy import deepcopy
from decimal import Decimal
import hashlib
import json

import pytest

import whole_portfolio_robustness_engine as engine


def test_six_instrument_weight_sets_are_exact_and_reconciled():
    prereg = engine._yaml(engine.PREREG_PATH)
    targets = engine._yaml(engine.TARGETS_PATH)
    gates = engine._yaml(engine.GATES_PATH)
    variants = engine.derive_instrument_weights(targets, gates, prereg)
    assert set(variants) == {
        "BASELINE", "BROAD_PLUS_5", "DEFENSIVE_PLUS_5",
        "CRYPTO_HALF", "GOLD_PLUS_2", "DIVERSIFIED_BALANCE",
    }
    assert all(sum(weights.values()) == Decimal("100") for weights in variants.values())
    assert variants["BASELINE"]["CASH"] == Decimal("12.50")
    assert variants["BROAD_PLUS_5"]["CASH"] == Decimal("12.50")
    assert variants["DEFENSIVE_PLUS_5"]["CASH"] == Decimal("17.50")
    assert variants["CRYPTO_HALF"]["CASH"] == Decimal("14.50")
    assert variants["GOLD_PLUS_2"]["GLD"] == Decimal("6.00")
    assert variants["DIVERSIFIED_BALANCE"]["CASH"] == Decimal("15.50")

    direct = {
        row["ticker"] for row in targets["destination"]
        if row["asset_class"] == "equity" and row["ticker"] in variants["BASELINE"]
    }
    crypto = {
        row["ticker"] for row in targets["destination"]
        if row["asset_class"] == "crypto" and row["ticker"] in variants["BASELINE"]
    }
    members = {
        "eligible_direct_equity": direct,
        "broad_market_funds": engine.BROAD,
        "gold": engine.GOLD,
        "crypto": crypto,
        "cash_and_protected_capital": {"CASH"},
    }
    definitions = {row["id"]: row for row in prereg["variants"]["definitions"]}
    for variant_id, weights in variants.items():
        exact_sleeves = {
            sleeve: sum((weights[ticker] for ticker in tickers), Decimal("0"))
            for sleeve, tickers in members.items()
        }
        expected = {
            sleeve: Decimal(value)
            for sleeve, value in definitions[variant_id]["expected_sleeves_pct"].items()
        }
        assert exact_sleeves == expected


def test_gated_capital_is_cash_and_never_an_active_security():
    prereg = engine._yaml(engine.PREREG_PATH)
    targets = engine._yaml(engine.TARGETS_PATH)
    gates = engine._yaml(engine.GATES_PATH)
    variants = engine.derive_instrument_weights(targets, gates, prereg)
    gated = {row["ticker"] for row in gates["gates"]}
    assert gated == {"SNPS", "ICE", "SPGI", "WM", "RKLB", "TSLA"}
    assert all(not gated.intersection(weights) for weights in variants.values())


def test_no_renormalization_if_policy_total_changes():
    prereg = engine._yaml(engine.PREREG_PATH)
    targets = deepcopy(engine._yaml(engine.TARGETS_PATH))
    gates = engine._yaml(engine.GATES_PATH)
    targets["destination"][0]["target_pct"] = 106
    with pytest.raises(engine.DataGateError, match="100%"):
        engine.derive_instrument_weights(targets, gates, prereg)


def test_crypto_uses_only_lawfully_completed_prior_utc_close():
    sessions = ["2024-04-02", "2024-04-03"]
    assert engine._required_dates("crypto", sessions, "2024-04-02", "2024-04-03") == [
        "2024-04-01", "2024-04-02"
    ]
    assert engine._eligible_session_start("crypto", "2021-01-04", "2021-06-17") == "2021-06-18"
    assert engine._eligible_session_start("equity", "2021-01-04", "2021-06-17") == "2021-06-17"


def test_dff_validation_rejects_internal_calendar_gap_and_nonfinite_rate():
    doc = {
        "provider": "FRED", "series": "DFF",
        "rows": [
            {"date": "2024-04-01", "rate_pct": "5.33"},
            {"date": "2024-04-03", "rate_pct": "NaN"},
        ],
    }
    issues = engine._validate_dff(doc, "2024-04-01", "2024-04-03")
    assert "DFF: invalid rate on 2024-04-03" in issues
    assert any("2 required calendar observations missing" in issue for issue in issues)


def test_corporate_action_bytes_must_match_inventory_pin(tmp_path, monkeypatch):
    doc = {
        "provider": "ALPACA_CORPORATE_ACTIONS", "schema_version": "1.0",
        "rows": [{"id": "event-1", "action_type": "cash_dividend"}],
    }
    path = tmp_path / "alpaca_actions.json"
    payload = json.dumps(doc, sort_keys=True).encode()
    path.write_bytes(payload)
    monkeypatch.setattr(engine, "ACTION_PATH", path)
    monkeypatch.setattr(engine, "ROOT", tmp_path)
    inventory = {"corporate_actions": {
        "error": None, "type_failures": {}, "row_count": 1,
        "transformed_path": "alpaca_actions.json",
        "transformed_sha256": hashlib.sha256(payload).hexdigest(),
    }}
    assert engine._validate_actions(inventory)[1] == []
    path.write_text("{}", encoding="utf-8")
    assert engine._validate_actions(inventory)[1] == ["corporate actions: frozen hash mismatch"]


def test_missing_candidate_file_returns_halt_receipt_not_traceback(monkeypatch):
    real_candidate_path = engine._candidate_path
    missing = engine.ROOT / "missing-SOL-test.json"
    assert not missing.exists()
    monkeypatch.setattr(
        engine, "_candidate_path",
        lambda ticker, kind: missing if ticker == "SOL" else real_candidate_path(ticker, kind),
    )
    report = engine.build_data_gate()
    assert report.ready is False
    assert report.freeze["datasets"]["SOL"]["sha256"] is None
    assert any("SOL: unreadable candidate" in issue for issue in report.issues)


def test_current_frozen_gate_halts_on_disclosed_sol_gap_not_silent_fill():
    report = engine.build_data_gate()
    assert report.ready is False
    assert report.freeze["gate"] == "HALT"
    assert report.freeze["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"
    sol = [issue for issue in report.issues if issue.startswith("SOL:")]
    assert len(sol) == 2
    assert any("required confirmation observations missing" in issue for issue in sol)
    assert any("102 required holdout_all_current_assets observations missing" in issue for issue in sol)
    assert all("pinned selected source bytes unavailable" in issue for issue in sol)
    assert not [issue for issue in report.issues if not issue.startswith("SOL:")]
    assert report.freeze["corporate_action_count"] == 820
    assert report.freeze["corporate_actions_sha256"] == (
        "a75341f1279665423722074fbc3c89eed2a0c4708e8aefcd658220c3e7bc83b2"
    )


def test_require_ready_refuses_to_emit_results_from_incomplete_input():
    with pytest.raises(engine.DataGateError, match="data gate halted"):
        engine.require_ready()


def test_engine_has_no_brokerage_holdings_margin_or_stage1_dependency():
    source = engine.Path(engine.__file__).read_text(encoding="utf-8")
    for prohibited in (
        "import alpaca_client", "import allocate", "import holdings",
        "import margin_state", "import level1_stage1",
    ):
        assert prohibited not in source
