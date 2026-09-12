"""Read-only binding of private chart analysis to an external review artifact.

The two files are explicit operator-provisioned data inputs.  A hash binds
bytes, not an identity or signature; the trusted operator establishes who
provisioned the separately generated review.  Paths inside either JSON are
display metadata only and are never opened.
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
    """Read no more than the bound plus one byte before parsing JSON."""
    if path is None:
        return None, None, "not configured"
    try:
        with path.open("rb") as handle:
            data = handle.read(MAX_ARTIFACT_BYTES + 1)
    except OSError:
        return None, None, "unavailable"
    if len(data) > MAX_ARTIFACT_BYTES:
        return None, None, "too large"
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return None, None, "malformed"
    return (value, data, "ok") if isinstance(value, dict) else (None, None, "malformed")


def _text(value: object) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _same_text(*values: object) -> bool:
    return all(_text(value) is not None for value in values) and len(set(values)) == 1


def _daily_equivalent(intake: object, evidence: object) -> bool:
    # The established receipt spelling is Daily; supported evidence spells it 1D.
    return (intake == evidence) or ({intake, evidence} == {"Daily", "1D"})


def _clean_review(review: dict, draft_bytes: bytes) -> tuple[dict, str] | None:
    artifact = review.get("reviewed_artifact")
    if not isinstance(artifact, dict):
        return None
    files = artifact.get("files")
    entry = files.get("chart-evidence-draft.json") if isinstance(files, dict) else None
    counts = review.get("severity_counts")
    if not isinstance(entry, dict) or not isinstance(counts, dict):
        return None
    digest = hashlib.sha256(draft_bytes).hexdigest()
    clean_counts = all(counts.get(name) == 0 and isinstance(counts.get(name), int)
                       and not isinstance(counts.get(name), bool)
                       for name in ("BLOCKING", "MAJOR", "MINOR"))
    if not (review.get("schema_version") == 1
            and review.get("review_kind") == "independent_private_analytical_artifact_review"
            and _text(review.get("review_id")) and _text(review.get("reviewer"))
            and _text(review.get("reviewed_at_utc"))
            and review.get("verdict") == "CLEAN_FOR_PRIVATE_ADVISORY_REFERENCE"
            and clean_counts and review.get("findings") == []
            and review.get("material_corrections_required") is False
            and review.get("principal_acceptance") is None
            and review.get("portfolio_policy_acceptance") is False
            and entry.get("byte_size") == len(draft_bytes)
            and entry.get("sha256") == digest):
        return None
    return artifact, digest


def _claim_ids(content: dict, identity: dict) -> set[str] | None:
    ids: set[str] = set()
    for group in ("visible_facts", "observations"):
        claims = content.get(group)
        if not isinstance(claims, list):
            return None
        for claim in claims:
            if not isinstance(claim, dict) or not _text(claim.get("id")):
                return None
            source = claim.get("source")
            if not isinstance(source, dict) or not _same_text(
                    source.get("intake_id"), identity.get("intake_id")) or not _same_text(
                    source.get("retained_image_sha256"), identity.get("retained_image_sha256")):
                return None
            ids.add(claim["id"])
    return ids


def reviewed_evidence(inbox_root: Path | str, analysis_path: Path | None,
                      review_path: Path | None) -> dict[str, dict]:
    """Return display annotations, never mutating receipts or portfolio state."""
    draft, draft_bytes, draft_state = _read_json(analysis_path)
    review, review_bytes, review_state = _read_json(review_path)
    records = chart_inbox.list_records(inbox_root)
    unavailable = f"Private analysis is {draft_state}; independent review is {review_state}."
    result = {str(r.get("intake_id")): {"state": "unverified", "reason": unavailable}
              for r in records if isinstance(r.get("intake_id"), str)}
    if not draft or not review or not draft_bytes or not review_bytes:
        return result
    clean = _clean_review(review, draft_bytes)
    if not (draft.get("document_type") == "private_advisory_chart_evidence_draft"
            and draft.get("status") == "AWAITING_CHATGPT_INDEPENDENT_REVIEW"
            and isinstance(draft.get("records"), list) and clean):
        for value in result.values():
            value["reason"] = "Private analysis and review are not independently bound."
        return result
    artifact, draft_hash = clean
    review_records = review.get("records")
    if not isinstance(review_records, list):
        return result
    reviewed = {r.get("record_id"): r for r in review_records if isinstance(r, dict)}
    for draft_record in draft["records"]:
        if not isinstance(draft_record, dict):
            continue
        identity, content = draft_record.get("identity_and_capture"), draft_record.get("content")
        if not isinstance(identity, dict) or not isinstance(content, dict):
            continue
        intake_id = identity.get("intake_id")
        receipt = next((r for r in records if r.get("intake_id") == intake_id), None)
        check = reviewed.get(draft_record.get("record_id"))
        if not receipt or not isinstance(check, dict) or check.get("findings") != []:
            continue
        image = chart_inbox.read_image_bytes(inbox_root, intake_id)
        claims = _claim_ids(content, identity)
        claimed = check.get("claimed_ids_reviewed")
        if not image or claims is None or not isinstance(claimed, list) or set(claimed) != claims:
            continue
        actual_hash = hashlib.sha256(image[0]).hexdigest()
        if not (_same_text(identity.get("ticker"), receipt.get("declared_ticker"), check.get("ticker"))
                and _same_text(identity.get("intake_id"), receipt.get("intake_id"), check.get("intake_id"))
                and _same_text(identity.get("retained_image_sha256"), receipt.get("content_sha256"), check.get("retained_image_sha256"), actual_hash)
                and _same_text(identity.get("receipt_sha256"), check.get("receipt_sha256"))
                and _daily_equivalent(receipt.get("declared_timeframe"), identity.get("visible_timeframe"))
                and identity.get("visible_timeframe") == check.get("visible_timeframe") == "1D"
                and check.get("mechanical_result") == "pass"
                and check.get("image_claim_review_result") == "supported within stated limits"):
            continue
        result[str(intake_id)] = {
            "state": "reviewed", "review_id": review["review_id"], "reviewer": review["reviewer"],
            "reviewed_at": review["reviewed_at_utc"], "draft_sha256": draft_hash,
            "review_sha256": hashlib.sha256(review_bytes).hexdigest(),
            "limitations": review.get("limitations") if isinstance(review.get("limitations"), list) else [],
            "facts": content.get("visible_facts") or [], "observations": content.get("observations") or [],
            "inferences": content.get("inferences") or [], "uncertainties": content.get("uncertainties") or [],
            "prohibited_uses": draft_record.get("prohibited_uses") or [],
            "export_attribution_time": identity.get("visible_export_attribution_timestamp"),
            "review_scope": review.get("methods") if isinstance(review.get("methods"), list) else [],
        }
    return result
