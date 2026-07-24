"""
dividend_ledger.py — MARGIN-0005 research-only dividend/corporate-action
ledger bridge (S2, third and final authorized S2 PR under the charter's
<=3 ceiling; scope per `research/margin_target_study/S2_G2_SCOPE_DETERMINATION.md`
§5, item 1, itself filed under `governance/decisions/OPS-0003-post-acceptance-
workstream-priority-transition.md` item 4).

Authorized by `governance/decisions/MARGIN-0005-margin-target-research-charter.md`
(charter §4, "Research package" row, which names this file) and
`research/margin_target_study/PROTOCOL_V2.md` §13's implementation-architecture
list. Closes the literal G2-gate obligations for **T-D1** (dividend
uniqueness) and **T-D2** (primary-path purity) that the scope determination's
§3 table identified as blocked purely on this module not existing yet:
neither test had a construction-layer artifact to test against before this PR
(T-D3/T-D5 were already satisfied at G1/G2B respectively; T-D4 is closed by
`validation_lib.py`, filed in this same PR).

## Scope

Bridges `data_acquisition.py`'s already-acquired, already-G1-validated,
gross-declared point-in-time dividend ledger
(`research/margin_target_study/data/dividends/dividend_ledger.json`) and
spin-off ledger (`research/margin_target_study/data/corporate_actions/
spinoffs.json`) into `margin_simulation.simulate()`'s exact optional-input
shapes:

    dividend_events:         {date: {ticker: gross cash per share}}
    corporate_action_events: {date: [{"ticker": ..., "ratio": ..., "unit_value": ...}]}

This module performs READ-ONLY file I/O under
`research/margin_target_study/data/` — the only I/O anywhere in it — and
never writes anything, anywhere. It never calls `margin_simulation.simulate()`,
never touches `trial_ledger.jsonl` or `candidate_freeze.yaml`, and consumes
zero of the 300-run trial ceiling. Zero import relationship with
`allocate.py`/`margin_state.py` in either direction (charter §4 / protocol
§13). It never imports, opens, or references the quarantined total-return
validation dataset — that access is reserved to `validation_lib.py` alone
(protocol §14 T-D4); see the isolation tests in `test_validation_lib.py`,
not duplicated here (deliberately not spelling out that dataset's own
directory/field names in this docstring, so a plain substring scan of this
file's source correctly finds none of them).

## Credited-date convention (R2 pre-S3 integration safety)

`research/margin_target_study/S2_G2_SCOPE_DETERMINATION.md` §4 records an
unresolved pre-S3 integration constraint from PR #140's independent review:
`repayment_lib.r2_dividends_first` must never be wired into `simulate()`'s
pre-trade hook using a same-day dividend amount *before that dividend is
actually credited to cash* — under insufficient idle cash that ordering
could fund a repayment by selling shares before the dividend structurally
lands. This module resolves that structurally, not procedurally: every
`build_dividend_events()` output is keyed by whichever single date the
active `credit_convention` treats as the day the cash exists —

  * `"ex_date"` (default) — the frozen PRIMARY registered convention
    (`pre_registration.yaml` `dividends.credit: ex_date`, matching
    `data_acquisition.py`'s own `dividend_ledger.json` `credit_convention`
    field and the T-D3 reconciliation methodology already passed at G1).
    Under this convention, "credited" and "ex_date" are, by the frozen
    pre-registration's own definition, the SAME event — there is no earlier
    date this module could leak, because the primary study design itself
    treats ex_date as when the cash structurally exists in the simulation.
  * `"pay_date_lag_30d"` — the frozen SENSITIVITY variant (same
    `pre_registration.yaml` key, `sensitivity: pay_date_lag_30d`), using
    the ledger's own `payable_date` (the literal date real dividend cash
    lands in a brokerage account) when present and chronologically sane,
    else a documented `ex_date + 30 calendar days` fallback (disclosed
    below, not silently assumed).

Neither convention is ever keyed by `announcement_date` or `record_date`
(both of which precede the cash structurally existing) — this module
exposes no function that would let a future caller (including R2) observe
a ticker's dividend information at any date earlier than the convention's
own credited date. There is exactly one date per event in the returned
dict; there is no separate "declared amount" lookup a repayment rule could
read ahead of it.

## T-D1 (dividend uniqueness)

Raw ledger rows are deduplicated by identity — the vendor's own `alpaca_id`
when present, else a composite (`symbol`, `ex_date`, `special`,
`gross_declared`, `payable_date`) key — BEFORE aggregation, so a literal
duplicate row (accidental re-fetch, re-import, or a hand-constructed
duplicate-injection test) can never be credited twice. Two genuinely
DISTINCT same-day events for one ticker (e.g. a regular + a special
dividend sharing an `ex_date`, both real rows in the acquired ledger) are
summed into one combined per-share figure for that date — correct
behavior, not a double-count, since `simulate()`'s `dividend_events` shape
carries at most one combined per-share amount per (ticker, date).

## T-D2 (primary-path purity)

This module reads only the gross-declared dividend ledger and the spin-off
ledger — never the quarantined total-return validation dataset. The
divergence-from-TR sanity check itself (proving the primary path is
genuinely NOT total-return-adjusted) lives in `test_validation_lib.py`,
which is licensed to touch the TR namespace; this module's contribution to
T-D2 is structural (it cannot reference TR by construction — see the
isolation tests) rather than an assertion this file makes about itself.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RESEARCH_DATA = _HERE / "research" / "margin_target_study" / "data"

DEFAULT_DIVIDEND_LEDGER_PATH = _RESEARCH_DATA / "dividends" / "dividend_ledger.json"
DEFAULT_CORPORATE_ACTION_LEDGER_PATH = _RESEARCH_DATA / "corporate_actions" / "spinoffs.json"

CREDIT_CONVENTION_EX_DATE = "ex_date"
CREDIT_CONVENTION_PAY_DATE_LAG_30D = "pay_date_lag_30d"
CREDIT_CONVENTIONS = (CREDIT_CONVENTION_EX_DATE, CREDIT_CONVENTION_PAY_DATE_LAG_30D)

# Only used as a fallback when a pay-date-convention row lacks a usable
# `payable_date` (data_acquisition.py's own G1 `validate()` already checks
# a `payable<ex` chronology failure and a `payable availability` ratio, so
# a validated ledger should rarely hit this path) — disclosed, not silent.
PAY_DATE_FALLBACK_LAG_DAYS = 30


# ── loading (READ-ONLY; the only I/O in this module) ────────────────────────

def load_dividend_ledger(path: str | Path | None = None) -> list[dict]:
    """Raw `dividends` rows from the acquired, G1-validated ledger JSON."""
    p = Path(path) if path is not None else DEFAULT_DIVIDEND_LEDGER_PATH
    with open(p) as f:
        doc = json.load(f)
    return doc["dividends"]


def load_corporate_action_ledger(path: str | Path | None = None) -> list[dict]:
    """Raw spin-off `events` rows from the acquired, G1-validated ledger JSON."""
    p = Path(path) if path is not None else DEFAULT_CORPORATE_ACTION_LEDGER_PATH
    with open(p) as f:
        doc = json.load(f)
    return doc["events"]


# ── dividend events ──────────────────────────────────────────────────────────

def _row_identity(row: dict) -> tuple:
    """Deduplication key for T-D1 — the vendor's own row identifier when
    available (the strongest signal a row is a literal re-fetch of the same
    event), else a composite of fields that would be identical only for a
    true duplicate, never for two distinct same-day dividends (which differ
    in `special` and/or `gross_declared` in every real acquired row)."""
    if row.get("alpaca_id"):
        return ("id", row["alpaca_id"])
    return ("composite", row["symbol"], row["ex_date"], bool(row.get("special")),
            round(float(row["gross_declared"]), 10), row.get("payable_date"))


def _credited_date(row: dict, convention: str) -> str:
    if convention == CREDIT_CONVENTION_EX_DATE:
        return row["ex_date"]
    if convention == CREDIT_CONVENTION_PAY_DATE_LAG_30D:
        pay = row.get("payable_date")
        if pay and pay >= row["ex_date"]:
            return pay
        return (date.fromisoformat(row["ex_date"])
                + timedelta(days=PAY_DATE_FALLBACK_LAG_DAYS)).isoformat()
    raise ValueError(f"unknown credit_convention {convention!r}; must be one of {CREDIT_CONVENTIONS}")


def build_dividend_events(rows: list[dict], *,
                          credit_convention: str = CREDIT_CONVENTION_EX_DATE
                          ) -> dict[str, dict[str, float]]:
    """Build `margin_simulation.simulate()`'s `dividend_events` input:
    `{credited_date: {ticker: gross cash per share}}`.

    T-D1: rows are deduplicated by `_row_identity()` before aggregation — a
    literal duplicate row credits exactly once, never twice. Genuinely
    distinct same-(ticker, credited_date) events (e.g. regular + special)
    are summed, matching `simulate()`'s single-per-share-figure-per-day
    contract. Non-positive `gross_declared` rows are dropped (no negative
    or zero dividend cash is ever credited)."""
    if credit_convention not in CREDIT_CONVENTIONS:
        raise ValueError(f"unknown credit_convention {credit_convention!r}; "
                         f"must be one of {CREDIT_CONVENTIONS}")
    seen: set[tuple] = set()
    events: dict[str, dict[str, float]] = {}
    for row in rows:
        ident = _row_identity(row)
        if ident in seen:
            continue
        seen.add(ident)
        amt = float(row["gross_declared"])
        if amt <= 0:
            continue
        credited = _credited_date(row, credit_convention)
        bucket = events.setdefault(credited, {})
        bucket[row["symbol"]] = bucket.get(row["symbol"], 0.0) + amt
    return events


# ── corporate-action (spin-off) events ───────────────────────────────────────

def build_corporate_action_events(events: list[dict], *, strict: bool = True
                                  ) -> dict[str, list[dict]]:
    """Build `margin_simulation.simulate()`'s `corporate_action_events` input:
    `{ex_date: [{"ticker": parent, "ratio": ratio_child_per_parent,
    "unit_value": child_close_on_parent_ex_session}]}` — per
    assumptions-ledger A-17 (opening-entitled shares x ratio x distributed-
    security consolidated close, credited as reinvestable cash).

    Keyed by `ex_date` only — spin-off events carry no `payable_date`
    concept (the distribution is a same-session in-kind event, valued at
    the parent's own ex-distribution session per A-17), matching the
    already-passed T-D3 reconciliation methodology in `data_acquisition.py`.

    `strict=True` (default): raises on an event with no valid
    `child_close_on_parent_ex_session` — `data_acquisition.py`'s own G1
    `validate()` already requires this field to be present and positive
    for every event, so encountering one here signals a data-integrity
    failure upstream, not a case to silently skip (repo convention: fail
    loudly on malformed input rather than produce a nonsensical reading).
    `strict=False` skips such an event instead, for callers who have their
    own reason to tolerate an incomplete record."""
    out: dict[str, list[dict]] = {}
    for ev in events:
        unit_value = ev.get("child_close_on_parent_ex_session")
        if not unit_value or unit_value <= 0:
            if strict:
                raise ValueError(
                    f"corporate-action event {ev.get('parent')}->{ev.get('child')} "
                    f"ex {ev.get('ex_date')} has no valid "
                    "child_close_on_parent_ex_session — data_acquisition.py's G1 "
                    "validate() should already guarantee this; treat as a "
                    "data-integrity failure, not a silent skip")
            continue
        out.setdefault(ev["ex_date"], []).append({
            "ticker": ev["parent"],
            "ratio": float(ev["ratio_child_per_parent"]),
            "unit_value": float(unit_value),
        })
    return out
