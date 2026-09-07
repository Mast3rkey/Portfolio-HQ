#!/usr/bin/env python3
"""Fail-closed checks for PORTFOLIO-ROBUSTNESS-V2-0001 preregistration."""

from __future__ import annotations

import hashlib
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "research/whole_portfolio_robustness_v2/pre_registration.yaml"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def validate(root: Path = ROOT, prereg_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    path = prereg_path or (root / PREREG.relative_to(ROOT))
    try:
        p = _load(path)
    except Exception as exc:  # fail closed with useful diagnostics
        return [f"cannot load preregistration: {exc}"]

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(p.get("study_id") == "PORTFOLIO-ROBUSTNESS-V2-0001", "wrong study_id")
    require(p.get("status") == "PREREGISTERED_NOT_EXECUTED", "study is not preregistered/unexecuted")
    predecessor = p.get("predecessor", {})
    require(predecessor.get("disposition") == "EVIDENCE_LIMITED_NOT_DECISION_GRADE", "predecessor limitation missing")
    require(predecessor.get("historical_holdout_exposure") == "EXPOSED_CORRECTION_REPLICATION_NOT_FRESH_HOLDOUT", "holdout exposure mislabeled")

    pins = p.get("frozen_inputs", {}).get("files", {})
    for rel, expected in pins.items():
        candidate = root / rel
        require(candidate.is_file(), f"missing pinned file: {rel}")
        if candidate.is_file():
            require(_sha256(candidate) == expected, f"pin drift: {rel}")
    frozen = p.get("frozen_inputs", {})
    require(frozen.get("crypto_required") == ["BTC", "ETH", "SOL"], "crypto roster must include BTC/ETH/SOL")
    require(frozen.get("crypto") == "NEW_SUCCESSOR_DISPOSITION_REQUIRED_BEFORE_EXECUTION", "crypto evidence gate missing")

    try:
        targets = _load(root / "targets.yaml")["destination"]
        gates = _load(root / "gates.yaml")["gates"]
        gated = {row["ticker"] for row in gates}
        expected_gated = set(p["baseline"]["gated_tickers"])
        require(gated == expected_gated, "gated ticker set does not derive from gates.yaml")
        assigned = sum(Decimal(str(row["target_pct"])) for row in targets)
        require(assigned == Decimal(p["baseline"]["target_assigned_pct"]), "assigned target total mismatch")
        unallocated = Decimal("100") - assigned
        require(unallocated == Decimal(p["baseline"]["unallocated_cash_pct"]), "unallocated cash mismatch")
        by_ticker = {row["ticker"]: row for row in targets}
        gated_weight = sum(Decimal(str(by_ticker[t]["target_pct"])) for t in gated)
        require(gated_weight == Decimal(p["baseline"]["gated_target_cash_pct"]), "gated cash mismatch")
        sleeves = {
            "eligible_direct_equity": sum(Decimal(str(r["target_pct"])) for r in targets if r["asset_class"] == "equity" and r["ticker"] not in gated),
            "broad_market_funds": sum(Decimal(str(r["target_pct"])) for r in targets if r["asset_class"] == "fund" and r["ticker"] != "GLD"),
            "gold": Decimal(str(by_ticker["GLD"]["target_pct"])),
            "crypto": sum(Decimal(str(r["target_pct"])) for r in targets if r["asset_class"] == "crypto"),
            "cash_and_protected_capital": sum(Decimal(str(r["target_pct"])) for r in targets if r["asset_class"] in {"cash", "reserve"}) + gated_weight + unallocated,
        }
        declared = {k: Decimal(v) for k, v in p["baseline"]["sleeves_pct"].items()}
        require(sleeves == declared, f"derived sleeves mismatch: {sleeves}")
        require(sum(declared.values()) == Decimal("100.00"), "baseline does not reconcile to 100%")
    except Exception as exc:
        errors.append(f"cannot derive baseline: {exc}")

    required_variants = {"BASELINE", "BROAD_PLUS_5", "DEFENSIVE_PLUS_5", "CRYPTO_HALF", "GOLD_PLUS_2", "DIVERSIFIED_BALANCE"}
    definitions = p.get("variants", {}).get("definitions", [])
    require({v.get("id") for v in definitions} == required_variants, "fixed variant set mismatch")
    for variant in definitions:
        try:
            total = sum(Decimal(x) for x in variant["expected_sleeves_pct"].values())
            require(total == Decimal("100.00"), f"variant {variant.get('id')} does not sum to 100%")
        except Exception as exc:
            errors.append(f"invalid variant {variant.get('id')}: {exc}")

    windows = p.get("windows", {})
    require(windows.get("correction_replication", {}).get("exposure") == "PREVIOUSLY_EXPOSED", "correction interval exposure missing")
    require(windows.get("asset_selected_peak_trough_windows") == "PROHIBITED", "asset-selected windows not prohibited")
    require(len(windows.get("fixed_regimes", [])) >= 5, "insufficient fixed regime subperiods")
    require(p.get("frictions", {}).get("one_way_cost_bps") == ["0", "10", "25"], "cost sensitivities changed")
    require(set(p.get("frictions", {}).get("tax_profiles", [])) == {"TAX_DEFERRED", "TAXABLE_MID", "TAXABLE_HIGH"}, "tax sensitivity incomplete")
    require(p.get("bootstrap", {}).get("resamples") == 2000, "bootstrap draws changed")
    require(p.get("bootstrap", {}).get("mean_block_sessions") == 21, "bootstrap block length changed")

    metric_groups = p.get("metrics", {})
    for group in ("return", "risk_adjusted", "tail", "concentration", "operations"):
        require(bool(metric_groups.get(group)), f"missing metric group: {group}")
    thresholds = p.get("review_thresholds", {})
    require(thresholds.get("default") == "RETAIN_BASELINE", "baseline is not default disposition")
    require(thresholds.get("close_call_rule") == "RETAIN_BASELINE", "close-call rule changed")
    require(thresholds.get("target_change_rule") == "SEPARATE_EXPLICIT_REVIEWED_DECISION_REQUIRED", "automatic target change possible")

    integrity = p.get("integrity", {})
    for key in ("no_interpolation", "no_forward_fill_prices", "no_zero_return_substitution"):
        require(integrity.get(key) is True, f"integrity control disabled: {key}")
    require(integrity.get("execution_before_preregistration_merge") == "PROHIBITED", "result-blind merge gate missing")

    safety = p.get("safety", {})
    require(safety.get("advisory_only") is True, "advisory-only boundary missing")
    for key in ("uses_holdings", "uses_brokerage_or_credentials", "places_orders_or_trades", "changes_targets_or_gates", "changes_margin_policy", "arms_or_executes_stage1"):
        require(safety.get(key) is False, f"unsafe capability enabled: {key}")
    require(safety.get("stage1_state") == "UNARMED_AND_NOT_EXECUTABLE", "Stage 1 boundary changed")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print("PASS: PORTFOLIO-ROBUSTNESS-V2-0001 is frozen, internally reconciled, and unexecuted")
