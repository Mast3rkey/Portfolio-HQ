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
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from types import CodeType, FunctionType
from typing import Any

import yaml

import allocate
import earnings
import level1_policy_summary
import margin_state
from portfolio_hq.owner import account_staging

SCHEMA_VERSION = 1
MAX_SUPPLEMENT_BYTES = 512 * 1024
FRESH_SECONDS = 2 * 86400
POLICY_FILES = ("targets.yaml", "gates.yaml", "issuer_lookthrough.yaml")
EXECUTION_FILES = ("allocate.py", "earnings.py", "level1_policy_summary.py",
                   "margin_state.py",
                   "portfolio_hq/owner/account_staging.py",
                   "portfolio_hq/owner/private_allocation.py")
# CPython sets CO_OPTIMIZED on function bodies but not on class bodies, which
# are also module-level code constants.  It is the discriminator used below.
CO_OPTIMIZED = 0x1


class AllocationEvidenceError(ValueError):
    """The named evidence cannot support an actionable allocation result."""


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise AllocationEvidenceError(f"{label} must be an explicit ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except (OverflowError, ValueError) as exc:
        raise AllocationEvidenceError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise AllocationEvidenceError(f"{label} must include a timezone")
    try:
        return parsed.astimezone(timezone.utc)
    except (OverflowError, ValueError) as exc:
        raise AllocationEvidenceError(f"{label} is outside the supported timestamp range") from exc


def _observation_age(value: Any, label: str, as_of: datetime) -> tuple[str, float]:
    """Return original precision and age; date-only values use calendar days."""
    if isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        try:
            observed = date.fromisoformat(value)
        except ValueError as exc:
            raise AllocationEvidenceError(
                f"{label} must be an ISO-8601 date or timezone-aware timestamp") from exc
        if observed.isoformat() != value:
            raise AllocationEvidenceError(f"{label} must be a canonical ISO-8601 date")
        return value, float((as_of.date() - observed).days)
    observed = _parse_timestamp(value, label)
    try:
        return value, (as_of - observed).total_seconds() / 86400
    except OverflowError as exc:
        raise AllocationEvidenceError(f"{label} is outside the supported timestamp range") from exc


def _finite(value: Any, label: str, low: float = 0.0, high: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AllocationEvidenceError(f"{label} must be a finite number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise AllocationEvidenceError(f"{label} must be a finite number") from exc
    if not math.isfinite(result):
        raise AllocationEvidenceError(f"{label} must be a finite number")
    if result < low or (high is not None and result > high):
        raise AllocationEvidenceError(f"{label} is outside [{low}, {high}]")
    return result


def _fresh(value: Any, label: str, as_of: datetime) -> str:
    original, age_days = _observation_age(value, label, as_of)
    age = age_days * 86400
    if age < 0:
        raise AllocationEvidenceError(f"{label} is in the future")
    if age > FRESH_SECONDS:
        raise AllocationEvidenceError(f"{label} is stale (> 2 days)")
    return original


def _informational_age(value: Any, label: str, as_of: datetime) -> float:
    """Validate identity/time but allow genuinely old informational evidence."""
    _, age = _observation_age(value, label, as_of)
    if age < 0:
        raise AllocationEvidenceError(f"{label} is in the future")
    return age


def _observation_date(value: str, label: str) -> date:
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return date.fromisoformat(value)
    return _parse_timestamp(value, label).date()


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


def _git(root: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    try:
        return subprocess.run(["git", "-C", str(root), *args], input=input_bytes,
                              check=True, capture_output=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AllocationEvidenceError("identified source could not be verified by Git") from exc


def _defined_functions(source: bytes, name: str) -> dict[str, CodeType]:
    """Module-level ``def`` code objects compiled from the verified bytes.

    Nested defs and closures need no separate entry: code objects compare by
    value and that comparison recurses through ``co_consts``, so tampering
    inside an inner function still changes its enclosing function's code.
    """
    try:
        module_code = compile(source, name, "exec", dont_inherit=True)
    except (SyntaxError, ValueError) as exc:
        raise AllocationEvidenceError(f"verified source does not compile: {name}") from exc
    # Later definitions shadow earlier ones, matching import-time semantics.
    return {const.co_name: const for const in module_code.co_consts
            if isinstance(const, CodeType) and const.co_flags & CO_OPTIMIZED}


def _verify_loaded_code(consumed: dict[str, bytes]) -> None:
    """Bind the in-memory callables to the named commit, not just the disk.

    Matching on-disk bytes cannot show that the *loaded* code came from them.
    A long-lived process may hold modules imported before the checkout moved,
    or replaced in memory afterwards, and would otherwise publish a result
    produced by different code under ``expected_source_sha``.  Every
    module-level function the commit defines must therefore still be present
    and byte-identical in compiled code.

    Scope is deliberately the functions these files *define*.  Names merely
    imported into them are covered only by the shared-root check in
    :func:`_source_bytes` and are disclosed as a limitation; the adapter
    injects the market metrics and the earnings provider, so the two live
    data paths are not consulted for this result either way.

    In-process self-verification is irreducibly partial at exactly two
    points: replacing ``run`` or this function itself removes the check
    before it can run.  Everything else in these files, including the
    retained-review validators and the rest of this module, is covered --
    :func:`run` performs this check before it judges any evidence.
    """
    modules = {"allocate.py": allocate, "earnings.py": earnings,
               "level1_policy_summary.py": level1_policy_summary,
               "margin_state.py": margin_state,
               "portfolio_hq/owner/account_staging.py": account_staging,
               "portfolio_hq/owner/private_allocation.py": sys.modules[__name__]}
    if set(modules) != set(EXECUTION_FILES):
        raise AllocationEvidenceError("executing dependency binding is incomplete")
    for name, module in modules.items():
        for attr, expected in _defined_functions(consumed[name], name).items():
            loaded = getattr(module, attr, None)
            if not isinstance(loaded, FunctionType) or loaded.__code__ != expected:
                raise AllocationEvidenceError(
                    f"loaded code does not match the named commit: {name}:{attr}")


def _source_bytes(source_root: Path, expected_sha: str) -> tuple[dict[str, bytes], dict]:
    root = source_root.resolve()
    executing_root = Path(allocate.__file__).resolve().parent
    adapter_root = Path(__file__).resolve().parents[2]
    dependency_roots = {Path(module.__file__).resolve().parent for module in
                        (allocate, earnings, level1_policy_summary, margin_state)}
    staging_root = Path(account_staging.__file__).resolve().parents[2]
    if root != executing_root or root != adapter_root or root != staging_root or dependency_roots != {root}:
        raise AllocationEvidenceError("source root differs from the executing adapter/allocator checkout")
    sha = _git(root, "rev-parse", "--verify", "HEAD").decode().strip()
    if sha != expected_sha or not isinstance(expected_sha, str) or len(expected_sha) != 40:
        raise AllocationEvidenceError(f"source SHA mismatch: expected {expected_sha}, found {sha}")
    names = POLICY_FILES + EXECUTION_FILES
    status = _git(root, "status", "--porcelain=v1", "--", *names).decode()
    if status:
        raise AllocationEvidenceError("policy or executing dependency has staged/uncommitted drift")
    consumed, hashes = {}, {}
    for name in names:
        path = root / name
        if path.is_symlink() or not path.is_file() or path.resolve() != root / name:
            raise AllocationEvidenceError(f"required source is missing, redirected, or nonregular: {name}")
        committed = _git(root, "show", f"{expected_sha}:{name}")
        try:
            working = path.read_bytes()
        except OSError as exc:
            raise AllocationEvidenceError(f"required source could not be read: {name}") from exc
        if working != committed:
            raise AllocationEvidenceError(f"working bytes do not match named commit: {name}")
        consumed[name] = committed
        hashes[name] = hashlib.sha256(committed).hexdigest()
    _verify_loaded_code(consumed)
    return consumed, {"source_root": str(root), "git_sha": sha,
                      "files_sha256": {n: hashes[n] for n in POLICY_FILES},
                      "execution_sha256": {n: hashes[n] for n in EXECUTION_FILES}}


def _policy(source_root: Path, expected_sha: str) -> tuple[dict, dict, dict, dict]:
    consumed, provenance = _source_bytes(source_root, expected_sha)
    try:
        targets = yaml.safe_load(consumed["targets.yaml"]) or {}
        gates_doc = yaml.safe_load(consumed["gates.yaml"])
        lookthrough = yaml.safe_load(consumed["issuer_lookthrough.yaml"]) or {}
    except yaml.YAMLError as exc:
        raise AllocationEvidenceError("verified policy bytes are malformed YAML") from exc
    if not isinstance(targets, dict) or not isinstance(gates_doc, dict):
        raise AllocationEvidenceError("verified policy roots must be mappings")
    gate_rows = gates_doc.get("gates")
    if not isinstance(gate_rows, list):
        raise AllocationEvidenceError("verified gates policy must contain a gates list")
    gates = {}
    for index, row in enumerate(gate_rows):
        if not isinstance(row, dict) or not isinstance(row.get("ticker"), str) or not row["ticker"]:
            raise AllocationEvidenceError(f"verified gate row {index} has no valid ticker")
        ticker = row["ticker"].upper()
        if ticker in gates:
            raise AllocationEvidenceError(f"verified gates contain duplicate ticker {ticker}")
        gates[ticker] = row
    if not isinstance(lookthrough, dict):
        raise AllocationEvidenceError("verified issuer lookthrough root must be a mapping")
    return targets, gates, lookthrough, provenance


def _source_id(value: Any, label: str) -> str:
    if (not isinstance(value, str) or not value.strip() or
            not account_staging._CLIENT_ID_RE.fullmatch(value.strip())):
        raise AllocationEvidenceError(f"{label} has an invalid source identity")
    return value.strip()


def _validate_output_numbers(value: Any, path: str = "canonical_result") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _validate_output_numbers(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_output_numbers(child, f"{path}[{index}]")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        try:
            valid = math.isfinite(value)
        except OverflowError:
            valid = False
        if not valid:
            raise AllocationEvidenceError(f"{path} contains a non-finite output number")


def _level1_sleeves(targets: dict, holdings: dict, result: dict) -> dict:
    """Join the accepted sleeve policy to the values this run actually observed.

    Level 2 already falls out of :func:`allocate.plan` per instrument.  The
    sleeve view is the same facts grouped the way a whole-portfolio review
    needs them, and it invents no policy: the sleeve definitions, their
    members and their percentages all come from
    :func:`level1_policy_summary.build_policy_summary`, reading the verified
    canonical ``targets.yaml`` bytes this run already consumed.  An
    ``asset_class`` rollup would be wrong here -- the accepted policy splits
    SPY/VEA/VWO from GLD although both are funds -- so the governed mapping is
    used rather than reconstructed.

    Dollar figures inherit the allocator's own availability.  When the book is
    unavailable they are ``None`` with a stated reason, never estimated, which
    is the same withholding rule ``plan`` applies to its own dollars.
    """
    summary = level1_policy_summary.build_policy_summary(targets)
    book = result.get("book")
    known = bool(result.get("dollars_available")) and isinstance(book, (int, float))
    reason = None if known else "book is unavailable, so no sleeve dollar figure is published"
    cash = result.get("cash")
    # A share OF the book is undefined at a zero book, while the dollar figures
    # themselves remain exactly right. Withhold only the undefined one rather
    # than discarding a whole valid view -- or dividing and escaping the
    # envelope, since decimal raises ZeroDivisionError, not ValueError.
    book_total = Decimal(str(book)) if known else None
    pct_defined = known and book_total != 0

    sleeves, assigned = {}, set()
    for name, members in summary["members"].items():
        assigned.update(members)
        # CASH/RESERVE are synthetic destination rows, not holdable tickers --
        # the adapter rejects them as holding identities. The balance those
        # rows stand for is the tracked cash the allocator itself used.
        cash_sleeve = name == "cash_and_reserve"
        if not known:
            current = None
        elif cash_sleeve:
            current = float(cash) if isinstance(cash, (int, float)) else None
        else:
            current = float(sum(holdings.get(ticker, 0.0) for ticker in members))
        target_pct = Decimal(summary["sleeves_pct"][name])
        target = float(book_total * target_pct / 100) if known else None
        sleeves[name] = {
            "governed_target_pct": summary["sleeves_pct"][name],
            "members": list(members),
            "exposure_basis": "tracked cash balance" if cash_sleeve
                              else "sum of held member values",
            "current_value": current,
            "current_pct": (None if current is None or not pct_defined
                            else float(Decimal(str(current)) * 100 / book_total)),
            "target_value": target,
            # Positive means under the accepted sleeve weight.
            "gap_value": None if current is None or target is None else target - current,
        }

    # Anything held outside the accepted roster is disclosed, never folded into
    # a sleeve and never silently dropped; plan() reports the same names.
    unassigned = {t: v for t, v in holdings.items() if t not in assigned}
    return {
        "status": summary["status"],
        "policy_source": summary["policy_source"],
        "policy_basis": list(summary["policy_basis"]),
        "dollars_known": known,
        "withheld_reason": reason,
        "sleeves": sleeves,
        "unallocated_policy_pct": summary["sleeves_pct"]["unallocated"],
        "unassigned_holdings": unassigned,
        "reconciliation": dict(summary["reconciliation"]),
        "notes": [
            "sleeve exposure is gross of margin debt; book is net of it",
            "unallocated policy weight is held as cash and is never redistributed",
        ],
    }


def _review_evidence(runtime_root: Path | str, doc: dict) -> tuple[dict, bytes, str, dict]:
    verified = account_staging._verified(runtime_root, doc["submission_id"])
    if verified is None:
        raise AllocationEvidenceError("expected submission is absent or its binding is invalid")
    directory, original, receipt_bytes, receipt = verified
    receipt_hash = hashlib.sha256(receipt_bytes).hexdigest()
    if receipt_hash != doc["receipt_sha256"]:
        raise AllocationEvidenceError("expected receipt identity does not match retained bytes")
    paths = account_staging._review_paths(directory)
    reviews = []
    for path in paths:
        if path.name.startswith("."):
            continue
        if not path.name.endswith(".json") or not account_staging._ID_RE.fullmatch(path.stem):
            raise AllocationEvidenceError("review history contains an unrecognized entry")
        if not account_staging._safe_regular_file(path):
            raise AllocationEvidenceError("review history contains redirected or nonregular evidence")
        raw = account_staging._bounded(path, account_staging.MAX_REVIEW_BYTES)
        if not raw:
            raise AllocationEvidenceError("review history contains absent or oversized evidence")
        try:
            review = json.loads(raw, object_pairs_hook=account_staging._pairs,
                                parse_constant=account_staging._constant)
        except (UnicodeDecodeError, ValueError, RecursionError) as exc:
            raise AllocationEvidenceError("review history contains malformed evidence") from exc
        if not account_staging._valid_review(review, path, receipt, receipt_bytes):
            raise AllocationEvidenceError("review history contains invalid or incompletely bound evidence")
        reviews.append((review, raw))
    selected = [(review, raw) for review, raw in reviews if review["review_id"] == doc["review_id"]]
    if len(selected) != 1 or selected[0][0]["reviewer"] != doc["reviewer"]:
        raise AllocationEvidenceError("expected review identity/reviewer is absent")
    chosen, chosen_bytes = selected[0]
    if hashlib.sha256(chosen_bytes).hexdigest() != doc["review_sha256"]:
        raise AllocationEvidenceError("expected review bytes do not match review_sha256")
    if chosen["decision"] != "confirmed" or any(r["decision"] == "rejected" for r, _ in reviews):
        raise AllocationEvidenceError("expected review is rejected or conflicting")
    instants = [(account_staging._review_order_key(r)[0], r["review_id"]) for r, _ in reviews]
    latest = max(i for i, _ in instants)
    if sum(i == latest for i, _ in instants) != 1:
        raise AllocationEvidenceError("review precedence is ambiguous at an equal instant")
    if account_staging._review_order_key(chosen)[0] != latest:
        raise AllocationEvidenceError("expected review is superseded")

    selected_received = _parse_timestamp(receipt["received_at"], "received_at")
    submissions = account_staging._root(runtime_root, create=False)
    try:
        entries = tuple(submissions.iterdir())
    except OSError as exc:
        raise AllocationEvidenceError("submission history could not be enumerated") from exc
    for entry in entries:
        if not account_staging._ID_RE.fullmatch(entry.name):
            continue
        other_verified = account_staging._verified(runtime_root, entry.name)
        if other_verified is None:
            raise AllocationEvidenceError("submission history contains invalid retained evidence")
        record = other_verified[3]
        if record["submission_id"] == receipt["submission_id"]:
            continue
        other = _parse_timestamp(record["received_at"], "received_at")
        if other >= selected_received:
            raise AllocationEvidenceError("expected submission is superseded or has ambiguous precedence")
    return receipt, original, receipt_hash, chosen


def run(runtime_root: Path | str, supplement_bytes: bytes, *, source_root: Path | str,
        expected_source_sha: str) -> dict:
    """Return a provenance envelope containing the real ``allocate.plan`` result.

    Errors are returned as a controlled, non-actionable envelope.  In
    particular, no current-looking dependent dollar fields are synthesized.
    """
    supplement_hash = hashlib.sha256(supplement_bytes).hexdigest()
    try:
        # Verify and bind the executing code before it is used to judge any
        # evidence: the retained-review validators are themselves part of the
        # bound surface, so they must not run ahead of their own check.
        targets, gates, lookthrough, policy = _policy(Path(source_root), expected_source_sha)
        doc = _json(supplement_bytes)
        allowed = {"schema_version", "as_of", "submission_id", "receipt_sha256",
                   "review_id", "reviewer", "review_sha256", "buffer", "market",
                   "earnings", "regime"}
        if (set(doc) not in (allowed, allowed - {"buffer"}) or
                type(doc.get("schema_version")) is not int or
                doc["schema_version"] != SCHEMA_VERSION):
            raise AllocationEvidenceError("supplement must use schema_version 1 and only documented fields")
        as_of = _parse_timestamp(doc["as_of"], "as_of")
        receipt, original, receipt_hash, _ = _review_evidence(runtime_root, doc)
        normalized, issues = account_staging.validate(original)
        if issues:
            raise AllocationEvidenceError("confirmed submission unexpectedly has material issues")

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
            if buffer["currency"] != "USD":
                raise AllocationEvidenceError("buffer currency/source_id is invalid")
            _source_id(buffer["source_id"], "buffer.source_id")
            _fresh(buffer["observed_at"], "buffer.observed_at", as_of)

        holdings, shares = {}, {}
        observation_provenance = []
        for index, h in enumerate(normalized["holdings"]):
            if h["ticker"] in roster and roster[h["ticker"]]["asset_class"] in {"cash", "reserve"}:
                raise AllocationEvidenceError(
                    f"holding identity {h['ticker']} collides with a synthetic cash/reserve sleeve")
            qty = _finite(h["quantity"], f"holdings[{index}].quantity")
            shares[h["ticker"]] = qty
            if qty == 0:
                continue
            if h["freshness"] != "current" or h["valuation"] is None or h["valuation"]["freshness"] != "current":
                raise AllocationEvidenceError(f"{h['ticker']} has an unavailable required valuation")
            _fresh(h["observed_at"], f"{h['ticker']}.observed_at", as_of)
            _fresh(h["valuation"]["observed_at"], f"{h['ticker']}.valuation.observed_at", as_of)
            value = qty * _finite(h["valuation"]["unit_price"], f"{h['ticker']}.unit_price")
            if not math.isfinite(value):
                raise AllocationEvidenceError(f"{h['ticker']} valuation product is not finite")
            holdings[h["ticker"]] = value
            observation_provenance.append({"ticker": h["ticker"], "quantity_observed_at": h["observed_at"],
                                           "valuation_observed_at": h["valuation"]["observed_at"],
                                           "currency": h["valuation"]["currency"]})

        market_doc = doc["market"]
        if not isinstance(market_doc, list):
            raise AllocationEvidenceError("market must be a list")
        metrics = {}
        for i, row in enumerate(market_doc):
            required = {"ticker", "available", "price", "sma200", "rsi14", "currency",
                        "observed_at", "source_id"}
            if not isinstance(row, dict) or set(row) != required:
                raise AllocationEvidenceError(f"market[{i}] has an invalid shape")
            tk = row["ticker"]
            if tk in metrics or tk not in roster or row["currency"] != "USD":
                raise AllocationEvidenceError(f"market[{i}] has duplicate, non-roster, or non-USD identity")
            if type(row["available"]) is not bool:
                raise AllocationEvidenceError(f"market[{i}].available must be Boolean")
            _source_id(row["source_id"], f"market[{i}].source_id")
            age = _informational_age(row["observed_at"], f"market[{i}].observed_at", as_of)
            if row["available"]:
                price = _finite(row["price"], f"market[{i}].price", low=0.000000001)
                sma = (None if row["sma200"] is None else
                       _finite(row["sma200"], f"market[{i}].sma200", low=0.000000001))
                rsi = (None if row["rsi14"] is None else
                       _finite(row["rsi14"], f"market[{i}].rsi14", high=100.0))
                metrics[tk] = ({"price": price, "sma200": sma, "rsi14": rsi}
                               if age <= 2 else
                               {"error": "dated market evidence unavailable"})
            elif not row["available"] and any(
                    row[k] is not None for k in ("price", "sma200", "rsi14")):
                raise AllocationEvidenceError(f"market[{i}] unavailable values must be null")
            else:
                metrics[tk] = {"error": "dated market evidence unavailable"}
        eligible_market = {tk for tk, meta in roster.items()
                           if meta["asset_class"] not in {"crypto", "cash", "reserve"}
                           and tk not in gates}
        if not eligible_market <= metrics.keys():
            raise AllocationEvidenceError("market evidence must cover every eligible non-crypto ticker")

        earnings_doc = doc["earnings"]
        if not isinstance(earnings_doc, list):
            raise AllocationEvidenceError("earnings must be a list")
        earnings = {}
        for i, row in enumerate(earnings_doc):
            if not isinstance(row, dict) or set(row) != {"ticker", "next_date", "observed_at", "source_id"}:
                raise AllocationEvidenceError(f"earnings[{i}] has an invalid shape")
            tk = row["ticker"]
            if tk in earnings or tk not in roster or tk in gates:
                raise AllocationEvidenceError(f"earnings[{i}] has an invalid identity")
            _source_id(row["source_id"], f"earnings[{i}].source_id")
            age = _informational_age(row["observed_at"], f"earnings[{i}].observed_at", as_of)
            if row["next_date"] is not None:
                try:
                    next_date = date.fromisoformat(row["next_date"])
                except (TypeError, ValueError) as exc:
                    raise AllocationEvidenceError(f"earnings[{i}].next_date is invalid") from exc
                if next_date < _observation_date(
                        row["observed_at"], f"earnings[{i}].observed_at"):
                    raise AllocationEvidenceError(
                        f"earnings[{i}].next_date predates its observation")
                earnings[tk] = ((next_date - as_of.date()).days
                                if age <= 2 and next_date >= as_of.date() else None)
            else:
                earnings[tk] = None  # canonically allowed, disclosed unknown
        if earnings.keys() != eligible_market:
            raise AllocationEvidenceError("earnings evidence must cover every eligible non-crypto ticker exactly")

        regime = doc["regime"]
        if not isinstance(regime, dict) or set(regime) != {"ok", "known", "observed_at", "source_id"}:
            raise AllocationEvidenceError("regime has an invalid shape")
        if type(regime["ok"]) is not bool or type(regime["known"]) is not bool:
            raise AllocationEvidenceError("regime ok/known must be Boolean")
        _source_id(regime["source_id"], "regime.source_id")
        regime_age = _informational_age(regime["observed_at"], "regime.observed_at", as_of)
        regime_ok = regime["ok"] if regime["known"] and regime_age <= 2 else False
        regime_known = regime["known"] and regime_age <= 2

        cash_row, debt_row = normalized["cash"][0], normalized["debt_margin"][0]
        holdings_state = {"shares": shares, "crypto_shares": {},
                          "cash": {"balance": cash_row["balance"],
                                   "synced_at": cash_row["observed_at"]},
                          "margin": {"debt": debt_row["balance"], "buffer_pct": buffer_pct,
                                     "synced_at": debt_row["observed_at"]}}
        cash_state = allocate.load_cash_state(holdings_state, as_of=as_of)
        margin_state = allocate.load_margin_state(holdings_state, as_of=as_of)
        valuation = allocate.valuation_completeness(holdings, holdings_state)
        availability = allocate.current_dollar_availability(cash_state, margin_state, valuation)
        result = allocate.plan(
            targets, holdings, roster, metrics, regime_ok, regime_known,
            cash_state["balance"], margin_debt=debt_row["balance"],
            margin_buffer_pct=buffer_pct, gates_cfg=gates,
            lookthrough=lookthrough, holdings_state=holdings_state,
            dollars_available=availability["available"], earnings_provider=earnings.get,
            as_of=as_of)
        _validate_output_numbers(result)
        level1 = _level1_sleeves(targets, holdings, result)
        _validate_output_numbers(level1, "level1")
        return {"actionable": bool(result["dollars_available"]),
                "blocked_reasons": availability["blocked_by"],
                "as_of": doc["as_of"], "canonical_result": result,
                "level1": level1,
                "provenance": {"submission_id": doc["submission_id"],
                    "submission_sha256": receipt["submission_sha256"],
                    "receipt_sha256": receipt_hash, "review_id": doc["review_id"],
                    "review_sha256": doc["review_sha256"],
                    "reviewer": doc["reviewer"], "supplement_sha256": supplement_hash,
                    "policy": policy, "observations": observation_provenance,
                    "buffer": buffer, "market": market_doc, "earnings": earnings_doc,
                    "regime": regime},
                "discrepancies": ["protected_capital submission rows are retained evidence but are not inferred as allocator reserve"],
                "limitations": ["recommendations only; no orders", "no broker retrieval or network access",
                                "unknown earnings is disclosed by the canonical result",
                                "executing code is bound to the named commit for the functions these"
                                " files define; names imported into them are covered only by the"
                                " shared source-root check"]}
    except (AllocationEvidenceError, ArithmeticError, account_staging.AccountStorageError,
            account_staging.AccountSubmissionRejected, KeyError,
            OSError, TypeError, ValueError) as exc:
        return {"actionable": False, "blocked_reasons": [str(exc)], "as_of": None,
                "canonical_result": None, "level1": None,
                "provenance": {"supplement_sha256": supplement_hash},
                "discrepancies": [], "limitations": ["No dependent dollar result is available."]}


def _json_safe(value: Any, path: str = "output") -> Any:
    """ISO-encode calendar values for the CLI's JSON boundary.

    The canonical result legitimately carries real ``date`` objects -- the
    retained common-driver measurement is one -- and :func:`run` returns them
    unchanged so Python callers keep canonical fidelity.  Only this boundary
    needs a serializable form, and anything it cannot represent faithfully is
    refused rather than coerced, so an unexpected type surfaces as a
    controlled envelope instead of an uncaught traceback.
    """
    if isinstance(value, dict):
        return {key: _json_safe(child, f"{path}.{key}") for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(child, f"{path}[{index}]") for index, child in enumerate(value)]
    if isinstance(value, (datetime, date)):  # datetime subclasses date; both isoformat
        return value.isoformat()
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise AllocationEvidenceError(f"{path} is not JSON-serializable: {type(value).__name__}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline private confirmed-evidence allocation adapter")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--supplement", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--expected-source-sha", required=True)
    args = parser.parse_args(argv)
    try:
        with args.supplement.open("rb") as handle:
            supplement = handle.read(MAX_SUPPLEMENT_BYTES + 1)
        output = run(args.runtime_root, supplement, source_root=args.source_root,
                     expected_source_sha=args.expected_source_sha)
    except OSError as exc:
        output = {"actionable": False, "blocked_reasons": [f"supplement could not be read: {exc}"],
                  "as_of": None, "canonical_result": None, "provenance": {},
                  "discrepancies": [], "limitations": ["No dependent dollar result is available."]}
    try:
        text = json.dumps(_json_safe(output), sort_keys=True, indent=2)
    except (AllocationEvidenceError, RecursionError, TypeError, ValueError) as exc:
        output = {"actionable": False, "blocked_reasons": [str(exc)], "as_of": None,
                  "canonical_result": None, "provenance": {}, "discrepancies": [],
                  "limitations": ["No dependent dollar result is available."]}
        text = json.dumps(output, sort_keys=True, indent=2)
    print(text)
    return 0 if output["actionable"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
