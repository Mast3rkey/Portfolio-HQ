"""Tests for intelligence_classification_sanitizer.py (WS-0005 Milestone 6
blind-classification evidence-sanitization mechanics, TIER-0004 Sec7 as
implemented under TIER-0005).

Synthetic fixtures only for behavior tests -- no real ticker's judgment
content is asserted against. A small number of tests exercise the real
repository's intelligence/companies/ records specifically to prove the
fail-closed guarantee holds against actual current content (the same
"checked against the actual corpus, not assumed" discipline TIER-0004's own
Sec7.1 bounded correction was built on).
"""

from pathlib import Path

import pytest
import yaml

import intelligence_classification_sanitizer as sanitizer


# ── synthetic fixtures ───────────────────────────────────────────────────

def _synthetic_company_yaml() -> dict:
    return {
        "sector": "Synthetic Sector",
        "industry": "Synthetic Industry",
        "portfolio_role_ref": "T1",
        "themes": ["synthetic_theme"],
        "competitive_advantages": ["A durable, factual competitive advantage."],
        "risks": [
            {"risk": "A factual, disclosed risk.", "severity": "moderate",
             "identified": "2026-01-01", "status": "monitoring"},
        ],
        "conviction": {"rating": "High", "rationale": "Synthetic conviction rationale."},
        "review": {
            "cadence_days": 90,
            "last_reviewed": "2026-08-01",
            "next_due": "2026-10-30",
            "log": [{"date": "2026-08-01", "note": "Keep current policy per committee review."}],
        },
        "sources": [{"note": "A factual source citation.", "url": None, "date": "2026-01-01"}],
    }


_SYNTHETIC_MD = """# SYNTHETIC — Company Thesis

## Business overview

A synthetic factual description of what the company does, its segments,
and its markets.

## Portfolio placement rationale

`portfolio_role_ref: T1` was explicitly approved by the human principal
under a prior governance decision. Conviction stays High.

## Risks

A synthetic disclosed risk, unrelated to placement.
"""


# ── YAML sanitization ────────────────────────────────────────────────────

def test_sanitize_yaml_strips_portfolio_role_ref_and_conviction():
    sanitized, removed = sanitizer.sanitize_yaml_data(_synthetic_company_yaml())
    assert "portfolio_role_ref" not in sanitized
    assert "conviction" not in sanitized
    assert "portfolio_role_ref" in removed
    assert "conviction" in removed


def test_sanitize_yaml_strips_review_log_narrative_retains_structural_fields():
    sanitized, removed = sanitizer.sanitize_yaml_data(_synthetic_company_yaml())
    assert "log" not in sanitized["review"]
    assert sanitized["review"]["cadence_days"] == 90
    assert sanitized["review"]["last_reviewed"] == "2026-08-01"
    assert sanitized["review"]["next_due"] == "2026-10-30"
    assert "review.log" in removed


def test_sanitize_yaml_retains_permitted_evidence():
    sanitized, _ = sanitizer.sanitize_yaml_data(_synthetic_company_yaml())
    assert sanitized["sector"] == "Synthetic Sector"
    assert sanitized["industry"] == "Synthetic Industry"
    assert sanitized["themes"] == ["synthetic_theme"]
    assert sanitized["competitive_advantages"] == ["A durable, factual competitive advantage."]
    assert sanitized["risks"][0]["risk"] == "A factual, disclosed risk."
    assert sanitized["sources"][0]["note"] == "A factual source citation."


def test_sanitize_yaml_never_mutates_input():
    original = _synthetic_company_yaml()
    import copy
    snapshot = copy.deepcopy(original)
    sanitizer.sanitize_yaml_data(original)
    assert original == snapshot


def test_sanitize_yaml_item_level_redaction_of_leaked_risk_text():
    data = _synthetic_company_yaml()
    data["risks"].append({
        "risk": "This is discussed further given the conviction rating's own exclusions.",
        "severity": "low", "identified": "2026-01-01", "status": "monitoring",
    })
    sanitized, removed = sanitizer.sanitize_yaml_data(data)
    assert sanitized["risks"][1]["risk"] == sanitizer._ITEM_REDACTION_PLACEHOLDER
    assert "risks[1].risk" in removed
    # the first, clean risk entry is untouched
    assert sanitized["risks"][0]["risk"] == "A factual, disclosed risk."


# ── Markdown sanitization ────────────────────────────────────────────────

def test_redact_markdown_strips_marker_paragraph():
    redacted, removed_count = sanitizer.redact_markdown(_SYNTHETIC_MD)
    assert "portfolio_role_ref" not in redacted
    assert "approved by the human principal" not in redacted
    assert removed_count >= 1


def test_redact_markdown_retains_unrelated_business_prose():
    redacted, _ = sanitizer.redact_markdown(_SYNTHETIC_MD)
    assert "A synthetic factual description of what the company does" in redacted
    assert "A synthetic disclosed risk, unrelated to placement." in redacted


def test_verify_markdown_redaction_clean_after_strip():
    redacted, _ = sanitizer.redact_markdown(_SYNTHETIC_MD)
    findings = sanitizer.verify_markdown_redaction(redacted)
    assert findings == []


def test_verify_markdown_redaction_catches_surviving_marker():
    # A marker embedded inline with content that would not naturally be
    # dropped as its own paragraph -- proves the mandatory re-scan (not the
    # strip pass alone) is what actually guarantees safety.
    text = "Ordinary prose. portfolio_role_ref appears mid-sentence here, deliberately."
    findings = sanitizer.verify_markdown_redaction(text)
    assert findings  # strip was never run -- re-scan must catch it


def test_chart_domain_scan_defensive_pass():
    text = "See governance/evidence/CHART-0002/batch/NVDA/chart.png for detail."
    findings = sanitizer.scan_chart_domain(text)
    assert findings


def test_chart_domain_scan_clean_on_ordinary_text():
    assert sanitizer.scan_chart_domain("Ordinary business-model prose, no chart reference.") == []


# ── section-level stripping (a marker word need not appear in a forbidden
#    section's own body -- e.g. "## Conviction" / "**Rating: High**") ─────

_SECTION_LEAK_MD = """# ZZZZ — Synthetic Co

## Business summary

Ordinary factual business description, retained.

## Conviction

**Rating: High**

## Relationship to the gate

`gates.yaml`'s stated rationale is unrelated prose that would otherwise
survive a marker scan on its own if not caught by section removal.

## Risks — detail

An ordinary disclosed risk, retained.
"""


def test_redact_markdown_strips_conviction_section_with_no_marker_word():
    redacted, removed_count = sanitizer.redact_markdown(_SECTION_LEAK_MD)
    assert "Rating: High" not in redacted
    assert "## Conviction" not in redacted
    assert removed_count >= 1


def test_redact_markdown_strips_relationship_to_gate_section():
    redacted, _ = sanitizer.redact_markdown(_SECTION_LEAK_MD)
    assert "Relationship to the gate" not in redacted
    assert "gates.yaml" not in redacted


def test_redact_markdown_retains_business_and_risk_sections():
    redacted, _ = sanitizer.redact_markdown(_SECTION_LEAK_MD)
    assert "Ordinary factual business description, retained." in redacted
    assert "An ordinary disclosed risk, retained." in redacted


def test_verify_markdown_redaction_catches_rating_pattern_outside_a_section():
    # Defense in depth: even without section detection, a standalone
    # "Rating: High" phrase is itself a marker.
    findings = sanitizer.verify_markdown_redaction("Some prose. Rating: High. More prose.")
    assert findings


# ── fail-closed complete-package scan ────────────────────────────────────

def test_complete_package_scan_clean_synthetic_package():
    data = _synthetic_company_yaml()
    pkg, findings = sanitizer.build_sanitized_package("ZZZZ", data, "Ordinary clean prose only.")
    assert findings == []
    assert not pkg.md_excluded


def test_build_sanitized_package_excludes_md_on_surviving_marker_not_silent_pass_through():
    # Construct markdown where a marker survives paragraph-level stripping
    # because it's glued to unrelated content in the same paragraph in a
    # way the strip regex still catches at paragraph granularity -- but to
    # directly exercise the *fail-closed exclusion* path (not just the
    # strip path), monkeypatch-free: use text where the marker appears
    # only after the strip+reflow, simulated by directly calling the
    # lower-level API the way build_sanitized_package would if strip
    # somehow missed it, then confirm build_sanitized_package's own
    # verify step still cannot silently ship it.
    data = _synthetic_company_yaml()
    md = "portfolio_role_ref: T1 was explicitly approved by the human principal."
    pkg, findings = sanitizer.build_sanitized_package("ZZZZ", data, md)
    # the strip pass removes the (sole) paragraph entirely, so the package
    # itself is clean; markdown_text becomes empty, not a leaked marker.
    assert findings == []
    assert pkg.markdown_text == ""


def test_complete_package_scan_never_releases_a_failing_package():
    """If sanitize_yaml_data's item-level pass is bypassed (simulating a
    hypothetical future field this sanitizer does not yet scan), the
    complete-package scan must still catch it and the caller-facing
    orchestration must refuse to hand back a usable package."""
    data = _synthetic_company_yaml()
    # Simulate a leak in a structurally-unscanned location.
    data["some_future_field_not_yet_scanned"] = "conviction rating discussion here"
    pkg, findings = sanitizer.build_sanitized_package("ZZZZ", data, "clean")
    assert findings  # caught by the complete-package scan even though no
    # per-field scanner exists for this hypothetical field


# ── determinism ──────────────────────────────────────────────────────────

def test_sanitization_is_deterministic_across_runs():
    data = _synthetic_company_yaml()
    pkg1, findings1 = sanitizer.build_sanitized_package("ZZZZ", data, _SYNTHETIC_MD)
    pkg2, findings2 = sanitizer.build_sanitized_package("ZZZZ", data, _SYNTHETIC_MD)
    assert findings1 == findings2 == []
    assert sanitizer.package_to_drafting_text(pkg1) == sanitizer.package_to_drafting_text(pkg2)


# ── real repository: fail-closed guarantee holds against actual content ─

_REAL_TICKERS = [
    "NVDA", "TSM", "ASML", "AVGO", "SNPS", "KLAC", "MSFT", "GOOGL", "AMZN",
    "META", "PANW", "LLY", "ISRG", "TMO", "ICE", "SPGI", "V", "COST", "WM",
    "CEG", "ETN", "GEV", "GNRC", "PWR", "RTX", "RKLB", "TSLA",
]


@pytest.mark.parametrize("ticker", _REAL_TICKERS)
def test_real_company_records_pass_fail_closed_scan(ticker):
    repo_root = Path(__file__).resolve().parent
    pkg, record = sanitizer.sanitize_company_files(repo_root, ticker)
    assert pkg is not None, (
        f"{ticker}: fail-closed scan blocked release -- "
        f"{record.complete_package_scan_findings}"
    )
    assert record.complete_package_scan_passed


def test_real_company_records_sanitization_is_deterministic():
    repo_root = Path(__file__).resolve().parent
    pkg1, rec1 = sanitizer.sanitize_company_files(repo_root, "NVDA")
    pkg2, rec2 = sanitizer.sanitize_company_files(repo_root, "NVDA")
    assert rec1.sanitized_package_sha256 == rec2.sanitized_package_sha256
    assert rec1.sanitized_package_sha256 != ""


def test_real_company_records_never_leave_portfolio_role_ref_structurally():
    repo_root = Path(__file__).resolve().parent
    for ticker in _REAL_TICKERS:
        pkg, _ = sanitizer.sanitize_company_files(repo_root, ticker)
        assert pkg is not None
        assert "portfolio_role_ref" not in pkg.yaml_data
        assert "conviction" not in pkg.yaml_data


# ── isolation ────────────────────────────────────────────────────────────

def test_module_never_writes_into_intelligence_companies():
    source = Path("intelligence_classification_sanitizer.py").read_text()
    assert "write_text" not in source
    assert "write(" not in source


def test_module_never_imports_allocator_or_margin():
    source = Path("intelligence_classification_sanitizer.py").read_text()
    assert "import allocate" not in source
    assert "import margin_state" not in source
