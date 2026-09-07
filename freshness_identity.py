"""
freshness_identity.py — deterministic fingerprint and task-instance
identity helpers for the Research Freshness Framework (see
docs/FRESHNESS_PLANNER_V1_SPEC.md §7/§12/§13; authorized in bounded scope
by governance/decisions/AUTO-0002-freshness-local-foundation.md).

Exactly two public functions, both pure: no file I/O, no network access,
no implicit system clock, no randomness — every value is supplied by the
caller. A third function, computing a filing-derived fingerprint, is
explicitly not authorized by AUTO-0002 and does not exist here.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Sequence
from datetime import date, datetime

_FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ── canonicalization primitives ─────────────────────────────────────────────

def _normalize_string(value: object, name: str) -> str:
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


def _normalize_date(value: object, name: str) -> str:
    """AUTO-0002 Decision §3 date-normalization rule: same local ISO-date
    rule as §1 — a date object or strict YYYY-MM-DD string accepted and
    canonicalized to YYYY-MM-DD; a datetime rejected outright, never
    truncated (checked before date, since datetime subclasses date); any
    other type or malformed string rejected."""
    if isinstance(value, datetime):
        raise ValueError(f"{name} must not be a datetime — pass a date or YYYY-MM-DD string")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        if not _ISO_DATE_RE.match(value):
            raise ValueError(f"{name} must be a strict YYYY-MM-DD string, got {value!r}")
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(f"{name} is not a valid calendar date: {value!r}") from exc
        return parsed.date().isoformat()
    raise ValueError(f"{name} must be a date or a YYYY-MM-DD string, got {type(value).__name__}")


def _validate_fingerprint_assignments(value: object) -> list[tuple[str, int]]:
    """AUTO-0002 Decision §3 step 5 — exact container/pair validation
    order, duplicate/conflict detection, then sort."""
    if isinstance(value, (str, bytes, bytearray)):
        raise ValueError(
            f"fingerprint_assignments must not be a str/bytes/bytearray, got "
            f"{type(value).__name__}"
        )
    if not isinstance(value, Sequence):
        raise ValueError(
            f"fingerprint_assignments must be a collections.abc.Sequence, got "
            f"{type(value).__name__}"
        )

    snapshot = tuple(value)
    if len(snapshot) == 0:
        raise ValueError("fingerprint_assignments must not be empty")

    validated: list[tuple[str, int]] = []
    for item in snapshot:
        if isinstance(item, (str, bytes, bytearray)):
            raise ValueError(
                f"fingerprint_assignments item must not be a str/bytes/bytearray, "
                f"got {type(item).__name__}: {item!r}"
            )
        if not isinstance(item, Sequence):
            raise ValueError(
                f"fingerprint_assignments item must be a collections.abc.Sequence, "
                f"got {type(item).__name__}: {item!r}"
            )
        if len(item) != 2:
            raise ValueError(
                f"fingerprint_assignments item must have exactly 2 elements, got "
                f"{len(item)}: {item!r}"
            )

        fingerprint, ordinal = item[0], item[1]

        if not isinstance(fingerprint, str) or not _FINGERPRINT_RE.match(fingerprint):
            raise ValueError(
                f"fingerprint_assignments item fingerprint must be a lowercase "
                f"64-character hex digest matching ^[0-9a-f]{{64}}$, got {fingerprint!r}"
            )

        if isinstance(ordinal, bool):
            raise ValueError(
                f"fingerprint_assignments item ordinal must not be bool, got {ordinal!r}"
            )
        if not isinstance(ordinal, int):
            raise ValueError(
                f"fingerprint_assignments item ordinal must be an int, got "
                f"{type(ordinal).__name__}: {ordinal!r}"
            )
        if ordinal < 1:
            raise ValueError(
                f"fingerprint_assignments item ordinal must be >= 1, got {ordinal!r}"
            )

        validated.append((fingerprint, ordinal))

    seen_pairs: set[tuple[str, int]] = set()
    seen_ordinal_by_fingerprint: dict[str, int] = {}
    for fingerprint, ordinal in validated:
        pair = (fingerprint, ordinal)
        if pair in seen_pairs:
            raise ValueError(f"duplicate (fingerprint, ordinal) pair: {pair!r}")
        seen_pairs.add(pair)

        prior_ordinal = seen_ordinal_by_fingerprint.get(fingerprint)
        if prior_ordinal is not None and prior_ordinal != ordinal:
            raise ValueError(
                f"fingerprint {fingerprint!r} appears with conflicting ordinals: "
                f"{prior_ordinal!r} and {ordinal!r}"
            )
        seen_ordinal_by_fingerprint[fingerprint] = ordinal

    return sorted(validated, key=lambda pair: (pair[0], pair[1]))


def _hash_canonical_fields(pairs: list[list[object]]) -> str:
    payload = json.dumps(pairs, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ── public API ─────────────────────────────────────────────────────────────

def compute_cadence_fingerprint(
    *,
    ticker: str,
    next_due: date | str,
    template_version: str,
) -> str:
    """AUTO-0002 Decision §3 / spec §7. Canonical fields, in order:
    fingerprint_type="cadence_v1", ticker, next_due, template_version."""
    norm_ticker = _normalize_string(ticker, "ticker")
    norm_next_due = _normalize_date(next_due, "next_due")
    norm_template_version = _normalize_string(template_version, "template_version")

    pairs = [
        ["fingerprint_type", "cadence_v1"],
        ["ticker", norm_ticker],
        ["next_due", norm_next_due],
        ["template_version", norm_template_version],
    ]
    return _hash_canonical_fields(pairs)


def compute_task_instance_id(
    *,
    ticker: str,
    episode_id: str,
    fingerprint_assignments: Sequence,
    template_version: str,
) -> str:
    """AUTO-0002 Decision §3 / spec §13. Canonical fields, in order:
    fingerprint_type="task_instance_v1", ticker, episode_id,
    fingerprint_assignments (sorted validated pairs), template_version."""
    norm_ticker = _normalize_string(ticker, "ticker")
    norm_episode_id = _normalize_string(episode_id, "episode_id")
    norm_template_version = _normalize_string(template_version, "template_version")
    sorted_assignments = _validate_fingerprint_assignments(fingerprint_assignments)

    pairs = [
        ["fingerprint_type", "task_instance_v1"],
        ["ticker", norm_ticker],
        ["episode_id", norm_episode_id],
        ["fingerprint_assignments", [[fp, ordinal] for fp, ordinal in sorted_assignments]],
        ["template_version", norm_template_version],
    ]
    return _hash_canonical_fields(pairs)
