from pathlib import Path

import pytest
import yaml

from margin_current_s3_preregistration_validator import REGISTER, validate
from margin_simulation import RepaymentDecision, ScenarioConfig, simulate
from repayment_lib import r1_deposits_first


def _mutated(tmp_path: Path, mutate) -> Path:
    data = yaml.safe_load(REGISTER.read_text())
    mutate(data)
    path = tmp_path / "scope.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


def test_scoping_register_is_incomplete_and_consistent():
    assert validate() == []


@pytest.mark.parametrize("mutation", [
    lambda d: d.update(study_id="SWAPPED"),
    lambda d: d.update(status="PREREGISTERED_NOT_EXECUTED"),
    lambda d: d["required_unresolved_decisions"].pop(),
    lambda d: d["execution"].update(historical_execution_authorized=True),
    lambda d: d["exposure_and_coverage_ledger"]["successor_fresh_period"].update(status="FRESH"),
    lambda d: d["candidate_registry"].update(status="FROZEN"),
    lambda d: d["trial_budget"].update(status="DEFINED"),
])
def test_authority_and_scope_mutations_fail_closed(tmp_path, mutation):
    assert validate(_mutated(tmp_path, mutation))


def test_duplicate_key_and_nonfinite_and_wrong_type_fail_closed(tmp_path):
    duplicate = tmp_path / "duplicate.yaml"
    duplicate.write_text(REGISTER.read_text() + "\nstudy_id: AGAIN\n")
    assert "duplicate key" in validate(duplicate)[0]
    nonfinite = tmp_path / "nonfinite.yaml"
    nonfinite.write_text(REGISTER.read_text() + "\nnonfinite: .nan\n")
    assert validate(nonfinite) == ["register must be a finite mapping with string keys"]
    assert validate(_mutated(tmp_path, lambda d: d.update(required_unresolved_decisions="wrong")))


def test_r1_pretrade_reproduction_requires_future_event_order_regression():
    dates = ["2000-01-03", "2000-01-04"]
    calls = 0

    def hook(state, prior_gross):
        nonlocal calls
        calls += 1
        if calls == 1:
            return RepaymentDecision(leverage_target=1.8)
        return r1_deposits_first(state, prior_gross, is_deposit_day=True, target_leverage=1.25)

    result = simulate(
        ScenarioConfig("synthetic", 1.8, 0.0, 0.0, pre_trade_fn=hook),
        {"X": 1.0}, {"X": ([100.0, 100.0], 0)}, dates, dates,
        deposit_amount=100.0, min_lot=1.0,
    )
    repayments = [e for e in result.events if e["kind"] == "repayment"]
    day1 = [e for e in result.events if e["day"] == 1]
    assert result.gross_series == pytest.approx([180.0, 200.0])
    assert result.debt_series == pytest.approx([80.0, 25.0])
    assert result.cash_series == pytest.approx([0.0, 25.0])
    assert repayments == [{"day": 1, "kind": "repayment", "amount": pytest.approx(55.0), "source": "pre_trade"}]
    assert [e["kind"] for e in day1].index("repayment") < [e["kind"] for e in day1].index("deposit")
    assert result.tax_lot_events[0]["shares_sold"] == pytest.approx(0.55)
    assert result.tax_lot_events[0]["sale_day"] == 1
