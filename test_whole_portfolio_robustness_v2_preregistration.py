from __future__ import annotations

import copy
from pathlib import Path

import yaml

import whole_portfolio_robustness_v2_preregistration_validator as validator


def test_preregistration_passes() -> None:
    assert validator.validate() == []


def test_tampered_variant_fails_closed(tmp_path: Path) -> None:
    data = yaml.safe_load(validator.PREREG.read_text(encoding="utf-8"))
    data = copy.deepcopy(data)
    data["variants"]["definitions"][1]["expected_sleeves_pct"]["broad_market_funds"] = "29.00"
    path = tmp_path / "pre_registration.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors = validator.validate(prereg_path=path)
    assert any("does not sum to 100%" in error for error in errors)


def test_safety_and_holdout_labels_fail_closed(tmp_path: Path) -> None:
    data = yaml.safe_load(validator.PREREG.read_text(encoding="utf-8"))
    data["safety"]["places_orders_or_trades"] = True
    data["windows"]["correction_replication"]["exposure"] = "FRESH"
    path = tmp_path / "pre_registration.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors = validator.validate(prereg_path=path)
    assert any("unsafe capability" in error for error in errors)
    assert any("correction interval exposure" in error for error in errors)


def test_calendar_and_foreign_tax_controls_fail_closed(tmp_path: Path) -> None:
    data = yaml.safe_load(validator.PREREG.read_text(encoding="utf-8"))
    data["portfolio_mechanics"]["crypto_calendar_alignment"] = "XNYS_ROWS_ONLY"
    data["frictions"]["foreign_dividends"]["mandatory_sensitivities"] = []
    path = tmp_path / "pre_registration.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors = validator.validate(prereg_path=path)
    assert any("crypto weekend/calendar alignment" in error for error in errors)
    assert any("foreign-dividend sensitivities" in error for error in errors)


def test_v2_contains_no_result_outputs() -> None:
    root = validator.PREREG.parent
    prohibited = {"input_freeze.json", "portfolio_paths.json", "metrics.json", "bootstrap.json", "sensitivity_matrix.json", "results.md", "disposition.yaml"}
    assert prohibited.isdisjoint({p.name for p in root.iterdir()})


def test_predecessor_outputs_are_untouched() -> None:
    assert (validator.ROOT / "research/whole_portfolio_robustness/execution/results.md").is_file()
    assert (validator.ROOT / "governance/decisions/RISK-0005-whole-portfolio-evidence-disposition.md").is_file()
