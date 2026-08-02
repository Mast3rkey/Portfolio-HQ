"""Package-integrity tests for the CHART-0001 NVDA daily pilot evidence
package (governance/evidence/CHART-0001/nvda-daily-2026-08-01/).

These tests verify the retained package's internal consistency (file count,
hash reconciliation, required fields, fact/interpretation separation, and the
draft-stage governance invariants CHART-0001 requires) — they do not import
or couple to allocate.py, margin_state.py, levels.py,
intelligence_validator.py, dashboard code, or brokerage code, matching this
package's own no-coupling scope.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

PACKAGE_DIR = Path(__file__).parent / "governance" / "evidence" / "CHART-0001" / "nvda-daily-2026-08-01"
CHART_0001_ROOT = Path(__file__).parent / "governance" / "evidence" / "CHART-0001"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def package_files() -> list[Path]:
    assert PACKAGE_DIR.is_dir(), f"expected package directory at {PACKAGE_DIR}"
    return sorted(PACKAGE_DIR.iterdir())


@pytest.fixture(scope="module")
def record(package_files) -> dict:
    with open(PACKAGE_DIR / "record.yaml") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def manifest(package_files) -> dict:
    with open(PACKAGE_DIR / "MANIFEST.json") as f:
        return json.load(f)


# ── package shape ────────────────────────────────────────────────────────

def test_package_contains_exactly_one_image_plus_the_three_required_files(package_files):
    names = {p.name for p in package_files}
    assert names == {"NVDA__2026-08-01__1D.png", "record.yaml", "MANIFEST.json", "README.md"}


def test_no_second_pilot_package_exists_under_chart_0001():
    subdirs = [p for p in CHART_0001_ROOT.iterdir() if p.is_dir()]
    assert subdirs == [PACKAGE_DIR]


def test_no_second_image_anywhere_in_the_package(package_files):
    images = [p for p in package_files if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    assert len(images) == 1


# ── parsing ──────────────────────────────────────────────────────────────

def test_record_yaml_parses(record):
    assert isinstance(record, dict)


def test_manifest_json_parses(manifest):
    assert isinstance(manifest, dict)


# ── required record fields ──────────────────────────────────────────────

def test_record_has_required_top_level_sections(record):
    for key in (
        "record_id",
        "identity_and_capture",
        "privacy_and_redaction",
        "content",
        "thesis_relationship",
        "prohibited_uses",
        "provenance",
        "lifecycle",
    ):
        assert key in record, f"record.yaml missing required section: {key}"


def test_ticker_is_nvda_and_timeframe_is_daily(record):
    ident = record["identity_and_capture"]
    assert ident["ticker"] == "NVDA"
    assert "daily" in ident["timeframe"].lower() or ident["timeframe"] == "1D"


# ── fact/interpretation separation ──────────────────────────────────────

def test_content_fields_are_separate_lists(record):
    content = record["content"]
    for key in ("visible_facts", "observations", "inferences", "uncertainties"):
        assert key in content, f"content missing {key}"
        assert isinstance(content[key], list), f"content.{key} must be a list"
        assert len(content[key]) > 0, f"content.{key} must not be empty"

    # the four lists must be genuinely distinct collections, not aliases of
    # one shared list
    lists = [content["visible_facts"], content["observations"], content["inferences"], content["uncertainties"]]
    ids = {id(lst) for lst in lists}
    assert len(ids) == 4


# ── advisory / governance boundary ──────────────────────────────────────

def test_governed_consequence_is_none(record):
    assert record["thesis_relationship"]["governed_consequence"] == "none"


def test_prohibited_uses_include_controlling_safeguards(record):
    prohibited = " ".join(str(x).lower() for x in record["prohibited_uses"])
    for phrase in ("allocator", "ladder-0001", "intelligence", "score", "signal", "execution", "tier"):
        assert phrase in prohibited, f"prohibited_uses does not cover: {phrase}"


# ── hash reconciliation ─────────────────────────────────────────────────

def test_retained_image_sha256_matches_actual_file(package_files):
    image_path = PACKAGE_DIR / "NVDA__2026-08-01__1D.png"
    assert image_path in package_files
    assert _sha256(image_path) == "7afb06217c762a3d31f20e9cf92339dfa4bc0ea73870fd2f3817f3e5452c220b"


def test_retained_image_sha256_matches_record_and_manifest(record, manifest, package_files):
    actual = _sha256(PACKAGE_DIR / "NVDA__2026-08-01__1D.png")
    assert record["identity_and_capture"]["retained_image_sha256"] == actual
    assert manifest["retained_sha256"] == actual


def test_governed_source_hash_matches_across_record_and_manifest(record, manifest):
    assert (
        record["identity_and_capture"]["governed_source_sha256"]
        == manifest["governed_source_sha256"]
        == "0ddc0eb0aded012618c368343f657f983d5bb9db7d130f58965f4bb542c4055f"
    )


def test_source_and_retained_hashes_differ_consistent_with_declared_redaction(record, manifest):
    ident = record["identity_and_capture"]
    assert ident["governed_source_sha256"] != ident["retained_image_sha256"], (
        "a transformation was declared (redaction), so source and retained hashes must differ"
    )
    assert manifest["transformation_history"], "manifest must disclose the transformation that explains the hash difference"
    assert manifest["privacy_result"] == "redacted"


# ── privacy ──────────────────────────────────────────────────────────────

def test_privacy_status_is_passed_or_redacted(record, manifest):
    assert record["privacy_and_redaction"]["status"] in {"passed", "redacted"}
    assert manifest["privacy_result"] in {"passed", "redacted"}


def test_username_exception_not_applied(record, manifest):
    assert record["privacy_and_redaction"]["username_exception_applied"] is False
    assert manifest["username_exception_applied"] is False


# ── accepted-stage governance invariants ────────────────────────────────

def test_provenance_reviewer_identifies_final_review(record):
    reviewer = record["provenance"]["reviewer"]
    assert reviewer is not None
    assert "4836601466" in reviewer
    assert "COMMENTED" in reviewer
    assert "APPROVED FOR PRINCIPAL ACCEPTANCE" in reviewer


def test_provenance_reviewed_head_is_exact_final_head(record):
    assert record["provenance"]["reviewed_head"] == "9c3dcc0d912c9af4a8c69670ee6d3bb1c9054550"


def test_provenance_principal_acceptance_is_recorded(record):
    acceptance = record["provenance"]["principal_acceptance"]
    assert acceptance is not None
    assert "9c3dcc0d912c9af4a8c69670ee6d3bb1c9054550" in acceptance


def test_principal_acceptance_preserves_one_image_no_scaling_boundary(record):
    acceptance = record["provenance"]["principal_acceptance"].lower()
    assert "one-image" in acceptance or "one image" in acceptance
    assert "no scaling" in acceptance or "scaling" in acceptance


def test_lifecycle_status_is_accepted(record):
    assert record["lifecycle"]["lifecycle_status"] == "accepted"


def test_provenance_records_merge(record):
    prov = record["provenance"]
    assert prov["merged_pr"] == 220
    assert prov["merge_commit"] == "5fbd529a736df4fbb46b72fed1351414aa07db1b"


def test_provenance_records_post_merge_verification(record):
    assert record["provenance"]["post_merge_verification"] == "passed"


def test_provenance_records_merge_commit_ci_run(record):
    assert record["provenance"]["merge_commit_ci_run"] == 30728722064


# ── no leaked local paths ───────────────────────────────────────────────

def test_no_absolute_user_path_committed(package_files):
    for path in package_files:
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        text = path.read_text(errors="ignore")
        assert "/Users/nickmasters" not in text, f"{path.name} contains an absolute user path"
        assert "/Users/" not in text, f"{path.name} contains an absolute path under /Users/"


# ── review 4836345012 bounded-correction regressions ────────────────────

def _content_text(record: dict) -> str:
    content = record["content"]
    parts = []
    for key in ("visible_facts", "observations", "inferences", "uncertainties"):
        parts.extend(str(x) for x in content[key])
    return "\n".join(parts)


def test_no_entry_claims_three_ed_marker_pairs(record):
    text = _content_text(record)
    assert "three" not in text.lower() or "E/D" not in text, (
        "a content entry still claims three E/D marker pairs (independently "
        "reconfirmed as four, per review 4836345012 Finding 1)"
    )
    for entry in record["content"]["visible_facts"] + record["content"]["observations"]:
        if "E/D" in entry or ("marker pair" in entry.lower()):
            assert "three" not in entry.lower(), f"stale 'three' E/D claim: {entry!r}"


def test_one_entry_records_four_ed_marker_pairs(record):
    text = _content_text(record)
    assert "four" in text and ("E/D" in text or "marker pair" in text.lower()), (
        "no content entry records the independently reconfirmed four E/D marker pairs"
    )


def test_no_distinct_recent_candle_purple_marker_feature(record):
    text = _content_text(record).lower()
    assert "15-20 candles" not in text and "15–20 candles" not in text, (
        "a stale 'row of markers confined to the most recent candles' claim remains "
        "(review 4836345012 Finding 2: this is the same object as the full-width dashed line)"
    )


def test_no_pivot_or_price_alert_marker_interpretation(record):
    text = _content_text(record).lower()
    assert "pivot-point-style" not in text
    assert "price-alert-style" not in text
    assert "marker series" not in text


def test_record_and_manifest_redaction_geometry_agree(record, manifest):
    geometry = "x=[0,169), y=[0,49)"
    record_text = record["privacy_and_redaction"]["redactions_applied"][0]
    manifest_text = json.dumps(manifest["transformation_history"])
    assert geometry in record_text, f"record.yaml redaction entry missing {geometry!r}"
    assert geometry in manifest_text, f"MANIFEST.json transformation_history missing {geometry!r}"
    # the superseded, one-pixel-narrower/shorter figure must not appear as the
    # declared (non-historical) geometry anywhere in the manifest's verifiability_boundary
    assert "x=[0,168), y=[0,48)" not in json.dumps(manifest["source_provenance_chain"])


def test_manifest_discloses_color_mode_conversion(manifest):
    color_entries = [
        t for t in manifest["transformation_history"]
        if "rgba" in json.dumps(t).lower() or "color-mode" in str(t.get("transformation", "")).lower()
    ]
    assert color_entries, "MANIFEST.json transformation_history does not disclose the RGBA-to-RGB conversion"
    entry = color_entries[0]
    disclosure = json.dumps(entry).lower()
    assert "rgba" in disclosure
    assert "rgb" in disclosure
    assert "opaque" in disclosure


# ── lifecycle-closure synchronization (accepted, merged state) ─────────

def test_manifest_generated_hashes_match_actual_record_and_readme_bytes(manifest):
    for name in ("record.yaml", "README.md"):
        actual = _sha256(PACKAGE_DIR / name)
        assert manifest["generated_file_hashes"][name] == actual, f"MANIFEST.json hash for {name} is stale"


def test_readme_no_longer_claims_unaccepted_or_unmerged():
    text = (PACKAGE_DIR / "README.md").read_text().lower()
    for phrase in (
        "not accepted",
        "not merged",
        "awaiting review",
        "awaiting principal",
        "must still be reviewed",
        "must still be accepted",
        "before this pr may merge",
        "preparation only",
    ):
        assert phrase not in text, f"README.md still contains stale draft-stage language: {phrase!r}"


def test_readme_retains_no_scaling_and_advisory_boundaries():
    text = (PACKAGE_DIR / "README.md").read_text().lower()
    assert "no scaling authority" in text
    assert "secondary observational evidence" in text
    assert "ladder-0001" in text
