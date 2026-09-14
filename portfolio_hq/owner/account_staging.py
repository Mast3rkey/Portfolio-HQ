"""Private, immutable staging for manually supplied account observations.

This module stores exact client bytes below one explicitly configured runtime
root.  It does not import portfolio or allocation code and cannot adopt the
observations it receives.  A review is an immutable annotation bound to the
submission and receipt bytes; it is not engineering approval or authority to
trade.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import secrets
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

SCHEMA_VERSION = 1
MAX_SUBMISSION_BYTES = 2 * 1024 * 1024
MAX_RECEIPT_BYTES = 128 * 1024
MAX_REVIEW_BYTES = 64 * 1024
MAX_ITEMS = 512
SUBMISSIONS_DIRNAME = "submissions"
STAGING_DIRNAME = ".incoming"
SUBMISSION_FILENAME = "submission.json"
RECEIPT_FILENAME = "receipt.json"
REVIEWS_DIRNAME = "reviews"

_ID_RE = re.compile(r"\A[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}\Z")
_CLIENT_ID_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_TICKER_RE = re.compile(r"\A[A-Z0-9][A-Z0-9.\-]{0,15}\Z")
_CURRENCY_RE = re.compile(r"\A[A-Z]{3}\Z")
_SHA256_RE = re.compile(r"\A[0-9a-f]{64}\Z")
_AUTHORITY_ITEMS = (("data_only", True), ("policy_adopted", False),
                    ("engineering_approved", False), ("executable", False))
_REVIEW_MEANING = (
    "data confirmation only; not engineering approval, policy adoption, or executable authority"
)


class AccountSubmissionRejected(ValueError):
    pass


class AccountStorageError(RuntimeError):
    pass


class AccountReviewRejected(ValueError):
    pass


class Snapshot(NamedTuple):
    records: tuple[dict, ...]
    originals: dict[str, bytes]


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AccountSubmissionRejected(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise AccountSubmissionRejected(f"non-finite JSON number: {value}")


def _parse_json(data: bytes) -> dict:
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
    except AccountSubmissionRejected:
        raise
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise AccountSubmissionRejected("submission must be valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise AccountSubmissionRejected("submission must be a JSON object")
    return value


def _text(value, label: str, *, pattern=None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AccountSubmissionRejected(f"{label} must be non-empty text")
    value = value.strip()
    if pattern and not pattern.fullmatch(value):
        raise AccountSubmissionRejected(f"{label} has an invalid format")
    return value


def _number(value, label: str, *, nonnegative: bool = True) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AccountSubmissionRejected(f"{label} must be a finite number, not Boolean")
    try:
        finite = math.isfinite(value)
    except OverflowError as exc:
        raise AccountSubmissionRejected(
            f"{label} is outside the supported finite numeric range") from exc
    if not finite:
        raise AccountSubmissionRejected(f"{label} must be a finite number, not Boolean")
    if nonnegative and value < 0:
        raise AccountSubmissionRejected(f"{label} must not be negative")
    return value


def _timestamp(value, label: str) -> str:
    text = _text(value, label)
    candidate = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise AccountSubmissionRejected(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise AccountSubmissionRejected(f"{label} must include a timezone")
    return text


def _freshness(value, label: str) -> str:
    value = _text(value, label)
    if value not in {"current", "stale", "unknown"}:
        raise AccountSubmissionRejected(f"{label} must be current, stale, or unknown")
    return value


def _list(value, label: str) -> list:
    if not isinstance(value, list) or len(value) > MAX_ITEMS:
        raise AccountSubmissionRejected(f"{label} must be a list of at most {MAX_ITEMS} items")
    return value


def validate(data: bytes) -> tuple[dict, list[dict]]:
    """Validate exact submission bytes and return normalized display data/issues."""
    if not data:
        raise AccountSubmissionRejected("submission is empty")
    if len(data) > MAX_SUBMISSION_BYTES:
        raise AccountSubmissionRejected("submission exceeds the 2 MiB limit")
    doc = _parse_json(data)
    if doc.get("schema_version") != SCHEMA_VERSION or isinstance(doc.get("schema_version"), bool):
        raise AccountSubmissionRejected("schema_version must be 1")
    client_id = _text(doc.get("client_submission_id"), "client_submission_id",
                      pattern=_CLIENT_ID_RE)
    submitted_at = _timestamp(doc.get("submitted_at"), "submitted_at")
    issues: list[dict] = []
    normalized = {"schema_version": 1, "client_submission_id": client_id,
                  "submitted_at": submitted_at, "holdings": [], "cash": [],
                  "debt_margin": [], "protected_capital": []}

    holdings = _list(doc.get("holdings"), "holdings")
    seen = set()
    for index, item in enumerate(holdings):
        if not isinstance(item, dict):
            raise AccountSubmissionRejected(f"holdings[{index}] must be an object")
        ticker = _text(item.get("ticker"), f"holdings[{index}].ticker", pattern=_TICKER_RE)
        if ticker in seen:
            raise AccountSubmissionRejected(f"duplicate holding identity: {ticker}")
        seen.add(ticker)
        row = {"ticker": ticker,
               "quantity": _number(item.get("quantity"), f"holdings[{index}].quantity"),
               "observed_at": _timestamp(item.get("observed_at"), f"holdings[{index}].observed_at"),
               "freshness": _freshness(item.get("freshness"), f"holdings[{index}].freshness")}
        valuation = item.get("valuation")
        if valuation is None:
            row["valuation"] = None
            issues.append({"severity": "material", "code": "missing_valuation",
                           "message": f"{ticker} has quantity but no dated valuation observation."})
        elif isinstance(valuation, dict):
            row["valuation"] = {
                "unit_price": _number(valuation.get("unit_price"), f"{ticker}.valuation.unit_price"),
                "currency": _text(valuation.get("currency"), f"{ticker}.valuation.currency",
                                  pattern=_CURRENCY_RE),
                "observed_at": _timestamp(valuation.get("observed_at"), f"{ticker}.valuation.observed_at"),
                "freshness": _freshness(valuation.get("freshness"), f"{ticker}.valuation.freshness"),
            }
        else:
            raise AccountSubmissionRejected(f"{ticker}.valuation must be an object or null")
        if row["freshness"] == "stale" or (row["valuation"] and row["valuation"]["freshness"] == "stale"):
            issues.append({"severity": "material", "code": "stale_holding",
                           "message": f"{ticker} is explicitly marked stale."})
        normalized["holdings"].append(row)

    section_specs = (
        ("cash", "account_id", "balance", False),
        ("debt_margin", "account_id", "balance", False),
        ("protected_capital", "evidence_id", "amount", True),
    )
    for section, identity_key, amount_key, require_basis in section_specs:
        identities = set()
        for index, item in enumerate(_list(doc.get(section), section)):
            if not isinstance(item, dict):
                raise AccountSubmissionRejected(f"{section}[{index}] must be an object")
            identity = _text(item.get(identity_key), f"{section}[{index}].{identity_key}",
                             pattern=_CLIENT_ID_RE)
            if identity in identities:
                raise AccountSubmissionRejected(f"duplicate {section} identity: {identity}")
            identities.add(identity)
            row = {identity_key: identity,
                   amount_key: _number(item.get(amount_key), f"{section}[{index}].{amount_key}"),
                   "currency": _text(item.get("currency"), f"{section}[{index}].currency",
                                     pattern=_CURRENCY_RE),
                   "observed_at": _timestamp(item.get("observed_at"), f"{section}[{index}].observed_at"),
                   "freshness": _freshness(item.get("freshness"), f"{section}[{index}].freshness")}
            if require_basis:
                row["basis"] = _text(item.get("basis"), f"{section}[{index}].basis")
            if row["freshness"] == "stale":
                issues.append({"severity": "material", "code": f"stale_{section}",
                               "message": f"{section} observation {identity} is explicitly marked stale."})
            normalized[section].append(row)

    for section in ("holdings", "cash", "debt_margin", "protected_capital"):
        if not normalized[section]:
            issues.append({"severity": "material", "code": f"missing_{section}",
                           "message": f"No {section.replace('_', ' ')} observations were supplied; unavailable remains unavailable."})
    return normalized, issues


def _root(runtime_root: Path | str, *, create: bool) -> Path:
    root = Path(os.path.realpath(Path(runtime_root)))
    child = root / SUBMISSIONS_DIRNAME
    if os.path.islink(child):
        raise AccountStorageError("account submissions directory is a symbolic link")
    if create:
        try:
            child.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise AccountStorageError(
                "could not create the account submissions directory") from exc
    try:
        available = child.is_dir() and os.path.realpath(child) == str(child)
    except OSError as exc:
        raise AccountStorageError(
            "could not inspect the account submissions directory") from exc
    if not available:
        raise AccountStorageError("account submissions directory is unavailable or redirected")
    return child


def _new_id() -> str:
    return f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(6)}"


def _dir(runtime_root, submission_id: str) -> Path:
    if not isinstance(submission_id, str) or not _ID_RE.fullmatch(submission_id):
        raise ValueError("invalid submission id")
    return _root(runtime_root, create=False) / submission_id


def ingest(runtime_root: Path | str, data: bytes) -> dict:
    normalized, issues = validate(data)
    root = _root(runtime_root, create=True)
    digest = hashlib.sha256(data).hexdigest()
    if normalized["client_submission_id"] in _existing_client_ids(runtime_root):
        raise AccountSubmissionRejected(
            "client_submission_id was already used; changed content requires a new identity")
    submission_id = _new_id()
    receipt = {"schema_version": 1, "submission_id": submission_id,
               "client_submission_id": normalized["client_submission_id"],
               "received_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
               "submission_sha256": digest, "byte_size": len(data),
               "normalized": normalized, "issues": issues,
               "state": "awaiting_review", "authority": dict(_AUTHORITY_ITEMS)}
    receipt_bytes = (json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n").encode()
    if len(receipt_bytes) > MAX_RECEIPT_BYTES:
        raise AccountSubmissionRejected(
            "validated submission would produce a receipt larger than the supported bound")
    staging_root = root.parent / STAGING_DIRNAME
    if os.path.islink(staging_root):
        raise AccountStorageError("account staging directory is a symbolic link")
    try:
        staging_root.mkdir(mode=0o700, exist_ok=True)
        staging_redirected = os.path.realpath(staging_root) != str(staging_root)
    except OSError as exc:
        raise AccountStorageError(
            "could not create or inspect the account staging directory") from exc
    if staging_redirected:
        raise AccountStorageError("account staging directory is redirected")
    staging = staging_root / submission_id
    final = root / submission_id
    try:
        staging.mkdir(mode=0o700)
        (staging / SUBMISSION_FILENAME).write_bytes(data)
        (staging / RECEIPT_FILENAME).write_bytes(receipt_bytes)
        (staging / REVIEWS_DIRNAME).mkdir(mode=0o700)
        os.replace(staging, final)
        return receipt
    except (OSError, FileExistsError) as exc:
        shutil.rmtree(staging, ignore_errors=True)
        raise AccountStorageError("account submission could not be stored atomically") from exc


def _bounded(path: Path, limit: int) -> bytes | None:
    try:
        with path.open("rb") as handle:
            data = handle.read(limit + 1)
    except OSError:
        return None
    return data if len(data) <= limit else None


def _safe_regular_file(path: Path) -> bool:
    """Prove a read candidate is a non-redirected regular file before open."""
    try:
        mode = path.stat(follow_symlinks=False).st_mode
    except OSError:
        return False
    return (not os.path.islink(path) and stat.S_ISREG(mode)
            and os.path.realpath(path) == str(path))


def _existing_client_ids(runtime_root: Path | str) -> set[str]:
    """Recover identities from retained originals, never mutable receipt claims.

    Once a server-identified entry exists, inability to reconstruct its original
    is ambiguous rather than evidence that an identity is free. Fail closed so
    damaged storage cannot authorize a duplicate submission.
    """
    try:
        root = _root(runtime_root, create=False)
        entries = tuple(root.iterdir())
    except AccountStorageError:
        raise
    except OSError as exc:
        raise AccountStorageError(
            "could not enumerate retained account identities") from exc
    identities = set()
    for entry in entries:
        if not _ID_RE.fullmatch(entry.name):
            continue
        if os.path.islink(entry) or not entry.is_dir() \
                or os.path.realpath(entry) != str(entry):
            raise AccountStorageError(
                "cannot prove a retained account identity is unused: entry is redirected or nonregular")
        path = entry / SUBMISSION_FILENAME
        data = _bounded(path, MAX_SUBMISSION_BYTES) if _safe_regular_file(path) else None
        if data is None:
            raise AccountStorageError(
                "cannot prove a retained account identity is unused: original is unavailable")
        try:
            normalized, _ = validate(data)
        except AccountSubmissionRejected as exc:
            raise AccountStorageError(
                "cannot prove a retained account identity is unused: original is invalid") from exc
        identities.add(normalized["client_submission_id"])
    return identities


def _valid_receipt(receipt: object, normalized: dict, issues: list[dict],
                   submission_id: str, original: bytes) -> bool:
    expected_keys = {"schema_version", "submission_id", "client_submission_id",
                     "received_at", "submission_sha256", "byte_size", "normalized",
                     "issues", "state", "authority"}
    return (isinstance(receipt, dict) and set(receipt) == expected_keys
            and type(receipt.get("schema_version")) is int
            and receipt["schema_version"] == SCHEMA_VERSION
            and receipt.get("submission_id") == submission_id
            and receipt.get("client_submission_id") == normalized["client_submission_id"]
            and _valid_timestamp(receipt.get("received_at"))
            and type(receipt.get("byte_size")) is int
            and receipt["byte_size"] == len(original)
            and isinstance(receipt.get("submission_sha256"), str)
            and bool(_SHA256_RE.fullmatch(receipt["submission_sha256"]))
            and receipt["submission_sha256"] == hashlib.sha256(original).hexdigest()
            and _same_json_value(receipt.get("normalized"), normalized)
            and _same_json_value(receipt.get("issues"), issues)
            and receipt.get("state") == "awaiting_review"
            and _same_json_value(receipt.get("authority"), dict(_AUTHORITY_ITEMS)))


def _valid_timestamp(value: object) -> bool:
    try:
        _timestamp(value, "timestamp")
    except AccountSubmissionRejected:
        return False
    return True


def _same_json_value(left: object, right: object) -> bool:
    """Compare JSON trees without Python's Boolean/integer coercion.

    Python considers ``False == 0`` and ``True == 1``. Persisted evidence may
    not use that convenience because its JSON types are part of the receipt
    schema. Canonical JSON keeps those types distinct while preserving the
    legitimate input distinction between an explicitly supplied ``0`` and
    ``0.0``.
    """
    try:
        return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
            right, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError):
        return False


def _verified(runtime_root, submission_id: str):
    try:
        directory = _dir(runtime_root, submission_id)
    except (ValueError, AccountStorageError):
        return None
    if os.path.islink(directory) or os.path.realpath(directory) != str(directory):
        return None
    original_path = directory / SUBMISSION_FILENAME
    receipt_path = directory / RECEIPT_FILENAME
    if not all(_safe_regular_file(path) for path in (original_path, receipt_path)):
        return None
    original = _bounded(original_path, MAX_SUBMISSION_BYTES)
    receipt_bytes = _bounded(receipt_path, MAX_RECEIPT_BYTES)
    if original is None or receipt_bytes is None:
        return None
    try:
        receipt = json.loads(receipt_bytes, object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, UnicodeDecodeError, RecursionError):
        return None
    try:
        normalized, issues = validate(original)
    except AccountSubmissionRejected:
        return None
    if not _valid_receipt(receipt, normalized, issues, submission_id, original):
        return None
    return directory, original, receipt_bytes, receipt


def snapshot(runtime_root: Path | str) -> Snapshot:
    try:
        root = _root(runtime_root, create=False)
    except AccountStorageError:
        return Snapshot((), {})
    records, originals = [], {}
    for entry in sorted(root.iterdir(), reverse=True):
        if not entry.is_dir() or not _ID_RE.fullmatch(entry.name):
            continue
        verified = _verified(runtime_root, entry.name)
        if verified is None:
            continue
        directory, original, receipt_bytes, receipt = verified
        reviews = []
        review_root = directory / REVIEWS_DIRNAME
        if review_root.is_dir() and not os.path.islink(review_root):
            for path in sorted(review_root.iterdir()):
                data = _bounded(path, MAX_REVIEW_BYTES) if _safe_regular_file(path) else None
                if not data:
                    continue
                try:
                    review = json.loads(data, object_pairs_hook=_pairs, parse_constant=_constant)
                except (ValueError, UnicodeDecodeError, RecursionError):
                    continue
                if _valid_review(review, path, receipt, receipt_bytes):
                    reviews.append(review)
        shown = dict(receipt)
        shown["reviews"] = reviews
        records.append(shown)
        originals[entry.name] = original
    return Snapshot(tuple(records), originals)


def _valid_review(review: object, path: Path, receipt: dict,
                  receipt_bytes: bytes) -> bool:
    expected_keys = {"schema_version", "review_id", "submission_id", "decision",
                     "reviewer", "reviewed_at", "submission_sha256", "receipt_sha256",
                     "meaning"}
    if not isinstance(review, dict) or set(review) != expected_keys:
        return False
    review_id = review.get("review_id")
    decision = review.get("decision")
    reviewer = review.get("reviewer")
    material = any(item.get("severity") == "material" for item in receipt["issues"])
    return (type(review.get("schema_version")) is int
            and review["schema_version"] == SCHEMA_VERSION
            and isinstance(review_id, str) and bool(_ID_RE.fullmatch(review_id))
            and path.name == f"{review_id}.json"
            and review.get("submission_id") == receipt["submission_id"]
            and isinstance(decision, str) and decision in {"confirmed", "rejected"}
            and not (decision == "confirmed" and material)
            and isinstance(reviewer, str) and bool(_CLIENT_ID_RE.fullmatch(reviewer))
            and _valid_timestamp(review.get("reviewed_at"))
            and review.get("submission_sha256") == receipt["submission_sha256"]
            and review.get("receipt_sha256") == hashlib.sha256(receipt_bytes).hexdigest()
            and review.get("meaning") == _REVIEW_MEANING)


def review(runtime_root: Path | str, submission_id: str, decision: object,
           reviewer: str) -> dict:
    if not isinstance(decision, str) or decision not in {"confirmed", "rejected"}:
        raise AccountReviewRejected("decision must be confirmed or rejected")
    try:
        reviewer = _text(reviewer, "reviewer", pattern=_CLIENT_ID_RE)
    except AccountSubmissionRejected as exc:
        raise AccountReviewRejected(str(exc)) from exc
    verified = _verified(runtime_root, submission_id)
    if verified is None:
        raise AccountReviewRejected("submission or receipt binding is invalid")
    directory, original, receipt_bytes, receipt = verified
    if decision == "confirmed" and any(i.get("severity") == "material" for i in receipt["issues"]):
        raise AccountReviewRejected("material discrepancies remain unresolved; this exact version cannot be confirmed")
    review_id = _new_id()
    record = {"schema_version": 1, "review_id": review_id,
              "submission_id": submission_id, "decision": decision,
              "reviewer": reviewer,
              "reviewed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
              "submission_sha256": hashlib.sha256(original).hexdigest(),
              "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
              "meaning": _REVIEW_MEANING}
    path = directory / REVIEWS_DIRNAME / f"{review_id}.json"
    review_root = directory / REVIEWS_DIRNAME
    if os.path.islink(review_root) or os.path.realpath(review_root) != str(review_root):
        raise AccountStorageError("review history directory is redirected")
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(record, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
    except OSError as exc:
        raise AccountStorageError("review could not be stored immutably") from exc
    return record


def original(runtime_root: Path | str, submission_id: str) -> bytes | None:
    verified = _verified(runtime_root, submission_id)
    return verified[1] if verified else None
