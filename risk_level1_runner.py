"""Two-phase, network-free RISK-0001 data-gate freeze and one-shot runner."""

from __future__ import annotations

import argparse
import copy
import json
import math
import statistics
import subprocess
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

import yaml

import level1_sleeve_robustness_preregistration_validator as authority
import risk_level1_core as core


EXECUTION_RECEIPT = core.RESULTS / "execution_receipt.json"
RAW_EVIDENCE_PATH = core.RESULTS / "raw_evidence.json"
CELL_RESULTS_PATH = core.RESULTS / "cell_results.json"
DISPOSITION_PATH = core.RESULTS / "disposition.json"
DIAGNOSTICS_PATH = core.RESULTS / "diagnostics.json"
LIMITATIONS_PATH = core.RESULTS / "LIMITATIONS_AND_SURVIVORSHIP.md"
RESULTS_REPORT_PATH = core.RESULTS / "RESULTS.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _receipt_files() -> list[Path]:
    return sorted((core.DATA / "receipts").glob("*.final.json"))


def _receipt_records() -> list[dict[str, Any]]:
    records = []
    for path in _receipt_files():
        value = core.load_json(path)
        value["receipt_path"] = str(path.relative_to(core.ROOT))
        records.append(value)
    return records


def _write_receipt_inventory() -> dict[str, Any]:
    records = []
    for path in sorted((core.DATA / "receipts").glob("*.json")):
        value = core.load_json(path)
        records.append({"receipt_path": str(path.relative_to(core.ROOT)),
                        "receipt_sha256": core.sha256_file(path),
                        "dataset_id": value.get("dataset_id"), "provider": value.get("provider"),
                        "response_status": value.get("response_status"), "error": value.get("error"),
                        "raw_byte_count": value.get("raw_byte_count"), "raw_sha256": value.get("raw_sha256"),
                        "terminal_marker": value.get("next_page_or_terminal_marker")})
    output = {"schema_version": "1.0", "study_id": "RISK-0001", "generated_at_utc": now_utc(),
              "receipt_count": len(records), "failed_attempt_count": sum(row["error"] is not None for row in records),
              "records": records}
    core.write_json(core.DATA / "acquisition_receipt_inventory.json", output)
    return output


def _identity_success(receipts: list[Mapping[str, Any]]) -> dict[str, bool]:
    output = {}
    for rep in ("CEG", "GEV", "RKLB", "RTX", "META", "SPGI"):
        matches = [row for row in receipts if row["dataset_id"].startswith(f"identity:{rep}:")]
        output[rep] = bool(matches and all(row["response_status"] == 200 and row["raw_sha256"] for row in matches))
    return output


def _manifest_record(source: Mapping[str, Any], family: str, receipts: list[Mapping[str, Any]], eligibility: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    rep = source["instrument"]
    provider = source.get("selected_provider")
    selected_receipts = [row for row in receipts if row["dataset_id"].startswith((f"stock:{rep}:", f"crypto:{rep}:")) and (provider is None or row["provider"] == provider)]
    quality = source.get("primary_quality") if str(provider).startswith("ALPACA") else source.get("fallback_quality")
    relevant = [row for row in eligibility["records"] if row["representation_id"] == rep]
    endpoints = config["acquisition"]["crypto" if family == "CRYPTO" else "equities_etfs"]
    source_classification = "PRIMARY" if provider in ("ALPACA_MARKET_DATA", "ALPACA_CRYPTO") else "WHOLE_PATH_FALLBACK" if provider else "UNAVAILABLE"
    raw_hashes = [row["raw_sha256"] for row in selected_receipts if row.get("raw_sha256")]
    raw_bytes = sum(int(row.get("raw_byte_count") or 0) for row in selected_receipts)
    window_states = {window: sorted({row["cell_missingness_state"] for row in relevant if row["window_id"] == window}) for window in core.WINDOWS}
    return {
        "dataset_id": f"RISK-0001:{family}:{rep}", "instrument_identity": rep,
        "study_role": "CRYPTO_SPOT_RETURN_INPUT" if family == "CRYPTO" else "EQUITY_ETF_TOTAL_RETURN_INPUT",
        "provider": provider, "source_classification": source_classification,
        "endpoint_locator": endpoints["endpoint"] if source_classification == "PRIMARY" else endpoints.get("fallback_endpoint"),
        "query_parameters": endpoints["parameters"] if source_classification == "PRIMARY" else endpoints.get("fallback_parameters"),
        "acquisition_timestamp_utc": selected_receipts[0]["request_timestamp_utc"] if selected_receipts else None,
        "pagination_page_receipts": [row["receipt_path"] for row in selected_receipts],
        "terminal_pagination_proved": bool(selected_receipts and selected_receipts[-1].get("next_page_or_terminal_marker") == "TERMINAL"),
        "raw_byte_count": raw_bytes, "raw_sha256": core.canonical_hash(raw_hashes) if raw_hashes else None,
        "raw_page_hashes": raw_hashes,
        "transformed_path": source.get("selected_path"),
        "transformed_byte_count": (core.ROOT / source["selected_path"]).stat().st_size if source.get("selected_path") else 0,
        "transformed_sha256": source.get("selected_transformed_sha256"),
        "first_observation": (quality or {}).get("first_observation"), "last_observation": (quality or {}).get("last_observation"),
        "row_count": (quality or {}).get("row_count", 0), "expected_row_count": (quality or {}).get("expected_row_count", 0),
        "frequency": "UTC_DAILY" if family == "CRYPTO" else "XNYS_SESSION_DAILY",
        "timezone": "UTC" if family == "CRYPTO" else "America/New_York",
        "market_session_calendar": "UTC_24_7" if family == "CRYPTO" else "XNYS_OFFICIAL_SESSIONS",
        "close_convention": "UTC_DAILY_CLOSE" if family == "CRYPTO" else "OFFICIAL_SESSION_CLOSE",
        "inception_listing_date": source.get("lawful_inception") or (config.get("identity_boundaries", {}).get(rep) or {}).get("lawful_inception") or (quality or {}).get("first_observation"),
        "structured_gap_blocks": (quality or {}).get("gap_blocks", []), "duplicates": (quality or {}).get("duplicates", 0),
        "missingness_classification": window_states,
        "transformations": ["UTC_OR_SESSION_DATE_NORMALIZATION", "SORT_CANONIC_ASCENDING", "FINITE_OHLC_NORMALIZATION"],
        "adjustment_mode": "SPOT" if family == "CRYPTO" else "SPLIT_ADJUSTED_NON_TOTAL_RETURN_CLOSE_PLUS_EXPLICIT_EVENTS",
        "total_return_construction": "SPOT_PRICE_RETURN_ONLY" if family == "CRYPTO" else "SPLIT_ADJUSTED_NON_TOTAL_RETURN_PRICE_PLUS_EXPLICIT_GROSS_DIVIDENDS",
        "dividend_treatment": "NOT_APPLICABLE" if family == "CRYPTO" else "GROSS_DECLARED_CASH_CREDITED_ON_EX_DATE",
        "split_treatment": "NOT_APPLICABLE" if family == "CRYPTO" else "PRICE_PATH_SPLIT_ADJUSTED_SPLIT_EVENTS_CONTINUITY_ONLY_NO_DOUBLE_COUNT",
        "corporate_action_treatment": "SPOT_ONLY_NO_YIELD" if family == "CRYPTO" else "UNRESOLVED_NONCASH_ACTION_MAKES_INTERSECTING_CELL_NULL",
        "ticker_legal_identity_lineage": (config.get("identity_boundaries", {}).get(rep) or {}).get("rule", "CURRENT_LISTED_IDENTITY_NO_PREDECESSOR_STITCHING"),
        "limitations": [value for value in (source.get("primary_error"), source.get("fallback_error"), source.get("action_acquisition_error")) if value],
        "licensing_provenance": "EXISTING_REPOSITORY_ALPACA_PRECEDENT" if source_classification == "PRIMARY" else "QUARANTINED_NOT_COMMITTED" if source_classification == "WHOLE_PATH_FALLBACK" else "NO_INPUT",
        "commit_quarantine_disposition": source["commit_or_quarantine_disposition"],
        "scenario_window_eligibility": window_states,
        "metric_eligibility": "PATH_METRICS_FOLLOW_CELL_STATE_DFF_METRICS_SEPARATELY_GATED",
        "abstention_remediation_status": "FROZEN_NO_REMEDIATION_AFTER_EXECUTION" if provider else "ABSTAIN_MISSING_SOURCE",
    }


def _write_manifest(prereg: Mapping[str, Any], config: Mapping[str, Any], source_inventory: Mapping[str, Any], receipts: list[Mapping[str, Any]], eligibility: Mapping[str, Any]) -> dict[str, Any]:
    family_by_rep = core.representation_family(prereg)
    sources = list(source_inventory["stock_and_etf_datasets"]) + list(source_inventory["crypto_datasets"])
    datasets = [_manifest_record(source, family_by_rep[source["instrument"]], receipts, eligibility, config) for source in sources]
    dff = source_inventory["comparator_dataset"]
    dff_receipts = [row for row in receipts if row["dataset_id"] == "comparator:DFF:FRED"]
    datasets.append({
        "dataset_id": "RISK-0001:COMPARATOR:DFF", "instrument_identity": "DFF", "study_role": "ANALYTICAL_OPPORTUNITY_COST_ONLY",
        "provider": dff.get("selected_provider"), "source_classification": "OFFICIAL_PUBLIC_DOMAIN" if dff.get("selected_provider") else "UNAVAILABLE",
        "endpoint_locator": config["acquisition"]["comparator"]["endpoint"], "query_parameters": {"series": "DFF"},
        "acquisition_timestamp_utc": dff_receipts[0]["request_timestamp_utc"] if dff_receipts else None,
        "pagination_page_receipts": [row["receipt_path"] for row in dff_receipts], "terminal_pagination_proved": bool(dff_receipts),
        "raw_byte_count": sum(int(row.get("raw_byte_count") or 0) for row in dff_receipts),
        "raw_sha256": core.canonical_hash([row["raw_sha256"] for row in dff_receipts]) if dff_receipts else None,
        "raw_page_hashes": [row["raw_sha256"] for row in dff_receipts], "transformed_path": dff.get("selected_path"),
        "transformed_byte_count": (core.ROOT / dff["selected_path"]).stat().st_size if dff.get("selected_path") else 0,
        "transformed_sha256": dff.get("selected_transformed_sha256"), "first_observation": dff.get("first_observation"),
        "last_observation": dff.get("last_observation"), "row_count": dff.get("row_count", 0), "expected_row_count": None,
        "frequency": "FEDERAL_RESERVE_BUSINESS_DAY_OBSERVATION", "timezone": "America/New_York",
        "market_session_calendar": "US_FEDERAL_RESERVE_BANK_BUSINESS_DAYS", "close_convention": "LAWFUL_AT_23_59_59_ET_ONE_BUSINESS_DAY_LAGGED",
        "inception_listing_date": dff.get("first_observation"), "structured_gap_blocks": [], "duplicates": 0,
        "missingness_classification": "PER_WINDOW_ZERO_MISSING_REQUIRED_LAWFULLY_LAGGED_OBSERVATIONS",
        "transformations": ["CSV_PARSE", "DOT_MISSING_ROWS_PRESERVED_AS_MISSING", "ONE_BUSINESS_DAY_LAWFUL_AVAILABILITY_LAG"],
        "adjustment_mode": "NOT_APPLICABLE", "total_return_construction": "SIMPLE_ACTUAL_360_DAILY_FACTOR_COMPOUNDED_BY_CALENDAR_DAY",
        "dividend_treatment": "NOT_APPLICABLE", "split_treatment": "NOT_APPLICABLE", "corporate_action_treatment": "NOT_APPLICABLE",
        "ticker_legal_identity_lineage": "OFFICIAL_FRED_SERIES_DFF", "limitations": [dff.get("error")] if dff.get("error") else [],
        "licensing_provenance": "OFFICIAL_US_GOVERNMENT_PUBLIC_DOMAIN", "commit_quarantine_disposition": dff["commit_or_quarantine_disposition"],
        "scenario_window_eligibility": "AFFECTED_OPPORTUNITY_COST_METRICS_ONLY", "metric_eligibility": "ZERO_MISSING_REQUIRED_OBSERVATIONS",
        "abstention_remediation_status": "FROZEN_NO_ANALYTICAL_FALLBACK",
    })
    manifest = {"schema_version": "1.0", "study_id": "RISK-0001", "generated_at_utc": now_utc(),
                "authority": {"protocol_sha256": config["authority"]["protocol_sha256"], "preregistration_sha256": config["authority"]["preregistration_sha256"],
                              "implementation_config_sha256": core.sha256_file(core.CONFIG_PATH)},
                "provider_fallback_hierarchy": prereg["fallback_order"], "dataset_count": len(datasets), "datasets": datasets,
                "corporate_actions": source_inventory["corporate_actions"], "identity_evidence": source_inventory["identity_evidence"],
                "quarantine_policy": "YAHOO_AND_COINBASE_BYTES_NOT_COMMITTED_HASH_PINNED_BY_RECEIPTS_AND_MANIFEST"}
    core.MANIFEST_PATH.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return manifest


def prepare() -> None:
    raise core.IntegrityError(
        "RISK-0002 requires exact frozen attempt-1 input reuse; prepare/reacquisition is prohibited"
    )


def _historical_attempt_1_prepare_procedure() -> None:
    """Retained only as forensic implementation context; attempt 2 may not call it."""
    if EXECUTION_RECEIPT.exists():
        raise core.IntegrityError("execution receipt already exists; no new prepare/rerun is permitted")
    validated = authority.validate_repository()
    if validated.errors:
        raise core.IntegrityError("authority invalid: " + "; ".join(validated.errors))
    config = core.load_yaml(core.CONFIG_PATH)
    prereg = core.load_yaml(core.PREREG_PATH)
    source_inventory = core.load_json(core.SOURCE_INVENTORY_PATH)
    if authority.sha256_file(core.PROTOCOL_PATH) != config["authority"]["protocol_sha256"] or authority.sha256_file(core.PREREG_PATH) != config["authority"]["preregistration_sha256"]:
        raise core.IntegrityError("authority hash mismatch")
    receipts = _receipt_records()
    if not receipts:
        raise core.IntegrityError("study-wide receipt registry is empty")
    receipt_inventory = _write_receipt_inventory()
    runtime_config = copy.deepcopy(config)
    runtime_config["_identity_receipt_complete"] = _identity_success(receipts)
    schedule = core.xny_schedule("2004-11-18", "2026-07-31")
    calendar_path = core.DATA / "transformed/XNYS_sessions.json"
    core.write_json(calendar_path, {"schema_version": "1.0", "calendar": "XNYS", "provider": "exchange_calendars", "package_version": config["calendar"]["package_version"], "sessions": schedule})
    documents = {}
    quality_map = {}
    for family, reps in core.family_representations(prereg).items():
        for rep in reps:
            source = core.selected_record(source_inventory, rep)
            documents[rep] = core.selected_document(source)
            quality_map[rep] = source.get("primary_quality") if str(source.get("selected_provider")).startswith("ALPACA") else source.get("fallback_quality")
    gold_evidence = core.gold_peer_evidence(documents, quality_map, schedule)
    admitted = set(core.admitted_gold_peers(prereg, gold_evidence))
    eligibility = core.build_eligibility(prereg, runtime_config, source_inventory, documents, admitted)
    # Identity evidence failures are cell-local action/lineage failures, not a global halt.
    identity_ok = runtime_config["_identity_receipt_complete"]
    for row in eligibility["records"]:
        rep = row["representation_id"]
        if rep in identity_ok and not identity_ok[rep] and row["cell_missingness_state"] == "ELIGIBLE":
            row["cell_missingness_state"] = "CORPORATE_ACTION_UNRESOLVED"
            row["reason"] = "PRIMARY_IDENTITY_EVIDENCE_RECEIPT_UNAVAILABLE"
    eligibility["state_counts"] = {state: sum(row["cell_missingness_state"] == state for row in eligibility["records"]) for state in core.MISSINGNESS}
    core.write_json(core.ELIGIBILITY_PATH, eligibility)
    config_hash = core.sha256_file(core.CONFIG_PATH)
    dff_hash = source_inventory["comparator_dataset"].get("selected_transformed_sha256") or "0" * 64
    action_hash = source_inventory["corporate_actions"].get("transformed_sha256") or "0" * 64
    lineage_hash = source_inventory["identity_evidence"]["registry_sha256"]
    calendar_hash = core.sha256_file(calendar_path)
    data_hashes = {}
    for rep in core.representation_family(prereg):
        source = core.selected_record(source_inventory, rep)
        data_hashes[rep] = core.canonical_hash({"selected": source.get("selected_transformed_sha256"), "actions": action_hash,
                                                "lineage": lineage_hash, "dff": dff_hash, "calendar": calendar_hash})
    registry = core.trial_registry(prereg, config_hash, eligibility, data_hashes)
    core.write_json(core.TRIAL_REGISTRY_PATH, registry)
    manifest = _write_manifest(prereg, config, source_inventory, receipts, eligibility)
    import risk_level1_data_manifest_validator as manifest_validator
    manifest_errors = manifest_validator.validate_manifest(require_local_quarantine=True)
    if manifest_errors:
        raise core.IntegrityError("manifest validation failed: " + "; ".join(manifest_errors))
    implementation_files = [core.ROOT / name for name in ("risk_level1_acquisition.py", "risk_level1_core.py", "risk_level1_runner.py", "risk_level1_data_manifest_validator.py", "risk_level1_result_validator.py")]
    missing_code = [path.name for path in implementation_files if not path.is_file()]
    if missing_code:
        raise core.IntegrityError(f"implementation bundle incomplete: {missing_code}")
    freeze = {"schema_version": "1.0", "study_id": "RISK-0001", "frozen_at_utc": now_utc(),
              "stage_a": {"status": "PASS", "gates": list(prereg["data_gate"]["GLOBAL_STUDY_INTEGRITY"]["gates"])},
              "authority_hashes": {"protocol": core.sha256_file(core.PROTOCOL_PATH), "preregistration": core.sha256_file(core.PREREG_PATH)},
              "implementation_config_sha256": config_hash,
              "implementation_code_hashes": {path.name: core.sha256_file(path) for path in implementation_files},
              "source_inventory_sha256": core.sha256_file(core.SOURCE_INVENTORY_PATH), "manifest_sha256": core.sha256_file(core.MANIFEST_PATH),
              "acquisition_receipt_inventory_sha256": core.sha256_file(core.DATA / "acquisition_receipt_inventory.json"),
              "acquisition_receipt_count": receipt_inventory["receipt_count"], "failed_acquisition_attempt_count": receipt_inventory["failed_attempt_count"],
              "calendar_sha256": calendar_hash, "eligibility_matrix_sha256": core.sha256_file(core.ELIGIBILITY_PATH),
              "trial_registry_sha256": core.sha256_file(core.TRIAL_REGISTRY_PATH), "registered_cell_count": 777,
              "gold_peer_evidence": gold_evidence, "admitted_gold_peers": sorted(admitted, key=("IAU", "SGOL", "GLDM").index),
              "network_after_freeze": "PROHIBITED", "execution_permitted": True}
    core.write_json(core.FREEZE_PATH, freeze)
    print(f"RISK-0001 data gate frozen: cells=777 eligible={eligibility['state_counts']['ELIGIBLE']} admitted_gold={freeze['admitted_gold_peers']}")


def _verify_freeze() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    freeze = core.load_json(core.FREEZE_PATH)
    if freeze.get("attempt_id") != core.ATTEMPT_2_ID:
        raise core.IntegrityError("attempt-2 Stage-A identity mismatch")
    if freeze.get("attempt_authorization_consumed") is not False:
        raise core.IntegrityError("attempt-2 Stage-A must precede authorization consumption")
    if freeze.get("registered_cells_executed") != 0:
        raise core.IntegrityError("attempt-2 Stage-A must attest zero registered cells executed")
    config = core.load_yaml(core.CONFIG_PATH)
    prereg = core.load_yaml(core.PREREG_PATH)
    eligibility = core.load_json(core.ELIGIBILITY_PATH)
    checks = {
        core.MANIFEST_PATH: freeze["manifest_sha256"], core.ELIGIBILITY_PATH: freeze["eligibility_matrix_sha256"],
        core.TRIAL_REGISTRY_PATH: freeze["trial_registry_sha256"], core.SOURCE_INVENTORY_PATH: freeze["source_inventory_sha256"],
        core.DATA / "acquisition_receipt_inventory.json": freeze["acquisition_receipt_inventory_sha256"],
    }
    for path, expected in checks.items():
        if core.sha256_file(path) != expected:
            raise core.IntegrityError(f"frozen input hash mismatch: {path}")
    for name, expected in freeze["implementation_code_hashes"].items():
        if core.sha256_file(core.ROOT / name) != expected:
            raise core.IntegrityError(f"frozen implementation hash mismatch: {name}")
    if eligibility["registered_cell_count"] != 777:
        raise core.IntegrityError("frozen eligibility count mismatch")
    return freeze, config, prereg, eligibility


def _verify_independent_preexecution_review() -> None:
    if not core.ATTEMPT_2_REVIEW_RECEIPT_PATH.is_file():
        raise core.IntegrityError(
            "mandatory independent exact-head preexecution review receipt is absent"
        )
    review = core.load_schema_json(core.ATTEMPT_2_REVIEW_RECEIPT_PATH)
    expected_keys = (
        "schema_version", "study_id", "attempt_id", "review_type",
        "reviewed_head", "stage_a_attestation_sha256", "reviewer_identity",
        "reviewer_independence", "disposition", "review_url", "reviewed_at_utc",
    )
    if tuple(review) != expected_keys:
        raise core.IntegrityError("preexecution review receipt exact keys/order mismatch")
    if review["study_id"] != "RISK-0001" or review["attempt_id"] != core.ATTEMPT_2_ID:
        raise core.IntegrityError("preexecution review receipt attempt identity mismatch")
    if review["review_type"] != "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD":
        raise core.IntegrityError("preexecution review receipt type mismatch")
    if review["reviewer_independence"] is not True or review["disposition"] != "PASS":
        raise core.IntegrityError("independent preexecution review has not passed")
    if review["stage_a_attestation_sha256"] != core.sha256_file(core.FREEZE_PATH):
        raise core.IntegrityError("preexecution review is not bound to the Stage-A attestation")
    if not all(type(review[key]) is str and review[key] for key in ("reviewed_head", "reviewer_identity", "review_url", "reviewed_at_utc")):
        raise core.IntegrityError("preexecution review receipt identity fields are incomplete")
    current_head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=core.ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if review["reviewed_head"] != current_head:
        raise core.IntegrityError("preexecution review is not bound to the current exact head")


def _cell_index(document: Mapping[str, Any], family: str, start: str, end: str, schedule: list[Mapping[str, str]]) -> list[tuple[str, float]]:
    if family == "CRYPTO":
        return core.align_crypto_to_xnys(document, start, end, schedule)
    return core.total_return_index(document, start, end)


def _raw_operands(metric: str, metrics: Mapping[str, Any], comparator_return: float | None) -> dict[str, str] | None:
    if metric == "EXPOSURE_SCALED_DRAWDOWN_LOSS":
        return {"drawdown": core.decimal_text(metrics["max_drawdown"])}
    if metric == "EXPOSURE_SCALED_STRESS_LOSS":
        return {"stress_return": core.decimal_text(metrics["asset_total_return"])}
    if metric == "EXPOSURE_SCALED_UNDERWATER_BURDEN":
        return {"underwater_area_days": core.decimal_text(metrics["underwater_area_days"])}
    if metric == "EXPOSURE_SCALED_EXCESS_CONTRIBUTION" and comparator_return is not None:
        return {"asset_total_return": core.decimal_text(metrics["asset_total_return"]), "comparator_total_return": core.decimal_text(comparator_return)}
    return None


def execute() -> None:
    if EXECUTION_RECEIPT.exists():
        raise core.IntegrityError("RISK-0001 execution receipt exists: rerun prohibited")
    freeze, config, prereg, eligibility = _verify_freeze()
    _verify_independent_preexecution_review()
    core.RESULTS.mkdir(parents=True, exist_ok=True)
    core.write_json(EXECUTION_RECEIPT, {"schema_version": "1.0", "study_id": "RISK-0001", "attempt_id": core.ATTEMPT_2_ID, "started_at_utc": now_utc(),
                                       "status": "EXECUTION_STARTED_NO_RERUN_PERMITTED", "data_gate_freeze_sha256": core.sha256_file(core.FREEZE_PATH),
                                       "rerun_after_this_marker": "PROHIBITED"})
    source_inventory = core.load_json(core.SOURCE_INVENTORY_PATH)
    schedule = core.load_json(core.DATA / "transformed/XNYS_sessions.json")["sessions"]
    documents = {rep: core.selected_document(core.selected_record(source_inventory, rep)) for rep in core.representation_family(prereg)}
    dff_path = source_inventory["comparator_dataset"].get("selected_path")
    dff = core.load_json(core.ROOT / dff_path) if dff_path else None
    lookup = core.eligibility_lookup(eligibility)
    registry = core.load_json(core.TRIAL_REGISTRY_PATH)
    registry_lookup = {(row["representation_id"], row["scenario_id"], row["window_id"]): row for row in registry["records"]}
    computed: dict[tuple[str, str], dict[str, Any]] = {}
    cell_results = []
    for rep, family in core.representation_family(prereg).items():
        for window in core.WINDOWS:
            base = lookup[(rep, "HISTORICAL_REFERENCE", window)]
            state = base["cell_missingness_state"]
            metrics = None
            comparator_return = None
            comparator_missing: list[str] = []
            if state == "ELIGIBLE":
                try:
                    index = _cell_index(documents[rep], family, base["effective_start"], base["effective_end"], schedule)
                    metrics = core.path_metrics(index, 365 if family == "CRYPTO" else 252)
                    if dff is not None:
                        comparator_return, comparator_missing = core.dff_total_return(dff, base["effective_start"], base["effective_end"])
                    metrics["comparator_total_return"] = comparator_return
                    metrics["excess_total_return"] = None if comparator_return is None else metrics["asset_total_return"] - comparator_return
                except (core.IntegrityError, ValueError, ArithmeticError, statistics.StatisticsError) as exc:
                    state = "QUALITY_GATE_FAILED"
                    metrics = None
                    comparator_missing = [f"runtime_integrity:{type(exc).__name__}:{exc}"]
            computed[(rep, window)] = {"missingness_state": state, "metrics": metrics, "comparator_missing": comparator_missing,
                                       "effective_start": base["effective_start"], "effective_end": base["effective_end"]}
            for scenario in core.SCENARIOS:
                trial = registry_lookup[(rep, scenario, window)]
                scaled = None
                if metrics is not None:
                    exposure = Decimal(prereg["scenario_magnitudes"]["values_pct"][family][scenario])
                    scaled = {"drawdown_loss_pp": core.decimal_text(exposure * abs(Decimal(str(metrics["max_drawdown"])))),
                              "stress_loss_pp": core.decimal_text(exposure * max(Decimal("0"), -Decimal(str(metrics["asset_total_return"])))),
                              "underwater_burden_ppdays": core.decimal_text(exposure * Decimal(str(metrics["underwater_area_days"]))),
                              "excess_contribution_pp": None if comparator_return is None else core.decimal_text(exposure * (Decimal(str(metrics["asset_total_return"])) - Decimal(str(comparator_return))))}
                cell_results.append({"cell_id": trial["cell_id"], "representation_id": rep, "research_family": family,
                                     "scenario_id": scenario, "window_id": window, "execution_state": state,
                                     "effective_start": base["effective_start"], "effective_end": base["effective_end"],
                                     "metrics": metrics, "exposure_scaled_metrics": scaled,
                                     "comparator_missing_required_observations": comparator_missing})
    raw_by_family = {}
    final_by_family = {}
    gold_evidence = freeze["gold_peer_evidence"]
    admitted = set(freeze["admitted_gold_peers"])
    for family, all_reps in core.family_representations(prereg).items():
        reps = all_reps if family != "FUND_GLD_DEFENSIVE" else ["GLD"] + [rep for rep in ("IAU", "SGOL", "GLDM") if rep in admitted]
        directions = {}
        for scenario in ("LOWER", "HIGHER"):
            observations = []
            for rep in reps:
                for metric, window in core.VOTING_PLAN:
                    record = computed[(rep, window)]
                    state = record["missingness_state"]
                    operands = None
                    candidate = None
                    reference = None
                    if state == "ELIGIBLE":
                        operands = _raw_operands(metric, record["metrics"], record["metrics"]["comparator_total_return"])
                        if operands is None:
                            state = "MISSING_SOURCE_DATA"
                        else:
                            candidate, reference = core.scenario_report_values(prereg, family, scenario, metric, operands)
                    observations.append({"scenario_id": scenario, "research_family": family, "representation_id": rep,
                                         "metric_id": metric, "window_id": window, "raw_operands": operands,
                                         "reported_candidate": candidate, "reported_reference": reference,
                                         "missingness_state": state})
            directions[scenario] = {"observations": observations}
        evidence = {"study_id": "RISK-0001", "research_family": family,
                    "gold_peer_evidence": gold_evidence if family == "FUND_GLD_DEFENSIVE" else [],
                    "directions": directions}
        raw_by_family[family] = evidence
        final_by_family[family] = authority.evaluate_study_evidence(evidence)
    core.write_json(RAW_EVIDENCE_PATH, {"schema_version": "1.0", "study_id": "RISK-0001", "attempt_id": core.ATTEMPT_2_ID, "families": raw_by_family})
    executed = sum(row["execution_state"] == "ELIGIBLE" for row in cell_results)
    nulls = len(cell_results) - executed
    core.write_json(CELL_RESULTS_PATH, {"schema_version": "1.0", "study_id": "RISK-0001", "attempt_id": core.ATTEMPT_2_ID, "registered_cell_count": 777,
                                       "execution_count": executed, "ineligible_or_null_count": nulls,
                                       "state_counts": {state: sum(row["execution_state"] == state for row in cell_results) for state in core.MISSINGNESS},
                                       "records": cell_results})
    disposition = {"schema_version": "1.0", "study_id": "RISK-0001", "attempt_id": core.ATTEMPT_2_ID, "generated_at_utc": now_utc(),
                   "authority_entrypoint": "level1_sleeve_robustness_preregistration_validator.evaluate_study_evidence",
                   "family_order": list(core.FAMILIES), "families": final_by_family,
                   "no_policy_effect": True, "automatic_adoption": False,
                   "replacement_level1_method_created": False, "level2_membership_or_sizing_created": False,
                   "whole_portfolio_constructed": False, "residual_cash_debt_margin_or_leverage_analyzed": False}
    core.write_json(DISPOSITION_PATH, disposition)
    equity_metrics = [row for row in cell_results if row["research_family"] == "EQUITY" and row["scenario_id"] == "HISTORICAL_REFERENCE" and row["metrics"] is not None]
    diagnostics = {"schema_version": "1.0", "study_id": "RISK-0001",
                   "selection_conditioned_cohort_warning": "The frozen current cohort is not the historical opportunity set.",
                   "gold_peer_admission_evidence": gold_evidence, "admitted_gold_peers": list(freeze["admitted_gold_peers"]),
                   "equity": {"expected_constituents": 27,
                              "eligible_observations_by_window": {window: len({row["representation_id"] for row in equity_metrics if row["window_id"] == window}) for window in core.WINDOWS},
                              "canonical_constituent_order": list(prereg["representations"]["EQUITY"]["ids"]),
                              "loo_derivation": "MECHANICALLY_DERIVED_INSIDE_CANONICAL_EVALUATOR_FROM_THE_SAME_27_CONSTITUENT_STATE_OBJECTS_NO_SECOND_LOO_DATASET"},
                   "representation_evidence": {family: {"mandatory_representations": reps} for family, reps in core.family_representations(prereg).items()},
                   "censored_recovery_count": sum(bool(row.get("metrics") and row["metrics"]["recovery_censor_status"] == "CENSORED_AT_WINDOW_END") for row in cell_results if row["scenario_id"] == "HISTORICAL_REFERENCE"),
                   "limitations_are_preserved_not_imputed": True}
    core.write_json(DIAGNOSTICS_PATH, diagnostics)
    core.write_schema_json(EXECUTION_RECEIPT, {"schema_version": "1.0", "study_id": "RISK-0001", "attempt_id": core.ATTEMPT_2_ID,
                                               "started_at_utc": core.load_json(EXECUTION_RECEIPT)["started_at_utc"],
                                               "completed_at_utc": now_utc(), "status": "COMPLETED_RESULTS_OBSERVED_NO_RERUN_PERMITTED",
                                               "data_gate_freeze_sha256": core.sha256_file(core.FREEZE_PATH), "registered_cell_count": 777,
                                               "execution_count": executed, "ineligible_or_null_count": nulls,
                                               "raw_evidence_sha256": core.sha256_file(RAW_EVIDENCE_PATH),
                                               "cell_results_sha256": core.sha256_file(CELL_RESULTS_PATH),
                                               "disposition_sha256": core.sha256_file(DISPOSITION_PATH), "rerun": "PROHIBITED"})
    _write_reports(disposition, cell_results, diagnostics)
    print(f"RISK-0001 one-shot execution complete: registered=777 executed={executed} null={nulls}")


def _write_reports(disposition: Mapping[str, Any], cells: list[Mapping[str, Any]], diagnostics: Mapping[str, Any]) -> None:
    counts = {state: sum(row["execution_state"] == state for row in cells) for state in core.MISSINGNESS}
    lines = ["# RISK-0001 Results", "", "This is a preregistered historical replay. It changes no portfolio policy, target, membership, sizing, cash, debt, margin, leverage, allocator, or execution behavior.", "",
             "## Closed family dispositions", ""]
    for family in core.FAMILIES:
        result = disposition["families"][family]
        lines.append(f"- `{family}`: `{result['result']}`; review direction `{result['review_direction']}`; point target `{result['point_target_assessment']}`; method direction `{result['method_review_direction']}`.")
    lines += ["", "`provisional_scenario_not_rejected` is non-rejection only—not validation, optimization, adoption, or recommendation.", "",
              "## Cell accounting", "", f"- Registered: 777", f"- Executed eligible cells: {sum(row['execution_state'] == 'ELIGIBLE' for row in cells)}",
              f"- Ineligible/null cells: {sum(row['execution_state'] != 'ELIGIBLE' for row in cells)}"]
    lines += [f"- `{state}`: {count}" for state, count in counts.items()]
    lines += ["", "## Boundaries", "", "No whole portfolio was constructed. No residual was assigned. DFF is analytical opportunity cost only. Equity is constituent/cross-sectional evidence only; broad-market and crypto representations remain separate; conditional gold peers are not ranked or selected.", ""]
    RESULTS_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    limitations = """# RISK-0001 Limitations and Survivorship

- The 27-equity population is the frozen current evidence-ready cohort, not the historical opportunity set. Results are selection-conditioned and do not establish final membership.
- Lawful pre-inception periods remain `NOT_APPLICABLE_PRE_INCEPTION`; they are not fabricated or zero-filled.
- Known gaps, unavailable providers, unresolved identity/corporate actions, failed quality gates, and conditional gold exclusions remain explicit nulls in the 777-cell registry.
- Yahoo and Coinbase fallback payloads, if used, are quarantined for licensing and pinned by receipts/hashes rather than committed.
- Split-adjusted non-total-return prices are combined with explicit gross dividends once. Splits are continuity events and are not added as a second return. Gold fund expenses remain embedded in observed paths. Crypto is spot-only with no yield.
- DFF uses the registered actual/360 convention and one-Federal-Reserve-business-day lawful-availability lag. It is not cash, a residual destination, or a fifth sleeve.
- Known historical windows are preregistered replays, not untouched or prospective evidence.
- This single observed execution may not be rerun under RISK-0001. A discovered post-result integrity defect must be recorded and requires separate authority before correction/re-execution.
"""
    LIMITATIONS_PATH.write_text(limitations, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "execute"))
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare()
    else:
        execute()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
