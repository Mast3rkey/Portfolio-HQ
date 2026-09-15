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


def test_returned_nested_objects_cannot_mutate_storage_templates_or_later_receipts(tmp_path):
    original = synthetic_document(identity="mutable-return", holding_freshness="stale",
                                  include_protected=False)
    first = account_staging.ingest(tmp_path, original)
    receipt_path = tmp_path / "submissions" / first["submission_id"] / "receipt.json"
    persisted = receipt_path.read_bytes()
    first["authority"]["executable"] = True
    first["normalized"]["holdings"][0]["quantity"] = False
    first["issues"][0]["severity"] = "not-material"

    assert receipt_path.read_bytes() == persisted
    stored = account_staging.snapshot(tmp_path).records[0]
    assert stored["authority"] == {"data_only": True, "policy_adopted": False,
                                    "engineering_approved": False, "executable": False}
    assert stored["normalized"]["holdings"][0]["quantity"] == 0
    assert stored["issues"][0]["severity"] == "material"

    later = account_staging.ingest(tmp_path, synthetic_document(identity="later-receipt"))
    assert later["authority"]["executable"] is False
    assert account_staging.snapshot(tmp_path).records[0]["authority"]["executable"] is False


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


def test_submissions_regular_file_is_controlled_storage_failure(tmp_path: Path):
    (tmp_path / "submissions").write_text("not a directory")
    with pytest.raises(account_staging.AccountStorageError, match="could not create"):
        account_staging.ingest(tmp_path, synthetic_document())


def test_root_creation_oserror_is_controlled_storage_failure(tmp_path: Path, monkeypatch):
    target = tmp_path / "runtime" / "submissions"
    real_mkdir = Path.mkdir

    def denied(path, *args, **kwargs):
        if path == target:
            raise PermissionError("synthetic read-only root")
        return real_mkdir(path, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", denied)
    with pytest.raises(account_staging.AccountStorageError, match="could not create"):
        account_staging.ingest(tmp_path / "runtime", synthetic_document())


def test_staging_directory_oserror_is_controlled_storage_failure(tmp_path: Path, monkeypatch):
    target = tmp_path / account_staging.STAGING_DIRNAME
    real_mkdir = Path.mkdir

    def denied(path, *args, **kwargs):
        if path == target:
            raise PermissionError("synthetic read-only staging root")
        return real_mkdir(path, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", denied)
    with pytest.raises(account_staging.AccountStorageError, match="account staging directory"):
        account_staging.ingest(tmp_path, synthetic_document())
    assert account_staging.snapshot(tmp_path).records == ()


def test_authenticated_submit_renders_controlled_root_storage_failure(signed_in):
    root = signed_in["config"].account_root
    root.mkdir(parents=True)
    (root / "submissions").write_text("not a directory")
    status, _, page = signed_in["client"].request(
        "POST", "/accounts/submit", synthetic_document(),
        {"Content-Type": "application/json"})
    assert status == 500
    assert b"storage could not be read" in page
    assert b"No account state is being shown" in page


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
    with pytest.raises(account_staging.AccountStorageError, match="redirected"):
        account_staging.snapshot(tmp_path)
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


def test_snapshot_top_level_enumeration_failure_is_controlled_and_blocks_ingest(
        tmp_path, monkeypatch):
    account_staging.ingest(tmp_path, synthetic_document(identity="retained-before-error"))
    submissions = tmp_path / "submissions"
    before = {entry.name for entry in os.scandir(submissions)}
    real_iterdir = Path.iterdir

    def unavailable(path):
        if path == submissions:
            raise OSError("synthetic submissions enumeration failure")
        return real_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", unavailable)
    with pytest.raises(account_staging.AccountStorageError, match="enumerate retained"):
        account_staging.snapshot(tmp_path)
    with pytest.raises(account_staging.AccountStorageError, match="enumerate retained"):
        account_staging.ingest(tmp_path, synthetic_document(identity="new-while-unavailable"))
    assert {entry.name for entry in os.scandir(submissions)} == before


def test_snapshot_translates_synthetic_root_iterdir_oserror(tmp_path, monkeypatch):
    class UnavailableDirectory:
        def iterdir(self):
            raise OSError("synthetic root iterdir failure")

    monkeypatch.setattr(account_staging, "_root", lambda *_args, **_kwargs: UnavailableDirectory())
    with pytest.raises(account_staging.AccountStorageError, match="enumerate retained"):
        account_staging.snapshot(tmp_path)


def test_review_history_enumeration_failure_blocks_snapshot_and_new_review(
        tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="history-unavailable"))
    account_staging.review(tmp_path, receipt["submission_id"], "rejected", "reviewer-1")
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    before = {entry.name for entry in os.scandir(review_root)}
    real_iterdir = Path.iterdir

    def unavailable(path):
        if path == review_root:
            raise OSError("synthetic review enumeration failure")
        return real_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", unavailable)
    with pytest.raises(account_staging.AccountStorageError, match="enumerate review history"):
        account_staging.snapshot(tmp_path)
    with pytest.raises(account_staging.AccountStorageError, match="enumerate review history"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-2")
    assert {entry.name for entry in os.scandir(review_root)} == before


@pytest.mark.parametrize("complete_before_error", [False, True])
def test_review_write_error_never_publishes_partial_or_complete_final(
        tmp_path, monkeypatch, complete_before_error):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity=(
        "partial-write" if not complete_before_error else "complete-write-error")))
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    real_open = Path.open

    class FailingWrite:
        def __init__(self, handle):
            self.handle = handle

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            self.handle.close()

        def write(self, data):
            amount = len(data) if complete_before_error else max(1, len(data) // 3)
            self.handle.write(data[:amount])
            self.handle.flush()
            raise OSError("synthetic write failure after real bytes")

    def failing_open(path, *args, **kwargs):
        handle = real_open(path, *args, **kwargs)
        return FailingWrite(handle) if path.parent == review_root and path.name.startswith(
            ".review-") else handle

    monkeypatch.setattr(Path, "open", failing_open)
    with pytest.raises(account_staging.AccountStorageError, match="stored immutably"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    assert list(review_root.glob("*.json")) == []
    assert list(review_root.iterdir()) == []
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []


def test_review_close_error_never_publishes_final(tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="close-error"))
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    real_open = Path.open

    class FailingClose:
        def __init__(self, handle):
            self.handle = handle

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            self.handle.close()
            raise OSError("synthetic close failure after real close")

        def write(self, data):
            return self.handle.write(data)

    def failing_open(path, *args, **kwargs):
        handle = real_open(path, *args, **kwargs)
        return FailingClose(handle) if path.parent == review_root and path.name.startswith(
            ".review-") else handle

    monkeypatch.setattr(Path, "open", failing_open)
    with pytest.raises(account_staging.AccountStorageError, match="stored immutably"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    assert list(review_root.iterdir()) == []
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []


def test_review_publication_failure_cleans_temp_and_publishes_nothing(tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="publish-error"))
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"

    def unavailable_link(_source, _destination, **_kwargs):
        raise OSError("synthetic atomic publication failure")

    monkeypatch.setattr(os, "link", unavailable_link)
    with pytest.raises(account_staging.AccountStorageError, match="stored immutably"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    assert list(review_root.iterdir()) == []
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == []


def test_review_serialization_and_temp_creation_fail_before_publication(tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="serialize-error"))
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    real_dumps = json.dumps

    def unavailable_serialization(value, *args, **kwargs):
        if isinstance(value, dict) and "review_id" in value:
            raise ValueError("synthetic review serialization failure")
        return real_dumps(value, *args, **kwargs)

    monkeypatch.setattr(account_staging.json, "dumps", unavailable_serialization)
    with pytest.raises(account_staging.AccountStorageError, match="serialized"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    assert list(review_root.iterdir()) == []
    monkeypatch.setattr(account_staging.json, "dumps", real_dumps)

    real_open = Path.open

    def unavailable_open(path, *args, **kwargs):
        if path.parent == review_root and path.name.startswith(".review-"):
            raise PermissionError("synthetic temporary creation failure")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", unavailable_open)
    with pytest.raises(account_staging.AccountStorageError, match="stored immutably"):
        account_staging.review(tmp_path, receipt["submission_id"], "confirmed", "reviewer-1")
    assert list(review_root.iterdir()) == []


def test_review_cleanup_failure_leaves_only_ignored_temp_remnant(tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="cleanup-error"))
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    real_unlink = Path.unlink

    def unavailable_unlink(path, *args, **kwargs):
        if path.parent == review_root and path.name.startswith(".review-"):
            raise OSError("synthetic temporary cleanup failure")
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", unavailable_unlink)
    review = account_staging.review(
        tmp_path, receipt["submission_id"], "rejected", "reviewer-1")
    entries = list(review_root.iterdir())
    assert sum(path.name == f"{review['review_id']}.json" for path in entries) == 1
    assert sum(path.name.startswith(".review-") for path in entries) == 1
    assert account_staging.snapshot(tmp_path).records[0]["reviews"] == [review]


def test_review_final_collision_never_overwrites_prior_review(tmp_path, monkeypatch):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="review-collision"))
    fixed_id = "20260915T120000Z-0123456789ab"
    monkeypatch.setattr(account_staging, "_new_id", lambda: fixed_id)
    first = account_staging.review(
        tmp_path, receipt["submission_id"], "rejected", "reviewer-first")
    final = tmp_path / "submissions" / receipt["submission_id"] / "reviews" / f"{fixed_id}.json"
    prior_bytes = final.read_bytes()

    with pytest.raises(account_staging.AccountStorageError, match="stored immutably"):
        account_staging.review(
            tmp_path, receipt["submission_id"], "confirmed", "reviewer-second")
    assert final.read_bytes() == prior_bytes
    history = account_staging.snapshot(tmp_path).records[0]["reviews"]
    assert history == [first]
    assert list(final.parent.iterdir()) == [final]


def test_rejected_review_atomic_bytes_restart_and_temp_remnant_handling(tmp_path):
    receipt = account_staging.ingest(tmp_path, synthetic_document(identity="atomic-success"))
    review = account_staging.review(
        tmp_path, receipt["submission_id"], "rejected", "reviewer-1")
    review_root = tmp_path / "submissions" / receipt["submission_id"] / "reviews"
    final = review_root / f"{review['review_id']}.json"
    assert json.loads(final.read_bytes()) == review

    remnant = review_root / ".review-interrupted.tmp"
    remnant.write_bytes(final.read_bytes())
    restarted = account_staging.snapshot(tmp_path)
    assert restarted.records[0]["reviews"] == [review]
    assert final.read_bytes() == (json.dumps(
        review, sort_keys=True, separators=(",", ":")) + "\n").encode()


def test_authenticated_review_publication_failure_has_no_false_confirmation(
        signed_in, monkeypatch):
    root = signed_in["config"].account_root
    receipt = account_staging.ingest(root, synthetic_document(identity="http-publish-error"))
    review_root = root / "submissions" / receipt["submission_id"] / "reviews"

    def unavailable_link(_source, _destination, **_kwargs):
        raise OSError("synthetic atomic publication failure")

    monkeypatch.setattr(os, "link", unavailable_link)
    status, _, page = signed_in["client"].request(
        "POST", f"/accounts/review/{receipt['submission_id']}",
        b"decision=confirmed&reviewer=reviewer-1",
        {"Content-Type": "application/x-www-form-urlencoded"})
    assert status == 409
    assert b"Review not recorded" in page
    assert b"No review decision recorded" in page
    assert b"confirmed by reviewer-1" not in page
    assert list(review_root.iterdir()) == []


def test_authenticated_accounts_get_and_flash_surface_snapshot_storage_failure(
        signed_in, monkeypatch):
    def unavailable(_root):
        raise account_staging.AccountStorageError("synthetic enumeration failure")

    monkeypatch.setattr(account_staging, "snapshot", unavailable)
    status, _, page = signed_in["client"].request("GET", "/accounts")
    assert status == 500
    assert b"storage could not be read" in page
    assert b"No account state is being shown" in page

    status, _, page = signed_in["client"].request(
        "POST", "/accounts/submit", b"{}", {"Content-Type": "application/json"})
    assert status == 500
    assert b"storage could not be read" in page


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
