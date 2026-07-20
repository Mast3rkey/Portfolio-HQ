"""
freshness_cadence.py — pure cadence-trigger core for the Research Freshness
Framework (see docs/FRESHNESS_PLANNER_V1_SPEC.md §2/§7/§9; authorized in
bounded scope by governance/decisions/AUTO-0003-cadence-trigger-core.md).

Exactly one public function, `compute_due_cadence_fingerprint`: given a
ticker's current enrollment/checkpoint gating state and an explicit
`next_due`/`as_of_date` pair, decides whether that ticker's cadence is
strictly overdue (`next_due < as_of_date`, PI-0011's rule, adopted by
AUTO-0001 — equality is never overdue) and, only when it is, delegates
fingerprint production, unchanged, to the existing
`freshness_identity.compute_cadence_fingerprint`. This module never
reimplements the canonical-JSON/SHA-256 cadence-hashing algorithm
AUTO-0002 already fixed once.

Pure and deterministic: every value is supplied by the caller. No file
I/O, no YAML loading, no implicit system-clock access, no network access,
no randomness, no import of `intelligence_report.py` (a `PI-0011`-owned
module this decision has no standing to modify or couple to — see the
ADR's §4 equivalence-path resolution). The only project-internal import
is the existing public `freshness_identity.compute_cadence_fingerprint`,
imported under a private name.

All six inputs are fully validated, and the `monitoring_enabled`/
`checkpoint_status` cross-field invariant is checked, before any gating or
overdue evaluation runs — an invalid input can never fall through to a
`None` result that looks like a valid "not due" or "disabled" answer.
"""

from __future__ import annotations

import unicodedata
from datetime import date, datetime

from freshness_identity import (
    compute_cadence_fingerprint as _compute_cadence_fingerprint,
)

_CHECKPOINT_STATUSES = ("pending", "verified")
_ASCII_DIGITS = frozenset("0123456789")


# ── string-field normalization (ticker / template_version only) ────────────

def _normalize_open_string(value: object, name: str) -> str:
    """Same contract `freshness_identity.py`'s own private `_normalize_string`
    already fixes for `ticker`/`template_version` (AUTO-0002 Decision §3):
    require `str`; apply Unicode NFC; reject empty after normalization;
    reject any C0 control character (`< 0x20`) or C1 control character
    (`0x7F`-`0x9F`). Never stripped, uppercased, casefolded, or otherwise
    transformed beyond NFC. Independently implemented here — that helper is
    private and not part of `freshness_identity.py`'s authorized public
    surface, so it is reimplemented with equivalent semantics rather than
    imported, the same pattern `AUTO-0002` already used for its own local
    ISO-date parser relative to `intelligence_report.py`'s."""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a str, got {type(value).__name__}")
    normalized = unicodedata.normalize("NFC", value)
    if normalized == "":
        raise ValueError(f"{name} must not be empty after NFC normalization")
    for ch in normalized:
        code = ord(ch)
        if code < 0x20 or 0x7F <= code <= 0x9F:
            raise ValueError(
                f"{name} contains a disallowed control character "
                f"U+{code:04X} (C0 below 0x20 or C1 0x7F-0x9F)"
            )
    return normalized


# ── strict local date parser (next_due / as_of_date only) ──────────────────

def _parse_strict_date(value: object, name: str) -> date:
    """Accepts a `datetime.date` object, or a strict ASCII `YYYY-MM-DD`
    string: exactly 10 characters, ASCII digits `0`-`9` at positions
    0-3/5-6/8-9, hyphens at positions 4 and 7, and a valid calendar date.
    Rejects a `datetime.datetime` outright (checked before `date`, since
    `datetime` is itself a `date` subclass — never silently truncated to
    its calendar date); rejects compact dates, partial dates, timestamps,
    whitespace-padded dates, non-ASCII/Unicode-digit variants (Python's
    `\\d` regex class matches Unicode decimal digits unless `re.ASCII` is
    set — this parser checks digit identity by exact character membership
    instead of a bare `\\d` pattern, so a look-alike Unicode digit is never
    silently accepted), malformed calendar dates, and every other type.
    Independently implemented here, not imported from or delegated to
    `intelligence_report.py` or any other module's local ISO-date parser."""
    if isinstance(value, datetime):
        raise ValueError(f"{name} must not be a datetime — pass a date or a strict YYYY-MM-DD string")
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        if len(value) != 10:
            raise ValueError(f"{name} must be a strict YYYY-MM-DD string, got {value!r}")
        if value[4] != "-" or value[7] != "-":
            raise ValueError(f"{name} must be a strict YYYY-MM-DD string, got {value!r}")
        for i in (0, 1, 2, 3, 5, 6, 8, 9):
            if value[i] not in _ASCII_DIGITS:
                raise ValueError(f"{name} must be a strict YYYY-MM-DD string, got {value!r}")
        try:
            return date(int(value[0:4]), int(value[5:7]), int(value[8:10]))
        except ValueError as exc:
            raise ValueError(f"{name} is not a valid calendar date: {value!r}") from exc
    raise ValueError(f"{name} must be a date or a strict YYYY-MM-DD string, got {type(value).__name__}")


# ── public API ───────────────────────────────────────────────────────────

def compute_due_cadence_fingerprint(
    *,
    ticker: str,
    monitoring_enabled: bool,
    checkpoint_status: str,
    next_due: date | str,
    as_of_date: date | str,
    template_version: str,
) -> str | None:
    """AUTO-0003 Decision §3 complete function contract — validation
    first, gating, strict overdue rule, delegation. Fixed step order:

    1. Validate and normalize `ticker`.
    2. Validate and normalize `template_version`.
    3. Validate `monitoring_enabled` is exactly `bool`.
    4. Validate `checkpoint_status` is a `str` and exactly `"pending"` or
       `"verified"`.
    5. Validate and parse `next_due`.
    6. Validate and parse `as_of_date`.
    7. Cross-field invariant: `monitoring_enabled is True` together with
       `checkpoint_status == "pending"` raises `ValueError`.

    All validation above completes before any gate, precedence rank, or
    overdue evaluation below is ever reached — this ordering is the
    structural guarantee (identical in kind to
    `freshness_state.evaluate_freshness_state`'s own "all validation runs
    to completion before any precedence rank is evaluated") that an
    invalid input can never fall through to a `None` result that looks
    like a valid "not due" or "disabled" answer.

    8. Gate: `monitoring_enabled is False` or `checkpoint_status ==
       "pending"` returns `None`.
    9. Strict overdue rule: `next_due < as_of_date` is overdue;
       `next_due == as_of_date` is not overdue; `next_due > as_of_date` is
       not overdue. Not overdue returns `None`.
    10. If overdue, delegate fingerprint production, unchanged, to the
        existing `freshness_identity.compute_cadence_fingerprint` and
        return its result exactly as received.
    """
    normalized_ticker = _normalize_open_string(ticker, "ticker")
    normalized_template_version = _normalize_open_string(template_version, "template_version")

    if not isinstance(monitoring_enabled, bool):
        raise ValueError(
            f"monitoring_enabled must be exactly bool, got {monitoring_enabled!r} "
            f"({type(monitoring_enabled).__name__})"
        )

    # Type-checked before closed-vocabulary membership: an unhashable value
    # (list, dict) must raise this function's own documented ValueError,
    # never an uncaught TypeError from `in`.
    if not isinstance(checkpoint_status, str):
        raise ValueError(
            f"checkpoint_status must be a str, got {checkpoint_status!r} "
            f"({type(checkpoint_status).__name__})"
        )
    if checkpoint_status not in _CHECKPOINT_STATUSES:
        raise ValueError(
            f"checkpoint_status must be exactly one of {list(_CHECKPOINT_STATUSES)}, "
            f"got {checkpoint_status!r}"
        )

    next_due_date = _parse_strict_date(next_due, "next_due")
    as_of_date_date = _parse_strict_date(as_of_date, "as_of_date")

    if monitoring_enabled is True and checkpoint_status == "pending":
        raise ValueError(
            "monitoring_enabled is True but checkpoint_status is \"pending\" — "
            "invalid combination"
        )

    # All validation is now complete.

    if monitoring_enabled is False or checkpoint_status == "pending":
        return None

    if not (next_due_date < as_of_date_date):
        return None

    return _compute_cadence_fingerprint(
        ticker=normalized_ticker,
        next_due=next_due_date,
        template_version=normalized_template_version,
    )
