#!/usr/bin/env python3
"""Rendered-browser gate for the private owner account-staging journey.

This is intentionally standalone: the regular Python test suite does not need
Playwright.  The workflow that calls this script installs its pinned browser
dependency, while every service write and every synthetic observation stays in
one temporary directory.
"""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit


REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

if importlib.util.find_spec("playwright") is None:
    raise SystemExit(
        "ERROR: Playwright is required; install the workflow-pinned release and Chromium."
    )

from playwright.sync_api import Page, sync_playwright  # noqa: E402

from portfolio_hq.owner import auth as auth_mod  # noqa: E402
from portfolio_hq.owner import service as service_mod  # noqa: E402


TOKEN = "synthetic-browser-validation-token"
VIEWPORTS = {"narrow": {"width": 390, "height": 844},
             "wide": {"width": 1440, "height": 900}}
MAX_SCREENSHOT_LOG_BYTES = 2 * 1024 * 1024


def synthetic_document(
    identity: str,
    *,
    holding_freshness: str = "current",
    include_protected: bool = True,
    quantity: int = 0,
) -> bytes:
    """Return compact, deterministic, wholly synthetic account evidence."""
    document = {
        "schema_version": 1,
        "client_submission_id": identity,
        "submitted_at": "2026-09-14T12:00:00Z",
        "holdings": [{
            "ticker": "SYNTH",
            "quantity": quantity,
            "observed_at": "2026-09-14T11:00:00Z",
            "freshness": holding_freshness,
            "valuation": {
                "unit_price": 12.5,
                "currency": "USD",
                "observed_at": "2026-09-14T10:00:00Z",
                "freshness": holding_freshness,
            },
        }],
        "cash": [{
            "account_id": "synthetic-cash",
            "balance": 0,
            "currency": "USD",
            "observed_at": "2026-09-14T11:00:00Z",
            "freshness": "current",
        }],
        "debt_margin": [{
            "account_id": "synthetic-margin",
            "balance": 0,
            "currency": "USD",
            "observed_at": "2026-09-14T11:00:00Z",
            "freshness": "unknown",
        }],
        "protected_capital": ([{
            "evidence_id": "synthetic-reserve",
            "amount": 25,
            "currency": "USD",
            "observed_at": "2026-09-14T11:00:00Z",
            "freshness": "current",
            "basis": "synthetic browser fixture",
        }] if include_protected else []),
    }
    return json.dumps(document, separators=(",", ":")).encode("utf-8")


def conflicting_document(identity: str) -> bytes:
    document = json.loads(synthetic_document(identity))
    document["holdings"].append(dict(document["holdings"][0]))
    return json.dumps(document, separators=(",", ":")).encode("utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def login(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/accounts")
    require(page.url == f"{base_url}/login", "anonymous account route was not denied")
    require(page.get_by_role("heading", name="Sign in", exact=True).is_visible(),
            "sign-in page was not rendered")
    page.locator("#token").fill(TOKEN)
    with page.expect_request(
        lambda request: request.method == "POST"
        and urlsplit(request.url).path == "/login"
    ) as login_request, page.expect_response(
        lambda response: response.request.method == "POST"
        and urlsplit(response.url).path == "/login"
    ) as login_response:
        page.get_by_role("button", name="Sign in", exact=True).click()
    request = login_request.value
    response = login_response.value
    origin = request.header_value("origin")
    destination = urlsplit(request.url).path
    print(f"LOGIN_FORM status={response.status} origin={origin} destination={destination}")
    require(origin == base_url, "native login form did not send its same-origin Origin")
    require(destination == "/login", "native login form used an unexpected destination")
    require(response.status == 303, "native login form did not receive its successful redirect")
    page.wait_for_url(f"{base_url}/")
    page.goto(f"{base_url}/accounts")
    require(page.get_by_role(
        "heading", name="Submit a manual account version", exact=True
    ).is_visible(),
            "authenticated account page was not rendered")


def upload(page: Page, identity: str, payload: bytes) -> None:
    page.locator('input[name="account"]').set_input_files({
        "name": f"{identity}.json",
        "mimeType": "application/json",
        "buffer": payload,
    })
    page.get_by_role("button", name="Retain exact version", exact=True).click()
    page.wait_for_load_state("networkidle")


def card(page: Page, identity: str):
    return page.locator("section.card").filter(
        has=page.get_by_text(identity, exact=True)
    )


def history_entry(page: Page, identity: str, decision: str, reviewer: str):
    return card(page, identity).locator("li").filter(
        has_text=re.compile(
            rf"^{re.escape(decision)} by {re.escape(reviewer)} at "
        )
    )


def review(page: Page, identity: str, decision: str, reviewer: str) -> int:
    selected = card(page, identity)
    require(selected.count() == 1, f"expected exactly one card for {identity}")
    selected.locator('input[name="reviewer"]').fill(reviewer)
    label = "Confirm exact version" if decision == "confirmed" else "Reject exact version"
    with page.expect_response(re.compile(r"/accounts/review/")) as response:
        selected.get_by_role("button", name=label, exact=True).click()
    page.wait_for_load_state("networkidle")
    return response.value.status


def assert_no_page_overflow(page: Page, name: str) -> None:
    dimensions = page.evaluate(
        "() => ({width: document.documentElement.clientWidth, "
        "scroll: document.documentElement.scrollWidth})"
    )
    require(dimensions["scroll"] <= dimensions["width"],
            f"{name} page overflowed: {dimensions}")


def screenshot_record(page: Page, name: str, state: str, *, target=None) -> tuple[str, bytes]:
    # An element capture may extend below the viewport, but it retains the
    # responsive layout produced at the declared browser viewport. This keeps
    # the complete receipt/discrepancy card inspectable without capturing
    # unrelated versions or an unbounded full-page image.
    png = target.screenshot() if target is not None else page.screenshot(full_page=False)
    viewport = page.viewport_size
    digest = hashlib.sha256(png).hexdigest()
    encoded = base64.b64encode(png)
    header = (f"{name}_BEGIN sha256={digest} "
              f"viewport={viewport['width']}x{viewport['height']} state={state}")
    return header, encoded


def emit_screenshots(records: list[tuple[str, bytes]]) -> None:
    encoded_size = sum(len(encoded) for _, encoded in records)
    require(encoded_size <= MAX_SCREENSHOT_LOG_BYTES,
            f"combined screenshot log payload is too large: {encoded_size} bytes")
    for header, encoded in records:
        print(header)
        text = encoded.decode("ascii")
        for offset in range(0, len(text), 120):
            print(text[offset:offset + 120])
        print(header.split("_BEGIN", 1)[0] + "_END")


def source_identity() -> tuple[str, str]:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD", "HEAD^{tree}"], cwd=REPOSITORY,
        check=True, capture_output=True, text=True,
    )
    head, tree = result.stdout.splitlines()
    return head, tree


def run() -> None:
    head, tree = source_identity()
    print(f"SOURCE head={head} tree={tree}")
    screenshots: list[tuple[str, bytes]] = []
    actions: list[str] = []
    server = None
    thread = None

    with tempfile.TemporaryDirectory(prefix="portfolio-hq-browser-") as temporary:
        runtime = Path(temporary)
        config = service_mod.build_config(
            inbox_root=runtime / "inbox",
            export_path=runtime / "synthetic-export-not-built.json",
            account_root=runtime / "accounts",
            host="127.0.0.1",
            env={auth_mod.TOKEN_ENV_VAR: TOKEN},
        )
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0), service_mod._make_handler(config)
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_address[1]}"

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                try:
                    narrow = browser.new_context(
                        viewport=VIEWPORTS["narrow"], accept_downloads=True
                    )
                    page = narrow.new_page()
                    login(page, base_url)
                    actions.append("anonymous denial and narrow authenticated sign-in")

                    clean = synthetic_document("browser-clean")
                    upload(page, "browser-clean", clean)
                    clean_card = card(page, "browser-clean")
                    require(clean_card.count() == 1, "clean receipt was not rendered")
                    require(clean_card.get_by_text(
                        "No validation discrepancy was found. This does not establish "
                        "freshness or correctness.", exact=True
                    ).is_visible(),
                            "clean discrepancy outcome was not rendered")

                    with page.expect_download() as download_event:
                        clean_card.get_by_role(
                            "link", name="Retrieve retained original", exact=True
                        ).click()
                    retained = Path(download_event.value.path()).read_bytes()
                    require(retained == clean, "retrieved original did not retain exact bytes")
                    require(review(page, "browser-clean", "confirmed", "synthetic-reviewer") == 200,
                            "clean exact version was not confirmed")
                    require(history_entry(
                        page, "browser-clean", "confirmed", "synthetic-reviewer"
                    ).is_visible(),
                        "confirmation/reviewer history was not rendered")
                    actions.append("clean submit, receipt, exact-original retrieval, confirmation")

                    stale = synthetic_document(
                        "browser-stale-missing", holding_freshness="stale",
                        include_protected=False,
                    )
                    upload(page, "browser-stale-missing", stale)
                    stale_card = card(page, "browser-stale-missing")
                    require(stale_card.locator("strong").get_by_text(
                        "stale_holding", exact=True
                    ).is_visible(),
                            "stale discrepancy was not rendered")
                    require(stale_card.locator("strong").get_by_text(
                        "missing_protected_capital", exact=True
                    ).is_visible(),
                        "missing-evidence discrepancy was not rendered")
                    require(review(page, "browser-stale-missing", "confirmed",
                                   "synthetic-reviewer") == 409,
                            "material discrepancies did not block confirmation")
                    require(card(page, "browser-stale-missing").get_by_text(
                        "No review decision recorded.", exact=True).is_visible(),
                        "blocked confirmation unexpectedly created review history")

                    upload(page, "browser-conflict", conflicting_document("browser-conflict"))
                    require(page.get_by_text(
                        "Submission rejected: duplicate holding identity: SYNTH", exact=True
                    ).is_visible(),
                            "conflicting evidence was not rejected")
                    require(card(page, "browser-conflict").count() == 0,
                            "conflicting evidence was retained")

                    changed = synthetic_document("browser-changed", quantity=1)
                    upload(page, "browser-changed", changed)
                    require(card(page, "browser-changed").get_by_text(
                        "No review decision recorded.", exact=True).is_visible(),
                        "changed bytes inherited a review decision")
                    require(history_entry(
                        page, "browser-clean", "confirmed", "synthetic-reviewer"
                    ).is_visible(),
                        "changed bytes altered the prior exact-version history")
                    assert_no_page_overflow(page, "narrow account")
                    stale_card = card(page, "browser-stale-missing")
                    screenshots.append(screenshot_record(
                        page, "NARROW_ACCOUNT_DISCREPANCY", "stale-missing-blocked",
                        target=stale_card,
                    ))
                    narrow.close()
                    actions.append("stale/missing block, conflict rejection, changed-version isolation")

                    wide = browser.new_context(viewport=VIEWPORTS["wide"])
                    wide_page = wide.new_page()
                    login(wide_page, base_url)
                    require(history_entry(
                        wide_page, "browser-clean", "confirmed", "synthetic-reviewer"
                    ).is_visible(),
                        "wide session did not retrieve confirmation history")
                    require(review(wide_page, "browser-changed", "rejected",
                                   "synthetic-wide-reviewer") == 200,
                            "separate exact version was not rejected")
                    require(history_entry(
                        wide_page, "browser-changed", "rejected", "synthetic-wide-reviewer"
                    ).is_visible(),
                        "rejection/reviewer history was not rendered")
                    assert_no_page_overflow(wide_page, "wide account")
                    history_entry(
                        wide_page, "browser-changed", "rejected", "synthetic-wide-reviewer"
                    ).scroll_into_view_if_needed()
                    screenshots.append(screenshot_record(
                        wide_page, "WIDE_ACCOUNT_REVIEW_HISTORY", "confirmed-and-rejected"
                    ))
                    wide.close()
                    actions.append("wide history retrieval and separate rejection")
                finally:
                    browser.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    require(thread is not None and not thread.is_alive(), "owner service did not stop")
    emit_screenshots(screenshots)
    for action in actions:
        print(f"PASS {action}")
    print("PASS responsive viewports 390x844 and 1440x900; no document overflow")
    print("PASS temporary runtime removed and owner service stopped")


if __name__ == "__main__":
    run()
