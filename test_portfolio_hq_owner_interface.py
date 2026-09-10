"""Focused, adversarial tests for the private owner interface.

Covers the trust boundary between the read-only dashboard and the new
write-capable owner service, fail-closed authentication, session handling,
CSRF and method restrictions, HTTP-level chart intake, the owner-facing
presentation contract (responsive, offline, recommendation-only, honest about
unavailable values), the canonical-reuse rule for the presentation export, and
proof that the historical dashboard surface is unchanged.
"""

from __future__ import annotations

import ast
import hashlib
import http.client
import json
import subprocess
import sys
import threading
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from portfolio_hq.owner import auth as auth_mod
from portfolio_hq.owner import chart_inbox as inbox_mod
from portfolio_hq.owner import render as render_mod
from portfolio_hq.owner import service as service_mod
from portfolio_hq.owner.cli import main as owner_cli_main
from portfolio_hq.owner.export_io import (
    EXPORT_SCHEMA_VERSION,
    load_export,
    write_export,
)
from test_portfolio_hq_owner_chart_inbox import jpeg_bytes, png_bytes

REPO_ROOT = Path(__file__).resolve().parent
TOKEN = "owner-test-token-with-plenty-of-entropy-0123456789"
FIXED_NOW = datetime(2026, 9, 10, 12, 0, 0, tzinfo=timezone.utc)


# ── fixtures ─────────────────────────────────────────────────────────────────

def _sample_export() -> dict:
    return {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "meta": {
            "generated_at": "2026-09-10T12:00:00Z",
            "repo_name": "Portfolio-HQ",
            "source_commit": "a" * 40,
            "source_commit_short": "aaaaaaa",
            "branch": "main",
            "git_available": True,
            "worktree_dirty": False,
            "worktree_dirty_path_count": 0,
        },
        "input_digests": [
            {"path": "holdings.yaml", "exists": True, "sha256": "b" * 64,
             "size_bytes": 10},
        ],
        "attention": {
            "blockers": [{"title": "A blocking thing", "detail": "detail one"}],
            "warnings": [{"title": "A warning thing", "detail": "detail two"}],
            "infos": [],
        },
        "recommendation_state": {
            "allocation_available": False,
            "unavailable_reasons": ["no live market data in the offline export"],
            "disclosure": "Portfolio-HQ is recommendation-only.",
        },
        "capital": {
            "available": True,
            "reason": None,
            "cash": {"state": "stale", "usable_as_current": False, "balance": 1041.23,
                     "synced_at": "2026-08-01", "age_days": 40,
                     "reason": "cash synced 40d ago"},
            "margin_observation": {"state": "stale", "usable_as_current": False,
                                   "debt": 0.0, "buffer_pct": 100.0,
                                   "synced_at": "2026-07-31", "age_days": 41,
                                   "age_unverifiable": False, "stale": True,
                                   "leverage_cap": 1.8, "buffer_floor_pct": 30.0,
                                   "below_buffer_floor": False,
                                   "reason": "margin synced 41d ago"},
            "protected_percentages": {"cash_pct": 1.0, "reserve_pct": 4.0,
                                      "unreconciled_pct": 0.75,
                                      "static_protected_pct": 5.75,
                                      "gated_target_pct": 0.0,
                                      "destination_total_pct": 99.25,
                                      "note": "percent of book"},
            "book": {"available": False,
                     "blocked_by": ["CASH STATE: stale", "VALUATION: no feed"],
                     "reason": "CASH STATE: stale; VALUATION: no feed",
                     "value": None},
        },
        "holdings_effective": {"date": "2026-07-31", "source": "margin sync date"},
        "level1": {
            "available": True, "reason": None,
            "status": "CURRENT_ACCEPTED_POLICY_SNAPSHOT",
            "policy_source": "targets.yaml",
            "policy_basis": ["PHQ-2026-02"],
            "units": "percent_of_book",
            "sleeves_pct": {"direct_equity": "63.25", "broad_market_funds": "23.00",
                            "gold_defensive": "4.00", "crypto": "4.00",
                            "cash_and_reserve": "5.00", "unallocated": "0.75"},
            "members": {"direct_equity": ["NVDA"], "crypto": ["BTC"]},
            "reconciliation": {"assigned_pct": "99.25", "unallocated_pct": "0.75",
                               "total_pct": "100.00"},
        },
        "level2": [
            {"ticker": "NVDA", "asset_class": "equity", "sleeve": "direct_equity",
             "target_pct": 4.5, "gated": False, "gate_status": None,
             "gate_allow_add": None, "gate_authority": None, "gate_next": None,
             "held": True, "held_quantity": 1.86, "held_kind": "equity"},
            {"ticker": "TSLA", "asset_class": "equity", "sleeve": "direct_equity",
             "target_pct": 0.75, "gated": True, "gate_status": "hold_no_add",
             "gate_allow_add": False, "gate_authority": "PHQ-2026-01",
             "gate_next": "await review", "held": False, "held_quantity": None,
             "held_kind": None},
        ],
        "concentration": {
            "clusters": [{"name": "semis", "cap_pct": 25.0, "tickers": ["NVDA"]}],
            "single_issuer_ceiling_pct": 8.0, "ai_platform_ceiling_pct": 40.0,
            "ai_platform_measured_pct": 40.03, "crypto_sleeve_pct": 4.0,
        },
        "gates": [{"ticker": "TSLA", "status": "hold_no_add",
                   "authority": "PHQ-2026-01", "allow_add": False,
                   "holds_existing_shares": False, "next_gate": "await review"}],
        "intelligence": {
            "available": True, "note": None, "company_records": 53,
            "company_notes": 53, "theme_records": 2, "companies_scanned": 53,
            "overdue_reviews": [{"ticker": "LLY", "detail": "review due 2026-08-31"}],
            "schema_invalid": [], "role_drift": [], "freshness_rows": 9,
            "monitoring_enabled_rows": 0,
        },
        "decisions_index": [
            {"decision_id": "PHQ-2026-02", "date": "2026-07-31",
             "status": "Accepted", "category": "portfolio_architecture"},
        ],
        "workstreams": [
            {"id": "WS-0014", "title": "Cross-asset synthesis",
             "status": "proposed", "priority": "secondary",
             "next_action": "await authorization"},
        ],
        "chart_request": {
            "eligible_tickers": ["BTC", "NVDA", "TSLA"],
            "accepted_timeframes": ["1D"],
            "requested_batch_specified": False,
            "instructions": "Capture the whole chart window.",
            "note": "No production chart batch has been requested.",
        },
        "boundaries": {"recommendation_only": True, "places_orders": False,
                       "brokerage_connected": False, "reads_live_account": False,
                       "arms_or_executes_stage1": False,
                       "mutates_repository_state": False},
    }


class Client:
    """Minimal HTTP client bound to one running owner service."""

    def __init__(self, port: int) -> None:
        self.port = port
        self.cookie: str | None = None

    def request(self, method: str, path: str, body: bytes | None = None,
                headers: dict | None = None, *, use_cookie: bool = True):
        sent = dict(headers or {})
        if use_cookie and self.cookie:
            sent.setdefault("Cookie", self.cookie)
        if body is not None:
            sent.setdefault("Content-Length", str(len(body)))
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=20)
        try:
            conn.request(method, path, body=body, headers=sent)
            response = conn.getresponse()
            payload = response.read()
            return response.status, dict(response.getheaders()), payload
        finally:
            conn.close()

    def sign_in(self, token: str = TOKEN):
        body = f"token={token}".encode()
        status, headers, _ = self.request(
            "POST", "/login", body,
            {"Content-Type": "application/x-www-form-urlencoded"}, use_cookie=False)
        raw = headers.get("Set-Cookie", "")
        if "phq_owner_session=" in raw:
            self.cookie = raw.split(";")[0]
        return status, headers


def multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    boundary = "----phqtestboundary42"
    parts = []
    for key, value in fields.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"'
            f"\r\n\r\n{value}\r\n".encode()
        )
    for key, (filename, data) in files.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"; '
            f'filename="{filename}"\r\nContent-Type: application/octet-stream'
            f"\r\n\r\n".encode() + data + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


@pytest.fixture
def owner_env(tmp_path: Path):
    """A configured, running owner service plus its inbox and export paths."""
    inbox = tmp_path / "inbox"
    export_path = tmp_path / "export.json"
    write_export(export_path, _sample_export())
    config = service_mod.build_config(
        inbox_root=inbox, export_path=export_path, host="127.0.0.1",
        env={auth_mod.TOKEN_ENV_VAR: TOKEN})
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), service_mod._make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield {
            "client": Client(httpd.server_address[1]),
            "inbox": inbox,
            "export_path": export_path,
            "config": config,
        }
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


@pytest.fixture
def signed_in(owner_env):
    owner_env["client"].sign_in()
    return owner_env


# ── the trust boundary ───────────────────────────────────────────────────────

def test_hosted_service_imports_no_investment_code():
    """A fresh interpreter importing the service must not pull in investment code.

    Run as a subprocess so no other test's imports can mask a real leak. This
    is the boundary the whole design rests on: the hosted, write-capable half
    cannot compute a portfolio number because it cannot reach the code that
    would.
    """
    program = (
        "import portfolio_hq.owner.service, sys; "
        "print(','.join(sorted(m for m in ("
        "'allocate','alpaca_client','margin_state','levels','pandas','numpy',"
        "'yfinance','earnings','crypto','indicators','regime_gate',"
        "'level1_policy_summary','portfolio_hq.dashboard.model',"
        "'portfolio_hq.dashboard.render','portfolio_hq.owner.export'"
        ") if m in sys.modules)))"
    )
    result = subprocess.run([sys.executable, "-c", program], cwd=str(REPO_ROOT),
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "", (
        f"the hosted service leaked imports: {result.stdout.strip()}")


@pytest.mark.parametrize("module_name", [
    "portfolio_hq.owner.service",
    "portfolio_hq.owner.render",
    "portfolio_hq.owner.chart_inbox",
    "portfolio_hq.owner.auth",
    "portfolio_hq.owner.export_io",
])
def test_runtime_modules_declare_no_investment_imports(module_name: str):
    module = sys.modules[module_name] if module_name in sys.modules else None
    if module is None:  # pragma: no cover - imported at module scope above
        __import__(module_name)
        module = sys.modules[module_name]
    tree = ast.parse(Path(module.__file__).read_text())
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    forbidden = {"allocate", "alpaca_client", "margin_state", "levels", "pandas",
                 "yfinance", "earnings", "indicators", "regime_gate",
                 "level1_policy_summary"}
    assert not (roots & forbidden), f"{module_name} imports {roots & forbidden}"


def test_owner_package_import_stays_lazy():
    """Importing the package must not drag the build-time half in with it."""
    program = (
        "import portfolio_hq.owner, sys; "
        "print('LEAK' if 'portfolio_hq.owner.export' in sys.modules else 'clean'); "
        "print(callable(portfolio_hq.owner.build_owner_export))"
    )
    result = subprocess.run([sys.executable, "-c", program], cwd=str(REPO_ROOT),
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == ["clean", "True"]


def test_owner_package_getattr_rejects_unknown_names():
    import portfolio_hq.owner as owner_pkg

    with pytest.raises(AttributeError):
        owner_pkg.definitely_not_a_real_symbol


# ── the existing dashboard is unchanged ──────────────────────────────────────

def test_dashboard_server_still_rejects_every_mutating_method(tmp_path: Path):
    from portfolio_hq.dashboard.server import _make_handler as dashboard_handler

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), dashboard_handler(REPO_ROOT))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        client = Client(httpd.server_address[1])
        for method in ("POST", "PUT", "DELETE", "PATCH"):
            status, _, _ = client.request(method, "/", b"", {})
            assert status == 405, f"dashboard accepted {method}"
        status, _, _ = client.request("GET", "/charts/upload")
        assert status == 404, "dashboard grew an upload route"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def test_dashboard_cli_still_refuses_a_non_loopback_bind():
    from portfolio_hq.dashboard.cli import build_parser

    parser = build_parser()
    for host in ("0.0.0.0", "10.0.0.5", "example.com"):
        with pytest.raises(SystemExit):
            parser.parse_args(["serve", "--host", host])


def test_dashboard_modules_do_not_import_the_owner_package():
    dashboard_dir = REPO_ROOT / "portfolio_hq" / "dashboard"
    for path in sorted(dashboard_dir.glob("*.py")):
        source = path.read_text()
        assert "owner" not in {
            node.module.split(".")[-1]
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.ImportFrom) and node.module
        }, f"{path.name} reaches into the owner package"


# ── authentication is mandatory and fail-closed ─────────────────────────────

def test_missing_token_refuses_to_configure_the_service(tmp_path: Path):
    with pytest.raises(auth_mod.OwnerAuthNotConfigured):
        service_mod.build_config(inbox_root=tmp_path / "i",
                                 export_path=tmp_path / "e.json",
                                 host="0.0.0.0", env={})


def test_missing_token_refuses_even_on_loopback(tmp_path: Path):
    """No 'it's only localhost' exemption: unconfigured means it does not run."""
    with pytest.raises(auth_mod.OwnerAuthNotConfigured):
        service_mod.build_config(inbox_root=tmp_path / "i",
                                 export_path=tmp_path / "e.json",
                                 host="127.0.0.1", env={})


@pytest.mark.parametrize("value", ["", "   ", "short", "x" * 31])
def test_weak_or_absent_tokens_are_refused(value: str):
    with pytest.raises(auth_mod.OwnerAuthNotConfigured):
        auth_mod.require_owner_token({auth_mod.TOKEN_ENV_VAR: value})


def test_token_of_minimum_length_is_accepted():
    token = "y" * auth_mod.MIN_TOKEN_LENGTH
    assert auth_mod.require_owner_token({auth_mod.TOKEN_ENV_VAR: token}) == token


def test_no_owner_token_is_committed_anywhere_in_the_repository():
    """No tracked file may assign a real-looking value to the owner token.

    Judged by content rather than by path: documentation legitimately shows
    ``PORTFOLIO_HQ_OWNER_TOKEN="$(python -c ...)"``, which generates a secret
    rather than containing one. What must never appear is a literal long enough
    to *be* a usable token.
    """
    import re

    hits = subprocess.run(
        ["git", "grep", "-nI", "-e", f"{auth_mod.TOKEN_ENV_VAR}="],
        cwd=str(REPO_ROOT), capture_output=True, text=True)
    assert hits.returncode in (0, 1), hits.stderr

    literal = re.compile(r"[A-Za-z0-9_\-]{%d,}" % auth_mod.MIN_TOKEN_LENGTH)
    offenders = []
    for line in hits.stdout.splitlines():
        _, _, text = line.partition(":")
        _, _, text = text.partition(":")
        assignment = text.split(f"{auth_mod.TOKEN_ENV_VAR}=", 1)[-1]
        # Strip the variable name itself, which is longer than the threshold.
        assignment = assignment.replace(auth_mod.TOKEN_ENV_VAR, "")
        if literal.search(assignment):
            offenders.append(line)
    assert offenders == [], f"a token-shaped literal is committed: {offenders}"


def test_concurrent_identical_uploads_store_only_one_copy(signed_in, monkeypatch):
    """Duplicate detection must hold under the threaded server.

    Duplicate detection is a read-then-write, so a naive implementation races:
    two simultaneous uploads of the same image can both conclude "no duplicate
    exists" and both store a copy. A plain thread burst does not reliably
    interleave inside that window, so the window is widened deterministically —
    the duplicate lookup is made slow — and the intake lock is what must still
    make the outcome correct. Without the lock this test fails; with it, passes.
    """
    import time

    real_lookup = inbox_mod.find_by_content_hash

    def slow_lookup(*args, **kwargs):
        result = real_lookup(*args, **kwargs)
        time.sleep(0.15)   # widen the read-then-write window
        return result

    monkeypatch.setattr(inbox_mod, "find_by_content_hash", slow_lookup)

    image = png_bytes(37, 23)
    body, content_type = multipart({}, {"chart": ("race.png", image)})
    results: list[int] = []
    results_lock = threading.Lock()
    start = threading.Barrier(6)

    def upload():
        client = Client(signed_in["client"].port)
        client.cookie = signed_in["client"].cookie
        start.wait(timeout=20)
        status, _, _ = client.request("POST", "/charts/upload", body,
                                      {"Content-Type": content_type})
        with results_lock:
            results.append(status)

    threads = [threading.Thread(target=upload) for _ in range(6)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=60)

    assert len(results) == 6 and set(results) == {200}, results
    stored = list((signed_in["inbox"] / "charts").rglob("original.*"))
    assert len(stored) == 1, f"{len(stored)} copies of identical content stored"
    records = inbox_mod.list_records(signed_in["inbox"])
    assert len(records) == 6
    assert sum(1 for r in records
               if r["state"] == inbox_mod.STATE_QUARANTINED) == 1


def test_cli_serve_fails_closed_without_a_token(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.delenv(auth_mod.TOKEN_ENV_VAR, raising=False)
    code = owner_cli_main(["serve", "--export", str(tmp_path / "e.json"),
                           "--inbox", str(tmp_path / "inbox")])
    assert code == 2
    assert auth_mod.TOKEN_ENV_VAR in capsys.readouterr().err
    assert not (tmp_path / "inbox").exists(), "a refused start must create nothing"


def test_session_values_cannot_be_forged_or_extended():
    signer = auth_mod.SessionSigner(TOKEN)
    value = signer.issue(now=1000.0, ttl_seconds=100)
    assert signer.verify(value, now=1050.0) is True
    assert signer.verify(value, now=1101.0) is False, "expired value accepted"

    expiry, signature = value.split(".")
    forged = f"{int(expiry) + 10_000}.{signature}"
    assert signer.verify(forged, now=1050.0) is False, "expiry extension accepted"
    assert signer.verify(f"{expiry}.{'0' * 64}", now=1050.0) is False
    for junk in ("", "abc", "not.a.session", None, 12345, "9999999999.x"):
        assert signer.verify(junk, now=1050.0) is False


def test_rotating_the_token_invalidates_outstanding_sessions():
    old = auth_mod.SessionSigner(TOKEN).issue(now=1000.0)
    assert auth_mod.SessionSigner("rotated-" + TOKEN).verify(old, now=1001.0) is False


def test_token_comparison_rejects_non_strings_and_near_misses():
    assert auth_mod.token_matches(TOKEN, TOKEN) is True
    assert auth_mod.token_matches(TOKEN + "x", TOKEN) is False
    assert auth_mod.token_matches("", TOKEN) is False
    assert auth_mod.token_matches(None, TOKEN) is False
    assert auth_mod.token_matches(b"bytes", TOKEN) is False


def test_login_throttle_locks_out_then_recovers():
    throttle = auth_mod.LoginThrottle(max_attempts=3, lockout_seconds=60)
    assert throttle.locked_out("1.2.3.4", now=0.0) is False
    for _ in range(3):
        throttle.record_failure("1.2.3.4", now=0.0)
    assert throttle.locked_out("1.2.3.4", now=1.0) is True
    assert throttle.locked_out("5.6.7.8", now=1.0) is False, "lockout leaked"
    assert throttle.locked_out("1.2.3.4", now=61.0) is False, "never recovers"


def test_login_throttle_memory_is_bounded():
    throttle = auth_mod.LoginThrottle(max_attempts=2, lockout_seconds=10,
                                      max_tracked=16)
    for i in range(500):
        throttle.record_failure(f"10.0.0.{i}", now=float(i))
    assert len(throttle._failures) <= 16


# ── unauthorized access fails closed over HTTP ──────────────────────────────

@pytest.mark.parametrize("path", ["/", "/portfolio", "/research", "/charts",
                                  "/charts/image/20260910T120000Z-abcdef123456"])
def test_pages_require_authentication(owner_env, path: str):
    status, headers, body = owner_env["client"].request("GET", path)
    assert status == 303 and headers.get("Location") == "/login"
    assert b"NVDA" not in body and b"1041" not in body


def test_unauthenticated_upload_is_refused_and_writes_nothing(owner_env):
    body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
    status, headers, _ = owner_env["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 303 and headers.get("Location") == "/login"
    assert inbox_mod.list_records(owner_env["inbox"]) == []
    assert not (owner_env["inbox"] / "charts").exists()


def test_forged_session_cookie_is_rejected(owner_env):
    client = owner_env["client"]
    client.cookie = f"{auth_mod.SESSION_COOKIE_NAME}=99999999999.{'f' * 64}"
    status, headers, _ = client.request("GET", "/portfolio")
    assert status == 303 and headers.get("Location") == "/login"


def test_malformed_cookie_header_does_not_crash_the_service(owner_env):
    client = owner_env["client"]
    for junk in ("=====", "phq_owner_session", "a=b; ;;; c", "%%%"):
        status, headers, _ = client.request("GET", "/", None, {"Cookie": junk})
        assert status == 303 and headers.get("Location") == "/login"


def test_wrong_token_is_refused_and_sets_no_cookie(owner_env):
    body = b"token=definitely-not-the-owner-token"
    status, headers, page = owner_env["client"].request(
        "POST", "/login", body,
        {"Content-Type": "application/x-www-form-urlencoded"}, use_cookie=False)
    assert status == 401
    assert "Set-Cookie" not in headers
    assert b"not accepted" in page


def test_repeated_failures_lock_the_login_endpoint(owner_env):
    client = owner_env["client"]
    body = b"token=wrong-token-value"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    seen_lock = False
    for _ in range(auth_mod.MAX_FAILED_ATTEMPTS + 2):
        status, _, _ = client.request("POST", "/login", body, headers,
                                      use_cookie=False)
        if status == 429:
            seen_lock = True
            break
    assert seen_lock, "the login endpoint never locked out"
    # A correct token is still refused while locked: fail closed.
    status, _, _ = client.request("POST", "/login", f"token={TOKEN}".encode(),
                                  headers, use_cookie=False)
    assert status == 429


def test_successful_sign_in_sets_a_hardened_cookie(owner_env):
    status, headers = owner_env["client"].sign_in()
    assert status == 303 and headers.get("Location") == "/"
    cookie = headers["Set-Cookie"]
    assert "HttpOnly" in cookie and "SameSite=Strict" in cookie
    assert "Path=/" in cookie
    # Loopback bind: plain HTTP is the normal local case, so Secure is off.
    assert "Secure" not in cookie


def test_non_loopback_configuration_marks_the_cookie_secure(tmp_path: Path):
    config = service_mod.build_config(
        inbox_root=tmp_path / "i", export_path=tmp_path / "e.json",
        host="0.0.0.0", env={auth_mod.TOKEN_ENV_VAR: TOKEN})
    assert config.secure_cookie is True


@pytest.mark.parametrize("host,expected", [
    ("127.0.0.1", True), ("::1", True), ("localhost", True), ("", True),
    ("0.0.0.0", False), ("10.1.2.3", False), ("example.com", False),
])
def test_loopback_detection(host: str, expected: bool):
    assert service_mod.is_loopback_host(host) is expected


def test_sign_out_clears_the_session(signed_in):
    client = signed_in["client"]
    status, headers, _ = client.request("GET", "/logout")
    assert status == 303 and headers.get("Location") == "/login"
    assert "Max-Age=0" in headers.get("Set-Cookie", "")


def test_healthz_is_unauthenticated_and_discloses_nothing(owner_env):
    status, headers, body = owner_env["client"].request("GET", "/healthz",
                                                        use_cookie=False)
    assert status == 200
    assert json.loads(body) == {"status": "ok"}
    for secret in (b"NVDA", b"1041", b"aaaaaaa", b"main", b"holdings"):
        assert secret not in body


# ── method and route restrictions ────────────────────────────────────────────

@pytest.mark.parametrize("method", ["PUT", "DELETE", "PATCH", "OPTIONS"])
def test_only_get_and_post_are_served(signed_in, method: str):
    status, _, _ = signed_in["client"].request(method, "/", b"", {})
    assert status == 405


def test_unknown_routes_are_not_served(signed_in):
    for path in ("/nope", "/../etc/passwd", "/assets/../../secret",
                 "/holdings.yaml", "/targets.yaml", "/.env"):
        status, _, _ = signed_in["client"].request("GET", path)
        assert status == 404, path


def test_unknown_post_routes_are_not_served(signed_in):
    status, _, _ = signed_in["client"].request(
        "POST", "/charts/delete", b"x", {"Content-Type": "text/plain"})
    assert status == 404


def test_cross_origin_posts_are_refused(signed_in):
    body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
    status, _, _ = signed_in["client"].request(
        "POST", "/charts/upload", body,
        {"Content-Type": content_type, "Origin": "https://attacker.example"})
    assert status == 403
    assert inbox_mod.list_records(signed_in["inbox"]) == []


def test_cross_origin_login_is_refused(owner_env):
    status, _, _ = owner_env["client"].request(
        "POST", "/login", f"token={TOKEN}".encode(),
        {"Content-Type": "application/x-www-form-urlencoded",
         "Origin": "https://attacker.example"}, use_cookie=False)
    assert status == 403


def test_same_origin_post_is_allowed(signed_in):
    body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
    port = signed_in["client"].port
    status, _, _ = signed_in["client"].request(
        "POST", "/charts/upload", body,
        {"Content-Type": content_type, "Host": f"127.0.0.1:{port}",
         "Origin": f"http://127.0.0.1:{port}"})
    assert status == 200


def test_responses_that_leave_a_body_unread_close_the_connection(owner_env):
    """Refusals answered without draining the request body must not keep alive.

    The service speaks HTTP/1.1, so a persistent connection carrying an unread
    request body would have those leftover bytes misparsed as the start of the
    next request. Every refusal path that answers early therefore closes.
    """
    client = owner_env["client"]
    cases = [
        ("PUT", "/", b"x" * 400, {}),                                  # method refused
        ("POST", "/charts/upload", b"y" * 200, {}),                    # unauthenticated
        ("POST", "/charts/upload", b"z" * 16,
         {"Content-Type": "multipart/form-data; boundary=b",
          "Content-Length": str(service_mod.MAX_REQUEST_BYTES + 1)}),  # oversized
    ]
    for method, path, body, extra in cases:
        conn = http.client.HTTPConnection("127.0.0.1", client.port, timeout=20)
        try:
            headers = {"Content-Length": str(len(body)), **extra}
            conn.request(method, path, body=body, headers=headers)
            response = conn.getresponse()
            response.read()
            assert response.will_close is True, f"{method} {path} stayed keep-alive"
            assert response.getheader("Connection", "").lower() == "close"
        finally:
            conn.close()


def test_a_normal_connection_stays_reusable(signed_in):
    """Ordinary responses must not close: a phone reloading pages reuses one
    connection, and closing every time would be a self-inflicted regression."""
    conn = http.client.HTTPConnection("127.0.0.1", signed_in["client"].port,
                                      timeout=20)
    try:
        for path in ("/healthz", "/healthz", "/healthz"):
            conn.request("GET", path)
            response = conn.getresponse()
            payload = response.read()
            assert response.status == 200
            assert response.will_close is False, "the connection closed early"
            assert json.loads(payload) == {"status": "ok"}
    finally:
        conn.close()


def test_security_headers_are_present_on_pages(signed_in):
    _, headers, _ = signed_in["client"].request("GET", "/")
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["Referrer-Policy"] == "no-referrer"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Cache-Control"] == "no-store"
    csp = headers["Content-Security-Policy"]
    assert "default-src 'none'" in csp and "frame-ancestors 'none'" in csp
    assert "script-src" not in csp, "no script source should ever be allowed"


# ── chart intake over HTTP ───────────────────────────────────────────────────

def test_upload_happy_path_quarantines_and_reports_back(signed_in):
    image = png_bytes(50, 30)
    body, content_type = multipart({"ticker": "NVDA", "timeframe": "1D"},
                                   {"chart": ("NVDA daily.png", image)})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 200
    assert b"Received." in page and b"quarantined" in page.lower()

    records = inbox_mod.list_records(signed_in["inbox"])
    assert len(records) == 1
    record = records[0]
    assert record["state"] == inbox_mod.STATE_QUARANTINED
    assert record["declared_ticker"] == "NVDA"
    assert record["content_sha256"] == hashlib.sha256(image).hexdigest()
    stored = signed_in["inbox"] / record["stored_relpath"]
    assert stored.read_bytes() == image, "HTTP transport altered the image bytes"


def test_upload_preserves_bytes_of_a_jpeg_too(signed_in):
    image = jpeg_bytes(64, 40)
    body, content_type = multipart({}, {"chart": ("shot.jpeg", image)})
    signed_in["client"].request("POST", "/charts/upload", body,
                                {"Content-Type": content_type})
    record = inbox_mod.list_records(signed_in["inbox"])[0]
    assert (signed_in["inbox"] / record["stored_relpath"]).read_bytes() == image


def test_duplicate_upload_is_reported_and_stores_no_second_copy(signed_in):
    body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
    signed_in["client"].request("POST", "/charts/upload", body,
                                {"Content-Type": content_type})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 200 and b"Already received" in page
    stored = list((signed_in["inbox"] / "charts").rglob("original.*"))
    assert len(stored) == 1


def test_unsupported_upload_is_reported_and_stores_nothing(signed_in):
    body, content_type = multipart({}, {"chart": ("evil.png", b"GIF89a" + b"\x00" * 40)})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 400
    assert b"Not accepted" in page and b"PNG and JPEG" in page
    assert inbox_mod.list_records(signed_in["inbox"]) == []


def test_corrupt_upload_is_reported_and_stores_nothing(signed_in):
    body, content_type = multipart({}, {"chart": ("cut.png", png_bytes()[:24])})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 400 and b"damaged or incomplete" in page
    assert inbox_mod.list_records(signed_in["inbox"]) == []


def test_oversized_upload_is_refused_on_the_declared_length(signed_in):
    """Refused from the Content-Length header, before any payload is read."""
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", b"x" * 16,
        {"Content-Type": "multipart/form-data; boundary=b",
         "Content-Length": str(service_mod.MAX_REQUEST_BYTES + 1)})
    assert status == 413
    assert inbox_mod.list_records(signed_in["inbox"]) == []


def test_request_ceiling_is_bounded_and_above_the_image_ceiling():
    assert service_mod.MAX_REQUEST_BYTES > inbox_mod.MAX_UPLOAD_BYTES
    assert service_mod.MAX_REQUEST_BYTES < 128 * 1024 * 1024


@pytest.mark.parametrize("content_type,body", [
    ("multipart/form-data; boundary=b", b"garbage-not-multipart"),
    ("multipart/form-data", b"--b\r\n\r\n"),
    ("text/plain", b"chart=whatever"),
    ("application/json", b'{"chart": "x"}'),
    ("multipart/form-data; boundary=b", b""),
])
def test_malformed_upload_requests_are_refused_cleanly(signed_in, content_type, body):
    status, _, _ = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status in (400, 413), status
    assert inbox_mod.list_records(signed_in["inbox"]) == []


def test_upload_without_a_file_part_is_refused(signed_in):
    body, content_type = multipart({"ticker": "NVDA"}, {})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 400 and b"No chart file" in page


def test_upload_with_a_hostile_filename_stores_safely(signed_in):
    body, content_type = multipart(
        {}, {"chart": ("../../../../etc/passwd.png", png_bytes())})
    status, _, _ = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 200
    record = inbox_mod.list_records(signed_in["inbox"])[0]
    stored = (signed_in["inbox"] / record["stored_relpath"]).resolve()
    assert (signed_in["inbox"] / "charts").resolve() in stored.parents
    assert stored.name == "original.png"
    assert record["display_filename_sanitized"] is True


def test_upload_with_an_unlisted_ticker_is_refused(signed_in):
    body, content_type = multipart({"ticker": "ENRON"},
                                   {"chart": ("a.png", png_bytes())})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 400 and b"accepted Portfolio-HQ instrument list" in page
    assert inbox_mod.list_records(signed_in["inbox"]) == []


def test_storage_failure_is_surfaced_not_silently_accepted(signed_in):
    signed_in["inbox"].mkdir(parents=True, exist_ok=True)
    (signed_in["inbox"] / "charts").write_text("not a directory")
    body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
    status, _, page = signed_in["client"].request(
        "POST", "/charts/upload", body, {"Content-Type": content_type})
    assert status == 500
    assert b"could not be stored" in page and b"not received" in page


def test_retained_image_is_retrievable_for_review(signed_in):
    image = png_bytes(33, 21)
    body, content_type = multipart({}, {"chart": ("a.png", image)})
    signed_in["client"].request("POST", "/charts/upload", body,
                                {"Content-Type": content_type})
    record = inbox_mod.list_records(signed_in["inbox"])[0]
    status, headers, payload = signed_in["client"].request(
        "GET", "/charts/image/" + record["intake_id"])
    assert status == 200
    assert headers["Content-Type"] == "image/png"
    assert payload == image, "the reviewer must see the exact retained bytes"


@pytest.mark.parametrize("reference", [
    "../../../etc/passwd", "..%2f..%2fetc%2fpasswd", "", "not-an-id",
    "20260910T120000Z-000000000000", "20260910T120000Z-abcdef123456/../../x",
])
def test_chart_image_route_refuses_forged_references(signed_in, reference: str):
    status, _, _ = signed_in["client"].request("GET", "/charts/image/" + reference)
    assert status == 404


def test_multipart_parser_copies_payload_bytes_verbatim():
    """Byte fidelity is the whole point: the recorded hash must stay true."""
    payload = bytes(range(256)) * 8 + b"\r\n--fake-boundary\r\n" + b"\x00\r\r\n\n"
    body, content_type = multipart({"k": "v"}, {"chart": ("x.bin", payload)})
    fields = service_mod.parse_multipart(body, content_type)
    assert fields["k"] == "v"
    assert isinstance(fields["chart"], service_mod.UploadedFile)
    assert fields["chart"].content == payload
    assert fields["chart"].filename == "x.bin"


def test_multipart_parser_rejects_non_multipart_content_types():
    for content_type in ("application/json", "", "multipart/mixed; boundary=b",
                         "multipart/form-data; boundary=" + "z" * 400):
        assert service_mod.parse_multipart(b"anything", content_type) == {}


def test_multipart_parser_bounds_part_count_and_text_length():
    files = {f"f{i}": (f"{i}.png", b"x") for i in range(40)}
    body, content_type = multipart({}, files)
    assert len(service_mod.parse_multipart(body, content_type)) <= 8
    body2, ct2 = multipart({"ticker": "N" * 5000}, {})
    assert len(service_mod.parse_multipart(body2, ct2)["ticker"]) <= 256


# ── intake never gains authority ─────────────────────────────────────────────

_AUTHORITY_FILES = ("holdings.yaml", "targets.yaml", "gates.yaml",
                    "issuer_lookthrough.yaml", "governance/decisions.yaml",
                    "operations/WORKSTREAMS.yaml")


def test_a_full_owner_session_mutates_no_authoritative_repository_file(signed_in):
    before = {name: (REPO_ROOT / name).read_bytes() for name in _AUTHORITY_FILES}
    client = signed_in["client"]
    for path in ("/", "/portfolio", "/research", "/charts"):
        client.request("GET", path)
    body, content_type = multipart({"ticker": "NVDA", "timeframe": "1D"},
                                   {"chart": ("a.png", png_bytes())})
    client.request("POST", "/charts/upload", body, {"Content-Type": content_type})
    client.request("POST", "/charts/upload", body, {"Content-Type": content_type})
    after = {name: (REPO_ROOT / name).read_bytes() for name in _AUTHORITY_FILES}
    assert before == after, "the owner interface changed an authoritative file"


def test_intake_does_not_alter_the_presentation_export(signed_in):
    before = signed_in["export_path"].read_bytes()
    body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
    signed_in["client"].request("POST", "/charts/upload", body,
                                {"Content-Type": content_type})
    assert signed_in["export_path"].read_bytes() == before


def test_uploaded_chart_does_not_change_any_reported_portfolio_value(signed_in):
    client = signed_in["client"]
    _, _, before = client.request("GET", "/portfolio")
    body, content_type = multipart({"ticker": "NVDA", "timeframe": "1D"},
                                   {"chart": ("a.png", png_bytes())})
    client.request("POST", "/charts/upload", body, {"Content-Type": content_type})
    _, _, after = client.request("GET", "/portfolio")
    assert before == after, "an upload moved a portfolio figure"


def test_service_exposes_no_stage1_or_order_surface():
    """No order or Stage-1 *identifier* is referenced anywhere in the service.

    Checked over real code identifiers rather than raw text: the module's own
    safety documentation legitimately contains words like "brokerage" while
    stating that none is used, and a substring scan cannot tell the difference
    between a prohibition and a capability.
    """
    tree = ast.parse(Path(service_mod.__file__).read_text())
    identifiers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            identifiers.add(node.id.lower())
        elif isinstance(node, ast.Attribute):
            identifiers.add(node.attr.lower())
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names]
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            identifiers.update(n.lower() for n in names)
    forbidden_fragments = ("order", "trade", "stage1", "stage_1", "brokerage",
                           "alpaca", "robinhood", "margin", "arm")
    hits = {
        name for name in identifiers
        if any(fragment in name for fragment in forbidden_fragments)
    }
    assert hits == set(), f"service.py references {sorted(hits)}"


def test_no_owner_module_writes_outside_the_inbox(tmp_path: Path):
    """Every write path in the package must be the chart inbox's own."""
    owner_dir = REPO_ROOT / "portfolio_hq" / "owner"
    writers: list[str] = []
    for path in sorted(owner_dir.glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            is_write = False
            if isinstance(node, ast.Call):
                func = node.func
                name = getattr(func, "attr", None) or getattr(func, "id", None)
                if name in ("write_text", "write_bytes", "mkdir", "makedirs",
                            "rename", "replace", "unlink", "rmtree"):
                    is_write = True
                if name == "open":
                    for arg in list(node.args[1:2]) + [
                            kw.value for kw in node.keywords if kw.arg == "mode"]:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str) \
                                and any(f in arg.value for f in "wax+"):
                            is_write = True
            if is_write:
                writers.append(path.name)
    # Writing is confined to the inbox, the export writer, and the CLI/service
    # bootstrap that creates the inbox directory itself.
    assert set(writers) <= {"chart_inbox.py", "export_io.py", "service.py"}, writers


# ── owner-facing presentation contract ──────────────────────────────────────

@pytest.mark.parametrize("path", ["/", "/portfolio", "/research", "/charts"])
def test_every_page_is_mobile_ready_offline_and_scriptless(signed_in, path: str):
    status, headers, body = signed_in["client"].request("GET", path)
    assert status == 200
    assert headers["Content-Type"].startswith("text/html")
    assert b'name="viewport"' in body and b"width=device-width" in body
    assert b"<script" not in body, "the interface must ship no JavaScript"
    # No external host of any kind (the XML namespace URL is not a fetch).
    stripped = body.replace(b"http://www.w3.org", b"")
    assert b"http://" not in stripped and b"https://" not in stripped
    assert b"max-width: 599px" in body, "responsive stacking rule missing"
    assert b'name="robots" content="noindex' in body


@pytest.mark.parametrize("path", ["/", "/portfolio", "/research", "/charts"])
def test_recommendation_only_disclosure_is_on_every_page(signed_in, path: str):
    _, _, body = signed_in["client"].request("GET", path)
    assert b"Recommendation-only" in body
    assert b"never places, routes or submits an order" in body
    assert b"no brokerage connection" in body.lower()


def test_login_page_also_carries_the_disclosure_and_no_private_data(owner_env):
    _, _, body = owner_env["client"].request("GET", "/login", use_cookie=False)
    assert b"Recommendation-only" in body
    assert b"NVDA" not in body and b"1041" not in body


def test_home_page_speaks_plainly_about_what_needs_attention(signed_in):
    _, _, body = signed_in["client"].request("GET", "/")
    assert b"What needs your attention" in body
    assert b"A blocking thing" in body and b"A warning thing" in body
    assert b"No allocation recommendation can be produced right now" in body
    assert b"no live market data in the offline export" in body


def test_home_page_states_book_value_is_unavailable_with_the_reason(signed_in):
    _, _, body = signed_in["client"].request("GET", "/")
    assert b"Not available." in body
    assert b"CASH STATE: stale" in body
    assert b"What would fix it" in body


def test_portfolio_page_shows_level1_and_level2_from_the_export(signed_in):
    _, _, body = signed_in["client"].request("GET", "/portfolio")
    assert b"Level 1" in body and b"Direct equities" in body and b"63.25%" in body
    assert b"Level 2" in body and b"NVDA" in body and b"TSLA" in body
    assert b"gated" in body.lower()
    assert b"semis" in body and b"25.00%" in body


def test_portfolio_page_labels_a_stale_cash_observation_honestly(signed_in):
    _, _, body = signed_in["client"].request("GET", "/portfolio")
    assert b"dated observation, not current" in body
    assert b"2026-08-01" in body
    assert b"cash synced 40d ago" in body


def test_portfolio_page_does_not_present_a_market_value(signed_in):
    _, _, body = signed_in["client"].request("GET", "/portfolio")
    assert b"no live price is used" in body


def test_research_page_shows_freshness_and_decisions(signed_in):
    _, _, body = signed_in["client"].request("GET", "/research")
    assert b"Research coverage" in body and b"LLY" in body
    assert b"PHQ-2026-02" in body and b"WS-0014" in body


def test_charts_page_explains_the_quarantine_workflow(signed_in):
    _, _, body = signed_in["client"].request("GET", "/charts")
    assert b"Send a chart" in body
    assert b"Quarantined" in body
    assert b"does not change any holding, target, sleeve weight" in body
    assert b'accept="image/png,image/jpeg"' in body
    for ticker in (b"NVDA", b"TSLA", b"BTC"):
        assert b"<option value=\"" + ticker in body


def test_charts_page_survives_a_missing_export(tmp_path: Path):
    page = render_mod.charts_page(None, [], flash=None)
    assert "Send a chart" in page
    assert "not available" in page.lower() or "You can still upload it" in page


def test_pages_degrade_honestly_when_the_export_is_missing(tmp_path: Path):
    inbox = tmp_path / "inbox"
    config = service_mod.build_config(
        inbox_root=inbox, export_path=tmp_path / "absent.json", host="127.0.0.1",
        env={auth_mod.TOKEN_ENV_VAR: TOKEN})
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), service_mod._make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        client = Client(httpd.server_address[1])
        client.sign_in()
        for path in ("/", "/portfolio", "/research", "/charts"):
            status, _, body = client.request("GET", path)
            assert status == 200, path
            assert b"Recommendation-only" in body
        _, _, home = client.request("GET", "/")
        assert b"presentation export has not been built" in home
        # Intake still works with no export, but cannot attach a ticker.
        body, content_type = multipart({}, {"chart": ("a.png", png_bytes())})
        status, _, _ = client.request("POST", "/charts/upload", body,
                                      {"Content-Type": content_type})
        assert status == 200
        assert len(inbox_mod.list_records(inbox)) == 1
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def test_a_corrupt_export_is_treated_as_missing(tmp_path: Path):
    path = tmp_path / "export.json"
    path.write_text("{not json")
    assert load_export(path) is None
    path.write_text(json.dumps({"schema_version": 999}))
    assert load_export(path) is None, "a foreign schema version must be refused"
    assert load_export(tmp_path / "absent.json") is None


def test_rendered_values_are_escaped(tmp_path: Path):
    hostile = _sample_export()
    hostile["attention"]["warnings"] = [
        {"title": "<script>alert(1)</script>", "detail": "\" onmouseover=x"}
    ]
    hostile["level2"][0]["ticker"] = "<img src=x onerror=y>"
    markup = render_mod.home_page(hostile, {"total": 0, "quarantined": 0,
                                            "duplicates": 0, "reviewed": 0,
                                            "latest_received_at": None})
    assert "<script>alert(1)</script>" not in markup
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in markup
    portfolio = render_mod.portfolio_page(hostile)
    assert "<img src=x onerror=y>" not in portfolio


def test_record_fields_are_escaped_in_the_charts_table():
    record = {
        "intake_id": "20260910T120000Z-abcdef123456",
        "state": "quarantined_unreviewed",
        "received_at": "2026-09-10T12:00:00Z",
        "display_filename": "<script>bad</script>.png",
        "declared_ticker": "<b>NVDA</b>", "declared_timeframe": None,
        "media_type": "image/png", "image_width": 10, "image_height": 10,
        "content_sha256": "c" * 64, "display_filename_sanitized": True,
        "declared_extension_matches_content": False,
    }
    markup = render_mod.charts_page(_sample_export(), [record], flash=None)
    assert "<script>bad</script>" not in markup
    assert "&lt;script&gt;bad&lt;/script&gt;" in markup
    assert "extension did not match content" in markup


# ── the presentation export reuses canonical calculations ───────────────────

def test_export_reuses_canonical_functions_and_adds_no_allocator():
    source = Path(REPO_ROOT / "portfolio_hq" / "owner" / "export.py").read_text()
    for canonical in ("build_model", "build_policy_summary", "load_cash_state",
                      "load_margin_state", "current_dollar_availability",
                      "protected_weights"):
        assert canonical in source, f"export stopped reusing {canonical}"


def test_export_of_this_repository_is_canonical_and_honest():
    from portfolio_hq.owner.export import build_owner_export

    export = build_owner_export(REPO_ROOT, now=FIXED_NOW)
    assert export["schema_version"] == EXPORT_SCHEMA_VERSION

    # Full digests, not the dashboard's truncated display form.
    digests = {d["path"]: d for d in export["input_digests"]}
    assert "holdings.yaml" in digests
    present = [d for d in export["input_digests"] if d["sha256"]]
    assert present and all(len(d["sha256"]) == 64 for d in present)
    actual = hashlib.sha256((REPO_ROOT / "holdings.yaml").read_bytes()).hexdigest()
    assert digests["holdings.yaml"]["sha256"] == actual

    # Canonical Level-1 sleeves must agree exactly with the canonical module.
    import level1_policy_summary as lps

    canonical = lps.load_policy_summary(REPO_ROOT / "targets.yaml")
    assert export["level1"]["sleeves_pct"] == canonical["sleeves_pct"]
    assert export["level1"]["members"] == canonical["members"]

    # No invented book value, ever.
    assert export["capital"]["book"]["value"] is None
    assert export["capital"]["book"]["available"] is False
    assert export["capital"]["book"]["blocked_by"]

    assert export["boundaries"]["places_orders"] is False
    assert export["boundaries"]["arms_or_executes_stage1"] is False
    assert export["recommendation_state"]["allocation_available"] is False


def test_export_gated_protected_share_is_real_not_silently_zero():
    """Regression: the gated share of protected capital must be genuinely computed.

    ``allocate.protected_weights`` keys its gate lookup by TICKER. Handing it
    ``targets.yaml``'s allocator tuning block (``min_lot_dollars`` and friends)
    instead of the actionable gate map yields a confident, wrong ``0.00%`` —
    exactly the "silent policy breach, not a benign absence" that
    ``allocate.load_gates``'s own docstring warns about.
    """
    from portfolio_hq.owner.export import build_owner_export
    import yaml

    export = build_owner_export(REPO_ROOT, now=FIXED_NOW)
    protected = export["capital"]["protected_percentages"]

    targets = yaml.safe_load((REPO_ROOT / "targets.yaml").read_text())
    gates = yaml.safe_load((REPO_ROOT / "gates.yaml").read_text())
    gated = {entry["ticker"] for entry in gates["gates"]}
    weights = {row["ticker"]: float(row["target_pct"]) for row in targets["destination"]}
    expected = sum(weights[t] for t in gated if t in weights)

    assert gated, "the repository has no gated names to exercise this with"
    assert expected > 0
    assert protected["gated_target_pct"] == pytest.approx(expected)
    assert sorted(protected["gated_names"]) == sorted(gated)
    assert protected["gated_target_pct_reason"] is None

    # The static floor is a separate quantity and must not absorb the gated share.
    assert protected["static_protected_pct"] == pytest.approx(
        protected["cash_pct"] + protected["reserve_pct"] + protected["unreconciled_pct"])
    assert protected["static_protected_pct"] != protected["gated_target_pct"]


def test_unreadable_gates_report_unknown_rather_than_zero():
    """A gate set that cannot be read is unknown, never an empty gate set."""
    from types import SimpleNamespace

    from portfolio_hq.owner import export as export_mod

    model = export_mod.model_mod.build_model(REPO_ROOT, now=FIXED_NOW)
    blinded = SimpleNamespace(
        gates=model.gates,
        live_gates=(),                                   # nothing parsed
        margin=model.margin,
        spcx_state=SimpleNamespace(gates_unavailable=True),
    )
    capital = export_mod._capital(REPO_ROOT, blinded)
    protected = capital["protected_percentages"]
    assert protected["gated_target_pct"] is None, "unknown was reported as zero"
    assert "not zero" in protected["gated_target_pct_reason"]
    assert protected["static_protected_pct"] is not None, \
        "config-derived percentages stay knowable"


def test_portfolio_page_shows_the_gated_share_and_names(signed_in):
    _, _, body = signed_in["client"].request("GET", "/portfolio")
    assert b"Gated targets held as cash" in body


def test_portfolio_page_reports_an_unknown_gated_share_honestly():
    export = _sample_export()
    export["capital"]["protected_percentages"].update({
        "gated_target_pct": None,
        "gated_names": [],
        "gated_target_pct_reason": "gates.yaml could not be read, so the gated "
                                   "share of protected capital is unknown -- it "
                                   "is not zero",
    })
    markup = render_mod.portfolio_page(export)
    assert "not available" in markup
    assert "it is not zero" in markup
    assert ">0.00%<" not in markup


def test_export_level2_matches_the_canonical_destination_roster():
    from portfolio_hq.owner.export import build_owner_export
    import yaml

    export = build_owner_export(REPO_ROOT, now=FIXED_NOW)
    targets = yaml.safe_load((REPO_ROOT / "targets.yaml").read_text())
    exported = [row["ticker"] for row in export["level2"]]
    expected = [row["ticker"] for row in targets["destination"]]
    # Exact membership, no additions and no omissions. Row order comes from the
    # canonical dashboard model, which sorts; ordering is presentation, not policy.
    assert sorted(exported) == sorted(expected)
    assert len(exported) == len(set(exported)) == len(expected)
    by_ticker = {row["ticker"]: row for row in export["level2"]}
    for row in targets["destination"]:
        assert by_ticker[row["ticker"]]["target_pct"] == pytest.approx(
            float(row["target_pct"])), row["ticker"]
        assert by_ticker[row["ticker"]]["asset_class"] == row.get("asset_class")


def test_export_chart_allowlist_excludes_non_chartable_rows():
    from portfolio_hq.owner.export import build_owner_export

    export = build_owner_export(REPO_ROOT, now=FIXED_NOW)
    eligible = set(export["chart_request"]["eligible_tickers"])
    assert "CASH" not in eligible and "RESERVE" not in eligible
    assert "NVDA" in eligible
    assert export["chart_request"]["requested_batch_specified"] is False


def test_export_writes_deterministic_json(tmp_path: Path):
    from portfolio_hq.owner.export import build_owner_export

    export = build_owner_export(REPO_ROOT, now=FIXED_NOW)
    first = write_export(tmp_path / "a.json", export).read_bytes()
    second = write_export(tmp_path / "b.json", export).read_bytes()
    assert first == second
    assert load_export(tmp_path / "a.json") == export


def test_export_cli_writes_only_the_named_output(tmp_path: Path, capsys):
    before = {name: (REPO_ROOT / name).read_bytes() for name in _AUTHORITY_FILES}
    out = tmp_path / "nested" / "export.json"
    assert owner_cli_main(["export", "--repo-root", str(REPO_ROOT),
                           "--output", str(out)]) == 0
    assert out.is_file() and load_export(out) is not None
    assert "Recommendation-only" in capsys.readouterr().out
    after = {name: (REPO_ROOT / name).read_bytes() for name in _AUTHORITY_FILES}
    assert before == after


def test_owner_runtime_state_is_gitignored():
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", "var/owner/export.json"],
        cwd=str(REPO_ROOT))
    assert ignored.returncode == 0, "generated owner state must not be committable"


def _dockerfile_copy_sources() -> list[str]:
    """Repo-relative paths the deployment Dockerfile copies into the image."""
    dockerfile = REPO_ROOT / "deploy" / "owner_interface" / "Dockerfile"
    sources = []
    for line in dockerfile.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("COPY "):
            parts = stripped.split()
            sources.extend(parts[1:-1])
    return sources


def test_deployment_image_needs_only_the_standard_library(tmp_path: Path):
    """The documented deployment file set must actually run, on its own.

    Copies exactly what the Dockerfile copies into an isolated tree with no
    repository state and no third-party package on the path, then starts the
    service and answers a request. This is the provider-neutral deployment
    contract: if this passes, any host that can run CPython can host it.
    """
    sources = _dockerfile_copy_sources()
    assert sources, "the Dockerfile declared no COPY sources"

    image_root = tmp_path / "image"
    for rel in sources:
        source = REPO_ROOT / rel
        destination = image_root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            import shutil

            shutil.copytree(source, destination,
                            ignore=lambda *_: {"__pycache__"})
        else:
            destination.write_bytes(source.read_bytes())

    # Nothing authoritative may be needed by, or present in, the image.
    for authority in ("holdings.yaml", "targets.yaml", "gates.yaml",
                      "governance", "intelligence", "allocate.py"):
        assert not (image_root / authority).exists()

    program = (
        "import http.client, os, sys, threading\n"
        # -I is full isolation, so the image root is added explicitly rather
        # than inherited from PYTHONPATH or the working directory.
        "sys.path.insert(0, sys.argv[1])\n"
        "from http.server import ThreadingHTTPServer\n"
        "from portfolio_hq.owner import service as svc\n"
        "cfg = svc.build_config(inbox_root=os.path.join(os.getcwd(), 'inbox'),\n"
        "                       export_path='absent.json', host='0.0.0.0')\n"
        "httpd = ThreadingHTTPServer(('127.0.0.1', 0), svc._make_handler(cfg))\n"
        "threading.Thread(target=httpd.serve_forever, daemon=True).start()\n"
        "c = http.client.HTTPConnection('127.0.0.1', httpd.server_address[1], timeout=10)\n"
        "c.request('GET', '/healthz')\n"
        "r = c.getresponse(); body = r.read(); c.close()\n"
        "third_party = sorted(m for m in ('yaml', 'pandas', 'numpy', 'certifi',\n"
        "    'curl_cffi', 'yfinance', 'matplotlib', 'pytest') if m in sys.modules)\n"
        "print(r.status, body.decode().strip(), cfg.secure_cookie,\n"
        "      'portfolio_hq.dashboard' in sys.modules, third_party or ['none'])\n"
        "httpd.shutdown()\n"
    )
    env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        auth_mod.TOKEN_ENV_VAR: TOKEN,
    }
    result = subprocess.run(
        [sys.executable, "-I", "-c", program, str(image_root)],
        cwd=str(image_root), env=env, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    parts = result.stdout.split(maxsplit=4)
    status, payload, secure, dashboard_loaded, third_party = parts
    assert status == "200" and payload == '{"status":"ok"}'
    assert secure == "True", "a non-loopback bind must mark the cookie Secure"
    assert dashboard_loaded == "False", "the image pulled in the dashboard"
    assert third_party.strip() == "['none']", (
        f"the deployed service imported third-party packages: {third_party}")


def test_deployment_image_carries_no_secret():
    dockerfile = (REPO_ROOT / "deploy" / "owner_interface" / "Dockerfile").read_text()
    assert auth_mod.TOKEN_ENV_VAR in dockerfile, "the token variable is undocumented"
    assert f"{auth_mod.TOKEN_ENV_VAR}=" not in dockerfile, "a token value is baked in"
    assert "/data" in dockerfile, "no persistent volume is declared"


def test_deployment_contract_is_documented():
    doc = REPO_ROOT / "docs" / "PORTFOLIO_HQ_OWNER_INTERFACE.md"
    assert doc.is_file(), "the scoped architecture change must be documented"
    text = doc.read_text()
    for required in (auth_mod.TOKEN_ENV_VAR, "TLS", "loopback", "chart inbox",
                     "recommendation-only"):
        assert required.lower() in text.lower(), f"docs omit {required}"
