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
    gates = allocate.load_gates()
    market_tickers = [t for t, m in roster.items()
                      if m["asset_class"] not in {"crypto", "cash", "reserve"}]
    eligible_tickers = [t for t in market_tickers if t not in gates]
    review_bytes = (tmp_path / "submissions" / receipt["submission_id"] / "reviews" /
                    f"{review['review_id']}.json").read_bytes()
    supplement = {"schema_version": 1, "as_of": AS_OF,
        "submission_id": receipt["submission_id"],
        "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "review_id": review["review_id"], "reviewer": "chatgpt-review",
        "review_sha256": hashlib.sha256(review_bytes).hexdigest(),
        "buffer": {"percentage": 80, "currency": "USD",
                   "observed_at": "2026-09-15T11:00:00Z", "source_id": "display-synth"},
        "market": [{"ticker": t, "available": True, "price": 100, "sma200": 90, "rsi14": 40,
                    "currency": "USD", "observed_at": "2026-09-15T10:00:00Z",
                    "source_id": "market-synth"} for t in market_tickers],
        "earnings": [{"ticker": t, "next_date": "2026-10-15",
                      "observed_at": "2026-09-15T10:00:00Z",
                      "source_id": "earnings-synth"} for t in eligible_tickers],
        "regime": {"ok": True, "known": True, "observed_at": "2026-09-15T10:00:00Z",
                   "source_id": "regime-synth"}}
    return receipt, review, supplement


def _run(tmp_path, supplement):
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    return private_allocation.run(tmp_path, json.dumps(supplement, separators=(",", ":")).encode(),
                                  source_root=ROOT, expected_source_sha=head)


def test_retained_bytes_confirmed_version_to_real_noncrypto_plan_is_deterministic(
        tmp_path, monkeypatch):
    receipt, review, supplement = _setup(tmp_path)
    called = []
    real_plan = allocate.plan
    def recording_plan(*args, **kwargs):
        called.append((args, kwargs))
        return real_plan(*args, **kwargs)
    monkeypatch.setattr(allocate, "plan", recording_plan)
    monkeypatch.setattr(allocate, "AlpacaPaperClient",
                        lambda *a, **k: pytest.fail("broker client constructed"))
    monkeypatch.setattr(allocate, "days_until_earnings",
                        lambda *a, **k: pytest.fail("network earnings path used"))
    for name in ("record_cashflow", "record_interest", "record_margin_sync"):
        monkeypatch.setattr(allocate, name,
                            lambda *a, _name=name, **k: pytest.fail(f"write path used: {_name}"))
    import earnings
    cache_before = dict(earnings._CACHE)
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob("*") if p.is_file()}
    first = _run(tmp_path, supplement)
    second = _run(tmp_path, supplement)
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob("*") if p.is_file()}
    assert first == second
    assert first["canonical_result"] == real_plan(*called[0][0], **called[0][1])
    assert earnings._CACHE == cache_before
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
    assert not result["actionable"] and "conflicting" in result["blocked_reasons"][0]

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


def test_clock_compares_aware_instants_and_preserves_date_only_legacy():
    as_of = private_allocation._parse_timestamp(AS_OF, "as_of")
    equivalent = {"cash": {"balance": 1, "synced_at": "2026-09-16T01:00:00+14:00"}}
    assert allocate.load_cash_state(equivalent, as_of=as_of)["usable"]
    exact_future = {"cash": {"balance": 1, "synced_at": "2026-09-15T12:00:01Z"}}
    assert allocate.load_cash_state(exact_future, as_of=as_of)["state"] == "unknown"
    boundary = {"cash": {"balance": 1, "synced_at": "2026-09-13T12:00:00Z"}}
    assert allocate.load_cash_state(boundary, as_of=as_of)["usable"]
    stale = {"cash": {"balance": 1, "synced_at": "2026-09-13T11:59:59Z"}}
    assert allocate.load_cash_state(stale, as_of=as_of)["state"] == "stale"
    legacy = {"cash": {"balance": 1, "synced_at": __import__("datetime").date.today().isoformat()}}
    assert allocate.load_cash_state(legacy)["usable"]


def test_review_corruption_equal_instant_and_newer_submission_fail_closed(tmp_path):
    _, chosen, supplement = _setup(tmp_path / "corrupt")
    rejected = account_staging.review(tmp_path / "corrupt", supplement["submission_id"],
                                      "rejected", "chatgpt-review")
    path = (tmp_path / "corrupt" / "submissions" / supplement["submission_id"] /
            "reviews" / f"{rejected['review_id']}.json")
    damaged = json.loads(path.read_text())
    damaged["receipt_sha256"] = "0" * 64
    path.write_text(json.dumps(damaged))
    assert "invalid" in _run(tmp_path / "corrupt", supplement)["blocked_reasons"][0]

    _, chosen, supplement = _setup(tmp_path / "tie")
    other = account_staging.review(tmp_path / "tie", supplement["submission_id"],
                                   "confirmed", "chatgpt-review")
    path = (tmp_path / "tie" / "submissions" / supplement["submission_id"] /
            "reviews" / f"{other['review_id']}.json")
    tied = json.loads(path.read_text())
    tied["reviewed_at"] = chosen["reviewed_at"]
    path.write_text(json.dumps(tied, sort_keys=True, separators=(",", ":")) + "\n")
    assert "ambiguous" in _run(tmp_path / "tie", supplement)["blocked_reasons"][0]

    _setup(tmp_path / "newer", _account(identity="first"))
    _, _, old_supplement = _setup(tmp_path / "newer", _account(identity="second"))
    # The first record is now conservatively superseded by the explicitly newer second.
    records = account_staging.snapshot(tmp_path / "newer").records
    oldest = min(records, key=lambda r: private_allocation._parse_timestamp(
        r["received_at"], "received_at"))
    old_supplement["submission_id"] = oldest["submission_id"]
    old_supplement["receipt_sha256"] = hashlib.sha256(
        (tmp_path / "newer" / "submissions" / oldest["submission_id"] / "receipt.json").read_bytes()).hexdigest()
    old_review = oldest["reviews"][0]
    old_supplement["review_id"] = old_review["review_id"]
    old_supplement["review_sha256"] = hashlib.sha256(
        (tmp_path / "newer" / "submissions" / oldest["submission_id"] / "reviews" /
         f"{old_review['review_id']}.json").read_bytes()).hexdigest()
    assert "superseded" in _run(tmp_path / "newer", old_supplement)["blocked_reasons"][0]


def test_policy_and_executing_byte_drift_fail_closed_and_restore(tmp_path):
    _, _, supplement = _setup(tmp_path)
    for path, replacement in ((ROOT / "gates.yaml", b"gates: []\n"),
                              (ROOT / "allocate.py", b"# synthetic drift\n")):
        original = path.read_bytes()
        try:
            path.write_bytes(replacement)
            result = _run(tmp_path, supplement)
            assert not result["actionable"] and "drift" in result["blocked_reasons"][0]
        finally:
            path.write_bytes(original)


@pytest.mark.parametrize("mutation, phrase", [
    (lambda d: d.update(schema_version=True), "schema_version"),
    (lambda d: d["market"][0].update(source_id=None), "source identity"),
    (lambda d: d["market"][0].update(rsi14=900), "outside"),
    (lambda d: d["regime"].update(source_id=""), "source identity"),
    (lambda d: d.update(as_of="0001-01-01T00:00:00+01:00"), "timestamp"),
])
def test_supplement_type_domain_and_boundary_errors_are_controlled(tmp_path, mutation, phrase):
    _, _, supplement = _setup(tmp_path)
    mutation(supplement)
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and result["canonical_result"] is None
    assert phrase in result["blocked_reasons"][0]


def test_gated_market_may_be_omitted_and_unavailable_eligible_is_local(tmp_path):
    _, _, supplement = _setup(tmp_path)
    supplement["market"] = [r for r in supplement["market"] if r["ticker"] != "RKLB"]
    assert _run(tmp_path, supplement)["actionable"]
    row = next(r for r in supplement["market"] if r["ticker"] == "SPY")
    row.update(available=False, price=None, sma200=None, rsi14=None)
    result = _run(tmp_path, supplement)
    assert result["actionable"]
    assert any(r["ticker"] == "SPY" and r["action"] == "BLOCKED"
               for r in result["canonical_result"]["blocked"])


def test_cli_missing_and_oversized_supplement_are_controlled(tmp_path, capsys):
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    common = ["--runtime-root", str(tmp_path), "--source-root", str(ROOT),
              "--expected-source-sha", head, "--supplement"]
    assert private_allocation.main([*common, str(tmp_path / "absent.json")]) == 2
    assert "could not be read" in capsys.readouterr().out
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b"x" * (private_allocation.MAX_SUPPLEMENT_BYTES + 1))
    assert private_allocation.main([*common, str(oversized)]) == 2
    assert "exceeds 512 KiB" in capsys.readouterr().out


@pytest.mark.parametrize("ticker", ["CASH", "RESERVE"])
def test_synthetic_sleeve_holding_collision_cannot_double_count(tmp_path, ticker):
    account = _account(identity=f"collision-{ticker.lower()}")
    account["holdings"][0]["ticker"] = ticker
    _, _, supplement = _setup(tmp_path, account)
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and "collides" in result["blocked_reasons"][0]


def test_date_only_account_evidence_survives_to_provenance(tmp_path):
    account = _account(identity="date-only")
    account["holdings"][0]["observed_at"] = "2026-09-15"
    account["holdings"][0]["valuation"]["observed_at"] = "2026-09-15"
    account["cash"][0]["observed_at"] = "2026-09-15"
    account["debt_margin"][0]["observed_at"] = "2026-09-15"
    _, _, supplement = _setup(tmp_path, account)
    result = _run(tmp_path, supplement)
    assert result["actionable"]
    assert result["provenance"]["observations"][0]["quantity_observed_at"] == "2026-09-15"
    assert result["provenance"]["observations"][0]["valuation_observed_at"] == "2026-09-15"


def test_past_next_earnings_is_rejected(tmp_path):
    _, _, supplement = _setup(tmp_path)
    supplement["earnings"][0]["next_date"] = "2026-09-14"
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and "predates" in result["blocked_reasons"][0]


def test_stale_informational_evidence_degrades_locally_not_globally(tmp_path):
    _, _, supplement = _setup(tmp_path)
    supplement["regime"].update(known=False, observed_at="2026-01-01T00:00:00Z")
    supplement["earnings"][0]["observed_at"] = "2026-01-01"
    market = next(row for row in supplement["market"] if row["ticker"] == "SPY")
    market["observed_at"] = "2026-01-01"
    result = _run(tmp_path, supplement)
    assert result["actionable"] and result["canonical_result"]["regime_known"] is False
    assert any(row["ticker"] == "SPY" for row in result["canonical_result"]["blocked"])


def test_numeric_overflow_and_policy_permission_error_are_controlled(tmp_path, monkeypatch):
    _, _, supplement = _setup(tmp_path)
    supplement["market"][0]["price"] = 10 ** 1000
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and "finite" in result["blocked_reasons"][0]

    _, _, supplement = _setup(tmp_path / "permission", _account(identity="permission"))
    original = Path.read_bytes
    def guarded_read(path):
        if path == ROOT / "gates.yaml":
            raise PermissionError("synthetic denied")
        return original(path)
    monkeypatch.setattr(Path, "read_bytes", guarded_read)
    result = _run(tmp_path / "permission", supplement)
    assert not result["actionable"] and "could not be read" in result["blocked_reasons"][0]
