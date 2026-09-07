"""Integrity checks for the retained PORTFOLIO-ROBUSTNESS-0001 evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "research/whole_portfolio_robustness"
RESULTS = STUDY / "execution"
VALIDATION = STUDY / "validation"
EXECUTION_COMMIT = "1ce41d0efce16139f24de783df0e994d9a7c7853"
OUTPUT_MANIFEST_SHA256 = (
    "d81b892b28219f6bd930eb65336bbb3cffb692d0903355d2c21a31377edfafff"
)
NON_HOLDOUT_RECEIPT_SHA256 = (
    "a11e4536d38fc3c5870c1b898c0d4984c6ba90689c15e3b223d6202179d2786d"
)
SOL_ACQUISITION_RECEIPT_SHA256 = (
    "d6ee9c6f6f8a00dff6b9cc50fa99ef369e35c7b99e670bb9c17b21a7963e6ede"
)
RETENTION_RECEIPT_SHA256 = (
    "17e25d403b0f95c61801d917c8253147c6774a1181e4ef35cef34d94037514a8"
)
REGISTERED_OUTPUTS = {
    "bootstrap.json",
    "disposition.yaml",
    "input_freeze.json",
    "limitations.md",
    "metrics.json",
    "output_manifest.json",
    "portfolio_paths.json",
    "results.md",
    "sensitivity_matrix.json",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_retained_result_manifest_is_complete_and_exact() -> None:
    assert {path.name for path in RESULTS.iterdir()} == REGISTERED_OUTPUTS
    assert _sha256(RESULTS / "output_manifest.json") == OUTPUT_MANIFEST_SHA256
    manifest = _json(RESULTS / "output_manifest.json")
    assert set(manifest["files"]) == REGISTERED_OUTPUTS - {"output_manifest.json"}
    for name, expected in manifest["files"].items():
        assert _sha256(RESULTS / name) == expected
    assert manifest["advisory_only"] is True
    assert manifest["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"


def test_retained_disposition_preserves_policy_boundaries() -> None:
    disposition = _yaml(RESULTS / "disposition.yaml")
    freeze = _json(RESULTS / "input_freeze.json")
    metrics = _json(RESULTS / "metrics.json")
    sensitivity = _json(RESULTS / "sensitivity_matrix.json")
    bootstrap = _json(RESULTS / "bootstrap.json")

    assert disposition["disposition"] == "RETAIN_BASELINE"
    assert disposition["passing_variants"] == []
    assert disposition["automatic_adoption"] == "PROHIBITED"
    assert disposition["targets_changed"] is False
    assert disposition["advisory_only"] is True
    assert disposition["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"
    assert freeze["code_commit"] == EXECUTION_COMMIT
    assert freeze["holdout_results_emitted"] is True
    assert metrics["cell_count"] == 1728
    assert len(sensitivity["rows"]) == 1440
    assert len(bootstrap["records"]) == 10
    assert "**RETAIN_BASELINE**" in (RESULTS / "results.md").read_text(encoding="utf-8")


def test_retained_validation_and_acquisition_receipts_bind_the_run() -> None:
    freeze = _json(RESULTS / "input_freeze.json")
    validation = _json(VALIDATION / "non_holdout_validation_receipt.json")
    acquisition = _json(VALIDATION / "sol_acquisition_receipt.json")
    retention = _yaml(VALIDATION / "retention_receipt.yaml")

    assert (
        _sha256(VALIDATION / "non_holdout_validation_receipt.json")
        == NON_HOLDOUT_RECEIPT_SHA256
        == freeze["validation_receipt_sha256"]
    )
    assert (
        _sha256(VALIDATION / "sol_acquisition_receipt.json")
        == SOL_ACQUISITION_RECEIPT_SHA256
    )
    assert (
        _sha256(VALIDATION / "retention_receipt.yaml")
        == RETENTION_RECEIPT_SHA256
    )
    assert validation["status"] == "PASS"
    assert validation["phase"] == "NON_HOLDOUT_VALIDATION"
    assert validation["validation_case_count"] == 54
    assert validation["max_market_date_used"] == "2023-12-29"
    assert validation["input_freeze"]["code_commit"] == EXECUTION_COMMIT
    assert validation["holdout_results_emitted"] is False
    assert acquisition["hash_match"] is True
    assert acquisition["coverage_identity_match"] is True
    assert acquisition["no_registered_results_executed"] is True
    assert acquisition["actual_sha256"] == acquisition["expected_sha256"]
    assert acquisition["actual_sha256"] == freeze["datasets"]["SOL"]["sha256"]
    assert retention["execution_commit"] == EXECUTION_COMMIT
    assert retention["workflow_validation"] == "PASS"
    assert retention["independent_reproduction"]["status"] == "PASS"
    assert retention["disposition"] == "RETAIN_BASELINE"
    assert retention["targets_changed"] is False
    assert retention["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"
