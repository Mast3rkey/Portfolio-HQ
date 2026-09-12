"""Synthetic binding tests for the optional private chart-evidence reader."""
from __future__ import annotations

import hashlib
import json
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer

import pytest

from portfolio_hq.owner import chart_evidence, chart_inbox, render
from portfolio_hq.owner import service as service_mod
from portfolio_hq.owner.export_io import write_export
from test_portfolio_hq_owner_chart_inbox import png_bytes
from test_portfolio_hq_owner_interface import Client, _sample_export, multipart, TOKEN


def _artifacts(inbox: Path, *, reviewer="independent-ai", mutate=None):
    image = png_bytes()
    receipt = chart_inbox.ingest(inbox, image, display_filename="chart.png",
        declared_ticker="NVDA", declared_timeframe="Daily",
        allowed_tickers=frozenset({"NVDA"}), allowed_timeframes=frozenset({"Daily"}))
    # The receipt hash the evidence declares is the hash of the receipt actually
    # stored, so a fixture binds the real bytes rather than a placeholder.
    receipt_sha = hashlib.sha256(
        chart_inbox.read_receipt(inbox, receipt["intake_id"])[0]).hexdigest()
    record = {"record_id": "r1", "lifecycle": {}, "identity_and_capture": {
        "ticker": "NVDA", "intake_id": receipt["intake_id"], "visible_timeframe": "1D",
        "retained_image_sha256": receipt["content_sha256"], "receipt_sha256": receipt_sha,
        "visible_export_attribution_timestamp": "2026-09-11T15:34:00-04:00"},
        "content": {"visible_facts": [{"id": "f", "text": "synthetic fact", "source": {
                         "intake_id": receipt["intake_id"], "retained_image_sha256": receipt["content_sha256"]}}],
                    "observations": [{"id": "o", "text": "synthetic observation", "source": {
                         "intake_id": receipt["intake_id"], "retained_image_sha256": receipt["content_sha256"]}}],
                    "inferences": [{"id": "i", "text": "synthetic inference", "basis": ["f", "o"], "status": "tentative"}],
                    "uncertainties": ["unknown feed"]},
        "prohibited_uses": ["no allocation"], "provenance": {"draft_independent_reviewer": "draft-ai"}}
    draft = {"document_type": "private_advisory_chart_evidence_draft",
             "status": "AWAITING_CHATGPT_INDEPENDENT_REVIEW", "records": [record]}
    if mutate: mutate(record)
    analysis = inbox.parent / "analysis.json"; analysis.write_text(json.dumps(draft))
    data = analysis.read_bytes()
    review = {"schema_version": 1, "review_id": "synthetic-review-1", "review_kind": "independent_private_analytical_artifact_review",
      "reviewer": reviewer, "reviewed_at_utc": "2026-09-12T00:00:00Z",
      "verdict": "CLEAN_FOR_PRIVATE_ADVISORY_REFERENCE", "severity_counts": {"BLOCKING": 0, "MAJOR": 0, "MINOR": 0},
      "findings": [], "material_corrections_required": False,
      "principal_acceptance": None, "portfolio_policy_acceptance": False,
      "reviewed_artifact": {"filename": "private-review.zip", "byte_size": 1,
                              "sha256": "not-the-analysis", "files": {"chart-evidence-draft.json": {
                                  "byte_size": len(data), "sha256": hashlib.sha256(data).hexdigest()}}},
      "records": [{"record_id": "r1", "ticker": "NVDA", "intake_id": receipt["intake_id"],
        "retained_image_sha256": receipt["content_sha256"], "receipt_sha256": receipt_sha,
        "visible_timeframe": "1D", "visible_export_attribution_timestamp": "2026-09-11T15:34:00-04:00", "mechanical_result": "pass",
        "image_claim_review_result": "supported within stated limits", "claimed_ids_reviewed": ["f", "o", "i"], "findings": []}], "limitations": ["hash regeneration incomplete"], "methods": ["synthetic mechanical review"]}
    review_path = inbox.parent / "review.json"; review_path.write_text(json.dumps(review))
    return receipt, analysis, review_path


def test_matching_external_review_binds_daily_receipt_to_1d_evidence(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    found = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    assert found[receipt["intake_id"]]["state"] == "reviewed"
    assert found[receipt["intake_id"]]["export_attribution_time"].endswith("-04:00")


def test_reviewer_name_is_not_a_trust_signal_and_wrong_image_hash_fails_closed(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox", reviewer="draft-ai")
    # The separately provisioned artifact is the trust boundary; comparing
    # strings to the pending draft reviewer would neither prove nor disprove it.
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "reviewed"
    receipt, analysis, review = _artifacts(tmp_path / "other")
    payload = json.loads(review.read_text()); payload["records"][0]["retained_image_sha256"] = "0" * 64
    review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(tmp_path / "other", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def test_malformed_duplicate_key_and_oversized_artifacts_degrade_safely(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    analysis.write_text('{"document_type":"x","document_type":"y"}')
    found = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    assert found[receipt["intake_id"]]["state"] == "unverified"
    analysis.write_bytes(b" " * (chart_evidence.MAX_ARTIFACT_BYTES + 1))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def test_missing_reviewer_and_major_finding_fail_closed(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    payload = json.loads(review.read_text()); payload["reviewer"] = ""
    review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"
    _, analysis, review = _artifacts(tmp_path / "other")
    payload = json.loads(review.read_text()); payload["findings"] = [{"severity": "MAJOR"}]
    payload["severity_counts"]["MAJOR"] = 1; review.write_text(json.dumps(payload))
    assert all(v["state"] == "unverified" for v in chart_evidence.reviewed_evidence(tmp_path / "other", analysis, review).values())


def test_bad_nested_type_does_not_raise(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    payload = json.loads(review.read_text()); payload["reviewed_artifact"] = []
    review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def test_invalid_review_date_and_unhashable_nested_values_fail_closed(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    payload = json.loads(review.read_text()); payload["reviewed_at_utc"] = "not-a-date"
    review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"
    _, analysis, review = _artifacts(tmp_path / "other")
    payload = json.loads(review.read_text()); payload["records"][0]["record_id"] = []
    review.write_text(json.dumps(payload))
    assert all(v["state"] == "unverified" for v in chart_evidence.reviewed_evidence(tmp_path / "other", analysis, review).values())
    _, analysis, review = _artifacts(tmp_path / "third")
    payload = json.loads(review.read_text()); payload["records"][0]["claimed_ids_reviewed"] = [{}]
    review.write_text(json.dumps(payload))
    assert all(v["state"] == "unverified" for v in chart_evidence.reviewed_evidence(tmp_path / "third", analysis, review).values())


@pytest.mark.parametrize("stamp,expected", [
    # A trailing Z and an explicit numeric offset both carry a zone.
    ("2026-09-12T00:00:00Z", "reviewed"),
    ("2026-09-12T00:00:00+00:00", "reviewed"),
    ("2026-09-12T00:00:00-04:00", "reviewed"),
    # A naive stamp carries none, and any other placement of Z is not a zone.
    ("2026-09-12T00:00:00", "unverified"),
    ("2026-09-12T00:00:00ZZ", "unverified"),
    ("Z2026-09-12T00:00:00", "unverified"),
    ("2026-09-12T00:00:00+00:00Z", "unverified"),
    ("Z", "unverified"),
])
def test_review_timestamp_requires_a_real_zone(tmp_path: Path, stamp: str, expected: str):
    """Only a genuine UTC designator or numeric offset counts as zoned."""
    receipt, analysis, review = _artifacts(tmp_path / stamp.replace(":", "_"))
    payload = json.loads(review.read_text()); payload["reviewed_at_utc"] = stamp
    review.write_text(json.dumps(payload))
    found = chart_evidence.reviewed_evidence(tmp_path / stamp.replace(":", "_"), analysis, review)
    assert found[receipt["intake_id"]]["state"] == expected


def _with_counts(tmp_path: Path, slug: str, counts):
    """Bind a coherent fixture, then replace only its severity mapping."""
    receipt, analysis, review = _artifacts(tmp_path / slug)
    payload = json.loads(review.read_text()); payload["severity_counts"] = counts
    review.write_text(json.dumps(payload))
    found = chart_evidence.reviewed_evidence(tmp_path / slug, analysis, review)
    return found[receipt["intake_id"]]["state"]


def test_extra_declared_severity_contradicts_a_clean_verdict(tmp_path: Path):
    """A review declaring CRITICAL: 1 is not clean, whatever its verdict says."""
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    payload = json.loads(review.read_text())
    payload["severity_counts"]["CRITICAL"] = 1
    review.write_text(json.dumps(payload))
    found = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    assert found[receipt["intake_id"]]["state"] == "unverified"


@pytest.mark.parametrize("slug,counts,expected", [
    # The supported mapping, and only it, is clean.
    ("supported", {"BLOCKING": 0, "MAJOR": 0, "MINOR": 0}, "reviewed"),
    ("reordered", {"MINOR": 0, "BLOCKING": 0, "MAJOR": 0}, "reviewed"),
    # An unsupported severity is rejected even when it declares nothing.
    ("extra_zero", {"BLOCKING": 0, "MAJOR": 0, "MINOR": 0, "CRITICAL": 0}, "unverified"),
    ("extra_unknown", {"BLOCKING": 0, "MAJOR": 0, "MINOR": 0, "UNKNOWN": 1}, "unverified"),
    ("extra_lowercase", {"BLOCKING": 0, "MAJOR": 0, "MINOR": 0, "minor": 0}, "unverified"),
    ("extra_malformed", {"BLOCKING": 0, "MAJOR": 0, "MINOR": 0, "CRITICAL": {}}, "unverified"),
    # A missing severity leaves part of the review unstated.
    ("missing_blocking", {"MAJOR": 0, "MINOR": 0}, "unverified"),
    ("missing_major", {"BLOCKING": 0, "MINOR": 0}, "unverified"),
    ("missing_minor", {"BLOCKING": 0, "MAJOR": 0}, "unverified"),
    ("empty", {}, "unverified"),
    # A supported severity must carry a real, non-Boolean integer zero.
    ("nonzero", {"BLOCKING": 0, "MAJOR": 1, "MINOR": 0}, "unverified"),
    ("negative", {"BLOCKING": -1, "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("bool_false", {"BLOCKING": False, "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("bool_true", {"BLOCKING": True, "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("float_zero", {"BLOCKING": 0.0, "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("string_zero", {"BLOCKING": "0", "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("null", {"BLOCKING": None, "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("nested", {"BLOCKING": {"count": 0}, "MAJOR": 0, "MINOR": 0}, "unverified"),
    ("listed", {"BLOCKING": [0], "MAJOR": 0, "MINOR": 0}, "unverified"),
    # The mapping itself may be malformed; none of these may raise.
    ("not_a_mapping", [0, 0, 0], "unverified"),
    ("scalar", 0, "unverified"),
    ("text", "clean", "unverified"),
    ("none", None, "unverified"),
])
def test_severity_mapping_must_match_the_supported_schema(
        tmp_path: Path, slug: str, counts, expected: str):
    """Only an exact, all-zero supported mapping is clean; nothing else raises."""
    assert _with_counts(tmp_path, slug, counts) == expected


@pytest.mark.parametrize("field,value", [
    ("ticker", "TSLA"), ("intake_id", "20260912T000000Z-abcdef123456"),
    ("visible_timeframe", "4H"),
    ("visible_export_attribution_timestamp", "2026-09-11T15:39:00-04:00"),
])
def test_review_identity_mismatches_fail_closed(tmp_path: Path, field: str, value: str):
    receipt, analysis, review = _artifacts(tmp_path / field)
    payload = json.loads(review.read_text()); payload["records"][0][field] = value
    review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(tmp_path / field, analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def test_claim_source_reference_mismatch_fails_closed(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    payload = json.loads(analysis.read_text())
    payload["records"][0]["content"]["observations"][0]["source"]["intake_id"] = "not-a-receipt"
    analysis.write_text(json.dumps(payload))
    # Update the analysis binding so this test reaches source-reference validation.
    review_payload = json.loads(review.read_text()); data = analysis.read_bytes()
    review_payload["reviewed_artifact"]["files"]["chart-evidence-draft.json"].update(
        byte_size=len(data), sha256=hashlib.sha256(data).hexdigest())
    review.write_text(json.dumps(review_payload))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


@pytest.mark.parametrize("target,value", [
    ("identity_and_capture.visible_timeframe", []),
    ("identity_and_capture.visible_timeframe", {}),
    ("content.uncertainties", 42),
    ("prohibited_uses", 42),
])
def test_malformed_draft_display_or_timeframe_fields_fail_closed(tmp_path: Path, target: str, value):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    draft = json.loads(analysis.read_text()); record = draft["records"][0]
    parent, _, key = target.rpartition(".")
    for part in parent.split(".") if parent else ():
        record = record[part]
    record[key] = value
    analysis.write_text(json.dumps(draft)); data = analysis.read_bytes()
    review_data = json.loads(review.read_text())
    review_data["reviewed_artifact"]["files"]["chart-evidence-draft.json"].update(
        byte_size=len(data), sha256=hashlib.sha256(data).hexdigest())
    review.write_text(json.dumps(review_data))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


@pytest.mark.parametrize("field,value", [("limitations", 42), ("methods", [42])])
def test_malformed_review_display_fields_fail_closed(tmp_path: Path, field: str, value):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    payload = json.loads(review.read_text()); payload[field] = value; review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def test_duplicate_draft_identity_fails_all_badges_closed(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    draft = json.loads(analysis.read_text()); draft["records"].append(draft["records"][0])
    analysis.write_text(json.dumps(draft)); data = analysis.read_bytes()
    review_data = json.loads(review.read_text())
    review_data["reviewed_artifact"]["files"]["chart-evidence-draft.json"].update(
        byte_size=len(data), sha256=hashlib.sha256(data).hexdigest())
    review.write_text(json.dumps(review_data))
    assert chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def _receipt_path(inbox: Path, intake_id: str) -> Path:
    return inbox / chart_inbox.CHARTS_DIRNAME / intake_id / chart_inbox.RECORD_FILENAME


def test_declared_receipt_hash_is_the_hash_of_the_stored_receipt_bytes(tmp_path: Path):
    """The positive case binds exact bytes, not a repeated string."""
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    found = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    assert found[receipt["intake_id"]]["state"] == "reviewed"
    stored = _receipt_path(tmp_path / "inbox", receipt["intake_id"]).read_bytes()
    declared = json.loads(analysis.read_text())["records"][0]["identity_and_capture"]["receipt_sha256"]
    assert declared == hashlib.sha256(stored).hexdigest()
    # Both artifacts repeating the same wrong hash must not manufacture a binding.
    draft = json.loads(analysis.read_text())
    draft["records"][0]["identity_and_capture"]["receipt_sha256"] = "b" * 64
    analysis.write_text(json.dumps(draft)); data = analysis.read_bytes()
    payload = json.loads(review.read_text())
    payload["records"][0]["receipt_sha256"] = "b" * 64
    payload["reviewed_artifact"]["files"]["chart-evidence-draft.json"].update(
        byte_size=len(data), sha256=hashlib.sha256(data).hexdigest())
    review.write_text(json.dumps(payload))
    assert chart_evidence.reviewed_evidence(
        tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"


@pytest.mark.parametrize("slug,field,value", [
    ("received_at", "received_at", "2099-01-01T00:00:00Z"),
    ("influence", "influence", "this receipt now claims influence"),
    ("ticker", "declared_ticker", "TSLA"),
    ("content_hash", "content_sha256", "d" * 64),
    ("state", "state", "duplicate"),
])
def test_material_receipt_mutation_after_review_fails_closed(
        tmp_path: Path, slug: str, field: str, value: str):
    """A receipt edited after review no longer matches what was reviewed."""
    receipt, analysis, review = _artifacts(tmp_path / slug)
    path = _receipt_path(tmp_path / slug, receipt["intake_id"])
    before = path.read_bytes()
    doc = json.loads(before); doc[field] = value; path.write_text(json.dumps(doc))
    assert path.read_bytes() != before, "the mutation must actually change the bytes"
    assert chart_evidence.reviewed_evidence(
        tmp_path / slug, analysis, review)[receipt["intake_id"]]["state"] == "unverified"


def test_a_single_changed_receipt_byte_fails_closed(tmp_path: Path):
    """Re-serialising the same fields with different whitespace is enough."""
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    path = _receipt_path(tmp_path / "inbox", receipt["intake_id"])
    before = path.read_bytes()
    path.write_bytes(before + b" ")
    assert chart_evidence.reviewed_evidence(
        tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "unverified"
    path.write_bytes(before)
    assert chart_evidence.reviewed_evidence(
        tmp_path / "inbox", analysis, review)[receipt["intake_id"]]["state"] == "reviewed"


@pytest.mark.parametrize("slug,payload", [
    ("malformed", b"{not json"),
    ("duplicate_key", b'{"intake_id": "a", "intake_id": "b"}'),
    ("not_a_mapping", b"[]"),
    ("empty", b""),
    ("not_utf8", b"\xff\xfe\x00"),
])
def test_unreadable_receipt_fails_closed_without_raising(
        tmp_path: Path, slug: str, payload: bytes):
    """Nothing reads as reviewed, and no shape of broken receipt raises.

    Some of these the enumeration itself cannot parse, so the row drops out
    entirely; a duplicate-keyed receipt parses last-wins there but is still
    rejected on the byte-verified read.  Either way no annotation survives.
    """
    receipt, analysis, review = _artifacts(tmp_path / slug)
    path = _receipt_path(tmp_path / slug, receipt["intake_id"])
    assert chart_evidence.reviewed_evidence(
        tmp_path / slug, analysis, review)[receipt["intake_id"]]["state"] == "reviewed"
    path.write_bytes(payload)
    assert chart_inbox.read_receipt(tmp_path / slug, receipt["intake_id"]) is None
    found = chart_evidence.reviewed_evidence(tmp_path / slug, analysis, review)
    assert all(value["state"] == "unverified" for value in found.values())
    assert found.get(receipt["intake_id"], {"state": "unverified"})["state"] == "unverified"


def test_oversized_receipt_is_rejected_even_though_it_parses(tmp_path: Path):
    """The bound is load-bearing: this receipt is valid JSON the row still shows."""
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    path = _receipt_path(tmp_path / "inbox", receipt["intake_id"])
    doc = json.loads(path.read_text())
    doc["padding"] = "x" * chart_inbox.MAX_RECEIPT_BYTES
    path.write_text(json.dumps(doc))
    assert path.stat().st_size > chart_inbox.MAX_RECEIPT_BYTES
    # Enumeration still lists the row, so this is the bound rejecting it.
    assert len(chart_inbox.list_records(tmp_path / "inbox")) == 1
    assert chart_inbox.read_receipt(tmp_path / "inbox", receipt["intake_id"]) is None
    found = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    assert found[receipt["intake_id"]]["state"] == "unverified"


def test_missing_receipt_fails_closed(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    _receipt_path(tmp_path / "inbox", receipt["intake_id"]).unlink()
    found = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    assert all(v["state"] == "unverified" for v in found.values())


def test_read_receipt_returns_bytes_and_the_record_they_parse_to(tmp_path: Path):
    """Validation and display metadata derive from the bytes that were hashed."""
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    raw, record = chart_inbox.read_receipt(tmp_path / "inbox", receipt["intake_id"])
    assert raw == _receipt_path(tmp_path / "inbox", receipt["intake_id"]).read_bytes()
    assert record == json.loads(raw.decode("utf-8"))
    # Every receipt field the reader validates against comes from this record.
    for field in ("intake_id", "declared_ticker", "declared_timeframe", "content_sha256"):
        assert record[field] == receipt[field]
    assert chart_inbox.read_receipt(tmp_path / "inbox", "not-an-id") is None
    assert chart_inbox.read_receipt(tmp_path / "inbox", "20260910T120000Z-000000000000") is None


def _dup_inbox(inbox: Path):
    """One retained original plus a duplicate recognised against it."""
    image = png_bytes()
    kw = dict(display_filename="chart.png", declared_ticker="NVDA",
              declared_timeframe="Daily", allowed_tickers=frozenset({"NVDA"}),
              allowed_timeframes=frozenset({"Daily"}))
    original = chart_inbox.ingest(inbox, image, **kw)
    duplicate = chart_inbox.ingest(inbox, image, **kw)
    assert duplicate["state"] == chart_inbox.STATE_DUPLICATE
    assert duplicate["duplicate_of"] == original["intake_id"]
    return image, original, duplicate


def test_duplicate_row_links_to_the_original_it_was_recognised_against(tmp_path: Path):
    inbox = tmp_path / "inbox"
    image, original, duplicate = _dup_inbox(inbox)
    links = chart_inbox.viewable_image_ids(inbox)
    assert links[original["intake_id"]] == original["intake_id"]
    assert links[duplicate["intake_id"]] == original["intake_id"]
    page = render.charts_page({}, chart_inbox.list_records(inbox), image_links=links)
    assert f'/charts/image/{original["intake_id"]}' in page
    # The duplicate's own id is never offered: it holds no bytes.
    assert f'/charts/image/{duplicate["intake_id"]}' not in page
    assert chart_inbox.read_image_bytes(inbox, duplicate["intake_id"]) is None
    # And no second copy was created for it.
    dup_dir = inbox / chart_inbox.CHARTS_DIRNAME / duplicate["intake_id"]
    assert sorted(p.name for p in dup_dir.iterdir()) == [chart_inbox.RECORD_FILENAME]


@pytest.mark.parametrize("slug,break_it", [
    ("missing", lambda rec: rec.pop("duplicate_of")),
    ("null", lambda rec: rec.update(duplicate_of=None)),
    ("malformed", lambda rec: rec.update(duplicate_of="../../../etc/passwd")),
    ("not_an_id", lambda rec: rec.update(duplicate_of="not-an-id")),
    ("wrong_type", lambda rec: rec.update(duplicate_of=["x"])),
    ("unknown", lambda rec: rec.update(duplicate_of="20260910T120000Z-abcdef123456")),
])
def test_unresolvable_duplicate_reference_offers_no_link(
        tmp_path: Path, slug: str, break_it):
    inbox = tmp_path / slug
    _, original, duplicate = _dup_inbox(inbox)
    path = inbox / chart_inbox.CHARTS_DIRNAME / duplicate["intake_id"] / chart_inbox.RECORD_FILENAME
    doc = json.loads(path.read_text()); break_it(doc); path.write_text(json.dumps(doc))
    links = chart_inbox.viewable_image_ids(inbox)
    assert duplicate["intake_id"] not in links
    page = render.charts_page({}, chart_inbox.list_records(inbox), image_links=links)
    assert "No retained original is available to open" in page


def test_duplicate_pointing_at_another_duplicate_offers_no_link(tmp_path: Path):
    """A duplicate is not a retained original, so chaining resolves to nothing."""
    inbox = tmp_path / "inbox"
    _, original, duplicate = _dup_inbox(inbox)
    path = inbox / chart_inbox.CHARTS_DIRNAME / duplicate["intake_id"] / chart_inbox.RECORD_FILENAME
    doc = json.loads(path.read_text()); doc["duplicate_of"] = duplicate["intake_id"]
    path.write_text(json.dumps(doc))
    assert duplicate["intake_id"] not in chart_inbox.viewable_image_ids(inbox)


def test_no_link_when_the_originals_image_is_gone(tmp_path: Path):
    inbox = tmp_path / "inbox"
    _, original, duplicate = _dup_inbox(inbox)
    (inbox / chart_inbox.CHARTS_DIRNAME / original["intake_id"] / "original.png").unlink()
    links = chart_inbox.viewable_image_ids(inbox)
    assert original["intake_id"] not in links and duplicate["intake_id"] not in links
    page = render.charts_page({}, chart_inbox.list_records(inbox), image_links=links)
    assert "/charts/image/" not in page
    assert "No retained original is available to open" in page


def test_duplicate_link_serves_the_exact_original_bytes_over_http(tmp_path: Path):
    """The offered route really returns the original's retained bytes."""
    inbox = tmp_path / "inbox"; export = tmp_path / "export.json"
    write_export(export, _sample_export())
    image, original, duplicate = _dup_inbox(inbox)
    config = service_mod.build_config(inbox_root=inbox, export_path=export, host="127.0.0.1",
                                      env={"PORTFOLIO_HQ_OWNER_TOKEN": TOKEN})
    server = ThreadingHTTPServer(("127.0.0.1", 0), service_mod._make_handler(config))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        client = Client(server.server_address[1])
        # Anonymous access stays redirected, for the offered link too.
        assert client.request("GET", f'/charts/image/{original["intake_id"]}',
                              use_cookie=False)[0] == 303
        assert client.sign_in()[0] == 303
        status, _, page = client.request("GET", "/charts")
        assert status == 200
        offered = f'/charts/image/{original["intake_id"]}'.encode()
        assert offered in page
        assert f'/charts/image/{duplicate["intake_id"]}'.encode() not in page
        status, headers, payload = client.request("GET", offered.decode())
        assert status == 200 and headers["Content-Type"] == "image/png"
        assert payload == image, "the duplicate's link must serve the original bytes"
        # The duplicate's own id still 404s; the page simply never offers it.
        assert client.request("GET", f'/charts/image/{duplicate["intake_id"]}')[0] == 404
    finally:
        server.shutdown(); server.server_close(); thread.join()


def test_authenticated_chart_evidence_and_malformed_confirmation_do_not_disconnect(tmp_path: Path):
    """The optional reader cannot turn a GET or upload confirmation into a 500."""
    inbox = tmp_path / "inbox"; export = tmp_path / "export.json"; write_export(export, _sample_export())
    receipt, analysis, review = _artifacts(inbox)
    config = service_mod.build_config(inbox_root=inbox, export_path=export, host="127.0.0.1",
                                      env={"PORTFOLIO_HQ_OWNER_TOKEN": TOKEN}, analysis_path=analysis, review_path=review)
    server = ThreadingHTTPServer(("127.0.0.1", 0), service_mod._make_handler(config))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        client = Client(server.server_address[1])
        assert client.request("GET", "/charts", use_cookie=False)[0] == 303
        assert client.request("GET", f'/charts/image/{receipt["intake_id"]}', use_cookie=False)[0] == 303
        assert client.sign_in()[0] == 303
        status, _, page = client.request("GET", "/charts")
        assert status == 200 and b"independently reviewed" in page
        assert client.request("GET", f'/charts/image/{receipt["intake_id"]}')[0] == 200
        draft = json.loads(analysis.read_text()); draft["records"][0]["identity_and_capture"]["visible_timeframe"] = []
        analysis.write_text(json.dumps(draft)); data = analysis.read_bytes()
        review_data = json.loads(review.read_text())
        review_data["reviewed_artifact"]["files"]["chart-evidence-draft.json"].update(byte_size=len(data), sha256=hashlib.sha256(data).hexdigest())
        review.write_text(json.dumps(review_data))
        assert client.request("GET", "/charts")[0] == 200
        body, content_type = multipart({"ticker": "NVDA", "timeframe": "1D"}, {"chart": ("new.png", png_bytes(3, 2))})
        assert client.request("POST", "/charts/upload", body, {"Content-Type": content_type})[0] == 200
    finally:
        server.shutdown(); server.server_close(); thread.join()


def test_expanded_evidence_uses_a_full_width_phone_reading_surface(tmp_path: Path):
    receipt, analysis, review = _artifacts(tmp_path / "inbox")
    evidence = chart_evidence.reviewed_evidence(tmp_path / "inbox", analysis, review)
    page = render.charts_page({}, chart_inbox.list_records(tmp_path / "inbox"), evidence=evidence)
    css = (Path(render.__file__).parent / "assets" / "owner.css").read_text()
    assert 'class="evidence-cell"' in page
    assert 'class="evidence-panel"' in page
    assert "table.grid td.evidence-cell {\n    display: block;" in css
    assert ".evidence-panel .chip" in css and "white-space: normal;" in css
    assert "Optional advisory reference" in page
