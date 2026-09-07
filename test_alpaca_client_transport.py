import json
from contextlib import nullcontext

import pytest

import alpaca_client


CREDS = {
    "ALPACA_API_KEY": "test-key",
    "ALPACA_API_SECRET": "test-secret",
    "ALPACA_BASE_URL": "https://paper-api.alpaca.markets/v2",
}


def _client(monkeypatch, base=CREDS["ALPACA_BASE_URL"]):
    credentials = {**CREDS, "ALPACA_BASE_URL": base}
    monkeypatch.setattr(alpaca_client, "load_credentials", lambda: credentials)
    return alpaca_client.AlpacaPaperClient()


@pytest.mark.parametrize(
    "base",
    [
        "http://paper-api.alpaca.markets/v2",
        "https://paper-api.alpaca.markets.evil.example/v2",
        "https://paper-api.alpaca.markets@evil.example/v2",
        "https://paper-api.alpaca.markets:444/v2",
        "https://paper-api.alpaca.markets/v2/account",
        "https://paper-api.alpaca.markets/v2?next=https://evil.example",
    ],
)
def test_paper_guard_rejects_deceptive_or_noncanonical_base(monkeypatch, base):
    with pytest.raises(RuntimeError):
        _client(monkeypatch, base)


def test_paper_guard_accepts_only_canonical_base_with_optional_trailing_slash(monkeypatch):
    assert _client(monkeypatch).base == alpaca_client.PAPER_BASE
    assert _client(monkeypatch, CREDS["ALPACA_BASE_URL"] + "/").base == alpaca_client.PAPER_BASE


@pytest.mark.parametrize("method,body", [("POST", None), ("DELETE", None), ("GET", {"x": 1})])
def test_request_primitive_is_structurally_read_only(monkeypatch, method, body):
    client = _client(monkeypatch)
    with pytest.raises(RuntimeError, match="GET requests without a body only"):
        client._req(method, f"{client.base}/account", body=body)


def test_request_primitive_rejects_untrusted_destination_before_io(monkeypatch):
    client = _client(monkeypatch)
    client._opener.open = lambda *args, **kwargs: pytest.fail("network must not be reached")
    with pytest.raises(RuntimeError, match="untrusted Alpaca endpoint"):
        client._req("GET", "https://data.alpaca.markets.evil.example/v2/stocks/SPY/bars")


def test_trusted_get_sends_no_body_and_preserves_credentials(monkeypatch):
    client = _client(monkeypatch)
    captured = {}

    class Response:
        def read(self):
            return json.dumps({"bars": []}).encode()

    def open_request(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return nullcontext(Response())

    client._opener.open = open_request
    assert client._req("GET", f"{alpaca_client.DATA_BASE}/SPY/bars") == {"bars": []}
    request = captured["request"]
    assert request.get_method() == "GET"
    assert request.data is None
    assert request.get_header("Apca-api-key-id") == "test-key"
    assert request.get_header("Apca-api-secret-key") == "test-secret"
    assert captured["timeout"] == 30


def test_redirect_handler_refuses_to_forward_credentials():
    handler = alpaca_client._RejectRedirects()
    with pytest.raises(RuntimeError, match="refusing redirected"):
        handler.redirect_request(None, None, 302, "Found", {}, "https://evil.example/")
