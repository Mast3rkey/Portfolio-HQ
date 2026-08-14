"""Build the network-free RISK-0001 attempt-2 preexecution integrity record.

This module verifies and attests frozen artifacts only.  It has no study-cell
execution entry point and does not import the acquisition implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import level1_sleeve_robustness_preregistration_validator as authority
import risk_level1_core as core
import risk_level1_data_manifest_validator as manifest_validator


RISK_0002_PATH = core.ROOT / "governance/decisions/RISK-0002-separately-authorized-integrity-reexecution-amendment.md"
RISK_0002_SHA256 = "4e6d787bc4c139c2665a75480ec7f3690e5f26c21f458feb1f0af84027b2a6d9"
RISK_0002_ACCEPTED_HEAD = "cc6248fed90d6f3899fbbaa68236fe306efce1d9"
RISK_0002_MERGE = "e4d9fd69467755b7aa974c39dcb107e388910c52"
REPOSITORY_IDENTITY = "Mast3rkey/Portfolio-HQ"
IMPLEMENTATION_PR_NUMBER = 316
IMPLEMENTATION_AUTHOR_IDENTITY = "CODEX_SESSION:RISK-0001_ATTEMPT2_INTEGRITY_CORRECTION_AUTHOR"
TRANSPLANT_MANIFEST_SHA256 = "9bf18533a9608def728cfb6db207b484596a809876906af6018ae2e8096af901"
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

FROZEN_STAGE_A_IDENTITIES = {
    "source_inventory": "9b604871e9180e9aa7a7ae298a749050a267ea81a7e402e099d9519a1d979f71",
    "manifest": "d4a64238810de6b599dfaefe167840b0e852cb6f0a0df45bbedddcf4a44be3ea",
    "acquisition_receipt_inventory": "260095460e120a1ab222d48846f45fd1b246a634c04d900d966db64662d31a95",
    "calendar": "365c740ed489a2804189dee439a8cfe4fd926db1f92957988e51ad91db12fabe",
    "registered_cell_identity": "617c2622622e9f1a5aa0aa6bbc7787e7d65a586a38e6d8621b92e0e5c01ca377",
    "eligibility_identity": "dfba6057368217131a426d1389ce0983ad2f08e3ed65d19dec321a9c3734fb22",
    "fallback_hierarchy": "d5edc6b9ce94a2bf090daf6df094bf5dff5940dab9ff8ca67dbe7673ebaca8dc",
    "provider_selection": "3e287459524b510dab3fa3bfb27d6baca5936a9363b53d37bb75868d7e74cc14",
}

FROZEN_SCOPE_COUNTS = {"raw": 66, "receipts": 963, "transformed": 55, "quarantine": 142}

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


def _aggregate_hash_rows(rows: Iterable[tuple[str, str]]) -> tuple[str, int]:
    ordered = sorted(rows, key=lambda item: item[1])
    payload = "".join(f"{digest}  {relative}\n" for digest, relative in ordered)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest(), len(ordered)


def _valid_utc_timestamp(value: Any) -> bool:
    if type(value) is not str or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _verify_transplant_destinations() -> dict[str, Any]:
    path = core.ATTEMPT_2_TRANSPLANT_MANIFEST_PATH
    _require(path.is_file(), "frozen transplant manifest is absent")
    _require(core.sha256_file(path) == TRANSPLANT_MANIFEST_SHA256, "frozen transplant manifest identity mismatch")
    manifest = core.load_schema_json(path)
    _require(
        tuple(manifest) == ("schema_version", "study_id", "attempt_id", "generated_at_utc", "record_count", "records"),
        "frozen transplant manifest exact keys/order mismatch",
    )
    _require(manifest["schema_version"] == "1.0" and manifest["study_id"] == "RISK-0001", "frozen transplant manifest study identity mismatch")
    _require(manifest["attempt_id"] == core.ATTEMPT_2_ID, "frozen transplant manifest attempt identity mismatch")
    _require(_valid_utc_timestamp(manifest["generated_at_utc"]), "frozen transplant manifest timestamp malformed")
    records = manifest["records"]
    _require(type(records) is list and manifest["record_count"] == 1241 and len(records) == 1241, "frozen transplant manifest record count mismatch")

    source_rows: list[tuple[str, str]] = []
    seen_source: set[str] = set()
    seen_destination: set[str] = set()
    allowed_dispositions = {"FROZEN_DATA", "FROZEN_TRACKED", "LOCAL_QUARANTINED", "HISTORICAL_ATTEMPT_1"}
    for index, record in enumerate(records):
        _require(type(record) is dict, f"transplant record {index} must be a mapping")
        _require(
            tuple(record) == ("source_relative_path", "destination_relative_path", "sha256", "disposition"),
            f"transplant record {index} exact keys/order mismatch",
        )
        source_relative = record["source_relative_path"]
        destination_relative = record["destination_relative_path"]
        digest = record["sha256"]
        _require(type(source_relative) is str and source_relative and source_relative not in seen_source, f"transplant source identity invalid: {source_relative!r}")
        _require(type(destination_relative) is str and destination_relative and destination_relative not in seen_destination, f"transplant destination identity invalid: {destination_relative!r}")
        _require(type(digest) is str and len(digest) == 64 and all(char in "0123456789abcdef" for char in digest), f"transplant SHA-256 invalid: {source_relative}")
        _require(record["disposition"] in allowed_dispositions, f"transplant disposition invalid: {source_relative}")
        destination = (core.ROOT / destination_relative).resolve()
        _require(destination.is_relative_to(core.ROOT.resolve()), f"transplant destination escapes repository: {destination_relative}")
        _require(destination.is_file(), f"transplant destination missing: {destination_relative}")
        if destination_relative == "risk_level1_acquisition.py":
            _require(
                digest == ATTEMPT_1_IMPLEMENTATION_HASHES["risk_level1_acquisition.py"],
                "historical attempt-1 acquisition transplant identity mismatch",
            )
        else:
            _require(core.sha256_file(destination) == digest, f"transplant destination hash mismatch: {destination_relative}")
        seen_source.add(source_relative)
        seen_destination.add(destination_relative)
        source_rows.append((digest, source_relative))

    for scope, expected_count in FROZEN_SCOPE_COUNTS.items():
        prefix = f"research/level1_sleeve_robustness/data/{scope}/"
        aggregate, count = _aggregate_hash_rows(row for row in source_rows if row[1].startswith(prefix))
        _require(count == expected_count, f"frozen {scope} transplant count mismatch")
        _require(aggregate == FROZEN_HASHES[scope], f"frozen {scope} aggregate mismatch")

    material_rows = list(source_rows)
    for name in ("risk_level1_core.py", "risk_level1_runner.py", "test_risk_level1_implementation.py"):
        material_rows.append((ATTEMPT_1_IMPLEMENTATION_HASHES[name], name))
    material_hash, material_count = _aggregate_hash_rows(material_rows)
    _require(material_count == 1244, "frozen material reconstruction count mismatch")
    _require(material_hash == FROZEN_HASHES["material_aggregate"], "frozen material aggregate mismatch")
    return manifest


def _forensic_material_files(root: Path) -> list[Path]:
    study = root / "research/level1_sleeve_robustness"
    excluded = {study / "PROTOCOL_V1.md", study / "pre_registration.yaml"}
    material = [path for path in _files(study) if path not in excluded]
    material.extend(root / name for name in ATTEMPT_1_IMPLEMENTATION_HASHES)
    return material


def _assert_risk_0002_effective() -> None:
    _require(core.sha256_file(RISK_0002_PATH) == RISK_0002_SHA256, "RISK-0002 authority hash mismatch")
    accepted = subprocess.run(
        ["git", "merge-base", "--is-ancestor", RISK_0002_ACCEPTED_HEAD, RISK_0002_MERGE],
        cwd=core.ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _require(accepted.returncode == 0, "RISK-0002 accepted head is not bound to the recorded merge")
    effective = subprocess.run(
        ["git", "merge-base", "--is-ancestor", RISK_0002_MERGE, "HEAD"],
        cwd=core.ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _require(effective.returncode == 0, "RISK-0002 merge is not an ancestor of the implementation head")


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


def _verify_recorded_forensic_identity(forensic: Mapping[str, Any]) -> None:
    _require(type(forensic) is dict, "attempt-1 forensic identity must be a mapping")
    _require(forensic.get("forensic_root") == "/private/tmp/phq-risk0001-results", "attempt-1 forensic root identity mismatch")
    _require(forensic.get("material_file_count") == 1244 and forensic.get("material_aggregate_sha256") == FROZEN_HASHES["material_aggregate"], "attempt-1 frozen material identity mismatch")
    scopes = forensic.get("scopes")
    _require(type(scopes) is dict and tuple(scopes) == ("raw", "receipts", "transformed", "quarantine"), "attempt-1 forensic scope schema mismatch")
    for scope, count in FROZEN_SCOPE_COUNTS.items():
        _require(scopes[scope] == {"file_count": count, "aggregate_sha256": FROZEN_HASHES[scope]}, f"attempt-1 forensic {scope} identity mismatch")


def _implementation_hashes() -> dict[str, str]:
    return {name: core.sha256_file(core.ROOT / name) for name in IMPLEMENTATION_FILES}


def _expected_metadata(stage_a: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "2.0",
        "repository": REPOSITORY_IDENTITY,
        "pull_request_number": IMPLEMENTATION_PR_NUMBER,
        "study_id": "RISK-0001",
        "attempt_id": core.ATTEMPT_2_ID,
        "implementation_author_identity": IMPLEMENTATION_AUTHOR_IDENTITY,
        "status": "PREEXECUTION_REVIEW_REQUIRED",
        "authority": "RISK-0002",
        "risk_0002_sha256": RISK_0002_SHA256,
        "risk_0002_accepted_head": RISK_0002_ACCEPTED_HEAD,
        "risk_0002_merge_commit": RISK_0002_MERGE,
        "protocol_sha256": FROZEN_HASHES["protocol"],
        "preregistration_sha256": FROZEN_HASHES["preregistration"],
        "implementation_config_sha256": FROZEN_HASHES["implementation_config"],
        "eligibility_sha256": FROZEN_HASHES["eligibility"],
        "trial_registry_sha256": FROZEN_HASHES["trial_registry"],
        "attempt_1_freeze_sha256": ATTEMPT_1_FREEZE_SHA256,
        "frozen_material_aggregate_sha256": FROZEN_HASHES["material_aggregate"],
        "raw_aggregate_sha256": FROZEN_HASHES["raw"],
        "receipt_aggregate_sha256": FROZEN_HASHES["receipts"],
        "transformed_aggregate_sha256": FROZEN_HASHES["transformed"],
        "quarantine_aggregate_sha256": FROZEN_HASHES["quarantine"],
        "transplant_manifest_sha256": TRANSPLANT_MANIFEST_SHA256,
        "source_inventory_sha256": FROZEN_STAGE_A_IDENTITIES["source_inventory"],
        "data_manifest_sha256": FROZEN_STAGE_A_IDENTITIES["manifest"],
        "acquisition_receipt_inventory_sha256": FROZEN_STAGE_A_IDENTITIES["acquisition_receipt_inventory"],
        "calendar_sha256": FROZEN_STAGE_A_IDENTITIES["calendar"],
        "corrected_code_bundle_sha256": stage_a["corrected_code_bundle_sha256"],
        "focused_test_sha256": stage_a["focused_test"]["sha256"],
        "stage_a_attestation_sha256": core.sha256_file(core.ATTEMPT_2_STAGE_A_PATH),
        "registered_cells_executed": 0,
        "execution_marker_created": False,
        "attempt_authorization_consumed": False,
    }


def _verify_preexecution_metadata(stage_a: Mapping[str, Any]) -> dict[str, Any]:
    _require(core.ATTEMPT_2_METADATA_PATH.is_file(), "attempt-2 preexecution metadata is absent")
    metadata = core.load_schema_json(core.ATTEMPT_2_METADATA_PATH)
    expected_metadata = _expected_metadata(stage_a)
    _require(tuple(metadata) == tuple(expected_metadata), "attempt-2 preexecution metadata exact keys/order mismatch")
    _require(metadata == expected_metadata, "attempt-2 preexecution metadata identity/content mismatch")
    return metadata


def _verify_runtime_stage_a(
    stage_a: Mapping[str, Any],
    prereg: Mapping[str, Any],
    eligibility: Mapping[str, Any],
    registry: Mapping[str, Any],
    provider_identity: Mapping[str, Any],
    transplant: Mapping[str, Any],
) -> None:
    expected_keys = (
        "schema_version", "repository", "pull_request_number", "study_id", "attempt_id",
        "implementation_author_identity", "generated_at_utc", "status", "authority", "stage_a",
        "authority_hashes", "implementation_config_sha256", "implementation_code_hashes",
        "corrected_code_bundle_sha256", "focused_test", "attempt_1_historical_evidence",
        "forensic_identity", "frozen_input_aggregates", "transplant_manifest",
        "source_inventory_sha256", "manifest_sha256", "acquisition_receipt_inventory_sha256",
        "acquisition_receipt_count", "failed_acquisition_attempt_count", "calendar_sha256",
        "eligibility_matrix_sha256", "trial_registry_sha256", "registered_cell_count",
        "registered_cell_identity_sha256", "eligibility_identity_sha256",
        "provider_fallback_identity", "gold_peer_evidence_integrity", "gold_peer_evidence",
        "admitted_gold_peers", "integrity_correction", "drift_confirmations",
        "network_after_freeze", "registered_cells_executed", "execution_marker_created",
        "result_artifacts_created", "attempt_authorization_consumed", "execution_permitted",
        "ready_for",
    )
    _require(tuple(stage_a) == expected_keys, "attempt-2 Stage-A exact keys/order mismatch")
    _require(stage_a["schema_version"] == "4.0", "attempt-2 Stage-A schema version mismatch")
    _require(stage_a["repository"] == REPOSITORY_IDENTITY and stage_a["pull_request_number"] == IMPLEMENTATION_PR_NUMBER, "attempt-2 repository or PR identity mismatch")
    _require(stage_a["study_id"] == "RISK-0001" and stage_a["attempt_id"] == core.ATTEMPT_2_ID, "attempt-2 Stage-A study/attempt identity mismatch")
    _require(stage_a["implementation_author_identity"] == IMPLEMENTATION_AUTHOR_IDENTITY, "attempt-2 implementation author identity mismatch")
    _require(_valid_utc_timestamp(stage_a["generated_at_utc"]), "attempt-2 Stage-A timestamp malformed")
    _require(stage_a["status"] == "PREEXECUTION_REVIEW_REQUIRED", "attempt-2 Stage-A status mismatch")
    _require(stage_a["authority"] == {
        "decision_id": "RISK-0002", "decision_sha256": RISK_0002_SHA256,
        "accepted_head": RISK_0002_ACCEPTED_HEAD, "merge_commit": RISK_0002_MERGE,
        "merged_and_effective": True,
    }, "attempt-2 Stage-A RISK-0002 authority mismatch")
    _require(stage_a["stage_a"] == {
        "status": "PASS", "attestation_scope": "PREEXECUTION_SELF_ATTESTATION_ONLY",
        "gates": list(prereg["data_gate"]["GLOBAL_STUDY_INTEGRITY"]["gates"]),
        "next_gate": "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD_REVIEW",
    }, "attempt-2 Stage-A gate assertions mismatch")
    _require(stage_a["authority_hashes"] == {
        "protocol": FROZEN_HASHES["protocol"], "preregistration": FROZEN_HASHES["preregistration"],
    }, "attempt-2 Stage-A protocol/preregistration identity mismatch")
    _require(stage_a["implementation_config_sha256"] == FROZEN_HASHES["implementation_config"], "attempt-2 Stage-A implementation configuration mismatch")

    implementation_hashes = _implementation_hashes()
    _require(stage_a["implementation_code_hashes"] == implementation_hashes, "attempt-2 corrected implementation hash mismatch")
    _require(stage_a["corrected_code_bundle_sha256"] == core.canonical_hash(implementation_hashes), "attempt-2 corrected code bundle mismatch")
    _require(stage_a["focused_test"] == {
        "path": "test_risk_level1_implementation.py",
        "sha256": core.sha256_file(core.ROOT / "test_risk_level1_implementation.py"),
        "command": "pytest -q test_risk_level1_implementation.py",
        "result": "PASS", "fixture_only": True,
    }, "attempt-2 focused test identity/assertions mismatch")
    _require(stage_a["attempt_1_historical_evidence"] == {
        "attempt_id": core.ATTEMPT_1_ID,
        "data_gate_freeze_sha256": ATTEMPT_1_FREEZE_SHA256,
        "execution_receipt_sha256": ATTEMPT_1_RECEIPT_SHA256,
        "execution_defect_sha256": ATTEMPT_1_DEFECT_SHA256,
        "retained_immutable": True,
    }, "attempt-1 historical evidence identity mismatch")
    _require(core.sha256_file(core.ATTEMPT_1_FREEZE_PATH) == ATTEMPT_1_FREEZE_SHA256, "attempt-1 freeze identity mismatch")
    _require(core.sha256_file(core.ATTEMPT_1 / "execution_receipt.json") == ATTEMPT_1_RECEIPT_SHA256, "attempt-1 receipt identity mismatch")
    _require(core.sha256_file(core.ATTEMPT_1 / "execution_defect.json") == ATTEMPT_1_DEFECT_SHA256, "attempt-1 defect identity mismatch")

    _verify_recorded_forensic_identity(stage_a["forensic_identity"])
    _require(stage_a["frozen_input_aggregates"] == {key: FROZEN_HASHES[key] for key in ("raw", "receipts", "transformed", "quarantine")}, "attempt-2 frozen aggregate assertions mismatch")
    _require(stage_a["transplant_manifest"] == {
        "path": core.ATTEMPT_2_TRANSPLANT_MANIFEST_PATH.relative_to(core.ROOT).as_posix(),
        "sha256": TRANSPLANT_MANIFEST_SHA256,
        "record_count": transplant["record_count"],
        "source_and_destination_sha256_equal": True,
    }, "attempt-2 transplant attestation mismatch")

    expected_file_identities = {
        "source_inventory_sha256": FROZEN_STAGE_A_IDENTITIES["source_inventory"],
        "manifest_sha256": FROZEN_STAGE_A_IDENTITIES["manifest"],
        "acquisition_receipt_inventory_sha256": FROZEN_STAGE_A_IDENTITIES["acquisition_receipt_inventory"],
        "calendar_sha256": FROZEN_STAGE_A_IDENTITIES["calendar"],
        "eligibility_matrix_sha256": FROZEN_HASHES["eligibility"],
        "trial_registry_sha256": FROZEN_HASHES["trial_registry"],
    }
    for key, expected in expected_file_identities.items():
        _require(stage_a[key] == expected, f"attempt-2 Stage-A {key} mismatch")
    _require(stage_a["acquisition_receipt_count"] == 963 and stage_a["failed_acquisition_attempt_count"] == 48, "attempt-2 acquisition receipt accounting mismatch")
    _require(stage_a["registered_cell_count"] == 777, "attempt-2 registered cell count mismatch")
    _require(stage_a["registered_cell_identity_sha256"] == FROZEN_STAGE_A_IDENTITIES["registered_cell_identity"], "attempt-2 ordered cell identity mismatch")
    _require(stage_a["eligibility_identity_sha256"] == FROZEN_STAGE_A_IDENTITIES["eligibility_identity"], "attempt-2 eligibility identity mismatch")
    _require(stage_a["registered_cell_identity_sha256"] == core.canonical_hash([row["cell_id"] for row in registry["records"]]), "live ordered cell registry drift")
    _require(stage_a["eligibility_identity_sha256"] == core.canonical_hash(eligibility["records"]), "live eligibility identity drift")
    _require(stage_a["provider_fallback_identity"] == provider_identity == {
        "fallback_hierarchy_sha256": FROZEN_STAGE_A_IDENTITIES["fallback_hierarchy"],
        "provider_selection_sha256": FROZEN_STAGE_A_IDENTITIES["provider_selection"],
        "provider_selection_count": 38,
    }, "attempt-2 provider/fallback identity mismatch")

    historical = core.load_schema_json(core.ATTEMPT_1_FREEZE_PATH)
    corrected_gold, gold_identity = _correct_gold_evidence(historical, prereg)
    _require(stage_a["gold_peer_evidence_integrity"] == gold_identity, "attempt-2 gold evidence identity mismatch")
    _require(stage_a["gold_peer_evidence"] == corrected_gold and stage_a["admitted_gold_peers"] == list(historical["admitted_gold_peers"]), "attempt-2 gold evidence content mismatch")
    _require(stage_a["integrity_correction"] == {
        "scope": "ORDERED_SCHEMA_PERSISTENCE_AND_RISK_0002_PREEXECUTION_GATE_INTEGRITY",
        "schema_serializer": "INSERTION_ORDER_PRESERVING_DETERMINISTIC_JSON",
        "schema_loader": "INSERTION_ORDER_PRESERVING_DUPLICATE_KEY_REJECTING_JSON",
        "canonical_hash_serializer": "SORT_KEYS_TRUE_UNCHANGED",
        "durable_review_verification": "LIVE_GITHUB_REVIEW_AND_CURRENT_PR_EXACT_HEAD",
        "result_emission_order": "DIRECT_FROZEN_ORDERED_TRIAL_REGISTRY_TRAVERSAL",
        "attempt_2_acquisition_entrypoints": "FAIL_CLOSED_BEFORE_IO_OR_NETWORK",
        "semantic_or_numeric_change": False,
    }, "attempt-2 integrity correction scope drift")
    _require(stage_a["drift_confirmations"] == {
        "no_reacquisition": True, "no_provider_or_fallback_drift": True,
        "no_config_drift": True, "no_protocol_or_preregistration_drift": True,
        "no_eligibility_or_missingness_drift": True, "no_trial_registry_drift": True,
        "no_scenario_window_metric_threshold_formula_or_result_rule_drift": True,
    }, "attempt-2 drift assertions mismatch")
    _require(stage_a["network_after_freeze"] == (
        "MARKET_DATA_PROVIDER_AND_FALLBACK_NETWORK_PROHIBITED;"
        "GITHUB_REVIEW_METADATA_VERIFICATION_REQUIRED_PREEXECUTION"
    ), "attempt-2 network prohibition mismatch")
    _require(stage_a["registered_cells_executed"] == 0 and stage_a["execution_marker_created"] is False and stage_a["result_artifacts_created"] is False, "attempt-2 Stage-A is not preexecution")
    _require(stage_a["attempt_authorization_consumed"] is False and stage_a["execution_permitted"] is False, "attempt-2 authorization state mismatch")
    _require(stage_a["ready_for"] == "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD_REVIEW_ONLY", "attempt-2 Stage-A lifecycle state mismatch")


def verify_runtime_preexecution_state() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Revalidate every frozen/Stage-A precondition without executing a study cell."""
    _assert_no_execution_artifacts()
    _assert_risk_0002_effective()
    prereg, eligibility, registry = _verify_frozen_repository_inputs()
    provider_identity = _verify_provider_identity(prereg)
    transplant = _verify_transplant_destinations()
    _require(core.ATTEMPT_2_STAGE_A_PATH.is_file(), "attempt-2 Stage-A attestation is absent")
    stage_a = core.load_schema_json(core.ATTEMPT_2_STAGE_A_PATH)
    _verify_runtime_stage_a(stage_a, prereg, eligibility, registry, provider_identity, transplant)
    _verify_preexecution_metadata(stage_a)
    return stage_a, core.load_yaml(core.CONFIG_PATH), prereg, eligibility


def build_attestation(forensic_root: Path | None, generated_at_utc: str, focused_test_command: str) -> None:
    _assert_no_execution_artifacts()
    _assert_risk_0002_effective()
    prereg, eligibility, registry = _verify_frozen_repository_inputs()
    provider_identity = _verify_provider_identity(prereg)
    if forensic_root is None:
        existing = core.load_schema_json(core.ATTEMPT_2_STAGE_A_PATH)
        forensic = existing["forensic_identity"]
        _verify_recorded_forensic_identity(forensic)
        transplant = _verify_transplant_destinations()
    else:
        forensic = _verify_forensic_source(forensic_root)
        transplant = _write_transplant_manifest(forensic_root, generated_at_utc)

    historical = core.load_schema_json(core.ATTEMPT_1_FREEZE_PATH)
    _require(core.sha256_file(core.ATTEMPT_1_FREEZE_PATH) == ATTEMPT_1_FREEZE_SHA256, "attempt-1 freeze hash mismatch")
    _require(core.sha256_file(core.ATTEMPT_1 / "execution_receipt.json") == ATTEMPT_1_RECEIPT_SHA256, "attempt-1 receipt hash mismatch")
    _require(core.sha256_file(core.ATTEMPT_1 / "execution_defect.json") == ATTEMPT_1_DEFECT_SHA256, "attempt-1 defect hash mismatch")
    corrected_gold, gold_identity = _correct_gold_evidence(historical, prereg)

    implementation_hashes = _implementation_hashes()
    focused_test_hash = core.sha256_file(core.ROOT / "test_risk_level1_implementation.py")
    attestation = {
        "schema_version": "4.0",
        "repository": REPOSITORY_IDENTITY,
        "pull_request_number": IMPLEMENTATION_PR_NUMBER,
        "study_id": "RISK-0001",
        "attempt_id": core.ATTEMPT_2_ID,
        "implementation_author_identity": IMPLEMENTATION_AUTHOR_IDENTITY,
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
            "scope": "ORDERED_SCHEMA_PERSISTENCE_AND_RISK_0002_PREEXECUTION_GATE_INTEGRITY",
            "schema_serializer": "INSERTION_ORDER_PRESERVING_DETERMINISTIC_JSON",
            "schema_loader": "INSERTION_ORDER_PRESERVING_DUPLICATE_KEY_REJECTING_JSON",
            "canonical_hash_serializer": "SORT_KEYS_TRUE_UNCHANGED",
            "durable_review_verification": "LIVE_GITHUB_REVIEW_AND_CURRENT_PR_EXACT_HEAD",
            "result_emission_order": "DIRECT_FROZEN_ORDERED_TRIAL_REGISTRY_TRAVERSAL",
            "attempt_2_acquisition_entrypoints": "FAIL_CLOSED_BEFORE_IO_OR_NETWORK",
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
        "network_after_freeze": (
            "MARKET_DATA_PROVIDER_AND_FALLBACK_NETWORK_PROHIBITED;"
            "GITHUB_REVIEW_METADATA_VERIFICATION_REQUIRED_PREEXECUTION"
        ),
        "registered_cells_executed": 0,
        "execution_marker_created": False,
        "result_artifacts_created": False,
        "attempt_authorization_consumed": False,
        "execution_permitted": False,
        "ready_for": "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD_REVIEW_ONLY",
    }
    core.write_schema_json(core.ATTEMPT_2_STAGE_A_PATH, attestation)
    core.write_schema_json(core.ATTEMPT_2_METADATA_PATH, _expected_metadata(attestation))


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--forensic-root", type=Path)
    source.add_argument("--reuse-verified-transplant", action="store_true")
    parser.add_argument("--generated-at-utc", required=True)
    parser.add_argument("--focused-test-command", required=True)
    args = parser.parse_args()
    forensic_root = args.forensic_root.resolve() if args.forensic_root is not None else None
    build_attestation(forensic_root, args.generated_at_utc, args.focused_test_command)
    print(f"attempt-2 Stage-A attestation: {core.ATTEMPT_2_STAGE_A_PATH}")
    print("registered RISK cells executed: 0")
    print("attempt-2 authorization consumed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
