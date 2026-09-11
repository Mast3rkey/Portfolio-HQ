"""Structural completeness verification for accepted chart images.

Why this exists
---------------
Sniffing a magic number and reading a dimension header proves a payload
*starts* like an image. It does not prove the uploaded bytes form a complete,
usable one. A chart inbox that stores an evidence file a later reviewer
cannot open has failed at its one job, so acceptance is decided here on the
whole byte stream rather than on its first few fields.

Why standard library only
-------------------------
A full decoder is not needed to answer "are these bytes complete", and pulling
one in would be the wrong trade twice over: it would put a large native
image-parsing library directly on an untrusted-input boundary, and it would
break the hosted service's standard-library-only property, which the
provider-neutral deployment contract depends on. Everything below uses
``zlib`` and nothing else.

What each check actually proves — stated precisely, because the difference
matters for an evidence-receipt boundary:

* **PNG — completeness is genuinely proven.** Every chunk's CRC-32 is verified,
  chunk ordering and the terminal ``IEND`` are required, and the concatenated
  ``IDAT`` stream is actually decompressed and its length checked against the
  size the ``IHDR`` header implies (Adam7 interlacing included). A truncated,
  corrupt, or header-only PNG cannot pass: the arithmetic does not work out.

**JPEG is not accepted, and the reason is worth stating plainly.** Earlier
revisions of this module admitted JPEG on a hand-written structural check, then
tightened that check twice under review. The check could validate every frame
and scan header field, every table declaration and every marker boundary — and
still not establish the one thing that matters, because a JPEG's image lives in
a Huffman-coded bitstream that only a decoder can read. Structurally coherent
metadata can carry an unusable raster.

That is not a hypothetical. A 141-byte payload declaring a 65535x65535 frame
with one entropy byte satisfied every structural rule and was refused outright
by a real decoder as a decompression bomb. PNG has no such gap: ``IHDR``'s
dimensions are checked against ``MAX_RAW_IMAGE_BYTES`` and then *proved* by
decompressing the image data, because the format's compression is ``zlib`` and
``zlib`` is in the standard library. JPEG has no standard-library equivalent, so
the only honest options were to ship a home-grown JPEG codec on an
untrusted-input boundary, add a native decoder to a service whose whole
deployment contract rests on being standard-library-only, or stop claiming a
guarantee that could not be met. This module takes the third.

JPEG bytes are therefore still *recognised* — so a ``.png`` filename wrapping
JPEG content is refused for what it actually is, and the owner is told to
convert rather than left guessing — but never admitted. Converting a JPEG chart
to PNG before intake is a local preparation step, documented in
``docs/PORTFOLIO_HQ_OWNER_INTERFACE.md``; the hosted service never transcodes.

``test_portfolio_hq_owner_image_integrity.py`` cross-checks these verdicts
against a real decoder (Pillow, already present transitively via matplotlib) on
generated and deliberately damaged images, so the guarantees above are measured
against an independent implementation rather than asserted.
"""

from __future__ import annotations

import zlib

#: Accepted formats. Exactly one, deliberately — a format whose completeness we
#: cannot establish from its own bytes is a format we cannot honestly
#: quarantine as evidence, and PNG is the only one we can.
SUPPORTED_MEDIA_TYPES = ("image/png",)

#: Recognised but not accepted. Sniffing JPEG is what lets a ``.png`` filename
#: wrapping JPEG bytes be refused for what it is.
RECOGNISED_UNSUPPORTED_MEDIA_TYPES = ("image/jpeg",)

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


def _unsupported(detail: str) -> ImageIntegrityError:
    """The payload is a format this inbox does not accept.

    Deliberately *not* ``corrupt_or_unreadable_image``: the file may be
    perfectly sound. Saying so plainly is the point — the owner needs to know to
    convert it, not to think their chart is broken.
    """
    return ImageIntegrityError("unsupported_media_type", detail)


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
    if media_type == "image/jpeg":
        raise _unsupported(
            "this file's own bytes are JPEG, whatever it is named, and the "
            "chart inbox accepts PNG only — convert the chart to PNG before "
            "uploading it")
    if media_type != "image/png":
        raise _unsupported(
            "the chart inbox accepts PNG only, decided by inspecting the file's "
            "own content — re-save or convert the chart as PNG")
    width, height = _verify_png(data)
    return media_type, width, height
