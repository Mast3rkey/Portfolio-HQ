from pathlib import Path
from decimal import Decimal

import pytest
import yaml

from margin_current_s3_preregistration_validator import REGISTER, _finite, main, validate
from margin_simulation import RepaymentDecision, ScenarioConfig, _leverage_capped_margin, simulate
from repayment_lib import r1_deposits_first


def _mutated(tmp_path: Path, mutate) -> Path:
    data = yaml.safe_load(REGISTER.read_text())
    mutate(data)
    path = tmp_path / "scope.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


def test_scoping_register_is_incomplete_and_consistent():
    assert validate() == []


def test_current_inventory_numeric_owners_and_roster_counts_match_live_yaml():
    targets = yaml.safe_load(Path("targets.yaml").read_text())
    rows = targets["destination"]
    assert len(rows) == 36
    assert sum(row["target_pct"] for row in rows) == pytest.approx(99.25)
    assert targets["caps"]["clusters"] == [
        {"name": "semis", "pct": 25.0, "tickers": ["ASML", "TSM", "NVDA", "AVGO", "KLAC"]},
        {"name": "power_infra", "pct": 20.0, "tickers": ["ETN", "GEV", "PWR"]},
        {"name": "oil", "pct": 20.0, "tickers": []},
    ]
    assert targets["margin"] == {"leverage_cap": 1.8, "buffer_floor_pct": 30.0}
    assert targets["levels"] == {"rung_atr_multipliers": [1.0, 2.0, 3.0], "practicality_cap_pct": 25, "swing_low_sessions": 60}
    assert targets["gates"] == {"min_lot_dollars": 25, "trend_rsi_override": 30, "earnings_blackout_days": 7}


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


@pytest.mark.parametrize("mutation, expected", [
    (lambda d: d.update(required_unresolved_decisions=[{}]), "missing, duplicate, or changed unresolved-decision register"),
    (lambda d: d.update(candidate_registry=None), "candidate registry must remain undefined"),
    (lambda d: d.update(trial_budget=[]), "trial budget must remain undefined"),
    (lambda d: d["exposure_and_coverage_ledger"].update(original_margin_track_2=None), "original Track 2 exposure record must be a mapping"),
    (lambda d: d["exposure_and_coverage_ledger"].update(successor_fresh_period=None), "successor fresh-period record must be a mapping"),
])
def test_nested_malformed_values_return_clear_errors(tmp_path, mutation, expected):
    assert expected in validate(_mutated(tmp_path, mutation))


def test_huge_integer_returns_error_instead_of_crashing(tmp_path):
    path = tmp_path / "huge.yaml"
    path.write_text(REGISTER.read_text() + f"\nunexpected_huge_integer: {1 << 4096}\n")
    assert validate(path) == ["register must be a finite mapping with string keys"]


def test_recursive_yaml_alias_returns_controlled_failure_without_traceback(tmp_path, capsys):
    path = tmp_path / "recursive.yaml"
    path.write_text(REGISTER.read_text() + "\nrecursive: &recursive [*recursive]\n")
    expected = ["register must be a finite mapping with string keys"]
    assert validate(path) == expected
    assert main(path) == 1
    captured = capsys.readouterr()
    assert captured.out == "ERROR: register must be a finite mapping with string keys\n"
    assert captured.err == ""


def test_ordinary_reused_aliases_remain_valid(tmp_path):
    path = tmp_path / "shared.yaml"
    path.write_text(REGISTER.read_text() + "\nshared: &shared [alpha, {beta: 1}]\nleft: *shared\nright: *shared\n")
    assert validate(path) == []


def test_deep_and_exponentially_shared_acyclic_structures_are_bounded():
    deep: object = "leaf"
    for _ in range(5000):
        deep = [deep]
    assert _finite(deep)

    shared: object = "leaf"
    for _ in range(5000):
        shared = [shared, shared]
    assert _finite(shared)


def test_margin_cost_source_and_whole_portfolio_costs_are_not_conflated():
    scope = yaml.safe_load(REGISTER.read_text())
    inherited = scope["preserved_design_requirements_from_margin_0005"]
    assert inherited["costs_bps_one_way"] == ["0", "5", "15"]
    assert inherited["excluded_cost_registry"] == "PORTFOLIO_ROBUSTNESS_V2_0_10_25_BPS_NOT_IMPORTED"
    oracle = scope["proposed_accounting_contract"]["synthetic_oracle_10bps_fixture_only"]
    assert oracle["classification"] == "SYNTHETIC_ARITHMETIC_NOT_MARGIN_0005_COST_CELL_OR_ACCOUNT_FACT"


def test_cost_aware_synthetic_oracle_and_book_conservation():
    G, D, A, L = map(Decimal, ("180", "80", "100", "1.25"))
    s = b = Decimal("0.001")
    N = G - D
    repayment = min(A, D, max(Decimal(0), G / L - N))
    assert repayment == Decimal("44")
    D_i, A_i, N_i = D - repayment, A - repayment, N + repayment
    capacity = _leverage_capped_margin(float(G), float(D_i), float(A_i), float(L), float("inf"))
    assert capacity == pytest.approx(14.0)

    p_cash = A_i / (1 + b)
    assert p_cash.quantize(Decimal("0.0000000001")) == Decimal("55.9440559441")
    assert G + p_cash + Decimal(0) - D_i == N_i + A_i - b * p_cash

    p_target = (L * (N_i + A_i) - G) / (1 + L * b)
    draw = (1 + b) * p_target - A_i
    assert p_target.quantize(Decimal("0.0000000001")) == Decimal("69.9126092385")
    assert draw.quantize(Decimal("0.0000000001")) == Decimal("13.9825218477")
    assert (G + p_target) / ((G + p_target) - (D_i + draw)) == L

    q = (G - L * N) / (1 - L * s)
    assert q.quantize(Decimal("0.0000000001")) == Decimal("55.0688360451")
    lhs = (G - q) - (D - (1 - s) * q)
    rhs = N - s * q
    assert abs(lhs - rhs) < Decimal("1e-24")


def test_three_deployment_semantics_and_source_ledger_remain_distinct():
    scope = yaml.safe_load(REGISTER.read_text())
    contract = scope["proposed_accounting_contract"]
    assert set(contract["deployment_semantics"]) == {
        "CASH_ONLY_NO_NEW_DRAW_PROPOSAL",
        "INHERITED_DEPOSIT_DAY_CAPACITY_AND_WEIGHTED_GAPS",
        "GENUINE_END_CYCLE_TARGET_PROPOSAL",
    }
    inherited = contract["deployment_semantics"]["INHERITED_DEPOSIT_DAY_CAPACITY_AND_WEIGHTED_GAPS"]
    assert inherited["meaning"].startswith("CAPACITY_ONLY")
    assert "same_cycle_reborrow" in contract["repayment_source_ledger"]["fields"]
    assert scope["candidate_mapping_proposal"]["status"] == "PARTIAL_SOURCE_DERIVED_NOT_ACCEPTED_REGISTRY"


def test_reviewer_source_dispositions_do_not_claim_acquisition_or_admission():
    text = Path("research/current_architecture_readiness/EVIDENCE_AND_INPUT_REMEDIATION.md").read_text()
    assert "illustrative first-day VWAP values 414.44/21.08" in text
    assert "not proof of coverage or admission" in text
    assert "no archive path, returned bytes, byte count, hash, or receipt" in text


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
