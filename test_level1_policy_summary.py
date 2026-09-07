from copy import deepcopy
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from level1_policy_summary import PolicySummaryError, build_policy_summary, load_policy_summary


ROOT = Path(__file__).parent


def _targets():
    return yaml.safe_load((ROOT / "targets.yaml").read_text(encoding="utf-8"))


def test_live_policy_reconciles_to_the_whole_book():
    result = load_policy_summary(ROOT / "targets.yaml")
    assert result["reconciliation"] == {
        "assigned_pct": "99.25",
        "unallocated_pct": "0.75",
        "total_pct": "100.00",
    }


def test_live_policy_exposes_requested_level1_sleeves_exactly():
    sleeves = load_policy_summary(ROOT / "targets.yaml")["sleeves_pct"]
    assert sleeves["direct_equity"] == "63.25"
    assert sleeves["broad_market_funds"] == "23.00"
    assert sleeves["broad_market_and_equities"] == "86.25"
    assert sleeves["gold_defensive"] == "4.00"
    assert sleeves["crypto"] == "4.00"
    assert sleeves["cash_and_reserve"] == "5.00"


def test_fund_mapping_is_explicit_not_asset_class_guessing():
    members = load_policy_summary(ROOT / "targets.yaml")["members"]
    assert members["broad_market_funds"] == ["SPY", "VEA", "VWO"]
    assert members["gold_defensive"] == ["GLD"]


def test_unknown_fund_fails_closed():
    data = _targets()
    data["destination"].append(
        {"ticker": "MYSTERY", "target_pct": Decimal("0"), "asset_class": "fund"}
    )
    with pytest.raises(PolicySummaryError, match="no deterministic Level-1 mapping"):
        build_policy_summary(data)


def test_duplicate_ticker_fails_closed():
    data = _targets()
    data["destination"].append(deepcopy(data["destination"][0]))
    with pytest.raises(PolicySummaryError, match="duplicate destination ticker"):
        build_policy_summary(data)


@pytest.mark.parametrize("value", [-1, "NaN", "Infinity", "not-a-number"])
def test_invalid_weight_fails_closed(value):
    data = _targets()
    data["destination"][0]["target_pct"] = value
    with pytest.raises(PolicySummaryError):
        build_policy_summary(data)


def test_overallocated_policy_fails_closed():
    data = _targets()
    data["destination"][0]["target_pct"] = 106
    with pytest.raises(PolicySummaryError, match="exceed 100%"):
        build_policy_summary(data)


def test_summary_is_recommendation_only_and_stage1_inert():
    safety = load_policy_summary(ROOT / "targets.yaml")["safety"]
    assert safety == {
        "changes_policy": False,
        "uses_live_data": False,
        "uses_holdings": False,
        "places_orders": False,
        "arms_or_executes_stage1": False,
    }


def test_module_has_no_allocator_brokerage_or_stage1_imports():
    source = (ROOT / "level1_policy_summary.py").read_text(encoding="utf-8")
    for prohibited in (
        "import allocate",
        "import alpaca_client",
        "import margin_state",
        "import level1_stage1",
    ):
        assert prohibited not in source
