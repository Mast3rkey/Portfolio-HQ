from copy import deepcopy
from decimal import Decimal

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


def test_current_frozen_gate_halts_on_disclosed_sol_gap_not_silent_fill():
    report = engine.build_data_gate()
    assert report.ready is False
    assert report.freeze["gate"] == "HALT"
    assert report.freeze["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"
    sol = [issue for issue in report.issues if issue.startswith("SOL:")]
    assert len(sol) == 1
    assert "required holdout observations missing" in sol[0]
    assert "pinned selected source bytes unavailable" in sol[0]


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
