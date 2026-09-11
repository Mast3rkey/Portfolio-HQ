"""Adversarial tests for chart-image completeness verification.

The inbox previously accepted a payload once it could read a dimension field:
a PNG truncated immediately after IHDR, a PNG with its IEND removed, and a
JPEG that was a frame header with no scan at all were all stored as valid chart
evidence. These tests pin the boundary at *complete image*, not *parsable
header*, and cross-check the verdicts against a real decoder.
"""

from __future__ import annotations

import io
import struct
import zlib

import pytest

from portfolio_hq.owner import image_integrity as integrity
from test_portfolio_hq_owner_chart_inbox import (
    REAL_JPEG_SIZE,
    header_only_jpeg_bytes,
    jpeg_bytes,
    png_bytes,
)

try:  # Pillow arrives transitively with matplotlib; treat it as a bonus layer.
    from PIL import Image as _PIL_Image
except ImportError:  # pragma: no cover - exercised only without Pillow
    _PIL_Image = None

requires_pillow = pytest.mark.skipif(
    _PIL_Image is None, reason="Pillow unavailable; core coverage does not need it")


# ── helpers ──────────────────────────────────────────────────────────────────

def _png_chunks(data: bytes):
    """Yield ``(offset, length, type, payload_end)`` for each chunk."""
    offset = 8
    while offset + 8 <= len(data):
        length = int.from_bytes(data[offset:offset + 4], "big")
        chunk_type = data[offset + 4:offset + 8]
        yield offset, length, chunk_type, offset + 8 + length + 4
        offset += 8 + length + 4


def _offset_of(data: bytes, wanted: bytes) -> tuple[int, int]:
    for offset, length, chunk_type, end in _png_chunks(data):
        if chunk_type == wanted:
            return offset, end
    raise AssertionError(f"no {wanted!r} chunk in the fixture")


def _flip(data: bytes, index: int) -> bytes:
    return data[:index] + bytes([data[index] ^ 0x5A]) + data[index + 1:]


def _accepts(data: bytes) -> bool:
    try:
        integrity.verify_complete_image(data)
        return True
    except integrity.ImageIntegrityError:
        return False


def _reason(data: bytes) -> str:
    with pytest.raises(integrity.ImageIntegrityError) as excinfo:
        integrity.verify_complete_image(data)
    return excinfo.value.reason


def _pillow_decodes(data: bytes) -> bool:
    if _PIL_Image is None:  # pragma: no cover - guarded by requires_pillow
        raise RuntimeError("Pillow unavailable")
    try:
        image = _PIL_Image.open(io.BytesIO(data))
        image.load()
        return True
    except Exception:
        return False


# ── valid images are accepted ────────────────────────────────────────────────

def test_a_real_png_is_accepted_with_its_true_dimensions():
    assert integrity.verify_complete_image(png_bytes(40, 24)) == ("image/png", 40, 24)


def test_a_real_jpeg_is_accepted_with_its_true_dimensions():
    media_type, width, height = integrity.verify_complete_image(jpeg_bytes())
    assert media_type == "image/jpeg"
    assert (width, height) == REAL_JPEG_SIZE


@pytest.mark.parametrize("size", [(1, 1), (2, 3), (17, 5), (256, 129), (800, 600)])
def test_real_pngs_of_many_shapes_are_accepted(size):
    width, height = size
    assert integrity.verify_complete_image(png_bytes(width, height)) == \
        ("image/png", width, height)


# ── PNG: incomplete payloads are refused ─────────────────────────────────────

def test_png_truncated_immediately_after_ihdr_is_refused():
    """The exact regression: dimensions readable, no image behind them."""
    png = png_bytes()
    _, ihdr_end = _offset_of(png, b"IHDR")
    truncated = png[:ihdr_end]
    assert len(truncated) > 8, "fixture sanity"
    assert _reason(truncated) == "corrupt_or_unreadable_image"


def test_png_with_header_but_no_image_data_is_refused():
    png = png_bytes()
    _, ihdr_end = _offset_of(png, b"IHDR")
    iend_start, iend_end = _offset_of(png, b"IEND")
    header_plus_terminator = png[:ihdr_end] + png[iend_start:iend_end]
    assert _reason(header_plus_terminator) == "corrupt_or_unreadable_image"


def test_png_without_its_iend_terminator_is_refused():
    png = png_bytes()
    iend_start, _ = _offset_of(png, b"IEND")
    assert _reason(png[:iend_start]) == "corrupt_or_unreadable_image"


def test_png_truncated_mid_image_data_is_refused():
    png = png_bytes(120, 90)
    assert _reason(png[:len(png) // 2]) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("chopped", [1, 2, 5, 13])
def test_png_missing_its_last_bytes_is_refused(chopped: int):
    assert _reason(png_bytes()[:-chopped]) == "corrupt_or_unreadable_image"


def test_png_with_a_corrupted_chunk_crc_is_refused():
    png = png_bytes()
    _, ihdr_end = _offset_of(png, b"IHDR")
    assert _reason(_flip(png, ihdr_end - 1)) == "corrupt_or_unreadable_image"


def test_png_with_corrupted_image_data_is_refused():
    png = png_bytes(64, 48)
    idat_start, _ = _offset_of(png, b"IDAT")
    assert _reason(_flip(png, idat_start + 20)) == "corrupt_or_unreadable_image"


def test_png_with_an_overlong_chunk_length_is_refused():
    png = png_bytes()
    idat_start, _ = _offset_of(png, b"IDAT")
    forged = png[:idat_start] + (2 ** 30).to_bytes(4, "big") + png[idat_start + 4:]
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_png_not_beginning_with_ihdr_is_refused():
    png = png_bytes()
    _, ihdr_end = _offset_of(png, b"IHDR")
    reordered = png[:8] + png[ihdr_end:] + png[8:ihdr_end]
    assert _reason(reordered) == "corrupt_or_unreadable_image"


def test_png_with_data_after_iend_is_refused():
    png = png_bytes()
    assert _reason(png + b"trailing junk") == "corrupt_or_unreadable_image"


def test_png_declaring_zero_dimensions_is_refused():
    png = png_bytes()
    ihdr_start, _ = _offset_of(png, b"IHDR")
    payload = ihdr_start + 8
    forged = png[:payload] + struct.pack(">II", 0, 0) + png[payload + 8:]
    # Repair the CRC so the rejection is about the dimensions, not the checksum.
    body = forged[ihdr_start + 4:payload + 13]
    forged = (forged[:payload + 13]
              + (zlib.crc32(body) & 0xFFFFFFFF).to_bytes(4, "big")
              + forged[payload + 17:])
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_png_signature_alone_is_refused():
    assert _reason(b"\x89PNG\r\n\x1a\n") == "corrupt_or_unreadable_image"


def test_png_declaring_impossible_dimensions_is_refused_without_allocating():
    """A decompression bomb must be refused from its header arithmetic."""
    png = png_bytes()
    ihdr_start, _ = _offset_of(png, b"IHDR")
    payload = ihdr_start + 8
    forged = png[:payload] + struct.pack(">II", 65535, 65535) + png[payload + 8:]
    body = forged[ihdr_start + 4:payload + 13]
    forged = (forged[:payload + 13]
              + (zlib.crc32(body) & 0xFFFFFFFF).to_bytes(4, "big")
              + forged[payload + 17:])
    assert _reason(forged) == "corrupt_or_unreadable_image"


def _assemble_png(declared_height: int, actual_rows: int, width: int = 16) -> bytes:
    """A PNG whose IHDR declares one height while its IDAT carries another.

    Every chunk CRC is correct, IHDR is first, IEND is present, and the
    compressed stream terminates cleanly — so container-level checks alone all
    pass. Only comparing the decompressed raster against the size the header
    implies catches it. This is a file an attacker (or a half-finished write)
    can genuinely produce.
    """
    def chunk(tag: bytes, payload: bytes) -> bytes:
        body = tag + payload
        return (struct.pack(">I", len(payload)) + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))

    raster = b"".join(b"\x00" + bytes((x * 3) % 256 for x in range(width * 3))
                      for _ in range(actual_rows))
    return (b"\x89PNG\r\n\x1a\x0a".replace(b"\x0a", b"\n")
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, declared_height,
                                         8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raster))
            + chunk(b"IEND", b""))


def test_png_whose_image_data_is_short_for_its_declared_height_is_refused():
    """Structurally perfect, but the raster does not match the header."""
    honest = _assemble_png(declared_height=8, actual_rows=8)
    assert integrity.verify_complete_image(honest) == ("image/png", 16, 8)

    short = _assemble_png(declared_height=8, actual_rows=4)
    assert _reason(short) == "corrupt_or_unreadable_image"


def test_png_whose_image_data_is_long_for_its_declared_height_is_refused():
    assert _reason(_assemble_png(declared_height=4, actual_rows=9)) == \
        "corrupt_or_unreadable_image"


@pytest.mark.parametrize("actual_rows", [0, 1, 3, 7, 9, 40])
def test_only_the_exact_raster_size_is_accepted(actual_rows: int):
    data = _assemble_png(declared_height=8, actual_rows=actual_rows)
    if actual_rows == 8:
        assert _accepts(data)
    else:
        assert _reason(data) == "corrupt_or_unreadable_image"


@requires_pillow
def test_a_short_raster_png_is_where_we_are_stricter_than_a_lenient_decoder():
    """Pillow renders this file; we refuse it, deliberately.

    A PNG declaring eight rows while carrying four decodes happily in a lenient
    decoder, which simply leaves the remainder blank. For a chart the owner
    submits as evidence that is the wrong trade: the stored image would silently
    misrepresent itself, and the recorded dimensions would describe content that
    is not there. Strictness is the point of this boundary, so this asymmetry is
    pinned rather than left to drift.
    """
    short = _assemble_png(declared_height=8, actual_rows=4)
    assert _accepts(short) is False, "the inbox must refuse a short raster"
    assert _pillow_decodes(short) is True, (
        "if a real decoder starts refusing this too, this test is merely stale, "
        "not a regression — the inbox behaviour above is what matters")


# ── JPEG: incomplete payloads are refused ────────────────────────────────────

def test_jpeg_header_without_a_scan_is_refused():
    """The fixture that used to pass as a valid JPEG."""
    header_only = header_only_jpeg_bytes()
    assert _reason(header_only) == "corrupt_or_unreadable_image"


def test_jpeg_header_without_a_scan_is_also_rejected_by_a_real_decoder():
    if _PIL_Image is None:  # pragma: no cover
        pytest.skip("Pillow unavailable")
    assert _pillow_decodes(header_only_jpeg_bytes()) is False


def test_jpeg_truncated_after_its_frame_header_is_refused():
    assert _reason(jpeg_bytes()[:40]) == "corrupt_or_unreadable_image"


def test_jpeg_without_its_end_marker_is_refused():
    assert _reason(jpeg_bytes()[:-2]) == "corrupt_or_unreadable_image"


def test_jpeg_truncated_mid_scan_is_refused():
    jpeg = jpeg_bytes()
    assert _reason(jpeg[:len(jpeg) - 40]) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("keep", [3, 4, 10, 20, 100, 300])
def test_every_jpeg_prefix_short_of_the_whole_is_refused(keep: int):
    jpeg = jpeg_bytes()
    assert keep < len(jpeg), "fixture sanity"
    assert _reason(jpeg[:keep]) == "corrupt_or_unreadable_image"


def test_jpeg_with_a_malformed_segment_length_is_refused():
    jpeg = jpeg_bytes()
    # Byte 4-5 is the APP0 segment length; a bogus length desynchronises the
    # marker walk, which must be detected rather than skipped past.
    forged = jpeg[:4] + (60000).to_bytes(2, "big") + jpeg[6:]
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_jpeg_with_a_zero_segment_length_is_refused():
    jpeg = jpeg_bytes()
    forged = jpeg[:4] + (0).to_bytes(2, "big") + jpeg[6:]
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_jpeg_magic_alone_is_refused():
    assert _reason(b"\xff\xd8\xff") == "corrupt_or_unreadable_image"


def test_jpeg_soi_and_eoi_only_is_refused():
    assert _reason(b"\xff\xd8\xff\xd9") in ("corrupt_or_unreadable_image",
                                            "unsupported_media_type")


def _jpeg_without_eoi_but_terminated_scan() -> bytes:
    """A JPEG whose scan ends at a real marker, with no EOI anywhere.

    Chopping the trailing EOI alone is caught earlier, because the entropy scan
    then runs off the end of the buffer. Appending a well-formed comment
    segment terminates the scan legitimately, so the stream parses cleanly to
    EOF — and only the explicit end-of-image requirement catches that the image
    was never finished.
    """
    jpeg = jpeg_bytes()
    assert jpeg.endswith(b"\xff\xd9"), "fixture should end with EOI"
    comment = b"\xff\xfe" + struct.pack(">H", 4) + b"hi"
    return jpeg[:-2] + comment


def test_jpeg_that_parses_cleanly_but_never_ends_is_refused():
    forged = _jpeg_without_eoi_but_terminated_scan()
    assert b"\xff\xd9" not in forged, "the fixture must contain no EOI"
    assert _reason(forged) == "corrupt_or_unreadable_image"


@requires_pillow
def test_an_unterminated_jpeg_is_where_we_are_stricter_than_a_lenient_decoder():
    """Same asymmetry, deliberately: a lenient decoder renders an image whose
    stream was never finished. An unfinished capture is not complete evidence,
    so the inbox refuses it."""
    forged = _jpeg_without_eoi_but_terminated_scan()
    assert _accepts(forged) is False, "the inbox must refuse an unterminated JPEG"
    assert _pillow_decodes(forged) is True, (
        "if a real decoder starts refusing this too, this test is merely stale, "
        "not a regression — the inbox behaviour above is what matters")


# ── format gate ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("payload", [
    b"GIF89a" + b"\x00" * 40,
    b"RIFF\x24\x00\x00\x00WEBPVP8 " + b"\x00" * 16,
    b"%PDF-1.7\n" + b"\x00" * 32,
    b"<svg xmlns='http://www.w3.org/2000/svg'/>",
    b"PK\x03\x04" + b"\x00" * 40,
    b"MZ\x90\x00" + b"\x00" * 40,
    b"\x00" * 64,
])
def test_other_formats_are_unsupported_not_merely_corrupt(payload: bytes):
    assert _reason(payload) == "unsupported_media_type"


def test_empty_payload_has_its_own_reason():
    assert _reason(b"") == "empty_payload"


def test_the_accepted_set_is_exactly_png_and_jpeg():
    assert integrity.SUPPORTED_MEDIA_TYPES == ("image/png", "image/jpeg")


def test_sniffing_uses_only_leading_bytes():
    assert integrity.sniff_media_type(png_bytes()) == "image/png"
    assert integrity.sniff_media_type(jpeg_bytes()) == "image/jpeg"
    assert integrity.sniff_media_type(b"\x89PNG") is None
    assert integrity.sniff_media_type(b"") is None


# ── cross-check against a real decoder ───────────────────────────────────────

def _pillow_png(width: int, height: int, **kwargs) -> bytes:
    buffer = io.BytesIO()
    _PIL_Image.new("RGB", (width, height), (40, 110, 170)).save(
        buffer, format="PNG", **kwargs)
    return buffer.getvalue()


def _pillow_jpeg(width: int, height: int, **kwargs) -> bytes:
    buffer = io.BytesIO()
    _PIL_Image.new("RGB", (width, height), (170, 110, 40)).save(
        buffer, format="JPEG", quality=85, **kwargs)
    return buffer.getvalue()


@requires_pillow
@pytest.mark.parametrize("mode", ["RGB", "L", "RGBA", "P"])
def test_real_pngs_from_a_real_encoder_are_accepted(mode: str):
    buffer = io.BytesIO()
    _PIL_Image.new(mode, (48, 31)).save(buffer, format="PNG")
    assert integrity.verify_complete_image(buffer.getvalue()) == ("image/png", 48, 31)


@requires_pillow
def test_interlaced_adam7_pngs_are_accepted():
    """Adam7 changes the expected raster size; getting it wrong would reject
    every interlaced PNG, or accept a truncated one."""
    data = _pillow_png(37, 23, interlace=1)
    assert integrity.verify_complete_image(data) == ("image/png", 37, 23)


@requires_pillow
@pytest.mark.parametrize("kwargs", [{}, {"progressive": True},
                                    {"restart_marker_blocks": 1}, {"optimize": True}])
def test_real_jpeg_variants_are_accepted(kwargs):
    data = _pillow_jpeg(52, 34, **kwargs)
    assert integrity.verify_complete_image(data) == ("image/jpeg", 52, 34)


@requires_pillow
def test_nothing_a_real_decoder_rejects_is_ever_accepted():
    """The safety-critical direction: zero false accepts.

    Our verifier may be *stricter* than a lenient decoder — a PNG missing its
    IEND still renders in Pillow but is refused here, which is correct for
    evidence. It must never be looser.
    """
    png = _pillow_png(64, 40)
    jpeg = _pillow_jpeg(64, 40)
    damaged = [
        png[:33], png[:len(png) // 2], png[:-12], png[:-1], png[:8],
        _flip(png, 30), _flip(png, len(png) - 20),
        jpeg[:40], jpeg[:-2], jpeg[:len(jpeg) // 2], b"\xff\xd8\xff",
        header_only_jpeg_bytes(),
    ]
    damaged += [
        _assemble_png(declared_height=8, actual_rows=4),
        _jpeg_without_eoi_but_terminated_scan(),
    ]
    false_accepts = [
        index for index, payload in enumerate(damaged)
        if _accepts(payload) and not _pillow_decodes(payload)
    ]
    assert false_accepts == [], (
        f"accepted payload(s) a real decoder cannot read: {false_accepts}")
    # And confirm the asymmetry runs the safe way round: we refuse everything
    # in this set, including the two a lenient decoder would still render.
    assert not any(_accepts(payload) for payload in damaged)


@requires_pillow
def test_everything_we_accept_a_real_decoder_can_actually_open():
    """The persisted evidence must be consumable by a later analysis path."""
    for data in (png_bytes(40, 24), jpeg_bytes(),
                 _pillow_png(64, 40), _pillow_jpeg(64, 40),
                 _pillow_png(37, 23, interlace=1),
                 _pillow_jpeg(52, 34, progressive=True)):
        assert _accepts(data), "fixture should be accepted"
        assert _pillow_decodes(data) is True, (
            "accepted an image a real decoder cannot open")


@requires_pillow
def test_reported_dimensions_match_a_real_decoder():
    for data in (png_bytes(40, 24), jpeg_bytes(), _pillow_png(123, 45),
                 _pillow_jpeg(80, 61), _pillow_png(37, 23, interlace=1)):
        _, width, height = integrity.verify_complete_image(data)
        image = _PIL_Image.open(io.BytesIO(data))
        assert (width, height) == image.size
