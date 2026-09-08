#!/usr/bin/env python3
"""Fail-closed validation of the unexecuted PORTFOLIO-ROBUSTNESS-V2-0001 contract."""
from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "research/whole_portfolio_robustness_v2/pre_registration.yaml"
PROTOCOL = ROOT / "research/whole_portfolio_robustness_v2/PROTOCOL.md"
EXPECTED_CONTRACT_SHA256 = "775522c6840d494dd9c1849a50e4db0d3493b4e5754ac4706ec6ab5fa616e8dd"
EXPECTED_PINS = {
    "targets.yaml": "69cda30c3f2f7bff00ef4cd3f8f59cda83ece999145e82646ff0987041da874d",
    "gates.yaml": "e9a0bcd98a45f75b77e5f60076be34c4eda890255bb9aa0cf1a14868418f2d86",
    "issuer_lookthrough.yaml": "6cf4e417e747d9a1ae9621e57d238c685ab593fb65539d561a5d136c7027b0b9",
    "research/buy_ladder_backtest/inputs/input_disposition.json": "05a86b0f42df6b055532076d2e84e7ac7a460799012402904afe1fcb1e72ab2e",
    "research/buy_ladder_backtest/inputs/corporate_actions.json": "79be46b9e64191d4897c5b9ada2c7ba7cfb8c4f86eca4e9ec6943c5895a6d2f1",
    "research/buy_ladder_backtest/inputs/price_anomaly_overrides.json": "9f0a9513b769e036f4d1b209f5d63b6b32893fdc375a319252b5b89dc953c13f",
    "research/buy_ladder_backtest/PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md": "6f9e335caa5f0733c57932637cca1563a9daeb94a4dcdb81fe51587920f7c60f",
    "research/buy_ladder_backtest/PROTOCOL_V2.md": "0529d0d64b213ad876173ba16f555b6c27b7812f483a4839bdffd9f47d609fe4",
    "research/level1_sleeve_robustness/data/transformed/selected/DFF.json": "a4610d02a33fc4e72eff5c54ba8499b7d0f85e5d828dd054e4158f967b530b5b",
    "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json": "365c740ed489a2804189dee439a8cfe4fd926db1f92957988e51ad91db12fabe",
}
COSTS = ("0", "10", "25")
TAX_PROFILES = ("TAX_DEFERRED", "TAXABLE_MID", "TAXABLE_HIGH")
CADENCES = ("QUARTERLY", "ANNUAL")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class _UnambiguousSafeLoader(yaml.SafeLoader):
    """Safe YAML with duplicate keys, aliases, and merge keys rejected."""

    def compose_node(self, parent: Any, index: Any) -> Any:
        if self.check_event(yaml.AliasEvent):
            event = self.peek_event()
            raise yaml.constructor.ConstructorError(
                None, None, f"YAML aliases are prohibited: *{event.anchor}", event.start_mark
            )
        return super().compose_node(parent, index)

    def construct_mapping(self, node: Any, deep: bool = False) -> dict[Any, Any]:
        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(None, None, "expected mapping node", node.start_mark)
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "YAML merge keys are prohibited", key_node.start_mark,
                )
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "unhashable mapping key", key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"duplicate mapping key: {key!r}", key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _load(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=_UnambiguousSafeLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def _contract_digest(data: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(data, allow_nan=False))
    del clone["integrity"]["frozen_contract"]["expected_sha256"]
    canonical = json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _decimal(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{label} is boolean, not numeric")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{label} is not numeric") from exc
    if not number.is_finite():
        raise ValueError(f"{label} is nonfinite")
    return number


def _reject_nonfinite(value: Any, location: str = "root") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"nonfinite value at {location}")
    if isinstance(value, dict):
        for key, child in value.items():
            _reject_nonfinite(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_nonfinite(child, f"{location}[{index}]")


def validate(root: Path = ROOT, prereg_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    path = prereg_path or root / PREREG.relative_to(ROOT)

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def mapping(value: Any, location: str) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        errors.append(f"{location}: expected mapping")
        return {}

    try:
        p = _load(path)
        _reject_nonfinite(p)
    except Exception as exc:
        return [f"cannot load preregistration: {exc}"]

    try:
        declared_digest = p["integrity"]["frozen_contract"]["expected_sha256"]
        actual_digest = _contract_digest(p)
        require(declared_digest == EXPECTED_CONTRACT_SHA256, "contract digest declaration changed")
        require(actual_digest == EXPECTED_CONTRACT_SHA256, "frozen contract drift")
    except Exception as exc:
        errors.append(f"invalid or missing frozen contract digest: {exc}")

    require(p.get("study_id") == "PORTFOLIO-ROBUSTNESS-V2-0001", "wrong study_id")
    require(p.get("status") == "PREREGISTERED_NOT_EXECUTED", "study is not preregistered/unexecuted")
    correction = mapping(p.get("correction"), "correction")
    require(correction.get("kind") == "PRE_EXECUTION_CONTRACT_CORRECTION", "pre-execution correction label missing")
    require(correction.get("study_identity_preserved") is True, "study identity is not preserved")

    frozen_inputs = mapping(p.get("frozen_inputs"), "frozen_inputs")
    pins = frozen_inputs.get("files")
    require(pins == EXPECTED_PINS, "pinned-file registry changed, incomplete, duplicated, or self-removed")
    if isinstance(pins, dict):
        for rel, expected in EXPECTED_PINS.items():
            candidate = root / rel
            require(candidate.is_file(), f"missing pinned file: {rel}")
            if candidate.is_file():
                require(_sha256(candidate) == expected, f"pin drift: {rel}")
    incorporation = mapping(frozen_inputs.get("upstream_incorporation_scope"), "frozen_inputs.upstream_incorporation_scope")
    require(incorporation.get("local_v2_precedence") == "THIS_PRE_REGISTRATION_PORTFOLIO_MECHANICS_AND_FRICTIONS_CONTROL_AND_SUPERSEDE_ANY_PREDECESSOR_CONFLICT", "upstream/local precedence changed")
    require(incorporation.get("retained_normative_mechanics") == [
        "ACCEPTED_INPUT_DISPOSITION_AND_PRICE_ANOMALY_CORRECTIONS", "SPLIT_NORMALIZATION",
        "PRIOR_CLOSE_SHARE_ENTITLEMENT", "EX_DATE_NET_RECEIVABLE_RECOGNITION",
        "SOURCE_WITHHOLDING_AND_SAME_DIVIDEND_FOREIGN_TAX_CREDIT_MECHANICS",
    ], "upstream incorporation scope changed")
    require(incorporation.get("not_imported") == [
        "LADDER_ARMS", "FILLS", "BUDGETS_OR_CONTRIBUTIONS", "REBALANCE_OR_TRADE_TIMING", "DECISION_CRITERIA"
    ], "excluded predecessor mechanics changed")
    integrity = mapping(p.get("integrity"), "integrity")
    protocol_path = root / PROTOCOL.relative_to(ROOT)
    require(protocol_path.is_file(), f"missing pinned protocol: {PROTOCOL.relative_to(ROOT)}")
    if protocol_path.is_file():
        require(integrity.get("protocol_sha256") == _sha256(protocol_path), "protocol pin drift")

    baseline_section = mapping(p.get("baseline"), "baseline")
    baseline_sleeves = mapping(baseline_section.get("sleeves_pct"), "baseline.sleeves_pct")

    try:
        targets = _load(root / "targets.yaml")["destination"]
        gates = _load(root / "gates.yaml")["gates"]
        tickers = [row["ticker"] for row in targets]
        gate_tickers = [row["ticker"] for row in gates]
        require(len(tickers) == len(set(tickers)), "duplicate target ticker")
        require(len(gate_tickers) == len(set(gate_tickers)), "duplicate gate ticker")
        gated = set(gate_tickers)
        registered_gates = baseline_section.get("gated_tickers")
        if not isinstance(registered_gates, list) or not all(isinstance(ticker, str) for ticker in registered_gates):
            raise ValueError("baseline.gated_tickers: expected list of string identities")
        require(gated == set(registered_gates), "gated ticker set mismatch")
        assigned = sum((_decimal(row["target_pct"], f"target {row['ticker']}") for row in targets), Decimal(0))
        require(assigned == _decimal(baseline_section.get("target_assigned_pct"), "baseline.target_assigned_pct"), "assigned target total mismatch")
        by_ticker = {row["ticker"]: row for row in targets}
        unallocated = Decimal(100) - assigned
        gated_weight = sum((_decimal(by_ticker[t]["target_pct"], f"gated target {t}") for t in gated), Decimal(0))
        sleeves = {
            "eligible_direct_equity": sum((_decimal(r["target_pct"], r["ticker"]) for r in targets if r["asset_class"] == "equity" and r["ticker"] not in gated), Decimal(0)),
            "broad_market_funds": sum((_decimal(r["target_pct"], r["ticker"]) for r in targets if r["asset_class"] == "fund" and r["ticker"] != "GLD"), Decimal(0)),
            "gold": _decimal(by_ticker["GLD"]["target_pct"], "GLD"),
            "crypto": sum((_decimal(r["target_pct"], r["ticker"]) for r in targets if r["asset_class"] == "crypto"), Decimal(0)),
            "cash_and_protected_capital": sum((_decimal(r["target_pct"], r["ticker"]) for r in targets if r["asset_class"] in {"cash", "reserve"}), Decimal(0)) + gated_weight + unallocated,
        }
        declared = {k: _decimal(v, f"baseline.sleeves_pct.{k}") for k, v in baseline_sleeves.items()}
        require(sleeves == declared and sum(declared.values()) == Decimal("100.00"), "derived baseline sleeves mismatch")
    except Exception as exc:
        errors.append(f"cannot derive baseline: {exc}")

    variants = mapping(p.get("variants"), "variants")
    definitions = variants.get("definitions", [])
    if not isinstance(definitions, list):
        errors.append("variant registry must be a list")
        definitions = []
    expected_ids = ["BASELINE", "BROAD_PLUS_5", "DEFENSIVE_PLUS_5", "CRYPTO_HALF", "GOLD_PLUS_2", "DIVERSIFIED_BALANCE"]
    ids = [v.get("id") for v in definitions if isinstance(v, dict)]
    identities_are_strings = all(isinstance(identity, str) for identity in ids)
    unique_ids = identities_are_strings and len(ids) == len(set(ids))
    require(ids == expected_ids and unique_ids, "fixed variant registry malformed or duplicated")
    baseline: dict[str, Decimal] = {}
    for key, value in baseline_sleeves.items():
        try:
            baseline[key] = _decimal(value, f"baseline.sleeves_pct.{key}")
        except Exception as exc:
            errors.append(str(exc))
    for index, variant in enumerate(definitions):
        if not isinstance(variant, dict):
            errors.append(f"malformed variant entry at index {index}: expected mapping")
            continue
        try:
            derived = dict(baseline)
            for transform in variant["transforms"]:
                amount = _decimal(transform["percentage_points"], "transform amount")
                require(amount > 0, f"variant {variant['id']} transform must be positive")
                require(transform.get("within_sleeve_rule") == "PRO_RATA", f"variant {variant['id']} transform is not pro rata")
                derived[transform["from"]] -= amount
                derived[transform["to"]] += amount
            expected = {k: _decimal(v, k) for k, v in variant["expected_sleeves_pct"].items()}
            require(derived == expected and sum(expected.values()) == Decimal(100), f"variant {variant['id']} expected sleeves do not match transforms")
        except Exception as exc:
            errors.append(f"invalid variant {variant.get('id', f'index {index}')}: {exc}")

    frictions = mapping(p.get("frictions"), "frictions")
    require(frictions.get("primary_cell") == {"one_way_cost_bps": "10", "tax_profile": "TAXABLE_MID", "rebalance_cadence": "QUARTERLY"}, "primary cell changed")
    registry = frictions.get("cell_registry", [])
    expected_cells = [(c, t, cadence) for c in COSTS for t in TAX_PROFILES for cadence in CADENCES]
    actual_cells = []
    for cell in registry if isinstance(registry, list) else []:
        if not isinstance(cell, dict):
            errors.append("malformed cell registry entry")
            continue
        raw_triple = (cell.get("one_way_cost_bps"), cell.get("tax_profile"), cell.get("rebalance_cadence"))
        if not all(isinstance(item, str) for item in raw_triple):
            errors.append("malformed cell registry identity: expected strings")
            continue
        triple = raw_triple
        actual_cells.append(triple)
        require(cell.get("cell_id") == f"COST_{triple[0]}_TAX_{triple[1]}_CADENCE_{triple[2]}", "malformed cell id")
    require(actual_cells == expected_cells and len(set(actual_cells)) == 18, "cell registry is not the exact unique 18-cell Cartesian product")

    thresholds = mapping(p.get("review_thresholds"), "review_thresholds")
    support = mapping(thresholds.get("support_gate"), "review_thresholds.support_gate")
    require(support.get("window") == "correction_replication", "support gate window changed")
    require(support.get("window_role") == "VOTING_SUPPORT_COUNT_ONLY_CONTEXT_SUPPORT_CANNOT_SUBSTITUTE", "support gate window role changed")
    require(support.get("minimum_passing_cells") == 15 and support.get("minimum_fraction") == "0.80", "80% support threshold changed")
    require(support.get("primary_cell_included") is True, "primary cell excluded from support denominator")
    predicate = support.get("cell_predicate_all_required", {})
    require(predicate == {"net_cagr_delta_pp_per_year_gte": "-0.50", "sharpe_delta_gte": "0.05", "sortino_delta_gte": "0.05", "tail_either": {"max_drawdown_improvement_pp_gte": "2.00", "daily_cvar_95_improvement_pp_gte": "0.10"}}, "cell predicate changed")
    bootstrap = mapping(p.get("bootstrap"), "bootstrap")
    require(bootstrap.get("decision_window") == "correction_replication", "decision bootstrap window changed")
    require(bootstrap.get("context_role") == "NON_VOTING_CONTEXT_EVIDENCE_CANNOT_SUBSTITUTE_FOR_CORRECTION_REPLICATION_DECISION_BOOTSTRAP", "bootstrap context role changed")
    foreign = mapping(frictions.get("foreign_dividends"), "frictions.foreign_dividends")
    require(foreign.get("sensitivity_inventory") == ["STANDARD_AVAILABLE_CREDIT", "ZERO_FOREIGN_TAX_CREDIT", "ETN_25_PERCENT_IRISH_WITHHOLDING", "JOINT_ZERO_CREDIT_AND_ETN_25_PERCENT_IRISH_WITHHOLDING"], "foreign sensitivity inventory changed")
    require(foreign.get("decision_rule") == "FULL_CANONICALLY_ORDERED_PASSING_SET_OR_EVERY_PER_VARIANT_GATE_BOOLEAN_CHANGE_CAUSES_UNABLE_TO_DETERMINE", "foreign decision rule changed")
    require(foreign.get("veto") == "IF_ANY_SEPARATE_OR_JOINT_CASE_CHANGES_FULL_CANONICALLY_ORDERED_PASSING_SET_OR_ANY_PER_VARIANT_GATE_BOOLEAN_THEN_UNABLE_TO_DETERMINE", "foreign veto changed")

    dividend = mapping(p.get("portfolio_mechanics"), "portfolio_mechanics")
    cash = mapping(dividend.get("cash_accrual"), "portfolio_mechanics.cash_accrual")
    require(cash.get("tax_rate") == "CURRENT_CELL_TAX_PROFILE_ORDINARY_INCOME_RATE", "cash ordinary-income tax rule changed")
    require(cash.get("day_count") == "ACT/360" and cash.get("annual_drag_bps") == "25", "cash accrual convention changed")
    require(dividend.get("dividend_boundary_example") == {"prior_close_shares": "1", "prior_close_price": "100", "ex_date_price": "98", "gross_dividend": "2", "tax_profile": "TAX_DEFERRED", "ex_date_nav": "100", "ex_date_spendable_cash": "0", "payable_date_cash_before_other_events": "2"}, "dividend boundary example changed")
    require(dividend.get("dividend_settlement_calendar") == "EVERY_CALENDAR_DATE_NOT_ONLY_XNYS_SESSIONS", "dividend settlement calendar changed")
    examples = dividend.get("non_xnys_boundary_examples", [])
    examples_well_formed = isinstance(examples, list) and len(examples) == 2 and all(isinstance(x, dict) for x in examples)
    require(examples_well_formed, "non-XNYS dividend boundary registry malformed")
    if examples_well_formed:
        require([(x.get("ticker"), x.get("payable_date"), x.get("first_eligible_accrual_day"), x.get("first_interest_credit_date")) for x in examples] == [
            ("TMO", "2023-01-16", "2023-01-17", "2023-01-18"),
            ("TSM", "2025-01-09", "2025-01-10", "2025-01-11"),
        ], "non-XNYS dividend boundary examples changed")
        traces = [example.get("xnys_trace") for example in examples]
        traces_well_formed = all(isinstance(trace, list) and all(isinstance(row, dict) for row in trace) for trace in traces)
        require(traces_well_formed, "non-XNYS dividend trace registry malformed")
        if traces_well_formed:
            require([row.get("xnys_close_nav") for row in traces[0] if row.get("xnys_session")] == [
                "100.0000000000000000000000000000000000000", "100.0098611111111111111111111111111111111"
            ], "TMO interest posting trace changed")
            require([row.get("xnys_close_nav") for row in traces[1] if row.get("xnys_session")] == [
                "100.0000000000000000000000000000000000000", "100.0295862506745946394890260631001371742"
            ], "TSM interest posting trace changed")

    linked_tail = mapping(thresholds.get("linked_tail_gate"), "review_thresholds.linked_tail_gate")
    tail_paths = linked_tail.get("predeclared_paths", [])
    tail_paths_well_formed = isinstance(tail_paths, list) and len(tail_paths) == 2 and all(isinstance(x, dict) for x in tail_paths)
    require(tail_paths_well_formed, "linked tail-path registry malformed")
    if tail_paths_well_formed:
        require([(x.get("tail_metric"), x.get("primary_improvement_pp_gte"), x.get("bootstrap_probability_positive_gte")) for x in tail_paths] == [
            ("MAX_DRAWDOWN", "2.00", "0.75"), ("DAILY_CVAR_95", "0.10", "0.75")
        ], "linked tail/bootstrap paths changed")
    disposition = mapping(thresholds.get("multiple_passer_disposition"), "review_thresholds.multiple_passer_disposition")
    require(disposition.get("canonical_alternative_order") == [
        "BROAD_PLUS_5", "DEFENSIVE_PLUS_5", "CRYPTO_HALF", "GOLD_PLUS_2", "DIVERSIFIED_BALANCE"
    ], "multiple-passer canonical order changed")

    safety = mapping(p.get("safety"), "safety")
    require(safety.get("stage1_state") == "UNARMED_AND_NOT_EXECUTABLE", "Stage 1 boundary changed")
    for key in ("uses_holdings", "uses_brokerage_or_credentials", "places_orders_or_trades", "changes_targets_or_gates", "changes_margin_policy", "arms_or_executes_stage1"):
        require(safety.get(key) is False, f"unsafe capability enabled: {key}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print("PASS: PORTFOLIO-ROBUSTNESS-V2-0001 contract is frozen, reconciled, and unexecuted")
