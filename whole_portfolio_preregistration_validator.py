"""Fail-closed validator for PORTFOLIO-ROBUSTNESS-0001.

The validator derives the study baseline from accepted policy files. It does
not read holdings, contact a broker, place orders, or touch Stage 1.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping

import yaml


ROOT = Path(__file__).resolve().parent
PREREG_PATH = ROOT / "research/whole_portfolio_robustness/pre_registration.yaml"
TARGETS_PATH = ROOT / "targets.yaml"
GATES_PATH = ROOT / "gates.yaml"
LOOKTHROUGH_PATH = ROOT / "issuer_lookthrough.yaml"
SOURCE_INVENTORY_PATH = ROOT / "research/level1_sleeve_robustness/data/source_inventory.json"
DFF_PATH = ROOT / "research/level1_sleeve_robustness/data/transformed/selected/DFF.json"
XNYS_PATH = ROOT / "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json"
MARKET_DATA_ROOT = ROOT / "research/level1_sleeve_robustness/data/transformed/candidates"

SLEEVES = (
    "eligible_direct_equity",
    "broad_market_funds",
    "gold",
    "crypto",
    "cash_and_protected_capital",
)
BROAD = frozenset({"SPY", "VEA", "VWO"})
GOLD = frozenset({"GLD"})
PREREGISTRATION_SHA256 = "d985952a527a5697f37177f281ac179ed7a0fdd35b760b52a93bf64fceb52c6c"


class PreregistrationError(ValueError):
    """Raised when the preregistration or its policy basis has drifted."""


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise PreregistrationError(f"{path}: mapping required")
    return value


def _decimal(value: Any, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise PreregistrationError(f"{label}: finite decimal required") from exc
    if not result.is_finite():
        raise PreregistrationError(f"{label}: finite decimal required")
    return result


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def market_data_path_hash(root: Path = MARKET_DATA_ROOT) -> tuple[int, str]:
    """Hash the sorted file-SHA listing, matching the shell freeze receipt."""

    files = sorted(path for path in root.rglob("*.json") if path.is_file())
    lines = "".join(f"{_sha256(path)}  {path.relative_to(ROOT)}\n" for path in files)
    return len(files), hashlib.sha256(lines.encode("utf-8")).hexdigest()


def derive_baseline(targets: Mapping[str, Any], gates: Mapping[str, Any]) -> dict[str, Decimal]:
    destination = targets.get("destination")
    gate_rows = gates.get("gates")
    if not isinstance(destination, list) or not isinstance(gate_rows, list):
        raise PreregistrationError("targets.destination and gates.gates must be lists")

    weights: dict[str, Decimal] = {}
    classes: dict[str, str] = {}
    for row in destination:
        if not isinstance(row, Mapping):
            raise PreregistrationError("destination row must be a mapping")
        ticker = str(row.get("ticker", "")).upper()
        if not ticker or ticker in weights:
            raise PreregistrationError(f"duplicate or empty destination ticker: {ticker!r}")
        weight = _decimal(row.get("target_pct"), f"{ticker}.target_pct")
        if weight < 0:
            raise PreregistrationError(f"{ticker}.target_pct must be non-negative")
        weights[ticker] = weight
        classes[ticker] = str(row.get("asset_class", ""))

    gate_tickers: set[str] = set()
    for row in gate_rows:
        if not isinstance(row, Mapping):
            raise PreregistrationError("gate row must be a mapping")
        ticker = str(row.get("ticker", "")).upper()
        if ticker in gate_tickers or ticker not in weights:
            raise PreregistrationError(f"invalid or duplicate gate ticker: {ticker!r}")
        if row.get("allow_add") is not False or row.get("status") != "cash_pending_clearance":
            raise PreregistrationError(f"{ticker}: study requires the accepted closed cash gate")
        gate_tickers.add(ticker)

    assigned = sum(weights.values(), Decimal("0"))
    if assigned > Decimal("100"):
        raise PreregistrationError("assigned targets exceed 100%")
    unallocated = Decimal("100") - assigned
    gated_cash = sum((weights[ticker] for ticker in gate_tickers), Decimal("0"))
    result = {name: Decimal("0") for name in SLEEVES}
    for ticker, weight in weights.items():
        asset_class = classes[ticker]
        if ticker in gate_tickers:
            result["cash_and_protected_capital"] += weight
        elif asset_class == "equity":
            result["eligible_direct_equity"] += weight
        elif asset_class == "crypto":
            result["crypto"] += weight
        elif asset_class in {"cash", "reserve"}:
            result["cash_and_protected_capital"] += weight
        elif asset_class == "fund" and ticker in BROAD:
            result["broad_market_funds"] += weight
        elif asset_class == "fund" and ticker in GOLD:
            result["gold"] += weight
        else:
            raise PreregistrationError(f"{ticker}: unregistered whole-portfolio mapping")
    result["cash_and_protected_capital"] += unallocated
    if sum(result.values(), Decimal("0")) != Decimal("100"):
        raise PreregistrationError("derived portfolio does not reconcile to 100%")
    result["target_assigned_pct"] = assigned
    result["unallocated_cash_pct"] = unallocated
    result["gated_target_cash_pct"] = gated_cash
    return result


def _expected_sleeves(value: Mapping[str, Any], label: str) -> dict[str, Decimal]:
    if set(value) != set(SLEEVES):
        raise PreregistrationError(f"{label}: exact sleeve set required")
    result = {key: _decimal(value[key], f"{label}.{key}") for key in SLEEVES}
    if any(weight < 0 for weight in result.values()) or sum(result.values()) != Decimal("100"):
        raise PreregistrationError(f"{label}: non-negative weights must sum to 100%")
    return result


def _validate_variants(prereg: Mapping[str, Any], baseline: Mapping[str, Decimal]) -> None:
    variants = prereg["variants"]
    if variants.get("optimization") != "PROHIBITED" or variants.get("grid_search") != "PROHIBITED":
        raise PreregistrationError("optimization and grid search must remain prohibited")
    definitions = variants.get("definitions")
    required_ids = {"BASELINE", "BROAD_PLUS_5", "DEFENSIVE_PLUS_5", "CRYPTO_HALF", "GOLD_PLUS_2", "DIVERSIFIED_BALANCE"}
    if not isinstance(definitions, list) or {row.get("id") for row in definitions} != required_ids:
        raise PreregistrationError("the six fixed portfolio definitions are required")
    base_weights = {key: baseline[key] for key in SLEEVES}
    for row in definitions:
        candidate = deepcopy(base_weights)
        transforms = row.get("transforms")
        if not isinstance(transforms, list):
            raise PreregistrationError(f"{row.get('id')}: transforms list required")
        for transfer in transforms:
            source, destination = transfer.get("from"), transfer.get("to")
            if source not in SLEEVES or destination not in SLEEVES or source == destination:
                raise PreregistrationError(f"{row.get('id')}: invalid sleeve transfer")
            if transfer.get("within_sleeve_rule") != "PRO_RATA":
                raise PreregistrationError(f"{row.get('id')}: only preregistered pro-rata transfers allowed")
            amount = _decimal(transfer.get("percentage_points"), "percentage_points")
            if amount <= 0 or candidate[source] < amount:
                raise PreregistrationError(f"{row.get('id')}: invalid transfer amount")
            candidate[source] -= amount
            candidate[destination] += amount
        expected = _expected_sleeves(row.get("expected_sleeves_pct", {}), str(row.get("id")))
        if candidate != expected:
            raise PreregistrationError(f"{row.get('id')}: transforms do not produce expected weights")


def validate_documents(prereg: Mapping[str, Any], targets: Mapping[str, Any], gates: Mapping[str, Any]) -> dict[str, Any]:
    if _canonical_sha256(prereg) != PREREGISTRATION_SHA256:
        raise PreregistrationError("registered study design drifted")
    if prereg.get("study_id") != "PORTFOLIO-ROBUSTNESS-0001" or prereg.get("status") != "PREREGISTERED_NOT_EXECUTED":
        raise PreregistrationError("wrong study identity or lifecycle state")
    if prereg["purpose"].get("automatic_adoption") != "PROHIBITED":
        raise PreregistrationError("automatic adoption must be prohibited")
    registered_gates = prereg["baseline"].get("gated_tickers")
    live_gates = [str(row.get("ticker", "")).upper() for row in gates.get("gates", [])]
    if registered_gates != live_gates:
        raise PreregistrationError("gated ticker order or membership drifted")
    baseline = derive_baseline(targets, gates)
    registered = _expected_sleeves(prereg["baseline"]["sleeves_pct"], "baseline")
    if registered != {key: baseline[key] for key in SLEEVES}:
        raise PreregistrationError("registered baseline does not match accepted targets and gates")
    for key in ("target_assigned_pct", "unallocated_cash_pct", "gated_target_cash_pct"):
        if _decimal(prereg["baseline"][key], key) != baseline[key]:
            raise PreregistrationError(f"registered {key} drifted")
    if _decimal(prereg["baseline"].get("reconciliation_total_pct"), "reconciliation_total_pct") != Decimal("100"):
        raise PreregistrationError("registered baseline must reconcile to 100%")
    components = prereg["baseline"].get("cash_and_protected_capital_components")
    expected_components = {
        "reserve": Decimal("4.00"),
        "explicit_cash": Decimal("1.00"),
        "unallocated_cash": baseline["unallocated_cash_pct"],
        "gated_target_cash": baseline["gated_target_cash_pct"],
    }
    if not isinstance(components, Mapping) or set(components) != set(expected_components):
        raise PreregistrationError("exact protected-cash component set required")
    registered_components = {
        key: _decimal(components[key], f"cash component {key}") for key in expected_components
    }
    if registered_components != expected_components or sum(registered_components.values()) != baseline["cash_and_protected_capital"]:
        raise PreregistrationError("protected-cash components do not reconcile to the derived baseline")
    _validate_variants(prereg, baseline)

    thresholds = prereg["review_thresholds"]
    if thresholds.get("default") != "RETAIN_BASELINE" or thresholds.get("close_call_rule") != "RETAIN_BASELINE":
        raise PreregistrationError("baseline-retention default required")
    if thresholds.get("target_change_rule") != "SEPARATE_EXPLICIT_REVIEWED_DECISION_REQUIRED":
        raise PreregistrationError("results must not silently change targets")
    gates_required = thresholds["required_for_recommend_policy_review"]
    if _decimal(gates_required.get("friction_cadence_cells_min_fraction_same_direction"), "stability") < Decimal("0.80"):
        raise PreregistrationError("multi-cell stability threshold weakened")
    if _decimal(gates_required.get("bootstrap_min_probability_sharpe_positive"), "bootstrap") < Decimal("0.75"):
        raise PreregistrationError("bootstrap confidence threshold weakened")

    bootstrap = prereg["bootstrap"]
    if bootstrap.get("resamples") != 2000 or bootstrap.get("mean_block_sessions") != 21 or bootstrap.get("seed") != 20260907:
        raise PreregistrationError("bootstrap design drifted")
    if prereg["portfolio_mechanics"].get("leverage") != "1.00" or prereg["portfolio_mechanics"].get("borrowing") != "PROHIBITED":
        raise PreregistrationError("whole-portfolio robustness must remain unlevered")

    safety = prereg["safety"]
    required_safety = {
        "advisory_only": True,
        "uses_holdings": False,
        "uses_brokerage_or_credentials": False,
        "places_orders_or_trades": False,
        "changes_targets_or_gates": False,
        "changes_margin_policy": False,
        "arms_or_executes_stage1": False,
        "stage1_state": "UNARMED_AND_NOT_EXECUTABLE",
    }
    if safety != required_safety:
        raise PreregistrationError("advisory-only safety boundary drifted")
    return {"study_id": prereg["study_id"], "status": "VALID", "baseline": {key: f"{baseline[key]:.2f}" for key in SLEEVES}}


def validate_files() -> dict[str, Any]:
    prereg = _load_yaml(PREREG_PATH)
    targets = _load_yaml(TARGETS_PATH)
    gates = _load_yaml(GATES_PATH)
    result = validate_documents(prereg, targets, gates)
    paths = {
        "targets.yaml": TARGETS_PATH,
        "gates.yaml": GATES_PATH,
        "issuer_lookthrough.yaml": LOOKTHROUGH_PATH,
        "source_inventory.json": SOURCE_INVENTORY_PATH,
        "DFF.json": DFF_PATH,
        "XNYS_sessions.json": XNYS_PATH,
    }
    pins = prereg["frozen_inputs"]["files"]
    for name, path in paths.items():
        if not path.is_file() or _sha256(path) != pins.get(name):
            raise PreregistrationError(f"frozen input hash mismatch: {name}")
    count, digest = market_data_path_hash()
    frozen = prereg["frozen_inputs"]
    if count != frozen.get("market_data_file_count") or digest != frozen.get("market_data_path_sha256"):
        raise PreregistrationError("market-data path inventory drifted")
    return result


if __name__ == "__main__":
    print(validate_files())
