from __future__ import annotations

import copy
import math
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import yaml

import whole_portfolio_robustness_v2_preregistration_validator as validator


def _data() -> dict:
    return copy.deepcopy(yaml.safe_load(validator.PREREG.read_text(encoding="utf-8")))


def _validate_copy(tmp_path: Path, data: dict) -> list[str]:
    path = tmp_path / "pre_registration.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return validator.validate(prereg_path=path)


def test_preregistration_passes() -> None:
    assert validator.validate() == []


def test_coherent_variant_drift_cannot_rebless_itself(tmp_path: Path) -> None:
    data = _data()
    variant = data["variants"]["definitions"][1]
    variant["transforms"][0]["percentage_points"] = "50.00"
    variant["expected_sleeves_pct"]["eligible_direct_equity"] = "6.50"
    variant["expected_sleeves_pct"]["broad_market_funds"] = "73.00"
    data["integrity"]["frozen_contract"]["expected_sha256"] = validator._contract_digest(data)
    errors = _validate_copy(tmp_path, data)
    assert "contract digest declaration changed" in errors
    assert "frozen contract drift" in errors


def test_consequential_threshold_tax_and_pin_drift_all_fail(tmp_path: Path) -> None:
    data = _data()
    data["review_thresholds"]["support_gate"]["cell_predicate_all_required"]["sharpe_delta_gte"] = "-999"
    data["frictions"]["tax_profile_parameters"]["TAXABLE_HIGH"]["ordinary_income_rate"] = "0"
    del data["frozen_inputs"]["files"]["targets.yaml"]
    errors = _validate_copy(tmp_path, data)
    assert "frozen contract drift" in errors
    assert any("pinned-file registry" in error for error in errors)
    assert any("cell predicate" in error for error in errors)


def test_duplicate_and_malformed_cell_entries_fail_closed(tmp_path: Path) -> None:
    data = _data()
    data["frictions"]["cell_registry"][1] = copy.deepcopy(data["frictions"]["cell_registry"][0])
    errors = _validate_copy(tmp_path, data)
    assert any("exact unique 18-cell" in error for error in errors)


def test_nonfinite_yaml_value_fails_before_semantics(tmp_path: Path) -> None:
    data = _data()
    data["bootstrap"]["resamples"] = math.inf
    errors = _validate_copy(tmp_path, data)
    assert errors == ["cannot load preregistration: nonfinite value at root.bootstrap.resamples"]


def test_primary_cell_and_exact_support_boundary_are_economic() -> None:
    data = _data()
    assert data["frictions"]["primary_cell"] == {
        "one_way_cost_bps": "10", "tax_profile": "TAXABLE_MID", "rebalance_cadence": "QUARTERLY"
    }
    cells = data["frictions"]["cell_registry"]
    assert len(cells) == 18
    assert sum(cell == {"cell_id": "COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY", **data["frictions"]["primary_cell"]} for cell in cells) == 1
    minimum = data["review_thresholds"]["support_gate"]["minimum_passing_cells"]
    assert minimum == math.ceil(Decimal("0.80") * len(cells)) == 15
    assert 14 < minimum <= 15


def test_dividend_receivable_boundary_and_cash_tax_math() -> None:
    data = _data()
    example = data["portfolio_mechanics"]["dividend_boundary_example"]
    ex_nav = Decimal(example["prior_close_shares"]) * Decimal(example["ex_date_price"]) + Decimal(example["gross_dividend"])
    assert ex_nav == Decimal(example["ex_date_nav"]) == Decimal("100")
    assert Decimal(example["ex_date_spendable_cash"]) == 0
    mid = data["frictions"]["tax_profile_parameters"]["TAXABLE_MID"]
    after_tax_daily_interest = Decimal("100") * ((Decimal("5.00") - Decimal("0.25")) / 100) * (1 - Decimal(mid["ordinary_income_rate"])) / 360
    assert after_tax_daily_interest == Decimal("0.01002777777777777777777777778")
    assert "EARNS_NO_CASH_INTEREST" in data["portfolio_mechanics"]["dividend_receivable_constraints"]


def test_foreign_veto_inventory_has_separate_and_joint_cases() -> None:
    inventory = _data()["frictions"]["foreign_dividends"]["sensitivity_inventory"]
    assert inventory == [
        "STANDARD_AVAILABLE_CREDIT", "ZERO_FOREIGN_TAX_CREDIT", "ETN_25_PERCENT_IRISH_WITHHOLDING",
        "JOINT_ZERO_CREDIT_AND_ETN_25_PERCENT_IRISH_WITHHOLDING",
    ]


def test_optimized_python_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-O", str(validator.ROOT / "whole_portfolio_robustness_v2_preregistration_validator.py")],
        cwd=validator.ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("PASS:")


def test_v2_contains_no_result_outputs() -> None:
    prohibited = {"input_freeze.json", "portfolio_paths.json", "metrics.json", "bootstrap.json", "sensitivity_matrix.json", "results.md", "disposition.yaml"}
    assert prohibited.isdisjoint({p.name for p in validator.PREREG.parent.iterdir()})


def test_predecessor_outputs_are_untouched() -> None:
    assert (validator.ROOT / "research/whole_portfolio_robustness/execution/results.md").is_file()
    assert (validator.ROOT / "governance/decisions/RISK-0005-whole-portfolio-evidence-disposition.md").is_file()
