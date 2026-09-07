from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import pytest

import whole_portfolio_robustness_result_validator as result_validator
import whole_portfolio_robustness_runner as runner


def _config() -> dict:
    return {
        "simulation": {
            "quarterly_months": [1, 4, 7, 10], "annual_months": [1],
            "fixed_point_tolerance_dollars": "0.000001",
            "fixed_point_max_iterations": 100,
        },
        "tax": {
            "gold_instrument": "GLD", "long_term_holding_days_minimum": 366,
        },
        "metrics": {"annualization_sessions": 252, "cagr_day_basis": "365.2425"},
    }


def _prereg() -> dict:
    return {
        "portfolio_mechanics": {"starting_value": "100000.00"},
        "frictions": {"tax_profiles": [
            {"id": "TAX_DEFERRED", "qualified_dividend_fraction": "0",
             "qualified_dividend_rate": "0", "ordinary_income_rate": "0",
             "short_gain_rate": "0", "long_gain_rate": "0", "gold_gain_rate": "0"},
            {"id": "TAXABLE", "qualified_dividend_fraction": "0.5",
             "qualified_dividend_rate": "0.10", "ordinary_income_rate": "0.30",
             "short_gain_rate": "0.30", "long_gain_rate": "0.20", "gold_gain_rate": "0.28"},
        ]},
    }


def _market(prices: dict[str, dict[str, float]], dividends: dict[str, dict[str, float]] | None = None) -> runner.MarketData:
    sessions = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
    factors = {(sessions[0], sessions[0]): 1.0}
    factors.update({(sessions[index - 1], sessions[index]): 1.0 for index in range(1, len(sessions))})
    return runner.MarketData(
        sessions=sessions, prices=prices,
        dividends=dividends or {ticker: {} for ticker in prices},
        cash_factor=factors, risk_free_factor=factors,
        first_available={ticker: min(values) for ticker, values in prices.items()},
        lookthrough={},
        caps={"issuer": 1.0, "ai": 1.0,
              "direct_tickers": frozenset(prices), "ai_tickers": frozenset(),
              "clusters": {"semis": {"cap": 1.0, "tickers": frozenset()},
                           "power_infra": {"cap": 1.0, "tickers": frozenset()}}},
    )


def test_frozen_decision_cell_and_advisory_boundaries():
    config = runner.load_config()
    assert config["decision_cell"] | {} == config["decision_cell"]
    assert config["decision_cell"]["cadence"] == "QUARTERLY"
    assert config["decision_cell"]["one_way_cost_bps"] == "10"
    assert config["decision_cell"]["tax_profile"] == "TAXABLE_MID"
    assert config["output"]["advisory_only"] is True
    assert config["output"]["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"


def test_hifo_tax_estimate_and_consumption_give_no_loss_credit():
    lots = [
        runner.Lot(2.0, 12.0, "2020-01-01", 0),
        runner.Lot(3.0, 15.0, "2024-01-01", 1),
        runner.Lot(1.0, 25.0, "2024-01-02", 2),
    ]
    tax = _prereg()["frictions"]["tax_profiles"][1]
    due, taxable_gain = runner._estimate_sale_tax(
        lots, 5.0, 20.0, "2024-06-01", "A", tax, _config()
    )
    # Highest basis is consumed first. The loss lot produces no credit, then
    # the $15 lot and one $12 lot produce $23 of taxable gains.
    assert taxable_gain == pytest.approx(23.0)
    assert due == pytest.approx(3 * 5 * 0.30 + 1 * 8 * 0.20)
    runner._consume_hifo(lots, 5.0)
    assert [(lot.quantity, lot.basis) for lot in lots] == [(1.0, 12.0)]


def test_simulation_credits_dividend_once_and_reconciles_nav():
    prices = {"A": {day: value for day, value in zip(
        ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        [10.0, 11.0, 12.0, 9.0],
    )}}
    market = _market(prices, {"A": {"2024-01-03": 1.0}})
    result = runner.simulate(
        "BASELINE", "SYNTHETIC", "2024-01-02", "2024-01-05",
        "QUARTERLY", "0", "TAX_DEFERRED", {"A": "50", "CASH": "50"},
        _prereg(), _config(), market,
    )
    assert result.values == pytest.approx([100000.0, 110000.0, 115000.0, 100000.0])
    assert result.rebalance_count == 1
    assert result.dividend_tax_paid == 0
    assert result.final_cash == pytest.approx(55000.0)


def test_pre_inception_weight_stays_cash_until_next_scheduled_rebalance():
    prices = {"A": {"2024-01-03": 11.0, "2024-01-04": 12.0, "2024-01-05": 9.0}}
    result = runner.simulate(
        "BASELINE", "SYNTHETIC", "2024-01-02", "2024-01-05",
        "QUARTERLY", "0", "TAX_DEFERRED", {"A": "50", "CASH": "50"},
        _prereg(), _config(), _market(prices),
    )
    assert result.values == pytest.approx([100000.0] * 4)
    assert result.one_way_notional == 0


def test_dff_uses_federal_business_day_lag_then_following_day(monkeypatch):
    monkeypatch.setattr(
        runner.risk_core, "federal_business_days",
        lambda _start, _end: ["2024-01-05", "2024-01-08", "2024-01-09", "2024-01-10"],
    )
    document = {"rows": [
        {"date": "2024-01-05", "rate_pct": "5"},
        {"date": "2024-01-08", "rate_pct": "6"},
        {"date": "2024-01-09", "rate_pct": "7"},
    ]}
    cash, risk_free = runner._lawful_rate_factors(
        ["2024-01-08", "2024-01-09"], document, 25.0
    )
    # Friday's observation becomes lawful after Monday's close and can first
    # inform Tuesday's accrual; Monday's observation remains unavailable.
    assert risk_free[("2024-01-08", "2024-01-09")] == pytest.approx(1 + 0.05 / 360)
    assert cash[("2024-01-08", "2024-01-09")] == pytest.approx(1 + 0.0475 / 360)


def test_validation_receipt_refuses_code_or_input_drift(tmp_path: Path, monkeypatch):
    original = {"gate": "READY", "code_commit": "a" * 40,
                "holdout_results_emitted": False}
    receipt = {
        "schema_version": "1.0", "study_id": "PORTFOLIO-ROBUSTNESS-0001",
        "phase": "NON_HOLDOUT_VALIDATION", "status": "PASS",
        "holdout_results_emitted": False,
        "input_freeze": original,
        "input_freeze_sha256": runner._canonical_hash(original),
        "validation_cutoff": "2023-12-29",
    }
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    monkeypatch.setattr(runner, "input_freeze", lambda: original | {"code_commit": "b" * 40})
    with pytest.raises(runner.ExecutionError, match="changed after non-holdout validation"):
        runner.verify_validation_receipt(path)


def test_workflow_limits_manual_execution_and_refuses_retained_result_rerun():
    workflow = Path(".github/workflows/run-whole-portfolio-robustness.yml").read_text(
        encoding="utf-8"
    )
    assert "if: github.ref == 'refs/heads/main'" in workflow
    assert "Refuse execution after governed results are retained" in workflow
    assert "research/whole_portfolio_robustness/execution/output_manifest.json" in workflow


def test_stationary_bootstrap_is_paired_and_deterministic():
    base = runner.SimulationResult(
        "BASELINE", "W", "QUARTERLY", "10", "TAXABLE_MID",
        ["1", "2", "3", "4"], [1, 1, 1, 1], [.01, -.02, .03, -.01],
        [.0001] * 4, [], 0, 0, 0, 0, 0, 0, 0, 0,
    )
    variant = runner.SimulationResult(
        "V", "W", "QUARTERLY", "10", "TAXABLE_MID",
        ["1", "2", "3", "4"], [1, 1, 1, 1], [.02, -.01, .04, 0],
        [.0001] * 4, [], 0, 0, 0, 0, 0, 0, 0, 0,
    )
    import random
    first = runner._bootstrap_once(base, variant, random.Random(7), 1 / 21)
    second = runner._bootstrap_once(base, variant, random.Random(7), 1 / 21)
    assert first == second
    assert all(math.isfinite(value) for value in first)


def test_sensitivity_matrix_covers_every_registered_window(monkeypatch):
    prereg = {"study_id": "PORTFOLIO-ROBUSTNESS-0001", "frictions": {
        "one_way_cost_bps": ["10"],
        "tax_profiles": [{"id": "TAXABLE_MID"}],
    }}
    config = {"decision_cell": {
        "cadence": "QUARTERLY", "one_way_cost_bps": "10",
        "tax_profile": "TAXABLE_MID",
    }}
    monkeypatch.setattr(
        runner.gate, "derive_instrument_weights",
        lambda *_args: {"BASELINE": {}, "V": {}},
    )
    rows = []
    for window in ("W1", "W2"):
        for cadence in ("QUARTERLY", "ANNUAL"):
            for variant, shift in (("BASELINE", 0.0), ("V", 0.1)):
                rows.append({
                    "variant": variant, "window": window, "cadence": cadence,
                    "one_way_cost_bps": "10", "tax_profile": "TAXABLE_MID",
                    "NET_TWR_CAGR": shift, "SHARPE_VS_LAGGED_DFF": shift,
                    "SORTINO_VS_LAGGED_DFF": shift, "MAX_DRAWDOWN": shift,
                    "DAILY_CVAR_95": shift,
                })
    result = runner.build_sensitivity(rows, prereg, config)
    assert len(result["rows"]) == 4
    assert {row["window"] for row in result["rows"]} == {"W1", "W2"}
    assert result["facts_inference_separation"] == "FACTS_ONLY"


def test_result_validator_fails_closed_on_incomplete_directory(tmp_path: Path):
    with pytest.raises(result_validator.ResultValidationError, match="exactly"):
        result_validator.validate(tmp_path)


def test_json_boundary_rejects_nonfinite_tokens(tmp_path: Path):
    path = tmp_path / "bad.json"
    path.write_text('{"value": NaN}', encoding="utf-8")
    with pytest.raises(runner.ExecutionError, match="nonfinite JSON token"):
        runner._read_json(path)
    with pytest.raises(result_validator.ResultValidationError, match="nonfinite JSON token"):
        result_validator._json(path)
    with pytest.raises(ValueError, match="Out of range float"):
        runner._canonical_bytes({"value": math.nan})


def test_runner_has_no_brokerage_holdings_margin_or_stage1_dependency():
    source = Path(runner.__file__).read_text(encoding="utf-8")
    for prohibited in (
        "import alpaca_client", "import allocate", "import holdings",
        "import margin_state", "import level1_stage1",
    ):
        assert prohibited not in source
