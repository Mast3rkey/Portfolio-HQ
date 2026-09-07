"""Reacquire only the frozen Coinbase SOL evidence for PORTFOLIO-ROBUSTNESS-0001.

This bounded utility cannot run a study or alter a registered input.  It reads
the already-frozen source inventory, downloads the same fixed historical
Coinbase candle pages used by the predecessor acquisition, normalizes them
deterministically, and succeeds only when the resulting bytes match the frozen
SHA-256.  A mismatch is retained as evidence and exits nonzero.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import ssl
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import certifi


ROOT = Path(__file__).resolve().parent
INVENTORY_PATH = ROOT / "research/level1_sleeve_robustness/data/source_inventory.json"
STUDY_ID = "PORTFOLIO-ROBUSTNESS-0001"
SOURCE_STUDY_ID = "RISK-0001"
SYMBOL = "SOL"
PROVIDER = "COINBASE_EXCHANGE"
HOST = "api.exchange.coinbase.com"
START = date(2004, 11, 18)
END = date(2026, 7, 31)
CHUNK_DAYS = 249
USER_AGENT = "Portfolio-HQ-PORTFOLIO-ROBUSTNESS-0001/1.0 evidence-recovery"


class ReacquisitionError(RuntimeError):
    """Raised when the frozen input cannot be safely reacquired or verified."""


class TrustedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Permit redirects only when they remain on the exact public endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _trusted_url(newurl):
            raise ReacquisitionError(f"refused Coinbase redirect to {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass(frozen=True)
class FrozenPin:
    selected_path: str
    sha256: str
    row_count: int
    first_observation: str
    last_observation: str


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_frozen_pin(path: Path = INVENTORY_PATH) -> FrozenPin:
    inventory = json.loads(path.read_text(encoding="utf-8"))
    if inventory.get("study_id") != SOURCE_STUDY_ID:
        raise ReacquisitionError("source inventory study identity mismatch")
    matches = [
        row for row in inventory.get("crypto_datasets", [])
        if row.get("instrument") == SYMBOL
    ]
    if len(matches) != 1:
        raise ReacquisitionError("source inventory must contain exactly one SOL row")
    row = matches[0]
    quality = row.get("fallback_quality") or {}
    expected = {
        "selected_provider": PROVIDER,
        "whole_path_only": True,
        "commit_or_quarantine_disposition": "QUARANTINED_HASH_PINNED",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ReacquisitionError(f"frozen SOL {key} mismatch")
    if quality.get("duplicates") != 0 or quality.get("missing_count") != 0:
        raise ReacquisitionError("frozen SOL fallback quality is not complete")
    if quality.get("gap_blocks") != [] or quality.get("invalid_ohlc") != 0:
        raise ReacquisitionError("frozen SOL fallback quality is not clean")
    pin = FrozenPin(
        selected_path=str(row.get("selected_path", "")),
        sha256=str(row.get("selected_transformed_sha256", "")),
        row_count=int(quality.get("row_count", -1)),
        first_observation=str(quality.get("first_observation", "")),
        last_observation=str(quality.get("last_observation", "")),
    )
    if pin.selected_path != (
        "research/level1_sleeve_robustness/data/quarantine/selected/SOL.json"
    ):
        raise ReacquisitionError("frozen SOL selected path mismatch")
    if len(pin.sha256) != 64 or any(c not in "0123456789abcdef" for c in pin.sha256):
        raise ReacquisitionError("frozen SOL SHA-256 is invalid")
    if (pin.row_count, pin.first_observation, pin.last_observation) != (
        1871,
        "2021-06-17",
        "2026-07-31",
    ):
        raise ReacquisitionError("frozen SOL coverage identity mismatch")
    return pin


def page_requests() -> list[tuple[int, date, date, str]]:
    """Return the exact fixed 249-day request schedule used by attempt 1."""
    requests = []
    cursor = START
    page = 0
    while cursor <= END:
        chunk_end = min(cursor + timedelta(days=CHUNK_DAYS), END)
        params = {
            "granularity": "86400",
            "start": datetime.combine(
                cursor, datetime.min.time(), tzinfo=timezone.utc
            ).isoformat().replace("+00:00", "Z"),
            "end": datetime.combine(
                chunk_end + timedelta(days=1),
                datetime.min.time(),
                tzinfo=timezone.utc,
            ).isoformat().replace("+00:00", "Z"),
        }
        url = (
            f"https://{HOST}/products/{SYMBOL}-USD/candles?"
            f"{urllib.parse.urlencode(params)}"
        )
        requests.append((page, cursor, chunk_end, url))
        cursor = chunk_end + timedelta(days=1)
        page += 1
    return requests


def _trusted_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    return (
        parsed.scheme == "https"
        and parsed.hostname == HOST
        and parsed.port in (None, 443)
        and parsed.username is None
        and parsed.password is None
        and parsed.path == f"/products/{SYMBOL}-USD/candles"
    )


def fetch_page(url: str, *, retries: int = 4) -> bytes:
    if not _trusted_url(url):
        raise ReacquisitionError("refused non-canonical Coinbase URL")
    context = ssl.create_default_context(cafile=certifi.where())
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=context), TrustedRedirectHandler()
    )
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": USER_AGENT}, method="GET"
            )
            with opener.open(request, timeout=90) as response:
                final_url = response.geturl()
                status = int(response.status)
                payload = response.read()
            if status != 200 or not _trusted_url(final_url):
                raise ReacquisitionError(
                    f"untrusted Coinbase response: status={status} url={final_url}"
                )
            return payload
        except Exception as exc:  # network boundary
            last_error = exc
            if attempt < retries:
                time.sleep(float(attempt))
    raise ReacquisitionError(f"Coinbase request failed after {retries} attempts: {last_error}")


def _finite_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def normalize(rows: list[list[Any]]) -> dict[str, Any]:
    normalized = []
    for row in rows:
        if type(row) is not list or len(row) != 6:
            raise ReacquisitionError("Coinbase SOL candle must have six fields")
        stamp, low, high, open_, close, volume = row
        day = datetime.fromtimestamp(int(stamp), tz=timezone.utc).date().isoformat()
        if START.isoformat() <= day <= END.isoformat():
            normalized.append(
                {
                    "date": day,
                    "open": _finite_number(open_),
                    "high": _finite_number(high),
                    "low": _finite_number(low),
                    "close": _finite_number(close),
                    "volume": _finite_number(volume),
                }
            )
    unique = {row["date"]: row for row in normalized}
    return {
        "schema_version": "1.0",
        "instrument": SYMBOL,
        "provider": PROVIDER,
        "adjustment": "SPOT",
        "rows": [unique[key] for key in sorted(unique)],
        "events": [],
    }


def acquire(
    output_dir: Path,
    *,
    fetcher: Callable[[str], bytes] = fetch_page,
    sleep_seconds: float = 0.05,
) -> tuple[Path, Path, bool]:
    pin = load_frozen_pin()
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows: list[list[Any]] = []
    page_receipts = []
    for page, cursor, chunk_end, url in page_requests():
        payload = fetcher(url)
        raw_path = raw_dir / f"page-{page:04d}.json"
        raw_path.write_bytes(payload)
        parsed = json.loads(payload)
        if type(parsed) is not list:
            raise ReacquisitionError(f"Coinbase SOL page {page}: list required")
        rows.extend(parsed)
        page_receipts.append(
            {
                "page_index": page,
                "cursor_in": cursor.isoformat(),
                "chunk_end": chunk_end.isoformat(),
                "endpoint_locator": url,
                "response_status": 200,
                "raw_byte_count": len(payload),
                "raw_sha256": sha256_bytes(payload),
            }
        )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    document = normalize(rows)
    candidate = canonical_json_bytes(document)
    candidate_path = output_dir / "SOL.json"
    candidate_path.write_bytes(candidate)
    actual_sha = sha256_bytes(candidate)
    dates = [row["date"] for row in document["rows"]]
    observed = {
        "row_count": len(dates),
        "first_observation": dates[0] if dates else None,
        "last_observation": dates[-1] if dates else None,
    }
    identity_match = observed == {
        "row_count": pin.row_count,
        "first_observation": pin.first_observation,
        "last_observation": pin.last_observation,
    }
    hash_match = actual_sha == pin.sha256
    receipt = {
        "schema_version": "1.0",
        "study_id": STUDY_ID,
        "purpose": "FROZEN_INPUT_RECOVERY_ONLY_NO_RESULTS_EXECUTED",
        "source_study_id": SOURCE_STUDY_ID,
        "instrument": SYMBOL,
        "provider": PROVIDER,
        "selected_path": pin.selected_path,
        "expected_sha256": pin.sha256,
        "actual_sha256": actual_sha,
        "hash_match": hash_match,
        "coverage_identity_match": identity_match,
        "expected": {
            "row_count": pin.row_count,
            "first_observation": pin.first_observation,
            "last_observation": pin.last_observation,
        },
        "observed": observed,
        "page_count": len(page_receipts),
        "pages": page_receipts,
        "no_registered_results_executed": True,
    }
    receipt_path = output_dir / "receipt.json"
    receipt_path.write_bytes(canonical_json_bytes(receipt))
    return candidate_path, receipt_path, hash_match and identity_match


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        candidate, receipt, verified = acquire(args.output_dir)
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "1.0",
            "study_id": STUDY_ID,
            "purpose": "FROZEN_INPUT_RECOVERY_ONLY_NO_RESULTS_EXECUTED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "no_registered_results_executed": True,
        }
        failure_path = args.output_dir / "failure.json"
        failure_path.write_bytes(canonical_json_bytes(failure))
        print(f"failure={failure_path}")
        print("verified=false")
        return 3
    print(f"candidate={candidate}")
    print(f"receipt={receipt}")
    print(f"verified={str(verified).lower()}")
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
