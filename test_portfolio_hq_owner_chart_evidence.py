"""Synthetic binding tests for the optional private chart-evidence reader."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from portfolio_hq.owner import chart_evidence, chart_inbox
from test_portfolio_hq_owner_chart_inbox import png_bytes


def _artifacts(inbox: Path, *, reviewer="independent-ai", mutate=None):
    image = png_bytes()
    receipt = chart_inbox.ingest(inbox, image, display_filename="chart.png",
        declared_ticker="NVDA", declared_timeframe="Daily",
        allowed_tickers=frozenset({"NVDA"}), allowed_timeframes=frozenset({"Daily"}))
    record = {"record_id": "r1", "lifecycle": {}, "identity_and_capture": {
        "ticker": "NVDA", "intake_id": receipt["intake_id"], "visible_timeframe": "1D",
        "retained_image_sha256": receipt["content_sha256"], "receipt_sha256": "a" * 64,
        "visible_export_attribution_timestamp": "2026-09-11T15:34:00-04:00"},
        "content": {"visible_facts": [{"id": "f", "text": "synthetic fact", "source": {
                         "intake_id": receipt["intake_id"], "retained_image_sha256": receipt["content_sha256"]}}],
                    "observations": [], "inferences": [], "uncertainties": ["unknown feed"]},
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
        "retained_image_sha256": receipt["content_sha256"], "receipt_sha256": "a" * 64,
        "visible_timeframe": "1D", "mechanical_result": "pass",
        "image_claim_review_result": "supported within stated limits", "claimed_ids_reviewed": ["f"], "findings": []}], "limitations": ["hash regeneration incomplete"]}
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
