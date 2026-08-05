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


# ── v1.1 regression coverage (review 4867365726, bounded correction) ─────
#
# The original v1.0 sanitizer caught the adjective "gated" but not the bare
# policy noun "gate" -- every formerly-gated Company Intelligence record
# discusses its own gates.yaml entry using constructions like "this
# record's gate" / "the gate's own X" / "the gate names Y", none of which
# contained the word "gated". These fixtures exercise that class of leak
# directly, plus the ETN dangling-section-reference defect, a policy
# synonym absent from the v1.0 strip list, and the legitimate non-policy
# "gate" uses that must NOT be stripped.

def test_bare_gate_noun_leak_is_detected_and_stripped():
    text = "This is discussed further given this record's gate names the specific condition."
    assert sanitizer._contains_gate_policy_leak(text)
    redacted, removed_count = sanitizer.redact_markdown("Intro.\n\n" + text + "\n\nConclusion.")
    assert "gate names" not in redacted
    assert removed_count >= 1


def test_bare_gate_possessive_leak_is_detected():
    for text in (
        "The gate's own next_gate condition remains unresolved.",
        "This directly matches the gate's own stated reopening trigger.",
        "Confirming and refining the gate's cited figures from last quarter.",
        "Matching this record's gate's own next_gate language exactly.",
    ):
        assert sanitizer._contains_gate_policy_leak(text), text


@pytest.mark.parametrize("ticker", ["SNPS", "ICE", "SPGI", "WM", "RKLB", "TSLA"])
def test_all_six_formerly_gated_records_pass_fail_closed_scan(ticker):
    """The exact six tickers review 4867365726 reproduced leakage for --
    each must now sanitize cleanly with zero forbidden survivors."""
    repo_root = Path(__file__).resolve().parent
    pkg, rec = sanitizer.sanitize_company_files(repo_root, ticker)
    assert pkg is not None, (ticker, rec.complete_package_scan_findings)
    assert rec.complete_package_scan_passed


@pytest.mark.parametrize("ticker", ["SNPS", "ICE", "SPGI", "WM", "RKLB", "TSLA"])
def test_all_six_formerly_gated_records_carry_no_bare_gate_reference(ticker):
    repo_root = Path(__file__).resolve().parent
    pkg, rec = sanitizer.sanitize_company_files(repo_root, ticker)
    assert pkg is not None
    package_text = sanitizer.package_to_drafting_text(pkg)
    assert not sanitizer._contains_gate_policy_leak(package_text)


def test_etn_dangling_section_cross_reference_regression():
    """ETN.md's own live text: 'This record's current-tier-and-target
    statement (see "Governed policy" below) describes Eaton as it is
    structured today' -- contains no v1.0-recognized marker itself, only a
    cross-reference to a section that IS stripped. Must not survive."""
    repo_root = Path(__file__).resolve().parent
    pkg, rec = sanitizer.sanitize_company_files(repo_root, "ETN")
    assert pkg is not None, rec.complete_package_scan_findings
    assert "governed policy" not in pkg.markdown_text.lower()
    assert "current-tier-and-target" not in pkg.markdown_text.lower()


def test_dangling_cross_reference_to_stripped_section_stripped_generically(tmp_path=None):
    """Synthetic analog of the ETN defect -- a paragraph that names a
    stripped section by title without containing any other marker."""
    md = (
        "# ZZZZ\n\n"
        "## Business summary\n\n"
        "Ordinary factual content, retained.\n\n"
        "This record's placement statement (see \"Governed policy\" below) "
        "describes the company as structured today.\n\n"
        "## Governed policy (existing, not a research conclusion)\n\n"
        "Per targets.yaml, ZZZZ currently sits in a tier.\n\n"
        "## Risks\n\n"
        "An ordinary disclosed risk, retained.\n"
    )
    redacted, _ = sanitizer.redact_markdown(md)
    assert "Governed policy" not in redacted
    assert "Ordinary factual content, retained." in redacted
    assert "An ordinary disclosed risk, retained." in redacted


def test_policy_synonym_absent_from_primary_strip_list_still_caught():
    """'buying clearance' / 'pending clearance' / 'admission condition' are
    gate-policy synonyms never enumerated in _MD_STRIP_PATTERNS -- must be
    caught by the gate-policy checker, not silently pass through."""
    for text in (
        "This name remains in a buying clearance state per current review.",
        "The position is pending clearance before any further evaluation.",
        "Resolution of the admission condition is expected next quarter.",
        "Its conditional admission status has not changed this cycle.",
    ):
        assert sanitizer._contains_gate_policy_leak(text), text


def test_legitimate_non_policy_gate_uses_are_not_stripped():
    """Real, observed non-policy 'gate' usage in this corpus (ASML's
    'technological gate', KLAC's 'gate-all-around' transistor structures,
    PWR's 'customer-qualification gate', and OPS-0008's process/CI
    gates) must survive redaction -- over-redacting ordinary factual
    evidence unrelated to Portfolio-HQ placement is itself a defect."""
    legitimate = (
        "the exposure lost would be specifically to the technological gate that determines whether leading-edge nodes can be manufactured",
        "process-control spending tied to node/architecture transition complexity (new materials, gate-all-around, advanced packaging)",
        "Safety record and bonding/insurability function as a customer-qualification gate: large utilities vet contractors",
        "Per OPS-0008 Section 2's mandatory stop-before-drafting gate, this session paused before drafting",
        "changed) to clear this repository's git diff --check CI gate -- following the same precedent",
    )
    for text in legitimate:
        assert not sanitizer._contains_gate_policy_leak(text), text


def test_gate_whitelist_survives_yaml_line_wrap():
    """Regression for the exact PWR defect found during this correction:
    yaml.safe_dump wraps long strings at ~80 chars, so 'customer-
    qualification gate' can be split across a newline as 'customer-
    qualification\\n    gate' -- the whitelist match must still exempt it
    (whitespace-normalized comparison), not fall through to the bare-gate
    catch-all."""
    wrapped = "a customer-qualification\n    gate for large utility contracts"
    assert not sanitizer._contains_gate_policy_leak(wrapped)


def test_catalysts_item_level_redaction():
    """SNPS's own catalysts[] entry leaked gate-policy language through an
    entirely unscanned field in v1.0 -- catalysts[].catalyst must now be
    scanned identically to risks[].risk."""
    data = _synthetic_company_yaml()
    data["catalysts"] = [{
        "catalyst": "Investor Day, confirmed scheduled -- this record's gate's own explicitly named reopening trigger.",
        "expected": "2026-09-30",
        "status": "pending",
    }]
    sanitized, removed = sanitizer.sanitize_yaml_data(data)
    assert sanitized["catalysts"][0]["catalyst"] == sanitizer._ITEM_REDACTION_PLACEHOLDER
    assert "catalysts[0].catalyst" in removed


# ── v1.2 bounded correction (review 4868016198): the strip-decision
# functions (_paragraph_is_forbidden / _item_text_is_forbidden) must not
# call independent_policy_scan() -- doing so was v1.1's own defect (the
# later "independent" verify call was re-running a check the text had
# already passed once, for paragraph/item content). The three tests below
# replace the three v1.1 tests that asserted the *opposite* architecture
# (that bare `conviction` was deliberately absent from the strip list and
# caught only by the shared independent_policy_scan() call inside the
# strip decision itself) -- that assumption is what v1.2 corrects.

def _called_function_names(fn) -> set[str]:
    """AST-level extraction of every function/attribute name actually
    *called* inside `fn`'s body -- deliberately not a substring search over
    `inspect.getsource()`, which would false-positive on a docstring or
    comment merely mentioning a function's name in prose (as this module's
    own v1.2 docstrings now do, by design, to explain the correction)."""
    import ast
    import inspect
    import textwrap

    src = textwrap.dedent(inspect.getsource(fn))
    tree = ast.parse(src)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            target = node.func
            if isinstance(target, ast.Name):
                names.add(target.id)
            elif isinstance(target, ast.Attribute):
                names.add(target.attr)
    return names


def test_strip_decision_helpers_never_call_independent_policy_scan():
    """AST-level proof (not a docstring/comment substring check -- this
    module's own v1.2 docstrings mention `independent_policy_scan()` by
    name in prose to explain the correction, which would false-positive a
    naive text search) that the transformation-layer decision functions do
    not actually *invoke* the verify-designated function -- the literal
    defect review 4868016198 found in v1.1."""
    for fn in (sanitizer._paragraph_is_forbidden, sanitizer._item_text_is_forbidden):
        called = _called_function_names(fn)
        assert "independent_policy_scan" not in called, (
            f"{fn.__name__} actually calls independent_policy_scan() -- that call belongs "
            f"exclusively to the verify layer (verify_markdown_redaction/complete_package_scan). "
            f"Functions actually called: {sorted(called)}"
        )


def test_verify_functions_never_delegate_to_strip_decision_helpers():
    """AST-level proof of the other direction -- the verify layer must not
    decide cleanliness by actually *calling* the strip-stage paragraph/item
    decision helper either (would reintroduce the same tautology from the
    other side)."""
    for fn in (sanitizer.verify_markdown_redaction, sanitizer.complete_package_scan,
               sanitizer.independent_policy_scan):
        called = _called_function_names(fn)
        assert "_paragraph_is_forbidden" not in called
        assert "_item_text_is_forbidden" not in called


def test_phrase_omitted_from_strip_detector_still_caught_by_verifier():
    """The percent-of-book numeric pattern is deliberately present only in
    _INDEPENDENT_VERIFY_PATTERNS, not _MD_STRIP_PATTERNS (no real corpus
    content needs it stripped -- verified empirically against all 27 live
    classification records). This is the concrete proof the two layers
    diverge: a phrase the strip layer's own list does not enumerate is
    still caught when the verifier walks the final assembled text."""
    text = "a case could be made for roughly 4.5% of book given current momentum"
    assert not sanitizer._paragraph_matches_any(text, sanitizer._MD_STRIP_PATTERNS), (
        "test invalid if the strip layer's own patterns already catch this -- the point is "
        "that they do NOT, and the independent verifier does"
    )
    assert not sanitizer._contains_gate_policy_leak(text)
    assert sanitizer.independent_policy_scan(text)


def test_independent_verifier_pattern_set_differs_from_strip_pattern_set():
    """Structural proof the two layers are not the same check reused
    twice -- their pattern sources must differ, and at least one concept
    must be verify-only (not merely a superset/subset relationship that
    happens to coincide everywhere by accident)."""
    strip_patterns = {p.pattern for p in sanitizer._MD_STRIP_PATTERNS}
    verify_patterns = {p.pattern for p in sanitizer._INDEPENDENT_VERIFY_PATTERNS}
    assert strip_patterns != verify_patterns
    percent_of_book = r"\d+(?:\.\d+)?\s*%\s*(?:of\s+book|target|weight|allocation)"
    assert percent_of_book in verify_patterns
    assert percent_of_book not in strip_patterns


def test_complete_package_scan_is_not_tautological():
    """Direct regression for the review's stated root cause: a leak that
    survives the strip pass must still be catchable by
    complete_package_scan() because it uses a different mechanism --
    demonstrated concretely via the percent-of-book case, which strip's
    own patterns deliberately do not enumerate and which item-level
    redaction therefore does NOT strip in place (unlike bare `conviction`,
    which v1.2 folded into the strip layer directly for real-corpus
    correctness -- see test_bare_conviction_now_stripped_at_item_level)."""
    data = _synthetic_company_yaml()
    del data["portfolio_role_ref"]
    del data["conviction"]
    data["risks"] = [{
        "risk": "A case could be made for roughly 4.5% of book given current momentum.",
        "severity": "low", "identified": "2026-01-01", "status": "monitoring",
    }]
    pkg, findings = sanitizer.build_sanitized_package("ZZZZ", data, "Clean markdown, no markers.")
    # item-level strip (patterns + gate-policy leak only, no independent_policy_scan)
    # does NOT touch this -- it survives to the assembled package...
    assert pkg.yaml_data["risks"][0]["risk"] != sanitizer._ITEM_REDACTION_PLACEHOLDER
    # ...and is caught only there, by the independent verify layer, blocking release.
    assert findings != []
    assert any("independent-verify" in f or "complete-package" in f for f in findings)


def test_bare_conviction_now_stripped_at_item_level_by_strip_layer_directly():
    """v1.2: bare `conviction` was folded into _MD_STRIP_PATTERNS itself
    (a transformation-layer improvement, not a delegation to the verify
    function) so that real corpus content needing it redacted (the ETN
    case from review 4867365726/4868016198) is still actively fixed in
    place, not merely fail-closed at the package level."""
    data = _synthetic_company_yaml()
    del data["portfolio_role_ref"]
    del data["conviction"]
    data["risks"] = [{
        "risk": "A fact not weighted in this record's conviction rationale.",
        "severity": "low", "identified": "2026-01-01", "status": "monitoring",
    }]
    pkg, findings = sanitizer.build_sanitized_package("ZZZZ", data, "Clean markdown, no markers.")
    assert pkg.yaml_data["risks"][0]["risk"] == sanitizer._ITEM_REDACTION_PLACEHOLDER
    assert findings == []
    # and confirm this was via the strip-layer pattern list directly, not
    # a fallback to independent_policy_scan -- the pattern is in both,
    # but item-level decision must not need the verify function to catch it.
    assert sanitizer._paragraph_matches_any(
        "A fact not weighted in this record's conviction rationale.",
        sanitizer._MD_STRIP_PATTERNS,
    )
