"""Structural completeness verification for accepted chart images.

Why this exists
---------------
Sniffing a magic number and reading a dimension header proves an image *starts*
like a PNG or JPEG. It does not prove the uploaded bytes form a complete,
usable image. A chart inbox that stores an evidence file a later reviewer
cannot open has failed at its one job, so acceptance is decided here on the
whole byte stream rather than on its first few fields.

Why standard library only
-------------------------
A full decoder is not needed to answer "are these bytes complete", and pulling
one in would be the wrong trade twice over: it would put a large native
image-parsing library directly on an untrusted-input boundary, and it would
break the hosted service's standard-library-only property, which the
provider-neutral deployment contract depends on. Everything below uses
``zlib`` and ``struct``.

What each check actually proves — stated precisely, because the difference
matters for an evidence-receipt boundary:

* **PNG — completeness is genuinely proven.** Every chunk's CRC-32 is verified,
  chunk ordering and the terminal ``IEND`` are required, and the concatenated
  ``IDAT`` stream is actually decompressed and its length checked against the
  size the ``IHDR`` header implies (Adam7 interlacing included). A truncated,
  corrupt, or header-only PNG cannot pass: the arithmetic does not work out.
* **JPEG — structural completeness is proven; pixel validity is not.** The
  marker stream is walked in full: a frame header, at least one scan, non-empty
  entropy-coded data with correct byte-stuffing and restart handling, and a
  terminating ``EOI``. A header-only or truncated JPEG cannot pass. This does
  not verify Huffman tables decode to sensible pixels, which would require a
  full decoder; it is deliberately the container-level guarantee.

``test_portfolio_hq_owner_image_integrity.py`` cross-checks these verdicts
against a real decoder (Pillow, already present transitively via matplotlib) on
generated and deliberately damaged images, so the guarantees above are measured
against an independent implementation rather than asserted.
"""

from __future__ import annotations

import zlib

#: Accepted formats. Deliberately narrow — a format whose completeness we
#: cannot establish from its own bytes is a format we cannot honestly
#: quarantine as evidence.
SUPPORTED_MEDIA_TYPES = ("image/png", "image/jpeg")

#: Ceiling on the *decompressed* PNG raster implied by the IHDR header. Bounds
#: a decompression bomb: a small payload can declare enormous dimensions, and
#: without this the length check below would size its own buffer from
#: attacker-supplied numbers.
MAX_RAW_IMAGE_BYTES = 512 * 1024 * 1024

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_PNG_CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
_PNG_ALLOWED_DEPTHS = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8},
                       4: {8, 16}, 6: {8, 16}}
# Adam7 interlacing passes: (x_start, y_start, x_step, y_step).
_ADAM7_PASSES = ((0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 4, 4, 4),
                 (0, 2, 2, 4), (1, 2, 2, 2), (0, 1, 1, 2))

# Frame headers carrying dimensions. C4 (DHT), C8 (JPG) and CC (DAC) sit in the
# same 0xC0-0xCF range but are not frame headers.
_JPEG_SOF_MARKERS = frozenset(
    {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
)
_JPEG_SOI, _JPEG_EOI, _JPEG_SOS, _JPEG_TEM = 0xD8, 0xD9, 0xDA, 0x01


class ImageIntegrityError(Exception):
    """The payload is not an accepted, complete image.

    ``reason`` is one of the chart inbox's own closed rejection codes so the
    caller can surface it without re-deriving a classification:
    ``unsupported_media_type`` (not a format we accept at all) or
    ``corrupt_or_unreadable_image`` (right format, incomplete or damaged).
    """

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(detail)
        self.reason = reason
        self.detail = detail


def _corrupt(detail: str) -> ImageIntegrityError:
    return ImageIntegrityError("corrupt_or_unreadable_image", detail)


def sniff_media_type(data: bytes) -> str | None:
    """Media type implied by the payload's own leading bytes, or ``None``.

    The client's filename, extension and declared Content-Type are irrelevant
    here by design.
    """
    if data.startswith(_PNG_SIGNATURE):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    return None


# ── PNG ──────────────────────────────────────────────────────────────────────

def _png_raw_size(width: int, height: int, depth: int, colour_type: int,
                  interlace: int) -> int:
    """Exact uncompressed raster size the IHDR header implies.

    Each scanline carries one leading filter byte. Under Adam7 the image is
    seven independently-filtered reduced images, so the total is the sum of
    their sizes, not the non-interlaced figure.
    """
    channels = _PNG_CHANNELS[colour_type]

    def pass_bytes(pass_width: int, pass_height: int) -> int:
        if pass_width <= 0 or pass_height <= 0:
            return 0
        return pass_height * (1 + (pass_width * channels * depth + 7) // 8)

    if interlace == 0:
        return pass_bytes(width, height)
    total = 0
    for x_start, y_start, x_step, y_step in _ADAM7_PASSES:
        pass_width = (width - x_start + x_step - 1) // x_step if width > x_start else 0
        pass_height = (height - y_start + y_step - 1) // y_step if height > y_start else 0
        total += pass_bytes(pass_width, pass_height)
    return total


def _verify_png(data: bytes) -> tuple[int, int]:
    """Verify a complete, structurally legal PNG. Returns ``(width, height)``."""
    size = len(data)
    offset = len(_PNG_SIGNATURE)

    header: tuple[int, int, int, int, int] | None = None
    idat = bytearray()
    seen_types: list[bytes] = []
    idat_closed = False          # an IDAT run must be contiguous
    seen_iend = False

    while offset < size:
        if offset + 8 > size:
            raise _corrupt("the PNG ends inside a chunk header — it is truncated")
        length = int.from_bytes(data[offset:offset + 4], "big")
        chunk_type = data[offset + 4:offset + 8]
        if length > size:
            raise _corrupt("a PNG chunk declares a length larger than the file")
        end = offset + 8 + length
        if end + 4 > size:
            raise _corrupt("a PNG chunk is cut short — the file is truncated")
        payload = data[offset + 8:end]
        declared_crc = int.from_bytes(data[end:end + 4], "big")
        if zlib.crc32(chunk_type + payload) & 0xFFFFFFFF != declared_crc:
            raise _corrupt(
                f"the PNG {chunk_type.decode('ascii', 'replace')} chunk fails its "
                "own CRC — the file is damaged")

        if not seen_types and chunk_type != b"IHDR":
            raise _corrupt("the PNG does not begin with its IHDR header chunk")
        if seen_iend:
            raise _corrupt("the PNG carries data after its IEND terminator")

        if chunk_type == b"IHDR":
            if seen_types:
                raise _corrupt("the PNG carries more than one IHDR header")
            if length != 13:
                raise _corrupt("the PNG IHDR header is the wrong size")
            width, height, depth, colour_type, compression, filt, interlace = (
                int.from_bytes(payload[0:4], "big"),
                int.from_bytes(payload[4:8], "big"),
                payload[8], payload[9], payload[10], payload[11], payload[12],
            )
            if width <= 0 or height <= 0:
                raise _corrupt("the PNG declares a zero dimension")
            if colour_type not in _PNG_CHANNELS:
                raise _corrupt("the PNG declares an unknown colour type")
            if depth not in _PNG_ALLOWED_DEPTHS[colour_type]:
                raise _corrupt("the PNG declares an illegal bit-depth for its "
                               "colour type")
            if compression != 0 or filt != 0 or interlace not in (0, 1):
                raise _corrupt("the PNG declares an unsupported compression, "
                               "filter or interlace method")
            header = (width, height, depth, colour_type, interlace)
        elif chunk_type == b"IDAT":
            if idat_closed:
                raise _corrupt("the PNG image data is split by another chunk")
            idat += payload
        elif chunk_type == b"IEND":
            if length != 0:
                raise _corrupt("the PNG IEND terminator is malformed")
            seen_iend = True
        if chunk_type != b"IDAT" and idat:
            idat_closed = True

        seen_types.append(chunk_type)
        offset = end + 4

    if header is None:
        raise _corrupt("the PNG has no IHDR header chunk")
    if not seen_iend:
        raise _corrupt("the PNG has no IEND terminator — it is incomplete")
    if not idat:
        raise _corrupt("the PNG carries no image data (no IDAT chunk)")

    width, height, depth, colour_type, interlace = header
    if colour_type == 3 and b"PLTE" not in seen_types:
        raise _corrupt("the palette PNG has no PLTE palette chunk")

    expected = _png_raw_size(width, height, depth, colour_type, interlace)
    if expected > MAX_RAW_IMAGE_BYTES:
        raise _corrupt("the PNG declares dimensions too large to verify safely")

    # Actually decompress, bounded by the size the header implies. This is the
    # step a header-only or mid-IDAT-truncated file cannot survive.
    engine = zlib.decompressobj()
    try:
        raw = engine.decompress(bytes(idat), expected + 1)
        raw += engine.flush()
    except zlib.error as exc:
        raise _corrupt(f"the PNG image data will not decompress ({exc})") from exc
    if not engine.eof:
        raise _corrupt("the PNG image data stream is unterminated — the file is "
                       "truncated")
    if len(raw) != expected:
        raise _corrupt(
            f"the PNG image data is {len(raw):,} bytes but its header implies "
            f"{expected:,} — the file is incomplete or inconsistent")
    return width, height


# ── JPEG ─────────────────────────────────────────────────────────────────────

def _scan_entropy_coded_data(data: bytes, start: int) -> int:
    """Return the offset of the next real marker after a scan's payload.

    Inside entropy-coded data a literal ``0xFF`` byte is stuffed as ``0xFF 0x00``
    and restart markers (``0xFFD0``-``0xFFD7``) are interleaved; neither ends the
    scan. Anything else beginning ``0xFF`` does.
    """
    size = len(data)
    offset = start
    while offset < size:
        if data[offset] != 0xFF:
            offset += 1
            continue
        if offset + 1 >= size:
            raise _corrupt("the JPEG ends on a partial marker — it is truncated")
        following = data[offset + 1]
        if following == 0x00:          # stuffed literal 0xFF
            offset += 2
        elif following == 0xFF:        # fill byte
            offset += 1
        elif 0xD0 <= following <= 0xD7:  # restart marker
            offset += 2
        else:
            return offset
    raise _corrupt("the JPEG scan data is not terminated — the file is truncated")


def _verify_jpeg(data: bytes) -> tuple[int, int]:
    """Verify a complete JPEG marker stream. Returns ``(width, height)``."""
    size = len(data)
    offset = 2  # past SOI
    dimensions: tuple[int, int] | None = None
    scans = 0
    entropy_bytes = 0
    seen_eoi = False

    while offset < size:
        if data[offset] != 0xFF:
            raise _corrupt("the JPEG marker stream is out of step — the file is "
                           "damaged")
        while offset < size and data[offset] == 0xFF:
            offset += 1              # skip fill bytes
        if offset >= size:
            raise _corrupt("the JPEG ends on a partial marker — it is truncated")
        marker = data[offset]
        offset += 1

        if marker == _JPEG_EOI:
            seen_eoi = True
            break
        if marker == _JPEG_SOI or marker == _JPEG_TEM or 0xD0 <= marker <= 0xD7:
            continue                 # standalone markers carry no segment

        if offset + 2 > size:
            raise _corrupt("a JPEG segment header is cut short — the file is "
                           "truncated")
        segment_length = int.from_bytes(data[offset:offset + 2], "big")
        if segment_length < 2 or offset + segment_length > size:
            raise _corrupt("a JPEG segment is truncated or declares a bad length")
        segment = data[offset + 2:offset + segment_length]

        if marker in _JPEG_SOF_MARKERS:
            if len(segment) < 5:
                raise _corrupt("the JPEG frame header is too short")
            height = int.from_bytes(segment[1:3], "big")
            width = int.from_bytes(segment[3:5], "big")
            if width <= 0 or height <= 0:
                raise _corrupt("the JPEG declares a zero dimension")
            dimensions = (width, height)

        offset += segment_length

        if marker == _JPEG_SOS:
            scan_start = offset
            offset = _scan_entropy_coded_data(data, scan_start)
            entropy_bytes += offset - scan_start
            scans += 1

    if dimensions is None:
        raise _corrupt("the JPEG has no frame header — it carries no image")
    if scans == 0:
        raise _corrupt("the JPEG has no image scan — it is a header without an "
                       "image")
    if entropy_bytes == 0:
        raise _corrupt("the JPEG scan carries no image data")
    if not seen_eoi:
        raise _corrupt("the JPEG has no end-of-image marker — it is truncated")
    return dimensions


# ── public entry point ───────────────────────────────────────────────────────

def verify_complete_image(data: bytes) -> tuple[str, int, int]:
    """Verify the payload is a complete, accepted image.

    Returns ``(media_type, width, height)``. Raises ``ImageIntegrityError``
    carrying the chart inbox's own rejection reason. Never reads the filename,
    the extension, or any client-declared content type.
    """
    if not data:
        raise ImageIntegrityError("empty_payload", "the upload was empty")
    media_type = sniff_media_type(data)
    if media_type is None:
        raise ImageIntegrityError(
            "unsupported_media_type",
            "only PNG and JPEG chart images are accepted, decided by inspecting "
            "the file's own content")
    if media_type == "image/png":
        width, height = _verify_png(data)
    else:
        width, height = _verify_jpeg(data)
    return media_type, width, height
