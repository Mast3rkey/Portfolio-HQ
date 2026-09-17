"""
currentness_report.py — read-only currentness and binding-constraint preflight.

WHAT THIS ANSWERS, before anyone trusts an allocation recommendation:

  A. Is the accepted investment research current enough to rely on?
  B. What research/catalyst evidence is stale, lapsed, or unverified?
  C. Which portfolio-policy constraints are close to, at, or beyond their
     limits AT CANONICAL TARGET WEIGHTS?
  D. Can CURRENT holdings exposure be evaluated from repository evidence, or
     is fresh private evidence required?
  E. Do retained policy measurements still reconcile with recomputation from
     the currently committed sources?
  F. Is the canonical allocation machinery itself capable of producing dollar
     recommendations when supplied with valid fresh private evidence?

AUTHORITY BOUNDARY — this module reports state and evidence. It does not
create policy. It does not change membership, target weights, caps, cluster
definitions, gates, or margin rules. It authorizes no transaction. It makes no
external-event evidence operative. It emits no buy, sell, trim, hold, or
target-change field, and no composite investment score. Every status it
returns is a statement about *evidence and configuration*, never about the
attractiveness of a security.

WRITES: none, anywhere. This module opens every file it touches in read mode
only. It does not regenerate, overwrite, or delete
`intelligence/reports/staleness_report.md` — that artifact belongs to
`intelligence_report.py` under PI-0011, and section 4 below reports its health
rather than replacing it. Runtime/stdout truth is preferred over a tracked
artifact.

IMPORT DIRECTION — strictly one-way. This module MAY import production and
reporting helpers; nothing in production may import this module. Specifically:

  * `allocate.py` must never import `currentness_report`. Enforced by test.
  * `intelligence_report.py` declares (PI-0011) that it has no import
    relationship with `allocate.py` in either direction. THIS MODULE IMPORTING
    BOTH DOES NOT CREATE ONE — they remain mutually unaware; this module is a
    downstream consumer of each, separately. Enforced by test.

REUSE, not reimplementation. Every semantic below is the existing repository's
own, called through its own code:

  * company overdue / lapsed-catalyst semantics  → `intelligence_report`
    (`collect_staleness_findings`, public API). The strict rule
    `next_due < as_of` — so `next_due == as_of` is NOT overdue — is that
    module's, not re-derived here.
  * freshness registry/checkpoint schema + cross-file invariants →
    `freshness_validator.validate_registry_and_checkpoints_files` (public).
  * per-row derived freshness state → `freshness_state.evaluate_freshness_state`
    (public, pure, spec §9 precedence).
  * issuer / AI-platform common-driver exposure → `allocate._issuer_exposure`,
    the production formula, called directly.
  * canonical roster parsing → `allocate.build_roster`.
  * repository account-state freshness → `allocate.load_cash_state`,
    `allocate.load_margin_state`, `allocate.valuation_completeness`,
    `allocate.current_dollar_availability`.

`allocate._issuer_exposure` is underscore-private. It is called here
deliberately: the alternative is an independent second implementation of
look-through arithmetic, which would be a competing source of truth for a
live no-add control. A disclosed private call beats a silent duplicate. If a
public wrapper is ever introduced, this call should move to it.

FAIL CLOSED. Where an input cannot be read, parsed, or validated, this module
reports UNAVAILABLE / UNVERIFIED / STALE with a reason. It never substitutes
zero, never infers "clean", and never presents a stale observation as current.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent

TARGETS_FILE = HERE / "targets.yaml"
HOLDINGS_FILE = HERE / "holdings.yaml"
LOOKTHROUGH_FILE = HERE / "issuer_lookthrough.yaml"
COMPANIES_DIR = HERE / "intelligence" / "companies"
FRESHNESS_REGISTRY_FILE = HERE / "intelligence" / "freshness_registry.yaml"
FRESHNESS_CHECKPOINTS_FILE = HERE / "intelligence" / "freshness_checkpoints.yaml"
COMMITTED_STALENESS_REPORT = HERE / "intelligence" / "reports" / "staleness_report.md"
PRIVATE_ALLOCATION_MODULE = "portfolio_hq.owner.private_allocation"


# ── closed status vocabularies ────────────────────────────────────────────
#
# Deliberately small and closed. A status is evidence/configuration state —
# never an investment opinion. There is no composite score and no ranking.

OK = "OK"
APPROACHING = "APPROACHING"
AT_LIMIT = "AT_LIMIT"
OVER_LIMIT = "OVER_LIMIT"
UNAVAILABLE = "UNAVAILABLE"
STALE = "STALE"
UNVERIFIED = "UNVERIFIED"
DISCREPANCY = "DISCREPANCY"

STATUSES = (OK, APPROACHING, AT_LIMIT, OVER_LIMIT, UNAVAILABLE, STALE,
            UNVERIFIED, DISCREPANCY)

# Repository-account-state verdicts — a separate, closed vocabulary, because
# "is the repository's own baseline fresh" is a different question from "is a
# constraint near its limit", and conflating them is exactly the error this
# unit exists to prevent.
REPOSITORY_STATE_CURRENT = "REPOSITORY_STATE_CURRENT"
REPOSITORY_STATE_STALE = "REPOSITORY_STATE_STALE"
PRIVATE_CURRENT_EVIDENCE_REQUIRED = "PRIVATE_CURRENT_EVIDENCE_REQUIRED"

REPOSITORY_STATE_VERDICTS = (REPOSITORY_STATE_CURRENT, REPOSITORY_STATE_STALE,
                             PRIVATE_CURRENT_EVIDENCE_REQUIRED)

CURRENT_HOLDINGS_UNAVAILABLE = "UNAVAILABLE_FROM_REPOSITORY_STATE"
RETAINED_MEASUREMENT_DISCREPANCY = "RETAINED_MEASUREMENT_DISCREPANCY"


# ── diagnostic display thresholds (NOT policy) ────────────────────────────
#
# APPROACHING_UTILISATION_PCT is a DISPLAY threshold for this diagnostic only.
# It is NOT a limit, NOT a policy parameter, and changes no allocator
# behaviour whatsoever: the allocator's own binding tests live in
# `allocate.plan()` and are untouched by this module. Per NUM-0001 it is
# recorded as a provisional guardrail — not empirically calibrated — whose
# review condition is: revisit if an accepted decision ever defines a real
# proximity band, at which point this display threshold should be deleted in
# favour of that one rather than competing with it.
#
# Every constraint row also carries its raw utilisation and headroom, so the
# label is never the only information available to a reader.
APPROACHING_UTILISATION_PCT = 90.0

# Tolerance for "retained measurement still reconciles". Sized for
# deterministic float formatting/rounding only, not for economic drift.
RETAINED_MEASUREMENT_TOLERANCE_PCT = 1e-4


class CurrentnessReportError(ValueError):
    """Raised only for programmer error in this module's own arguments."""


# ── strict numeric handling ───────────────────────────────────────────────

def _checked_pct(value: object, label: str, *,
                 minimum: float | None = None) -> tuple[float | None, str | None]:
    """Validate a percentage without raising. Returns `(value, None)` or
    `(None, reason)`.

    A percentage must be a real, finite, non-Boolean number. `bool` is a
    subclass of `int`, so `True` would otherwise silently become 1.0 and a
    malformed config would read as a valid 1% weight — exactly the coercion
    `float()` performs. Rejected here, before any production helper sees it.

    Non-raising by design: a malformed configuration must make its own section
    controlled-`UNAVAILABLE`, not abort the whole diagnostic and take the
    sections that are perfectly readable down with it.
    """
    if isinstance(value, bool):
        return None, f"{label} must not be a boolean, got {value!r}"
    if not isinstance(value, (int, float)):
        return None, (f"{label} must be a real number, got {value!r} "
                      f"({type(value).__name__})")
    result = float(value)
    if not math.isfinite(result):
        return None, f"{label} must be finite, got {value!r}"
    if minimum is not None and result < minimum:
        return None, f"{label} must be >= {minimum}, got {result}"
    return result, None


def _as_iso(value: object) -> str | None:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _parse_date(value: object) -> date | None:
    """Calendar date only. A `datetime` is NOT truncated to a date — that is
    `intelligence_report._parse_iso_date`'s existing, deliberate choice, and
    this module matches it rather than introducing a second convention."""
    if isinstance(value, datetime):
        return None
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


# ── section 1: repository account-state status ────────────────────────────

@dataclass(frozen=True)
class PrivateEvidenceCapability:
    """Existence and shape of the accepted private-evidence path.

    Established by INSPECTING THE MODULE ONLY. No private account evidence is
    read, imported, stored, or reported — not from `var/`, not from any
    runtime root, not from any envelope. This records that a path exists, not
    what has ever travelled down it.
    """
    available: bool
    module: str
    entrypoint: str | None
    schema_version: int | None
    detail: str

    def as_dict(self) -> dict:
        return {"available": self.available, "module": self.module,
                "entrypoint": self.entrypoint,
                "schema_version": self.schema_version, "detail": self.detail}


@dataclass(frozen=True)
class RepositoryAccountState:
    verdict: str                      # one of REPOSITORY_STATE_VERDICTS
    cash_state: str | None            # allocate's own three-state classification
    cash_synced_at: str | None
    cash_age_days: float | None
    margin_state: str | None
    margin_synced_at: str | None
    margin_age_days: float | None
    holdings_observation_notes: tuple[str, ...]
    valuation_complete: bool | None
    valuation_evidence_dated: bool | None
    positions_requiring_valuation: int | None
    dollars_from_repository_state: bool
    blocked_by: tuple[str, ...]
    margin_usage_statement: str
    private_evidence: PrivateEvidenceCapability
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "cash_state": self.cash_state,
            "cash_synced_at": self.cash_synced_at,
            "cash_age_days": self.cash_age_days,
            "margin_state": self.margin_state,
            "margin_synced_at": self.margin_synced_at,
            "margin_age_days": self.margin_age_days,
            "holdings_observation_notes": list(self.holdings_observation_notes),
            "valuation_complete": self.valuation_complete,
            "valuation_evidence_dated": self.valuation_evidence_dated,
            "positions_requiring_valuation": self.positions_requiring_valuation,
            "dollars_from_repository_state": self.dollars_from_repository_state,
            "blocked_by": list(self.blocked_by),
            "margin_usage_statement": self.margin_usage_statement,
            "private_evidence": self.private_evidence.as_dict(),
            "notes": list(self.notes),
        }


# THE DATED-VALUATION-EVIDENCE RULE.
#
# `holdings.yaml` dates exactly two blocks — `cash.synced_at` and
# `margin.synced_at`. Verified against `allocate.write_state()`, which is the
# only writer of this file: it emits `synced_at` for the cash and margin blocks
# and writes `holdings:`, `shares:` and `crypto_shares:` as bare
# ticker -> value/quantity mappings with no timestamp of any kind.
#
# So there is NO per-position valuation timestamp in this schema. The manual
# `holdings:` dollar snapshot is a real resolved value, but an UNDATED one: it
# cannot establish that a position's value is CURRENT, only that some value was
# recorded at some unrecorded time. Structural completeness
# (`valuation_completeness()` — "is every tracked position valued at all") and
# currency ("is that valuation current") are two different claims, and only the
# first is provable from repository state today.
#
# Therefore: whenever repository state holds any nonzero position, current
# dollar availability is false. The accepted private-evidence adapter remains
# the route to a real current portfolio. An empty book is the one case that
# genuinely needs no valuation evidence — there is nothing to value.
#
# This module deliberately does NOT name a hypothetical future timestamp field.
# Inventing one would create a new valuation authority, which is out of scope;
# `test_holdings_schema_still_dates_only_cash_and_margin` pins the schema fact
# above so that if a dated valuation form is ever added, that test fails and
# forces a deliberate decision rather than this rule silently persisting.
VALUATION_EVIDENCE_TRACKS = ("shares", "crypto_shares", "holdings")


def dated_valuation_evidence(holdings_doc: dict) -> dict:
    """Is there admissible DATED evidence that position valuations are current?

    Returns `{"tracks_declared", "declaration_reason", "position_count",
    "dated", "reason"}`.

    TWO QUESTIONS, ASKED IN ORDER, AND THE FIRST ONE GATES THE SECOND.

    1. ARE THE POSITION TRACKS DECLARED AT ALL? An UNDECLARED track is not an
       EMPTY track. `shares`, `crypto_shares` and `holdings` were previously
       read as `holdings_doc.get(track) or {}` with non-mappings skipped, so an
       absent key, an explicit `null`, or a non-mapping value all produced the
       same zero-position answer as a genuinely declared empty book — and a
       file whose entire position record this module could not read reported
       `REPOSITORY_STATE_CURRENT` with `position_count = 0`, indistinguishable
       from a real empty book. An explicit empty mapping IS a declaration and
       stays valid; absence, `null` and non-mapping are refusals to answer, and
       this fails closed on each.

       This check also has to run BEFORE `allocate.valuation_completeness()` is
       reached: that production helper iterates `data["shares"]` and
       `data["crypto_shares"]` directly and raises `AttributeError` on a
       non-mapping track, and building the resolved-value map raises
       `ValueError` on a non-mapping `holdings`. Those are uncaught crashes,
       not diagnostics. `allocate.py` is NOT modified to defend against them;
       this boundary simply refuses to hand the production helper input it
       cannot legitimately compute on, exactly as `validate_lookthrough` does.

    2. ONLY IF ALL THREE ARE DECLARED: is there a DATED current valuation for
       the positions they contain? `dated` is True only when the question does
       not arise — i.e. there is no position to value.

    No position schema is introduced and no timestamp authority is claimed
    here: this asks whether the three tracks the existing schema already
    defines were declared, and whether anything in the file dates them.
    """
    if not isinstance(holdings_doc, dict):
        # The caller in this module coerces a non-mapping document to {} before
        # reaching here, but this is public: a non-mapping document declares no
        # track at all, and that is a refusal to answer like any other.
        holdings_doc = {}

    undeclared: list[str] = []
    for track in VALUATION_EVIDENCE_TRACKS:
        if track not in holdings_doc:
            undeclared.append(f"{track} (key absent)")
            continue
        value = holdings_doc[track]
        if value is None:
            undeclared.append(f"{track} (explicit null)")
        elif not isinstance(value, dict):
            # bool is an int subclass and str/list are iterable; neither is a
            # mapping, and neither is an empty track.
            undeclared.append(f"{track} (not a mapping: {type(value).__name__})")

    if undeclared:
        return {
            "tracks_declared": False,
            "declaration_reason": (
                "POSITION TRACK DECLARATION: holdings.yaml does not declare every "
                f"position track as a mapping — {', '.join(undeclared)}. An "
                "undeclared track is NOT an empty track: an absent key, an explicit "
                "null, or a non-mapping value is a position record this module "
                "cannot read, not one proven to hold nothing, and reading it as "
                "empty would let an entirely unread book report a complete, current "
                "valuation. All three of shares, crypto_shares and holdings must be "
                "present and mappings (an explicit empty mapping is a valid "
                "declaration of an empty track). Reported UNAVAILABLE instead; the "
                "accepted private-evidence adapter remains a separate, valid path."),
            "position_count": None,
            "dated": False,
            "reason": None,
        }

    # One POSITION, counted once. A ticker may legitimately appear in more than
    # one track (a share-tracked name that also carries a manual dollar
    # fallback is the documented production pattern), and that is still a
    # single position to value — not two.
    positions: set[str] = set()
    for track in VALUATION_EVIDENCE_TRACKS:
        for ticker, raw in holdings_doc[track].items():
            value, _ = _checked_pct(raw, f"{track}.{ticker}")
            # A malformed entry is NOT dismissed as absent: it is a tracked
            # line this module cannot prove is empty, so it counts.
            if value is None or value != 0:
                positions.add(str(ticker).strip().upper())

    if not positions:
        return {"tracks_declared": True, "declaration_reason": None,
                "position_count": 0, "dated": True, "reason": None}

    shown = ", ".join(sorted(positions)[:12]) + ("…" if len(positions) > 12 else "")
    return {
        "tracks_declared": True,
        "declaration_reason": None,
        "position_count": len(positions),
        "dated": False,
        "reason": (
            f"VALUATION CURRENCY: {len(positions)} nonzero position(s) ({shown}) have no "
            "dated current valuation. holdings.yaml dates only cash.synced_at and "
            "margin.synced_at — shares, crypto_shares and the manual holdings snapshot "
            "carry no per-position observation date, so no repository-only value can be "
            "shown to be CURRENT. Supply confirmed evidence through the accepted private "
            "adapter instead."),
    }


# The one sentence this unit exists to make impossible to get wrong.
MARGIN_USAGE_UNAVAILABLE = (
    "current live margin usage unavailable from repository-only evidence — "
    "holdings.yaml's margin block is a historical repository observation, not "
    "the owner's current account. A historical debt of 0.0 is NOT evidence "
    "that the account currently carries no margin."
)


def detect_private_evidence_capability() -> PrivateEvidenceCapability:
    """Report that the accepted confirmed-private-evidence path exists.

    Imports the adapter module to confirm it is present and exposes its
    documented entrypoint. Reads no runtime root, no submission, no receipt,
    no review artifact, and no account value of any kind.
    """
    try:
        import importlib
        mod = importlib.import_module(PRIVATE_ALLOCATION_MODULE)
    except Exception as exc:  # pragma: no cover - environment-dependent
        return PrivateEvidenceCapability(
            available=False, module=PRIVATE_ALLOCATION_MODULE, entrypoint=None,
            schema_version=None,
            detail=f"adapter not importable in this environment: {exc.__class__.__name__}")
    entry = "run" if callable(getattr(mod, "run", None)) else None
    raw_version = getattr(mod, "SCHEMA_VERSION", None)
    version = raw_version if isinstance(raw_version, int) and not isinstance(raw_version, bool) else None
    if entry is None:
        return PrivateEvidenceCapability(
            available=False, module=PRIVATE_ALLOCATION_MODULE, entrypoint=None,
            schema_version=version,
            detail="adapter imported but exposes no callable run() entrypoint")
    return PrivateEvidenceCapability(
        available=True, module=PRIVATE_ALLOCATION_MODULE, entrypoint=entry,
        schema_version=version,
        detail=("accepted offline bridge present: a caller may supply confirmed "
                "private holdings/cash/debt/buffer/market evidence in memory and "
                "reach canonical allocate.plan(). Existence only — no private "
                "evidence was read, and none is required to produce this report."))


def _holdings_observation_notes(holdings_doc: dict, valuation: dict | None = None) -> tuple[str, ...]:
    """Describe what share-count observation dating the repository actually
    offers. `holdings.yaml` carries no per-position observation date — only
    the cash and margin blocks are dated — so this states that plainly rather
    than inventing a date."""
    notes: list[str] = []

    def _count(track: str, label: str) -> str:
        # An undeclared track has NO countable size. `len()` of a str or list
        # would publish a number ("7 positions" for the string "AAPL 1") that
        # describes the wrong thing entirely, so say what is actually true.
        if track not in holdings_doc:
            return f"{label}: NOT DECLARED (key absent — not an empty track)"
        value = holdings_doc[track]
        if value is None:
            return f"{label}: NOT DECLARED (explicit null — not an empty track)"
        if not isinstance(value, dict):
            return (f"{label}: NOT DECLARED (not a mapping: "
                    f"{type(value).__name__} — not an empty track)")
        return f"{label}: {len(value)}"

    notes.append(_count("shares", "share-tracked equity/fund positions"))
    notes.append(_count("crypto_shares", "share-tracked crypto positions"))
    notes.append(_count("holdings", "manual dollar-valued positions (the only "
                                    "repository-native resolved valuations)"))
    notes.append("holdings.yaml carries NO per-position observation date — share "
                 "counts are undated repository state and their currency cannot be "
                 "established from this file")
    if valuation is not None:
        unresolved = tuple(valuation.get("unresolved") or ())
        if unresolved:
            shown = ", ".join(unresolved[:12]) + ("…" if len(unresolved) > 12 else "")
            notes.append(
                f"{len(unresolved)} nonzero tracked position(s) have NO resolved "
                f"current dollar value in repository state ({shown}) — this module "
                "fetches no prices, so a quantity is never treated as a valuation")
    return tuple(notes)


def collect_repository_account_state(
    *, holdings_path: Path | str | None = None,
    as_of: datetime | date | None = None,
) -> RepositoryAccountState:
    """Classify the repository's own account baseline. Never the live account."""
    holdings_path = Path(holdings_path) if holdings_path is not None else HOLDINGS_FILE
    private = detect_private_evidence_capability()

    try:
        import allocate
    except Exception as exc:  # pragma: no cover - environment-dependent
        return RepositoryAccountState(
            verdict=PRIVATE_CURRENT_EVIDENCE_REQUIRED,
            cash_state=None, cash_synced_at=None, cash_age_days=None,
            margin_state=None, margin_synced_at=None, margin_age_days=None,
            holdings_observation_notes=(),
            valuation_complete=None, valuation_evidence_dated=None,
            positions_requiring_valuation=None,
            dollars_from_repository_state=False,
            blocked_by=(f"allocate not importable: {exc.__class__.__name__}",),
            margin_usage_statement=MARGIN_USAGE_UNAVAILABLE,
            private_evidence=private,
            notes=("repository freshness semantics unavailable — fail closed",))

    try:
        doc = yaml.safe_load(holdings_path.read_text()) or {}
    except (OSError, yaml.YAMLError) as exc:
        return RepositoryAccountState(
            verdict=PRIVATE_CURRENT_EVIDENCE_REQUIRED,
            cash_state=None, cash_synced_at=None, cash_age_days=None,
            margin_state=None, margin_synced_at=None, margin_age_days=None,
            holdings_observation_notes=(),
            valuation_complete=None, valuation_evidence_dated=None,
            positions_requiring_valuation=None,
            dollars_from_repository_state=False,
            blocked_by=(f"holdings file unreadable: {exc.__class__.__name__}",),
            margin_usage_statement=MARGIN_USAGE_UNAVAILABLE,
            private_evidence=private,
            notes=("repository baseline unreadable — fail closed",))
    if not isinstance(doc, dict):
        doc = {}

    cash = allocate.load_cash_state(doc, as_of=as_of) if as_of else allocate.load_cash_state(doc)
    margin = allocate.load_margin_state(doc, as_of=as_of) if as_of else allocate.load_margin_state(doc)

    # THE DECLARATION GATE, asked FIRST. `valuation_completeness()` and the
    # resolved-value map below both index the position tracks directly and
    # raise on a non-mapping one, so whether the tracks were declared at all
    # has to be settled before either is reached — and an undeclared track can
    # never be read as an empty one (see `dated_valuation_evidence`).
    evidence = dated_valuation_evidence(doc)

    if evidence["tracks_declared"]:
        # THE RESOLVED-VALUE MAP. `allocate.valuation_completeness()`'s first
        # argument is, by production contract, RESOLVED CURRENT DOLLAR VALUES
        # for every nonzero tracked position — production reaches it through
        # `resolve_holdings()` (qty x latest price) or, in the private adapter,
        # through confirmed evidence. A raw `shares:` quantity is NOT a dollar
        # value, and because it is finite and nonzero it would satisfy the
        # completeness check as though it were one: 4.05 shares would read as a
        # resolved $4.05 holding and a fresh-dated but entirely unvalued book
        # would report REPOSITORY_STATE_CURRENT.
        #
        # This module fetches no prices — it is offline and read-only by
        # contract — so the ONLY repository-native resolved dollar values are
        # the manual `holdings:` snapshot, which is exactly where
        # `resolve_holdings()` itself starts (`result =
        # dict(data.get("holdings", {}))`) before applying prices this module
        # does not have. Anything share- or coin-tracked without such an entry
        # is therefore genuinely unresolved here, and `valuation_completeness()`
        # reports it as such — fail closed, never a quantity promoted to a
        # valuation, and never an invented price.
        resolved_values = dict(doc["holdings"])
        valuation = allocate.valuation_completeness(resolved_values, doc)
    else:
        # NOT an evaluated completeness result and never presented as one: an
        # explicitly incomplete stand-in carrying the declaration failure as
        # its own reason, so the SINGLE production availability rule still
        # computes the answer and this module does not grow a second one.
        valuation = {"complete": False, "unresolved": (),
                     "reason": evidence["declaration_reason"]}

    availability = allocate.current_dollar_availability(cash, margin, valuation)

    # THE CURRENCY GATE, applied ON TOP of the production availability fact.
    # `valuation_completeness()` proves every tracked position carries SOME
    # value; it does not — and cannot — prove that value is current, because
    # nothing in this schema dates it. This gate may only ever RESTRICT the
    # production answer further; it can never make unavailable state available.
    blocked = list(availability.get("blocked_by") or ())
    if evidence["reason"] is not None:
        # Only the currency reason is appended here. A declaration failure is
        # already carried above as the valuation blocker, so it is stated once.
        blocked.append(evidence["reason"])
    dollars_ok = bool(availability.get("available")) and bool(evidence["dated"])

    both_usable = bool(cash.get("usable")) and bool(margin.get("usable"))
    if both_usable and dollars_ok:
        verdict = REPOSITORY_STATE_CURRENT
    elif cash.get("state") == "stale" or margin.get("state") == "stale":
        verdict = REPOSITORY_STATE_STALE
    else:
        verdict = PRIVATE_CURRENT_EVIDENCE_REQUIRED

    notes: list[str] = []
    if not evidence["tracks_declared"]:
        notes.append(
            "valuation completeness was NOT evaluated: the position tracks were "
            "not all declared as mappings, so there was nothing to evaluate "
            "completeness against and no zero was substituted for the missing "
            "declaration")
    if verdict != REPOSITORY_STATE_CURRENT:
        notes.append(
            "repository baseline cannot support a current dollar recommendation "
            "on its own; the accepted private-evidence adapter remains a valid, "
            "separate path and is NOT blocked by this verdict")
    raw_buffer = (doc.get("margin") or {}).get("buffer_pct") if isinstance(doc.get("margin"), dict) else None
    if raw_buffer is not None:
        notes.append(
            "holdings.yaml's margin.buffer_pct is a repository-recorded value; the "
            "repository's own convention requires Robinhood's DISPLAYED buffer and "
            "it is only as fresh as its sync date")

    return RepositoryAccountState(
        verdict=verdict,
        cash_state=cash.get("state"), cash_synced_at=_as_iso(cash.get("synced_at")),
        cash_age_days=cash.get("age_days"),
        margin_state=margin.get("state"), margin_synced_at=_as_iso(margin.get("synced_at")),
        margin_age_days=margin.get("age_days"),
        holdings_observation_notes=_holdings_observation_notes(doc, valuation),
        valuation_complete=(bool(valuation.get("complete"))
                            if evidence["tracks_declared"] else None),
        valuation_evidence_dated=bool(evidence["dated"]),
        positions_requiring_valuation=(None if evidence["position_count"] is None
                                       else int(evidence["position_count"])),
        dollars_from_repository_state=dollars_ok,
        blocked_by=tuple(blocked),
        margin_usage_statement=MARGIN_USAGE_UNAVAILABLE,
        private_evidence=private,
        notes=tuple(notes),
    )


# ── section 2: Company Intelligence currentness ───────────────────────────

@dataclass(frozen=True)
class CompanyRecordCurrentness:
    ticker: str
    last_reviewed: str | None
    next_due: str | None
    overdue: bool
    days_overdue: int | None
    catalysts_present: bool
    lapsed_catalyst_count: int
    unevaluable_field_count: int
    schema_invalid: bool
    status: str
    anomalies: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "ticker": self.ticker, "last_reviewed": self.last_reviewed,
            "next_due": self.next_due, "overdue": self.overdue,
            "days_overdue": self.days_overdue,
            "catalysts_present": self.catalysts_present,
            "lapsed_catalyst_count": self.lapsed_catalyst_count,
            "unevaluable_field_count": self.unevaluable_field_count,
            "schema_invalid": self.schema_invalid, "status": self.status,
            "anomalies": list(self.anomalies),
        }


@dataclass(frozen=True)
class LapsedCatalystRow:
    ticker: str
    catalyst: str
    expected: str
    days_overdue: int
    in_canonical_roster: bool

    def as_dict(self) -> dict:
        return {"ticker": self.ticker, "catalyst": self.catalyst,
                "expected": self.expected, "days_overdue": self.days_overdue,
                "in_canonical_roster": self.in_canonical_roster}


@dataclass(frozen=True)
class CompanyIntelligenceCurrentness:
    as_of: str
    records: tuple[CompanyRecordCurrentness, ...]
    lapsed_catalysts: tuple[LapsedCatalystRow, ...]
    record_count: int
    overdue_count: int
    records_with_lapsed_catalysts: int
    total_lapsed_catalysts: int
    records_without_catalysts: int
    schema_invalid_count: int
    canonical_covered: tuple[str, ...]
    canonical_uncovered: tuple[str, ...]
    non_roster_records: tuple[str, ...]
    status: str
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "as_of": self.as_of,
            "records": [r.as_dict() for r in self.records],
            "lapsed_catalysts": [c.as_dict() for c in self.lapsed_catalysts],
            "record_count": self.record_count,
            "overdue_count": self.overdue_count,
            "records_with_lapsed_catalysts": self.records_with_lapsed_catalysts,
            "total_lapsed_catalysts": self.total_lapsed_catalysts,
            "records_without_catalysts": self.records_without_catalysts,
            "schema_invalid_count": self.schema_invalid_count,
            "canonical_covered": list(self.canonical_covered),
            "canonical_uncovered": list(self.canonical_uncovered),
            "non_roster_records": list(self.non_roster_records),
            "status": self.status, "notes": list(self.notes),
        }


NOT_OVERDUE_IS_NOT_CURRENT = (
    "A record that is not overdue is NOT thereby current. `next_due` has not "
    "arriving is a statement about a configured cadence, never evidence that no "
    "material filing, earnings release, guidance change, or corporate action has "
    "occurred since `last_reviewed`. This repository performs no event detection "
    "(see section 3), so nothing here can rule that out."
)


def collect_company_currentness(
    *, companies_dir: Path | str | None = None,
    canonical_equities: tuple[str, ...] = (),
    as_of_date: date | None = None,
) -> CompanyIntelligenceCurrentness:
    """Evaluate every `intelligence/companies/*.yaml` record.

    Overdue and lapsed-catalyst determination is delegated in full to
    `intelligence_report.collect_staleness_findings` — this function adds only
    facts that module does not report (catalyst absence, `last_reviewed`
    anomalies, canonical-roster coverage) and never re-derives the rules.
    """
    companies_dir = Path(companies_dir) if companies_dir is not None else COMPANIES_DIR
    as_of_date = as_of_date or date.today()

    import intelligence_report

    findings = intelligence_report.collect_staleness_findings(companies_dir, as_of_date)

    overdue_by = {o.ticker: o for o in findings.overdue_reviews}
    lapsed_by: dict[str, list] = {}
    for c in findings.lapsed_catalysts:
        lapsed_by.setdefault(c.ticker, []).append(c)
    unable_by: dict[str, int] = {}
    for u in findings.unable_to_evaluate:
        unable_by[u.ticker] = unable_by.get(u.ticker, 0) + 1
    invalid = {i.ticker for i in findings.schema_invalid}

    canonical = tuple(t.upper() for t in canonical_equities)
    records: list[CompanyRecordCurrentness] = []
    without_catalysts = 0

    for ticker in findings.companies_scanned:
        path = companies_dir / f"{ticker}.yaml"
        anomalies: list[str] = []
        last_reviewed_raw = None
        next_due_raw = None
        catalysts_present = False
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except (OSError, yaml.YAMLError):
            data = {}
            anomalies.append("record unreadable or unparseable at report time")
        if isinstance(data, dict):
            review = data.get("review")
            if isinstance(review, dict):
                last_reviewed_raw = review.get("last_reviewed")
                next_due_raw = review.get("next_due")
            catalysts = data.get("catalysts")
            catalysts_present = bool(isinstance(catalysts, list) and catalysts)

        if not catalysts_present:
            without_catalysts += 1
            anomalies.append(
                "no catalysts[] — the only event signal this repository can "
                "currently derive cannot fire for this record")

        lr = _parse_date(last_reviewed_raw)
        if last_reviewed_raw is not None and lr is None:
            anomalies.append("last_reviewed missing, unparseable, or not a calendar date")
        elif lr is not None and lr > as_of_date:
            anomalies.append(f"last_reviewed {lr.isoformat()} is in the future relative to {as_of_date.isoformat()}")
        nd = _parse_date(next_due_raw)
        if nd is not None and lr is not None and nd < lr:
            anomalies.append("next_due precedes last_reviewed")

        o = overdue_by.get(ticker)
        lapsed_here = lapsed_by.get(ticker, [])
        unevaluable = unable_by.get(ticker, 0)
        is_invalid = ticker in invalid

        if is_invalid:
            status = UNVERIFIED
        elif o is not None:
            status = STALE
        elif lapsed_here or unevaluable or anomalies:
            status = UNVERIFIED
        else:
            status = OK

        records.append(CompanyRecordCurrentness(
            ticker=ticker,
            last_reviewed=_as_iso(last_reviewed_raw),
            next_due=_as_iso(next_due_raw),
            overdue=o is not None,
            days_overdue=o.days_overdue if o is not None else None,
            catalysts_present=catalysts_present,
            lapsed_catalyst_count=len(lapsed_here),
            unevaluable_field_count=unevaluable,
            schema_invalid=is_invalid,
            status=status,
            anomalies=tuple(anomalies),
        ))

    scanned = set(findings.companies_scanned)
    covered = tuple(t for t in canonical if t in scanned)
    uncovered = tuple(t for t in canonical if t not in scanned)
    non_roster = tuple(sorted(scanned - set(canonical))) if canonical else ()

    lapsed_rows = tuple(sorted(
        (LapsedCatalystRow(ticker=c.ticker, catalyst=c.catalyst, expected=c.expected,
                           days_overdue=c.days_overdue,
                           in_canonical_roster=c.ticker in set(canonical))
         for c in findings.lapsed_catalysts),
        key=lambda r: (r.expected, r.ticker)))

    if findings.schema_invalid:
        status = UNVERIFIED
    elif findings.overdue_reviews:
        status = STALE
    elif lapsed_rows or findings.unable_to_evaluate or uncovered:
        status = UNVERIFIED
    else:
        status = OK

    return CompanyIntelligenceCurrentness(
        as_of=as_of_date.isoformat(),
        records=tuple(records),
        lapsed_catalysts=lapsed_rows,
        record_count=len(findings.companies_scanned),
        overdue_count=len(findings.overdue_reviews),
        records_with_lapsed_catalysts=len(lapsed_by),
        total_lapsed_catalysts=len(findings.lapsed_catalysts),
        records_without_catalysts=without_catalysts,
        schema_invalid_count=len(findings.schema_invalid),
        canonical_covered=covered,
        canonical_uncovered=uncovered,
        non_roster_records=non_roster,
        status=status,
        notes=(NOT_OVERDUE_IS_NOT_CURRENT,),
    )


# ── section 3: freshness monitor status ───────────────────────────────────

@dataclass(frozen=True)
class FreshnessMonitorRow:
    ticker: str
    monitoring_enabled: bool | None
    checkpoint_status: str | None
    channels_declared: int
    checkpoint_present: bool
    derived_state: str | None
    status: str
    detail: str = ""

    def as_dict(self) -> dict:
        return {"ticker": self.ticker, "monitoring_enabled": self.monitoring_enabled,
                "checkpoint_status": self.checkpoint_status,
                "channels_declared": self.channels_declared,
                "checkpoint_present": self.checkpoint_present,
                "derived_state": self.derived_state, "status": self.status,
                "detail": self.detail}


@dataclass(frozen=True)
class FreshnessMonitorStatus:
    rows: tuple[FreshnessMonitorRow, ...]
    enrolled_count: int
    monitoring_enabled_count: int
    verified_checkpoint_count: int
    pending_or_unverified_count: int
    duplicate_tickers: tuple[str, ...]
    schema_valid: bool
    schema_errors: tuple[str, ...]
    cadence_mechanism_exists: bool
    operational_event_monitoring_exists: bool
    status: str
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "rows": [r.as_dict() for r in self.rows],
            "enrolled_count": self.enrolled_count,
            "monitoring_enabled_count": self.monitoring_enabled_count,
            "verified_checkpoint_count": self.verified_checkpoint_count,
            "pending_or_unverified_count": self.pending_or_unverified_count,
            "duplicate_tickers": list(self.duplicate_tickers),
            "schema_valid": self.schema_valid,
            "schema_errors": list(self.schema_errors),
            "cadence_mechanism_exists": self.cadence_mechanism_exists,
            "operational_event_monitoring_exists": self.operational_event_monitoring_exists,
            "status": self.status, "notes": list(self.notes),
        }


CADENCE_VS_MONITORING_NOTE = (
    "A DATE-CADENCE MECHANISM EXISTS (freshness_identity / freshness_state / "
    "freshness_cadence are deterministic local functions, and freshness_validator "
    "enforces the registry/checkpoint schema). OPERATIONAL LIVE EVENT MONITORING "
    "DOES NOT: this report asserts monitoring only where a row is enabled AND its "
    "checkpoint is verified. AUTO-0001/AUTO-0002/AUTO-0003 are not claimed here to "
    "perform any network retrieval — no executable repository evidence of a "
    "network adapter or scheduler was consulted or relied on to produce this "
    "report, and none is implied. Because this repository contains no monitor-run "
    "record surface, spec §9's precedence rule makes the `current` state "
    "unreachable for every ticker by construction — an absence of monitoring "
    "infrastructure, reported as such rather than inferred away."
)


def collect_freshness_monitor_status(
    *, registry_path: Path | str | None = None,
    checkpoints_path: Path | str | None = None,
) -> FreshnessMonitorStatus:
    """Report enrollment/monitoring/checkpoint state per registry row.

    Schema and cross-file invariants come from
    `freshness_validator.validate_registry_and_checkpoints_files`; the derived
    per-row state comes from `freshness_state.evaluate_freshness_state` (spec
    §9 precedence). Neither rule is re-implemented here.
    """
    registry_path = Path(registry_path) if registry_path is not None else FRESHNESS_REGISTRY_FILE
    checkpoints_path = Path(checkpoints_path) if checkpoints_path is not None else FRESHNESS_CHECKPOINTS_FILE

    import freshness_state
    import freshness_validator

    validation = freshness_validator.validate_registry_and_checkpoints_files(
        registry_path, checkpoints_path)

    def _load(path: Path) -> dict:
        try:
            doc = yaml.safe_load(path.read_text())
        except (OSError, yaml.YAMLError):
            return {}
        return doc if isinstance(doc, dict) else {}

    registry_doc = _load(registry_path)
    checkpoints_doc = _load(checkpoints_path)
    registry_rows = [r for r in (registry_doc.get("tickers") or []) if isinstance(r, dict)]
    checkpoint_rows = [r for r in (checkpoints_doc.get("tickers") or []) if isinstance(r, dict)]

    seen: dict[str, int] = {}
    for r in registry_rows:
        tk = r.get("ticker")
        if isinstance(tk, str):
            seen[tk] = seen.get(tk, 0) + 1
    duplicates = tuple(sorted(t for t, n in seen.items() if n > 1))

    checkpoints_by: dict[str, dict] = {}
    for r in checkpoint_rows:
        tk = r.get("ticker")
        if isinstance(tk, str) and tk not in checkpoints_by:
            checkpoints_by[tk] = r

    rows: list[FreshnessMonitorRow] = []
    enabled_count = 0
    verified_count = 0

    for r in registry_rows:
        tk = r.get("ticker") if isinstance(r.get("ticker"), str) else "<malformed>"
        raw_enabled = r.get("monitoring_enabled")
        enabled = raw_enabled if isinstance(raw_enabled, bool) else None
        cp = checkpoints_by.get(tk)
        cp_present = cp is not None
        raw_status = cp.get("checkpoint_status") if cp_present else None
        cp_status = raw_status if isinstance(raw_status, str) else None
        channels = cp.get("channels") if cp_present else None
        channel_count = len(channels) if isinstance(channels, dict) else 0

        if enabled is True:
            enabled_count += 1
        if cp_status == "verified":
            verified_count += 1

        derived: str | None = None
        detail = ""
        if enabled is None:
            detail = "monitoring_enabled is missing or not a boolean"
        elif not cp_present:
            detail = "no checkpoint row for this registry ticker"
        elif cp_status is None:
            detail = "checkpoint_status is missing or not a string"
        else:
            # `monitor_record_exists=False` is the only honest value available:
            # this repository contains no monitor-run record surface at all, so
            # spec §9's precedence rule makes `current` UNREACHABLE by
            # construction for every ticker, however its registry row and
            # checkpoint are set. That is a disclosure about the absence of
            # operational monitoring, not a defect in this call.
            try:
                derived = freshness_state.evaluate_freshness_state(
                    monitoring_enabled=enabled,
                    checkpoint_status=cp_status,
                    monitor_record_exists=False,
                    latest_monitor_state=None,
                    outstanding=frozenset(),
                    assigned=frozenset(),
                    awaiting_human_incorporation=frozenset(),
                    incorporated=frozenset(),
                )
            except ValueError as exc:
                detail = f"freshness state not derivable: {exc}"

        if derived == "current":
            status = OK
        elif derived is None:
            status = UNAVAILABLE
        else:
            status = UNVERIFIED
            if not detail:
                detail = (f"derived state {derived!r} — no verified live monitoring "
                          "channel is established for this ticker")

        rows.append(FreshnessMonitorRow(
            ticker=tk, monitoring_enabled=enabled, checkpoint_status=cp_status,
            channels_declared=channel_count, checkpoint_present=cp_present,
            derived_state=derived, status=status, detail=detail))

    pending_or_unverified = sum(1 for r in rows if r.status != OK)
    operational = any(r.status == OK for r in rows)

    if not validation.valid or duplicates:
        status = UNVERIFIED
    elif not rows:
        status = UNAVAILABLE
    elif operational and pending_or_unverified == 0:
        status = OK
    else:
        status = UNVERIFIED

    return FreshnessMonitorStatus(
        rows=tuple(rows),
        enrolled_count=len(registry_rows),
        monitoring_enabled_count=enabled_count,
        verified_checkpoint_count=verified_count,
        pending_or_unverified_count=pending_or_unverified,
        duplicate_tickers=duplicates,
        schema_valid=bool(validation.valid),
        schema_errors=tuple(validation.errors),
        cadence_mechanism_exists=True,
        operational_event_monitoring_exists=operational,
        status=status,
        notes=(CADENCE_VS_MONITORING_NOTE,),
    )


# ── section 4: committed staleness-report health ──────────────────────────

@dataclass(frozen=True)
class CommittedStalenessReportHealth:
    present: bool
    path: str
    as_of_date: str | None
    companies_scanned_claim: int | None
    current_company_count: int
    status: str
    detail: str

    def as_dict(self) -> dict:
        return {"present": self.present, "path": self.path,
                "as_of_date": self.as_of_date,
                "companies_scanned_claim": self.companies_scanned_claim,
                "current_company_count": self.current_company_count,
                "status": self.status, "detail": self.detail}


def inspect_committed_staleness_report(
    *, report_path: Path | str | None = None,
    current_company_count: int = 0,
    as_of_date: date | None = None,
) -> CommittedStalenessReportHealth:
    """Read-only health check on `intelligence/reports/staleness_report.md`.

    This function NEVER writes, regenerates, or deletes that artifact. It is
    owned by `intelligence_report.py` under PI-0011, and no accepted decision
    designates this module as its replacement. Runtime/stdout truth from
    section 2 above is the current answer; this section only reports whether
    the committed file still agrees with it.
    """
    report_path = Path(report_path) if report_path is not None else COMMITTED_STALENESS_REPORT
    as_of_date = as_of_date or date.today()

    if not report_path.exists():
        return CommittedStalenessReportHealth(
            present=False, path=str(report_path), as_of_date=None,
            companies_scanned_claim=None,
            current_company_count=current_company_count, status=UNAVAILABLE,
            detail="no committed staleness report present")
    try:
        text = report_path.read_text()
    except OSError as exc:
        return CommittedStalenessReportHealth(
            present=True, path=str(report_path), as_of_date=None,
            companies_scanned_claim=None,
            current_company_count=current_company_count, status=UNAVAILABLE,
            detail=f"committed staleness report unreadable: {exc.__class__.__name__}")

    as_of_match = re.search(r"_As of:\s*(\d{4}-\d{2}-\d{2})", text)
    scanned_match = re.search(r"(\d+)\s+companies scanned", text)
    reported_as_of = as_of_match.group(1) if as_of_match else None
    scanned_claim = int(scanned_match.group(1)) if scanned_match else None

    problems: list[str] = []
    if reported_as_of is None:
        problems.append("no parseable as-of date")
    else:
        parsed = _parse_date(reported_as_of)
        if parsed is None:
            problems.append("as-of date unparseable")
        elif parsed < as_of_date:
            problems.append(f"as-of {reported_as_of} predates this run ({as_of_date.isoformat()}) by {(as_of_date - parsed).days}d")
    if scanned_claim is None:
        problems.append("no parseable scanned-company count")
    elif scanned_claim != current_company_count:
        problems.append(f"claims {scanned_claim} companies scanned; {current_company_count} records exist now")

    status = STALE if problems else OK
    detail = ("committed artifact agrees with the current corpus"
              if not problems else
              "; ".join(problems) + " — prefer this run's stdout truth; the committed "
              "artifact is NOT regenerated by this module")
    return CommittedStalenessReportHealth(
        present=True, path=str(report_path), as_of_date=reported_as_of,
        companies_scanned_claim=scanned_claim,
        current_company_count=current_company_count, status=status, detail=detail)


# ── section 5: target-weight concentration preflight ──────────────────────

@dataclass(frozen=True)
class ClusterConstraint:
    name: str
    cap_pct: float
    members: tuple[str, ...]
    target_exposure_pct: float
    utilisation_pct: float | None
    headroom_pct: float
    status: str
    detail: str = ""

    def as_dict(self) -> dict:
        return {"name": self.name, "cap_pct": self.cap_pct,
                "members": list(self.members),
                "target_exposure_pct": self.target_exposure_pct,
                "utilisation_pct": self.utilisation_pct,
                "headroom_pct": self.headroom_pct, "status": self.status,
                "detail": self.detail}


@dataclass(frozen=True)
class IssuerConstraint:
    ticker: str
    direct_pct: float
    embedded_pct: float
    effective_pct: float
    ceiling_pct: float
    utilisation_pct: float | None
    headroom_pct: float
    status: str

    def as_dict(self) -> dict:
        return {"ticker": self.ticker, "direct_pct": self.direct_pct,
                "embedded_pct": self.embedded_pct,
                "effective_pct": self.effective_pct,
                "ceiling_pct": self.ceiling_pct,
                "utilisation_pct": self.utilisation_pct,
                "headroom_pct": self.headroom_pct, "status": self.status}


@dataclass(frozen=True)
class CommonDriverConstraint:
    recomputed_pct: float
    ceiling_pct: float
    utilisation_pct: float | None
    headroom_pct: float
    retained_value_pct: float | None
    retained_measured_at: str | None
    retained_delta_pct: float | None
    reconciles: bool | None
    status: str
    limit_status: str
    discrepancy_flag: str | None
    detail: str = ""

    def as_dict(self) -> dict:
        return {"recomputed_pct": self.recomputed_pct,
                "ceiling_pct": self.ceiling_pct,
                "utilisation_pct": self.utilisation_pct,
                "headroom_pct": self.headroom_pct,
                "retained_value_pct": self.retained_value_pct,
                "retained_measured_at": self.retained_measured_at,
                "retained_delta_pct": self.retained_delta_pct,
                "reconciles": self.reconciles, "status": self.status,
                "limit_status": self.limit_status,
                "discrepancy_flag": self.discrepancy_flag, "detail": self.detail}


@dataclass(frozen=True)
class TargetWeightConcentration:
    available: bool
    basis: str
    clusters: tuple[ClusterConstraint, ...]
    issuers: tuple[IssuerConstraint, ...]
    max_issuer: IssuerConstraint | None
    common_driver: CommonDriverConstraint | None
    destination_total_pct: float | None
    status: str
    detail: str = ""

    def as_dict(self) -> dict:
        return {
            "available": self.available, "basis": self.basis,
            "clusters": [c.as_dict() for c in self.clusters],
            "issuers": [i.as_dict() for i in self.issuers],
            "max_issuer": self.max_issuer.as_dict() if self.max_issuer else None,
            "common_driver": self.common_driver.as_dict() if self.common_driver else None,
            "destination_total_pct": self.destination_total_pct,
            "status": self.status, "detail": self.detail,
        }


def _padded_identity_reason(field: str, value: str) -> str:
    """Why a whitespace-padded issuer or fund identity is REFUSED, not trimmed.

    `allocate._issuer_exposure` resolves identities with `.upper()` and NO
    `.strip()` — `iss["ticker"].upper()` and `f["fund"].upper()`. A padded
    identity therefore never matches the canonical holdings key production
    looks up, so its direct and embedded exposure both silently compute as
    0.0 and the 8% issuer and 40% common-driver no-add controls are understated
    while still reporting a clean OK.

    Two responses were available. CANONICALISING here (trimming before use)
    would let this diagnostic publish a DIFFERENT, correct exposure than the
    production allocator would compute from the very same configuration file —
    masking a live production mismatch behind a healthy-looking report, which
    is the opposite of what a preflight is for. REFUSING is the response taken,
    and it matches the repository's own precedent: `allocate.build_roster`
    already rejects a whitespace-padded `asset_class` outright rather than
    normalising it. `_issuer_exposure` is not modified; the configuration is
    required to be canonical, or the section reports UNAVAILABLE.

    Case is NOT rejected: production applies `.upper()` to both identities, so
    a lowercase identity resolves identically in production and here. Padding
    is the only divergence, and it is the only thing refused.
    """
    return (f"{field} {value!r} is whitespace-padded. The production exposure "
            "helper resolves identities with .upper() and no .strip(), so a "
            "padded identity matches no canonical holdings key and silently "
            "contributes 0.0% direct and 0.0% embedded exposure — understating "
            "the 8% issuer and 40% common-driver controls while still reading as "
            "OK. It is refused rather than trimmed, so this report can never "
            "show an exposure the allocator would not compute from the same "
            "file; fix the identity in issuer_lookthrough.yaml.")


def validate_lookthrough(lookthrough: object) -> tuple[dict | None, str | None]:
    """Strictly validate every look-through value this section consumes.

    Returns `(validated, None)` or `(None, reason)`. `validated` carries the
    two ceilings and the issuer rows, already proven well-formed.

    WHY THIS EXISTS, both halves:

    1. NO SILENT CEILING FALLBACK. `issuer_ceiling_pct` and
       `common_driver_ceiling_pct` are safety-sensitive constraint values. A
       missing key previously defaulted to the historical 8.0/40.0 literals, so
       an absent configuration still produced a plausible OK/OVER_LIMIT verdict
       as though the active constraint were known. Both are REQUIRED here —
       the same fail-loud treatment `allocate._resolve_margin_config` already
       gives the 1.8x cap and 30% floor (NUM-0001 P1-1), expressed as
       controlled UNAVAILABLE because a diagnostic must not abort.

    2. NO MALFORMED VALUE REACHING THE PRODUCTION HELPER.
       `allocate._issuer_exposure` computes `float(f["fund_holding_weight"])`,
       and `float(True)` is 1.0 — a Boolean weight would silently become a
       100% fund constituent. `_issuer_exposure` is NOT modified to defend
       against this; it keeps owning the arithmetic, and this boundary simply
       refuses to hand it anything it cannot legitimately compute on.

    Every key validated below is one `_issuer_exposure` actually reads.
    """
    if not isinstance(lookthrough, dict):
        return None, "issuer_lookthrough configuration is not a mapping"

    ceilings: dict[str, float] = {}
    for key in ("issuer_ceiling_pct", "common_driver_ceiling_pct"):
        if key not in lookthrough:
            return None, (
                f"issuer_lookthrough.yaml is missing required '{key}' — this is a "
                "safety-sensitive constraint value and is never defaulted to a "
                "historical literal; the section reports UNAVAILABLE instead")
        value, reason = _checked_pct(lookthrough[key], f"issuer_lookthrough.{key}",
                                     minimum=0.0)
        if reason is not None:
            return None, reason
        ceilings[key] = value

    # MEMBERSHIP IS EXPLICIT OR IT IS UNKNOWN. A missing key is not an empty
    # set: absent `issuers` would silently publish 0.0000% common-driver
    # exposure, and an absent per-issuer `funds` would silently drop that
    # issuer's embedded exposure — both UNDERSTATING the 8% issuer and 40%
    # common-driver no-add controls while looking like a clean result.
    if "issuers" not in lookthrough:
        return None, (
            "issuer_lookthrough.yaml is missing required 'issuers' — an absent "
            "membership key is not an empty membership, and treating it as one "
            "would understate the issuer and common-driver controls; the section "
            "reports UNAVAILABLE instead")
    raw_issuers = lookthrough["issuers"]
    if not isinstance(raw_issuers, list):
        return None, "issuer_lookthrough.issuers must be a list"

    seen: set[str] = set()
    issuers: list[dict] = []
    for i, row in enumerate(raw_issuers):
        label = f"issuer_lookthrough.issuers[{i}]"
        if not isinstance(row, dict):
            return None, f"{label} is not a mapping"
        ticker = row.get("ticker")
        if not isinstance(ticker, str) or not ticker.strip():
            return None, f"{label}.ticker must be a non-empty string, got {ticker!r}"
        if ticker != ticker.strip():
            return None, _padded_identity_reason(f"{label}.ticker", ticker)
        key = ticker.upper()
        if key in seen:
            # _issuer_exposure keys its result dict by ticker, so a duplicate
            # would be silently collapsed and one row's weights lost.
            return None, f"{label}.ticker {key!r} is a duplicate issuer identity"
        seen.add(key)

        if "funds" not in row:
            return None, (
                f"{label} is missing required 'funds' — an absent membership key is "
                "not an empty membership, and treating it as one would drop this "
                "issuer's embedded exposure and understate the controls")
        raw_funds = row["funds"]
        if not isinstance(raw_funds, list):
            return None, f"{label}.funds must be a list"
        funds: list[dict] = []
        fund_seen: set[str] = set()
        for j, fund in enumerate(raw_funds):
            flabel = f"{label}.funds[{j}]"
            if not isinstance(fund, dict):
                return None, f"{flabel} is not a mapping"
            fund_id = fund.get("fund")
            if not isinstance(fund_id, str) or not fund_id.strip():
                return None, f"{flabel}.fund must be a non-empty string, got {fund_id!r}"
            if fund_id != fund_id.strip():
                return None, _padded_identity_reason(f"{flabel}.fund", fund_id)
            fund_key = fund_id.upper()
            if fund_key in fund_seen:
                return None, f"{flabel}.fund {fund_key!r} is a duplicate fund identity"
            fund_seen.add(fund_key)
            if "fund_holding_weight" not in fund:
                return None, f"{flabel} is missing 'fund_holding_weight'"
            weight, reason = _checked_pct(fund["fund_holding_weight"],
                                          f"{flabel}.fund_holding_weight",
                                          minimum=0.0)
            if reason is not None:
                return None, reason
            funds.append({"fund": fund_id, "fund_holding_weight": weight})
        issuers.append({"ticker": ticker, "funds": funds})

    return {"issuer_ceiling_pct": ceilings["issuer_ceiling_pct"],
            "common_driver_ceiling_pct": ceilings["common_driver_ceiling_pct"],
            "issuers": issuers,
            "retained_common_driver_measurement":
                lookthrough.get("retained_common_driver_measurement")}, None


TARGET_WEIGHT_BASIS = (
    "CANONICAL TARGET WEIGHTS (full-deployment basis) — not current holdings. "
    "Computed by supplying the production exposure helper a unit book of 100.0 "
    "with each row's own target_pct as its value, so direct and embedded "
    "percentages are target-weight percentages by construction."
)


def _utilisation(value: float, limit: float) -> float | None:
    if limit <= 0:
        return None
    return value / limit * 100.0


def _limit_status(value: float, limit: float,
                  approaching_pct: float = APPROACHING_UTILISATION_PCT) -> str:
    if limit <= 0:
        return UNAVAILABLE
    if value > limit:
        return OVER_LIMIT
    if math.isclose(value, limit, rel_tol=0.0, abs_tol=1e-9):
        return AT_LIMIT
    if _utilisation(value, limit) >= approaching_pct:
        return APPROACHING
    return OK


def collect_target_weight_concentration(
    *, targets_path: Path | str | None = None,
    lookthrough_path: Path | str | None = None,
    approaching_pct: float = APPROACHING_UTILISATION_PCT,
) -> TargetWeightConcentration:
    """Cluster, issuer, and common-driver exposure at canonical target weights.

    Issuer and common-driver arithmetic is the production helper's
    (`allocate._issuer_exposure`) — never re-implemented here. If that helper
    cannot be imported, this section reports UNAVAILABLE rather than
    substituting a second implementation.
    """
    targets_path = Path(targets_path) if targets_path is not None else TARGETS_FILE
    lookthrough_path = Path(lookthrough_path) if lookthrough_path is not None else LOOKTHROUGH_FILE

    def _unavailable(detail: str) -> TargetWeightConcentration:
        return TargetWeightConcentration(
            available=False, basis=TARGET_WEIGHT_BASIS, clusters=(), issuers=(),
            max_issuer=None, common_driver=None, destination_total_pct=None,
            status=UNAVAILABLE, detail=detail)

    try:
        import allocate
    except Exception as exc:  # pragma: no cover - environment-dependent
        return _unavailable(
            f"production exposure helper unavailable ({exc.__class__.__name__}); "
            "look-through arithmetic is deliberately NOT re-implemented here")

    try:
        targets = yaml.safe_load(targets_path.read_text()) or {}
        lookthrough = yaml.safe_load(lookthrough_path.read_text()) or {}
    except (OSError, yaml.YAMLError) as exc:
        return _unavailable(f"policy configuration unreadable: {exc.__class__.__name__}")
    if not isinstance(targets, dict) or not isinstance(lookthrough, dict):
        return _unavailable("policy configuration is not a mapping")

    # Validate the RAW rows FIRST. `allocate.build_roster` coerces with
    # `float(row["target_pct"])`, which silently accepts a boolean (True -> 1.0)
    # because bool subclasses int. That is production behaviour and is NOT
    # changed by this module — but this diagnostic will not report a
    # constraint computed from a value it cannot trust, so it checks the raw
    # config before the coercion happens. Controlled UNAVAILABLE, matching the
    # look-through path below: one malformed config value must not abort the
    # whole report and silence the sections that ARE readable.
    for i, row in enumerate(targets.get("destination") or []):
        if not isinstance(row, dict):
            continue
        ticker = row.get("ticker")
        label = f"destination row #{i} ({ticker!r}).target_pct"
        if "target_pct" in row:
            _, reason = _checked_pct(row["target_pct"], label)
            if reason is not None:
                return _unavailable(reason)

    # Ceilings and every consumed look-through row are REQUIRED and strictly
    # validated before the production exposure helper is called. No historical
    # literal is ever substituted for a missing safety-sensitive ceiling.
    validated, reason = validate_lookthrough(lookthrough)
    if reason is not None:
        return _unavailable(reason)
    lookthrough = validated

    try:
        roster = allocate.build_roster(targets)
    except Exception as exc:
        return _unavailable(f"canonical roster not parseable: {exc.__class__.__name__}: {exc}")

    # Target-weight basis: a unit book of 100.0 with each row's target_pct as
    # its dollar value makes value/book*100 == target_pct exactly.
    unit_book = 100.0
    target_values: dict[str, float] = {}
    for ticker, meta in roster.items():
        value, reason = _checked_pct(meta.get("target_pct"), f"{ticker}.target_pct")
        if reason is not None:
            return _unavailable(reason)
        target_values[ticker] = value
    destination_total = sum(target_values.values())

    clusters: list[ClusterConstraint] = []
    for raw in (targets.get("caps", {}) or {}).get("clusters", []) or []:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name", "<unnamed>"))
        cap, reason = _checked_pct(raw.get("pct"), f"cluster {name}.pct", minimum=0.0)
        if reason is not None:
            return _unavailable(reason)
        members = tuple(sorted(str(t).upper() for t in (raw.get("tickers") or [])))
        exposure = sum(target_values.get(t, 0.0) for t in members)
        if not members:
            status, detail = UNAVAILABLE, (
                "cluster has no members in the canonical roster — this cap cannot "
                "bind on anything and is dead configuration, not a satisfied limit")
        else:
            status = _limit_status(exposure, cap, approaching_pct)
            missing = tuple(t for t in members if t not in target_values)
            detail = (f"members absent from the canonical roster: {', '.join(missing)}"
                      if missing else "")
        clusters.append(ClusterConstraint(
            name=name, cap_pct=cap, members=members,
            target_exposure_pct=exposure,
            utilisation_pct=_utilisation(exposure, cap),
            headroom_pct=cap - exposure, status=status, detail=detail))

    issuer_ceiling = lookthrough["issuer_ceiling_pct"]
    driver_ceiling = lookthrough["common_driver_ceiling_pct"]

    exposure = allocate._issuer_exposure(target_values, unit_book, lookthrough)

    issuers: list[IssuerConstraint] = []
    for ticker, row in sorted(exposure["issuers"].items()):
        eff = float(row["effective_pct"])
        issuers.append(IssuerConstraint(
            ticker=ticker, direct_pct=float(row["direct_pct"]),
            embedded_pct=float(row["embedded_pct"]), effective_pct=eff,
            ceiling_pct=issuer_ceiling,
            utilisation_pct=_utilisation(eff, issuer_ceiling),
            headroom_pct=issuer_ceiling - eff,
            status=_limit_status(eff, issuer_ceiling, approaching_pct)))
    max_issuer = max(issuers, key=lambda i: i.effective_pct) if issuers else None

    recomputed = float(exposure["common_driver_current_pct"])
    retained_raw = lookthrough.get("retained_common_driver_measurement")
    retained_value: float | None = None
    retained_at: str | None = None
    if isinstance(retained_raw, dict):
        raw_value = retained_raw.get("value_pct")
        if isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool) \
                and math.isfinite(float(raw_value)):
            retained_value = float(raw_value)
        retained_at = _as_iso(retained_raw.get("measured_at"))

    if retained_value is None:
        reconciles = None
        delta = None
        flag = None
        detail = "no parseable retained measurement to reconcile against"
    else:
        delta = recomputed - retained_value
        reconciles = abs(delta) <= RETAINED_MEASUREMENT_TOLERANCE_PCT
        flag = None if reconciles else RETAINED_MEASUREMENT_DISCREPANCY
        detail = ("retained measurement reconciles with recomputation"
                  if reconciles else
                  f"retained {retained_value:.4f}% (measured {retained_at}) does not "
                  f"reconcile with recomputation {recomputed:.4f}% from the currently "
                  f"committed targets.yaml + issuer_lookthrough.yaml; delta "
                  f"{delta:+.4f}pp. Reported only — the retained measurement is NOT "
                  "replaced, the ceiling is NOT changed, and no policy response is "
                  "inferred.")

    limit_status = _limit_status(recomputed, driver_ceiling, approaching_pct)
    driver_status = DISCREPANCY if flag else limit_status
    common_driver = CommonDriverConstraint(
        recomputed_pct=recomputed, ceiling_pct=driver_ceiling,
        utilisation_pct=_utilisation(recomputed, driver_ceiling),
        headroom_pct=driver_ceiling - recomputed,
        retained_value_pct=retained_value, retained_measured_at=retained_at,
        retained_delta_pct=delta, reconciles=reconciles,
        status=driver_status, limit_status=limit_status, discrepancy_flag=flag,
        detail=(detail + f" | limit status at target weights: {limit_status}"))

    severities = ([c.status for c in clusters] + [i.status for i in issuers]
                  + [driver_status, limit_status])
    if OVER_LIMIT in severities or DISCREPANCY in severities:
        overall = OVER_LIMIT if OVER_LIMIT in severities else DISCREPANCY
    elif AT_LIMIT in severities:
        overall = AT_LIMIT
    elif APPROACHING in severities:
        overall = APPROACHING
    elif UNAVAILABLE in severities:
        overall = UNAVAILABLE
    else:
        overall = OK

    return TargetWeightConcentration(
        available=True, basis=TARGET_WEIGHT_BASIS, clusters=tuple(clusters),
        issuers=tuple(issuers), max_issuer=max_issuer, common_driver=common_driver,
        destination_total_pct=destination_total, status=overall,
        detail="")


# ── section 6: current-holdings concentration status ──────────────────────

@dataclass(frozen=True)
class CurrentHoldingsExposure:
    """Current-holdings exposure, or an explicit refusal to fabricate one."""
    available: bool
    result: str
    status: str
    detail: str
    clusters: tuple[ClusterConstraint, ...] = ()
    issuers: tuple[IssuerConstraint, ...] = ()
    common_driver: CommonDriverConstraint | None = None

    def as_dict(self) -> dict:
        return {"available": self.available, "result": self.result,
                "status": self.status, "detail": self.detail,
                "clusters": [c.as_dict() for c in self.clusters],
                "issuers": [i.as_dict() for i in self.issuers],
                "common_driver": self.common_driver.as_dict() if self.common_driver else None}


def collect_current_holdings_exposure(
    repository_state: RepositoryAccountState,
    *, supplied_exposure: dict | None = None,
) -> CurrentHoldingsExposure:
    """Repository-only default: UNAVAILABLE_FROM_REPOSITORY_STATE.

    `supplied_exposure` is a PURE SEAM for a later, separately authorized
    caller that has already computed current exposure from confirmed private
    evidence through the accepted adapter. This function performs NO account
    ingestion, accepts no credentials, reads no runtime root, and stores
    nothing. Passing None — the default, and the only path this unit
    exercises against the real repository — yields UNAVAILABLE.

    When supplied, the caller owns the numbers entirely; this function only
    labels and passes them through, and never re-derives or persists them.
    """
    if supplied_exposure is None:
        if repository_state.verdict == REPOSITORY_STATE_CURRENT:
            detail = ("repository account state is current, but current-holdings "
                      "exposure is still not computed here: this unit's scope is "
                      "the preflight, and exposure at current holdings requires an "
                      "explicitly supplied, already-computed result")
        else:
            detail = ("repository account state is not current "
                      f"({repository_state.verdict}), so any exposure computed from "
                      "it would be a stale observation presented as a current one. "
                      "Refused. Supply already-computed exposure from confirmed "
                      "private evidence via the accepted adapter instead.")
        return CurrentHoldingsExposure(
            available=False, result=CURRENT_HOLDINGS_UNAVAILABLE,
            status=UNAVAILABLE, detail=detail)

    if not isinstance(supplied_exposure, dict):
        raise CurrentnessReportError("supplied_exposure must be a mapping or None")

    clusters = tuple(supplied_exposure.get("clusters") or ())
    issuers = tuple(supplied_exposure.get("issuers") or ())
    driver = supplied_exposure.get("common_driver")
    for row in clusters:
        if not isinstance(row, ClusterConstraint):
            raise CurrentnessReportError("supplied clusters must be ClusterConstraint values")
    for row in issuers:
        if not isinstance(row, IssuerConstraint):
            raise CurrentnessReportError("supplied issuers must be IssuerConstraint values")
    if driver is not None and not isinstance(driver, CommonDriverConstraint):
        raise CurrentnessReportError("supplied common_driver must be a CommonDriverConstraint")

    severities = [c.status for c in clusters] + [i.status for i in issuers]
    if driver is not None:
        severities.append(driver.status)
    for level in (OVER_LIMIT, DISCREPANCY, AT_LIMIT, APPROACHING, UNAVAILABLE):
        if level in severities:
            status = level
            break
    else:
        status = OK if severities else UNAVAILABLE

    return CurrentHoldingsExposure(
        available=True, result="SUPPLIED_BY_CALLER", status=status,
        detail=("exposure supplied by the caller from already-confirmed evidence; "
                "this module computed, re-derived, and stored none of it"),
        clusters=clusters, issuers=issuers, common_driver=driver)


# ── section 7/8: binding-constraint summary and authority disclaimer ──────

AUTHORITY_DISCLAIMER = (
    "This module reports state and evidence only. It does not create policy. "
    "It does not change membership, target weights, caps, cluster definitions, "
    "gates, or margin rules. It authorizes no transaction and recommends no "
    "buy, sell, trim, or hold. It does not make external-event evidence "
    "operative. Nothing here is an investment score, ranking, or opinion about "
    "any security."
)

_SEVERITY_ORDER = (OVER_LIMIT, DISCREPANCY, AT_LIMIT, STALE, UNVERIFIED,
                   UNAVAILABLE, APPROACHING, OK)


@dataclass(frozen=True)
class AttentionItem:
    area: str
    status: str
    message: str

    def as_dict(self) -> dict:
        return {"area": self.area, "status": self.status, "message": self.message}


@dataclass(frozen=True)
class CurrentnessReport:
    generated_at: str
    as_of_date: str
    repository_account_state: RepositoryAccountState
    company_intelligence: CompanyIntelligenceCurrentness
    freshness_monitor: FreshnessMonitorStatus
    committed_staleness_report: CommittedStalenessReportHealth
    target_weight_concentration: TargetWeightConcentration
    current_holdings_exposure: CurrentHoldingsExposure
    attention: tuple[AttentionItem, ...]
    overall_status: str
    authority_disclaimer: str = AUTHORITY_DISCLAIMER

    def as_dict(self) -> dict:
        return {
            "generated_at": self.generated_at, "as_of_date": self.as_of_date,
            "repository_account_state": self.repository_account_state.as_dict(),
            "company_intelligence": self.company_intelligence.as_dict(),
            "freshness_monitor": self.freshness_monitor.as_dict(),
            "committed_staleness_report": self.committed_staleness_report.as_dict(),
            "target_weight_concentration": self.target_weight_concentration.as_dict(),
            "current_holdings_exposure": self.current_holdings_exposure.as_dict(),
            "attention": [a.as_dict() for a in self.attention],
            "overall_status": self.overall_status,
            "authority_disclaimer": self.authority_disclaimer,
        }


def _worst(statuses) -> str:
    present = [s for s in statuses if s in STATUSES]
    for level in _SEVERITY_ORDER:
        if level in present:
            return level
    return OK


def _canonical_equities(targets_path: Path) -> tuple[str, ...]:
    try:
        targets = yaml.safe_load(targets_path.read_text()) or {}
    except (OSError, yaml.YAMLError):
        return ()
    if not isinstance(targets, dict):
        return ()
    return tuple(sorted(
        str(row.get("ticker")).upper()
        for row in (targets.get("destination") or [])
        if isinstance(row, dict) and row.get("asset_class") == "equity"
        and isinstance(row.get("ticker"), str)))


def build_report(
    *, root: Path | str | None = None,
    as_of: datetime | date | None = None,
    supplied_exposure: dict | None = None,
    approaching_pct: float = APPROACHING_UTILISATION_PCT,
) -> CurrentnessReport:
    """Assemble every section. Read-only end to end."""
    base = Path(root) if root is not None else HERE
    if isinstance(as_of, datetime):
        as_of_date = as_of.date()
        as_of_dt: datetime | date | None = as_of
    elif isinstance(as_of, date):
        as_of_date = as_of
        as_of_dt = as_of
    else:
        as_of_date = date.today()
        as_of_dt = None

    targets_path = base / "targets.yaml"
    canonical = _canonical_equities(targets_path)

    repo_state = collect_repository_account_state(
        holdings_path=base / "holdings.yaml", as_of=as_of_dt)
    companies = collect_company_currentness(
        companies_dir=base / "intelligence" / "companies",
        canonical_equities=canonical, as_of_date=as_of_date)
    monitor = collect_freshness_monitor_status(
        registry_path=base / "intelligence" / "freshness_registry.yaml",
        checkpoints_path=base / "intelligence" / "freshness_checkpoints.yaml")
    staleness = inspect_committed_staleness_report(
        report_path=base / "intelligence" / "reports" / "staleness_report.md",
        current_company_count=companies.record_count, as_of_date=as_of_date)
    concentration = collect_target_weight_concentration(
        targets_path=targets_path,
        lookthrough_path=base / "issuer_lookthrough.yaml",
        approaching_pct=approaching_pct)
    holdings_exposure = collect_current_holdings_exposure(
        repo_state, supplied_exposure=supplied_exposure)

    attention: list[AttentionItem] = []

    if repo_state.verdict != REPOSITORY_STATE_CURRENT:
        attention.append(AttentionItem(
            area="repository account state", status=STALE,
            message=(f"{repo_state.verdict} — repository baseline cannot support a "
                     "current dollar recommendation; confirmed private evidence is "
                     "required for a current allocation run")))
    attention.append(AttentionItem(
        area="current margin usage", status=UNAVAILABLE,
        message=MARGIN_USAGE_UNAVAILABLE))

    if companies.overdue_count:
        attention.append(AttentionItem(
            area="company intelligence", status=STALE,
            message=f"{companies.overdue_count} company record(s) overdue under the existing next_due rule"))
    if companies.total_lapsed_catalysts:
        attention.append(AttentionItem(
            area="company intelligence", status=UNVERIFIED,
            message=(f"{companies.total_lapsed_catalysts} lapsed pending catalyst(s) across "
                     f"{companies.records_with_lapsed_catalysts} record(s)")))
    if companies.records_without_catalysts:
        attention.append(AttentionItem(
            area="company intelligence", status=UNVERIFIED,
            message=(f"{companies.records_without_catalysts} record(s) declare no catalysts — "
                     "the only derivable event signal cannot fire for them")))
    if companies.canonical_uncovered:
        attention.append(AttentionItem(
            area="company intelligence", status=UNAVAILABLE,
            message=f"canonical equities without a record: {', '.join(companies.canonical_uncovered)}"))

    if not monitor.operational_event_monitoring_exists:
        attention.append(AttentionItem(
            area="freshness monitoring", status=UNVERIFIED,
            message=(f"no ticker has verified live monitoring "
                     f"({monitor.monitoring_enabled_count}/{monitor.enrolled_count} enabled, "
                     f"{monitor.verified_checkpoint_count}/{monitor.enrolled_count} checkpoints verified) "
                     "— a date-cadence mechanism exists; operational event monitoring does not")))
    if not monitor.schema_valid:
        attention.append(AttentionItem(
            area="freshness monitoring", status=UNVERIFIED,
            message=f"registry/checkpoint schema validation failed ({len(monitor.schema_errors)} error(s))"))
    if monitor.duplicate_tickers:
        attention.append(AttentionItem(
            area="freshness monitoring", status=UNVERIFIED,
            message=f"duplicate registry ticker identity: {', '.join(monitor.duplicate_tickers)}"))

    if staleness.status != OK:
        attention.append(AttentionItem(
            area="committed staleness report", status=staleness.status,
            message=staleness.detail))

    for cluster in concentration.clusters:
        if cluster.status in (OVER_LIMIT, AT_LIMIT, APPROACHING, UNAVAILABLE):
            attention.append(AttentionItem(
                area=f"cluster cap: {cluster.name}", status=cluster.status,
                message=(f"{cluster.target_exposure_pct:.2f}% of book at target vs "
                         f"{cluster.cap_pct:.2f}% cap"
                         + (f" — {cluster.detail}" if cluster.detail else ""))))
    for issuer in concentration.issuers:
        if issuer.status in (OVER_LIMIT, AT_LIMIT, APPROACHING):
            attention.append(AttentionItem(
                area=f"issuer ceiling: {issuer.ticker}", status=issuer.status,
                message=(f"effective {issuer.effective_pct:.2f}% at target vs "
                         f"{issuer.ceiling_pct:.2f}% ceiling")))
    if concentration.max_issuer is not None:
        mi = concentration.max_issuer
        attention.append(AttentionItem(
            area="issuer ceiling: closest to limit", status=mi.status,
            message=(f"{mi.ticker} is the highest effective issuer exposure at target "
                     f"weights: {mi.effective_pct:.4f}% against a {mi.ceiling_pct:.2f}% "
                     f"ceiling ({mi.headroom_pct:+.4f}pp headroom). Reported at every "
                     "status so the closest constraint is never invisible.")))
    driver = concentration.common_driver
    if driver is not None and driver.status != OK:
        attention.append(AttentionItem(
            area="AI/platform common-driver ceiling", status=driver.status,
            message=(f"recomputed {driver.recomputed_pct:.4f}% at target vs "
                     f"{driver.ceiling_pct:.2f}% ceiling. {driver.detail}")))
    if not concentration.available:
        attention.append(AttentionItem(
            area="target-weight concentration", status=UNAVAILABLE,
            message=concentration.detail))

    attention.append(AttentionItem(
        area="current-holdings exposure", status=holdings_exposure.status,
        message=f"{holdings_exposure.result} — {holdings_exposure.detail}"))

    repo_status = (OK if repo_state.verdict == REPOSITORY_STATE_CURRENT
                   else STALE)
    overall = _worst([repo_status, companies.status, monitor.status,
                      staleness.status, concentration.status,
                      holdings_exposure.status])

    generated = (as_of_dt.isoformat() if isinstance(as_of_dt, datetime)
                 else as_of_date.isoformat())

    return CurrentnessReport(
        generated_at=generated, as_of_date=as_of_date.isoformat(),
        repository_account_state=repo_state, company_intelligence=companies,
        freshness_monitor=monitor, committed_staleness_report=staleness,
        target_weight_concentration=concentration,
        current_holdings_exposure=holdings_exposure,
        attention=tuple(attention), overall_status=overall)


# ── rendering ─────────────────────────────────────────────────────────────

def _pct(value: float | None, width: int = 7, places: int = 2) -> str:
    return "n/a".rjust(width) if value is None else f"{value:.{places}f}%".rjust(width)


def render(report: CurrentnessReport) -> str:
    """Human-readable stdout view. Same facts as `as_dict()`, no others."""
    L: list[str] = []
    A = L.append
    A("PORTFOLIO-HQ — CURRENTNESS & BINDING-CONSTRAINT PREFLIGHT")
    A(f"as-of {report.as_of_date}   overall: {report.overall_status}")
    A("recommendation-only diagnostic — no policy, no account access, no trade.")
    A("")

    r = report.repository_account_state
    A("1. REPOSITORY ACCOUNT-STATE STATUS")
    A(f"   verdict                     {r.verdict}")
    A(f"   cash observation            {r.cash_state} (synced {r.cash_synced_at}, age {r.cash_age_days}d)")
    A(f"   margin observation          {r.margin_state} (synced {r.margin_synced_at}, age {r.margin_age_days}d)")
    # None is NOT "False": completeness was never evaluated, because the
    # position tracks were not all declared. Say that rather than printing a
    # bare None a reader could take for a falsy result.
    A(f"   valuation complete          "
      f"{'NOT EVALUATED (position tracks undeclared)' if r.valuation_complete is None else r.valuation_complete}")
    A(f"   dollars from repo state     {r.dollars_from_repository_state}")
    for note in r.holdings_observation_notes:
        A(f"     · {note}")
    for reason in r.blocked_by:
        A(f"     blocked: {reason}")
    A(f"   CURRENT MARGIN USAGE        {r.margin_usage_statement}")
    pe = r.private_evidence
    A(f"   private-evidence path       available={pe.available} module={pe.module} entrypoint={pe.entrypoint} schema_version={pe.schema_version}")
    A(f"     · {pe.detail}")
    for note in r.notes:
        A(f"     · {note}")
    A("")

    c = report.company_intelligence
    A("2. COMPANY-INTELLIGENCE CURRENTNESS")
    A(f"   records {c.record_count}   overdue {c.overdue_count}   "
      f"records w/ lapsed catalysts {c.records_with_lapsed_catalysts}   "
      f"lapsed catalysts {c.total_lapsed_catalysts}")
    A(f"   records with no catalysts   {c.records_without_catalysts}")
    A(f"   schema-invalid records      {c.schema_invalid_count}")
    A(f"   canonical covered           {len(c.canonical_covered)}")
    A(f"   canonical uncovered         {len(c.canonical_uncovered)}"
      + (f" ({', '.join(c.canonical_uncovered)})" if c.canonical_uncovered else ""))
    A(f"   non-roster records          {len(c.non_roster_records)}")
    if c.lapsed_catalysts:
        A("   lapsed pending catalysts (expected < as-of, status pending):")
        for row in c.lapsed_catalysts:
            mark = "*" if row.in_canonical_roster else " "
            A(f"     {row.expected} {row.ticker:<6}{mark} {row.days_overdue:>4}d  {row.catalyst[:74]}")
        A("     (* = canonical roster name)")
    A(f"   NOTE: {c.notes[0] if c.notes else ''}")
    A("")

    m = report.freshness_monitor
    A("3. FRESHNESS MONITOR STATUS")
    A(f"   enrolled {m.enrolled_count}   monitoring enabled {m.monitoring_enabled_count}   "
      f"checkpoints verified {m.verified_checkpoint_count}   pending/unverified {m.pending_or_unverified_count}")
    A(f"   registry/checkpoint schema valid  {m.schema_valid}")
    if m.duplicate_tickers:
        A(f"   duplicate registry tickers        {', '.join(m.duplicate_tickers)}")
    A(f"   date-cadence mechanism exists     {m.cadence_mechanism_exists}")
    A(f"   operational event monitoring      {m.operational_event_monitoring_exists}")
    A(f"   NOTE: {m.notes[0] if m.notes else ''}")
    A("")

    s = report.committed_staleness_report
    A("4. COMMITTED STALENESS-REPORT HEALTH")
    A(f"   status {s.status}   as-of {s.as_of_date}   claims {s.companies_scanned_claim} scanned   "
      f"records now {s.current_company_count}")
    A(f"     · {s.detail}")
    A("")

    t = report.target_weight_concentration
    A("5. TARGET-WEIGHT CONCENTRATION PREFLIGHT")
    A(f"   basis: {t.basis}")
    if not t.available:
        A(f"   {t.status} — {t.detail}")
    else:
        A(f"   destination total {t.destination_total_pct:.2f}%")
        A("   cluster caps:")
        A(f"     {'name':<14}{'cap':>8}{'target':>9}{'util':>9}{'headroom':>10}  status")
        for cl in t.clusters:
            A(f"     {cl.name:<14}{_pct(cl.cap_pct,8)}{_pct(cl.target_exposure_pct,9)}"
              f"{_pct(cl.utilisation_pct,9,1)}{_pct(cl.headroom_pct,10)}  {cl.status}"
              + (f"  — {cl.detail}" if cl.detail else ""))
        A("   effective issuer exposure (8% ceiling family):")
        A(f"     {'ticker':<8}{'direct':>9}{'embedded':>10}{'effective':>11}{'headroom':>10}  status")
        for iss in t.issuers:
            A(f"     {iss.ticker:<8}{_pct(iss.direct_pct,9)}{_pct(iss.embedded_pct,10)}"
              f"{_pct(iss.effective_pct,11)}{_pct(iss.headroom_pct,10)}  {iss.status}")
        if t.max_issuer is not None:
            A(f"     maximum effective issuer: {t.max_issuer.ticker} "
              f"{t.max_issuer.effective_pct:.4f}% (ceiling {t.max_issuer.ceiling_pct:.2f}%) "
              f"→ {t.max_issuer.status}")
        d = t.common_driver
        if d is not None:
            A("   AI/platform common-driver ceiling:")
            A(f"     recomputed at target weights  {d.recomputed_pct:.4f}%")
            A(f"     ceiling                       {d.ceiling_pct:.2f}%   headroom {d.headroom_pct:+.4f}pp")
            A(f"     retained measurement          "
              + ("n/a" if d.retained_value_pct is None
                 else f"{d.retained_value_pct:.4f}% (measured {d.retained_measured_at})"))
            if d.retained_delta_pct is not None:
                A(f"     recomputed − retained         {d.retained_delta_pct:+.4f}pp")
            if d.discrepancy_flag:
                A(f"     {d.discrepancy_flag}")
            A(f"     status {d.status}   ceiling verdict {d.limit_status}")
            A(f"     {d.detail}")
    A("")

    h = report.current_holdings_exposure
    A("6. CURRENT-HOLDINGS CONCENTRATION STATUS")
    A(f"   CURRENT_HOLDINGS_EXPOSURE: {h.result}")
    A(f"   status {h.status}")
    A(f"     · {h.detail}")
    A("")

    A("7. BINDING-CONSTRAINT SUMMARY")
    A("   Before trusting an allocation recommendation, these need attention:")
    for item in report.attention:
        A(f"     [{item.status:<11}] {item.area}")
        A(f"                    {item.message}")
    A("")

    A("8. CURRENTNESS VS INVESTMENT AUTHORITY")
    for line in report.authority_disclaimer.split(". "):
        if line.strip():
            A(f"   · {line.strip().rstrip('.')}.")
    return "\n".join(L)


# ── CLI ───────────────────────────────────────────────────────────────────

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="currentness_report.py",
        description=("Read-only currentness and binding-constraint preflight. "
                     "Writes nothing, accesses no brokerage, recommends no trade."))
    parser.add_argument("--json", action="store_true",
                        help="emit the machine-readable result instead of the text view")
    parser.add_argument("--root", default=None,
                        help="repository root to read (defaults to this file's directory)")
    parser.add_argument("--as-of", default=None,
                        help="ISO date to evaluate against (defaults to today)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    as_of: date | None = None
    if args.as_of:
        parsed = _parse_date(args.as_of)
        if parsed is None:
            print(f"error: --as-of must be an ISO calendar date, got {args.as_of!r}",
                  file=sys.stderr)
            return 2
        as_of = parsed
    report = build_report(root=args.root, as_of=as_of)
    if args.json:
        print(json.dumps(report.as_dict(), indent=2, sort_keys=True, default=str))
    else:
        print(render(report))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
