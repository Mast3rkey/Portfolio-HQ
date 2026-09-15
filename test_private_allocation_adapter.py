"""Synthetic end-to-end coverage for the private allocation adapter."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date, datetime, timezone
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


def _independent_canonical_plan():
    """Rebuild the fixture's canonical plan without going through the adapter.

    Deliberately reconstructed from the fixture's own literals rather than by
    recording ``allocate.plan`` arguments: the adapter now binds loaded code to
    the named commit, so wrapping ``allocate.plan`` would (correctly) be
    refused.  Reproducing the inputs independently is also stronger evidence
    that the adapter changed nothing on the way into the canonical engine.
    """
    as_of = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)
    targets = allocate.load_yaml(ROOT / "targets.yaml")
    roster = allocate.build_roster(targets)
    gates = allocate.load_gates()
    metrics = {t: {"price": 100.0, "sma200": 90.0, "rsi14": 40.0} for t, m in roster.items()
               if m["asset_class"] not in {"crypto", "cash", "reserve"}}
    earn = {t: (date(2026, 10, 15) - as_of.date()).days for t in metrics if t not in gates}
    holdings = {"SYNTH": 100.0}
    holdings_state = {"shares": {"SYNTH": 1.0}, "crypto_shares": {},
                      "cash": {"balance": 100000, "synced_at": "2026-09-15T11:00:00Z"},
                      "margin": {"debt": 0, "buffer_pct": 80.0,
                                 "synced_at": "2026-09-15T11:00:00Z"}}
    cash_state = allocate.load_cash_state(holdings_state, as_of=as_of)
    margin = allocate.load_margin_state(holdings_state, as_of=as_of)
    availability = allocate.current_dollar_availability(
        cash_state, margin, allocate.valuation_completeness(holdings, holdings_state))
    return allocate.plan(targets, holdings, roster, metrics, True, True,
                         cash_state["balance"], margin_debt=0, margin_buffer_pct=80.0,
                         gates_cfg=gates, lookthrough=allocate.load_yaml(ROOT / "issuer_lookthrough.yaml"),
                         holdings_state=holdings_state,
                         dollars_available=availability["available"],
                         earnings_provider=earn.get, as_of=as_of)


def test_retained_bytes_confirmed_version_to_real_noncrypto_plan_is_deterministic(
        tmp_path, monkeypatch):
    receipt, review, supplement = _setup(tmp_path)
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
    assert first["canonical_result"] == _independent_canonical_plan()
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


@pytest.mark.parametrize("separator", [" ", "t"])
def test_legacy_observation_timestamp_separators_survive_real_plan(tmp_path, separator):
    account = _account(identity=f"legacy-separator-{ord(separator)}")
    observed = f"2026-09-15{separator}11:00:00+00:00"
    account["holdings"][0]["observed_at"] = observed
    account["holdings"][0]["valuation"]["observed_at"] = observed
    account["cash"][0]["observed_at"] = observed
    account["debt_margin"][0]["observed_at"] = observed
    _, _, supplement = _setup(tmp_path, account)
    result = _run(tmp_path, supplement)
    assert result["actionable"]
    assert result["provenance"]["observations"][0]["quantity_observed_at"] == observed


def test_expired_historically_valid_earnings_is_canonical_unknown(tmp_path):
    _, _, supplement = _setup(tmp_path)
    ticker = supplement["earnings"][0]["ticker"]
    supplement["earnings"][0].update(
        observed_at="2026-09-10", next_date="2026-09-11")
    result = _run(tmp_path, supplement)
    assert result["actionable"]
    rows = (result["canonical_result"]["buys"] +
            result["canonical_result"]["underweight"] +
            result["canonical_result"]["blocked"])
    assert any(row["ticker"] == ticker and
               row.get("earn_flag") == "earnings:unavailable" for row in rows)
    evidence = next(row for row in result["provenance"]["earnings"]
                    if row["ticker"] == ticker)
    assert evidence["observed_at"] == "2026-09-10"
    assert evidence["next_date"] == "2026-09-11"


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


def test_replacing_a_committed_function_in_memory_fails_closed(tmp_path, monkeypatch):
    """Matching disk bytes must not let patched in-memory code claim the SHA."""
    _, _, supplement = _setup(tmp_path)
    assert _run(tmp_path, supplement)["actionable"] is True
    real_plan = allocate.plan

    def wrapping_plan(*args, **kwargs):  # even a faithful wrapper is different code
        return real_plan(*args, **kwargs)

    monkeypatch.setattr(allocate, "plan", wrapping_plan)
    result = _run(tmp_path, supplement)
    assert not result["actionable"] and result["canonical_result"] is None
    assert result["blocked_reasons"] == [
        "loaded code does not match the named commit: allocate.py:plan"]
    assert "policy" not in result["provenance"]


@pytest.mark.parametrize("module_name, attr", [
    ("allocate.py", "build_roster"),
    ("portfolio_hq/owner/account_staging.py", "_valid_review"),
    ("portfolio_hq/owner/private_allocation.py", "_review_evidence"),
])
def test_binding_covers_every_declared_executing_file(tmp_path, monkeypatch, module_name, attr):
    _, _, supplement = _setup(tmp_path)
    module = {"allocate.py": allocate,
              "portfolio_hq/owner/account_staging.py": account_staging,
              "portfolio_hq/owner/private_allocation.py": private_allocation}[module_name]
    monkeypatch.setattr(module, attr, lambda *a, **k: pytest.fail("patched code ran"))
    result = _run(tmp_path, supplement)
    assert result["blocked_reasons"] == [
        f"loaded code does not match the named commit: {module_name}:{attr}"]


def test_binding_scope_is_defined_functions_not_imported_names(tmp_path, monkeypatch):
    """The declared scope is the functions these files define.

    ``days_until_earnings`` is imported into allocate, so it is outside the
    binding and conftest's repo-wide isolation keeps working.  That is safe
    here only because the adapter injects the earnings provider, so the live
    lookup is never consulted for this result -- assert that too.
    """
    _, _, supplement = _setup(tmp_path)
    monkeypatch.setattr(allocate, "days_until_earnings",
                        lambda *a, **k: pytest.fail("live earnings lookup used"))
    result = _run(tmp_path, supplement)
    assert result["actionable"] is True
    assert any("imported into them" in note for note in result["limitations"])


def test_execution_file_list_and_bound_modules_cannot_drift(tmp_path):
    """A new executing dependency must be bound, not silently unbound."""
    _, _, supplement = _setup(tmp_path)
    original = private_allocation.EXECUTION_FILES
    try:
        private_allocation.EXECUTION_FILES = original + ("indicators.py",)
        result = _run(tmp_path, supplement)
    finally:
        private_allocation.EXECUTION_FILES = original
    assert result["blocked_reasons"] == ["executing dependency binding is incomplete"]


def test_offline_run_opens_no_socket(tmp_path, monkeypatch):
    """Prove absence of network use directly, not just that clients are unused.

    Guarding named client attributes leaves the claim resting on knowing every
    entry point.  Denying the socket layer itself covers paths this test does
    not have to enumerate, including any cache refresh underneath them.
    """
    _, _, supplement = _setup(tmp_path)

    def denied(*args, **kwargs):
        raise AssertionError("socket opened during the offline allocation run")

    monkeypatch.setattr("socket.socket", denied)
    result = _run(tmp_path, supplement)
    assert result["actionable"] is True and result["blocked_reasons"] == []


def test_cli_emits_a_serializable_envelope_for_an_actionable_run(tmp_path, capsys):
    """The documented CLI must return the envelope, not a traceback.

    The canonical result carries a real ``date`` (the retained common-driver
    measurement), so the success path -- the CLI's whole purpose -- is the one
    that exercises the JSON boundary.
    """
    _, _, supplement = _setup(tmp_path)
    path = tmp_path / "supplement.json"
    path.write_bytes(json.dumps(supplement, separators=(",", ":")).encode())
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    code = private_allocation.main([
        "--runtime-root", str(tmp_path), "--supplement", str(path),
        "--source-root", str(ROOT), "--expected-source-sha", head])
    printed = json.loads(capsys.readouterr().out)
    assert code == 0 and printed["actionable"] is True
    assert printed["canonical_result"]["retained_common_driver_measurement"][
        "measured_at"] == "2026-07-30"
    assert printed["provenance"]["policy"]["git_sha"] == head


def test_cli_refuses_an_unserializable_envelope_instead_of_raising(monkeypatch, capsys):
    monkeypatch.setattr(private_allocation, "run",
                        lambda *a, **k: {"actionable": True, "canonical_result": {"x": object()}})
    code = private_allocation.main([
        "--runtime-root", str(ROOT), "--supplement", str(ROOT / "targets.yaml"),
        "--source-root", str(ROOT), "--expected-source-sha", "0" * 40])
    printed = json.loads(capsys.readouterr().out)
    assert code == 2 and printed["actionable"] is False
    assert printed["blocked_reasons"] == [
        "output.canonical_result.x is not JSON-serializable: object"]


def test_level1_sleeve_view_reports_governed_targets_and_observed_gaps(tmp_path):
    _, _, supplement = _setup(tmp_path)
    result = _run(tmp_path, supplement)
    level1 = result["level1"]
    assert result["actionable"] is True and level1["dollars_known"] is True
    assert level1["status"] == "CURRENT_ACCEPTED_POLICY_SNAPSHOT"
    assert level1["policy_source"] == "targets.yaml"

    # Percentages are the accepted policy, copied not recomputed.
    summary = __import__("level1_policy_summary").load_policy_summary(ROOT / "targets.yaml")
    for name, sleeve in level1["sleeves"].items():
        assert sleeve["governed_target_pct"] == summary["sleeves_pct"][name]
        assert sleeve["members"] == summary["members"][name]

    # The fixture holds only cash plus one off-roster ticker.
    cash_sleeve = level1["sleeves"]["cash_and_reserve"]
    assert cash_sleeve["current_value"] == 100000.0
    assert cash_sleeve["exposure_basis"] == "tracked cash balance"
    # Overweight cash shows as a negative gap against a 5% governed weight.
    assert cash_sleeve["gap_value"] < 0
    equity = level1["sleeves"]["direct_equity"]
    assert equity["current_value"] == 0.0 and equity["gap_value"] > 0
    assert equity["target_value"] == pytest.approx(
        result["canonical_result"]["book"] * 63.25 / 100)


def test_level1_uses_the_governed_mapping_not_an_asset_class_rollup(tmp_path):
    """GLD and SPY are both funds but sit in different accepted sleeves."""
    _, _, supplement = _setup(tmp_path)
    level1 = _run(tmp_path, supplement)["level1"]
    broad = set(level1["sleeves"]["broad_market_funds"]["members"])
    gold = set(level1["sleeves"]["gold_defensive"]["members"])
    assert "GLD" in gold and "GLD" not in broad
    assert {"SPY", "VEA", "VWO"} <= broad
    assert not broad & gold


def test_level1_withholds_dollars_when_the_book_is_unavailable(tmp_path):
    _, _, supplement = _setup(tmp_path)
    supplement.pop("buffer")  # book becomes unavailable, per the canonical rule
    result = _run(tmp_path, supplement)
    assert result["canonical_result"]["book"] is None
    level1 = result["level1"]
    assert level1["dollars_known"] is False
    assert "book is unavailable" in level1["withheld_reason"]
    for sleeve in level1["sleeves"].values():
        # Policy survives; every observed and derived dollar is withheld.
        assert sleeve["governed_target_pct"] and sleeve["members"]
        assert sleeve["current_value"] is None and sleeve["current_pct"] is None
        assert sleeve["target_value"] is None and sleeve["gap_value"] is None


def test_level1_discloses_holdings_outside_the_accepted_roster(tmp_path):
    _, _, supplement = _setup(tmp_path)
    level1 = _run(tmp_path, supplement)["level1"]
    assert level1["unassigned_holdings"] == {"SYNTH": 100.0}
    for sleeve in level1["sleeves"].values():
        assert "SYNTH" not in sleeve["members"]


def test_level1_never_redistributes_the_unallocated_policy_weight(tmp_path):
    _, _, supplement = _setup(tmp_path)
    level1 = _run(tmp_path, supplement)["level1"]
    assert level1["unallocated_policy_pct"] == "0.75"
    assert level1["reconciliation"]["assigned_pct"] == "99.25"
    assigned = sum(float(s["governed_target_pct"]) for s in level1["sleeves"].values())
    assert assigned == pytest.approx(99.25)


def test_non_actionable_envelope_still_carries_the_level1_key(tmp_path):
    _, _, supplement = _setup(tmp_path)
    supplement["schema_version"] = 99
    result = _run(tmp_path, supplement)
    assert result["actionable"] is False
    assert result["canonical_result"] is None and result["level1"] is None


def test_sleeve_policy_module_is_byte_verified_and_code_bound(tmp_path, monkeypatch):
    """The sleeve mapping must carry the allocator's own provenance."""
    _, _, supplement = _setup(tmp_path)
    assert "level1_policy_summary.py" in private_allocation.EXECUTION_FILES
    baseline = _run(tmp_path, supplement)
    assert "level1_policy_summary.py" in baseline["provenance"]["policy"]["execution_sha256"]

    import level1_policy_summary
    monkeypatch.setattr(level1_policy_summary, "build_policy_summary",
                        lambda *a, **k: pytest.fail("patched sleeve policy ran"))
    result = _run(tmp_path, supplement)
    assert result["blocked_reasons"] == [
        "loaded code does not match the named commit: "
        "level1_policy_summary.py:build_policy_summary"]


def test_level1_withholds_only_the_undefined_percentage_at_a_zero_book(tmp_path):
    """A zero book makes a share OF the book undefined, not the dollars.

    Reachable through confirmed evidence, not a contrived state: holdings
    exactly offset by margin debt give book == 0 with no staging issue and an
    actionable run. decimal raises ZeroDivisionError rather than ValueError, so
    an unguarded division here would leave the controlled envelope entirely.
    """
    account = _account()                        # SYNTH qty 1 @ 100 -> invested 100
    account["cash"][0]["balance"] = 0
    account["debt_margin"][0]["balance"] = 100  # book = 100 + 0 - 100
    _, _, supplement = _setup(tmp_path, account)
    result = _run(tmp_path, supplement)
    assert result["canonical_result"] is not None, result["blocked_reasons"]
    assert result["canonical_result"]["book"] == 0
    level1 = result["level1"]
    assert level1["dollars_known"] is True
    for name, sleeve in level1["sleeves"].items():
        assert sleeve["target_value"] == 0.0
        assert sleeve["current_pct"] is None, name
        assert sleeve["gap_value"] == -sleeve["current_value"]
    # SYNTH is off-roster, so no sleeve claims the one held position.
    assert level1["unassigned_holdings"] == {"SYNTH": 100.0}
    assert level1["sleeves"]["direct_equity"]["current_value"] == 0.0


def test_envelope_states_every_observed_position_including_ones_at_target(tmp_path):
    """A position already at or above target appears in no plan() row.

    Without an echo of what was observed, most of a real portfolio would be
    absent from the envelope and the Level-1 sleeve percentages would be
    unexplainable. Off-roster holdings were already disclosed with values, so
    on-roster ones must be too.
    """
    account = _account()
    # Small cash keeps the book small, so SPY's holding exceeds its target.
    account["cash"][0]["balance"] = 1000
    account["holdings"] = [
        # SPY above its governed target: a candidate in no plan() row section.
        {"ticker": "SPY", "quantity": 30, "observed_at": "2026-09-15T11:00:00Z",
         "freshness": "current",
         "valuation": {"unit_price": 560.0, "currency": "USD",
                       "observed_at": "2026-09-15T10:00:00Z", "freshness": "current"}},
        {"ticker": "SYNTH", "quantity": 1, "observed_at": "2026-09-15T11:00:00Z",
         "freshness": "current",
         "valuation": {"unit_price": 100.0, "currency": "USD",
                       "observed_at": "2026-09-15T10:00:00Z", "freshness": "current"}},
    ]
    _, _, supplement = _setup(tmp_path, account)
    result = _run(tmp_path, supplement)
    assert result["actionable"] is True
    cr = result["canonical_result"]
    listed = {row["ticker"] for section in ("buys", "underweight", "blocked", "trims",
                                            "no_add_gated")
              for row in cr[section]}
    assert "SPY" not in listed, "fixture no longer exercises an at-or-above-target name"

    observed = {row["ticker"]: row for row in result["provenance"]["observations"]}
    assert observed["SPY"]["quantity"] == 30
    assert observed["SPY"]["unit_price"] == 560.0
    assert observed["SPY"]["value"] == 30 * 560.0
    # The echo is internally checkable: quantity * unit_price == value.
    for row in observed.values():
        assert row["value"] == pytest.approx(row["quantity"] * row["unit_price"])
    # It reconciles with the sleeve it feeds.
    assert result["level1"]["sleeves"]["broad_market_funds"]["current_value"] == 30 * 560.0


def test_observed_positions_survive_when_book_derived_dollars_are_withheld(tmp_path):
    """Confirmed observations carry no book dependency, so they are not withheld."""
    _, _, supplement = _setup(tmp_path)
    supplement.pop("buffer")
    result = _run(tmp_path, supplement)
    assert result["canonical_result"]["book"] is None
    assert result["level1"]["dollars_known"] is False
    observed = {row["ticker"]: row for row in result["provenance"]["observations"]}
    assert observed["SYNTH"]["value"] == 100.0 and observed["SYNTH"]["quantity"] == 1
