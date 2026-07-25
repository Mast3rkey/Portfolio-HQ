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

Raw ledger rows are deduplicated by identity BEFORE aggregation, so a
literal duplicate row (accidental re-fetch, re-import, or a
hand-constructed duplicate-injection test) can never be credited twice.
Two genuinely DISTINCT same-day events for one ticker (e.g. a regular + a
special dividend sharing an `ex_date`, both real rows in the acquired
ledger) are summed into one combined per-share figure for that date —
correct behavior, not a double-count, since `simulate()`'s
`dividend_events` shape carries at most one combined per-share amount per
(ticker, date).

**Identity model (F-5, refined by NEW-2): core economic identity, separated
from supplemental metadata.** Rows are grouped by a CORE identity —
`(symbol, ex_date, special)` — the minimal set of fields T-D1's own
distinctness reasoning actually relies on (two real distinct same-day
dividends differ in `special`; that is the one field that legitimately
separates two credited events on the same day for the same ticker).
`gross_declared` and `payable_date` are deliberately NOT part of core
identity — they are supplemental facts ABOUT one declaration, not what
makes two rows describe different declarations:

* **`gross_declared` in core identity would be wrong in both directions.**
  Two rows sharing every other field but reporting different amounts are
  not two distinct dividends — they are the SAME declaration with a data
  inconsistency (e.g. a corrected re-fetch), and including the amount in
  identity would silently treat that inconsistency as two real, summed
  events. (The pre-NEW-2 composite key DID include `gross_declared`,
  which is exactly how it introduced the "conflicting amount" gap NEW-2
  closes — see below.)
* **`payable_date` in core identity is the residual F-5 gap NEW-2
  closes.** F-5 fixed the `alpaca_id`-presence asymmetry, but the
  composite key it introduced still included `payable_date`, so two rows
  for the same declaration that differ only in whether `payable_date` is
  present would still fall into different composite buckets and both
  credit. Excluding it from core identity (see below for how it is still
  used, as supplemental metadata) closes that gap the same way F-5 closed
  the `alpaca_id` one.

**Within one core-identity group, rows are either a TRUE duplicate (safe
to silently collapse to one credit) or a CONFLICT (ambiguous — must never
be silently resolved by row order):**

* If every row in the group reports the SAME `gross_declared` (within
  float rounding) and every NON-missing `payable_date` in the group
  agrees, the group is a true duplicate (or duplicates) of one real
  declaration — collapsed to a single credit, `payable_date` taken from
  whichever row(s) supplied it (missing `payable_date` on some copies
  never blocks this).
* If the group's rows report **different `gross_declared` values**, or
  **different NON-missing `payable_date` values**, that is a CONFLICT:
  the data disagrees about what actually happened, and this module MUST
  NOT silently pick a row by encounter order — the pre-NEW-2 first-seen-
  wins behavior for an `alpaca_id`-matched pair with a genuinely
  different amount is exactly this failure mode. `strict=True` (the
  default, matching this module's existing `build_corporate_action_events`
  convention) raises `ValueError` naming the conflicting values.
  `strict=False` excludes that (symbol, ex_date, special) event from the
  output entirely — deterministic and order-independent (nothing "wins"),
  never a guess.

Two rows in the SAME group with different `alpaca_id`s are just a
duplicate report of the same declaration under two vendor row identifiers
(no conflict, provided the amount/payable-date agree); `alpaca_id` is
informational only and does not itself gate grouping or conflict
detection — the group's own agreement/disagreement on the economically
meaningful fields is authoritative. Grouping and conflict detection are
computed over the FULL set of rows in a group (via Python `set`
membership), never by streaming row order, so every outcome — true
duplicate, conflict-raise, or conflict-exclude — is identical regardless
of the input list's order.

## FR-1 — credited amount is RAW, never the comparison-rounded value

An independent delta re-review of NEW-2 found that `_resolve_core_identity_
group()` was returning `round(amount, 10)` — the SAME value used to detect
whether a group's rows agree within float-representation tolerance — as
the CREDITED economic amount. On the real 822-row G1 ledger (every group a
singleton, so this never involved a real duplicate-resolution choice) this
silently rounded 39 of 820 credited amounts by up to ~3.34e-11 relative to
the pre-NEW-2 (790979f) output, which credited the raw, unrounded
`gross_declared` value directly. Comparison and the credited value are now
computed separately: `_rounded_for_comparison()` (a real 1e-10 tolerance
for detecting true-duplicate-vs-conflict, not an economic rounding policy)
decides duplicate-vs-conflict; the value actually credited is always the
RAW `gross_declared` of a deterministically chosen representative row —
`min()` over the group's raw amounts, which is order-independent (never
depends on which row the input list happened to place first) and, for
every real G1 group (all singletons), trivially returns that one row's own
raw value unchanged — byte-for-byte identical to `790979f`'s output for
every one of the real ledger's 820 (date, ticker) pairs (see
`test_build_dividend_events_real_g1_ledger_values_match_independent_
aggregation` in `test_validation_lib.py`, which independently re-aggregates
the raw ledger — not by calling this module's own function twice — and
asserts exact value equality, not merely matching counts).

## FR-2/FR-3 — numeric-field validation extended to `gross_declared` and
`ratio_child_per_parent`; overflow normalized to `ValueError`

NEW-1 validated `child_close_on_parent_ex_session` via
`_valid_positive_finite_number()` but left `gross_declared` (dividends) and
`ratio_child_per_parent` (corporate actions) converted through a bare,
unchecked `float()` call — silently accepting a numeric string (`"0.50"`),
a non-finite string (`"inf"`), or `NaN`/`±inf` itself. Both fields are now
validated before any `float()` conversion is trusted:

* `gross_declared` — `_valid_finite_number()` (new): an actual `int`/
  `float` scalar (never `bool`), finite (rejects `NaN`/`±inf`). Unlike
  `_valid_positive_finite_number()`, this does NOT reject zero or negative
  values — a non-positive `gross_declared` is a legitimate "no dividend
  cash" input this module's own `amount <= 0` drop rule already handles
  downstream (and `data_acquisition.py`'s G1 `validate()` already flags a
  non-positive gross as a data-quality issue upstream), not a validation
  failure. Checked once per row, before grouping: `strict=True` (default)
  raises `ValueError` naming the row's identity and the rejected value;
  `strict=False` excludes just that one malformed row (not its whole
  core-identity group, and never any other group) from consideration.
* `ratio_child_per_parent` — validated via the existing
  `_valid_positive_finite_number()` (a spin-off ratio is always a positive
  number of child shares per parent share, the same economic constraint
  `child_close_on_parent_ex_session` already carries), on the same
  strict/nonstrict footing as that field.

Both `_valid_finite_number()` and `_valid_positive_finite_number()` also
now catch `OverflowError` (FR-3): an arbitrary-precision Python `int` whose
magnitude cannot be represented as a `float` (e.g. `10**400`, a shape
`json.load()` can legally produce) previously leaked `OverflowError` — an
exception type this module's own contract never named — straight out of
an unguarded `float()` call. Both helpers now treat that case as `None`
(the same uniform "invalid" outcome as every other failure mode), so it
surfaces as this module's own `ValueError` (or a deterministic nonstrict
exclusion), never an incidental `OverflowError`.

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
import math
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

def _core_identity(row: dict) -> tuple[str, str, bool]:
    """T-D1 CORE economic identity (NEW-2): `(symbol, ex_date, special)` —
    the minimal set of fields that determine whether two rows describe the
    SAME real dividend declaration. Deliberately excludes `gross_declared`
    and `payable_date` (see the module docstring's "Identity model"
    section for the full reasoning) — both are supplemental facts about a
    declaration, not what makes two declarations distinct."""
    return (row["symbol"], row["ex_date"], bool(row.get("special")))


def _valid_finite_number(value: object) -> float | None:
    """FR-2: validates `gross_declared` — an actual `int`/`float` scalar
    (never `bool`, despite `bool` being an `int` subclass), finite
    (rejects `NaN`/`+inf`/`-inf`, and — FR-3 — an out-of-range magnitude
    that would raise `OverflowError` inside `float()`, e.g. `10**400`).
    Deliberately NOT positivity-gated, unlike `_valid_positive_finite_
    number()` below: a non-positive `gross_declared` is a legitimate "no
    dividend cash" input (`build_dividend_events()`'s own `amount <= 0`
    drop rule handles it, not this validator) — `data_acquisition.py`'s G1
    `validate()` already flags a non-positive gross as a data-quality
    issue upstream, but this module stays defensive rather than assuming
    that guarantee holds for every caller. Returns the `float` value on
    success, `None` on any failure (never coerces a numeric string, never
    lets a non-finite or out-of-range value pass silently)."""
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, float)):
        return None
    try:
        numeric = float(value)
    except OverflowError:
        return None
    if not math.isfinite(numeric):
        return None
    return numeric


def _raw_amount(row: dict) -> float:
    """RAW (unrounded) `gross_declared` — the value actually credited
    (FR-1). Callers of this function (`_resolve_core_identity_group`
    below) only ever see rows that already passed `build_dividend_events`'
    own per-row `_valid_finite_number()` filter, so this `float()` call is
    always applied to an already-validated numeric value, never an
    unchecked one."""
    return float(row["gross_declared"])


def _rounded_for_comparison(row: dict) -> float:
    """A real 1e-10 float-representation tolerance used ONLY to decide
    whether a core-identity group's rows are a true duplicate or a
    conflict (FR-1) — never returned as, or mixed into, the credited
    economic amount itself."""
    return round(_raw_amount(row), 10)


def _resolve_core_identity_group(rows: list[dict], *, strict: bool
                                 ) -> tuple[float, str | None] | None:
    """Resolves every row sharing one CORE identity into a single
    `(amount, payable_date)` pair, or detects that the group is a CONFLICT
    (see module docstring). Returns `None` when `strict=False` and a
    conflict was found — the caller excludes that event entirely. Raises
    `ValueError` when `strict=True` and a conflict was found. The decision
    is computed over `set`s of the group's OWN values, never by iteration
    order, so it is identical for any permutation of `rows`.

    FR-1: the returned `amount` is always a RAW (unrounded) value —
    `min()` over the group's raw amounts, a deterministic, order-
    independent tie-break among rows already known (via the rounded
    comparison below) to agree within tolerance. For every real G1
    ledger group (always a singleton), this trivially returns that one
    row's own raw value, unchanged."""
    rounded_set = {_rounded_for_comparison(r) for r in rows}
    if len(rounded_set) > 1:
        if strict:
            raise ValueError(
                f"conflicting gross_declared amounts for {rows[0]['symbol']} "
                f"ex {rows[0]['ex_date']} special={bool(rows[0].get('special'))}: "
                f"{sorted(rounded_set)} — the same declaration was reported with "
                "different amounts; this must be resolved upstream (or pass "
                "strict=False to exclude the event), never silently picked by "
                "row order")
        return None
    amount = min(_raw_amount(r) for r in rows)

    payable_dates = {p for p in (r.get("payable_date") for r in rows) if p}
    if len(payable_dates) > 1:
        if strict:
            raise ValueError(
                f"conflicting payable_date values for {rows[0]['symbol']} "
                f"ex {rows[0]['ex_date']} special={bool(rows[0].get('special'))}: "
                f"{sorted(payable_dates)} — the same declaration was reported "
                "with different payable dates; this must be resolved upstream "
                "(or pass strict=False to exclude the event), never silently "
                "picked by row order")
        return None
    payable_date = next(iter(payable_dates), None)

    return amount, payable_date


def _credited_date_for(ex_date: str, payable_date: str | None, convention: str) -> str:
    if convention == CREDIT_CONVENTION_EX_DATE:
        return ex_date
    if convention == CREDIT_CONVENTION_PAY_DATE_LAG_30D:
        if payable_date and payable_date >= ex_date:
            return payable_date
        return (date.fromisoformat(ex_date)
                + timedelta(days=PAY_DATE_FALLBACK_LAG_DAYS)).isoformat()
    raise ValueError(f"unknown credit_convention {convention!r}; must be one of {CREDIT_CONVENTIONS}")


def build_dividend_events(rows: list[dict], *,
                          credit_convention: str = CREDIT_CONVENTION_EX_DATE,
                          strict: bool = True
                          ) -> dict[str, dict[str, float]]:
    """Build `margin_simulation.simulate()`'s `dividend_events` input:
    `{credited_date: {ticker: gross cash per share}}`.

    T-D1 (NEW-2 refinement of F-5): rows are grouped by CORE identity
    (`_core_identity()` — `symbol`, `ex_date`, `special`) before
    aggregation. Within a group, a TRUE duplicate (agreeing amount, and
    agreeing on every non-missing `payable_date`) credits exactly once
    regardless of how many copies exist or which optional fields any copy
    is missing. A CONFLICT (disagreeing amount and/or disagreeing
    non-missing `payable_date` within a group) is never silently resolved
    by row order: `strict=True` (default, matching this module's existing
    `build_corporate_action_events` convention) raises `ValueError` naming
    the conflicting values; `strict=False` excludes that event from the
    output. Genuinely distinct same-(ticker, credited_date) events (e.g.
    regular + special, which differ in `special` and so form separate
    groups) are summed, matching `simulate()`'s single-per-share-figure-
    per-day contract. A resolved group whose amount is non-positive is
    dropped (no negative or zero dividend cash is ever credited).

    FR-2: every row's `gross_declared` is validated via
    `_valid_finite_number()` BEFORE grouping — an actual `int`/`float`
    scalar, finite (never a numeric string, `NaN`, `±inf`, or an
    out-of-range magnitude, FR-3). `strict=True` (default) raises
    `ValueError` naming the offending row's identity and the rejected
    value; `strict=False` excludes just that one malformed row (never its
    whole core-identity group, and never any other group) from
    consideration."""
    if credit_convention not in CREDIT_CONVENTIONS:
        raise ValueError(f"unknown credit_convention {credit_convention!r}; "
                         f"must be one of {CREDIT_CONVENTIONS}")
    valid_rows: list[dict] = []
    for row in rows:
        if _valid_finite_number(row.get("gross_declared")) is None:
            if strict:
                raise ValueError(
                    f"invalid gross_declared for {row.get('symbol')} ex "
                    f"{row.get('ex_date')} special={bool(row.get('special'))}: "
                    f"{row.get('gross_declared')!r} — must be an actual int/"
                    "float, finite (not NaN/±inf/a numeric string/bool/None/"
                    "out-of-range)")
            continue
        valid_rows.append(row)

    groups: dict[tuple[str, str, bool], list[dict]] = {}
    for row in valid_rows:
        groups.setdefault(_core_identity(row), []).append(row)

    events: dict[str, dict[str, float]] = {}
    for (symbol, ex_date, _special), group_rows in groups.items():
        resolved = _resolve_core_identity_group(group_rows, strict=strict)
        if resolved is None:
            continue
        amount, payable_date = resolved
        if amount <= 0:
            continue
        credited = _credited_date_for(ex_date, payable_date, credit_convention)
        bucket = events.setdefault(credited, {})
        bucket[symbol] = bucket.get(symbol, 0.0) + amount
    return events


# ── corporate-action (spin-off) events ───────────────────────────────────────

def _valid_positive_finite_number(value: object) -> float | None:
    """NEW-1/F-12: accepts ONLY a real numeric SCALAR type (`int` or
    `float`) that is finite and strictly positive; returns the `float`
    value on success, `None` on any failure. Deliberately rejects:

    * `bool` — despite `bool` being an `int` subclass in Python
      (`isinstance(True, int)` is `True`), this module has no documented
      reason to treat a boolean as a numeric price, so it is excluded
      explicitly rather than silently accepted as `1.0`/`0.0`.
    * numeric STRINGS (e.g. `"50.0"`) — a malformed or mistyped field that
      happens to parse is not the same as a field that was actually
      recorded as a number; coercing strings would let a data-quality bug
      upstream pass validation silently. This module never calls `float()`
      on an unchecked value.
    * non-finite values (`NaN`, `+inf`, `-inf`) — a spin-off valuation can
      never legitimately be infinite or undefined.
    * zero and negative values — a distributed security's consolidated
      close is always a positive price.
    * FR-3: an out-of-range magnitude (e.g. an arbitrary-precision int
      like `10**400`, a shape `json.load()` can legally produce) that
      would raise `OverflowError` inside `float()` — caught and treated
      the same as every other failure mode, never leaking `OverflowError`
      past this function.

    `None` is returned uniformly for every failure mode so the caller
    (`build_corporate_action_events` below) has one bar to check, not a
    tangle of a `TypeError`/`OverflowError` here and a range check there."""
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, float)):
        return None
    try:
        numeric = float(value)
    except OverflowError:
        return None
    if not math.isfinite(numeric) or numeric <= 0:
        return None
    return numeric


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
    own reason to tolerate an incomplete record.

    F-12/NEW-1 correction: `child_close_on_parent_ex_session` is validated
    by `_valid_positive_finite_number()` above — only an actual `int`/
    `float` scalar (never `bool`, never a numeric string, never NaN/±inf,
    never non-positive) is accepted. Anything else fails with `ValueError`
    naming the offending event AND the exact rejected value, never an
    incidental `TypeError`, and never a silent string-to-number coercion.

    FR-2: `ratio_child_per_parent` is now validated the SAME way, via the
    same `_valid_positive_finite_number()` — a spin-off ratio (child
    shares per parent share) is always a positive number, the same
    economic constraint `child_close_on_parent_ex_session` already
    carries. Previously this field was converted through a bare, unchecked
    `float()` — silently accepting a numeric string and letting `NaN`/
    `±inf` pass straight through into the output event."""
    out: dict[str, list[dict]] = {}
    for ev in events:
        raw_ratio = ev.get("ratio_child_per_parent")
        ratio = _valid_positive_finite_number(raw_ratio)
        raw_unit_value = ev.get("child_close_on_parent_ex_session")
        unit_value = _valid_positive_finite_number(raw_unit_value)
        if ratio is None or unit_value is None:
            if strict:
                bad_field, bad_value = (
                    ("ratio_child_per_parent", raw_ratio) if ratio is None
                    else ("child_close_on_parent_ex_session", raw_unit_value))
                raise ValueError(
                    f"corporate-action event {ev.get('parent')}->{ev.get('child')} "
                    f"ex {ev.get('ex_date')} has no valid {bad_field} "
                    f"(got {bad_value!r}) — data_acquisition.py's G1 validate() "
                    "should already guarantee this; treat as a data-integrity "
                    "failure, not a silent skip")
            continue
        out.setdefault(ev["ex_date"], []).append({
            "ticker": ev["parent"],
            "ratio": ratio,
            "unit_value": unit_value,
        })
    return out
