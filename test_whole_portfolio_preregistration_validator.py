from copy import deepcopy
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from whole_portfolio_preregistration_validator import (
    PreregistrationError,
    derive_baseline,
    market_data_path_hash,
    validate_documents,
    validate_files,
)


ROOT = Path(__file__).parent


def _yaml(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def _documents():
    return (
        _yaml("research/whole_portfolio_robustness/pre_registration.yaml"),
        _yaml("targets.yaml"),
        _yaml("gates.yaml"),
    )


def test_live_preregistration_and_all_frozen_inputs_validate():
    result = validate_files()
    assert result["status"] == "VALID"
    assert result["baseline"] == {
        "eligible_direct_equity": "56.50",
        "broad_market_funds": "23.00",
        "gold": "4.00",
        "crypto": "4.00",
        "cash_and_protected_capital": "12.50",
    }


def test_baseline_is_derived_from_policy_and_protected_capital():
    _, targets, gates = _documents()
    baseline = derive_baseline(targets, gates)
    assert baseline["target_assigned_pct"] == Decimal("99.25")
    assert baseline["unallocated_cash_pct"] == Decimal("0.75")
    assert baseline["gated_target_cash_pct"] == Decimal("6.75")
    assert sum(baseline[key] for key in baseline if key.endswith("equity") or key in {"broad_market_funds", "gold", "crypto", "cash_and_protected_capital"}) == Decimal("100")


def test_market_data_inventory_is_complete_and_pinned():
    count, digest = market_data_path_hash()
    assert count == 37
    assert digest == "12cf4ab51fc0dc0787378c0915603a73e77479349658a2c4a926d855d46ce825"


def test_every_variant_reconciles_and_is_fixed_before_results():
    prereg, targets, gates = _documents()
    validate_documents(prereg, targets, gates)
    assert prereg["variants"]["optimization"] == "PROHIBITED"
    assert prereg["variants"]["grid_search"] == "PROHIBITED"
    for variant in prereg["variants"]["definitions"]:
        assert sum(float(value) for value in variant["expected_sleeves_pct"].values()) == 100.0


def test_target_drift_fails_instead_of_renormalizing():
    prereg, targets, gates = _documents()
    targets = deepcopy(targets)
    targets["destination"][0]["target_pct"] = 5.99
    with pytest.raises(PreregistrationError, match="baseline does not match"):
        validate_documents(prereg, targets, gates)


def test_gate_clearance_fails_instead_of_inventing_activation_history():
    prereg, targets, gates = _documents()
    gates = deepcopy(gates)
    gates["gates"][0]["allow_add"] = True
    with pytest.raises(PreregistrationError, match="accepted closed cash gate"):
        validate_documents(prereg, targets, gates)


def test_gate_membership_drift_fails_closed():
    prereg, targets, gates = _documents()
    gates = deepcopy(gates)
    gates["gates"] = gates["gates"][:-1]
    with pytest.raises(PreregistrationError, match="gated ticker"):
        validate_documents(prereg, targets, gates)


def test_variant_transform_cannot_be_changed_after_registration():
    prereg, targets, gates = _documents()
    prereg = deepcopy(prereg)
    prereg["variants"]["definitions"][1]["transforms"][0]["percentage_points"] = "4.99"
    with pytest.raises(PreregistrationError, match="registered study design drifted"):
        validate_documents(prereg, targets, gates)


def test_protected_cash_components_must_reconcile():
    prereg, targets, gates = _documents()
    prereg = deepcopy(prereg)
    prereg["baseline"]["cash_and_protected_capital_components"]["gated_target_cash"] = "6.50"
    with pytest.raises(PreregistrationError, match="registered study design drifted"):
        validate_documents(prereg, targets, gates)


@pytest.mark.parametrize(
    ("section", "field", "replacement"),
    [
        ("windows", "confirmation", {"start": "2021-01-05", "end": "2023-12-29", "voting": True}),
        ("frictions", "one_way_cost_bps", ["0", "5", "10"]),
        ("metrics", "tail", ["MAX_DRAWDOWN"]),
        ("review_thresholds", "close_call_rule", "RECOMMEND_POLICY_REVIEW"),
    ],
)
def test_any_consequential_design_drift_fails_closed(section, field, replacement):
    prereg, targets, gates = _documents()
    prereg = deepcopy(prereg)
    prereg[section][field] = replacement
    with pytest.raises(PreregistrationError, match="registered study design drifted"):
        validate_documents(prereg, targets, gates)


@pytest.mark.parametrize("field", ["automatic_adoption", "grid_search", "optimization"])
def test_result_driven_adoption_or_search_cannot_be_enabled(field):
    prereg, targets, gates = _documents()
    prereg = deepcopy(prereg)
    if field == "automatic_adoption":
        prereg["purpose"][field] = "PERMITTED"
    else:
        prereg["variants"][field] = "PERMITTED"
    with pytest.raises(PreregistrationError):
        validate_documents(prereg, targets, gates)


def test_close_calls_retain_baseline_and_target_change_needs_review():
    prereg, _, _ = _documents()
    thresholds = prereg["review_thresholds"]
    assert thresholds["default"] == "RETAIN_BASELINE"
    assert thresholds["close_call_rule"] == "RETAIN_BASELINE"
    assert thresholds["target_change_rule"] == "SEPARATE_EXPLICIT_REVIEWED_DECISION_REQUIRED"


def test_stage1_margin_holdings_and_brokerage_boundaries_are_inert():
    prereg, targets, gates = _documents()
    validate_documents(prereg, targets, gates)
    assert prereg["safety"] == {
        "advisory_only": True,
        "uses_holdings": False,
        "uses_brokerage_or_credentials": False,
        "places_orders_or_trades": False,
        "changes_targets_or_gates": False,
        "changes_margin_policy": False,
        "arms_or_executes_stage1": False,
        "stage1_state": "UNARMED_AND_NOT_EXECUTABLE",
    }
    source = (ROOT / "whole_portfolio_preregistration_validator.py").read_text(encoding="utf-8")
    for prohibited in ("import allocate", "import alpaca_client", "import holdings", "import margin_state", "import level1_stage1"):
        assert prohibited not in source
