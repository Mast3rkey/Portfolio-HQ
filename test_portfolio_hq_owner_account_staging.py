"""Adversarial synthetic tests for private manual-account staging."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from portfolio_hq.owner import account_staging, render
from test_portfolio_hq_owner_interface import multipart, owner_env, signed_in  # noqa: F401


def synthetic_document(*, identity="synthetic-v1", holding_freshness="current",
                       include_protected=True, basis="synthetic fixture"):
    doc = {
        "schema_version": 1,
        "client_submission_id": identity,
        "submitted_at": "2026-09-14T12:00:00Z",
        "holdings": [{"ticker": "SYNTH", "quantity": 0,
                      "observed_at": "2026-09-14T11:00:00Z",
                      "freshness": holding_freshness,
                      "valuation": {"unit_price": 12.5, "currency": "USD",
                                    "observed_at": "2026-09-14T10:00:00Z",
                                    "freshness": holding_freshness}}],
        "cash": [{"account_id": "synthetic-cash", "balance": 0,
                  "currency": "USD", "observed_at": "2026-09-14T11:00:00Z",
                  "freshness": "current"}],
        "debt_margin": [{"account_id": "synthetic-margin", "balance": 0,
                         "currency": "USD", "observed_at": "2026-09-14T11:00:00Z",
                         "freshness": "unknown"}],
        "protected_capital": ([{"evidence_id": "synthetic-reserve", "amount": 25,
                                "currency": "USD", "observed_at": "2026-09-14T11:00:00Z",
                                "freshness": "current", "basis": basis}]
                              if include_protected else []),
    }
    return json.dumps(doc, separators=(",", ":")).encode()


def sized_document(size: int, *, identity: str) -> bytes:
    seed = synthetic_document(identity=identity, basis="")
    assert len(seed) <= size
    result = synthetic_document(identity=identity, basis="x" * (size - len(seed)))
    assert len(result) == size
    return result


def test_exact_bytes_receipt_zero_and_restart_persistence(tmp_path: Path):
    original = synthetic_document()
    receipt = account_staging.ingest(tmp_path, original)
    assert receipt["byte_size"] == len(original)
    assert receipt["submission_sha256"] == hashlib.sha256(original).hexdigest()
    assert receipt["normalized"]["holdings"][0]["quantity"] == 0
    assert receipt["normalized"]["cash"][0]["balance"] == 0
    restarted = account_staging.snapshot(tmp_path)
    assert restarted.originals[receipt["submission_id"]] == original
    assert restarted.records[0]["reviews"] == []


def test_receipt_bound_is_enforced_before_publication_and_near_boundary_roundtrips(tmp_path):
    # Exact independent-review reproduction: valid input below 2 MiB whose
    # normalized receipt used to exceed the reader's 128 KiB ceiling.
    overflowing = sized_document(131_833, identity="receipt-overflow")
    with pytest.raises(account_staging.AccountSubmissionRejected, match="receipt larger"):
        account_staging.ingest(tmp_path / "overflow", overflowing)
    assert account_staging.snapshot(tmp_path / "overflow").records == ()

    accepted = sized_document(130_500, identity="receipt-near-boundary")
    receipt = account_staging.ingest(tmp_path / "accepted", accepted)
    view = account_staging.snapshot(tmp_path / "accepted")
    receipt_path = (tmp_path / "accepted" / "submissions" / receipt["submission_id"]
                    / "receipt.json")
    assert account_staging.MAX_RECEIPT_BYTES - receipt_path.stat().st_size < 1024
    assert view.originals[receipt["submission_id"]] == accepted
    assert account_staging.original(tmp_path / "accepted", receipt["submission_id"]) == accepted


@pytest.mark.parametrize("mutator", [
    lambda b: b.replace(b'"quantity":0', b'"quantity":true'),
    lambda b: b.replace(b'"quantity":0', b'"quantity":NaN'),
    lambda b: b.replace(b'"schema_version":1', b'"schema_version":1,"schema_version":1'),
    lambda b: b.replace(b'"observed_at":"2026-09-14T11:00:00Z"', b'"observed_at":"missing"', 1),
])
def test_malformed_nonfinite_boolean_duplicate_key_and_invalid_date_fail_closed(tmp_path, mutator):
    with pytest.raises(account_staging.AccountSubmissionRejected):
        account_staging.ingest(tmp_path, mutator(synthetic_document()))
    assert account_staging.snapshot(tmp_path).records == ()


def test_missing_stale_duplicate_identity_and_changed_content(tmp_path: Path):
    stale = account_staging.ingest(tmp_path, synthetic_document(
        identity="stale", holding_freshness="stale", include_protected=False))
    codes = {issue["code"] for issue in stale["issues"]}
    assert {"stale_holding", "missing_protected_capital"} <= codes
    with pytest.raises(account_staging.AccountReviewRejected, match="material discrepancies"):
        account_staging.review(tmp_path, stale["submission_id"], "confirmed", "reviewer-1")
    rejected = account_staging.review(tmp_path, stale["submission_id"], "rejected", "reviewer-1")
    assert rejected["decision"] == "rejected"
    with pytest.raises(account_staging.AccountSubmissionRejected, match="already used"):
        account_staging.ingest(tmp_path, synthetic_document(identity="stale"))


@pytest.mark.parametrize("decision", [
    [], {}, [[]], {"nested": []}, set(), 1, True, None, 1.0, "other",
])
def test_public_review_api_rejects_every_wrong_decision_type_without_writing(
        tmp_path: Path, decision):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    reviews = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    with pytest.raises(account_staging.AccountReviewRejected, match="decision must be"):
        account_staging.review(tmp_path, receipt["submission_id"], decision, "reviewer-1")
    assert list(reviews.iterdir()) == []


def test_confirmation_binds_exact_submission_and_receipt_and_tampering_hides_record(tmp_path: Path):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    review = account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    assert review["submission_sha256"] == receipt["submission_sha256"]
    directory = tmp_path / "submissions" / receipt["submission_id"]
    (directory / "submission.json").write_bytes(synthetic_document(identity="changed"))
    assert account_staging.snapshot(tmp_path).records == ()
    assert account_staging.original(tmp_path, receipt["submission_id"]) is None


def test_tampered_receipt_or_review_binding_is_not_trusted(tmp_path: Path):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    review = account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    directory = tmp_path / "submissions" / receipt["submission_id"]
    review_path = directory / "reviews" / f"{review['review_id']}.json"
    altered = json.loads(review_path.read_text())
    altered["receipt_sha256"] = "0" * 64
    review_path.write_text(json.dumps(altered))
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []
    receipt_path = directory / "receipt.json"
    stored = json.loads(receipt_path.read_text())
    stored["byte_size"] += 1
    receipt_path.write_text(json.dumps(stored))
    assert account_staging.snapshot(tmp_path).records == ()


def test_receipt_identity_is_reconstructed_from_original_and_cannot_be_reused(tmp_path: Path):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    directory = tmp_path / "submissions" / receipt["submission_id"]
    receipt_path = directory / "receipt.json"
    forged = json.loads(receipt_path.read_text())
    forged["client_submission_id"] = "forged-client"
    receipt_path.write_text(json.dumps(forged, sort_keys=True, separators=(",", ":")) + "\n")
    assert account_staging.snapshot(tmp_path).records == ()
    with pytest.raises(account_staging.AccountReviewRejected, match="binding is invalid"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    with pytest.raises(account_staging.AccountSubmissionRejected, match="already used"):
        account_staging.ingest(tmp_path, synthetic_document())


@pytest.mark.parametrize("mutation", [
    lambda review: review.update(decision="confirmed"),
    lambda review: review.update(review_id="wrong-id"),
    lambda review: review.update(schema_version=True),
])
def test_review_semantics_are_reconstructed_not_trusted(tmp_path: Path, mutation):
    stale = json.loads(synthetic_document(identity="stale-review",
                                          holding_freshness="stale"))
    stale["cash"][0]["freshness"] = "stale"
    stale["debt_margin"][0]["freshness"] = "stale"
    stale["protected_capital"][0]["freshness"] = "stale"
    receipt = account_staging.ingest(
        tmp_path, json.dumps(stale, separators=(",", ":")).encode())
    assert len(receipt["issues"]) == 4
    review = account_staging.review(tmp_path, receipt["submission_id"], "rejected", "reviewer-1")
    path = (tmp_path / "submissions" / receipt["submission_id"] / "reviews"
            / f"{review['review_id']}.json")
    forged = json.loads(path.read_text())
    mutation(forged)
    path.write_text(json.dumps(forged, sort_keys=True, separators=(",", ":")) + "\n")
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []


@pytest.mark.parametrize(("field", "value"), [
    ("decision", []), ("decision", {}), ("review_id", []),
    ("submission_id", {}), ("reviewer", []), ("reviewed_at", {}),
    ("submission_sha256", []), ("receipt_sha256", {}), ("meaning", []),
])
def test_wrong_persisted_review_field_types_are_ignored_without_crashing(
        tmp_path: Path, field, value):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    review = account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    path = (tmp_path / "submissions" / receipt["submission_id"] / "reviews"
            / f"{review['review_id']}.json")
    malformed = json.loads(path.read_text())
    malformed[field] = value
    path.write_text(json.dumps(malformed, separators=(",", ":")))
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []


@pytest.mark.parametrize("mutation", [
    lambda receipt: receipt["normalized"]["holdings"][0].update(quantity=False),
    lambda receipt: receipt["normalized"]["cash"][0].update(balance=False),
    lambda receipt: receipt["normalized"]["debt_margin"][0].update(balance=False),
    lambda receipt: receipt["normalized"]["protected_capital"][0].update(amount=False),
    lambda receipt: receipt["normalized"].update(schema_version=False),
    lambda receipt: receipt["authority"].update(data_only=1),
])
def test_nested_receipt_types_must_exactly_match_original_derived_types(tmp_path, mutation):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    path = tmp_path / "submissions" / receipt["submission_id"] / "receipt.json"
    malformed = json.loads(path.read_text())
    mutation(malformed)
    path.write_text(json.dumps(malformed, sort_keys=True, separators=(",", ":")) + "\n")
    assert account_staging.snapshot(tmp_path).records == ()
    with pytest.raises(account_staging.AccountReviewRejected, match="binding is invalid"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")


def test_legitimate_integer_and_float_numeric_forms_remain_distinct_and_accepted(tmp_path):
    integer = account_staging.ingest(tmp_path, synthetic_document(identity="integer-zero"))
    floating_doc = json.loads(synthetic_document(identity="float-zero"))
    floating_doc["holdings"][0]["quantity"] = 0.0
    floating = account_staging.ingest(
        tmp_path, json.dumps(floating_doc, separators=(",", ":")).encode())
    records = {record["submission_id"]: record for record in account_staging.snapshot(tmp_path).records}
    assert type(records[integer["submission_id"]]["normalized"]["holdings"][0]["quantity"]) is int
    assert type(records[floating["submission_id"]]["normalized"]["holdings"][0]["quantity"]) is float


def _one_retained_directory(root: Path) -> Path:
    entries = list((root / "submissions").iterdir())
    assert len(entries) == 1
    return entries[0]


@pytest.mark.parametrize("damage", ["invalid_json", "oversized", "symlink", "nonregular"])
def test_damaged_retained_original_blocks_all_new_identity_claims(tmp_path: Path, damage):
    first = synthetic_document(identity="dup-a")
    account_staging.ingest(tmp_path, first)
    directory = _one_retained_directory(tmp_path)
    original = directory / "submission.json"
    if damage == "invalid_json":
        original.write_bytes(b"{invalid")
    elif damage == "oversized":
        original.write_bytes(b" " * (account_staging.MAX_SUBMISSION_BYTES + 1))
    elif damage == "symlink":
        external = tmp_path / "external-original.json"
        original.rename(external)
        original.symlink_to(external)
    else:
        original.unlink()
        original.mkdir()
    with pytest.raises(account_staging.AccountStorageError, match="cannot prove"):
        account_staging.ingest(tmp_path, first)
    assert _one_retained_directory(tmp_path) == directory


def test_redirected_or_nonregular_retained_entry_blocks_new_identity(tmp_path: Path):
    account_staging.ingest(tmp_path, synthetic_document(identity="dup-a"))
    directory = _one_retained_directory(tmp_path)
    external = tmp_path / "external-entry"
    directory.rename(external)
    directory.symlink_to(external, target_is_directory=True)
    with pytest.raises(account_staging.AccountStorageError, match="redirected or nonregular"):
        account_staging.ingest(tmp_path, synthetic_document(identity="distinct-b"))
    assert list((tmp_path / "submissions").iterdir()) == [directory]
    assert directory.is_symlink()
    assert {path.name for path in external.iterdir()} == {
        "submission.json", "receipt.json", "reviews"}


def test_retained_original_read_error_blocks_new_identity(tmp_path: Path, monkeypatch):
    account_staging.ingest(tmp_path, synthetic_document(identity="dup-a"))
    original = _one_retained_directory(tmp_path) / "submission.json"
    real_open = Path.open

    def denied(path, *args, **kwargs):
        if path == original and (not args or args[0] == "rb"):
            raise PermissionError("synthetic denied read")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", denied)
    with pytest.raises(account_staging.AccountStorageError, match="original is unavailable"):
        account_staging.ingest(tmp_path, synthetic_document(identity="distinct-b"))
    assert _one_retained_directory(tmp_path).name == original.parent.name


def test_valid_unrelated_retained_entry_allows_a_distinct_identity(tmp_path: Path):
    first = account_staging.ingest(tmp_path, synthetic_document(identity="identity-a"))
    second = account_staging.ingest(tmp_path, synthetic_document(identity="identity-b"))
    assert first["submission_id"] != second["submission_id"]
    assert len(account_staging.snapshot(tmp_path).records) == 2


def test_oversize_bounded_read_and_symlink_containment(tmp_path: Path):
    with pytest.raises(account_staging.AccountSubmissionRejected, match="2 MiB"):
        account_staging.ingest(tmp_path, b"{" + b" " * account_staging.MAX_SUBMISSION_BYTES)
    outside = tmp_path / "outside"
    outside.mkdir()
    root = tmp_path / "runtime"
    root.mkdir()
    os.symlink(outside, root / "submissions")
    with pytest.raises(account_staging.AccountStorageError, match="symbolic link"):
        account_staging.ingest(root, synthetic_document())
    assert list(outside.iterdir()) == []


def test_persisted_oversize_and_redirected_review_history_fail_closed(tmp_path: Path):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    directory = tmp_path / "submissions" / receipt["submission_id"]
    receipt_path = directory / "receipt.json"
    receipt_path.write_bytes(b" " * (account_staging.MAX_RECEIPT_BYTES + 1))
    assert account_staging.snapshot(tmp_path).records == ()

    second = account_staging.ingest(tmp_path, synthetic_document(identity="review-link"))
    second_dir = tmp_path / "submissions" / second["submission_id"]
    (second_dir / "reviews").rmdir()
    outside = tmp_path / "outside-reviews"
    outside.mkdir()
    os.symlink(outside, second_dir / "reviews")
    with pytest.raises(account_staging.AccountStorageError, match="redirected"):
        account_staging.review(tmp_path, second["submission_id"], "confirmed", "reviewer-1")
    assert list(outside.iterdir()) == []


def test_review_file_symlink_is_rejected_without_opening_external_target(tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document())
    review = account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    review_path = (tmp_path / "submissions" / receipt["submission_id"] / "reviews"
                   / f"{review['review_id']}.json")
    outside = tmp_path / "external-review.json"
    review_path.rename(outside)
    review_path.symlink_to(outside)
    opened = []
    real_open = Path.open

    def recording_open(path, *args, **kwargs):
        opened.append(path)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", recording_open)
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []
    assert outside not in opened
    assert review_path not in opened


def test_huge_integer_is_controlled_rejection_in_domain_and_authenticated_http(signed_in):
    huge = synthetic_document(identity="huge-number").replace(b'"quantity":0',
                                                                      b'"quantity":1' + b"0" * 400)
    with pytest.raises(account_staging.AccountSubmissionRejected, match="numeric range"):
        account_staging.ingest(signed_in["config"].account_root, huge)
    status, _, page = signed_in["client"].request(
        "POST", "/accounts/submit", huge, {"Content-Type": "application/json"})
    assert status == 400
    assert b"outside the supported finite numeric range" in page
    assert account_staging.snapshot(signed_in["config"].account_root).records == ()


def test_malformed_review_cannot_break_authenticated_accounts_page_or_flash(signed_in):
    root = signed_in["config"].account_root
    original = synthetic_document(identity="malformed-review-page")
    receipt = account_staging.ingest(root, original)
    review = account_staging.review(root, receipt["submission_id"], "confirmed", "reviewer-1")
    path = root / "submissions" / receipt["submission_id"] / "reviews" / f"{review['review_id']}.json"
    malformed = json.loads(path.read_text())
    malformed["decision"] = []
    path.write_text(json.dumps(malformed, separators=(",", ":")))

    status, _, page = signed_in["client"].request("GET", "/accounts")
    assert status == 200 and b"No review decision recorded" in page
    status, _, page = signed_in["client"].request(
        "POST", "/accounts/submit", original, {"Content-Type": "application/json"})
    assert status == 400 and b"Submission rejected" in page
    assert b"No review decision recorded" in page


def test_authenticated_http_journey_cross_origin_and_html_escaping(signed_in):
    client = signed_in["client"]
    original = synthetic_document(identity="synthetic-html")
    body, content_type = multipart({}, {"account": ("<account>.json", original)})
    status, _, page = client.request("POST", "/accounts/submit", body,
                                     {"Content-Type": content_type})
    assert status == 200
    assert b"Exact submission retained" in page
    records = account_staging.snapshot(signed_in["config"].account_root).records
    submission_id = records[0]["submission_id"]
    status, _, retained = client.request("GET", f"/accounts/original/{submission_id}")
    assert status == 200 and retained == original
    status, _, _ = client.request("POST", f"/accounts/review/{submission_id}",
                                  b"decision=confirmed&reviewer=%3Cowner%3E",
                                  {"Content-Type": "application/x-www-form-urlencoded"})
    assert status == 409  # unknown debt freshness is not itself invented as stale; no missing material issue
    # The fixture has no material issue; reviewer syntax, not HTML, is rejected.
    status, _, page = client.request("POST", f"/accounts/review/{submission_id}",
                                     b"decision=confirmed&reviewer=owner-1",
                                     {"Content-Type": "application/x-www-form-urlencoded"})
    assert status == 200 and b"data confirmation only" in page
    status, _, _ = client.request("POST", "/accounts/submit", body,
                                  {"Content-Type": content_type,
                                   "Origin": "https://attacker.invalid"})
    assert status == 403


def test_anonymous_denial_and_scriptless_responsive_render(owner_env):
    status, headers, _ = owner_env["client"].request("GET", "/accounts", use_cookie=False)
    assert status == 303 and headers["Location"] == "/login"
    markup = render.accounts_page([{
        "submission_id": "id<script>", "client_submission_id": "<b>bad</b>",
        "received_at": "now", "byte_size": 1, "submission_sha256": "x",
        "normalized": {}, "issues": [{"code": "<x>", "message": "<script>"}],
        "reviews": [],
    }])
    assert "<script>" not in markup and "&lt;script&gt;" in markup
    assert 'name="viewport"' in markup and "<script" not in markup
