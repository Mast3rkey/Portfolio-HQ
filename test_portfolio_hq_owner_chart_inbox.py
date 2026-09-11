"""Focused, adversarial tests for the owner chart inbox.

Covers the intake trust boundary directly, without HTTP: format sniffing that
ignores the client's filename, bounded size, corruption detection, path
traversal, server-generated storage identity, overwrite refusal, duplicate
detection, metadata integrity, storage failure, and the standing guarantee that
receiving a chart adopts nothing.
"""

from __future__ import annotations

import base64
import hashlib
import json
import struct
import zlib
from datetime import datetime, timezone
from pathlib import Path

import pytest

from portfolio_hq.owner import chart_inbox as inbox_mod

FIXED_NOW = datetime(2026, 9, 10, 12, 0, 0, tzinfo=timezone.utc)
ALLOWED_TICKERS = frozenset({"NVDA", "MSFT", "BTC"})
ALLOWED_TIMEFRAMES = frozenset({"1D"})


# ── image builders (no third-party imaging dependency) ───────────────────────

def png_bytes(width: int = 40, height: int = 24) -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        payload = tag + data
        return (struct.pack(">I", len(data)) + payload
                + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF))

    scanlines = b"".join(
        b"\x00" + bytes([(x * 7 + y * 3) % 256 for x in range(width * 3)])
        for y in range(height)
    )
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(scanlines))
            + chunk(b"IEND", b""))


#: A real, complete, decodable 32x18 JPEG, embedded so the positive fixture is
#: an actual image rather than a hand-assembled header.
#:
#: The previous fixture built SOI + APP0 + SOF0 + EOI — a frame header with no
#: scan and no image data at all. It passed only because validation stopped at
#: the first dimensions marker, and a positive fixture that is not a real image
#: cannot demonstrate that real images are accepted. Pillow refuses it outright
#: ("cannot identify image file"); ``header_only_jpeg_bytes`` below keeps it as
#: a *negative* fixture, which is the only honest use for it.
_REAL_JPEG_32x18_B64 = (
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQY"
    "GBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYa"
    "KCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAAR"
    "CAASACADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAA"
    "AgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkK"
    "FhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWG"
    "h4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl"
    "5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREA"
    "AgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYk"
    "NOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOE"
    "hYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk"
    "5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDwyx8PdPk/SuhsfD/T5P0rvrHw90+T9K6G"
    "x8P9Pk/SjDYk8fLeIdtTgbHw90+T9K6Gx8P9Pk/Su+sfD/T5K249GS3jDMmSei+teyswp4am"
    "61aVordn6DlnEDbSTMKxVePlH5V0Niq8fKPyoor5XDH8+Zb0OhsUXj5R+VSSgG9bIHGAPyoo"
    "ry+Mf+Rav8S/Jn6Tkfxo/9k="
)
REAL_JPEG_SIZE = (32, 18)


def jpeg_bytes() -> bytes:
    """A complete, decodable JPEG of size ``REAL_JPEG_SIZE``."""
    return base64.b64decode("".join(_REAL_JPEG_32x18_B64))


def header_only_jpeg_bytes(width: int = 32, height: int = 18) -> bytes:
    """SOI + APP0 + SOF0 + EOI: dimensions, but no scan and no image data.

    The frame header's own component records are deliberately *valid* — three
    components, legal sampling factors, legal table slots — so that the only
    thing wrong with this payload is the missing scan. An earlier version
    zero-filled them, which meant the frame header was independently malformed
    and the missing scan was never the reason it was refused.

    A JPEG segment length counts the two length bytes plus the payload:
    2 + len("JFIF\\0") + 11 = 18. This must be REJECTED — it is a header, not
    an image.
    """
    app0 = b"\xff\xe0" + struct.pack(">H", 18) + b"JFIF\x00" + bytes(11)
    components = bytes([1, 0x11, 0, 2, 0x11, 0, 3, 0x11, 0])
    sof0 = (b"\xff\xc0" + struct.pack(">H", 17) + b"\x08"
            + struct.pack(">HH", height, width) + b"\x03" + components)
    return b"\xff\xd8" + app0 + sof0 + b"\xff\xd9"


@pytest.fixture
def inbox(tmp_path: Path) -> Path:
    return tmp_path / "inbox"


def _ingest(root: Path, data: bytes, **kwargs):
    kwargs.setdefault("allowed_tickers", ALLOWED_TICKERS)
    kwargs.setdefault("allowed_timeframes", ALLOWED_TIMEFRAMES)
    kwargs.setdefault("now", FIXED_NOW)
    return inbox_mod.ingest(root, data, **kwargs)


# ── happy path and metadata integrity ────────────────────────────────────────

def test_happy_path_quarantines_and_retains_bytes_exactly(inbox: Path):
    data = png_bytes()
    record = _ingest(inbox, data, display_filename="NVDA daily.png",
                     declared_ticker="NVDA", declared_timeframe="1D")

    assert record["state"] == inbox_mod.STATE_QUARANTINED
    assert record["content_sha256"] == hashlib.sha256(data).hexdigest()
    assert record["byte_size"] == len(data)
    assert record["media_type"] == "image/png"
    assert (record["image_width"], record["image_height"]) == (40, 24)
    assert record["declared_ticker"] == "NVDA"
    assert record["declared_timeframe"] == "1D"
    assert record["duplicate_of"] is None

    stored = inbox / record["stored_relpath"]
    assert stored.read_bytes() == data, "retained bytes must be byte-identical"


def test_record_is_persisted_as_readable_json_and_listed(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="a.png")
    on_disk = json.loads(
        (inbox / "charts" / record["intake_id"] / "intake.json").read_text()
    )
    assert on_disk == record
    listed = inbox_mod.list_records(inbox)
    assert [r["intake_id"] for r in listed] == [record["intake_id"]]


def test_intake_is_never_reviewed_or_influential_at_receipt(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="a.png")
    assert record["review"] == {
        "reviewed": False, "decision": None, "decided_at": None, "reviewer": None,
    }
    # Every influence assertion must be False: receipt adopts nothing.
    assert record["influence"] and all(v is False for v in record["influence"].values())
    for key in ("influences_recommendations", "changes_level1_or_level2_targets",
                "changes_policy_or_caps_or_clusters", "changes_holdings",
                "arms_or_executes_stage1", "creates_order_or_trade"):
        assert record["influence"][key] is False


def test_persisted_states_are_a_closed_vocabulary(inbox: Path):
    data = png_bytes()
    first = _ingest(inbox, data, display_filename="a.png")
    second = _ingest(inbox, data, display_filename="a.png")
    for record in (first, second):
        assert record["state"] in inbox_mod.INTAKE_STATES


def test_inbox_summary_counts(inbox: Path):
    data = png_bytes()
    _ingest(inbox, data, display_filename="a.png")
    _ingest(inbox, data, display_filename="a.png")          # duplicate
    _ingest(inbox, png_bytes(11, 9), display_filename="b.png")
    summary = inbox_mod.inbox_summary(inbox)
    assert summary["total"] == 3
    assert summary["quarantined"] == 2
    assert summary["duplicates"] == 1
    assert summary["reviewed"] == 0


def test_missing_inbox_lists_empty_rather_than_raising(tmp_path: Path):
    assert inbox_mod.list_records(tmp_path / "absent") == []
    assert inbox_mod.inbox_summary(tmp_path / "absent")["total"] == 0


# ── format handling: content decides, never the filename ────────────────────

def test_jpeg_is_accepted_with_real_dimensions(inbox: Path):
    record = _ingest(inbox, jpeg_bytes(), display_filename="shot.jpg")
    assert record["media_type"] == "image/jpeg"
    assert (record["image_width"], record["image_height"]) == REAL_JPEG_SIZE
    assert record["stored_relpath"].endswith("original.jpg")


@pytest.mark.parametrize("payload", [
    b"GIF89a" + b"\x00" * 32,                       # GIF
    b"RIFF\x24\x00\x00\x00WEBPVP8 " + b"\x00" * 16,  # WebP
    b"%PDF-1.7\n" + b"\x00" * 32,                   # PDF
    b"<svg xmlns='http://www.w3.org/2000/svg'></svg>",
    b"PK\x03\x04" + b"\x00" * 32,                   # zip
    b"#!/bin/sh\nrm -rf /\n",                       # script
])
def test_unsupported_formats_are_refused(inbox: Path, payload: bytes):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, payload, display_filename="chart.png")
    assert excinfo.value.reason == "unsupported_media_type"
    assert not (inbox / "charts").exists(), "a rejection must write nothing"


def test_extension_is_never_trusted_to_decide_the_media_type(inbox: Path):
    """A JPEG named .png is stored as a JPEG, and the mismatch is recorded."""
    record = _ingest(inbox, jpeg_bytes(), display_filename="totally-a.png")
    assert record["media_type"] == "image/jpeg"
    assert record["stored_relpath"].endswith("original.jpg")
    assert record["declared_extension_matches_content"] is False
    assert (inbox / record["stored_relpath"]).read_bytes() == jpeg_bytes()


def test_matching_extension_is_reported_as_matching(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="chart.PNG")
    assert record["declared_extension_matches_content"] is True


def test_executable_disguised_as_png_extension_is_still_refused(inbox: Path):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, b"MZ\x90\x00" + b"\x00" * 64, display_filename="chart.png")
    assert excinfo.value.reason == "unsupported_media_type"


def test_sniffer_ignores_everything_but_leading_bytes():
    assert inbox_mod.sniff_media_type(png_bytes()) == "image/png"
    assert inbox_mod.sniff_media_type(jpeg_bytes()) == "image/jpeg"
    assert inbox_mod.sniff_media_type(b"\x89PNG") is None  # truncated magic
    assert inbox_mod.sniff_media_type(b"") is None


# ── size and corruption bounds ───────────────────────────────────────────────

def test_empty_payload_is_refused(inbox: Path):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, b"", display_filename="empty.png")
    assert excinfo.value.reason == "empty_payload"
    assert not (inbox / "charts").exists()


def test_oversized_payload_is_refused_before_any_write(inbox: Path):
    data = png_bytes(64, 64)
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, data, display_filename="big.png", max_bytes=len(data) - 1)
    assert excinfo.value.reason == "payload_too_large"
    assert not (inbox / "charts").exists()


def test_payload_exactly_at_the_limit_is_accepted(inbox: Path):
    data = png_bytes()
    record = _ingest(inbox, data, display_filename="edge.png", max_bytes=len(data))
    assert record["state"] == inbox_mod.STATE_QUARANTINED


def test_default_ceiling_is_bounded_and_declared():
    assert 0 < inbox_mod.MAX_UPLOAD_BYTES <= 64 * 1024 * 1024


@pytest.mark.parametrize("payload,label", [
    (b"\x89PNG\r\n\x1a\n" + b"\x00" * 8, "png header without IHDR"),
    (b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR"
     + struct.pack(">IIBBBBB", 0, 0, 8, 2, 0, 0, 0), "png with zero dimensions"),
    (b"\xff\xd8\xff", "jpeg magic only"),
    (b"\xff\xd8" + b"\xff\xc0" + struct.pack(">H", 17) + b"\x08"
     + struct.pack(">HH", 0, 0) + b"\x03" + bytes(9), "jpeg with zero dimensions"),
    (b"\xff\xd8" + b"\xff\xc0" + struct.pack(">H", 900), "jpeg truncated segment"),
])
def test_corrupt_or_truncated_images_are_refused(inbox: Path, payload: bytes, label: str):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, payload, display_filename="broken.png")
    assert excinfo.value.reason == "corrupt_or_unreadable_image", label
    assert not (inbox / "charts").exists()


def test_a_jpeg_advertising_a_size_with_no_usable_scan_is_refused(inbox: Path):
    """The shape that reached storage before: a frame header exposing
    dimensions, an empty scan header, one entropy byte and an EOI. It walks
    like a JPEG and no decoder can open it."""
    frame = b"\xff\xc0" + struct.pack(">H", 7) + b"\x08" + struct.pack(">HH", 18, 32)
    payload = (b"\xff\xd8" + frame + b"\xff\xda" + struct.pack(">H", 2)
               + b"\x42\xff\xd9")
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, payload, display_filename="chart.jpg")
    assert excinfo.value.reason == "corrupt_or_unreadable_image"
    assert not (inbox / "charts").exists()


def test_a_legal_but_unsupported_jpeg_variant_is_refused_as_unsupported(inbox: Path):
    """Arithmetic-coded JPEG is valid and unreadable by common decoders. The
    owner is told it is the wrong *variant*, not that their file is damaged."""
    def segment(marker: int, body: bytes) -> bytes:
        return bytes((0xFF, marker)) + struct.pack(">H", len(body) + 2) + body

    quantisation = segment(0xDB, b"\x00" + bytes(64))
    huffman = segment(0xC4, b"\x00" + bytes([1] + [0] * 15) + b"\x00")
    # 0xFFC9 is SOF9: arithmetic-coded extended sequential.
    frame = segment(0xC9, b"\x08" + struct.pack(">HH", 18, 32) + b"\x01"
                    + bytes([1, 0x11, 0]))
    scan = segment(0xDA, b"\x01" + bytes([1, 0x00]) + bytes([0, 63, 0]))
    payload = (b"\xff\xd8" + quantisation + huffman + frame + scan
               + b"\x42\xff\xd9")
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, payload, display_filename="chart.jpg")
    assert excinfo.value.reason == "unsupported_media_type"
    assert "arithmetic" in str(excinfo.value)
    assert not (inbox / "charts").exists()


def test_truncated_real_png_is_refused(inbox: Path):
    with pytest.raises(inbox_mod.ChartIntakeRejected):
        _ingest(inbox, png_bytes()[:20], display_filename="cut.png")


# ── filename handling and path safety ────────────────────────────────────────

@pytest.mark.parametrize("hostile", [
    "../../../../etc/passwd",
    "..\\..\\windows\\system32\\config\\sam",
    "/etc/shadow",
    "C:\\Users\\owner\\secret.png",
    "....//....//escape.png",
    "chart.png\x00.sh",
    "chart\n\rinjected.png",
    "." * 300 + ".png",
])
def test_hostile_filenames_never_reach_the_filesystem(inbox: Path, hostile: str):
    record = _ingest(inbox, png_bytes(), display_filename=hostile)

    stored = inbox / record["stored_relpath"]
    charts_root = (inbox / "charts").resolve()
    assert charts_root in stored.resolve().parents, "storage escaped the inbox"
    assert stored.is_file() and stored.read_bytes() == png_bytes()
    # The stored name is a fixed constant; the hostile text survives only as
    # sanitised display metadata.
    assert stored.name == "original.png"
    assert record["display_filename_sanitized"] is True
    for banned in ("/", "\\", "\x00", "\n", "\r"):
        assert banned not in record["display_filename"]
    assert ".." not in record["display_filename"]


def test_only_files_created_are_inside_the_inbox(inbox: Path, tmp_path: Path):
    before = {p for p in tmp_path.rglob("*")}
    _ingest(inbox, png_bytes(), display_filename="../../escape.png")
    created = {p for p in tmp_path.rglob("*")} - before
    assert created, "nothing was created at all"
    for path in created:
        assert inbox in path.parents or path == inbox


def test_sanitize_display_filename_is_pure_and_bounded():
    safe, changed = inbox_mod.sanitize_display_filename("../../evil.png")
    assert changed is True and "/" not in safe and ".." not in safe
    unchanged, changed2 = inbox_mod.sanitize_display_filename("NVDA daily.png")
    assert unchanged == "NVDA daily.png" and changed2 is False
    blank, _ = inbox_mod.sanitize_display_filename("")
    assert blank == "(unnamed upload)"
    long_name, _ = inbox_mod.sanitize_display_filename("z" * 500 + ".png")
    assert len(long_name) <= 128
    none_name, _ = inbox_mod.sanitize_display_filename(None)
    assert none_name == "(unnamed upload)"


def test_generated_storage_identity_is_server_side_and_opaque(inbox: Path):
    first = _ingest(inbox, png_bytes(1, 1), display_filename="alpha.png")
    second = _ingest(inbox, png_bytes(2, 2), display_filename="alpha.png")
    for record in (first, second):
        assert inbox_mod._INTAKE_ID_RE.match(record["intake_id"])
        assert "alpha" not in record["intake_id"]
    assert first["intake_id"] != second["intake_id"], "ids must not collide"


def test_record_dir_refuses_a_forged_intake_id(inbox: Path):
    for forged in ("../escape", "..", "", "20260910T120000Z-nothex!!", "/abs"):
        with pytest.raises(ValueError):
            inbox_mod._record_dir(inbox, forged)


def test_list_records_ignores_foreign_directories(inbox: Path):
    _ingest(inbox, png_bytes(), display_filename="a.png")
    junk = inbox / "charts" / "not-an-intake-id"
    junk.mkdir(parents=True)
    (junk / "intake.json").write_text('{"intake_id": "smuggled"}')
    ids = {r["intake_id"] for r in inbox_mod.list_records(inbox)}
    assert "smuggled" not in ids and len(ids) == 1


def test_list_records_skips_unparseable_records(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="a.png")
    (inbox / "charts" / record["intake_id"] / "intake.json").write_text("{not json")
    assert inbox_mod.list_records(inbox) == []


# ── duplicates and overwrite refusal ─────────────────────────────────────────

def test_identical_content_is_recorded_as_a_duplicate_without_a_second_copy(inbox: Path):
    data = png_bytes()
    first = _ingest(inbox, data, display_filename="one.png")
    second = _ingest(inbox, data, display_filename="two.png")

    assert second["state"] == inbox_mod.STATE_DUPLICATE
    assert second["duplicate_of"] == first["intake_id"]
    assert second["stored_relpath"] is None and second["stored_filename"] is None
    stored = list((inbox / "charts").rglob("original.*"))
    assert len(stored) == 1, "duplicate must not store the bytes again"
    assert stored[0].read_bytes() == data


def test_a_third_identical_upload_points_at_the_original_not_a_duplicate(inbox: Path):
    data = png_bytes()
    first = _ingest(inbox, data, display_filename="one.png")
    _ingest(inbox, data, display_filename="two.png")
    third = _ingest(inbox, data, display_filename="three.png")
    assert third["duplicate_of"] == first["intake_id"]


def test_different_content_is_not_a_duplicate(inbox: Path):
    _ingest(inbox, png_bytes(4, 4), display_filename="a.png")
    other = _ingest(inbox, png_bytes(5, 5), display_filename="b.png")
    assert other["state"] == inbox_mod.STATE_QUARANTINED
    assert other["duplicate_of"] is None


def test_colliding_intake_id_refuses_to_overwrite(inbox: Path, monkeypatch):
    """A duplicate storage identity must fail loudly, never silently replace."""
    monkeypatch.setattr(inbox_mod, "new_intake_id",
                        lambda now=None: "20260910T120000Z-abcdef123456")
    original = png_bytes(6, 6)
    first = _ingest(inbox, original, display_filename="first.png")
    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(7, 7), display_filename="second.png")
    # The first record survives untouched.
    assert (inbox / first["stored_relpath"]).read_bytes() == original
    assert len(inbox_mod.list_records(inbox)) == 1


def test_a_preexisting_intake_directory_is_never_written_into(inbox: Path, monkeypatch):
    """The directory guard is tested on its own, not only via the file guard.

    Storage protection is layered: the record directory is created with
    ``exist_ok=False`` and the files inside are opened ``O_EXCL``. Because the
    file guard alone would catch a collision where an image already exists,
    this covers the case it cannot — an intake directory that exists but is
    empty, which a permissive ``mkdir`` would happily adopt and write into.
    """
    intake_id = "20260910T120000Z-0f1e2d3c4b5a"
    monkeypatch.setattr(inbox_mod, "new_intake_id", lambda now=None: intake_id)
    squatted = inbox / "charts" / intake_id
    squatted.mkdir(parents=True)

    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(), display_filename="a.png")

    assert list(squatted.iterdir()) == [], "the inbox wrote into a directory it did not create"
    assert inbox_mod.list_records(inbox) == []


def test_existing_image_file_is_never_overwritten(inbox: Path, monkeypatch):
    monkeypatch.setattr(inbox_mod, "new_intake_id",
                        lambda now=None: "20260910T120000Z-0123456789ab")
    _ingest(inbox, png_bytes(6, 6), display_filename="first.png")
    directory = inbox / "charts" / "20260910T120000Z-0123456789ab"
    sentinel = (directory / "original.png").read_bytes()
    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(9, 9), display_filename="again.png")
    assert (directory / "original.png").read_bytes() == sentinel


# ── a failed intake publishes nothing (transactional storage) ───────────────

def _assert_nothing_partial_anywhere(inbox: Path, expected_ids: list[str]) -> None:
    """No orphan bytes, no abandoned directory, no staged remnant — anywhere.

    Checked across the WHOLE inbox, not just ``charts/``: a leaked staging tree
    is exactly as much of an orphan as a leaked intake directory, and only
    looking where the index looks would miss it.
    """
    charts = inbox / "charts"
    intake_dirs = sorted(d.name for d in charts.iterdir()
                         if d.is_dir() and inbox_mod._INTAKE_ID_RE.match(d.name))
    assert intake_dirs == sorted(expected_ids), "an abandoned intake directory remains"

    images = sorted(path.relative_to(inbox).as_posix()
                    for path in inbox.rglob("original.*"))
    expected_images = sorted(f"charts/{i}/original.png" for i in expected_ids)
    assert images == expected_images, "orphaned image bytes remain"

    staging = inbox / inbox_mod.STAGING_DIRNAME
    if staging.exists():
        assert list(staging.iterdir()) == [], "a staged intake was abandoned"

    for record_file in inbox.rglob(inbox_mod.RECORD_FILENAME):
        json.loads(record_file.read_text())  # no partial/unparseable record


def _fail_writing(filename: str):
    """An ``open`` replacement that fails only for one filename."""
    real_open = open

    def guarded(file, mode="r", *args, **kwargs):
        if str(file).endswith(filename) and any(f in mode for f in "wax+"):
            raise OSError(28, "No space left on device")
        return real_open(file, mode, *args, **kwargs)

    return guarded


def test_failure_after_the_image_is_written_leaves_nothing_behind(inbox: Path,
                                                                  monkeypatch):
    """The exact regression: the record write fails once the bytes are on disk.

    Previously the directory and ``original.png`` survived the failure, so the
    owner was told the chart was NOT received while its bytes stayed on the
    volume — invisible to ``list_records`` and ambiguous for future duplicate
    detection. A failed intake must publish nothing at all.
    """
    # An existing, successful intake that must survive the failure untouched.
    survivor = _ingest(inbox, png_bytes(11, 7), display_filename="keep.png")
    survivor_bytes = (inbox / survivor["stored_relpath"]).read_bytes()

    monkeypatch.setattr("builtins.open", _fail_writing("intake.json"))
    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(40, 24), display_filename="doomed.png")
    monkeypatch.undo()

    _assert_nothing_partial_anywhere(inbox, [survivor["intake_id"]])
    assert (inbox / survivor["stored_relpath"]).read_bytes() == survivor_bytes
    assert [r["intake_id"] for r in inbox_mod.list_records(inbox)] == \
        [survivor["intake_id"]]

    # A later clean retry behaves completely normally.
    retry = _ingest(inbox, png_bytes(40, 24), display_filename="retry.png")
    assert retry["state"] == inbox_mod.STATE_QUARANTINED
    assert (inbox / retry["stored_relpath"]).read_bytes() == png_bytes(40, 24)
    assert len(inbox_mod.list_records(inbox)) == 2


def test_failure_while_publishing_leaves_nothing_behind(inbox: Path, monkeypatch):
    """Failure at the single publishing step must also leave no trace."""
    survivor = _ingest(inbox, png_bytes(9, 5), display_filename="keep.png")

    def refuse(*args, **kwargs):
        raise OSError(5, "Input/output error")

    monkeypatch.setattr(inbox_mod.os, "rename", refuse)
    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(40, 24), display_filename="doomed.png")
    monkeypatch.undo()

    assert [r["intake_id"] for r in inbox_mod.list_records(inbox)] == \
        [survivor["intake_id"]]
    _assert_nothing_partial_anywhere(inbox, [survivor["intake_id"]])


def test_failure_writing_the_image_leaves_nothing_behind(inbox: Path, monkeypatch):
    monkeypatch.setattr("builtins.open", _fail_writing("original.png"))
    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(), display_filename="doomed.png")
    monkeypatch.undo()
    assert inbox_mod.list_records(inbox) == []
    _assert_nothing_partial_anywhere(inbox, [])


def test_an_in_flight_intake_is_invisible_to_the_index(inbox: Path):
    """Staging must not sit where the filesystem index looks."""
    _ingest(inbox, png_bytes(), display_filename="a.png")
    staging = inbox / inbox_mod.STAGING_DIRNAME
    charts = inbox / "charts"
    assert inbox_mod.STAGING_DIRNAME != "charts"
    assert staging.resolve().parent == charts.resolve().parent
    # Even a leftover staged tree cannot be listed as a record.
    forged = staging / "20260911T120000Z-abcdef123456.deadbeefcafe"
    forged.mkdir(parents=True, exist_ok=True)
    (forged / inbox_mod.RECORD_FILENAME).write_text('{"intake_id": "smuggled"}')
    assert "smuggled" not in {r.get("intake_id") for r in inbox_mod.list_records(inbox)}


# ── the storage boundary is containment-safe (no symlink redirection) ───────

def test_a_symlinked_charts_root_is_refused_and_writes_nothing_outside(tmp_path: Path):
    """``mkdir`` and ``open`` follow a symlinked parent.

    With ``charts`` pointing elsewhere, the generated intake directory, the
    image and the record were all created outside the configured inbox — while
    the stored record still claimed an inbox-relative path.
    """
    inbox = tmp_path / "inbox"
    outside = tmp_path / "outside"
    inbox.mkdir()
    outside.mkdir()
    (inbox / "charts").symlink_to(outside, target_is_directory=True)

    with pytest.raises(inbox_mod.ChartInboxStorageError) as excinfo:
        _ingest(inbox, png_bytes(), display_filename="a.png")
    assert "symbolic link" in str(excinfo.value)

    assert list(outside.rglob("*")) == [], "bytes were written outside the inbox"
    assert inbox_mod.list_records(inbox) == [], "a redirected inbox must not list"


def test_a_symlinked_charts_root_fails_closed_on_every_read_path(tmp_path: Path):
    inbox = tmp_path / "inbox"
    outside = tmp_path / "outside"
    inbox.mkdir()
    outside.mkdir()
    (inbox / "charts").symlink_to(outside, target_is_directory=True)

    assert inbox_mod.list_records(inbox) == []
    assert inbox_mod.inbox_summary(inbox)["total"] == 0
    assert inbox_mod.find_by_content_hash(inbox, "0" * 64) is None
    assert inbox_mod.read_image_bytes(inbox, "20260911T120000Z-abcdef123456") is None


def test_a_symlink_planted_after_the_fact_is_still_refused(tmp_path: Path):
    inbox = tmp_path / "inbox"
    outside = tmp_path / "outside"
    inbox.mkdir()
    outside.mkdir()
    first = _ingest(inbox, png_bytes(12, 8), display_filename="a.png")
    assert first["state"] == inbox_mod.STATE_QUARANTINED

    # Replace the real charts directory with a redirection.
    genuine = inbox / "charts"
    genuine.rename(tmp_path / "real_charts")
    genuine.symlink_to(outside, target_is_directory=True)

    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(40, 24), display_filename="b.png")
    assert list(outside.rglob("*")) == []


def test_a_symlinked_inbox_root_is_legitimate_and_still_works(tmp_path: Path):
    """An operator may point the inbox at a mounted volume through a symlink.

    Only redirection *beneath* the resolved root is refused; the root itself is
    resolved and treated as authoritative.
    """
    real = tmp_path / "volume"
    real.mkdir()
    link = tmp_path / "inbox-link"
    link.symlink_to(real, target_is_directory=True)

    record = _ingest(link, png_bytes(), display_filename="a.png")
    assert record["state"] == inbox_mod.STATE_QUARANTINED
    assert (real / record["stored_relpath"]).read_bytes() == png_bytes()
    assert len(inbox_mod.list_records(link)) == 1
    assert inbox_mod.read_image_bytes(link, record["intake_id"])[0] == png_bytes()


def test_ordinary_storage_is_unaffected_by_the_containment_checks(inbox: Path):
    record = _ingest(inbox, png_bytes(33, 21), display_filename="normal.png")
    stored = inbox / record["stored_relpath"]
    assert stored.is_file()
    assert not stored.is_symlink()
    assert not stored.parent.is_symlink()
    assert stored.resolve() == stored
    assert (inbox / "charts").resolve() == (inbox / "charts")


# ── declared context: only through an explicit, validated mechanism ─────────

def test_ticker_outside_the_accepted_list_is_refused(inbox: Path):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, png_bytes(), display_filename="a.png", declared_ticker="ENRON")
    assert excinfo.value.reason == "invalid_ticker"
    assert not (inbox / "charts").exists()


def test_malformed_ticker_is_refused(inbox: Path):
    for hostile in ("<script>", "NVDA;DROP", "N" * 40, "../NVDA"):
        with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
            _ingest(inbox, png_bytes(), display_filename="a.png",
                    declared_ticker=hostile)
        assert excinfo.value.reason == "invalid_ticker"


def test_ticker_is_refused_when_no_accepted_list_is_available(inbox: Path):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        inbox_mod.ingest(inbox, png_bytes(), display_filename="a.png",
                         declared_ticker="NVDA", allowed_tickers=None,
                         allowed_timeframes=None, now=FIXED_NOW)
    assert excinfo.value.reason == "invalid_ticker"


def test_unknown_timeframe_is_refused(inbox: Path):
    with pytest.raises(inbox_mod.ChartIntakeRejected) as excinfo:
        _ingest(inbox, png_bytes(), display_filename="a.png", declared_timeframe="7m")
    assert excinfo.value.reason == "invalid_timeframe"


def test_context_is_optional_and_never_guessed_from_the_filename(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="NVDA__2026-08-01__1D.png")
    assert record["declared_ticker"] is None
    assert record["declared_timeframe"] is None
    assert record["declared_context_source"] is None


def test_supplied_context_records_its_trustworthy_source(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="a.png",
                     declared_ticker="btc", declared_timeframe="1D")
    assert record["declared_ticker"] == "BTC", "tickers normalise to upper case"
    assert record["declared_context_source"] == \
        "owner_form_selection_validated_against_accepted_roster"


# ── storage failure ──────────────────────────────────────────────────────────

def test_storage_failure_is_reported_not_swallowed(inbox: Path):
    # A regular file where the charts directory belongs: mkdir cannot succeed,
    # deterministically and regardless of the running uid.
    inbox.mkdir(parents=True)
    (inbox / "charts").write_text("not a directory")
    with pytest.raises(inbox_mod.ChartInboxStorageError):
        _ingest(inbox, png_bytes(), display_filename="a.png")


def test_missing_storage_directory_is_created_on_demand(inbox: Path):
    assert not inbox.exists()
    record = _ingest(inbox, png_bytes(), display_filename="a.png")
    assert (inbox / record["stored_relpath"]).is_file()


def test_unreadable_inbox_root_is_not_a_crash(tmp_path: Path):
    target = tmp_path / "file-not-a-dir"
    target.write_text("x")
    assert inbox_mod.list_records(target) == []


# ── reviewer handoff ─────────────────────────────────────────────────────────

def test_retained_image_can_be_read_back_for_review(inbox: Path):
    data = png_bytes()
    record = _ingest(inbox, data, display_filename="a.png")
    found = inbox_mod.read_image_bytes(inbox, record["intake_id"])
    assert found == (data, "image/png")


def test_read_image_bytes_refuses_forged_or_unknown_references(inbox: Path):
    _ingest(inbox, png_bytes(), display_filename="a.png")
    for forged in ("../../etc/passwd", "..", "", "not-an-id",
                   "20260910T120000Z-000000000000"):
        assert inbox_mod.read_image_bytes(inbox, forged) is None


def test_duplicate_marker_exposes_no_bytes(inbox: Path):
    data = png_bytes()
    _ingest(inbox, data, display_filename="one.png")
    duplicate = _ingest(inbox, data, display_filename="two.png")
    assert inbox_mod.read_image_bytes(inbox, duplicate["intake_id"]) is None


def test_read_image_bytes_ignores_a_tampered_media_type(inbox: Path):
    record = _ingest(inbox, png_bytes(), display_filename="a.png")
    path = inbox / "charts" / record["intake_id"] / "intake.json"
    tampered = json.loads(path.read_text())
    tampered["media_type"] = "text/html"
    path.write_text(json.dumps(tampered))
    assert inbox_mod.read_image_bytes(inbox, record["intake_id"]) is None


# ── the inbox touches nothing else ───────────────────────────────────────────

def test_chart_inbox_imports_no_investment_code():
    import ast

    source = Path(inbox_mod.__file__).read_text()
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    forbidden = {"allocate", "alpaca_client", "margin_state", "levels", "pandas",
                 "yaml", "earnings", "crypto", "indicators"}
    assert not (imported & forbidden), f"chart inbox imported {imported & forbidden}"


def test_ingest_never_touches_repository_authority_files(inbox: Path, monkeypatch,
                                                         tmp_path: Path):
    """Prove by interception that no authoritative path is opened for writing."""
    real_open = open
    opened_for_write: list[str] = []

    def watching_open(file, mode="r", *args, **kwargs):
        if any(flag in mode for flag in ("w", "a", "x", "+")):
            opened_for_write.append(str(file))
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", watching_open)
    _ingest(inbox, png_bytes(), display_filename="a.png")

    assert opened_for_write, "the test intercepted nothing"
    inbox_resolved = str(inbox.resolve())
    for path in opened_for_write:
        assert str(Path(path).resolve()).startswith(inbox_resolved), path
        for authority in ("holdings.yaml", "targets.yaml", "gates.yaml",
                          "governance", "intelligence", "operations"):
            assert authority not in path
