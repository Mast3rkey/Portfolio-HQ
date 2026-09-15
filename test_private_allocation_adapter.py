"""Synthetic end-to-end coverage for the private allocation adapter."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

import allocate
from portfolio_hq.owner import account_staging, private_allocation

ROOT = Path(__file__).resolve().parent
AS_OF = "2026-09-15T12:00:00Z"


def _account(identity="adapter-v1", *, currency="USD", price=100, include_valuation=True):
    return {"schema_version": 1, "client_submission_id": identity,
            "submitted_at": "2026-09-15T11:30:00Z",
            "holdings": [{"ticker": "SYNTH", "quantity": 1,
                "observed_at": "2026-09-15T11:00:00Z", "freshness": "current",
                "valuation": ({"unit_price": price, "currency": currency,
                    "observed_at": "2026-09-15T10:00:00Z", "freshness": "current"}
                    if include_valuation else None)}],
            "cash": [{"account_id": "cash-1", "balance": 100000, "currency": currency,
                "observed_at": "2026-09-15T11:00:00Z", "freshness": "current"}],
            "debt_margin": [{"account_id": "margin-1", "balance": 0, "currency": currency,
                "observed_at": "2026-09-15T11:00:00Z", "freshness": "current"}],
            "protected_capital": [{"evidence_id": "display-only", "amount": 1,
                "currency": currency, "observed_at": "2026-09-15T11:00:00Z",
                "freshness": "current", "basis": "synthetic; not allocator authority"}]}


def _setup(tmp_path, account=None):
    original = json.dumps(account or _account(), separators=(",", ":")).encode()
    receipt = account_staging.ingest(tmp_path, original)
    review = account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "chatgpt-review")
    receipt_bytes = (tmp_path / "submissions" / receipt["submission_id"] / "receipt.json").read_bytes()
    roster = allocate.build_roster(allocate.load_yaml(ROOT / "targets.yaml"))
    market_tickers = [t for t, m in roster.items()
                      if m["asset_class"] not in {"crypto", "cash", "reserve"}]
    supplement = {"schema_version": 1, "as_of": AS_OF,
        "submission_id": receipt["submission_id"],
        "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "review_id": review["review_id"], "reviewer": "chatgpt-review",
        "buffer": {"percentage": 80, "currency": "USD",
                   "observed_at": "2026-09-15T11:00:00Z", "source_id": "display-synth"},
        "market": [{"ticker": t, "price": 100, "sma200": 90, "rsi14": 40,
                    "currency": "USD", "observed_at": "2026-09-15T10:00:00Z",
                    "source_id": "market-synth"} for t in market_tickers],
        "earnings": [{"ticker": t, "next_date": "2026-10-15",
                      "observed_at": "2026-09-15T10:00:00Z",
                      "source_id": "earnings-synth"} for t in market_tickers],
        "regime": {"ok": True, "known": True, "observed_at": "2026-09-15T10:00:00Z",
                   "source_id": "regime-synth"}}
    return receipt, review, supplement


def _run(tmp_path, supplement):
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    return private_allocation.run(tmp_path, json.dumps(supplement, separators=(",", ":")).encode(),
                                  source_root=ROOT, expected_source_sha=head)


def test_retained_bytes_confirmed_version_to_real_noncrypto_plan_is_deterministic(tmp_path):
    receipt, review, supplement = _setup(tmp_path)
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob("*") if p.is_file()}
    first = _run(tmp_path, supplement)
    second = _run(tmp_path, supplement)
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob("*") if p.is_file()}
    assert first == second
    assert before == after
    assert first["actionable"] is True
    assert first["canonical_result"]["book"] == 100100
    assert any(row["asset_class"] != "crypto" for row in first["canonical_result"]["buys"])
    assert first["canonical_result"]["orphans"] == {"SYNTH": 100.0}
    assert first["provenance"]["submission_sha256"] == receipt["submission_sha256"]
    assert first["provenance"]["review_id"] == review["review_id"]
    assert first["provenance"]["observations"][0]["valuation_observed_at"].endswith("10:00:00Z")
    assert first["provenance"]["policy"]["files_sha256"] == {
        "targets.yaml": "69cda30c3f2f7bff00ef4cd3f8f59cda83ece999145e82646ff0987041da874d",
        "gates.yaml": "e9a0bcd98a45f75b77e5f60076be34c4eda890255bb9aa0cf1a14868418f2d86",
        "issuer_lookthrough.yaml": "6cf4e417e747d9a1ae9621e57d238c685ab593fb65539d561a5d136c7027b0b9"}


@pytest.mark.parametrize("mutation, phrase", [
    (lambda d: d["buffer"].update(observed_at="2026-09-12T00:00:00Z"), "stale"),
    (lambda d: d["market"][0].update(observed_at="2026-09-16T00:00:00Z"), "future"),
    (lambda d: d.update(review_id="20260915T000000Z-000000000000"), "review identity"),
])
def test_missing_stale_future_and_wrong_version_are_controlled(tmp_path, mutation, phrase):
    _, _, supplement = _setup(tmp_path)
    mutation(supplement)
    result = _run(tmp_path, supplement)
    assert result["actionable"] is False
    assert result["canonical_result"] is None
    assert phrase in result["blocked_reasons"][0]


def test_missing_buffer_runs_canonical_plan_but_withholds_dollars(tmp_path):
    _, _, supplement = _setup(tmp_path)
    supplement.pop("buffer")
    result = _run(tmp_path, supplement)
    assert result["actionable"] is False
    assert result["canonical_result"]["dollars_available"] is False
    assert result["canonical_result"]["book"] is None
    assert result["canonical_result"]["cash"] is None
    assert result["canonical_result"]["buys"] == []
    assert all(row["target"] is None and row["gap"] is None
               for row in result["canonical_result"]["underweight"])
    assert "buffer_pct" in result["blocked_reasons"][0]


def test_rejection_supersession_and_receipt_tamper_fail_closed(tmp_path):
    _, _, supplement = _setup(tmp_path)
    account_staging.review(tmp_path, supplement["submission_id"], "rejected", "chatgpt-review")
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and "superseded" in result["blocked_reasons"][0]

    receipt_path = tmp_path / "submissions" / supplement["submission_id"] / "receipt.json"
    receipt_path.write_bytes(receipt_path.read_bytes() + b" ")
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and "receipt identity" in result["blocked_reasons"][0]


def test_cross_currency_and_unpriced_nonzero_holding_are_unavailable(tmp_path):
    _, _, supplement = _setup(tmp_path / "fx", _account(identity="fx", currency="EUR"))
    assert "cross-currency" in _run(tmp_path / "fx", supplement)["blocked_reasons"][0]

    original = _account(identity="unpriced", include_valuation=False)
    data = json.dumps(original, separators=(",", ":")).encode()
    receipt = account_staging.ingest(tmp_path / "unpriced", data)
    assert "missing_valuation" in {i["code"] for i in receipt["issues"]}
    with pytest.raises(account_staging.AccountReviewRejected):
        account_staging.review(tmp_path / "unpriced", receipt["submission_id"],
                               "confirmed", "chatgpt-review")


def test_clock_and_earnings_injection_preserve_legacy_defaults(monkeypatch):
    state = {"cash": {"balance": 1, "synced_at": "2026-09-15T01:02:03Z"}}
    assert allocate.load_cash_state(state, as_of=private_allocation._parse_timestamp(
        AS_OF, "as_of").date())["usable"]
    monkeypatch.setattr("earnings.next_earnings_date", lambda ticker: __import__("datetime").date(2026, 10, 15))
    from earnings import days_until_earnings
    assert days_until_earnings("SYNTH", as_of=__import__("datetime").date(2026, 9, 15)) == 30
