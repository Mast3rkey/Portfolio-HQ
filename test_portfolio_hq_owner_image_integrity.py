"""Adversarial tests for chart-image completeness verification.

Two boundaries are pinned here.

*Completeness.* The inbox once accepted a payload as soon as it could read a
dimension field: a PNG truncated immediately after IHDR and a PNG with its IEND
removed were both stored as valid chart evidence. Acceptance is now decided on
the whole byte stream, and the verdicts are cross-checked against a real
decoder.

*Format.* PNG is the only accepted format. JPEG was admitted, then withdrawn:
no amount of structural checking could establish that a JPEG's Huffman-coded
raster is readable, and a 141-byte payload declaring a 65535x65535 frame proved
the point by satisfying every structural rule while a real decoder refused it
outright. The tests below therefore assert that JPEG is *recognised and
refused* — by content, never by filename — rather than asserting anything about
JPEG admission.
"""

from __future__ import annotations

import io
import struct
import zlib

import pytest

from portfolio_hq.owner import image_integrity as integrity
from test_portfolio_hq_owner_chart_inbox import jpeg_bytes, png_bytes

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


def _detail(data: bytes) -> str:
    """The verifier's own explanation.

    Some rules below are redundant *for the verdict* — remove them and the
    payload is still refused, by a later rule, for a vaguer reason. They are
    kept because the owner is told what is wrong with their file, and a wrong
    diagnosis on an evidence boundary is its own failure. Pinning the wording
    is what makes those rules testable at all.
    """
    with pytest.raises(integrity.ImageIntegrityError) as excinfo:
        integrity.verify_complete_image(data)
    return str(excinfo.value)


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


def test_a_real_jpeg_is_refused_as_unsupported_not_as_damage():
    """A sound JPEG is not a broken file; the owner is told to convert it."""
    assert _reason(jpeg_bytes()) == "unsupported_media_type"
    assert "PNG only" in _detail(jpeg_bytes())


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
    """The ordering rule owns this diagnosis. Remove it and the file is still
    refused \u2014 by the missing-header rule, which is a different and vaguer
    claim \u2014 so the wording is pinned as well as the verdict."""
    png = png_bytes()
    _, ihdr_end = _offset_of(png, b"IHDR")
    reordered = png[:8] + png[ihdr_end:] + png[8:ihdr_end]
    assert _reason(reordered) == "corrupt_or_unreadable_image"
    assert "does not begin with its IHDR" in _detail(reordered)


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
    assert "zero dimension" in _detail(forged)


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
    # Pinned on the wording, not just the verdict: without the ceiling the file
    # is still refused, but only after the raster-length comparison — which is
    # exactly the check the ceiling exists to run *before*.
    assert "dimensions too large to verify safely" in _detail(forged)


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


def test_the_accepted_set_is_exactly_png():
    assert integrity.SUPPORTED_MEDIA_TYPES == ("image/png",)


def test_jpeg_is_recognised_but_not_accepted():
    """Recognising JPEG is what lets it be refused *for what it is*. If sniffing
    simply forgot the format, a JPEG would be refused as unidentifiable and the
    owner would be left guessing why their perfectly good chart bounced."""
    assert integrity.RECOGNISED_UNSUPPORTED_MEDIA_TYPES == ("image/jpeg",)
    assert "image/jpeg" not in integrity.SUPPORTED_MEDIA_TYPES
    assert integrity.sniff_media_type(jpeg_bytes()) == "image/jpeg"


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


def _undecodable_but_structurally_coherent_jpeg() -> bytes:
    """The payload that ended JPEG support.

    Every structural rule the hand-written parser could enforce is satisfied:
    quantisation and Huffman tables defined, a baseline frame with one coherent
    component record, a scan selecting it with legal spectral fields, entropy
    data, EOI. It declares 65535x65535 from 141 bytes, and a real decoder
    refuses it outright. No amount of further structural checking reaches this,
    because the bound that would catch it requires actually decompressing the
    raster — which PNG allows through ``zlib`` and JPEG does not allow at all
    without a codec.
    """
    def segment(marker: int, body: bytes) -> bytes:
        return bytes((0xFF, marker)) + struct.pack(">H", len(body) + 2) + body

    return (b"\xff\xd8"
            + segment(0xDB, b"\x00" + bytes(64))
            + segment(0xC4, b"\x00" + bytes([1] + [0] * 15) + b"\x00")
            + segment(0xC4, b"\x10" + bytes([1] + [0] * 15) + b"\x00")
            + segment(0xC0, b"\x08" + struct.pack(">HH", 65535, 65535)
                      + b"\x01" + bytes([1, 0x11, 0]))
            + segment(0xDA, b"\x01" + bytes([1, 0x00]) + bytes([0, 63, 0]))
            + b"\x42\xff\xd9")


def test_the_jpeg_that_ended_jpeg_support_is_refused():
    """Refused on format, so its structure never gets a chance to matter."""
    assert _reason(_undecodable_but_structurally_coherent_jpeg()) == \
        "unsupported_media_type"


@requires_pillow
def test_that_jpeg_really_is_one_a_real_decoder_cannot_open():
    """Guards the premise. If a future Pillow happily loaded this, the fixture
    would no longer demonstrate why the format was withdrawn."""
    assert _pillow_decodes(_undecodable_but_structurally_coherent_jpeg()) is False


@requires_pillow
@pytest.mark.parametrize("kwargs", [
    {}, {"progressive": True}, {"optimize": True},
    {"restart_marker_blocks": 1}, {"subsampling": 2},
])
def test_sound_jpegs_from_a_real_encoder_are_refused_as_unsupported(kwargs):
    """These files are perfectly good. They are still not accepted, and the
    reason says so rather than calling them damaged."""
    data = _pillow_jpeg(52, 34, **kwargs)
    assert _pillow_decodes(data) is True, "fixture should be a sound JPEG"
    assert _reason(data) == "unsupported_media_type"
    assert "PNG only" in _detail(data)


@requires_pillow
def test_nothing_a_real_decoder_rejects_is_ever_accepted():
    """The safety-critical direction: zero false accepts.

    Our verifier may be *stricter* than a lenient decoder — a PNG missing its
    IEND still renders in Pillow but is refused here, which is correct for
    evidence. It must never be looser.
    """
    png = _pillow_png(64, 40)
    damaged = [
        png[:33], png[:len(png) // 2], png[:-12], png[:-1], png[:8],
        _flip(png, 30), _flip(png, len(png) - 20),
        _assemble_png(declared_height=8, actual_rows=4),
        b"\x89PNG\r\n\x1a\n",
    ]
    false_accepts = [
        index for index, payload in enumerate(damaged)
        if _accepts(payload) and not _pillow_decodes(payload)
    ]
    assert false_accepts == [], (
        f"accepted payload(s) a real decoder cannot read: {false_accepts}")
    # And confirm the asymmetry runs the safe way round: we refuse everything
    # in this set, including the ones a lenient decoder would still render.
    assert not any(_accepts(payload) for payload in damaged)


@requires_pillow
def test_no_jpeg_payload_of_any_shape_is_ever_accepted():
    """Sound, damaged, truncated, hand-built — the format gate comes first."""
    jpeg = _pillow_jpeg(64, 40)
    for payload in (jpeg, jpeg[:40], jpeg[:-2], jpeg[:len(jpeg) // 2],
                    b"\xff\xd8\xff", jpeg_bytes(),
                    _undecodable_but_structurally_coherent_jpeg()):
        assert not _accepts(payload)


@requires_pillow
def test_everything_we_accept_a_real_decoder_can_actually_open():
    """The persisted evidence must be consumable by a later analysis path."""
    for data in (png_bytes(40, 24), _pillow_png(64, 40),
                 _pillow_png(37, 23, interlace=1), _pillow_png(1, 1)):
        assert _accepts(data), "fixture should be accepted"
        assert _pillow_decodes(data) is True, (
            "accepted an image a real decoder cannot open")


@requires_pillow
def test_reported_dimensions_match_a_real_decoder():
    for data in (png_bytes(40, 24), _pillow_png(123, 45),
                 _pillow_png(37, 23, interlace=1)):
        _, width, height = integrity.verify_complete_image(data)
        image = _PIL_Image.open(io.BytesIO(data))
        assert (width, height) == image.size
