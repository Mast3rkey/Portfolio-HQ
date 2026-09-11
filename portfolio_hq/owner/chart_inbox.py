"""Chart intake inbox — a deliberate, inspectable quarantine for owner-supplied
chart images.

Trust boundary
--------------
This module is the ONLY place in ``portfolio_hq`` that writes bytes the owner
supplied. It writes exclusively beneath one explicitly-provided ``inbox_root``
and derives every stored path from server-generated identifiers, never from a
client-supplied filename. It imports nothing from the repository's investment
code: no ``allocate``, no ``margin_state``, no brokerage client, no
``holdings.yaml``/``targets.yaml``/``gates.yaml`` reader. Standard library only.

What intake is, and is not
--------------------------
Intake is *evidence receipt*, not adoption. A stored chart is quarantined as
unreviewed and untrusted. Nothing here — and nothing that reads what this
writes — changes portfolio membership, Level-1 or Level-2 targets, policy,
cluster caps, margin doctrine, holdings, Stage-1 state, or any order. There is
no order path in this package at all.

Accepted formats are PNG and JPEG only, decided by inspecting the file's own
leading bytes and parsing its real dimension header. A client-supplied
extension is never trusted, never used to choose a storage path, and never
used to decide the media type; it is retained for display and flagged when it
disagrees with the actual content.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path

from . import image_integrity

# ── contract constants ───────────────────────────────────────────────────────

SCHEMA_VERSION = 1

#: Hard ceiling on a single upload. The largest image in the repository's own
#: accepted CHART-0002 cohort is ~1.8 MB; 25 MiB leaves generous headroom for a
#: high-resolution tablet screenshot while keeping the bound small enough that a
#: single request can never exhaust a small private host.
MAX_UPLOAD_BYTES = 25 * 1024 * 1024

#: PNG only. HEIC/HEIF, WebP, GIF, SVG, PDF, JPEG and everything else are
#: rejected rather than silently transcoded: this unit adds no image-decoding
#: dependency, and a format whose completeness we cannot establish from its own
#: bytes is a format we cannot honestly quarantine. PNG is the only format whose
#: completeness the standard library can actually prove — see
#: ``image_integrity``'s own module docstring for why JPEG was withdrawn rather
#: than admitted on a structural check that could not guarantee decodability.
#: The owner converts to PNG before uploading; the service never transcodes.
#: Defined once, in image_integrity, so the accepted set and the set actually
#: verified can never drift apart.
SUPPORTED_MEDIA_TYPES = image_integrity.SUPPORTED_MEDIA_TYPES

_EXTENSION_FOR_MEDIA_TYPE = {"image/png": "png"}
_EXTENSIONS_MATCHING_MEDIA_TYPE = {"image/png": frozenset({"png"})}

#: Persisted intake states. Closed vocabulary. This unit only ever writes these
#: two. Post-intake review transitions are intentionally NOT implemented here —
#: see ``review`` in the record, which stays un-decided.
STATE_QUARANTINED = "quarantined_unreviewed"
STATE_DUPLICATE = "duplicate"
INTAKE_STATES = (STATE_QUARANTINED, STATE_DUPLICATE)

#: Closed rejection vocabulary. A rejection writes NOTHING to disk (no record,
#: no bytes) so a hostile or clumsy caller cannot fill the volume; the reason is
#: returned to the caller for immediate display instead.
REJECTION_REASONS = (
    "empty_payload",
    "payload_too_large",
    "unsupported_media_type",
    "corrupt_or_unreadable_image",
    "invalid_ticker",
    "invalid_timeframe",
)

CHARTS_DIRNAME = "charts"
RECORD_FILENAME = "intake.json"
#: Private staging area, a sibling of charts/ so a completed intake moves
#: into place with one same-filesystem rename. list_records() only scans
#: charts/, so an in-flight intake is never visible to the index.
STAGING_DIRNAME = ".incoming"

_INTAKE_ID_RE = re.compile(r"\A[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}\Z")
_TICKER_RE = re.compile(r"\A[A-Z0-9][A-Z0-9.\-]{0,11}\Z")
_TIMEFRAME_RE = re.compile(r"\A[A-Za-z0-9]{1,8}\Z")
_DISPLAY_FILENAME_SAFE_RE = re.compile(r"[^A-Za-z0-9._ -]")
_MAX_DISPLAY_FILENAME = 128


# ── errors ───────────────────────────────────────────────────────────────────

class ChartIntakeRejected(Exception):
    """Validation failed. Nothing was written."""

    def __init__(self, reason: str, message: str) -> None:
        if reason not in REJECTION_REASONS:
            raise ValueError(f"unknown rejection reason: {reason!r}")
        super().__init__(message)
        self.reason = reason
        self.message = message


class ChartInboxStorageError(Exception):
    """The inbox directory could not be created or written. Nothing usable was
    stored. Raised instead of a bare OSError so a caller can distinguish
    "the owner sent something bad" from "this host cannot store anything"."""


# ── content inspection (never trusts the filename) ──────────────────────────
#
# Delegated to image_integrity, which verifies the WHOLE byte stream rather
# than a magic number and a dimension field. Reading IHDR dimensions proves an
# image starts like a PNG; it does not prove the bytes form a complete image a
# later reviewer can open. See that module for exactly what each format's check
# does and does not establish.

sniff_media_type = image_integrity.sniff_media_type


# ── identity and display-name handling ───────────────────────────────────────

def sanitize_display_filename(raw: object) -> tuple[str, bool]:
    """Reduce a client-supplied filename to safe *display* text.

    Returns ``(safe_text, was_modified)``. The result is never used to build a
    path — see ``ingest``, which derives every path from the server-generated
    intake id. Directory separators, parent references, drive letters, NUL and
    control characters are removed here so the string is also safe to render.
    """
    original = "" if raw is None else str(raw)
    # Take the last path component under both POSIX and Windows conventions,
    # then drop anything that is not plainly printable filename text.
    candidate = original.replace("\\", "/").split("/")[-1]
    candidate = candidate.replace("\x00", "")
    candidate = _DISPLAY_FILENAME_SAFE_RE.sub("_", candidate)
    candidate = candidate.strip(" .")
    while ".." in candidate:
        candidate = candidate.replace("..", ".")
    candidate = candidate[:_MAX_DISPLAY_FILENAME]
    if not candidate:
        candidate = "(unnamed upload)"
    return candidate, candidate != original


def new_intake_id(now: datetime | None = None) -> str:
    """Server-generated storage identity: a UTC timestamp plus 48 random bits.

    Contains no client-supplied character. Matches ``_INTAKE_ID_RE``, which is
    re-checked before the id is ever joined to a path.
    """
    stamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return f"{stamp.strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(6)}"


def _validated_intake_id(intake_id: object) -> str:
    text = "" if intake_id is None else str(intake_id)
    if not _INTAKE_ID_RE.match(text):
        raise ValueError(f"refusing to build a path from intake id {intake_id!r}")
    return text


def _assert_not_redirected(path: Path, label: str) -> None:
    """Refuse a path that does not resolve to itself.

    Containment is checked by *identity after resolution*, not by comparing
    string prefixes: a prefix test is satisfied by a path that merely looks
    contained while a symlinked component redirects the real write elsewhere.
    """
    if os.path.islink(path):
        raise ChartInboxStorageError(
            f"the chart inbox {label} is a symbolic link; refusing to write "
            f"through it: {path}")
    try:
        resolved = os.path.realpath(path)
    except OSError as exc:  # pragma: no cover - defensive
        raise ChartInboxStorageError(
            f"could not resolve the chart inbox {label}: {exc}") from exc
    if resolved != str(path):
        raise ChartInboxStorageError(
            f"the chart inbox {label} resolves outside itself ({resolved}); "
            f"refusing to write through a redirected path")


def _charts_root(inbox_root: Path | str, *, create: bool) -> Path:
    """The charts directory, resolved and proven to be contained.

    ``inbox_root`` itself is resolved first and the result treated as
    authoritative: an operator may legitimately point the inbox at a mounted
    volume through a symlink. Everything *beneath* that resolved root must not
    be redirected — ``Path.mkdir`` and ``open`` both follow a symlinked parent,
    so a symlink at ``charts`` would otherwise place the generated intake
    directory, the image and the record entirely outside the configured inbox.
    """
    try:
        root = Path(os.path.realpath(Path(inbox_root)))
    except OSError as exc:  # pragma: no cover - defensive
        raise ChartInboxStorageError(
            f"could not resolve the chart inbox root: {exc}") from exc
    charts = root / CHARTS_DIRNAME
    # Check BEFORE creating anything: mkdir(exist_ok=True) on a symlink to an
    # existing directory succeeds silently and writes to the target.
    if os.path.islink(charts):
        raise ChartInboxStorageError(
            f"the chart inbox 'charts' path is a symbolic link; refusing to "
            f"write through it: {charts}")
    if create:
        try:
            charts.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise ChartInboxStorageError(
                f"could not create the chart inbox directory: {exc}") from exc
    _assert_not_redirected(charts, "'charts' directory")
    if create and not charts.is_dir():
        raise ChartInboxStorageError(
            f"the chart inbox 'charts' path is not a directory: {charts}")
    return charts


def _charts_root_for_read(inbox_root: Path | str) -> Path | None:
    """The charts directory for read-only use, or ``None`` if unusable.

    Fails closed in the same cases the write path refuses, so a redirected
    inbox cannot make duplicate detection or the record listing report on a
    directory the write path would never have used.
    """
    try:
        charts = _charts_root(inbox_root, create=False)
    except ChartInboxStorageError:
        return None
    return charts if charts.is_dir() else None


def _record_dir(inbox_root: Path, intake_id: str) -> Path:
    return _charts_root(inbox_root, create=False) / _validated_intake_id(intake_id)


# ── read side ────────────────────────────────────────────────────────────────

def list_records(inbox_root: Path | str) -> list[dict]:
    """Every readable intake record, newest first. Missing inbox → empty list.

    The filesystem is the index: there is no separate database or manifest to
    drift out of sync with what is actually stored.
    """
    charts = _charts_root_for_read(inbox_root)
    if charts is None:
        return []
    records: list[dict] = []
    for entry in sorted(charts.iterdir(), reverse=True):
        if not entry.is_dir() or not _INTAKE_ID_RE.match(entry.name):
            continue
        record_path = entry / RECORD_FILENAME
        try:
            loaded = json.loads(record_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(loaded, dict):
            records.append(loaded)
    records.sort(key=lambda r: str(r.get("received_at", "")), reverse=True)
    return records


def find_by_content_hash(inbox_root: Path | str, content_sha256: str) -> dict | None:
    """The first *stored* record whose retained bytes have this hash.

    Duplicate markers are skipped: a duplicate holds no bytes of its own, so
    chaining duplicates to duplicates would produce a reference with no image
    behind it.
    """
    # Sort on (received_at, intake_id): receipt timestamps have one-second
    # resolution, so two uploads within the same second would otherwise resolve
    # by incidental ordering. The intake id begins with that same timestamp and
    # ends in random hex, making the tie-break stable and reproducible.
    ordered = sorted(
        list_records(inbox_root),
        key=lambda r: (str(r.get("received_at", "")), str(r.get("intake_id", ""))),
    )
    for record in ordered:
        if record.get("state") == STATE_QUARANTINED and \
                record.get("content_sha256") == content_sha256:
            return record
    return None


# ── write side ───────────────────────────────────────────────────────────────

def _validated_ticker(value: object, allowed: frozenset[str] | None) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    if not text:
        return None
    if not _TICKER_RE.match(text):
        raise ChartIntakeRejected(
            "invalid_ticker",
            "The submitted ticker is not a well-formed symbol.",
        )
    if not allowed:
        raise ChartIntakeRejected(
            "invalid_ticker",
            "No accepted instrument list is available right now, so a ticker "
            "cannot be attached to this upload. Submit it without a ticker, or "
            "rebuild the presentation export first.",
        )
    if text not in allowed:
        raise ChartIntakeRejected(
            "invalid_ticker",
            f"{text} is not in the accepted Portfolio-HQ instrument list.",
        )
    return text


def _validated_timeframe(value: object, allowed: frozenset[str] | None) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if not _TIMEFRAME_RE.match(text):
        raise ChartIntakeRejected(
            "invalid_timeframe", "The submitted timeframe is not well formed."
        )
    if not allowed or text not in allowed:
        raise ChartIntakeRejected(
            "invalid_timeframe",
            f"{text} is not one of the accepted chart timeframes.",
        )
    return text


def _publish_intake(inbox_root: Path | str, intake_id: str, record: dict, *,
                    image: bytes | None, stored_filename: str | None) -> None:
    """Write one intake so that it is either wholly present or wholly absent.

    A chart inbox whose index is the filesystem cannot afford a half-written
    intake. The original build order — create directory, write image, write
    record — left the image bytes on disk when the record write failed late
    (disk full, quota, I/O error), so the owner was told the chart was NOT
    received while its bytes stayed behind, invisible to ``list_records`` and
    ambiguous for future duplicate detection.

    The intake is therefore assembled in a private staging directory and moved
    into place with a single ``os.rename``, which is atomic within a
    filesystem. Any failure before that rename removes the staging tree, so a
    failed intake leaves nothing at all. Nothing outside the staging directory
    this call created is ever removed.
    """
    charts = _charts_root(inbox_root, create=True)
    final = charts / _validated_intake_id(intake_id)

    # Claim-time collision check. Renaming a directory onto an existing *empty*
    # directory would otherwise succeed silently, which would be an overwrite.
    if os.path.lexists(final):
        raise ChartInboxStorageError(f"intake directory already exists: {final}")

    staging_root = charts.parent / STAGING_DIRNAME
    staging = staging_root / f"{intake_id}.{secrets.token_hex(6)}"
    try:
        staging_root.mkdir(parents=True, exist_ok=True)
        _assert_not_redirected(staging_root, "staging directory")
        staging.mkdir(parents=False, exist_ok=False)
    except OSError as exc:
        raise ChartInboxStorageError(
            f"could not stage the chart intake: {exc}") from exc

    try:
        if stored_filename is not None and image is not None:
            # "xb" is O_CREAT|O_EXCL: an existing file is an error, never an
            # overwrite, and O_EXCL refuses to follow a final-component
            # symlink. The name is a fixed constant, so no client-supplied
            # text reaches the filesystem.
            with open(staging / stored_filename, "xb") as handle:
                handle.write(image)
        with open(staging / RECORD_FILENAME, "x", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2, sort_keys=True)
            handle.write("\n")
        _assert_not_redirected(staging, "staged intake directory")
        # The single publishing step. Before it nothing is visible to the
        # index; after it the intake is complete.
        os.rename(staging, final)
    except OSError as exc:
        _discard_staging(staging)
        raise ChartInboxStorageError(
            f"could not write the chart intake record: {exc}") from exc
    except BaseException:
        # Including a non-OSError failure mid-publish: still leave nothing.
        _discard_staging(staging)
        raise


def _discard_staging(staging: Path) -> None:
    """Remove exactly the staging directory this call created, and nothing else."""
    try:
        shutil.rmtree(staging, ignore_errors=True)
    except Exception:  # pragma: no cover - rmtree already ignores errors
        pass


def ingest(
    inbox_root: Path | str,
    data: bytes,
    *,
    display_filename: object = None,
    declared_ticker: object = None,
    declared_timeframe: object = None,
    allowed_tickers: frozenset[str] | None = None,
    allowed_timeframes: frozenset[str] | None = None,
    now: datetime | None = None,
    max_bytes: int = MAX_UPLOAD_BYTES,
) -> dict:
    """Validate, quarantine and record one owner-supplied chart image.

    Raises ``ChartIntakeRejected`` (nothing written) or
    ``ChartInboxStorageError`` (nothing usable written). On success returns the
    persisted record. The returned record's ``state`` is ``quarantined_unreviewed``
    for new content, or ``duplicate`` when identical bytes are already stored —
    a duplicate is recorded for visibility but stores no second copy of the image.
    """
    if not data:
        raise ChartIntakeRejected("empty_payload", "The uploaded file was empty.")
    if len(data) > max_bytes:
        raise ChartIntakeRejected(
            "payload_too_large",
            f"The upload is {len(data):,} bytes; the limit is {max_bytes:,} bytes.",
        )

    # Verify the WHOLE byte stream, not just its opening fields. A payload that
    # merely starts like an image, or carries a dimension header with no usable
    # image behind it, is not evidence a reviewer could ever open.
    try:
        media_type, width, height = image_integrity.verify_complete_image(data)
    except image_integrity.ImageIntegrityError as failure:
        if failure.reason == "unsupported_media_type":
            # Carry the verifier's own wording rather than a generic line: it
            # distinguishes "those bytes are not an image at all" from "those
            # bytes are a JPEG", and an owner holding a perfectly sound JPEG
            # needs to be told to convert it, not that it is damaged.
            raise ChartIntakeRejected(
                "unsupported_media_type",
                f"Not accepted: {failure.detail}.",
            ) from failure
        raise ChartIntakeRejected(
            "corrupt_or_unreadable_image",
            f"The file is not a complete, readable image: {failure.detail}.",
        ) from failure

    # Validate the declared context BEFORE creating anything on disk.
    ticker = _validated_ticker(declared_ticker, allowed_tickers)
    timeframe = _validated_timeframe(declared_timeframe, allowed_timeframes)

    content_sha256 = hashlib.sha256(data).hexdigest()
    safe_display, display_modified = sanitize_display_filename(display_filename)
    declared_ext = safe_display.rsplit(".", 1)[-1].lower() if "." in safe_display else ""
    extension_mismatch = bool(declared_ext) and declared_ext not in \
        _EXTENSIONS_MATCHING_MEDIA_TYPE[media_type]

    received_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    intake_id = new_intake_id(received_at)
    existing = find_by_content_hash(inbox_root, content_sha256)

    stored_extension = _EXTENSION_FOR_MEDIA_TYPE[media_type]
    stored_filename = f"original.{stored_extension}" if existing is None else None

    record = {
        "schema_version": SCHEMA_VERSION,
        "intake_id": intake_id,
        "state": STATE_DUPLICATE if existing is not None else STATE_QUARANTINED,
        "received_at": received_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content_sha256": content_sha256,
        "byte_size": len(data),
        "media_type": media_type,
        "image_width": width,
        "image_height": height,
        "stored_filename": stored_filename,
        "stored_relpath": (
            None if stored_filename is None
            else f"{CHARTS_DIRNAME}/{intake_id}/{stored_filename}"
        ),
        "display_filename": safe_display,
        "display_filename_sanitized": display_modified,
        "declared_extension_matches_content": not extension_mismatch,
        "declared_ticker": ticker,
        "declared_timeframe": timeframe,
        "declared_context_source": (
            "owner_form_selection_validated_against_accepted_roster"
            if (ticker or timeframe) else None
        ),
        "duplicate_of": None if existing is None else existing.get("intake_id"),
        "review": {
            "reviewed": False,
            "decision": None,
            "decided_at": None,
            "reviewer": None,
        },
        # Explicit, machine-checkable statement of what receipt does NOT do.
        # Nothing in this repository reads these as permission; they exist so
        # the stored record itself carries the boundary it was created under.
        "influence": {
            "influences_recommendations": False,
            "changes_portfolio_membership": False,
            "changes_level1_or_level2_targets": False,
            "changes_policy_or_caps_or_clusters": False,
            "changes_margin_doctrine": False,
            "changes_holdings": False,
            "arms_or_executes_stage1": False,
            "creates_order_or_trade": False,
        },
        "note": (
            "Evidence receipt only. This image is quarantined as unreviewed and "
            "untrusted. It has not been interpreted, accepted as evidence, or "
            "allowed to affect any recommendation, target, holding or policy."
        ),
    }

    _publish_intake(inbox_root, intake_id, record,
                    image=data if stored_filename is not None else None,
                    stored_filename=stored_filename)
    return record


def read_image_bytes(inbox_root: Path | str, intake_id: str) -> tuple[bytes, str] | None:
    """Retained bytes plus media type for one quarantined intake.

    Returns ``None`` when the id is unknown, malformed, or refers to a
    duplicate marker (which holds no bytes of its own). The path is rebuilt
    from the validated id and the record's own fixed filename constant; the
    stored record can never redirect a read outside the inbox.
    """
    if not _INTAKE_ID_RE.match(intake_id or ""):
        return None
    charts = _charts_root_for_read(inbox_root)
    if charts is None:
        return None
    directory = charts / intake_id
    try:
        record = json.loads((directory / RECORD_FILENAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or record.get("state") != STATE_QUARANTINED:
        return None
    media_type = record.get("media_type")
    if media_type not in SUPPORTED_MEDIA_TYPES:
        return None
    filename = f"original.{_EXTENSION_FOR_MEDIA_TYPE[media_type]}"
    try:
        return (directory / filename).read_bytes(), media_type
    except OSError:
        return None


def inbox_summary(inbox_root: Path | str) -> dict:
    """Counts the owner interface shows without loading every record twice."""
    records = list_records(inbox_root)
    return {
        "total": len(records),
        "quarantined": sum(1 for r in records if r.get("state") == STATE_QUARANTINED),
        "duplicates": sum(1 for r in records if r.get("state") == STATE_DUPLICATE),
        "reviewed": sum(1 for r in records
                        if isinstance(r.get("review"), dict) and r["review"].get("reviewed")),
        "latest_received_at": records[0].get("received_at") if records else None,
    }
