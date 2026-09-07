"""Fail-closed validator for PORTFOLIO-ROBUSTNESS-0001 result bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

import whole_portfolio_robustness_engine as gate
import whole_portfolio_robustness_runner as runner


STUDY_ID = "PORTFOLIO-ROBUSTNESS-0001"
REQUIRED = {
    "input_freeze.json", "portfolio_paths.json", "metrics.json",
    "bootstrap.json", "sensitivity_matrix.json", "limitations.md",
    "results.md", "disposition.yaml", "output_manifest.json",
}
METRIC_NULLABLE = {"CALMAR", "RECOVERY_DAYS"}
BOOTSTRAP_STATS = {
    "NET_TWR_CAGR_DELTA", "SHARPE_DELTA",
    "MAX_DRAWDOWN_DELTA", "DAILY_CVAR_95_DELTA",
}
METRIC_IDENTITY = {
    "variant", "window", "cadence", "one_way_cost_bps", "tax_profile",
}
METRIC_SUPPORT = {
    "RECOVERY_CENSORED", "TRANSACTION_COST_DOLLARS", "TAX_PAID_DOLLARS",
    "DIVIDEND_TAX_DOLLARS", "REALIZED_GAIN_TAX_DOLLARS", "ENDING_VALUE",
    "FINAL_CASH", "FACTS_ONLY",
}
PATH_KEYS = {
    "cell_id", "variant", "window", "cadence", "one_way_cost_bps",
    "tax_profile", "dates", "index", "daily_net_returns",
    "daily_lagged_dff_returns",
}


class ResultValidationError(RuntimeError):
    """Raised when a result bundle violates its frozen output contract."""


def _reject_json_constant(token: str) -> None:
    raise ResultValidationError(f"nonfinite JSON token {token}")


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=_reject_json_constant,
    )
    if type(value) is not dict:
        raise ResultValidationError(f"{path.name}: JSON mapping required")
    return value


def _yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ResultValidationError(f"{path.name}: YAML mapping required")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_finite(value: Any, location: str, *, nullable: bool = False) -> None:
    if value is None:
        if not nullable:
            raise ResultValidationError(f"{location}: null is not permitted")
        return
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        if not math.isfinite(float(value)):
            raise ResultValidationError(f"{location}: nonfinite number")
        return
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_finite(item, f"{location}[{index}]", nullable=nullable)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            _assert_finite(item, f"{location}.{key}", nullable=key in METRIC_NULLABLE)
        return
    raise ResultValidationError(f"{location}: unsupported value type")


def _require_identity(document: Mapping[str, Any], name: str) -> None:
    if document.get("schema_version") != "1.0" or document.get("study_id") != STUDY_ID:
        raise ResultValidationError(f"{name}: schema or study identity mismatch")


def _validate_manifest(root: Path, manifest: Mapping[str, Any]) -> None:
    _require_identity(manifest, "output_manifest.json")
    if manifest.get("advisory_only") is not True:
        raise ResultValidationError("output_manifest.json: advisory boundary drift")
    if manifest.get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise ResultValidationError("output_manifest.json: Stage 1 boundary drift")
    expected = REQUIRED - {"output_manifest.json"}
    files = manifest.get("files")
    if type(files) is not dict or set(files) != expected:
        raise ResultValidationError("output_manifest.json: file registry mismatch")
    for name, digest in files.items():
        if digest != _sha256(root / name):
            raise ResultValidationError(f"{name}: output hash mismatch")


def _expected_registry(prereg: Mapping[str, Any]) -> tuple[set[str], set[str], list[str], list[str]]:
    variants = [str(row["id"]) for row in prereg["variants"]["definitions"]]
    windows = [name for name, _, _ in runner.registered_windows(prereg)]
    costs = [str(value) for value in prereg["frictions"]["one_way_cost_bps"]]
    taxes = [str(row["id"]) for row in prereg["frictions"]["tax_profiles"]]
    cells = {
        runner._cell_id(variant, window, cadence, cost, tax)
        for variant in variants for window in windows
        for cadence in (runner.QUARTERLY, runner.ANNUAL)
        for cost in costs for tax in taxes
    }
    paths = {
        runner._cell_id(variant, window, "QUARTERLY", "10", "TAXABLE_MID")
        for variant in variants for window in windows
    }
    return cells, paths, variants, windows


def _validate_freeze(document: Mapping[str, Any]) -> None:
    if document.get("gate") != "READY" or document.get("holdout_results_emitted") is not True:
        raise ResultValidationError("input_freeze.json: READY emitted-holdout freeze required")
    if document.get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise ResultValidationError("input_freeze.json: Stage 1 boundary drift")
    receipt_hash = document.get("validation_receipt_sha256")
    if not isinstance(receipt_hash, str) or len(receipt_hash) != 64:
        raise ResultValidationError("input_freeze.json: validation receipt hash missing")
    current = runner.input_freeze()
    emitted = dict(document)
    emitted.pop("validation_receipt_sha256", None)
    emitted["holdout_results_emitted"] = False
    if emitted != current:
        raise ResultValidationError("input_freeze.json: current implementation/input mismatch")


def _validate_metrics(document: Mapping[str, Any], expected: set[str]) -> list[dict[str, Any]]:
    _require_identity(document, "metrics.json")
    records = document.get("records")
    if not isinstance(records, list) or document.get("cell_count") != len(expected):
        raise ResultValidationError("metrics.json: wrong cell count")
    if document.get("facts_inference_separation") != "FACTS_ONLY":
        raise ResultValidationError("metrics.json: facts boundary missing")
    prereg = _yaml(gate.PREREG_PATH)
    registered_metrics = {
        str(metric) for group in prereg["metrics"].values()
        if isinstance(group, list) for metric in group
    }
    required_keys = METRIC_IDENTITY | registered_metrics | METRIC_SUPPORT
    found: set[str] = set()
    for index, record in enumerate(records):
        if type(record) is not dict or record.get("FACTS_ONLY") is not True:
            raise ResultValidationError(f"metrics.json[{index}]: FACTS_ONLY required")
        if set(record) != required_keys:
            raise ResultValidationError(f"metrics.json[{index}]: metric field registry mismatch")
        cell = runner._cell_id(
            str(record.get("variant")), str(record.get("window")),
            str(record.get("cadence")), str(record.get("one_way_cost_bps")),
            str(record.get("tax_profile")),
        )
        if cell in found:
            raise ResultValidationError(f"metrics.json: duplicate cell {cell}")
        found.add(cell)
        _assert_finite(record, f"metrics.json[{index}]")
    if found != expected:
        raise ResultValidationError("metrics.json: Cartesian registry mismatch")
    return records


def _validate_paths(document: Mapping[str, Any], expected: set[str]) -> None:
    _require_identity(document, "portfolio_paths.json")
    if document.get("scope") != "DECISION_CELL_ONLY_ALL_REGISTERED_WINDOWS":
        raise ResultValidationError("portfolio_paths.json: scope drift")
    records = document.get("records")
    if not isinstance(records, list):
        raise ResultValidationError("portfolio_paths.json: records required")
    found: set[str] = set()
    for index, record in enumerate(records):
        if type(record) is not dict:
            raise ResultValidationError(f"portfolio_paths.json[{index}]: mapping required")
        if set(record) != PATH_KEYS:
            raise ResultValidationError(f"portfolio_paths.json[{index}]: field registry mismatch")
        cell = record.get("cell_id")
        dates = record.get("dates")
        series = [record.get("index"), record.get("daily_net_returns"),
                  record.get("daily_lagged_dff_returns")]
        if not isinstance(cell, str) or cell in found:
            raise ResultValidationError("portfolio_paths.json: duplicate or missing cell")
        if not isinstance(dates, list) or len(dates) < 2 or dates != sorted(set(dates)):
            raise ResultValidationError(f"portfolio_paths.json[{index}]: invalid dates")
        if any(not isinstance(values, list) or len(values) != len(dates) for values in series):
            raise ResultValidationError(f"portfolio_paths.json[{index}]: unaligned path")
        if any(float(value) <= 0 for value in series[0]):
            raise ResultValidationError(f"portfolio_paths.json[{index}]: nonpositive index")
        _assert_finite(record, f"portfolio_paths.json[{index}]")
        found.add(cell)
    if found != expected:
        raise ResultValidationError("portfolio_paths.json: decision-path registry mismatch")


def _validate_bootstrap(document: Mapping[str, Any], variants: Sequence[str], prereg: Mapping[str, Any]) -> list[dict[str, Any]]:
    _require_identity(document, "bootstrap.json")
    if document.get("method") != prereg["bootstrap"]["method"]:
        raise ResultValidationError("bootstrap.json: method drift")
    if document.get("facts_inference_separation") != "FACTS_ONLY":
        raise ResultValidationError("bootstrap.json: facts boundary missing")
    records = document.get("records")
    expected = {(window, variant) for window in prereg["bootstrap"]["windows"]
                for variant in variants if variant != "BASELINE"}
    if not isinstance(records, list) or len(records) != len(expected):
        raise ResultValidationError("bootstrap.json: record count mismatch")
    found: set[tuple[str, str]] = set()
    for index, record in enumerate(records):
        key = (str(record.get("window")), str(record.get("variant")))
        if key in found or record.get("resamples") != int(prereg["bootstrap"]["resamples"]):
            raise ResultValidationError(f"bootstrap.json[{index}]: identity or resample mismatch")
        for statistic in BOOTSTRAP_STATS:
            values = record.get(statistic)
            if type(values) is not dict or not 0 <= float(values.get("probability_positive", -1)) <= 1:
                raise ResultValidationError(f"bootstrap.json[{index}]: invalid {statistic}")
        _assert_finite(record, f"bootstrap.json[{index}]")
        found.add(key)
    if found != expected:
        raise ResultValidationError("bootstrap.json: registry mismatch")
    return records


def _validate_sensitivity(document: Mapping[str, Any], variants: Sequence[str], windows: Sequence[str], prereg: Mapping[str, Any]) -> None:
    _require_identity(document, "sensitivity_matrix.json")
    if document.get("facts_inference_separation") != "FACTS_ONLY":
        raise ResultValidationError("sensitivity_matrix.json: facts boundary missing")
    rows = document.get("rows")
    expected = {
        (window, variant, cadence, str(cost), str(tax["id"]))
        for window in windows for variant in variants if variant != "BASELINE"
        for cadence in (runner.QUARTERLY, runner.ANNUAL)
        for cost in prereg["frictions"]["one_way_cost_bps"]
        for tax in prereg["frictions"]["tax_profiles"]
    }
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ResultValidationError("sensitivity_matrix.json: record count mismatch")
    found: set[tuple[str, str, str, str, str]] = set()
    for index, row in enumerate(rows):
        key = (str(row.get("window")), str(row.get("variant")), str(row.get("cadence")),
               str(row.get("one_way_cost_bps")), str(row.get("tax_profile")))
        if key in found:
            raise ResultValidationError("sensitivity_matrix.json: duplicate cell")
        _assert_finite(row, f"sensitivity_matrix.json[{index}]")
        found.add(key)
    if found != expected:
        raise ResultValidationError("sensitivity_matrix.json: registry mismatch")


def validate(root: Path) -> dict[str, Any]:
    if not root.is_dir() or {path.name for path in root.iterdir()} != REQUIRED:
        raise ResultValidationError("result directory must contain exactly the registered outputs")
    manifest = _json(root / "output_manifest.json")
    _validate_manifest(root, manifest)
    freeze = _json(root / "input_freeze.json")
    _validate_freeze(freeze)
    prereg = _yaml(gate.PREREG_PATH)
    expected_cells, expected_paths, variants, windows = _expected_registry(prereg)
    metrics = _validate_metrics(_json(root / "metrics.json"), expected_cells)
    _validate_paths(_json(root / "portfolio_paths.json"), expected_paths)
    bootstraps = _validate_bootstrap(_json(root / "bootstrap.json"), variants, prereg)
    sensitivity = _json(root / "sensitivity_matrix.json")
    _validate_sensitivity(sensitivity, variants, windows, prereg)
    disposition = _yaml(root / "disposition.yaml")
    _require_identity(disposition, "disposition.yaml")
    if disposition.get("disposition") not in prereg["review_thresholds"]["disposition_values"]:
        raise ResultValidationError("disposition.yaml: unregistered disposition")
    if disposition.get("automatic_adoption") != "PROHIBITED" or disposition.get("targets_changed") is not False:
        raise ResultValidationError("disposition.yaml: policy boundary drift")
    if disposition.get("advisory_only") is not True or disposition.get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise ResultValidationError("disposition.yaml: advisory or Stage 1 boundary drift")
    config = runner.load_config()
    market = runner.load_market_data(freeze, config)
    recomputed = runner.decide(metrics, sensitivity, bootstraps, prereg, config, market)
    if disposition != recomputed:
        raise ResultValidationError("disposition.yaml: decision does not reproduce from facts")
    limitations = (root / "limitations.md").read_text(encoding="utf-8")
    results = (root / "results.md").read_text(encoding="utf-8")
    for name, text in (("limitations.md", limitations), ("results.md", results)):
        if STUDY_ID not in text or "UNARMED" not in text or "NOT EXECUTABLE" not in text:
            raise ResultValidationError(f"{name}: required identity/boundary missing")
    return {
        "status": "PASS", "study_id": STUDY_ID,
        "metric_cells": len(expected_cells), "decision_paths": len(expected_paths),
        "bootstrap_records": len(bootstraps), "sensitivity_records": len(sensitivity["rows"]),
        "disposition": disposition["disposition"],
        "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result_dir", type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(validate(args.result_dir), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
