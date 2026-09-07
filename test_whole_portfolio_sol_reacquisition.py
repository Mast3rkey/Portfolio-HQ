from __future__ import annotations

import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

import risk_level1_acquisition as predecessor
import whole_portfolio_sol_reacquisition as recovery


def candle(day: str, close: float = 10.0) -> list[float]:
    stamp = int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp())
    return [stamp, close - 2, close + 2, close - 1, close, 100.0]


def test_frozen_pin_is_exact_and_clean():
    pin = recovery.load_frozen_pin()
    assert pin == recovery.FrozenPin(
        selected_path=(
            "research/level1_sleeve_robustness/data/quarantine/selected/SOL.json"
        ),
        sha256="79b1f614d43b57e530297c503322b2c282dcca2f6f6e474ce20ced8611cd584a",
        row_count=1871,
        first_observation="2021-06-17",
        last_observation="2026-07-31",
    )


def test_page_schedule_reproduces_attempt_one_boundaries():
    pages = recovery.page_requests()
    # The inventory's 33 receipts are one Alpaca primary plus 32 Coinbase pages.
    assert len(pages) == 32
    assert pages[0][0:3] == (
        0,
        recovery.START,
        recovery.START + recovery.timedelta(days=249),
    )
    assert pages[-1][2] == recovery.END
    assert all(current[2] + recovery.timedelta(days=1) == following[1]
               for current, following in zip(pages, pages[1:]))
    assert all(recovery._trusted_url(page[3]) for page in pages)


def test_page_schedule_exactly_matches_predecessor_acquisition(monkeypatch):
    observed = []

    def fake_fetch(**kwargs):
        observed.append(kwargs["url"])
        return b"[]", {}

    monkeypatch.setattr(predecessor, "fetch_bytes", fake_fetch)
    monkeypatch.setattr(predecessor, "write_json", lambda *_args: None)
    monkeypatch.setattr(predecessor.time, "sleep", lambda _seconds: None)
    rows, receipts = predecessor.coinbase_crypto("SOL")
    assert rows == []
    assert len(receipts) == 32
    assert observed == [page[3] for page in recovery.page_requests()]


@pytest.mark.parametrize(
    "url",
    [
        "http://api.exchange.coinbase.com/products/SOL-USD/candles",
        "https://api.exchange.coinbase.com.evil.test/products/SOL-USD/candles",
        "https://user:pass@api.exchange.coinbase.com/products/SOL-USD/candles",
        "https://api.exchange.coinbase.com/products/BTC-USD/candles",
        "https://api.exchange.coinbase.com:444/products/SOL-USD/candles",
    ],
)
def test_url_boundary_rejects_every_noncanonical_endpoint(url):
    assert recovery._trusted_url(url) is False


def test_redirect_handler_rejects_off_host_before_following():
    handler = recovery.TrustedRedirectHandler()
    with pytest.raises(recovery.ReacquisitionError, match="refused Coinbase redirect"):
        handler.redirect_request(None, None, 302, "Found", {}, "https://evil.test/x")


def test_normalization_matches_predecessor_semantics_and_is_canonical():
    older = candle("2021-06-17", 10)
    newer = candle("2021-06-18", 11)
    replacement = candle("2021-06-17", 12)
    document = recovery.normalize([newer, older, replacement])
    assert document["provider"] == "COINBASE_EXCHANGE"
    assert [row["date"] for row in document["rows"]] == [
        "2021-06-17",
        "2021-06-18",
    ]
    assert document["rows"][0]["close"] == 12.0
    assert document == predecessor.normalize_coinbase(
        "SOL", [newer, older, replacement]
    )
    assert recovery.canonical_json_bytes(document).endswith(b"\n")


def test_acquisition_mismatch_receipt_is_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    trusted_url = (
        "https://api.exchange.coinbase.com/products/SOL-USD/candles?"
        "granularity=86400&start=2004-11-18T00%3A00%3A00Z&"
        "end=2026-08-01T00%3A00%3A00Z"
    )
    monkeypatch.setattr(
        recovery,
        "page_requests",
        lambda: [(0, recovery.START, recovery.END, trusted_url)],
    )
    payload = json.dumps([candle("2021-06-17")]).encode()
    candidate, receipt_path, verified = recovery.acquire(
        tmp_path, fetcher=lambda _url: payload, sleep_seconds=0
    )
    receipt = json.loads(receipt_path.read_text())
    assert candidate.is_file()
    assert verified is False
    assert receipt["hash_match"] is False
    assert receipt["coverage_identity_match"] is False
    assert receipt["no_registered_results_executed"] is True
    assert receipt["actual_sha256"] == recovery.sha256_bytes(candidate.read_bytes())


def test_module_has_no_result_engine_or_credential_surface():
    source = inspect.getsource(recovery)
    assert "whole_portfolio_robustness_engine" not in source
    assert "ALPACA_API_KEY" not in source
    assert "APCA_API" not in source
    assert "GITHUB_TOKEN" not in source
    assert 'method="GET"' in source
    assert "TrustedRedirectHandler" in source
