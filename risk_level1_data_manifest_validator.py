"""Fail-closed schema/provenance validator for RISK-0001 acquisition artifacts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

import yaml

import risk_level1_core as core


DATASET_KEYS = (
    "dataset_id", "instrument_identity", "study_role", "provider", "source_classification",
    "endpoint_locator", "query_parameters", "acquisition_timestamp_utc", "pagination_page_receipts",
    "terminal_pagination_proved", "raw_byte_count", "raw_sha256", "raw_page_hashes",
    "transformed_path", "transformed_byte_count", "transformed_sha256", "first_observation",
    "last_observation", "row_count", "expected_row_count", "frequency", "timezone",
    "market_session_calendar", "close_convention", "inception_listing_date", "structured_gap_blocks",
    "duplicates", "missingness_classification", "transformations", "adjustment_mode",
    "total_return_construction", "dividend_treatment", "split_treatment", "corporate_action_treatment",
    "ticker_legal_identity_lineage", "limitations", "licensing_provenance",
    "commit_quarantine_disposition", "scenario_window_eligibility", "metric_eligibility",
    "abstention_remediation_status",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def validate_manifest(path: Path = core.MANIFEST_PATH, *, require_local_quarantine: bool = False) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return (f"manifest load failed: {exc}",)
    if type(manifest) is not dict:
        return ("manifest root must be a mapping",)
    expected_top = ("schema_version", "study_id", "generated_at_utc", "authority", "provider_fallback_hierarchy", "dataset_count", "datasets", "corporate_actions", "identity_evidence", "quarantine_policy")
    if tuple(manifest) != expected_top:
        errors.append(f"manifest exact top keys/order required: {expected_top}")
        return tuple(errors)
    if manifest["schema_version"] != "1.0" or manifest["study_id"] != "RISK-0001":
        errors.append("manifest identity mismatch")
    prereg = core.load_yaml(core.PREREG_PATH)
    if manifest["provider_fallback_hierarchy"] != prereg["fallback_order"]:
        errors.append("manifest provider/fallback hierarchy drift")
    datasets = manifest["datasets"]
    if type(datasets) is not list or len(datasets) != 38 or manifest["dataset_count"] != 38:
        errors.append("manifest must contain exactly 37 representations plus DFF")
        return tuple(errors)
    ids = []
    for index, row in enumerate(datasets):
        if type(row) is not dict or tuple(row) != DATASET_KEYS:
            errors.append(f"datasets[{index}] exact keys/order mismatch")
            continue
        ids.append(row["dataset_id"])
        provider = row["provider"]
        if provider is not None and provider not in ("ALPACA_MARKET_DATA", "YAHOO_FINANCE_CHART", "ALPACA_CRYPTO", "COINBASE_EXCHANGE", "FRED"):
            errors.append(f"datasets[{index}] provider outside frozen hierarchy")
        expected_class = {"ALPACA_MARKET_DATA": "PRIMARY", "ALPACA_CRYPTO": "PRIMARY",
                          "YAHOO_FINANCE_CHART": "WHOLE_PATH_FALLBACK",
                          "COINBASE_EXCHANGE": "WHOLE_PATH_FALLBACK",
                          "FRED": "OFFICIAL_PUBLIC_DOMAIN", None: "UNAVAILABLE"}.get(provider)
        if expected_class is not None and row["source_classification"] != expected_class:
            errors.append(f"datasets[{index}] provider/source classification violates frozen fallback order")
        if row["transformed_sha256"] is not None and not SHA_RE.fullmatch(str(row["transformed_sha256"])):
            errors.append(f"datasets[{index}] transformed SHA invalid")
        if row["raw_sha256"] is not None and not SHA_RE.fullmatch(str(row["raw_sha256"])):
            errors.append(f"datasets[{index}] raw SHA invalid")
        if row["raw_byte_count"] < 0 or row["transformed_byte_count"] < 0 or row["row_count"] < 0:
            errors.append(f"datasets[{index}] negative count")
        if provider is not None and not row["pagination_page_receipts"]:
            errors.append(f"datasets[{index}] selected source missing receipts")
        if provider is not None and not row["terminal_pagination_proved"]:
            errors.append(f"datasets[{index}] terminal pagination not proved")
        for receipt in row["pagination_page_receipts"]:
            receipt_path = core.ROOT / receipt
            if not receipt_path.is_file():
                errors.append(f"datasets[{index}] receipt missing: {receipt}")
                continue
            value = core.load_json(receipt_path)
            required_receipt = ("endpoint_locator", "request_timestamp_utc", "response_status", "page_index",
                                "next_page_or_terminal_marker", "raw_byte_count", "raw_sha256", "provider")
            if any(value.get(key) is None for key in required_receipt):
                errors.append(f"datasets[{index}] receipt required field missing: {receipt}")
            if value.get("provider") != provider:
                errors.append(f"datasets[{index}] receipt provider mismatch: {receipt}")
        if row["raw_page_hashes"] and row["raw_sha256"] != core.canonical_hash(row["raw_page_hashes"]):
            errors.append(f"datasets[{index}] aggregate raw hash mismatch")
        transformed = row["transformed_path"]
        if transformed:
            local = core.ROOT / transformed
            quarantined = "quarantine" in Path(transformed).parts
            if local.is_file():
                if core.sha256_file(local) != row["transformed_sha256"]:
                    errors.append(f"datasets[{index}] transformed hash mismatch")
            elif not quarantined or require_local_quarantine:
                errors.append(f"datasets[{index}] transformed file missing")
        if row["instrument_identity"] in ("BTC", "ETH", "SOL"):
            if row["total_return_construction"] != "SPOT_PRICE_RETURN_ONLY" or row["dividend_treatment"] != "NOT_APPLICABLE":
                errors.append(f"datasets[{index}] crypto yield/dividend boundary violated")
        if row["instrument_identity"] in ("GLD", "IAU", "SGOL", "GLDM") and "EXPENSE" in str(row["transformations"]):
            errors.append(f"datasets[{index}] second gold expense subtraction prohibited")
    if len(ids) != len(set(ids)):
        errors.append("manifest dataset IDs must be unique")
    authority_hashes = manifest["authority"]
    if authority_hashes.get("protocol_sha256") != core.sha256_file(core.PROTOCOL_PATH):
        errors.append("manifest protocol hash mismatch")
    if authority_hashes.get("preregistration_sha256") != core.sha256_file(core.PREREG_PATH):
        errors.append("manifest preregistration hash mismatch")
    return tuple(errors)


def main() -> int:
    errors = validate_manifest()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("RISK-0001 data manifest valid: 38 datasets, frozen hierarchy and provenance complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
