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
    require(all(isinstance(v.get("hypothesis"), str) and v["hypothesis"].strip() for v in definitions), "variant hypothesis missing")
    baseline_sleeves = {k: Decimal(v) for k, v in p.get("baseline", {}).get("sleeves_pct", {}).items()}
    for variant in definitions:
        try:
            expected = {k: Decimal(x) for k, x in variant["expected_sleeves_pct"].items()}
            total = sum(expected.values())
            require(total == Decimal("100.00"), f"variant {variant.get('id')} does not sum to 100%")
            derived = dict(baseline_sleeves)
            for transform in variant.get("transforms", []):
                amount = Decimal(transform["percentage_points"])
                derived[transform["from"]] -= amount
                derived[transform["to"]] += amount
                require(transform.get("within_sleeve_rule") == "PRO_RATA", f"variant {variant.get('id')} transform is not pro rata")
            require(derived == expected, f"variant {variant.get('id')} expected sleeves do not match transforms")
        except Exception as exc:
            errors.append(f"invalid variant {variant.get('id')}: {exc}")

    windows = p.get("windows", {})
    require(windows.get("correction_replication", {}).get("exposure") == "PREVIOUSLY_EXPOSED", "correction interval exposure missing")
    require(windows.get("asset_selected_peak_trough_windows") == "PROHIBITED", "asset-selected windows not prohibited")
    require(len(windows.get("fixed_regimes", [])) >= 5, "insufficient fixed regime subperiods")
    require(p.get("frictions", {}).get("one_way_cost_bps") == ["0", "10", "25"], "cost sensitivities changed")
    require(set(p.get("frictions", {}).get("tax_profiles", [])) == {"TAX_DEFERRED", "TAXABLE_MID", "TAXABLE_HIGH"}, "tax sensitivity incomplete")
    mechanics = p.get("portfolio_mechanics", {})
    require(mechanics.get("valuation_calendar") == "XNYS_SESSIONS", "portfolio valuation calendar missing")
    require(mechanics.get("crypto_calendar_alignment") == "COMPOUND_EVERY_INTERVENING_UTC_DAILY_CLOSE_RETURN_INTO_NEXT_XNYS_VALUATION_NO_FUTURE_CLOSE", "crypto weekend/calendar alignment ambiguous")
    require(mechanics.get("survivorship_disclosure") == "CURRENT_ROSTER_HISTORICAL_COUNTERFACTUAL_WITH_HINDSIGHT_SELECTION_BIAS", "survivorship disclosure missing")
    foreign = p.get("frictions", {}).get("foreign_dividends", {})
    require(foreign.get("tentative_us_tax_rate") == "PROFILE_QUALIFIED_FRACTION_TIMES_QUALIFIED_RATE_PLUS_REMAINDER_TIMES_ORDINARY_RATE", "foreign-dividend U.S. tax-rate rule ambiguous")
    require(foreign.get("foreign_tax_credit_cap") == "SAME_DIVIDEND_TENTATIVE_US_TAX", "foreign tax credit cap ambiguous")
    require(set(foreign.get("mandatory_sensitivities", [])) == {"ZERO_FOREIGN_TAX_CREDIT", "ETN_25_PERCENT_IRISH_WITHHOLDING"}, "foreign-dividend sensitivities incomplete")
    require(foreign.get("decision_rule") == "WINNER_OR_GATE_CHANGE_CAUSES_UNABLE_TO_DETERMINE", "foreign-dividend decision rule ambiguous")
    require(p.get("frictions", {}).get("dividend_tax_timing") == "EX_DATE_DEBIT", "dividend tax timing ambiguous")
    require(p.get("frictions", {}).get("realized_gain_tax_timing") == "EACH_REBALANCE", "realized-gain tax timing ambiguous")
    require(p.get("bootstrap", {}).get("resamples") == 2000, "bootstrap draws changed")
    require(p.get("bootstrap", {}).get("mean_block_sessions") == 21, "bootstrap block length changed")

    metric_groups = p.get("metrics", {})
    for group in ("return", "risk_adjusted", "tail", "concentration", "operations"):
        require(bool(metric_groups.get(group)), f"missing metric group: {group}")
    thresholds = p.get("review_thresholds", {})
    require(thresholds.get("default") == "RETAIN_BASELINE", "baseline is not default disposition")
    require(thresholds.get("close_call_rule") == "RETAIN_BASELINE", "close-call rule changed")
    require(thresholds.get("target_change_rule") == "SEPARATE_EXPLICIT_REVIEWED_DECISION_REQUIRED", "automatic target change possible")
    concentration = thresholds.get("required_for_recommend_policy_review", {}).get("concentration_limits", {})
    require(concentration == {
        "direct_hhi_max_delta": "0.00",
        "max_direct_name_max_delta_pp": "0.00",
        "effective_issuer_max_worsening_pp": "0.25",
        "ai_platform_common_driver_max_worsening_pp": "0.25",
        "semis_cluster_cap_pct": "25.00",
        "power_infra_cluster_cap_pct": "20.00",
    }, "numeric concentration limits missing or changed")

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
