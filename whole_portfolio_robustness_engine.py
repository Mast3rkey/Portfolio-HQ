"""Network-free data gate for PORTFOLIO-ROBUSTNESS-0001.

This module intentionally stops before portfolio results.  It proves that the
registered roster can be evaluated from the exact frozen inputs.  Missing or
quarantined bytes are reported as evidence gaps; they are never replaced,
interpolated, forward-filled, or silently dropped.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

import yaml

import whole_portfolio_preregistration_validator as prereg_validator


ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "research/whole_portfolio_robustness"
PREREG_PATH = STUDY / "pre_registration.yaml"
TARGETS_PATH = ROOT / "targets.yaml"
GATES_PATH = ROOT / "gates.yaml"
SOURCE_INVENTORY_PATH = ROOT / "research/level1_sleeve_robustness/data/source_inventory.json"
XNYS_PATH = ROOT / "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json"
DFF_PATH = ROOT / "research/level1_sleeve_robustness/data/transformed/selected/DFF.json"
CANDIDATE_ROOT = ROOT / "research/level1_sleeve_robustness/data/transformed/candidates"

BROAD = frozenset({"SPY", "VEA", "VWO"})
GOLD = frozenset({"GLD"})
CASH_LIKE = frozenset({"CASH", "RESERVE"})


class DataGateError(RuntimeError):
    """Raised when frozen data cannot support the registered execution."""


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise DataGateError(f"{path}: JSON mapping required")
    return value


def _yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise DataGateError(f"{path}: YAML mapping required")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _days(start: str, end: str) -> list[str]:
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    return [(first + timedelta(days=n)).isoformat() for n in range((last - first).days + 1)]


def _inventory_rows(inventory: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    rows = list(inventory.get("stock_and_etf_datasets", [])) + list(inventory.get("crypto_datasets", []))
    result: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        ticker = str(row.get("instrument", ""))
        if not ticker or ticker in result:
            raise DataGateError(f"source inventory duplicate or empty instrument: {ticker!r}")
        result[ticker] = row
    return result


def derive_instrument_weights(
    targets: Mapping[str, Any], gates: Mapping[str, Any], prereg: Mapping[str, Any]
) -> dict[str, dict[str, Decimal]]:
    """Derive all six fixed portfolios without renormalizing accepted policy."""

    gate_tickers = {str(row["ticker"]) for row in gates["gates"]}
    destination = list(targets["destination"])
    assigned = sum((Decimal(str(row["target_pct"])) for row in destination), Decimal("0"))
    if assigned > Decimal("100"):
        raise DataGateError("assigned targets exceed 100%")
    base: dict[str, Decimal] = {}
    sleeve_members: dict[str, list[str]] = {
        "eligible_direct_equity": [], "broad_market_funds": [], "gold": [], "crypto": []
    }
    cash = Decimal("100") - assigned
    for row in destination:
        ticker = str(row["ticker"])
        weight = Decimal(str(row["target_pct"]))
        kind = str(row["asset_class"])
        if ticker in gate_tickers or ticker in CASH_LIKE:
            cash += weight
            continue
        if kind == "equity":
            sleeve = "eligible_direct_equity"
        elif kind == "crypto":
            sleeve = "crypto"
        elif kind == "fund" and ticker in BROAD:
            sleeve = "broad_market_funds"
        elif kind == "fund" and ticker in GOLD:
            sleeve = "gold"
        else:
            raise DataGateError(f"{ticker}: no registered active-sleeve mapping")
        base[ticker] = weight
        sleeve_members[sleeve].append(ticker)
    base["CASH"] = cash
    if sum(base.values(), Decimal("0")) != Decimal("100"):
        raise DataGateError("baseline instrument weights do not total 100%")

    variants: dict[str, dict[str, Decimal]] = {}
    for definition in prereg["variants"]["definitions"]:
        weights = dict(base)
        for transfer in definition["transforms"]:
            source, target = transfer["from"], transfer["to"]
            amount = Decimal(str(transfer["percentage_points"]))
            if source == "cash_and_protected_capital":
                source_members = ["CASH"]
            else:
                source_members = sleeve_members[source]
            if target == "cash_and_protected_capital":
                target_members = ["CASH"]
            else:
                target_members = sleeve_members[target]
            source_total = sum((weights[item] for item in source_members), Decimal("0"))
            target_total = sum((weights[item] for item in target_members), Decimal("0"))
            if source_total < amount or source_total <= 0 or target_total <= 0:
                raise DataGateError(f"{definition['id']}: invalid pro-rata transfer")
            source_moved = Decimal("0")
            for item in source_members[:-1]:
                moved = amount * weights[item] / source_total
                weights[item] -= moved
                source_moved += moved
            weights[source_members[-1]] -= amount - source_moved
            target_moved = Decimal("0")
            for item in target_members[:-1]:
                moved = amount * weights[item] / target_total
                weights[item] += moved
                target_moved += moved
            weights[target_members[-1]] += amount - target_moved
            # Decimal division of pro-rata weights can leave a sub-ulp residue;
            # assign only that arithmetic residue to the final destination.
            residue = Decimal("100") - sum(weights.values(), Decimal("0"))
            if abs(residue) > Decimal("1e-20"):
                raise DataGateError(f"{definition['id']}: transfer failed exact reconciliation")
            weights[source_members[-1]] += residue
        if sum(weights.values(), Decimal("0")) != Decimal("100"):
            raise DataGateError(f"{definition['id']}: instrument weights do not total 100%")
        variants[str(definition["id"])] = weights
    return variants


def _candidate_path(ticker: str, kind: str) -> Path:
    folder = "alpaca_crypto" if kind == "crypto" else "alpaca"
    return CANDIDATE_ROOT / folder / f"{ticker}.json"


def _validate_document(path: Path, ticker: str) -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    try:
        doc = _json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DataGateError) as exc:
        return {}, [f"{ticker}: unreadable candidate: {exc}"]
    if doc.get("instrument") != ticker:
        issues.append(f"{ticker}: candidate identity mismatch")
    rows = doc.get("rows")
    if not isinstance(rows, list) or not rows:
        return doc, issues + [f"{ticker}: rows missing"]
    seen: set[str] = set()
    prior = ""
    for row in rows:
        day = str(row.get("date", ""))
        try:
            value = float(row.get("close"))
        except (TypeError, ValueError):
            value = math.nan
        if not day or day in seen or day <= prior:
            issues.append(f"{ticker}: dates must be unique and increasing")
            break
        if not math.isfinite(value) or value <= 0:
            issues.append(f"{ticker}: nonpositive or nonfinite close on {day}")
            break
        seen.add(day)
        prior = day
    return doc, issues


def _required_dates(kind: str, sessions: list[str], start: str, end: str) -> list[str]:
    if kind == "crypto":
        # Crypto close stamped D is complete at 00:00 UTC on D+1.  The XNYS
        # session on D therefore lawfully uses D-1, matching RISK-0001.
        return sorted({(date.fromisoformat(day) - timedelta(days=1)).isoformat()
                       for day in sessions if start <= day <= end})
    return [day for day in sessions if start <= day <= end]


@dataclass(frozen=True)
class GateReport:
    ready: bool
    freeze: dict[str, Any]
    issues: tuple[str, ...]


def build_data_gate(root: Path = ROOT) -> GateReport:
    """Validate the exact registered execution inputs and return a freeze receipt."""

    if root != ROOT:
        raise DataGateError("alternate roots are not supported; use dependency monkeypatching in tests")
    prereg_validator.validate_files()
    prereg = _yaml(PREREG_PATH)
    targets = _yaml(TARGETS_PATH)
    gates = _yaml(GATES_PATH)
    inventory = _json(SOURCE_INVENTORY_PATH)
    sources = _inventory_rows(inventory)
    variants = derive_instrument_weights(targets, gates, prereg)
    active = {str(row["ticker"]): str(row["asset_class"]) for row in targets["destination"]
              if str(row["ticker"]) in variants["BASELINE"] and str(row["ticker"]) != "CASH"}
    sessions_doc = _json(XNYS_PATH)
    sessions = [str(row["session"]) for row in sessions_doc["sessions"]]
    if sessions != sorted(set(sessions)):
        raise DataGateError("XNYS sessions must be unique and increasing")

    window = prereg["windows"]["holdout_all_current_assets"]
    start, end = str(window["start"]), str(window["end"])
    issues: list[str] = []
    datasets: dict[str, Any] = {}
    for ticker in sorted(active):
        kind = active[ticker]
        source = sources.get(ticker)
        if source is None:
            issues.append(f"{ticker}: source inventory row missing")
            continue
        selected_path = ROOT / str(source.get("selected_path", ""))
        selected_sha = str(source.get("selected_transformed_sha256", ""))
        candidate_path = _candidate_path(ticker, kind)
        doc, document_issues = _validate_document(candidate_path, ticker)
        issues.extend(document_issues)
        rows = {str(row["date"]) for row in doc.get("rows", [])}
        missing = [day for day in _required_dates(kind, sessions, start, end) if day not in rows]
        if missing:
            if selected_path.is_file() and _sha256(selected_path) == selected_sha:
                selected, selected_issues = _validate_document(selected_path, ticker)
                selected_rows = {str(row["date"]) for row in selected.get("rows", [])}
                selected_missing = [day for day in _required_dates(kind, sessions, start, end)
                                    if day not in selected_rows]
                if not selected_issues and not selected_missing:
                    doc, candidate_path, missing = selected, selected_path, []
                else:
                    issues.extend(selected_issues)
            if missing:
                issues.append(
                    f"{ticker}: {len(missing)} required holdout observations missing "
                    f"({missing[0]}..{missing[-1]}); pinned selected source "
                    f"{'available' if selected_path.is_file() else 'bytes unavailable'}"
                )
        datasets[ticker] = {
            "path": str(candidate_path.relative_to(ROOT)),
            "sha256": _sha256(candidate_path),
            "provider": doc.get("provider"),
            "row_count": len(doc.get("rows", [])),
            "selected_inventory_sha256": selected_sha,
        }

    dff = _json(DFF_PATH)
    dff_dates = {str(row["date"]) for row in dff.get("rows", [])}
    if not dff_dates or max(dff_dates) < end:
        issues.append("DFF: frozen comparator does not cover evaluation end")

    freeze = {
        "schema_version": "1.0",
        "study_id": prereg["study_id"],
        "gate": "READY" if not issues else "HALT",
        "holdout": {"start": start, "end": end},
        "preregistration_sha256": _sha256(PREREG_PATH),
        "targets_sha256": _sha256(TARGETS_PATH),
        "gates_sha256": _sha256(GATES_PATH),
        "source_inventory_sha256": _sha256(SOURCE_INVENTORY_PATH),
        "xnys_sha256": _sha256(XNYS_PATH),
        "dff_sha256": _sha256(DFF_PATH),
        "variant_instrument_weights_sha256": _canonical_hash(
            {name: {ticker: str(weight) for ticker, weight in sorted(weights.items())}
             for name, weights in sorted(variants.items())}
        ),
        "datasets": datasets,
        "advisory_only": True,
        "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    }
    return GateReport(not issues, freeze, tuple(issues))


def require_ready() -> dict[str, Any]:
    report = build_data_gate()
    if not report.ready:
        raise DataGateError("data gate halted: " + "; ".join(report.issues))
    return report.freeze


if __name__ == "__main__":
    report = build_data_gate()
    print(json.dumps({"freeze": report.freeze, "issues": report.issues}, indent=2, sort_keys=True))
    raise SystemExit(0 if report.ready else 2)
