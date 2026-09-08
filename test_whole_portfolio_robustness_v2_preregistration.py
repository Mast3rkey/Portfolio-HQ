from __future__ import annotations

import copy
import json
import math
import subprocess
import sys
import shutil
from decimal import Decimal, localcontext
from pathlib import Path

import yaml
import pytest

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
    def daily_change(dff_percent: str) -> Decimal:
        gross_rate = Decimal(dff_percent) / 100
        return Decimal(100) * (
            gross_rate - max(gross_rate, Decimal(0)) * Decimal(mid["ordinary_income_rate"])
            - Decimal("0.0025")
        ) / 360

    assert daily_change("5") == Decimal("0.009861111111111111111111111111")
    assert daily_change("0") == Decimal("-0.0006944444444444444444444444444")
    assert daily_change("-1") == Decimal("-0.003472222222222222222222222222")
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


def _isolated_root(tmp_path: Path) -> Path:
    root = tmp_path / "isolated"
    for rel in validator.EXPECTED_PINS:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(validator.ROOT / rel, target)
    for source in (validator.PREREG, validator.PROTOCOL):
        target = root / source.relative_to(validator.ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return root


def test_normative_upstream_protocol_pin_rejects_byte_drift(tmp_path: Path) -> None:
    root = _isolated_root(tmp_path)
    assert validator.validate(root=root) == []
    (root / "research/buy_ladder_backtest/PROTOCOL_V2.md").write_text(
        "incompatible ex-date cash; no split normalization\n", encoding="utf-8"
    )
    assert "pin drift: research/buy_ladder_backtest/PROTOCOL_V2.md" in validator.validate(root=root)


def test_normative_upstream_pin_cannot_be_removed_and_self_reblessed(tmp_path: Path) -> None:
    data = _data()
    del data["frozen_inputs"]["files"]["research/buy_ladder_backtest/PROTOCOL_V2.md"]
    data["integrity"]["frozen_contract"]["expected_sha256"] = validator._contract_digest(data)
    errors = _validate_copy(tmp_path, data)
    assert "contract digest declaration changed" in errors
    assert any("pinned-file registry" in error for error in errors)


def test_duplicate_mapping_keys_rejected_even_when_last_restores_value(tmp_path: Path) -> None:
    pristine = validator.PREREG.read_text(encoding="utf-8")
    top = tmp_path / "top.yaml"
    top.write_text("schema_version: '999'\n" + pristine, encoding="utf-8")
    assert any("duplicate mapping key: 'schema_version'" in error for error in validator.validate(prereg_path=top))

    nested = tmp_path / "nested.yaml"
    nested.write_text(pristine.replace("  disposition: EVIDENCE_LIMITED_NOT_DECISION_GRADE\n", "  disposition: WRONG\n  disposition: EVIDENCE_LIMITED_NOT_DECISION_GRADE\n", 1), encoding="utf-8")
    assert any("duplicate mapping key: 'disposition'" in error for error in validator.validate(prereg_path=nested))


def test_duplicate_mapping_key_rejected_under_optimized_python(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.yaml"
    path.write_text("schema_version: '999'\n" + validator.PREREG.read_text(encoding="utf-8"), encoding="utf-8")
    code = "import sys,whole_portfolio_robustness_v2_preregistration_validator as v; e=v.validate(prereg_path=v.Path(sys.argv[1])); raise SystemExit(0 if any('duplicate mapping key' in x for x in e) else 1)"
    result = subprocess.run([sys.executable, "-O", "-c", code, str(path)], cwd=validator.ROOT, check=False)
    assert result.returncode == 0


def test_alias_and_merge_yaml_are_rejected(tmp_path: Path) -> None:
    alias = tmp_path / "alias.yaml"
    alias.write_text("base: &base {x: 1}\ncopy: *base\n", encoding="utf-8")
    assert any("aliases are prohibited" in error for error in validator.validate(prereg_path=alias))


def test_non_xnys_settlement_and_linked_decision_rules_are_frozen() -> None:
    data = _data()
    mechanics = data["portfolio_mechanics"]
    assert mechanics["dividend_settlement_calendar"] == "EVERY_CALENDAR_DATE_NOT_ONLY_XNYS_SESSIONS"
    examples = mechanics["non_xnys_boundary_examples"]
    assert [(x["payable_date"], x["first_eligible_accrual_day"], x["first_interest_credit_date"]) for x in examples] == [
        ("2023-01-16", "2023-01-17", "2023-01-18"),
        ("2025-01-09", "2025-01-10", "2025-01-11"),
    ]
    session_data = json.loads((validator.ROOT / "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json").read_text())
    sessions = {row["session"] for row in session_data["sessions"]}
    expected_membership = {
        "2023-01-16": False, "2023-01-17": True, "2023-01-18": True,
        "2025-01-09": False, "2025-01-10": True, "2025-01-11": False,
        "2025-01-12": False, "2025-01-13": True,
    }
    assert {date: date in sessions for date in expected_membership} == expected_membership

    with localcontext() as context:
        context.prec = 40
        daily_rate = (Decimal("0.05") - Decimal("0.05") * Decimal("0.24") - Decimal("0.0025")) / 360
        compounded = [Decimal("100") * (1 + daily_rate) ** days for days in range(4)]
    assert Decimal(examples[0]["xnys_trace"][1]["xnys_close_nav"]) == Decimal("100")
    assert Decimal(examples[0]["xnys_trace"][2]["xnys_close_nav"]) == compounded[1]
    assert Decimal(examples[1]["xnys_trace"][1]["xnys_close_nav"]) == Decimal("100")
    assert Decimal(examples[1]["xnys_trace"][2]["nav_after_events"]) == compounded[1]
    assert Decimal(examples[1]["xnys_trace"][3]["nav_after_events"]) == compounded[2]
    assert Decimal(examples[1]["xnys_trace"][4]["xnys_close_nav"]) == compounded[3]
    thresholds = data["review_thresholds"]
    assert [x["tail_metric"] for x in thresholds["linked_tail_gate"]["predeclared_paths"]] == ["MAX_DRAWDOWN", "DAILY_CVAR_95"]
    disposition = thresholds["multiple_passer_disposition"]
    assert disposition["empty_passing_set"] == "RETAIN_BASELINE"
    assert disposition["ranking_or_tiebreak"] == "PROHIBITED"


def test_foreign_decision_fields_use_full_passing_set_not_winner() -> None:
    foreign = _data()["frictions"]["foreign_dividends"]
    assert foreign["decision_rule"] == "FULL_CANONICALLY_ORDERED_PASSING_SET_OR_EVERY_PER_VARIANT_GATE_BOOLEAN_CHANGE_CAUSES_UNABLE_TO_DETERMINE"
    assert foreign["veto"] == "IF_ANY_SEPARATE_OR_JOINT_CASE_CHANGES_FULL_CANONICALLY_ORDERED_PASSING_SET_OR_ANY_PER_VARIANT_GATE_BOOLEAN_THEN_UNABLE_TO_DETERMINE"


def test_upstream_incorporation_is_narrow_and_local_v2_controls() -> None:
    scope = _data()["frozen_inputs"]["upstream_incorporation_scope"]
    assert scope["retained_normative_mechanics"] == [
        "ACCEPTED_INPUT_DISPOSITION_AND_PRICE_ANOMALY_CORRECTIONS", "SPLIT_NORMALIZATION",
        "PRIOR_CLOSE_SHARE_ENTITLEMENT", "EX_DATE_NET_RECEIVABLE_RECOGNITION",
        "SOURCE_WITHHOLDING_AND_SAME_DIVIDEND_FOREIGN_TAX_CREDIT_MECHANICS",
    ]
    assert "CASH_RATE_FORMULA" in scope["superseded_predecessor_economics"]
    assert "ACCRUAL_DAY_VERSUS_CREDIT_RECOGNITION_DATE_CLOCK" in scope["superseded_predecessor_economics"]
    assert scope["not_imported"] == [
        "LADDER_ARMS", "FILLS", "BUDGETS_OR_CONTRIBUTIONS", "REBALANCE_OR_TRADE_TIMING", "DECISION_CRITERIA"
    ]


@pytest.mark.parametrize("malformed", [None, "not-a-mapping", ["not-a-mapping"], 7])
def test_malformed_variant_entries_return_stable_diagnostics(tmp_path: Path, malformed: object) -> None:
    data = _data()
    data["variants"]["definitions"][1] = malformed
    errors = _validate_copy(tmp_path, data)
    assert "malformed variant entry at index 1: expected mapping" in errors
    assert "frozen contract drift" in errors


def test_malformed_variant_entries_reject_under_optimized_python(tmp_path: Path) -> None:
    paths = []
    for index, malformed in enumerate((None, "not-a-mapping", ["not-a-mapping"], 7)):
        data = _data()
        data["variants"]["definitions"][1] = malformed
        path = tmp_path / f"variant-{index}.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        paths.append(path)
    code = "import sys,whole_portfolio_robustness_v2_preregistration_validator as v; results=[v.validate(prereg_path=v.Path(p)) for p in sys.argv[1:]]; raise SystemExit(0 if all(any('malformed variant entry at index 1' in e for e in r) for r in results) else 1)"
    result = subprocess.run([sys.executable, "-O", "-c", code, *(str(path) for path in paths)], cwd=validator.ROOT, check=False)
    assert result.returncode == 0


def test_malformed_directly_related_registries_do_not_crash_diagnostics(tmp_path: Path) -> None:
    for path_parts, expected in (
        (("portfolio_mechanics", "non_xnys_boundary_examples"), "non-XNYS dividend boundary registry malformed"),
        (("review_thresholds", "linked_tail_gate", "predeclared_paths"), "linked tail-path registry malformed"),
    ):
        data = _data()
        target = data
        for part in path_parts[:-1]:
            target = target[part]
        target[path_parts[-1]] = [None, "invalid"]
        errors = _validate_copy(tmp_path, data)
        assert expected in errors


@pytest.mark.parametrize("replacement", [None, "invalid", [], 7])
def test_malformed_baseline_sleeves_returns_diagnostics(tmp_path: Path, replacement: object) -> None:
    data = _data()
    data["baseline"]["sleeves_pct"] = replacement
    errors = _validate_copy(tmp_path, data)
    assert "baseline.sleeves_pct: expected mapping" in errors
    assert "frozen contract drift" in errors


@pytest.mark.parametrize("value", ["NaN", "Infinity", "not-a-number", None])
def test_invalid_baseline_numbers_return_path_diagnostics(tmp_path: Path, value: object) -> None:
    data = _data()
    data["baseline"]["sleeves_pct"]["eligible_direct_equity"] = value
    errors = _validate_copy(tmp_path, data)
    assert any("baseline.sleeves_pct.eligible_direct_equity" in error for error in errors)
    assert "frozen contract drift" in errors


@pytest.mark.parametrize("section", [
    "correction", "frozen_inputs", "integrity", "baseline", "variants", "frictions",
    "review_thresholds", "portfolio_mechanics", "safety",
])
def test_malformed_top_level_mapping_sections_never_escape(tmp_path: Path, section: str) -> None:
    data = _data()
    data[section] = ["invalid"]
    errors = _validate_copy(tmp_path, data)
    assert errors
    assert f"{section}: expected mapping" in errors


def test_malformed_registry_identities_never_reach_set_with_unhashable_values(tmp_path: Path) -> None:
    for mutate, diagnostic in (
        (lambda data: data["variants"]["definitions"][0].update(id=["BASELINE"]), "fixed variant registry malformed"),
        (lambda data: data["frictions"]["cell_registry"][0].update(tax_profile=["TAX_DEFERRED"]), "malformed cell registry identity"),
        (lambda data: data["baseline"].update(gated_tickers=[["SNPS"]]), "baseline.gated_tickers"),
    ):
        data = _data()
        mutate(data)
        errors = _validate_copy(tmp_path, data)
        assert any(diagnostic in error for error in errors)


def test_malformed_container_matrix_rejects_under_optimized_python(tmp_path: Path) -> None:
    paths = []
    mutations = [
        lambda data: data["baseline"].update(sleeves_pct=[]),
        lambda data: data["baseline"]["sleeves_pct"].update(eligible_direct_equity="NaN"),
        lambda data: data.update(correction=None),
        lambda data: data.update(frozen_inputs="invalid"),
        lambda data: data.update(integrity=[]),
        lambda data: data.update(variants=7),
        lambda data: data.update(frictions=None),
        lambda data: data.update(review_thresholds="invalid"),
        lambda data: data.update(portfolio_mechanics=[]),
        lambda data: data.update(safety=7),
    ]
    for index, mutate in enumerate(mutations):
        data = _data()
        mutate(data)
        path = tmp_path / f"container-{index}.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        paths.append(path)
    code = "import sys,whole_portfolio_robustness_v2_preregistration_validator as v; results=[v.validate(prereg_path=v.Path(p)) for p in sys.argv[1:]]; raise SystemExit(0 if all(r for r in results) else 1)"
    result = subprocess.run([sys.executable, "-O", "-c", code, *(str(path) for path in paths)], cwd=validator.ROOT, check=False)
    assert result.returncode == 0


def test_missing_pinned_v2_protocol_returns_diagnostic(tmp_path: Path) -> None:
    root = _isolated_root(tmp_path)
    (root / validator.PROTOCOL.relative_to(validator.ROOT)).unlink()
    errors = validator.validate(root=root)
    assert f"missing pinned protocol: {validator.PROTOCOL.relative_to(validator.ROOT)}" in errors


@pytest.mark.parametrize("window", ["context", "UNKNOWN_WINDOW", None])
def test_support_gate_rejects_nonvoting_unknown_or_removed_window(tmp_path: Path, window: object) -> None:
    data = _data()
    if window is None:
        del data["review_thresholds"]["support_gate"]["window"]
    else:
        data["review_thresholds"]["support_gate"]["window"] = window
    errors = _validate_copy(tmp_path, data)
    assert "support gate window changed" in errors
    assert "frozen contract drift" in errors


def test_support_and_decision_bootstrap_are_bound_to_voting_correction_window() -> None:
    data = _data()
    support = data["review_thresholds"]["support_gate"]
    assert support["window"] == "correction_replication"
    assert support["minimum_passing_cells"] == 15
    assert support["window_role"] == "VOTING_SUPPORT_COUNT_ONLY_CONTEXT_SUPPORT_CANNOT_SUBSTITUTE"
    assert data["bootstrap"]["decision_window"] == "correction_replication"
    assert data["bootstrap"]["context_role"] == "NON_VOTING_CONTEXT_EVIDENCE_CANNOT_SUBSTITUTE_FOR_CORRECTION_REPLICATION_DECISION_BOOTSTRAP"
    assert data["review_thresholds"]["context_direction_gate"]["window"] == "context"
