"""Read-only binding of private chart analysis to a separately reviewed file.

Both paths are explicitly provisioned by the operator.  They are data inputs,
never upload targets, and this module never follows a path embedded in either
artifact.  A matching hash binds bytes, not a reviewer identity or signature.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import chart_inbox

MAX_ARTIFACT_BYTES = 2 * 1024 * 1024


class _DuplicateKey(ValueError):
    pass


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _constant(value):
    raise ValueError(f"non-finite JSON value: {value}")


def _read_json(path: Path | None) -> tuple[dict | None, bytes | None, str]:
    if path is None:
        return None, None, "not configured"
    try:
        data = path.read_bytes()
    except OSError:
        return None, None, "unavailable"
    if len(data) > MAX_ARTIFACT_BYTES:
        return None, None, "too large"
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return None, None, "malformed"
    return (value if isinstance(value, dict) else None), data, "ok" if isinstance(value, dict) else "malformed"


def _same_text(*values: object) -> bool:
    return all(isinstance(v, str) and v for v in values) and len(set(values)) == 1


def _daily_equivalent(intake: object, evidence: object) -> bool:
    # The established inbox spelling is Daily; analytical evidence uses 1D.
    return (intake == evidence) or ({intake, evidence} == {"Daily", "1D"})


def reviewed_evidence(inbox_root: Path | str, analysis_path: Path | None,
                      review_path: Path | None) -> dict[str, dict]:
    """Return display-safe annotations keyed by strict intake id.

    Anything missing, malformed, self-approved, or not mechanically bound is
    deliberately absent from the reviewed state.  Receipts remain unchanged.
    """
    draft, draft_bytes, draft_state = _read_json(analysis_path)
    review, _, review_state = _read_json(review_path)
    records = chart_inbox.list_records(inbox_root)
    unavailable = f"Private analysis is {draft_state}; independent review is {review_state}."
    result = {str(r.get("intake_id")): {"state": "unverified", "reason": unavailable}
              for r in records if isinstance(r.get("intake_id"), str)}
    if not draft or not review or not draft_bytes:
        return result
    digest = hashlib.sha256(draft_bytes).hexdigest()
    if not (draft.get("document_type") == "private_advisory_chart_evidence_draft"
            and draft.get("status") == "AWAITING_CHATGPT_INDEPENDENT_REVIEW"
            and isinstance(draft.get("records"), list)
            and review.get("schema_version") == 1
            and review.get("review_kind") == "independent_private_analytical_artifact_review"
            and review.get("verdict") == "CLEAN_FOR_PRIVATE_ADVISORY_REFERENCE"
            and review.get("material_corrections_required") is False
            and review.get("principal_acceptance") is None
            and review.get("portfolio_policy_acceptance") is False
            and review.get("reviewed_artifact", {}).get("filename") == "chart-evidence-draft.json"
            and review.get("reviewed_artifact", {}).get("byte_size") == len(draft_bytes)
            and review.get("reviewed_artifact", {}).get("sha256") == digest):
        for value in result.values(): value["reason"] = "Private analysis and review are not independently bound."
        return result
    reviewed = {r.get("record_id"): r for r in review.get("records", []) if isinstance(r, dict)}
    for draft_record in draft["records"]:
        if not isinstance(draft_record, dict): continue
        identity = draft_record.get("identity_and_capture")
        content = draft_record.get("content")
        if not isinstance(identity, dict) or not isinstance(content, dict): continue
        intake_id = identity.get("intake_id")
        receipt = next((r for r in records if r.get("intake_id") == intake_id), None)
        check = reviewed.get(draft_record.get("record_id"))
        if not receipt or not isinstance(check, dict): continue
        image = chart_inbox.read_image_bytes(inbox_root, intake_id)
        if not image: continue
        actual_hash = hashlib.sha256(image[0]).hexdigest()
        provenance = draft_record.get("provenance")
        if not isinstance(provenance, dict):
            continue
        if not (_same_text(identity.get("ticker"), receipt.get("declared_ticker"), check.get("ticker"))
                and _same_text(identity.get("intake_id"), receipt.get("intake_id"), check.get("intake_id"))
                and _same_text(identity.get("retained_image_sha256"), receipt.get("content_sha256"), check.get("retained_image_sha256"), actual_hash)
                and _same_text(identity.get("receipt_sha256"), check.get("receipt_sha256"))
                and _daily_equivalent(receipt.get("declared_timeframe"), identity.get("visible_timeframe"))
                and identity.get("visible_timeframe") == check.get("visible_timeframe") == "1D"
                and check.get("mechanical_result") == "pass"
                and check.get("image_claim_review_result") == "supported within stated limits"
                and review.get("reviewer") != provenance.get("draft_independent_reviewer")):
            continue
        result[str(intake_id)] = {"state": "reviewed", "reviewer": review.get("reviewer"),
            "reviewed_at": review.get("reviewed_at_utc"), "limitations": review.get("limitations") or [],
            "facts": content.get("visible_facts") or [], "observations": content.get("observations") or [],
            "inferences": content.get("inferences") or [], "uncertainties": content.get("uncertainties") or [],
            "prohibited_uses": draft_record.get("prohibited_uses") or [],
            "export_attribution_time": identity.get("visible_export_attribution_timestamp"),
            "review_scope": review.get("methods") or []}
    return result
