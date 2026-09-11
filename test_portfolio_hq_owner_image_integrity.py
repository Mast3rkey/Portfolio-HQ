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


# ── JPEG: structural admission ───────────────────────────────────────────────
#
# A JPEG can be a well-formed *marker stream* and still be something no decoder
# will read. Dimensions live in the frame header, so a file can advertise a
# size while its frame header's declared length contradicts its component
# count, or its scan header selects nothing, selects a component the frame
# never defined, or declares a coefficient range its own frame mode forbids.
# The builders below produce exactly those shapes, one defect at a time,
# against a control that is otherwise byte-for-byte valid.

def _jpeg_segment(marker: int, payload: bytes) -> bytes:
    return bytes((0xFF, marker)) + struct.pack(">H", len(payload) + 2) + payload


def _jpeg_dqt(slot: int = 0) -> bytes:
    """DQT defining one 8-bit quantisation table in `slot`."""
    return _jpeg_segment(0xDB, bytes([slot]) + bytes(64))


def _jpeg_dht(table_class: int, slot: int) -> bytes:
    """DHT defining one table (a single one-bit code) in `(class, slot)`."""
    counts = bytes([1] + [0] * 15)
    return _jpeg_segment(0xC4, bytes([(table_class << 4) | slot]) + counts + b"\x00")


_THREE_COMPONENTS = ((1, 0x11, 0), (2, 0x11, 0), (3, 0x11, 0))
_THREE_SELECTORS = ((1, 0x00), (2, 0x00), (3, 0x00))


def _jpeg_sof(marker: int = 0xC0, *, precision: int = 8, height: int = 18,
              width: int = 32, components=_THREE_COMPONENTS,
              declared_count: int | None = None) -> bytes:
    """A frame header. `declared_count` decouples Nf from the records present."""
    count = len(components) if declared_count is None else declared_count
    payload = (bytes([precision]) + struct.pack(">HH", height, width)
               + bytes([count]) + b"".join(bytes(record) for record in components))
    return _jpeg_segment(marker, payload)


def _jpeg_sos(*, components=_THREE_SELECTORS, declared_count: int | None = None,
              spectral: tuple[int, int] = (0, 63), approximation: int = 0) -> bytes:
    """A scan header. `declared_count` decouples Ns from the records present."""
    count = len(components) if declared_count is None else declared_count
    payload = (bytes([count]) + b"".join(bytes(record) for record in components)
               + bytes([spectral[0], spectral[1], approximation]))
    return _jpeg_segment(0xDA, payload)


def _jpeg_stream(*parts: bytes, entropy: bytes = b"\x42") -> bytes:
    return b"\xff\xd8" + b"".join(parts) + entropy + b"\xff\xd9"


def _baseline_jpeg(**sof_kwargs) -> bytes:
    """The control: every structure coherent, tables defined, terminated."""
    return _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                        _jpeg_sof(**sof_kwargs), _jpeg_sos())


def _progressive_jpeg(**sos_kwargs) -> bytes:
    """A progressive frame carrying one DC scan, defect injected via `sos_kwargs`."""
    defaults = {"spectral": (0, 0), "approximation": 0}
    defaults.update(sos_kwargs)
    return _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                        _jpeg_sof(marker=0xC2), _jpeg_sos(**defaults))


def _reviewer_counterexample() -> bytes:
    """SOI + a frame header exposing only dimensions + an empty scan header.

    This is the payload the previous verifier accepted as a 32x18 JPEG. Nothing
    here can be decoded: the frame header stops before its component count and
    the scan header declares a length of 2, so it selects nothing at all.
    """
    frame = b"\xff\xc0" + struct.pack(">H", 7) + b"\x08" + struct.pack(">HH", 18, 32)
    return b"\xff\xd8" + frame + b"\xff\xda" + struct.pack(">H", 2) + b"\x42\xff\xd9"


def test_the_control_jpeg_is_accepted():
    """Every adversarial case below differs from this by exactly one field."""
    assert integrity.verify_complete_image(_baseline_jpeg()) == ("image/jpeg", 32, 18)


def test_a_jpeg_exposing_dimensions_with_no_usable_scan_is_refused():
    """The finding this section exists for.

    The earlier verifier read width and height out of a frame header, saw one
    SOS marker, one entropy byte and an EOI, and stored the result as a chart.
    """
    assert _reason(_reviewer_counterexample()) == "corrupt_or_unreadable_image"


@requires_pillow
def test_the_undecodable_dimension_only_jpeg_is_refused_by_a_real_decoder_too():
    assert _pillow_decodes(_reviewer_counterexample()) is False
    assert _accepts(_reviewer_counterexample()) is False


# ── JPEG frame header ────────────────────────────────────────────────────────

def test_jpeg_frame_header_too_short_to_carry_a_component_count_is_refused():
    short = b"\xff\xd8" + (b"\xff\xc0" + struct.pack(">H", 7) + b"\x08"
                           + struct.pack(">HH", 18, 32)) + b"\xff\xd9"
    assert _reason(short) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("declared_count", [1, 2, 4])
def test_jpeg_frame_component_count_inconsistent_with_its_length_is_refused(
        declared_count: int):
    """Three component records present, a different number claimed."""
    forged = _baseline_jpeg(declared_count=declared_count)
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_jpeg_frame_header_declaring_no_components_is_refused():
    """A frame with no components makes every scan selector dangle, so the
    reference rule would refuse this too. The frame is where the defect is."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(components=()), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"
    assert "declares no colour components" in _detail(forged)


def test_jpeg_frame_header_reusing_a_component_id_is_refused():
    forged = _baseline_jpeg(components=((1, 0x11, 0), (1, 0x11, 0), (3, 0x11, 0)))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_duplicate_frame_component_is_caught_even_when_nothing_dangles():
    """Isolates the rule.

    In the case above the duplicate also leaves component 2 undefined, so the
    scan's own reference check would refuse the file anyway. Here the frame
    declares component 1 twice and the scan selects only component 1, so
    nothing dangles and the duplicate rule is the only thing standing between
    a two-record frame claiming to have two components and storage.
    """
    forged = _jpeg_stream(
        _jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
        _jpeg_sof(components=((1, 0x11, 0), (1, 0x11, 0))),
        _jpeg_sos(components=((1, 0x00),)))
    assert _reason(forged) == "corrupt_or_unreadable_image"
    assert "same colour component twice" in _detail(forged)


def test_a_frame_pointing_at_an_impossible_quant_slot_says_so_precisely():
    """A slot above 3 can never be defined, so the definedness rule would also
    refuse this file — with the wrong explanation. The owner is told the header
    is malformed, not that a table is missing."""
    forged = _baseline_jpeg(components=((1, 0x11, 9), (2, 0x11, 0), (3, 0x11, 0)))
    assert "quantisation table slot that cannot exist" in _detail(forged)


@pytest.mark.parametrize("sampling", [0x00, 0x01, 0x10, 0x51, 0x15])
def test_jpeg_frame_header_with_an_illegal_sampling_factor_is_refused(sampling: int):
    forged = _baseline_jpeg(
        components=((1, sampling, 0), (2, 0x11, 0), (3, 0x11, 0)))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_jpeg_frame_header_pointing_at_an_impossible_quant_slot_is_refused():
    forged = _baseline_jpeg(components=((1, 0x11, 9), (2, 0x11, 0), (3, 0x11, 0)))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_with_two_frame_headers_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_sof(width=64), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_scan_before_any_frame_header_is_refused():
    """With no frame yet, every selector is by definition undefined, so the
    reference rule would refuse this file too. Saying "there is no image here"
    is the accurate diagnosis, so the ordering is pinned."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sos(), _jpeg_sof())
    assert _reason(forged) == "corrupt_or_unreadable_image"
    assert "before any frame header" in _detail(forged)


# ── JPEG variants outside the admitted subset ────────────────────────────────
#
# These are legal JPEG. They are refused as *unsupported*, not as damage,
# because the owner needs to know to re-save rather than think the file broke.

@pytest.mark.parametrize("marker", [0xC3, 0xC5, 0xC6, 0xC7,
                                    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF])
def test_lossless_differential_and_arithmetic_jpeg_is_unsupported_not_corrupt(
        marker: int):
    assert _reason(_baseline_jpeg(marker=marker)) == "unsupported_media_type"


@pytest.mark.parametrize("marker", [0xC0, 0xC1, 0xC2])
def test_baseline_extended_and_progressive_frames_are_admitted(marker: int):
    spectral = (0, 0) if marker == 0xC2 else (0, 63)
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(marker=marker), _jpeg_sos(spectral=spectral))
    assert integrity.verify_complete_image(forged) == ("image/jpeg", 32, 18)


@pytest.mark.parametrize("precision", [0, 1, 12, 16, 255])
def test_jpeg_outside_eight_bit_precision_is_unsupported_not_corrupt(precision: int):
    assert _reason(_baseline_jpeg(precision=precision)) == "unsupported_media_type"


def test_a_jpeg_with_more_components_than_a_chart_can_have_is_unsupported():
    forged = _baseline_jpeg(
        components=tuple((index, 0x11, 0) for index in range(1, 6)))
    assert _reason(forged) == "unsupported_media_type"


@pytest.mark.parametrize("count", [1, 3, 4])
def test_greyscale_colour_and_cmyk_component_counts_are_all_admitted(count: int):
    components = tuple((index, 0x11, 0) for index in range(1, count + 1))
    selectors = tuple((index, 0x00) for index in range(1, count + 1))
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(components=components),
                          _jpeg_sos(components=selectors))
    assert integrity.verify_complete_image(forged) == ("image/jpeg", 32, 18)


# ── JPEG scan header ─────────────────────────────────────────────────────────

def test_a_jpeg_scan_header_with_no_payload_at_all_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), b"\xff\xda" + struct.pack(">H", 2))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_scan_selecting_no_components_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_sos(components=()))
    assert _reason(forged) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("declared_count", [1, 2, 4, 255])
def test_jpeg_scan_component_count_inconsistent_with_its_length_is_refused(
        declared_count: int):
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(),
                          _jpeg_sos(declared_count=declared_count))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_scan_with_a_truncated_selector_record_is_refused():
    """Three selectors claimed; the third record is cut in half."""
    payload = b"\x03" + b"\x01\x00\x02\x00\x03" + bytes([0, 63, 0])
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_segment(0xDA, payload))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_scan_selecting_an_undefined_component_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(),
                          _jpeg_sos(components=((1, 0x00), (2, 0x00), (9, 0x00))))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_scan_selecting_the_same_component_twice_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(),
                          _jpeg_sos(components=((1, 0x00), (1, 0x00), (3, 0x00))))
    assert _reason(forged) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("spectral,approximation", [
    ((5, 63), 0),     # a sequential scan cannot start above DC
    ((0, 10), 0),     # nor stop below the last coefficient
    ((0, 63), 0x11),  # nor carry successive approximation
    ((0, 63), 0x01),
])
def test_a_sequential_jpeg_scan_with_progressive_only_fields_is_refused(
        spectral, approximation):
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(),
                          _jpeg_sos(spectral=spectral, approximation=approximation))
    assert _reason(forged) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("spectral", [(0, 40), (0, 63), (70, 70), (5, 2), (1, 70)])
def test_a_progressive_jpeg_scan_with_an_impossible_range_is_refused(spectral):
    assert _reason(_progressive_jpeg(spectral=spectral)) == \
        "corrupt_or_unreadable_image"


@pytest.mark.parametrize("spectral", [(70, 70), (5, 2), (1, 70), (64, 64)])
def test_a_single_component_progressive_scan_range_is_checked_on_its_own(spectral):
    """Isolates the range rule from the AC-single-component rule: these scans
    select one component, so the only thing wrong with them is the range."""
    forged = _progressive_jpeg(components=((1, 0x00),), spectral=spectral)
    assert "coefficient range no decoder can read" in _detail(forged)


@pytest.mark.parametrize("approximation", [0xE0, 0x0E, 0xFF])
def test_a_progressive_jpeg_scan_with_an_impossible_approximation_is_refused(
        approximation: int):
    assert _reason(_progressive_jpeg(approximation=approximation)) == \
        "corrupt_or_unreadable_image"


def test_a_progressive_ac_scan_selecting_several_components_is_refused():
    """AC scans in a progressive JPEG carry exactly one component."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(marker=0xC2),
                          _jpeg_sos(spectral=(1, 5)))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_progressive_ac_scan_with_one_component_is_accepted():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(marker=0xC2),
                          _jpeg_sos(components=((1, 0x00),), spectral=(1, 5)))
    assert integrity.verify_complete_image(forged) == ("image/jpeg", 32, 18)


def test_a_progressive_dc_refinement_scan_needs_no_huffman_table():
    """Ah > 0 on a DC scan is coded without tables; requiring one would reject
    the second half of every real progressive JPEG."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(1, 0), _jpeg_sof(marker=0xC2),
                          _jpeg_sos(spectral=(0, 0), approximation=0x10))
    assert integrity.verify_complete_image(forged) == ("image/jpeg", 32, 18)


# ── JPEG tables the scan actually needs ──────────────────────────────────────

def test_a_structurally_perfect_jpeg_with_no_scan_at_all_is_refused():
    """Frame header valid, tables defined, terminated — and no image in it."""
    forged = (b"\xff\xd8" + _jpeg_dqt(0) + _jpeg_dht(0, 0) + _jpeg_dht(1, 0)
              + _jpeg_sof() + b"\xff\xd9")
    assert "no image scan" in _detail(forged)


def test_a_jpeg_whose_scan_carries_not_one_byte_of_image_data_is_refused():
    """A complete, coherent scan header followed straight by EOI."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_sos(), entropy=b"")
    assert "carries no image data" in _detail(forged)


def test_a_jpeg_whose_scan_needs_an_undefined_quantisation_table_is_refused():
    forged = _jpeg_stream(_jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(),
                          _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_frame_pointing_at_a_quant_slot_that_is_never_defined_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(components=((1, 0x11, 1), (2, 0x11, 0),
                                                (3, 0x11, 0))),
                          _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_with_no_huffman_tables_at_all_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_sof(), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_missing_the_ac_huffman_table_its_scan_uses_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_sof(), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_scan_pointing_at_an_impossible_table_slot_says_so_precisely():
    """As with the frame's quantisation slot: a slot above 3 can never be
    defined, so the definedness rule would refuse this too, less accurately."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(),
                          _jpeg_sos(components=((1, 0xF0), (2, 0x00), (3, 0x00))))
    assert "entropy table slot that cannot exist" in _detail(forged)


def test_a_jpeg_scan_selecting_more_components_than_a_scan_may_carry_says_so():
    """Five coherent selector records. A frame may hold at most four
    components, so the reference and duplicate rules would also catch this;
    the ceiling is what names the actual defect."""
    forged = _jpeg_stream(
        _jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(),
        _jpeg_sos(components=((1, 0x00), (2, 0x00), (3, 0x00),
                              (1, 0x00), (2, 0x00))))
    assert "more colour components than a scan may carry" in _detail(forged)


def test_a_jpeg_scan_pointing_at_an_undefined_table_slot_is_refused():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(),
                          _jpeg_sos(components=((1, 0x20), (2, 0x00), (3, 0x00))))
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_quantisation_table_cut_short_is_refused():
    forged = _jpeg_stream(_jpeg_segment(0xDB, b"\x00" + bytes(40)),
                          _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(),
                          _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_huffman_table_header_cut_short_is_refused():
    """The 16 code-length counts themselves do not fit in the segment, which
    is a different cut from a table whose *values* run past the end."""
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_segment(0xC4, b"\x00" + bytes(5)),
                          _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(),
                          _jpeg_sos())
    assert "Huffman table header is cut short" in _detail(forged)


def test_a_jpeg_huffman_table_cut_short_is_refused():
    truncated = _jpeg_segment(0xC4, b"\x00" + bytes([2] + [0] * 15) + b"\x00")
    forged = _jpeg_stream(_jpeg_dqt(0), truncated, _jpeg_dht(1, 0), _jpeg_sof(),
                          _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("spec", [0x24, 0x09, 0x30])
def test_a_jpeg_declaring_an_out_of_range_huffman_table_is_refused(spec: int):
    table = _jpeg_segment(0xC4, bytes([spec]) + bytes([1] + [0] * 15) + b"\x00")
    forged = _jpeg_stream(_jpeg_dqt(0), table, _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("spec", [0x24, 0x09, 0x20])
def test_a_jpeg_declaring_an_out_of_range_quantisation_table_is_refused(spec: int):
    table = _jpeg_segment(0xDB, bytes([spec]) + bytes(64))
    forged = _jpeg_stream(table, _jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


@pytest.mark.parametrize("payload", [b"\x00", b"\x00\x01\x00", b""])
def test_a_jpeg_restart_interval_header_of_the_wrong_size_is_refused(payload: bytes):
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_segment(0xDD, payload), _jpeg_sos())
    assert _reason(forged) == "corrupt_or_unreadable_image"


def test_a_jpeg_declaring_a_restart_interval_is_still_accepted():
    forged = _jpeg_stream(_jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0),
                          _jpeg_sof(), _jpeg_segment(0xDD, b"\x00\x08"),
                          _jpeg_sos(), entropy=b"\x11\xff\xd0\x22")
    assert integrity.verify_complete_image(forged) == ("image/jpeg", 32, 18)


# ── JPEG structural admission, measured against a real decoder ───────────────

def _jpeg_marker_offset(data: bytes, marker: int) -> int:
    """Offset of the ``0xFF`` byte introducing the first `marker` segment.

    Derived by walking the stream rather than searching for the byte pair: a
    0xFF 0xC0 can occur inside entropy data or an EXIF blob, and a test that
    silently mutated the wrong bytes would prove nothing.
    """
    offset = 2
    while offset < len(data) - 1:
        assert data[offset] == 0xFF, "marker walk lost sync"
        while data[offset] == 0xFF:
            offset += 1
        found = data[offset]
        offset += 1
        if found == marker:
            return offset - 2
        if found in (0xD8, 0xD9, 0x01) or 0xD0 <= found <= 0xD7:
            continue
        offset += int.from_bytes(data[offset:offset + 2], "big")
    raise AssertionError(f"marker 0xFF{marker:02X} not present")


def _set_byte(data: bytes, index: int, value: int) -> bytes:
    mutated = bytearray(data)
    mutated[index] = value
    return bytes(mutated)


#: Every entry `_surgical_jpeg_mutants()` produces. Spelled out because
#: ``parametrize`` runs at import time, before the Pillow guard, and because a
#: corpus that silently shrank would weaken every test that walks it.
_SURGICAL_MUTANT_NAMES = (
    "frame component count too low",
    "frame component count too high",
    "frame component count zero",
    "duplicate frame component id",
    "zero sampling factor",
    "impossible quantisation slot",
    "twelve-bit precision",
    "zero width",
    "zero height",
    "scan selects no components",
    "scan component count too low",
    "scan component count too high",
    "scan selects an undefined component",
    "duplicate scan selector",
    "scan uses an undefined entropy table",
    "sequential scan starts above DC",
    "sequential scan stops below the last coefficient",
    "sequential scan claims successive approximation",
)


def _surgical_jpeg_mutants() -> dict[str, bytes]:
    """One structural defect per entry, injected into a real encoder's output.

    Hand-built fixtures prove the parser's rules; these prove the rules survive
    contact with a genuine 3-component baseline JPEG, entropy data and all.
    """
    real = _pillow_jpeg(64, 40)
    sof = _jpeg_marker_offset(real, 0xC0)
    sos = _jpeg_marker_offset(real, 0xDA)
    precision, height, width, count = sof + 4, sof + 5, sof + 7, sof + 9
    first_component, first_sampling, first_quant = count + 1, count + 2, count + 3
    second_component = count + 4
    scan_count = sos + 4
    first_selector, first_tables = scan_count + 1, scan_count + 2
    second_selector = scan_count + 3
    spectral_start = scan_count + 1 + 2 * real[scan_count]
    return {
        "frame component count too low": _set_byte(real, count, 2),
        "frame component count too high": _set_byte(real, count, 4),
        "frame component count zero": _set_byte(real, count, 0),
        "duplicate frame component id":
            _set_byte(real, second_component, real[first_component]),
        "zero sampling factor": _set_byte(real, first_sampling, 0x00),
        "impossible quantisation slot": _set_byte(real, first_quant, 9),
        "twelve-bit precision": _set_byte(real, precision, 12),
        "zero width": _set_byte(_set_byte(real, width, 0), width + 1, 0),
        "zero height": _set_byte(_set_byte(real, height, 0), height + 1, 0),
        "scan selects no components": _set_byte(real, scan_count, 0),
        "scan component count too low": _set_byte(real, scan_count, 2),
        "scan component count too high": _set_byte(real, scan_count, 4),
        "scan selects an undefined component": _set_byte(real, first_selector, 0x77),
        "duplicate scan selector":
            _set_byte(real, second_selector, real[first_selector]),
        "scan uses an undefined entropy table": _set_byte(real, first_tables, 0x30),
        "sequential scan starts above DC": _set_byte(real, spectral_start, 5),
        "sequential scan stops below the last coefficient":
            _set_byte(real, spectral_start + 1, 10),
        "sequential scan claims successive approximation":
            _set_byte(real, spectral_start + 2, 0x11),
    }


@requires_pillow
def test_the_surgical_jpeg_mutants_are_genuinely_one_field_apart():
    """Guards the corpus itself: a mutant equal to the original proves nothing."""
    real = _pillow_jpeg(64, 40)
    assert _accepts(real) and _pillow_decodes(real) is True
    mutants = _surgical_jpeg_mutants()
    assert sorted(mutants) == sorted(_SURGICAL_MUTANT_NAMES), (
        "the corpus and the parametrised name list have drifted apart")
    for name, mutant in mutants.items():
        assert mutant != real, f"{name!r} did not change any byte"
        assert len(mutant) == len(real), f"{name!r} changed the file length"


@requires_pillow
@pytest.mark.parametrize("name", _SURGICAL_MUTANT_NAMES)
def test_every_structurally_damaged_real_jpeg_is_refused(name: str):
    assert _reason(_surgical_jpeg_mutants()[name]) in (
        "corrupt_or_unreadable_image", "unsupported_media_type")


@requires_pillow
def test_no_structurally_damaged_jpeg_is_accepted_that_a_real_decoder_refuses():
    """The safety-critical direction, at the parser's acceptance boundary.

    Simple truncations are easy to catch. These are the shapes that survive a
    marker walk and still cannot be decoded — the ones the earlier verifier
    let through.
    """
    corpus = dict(_surgical_jpeg_mutants())
    corpus["dimension-only frame, empty scan"] = _reviewer_counterexample()
    corpus["scan header with no payload"] = _jpeg_stream(
        _jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(),
        b"\xff\xda" + struct.pack(">H", 2))
    corpus["scan before any frame"] = _jpeg_stream(
        _jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sos(), _jpeg_sof())
    corpus["two frame headers"] = _jpeg_stream(
        _jpeg_dqt(0), _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(),
        _jpeg_sof(width=64), _jpeg_sos())
    corpus["quantisation table never defined"] = _jpeg_stream(
        _jpeg_dht(0, 0), _jpeg_dht(1, 0), _jpeg_sof(), _jpeg_sos())

    false_accepts = sorted(
        name for name, payload in corpus.items()
        if _accepts(payload) and not _pillow_decodes(payload))
    assert false_accepts == [], (
        f"accepted payload(s) a real decoder cannot read: {false_accepts}")
    still_accepted = sorted(name for name, payload in corpus.items()
                            if _accepts(payload))
    assert still_accepted == [], (
        f"structurally damaged payload(s) were accepted: {still_accepted}")


@requires_pillow
@pytest.mark.parametrize("name", [
    "sequential scan starts above DC",
    "sequential scan stops below the last coefficient",
    "sequential scan claims successive approximation",
])
def test_scan_field_incoherence_is_where_we_are_stricter_than_a_lenient_decoder(
        name: str):
    """A sequential frame whose scan carries progressive-only fields is
    non-conformant; libjpeg renders it anyway. Refusing it is the safe error
    for evidence, and no real encoder emits it — see the accepted-variants
    sweep below."""
    mutant = _surgical_jpeg_mutants()[name]
    assert _accepts(mutant) is False
    assert _pillow_decodes(mutant) is True, (
        "fixture no longer demonstrates the asymmetry; re-check the parser")


@requires_pillow
@pytest.mark.parametrize("kwargs", [
    {}, {"optimize": True},
    {"progressive": True}, {"progressive": True, "optimize": True},
    {"restart_marker_rows": 1}, {"restart_marker_blocks": 2},
    {"progressive": True, "restart_marker_rows": 1},
    {"subsampling": 0}, {"subsampling": 1}, {"subsampling": 2},
])
def test_the_narrowed_subset_still_admits_everything_a_real_encoder_emits(kwargs):
    """The tightened frame and scan rules must not start refusing real charts."""
    data = _pillow_jpeg(64, 40, **kwargs)
    assert integrity.verify_complete_image(data) == ("image/jpeg", 64, 40)
    assert _pillow_decodes(data) is True


@requires_pillow
@pytest.mark.parametrize("quality", [1, 10, 50, 85, 95, 100])
def test_every_encoder_quality_setting_is_still_admitted(quality: int):
    """Low quality drops coefficients and shrinks the Huffman tables; the
    table-definedness rules must not start refusing those files."""
    buffer = io.BytesIO()
    _PIL_Image.new("RGB", (64, 40), (170, 110, 40)).save(
        buffer, format="JPEG", quality=quality)
    assert integrity.verify_complete_image(buffer.getvalue()) == \
        ("image/jpeg", 64, 40)


@requires_pillow
@pytest.mark.parametrize("mode", ["L", "RGB", "CMYK"])
def test_greyscale_colour_and_cmyk_encoder_output_is_still_admitted(mode: str):
    buffer = io.BytesIO()
    _PIL_Image.new(mode, (48, 31)).save(buffer, format="JPEG", quality=85)
    assert integrity.verify_complete_image(buffer.getvalue()) == \
        ("image/jpeg", 48, 31)


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
