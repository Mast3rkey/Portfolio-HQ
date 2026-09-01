#!/usr/bin/env python3
"""
allocate.py — manual-allocation ADVISOR. Recommendations only.

This tool NEVER places, modifies, or cancels an order anywhere. It reads your
holdings + canonical destination targets (targets.yaml, PHQ-2026-02), pulls
market data from Alpaca (read-only), applies your gates (targets.yaml,
gates.yaml, issuer_lookthrough.yaml), and prints/logs a
BUY / TRIM / NO ADD / BLOCKED table plus a short summary. You execute
manually on Robinhood.

Usage:
    python allocate.py update-cash 2000  # sync the TOTAL account cash balance
    python allocate.py --review          # the allocation check (cash is tracked
                                         #   state, not a runtime argument)
    python allocate.py update-shares         # paste "TICKER qty" lines, Ctrl-D (stocks/ETFs)
    python allocate.py update-crypto-shares  # paste "COIN qty" lines, Ctrl-D (BTC/ETH/SOL)
    python allocate.py update-holdings       # paste "TICKER value" lines, Ctrl-D (manual fallback)
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import yaml

from alpaca_client import AlpacaPaperClient
from indicators import compute_all
from regime_gate import regime_ok_from_closes
from earnings import days_until_earnings
from crypto import fetch_crypto
from margin_state import classify_margin_state, concentration_risk_score

HERE = Path(__file__).resolve().parent
TARGETS_FILE = HERE / "targets.yaml"
HOLDINGS_FILE = HERE / "holdings.yaml"
GATES_FILE = HERE / "gates.yaml"
LOOKTHROUGH_FILE = HERE / "issuer_lookthrough.yaml"
LOGS_DIR = HERE / "logs"
PERF_LOG_FILE = HERE / "performance_log.csv"
# `net_equity` keeps its historical meaning (gross - margin_debt) so the existing
# series stays continuous and comparable; `cash` and `book` are ADDED rather than
# redefining it, so tracked cash is never omitted from the recorded book value.
# Rows written before this change carry empty cash/book — honestly blank, not
# back-filled with a number nobody measured.
PERF_FIELDS = ["date", "net_equity", "gross", "margin_debt", "cash", "book",
               "qqq_price", "voo_price", "note"]

DAILY_LIMIT = 320  # margin above the ~290-300 trading days in DAYS_BACK, so a
                    # holiday-heavy stretch can't starve the 200-SMA of bars
DAYS_BACK = 420
STALE_MARGIN_DAYS = 2   # warn if margin debt/buffer haven't been synced in this many days


def _margin_buffer_age_days(synced_at) -> float | None:
    """Days since holdings.yaml's margin.synced_at, or None if missing,
    unparseable, OR in the future. Fails safe: a malformed/absent/future date
    never raises and never yields a fabricated number (0 would read as
    'freshly synced' and hide real staleness; a negative number for a future
    date is nonsensical, not 'fresher than fresh') -- it yields 'age unknown',
    which every caller (render(), classify_margin_state() via main()) treats
    as 'do not judge staleness from this'. Single source of truth so the
    review banner and the risk-classifier's own reasons are always computed
    from the identical age, never contradict each other. Pair with
    _margin_buffer_age_unverifiable() at the call site to distinguish
    'no age info at all' from 'an age was attempted and is invalid' --
    this function alone conflates the two into the same None."""
    if not synced_at:
        return None
    try:
        age = (date.today() - date.fromisoformat(str(synced_at))).days
    except ValueError:
        return None
    return age if age >= 0 else None


def _margin_buffer_age_unverifiable(synced_at) -> bool:
    """True when synced_at is present but does not resolve to a valid,
    non-negative age (malformed string or a future date) or is absent
    entirely -- i.e. whenever _margin_buffer_age_days(synced_at) is None.
    Kept as a distinct call (rather than inferring this from the age being
    None at each call site) so main()'s wiring into classify_margin_state()
    reads as an explicit decision, matching that function's own explicit
    buffer_data_unverifiable parameter."""
    return _margin_buffer_age_days(synced_at) is None


# ── tracked cash state ─────────────────────────────────────────────────────────
#
# Correction F, stated as code rather than assumed: NOTHING in this repository
# models Robinhood preserving a literal cash balance while borrowing on margin.
# Brokers generally apply settled cash before extending credit, and holdings.yaml
# itself records that Robinhood's buffer formula "weights something this simple
# subtraction misses" -- i.e. the mechanics are explicitly NOT modeled here.
# Rather than invent broker behavior, a margin-funded recommendation FAILS
# CLOSED. This is consistent with PHQ-2026-01 item 6 ("No new margin is
# authorized") and changes no accepted number.
MARGIN_CASH_PRESERVATION_UNPROVEN = (
    "margin-funded buys are blocked: this repository has no evidence that a "
    "margin-funded purchase preserves a literal protected cash balance, and "
    "PHQ-2026-01 item 6 authorizes no new margin. Use a cash-funded run.")


#: The three distinct states any persisted numeric observation can be in. A
#: fallback value is NEVER one of them: substituting zero for an unknown, then
#: labelling the result "actual", publishes a knowingly false figure — the exact
#: failure PHQ-2026-07 item 4 forbids.
STATE_CURRENT = "current"
STATE_STALE = "stale"
STATE_UNKNOWN = "unknown"


def _finite_scalar(raw, label: str, *, minimum: float | None = None,
                   maximum: float | None = None) -> tuple[float | None, str | None]:
    """Validate a persisted numeric scalar, fail-closed. Returns (value, reason).

    Rejects, in this order and each for its own reason:

    * ``bool`` — ``True`` is an ``int`` in Python, so ``float(True) == 1.0``
      would silently read as one dollar;
    * anything not an ``int``/``float``;
    * any non-finite value — ``NaN`` in particular defeats EVERY comparison
      (``nan < 30`` and ``nan >= 30`` are both False), so a NaN buffer would
      pass a floor check by passing neither branch of it;
    * anything outside its accepted domain.

    A rejection returns ``(None, reason)``. There is deliberately no fallback
    value: the caller must treat the observation as unknown.
    """
    if isinstance(raw, bool):
        return None, f"{label} is a boolean, not a number: {raw!r}"
    if not isinstance(raw, (int, float)):
        return None, f"{label} is not a number: {raw!r}"
    val = float(raw)
    if not math.isfinite(val):
        return None, f"{label} is not finite: {raw!r}"
    if minimum is not None and val < minimum:
        return None, f"{label} is below its accepted minimum {minimum}: {raw!r}"
    if maximum is not None and val > maximum:
        return None, f"{label} is above its accepted maximum {maximum}: {raw!r}"
    return val, None


def _state_age_days(synced_at) -> float | None:
    """Days since an ISO ``synced_at``, or None when missing, unparseable, or
    in the FUTURE. Identical fail-safe semantics to _margin_buffer_age_days --
    a fabricated 0 would read as 'freshly synced' and hide real staleness, and a
    negative age for a future date is nonsensical rather than 'extra fresh'."""
    if not synced_at:
        return None
    try:
        age = (date.today() - date.fromisoformat(str(synced_at))).days
    except ValueError:
        return None
    return age if age >= 0 else None


def load_cash_state(data: dict | None = None) -> dict:
    """Read holdings.yaml's tracked ``cash:`` block and classify it.

    Per PHQ-2026-07 item 4, the verdict is a THREE-state classification, not a
    boolean:

    * ``current`` — present, valid, in-domain, within STALE_MARGIN_DAYS. The
      only state a dollar recommendation may act on (``usable`` True).
    * ``stale``   — a genuine past observation whose date is too old. The
      balance is RETAINED and may be displayed, but only as stale historical
      evidence carrying its own date. It is never presented as current.
    * ``unknown`` — absent, malformed, non-numeric, non-finite, out-of-domain,
      or undateable. ``balance`` is None. Zero is never substituted for it.

    ``balance`` is the TOTAL account cash balance — never a deposit delta."""
    data = load_yaml(HOLDINGS_FILE) if data is None else (data or {})
    block = data.get("cash")
    out = {"present": False, "balance": None, "synced_at": None, "age_days": None,
           "usable": False, "state": STATE_UNKNOWN, "reason": None}
    if block is None:
        out["reason"] = ("holdings.yaml has no `cash:` block — the total account cash "
                         "balance is unknown, so book value and every target dollar "
                         "figure would be understated. Run: allocate.py update-cash <balance>")
        return out
    if not isinstance(block, dict):
        out["reason"] = "holdings.yaml `cash:` is not a mapping (expected balance + synced_at)"
        return out
    out["present"] = True
    out["synced_at"] = block.get("synced_at")
    # Cash is a non-negative dollar amount. A negative, non-finite, or boolean
    # balance is UNKNOWN, not a small number — see _finite_scalar.
    value, reason = _finite_scalar(block.get("balance"), "holdings.yaml cash.balance",
                                   minimum=0.0)
    if reason is not None:
        out["reason"] = reason
        return out
    age = _state_age_days(out["synced_at"])
    out["age_days"] = age
    if age is None:
        out["reason"] = (f"cash.synced_at is missing, malformed, or in the future "
                         f"({out['synced_at']!r}) — age cannot be established, so this "
                         f"observation cannot be dated and is unknown, not stale")
        return out
    # Past this point the observation is real and dated: it is either current or
    # stale, and in BOTH cases the balance is retained as a genuine observation.
    out["balance"] = value
    if age > STALE_MARGIN_DAYS:
        out["state"] = STATE_STALE
        out["reason"] = (f"cash synced {age}d ago (> {STALE_MARGIN_DAYS}d) — re-sync the "
                         f"actual current balance: allocate.py update-cash <balance>")
        return out
    out["state"] = STATE_CURRENT
    out["usable"] = True
    return out


def load_margin_state(data: dict | None = None) -> dict:
    """Read holdings.yaml's ``margin:`` block and classify it.

    Same three-state contract as load_cash_state. Margin debt participates in
    the book identity (book = invested + cash - debt), so a stale, malformed, or
    out-of-domain margin block must be caught BEFORE it affects book or buying
    capacity -- not merely footnoted afterward. A NEGATIVE debt is rejected
    outright rather than accepted as a small number: ``gross - (-debt)`` ADDS
    capital, silently inflating net equity."""
    data = load_yaml(HOLDINGS_FILE) if data is None else (data or {})
    block = data.get("margin") or {}
    out = {"present": bool(block), "debt": None, "buffer_pct": None,
           "synced_at": block.get("synced_at") if isinstance(block, dict) else None,
           "age_days": None, "usable": False, "state": STATE_UNKNOWN, "reason": None}
    if not isinstance(block, dict) or not block:
        out["reason"] = "holdings.yaml has no usable `margin:` block"
        return out
    debt, reason = _finite_scalar(block.get("debt"), "margin.debt", minimum=0.0)
    if reason is not None:
        out["reason"] = reason
        return out
    # Robinhood displays the buffer as a percentage; 0-100 is its whole accepted
    # domain. Anything outside it is not a buffer reading we can act on.
    # The buffer is REQUIRED, not optional, wherever this state is claimed
    # usable. The 30% buffer floor is a hard cutoff that consumes this value, so
    # a block carrying a current debt and date but a missing or null buffer was
    # previously classified usable with `buffer_pct = None` -- the floor check
    # then had nothing to check. An absent buffer is an unknown buffer, and
    # unknown is never a pass.
    bp = block.get("buffer_pct")
    if bp is None:
        out["reason"] = ("margin.buffer_pct is missing or null — the 30% buffer floor "
                         "cannot be evaluated against an absent reading, so this margin "
                         "observation is unknown, not current")
        return out
    buffer_pct, reason = _finite_scalar(bp, "margin.buffer_pct",
                                        minimum=0.0, maximum=100.0)
    if reason is not None:
        out["reason"] = reason
        return out
    # The parsed values are retained whatever the DATE verdict turns out to be.
    # They are real, validated numbers read off the file, and the pre-existing
    # margin risk-state classifier needs them to distinguish "a buffer exists but
    # its sync date is unverifiable" from "no buffer was ever recorded" -- two
    # materially different warnings. `usable` below, never these fields, is what
    # gates a dollar recommendation.
    out["debt"] = debt
    out["buffer_pct"] = buffer_pct
    age = _state_age_days(out["synced_at"])
    out["age_days"] = age
    if age is None:
        out["reason"] = (f"margin.synced_at is missing, malformed, or in the future "
                         f"({out['synced_at']!r}) — age cannot be established, so this "
                         f"observation cannot be dated and is unknown, not stale")
        return out
    if age > STALE_MARGIN_DAYS:
        out["state"] = STATE_STALE
        out["reason"] = (f"margin synced {age}d ago (> {STALE_MARGIN_DAYS}d) — re-sync: "
                         f"allocate.py update-margin <debt> <buffer_pct>")
        return out
    out["state"] = STATE_CURRENT
    out["usable"] = True
    return out


def valuation_completeness(holdings: dict, data: dict | None = None) -> dict:
    """Prove every nonzero tracked position carries a current value.

    resolve_holdings() falls back to the manual `holdings` dict when a price is
    missing and then drops any zero value, so an unpriced position previously
    VANISHED from gross and book silently. Whether a position is priced is now
    an explicit, reported fact, and an unresolved symbol blocks dollar
    recommendations rather than quietly shrinking the book."""
    data = load_yaml(HOLDINGS_FILE) if data is None else (data or {})
    expected = []
    for tk, qty in (data.get("shares") or {}).items():
        if float(qty) != 0:
            expected.append(tk)
    for c, qty in (data.get("crypto_shares") or {}).items():
        if float(qty) != 0:
            expected.append(c)
    # A resolved value must be a real, finite, nonzero number. bool(nan) is True
    # in Python, so a NaN price would otherwise read as "resolved" and then
    # poison gross, book, and every dollar figure derived from them.
    unresolved = []
    for t in expected:
        val, bad = _finite_scalar(holdings.get(t, 0.0) or 0.0, f"resolved value for {t}")
        if bad is not None or val == 0.0:
            unresolved.append(t)
    unresolved = sorted(unresolved)
    # SEPARATELY from the expected-symbol coverage proof above, every resolved
    # value that is actually present must itself be a finite number. The
    # coverage loop only ever visits symbols enumerated by `shares:`/
    # `crypto_shares:`, so a manual or orphan entry -- one in the resolved set
    # but tracked nowhere -- was never examined at all: `{"MAN": nan}` returned
    # complete=True with expected_count=0, and that NaN then propagated into
    # gross, net_equity and book. These are two different claims (nothing is
    # MISSING; nothing present is MALFORMED) and both must hold.
    invalid = sorted(t for t, v in (holdings or {}).items()
                     if _finite_scalar(v, f"resolved value for {t}")[1] is not None)
    reasons = []
    if unresolved:
        reasons.append("no current value for " + ", ".join(unresolved) +
                       " — these nonzero holdings would silently vanish from the book")
    if invalid:
        reasons.append("non-finite or non-numeric resolved value for " + ", ".join(invalid) +
                       " — this would poison gross, net equity and book")
    return {"expected_count": len(expected), "unresolved": unresolved,
            "invalid": invalid,
            "complete": not unresolved and not invalid,
            "reason": None if not reasons else "; ".join(reasons)}


def current_dollar_availability(cash_state: dict, margin_state: dict,
                                valuation: dict) -> dict:
    """THE single fact: may this run publish CURRENT dollar figures at all?

    PHQ-2026-07 items 4, 5 and 9 each independently block current dollar output,
    and every one of them feeds the SAME book identity:

        book = resolved invested holdings + tracked cash - margin debt

    Cash was previously the only switch. That is not sufficient, because the
    other two terms of that identity can be just as unknown:

    * a STALE margin debt makes `- debt` an unverified number, so book, the
      protected floor and every target dollar derived from book are unverified;
    * an INCOMPLETE valuation means a tracked position is missing from `gross`
      entirely, so book is understated by an amount nobody has measured.

    Either one produces figures that LOOK current. Withdrawing the buys and
    trims does not make the accounting true -- the review's own probes showed a
    numeric book and protected floor published under both conditions.

    This function is the only place that answer is computed. `plan()` and both
    renderers consume its result; none of them re-derives it, so there is no
    second rule that can drift out of agreement with this one.

    What is deliberately NOT gated here: diagnostics that remain independently
    knowable. Margin risk state, buffer proximity and the regime read do not
    depend on cash, so withholding a cash-derived dollar must never silence
    them.
    """
    blocked = []
    if not cash_state.get("usable"):
        blocked.append(f"CASH STATE: {cash_state.get('reason')}")
    if not margin_state.get("usable"):
        blocked.append(f"MARGIN STATE: {margin_state.get('reason')}")
    if not valuation.get("complete"):
        blocked.append(f"VALUATION: {valuation.get('reason')}")
    return {"available": not blocked, "blocked_by": blocked,
            "reason": None if not blocked else "; ".join(blocked)}


# ── protected-capital accounting ───────────────────────────────────────────────
#
# THE CONTRACT, stated once, here.
#
#   book = resolved invested holdings + tracked cash - margin debt
#
# `margin_capacity()` computes net_equity = gross - margin_debt (cash EXCLUDED);
# `plan()` then adds cash exactly once. Tracked cash enters that identity in
# exactly one place.
#
# Some destination capital is deliberately NOT deployable:
#
#   * the CASH row's own target_pct;
#   * the RESERVE row's own target_pct;
#   * the unreconciled destination remainder (100% - destination total) --
#     today 0.7500%, freed by PHQ-2026-04's SPCX retirement and deliberately
#     never renormalized. It is unallocated capital, so it is protected too;
#   * for each actionable-gated name, its UNFILLED target dollars, i.e.
#     max(0, gated_target$ - current gated holding value). A gated name that is
#     already held contributes its held value to the book, so protecting its
#     FULL target in cash on top of that would double-count it.
#
# Previously none of this was computed. RESERVE/CASH were skipped as
# "definitionally satisfied" with no evidence, and protection held only as an
# accidental consequence of the per-name ceiling (max_by_name = target -
# current) capping total buys at the deployable share of book. That is an
# emergent property, not an invariant: nothing asserted it and no test proved
# it. It is asserted and tested now.

CASH_ASSET_CLASS = "cash"
RESERVE_ASSET_CLASS = "reserve"


def _q(x) -> Decimal:
    """Decimal-safe conversion for configuration percentages.

    Destination weights are exact two-decimal configuration values; summing 36
    of them in binary float leaves a residue that makes an exact 100.0000
    comparison meaningless. Every percentage identity below is computed in
    Decimal and only converted to float at the boundary."""
    return Decimal(str(x))


def destination_reconciliation(targets: dict) -> dict:
    """Exact destination-total reconciliation, in Decimal.

    Returns destination_total_pct and unreconciled_pct = 100 - total. A total
    ABOVE 100% is a configuration error and raises: it would mean the canonical
    architecture promises more capital than exists, and every downstream dollar
    figure would be silently inflated."""
    rows = targets.get("destination") or []
    total = sum((_q(r["target_pct"]) for r in rows), Decimal("0"))
    if total > Decimal("100"):
        raise ValueError(
            f"targets.yaml destination total is {total}% — above 100%. The canonical "
            "architecture cannot allocate more than the whole book; refusing to "
            "compute any dollar figure from it.")
    return {"destination_total_pct": float(total),
            "unreconciled_pct": float(Decimal("100") - total)}


def protected_weights(targets: dict, gates_cfg: dict | None = None) -> dict:
    """The static (holdings-independent) protected percentages of book.

    cash_pct + reserve_pct + unreconciled_pct are protected regardless of what
    is held. gated_target_pct is reported for disclosure but is NOT part of the
    static figure — the gated requirement depends on what is already held and is
    computed per-run by protected_capital()."""
    gates_cfg = gates_cfg or {}
    rows = targets.get("destination") or []
    cash_pct = sum((_q(r["target_pct"]) for r in rows
                    if r.get("asset_class") == CASH_ASSET_CLASS), Decimal("0"))
    reserve_pct = sum((_q(r["target_pct"]) for r in rows
                       if r.get("asset_class") == RESERVE_ASSET_CLASS), Decimal("0"))
    gated_pct = sum((_q(r["target_pct"]) for r in rows
                     if r["ticker"] in gates_cfg), Decimal("0"))
    rec = destination_reconciliation(targets)
    unrec = _q(rec["unreconciled_pct"])
    return {
        "cash_pct": float(cash_pct),
        "reserve_pct": float(reserve_pct),
        "unreconciled_pct": float(unrec),
        "gated_target_pct": float(gated_pct),
        "static_protected_pct": float(cash_pct + reserve_pct + unrec),
        "destination_total_pct": rec["destination_total_pct"],
    }


def protected_capital(targets: dict, roster: dict, holdings: dict, book: float | None,
                      actual_cash: float | None, gates_cfg: dict | None = None) -> dict:
    """Full protected-capital accounting for one run.

    protected_floor = book x (cash% + reserve% + unreconciled%)
                    + sum over gated names of max(0, gated_target$ - held$)

    cash_shortfall / cash_surplus are measured against ACTUAL CASH, never
    against buying power. Margin capacity can never satisfy this floor: see
    render()'s margin section and MARGIN_CASH_PRESERVATION_UNPROVEN.

    ``actual_cash`` is None when the current cash observation is stale or
    unknown. PHQ-2026-07 item 4 forbids substituting zero for it, so every
    dollar figure that depends on it -- book, the floor, the per-gated-name
    requirement, shortfall, surplus -- is returned as None and ``cash_known``
    is False. The percentage fields are config-derived and stay knowable in
    every state. A None surplus means nothing is deployable: fail closed."""
    gates_cfg = gates_cfg or {}
    w = protected_weights(targets, gates_cfg)
    cash_known = actual_cash is not None and book is not None
    if not cash_known:
        # No fabricated zero, and no dollar figure derived from a quantity we do
        # not have. Every one of these is genuinely unavailable, not $0.00.
        return {
            **w,
            "cash_known": False,
            "book": None,
            "actual_cash": None,
            "static_protected_dollars": None,
            "gated_cash_required_dollars": None,
            "gated_detail": [],
            "protected_floor_dollars": None,
            "cash_shortfall_dollars": None,
            "cash_surplus_dollars": None,
        }
    book = float(book)
    static_dollars = book * w["static_protected_pct"] / 100.0
    gated_detail = []
    gated_required = 0.0
    for tk in sorted(gates_cfg):
        meta = roster.get(tk)
        if meta is None:
            continue
        target_dollars = book * float(meta["target_pct"]) / 100.0
        held = float(holdings.get(tk, 0.0))
        unfilled = max(0.0, target_dollars - held)
        gated_required += unfilled
        gated_detail.append({"ticker": tk, "target_pct": float(meta["target_pct"]),
                             "target_dollars": target_dollars, "held_dollars": held,
                             "cash_required_dollars": unfilled})
    floor = static_dollars + gated_required
    actual_cash = float(actual_cash)
    return {
        **w,
        "cash_known": True,
        "book": book,
        "actual_cash": actual_cash,
        "static_protected_dollars": static_dollars,
        "gated_cash_required_dollars": gated_required,
        "gated_detail": gated_detail,
        "protected_floor_dollars": floor,
        "cash_shortfall_dollars": max(0.0, floor - actual_cash),
        "cash_surplus_dollars": max(0.0, actual_cash - floor),
    }


# ── config / state io ──────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


# Independent review, PR #202, MAJOR finding 3: the exact, case-sensitive
# vocabulary the canonical v1.30 destination schema supports (targets.yaml's
# own header comment). No other value, and no case variant of these, is
# valid -- an unrecognized or miscased asset_class must fail loudly, never
# silently fall through as tradable ("equity") or non-tradable.
VALID_ASSET_CLASSES = frozenset({"equity", "fund", "crypto", "reserve", "cash"})


def build_roster(targets: dict) -> dict:
    """Return {ticker: {target_pct, asset_class}} from targets.yaml's
    `destination:` list — the canonical v1.30 architecture (PHQ-2026-02).
    Every row (including RESERVE/CASH synthetic sleeves) is included; callers
    that need only market-tradable tickers should filter on asset_class.

    Every row is validated at parse time (independent review, PR #202,
    MAJOR finding 3 + destination-row validation): a missing/blank/
    duplicate ticker, a missing/non-numeric/negative target_pct, or a
    missing/blank/unknown/miscased asset_class each raise loudly, naming
    the offending row, rather than silently defaulting or surfacing as an
    unlabeled KeyError/ValueError deeper in plan()."""
    roster: dict[str, dict] = {}
    for i, row in enumerate(targets.get("destination", []) or []):
        label = f"destination row #{i}"
        if not isinstance(row, dict):
            raise ValueError(f"targets.yaml {label} is not a mapping: {row!r}")

        raw_ticker = row.get("ticker")
        if not isinstance(raw_ticker, str) or not raw_ticker.strip():
            raise ValueError(f"targets.yaml {label} has a missing or blank 'ticker'")
        tk = raw_ticker.strip().upper()
        label = f"targets.yaml destination row #{i} ({tk})"
        if tk in roster:
            raise ValueError(f"{label} is a duplicate ticker")

        if "target_pct" not in row or row["target_pct"] is None:
            raise ValueError(f"{label} is missing 'target_pct'")
        try:
            target_pct = float(row["target_pct"])
        except (TypeError, ValueError):
            raise ValueError(f"{label} has a non-numeric 'target_pct': {row['target_pct']!r}")
        if target_pct < 0:
            raise ValueError(f"{label} has a negative 'target_pct': {target_pct}")

        asset_class = row.get("asset_class")
        if not isinstance(asset_class, str) or not asset_class.strip():
            raise ValueError(f"{label} has a missing or blank 'asset_class'")
        if asset_class != asset_class.strip():
            raise ValueError(f"{label} has a whitespace-padded 'asset_class': {asset_class!r}")
        if asset_class not in VALID_ASSET_CLASSES:
            raise ValueError(
                f"{label} has an unrecognized 'asset_class' {asset_class!r} — "
                f"must be exactly one of {sorted(VALID_ASSET_CLASSES)} "
                "(case-sensitive; no unknown value is silently accepted)")

        roster[tk] = {"target_pct": target_pct, "asset_class": asset_class}
    return roster


def load_gates() -> dict[str, dict]:
    """Actionable gates, represented separately from targets.yaml per
    PHQ-2026-02 — {ticker: {status, authority, allow_add, next_gate, ...}}.
    A gated ticker's target capital is never bought and never renormalized
    into any other name (see gates.yaml, plan()).

    gates.yaml is MANDATORY under the canonical PHQ-2026-02 architecture —
    a gated ticker (e.g. SPCX) becoming an ordinary, unflagged buy candidate
    because its gate config failed to load would be a silent policy breach,
    not a benign absence. Missing, unreadable, malformed, or structurally
    invalid configuration must never be interpreted as an empty gate set;
    this fails loudly instead, mirroring _resolve_margin_config()'s existing
    fail-loud convention (NUM-0001 P1-1) for the same reason: both are
    safety-critical parameters where a wrong default is worse than a crash.
    Independent review, PR #202, MAJOR finding 1."""
    if not GATES_FILE.exists():
        raise ValueError(
            f"gates.yaml is missing ({GATES_FILE}) — required under the "
            "canonical PHQ-2026-02 architecture; cannot safely treat this "
            "as 'no gates', which would let a gated ticker appear as an "
            "ordinary buy candidate")
    try:
        raw = GATES_FILE.read_text()
    except OSError as e:
        raise ValueError(f"gates.yaml could not be read ({GATES_FILE}): {e}")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise ValueError(f"gates.yaml is not valid YAML ({GATES_FILE}): {e}")
    if not isinstance(data, dict):
        raise ValueError(
            f"gates.yaml ({GATES_FILE}) must parse to a mapping with a "
            f"top-level 'gates' key, got {type(data).__name__}")
    gate_list = data.get("gates")
    if gate_list is None:
        raise ValueError(f"gates.yaml ({GATES_FILE}) is missing its top-level 'gates' key")
    if not isinstance(gate_list, list):
        raise ValueError(
            f"gates.yaml ({GATES_FILE}) 'gates' key must be a list, "
            f"got {type(gate_list).__name__}")
    result: dict[str, dict] = {}
    for i, g in enumerate(gate_list):
        if not isinstance(g, dict) or not g.get("ticker"):
            raise ValueError(
                f"gates.yaml ({GATES_FILE}) entry #{i} is missing a required "
                "'ticker' field")
        result[str(g["ticker"]).upper()] = g
    return result


def load_issuer_lookthrough() -> dict:
    """8%/40% no-add control configuration (PHQ-2026-02) — issuer
    ceiling/common-driver ceiling, the retained point-in-time 40.0284%
    measurement, and the hand-maintained ETF look-through constituent
    weights (never live-fetched — see issuer_lookthrough.yaml header)."""
    if not LOOKTHROUGH_FILE.exists():
        return {}
    return load_yaml(LOOKTHROUGH_FILE) or {}


# ── data acquisition ───────────────────────────────────────────────────────────

def fetch_market(client, tickers: list[str], regime_ticker: str) -> tuple[dict, bool, list]:
    """Fetch indicators for every ticker + the regime signal. Returns
    (metrics_by_ticker, regime_ok, regime_closes_len_flag)."""
    metrics: dict[str, dict] = {}
    all_syms = sorted(set(tickers) | {regime_ticker})
    regime_bars = None
    for sym in all_syms:
        try:
            bars = client.get_bars(sym, "1Day", DAILY_LIMIT, DAYS_BACK)
        except Exception as e:
            metrics[sym] = {"error": str(e)[:80]}
            continue
        if sym == regime_ticker:
            regime_bars = bars
        if not bars:
            metrics[sym] = {"error": "no bars"}
            continue
        metrics[sym] = compute_all(bars)

    if regime_bars:
        closes = [float(b["c"]) for b in regime_bars]
        regime_ok = regime_ok_from_closes(closes)
        regime_known = len(closes) >= 2
    else:
        regime_ok, regime_known = False, False
    return metrics, regime_ok, regime_known


def resolve_holdings(client, metrics: dict | None = None,
                     crypto_prices: dict | None = None) -> dict[str, float]:
    """Live-value every share-tracked position (qty x latest price); fall back to the
    manual dollar snapshot in 'holdings' for anything with no share/coin count or no
    live price. 'shares' and 'crypto_shares' are the source of truth
    for any ticker/coin present there; 'holdings' entries are only the fallback/override
    layer. Pass 'metrics' (from fetch_market) and 'crypto_prices' ({coin: price}, e.g.
    from crypto.fetch_crypto) to reuse prices already fetched this run and avoid a
    second round of API calls; omit either to fetch fresh (e.g. from log_performance()
    running standalone)."""
    data = load_yaml(HOLDINGS_FILE)
    shares = data.get("shares", {}) or {}
    crypto_shares = data.get("crypto_shares", {}) or {}
    result = dict(data.get("holdings", {}) or {})
    for t, qty in shares.items():
        price = metrics.get(t, {}).get("price") if metrics else None
        if price is None:
            try:
                bars = client.get_bars(t, "1Day", 1, days_back=5)
                price = bars[-1]["c"] if bars else None
            except Exception:
                price = None
        if price is not None:
            result[t] = round(float(qty) * float(price), 2)
        # else: leave whatever 'holdings' already had for t (or nothing), rather
        # than silently dropping/zeroing a position on a transient price-fetch miss.
    if crypto_shares:
        prices = crypto_prices
        if prices is None:
            try:
                raw = client.get_crypto_latest([f"{c}/USD" for c in crypto_shares])
                prices = {c: raw.get(f"{c}/USD") for c in crypto_shares}
            except Exception:
                prices = {}
        for c, qty in crypto_shares.items():
            px = (prices or {}).get(c)
            if px is not None:
                result[c] = round(float(qty) * float(px), 2)
            # else: same fallback-to-manual-value behavior as stocks above.
    return {t: v for t, v in result.items() if v}


# ── core allocation logic ──────────────────────────────────────────────────────

def _resolve_margin_config(targets: dict) -> tuple[float, float]:
    """targets.yaml is the sole canonical owner of leverage_cap/buffer_floor_pct.
    Both are safety-critical (the 1.8x cap and 30% floor) so a missing or
    malformed margin: block must fail loudly rather than silently substitute
    the historical 1.8/30.0 defaults (NUM-0001 P1-1)."""
    margin_cfg = targets.get("margin")
    if not isinstance(margin_cfg, dict):
        raise ValueError(
            "targets.yaml 'margin' block is missing or not a mapping — "
            "required keys: leverage_cap, buffer_floor_pct")
    missing = [k for k in ("leverage_cap", "buffer_floor_pct") if k not in margin_cfg]
    if missing:
        raise ValueError(
            f"targets.yaml 'margin' block missing required key(s): {', '.join(missing)}")
    try:
        leverage_cap = float(margin_cfg["leverage_cap"])
        buffer_floor_pct = float(margin_cfg["buffer_floor_pct"])
    except (TypeError, ValueError):
        raise ValueError(
            "targets.yaml 'margin' block has a non-numeric leverage_cap or "
            "buffer_floor_pct")
    return leverage_cap, buffer_floor_pct


def margin_capacity(gross, margin_debt, cash, leverage_cap, buffer_pct, buffer_floor_pct,
                    margin_requested):
    """Structural leverage-cap + buffer-floor check (July 2026 margin doctrine).
    Buffer is a capacity ceiling, not a timing throttle — hard cutoff, no taper.
    Returns (net_equity, margin_allowed, forced_delever, block_reason)."""
    net_equity = gross - margin_debt
    if buffer_pct is not None and buffer_pct < buffer_floor_pct:
        return net_equity, 0.0, True, (
            f"buffer {buffer_pct:.1f}% < {buffer_floor_pct:.0f}% floor — forced de-lever")
    max_by_leverage = max(0.0, leverage_cap * (net_equity + cash) - gross - cash)
    allowed = min(margin_requested, max_by_leverage)
    reason = "" if allowed >= margin_requested - 1e-9 else (
        f"leverage cap {leverage_cap:.2f}x (max additional margin ${max_by_leverage:,.0f})")
    return net_equity, allowed, False, reason


def _issuer_exposure(holdings: dict, book: float, lookthrough: dict) -> dict:
    """Current effective issuer/common-driver exposure computed from LIVE
    reconciled holdings + current prices (never the frozen retained
    measurement) — PHQ-2026-02 Phase 7/8. effective_pct = direct + embedded
    (via the hand-maintained, point-in-time fund_holding_weight constituent
    table in issuer_lookthrough.yaml — never a live ETF-constituent fetch)."""
    issuers = {}
    common_driver_pct = 0.0
    for iss in lookthrough.get("issuers", []) or []:
        tk = iss["ticker"].upper()
        direct_pct = (float(holdings.get(tk, 0.0)) / book * 100.0) if book > 0 else 0.0
        embedded_pct = 0.0
        for f in iss.get("funds", []) or []:
            fund_pct_of_book = (float(holdings.get(f["fund"].upper(), 0.0)) / book * 100.0) if book > 0 else 0.0
            embedded_pct += fund_pct_of_book * float(f["fund_holding_weight"])
        effective_pct = direct_pct + embedded_pct
        issuers[tk] = {"direct_pct": direct_pct, "embedded_pct": embedded_pct,
                       "effective_pct": effective_pct}
        common_driver_pct += effective_pct
    return {"issuers": issuers, "common_driver_current_pct": common_driver_pct}


def plan(targets, holdings, roster, metrics, regime_ok, regime_known, cash,
         margin_debt=0.0, margin_buffer_pct=None, margin_requested=0.0,
         gates_cfg=None, lookthrough=None, holdings_state=None,
         dollars_available=True):
    """PHQ-2026-02 canonical-destination allocator. `roster` is
    build_roster()'s per-ticker {target_pct, asset_class} (canonical v1.30 —
    see targets.yaml). `gates_cfg` is load_gates()'s output (actionable
    gates, represented separately — a gated ticker is never a buy candidate
    and its target capital is never renormalized into another name, it
    simply never enters buy_candidates). `lookthrough` is
    load_issuer_lookthrough()'s output (8%/40% no-add controls).

    `cash` is None when the current cash observation is stale or unknown.
    PHQ-2026-07 item 4: no zero is substituted for it.

    `dollars_available` carries the caller's answer to the OTHER preconditions
    on current dollar output -- current margin state and complete valuation --
    as computed by `current_dollar_availability()`, which is their only owner.
    `main()` always supplies it. It defaults True for direct callers that are
    exercising allocation mechanics and are asserting nothing about observational
    freshness; for such a caller the effective rule is exactly `cash is not None`,
    which is what it was before. It is deliberately a supplied FACT rather than a
    second derivation, so no competing availability rule can drift from the owner.

    When current dollars are unavailable for ANY of those reasons, ranking and gap
    ordering still run so the observational view survives, but `book`, `cash`, and
    every protected-capital dollar figure are returned as None,
    `dollars_available` is False, and NOTHING is deployable -- the cash surplus
    that bounds buys is unavailable, so it funds nothing."""
    gates = targets.get("gates", {})
    caps = targets.get("caps", {})
    gates_cfg = gates_cfg or {}
    lookthrough = lookthrough or {}
    min_lot = float(gates.get("min_lot_dollars", 25))
    trend_rsi_override = float(gates.get("trend_rsi_override", 30))
    blackout_days = int(gates.get("earnings_blackout_days", 7))
    issuer_ceiling = float(lookthrough.get("issuer_ceiling_pct", 8.0))
    common_driver_ceiling = float(lookthrough.get("common_driver_ceiling_pct", 40.0))
    lookthrough_issuer_tickers = {i["ticker"].upper() for i in lookthrough.get("issuers", []) or []}
    lookthrough_fund_tickers = {f["fund"].upper() for i in lookthrough.get("issuers", []) or []
                                for f in i.get("funds", []) or []}
    # Correlated-cluster concentration caps (semis, power/infra, ...) — each measured
    # against book (net equity), mechanically trimmed on breach, no RSI gate. A ticker
    # may belong to more than one cluster; every cluster it's in must have room for a buy.
    clusters = [{"name": c["name"], "pct": float(c["pct"]),
                "tickers": {t.upper() for t in c["tickers"]}}
               for c in (caps.get("clusters", []) or [])]
    leverage_cap, buffer_floor_pct = _resolve_margin_config(targets)

    gross = sum(float(v) for v in holdings.values())
    # PHQ-2026-07 item 4. A None cash observation is UNKNOWN, never zero. The
    # ranking below still needs a finite scale to order gaps by, so it uses net
    # equity alone -- but that number never escapes as `book`, and every dollar
    # figure derived from it is withheld, because a book computed without a
    # cash balance we do not have is not the book.
    # ONE switch, from the one owner. Cash alone was insufficient: a stale margin
    # debt or an unresolved tracked position leaves book unverified or understated
    # while cash itself is perfectly current.
    dollars_ok = (cash is not None) and bool(dollars_available)
    cash_value = float(cash) if cash is not None else 0.0
    net_equity, margin_allowed, forced_delever, margin_block_reason = margin_capacity(
        gross, margin_debt, cash_value, leverage_cap, margin_buffer_pct,
        buffer_floor_pct, float(margin_requested))
    book = net_equity + cash_value           # doctrine: book = net equity + tracked cash
    # ---- PROTECTED-CAPITAL ACCOUNTING -------------------------------------
    # Cash-funded buys are bounded by the CASH SURPLUS -- actual cash above the
    # protected floor -- never by raw cash and never by buying power. Margin is
    # reported separately and, per MARGIN_CASH_PRESERVATION_UNPROVEN, may not
    # fund buys at all: there is no evidence it preserves literal cash.
    protection = protected_capital(targets, roster, holdings,
                                   book if dollars_ok else None,
                                   cash_value if dollars_ok else None, gates_cfg)
    # Valuation completeness is computed against the tracked state, so an
    # unpriced nonzero holding is a REPORTED fact rather than a silent
    # disappearance from gross/book. `holdings_state` is injectable for tests;
    # production passes the real holdings.yaml mapping.
    valuation = valuation_completeness(holdings, holdings_state)
    margin_funding_blocked = float(margin_requested) > 0
    # None surplus (unknown cash) deploys nothing. Fail closed, not open.
    deployable = protection["cash_surplus_dollars"] or 0.0
    # per-cluster running value + per-ticker target/current, for the mechanical trim below
    cluster_value = {c["name"]: sum(float(holdings.get(t, 0)) for t in c["tickers"])
                     for c in clusters}
    cluster_info: dict[str, dict[str, dict]] = {c["name"]: {} for c in clusters}

    exposure = _issuer_exposure(holdings, book, lookthrough)
    common_driver_running_pct = exposure["common_driver_current_pct"]
    issuer_running_pct = {tk: v["effective_pct"] for tk, v in exposure["issuers"].items()}

    rows: list[dict] = []          # BLOCKED / info rows
    buy_candidates: list[dict] = []
    trims: list[dict] = []
    no_add_gated: list[dict] = []   # PHQ-2026-02: gated destination capital, held as cash

    for tk, meta in roster.items():
        asset_class = meta["asset_class"]
        m = metrics.get(tk, {}) if asset_class != "crypto" else {}
        target_dollars = book * meta["target_pct"] / 100.0
        current = float(holdings.get(tk, 0.0))
        gap = target_dollars - current
        price = m.get("price")
        rsi = m.get("rsi14")
        sma200 = m.get("sma200")
        vs200 = ((price / sma200 - 1) * 100) if (price and sma200) else None

        base = {"ticker": tk, "asset_class": asset_class, "price": price, "rsi": rsi,
                "vs200": vs200, "target": target_dollars, "current": current,
                "gap": gap}
        tk_clusters = [c["name"] for c in clusters if tk in c["tickers"]]
        gate = gates_cfg.get(tk)
        # Independent review, PR #202, MAJOR finding 2: a gated or synthetic
        # non-tradable (reserve/cash) row must never become a mechanical
        # cluster-trim candidate, even if a future config mistakenly lists
        # one as a cluster member — a gate blocks adds, it must never create
        # or permit an automatic sale. Guarded here, at the single source
        # cluster_info feeds, rather than by filtering candidates later.
        trim_eligible = asset_class not in ("reserve", "cash") and gate is None
        if trim_eligible:
            for cname in tk_clusters:
                cluster_info[cname][tk] = {"current": current, "target": target_dollars,
                                           "price": price, "rsi": rsi, "asset_class": asset_class}

        # ---- RESERVE/CASH: never a buy candidate ---------------------------
        # They are not market instruments, so they are never PURCHASED here.
        # Their satisfaction is NOT assumed: protected_capital() proves it
        # against the tracked cash balance, and a shortfall blocks buys.
        if asset_class in ("reserve", "cash"):
            continue

        # ---- GATED (PHQ-2026-02): target capital held as cash, no renormalize --
        if gate is not None:
            no_add_gated.append({**base, "action": "NO ADD — GATED",
                                 "status": gate.get("status"),
                                 "authority": gate.get("authority"),
                                 "next_gate": gate.get("next_gate"),
                                 "holds_existing_shares": bool(current > 0)})
            continue

        # ---- only underweight names are buy candidates -------------------
        if gap < min_lot:
            continue
        if asset_class != "crypto" and (m.get("error") or price is None):
            rows.append({**base, "action": "BLOCKED", "dollars": 0,
                         "reason": f"no-data ({m.get('error','insufficient bars')})"})
            continue

        # No trend/RSI/earnings timing gate for crypto (Decisions Log, July
        # 2026: conviction-sizing, not a timing call — unchanged by this
        # migration).
        if asset_class != "crypto":
            # ---- TREND gate -------------------------------------------------
            if sma200 is not None and price < sma200:
                if rsi is None or rsi >= trend_rsi_override:
                    rows.append({**base, "action": "BLOCKED", "dollars": 0,
                                 "reason": f"downtrend (px {vs200:+.1f}% vs 200SMA, RSI "
                                           f"{'n/a' if rsi is None else f'{rsi:.0f}'})"})
                    continue

            # ---- EARNINGS gate ------------------------------------------------
            de = days_until_earnings(tk)
            if de is None:
                base["earn_flag"] = "earnings:unavailable"
            elif 0 <= de <= blackout_days:
                rows.append({**base, "action": "BLOCKED", "dollars": 0,
                             "reason": f"earnings in {de}d"})
                continue

        max_by_name = max(0.0, target_dollars - current)  # canonical destination is the ceiling

        buy_candidates.append({**base, "clusters": tk_clusters,
                               "max_by_name": max_by_name,
                               "want": min(gap, max_by_name),
                               "earn_flag": base.get("earn_flag", "")})

    # ---- CLUSTER CAPS: mechanical trim, no RSI gate --------------------------
    # Correlation/concentration risk limit, not a return-timing call. Names
    # already trimmed (or by an earlier cluster in this loop) are skipped;
    # trims largest-overweight-first, floored at each name's own target.
    already_trimmed = {t["ticker"] for t in trims}
    for c in clusters:
        cname, cap_pct = c["name"], c["pct"]
        info = cluster_info[cname]
        cap_dollars = book * cap_pct / 100.0
        excess = cluster_value[cname] - cap_dollars
        if excess < min_lot:
            continue
        candidates = sorted(
            ({"ticker": tk, **i, "overweight": i["current"] - i["target"]}
             for tk, i in info.items()
             if tk not in already_trimmed and i["current"] - i["target"] >= min_lot),
            key=lambda x: x["overweight"], reverse=True)
        for cand in candidates:
            if excess < min_lot:
                break
            amt = min(cand["overweight"], excess)
            if amt < min_lot:
                continue
            trims.append({
                "ticker": cand["ticker"], "asset_class": cand["asset_class"],
                "price": cand["price"], "rsi": cand["rsi"], "vs200": None,
                "target": cand["target"], "current": cand["current"],
                "gap": cand["target"] - cand["current"],
                "action": "TRIM", "dollars": amt,
                "reason": f"{cname} cluster cap {cap_pct:.0f}% "
                          f"(${cand['overweight']:,.0f} over own target)"})
            cluster_value[cname] -= amt
            excess -= amt
            already_trimmed.add(cand["ticker"])
            for c2 in clusters:
                if cand["ticker"] in cluster_info[c2["name"]]:
                    cluster_info[c2["name"]][cand["ticker"]]["current"] = cand["current"] - amt

    # ---- greedy allocation to largest passing gaps -----------------------
    # PHQ-2026-02 Phase 7/8: 8% effective-issuer and 40% common-driver
    # ceilings are NO-ADD controls (never a trim/sell), applied here as a
    # clip-or-block on the buy amount, same mechanism as a cluster cap.
    cluster_pct = {c["name"]: c["pct"] for c in clusters}
    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    # Actual cash spent this cycle, tracked separately from buying power so
    # cash_after_plan can never be inflated by unused margin capacity.
    cash_left = deployable
    cash_spent = 0.0
    buys: list[dict] = []
    no_add_issuer: list[dict] = []
    no_add_common_driver: list[dict] = []
    for c in buy_candidates:
        tk = c["ticker"]
        want = min(c["gap"], c["max_by_name"])
        blocked_by = None
        for cname in c["clusters"]:
            room = book * cluster_pct[cname] / 100.0 - cluster_value[cname]
            if room < min_lot:
                blocked_by = cname
                break
            want = min(want, room)
        if blocked_by:
            rows.append({**c, "action": "BLOCKED", "dollars": 0,
                         "reason": f"{blocked_by} cluster cap {cluster_pct[blocked_by]:.0f}%"})
            continue

        # ---- 8% effective-issuer no-add ceiling --------------------------
        issuer_blocked = False
        if tk in lookthrough_issuer_tickers and book > 0:
            cur_pct = issuer_running_pct.get(tk, 0.0)
            if cur_pct >= issuer_ceiling:
                no_add_issuer.append({**c, "action": "NO ADD — ISSUER CEILING",
                                      "current_effective_pct": cur_pct,
                                      "ceiling_pct": issuer_ceiling})
                issuer_blocked = True
            else:
                room_pct = issuer_ceiling - cur_pct
                room_dollars = room_pct / 100.0 * book
                want = min(want, room_dollars)
        if issuer_blocked:
            continue
        # A fund purchase (SPY/VEA/VWO) embeds proportionally into every
        # issuer it backs — clip to the tightest room among all of them too.
        if tk in lookthrough_fund_tickers and book > 0:
            for iss in lookthrough.get("issuers", []) or []:
                for f in iss.get("funds", []) or []:
                    if f["fund"].upper() != tk:
                        continue
                    iss_tk = iss["ticker"].upper()
                    cur_pct = issuer_running_pct.get(iss_tk, 0.0)
                    fhw = float(f["fund_holding_weight"])
                    if fhw <= 0:
                        continue
                    if cur_pct >= issuer_ceiling:
                        want = 0.0
                        continue
                    room_pct = issuer_ceiling - cur_pct
                    room_dollars = (room_pct / fhw) / 100.0 * book
                    want = min(want, room_dollars)

        # ---- 40% AI/platform common-driver no-add ceiling ----------------
        is_common_driver_member = tk in lookthrough_issuer_tickers or tk in lookthrough_fund_tickers
        if is_common_driver_member and book > 0:
            if common_driver_running_pct >= common_driver_ceiling:
                no_add_common_driver.append({**c, "action": "NO ADD — COMMON-DRIVER CEILING",
                                             "current_common_driver_pct": common_driver_running_pct,
                                             "ceiling_pct": common_driver_ceiling})
                continue
            else:
                room_pct = common_driver_ceiling - common_driver_running_pct
                # marginal common-driver contribution per dollar of this buy:
                # direct issuer = 1:1; fund = sum of its backed issuers' fund_holding_weight
                if tk in lookthrough_issuer_tickers:
                    marginal_frac = 1.0
                else:
                    marginal_frac = sum(
                        float(f["fund_holding_weight"])
                        for iss in lookthrough.get("issuers", []) or []
                        for f in iss.get("funds", []) or []
                        if f["fund"].upper() == tk)
                if marginal_frac > 0:
                    room_dollars = (room_pct / marginal_frac) / 100.0 * book
                    want = min(want, room_dollars)

        alloc = min(want, cash_left)
        if alloc < min_lot:
            if cash_left < min_lot and deployable > 0:
                rows.append({**c, "action": "BLOCKED", "dollars": 0,
                             "reason": "cash exhausted"})
            continue
        buys.append({**c, "action": "BUY", "dollars": alloc,
                     "reason": c.get("earn_flag", "")})
        cash_left -= alloc
        cash_spent += alloc
        for cname in c["clusters"]:
            cluster_value[cname] += alloc
        alloc_pct_of_book = (alloc / book * 100.0) if book > 0 else 0.0
        if tk in lookthrough_issuer_tickers:
            issuer_running_pct[tk] = issuer_running_pct.get(tk, 0.0) + alloc_pct_of_book
            common_driver_running_pct += alloc_pct_of_book
        elif tk in lookthrough_fund_tickers:
            for iss in lookthrough.get("issuers", []) or []:
                for f in iss.get("funds", []) or []:
                    if f["fund"].upper() != tk:
                        continue
                    iss_tk = iss["ticker"].upper()
                    delta = alloc_pct_of_book * float(f["fund_holding_weight"])
                    issuer_running_pct[iss_tk] = issuer_running_pct.get(iss_tk, 0.0) + delta
                    common_driver_running_pct += delta

    deployed_total = sum(b["dollars"] for b in buys)
    # Every buy above is cash-funded and bounded by cash_surplus_dollars, so
    # margin_used is structurally zero. Kept explicit rather than removed so the
    # margin section still reports honestly, and asserted below.
    margin_used = 0.0
    if dollars_ok:
        cash_after_plan = protection["actual_cash"] - cash_spent
        # THE INVARIANT. Cash-funded buys may never breach the protected floor,
        # and unused margin may never disguise a breach. Asserted, not emergent.
        assert cash_spent <= protection["cash_surplus_dollars"] + 1e-6, (
            f"cash-funded buys ${cash_spent:,.2f} exceed cash surplus "
            f"${protection['cash_surplus_dollars']:,.2f}")
        assert cash_after_plan >= protection["protected_floor_dollars"] - 1e-6 or \
            protection["cash_shortfall_dollars"] > 0, (
            f"cash after plan ${cash_after_plan:,.2f} is below the protected floor "
            f"${protection['protected_floor_dollars']:,.2f}")
    else:
        # Unknown cash: there is no post-plan cash figure to report, and the
        # complementary invariant is that nothing was funded at all.
        cash_after_plan = None
        assert cash_spent == 0.0, (
            f"cash-funded buys ${cash_spent:,.2f} were made while the cash "
            f"observation was stale or unknown")

    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    unresolved = {t: float(v) for t, v in holdings.items() if t.upper() not in roster}
    leverage_current = (gross / net_equity) if net_equity > 0 else None
    return {
        # `book`/`cash` are None when the cash observation is unusable: a book
        # computed without a cash balance we do not have is not the book.
        "book": book if dollars_ok else None,
        "cash": cash_value if dollars_ok else None,
        "dollars_available": dollars_ok,
        "cash_left": cash_left if dollars_ok else None,
        # Actual cash, kept strictly distinct from buying power.
        "cash_spent": cash_spent,
        "cash_after_plan": cash_after_plan,
        "cash_funded_capacity": protection["cash_surplus_dollars"],
        "unused_margin_capacity": max(0.0, margin_allowed - margin_used),
        "margin_funding_blocked": margin_funding_blocked,
        "margin_funding_block_reason": (
            MARGIN_CASH_PRESERVATION_UNPROVEN if margin_funding_blocked else None),
        "protection": protection,
        "valuation": valuation,
        "buys": buys, "trims": trims, "blocked": rows,
        "underweight": buy_candidates,
        "no_add_gated": no_add_gated,
        "no_add_issuer": no_add_issuer,
        "no_add_common_driver": no_add_common_driver,
        "unresolved": unresolved,
        "orphans": unresolved,   # retained alias — see render()
        "issuer_exposure": exposure["issuers"],
        "common_driver_current_pct": exposure["common_driver_current_pct"],
        "common_driver_ceiling_pct": common_driver_ceiling,
        "issuer_ceiling_pct": issuer_ceiling,
        "retained_common_driver_measurement": lookthrough.get("retained_common_driver_measurement"),
        "regime_ok": regime_ok, "regime_known": regime_known,
        "clusters": [
            {
                "name": c["name"], "value": cluster_value[c["name"]], "pct": c["pct"],
                "current_pct": (cluster_value[c["name"]] / book * 100.0) if book > 0 else None,
                "ratio_to_cap": (cluster_value[c["name"]] / (book * c["pct"] / 100.0))
                                if (c["pct"] > 0 and book > 0) else None,
            }
            for c in clusters
        ],
        "margin": {
            "gross": gross, "net_equity": net_equity, "debt": margin_debt,
            "buffer_pct": margin_buffer_pct, "buffer_floor_pct": buffer_floor_pct,
            "leverage_current": leverage_current, "leverage_cap": leverage_cap,
            "requested": float(margin_requested), "allowed": margin_allowed,
            "used": margin_used, "forced_delever": forced_delever,
            "block_reason": margin_block_reason,
        },
    }


# ── rendering ──────────────────────────────────────────────────────────────────

def _unavailability_reason(result) -> str:
    """Why current dollars are withheld, in the reader's words.

    The superseded text always said "cash observation is not current", which is
    wrong -- and misleadingly so -- whenever cash is perfectly current and it is
    the MARGIN state or an unresolved position that blocks. Read from the one
    owner's own result when present; fall back to the generic phrasing only for
    a direct plan() caller that supplied no availability fact.
    """
    av = result.get("dollar_availability") or {}
    reason = av.get("reason")
    return reason if reason else "a required current observation is unavailable"


def _fmt_row(r, dollars_available: bool = True):
    px = f"${r['price']:.2f}" if r.get("price") else "n/a"
    rsi = f"{r['rsi']:.0f}" if r.get("rsi") is not None else "n/a"
    vs = f"{r['vs200']:+.1f}%" if r.get("vs200") is not None else "n/a"
    # A gap dollar figure is book-derived, and book is unknown when the cash
    # observation is not current. PHQ-2026-07 item 4: withhold, never estimate.
    if not dollars_available:
        dollars = "n/a"
    else:
        dollars = f"${r['dollars']:,.0f}" if r.get("dollars") else "—"
    action = r["action"] + (f": {r['reason']}" if r.get("reason") else "")
    return f"| {r['ticker']:<6} | {action:<34} | {dollars:>8} | {px:>8} | {rsi:>4} | {vs:>7} |"


def render(result, review: bool) -> str:
    L = []
    #: Is the cash observation current? Gates every book-derived DOLLAR figure
    #: below. Percentages, tickers, prices, RSI and trend are unaffected -- they
    #: do not depend on the cash balance, so the observational view survives.
    _ck = bool(result.get("dollars_available", True))
    regime = ("ABOVE 200-EMA (risk-on)" if result["regime_ok"]
              else "BELOW 200-EMA (risk-off)") if result["regime_known"] else "UNKNOWN"

    L.append(f"# Allocation advisory — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    if result.get("dollars_available", True):
        L.append(f"**Book:** ${result['book']:,.0f}  |  "
                 f"**Tracked cash:** ${result['cash']:,.0f}  |  "
                 f"**Regime (QQQ):** {regime}")
    else:
        # PHQ-2026-07 item 4. No dollar book, and no "$0" standing in for a
        # balance we do not have.
        L.append(f"**Book:** UNAVAILABLE ({_unavailability_reason(result)})  |  "
                 f"**Regime (QQQ):** {regime}")
    L.append("")

    # ---- ACTIONABILITY BANNER, first, before any dollar figure -------------
    if result.get("actionable") is False:
        L.append("> ## ⛔ NON-ACTIONABLE — dollar recommendations withdrawn")
        L.append(">")
        for b in result.get("actionable_blocks", []):
            L.append(f"> - {b}")
        L.append(">")
        L.append("> The table below is OBSERVATIONAL ONLY. No buy or trim below may be "
                 "executed until every block above is cleared.")
        L.append("")

    # ---- PROTECTED-CAPITAL ACCOUNTING --------------------------------------
    prot = result.get("protection")
    if prot and not prot.get("cash_known", True):
        # ---- UNKNOWN/STALE CASH: percentages only, no dollar figure ---------
        # Every dollar quantity here depends on a cash balance that is not
        # current. PHQ-2026-07 item 4 forbids presenting a derived fallback as
        # observed, so they are withheld rather than shown as $0.00.
        cs = result.get("cash_state") or {}
        L.append("### Protected-capital accounting — DOLLAR FIGURES UNAVAILABLE")
        L.append("")
        L.append(f"The cash observation is **{cs.get('state', 'unknown')}**, so book, the "
                 "protected floor, every target dollar figure, and any shortfall are "
                 "**unavailable** — not zero, and not estimated.")
        L.append("")
        if cs.get("state") == STATE_STALE and cs.get("balance") is not None:
            L.append(f"> **Stale historical evidence, not a current balance:** the last "
                     f"recorded cash observation was **${cs['balance']:,.2f}** as of "
                     f"**{cs.get('synced_at')}** ({cs.get('age_days')}d ago). It is shown "
                     f"for evidence only and is NOT used in any figure above or below.")
            L.append("")
        L.append("| Item | Value |")
        L.append("|---|---:|")
        L.append(f"| Actual tracked cash | UNAVAILABLE ({cs.get('state', 'unknown')}) |")
        L.append(f"| Book | UNAVAILABLE |")
        L.append(f"| Protected floor | UNAVAILABLE |")
        L.append(f"| Destination total | {prot['destination_total_pct']:.4f}% |")
        L.append(f"| Unreconciled remainder | {prot['unreconciled_pct']:.4f}% |")
        L.append(f"| CASH target | {prot['cash_pct']:.4f}% |")
        L.append(f"| RESERVE target | {prot['reserve_pct']:.4f}% |")
        L.append(f"| Gated target weight | {prot['gated_target_pct']:.4f}% |")
        L.append(f"| Static protected | {prot['static_protected_pct']:.4f}% |")
        L.append("")
        L.append("**CASH+RESERVE satisfaction is UNPROVEN.** It is proved against a current "
                 "tracked balance or it is not proved at all — it is never assumed. Run: "
                 "`allocate.py update-cash <total_balance>`")
        L.append("")
    elif prot:
        cs = result.get("cash_state") or {}
        L.append("### Protected-capital accounting")
        L.append("")
        L.append("| Item | Value |")
        L.append("|---|---:|")
        L.append(f"| Actual tracked cash | ${prot['actual_cash']:,.2f} |")
        L.append(f"| Cash synced | {cs.get('synced_at')} "
                 f"({'usable' if cs.get('usable') else 'NOT USABLE'}) |")
        L.append(f"| Invested gross | ${result['margin']['gross']:,.2f} |")
        L.append(f"| Margin debt | ${result['margin']['debt']:,.2f} |")
        L.append(f"| **Book** (invested + cash − debt) | **${prot['book']:,.2f}** |")
        L.append(f"| Destination total | {prot['destination_total_pct']:.4f}% |")
        L.append(f"| Unreconciled remainder | {prot['unreconciled_pct']:.4f}% |")
        L.append(f"| CASH target | {prot['cash_pct']:.4f}% |")
        L.append(f"| RESERVE target | {prot['reserve_pct']:.4f}% |")
        L.append(f"| Gated target weight | {prot['gated_target_pct']:.4f}% |")
        L.append(f"| Static protected | {prot['static_protected_pct']:.4f}% = "
                 f"${prot['static_protected_dollars']:,.2f} |")
        L.append(f"| Gated cash required | ${prot['gated_cash_required_dollars']:,.2f} |")
        L.append(f"| **Protected floor** | **${prot['protected_floor_dollars']:,.2f}** |")
        if prot["cash_shortfall_dollars"] > 0:
            L.append(f"| **Protected SHORTFALL** | **−${prot['cash_shortfall_dollars']:,.2f}** |")
        else:
            L.append(f"| Protected surplus | ${prot['cash_surplus_dollars']:,.2f} |")
        L.append(f"| Cash-funded capacity | ${result.get('cash_funded_capacity', 0.0):,.2f} |")
        L.append(f"| Unused MARGIN capacity (not cash) | "
                 f"${result.get('unused_margin_capacity', 0.0):,.2f} |")
        _cap = result.get("cash_after_plan")
        L.append(f"| Cash remaining after plan | "
                 f"{'UNAVAILABLE' if _cap is None else f'${_cap:,.2f}'} |")
        L.append("")
        if prot["cash_shortfall_dollars"] > 0:
            L.append(f"**CASH+RESERVE are NOT satisfied.** Actual cash "
                     f"${prot['actual_cash']:,.2f} is below the ${prot['protected_floor_dollars']:,.2f} "
                     f"floor — satisfaction is proved by the tracked balance, never assumed.")
            L.append("")
        if result.get("margin_funding_blocked"):
            L.append(f"**Margin funding blocked.** {result.get('margin_funding_block_reason')}")
            L.append("")
        val = result.get("valuation") or {}
        if val and not val.get("complete", True):
            L.append(f"**Valuation incomplete.** {val.get('reason')}")
            L.append("")
    L.append("| Ticker | Action | Dollars | Price | RSI | vs200 |")
    L.append("|--------|--------|--------:|------:|----:|------:|")

    for r in result["trims"]:
        L.append(_fmt_row(r, _ck))
    if review:
        # rebalance view: show every underweight name that passes gates
        for r in result["underweight"]:
            rr = dict(r, action="UNDER", dollars=r["want"],
                      reason=r.get("earn_flag", "") or "to target")
            L.append(_fmt_row(rr, _ck))
    else:
        for r in result["buys"]:
            L.append(_fmt_row(r, _ck))
    for r in result["blocked"]:
        L.append(_fmt_row(r, _ck))

    rendered_any = result["trims"] or result["blocked"] or (
        result["underweight"] if review else result["buys"])
    if not rendered_any:
        L.append("| — | nothing actionable | — | — | — | — |")

    # 3-line summary
    deployed = sum(b["dollars"] for b in result["buys"])
    n_buy = len(result["buys"])
    L.append("")
    L.append("## Summary")
    if review:
        under_total = sum(r["want"] for r in result["underweight"])
        _tot = f"${under_total:,.0f}" if _ck else "an UNAVAILABLE dollar amount"
        L.append(f"- **Review mode** (no new cash). {len(result['underweight'])} underweight "
                 f"name(s) totaling {_tot} to target; "
                 f"{len(result['trims'])} trim candidate(s); "
                 f"{len(result['blocked'])} blocked.")
    elif not _ck:
        # No cash figure exists, so there is no deployable pool to report and
        # nothing was deployed. Say that, rather than arithmetic on a None.
        L.append(f"- **NOTHING DEPLOYED.** {_unavailability_reason(result)}, so "
                 f"available cash, the deployable pool and the post-plan remainder are "
                 f"all UNAVAILABLE; {n_buy} buy(s) were made.")
    else:
        mg = result["margin"]
        margin_note = f" (incl. ${mg['used']:,.0f} margin)" if mg["used"] > 0.01 else ""
        pool = result['cash'] + mg['allowed']
        L.append(f"- Deployed **${deployed:,.0f}**{margin_note} of ${pool:,.0f} available "
                 f"(${result['cash']:,.0f} cash + ${mg['allowed']:,.0f} margin) across "
                 f"**{n_buy} buy(s)**; ${result['cash_left']:,.0f} left.")
    L.append(f"- Regime **{regime}** (informational — no longer gates buys; "
             "see `reports/regime_backtest.md`).")
    # Cluster VALUE is a real holdings figure and stays. Its %-of-book is
    # book-derived, so it is withheld -- never silently rendered as 0.0%.
    cluster_bits = "; ".join(
        f"{c['name']} ${c['value']:,.0f} "
        + (f"({c['value']/result['book']*100:.1f}% of book, "
           if (_ck and result['book']) else "(%-of-book n/a, ")
        + f"cap {c['pct']:.0f}%)"
        for c in result.get("clusters", []))
    L.append(f"- **{len(result['trims'])} trim(s)**, "
             f"**{len(result['blocked'])} blocked**"
             + (f"; {cluster_bits}." if cluster_bits else "."))
    # ---- PHQ-2026-02: NO ADD tables (gated / issuer ceiling / common-driver) --
    gated = result.get("no_add_gated") or []
    if gated:
        L.append("")
        L.append("## NO ADD — GATED (target capital held as cash, no renormalization)")
        L.append("| Ticker | Target | Current | Status | Authority | Next gate |")
        L.append("|--------|-------:|--------:|--------|-----------|-----------|")
        for r in sorted(gated, key=lambda x: x["ticker"]):
            held = "holds existing shares" if r["holds_existing_shares"] else "no position"
            L.append(f"| {r['ticker']:<6} | ${r['target']:,.0f} | ${r['current']:,.0f} "
                     f"({held}) | {r['status']} | {r['authority']} | {r['next_gate']} |")

    issuer_no_add = result.get("no_add_issuer") or []
    if issuer_no_add:
        L.append("")
        L.append("## NO ADD — ISSUER CEILING (8% effective-issuer, PHQ-2026-01/02)")
        L.append("| Ticker | Current effective | Ceiling |")
        L.append("|--------|-------------------:|--------:|")
        for r in issuer_no_add:
            L.append(f"| {r['ticker']:<6} | {r['current_effective_pct']:.2f}% | "
                     f"{r['ceiling_pct']:.1f}% |")

    cd_no_add = result.get("no_add_common_driver") or []
    if cd_no_add:
        L.append("")
        L.append("## NO ADD — COMMON-DRIVER CEILING (40% AI/platform, PHQ-2026-01/02)")
        L.append("| Ticker | Current aggregate | Ceiling |")
        L.append("|--------|-------------------:|--------:|")
        for r in cd_no_add:
            L.append(f"| {r['ticker']:<6} | {r['current_common_driver_pct']:.2f}% | "
                     f"{r['ceiling_pct']:.1f}% |")

    cd_pct = result.get("common_driver_current_pct")
    if cd_pct is not None:
        retained = result.get("retained_common_driver_measurement") or {}
        L.append("")
        L.append("## 40% AI/platform common-driver exposure")
        L.append(f"- **Current calculated: {cd_pct:.4f}%** (live, from reconciled holdings "
                 f"+ current prices, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) vs "
                 f"**{result.get('common_driver_ceiling_pct', 40.0):.1f}% ceiling**.")
        if retained:
            L.append(f"- **Retained policy measurement: {retained.get('value_pct')}%** "
                     f"(point-in-time, measured {retained.get('measured_at')}, "
                     f"{retained.get('methodology')}) — **above ceiling, not rounded into "
                     f"compliance, may not be increased without separate principal "
                     f"approval** (PHQ-2026-01 point 9, PHQ-2026-02).")

    unresolved = result.get("unresolved") or {}
    if unresolved:
        L.append("")
        L.append("## UNRESOLVED — PRINCIPAL POLICY DECISION REQUIRED")
        for t, v in sorted(unresolved.items()):
            L.append(f"- **{t}** (${v:,.0f}, counts toward book, no canonical target, "
                     "no buy/trim/exit instruction).")

    mg = result["margin"]
    if mg["debt"] > 0 or mg["requested"] > 0:
        lev_s = f"{mg['leverage_current']:.2f}x" if mg["leverage_current"] is not None else "n/a"
        buf_s = f"{mg['buffer_pct']:.1f}%" if mg["buffer_pct"] is not None else "unsynced"
        synced_at = mg.get("synced_at")
        age_days = _margin_buffer_age_days(synced_at)
        L.append("")
        L.append("## Margin")
        L.append("| | |")
        L.append("|---|---:|")
        # Gross is independently knowable (it comes from a COMPLETE valuation,
        # which the availability fact already required). Net equity is NOT: it is
        # `gross - debt`, so an unusable margin observation makes it a derived
        # current-dollar figure computed from an unverified term. It is withheld,
        # and the debt behind it is shown as DATED EVIDENCE rather than as a
        # current reading. PHQ-2026-07 item 4.
        _ms = result.get("margin_state_check") or {}
        if _ms and not _ms.get("usable", True):
            L.append(f"| Invested gross | ${mg['gross']:,.0f} |")
            L.append("| Net equity (gross − debt) | UNAVAILABLE — margin state is "
                     f"{_ms.get('state', 'unknown')} |")
            L.append(f"| Margin debt (dated evidence, {_ms.get('synced_at')}) | "
                     f"${mg['debt']:,.0f} — not a current reading |")
        else:
            L.append(f"| Gross / net equity | ${mg['gross']:,.0f} / ${mg['net_equity']:,.0f} |")
            L.append(f"| Margin debt | ${mg['debt']:,.0f} |")
        # Tracked cash is part of the book identity, so the health view reports
        # it too rather than showing a book that silently omits it.
        _p = result.get("protection")
        if _p and not _p.get("cash_known", True):
            # Same rule as the protected-capital section above: withhold every
            # book-derived dollar rather than print a fabricated zero.
            _cs = result.get("cash_state") or {}
            L.append(f"| Tracked cash | UNAVAILABLE ({_cs.get('state', 'unknown')}) |")
            L.append("| Book (invested + cash − debt) | UNAVAILABLE |")
            L.append("| Protected floor | UNAVAILABLE |")
        elif _p:
            L.append(f"| Tracked cash | ${_p['actual_cash']:,.0f} |")
            L.append(f"| Book (invested + cash − debt) | ${_p['book']:,.0f} |")
            L.append(f"| Protected floor | ${_p['protected_floor_dollars']:,.0f} |")
            if _p["cash_shortfall_dollars"] > 0:
                L.append(f"| **Protected shortfall** | **−${_p['cash_shortfall_dollars']:,.0f}** |")
            else:
                L.append(f"| Protected surplus | ${_p['cash_surplus_dollars']:,.0f} |")
        L.append(f"| Leverage (gross/equity) | {lev_s} vs {mg['leverage_cap']:.2f}x cap |")
        L.append(f"| Buffer (last synced) | {buf_s} vs {mg['buffer_floor_pct']:.0f}% floor |")
        if mg["requested"] > 0:
            L.append(f"| Margin requested / allowed | ${mg['requested']:,.0f} / ${mg['allowed']:,.0f} |")
        if mg["forced_delever"]:
            L.append("")
            L.append(f"> ⚠️ **FORCED DE-LEVER — {mg['block_reason']}.** "
                      "No margin-funded buying this cycle; trim or pay down debt.")
        elif mg["block_reason"]:
            L.append("")
            L.append(f"> Margin request clipped — {mg['block_reason']}.")
        stale_banner_shown = age_days is not None and age_days >= STALE_MARGIN_DAYS
        unverifiable_banner_shown = age_days is None and mg["requested"] > 0
        if stale_banner_shown:
            L.append("")
            L.append(f"> ⚠️ **Margin data is {age_days} day(s) old** (last synced {synced_at}) — "
                      "re-check Robinhood and run `update-margin` before trusting this leverage/buffer read.")
        elif unverifiable_banner_shown:
            L.append("")
            L.append("> ⚠️ **No valid sync date on record for margin state** (missing, "
                      "malformed, or in the future) — run `update-margin` to establish one.")
        ms = result.get("margin_state")
        if ms is not None:
            L.append("")
            L.append(f"**Margin risk state: {ms.current_state}**")
            if ms.reasons:
                for reason in ms.reasons:
                    # The banners above already surfaced these same facts (age +
                    # synced_at + a call to action) -- skip classify_margin_state()'s
                    # own same-fact reason line here so the two don't say the same
                    # thing twice.
                    if stale_banner_shown and reason.startswith("margin data is") \
                            and "day(s) old" in reason:
                        continue
                    if unverifiable_banner_shown and reason.startswith("margin sync date is"):
                        continue
                    L.append(f"- {reason}")
            if ms.violated_constraints:
                L.append(f"- Violated constraints: {', '.join(ms.violated_constraints)}")
            L.append(f"- Allowed actions: {', '.join(ms.allowed_actions)}")
            if ms.concentration_source:
                L.append(f"- Tightest concentration pressure: {ms.concentration_source} "
                         f"({ms.risk_metrics.get('concentration_score', 0.0):.2f})")
        L.append("")
        L.append("_Buffer is synced from Robinhood via `update-margin`, not live — "
                  "verify before any large margin-funded buy._")
    L.append("")
    L.append("_Advisory only. This tool places no orders. Execute manually._")
    return "\n".join(L)


def render_health(result) -> str:
    """Snapshot risk/health view — pure presentation. Consumes only `result`
    (plan()'s output, plus whatever main() has already attached to it, e.g.
    `margin_state`); never reads YAML, never fetches, never recomputes a
    portfolio ratio plan() didn't already compute. V1 scope: leverage, buffer,
    margin risk state, cluster caps, and 8%/40% no-add ceilings — a
    point-in-time snapshot only, no historical trend, no repayment
    recommendation, no new buy/trim/block decision of any kind."""
    L = []
    L.append(f"# Portfolio Health View — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    _ck = bool(result.get("dollars_available", True))
    L.append(f"**Book:** ${result['book']:,.0f}" if _ck
             else f"**Book:** UNAVAILABLE ({_unavailability_reason(result)})")

    mg = result["margin"]
    lev_s = f"{mg['leverage_current']:.2f}x" if mg["leverage_current"] is not None else "n/a"
    buf_s = f"{mg['buffer_pct']:.1f}%" if mg["buffer_pct"] is not None else "unsynced"
    L.append("")
    L.append("## Margin")
    L.append("| | |")
    L.append("|---|---:|")
    L.append(f"| Leverage (gross/equity) | {lev_s} vs {mg['leverage_cap']:.2f}x cap |")
    L.append(f"| Buffer (last synced) | {buf_s} vs {mg['buffer_floor_pct']:.0f}% floor |")

    # Tracked cash is part of the book identity, so the health view reports it
    # rather than showing a book value that silently omits it.
    _p = result.get("protection")
    if _p:
        L.append("")
        L.append("## Protected capital")
        L.append("| | |")
        L.append("|---|---:|")
        if not _p.get("cash_known", True):
            # Same rule as render(): withhold every book-derived dollar figure
            # rather than print a fabricated zero. PHQ-2026-07 item 4.
            _cs = result.get("cash_state") or {}
            L.append(f"| Tracked cash | UNAVAILABLE ({_cs.get('state', 'unknown')}) |")
            L.append("| Book (invested + cash − debt) | UNAVAILABLE |")
            L.append("| Protected floor | UNAVAILABLE |")
            L.append(f"| Static protected weight | {_p['static_protected_pct']:.4f}% |")
        else:
            L.append(f"| Tracked cash | ${_p['actual_cash']:,.0f} |")
            L.append(f"| Book (invested + cash − debt) | ${_p['book']:,.0f} |")
            L.append(f"| Protected floor | ${_p['protected_floor_dollars']:,.0f} |")
            if _p["cash_shortfall_dollars"] > 0:
                L.append(
                    f"| **Protected shortfall** | **−${_p['cash_shortfall_dollars']:,.0f}** |")
            else:
                L.append(f"| Protected surplus | ${_p['cash_surplus_dollars']:,.0f} |")

    L.append("")
    L.append("## Margin risk state")
    ms = result.get("margin_state")
    if ms is None:
        L.append("> ⚠️ **UNAVAILABLE** — margin risk state was not computed for this "
                  "result (`classify_margin_state()` was never run against it). This is "
                  "a data-availability gap, not a risk finding — do not read it as NORMAL.")
    else:
        L.append(f"**{ms.current_state}**")
        for reason in ms.reasons:
            L.append(f"- {reason}")
        if ms.violated_constraints:
            L.append(f"- Violated constraints: {', '.join(ms.violated_constraints)}")
        if ms.allowed_actions:
            L.append(f"- Allowed actions: {', '.join(ms.allowed_actions)}")
        if ms.concentration_source:
            L.append(f"- Tightest concentration pressure: {ms.concentration_source} "
                     f"({ms.risk_metrics.get('concentration_score', 0.0):.2f})")

    L.append("")
    L.append("## Clusters")
    clusters = result.get("clusters") or []
    if clusters:
        L.append("| Cluster | %-of-book | Cap | Ratio-to-cap |")
        L.append("|---|---:|---:|---:|")
        for c in clusters:
            pct_s = f"{c['current_pct']:.1f}%" if c.get("current_pct") is not None else "n/a"
            ratio_s = f"{c['ratio_to_cap']:.2f}x" if c.get("ratio_to_cap") is not None else "n/a"
            L.append(f"| {c['name']} | {pct_s} | {c['pct']:.0f}% | {ratio_s} |")
    else:
        L.append("_No clusters configured._")

    L.append("")
    L.append("## 8%/40% no-add ceilings (PHQ-2026-02)")
    L.append(f"- Common-driver current: {result.get('common_driver_current_pct', 0.0):.2f}% "
             f"vs {result.get('common_driver_ceiling_pct', 40.0):.1f}% ceiling.")
    retained = result.get("retained_common_driver_measurement") or {}
    if retained:
        L.append(f"- Retained policy measurement: {retained.get('value_pct')}% "
                 f"(point-in-time, {retained.get('measured_at')}) — above ceiling.")
    issuer_exp = result.get("issuer_exposure") or {}
    if issuer_exp:
        L.append("| Issuer | Effective | Ceiling |")
        L.append("|--------|----------:|--------:|")
        for tk, v in sorted(issuer_exp.items(), key=lambda kv: -kv[1]["effective_pct"]):
            L.append(f"| {tk:<6} | {v['effective_pct']:.2f}% | "
                     f"{result.get('issuer_ceiling_pct', 8.0):.1f}% |")

    L.append("")
    L.append("_Crypto sleeve and T1/T2 proximity views retired by PHQ-2026-02's migration "
              "to the canonical v1.30 flat per-ticker destination architecture — BTC/ETH/SOL "
              "and every former T1/T2 name now report through the ordinary buy/hold/gated "
              "tables above like any other destination ticker._")

    L.append("")
    L.append("_Snapshot only — no historical trend, no repayment recommendation. "
              "Advisory only. This tool places no orders._")
    return "\n".join(L)


# ── update-holdings ─────────────────────────────────────────────────────────────

BOOK_CHANGE_WARN_PCT = 30.0   # abort write if book moves more than this without --confirm


def _parse_ticker_value_pairs(text: str) -> dict[str, float]:
    """Accept any whitespace layout: one pair per line OR many pairs per line.
    Walk tokens, pairing a ticker with the numeric value that follows it."""
    tokens = text.replace("$", "").replace(",", "").split()
    new: dict[str, float] = {}
    pending: str | None = None
    for tok in tokens:
        try:
            val = float(tok)
        except ValueError:
            if pending is not None:
                print(f"  skipped (no value for {pending!r})", file=sys.stderr)
            pending = tok.upper()
            continue
        if pending is None:
            print(f"  skipped (value {tok!r} with no ticker)", file=sys.stderr)
            continue
        new[pending] = val
        pending = None
    if pending is not None:
        print(f"  skipped (no value for {pending!r})", file=sys.stderr)
    return new


def update_holdings(replace: bool = False, confirm: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'TICKER value' lines (e.g. 'TICKER 24.45'). End with Ctrl-D.\n"
          f"Mode: {mode} manual holdings. This is only for positions NOT tracked by "
          f"share/coin count — anything in 'shares' or\n"
          f"'crypto_shares' is live-priced and overrides whatever's pasted here. Use "
          f"'update-shares' for a stock/ETF, 'update-crypto-shares' for a coin.\n",
          file=sys.stderr)
    new = {k: round(v, 2) for k, v in _parse_ticker_value_pairs(sys.stdin.read()).items()}

    # Merge (default) preserves positions you didn't paste; replace overwrites.
    prior = (load_yaml(HOLDINGS_FILE) or {}).get("holdings", {}) or {}
    existing = {} if replace else prior
    merged = {**{k.upper(): float(v) for k, v in existing.items()}, **new}
    merged = {k: v for k, v in merged.items() if v}   # drop zeroed-out positions

    # Sanity check: a big book-value swing usually means a partial-paste wipe.
    prior_total = sum(float(v) for v in prior.values())
    new_total = sum(merged.values())
    if prior_total > 0:
        change_pct = (new_total - prior_total) / prior_total * 100
        if abs(change_pct) > BOOK_CHANGE_WARN_PCT and not confirm:
            print(f"\n⚠️  ABORTED — book would change {change_pct:+.1f}% "
                  f"(${prior_total:,.0f} → ${new_total:,.0f}), more than "
                  f"{BOOK_CHANGE_WARN_PCT:.0f}%.\n"
                  f"    Positions: {len(prior)} → {len(merged)}. If intentional, re-run with --confirm.\n"
                  f"    Nothing was written.", file=sys.stderr)
            sys.exit(1)

    prior_yaml = load_yaml(HOLDINGS_FILE) if HOLDINGS_FILE.exists() else {}
    write_state(merged, prior_yaml.get("margin"), prior_yaml.get("shares"),
               prior_yaml.get("crypto_shares"))
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} total manual positions in {HOLDINGS_FILE}", file=sys.stderr)


def update_shares(replace: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'TICKER qty' lines (e.g. 'AAPL 0.138'). End with Ctrl-D.\n"
          f"Mode: {mode} share counts. These are live-priced via Alpaca on every run — "
          f"only update a ticker here after a real buy/sell/trim changes its share "
          f"count.\n", file=sys.stderr)
    new = _parse_ticker_value_pairs(sys.stdin.read())

    prior_yaml = load_yaml(HOLDINGS_FILE) if HOLDINGS_FILE.exists() else {}
    prior = prior_yaml.get("shares", {}) or {}
    existing = {} if replace else prior
    merged = {**{k.upper(): float(v) for k, v in existing.items()}, **new}
    merged = {k: v for k, v in merged.items() if v}   # drop zeroed-out (fully sold) positions

    write_state(prior_yaml.get("holdings"), prior_yaml.get("margin"), merged,
               prior_yaml.get("crypto_shares"))
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} share-tracked positions in {HOLDINGS_FILE}", file=sys.stderr)


def update_crypto_shares(replace: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'COIN qty' lines (e.g. 'ETH 0.209385'). End with Ctrl-D.\n"
          f"Mode: {mode} crypto coin counts. Live-priced via Alpaca on every run — "
          f"only update a coin here after a real buy/sell/trim changes its holding.\n",
          file=sys.stderr)
    new = _parse_ticker_value_pairs(sys.stdin.read())

    prior_yaml = load_yaml(HOLDINGS_FILE) if HOLDINGS_FILE.exists() else {}
    prior = prior_yaml.get("crypto_shares", {}) or {}
    existing = {} if replace else prior
    merged = {**{k.upper(): float(v) for k, v in existing.items()}, **new}
    merged = {k: v for k, v in merged.items() if v}   # drop zeroed-out (fully sold) coins

    write_state(prior_yaml.get("holdings"), prior_yaml.get("margin"),
               prior_yaml.get("shares"), merged)
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} crypto-share-tracked coins in {HOLDINGS_FILE}", file=sys.stderr)


def write_state(holdings: dict | None, margin: dict | None, shares: dict | None,
                crypto_shares: dict | None = None, cash: dict | None = None,
                _preserve_cash: bool = True):
    """Write holdings.yaml. Each block is written as given — callers that aren't
    changing a given block pass through its prior value so nothing is silently
    dropped.

    ``cash`` defaults to PRESERVING whatever is already on file. This function
    rewrites the WHOLE file, so before the cash block existed every update path
    (update-holdings / update-shares / update-crypto-shares / update-margin)
    would have silently DELETED it — turning a tracked balance into 'unknown'
    as a side effect of an unrelated sync. Preservation is the default and is
    tested for every command; a caller that genuinely means to change cash
    passes it explicitly."""
    holdings = holdings or {}
    shares = shares or {}
    crypto_shares = crypto_shares or {}
    if cash is None and _preserve_cash:
        cash = (load_yaml(HOLDINGS_FILE) or {}).get("cash")
    with open(HOLDINGS_FILE, "w") as f:
        f.write("# holdings.yaml — three tracks. 'shares' (ticker: qty) and\n"
                "# 'crypto_shares' (coin: qty) are the source of truth for any normally\n"
                "# -traded position or coin — live-valued every run via Alpaca (qty x\n"
                "# latest price). Update with 'allocate.py update-shares' / "
                "'update-crypto-shares'\n"
                "# after a real buy/sell/trim changes a count.\n"
                "# 'holdings' (ticker: dollar value) is the manual fallback for anything\n"
                "# NOT share-tracked. Currently empty/unused.\n"
                "# Update it with 'allocate.py update-holdings' if a future ticker needs it.\n")
        if cash:
            f.write("# cash: TOTAL account cash balance (never a deposit delta), synced via\n"
                    "# 'allocate.py update-cash <balance>'. Participates in the book identity\n"
                    "# book = invested + cash - margin_debt exactly once. A sync older than\n"
                    "# STALE_MARGIN_DAYS fails closed and blocks every dollar recommendation.\n"
                    "cash:\n"
                    f"  balance: {round(float(cash.get('balance', 0.0)), 2)}\n"
                    f"  synced_at: {cash.get('synced_at') or date.today().isoformat()}\n")
        if margin:
            f.write("# margin: synced via 'allocate.py update-margin <debt> <buffer_pct>' — "
                    "buffer_pct comes from Robinhood directly (per-security maintenance\n"
                    "# ratios aren't available via Alpaca), so it's only as fresh as the "
                    "last sync. Verify on Robinhood before any large margin-funded buy.\n"
                    "# IMPORTANT: always use Robinhood's own DISPLAYED buffer % — do not derive\n"
                    "# it from (portfolio value - maint req) / portfolio value. Checked twice\n"
                    "# against real screens and it doesn't reconcile (off by several points);\n"
                    "# Robinhood's actual formula weights something this simple subtraction misses.\n"
                    "margin:\n"
                    f"  debt: {round(float(margin.get('debt', 0.0)), 2)}\n"
                    f"  buffer_pct: {round(float(margin.get('buffer_pct', 0.0)), 2)}\n"
                    f"  synced_at: {margin.get('synced_at') or date.today().isoformat()}\n")
        f.write("holdings:\n")
        if holdings:
            for t in sorted(holdings):
                f.write(f"  {t}: {round(holdings[t], 2)}\n")
        else:
            f.write("  {}\n")
        f.write("shares:\n")
        if shares:
            for t in sorted(shares):
                f.write(f"  {t}: {shares[t]}\n")
        else:
            f.write("  {}\n")
        f.write("crypto_shares:\n")
        if crypto_shares:
            for c in sorted(crypto_shares):
                f.write(f"  {c}: {crypto_shares[c]}\n")
        else:
            f.write("  {}\n")
    log_performance(quiet=True)   # auto-snapshot on every holdings/shares/margin sync


def update_cash(balance: float):
    """Record the TOTAL current account cash balance and today's sync date.

    This is a TOTAL, never a deposit delta. A deposit is recorded by re-syncing
    the new total — which is precisely why the old additive ``--cash`` deposit
    argument is retired: adding a deposit on top of a tracked balance would
    double-count it. Every other state block is preserved."""
    # Validate BEFORE reading, writing, or printing. The superseded form did
    # ``float(balance)`` then ``balance < 0``, which admits every value that
    # defeats a comparison: ``nan < 0`` is False, ``inf < 0`` is False, and
    # ``float(True)`` is 1.0. Each then persisted into holdings.yaml and printed
    # "cash synced" -- a command reporting success after writing poison.
    # PHQ-2026-07 items 1 and 4: the same shared boundary that guards the READ
    # path guards the WRITE path, so state cannot be corrupted through a door
    # the reader is not allowed to open.
    balance, bad = _finite_scalar(balance, "cash balance", minimum=0.0)
    if bad is not None:
        raise ValueError(f"refusing to sync cash: {bad}")
    prior = load_yaml(HOLDINGS_FILE) or {}
    write_state(prior.get("holdings"), prior.get("margin"), prior.get("shares"),
                prior.get("crypto_shares"),
                cash={"balance": balance, "synced_at": date.today().isoformat()})
    print(f"cash synced: total balance ${balance:,.2f} in {HOLDINGS_FILE}", file=sys.stderr)


def update_margin(debt: float, buffer_pct: float):
    """Record margin debt and Robinhood's OWN displayed buffer percentage.

    Both values are validated through the shared boundary before anything is
    written or printed. This writer previously had no validation at all: a
    negative debt (which INFLATES net equity, since ``gross - (-debt)`` adds
    capital), a NaN that defeats every later comparison, or a buffer outside its
    0-100 domain all persisted and reported success. PHQ-2026-07 item 4."""
    debt, bad = _finite_scalar(debt, "margin debt", minimum=0.0)
    if bad is not None:
        raise ValueError(f"refusing to sync margin: {bad}")
    buffer_pct, bad = _finite_scalar(buffer_pct, "margin buffer_pct",
                                     minimum=0.0, maximum=100.0)
    if bad is not None:
        raise ValueError(f"refusing to sync margin: {bad}")
    prior = load_yaml(HOLDINGS_FILE) or {}
    write_state(prior.get("holdings"), {"debt": debt, "buffer_pct": buffer_pct,
                          "synced_at": date.today().isoformat()}, prior.get("shares"),
               prior.get("crypto_shares"))
    print(f"margin synced: debt=${debt:,.2f} buffer={buffer_pct:.2f}% in {HOLDINGS_FILE}",
          file=sys.stderr)


# ── performance log (net equity vs QQQ/VOO) ─────────────────────────────────────
# Descriptive only — logs realized book value against a benchmark. Does not
# predict, does not gate any buy/trim decision. See render_performance() for
# the deposit/withdrawal caveat this comparison can't correct for.

def _read_perf_log() -> list[dict]:
    """Read performance_log.csv, tolerating rows written before `cash`/`book`
    existed. Those columns are filled with "" — honestly blank, never
    back-filled with a number nobody measured."""
    if not PERF_LOG_FILE.exists():
        return []
    with open(PERF_LOG_FILE, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in PERF_FIELDS:
            r.setdefault(k, "")
            if r.get(k) is None:
                r[k] = ""
    return rows


def log_performance(note: str = "", client=None, quiet: bool = False,
                   resolved_holdings: dict | None = None):
    """Snapshot net equity + QQQ/VOO vs performance_log.csv. Called automatically
    after update-holdings, update-shares, update-margin, and every allocate run —
    never lets a price-fetch failure block the primary action it's piggybacking on.
    Pass 'resolved_holdings' (already live-priced, e.g. from main()'s primary flow)
    to avoid a second round of per-ticker price fetches; omit it to resolve fresh."""
    holdings_yaml = load_yaml(HOLDINGS_FILE) or {}
    # Route margin debt through the validating reader rather than the raw dict:
    # a negative, non-finite, or malformed debt would otherwise flow straight
    # into net_equity and be RECORDED as a data point. PHQ-2026-07 item 8 -- a
    # row may never record stale or unknown state as current.
    margin_status = load_margin_state(holdings_yaml)
    margin_state = holdings_yaml.get("margin", {}) or {}
    if not margin_status["usable"]:
        if not quiet:
            print(f"  (performance log: snapshot SKIPPED — margin state is "
                  f"{margin_status['state']}: {margin_status['reason']})", file=sys.stderr)
        return
    margin_debt = margin_status["debt"]
    # Fallback gross if live resolution fails below: last raw 'holdings' dict on
    # file (misses share-tracked positions, but keeps this from crashing).
    gross = sum(float(v) for v in (holdings_yaml.get("holdings", {}) or {}).values())

    c = client or AlpacaPaperClient()
    resolution_failed = False
    if resolved_holdings is not None:
        # A caller-supplied set is NOT exempt from value validation. Coverage is
        # the caller's business -- second-guessing which symbols it resolved
        # against a holdings file it may not be using would be wrong, and that
        # scoping is deliberate and unchanged. But a value that is not a finite
        # number is nobody's legitimate input: `{"MAN": nan}` previously wrote a
        # current row with gross=nan, net_equity=nan and book=nan straight into
        # the canonical ledger. The SAME completeness result that gates the
        # allocator gates this write. PHQ-2026-07 items 8 and 9.
        _vc = valuation_completeness(resolved_holdings, holdings_yaml)
        if _vc["invalid"]:
            # Report ONLY the value-validity failure. `reason` also carries the
            # expected-symbol coverage complaint, which does not apply to a
            # supplied set and would name the wrong cause.
            if not quiet:
                print("  (performance log: snapshot SKIPPED — non-finite or "
                      "non-numeric resolved value for "
                      + ", ".join(_vc["invalid"])
                      + " — this would poison gross, net equity and book)",
                      file=sys.stderr)
            return
        gross = sum(float(v) for v in resolved_holdings.values())
    else:
        try:
            gross = sum(float(v) for v in resolve_holdings(c).values())
        except Exception as e:
            resolution_failed = True
            if not quiet:
                print(f"  (performance log: couldn't resolve live holdings — {e})", file=sys.stderr)
    net_equity = gross - margin_debt
    # Only a CURRENT cash observation may be recorded in a current row. A stale
    # balance is a real past fact, but writing it into today's row would assert
    # it is today's -- exactly the corruption this column exists to prevent.
    cash_state = load_cash_state(holdings_yaml)
    cash_balance = cash_state["balance"] if cash_state["usable"] else None
    book = (net_equity + cash_balance) if cash_balance is not None else None

    # Do not write a misleading snapshot. When live valuation could NOT be
    # resolved, `gross` falls back to the raw manual dict (empty today, so
    # zero) and every figure derived from it would understate the book —
    # recording that as a data point corrupts the series more than skipping
    # the row does. This is deliberately scoped to the case where THIS
    # function attempted resolution and it failed: a caller that supplies
    # `resolved_holdings` has already resolved, and second-guessing its set
    # against a holdings file it may not even be using would be wrong.
    if resolution_failed:
        if not quiet:
            print("  (performance log: snapshot SKIPPED — live valuation unavailable, "
                  "so gross/book would be understated)", file=sys.stderr)
        return

    qqq_price = voo_price = None
    try:
        qqq = c.get_bars("QQQ", "1Day", limit=1, days_back=5)
        voo = c.get_bars("VOO", "1Day", limit=1, days_back=5)
        qqq_price = qqq[-1]["c"] if qqq else None
        voo_price = voo[-1]["c"] if voo else None
    except Exception as e:
        if not quiet:
            print(f"  (performance log: couldn't fetch QQQ/VOO — {e})", file=sys.stderr)

    rows = _read_perf_log()
    today = date.today().isoformat()
    rows = [r for r in rows if r["date"] != today]   # idempotent same-day re-log
    rows.append({"date": today, "net_equity": round(net_equity, 2),
                "gross": round(gross, 2), "margin_debt": round(margin_debt, 2),
                "cash": ("" if cash_balance is None else round(cash_balance, 2)),
                "book": ("" if book is None else round(book, 2)),
                "qqq_price": qqq_price, "voo_price": voo_price, "note": note})
    rows.sort(key=lambda r: r["date"])

    with open(PERF_LOG_FILE, "w", newline="") as f:
        # csv's default "excel" dialect writes CRLF regardless of platform;
        # every other tracked file in this repo is LF-only, and CI's
        # git-diff-check step flags a rewritten CRLF row as trailing
        # whitespace. Force LF to match repo convention.
        w = csv.DictWriter(f, fieldnames=PERF_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    if quiet:
        print(f"  (performance snapshot updated: net equity ${net_equity:,.2f})", file=sys.stderr)
    else:
        print(f"logged: {today} net_equity=${net_equity:,.2f} QQQ=${qqq_price} VOO=${voo_price} "
              f"in {PERF_LOG_FILE}", file=sys.stderr)


def render_performance() -> str:
    rows = _read_perf_log()
    if len(rows) < 2:
        return ("# Performance log\n\nNot enough history yet — "
                f"{len(rows)} snapshot(s) logged. Run `log-performance` again on a "
                "future date to get a comparison.")

    first, last = rows[0], rows[-1]
    prev = rows[-2] if len(rows) >= 2 else first

    def pct(a, b):
        a, b = float(a), float(b)
        return (b / a - 1) * 100 if a else None

    def fmt(p):
        return f"{p:+.1f}%" if p is not None else "n/a"

    L = ["# Performance log — net equity vs QQQ/VOO", "",
        f"**{len(rows)} snapshot(s)** logged, {first['date']} → {last['date']}", "",
        "| | Since first log | Since last log |",
        "|---|---:|---:|",
        f"| Net equity | {fmt(pct(first['net_equity'], last['net_equity']))} "
        f"| {fmt(pct(prev['net_equity'], last['net_equity']))} |",
        f"| QQQ | {fmt(pct(first['qqq_price'], last['qqq_price']))} "
        f"| {fmt(pct(prev['qqq_price'], last['qqq_price']))} |",
        f"| VOO | {fmt(pct(first['voo_price'], last['voo_price']))} "
        f"| {fmt(pct(prev['voo_price'], last['voo_price']))} |",
        "", "_Latest snapshot:_",
        f"- {last['date']}: net equity ${float(last['net_equity']):,.0f}, "
        f"gross ${float(last['gross']):,.0f}, margin debt ${float(last['margin_debt']):,.0f}"
        + (f" — _{last['note']}_" if last.get("note") else ""),
        "",
        "> ⚠️ **This is a rough directional check, not a precise return calc.** "
        "Net equity moves from deposits, withdrawals, and margin draws/paydowns, "
        "none of which are backed out here — a big deposit between snapshots will "
        "show up as \"growth\" that has nothing to do with market performance. "
        "Treat divergence from QQQ/VOO as a prompt to look closer, not a verdict.",
    ]
    return "\n".join(L)


# ── main ────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "update-holdings":
        update_holdings(replace="--replace" in sys.argv,
                        confirm="--confirm" in sys.argv)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-shares":
        update_shares(replace="--replace" in sys.argv)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-crypto-shares":
        update_crypto_shares(replace="--replace" in sys.argv)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-cash":
        if len(sys.argv) != 3:
            print("usage: allocate.py update-cash <total_balance>", file=sys.stderr)
            sys.exit(1)
        update_cash(float(sys.argv[2]))
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-margin":
        if len(sys.argv) != 4:
            print("usage: allocate.py update-margin <debt> <buffer_pct>", file=sys.stderr)
            sys.exit(1)
        update_margin(float(sys.argv[2]), float(sys.argv[3]))
        return
    if len(sys.argv) > 1 and sys.argv[1] == "log-performance":
        log_performance(note=" ".join(sys.argv[2:]))
        return

    ap = argparse.ArgumentParser(description="Manual-allocation advisor (no orders).")
    ap.add_argument("--cash", type=float, default=None,
                    help="RETIRED. Cash is now a tracked TOTAL balance in "
                         "holdings.yaml — sync it with 'allocate.py update-cash "
                         "<total_balance>'. Passing --cash is refused because an "
                         "additive deposit on top of a tracked balance would "
                         "double-count it.")
    ap.add_argument("--margin", type=float, default=0.0,
                    help="margin-funded buying power requested this cycle "
                         "(clipped to the 1.8x leverage cap / blocked below the buffer floor)")
    ap.add_argument("--review", action="store_true", help="rebalance check, no new cash")
    ap.add_argument("--levels", action="store_true", help="buy-level staging report")
    ap.add_argument("--ticker", type=str, default=None, help="limit --levels to one ticker")
    ap.add_argument("--performance", action="store_true",
                    help="show net-equity-vs-QQQ/VOO log (see log-performance to add a snapshot)")
    ap.add_argument("--health", action="store_true",
                    help="snapshot risk/health view (leverage, buffer, clusters, "
                         "8%%/40%% no-add ceilings) — observational, no new cash")
    ap.add_argument("--no-log", action="store_true",
                    help="suppress the timestamped allocation-log file and the "
                         "performance_log.csv snapshot this run would otherwise write, "
                         "for a genuinely read-only check. Only valid together with "
                         "--review (a real deployment run must keep its audit "
                         "trail; --health never writes a log to begin with). Standard "
                         "behavior (both writes happen) is unchanged when this flag "
                         "is omitted.")
    args = ap.parse_args()
    # Resolve the --cash ambiguity FAIL-CLOSED. Exactly one authoritative total
    # cash balance exists (holdings.yaml `cash:`) and it is consumed exactly
    # once; an obsolete additive --cash value must never be silently added to it.
    if args.cash is not None:
        ap.error(
            "--cash is retired. Cash is now a TRACKED TOTAL balance in holdings.yaml, "
            "consumed exactly once in book = invested + cash - margin_debt. An additive "
            "deposit passed here would be double-counted against it.\n"
            "  Migration: record the new TOTAL balance, then run the check:\n"
            "    allocate.py update-cash <total_balance>\n"
            "    allocate.py --review")
    # Nothing re-seeds args.cash afterwards: cash comes from tracked state via
    # load_cash_state(), so no fabricated value can survive this point.
    if args.no_log and not args.review:
        ap.error("--no-log is only valid together with --review — it exists to keep "
                 "the read-only phone check read-only. A real allocation "
                 "run must keep its audit trail (log file + performance_log.csv), and "
                 "--health never writes either to begin with, so --no-log is not "
                 "needed there.")
    if args.performance:
        print(render_performance())
        return
    if args.review or args.health:
        args.margin = 0.0

    if args.levels:
        from levels import run_levels
        targets = load_yaml(TARGETS_FILE)
        out = run_levels(targets, AlpacaPaperClient(), only_ticker=args.ticker)
        print(out)
        LOGS_DIR.mkdir(exist_ok=True)
        log_path = LOGS_DIR / f"levels-{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.md"
        log_path.write_text(out + "\n")
        print(f"\n[logged to {log_path}]", file=sys.stderr)
        return

    targets = load_yaml(TARGETS_FILE)
    holdings_yaml = load_yaml(HOLDINGS_FILE) or {}
    margin_state = holdings_yaml.get("margin", {}) or {}
    # Validated read, same reader the actionability gate below uses. An
    # out-of-domain debt (negative, non-finite) is never allowed to reach
    # net_equity even in the purely observational view.
    _margin_read = load_margin_state(holdings_yaml)
    margin_debt = _margin_read["debt"] if _margin_read["debt"] is not None else 0.0
    margin_buffer_pct = _margin_read["buffer_pct"]
    roster = build_roster(targets)
    if not roster:
        print("No tickers in targets.yaml — paste your roster into the "
              "destination list.", file=sys.stderr)
        sys.exit(1)
    gates_cfg = load_gates()
    lookthrough = load_issuer_lookthrough()

    client = AlpacaPaperClient()
    # RESERVE/CASH aren't market tickers — never fetch bars for them.
    market_tickers = [tk for tk, meta in roster.items()
                      if meta["asset_class"] not in ("crypto", "reserve", "cash")]
    metrics, regime_ok, regime_known = fetch_market(
        client, market_tickers, targets.get("regime_ticker", "QQQ"))

    # Crypto prices fetched BEFORE resolve_holdings so plan()'s gap math (which
    # reads crypto values straight out of 'holdings') uses live qty x price
    # too, not just the display table below. Coin list now comes from
    # targets.yaml's `destination:` (asset_class: crypto), per PHQ-2026-02 —
    # each coin carries its own target_pct there, replacing the prior
    # aggregate crypto.sleeve_pct sleeve.
    coins = [tk for tk, meta in roster.items() if meta["asset_class"] == "crypto"]
    prices = fetch_crypto(client, coins, {}) if coins else {}
    crypto_price_map = {c: d["price"] for c, d in prices.items() if d["price"] is not None}

    holdings = resolve_holdings(client, metrics, crypto_price_map)  # live qty x price

    # ---- FRESHNESS + VALUATION GATES, BEFORE any dollar recommendation ------
    # Every one of these is checked ahead of plan(), not footnoted afterward. A
    # failing gate does not suppress the observational view — it makes the run
    # explicitly NON-ACTIONABLE and blocks dollar recommendations.
    cash_state = load_cash_state(holdings_yaml)
    margin_status = _margin_read          # one reader, one owner, read once above
    valuation = valuation_completeness(holdings, holdings_yaml)
    # ONE owner computes whether current dollars may be published at all, and
    # the same list drives the NON-ACTIONABLE banner. Previously these were
    # three separate appends here while plan() and both renderers switched on
    # cash alone -- so a stale margin or an unresolved position produced a
    # banner and still published a numeric book and protected floor.
    availability = current_dollar_availability(cash_state, margin_status, valuation)
    actionable_blocks = list(availability["blocked_by"])
    if args.margin:
        actionable_blocks.append(f"MARGIN FUNDING: {MARGIN_CASH_PRESERVATION_UNPROVEN}")

    # The single authoritative total cash balance, consumed exactly once. When
    # the state is stale or unknown this is None -- NOT zero. PHQ-2026-07 item
    # 4: a fabricated zero would flow into book, the protected floor, every
    # target dollar and the shortfall, and would then be rendered as though it
    # were observed. None makes those figures unavailable instead.
    tracked_cash = cash_state["balance"] if cash_state["usable"] else None

    result = plan(targets, holdings, roster, metrics, regime_ok, regime_known, tracked_cash,
                  margin_debt=margin_debt, margin_buffer_pct=margin_buffer_pct,
                  margin_requested=args.margin, gates_cfg=gates_cfg, lookthrough=lookthrough,
                  holdings_state=holdings_yaml,
                  dollars_available=availability["available"])
    result["margin"]["synced_at"] = margin_state.get("synced_at")
    result["cash_state"] = cash_state
    result["margin_state_check"] = margin_status
    result["dollar_availability"] = availability
    result["actionable"] = not actionable_blocks
    result["actionable_blocks"] = actionable_blocks
    if actionable_blocks:
        # Dollar recommendations are withdrawn, not merely annotated.
        result["buys"] = []
        result["trims"] = []
        result["cash_spent"] = 0.0
        # None whenever current dollars are unavailable -- for ANY of the three
        # reasons, not only a stale cash reading.
        result["cash_after_plan"] = (tracked_cash if availability["available"] else None)

    # ---- margin risk-state classification (Phase 2D) -----------------------
    # Pure post-hoc read of plan()'s own output — computed AFTER plan() has
    # already decided every buy/trim/block; cannot influence allocation.
    # Concentration scope: cluster-cap proximities only.
    # ratio_to_cap is computed once in plan() (same guard: pct>0 and book>0) —
    # read here, never recomputed, so this formula has exactly one owner.
    cluster_proximities = {
        f"cluster:{c['name']}": c["ratio_to_cap"]
        for c in result.get("clusters", [])
        if c.get("ratio_to_cap") is not None
    }
    concentration_score, concentration_source = concentration_risk_score(cluster_proximities)
    margin_cfg = targets.get("margin", {}) or {}
    states_cfg = margin_cfg.get("states", {}) or {}
    caution_cfg = states_cfg.get("caution", {}) or {}
    restricted_cfg = states_cfg.get("restricted", {}) or {}
    concentration_cfg = margin_cfg.get("concentration_adjustment", {}) or {}
    synced_at_raw = margin_state.get("synced_at")
    buffer_data_age_days = _margin_buffer_age_days(synced_at_raw)
    buffer_data_unverifiable = _margin_buffer_age_unverifiable(synced_at_raw)
    result["margin_state"] = classify_margin_state(
        gross=result["margin"]["gross"],
        margin_debt=result["margin"]["debt"],
        buffer_pct=result["margin"]["buffer_pct"],
        leverage_cap=result["margin"]["leverage_cap"],
        buffer_floor_pct=result["margin"]["buffer_floor_pct"],
        concentration_score=concentration_score,
        concentration_source=concentration_source,
        buffer_data_age_days=buffer_data_age_days,
        stale_threshold_days=float(STALE_MARGIN_DAYS),
        buffer_data_unverifiable=buffer_data_unverifiable,
        caution_leverage_fraction=caution_cfg.get("leverage_fraction_of_cap"),
        caution_buffer_comfort_multiplier=caution_cfg.get("buffer_comfort_multiplier"),
        restricted_leverage_fraction=restricted_cfg.get("leverage_fraction_of_cap"),
        restricted_buffer_comfort_multiplier=restricted_cfg.get("buffer_comfort_multiplier"),
        concentration_tightening_coefficient=concentration_cfg.get("tightening_coefficient") or 0.0,
        concentration_min_fraction=(0.5 if concentration_cfg.get("min_fraction") is None
                                     else concentration_cfg["min_fraction"]),
    )

    if args.health:
        print(render_health(result))
        return

    out = render(result, review=args.review)
    print(out)

    if args.no_log:
        print("\n[--no-log: allocation log and performance_log.csv snapshot both "
              "suppressed]", file=sys.stderr)
    else:
        LOGS_DIR.mkdir(exist_ok=True)
        log_path = LOGS_DIR / f"allocation-{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.md"
        log_path.write_text(out + "\n")
        print(f"\n[logged to {log_path}]", file=sys.stderr)
        log_performance(client=client, quiet=True, resolved_holdings=holdings)   # auto-snapshot


if __name__ == "__main__":
    main()
