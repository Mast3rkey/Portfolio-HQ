"""
freshness_state.py — pure freshness-state precedence evaluator for the
Research Freshness Framework (see docs/FRESHNESS_PLANNER_V1_SPEC.md §9;
authorized in bounded scope by
governance/decisions/AUTO-0002-freshness-local-foundation.md).

Implements exactly the four-state, fail-closed precedence rule over
explicit, already-computed, typed inputs. No YAML loading, no file I/O, no
system clock, no network, no GitHub access, and no import of
intelligence_report.py or freshness_validator.py — this module is a pure
function over its arguments only.
"""

from __future__ import annotations

import re
from collections.abc import Set as AbstractSet

_CHECKPOINT_STATUSES = {"pending", "verified"}
_MONITOR_STATES = {"healthy", "degraded", "failed"}

_FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")

_STATES = ("current", "unverified", "review_due", "pending_human_review")


def _validate_bool(value: object, name: str) -> None:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be exactly bool, got {value!r} ({type(value).__name__})")


def _snapshot_fingerprint_set(value: object, name: str) -> frozenset[str]:
    if not isinstance(value, AbstractSet):
        raise ValueError(
            f"{name} must be an instance of collections.abc.Set (set or frozenset), "
            f"got {value!r} ({type(value).__name__})"
        )
    # A conforming collections.abc.Set is not guaranteed to yield only
    # hashable members -- a custom implementation could still produce an
    # unhashable member (e.g. a list or dict), which frozenset() would
    # reject with TypeError. That must surface as this function's
    # documented ValueError contract, not an uncaught TypeError, so the
    # member-format validation below always gets the chance to run.
    try:
        snapshot = frozenset(value)
    except TypeError as exc:
        raise ValueError(
            f"{name} contains a member that cannot be represented in a frozenset"
        ) from exc
    for member in snapshot:
        if not isinstance(member, str) or not _FINGERPRINT_RE.match(member):
            raise ValueError(
                f"{name} contains a member that is not a lowercase 64-character hex "
                f"digest matching ^[0-9a-f]{{64}}$: {member!r}"
            )
    return snapshot


def evaluate_freshness_state(
    *,
    monitoring_enabled: bool,
    checkpoint_status: str,
    monitor_record_exists: bool,
    latest_monitor_state: str | None,
    outstanding: AbstractSet[str],
    assigned: AbstractSet[str],
    awaiting_human_incorporation: AbstractSet[str],
    incorporated: AbstractSet[str],
) -> str:
    """AUTO-0002 Decision §2 / spec §9 precedence rule. All validation
    completes before any precedence rank is evaluated, so invalid input
    can never fall through to `current`."""

    _validate_bool(monitoring_enabled, "monitoring_enabled")
    _validate_bool(monitor_record_exists, "monitor_record_exists")

    # Type-checked before closed-set membership: an unhashable value
    # (list, dict) would raise TypeError from `in` against a set, not
    # the ValueError this function's contract guarantees for all invalid
    # input.
    if not isinstance(checkpoint_status, str):
        raise ValueError(
            f"checkpoint_status must be a str, got {checkpoint_status!r} "
            f"({type(checkpoint_status).__name__})"
        )
    if checkpoint_status not in _CHECKPOINT_STATUSES:
        raise ValueError(
            f"checkpoint_status must be exactly one of {sorted(_CHECKPOINT_STATUSES)}, "
            f"got {checkpoint_status!r}"
        )

    if monitor_record_exists is False and latest_monitor_state is not None:
        raise ValueError(
            "monitor_record_exists is False but latest_monitor_state is not None "
            f"(got {latest_monitor_state!r}) — contradiction"
        )
    if monitor_record_exists is True and latest_monitor_state is None:
        raise ValueError(
            "monitor_record_exists is True but latest_monitor_state is None — a "
            "monitor run always records a state"
        )
    if monitor_record_exists is True:
        # Same type-before-membership guard as checkpoint_status above.
        if not isinstance(latest_monitor_state, str):
            raise ValueError(
                f"latest_monitor_state must be a str, got {latest_monitor_state!r} "
                f"({type(latest_monitor_state).__name__})"
            )
        if latest_monitor_state not in _MONITOR_STATES:
            raise ValueError(
                f"latest_monitor_state must be exactly one of {sorted(_MONITOR_STATES)} "
                f"when monitor_record_exists is True, got {latest_monitor_state!r}"
            )

    outstanding_snap = _snapshot_fingerprint_set(outstanding, "outstanding")
    assigned_snap = _snapshot_fingerprint_set(assigned, "assigned")
    awaiting_snap = _snapshot_fingerprint_set(awaiting_human_incorporation, "awaiting_human_incorporation")
    incorporated_snap = _snapshot_fingerprint_set(incorporated, "incorporated")

    all_sets = {
        "outstanding": outstanding_snap,
        "assigned": assigned_snap,
        "awaiting_human_incorporation": awaiting_snap,
        "incorporated": incorporated_snap,
    }
    seen: dict[str, str] = {}
    for set_name, members in all_sets.items():
        for member in members:
            prior = seen.get(member)
            if prior is not None:
                raise ValueError(
                    f"fingerprint {member!r} appears in more than one state set: "
                    f"{prior!r} and {set_name!r}"
                )
            seen[member] = set_name

    if awaiting_snap:
        return "pending_human_review"

    if outstanding_snap or assigned_snap:
        return "review_due"

    if (
        monitoring_enabled is False
        or checkpoint_status == "pending"
        or monitor_record_exists is False
        or latest_monitor_state in ("degraded", "failed")
    ):
        return "unverified"

    return "current"
