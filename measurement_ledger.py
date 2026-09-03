"""Validated, append-only portfolio measurement ledgers.

These ledgers are descriptive evidence.  They never change holdings, targets,
margin policy, recommendations, or execution state.

Exact time-weighted return (TWR) is deliberately fail-closed.  A cash flow must
carry an immediately-before and immediately-after whole-book valuation.  If
that evidence is absent or inconsistent, no exact TWR is reported.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping


CASHFLOW_FIELDS = (
    "occurred_at",
    "direction",
    "amount",
    "book_before",
    "book_after",
    "source",
    "note",
)
MARGIN_FIELDS = (
    "observed_at",
    "event_type",
    "amount",
    "resulting_debt",
    "resulting_buffer_pct",
    "source",
    "note",
)
INTEREST_FIELDS = (
    "charged_at",
    "amount_charged",
    "statement_period_start",
    "statement_period_end",
    "source",
    "note",
)


class MeasurementError(ValueError):
    """Raised when evidence cannot be recorded or interpreted honestly."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _timestamp(value: str | datetime, *, field: str) -> datetime:
    if isinstance(value, datetime):
        result = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            result = datetime.fromisoformat(text)
        except ValueError as exc:
            raise MeasurementError(f"{field} must be an ISO-8601 timestamp") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise MeasurementError(f"{field} must include a timezone")
    return result.astimezone(timezone.utc)


def _iso(value: str | datetime, *, field: str) -> str:
    return _timestamp(value, field=field).isoformat().replace("+00:00", "Z")


def _number(value, *, field: str, minimum: float | None = None,
            maximum: float | None = None) -> float:
    if isinstance(value, bool):
        raise MeasurementError(f"{field} must be numeric, not boolean")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise MeasurementError(f"{field} must be numeric") from exc
    if not math.isfinite(result):
        raise MeasurementError(f"{field} must be finite")
    if minimum is not None and result < minimum:
        raise MeasurementError(f"{field} must be at least {minimum}")
    if maximum is not None and result > maximum:
        raise MeasurementError(f"{field} must be at most {maximum}")
    return result


def _clean_text(value, *, field: str, required: bool = False) -> str:
    text = "" if value is None else str(value).strip()
    if required and not text:
        raise MeasurementError(f"{field} is required")
    if "\x00" in text or "\r" in text or "\n" in text:
        raise MeasurementError(f"{field} must be a single line")
    return text


def _read_rows(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, strict=True)
            if tuple(reader.fieldnames or ()) != fields:
                raise MeasurementError(
                    f"{path.name} has unexpected columns: {reader.fieldnames!r}"
                )
            rows = []
            for line_number, row in enumerate(reader, start=2):
                # DictReader stores surplus cells under a None key and missing
                # cells as None values.  Neither may be silently discarded:
                # accepting either would let a malformed durable record survive
                # validation and then influence later measurement.
                if set(row) != set(fields) or any(value is None for value in row.values()):
                    raise MeasurementError(
                        f"{path.name} row {line_number} does not match its schema"
                    )
                rows.append({field: row[field] for field in fields})
            return rows
    except csv.Error as exc:
        raise MeasurementError(f"{path.name} contains malformed CSV") from exc


def _append(path: Path, fields: tuple[str, ...], row: Mapping[str, object]) -> None:
    exists = path.exists()
    if exists:
        _read_rows(path, fields)  # validate the durable schema before appending
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fields})


def record_cashflow(path: Path, *, direction: str, amount,
                    book_before, book_after, source: str = "broker_statement",
                    note: str = "", occurred_at: str | datetime | None = None) -> dict:
    """Record one external contribution or withdrawal with bracketing values."""
    direction = _clean_text(direction, field="direction", required=True).lower()
    if direction not in {"deposit", "withdrawal"}:
        raise MeasurementError("direction must be deposit or withdrawal")
    amount = _number(amount, field="amount", minimum=0.01)
    before = _number(book_before, field="book_before", minimum=0.0)
    after = _number(book_after, field="book_after", minimum=0.0)
    expected = before + amount if direction == "deposit" else before - amount
    if not math.isclose(after, expected, abs_tol=0.01, rel_tol=0.0):
        raise MeasurementError(
            f"book_after must equal book_before {'+' if direction == 'deposit' else '-'} "
            f"amount within $0.01 (expected {expected:.2f}, got {after:.2f})"
        )
    row = {
        "occurred_at": _iso(occurred_at or utc_now(), field="occurred_at"),
        "direction": direction,
        "amount": f"{amount:.2f}",
        "book_before": f"{before:.2f}",
        "book_after": f"{after:.2f}",
        "source": _clean_text(source, field="source", required=True),
        "note": _clean_text(note, field="note"),
    }
    rows = _read_rows(path, CASHFLOW_FIELDS)
    if rows and _timestamp(row["occurred_at"], field="occurred_at") <= _timestamp(
            rows[-1]["occurred_at"], field="existing occurred_at"):
        raise MeasurementError("cash-flow timestamps must be strictly increasing")
    _append(path, CASHFLOW_FIELDS, row)
    return row


def record_margin_sync(path: Path, *, resulting_debt, resulting_buffer_pct,
                       prior_debt=None, source: str = "robinhood_displayed",
                       note: str = "", observed_at: str | datetime | None = None,
                       validate_only: bool = False) -> dict:
    """Record a debt/buffer observation and infer its event class from debt delta."""
    debt = _number(resulting_debt, field="resulting_debt", minimum=0.0)
    buffer_pct = _number(
        resulting_buffer_pct, field="resulting_buffer_pct", minimum=0.0, maximum=100.0
    )
    if prior_debt is None:
        event_type, amount = "initial_sync", 0.0
    else:
        prior = _number(prior_debt, field="prior_debt", minimum=0.0)
        delta = debt - prior
        if math.isclose(delta, 0.0, abs_tol=0.005, rel_tol=0.0):
            event_type, amount = "resync", 0.0
        elif delta > 0:
            event_type, amount = "draw", delta
        else:
            event_type, amount = "paydown", -delta
    row = {
        "observed_at": _iso(observed_at or utc_now(), field="observed_at"),
        "event_type": event_type,
        "amount": f"{amount:.2f}",
        "resulting_debt": f"{debt:.2f}",
        "resulting_buffer_pct": f"{buffer_pct:.2f}",
        "source": _clean_text(source, field="source", required=True),
        "note": _clean_text(note, field="note"),
    }
    rows = _read_rows(path, MARGIN_FIELDS)
    if rows and _timestamp(row["observed_at"], field="observed_at") <= _timestamp(
            rows[-1]["observed_at"], field="existing observed_at"):
        raise MeasurementError("margin observation timestamps must be strictly increasing")
    if not validate_only:
        _append(path, MARGIN_FIELDS, row)
    return row


def record_interest(path: Path, *, amount_charged, statement_period_start: str,
                    statement_period_end: str, source: str = "broker_statement",
                    note: str = "", charged_at: str | datetime | None = None) -> dict:
    """Record one actual broker interest charge; estimates are not accepted."""
    amount = _number(amount_charged, field="amount_charged", minimum=0.01)
    try:
        start = date.fromisoformat(_clean_text(
            statement_period_start, field="statement_period_start", required=True
        ))
        end = date.fromisoformat(_clean_text(
            statement_period_end, field="statement_period_end", required=True
        ))
    except ValueError as exc:
        raise MeasurementError("statement periods must be ISO-8601 dates") from exc
    if end < start:
        raise MeasurementError("statement_period_end must not precede start")
    row = {
        "charged_at": _iso(charged_at or utc_now(), field="charged_at"),
        "amount_charged": f"{amount:.2f}",
        "statement_period_start": start.isoformat(),
        "statement_period_end": end.isoformat(),
        "source": _clean_text(source, field="source", required=True),
        "note": _clean_text(note, field="note"),
    }
    rows = _read_rows(path, INTEREST_FIELDS)
    if rows and _timestamp(row["charged_at"], field="charged_at") <= _timestamp(
            rows[-1]["charged_at"], field="existing charged_at"):
        raise MeasurementError("interest charge timestamps must be strictly increasing")
    _append(path, INTEREST_FIELDS, row)
    return row


@dataclass(frozen=True)
class ExactTWR:
    start_at: str
    end_at: str
    return_pct: float
    valuation_count: int
    cashflow_count: int


def exact_twr(performance_rows: Iterable[Mapping[str, object]],
              cashflow_rows: Iterable[Mapping[str, object]]) -> ExactTWR:
    """Link exact subperiod returns, failing closed on missing valuation evidence."""
    valuations: list[tuple[datetime, float]] = []
    for row in performance_rows:
        if not row.get("observed_at") or row.get("book") in {None, ""}:
            continue
        at = _timestamp(row["observed_at"], field="performance observed_at")
        book = _number(row["book"], field="performance book", minimum=0.0)
        valuations.append((at, book))
    valuations.sort(key=lambda item: item[0])
    if len(valuations) < 2:
        raise MeasurementError(
            "exact TWR needs at least two timestamped whole-book snapshots"
        )
    if any(a[0] >= b[0] for a, b in zip(valuations, valuations[1:])):
        raise MeasurementError("performance timestamps must be strictly increasing")

    flows: list[tuple[datetime, float, float]] = []
    for row in cashflow_rows:
        at = _timestamp(row.get("occurred_at", ""), field="cashflow occurred_at")
        direction = _clean_text(row.get("direction"), field="direction", required=True)
        if direction not in {"deposit", "withdrawal"}:
            raise MeasurementError("cashflow direction must be deposit or withdrawal")
        amount = _number(row.get("amount"), field="cashflow amount", minimum=0.01)
        before = _number(row.get("book_before"), field="cashflow book_before", minimum=0.0)
        after = _number(row.get("book_after"), field="cashflow book_after", minimum=0.0)
        expected = before + amount if direction == "deposit" else before - amount
        if not math.isclose(after, expected, abs_tol=0.01, rel_tol=0.0):
            raise MeasurementError("cashflow bracketing values do not reconcile")
        flows.append((at, before, after))
    flows.sort(key=lambda item: item[0])
    if any(a[0] >= b[0] for a, b in zip(flows, flows[1:])):
        raise MeasurementError("cash-flow timestamps must be strictly increasing")

    start_at, start_book = valuations[0]
    end_at = valuations[-1][0]
    in_window = [flow for flow in flows if start_at < flow[0] < end_at]
    # A boundary collision cannot establish whether the flow happened before or
    # after the valuation; refusing is more honest than choosing an ordering.
    valuation_times = {valuation[0] for valuation in valuations}
    if any(flow[0] in valuation_times for flow in flows):
        raise MeasurementError("cashflow timestamp collides with a valuation timestamp")

    factor = 1.0
    prior_at, prior_book = valuations[0]
    flow_index = 0
    for current_at, current_book in valuations[1:]:
        while flow_index < len(in_window) and in_window[flow_index][0] < current_at:
            flow_at, before, after = in_window[flow_index]
            if flow_at <= prior_at:
                flow_index += 1
                continue
            if prior_book <= 0:
                raise MeasurementError("a return subperiod starts with non-positive book")
            factor *= before / prior_book
            prior_at, prior_book = flow_at, after
            flow_index += 1
        if prior_book <= 0:
            raise MeasurementError("a return subperiod starts with non-positive book")
        factor *= current_book / prior_book
        prior_at, prior_book = current_at, current_book

    return ExactTWR(
        start_at=_iso(start_at, field="start_at"),
        end_at=_iso(end_at, field="end_at"),
        return_pct=(factor - 1.0) * 100.0,
        valuation_count=len(valuations),
        cashflow_count=len(in_window),
    )


def read_cashflows(path: Path) -> list[dict[str, str]]:
    return _read_rows(path, CASHFLOW_FIELDS)
