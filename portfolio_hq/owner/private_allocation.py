"""Offline bridge from confirmed private evidence to the canonical allocator.

The caller must name every evidence version.  This module neither retrieves
broker data nor writes state; it reconstructs retained bytes, validates a small
supplement, and calls :func:`allocate.plan` with in-memory observations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

import allocate
from portfolio_hq.owner import account_staging

SCHEMA_VERSION = 1
MAX_SUPPLEMENT_BYTES = 512 * 1024
FRESH_SECONDS = 2 * 86400
POLICY_FILES = ("targets.yaml", "gates.yaml", "issuer_lookthrough.yaml")


class AllocationEvidenceError(ValueError):
    """The named evidence cannot support an actionable allocation result."""


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise AllocationEvidenceError(f"{label} must be an explicit ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError as exc:
        raise AllocationEvidenceError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise AllocationEvidenceError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _finite(value: Any, label: str, low: float = 0.0, high: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise AllocationEvidenceError(f"{label} must be a finite number")
    result = float(value)
    if result < low or (high is not None and result > high):
        raise AllocationEvidenceError(f"{label} is outside [{low}, {high}]")
    return result


def _fresh(value: Any, label: str, as_of: datetime) -> str:
    original = value
    observed = _parse_timestamp(value, label)
    age = (as_of - observed).total_seconds()
    if age < 0:
        raise AllocationEvidenceError(f"{label} is in the future")
    if age > FRESH_SECONDS:
        raise AllocationEvidenceError(f"{label} is stale (> 2 days)")
    return original


def _json(data: bytes) -> dict:
    if not data or len(data) > MAX_SUPPLEMENT_BYTES:
        raise AllocationEvidenceError("supplement is empty or exceeds 512 KiB")
    try:
        # Reuse the staging boundary's duplicate-key, non-finite-number and
        # exact UTF-8 rules rather than creating a looser second JSON parser.
        doc = account_staging._parse_json(data)
    except (account_staging.AccountSubmissionRejected, UnicodeDecodeError,
            ValueError, RecursionError) as exc:
        raise AllocationEvidenceError("supplement must be valid UTF-8 JSON") from exc
    if not isinstance(doc, dict):
        raise AllocationEvidenceError("supplement must be a JSON object")
    return doc


def _policy(source_root: Path, expected_sha: str) -> tuple[dict, dict, dict, dict]:
    root = source_root.resolve()
    hashes = {}
    for name in POLICY_FILES:
        path = root / name
        if not path.is_file() or path.resolve().parent != root:
            raise AllocationEvidenceError(f"required policy file unavailable: {name}")
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        sha = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
            capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AllocationEvidenceError("source root is not an identified Git checkout") from exc
    if sha != expected_sha:
        raise AllocationEvidenceError(f"source SHA mismatch: expected {expected_sha}, found {sha}")
    targets = allocate.load_yaml(root / "targets.yaml")
    gates = allocate.load_gates(root / "gates.yaml")
    lookthrough = allocate.load_issuer_lookthrough(root / "issuer_lookthrough.yaml")
    return targets, gates, lookthrough, {"source_root": str(root), "git_sha": sha,
                                        "files_sha256": hashes}


def run(runtime_root: Path | str, supplement_bytes: bytes, *, source_root: Path | str,
        expected_source_sha: str) -> dict:
    """Return a provenance envelope containing the real ``allocate.plan`` result.

    Errors are returned as a controlled, non-actionable envelope.  In
    particular, no current-looking dependent dollar fields are synthesized.
    """
    supplement_hash = hashlib.sha256(supplement_bytes).hexdigest()
    try:
        doc = _json(supplement_bytes)
        allowed = {"schema_version", "as_of", "submission_id", "receipt_sha256",
                   "review_id", "reviewer", "buffer", "market", "earnings", "regime"}
        if (set(doc) not in (allowed, allowed - {"buffer"}) or
                doc.get("schema_version") != SCHEMA_VERSION):
            raise AllocationEvidenceError("supplement must use schema_version 1 and only documented fields")
        as_of = _parse_timestamp(doc["as_of"], "as_of")
        snap = account_staging.snapshot(runtime_root)
        matches = [r for r in snap.records if r["submission_id"] == doc["submission_id"]]
        if len(matches) != 1:
            raise AllocationEvidenceError("expected submission is absent or its binding is invalid")
        receipt = matches[0]
        receipt_path = (Path(runtime_root) / account_staging.SUBMISSIONS_DIRNAME /
                        doc["submission_id"] / account_staging.RECEIPT_FILENAME)
        receipt_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        if receipt_hash != doc["receipt_sha256"]:
            raise AllocationEvidenceError("expected receipt identity does not match retained bytes")
        reviews = receipt["reviews"]
        selected = [r for r in reviews if r["review_id"] == doc["review_id"]]
        if len(selected) != 1 or selected[0]["reviewer"] != doc["reviewer"]:
            raise AllocationEvidenceError("expected review identity/reviewer is absent")
        if selected[0]["decision"] != "confirmed":
            raise AllocationEvidenceError("expected review rejected this version")
        if reviews[-1]["review_id"] != doc["review_id"] or any(
                r["decision"] != "confirmed" for r in reviews):
            raise AllocationEvidenceError("expected review is conflicting or superseded")
        original = snap.originals[doc["submission_id"]]
        normalized, issues = account_staging.validate(original)
        if issues:
            raise AllocationEvidenceError("confirmed submission unexpectedly has material issues")

        targets, gates, lookthrough, policy = _policy(Path(source_root), expected_source_sha)
        roster = allocate.build_roster(targets)
        currencies = {row["currency"] for key in ("cash", "debt_margin")
                      for row in normalized[key]}
        currencies |= {h["valuation"]["currency"] for h in normalized["holdings"]
                       if h["valuation"] is not None and h["quantity"] != 0}
        if currencies != {"USD"}:
            raise AllocationEvidenceError(
                "cross-currency evidence is unavailable: no FX conversion is authorized")
        if len(normalized["cash"]) != 1 or len(normalized["debt_margin"]) != 1:
            raise AllocationEvidenceError("exactly one cash and one debt observation are required")
        for section in ("cash", "debt_margin"):
            row = normalized[section][0]
            if row["freshness"] != "current":
                raise AllocationEvidenceError(f"{section} freshness is not current")
            _fresh(row["observed_at"], f"{section}.observed_at", as_of)

        buffer = doc.get("buffer")
        buffer_pct = None
        if buffer is not None:
            if not isinstance(buffer, dict) or set(buffer) != {"percentage", "currency", "observed_at", "source_id"}:
                raise AllocationEvidenceError("buffer must contain percentage, currency, observed_at, source_id")
            buffer_pct = _finite(buffer["percentage"], "buffer.percentage", high=100.0)
            if buffer["currency"] != "USD" or not isinstance(buffer["source_id"], str) or not buffer["source_id"]:
                raise AllocationEvidenceError("buffer currency/source_id is invalid")
            _fresh(buffer["observed_at"], "buffer.observed_at", as_of)

        holdings, shares = {}, {}
        observation_provenance = []
        for index, h in enumerate(normalized["holdings"]):
            qty = _finite(h["quantity"], f"holdings[{index}].quantity")
            shares[h["ticker"]] = qty
            if qty == 0:
                continue
            if h["freshness"] != "current" or h["valuation"] is None or h["valuation"]["freshness"] != "current":
                raise AllocationEvidenceError(f"{h['ticker']} has an unavailable required valuation")
            _fresh(h["observed_at"], f"{h['ticker']}.observed_at", as_of)
            _fresh(h["valuation"]["observed_at"], f"{h['ticker']}.valuation.observed_at", as_of)
            holdings[h["ticker"]] = qty * _finite(h["valuation"]["unit_price"], f"{h['ticker']}.unit_price")
            observation_provenance.append({"ticker": h["ticker"], "quantity_observed_at": h["observed_at"],
                                           "valuation_observed_at": h["valuation"]["observed_at"],
                                           "currency": h["valuation"]["currency"]})

        market_doc = doc["market"]
        if not isinstance(market_doc, list):
            raise AllocationEvidenceError("market must be a list")
        metrics = {}
        for i, row in enumerate(market_doc):
            if not isinstance(row, dict) or set(row) != {"ticker", "price", "sma200", "rsi14", "currency", "observed_at", "source_id"}:
                raise AllocationEvidenceError(f"market[{i}] has an invalid shape")
            tk = row["ticker"]
            if tk in metrics or tk not in roster or row["currency"] != "USD":
                raise AllocationEvidenceError(f"market[{i}] has duplicate, non-roster, or non-USD identity")
            _fresh(row["observed_at"], f"market[{i}].observed_at", as_of)
            metrics[tk] = {k: _finite(row[k], f"market[{i}].{k}") for k in ("price", "sma200", "rsi14")}
        required_market = {tk for tk, meta in roster.items()
                           if meta["asset_class"] not in {"crypto", "cash", "reserve"}}
        if metrics.keys() != required_market:
            raise AllocationEvidenceError("market evidence must cover every non-crypto market roster ticker exactly")

        earnings_doc = doc["earnings"]
        if not isinstance(earnings_doc, list):
            raise AllocationEvidenceError("earnings must be a list")
        earnings = {}
        for i, row in enumerate(earnings_doc):
            if not isinstance(row, dict) or set(row) != {"ticker", "next_date", "observed_at", "source_id"}:
                raise AllocationEvidenceError(f"earnings[{i}] has an invalid shape")
            tk = row["ticker"]
            if tk in earnings or tk not in required_market:
                raise AllocationEvidenceError(f"earnings[{i}] has an invalid identity")
            _fresh(row["observed_at"], f"earnings[{i}].observed_at", as_of)
            if row["next_date"] is not None:
                try:
                    next_date = date.fromisoformat(row["next_date"])
                except (TypeError, ValueError) as exc:
                    raise AllocationEvidenceError(f"earnings[{i}].next_date is invalid") from exc
                earnings[tk] = (next_date - as_of.date()).days
            else:
                earnings[tk] = None  # canonically allowed, disclosed unknown
        if earnings.keys() != required_market:
            raise AllocationEvidenceError("earnings evidence must cover every non-crypto market roster ticker exactly")

        regime = doc["regime"]
        if not isinstance(regime, dict) or set(regime) != {"ok", "known", "observed_at", "source_id"}:
            raise AllocationEvidenceError("regime has an invalid shape")
        if type(regime["ok"]) is not bool or type(regime["known"]) is not bool:
            raise AllocationEvidenceError("regime ok/known must be Boolean")
        _fresh(regime["observed_at"], "regime.observed_at", as_of)

        cash_row, debt_row = normalized["cash"][0], normalized["debt_margin"][0]
        holdings_state = {"shares": shares, "crypto_shares": {},
                          "cash": {"balance": cash_row["balance"],
                                   "synced_at": cash_row["observed_at"]},
                          "margin": {"debt": debt_row["balance"], "buffer_pct": buffer_pct,
                                     "synced_at": debt_row["observed_at"]}}
        cash_state = allocate.load_cash_state(holdings_state, as_of=as_of.date())
        margin_state = allocate.load_margin_state(holdings_state, as_of=as_of.date())
        valuation = allocate.valuation_completeness(holdings, holdings_state)
        availability = allocate.current_dollar_availability(cash_state, margin_state, valuation)
        result = allocate.plan(
            targets, holdings, roster, metrics, regime["ok"], regime["known"],
            cash_state["balance"], margin_debt=debt_row["balance"],
            margin_buffer_pct=buffer_pct, gates_cfg=gates,
            lookthrough=lookthrough, holdings_state=holdings_state,
            dollars_available=availability["available"], earnings_provider=earnings.get,
            as_of=as_of)
        return {"actionable": bool(result["dollars_available"]),
                "blocked_reasons": availability["blocked_by"],
                "as_of": doc["as_of"], "canonical_result": result,
                "provenance": {"submission_id": doc["submission_id"],
                    "submission_sha256": receipt["submission_sha256"],
                    "receipt_sha256": receipt_hash, "review_id": doc["review_id"],
                    "reviewer": doc["reviewer"], "supplement_sha256": supplement_hash,
                    "policy": policy, "observations": observation_provenance,
                    "buffer": buffer, "market": market_doc, "earnings": earnings_doc,
                    "regime": regime},
                "discrepancies": ["protected_capital submission rows are retained evidence but are not inferred as allocator reserve"],
                "limitations": ["recommendations only; no orders", "no broker retrieval or network access",
                                "unknown earnings is disclosed by the canonical result"]}
    except (AllocationEvidenceError, account_staging.AccountStorageError,
            account_staging.AccountSubmissionRejected, KeyError, TypeError, ValueError) as exc:
        return {"actionable": False, "blocked_reasons": [str(exc)], "as_of": None,
                "canonical_result": None, "provenance": {"supplement_sha256": supplement_hash},
                "discrepancies": [], "limitations": ["No dependent dollar result is available."]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline private confirmed-evidence allocation adapter")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--supplement", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--expected-source-sha", required=True)
    args = parser.parse_args(argv)
    output = run(args.runtime_root, args.supplement.read_bytes(), source_root=args.source_root,
                 expected_source_sha=args.expected_source_sha)
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0 if output["actionable"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
