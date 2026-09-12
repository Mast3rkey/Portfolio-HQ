"""Private owner-interface HTTP service — the one write-capable surface.

Relationship to the existing dashboard server
---------------------------------------------
``portfolio_hq.dashboard.server`` is unchanged by this unit and stays exactly
what it was: loopback-only, GET-only, serving one generated page, rejecting
every mutating method with 405. It is not rebound, wrapped, subclassed or
reused here.

This is a **separate** service with a **separate**, narrower job. It is the only
component in the repository that accepts a request body, and the only one that
writes bytes a client supplied. Keeping the two apart is the point: the
read-only dashboard cannot acquire an upload path by accident, and this service
cannot acquire portfolio-calculation authority by accident — it holds none.

What this service can and cannot reach
--------------------------------------
* It imports ``portfolio_hq.owner.export`` for ``load_export`` only — a JSON
  reader. It never imports ``allocate``, ``margin_state``, ``levels``, a
  brokerage client, or ``portfolio_hq.dashboard.model``, so it cannot compute a
  portfolio number even by mistake. ``test_portfolio_hq_owner_interface.py``
  asserts this from the module import graph.
* It reads exactly two paths: the presentation export file and the chart inbox
  directory. It never opens ``holdings.yaml``, ``targets.yaml``, ``gates.yaml``,
  ``governance/`` or ``intelligence/``.
* It writes exactly one place: beneath the configured chart inbox root, through
  ``chart_inbox.ingest``, which derives every path from a server-generated id.
* There is no order path, no brokerage call, no Stage-1 surface, and no route
  that mutates repository state.

Authentication is mandatory. The service refuses to start without a configured
owner token on **every** host, loopback included, so a misconfigured deployment
serves nothing rather than serving private data anonymously.
"""

from __future__ import annotations

import ipaddress
import json
import threading
from dataclasses import dataclass
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from . import auth as auth_mod
from . import chart_evidence, chart_inbox, render
from .export_io import load_export

#: Slack above the image ceiling for multipart framing and the small text
#: fields. A request larger than this is refused before its body is read.
_FIELD_SLACK_BYTES = 64 * 1024
MAX_REQUEST_BYTES = chart_inbox.MAX_UPLOAD_BYTES + _FIELD_SLACK_BYTES

_MAX_MULTIPART_PARTS = 8
_MAX_TEXT_FIELD_BYTES = 256
_READ_CHUNK = 64 * 1024

_SECURITY_HEADERS = (
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "no-referrer"),
    ("X-Frame-Options", "DENY"),
    ("Cache-Control", "no-store"),
    # No script source is allowed at all: the interface ships no JavaScript.
    ("Content-Security-Policy",
     "default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; "
     "form-action 'self'; base-uri 'none'; frame-ancestors 'none'"),
)


@dataclass(frozen=True)
class OwnerServiceConfig:
    """Everything the running service is allowed to touch."""

    token: str
    inbox_root: Path
    export_path: Path
    analysis_path: Path | None = None
    review_path: Path | None = None
    secure_cookie: bool = True

    @property
    def signer(self) -> auth_mod.SessionSigner:
        return auth_mod.SessionSigner(self.token)


def is_loopback_host(host: str) -> bool:
    if host in ("localhost", ""):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def build_config(
    *,
    inbox_root: Path | str,
    export_path: Path | str,
    host: str = "127.0.0.1",
    env: dict | None = None,
    analysis_path: Path | str | None = None,
    review_path: Path | str | None = None,
) -> OwnerServiceConfig:
    """Resolve configuration, or raise ``OwnerAuthNotConfigured``.

    The cookie is marked ``Secure`` unless the service is bound to loopback,
    where plain HTTP is the normal local case. Any non-loopback deployment is
    therefore expected to sit behind TLS termination, and its session cookie
    will not be sent over plain HTTP.
    """
    token = auth_mod.require_owner_token(env)
    return OwnerServiceConfig(
        token=token,
        inbox_root=Path(inbox_root),
        export_path=Path(export_path),
        analysis_path=Path(analysis_path) if analysis_path else None,
        review_path=Path(review_path) if review_path else None,
        secure_cookie=not is_loopback_host(host),
    )


# ── multipart/form-data (byte-exact, bounded) ────────────────────────────────

@dataclass(frozen=True)
class UploadedFile:
    filename: str | None
    content: bytes


def _boundary_from_content_type(content_type: str) -> bytes | None:
    if not content_type:
        return None
    head, _, params = content_type.partition(";")
    if head.strip().lower() != "multipart/form-data":
        return None
    for chunk in params.split(";"):
        key, _, value = chunk.partition("=")
        if key.strip().lower() != "boundary":
            continue
        value = value.strip().strip('"')
        if not value or len(value) > 200:
            return None
        return value.encode("latin-1", "ignore")
    return None


def _part_disposition(headers: bytes) -> tuple[str | None, str | None]:
    """Return ``(field_name, filename)`` from a part's own headers."""
    name = filename = None
    for line in headers.split(b"\r\n"):
        try:
            text = line.decode("utf-8", "replace")
        except Exception:  # pragma: no cover - decode never raises with replace
            continue
        key, _, value = text.partition(":")
        if key.strip().lower() != "content-disposition":
            continue
        for chunk in value.split(";")[1:]:
            attr, _, raw = chunk.partition("=")
            raw = raw.strip().strip('"')
            attr = attr.strip().lower()
            if attr == "name":
                name = raw
            elif attr == "filename":
                filename = raw
    return name, filename


def parse_multipart(body: bytes, content_type: str) -> dict[str, object]:
    """Split a multipart body into fields without touching payload bytes.

    Written explicitly rather than delegated to ``email``/``cgi``: the payload
    is a binary image whose SHA-256 the inbox records, so any line-ending
    normalisation a text-oriented parser might apply would silently corrupt the
    very bytes we promise to retain unchanged. This splitter copies payload
    slices verbatim.
    """
    boundary = _boundary_from_content_type(content_type)
    if boundary is None:
        return {}
    delimiter = b"\r\n--" + boundary
    # Prepending CRLF makes the first delimiter look like every other one.
    segments = (b"\r\n" + body).split(delimiter)
    fields: dict[str, object] = {}
    for segment in segments[1:]:
        if len(fields) >= _MAX_MULTIPART_PARTS:
            break
        if segment.startswith(b"--"):  # closing delimiter; epilogue follows
            break
        if not segment.startswith(b"\r\n"):
            continue  # malformed part framing — skip rather than guess
        head, sep, payload = segment[2:].partition(b"\r\n\r\n")
        if not sep:
            continue
        name, filename = _part_disposition(head)
        if not name:
            continue
        if filename is not None:
            fields[name] = UploadedFile(filename=filename, content=payload)
        else:
            fields[name] = payload[:_MAX_TEXT_FIELD_BYTES].decode("utf-8", "replace")
    return fields


# ── handler ──────────────────────────────────────────────────────────────────

def _make_handler(config: OwnerServiceConfig):
    # Duplicate detection is a read-then-write over the inbox directory, and
    # this server is threaded. Serialising intake keeps two simultaneous
    # uploads of the same image from each concluding "no duplicate exists" and
    # both storing a copy. Intake is rare and I/O-bound, so the contention cost
    # is irrelevant. (One process only: a multi-instance deployment would need
    # a shared lock, which this single-owner interface does not use.)
    intake_lock = threading.Lock()

    class OwnerHandler(BaseHTTPRequestHandler):
        server_version = "PortfolioHQOwner/1.0"
        protocol_version = "HTTP/1.1"
        throttle = auth_mod.LoginThrottle()

        # ── plumbing ───────────────────────────────────────────────────────
        def _send(self, status: int, body: bytes, content_type: str,
                  extra_headers: tuple[tuple[str, str], ...] = ()) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            for key, value in _SECURITY_HEADERS:
                self.send_header(key, value)
            for key, value in extra_headers:
                self.send_header(key, value)
            if self.close_connection:
                # Advertise the close rather than just dropping the socket, so
                # a client is not left guessing why the connection ended.
                self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _html(self, status: int, markup: str,
                  extra_headers: tuple[tuple[str, str], ...] = ()) -> None:
            self._send(status, markup.encode("utf-8"),
                       "text/html; charset=utf-8", extra_headers)

        def _redirect(self, location: str,
                      extra_headers: tuple[tuple[str, str], ...] = ()) -> None:
            self._send(303, b"", "text/plain; charset=utf-8",
                       (("Location", location), *extra_headers))

        def _deny(self, status: int, message: str) -> None:
            # A denial is terminal, and several denial paths (an unknown POST
            # route, a rejected method) answer without draining the request
            # body. Closing the connection removes the whole class of
            # keep-alive desynchronisation that leftover body bytes would
            # otherwise cause on the next request.
            self.close_connection = True
            # Keep the navigation for a signed-in owner: a 404 should not look
            # like being signed out.
            self._html(status, render.error_page(
                status, message, signed_in=self._authenticated()))

        def _cookie_header(self, value: str, *, max_age: int) -> tuple[str, str]:
            parts = [
                f"{auth_mod.SESSION_COOKIE_NAME}={value}",
                "Path=/",
                "HttpOnly",
                "SameSite=Strict",
                f"Max-Age={max_age}",
            ]
            if config.secure_cookie:
                parts.append("Secure")
            return ("Set-Cookie", "; ".join(parts))

        def _identity(self) -> str:
            try:
                return str(self.client_address[0])
            except Exception:  # pragma: no cover - defensive
                return "unknown"

        def _authenticated(self) -> bool:
            raw = self.headers.get("Cookie")
            if not raw:
                return False
            try:
                jar = SimpleCookie()
                jar.load(raw)
            except Exception:
                return False
            morsel = jar.get(auth_mod.SESSION_COOKIE_NAME)
            if morsel is None:
                return False
            return config.signer.verify(morsel.value)

        def _same_origin(self) -> bool:
            """Reject a cross-site POST.

            ``SameSite=Strict`` already stops a browser sending the session
            cookie cross-site; this is the belt-and-braces server-side check
            for the case where an ``Origin`` header is present and disagrees
            with the host we were addressed as.
            """
            origin = self.headers.get("Origin")
            if not origin:
                return True  # no Origin: not a cross-site browser form post
            host = (self.headers.get("Host") or "").strip()
            try:
                parsed = urlsplit(origin)
            except ValueError:
                return False
            return bool(parsed.netloc) and parsed.netloc == host

        def _read_body(self) -> bytes | None:
            raw_length = self.headers.get("Content-Length")
            if raw_length is None:
                return None
            try:
                length = int(raw_length)
            except ValueError:
                return None
            if length < 0 or length > MAX_REQUEST_BYTES:
                return None
            chunks: list[bytes] = []
            remaining = length
            while remaining > 0:
                chunk = self.rfile.read(min(_READ_CHUNK, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            body = b"".join(chunks)
            return body if len(body) == length else None

        def _export(self) -> dict | None:
            return load_export(config.export_path)

        # ── routing ────────────────────────────────────────────────────────
        def do_GET(self):  # noqa: N802 (stdlib naming)
            path = urlsplit(self.path).path

            if path == "/healthz":
                # Liveness for a private host's health checker. Deliberately
                # carries no portfolio, chart, provenance or configuration
                # detail, and needs no authentication.
                self._send(200, b'{"status":"ok"}\n', "application/json")
                return

            if path == "/login":
                if self._authenticated():
                    self._redirect("/")
                    return
                self._html(200, render.login_page())
                return

            if path == "/logout":
                self._redirect("/login", (self._cookie_header("", max_age=0),))
                return

            if not self._authenticated():
                self._redirect("/login")
                return

            inbox = config.inbox_root
            if path == "/":
                self._html(200, render.home_page(self._export(),
                                                 chart_inbox.inbox_summary(inbox)))
            elif path == "/portfolio":
                self._html(200, render.portfolio_page(self._export()))
            elif path == "/research":
                self._html(200, render.research_page(self._export()))
            elif path == "/charts":
                self._html(200, render.charts_page(self._export(),
                                                   chart_inbox.list_records(inbox),
                                                   evidence=chart_evidence.reviewed_evidence(
                                                       inbox, config.analysis_path, config.review_path)))
            elif path.startswith("/charts/image/"):
                self._serve_chart_image(path[len("/charts/image/"):])
            else:
                self._deny(404, "There is no page at that address.")

        def do_HEAD(self):  # noqa: N802
            self.do_GET()

        def do_POST(self):  # noqa: N802
            path = urlsplit(self.path).path
            if path == "/login":
                self._handle_login()
                return
            if not self._authenticated():
                # Answered without reading the body, so close rather than leave
                # the unread payload to be misparsed as the next request.
                self.close_connection = True
                self._redirect("/login")
                return
            if path == "/charts/upload":
                self._handle_upload()
                return
            self._deny(404, "There is no page at that address.")

        # Every other method: this service has exactly two verbs.
        def do_PUT(self):  # noqa: N802
            self._deny(405, "This interface accepts only GET and POST.")

        do_DELETE = do_PATCH = do_OPTIONS = do_PUT  # noqa: N815

        # ── handlers ───────────────────────────────────────────────────────
        def _handle_login(self):
            if not self._same_origin():
                self._deny(403, "Cross-site form submissions are refused.")
                return
            identity = self._identity()
            if self.throttle.locked_out(identity):
                self.close_connection = True  # body deliberately not read
                self._html(429, render.login_page(locked=True))
                return
            body = self._read_body()
            if body is None:
                # The body was absent, unreadable, or declared larger than we
                # accept. We did not drain it, so this connection cannot be
                # reused for a further request.
                self.close_connection = True
                self._deny(400, "The sign-in request could not be read.")
                return
            supplied = None
            content_type = self.headers.get("Content-Type", "")
            if content_type.startswith("application/x-www-form-urlencoded"):
                from urllib.parse import parse_qs

                parsed = parse_qs(body[:_MAX_TEXT_FIELD_BYTES * 4].decode("utf-8", "replace"))
                values = parsed.get("token") or []
                supplied = values[0] if values else None
            else:
                field = parse_multipart(body, content_type).get("token")
                supplied = field if isinstance(field, str) else None

            if not auth_mod.token_matches(supplied, config.token):
                self.throttle.record_failure(identity)
                self._html(401, render.login_page(error="That token was not accepted."))
                return
            self.throttle.record_success(identity)
            session = config.signer.issue()
            self._redirect("/", (self._cookie_header(
                session, max_age=auth_mod.SESSION_TTL_SECONDS),))

        def _handle_upload(self):
            if not self._same_origin():
                self._deny(403, "Cross-site form submissions are refused.")
                return
            body = self._read_body()
            if body is None:
                # Refused on the declared Content-Length, before reading a
                # single byte of payload. Nothing was buffered and nothing was
                # written; the connection closes because the body was not drained.
                self.close_connection = True
                self._deny(413, "The upload was missing, unreadable, or larger "
                                "than this interface accepts.")
                return
            fields = parse_multipart(body, self.headers.get("Content-Type", ""))
            uploaded = fields.get("chart")
            if not isinstance(uploaded, UploadedFile):
                self._charts_flash({"kind": "rejected",
                                    "reason": "empty_payload",
                                    "message": "No chart file was included."}, 400)
                return

            export = self._export()
            request = (export or {}).get("chart_request") or {}
            allowed_tickers = frozenset(request.get("eligible_tickers") or ())
            allowed_timeframes = frozenset(request.get("accepted_timeframes") or ())
            ticker = fields.get("ticker") if isinstance(fields.get("ticker"), str) else None
            timeframe = (fields.get("timeframe")
                         if isinstance(fields.get("timeframe"), str) else None)

            try:
                with intake_lock:
                    record = chart_inbox.ingest(
                        config.inbox_root,
                        uploaded.content,
                        display_filename=uploaded.filename,
                        declared_ticker=ticker or None,
                        declared_timeframe=timeframe or None,
                        allowed_tickers=allowed_tickers or None,
                        allowed_timeframes=allowed_timeframes or None,
                    )
            except chart_inbox.ChartIntakeRejected as rejected:
                self._charts_flash({"kind": "rejected",
                                    "reason": rejected.reason,
                                    "message": rejected.message}, 400)
                return
            except chart_inbox.ChartInboxStorageError as failure:
                # Storage is broken on this host. Say so plainly instead of
                # implying the chart was safely received.
                self._charts_flash({
                    "kind": "rejected",
                    "reason": "storage_failure",
                    "message": ("The chart could not be stored on this host, so "
                                "it was not received. Check the inbox volume."),
                }, 500)
                self.log_error("chart inbox storage failure: %s", failure)
                return

            if record.get("state") == chart_inbox.STATE_DUPLICATE:
                flash = {"kind": "duplicate",
                         "message": ("This exact image was already received, so it "
                                     "was recorded as a duplicate and not stored "
                                     "a second time.")}
            else:
                flash = {"kind": "accepted",
                         "message": ("The chart is stored and quarantined as "
                                     "unreviewed evidence. It changes nothing on "
                                     "its own.")}
            self._charts_flash(flash, 200)

        def _charts_flash(self, flash: dict, status: int) -> None:
            self._html(status, render.charts_page(
                self._export(), chart_inbox.list_records(config.inbox_root),
                evidence=chart_evidence.reviewed_evidence(
                    config.inbox_root, config.analysis_path, config.review_path),
                flash=flash))

        def _serve_chart_image(self, intake_id: str) -> None:
            """Return one retained original so a reviewer can actually look at it.

            The path is rebuilt inside ``chart_inbox`` from a strictly validated
            id; nothing from the URL reaches the filesystem uninspected, and a
            malformed or unknown id is a plain 404.
            """
            found = chart_inbox.read_image_bytes(config.inbox_root, intake_id)
            if found is None:
                self._deny(404, "No retained chart image with that reference.")
                return
            data, media_type = found
            self._send(200, data, media_type,
                       (("Content-Disposition", "inline"),))

        def log_message(self, fmt, *args):  # keep the console quiet-ish
            return

    return OwnerHandler


def serve(
    *,
    inbox_root: Path | str,
    export_path: Path | str,
    host: str = "127.0.0.1",
    port: int = 8080,
    env: dict | None = None,
    analysis_path: Path | str | None = None,
    review_path: Path | str | None = None,
) -> None:
    """Start the private owner interface (blocking). Ctrl-C to stop."""
    config = build_config(inbox_root=inbox_root, export_path=export_path,
                          host=host, env=env, analysis_path=analysis_path,
                          review_path=review_path)
    Path(config.inbox_root).mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), _make_handler(config))
    bound_host, bound_port = httpd.server_address[0], httpd.server_address[1]
    print(f"Portfolio-HQ private owner interface on http://{bound_host}:{bound_port}")
    print(f"  chart inbox:        {Path(config.inbox_root).resolve()}")
    print(f"  presentation export: {Path(config.export_path).resolve()}"
          f"{'' if Path(config.export_path).is_file() else '  (not built yet)'}")
    print("  authentication:     required (PORTFOLIO_HQ_OWNER_TOKEN)")
    if config.secure_cookie:
        print("  NOTE: bound to a non-loopback address. Terminate TLS in front of "
              "this process — the session cookie is marked Secure and will not "
              "be sent over plain HTTP.")
    print("  Recommendation-only. No brokerage connection, no order path.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping the owner interface.")
    finally:
        httpd.server_close()


def healthz_payload() -> bytes:
    """The exact body ``/healthz`` returns — exposed for tests."""
    return json.dumps({"status": "ok"}).encode("utf-8") + b"\n"
