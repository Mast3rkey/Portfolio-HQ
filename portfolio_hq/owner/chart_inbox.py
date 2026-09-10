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
from datetime import datetime, timezone
from pathlib import Path

# ── contract constants ───────────────────────────────────────────────────────

SCHEMA_VERSION = 1

#: Hard ceiling on a single upload. The largest image in the repository's own
#: accepted CHART-0002 cohort is ~1.8 MB; 25 MiB leaves generous headroom for a
#: high-resolution tablet screenshot while keeping the bound small enough that a
#: single request can never exhaust a small private host.
MAX_UPLOAD_BYTES = 25 * 1024 * 1024

#: Deliberately narrow. HEIC/HEIF, WebP, GIF, SVG, PDF and everything else are
#: rejected rather than silently transcoded: this unit adds no image-decoding
#: dependency, and a format we cannot verify from its own header is a format we
#: cannot honestly quarantine. The owner re-saves as PNG or JPEG instead.
SUPPORTED_MEDIA_TYPES = ("image/png", "image/jpeg")

_EXTENSION_FOR_MEDIA_TYPE = {"image/png": "png", "image/jpeg": "jpg"}
_EXTENSIONS_MATCHING_MEDIA_TYPE = {
    "image/png": frozenset({"png"}),
    "image/jpeg": frozenset({"jpg", "jpeg"}),
}

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

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sniff_media_type(data: bytes) -> str | None:
    """Return the media type implied by the payload's own leading bytes.

    ``None`` means "not a format this inbox accepts". The client's filename,
    extension and any declared Content-Type are irrelevant here by design.
    """
    if data.startswith(_PNG_MAGIC):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    return None


def _png_dimensions(data: bytes) -> tuple[int, int] | None:
    # 8-byte magic, then a length-13 'IHDR' chunk whose payload starts with
    # big-endian uint32 width and height.
    if len(data) < 33 or data[12:16] != b"IHDR":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width <= 0 or height <= 0:
        return None
    return width, height


# SOF markers carrying frame dimensions. C4 (DHT), C8 (JPG extension) and CC
# (DAC) share the 0xC0-0xCF range but are not frame headers.
_JPEG_SOF_MARKERS = frozenset(
    {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
)


def _jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    i = 2  # skip SOI
    n = len(data)
    while i + 3 < n:
        if data[i] != 0xFF:
            return None  # desynchronised marker stream — treat as corrupt
        marker = data[i + 1]
        if marker == 0xFF:  # fill byte
            i += 1
            continue
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:  # standalone
            i += 2
            continue
        if marker == 0xD9:  # EOI before any frame header
            return None
        seg_len = int.from_bytes(data[i + 2:i + 4], "big")
        if seg_len < 2 or i + 2 + seg_len > n:
            return None  # truncated segment
        if marker in _JPEG_SOF_MARKERS:
            if seg_len < 7:
                return None
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            if width <= 0 or height <= 0:
                return None
            return width, height
        i += 2 + seg_len
    return None


def image_dimensions(data: bytes, media_type: str) -> tuple[int, int] | None:
    """Parse real pixel dimensions from the payload's own header.

    ``None`` means the header is absent, truncated or self-inconsistent — i.e.
    the payload is not a usable image even though its first bytes matched a
    known magic number. This is the inbox's corruption check; it deliberately
    needs no third-party image library.
    """
    if media_type == "image/png":
        return _png_dimensions(data)
    if media_type == "image/jpeg":
        return _jpeg_dimensions(data)
    return None


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


def _record_dir(inbox_root: Path, intake_id: str) -> Path:
    if not _INTAKE_ID_RE.match(intake_id):
        raise ValueError(f"refusing to build a path from intake id {intake_id!r}")
    return Path(inbox_root) / CHARTS_DIRNAME / intake_id


# ── read side ────────────────────────────────────────────────────────────────

def list_records(inbox_root: Path | str) -> list[dict]:
    """Every readable intake record, newest first. Missing inbox → empty list.

    The filesystem is the index: there is no separate database or manifest to
    drift out of sync with what is actually stored.
    """
    charts = Path(inbox_root) / CHARTS_DIRNAME
    if not charts.is_dir():
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

    media_type = sniff_media_type(data)
    if media_type is None:
        raise ChartIntakeRejected(
            "unsupported_media_type",
            "Only PNG and JPEG chart images are accepted, decided by inspecting "
            "the file's own content. Re-save the chart as PNG or JPEG.",
        )
    dimensions = image_dimensions(data, media_type)
    if dimensions is None:
        raise ChartIntakeRejected(
            "corrupt_or_unreadable_image",
            "The file starts like an image but its size header could not be "
            "read, so it is truncated or corrupt.",
        )

    # Validate the declared context BEFORE creating anything on disk.
    ticker = _validated_ticker(declared_ticker, allowed_tickers)
    timeframe = _validated_timeframe(declared_timeframe, allowed_timeframes)

    width, height = dimensions
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

    directory = _record_dir(inbox_root, intake_id)
    try:
        # exist_ok=False: a colliding intake id must fail loudly, never
        # silently reuse or overwrite an existing record directory.
        directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise ChartInboxStorageError(
            f"intake directory already exists: {directory}"
        ) from None
    except OSError as exc:
        raise ChartInboxStorageError(
            f"could not create the chart inbox directory: {exc}"
        ) from exc

    try:
        if stored_filename is not None:
            # "xb" is O_CREAT|O_EXCL: an existing file is an error, never an
            # overwrite. The name is a fixed constant, so no client-supplied
            # text reaches the filesystem.
            with open(directory / stored_filename, "xb") as fh:
                fh.write(data)
        with open(directory / RECORD_FILENAME, "x", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2, sort_keys=True)
            fh.write("\n")
    except OSError as exc:
        raise ChartInboxStorageError(
            f"could not write the chart intake record: {exc}"
        ) from exc

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
    directory = _record_dir(inbox_root, intake_id)
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
