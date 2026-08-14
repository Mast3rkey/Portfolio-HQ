"""Build the network-free RISK-0001 attempt-2 preexecution integrity record.

This module verifies and attests frozen artifacts only.  It has no study-cell
execution entry point and does not import the acquisition implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path
from typing import Any, Iterable, Mapping

import level1_sleeve_robustness_preregistration_validator as authority
import risk_level1_core as core
import risk_level1_data_manifest_validator as manifest_validator


RISK_0002_PATH = core.ROOT / "governance/decisions/RISK-0002-separately-authorized-integrity-reexecution-amendment.md"
RISK_0002_SHA256 = "4e6d787bc4c139c2665a75480ec7f3690e5f26c21f458feb1f0af84027b2a6d9"
RISK_0002_ACCEPTED_HEAD = "cc6248fed90d6f3899fbbaa68236fe306efce1d9"
RISK_0002_MERGE = "e4d9fd69467755b7aa974c39dcb107e388910c52"
ATTEMPT_1_FREEZE_SHA256 = "e6a14574e743827c35a0ed99ea3aa186d30125217eb1d121978ee0fb738a05c5"
ATTEMPT_1_RECEIPT_SHA256 = "49f8333bc3cc8d31dfc07b5d8aafe342b5b84f59167a881f6d4468bdcb32c047"
ATTEMPT_1_DEFECT_SHA256 = "cb2c306f96104998efff338fb5ef52f095b9feab0e0ed5c1aa96c95b4c55f1b9"

FROZEN_HASHES = {
    "material_aggregate": "bee2e34fc438d92b51811f756e16a7f474229a4b985114190c3655c1c3c3c63f",
    "raw": "76b9a429d15280b9b16624e66cc80129d2a7359cb12bcc948ed126ad2c19bfb7",
    "receipts": "abf6f603d71f388288a4c3e691e810f683f36fbec2c5d696ef9448551a677ce7",
    "transformed": "955f3cd5a61aa465697b1b128b102114ab97ade549cc3f0196194d1049aec605",
    "quarantine": "17a8cced2e0886165f17d3b2d76844b167b8a02cf1b0b0c1891c315eac2df467",
    "protocol": "90277ad4767e4766d7a38c1199affde66f44e55ff16fd7f73e0894380cf8a425",
    "preregistration": "8da1697456e8a8f4a168c99ae8387c77cd023e0e615cf51c78110165223d3c5a",
    "implementation_config": "9f97162260ca97ef340b56811d8d91009235922cddf478ff39be7270614301de",
    "eligibility": "3854e9203c6b282e3d7c398b19a8f35de6cdad1c291b06456af19fa4d47ed680",
    "trial_registry": "8942227dfba3a4fff6b1b94067ad252f0890cfa0959e2939e25ef98036904f51",
}

ATTEMPT_1_IMPLEMENTATION_HASHES = {
    "risk_level1_acquisition.py": "ba35770c1b44e6d21cfde241d006d9b0708de4446c9cbbfdc1bd81ec184a25ef",
    "risk_level1_core.py": "a303542dae27b07d0a13b43f327a3b7038446f5ddeef0172e0f1e47b5097d8c1",
    "risk_level1_data_manifest_validator.py": "ed5f21adefda9cec6d631121806aa45814ff7a603871c6da258625c04886602e",
    "risk_level1_result_validator.py": "57fa533c2707105566ded9d62e1d11d75ac0229c3937241b089bce8bcf6b7a46",
    "risk_level1_runner.py": "4475701eac8c9769fc8dbe05b664941f93ae33d471d6ef7eed6a78663cad3e2e",
    "test_risk_level1_implementation.py": "af297f7ad5f37e47b79d93255f64b16794d8ba9c15a820e2a0769506ff42199e",
    "requirements.txt": "42ec81c69cc7e5569b719f1dc0ed1acd001a7b006a3c59e7888e840b6b76015d",
}

GOLD_PEER_KEYS = (
    "peer_id",
    "identity_and_inception",
    "unresolved_required_session_gaps",
    "dividend_split_action_treatment",
    "overlap_total_return_correlation",
    "overlap_annualized_return_difference_pp",
    "overlap_max_drawdown_difference_pp",
)

IMPLEMENTATION_FILES = (
    "risk_level1_acquisition.py",
    "risk_level1_attempt2_attestation.py",
    "risk_level1_core.py",
    "risk_level1_data_manifest_validator.py",
    "risk_level1_result_validator.py",
    "risk_level1_runner.py",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise core.IntegrityError(message)


def _files(path: Path) -> list[Path]:
    return sorted((item for item in path.rglob("*") if item.is_file()), key=str)


def _aggregate(root: Path, files: Iterable[Path]) -> tuple[str, int]:
    ordered = sorted(files, key=lambda path: path.relative_to(root).as_posix())
    rows = "".join(
        f"{core.sha256_file(path)}  {path.relative_to(root).as_posix()}\n"
        for path in ordered
    )
    return hashlib.sha256(rows.encode("utf-8")).hexdigest(), len(ordered)


def _forensic_material_files(root: Path) -> list[Path]:
    study = root / "research/level1_sleeve_robustness"
    excluded = {study / "PROTOCOL_V1.md", study / "pre_registration.yaml"}
    material = [path for path in _files(study) if path not in excluded]
    material.extend(root / name for name in ATTEMPT_1_IMPLEMENTATION_HASHES)
    return material


def _assert_risk_0002_effective() -> None:
    _require(core.sha256_file(RISK_0002_PATH) == RISK_0002_SHA256, "RISK-0002 authority hash mismatch")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", RISK_0002_MERGE, "HEAD"],
        cwd=core.ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _require(result.returncode == 0, "RISK-0002 merge is not an ancestor of the implementation head")


def _assert_no_execution_artifacts() -> None:
    forbidden = {
        "execution_receipt.json", "raw_evidence.json", "cell_results.json",
        "disposition.json", "diagnostics.json", "RESULTS.md",
        "LIMITATIONS_AND_SURVIVORSHIP.md",
    }
    found = [path for path in _files(core.ATTEMPT_2) if path.name in forbidden]
    _require(not found, f"attempt-2 execution/result artifact exists: {found}")
    _require(not core.RESULTS.exists(), "attempt-2 result namespace must not exist before review")


def _verify_forensic_source(forensic_root: Path) -> dict[str, Any]:
    _require(forensic_root.is_dir(), f"forensic root missing: {forensic_root}")
    material_hash, material_count = _aggregate(forensic_root, _forensic_material_files(forensic_root))
    _require(material_count == 1244, f"forensic material file count {material_count} != 1244")
    _require(material_hash == FROZEN_HASHES["material_aggregate"], "forensic material aggregate mismatch")
    scopes: dict[str, Any] = {}
    for name in ("raw", "receipts", "transformed", "quarantine"):
        scope_hash, count = _aggregate(
            forensic_root,
            _files(forensic_root / "research/level1_sleeve_robustness/data" / name),
        )
        _require(scope_hash == FROZEN_HASHES[name], f"forensic {name} aggregate mismatch")
        scopes[name] = {"file_count": count, "aggregate_sha256": scope_hash}
    for name, expected in ATTEMPT_1_IMPLEMENTATION_HASHES.items():
        _require(core.sha256_file(forensic_root / name) == expected, f"forensic implementation mismatch: {name}")
    return {
        "forensic_root": str(forensic_root),
        "material_file_count": material_count,
        "material_aggregate_sha256": material_hash,
        "scopes": scopes,
    }


def _transplant_pairs(forensic_root: Path) -> list[tuple[Path, Path, str]]:
    pairs: list[tuple[Path, Path, str]] = []
    source_data = forensic_root / "research/level1_sleeve_robustness/data"
    for source in _files(source_data):
        relative = source.relative_to(forensic_root)
        pairs.append((source, core.ROOT / relative, "LOCAL_QUARANTINED" if "quarantine" in relative.parts else "FROZEN_DATA"))
    for relative_text in (
        "requirements.txt",
        "risk_level1_acquisition.py",
        "risk_level1_data_manifest_validator.py",
        "risk_level1_result_validator.py",
        "research/level1_sleeve_robustness/data_manifest.yaml",
        "research/level1_sleeve_robustness/implementation_config.yaml",
        "research/level1_sleeve_robustness/eligibility_matrix.json",
        "research/level1_sleeve_robustness/trial_registry.json",
    ):
        relative = Path(relative_text)
        pairs.append((forensic_root / relative, core.ROOT / relative, "FROZEN_TRACKED"))
    historical = (
        ("research/level1_sleeve_robustness/data_gate_freeze.json", "data_gate_freeze.json"),
        ("research/level1_sleeve_robustness/results/execution_receipt.json", "execution_receipt.json"),
        ("research/level1_sleeve_robustness/results/execution_defect.json", "execution_defect.json"),
    )
    for source_text, destination_name in historical:
        pairs.append((forensic_root / source_text, core.ATTEMPT_1 / destination_name, "HISTORICAL_ATTEMPT_1"))
    return pairs


def _write_transplant_manifest(forensic_root: Path, generated_at_utc: str) -> dict[str, Any]:
    records = []
    for source, destination, disposition in _transplant_pairs(forensic_root):
        _require(source.is_file(), f"transplant source missing: {source}")
        _require(destination.is_file(), f"transplant destination missing: {destination}")
        source_hash = core.sha256_file(source)
        destination_hash = core.sha256_file(destination)
        _require(source_hash == destination_hash, f"transplant byte mismatch: {destination}")
        records.append({
            "source_relative_path": source.relative_to(forensic_root).as_posix(),
            "destination_relative_path": destination.relative_to(core.ROOT).as_posix(),
            "sha256": source_hash,
            "disposition": disposition,
        })
    manifest = {
        "schema_version": "1.0",
        "study_id": "RISK-0001",
        "attempt_id": core.ATTEMPT_2_ID,
        "generated_at_utc": generated_at_utc,
        "record_count": len(records),
        "records": records,
    }
    core.write_schema_json(core.ATTEMPT_2_TRANSPLANT_MANIFEST_PATH, manifest)
    return manifest


def _verify_frozen_repository_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    paths = {
        "protocol": core.PROTOCOL_PATH,
        "preregistration": core.PREREG_PATH,
        "implementation_config": core.CONFIG_PATH,
        "eligibility": core.ELIGIBILITY_PATH,
        "trial_registry": core.TRIAL_REGISTRY_PATH,
    }
    for name, path in paths.items():
        _require(core.sha256_file(path) == FROZEN_HASHES[name], f"frozen {name} hash mismatch")
    validation = authority.validate_repository()
    _require(not validation.errors, "RISK authority invalid: " + "; ".join(validation.errors))
    manifest_errors = manifest_validator.validate_manifest(require_local_quarantine=True)
    _require(not manifest_errors, "frozen manifest invalid: " + "; ".join(manifest_errors))

    prereg = core.load_yaml(core.PREREG_PATH)
    eligibility = core.load_schema_json(core.ELIGIBILITY_PATH)
    registry = core.load_schema_json(core.TRIAL_REGISTRY_PATH)
    _require(eligibility["registered_cell_count"] == 777 and len(eligibility["records"]) == 777, "eligibility is not exact 777")
    _require(registry["registered_cell_count"] == 777 and len(registry["records"]) == 777, "trial registry is not exact 777")
    _require(registry["reserve_trials"] == 0 and registry["unused_capacity_reuse"] == "PROHIBITED", "trial capacity drift")
    eligibility_ids = [
        (row["representation_id"], row["scenario_id"], row["window_id"])
        for row in eligibility["records"]
    ]
    registry_ids = [
        (row["representation_id"], row["scenario_id"], row["window_id"])
        for row in registry["records"]
    ]
    _require(len(set(eligibility_ids)) == 777, "eligibility cell identities are not unique")
    _require(len(set(row["cell_id"] for row in registry["records"])) == 777, "trial cell IDs are not unique")
    _require(eligibility_ids == registry_ids, "eligibility/trial identity order or content drift")
    return prereg, eligibility, registry


def _verify_provider_identity(prereg: Mapping[str, Any]) -> dict[str, Any]:
    source = core.load_schema_json(core.SOURCE_INVENTORY_PATH)
    manifest = core.load_yaml(core.MANIFEST_PATH)
    _require(manifest["provider_fallback_hierarchy"] == prereg["fallback_order"], "provider fallback hierarchy drift")
    source_rows = list(source["stock_and_etf_datasets"]) + list(source["crypto_datasets"])
    manifest_by_instrument = {
        row["instrument_identity"]: row
        for row in manifest["datasets"]
        if row["instrument_identity"] != "DFF"
    }
    selections = []
    for row in source_rows:
        instrument = row["instrument"]
        _require(instrument in manifest_by_instrument, f"manifest provider row missing: {instrument}")
        _require(row["selected_provider"] == manifest_by_instrument[instrument]["provider"], f"provider drift: {instrument}")
        _require(row["selected_transformed_sha256"] == manifest_by_instrument[instrument]["transformed_sha256"], f"transformed identity drift: {instrument}")
        selections.append({"instrument": instrument, "selected_provider": row["selected_provider"]})
    comparator = source["comparator_dataset"]
    _require(comparator["selected_provider"] == next(row for row in manifest["datasets"] if row["instrument_identity"] == "DFF")["provider"], "DFF provider drift")
    return {
        "fallback_hierarchy_sha256": core.canonical_hash(prereg["fallback_order"]),
        "provider_selection_sha256": core.canonical_hash(selections),
        "provider_selection_count": len(selections) + 1,
    }


def _correct_gold_evidence(historical: Mapping[str, Any], prereg: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    original = historical["gold_peer_evidence"]
    corrected = []
    for index, record in enumerate(original):
        _require(type(record) is dict and set(record) == set(GOLD_PEER_KEYS), f"historical gold evidence schema mismatch at {index}")
        corrected.append({key: record[key] for key in GOLD_PEER_KEYS})
    _require(core.canonical_hash(original) == core.canonical_hash(corrected), "gold evidence semantic values changed")
    admitted = authority._admitted_gold_peers(prereg, corrected)
    _require(tuple(historical["admitted_gold_peers"]) == admitted, "gold admission result changed")
    round_trip = core.load_schema_json_bytes(core.schema_json_bytes({"gold_peer_evidence": corrected}))
    _require(tuple(round_trip["gold_peer_evidence"][0]) == GOLD_PEER_KEYS, "corrected gold evidence order did not round trip")
    return corrected, {
        "semantic_canonical_sha256": core.canonical_hash(corrected),
        "ordered_schema_sha256": core.sha256_bytes(core.schema_json_bytes(corrected)),
        "admitted_gold_peers": list(admitted),
    }


def build_attestation(forensic_root: Path, generated_at_utc: str, focused_test_command: str) -> None:
    _assert_no_execution_artifacts()
    _assert_risk_0002_effective()
    forensic = _verify_forensic_source(forensic_root)
    prereg, eligibility, registry = _verify_frozen_repository_inputs()
    provider_identity = _verify_provider_identity(prereg)
    transplant = _write_transplant_manifest(forensic_root, generated_at_utc)

    historical = core.load_schema_json(core.ATTEMPT_1_FREEZE_PATH)
    _require(core.sha256_file(core.ATTEMPT_1_FREEZE_PATH) == ATTEMPT_1_FREEZE_SHA256, "attempt-1 freeze hash mismatch")
    _require(core.sha256_file(core.ATTEMPT_1 / "execution_receipt.json") == ATTEMPT_1_RECEIPT_SHA256, "attempt-1 receipt hash mismatch")
    _require(core.sha256_file(core.ATTEMPT_1 / "execution_defect.json") == ATTEMPT_1_DEFECT_SHA256, "attempt-1 defect hash mismatch")
    corrected_gold, gold_identity = _correct_gold_evidence(historical, prereg)

    implementation_hashes = {
        name: core.sha256_file(core.ROOT / name) for name in IMPLEMENTATION_FILES
    }
    focused_test_hash = core.sha256_file(core.ROOT / "test_risk_level1_implementation.py")
    attestation = {
        "schema_version": "2.0",
        "study_id": "RISK-0001",
        "attempt_id": core.ATTEMPT_2_ID,
        "generated_at_utc": generated_at_utc,
        "status": "PREEXECUTION_REVIEW_REQUIRED",
        "authority": {
            "decision_id": "RISK-0002",
            "decision_sha256": RISK_0002_SHA256,
            "accepted_head": RISK_0002_ACCEPTED_HEAD,
            "merge_commit": RISK_0002_MERGE,
            "merged_and_effective": True,
        },
        "stage_a": {
            "status": "PASS",
            "attestation_scope": "PREEXECUTION_SELF_ATTESTATION_ONLY",
            "gates": list(prereg["data_gate"]["GLOBAL_STUDY_INTEGRITY"]["gates"]),
            "next_gate": "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD_REVIEW",
        },
        "authority_hashes": {
            "protocol": core.sha256_file(core.PROTOCOL_PATH),
            "preregistration": core.sha256_file(core.PREREG_PATH),
        },
        "implementation_config_sha256": core.sha256_file(core.CONFIG_PATH),
        "implementation_code_hashes": implementation_hashes,
        "corrected_code_bundle_sha256": core.canonical_hash(implementation_hashes),
        "focused_test": {
            "path": "test_risk_level1_implementation.py",
            "sha256": focused_test_hash,
            "command": focused_test_command,
            "result": "PASS",
            "fixture_only": True,
        },
        "attempt_1_historical_evidence": {
            "attempt_id": core.ATTEMPT_1_ID,
            "data_gate_freeze_sha256": ATTEMPT_1_FREEZE_SHA256,
            "execution_receipt_sha256": ATTEMPT_1_RECEIPT_SHA256,
            "execution_defect_sha256": ATTEMPT_1_DEFECT_SHA256,
            "retained_immutable": True,
        },
        "forensic_identity": forensic,
        "frozen_input_aggregates": {key: FROZEN_HASHES[key] for key in ("raw", "receipts", "transformed", "quarantine")},
        "transplant_manifest": {
            "path": core.ATTEMPT_2_TRANSPLANT_MANIFEST_PATH.relative_to(core.ROOT).as_posix(),
            "sha256": core.sha256_file(core.ATTEMPT_2_TRANSPLANT_MANIFEST_PATH),
            "record_count": transplant["record_count"],
            "source_and_destination_sha256_equal": True,
        },
        "source_inventory_sha256": historical["source_inventory_sha256"],
        "manifest_sha256": historical["manifest_sha256"],
        "acquisition_receipt_inventory_sha256": historical["acquisition_receipt_inventory_sha256"],
        "acquisition_receipt_count": historical["acquisition_receipt_count"],
        "failed_acquisition_attempt_count": historical["failed_acquisition_attempt_count"],
        "calendar_sha256": historical["calendar_sha256"],
        "eligibility_matrix_sha256": core.sha256_file(core.ELIGIBILITY_PATH),
        "trial_registry_sha256": core.sha256_file(core.TRIAL_REGISTRY_PATH),
        "registered_cell_count": len(registry["records"]),
        "registered_cell_identity_sha256": core.canonical_hash([row["cell_id"] for row in registry["records"]]),
        "eligibility_identity_sha256": core.canonical_hash(eligibility["records"]),
        "provider_fallback_identity": provider_identity,
        "gold_peer_evidence_integrity": gold_identity,
        "gold_peer_evidence": corrected_gold,
        "admitted_gold_peers": list(historical["admitted_gold_peers"]),
        "integrity_correction": {
            "scope": "ORDER_SENSITIVE_SCHEMA_JSON_PERSISTENCE_ONLY",
            "schema_serializer": "INSERTION_ORDER_PRESERVING_DETERMINISTIC_JSON",
            "schema_loader": "INSERTION_ORDER_PRESERVING_DUPLICATE_KEY_REJECTING_JSON",
            "canonical_hash_serializer": "SORT_KEYS_TRUE_UNCHANGED",
            "semantic_or_numeric_change": False,
        },
        "drift_confirmations": {
            "no_reacquisition": True,
            "no_provider_or_fallback_drift": True,
            "no_config_drift": True,
            "no_protocol_or_preregistration_drift": True,
            "no_eligibility_or_missingness_drift": True,
            "no_trial_registry_drift": True,
            "no_scenario_window_metric_threshold_formula_or_result_rule_drift": True,
        },
        "network_after_freeze": "PROHIBITED",
        "registered_cells_executed": 0,
        "execution_marker_created": False,
        "result_artifacts_created": False,
        "attempt_authorization_consumed": False,
        "execution_permitted": False,
        "ready_for": "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD_REVIEW_ONLY",
    }
    core.write_schema_json(core.ATTEMPT_2_STAGE_A_PATH, attestation)
    metadata = {
        "schema_version": "1.0",
        "study_id": "RISK-0001",
        "attempt_id": core.ATTEMPT_2_ID,
        "status": "PREEXECUTION_REVIEW_REQUIRED",
        "authority": "RISK-0002",
        "protocol_sha256": FROZEN_HASHES["protocol"],
        "preregistration_sha256": FROZEN_HASHES["preregistration"],
        "implementation_config_sha256": FROZEN_HASHES["implementation_config"],
        "eligibility_sha256": FROZEN_HASHES["eligibility"],
        "trial_registry_sha256": FROZEN_HASHES["trial_registry"],
        "raw_aggregate_sha256": FROZEN_HASHES["raw"],
        "transformed_aggregate_sha256": FROZEN_HASHES["transformed"],
        "corrected_code_bundle_sha256": attestation["corrected_code_bundle_sha256"],
        "focused_test_sha256": focused_test_hash,
        "stage_a_attestation_sha256": core.sha256_file(core.ATTEMPT_2_STAGE_A_PATH),
        "registered_cells_executed": 0,
        "execution_marker_created": False,
        "attempt_authorization_consumed": False,
    }
    core.write_schema_json(core.ATTEMPT_2_METADATA_PATH, metadata)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--forensic-root", type=Path, required=True)
    parser.add_argument("--generated-at-utc", required=True)
    parser.add_argument("--focused-test-command", required=True)
    args = parser.parse_args()
    build_attestation(args.forensic_root.resolve(), args.generated_at_utc, args.focused_test_command)
    print(f"attempt-2 Stage-A attestation: {core.ATTEMPT_2_STAGE_A_PATH}")
    print("registered RISK cells executed: 0")
    print("attempt-2 authorization consumed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
